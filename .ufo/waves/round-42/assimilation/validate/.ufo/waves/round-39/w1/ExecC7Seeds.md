# C7 seed replay

## Axes and finding

- **Verdict:** all three runs printed `C7=met`.
- **Check stability:** all five checks passed for every seed. The negative-witness lines are identical and all four witnesses were rejected in every run.
- **Draw variation:** the drawn state differs across the seeds: `fresh` (20261024), `unavailable` (7), and `no-copy` (99). The only check-line detail that varies is `drift_kill_v2`'s `drawn` value and the corresponding `got` state for S103; its check result, remaining row states, `want`, `want_drifted`, and `flips_ok` are invariant.

Evidence below is the output of the requested command for each seed, run against revision `13bfba23b7ca063c76d3504a2ff6eb7b6a294932`.

## Seed 20261024

Command: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/count-c7.py 13bfba23b7ca063c76d3504a2ff6eb7b6a294932 --seed 20261024`

```text
negative witness-token-entry        rejected
negative witness-dangling-row       rejected
negative witness-summary-only-live  rejected
negative witness-comment-anchors    rejected
check anchors_v2       PASS (anchors=3 short=[] not_in_code=[] unique=True)
check capability_v2    PASS (paths=['tools/mori-source-drift.py', '.ufo/waves/round-37/evidence/c2-after-v3.txt', '.ufo/waves/round-37/evidence/drift-live-r37.txt'] not_file=[])
check live_rows_v2     PASS (named=10 summary_drifted=10 unknown=[] unique=True no_copy=[])
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill_v2    PASS (drawn=fresh exit=1 row_states=('FAIL', "got=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'fresh'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh'), ('S109', 'unavailable'), ('S110', 'unavailable')] want=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'drifted'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh'), ('S109', 'unavailable'), ('S110', 'unavailable')]") want_drifted=['S103'] flips_ok=True)
C7=met
```

## Seed 7

Command: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/count-c7.py 13bfba23b7ca063c76d3504a2ff6eb7b6a294932 --seed 7`

```text
negative witness-token-entry        rejected
negative witness-dangling-row       rejected
negative witness-summary-only-live  rejected
negative witness-comment-anchors    rejected
check anchors_v2       PASS (anchors=3 short=[] not_in_code=[] unique=True)
check capability_v2    PASS (paths=['tools/mori-source-drift.py', '.ufo/waves/round-37/evidence/c2-after-v3.txt', '.ufo/waves/round-37/evidence/drift-live-r37.txt'] not_file=[])
check live_rows_v2     PASS (named=10 summary_drifted=10 unknown=[] unique=True no_copy=[])
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill_v2    PASS (drawn=unavailable exit=1 row_states=('FAIL', "got=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'unavailable'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh'), ('S109', 'unavailable'), ('S110', 'unavailable')] want=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'drifted'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh'), ('S109', 'unavailable'), ('S110', 'unavailable')]") want_drifted=['S103'] flips_ok=True)
C7=met
```

## Seed 99

Command: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/count-c7.py 13bfba23b7ca063c76d3504a2ff6eb7b6a294932 --seed 99`

```text
negative witness-token-entry        rejected
negative witness-dangling-row       rejected
negative witness-summary-only-live  rejected
negative witness-comment-anchors    rejected
check anchors_v2       PASS (anchors=3 short=[] not_in_code=[] unique=True)
check capability_v2    PASS (paths=['tools/mori-source-drift.py', '.ufo/waves/round-37/evidence/c2-after-v3.txt', '.ufo/waves/round-37/evidence/drift-live-r37.txt'] not_file=[])
check live_rows_v2     PASS (named=10 summary_drifted=10 unknown=[] unique=True no_copy=[])
check named_row_drift  PASS (exit=0 row_states=('PASS', ''))
check drift_kill_v2    PASS (drawn=no-copy exit=1 row_states=('FAIL', "got=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'no-copy'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh'), ('S109', 'unavailable'), ('S110', 'unavailable')] want=[('S101', 'fresh'), ('S102', 'excerpt'), ('S103', 'drifted'), ('S104', 'unavailable'), ('S105', 'unavailable'), ('S106', 'no-copy'), ('S107', 'no-copy'), ('S108', 'fresh'), ('S109', 'unavailable'), ('S110', 'unavailable')]") want_drifted=['S103'] flips_ok=True)
C7=met
```

## Risks and blockers

No blocker. No install, other check, build, lint, or test was run; the three counter replays above are the requested evidence.
