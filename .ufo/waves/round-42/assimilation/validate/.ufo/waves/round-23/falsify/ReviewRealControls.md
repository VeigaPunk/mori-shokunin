# ReviewRealControls — round 23 falsification (source-only)

Seat: `MadoR22-2.ReviewRealControls` (reviewer). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`
Production pinned: `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` · Expectation seal: `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`

## Scope and method

Axes assigned: (a) the frozen default two-path real observation, (b) the r21 real identity/control
receipts, (c) semantic limits, (d) root topology, (e) C1 count-vs-list equality.

Method: **source and committed evidence only**. No tool was executed, no selftest, no driver, no
quota/host read, no source/expectation edit, no sibling or fleet write. Every numeric claim below was
re-derived from committed bytes with `git show` / `git cat-file` and from the committed measure4
evidence JSON. No tools were installed (nothing to install for this scope).

## Verdict summary

| Axis | Result |
|---|---|
| C1 count-vs-list equality | **Holds.** Independently re-derived; receipt lists equal derived lists element-for-element. |
| C1 real control (r21 identity/control) | **Holds.** Exit 0 `RETENTION_RECONCILED`, alias absent, identity digests reproduce; source-delta guard holds byte-exactly. |
| Frozen default two-path real observation (C2) | **Reproduced exactly** by the pinned driver; the sealed oracle's real headline passed with `reason: null`. |
| Semantic limits | **Implementation conforms** to the sealed rules; two output-level limit gaps (S5, S6). |
| Root topology | **Gap in the frozen artefact** (S2): the topology fact the sealed rule depends on is not recorded in the frozen bytes. |
| C2 strict coverage target | **Still UNPROVABLE at 29/30.** Unchanged by this review. Two red checks (C34, C30) both descend from the single frozen `CaseEscapedSpace` contradiction. |

No new failure was found in C1. The C2 reds are retained as instructed; **no special-casing, exclusion,
relabelling or rewrite** of `CaseEscapedSpace` is proposed here.

---

## Findings by severity

### S1 — Medium — Driver check `C30.c2_oracle_real_control_agrees` is unsatisfiable in this wave and its red must not be reported as a real-control failure

* Evidence: `.ufo/waves/round-23/build/MeasureDriver/measure-round23-v2.py:1108-1112` requires
  `oracle_real_counts['unmet'] == 0` over the oracle's **combined** case+real-control denominator.
  `evidence/measure4/c2-after-real-observed.json` → `counts = {total: 31, pass: 30, unmet: 1}`, and the
  single unmet row is `CaseEscapedSpace.json` (`results[].status = "unmet"`,
  `headline = {exit_match:false, finding_match:false, paths_match:false}`) — the frozen contradiction
  recorded in `evidence/frozen-contradiction.json`.
* The same file's `real_control` entry reports `headline = {exit_match: true, finding_match: true,
  paths_match: true}` and `reason: null`; all 284 supplementary checks pass
  (`supplementary_counts = {total: 284, pass: 284, unmet: 0}`).
* The driver's own real-control check `C29.c2_real_control_matches_frozen` **passed**
  (`evidence/measure4/summary.json`), and `evidence/measure4/c2-real-control.json` is byte-consistent
  with `frozen/c2-expected-real.json` on every pinned field.
* Impact: C30's red is a **denominator conflation** — it re-counts the frozen case contradiction as
  evidence about the real control. Reporting "the C2 real control failed" would be false; the correct
  statement is: *the real control passed on its own terms; C30 is unsatisfiable while
  `CaseEscapedSpace` stays red.* Both C30 and C34 must be reported as one cause (the frozen
  contradiction), not as two independent failures.
* Recommendation (advisory only; no code change proposed here): a future driver revision should read
  the oracle's `real_control.status`/`reason` rather than the combined `unmet` counter.

### S2 — Medium — The frozen default two-path real observation does not record the root topology its own sealed rule depends on

* `frozen/c2-expected-real.json` records only two mountinfo lines:
  `"65 33 0:30 /@home /home ... - btrfs /dev/mapper/root ..."` and
  `"244 33 259:1 / /tmp ... - xfs /dev/nvme0n1p1 ..."`. Its `observation_commands` includes the `"/"`
  filter (`awk '$5=="/home" || $5=="/tmp" || $5=="/"' /proc/self/mountinfo`), but the `observed` object
  does **not** record the `"/"` mount's id.
* The sealed rule (`preseal-amendment.md`, "Final pre-seal clarifications"; implemented in
  `tools/mori-quota-surface.py:407-463` `covering_mounts`/`resolve_mount`) refuses with
  `unknown / n/a / ambiguous_overmount` when the chosen mount's **parent id is present in the snapshot**
  but is not the id of the **longest strictly-shorter covering mount**. For both default paths the only
  strictly-shorter cover is `"/"`, and both recorded lines carry parent id `33`. The branch taken
  therefore hinges on the id of the `"/"` mount — a host fact absent from every committed byte I could
  read.
* Consequence: the frozen control is **not self-sufficient for re-derivation**. If the root mount's id
  were ever not `33`, a fully conforming implementation returns `ambiguous_overmount` for *both* default
  paths → exit 2 `QUOTA_STATE_UNKNOWN`, i.e. a frozen exit 0 could be contradicted by correct code.
  The measured run at `f3dc07c` produced the frozen rows (so the topology held on 2026-10-21), and the
  frozen `note` already labels later divergence as host drift rather than an oracle rewrite — so the
  practical exposure is bounded, but the artefact is under-specified.
* Note the rule is deliberately asymmetric (an absent parent id means "unknown topology" and triggers no
  refusal). The frozen bytes do not say which branch applies, so they cannot settle it either way.

### S3 — Low — The real control does not pin the supplementary per-path metadata (`quota_option_keys`, `btrfs_qgroups_mode`)

* `frozen/c2-expected-real.json` → `expected_paths[]` carries exactly seven keys (the six scored
  primary fields + `device_check`). The deployed tool emits nine.
* `oracle-quota.py` `evaluate_real` compares only `PATH_KEYS + ("device_check",)` and builds
  `per_index` from `SUPP_PATH_KEYS` **present in the expected entry** — empty for the real run — so no
  supplementary path check runs against the real observation; `measure-round23-v2.py:1094` (C29)
  likewise compares seven fields.
* Observed values were semantically correct (`btrfs → quota_option_keys: []`, `btrfs_qgroups_mode:
  null`; `/tmp → ["noquota"]`, `null`), but a real-mode drift in those fields — e.g. btrfs emitting an
  option key, or a non-null `btrfs_qgroups_mode` in real mode — would pass **both** the driver check and
  the sealed oracle for the real control. The fixture cases do pin them (284/284 supplementary pass).
* Partial mitigation already in place: C29 pins the observed **path set** by equality, so an extra or
  missing default path would be caught.

### S4 — Low — The deployed production probe is not byte-identical to the preserved candidate it names; the preserved candidate copy is broken

* `tools/mori-quota-surface.py` at `f3dc07c` (sha256 `e4857413…`, 1920 lines) opens with
  `"""mori-quota-surface-v3.py — read-only quota-surface probe (FR2 / EDQUOT).` and describes itself as
  "a new candidate authored alongside `mori-quota-surface.py` (the original, unaltered) and
  `mori-quota-surface-v2.py`". Its deployed **path** is `tools/mori-quota-surface.py`.
* Tree content: `.ufo/waves/round-23/build/ImplQuota/mori-quota-surface.py` (the original, 1376 lines),
  `…/mori-quota-surface-v2.py`, `…/mori-quota-surface-v3.py` (sha256 `5199e97b…`).
* `build/ImplQuota/mori-quota-surface-v3.py` differs from the deployed file in five hunks, and two of
  them matter:
  * it still contains the pre-repair unpacking `state, enforcement, basis, mode = classify(...)` while
    `classify` returns a 2-tuple → `ValueError` on every classification (the repair landed in the
    production path at `5729e7f` and was never folded back into the preserved copy);
  * it emits `"limits": list(LIMITS)` instead of the contract's **fixed boundary text** string; the
    deployed runtime emits the joined string, which is what the oracle's `limits_text` check and the
    frozen `limits` value require.
  * plus the tightened fixture validation and the corrected selftest fixture device input.
* Impact: any reviewer, mutator or connector that takes `build/ImplQuota/mori-quota-surface-v3.py` as
  "the v3 source" works from bytes that cannot run and whose `limits` shape violates the contract. The
  **deployed** runtime is the contract-conformant one; the preserved candidate copy is stale evidence
  only. Identity hazard for rerouting, not a behavioural defect in production.

### S5 — Low — The machine-readable verdict is path-scoped but not labelled as such

* `frozen/c2-expected-real.json` note: *"/dev/shm (tmpfs usrquota) is observed but outside the default
  paths."* The tool's default scope is exactly `(fleet root, /tmp)` (`tools/mori-quota-surface.py:150`).
* The emitted JSON carries `finding_id: "QUOTA_DISABLED"`, `exit_code: 0` and no scope qualifier in any
  machine-readable field (the docstring says "every probed path is visibly quota-disabled"; the `limits`
  string does not say the verdict covers only the probed paths). A consumer reading `finding_id`/`exit_code`
  alone could over-generalise a two-path verdict to the host, which the same host contradicts
  (`/dev/shm` tmpfs `usrquota`).
* Low severity: the frozen file states it in prose and the finding is a runway-reporting signal, not a
  failure claim.

### S6 — Info — The real-mode resolution side-effect limit is not stated in the output

* `preseal-amendment.md` ("Boundary and scope"): *"realpath/stat can trigger automount or block on
  remote filesystems; no guarantee of effect-free resolution on arbitrary paths."*
* `tools/mori-quota-surface.py:155` `LIMITS` enumerates eight quota/df/EDQUOT limit sentences but omits
  the automount/block caveat, while `real_inputs` performs `os.stat` and `os.path.realpath` on every
  operator-supplied `--path`. The "operator-pinned runway target" nature of non-default paths appears
  only in the docstring, not in the output.

### S7 — Info — The identity-pin qualification understates one of its three links

* `frozen/c1-expected-real-identities.json` calls all three digests a *"Co-evolved transcription of
  retained receipt identities and independently applied frozen non-author globs; not historical execution
  authentication."*
* Independent check: the frozen `raw_hits` digest `c275d2c2…` is byte-identical to the SHA-256 of the
  **r21 receipt's own `hits` list** as committed at `77a5bbe`
  (`.ufo/waves/round-21/evidence/final/retention-floor.json`, receipt sha256 `4001e2d9…`). That link is
  therefore historically anchored to the r21 run. `scanner_hits` / `policy_excluded_hits` are genuinely
  co-evolved (they are the result of applying the frozen non-author globs), matching the file's wording.
* No clearance implication in either direction: the tool itself reports `receipt_authenticity:
  "unattested"` and `privacy_clearance: false`.

---

## Verified positives (evidence for the claims, independently re-derived)

**P1 — C1 count-vs-list equality holds, and the arithmetic is structural, not coincidental.**
From `evidence/measure4/c1-real-control.json`: `raw_total 95 = len(raw_hits) 95`;
`scanner_total 90 = len(scanner_hits) 90`; `policy_excluded 5 = len(policy_excluded_hits) 5`;
`non_author 5 = policy_excluded`; `allowlisted 86`; `scanner_unallowlisted 4`;
`raw_not_allowlisted 9 = 95 − 86`; `forbidden_allowlist 0`. `scanner ∪ excluded = raw`, disjoint.
In the source (`tools/mori-retention-reconcile.py:233-236`) `raw_not_allowlisted` counts **hits** whose
`(path,class,line_sha256)` is not in `allowed_keys`, while `allowlisted` counts the **same hit
population** that is in `allowed_keys` → `95 − 86 = 9` holds by construction at hit level.
I re-derived the populations independently from the r21 receipt at `77a5bbe` plus the frozen policy
globs and the committed allowlist: `allowed 86`, `forbidden rows 0`, `scanner_unallowlisted 4`,
`raw_not_allowlisted 9`, and the receipt's own `unallowlisted_hits` (4) and `allowlisted_hits` (86)
lists are **element-for-element equal** to my derived lists.

**P2 — The three frozen identity digests reproduce.**
Recomputing the frozen encoding (SHA-256 of `json.dumps(sorted full 4‑tuples)`, separators `,`/`:`,
default `ensure_ascii`) from the measured output gives `raw_hits c275d2c2…`, `scanner_hits 9690b3a9…`,
`policy_excluded_hits 17c348f0…` — identical to `frozen/c1-expected-real-identities.json`. Independently
re-derived from the r21 receipt bytes: `raw_hits c275d2c2…` (the receipt's own `hits` list),
`scanner_hits 9690b3a9…` and `policy_excluded_hits 17c348f0…` (globs applied by me). Driver check
`C35.c1_real_identity_pins` passed.

**P3 — The misleading alias carried the policy-filtered count; the true raw complement is 9.**
Entering arm `raw_unallowlisted = 4` equals the after arm's `scanner_unallowlisted = 4`, while the
genuine raw complement is `9`. This is exactly the defect the cutover removes, and it is confirmed by
the entering-arm value, not by name similarity.

**P4 — Before/after outputs are identical apart from the three declared exceptions.**
`evidence/measure4/c1-real-control-entering.json` (wrapper) → `stdout` parsed vs
`evidence/measure4/c1-real-control.json`: key-set difference is exactly `['raw_unallowlisted']`;
no non-exempt key differs (schema, `tool_sha256` and `argv` exempted — and `argv` is in fact
identical). All **18** same-instance replay pairs show `keysΔ = ['raw_unallowlisted']` or `[]` and
`non-exemptΔ = []`, with exit codes and finding ids equal pair-wise
(`RETENTION_RECONCILED` / `RETENTION_RECONCILIATION_MISMATCH` / `RETENTION_RECONCILIATION_SETUP`).
No key, value, exit code or finding id moved.

**P5 — The C1 source-delta guard holds byte-exactly.**
`git show 1bfe708:tools/mori-retention-reconcile.py | sha256sum` = `0795bac9…` (= frozen
`entering_sha256`); applying exactly the two frozen replacements
(`SCHEMA='mori-retention-reconciliation-v1'`→`…-v2`, deletion of
`'raw_unallowlisted':len(unallowed),`) yields `4599ee1a…` (= frozen `transformed_sha256`), and
`git show f3dc07c:tools/mori-retention-reconcile.py | sha256sum` = `4599ee1a…`. No other source byte
changed.

**P6 — The frozen controls are byte-identical between seal and production.**
`git ls-tree` on `22772c10` and `f3dc07c` yields the same blob ids for every `frozen/` artefact,
including `c1-expected-real.json` (`86897dc3…`), `c1-expected-real-identities.json` (`5da898c2…`),
`c2-expected-real.json` (`3169b32a…`) and all 30 quota cases. The C1 inputs are anchored: the receipt
blob at `77a5bbe` hashes to `4001e2d9…`, matching `frozen/c1-expected-real.json:inputs_sha256`, and the
tool's emitted `inputs_sha256` equals the frozen object exactly.

**P7 — The frozen default two-path real observation was reproduced exactly.**
`evidence/measure4/c2-real-control.json` == `frozen/c2-expected-real.json` expectations: exit 0,
`QUOTA_DISABLED`; fleet root `/home/vgpnk/Projects/shokunin` → btrfs, `/home`, disabled,
`btrfs_qgroups_dir_absent`, `btrfs_subvolume_skipped`; `/tmp` → xfs, `/tmp`, disabled,
`xfs_noquota_option`, `match`. Driver `C29` passed; the sealed oracle's real headline is
`exit/finding/paths` all true with `reason: null`.

**P8 — The semantic-limit implementation matches the sealed rules (source-read only).**
`tools/mori-quota-surface.py`: btrfs qgroups absence yields `disabled`/`btrfs_qgroups_dir_absent` **only**
via `FileNotFoundError` (any other `OSError` → `qgroups=None` → unknown, never absent/disabled) —
`scan_btrfs_sysfs` (`:571-…`); a parent sysfs listing failure returns an empty map → `btrfs_device_unmapped`
(unknown), never disabled; device mismatch preempts the filesystem table for every fstype; btrfs skips
device equality **only** when the stat major is 0 (frozen fleet-root `st_dev 0:57` → `btrfs_subvolume_skipped`);
real mode never opens `qgroups/mode` (mode stays null — the S079 safety correction); xfs precedence is
conflict → `noquota` → enforced key → accounting-only key → absent; tmpfs hardlimit vocabulary is
restricted to the four documented keys; ext2/3/4 is always unknown (`ext_quota_option_unverified` vs
`ext_quota_superblock_unobservable`); no mount source, option value, UUID or file name from option values
is echoed; `df_covers_quota` is always false; verdict precedence enabled > unknown > disabled
(`verdict`, `:561`).

**P9 — The selftest arm correction is a fixture-input correction, and it is a different arm from the frozen case.**
`evidence/quota-selftest-delivered.json` (revision `56ac3ba`) failed the `escaped-mount-point` arm with
`device_mismatch` (the fixture's `st_dev` did not match the mount device);
`evidence/quota-selftest-corrected.json` (revision `f3dc07c`) is `arms: 49, exit 0`. The production diff
against the preserved candidate shows the correction is the **fixture input**
(`path_entry("/srv data", st_dev="259:2")`), not the expectation — the arm still requires
`RC_ENABLED`/`ENABLED`/`xfs_quota_option`. That arm (mount point `"/srv data"`, single mount) is
distinct from the frozen `CaseEscapedSpace` case (mount ids 43/33/42, path `"/srv/my data/sub dir"`,
`/srv` cover). Keep the two apart; the selftest green is not evidence about `CaseEscapedSpace`.

**P10 — Headline claim status for this seat's scope.**
C1 (calibration): **held 5** — original 26 requirements 25/26 before (R25 red) → **26/26 after**, alias
runs 8 → 0, schema v2 in every parsed run, real control reproduced, count-vs-list equality independently
confirmed, source-delta guard byte-exact, supplementary guards green. No new failure observed in scope.
C2 (coverage): strict target **remains UNPROVABLE at 29/30** — unchanged by this review; the two red
checks are `C34` and `C30`, both descending from the single frozen `CaseEscapedSpace` contradiction, and
`C30` must be attributed as a denominator conflation (S1), not as a real-control failure.
`privacy_clearance` remains false; carried debt unchanged (4 unallowlisted hits, original permission RED
11/12, two unknown dispositions, baseline acceptance blocked). No clearance, health or admission claim is
made or implied by this report.

---

## Residual risks and verification gaps

1. **No host read by this seat.** The C2 real observation is verified only as *reproduced by the pinned
   driver* at `f3dc07c` on 2026-10-21; current host state may differ (the frozen note treats divergence
   as drift, not an oracle rewrite).
2. **Root topology (S2) is unverifiable from committed bytes.** The `"/"` mount id, and whether id `33`
   is present in the snapshot at all, appear in no committed file I could read; the parent-ID branch taken
   by the real observation cannot be independently confirmed.
3. **Real-control supplementary fields are unpinned (S3).**
4. **The r21 receipt was re-verified by replay, not by re-executing the original r21 run at its own
   revision**; `summary.json:scope_notes.r22_reproduction` records that the r22 reproduction was not
   attempted. The C1 identity chain is therefore: committed r21 receipt bytes → independently re-derived
   populations → frozen digests → measured output, with `receipt_authenticity: "unattested"`.
5. **Candidate-vs-production drift (S4)** means preserved build copies cannot be used as mutation
   baselines for the deployed quota runtime.
6. **The frozen `CaseEscapedSpace` contradiction remains unresolved by design.** I propose no
   special-case, exclusion, relabelling or rewrite of it, and no oracle change that would convert 29/30
   into a demonstrated pass.
