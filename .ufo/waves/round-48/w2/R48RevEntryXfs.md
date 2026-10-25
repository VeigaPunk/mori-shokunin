# R48RevEntryXfs — XFS (S479) row re-open, round 48 wave 2

Seat: R48RevEntryXfs. Lane: mori-shokunin. Leaf seat; no subagents dispatched; nothing mutated
(read-only review; scratch at `.scratch/r48w2-R48RevEntryXfs/`).

**Attacked:** all 7 S479 rows (lines 26–32) of `corpus/knowledge/quota-observability-r48.md`
against the normalised committed copy `corpus/evidence/sources-r48/xfs_quota.8.html`
(tags → space, entities decoded, whitespace collapsed; per-seat normalisation replicated, not
the counter's).
**Verdict: BREAKS — class OVERCLAIM (minor, one row).** Six of seven rows HOLD; row X5
(`limits are never enforced on the superuser …`, line 30) carries a consequence clause
("so a root-owned workload cannot hit a quota") that is stronger than the id-scoped exemption
the quote states.

## Method

Normalised copy produced by an independent script in scratch (`xfs_norm.txt`); each quote
located by substring search (all 7 found); ±300 normalised characters printed below exactly as
observed. Judged against the six classes of `w1/CritEntryRisk.md` (P1 overclaim, P2 negation,
P3 example-generalised, P4 wrong filesystem, P5 vendor-authority, P6 number-from-example).

## Per-row findings

### X1 — line 26 — HOLDS
Claim: `On XFS, quota accounting and limit enforcement are separate states; a mount can account without enforcing.`
Quote: `XFS distinguishes between quota accounting and limit enforcement.`
Context (±300):

```
filesystems. The first time quota accounting is turned on (at mount time), XFS does an
automatic quotacheck internally; afterwards, the quota system will always be completely
consistent until quotas are manually turned off. 2. There is no need for quota file(s) in the
root of the XFS filesystem. 3. XFS distinguishes between quota accounting and limit
enforcement. Quota accounting must be turned on at the time of mounting the XFS filesystem.
However, it is possible to turn on/off limit enforcement any time quota accounting is turned
on. The "quota" option to the mount command turns on both (user) quota accounting and
enforcement. The "uqnoenforce" option mus
```

The "account without enforcing" half is not in the quote itself but in the very next sentence
of the same numbered item ("turn on/off limit enforcement any time quota accounting is turned
on"; `uqnoenforce` mounts accounting with enforcement disabled). Claim is a faithful
compression of item 3; not stronger.

### X2 — line 27 — HOLDS
Claim: `Accounting is chosen at mount time, while enforcement can be switched afterwards.`
Quote: `Quota accounting must be turned on at the time of mounting the XFS filesystem.`
Context (±300): see X1 above — the quote is the first half of the sentence pair; the second
half of the claim ("enforcement can be switched afterwards") is the immediately following
sentence ("it is possible to turn on/off limit enforcement any time quota accounting is
turned on"). Composite claim, fully scoped inside item 3, no overreach.

### X3 — line 28 — HOLDS
Claim: `XFS accounts usage for every user, including users that have no limit set, so a zero limit and a zero usage are different things.`
Quote: `XFS filesystems perform quota accounting whether the user has quota limits or not.`
Context (±300):

```
uota limits cannot be set before turning on quotas on. 8. XFS filesystems keep quota
accounting on the superuser (user ID zero), and the tool will display the superuser's usage
information. However, limits are never enforced on the superuser (nor are they enforced for
group and project ID zero). 9. XFS filesystems perform quota accounting whether the user has
quota limits or not. 10. XFS supports the notion of project quota, which can be used to
implement a form of directory tree quota (i.e. to restrict a directory tree to only being
able to use up a component of the filesystems available space; or simply to keep track of
```

The "so" clause is a plain restatement of what accounting-without-limits means (usage exists
independent of any configured limit); it adds no fact beyond the quote. Not a negation
context — "or not" here is the supported case, not a denial.

### X4 — line 29 — HOLDS
Claim: `An XFS filesystem with enforcement turned off is still a usage-accounting source.`
Quote: `XFS filesystems with limit enforcement turned off can be used as an effective disk usage accounting system`
Context (±300):

```
ta subsystem provides a mechanism to control usage of disk space. Quotas can be set for each
individual user on any/all of the local filesystems. The quota subsystem warns users when
they exceed their allotted limit, but allows some extra space for current work (hard
limit/soft limit). In addition, XFS filesystems with limit enforcement turned off can be
used as an effective disk usage accounting system. Users' View of Disk Quotas To most users,
disk quotas are either of no concern or a fact of life that cannot be avoided.
```

Direct paraphrase; the soft/hard discussion in context is separate and not leaned on by the
claim.

### X5 — line 30 — **OVERCLAIM (minor)**
Claim: `Limits are never enforced on the superuser or on group and project ID zero, so a root-owned workload cannot hit a quota.`
Quote: `limits are never enforced on the superuser (nor are they enforced for group and project ID zero)`
Context (±300):

```
hat allows quota limit information to be backed up for later restoration, should the need
arise. 7. Quota limits cannot be set before turning on quotas on. 8. XFS filesystems keep
quota accounting on the superuser (user ID zero), and the tool will display the superuser's
usage information. However, limits are never enforced on the superuser (nor are they
enforced for group and project ID zero). 9. XFS filesystems perform quota accounting
whether the user has quota limits or not. 10. XFS supports the notion of project quota,
which can be used to implement a form of directory tree quota …
```

First clause: verbatim-paraphrase, fine. The "so" clause breaks: the exemption the page states
is **per charged id** — uid 0, gid 0, project id 0 — not per workload. A root-owned workload
can still be charged to a non-zero group or a non-zero project (its files' gid/projid follow
the process egid and the directory's project id), and *those* quotas are enforced. So "a
root-owned workload cannot hit a quota" drops the id-zero scoping and reads as a workload-wide
exemption the quote does not give. Same class as CritEntryRisk P1 (claim stronger than
quote), low severity: the correct restatement is "cannot hit a uid-0/gid-0/projid-0 quota" or
"cannot hit a user quota on uid 0". Note the entry's own Boundaries section already scopes the
exemption correctly ("root and ID-zero exemption … stated for XFS"), so this is a
claim-cell wording defect, not a misunderstanding of the source.

### X6 — line 31 — HOLDS
Claim: `A user at the hard limit sees the write or create fail with the EDQUOT error.`
Quote: `If a user's usage reaches the hard limit, further requests for space (or attempts to create a file) fail with the "Quota exceeded" (EDQUOT) error.`
Context (±300):

```
that have been set by the system administrators and current usage. There are four numbers
for each limit: current usage, soft limit (quota), hard limit, and time limit. The soft
limit is the number of 1K-blocks (or files) that the user is expected to remain below. The
hard limit cannot be exceeded. If a user's usage reaches the hard limit, further requests
for space (or attempts to create a file) fail with the "Quota exceeded" (EDQUOT) error. When
a user exceeds the soft limit, the timer is enabled. Any time the quota drops below the soft
limits, the timer is disabled. If the timer pops, the particular limit that has been
exceeded is treated as if the hard limit has been reached …
```

Verbatim support; the hard/soft distinction the P1 attack exploited is preserved — the claim
is explicitly conditioned on "at the hard limit", and the following sentences confirm soft
limit goes through a timer first.

### X7 — line 32 — HOLDS
Claim: `The `quot` subcommand reads usage by scanning the whole filesystem, also with quotas off, and can be slow, so it is not a one-shot probe.`
Quote: `This command can be used even when filesystem quota are not enabled, as it is a full-filesystem scan (it may also take a long time...).`
Context (±300):

```
file . The file must be in the format produced by the dump command. quot [ -g | -p | -u ] [
-bir ] [ -acnv ] [ -f file ] Summarize filesystem ownership, by user, group or project. This
command uses a special XFS "bulkstat" interface to quickly scan an entire filesystem and
report usage information. This command can be used even when filesystem quota are not
enabled, as it is a full-filesystem scan (it may also take a long time...). The -a option
displays information on all filesystems. The -c option displays a histogram instead of a
report. The -n option displays numeric IDs rather than names.
```

Every factual clause ("whole filesystem", "with quotas off", "can be slow") is in the quote;
"not a one-shot probe" is lane guidance entailed by them, not an added fact. Watched for
context tension: the page also says bulkstat scans "quickly", but the claim's "can be slow"
rests on the quote's own hedge ("may also take a long time"), so no contradiction.

## Cross-cutting checks

- **Negation context (P2):** no S479 quote asserts a denied state; X3's "or not" is the
  supported case (accounting happens in *both* cases).
- **Example scoping (P3/P6):** no S479 quote comes from an example, manifest, or conditional
  workaround; all are normative numbered items or command descriptions.
- **Filesystem scope (P4):** every claim names XFS or the `quot` subcommand of `xfs_quota(8)`;
  no row exports XFS behavior to another filesystem.
- **Vendor authority (P5):** not applicable — man7 xfs_quota(8) is the tool's own manual.
- **Located status:** all 7 quotes substring-located in the normalised copy at offsets 8136,
  8202, 9394, 3305, 9293, 4071, 14926.

## Evidence log

- Read: `w1/CritEntryRisk.md` (six classes), `corpus/knowledge/quota-observability-r48.md`
  (S479 rows + Boundaries), committed copy `xfs_quota.8.html` (33702 bytes).
- Ran (read-only; TMPDIR not needed — no lane tool invoked; pure file reads + local
  normalisation script in `.scratch/r48w2-R48RevEntryXfs/`): Python normalise
  (strip `<…>`, `html.unescape`, whitespace collapse) then `str.find` per quote; offsets above.
- Tooling: no installs or upgrades needed (RULES.md honored; nothing to record; pacman untouched).
- UNVERIFIED: the frozen `count-c2.py` run itself (not my seat's scope to re-run the counter);
  the row judgments above are from the normalised page text only.
