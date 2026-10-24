# ExeDagP — first-parent merge fixture

Axes: receipt fidelity; first-parent merge edit detection.

## Result

Re-derived `.ufo/waves/round-40/evidence/c11-after-fixture-p.txt` with the landed gate v3. The DAG result contains exactly one changed event, `changed S001 superseded_by=S002`; it is also present in the v2 red control. No additional changed line is attributed to the merge. The after timing line is `superseded_as_of=[S001] stale_supersede=[]`. The red v2 control instead classified S001 as stale. Both runs exit 1 for the expected append-only violation.

## Commands and outputs

Working directory for both commands: `/home/vgpnk/Projects/shokunin/mori-shokunin`.

Command:

```text
python3 .ufo/waves/round-40/fixtures/run-c11-dags.py tools/mori-sources-appendonly.py /home/vgpnk/Projects/shokunin/mori-shokunin /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/evidence/c11-after-fixture-p.txt dag-p
```

Process stdout: empty. Exit status: 0. The runner wrote this receipt to the assigned evidence path:

```text
command: python3 .ufo/waves/round-40/fixtures/run-c11-dags.py tools/mori-sources-appendonly.py /home/vgpnk/Projects/shokunin/mori-shokunin /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/evidence/c11-after-fixture-p.txt dag-p

== first-parent-lacks-path merge contributes no edits (dag-p, --round-base b0=07be6c7f1765)
P-C11: at revision R, tools/mori-sources-appendonly.py reports, after its summary line, `supersede_timing superseded_as_of=[...] stale_supersede=[...]`; the timing line's eligible set is every superseded id present at R — a never-edited superseded id's last immutable-cell edit is its first-sighting commit, so it reaches the as-of/stale test — and an edit at a commit is a change against its first parent's state only: when the first parent lacks the path the commit contributes no edits (a delete-then-re-add contributes no changed event; ids still compare tip cells against first-sighting cells), never a fall-through to another parent's state; the lane-history verdicts are unchanged except the eligible-set extension — S226 joins superseded_as_of (19 ids) at the landed tip, no id is stale at the tip, S069 is stale at e37dcc6 — and the selftest carries committed fixtures for a never-edited superseded row (as-of), a merge whose first parent lacks the path (no fabricated edit), and a linear delete-then-re-add (no changed event).
changed S001 superseded_by=S002
appendonly_violations=1 ids=[S001] deleted=[] superseded=[S001] round_changed=[S001]
supersede_timing superseded_as_of=[S001] stale_supersede=[]
EXIT=1
```

Comparison command:

```text
diff -u .ufo/waves/round-40/evidence/c11-red-firstparent.txt .ufo/waves/round-40/evidence/c11-after-fixture-p.txt
```

Exit status: 1 (files differ). Exact stdout:

```diff
--- .ufo/waves/round-40/evidence/c11-red-firstparent.txt	2026-10-24 02:41:05.314909327 -0300
+++ .ufo/waves/round-40/evidence/c11-after-fixture-p.txt	2026-10-24 03:00:22.269259845 -0300
@@ -1,8 +1,8 @@
-command: python3 .ufo/waves/round-40/fixtures/run-c11-dags.py .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py /home/vgpnk/Projects/shokunin/mori-shokunin /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/evidence/c11-red-firstparent.txt dag-p
+command: python3 .ufo/waves/round-40/fixtures/run-c11-dags.py tools/mori-sources-appendonly.py /home/vgpnk/Projects/shokunin/mori-shokunin /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/evidence/c11-after-fixture-p.txt dag-p
 
 == first-parent-lacks-path merge contributes no edits (dag-p, --round-base b0=07be6c7f1765)
-P-C9: at revision R, tools/mori-sources-appendonly.py reports, after its summary line, `supersede_timing superseded_as_of=[...] stale_supersede=[...]`; an id is superseded-as-of only when its latest superseding row's landing commit is a descendant, by `git merge-base --is-ancestor`, of the commit of the id's last immutable-cell edit, where an edit at a commit is a change against its first parent's state (not the previous walk record), the path walk uses `--full-history`, and the lane-history verdicts are unchanged — S069 is stale at `e37dcc6` and no id is stale at the round-39 tip — and the selftest carries committed fixtures for a side-branch superseder (stale, not as-of) and a merge that must not fabricate an edit (round-38 gate bytes print as-of and a fabricated edit there; the round-39 gate prints stale and no edit).
+P-C11: at revision R, tools/mori-sources-appendonly.py reports, after its summary line, `supersede_timing superseded_as_of=[...] stale_supersede=[...]`; the timing line's eligible set is every superseded id present at R — a never-edited superseded id's last immutable-cell edit is its first-sighting commit, so it reaches the as-of/stale test — and an edit at a commit is a change against its first parent's state only: when the first parent lacks the path the commit contributes no edits (a delete-then-re-add contributes no changed event; ids still compare tip cells against first-sighting cells), never a fall-through to another parent's state; the lane-history verdicts are unchanged except the eligible-set extension — S226 joins superseded_as_of (19 ids) at the landed tip, no id is stale at the tip, S069 is stale at e37dcc6 — and the selftest carries committed fixtures for a never-edited superseded row (as-of), a merge whose first parent lacks the path (no fabricated edit), and a linear delete-then-re-add (no changed event).
 changed S001 superseded_by=S002
 appendonly_violations=1 ids=[S001] deleted=[] superseded=[S001] round_changed=[S001]
-supersede_timing superseded_as_of=[] stale_supersede=[S001]
+supersede_timing superseded_as_of=[S001] stale_supersede=[]
 EXIT=1
```

The changed-event and violation lines are unchanged between red and after receipts; only the runner/gate/prose descriptors and the timing classification differ. No tools were installed. No blocker.