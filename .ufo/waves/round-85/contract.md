# mori round 85 — frozen contract

Round 85 (attempt 1), lane `mori`, date 2026-11-04. Entering revision
`2cc4b1ae35a83e4fd3fc48bae842bdf38df2e80e` (branch `master`, r84 verifier spot-check commit).
Axes: **operability** (C1, score 7), **calibration** (C2, score 5, tied lowest) and **depth**
(C3, score 5, tied lowest). This file freezes the three predicates, their populations, kill rules,
targets and do-nothing controls **before any after-value exists**. Nothing below is narrowed after
data; a miss is an honest stop.

The three claims come from `SCORECARD.md` `## Planned (round 85)`: (1) the C1 reviewer's two
surviving counter mutants (`.ufo/waves/round-84/w1/Mo84R01C1.md` §5, X1/X2) get the failing arm
each needs; (2) the record's executing-counter-bytes gap (`.ufo/waves/round-84/w1/Mo84R03Record.md`
§0) becomes a bound receipt grammar; (3) the r84 C3 residual (own census observation) moves the
live reading from a self-report to a fact. They are causally separable: each counter reads only its
own subject's bytes at the graded revision.

## P-C1 — operability: the two surviving r84-counter mutants get their arms

Frozen predicate sentence:

> At revision R `python3 -I .ufo/waves/round-85/count-c1.py R` prints
> `C1=met mutants=2 killed=2 survivors=0 total=2 arms=17 r84=met` and exits 0, where both `old`
> anchors below occur exactly once in `.ufo/waves/round-84/count-c1.py` at R, the pristine copy's
> own `--selftest` is green with exactly 17 arms and carries both new arm labels, each mutated
> copy's own `--selftest` reads killed, and the r84 counter at R still prints its frozen 4-mutant
> `C1=met ... killed=2 equivalent=2 survivors=0 total=4` line, rc 0.

Kill rule (frozen): a mutant is killed iff its mutated copy's own `--selftest` exits non-zero **or**
prints `fail=<n>` with n > 0, conditional on the pristine copy being green. Green means rc 0, the
token `fail=0` present, and no `fail=<n>` with n > 0. An anchor that does not occur exactly once is
`unanchored` and never counted killed; an empty mutation is `empty-mutation`; a red pristine, an
unanchored anchor, an empty mutation, a red detector or a missing arm label keeps the claim unmet.
Exit 2 is setup, never a pass.

The two-mutant population (measured by the r84 C1 reviewer at `c4845c83`,
`.ufo/waves/round-84/w1/Mo84R01C1.md` §5 — "extra-mutant sweep", X1/X2; anchors at
`.ufo/waves/round-84/count-c1.py:150-151` at the entering revision):

| label | old | new | class |
|---|---|---|---|
| `X1_killed_rescued_as_equivalent` | `if not k and coupling is not None:` | `if coupling is not None:` | non-equivalent: a killed mutant with a registered coupling reads `equivalent` |
| `X2_coupling_duplicate_passes` | `coupled = all(base.count(marker) == 1 for marker in coupling)` | `coupled = all(base.count(marker) >= 1 for marker in coupling)` | non-equivalent: a duplicated coupling marker still reads `equivalent` |

Seat that lands the arms: `.ufo/waves/round-84/count-c1.py` `selfcheck()` only (+2 arms, 15 → 17):
1. `killed_mutant_with_coupling_not_equivalent` — a fixture whose label is in `EQUIVALENT`, whose
   three coupling markers each occur exactly once, and whose mutation makes the fixture's own run
   exit 1 with `fail=1` must grade `killed` with `equivalent=0`; under X1 it grades `equivalent`.
2. `duplicate_coupling_not_equivalent` — a fixture where one coupling marker occurs twice and the
   mutation is non-killing must grade `survived` with a `coupling-absent` extra and `not met`;
   under X2 it grades `equivalent` and `met`.

Target: `C1=met mutants=2 killed=2 survivors=0 total=2 arms=17 r84=met` rc 0 at the after revision.
Entering control (measured, `evidence/controls-r85.txt`): `C1=unmet mutants=2 killed=0 survivors=2
total=2 arms=15 harness=stub missing=killed_mutant_with_coupling_not_equivalent,duplicate_coupling_not_equivalent`
rc 1 at `2cc4b1ae` — the anchors and the kill rule are frozen, the two arms are not yet landed.

## P-C2 — calibration: every after receipt binds command, revision and subject bytes

Frozen predicate sentence:

> At revision R `python3 -I .ufo/waves/round-85/count-c2.py R` prints
> `C2=met receipts=3 bindings=5 bound=5 revs=3 limits=3 cmd=3 summary=3 mismatch=0` and exits 0,
> where each of the three frozen receipts carries exactly one `# cmd:`, one `# rev:` (40-hex),
> one `# limits:` line and at least one `# counter-sha256: <64-hex> <repo-relative path>` line;
> the `# rev:` resolves to a commit that is R or an ancestor of R; every bound path's bytes at
> that revision hash to the stated sha256; and the receipt body (after the single `# ---` line)
> carries its frozen summary token.

Frozen receipts (path → bound paths → summary token):

| receipt | bound paths | summary token |
|---|---|---|
| `.ufo/waves/round-85/evidence/after-r85.txt` | `.ufo/waves/round-85/count-c1.py`, `count-c2.py`, `count-c3.py` | `C1=met` |
| `.ufo/waves/round-85/evidence/record-sweep-r85.txt` | `tools/mori-record-sweep.py` | `RECORD_SWEEP` |
| `.ufo/waves/round-85/evidence/claim-sweep-r85.txt` | `tools/mori-claim-sweep.py` | `CLAIM_SWEEP` |

Rule (frozen): a header line is `# cmd: <text>`, `# rev: <40-hex>`, `# limits: <text containing the
word "limit">`, `# counter-sha256: <64-hex> <path>`; a duplicate cmd/rev/limits line, a missing
header, a non-ancestor revision, a hash that does not match the named path at that revision, or a
missing summary token is a mismatch. `bindings` counts `# counter-sha256:` lines; `bound` counts
the ones whose hash verifies. Exit 2 is setup, never a pass.

Target: `C2=met receipts=3 bindings=5 bound=5 revs=3 limits=3 cmd=3 summary=3 mismatch=0` rc 0.
Entering control (frozen): `C2=unmet receipts=0 harness=absent` rc 1 at `2cc4b1ae`. Defeat
controls (frozen): a receipt whose `# counter-sha256:` names the pre-arm bytes (the r84 counter at
the freeze commit) reads `C2=unmet bound=4 mismatch=1`; a receipt without headers reads
`C2=unmet headers=<receipt>` rc 1.

## P-C3 — depth: the counter observes the census itself and reconciles the subject

Frozen predicate sentence:

> At revision R `python3 -I .ufo/waves/round-85/count-c3.py R` prints
> `C3=met observed=3 aa=stable own_tokens=N subject_tokens=N unmatched=0 unnamed=0` and exits 0,
> where the counter runs `tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json`
> from R's own bytes three times in scratch (each with R's baseline and
> `MORI_SHOKUNIN_ROOT=<fleet root>`), every run exits 1 with a non-empty `MORI_DRIFT:` token line
> and the three token lines are identical; the subject `.ufo/waves/round-83/count-c2.py` at R runs
> and prints a `C2=met` tail plus one `LIVE_DELTA <token> <class>` line per non-agreed token; the
> counter derives, from R's own baseline and classification bytes, the class of every token in the
> union of the snapshot's token line and its own observed token line; `own_tokens` equals the
> subject's `live_tokens`; every subject-named delta token carries the class the counter's own
> observation derives (`unmatched=0`); and every token the counter's own observation classifies as
> a non-agreed delta is named by the subject with that class (`unnamed=0`).

Classes (frozen, the r83 rule): `absent-live`, `added-live`, `class-changed:<snapshot>-><live>`,
`agreed`; the derivation table is the r83 `derive()` rule over the baseline's `SURFACE`/`FINDING`/
key names (`value-changed` when the name is in the baseline, `added-since-r10` otherwise), and a
stated `unexplainable` class is never equal to a derived class.

Target: `C3=met observed=3 aa=stable own_tokens=N subject_tokens=N unmatched=0 unnamed=0` rc 0.
Claim type: **capability acquisition** (AXES.md *Capabilities*) — the counter is the claimed
artifact and its row enters the SCORECARD capabilities table in the same round.
Entering control (measured, `evidence/controls-r85.txt`): `C3=unmet observed=absent harness=absent`
rc 1 at `2cc4b1ae` (the counter does not exist there). Defeat control (measured): the same counter
over a fixture repo whose census stub prints no `MORI_DRIFT:` line reads `C3=unmet observed=3
aa=unstable own_tokens=0 rcs=1,1,1` rc 1. Disclosed reading: the new counter applied retroactively
to `2cc4b1ae`'s subject and host bytes already reads `C3=met ... own_tokens=64
subject_tokens=64`; the before value of this claim is the absence of the observation capability,
not a subject change.

## Freeze record

- Frozen at this commit before any seat ran; the three counters and `evidence/controls-r85.txt`
  land in the freeze commit.
- No pre-data amendment at freeze time. Any later amendment is appended below with its measured
  reason before an after value exists, and disclosed in the report and the round lesson.

### Amendments

**A1 (pre-data, 2026-11-04T08:12-03:00, before any after value existed).** `count-c2.py` verified a
receipt's `# counter-sha256:` binding against the bytes at the GRADED TIP rather than at the
receipt's own `# rev:`. P-C2's sentence already said "every bound path's bytes at that revision
hash to the stated sha256", so the code — not the predicate — was wrong: `grade()` now takes a
per-revision loader (`make_loader(rev)`) and `verify_bindings` reads the named revision's blob.
No predicate, kill rule, target, receipt or class changed; the counter's selftest stays
`pass=15 fail=0` and a hand-built receipt set committed after a code revision reads
`C2=met receipts=3 bindings=5 bound=5 revs=3 limits=3 cmd=3 summary=3 mismatch=0`, rc 0 (L1 probe
in scratch). `count-c1.py` (18 arms) and `count-c3.py` (19 arms) are unchanged.

**A2 (pre-data, 2026-11-04T08:17-03:00, before any after value existed; from the connector seat's
clause sweep `w1/Mo85K01Conn.md` §2, rows C1-D1, C2-D1/D2/D3/D4/D6, C3-D1/D2/D4).** Five
clarifications; **no predicate, target value, receipt, class or kill rule changed**:
- C1: the met path binds the two arm labels in the subject's BYTES plus a green pristine selftest
  with exactly 17 passing arms and the tail's `arms=17`; an arm whose name is present but whose
  assertion is vacuous is the round's mutation-probe finding, not a met-path clause (named limit).
- C2: the header block is everything before the first `# ---`; a header-shaped line after the
  separator is body text. Header lines are matched loosely, so a second malformed `# rev:` is
  `duplicate-rev`/`bad-rev` rather than invisible, and a malformed `# counter-sha256:` line is a
  `malformed-binding` problem and still counts toward `bindings`.
- C2: `# limits:` requires at least three words and the word "limit" (the counter's rule; the
  contract's rule list now states it).
- C2: the headerless-receipt defeat control reads `C2=unmet ... mismatch>=1` (the counter has no
  `headers=<receipt>` literal); the stale-digest control reads `C2=unmet ... bound=4 mismatch=1`.
**A3 (pre-data, 2026-11-04T08:20-03:00; connector row C3-D3).** `count-c3.py` now captures the
subject's `C2=<verdict>` status and `met` requires `verdict=met` in addition to rc 0 and
`live=derived`; the prose already said "prints a `C2=met` tail", so this is the code catching up to
the frozen sentence. Selftest 19 → 20 arms; the entering retroactive run stays
`C3=met observed=3 aa=stable own_tokens=64 ...`, rc 0.
- C3: the exact printed tail is `C3=<verdict> observed=3 aa=... own_tokens=N subject_tokens=N
  subject_deltas=D unmatched=N unnamed=N`; `met` additionally requires the counter's own detector
  selftest green and the classification file to parse with `malformed=0 duplicates=0`. The entering
  control is the counter FILE's absence at `2cc4b1ae` (`git cat-file -e` fails; no counter output
  exists there); running the frozen counter retroactively over that revision reads `C3=met` and
  that reading is disclosed, not the before value.
