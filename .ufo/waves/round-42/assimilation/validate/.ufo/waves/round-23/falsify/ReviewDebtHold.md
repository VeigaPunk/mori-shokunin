# ReviewDebtHold — open-debt hold verification (mori round 23, wave 2 falsification)

Seat: `MadoR22-2.ReviewDebtHold` (read-only reviewer). Item: independently verify that the
four unallowlisted inherited retention identities, the two unknown loss-accounting
dispositions, the old red original permission control and the blocked baseline acceptance
remain **unaltered**; reclassify nothing, clear nothing.

Verdict: **all four debts are intact.** No reclassification, clearance, promotion or
acceptance was found anywhere in the round-23 delta. Two traceability findings (F1, F2)
record where the lane's *own* evidence for "still debt" is asserted or bound to a stale
revision; both are closed by the independent recomputation below, not by the lane's
receipt chain. No lane code, oracle, expectation or frozen file was modified.

---

## 1. Method and bounds

Read-only throughout. No test, gate, linter, selftest, quota probe, driver or fixture was
executed (this item authorizes no invocation; `mori-evidence-loss.py audit` was therefore
**not** run and the RED 11/12 control was **not** rerun — its preservation is shown from
byte identity plus the tool's own decision logic, §3.3). No live host read of any kind
(no `/proc/self/mountinfo`, no qgroup/mode, no quotactl/btrfs/xfs_quota/repquota/mount).
No credential/auth file, `agent.db`, `Documents`, shell history, journal or session
transcript was opened. No sibling report, lane index, `jj` ref or production/frozen/oracle
file was written. Tools installed: **none** (no install was needed; `git`, `python3` were
already present, so the operator tooling directive records no channel action).

Git usage was read-only and absolute: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin
show|log|status|rev-parse|ls-tree|cat-file|diff|merge-base`.

Revisions used:

| label | revision | role |
|---|---|---|
| ENTERING | `1bfe708a170c877db3319060d0ab38771efe03ac` | r23 entering (r22 admitted) |
| SEAL | `22772c10f6e3c1d8d3fe1b72083a6194e9f4e687` | expectation seal |
| PROD | `f3dc07c0bf423cc1947d0ffa91afa9ce236fbe3c` | production pin under review |
| HEAD | `6eb889c037163e4886eaa61501258910d6a529b9` | current lane HEAD (post-pin evidence) |
| R21 | `9fb1f911cfdd6061005c300795f44b1b45523897` | r21 measured revision (r21 receipt ground) |
| MID | `56ac3badb4d84ed5b0b117d6295fc832341e01f3` | r23 mid revision that produced the retention-floor receipt |

## 2. Independent recomputation used as the primary instrument

The lane's own "debt carried" statements are prose plus a driver literal. To avoid
restating them, the frozen policy was re-applied from scratch to the committed trees,
using only read-only git plumbing:

* policy: `.ufo/waves/round-18/frozen/c1-policy.json` (blob `8bf285bddce57f7fdefbbf514cb0b3bf97652742`,
  identical at ENTERING and PROD) — classes R1–R9, `must_redact_paths`, `non_author_paths_glob`;
* allowlist: `corpus/evidence/retention-allowlist.json` (blob `f8be55b1204bbb0b54b5f089407a4a10c8145b15`,
  identical at ENTERING and PROD) — 86 rows, 0 forbidden rows;
* population: every tracked blob of the revision via `git ls-tree -r -z --full-tree` +
  `git cat-file --batch`, NUL-containing blobs skipped, UTF-8 with `errors=replace`,
  per-line SHA-256 (mirrors `tools/mori-retention-gate.py:_blob_hits`);
* membership: allowlist key = `(path, class, line_sha256)`; must-redact paths may carry no row.

Results (metric = unallowlisted in-scope hits, `tools/mori-retention-gate.py:_scan_result`):

| revision | raw_total | allowlisted hits | non_author | **metric (unallowlisted)** | routed (in must-redact) | forbidden rows | stale rows |
|---|---|---|---|---|---|---|---|
| R21 `9fb1f91` | 95 | 86 | 5 | **4** | 0 | 0 | 0 |
| MID `56ac3ba` | 95 | 86 | 5 | **4** | 0 | 0 | 0 |
| PROD `f3dc07c` | 95 | 86 | 5 | **4** | 0 | 0 | 0 |
| HEAD `6eb889c` | 95 | 86 | 5 | **4** | 0 | 0 | 0 |

The four unallowlisted identities are byte-identical at all four revisions, and identical
to the retained r21 receipt's `unallowlisted_hits` (multiset of
`(path, class, line, line_sha256)`):

```
.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json  R2  line 8   8d92bfa35a80…
.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json  R5  line 11  7f23448e6e23…
.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json  R6  line 12  0cdc89722df0…
.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json  R8  line 14  1d2b6e6ed2ba…
```

(Paths/classes/line numbers/digests are lane-internal synthetic metadata already published
in the committed r21 receipt; no matched private value is printed.)

Delta check ENTERING→PROD: 377 blobs added, 0 removed, 6 changed. Re-applying the frozen
policy regexes to every added/changed blob yields **0** policy-class hits, and no added
blob is inside `must_redact_paths` — so the r23 round could not have introduced a fifth
hit, and did not remove one. Same for PROD→HEAD (58 added, 0 removed, 1 changed → 0 hits).
Untracked wave artifacts (`.ufo/waves/round-23/**`, including `wave2-run.json`,
`wave2-spec.json`, `wave2-response1.json`, `falsify/**`) were also scanned: 0 policy-class
hits.

## 3. Debt-by-debt verification

### 3.1 Four unallowlisted retention hits — UNALTERED (metric 4, same identities)

* Independent recomputation: §2 — metric 4 at R21/MID/PROD/HEAD, identical identities.
* Lane receipts agree: `.ufo/waves/round-23/evidence/retention-floor-delivered.json`
  (`measured_revision 56ac3ba…`, exit 1, `metric 4`, `non_author 5`, 86 allowlisted hits)
  and `evidence/retention-floor-comparison.json`
  (`metric 4, raw 95, allowlisted 86, non_author 5, new_unallowlisted 0,
  missing_unallowlisted 0, same_inherited_identities true, privacy_clearance false`).
* Cross-check against the retained r21 receipt: the r21 `unallowlisted_hits` multiset and
  the r23 delivered multiset are **equal** (no r21-only, no r23-only entry).
* Allowlist and policy bytes are unchanged (blobs above) and the allowlist carries no row
  for the four-hit path, so the hits were not reclassified as allowlisted; 0 forbidden
  rows, so no must-redact path was granted a row; 0 stale rows, so no allowlist row was
  left dangling.
* C1 identity pins still hold and were re-derived independently: recomputing
  `SHA256(json.dumps(sorted((path,line,class,line_sha256) tuples), separators=(',',':')))`
  over the r23 real control's `raw_hits` / `scanner_hits` / `policy_excluded_hits` gives
  `c275d2c2ea7600f45160dea966cb107377650df03656eafecb44fe7f78d9bedf`,
  `9690b3a9cf4a7daaefacb1d0d69126a81afa441c288249fc2346aa6bc65d4970`,
  `17c348f0a05e4b7827de754fd7b5d57c75f94203377b86155bfe51b8b3a9c5f7` — equal to
  `frozen/c1-expected-real-identities.json` (`digests`) and to
  `evidence/measure4/c1-real-control.json → c1_real_control.identity_pins`
  (`identity_match true`, `twin_rejected true`, `receipt_pin_match true`).
* **The C1 cutover did not hide the debt.** Removing `raw_unallowlisted` leaves the same
  count under a canonical name: `evidence/measure4/c1-real-control.json` shows
  `scanner_unallowlisted 4` (expected 4, matches true), `raw_not_allowlisted 9`,
  `raw_total 95`, `policy_excluded 5`, `scanner_total 90`, `retention_state "red"`,
  `privacy_clearance false`, `forbidden_keys_present []`. The reconciler's own output
  therefore still states the debt in red with no clearance.
* Nothing in the round-23 delta redaction- or allowlist-expands the four hits: the only
  changed production file is `tools/mori-retention-reconcile.py` (2 lines: `SCHEMA`
  `…-v1`→`…-v2` and deletion of the `'raw_unallowlisted':len(unallowed),` producer
  fragment) plus the new read-only `tools/mori-quota-surface.py`. No
  `corpus/evidence/retention-allowlist.json`, policy, or `corpus/evidence/**` change.

### 3.2 Two unknown loss-accounting dispositions — UNALTERED (still unknown)

* `corpus/evidence/loss-accounting-r21.json` blob `c055b634d8ceff3789e0c7a015280c0254e3ac6d`
  is **identical** at ENTERING, PROD and HEAD; working tree clean for it.
* Content at PROD: `observations[0] = {id: "aggregator-r10", state: "unresolved",
  independent_disposition: null}`, `observations[1] = {id: "aggregator-r10-resume",
  state: "unresolved", independent_disposition: null}` — i.e. still `unresolved`, still no
  independent disposition.
* Required pair unchanged: `.ufo/waves/round-21/frozen/required.json` blob
  `6124b34fd3e2382290e754e78c35a5d1e6b81e85` at ENTERING and PROD; both
  `aggregator-r10*` ids still required.
* Referenced evidence still resolves byte-exactly (checked against the named revisions,
  not just the working tree): baseline
  `corpus/evidence/baseline-r10-20261015T2231Z.json@e9f340c…` =
  `0993b23505deab2aeb05b2309bdf7dd6eaad2b82f27852491352511aa9670478`;
  deletion `.ufo/waves/round-21/evidence/removal-metadata.txt@a8442a0…` =
  `4276625be64ab1943bb5781dab7a3d9e8c912bdb48ea562870f20b70b753263e`;
  cleanup `.ufo/waves/round-21/evidence/cleanup-receipts.tsv@a8442a0…` =
  `46f84c3a60ac701ec7d0c16523e5bbfa999be3999cb61029be8fba50785970a7`; all 6 accounting
  references and both required references match.
* The audit tool itself is unchanged: `tools/mori-evidence-loss.py` blob
  `98cc66e1f4cd0bcbc77104dbbe5f1f3be7431ea1` identical at R21, PROD and HEAD. Its decision
  logic still forces `state == "unresolved"` → `unresolved` finding
  (`tools/mori-evidence-loss.py:545-547`) and `pin_allowed = False` unconditionally
  (`:613`, `:630`), and `audit()` returns rc 1 — i.e. a rerun would still be
  "2 unresolved, pin blocked", never 0.
* No round-23 file mentions `aggregator-r10` and no r23 artifact writes a
  `mori-loss-accounting-v1` document; grep over `.ufo/waves/round-23/**` (excluding the
  frozen seat payload/registry blobs) finds no `independent_disposition` write and no
  "disposition resolved" claim. The r23 wave added no accounting document at all
  (no added file contains the `mori-loss-accounting-v1` schema).

### 3.3 Old red original permission control — UNALTERED (RED 11/12)

* The r21 control receipt is byte-unchanged: `.ufo/waves/round-21/evidence/final/
  fixture-original-observed.json` blob `137ff1f0d6bd864ce1d546f2dd31fdd00e04b2cc` at
  ENTERING and PROD (and the whole `.ufo/waves/round-21/` tree is unchanged
  ENTERING→PROD, `git diff --stat` empty).
* Its content: 12 cases, **11 fully passed**, 1 failing — case `valid-independently-disposed`
  expecting `run-1-expected-rc 0` / `run-2-expected-rc 0`,
  `run-1-count-unresolved 0` / `run-2-count-unresolved 0`,
  `run-1-count-pin_allowed True` / `run-2-count-pin_allowed True`, observed
  `1 / 1 / False` in each pair. That is the recorded "expected
  original-positive-permission contradiction" (`r21 summary.json → fixtures.original_control
  = {matched 11, total 12, rc 1}`).
* The red is structural, not incidental: the failing case demands `pin_allowed == True`,
  while `tools/mori-evidence-loss.py:613` sets `pin_allowed = False` unconditionally
  ("This observer has no authenticated outside-acceptance input"), and the fixture that
  produced the 11/12 (`.ufo/waves/round-21/fixture-loss.py`) and the frozen cases
  (`.ufo/waves/round-21/frozen/cases.json` blob `e7ccfb4c31252e777ef48d797ee64abfa4193abe`,
  `before-rule.json` blob `c0cdb1891beab51ddeb428de42a6ff7a771ab124`,
  `after-rule.json` blob `0bf3b407e0d4e31b90a0dc51a71602a00939d8c7`,
  `before-accounting.json` blob `17a91f3817aab034a84d1c15e6a24aafbcb6661e`) are all
  unchanged. A rerun against the unchanged tool and unchanged fixtures therefore
  reproduces 11/12.
* The lane states this honestly: `evidence/measure4/summary.json →
  carried_open_debt.original_permission_control = "RED 11/12 retained byte-unchanged,
  not rerun"` — it does not claim a fresh measurement.
* Not rerun here: this seat's item authorizes no fixture/driver invocation, so §3.3 is a
  preservation proof (byte identity + tool logic), not a fresh red receipt. See G2.

### 3.4 Blocked baseline acceptance and privacy clearance — UNALTERED (blocked)

* The governing criterion is untouched: `corpus/QUALITY.md` (criterion 69: a disappearance
  without an independently evidenced per-identity settlement/cleanup-accounted disposition
  is `census-regression` and **blocks baseline acceptance**; the r20 baseline is a retained
  historical artifact, **not an accepted behavioral reference**) is byte-identical
  ENTERING→PROD (`git diff --stat` empty). `PROVINCE.md` and `corpus/README.md` are also
  byte-identical ENTERING→PROD, including the standing statement "Original permission
  control 11/12 remains red, two historical dispositions remain unknown, and the invalid
  r20 baseline is not accepted or re-pinned."
* No re-pin / acceptance artifact: the round-23 delta contains no baseline, pin,
  acceptance or census file; `tools/mori-census.sh` is unchanged
  (`git diff --stat` empty); `corpus/knowledge/drift-repin-r20.md` blob unchanged.
* No clearance claim anywhere: grep over the entire ENTERING→PROD diff and over
  `.ufo/waves/round-23/**` finds **no** `privacy_clearance: true`, no `pin_allowed: true`,
  no `baseline accepted` / `acceptance granted` / `promotion granted` phrasing, and no
  "debt cleared" / "no longer debt" statement. The r23 outputs and docs state the
  opposite: `corpus/lessons/round-23.md:18-19`, `corpus/knowledge/quota-surface-r23.md:96-97`,
  `SKILL.md:604-605`, `SCORECARD.md` round-23 block, `LOG.md` r23 tail — all carry
  "four unallowlisted hits, permission control RED 11/12, two unknown dispositions, baseline
  acceptance blocked, no privacy clearance".
* `corpus/knowledge/quota-surface-r23.md` explicitly separates visibility from clearance:
  "Privacy/history clearance and baseline acceptance remain blocked by the existing
  independent debt, not changed by quota visibility" — the new probe grants no acceptance.
* Sibling falsify reports are consistent: no report in `.ufo/waves/round-23/falsify/*.md`
  claims clearance; e.g. `C1R18.md:287` "none of it is cleared here",
  `CriticC2Scope.md:233` "Open debt (unchanged, not cleared)".

## 4. Findings by severity

**F1 — MEDIUM (traceability, not state): the lane's "still debt" evidence for the four hits
is bound to a stale revision, and the summary's debt block is a constant, not a measurement.**

* `evidence/measure4/c1-real-control.json` reconciles at `input_revision
  77a5bbe8a0b41dfbfd2546d024d36e294b814bd0` / `measured_revision
  9fb1f911cfdd6061005c300795f44b1b45523897` — the r21 receipt and the r21 measured tree,
  **not** the production pin `f3dc07c`. It therefore cannot by itself evidence that the
  four hits persist in the current tree.
* The current-tree receipt is `evidence/retention-floor-delivered.json` at
  `measured_revision 56ac3badb…` (MID), two commits behind PROD, plus
  `evidence/retention-floor-comparison.json` (also MID).
* `summary.json → carried_open_debt` is a hardcoded literal in the driver
  (`.ufo/waves/round-23/build/MeasureDriver/measure-round23-v2.py:1163-1169`:
  `unallowlisted_retention_hits: 4`, `original_permission_control: "RED 11/12 retained
  byte-unchanged, not rerun"`, `historical_dispositions: "two unknown"`,
  `baseline_acceptance: "blocked"`, `privacy_clearance: False`) — it is emitted
  unconditionally and is never computed from a measurement, so it can neither detect nor
  falsify a change in the debt.
* Consequence: the *state* is correct (independently recomputed at PROD and HEAD in §2,
  metric 4, identical identities) but the *receipt chain* for "the debt is still there at
  the pin" is one-to-two commits stale and the summary asserts rather than measures.
  A future round that changes the tree could emit the same `carried_open_debt` block with
  a different underlying reality.
* Non-remediation note (not mine to execute): the fix belongs to the driver — measure the
  gate metric at the measured revision and record the revision the claim is bound to
  instead of writing a constant, or label the block explicitly as an assertion with a
  receipt pointer. No file was changed by this seat.

**F2 — LOW (presentation): a hardcoded debt block is emitted in the same JSON as measured
claim checks, with no marker distinguishing assertion from measurement.**
`summary.json` presents `carried_open_debt` next to `c1_original_26` /
`c1_supplementary` / `c2` results, all of which are measured; a reader can take
`unallowlisted_retention_hits: 4` for a measurement of the pin. Same root cause as F1;
same suggested remedy (marker or computation). No state effect.

**F3 — LOW (residual, disclosed): the r22 driver in the tree no longer reproduces r22
in-lane, by design of the C1 cutover.**
`.ufo/waves/round-22/measure-round22.py:58` runs the **lane working-tree** tool
(`tool=LANE/'tools/mori-retention-reconcile.py'`), whose v2 output no longer contains
`raw_unallowlisted`; the r22 oracle and refinement checks read that key
(`.ufo/waves/round-22/oracle-reconcile-v2.py:48,52,53`;
`.ufo/waves/round-22/refinement-reconcile.py:186-192`). The r22 `safe_outputs` whitelist
is a subset test (`set(value) <= allowed`, `measure-round22.py:20,28`) and is therefore
*not* broken by key removal — the key-read checks are. This is pre-registered and
disclosed: `preseal-amendment.md` §"C1 bounded clean cutover", `contract.md` §C1
"Declared consequence", `corpus/knowledge/retention-reconciliation-r22.md` §"Round23 API
correction", `SKILL.md` r23 row, and the r23 driver `scope_notes.r22_reproduction =
"not attempted…"`. **No debt effect:** the four-hit metric is produced by
`tools/mori-retention-gate.py` (unchanged) and the permission/loss/baseline authorities are
independent of the reconciler key. Residual risk is operational only: an operator running
the r22 driver in-lane sees unexplained failures and must reproduce in a checkout of
`da40bb20f81da125d798f73cd1653655be1255ca`.

**F4 — INFO: no reclassification, clearing or acceptance found.** Positive confirmation:
allowlist (86 rows, 0 forbidden) and policy bytes unchanged; `corpus/evidence/**`,
`corpus/QUALITY.md`, `corpus/README.md`, `PROVINCE.md`, `tools/mori-evidence-loss.py`,
`tools/mori-retention-gate.py`, `tools/mori-census.sh` unchanged ENTERING→PROD; the whole
`.ufo/waves/round-21/` tree unchanged; `corpus/knowledge/drift-repin-r20.md` unchanged;
no r23 file contains `privacy_clearance: true`, `pin_allowed: true` or an acceptance
claim; the only changed production file is the two-line C1 cutover in
`tools/mori-retention-reconcile.py` plus the new read-only `tools/mori-quota-surface.py`.

**F5 — INFO: the frozen contradiction (C2 `CaseEscapedSpace`) is unrelated to this item and
was left untouched.** `evidence/frozen-contradiction.json` (seal `22772c1…`, case
`.ufo/waves/round-23/frozen/quota-cases/CaseEscapedSpace.json`,
`sha256 8340738a509e474a94a815637e66b407dfb60c6449511e52db55296d844abeea`) records
`primary_pass 26/27`, `supplemental_pass 3/3`, `pass 29/30`, and the strict
`ambiguous_overmount` vs the frozen expected `enabled` row. It contains no debt, clearance
or disposition claim; it is unaffected by this review and is not reclassified here.

## 5. Residual risk and verification gaps

* **G1 — the lane's committed "debt still 4 at the pin" receipt is at MID (`56ac3ba`), not
  at PROD (`f3dc07c`), and the C1 real control is bound to the r21 tree.** Closed for this
  review by the independent recomputation in §2 (PROD and HEAD both: raw 95 / allowlisted
  86 / non-author 5 / metric 4 / identical identities / 0 forbidden / 0 stale). It remains
  open as a *lane receipt-chain* gap for the next round's driver to close by measuring at
  the measured revision.
* **G2 — RED 11/12 was not rerun here** (no invocation authorized for this seat). The
  preservation argument is byte identity of the tool, fixture, frozen cases and the
  recorded receipt, plus the tool's unconditional `pin_allowed = False`
  (`tools/mori-evidence-loss.py:613,630`) and rc-1 audit return. A fresh 11/12 receipt
  would require a fixture invocation outside this item's authorization.
* **G3 — the two dispositions are verified as "still recorded unresolved with no
  independent disposition", not as "still correctly unknown".** Whether the underlying
  `aggregator-r10*` disappearance has since acquired an independent, actor-distinct
  disposition is outside the lane's authority to settle (QUALITY 69; PROVINCE §
  independent-disposition ownership) and outside this item; nothing in the r23 delta
  asserts such a disposition either way.
* **G4 — privacy clearance remains false in every measured output, but "false" is a
  property of the tool's own field, not an independent privacy assessment.** The frozen
  policy is a recall floor, not a privacy proof (policy `known_limit`); the four
  unallowlisted hits are regex-visible only. No clearance is claimed and none is implied
  by this review.
* **G5 — untracked wave artifacts** (`.ufo/waves/round-23/falsify/**`,
  `wave2-*.json`) are outside the committed tree and were scanned for policy-class hits
  only (0 found). They carry no debt claim that I could audit against committed bytes;
  they are sibling work products, not authority.
* **G6 — the four-hit path is a nested byte-identical copy of the policy source under
  `.ufo/waves/round-20/falsify/NoHarmRun/rg/…`.** It is tracked, unchanged and is the
  sole carrier of the four unallowlisted hits. No redaction or allowlist change was made
  here; remediation remains operator/L1 territory and out of scope for this review.

## 6. Bottom line

| debt item | state at PROD/HEAD | evidence class | reclassified? |
|---|---|---|---|
| four unallowlisted retention hits | metric 4, identical identities, raw 95 / allowlisted 86 / non-author 5 | independent recomputation (git plumbing) + lane receipts at MID/r21 | no |
| two unknown loss-accounting dispositions | both `unresolved`, `independent_disposition: null` | byte identity + tool decision logic + digests at named revisions | no |
| old red original permission control | RED 11/12 retained, not rerun | byte identity of tool/fixture/frozen cases + recorded receipt | no |
| blocked baseline acceptance / privacy clearance | blocked; `privacy_clearance false` | unchanged QUALITY 69 / PROVINCE / README, no acceptance artifact, no clearance claim in delta | no |

Nothing was reclassified or cleared. The two findings that deserve attention are
traceability-only: the driver's `carried_open_debt` block is a constant (F1/F2) and the
lane's own current-tree retention receipt predates the pin (G1). The debt state itself
is confirmed intact by an independent recomputation, not by restating the lane's prose.

Tool installs/updates this seat: none.
