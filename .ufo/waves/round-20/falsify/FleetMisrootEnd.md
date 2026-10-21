HOLDS

Scoped result: no untracked file in the fleet root names mori round 20 or a MoriR20 seat. The only untracked entry, `.ufo/waves/round-20/final/AuditCase07.md`, is a Souji audit artifact. It is a probable Souji misroot [INFERENCE], not a mori artifact.

## 1. The command as written fails; an equivalent read-only run was used

- `git -C /home/vgpnk/Projects/shokunin status --porcelain --no-optional-locks` prints `error: unknown option 'no-optional-locks'` plus usage, **exit 129**. `--no-optional-locks` is a global git option and must come before the subcommand.
- Equivalent run used instead (same read-only effect, no pathspec): `git --no-optional-locks -C /home/vgpnk/Projects/shokunin status --porcelain` → **exit 0**:

```
 M .ufo/l0-questions.md
 M .ufo/state/kagi.report-baseline
 M .ufo/state/kama.report-baseline
 M .ufo/state/mori.report-baseline
 M .ufo/state/tabi.report-baseline
 M .ufo/watchdog.log
?? .ufo/waves/round-20/
```

- Same command with `--untracked-files=all` → **exit 0**. The only `??` entry is `.ufo/waves/round-20/final/AuditCase07.md`.
- Tooling: git 2.56.0, pre-installed. Nothing installed or updated.

## 2. Match criteria and result

- Seat names: 76 from `wave1-spec.json` + 67 from `wave2-spec.json` = 143 unique, 0 duplicates (`/usr/bin/jq -r '.items[].name'`).
- `AuditCase07.md` (8784 bytes, 112 lines), Python fixed-string check, word-bounded:
  - seat-name hits: 0 of 143
  - `mori` (any case): 0. `MoriR20`: 0.
  - `round-20` / `r20` tokens: 7, all Souji. Line 1 "round-20 C1 case"; line 29 `/var/tmp/souji-r20-audit-contract.*`; line 31 `souji-r20w2-audit-contract`; line 40 `.ufo/waves/round-20/w2/Seat.md`; line 112 `r20-audit-contract.py`.
  - `souji` tokens: 5.
- Path `.ufo/waves/round-20/final/AuditCase07.md`: contains `round-20`, but no `mori` and no seat name.
- Result: 0 untracked files qualify.

## 3. Why AuditCase07 is Souji's (probable misroot)

- Content cites `tools/souji-seat-audit.py` and Souji waves. Pin `1988860ed28a460f4e5228dfcdb3a7a6c5b8d8f1`:
  - `git --no-optional-locks -C souji-shokunin cat-file -t <pin>` → `commit`, exit 0.
  - Same against the fleet repo → `fatal: git cat-file: could not get object info`, exit 128.
- `souji-shokunin/.ufo/waves/round-20/final/` holds AuditCase01–06 and AuditCase08–25. AuditCase07 is the only gap, and the fleet-root copy fills it.
- Souji's round-20 final artifacts live in its own lane. The souji line appended to tracked `.ufo/l0-questions.md` cites `souji-shokunin/.ufo/waves/round-20/final/FinalHeldAuthority.md`.
- [INFERENCE] The fleet-root file is Souji's AuditCase07, written with a fleet-root-relative path.

## 4. Timeline (`stat`, -03:00)

| Object | Time |
|---|---|
| fleet `round-20/` and `round-20/w1/` birth | 2026-10-21 06:56:45 (same instant) |
| fleet `round-20/w1/` | empty, 0 entries. git does not report empty directories. |
| fleet `round-20/final/` and AuditCase07.md birth | 07:02:53 |
| fleet `round-20/` ctime and mtime | 07:27:57. An entry was created or removed then; none remains. Cause unobserved. |
| watchdog.log line 584: `launch mori round=20 pgid=1498812` | 07:18:05 |
| mori lane `build/ evidence/ falsify/ frozen/` birth | 07:22:30 |
| mori `wave1-spec.json` / `wave1-dispatch-receipt.json` birth | 07:26:28 / 07:27:06 |

- The watchdog log shows `round=20` launches by 8 lanes: mado, kaidoku, kama, tameshi, tsukuroi (05:13:11), souji (05:13:50), tabi (06:47:50) and mori (07:18:05). "round-20" alone does not identify mori.
- The fleet-root tree predates the mori launch record by 21 min and the mori lane tree by 26 min. [INFERENCE] mori did not create it.
- The 07:27:57 change came 51 s after the mori wave-1 dispatch receipt. Nothing persisted, so the tree cannot attribute it. [INFERENCE] unattributed.

## 5. Tracked changes that name mori round 20 (outside the untracked scope; flagged)

- `.ufo/state/mori.report-baseline`: `-19 e3b0…` → `+20 e3b0…`. Kagi, kama and tabi move the same way (24→25, 20→21, 19→20). [INFERENCE] orchestrator launch bookkeeping, not a misrooted report.
- `.ufo/watchdog.log`: four lines appended at lines 582–585, including `2026-10-21T07:18:05-03:00 launch mori round=20 pgid=1498812 driver=hyaku-inline attempt=1`.
- Both are uncommitted modifications. Neither is a report written to the wrong root.

## 6. Ignored entries (names only)

Ignored entries were listed with pathspec exclusions for `.ufo/interactive-sessions`, `.ufo/worktrees` and `.jj`. Those directories were never opened.

- `!! "bash: /home/vgpnk/Projects/shokunin/souji-shokunin/"`: a directory named `bash: ` (trailing space) that mirrors `home/vgpnk/Projects/shokunin/souji-shokunin/tests/tools/`. Its mtime is 2026-10-18 14:01, which predates this session. Its leaf is a regular file named `souji-verify.sh: No such file or directory`. [INFERENCE] a shell error string used as a path. Souji-related, not mori.
- `!! mori-shokunin/`: the lane itself, ignored by `.gitignore:1` (`*-shokunin/`).
- No other ignored name contains `round-20` or `mori`.

## 7. Limits

- "Untracked" follows `git status`. Ignored files and empty directories are excluded. Ignored entries were checked by name only, and their contents were not read.
- Tracked files were examined only where listed in section 5. Other lanes were not searched, per the bounds. The verdict covers the fleet root only.

## 8. Side effects

- Fleet root: no writes, no deletions, no index writes (`--no-optional-locks`).
- Written: this report at `mori-shokunin/.ufo/waves/round-20/falsify/FleetMisrootEnd.md`. Scratch files are under `/tmp/mori-r20-*`.
- No subagents, no tool installs, no census run.

## 9. For the main agent

- Ask the Souji owner to confirm and relocate `.ufo/waves/round-20/final/AuditCase07.md`. It was not moved or deleted here.
- After that, re-run `git --no-optional-locks -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all`. Expect no untracked lines.
- The empty `round-20/w1/` and the `bash: ` tree are invisible to `status`. They need the same owner decision.
