# QXfsConflict — falsification of sealed C2 case `CaseXfsConflict`

Seat `MadoR22-2.QXfsConflict` · wave round-23 · claim C2 (quota visibility, `tools/mori-quota-surface.py`)
Receipt: `.ufo/waves/round-23/falsify/QXfsConflict/scan.json` (sha256 `67fbb134cab9aa2fc7b266ec31141f7fc7b30ee7e3cadc7c07512f7f4855e691`)

## Verdict

**MATCH — the sealed expectation is reproduced exactly. No falsification of the tool on this case.**

The tool did **not** report `enabled` (usrquota present) and did **not** report `disabled` (noquota present);
it took the conflict branch and returned `unknown / n/a / xfs_conflicting_quota_options` for both probed
paths, exit 2, `finding_id` `QUOTA_STATE_UNKNOWN`. Exit code, finding id and the ordered six-field tuples
all equal the frozen expected bytes. No mismatch to report for this case.

## 1. Identity and binding (byte evidence)

| item | path | sha256 |
|---|---|---|
| sealed case | `.ufo/waves/round-23/frozen/quota-cases/CaseXfsConflict.json` | `84dfae8db5f4803e58e82be92d2ac07d321c98214f1a29fee9f844e9d3c56680` |
| case-decisions selection | `frozen/case-decisions.json` → `decisions[id=CaseXfsConflict].selected_sha256` | `84dfae8d…c56680` — **matches the frozen bytes** |
| original proposal (rejected shape, preserved) | `.ufo/waves/round-23/cases-proposed/CaseXfsConflict.json` | `197388a69be4e3c483d853c4a400fed7adc57f5ae972dff9047758f33bb4dab1` |
| selected source (identical bytes to the frozen copy) | `.ufo/waves/round-23/cases-corrected/CaseXfsConflict.json` | `84dfae8d…c56680` |
| candidate tool (worktree) | `tools/mori-quota-surface.py` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` |
| same tool at pinned production `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` | `git show f3dc07c:tools/mori-quota-surface.py` | `e4857413…f7e92` — **byte-identical to the worktree** |
| my fixture copy | `/fast/scratch/hyaku/mori-r23/QXfsConflict/fixture.json` | `289b803e2dd531a204a4de08355dd1ffd748cc790d719e14b89b950880562c63` |

HEAD is `6eb889c037163e4886eaa61501258910d6a529b9` ("pin stable evidence and fresh 96-seat falsification
payload"); `git diff --stat f3dc07c HEAD` touches only wave evidence files, **not** the tool, so the
measured bytes are the pinned production bytes. Expectation seal `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`.
No production, frozen, oracle or expectation byte was edited by this seat.

Fixture provenance: `case["fixture"]` copied verbatim into my own fast-scratch file and compared back with
`json.loads(fixture.json) == case["fixture"]` → **True** (only key order/indentation differ).

## 2. Derivation chain actually read before execution

1. `contract.md` §C2 quota-classification table, xfs row 4: *"`noquota` together with any quota key →
   unknown / n/a / `xfs_conflicting_quota_options`"*.
2. `preseal-amendment.md`, "C2 final rules superseding only erroneous/ambiguous original clauses", XFS
   precedence: *"conflict(noquota with ANY quota/enforcement or noenforce key), then noquota, then any
   enforced key, then any accounting-only key, else absent"*.
3. `corpus/knowledge/quota-surface-r23.md` decision table row: *"XFS conflicting noquota plus quota flag,
   or no quota token at all → unknown — defensive parser rules, not claimed normal v7.2 kernel output"*;
   case sources `S077, S078, S082` (mountinfo field parsing / xfs quota option vocabulary).
4. `frozen/case-decisions.json`: `CaseXfsConflict` is `primary: true`, reason *"Independent source-derived
   pre-measurement correction; exact author bytes, no L1 expectation edits"*.
5. Proposal → selected delta (`diff` of the two case files, three changes, **expectations byte-identical**):
   canonical UUID key `11111111-2222-…` → `6b1f4a2c-8d3e-4c5b-9f70-1a2b3c4d5e6f`; added the required
   `qgroups_enabled: null` fixture member; rationale reworded to cite the amendment's precedence sentence.
6. Selected implementation branch (`tools/mori-quota-surface.py:489-491`, `classify()`):
   `if "noquota" in keys and (keys & XFS_QUOTA_KEYS or keys & XFS_NOENFORCE_KEYS): return ("unknown","n/a","xfs_conflicting_quota_options")`
   — the conflict branch is evaluated **first**, ahead of the `noquota`-only and the enforced-key branches.
   Fixture record keys are strict (`UUID_KEYS = {devices, qgroups, qgroups_enabled, qgroups_mode}`,
   `tools/mori-quota-surface.py:187-190`).

## 3. Execution (fixture mode only; one child at a time)

argv as given and as executed (child-confirmed via `getrusage` wrapper run C):

```
/usr/bin/prlimit --as=402653184 --cpu=15 -- /usr/bin/timeout -s KILL 15s \
  /usr/bin/python3 -I \
  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
  --fixture /fast/scratch/hyaku/mori-r23/QXfsConflict/fixture.json
```

* `RLIMIT_AS` reported **inside** the child by `resource.getrlimit(RLIMIT_AS)` → `[402653184, 402653184]`
  bytes = 384 MiB exactly; `RLIMIT_CPU` → `[15, 15]`; wall timeout `timeout -s KILL 15s`.
* `TMPDIR=/fast/scratch/hyaku/mori-r23/QXfsConflict`; CPython 3.14.8 (`/usr/bin/python3` → `python3.14`);
  `prlimit` util-linux 2.42.4. No installs or updates performed.
* Child exit **2**; stdout 1242 bytes, sha256 `ac2274fb1287f63b321cfd3d9db949cd8b459d403f35650aec03532d11cc674a`;
  stderr 0 bytes, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty).
* No timeout; child wall CPU ≈ 0.032 s; **peak RSS 19 852 KiB ≈ 19.4 MiB**, far inside the 384 MiB cap.
* Repeat invocation (run B, same argv/limits) produced a **byte-identical** stdout sha256 → deterministic.
* Real mode was never entered; the argv contains only `--fixture`, so no `/proc/self/mountinfo`, sysfs,
  `quotactl`, mount or any other host read happened.

## 4. Primary comparison (six-field denominator — scored, kept separate from metadata)

| field | actual | expected | match |
|---|---|---|---|
| exit | 2 | 2 | ✅ |
| finding_id | `QUOTA_STATE_UNKNOWN` | `QUOTA_STATE_UNKNOWN` | ✅ |
| path count | 2 | 2 | ✅ |

Ordered six-field tuples `(path, fstype, mount_point, quota_state, enforcement, basis)`:

| # | actual | expected | tuple |
|---|---|---|---|
| 0 | `("/srv/quota-lab","xfs","/srv/quota-lab","unknown","n/a","xfs_conflicting_quota_options")` | identical | ✅ |
| 1 | `("/srv/quota-lab/data","xfs","/srv/quota-lab","unknown","n/a","xfs_conflicting_quota_options")` | identical | ✅ |

`ordered_six_field_tuples_equal: true`. Per-field equality for all 12 field comparisons is recorded in the
receipt (`comparison.primary[i].field_match`).

## 5. Supplementary metadata (reported apart; never folded into the primary denominator)

This case carries **no** `supplementary_expected` block, so nothing here is scored; it is reported as
observation only:

| path | device_check | quota_option_keys | btrfs_qgroups_mode |
|---|---|---|---|
| `/srv/quota-lab` | `match` | `["noquota","usrquota"]` | `null` |
| `/srv/quota-lab/data` | `match` | `["noquota","usrquota"]` | `null` |

`quota_option_keys` contains recognized xfs keys only (including `noquota`), sorted, with no option values —
exactly what the amendment prescribes. `btrfs_qgroups_mode` is `null` on an xfs row, and real mode never
reads the mode attribute in any case.

## 6. Output shape and leakage (sealed oracle logic applied to my captured stdout)

The sealed oracle `oracle-quota.py` was imported **read-only** (`importlib`, no tool executed, no other case
run) and its own `evaluate_case()` / `supplementary_checks()` / `canaries()` / `leakage_hits()` were applied
to the captured stdout:

* headline: `exit_match=true, finding_match=true, paths_match=true`, `ok=true`, `reason=None`;
* supplementary checks (schema, exit_consistency, output_keys_allowed, output_key_set, error_token,
  path_key_set, df_covers_quota, limits_text, no_leakage): **all `pass`, 0 unmet**;
* top-level keys exactly `{df_covers_quota, exit_code, finding_id, limits, paths, schema}`; per-path keys
  exactly the nine documented fields; `df_covers_quota: false`;
* leakage: 21 fixture-derived canaries (UUID, mount sources `/dev/mapper/root`, `/dev/nvme0n1p1`,
  `dm-0`, option tokens `compress=zstd:3`, `discard=async`, `space_cache=v2`, `subvolid=…`, `subvol=/@`,
  `logbufs=8`, `logbsize=256k`, option values) → **0 hits** in stdout.

## 7. Findings by severity

**High / Medium — none.** No defect is falsifiable on this case.

**Low / informational**

* **L1 — the original proposal bytes are not a valid fixture under the shipped schema (static, not
  executed).** `cases-proposed/CaseXfsConflict.json` omits `qgroups_enabled`, while the tool requires the
  exact record key set `{devices, qgroups, qgroups_enabled, qgroups_mode}` (`tools/mori-quota-surface.py:187-190`),
  so the proposal shape would be refused as `QUOTA_SETUP` (`fixture_btrfs_record_keys`) rather than classified.
  The sealed frozen case carries the corrected shape, so the scored expectation is unaffected. Recorded here
  because it is the concrete behavioural difference between the preserved proposal and the sealed selection;
  I did not execute it, since this seat is authorized for exactly one fixture invocation.
* **L2 — the conflict basis is genuinely reached, not approximated.** With super options
  `rw,inode64,logbufs=8,logbsize=256k,noquota,usrquota` the key set contains both `noquota` and the
  enforcement key `usrquota`, and the conflict branch precedes both the `noquota`-only and the
  `enabled/enforced` branches. The tool therefore invents neither a disabled nor an enabled fact.
* **L3 — the amendment's parent-ID topology refusal did not preempt this case.** Mount `244` (mount point
  `/srv/quota-lab`) has parent id `33`, and the longest strictly shorter covering mount (`/`, id `33`) has
  exactly that id, so `resolve_mount()` does not return `ambiguous_overmount` (`tools/mori-quota-surface.py`,
  `resolve_mount`). A fixture variant with a differing parent id would be refused instead; that variant is
  a different case and outside this seat's item.
* **L4 — component-prefix resolution is what puts `/srv/quota-lab/data` under the `/srv/quota-lab` mount**,
  and the device check is `match` because mount device `259:1` equals the path's `st_dev` `259:1`; the
  btrfs `st_dev`-skip rule is not involved.
* **L5 — `enforcement` is the literal string `n/a` and `basis` is a fixed token**; no mount source, UUID,
  option value or file name is echoed anywhere in the output.

## 8. Residual risk and verification gaps

* This seat falsified **one** of the 30 sealed C2 cases. The aggregate C2 status (29/30, with the frozen
  `CaseEscapedSpace` strict red) is **not** re-measured here and is not my claim; that red is outside this
  seat's item and was left untouched. Nothing in this report excuses, special-cases, relabels or rewrites it.
* The sealed oracle was **not** run end-to-end (not authorized: it would execute all 30 cases and its own
  launcher uses a 30 s timeout and no rlimit). Instead the sealed module was imported read-only and its
  evaluation functions applied to my captured stdout — the same decision logic, applied to my bytes.
* Real mode, the public selftest, the full driver and any privileged quota interface were not exercised;
  this report says nothing about them.
* The `RLIMIT_AS` bound was verified inside the child (`getrlimit` → 402653184 bytes = 384 MiB) and the
  peak RSS (19.4 MiB) confirms the child stayed well inside it.
* Two exploratory invocations made before the canonical run are recorded in the receipt
  (`superseded_exploratory_invocations`): the first passed `--as=393216`, which `prlimit` reads as **bytes**
  (384 KiB, a unit slip on my side) and which fails identically for the baseline interpreter
  `python3 -I -c 'print("ok")` (SIGSEGV 139) — it is not a tool signal; the second ran under a 32 MiB cap
  and produced byte-identical stdout. The canonical measurement is the `--as=402653184` run above.
* Open debt is unchanged by this seat: four unallowlisted inherited hits (raw 95 / allowlisted 86 /
  non-author 5), original permission control RED 11/12, two unknown dispositions, baseline acceptance
  blocked, `privacy_clearance=false`. Probe visibility/accounting consistency is not clearance, health or
  admission, and this report carries no closure, promotion or remediation authority.

## 9. Scope and hygiene

* Files written by this seat, and only these: `.ufo/waves/round-23/falsify/QXfsConflict.md` (this report)
  and `.ufo/waves/round-23/falsify/QXfsConflict/scan.json` (the receipt). Scratch artefacts live under
  `/fast/scratch/hyaku/mori-r23/QXfsConflict/`. No lane index, jj ref, fleet root, sibling or production path
  was touched; no git `add`/`commit`/`push`, no mutating `jj`.
* Read-only VCS plumbing only (`log`, `status`, `rev-parse`, `diff`, `show`). No quota tool, `quotactl`,
  `btrfs`/`xfs_quota`/`repquota`, mount or remediation command; no live qgroup/mode read; no journal,
  service, session-transcript, `agent.db` or credential access.
* No builds, linters, formatters, gates, full suite or public selftest were run; no subagents; no
  delegation; no tool installs or updates (existing: Git 2.56.0, Python 3.14.8, prlimit/util-linux 2.42.4).
* One byproduct was produced and removed: the read-only import of `oracle-quota.py` made importlib write
  `.ufo/waves/round-23/__pycache__/oracle-quota.cpython-314.pyc`. That single file and its directory were
  deleted by this seat afterwards; the oracle's own bytes are unchanged (sha256
  `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec`, identical to HEAD). No other
  `__pycache__` (`.ufo/waves/round-22/frozen/`, `tools/`) was created or removed by this seat.
