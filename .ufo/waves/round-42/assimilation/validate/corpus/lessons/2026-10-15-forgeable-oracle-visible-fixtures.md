# Lesson — a fixture oracle can be forged when the system under test can see which case is running

date: 2026-10-15 · lane: mori-shokunin · round: 4 · source seat: lessons-distiller (flash wave)

Measured against the round-3 **frozen oracle** `tools/mori-silence-cases.sh` sha256
`505a7504811401b13fd96f8925605e744fbb54970c8ac65ac331b053d647e580` and census r2
`tools/mori-census.sh` sha256
`fe22a14f0bb6d90ffed14506abfcd76153ebf31cf3cb769b97e7eec61cc2f3c9`
(`VERSION=census-r2`). The round-4 wave was editing the oracle while this note was
written; every figure carries its sha, and the hardened revision is measured in
**Cutover state** below. This is a class note, not a scalar score.

## The lesson

A behavioral oracle is a measuring device: it feeds the system under test (SUT) a
fixture and grades the answer. Two defects measured in round 4 composed into one
class — **the oracle's maximum tally was reachable with no logic at all**:

1. **Identity leak.** Each case built its fixture at `$WORK/c/$CASE_ID` and handed
   the census that path, with the same id inside `MORI_UFO_DIR`, `MORI_STATE_DIR`,
   `MORI_DISK_TARGETS`, … (frozen sha: `:149`, `:269`, `:270`, `:271`, `:273`,
   `:285`). The census — the SUT — could read *which case was running* and answer
   by identity instead of behavior. The expectation table is the case-id list, so
   the leak hands the SUT the answer key.
2. **A matcher that accepted a non-state.** `assert_case` compared with
   `case "$obs" in $want)` (`:361-365`); a `|` introduced by parameter expansion
   is a **literal** pattern character in bash, so the want-sets
   `not-open|unavailable` and `progressing-weak|silent` could only ever be matched
   by a literal string that no implementation can legitimately emit (the state
   vocabulary has no `|` member).

Together: a no-logic census that prints, per leaked case id, the canned expected
row scored **`matched=27 total=27`, exit 0** — including `PASS ledger-missing-not-silent
(state=not-open|unavailable via lane…)`, a "state" that is not a state. The same
oracle scored the honest census **25/27**. The count registered as the lane's
terminal end-goal was reachable only by lying, and the oracle's own defect was the
lie's accomplice. (Round 3 recorded the forgery as a one-line note,
`.ufo/reports/round-3/mori-goalwave.md:73`; this note carries the measured repro.)

## What was measured (2026-10-15T17:29–17:37Z, /tmp scratch)

The two frozen-oracle runs were executed twice: once with the live working tree
(sha checked immediately before) and once with a git-extracted copy of the frozen
revision (`git show HEAD:tools/mori-silence-cases.sh`, sha verified `505a7504…`);
both log pairs are **byte-identical**, so the mid-wave edit did not touch these
figures.

| # | oracle | census | result |
|---|---|---|---|
| 1 | frozen `505a7504…` | honest r2 `fe22a14f…` | `matched=25 total=27`, exit 1; FAILs = the two literal-alternation cases |
| 2 | frozen `505a7504…` | no-logic sniffer, 26 lines, reads only the leaked id | **`matched=27 total=27`, exit 0** |
| 3 | hardened `be0e28b8…` (in-flight) | honest r2 `fe22a14f…` | `matched=28 total=28`, exit 0 |
| 4 | hardened `be0e28b8…` | the same sniffer | `matched=1 total=28`, exit 1 |

Logs (scratch, sha256): frozen-honest `5ec51973…`, frozen-sniffer `5e2cbba8…`,
after-honest `a7e4a580…`, after-sniffer `bdbd1aa2…`; sniffer source `82e49804…`
(all under `/tmp/mori-lessons-r4/`). The sniffer's whole "logic" is
`case "$id" in …)` over the id parsed from `MORI_SHOKUNIN_ROOT`, then printing a
canned `SURFACE lane.<lane>: <state>` row, the finding and the exit code.

Bash semantics probe (this host, GNU bash 5.3.15):

```
$ want='not-open|unavailable'; obs=unavailable
$ case "$obs" in $want) echo MATCH;; *) echo no-match;; esac
no-match
$ [[ "$obs" =~ ^($want)$ ]] && echo MATCH
MATCH
```

## Why it is easy to miss

- The tally is a scalar: `25/27` reads as "the implementation still fails 2 of 27",
  not as "the oracle cannot pass 2 of 27" — round 3 needed a whole section and a
  counterfactual witness to prove those two FAILs were the oracle's
  (`corpus/knowledge/silence-cutover-r3.md:182-217`).
- The leak is the harness's own ergonomics (human-readable case directories), not
  something the SUT shows; nothing in the SUT's output says whether it used the
  input or the identity.
- Standard probes point the wrong way. Mutant-census probes (round-2 lesson) make
  the SUT *worse* and check the oracle notices; they never ask "can a SUT with no
  logic reach the ceiling?". Only a deliberate **forgery probe** — a cheating SUT —
  finds a false-green channel. (Inverse of the round-2 lesson's crash-masking
  false-red; both come from trusting one number.)
- The two defects reinforce each other: because the pattern could only match the
  literal string, the forger's impossible state was exactly what the failing
  cases demanded — while an honest implementation failed those same cases.

## Countermeasures that fit this codebase (evidence-backed)

1. **Opaque per-case trees, no marker exports.** Round-4 revision `be0e28b8…`:
   `new_case` builds `CASE_DIR=$(mktemp -d "$WORK/case.XXXXXXXX")` (`:187`) and
   `MORI_FIXTURE=1` is gone from the census export list. Measured effect: the
   sniffer drops from 27/27 to 1/28 (row 4).
2. **Shape invariance as a case.** Build the same fixture bytes under two random
   directory names and require identical grades *and* identical stdout
   (`:690-734`). Measured: it fired against the sniffer in row 4 (the sniffer's
   stdout embedded the path-derived id).
3. **Alternation-safe matching.** `want_match()` (`:342-348`, call site `:389`)
   replaces the `case` dispatch; give the matcher its own self-test —
   a want-set `a|b` must accept `a` and `b`.
4. **Register expectations as membership, not an integer target**, where a case
   admits a set of correct states: a raw `N=M` end-goal made a matcher defect look
   like an implementation gap for a full round.
5. **Keep a forgery probe in the oracle's repertoire.** A stub that reads whatever
   identity it can see and prints the expected shape; the oracle must reject it.
   Seconds to run, and it is the only probe that finds this class.

## Applying it (any lane)

- List every path and environment value handed to the SUT; if any encodes which
  scenario is running, there is a sniffer channel. In bash harnesses:
  `grep -nE 'CASE_ID|\$WORK/c/' harness.sh` and review each hit.
- Grep for expanded-pattern matchers: `grep -nE 'case .* in \$\{?\w+' harness.sh`.
  `case "$x" in "$p")` is still a literal compare, not alternation; if a set is
  intended, use a match helper and test the helper.
- Run the cheat: point the harness at a stub that answers from identity (or from
  echo) and check whether the harness can tell. If it cannot, its tally is void.
- Prefer hash/random fixture directory names; do not export fixture markers the
  SUT can branch on — grading must be behavior-based.

## Cutover state measured (round-4 hardening, mid-wave snapshots)

- oracle `be0e28b8…` (in-flight; the frozen `505a7504…` is still git HEAD's bytes):
  opaque dirs, no `MORI_FIXTURE`, `want_match`, shape-invariance case.
- census `af2d4e79…` (in-flight): the `:227` `state_n` bare pipeline is rc-gated
  (`cap find` + disclosure field). Measured by this seat: at the `fe22a14f` bytes,
  the canary (`.ufo/state` `chmod 000`) exits rc 1 with the header line only,
  **0** verdict lines, 0 bytes stderr; at `af2d4e79…` the same canary exits rc 1
  with 13 lines and a full `MORI_CENSUS: DRIFT` verdict, identical to the readable
  control. Class definition:
  `corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md`.
- The honest end-to-end tally at the **final** round-4 SHAs is the wave's
  acceptance job; rows 3–4 above are this seat's anti-sniff evidence. The wave's
  own receipt `corpus/evidence/verdict-r4-20261015T173551Z-sniffer-v2.log`
  independently shows the same close (`m4b`/`m4c` verbatim → `matched=1 total=28`)
  and adds a stronger forger: `v2b`, an identity-blind replay keyed on invocation
  order, reaches `matched=27 total=28` — its **only** failure is the
  shape-invariance case.

## Limits

- All scratch under `/tmp/mori-lessons-r4/` (shas above). Re-run recipe:
  `git show HEAD:tools/mori-silence-cases.sh > /tmp/oracle-frozen.sh`;
  `git show HEAD:tools/mori-census.sh > /tmp/census-r2.sh`; then
  `bash /tmp/oracle-frozen.sh /tmp/census-r2.sh` (expect `matched=25 total=27`)
  and `bash /tmp/oracle-frozen.sh <sniffer>` (expect `27/27`, exit 0). The sniffer
  body is a 26-line id→row table, mechanical, not reproduced inline.
- Shape invariance is the load-bearing counter against name-keyed sniffers (row 4)
  and invocation-order replay (the wave's `v2b` receipt); it is necessary, not
  sufficient: a forger keyed on fixture *content* (memorized content→expectation
  table) still passes it. Only randomizing fixture parameters makes memorization
  cost approach real logic.
- Row 2 shows the ceiling *was* reachable without logic at those SHAs; it does not
  claim any real census did so.
- The canary closes the `:227` unreadable-`.ufo/state` input only; the other
  unreadable-input canaries were swept in the round-3 lesson and are not re-swept
  here.
- `be0e28b8…`/`af2d4e79…` are mid-wave snapshots; re-run rows 3–4 and the canary
  at the final round-4 SHAs before quoting them as steady state.
- No liveness claim; live census figures elsewhere are mutable.