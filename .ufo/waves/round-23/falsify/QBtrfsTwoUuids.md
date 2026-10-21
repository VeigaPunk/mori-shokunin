# Round-23 falsification report — seat `QBtrfsTwoUuids` (C2 sealed case `CaseBtrfsTwoUuids`)

Seat: `MadoR22-2.QBtrfsTwoUuids` (lane leaf, no dispatch).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Production pinned: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` · expectation seal: `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`.
Receipt: `.ufo/waves/round-23/falsify/QBtrfsTwoUuids/scan.json`.
Scratch (all deliberate scratch under the latest operator directive): `/fast/scratch/hyaku/mori-r23/QBtrfsTwoUuids/`.

---

## 1. Verdict for this seat's one case

**`CaseBtrfsTwoUuids` MATCHES the sealed expectation — no new failure. The wave-level red is retained and is *not* excused (see §6).**

| dimension | given (sealed `expected`) | actual (measured) | equal |
|---|---|---|---|
| exit | `2` | `2` | yes |
| `finding_id` | `QUOTA_STATE_UNKNOWN` | `QUOTA_STATE_UNKNOWN` | yes |
| path count | 1 | 1 (0 missing, 0 extra) | yes |
| ordered six-field tuple | `("/srv/data/store","btrfs","/srv/data","unknown","n/a","btrfs_device_unmapped")` | `("/srv/data/store","btrfs","/srv/data","unknown","n/a","btrfs_device_unmapped")` | yes |

The six primary fields are exactly `(path, fstype, mount_point, quota_state, enforcement, basis)` — the same order and the same tuple-equality semantics as the sealed oracle (`oracle-quota.py:57` `PATH_KEYS`, `:329-331` `headline["paths_match"] = [tuple(...) for observed] == [tuple(...) for expected]`). Field-level diff is empty (`field_mismatches: {}`).

### Supplementary metadata — reported separately, never folded into the primary denominator

Observed (not scored by this case file, which carries no `supplementary_expected` block):

- `device_check`: `btrfs_subvolume_skipped`
- `quota_option_keys`: `[]`
- `btrfs_qgroups_mode`: `null`

These are recorded in the receipt under `comparison.per_path[0].supplementary_actual` and are **not** part of the six-field verdict. The primary denominator is untouched by them.

---

## 2. What was read (evidence base)

- `.ufo/waves/round-23/contract.md` — §C2 (probe, fixture format, mount resolution, quota table, verdict precedence, output schema, limits).
- `.ufo/waves/round-23/preseal-amendment.md` — the C2 superseding rules (btrfs `qgroups_enabled` member, device-mismatch preemption, mount parent-ID refusal, fixture source resolution, tmpfs/ext/xfs precedence, fixture validation, primary-vs-supplementary separation).
- `.ufo/waves/round-23/frozen/quota-cases/CaseBtrfsTwoUuids.json` — the sealed case (schema `mori-quota-case-v1`, keys `schema,id,scenario,fixture,expected,rationale,sources`; sources `["S079","S080","S081","S082"]`).
- `.ufo/waves/round-23/build/CaseBtrfsTwoUuids.md` — the wave-1 source derivation (author seat `MadoR22-2.CaseBtrfsTwoUuids-8`), including its "why both claimants agree on `qgroups`" argument and the corrected derivation.
- `tools/mori-quota-surface.py` — the production implementation executed (read-only; not edited).
- `.ufo/waves/round-23/oracle-quota.py` — only to confirm comparison semantics (`:57-63` key sets, `:103-164` canary/leakage rules, `:299-339` case evaluation). The oracle was **not** executed.
- `.ufo/waves/round-23/frozen/seal-manifest.json`, `.ufo/waves/round-23/evidence/frozen-contradiction.json`, `.ufo/waves/round-23/evidence/quota-selftest-corrected.json`.

### Derivation re-checked against the sealed bytes (independent of the tool)

1. Realpath `/srv/data/store`. Covering mount points in the fixture mountinfo: `/` (btrfs `/@root`, id 24) and `/srv/data` (btrfs `/@data`, id 36, major:minor `0:44`). Longest component-prefix wins → `mount_point /srv/data`, `fstype btrfs`. `/proc` and `/tmp` are not prefixes.
2. No covering mount point occurs twice → the amendment's `ambiguous_overmount` refusal does not apply. Parent-ID check: the selected mount's `parent_id` is `28`, which is **not** a mount id present in the snapshot (`23,24,30,36`); per the amendment a missing parent id is unknown topology and triggers no refusal. (Had `28` been a *present* id that was not the longest strictly shorter cover, the rule would have refused the row — it is not, so the row stands.)
3. Device check: `fstype` is btrfs and the path's `st_dev` major is `0` → the btrfs equality skip applies (S081 `fs/btrfs/inode.c:8246 stat->dev = BTRFS_I(inode)->root->anon_dev`), so `0:44 ≠ 0:57` is `btrfs_subvolume_skipped`, not `device_mismatch`. The row therefore reaches the filesystem table.
4. Fixture source resolution: raw decoded source `/dev/dm-3` → `device_links` → basename `dm-3`; **two** uuids (`a7c3e9d1-…`, `f2b5d804-…`) list `dm-3` in their `devices` arrays → the "zero or several uuids list the device" row → `unknown` / `n/a` / `btrfs_device_unmapped`. The third uuid (`3e8a1c47-…`, `dm-0`, `qgroups:false`) is a decoy on another device.
5. Verdict precedence: no setup error, no `enabled` path, one `unknown` path → exit `2`, `QUOTA_STATE_UNKNOWN`.

This matches the sealed `expected` block field-for-field.

---

## 3. The one invocation (fixture mode only)

Real mode was **never** invoked. No quota tool (`quotactl`, `btrfs qgroup`, `xfs_quota`, `repquota`), no mount/remount, no `df`, no privileged or mutating interface was called. `--fixture` mode opens only the fixture file.

```
argv: ["/usr/bin/prlimit", "--as=402653184", "/usr/bin/timeout", "-s", "KILL", "15",
       "/usr/bin/python3", "-I",
       "/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py",
       "--fixture", "/fast/scratch/hyaku/mori-r23/QBtrfsTwoUuids/fixture.json"]
cwd:  /fast/scratch/hyaku/mori-r23/QBtrfsTwoUuids
env overrides: TMPDIR=/fast/scratch/hyaku/mori-r23/QBtrfsTwoUuids, PYTHONHASHSEED=0, PYTHONDONTWRITEBYTECODE=1
limits: address space 402653184 B (384 MiB), wall clock 15 s, kill signal KILL
```

- exit: **2** · stdout: 977 bytes, valid single JSON object · stderr: **empty** (`""`)
- stdout sha256 `3db97edbe189ac2bf00d3d562d7dd63c8e867032abe5bde12b78b12384ffbc20` · stderr sha256 `e3b0c442…` (empty)

### Hashes (byte identities)

| artefact | sha256 |
|---|---|
| sealed case `frozen/quota-cases/CaseBtrfsTwoUuids.json` | `6bdcea63cf12d1d63e82e6cbaca827c3e00729dfd016f28331d260d6f0e7328c` |
| executed tool `tools/mori-quota-surface.py` (working tree) | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| same file as git blob at the pinned production revision `f3dc07c` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` (identical) |
| my copied fixture `fixture.json` | `5fb0ef10086eb80c401e8bb9bd89e490e1c10d50e06382acb94ffb8e84bbe014` |

- The case hash equals the `seal-manifest.json` entry for that path (`6bdcea63…`, 6839 bytes) and `git cat-file -p 22772c1:…/CaseBtrfsTwoUuids.json | sha256sum` — i.e. the sealed case bytes are **unchanged** at the pin and in the working tree. `git diff 22772c1 HEAD -- …/CaseBtrfsTwoUuids.json` is empty. Expected bytes were not edited.
- `git diff --stat f3dc07c HEAD -- tools/` is empty: the working-tree tool is byte-identical to production at the pin, which is what was executed.
- `git merge-base --is-ancestor 22772c1 f3dc07c` → true (seal is a strict ancestor of the executed production), and `git cat-file -p 22772c1:tools/mori-quota-surface.py` is empty (the quota production path was absent at seal, as the contract requires).
- `fixture.json` is `case["fixture"]` copied verbatim (only JSON re-serialisation: `json.dumps(..., sort_keys=True, indent=2)`); the tool received the exact sealed fixture object.

### Honest note on a discarded harness attempt

The first wrapper attempt added `--nofile=256 --nproc=64` on top of the specified limits. `RLIMIT_NPROC` is counted per real user across all threads, so the wrapper could not fork: `timeout: fork system call failed: Resource temporarily unavailable`, exit **125**, empty stdout, and **the tool never started**. This is recorded verbatim in the receipt under `harness_notes.discarded_first_wrapper_attempt` (marked `tool_started: false`, `classification: "harness error, NOT a tool measurement"`). The measurement above is the only run in which the tool executed; it applied exactly the specified 384 MiB address space and 15 s timeout.

---

## 4. Output discipline checks (independent replication of the sealed oracle's rules)

The oracle's leakage-canary rules (`oracle-quota.py:103-164`) were re-implemented in this seat's own scratch script (the oracle module was **not** imported or executed) and applied to the captured stdout:

- Canary set derived from the fixture: 22 canaries — 3 btrfs UUIDs, 3 mount sources (`/dev/dm-0`, `/dev/dm-3`, `/dev/nvme0n1p1`), 12 `key=value` super-option tokens, 4 distinctive option values (`/@data`, `/@root`, `zstd:3` ×2).
- **Leakage hits: 0.** No UUID, no mount source, no device basename (`dm-0`, `dm-3`), no option token or option value appears in stdout. The only occurrences of the substring `qgroup` are the fixed `limits` prose and the output key name `btrfs_qgroups_mode` — not fixture data.
- Top-level output keys are exactly `{schema, finding_id, exit_code, paths, df_covers_quota, limits}` — the sealed `OUTPUT_KEYS` set, with **no** `error` token (correct: this is not a `QUOTA_SETUP` verdict).
- Each path row carries exactly the nine allowed keys `{path, fstype, mount_point, quota_state, enforcement, basis, device_check, quota_option_keys, btrfs_qgroups_mode}`; `df_covers_quota` is `false`; `limits` is nonempty; `exit_code` (2) is consistent with the process exit (2).
- The fixture is well-formed under the amendment's strict validation: exact top-level key set, one path with the exact path key set, canonical `st_dev` `0:57`, canonical UUID keys, plain basenames, `qgroups:false` paired with `qgroups_enabled:null`/`qgroups_mode:null`, `qgroups:true` paired with `qgroups_enabled:true`/`qgroups_mode:"qgroup"`, no duplicated covering mount point. The tool therefore took the verdict path, not the setup path.

---

## 5. Discriminating power of the case (static, from the executed source)

Read from the executed tool, `tools/mori-quota-surface.py`:

- `classify_btrfs` (`:465-486`): the claimant set is built by scanning every uuid whose `devices` contains the resolved basename; `if len(matched) != 1: return ("unknown","n/a","btrfs_device_unmapped"), None`. The several-claimants condition is therefore decided *before* any per-claimant `qgroups`/`enabled` reading.
- `evaluate` (`:513-560`): the row reaches `classify` only after the btrfs stat-major-0 equality skip, and `btrfs_qgroups_mode` is left `null` on the several-claimants branch.
- `verdict` (`:561-568`): `enabled` beats `unknown`; with no enabled path and one unknown path → `RC_SETUP` (2) + `QUOTA_STATE_UNKNOWN`.

Consequence: the case is a real trap, not a tautology. An implementation that resolves the device to the **first** or **last** matching uuid would take the `enabled` branch (both claimants carry `qgroups:true`/`qgroups_enabled:true`) and emit `quota_state=enabled`, `basis=btrfs_qgroups_enabled` — a mismatch against the sealed `unknown`/`btrfs_device_unmapped`. An implementation that counts claimants *after* filtering by `qgroups` would likewise see two `qgroups:true` claimants and still land on `unknown`, so the sealed expectation is robust to the count-vs-filter ambiguity the wave-1 author flagged (build/CaseBtrfsTwoUuids.md, "Why both claimants carry `qgroups: true`"). The measured production tool agrees with the sealed expectation on the count-first reading.

I did **not** execute a mutant (that would need a scratch clone and a mutation run, neither of which this seat's item authorises), so this paragraph is source-level reasoning, clearly labelled as such, not an executed mutation result.

---

## 6. `CaseEscapedSpace` — retained red, not excused

The wave's known strict red is **CaseEscapedSpace**, not this case. From `evidence/frozen-contradiction.json` (schema `mori-r23-frozen-oracle-contradiction-v1`, seal `22772c10…`):

- sealed expected: exit `1`, `QUOTA_ENABLED`, with `/srv/my data/sub dir` → xfs `/srv/my data`, `enabled`/`enforced`/`xfs_quota_option`;
- the sealed parent-ID rule requires instead `unknown`/`n/a`/`ambiguous_overmount` with `fstype: null`, `mount_point: null`, `device_check: not_checked` (selected mount id `43`, parent id `33`, longest strictly shorter cover `/srv` id `42`, parent present in the snapshot);
- actual at the measured revision: exit `2`, `QUOTA_STATE_UNKNOWN`, first path `ambiguous_overmount` — a strict red against the frozen expectation;
- population at that measurement: **29/30** (primary 26/27, supplemental 3/3), with the single failure being this case;
- disposition on record: keep both the expected output and the parent-ID rule unchanged — no exception, no special case, no exclusion, no relabelling.

This seat **did not run** CaseEscapedSpace (my item authorises exactly one fixture-mode case: `CaseBtrfsTwoUuids`) and did not re-derive or modify it. I restate it here so the red stays visible and unreduced: the wave-level strict C2 target remains **UNPROVABLE at 29/30**, and my case adds **no** additional failure to that population. The separate quota selftest arm (`evidence/quota-selftest-corrected.json`: `{"arms":49,"exit_code":0,"finding_id":"QUOTA_SELFTEST_OK"}` at revision `f3dc07c`) is a **different** arm and must not be conflated with the frozen `CaseEscapedSpace` red.

Also confirmed: the tool delta between the population's measured revision `5729e7ff…` and the pinned production `f3dc07c` is confined to fixture-validation tightening (`paths` nonempty; exact path-record key set) and to `--selftest` arm corrections (`/srv data` arm's `st_dev`; two new setup arms). It does **not** touch mount resolution, the parent-ID refusal rule, `classify_btrfs` or the verdict precedence — so the population result measured at `5729e7f` is not invalidated by the pin, and this case's measurement at the pin is consistent with it.

---

## 7. Findings by severity

No blocking or major finding for this seat's case.

- **[info] `CaseBtrfsTwoUuids` is confirmed green at the pinned production revision** — exit `2`, `QUOTA_STATE_UNKNOWN`, six-field tuple identical to the sealed expectation, no leakage, no extra/missing rows.
- **[info] The wave's strict red remains exactly one case (`CaseEscapedSpace`), retained and unexcused**, so the strict C2 coverage target stays unprovable at 29/30. My measurement neither advances nor reduces that count; it is an independent confirmation of one of the 29 passes.
- **[minor, inherited from the case author] The case pins an output, not a branch.** `unknown`/`n/a`/`btrfs_device_unmapped` is also what a (wrong) implementation that refused to read `qgroups/enabled` for a present-but-disabled qgroups group would emit. This single row therefore cannot distinguish "several claimants" from "enabled attribute unreadable"; that discrimination lives in the sibling btrfs cases, not here. Recorded as residual risk, not as a defect of the sealed case.
- **[minor, inherited] The disagreeing-claimant variant (one claimant enabled, one disabled) is not sealed** — the wave-1 author deliberately left it unwritten because its expectation depends on the contract owner's count-vs-filter reading. It remains a coverage gap in the sealed population, unchanged by this report.

## 8. Residual risk and verification gaps

- One invocation, one seed: no repeat run of the same case, so the result is a single observation (the tool is deterministic — no clock, no randomness, no host state in fixture mode — but I did not demonstrate that empirically).
- No real-mode arm was executed by this seat (out of scope: real mode would read `/proc/self/mountinfo` and `/sys/fs/btrfs`); the frozen real control `frozen/c2-expected-real.json` is therefore unverified by me.
- The sealed oracle (`oracle-quota.py`) was read but not executed here, so my comparison is a faithful re-implementation of its semantics (six-field ordered tuples, exit, `finding_id`, key sets, canary leakage) rather than a run of the sealed driver. The wave's `RerunPinnedDriver` seat owns the full-driver execution and its expected exit `1`.
- The mutation claim in §5 is source-level reasoning, not an executed mutant; no mutation clone was created and no mutation run was performed.
- Only the `btrfs_device_unmapped` basis token was exercised here. The sibling tokens in the btrfs table (`btrfs_qgroups_enabled`, `btrfs_qgroups_disabled`, `btrfs_qgroups_enabled_unavailable`, `btrfs_qgroups_dir_absent`) are outside this seat's scope.

## 9. Bounds and tooling compliance

- Wrote exactly two lane paths: this report and `.ufo/waves/round-23/falsify/QBtrfsTwoUuids/scan.json` (the assigned receipt). No other lane, fleet, production, frozen, oracle or source file was touched; no git/jj mutation in the lane; no sibling seat was written to.
- No live host quota read of any kind: the only file opened by the tool was my own scratch fixture. No `quotactl`/ioctl, no `btrfs`/`xfs_quota`/`repquota`, no `mount`, no remediation, no real qgroup mode or limit read.
- No build, test, linter, formatter, gate, smoke run, driver run, or `--selftest` execution was performed. One fixture-mode invocation of the candidate was performed, as explicitly authorised by my item.
- No session transcript was read (this wave permits none). No credential/auth/config file, no `agent.db`, no journal/journalctl, no process/session probe, no history/Documents read.
- No tool was installed or updated by this seat: the run used the pre-installed `/usr/bin/prlimit`, `/usr/bin/timeout` and `/usr/bin/python3` (Python 3.14.8). Nothing to record in the install ledger.
- Scratch discipline: all deliberate scratch under `/fast/scratch/hyaku/mori-r23/QBtrfsTwoUuids/` (`run.py`, `fixture.json`, `stdout.txt`, `stderr.txt`); no `/tmp` use; `TMPDIR` pinned to that directory.
