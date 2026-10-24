# ConnectCountsFinal — denominator/name connect audit (r23 falsification lane)

Seat: `MadoR22-2.ConnectCountsFinal` (connector, W2 batch of 96, one task call).
Scope: connect the *independently measured* names/denominators of C1 and C2 to each
other and to the W1/W2 seat histories; flag conflation and incomplete provenance.
Read-only seat: no code, contract, oracle, frozen-case, registry or lane-index edit;
no driver/oracle/selftest execution; no quota tool, mount, qgroup or host read.
Only read-only `git show/log/status/rev-parse/ls-tree/cat-file/merge-base/diff` and
file/JSON reads were used.

Pinned facts used (all bytes verified locally):
- production pin `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`; expectation seal
  `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`; dispatch-payload commit
  `6eb889c037163e4886eaa61501258910d6a529b9` (descendant of the pin).
- `.ufo/waves/round-23/evidence/measure4/summary.json` sha256
  `381e963e04c3bcfec64b4b7841ba2a921bd68defbc2f7953a857631d37542353`
- `frozen/case-decisions.json` `b05a007262b52ab0266bd2e7b6a55d8fa05aab8fc518243036e84638960bc60a`
- `frozen/seal-manifest.json` `8ff351f2dec6509d09865e827ffadb8341e522076ad88699ae433be07321c082`
- `oracle-quota.py` `f1f4a027728180436fc5161171b0f6ad4ca4176229b5240aabb33e3f2af36bec` ·
  `oracle-rename.py` `a55b2b50d3e7447a1d5312c8b066a13137a6a6895f0343b3240ebf081d97c5f2`
- `frozen/quota-cases/CaseEscapedSpace.json` `8340738a509e474a94a815637e66b407dfb60c6449511e52db55296d844abeea`
- `evidence/source-accounting.json` `3e021f5f5d7407e006ff379f62d5b0203e8a7ec9f1f3f376415de62d0b54f92b`
- `evidence/frozen-contradiction.json` `e06e90b76983a0f8df6542e70f19d4a2d89b12e35cea3c9bce4abfe11a8ff771`
- `evidence/quota-selftest-corrected.json` `5901b38ac63299fae9f2d27f23e64fb69bab803c2d190d7829650688bb80fbe8`
- `corpus/SOURCES.md` `1f49a4d8338a48f7a85c0614ab24261b5b113d858259e41c30f0f0930ff6ad09`
  (working tree == committed blob at the pin) · `corpus/lessons/round-23.md`
  `93cfe32de5d36731fa266478120ff1565d1bdd7822868598624025e185e1339b` ·
  `corpus/knowledge/quota-surface-r23.md` `2614a8f133072b27a3d5e07a7ad5d70455f509ef4052c01a9ad7e112879b8c84`

---

## 1. Axes named

| # | Axis | What counts as green here |
|---|---|---|
| A1 | **Denominator integrity** | every reported count resolves to exactly one named denominator, stated with its artifact and byte identity |
| A2 | **Name/namespace separation** | `supplemental`, `source`, `86`, `8` are not used for two different quantities in one report surface |
| A3 | **Provenance completeness** | each count is traceable to (seat lineage → artifact → digest → revision), not to an aggregate only |
| A4 | **No-harm / freeze integrity** | no frozen case/rule/oracle/contract byte changed; strict C2 red stays red; no admission, clearance or promotion implied |
| A5 | **Honest attribution** | a red in one artifact is not silently re-attributed to another artifact (host real control vs case set) |

---

## 2. C1 — "26 original" and "alias 8→0" are two different denominators, both real

**Observed (measure4):** `c1_original_26` before `pass 25 / total 26 / unmet ["R25"]`,
after `pass 26 / total 26 / unmet []`; `misleading_alias_runs` before `8`, after `0`;
oracle exits before `1`, after `0`. `denominators.c1_original_requirements = 26`
(driver constant `C1_REQUIREMENT_COUNT = 26`, `measure-round23-v2.py:108`).

**Connected denominators (all from `evidence/measure4/c1-before-observed.json` /
`c1-after-observed.json`, both `parsed_runs: 18`, `run_count: 18`):**

| quantity | value | exact meaning | where |
|---|---|---|---|
| requirement ids | 26 (`R01`…`R26`) | the **original** denominator | `frozen/c1-requirements.json` (ids list), `oracle-rename.py` `data['results']` |
| tool invocations (arms) | 18 | distinct fixture invocations the oracle made | `data['runs']`, variants `valid, drop, inject, digest, line, class, metric, forbidden, invalid-revision, diverged, policy-changed, allowlist-changed, malformed, bool-line, duplicate, bool-metric, valid(receipt-override), symlink` |
| check-shaped outputs | 8 | arms whose stdout is a check document | driver check `C23.c1_same_instance_output_equivalence` → `shapes {check: 8, setup: 10}` |
| setup envelopes | 10 | arms whose stdout is a setup document (never carried the alias) | same check |
| alias-bearing runs before | **8** | exactly the 8 check-shaped arms | `misleading_alias_runs` (oracle) = 8; equals `shapes.check` = 8 |
| schema-v2 runs | 0 → **18/18** | every parsed run, not just the 8 check arms | `schema_v2_runs` 0 before / 18 after; driver `C20` |
| driver checks standing for the 26 | 4 | `ORIGINAL_26_CHECKS = (C17, C18, C19, C20)` | `measure-round23-v2.py:111` |

**Requirement→arm mapping [INFERENCE from `oracle-rename.py` source, cross-checked
against the observed 18-run variant list]:** 16 of the 26 ids (R01–R12, R22–R24, R26)
read a **check** output and are carried by the 8 check arms (R01–R04, R22–R24, R26
all share the single `valid` arm; R11/R12 share `forbidden`); 9 ids (R13–R21) are
carried by 9 setup arms, and R18 asserts **two** arms (`bool-line` and `bool-metric`,
the code comment says "conjunctive in R18, not a hidden extra requirement"); R25 is
computed over all 18 runs. 16 + 9 + 1 = 26 ids over 18 invocations.

**Conflation risk A2 (real).** "alias 8→0" has **no denominator attached in any
receipt surface**: `summary.json` → `c1_original_26.misleading_alias_runs {before: 8,
after: 0}` and `oracle stdout` → `counts.misleading_alias_runs = 8`. The denominator
(18 parsed runs / 8 check arms) exists only in the oracle JSON body
(`parsed_runs`, `schema_v2_runs`) and in the driver check `C20.parsed_runs = 18`.
A reader who sees "8" next to "26 requirements" will read "8 of 26 requirements
carried the alias" — **that reading is wrong**; the correct statement is
"8 of 18 parsed invocations (all 8 check-shaped arms) carried the alias before;
0 of 18 after; schema v2 went 0/18 → 18/18". Also note the before-arm red is
**exactly** R25 (alias+schema), as pre-registered — that is the only unmet original
requirement, and it is the same fact the "8" measures, so "8" and "25/26" must not be
added as independent evidence.

**Pre-registered and honoured.** `frozen/c1-requirements.json.before_expected`
= `{"misleading_alias_runs": ">0", "unmet": ["R25"]}` — matches the observed
before-arm exactly (8 > 0, only R25 unmet). No expectation was tuned to the result.

---

## 3. C2 — three different "supplemental" quantities that must never be merged

**Observed:** `c2_oracle_after` → `counts {pass 29, total 30, unmet 1}`,
`supplementary_counts {pass 274, total 274, unmet 0}`, `tool_present true`;
`c2_oracle_before` → `counts {capability_absent 30, pass 0, total 30}`,
`supplementary_counts {pass 0, total 0, unmet 0}`.
`denominators.c2_sealed_cases = 30`; driver `C34` `pass 29/30` (red);
`C30` (oracle with `--real-expected`) `pass 30 / total 31 / unmet 1`.

**(i) 30 sealed cases = 27 primary + 3 source-review supplemental.**
`frozen/case-decisions.json`: `selected_cases 30`, `independent_primary 27`,
`source_review_supplemental 3`; 30 decisions, of which `primary: true` for 27 and
`primary: false` for exactly `SupplementHiddenMount`, `SupplementQgroupDisabled`,
`SupplementQgroupUnknown` (reason: "Source-review discovery guard before candidate
inspection/result"). `frozen/seal-manifest.json` repeats `primary_c2 27`,
`source_review_supplemental_c2 3`, `c1_original_requirements 26`,
`supplementary_never_redefines_primary_denominator true`.
Directory census: `cases-proposed` 27, `cases-corrected` 27, `cases-supplemental` 3,
`frozen/quota-cases` 30. Driver check `C04` reports `sealed_cases 30,
sealed_proposals 27` (the 27 original proposals are retained in `cases-proposed/`).

**(ii) 274 = per-case output-property checks, a different axis.** From
`evidence/measure4/c2-after-observed.json`: every case carries 9 base supplementary
checks (`schema, exit_consistency, output_keys_allowed, output_key_set, error_token,
path_key_set, df_covers_quota, limits_text, no_leakage`); `CaseSetupMalformed.json`
carries 10 (adds `setup_no_partial_verdict`); `CaseBtrfsDevMatch.json` carries 12
(adds `device_check[0], quota_option_keys[0], btrfs_qgroups_mode[0]`).
28×9 + 1×10 + 1×12 = **274** exactly.

**Conflation risk A2 (real, and it hides a fact).** The word "supplemental" is used
for (a) the 3 **cases** counted *inside* the 30-case denominator, and (b) the 274
**checks** counted *outside* it. The two are not interchangeable and one of them
covers the red case: **CaseEscapedSpace's own 9 supplementary checks all PASS**
while its primary expectation is `unmet`. So "supplementary 274/274" and "primary
29/30" measure disjoint properties; quoting them side by side without labels invites
the false conclusion that only the six-field tuple is in dispute, or conversely that
"everything else is green" implies the primary row was wrong. Additionally, the
274-check axis has **no before-arm** (0/0, tool absent) → it is an after-only
measurement and cannot be presented as a before→after delta.

**Conflation risk A2 (aggregate).** The headline "29/30" silently mixes two
provenance families: 27 independently-authored primary cases and 3 source-review
discovery guards. The driver's own denominator surface (`denominators.c2_sealed_cases
= 30`) does **not** carry the 27/3 split; the split survives only in
`frozen/case-decisions.json` (committed, sealed) and in the hand-written
`evidence/frozen-contradiction.json` (`primary_pass 26 / primary_total 27`,
`supplemental_pass 3 / supplemental_total 3`) — the latter is a connector-produced
evidence artifact, not a driver computation. The 26/27 + 3/3 split is *derivable*
from committed bytes (case-decisions `primary` flags × the single unmet case), and it
is consistent with `pass 29/30`, but the driver never recomputes it.

---

## 4. The one red: provenance of the frozen contradiction (now identified)

`frozen/quota-cases/CaseEscapedSpace.json` (sha `8340738a…`) is byte-identical to the
sealed decision (`case-decisions.json` → id `CaseEscapedSpace`, selected
`cases-corrected/CaseEscapedSpace.json`, `selected_sha256 8340738a…`, `primary true`).
Its fixture mountinfo is:

```
33 2 0:30 /@ / rw,… - btrfs /dev/mapper/root …
42 33 0:44 / /srv rw,… - xfs /dev/mapper/srv rw,…,noquota
43 33 0:45 / /srv/my\040data rw,… - xfs /dev/mapper/data rw,inode64,usrquota,attr2
```

For path `/srv/my data/sub dir` the chosen mount is **43** (longest component-prefix
cover, `\040` decoded), the **parent id** field of that mount line is **33**, and the
longest *strictly shorter* covering mount is **42** (`/srv`). The pre-seal amendment's
final clarification ("refuses when the chosen mount's parent ID is present in the
snapshot but is not the ID of the longest strictly-shorter covering mount … use
unknown/n/a/ambiguous_overmount with null fstype/mountpoint and not_checked
device_check") therefore pre-empts classification: the observed output is
`fstype null, mount_point null, quota_state unknown, enforcement n/a, basis
ambiguous_overmount, device_check not_checked`, and the run verdict becomes
exit 2 `QUOTA_STATE_UNKNOWN`. The frozen expectation demands
`xfs / enabled / enforced / xfs_quota_option` and run verdict exit 1 `QUOTA_ENABLED`.

**Where the contradiction comes from (new, byte-level).** The frozen case's own
`rationale` field enumerates the refusals it believed did *not* touch it: "The
duplicated-covering-mountpoint → unknown/null fstype+mount_point/ambiguous_overmount
change does not touch this case: each covering mountpoint ('/', '/srv', '/srv/my data')
occurs exactly once in the mountinfo, so no overmount refusal is triggered." The case
rationale is written against the **duplicate-mountpoint** refusal and does not
account for the **parent-ID** refusal, which was added in the amendment's
"Final pre-seal clarifications" block. The frozen case's `sources` are
`["S077","S078","S082"]` — no registry row backs parent-ID topology (S085 backs
mountinfo per-mount emission/escaping, explicitly "not topology inferred from
ordering"). So the red arises from an **L1 policy rule that is not source-derived**,
while the expectation it contradicts is source-derived. Both bytes stay unchanged;
the strict C2 target therefore remains **UNPROVABLE at 29/30** (30/31 with
`--real-expected`, C30 red for the same single case).

Scope of the mismatch is narrow and should be stated as such: the **second** path
(`/srv/plain` → 42 → xfs `noquota` → disabled/`xfs_noquota_option`, `device_check
match`) matches the frozen expectation exactly. Only path 1 and the run-level
`exit_code`/`finding_id` differ — one path plus one verdict, not a general
non-conformance.

**Attribution risk A5 (real).** `summary.json` reports `real_controls_pass: false`
and `all_claim_checks_pass: false`. But `C25.c1_real_control_matches_frozen` **PASS**
(all 15 frozen key values match: `raw_total 95, allowlisted 86, non_author 5,
policy_excluded 5, scanner_total 90, scanner_unallowlisted 4, raw_not_allowlisted 9,
retention_state red, privacy_clearance false`, plus receipt/inputs sha and identity
pins) and `C29.c2_real_control_matches_frozen` **PASS** (host `/home…` → btrfs
`/home` `btrfs_qgroups_dir_absent` `btrfs_subvolume_skipped`; `/tmp` → xfs `/tmp`
`xfs_noquota_option` `match`). The only failing real-control-family check is
`C30.c2_oracle_real_control_agrees`, which fails **because the sealed case set still
contains the one unmet case** (`pass 30 / total 31 / unmet 1`). So "real controls
fail" must not be read as "the host observation disagrees with the frozen control" —
it is the case-set red propagated into that one aggregate check.

---

## 5. "source 76→86" — verified independently, plus a namespace collision

**Independently counted** (read-only `git show`, not the connector artifact):

| revision | `corpus/SOURCES.md` lines | rows starting `| S` | last id |
|---|---|---|---|
| entering `1bfe708a…` | 123 | **76** | `| S076 |` |
| pin `f3dc07c0…` | 136 | **86** | `| S086 |` |

Rows `S077`…`S086` at the pin = **10**; the working-tree file digest
`1f49a4d8…` equals the committed blob at the pin. This matches
`evidence/source-accounting.json` exactly (`before_rows 76, after_rows 86,
new_ids [S077…S086]`, note "Source count only, no frontier/capability admission
implied").

**Incomplete provenance A3 (real).** The sealed contract's C2 sentence still reads
"New read-only probe `tools/mori-quota-surface.py` (sourced: **S077–S084**)" — 8
ids — while the landed registry has 10 (S085, S086 beyond the contract's range).
The amendment licenses this ("Original source IDs S077–S084 were forward assignments,
not existing registry rows; registry and lesson Gate land before sourced knowledge
admission") and `corpus/lessons/round-23.md` explains it ("Additional source rows
085/086 close original source coverage gaps, not implementation-result-selected
evidence"; the Gate table lists all ten with located quotes ≤25 words). Seat
lineage: W1 had exactly eight `Src*` scout seats (SrcXfsDoc, SrcXfsShowargs,
SrcBtrfsSysfs, SrcBtrfsQgroup, SrcBtrfsGetattr, SrcProcMountinfo, SrcExt4Doc,
SrcTmpfsDoc); the two extra rows have **W2-only** provenance (`ReopenS085`,
`ReopenS086` scouts in the 96-seat batch). And the landed knowledge note's own
provenance line is internally uneven: `source: S077–S086` while
`verified-at: … independently re-opened initial eight sources`. Nothing in the wave
touches the sealed contract bytes (C10 proves contract/amendment byte-identical
seal→pin), so this is a **statement-vs-registry lag**, not a byte defect — but any
downstream reader who equates "contract says S077–S084" with "the registry gained
only S077–S084" is wrong by two rows.

**Namespace collision A2 (real).** "86" denotes two unrelated quantities in the same
report surface: **86 registry rows** (source-accounting) and **86 allowlisted
hits** (C1 real control). They live side by side in the round's own context line
("four unallowlisted inherited hits (raw95/allowlisted86/non-author5)") and in
`summary.c1_real_control.keys`. Arithmetic of the hit side: `raw_total 95 −
allowlisted 86 − non_author 5 = 4 = scanner_unallowlisted`; `raw_total 95 −
allowlisted 86 = 9 = raw_not_allowlisted`; `scanner_total 90 = raw_total 95 −
policy_excluded 5`. Also "source" itself is overloaded: **source rows** (SOURCES.md
ids S077–S086) vs **source hits** (scanner/policy hits in the retention
reconciliation). This is the same family of confusion as the retired
`raw_unallowlisted` name (lesson M2) — the same fix pattern (explicit canonical
names) applies to `source`/`86` in ledger prose.

---

## 6. W1 / W2 seat histories

**W1 (64 seats, one payload).** `wave1-ledger.json` (`b9c88666…`) has 8 attempt
records, all for the same payload `sha256 cd8a5fa64e69ce55c0dec70d02d8bf77a3d1fbd27bd3fcf61660a63d3d3cc628`
/ `payload_bytes 88738` / `tasks_count 64`: attempts 1–7 = `result "refused"`,
`started_ids 0`, refusal "Background job limit reached (100)"; attempt 8 =
`result "started"`, `started_ids 64`, at 17:24:14Z. `wave1-attempts.json`
(`e7fe4977…`) supplies the grant lines that explain it: live background jobs at each
attempt were 168 / 153 / 122 / 165 / 146 / 117 (> the 100 cap) and at attempt 8
**92** (≤ cap) — so the single start is a capacity fact, not a retry of a broken
payload. `evidence/wave1-report-presence.json`: **64/64 reports present** with bytes
and sha256, bound to `dispatch_payload_sha256 cd8a5fa6…`.
Provenance caveat already declared by L1 and honoured here: the ledger is a
**retrospective** binding ("retrospective binding; original attempts record
timestamps/results after the call, not a pre-call committed-payload log"), and
`corpus/lessons/round-23.md` repeats it ("seven zero-spawn refusals and one 64-seat
start, not proof of pre-call committed payload logging (Q53/56)").

**W2 (96 seats, one batch).** `wave2-run.json` (`63205203…`, 177691 bytes) →
`counts {spawn 96, resume 0, total 96}`, one `taskCall` with **96 tasks in one call**
(one-swarm-per-wave), role census: reviewer 65, scout 12, mutation-tester 8,
critic 4, connector 3, sentinel 2, scribe 1, simplifier 1 (=96).
`wave2-ledger.json` (`b9e82807…`): attempt 1, `started_ids 96`, `tasks_count 96`,
`payload_sha256 d28cc9f2…`, `payload_bytes 159710`, `payload_revision 6eb889c0…`.
`evidence/wave2-payload-binding.json`: `mori-dispatch-ledger.py bind` exit 0,
`PAYLOAD_BOUND`, same digest/bytes/rev.

**Seat→denominator lineage (A3).** The denominators have seat-level ancestry in the
dispatch payload text: `C1R01`…`C1R26` (26 reviewer seats) ↔ the 26 original
requirement ids `R01`…`R26`; the 30 `Q*` reviewer seats ↔ the 30 sealed cases
(27 primary + the 3 supplemental as `QHiddenMount` / `QQgroupDisabled` /
`QQgroupUnknown`); `ReopenS077`…`ReopenS086` (10 scout seats) ↔ the 10 new registry
rows; `Mut*` (8 mutation-testers) ↔ the C1/C2 mutation arms; `C1R*` ↔ the C1
original-26. **Seat ids are carried by the wave's own registry files, not by the count
artifacts**: `.ufo/waves/round-23/wave2-assignments.json` (96 `seat → agentId`
entries) and `.ufo/waves/round-23/wave2-record.json` (schema `ufo-swarm-registry-v1`,
96 members with `kind`/`agentId`/`role`, reportDir `.ufo/waves/round-23/falsify`).
Both are **untracked until the wave settles**, so a committed count artifact
(`summary.json`, the oracles) carries counts and check ids only — by design, not a
missing field (§10). That separation is what makes "26", "30", "274" and "8" read as
free-floating numbers in *count-only* receipts.

**Two items initially read as provenance gaps A3 — both are withdrawn as gaps in §10
after the L1 ruling and re-derivation; retained here for the audit trail.**
1. **The bound payload digest is not the whole-file digest — by design.** Ledger and
   binding say `d28cc9f2…` / 159710 bytes; the committed and working
   `wave2-run.json` whole-file digest is `63205203…` / 177691 bytes (extra
   `registry` (96 members), `compaction`, `counts`, `policy` fields sit outside the
   canonical payload). §10 re-derives the canonical payload digest from committed
   bytes and it matches exactly (`d28cc9f2…` / 159710); same for W1
   (`cd8a5fa6…` / 88738). The binding is over the canonical `{context, tasks}`
   payload only and is **not** comparable to a whole-file digest. *(Withdrawn as a
   gap.)*
2. **The W2 record and the audited receipts live outside the pinned revision.**
   `git merge-base --is-ancestor f3dc07c0… 6eb889c0…` → rc 0 (the pin **is** an
   ancestor of the dispatch commit; seal ⊏ pin ⊏ 6eb889c0 — no branch anomaly), but
   `git ls-tree f3dc07c0… .ufo/waves/round-23/` contains **no** `wave2-*` file and its
   `evidence/` subtree lists `measure1`, `measure2`, `measure3` only — **not**
   `measure4/`, not `quota-selftest-corrected.json` (both land in `6eb889c0`), and no
   `falsify/` tree at all. So every receipt cited by this round's context
   ("Actual stable receipts …/evidence/measure4/ and quota-selftest-corrected.json")
   is committed **after** the revision it measured. Per the L1 ruling this is a
   **deliberate separation, not a gap**: the measured code pin and the later receipt
   commit are distinct on purpose (the pin freezes the code + expectations under
   measurement; the descendant commit pins the receipts produced against that pin).
   The driver records `measured_revision f3dc07c0…` and `seal_revision 22772c10…`
   and proves `seal ⊏ revision` (C01, rc 0) plus byte-identity seal→pin for 37
   frozen artefacts (C08, C09, C10, C12). *(Withdrawn as a gap; restated in §10.)*

**Quota selftest arm kept separate (as instructed).** `evidence/quota-selftest-corrected.json`
= `{"arms": 49, "exit_code": 0, "finding_id": "QUOTA_SELFTEST_OK"}` at
`measured_revision f3dc07c0…`, argv `python3 -I tools/mori-quota-surface.py --selftest`.
This is the **co-evolved public selftest**, whose `escaped-mount-point` arm is a
*different* fixture from the frozen `CaseEscapedSpace` (per `corpus/lessons/round-23.md`:
the selftest arm "accidentally combines mount259:2 with helper's default stat259:1 …
Correct only its input to explicit259:2"). 49/49 must never be reported as evidence
about the frozen topology case; the frozen case remains `unmet`.

---

## 7. Complete count→denominator ledger (the safe reading)

| reported number | exact denominator | artifact of record | provenance gap |
|---|---|---|---|
| 26 | C1 original requirement ids R01–R26 | `frozen/c1-requirements.json`; `oracle-rename.py` `data['results']` | realised in the driver by only 4 aggregate checks (`ORIGINAL_26_CHECKS`) |
| 18 | parsed oracle runs / fixture arms (8 check + 10 setup) | `c1-before/after-observed.json` (`parsed_runs`) | denominator absent from the printed `counts` |
| 8 → 0 | alias-bearing parsed runs before → after (all 8 check arms) | `misleading_alias_runs`; `C23.shapes {check:8, setup:10}` | **denominator unstated in every printed receipt** |
| 0 → 18 | schema-v2 runs | `schema_v2_runs`; `C20` | ok |
| 5 | C1 supplementary driver checks C21, C22, C23, C24, C35 | `SUPPLEMENTARY_CHECKS` (`measure-round23-v2.py:113`); `denominators.c1_supplementary_guards` | **only 4 guard objects appear under `c1_supplementary.guards`**; the 5th (C35 identity pins) is materialised under `c1_real_control.identity_pins` |
| 27 / 3 | C2 primary cases / C2 source-review supplemental cases (both inside 30) | `frozen/case-decisions.json` (`primary` flags); `seal-manifest` `primary_c2`/`source_review_supplemental_c2` | not carried by `denominators.c2_sealed_cases = 30` |
| 30 | C2 sealed cases (27+3) | `frozen/quota-cases/` (30 files) | aggregate hides the two provenance families |
| 29 / 30 | C2 cases passed (26 primary + 3 supplemental) | `c2-oracle-after.json` `counts` | red is one case (see §4) |
| 274 / 274 | C2 supplementary **output checks** (28×9 + 1×10 + 1×12), incl. the red case's 9 | `c2-oracle-after.json` `supplementary_counts`; per-case `supplementary[]` | **after-only** (before = 0/0); different axis from the 3 supplemental *cases* |
| 30 / 31 | C2 with `--real-expected` (30 cases + 1 real-control requirement) | `C30` | `C30` red inherits the single case-set red |
| 76 → 86 | `corpus/SOURCES.md` rows (10 added, S077–S086) | `evidence/source-accounting.json` + my own `git show` count | contract still names S077–S084; knowledge note `verified-at` says "initial eight" |
| 95 / 86 / 5 / 4 / 9 / 90 | raw_total / allowlisted / non_author / scanner_unallowlisted / raw_not_allowlisted / scanner_total | `frozen/c1-expected-real.json`; `summary.c1_real_control.keys` (all match) | "86" collides with the registry-row 86; "source" overloaded |
| 49 / 49 | quota **selftest** arms (co-evolved public selftest) | `evidence/quota-selftest-corrected.json` | must not be read as evidence about the frozen case |
| 64 / 8 | W1 seats / W1 dispatch attempts (7 refusals + 1 start of 64) | `wave1-ledger.json`; `wave1-attempts.json` (live 168…117 vs 92) | ledger is retrospective, declared by L1 |
| 96 / 1 | W2 seats / W2 task calls | `wave2-run.json` `counts`; `wave2-ledger.json` | bound digest is the **canonical `{context,tasks}` payload** (re-derived, matches; §10), not a whole-file digest; seat ids in `wave2-assignments.json` + `wave2-record.json` (untracked until wave settles) |

---

## 8. Proposed move (one, bounded, no-harm)

**Move: land a single *count→denominator→lineage legend* as a wave **evidence
artifact** (not a driver edit), e.g. `.ufo/waves/round-23/evidence/count-denominators.json`,
and reference it from the falsification report set.**

Content: one row per number in §7 with `{name, value_before, value_after,
denominator, denominator_definition, artifact_path, artifact_sha256, revision,
seat_lineage, provenance_gap}` — including (a) the alias counter's denominator
`parsed_runs = 18` and the `8 = 8 check arms` decomposition, (b) the three distinct
"supplemental" notions named apart (`source_review_supplemental_cases = 3` ⊂
`c2_sealed_cases = 30`; `supplementary_output_checks = 274` ∉ any case denominator;
before-arm 0/0), (c) `c2_primary_cases = 27` beside `c2_sealed_cases = 30`,
(d) `c1_supplementary_guard_checks = 5` decomposed as `4 guards + C35` stored under
`c1_real_control.identity_pins`, (e) `source_rows 76→86` labelled distinctly from
`allowlisted 86`, (f) the `C30 ← case-set` attribution so `real_controls_pass=false`
cannot be read as a host-observation mismatch, (g) `49/49 selftest` labelled
"co-evolved public selftest — not the frozen CaseEscapedSpace", (h) the W1/W2
dispatch-digest caveats.

**Why this shape (second-order):** precedent exists in this very wave —
`evidence/source-accounting.json` is exactly such a connector-produced, digest-bearing
count artifact, and it was committed in the post-measurement pin commit
(`6eb889c0`), i.e. **outside the sealed driver**. Writing the legend as an evidence
file therefore (i) touches **no** frozen case/rule/oracle/contract/driver byte, so
`C08/C09/C10/C12/C13` (byte identity seal→pin, driver_matches_sealed_bytes) stay
green; (ii) does not require re-sealing the driver, which a driver edit *would*
(`driver_sha256` changes → `C13` breaks unless the driver is re-sealed after the
implementation, i.e. after the freeze — the one thing this round must not do);
(iii) keeps every count, the strict 29/30, the 25/26→26/26, the 274/274 and the
`unmet` case exactly as they are, so it cannot be read as an admission, a clearance,
a promotion or an expectation repair.

**Affected axes:** A1 (denominator integrity), A2 (name separation), A3 (provenance),
A5 (attribution). **Harmed axes:** none — A4 is preserved by construction (no frozen
byte touched, no special-case, no relabel of the red case, no driver/production edit).

**Risks.**
- R1 A report that quotes "8" without `parsed_runs = 18` invites the "8 of 26
  requirements" misreading → the legend must attach the denominator to the value, not
  in prose.
- R2 If the legend is ever read as a *capability* or *admission* statement, it
  overstates: `probe visibility/accounting consistency is never
  clearance/health/admission` (round context) and `privacy_clearance=false` stays.
- R3 The legend must not re-derive or restate the red case's expectation; it may
  only record that the case is `unmet` and that the contradiction is preserved
  (frozen bytes unchanged) — otherwise it would be a disguised expectation repair.
- R4 It must be generated from **committed** bytes (`wave2-run.json` @6eb889c0,
  `corpus/SOURCES.md` @f3dc07c0, `frozen/case-decisions.json` @seal) and carry its
  own source digests, or it inherits the same non-re-derivable-digest weakness
  documented in §6.
- R5 Deferred, deliberately: adding `denominators.c2_primary_cases` /
  `c2_source_review_supplemental_cases` **inside** the driver summary is the cleaner
  fix, but it changes driver bytes and would require a re-seal → **not recommended
  in this wave**; record as a r24 candidate.

**Verification (what I ran, and what I did not).** I ran no driver, no oracle, no
selftest, no quota/mount/qgroup command, no live host read; every number above is
either (a) read from committed evidence bytes with digests listed at the top, or
(b) computed by read-only `git show`/`git ls-tree`/`git merge-base`/`sha256sum`/
`wc -c` over committed blobs, or (c) explicitly marked `[INFERENCE]` (the
requirement→arm mapping, derived from `oracle-rename.py` source and cross-checked
against the observed 18-run variant list). The independent row count 76 → 86 was
recomputed by me from the committed `corpus/SOURCES.md` at both revisions and matches
`evidence/source-accounting.json`. The 274 decomposition 28×9 + 1×10 + 1×12 was
recomputed from `c2-after-observed.json`. The alias-denominator decomposition
8 check + 10 setup was taken from the driver's own `C23.shapes` and cross-checked
against the oracle's 18-run variant list and the observed `misleading_alias_runs`
values 8/0.

---

## 9. Addendum — two further provenance facts observed in the live lane (sibling-produced, untracked)

Both were produced by other W2 seats while this audit ran; neither is in the pinned
revision (`f3dc07c0…`), and neither changes a count. They are recorded here because
they change what a future "source count" or "case provenance" sentence may assert.

**9.1 The source-id namespace is now drifting past the registry.** The registry at the
pin holds **86 rows** (S001–S086; §5). The live working tree additionally carries
untracked `.ufo/waves/round-23/evidence/post-falsification-sources.json` declaring
**three more** source rows staged as "post-falsification source correction, no
sealed target change": `S087` `fs/ext4/super.c`
(sha `4cae2369…`, 216306 B), `S088` `include/linux/quotaops.h`
(sha `2a316c77…`, 10287 B), `S089` `fs/quota/dquot.c`
(sha `951a0c8d…`, 84353 B), each with a stored raw copy under
`evidence/sources/`. So "source count" now has **two live values**: 86 = registry rows
at the pin (the number `evidence/source-accounting.json` reports), and 89 = rows
*opened* including post-falsification corrections (not in `corpus/SOURCES.md`, not in
the seal). Any ledger line that says "source 76→86" must say **"registry rows at
`f3dc07c0`"**; a later reader who counts opened source ids (89) and compares it with
the registry (86) will otherwise read a 3-row discrepancy that is a *stage* difference,
not a lost row.

**9.2 One of the 27 primary cases has a broken chain from author original to sealed
bytes.** `frozen/case-decisions.json` (sealed) records for `CaseTmpfsNoQuota`:
`original cases-proposed/CaseTmpfsNoQuota.json` (`f4814c94…`),
`selected cases-corrected/CaseTmpfsNoQuota.json` (`7afd98c1…`), `primary true`,
reason "Independent source-derived pre-measurement correction; exact author bytes, no
L1 expectation edits". Independently checked with read-only git:

- `git ls-tree 22772c10… .ufo/waves/round-23/cases-corrected/` — the tree contains
  **26 distinct corrected case ids + `CaseSymlinkRealpath-final.json`** and **no
  `CaseTmpfsNoQuota.json`**; the working tree `cases-corrected/` likewise lacks it.
- `frozen/quota-cases/CaseTmpfsNoQuota.json` **does** exist at the seal with
  sha256 `7afd98c1…` — identical to the decision's `selected_sha256`.
- The sibling erratum `.ufo/waves/round-23/evidence/tmpfs-source-provenance-erratum.json`
  (untracked) states: `selected_source_path_at_seal: false`,
  `fixture_unchanged: false`, `expected_unchanged: true`,
  `different_top_fields: ["scenario","fixture","rationale"]`, and the status
  "L1 selected an author-corrected draft during source copying, then incorrectly told
  author original selected; author deleted draft. Frozen expected bytes themselves
  landed before production and remain unchanged. Preserve original/selected bytes and
  disclose missing intermediary; do not rewrite frozen case-decisions."

Consequence for the axes: the sealed **frozen bytes are intact and byte-identical to
the recorded `selected_sha256`**, the case's expected bytes are unchanged, and the
case **passes** (the only unmet case in the 30 is `CaseEscapedSpace`). What is not
resolvable is the *author* chain: the decision names a `selected` path that does not
exist in the tree, and the author draft it was copied from was deleted, so the
decision's "exact author bytes" claim is **unverifiable for this one case** (and the
word "original" in the erratum's status sentence refers to the proposal, not the
selected draft). This is exactly the "incomplete provenance" class this audit is
asked to flag — and it is already disclosed by its author, so the correct action is
**disclosure only**: no rewrite of `frozen/case-decisions.json`, no change to the
30-case denominator, no change to 29/30, no change to any expectation. It does mean
the case-population provenance sentence must be written as: *30 sealed cases; 29 have a
resolvable original→selected path in the tree; 1 (`CaseTmpfsNoQuota`) has intact
frozen bytes matching the recorded `selected_sha256` but an intermediary author draft
that was deleted, disclosed in `evidence/tmpfs-source-provenance-erratum.json`.*

---

## 10. Correction (L1 ruling, `MadoR22-2`) — the payload-binding "gap" was a category error

**Ruling received:** `mori-dispatch-ledger.py` hashes **only** the canonical validator
payload, not the whole dispatch envelope file; therefore the outer-file digest is
*expected* to differ from the bound payload digest, and the difference is not a
provenance gap.

**Independently re-derived (metadata only — no gate, driver, oracle, selftest or
probe was rerun):** the ledger's `_payload_identity`
(`tools/mori-dispatch-ledger.py:120–164`) locates the unique `run`/`taskCall` object,
then hashes `json.dumps({"context":…, "tasks":…}, ensure_ascii=False, sort_keys=True,
separators=(",",":")).encode("utf-8")`.

| wave | canonical payload bytes | canonical payload sha256 | ledger-recorded | match |
|---|---|---|---|---|
| W2 (`wave2-run.json`, `taskCall`) | **159710** | **`d28cc9f2dbf120831d85277e0fa47f0c10b658c4bafc0a36b4099ac069103efd`** | 159710 / `d28cc9f2…` | **yes** |
| W1 (`wave1-run.json`, `taskCall`) | **88738** | **`cd8a5fa64e69ce55c0dec70d02d8bf77a3d1fbd27bd3fcf61660a63d3d3cc628`** | 88738 / `cd8a5fa6…` | **yes** |

Both waves' bound payload digests re-derive **exactly** from the committed dispatch
bytes. The outer envelope files carry extra, non-payload fields (`schema`, `wave`,
`policy`, `counts`, `registry`, `compaction`, `note`, `resumeSends`), which is why
their whole-file digests differ (`63205203…`/177691 for W2, `ec12c513…`/101251 for
W1).

**Accordingly §6 "provenance gap 1" is withdrawn.** The correct statement is: the
binding covers the canonical `{context, tasks}` payload only; it is **not** a
whole-file digest and must never be compared against one. The W1 ledger's own
"retrospective binding" note remains accurate and L1-declared, and the `PAYLOAD_BOUND`
receipt in `evidence/wave2-payload-binding.json` (exit 0, rev `6eb889c0…`) is
re-derivable from committed bytes.

**§6 "provenance gap 2" is withdrawn as a gap and restated as a deliberate
separation.** The measured code pin (`f3dc07c0…`) and the later receipt commit
(`6eb889c0…`, which carries `evidence/measure4/`, `evidence/quota-selftest-corrected.json`,
`wave2-run.json`, `wave2-record.json`) are distinct **by design**: the pin freezes the
code + expectations under measurement, the descendant commit pins the receipts
produced against that pin. Verified linear order: seal `22772c10…` ⊏ pin `f3dc07c0…`
⊏ `6eb889c0…` (`git merge-base --is-ancestor` rc 0 both ways of the first pair). No
claim is made that the receipts live inside the measured revision.

**Seat ids ARE carried — by the wave's own registry files (untracked until the wave
settles), not by the count artifacts.** `.ufo/waves/round-23/wave2-assignments.json`
(sha256 `fd9717fadbe1b7d6c35e0910f1ead41492c8d191784a864c3617f4254a501459`, 96
entries, `seat → agentId`, e.g. `C1R01 → MadoR22-2.C1R01`) and
`.ufo/waves/round-23/wave2-record.json` (sha256
`19ac799bbfddb06ea5ae256380e855762c431c7478670e003c4ac4e849d380ee`, schema
`ufo-swarm-registry-v1`, wave `mori-r23-falsify`, reportDir
`.ufo/waves/round-23/falsify`, 96 members with `kind`/`agentId`/`role`). Both are
currently **untracked** (they land when the wave settles), so the accurate statement
is: *seat-level lineage exists in committed-and-untracked wave registry files; the
committed count artifacts (`summary.json`, oracles) carry counts only, and that is by
design, not a missing field.* The lineage mapping itself is unchanged and still
holds: `C1R01`…`C1R26` ↔ `R01`…`R26`; 30 `Q*` seats ↔ the 30 sealed cases (27 primary
+ `QHiddenMount`/`QQgroupDisabled`/`QQgroupUnknown`); `ReopenS077`…`ReopenS086` ↔ the
10 new registry rows.

**Retained unchanged (not affected by this ruling):** every denominator observation in
§2, §3, §5 and §7 (26 / 18 / 8 / 5 / 27 / 3 / 30 / 274 / 31 / 76→86 / 95-86-5 / 49);
the frozen-contradiction provenance in §4; the `C30 ← case-set` attribution in §5;
the W1 attempt/refusal history and the W1 "retrospective binding" declaration; the
**real Tmpfs source gap** in §9.2 (`CaseTmpfsNoQuota`: sealed frozen bytes
`7afd98c1…` intact and equal to the recorded `selected_sha256`, expected bytes
unchanged, case passes, but the decision's `selected` path
`cases-corrected/CaseTmpfsNoQuota.json` does not exist at the seal or in the working
tree and the intermediary author draft was deleted — disclosed in
`evidence/tmpfs-source-provenance-erratum.json`; disclosure only, no rewrite of
`frozen/case-decisions.json`); and the source-id namespace drift in §9.1 (registry
86 rows at the pin vs S087–S089 opened post-falsification, untracked).

**Effect on the proposed move (§8):** the legend must record the bound-payload
identity as `{canonical payload sha256, canonical payload bytes, canonicalisation
rule}` — explicitly **not** a whole-file digest — and must cite
`wave2-assignments.json` / `wave2-record.json` for seat lineage with their untracked
status stated, instead of implying seat ids are absent from the wave. The A1/A2/A3
observations and the no-harm analysis of the move are unchanged.

**No-harm ledger for this seat:** 0 production edits, 0 frozen-case edits, 0 oracle
edits, 0 contract/amendment edits, 0 registry edits, 0 lane-index/refs edits, 0
executions of any harness; the only write is this report at
`.ufo/waves/round-23/falsify/ConnectCountsFinal.md`.

**No tools were installed or updated by this seat** (read-only audit; no channel
needed).

Report: .ufo/waves/round-23/falsify/ConnectCountsFinal.md
