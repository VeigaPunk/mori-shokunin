# Mo52MutC1Arms — round 52 wave w1 mutation report (count-c1.py)

Seat: Mo52MutC1Arms (mutation tester, leaf). Assignment: >= 12 single-point mutations of
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/count-c1.py` in scratch copies, one per arm
(A axes / B shonen / C living / D locators), detector `--selftest`, killed iff nonzero. Scratch:
`/fast/scratch/hyaku/mori-r52/Mo52MutC1Arms/`. No subagents. No lane/fleet mutation (all git ops read-only;
counter runs used `--repo` only for `git show/cat-file/ls-tree/archive/status`).

## Baseline (pristine)

- `sha256sum count-c1-pristine.py` = `e864922790451b4026be784d5344d9a06827b251ed3c81bfe26b1c559ee3c300` — equals the
  frozen hash in `evidence/freeze-sha256.txt` line 2.
- `python3 count-c1-pristine.py --selftest` → 42× PASS, `C1_SELFTEST pass=42 fail=0`, exit 0.
- Real-data calibration at the landed tip on an isolated `--no-local` clone of the lane
  (`git clone --no-local /home/vgpnk/Projects/shokunin/mori-shokunin <scratch>/lane-clone`,
  `rev-parse --show-toplevel` = the clone; data commit `8524904adb…` present):
  `python3 count-c1-pristine.py 8524904adb25e44f24d9f25aac7eae909625c18c --repo <scratch>/lane-clone
  --fleet-repo /home/vgpnk/Projects/shokunin --scratch <scratch>/c1-clone-pristine`
  → `C1=met items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0
  lane_writes=0 manifest=6209bdb8e400 rev=8524904adb25e44f24d9f25aac7eae909625c18c`, exit 0. Identical to
  `evidence/c1-at-data.txt`.

Baseline is green → kills are meaningful (no inconclusive baseline).

## Mutant table

Each mutant = pristine bytes + one single-point change (unified diff vs pristine, 1–5 lines). Each mutates exactly
one behavior of one arm; the check column names the `--selftest` assertion designed to isolate that arm.

| id | arm | single-point change (line in pristine) | isolating check(s) | selftest rc | fail= | verdict |
|---|---|---|---|---|---|---|---|
| M1 | A | `check_axes`: `re.search(r"\b%s\b" % re.escape(verdict), …)` → `re.search(re.escape(verdict), …)` (L203) — verdict whole-word → substring | `verdict_substring_unmet` | 1 | 1 | **KILLED** |
| M2 | A | `axes_table`: `if len(heads) != 1:` → `if len(heads) > 2:` (L126) — accepts two `## Axes` headings | `second_axes_heading_unmet` | 1 | 1 | **KILLED** |
| M3 | A | `check_axes`: delete the Score-cell block (`st = scores.get(ax)` … L207‑211) — Score arm dropped | `score_cell_unread_unmet`, `newest_closure_score_wins_unmet` | 1 | 2 | **KILLED** |
| M4 | A | `manifest_targets`: `r.get("verdict") != "admitted"` → `not str(r.get("verdict") or "").startswith("admitted")` (L101) — `admitted` → startswith | `admitted_prefix_verdict_ignored` (does NOT fire, see survivor §) | 0 | 0 | **SURVIVED** |
| M5 | B | `check_pins`: `if path is None or not regular(path):` → `if path is None:` (L271) — symlink/regular check dropped | `symlinked_pin_path_unmet` | 1 | 1 | **KILLED** |
| M6 | B | `check_pins`: delete `elif not has_receipt:` branch (L284‑285) — receipt check dropped | `receipt_missing_unmet` | 1 | 1 | **KILLED** |
| M7 | C | `check_living`: delete the `pin_removed_or_rewritten` loop over entering pins (L331‑333) | `living_rewritten_in_place_unmet`, `living_pin_deleted_unmet` | 1 | 2 | **KILLED** |
| M8 | C | `superseded`: `cur is not None and cur != crit and …` → `cur is not None and …` (L314) — accepts the pin's own criterion number as superseding | none (see survivor §) | 0 | 0 | **SURVIVED** |
| M9 | C | `check_living`: skip condition `quoted(line_no, span) and any(l2 == line_no and not quoted(l2, s2) …)` → `quoted(line_no, span)` (L340) — quotation skip without the same-line replacement rule | `living_superseding_pin_wrong_unmet` | 1 | 1 | **KILLED** |
| M10 | C | `check_living`: `ok = rc == 0 and tally_ok(...)` → `ok = tally_ok(...)` (L363) — rc==0 dropped | `living_nonzero_rc_unmet` | 1 | 1 | **KILLED** |
| M11 | D | `check_locators`: `if q:` → `if q and False:` (L402) — quote check becomes range-only | `locator_quote_ws_folded_unmet_when_split`, `locator_quote_absent_unmet`, `locator_pair_absent_unmet` | 1 | 2 | **KILLED** |
| M12 | D | `evaluate`: `errs = … + (1 if writes else 0)` → without `+ (1 …)` (L432) and delete `if writes: failed.append("lane_writes")` (L437‑438) — lane_writes ignored | `lane_writes_error_unmet` | 1 | 1 | **KILLED** |

Detector command per mutant: `python3 count-c1-mutNN.py --selftest`; exit code = verdict (killed iff nonzero).
Hashes before run == after run (restoration, see below).

## Survivors — arm text

### M4 (arm A: `admitted` → startswith) — SURVIVED

`--selftest` still exits 0 (`C1_SELFTEST pass=42 fail=0`). The isolating check `admitted_prefix_verdict_ignored`
only asserts `manifest_targets(manifest)["coverage"] == (47, "improved")`; the selftest manifest's only
`admitted-pending` round (46) grades coverage, whose best admitted round is 47, so accepting round 46 changes no
target and the check cannot distinguish.

Direct probe (same manifest as selftest): pristine `manifest_targets` == mut04 `manifest_targets` (identical dict).

Semantic gap probe — a manifest where a pending round is the newest improved for an axis:

```
rounds: 40 admitted (all axes improved); 45 admitted-pending (freshness improved); 48 admitted (freshness unchanged)
pristine targets: freshness=(40, improved)   mut04 targets: freshness=(45, improved)
```

So a `admitted-pending` round can become the expected `round N` target. P-C1 / contract arm (A) demands verdict
exactly `admitted`; the mutated counter would (a) demand the SCORECARD Last change cell quote a round the fleet
never admitted (false unmet on correct data), and (b) treat a row naming a pending round as satisfying the
verdict-word check for an expectation built from a pending round (false met on data that violates P-C1).

Real data at `8524904adb…` (clean clone): output byte-identical to pristine — `C1=met items=42 … mismatches=0
errors=0 hidden=0 lane_writes=0`, exit 0. The fleet MANIFEST at the pinned fleet revision has no admitted-pending
round that outranks an admitted round for any axis, so the weakened arm is not exercised by the current claim. It
is a latent contract hole, not a current claim failure.

### M8 (arm C: superseded() accepts the pin's own criterion) — SURVIVED

`--selftest` exits 0. No check covers a later criterion carrying the *same* number as the pin. The only
supersede checks use distinct criterion numbers (12→13).

Probe: QUALITY.md with the original pin under criterion 12 and a later line also numbered 12 reading
`12. … supersedes 12's check. …`:

```
superseded("corpus/QUALITY.md", text, 5, 12, "`python3 tools/c.py --selftest` → `pass=12 fail=0`")
pristine → False     mut08 → True
```

Effect: a duplicate-number later row can retire a live pin (the pin stops being run, counted `superseded`/ok)
without a valid successor criterion, per the contract's criterion-supersession rule. Feasibility on real content is
low (criterion numbers are normally unique), but nothing in the detector catches the weakening.

Real data at `8524904adb…` (clean clone): output byte-identical to pristine, `C1=met`, exit 0.

## Side observation — lane_writes against the live lane

First calibration attempts ran `--repo /home/vgpnk/Projects/shokunin/mori-shokunin` (live working tree) in
parallel with other wave seats writing their reports into the lane:

```
pristine: C1=unmet … errors=1 … lane_writes=13 failed=errors,lane_writes   (exit 1)
mut04:    C1=unmet … errors=1 … lane_writes=22 failed=errors,lane_writes   (exit 1)
mut08:    C1=unmet … errors=1 … lane_writes=13 failed=errors,lane_writes   (exit 1)
```

Items were all ok (`mismatches=0`) in those runs; the failures came solely from the `lane_writes` arm seeing
concurrent sibling writers' new untracked files in the live lane during the run. On an isolated clone the same
commands read `lane_writes=0`. This is an operational caveat of running the counter against the live repo while a
wave is writing (the frozen controls, receipts and evidence all used clones/quiescent state), not a counter-logic
defect. The mutated counters and pristine behave identically under both conditions.

## Restoration evidence

- Detector ran on pristine, each mutated, and restored bytes: after all runs, `sha256sum` of all 13 scratch files
  equals their before-run hashes (mutants differ from pristine only by the documented single-point change; pristine
  = `e864922790451b4026be784d5344d9a06827b251ed3c81bfe26b1c559ee3c300`).
- Lane counter file unchanged: `sha256sum …/round-52/count-c1.py` = `e864922790451b4026be784d5344d9a06827b251ed3c81bfe26b1c559ee3c300` (frozen bytes intact).
- No files created inside `/home/vgpnk/Projects/shokunin/mori-shokunin` by the counter runs (git status showed only sibling-seat report writes; the counter writes only under its `--scratch`). Scratch removed at end of seat.

## Findings

- [MED] `count-c1.py` `manifest_targets` (L101): mutating the exact-verdict comparison to `startswith` is
  undetected by `--selftest` (M4 survives; `admitted_prefix_verdict_ignored` cannot observe it). Arm (A)'s
  "verdict exactly `admitted`" guarantee is not pinned by a check that fails when a pending round changes a
  target. Suggest round-53 check: manifest with an `admitted-pending` round as the newest improved for an axis,
  asserting the target stays the admitted round.
- [MED] `count-c1.py` `superseded` (L314): dropping the `cur != crit` guard is undetected (M8 survives). A later
  criterion carrying the pin's own number can retire a live pin. Suggest round-53 check: same-number later
  criterion carrying `supersedes N's check` must NOT supersede.
- [LOW] Running the counter with `--repo` on the live lane while wave seats write gives false `lane_writes>0`
  (13–22) → `failed=errors,lane_writes` even with all items ok. Evidence receipts and controls avoid this by using
  clones. Not a logic defect; the `lane_writes` arm measures working-tree churn, which concurrent sibling writers
  create. Worth a named-limit note for round 53.
- Killed 10/12: the selftest isolates M1, M2, M3, M5, M6, M7, M9, M10, M11, M12 (each arm's listed check
  fired and exit 1). These named arm-isolating controls: verdict word-boundary (A), single-Axes-heading (A),
  Score cell (A), regular-file pin path (B), receipt presence (B), pin_removed byte-for-byte presence (C),
  same-line quotation-replacement rule (C), rc==0 (C), locator quote/pair content (D), lane_writes (D).
