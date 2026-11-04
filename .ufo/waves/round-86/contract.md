# mori round 86 — frozen contract

Round 86 (attempt 1), lane `mori`, date 2026-11-04. Entering revision
`fec2b328a4c83e0c61bc09d70e254ca47d547d34` (branch `master`, r85 verifier spot-check commit).
Axes: **operability** (C1, score 7), **calibration** (C2, score 5, tied lowest) and **depth**
(C3, score 5, tied lowest; claim type: capability acquisition). This file freezes the three
predicates, their populations, kill rules, targets and do-nothing controls **before any after-value
exists**. Nothing below is narrowed after data; a miss is an honest stop.

The claims come from `SCORECARD.md` `## Planned (round 86)`: (1) the r85 mutation probe's
surviving unarmed clauses get the arm each needs (`.ufo/waves/round-85/w1/Mo85M01Mut.md` §5 and
§7), starting with the duplicate-separator class (H-C2-01), the A1 bind-at-own-rev regression guard
(H-C2-A1) and C3's met-level verdict conjunct (H-C3-metverdict), with C3's `observe_three`
stability rule; (2) the C2 predicate's named stale-body limit becomes a body-versus-command binding;
(3) the own-observation rule is carried into the drift classification and its stated classes are
reconciled with a second, value-level observation. They are causally separable: C1 reads only
`.ufo/waves/round-85/count-c3.py`; C2 reads only `.ufo/waves/round-85/count-c2.py` and the receipt
set; C3 reads only the census, the r10 baseline and the r82 classification/snapshot. No claim's
counter reads another claim's subject.

## P-C1 — operability: six surviving r85-C3-counter mutants get the failing arm each

Frozen predicate sentence:

> At revision R `python3 -I .ufo/waves/round-86/count-c1.py R` prints
> `C1=met mutants=6 killed=6 survivors=0 total=6 arms=26` and exits 0, where each of the six `old`
> anchors below occurs exactly once in `.ufo/waves/round-85/count-c3.py` at R, the pristine copy's
> own `--selftest` is green with exactly 26 arms and carries all six new arm labels as `PASS`
> lines, and each mutated copy's own `--selftest` is killed by the frozen kill rule.

Kill rule (frozen): a mutant is killed iff its mutated copy's own `--selftest` exits non-zero **or**
prints `fail=<n>` with n > 0, conditional on the pristine copy being green. Green means rc 0, the
token `fail=0` present, and no `fail=<n>` with n > 0. An anchor that does not occur exactly once is
`unanchored` and never counted killed; an empty mutation is `empty-mutation`; a red pristine, an
unanchored anchor, an empty mutation, a red detector or a missing arm label keeps the claim unmet.
Exit 2 is setup, never a pass.

The six-mutant population (from `.ufo/waves/round-85/w1/Mo85M01Mut.md` §5, "HEAD-adapted mutants",
and §7 items 11–13; anchors are the **after-form** ones this round requires the subject to carry):

| label | old (after-form anchor, exactly once at R) | new | arm label |
|---|---|---|---|
| `H-C3-metverdict` | `return (rc == 0 and fields.get("verdict") == "met"` | `return (rc == 0 and True` | `subject_verdict_met_required` |
| `C3-01-rc-range` | `all(rc == 1 for rc in rcs)` | `all(rc in (0, 1) for rc in rcs)` | `stability_rc_must_be_1` |
| `C3-02-rc-dropped` | `all(rc == 1 for rc in rcs)` | `True` | `stability_rc_required` |
| `C3-03-order` | `all(tokens == first for tokens in token_lines[1:])` | `all(sorted(tokens) == sorted(first) for tokens in token_lines[1:])` | `stability_exact_order` |
| `C3-04-agreed-skip` | `if word == "agreed":` | `if False:` | `reconcile_agreed_skip` |
| `C3-07-subject-tokens` | `and subject_tokens == len(own_tokens)` | `and True` | `met_requires_subject_tokens` |

Seat that lands the arms (sole writer of `.ufo/waves/round-85/count-c3.py` this round): extract
three pure helpers and wire them in without changing any other behaviour:
1. `stability(rcs, token_lines)` — all rc equal 1, all token lines non-empty, all lines exactly
   equal to the first; `observe_three` calls it.
2. `subject_ok(rc, fields)` — rc 0 and `fields["verdict"] == "met"` and `fields["live"] ==
   "derived"`; `main` calls it.
3. `met_verdict(own_ok, stable, own_tokens, subject_tokens, unmatched, unnamed, malformed,
   duplicates)` — the current met expression, including `subject_tokens == len(own_tokens)`;
   `main` calls it.
Plus the six arm cases above (selftest 20 → 26 arms). The existing 20 arms stay byte-green.

Target: `C1=met mutants=6 killed=6 survivors=0 total=6 arms=26`.
Entering control (frozen): at `fec2b328` the subject's selftest has 20 arms and none of the six
anchors exist, so `C1=unmet` (arm-count and anchor failures). Population/stub control (frozen): a
subject that prints the six `PASS` labels and `pass=26 fail=0` but implements no checks must read
`C1=unmet` (every mutant survives) — the labels and the tally alone are not the work.

## P-C2 — calibration: each receipt's body is bound to its command, not just to a digest

Frozen predicate sentence:

> At revision R `python3 -I .ufo/waves/round-86/count-c2.py R` prints
> `C2=met receipts=5 bindings=7 bound=7 revs=5 limits=5 cmd=5 summary=5 replay=2 matched=4
> defeated=1 legacy=3 unexpected=0` and exits 0, where the subject
> `.ufo/waves/round-85/count-c2.py` at R is green in its own `--selftest` with exactly 21 arms and
> carries the three new arm labels `replay_match`, `replay_stale_mismatch`,
> `replay_none_requires_reason`; the subject run at R over the five frozen receipts prints that
> same line; and the r86 counter independently executes the `required` receipt's `# cmd:` in a
> scratch export of that receipt's own `# rev:` and reproduces its body byte-for-byte, while the
> `reject` receipt's body differs from its command's output in that same export.

Rule (frozen, extending the r85 grammar): a header line is `# cmd: <text>`, `# rev: <40-hex>`,
`# limits: <text containing "limit" and ≥3 words>`, `# counter-sha256: <64-hex> <path>`, and a new
optional `# replay: required|none` with, for `none`, `# no-replay: <≥3 words>`. A receipt with
`# replay: required` must have its body equal to the stdout of its `# cmd:`, executed in a scratch
export of the receipt's `# rev:` with `GIT_CONFIG_GLOBAL=/dev/null`; a mismatch is a problem. The
frozen r85 receipts carry no `# replay:` line and are graded by the r85 header grammar as `legacy`
(a named, frozen limit: their bodies predate the replay rule). A receipt the population marks
`expect=reject` must produce at least one problem; one marked `expect=met` must produce none.

Frozen receipt population (path → token → replay → expect):

| receipt | summary token | replay | expect | bindings |
|---|---|---|---|---|
| `.ufo/waves/round-85/evidence/after-r85.txt` | `C1=met` | legacy | met | 3 |
| `.ufo/waves/round-85/evidence/record-sweep-r85.txt` | `RECORD_SWEEP` | legacy | met | 1 |
| `.ufo/waves/round-85/evidence/claim-sweep-r85.txt` | `CLAIM_SWEEP` | legacy | met | 1 |
| `.ufo/waves/round-86/evidence/after-c1-r86.txt` | `C1=met` | required | met | 1 |
| `.ufo/waves/round-86/evidence/replay-defeat-r86.txt` | `C1=met` | required | reject | 1 |

`bindings=7`, `bound=7`: the two new receipts bind `.ufo/waves/round-86/count-c1.py` at the
revision their `# rev:` names. `matched=4` (three legacy + the after receipt), `defeated=1` (the
defeat receipt), `unexpected=0` (no receipt failed its expectation).

Target: `C2=met receipts=5 bindings=7 bound=7 revs=5 limits=5 cmd=5 summary=5 replay=2 matched=4
defeated=1 legacy=3 unexpected=0`.
Entering control (frozen): at `fec2b328` the two r86 receipts do not exist and the subject's
selftest has 18 arms with none of the three replay labels, so `C2=unmet`.
Stale-body control (frozen, load-bearing): the defeat receipt carries correct headers, a correct
`# rev:`, a correct `# counter-sha256:`, and a body that differs from its command's stdout by one
byte. Under a header-only gate it reads met; under the replay rule it is `defeated` — that single
receipt is the do-nothing control for this claim.

## P-C3 — depth: the classification's stated classes are reconciled with a value-level observation

Claim type: **capability acquisition** (AXES.md *Capabilities*): the value-channel observer is the
claimed artifact and its row enters the SCORECARD capabilities table in the same round.

Frozen predicate sentence:

> At revision R `python3 -I .ufo/waves/round-86/count-c3.py R` prints
> `C3=met observations=2 aa=stable tokens=64 derived=64 name_agree=64 value_rows=14
> contradicting=2` and exits 0, where the counter observes `tools/mori-census.sh` from R's own
> bytes **twice through each of two surfaces** in separate scratch trees with R's baseline and
> `MORI_SHOKUNIN_ROOT=<fleet root>`: the drift surface (`--drift <baseline>`; every run exits 1
> with a non-empty `MORI_DRIFT:` token line, both token lines identical) and the full-report
> surface (no `--drift`; both runs exit 0 or 1 with `SURFACE ` rows, and every non-volatile
> field's multiset of `key=value` occurrences is identical across the two runs, volatile fields
> taken from the baseline's own `# volatile_fields=` header);
> `tokens` is the count of `DRIFT_CLASS` rows in `corpus/evidence/drift-classification-r82.txt`
> and every stated class equals the frozen name-rule derivation; `value_rows` counts the stated
> `value-changed` rows; and `contradicting` counts those of them whose field name's recorded value
> appears **equal** in the r10 baseline and in the live observation (both runs), i.e. a
> `value-changed` label the value channel does not support.

Rule (frozen): the name-rule derivation is the r83 `derive()` table (SURFACE/FINDING name in the
baseline → `value-changed`, else `added-since-r10`; `VERDICT`/`HEADER`/`BLANK` → `value-changed`;
non-key shape → `value-changed`; key in the baseline → `value-changed`, else `added-since-r10`).
The value channel extracts `name=value` atoms from the baseline bytes and from the live output;
for a stated `value-changed` row whose token body is a bare key, it compares the baseline's value
set with the live value set: `equal` (contradicting), `differs` (supported), `masked` (baseline
value is `<V>`), `absent` (not extractable in one side), `name-shape` (SURFACE/FINDING/word token —
the rule does not apply). `contradicting` is the count of `equal`.

Target: `C3=met observations=2 aa=stable tokens=64 derived=64 name_agree=64 value_rows=14
contradicting=2`.
Named limit: `contradicting=2` is the measured value of the two static-string rows
(`-subject_commits` `yes`, `-window` `launch..NOW`); `differs`/`masked`/`absent`/`name-shape`
counts are printed but not target-bound because live values move. The value channel reads the
census's own textual full report; it is not a second census implementation.
Entering control (frozen): at `fec2b328` the counter FILE does not exist
(`git cat-file -e <rev>:.ufo/waves/round-86/count-c3.py` rc 128); the capability is the claim.
Disclosed reading: applied retroactively to the entering bytes the counter reads `C3=met` — this
row claims a capability, not a subject-state move.

## Frozen instruments

The three counters `.ufo/waves/round-86/count-c1.py`, `count-c2.py`, `count-c3.py` are committed at
the freeze commit with this contract, before any after-value exists. Their `--selftest` arms are
graded in the same run they grade (each counter runs its own selftest and prints `detector=green`).
`python3 -I` is mandatory: no user site-packages, no `PYTHONPATH` contamination.

## Do-nothing controls (committed before data)

`evidence/controls-r86.txt` records: each counter at the entering revision (all three `unmet` by
absence), the C1 label-only stub (unmet: all six mutants survive), the C2 header-only gate against
the defeat receipt (met — which is why the replay rule, not the digest, is the claim), and the C3
retroactive reading (met, disclosed). `evidence/controls-r86-defeated.txt` records each control
being defeated by the landed work (the same input reading met/unmet as the claim requires).

## Amendments (pre-data; no after-value existed when each landed)

**A1 (2026-11-04, before any seat returned a claim reading; scout `w1/Mo86Sc01Scout.md` R1/R2).**
Two clarifications of P-C2, neither moving a target, population or count:
(i) the subject `.ufo/waves/round-85/count-c2.py` accepts `--scratch DIR` (defaulting to
`$HYAKU_SCRATCH`, else a temp dir) and runs green under it — the replay pass needs a scratch root
it owns, and the r86 counter invokes the subject with `--scratch`;
(ii) the r86 counter's stub guard is the three arm labels plus the subject's own 21-arm green
selftest; it no longer requires a particular helper name (`def replay_receipt(`), because the
contract never froze a function name and the name is not behaviour. The frozen counts, the receipt
population and the target line are unchanged.

