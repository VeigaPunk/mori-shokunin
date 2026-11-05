# Round 95 frozen contract — mori (L1 MoriR95, attempt 1)

Entering `754f4991198c16ddd1d4a3ea9206cfb7d74d6827` (lane `master`, = origin). Fixture base `84b152308fa6c2f224ad75dff68e525dab9057ac`
(the round-94 base); admission reference `7b3fe9d540c98b8b0390a0f9bbe78de4341092a5` (round-94 entering).
Freeze: this commit, before any wave output. Frozen artifacts: `count-c1.py` (C1), `count-c2.sh` (C2), this contract,
and the before receipts in `evidence/`. No seat edits any of them; the wave scores them as committed.

Axes (SCORECARD): **calibration** 5 (C1, tied lowest non-retired with depth 5 and freshness 5) and **operability** 7
(C2, a capability acquisition; no score move is claimed). Trend targets: discernment (C1), quality (C2 as a runnable check).

Planner: the L1 holds the §3 planner seat by disclosure (the validator refuses `planner`; L0 question D1 round-93/94 is open
and operator-owned). The frozen predicates below were written by the L1 before any wave seat ran.

## Claim C1 — calibration: the round-94 admission battery's self-claimed coverage matches its kills

Self-assessment under test (round-94 lesson, `corpus/lessons/round-94.md` C1): the frozen battery shows the admission check
is a whole-token test. Observed gap (round-94 mutation probe `.ufo/waves/round-94/w1/Mo94M01Mut.md`): four non-equivalent
mutants of the same counter (m2 length clause, m3 census gate, m4 trio floor, m6 patched12 gate) pass the frozen battery.
Calibration = the count of mutants on which the battery's self-report (`met` as the counter's kill claim) disagrees with
observed behaviour.

Predicate P-C1r95 (same sentence in `count-c1.py` docstring and the receipt): running
`python3 -I .ufo/waves/round-95/count-c1.py <rev> --lane <lane> --census <census>` prints `C1=met survivors=0 killed=7/7`
and exits 0 iff the pristine counter (sha256 `6eb7fa4c…`, round-94 `count-c1v2.py`) is green on BASE, every pristine fixture
has its declared verdict, and every one of the seven mutants m1, m1b, m2, m3, m4, m6, m7 is killed by at least one fixture.
Fixtures: R94-L/R/M (round-94 embedded-hash fixtures, unchanged), R95-LEN (5-char admission prefix), R95-CEN (census
stub failing), R95-TRIO (one `recheck:` line removed from `boot-anchor-win-r73.md`), R95-PAT (one body line appended to
`counter-win-r77.md`, `verified-at` untouched).

- Before (round-94 battery only, the same run): `before_r94_survivors` — expected to name m2, m3, m4, m6 (round-94 probe).
- Do-nothing control: the round-94 battery reaches `survivors=4`, so do-nothing does not meet the claim.
- Equivalent mutant m5 (`adm_ok != 19` → `adm_ok < 1`) is declared, not scored: `adm_ok + adm_fail = 19` on every input
  (one increment per NINETEEN file), so the two conditions agree on every reachable pair. Listed, never counted as killed.
- Kill rule: a mutant is killed iff its verdict on some fixture differs from the pristine verdict on that fixture
  (`C1=` token and `checks_failed` list). A run with no `C1=` line counts as `crash` and as killed, never as a pass.
- Amendment rule: the pristine counter is not edited. A mutant that survives after landing is reported as a residual, not
  patched into the frozen battery.

## Claim C2 — operability (capability acquisition): the lane's counting surface runs with the host home directory absent

Before (pre-existing artifact, not a round-95 file): the round-93 counter `.ufo/waves/round-93/count-c1.py` hardcodes the
host census path (`CENSUS` constant). Round-94 counter `.ufo/waves/round-94/count-c1v2.py` takes the fleet root by `--census`
or `SHOKUNIN_ROOT` and has no host path. Critic K01 of round 94 (`w1/Mo94K01Crit.md` §2f) named this exact shape as the
admissible before→after: a pre-existing host-bound counter measured where the host literal is absent.

Predicate P-C2r95 (same sentence in `count-c2.sh` header and the receipt): running
`bash .ufo/waves/round-95/count-c2.sh <rev> <lane> <fleet>` prints `HOSTINDEP hidden=1 before=C1=unmet(...) after=C1=met(rc=0)
control_outside=C1=met(rc=0)` and exits 0 iff, inside `unshare -rm` with the account home replaced by an empty tmpfs:
(a) the census path under the home directory is absent (`hidden=1`), (b) the round-93 counter prints `C1=unmet` or exits
non-zero, and (c) the round-94 counter with `--census` on a copied census prints `C1=met` with rc 0; and (d) the round-93
counter run outside the namespace prints `C1=met` rc 0 (positive control: the namespace is the cause).

- Do-nothing control: the entering state is the round-93 counter in the namespace, which is `C1=unmet`, so do-nothing fails (b)
  and (c) would not be reached without the successor. The before receipt is `evidence/before-c2-r95.txt`.
- Capability row (SCORECARD) enters on a passing run in this round: name `host-independent counting namespace`; evidence
  `.ufo/waves/round-95/count-c2.sh`; first-working round 95.
- Limit, stated not waived: the namespace hides only the account home directory; it does not prove the counter is host-free
  beyond that path (a literal elsewhere would not be caught), and `user_namespaces(7)` availability is host configuration
  (`/proc/sys/user/max_user_namespaces`, read-only here; no sysctl is changed).

## Frontier step (protocol §2b)

- `corpus/SOURCES.md` census before→after: `sources-census.sh validate --root <fleet> mori` exit 0 at entering (see the
  round report); at landing, exit 0 required. Rows added this round: S626 (`unshare(1)` manual, util-linux, man7) and S627
  (`user_namespaces(7)` manual, man7) — both opened in the round by a scout seat and re-opened by the L1 before the gate; any
  row the lesson does not cite is not appended (CORPUS rule 4).
- The sourced claim: C2's mechanism (user namespace plus mount namespace, tmpfs over a directory) rests on S626 / S627.
- Mistake mined: from the round-94 record (`corpus/lessons/round-94.md` Mistakes) and the round-95 spot-check routing, see
  the round lesson `## Mistakes`.

## Wave shape

ONE v1 wave `w1`, 12 seats, band 8–16: executor 2, scout 1, scribe 1, reviewer 2, critic 2, mutation-tester 2, labrat 1,
connector 1. Attack seats 7/12 (reviewer, critic, mutation-tester, labrat) ≥ 25 %. Connector 1 (≤ 2).
Seats are scored on the committed bytes of this contract's artifacts.

## Declared before data

- Both predicates above, both kill rules, the mutant anchors and their pins, the fixture list, the equivalence argument for m5,
  and the sourced-claim plan. No predicate, fixture or threshold changes after any seat has scored.
- Pins: `count-c1.py` and `count-c2.sh` as committed in this freeze commit; pristine counter sha256 `6eb7fa4c…`.
- Scratch: all clones and fixtures under `$HYAKU_SCRATCH/mori-r95` (`/fast/scratch/hyaku`), deleted on exit.
