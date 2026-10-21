# QNoCover — falsification of sealed C2 case `CaseNoCover` (round 23)

Seat: `QNoCover` (leaf falsifier, read-only seat). Scope: **exactly one** sealed C2
case, `CaseNoCover.json`, executed in **fixture mode only**. No real mode, no other
case, no build/test/lint. No source, case, oracle, expectation or production file
was edited; the only writes are this report and the assigned receipt.

---

## 1. Inputs (exact byte identities)

| Item | Path | SHA-256 |
|---|---|---|
| Sealed case | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/quota-cases/CaseNoCover.json` | `334c7cfdddbf9b9f650e62dab94aeba656047044402de166d5b094ed1d210215` |
| Selected (corrected) case | `.ufo/waves/round-23/cases-corrected/CaseNoCover.json` | `334c7cfdddbf9b9f650e62dab94aeba656047044402de166d5b094ed1d210215` |
| Original proposal | `.ufo/waves/round-23/cases-proposed/CaseNoCover.json` | `27fd2e5f12fe0db0767f72649457a6cac4ed048109c6d660e7ac5e723a3d49d6` |
| Candidate tool under test | `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| My fixture copy | `/fast/scratch/hyaku/mori-r23/QNoCover/fixture.json` | `6a70ea1169d1770486c49f3d561d95a26fbc5d85b6a93a2e43a8620cfa2cc0db` |
| Receipt | `.ufo/waves/round-23/falsify/QNoCover/scan.json` | `502cbfd7b43216676dd58942514fb5b8e3956d503636cfe3d97300feba88548b` |

* `frozen/quota-cases/CaseNoCover.json` is **byte-identical** to
  `cases-corrected/CaseNoCover.json` (the file named by
  `frozen/case-decisions.json` as the selected case for id `CaseNoCover`,
  `primary: true`, reason "Independent source-derived pre-measurement correction;
  exact author bytes, no L1 expectation edits"). Both also match the blob at the
  pinned production commit `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`
  (`git show <pin>:.ufo/waves/round-23/frozen/quota-cases/CaseNoCover.json`).
* The frozen fixture is the proposal fixture **plus** the amendment-required
  `qgroups_enabled: null` member on the single btrfs UUID record. Delta confirmed
  programmatically: only top-level key `btrfs_sysfs` differs; `expected` block is
  byte-equal between proposal and sealed case.
* **Same-identity / one canonical runtime:** the working-tree tool blob equals the
  blob at pinned commit `f3dc07c0` and at `HEAD` (`6eb889c0`); `git log <pin>..HEAD
  -- tools/mori-quota-surface.py` is empty and `git diff <pin>..HEAD -- <tool>` is
  empty. `f3dc07c0` is an ancestor of `HEAD`. The executed file is therefore the
  pinned production source — no rerouting, no substituted candidate.
* My fixture copy is a JSON-equal copy of `case["fixture"]` (asserted in the
  receipt: `equals_case_fixture: true`); the case file itself was never modified.

## 2. Source derivation / amendment read

* Contract C2 (`contract.md`): mount resolution per path — candidate mounts are
  those whose mount point equals the realpath, is `/`, or is a **component**
  prefix of the realpath; longest mount point wins; **none → `unknown`, basis
  `no_covering_mount`**. Verdict precedence: setup → 2; any `enabled` → 1
  `QUOTA_ENABLED`; else any `unknown` → 2 `QUOTA_STATE_UNKNOWN`; else 0.
* Pre-seal amendment (`preseal-amendment.md`), which supersedes the ambiguous
  original clauses: parse the **last three fields of each chosen line** (never
  file-wide), decode only `\040/\011/\012/\134`, reject other escapes as
  `QUOTA_SETUP`; on no-cover/ambiguous/device-mismatch preemption
  `quota_option_keys=[]`, `btrfs_qgroups_mode=null`, `device_check=not_checked`,
  `fstype=null`, `mount_point=null`; the primary denominator stays the **six**
  scored fields, with supplementary metadata asserted separately and never
  inserted into the primary expectation.
* Derived source row: `sources: ["S082"]`; the evidence row for S082 in
  `.ufo/waves/round-23/evidence/source-quotes.json` is "Parsers should ignore all
  unrecognised optional fields." (`source_sha256 e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126`),
  i.e. the case exercises optional-field-tolerant mountinfo parsing.
* Implementation read (source review only, before execution):
  `tools/mori-quota-surface.py:407-419` `covering_mounts()` uses
  `point == resolved or point == "/" or resolved.startswith(point + "/")`;
  `:421-462` `resolve_mount()` returns the refusal `"no_covering_mount"` when
  `covered` is empty; `:513-559` `evaluate()` seeds the row with
  `fstype=None, mount_point=None, quota_state="unknown", enforcement="n/a",
  basis="no_covering_mount", device_check="not_checked", quota_option_keys=[],
  btrfs_qgroups_mode=None` and returns that row unchanged when `mount is None`;
  `:561-569` `verdict()` maps an `unknown` row to exit 2 / `QUOTA_STATE_UNKNOWN`.

## 3. Execution (single child, one case, fixture mode)

Scratch root (never `/tmp`): `/fast/scratch/hyaku/mori-r23/QNoCover/`.

```
argv : python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
            --fixture /fast/scratch/hyaku/mori-r23/QNoCover/fixture.json
wrapper: timeout --signal=KILL 15 prlimit --as=402653184   # 384 MiB address space, 15 s
cwd  : /fast/scratch/hyaku/mori-r23/QNoCover
```

Observed: **exit 2**, stdout = one JSON object (sha256
`eb28693562691531b126e37df9bc8ed0b2ab372826a6241a400b253f46becf68`), stderr
**empty** (sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).
No timeout, no signal, no memory-limit kill, no setup error.

stdout (verbatim):

```json
{"df_covers_quota":false,"exit_code":2,"finding_id":"QUOTA_STATE_UNKNOWN","limits":"no per-user, per-group or per-project limit or usage is read. no NFS or server-side quota and no overlay or fuse quota is covered. a visible btrfs qgroups directory does not imply that any limit is set. an ext2/ext3/ext4 quota feature in the superblock is unobservable without privileged tools. sysfs and mountinfo races during quota enable, disable or remount are not excluded. df capacity percentages never cover quota exhaustion (FR2 / EDQUOT). QUOTA_DISABLED is not a capacity or health verdict; ENOSPC can coexist. the btrfs qgroups mode attribute is never read, so btrfs_qgroups_mode is null in real mode.","paths":[{"basis":"no_covering_mount","btrfs_qgroups_mode":null,"device_check":"not_checked","enforcement":"n/a","fstype":null,"mount_point":null,"path":"/srv/quota-probe/data","quota_option_keys":[],"quota_state":"unknown"}],"schema":"mori-quota-surface-v1"}
```

## 4. Comparison against the sealed expectation

Primary (six scored fields per path, ordered as the sealed tuple):

| # | Field | Expected (sealed) | Actual | Match |
|---|---|---|---|---|
| 0 | `path` | `/srv/quota-probe/data` | `/srv/quota-probe/data` | ✅ |
| 0 | `fstype` | `null` | `null` | ✅ |
| 0 | `mount_point` | `null` | `null` | ✅ |
| 0 | `quota_state` | `unknown` | `unknown` | ✅ |
| 0 | `enforcement` | `n/a` | `n/a` | ✅ |
| 0 | `basis` | `no_covering_mount` | `no_covering_mount` | ✅ |

* `exit`: expected `2` — actual `2` ✅
* `finding_id`: expected `QUOTA_STATE_UNKNOWN` — actual `QUOTA_STATE_UNKNOWN` ✅
* path count expected 1 — actual 1 ✅; **all six-field tuples match: true**
* output `exit_code` field `2` equals the process exit `2` (internal consistency)
* output `schema` = `mori-quota-surface-v1` (the contract's spelling; the module
  docstring still names itself `mori-quota-surface-v3.py` — cosmetic only, no
  behavioural effect; flagged below as a minor observation)

Supplementary metadata (asserted **apart** from the six-field denominator, per the
amendment — these values are *not* part of the sealed primary expectation and do
not widen it):

| Field | Observed | Amendment expectation for a no-cover row |
|---|---|---|
| `device_check` | `not_checked` | `not_checked` ✅ |
| `quota_option_keys` | `[]` | `[]` ✅ |
| `btrfs_qgroups_mode` | `null` | `null` ✅ |

Leakage scan of stdout (must never echo mount sources, option values, device
links or UUIDs): tokens `/dev/nvme0n1p1`, `/dev/nvme0n1p2`, `/dev/mapper/root`,
`dm-0`, `1d02a454-c549-4a35-b567-89d60902af8e`, `noquota`, `attr2`, `compress`,
`subvol` — **none present** ✅.

## 5. Verdict

**PASS — no mismatch for `CaseNoCover`.** The sealed C2 expectation for this case
is reproduced exactly by the pinned production tool in fixture mode: exit `2`,
finding `QUOTA_STATE_UNKNOWN`, and the ordered six-field tuple
`(/srv/quota-probe/data, null, null, unknown, n/a, no_covering_mount)`.

Why this case is discriminating (source-level, not just outcome-level): the fixture
mountinfo has **no `/` mount line**, and the nearest mount point `/srv/quota` is a
*string* prefix but **not a component** prefix of `/srv/quota-probe/data`. A
naive `startswith(point)` implementation would have selected the `/srv/quota`
xfs mount and returned `disabled / n/a / xfs_noquota_option` with exit `0`. The
implementation appends the `/` component boundary
(`mori-quota-surface.py:414-416`), so the no-cover refusal is reached and the
`/srv/quota` xfs `noquota` line is correctly *not* consulted — the case is not
vacuous and the green result is earned, not accidental.

## 6. Scope discipline, prohibitions honoured

* Fixture mode only; **no real mode** invocation, no host mountinfo/sysfs read,
  no `quotactl`/`btrfs qgroup`/`xfs_quota`/`repquota`/`mount` call, no quota
  tooling of any kind, no credential/`agent.db`/session-transcript read, no
  journal/service/process probe.
* Only `git show/log/status/rev-parse/merge-base/diff`-style read-only git on the
  absolute lane repo; no lane `git add/commit/push`, no `jj` mutation, no writes
  outside my assigned report + receipt path and my own scratch tree.
* One child at a time; one fixture invocation total; no build/test/lint/suite.
* Expected/case/oracle/production bytes unchanged — verified by re-hashing the
  frozen case, the tool and the sealed bytes at the pinned commit.
* **Tool installs: none.** No install or update was needed for this task
  (stock `python3` 3.14.8, coreutils `timeout`, `prlimit` were already present),
  so no tool/version/channel record is owed.

## 7. Residual risk / verification gaps (not defects in this seat's scope)

1. **Case-level coverage only.** This seat proves one of the 30 sealed C2 cases.
   The C2 headline ("every sealed case matches") is *not* established here, and
   I did not run any other case — by instruction. The known strict red in
   `CaseEscapedSpace` (frozen contradiction, `evidence/frozen-contradiction.json`)
   remains a genuine mismatch that **must not be excused**; it is untouched and
   unaddressed by this seat, and I neither verified nor excused it.
2. **Fixture-only reach.** `no_covering_mount` is unreachable in real mode, where
   `/` is always a mount point; this case therefore proves the fixture-mode
   resolution path only, not any real-mode behaviour.
3. **Exit-code ambiguity (observation, contract-compliant).** Exit `2` denotes both
   `QUOTA_SETUP` and `QUOTA_STATE_UNKNOWN`; only `finding_id` separates them.
   The sealed oracle compares exit **and** finding_id together
   (`oracle-quota.py:329-330`), so the ambiguity is handled — but any harness that
   keyed on exit code alone would conflate a setup failure with an unknown
   verdict. Worth flagging to the integrator; no change is required by contract.
4. **Cosmetic drift.** The module docstring names `mori-quota-surface-v3.py` while
   the file is `mori-quota-surface.py` and `SCHEMA` is `mori-quota-surface-v1`
   (the contract-required spelling). No behavioural impact, but it is a
   documentation inconsistency a future reader could trip over.
5. **Fixture-input correction provenance.** The sealed fixture carries the
   amendment-mandated `qgroups_enabled: null`. I confirmed the frozen bytes match
   the selected/corrected case and the pinned commit, but the *authoring* of that
   delta rests on `cases-corrected/` + `case-decisions.json`, which is upstream of
   this seat.

**Residual risk overall: low for this case.** The single bounded fixture
invocation was hermetic (scratch fixture copy, `-I` isolated interpreter, 384 MiB
AS cap, 15 s timeout), fully hashed, and the observed output reproduces the sealed
expectation on every scored field with no leakage.
