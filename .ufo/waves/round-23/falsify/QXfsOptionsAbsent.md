# QXfsOptionsAbsent — round-23 C2 falsification of `CaseXfsOptionsAbsent.json`

**Verdict: MATCH (case not falsified).** The sealed case's expectation — exit `2`,
`finding_id` `QUOTA_STATE_UNKNOWN`, and the ordered six-field tuple
`(/srv/data, xfs, /srv/data, unknown, n/a, xfs_quota_options_absent)` — is reproduced
exactly, byte for byte, by the pinned production tool under the required bounded
invocation. No frozen case/rule/oracle byte was edited; no expected byte was touched.

Seat: `QXfsOptionsAbsent` · mode: **fixture only** (one case, one invocation chain, no real
mode, no host quota read, no selftest arm, no other case).

Receipt: `.ufo/waves/round-23/falsify/QXfsOptionsAbsent/scan.json`
(sha256 of the receipt is recorded at the end of this report).

## 1. Identities (byte-exact)

| item | value |
|---|---|
| case file | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/quota-cases/CaseXfsOptionsAbsent.json` |
| case sha256 (working tree) | `d54cba9914cf85c4c4036b250b2e8c6dd3401f770e3929f5072c980797e16a58` |
| case sha256 at seal commit `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687` | `d54cba9914cf85c4c4036b250b2e8c6dd3401f770e3929f5072c980797e16a58` |
| frozen bytes unchanged vs seal | **True** (re-checked after the run: same sha256) |
| case equals the selected corrected case (`cases-corrected/CaseXfsOptionsAbsent.json`) | **True** (identical sha256 `d54cba99…`; per `frozen/case-decisions.json`, id `CaseXfsOptionsAbsent`, `primary: true`) |
| seal is ancestor of production pin | yes (`git merge-base --is-ancestor 22772c10… f3dc07c0…` → 0) |
| production pin | `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` |
| tool | `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py` |
| tool sha256 (working tree) | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| tool sha256 at the pin | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| tool git blob at the pin | `439ff4c1a68fc4f98182c6b855b3b4c790286851` |
| tool bytes identical to the pinned production blob | **True** |
| own fixture copy | `/fast/scratch/hyaku/mori-r23/QXfsOptionsAbsent/fixture.json` sha256 `5f5b298a8c29308db22edabd52a166016cf10a24ac8adeb7c8a03f06da10eef7` (775 bytes) |
| fixture provenance | `case["fixture"]` serialized verbatim (`json.dumps`, `sort_keys`, `separators=(',',':')`); `json.loads(fixture) == case["fixture"]` → **True** |

`git status --porcelain --untracked-files=no` on the lane is empty: this seat changed no
tracked file, no frozen byte and no expectation. The only writes are this report, the
seat receipt and files under `/fast/scratch/hyaku/mori-r23/QXfsOptionsAbsent/`.

## 2. Source derivation re-opened (case rationale → frozen sources)

The case cites `S077`, `S078`, `S082`. The frozen source texts
(`evidence/sources/`, digests in `evidence/sources-manifest.json`) were re-read directly:

* **S077** (`Documentation/admin-guide/xfs.rst`, v7.2, lines 171–185): `noquota`
  ("Forcibly turns off all quota accounting and enforcement"), `uquota/usrquota/
  uqnoenforce/quota`, `gquota/grpquota/gqnoenforce`, `pquota/prjquota/pqnoenforce`.
  This is exactly the option vocabulary the case's absent-test uses.
* **S078** (`fs/xfs/xfs_super.c`, v7.2, `xfs_showargs` lines 238–254): per scope the
  kernel prints `,usrquota` / `,uqnoenforce` (238–241), `,prjquota` / `,pqnoenforce`
  (243–246), `,grpquota` / `,gqnoenforce` (248–251) and prints `,noquota` only when
  `!(mp->m_qflags & XFS_ALL_QUOTA_ACCT)` (253–254). **Consequence, confirmed by source:**
  a kernel-emitted xfs super-option string always contains either `noquota` or at least
  one quota/noenforce key, so the "neither" arm of the C2 table is unreachable in real
  mode. The case is therefore a synthetic-only fixture exercised through `--fixture`,
  exactly as its rationale states — and this seat ran it that way.
* **S082** (`Documentation/filesystems/proc.rst` v7.2, §3.5, lines 1965–1990): field
  layout `(1)…(m+4)` with the `-` separator at `(m+1)`, fstype `(m+2)`, mount source
  `(m+3)`, super options `(m+4)`, and "Parsers should ignore all unrecognised optional
  fields". The tool's `parse_mountinfo()` (separator scan + last three fields) matches.

The fixture's single xfs line
`40 1 253:2 / /srv/data rw,relatime shared:20 - xfs /dev/mapper/data rw,attr2,inode64,logbufs=8,logbsize=32k,noalign`
parses to super-option keys `rw, attr2, inode64, logbufs, logbsize, noalign` — no
`noquota`, none of `usrquota,uquota,quota,grpquota,gquota,prjquota,pquota`, none of
`uqnoenforce,gqnoenforce,pqnoenforce,qnoenforce`. The C2 table's fifth xfs row
(`unknown | n/a | xfs_quota_options_absent`) is therefore the only applicable row.

**Pre-seal amendment** (`preseal-amendment.md`) leaves this expectation unchanged:
its xfs precedence list (conflict → noquota → enforced key → accounting-only key →
absent) still lands on the absent arm, and its only fixture-level requirement touching
this file is the mandatory `qgroups_enabled` member, which the case carries as `null`
(paired with `qgroups:false` / `qgroups_mode:null`, as the amendment demands). The
device check cannot preempt the classification: fixture `st_dev` `253:2` equals the
chosen mount's field 3 `253:2`. The amendment's `ambiguous_overmount` refusal is not
reached: `/srv/data` occurs once, and the chosen mount's parent id `1` is exactly the id
of the longest strictly shorter covering mount (`/`), so no parent-id conflict exists.

## 3. Invocation (exactly one child at a time)

```
argv given   : python3 -I TOOL --fixture ABS_FIXTURE
argv actual  : ['/usr/bin/timeout', '15',
                '/usr/bin/prlimit', '--as=402653184', '--',
                '/usr/bin/python3', '-I',
                '/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py',
                '--fixture', '/fast/scratch/hyaku/mori-r23/QXfsOptionsAbsent/fixture.json']
cwd          : /fast/scratch/hyaku/mori-r23/QXfsOptionsAbsent
limits       : address_space_bytes=402653184 (384 MiB), timeout_seconds=15
rlimit check : RLIMIT_AS inside the interpreter = (402653184, 402653184) — verified by a
               separate probe child (`resource.getrlimit(RLIMIT_AS)`), interpreter VmPeak 17.6 MB
TMPDIR       : /fast/scratch/hyaku/mori-r23/QXfsOptionsAbsent/ (no /tmp fallback)
```

**Harness artifact, disclosed and isolated.** Running `prlimit` straight from this
seat's session shell segfaults its child (exit `139`, empty stdout/stderr) — *not* the
tool and *not* the case: `prlimit --as=393216 -- /bin/true` and
`prlimit --as=393216 python3 -I -c 'print("ok")'` fail identically, because that
shell's `VmSize` is ≈19 GiB, so the forked child inherits an address space already far
above `RLIMIT_AS` and dies on exec. `exec`ing a small binary first (the canonical chain
above) shrinks the inherited address space, after which `prlimit` behaves exactly as
specified. A corroborating run using `bash -c 'ulimit -v 393216; exec timeout -s KILL 15
python3 -I TOOL --fixture FIXTURE'` produced **byte-identical** stdout and stderr.
Both bounded runs and the artifact probe are recorded separately in the receipt.

`--fixture` mode opens the fixture file and nothing else: `probe_fixture()` calls
`load_fixture()` and `evaluate()`; `scan_btrfs_sysfs()` / `real_inputs()` (which read
`/proc/self/mountinfo`, `os.stat` and `/sys/fs/btrfs`) are on the real-mode path only.
No host quota state was read; real mode was never invoked.

## 4. Observed result

| channel | value |
|---|---|
| process exit | `2` |
| stdout sha256 | `fdbb22a30e9226099378559d25523f9ede99f400ff9eea9af2a00ea5cfbda08a` (954 bytes) |
| stderr sha256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) |

Verbatim stdout (single line, complete):

```json
{"df_covers_quota":false,"exit_code":2,"finding_id":"QUOTA_STATE_UNKNOWN","limits":"no per-user, per-group or per-project limit or usage is read. no NFS or server-side quota and no overlay or fuse quota is covered. a visible btrfs qgroups directory does not imply that any limit is set. an ext2/ext3/ext4 quota feature in the superblock is unobservable without privileged tools. sysfs and mountinfo races during quota enable, disable or remount are not excluded. df capacity percentages never cover quota exhaustion (FR2 / EDQUOT). QUOTA_DISABLED is not a capacity or health verdict; ENOSPC can coexist. the btrfs qgroups mode attribute is never read, so btrfs_qgroups_mode is null in real mode.","paths":[{"basis":"xfs_quota_options_absent","btrfs_qgroups_mode":null,"device_check":"match","enforcement":"n/a","fstype":"xfs","mount_point":"/srv/data","path":"/srv/data","quota_option_keys":[],"quota_state":"unknown"}],"schema":"mori-quota-surface-v1"}
```

Pretty-printed:

```json
{
  "df_covers_quota": false,
  "exit_code": 2,
  "finding_id": "QUOTA_STATE_UNKNOWN",
  "limits": "no per-user, per-group or per-project limit or usage is read. no NFS or server-side quota and no overlay or fuse quota is covered. a visible btrfs qgroups directory does not imply that any limit is set. an ext2/ext3/ext4 quota feature in the superblock is unobservable without privileged tools. sysfs and mountinfo races during quota enable, disable or remount are not excluded. df capacity percentages never cover quota exhaustion (FR2 / EDQUOT). QUOTA_DISABLED is not a capacity or health verdict; ENOSPC can coexist. the btrfs qgroups mode attribute is never read, so btrfs_qgroups_mode is null in real mode.",
  "paths": [
    {
      "basis": "xfs_quota_options_absent",
      "btrfs_qgroups_mode": null,
      "device_check": "match",
      "enforcement": "n/a",
      "fstype": "xfs",
      "mount_point": "/srv/data",
      "path": "/srv/data",
      "quota_option_keys": [],
      "quota_state": "unknown"
    }
  ],
  "schema": "mori-quota-surface-v1"
}
```

## 5. Primary comparison (the case's own six-field denominator)

Field order as scored: `path, fstype, mount_point, quota_state, enforcement, basis`.

| check | expected | actual | match |
|---|---|---|---|
| process exit | `2` | `2` | **yes** |
| `finding_id` | `QUOTA_STATE_UNKNOWN` | `QUOTA_STATE_UNKNOWN` | **yes** |
| path 0 six-tuple | `("/srv/data", "xfs", "/srv/data", "unknown", "n/a", "xfs_quota_options_absent")` | `("/srv/data", "xfs", "/srv/data", "unknown", "n/a", "xfs_quota_options_absent")` | **yes** |
| path count / order | 1 path, `/srv/data` first | 1 path, `/srv/data` first | **yes** |

**Primary pass: 1/1** (case denominator = 1). The tool's own `exit_code` field also
equals the process exit (`2`), so the output is internally consistent.

## 6. Supplementary metadata (reported apart — never inside the primary denominator)

The sealed case carries **no** supplementary expectation keys; the following are
observed metadata plus the values the case rationale implies, checked separately.

| field | observed | implied by the case rationale | agree |
|---|---|---|---|
| `device_check` | `match` | `match` (fixture `st_dev` `253:2` == mount field 3 `253:2`) | yes |
| `quota_option_keys` | `[]` | `[]` (no xfs quota/noquota/noenforce key in the super options) | yes |
| `btrfs_qgroups_mode` | `null` | `null` (xfs row; mode never projected for a non-btrfs row) | yes |
| `schema` | `mori-quota-surface-v1` | `mori-quota-surface-v1` | yes |
| `df_covers_quota` | `false` | `false` (contract C2) | yes |
| `limits` | present (boundary text) | present | yes |

Supplementary pass: 6/6 observed-vs-implied checks — reported separately; it does not
widen or narrow the primary 1/1.

## 7. Integrity checks

* Output path objects carry exactly the nine allowed keys
  (`path, fstype, mount_point, quota_state, enforcement, basis, device_check,
  quota_option_keys, btrfs_qgroups_mode`) — **true**, no extra key.
* Leak probe over the stdout bytes for mount sources (`/dev/mapper/data`, `dm-3`,
  `/dev/mapper/root`, `dm-0`, `/dev/nvme0n1p2`), the fixture UUID
  (`d1e4f2a0-…`), non-quota option names (`attr2`, `inode64`, `logbufs`, `logbsize`,
  `noalign`, `space_cache`, `subvolid`, `subvol=`) and option values (`errors=`,
  `relatime`, `shared:`): **zero hits**.
* Case file sha256 unchanged after the run; tool file sha256 unchanged after the run;
  lane has no tracked modifications.
* Expected bytes untouched: the sealed `expected` object was read, never rewritten.

## 8. Scope, and what this seat deliberately did not do

* Only `CaseXfsOptionsAbsent` was executed — one case, fixture mode only. No real-mode
  run, no `--selftest` arm, no other sealed case, no builds, no lint, no full suite.
* `CaseEscapedSpace` was **not** executed here (other seat). Its strict red is a known,
  recorded contradiction (`evidence/frozen-contradiction.json`: selected mount 43 /
  parent 33 versus the shorter `/srv` cover 42, sealed rule requiring
  `unknown/n/a/ambiguous_overmount` with null fstype/mountpoint, frozen expectation
  `exit 1 / QUOTA_ENABLED`). It is a **mismatch to be reported, not excused**; it is
  unrelated to this case's fixture and does not affect the C2 strict target staying
  UNPROVABLE at 29/30. No exception, exclusion, relabel or rewrite was applied to it.
* The quota selftest 49/49 arm (separately corrected fixture input) is a different arm
  and is **not** this case; no selftest was run here, and the two must not be conflated.
* No quota tool, `quotactl`, `btrfs qgroup`, `xfs_quota`, `repquota`, mount or
  remediation call was made; no live qgroup/mode value was read; `privacy_clearance`
  stays false and no baseline acceptance is implied by this result.

## 9. Residual risk and verification gaps

1. **This is a synthetic arm only.** By S078 the "neither noquota nor any quota key"
   state is unreachable from a kernel-emitted xfs super-option string, so the case
   validates the classifier's absent-arm logic and its fixture plumbing, not a reachable
   host state. No real-mode arm of this arm exists and none was attempted.
2. **Harness-level bound.** The 384 MiB `RLIMIT_AS` had to be applied via
   `exec`+`prlimit` (or `ulimit -v`) because `prlimit` forked from this seat's
   ~19 GiB-VmSize shell crashes its child with SIGSEGV. The interpreter's own VmPeak
   was 17.6 MB, so the bound is not close to binding; the crash is a harness artifact,
   demonstrated with `/bin/true`. Sibling seats that invoke `prlimit` directly from a
   smaller-address-space shell are unaffected.
3. **Expected bytes not edited, expectation re-derivation not re-adjudicated.** This
   seat confirms the tool reproduces the sealed expectation; it does not re-open whether
   the sealed expectation is itself correct against S077/S078/S082. For this case the
   re-opened sources agree with the sealed row (`unknown | n/a | xfs_quota_options_absent`).
4. **One case, one pass.** Determinism rests on two byte-identical bounded runs of the
   same case, not on a repeated-measurement series.
5. **Scope note, no impact on this case.** The tool's xfs noenforce key set includes the
   generic `qnoenforce` alongside `uqnoenforce/gqnoenforce/pqnoenforce`; `qnoenforce`
   appears in the contract table but not in the S077/S078 kernel vocabulary. It is
   irrelevant to this case (no noenforce key is present in the fixture) and was not
   exercised here; flagged only because it is an adjacent, unexercised input surface.
6. Nothing in this report is an admission: C1 calibration (held 5) and the C2 strict
   coverage target (UNPROVABLE at 29/30) are unchanged by this seat's result, and
   probe visibility is not clearance, health or admission.

## 10. Reproduction

```
cd /fast/scratch/hyaku/mori-r23/QXfsOptionsAbsent
bash -c 'exec /usr/bin/timeout -s KILL 15 /usr/bin/prlimit --as=402653184 -- \
  /usr/bin/python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
  --fixture /fast/scratch/hyaku/mori-r23/QXfsOptionsAbsent/fixture.json'
# exit 2; stdout sha256 fdbb22a30e9226099378559d25523f9ede99f400ff9eea9af2a00ea5cfbda08a
```

Receipt: `.ufo/waves/round-23/falsify/QXfsOptionsAbsent/scan.json`
(`mori-r23-quota-case-falsify-scan-v1`, verdict `MATCH__case_not_falsified`,
primary 1/1, 8837 bytes, sha256
`4ab43ad56abaa57e19b7083561dc34f0fc20ab7bc7e34b3d983b15f9a7ae416d`).

Verbatim stdout block in §4 is byte-identical to the captured stdout
(block sha256 `05f4163c2f6cbedd51c9e4a8e8051e7ba2030239e57baabab0a6a2069f002682`
= `fdbb22a30e9226099378559d25523f9ede99f400ff9eea9af2a00ea5cfbda08a` with the
trailing newline stripped).

Receipt digest history: the digest quoted above (`4ab43ad5…7ae416d`, 8837 bytes) is the
**pre-correction** receipt. The receipt now additionally carries an appended
`corrections` array (3 entries — nothing removed, no prior field rewritten); its current
digest is `203587a124335c846bb58b253844b25060376d816f047fc9d27bbb95ddb44479`
(11544 bytes). See §11.

## 11. Correction (appended after the fact; §3 and §9 wording preserved above for the record)

Requested by L1 (`MadoR22-2`) after this seat's report was filed. **No prior report text
was rewritten and no receipt field was removed**; the correction is appended here and as
an appended `corrections` array in the receipt.

### 11.1 Unit error in the red startup probe

`prlimit --as` takes **bytes**. The red startup probe recorded in the receipt
(`runs[2]`, chain `prlimit --as=393216 … timeout … python3 -I TOOL --fixture FIXTURE`,
exit `139`, empty stdout/stderr) therefore applied an address-space cap of
**393216 bytes = 384 KiB**, not 384 MiB. A 384 KiB address-space cap is unattainable
for *any* dynamically linked binary — the libc mapping alone exceeds it — so the
SIGSEGV of `/bin/echo hi` and of `python3 -I -c 'print("ok")'` under that value is
explained by the unit error in that probe alone. That probe was a harness probe, not a
case measurement: it exercised no case bytes, produced no verdict and is not part of
the case denominator.

### 11.2 The inherited-VmSize explanation is withdrawn as a finding

§3's "Harness artifact" paragraph and §9 item 2 attribute the failures to an inherited
≈19 GiB `VmSize` of the session shell. **That causality was not established**: no
controlled measurement separated the unit error (§11.1) from a possible
inherited-address-space effect. The observations are consistent with an inherited
effect — probes at 1048576–8388608 *bytes* failed with "failed to map segment from
shared object" from the large-VmSize shell, while an `exec`-then-`prlimit` chain at
402653184 bytes succeeded — but consistency is not proof, and the unit error alone
accounts for the 393216-byte failures. The inherited-VmSize claim is therefore
withdrawn as a finding and retained only as an unverified hypothesis. Nothing in the
case measurement depended on it.

### 11.3 Both successful SUT runs genuinely ran under a 384 MiB cap

The canonical run's cap was `--as=402653184` bytes = **384 MiB exactly** (correct unit),
and the corroborating run used `ulimit -v 393216` **KiB = 384 MiB**. In both cases the
child interpreter reported `RLIMIT_AS = (402653184, 402653184)` bytes, so the 384 MiB
address-space bound was in force with the 15 s timeout. Disclosure preserved as
captured: **two successful SUT runs** (each exit `2`, byte-identical stdout sha256
`fdbb22a3…bda08a`, empty stderr) **plus one red startup probe** (§11.1). No
single-invocation compliance is claimed; the receipt lists all three runs separately
with their actual argv.

### 11.4 No frozen, production or expectation change

This correction alters no measurement: the case sha256
`d54cba9914cf85c4c4036b250b2e8c6dd3401f770e3929f5072c980797e16a58`, the tool sha256
`e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92`, the primary
comparison (1/1), the exit/`finding_id` match and the supplementary checks (6/6) all
stand unchanged. The historical pin `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` and the
frozen results are unchanged; final C2 production is withdrawn after all 96 pinned seats
settle, which does not alter this seat's measurement or its `MATCH__case_not_falsified`
verdict for `CaseXfsOptionsAbsent`. This correction is not an admission, clearance,
health verdict or baseline acceptance.

### 11.5 Post-measurement lane state (observed after the correction; factual only)

After this seat's measurement and correction, the lane working tree shows an
**uncommitted** deletion of `tools/mori-quota-surface.py` together with concurrent
edits to `SKILL.md`, `PROVINANCE.md`, `SCORECARD.md`, `LOG.md`, `corpus/*` and
`.ufo/waves/round-23/build/*` — the parent's in-flight production cutover, not this
seat's action (this seat wrote only this report, its own receipt under
`.ufo/waves/round-23/falsify/QXfsOptionsAbsent/`, and files under
`/fast/scratch/hyaku/mori-r23/QXfsOptionsAbsent/`). The measured artifact remains
recoverable and identity-bound: git blob `439ff4c1a68fc4f98182c6b855b3b4c790286851` at
both `f3dc07c0…` and HEAD `6eb889c0…`, sha256
`e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` — byte-identical to
the bytes this seat executed. The frozen case bytes
(`d54cba9914cf85c4c4036b250b2e8c6dd3401f770e3929f5072c980797e16a58`) are unchanged, so
the measurement remains reproducible from the pinned blob regardless of the working-tree
cutover. This observation changes no verdict and implies no admission.

### 11.6 Git-probe provenance (clarification, no change)

The git probes behind §1/§7 (`git show <rev>:<path>`, `git rev-parse <rev>:<path>`,
`git ls-tree`, `git merge-base --is-ancestor`, `git status --porcelain
--untracked-files=no`) all ran against the lane repo `mori-shokunin`, which is a normal
clone: no `extensions.partialclone`, no `remote.origin.promisor`, no `.promisor` packs,
`git count-objects -v` reporting 8618 loose and 745 in-pack objects. Every object those
probes touched was already local, so no lazy fetch was possible and no blob could have
been materialised. This seat used no blobless/partial clone and no
`tests/report-audit/promisor-grid.py` fixture, so the "missing blob ⇒ content-derived
refusal" premise of that lane does not apply here; the integrity claims in §1 and §7
rest on working-tree bytes and on a pinned blob present locally
(`439ff4c1a68fc4f98182c6b855b3b4c790286851`, sha256 `e4857413…5b8f7e92`). No change to
any claim, measurement or verdict.
