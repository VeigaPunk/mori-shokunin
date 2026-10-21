# QBtrfsDevMatch — round-23 falsification of the sealed C2 case `CaseBtrfsDevMatch`

Seat: `MadoR22-2.QBtrfsDevMatch` (reviewer, leaf; no delegation).
Wave: mori round 23, claim **C2 — coverage** (FR2 quota/EDQUOT observability).
Production under test: `tools/mori-quota-surface.py` @ `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`.
Expectation seal: `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`.
Receipt: `.ufo/waves/round-23/falsify/QBtrfsDevMatch/scan.json`
(`sha256 acb31d4a7c2eef65b42f0e4dda829dd6c1ead78f678491c0c5d1ad22ff530ce2`).

## Verdict

**MATCH — no falsification of this case.**

| facet | given (sealed expectation) | actual (observed) | match |
|---|---|---|---|
| exit | `0` | `0` | yes |
| `finding_id` | `QUOTA_DISABLED` | `QUOTA_DISABLED` | yes |
| ordered six-field tuple | `('/opt/mori/quota-case', 'btrfs', '/', 'disabled', 'n/a', 'btrfs_qgroups_dir_absent')` | identical | yes |

Primary (scored, six-field denominator) and supplementary metadata were compared
separately; the six-field denominator was not widened by any supplementary field.
All 13 sealed supplementary checks pass (0 unmet). No expected byte was edited.

## What was read before executing

| artifact | path | why |
|---|---|---|
| sealed case | `.ufo/waves/round-23/frozen/quota-cases/CaseBtrfsDevMatch.json` | the case under falsification |
| case derivation (author report) | `.ufo/waves/round-23/build/CaseBtrfsDevMatch.md` | how the expectation was derived, and its recorded ambiguities A1–A5 |
| original proposal / corrected case | `.ufo/waves/round-23/cases-proposed/CaseBtrfsDevMatch.json`, `.ufo/waves/round-23/cases-corrected/CaseBtrfsDevMatch.json` | verify the sealed file's claimed one-field delta |
| amendment | `.ufo/waves/round-23/preseal-amendment.md` | the C2 final rules that supersede the contract's ambiguous clauses |
| contract | `.ufo/waves/round-23/contract.md` | C2 fixture format, classification table, verdict precedence |
| implementation | `tools/mori-quota-surface.py` | the selected quota implementation |
| sealed oracle | `.ufo/waves/round-23/oracle-quota.py` | the sealed comparison logic (imported, not re-implemented) |
| source rows | `.ufo/waves/round-23/evidence/source-quotes.json` | S079–S082 quotes behind the case's derivation |
| frozen contradiction | `.ufo/waves/round-23/evidence/frozen-contradiction.json` | context: the known strict red is `CaseEscapedSpace`, not this case |

## Byte identities (verified, not asserted)

| object | sha256 | provenance check |
|---|---|---|
| sealed case file | `a74da5db52f71ec3f4a92018b2f2cd35fb43e349773e17ccce8a8235bbbd43bc` | `git hash-object` = `136d98b9e4a7d6770cc21f65e3b12361baf9f60d` = blob at seal `22772c1` = blob at `HEAD` (6eb889c); identical to `cases-corrected/CaseBtrfsDevMatch.json` |
| original proposal | `02a4389147083d939e421300756eb1d4bdc0d927f4ade089778c3079fb2aea70` | unchanged proposal; differs from the sealed case by exactly the added `qgroups_enabled: null` field |
| tool | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` | worktree == `git show f3dc07c:tools/mori-quota-surface.py`; `git diff f3dc07c..HEAD -- tools/mori-quota-surface.py` is empty |
| oracle | `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec` | worktree == blob at seal == blob at `HEAD` |
| fixture written for the run | `761956a1c793f4e623a1647f134a76ff341783fdfc97bcae2deaf16998bd1949` (836 B) | `json.dumps(case["fixture"], indent=2, sort_keys=True) + "\n"` — the oracle's own canonical fixture form (`oracle-quota.py`, main) |
| observed stdout | `63ca6c223c55a3d9cc3f7f64031b5e81ac5501441c18793bd4c72e8f7164ac25` | byte-identical across two independent runs |

## Exact execution (fixture mode only; real mode never invoked)

Scratch (this seat's own tree, no `/tmp`): `/fast/scratch/hyaku/mori-r23/QBtrfsDevMatch/`
— `fixture.json`, `stdout.json`, `stderr.txt`, `exit.txt`, `stdout2.json`, `stderr2.txt`,
`compare.py`.

```
argv (given, canonical tool invocation):
  python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
          --fixture /fast/scratch/hyaku/mori-r23/QBtrfsDevMatch/fixture.json

argv (actual, as executed, one child at a time):
  prlimit --as=402653184 -- timeout -s KILL 15 \
    python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
            --fixture /fast/scratch/hyaku/mori-r23/QBtrfsDevMatch/fixture.json
```

* address-space limit 384 MiB (`402653184` bytes), wall timeout 15 s, `TMPDIR` and cwd inside
  the seat scratch dir; the two runs were strictly sequential (one child at a time).
* exit `0`; stderr empty (0 bytes); stdout one JSON object.
* Repeat run: exit `0`, stdout **byte-identical** (`cmp` clean), stderr 0 bytes → the observed
  verdict is deterministic, not a one-shot accident.
* Only `--fixture` mode was used. No `--path`, no `--selftest`, no real-mode call, and no
  host read of `/proc/self/mountinfo`, `/sys/fs/btrfs`, `stat`, `quotactl`, `btrfs`,
  `xfs_quota`, `repquota` or `mount` was performed by me or by the tool.

## Primary comparison (scored six-field denominator)

Ordered tuple = `(path, fstype, mount_point, quota_state, enforcement, basis)`.

| field | given | actual | match |
|---|---|---|---|
| path | `/opt/mori/quota-case` | `/opt/mori/quota-case` | yes |
| fstype | `btrfs` | `btrfs` | yes |
| mount_point | `/` | `/` | yes |
| quota_state | `disabled` | `disabled` | yes |
| enforcement | `n/a` | `n/a` | yes |
| basis | `btrfs_qgroups_dir_absent` | `btrfs_qgroups_dir_absent` | yes |

The comparison was performed by importing the **sealed** oracle
(`oracle-quota.py`, `sha256 f1f4a0…`, byte-identical to the seal commit) and calling its
`evaluate_case()` on this one case only — not by re-implementing the rule. Result:
`ok = True`, `headline = {exit_match: true, finding_match: true, paths_match: true}`,
`reason = None`.

## Supplementary metadata (reported apart from the six-field denominator)

Sealed `supplementary_expected` (kept out of `expected.paths[0]`, so the original denominator
is untouched):

| field | given | actual | match |
|---|---|---|---|
| `device_check` | `match` | `match` | yes |
| `quota_option_keys` | `[]` | `[]` | yes |
| `btrfs_qgroups_mode` | `null` | `null` | yes |

13/13 sealed supplementary checks pass, 0 unmet: `schema`
(`mori-quota-surface-v1`), `exit_consistency` (0), `output_keys_allowed`, `output_key_set`
(exactly `{schema, finding_id, exit_code, paths, df_covers_quota, limits}`),
`error_token` (absent, legal), `path_key_set` (exactly the 9 output path keys),
`df_covers_quota` (false), `limits_text` (non-empty str), the three per-row metadata checks
above, and `no_leakage` (no uuid, no mount source, no `key=value` option token or option value
echoed in stdout).

## Independent rule audit (derivation re-derived from contract + amendment, then compared)

1. **Covering mount.** The path `/opt/mori/quota-case` is covered by exactly one mount point,
   `/` (the `/home` btrfs mount is not a component-prefix cover; `/proc` and `/dev` are not
   either). No covering mount point occurs more than once → the amendment's
   `ambiguous_overmount` refusal does **not** trigger. The chosen mount's parent id is `1`,
   which is absent from the snapshot ids `{22, 23, 31, 32}` → the amendment's parent-id
   refusal does **not** trigger (a missing parent id is unknown topology, not a refusal).
   Consequence: fstype `btrfs`, mount point `/`.
2. **Device check.** Mount `major:minor` = `0:26`, path `st_dev` = `0:26` → equal → the
   amendment's final clause "Equal → match" applies; the device-mismatch preemption is not
   engaged, and the btrfs skip branch (which exists only to avoid a *false* mismatch) never
   applies. `device_check = match`, no preemption, so the filesystem table is reached.
3. **Quota classification.** Raw decoded source `/dev/mapper/root` is looked up in
   `device_links` → mapped basename `dm-0` (the amendment's raw-source lookup rule).
   Exactly one uuid (`8f3c1d2e-…-0a1b2c3d4e5f`) lists `dm-0` in `devices` → the
   single-uuid btrfs rows apply; `btrfs_device_unmapped` does not. That record has
   `qgroups: false` **and** `qgroups_enabled: null` **and** `qgroups_mode: null`, exactly
   the amendment's required pairing, so the parent inspection succeeded and the absent-dir
   row holds → `disabled` / `n/a` / `btrfs_qgroups_dir_absent`. The `qgroups: true` rows
   (`btrfs_qgroups_enabled` / `_disabled` / `_enabled_unavailable`) are not reachable here.
4. **Option keys.** btrfs carries its mechanism in sysfs, not in mount options → the
   amendment's "for btrfs `quota_option_keys = []`" → `[]` (the super options
   `rw,space_cache,subvolid=5,subvol=/` contain no quota key).
5. **Verdict.** One path, `disabled`; no enabled, no unknown → exit `0`, `QUOTA_DISABLED`.

The observed output agrees with the re-derived rule at every step, so the match is not an
artifact of the implementation.

## Findings

* **No mismatch in this case.** Nothing in the case, its derivation, the amendment rules or
  the implementation's handling of this fixture is contradicted by the observed run.
* **Low — `device_check = match` is reached only because equality is tested before the btrfs
  skip.** The implementation orders the checks as *equal → `match`*, then
  *btrfs and stat major 0 → `btrfs_subvolume_skipped`*, then *mismatch → preemption*
  (`tools/mori-quota-surface.py`, `evaluate()`). The amendment's phrasing "Btrfs skips
  equality only when stat major is 0" reads, in isolation, as if a btrfs path with stat major
  `0` (this fixture: `0:26`) would skip the equality check and report
  `btrfs_subvolume_skipped`. The amendment's closing clause "Equal → match" and the
  implementation's order both yield `match`, and the sealed supplementary expectation
  (`match`) is what the case author derived. This is a **phrasing ambiguity in the amendment,
  not a defect in the case or the tool**, and it does not affect any scored field. It is
  recorded because the sealed supplementary value is only stable under the "equal wins" reading.
* **Low — the equality this case pins is synthetic.** The case author recorded this himself as
  ambiguity A1 (btrfs `st_dev` is the root's anonymous device per S081
  `stat->dev = BTRFS_I(inode)->root->anon_dev;`, so a real btrfs path normally mismatches the
  mount's `major:minor`). The case deliberately exercises the defensive equal branch; the
  real-world anchor remains the frozen real control (`btrfs_subvolume_skipped`). No claim about
  host behaviour is made or implied by this run.
* **Closed since the author's report — A2 (device_check unverified by any sealed case) is now
  closed for the btrfs-equal branch only.** The corrected case carries
  `supplementary_expected.device_check = match`, so the branch is checked. It remains
  unconstrained for the other three `device_check` values in the sealed population; that is a
  population-level coverage gap owned by L1, not a defect of this case.

## Explicit scope statements (not excuses)

* **`CaseEscapedSpace` was not executed in this seat.** My seat's scope is exactly one
  fixture-mode case. The known strict red (29/30, `evidence/frozen-contradiction.json`:
  selected mount id 43, parent id 33, longest strictly shorter cover id 42 `/srv` →
  `unknown/n/a/ambiguous_overmount`, versus the frozen expectation of an enabled xfs row) is a
  **different** case and remains a **mismatch** that this report neither excuses nor
  relabels. This case is not implicated by that contradiction: it has a single covering mount
  point and an absent parent id, so `ambiguous_overmount` cannot apply to it.
* **Real mode was never invoked.** No real control was executed, so this report makes no
  claim about the live host's quota state; `df_covers_quota: false` remains the tool's own
  standing statement that df percentages do not cover quota exhaustion.
* **No expected, oracle, frozen or production byte was modified.** Post-run re-verification:
  sealed case `sha256 a74da5db…`, blob `136d98b9…` (identical to the seal commit and to
  `HEAD`); tool `sha256 e4857413…`; oracle `sha256 f1f4a027…`. `git status --porcelain` on
  `frozen/`, `cases-corrected/`, `cases-proposed/` and `tools/` shows no modification — the
  only entries are untracked caches (the pre-existing `tools/__pycache__/`, mtime 15:17, and
  `.ufo/waves/round-23/__pycache__/`, recreated at 15:33 by a concurrent process) and the
  wave's own untracked `falsify/` output.
* **`QUOTA_DISABLED` is not a capacity or health verdict.** The tool's own `limits` text says
  so; ENOSPC can coexist. Nothing here is a clearance, an admission, a promotion or a health
  claim.

## Bounds and hygiene

* Writes: only `.ufo/waves/round-23/falsify/QBtrfsDevMatch.md` (this report) and
  `.ufo/waves/round-23/falsify/QBtrfsDevMatch/scan.json` (the receipt), plus synthetic
  scratch under `/fast/scratch/hyaku/mori-r23/QBtrfsDevMatch/`. No `/tmp` use. No lane index,
  `jj`, ref, fleet-root or sibling writes.
* One child at a time (two sequential invocations of the same single case); 384 MiB address
  space and 15 s timeout via `prlimit`/`timeout`; no background jobs, no delegation, no
  subagents.
* Read-only VCS plumbing only (`log`, `status`, `rev-parse`, `ls-tree`, `cat-file`,
  `show`, `hash-object`, `merge-base`, `diff`); no `add`/`commit`/`push`, no mutating `jj`.
* No quota interface was called or read: no `quotactl`/`ioctl`, no `btrfs`, `xfs_quota`,
  `repquota`, `mount`, no real qgroup reads. The tool ran in fixture mode and read exactly one
  file: my scratch `fixture.json`.
* One byproduct of my own was created and removed: importing the sealed oracle produced
  `.ufo/waves/round-23/__pycache__/oracle-quota.cpython-314.pyc`; I deleted that file and the
  then-empty directory, and verified the path was gone. At the final integrity check (15:34)
  the same path existed again with a 15:33 mtime — i.e. a concurrent process in this shared
  lane re-created the bytecode cache after my removal. I left that re-created file untouched
  (it is not mine to delete; it is a `__pycache__` of an unchanged frozen file and affects no
  frozen byte). `git status --porcelain` on `frozen/`, `cases-corrected/`, `cases-proposed/`
  and `tools/` shows no modification by me.
* **Installs: none.** No `pacman`, `uv`, `cargo` or `npm` transaction was performed, so
  nothing to record beyond the pre-existing tooling used: `python3` 3.14.8, `prlimit`
  (util-linux), `timeout` (coreutils). No system upgrade, no service restart; host-wide
  package transactions remain paused.
* No session transcript, `agent.db`, credential/auth file, `.ufo/interactive-sessions`,
  `~/.omp` session, journal/journalctl, process/service/session probe, or shell-history read
  was performed. `agent://` was not used.

## Residual risk and verification gaps

1. **Population-level, not mine:** this seat proves one case. The 30-case strict population
   still carries the `CaseEscapedSpace` red (29/30) and the four unallowlisted inherited hits,
   original permission RED 11/12, the two unknown dispositions, blocked baseline acceptance
   and `privacy_clearance=false` — all unchanged by this run.
2. **The `device_check` reading for btrfs-with-stat-major-0** rests on the "equal wins"
   ordering (see the low finding above). If L1 later re-orders that rule, this case's
   *supplementary* expectation would flip to `btrfs_subvolume_skipped`; the scored six-field
   tuple would not change.
3. **Only the btrfs-equal branch of `device_check` is sealed.** The mismatch, not-checked and
   `btrfs_subvolume_skipped` values remain unconstrained by the sealed population outside this
   case's fixture.
4. **No live-host corroboration** — by design: fixture mode only. The real control remains
   the declared-live-read arm owned by `RerunPinnedDriver`, not by this seat.
5. **Determinism** was checked for one invocation shape (`python3 -I`, fixture mode) on this
   host at this revision; the repeat run was byte-identical.
