# Mo97MutC2 — mutation test of the frozen C2 counter (round 97, wave w1)

Seat: mutation-tester. Target: `.ufo/waves/round-97/count-c2.py` (frozen). Method: 10 single-change
mutants, each exercised on the rebuilt controls-r97.sh fixtures plus 3 constructed killer fixtures.
Lane bytes never edited — all mutants are copies in scratch `$HYAKU_SCRATCH/mori-r97/Mo97MutC2`
(removed after evidence extraction; the generator, battery driver, outputs and this report's cited
lines lived there). No tool installs were needed (stock python3/curl/git only).

## Instrument and mutant hashes (before/after)

- pristine (lane copy): sha256 `957a7be605ba920734a218388b7ebb50f4f829979931c6e4193caee2149a1e91`
  — equals the freeze value recorded in `contract.md` / first line of `evidence/controls-r97.txt`.
  Re-checked after the battery: unchanged (`957a7be6…a1e91`) — restoration evidence.
- Mutants (sha256 of full mutant file, each a verified single string replacement, applied exactly once):
  - M1_hole_guard `f0b2f371c4e4097d…7adddfb`: `hole = "pass" if good and hole != "fail" else "fail"` → `hole = "pass"` (hole guard comparison dropped)
  - M2_ignore_unpinned `6f2de78b42747974…36c209f1`: `if unpinned != 0:` → `if unpinned < 0:`
  - M3_ignore_mismatch `1174fa39ab928e13…1fc9a569f`: `if mismatch != 0:` → `if mismatch < 0:`
  - M4_liveok_contentdrift `6c762515eddb0fea…868b4ed46`: `LIVE_OK = {"fresh", "time-churn"}` → `LIVE_OK = {"fresh", "time-churn", "content-drift"}`
  - M5_newest_lowest `6218ae348ea354e4…118feeb58225`: `if best is None or n > best[0]:` → `n < best[0]` (newest_copy picks lowest round N)
  - M6_accept_absent `2d4d254274102959…6f96d064a46b`: `if good:` → `if good or st is None:` (absent target row accepted)
  - M7_skip_live_rc `6df9f08bf47f6aff…2bc4ac5ad1e`: `if lr.returncode != 0 or any(...)` → `if any(...)` (live rc check skipped)
  - M8_nolive_met `81f609bd5626a7bb…5bd0233cb`: `failed.append("live_skipped")` → `pass` (`--no-live` counts as met)
  - M9_missing_class_ok `4e3a34d77de10a1a…b03ee32a8`: `any(classes.get(s) not in LIVE_OK …)` → `any(classes.get(s, "fresh") not in LIVE_OK …)`
  - M10_drop_S623 `349ffd53d30bfc4c…71f4a3`: `TARGETS = ("S615", "S616", "S623")` → `TARGETS = ("S615", "S616")`

## Fixtures

Rebuilt exactly per `controls-r97.sh`: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive
973b2af11f41bd362163d7e29ac08286832f546b | tar -x -C <fix>`; candidate pins copied from
`.ufo/waves/round-97/candidate/{S615,S616,S623}.html` into `corpus/evidence/sources-r97/`;
F3's S616 replaced by today's live `curl https://docs.python.org/3/library/tokenize.html` (network
was up, HTTP 200); F4 sed swaps S623's URL cmdline.html→configure.html; F2/F7 add a 362,493-byte
/dev/urandom S615 copy. Three constructed killer fixtures:
- F6_norow: pins + delete the `| S623 |` table row from SOURCES.md.
- F7_twocopies: pins + junk S615 copy at `corpus/evidence/sources-r90/S615.html` (two copies, different rounds).
- F8_noadj: pins + delete `tools/mori-drift-adjudicate.py` (drift-recheck setup-failure path, rc=2).

Comparison rule (tasking: "killed = any verdict line differs from pristine"): every counter stdout
line is a verdict line (TARGET/LIVE/C2), compared together with exit rc. LIVE lines embed wall-clock
fields (`run-start=`, `as-of=`, `window=`) that differ between any two runs, so exactly those three
fields are stripped; nothing else is normalized. Calibration: pristine run twice on F1 and F5 →
IDENTICAL after normalization (no clock false-kills). No run printed `C2_SETUP`; no baseline was
inconclusive.

## Pristine baselines (all match the contract's expected verdicts)

```
F1_donothing    rc=1 C2=unmet mismatch=0 unpinned=3 targets_ok=0/3 hole_guard=n/a live=S615:no-copy,S616:no-copy,S623:no-copy checks_failed=unpinned,target_S615,target_S616,target_S623,live
F2_hole         rc=1 C2=unmet mismatch=0 unpinned=0 targets_ok=2/3 hole_guard=fail live=skipped checks_failed=target_S615,live_skipped
F3_livebytes    rc=1 C2=unmet mismatch=1 unpinned=0 targets_ok=2/3 hole_guard=pass live=skipped checks_failed=mismatch,target_S616,live_skipped
F4_contentdrift rc=1 C2=unmet mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass live=S615:time-churn,S616:time-churn,S623:content-drift checks_failed=live
F5_positive     rc=0 C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass live=S615:time-churn,S616:time-churn,S623:time-churn checks_failed=-
```
F1 equals the contract Before line; F5 equals the contract Target line (every live class time-churn ∈ {fresh, time-churn}).

## Kill matrix (controls fixtures F1–F5)

```
M1_hole_guard            F1:survived  F2:KILLED  F3:survived  F4:survived  F5:survived
M2_ignore_unpinned       F1:KILLED  F2:survived  F3:survived  F4:survived  F5:survived
M3_ignore_mismatch       F1:survived  F2:survived  F3:KILLED  F4:survived  F5:survived
M4_liveok_contentdrift   F1:survived  F2:survived  F3:survived  F4:KILLED  F5:survived
M5_newest_lowest         F1:survived  F2:survived  F3:survived  F4:survived  F5:survived
M6_accept_absent         F1:survived  F2:survived  F3:survived  F4:survived  F5:survived
M7_skip_live_rc          F1:survived  F2:survived  F3:survived  F4:survived  F5:survived
M8_nolive_met            F1:survived  F2:KILLED  F3:KILLED  F4:survived  F5:survived
M9_missing_class_ok      F1:survived  F2:survived  F3:survived  F4:survived  F5:survived
M10_drop_S623            F1:KILLED  F2:KILLED  F3:KILLED  F4:KILLED  F5:KILLED
```

Decisive differing lines (pristine | mutant):
- M1, F2: `hole_guard=fail` | `hole_guard=pass` (C2 line).
- M2, F1: `checks_failed=unpinned,target_S615,target_S616,target_S623,live` | `checks_failed=target_S615,target_S616,target_S623,live`.
- M3, F3: `checks_failed=mismatch,target_S616,live_skipped` | `checks_failed=target_S616,live_skipped`.
- M4, F4: `C2=unmet … checks_failed=live` rc=1 | `C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass live=S615:time-churn,S616:time-churn,S623:content-drift checks_failed=-` rc=0. Content-drift accepted as healthy.
- M8, F2/F3: `checks_failed=target_S615,live_skipped` | `checks_failed=target_S615`; `checks_failed=mismatch,target_S616,live_skipped` | `checks_failed=mismatch,target_S616` (`--no-live` would score met whenever the offline legs pass).
- M10, F1: pristine prints `TARGET S623 unpinned …` + live has S623:no-copy; mutant's TARGET/live lines lack S623. F4: rc 1→0 — with S623 unchecked, its content-drift becomes invisible (`C2=met … checks_failed=-`). F2/F3: `targets_ok=2/3` | `targets_ok=1/3`. F5: TARGET/live lines lose S623.

## Survivors on the controls and their killer fixtures

- M5 (newest_copy lowest N): survived F1–F5 — every control tree holds at most one copy per target,
  so `>` vs `<` is unobservable. KILLED by F7_twocopies:
  `TARGET S615 unpinned copy=corpus/evidence/sources-r97/S615.html copy_sha=7891c58897fe9f78…`
  | `TARGET S615 unpinned copy=corpus/evidence/sources-r90/S615.html copy_sha=a0017dfa15a87124…`
  (mutant reads the junk r90 copy; pristine reads the r97 pin the digest tool's actual= names).
- M6 (accept absent): survived F1–F5 — no control removes a row. KILLED by F6_norow:
  `… targets_ok=2/3 hole_guard=pass … checks_failed=target_S623,live` |
  `… targets_ok=3/3 hole_guard=pass … checks_failed=live` (absent S623 counted toward 3/3).
- M9 (missing class defaults ok): survived F1–F5 — the controls never produce a classless target
  while drift-recheck exits 0 (F8's classless case has rc=2, which M9's intact rc check catches, and
  the `live=` display field keeps its own `classes.get(s, "missing")` default). KILLED by F6_norow:
  pristine/mutant TARGET lines equal, but
  `checks_failed=target_S623,live` | `checks_failed=target_S623` — the live leg silently passes a
  target drift-recheck never printed (drift-recheck exits 0; `--only` ids absent from the registry
  are skipped without complaint).

## True survivor — coverage finding, not a counter defect

M7 (skip live rc check) survived every fixture including both constructed rc≠0 cases:
- F8_noadj (drift-recheck rc=2, empty stdout): pristine and M7 byte-identical after normalization —
  the missing classes already fail the class check.
- F6_norow (rc=0): identical trivially (dropped check is a no-op).
Argument from the frozen instrument bytes (`tools/mori-drift-recheck.py`, rev 973b2af): `run()` returns
`1 if unresolved else 0`; `unresolved` increments only in the `token is None` branch, which emits
`"<sid> unresolved as-of=…"` — the counter parses that row's class as `unresolved` ∉ LIVE_OK. All
setup failures (`MORI_DRIFT_RECHECK_SETUP`, rc=2) are written to stderr before any stdout, leaving
every target's class missing ∉ LIVE_OK. So over this revision's tools, rc≠0 ⇒ the class check already
fails ⇒ the rc check is redundant defense-in-depth and cannot be killed by any fixture built from the
frozen instruments. It would matter only against a future drift-recheck that exits nonzero while
printing only fresh/time-churn rows. The frozen counter is correct as-is; no contract change follows.

## Findings summary

1. The counter's discriminating power is real: 9/10 single-change mutants killed (M1, M2, M3, M4,
   M8, M10 by the rebuilt controls alone; M5, M6, M9 additionally by constructed fixtures F7/F6/F6).
2. The controls' coverage gaps are exactly the three constructs above: multi-round copy sets (M5),
   deleted registry rows (M6), and classless-but-rc-0 live legs (M9). Each is cheap to add as a
   control if the lane wants the counter's neighbours covered by pre-freeze fixtures too.
3. M4's kill confirms the live-leg whitelist is the only thing standing between C2=met and
   content-drift: drift-recheck itself exits 0 on content-drift (adjudicator semantics), so any
   future widening of LIVE_OK beyond {fresh, time-churn} flips the r96 content-drift control green.
4. No mutant made a `C2_SETUP` (rc=2) path score met; the setup guard held in all 62 runs.

## Unrun checks (named, not run)

- Mutants were exercised against the entering-revision instruments (per the controls recipe). I did
  not rerun the battery against a landing-revision (`e85ed912…`) tree, where `--root` supplies that
  tree's own digest/drift tools.
- count-c1.py was not mutation-tested (not this seat's assignment).
- No adversarial live surface was staged beyond the controls' own URL swap (e.g. a server serving
  ua-dependent bodies).

Evidence files (raw stdout/rc/diffs per run) lived in scratch and were removed with it after the
cited lines above were extracted; the decisive outputs are quoted verbatim in this report.
Scratch `$HYAKU_SCRATCH/mori-r97/Mo97MutC2` removed; lane `count-c2.py` re-hashed after the battery:
`957a7be605ba920734a218388b7ebb50f4f829979931c6e4193caee2149a1e91` (unchanged).
