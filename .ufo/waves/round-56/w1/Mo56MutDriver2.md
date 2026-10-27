# Mo56MutDriver2 — mutation probe of tools/mori-driver-liveness.py (16 mutants)

Seat task: mutation-test the C1 driver-liveness probe with the four assigned
mutations plus at least eight more, same protocol as MutDriver1: one plausible
single-point defect at a time on an isolated scratch copy, run the same bounded
detector on pristine/mutated/restored bytes, record mutant / expected detector /
output / verdict / restoration evidence. Leaf seat, detection and report only.

## Detector and environment

- Detector (bounded, frozen): the tool's own selftest —
  `python3 <copy>/tools/mori-driver-liveness.py --selftest` — which runs the 13
  `t_*` cases over the 9 frozen fixtures. Kill criterion: `fail>0` (rc=1). The
  copy sits at `<scratch>/tools/` with fixtures at
  `<scratch>/.ufo/waves/round-56/fixtures/driver/` because `_fixture_dir()`
  resolves relative to `__file__` (tool line 251-253).
- Pristine bytes: `tools/mori-driver-liveness.py` sha256
  `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997` — equal to
  the frozen PIN in `.ufo/waves/round-56/count-c1.py:46` (verified
  `sha256sum` on the repo file; the repo file was never written, only copied).
- Baseline on pristine bytes: `DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0`,
  rc=0. A nonzero baseline would make every verdict INCONCLUSIVE; it is green.
- Scratch: `/fast/scratch/hyaku/mori-r56/Mo56MutDriver2/`
  (`TMPDIR=<scratch>/tmp`). Methodology script `mutate.py` lived there; each
  mutant applied as exact-once `str.replace` on pristine bytes, selftest run,
  bytes restored, sha256 re-asserted after every probe. Fixture tree copied
  with `shutil.copytree(..., symlinks=True)` — required: `state-shapes/state/
  kake.round` is a symlink (`kake.round -> mori.round`); a dereferencing copy
  silently degrades `t_state_shapes` (observed: naive copytree made the
  baseline fail `t_state_shapes`, proving the case is fixture-sensitive).
- Survivor validity rule: a survived mutant is only a coverage finding if it is
  behavior-bearing, so each survivor was re-run on a synthetic input where its
  JSON output must differ from pristine (diffs recorded below).
- No installs needed; `python3` stdlib only.

## Mutation results (16 mutants: 8 KILLED, 8 SURVIVED)

All lines reference the pinned file `mori-shokunin/tools/mori-driver-liveness.py`.

| # | Mutation (behavior-bearing point) | Verdict | Killing case(s) | Fixture coverage |
|---|-----------------------------------|---------|-----------------|------------------|
| M1 | `state_shapes` follows symlinks: `isfile` tested before `islink` (lines 188-191, order swapped) | KILLED | `t_state_shapes` | `state-shapes` fixture's `kake.round` symlink-to-regular discriminates; only symlink in all 9 fixtures |
| M2 | `lane-dead-no-report` does not clear the round's `open_launches` (line 157 deleted) | KILLED | `t_attempt_rollover` | `attempt-rollover` has launch(att1) -> dead r56 -> launch(att2) -> complete(att2); unclosed 1 vs 0 |
| M3 | complete-side attempt keying dropped: closes `(round,None)` only (lines 139-140 deleted) | KILLED | `t_hyaku_pairing`, `t_attempt_rollover` | `hyaku-pairing`, `attempt-rollover`, `two-lanes`, `variants` all pair attempt-keyed launch/complete; the two simplest fail first |
| M4 | `parse_ts` accepts any token: `return 0.0` instead of `None` (lines 73-74) | KILLED | `t_malformed_refusal`, `t_other_lines_not_malformed` | `malformed` fixture has 5 ts-broken lines + 1 ts-first non-event line; mutant reclassifies 4 malformed as events + 1 as other_lines |
| M5 | `in_flight` conflated with unclosed: `len(open_launches)>0` instead of `last_event=="launch"` (line 172) | SURVIVED | — | No fixture leaves an open launch when `last_event` is complete/dead/wrap; `in_flight` only ever co-varies with `unclosed>0` in fixtures |
| M6 | `wrap` does not close the round's open launch (line 150 `close_round()` deleted) | SURVIVED | — | `variants` wraps lanes kotoba/mado that have NO open launch; no fixture has launch-then-wrap in one round |
| M7 | `lane-dead-no-report` clears open launches of ALL rounds (`open_launches=[]` instead of round filter, line 157) | SURVIVED | — | `attempt-rollover`/`fails-and-dead` have deads only with open launches in the SAME round; cross-round scope untested |
| M8 | `close_round` removes ALL opens of the round, not the keyed one (lines 116-120 rewritten) | SURVIVED | — | No fixture has two concurrent same-round opens where exactly one is keyed-closed |
| M9 | `state_shapes` drops the `*.round` name filter (lines 185-186 deleted) | SURVIVED | — | `state-shapes/state/` contains only `.round` names; filter dead code under fixtures |
| M10 | whitespace-only log no longer "empty": `text==""` instead of `text.strip()==""` (line 217) | SURVIVED | — | `t_empty_log` writes `""` only; no whitespace-only log input |
| M11 | `newest_ts` takes last event ts, not max (line 108) | SURVIVED | — | `log.newest_ts` asserted by no case; fixture logs are ts-ordered |
| M12 | `rounds_seen` counts event lines not distinct rounds (`set`->`list`, lines 111,113,170) | SURVIVED | — | `rounds_seen` asserted by no case |
| M13 | wrap rest accepts only `landed`, the `complete` form malformed (line 62) | KILLED | `t_variants` | `variants` has `wrap mado round=51 complete` — only wrap-complete line in fixtures |
| M14 | ts-first non-event prose counted malformed, not `other_lines` (lines 101-102 -> `_bad`) | KILLED | `t_variants`, `t_other_lines_not_malformed` | `variants` 2 other_lines, `malformed` 1 other_line; boundary explicitly counted |
| M15 | dead rest requires the `(...)` parenthetical (line 60) | KILLED | `t_launch_fail_and_dead_legacy` | `fails-and-dead` dead has no paren; `attempt-rollover` has one — paren-vs-no-paren covered |
| M16 | complete rest accepts only `; hyaku-inline attempt=<n>` (line 59) | KILLED | `t_legacy_grammar`, `t_variants` | `legacy-grammar` (advancing), `variants` (respawning) cover the non-inline complete forms |

## Survivor validity evidence (synthetic inputs, pristine vs mutant)

Each diff is `path: [pristine, mutant]` in the emitted JSON (tool run with
`--now 1800000000 --log <syn>` on a one-lane synthetic `watchdog.log`):

- M5 — `launch att=1; launch att=2; complete att=1` (same round):
  `/lanes/mori/in_flight: [false, true]`. Pristine reports not-in-flight after
  a complete; mutant reports in-flight because attempt-2 launch stays open.
- M6 — `launch r9; wrap r9 landed`: `/lanes/mori/unclosed: [0, 1]`.
- M7 — `launch r1; launch r2; dead r1`: `/lanes/mori/unclosed: [1, 0]` —
  mutant wrongly clears the still-open round-2 launch.
- M8 — `launch att=1; launch att=2; complete att=1` (same round):
  `/lanes/mori/unclosed: [1, 0]` — mutant closes the attempt-2 launch it was
  not keyed to.
- M9 — state dir `{mori.round (file), README.txt (file)}`:
  `/state_dir/regular: [1, 2]` — non-`.round` entries leak into shape counts.
- M10 — log containing `  \n\n`: pristine `verdict=DRIVER_LIVENESS_UNAVAILABLE`,
  `log.state="empty"`, rc=2; mutant `verdict=DRIVER_LIVENESS_OK`,
  `log.lines=0`, rc=0 — violates the docstring "missing/unreadable/empty log —
  unavailable is never zero".
- M11 — out-of-order ts (`10:30` launch, `10:00` complete):
  `/log/newest_ts: [1793107800.0, 1793106000.0]`.
- M12 — `attempt-rollover` fixture itself: `/lanes/mori/rounds_seen: [1, 4]` —
  the field is emitted but never asserted.

Every survivor differs from pristine -> none is an equivalent mutant; each is a
real coverage hole in the 13-case detector.

## Restoration evidence

- Every mutant: `mutant_sha256` recorded (first 16 hex in probe log), file
  restored to pristine bytes, `restored_sha256 == 6b3dba74c639190e` asserted
  per mutation (`assert` in driver; all printed `pristine match: True`).
- Final: `FINAL sha256=6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997 (pristine True)`;
  repo `sha256sum` re-verified identical to PIN after the run. The lane repo,
  fleet repo, and fixtures were never written — mutation applied only to the
  scratch copy.

## Detector transcript (verbatim)

```
PRISTINE sha256=6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997
BASELINE rc=0 :: DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0
M1  KILLED   fail=1  failed=t_state_shapes
M2  KILLED   fail=1  failed=t_attempt_rollover
M3  KILLED   fail=2  failed=t_hyaku_pairing,t_attempt_rollover
M4  KILLED   fail=2  failed=t_malformed_refusal,t_other_lines_not_malformed
M5  SURVIVED pass=13 fail=0  (synthetic diff: in_flight false->true)
M6  SURVIVED pass=13 fail=0  (synthetic diff: unclosed 0->1)
M7  SURVIVED pass=13 fail=0  (synthetic diff: unclosed 1->0)
M8  SURVIVED pass=13 fail=0  (synthetic diff: unclosed 1->0)
M9  SURVIVED pass=13 fail=0  (synthetic diff: state_dir/regular 1->2)
M10 SURVIVED pass=13 fail=0  (synthetic diff: verdict UNAVAILABLE->OK, rc 2->0)
M11 SURVIVED pass=13 fail=0  (synthetic diff: log/newest_ts 1793107800->1793106000)
M12 SURVIVED pass=13 fail=0  (synthetic diff: rounds_seen 1->4)
M13 KILLED   fail=1  failed=t_variants
M14 KILLED   fail=2  failed=t_variants,t_other_lines_not_malformed
M15 KILLED   fail=1  failed=t_launch_fail_and_dead_legacy
M16 KILLED   fail=2  failed=t_legacy_grammar,t_variants
FINAL sha256=6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997 (pristine True)
```

## Mutant specifications (exact replacements applied)

- M1: swap `if os.path.islink(p):` block with `elif os.path.isfile(p):` (lines
  188-191) so the file test runs first.
- M2: delete `row["open_launches"] = [k for k in row["open_launches"] if k[0] != int(round_s)]` (line 157).
- M3: delete `if m2.group(1) is not None: key = (int(round_s), int(m2.group(1)))` (lines 139-140).
- M4: `except (ValueError, OverflowError): return None` -> `return 0.0` (lines 73-74).
- M5: `"in_flight": row["last_event"] == "launch"` -> `"in_flight": len(row["open_launches"]) > 0` (line 172).
- M6: delete `close_round()` in the `wrap` branch (line 150).
- M7: line 157 -> `row["open_launches"] = []`.
- M8: `close_round` body (lines 116-120) -> `row["open_launches"] = [k for k in row["open_launches"] if k[0] != int(round_s)]`.
- M9: delete `if not name.endswith(".round"): continue` (lines 185-186).
- M10: `if text.strip() == "":` -> `if text == "":` (line 217).
- M11: `newest_ts = ts if newest_ts is None else max(newest_ts, ts)` -> `newest_ts = ts` (line 108).
- M12: `"rounds": set()` -> `"rounds": []` and `row["rounds"].add(...)` -> `.append(...)` (lines 111, 113).
- M13: WRAP_REST_RE `(?:landed|complete)` -> `landed` (line 62).
- M14: `other_lines += 1` -> `_bad(raw)` (line 101).
- M15: DEAD_REST_RE `(?: \((.*)\))?` -> ` \((.*)\)` (line 60).
- M16: COMPLETE_REST_RE `(?:hyaku-inline attempt=(\d+)|advancing to round=(\d+)|respawning)` -> `hyaku-inline attempt=(\d+)` (line 59).

## Assessment

The detector is strong where the fixtures were authored to discriminate:
attempt pairing (M2, M3), the malformed/other_lines boundary and ts-validity
gate (M4, M14), grammar variants for dead/wrap/complete rests (M13, M15, M16),
and the symlink classification (M1). It is blind along three axes:

1. Pairing-state semantics under interleavings no fixture encodes — concurrent
   same-round opens (M5, M8), launch-then-wrap (M6), dead with opens in other
   rounds (M7). All four change `unclosed`/`in_flight` on plausible live-log
   interleavings and all four pass 13/13.
2. Filter/predicate boundaries with no exercising fixture — non-`.round`
   entries in the state dir (M9), whitespace-only logs (M10). M10 is the
   worst survivor: it flips verdict UNAVAILABLE->OK with rc 2->0 on input the
   docstring calls empty.
3. Emitted-but-never-asserted fields — `log.newest_ts` (M11) and
   `lanes.*.rounds_seen` (M12) can regress freely; `mtime_age_s` was not even
   probed since nothing reads it.

Surviving mutants are coverage findings only; no contract change is proposed.
Routing for round 57 (named limits, not fixes): a fixture with two same-round
attempt opens + keyed complete; a launch-then-wrap fixture; a dead fixture
with opens in a second round; a non-`.round` entry in the state fixture; a
whitespace-only-log case; assertions on `newest_ts`/`rounds_seen`.

UNVERIFIED: what MutDriver1 probed (its report was not in `w1/` at run time);
overlap with its mutation set is possible for the four assigned mutants M1-M4
only if that seat received the same list. No sibling files were touched.

## Findings

- **MED** — Surviving mutants M5, M8: `unclosed`/`in_flight` pairing semantics
  under concurrent same-round attempt opens are untested; a wrong-key or
  close-all defect ships silently. `tools/mori-driver-liveness.py:116-120,172`.
- **MED** — Surviving mutant M6: `wrap` failing to close a round's open launch
  is undetected; wrap fixtures (`variants`: kotoba, mado) carry no open
  launches. `tools/mori-driver-liveness.py:144-150`.
- **MED** — Surviving mutant M7: `lane-dead-no-report` clearing other rounds'
  open launches is undetected; both dead fixtures have opens only in the dead
  round. `tools/mori-driver-liveness.py:157`.
- **MED** — Surviving mutant M10: whitespace-only log flips
  `DRIVER_LIVENESS_UNAVAILABLE` (rc 2) to `OK` (rc 0) with `lines=0`,
  contradicting the docstring's "unavailable is never zero"; only `""` is
  tested. `tools/mori-driver-liveness.py:217`.
- **LOW** — Surviving mutant M9: `*.round` suffix filter is dead code under
  the state fixture (only `.round` names present); stray state-dir entries
  would silently inflate shape counts. `tools/mori-driver-liveness.py:185-186`.
- **LOW** — Surviving mutants M11, M12: `log.newest_ts` (line 108) and
  `lanes.*.rounds_seen` (lines 111,113,170) are emitted but asserted by no
  case; also `log.mtime_age_s` (line 227) is unasserted — unprobed.
- **LOW** — Fixture-robustness note (not a surviving mutant): the
  `state-shapes` fixture's discriminating `kake.round` symlink means any
  fixture-copy path that dereferences symlinks silently degrades
  `t_state_shapes`' meaning; observed firsthand (naive `copytree` broke the
  baseline). `.ufo/waves/round-56/fixtures/driver/state-shapes/state/`.

Report: .ufo/waves/round-56/w1/Mo56MutDriver2.md
