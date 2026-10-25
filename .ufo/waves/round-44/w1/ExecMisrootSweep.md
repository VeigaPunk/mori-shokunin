# ExecMisrootSweep — round 44, wave 1

Seat: `L1Mori44-4.ExecMisrootSweep` (leaf executor). Read-only sweep; nothing was
deleted, moved, or written outside this report.

Revisions measured during the sweep:

- fleet root `/home/vgpnk/Projects/shokunin`: `HEAD` = `23629d9885883ff452d896e6a8c00259da516d03` (branch `HEAD`)
- lane `/home/vgpnk/Projects/shokunin/mori-shokunin`: `HEAD` = `7cb59c6891d4f5d0266fe062565f094da835dc84` (branch `HEAD`) — matches the frozen instrument revision named in the wave context.

## Result

**Nothing found.** `MORI_MISROOT_CLEAN`: no untracked file at the fleet root names
`mori` or `round-44`, so there is no misroot attributable to this lane in this
sweep. Lane checkout is clean of untracked writes outside `.ufo/waves/round-44/`.

## 1. Fleet-root status (no pathspec)

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
 M .ufo/state/chousa.report-baseline
 M .ufo/state/kagi.report-baseline
 M .ufo/state/kaidoku.report-baseline
 M .ufo/state/kake.report-baseline
 M .ufo/state/kama.report-baseline
 M .ufo/state/kasegi.report-baseline
 M .ufo/state/kengaku.report-baseline
 M .ufo/state/kumitate.report-baseline
 M .ufo/state/mado.report-baseline
 M .ufo/state/mori.report-baseline
 M .ufo/state/souji.report-baseline
 M .ufo/state/tabi.report-baseline
 M .ufo/state/tameshi.report-baseline
 M .ufo/state/tsukuroi.report-baseline
 M .ufo/watchdog.log
 M scripts/hyaku/hyaku.env
 M scripts/hyaku/lane-addendum.md
?? .omp/mcp.json
?? .scratch/goal-20261025-hyaku-12h.md
?? .ufo/state/kotoba.report-baseline
?? .ufo/state/kotodama.report-baseline
?? .ufo/state/revenger.report-baseline
---EXIT:0
```

22 entries: 17 tracked modifications, 5 untracked files. The full enumeration with
`--untracked-files=all` returns the same 22 lines, so no untracked directory is
collapsing hidden children.

### Untracked files, checked for `mori` / `round-44` content

Match count is `grep -c -i -E 'mori|round-44|round 44|r44' <file>`; 0 means the file
names neither this lane nor this round.

| path | size | matches | first two lines |
|---|---|---|---|
| `.omp/mcp.json` | 285 B | 0 | `{` / `  "$schema": "https://raw.githubusercontent.com/can1357/oh-my-pi/main/packages/coding-agent/src/config/mcp-schema.json",` |
| `.scratch/goal-20261025-hyaku-12h.md` | 2667 B | 0 | `<!-- ORCHESTRATOR-OWNED run state (hyaku run 6). Not a misroot: lanes and seats never move, copy-then-delete, or edit this file. -->` / `# hyaku run 6 — 12h training run (2026-10-25)` |
| `.ufo/state/kotoba.report-baseline` | 68 B | 0 | `68 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (single line) |
| `.ufo/state/kotodama.report-baseline` | 68 B | 0 | `69 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (single line) |
| `.ufo/state/revenger.report-baseline` | 68 B | 0 | `68 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (single line) |

Verdict per file: **none is this lane's misroot.** No untracked fleet-root file
names `mori` or `round-44`, so no seat wrote a mori-round-44 artifact to the fleet
root in the bytes `git status` can see. For the record:

- `.omp/mcp.json` — agent-harness MCP config (`rea` stdio server, `"enabled": false`); fleet-level tooling, lane-agnostic.
- `.scratch/goal-20261025-hyaku-12h.md` — self-declares as ORCHESTRATOR-OWNED hyaku run-6 state; lane-agnostic.
- `.ufo/state/{kotoba,kotodama,revenger}.report-baseline` — one-line `<count> <sha256>` baselines belonging to other seats (kotoba, kotodama, revenger), same shape as the 14 tracked `*.report-baseline` files; not mori artifacts.

### Tracked modifications (reported, not misroot candidates)

The 17 ` M` entries are fleet-root orchestrator state and hyaku runner scripts
(`git diff --stat`: 17 files changed, 712 insertions(+), 31 deletions(-); the bulk is
`.ufo/watchdog.log` +676 lines and `scripts/hyaku/{hyaku.env,lane-addendum.md}`).
`.ufo/state/mori.report-baseline` is among them: it is a *tracked* two-line baseline
edit by the fleet's baseline machinery, not an untracked file written by a seat, and
`mori-misroot-sweep.py` inspects untracked files only. Flagged here for visibility,
not scored as a misroot.

## 2. Misroot sweep

The assigned argv, run from the fleet root (the default tool cwd), fails because the
tool is not installed at the fleet root — it lives in the lane repo's `tools/`:

```
$ cd /home/vgpnk/Projects/shokunin && python3 tools/mori-misroot-sweep.py --fleet-root /home/vgpnk/Projects/shokunin --lane mori --round 44
python3: can't open file '/home/vgpnk/Projects/shokunin/tools/mori-misroot-sweep.py': [Errno 2] No such file or directory
---EXIT:2
```

Same argv, run with cwd = lane repo so the relative script path resolves (all flags
identical, `--fleet-root` still the fleet root):

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 tools/mori-misroot-sweep.py --fleet-root /home/vgpnk/Projects/shokunin --lane mori --round 44
{"candidate_count": 0, "candidates": [], "detection_only": true, "finding": "MORI_MISROOT_CLEAN", "fleet_root": "/home/vgpnk/Projects/shokunin", "git_command": ["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", "/home/vgpnk/Projects/shokunin", "status", "--porcelain=v1", "-z", "--untracked-files=all"], "lane": "mori", "legacy_pathspec": null, "moves_or_deletes": false, "repo_root": "/home/vgpnk/Projects/shokunin", "round": 44, "scan": {"bytes_read": 3156, "non_regular_skipped": 0, "read_cap": 65536, "regular_files": 5, "truncated_files": 0, "unreadable": 0, "untracked_entries": 5}, "schema": "mori-misroot-sweep-v1"}
---EXIT:0
```

- argv: `python3 tools/mori-misroot-sweep.py --fleet-root /home/vgpnk/Projects/shokunin --lane mori --round 44`
- exit code: `0`
- `finding`: `MORI_MISROOT_CLEAN`, `candidate_count`: `0`, `candidates`: `[]`
- scan: 5 untracked entries, 5 regular files, 3156 bytes read, 0 truncated, 0 unreadable, 0 non-regular skipped, 64 KiB read cap
- `detection_only: true`, `moves_or_deletes: false`

The tool's 5 untracked entries agree exactly with the 5 `??` lines in §1.

## 3. Lane checkout clean of untracked writes outside `.ufo/waves/round-44/`

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain
?? .ufo/waves/round-44/w1-spec.json
---EXIT:0
```

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --porcelain --untracked-files=all | grep -v '^?? \.ufo/waves/round-44/' || echo "(none)"
(none)
```

Confirmed: the lane's only status entry is `?? .ufo/waves/round-44/w1-spec.json`,
which is inside `.ufo/waves/round-44/`. No tracked file is modified in the lane
checkout (frozen instruments `contract.md`, `count-c1.py`, `count-c2.py`,
`count-c3.py`, `tools/mori-gate-registry.py`, `fixtures/`, `SKILL.md`, `SCORECARD.md`,
`LOG.md`, `corpus/` all show no modification). This report adds only
`.ufo/waves/round-44/w1/ExecMisrootSweep.md`, likewise inside the round directory.

## Limits of this sweep

- `mori-misroot-sweep.py` reads only the first 65536 bytes of each untracked
  *regular* file and inspects untracked files only; git-ignored files never reach
  `git status` and cannot be seen by this sweep. 0 files were truncated here
  (max file 2667 B), so the byte cap did not bite.
- A candidate would be a review lead, not proof of seat ownership; there were none,
  so no header adjudication was needed.
- No tool was installed or upgraded for this task.

## Files changed

- `.ufo/waves/round-44/w1/ExecMisrootSweep.md` (this report) — nothing else.
