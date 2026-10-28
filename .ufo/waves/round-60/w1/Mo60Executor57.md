# Mo60Executor57 — hostile-tree battery at the freeze revision (r60 w1)

Seat `Mo60Executor57` (executor). Assignment: for each of the 13 committed hostile
trees, materialize it from the frozen revision in scratch and run the pinned
`tools/mori-entry-claims-check.py` with `--artifacts-json` from the counter's frozen
map; return per-tree `ok` plus the first three reasons. Read-only on the lane; no
commits, no lane VCS mutation, no fleet/sibling writes.

## Pins used

| Role | Value |
|---|---|
| Freeze revision (contract) | `ac496c7cde8cad965079858accae3bedfe4a73f2` |
| Entering revision (contract) | `ddfb12fb0838b4307c445194a844f0c4b1950195` (ancestor of the freeze: `git merge-base --is-ancestor` → 0) |
| Lane tip at start / later / at end | `b3c25613`, then `0f8340cf62b588fd64be8d9176ed7d5444c426b2` (tip moved mid-wave as the card warned) |
| `tools/mori-entry-claims-check.py` at freeze **and** tip | sha256 `cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69` (= `PIN_EC`), blob `19dc2960…` |
| `tools/mori-settlement-scan.py` at freeze and tip | sha256 `4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9` (= `PIN_SCAN`) |
| `.ufo/waves/round-60/count-c2.py` at freeze and tip | sha256 `8c4814f5…ccdf976`, blob `af6ac716…` |
| `trees-c2h/` tree object at freeze, at `b3c25613`, at `0f8340cf` | `fc3703949d493097cba8134da3aecd116c6a8e6a` (identical at all three) |
| `trees-c2h-expects.json` blob at all three | `e190b617cc69ae2dc83cc7d0a3b09ed44cd3c785` |

`git diff --quiet ac496c7c 0f8340cf -- .ufo/waves/round-60/trees-c2h
.ufo/waves/round-60/trees-c2h-expects.json .ufo/waves/round-60/count-c2.py
tools/mori-entry-claims-check.py tools/mori-settlement-scan.py
corpus/knowledge/wave-settlement-artifacts-r59.md` → rc 0, so every C2 byte I measured
at the freeze is still the byte at the tip. The tip movement during this wave touched
only `corpus/SOURCES.md`, `corpus/lessons/round-60.md` and evidence receipts.

Environment: Python `3.14.8`, git `2.56.0`, `LANG=en_US.UTF-8`. Disk guard before heavy
work: `/fast/scratch/hyaku use%=26 free=599G` (green; `/tmp` 14%, `/var/tmp` 38%).
No tool installed or updated.

Scratch: `$HYAKU_SCRATCH/mori-r60/Mo60Executor57` (`/fast/scratch/hyaku/mori-r60/Mo60Executor57`),
`TMPDIR` set there, sandbox clone under `<scratch>/mut/laneclone` (`git rev-parse
--show-toplevel` → that path, asserted before every git write). Removed before yielding
after copying the digests below.

## Method

1. Extracted the two frozen blobs read-only, never from the working tree:
   `git show ac496c7c:.ufo/waves/round-60/count-c2.py > $S/count-c2-freeze.py`
   (`8c4814f5…`), `git show ac496c7c:tools/mori-entry-claims-check.py > $S/ec-tool.py`
   (`cffe9f33…`), and asserted the tool sha against `PIN_EC` in the driver before any run.
2. Pulled the counter's frozen claims-copy → `.ufo`-artifact map straight out of the
   freeze blob and asserted equality with my `--artifacts-json`
   (`ARTIFACTS` == my file, 6 entries; `MIN_CLAIMS=10`, `MIN_FILES=3`).
3. For each of the 13 trees: `git ls-tree -r ac496c7c <tree>/` → `git show` each blob →
   write under `<scratch>/trees/<name>/`; run
   `python3 ec-tool.py --root <tree> --entry corpus/knowledge/wave-settlement-artifacts-r59.md
   --registry corpus/SOURCES.md --artifacts-json <scratch>/artifacts.json
   --min-claims 10 --min-files 3` (this is the counter's own tree invocation,
   `count-c2.py:382-390`), capture exit + JSON.
4. Cross-checks: 104 materialized files hashed to the exact git blob ids (`0 mismatches`,
   `0 extras`, all mode `100644`); the tool left each root byte-identical (before/after
   sha256 snapshot of every file, `root_mutated=False` ×13); a second and third
   independent run produced byte-identical stdout per tree; the counter itself was then
   run at the freeze from a fresh scratch.

## Per-tree result — 13/13 match the frozen expect table

`ok` = the tool's JSON `ok`; exit 0 iff ok. `files` = materialized files (entry +
registry + 6 copies; `expect.txt` is counter-side and not materialized).

| tree | files | exit | ok | reasons emitted | claims/files/spans | first three reasons |
|---|---|---|---|---|---|---|
| `h00-good-control` | 8 | 0 | **true** | 0 | 10/4/10 | — |
| `h01-semantically-empty` | 8 | 1 | false | 38 | 10/1/1 | `grammar:- **K99** — dangling claim with no pin o` · `text:short=K1` · `text:short=K2` |
| `h02-malformed-claim` | 8 | 1 | false | 1 | 10/4/10 | `grammar:- **K77** — malformed claim line missing` |
| `h03-line-offset-alias` | 8 | 1 | false | 1 | 10/3/9 | `distinct:dup_span=K1=K10` |
| `h04-blank-quote` | 8 | 1 | false | 1 | 10/4/9 | `span:blank=K1` |
| `h05-short-quotes` | 8 | 1 | false | 6 | 4/1/4 | `claims_min:4` · `files_min:1` · `span:short=K1` |
| `h06-degenerate-text` | 8 | 1 | false | 37 | 10/2/2 | `text:short=K1` · `text:short=K2` · `text:short=K3` |
| `h07-single-row` | 8 | 1 | false | 6 | 10/4/10 | `rows:missing=S902` · `rows:missing=S903` · `rows:missing=S904` |
| `h08-row-not-mined` | 8 | 1 | false | 4 | 10/4/10 | `rows:status=S901` · `rows:status=S902` · `rows:status=S903` |
| `h09-usedby-other` | 8 | 1 | false | 4 | 10/4/10 | `rows:usedby=S901` · `rows:usedby=S902` · `rows:usedby=S903` |
| `h10-stale-pin` | 8 | 1 | false | 3 | 10/4/10 | `pin:1` · `pin:2` · `pin:3` |
| `h11-wrong-line` | 8 | 1 | false | 1 | 10/4/10 | `span:1` |
| `h12-no-frontmatter` | 8 | 1 | false | 5 | 10/4/10 | `frontmatter:source` · `frontmatter:verified-at` · `frontmatter:recheck` |

Verdict check against `FROZEN_EXPECTS` (`count-c2.py:83-98`, byte-equal to the committed
`trees-c2h-expects.json` — compared programmatically): **13/13 `match=True`**, i.e.
`ok == (expect is empty)` for every tree *and* every frozen prefix occurs in the reason
list. `h00` is the no-false-negative control: `ok=true`, `reasons=[]`, `min_span=13`.
`h01`/`h06` carry the `distinct:dup_span` / `span:short` reasons past position 3 (h01
`distinct:dup_span` first at index 21, h07 `rows:binding` at index 4) — the reason
*set* is complete, only the ordering differs from the expect file's order.

Two structural notes on the tree arm, both already recorded by other seats and both
verified here: the matcher is a **prefix cover** (`count-c2.py:402-403`,
`all(any(r.startswith(e) …))`), so `pin:` and `span:` are each satisfied by a single reason;
and `h05`/`h01`/`h06` also emit `claims_min`/`files_min` which the frozen table does not
require (superset is accepted by design).

## Counter reproduction at the freeze

```
$ TMPDIR=$S/tmp python3 $S/count-c2-freeze.py ac496c7cde8cad965079858accae3bedfe4a73f2 \
    --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch $S/receipt
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok \
  claims=13 files=6 spans=13 rev=ac496c7cde8cad965079858accae3bedfe4a73f2      # exit 0
```

- `diff` against the committed `.ufo/waves/round-60/evidence/c2-at-freeze.txt` →
  **byte-equal** (that receipt is not present at `ac496c7c` itself; it landed in
  `76904b21`, and its content is my line verbatim, including `rev=ac496c7c…`).
- Do-nothing control reproduced: at `ddfb12fb…` the same counter prints
  `C2=unmet … failed=entry,pins,rows,selftest,tool_absent,trees,trees_set`, exit 1 —
  byte-equal to `evidence/control-c2-do-nothing.txt`.
- Tool selftest at the frozen bytes: `ENTRYCLAIMS_SELFTEST pass=13 fail=0`, exit 0;
  counter selftest: `C2_SELFTEST pass=8 fail=0`, exit 0.
- Real entry, independently materialized (not via the counter): `ok=True,
  reasons=[], stats={claims:13, files:6, spans:13, min_span:12}`.
- H5 drift arm verified directly with the pinned scan tool: r53 file →
  `SETTLEMENT_SCAN_FAIL` with `member[0]:extra_keys=report_file` (…, `member[2]` same);
  r54 bytes at an r53-named path → `SETTLEMENT_SCAN_OK` (exit 0). The reason is the
  member key-set class, not a filename heuristic.
- Runs against the sandbox clone at `ac496c7c` and against the lane produce byte-identical
  output; two consecutive runs sharing one `--scratch` also agree.

## Kill-rule / falsification probes (sandbox clone only, `<scratch>/mut/laneclone`)

Each mutant was committed **inside the clone** (`git rev-parse --show-toplevel` asserted)
and the frozen counter was run at that clone rev.

| mutant | change | counter verdict |
|---|---|---|
| A | extra 14th tree `h13-rogue/` with empty expect.txt | `unmet … failed=tree:h13-rogue:frozen,trees,trees_set` (exit 1) |
| B | `h02/expect.txt` rewritten to `grammar,text:short` | `unmet … failed=expect_tamper:h02-malformed-claim,trees` |
| C | `tools/mori-entry-claims-check.py` +1 line (G1) | `unmet … failed=…,tool_sha,tree:h00-good-control:tool,…` — and `ec-tool.py` was **never written** to the counter's scratch (`ls` → ENOENT): the unpinned blob does not run |
| D | `h08` registry deleted | `unmet … failed=tree:h08-row-not-mined:reasons,trees` |
| E | inert extra file + rewritten claim *text* in `h00` (same verdict) | `met` — the tree arm is verdict-based, not byte-pinned |
| G | whole tree `h12` removed | `unmet … failed=trees,trees_set` |
| H | `h02`'s malformed line repaired | `unmet … failed=tree:h02-malformed-claim:verdict,trees` |
| J | `h03` entry deleted | `unmet … failed=tree:h03-line-offset-alias:reasons,trees` |
| K | `h08` 3 of 4 rows repaired (`S904` still `queued`) | `met` — see F3 below |

A–D, G, H, J all fail closed with an attributable `tree:<name>:*` token. E is expected
(the counter re-derives verdicts, it does not byte-compare trees); K is a real gap.

## Findings (detection only; nothing remediated)

### F1 — MEDIUM — stale `--scratch` can report `met` for a revision that is not met
`count-c2.py:157` only creates the scratch dir; `:367` evaluates
`scratch/"trees"/<name>` and `:369-376` materializes only the paths `git ls-tree`
returns at R. A file deleted at R survives from an earlier run.

```
# fresh scratch at the freeze                                          -> C2=met
# mutant D (h08 registry deleted, rev 6cf675e2…), SAME pre-seeded scratch -> C2=met   <-- masked
# mutant D, fresh scratch                                              -> C2=unmet … failed=tree:h08-row-not-mined:reasons,trees
```

Same class on the entry arm: mutant F (entry file deleted, `29f2b5ab…`) → fresh scratch
`failed=entry,entry_absent,pins,rows,tree:h00:verdict,…`; pre-seeded scratch
`failed=entry,entry_absent,pins,rows` only — every `tree:*:verdict` masked. The frozen
receipts themselves are sound (fresh scratch, and my fresh re-derivation reproduces
them), but the fail-closed property is scratch-state dependent. Independently reported as
`Mo60Reviewer01.md` F1 (tree arm); this seat adds the entry-arm instance and the
converse demonstrability that `met` is reachable at a bad rev.

### F2 — MEDIUM — the pin gate does not isolate the child's environment
`count-c2.py:151` runs the pinned tool with `env={**os.environ, "TMPDIR": …}`, so an
ambient `PYTHONPATH` reaches the child even though its bytes are pin-verified.

```
# mutant H (h02 repaired) -> C2=unmet … failed=tree:h02-malformed-claim:verdict,trees
# same rev, PYTHONPATH=<scratch>/inject (a sitecustomize.py that rewrites the JSON
# json.dumps of any root ending in h02-malformed-claim to ok:false/grammar:…):
PYTHONPATH=$S/inject python3 $S/count-c2-freeze.py 8804f1ea… --repo $C --scratch …
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok …
```

`met` was produced at a revision where the hostile tree no longer fails, with no tree
bytes changed. Requires caller-environment control, so it is not a scoring lever inside
the frozen threat model (bytes at R only), but it means G1's "the pinned blob is what
executes" is only true modulo the interpreter environment. The same class was reported
for `count-c1.py` (`Mo60Sentinel41.md` F1, with `GIT_DIR`/alternates). Suggested shape:
sanitize the child env in `run_pinned` (`PYTHONPATH`, `PYTHONHOME`, `PYTHONSTARTUP`,
`GIT_*` redirectors) — no predicate change.

### F3 — MEDIUM — the tree arm's prefix cover accepts a weakened tree (kill-rule hole)
`count-c2.py:402-403` demands only that each frozen prefix occur *somewhere*:

```
# mutant K: h08's S901..S903 rows repaired to `mined`, S904 left `queued` (4→1 queued)
python3 ec-tool.py --root …/h08-row-not-mined …
{"ok": false, "reasons": ["rows:status=S904", "rows:binding=…/w1-results-r57.json"], …}
count-c2.py … -> C2=met selftest=ok … trees=ok …            # exit 0
```

An attacker who controls the tree at R can therefore keep one degenerate row per hostile
tree and still satisfy `rows:status`/`pin:`/`span:`/`grammar` — the "13 hostile trees"
arm is satisfiable by 13 nearly-clean trees. This is the reason-set analogue of the
`h00`-only weakening that the frozen expect table guards against by tree, but *within*
a tree nothing is guarded: the frozen predicate has no per-reason-count or
per-claim-coverage requirement. The substantive protections (H1–H5 in the tool) are
unaffected; this is about what the counter certifies. Not a met-flip at the freeze —
with the committed trees the reason sets are rich (h01 38 reasons, h06 37) — but the
kill rule as written does not exclude a weakened tree.

### F4 — LOW — H2's "≥8 distinct bytes" is implemented as span *length*, and overlap is not distinct-aliasing
`ec-tool.py:49` comment says "minimum distinct bytes per claim span"; `:168` compares
`end - start < MIN_SPAN`. A 10-byte line of one repeated byte passes:
`min_span=10, spans=12, ok=True, reasons=[]` on a 3-copy fixture whose quotes are
`"AAAAAAAAAA"`, `"BBBBBBBBBB"`, … And overlapping windows of one line are *different*
triples, so `spans == claims` is reachable from one line of evidence:

```
18 claims, offsets 1/3/5/7/9/11 of the same 62-byte line, 3 copies
-> ok=True stats={claims:18, files:3, spans:18, min_span:12} reasons=[]
```

Both are already on record (`Mo60Critic22.md` F3/F4) — this seat confirms them on the
frozen bytes with an independent fixture; no new class.

### F5 — LOW — H1 is a two-clause substring heuristic: bypass shapes and one false positive
`ec-tool.py:114`: `if "**K" in ln or (ln.lstrip().startswith("-") and "Quote:" in ln)`.
Measured on a 12-claim legal fixture, one extra line appended:

| appended line | verdict |
|---|---|
| `+ **K13** — … Quote: \`…\` (…:line:6; pin …)` | **ok=True** (unchecked) |
| `\| K13 \| … Quote: `…` \|` (table cell) | **ok=True** |
| `K13 — … Quote: \`…\` (…)` (bare label) | **ok=True** |
| `… Quote: \`…\` (…)` (prose, no dash, no `**K`) | **ok=True** |
| `* **K13** — …` / `1. **K13** — …` / `  - K13 — …` | `grammar:` → blocks |
| `Note: **K1** is the round-54 seats claim.` (benign prose) | `grammar:` → **false positive** |

So H1 still admits claim-shaped lines in the two positions a Markdown writer actually
uses (`+` bullets, table cells) plus bare-label/no-dash forms, and it rejects honest
prose that mentions a claim id in bold. Already reported as `Mo60Critic22.md` F1
(`*`/`+`/fullwidth-colon/lowercase/ZWSP probes) and `Mo60Reviewer04.md` F2 (the
false-positive). The `+`-bullet and table-cell shapes are the additions here.

### F6 — LOW — H4 still lets one registry row bind every copy
`ec-tool.py:237` binds via `any(art in b for b in binders)` over a flattened source-cell
string, and `:196-220` only looks up the *set* of S-ids mentioned in the head, not
one id per copy. With three `source: S901 — …` head lines and a single `S901` row whose
source cell lists all three artifact paths:

```
12 claims / 3 copies / 1 registry row   ->  ok=True, reasons=[]
```

i.e. "one fabricated row covers every copy" — the r59 defect H4 is worded against — is
still reachable. Confirmed independently of `Mo60Reviewer04.md`/`Mo60Critic21.md`, which
name the same shape; this seat's run is the executable witness (`rows:missing=S902,
S903` appear only when the head keeps distinct S-ids).

### F7 — INFO — lane observation, not a defect of these instruments
`/home/vgpnk/Projects/shokunin/mori-shokunin/EXEC-MARKER` existed untracked at 13:18
(90 B, content pointing at `/fast/scratch/hyaku/mori-r60/Mo60Executor58/se-old/real2/round-53/w1-results.json`,
i.e. another seat's PoC CWD write) and is gone now. It was never committed. Not written
by this seat; noted because an untracked marker in the lane root is exactly the G1 CWD
escape class `Mo60Sentinel41.md` F2 describes. No action taken (detection only).

## Summary

- **Claim under test is sustained at the freeze revision.** All 13 trees evaluate to the
  verdict their frozen expect table demands, `h00` clean, `h01`–`h12` blocked with the
  frozen reason families, tool and counter selftests green, real entry `ok` at
  `claims=13 files=6 spans=13`, and the frozen counter reproduces
  `C2=met … rev=ac496c7c…` byte-equal to the committed receipt and the committed
  do-nothing control.
- Materialization is faithful (104/104 blobs match git object ids) and the tool is
  read-only over its root (0 mutations ×13) and deterministic (3 runs, identical stdout).
- The counter's fail-closed behaviour has four residual gaps: scratch-state dependence
  (F1), child-env inheritance through the pin gate (F2), prefix-cover acceptance of
  weakened trees (F3), plus the tool-level H2/H4/H1 wordings F4–F6 that are already on
  other seats' record. None of them flips C2 at the freeze; all of them are things a
  successor revision should carry.

## Evidence retained (before scratch cleanup)

| file | sha256 |
|---|---|
| `count-c2-freeze.py` (freeze blob) | `8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976` |
| `ec-tool.py` (freeze blob) | `cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69` |
| `mine.txt` (counter receipt line) | `5890ace1c7d0713d5d1e0b952c1a80d985938053bfad80ec03a34f1348f90b80` |
| `trees-out-full.json` (13-tree detail) | `e72f859b802787a1c2a2aca9c9edf0128d8257e12b180b897547effbede0e1a6` |
| `receipt-compact.json` (per-tree ok+first3) | `b3ced349d7d4efe03036f676b4d3fd190bc2ca8ae55e3a08e4e4410d8da5b6e3` |
| `trees-out-pass2.json` (2nd pass, determinism) | `279a3fb6dae663d5bed2400130d4f7cad7f125000cefde3ac051c386a2245019` |
| `artifacts.json` (frozen claims-copy map) | `1d617c9cd7de1e21ab2ddc437f0730b4edbae99b316c2bbee5c741e0503841ac` |

All seven files remain in the seat scratch with the digests above verified after cleanup.

Scratch (`/fast/scratch/hyaku/mori-r60/Mo60Executor57`) was cleaned to 64 KB: the
sandbox clone, the 13 materialized trees, all mutant scratch roots and the probe fixtures
were removed; only the six receipt files above (`count-c2-freeze.py`, `ec-tool.py`,
`mine.txt`, `trees-out-full.json`, `trees-out-pass2.json`, `receipt-compact.json`) and the
`artifacts.json` map remain, with the digests unchanged after the trim. No installs, no
commits, no lane worktree writes from this seat.
