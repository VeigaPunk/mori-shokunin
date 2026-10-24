# Round-18 misroot and scratch audit

Read-only checks completed; no files were deleted or changed by the checks. This report is the sole requested write.

## Findings

- Fleet root `git -C /home/vgpnk/Projects/shokunin status --porcelain` exited 0. It showed tracked modification `.ufo/watchdog.log`; untracked `.ufo/reports/round-19/kama.md`; 14 untracked `.ufo/state/*.report-baseline` files (`chousa`, `kagi`, `kaidoku`, `kake`, `kama`, `kasegi`, `kengaku`, `kumitate`, `mado`, `mori`, `souji`, `tabi`, `tameshi`, `tsukuroi`); and untracked `.ufo/waves/round-37/`.
- Of those untracked paths, `.ufo/reports/round-19/kama.md` is the only one observed to contain round-18 references. Its first line identifies a round-19 report; this is a cross-round reference in a fleet-root report, not evidence that an r18 file was misrooted into the mori lane. The state baselines' first lines were metadata-only and did not name round 18. The sole file listed below `round-37/` was `falsify/AuditRemainder6.md`; its first line identifies round 37, not round 18.
- The requested first-line selector on Markdown files returned the full Markdown heading block from `read`; I used no excerpts in this report. This limits the first-line-only check for those Markdown files; the full-block return exposed the round-18 references above.
- `/tmp` scan: the unprivileged command emitted no matching paths but exited 1 because traversal encountered permission-denied directories. A read-only `sudo -n` retry with the same depth, time cutoff, and name predicate completed with exit 0 and no matches. Thus no matching `*mori*` path newer than `2026-10-21 02:47` was found within `/tmp` at depth 2.
- Clone porcelain results, all exit 0:
  - `DispatchLedger`: `?? tools/mori-dispatch-ledger.py`
  - `FreezeOrder`: `?? tools/mori-freeze-order.py`
  - `RetentionGate`: `?? .ufo/waves/round-18/gate-snapshots/`; `?? tools/mori-retention-gate.py`
  - `MutDispatchLedger`, `MutFreezeOrder`, `MutRetentionGate`: empty status output.
- Directory listings showed `.scratch/` directories in the six clones. The requested porcelain checks did not list `.scratch/`; their contents were not inspected, so this does not establish that they are empty.

## Commands and exits

- `git -C /home/vgpnk/Projects/shokunin status --porcelain` — exit 0.
- `find /tmp -maxdepth 2 -newermt '2026-10-21 02:47' -name '*mori*'` — exit 1 (permission errors; incomplete unprivileged traversal).
- `sudo -n find /tmp -maxdepth 2 -newermt '2026-10-21 02:47' -name '*mori*'` — exit 0, no matches.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/<clone> status --porcelain` — exit 0 for each of `DispatchLedger`, `FreezeOrder`, `RetentionGate`, `MutDispatchLedger`, `MutFreezeOrder`, and `MutRetentionGate`; results above.

No tools were installed or updated.
