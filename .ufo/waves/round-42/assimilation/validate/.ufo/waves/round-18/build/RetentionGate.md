# Round 18 C1 retention gate — executor report

## Files changed

- `.ufo/worktrees/round-18/RetentionGate/tools/mori-retention-gate.py`
- `.ufo/worktrees/round-18/RetentionGate/.ufo/waves/round-18/gate-snapshots/retention/retention.json` (new, one-file pinned snapshot)

The scanner validates the frozen policy, traverses only the requested revision using `git cat-file` and `git ls-tree`, skips NUL-containing blobs, decodes UTF-8 with replacement, and emits hit metadata only (path, line, class, line SHA-256). It implements allowlist matching, forbidden entries on must-redact paths, stale-row warnings, non-author metric exclusion, and full population comparison. Selftest fixtures and the frozen snapshot's synthetic line are base64-encoded in tracked files so their test-only match strings do not become retained hits themselves. The frozen snapshot has one file; its SHA-256 is pinned in the tool.

## Required evidence

All commands below ran against the final tool SHA-256 recorded below.

1. Command:

   `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/RetentionGate/tools/mori-retention-gate.py scan --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev d005cdd --policy /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/frozen/c1-policy.json --expect-population /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/frozen/c1-population.json`

   Exit **1** (`RETENTION_FINDINGS`): metric **116**, routed **40**, population_match **true**, 119 total hit rows, 3 non-author hit rows, 0 new and 0 missing population rows.

2. Command:

   `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/RetentionGate/tools/mori-retention-gate.py scan --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev 29b0dc7 --policy /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/frozen/c1-policy.json --expect-population /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/frozen/c1-population.json`

   Exit **1** (`RETENTION_FINDINGS`): metric **120**, routed **40**, population_match **false**, 123 total hit rows, 3 non-author hit rows, **4 new** and 0 missing population rows. This does **not** meet the requested “identical hits plus zero new” expectation at 29b0dc7. I left the frozen-policy result intact rather than suppressing or reclassifying those hits.

3. Command:

   `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/RetentionGate/.scratch python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/RetentionGate/tools/mori-retention-gate.py --selftest`

   Exit **0**: `SELFTEST retention-gate PASS 19/19`. The arms cover positive R1–R9 cases; the R2 root-only and R4 no-trailing-slash negative controls; binary skip; allowlist match by line SHA-256; allowlist_forbidden; allowlist_stale warning; non-author exclusion; missing revision; tampered snapshot; and a planted fake secret absent from stdout.

4. Command:

   `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/RetentionGate/tools/mori-retention-gate.py --frozen-run`

   Exit **0** (`FROZEN_OK`): verdict_match **true**; the pinned synthetic verdict is a one-hit, exit-1 scan result with metric 1 and routed 1. Snapshot SHA-256: `55fcdd710d2bec1eef198997b3ccfa4fc584b7c7d44ad447fccf6fa48d8a00e8`.

## Integrity, risks, and blockers

- Tool SHA-256: `9d42f403373d976405e804251ed4a5d010eb648f05c05e02cd909d08a8e52d05`.
- Snapshot SHA-256: `55fcdd710d2bec1eef198997b3ccfa4fc584b7c7d44ad447fccf6fa48d8a00e8`.
- The 29b0dc7 expectation is the outstanding blocker: measured results contain four new rows versus the frozen d005cdd population. No matched text or hit paths are reproduced here. This executor made no lane-source, allowlist, or frozen-input changes.
- No tools were installed. No build, lint, formatter, or unrelated test commands were run. LSP was unavailable in the exposed tool routes; this standalone new tool had no existing caller symbols to refactor.
