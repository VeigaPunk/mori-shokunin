# mori round 59 — frozen contract (claims, predicates, kill rules, controls)

Frozen by L1 MoriR59a2 (attempt 2) before any seat scores. Entering branch
revision: `2b9f03975bfb6e508f35074ac8181ec8bf54e805` (lane `master` tip;
`jj-lane.sh state` local=remote). All counting commands run read-only from the
lane repo working tree. Attempt-1 leftovers (`count-c1.py`, `count-c2.py`
drafted 2026-10-27, selftest 21/24, never frozen or dispatched) were discarded
and replaced; they are not evidence.

Round-58 verifier spot-check routed defects this round must fix
(`corpus/lessons/round-58-verifier-spotcheck.md` ## Routed defects for
round 59):
1. SHONEN assessment bound to the wrong lane — re-file against
   `mori-shokunin/SHONEN.md` in the report.
2. Duplicate source row S552 — appended reconciliation + `## Mistakes` row +
   QUALITY criterion (grep registry for DOI/sha before a new row).
3. C1 target/predicate identity — frozen C1 whose every required output token
   is emitted by the counting command; exact row keys, pointer roots,
   emptiness, duplicate keys, revision-pinned MANIFEST binding,
   active-section binding all proven against W1's constructions.
4. C2 predicates — frontmatter required (fails a frontmatter-less body),
   distinct claims, designated quote spans, exact `used-by` match, no extra
   columns; explicit scratch-path CLI on every new counter.

No scalar score change is claimed on either axis. No axis-harm claim is made;
a no-harm reviewer seat is in the wave.

## C1 — calibration (score 5, tied lowest non-retired)

Claim: the lane lands a capability `tools/mori-register-check.py` at frozen
sha256 `02feb852…954f7b` — the active capabilities-register checker that
VERIFIES the two round-56 admitted capabilities in the ACTIVE register
(the unique `## Capabilities` section self-declaring "current capabilities
register", `SCORECARD.md:1951-1953`; NOT the superseded `— none yet —` stub) —
with (a) unique-register identity, (b) exact key/name/pointer binding, and
(c) MANIFEST `rounds[832]` binding at revision-pinned fleet commit
`2807c6ab8a9b04dcf256682bcd722c695fdd6e14`; plus a frozen counter
`.ufo/waves/round-59/count-c1.py` that emits its own target.

- Counting command: `python3 .ufo/waves/round-59/count-c1.py R [--scratch DIR]`
- Frozen target output (after): `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=R`, exit 0.
- Before (do-nothing control, §9): at entering `2b9f0397` the tool does not
  exist → `C1=unmet … failed=tool_absent`, exit 1. The two register rows
  pre-exist since round 57; the C1 do-nothing arm is met-proof through the
  tool/fixture/pointer arms, not through row absence.
- Hostile fixtures (§9, 13 committed trees under
  `.ufo/waves/round-59/fixtures-c1/`): stub-only and double-declared
  registers, duplicate and missing keys, missing/absolute/parent-relative
  pointers, empty pointer cell, altered name, substring-only name, foreign
  lane, wrong index, lane_round mismatch — each MUST score UNMET covering its
  frozen expect prefix. Any scoring met invalidates the counter.
- Kill rule: any post-freeze change to counter bytes, contract bytes, the
  predicate sentence or the target output invalidates the claim.
- Selftest: `count-c1.py --selftest` → `C1_SELFTEST pass=6 fail=0`, exit 0.

## C2 — depth (score 5, tied lowest non-retired)

Claim: the lane lands a capability `tools/mori-settlement-scan.py` at frozen
sha256 `4c04bf21…5ac9a9` (validates orchestrator `*-results.json` settlement
artifacts: object/seats==members/member key-set/name-unique/role enum,
verdict SETTLEMENT_SCAN_OK / FAIL) AND a new sourced depth entry
`corpus/knowledge/wave-settlement-artifacts-r59.md` carrying ≥10 byte-exact
pin-bound claims (`Quote: \`<q>\` (<copy>:line:<n>|offset:<n>; pin <sha64>)`)
over ≥3 distinct artifacts pinned in `corpus/evidence/sources-r59/` — each
copy byte-equal to its named `.ufo` artifact at R — plus the registry rows
those claims cite (status mined, `used-by` exactly the entry).

- Counting command: `python3 .ufo/waves/round-59/count-c2.py R [--scratch DIR]`
- Frozen target output (after): `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=N files=F rev=R` (N ≥ 10, F ≥ 3), exit 0.
- Before (do-nothing control): at entering `2b9f0397` the tool, entry, copies
  and rows do not exist → `C2=unmet … failed=tool_absent`, exit 1.
- Hostile trees (§9, 12 committed trees under `.ufo/waves/round-59/trees-c2/`):
  no frontmatter, duplicate K, wrong-line quote, stale pin, <10 claims,
  outside-file claim, missing/queued/extra-cell/wrong-used-by rows,
  sub-minimum quote, malformed claim line — each MUST evaluate UNMET covering
  its frozen expect prefix. Any met invalidates the counter.
- Scan arm: the five r54–r58 wave-results files MUST scan OK with
  members==seats; the r53 file MUST scan FAIL (`report_file` extra keys —
  schema drift, reported not fixed).
- Sourced-claim rule (§2b): the entry cites only S### rows opened this round
  (one per cited artifact copy; a ≥1 admit / ≥1 reject Gate pair lands in the
  round-59 lesson), satisfying the frontier sourced-claim requirement.
- Kill rule: same as C1 — frozen bytes/predicate/target.
- Selftest: `count-c2.py --selftest` → `C2_SELFTEST pass=9 fail=0`, exit 0.

## Round shape

One v2 wave `w1`, 64 seats, policy v2 (band 64–128). Attack share ≥ 25%
(reviewer+critic+mutation-tester+sentinel). §3 planner seat is held by the L1;
bounded planning data-walks ride connector items (`planner` is not a
validator role — orchestrator ruling 2026-10-19).

## Assimilation / quarantine / considerthese

- Assimilation: none expected (`Assimilation: none` unless a seat finds a fit).
- Quarantine slice: re-derive the mori absent-defect-register rows at round
  time; hand-check verdicts land in the lesson.
- considerthese: at most one still-unimplemented proposal from
  `considerthese/2026-10-26.md`.

## Census

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
at round start and round end (exit 0 required at end; new S rows for the
C2 artifacts raise the row count).
