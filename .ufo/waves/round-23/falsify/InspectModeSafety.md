# InspectModeSafety — does the final no-mode-read decision avoid the btrfs ASSERT race?

**Verdict: YES, source-verified for the pinned production bytes.** The pinned tool never
constructs or opens the btrfs `qgroups/mode` attribute in real mode, so `qgroup_mode_show()`
— the only show function in the reopened sources carrying
`ASSERT(btrfs_qgroup_enabled(fs_info))` — is unreachable from the probe. The race that made
an "enabled-first, then mode" gate unsafe is real in S079/S080 and is avoided categorically
by never issuing the read, not by narrowing a window. The remaining real-mode qgroups read is
the `enabled` attribute, whose show function contains no ASSERT.

No live sysfs/attribute read, tool execution, host probe, edit, or install was performed.

## 1. Artifacts and exact identities

| item | identity |
|---|---|
| lane pin (production commit) | `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` |
| lane HEAD at inspection | `6eb889c037163e4886eaa61501258910d6a529b9`; pin is an ancestor (`git merge-base --is-ancestor` rc 0) |
| `tools/mori-quota-surface.py` blob | `439ff4c1a68fc4f98182c6b855b3b4c790286851`, identical at pin and HEAD (`git diff --stat` empty; the working-tree file's sha256 equals the pin blob's content sha256) |
| pinned tool bytes | 66644 bytes, sha256 `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| measure4 exercised tool | same sha256 `e4857413…`, staged path recorded in `evidence/measure4/c2-after-real-observed.json` (`tool.sha256`) |
| S079 `fs/btrfs/sysfs.c` (v7.2) | 72925 bytes, sha256 `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` |
| S080 `fs/btrfs/qgroup.c` (v7.2) | 139049 bytes, sha256 `121a0af27f9553a9749c837536d618e2ea50d44ce54b30b032fa56e6f3df6ed5` |
| build v3 candidate (not the sealed artifact) | `build/ImplQuota/mori-quota-surface-v3.py`, 66279 bytes, sha256 `5199e97b…`; differs from pinned bytes, but its `scan_btrfs_sysfs` region is byte-identical to production (diff hunks at other lines; see §4) |

Frozen case/oracle/expectation bytes were not opened for write and not changed. This report
does not evaluate C1/C2 counts or the frozen CaseEscapedSpace contradiction.

## 2. Reopened kernel facts (S079, S080 only)

### S079 — the two qgroups show functions

* `qgroup_enabled_show` (S079 `fs/btrfs/sysfs.c:2355-2368`): under
  `spin_lock(&fs_info->qgroup_lock)`, reads
  `enabled = fs_info->qgroup_flags & BTRFS_QGROUP_STATUS_FLAG_ON`, unlocks, emits `%d\n`
  (2363-2366). **No ASSERT anywhere in this function.** It reports the in-memory status
  `FLAG_ON` bit, not the runtime enable state.
* `qgroup_mode_show` (S079 `:2370-2395`): under the same spinlock, line 2378 is
  `ASSERT(btrfs_qgroup_enabled(fs_info));`; then it switches on `btrfs_qgroup_mode()` and
  emits `qgroup\n` (FULL) or `squota\n` (SIMPLE), default warning for anything else;
  registered as `BTRFS_ATTR(qgroups, mode, qgroup_mode_show)` at 2395. This is the sole
  qgroups show function with an assertion.

### S080 — what `btrfs_qgroup_enabled()` actually tests, and the two orderings

* `btrfs_qgroup_mode()` (S080 `fs/btrfs/qgroup.c:33-40`): returns DISABLED when
  `BTRFS_FS_QUOTA_ENABLED` is clear in `fs_info->flags`; otherwise SIMPLE or FULL from
  `qgroup_flags` bits.
* `btrfs_qgroup_enabled()` (`:42-45`) is `btrfs_qgroup_mode() != DISABLED`, i.e. it tests
  the **runtime** `BTRFS_FS_QUOTA_ENABLED` bit. The `enabled` sysfs attribute tests the
  **`FLAG_ON` status bit** (S079:2363). They are different words.
* Quota **disable** (`btrfs_quota_disable`, `:1332`):
  `clear_bit(BTRFS_FS_QUOTA_ENABLED, &fs_info->flags)` at **:1367**, outside
  `qgroup_lock` (the mutex was dropped at :1360), then reservation flush (:1375),
  transaction start (:1390), and only later, under `spin_lock(&fs_info->qgroup_lock)` at
  :1403, `fs_info->qgroup_flags &= ~BTRFS_QGROUP_STATUS_FLAG_ON` at **:1406** and
  `~SIMPLE_MODE` at :1407, unlock at :1409. The sysfs directory is removed still later via
  `btrfs_free_qgroup_config()` (:1411), which calls `btrfs_sysfs_del_qgroups()` at :689.
  So during **[1367, 1406]** the directory is present and `enabled` still reads 1 while
  `btrfs_qgroup_enabled()` is already false. A `mode` read in that window enters
  `qgroup_mode_show`, takes `qgroup_lock`, and evaluates the ASSERT against the cleared
  runtime bit. The `qgroup_lock` does not serialize with the earlier `clear_bit`, so
  taking the lock does not close the window.
* Quota **enable** (`btrfs_quota_enable`, `:997`): `btrfs_sysfs_add_qgroups()` creates the
  directory at **:1032**; `fs_info->qgroup_flags = BTRFS_QGROUP_STATUS_FLAG_ON` at
  **:1104**; the runtime bit is set only at **:1256** (`set_bit` under `qgroup_lock`).
  During **[1104, 1256]** `enabled` can read 1 while `btrfs_qgroup_enabled()` is still false —
  the same overlap in the opposite direction. (Mount-time `qgroup_flags |= flags;
  if FLAG_ON set_bit(...)` at :612-615 sets the runtime bit immediately and is not this
  window.)

**Therefore an enabled-first gate is not race-safe**, exactly as the pre-seal amendment and
SentinelProbe concluded: `enabled` reports `FLAG_ON`, the ASSERT tests the runtime bit, and
both orderings expose intervals where `enabled == 1` coexists with a failing ASSERT.

### Inference boundary

S079/S080 show the ASSERT invocation; the macro's expansion (e.g. `BUG()` when
`CONFIG_BTRFS_ASSERT=y`, otherwise a non-fatal behaviour) lives outside the two reopened
files. I did not read the host kernel config or messages.h. The safety conclusion below does
not depend on that expansion: the failing show function is never invoked.

## 3. Does the final decision avoid the race?

**Yes.** The decision recorded in `preseal-amendment.md:132-140` ("Real mode therefore NEVER
reads qgroups/mode and emits btrfs_qgroups_mode=null as intentionally unobserved") and in
the committed knowledge `corpus/knowledge/quota-surface-r23.md:99-109` ("Final real-mode
design NEVER reads qgroups/mode"; it explicitly supersedes the earlier enabled-first
instruction) is implemented in the pinned production bytes such that no real-mode code path
can form the `mode` pathname. With the read never issued:

* `qgroup_mode_show` is never entered, so the ASSERT at S079:2378 is unreachable and no
  kernel assertion can be evaluated, regardless of the disable/enable window and regardless
  of `CONFIG_BTRFS_ASSERT`.
* The only real-mode qgroups attribute opened is `qgroups/enabled`; `qgroup_enabled_show`
  (S079:2355-2368) has no ASSERT. It locks, reads `FLAG_ON`, unlocks, emits the number.
  Directory listings (`/sys/fs/btrfs`, `<uuid>/devices`) and `os.stat(<uuid>/qgroups)` do
  not invoke qgroups show functions at all.
* Reading `enabled` can still be a stale observation during the [1367,1406] disable window
  (it may report 1 while disable is in flight). That is a classification-timeliness fact,
  not a kernel-safety one: no ASSERT and no writer is involved. The contract already
  disclaims enable/disable/remount races (`contract.md`, "sysfs/mountinfo races during
  enable/disable/remount are not excluded").

## 4. Implementation audit of the pinned production bytes

Static source audit of `tools/mori-quota-surface.py` at pin (blob
`439ff4c1…`, sha256 `e4857413…`); AST parse and explicit call-site enumeration, no
execution:

* `scan_btrfs_sysfs()` (:571-627) sets `mode = None` (:599) and stores it unchanged
  (:625). The inline reason at :616-620 states the show function asserts enabled and the
  attribute is never read.
* The only filesystem path joins in the file are:
  `BTRFS_SYSFS + name` (:586), `directory + "devices"` (:594),
  `directory + "qgroups"` (:600), `qgroups_path + "enabled"` (:609).
  **No join uses `"mode"`.**
* The only call to `read_sysfs_text()` is the `enabled` path at :609; `read_sysfs_text`
  itself opens its argument at :633. It has no other call site.
* All `open()` call sites: :633 (the enabled/attribute reader), :660 (`MOUNTINFO`),
  :697 (fixture JSON). `os.stat` call sites: :602 (`<uuid>/qgroups`), :668 (probed path).
  `os.listdir` call sites: :581 (`/sys/fs/btrfs`), :594 (`<uuid>/devices`). No call reads
  `qgroups/mode`.
* The three `"mode"` string literals are :625 (record dict key), :769 (fixture record
  field), :481 (`record["mode"]` lookup in `classify_btrfs`). None is used in a path.
  `record["mode"]` is therefore `None` for every real-mode record; a non-null value is only
  possible through the fixture projection `btrfs_modes()` (:399-404).
* Read-failure behaviour at the sysfs surface: `os.stat(qgroups_path)` maps
  `FileNotFoundError` to `qgroups=False` (dir_absent) and other `OSError` to `qgroups=None`
  (unknown), :601-606; an unreadable/enotdir `enabled` read returns `None`, mapped to
  `enabled=None` and basis `btrfs_qgroups_enabled_unavailable`, :609-615 + `classify_btrfs`
  :484. No error path falls back to reading mode.

The pinned artifact is not byte-identical to the build v3 candidate (`5199e97b…`, 66279
bytes), but the `scan_btrfs_sysfs` region and the no-read comments are identical; the diff
between the pinned blob and the v3 candidate is outside that function. Measure4 recorded the
pinned sha256 as the exercised tool, so the receipt documents above are tied to the audited
bytes, not to the v3 working copy. Exact diff hunks between the pinned blob and the v3
candidate: 551, 711, 715-716, 781, 792, 1537, 1776-1789 — none inside `scan_btrfs_sysfs()`
(:571-627).

## 5. Behavioural corroboration from existing receipts (not re-run)

From `evidence/measure4/c2-after-real-observed.json` (tool.sha256 `e4857413…`):

* Real control stdout: both paths carry `"btrfs_qgroups_mode": null`; fleet root is
  `disabled / btrfs_qgroups_dir_absent`, `/tmp` is `disabled / xfs_noquota_option`. The
  output's limits string includes "the btrfs qgroups mode attribute is never read, so
  btrfs_qgroups_mode is null in real mode."
* Fixture projection is separate and unchanged: CaseBtrfsQgroup yields mode `qgroup`,
  CaseBtrfsSquota yields `squota`, SupplementQgroupDisabled/Unknown yield null with
  `btrfs_qgroups_disabled` / `btrfs_qgroups_enabled_unavailable`.
* The frozen real expectation (`frozen/c2-expected-real.json`) asserts only the six
  contract fields; it contains no `btrfs_qgroups_mode`, so null real-mode metadata does not
  change that control.

These receipts are cited as existing evidence; I did not execute the driver, oracle, or
selftest.

## 6. Residual observations and gaps

1. **Documentation hazard, not a code defect.** The committed knowledge file still contains
   the superseded enabled-first instruction at lines 20-24 ("Read enabled first; read mode
   only when enabled is1"), then explicitly supersedes it at lines 99-109. The pinned tool
   follows the final section (never reads mode). A future editor reading only lines 20-24
   could reintroduce the ASSERT race; the supersession is stated in the same file, and no
   edit was made here by wave rule.
2. **Stale enabled during disable.** As above, `enabled` reads the `FLAG_ON` word, which is
   cleared at S080:1406, after the runtime bit at :1367. A transient `enabled` classification
   during an in-flight disable is possible; it cannot trip an assert and is covered by the
   contract's stated race exclusion.
3. **Assert expansion not verified.** `CONFIG_BTRFS_ASSERT`/messages.h were not reopened and
   no kernel config was read; the conclusion is deliberately independent of it.
4. **Kernfs/kobject lifetime not analysed.** This seat checked only the ASSERT surface in
   S079/S080. Whether sysfs active references protect a concurrent `enabled` read against
   directory teardown is outside this question; the probe maps read failures to `None`
   (unknown), so it makes no snapshot or lifetime guarantee.
5. **No live mode read was performed**, per the wave bounds; the source reasoning above is
   static. No host sysfs, mountinfo or quota state was inspected by this seat.

## 7. Confidence

- That `qgroup_mode_show` alone asserts enabled and that `enabled` reports a different bit
  from the asserted runtime state: **high**, direct S079:2355-2395 and S080:33-45.
- That the enabled-first gate has real windows in both the disable and enable orderings:
  **high**, direct S080:1367/1403-1412 and :1032/1104/1254-1259.
- That the pinned production bytes never open `qgroups/mode` in real mode: **high**, AST
  call-site audit plus exact blob identity and measure4 hash.
- That the decision therefore makes the ASSERT unreachable from the probe: **high**,
  follows from the absence of the only path that enters that show function.

## Boundaries observed

- Read-only seat: no code edits, no frozen case/oracle/expectation edits, no lane index/jj/ref
  changes, no sibling writes. Only this report and the pre-existing scratch directory
  `/fast/scratch/hyaku/mori-r23/InspectModeSafety/` were created/used; no files were written
  there.
- No execution of the probe, oracle, selftest, driver, builds, tests, linters or gates; no
  journal/process/service/transcript/credential reads; no quota/mount/ioctl calls; no
  installs or updates (none needed).
- Kernel evidence was limited to the cached S079/S080 sources named by the wave.
