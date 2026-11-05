# Round 91 — mori (L1 MoriR91, attempt 1) — lesson

Entering revision `79eaa8cfe5e0b9b1c5ff45f524199d4a123f0520`. Frozen contract
`.ufo/waves/round-91/contract.md` (committed at `e02b8a39`, before any wave output). One v1 wave,
`w1`, 12 seats; five seats returned no output (see Mistake 4). Honest stop: neither claim was
measured, so neither lands a score move.

## Claims and their verdicts

- **C1 calibration — the round-87 receipt gate's unarmed clause families get selftest arms and
  independent mutants killed with attribution.** Not measured. Its populations P1
  (`Mo91E01Arms`) and P2 (`Mo91M01Mut`) are absent: both seats returned empty. The counter
  candidate `w1/candidates/count-c1.py` (`Mo91E03C1Ctr`) was run at the entering revision with
  the frozen P2 absent; it exits 2 (setup), which is the frozen behaviour for an absent population.
  Attack findings on the frozen predicate are in Mistake 3.
- **C2 freshness — a dated census snapshot of the round-86 value channel.** Not measured. The
  snapshot and counter seat `Mo91E02Snap` returned empty; `git show 79eaa8cf:corpus/evidence/value-census-2026-11-05.txt`
  does not exist, so the do-nothing reading is `snapshot=absent`, as the contract requires.
- **Carried, not claimed:** operability (nonce guard for the round-90 gate), depth (supersession
  record for the round-87 arm pins). The pins map is in `w1/candidates/pins.txt`; it is the input
  to the supersession record and was not written as one this round.

## What the round did

- Mined mistake R8 and fixed its detection: `tools/mori-source-digest.py` (sha256
  `a692b159646e8979f9fc95d5eee82a9a30cee4d8f67432ee824fff7e9d30cee7`, a copy of the seat's
  `digest-check.py`). Real run at the entering registry: `DIGEST_CHECK rows=121 ok=87 mismatch=2
  prefix_only=31 unpinned=1`. Able-to-fail: one hex character flipped in S490's recorded digest
  gives `DIGEST S490 mismatch` and `mismatch=3`, exit 1 (seat `Mo91E04Digest` §Able-to-fail).
- Found a second defect of the same class, S235 (`Mo91Sc02Lesson` sweep), and five full-length
  digests that disagree with a committed copy named by id (S156, S158, S159, S235, S615).
- Opened two sources (`Mo91Sc01Src`); re-opened S617 myself on 2026-11-05: sha256 of the PDF
  `056ac9b9…83edff342` matches, `grep -c -F` of the located opening = 1. S617 admitted (`mined`);
  S618 rejected with reason and flip.
- Two attacks on the frozen predicates (`Mo91R01Atk`, `Mo91R02Atk`): forgers accepted by the frozen
  wording, listed in Mistake 3.
- Scout map of the frozen receipts that pin the round-87 arm count (`Mo91S01Pins`).

## Mistakes

| Class | Evidence pointer | Captured-by | Fix, and what makes it able to fail |
|---|---|---|---|
| `recorded-digest-unverified` — a registry row's full 64-hex digest is never compared with the pinned copy it names; a 16-character agreement passes unchecked | R8: `corpus/SOURCES.md` S615 recorded `7891c58897fe9f78…8b1f8a60ad1a6f0`; pinned `.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html` = `7891c58897fe9f78…94b0f83b9a8a42f5`. Second instance: S235 recorded `9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30cda99359e6df057ad8020`, pinned `corpus/evidence/sources-r42/S235.pdf` = `…a30dca99…`. | none — `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` reads no digest and no pinned copy (seat `Mo91Sc02Lesson` §1; `grep -c -E 'sha256|digest'` on the committed census = 0 hits in validation logic) | `tools/mori-source-digest.py`. Shown able to fail: the S490 flip above exits 1 and names the row. Not yet a gate: it is not wired into the census. |
| `correction-held-append-only` — the two wrong digests are recorded in admitted rows; the registry rule forbids in-place rewrite of a row's digest, so the correction has no home yet | `corpus/SOURCES.md` S615 and S235 rows; `CORPUS.md` rule 2 | none | Correction of record below. A row-level correction needs an appended supersession row (CORPUS rule 2); not written this round. |
| `frozen-family-label-mismatch` — the frozen C1 kill rule names families by prefix (`c2-supersede`), but the subject's own FAIL labels are `supersede_*`, `absent_*`; the rule as written makes an honest arm for the supersede family read `isolated` | fixture run in `Mo91E03C1Ctr` report: `MUTANT p1 p1-c2-supersede c2-supersede isolated rc=1 labels=supersede_absent_target,supersede_requires_clean`; `.ufo/waves/round-87/count-c2.py` label strings | none — the contract was frozen by a lane L1 that did not read the subject's label strings | Not repaired: C1 is not measured this round. The mapping (family → label prefix) must be frozen in the contract before data in round 92. Shown able to fail: the fixture reads `isolated=1`. |
| `attack-found-forgers-in-frozen-predicates` — C1 accepts 3 of 4 forgers and C2 accepts 6 of 10 forgers as the contract is worded; the do-nothing control could not reveal any of them | `Mo91R01Atk` §Forgers (C1 `ATTACK C1 forger-accepted=3 rejected=1`); `Mo91R02Atk` §Forgers (C2 `ATTACK C2 forger-accepted=6 rejected=4`; F0 self-asserted date, F2 forged vintage line, F5/F5b raw inputs not byte-exact, F6 invented token line) | none — a do-nothing control grades behaviour at the entering revision, never the wording's reach | Round 92 must amend the contract **before** its controls commit (disclosed as pre-data amendment): C1 — counts re-derived from executions at R, FAIL labels only from arms that fail when behaviour changes, `pristine=0 unanchored=0` printed; C2 — raw-input sha256 manifest committed and recomputed, token-set closure, `unclassified` counts re-derived tokens with no snapshot line, date tied to the snapshot's committed date. A text-only rule proves nothing about capture time; that residual is named. |
| `wave-seat-silent-death` — five of twelve seats (`Mo91E01Arms`, `Mo91E02Snap`, `Mo91M01Mut`, `Mo91K01Conn`, `Mo91C01Ctl`) settled with empty output and null status/note; no error text reaches the wave record | `w1-results.json` (entries with `"output": ""`, `"note": null`); `w1/swarm-registry.json` (`agentId: null` for every spawn member); dispatch at `02:17:33` per `w1.ready.dispatched` | none — the registry records no agent ids and the results file carries no failure reason | Dead seats stay dead (not replaced); recorded here and in the report; the operator is asked for the failure cause via `.ufo/l0-questions.md`. Fix belongs to the wave tooling: results must carry a spawn or stop reason per seat. |

## Corrections of record (append-only; registry rows unchanged)

- **C-1 (round-90 defect R8).** The S615 row's recorded digest `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b8f1a60ad1a6f0`
  is not the full sha256 of its pinned copy. The full value, measured by `tools/mori-source-digest.py`
  on `.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html`, is
  `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5`.
- **C-2 (new).** S235 recorded `9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30cda99359e6df057ad8020`;
  measured full sha256 of `corpus/evidence/sources-r42/S235.pdf` is
  `9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020`.
- **C-3 (unresolved).** S156, S158 and S159 record full digests that match no committed copy named
  by their own id; their cells may cite a different artifact. Not classified as defects this round.

## Gate (sources, protocol §2b)

| Row | URL | Located quote (≤25 words) | Access | Decision |
|---|---|---|---|---|
| S617 | https://web.eecs.umich.edu/~weimerw/2022-481F/readings/mutation-testing.pdf (Jia & Harman, TSE 2011) | "Mutation Testing is a fault-based testing technique which provides a testing criterion called the" (14 words) | 2026-11-05; sha256 `056ac9b9…83edff342`; `grep -c -F` = 1 | admit — grounds the knowledge entry `corpus/knowledge/calibration-arming-r91.md` |
| S618 | https://sre.google/sre-book/monitoring-distributed-systems/ | "Observational experiments conducted over a very long time horizon (months or years) with a low sampling rate (hours or days)" (20 words) | 2026-11-05; sha256 `3117d94a…c4c2a75`; `grep -c -F` = 1 | reject — sampling cadence, not a dated-snapshot or drift practice; flip recorded in its row |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` before this
round: 389 rows, exit 0; after: 391 rows (S617 `mined`, S618 `rejected`), see the report.

## Assimilation and considerthese

`Assimilation: none` — the round's two claims were not admitted and no `merge/mori/` theme was
assimilated. `considerthese/`: no proposal mined this round; the seat budget went to the claims and
the mistake sweep. Carried to round 92.
