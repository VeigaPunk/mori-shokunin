# mori round-87 — frozen contract (claims, counters, controls)

lane: mori · round: 87 · attempt 1 · date: 2026-11-04 · L1: MoriR87
entering revision: `6fc09d69edbb11e5070ff33258de49f062c0fb9b` (lane branch `master`, `ahead=0`)
axes: **operability** (score 7) and **calibration** (score 5, tied lowest: depth 5, freshness 5,
calibration 5). Detection and report only.

Two claims. Each is causally separable: C1 grades three selftest arm sets added to the r86
counters; C2 grades a receipt population and its supersede rule. Neither reads the other's work.

## C1 — operability — the six surviving r86-counter clauses get the failing arm each

**Frozen predicate P-C1** (identical sentence here, in `.ufo/waves/round-87/count-c1.py` and in the
receipt label):

> At revision R `python3 -I .ufo/waves/round-87/count-c1.py R` prints
> `C1=met mutants=6 killed=6 survivors=0 total=6 arms=54` and exits 0, where each of the six `old`
> anchors occurs exactly once in its named r86 counter at R, each pristine copy's own `--selftest`
> is green with exactly its frozen arm count (count-c1.py 18, count-c2.py 13, count-c3.py 23), and
> each mutated copy's own `--selftest` is killed by the frozen kill rule.

Population (all six survive the entering selftests; measured by
`.ufo/waves/round-87/evidence/probe-r87.txt` at `6fc09d69`):

| mutant | file | clause |
|---|---|---|
| `M1-unanchored-conjunct` | count-c1.py | the `met` refusal of unanchored/empty mutations |
| `M2-total-floor` | count-c1.py | the `total > 0` floor in `met` |
| `M3-arms-tally` | count-c1.py | the tail `arms=` reading of the subject tally |
| `M4-receipt-summary` | count-c2.py | the body summary-token requirement |
| `M5-binding-digest` | count-c2.py | the counter-sha256 binding comparison |
| `M6-keyshape` | count-c3.py | the non-keyshape branch of `derive()` |

**Kill rule (frozen):** a mutant is killed iff the mutated copy's own `--selftest` exits non-zero
**or** prints `fail=<n>` with n > 0, conditional on the pristine copy being green with its frozen
arm count. An anchor that does not occur exactly once is `unanchored` and never counted killed; an
empty mutation is `empty-mutation`; a red pristine, a wrong arm count, an unanchored anchor, an
empty mutation or a red detector keeps the claim unmet. Exit 2 is setup, never a pass.

**Do-nothing control (C1):** `.ufo/waves/round-87/evidence/controls-r87.txt` §C1 — the frozen
counter over the entering bytes reads `C1=unmet mutants=6 killed=0 survivors=6 total=6 arms=48`
(rc 1), and a label-only fixture that prints the six `PASS <label>` lines without any assertion
still reads `C1=unmet ... survivors=6` (rc 1). Labels and tallies alone are not the work.

## C2 — calibration — a legacy receipt is superseded by a replaying successor

**Frozen predicate P-C2** (identical sentence here, in `.ufo/waves/round-87/count-c2.py` and in
the receipt label):

> At revision R `python3 -I .ufo/waves/round-87/count-c2.py R` prints `C2=met receipts=7 absent=0
> bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2
> legacy=1 unexpected=0` and exits 0, where the seven population receipts all exist at R, every
> `# counter-sha256:` binding matches its named path's bytes at the receipt's own `# rev:`, both
> `# replay: clone` receipts reproduce their bodies in a `--shared` clone checked out at that rev,
> the one reject receipt still reports a problem, and a legacy receipt (no `# replay:` line)
> counts `superseded` only when a present, problem-free successor names it in `# supersedes:`.

Population: the r85 receipts `after-r85.txt`, `record-sweep-r85.txt`, `claim-sweep-r85.txt`
(legacy), the r86 receipts `after-c1-r86.txt` (met) and `replay-defeat-r86.txt` (reject), and this
round's successors `.ufo/waves/round-87/evidence/record-sweep-r87.txt` and `claim-sweep-r87.txt`
(`# replay: clone`, `# supersedes:` the two r85 sweep receipts). `after-r85.txt` stays `legacy`:
its body is a live-observation run (count-c3 observes the census three times), so no committed-byte
successor can reproduce it; the reason is recorded in the round lesson's Gate block.

**Do-nothing control (C2):** `controls-r87.txt` §C2 — at the entering revision both successors are
absent, so the frozen counter reads `C2=unmet receipts=5 absent=2 ... superseded=0 legacy=3`, and a
fixture carrying both successor files with correct headers and digests but fabricated bodies
replays as `replay-mismatch`, leaving `superseded=0 legacy=3` (rc 1). The supersede rule reads the
replay, not the header.

## Freeze

Frozen at this commit, before any after-value existed: `count-c1.py`, `count-c2.py`, this
contract, `evidence/controls-r87.txt` and `evidence/probe-r87.txt`. No target, population or
kill rule moves after data. A miss is an honest stop.
