# OutsideClosure — r21 bounded scope, calibration score, retention-denominator clarification

Seat MoriR22.OutsideClosure (scout, read-only). Lane HEAD observed `306e06ecd02e0ea8e544fbd30d1ff7e7359c581e`;
latest SCORECARD commit `77a5bbe` (round-21 landing). No tests, builds, gates or retention scans were run;
every count below is a `jq` projection of retained, committed receipt bytes, not a fresh measurement.
No matched text was read into or emitted from this report. No installs.

## 1. Latest r21 bounded scope and calibration score (SCORECARD.md:1280-1346)

- Scope: steered round21 only — C1 retained disappearance accounting (freshness5 held), C2
  evidence-loss-first permission correction (calibration5 held). Measured at `9fb1f911cfdd6061005c300795f44b1b45523897`.
  "Planned scope remains the completed steered round21 only" (:1345-1346).
- Calibration: **5 held**, verdict "improved bounded calibration"; frozen synthetic mismatches 2→0 of 6,
  outside-adjudicated sample 1→0 of 2; "Six synthetic cases establish consistency only" (:1317).
- No score increase, promotion, settlement, positive authorization or privacy clearance (:1339-1341).
- Retention sentence: "Retention floor4→4 identical inherited policy-copy hits, rc1 both; still red." (:1340-1341).
  It states no raw or scanner denominator.

## 2. Direct referenced evidence (observed)

Receipts `.ufo/waves/round-21/evidence/final/retention-floor-entering.json` (`--rev e9f340c`) and
`retention-floor.json` (`--rev 9fb1f91`), both schema `mori-r21-command-receipt-v1`, measured_revision `9fb1f91`,
exit_code 1, finding_id `RETENTION_FINDINGS`, policy_sha256 `db06e981…3128`, using the frozen
`.ufo/waves/round-18/frozen/c1-policy.json` and `corpus/evidence/retention-allowlist.json`.

| Field (both receipts identical) | Value |
|---|---:|
| hits (raw) | 95 |
| allowlisted_hits | 86 |
| unallowlisted_hits / metric | 4 / 4 |
| non_author | 5 |
| forbidden_allowlist, routed, warnings | 0, 0, 0 |
| distinct hit paths | 32 |

Partition by identity (path, line, class, line_sha256), computed from the receipt lists:
- 86 allowlisted + 4 unallowlisted + 5 other = 95. The 5 "other" are exactly the non-author population:
  `corpus/lessons/round-17-verifier-spotcheck.md` (3) and `corpus/lessons/round-18-verifier-spotcheck.md` (2),
  matched by the policy's `non_author_paths_glob` (`corpus/lessons/round-*-verifier-spotcheck.md`, `corpus/lessons/operator-*.md`).
- The exact policy path `.ufo/waves/round-18/frozen/c1-policy.json` carries **4** hits, all allowlisted.
- All 4 unallowlisted hits sit in `.ufo/waves/round-20/falsify/NoHarmRun/rg/.ufo/waves/round-18/frozen/c1-policy.json`,
  which is the **same blob** `8bf285bddce57f7fdefbbf514cb0b3bf97652742` as the policy at e9f340c, 9fb1f91, 77a5bbe and HEAD.
  So SCORECARD's "policy-copy hits" is accurate.
- "0 new": the sorted identity multisets are byte-equal across entering and final receipts
  (unallowlisted digest `c12b24df…5c7f`, full raw hit digest `1437530e…0a65`).
- The policy and allowlist blobs are unchanged from e9f340c through HEAD (`8bf285b`, `f8be55b`).
- r21 `claims-observed.json` and `measure-claims.json` carry no retention or denominator fields, so the two
  floor receipts are the only retained denominator source.

## 3. Reconciliation with the independent count (95 raw / 5 policy-source / 90 scanner / 4 unallowlisted / 0 new)

| Population derived from retained identities | Count | Matches the independent count? |
|---|---:|---|
| raw | 95 | yes |
| raw − 5 non-author hits excluded by the policy glob (author population) | 90 | yes, = 86 + 4 |
| raw − exact supplied policy path | 91 | no |
| raw − every blob equal to the policy (path + copy) | 87 | no |
| unallowlisted (all in the policy-copy blob) | 4 | yes |
| new unallowlisted identities, entering→final | 0 | yes |

Finding (high confidence for the arithmetic, `[INFERENCE]` for the meaning): the only retained identity partition
that gives exactly 95→90 removes the **5 policy-excluded non-author hits**. It does not remove hits in the policy
source file (4). The independent "5 policy source hits" therefore agrees with retained evidence when it is read as
"5 hits excluded by policy". Read literally as "5 hits in the policy file", it disagrees with the receipt (4 there,
8 across both byte-identical blobs). I cannot see the independent scanner's hit identities, so which reading is
meant stays unresolved.

Contract impact for L1: contract.md:13-15 defines the scanner-compatible denominator as raw minus exactly the
supplied policy path. Applied to the retained r21 receipt, that gives scanner_total=91, not 90. R03/R04 fixture
semantics (5→1→4) are internally coherent, but L1 MUST NOT label a real-receipt scanner_total of 91 as agreeing
with the independent 90. The 95→90 delta reconciles to `non_author` (already a separate field, R12), not to
`policy_excluded`. This is detection only; I do not recommend changing the frozen contract here.

## 4. Proposed append-only SCORECARD clarification (not applied; L1 owns production edits)

Append after SCORECARD.md:1346, without touching existing bytes:

```markdown
Round21 retention-denominator clarification (2026-10-21, append-only): both retained floor
receipts (`evidence/final/retention-floor-entering.json`, `retention-floor.json` under round21
waves; measured9fb1f91, rc1) report raw hits95 = allowlisted86 + unallowlisted4 + non-author5.
The independent scanner denominator90 equals raw minus the5 policy-glob non-author hits
(round-17/18 verifier-spotcheck lessons), not minus the policy source file, which carries4
allowlisted hits (raw minus that path is91). All4 unallowlisted hits are in a round20 falsify
copy that is the same blob as the frozen policy (8bf285b); entering/final identity multisets are
equal, so new hits are0. Agreement of these counts is accounting only: retention stays red,
privacy_clearance=false, the original permission control stays RED11/12, both disappearance
dispositions stay unknown and baseline acceptance stays blocked. No score, admission or round
change; outside closure decides.
```

## 5. Remaining unknowns

- The independent scanner's own hit identities (needed to confirm the "5 = non-author" reading rather than an
  unexplained policy-file count difference).
- Whether a policy-path-only scanner_total (91) or the author-population total (90) is the intended "secondary
  scanner-compatible denominator" for r22 claims. That is L1's or outside closure's decision.
- Nothing here authenticates private-data absence; a source hash is not secrecy.
