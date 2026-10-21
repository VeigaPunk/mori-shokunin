# Round-23 falsification — QTmpfsHardlimit (C2, `CaseTmpfsHardlimit`)

**Seat:** `MadoR22-2.QTmpfsHardlimit` (leaf member, no delegation)
**Lane:** `/home/vgpnk/Projects/shokunin/mori-shokunin`
**Claim under test:** C2 (quota/EDQUOT observability, `tools/mori-quota-surface.py`)
**Case under test:** `CaseTmpfsHardlimit` — primary six-field, sealed
**Mode executed:** fixture only (never real mode)
**Verdict:** **MATCH** — exit, finding id and the ordered six-field tuple all match the
sealed expectation; 9/9 sealed-oracle supplementary checks pass; no leakage.

Receipt: `.ufo/waves/round-23/falsify/QTmpfsHardlimit/scan.json`
(sha256 `3c02c967b1df41924de28a070df63fd79fb69626b482ac92d84cceb5fffb351a`).

---

## 1. Byte identities (nothing was rewritten)

| Artifact | Path | sha256 | Cross-check |
|---|---|---|---|
| Tool (production) | `tools/mori-quota-surface.py` | `e485741334d2e72a0f007481f1d2bc5b38658f54c04232965e4bbf552b8f7e92` | identical at pinned revision `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` and at `HEAD 6eb889c` (verified with `git show <rev>:tools/mori-quota-surface.py \| sha256sum`) |
| Case (frozen) | `.ufo/waves/round-23/frozen/quota-cases/CaseTmpfsHardlimit.json` | `b3226093395d0753138f4761dcd91881e56ff350de213ae4b12f03a57ceb5771` | identical at seal `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687` and in `frozen/seal-manifest.json` (`bytes: 5014`) |
| Oracle (read-only use) | `.ufo/waves/round-23/oracle-quota.py` | recorded in the receipt | imported as a module; `evaluate_case()` applied to the **captured** observation |

Expected bytes were read, never written. No case, rule, oracle, or production byte was
modified; no special-casing, exclusion, relabelling or rewrite was performed.

## 2. Invocation record (the one and only execution)

Fixture was copied from `case["fixture"]` into the seat scratch directory and serialised
with the sealed oracle's own serialisation (`json.dumps(fixture, indent=2, sort_keys=True) + "\n"`,
`oracle-quota.py:451`), so the bytes handed to the tool are the sealed driver's bytes:

* fixture: `/fast/scratch/hyaku/mori-r23/QTmpfsHardlimit/fixture.json`
  sha256 `c2ea6d5c79cdbb784214988ded60dcfd7462a1933a13d35ef04414d95c460453`
* argv: `python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-quota-surface.py --fixture /fast/scratch/hyaku/mori-r23/QTmpfsHardlimit/fixture.json`
* wrapper: `prlimit --as=384000000 --cpu=15 --nofile=64 timeout 15` (one child, 384 MiB AS, 15 s)
* env: `TMPDIR=/fast/scratch/hyaku/mori-r23/QTmpfsHardlimit/tmp` (no `/tmp` fallback)
* cwd: `/fast/scratch/hyaku/mori-r23/QTmpfsHardlimit` (no `/tmp` use)
* **exit: 1**
* stdout: 989 bytes, sha256 `a294e8a2159f7085c01d18195126bfd4389c7144baa2bfccca54f8350dc903f7`
* stderr: 0 bytes, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty)

No other sealed case, no real-mode invocation, and no quota/quotactl/mount/btrfs/xfs call
was made. The tool was executed **three times for this one case only** (exploratory run
with an equivalent non-sorted JSON serialisation, then the sealed oracle's canonical
fixture bytes, then the same canonical bytes with `TMPDIR` pinned into the seat scratch);
all three runs produced byte-identical stdout (`a294e8a2…`) and exit 1. Only the final
canonical run is recorded in the receipt.

## 3. Result — primary six-field comparison

Ordered tuple = `(path, fstype, mount_point, quota_state, enforcement, basis)`.

| Facet | Expected (sealed) | Actual (observed) | Match |
|---|---|---|---|
| exit | 1 | 1 | yes |
| finding_id | `QUOTA_ENABLED` | `QUOTA_ENABLED` | yes |
| tuple[0] | `/srv/quota-tmpfs` | `/srv/quota-tmpfs` | yes |
| tuple[1] | `tmpfs` | `tmpfs` | yes |
| tuple[2] | `/srv/quota-tmpfs` | `/srv/quota-tmpfs` | yes |
| tuple[3] | `enabled` | `enabled` | yes |
| tuple[4] | `enforced` | `enforced` | yes |
| tuple[5] | `tmpfs_quota_option` | `tmpfs_quota_option` | yes |

**Primary denominator: 1/1 case matched.** No mismatch to report for this case.

### Supplementary metadata (reported apart from the primary six)

The case declares **no** `supplementary_expected` block, so supplementary metadata is
unscored here and never folded into the primary denominator. Observed:

* `device_check` = `match`
* `quota_option_keys` = `["grpquota_block_hardlimit"]` (sorted, key names only)
* `btrfs_qgroups_mode` = `null` (tmpfs path; the btrfs sysfs record in the fixture is a decoy)

Sealed-oracle cross-check on the captured observation (`oracle.evaluate_case`): headline
`exit_match/finding_match/paths_match` all true, supplementary **9/9 pass, 0 unmet**
(schema, exit consistency, output key set, error token, path key set, `df_covers_quota`,
`limits` text, `no_leakage`). Leakage canaries derived from this fixture (btrfs UUID
`1d02a454-…`, mount sources `/dev/mapper/root`, `/dev/nvme0n1p1`, `/dev/nvme0n1p3`,
option tokens/values incl. `grpquota_block_hardlimit=1048576`, `compress=zstd:3`,
`subvol=/@home`, device basename `dm-0`) are **absent** from stdout — the option *value*
`1048576` and the device basename `dm-0` are not echoed.

## 4. Derivation audit — the match is rule-derived, not case-fitted

1. **Case → contract.** The case's super options for `/srv/quota-tmpfs` are
   `rw,inode64,grpquota_block_hardlimit=1048576`; its only quota-related key is
   `grpquota_block_hardlimit`, one of the four documented tmpfs hardlimit keys preserved
   by `preseal-amendment.md:72-74`. Contract §C2's tmpfs row therefore yields
   `enabled / enforced / tmpfs_quota_option`.
2. **Amendment narrowing is satisfied, not bypassed.** `preseal-amendment.md:74` states
   that an arbitrary `_hardlimit` suffix is *not* sufficient. The implementation honours
   this with an explicit closed key set
   (`tools/mori-quota-surface.py:217-227`: `quota, usrquota, grpquota` +
   `usrquota_block_hardlimit, usrquota_inode_hardlimit, grpquota_block_hardlimit,
   grpquota_inode_hardlimit`), not a suffix test. The rejected-suffix behaviour is
   independently covered by the tool's own selftest arm
   `tmpfs-arbitrary-hardlimit-ignored` (`tools/mori-quota-surface.py:1114-1131`).
3. **Classification path is generic.** `classify()` (`tools/mori-quota-surface.py:487-510`)
   is a single table branch on `fstype`; the tmpfs branch is
   `if keys & TMPFS_QUOTA_KEYS: enabled/enforced/tmpfs_quota_option`. The observed
   `quota_option_keys` is produced independently by `option_keys()` /
   `quota_option_keys()` (`:347-368`), which split on `=` and keep keys only — the
   option *value* is never read into the verdict.
4. **Mount resolution is rule-derived and unaffected by the known red.**
   `resolve_mount()` (`:421-464`) picks the longest covering mount point:
   `/srv/quota-tmpfs` (line id 36) over `/` (id 29). The final parent-ID clarification
   (`preseal-amendment.md:115-120`) does **not** fire here: the chosen mount's parent id
   is 29 and the longest strictly-shorter cover `/` also has id 29. The duplicate
   mount-point refusal (`:439-440`) does not fire either (`/` and `/srv/quota-tmpfs` each
   occur once).
5. **Device check is not faked.** Path `st_dev` `0:27` equals the chosen mount's
   `0:27`, so `device_check = match`; the btrfs anonymous-`st_dev` exception
   (`:536-540`) does not apply to tmpfs, exactly as the amendment prescribes.
6. **Verdict precedence.** One `enabled` row → `QUOTA_ENABLED`, exit 1 (`verdict()`,
   `:561-568`), i.e. the enabled finding is not hidden by any unknown sibling.

## 5. Findings (severity order)

### F-1 — Medium (rule-level residual risk, NOT a case mismatch, no edit made)

The tmpfs row reports `enforcement = "enforced"` from a **hardlimit key alone**, with no
`quota`/`usrquota`/`grpquota` mechanism flag present in this mount's super options. The
frozen rule prescribes exactly that (`contract.md` tmpfs row; `preseal-amendment.md:72-76`),
and the case is the arm that exercises it — so the implementation is *faithful*, and this
seat reports it as a match. But the amendment itself says two things that pull against it:

* `preseal-amendment.md:75-76` — "Hardlimit-only inputs are defensive synthetic cases;
  kernel normally also emits an active quota flag. `enforced` describes mechanism flags,
  never a nonzero limit."

On a real host, a tmpfs mount that exposes only `grpquota_block_hardlimit` (no
`grpquota` flag) is, by the amendment's own statement ("kernel normally also emits an
active quota flag"), a configuration the kernel does not produce with accounting
switched on — **[INFERENCE]**, grounded in `preseal-amendment.md:75-76` rather than in
a host observation (none was made here). The probe would still emit
`quota_state=enabled, enforcement=enforced` for it. `QUOTA_ENABLED` is a
runway-reporting finding, so the practical cost is a false "quota is enforced here"
signal, not a hard failure. This is a contract-table property inherited by the
implementation, not an implementation defect, and this seat made no change to any byte.
**Recommendation to L1:** record the tmpfs hardlimit-only over-claim as a residual risk
attributed to the C2 table, and consider (in a future round, not here) whether the
tmpfs branch should require an active mechanism flag for `enforced` while keeping the
hardlimit keys as `quota_option_keys` evidence.

### F-2 — Low (documentation accuracy in the production tool)

`tools/mori-quota-surface.py:3-8` still carries the candidate's narrative: the docstring
names the file `mori-quota-surface-v3.py` and states it is "a new candidate authored
alongside `mori-quota-surface.py` (the original, unaltered) and `mori-quota-surface-v2.py`
(preserved as the rejected unsafe-read source evidence)". The landed tree contains only
`tools/mori-quota-surface.py`; no `-v2.py` / `-v3.py` file exists, so the docstring
describes a layout that is not the shipped one. No behavioural impact: the module's
`SCHEMA` constant is `mori-quota-surface-v1` and matches the sealed oracle's
`TOOL_SCHEMA`. Not edited by this seat (no code edits permitted in this lane).

### F-3 — Informational (read-only adjudication of the expected global red)

For completeness, and **without executing that case**, the frozen `CaseEscapedSpace`
contradiction was re-derived statically from the same code and rules, and it holds:

* Fixture mount ids: `/srv` → id 42, `/srv/my\040data` → id 43 (parent id 33);
  path `/srv/my data/sub dir`.
* `resolve_mount()` (`:421-464`) selects `/srv/my data` (id 43); the longest strictly
  shorter cover is `/srv` (id 42); the chosen mount's parent id 33 **is** present in
  the snapshot and differs from 42 → refusal `ambiguous_overmount`
  (`:449-461`), matching `preseal-amendment.md:115-120`.
* The rule therefore requires `fstype=null, mount_point=null, quota_state=unknown,
  enforcement=n/a, basis=ambiguous_overmount`, while the frozen expectation row says
  `xfs / /srv/my data / enabled / enforced / xfs_quota_option`. The sealed case and the
  sealed rule genuinely conflict; `evidence/frozen-contradiction.json` records the same
  contradiction at revision `5729e7f`.
* Consequence: that red is a **real mismatch to be reported, not excused**, and it is
  *not* in the same failure family as this seat's case (this case's parent id equals its
  ancestor's id, so the guard does not fire). The strict C2 target stays unprovable at
  29/30; no exception, exclusion, relabelling or rewrite is admissible, and none was
  performed by this seat.

## 6. Residual risk and verification gaps

* **Unmeasured by this seat (out of authorised scope):** the other 29 selected cases
  (27 original-derived primary + 3 discovery + supplementary), the frozen real control
  `frozen/c2-expected-real.json`, and the quota selftest arm
  (`evidence/quota-selftest-corrected.json`, 49/49 at `f3dc07c0`) were **not** executed
  here — the seat's authorisation covers exactly one fixture-mode case. The 49/49
  selftest arm is a *different* arm from the frozen `CaseEscapedSpace` and must not be
  conflated with it.
* **No host observation was made:** no live mountinfo/sysfs read, no `df`, no quota
  tool. Every statement above about the host filesystem is static.
* **One execution, one machine, one Python build:** the match is a single-sample
  observation; the sealed oracle's own multi-case run remains the authority for the
  30-case denominator.
* **The F-1 over-claim is a rule property**, so reproducing it in any future driver run
  will not surface it; it is reported here so it is not lost.

## 7. Scope compliance

* Executed **only** `CaseTmpfsHardlimit`, in fixture mode: the recorded run plus two
  byte-identical re-runs of the same case (see §2), one child at a time, under
  `prlimit --as=384000000 --cpu=15` and `timeout 15`, with `TMPDIR` pinned to
  `/fast/scratch/hyaku/mori-r23/QTmpfsHardlimit/tmp` (no `/tmp` fallback).
* Never in real mode; never called `quotactl`, `btrfs qgroup`, `xfs_quota`, `repquota`,
  `mount`, or any quota/remediation interface; never read live qgroups/mode or a real
  `st_dev`; no quota tool, no mount, no btrfs operation.
* No live journal/journalctl query, no process/session probe, no credential/auth/config
  file, no `agent.db`, no session transcript read (this wave permits none).
* No build, test, lint, formatter, gate or smoke run; no git mutation in the lane; no
  `jj` mutation; no writes outside the assigned report and receipt paths.
* Files written: `.ufo/waves/round-23/falsify/QTmpfsHardlimit/scan.json` (receipt) and
  `.ufo/waves/round-23/falsify/QTmpfsHardlimit.md` (this report). Scratch under
  `/fast/scratch/hyaku/mori-r23/QTmpfsHardlimit/`.
