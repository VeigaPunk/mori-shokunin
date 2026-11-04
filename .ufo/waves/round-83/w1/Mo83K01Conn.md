# Mo83K01Conn — cross-lane overlap scan for the three round-83 instruments

Seat: Mo83K01Conn (connector, wave w1, round 83, attempt 1). Cross-lane overlap scan, read-only.
Detection and report only: no lane file was edited by this seat except this report; no sibling
repo, fleet-root, or host state was written. No subagents. No tools installed (read-only scans
via the harness grep/read tools and one `ls`/`git log` characterization command; nothing
needed installing). Scratch dir `/fast/scratch/hyaku/mori-r83/Mo83K01Conn` was created for the
one shell command and deleted in the same command (trap semantics; `rm -rf` confirmed).

Lane tip observed: `d2987c67c14ee94f5f4030db098a50c5bcec9502` ("round-83: pre-data amendment A1
(equivalent mutant) and re-taken control"). Scan performed against worktree bytes of all 20
sibling `*-shokunin` repos plus the anomalous `kumitate-shokinin` dir (see Observation 3).

## The three surfaces (from the frozen contract)

- **(a) Counter mutation adequacy** — mutation-testing a suite against anchored mutants:
  `.ufo/waves/round-83/count-c1.py` re-derives the 23-mutant anchored table and grades each
  mutated copy's own `--selftest` (P-C1, operability).
- **(b) Snapshot-bound classification with as-of** — `.ufo/waves/round-83/count-c2.py` grades
  `corpus/evidence/drift-classification-r82.txt` headers `# Snapshot:` / `# Snapshot-sha256:` /
  `# As-of:` against the committed raw snapshot `.ufo/waves/round-82/evidence/drift-r82-live.txt`
  (P-C2, calibration).
- **(c) Line-anchored occurrence in revision bytes** — `tools/mori-record-sweep.py`'s revision
  arm requires, on one line of `git show <rev>:<path>`, both the `key=value` token and the
  binding's `row_contains` anchor, with an `elsewhere` defeated fixture (P-C3, depth).

## Verdict rows (owner | evidence path:line | verdict | what mori must not claim)

### Surface (a) — counter mutation adequacy

| owner | evidence path:line | verdict | what mori must not claim |
|---|---|---|---|
| **tameshi-shokunin** (generic craft owner) | `tameshi-shokunin/PROVINCE.md:3-5` ("Domain: verification-fixture craft — … mutation testing …"), `:14-17` ("every lane's gate remains its own; tameshi owns only the reusable craft"); `tameshi-shokunin/tools/mutate-and-run.sh` (ls-confirmed), `repeat-control.py`, `pin-disposition.py`, `bash-witness-study.py`; `tameshi-shokunin/corpus/knowledge/fleet-kill-rate-ledger.md`, `mutation-score-semantics.md`, `witness-scoped-kill-verdict.md`, `arm-class-matrix.md`, nine `mutation-case-*.md` entries; recorded for the fleet at `tabi-shokunin/.ufo/waves/round-13/w1/SiblingOverlap.txt:33-39` | **overlap-declared** (tameshi declares generic ownership; mori's gate instance stays mori's own) | The mutation-testing *method*, the fleet-wide kill-rate regression ledger, cross-lane mutation audit of other lanes' gates, "first mutation-adequacy instrument in the fleet", or any novelty claim for anchored kill/survivor grading. Also not: the arXiv-2102.11378 and PIT source ground as fleet-fresh — tameshi's registry already holds both (`tameshi-shokunin/.ufo/evidence/kaika-round-1/sources-opened.tsv:9` S008 = arXiv:2102.11378; `:33` S041 = pitest.org); mori's S595/S598 are per-lane registry rows, tolerated as W04 duplicates, not new mining. |
| revenger-shokunin | `.ufo/waves/kaika-r1/mutation-post-l2.md:1-7,35-67` (mutation table, `killed 22/22 = 100%`, pristine+adversarial-probe detector); `.ufo/waves/kaika-r1/mutation-post.md:27` (KILLED 10/12); `.ufo/waves/round-61/build-dispatch.json:813-815` (MutantEvmVerifier), `:898-900` (MutantJsVerifier), `:973-975` (MutationReceiptConjuncts); `round-61/build/CriticCalibrationClaim.md:1-8` | contested (same instrument, own verifiers) | Nothing — revenger's tables grade its own `verify_*.py`; no overlap with mori's counters. |
| kengaku-shokunin | `.ufo/waves/round-25/falsify/MutDedupManifest.md:1-5,40-41` (3/4 killed), `MutRgBound.md:3-5` (six one-line mutants), `MutStateCheck.md:16-35` (2/5 killed), `MutVerdictBoundary.md:30-31`; `round-25/falsify-dispatch.json:930-931` ("Report which mutants survive (selftest still 0) — each survivor is a coverage gap") | contested (same instrument) | Nothing beyond the generic method ban. |
| game-dev-2d-shokunin | `LOG.md:14-15` (round-1 "targeted exit-2 mutant", no-follow mutant fixtures); `corpus/fixtures/run_battery.py:5464-5467` (`mutant_broken_scene_route`, `mutant_level_collision_removed`); `SCORECARD.md:259-260` ("120/120+ semantic mutations rejected", "mutants redden") | contested (same instrument, game fixtures) | Nothing beyond the generic method ban. |
| game-dev-3d-shokunin | `LOG.md:18-20` (`mutation-verdicts.json` since round 1); `SCORECARD.md:167` ("mutation matrix 6/6 load-bearing"), `:179` ("mutation coverage author 9/9 + verifier's own 4-mutation set"), `:296` (`r101-mutation-tester.md` 11/11); `considerthese/2026-10-22.md:21-22` (gate-draft.sh "mutation-tested 27/27") | contested (same instrument) | Nothing beyond the generic method ban. |
| audio-shokunin | `corpus/knowledge/2026-10-14-sox-preemptor-map-complete.md:44-47` ("15 single-byte mutants → no-detect"); `corpus/live/r78-critic/replay_gates.py:6-8` (targeted mutations → "which mutations still pass (forged/vacuous PASS) vs which are caught"); `LOG.md:1420-1421` ("revert mutants red") | contested (same instrument, detector fixtures) | Nothing beyond the generic method ban. |
| chousa-shokunin | `.ufo/waves/round-8/goal-wave/report-draft.md:117-130` (three scratch-copy gate mutants graded by `--drift` **and** the mutant's own selftest; banner-word mutant "selftest TOLERATES this class" at `:127` — the exact asymmetry mori's C1 counter grades); `round-25/build-dispatch.json:759-760` (ExecMetaMode "Build a mutant fixture set") | contested (same instrument) | Nothing beyond the generic method ban. |
| kasegi-shokunin | `.ufo/waves/round-23/falsify-spec.json:163-178` (three mutation-tester seats: MutateBountyConfine / MutateRelConfine / MutateBoundary); `round-23/falsify/CvssRecheck.md:171-179` (mutant table on a capture copy) | contested (same instrument) | Nothing beyond the generic method ban. |
| tabi-shokunin | `.ufo/waves/round-15/w1/CountReasonWitness.md:58` (`count_reason_mutant_control`: temp copy of the script bytes "with the single literal M1 replacement. If the replacement count is not exactly 1, fail" — an anchored-mutant arm, same shape as mori's anchor rule); `.ufo/waves/round-13/metadata-witness.py:43-52` (mirror-field mutations) | contested (same instrument) | Nothing beyond the generic method ban. |
| kagi-shokunin | `.ufo/waves/round-24/separability/c3-only/expected.json:10-11` ("15 same projected-identity mutants killed; controls exit0"); `.ufo/waves/round-23/falsify/CritVolatility.md:162` ("surviving mutants 288"); `.ufo/waves/round-25/build/ConnSiblings1.md:37-38` (kagi itself cites tameshi `mutate-and-run.sh:1110-1117` as the reusable convention) | contested (same instrument) | Nothing beyond the generic method ban. |
| **mori (self, prior claim — re-claim rule)** | `corpus/README.md:867-871` (coverage-map row "Mutation analysis as a test-adequacy criterion (r80, S595)" → `knowledge/mutation-adequacy-r80.md`); `knowledge/counter-mutation-adequacy-r83.md:1-3, K2 table` (S598; already lands this round); boundary in `knowledge/mutation-adequacy-r80.md` ## Boundaries: "the lane's own gate-quality craft, not a claim about another lane's tests" | **overlap-declared (self)** | mori must not re-claim the mutation-adequacy ground as new growth: it is already claimed (r80) and indexed in its own coverage map; r83's entry extends the same ground with the four requirement rows (pristine-green / anchored / two-channel kill / detector gate). Verdict wording for the round: "the r82 probe's 20 counter survivors get their named failing arms" — a lane-instance claim, never a method claim. |

Net for (a): **overlap-declared** — tameshi owns the generic mutation-testing craft and the
fleet kill-rate ledger; every attack lane runs its own instances; mori's frozen 23-mutant
anchored table against its own counters' `--selftest` is a distinct *instance* (no sibling
mutates mori's counters; mori mutates no sibling's gate), but the *method* is claimed
fleet-wide and must be credited as borrowed craft (mori's own r83 entry already cites S598
PIT; tameshi holds the same literature at S001–S046).

### Surface (b) — snapshot-bound classification with as-of

| owner | evidence path:line | verdict | what mori must not claim |
|---|---|---|---|
| **no sibling holds the surface** | Cross-lane grep for the frozen grammar `Snapshot-sha256|Snapshot:|run-start:` across all 20 sibling repos: zero hits; the only `As-of:` usages are report-header discipline (`kengaku-shokunin/.ufo/waves/round-77/w1/ScoutFrontierR77.md:10-13`) and wave-registry bookkeeping (`kotoba-shokunin/.ufo/waves/round-80/build/Kb80S14WaveRegistry.md:3`), not snapshot bindings | **distinct** (exact surface unheld) | — |
| kasegi-shokunin (nearest neighbor) | `.ufo/waves/round-38/wave1/ExecC2QuoteOnce.md:234-237` ("Line pins are snapshot-bound … 1-based normalized lines of the sha256 `63c8ad5271…e11cd42` capture; a re-capture with different bytes invalidates all of them"); `round-37/wave1/ScribeFrontierAmendments.md:139-141` (quote anchors bound to capture sha `ff3f3b2c…`) | contested (adjacent) | The general idea "bind a derived record to the sha256 of the bytes it was derived from" for **external-source quotes/captures** — kasegi owns that quote-pinning surface; mori's C2 binds a *classification of live census tokens* to a *committed raw snapshot file* with a graded as-of moment; different substrate, different population, different header grammar. Do not use kasegi's "snapshot-bound" vocabulary for mori's census snapshot without naming the distinction. |
| chousa-shokunin (nearest neighbor) | `round-8/goal-wave/report-draft.md:178-179` (committed lane baseline `corpus/evidence/gate-baseline-r8-20261016T033757Z.json` sha `1c81a6cb…`; `GATE_DRIFT` tokens), `:55` ("first cross-revision behavioral comparison") | contested (adjacent) | Behavioral-baseline drift contracts for a gate's own output (`--pin`/`--drift`, volatile-fields list) — chousa owns that; mori already has its own drift-pin line (`corpus/README.md:18`, `knowledge/drift-pin-r10.md`) and must present C2 as a *binding of the r82 classification to the raw snapshot bytes + as-of*, not as inventing snapshot baselines or drift classification. |
| tabi-shokunin | `round-16/w1/ConnPriorOutside.md:48` (`scripts/check-aria-metadata.mjs:90-96` — snapshot mismatch → exit 2 `snapshot_tampered`, classification before semantic evaluation) | contested (adjacent) | Snapshot-tamper *classification* of ARIA metadata snapshots; mori's counter grades a census classification's provenance headers, not a tamper-evidence gate. |
| kotoba-shokunin | `LOG.md:2225-2226` (R2 replay manifests frozen as sha256; "snapshot-bounded axis findings only") | contested (adjacent) | Manifest/digest freezing of replay outputs. |
| kake-shokunin | `.ufo/waves/round-30/w2/ReviewEntryHeadersDomains.md:30-33` ("Freshness: snapshot-bound (2026-10-22)", "present-tense platform fact pinned to the snapshot") | contested (adjacent) | Source-capture freshness pinning of platform facts. |
| **mori (self, prior claims — re-claim rule)** | `corpus/README.md:411` (coverage-map row "Drift baseline re-pin" → `knowledge/drift-repin-r20.md`), `:413-420` (round-21 correction: the r20 re-pin was **rejected for acceptance**, QUALITY69 supersedes 67), `:18` (`drift-pin-r10.md` behavioral pin), `:571-579` (`source-drift-r36.md` per-state classification of re-fetched source rows), `:44-48` (`source-drift-hardening-r37.md`, `source-drift-content-anchor-r38.md`); r82 classification graded at round 82 (`.ufo/waves/round-82/count-c2.py`, `corpus/evidence/drift-classification-r82.txt`) | **overlap-declared (self)** | mori must not re-claim drift classification, drift baselines, or source-capture classification as new ground — all are already claimed (and one rejected) in its own coverage map. C2's delta is strictly: the *committed raw snapshot* `drift-r82-live.txt` becomes the graded binding target via the `# Snapshot:` / `# Snapshot-sha256:` / `# As-of:` header grammar plus one live re-derivation. Phrase claims as binding-strengthening of the existing r82 classification, not a new surface. |

Net for (b): **distinct** — no sibling binds a derived token classification to a committed raw
snapshot by path + sha256 + as-of moment. The nearest practices (kasegi quote-pins, chousa
behavioral baselines, tabi tamper classes, kotoba manifest freezes) are all different
substrates and grammars; mori's own coverage map already holds the classification ground, so
the re-claim rule binds mori to "binding strengthening" language only.

### Surface (c) — line-anchored occurrence in revision bytes

| owner | evidence path:line | verdict | what mori must not claim |
|---|---|---|---|
| **chousa-shokunin** (closest holder) | `.ufo/waves/round-31/build/ConnectorSiblings31.md:18-22` (claims-JSONL `"sha256"` pins source bytes; `CLAIM_SOURCE_REVISION_MISMATCH` → `observed=stale` **before** the span check; counter target `REVISION_BINDING_MATCH=120/120`; **"Explicitly not git-revision binding."**); `build/ScribeLessonDraft/drafts.md:9-10` (`"line"` field → `CLAIM_LINE_MISMATCH` → `observed=mislocated`; counter `LINE_BINDING_MATCH=120/120`); `build/ExecC2Impl.md:25-28` (finding grammar `id=… pin=<12> actual=<12>`); `controls/ChousaR31.CriticClaimDesign31/evidence-manifest.txt:116-121` (frozen contract lines); base instrument chousa `tools/research-gate.sh verify-claims` with `at=line:N` first-occurrence semantics (`.ufo/waves/round-2/goal-wave/log-entry-draft.md:24-27`, `:59-61`) | **contested** (adjacent; chousa declares the non-overlap itself) | The claims-record **line-binding** surface (span must bind to the named line range in a *current* source file) and the claims-record **source-byte sha pin** surface. mori must never present its C3 as covering claims-JSONL line/sha records, and must not adopt `CLAIM_LINE_MISMATCH` / `CLAIM_SOURCE_REVISION_MISMATCH` names or the `LINE_BINDING_MATCH` / `REVISION_BINDING_MATCH` counter grammar. chousa's `verify-claims` remains the owner of "occurrence anywhere is not proof it is on the named line" for research claims; mori's C3 is the same *idea* applied to `git show <rev>:<path>` bytes with a `row_contains` anchor — cite chousa as sibling practice, do not absorb. |
| tabi-shokunin | `.ufo/waves/round-15/w1/AttackMissingRevision.md:21` (`git show 72dcf03:scripts/check-user-round-contract.mjs \| grep -nF "const masked = …"` → lines 429 and 859, count 2); `w1/CountReasonWitness.md:65-68` (C1 applicability counts `key=value` occurrences at a **baseline commit vs a measured commit** of the same path) | contested (adjacent) | Revision-anchored **occurrence counting** as a count witness (`check-user-round-contract.mjs` USER-round counting grammar). mori's C3 differs by requiring the value *and* the row anchor on one line (defeating the coincidental-occurrence shape tabi's count grammar deliberately does not distinguish) — but mori must not claim revision-byte occurrence checking generally; tabi has done `git show <rev>:<path>` byte checks since round 15. |
| kengaku-shokunin | `.ufo/waves/round-25/build/ConnKagi.md:16` ("Kengaku P3c/P3d … replace line/range-only assertions with frozen content tokens. Identity-sensitive tokens plus a count-preserving swap mutant are the relevant QM18 check shape") | contested (adjacent) | Content-token line anchors in registry/state checkers (P2b/P2c/P3c/P3d in `plans/state_check.py`). |
| kagi-shokunin | `.ufo/waves/round-25/build/ConnKagi.md:14-15` (kagi `round-24.md:130-137` C3 "binds `count=N sha256=…` to the actual membership and pairs fifteen swap mutants with fifteen pristine controls") | contested (adjacent) | Membership identity binding (count + digest) with swap-mutant controls. |
| tameshi-shokunin | `tools/receipt-revision-gate.py`, `tools/receipt-commit-bind.py`, `tools/anchor-drift-sweep.py`, `tools/command-binding.py` (ls-confirmed) | contested (adjacent) | Receipt→revision / receipt→commit binding craft (reusable method owner). |
| **mori (self, prior claim — re-claim rule)** | `corpus/README.md:879-883` (coverage-map row "Record revision precision (r82, S597)" → `knowledge/record-revision-precision-r82.md`); that entry's ## Boundaries: "This gate grades mori's own record and its explicitly registered bindings, never another lane's."; `knowledge/record-claim-integrity-r81.md` (r81 pinned arm, S596); `.ufo/waves/round-82/record-pins.json` (three frozen bindings) | **overlap-declared (self)** | mori must not re-claim the revision-arm ground: it is already claimed (r82) and indexed. C3's delta is the `ANCHORED_OCCURRENCE` scoping (value + `row_contains` on one line of the revision's bytes) with the `elsewhere` defeated fixture — the r82 entry itself names the coincidental-occurrence limit that C3 closes; phrase C3 as closing the recorded limit, not as new ground. |

Net for (c): **contested** at the boundary — chousa holds line-anchored occurrence for claims
records (declared "not git-revision binding"), tabi holds revision-byte occurrence counting,
tameshi holds receipt-revision binding craft; the exact intersection (row-anchored occurrence
inside `git show <rev>:<path>` bytes, with a defeated elsewhere-fixture) is unheld, so mori's
instance is distinct — but it must be claimed with named siblings, zero vocabulary overlap,
and explicit scoping to mori's own record carriers.

## Cross-cutting "must not claim" list (all three surfaces)

1. Never claim the mutation-testing *method*, fleet kill-rate ledger, or cross-lane mutation
   audit (tameshi's declared craft, `tameshi-shokunin/PROVINCE.md:3-17`; recorded at
   `tabi-shokunin/.ufo/waves/round-13/w1/SiblingOverlap.txt:33-39`).
2. Never claim fleet-first mining of arXiv:2102.11378 or pitest.org (tameshi `sources-opened.tsv:9,33`);
   mori's S595/S598 rows are tolerated W04 duplicate URLs, per the lane's own census experience.
3. Never claim claims-record line/sha binding (`CLAIM_LINE_MISMATCH`, `CLAIM_SOURCE_REVISION_MISMATCH`,
   `LINE_BINDING_MATCH`, `REVISION_BINDING_MATCH`, `verify-claims`) — chousa, round 31, "Explicitly
   not git-revision binding" (`ConnectorSiblings31.md:22`).
4. Never claim revision-byte occurrence counting generally (tabi, round 15) or
   receipt-revision binding craft (tameshi `tools/receipt-revision-gate.py`).
5. Never claim snapshot quote-pins (kasegi), behavioral gate baselines (chousa round 8),
   snapshot-tamper classification (tabi), or replay-manifest freezing (kotoba).
6. Never re-claim mori's own already-indexed ground as new growth: mutation adequacy
   (`corpus/README.md:867-871`), drift classification/re-pin (`:18`, `:411-420`), source-drift
   classification (`:44-48`, `:571-579`), record revision precision (`:879-883`). The re-claim
   rule is enforced by mori's own coverage map; all three r83 claims must read as
   *binding-strengthening / arm-completion on claimed ground*, and the coverage map must gain
   round-83 rows that point at the r80/r82 rows they extend.

## Adjacency verdict for the round record

- **(a) overlap-declared; instance distinct.** Heavy fleet practice (9 lanes hold instances);
  tameshi declared generic owner. mori's 23-mutant frozen anchored table grading its own
  counters' `--selftest` is not duplicated anywhere; no sibling mutates mori's counters and
  mori mutates no sibling gate (each lane's probes run in `/tmp`/scratch copies of its own
  bytes — same discipline as `Mo82M01Mutants.md`).
- **(b) distinct; nearest neighbors named.** Exact grammar unheld; five adjacent practices
  documented; mori's own prior classification ground must be credited (re-claim rule).
- **(c) contested boundary; exact intersection unheld.** chousa (line binding, current files),
  tabi (revision occurrence counts), kengaku/kagi (content tokens, membership binding),
  tameshi (receipt-revision craft) all border the surface; mori's row-anchored occurrence in
  revision bytes with a defeated elsewhere-fixture is its own.

## What I changed / produced

- Wrote this report only: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-83/w1/Mo83K01Conn.md`.
- No other lane, fleet, sibling, or host bytes were written. Scratch
  `/fast/scratch/hyaku/mori-r83/Mo83K01Conn` created and deleted (one shell command).

## Commands run (decisive subset, all read-only)

- `grep` (harness tool) over `/home/vgpnk/Projects/shokunin/*-shokunin` and per-lane batches for:
  `mutant|mutation|survivors=|killed=`; `mutation testing|mutant|mutation adequacy|mutation-post`;
  `Snapshot-sha256|Snapshot:|As-of:|DRIFT_CLASS|snapshot=bound|snapshot-bound|as-of moment`;
  `Snapshot-sha256|Snapshot:|run-start:`; `REVISION_MISMATCH|ANCHORED_OCCURRENCE|row_contains|rev-bytes|contains_value`;
  `verify-claims|CLAIM_LINE_MISMATCH|REVISION_BINDING_MATCH|LINE_BINDING_MATCH`;
  `mutation testing|mutants killed|kill-rate|mutate-and-run|mutation adequacy|mutation table|surviving mutant`.
  First batch returned "No matches" because the tool does not expand a bare `*` directory glob;
  re-issued with explicit `;`-separated lane paths (verified against mori itself as a positive
  control before trusting any negative result).
- `read` of the frozen contract, controls, counters, r82 probe, r82 spotcheck, tameshi
  PROVINCE.md, mori PROVINCE.md, mori coverage-map rows, and the mori r80/r81/r82/r83
  knowledge entries named above.
- One `bash` command: `ls` of `tameshi-shokunin/tools/` + `git log -1` of `kumitate-shokinin`
  and `kumitate-shokunin` (characterization only); scratch removed in the same command.
- No counters were executed; no lane gates were run (read-only seat).

## Verified / not verified

Verified: tameshi's generic craft ownership (PROVINCE + tools + knowledge inventory);
revenger/kengaku/game-dev-2d/game-dev-3d/audio/chousa/kasegi/tabi/kagi instance evidence with
path:line; zero sibling hits for the mori snapshot-header grammar; chousa's round-31 binding
surface and its explicit not-git-revision declaration; mori's own coverage-map rows for all
three grounds (re-claim rule satisfied by citing them); tameshi's duplicate URLs for mori's
r80/r83 sources.

Not verified: (i) lanes could hold surface (b) or (c) under vocabulary my token set missed —
the scans covered mori's grammar plus generic terms (`snapshot-bound`, `as-of`, `verify-claims`,
`git show`), but a sibling with wholly original naming would escape; (ii) kotodama, lore, mado,
souji, tsukuroi, kaidoku, kake, kama, kumitate-shokunin showed no instrument hits for the
narrow mutation-instrument pattern — their broad `mutant` hits were dispatch role names or
process-kill flags, but I did not exhaustively page every hit file; (iii) no execution of any
sibling counter or gate (out of scope for a read-only connector seat).

## Defects / observations in other seats' bytes (file:line)

1. **Already-self-corrected (not new):** `tameshi-shokunin/PROVINCE.md` round-16 append's line
   anchors `:85-91` and the round-1 anchor `:84-89` are stale against current
   `tools/mutate-and-run.sh` bytes (legs sit at `:88-94`/`:88-93`); tameshi's own round-72 append
   records the correction append-only and pins the measured spans via
   `tools/pointer-recheck.json` (`province-r72-*` rows). Cited here only so mori does not
   propagate the stale ranges.
2. **Fleet-root hygiene observation (not a lane defect, no write attempted):** a second
   kumitate worktree exists at `/home/vgpnk/Projects/shokunin/kumitate-shokinin` (misspelled,
   no `-shokunin` suffix), a clone of `https://github.com/VeigaPunk/shokunin.git` at tip
   `e140a9bf` ("round-80: kumitate dispatch evidence (hyaku inline attempt 1)", 2026-11-04
   05:35:38 -0300), beside the canonical `kumitate-shokunin` at `c6a7ebd3` ("round-80: freeze",
   05:41:58). Any sibling scan globbing `*-shokunin` silently misses it. Report-only; fleet
   root is unwritable to this seat.
3. **For mori's own integrator:** mori's coverage map (`corpus/README.md`) ends its round
   section indexing at round 82 (`:879-883`); the r83 knowledge entry
   `counter-mutation-adequacy-r83.md` exists but has no coverage-map row yet — the L1 should
   add round-83 rows pointing at the r80/r82 rows they extend (re-claim rule enforcement),
   if the integration contract requires map rows this round.
