# CriticContractC2 — attack on contract.md §C2 (round 23, wave 1)

Seat: `MadoR22-2.CriticContractC2-8` (read-only critic). Contract read in full at lane
commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8` (`git rev-parse HEAD` and
`git log -1 -- .ufo/waves/round-23/contract.md` both return it). Also read:
`frozen/c2-expected-real.json`, `wave1-spec.json` item list, and the five files present in
`cases-proposed/` (to measure fix impact only). No implementation read (none existed in
`build/` at read time). No live host reads, no tool runs beyond pure-string `python3 -c`
checks (`str.split` / `posixpath.normpath`). No installs.

Kernel-behaviour statements below are from my knowledge of the v6.x–v7.x sources named
as S077–S084; I did not fetch them this seat. Each is tagged `[INFERENCE]` and routed to
the seat that does fetch (RevengeStDev, RevengeTmpfsQuota, RevengeXfsHistory, source
re-openers). Where the claim is decisive, the counterexample still stands on the
contract's own text.

## Axes

- **A1 calibration** — every `enabled`/`disabled` is visibly true; no false green.
- **A2 determinism** — a blind implementation and a blind oracle derive the same output
  from the contract alone (no implementer-chosen behaviour).
- **A3 coverage** — the rule set handles kernel-producible mountinfo.
- **A4 minimization** — no target data echoed beyond the declared fields.
- **A5 safety** — read-only, no side effects.

## Summary

| id | defect | class | axes |
|---|---|---|---|
| D1 | equal-mount-point tie by "last line" is order-dependent; stacking truth is the parent ID | **fix before seal** | A1 A2 A3 |
| D2 | longest prefix selects mounts hidden under an overmount; btrfs st_dev skip turns it into a false green | **fix before seal** | A1 A3 |
| D3 | field splitting unspecified; empty mount source collapses under `split()` | **fix before seal** | A2 A3 |
| D4 | escape-decoding scope and invalid escapes unspecified | **fix before seal** | A2 |
| D5 | empty `paths` gives a vacuous exit 0 `QUOTA_DISABLED`; duplicates undefined | **fix before seal** | A1 A2 |
| D6 | an ext2/3/4 quota mount option is not evidence that quota is enabled | **fix before seal** | A1 |
| D7 | `device_check`, `quota_option_keys` and "quota-related key" vocabulary incomplete | **fix before seal** | A2 A4 |
| D8 | fixture semantics gaps (source missing from `device_links`, contradictory qgroups, mode newline, unnormalized realpath, st_dev grammar) | **fix before seal** | A2 |
| D9 | setup/selftest output shape undefined; setup errors could echo mountinfo text | **fix before seal** | A2 A4 |
| D10 | real-mode stat/realpath failure undefined | **fix before seal** | A2 |
| D11 | btrfs skip accepts any st_dev, even block-device majors | recommended pre-seal hardening (cheap, harms no axis) | A1 |
| L1–L8 | limits to disclose | disclose | — |

Checked and found sound: the candidate rule `mount point == realpath ∨ mount point == "/" ∨
realpath startswith mount point + "/"` handles `/` correctly (the explicit `/` clause
covers the `"//"` prefix problem) and never matches a sibling such as `/home2` for
`/home`. The verdict ladder is total once D5 is fixed.

---

## D1 — overmount tie by "last line" (fix before seal)

**Rule attacked:** "among equal mount points the **last** line wins."

**Why unsound:** mountinfo line order is iteration order of the namespace's mount set,
not stack order. Since v6.8 the namespace is an rbtree ordered by unique mount ID
`[INFERENCE]`. A `mount --move` of an older mount onto a busy mount point puts the
lower-ID mount on top, so it prints **first**. Propagation "tucking" (v4.11+) inserts a
new mount **under** an existing one `[INFERENCE]`. The stacking truth is printed in the
line itself: a mount stacked on mount point M has field 2 (parent ID) equal to the mount
it covers, and both print mount point M.

**Counterexample fixture (false green):**

```json
{"schema":"mori-quota-fixture-v1",
 "mountinfo":"1 0 259:2 / / rw,relatime shared:1 - ext4 /dev/nvme0n1p2 rw\n50 60 0:45 / /srv rw,relatime shared:20 - tmpfs tmpfs rw,usrquota\n60 1 0:30 /@srv /srv rw,relatime shared:21 - btrfs /dev/mapper/root rw,subvolid=300,subvol=/@srv\n",
 "paths":[{"path":"/srv/data","realpath":"/srv/data","st_dev":"0:45"}],
 "device_links":{"/dev/mapper/root":"dm-0"},
 "btrfs_sysfs":{"1d02a454-c549-4a35-b567-89d60902af8e":{"devices":["dm-0"],"qgroups":false,"qgroups_mode":null}}}
```

Mount 50 (tmpfs, quota active) has parent 60, so it sits on top of the btrfs mount at
`/srv`. The path's st_dev 0:45 is the tmpfs. The contract picks the last line (btrfs).
The btrfs device check is then skipped and the result is `disabled
btrfs_qgroups_dir_absent`, exit 0 `QUOTA_DISABLED`. The correct reading is `enabled
enforced tmpfs_quota_option`, exit 1. If the lower mount were xfs or ext4, the result
would instead be `unknown device_mismatch`, exit 2: still wrong, and it hides positive
evidence, which is the very thing the verdict ladder promises never to do.

**Pre-registration fix (replaces the tie sentence; D2 below uses the same rule):**

> Let `chain(m)` be m, its parent, the parent's parent, …, stopping at a parent ID that
> is absent from the table (a parent-ID cycle → `QUOTA_SETUP`). Mount n *covers* mount a
> when `n.parent_id == a.mount_id` and `n.mount_point == a.mount_point`. Candidate m is
> *blocked* if some `a ∈ chain(m)` is covered by an n that is not in `chain(m)`. Choose
> the longest mount point among unblocked candidates. If two or more unblocked candidates
> share that mount point → `unknown`, basis `ambiguous_overmount`. Line order is never
> used.

Lenient by design: parent IDs that are absent, or that point at an unrelated mount, are
not errors. That keeps the existing proposed cases valid. `CaseXfsDevMismatch.json` has
`/home` with parent 25 (`/proc`) and three dangling parents; its outcome is unchanged
under this rule. Add `ambiguous_overmount` to the basis vocabulary. One sealed case per
counterexample (D1, D2) is required, otherwise the rule goes unmeasured.

## D2 — longest prefix selects a hidden nested mount (fix before seal)

**Rule attacked:** "Choose the longest mount point", with no visibility test, plus the
btrfs `device_check` skip.

**Counterexample fixture (false green):**

```json
{"schema":"mori-quota-fixture-v1",
 "mountinfo":"1 0 0:30 /@ / rw,relatime shared:1 - btrfs /dev/mapper/root rw,subvolid=256,subvol=/@\n65 1 0:30 /@home /home rw,relatime shared:2 - btrfs /dev/mapper/root rw,subvolid=257,subvol=/@home\n70 65 0:31 / /home/scratch rw,relatime shared:3 - btrfs /dev/sdb rw,subvolid=5,subvol=/\n80 65 0:46 / /home rw,relatime shared:4 - tmpfs tmpfs rw,usrquota\n",
 "paths":[{"path":"/home/scratch/x","realpath":"/home/scratch/x","st_dev":"0:46"}],
 "device_links":{"/dev/mapper/root":"dm-0","/dev/sdb":"sdb"},
 "btrfs_sysfs":{"1d02a454-c549-4a35-b567-89d60902af8e":{"devices":["dm-0"],"qgroups":false,"qgroups_mode":null},
                "0f7c2a6e-3b1d-4c55-9e8a-2d4b6c8e1f00":{"devices":["sdb"],"qgroups":false,"qgroups_mode":null}}}
```

Mount 80 covers `/home` (parent 65, same mount point). Mount 70 hangs off 65, so it is
unreachable, and `/home/scratch/x` actually lives on the tmpfs (st_dev 0:46). The
contract chooses 70 (the longest prefix), skips the btrfs device check, and reports
`disabled`, exit 0. The correct result is `enabled`, exit 1. With an xfs mount at 70 it
degrades to `unknown device_mismatch` (exit 2) and again hides positive evidence. This
exact pattern is what the critic brief means by "overmounts hiding nested mounts". The
D1 blocked-chain rule fixes it: 70 is blocked because 65 ∈ chain(70) is covered by 80 ∉
chain(70).

## D3 — field splitting (fix before seal)

"fields 1–6, optional fields until `-`, then fstype, source, super options" does not say
how fields are separated. The kernel prints the source as-is (it may be an empty string
or `none`). Pure-string check here:
`'100 1 0:50 / /x rw,relatime shared:1 - tmpfs  rw,size=1024k'.split()` yields only two
post-separator fields, while `.split(' ')` yields `['tmpfs', '', 'rw,size=1024k']`.
One implementation reports `QUOTA_SETUP`; another treats `rw,size=1024k` as the source and
finds no super options.

**Fix:** "Split each line on single U+0020 characters. Fields 1–6 are positional (a root
or mount point can never be `-` because escaped spaces cannot split it). The first
standalone `-` at index ≥ 6 ends the optional fields. Exactly three fields must follow,
and the source may be empty. Any other count → `QUOTA_SETUP`. Field 3 must match
`^\d+:\d+$`." Add a sealed empty-source case.

## D4 — escape decoding (fix before seal)

The contract decodes `\040 \011 \012 \134` "in the mount point" only, which leaves three
things undecided:

- **Other fields.** The source is also kernel-escaped, and its realpath is a real-mode
  input; root (field 4) is escaped too.
- **Option values.** These are escaped by `seq_show_option` with set `,= \t\n\\`
  `[INFERENCE]`.
- **Invalid escapes.** Behaviour on `\101` or a trailing `\` is not defined. Counterexample
  mount point `/srv/a\101`: implementation A decodes it to `/srv/aA`, implementation B
  keeps it literally, and the oracle and the implementation diverge.

**Fix:** "Decode exactly the four escapes in fields 4, 5 and 10. Any other backslash
sequence in those fields → `QUOTA_SETUP` `mountinfo_parse`. Super options are never
decoded: split the raw text on `,`, and the key is the raw text before the first `=`."

## D5 — vacuous green on empty paths (fix before seal)

The fixture `"paths":[]` passes every listed setup check and falls through to "else 0
`QUOTA_DISABLED`", which is a green verdict with zero evidence. Duplicate paths (fixture
entries or repeated `--path`) are also undefined.

**Fix:** "`paths` must be non-empty, else `QUOTA_SETUP`. Output order equals input order.
Duplicates are reported once per occurrence" (or rejected; either way, state it).

## D6 — ext quota option ≠ enabled (fix before seal; calibration)

**Rule attacked:** "ext2/ext3/ext4 | any of quota,usrquota,grpquota,prjquota,usrjquota,
grpjquota | enabled | unknown | `ext_quota_option`".

**Evidence:** `Documentation/admin-guide/ext4.rst` (in the S077–S084 set) describes
`quota/noquota/grpquota/usrquota` as "ignored by the filesystem … used only by quota tools
to recognize volumes where quota should be turned on" `[INFERENCE: quoted from memory —
the ext4.rst source re-opener must confirm the exact text]`. Without the `quota`
superblock feature, accounting starts only through a quotaon `quotactl`, including for
journaled `usrjquota=` files. With the feature, quota is on at mount even when no option
is printed `[INFERENCE]`.

**Counterexample:** a fresh ext4 volume mounted
`… - ext4 /dev/sdc1 rw,relatime,usrquota`, on which quotaon has never run, gets
`QUOTA_ENABLED` ("visibly enabled"). No quota is active. This is false provenance on the
claim's own headline axis.

**Fix:** "ext with any listed key → `unknown`, enforcement `n/a`, basis
`ext_quota_option_activation_unobservable`. ext with none →
`ext_quota_superblock_unobservable` (unchanged)." Both ext rows then exit 2.
Consequence: CaseExt4Usrquota and CaseExt4Journaled expectations must be re-authored
before sealing. tmpfs and xfs are unaffected, because their options are printed from
in-kernel active state.

## D7 — incomplete vocabularies (fix before seal)

- **`device_check`.** Only `match` and `btrfs_subvolume_skipped` are defined. The value
  for a non-btrfs mismatch, for `no_covering_mount`, and for `ambiguous_overmount` is
  undefined. **Fix:** `match | btrfs_subvolume_skipped | mismatch | null` (null means no
  single chosen mount). Order: the device check runs before classification, so
  `device_mismatch` wins over `unsupported_fstype`.
- **`quota_option_keys`.** Undefined for `unknown device_mismatch`, `unsupported_fstype`
  and btrfs. **Fix:** "[] unless the classification row for the chosen fstype was
  evaluated; the device-mismatch, no-mount and unsupported results always give []." This
  avoids reporting the option keys of a mount the path is not on.
- **Quota-related keys.** The set is undefined (is `noquota` included? `jqfmt`? keys on
  unsupported fstypes?). **Fix:** per fstype, the set is exactly the keys named in that
  fstype's table rows. xfs: the 7 quota keys, the 4 `*noenforce` keys and `noquota`.
  ext: the 6 keys. tmpfs: `quota,usrquota,grpquota` plus `*_hardlimit` keys. Output is
  sorted and de-duplicated; `jqfmt` is excluded.
- **xfs mixed enforcement** (`prjquota,gqnoenforce`) currently resolves to `enforced` by
  row order. State it outright: `enforced` = at least one quota type enforced.

## D8 — fixture semantics gaps (fix before seal)

Each of these lets the blind implementation and the oracle diverge:

1. **Source absent from `device_links`.** Undefined. Fix: the basename of the decoded
   source text itself (mirrors the real-mode `realpath` of a non-symlink). A non-absolute
   or empty source → `btrfs_device_unmapped`. In real mode, never call `realpath` on a
   non-absolute source: `realpath("tmpfs")` reads the CWD. Resolve sources only for
   btrfs.
2. **`qgroups: false` with non-null `qgroups_mode`.** Contradictory. Fix:
   `QUOTA_SETUP fixture_schema`.
3. **Mode text.** sysfs prints `qgroup\n` / `squota\n` `[INFERENCE]`. Fix: strip one
   trailing `\n`; allowed values are `qgroup | squota`. Anything else is still `enabled`,
   but `btrfs_qgroups_mode` becomes null (never echo unknown text).
4. **`realpath` normalization.** Not required. `posixpath.normpath('//tmp')` stays
   `'//tmp'`, and `/home/` fails the "equals" test against `/home`. Fix: a fixture
   `realpath` must equal its own `posixpath.normpath` with any leading `//` collapsed,
   and contain no `.`/`..` components, else `QUOTA_SETUP`.
5. **st_dev grammar.** Fix: `^(0|[1-9]\d*):(0|[1-9]\d*)$`, compared as integers.
6. **`btrfs_sysfs` keys and `device_links` values.** Fix: keys must match the canonical
   UUID pattern; values must be bare basenames (no `/`).

## D9 — setup/selftest output and leakage (fix before seal)

"Missing/extra top-level keys … unparseable mountinfo line → exit 2 `QUOTA_SETUP`" does
not define the JSON shape. An implementation that reports `error: "bad line: <line>"`
echoes mount sources and every option, which violates "Never echo mount sources, other
options". The `--selftest` output is not specified at all, though C1 states it explicitly
for its own tool.

**Fix:** setup output is
`{schema, finding_id:"QUOTA_SETUP", exit_code:2, error:<token>, paths:[], df_covers_quota:false, limits}`,
with `error` drawn from the fixed set `bad_argument | fixture_schema | mountinfo_parse |
path_unstatable | internal`. Never include input text or line numbers beyond an integer
index. Selftest output: `{schema, finding_id:"QUOTA_SELFTEST_PASS"|"QUOTA_SELFTEST_FAIL",
exit_code, arms:[{id, ok}]}`, exit 0/1, and 2 on harness error.

## D10 — real-mode stat failure (fix before seal)

`os.stat` raising ENOENT/EACCES/ELOOP is undefined. `os.path.realpath` succeeds lexically
on missing paths, so an implementation may emit a verdict without any st_dev. **Fix:**
"any `os.stat` error → `QUOTA_SETUP` `path_unstatable` (no partial verdict)". Fixtures
cannot express this, so it needs a selftest arm.

## D11 — btrfs skip accepts any st_dev (recommended pre-seal hardening)

btrfs `s_dev` and every subvolume st_dev are anonymous devices with major 0
`[INFERENCE: get_anon_bdev; RevengeStDev to confirm]`. Today, a path whose st_dev is
`259:1` (a block-device major) resolved to a btrfs mount is accepted silently. **Fix:**
"btrfs with unequal st_dev → `btrfs_subvolume_skipped` only if the st_dev major is 0,
else `unknown device_mismatch`." This closes the block-backed variants of D1 and D2 even
before the parent-chain rule. It cannot catch a tmpfs overmount (also major 0), so D1
and D2 remain required. The real control is unaffected: st_dev is 0:57.

---

## Limits to disclose (not seal blockers; add to output `limits` and docs)

- **L1** — btrfs-on-btrfs misresolution with both st_dev majors 0 is undetectable from
  the permitted inputs (no `statfs` f_fsid). D1 and D2 remove the known structural
  causes, but not this residue.
- **L2** — races. Remount/enable/disable races are already listed. Also: path
  rename/symlink swap between `realpath` and `stat`; and automount. `realpath` lstat-walks
  intermediate components, so a `--path` under a systemd automount point triggers the
  mount `[INFERENCE]`. Pre-register the read order: realpath, then stat, then mountinfo,
  so a triggered automount is at least visible. The probe can therefore cause an
  automount (an A5 side effect); it never issues one itself.
- **L3** — xfs `enforced` is aggregated over quota types (D7).
- **L4** — tmpfs `enforced` can overstate enforcement: limit enforcement can be toggled
  off by quotactl while usage stays active and `usrquota` is still printed, and default
  limits of 0 mean unlimited `[INFERENCE; RevengeTmpfsQuota]`.
- **L5** — exit 2 is shared by `QUOTA_SETUP` and `QUOTA_STATE_UNKNOWN`. This matches the
  lane convention (the journal-window probe uses rc2 for both UNAVAILABLE and SETUP,
  `SKILL.md` gates table), so consumers must read `finding_id`. The enabled-over-unknown
  precedence hides a sibling's unknown at the exit level; it stays visible per path.
- **L6** — `mount_point` reveals the covering prefix of the *realpath*, which can differ
  from the given path. Mount points whose dentry was unlinked print a ` (deleted)`
  suffix `[INFERENCE]` and will not prefix-match.
- **L7** — one unparseable unrelated mountinfo line aborts the whole real-mode run. This
  is availability given up for "no partial verdict".
- **L8** — overlay, fuse, zfs, bcachefs, f2fs, gfs2 and ocfs2 are all
  `unsupported_fstype`, even when they print quota keys.

## Impact on proposed cases (read only to size the fixes)

The five present files (`CaseBtrfsSquota`, `CaseBtrfsUnmapped`, `CaseUnsupported`,
`CaseXfsDevMismatch`, `CaseXfsMixedEnforce`) have no duplicate mount points and no empty
fields. Their expected outcomes are unchanged by D1, D2, D3 and D11 under the lenient
parent rule. D6 invalidates the two ext "option present" cases (not yet present at read
time). D1, D2, D3 and D5 each need one new sealed case. FixtureLint should enforce the
D3, D4 and D8 grammar.

## Checks for L1 after integration

- Fixture-mode runs of the two D1 and D2 fixtures above. Expected under the fix:
  exit 1 `QUOTA_ENABLED`, tmpfs `/srv` and `/home`.
- An empty-source line.
- `paths: []` gives `QUOTA_SETUP`.
- `\101` in a mount point gives `QUOTA_SETUP`.
- An ext4 `usrquota` line gives `unknown`.
- A setup-error stdout must contain no input substring.

Tool installs: none.
