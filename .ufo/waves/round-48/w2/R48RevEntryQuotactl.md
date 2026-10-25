# R48RevEntryQuotactl — quotactl (S480) row review of `quota-observability-r48.md`

Seat: R48RevEntryQuotactl. Lane: mori-shokunin. Leaf seat, no subagents dispatched.
Attacked: the four claim rows citing S480 in `corpus/knowledge/quota-observability-r48.md`
(entry lines 33–36) against the committed copy
`corpus/evidence/sources-r48/quotactl.2.html` (man-pages 6.19, 2026-06-05), at landed tip
`e4dfff32d4f97c7ef250e9a7538fa75d4f284492`, including the directed check on the `ESRCH` row.
Review method: same as an XFS row review — quote located in the normalised copy, then the
claim judged against the page text around it (`w1/CritEntryRisk.md` checklist).

**Verdict: all four rows HOLD. No defect found in scope.** The `ESRCH` row's claim is what
the page says and no more, as analysed below.

## 0. Ground truth established first

- Working tree == tip: `git log -1 --format=%H` → `e4dfff32d4f97c7ef250e9a7538fa75d4f284492`;
  `git diff e4dfff32… -- corpus/knowledge/quota-observability-r48.md corpus/evidence/sources-r48/quotactl.2.html`
  → empty (exit 0).
- Frozen counter, read-only, `TMPDIR=<lane>/.scratch/r48w2-R48RevEntryQuotactl`:
  `python3 .ufo/waves/round-48/count-c2.py e4dfff32d4f97c7ef250e9a7538fa75d4f284492`
  → `C2=met claims=15 located=15 quote_missing=0 bad_rows=0 sources=4 source_rows=ok
  pins=ok provenance=ok rev=e4dfff32…`, rc=0. All four S480 quotes are therefore located;
  the seat's job is the entailment check the counter does not do.
- Independent re-derivation of `normalise` (strip `<…>`→space, `html.unescape`, collapse
  whitespace) on the committed copy located all four quotes at normalised offsets
  916, 1316, 3524, 4696 — consistent with `w1/CritEntryRisk.md` §2 (ESRCH at 3524).

## 1. Row: "Quota limits are per user, per group and per project on one filesystem." (S480)

Entry line 33; quote `can be used to set per-user, per-group, and per- project limits on the
amount of disk space used on a filesystem`.

Page text (HTML lines 90–97, DESCRIPTION; ±300 chars of context):

> "SYNOPSIS … The quota system can be used to set per-user, per-group, and per-
> project limits on the amount of disk space used on a filesystem. For each user
> and/or group, a soft limit and a hard limit can be set for each filesystem. The
> hard limit can't be exceeded. The soft limit can be exceeded, but warnings will
> ensue. Moreover, the user can't exceed the soft limit for more than grace period
> duration (one week by default) at a time; after this, the soft limit counts as a
> hard limit."

- Quote location is honest: `per- project` is the normalisation of the source's line break
  `per-\nproject` (HTML lines 90–91), not an altered text.
- Claim matches: the page literally says the quota system sets **per-user, per-group, and
  per-project** limits; the same paragraph scopes limits **per filesystem** ("a soft limit
  and a hard limit can be set for each filesystem"), which is the claim's "on one
  filesystem". Project quotas are corroborated by the same page's `PRJQUOTA` type
  (HTML lines 108–109) and the `Q_X…`/`XQM_PRJQUOTA` names (lines 147, 185–188).
- No strengthening, no negation slip, no scope leak. **HOLDS.**

## 2. Row: "After the grace period a soft limit is treated as a hard limit." (S480)

Entry line 34; quote `at a time; after this, the soft limit counts as a hard limit`.

Page text (HTML lines 93–97, DESCRIPTION; the ±300-char context is the same block above):

> "… the user can't exceed the soft limit for more than grace period duration
> (one week by default) at a time; after this, the soft limit counts as a hard
> limit."

- The quote is the tail of a conditional sentence: exceeding the soft limit beyond the
  grace period is what converts soft → hard. The claim's "after the grace period" is a
  fair compression of "can't exceed … for more than grace period duration …; after this,
  the soft limit counts as a hard limit" — it keeps the condition (the grace period
  elapsing) and does not add the P1-class error from `w1/CritEntryRisk.md` (it does not
  claim immediate write failure at soft-limit crossing; that would belong to the hard
  limit, which this row does not conflate).
- The "(one week by default)" detail is dropped, but the claim makes no duration
  statement, so nothing is lost or invented. **HOLDS.**

## 3. Row: "`ESRCH` from the quota syscall means quotas are not turned on, which is not the same observation as a usage of zero." (S480)

Entry line 35; quote `No disk quota is found for the indicated user. Quotas have not been
turned on for this filesystem.`

Page text (HTML lines 164–172, ERRORS; ±300 chars of context):

> "ENOTBLK — special is not a block device. EPERM — The caller lacked the required
> privilege (CAP_SYS_ADMIN) for the specified operation. ESRCH — No disk quota is
> found for the indicated user. Quotas have not been turned on for this
> filesystem. NOTES top …"

Directed check — "is the claim what the page says and no more?":

1. "means quotas are not turned on": directly stated — "Quotas have not been turned on
   for this filesystem." The first sentence of the gloss ("No disk quota is found for the
   indicated user") is a *broader* condition, but it is still a no-quota-record
   observation, never a usage value; the claim does not narrow the gloss into anything
   the page contradicts (e.g. it does not assert ESRCH is *only* ever "turned off", and
   even if read that way the page itself writes both sentences as the ESRCH description).
2. "not the same observation as a usage of zero": the page's gloss contains no usage
   quantity at all — ESRCH is listed among *errors* (EFAULT, EINVAL, ENOENT, ENOSYS,
   ENOTBLK, EPERM, ESRCH), not as a usage result. So distinguishing ESRCH from
   "usage = 0" contradicts nothing on the page and asserts nothing beyond it; it is the
   minimal observability reading of "no disk quota is found" (absent record ≠ zero
   record). It also matches the review-corrected usage in `w1/CritEntryRisk.md` P2, where
   this exact quote is described as distinguishing "no quota" from "zero usage", and the
   entry's own probe-shape section uses it the same way ("treat ESRCH as not turned on,
   never as zero", entry line 77).
3. The claim does not add anything extraneous: no claim about *which* subop raises ESRCH,
   no claim that ESRCH means enforcement is off, no recovery advice. **HOLDS** — what the
   page says, and no more.

## 4. Row: "`quotactl_fd()` addresses the filesystem by mount point, so it works where no block device exists." (S480)

Entry line 36; quote `quotactl_fd () instead works on the mount point, which avoids this
limitation and is simpler to use`.

Page text (HTML lines 190–200, NOTES "quotactl() versus quotactl_fd()"; ±300 chars of
context):

> "… The original quotactl() variant of this system call requires specifying the
> block device containing the filesystem to operate on. This makes it impossible
> to use in cases where the filesystem has no backing block device (e.g., tmpfs).
> Even when the block device does exist, it might be difficult to locate (requires
> scanning /proc/self/mounts and even some filesystem-specific parsing in the case
> of, for example, bcachefs). quotactl_fd() instead works on the mount point,
> which avoids this limitation and is simpler to use (since the filesystem to
> manipulate is typically specified by its mount point anyway)."

- Quote location is honest: `quotactl_fd ()` is the normalisation of
  `<b>quotactl_fd</b>()` (bold tag inside the parentheses).
- "addresses the filesystem by mount point": stated — "works on the mount point … since
  the filesystem to manipulate is typically specified by its mount point anyway".
  Strictly, `fd` may refer to any file or directory on the filesystem (HTML lines
  115–117), but the page itself summarises the mechanism as "works on the mount point",
  so the claim repeats the page's own characterisation.
- "works where no block device exists": stated — the block-device requirement "makes it
  impossible to use in cases where the filesystem has no backing block device (e.g.,
  tmpfs)", and the mount-point addressing "avoids this limitation".
- No scope leak to other filesystems' quota tools; the claim is about the syscall
  interface only. **HOLDS.**

## 5. Findings by severity

- Critical / major / minor: none in scope.
- Observation (not a defect): for the ESRCH row, the claim's first half ("quotas are not
  turned on") states one of the page's two glossed conditions for ESRCH; the page's other
  condition ("no disk quota … for the indicated user" — an absent per-id record) is the
  broader first sentence. A probe author treating ESRCH as strictly "quotas off" would
  under-cover the "quotas on but no record for this id" case. The claim is still safe for
  its stated purpose — ESRCH is never a usage reading — and the entry's Boundaries section
  does not overextend it, so this is a completeness note, not a falsity.

## 6. Residual risk / gaps

- Judged against the committed copy dated 2026-10-25 (man-pages 6.19); the live page can
  drift — named limit, recheck rows 9 in the entry cover it.
- Context examined is the whole committed copy (17,114 B, read in full); no other section
  of the page contradicts any of the four claims.
- Only S480 rows were in scope; S479/S481/S482 rows and non-table prose are other seats'
  assignments. UNVERIFIED by this seat: nothing inside the four-row scope.

## 7. Evidence log

- Read: `corpus/knowledge/quota-observability-r48.md` (all),
  `corpus/evidence/sources-r48/quotactl.2.html` (all 351 lines), `count-c2.py`
  (normalise + evaluate), `corpus/lessons/round-48.md`, `w1/CritEntryRisk.md`.
- Ran (read-only; `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48RevEntryQuotactl`):
  - `count-c2.py e4dfff32d4f97c7ef250e9a7538fa75d4f284492` → `C2=met claims=15 located=15 …`, rc=0.
  - `git diff e4dfff32… -- <entry> <copy>` → empty, rc=0; `git log -1 --format=%H` → tip.
  - normalise+`str.find` probe → the four quotes at offsets 916, 1316, 3524, 4696 with the
    contexts quoted in §1–§4.
- No mutating git/jj operations; no tracked file edited; report file only. Tooling: no
  installs needed (pacman paused per operator note; nothing required).

Report: .ufo/waves/round-48/w2/R48RevEntryQuotactl.md
