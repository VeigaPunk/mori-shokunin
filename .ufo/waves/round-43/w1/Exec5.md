# Exec5 — mori round 43, wave w1

Assigned move (L1): run `sha256sum .ufo/waves/round-42/count-c1.py` from the lane repo and paste stdout/stderr/exit code. Read-only evidence run; no production edits.

## Command as executed

- cwd: `/home/vgpnk/Projects/shokunin/mori-shokunin`
- command: `sha256sum .ufo/waves/round-42/count-c1.py` (wrapped with `printf 'exit_code=%s\n' "$?"` solely to surface the exit code in stdout)

## Exact evidence

stdout:
```
105ce075f33120837ba5a49a1ad4f23a3dd7dc17fea506ab917140bc7f2053f6  .ufo/waves/round-42/count-c1.py
exit_code=0
```

stderr: (empty — none produced)

exit code: `0`

- wall time: 0.020 s
- working directory confirmed via `pwd`: `/home/vgpnk/Projects/shokunin/mori-shokunin`

## Files changed

- `.ufo/waves/round-43/w1/Exec5.md` (this report — the only file written)
- No production files touched. Frozen counter `.ufo/waves/round-42/count-c1.py` was only read (sha256sum), never edited. No writes to fleet files, sibling repos, lane Git/jj state, lane index, `.ufo/state`, or `.ufo/watchdog.log`. All execution was a read-only hash in place; no code run outside the assigned command (no /tmp sandbox needed).

## Behavior

One read-only integrity probe of the round-42 frozen counter. Establishes the baseline digest `105ce075f33120837ba5a49a1ad4f23a3dd7dc17fea506ab917140bc7f2053f6` for round-43 attack/verification work; attack copies must be made in scratch, never in place.

## Remaining risks

- Digest reflects the file state at run time (2026-10-24); any later mutation of the counter would invalidate the baseline. Cross-checks by other seats should compare against this hash.
- Nothing else observed.

## Blockers

- None.

## Scope statement

Leaf member: zero subagents dispatched (not probeParent-seated). Stopped after the assigned implementation; shipping decisions left to the operator/L1.
