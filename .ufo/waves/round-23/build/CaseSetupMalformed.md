# CaseSetupMalformed — C2 fixture case: `device_links` key missing → setup verdict

Seat: `MadoR22-2.CaseSetupMalformed-8` (wave item `CaseSetupMalformed`)
Case file: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseSetupMalformed.json`
Case `id`: `CaseSetupMalformed` — the wave item name, matching the file name, the
report trailer path `.ufo/waves/round-23/build/CaseSetupMalformed.md` and the
naming convention already used by the sibling cases proposed in this wave
(`CaseUnsupported.json`, `CaseNoCover.json`, `CaseOptionalFields.json` all carry
the item name as `id`).

Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/contract.md`
(frozen at lane commit `4dc80c1be48308075e83af17f15fbfe7e95e6cb8`), §C2.
Detection only; no production edit, no delegation, no background job, no VCS mutation.

**Independence.** I did not open any candidate implementation
(`.ufo/waves/round-23/build/ImplQuota/`, `.scratch/round23/ImplQuota`) and did not open
the oracle directory contents (`.ufo/waves/round-23/build/OracleQuota/`) beyond the
directory listing that revealed it exists. I did not read the `cases-proposed/`
sibling *fixtures* while deriving my expectation; after my case file was already
written and its expectation fixed, I read three sibling case files
(`CaseUnsupported.json`, `CaseOptionalFields.json`, `CaseNoCover.json`) and one
sibling report (`build/CaseUnsupported.md`) **only** to confirm this wave's file
naming, JSON key order and report shape conventions. No sibling expectation,
fixture content or rationale influenced this derivation; my expectation was derived
and written before those reads.

**Live host reads.** None for the derivation. The only host surface I read in this
seat was `/proc/self/mountinfo` once, before the fixture was written, as a
format-realism reference; the fixture's decorative lines were subsequently rewritten
as synthetic lines (the values that remain — `0:30`, `259:1`, `0:57`, `/dev/mapper/root`,
`dm-0`, the uuid and the xfs super-option string — come from the contract's own
frozen `frozen/c2-expected-real.json`, not from that read). No `quotactl`, `btrfs`,
`xfs_quota`, `repquota`, `mount` or other privileged/mutating command was run. No
`/tmp` was used; nothing was written outside my one assigned case file and this
report.

## 1. Scenario and derivation

**Scenario.** A synthetic `mori-quota-fixture-v1` object that carries `schema`,
`mountinfo`, `paths` and `btrfs_sysfs` but **omits the required `device_links`
top-level key**. The fixture is therefore invalid, the probe must return the setup
verdict, and no per-path verdict may be produced.

**Derivation, contract row by contract row.**

1. **Fixture key set — the case's whole point.** §C2, contract.md lines 82–93:
   *"Fixture format `mori-quota-fixture-v1` (JSON object, exact keys):"* followed by the
   literal example carrying `schema`, `mountinfo`, `paths`, `device_links`,
   `btrfs_sysfs`, and then: *"Missing/extra top-level keys, non-absolute paths,
   malformed st_dev, malformed JSON, unparseable mountinfo line → exit 2 `QUOTA_SETUP`
   (no partial verdict)."* My fixture has four of the five exact keys and omits
   `device_links`, so it falls on the **missing-top-level-key** arm of that sentence.
   This is the arm the contract names explicitly, so the expectation does not depend
   on any unstated validation rule.
2. **Verdict.** §C2, contract.md lines 132–134: *"Verdict precedence: setup error →
   2 `QUOTA_SETUP`; else any `enabled` → 1 `QUOTA_ENABLED` … else any `unknown` → 2
   `QUOTA_STATE_UNKNOWN`; else 0 `QUOTA_DISABLED`."* A setup error is the first
   branch and is evaluated **before** any per-path state, so the fixture's two paths
   (which would each classify cleanly on their own) never contribute to the verdict.
3. **No partial verdict.** The parenthetical *"(no partial verdict)"* in the
   malformed-input sentence forbids emitting per-path classification records for a
   rejected fixture. Hence `expected.paths` is the empty list, not a list holding a
   `btrfs_device_unmapped` record and an `xfs_noquota_option` record.

**Expected object.**

```
exit      = 2
finding_id = "QUOTA_SETUP"
paths     = []            (empty — no partial verdict)
```

**No classification-table row applies.** The quota classification table
(contract.md lines 108–122) is reached only after a fixture has been accepted. This
case stops at the setup gate, one layer above the table; the twelve rows are
untouched by this expectation.

## 2. Why the fixture is otherwise deliberately valid

The case isolates exactly one defect. Every other part of the fixture is a
well-formed value, so an implementation that wrongly tolerates the missing key is
*visibly* wrong rather than accidentally right:

* **mountinfo** — six lines in the exact field layout of S082 (§4): fields 1–6,
  optional `shared:N` fields, the `-` separator, then fstype / source / super
  options. Every line has 11 space-separated fields and one separator (checked
  mechanically). A btrfs root line at `/`, a btrfs subvolume line at `/home`, an xfs
  line at `/tmp` with `noquota` in its super options, plus three decorative
  `proc`/`sysfs`/`tmpfs` lines that are inert for the two queried paths.
* **paths** — two entries, each with exactly `path`, `realpath`, `st_dev` in the
  `MAJ:MIN` string form the contract's fixture example uses:
  `/home/vgpnk/Projects/shokunin` (`0:57`) and `/tmp` (`259:1`). Both are absolute
  (no `non-absolute paths` arm), and both `st_dev` values are well-formed (no
  `malformed st_dev` arm).
* **btrfs_sysfs** — one uuid whose `devices` list names `dm-0`, with `qgroups:false`
  and `qgroups_mode:null`, mirroring the btrfs qgroup sysfs interface (S079).
* **The btrfs device difference is intentional, not an error.** The `/home` mount
  reports `major:minor 0:30` while the fleet-root path's `st_dev` is `0:57`: that is
  the per-subvolume anonymous device (S081), which the contract records as
  `device_check: "btrfs_subvolume_skipped"`. So the fixture would still be coherent
  if `device_links` were present.
* **`device_links` is the only omitted key.** Everything else in the contract's exact
  key list is present with a contract-shaped value.

## 3. Discrimination: what a lenient implementation would produce

If an implementation treats the absent `device_links` key as an empty mapping
instead of rejecting the fixture:

* the btrfs mount source `/dev/mapper/root` cannot be resolved to a device name, so
  **zero** btrfs uuids list that device and the `/home` path lands on the btrfs row
  *"zero or several uuids list the device → `unknown`, `n/a`,
  `btrfs_device_unmapped`"*;
* the `/tmp` path lands on the xfs row *"`noquota` and no quota key → `disabled`,
  `n/a`, `xfs_noquota_option`"*;
* no path is `enabled`, one path is `unknown`, so the verdict becomes **exit 2
  `QUOTA_STATE_UNKNOWN`** with two per-path records.

That is a different `finding_id` **and** a different `paths` list from the expected
`QUOTA_SETUP` / `[]`. The case therefore separates "malformed fixture rejected" from
"fixture accepted and classified" on both compared fields — it is not satisfied by a
lenient default for one missing key. Note also that both outcomes carry exit code
2, so the case only discriminates if the oracle compares `finding_id` (and the
per-path list) and not the exit code alone; §C2's measured clause does require
exactly that ("matches exit, finding_id and per-path … exactly").

## 4. Source anchors

* **S082 — procfs documentation (Linux v7.2)**, `Documentation/filesystems/proc.rst`,
  §3.5 `/proc/<pid>/mountinfo - Information about mounts`, lines 1965–1993.
  Anchors used: fields 1–6 at 1973–1978, with (3) `major:minor` "value of st_dev for
  files on filesystem" at 1975 and (5) "mount point: mount point relative to the
  process's root" at 1977; "(n…m) optional fields: zero or more fields of the form
  `tag[:value]`" at 1979; "(m+1) separator: marks the end of the optional fields" at
  1980; "(m+2) filesystem type" at 1981; "(m+3) mount source" at 1982; "(m+4) super
  options: per super block options" at 1983; "Parsers should ignore all unrecognised
  optional fields" at 1985. Supports the fixture's mountinfo layout only; this
  source says nothing about quota state.
* **S078 — `fs/xfs/xfs_super.c` (v7.2)**, `xfs_fs_show_options` and the quota
  option emission (usrquota/uqnoenforce, prjquota/pqnoenforce, grpquota/gqnoenforce,
  and `noquota`). Supports the xfs super-option string used in the fixture's `/tmp`
  line.
* **S079 — `fs/btrfs/sysfs.c` (v7.2)**, `qgroup_enabled_show`, `qgroup_mode_show`,
  the `qgroups` attribute group. Supports the `btrfs_sysfs` shape
  (`devices` / `qgroups` / `qgroups_mode`) used in the fixture.
* **S081 — `fs/btrfs/inode.c` (v7.2)**, `btrfs_getattr`: the reported `st_dev` comes
  from the root's anonymous device, not the superblock device. Supports the
  intentional `0:30` (mount) vs `0:57` (path) difference, and matches the contract's
  own citation of S081 for `btrfs_subvolume_skipped`.

The case's `sources` array is exactly `["S078", "S079", "S081", "S082"]` — the four
sources actually relied on. The **expected verdict itself** rests only on the
contract's fixture-format paragraph and its verdict-precedence sentence, not on any
kernel source; the sources support the fixture's realism.

S-id mapping note (transparency, not reliance): the S077–S084 rows are drafted in
`.ufo/waves/round-23/build/DraftSourceRows/rows.md` in the order xfs.rst,
xfs_super.c, btrfs sysfs.c, btrfs qgroup.c, btrfs inode.c, proc.rst, ext4.rst,
tmpfs.rst. The contract itself names **S081** for the per-subvolume anonymous
`st_dev`, which is `fs/btrfs/inode.c` under that positional mapping — the fifth
entry, and S081 is the fifth id — so the mapping is self-consistent and proc.rst is
**S082**. My citation of S078 (xfs_super.c), S079 (btrfs sysfs.c) and S082
(proc.rst) follows that same mapping.

## 5. Contract ambiguities found (reported, not resolved by fiat)

1. **The setup-error output's own shape is unspecified.** §C2 defines one output
   object — `schema: "mori-quota-surface-v1"`, `finding_id`, `exit_code`, `paths`,
   `df_covers_quota`, `limits` — and separately says a malformed fixture gives
   "exit 2 `QUOTA_SETUP` (no partial verdict)". It never says whether the setup
   error still emits that object (same schema, `paths: []`, `exit_code: 2`,
   `df_covers_quota: false`, `limits`) or a different, setup-shaped object. The C1
   tool in the same contract explicitly makes its schema apply to "every output
   (check, setup error, selftest)"; C2 has no equivalent sentence. My case asserts
   only what the case schema fixes — `exit`, `finding_id`, `paths` — so it is
   insensitive to this, but **L1 should state explicitly whether a C2 setup error
   carries `schema: "mori-quota-surface-v1"`**. Recommend: yes, one schema for every
   output, mirroring C1's wording, so the tool has a single output contract.
2. **`paths: []` versus an absent `paths` key.** "No partial verdict" says there is
   no per-path verdict; it does not say whether the key is present-but-empty or
   absent. The case schema fixes `expected.paths` as an ordered list, so I used the
   empty list. An oracle comparing "per-path tuples" would score an absent key as
   an empty set as well, so both implementations pass; but if the oracle does a
   literal key-by-key object comparison, an implementation that omits `paths`
   entirely would fail. Recommend the contract say the setup output carries
   `paths: []`.
3. **Exit code 2 is overloaded.** `QUOTA_SETUP` and `QUOTA_STATE_UNKNOWN` both
   exit 2. Any C2 measurement that keys on exit code alone cannot distinguish a
   rejected fixture from an unclassifiable path. §C2's measured clause does require
   `finding_id` to match, so the oracle is sound — but the contract's own limits
   prose does not say that exit 2 is deliberately overloaded, and a driver written
   from the prose alone could mistake it for a single condition. Recommend one
   sentence stating that exit 2 covers two distinct findings and that
   `finding_id` is the discriminator.
4. **Is `device_links` required unconditionally?** "Exact keys" says the fixture
   must carry all five keys, so a fixture with no btrfs path would still need
   `device_links` (possibly `{}`). My case sidesteps the question by including a
   btrfs path, so the expectation holds under either reading. If L1 intends
   `device_links` to be required only when a btrfs mount is present, this case
   remains valid; if L1 intends it unconditionally, this case also remains valid.
   Flagged because a future case with an xfs-only fixture would *not* be robust to
   the two readings.
5. **No validation rule for the *value* of `device_links`.** The malformed-input list
   names "malformed `st_dev`" and "malformed JSON" but says nothing about a
   `device_links` whose value is not a string, or a `btrfs_sysfs` entry with an
   unknown key. I chose the *missing key* arm precisely because it is the one the
   contract names. Recommend the contract enumerate the value-shape rules it wants
   (or state that only the key set is validated) so a future case can test them.
6. **Key-set validation order vs. mountinfo parsing.** If a fixture is *both*
   missing a key and carries an unparseable mountinfo line, both arms give the same
   `QUOTA_SETUP`, so the ordering is unobservable in this case and no ambiguity is
   raised here. Recorded only so the oracle author does not read a missing key as
   necessarily preceding a parse error.
7. **`enforcement` spelling.** The table writes `n/a` as a literal string while the
   output schema allows `null` for `fstype`, `mount_point` and `btrfs_qgroups_mode`.
   This case does not assert `enforcement` (the paths list is empty), so it is
   insensitive — but the same cutover question raised by the sibling cases applies
   and should be pinned once, centrally.

## 6. Tooling

No tool was installed or updated for this seat: no `pacman`, `uv`, `npx`, `cargo` or
release-binary install; no channels used. Only read-only repository reads
(`contract.md`, `wave1-spec.json`, `corpus/SOURCES.md` registry shape, the wave's
`frozen/c2-expected-real.json`, the wave's draft source rows, and the sibling
convention files named in the independence note). No test, build, lint or formatter
was run, per the wave's "no tests/builds/linters/formatters/smoke runs" rule.

## 7. Result

One case file written: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-proposed/CaseSetupMalformed.json`.

Verified mechanically (JSON parse only, no tool execution):

* top-level keys exactly `schema, id, scenario, fixture, expected, rationale, sources`;
  `schema` = `mori-quota-case-v1`; `id` = `CaseSetupMalformed`; `scenario` is one line.
* fixture keys exactly `schema, mountinfo, paths, btrfs_sysfs` — `device_links`
  deliberately absent, which is the defect under test; `schema` =
  `mori-quota-fixture-v1`.
* every `paths` entry has exactly `path`, `realpath`, `st_dev`; both `path` and
  `realpath` are absolute; both `st_dev` values are `MAJ:MIN` shaped.
* every mountinfo line has 11 fields and exactly one `-` separator, in the S082 layout.
* `expected` keys exactly `exit, finding_id, paths`; `exit` = 2, `finding_id` =
  `QUOTA_SETUP`, `paths` = `[]`.
* `sources` = `["S078", "S079", "S081", "S082"]` — all within S077–S084.

Expectation derived from `contract.md` §C2 only; no implementation consulted.

---

# CORRECTION (appended) — pre-seal amendment, corrected case file

Authority: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/preseal-amendment.md`
(written before L1 opened any ImplQuota candidate or ran any C2 candidate; no C2 result
observed by this seat). Corrected case file:
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/cases-corrected/CaseSetupMalformed.json`
(same `id`: `CaseSetupMalformed`). The original proposal at
`.ufo/waves/round-23/cases-proposed/CaseSetupMalformed.json` is **retained untouched**;
the corrected file is a separate artifact and does not supersede it in place.

## C1 delta (delta report)

**One fixture-member delta, no expectation delta.**

| item | original proposal | corrected file | reason |
|---|---|---|---|
| `btrfs_sysfs[uuid]` record members | `devices`, `qgroups`, `qgroups_mode` | `devices`, `qgroups`, **`qgroups_enabled`**, `qgroups_mode` | amendment, C2 final rules: "Add required fixture member `qgroups_enabled` to each btrfs_sysfs UUID record: true/false/null", and "qgroups false must pair with enabled=null/mode=null" |
| `qgroups_enabled` value | — | `null` | `qgroups` is `false`; the amendment requires `enabled=null` when the qgroups directory is absent |
| top-level keys | `schema`, `mountinfo`, `paths`, `btrfs_sysfs` | **unchanged** | `device_links` stays absent — that absence is the defect under test |
| `mountinfo`, `paths` | — | **unchanged** | no amendment clause touches them; see §C2 below |
| `expected` | exit 2, `QUOTA_SETUP`, `paths: []` | **unchanged** | the setup gate is not superseded by the amendment |
| `sources` | S078, S079, S081, S082 | **unchanged** | same four sources relied on |

## C2 delta — which amendment clauses apply to this case, and which do not

The amendment's C2 final rules were read against this fixture clause by clause:

* **Applies — btrfs `qgroups_enabled` member.** Added as `null` above, paired with
  `qgroups: false` and `qgroups_mode: null`.
* **Applies — "Missing/extra record keys setup".** This is why the original proposal's
  record was *not* left as-is: without `qgroups_enabled` the record itself was invalid
  under the amended rules, which would have made the fixture a two-defect case and
  destroyed its ability to discriminate a lenient implementation. The corrected record
  is exact, so the **only** remaining defect is the missing top-level `device_links`.
* **Applies — "Paths nonempty, unique, normalized absolute path/realpath … st_dev
  canonical decimal MAJ:MIN".** The two paths satisfy this; the corrected fixture keeps
  them unchanged. No correction was needed.
* **Applies — "UUID keys canonical UUIDs, devices and mapped values plain nonempty
  basenames".** `1d02a454-c549-4a35-b567-89d60902af8e` is canonical; `dm-0` is a plain
  basename. No correction needed.
* **Applies — "qgroups fields have exact bool/bool-or-null/mode-or-null types".** Now
  exactly `false` / `null` / `null`.
* **Applies — "Parse separator and the last THREE fields of EACH chosen line, never
  file-wide", "ignore empty trailing lines", octal rule.** The fixture's six lines each
  carry a separator and exactly eleven fields; no line contains a backslash; the text
  ends with a single newline. No correction needed.
* **Applies — "if ANY covering mountpoint occurs more than once, refuse classification
  … `ambiguous_overmount`".** Verified: the mount points are `/proc`, `/sys`, `/run`,
  `/`, `/home`, `/tmp` — each occurring exactly once. For
  `/home/vgpnk/Projects/shokunin` the covering points are `/` and `/home`, each once;
  for `/tmp` they are `/` and `/tmp`, each once. So the amended refusal does not fire
  on either queried path and no `ambiguous_overmount` retagging applies.
* **Applies — "Btrfs skips equality only when stat major is 0".** The fleet-root path's
  `st_dev` is `0:57`, major 0, so the skip still applies and the intended
  `device_check` for that path remains `btrfs_subvolume_skipped`. No correction needed.
* **Applies — "Fixture source resolution: lookup RAW decoded source in `device_links`;
  use its mapped basename when present, otherwise basename(source)."** Used in the
  discrimination argument below; it does not change the expected verdict.
* **Does not apply — ext2/ext3/ext4 retagging to `unknown`/`n/a`/
  `ext_quota_option_unverified`.** This fixture has no ext2/ext3/ext4 mount, so there is
  no ext positive case here to retag. The expected paths list is empty in any case.
* **Does not apply — "enabled btrfs basis" renaming to `btrfs_qgroups_enabled`.** This
  fixture's only UUID record has `qgroups: false`, so no btrfs *enabled* row is reached;
  no basis token appears in the expectation. The renames
  `btrfs_qgroups_enabled` / `btrfs_qgroups_disabled` / `btrfs_qgroups_enabled_unavailable`
  therefore do not appear in this case file.
* **Does not apply — "duplicated-covering-point case becomes unknown/null fstype +
  mountpoint / `ambiguous_overmount`".** No duplicated covering mount point exists in
  this fixture (verified above); the fixture is not that case.
* **Does not apply — "For unsupported/btrfs fstype quota_option_keys=[]".** The
  expectation asserts only the six scored per-path fields and the paths list is empty,
  so no `quota_option_keys` value is asserted or changed.
* **Does not apply — the XFS precedence rewrite and the tmpfs four-key restriction.**
  The fixture's xfs line carries only `noquota` and the tmpfs line is decorative; neither
  is a queried path, and no xfs/tmpfs expectation is asserted.

## Corrected discrimination argument

Under the amended source-resolution rule, a lenient implementation that treats the
absent `device_links` key as an empty mapping looks up the raw decoded source
`/dev/mapper/root`, finds no mapped basename, and falls back to `basename(source)` =
`root`. `root` appears in no UUID's `devices` list (`["dm-0"]`), so **zero** UUIDs list
that device and the `/home` path reaches the btrfs row "zero or several uuids list the
device → `unknown`, `n/a`, `btrfs_device_unmapped`". The `/tmp` path reaches "xfs,
`noquota` and no quota key → `disabled`, `n/a`, `xfs_noquota_option`". With no `enabled`
path and one `unknown` path the verdict becomes **exit 2 `QUOTA_STATE_UNKNOWN`** with two
per-path records — a different `finding_id` and a non-empty `paths` list.

The correct behaviour is **exit 2 `QUOTA_SETUP` with `paths: []`**. The case therefore
still separates "malformed fixture rejected" from "fixture accepted and classified" on
both compared fields, and it still cannot be satisfied by a lenient default for one
missing key — now under the stricter amended rules, with the record itself exact.

Both outcomes carry exit code 2, so the case discriminates only if the oracle compares
`finding_id` and the per-path list rather than the exit code alone.

## Corrected-file mechanical verification (JSON parse only; no tool execution)

* top-level keys exactly `schema, id, scenario, fixture, expected, rationale, sources`;
  `schema` = `mori-quota-case-v1`; `id` = `CaseSetupMalformed`; `scenario` is one line.
* fixture keys exactly `schema, mountinfo, paths, btrfs_sysfs` — `device_links`
  deliberately absent (the defect under test).
* `btrfs_sysfs` has exactly one UUID record with exactly `devices`, `qgroups`,
  `qgroups_enabled`, `qgroups_mode`; values `["dm-0"]`, `false`, `null`, `null` — the
  amendment's `qgroups false ⇒ enabled=null/mode=null` pairing.
* every `paths` entry has exactly `path`, `realpath`, `st_dev`; values absolute,
  unique, dotfree; `st_dev` values `0:57` and `259:1` are canonical `MAJ:MIN`.
* every mountinfo line has 11 fields and exactly one `-` separator; the six mount points
  are all distinct (no `ambiguous_overmount` trigger); no backslash appears.
* `expected` keys exactly `exit, finding_id, paths`; `exit` = 2, `finding_id` =
  `QUOTA_SETUP`, `paths` = `[]`.
* `sources` = `["S078", "S079", "S081", "S082"]`.

## No implementation reads, no tests

This seat read no candidate implementation (`.ufo/waves/round-23/build/ImplQuota/`,
`.scratch/round23/ImplQuota`) and ran no tool, test, build, lint or formatter. The
original case file in `cases-proposed/` was not modified.
