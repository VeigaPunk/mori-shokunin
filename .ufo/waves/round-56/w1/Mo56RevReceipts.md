# mori round 56 w1 — Mo56RevReceipts — receipt-integrity review of `.ufo/waves/round-56/evidence`

Seat: Mo56RevReceipts (reviewer, leaf — no subagents dispatched). Date: 2026-10-27.
Freeze tip under review: 8be2717b0809281d07dffe83dad424a4859e0747 (HEAD at review start: acc62f54fb0f53b47b428594dc27365150cbd76b; `git diff --stat 8be2717b -- .ufo/waves/round-56/evidence .ufo/waves/round-56/count-c1.py .ufo/waves/round-56/count-c2.py tools/mori-driver-liveness.py tools/mori-vote-bind.py` is empty, and `git status --porcelain` on the evidence dir is clean, so receipt bytes at the tip equal the working-tree bytes I read).

## Method

- Read all 11 files in `.ufo/waves/round-56/evidence` (exactly 11 exist).
- For each command receipt: re-ran the command the receipt's bytes were produced by (reconstructed from the counter/tool CLIs and lane convention), stripped the trailing `exit=N` line from the receipt, and `cmp`-ed the receipt remainder against fresh stdout; compared the receipt's recorded exit against the observed exit code separately. "Reproduces" below means byte-exact stdout match plus matching exit code.
- Verified every pin in freeze-sha256.txt by recomputing sha256 over `git show <rev>:<path>` at candidate revisions (data 6ced9da9, freeze commit 3f494b49, freeze tip 8be2717b, working tree).
- All runs read-only over the lane repo (`git show`/`rev-parse` only); counters materialized tools under `$TMPDIR`. Scratch: /fast/scratch/hyaku/mori-r56/Mo56RevReceipts (created, `TMPDIR` exported, removed at the end). No clone or archive needed. disk-guard status before runs: /fast/scratch/hyaku 28% used, 582.7G free. No tools installed; no pacman transactions; nothing written outside my report and scratch.

## Summary verdict table

| receipt | literal captured bytes | exit status carried | revision stamped | reproduces |
|---|---|---|---|---|
| c1-at-freeze.txt | yes | yes (`exit=0`) | yes (`rev=3f494b49cde612d929e82887a48e1660c022c359`) | yes (byte-exact, rc 0) |
| c2-at-freeze.txt | yes | yes (`exit=0`) | yes (`rev=3f494b49…`) | yes (byte-exact, rc 0) |
| controls.txt | yes | **no** (no exit line) | partial (do-nothing lines stamp truncated prefixes of 5b295eee…; 6 mutant lines stamp none) | yes (byte-exact, runner rc 0) |
| selftest-c1-counter.txt | yes | yes (`exit=0`) | n/a (selftest measures no revision) | yes (byte-exact, rc 0) |
| selftest-c2-counter.txt | yes | yes (`exit=0`) | n/a | yes (byte-exact, rc 0) |
| c2-old-counter-voted0.txt | yes | yes (`exit=1`) | yes (`rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa`) | yes (byte-exact, rc 1) |
| tally-r55.txt | yes | yes (`exit=0`) | **no** (mitigated, see F3) | yes (byte-exact, rc 0) |
| selftest-vote-bind.txt | yes | yes (`exit=0`) | n/a | yes (byte-exact, rc 0) |
| census-start.txt | yes | yes (`exit=0`) | **no** (see F2) | yes (byte-exact at current tree, rc 0) |
| driver-liveness-live.txt | yes | yes (`exit=0` trailer + embedded `"rc": 0`) | n/a (live host state; no revision exists) | no — live capture, drifts by design (see F6) |
| freeze-sha256.txt | n/a (pin list, not command output) | n/a | partial (tools block annotated @6ced9da9; top block unstamped — see F5) | yes (all 8 pins recompute) |

10 of 11 files are receipt-shaped; freeze-sha256.txt is a pin manifest. No retyped-summary defect (the routed round-55 class) found anywhere: every command receipt is literal captured stdout.

## Re-run evidence

Counter receipts (rev as stamped):

```
$ python3 .ufo/waves/round-56/count-c1.py 3f494b49cde612d929e82887a48e1660c022c359
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=3f494b49cde612d929e82887a48e1660c022c359   rc=0  == c1-at-freeze.txt (minus exit=0) byte-exact
$ python3 .ufo/waves/round-56/count-c2.py 3f494b49cde612d929e82887a48e1660c022c359
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=3f494b49cde612d929e82887a48e1660c022c359   rc=0  == c2-at-freeze.txt byte-exact
```

Freeze-tip label check — both counters also met at the actual freeze tip, identical verdict text modulo the rev stamp:

```
$ python3 .ufo/waves/round-56/count-c1.py 8be2717b0809281d07dffe83dad424a4859e0747
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747   rc=0
$ python3 .ufo/waves/round-56/count-c2.py 8be2717b0809281d07dffe83dad424a4859e0747
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747   rc=0
```

Selftests:

```
$ python3 .ufo/waves/round-56/count-c1.py --selftest   -> C1_COUNTER_SELFTEST pass=1 fail=0   rc=0  == receipt
$ python3 .ufo/waves/round-56/count-c2.py --selftest   -> C2_COUNTER_SELFTEST pass=1 fail=0   rc=0  == receipt
$ python3 tools/mori-vote-bind.py --selftest           -> VOTE_BIND_SELFTEST pass=16 fail=0   rc=0  == receipt
$ python3 tools/mori-driver-liveness.py --selftest     -> DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0   rc=0  (no direct receipt; covered inside c1-at-freeze)
```

Tally receipt (round-55 artifacts materialized from 8be2717b via `git show`; 16 `--voter Mo55RcNN` args):

```
$ python3 tools/mori-vote-bind.py tally --ledger <ledger.md> --results <results.json> --verb RECHECK --voter Mo55Rc01 .. Mo55Rc16
TALLY rows=78 agree=78 double=68 single=10 zero=0 dissent=0 voters=16 bound_voters=15   rc=0  == tally-r55.txt byte-exact
```

Tally input-byte stability (so the missing rev stamp cannot change the result): sha256 of `corpus/knowledge/kernel-v7.3-recheck-r55.md` = `462e67c148d66ce1…` and of `.ufo/waves/round-55/w1-results.json` = `2e5b0a0f94d1fa5b…` identical at 6ced9da9, 3f494b49, 8be2717b, and the working tree.

Old-counter contrast receipt:

```
$ python3 .ufo/waves/round-55/count-c1.py 5b295eeebd87ebd610d8d39bfe2035742f740cfa --repo /home/vgpnk/Projects/shokunin/mori-shokunin
C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=5b295eeebd87ebd610d8d39bfe2035742f740cfa failed=votes   rc=1  == c2-old-counter-voted0.txt byte-exact
```

Census receipt (`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`): rc 0, stdout byte-exact against census-start.txt — 23 W04 duplicate-url lines + `mori ok …/corpus/SOURCES.md`, unchanged by the S544/S545 appends.

Controls receipt (`python3 .ufo/waves/round-56/controls/controls.py 5b295eee…`): rc 0, all 8 lines byte-exact against controls.txt (2 PASS do-nothing + 6 KILLED mutants, no SURVIVOR/FAIL). Note the runner reads the counter/tool bytes from HEAD and runs the do-nothing counters AT the entering tip; tool and counter bytes are identical from 8be2717b to acc62f54 (pin checks pass at both), so the reproduction is stable.

Live driver-liveness receipt: re-ran `python3 tools/mori-driver-liveness.py` — rc 0, same schema `mori-driver-liveness-v1`, same verdict `DRIVER_LIVENESS_OK`, same 23-lane set, `malformed=0`, same watchdog.log path. Expected live drift between capture and re-run: kake completes 50→51, kumitate launches 57→58 and rounds_seen 49→50, log lines 1728→1730. A live receipt is a point-in-time capture; not byte-reproducible by design.

## Pin verification (freeze-sha256.txt)

All 8 pins recompute exactly:

- contract.md = 088761f3…, count-c1.py = c4e58eed…, count-c2.py = 4b350c77… at `.ufo/waves/round-56/` — identical at 3f494b49, 8be2717b, and working tree.
- controls/controls.py pin 5bf65ac0… matches only 8be2717b onward: the file was corrected in 8be2717b (fence mutant pattern `r"        if fence:\n            continue\n"` → plain string, so the regex replacement actually applies to a newline, not a literal backslash-n) and the pin was re-landed in the same commit. The committed controls.txt reproduces byte-exactly under the corrected, pinned runner.
- tools/mori-driver-liveness.py@6ced9da9 = 6b3dba74… and tools/mori-vote-bind.py@6ced9da9 = 8be1acdb… verified from `git show 6ced9da9:<path>`; they also equal the `PIN` constants inside count-c1.py / count-c2.py (both counters' pin arms pass).
- corpus/evidence/sources-r56/rfc8259.txt = 61a5378f… and watchdog-log-grammar.txt = 38ba3e6b… verified at 6ced9da9, 3f494b49, 8be2717b, and working tree.

Contract cross-check "start census … (exit 0, 316 rows, 23 W04)": the 23 W04 lines and `exit=0` are in the captured bytes; the 316-row figure is not. Verified true archaeologically: registry row count at 5b295eee (the entering tip, parent of data commit c419fe6d) is exactly 316; 318 from c419fe6d onward (S544 + S545). The receipt was captured against the 316-row state and still byte-reproduces at the 318-row tree because the two added rows contribute no W04.

## Findings

- F1 — MED — `.ufo/waves/round-56/evidence/controls.txt` (whole file): carries no exit status. Every other command receipt in this evidence set ends with an `exit=N` line; controls.txt ends on the last KILLED line. controls.py exits 1 on any FAIL/SURVIVOR/ERROR/SETUP, so without the recorded status the receipt bytes alone cannot distinguish a clean 8/8 run from a truncated capture. Reproduction confirms the missing value was 0 (runner rc 0, byte-exact lines). Named limit for the L1: append `exit=0` on the next re-land; no counter change implied.
- F2 — LOW — `.ufo/waves/round-56/evidence/census-start.txt`: no revision stamp, and the receipt bytes carry no row count, so the contract's "316 rows" half is prose-only (the routed-defect-1 letter is met — captured bytes are present — but the row-count claim rests on archaeology, which I verified: 316 rows at 5b295eee, 318 from c419fe6d). Future census receipts should embed the census-mode row line or a rev stamp; frozen contract text itself is accurate.
- F3 — LOW — `.ufo/waves/round-56/evidence/tally-r55.txt`: no revision stamp. Mitigated and safe: ledger/results bytes are identical across 6ced9da9→worktree (hashes above), and the same tally is rev-stamped inside c2-at-freeze.txt (`rev=3f494b49…`). A standalone tally receipt should still stamp its measured rev per the round's own routed-defect-2 rule.
- F4 — LOW — `.ufo/waves/round-56/evidence/controls.txt` lines 1–2: do-nothing rev stamps are truncated mid-hash (`rev=5b295eeebd87ebd610d8d39b` = 28 hex chars; `…fe2035742` = 34) by the runner's `verdict[:110]` slice; the six mutant lines stamp no rev at all (they mutate the tool from HEAD-at-capture, unstamped). Prefixes are unambiguous and reproduction is verified; cosmetic, but the mutant lines' measured revision exists and is not named.
- F5 — LOW — `.ufo/waves/round-56/evidence/freeze-sha256.txt`: the top pin block (contract.md, both counters, controls/controls.py) names no revision; the file header names only the data commit, which is wrong for that block (contract+counters landed at 3f494b49; the controls.py pin matches only 8be2717b, post-correction). All pins are in fact correct; annotate each block with its landing rev to remove the ambiguity.
- F6 — LOW — `.ufo/waves/round-56/evidence/driver-liveness-live.txt`: live receipt with no explicit capture wall-clock timestamp and no recorded command line (capture time ≈ epoch 1793107962 is only derivable from the embedded age fields). `rc: 0` is embedded and the `exit=0` trailer is present; drift on re-run is expected and observed (counts above). A timestamp field in the schema would make the capture self-dating.
- F7 — INFO — c1-at-freeze.txt / c2-at-freeze.txt stamp `rev=3f494b49…` (freeze commit) while the wave's freeze tip is 8be2717b. Verified not a substantive gap: both counters run `met` at 8be2717b with identical verdict text modulo the stamp, and the stamp is the honest measured revision. No action needed.

Residual risk: provenance above byte-reproduction (which shell captured a receipt) is unverifiable from receipt bytes alone; the rev stamps and pins are the only anchors, which is exactly why F1–F5 matter. No vote-shaped lines, no counter/predicate changes proposed; F1–F6 are receipt-format limits for round 57 routing, not claim defects — both frozen claims' evidence sets reproduce in full.

Scratch /fast/scratch/hyaku/mori-r56/Mo56RevReceipts removed after this report was written.
