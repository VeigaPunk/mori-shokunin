# Mo60MutationTester31 — mutation probe: `tools/mori-entry-claims-check.py` (C2 H1–H4)

Seat: Mo60MutationTester31 (leaf, read-only over the lane).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Freeze `ac496c7cde8cad965079858accae3bedfe4a73f2`; entering
`ddfb12fb0838b4307c445194a844f0c4b1950195`; lane tip observed during the seat
`b3c256138f00c704d5aa56eb0332d74506502ef2` (C1 data landing, as the contract warned).
Work performed in scratch only; no lane/VCS/fleet writes. Result: **5/5 mutants killed,
h00 control never flipped, 0 survivors.**

## Frozen bytes under test (pinned, verified)

| object | revision | sha256 |
|---|---|---|
| `tools/mori-entry-claims-check.py` | `ac496c7c` = tip = working tree | `cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69` (= `PIN_EC`) |
| same path at `ddfb12fb` | entering rev | absent (`git show` → empty; sha256 `e3b0c442…b855`) |
| `.ufo/waves/round-60/count-c2.py` | working tree | `8c4814f54c564a7f00beec5249de092a2d3b2c4043e07be773d80e8e3ccdf976` (= pinned count-c2 `8c4814f5…df976`) |

Tool docstring/selftest stand on themselves; the probe only touched the four
H1–H4 predicates named in the seat and no others.

## Method (scratch `/fast/scratch/hyaku/mori-r60/Mo60MutationTester31`)

Oracle = frozen tool blob via `git show ac496c7c:tools/mori-entry-claims-check.py`
(one copy under `oracle/ec.py`, never edited). Hostile trees = byte-exact
extraction of `git archive ac496c7c .ufo/waves/round-60/trees-c2h` into `trees/`;
all 117 extracted files verified against their git blob ids
(`git hash-object` vs `git ls-tree -r`), zero mismatches. `artifacts.json` is
count-c2's `ARTIFACTS` map verbatim; expects are
`.ufo/waves/round-60/trees-c2h-expects.json` verbatim.

Detector (`run.py`), the same criterion count-c2 applies in its tree arm
(`count-c2.py:398` verdict, `count-c2.py:402-403` reason membership), plus two
secondary arms:

- **D1** — each of the 13 trees evaluated with
  `--entry corpus/knowledge/wave-settlement-artifacts-r59.md --registry corpus/SOURCES.md
  --artifacts-json artifacts.json --min-claims 10 --min-files 3`; a tree is a
  violation when `out.ok != (expect == [])` or a frozen expected reason prefix is absent.
- **D2** — `--selftest`; violation unless exit 0 and `ENTRYCLAIMS_SELFTEST pass=13 fail=0`.
- **D3** — the real r59 entry on a freeze-rev-materialized root; violation unless
  `ok`, `claims>=10`, `files>=3`, `spans==claims`, no `rows*`/`pin*` reason.

Baseline (pristine oracle, sha `cffe9f33…e6e69`): **D1 clean, h00 `ok=true` with
`reasons=[]`, D2 `ENTRYCLAIMS_SELFTEST pass=13 fail=0`, D3 pass (`claims=13 files=6
spans=13 min_span=12`)** → 0 violations, detector not pre-failed. Detector
equivalence to the shipped counter confirmed independently:
`python3 .ufo/waves/round-60/count-c2.py ac496c7c --repo <lane> --scratch <scratch>/c2scratch`
→ `C2=met … trees=ok … rev=ac496c7c…`, exit 0.

Each mutant = oracle bytes with exactly one substitution (single occurrence asserted,
`diff -u` one hunk). Mutants were written as new files; the oracle was never rewritten
(see Restoration).

## Kill table

| # | mutant (sha256 of mutant bytes) | mutation site | predicate | mutant → target tree verdict | D1 | D2 | D3 | verdict |
|---|---|---|---|---|---|---|---|---|
| M1 | `m1_h1_grammar_off` `43fade7061cc…d2fa4d` | `mori-entry-claims-check.py:113-117` (grammar block deleted) | H1 | `h02-malformed-claim`: `ok=false, ["grammar:- **K77** …"]` → **`ok=true, []`, rc 0** | **verdict flip** | FAIL `grammar_blocks` (12/1) | pass | **KILLED** |
| M2 | `m2_min_span_1` `4e898a4ac3c6…f4edf` | `:49` `MIN_SPAN = 8` → `1` | H2 span ≥8 | `h05-short-quotes`: `["claims_min:4","files_min:1","span:short=K1..K4"]` → `["claims_min:4","files_min:1"]` (rc 1 both) | **reason loss** (expected `span:short` absent) | FAIL `short_span` (12/1) | pass | **KILLED** |
| M3 | `m3_span_collapse_off` `d76261566b50…adabc` | `:163-167` dup-span branch → `spans[key] = kid` | H2 distinct spans | `h03-line-offset-alias`: `ok=false, ["distinct:dup_span=K1=K10"], spans=9` → **`ok=true, []`, rc 0** | **verdict flip** | FAIL `alias_dup_span` (12/1) | pass | **KILLED** |
| M4 | `m4_min_text_1` `c83fec23cd6e…74bdae` | `:50` `MIN_TEXT = 10` → `1` | H3 text ≥10 | `h06-degenerate-text`: all 10 `text:short=K*` present → **all absent** (rc 1 both) | **reason loss** | FAIL `degenerate_text` (12/1) | pass | **KILLED** |
| M5 | `m5_h4_binder_off` `b8e7d88da18c…42663` | `:235-238` per-copy binder loop deleted | H4 per-copy row binding | `h07-single-row`: `["rows:missing=S902..S904", "rows:binding=…r55/r56/r57.json"]` → `["rows:missing=S902..S904"]` (rc 1 both) | **reason loss** (expected `rows:binding` absent) | FAIL `binding_missing` (12/1) | pass | **KILLED** |

Notes: D2 in every row is exit 1 with the single named check failing and
`ENTRYCLAIMS_SELFTEST pass=12 fail=1` — the tool's own selftest is per-predicate
sensitive for all five. D3 passing everywhere is correct: the real r59 entry is
genuinely clean, so a correct mutation should not make it fail.

### Additional affected trees (D1, full-suite run)

- M1: `h01-semantically-empty` loses its `grammar:- **K99** …` reason (not in h01's
  frozen expect list, so no D1 violation — see F3).
- M2: `h01` loses all `span:short=K*` (not expected for h01 — no violation).
- M3: `h01` loses all `distinct:dup_span=K*` (**expected** → D1 reason violation);
  `h06` loses its `distinct:dup_span` reasons (not in h06's expect list).
- M4: `h01` and `h06` each lose all `text:short=K*` (**both expected** → D1 reason
  violations on two trees).
- M5: only `h07`.

`h00-good-control` under every mutant: `ok=true, reasons=[]` — no mutant produced a
false positive, and no mutant "killed" the control (i.e. no kill is an artefact of an
over-strict detector).

## Findings (coverage, not contract claims)

- **F1 — the reason-membership arm is load-bearing.** Only M1 and M3 flip an `ok`
  flag; M2, M4 and M5 leave the entry verdict `false` because the trees that exercise
  their predicate are *also* failed by another predicate (`h05` by `claims_min`/
  `files_min`; `h01`/`h06` by `files_min`/`dup_span`/`span:` mismatch; `h07` by
  `rows:missing`). An ok-flag-only expect check — e.g. deleting `count-c2.py:402-403`
  — would survive 3 of 5 mutants. The frozen expect tables therefore rest on the
  reason-prefix half, and G3's tamper check (`count-c2.py:363-366`) is what keeps that
  half honest.
- **F2 — redundancy in the hostile trees, not in the tool.** `h05` cannot fail via
  `span:short` alone (it also trips `claims_min:4` and `files_min:1`), so the span
  minimum has no verdict-level witness; its witness is the expect-reason plus the
  selftest. Same shape for `h01`/`h06` (text) and `h07` (binding). A future round
  wanting verdict-level witnesses would need trees that are otherwise conforming.
- **F3 — expect tables are subset checks.** `h01` carries a malformed `**K99**` line,
  so pristine emits `grammar:- **K99** …` while its frozen expect is only
  `distinct:dup_span,text:short`, and the counter passes because it requires each
  expected prefix to be *present*, not that reasons be an exact set
  (`count-c2.py:402`). Consequence: a mutant that *adds* extra reasons to a hostile
  tree (e.g. an over-broad predicate) is invisible to D1. Not a defect against the
  frozen table; recorded as coverage.
- **F4 — G1 is orthogonal to this probe.** All five mutant blobs have sha ≠ `PIN_EC`,
  so count-c2's `run_pinned` (`count-c2.py:144-148`) refuses to execute any of them
  (`failed=tool_sha`). The kill table therefore measures the *predicate*, not the
  gate; the gate is structurally unable to be exercised by a mutated tool blob.
- **F5 — no false-suppression.** No mutant makes the 13-tree set pass where the
  frozen table demands failure (M1/M3 flip to `ok=true`, which D1 catches; M2/M4/M5
  lose expected reasons). No mutant silently weakens `h00`.

## Evidence — commands and literal outputs (scratch, cwd = scratch root)

```
$ sha256sum oracle/ec.py
cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69  oracle/ec.py
$ python3 run.py oracle/ec.py pristine
{"label":"pristine","sha":"cffe9f33…e6e69","killed":false,"violations":[]}
$ python3 run.py mut/m1_h1_grammar_off.py m1_h1_grammar_off
"killed": true, violations:
  h02-malformed-claim: verdict want_ok=False got=True
  selftest: rc=1 ['ENTRYCLAIMS_SELFTEST pass=12 fail=1']
$ python3 run.py mut/m2_min_span_1.py m2_min_span_1
"killed": true, violations:
  h05-short-quotes: missing_reason(expect=['span:short'] got=['claims_min:4','files_min:1'])
  selftest: rc=1 ['ENTRYCLAIMS_SELFTEST pass=12 fail=1']
$ python3 run.py mut/m3_span_collapse_off.py m3_span_collapse_off
"killed": true, violations:
  h01-semantically-empty: missing_reason(expect=['distinct:dup_span','text:short'] …)
  h03-line-offset-alias: verdict want_ok=False got=True
  selftest: rc=1 ['ENTRYCLAIMS_SELFTEST pass=12 fail=1']
$ python3 run.py mut/m4_min_text_1.py m4_min_text_1
"killed": true, violations:
  h01-semantically-empty: missing_reason(expect=['distinct:dup_span','text:short'] …)
  h06-degenerate-text: missing_reason(expect=['text:short'] got=['text:dup=…', …])
  selftest: rc=1 ['ENTRYCLAIMS_SELFTEST pass=12 fail=1']
$ python3 run.py mut/m5_h4_binder_off.py m5_h4_binder_off
"killed": true, violations:
  h07-single-row: missing_reason(expect=['rows:binding'] got=['rows:missing=S902','rows:missing=S903','rows:missing=S904'])
  selftest: rc=1 ['ENTRYCLAIMS_SELFTEST pass=12 fail=1']
```

Targeted single-tree reproduction, e.g. M2:

```
$ python3 mut/m2_min_span_1.py --root trees/h05-short-quotes \
    --entry corpus/knowledge/wave-settlement-artifacts-r59.md \
    --registry corpus/SOURCES.md --artifacts-json artifacts.json \
    --min-claims 10 --min-files 3
{"schema":"mori-entry-claims-v2","ok":false,
 "reasons":["claims_min:4","files_min:1"],
 "stats":{"claims":4,"files":1,"spans":4,"min_span":2}}       # rc 1
# pristine on the same tree:
{"ok":false,"reasons":["claims_min:4","files_min:1","span:short=K1",
 "span:short=K2","span:short=K3","span:short=K4"], …}          # rc 1
```

(Full per-tree JSON for all six runs is under `results/{pristine,m1_…,m5_…}.json` in
scratch.)

## Restoration evidence

Mutants were written as separate `mut/<name>.py` files; the oracle blob was opened
read-only and never rewritten. Before/after:

```
$ sha256sum oracle/ec.py                                  # before any mutant run
cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69
$ sha256sum oracle/ec.py                                  # after all 6 runs
cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69
$ sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-entry-claims-check.py
cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69
$ git -C <lane> diff --stat -- tools/ .ufo/waves/round-60/trees-c2h   # empty
$ git -C <lane> status --porcelain -- tools/ .ufo/waves/round-60/trees-c2h  # empty
```

No commit, no VCS mutation, no write outside my scratch and this report. Scratch is
removed after this file and the (nonexistent) receipts — nothing outside `/fast/scratch`
was ever written except this report.

## Limits

- Probe covers the four named predicates (H1, H2 span minimum and distinct-span
  collapse, H3 text minimum, H4 binder). H2's whitespace/byte-equality checks, H4's
  mined/used-by row checks, pins, frontmatter and H5's scan arm were not mutated
  (out of the seat's five-probe budget).
- Kill attribution is to the frozen expect table and the tool selftest; the shipped
  counter was run once at `ac496c7c` (met, `trees=ok`) to show detector equivalence,
  not per mutant (mutants cannot pass G1's sha gate by construction).
- Observation only; no remediation, no claim mutation. C2 stays "met at the freeze
  revision" as recorded by `evidence/c2-at-freeze.txt`.
