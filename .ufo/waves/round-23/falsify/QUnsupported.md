# Falsification seat QUnsupported — round 23, C2, sealed fixture case `CaseUnsupported`

Verdict: **MATCH** — exit code, `finding_id` and every ordered six-field tuple equal the sealed expectation.
No frozen case/rule/oracle byte was edited. Receipt: `.ufo/waves/round-23/falsify/QUnsupported/scan.json`.

Case tier: `independent_primary` (`frozen/case-decisions.json` → `CaseUnsupported`: `primary: true`, one of the
27 independent primary C2 cases). This seat neither enlarges nor shrinks that denominator.

## 1. Axes

| axis | definition for this seat | result |
|---|---|---|
| A1 argument fidelity | exact argv, tool bytes, fixture bytes, wrapper limits preserved and hashed | PASS (3 children, 1 harness error + 2 real runs, all bounded; byte-identical stdout) |
| A2 process envelope | exit code, stderr emptiness, timeout, AS limit | PASS (exit 2, stderr 0 B, 384 MiB AS, 15 s cap) |
| A3 primary classification | exit + `finding_id` + ordered six-field tuples vs sealed `expected` | PASS (1/1 path, 6/6 fields) |
| A4 supplementary metadata | `device_check`, `quota_option_keys`, `btrfs_qgroups_mode`, reported separately from the primary denominator | PASS (3/3) |
| A5 information containment | no mount source / super-option value / uuid / device name / st_dev leaked into stdout | PASS (0 hits over 17 patterns) |
| A6 isolation | fixture mode only, no host read, no other case, no selftest, no driver, no build/lint | PASS |
| A7 immutability | sealed case bytes unchanged vs seal commit and pinned revision; tool bytes = pinned production | PASS |

## 2. What was executed (and nothing else)

* Sealed case: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-23/frozen/quota-cases/CaseUnsupported.json`
  * sha256 `28f3080b116cf3e09e3ee77f3e8b53daff826fdfb4387a21d3c58850878b22b7`, 5549 bytes.
  * Identical to `frozen/seal-manifest.json` → `files[30]` (same sha256 + byte count), to
    `frozen/case-decisions.json` → `selected_sha256`, and to the git blob at the seal commit
    `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687` and at the pinned revision `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`
    (same blob id at both). `git status` for `frozen/` and `tools/` is clean.
  * Lineage intact: `cases-proposed/CaseUnsupported.json` sha256 `44c6f3a2…` = the recorded
    `original_sha256` (retained unaltered); `cases-corrected/CaseUnsupported.json` is byte-identical to the frozen file.
* Candidate tool: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py`
  * sha256 `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92`, git blob `439ff4c1a68fc4f98182c6b855b3b4c790286851`
    — identical at HEAD and at the pin `f3dc07c0…`, and the working copy is unmodified, so this measurement is on the
    pinned production bytes.
* Synthetic fixture: `case["fixture"]` copied into `/fast/scratch/hyaku/mori-r23/QUnsupported/fixture.json`
  (sha256 `6d0aa9bf9912cc305a226838a4dee74bfc6eb3376ca0c67353ee6d25b37998a0`;
  `json.loads(fixture) == case["fixture"]` → True). The sealed case file itself was never written to.
* argv (given): `python3 -I <TOOL> --fixture /fast/scratch/hyaku/mori-r23/QUnsupported/fixture.json`
  wrapper: `prlimit --as=402653184 --cpu=15 timeout -s KILL 15 …` (402653184 B = 384 MiB).
* stdout: `/fast/scratch/hyaku/mori-r23/QUnsupported/stdout.txt`
  (sha256 `a8cf0e8a8c31b5ae29158dd7db45b3fc35425e0e1e7b564b6222b719f0749039`, 1 line + trailing `\n`).
  stderr: `…/stderr.txt` (0 B, sha256 `e3b0c442…b855` — empty).

### Given vs actual envelope (recorded, not normalised away)

* **given**: mode `fixture`, address-space limit 384 MiB, timeout 15 s, one child at a time, real mode forbidden,
  this one case only.
* **actual**: children spawned **3**, all reaching the interpreter, all under the same prlimit/timeout envelope:
  1. **run 1 — harness error on the seat side**: the whole case FILE was passed instead of `case["fixture"]`.
     The tool correctly refused it: exit **2**, `finding_id` `QUOTA_SETUP`, error token `fixture_key_set`
     (top-level key set mismatch), `paths: []`, no input text echoed. No tool defect; the run's stdout file was
     overwritten by run 2 and is therefore not hashed.
  2. **run 2** — correct `case["fixture"]` input → exit **2**, stdout sha256 `a8cf0e8a…`.
  3. **run 3** (the recorded measurement run, whose bytes are in `stdout_json`/`stdout.txt`) → exit **2**,
     stdout sha256 `a8cf0e8a…` — **byte-identical to run 2**, i.e. the classification is deterministic here.
* No background jobs, no subagents/delegation, no driver, no selftest, no build/lint/formatter, no real-mode run,
  no quota tool / `quotactl` / `xfs_quota` / `repquota` / mount / remediation call.

## 3. Primary comparison (six scored fields, ordered)

Expected (sealed `expected.paths[0]`) vs actual (tool stdout `paths[0]`), field order
`(path, fstype, mount_point, quota_state, enforcement, basis)`:

| # | field | expected | actual | = |
|---|---|---|---|---|
| 1 | path | `/mnt/nfs/data` | `/mnt/nfs/data` | ✅ |
| 2 | fstype | `nfs4` | `nfs4` | ✅ |
| 3 | mount_point | `/mnt/nfs` | `/mnt/nfs` | ✅ |
| 4 | quota_state | `unknown` | `unknown` | ✅ |
| 5 | enforcement | `n/a` | `n/a` | ✅ |
| 6 | basis | `unsupported_fstype` | `unsupported_fstype` | ✅ |

* exit: expected `2` → actual `2` ✅ (`stdout.exit_code` field also `2`, consistent with the process exit).
* finding_id: expected `QUOTA_STATE_UNKNOWN` → actual `QUOTA_STATE_UNKNOWN` ✅.
* path count: expected 1 → actual 1 ✅ (order preserved; single path).
* output schema `mori-quota-surface-v1`; top-level key set exactly
  `{df_covers_quota, exit_code, finding_id, limits, paths, schema}` ✅; `df_covers_quota: false` ✅;
  no `error` key on a verdict ✅; exactly one JSON object on stdout ✅.

**Primary verdict: MATCH (1/1 path, 6/6 fields, exit and finding_id equal).**

## 4. Supplementary metadata (reported separately, never folded into the primary denominator)

The sealed case file carries **no** `supplementary_expected` key (only `CaseBtrfsDevMatch` has one across the 30 frozen
cases), so for this case the supplementary values exist only as prose in the sealed `rationale` and are derived here
from `preseal-amendment.md` — i.e. **unsealed**, and they do not change the scored denominator.

| field | expected (rationale / amendment) | actual | = |
|---|---|---|---|
| `device_check` | `match` (chosen mount `0:61` == fixture `st_dev 0:61`, fstype not btrfs) | `match` | ✅ |
| `quota_option_keys` | `[]` (unsupported fstype ⇒ empty; `hard`/`vers` are not quota keys) | `[]` | ✅ |
| `btrfs_qgroups_mode` | `null` | `null` | ✅ |

Supplementary verdict: 3/3 match. These are *not* scored against the sealed six-field expectation and do not widen it.

## 5. Rule-path audit (why the match is a real derivation, not a coincidence)

* Mount resolution (`tools/mori-quota-surface.py:421-462`, `covering_mounts` 407-419): covering mountpoints for
  realpath `/mnt/nfs/data` are `/` (mount id 29, btrfs) and `/mnt/nfs` (mount id 121, nfs4); each occurs exactly once
  ⇒ no repeated-mountpoint refusal (`len(points) != len(covered)`, line 439-440). Longest mount point wins →
  `/mnt/nfs` (8 chars) over `/` (1 char).
* Parent-ID rule (amendment, final pre-seal clarifications): the chosen mount's parent id 33-vs-29 check — here
  parent id `29` **is** the id of the longest strictly shorter covering mount (`/`), so no `ambiguous_overmount`
  refusal (lines 452-461). Had the parent id pointed elsewhere, the amendment's rule and the sealed expectation for
  `CaseEscapedSpace` would have demanded `ambiguous_overmount`; the two cases therefore diverge for a structural
  reason, not by special-casing.
* Field parse (`parse_mountinfo` 311-345, source S082 `Documentation/filesystems/proc.rst` §3.5, verified in
  `evidence/sources/S082-…` lines 1973-1983: fields 1-6, optional fields, `-` separator, then filesystem type,
  mount source, super options): the separator and the last three fields of the chosen line are taken per line
  (`require(len(fields) - separator - 1 == 3)`), giving fstype `nfs4`, mount point `/mnt/nfs`,
  source `nfs-server.example:/export` (never emitted).
* Device check (`evaluate` 513-556): chosen mount major:minor `0:61` equals path `st_dev 0:61` ⇒ `device_check`
  `match` (line 534-535). The btrfs subvolume skip (line 536) does not apply because the chosen fstype is nfs4.
  A mismatch would have preempted the filesystem table.
* Classification (`classify` 487-510): `nfs4` is not xfs/btrfs/ext2-3-4/tmpfs ⇒ the retained `other` row
  `("unknown", "n/a", "unsupported_fstype")` (line 510). The tool's own selftest encodes the same expectation
  independently (lines 1495-1498).
* Verdict precedence (`verdict` 561-568): no path enabled, one path unknown ⇒ `RC_SETUP`/`QUOTA_STATE_UNKNOWN` (line 567).
* Fixture validation (`load_fixture` 695-772): exact top-level key set (line 705), canonical `st_dev`
  (`DEVICE_RE`), canonical UUID key, exact UUID record key set including `qgroups_enabled`, and the
  `qgroups:false ⇒ enabled=null/mode=null` pairing (lines 747-760) — the corrected fixture shape of this case is
  accepted, and the proposal's old shape (no `qgroups_enabled`) would have been a setup error, which is exactly the
  amendment-mandated delta recorded in the sealed rationale.
* Fixture mode reads only the fixture file (`probe_fixture` 681-692): no host mountinfo, no sysfs, no stat.

## 6. Information containment

stdout checked against 17 patterns — `nfs-server.example`, `/export`, `vers=4.2`, `timeo=600`, `retrans=2`,
`rsize=1048576`, `wsize=1048576`, `hard`, `proto=tcp`, `sec=sys`, `0:61`, `6f1a2c3d`, `dm-0`, `/dev/mapper/root`,
`relatime`, `shared:`, `subvolid`: **0 hits**. No mount source, no super-option value, no uuid, no device name and no
input text reached stdout.

## 7. Residual observations (outside this seat's scored item, reported for the parent)

1. **Production bytes ≠ the seat's recorded build candidate.** The pinned production tool
   (`tools/mori-quota-surface.py`, sha256 `e4857413…`, git blob `439ff4c1…`) is *not* byte-identical to
   `.ufo/waves/round-23/build/ImplQuota/mori-quota-surface-v3.py` (sha256 `5199e97b…`): `classify()` returns a
   2-tuple instead of a 4-tuple (line 551), an empty `paths` list is now a setup error (line 711), a path entry must
   now match the key set *exactly* (lines 715-716), `limits` is serialised as one joined string instead of a list
   (lines 781, 792), and the selftest block differs by one changed arm (`st_dev` of the escaped-mount-point arm) plus
   one added arm. The string form of `limits` is what the sealed oracle demands
   (`oracle-quota.py:271-272`), so the production form is the consistent one; the build artifact is stale evidence.
   The measured candidate is the pinned production artifact, which is what the frozen cases are meant to test.
2. **Documented sibling names are stale.** The production docstring titles the file `mori-quota-surface-v3.py` and
   describes siblings `mori-quota-surface.py` / `-v2.py` that exist only under `build/ImplQuota/`. Cosmetic
   provenance drift, no behavioural effect.
3. **CaseEscapedSpace strict red was not executed by this seat.** Its frozen expectation contradicts the amendment's
   parent-ID rule (see `evidence/frozen-contradiction.json`: selected mount id 43, parent id 33, longest shorter
   cover id 42 at `/srv`). It stays a **reported mismatch** for the seat that owns it; nothing here excuses it, and
   this seat neither fixed, relabelled, excluded nor special-cased any frozen byte.

## 8. Residual risk and verification gaps

* One case, one candidate revision, one fixture: this seat falsifies `CaseUnsupported` only. It says nothing about the
  other 26 primary cases, the 3 source-review supplemental cases, the real-mode control, or the strict C2 target,
  which stays **UNPROVABLE at 29/30** for the reason recorded in `evidence/frozen-contradiction.json`.
* Real mode was never exercised (by design): the probe's real-mode readset, the `qgroups/enabled` handling and the
  "never read `qgroups/mode`" correction are unverified by this seat.
* The supplementary three values for this case are unsealed prose, so a future re-seal could legitimately restate them;
  the primary six-field match does not depend on them.
* Determinism was observed across two independent bounded runs of the same bytes only (not across processes/machines).
* `QUOTA_STATE_UNKNOWN` is an observability classification only: it is not a capacity, health, clearance or
  admission verdict, and NFS/server-side quota remains outside the probe's observability.

## 9. Tooling

No package was installed or updated by this seat (no pacman/uv/npm/cargo action, no service restart, no system
upgrade); the measurement used only pre-existing `python3`, `prlimit` and `timeout`. All deliberate scratch lives
under `/fast/scratch/hyaku/mori-r23/QUnsupported/` (fixture.json, stdout.txt, stderr.txt, compare.py, mkreceipt.py);
nothing was written to `/tmp`, no lane index/jj/ref was touched, no sibling file was modified.
