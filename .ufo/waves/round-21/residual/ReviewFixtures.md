# ReviewFixtures — round 21 residual review (independent fixture + Mut* probes)

Scope: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-21/fixture-loss.py`
(sha256 4217d234a600e7f27fb8301559873bd7258924e62374ee2d48228b1bb6d2155f) and the four
proposed probes `build/Mut{OldPermission,LostIdentity,DigestTrust,CleanupDisposition}`,
reviewed statically against the integrated evaluator
`tools/mori-evidence-loss.py` (sha256 62fdddbb58894b8d8fd8b67905346b3cf4c8ad240944e1876371e5ea321df511),
`.ufo/waves/round-21/contract.md`, and `.ufo/waves/round-21/trust-refinement.md`.
Frozen bytes touched: none. No target execution (probe/fixture/classifier never invoked);
git used read-only for static blob/digest cross-checks only; all reports written only to
this seat path. Seated as MoriR21.ReviewFixtures.

## Severity-ordered findings

### BLOCKER-1 — fixture harness cannot pass acceptance as authored: `duplicate-accounting-id` rc expectation is stale
- Evidence: `.ufo/waves/round-21/fixture-loss.py:281-283` expects `expected_rc: 1` for
  `duplicate-accounting-id`. The evaluator treats duplicate accounting ids as load-time
  input failure: `tools/mori-evidence-loss.py:377-378` raises
  `SetupError("duplicate_observation_id")` inside `_load_accounting`, `:1216-1218` maps it
  to rc2 with a `mori-evidence-loss:setup:*` payload. The evaluator's own `--selftest`
  pins exactly this (`:943-953`: expected rc2, finding
  `mori-evidence-loss:setup:duplicate_observation_id`). The contract's rc taxonomy
  (`contract.md:14` raw section, "rc2 setup/input failure") classifies a malformed
  duplicate-keyed document as input failure, not a per-row blocker (rc1).
- Classification: **fixture-side defect against the shared interface**, not an evaluator
  defect. Distinct from the stale positive control below: `build/FixtureLoss.md:5-22`
  documents the disposed control as intentionally retained from the original contract,
  but nowhere discloses that the duplicate case will also fail — so one L1 acceptance run
  would report `failed>=1` with two mixed causes, one documented, one not.
- Consequence: deterministic case failure + at least `-valid-output` failures (the rc2
  payload carries no `issues`/counters, `fixture-loss.py:340-355` flags them). The case
  must be re-specified (rc2 + setup-class finding, tolerance for a non-audit payload) or
  explicitly waived in writing before acceptance; otherwise the harness summary conflates
  a genuine stale control with an unacknowledged one.

### HIGH-1 — MutCleanupDisposition's independent positive control encodes the superseded contract; kill is unreachable
- Evidence: `build/MutCleanupDisposition/probe_cleanup_disposition.py:275-283` requires
  `independent_control` = `{unresolved:0, disposed:1, invalid:0}`, `pin_allowed=True`,
  rc0, and zero issues (`:64-65`). Under trust-refinement the evaluator *must* return the
  same row structurally disposed but blocked: `tools/mori-evidence-loss.py:580-595`
  appends `disposed` (status `structural_only`) **and** an `unresolved` entry with reason
  `external_review_required`, sets `pin_allowed=False` (`:612-619`), rc1 (`:636`).
  `trust-refinement.md:5` makes this mandatory.
- Consequence: `failures` is always non-empty (control fails for the exact behavior C1
  now mandates), so the script skips the mutant check entirely (`:295`) and can never
  emit `killed` — every run returns 2/inconclusive. The mutant logic itself is sound and
  would kill correctly once the control is updated: cleanup refs carry `actor`
  metadata (`:156`), so `independent_actor_not_distinct` fires
  (`tools/mori-evidence-loss.py:573-576`) and the expected finding
  `...:independent_disposition:independent_actor_not_distinct` (`:27-30`) matches
  `_finding_id` exactly (`:451-452`, `:506`).
- Ruling: per seat instructions, a probe whose *healthy* control contradicts the
  co-evolved contract produces no evidence either way; it must not be counted as a kill
  of anything, and the finding above is a probe defect, not an evaluator regression.

### HIGH-2 — MutDigestTrust symlink case expects the wrong refusal token; overall verdict permanently "inconclusive"
- Evidence: `build/MutDigestTrust/proposed-probe.py:260` demands reason `unsafe_path`
  for `symlink-substitution`. For a symlinked final path component the evaluator raises
  `unsafe_symlink` (`tools/mori-evidence-loss.py:196-199`), yielding
  `audit:{WAVE}:independent_disposition:unsafe_symlink`. The contract names no literal
  reason strings, so this was a probe-author guess.
- Consequence: `refusal(...)` is False; the mutated detector then fails the
  "rejected-or-blocked" branches (`:262-266`) and the case ends "inconclusive", so the
  overall status can never be `killed` (`:302-308`). The other half of this probe is
  correct and notably the *only* fixture-family positive control that already encodes
  the co-evolved semantics exactly (`:166-179`: disposed+structural_only +
  unresolved `external_review_required` + `pin_allowed False` + the single review
  issue) — verified against `:580-595,612-635`. One-line fix: expect `unsafe_symlink`.

### MEDIUM-1 — fixture `valid-independently-disposed` is stale *and* internally malformed; keep adjudicated, do not re-baseline
- The stale part (documented): `fixture-loss.py:266-269` expects rc0 /
  `unresolved:0` / `pin_allowed:true` — original-contract reading of "rc0 only complete
  valid accounting and zero unresolved" (`contract.md:14`). `trust-refinement.md:5`
  supersedes it; `build/FixtureLoss.md` (Trust refinement section) honestly declares the
  mismatch will be retained, "not a test pass and not silently normalized". Honor that:
  at acceptance this case's observed-vs-expected delta is the *expected* stale-control
  outcome, not a C1 evaluator failure.
- The malformed part (not documented, would persist even under pre-refinement
  semantics): the committed disposition artifact carries extra keys `fixture` and `kind`
  (`fixture-loss.py:144-152`), while `_disposition_record_matches` requires the exact
  key set `{id,actor,wave_id,disposition,independent}` (`tools/mori-evidence-loss.py:462`)
  → `disposition_record_mismatch`. Additionally the accounting cleanup provenance has no
  `actor` metadata (`fixture-loss.py:200-201`), so every disposed fixture row first hits
  `cleanup_actor_missing` (`:540,573-574`) — the evaluator cannot even evaluate the
  distinct-actor rule. Net effect for this row today: `invalid≥2`, unresolved via
  `disposition_invalid` (`:596-601`), `disposed=0` — i.e. the row is refused for
  authoring reasons *before* the trust question is reached. Anyone turning this case
  into a "passing" co-evolved case must fix all three (drop `fixture`/`kind`, add
  cleanup-actor metadata, expect rc1/unresolved1/pinFalse); adding only the second
  would be evidence laundering. The evaluator's own selftest shows the canonical clean
  record (`:806`: five keys, no decoration), as do MutDigestTrust
  (`proposed-probe.py:110-111`) and MutCleanupDisposition
  (`probe_cleanup_disposition.py:137-140`).

### MEDIUM-2 — fixture `same-actor-cleanup-only` passes, but tests a broader failure than its name
- The named attack (independent actor identical to cleanup actor) can never be exercised
  here: with no `actor` on the cleanup provenance (`fixture-loss.py:200-201`), the
  evaluator short-circuits at `cleanup_actor_missing` and the comparison at
  `tools/mori-evidence-loss.py:575-576` is unreachable. The case still satisfies its
  asserted surface (exact `disposed:0`/`pin_allowed:false`, rc1, `unresolved≥1`,
  `fixture-loss.py:306-309`) via the generic `disposition_invalid` channel. It is a
  blunted control, not a false one; contrast MutCleanupDisposition, which does arm the
  named comparison via cleanup-ref `actor` metadata. Label it accordingly if it is cited
  as covering the distinct-actor rule.

### LOW-1 — rc0 is unreachable by design under the co-evolved evaluator
- With `external_review_required` always added for structurally valid disposed rows
  (`tools/mori-evidence-loss.py:590-595`) and `pin_allowed` requiring zero unresolved
  (`:612-619`), `rc0` can no longer occur for any real or synthetic input. Not a defect —
  it is the operational consequence of "never automatic permission from this CLI alone"
  (`trust-refinement.md:5`) — but it should be recorded so no reviewer interprets a
  permanent rc1 as anomaly, and so the fixture suite's inability to ever observe rc0
  behavior (its one rc0 case being the stale control) is understood as inherent.

### LOW-2 — MutLostIdentity is sound and its controls are anchored to real lane data; minor env nit
- Expectations (`build/MutLostIdentity/probe-lost-identity.py:25-28`) were checked
  against production inputs without executing the evaluator: both `corpus/evidence/loss-accounting-r21.json`
  rows are `unresolved` with null disposition; all six provenance references
  (baseline/deletion/cleanup × 2) hash-match both the worktree bytes and the blobs at
  declared revision `e9f340ce…` (read-only `git cat-file` cross-check), and the frozen
  baseline sha `0993b235…` matches. So pristine/restored `CONTROL` (retained2/
  unresolved2, rc1, pin False) and mutated `MUTATED` (omitted1/retained1/unresolved1)
  are exactly what the co-evolved evaluator emits (`:511-543,620-636`); a `killed`
  verdict from this probe would be meaningful and must not be dismissed as a
  broken-control artifact. Its freshness framing is correct — dropping an accounting
  row must raise `omitted`, and the probe asserts rc1 in every phase (`:146-148`),
  consistent with "blocked until disposition".
- Nit: it invokes `sys.executable` without `-I` and sets no `PYTHONNOUSERSITE`
  (`:102-106`); env is an exact dict (no `PYTHONPATH`) and the target is stdlib-only,
  so impact is nil, but sibling probes use `-I -B`; align when convenient.

## Original-contract vs co-evolved expectations (honest map)

| Control / case | Expectation source | Status under integrated evaluator |
|---|---|---|
| fixture `valid-independently-disposed` rc0/pin-true | original contract | expected mismatch, documented in FixtureLoss.md; additionally malformed (MEDIUM-1). Never a regression signal by itself. |
| fixture `duplicate-accounting-id` rc1 | fixture over-read of shared interface | deterministic failure; fixture-side defect (BLOCKER-1). |
| fixture 9 negative cases (absent, unresolved, wrong-baseline, digest-tamper, symlink, absolute, parent, `independent:false`, missing file) | either layer | all pass today; `same-actor` variant is blunted (MEDIUM-2); disposed-row negatives succeed partly via the unintended `cleanup_actor_missing`/record-mismatch channels, so single-mutation attribution is weak even where green. |
| MutOldPermission (rule-flag flip; classify) | frozen C2 objects | sound. Pinned digests `10603c9e…` / `8bf6cd9f…` byte-verified today against `frozen/cases.json` and `frozen/after-rule.json`; baseline `((0,0),(1,2))` and mutant `((1,2),(0,0))` signatures re-derived from `classify` (`:677-715`) and match; setup/timeout/errors force None signature → inconclusive, never a kill (`:101-107,139-144`). Authorizing to run. |
| MutLostIdentity (accounting omission; audit) | co-evolved | sound, anchored to real rows (LOW-2). Authorizing to run. |
| MutDigestTrust (evidence tamper / symlink swap) | co-evolved | half-stale: digest-mismatch branch correct (`hash_mismatch`, `:438-439`); symlink branch expects wrong token (HIGH-2) → indeterminate today. |
| MutCleanupDisposition (same-actor disposition) | co-evolved mutant / stale control | mutant branch correct; control stale (HIGH-1) → indeterminate today; not a kill. |

## Residual risk
- All kill/survive judgments above are static derivations from the evaluator source
  (single revision, digest recorded); classification behavior of `audit` under untested
  filesystem races (e.g. TOCTOU between the two fixture reruns) is unobserved here.
- Fixture negative disposed rows exercising multiple simultaneous failure channels
  means the suite proves "refused", not "refused for the named reason"; only
  MutCleanupDisposition's `independent_actor_not_distinct` check names a reason today,
  and only MutDigestTrust pins exact issue payloads for its positive control.
- I did not run census, pin, or any probe (per bounds); H1/H2 make two of the four
  Mut probes non-evidentiary until patched — decisions above assume the current bytes
  (file digests recorded at top) and must be revisited if any seat rewrites them.

## Verification gaps
- Target execution of fixture-loss.py and all four probes remains L1's single
  acceptance step; nothing in this review substituted for it.
- `oracle-loss.py` and the `Rule*`/`Audit*`/`History*` seats were out of scope; I used
  them only as interface cross-references.
- Procedural note: my one-off static cross-checks invoked read-only `git cat-file` with
  a relative `-C` from the lane cwd; no git state was read-modified or written, and all
  seat outputs are confined to this report file.
