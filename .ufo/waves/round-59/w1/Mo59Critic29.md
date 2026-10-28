# Mo59Critic29 — hostile file-content robustness probe (C1/C2 counters + the two landed tools)

Scope: counter robustness under hostile file content — CRLF scorecard, NaN
manifest, BOM entry — plus nearby encoding attacks (non-UTF-8, bool-pun,
malformed-grammar, row-binding gaps). Read-only on the lane; all experiments on
a throwaway repo under `$HYAKU_SCRATCH/mori-r59/Mo59Critic29/lanehostile`
(cleaned before yield). Freeze `60b3a76a`, entering `2b9f0397`; probe repo
built from lane `HEAD` (`8ff344ff`) bytes only — same tool/fixer SHAs
(`38b733d8…`, `4c04bf21…` verified against frozen PINs). Baseline on the
scratch repo: `C1=met … rev=HEAD` and `C2=met … claims=11 files=6`, both rc 0
— mutations are measured against that green baseline.

Method: `mutate.py` applies one content mutation, commit, run frozen counter at
`HEAD` with `--repo <scratch>` (`--fleet` = real fleet for C1's
`MANIFEST_REV`), `git reset --hard` back. Tools probed directly via
`importlib` (`check()`, `scan_file()`). Counter selftests green first:
`C1_SELFTEST 6/0`, `C2_SELFTEST 9/0`, `REGCHECK 12/0`, `SETSCAN 10/0`.

## Findings

### F1 — C2 counter crashes (no verdict line) on non-UTF-8 committed content — defect, fixable

`eval_entry` catches `OSError` around `read_text(encoding="utf-8")`
(`count-c2.py:106-109`) but `UnicodeDecodeError` is a `ValueError`, not an
`OSError` — it propagates through `measure()` and `main()` and kills the run
with a traceback and **no `C2=` line at all**, rc 1.

Reproductions (each a single committed-bytes mutation in the scratch repo,
counter run at `HEAD`):

- non-UTF-8 real entry →
  `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 40`
  (traceback tail; zero output tokens)
- non-UTF-8 `corpus/SOURCES.md` → same crash at `count-c2.py` line reading
  `reg = (root / SOURCES).read_text(...)`
- a 13th hostile tree `trees-c2/t13-nonutf8/` whose entry is `\xff\xfe…` →
  same crash *in the trees arm*: one malformed fixture DoSes the entire
  counter run before `trees=`/`failed=` are printed.
- C1 twin: a fixture `expect.txt` of `\xff\xfe` crashes `count-c1.py:140`
  `expect = exp_b.decode()...` — traceback, no `C1=` line.
- Tool twin: `mori-register-check.py` catches only `OSError` on the scorecard
  read (`regcheck.py:108-111`); non-UTF-8 scorecard → tool crash, no JSON
  (the counter tolerates this: `out=None` → `real=bad`, stays alive). The
  tool's manifest read *does* survive because `ValueError` is in its catch —
  asymmetric.

Impact: never a false `met`, but a committed hostile/accidental non-UTF-8
file turns a clean `C?=unmet failed=<reason>` verdict into an unlabeled crash,
and for the trees/fixtures arm it aborts evaluation of *sibling* trees.
Smallest safe correction: catch `ValueError` (or `UnicodeDecodeError`)
alongside `OSError` in `eval_entry`'s entry and SOURCES reads, and wrap
`exp_b.decode()`/the tree-arm `eval_entry` call so a bad committed blob
yields `entry_absent`-style/`tree:<n>:verdict` failure rather than process
death. C1 symmetric at `count-c1.py:140`.

### F2 — C2 drift arm accepts *any* non-zero exit as "drift detected" — defect, fixable

`count-c2.py` (drift arm): `drift_ok = p.returncode != 0` — no check that the
tool emitted `SETTLEMENT_SCAN_FAIL` (or any JSON). A r53 file that is
non-UTF-8 crashes the tool (F1 twin); the crash is scored `drift=ok`:

    drift-nonutf8 → C2=met selftest=ok scan=ok drift=ok trees=ok … rc=0

The `drift=ok` token certifies "schema drift observed" when the tool never
produced a verdict — silent collapse of {crash, unreadable, not-json} into
"drift". Smallest safe correction: require
`out.get("verdict") == "SETTLEMENT_SCAN_FAIL"` (parse `p.stdout` like the scan
arm does) in addition to rc≠0.

### F3 — grammar-verdict asymmetry between the trees arm and the real-entry arm — defect, fixable

`eval_entry` returns `ok=False` for any `grammar:` reason, but the real-entry
arm's `entry_ok` prefix tuple
(`("frontmatter","distinct","claims_min","files","span","entry_absent")`,
`count-c2.py:311-314`) omits `grammar` — the same bytes that make a hostile
tree `verdict=false` are `entry=ok` when committed as the real entry:

- `entry-bom-claim` (UTF-8 BOM glued to the K2 claim line):
  `eval_entry` → `ok=False, reasons=['grammar:\ufeff- **K2** — …']`, yet
  `C2=met … entry=ok … claims=10` — the corrupted claim silently drops out of
  the count instead of failing the entry.
- `entry-malformed` (appended `- **KX** — malformed Quote: …`):
  `eval_entry` → `ok=False, reasons=['grammar:- **KX** …']`, yet `C2=met`.

So one evaluator, two verdicts on identical content. If `grammar` is meant as
"claim-looking lines must parse" (its role in the frozen trees), the real arm
should add `grammar` to the prefix set; if it's meant informational, the
trees arm shouldn't let it fail `ok` — pick one. Caveat for the canonical
judge: the predicate's literal `>=10 claims in the frozen grammar` is still
satisfied (malformed lines never *inflate* the count), so this is a
consistency/reporting defect, not a met-inversion.

### F4 — `seats`/`round` bool-pun passes the settlement scan — tool-level schema hole, latent

`setscan.py:62` uses `isinstance(seats, int)` and `seats == len(results)`;
Python `True == 1`, so `{"seats": true, "round": true, "results":[<1 member>]}`
produces `SETTLEMENT_SCAN_OK` and a summary `members==seats`. Demonstrated
end-to-end inside a `C2=met` run (`scan-boolpun`: artifact + copy rewritten
byte-identically, entry re-pinned → `C2=met … scan=ok`). Also `note: NaN` and
any `NaN`/`Infinity` in uninspected fields pass (`json.loads` non-strict).
Reachability caveat: the predicate only needs `round>=1` int and
`seats==len(results)`, so the pun needs a 1-seat file or `seats: false` with
0 results — no current wave shape hits it; classify as latent tool defect.
Smallest fix: `type(seats) is int` (and same for `round`), plus
`parse_constant` to reject `NaN`/`Infinity`.

### F5 — row-binding covers only SIDs in the first ten lines — coverage hole, borderline

`sids` are collected only from `head = lines[:10]`
(`count-c2.py:151-153`). A `source: S989` line appended at the bottom of the
entry cites an S-row the `rows` arm never binds:

    entry-body-source → C2=met … rows=ok   (S989 has no registry row at all)

The frozen predicate says "every S### the entry's source lines cite" — if
"source lines" means the frontmatter block only, current behavior is correct;
if any `source:` line in the entry counts, this is a real hole. Either way a
citation outside line 10 is silently ignored. Cheap hardening: scan all lines
for `source:`/`S###` citations but keep frontmatter-key presence check at
`[:10]`.

### F6 — duplicate quotes amplify the claim count under distinct K ids — spirit violation, letter-clean

Only `K<id>` distinctness is enforced (`distinct:dup=K…`); nothing checks
duplicate `(file, kind, n)` facts. `entry-dupquote-mass` rewrote K2–K8 to
byte-identical copies of K1's span: `C2=met … claims=11 files=3` with only 4
unique quoted facts (5 files' worth collapsed). The contract's round-58
routed defect #4 says "distinct claims" — the frozen counter reads that as
distinct K ids, so an entry can hit `claims>=10` with <10 facts. Every claim
is still genuinely byte-exact/pin-bound, so this inflates count, never
falsifies a span. Correction: add `(cfile, kind, n)` dedup or a
`distinct:span` reason — flag for the judge whether "distinct claims" was
meant to cover duplicate spans.

### Confirmed-robust surface (no counterexample found)

- **CRLF scorecard** → `C1=met` identical to baseline (universal-newline
  `read_text` + `splitlines` absorb `\r\n` through `## `-head, table-cell and
  key matching).
- **CRLF entry** → `C2=met` (claim regex anchored per `splitlines` line;
  `\r` can't live inside a matched claim line, so no smuggling).
- **CRLF SOURCES.md** → `C2=met`.
- **BOM entry** → `C2=unmet … failed=entry`, rc 1 — robustly rejected via
  `frontmatter:source` (SID regex still sees the line; rows bound anyway).
  Same rejection shape when planted as a hostile tree (`tree-bom-entry` →
  still `C2=met`, tree correctly false).
- **BOM on the `## Capabilities` heading** → `C1=unmet real=bad` with tool
  reasons `binding:declared_register=0(capabilities_sections=2),
  keys:missing×2` — clean rejection, not a crash.
- **BOM scorecard file-level** → `C1=met` (BOM lands on the `# title` line;
  harmless).
- **NaN manifest (tool level)**: `NaN` in `capabilities_added`,
  `lane_round`, or `rounds` → `manifest:entry_missing` / `lane_round` /
  `unreadable`; `Infinity` same. Non-strict JSON tolerated only in
  *uninspected* fields (`{"meta": NaN, "rounds": […]}` → ok=True) — cosmetic,
  since the bound fields must be real strings/ints.
- **scan-nonutf8** (REAL_SCAN artifact corrupted): `C2=unmet
  failed=scan,tree,tree:corpus/evidence/sources-r59/w1-results-r54.json` —
  correctly fails, and the tree arm catches the copy/artifact divergence.
- **sources-row-bom**: `C2=unmet failed=rows` — BOM'd S991 row isn't found.
- No false-`met` was produced by any content mutation; the failure modes are
  crash-instead-of-verdict (F1), reason-token collapse (F2), asymmetric
  verdict mapping (F3), latent schema pun (F4), and coverage interpretation
  (F5/F6).

## Evidence bundle

Scratch (removed before yield per round rules): repo
`$HYAKU_SCRATCH/mori-r59/Mo59Critic29/lanehostile`, baseline commit
`19474629…` — `mutate.py`, `run_mut.sh`, `toolprobe.py`, `gen_entry.py`,
`regen_entry.py`, `out-*.txt` per run. Exact reproduction commands:

    # counter-level (after `mutate.py <name>` + commit):
    python3 .ufo/waves/round-59/count-c2.py HEAD \
        --repo $HYAKU_SCRATCH/mori-r59/Mo59Critic29/lanehostile \
        --scratch <dir>
    python3 .ufo/waves/round-59/count-c1.py HEAD \
        --repo <same> --fleet /home/vgpnk/Projects/shokunin --scratch <dir>

Key line pointers: `count-c2.py:106-109` (OSError-only catch),
`:140`-analog `count-c1.py:140` (`exp_b.decode()`), `count-c2.py` drift arm
(`p.returncode != 0`), `count-c2.py:311-314` (`entry_ok` prefix tuple sans
`grammar`), `count-c2.py:151-153` (SIDs from `lines[:10]` only),
`setscan.py:62` (`isinstance(·, int)` bool-pun),
`regcheck.py:108-111` (scorecard OSError-only catch vs manifest's
ValueError-inclusive catch).

Impacted axes: calibration (F1 twin on C1, F5-adjacent trust in `real=`
tokens) and depth (F1–F6 on C2); none inverts a `met`/`unmet` verdict on the
committed corpus — they degrade reason fidelity and crash-safety of the
counting instruments themselves.
