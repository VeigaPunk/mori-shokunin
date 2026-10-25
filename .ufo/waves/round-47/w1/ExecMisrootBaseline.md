# ExecMisrootBaseline — w1 report (mori round 47)

Seat: ExecMisrootBaseline. Scope: fleet-root git status snapshot + misroot sweep; detection and report only. No files deleted, no production files touched, no fleet/lane mutation. No tools installed (none needed; per operator tooling directive, no install/update occurred). Scratch: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ExecMisrootBaseline` (created; used as TMPDIR for the lane tool).

## 1. `git -C /home/vgpnk/Projects/shokunin status --porcelain` (read-only)

Exit code 0. Per-path listing (porcelain=v1, `--untracked-files=all`):

**Modified (11):**
- `.ufo/state/kaidoku.report-baseline`
- `.ufo/state/kama.report-baseline`
- `.ufo/state/kasegi.report-baseline`
- `.ufo/state/kengaku.report-baseline`
- `.ufo/state/mado.report-baseline`
- `.ufo/state/mori.report-baseline`
- `.ufo/state/souji.report-baseline`
- `.ufo/state/tabi.report-baseline`
- `.ufo/state/tameshi.report-baseline`
- `.ufo/state/tsukuroi.report-baseline`
- `.ufo/watchdog.log`

**Untracked (2):**
- `.ufo/waves/round-30/wave1/ScribeLesson.md`
- `corpus/knowledge/journalctl-v262-field-filter-r36.md`

### Round-47 name scan on untracked files only

Pattern `round-47|r47` applied to both untracked trees (`/home/vgpnk/Projects/shokunin/.ufo/waves/round-30` and `/home/vgpnk/Projects/shokunin/corpus`): **no matches**. Both untracked files were read for characterization:
- `.ufo/waves/round-30/wave1/ScribeLesson.md` — round-30 seat report (headline "Round 30", touches `corpus/lessons/round-30.md`); no round-47/r47 content.
- `corpus/knowledge/journalctl-v262-field-filter-r36.md` — round-36 systemd 262 knowledge entry (`r36` in filename, "round 36" prose); no round-47/r47 content.

**No untracked file content names mori round 47 → nothing flagged.**

## 2. Misroot sweep tool

Command (run from lane root `/home/vgpnk/Projects/shokunin/mori-shokunin`, TMPDIR=scratch above):

```
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ExecMisrootBaseline \
  python3 tools/mori-misroot-sweep.py --fleet-root /home/vgpnk/Projects/shokunin --lane mori --round 47
```

Exit code 0. Output (JSON, schema `mori-misroot-sweep-v1`):

```json
{"candidate_count": 0, "candidates": [], "detection_only": true,
 "finding": "MORI_MISROOT_CLEAN",
 "fleet_root": "/home/vgpnk/Projects/shokunin",
 "git_command": ["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C",
   "/home/vgpnk/Projects/shokunin", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
 "lane": "mori", "legacy_pathspec": null, "moves_or_deletes": false,
 "repo_root": "/home/vgpnk/Projects/shokunin", "round": 47,
 "scan": {"bytes_read": 17626, "non_regular_skipped": 0, "read_cap": 65536,
   "regular_files": 2, "truncated_files": 0, "unreadable": 0, "untracked_entries": 2}}
```

Findings:
- **finding = `MORI_MISROOT_CLEAN`**, candidate_count = 0, moves_or_deletes = false, detection_only = true.
- The sweep's own scan sees exactly the same untracked surface as git status: 2 entries / 2 regular files (the two files above), 17,626 bytes read, none truncated/unreadable, none skipped. Independent agreement with §1.

## 3. Summary

- Fleet root has 11 modified paths (all `.ufo/state/*.report-baseline` plus `.ufo/watchdog.log`) and 2 untracked files.
- Neither untracked file names mori round 47 (`round-47`/`r47` grep — no matches); the misroot sweep concurs (candidate_count=0, MORI_MISROOT_CLEAN).
- No misroot candidate to flag; nothing deleted or altered.

## Blocks / risks

- None. Verified evidence only; no UNVERIFIED items for the assigned commands.
