measured 2026-10-23T09:34:11Z
# Residual CritNoHarm N1–N3

Advisory attack of `6d3d94b396698d67555a51c565eb6dc58d8cfa09` against `cedb0ec4f3a4f672804deac388b7191258f01fcd`; no canonical judgment or admission.
Notation: `$L` = `/home/vgpnk/Projects/shokunin/mori-shokunin`; `$T` = the full attacked tip above; `$S` = `/fast/scratch/hyaku/mori-r35/MoriR35.ResNoHarmFixes`. Output blocks are relevant excerpts, not complete stdout.
Axes: depth (technical correctness), operability (the declared command/result interface), calibration (truthful conformance claims).

| Axis | Original harm gone? | Revision introduces new harm? |
|---|---|---|
| depth | Yes: N1 now predicates partition status on the device. | None found in the revised sentence. |
| operability | Yes: N2's invalid-revision error now exits 2; a completed debt scan still exits 1. | N3's newly added round-pass mode returns 0 on a forbidden in-place restoration. |
| calibration | Yes: N3 no longer treats supersession as an append-only waiver. | Yes: the new round-pass authority overclaims absence of in-place edits; counterexample below. |

## N1 — device/parent predicate
VERDICT: holds — N1 fixed without new harm in the examined correction.

Commands: `timeout 120s git -C "$L" show "$T:SKILL.md"` and `timeout 120s git -C "$L" show "$T:corpus/evidence/sources-r34/S193.src"`.
Observed `SKILL.md:846-848`: “the device has a parent and the device itself is not a partition”, followed separately by “a reparent moves it with no partition check”.
Observed kernel passages:
```c
/* :2430-2433 */
static inline int device_is_not_partition(struct device *dev)
{
	return !(dev->type == &part_type);
}
/* :3508 */ if (dev->parent && device_is_not_partition(dev)) {
/* :3542 */ if (dev->parent && device_is_not_partition(dev))
```
Strongest original counterexample: a partition with a whole-disk parent. The helper rejects that device; the revised wording now rejects it too, independently of its parent's type. `S193.src:4653-4657,4705-4706` separately supports the retained reparent qualification. This is a static source comparison, not an executed kernel/device probe. Smallest safe correction: none needed for N1.

## N2 — error versus completed violation
VERDICT: holds — N2 fixed without new harm in the required invalid/good-revision probes.

The script was copied from `$T` into `$S` before execution, using `git show` piped to bounded `tee`. Copied SHA-256: `8a6f0ccfc257f759f81aefcd14cda506476c19e5655b798d4ddaca923cc9ff47`.
Executed:
```sh
timeout --signal=TERM --kill-after=2s 110s python3 -I -B "$S/check-sources-appendonly.py" refs/heads/ResNoHarmFixes-nonexistent --repo "$L"
```
```text
error: git rev-parse --verify refs/heads/ResNoHarmFixes-nonexistent^{commit} failed: fatal: Needed a single revision
exit=2
```
Executed the same command with `$T` replacing the nonexistent revision:
```text
rev=6d3d94b396698d67555a51c565eb6dc58d8cfa09 rows=204 commits=47
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] superseded=[S069,S182,S193]
exit=1
```
The latter is a completed scan finding historical violations, not an error. Adding `--round-base dd76eb79` produced the same 18-id summary, `round_changed=[]`, exit 0. The numeric `die()` at script `:31-33` replaces the former string exits for the explicit Git, malformed-row and empty-table error paths. Smallest safe correction: none for the exercised N2 failure class. Unexercised exception classes are not certified by these probes.

## N3 — waiver removed, but the new round gate has a false pass
VERDICT: fails — N3's supersession fix holds, but “fixed without new harm” fails for the newly introduced round-pass authority.

At `$T`, `corpus/QUALITY.md:799-811` explicitly preserves violations despite supersession. The good-revision output above confirms S069, S182 and S193 remain listed, with supersession only disposition metadata. To re-attack MutQ102's strongest original shape, I appended the identical source-free S205 shape to a scratch child of `$T` (no existing row edited):
```text
| S205 | | junk | C | junk | — | supersedes S041 | queued | 2026-10-23 | 365d | — |
```
Executed:
```sh
timeout --signal=TERM --kill-after=2s 110s python3 -I -B "$S/check-sources-appendonly.py" 84d34989ced500d0b0a96739435fd2052e278e13 --repo "$S/repo"
```
Observed `CHANGED id=S041 ... superseded_by=S205`, `appendonly_violations=18`, `superseded=[S041,S069,S182,S193]`, exit 1. S041 is no longer laundered. Full receipt: `$S/superseder-probe.txt:1-24`. This checker does not establish the new row's Gate validity, nor does revised 102 claim that.

**New round-mode counterexample:** scratch commit `26813ef934a28c4a0939ddc66388e3e8d23e70c8` is a direct child of `$T` and changes only S041's teaches cell back to its first-published bytes: remove `lane rule: ` after the semicolon. That is an in-place correction of a forbidden cell, not an allowed status/recheck/used-by change. QUALITY 81 (`:373-377`) grants no restoration exception; revised 102 opens with “lands no in-place change to an existing row”.
Executed:
```sh
timeout --signal=TERM --kill-after=2s 110s python3 -I -B "$S/check-sources-appendonly.py" 26813ef934a28c4a0939ddc66388e3e8d23e70c8 --repo "$S/repo" --round-base "$T"
```
```text
rev=26813ef934a28c4a0939ddc66388e3e8d23e70c8 rows=204 commits=48
appendonly_violations=17 ids=[S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] superseded=[S069,S182,S193]
round_changed=[]
exit=0
```
Evidence: `$S/restore-probe.txt:1-24`; exact one-row delta `$S/restore-delta.txt` (bounded `git diff --no-ext-diff --no-textconv "$T" 26813ef934a28c4a0939ddc66388e3e8d23e70c8 -- corpus/SOURCES.md`).
Cause: script `:88-89` records the edit, but `:98-99` excludes an id whose endpoint equals its origin; new `:119` computes `round_changed` only from that endpoint-filtered list. Precision: endpoint blindness already existed in the old checker; introducing it as an exit-0 round-pass authority and claiming no in-place edits is the new calibration/operability harm. This does not refute the observed pristine round-35 result or reinstate the removed supersession waiver.
Smallest safe correction: derive `round_changed` from **all** recorded `changes` whose commits fall in the round, not just `violations`; preserve the separate endpoint-debt list and supersession metadata. The restoration above must then print `round_changed=[S041]`, exit 1. This is a fixable detector defect, not an unavoidable axis tradeoff.

## Containment and limits
Only this report was written in the lane; scratch artifacts and Git-object writes were confined to `$S`. Clone used `--no-hardlinks --no-checkout` with GIT_DIR/GIT_WORK_TREE/GIT_INDEX_FILE unset; synthetic commits use empty address fields. A full upstream-source scratch copy was removed after reading the cited passages. Every command had a timeout of at most 120 s; all foreground commands completed, with no background job to kill. No subagents, canonical judge, agent runtime, host remediation, source fetches, builds or selftests; only the assigned checker probes ran. Host query: UTC clock. No tool installs or updates.
