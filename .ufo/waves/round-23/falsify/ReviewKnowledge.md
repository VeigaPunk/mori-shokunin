# ReviewKnowledge — claim-vs-source audit of the round-23 quota knowledge note, mode-safety correction, registry commands and historical EDQUOT/ENOSPC statements

Seat: `MadoR22-2.ReviewKnowledge` (reviewer, leaf; no subagent dispatch).
Lane: `mori-shokunin`, round 23 attempt 1. Production pin reviewed: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`; seal `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`.
Scope of this seat (assignment): audit the **new quota knowledge note** and the **final mode-safety
correction** claim-by-claim against the pinned sources; check the **factual current registry
commands**; check the **historical EDQUOT/ENOSPC statements**; and keep **dated pinned source**
strictly separated from **live observation**.

Method: read-only. `git -C <abs> show/log/status/rev-parse/ls-tree/cat-file` only; no lane mutation,
no `jj`, no sibling write, no transcript read, no live host read, no quota tool / quotactl / ioctl /
btrfs / xfs_quota / repquota / mount call, no `df`-style capacity probe, no probe/driver execution
(my item authorizes no run), no install. Nothing was installed or upgraded, so there is no
tool/version/channel record to log. No scratch tree was needed: no deliberate probe, clone or
mutation was performed, so `/fast/scratch/hyaku/mori-r23/ReviewKnowledge/` was not created. The
only file written by this seat is this report.

---

## 1. Findings by severity

### F1 — MEDIUM — The shipped production probe misidentifies itself and cites a sibling file that does not exist

`tools/mori-quota-surface.py` opens with a candidate-era header that is factually wrong in its
shipped location:

- `tools/mori-quota-surface.py:1` — `"""mori-quota-surface-v3.py — read-only quota-surface probe (FR2 / EDQUOT).`
- `tools/mori-quota-surface.py:4-8` — "This is the round-23 **pre-seal amendment candidate** for
  contract §C2 … It is a new candidate authored alongside `mori-quota-surface.py` (the original,
  unaltered) and `mori-quota-surface-v2.py` (preserved as the rejected unsafe-read source evidence…)."

In production that path **is** `mori-quota-surface.py`; there is no `tools/mori-quota-surface-v3.py`
and no `tools/mori-quota-surface-v2.py` (`git ls-tree -r HEAD tools/` shows one quota file). The
"original, unaltered" file survives only as rejected evidence under
`.ufo/waves/round-23/build/ImplQuota/mori-quota-surface.py` (sha256 `6b55315446e2e422…`, 1376 lines),
and the shipped file's own bytes differ from every preserved candidate:

| file | lines | sha256 |
|---|---|---|
| `build/ImplQuota/mori-quota-surface.py` (v1, reads `qgroups/mode` unconditionally, line 407) | 1376 | `6b55315446e2e42288337b16ba57783fd3dfa73c07e929014c6f146e6c50926a` |
| `build/ImplQuota/mori-quota-surface-v2.py` (reads mode when enabled==1, line 592) | 1882 | `5c8b251d69dd5cb0cd86757179a70bcf7e7ca0f4c1c465d37b1190e66d3728b6` |
| `build/ImplQuota/mori-quota-surface-v3.py` (never reads mode) | 1907 | `5199e97b5ac89a39b3f047586a6e624d7e95041415390750a93f91bf15d55129` |
| **`tools/mori-quota-surface.py` (production)** | **1920** | **`e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92`** |

Production is v3 **plus** the later round-23 repairs (the `classify` unpack fix at
`tools/mori-quota-surface.py:551`, the empty-path-population and exact-path-key fixture guards at
`:711` and `:715`, the `limits` string form at `:781` and `:792`, the co-evolved
`st_dev="259:2"` selftest input at `:1537`, and the new `setup-empty-path-population` arm at
`:1778`). The preserved v1/v2/v3 copies
therefore do **not** match production, so a reader who trusts the shipped header as provenance is
sent to bytes that are not the shipped tool.

Impact: the tool that SKILL.md registers as the current quota probe describes itself as an
unlanded candidate and points at three files, none of which is where the text says. This is a
documentation/provenance defect in a production artifact, not a behaviour defect.

Actionable: replace the header with the shipped identity (`mori-quota-surface.py`, production
revision `f3dc07c0…`, sealed-input lineage `22772c1…`), and state the differences
from v3 (the repairs listed above) instead of the candidate narrative. The candidate-relative
claims that ARE true (`v2 still read the btrfs qgroups/mode attribute in real mode` — verified at
`build/ImplQuota/mori-quota-surface-v2.py:592`) can stay, but only as history.

### F2 — MEDIUM — A dated fleet EDQUOT observation is carried as an undated present-tense fact in the shipped tool

`tools/mori-quota-surface.py:51-53` states, as current fact:

> "A read-only observability probe. `df` capacity percentages cannot see quota exhaustion (FR2:
> the fleet's actually reported disk failures are quota events, EDQUOT), so this probe reports, per
> path, whether a filesystem quota mechanism is visibly enabled…"

The underlying statement is a **historical fleet observation** retained in the corpus, not a live
measurement: `corpus/knowledge/audit-r11.md:95-99` (flake-seat battery, 9 green + 1 quota-aborted
run), `:168` (F13 row) and `:216` (D21 "environmental failure retained"). The same wording at
`SKILL.md:411-413` is now explicitly reclassified by the round-23 section as dated history
(`SKILL.md:599-600`: "The old `:411` statement about fleet failures is dated historical evidence, not
a universal current failure diagnosis"), but neither the tool docstring nor `SKILL.md:411-413`
itself carries that date at the point of claim.

Impact: the note itself keeps this separation ("The historical census selftest's `Disk quota
exceeded` abort is evidence of a failed write, not an identified filesystem/mechanism/cause",
`corpus/knowledge/quota-surface-r23.md:9-11`), so the note is compliant; the *tool* and the SKILL
row are not. A future reader can read the docstring as "the fleet's disk failures are quota events"
today.

Actionable: in the tool docstring and at `SKILL.md:411-413`, mark the statement as the retained
historical census observation (anchor `corpus/knowledge/audit-r11.md:95-99,168,216`, observed in
r11) and keep the live statement as the mechanism-visibility claim the probe actually supports.

### F3 — MEDIUM-LOW — The registry table still carries a retention command the current tool rejects

`SKILL.md:538` (the r22 registry row "retention receipt reconciliation") still gives the entry
command

> `python3 tools/mori-retention-reconcile.py check --repo . --rev INPUT_COMMIT --receipt …`

The current tool rejects a relative repo: `tools/mori-retention-reconcile.py:160`
`require(isinstance(a.repo,str) and a.repo.startswith('/') …,'repo_not_absolute')` → `Invalid` →
exit **2** `RETENTION_RECONCILIATION_SETUP` with error token `repo_not_absolute`
(`tools/mori-retention-reconcile.py:286-287`). That requirement landed in **r22**
(`git log -S repo_not_absolute -- tools/mori-retention-reconcile.py` → `da40bb2` "round-22: bind repo
root, strict JSON, raw complement"), i.e. *after* the row was written at r22's `8cb4afb`
(`git show 8cb4afb:SKILL.md` line 538 already carries `--repo .`), so the row's command has been
non-functional since r22 and was re-stated, not corrected, in r23. The r23 row (`SKILL.md:585`) uses
`--repo "$PWD"` and the r23 prose states "`--repo` must be absolute (`"$PWD"`, not `.`)"
(`SKILL.md:578-579`), so the supersession is *declared* — but the stale row carries no inline marker
and sits 40+ lines above the declaration.

Impact: a reader scanning the registry table for a runnable command can pick the one that exits 2
`repo_not_absolute`. Everything else in that row (verdict map, selftest, pinned values) is still
accurate.

Actionable: annotate `SKILL.md:538` in place, e.g. "entry superseded by the r23 row below
(`--repo` must be absolute; `--repo .` now exits 2 `repo_not_absolute`)". Do not delete the r22 row:
`SKILL.md:578-579` states old evidence is not rewritten.

### F4 — MEDIUM-LOW — The quoted historical stderr embeds a line number that no longer resolves, and the lane's FR2 row points at a closure disclaimer instead of the evidence

`corpus/knowledge/audit-r11.md:96` and `:168` quote the first-hand census failure verbatim:

> `tools/mori-census.sh: line 1983: printf: write error: Disk quota exceeded`

At the current tree `tools/mori-census.sh:1983` is a comment —
`#   2 not-open     no launch/steer line for the lane` — and the census file was last modified in
round 17 (`git log --oneline -- tools/mori-census.sh` → `fe9fa90`, `2be8294`, `273aa74`). The line
number is therefore bound to the r11-era file revision, but neither `audit-r11.md`, nor the new
note that inherits the quote (`corpus/knowledge/quota-surface-r23.md:9-11`), nor `SKILL.md:411-413`
records which revision the number belongs to. The new note's framing ("The **historical** census
selftest's … abort") is correct; the *artifact* it points at is unpinned.

Related, same family: the lane's own FR2 frontier rows still cite only the closure disclaimer —
`PROVINCE.md:45` "First evidence: `corpus/knowledge/audit-r11.md:218-222`" and the mirror
`corpus/README.md:333` — where `audit-r11.md:218-222` is the paragraph "No closure is claimed for
… quota observability …", not the first-hand abort evidence (`:95-99`, `:168`) nor the D21
disposition row (`:216`).

Actionable: (a) when the historical stderr is quoted again, name the revision the `line 1983`
anchor belongs to (audit-time census revision) or drop the line number; (b) either extend the FR2
"first evidence" anchors to `:95-99,168,216` or state explicitly that `:218-222` is a
closure-disclaimer anchor. Both are documentation-only; no frozen byte changes.

### F5 — LOW — The note's tmpfs row omits the `quota` key that the shipped probe treats as enabling

`corpus/knowledge/quota-surface-r23.md:47`:

> | tmpfs usrquota/grpquota flags or one of four documented hardlimit keys | enabled, enforced | S084/S086: actual emission tied to quota initialization; never arbitrary `_hardlimit` suffix matching |

The shipped probe enables on `quota` as well: `tools/mori-quota-surface.py:217-227`
`TMPFS_QUOTA_KEYS = {"quota","usrquota","grpquota","usrquota_block_hardlimit", …}` and
`:507-508` → `("enabled","enforced","tmpfs_quota_option")`. `S084` documents exactly that key
(`build/…/S084-Documentation_filesystems_tmpfs.rst:132-134`: "quota — User and group quota
accounting and enforcement is enabled on the mount"), and `S086` emits it via
`sb_has_quota_active(USRQUOTA|GRPQUOTA)` (`S086-mm_shmem.c:4878-4881`).

Impact: a reader of the knowledge note would not predict `quota` → enabled/enforced, i.e. the note
under-describes one of the three documented tmpfs quota flags.

Actionable: change the row to "tmpfs `quota`/`usrquota`/`grpquota` flags or one of the four
documented hardlimit keys".

### F6 — LOW — The note's audit anchor range misses the D21 disposition row

The note header cites `corpus/knowledge/audit-r11.md:95-99,168,218-222`
(`corpus/knowledge/quota-surface-r23.md:1`). `:95-99` and `:168` do carry the abort and the F13
verdict, and `:218-222` carries the "no closure is claimed / inherited observability limits"
paragraph. The retained **disposition** of that abort — `| D21 audit-time quota abort | **environmental
failure retained** …` — is at `corpus/knowledge/audit-r11.md:216`, one line outside the cited range,
and it is the row that actually states "no audit cleanup/remediation" (the fence the note re-states
in prose). Actionable: extend the anchor to `:95-99,168,216-222`.

### F7 — LOW — The mode-safety consequence is stated without the severity condition the admitted sources cannot establish

`corpus/knowledge/quota-surface-r23.md:101-108` states that "S079's mode reader then ASSERTs
enabled" (`:102-103`) and that reading mode is therefore unsafe. The *code fact* is verified
(`S079-fs_btrfs_sysfs.c:2378` `ASSERT(btrfs_qgroup_enabled(fs_info));` inside `qgroup_mode_show()`),
but the admitted source set S077–S086 contains **no** btrfs `ASSERT` macro definition, so whether
that assert is a `WARN`-style print or a `BUG()` is not established by the pinned sources.
`SentinelProbe.md` states the same limitation explicitly ("`ASSERT` becomes `BUG()` with
`CONFIG_BTRFS_ASSERT=y`; this host's kernel configuration was not read and the condition is
therefore explicitly conditional"), and the tool docstring keeps the conditional wording
("can trip a kernel assert on an assert-enabled kernel", `tools/mori-quota-surface.py:13-15`).

Impact: the note's phrasing is a kernel-source statement, so it is not false; but the operational
weight ("unsafe to read") rests on an unestablished severity. Actionable (one clause): note that the
assert's severity is not established by S077–S086 and that the correction is therefore taken
unconditionally rather than as a severity-weighted decision.

---

## 2. Claims verified against the pinned sources (no finding)

| Claim | Where claimed | Verified against |
|---|---|---|
| All ten registry rows S077–S086 pin byte-identical upstream v7.2 sources | `corpus/SOURCES.md` registry rows; `corpus/knowledge/quota-surface-r23.md:1-2` | Recomputed sha256 of all ten files in `.ufo/waves/round-23/evidence/sources/` matches `.ufo/waves/round-23/evidence/sources-manifest.json` byte-for-byte and size-for-size (10/10). |
| Every registry anchor line range resolves to the claimed code/doc text | `corpus/SOURCES.md` "anchor" cells | S077 `xfs.rst:171-185` (`noquota` + u/g/p families); S078 `xfs_super.c:238-254` (`usrquota`/`uqnoenforce`/…/`noquota` emission); S079 `sysfs.c:2355-2368` (enabled), `:2370-2395` (mode + ASSERT at 2378), `:2155` (device link); S080 `qgroup.c:432-445` (dir add at 442, "default this to quota off" at 444), `:470-474`, `:612-615`, `del` at 620/689/1295; S081 `inode.c:8245-8246` (`stat->dev = BTRFS_I(inode)->root->anon_dev`); S082 `proc.rst:1965-2002` with field table 1973-1983 and "Parsers should ignore all unrecognised optional fields" at 1985; S083 `ext4.rst:261-271` ("These options are ignored by the filesystem" at 262); S084 `tmpfs.rst:129-145` (quota table + exactly four hardlimit names); S085 `proc_namespace.c:135-193` (`seq_path_root` escape set `" \t\n\\"` at 151, separator `seq_puts(m, " - ")` at 172); S086 `shmem.c:4877-4894` (quota token emission) and `:5026-5038` (quota enable + default-limit copy). |
| "S079 exposes enabled from `BTRFS_QGROUP_STATUS_FLAG_ON`" | note:20-22 | `S079:2363` ✔ |
| "S080 creates the directory before parsing that flag and can leave it initialized while quota is off" | note:21-22 | `S080:442` `btrfs_sysfs_add_qgroups(fs_info)` precedes the status read at `:470`; on disable `FLAG_ON` is cleared (`S080:1406`) after the runtime bit (`S080:1367`) ✔ |
| "S083 documents plain quota hints as ignored by the filesystem and journal options as replay configuration" | note:25-28 | `S083:262-263` and `:266-270` ✔ |
| "S082 describes mountinfo fields, not a safe last-line-wins stack algorithm" | note:60 | `S082:1973-1983`; no ordering guarantee in the text ✔ |
| "S085 shows per-mount emission and escaped path fields" | note:61 | `S085:135-193` ✔ |
| "S081 assigns a btrfs path's stat device from its subvolume root's anonymous device" | note:67-69 | `S081:8246` ✔; probe honours it via `path_device[0]==0` → `btrfs_subvolume_skipped` (`tools/mori-quota-surface.py:537-539`) ✔ |
| Component-boundary cover, never a bare prefix | note:62-63 | `tools/mori-quota-surface.py:407-418` uses `point == resolved or point == "/" or resolved.startswith(point + "/")` ✔ |
| Output never leaks mount source, UUID, option value or quota-file name | note:83-85, 89-98 | Row construction `tools/mori-quota-surface.py:513-524` emits exactly `path, fstype, mount_point, quota_state, enforcement, basis, device_check, quota_option_keys, btrfs_qgroups_mode`; `quota_option_keys` is key-only (`tools/mori-quota-surface.py:360-371`); `mount.source`/UUIDs are used only internally (`:283`, `:468-470`, `:550`) ✔ |
| tmpfs hardlimit-only inputs are unreachable on a real kernel (so "enabled" is not an over-claim) | note:47 | `S086-mm_shmem.c:4638-4672`: the four hardlimit options set only `ctx->qlimits.*`; `SHMEM_SEEN_QUOTA` is set only by `quota`/`usrquota`/`grpquota` (`:4623,4629,4635`); `sbinfo->qlimits` is copied only under `ctx->seen & SHMEM_SEEN_QUOTA` (`:5027-5034`), so a hardlimit token cannot be printed without a quota flag ✔ (the amendment's "defensive synthetic case" wording is conservative but sound) |
| The final mode-safety correction is implemented, not only documented | note:99-109; `SKILL.md:588-593` | Production reads **only** `/sys/fs/btrfs/<uuid>/qgroups/enabled` (`tools/mori-quota-surface.py:609-615`); `mode` is never opened in real mode (`:616-620`); fixture mode projects `qgroup`/`squota` only when `enabled is True` (`:761-769`) ✔ |
| The correction precedes any C2 candidate measurement | note:108-109 | Correction text landed in the note at the **seal** commit `22772c1` (12 added lines, "Final pre-seal mode safety qualification"); production landed later at `1979a9d`; first measurement evidence at `5729e7f` (`evidence/measure1`) ✔ |
| The v1→v2→v3 candidate progression matches the documented read-set change | tool docstring `tools/mori-quota-surface.py:4-8`; note:99-109 | v1 reads `qgroups/mode` unconditionally (`build/ImplQuota/mori-quota-surface.py:407`); v2 reads it only when enabled==1 (`:592`); v3 never reads it (`:609`, `:625`) — the v3 docstring's characterization of v2 is accurate ✔ |
| Registry commands are factually current | `SKILL.md:585-586` | Retention CLI flags exist (`tools/mori-retention-reconcile.py:278-279`); quota CLI flags exist (`tools/mori-quota-surface.py:821-823`, `--path` repeatable via `action="append"`); verdict tokens match the tool constants (`tools/mori-retention-reconcile.py:17-19`; `tools/mori-quota-surface.py:137,140-143`); all ten pinned-value paths referenced by the r23 rows exist (`c1-requirements.json`, `c1-source-delta.json`, `c1-expected-real.json`, `c1-expected-real-identities.json`, `oracle-rename.py`, `frozen/quota-cases/`, `frozen/c2-expected-real.json`, r21 `retention-floor.json`, r18 `c1-policy.json`, `corpus/evidence/retention-allowlist.json`) ✔ |
| The shipped retention tool differs from its r22 binding by exactly the two pre-registered transformations | `SKILL.md:568-573`; contract C1 | `git show 1979a9d -- tools/mori-retention-reconcile.py` shows exactly two changed lines: `SCHEMA='mori-retention-reconciliation-v1'` → `-v2`, and removal of the `'raw_unallowlisted':len(unallowed),` producer fragment (the `scanner_unallowlisted` value is unchanged) ✔ |
| Probe defaults match the census's canonical default pair | note:51-52; `SKILL.md:586` | `tools/mori-quota-surface.py:149-150` `DEFAULT_PATHS = (FLEET_ROOT, "/tmp")`; `tools/mori-census.sh:321` `DISK_TARGETS=${MORI_DISK_TARGETS:-"$ROOT /tmp"}` with `ROOT` = fleet root (`tools/mori-census.sh:291`) ✔ (the census pair is operator-overridable; "canonical default" is the right qualifier) |
| "The retained r21 control is 4 versus 9" | `SKILL.md:571-573` | `frozen/c1-expected-real.json` → `scanner_unallowlisted: 4`, `raw_not_allowlisted: 9`, `raw_total: 95`, `allowlisted: 86`, `policy_excluded: 5`, `scanner_total: 90`, `retention_state: red`, `privacy_clearance: false`, `schema: mori-retention-reconciliation-v2`, `forbidden_keys: ["raw_unallowlisted"]` ✔ |
| Dated frozen host observation is not presented as a permanent live claim | note:51-56; `SKILL.md:596-601` | `frozen/c2-expected-real.json` (`observed_utc: 2026-10-21`, note "Host state may change … a later differing run is a drift observation, not an oracle rewrite"); the knowledge note calls it "a dated expected observation, not a permanent disabled assertion" ✔ |
| Historical vs live separation inside the note itself | note:9-11, 51-56, 82-85 | The note labels the census abort as historical evidence of a failed write, and states that no source table or probe "retrospectively diagnoses that failure" ✔ |

---

## 3. Residual risk

1. **F1 provenance drift.** The production probe's header points at three non-production paths and
   calls itself a candidate; the preserved candidates in `build/ImplQuota/` do not match the shipped
   bytes. A future auditor comparing `tools/mori-quota-surface.py` against "the v3 candidate" will
   find a 21-line/8-line difference and must reconstruct which of them is authoritative. Low
   behavioural risk (the shipped file is the one SKILL.md registers and the one the driver measured),
   real provenance risk.
2. **F2/F4 undated live-sounding history.** Two separate places (tool docstring, `SKILL.md:411-413`)
   keep a fleet-wide EDQUOT claim in the present tense, and the quoted stderr's line anchor no longer
   resolves in the current census file. Neither is false; both invite a reader to re-derive a
   current fleet diagnosis from an r11-era observation.
3. **F3 registry hygiene.** The registry table can still hand a reader a command that exits 2
   `repo_not_absolute`. The r23 declaration covers the intent, but table-scanning readers are not
   served by a declaration 40 lines away.
4. **Severity of the btrfs assert is not source-established** (F7). The correction is taken
   unconditionally, which is the conservative choice, but the note presents the hazard without the
   "severity unknown from S077–S086" qualifier that `SentinelProbe.md` itself states.
5. **Not in this seat's remit, recorded for the parent:** `PROVINCE.md:45` and
   `corpus/README.md:333` (FR2) were not updated even though `CriticScopeProvince.md` ruled
   "IN PROVINCE, conditionally" and `build/DraftProvince.md` drafted the text; the round-23 note is
   reachable from `SKILL.md:588` but not from the lane's own frontier row. Landing a frontier
   advance while C2's strict target is UNPROVABLE is the parent's call — this is recorded as a
   decision to make explicitly, not asserted here as a defect.

## 4. Verification gaps (not closed by this seat)

- I did **not** execute `tools/mori-quota-surface.py`, `--selftest`, the pinned driver, the sealed
  oracles or the census: my item authorizes no run, and C1/C2 measurement is other seats' work. All
  tool behaviour claims above are read from source, not from execution.
- I did **not** read any host quota state: no `mountinfo`, `stat`, `sysfs` or `/proc` read for this
  report, and no live check of the frozen real control's continued truth. The frozen control remains
  a dated 2026-10-21 observation only.
- I did **not** open the btrfs `ASSERT` macro definition (not among S077–S086); F7's severity gap is
  therefore left open by design rather than resolved.
- I did **not** compare the sealed C2 case expectations against the shipped tool's outputs (the
  `CaseEscapedSpace` strict red and the `29/30` coverage position are outside this seat's scope and
  remain as Main framed them).
- I did **not** audit `corpus/knowledge/quota-surface-r23.md` against the *seal manifest*
  dependency digests (seal-manifest.json hashing is another seat's scope), nor the r22 knowledge
  note's cutover text beyond the field-name correction already verified above.
- No transcript, session, credential or `agent.db` access; no `/fast/scratch` tree was needed.
