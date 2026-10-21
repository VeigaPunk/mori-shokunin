# QBtrfsUnmapped — round-23 C2 falsification of the sealed case `CaseBtrfsUnmapped`

Seat `MadoR22-2.QBtrfsUnmapped` · role reviewer (leaf, no dispatch) · wave `round-23` · axis **C2 coverage (FR2 quota/EDQUOT observability)**.
Scope executed: **exactly one** sealed C2 case, in **fixture mode only**. No real-mode run, no other case, no host quota read, no production/frozen/oracle edit.

## Pins and identities

| item | value |
|---|---|
| lane | `/home/vgpnk/Projects/shokunin/mori-shokunin` |
| production pin | `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` |
| expectation seal | `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687` |
| repo HEAD (observed) | `6eb889c037163e4886eaa61501258910d6a529b9` |
| case file | `.ufo/waves/round-23/frozen/quota-cases/CaseBtrfsUnmapped.json` |
| case sha256 | `1986ade4a150637c62102316fcec8c55523919d35c377759a5908d1e682e59b1` (4980 bytes) — identical to `frozen/seal-manifest.json` entry and to `cases-corrected/CaseBtrfsUnmapped.json` |
| original proposal (preserved) | `cases-proposed/CaseBtrfsUnmapped.json`, sha256 `c8796c446b4ab21dbc3a328ed309ceec855b17cf7318593c679ac13504244015` |
| candidate executable | `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py`, sha256 `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92`; git blob `439ff4c1a68fc4f98182c6b855b3b4c790286851` **identical at HEAD and at the pinned production revision** |
| sealed oracle | `.ufo/waves/round-23/oracle-quota.py`, sha256 `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec` |
| scratch (all deliberate work) | `/fast/scratch/hyaku/mori-r23/QBtrfsUnmapped/` |

## What was read (source derivation chain)

- `.ufo/waves/round-23/contract.md` (C2 table + fixture format), `.ufo/waves/round-23/preseal-amendment.md` (C2 superseding clauses: btrfs `qgroups_enabled`, device-mismatch preemption, ambiguous-overmount + parent-ID rule, raw-source `device_links` lookup, trailing-line rule, xfs/tmpfs/ext rules).
- The sealed case, its preserved original proposal, `.ufo/waves/round-23/build/CaseBtrfsUnmapped.md` (wave-1 author report, incl. its own A1–A6 / N1–N4 ambiguity notes), `.ufo/waves/round-23/frozen/case-decisions.json` (decision: `cases-corrected/…` selected, `primary: true`, reason "Independent source-derived pre-measurement correction").
- Source rows S079–S082 via `.ufo/waves/round-23/evidence/sources-manifest.json`: S079 `fs/btrfs/sysfs.c` (uuid `qgroups` attrs, `devices` kobject links), S080 `fs/btrfs/qgroup.c` (qgroups sysfs group lifecycle), S081 `fs/btrfs/inode.c` (`anon_dev` → per-subvolume anonymous `st_dev`), S082 `Documentation/filesystems/proc.rst` §3.5 (mountinfo grammar).
- Selected quota implementation `tools/mori-quota-surface.py` (parser, resolver, btrfs classifier, fixture loader) and the sealed oracle's own evaluation logic.

## The single invocation

Fixture copied verbatim from `case["fixture"]` into my own scratch file `fixture.json` (sha256 `948ab41e43df29b80857ea0e9e63629a721320cc12f1b881751cbe4888c35c2c`, 1066 bytes, semantically identical to the frozen fixture — verified by parse-and-compare).

```
given argv : python3 -I <TOOL> --fixture /fast/scratch/hyaku/mori-r23/QBtrfsUnmapped/fixture.json
actual argv: timeout -k 2 15 prlimit --as=402653184 --cpu=15 -- python3 -I <TOOL> --fixture <ABS_FIXTURE>
exit       : 2          timeout_hit: false
stdout     : 977 bytes, sha256 3db97edbe189ac2bf00d3d562d7dd63c8e867032abe5bde12b78b12384ffbc20
stderr     : empty (0 bytes), sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
```

One child only, one tool invocation only. Fixture mode opens exactly one file (the fixture); `/proc/self/mountinfo`, `/sys/fs/btrfs`, `quotactl`, `btrfs qgroup`, `xfs_quota`, `repquota` and mount tooling were never invoked and no real-mode path was probed.

## Given vs actual

Primary (the sealed six-field denominator), ordered tuples in the sealed field order `path, fstype, mount_point, quota_state, enforcement, basis`:

| tuple | given | actual |
|---|---|---|
| exit | `2` | `2` ✅ |
| finding_id | `QUOTA_STATE_UNKNOWN` | `QUOTA_STATE_UNKNOWN` ✅ |
| row 1 | `/srv/data/store, btrfs, /srv/data, unknown, n/a, btrfs_device_unmapped` | `/srv/data/store, btrfs, /srv/data, unknown, n/a, btrfs_device_unmapped` ✅ |

Row count 1/1, order preserved. **Ordered six-field tuples match exactly.**

Supplementary metadata (reported separately, never folded into the six-field denominator):

| field | given (case rationale, prose) | actual |
|---|---|---|
| `device_check` | `btrfs_subvolume_skipped` | `btrfs_subvolume_skipped` ✅ |
| `quota_option_keys` | `[]` | `[]` ✅ |
| `btrfs_qgroups_mode` | `null` | `null` ✅ |

Output shape: `schema=mori-quota-surface-v1`, `exit_code=2`, `df_covers_quota=false`, top-level keys exactly `{df_covers_quota, exit_code, finding_id, limits, paths, schema}`, path row keys exactly the nine documented ones. Leak scan of stdout: `squota`, `dm-0`, `dm-1`, `dm-9`, `/dev/mapper`, `vault`, `1d02a454`, `b3f1c7d2`, `zstd`, `@vault`, `usrquota`, `noquota` — **all absent**; the decoy uuid's `squota` mode and the unmapped device basename never reach the output.

Sealed-oracle verdict, obtained by applying `oracle-quota.py`'s own `evaluate_case()` to the observed stdout (no second tool run): `ok=true`, headline `exit_match/finding_match/paths_match = true`, `reason=null`, supplementary `9 total / 9 pass / 0 unmet` (schema, exit_consistency, output_keys_allowed, output_key_set, error_token, path_key_set, df_covers_quota, limits_text, no_leakage).

**Verdict for this case: PASS at the pinned production revision.** No implementation defect found for `CaseBtrfsUnmapped`.

## Findings by severity

### F1 — MEDIUM (seal-side coverage gap, not a tool defect): the case's supplementary claims are prose-only and are not machine-enforced

`frozen/quota-cases/CaseBtrfsUnmapped.json` has no `supplementary_expected` block (top-level keys are exactly `schema, id, scenario, fixture, expected, rationale, sources`). The oracle's `read_supplementary()` therefore yields an empty `per_index`, and `supplementary_checks()` asserts no per-path value at all for this case: `device_check`, `quota_option_keys` and `btrfs_qgroups_mode` — the three values the case's own `rationale` states under `SUPPLEMENTARY` — are never compared by the sealed harness. The case author flagged the same gap before the seal (their N3 and A5).

Demonstrated, not asserted: I applied the sealed oracle's `evaluate_case()` to in-memory mutations of the observed stdout (no repo/frozen byte touched, no extra tool run):

| in-memory mutation of the observed output | sealed-oracle verdict |
|---|---|
| `device_check` → `mismatch` (btrfs subvolume skip lost) | **still `ok=true`, 0 supplementary unmet** |
| `btrfs_qgroups_mode` → `"squota"` (decoy mode leak) | **still `ok=true`, 0 supplementary unmet** |
| `quota_option_keys` → `["usrquota"]` (btrfs claims an option quota) | **still `ok=true`, 0 supplementary unmet** |
| `quota_state` → `disabled` | caught (`paths_match=false`) |
| `mount_point` → `/` (wrong longest-cover rule) | caught (`paths_match=false`) |
| `basis` → `btrfs_qgroups_dir_absent` (decoy uuid consulted) | caught (`paths_match=false`) |
| extra key in a path row / uuid leaked in a value | caught (`path_key_set`, `no_leakage` unmet) |

So the six-field headline for this case is genuinely discriminating (the three classic wrong implementations — wrong cover, decoy-uuid leakage, defaulting an unmappable device to disabled — are all caught), but three of the amendment's "supplementary sealed checks" are unenforced here. `frozen/quota-cases/CaseBtrfsDevMatch.json` already ships a machine-readable `supplementary_expected`; **only 1 of 30 sealed cases does**, so this is a seal-wide pattern, not a single-case slip.

Recommendation (contract owner / L1, not applied by me — frozen bytes must stay unchanged): add `supplementary_expected` to the remaining 29 cases (or have the oracle derive `device_check`/`quota_option_keys`/`btrfs_qgroups_mode` from the amendment). Until then, `CaseBtrfsUnmapped` cannot be cited as machine-proof of `device_check=btrfs_subvolume_skipped` or of the decoy-mode non-leak; my run confirms the shipped tool does produce those values, but the harness would not notice if it stopped doing so.

### F2 — LOW (token overloading, real-mode only; out of this case's scope): `btrfs_device_unmapped` conflates three different causes

The contract table uses `btrfs_device_unmapped` for "zero **or several** uuids list the device" (missing mapping and ambiguous mapping), and `tools/mori-quota-surface.py:465-486` additionally returns it when a *matched* uuid's qgroups state could not be inspected (`qgroups is None`, the real-mode permission/listing-error path). The verdict is `unknown`/`n/a` in all three, which satisfies the amendment's "a parent sysfs permission/listing error is unknown, NEVER absent/disabled", but the token no longer distinguishes "device not mapped" from "mapping ambiguous" from "mapping present but uninspectable". In **fixture** mode this branch is unreachable (`load_fixture` requires `type(qgroups) is bool`), so it does not affect `CaseBtrfsUnmapped`; it is a real-mode readability loss, and it is the same overload the wave-1 author recorded as A4. No change proposed to the frozen token.

### F3 — LOW (production provenance/readability): the shipped tool's own header still describes itself as a pre-seal candidate

`tools/mori-quota-surface.py` opens with `"""mori-quota-surface-v3.py — read-only quota-surface probe (FR2 / EDQUOT).` and states "This is the round-23 pre-seal amendment candidate … with the pre-seal source safety correction applied", referring to sibling files "mori-quota-surface.py (the original, unaltered)" and "mori-quota-surface-v2.py (preserved as the rejected unsafe-read source evidence)". The shipped filename is `mori-quota-surface.py`, and production has since diverged from the referenced v3 candidate (`.ufo/waves/round-23/build/ImplQuota/mori-quota-surface-v3.py`, sha256 `5199e97b5ac89a39b3f047586a6e624d7e95041415390750a93f91bf15d55129`) by five post-seal edits: the classifier-result unpacking repair, the strict path-entry key set, the nonempty-path requirement, `limits` as a joined string, and the co-evolved selftest `st_dev` correction. The referenced "original"/"v2" variants exist only under `.ufo/waves/round-23/build/ImplQuota/`, never under `tools/`. A reader of the shipped artifact cannot tell from its own header which bytes are production. No behavioural effect; it does weaken traceability of the sealed→production delta.

### F4 — LOW (pre-existing contract design, no harness impact): exit code 2 is overloaded

The tool's own OUTPUT contract gives exit 2 to both `QUOTA_STATE_UNKNOWN` and `QUOTA_SETUP`. This case asserts exit **and** `finding_id`, so it is unambiguous here, and the sealed oracle checks `finding_id` as well; but any downstream consumer keying on the exit code alone cannot distinguish "could not determine" from "could not even parse the input". Informational only; no change recommended inside this wave.

### F5 — INFO: why the post-seal repair matters for this case specifically

The pre-seal v3 candidate line `state, enforcement, basis, mode = classify(...)` unpacks a 2-tuple into 4 names; `classify()` returns `((state, enforcement, basis), mode)`. Against that candidate every fixture case would raise `ValueError` inside `main()`'s guarded handler and answer `QUOTA_SETUP` (exit 2) — i.e. **all** C2 cases would be red, not just one. The production repair (committed in `5729e7f`, "repair classifier result unpacking and retain initial red measurement") is what makes the sealed verdict observable at all; at the pinned `f3dc07c` the case matches exactly. Worth stating because the sealed v3 candidate bytes are otherwise the natural "before" reference.

## Residual risk and verification gaps

- **Single invocation, no repeat.** I executed the tool exactly once (one child, 384 MiB AS, 15 s timeout, no timeout hit). Determinism for this case is therefore argued from construction (fixture mode: no clock, no randomness, no network, no host state) rather than re-measured; no second run was made, per the one-invocation bound.
- **Supplementary values are seat-observed, not harness-asserted** (F1). My `device_check=btrfs_subvolume_skipped`, `quota_option_keys=[]`, `btrfs_qgroups_mode=null` readings come from my own inspection of the stdout and from the sealed oracle's generic checks, not from a per-field assertion in the sealed case.
- **The C2 strict target stays UNPROVABLE at 29/30 — untouched by this seat.** The frozen contradiction (`evidence/frozen-contradiction.json`) is the `CaseEscapedSpace` case: selected mount id 43 with parent id 33 vs the longest strictly shorter cover id 42 at `/srv`, which the sealed parent-ID rule requires to be refused as `unknown/n/a/ambiguous_overmount` while the frozen expectation says `xfs /srv/my data / enabled / enforced / xfs_quota_option`. I did **not** execute `CaseEscapedSpace` (out of scope: one case only) and it is not excused, excluded, relabelled or special-cased by anything in this report. My case's topology does not touch that rule: its covering mount points `/` (id 28) and `/srv/data` (id 36) are distinct, and the selected mount's parent id 28 is present in the snapshot and *is* the id of the longest strictly shorter cover, so no refusal fires.
- **No live host observation backs this fixture.** Device names, uuids, mount lines and `st_dev` are synthetic; the case is a behavioural fixture, not a reproduction of this host's quota state. Nothing here is clearance, health, admission or baseline acceptance, and no probe visibility is claimed as such.
- **C1 untouched.** This seat ran no C1 arm; the alias/schema cutover claims and the open debt (four unallowlisted hits, permission RED 11/12, two unknown dispositions, blocked baseline acceptance, `privacy_clearance=false`) are unchanged by this seat.
- **S-id binding.** The case's `sources` array (`S079–S082`) maps to the rows in `evidence/sources-manifest.json`; the expectation itself derives from the contract table, not from the S-ids, so a registry remap cannot move the expectation.

## Constraint compliance

- One tool invocation, one child at a time, `prlimit --as=402653184 --cpu=15` + `timeout 15`, fixture mode only; no live host reads, no quota tooling, no `/sys/fs/btrfs` or `/proc/self/mountinfo` read, no mount/remediation.
- No production, frozen-case, oracle or contract byte was modified; frozen case sha256 unchanged (`1986ade4…`); the only writes are this report, the named receipt `falsify/QBtrfsUnmapped/scan.json`, and my own scratch under `/fast/scratch/hyaku/mori-r23/QBtrfsUnmapped/`.
- No subagent dispatch, no background job, no build/lint/test/formatter/gate/smoke run; no tool installed or updated (no pacman/uv/cargo/npm action), so there is no tool/version/channel record to report.
- All paths above are absolute; wave-relative names resolve under `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23`.

**Receipt:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/falsify/QBtrfsUnmapped/scan.json` (sha256 recorded below by the writer).
**Scratch:** `/fast/scratch/hyaku/mori-r23/QBtrfsUnmapped/` (`fixture.json`, `stdout.txt`, `stderr.txt`, `discriminating-power.txt`).

Report: .ufo/waves/round-23/falsify/QBtrfsUnmapped.md
