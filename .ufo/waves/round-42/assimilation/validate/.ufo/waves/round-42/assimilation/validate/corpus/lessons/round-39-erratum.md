# Round-39 erratum — append-only corrections to round-39 records

The round-39 fleet report and SCORECARD C2 row state the round-38 checker
printed `CONFORM=met` on the bypass-wait fixture ("bypass-wait likewise").
The committed receipt `c8-red-wait.txt` shows the r38 checker printed
`CONFORM=unmet exit=1` ("not reproduced"): the r38 checker rejected the
final pure wait+read fixture via its `bounded_reads` popen detection, not
via drain shape, and the intermediate form that r38 accepted also passes the
round-39 checker. No single fixture was met-by-r38 and unmet-by-r39 via
`drain_shape` (round-39 lesson finding 11). The drain_shape half is
re-claimed by round 40 claim C1 with a genuine before-control
(`evidence/c10-red-decoy.txt`: the r39 checker accepts the decoy-communicate
fixture, `evidence/c10-after-decoy.txt`: the round-40 checker rejects it via
`drain_bind`). The r39 report/SCORECARD sentence is superseded by this
erratum; the r39 fleet report is committed fleet history, outside lane write
scope.

Round-39 lesson Gate row for S227 labels its located quote "(18 words)"; the
quote "you can ask for commits that are reachable from r2 excluding those
that are reachable from r1" is 17 words. The round-39 closure routed the
label correction (routed defect 4); the registry row's anchor cell is
immutable, so the count is corrected here rather than by an in-place edit.

Round-39 contract prose "pass=11" for the gate selftest was stale (the gate
prints 12); round-39 contract C3 before-cell cites
`fixtures/make-ancestry-dags.py`, a path in no commit — the real builders
are the pinned `run-c9-dags.py` plus the gate's embedded DAG selftest cases.
Both corrections are recorded here; the r39 bytes stay frozen.
