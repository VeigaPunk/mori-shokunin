# ReviewRejectedCases — round 23 wave 2 (falsification seat)

Seat: `MadoR22-2.ReviewRejectedCases` (reviewer, wave 2, read-only).
Scope as dispatched: retained proposals and the rejected inconsistent symlink correction;
every exclusion's pre-measurement reason and exact selected author bytes; all 30 named final
cases; duplicate ids across history not double-counted.

Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`. Production pin `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c`,
seal `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687`.

**What this seat did:** read-only inspection of committed bytes (contract, pre-seal amendment, seal
manifest, case decisions, all 57 case files on disk, the sealed oracle and driver, and the
committed measure4 receipts), plus an independent re-derivation of the sealed mount-resolution
rules over all 30 sealed fixtures. No tool, oracle, selftest or driver was executed; no fixture
was run; no live host read; no git mutation; no sibling write; no transcript read; no subagent.
No scratch directory was needed (all analysis ran over repo bytes in memory), so
`/fast/scratch/hyaku/mori-r23/ReviewRejectedCases/` was not created. **No package install or
update was performed** (no tool was needed for this seat).

---

## 1. Verdict

| axis | verdict |
|---|---|
| Rejected symlink correction: real defect, real pre-measurement reason, bytes preserved | **PASS** |
| Every other exclusion carries a pre-measurement reason | **PASS** |
| All 30 named final cases present, one row per id, byte-exact against the seal | **PASS** |
| Duplicate ids across history not double-counted | **PASS** |
| `case-decisions.json` `selected` path for `CaseTmpfsNoQuota` resolves to a file | **FAIL (S1, medium)** — dangling path; sealed bytes unaffected |
| Single strict red is unique, non-inflated, and not double-reported | **PASS** (independent re-derivation) |

No case, rule, oracle or expectation byte was changed, and none is proposed for change. The strict
red at 29/30 remains exactly one case (`CaseEscapedSpace`); this report adds no second failure.

---

## 2. Findings by severity

### S1 — Medium — `frozen/case-decisions.json` names a `selected` file that never existed for `CaseTmpfsNoQuota`

* Evidence:
  * `.ufo/waves/round-23/frozen/case-decisions.json` decision `CaseTmpfsNoQuota`:
    `selected = "cases-corrected/CaseTmpfsNoQuota.json"`, `selected_sha256 = 7afd98c191a799e52bb9ac01b896b23eaa855b9e02ef1bc3f901aa13a03a49b5`.
  * The path is absent from the working tree and from the seal commit:
    `git ls-tree -r --name-only 22772c10… -- .ufo/waves/round-23/cases-corrected` lists 27 files and
    `CaseTmpfsNoQuota.json` is not among them; `git log --all -- .ufo/waves/round-23/cases-corrected/CaseTmpfsNoQuota.json`
    returns nothing. `cases-corrected/` contains 27 files, of which one
    (`CaseSymlinkRealpath.json`) is the rejected intermediate — i.e. 26 selected intermediates + 1 rejected.
  * The declared bytes do exist and are exact, but only as the sealed copy:
    `.ufo/waves/round-23/frozen/quota-cases/CaseTmpfsNoQuota.json` = `7afd98c1…`, byte-identical to
    the declared `selected_sha256` and to the seal manifest entry (43/43 seal-pinned files verify by
    sha256 **and** byte length; 0 problems; every one of the 43 also re-verified against the seal
    commit blob with `git show 22772c10…:<path>`, 0 problems).
  * The author seat's own report `.ufo/waves/round-23/build/CaseTmpfsNoQuota.md` declares its single
    deliverable to be the **original** proposal `cases-proposed/CaseTmpfsNoQuota.json`
    (sha `f4814c94a8a0f330df82caa46ef1695318e5b3b297545e3b2b888519c4dd4dbb`, 5386 bytes) — that file is
    retained and its hash matches the decision's `original_sha256`, but it is *not* the selected file.
    The selected file's own `rationale` states it is a pre-seal amendment re-derivation
    ("the original proposal left untouched in `cases-proposed/`", delta = the required
    `btrfs_sysfs` record with `qgroups_enabled`, two extra decoy mount lines, and the narrowed
    "four documented `*_hardlimit` keys" wording); its `expected` object is byte-identical to the
    original's, so the correction is source-derived, not result-driven.
  * `excluded_evidence` in the same file records only two entries (the symlink intermediate; the
    general "original proposals retained, none silently deleted"). It does **not** record that the
    `CaseTmpfsNoQuota` corrected intermediate was never committed.
* Impact: **measurement-neutral**. The oracle and the driver read only the sealed directory
  (`oracle-quota.py:395` `case_files = sorted(p for p in cases_dir.glob("*.json"))`;
  `measure-round23-v2.py:982` `staged_cases.glob('*.json')`), and `measure4` staged exactly the 30
  sealed files. So the dangling path cannot add, remove or duplicate a scored case. What is
  defective is the **provenance/exclusion record**: it asserts an "exact selected author bytes"
  provenance for one of the 30 cases through a path that does not exist, and the absence of that
  author-lane intermediate is unexplained in the exclusion list.
* Recommendation (advisory only, parent-side; no frozen byte may be rewritten in this round):
  record the gap in the exclusion ledger of a later round — e.g. "the corrected `CaseTmpfsNoQuota`
  intermediate was never committed; the sealed bytes exist only under `frozen/quota-cases/`" — and
  name the seat that authored the sealed copy. Do **not** rewrite `frozen/case-decisions.json` in
  place: its bytes are seal-pinned (`b05a0072…`, verified identical at the seal commit) and the
  amendment freezes it as history.

### S2 — Low (already attested elsewhere; reported here as confirmation, not as a new failure) — `C30.c2_oracle_real_control_agrees` is an aggregate check, not a real-control failure

* Evidence: `measure-round23-v2.py:1108-1112` predicates C30 on
  `oracle_real_counts.get('unmet') == 0`, i.e. the oracle's **combined** case+real-control counter.
  In `evidence/measure4/c2-after-real-observed.json` the counts are `{pass 30, total 31, unmet 1}`
  while the oracle's own real-control entry is `status: "pass"` with
  `headline = {exit_match: true, finding_match: true, paths_match: true}` and 10/10 supplementary
  checks passing; `C29.c2_real_control_matches_frozen` passes.
* Consequence: `summary.real_controls_pass = false` and `summary.all_claim_checks_pass_excluding_real_controls = false`
  are **not** evidence that the frozen C2 real control disagreed. C34 and C30 have one cause
  (`CaseEscapedSpace`) and must not be reported as two independent failures.
* Status: this exact attribution is already recorded by sibling seats
  (`falsify/ReviewRealControls.md` S1, `falsify/ReopenS081.md`, `falsify/RerunPinnedDriver.md`).
  I state it only so it is not counted twice; it adds no new failure and does not touch the 29/30
  denominator.

### S3 — Informational — the oracle's single headline counter mixes the primary 27 with the 3 source-review supplements

* Evidence: `oracle-quota.py:529-539` counts every row of `results` as a headline row, so
  `counts.total = 30` = 27 primary + 3 supplement cases; the primary/supplemental split is not in
  the oracle output itself but in `evidence/frozen-contradiction.json`
  (`primary_pass 26, primary_total 27, supplemental_pass 3, supplemental_total 3`) and in
  `frozen/case-decisions.json` (`primary` flags).
* Assessment: this is **not** double counting — each of the 30 ids appears once, and the 3
  supplements are semantically distinct from the 27 primaries (they cover the initialized-but-disabled
  btrfs qgroup, the initialized-but-unreadable `enabled` attribute, and the hidden-ancestor
  overmount; none of the 27 primaries exercises those). The split is disclosed rather than hidden.
  A reader who sees only `{"pass": 29, "total": 30}` should be pointed at
  `frozen-contradiction.json` for the 26/27 + 3/3 breakdown. No change proposed.

---

## 3. Verification performed (all by byte inspection, no execution)

### 3.1 The rejected inconsistent symlink correction — real defect, real reason, bytes preserved

* `cases-corrected/CaseSymlinkRealpath.json` (sha `ef8eeaa03fa2576d8c9e666acfa4b3c38f765d4cde0b6ff1cacda26a78e7eefb`)
  is genuinely self-inconsistent: its `fixture.paths[1].path` is `/tmp/mori-quota-target-dir` while its
  `expected.paths[1].path` is `/tmp/mori-quota-target` — the ordered per-path comparison fails on the
  path member itself. The defect is acknowledged by the author inside the selected file's `rationale`
  ("The intermediate artifact renamed the second fixture path … which would have made the ordered
  per-path comparison fail on the path member; that contradiction is my own defect").
* The selected replacement `cases-corrected/CaseSymlinkRealpath-final.json`
  (sha `275c360585a93e2f1bc7e2ded0f4cd42b07d5b0eeb16b9790d1980f456b0d07e`) is self-consistent: every
  `expected.paths[i].path` equals the matching `fixture.paths[i].path` in order, and its only delta
  from the original proposal is the mandated `qgroups_enabled` member.
* The frozen copy `frozen/quota-cases/CaseSymlinkRealpath.json` carries the `-final` bytes
  (`275c3605…`) — the rejected intermediate is **not** in the frozen set and therefore cannot enter
  the scored denominator. Byte-preservation of the rejected artefact: `git show 22772c10…:.ufo/waves/round-23/cases-corrected/CaseSymlinkRealpath.json`
  = `ef8eeaa0…`, identical to the working tree.
* Pre-measurement: the rejection is recorded in the seal-pinned `frozen/case-decisions.json`
  (`excluded_evidence[0]`), committed at the seal `22772c10…`, whose parent-ancestor relation puts
  the implementation commit `1979a9de…` strictly after it (`git rev-parse 1979a9d^` = the seal).

### 3.2 Every exclusion has a pre-measurement reason and exact selected bytes

* `excluded_evidence` has exactly two entries: (a) the symlink intermediate, (b) "original
  `cases-proposed` shapes retained but superseded by source-derived amended cases; none silently
  deleted". Both are source-review statements fixed at the seal commit; neither is result-driven.
* For all 30 decisions: `selected_sha256` equals the sha256 of the sealed file carrying the same id
  (30/30). For all 27 primary decisions with an `original`: the `original` path exists and its
  `original_sha256` matches the file on disk (27/27, zero mismatches) — the original proposals are
  retained, not silently deleted (`git ls-tree 22772c10… -- cases-proposed` = 27 files).
* The three supplements carry `primary: false` and the reason "Source-review discovery guard before
  candidate inspection/result"; their `selected_sha256` values match their sealed files (3/3).
* Only exception: S1 above.

### 3.3 All 30 named final cases

* `frozen/case-decisions.json`: 30 decisions, 30 **distinct** ids, 27 `primary: true` + 3
  `primary: false`; the declared counts `selected_cases 30 / independent_primary 27 /
  source_review_supplemental 3` match the files.
* `frozen/quota-cases/`: exactly 30 `*.json` files, one per id, every file's internal `id` equals its
  basename, and the 30 internal ids are unique (no id twice).
* Seal manifest: 43 pinned files, all verified by sha256 **and** byte length against the working
  tree (0 problems), and all 43 re-verified against the seal commit blob (0 problems) — the frozen
  case set, the decisions file and the seal manifest are byte-unchanged since sealing.
* `frozen/seal-manifest.json` also pins `primary_c2 27`, `source_review_supplemental_c2 3`,
  `c1_original_requirements 26`, `supplementary_never_redefines_primary_denominator: true`, and
  `production_at_seal.quota_absent: true` (confirmed: `git ls-tree 22772c10… tools/` contains no
  `mori-quota-surface.py`).
* Wave-2 payload coverage: all 30 sealed case ids are named in `wave2-spec.json`, **exactly one
  falsification seat per case** (`QBoundary` … `QQgroupUnknown`), no case named by two seats, no seat
  naming a non-existent case, and the C1 side has 26 requirement seats for the original 26
  requirements. (96 wave-2 items total.)

### 3.4 Duplicate ids across history are not double-counted

* 87 case files exist on disk across three author-lane directories plus the frozen set: 27 proposals,
  27 `cases-corrected` (26 selected intermediates + the 1 rejected symlink intermediate), 3
  supplements, 30 frozen (of which `frozen/quota-cases/CaseSymlinkRealpath.json` is the `-final`
  bytes). Per-id file multiplicity is therefore 3 for the 25 primary ids that have all three copies, 4 for
  `CaseSymlinkRealpath` (proposed + corrected + rejected corrected + frozen) and 2 for
  `CaseTmpfsNoQuota` and the three supplements.
* Nothing merges those directories into a scored population: the oracle globs only the cases dir it
  is given (the sealed `frozen/quota-cases`), the driver stages only that dir
  (`measure-round23-v2.py:982`) and reads `cases-proposed` solely for the C06 presence check
  (`:312`), never into the denominator.
* Measured result (`evidence/measure4/c2-after-observed.json`): 30 result rows, 30 unique case
  names, and **every** row's `case_sha256` equals the seal-manifest digest of that file (0
  mismatches); `counts = {pass 29, total 30, unmet 1}`; supplementary checks 274/274 pass.
  Before-arm: 30 rows, all `capability_absent`.
* Source-id hygiene: the 30 sealed cases cite only S077–S084, all of which exist as registry rows
  in `corpus/SOURCES.md` (S085/S086 are additional rows cited by no case); no duplicate or orphan
  source id.

### 3.5 Independent re-derivation: the strict red is exactly one case, and no other expectation is inconsistent

I re-implemented the sealed mount rules (per-line "last three fields after the `-` separator",
octal decode of exactly `\040 \011 \012 \134` on root/mountpoint/source, longest component-prefix
selection, duplicate-covering-mountpoint refusal, and the parent-ID refusal) over all 30 sealed
fixtures and compared the outcome with each case's own frozen `expected` row. Result: only three
fixtures trip a refusal, and two of the three expect it.

| case | chosen mount (id / parent) | refusal triggered | frozen expectation | verdict |
|---|---|---|---|---|
| `CaseStacked` | `/data` id 31, duplicate covering mount point | duplicate | `ambiguous_overmount` | consistent |
| `SupplementHiddenMount` | `/home/x/y` id 70, parent 65 | parent-ID (65 ≠ 80, the longest strictly-shorter cover `/home/x`) | `ambiguous_overmount` | consistent |
| `CaseEscapedSpace` | `/srv/my data` id 43, parent 33 | parent-ID (33 present in the snapshot and 33 ≠ 42, the longest strictly-shorter cover `/srv`) | `xfs_quota_option`, exit 1 `QUOTA_ENABLED` | **contradictory** |

This reproduces, from the sealed fixture bytes alone, the exact identity already recorded in
`evidence/frozen-contradiction.json` (selected id 43, parent 33, shorter cover 42, parent present),
and proves the red is **unique**: no other of the 30 sealed expectations conflicts with the sealed
rule set. The sibling row `/srv/plain` in that case is unaffected (its chosen mount `/srv` id 42 has
parent 33 = the id of the longest strictly-shorter cover `/`, so no refusal), which is why the
measured run yields `unknown` for row 1 and `disabled` for row 2 — matching
`evidence/frozen-contradiction.json.actual` exactly.

Per Main's standing instruction and `evidence/parent-strict-target-disposition.txt`: the case bytes,
the rule text and the oracle bytes stay unchanged; no special-casing, exclusion, relabelling or
rewrite is proposed or performed. The full-driver exit 1 is the expected consequence of this one
red. **This report adds no second failure and does not change the 29/30 denominator.**

---

## 4. Residual risk

1. **S1 (medium)** — the exclusion/provenance ledger for `CaseTmpfsNoQuota` points at a
   non-existent author-lane file. Anyone re-deriving "exact selected author bytes" from
   `case-decisions.json` alone will fail to find that path; the bytes are recoverable only from
   `frozen/quota-cases/`. The sealed measurement is unaffected, but the "author-lane independent of
   implementation" claim for that one case is not reconstructible from retained lane artefacts
   (the author seat's report names the original proposal as its only deliverable).
2. **Oracle-author credit for the sealed `CaseTmpfsNoQuota` copy is unrecorded** — the file's own
   rationale is written in the first person ("this corrected case re-derives the same scenario"),
   but no retained artefact names the seat. Authority for that copy is therefore unattributed in the
   lane.
3. **The oracle's headline counter (30) does not itself carry the primary/supplemental split**; a
   consumer reading only `c2-oracle-after.json` sees 29/30 without the 26/27 + 3/3 breakdown. The
   split exists in `frozen/case-decisions.json` and `evidence/frozen-contradiction.json` only.
4. **C30 remains an unsatisfiable aggregate while the frozen case stays red** (S2) — any future
   summary that reports `real_controls_pass` without the attribution note will misattribute it.
5. The 27 retained `cases-proposed/` files are the pre-amendment fixture shape: they are structurally
   invalid against the amended loader (`qgroups_enabled` missing) and must never be scored as
   inputs (two author reports already flagged this). They are retained as evidence, which is correct.

## 5. Verification gaps (not closable in this seat)

* I did **not** execute the tool, the oracle, the selftest or the driver, and did not re-run the
  measurement; every "pass"/"unmet" quoted here is read from the committed `measure4` receipts and
  cross-checked against the sealed bytes (per-row `case_sha256` vs seal manifest, 30/30 match).
* The re-derivation in §3.5 is an independent reading of the sealed rule text against the sealed
  fixtures; it is not a second execution of the oracle, and it does not adjudicate whether the
  implementation's behaviour is right in general — only whether each frozen expectation is
  consistent with the sealed rule set.
* The provenance question raised in S1 (which seat authored the sealed `CaseTmpfsNoQuota` copy, and
  why the intermediate was never committed) cannot be settled from committed lane bytes; it needs
  the L1's own record. I did not read any transcript or session state to attempt it.
* No claim here touches C1 (calibration), the open debt (4 unallowlisted hits, original permission
  RED 11/12, two unknown dispositions, baseline acceptance blocked, `privacy_clearance=false`), or
  any admission/promotion question. No clearance, health or admission claim is made or implied.

## 6. Files read (no writes other than this report and the receipt noted below)

`.ufo/waves/round-23/contract.md`, `preseal-amendment.md`, `frozen/seal-manifest.json`,
`frozen/case-decisions.json`, `frozen/quota-cases/*.json` (30), `cases-proposed/*.json` (27),
`cases-corrected/*.json` (27), `cases-supplemental/*.json` (3), `oracle-quota.py`,
`build/MeasureDriver/measure-round23-v2.py`, `build/CaseTmpfsNoQuota.md`,
`build/CaseSymlinkRealpath.md`, `evidence/measure4/{summary,c2-oracle-after,c2-oracle-before,
c2-after-observed,c2-after-real-observed}.json`, `evidence/frozen-contradiction.json`,
`evidence/parent-strict-target-disposition.txt`, `wave2-spec.json`, `wave1-assignments.json`,
`wave1-attempts.json`, `wave1-ledger.json`, `corpus/SOURCES.md`; plus read-only git
`log/ls-tree/show/status/rev-parse` at the seal and head revisions.

Synthetic receipt written by this seat:
`.ufo/waves/round-23/falsify/ReviewRejectedCases/case-ledger-check.json`
(sha256 `3faad5c1be8cd5736820fe487575dcf82f9bf08ee0065d46df13f7466c28b723`, 50867 bytes) — sha256 of
every case file across the four directories, the 30 decision rows with their declared vs observed
hashes, the duplicate-id census, and the independent refusal re-derivation results.
