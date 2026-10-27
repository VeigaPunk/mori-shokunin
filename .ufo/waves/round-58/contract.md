# mori round 58 — frozen contract (claims, predicates, kill rules, controls)

Frozen by L1 MoriR58 before any seat scores. Entering branch revision:
`b783d0b892637ce8d20f188cad20e4d8913ca635` (lane `master` tip; `jj-lane.sh state`
local=remote). All counting commands run from the lane repo working tree.

Round-57 verifier spot-check routed defects this round must fix
(`corpus/lessons/round-57-verifier-spotcheck.md` ## Routed defects for round 58):
1. frozen-counter target identity — bind to the ACTIVE register table, not the
   first `## Capabilities` heading;
2. counter false-green constructions — resolve evidence pointers
   (`git cat-file -e`) and bind quotes against a pinned byte-identical copy;
3. byte-faithful quotes (observation).

No scalar score change is claimed on either axis. No axis-harm claim is made;
a no-harm reviewer seat is in the wave.

## C1 — calibration (score 5, tied lowest non-retired)

Claim: the lane lands a frozen counter `.ufo/waves/round-58/count-c1.py` that
VERIFIES the two round-56 admitted capabilities are recorded in the ACTIVE
capabilities register — the section whose preamble self-describes as "the
lane's current capabilities register" (`SCORECARD.md:1953`, the round-35
register; NOT the superseded `— none yet —` stub at `SCORECARD.md:596`) —
with (a) table-identity binding proven against the freeze revision, (b) every
evidence pointer in the two rows resolved via `git cat-file -e R:<path>`, and
(c) each row's key bound to fleet `MANIFEST.json` `rounds[832].capabilities_added[j]`.

- Counting command: `python3 .ufo/waves/round-58/count-c1.py R`
- Frozen target output (after): `C1=met rows=2 pointers=ok manifest=ok binding=ok selftest=ok rev=R`, exit 0.
- Before (control): at entering `b783d0b8…`, `git cat-file -e b783d0b8…:.ufo/waves/round-58/count-c1.py` fails — the counter does not exist; and the round-57 counter on the same bytes prints `C1=unmet rows=0 evidence=bad`, exit 1 (known wrong-table false-negative, preserved as contrast at the landed tip).
- Do-nothing control (§9): a fixture register whose two rows name a nonexistent evidence path MUST score `C1=unmet … failed=pointers`, exit 1; a fixture whose only `## Capabilities` table is the stub MUST score `binding=bad`, exit 1. If either scores met, the counter is broken and no data is collected.
- Kill rule: any post-freeze change to the counter bytes, the predicate sentence, or the target output invalidates the claim.
- Selftest: `python3 .ufo/waves/round-58/count-c1.py --selftest` builds isolated throwaway git fixtures and asserts pass/fail per arm; `C1_SELFTEST pass=N fail=0`, exit 0.

## C2 — depth (score 5, tied lowest non-retired)

Claim: the lane lands a frozen counter `.ufo/waves/round-58/count-c2.py` and a
new source-grounded depth entry `corpus/knowledge/driver-events-r58.md` carrying
≥8 located claims on the event-class semantics of the round-56 driver-liveness
parser (`launch` / `complete` / `lane-dead-no-report` / `launch-fail` / `wrap`),
where every located quote is verified as a substring of a pinned source copy
whose sha256 equals the sha256 of `tools/mori-driver-liveness.py` at the
measured revision.

- Counting command: `python3 .ufo/waves/round-58/count-c2.py R`
- Frozen target output (after): `C2=met claims=N located=N copy=ok tree=ok rows=ok sources=ok rev=R` (N ≥ 8), exit 0.
- Before (control): at entering `b783d0b8…`, the entry, the pinned copy and the counter do not exist → `C2=unmet entry=absent`, exit 1.
- Do-nothing / junk controls (§9): (a) an entry whose quotes are NOT substrings of the pinned copy MUST score `C2=unmet … failed=quotes`; (b) a pinned copy whose sha256 differs from the tool at R MUST score `copy=bad`; (c) frontmatter missing `source:`/`verified-at:`/`recheck:`/`coverage-map:` MUST score `sources=bad`. Any control scoring met invalidates the counter.
- Sourced-claim rule (§2b): the entry cites registry row S550 (opened this round; own-work pinned copy of `tools/mori-driver-liveness.py`, byte-faithful Gate quote), and S550's `used-by` names the entry.
- Kill rule: same as C1 — frozen bytes/predicate/target.
- Selftest: `python3 .ufo/waves/round-58/count-c2.py --selftest` → `C2_SELFTEST pass=N fail=0`, exit 0.

## Round shape

One v2 wave `w1`, 64 seats, policy v2 (band 64–128). Attack share ≥ 25%
(reviewer+critic+mutation-tester+sentinel). §3 planner seat is held by the L1;
a bounded planning data-walk rides the connector seats (orchestrator ruling
2026-10-19: `planner` is not a swarm role).

## Assimilation / quarantine / considerthese

- Assimilation: none expected (say `Assimilation: none` unless a seat finds a fit).
- Quarantine slice: 3 rows (S244, S262, S268) — re-derive at round time; hand-check verdicts land in the lesson.
- considerthese: at most one still-unimplemented proposal from `considerthese/2026-10-26.md`; suggestion 1 (env/stale pin-check split) is ALREADY implemented in `tools/mori-pin-check.py:140-150` — land the status as a lesson/criterion note, not a claim.

## Census

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
at round start (322 rows, exit 0) and round end (exit 0 required; S550 expected → 323 rows).
