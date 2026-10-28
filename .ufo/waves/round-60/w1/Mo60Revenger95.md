# Mo60Revenger95 — r59 C2 decertification chain, per-class verdicts at r60

Seat: Mo60Revenger95 (revenger, leaf). Assignment: reconstruct the r59 C2
decertification chain from `Mo59Critic22`/`Mo59Critic23`/`Mo59Critic25`/
`Mo59Reviewer08` and give one verdict per class on whether the r60 instrument
now rejects it. Work read-only: no lane/fleet writes beyond this report, no VCS
mutation, no installs, no subagents.

## Verdict summary

| Class (r59 source) | r59 witness on r60 instrument | Verdict |
|---|---|---|
| Semantically-empty entry (Critic22 D1: text unchecked; false K9) | `text:short`/`text:dup` ⇒ `ok=False` ⇒ `C2=unmet` | **PARTIAL** — r59 witness rejected; class open (10 *distinct* ≥10-char texts, all false, still `C2=met`) |
| Alias / vacuous spans (Critic23 F1–F3, Reviewer08 dup-content; Critic22 D2) | `distinct:dup_span`, `span:blank`, `span:short` ⇒ `C2=unmet` | **PARTIAL** — line/offset alias + short/blank spans rejected; same content at genuinely distinct spans admitted |
| Drift confound (Critic25 M1 filename heuristic, M3 wrong-axis) | H5 attribution `:extra_keys=` + renamed r54 control | **CLOSED** for M1/M3 and for the real r53 file (67/67 reasons are `:extra_keys=`); residual: additive wrong-axis mutant M2 still passes the arm (test power only — tool bytes are sha-pinned) |
| Grammar orphan (Critic22 D3 / Reviewer08 F1: `grammar:` reached no arm) | grammar reason now makes `ok=False`; counter entry gate consumes `ok` | **CLOSED** — real r59 entry + one malformed claim line ⇒ `grammar:` only ⇒ `C2=unmet entry=bad` |

Adjacent r59 defects also closed by construction: row↔copy binding (Critic22
D4 / Critic23 F4) → `rows:binding` (tree `h07`); stale pin / wrong line /
frontmatter (`h10`–`h12`).

## Pins and revision discipline

Lane tip moved under me as the ticket warned; every re-derivation is pinned.

- Entering revision: `ddfb12fb0838b4307c445194a844f0c4b1950195`.
- Frozen (amended) revision under test: `ac496c7cde8cad965079858accae3bedfe4a73f2`.
- Lane tip when read: `b3c256138f00c704d5aa56eb0332d74506502ef2` (C1 data had
  landed: receipts/absent-set/SCORECARD/SOURCES S561–S564).
- Data provenance for the fixture: blobs at `b3c25613`; the real entry and the
  six copies are **byte-identical at `ac496c7c` and `HEAD`**
  (`wave-settlement-artifacts-r59.md` sha256 `441a751d…`, copy r54
  `ea48a0cc…`). `corpus/SOURCES.md` differs between the two revs (S561–S564 +
  registry-table move); rows S553–S558 used by the entry parse identically
  (11 cells, `mined`, used-by the entry).

Instrument bytes — verified equal in the working tree, at `ac496c7c`, and at
the lane tip:

```
8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976  .ufo/waves/round-60/count-c2.py
cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69  tools/mori-entry-claims-check.py
4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9  tools/mori-settlement-scan.py
ae90c90f2c5d47952d38b8f10a3ea4608a225a03765a60571b48ba25575cc2ee  .ufo/waves/round-60/trees-c2h-expects.json
$ git show ac496c7c:<same three paths> | sha256sum   → identical
$ git diff --stat ac496c7c HEAD -- .ufo/waves/round-60 tools/…
  (only w1-spec/dispatch/evidence/absent-set added; no instrument byte change)
```

Tip movement during the seat: the lane advanced `b3c25613` → `0f8340cf`
(round-60 lesson landing) and `corpus/lessons/round-60.md` carries another
seat's uncommitted `MM` edits. Re-verified at `0f8340cf`: the three instrument
shas above are unchanged and registry rows S553–S555 still parse (11 cells,
`mined`, source cell names the artifact path), so every verdict below holds
independently of the tip. No lane file was written by this seat.

## Method (read-only)

1. Read the four r59 reports and both r60 instruments in full.
2. Built a throwaway fixture repo at an explicit scratch path
   `$HYAKU_SCRATCH/mori-r60/Mo60Revenger95/fixture`
   (`git -C <fixture> init -q`, assertion `git -C … rev-parse --show-toplevel`
   printed that dir) containing only the paths the counter reads: both tools,
   `round-53` drift file, the five `round-{54..58}` scan files,
   `round-58/evidence/w1-settlement.json`, all 117 files of the 13
   `trees-c2h/` trees (9 each), the six copies, `corpus/SOURCES.md`, and the
   real entry.
3. Ran the frozen counter against that repo at each variant commit; ran the
   frozen verifier directly on the same roots to obtain per-reason attribution
   (`--root <root> --entry … --registry corpus/SOURCES.md --artifacts-json …`).
4. Replayed the Critic25 mutants as byte-modified copies of the pinned scan
   tool under scratch and evaluated the counter's exact H5 predicates
   (`count-c2.py:249-270`).
5. Re-derived the claim at the frozen revision against the lane itself
   (`--repo .`, read-only `git show`/`ls-tree` only).

Baseline reproduction (frozen target line, independently re-derived):

```
$ python3 .ufo/waves/round-60/count-c2.py ac496c7cde8cad965079858accae3bedfe4a73f2 \
    --repo . --scratch $S/run-lane-freeze
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok \
claims=13 files=6 spans=13 rev=ac496c7cde8cad965079858accae3bedfe4a73f2      exit 0
```

Same line on the fixture control commit `3c702e63` (byte-identical outputs,
`rev=` differs): `claims=13 files=6 spans=13`, exit 0. No false negative on
the real r59 entry.

Selftests on the frozen bytes: `C2_SELFTEST pass=8 fail=0` (exit 0),
`ENTRYCLAIMS_SELFTEST pass=13 fail=0` (exit 0).

## Class 1 — semantically-empty entry

**r59 witness** (Critic22 §Counterexample): 10 claims, nine texts `x.`, one
plainly false text, all ten quoting the same 6-byte span `"lane"` at offset 3,
plus a dangling `K99` line; scored `C2=met claims=10 files=5`.

**r60 result — witness rejected, class open.**

(a) Exact replay as a fixture commit `7b5306ba` (texts `x.`, one false text,
aliased `"lane"@offset:3`, `K99` present; 1 file):

```
TOOL rc=1 ok=False stats={'claims':10,'files':1,'spans':1,'min_span':6}
  reasons: grammar:- **K99** …, text:short=K1..K8,K10, text:dup=…, files_min:1,
           span:short=K1..K10, distinct:dup_span=K1=K2..K10
COUNT C2=unmet … entry=bad … claims=10 files=1 spans=1  (exit 1)
```

(b) Isolation of H3 (text check) — commit `962a2157`: 10 claims over 3 files
with **distinct, real, byte-exact spans** (10 spans, min 13 bytes) but every
text `x.`:

```
TOOL rc=1 ok=False stats={'claims':10,'files':3,'spans':10,'min_span':13}
  reasons: text:short=K1..K10, text:dup=K1=K2..K10         (nothing else)
COUNT C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=ok pins=ok
      tree=ok claims=10 files=3 spans=10 rev=962a2157…     (exit 1)
```

`spans == claims == 10`, `files >= 3`, rows/pins clean — the **only** failing
arm is `entry`, so the rejection is caused by the degenerate text, not by span
aliasing or a co-traveling arm. Line pointers: text reasons
`tools/mori-entry-claims-check.py:128-133`; `ok = len(reasons)==0` at `:239`;
counter entry gate requires `out["ok"] is True` and `spans == claims`
`.ufo/waves/round-60/count-c2.py:329-332`; `met` includes `entry_ok`
`:410-412`.

(c) **Residual (the class is not closed)** — commit `9d056853`: 10 claims,
three files, ten distinct real spans (min 13 bytes), pins exact, rows bound,
**no malformed line**, texts ten *distinct* ≥10-char sentences that are all
false about the quoted bytes (e.g. “The artifact stores waveform audio in YAML
format”, “Round fifty-four recorded nine hundred seats”, “The results array
holds no member entries”):

```
TOOL rc=0 ok=True stats={'claims':10,'files':3,'spans':10,'min_span':13} reasons=[]
COUNT C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok
      tree=ok claims=10 files=3 spans=10 rev=9d056853…      (exit 0)
```

So `C2=met` is still attainable by a zero-information entry whose texts pass a
length/distinctness floor. This matches the frozen predicate literally (H3 is
“pairwise distinct and ≥10 chars”), so it is not a predicate violation — but
it means the r59 conclusion “C2 certifies shape, not depth” survives H3.
Critic22's own K9 (the false sentence) is *not* a reason on the instrument at
all; only the nine `x.` lines are.

## Class 2 — alias / vacuous spans

**r59 witnesses:** Critic23 F1 (`line:1` ≡ `offset:0` on a one-line file),
F2 (10 claims over ~20 distinct bytes; same text at several positions),
F3 (whitespace-only quote), Reviewer08 duplicate-content claims; Critic22 D2
(all ten claims one 6-byte span).

**r60 result — aliasing and degeneracy rejected; vacuous-but-distinct spans
admitted.**

(a) Line/offset alias, commit `806f20d0`: `K1` cites r54 `line:2` (span
`(2,18)`), `K2` cites the same bytes as `offset:2`; 8 further distinct real
line spans; texts distinct:

```
TOOL rc=1 ok=False stats={'claims':10,'files':3,'spans':9,'min_span':13}
  reasons: ['distinct:dup_span=K1=K2']                     (single reason)
COUNT C2=unmet … entry=bad … claims=10 files=3 spans=9      (exit 1)
```

Span key is `(cfile,start,end)` — `tools/mori-entry-claims-check.py:160-167` —
so line/offset aliasing collapses, exactly the routed defect.

(b) Short/blank spans: `h05-short-quotes` → `span:short=K1..K4`,
`claims_min:4`, `files_min:1`; `h04-blank-quote` → `span:blank=K1`
(`:153-155`, `:168-169`). Whitespace-only quotes die on `not q.strip()`, so
Critic23 F3 is closed for any artifact.

(c) **Residual:** distinctness is per *span*, not per content, and there is no
requirement that a claim's span support its text. The accepted residual entry
`9d056853` above contains three claims quoting the **identical** 16-byte text
` "lane": "mori",` at three distinct file spans — accepted. Likewise any set
of ≥8-byte substrings at distinct offsets passes. This is the frozen H2 letter
(“claims resolve to distinct byte spans … ≥8 distinct bytes per span”), not an
implementation defect; it bounds the class to aliasing/degeneracy only.

## Class 3 — drift confound

**r59 witness** (Critic25): the old arm read only `returncode != 0` on the r53
file, so a filename heuristic (M1) or a wrong-axis predicate (M2: non-null
`note`) passed; r53 differs from r54–r58 on ≥3 independent axes.

**r60 arm** (`.ufo/waves/round-60/count-c2.py:229-270`): r53 must fail with
verdict `SETTLEMENT_SCAN_FAIL` **and** at least one reason containing
`":extra_keys="` (`DRIFT_REASON`, `:81`), **and** r54 bytes materialized at
`round-53-alias/w1.json` must scan `SETTLEMENT_SCAN_OK` (`:253-269`).

Mutant replay (byte copies of the pinned scan tool under scratch; predicates
applied exactly as `:249-270`):

| tool | r53 file rc / verdict / reason sample | control path rc/verdict | attributed | ctrl | arm |
|---|---|---|---|---|---|
| pinned `4c04bf21…` | 1 / FAIL / `member[0]:extra_keys=report_file` (67 reasons) | 0 / OK | True | True | **True** |
| M1 `+if "round-53" in str(path): fails.append("drift_path")` | 1 / FAIL / `drift_path` (68) | 1 / FAIL | True | False | **False** |
| M2 (Critic25 additive) `+ if note is not None: fails.append("note_not_null")` | 1 / FAIL / `member[0]:extra_keys=report_file` (134) | 0 / OK | True | True | **True** |
| M3 pure wrong-axis substitution `:extra_keys=` → `:wrong_axis=` | 1 / FAIL / `member[0]:wrong_axis=report_file` (67) | 0 / OK | **False** | True | **False** |

Real-file attribution: `all(":extra_keys=" in r for r in reasons) = True`,
reason families `Counter({'extra_keys': 67})`. The r59 confound (nonzero exit
attributable to any of several axes) is resolved for the real measurement: the
failure is the member key-set check.

**Residual:** the arm tests *presence* of the right reason, not exclusivity, so
Critic25's additive M2 still passes (the genuine `extra_keys` reasons co-occur,
`134 = 67 + 67`). This is test power, not an exploitable hole: the scan tool is
sha-pinned (`PIN_SCAN`, `count-c2.py:49-51`) and G1 refuses to execute
unpinned bytes, so no attacker can substitute M2 for the real tool. The
contract's H5 sentence claims only that “the filename-heuristic mutant dies” —
which is true.

## Class 4 — grammar orphan

**r59 witness** (Critic22 D3, Reviewer08 F1): `eval_entry` emitted `grammar:`
for malformed claim lines but the live arm partitioned reasons by prefix and
never routed `grammar`, so ten good claims plus one malformed line scored
`C2=met` end-to-end.

**r60 result — closed.** Replayed on the **real r59 entry** (commit
`1bc6a93a`: identical bytes plus one appended
`- **K11** — dangling claim with no pin or span`):

```
TOOL rc=1 ok=False stats={'claims':13,'files':6,'spans':13,'min_span':12}
  reasons: ['grammar:- **K11** — dangling claim with no pin o']
COUNT C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=ok pins=ok
      tree=ok claims=13 files=6 spans=13 rev=1bc6a93a…        (exit 1)
```

`spans == claims == 13`, `files == 6`, rows/pins clean — the sole difference
from the met control is the malformed line, and it alone flips `entry=bad`.
Mechanism: `grammar:` is appended at `tools/mori-entry-claims-check.py:115-117`
and `ok` is `len(reasons)==0` at `:239`; the counter now consumes `ok` rather
than re-partitioning prefixes (`count-c2.py:329-332`), and the hostile-tree arm
demands the same boolean (`:397-399`). Frozen tree `h02-malformed-claim`
evaluates `grammar` + `ok=False` (verified directly, below).

## Hostile-tree coverage read (13 trees, `trees-c2h-expects.json`)

Direct evaluation of the frozen verifier on each tree root (counter arm
`trees=ok` in every run above demands the same verdicts):

| tree | tool ok | reason families |
|---|---|---|
| h00-good-control | True | — (claims=10 files=4 spans=10) |
| h01-semantically-empty | False | `grammar`, `text:short`, `text:dup`, `span:short`, `distinct:dup_span`, `files_min:1` |
| h02-malformed-claim | False | `grammar` only |
| h03-line-offset-alias | False | `distinct:dup_span=K1=K10` only |
| h04-blank-quote | False | `span:blank=K1` |
| h05-short-quotes | False | `span:short=K1..K4`, `claims_min:4`, `files_min:1` |
| h06-degenerate-text | False | `text:short`, `text:dup`, `distinct:dup_span`, `files_min:2` |
| h07-single-row | False | `rows:missing=S902..S904`, `rows:binding=…r55/r56/r57.json` |

`h07` is the direct closure of Critic22 D4 / Critic23 F4: one SID cannot
blanket-cover several cited copies, because H4 binds *each cited copy* to a
mined, used-by-exact 11-cell row whose source cell names that copy's `.ufo`
artifact (`tools/mori-entry-claims-check.py:221-238`). Bounds note: H4 is
satisfied if a single row's source cell names several artifacts (the predicate
is per-copy existence, not per-copy distinct rows), and the `tree` arm still
requires all six copies byte-equal regardless of citation
(`count-c2.py:275-291`), so a dead pinned copy still passes — unchanged from
r59 Critic22 D5, outside the four routed classes.

## Bounds

- Frozen-bytes rule respected: no instrument was modified; mutants are
  scratch-only copies; all counters were executed from the lane path with
  `--repo <fixture>` or `--repo .` (read-only `git show`/`ls-tree`).
- Fixture commits are throwaway under `$HYAKU_SCRATCH/mori-r60/Mo60Revenger95/`
  (root asserted with `git -C … rev-parse --show-toplevel` before any git
  write); the scratch tree (fixture, roots, mutant tools, run dirs) was removed
  after these receipts were transcribed into this report; no lane/fleet/sibling
  writes, no VCS mutation of the lane.
- The counter's `entry` arm is the only production path exercised by variants;
  scan/drift/trees arms were green in every variant run (`scan=ok drift=ok
  trees=ok tree=ok`), so class attribution is not carried by cross-arm noise.
- Verdicts are about *rejection on the frozen r60 predicate*; semantic
  support between claim text and quoted bytes is not measurable by any
  byte-bound instrument and is reported as residual, not as a defect against
  the frozen letter.
