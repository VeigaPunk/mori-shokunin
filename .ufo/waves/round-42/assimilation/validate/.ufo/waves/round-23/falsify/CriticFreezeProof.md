# CriticFreezeProof — round 23 wave 2 (freeze/seal proof critic)

Seat: `MadoR22-2.CriticFreezeProof`. Read-only. Pins: production
`f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`, expectation seal
`22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`, lane HEAD `6eb889c037163e4886eaa61501258910d6a529b9`.
Method: read-only `git show/log/diff/ls-tree/merge-base/rev-parse/status`, in-process
SHA-256 over committed blobs and working copies, and one static (no tool execution) sweep
of the sealed parent-ID rule over frozen case bytes. No driver/oracle/tool/selftest run,
no live host reads, no installs. Scratch dir created (unused):
`/fast/scratch/hyaku/mori-r23/CriticFreezeProof/`.

## Verdict

The seal holds byte-for-byte: no frozen, oracle, driver, dependency, contract or
amendment byte changed between the seal and production or HEAD, and the strict
ancestry claim is true. C1 holds. C2 strict stays UNPROVABLE at 29/30, which I confirm.
Four defects remain, none of which change a count:

- One selected case's declared source file does not exist anywhere (F4).
- The sealed driver cannot detect that kind of hole (F8).
- The sealed C2 oracle's file name and self-description disagree (F5).
- A sealed W1 report is mutated in the working tree (F9).

## Axes

- A1 freeze integrity: seal → production byte identity.
- A2 selected-case provenance.
- A3 C1 calibration: original26 plus separate guards.
- A4 C2 coverage strict target.
- A5 seat/report identity.

## Findings

### F1 — Strict ancestry: holds (A1)
Linear chain `1bfe708 → 4dc80c1 → c1e8b81 → 22772c1 (seal) → 1979a9d → 5729e7f → 56ac3ba → f3dc07c (prod) → 6eb889c (HEAD)`.
`merge-base --is-ancestor seal prod` = 0, seal ≠ prod, and `rev-list --count seal..prod` = 4.
Commit times are monotone (seal 15:10:59, first production commit 15:15:15, prod 15:25:42, all -03:00).
Timestamps are corroboration only. I did not read the reflog, and no remote-ref evidence
proves a push-before-production order. Today only HEAD carries `origin/master`.

### F2 — Sealed bytes unchanged: holds (A1)
- All 43 `frozen/seal-manifest.json` entries match sha256 and size at the seal, at prod, at HEAD and in the working tree.
- The manifest blob itself is `8ff351f2…c082` at all four places.
- Excluding the measure dirs, `git diff --name-status seal prod` shows only:
  - added `build/ImplQuota/*.py`
  - added evidence files
  - modified `LOG.md`, `SKILL.md`, `corpus/knowledge/retention-reconciliation-r22.md`, `corpus/lessons/round-23.md`
  - added `tools/mori-quota-surface.py`
  - modified `tools/mori-retention-reconcile.py`
- No path under `frozen/`, `cases-*`, the oracles, the driver, the contract or the amendment changed.
- `prod..HEAD` adds only evidence, wave2 spec/run and `LOG.md`.
- The measure4 driver checks C01–C13 all pass. C13: executed driver sha `5c12fdc0…fbcd` equals the sealed driver.

### F3 — Reconciler and quota presence: holds (A1, A3)
- `tools/mori-retention-reconcile.py`: `0795bac9…de32` at `1bfe708` and at the seal; `4599ee1a…a36` at prod and HEAD. The prod value equals `frozen/c1-source-delta.json` `transformed_sha256`.
- `tools/mori-quota-surface.py`: absent at `1bfe708` and at the seal; `e4857413…7e92` at prod, equal to the working tree.

### F4 — COUNTEREXAMPLE: CaseTmpfsNoQuota's selected source does not exist (A2)
`frozen/case-decisions.json` names `"selected": "cases-corrected/CaseTmpfsNoQuota.json"`
with `selected_sha256 7afd98c1…49b5` and the reason "exact author bytes".

Evidence:
- The path is absent at the seal, at prod, at HEAD (all refs: `git log --all` has no entry) and in the working tree.
- The seal's `cases-corrected/` holds 27 files, but no `CaseTmpfsNoQuota.json`. Instead there are two CaseSymlinkRealpath files.
- A content-hash search of the lane (excluding .git/.jj/.scratch/interactive-sessions) finds `7afd98c1…` only at `frozen/quota-cases/CaseTmpfsNoQuota.json`.
- The author report `build/CaseTmpfsNoQuota.md` still has its W1-bound bytes (`2bcce078…bda1`, as in `evidence/wave1-report-presence.json`). It cites only the original proposal, while 26 of 27 other author reports reference `cases-corrected`.
- So the corrected bytes' authorship is unrecorded, and LOG's "names every selected exact author file" is false for this row.

Impact:
- The frozen copy's `expected` is JSON-equal to the original proposal. Only `fixture`, `rationale` and `scenario` differ (the btrfs/xfs lines and qgroups record were added).
- The case passes after the cutover, so no count changes.
- This is a provenance defect, not a byte-integrity one.

Smallest safe correction:
- Record the missing source as an explicit provenance-debt annotation (a new evidence file).
- Do not edit `case-decisions.json` or the frozen bytes.
- Do not count CaseTmpfsNoQuota as "independently authored, exact author bytes" in any provenance claim.

### F5 — Identity hazard in the sealed C2 oracle name (A2, A5)
- The wave-root `oracle-quota.py` (`f1f4a027…bec`) is byte-identical to `build/OracleQuota/oracle-quota-v3.py`.
- Its docstring and argparse `prog` call it `oracle-quota-v3.py`, and its docstring says "v1 (oracle-quota.py) is tolerant".
- That v1 is `build/OracleQuota/oracle-quota.py` (`982753f4…1624`), a different file.
- The receipts' `schema: mori-r23-c2-oracle-v3` disambiguates, but a reader who resolves the docstring's "oracle-quota.py" at the wave root gets v3, not v1.

Correction: an evidence note binding wave-root `oracle-quota.py` to `build/OracleQuota/oracle-quota-v3.py` by sha. Never edit the sealed bytes.

### F6 — CaseEscapedSpace contradiction: confirmed, unique, detectable at seal (A4)
From the frozen bytes `8340738a…eabfe`:
- Mount 43 `/srv/my\040data` (xfs, 0:45) has parent 33, which is btrfs `/`.
- The longest strictly-shorter cover is mount 42 `/srv` (0:44), so the sealed final-clarification parent-ID rule requires `unknown/n/a/ambiguous_overmount` with null fstype and mount_point.
- The frozen expected says `xfs/"/srv/my data"/enabled/enforced/xfs_quota_option`, exit 1 `QUOTA_ENABLED`.

Static sweep of that rule over all 30 frozen cases:
- CaseEscapedSpace is the only conflict.
- CaseStacked (duplicate mountpoint plus parent) and SupplementHiddenMount (parent) are consistently expected as ambiguous.

Cause of the conflict:
- The corrected CaseEscapedSpace is JSON-equal to its proposal in `expected`, `mountinfo`, `paths` and `device_links`. Only `btrfs_sysfs` and `rationale` changed.
- Its author report checks the duplicate-mountpoint delta ("Delta 4 … not applicable") but has no parent-ID delta.
- The sealed `ImplQuota.md` v2 table (delta #8) already applied the parent-ID rule.
- So the amendment sentence "No existing case expectation changes beyond the already-corrected stack" could be falsified from sealed bytes alone at seal time.

This is a seal-internal inconsistency, not a production defect. lesson23 lines 106–112 already concede it. I agree with Main's ruling: no special-casing, exclusion or relabelling, and strict C2 stays UNPROVABLE at 29/30.

### F7 — The additional driver failure has the same root (A4)
measure4 (`evidence/measure4/summary.json`) fails exactly two checks, C34 and C30. Report both, not just one.
- C34 `c2_after_every_case_matches`: 29/30, unmet 1.
- C30 `c2_oracle_real_control_agrees`: 30/31, unmet 1.
  - The unmet row is `results[7] CaseEscapedSpace.json` (case sha `8340738a…`) in `c2-after-real-observed.json`.
  - Its `real_control` headline has exit, finding and paths all matching.
  - C29 `c2_real_control_matches_frozen` passes: `QUOTA_DISABLED`, fleet root on btrfs `/home` `btrfs_qgroups_dir_absent`, `/tmp` on xfs `xfs_noquota_option`.
- Supplementary checks are 274/274 without the real control and 284/284 with it.

### F8 — The sealed driver cannot see F4-class holes (A1, A2)
- C05 and C06 only assert that the case and proposal counts are above 0 (observed 30 and 27).
- C08 binds frozen copies seal → revision, but nothing binds `case-decisions.json` `selected` paths and hashes to committed source files. That is why F4 passed every check.
- The driver is sealed and must not change this round.

Smallest correction: a separate static receipt in the next round, or a driver for a later round, checking that every decision row's `selected` blob exists at the seal with the declared sha.

### F9 — A sealed W1 report is mutated in the working tree (A5)
- `git status` shows ` M .ufo/waves/round-23/build/RevengeTmpfsQuota.md`.
- The sealed blob at `22772c1` is sha `bb1722f4…8e4c`. The working copy is `67c53f1d…473e`: 51 appended lines headed "Addendum — enforcement-off semantics (ReopenS084 followup …)", mtime 15:38:39 -03:00, after HEAD.
- The path is outside the seal manifest, so C12 does not catch it.
- It mutates the identity of a W1 seat's report in place. I do not infer the writer beyond the self-label.

Correction:
- Do not commit this into the W1 report path. Keep the W1 bytes `bb1722f4…`.
- Retain the addendum as a W2 ReopenS084 artifact under `falsify/`.

### F10 — Production lineage after the seal: acceptable (A1, A4)
- Production `1979a9d` equals ImplQuota v3 (`5199e97b…5129`, hash pinned in the sealed `ImplQuota.md` line 415) except two `limits` lines, which change a list into a joined string.
- Later edits are all production-only. None touches frozen bytes or expectations:
  - `5729e7f`: one-line return unpacking, after measure1 showed C2 at 5/30.
  - `56ac3ba`: nonempty paths, exact path-record keys, and two selftest arms.
  - `f3dc07c`: the selftest `escaped-mount-point` arm input gets st_dev 259:2.
- The selftest arm is distinct from frozen CaseEscapedSpace: there, `device_mismatch` preempted the arm, while the frozen case is a parent-ID refusal.
- `quota-selftest-corrected.json` shows 49 arms, exit 0, `QUOTA_SELFTEST_OK`.
  - Minor gap: the receipt carries no `tool_sha256`. It names the working-tree path and self-labels `measured_revision`.
  - Today that path's bytes equal the `f3dc07c` blob (`e4857413…`), so it is consistent now, but the byte binding is not in the receipt itself.

### F11 — C1 checked on its own: holds (A3)
- measure4 C17: before 25/26, unmet `[R25]`.
- C18: after 26/26, unmet `[]`.
- C19: `misleading_alias_runs` 8 → 0.
- C20: 18/18 parsed runs carry schema v2.
- C21: byte guard against the entering source after exactly two transforms.
- C22: three mutants, all rejected.
- C23: 18 same-instance arms, no divergence.
- C24: selftest v1 → v2, alias absent.
- C25: real control 86/5/… matches, argv and inputs match.
- C26: alias 4 → absent.
- C35: identity pins plus twin.
- Pins (C11): `c1-requirements.json` pins contract `2bb35aef…`, oracle `a55b2b50…`, r22 builder `1b3e16f7…` and r22 requirements `48ea2369…`. These equal the seal and revision blobs.
- `oracle-rename.py`, `c1-requirements.json`, `c1-expected-real.json` and `c2-expected-real.json` are unchanged since `4dc80c1`.

Chronology note, no harm: `c1-source-delta.json` landed at `c1e8b81` and `c1-expected-real-identities.json` at `22772c1`, not with the contract at `4dc80c1`. Both feed supplementary guards only (C21, C35), never original26, and both precede production.

## Debt carried, unchanged
Four unallowlisted retention hits (raw 95 / allowlisted 86 / non-author 5); original permission control RED 11/12; two unknown historical dispositions; baseline acceptance blocked; `privacy_clearance=false`. Nothing here clears, admits or promotes anything.

## Installs
None.
