author: mori L1 MoriR60 (round 60, hyaku run-11, in-session)
date: 2026-10-28
round: 60
entering: ddfb12fb0838b4307c445194a844f0c4b1950195
freeze: ac496c7cde8cad965079858accae3bedfe4a73f2 (amendments 1-2 pre-data, recorded in contract.md)

# Round 60 — instrument hardening (C1 calibration, C2 depth, C3 operability)

Fresh-start round: the rejected closures of rounds 57–59 and their verifier
spot-checks were read before declaring claims; every claim names a surface a
do-nothing control cannot reach, with control receipts committed pre-data
(`.ufo/waves/round-60/evidence/control-c{1,2,3}-do-nothing.txt`, scored at
the entering revision `ddfb12fb…`).

## Gate

- Candidates considered: the three declared claims (C1 record-receipt
  integrity, C2 hardened entry-claims verifier, C3 counter execution
  boundary); the shokuknow `merge/mori` package (136 rows / 80 entries —
  no theme matches instrument hardening this round); the considerthese
  2026-10-26 absolute-host-path item.
- Admitted (sources opened this round):
  - S561 — Mo59Critic22 report (own-work A): the four met-flip defect
    classes D1–D5; opened at `.ufo/waves/round-59/w1/Mo59Critic22.md`
    §Counterexample (2026-10-28): "K1–K10 identical (…:offset:3; …)"
    — the identical-span construction the old grammar scored `met`.
  - S562 — Mo59Sentinel57 report (own-work A): execution/write boundary;
    opened §F1 (2026-10-28): "the unpinned blob ran" while
    `failed=tool_sha` — pin-as-bookkeeping, not as an execution gate.
  - S563 — Mo59Critic25 report (own-work B): drift-arm attribution;
    opened §Decisive mutants (2026-10-28): "A nonzero exit on this file
    is attributable to any subset" — the confound the H5 control kills.
- Rejected:
  - S564 — Mo59Sentinel58 report: REJECTED as a same-scope duplicate of
    S562 (same F1 execution-gate finding; this round used none of its
    constructions); flip: a future round needing its distinct F2
    expect-tamper construction re-opens the row. Kept as the taste record.
- Registry sweep (QUALITY 155): `grep -c 'Mo59Critic22\|Mo59Sentinel57\|Mo59Critic25\|Mo59Sentinel58' corpus/SOURCES.md`
  → 0 before the append; the four names appeared in no earlier row, so
  S561–S564 are fresh own-work rows, not reconciliations.
- Spot-check: pending — filed for the round-60 non-author closure
  (≥1 admit: S561; ≥1 reject: S564).

## Round-59 absent-set correction (supersedes round-59)

This section supersedes round-59's absent-at-filing record (routed defect 3
of `corpus/lessons/round-59-verifier-spotcheck.md`). Truth by
`git cat-file -e` (full table: `.ufo/waves/round-60/evidence/r59-absent-set.md`):

- Mo59Critic29 — supersedes the round-59 lesson claim of absent-at-filing:
  committed pre-filing in `bf6c0ad3` (2026-10-28 03:12:38 -03); the record
  set of the wave completes at `f091bd77`. The lesson's set was wrong, the
  report's missing set did not name it — consistent.
- Mo59Reviewer16 — supersedes the round-59 lesson claim of absent-at-filing:
  committed pre-filing in `bf6c0ad3`; the record set completes at
  `f091bd77`.
- Mo59MutationTester32 — added `bf6c0ad3` (pre-filing), modified post-filing
  in `f091bd77`; the report's "missing" listed it because its modified bytes
  were uncommitted at filing.
- Mo59Executor40 — late: landed post-filing in `f091bd77` (07:42:42 -03).
- Mo59MutationTester31 — late: landed post-filing in `f091bd77`.
- `.ufo/waves/round-59/w1-results.json` — landed post-filing in `f091bd77`
  (the WAVE-DONE handoff arrived after the round commit; see Mistakes row 2).

Reading note (fixed here so both readings of the frozen C1 sentence hold on
the same bytes): `f091bd77` is the commit at which the round-59 wave RECORD
SET is complete — every one of the five names is covered by it, directly
(two files) or as the completing commit of a record whose earlier bytes
landed in `bf6c0ad3` (three files). The count-c1 lesson arm reads the
pointer file-globally; the per-name lines above now carry it distributively
as well (Mo60Reviewer03, this round's wave).

## Mistakes

1. class reference-drift · evidence: r59 report + `SCORECARD.md` (r59
   section, lines 2950–2951 at entering `ddfb12fb…`) cited
   `.ufo/waves/round-59/evidence/c1-entering.txt` and `c2-entering.txt`;
   no file was ever committed under those names — the receipts live at
   `control-c1-do-nothing.txt` / `control-c2-do-nothing.txt` (commit
   archaeology: Mo60Revenger96, this round's wave) · captured-by: none —
   no pointer-existence check ran before filing · fix: the r60-correction:
   re-pointing in SCORECARD (this round), the count-c1 DEAD-NAME ARM (a
   committed counter that scores uncorrected dead names unmet), and QUALITY
   criterion 156 (pointer-existence sweep before filing).
2. class landing · evidence: `f091bd77` committed `w1-results.json` and the
   late seat files at 07:42:42, after the r59 report was filed (07:41); the
   round committed before the wave's final handoff was swept · captured-by:
   none — no post-WAVE-DONE tree sweep before the report commit · fix: the
   round-60 procedure commits the round only after WAVE-DONE plus one
   explicit `git status --porcelain` sweep of the wave dir; recorded here
   so the non-author closure can check it (this round's own commits obey
   it).

## Wave w1

One v2 wave, 64 seats dispatched, 64 settled, zero empty outputs, zero
duplicates (`SETTLEMENT_SCAN_OK`, mori-settlement-scan over
`w1-results.json`). Role mix: reviewer 16, critic 8, mutation-tester 5,
sentinel 3, executor 12, scribe 6, scout 4, connector 2, revenger 4,
simplifier 4 — attack share 32/64 = 50%; L1 held the §3 planner seat; no
residual call. Dispatch `76904b21`, results `.ufo/waves/round-60/w1-results.json`,
64 seat reports under `w1/`. Dispatch-payload defect (recorded): the seats
received the `/skill:godspeed` leading line but not the verbatim directive
bytes (this round's spec builder relied on renderer injection that did not
happen; r59's builder embedded them) — builder fixed for future waves.

Per-claim verdicts from the wave (all receipts at named revisions):

- **C1 (calibration) — VERIFIED met, limits disclosed.** Re-derived
  byte-identical at the data revision by Mo60Reviewer03 (twice) and the
  receipt arms re-verified by Mo60Reviewer09 (2/2 byte-equal, rc 0);
  do-nothing control replayed byte-for-byte (Mo60Reviewer14/15); absent-set
  lies caught in the operative row (Mo60Critic26); dead-name constructions
  counted (Mo60Critic27); receipt relabeling caught (`bytes_differ`,
  Mo60Critic25). Routed limits: the lesson-arm pointer reading is
  file-global (fixed truthfully in the correction lines), the marker arm is
  existential not universal (clone-demonstrated, zero rogue lines on real
  bytes), and MutationTester33's M4 shows the lesson arm has a selftest
  blind spot.
- **C2 (depth) — measured met, instrument DECERTIFIED; unverified; no score
  claim.** The real entry verifies with no false negative
  (Mo60Reviewer04; benign mutations hold) and 5/5 predicate mutants die
  (Mo60MutationTester31), but Mo60Critic21 built a zero-evidential entry
  (nested-varying spans at offset 2/3, distinct filler texts) scoring
  `ok=true` and `C2=met` on a sandbox commit, and Mo60Critic22 found two
  further bypass classes (orphan claim-shaped lines silently skipped;
  claim text uninspected). Same class that decertified r59's C2: shape
  predicates cannot certify content. Honest stop.
- **C3 (operability) — measured met, instrument DECERTIFIED; unverified; no
  score claim.** Mo60Reviewer13 demonstrated the exact frozen `C3=met` line
  on a scratch clone whose count-c1 sha ≠ PIN_C1 (`met=True,
  failed=['count_c1_sha']` — the pin is checked but does not compose the
  verdict) and `containment=ok` beside `failed=g2_escape_written`;
  Mo60Sentinel41 falsified the contract's "count-c1 executes no
  repo-supplied tool blob" sentence (it executes four: two r59 counters,
  two tools — revision-pinned, but the pin is not an execution gate under a
  hostile `--repo`). The boundary gates themselves are real and necessary
  (Mo60MutationTester34: marker clause necessary; Mo60Sentinel42: all real
  escape classes refused) — the verdict composition is what fails.
- Aggregate (Mo60Critic28): no committed revision prints all three counters
  met without the claimed work — the do-nothing arms hold.

Spot-check material for the non-author closure: ≥1 admit (S561) and ≥1
reject (S564) are recorded above; the closure re-opens at least one.

## Wave-found instrument defects (routed; frozen bytes stand)

Recorded as seats reported them (evidence in the named w1 reports). The kill
rule froze the counters once seats scored, so these are routed to round 61,
not patched:

1. count-c3 verdict composition (Mo60Reviewer13 HIGH 1+2, Mo60Reviewer02 F1):
   `toolgate/containment/expectgate` output tokens derive from failed-list
   literals that are never appended, so they read "not skipped"; `met`
   omits the count-c1 pin checks — demonstrated: a scratch clone with
   count-c1 sha `f5ed5dd7…` ≠ PIN_C1 prints the exact frozen
   `C3=met toolgate=ok containment=ok expectgate=ok cases=6` line (direct
   measure: `met=True, failed=['count_c1_sha']`), and a pre-seeded
   `<scratch>/escape.txt` prints `containment=ok` with
   `failed=g2_escape_written`. On the real pinned revisions the checks all
   pass honestly, but the instrument cannot certify hostile input — the
   same class that decertified r59's C2.
2. count-c1 lesson-arm reading (Mo60Reviewer03): the pointer check is
   file-global; under a distributive reading of the contract sentence the
   tip scores 3/5. Fixed truthfully in the correction lines above (each
   name now carries `f091bd77` as the record-completing commit), so both
   readings hold on the same bytes; the counter itself is frozen.
3. count-c1 marker arm is existential, not universal (Mo60Reviewer03): a
   rogue marker line citing a dead name without its real pointer still
   scores met (clone-demonstrated; the real tip carries zero rogue lines).
4. count-c3 F2/F3 (Mo60Reviewer02): the G2 symlink arm uses a dangling
   in-root symlink (proves no-symlink-parent; the real escape is also
   refused), and the `tool_absent`/`tool_sha` failed-token match also
   matches the `scan_tool_*` variants.
5. Hygiene: a transient untracked `EXEC-MARKER` appeared at the lane root
   (~13:16–13:18) while a seat ran the old-counter PoC without `--scratch`
   (the r59 counter's scan arm invokes the blob with cwd = lane root) —
   cleaned by the seat; lane commits use explicit pathspecs, so no sweep
   risk materialized. This is Sentinel57's hole live: the old counter lets
   the blob write to the invoker's cwd.
