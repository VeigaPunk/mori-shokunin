# ExeGateLane — C2 lane line re-derivation

## Finding

Ran the append-only gate at `265a955cc67be4eae97d2dc5a9338a25f31eb29b`. Its `supersede_timing` line is byte-for-byte the same as line 22 of `.ufo/waves/round-40/evidence/c11-after-lane.txt`. Comparing the ordered as-of ID lists yields **no differing IDs**; both stale lists are empty.

The measured as-of list contains **35 IDs**, not the assigned expected count of 34. All 35, in output order, are: `S041, S044, S051, S062, S064, S067, S069, S070, S071, S083, S084, S090, S093, S096, S097, S101, S124, S127, S128, S129, S131, S140, S179, S180, S181, S182, S183, S184, S185, S186, S188, S189, S190, S193, S226`. `S226` is present and `stale_supersede=[]`. The line also matches the supplied after-lane receipt, so this is a count/claim discrepancy, not a gate-versus-receipt ID drift.

## Commands and outputs

Working directory for both commands: `/home/vgpnk/Projects/shokunin/mori-shokunin`.

1. Command: `python3 tools/mori-sources-appendonly.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --repo .`

   Exit code: **1**. Exact stdout:

   ```text
   P-C11: at revision R, tools/mori-sources-appendonly.py reports, after its summary line, `supersede_timing superseded_as_of=[...] stale_supersede=[...]`; the timing line's eligible set is every superseded id present at R — a never-edited superseded id's last immutable-cell edit is its first-sighting commit, so it reaches the as-of/stale test — and an edit at a commit is a change against its first parent's state only: when the first parent lacks the path the commit contributes no edits (a delete-then-re-add contributes no changed event; ids still compare tip cells against first-sighting cells), never a fall-through to another parent's state; the lane-history verdicts are unchanged except the eligible-set extension — S226 joins superseded_as_of (19 ids) at the landed tip, no id is stale at the tip, S069 is stale at e37dcc6 — and the selftest carries committed fixtures for a never-edited superseded row (as-of), a merge whose first parent lacks the path (no fabricated edit), and a linear delete-then-re-add (no changed event).
   changed S041 superseded_by=S206
   changed S044 superseded_by=S207
   changed S051 superseded_by=S208
   changed S062 superseded_by=S209
   changed S064 superseded_by=S210
   changed S069 superseded_by=S226
   changed S179 superseded_by=S211
   changed S180 superseded_by=S212
   changed S181 superseded_by=S213
   changed S182 superseded_by=S201
   changed S183 superseded_by=S214
   changed S184 superseded_by=S215
   changed S185 superseded_by=S216
   changed S186 superseded_by=S217
   changed S188 superseded_by=S218
   changed S189 superseded_by=S219
   changed S190 superseded_by=S220
   changed S193 superseded_by=S202
   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226] round_changed=[]
   supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226] stale_supersede=[]
   ```

2. Additional command run before consulting the seat routing entry: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b`

   Exit code: **0**. Exact stdout:

   ```text
   P-C10: at revision R, the round-40 conformance checker passes all nine checks on the round-40 counter bytes — the round-39 nine with three made sound — `timeout_scope` (every `timeout=` keyword in every counter resolves in the scope of its read site: a binding inside the enclosing function shadows the module map, a `global` rebinding is read at module scope, a module-level binding nested in `if`/`try`/`for`/`while` makes the name conditionally rebound and fails closed, and the value must be a finite positive number, so `1e400` fails and a fold raising `ZeroDivisionError` or `RecursionError` fails as a violation, not a setup error), `drain_bind` (every `Popen(` in every counter is drained in its own function by a `communicate(` bound to the same name, carrying its own timeout, with the result consumed — assigned to other than `_`, or returned — so a `wait(timeout=…)` plus `stdout.read()` drain fails even beside a decoy used communicate, an undrained second `Popen(` fails, and a tuple-wrapped or `_`-assigned communicate does not qualify), and `selftest_conjunct` (per counter: the counter's communicates all carry timeouts, stripping each communicate timeout one at a time is detected by that same rule, and the checker's own textual-mutation table carries a live `selftest_conjunct` entry whose anchor occurs in the counter — comm_violations are computed and reported per counter, not for the first counter only) — and the checker's `--selftest` applies eleven textual mutations to the counter of record, each flipping exactly its own check to FAIL.
   check predicate          PASS (exit=0 equal=True)
   check head_pin           PASS (pin=ede486b7a09afbacfb380d5871c46a8051a6dc2e tip=ede486b7a09afbacfb380d5871c46a8051a6dc2e)
   check tool_resolve       PASS (exit=0 resolved=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/fixtures/witness-summary-only-live.txt)
   check bounded_reads      PASS (count-c8.py: bounded=[] value=[])
   check timeout_scope      PASS (count-c8.py: bounded=[] value=[])
   check drain_bind         PASS (count-c8.py: violations=[])
   check timeout_state      PASS (exit=1 timeout_reason=True pass=False)
   check scratch            PASS (count-c8.py: mkdtemp_dir=True root=True)
   check selftest_conjunct  PASS (count-c8.py: honest_comm=[] strips=6 detected=6 anchor=True entry_live=True)
   CONFORM=met
   ```
