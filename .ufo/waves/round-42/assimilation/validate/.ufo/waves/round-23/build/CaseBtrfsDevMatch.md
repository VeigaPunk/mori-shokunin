# CaseBtrfsDevMatch — C2 fixture case: btrfs path whose st_dev equals the mount major:minor, qgroups absent

Seat: `MadoR22-2.CaseBtrfsDevMatch-8` (fixture-case author, leaf; no delegation).
Wave: mori round 23, claim **C2 — coverage** (FR2 quota/EDQUOT observability; capability,
score held 6). Contract read in full: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md`
(frozen at lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`, confirmed by
`git rev-parse HEAD` → `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`).

## Deliverable

| Path | Role |
|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseBtrfsDevMatch.json` | the one assigned C2 fixture case (`mori-quota-case-v1`) |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/build/CaseBtrfsDevMatch.md` | this report |

`sha256(case file) = 02a4389147083d939e421300756eb1d4bdc0d927f4ade089778c3079fb2aea70` (4396 B).

Case id `CaseBtrfsDevMatch`, one scenario, one fixture, one expectation.

## Scenario in one line

A btrfs **top-level** subvolume whose path `st_dev` is **equal** to the chosen mount's
`major:minor` (so the device check lands on the `match` branch instead of the usual
`btrfs_subvolume_skipped`), with the single uuid that lists the device reporting
`qgroups: false`.

## The fixture (exact bytes as written)

`mountinfo` (4 lines, newline-terminated; layout per proc.rst §3.5, S082):

```
22 1 0:5 / /proc rw,nosuid,nodev,noexec,relatime shared:13 - proc proc rw
23 1 0:6 / /dev rw,nosuid,relatime shared:2 - devtmpfs udev rw,size=4022784k,nr_inodes=1005961,mode=755
31 1 0:26 / / rw,relatime shared:1 - btrfs /dev/mapper/root rw,space_cache,subvolid=5,subvol=/
32 31 0:26 /home /home rw,relatime shared:1 - btrfs /dev/mapper/root rw,space_cache,subvolid=257,subvol=/home
```

* `paths`: one entry — `path` = `realpath` = `/opt/mori/quota-case`, `st_dev` = `"0:26"`.
* `device_links`: `{"/dev/mapper/root": "dm-0"}` (the contract's own example mapping, verbatim).
* `btrfs_sysfs`: one uuid `8f3c1d2e-4b5a-4c6d-9e8f-0a1b2c3d4e5f` with
  `devices: ["dm-0"]`, `qgroups: false`, `qgroups_mode: null`.

## Derivation (contract + kernel sources only — no implementation was read)

### 1. Mount resolution → the chosen mount is `/` (btrfs)

* contract.md:95-99: parse fields 1-6, optional fields until `-`, then fstype, source, super
  options; candidates = mount point equals realpath **or** is `/` **or** realpath starts with
  mount point + `/`; choose the **longest** mount point.
* Candidates for `/opt/mori/quota-case`: the `/` btrfs mount (mount point is `/`) and the
  `/home` btrfs mount (rejected — the realpath does not start with `/home/`). Longest wins →
  `/`; fstype `btrfs`, source `/dev/mapper/root`, super options `rw,space_cache,subvolid=5,subvol=/`.
* The two unrelated lines (`/proc`, `/dev`) exist to make the fixture a realistic full
  mountinfo text; neither is a candidate for this path.
* Source anchor: **S082** — proc.rst §3.5 field table (`proc.rst:1973-1983`): field 3
  `major:minor` at `:1975`, separator (m+1) at `:1980`, filesystem type (m+2) at `:1981`,
  mount source (m+3) at `:1982`, super options (m+4) at `:1983`; the optional-field rule
  "parsers should ignore all unrecognised optional fields" at `:1985-1986`, which the
  `shared:13` / `shared:2` / `shared:1` optional fields exercise.

### 2. Device check → `match` (and it is deliberately *not* in the expectation)

* contract.md:100-103: `device_mismatch` basis applies **only** when the chosen fstype is
  **not** btrfs; for btrfs a mismatch is expected (per-subvolume anonymous `st_dev`, S081) and
  is recorded as `device_check: "btrfs_subvolume_skipped"`; **equal → `device_check: "match"`**.
* Here `chosen.major:minor` = `0:26` and `path.st_dev` = `0:26` → equal → `device_check`
  would be `"match"`.
* Source anchor: **S081** — `fs/btrfs/inode.c:8246`,
  `stat->dev = BTRFS_I(inode)->root->anon_dev;` (sole `stat->dev` write in the file;
  `btrfs_getattr` at `:8215-8259` is the `.getattr` of every btrfs inode-op table). It shows
  the *normal* btrfs case is a per-subvolume anonymous device, hence a mismatch — so this case
  deliberately probes the defensive **equal** branch, which S081 neither proves reachable nor
  forbids (see Ambiguity A1).

### 3. Quota classification → `disabled` / `n/a` / `btrfs_qgroups_dir_absent`

* contract.md:115-117 (table rows, btrfs): "source basename maps to exactly one uuid whose
  `qgroups` is true" → `enabled`/`unknown`/`btrfs_qgroups_dir_present`; "… exactly one uuid,
  `qgroups` false" → `disabled`/`n/a`/**`btrfs_qgroups_dir_absent`**; "zero or several uuids
  list the device" → `unknown`/`n/a`/`btrfs_device_unmapped`.
* The chosen mount's source `/dev/mapper/root` resolves through `device_links` to device
  `dm-0`; exactly **one** uuid lists `dm-0` in `devices` and its `qgroups` is `false` →
  row 2 applies: `quota_state` `disabled`, `enforcement` `n/a` (the token as spelled in the
  table), `basis` `btrfs_qgroups_dir_absent`. The `btrfs_device_unmapped` row does not apply
  (exactly one uuid, not zero or several).
* Source anchors: **S079** — `fs/btrfs/sysfs.c` `qgroup_enabled_show:2355-2368`,
  `qgroup_mode_show:2370-2395`, qgroups attribute group and path comment `:2450-2461`
  (the sysfs surface whose directory presence/absence is being observed); **S080** —
  `fs/btrfs/qgroup.c` `btrfs_sysfs_add_qgroups` call sites `:441`, `:1032`,
  `btrfs_sysfs_del_qgroups` call sites `:620`, `:689`, `:1295` — the directory is created when
  quota roots are scanned/enabled and torn down on error or teardown, so *absence does not
  prove quota was never possible*. The `disabled` reading here is a **visibility** statement
  (nothing quota-related is visible), consistent with the contract's own limits text
  ("btrfs qgroup presence ≠ any limit set").

### 4. Verdict → exit 0, `QUOTA_DISABLED`

contract.md:132-134: setup error → 2 `QUOTA_SETUP`; else any `enabled` → 1
`QUOTA_ENABLED`; else any `unknown` → 2 `QUOTA_STATE_UNKNOWN`; else 0 `QUOTA_DISABLED`.
With one path that is `disabled`, no path is `enabled` and none is `unknown` → **exit 0,
`QUOTA_DISABLED`**.

### 5. Expected-key discipline (the assignment's specific check)

`expected.paths[0]` carries **exactly** the six compared facets — `path`, `fstype`,
`mount_point`, `quota_state`, `enforcement`, `basis` — and nothing else. Verified
mechanically on the written file:

```
expected row keys: ['basis', 'enforcement', 'fstype', 'mount_point', 'path', 'quota_state']
```

This matches contract.md:124-128 (the output path object) narrowed to the sealed-case
comparison rule "per-path `(path, fstype, mount_point, quota_state, enforcement, basis)`"
(contract.md, C2 "Measured" paragraph), and the oracle's own facet list
(`build/OracleQuota.md`: the case comparison is the 6-tuple; `device_check` appears **only**
in the 7-tuple used for the frozen real control).

Therefore the three output-only tokens carry **no** requirement here:

| output token | value this fixture would produce | in `expected`? | consequence |
|---|---|---|---|
| `device_check` | `match` (btrfs, equal `st_dev`) | **no** | the case passes whichever of `match` / `btrfs_subvolume_skipped` an implementation emits for btrfs |
| `quota_option_keys` | `[]` (btrfs super options `rw,space_cache,subvolid=5,subvol=/` carry no quota key) | **no** | not constrained |
| `btrfs_qgroups_mode` | `null` (fixture `qgroups_mode: null`) | **no** | not constrained |

That is deliberate and matches the contract (the comparison facets exclude them), but it
means this case's discriminating power lies entirely in `quota_state` / `basis` /
`mount_point` / `fstype` — **not** in the device-check token (see Ambiguity A2).

## Ambiguities found in the contract (for L1)

* **A1 — the btrfs "equal → match" branch is unanchored in reality.** contract.md:103 gives
  btrfs an explicit `equal → device_check: "match"` branch, but S081 shows btrfs `st_dev` is
  the root's anonymous device, so equality with the mount's `major:minor` is not the normal
  case and no source establishes it is reachable. My case pins a *synthetic* equality to
  exercise the branch as written. It is not a claim that the host behaves this way, and the
  frozen real control (btrfs fleet root → `btrfs_subvolume_skipped`) is the real-world
  anchor. If L1 prefers, the row can stay as-is because the branch is not observable in the
  compared facets (A2).
* **A2 — `device_check` is unverified by any sealed case.** Because the sealed-case
  comparison is the 6-tuple, the only place `device_check` is asserted is the frozen real
  control (7-tuple: btrfs → `btrfs_subvolume_skipped`, xfs → `match`). A candidate that
  always emitted `match`, or always `btrfs_subvolume_skipped`, would pass every sealed case.
  This is a **coverage gap of the contract's measurement design**, not of my case; if L1
  wants it closed, the cleanest fix is to add `device_check` to the compared per-path facets
  for cases — which is a contract amendment, out of my scope here.
* **A3 — "source basename" vs the `device_links` resolution.** contract.md:115-117 says the
  btrfs rows key on "source basename maps to exactly one uuid", while the fixture format
  supplies `device_links` (source path → device name) and `btrfs_sysfs[*].devices` holds
  *device names* ("dm-0"), not source basenames ("root"). A literal reading of "basename"
  would resolve `root`, find no uuid, and produce `btrfs_device_unmapped` → exit 2
  `QUOTA_STATE_UNKNOWN`. I used the contract's own example mapping verbatim
  (`{"/dev/mapper/root": "dm-0"}` + `devices: ["dm-0"]`), i.e. the *device-resolution*
  reading, which is also the only reading consistent with the frozen real control
  (btrfs → `btrfs_qgroups_dir_absent`, not `btrfs_device_unmapped`). Suggest L1 reword the
  table condition to "the mount source resolved through `device_links` lists the device of
  exactly one uuid".
* **A4 — fstype `type[.subtype]` is unresolved.** proc.rst §3.5 documents fstype as
  `type[.subtype]` (S082, `:1981`) while the table keys on bare `xfs`/`btrfs`/`ext2|3|4`/
  `tmpfs`; the contract does not say whether a dotted type is split or falls through to
  `unsupported_fstype`. My case uses the plain `btrfs`, so it does not depend on the answer.
* **A5 — untested-by-this-case contract clauses.** Octal-escape decoding of mount points
  (contract.md:96-97; not carried by S082 — see `build/SrcProcMountinfo.md` item 5), the
  "among equal mount points the **last** line wins" tie-break (my two btrfs mounts have
  different mount points), and `no_covering_mount` are all outside this case by construction.

## Bounds and hygiene

* **Independence held.** No candidate implementation was opened:
  `.ufo/waves/round-23/build/ImplQuota/` and `.scratch/round23/ImplQuota` were never read;
  the expectation is derived from `contract.md` + the S-ids listed below only. I did not open
  the sealed-case directory contents (`.ufo/waves/round-23/cases-proposed/` was empty when I
  started; I wrote one file there and read none of the siblings'), nor the oracle source
  (only `build/OracleQuota.md`, the oracle author's report, for the case-file facet/alias
  surface — it contains no implementation and no expected values for any case).
* **No host reads, no probes.** No `/proc/self/mountinfo` read, no `os.stat` of the fleet root
  or `/tmp`, no `readlink` of `/dev/mapper/*`, no `/sys/fs/btrfs` listing, no `quotactl`,
  `btrfs`, `xfs_quota`, `repquota` or `mount` call, no process/service/session probe, no
  `/tmp` use (`TMPDIR` was pointed at `.scratch/` for the one Python self-check).
* **No VCS mutation.** Only read-only plumbing (`git rev-parse HEAD`, `git status
  --porcelain`); no `git add/commit/push`, no mutating `jj`. The lane working tree still shows
  the round-23 artifacts as untracked, exactly as at entry.
* **No delegation, no background jobs, no installs.** The only command run besides reads was
  a single Python 3.14.8 stdlib script that re-parsed **my own** fixture text to confirm
  internal consistency (key sets, mountinfo field split, candidate selection, device→uuid
  mapping, `st_dev` equality). It exercised no mori tool, no candidate probe and no test
  suite; no mori build/test/lint/formatter/smoke run was performed, per the wave bounds.
* **No writes outside my two assigned paths** (the case file and this report).

## Sources relied on

| S-id | what it carries here | anchor used |
|---|---|---|
| S079 | btrfs qgroups sysfs surface (presence/absence of `/sys/fs/btrfs/<uuid>/qgroups/`) | `fs/btrfs/sysfs.c` `qgroup_enabled_show:2355-2368`, `qgroup_mode_show:2370-2395`, qgroups attribute group `:2450-2461` |
| S080 | qgroups sysfs entries are created on quota-root scan/enable and torn down on error/teardown → absence ≠ "never possible" | `fs/btrfs/qgroup.c` `btrfs_sysfs_add_qgroups:441,1032`, `btrfs_sysfs_del_qgroups:620,689,1295` |
| S081 | btrfs `st_dev` is the root's per-subvolume anonymous device → a btrfs mismatch is expected; the equal branch is defensive | `fs/btrfs/inode.c:8215-8259`, `:8246` |
| S082 | `/proc/<pid>/mountinfo` field layout used to parse the fixture's mountinfo | proc.rst §3.5 `:1965-2002`, field table `:1973-1983` |

Contract rows cited: `contract.md:95-103` (mount resolution + device check), `contract.md:105-122`
(quota classification table, btrfs rows `:115-117`), `contract.md:124-128` (output path
object), `contract.md:132-134` (verdict precedence), `contract.md:84-93` (fixture format and
setup-error arm).

## Suggested L1 actions

1. Seal `CaseBtrfsDevMatch.json` as a **btrfs-disabled** case that is *independent of the
   device-check token*, and record explicitly that it does not discriminate
   `match` vs `btrfs_subvolume_skipped` (A2).
2. Consider closing A2 by adding `device_check` to the compared per-path facets for cases
   (contract amendment) — the only current `device_check` assertion is the frozen real
   control.
3. Reword the btrfs table condition to name the `device_links` resolution (A3) so no case
   author can derive `btrfs_device_unmapped` from a literal "source basename" reading.

---

# APPENDED CORRECTION — pre-seal amendment (2026-10-21)

Authored after L1's instruction (`preseal-amendment.md`, written before any candidate
inspection or result). The original proposal is retained untouched; the corrected case is a
**new file** in a new directory.

| item | value |
|---|---|
| corrected case | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-corrected/CaseBtrfsDevMatch.json` (6253 B) |
| `sha256` corrected case | `a74da5db52f71ec3f4a92018b2f2cd35fb43e349773e17ccce8a8235bbbd43bc` |
| `sha256` original proposal (unchanged) | `02a4389147083d939e421300756eb1d4bdc0d927f4ade089778c3079fb2aea70` |
| `sha256` this report after the append | recorded in the message to L1 (computed after the append) |
| id | `CaseBtrfsDevMatch` (same id as the original proposal, as instructed) |

## Delta — exactly one fixture field

```
btrfs_sysfs["8f3c1d2e-4b5a-4c6d-9e8f-0a1b2c3d4e5f"].qgroups_enabled = null   (added)
```

Everything else in the fixture is byte-identical to the original proposal, and the whole
`expected` object is **identical** (`expected` equality checked mechanically:
`original.expected == corrected.expected` → `True`). The `scenario` line was reworded only to
name the new member; the `rationale` was extended with the amended derivation.

Why `null` and not `false`: the amendment requires `qgroups_enabled` on **every**
`btrfs_sysfs` UUID record (true / false / null) and states "qgroups false must pair with
enabled=null/mode=null" — this record has `qgroups: false` (directory absent) and
`qgroups_mode: null`, so `qgroups_enabled` is `null`. `qgroups_enabled: false` would encode
"the qgroups directory exists but its `enabled` attribute reads 0" — a different arm, which
the amendment maps to `disabled / n/a / btrfs_qgroups_disabled`, not to
`btrfs_qgroups_dir_absent`.

The other amendment deltas named by L1 do not touch this case: there is no `qgroups: true`
record here, so no basis changes to `btrfs_qgroups_enabled`; there is no ext2/3/4 path, so
no `ext_quota_option_unverified` change; and this fixture has no duplicated covering
mountpoint, so it does not become `unknown / n/a / ambiguous_overmount` with null
fstype/mount_point. Both arms are exercised by the sibling cases that own them.

## Derivation under the amended rules (unchanged outcome)

1. **Mount resolution** — the path `/opt/mori/quota-case` has exactly one covering
   mountpoint, `/` (the `/home` btrfs mount is not a covering mountpoint for it; `/proc` and
   `/dev` are not either). No covering mountpoint occurs more than once, so the amendment's
   duplicate-cover refusal (`unknown / n/a / ambiguous_overmount`, `fstype=null`,
   `mount_point=null`, `device_check=not_checked`) does not trigger. Longest
   component-prefix selection picks `/` → fstype `btrfs`, source `/dev/mapper/root`, super
   options `rw,space_cache,subvolid=5,subvol=/`. Each line is parsed with its own separator
   and its own last three fields; no line contains a backslash, so neither octal decoding nor
   escape rejection applies; the trailing empty line after the last `\n` is ignored.
2. **Device check** — the chosen mount's `major:minor` `0:26` equals the path `st_dev`
   `0:26` → `device_check = match`. The amendment's preemption rule (a mismatch preempts the
   filesystem table) is not engaged; the btrfs equality skip ("btrfs skips equality only when
   stat major is 0") is not engaged because there is no mismatch (and the stat major is 0
   anyway).
3. **Quota classification** — raw decoded source `/dev/mapper/root` is looked up in
   `device_links` → mapped basename `dm-0`; exactly one uuid lists `dm-0` in `devices`, so
   the btrfs single-uuid rows apply and `btrfs_device_unmapped` does not. That uuid has the
   qgroups directory **absent** (`qgroups: false`) and the parent inspection succeeded (the
   uuid record exists and lists the device), so the amendment's rule "Absent dir retains
   disabled/n/a/`btrfs_qgroups_dir_absent` only on a successful parent inspection" gives
   `quota_state = disabled`, `enforcement = n/a`, `basis = btrfs_qgroups_dir_absent` —
   identical to the original proposal's row (contract.md:116).
4. **Verdict** — no path enabled, no path unknown → exit `0`, `QUOTA_DISABLED`
   (contract.md:132-134; the amendment does not change the precedence).

## Supplementary tokens (kept out of the scored six)

The amendment adds supplementary sealed checks over `device_check`, `quota_option_keys` and
`qgroups_mode` "where given". For this case they are `device_check = "match"`,
`quota_option_keys = []` (the btrfs super options carry no quota key, and the amendment
states the btrfs mechanism is sysfs, not options, so the list is empty for btrfs) and
`btrfs_qgroups_mode = null`.

They are supplied in a **separate top-level key** `supplementary_expected` (not inside
`expected.paths[0]`), because the original case instruction fixed the expected path objects
to *exactly* the six scored facets and the amendment preserves the six-field denominator
separately from the supplementary assertions. If L1's supplementary check reads those values
from the expected path row instead, the same three values belong there as extra keys on
`expected.paths[0]` — say the word and I will re-emit the file in that shape (one-line
change, expectation otherwise identical). This is the A2 gap from the original report: with
these values given, the btrfs *equal* branch of the device check becomes checkable by a
sealed case for the first time.

## New ambiguity found while applying the amendment (please action)

* **C1 — the fixture schema string was not versioned.** The amendment makes
  `qgroups_enabled` a **required** member of every `btrfs_sysfs` UUID record while the
  fixture still declares `"schema": "mori-quota-fixture-v1"`, and the amendment also keeps
  the rule "Missing/extra record keys setup". A conformant tool that validates the *original*
  v1 record key set `{devices, qgroups, qgroups_mode}` will treat this corrected fixture as a
  setup error (exit 2 `QUOTA_SETUP`) and the case will fail for the wrong reason. The
  amendment's "extra record keys" rule must therefore be read against the amended key set
  `{devices, qgroups, qgroups_enabled, qgroups_mode}`. Recommendation to L1: state the
  amended record key set explicitly in the contract (or version the fixture schema string,
  e.g. `mori-quota-fixture-v2`), otherwise every corrected case carries this trap.
* **C2 — the "parent sysfs permission/listing error" arm is inexpressible in the fixture
  format.** The amendment distinguishes "absent directory" (→ `btrfs_qgroups_dir_absent`)
  from "parent sysfs permission/listing error" (→ unknown, never absent/disabled), but
  `mori-quota-fixture-v1` has no member to express a failed parent inspection: the uuid
  record's presence *is* the successful listing. A zero-UUID match is already spoken for by
  `btrfs_device_unmapped`. Suggest L1 add an explicit member (e.g. a per-uuid inspection
  status) or accept that this arm can only be exercised in real mode.
* **C3 — A3 is now closed by the amendment.** The amended source-resolution rule ("lookup
  RAW decoded source in `device_links`; use its mapped basename when present, otherwise
  basename(source)") resolves the "source basename" wording in favour of the mapping
  reading, which is the one my case already used. No change to my fixture was needed; the
  original A3 note stands as history.

## Hygiene of this correction

Same bounds as the original seat turn: no implementation read (`build/ImplQuota/`,
`.scratch/round23/ImplQuota` — neither was opened), no oracle source read, no host probe, no
privileged or mutating command, no `/tmp` use (`TMPDIR` pointed at `.scratch/`), no VCS
mutation (read-only `git rev-parse` / `git status`), no delegation, no installs, no mori
test/build/lint/smoke run — only one Python stdlib self-check over **my own** two case files
(JSON shape, key sets, type rules, per-line separator split, covering-mountpoint set, device
resolution, and the mechanical original-vs-corrected fixture diff that produced the
one-field delta above).
