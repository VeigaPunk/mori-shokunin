# QXfsMixedEnforce — falsification of one sealed C2 quota case (round 23)

Seat: `QXfsMixedEnforce` (leaf reviewer, no dispatch). Scope: **only** the sealed case
`CaseXfsMixedEnforce.json`, executed in **fixture mode** exactly once. Lane
`/home/vgpnk/Projects/shokunin/mori-shokunin`; scratch
`/fast/scratch/hyaku/mori-r23/QXfsMixedEnforce/`.

**Verdict: MATCH.** Exit, `finding_id` and the ordered six-field path tuple equal the sealed
expectation byte-for-byte; the case does not falsify C2, and no expected byte was touched.
This seat does **not** adjudicate the wave-level C2 target (strict 29/30 with the
`CaseEscapedSpace` red) — see §7.

---

## 1. What was read before running anything

| Input | Path | Use |
|---|---|---|
| Round-23 contract | `.ufo/waves/round-23/contract.md` | C2 claim, fixture schema, classification table |
| Pre-seal amendment | `.ufo/waves/round-23/preseal-amendment.md` | "C2 final rules superseding only erroneous/ambiguous original clauses" (XFS precedence, device preemption, mount resolution) |
| Sealed case | `.ufo/waves/round-23/frozen/quota-cases/CaseXfsMixedEnforce.json` | the object under test |
| Case decision | `.ufo/waves/round-23/frozen/case-decisions.json` (`decisions[24]`) | original → selected provenance |
| Seal manifest | `.ufo/waves/round-23/frozen/seal-manifest.json` | sealed digests of case/oracle |
| Sealed oracle | `.ufo/waves/round-23/oracle-quota.py` | comparison semantics (read, not re-run over the suite) |
| Production tool | `tools/mori-quota-surface.py` | the implementation under test |
| lesson23 Gate | `corpus/lessons/round-23.md` (rows S077–S086, Gate table) | source admission and the M3–M5 corrections |
| Registry rows | `corpus/SOURCES.md` (S077, S078) + `corpus/knowledge/quota-surface-r23.md` | source scope limits |
| Kernel primary source | `fs/xfs/xfs_super.c` @ v7.2 (fetched into scratch, digest-verified) | derivation check, see §5 |

No live host quota read was performed (no `quotactl`, `xfs_quota`, `btrfs qgroup`,
`repquota`, mount, or `/sys/fs/btrfs` inspection); no real mode was run; no session
transcript, credential file or `agent.db` was read; no build/test/lint/suite was run.

## 2. Byte identity and ordering (before execution)

* Sealed case sha256 `ed13abb0eabfbbb8dd8c3391d6cc665a939d8b30b60338f08a9b840e14cd44da`
  — **identical** to the seal-manifest entry and to the blob at the seal commit
  `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687` (`git show 22772c1:…` → same digest).
* `git merge-base --is-ancestor` → seal is an ancestor of the implementation commit
  `1979a9de4ef09eccad8cbbd24fd5c79404d9f8be` **and** of the pinned production revision
  `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`; seal commit time 15:10:59 precedes the
  implementation commit 15:15:15 and the pinned revision 15:25:42.
* `tools/mori-quota-surface.py` is **absent** at the seal commit (`fatal: path … does not
  exist`), so the quota production path did not exist when the expectation was sealed.
* Working-copy tool sha256 `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92`
  == the blob at the pinned revision `f3dc07c` (byte-identical: the candidate under test is
  exactly the pinned production source).
* The selected case's `fixture` and `expected` are **byte-equal** to the original proposal
  (`cases-proposed/CaseXfsMixedEnforce.json`, sha `6d6bb2a6…`); only the derivation text
  was superseded, exactly as the rationale claims.
* Case decision `decisions[24]`: primary, "Independent source-derived pre-measurement
  correction; exact author bytes, no L1 expectation edits."

## 3. Execution — exactly one child, fixture mode only

`case["fixture"]` was copied verbatim (JSON-equal) into my own scratch file
`/fast/scratch/hyaku/mori-r23/QXfsMixedEnforce/fixture.json`
(sha256 `4658aaf395827cebbab3ea02df2fa29398914ef1a223efbba596151359291be6`, 503 bytes;
content equality with `case["fixture"]` asserted programmatically).

Given argv (as assigned):

```
timeout -s KILL 15  prlimit --as=402653184 --  python3 -I \
  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
  --fixture /fast/scratch/hyaku/mori-r23/QXfsMixedEnforce/fixture.json
```

Actual argv (resolved binaries), cwd `/fast/scratch/hyaku/mori-r23/QXfsMixedEnforce`,
`TMPDIR=/fast/scratch/hyaku/mori-r23/QXfsMixedEnforce/`:

```
/usr/bin/timeout -s KILL 15 /usr/bin/prlimit --as=402653184 -- python3 -I \
  /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py \
  --fixture /fast/scratch/hyaku/mori-r23/QXfsMixedEnforce/fixture.json
```

* Address-space limit 384 MiB (`--as=402653184`), wall timeout 15 s, one child, no
  background job, no second invocation.
* Interpreter: Python 3.14.8 (GCC 16.2.1), `-I` isolated mode.
* **exit = 1**, stderr **empty** (0 bytes), stdout 1 JSON object.
* stdout sha256 `119a7826677db72a6e1994c86a156c17f62f50f7de423077b13827d67edb30c3`
  (970 bytes); stderr sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
  (empty). Full stdout is stored verbatim in
  `.ufo/waves/round-23/falsify/QXfsMixedEnforce/scan.json` → `run.stdout`.

Exit 1 is the **contract-defined** exit for `QUOTA_ENABLED` (a runway-reporting finding,
not a failure claim) — not an error.

## 4. Comparison — primary six fields (scored)

Field order used: `path, fstype, mount_point, quota_state, enforcement, basis`.

| | expected (sealed) | actual (observed) |
|---|---|---|
| exit | 1 | 1 ✅ |
| finding_id | `QUOTA_ENABLED` | `QUOTA_ENABLED` ✅ |
| tuple[0] | `/data/projects`, `xfs`, `/data`, `enabled`, `enforced`, `xfs_quota_option` | `/data/projects`, `xfs`, `/data`, `enabled`, `enforced`, `xfs_quota_option` ✅ |

Ordered tuple lists are equal (single row each) → **primary match**, denominator
`primary_six_field_only`. No expected byte was edited by this seat.

## 5. Supplementary metadata — reported separately, never rescored

The sealed case carries **no** `supplementary_expected` block (`supplementary_expected` is an
optional key of the oracle's case schema; this case does not use it). The device/option/mode
metadata therefore exists only as prose in the sealed rationale and is **unscored** by the
sealed oracle. Observed values, checked separately against that prose:

| field | rationale prose | observed | |
|---|---|---|---|
| `device_check` | `match` | `match` | ✅ |
| `quota_option_keys` | `["gqnoenforce","prjquota"]` | `["gqnoenforce","prjquota"]` | ✅ |
| `btrfs_qgroups_mode` | `null` | `null` | ✅ |

Output shape and leakage (oracle rules replicated): `schema = mori-quota-surface-v1` ✅;
top-level key set exactly `{df_covers_quota, exit_code, finding_id, limits, paths, schema}` ✅;
`exit_code` field == process exit ✅; each path row carries exactly the nine allowed keys ✅;
`df_covers_quota = false` ✅; `limits` non-empty text ✅; **no leakage** — the mount source
`/dev/mapper/data`, the device basename `dm-1` and the option token `data=ordered` appear
nowhere in stdout ✅ (oracle canary scan: `leakage_hits: []`).

Cross-check with the sealed oracle's own per-case verdict function
(`oracle-quota.py::evaluate_case`, applied to the **already observed** output of this single
case — no extra child, no suite run): `case_ok = true`, headline `exit_match/finding_match/
paths_match` all true, supplementary checks **9 total / 9 pass / 0 unmet**.

## 6. Why the tool produced this (code + primary source)

* Mount resolution (`tools/mori-quota-surface.py` `parse_mountinfo`/`covering_mounts`/
  `resolve_mount`): the three fixture lines parse to mounts `/` (ext4, id 1, parent 0),
  `/proc` (proc, id 25, parent 0) and `/data` (xfs, id 36, parent 1). Covering mounts for
  `/data/projects` are `/` and `/data`; the mount points are distinct, so the
  `ambiguous_overmount` refusal does not fire; longest component-prefix wins → `/data`; the
  longest strictly shorter cover is `/` (id 1) and the chosen mount's parent id is 1, equal to
  that ancestor's id, so the parent-id refusal does not fire either. fstype `xfs`, source
  `/dev/mapper/data`, super options `rw,inode64,prjquota,gqnoenforce` (last three fields of
  the chosen line, per the amendment).
* Device check: mount major:minor `253:2` == path `st_dev` `253:2` → `match`; mismatch
  preemption does not apply.
* Classification (`classify`, xfs branch): `noquota` absent → conflict rule does not fire;
  `noquota` rule does not fire; `prjquota` ∈ XFS_QUOTA_KEYS → `enabled / enforced /
  xfs_quota_option`. This is the amendment's precedence order and its "SOME quota-type
  enforcement flag is set, not all" reading.
* `quota_option_keys` = sorted recognized xfs quota/noenforce keys only (`inode64`, `rw` are
  not quota-related; no option value is ever emitted).
* Verdict precedence: one `enabled` row → exit 1, `QUOTA_ENABLED`.

Source verification of the derivation (primary source, digest-matched to registry row S078):
I fetched `fs/xfs/xfs_super.c` at tag v7.2 into my scratch; its sha256 is
`0a95697dcfcdab8f7ab6ea26fdb941db952db4b73ed93c30d21e40861ed0450c`, **exactly** the
registry S078 rawSHA. In that file:

* `xfs_fs_show_options` (238–254): `XFS_UQUOTA_ENFD → ",usrquota"` else `XFS_UQUOTA_ACCT →
  ",uqnoenforce"`; `XFS_PQUOTA_ENFD → ",prjquota"` else `XFS_PQUOTA_ACCT → ",pqnoenforce"`;
  `XFS_GQUOTA_ENFD → ",grpquota"` else `XFS_GQUOTA_ACCT → ",gqnoenforce"`; `",noquota"` is
  printed **only** when `!(m_qflags & XFS_ALL_QUOTA_ACCT)`.
* Option parsing (1547–1578): `Opt_pquota/Opt_prjquota` set `ACCT|ENFD`;
  `Opt_gqnoenforce` sets `ACCT` and clears `ENFD`; `Opt_noquota` clears both.

⇒ the fixture's super-option string `rw,inode64,prjquota,gqnoenforce` **is** kernel-emittable
(project quota enforced, group quota accounting-only), and the sealed expectation
(`enabled / enforced`) follows the amendment's rule. The rationale's source anchors check out.

## 7. Findings, by severity

**F1 — LOW (granularity, unscored; no expectation change warranted).** The output's
`enforcement` field is filesystem-level. For this fixture, project quota is *enforced* while
group quota is *accounting-only*; the row reports a single `enforced` string. The per-type
split is only recoverable from `quota_option_keys` (`prjquota` + `gqnoenforce`). A consumer
reading only `enforcement` can over-read "all quota types enforced". The single-field design
comes from the pre-registered contract's output table, not from this implementation, and the
amendment explicitly blesses the SOME-flag reading — so this is a reporting-granularity
observation for the parent, **not** a mismatch and **not** a proposed edit to sealed bytes.

**F2 — LOW (coverage note, not a defect in this case).** The tool's xfs `conflict` branch
(`noquota` + any quota/noenforce key) is unreachable from kernel-emitted super options,
because the kernel prints `,noquota` only when no accounting flag is set. This case does not
exercise that branch (and does not need to); other sealed cases own it. Recorded so the
parent does not read the xfs conflict rule as a host-observation claim.

**F3 — VERIFICATION GAP (scoring, not behaviour).** The sealed case has no
`supplementary_expected` block, so `device_check`, `quota_option_keys` and
`btrfs_qgroups_mode` are **not** part of the sealed scored surface for this case; they live
only in rationale prose. They are reported here separately and unscored. If the parent wants
supplementary metadata to be an enforced contract, it must be sealed as a separate frozen
block — I did not add one, and I did not widen this case's denominator.

**F4 — RESIDUAL RISK (scope).** This seat ran one case of the 27 primary sealed C2 cases
(plus 3 source-review supplements). Nothing here supports any statement about the other 29
cases, about the frozen `c2-expected-real.json` control (real mode — deliberately not run by
this seat), or about the wave-level C2 coverage target. The wave's strict red on
`CaseEscapedSpace` is retained as a mismatch by the seat that owns it; this seat neither ran
that case nor excuses it, and this report makes no aggregate-pass claim.

**F5 — no-install note.** No tool was installed or upgraded for this item (Python 3.14.8 and
`curl`/`prlimit`/`timeout` were already present); nothing to record in the tooling ledger.

## 8. Files written by this seat

* Receipt: `.ufo/waves/round-23/falsify/QXfsMixedEnforce/scan.json` (given/actual argv,
  exit, stdout/stderr with digests, tool/case/fixture digests, primary + supplementary
  comparison, shape/leakage checks, the sealed oracle's per-case verdict, provenance and
  ordering facts).
* This report: `.ufo/waves/round-23/falsify/QXfsMixedEnforce.md`.
* Scratch (outside the lane): `/fast/scratch/hyaku/mori-r23/QXfsMixedEnforce/`
  (`fixture.json`, `stdout.txt`, `stderr.txt`, `exit.txt`, `pyversion.txt`, `compare.py`,
  `xfs_super.c`).

Frozen case bytes, oracle bytes, tool bytes, seal manifest and case decisions are untouched:
`git status --porcelain` over `.ufo/waves/round-23/frozen`, `.ufo/waves/round-23/oracle-quota.py`
and `tools/` shows no modification (only the pre-existing untracked `tools/__pycache__/`).
