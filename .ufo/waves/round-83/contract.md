# mori round-83 — frozen contract (claims, predicates, kill rules, controls)

Round: 83 (attempt 1). Lane: mori-shokunin (fleet/host observability; detection and report only).
Entering revision: `68185d6e719054c55b107280085b05609e96165b`.
Freeze: this file plus the three counters in the same commit; nothing below changes after the
first wave seat exists. Every predicate is the same sentence in this contract, in the counter's
code and in the receipt label.

## Round claims

| Claim | Axis (score) | Claim type | One-sentence claim |
|---|---|---|---|
| C1 | operability (7) | measured | The r82 mutation probe's counter survivors get the failing arm the probe names, so the whole frozen 23-mutant counter population is killed by the counters' own `--selftest`. |
| C2 | calibration (5, tied lowest) | measured | The r82 drift classification is bound to one committed raw snapshot: its bytes and as-of moment are graded, and one live re-derivation is executed and reported. |
| C3 | depth (5, tied lowest) | measured | The record sweep's revision arm scopes its byte occurrence test to a line carrying the binding's row anchor, and the "value present only on an unrelated line" shape is a defeated fixture. |

Two claims work the tied-lowest axis (depth 5, freshness 5, calibration 5); C2 works
calibration and C3 works depth, so the lowest-axis obligation is met. C1 works operability (7).
The three claims are causally separable: each counter grades different lane bytes and no claim's
bytes are read by another claim's counter.

Nothing here is a remediation: mori detects and reports. No source and no receipt authorizes
stopping, killing, renicing or editing any process, unit, service or host state.

## P-C1 — operability: counter mutation adequacy

Frozen sentence. At revision R, `python3 -I .ufo/waves/round-83/count-c1.py R` prints

    C1=met mutants=23 killed=23 survivors=0 total=23 pristine=green

and exits 0, where the 23-mutant table below is re-derived from R's bytes (`old` anchors, each
occurring exactly once in the named file at R), each mutated copy's own `--selftest` — run as
`python3 -I <copy> --selftest --scratch <work>` with cwd/TMPDIR under scratch — reads *killed*
(its exit is non-zero **or** it prints `fail=<n>` with n > 0), and the three pristine counters'
own `--selftest` runs are green before any mutant is graded.

Kill rule (fixed before data): a mutant that survives, a `pristine=red`, an `unanchored` anchor,
an empty mutation, or a counter whose own detector selfcheck is not green makes the claim
`unmet`; an unrun mutant is never a kill. Exit 2 is setup, never a pass.

Target: `killed=23 survivors=0 total=23 pristine=green` at the landed tip.
Entering controls (measured, `evidence/controls-r83.txt`): at `68185d6e` the counter does not yet
exist (`C1=unmet harness=absent`, rc 1); at the freeze commit — where only this counter is new and
the three graded counters are still the r82 bytes — the same command reads
`C1=unmet ... survivors=20`, rc 1. The population control is the second run; a do-nothing round
keeps it at twenty survivors.

The 23 mutants are the r82 probe's primary-run counter table
(`.ufo/waves/round-82/w1/Mo82M01Mutants.md`, "Mutant table — primary run"). Three are already
killed at entering (`unanchored_still_graded`, `stale_accepted`, `derive_key_eol_only`); twenty
survive. The claim's delta is those twenty failing arms. The record-sweep tool's 15 mutants are
not in this population; they are covered by P-C3's arm floor and fixtures.

| file | label | old (exactly once) | new |
|---|---|---|---|
| .ufo/waves/round-82/count-c1.py | green_ignores_fail_token | `return rc == 0 and "fail=0" in out and not FAIL.search(out)` | `return rc == 0 and "fail=0" in out` |
| .ufo/waves/round-82/count-c1.py | killed_ignores_rc | `return rc != 0 or bool(FAIL.search(out))` | `return bool(FAIL.search(out))` |
| .ufo/waves/round-82/count-c1.py | ignore_pristine_red | `met = pristine_ok and total > 0` | `met = total > 0` |
| .ufo/waves/round-82/count-c1.py | accept_empty_population | `and total > 0 and survivors == 0` | `and survivors == 0` |
| .ufo/waves/round-82/count-c1.py | unanchored_excused | `e.startswith("empty-mutation") or e.startswith("unanchored") for e in extras` | `e.startswith("empty-mutation") for e in extras` |
| .ufo/waves/round-82/count-c1.py | detector_gate_dropped | `return 0 if (met and own_ok) else 1` | `return 0 if met else 1` |
| .ufo/waves/round-82/count-c1.py | unanchored_still_graded | `if base.count(old) != 1:` | `if base.count(old) < 1:` |
| .ufo/waves/round-82/count-c2.py | stale_accepted | `and not stale and agreed == len(tokens)` | `and agreed == len(tokens)` |
| .ufo/waves/round-82/count-c2.py | duplicates_accepted | `and malformed == 0 and duplicates == 0 and not stale` | `and malformed == 0 and not stale` |
| .ufo/waves/round-82/count-c2.py | retired_paths_unchecked | `return (BASELINE in line and CLASSES in line)` | `return True` |
| .ufo/waves/round-82/count-c2.py | red_literal_unchecked | `and "round-10 drift pin still red" not in line` | `and True` |
| .ufo/waves/round-82/count-c2.py | green_census_tokens_accepted | `p.returncode == 1 and bool(tokens)` | `bool(tokens)` |
| .ufo/waves/round-82/count-c2.py | finding_branch_inverted | `return "value-changed" if body[len("FINDING:"):] in findings else "added-since-r10"` | `return "value-changed" if body[len("FINDING:"):] not in findings else "added-since-r10"` |
| .ufo/waves/round-82/count-c2.py | malformed_not_residual | `residual={residual + malformed}` | `residual={residual}` |
| .ufo/waves/round-82/count-c2.py | keyshape_guard_inverted | `        return "value-changed"          # frozen table: "anything else" is value-changed` | `        return "added-since-r10"          # frozen table: "anything else" is value-changed` |
| .ufo/waves/round-82/count-c2.py | derive_key_eol_only | `KEY = re.compile(r"(?:^\|\s)([A-Za-z0-9_]+)=")` | `KEY = re.compile(r"(?:^\|\s)([A-Za-z0-9_]+)=$")` |
| .ufo/waves/round-82/count-c3.py | population_gate_dropped | `if not population_ok(pins):` | `if False:` |
| .ufo/waves/round-82/count-c3.py | defeated_accepted | `ok = p.returncode == 1 and fields.get("revisions", 0) >= expect[1] \` + newline + `            and "REVISION_MISMATCH" in out` | `ok = p.returncode == 1` |
| .ufo/waves/round-82/count-c3.py | carrier_drift_allowed | `if here != show(path):` | `if False:` |
| .ufo/waves/round-82/count-c3.py | bindings_floor_dropped | `and bindings >= 3` | `and bindings >= 1` |
| .ufo/waves/round-82/count-c3.py | selftest_red_accepted | `if rc != 0 or not m or int(m.group(2)) != 0 or arms < ARMS_FLOOR:` | `if not m or int(m.group(2)) != 0 or arms < ARMS_FLOOR:` |
| .ufo/waves/round-82/count-c3.py | revisions_default_zero | `met = (caught and q.returncode == 0 and fields.get("revisions", -1) == 0` | `met = (caught and q.returncode == 0 and fields.get("revisions", 0) == 0` |
| .ufo/waves/round-82/count-c3.py | summary_first_line | `        if m:` | `        if m and not fields:` |

Anchor-integrity rule: a repair that removes or duplicates one of these anchors makes the claim
`unmet` (the counter reports it as `unanchored`). Repairs add arms or make a main-path gate
reachable from `--selftest`; they never refactor the mutated expression away.

## P-C2 — calibration: snapshot-bound drift classification

Frozen sentence. At revision R, `python3 -I .ufo/waves/round-83/count-c2.py R` prints

    C2=met snapshot=bound asof=1 tokens=64 agreed=64 residual=0 live=derived

and exits 0, where `corpus/evidence/drift-classification-r82.txt` at R carries exactly one each of

    # Snapshot: .ufo/waves/round-82/evidence/drift-r82-live.txt
    # Snapshot-sha256: <64 lowercase hex>
    # As-of: <YYYY-MM-DDTHH:MM:SSZ>

such that the snapshot path exists at R, its bytes at R hash to the stated sha256, and the stated
as-of equals the snapshot's first `# run-start:` stamp normalized to UTC whole seconds. The
snapshot's last `MORI_DRIFT:` token list is the population; the classification file carries one
`DRIFT_CLASS <token> <class>` line per token, no extra token, no malformed line, no duplicate,
and every stated class equals the class derived from the baseline bytes at R by the r82 frozen
derivation table (unchanged). `SCORECARD.md` at R keeps the `## Retired` row `drift-pin-r10`
naming the baseline, the classification path **and** the snapshot path, and the `freshness` Axes
cell carrying `r10 pin retired` and the classification path and not the red literal. One live
re-derivation runs at R (the census at R against the baseline at R): it must exit 1 and print a
non-empty `MORI_DRIFT:` list; the counter prints `live_tokens=<n>` and `live_agree=<k>` as
measured readings, and `live=derived` means the live run happened — agreement is reported, not
required, because the census is a live observation.

Kill rule: a missing/mismatched snapshot header, a hash mismatch, a wrong as-of, a token without
a class, an extra class, a class that disagrees with the derivation table, a malformed or
duplicate class line, a green or empty live census, or a SCORECARD cell/retired row that lost its
named paths makes the claim `unmet`. `snapshot=absent` (no `# Snapshot:` line) is the entering
state.

Entering control (measured): `C2=unmet snapshot=absent`, rc 1.

## P-C3 — depth: anchored occurrence in the revision arm

Frozen sentence. At revision R, `python3 -I .ufo/waves/round-83/count-c3.py R` prints

    C3=met arm=anchored defeated=2 fixtures=2/2 bindings=3 revisions=0 arms=40

and exits 0, where `tools/mori-record-sweep.py` at R contains the marker `ANCHORED_OCCURRENCE`
and `REVISION_MISMATCH`; its own `--selftest` at R is green with `pass=N`, N >= 40; the counter's
two independent fixtures both read as declared: `elsewhere` — a revision binding whose value
occurs in the bound path's bytes only on a line that does **not** carry the binding's
`row_contains` anchor must be caught (`rc 1`, `revisions>=1`, `REVISION_MISMATCH ... rev-bytes`)
— and `conformant` — the value on the anchored row must be green (`rc 0`, `revisions=0`); and
the real lane run at R with `.ufo/waves/round-82/record-pins.json` (the three frozen bindings)
is green with `bindings>=3`, `revisions=0`, rc 0.

Frozen interface: the revision arm's byte check requires, on one and the same line of
`git show <rev>:<path>`, both the `key=value` token and the binding's `row_contains` string.
The carrier-side row test, the `rev-unresolvable`/`path-absent`/`row-value` details, the summary
grammar (`RECORD_SWEEP ... revisions=N`) and the r81 command arm stay byte-compatible.

Kill rule: an absent marker, a red tool selftest, an arm count below 40, a fixture that reads
other than declared, a real binding that is not green, or a worktree/carrier mismatch (setup)
makes the claim `unmet`/setup; a fixture whose "caught" reading comes only from the summary token
without `REVISION_MISMATCH rev-bytes` is not a kill.

Entering control (measured): `C3=unmet arm=absent`, rc 1.

## Do-nothing control rule (§9)

Each counter exists in the freeze commit, so the same command grades both states. The controls are
the counters run with no lane change: C1 reads `harness=absent` at `68185d6e` and `survivors=20`
at the freeze commit (same r82 counter bytes), C2 reads `snapshot=absent` at `68185d6e`, C3 reads
`arm=absent` at `68185d6e`. None of the three targets is
reachable by re-running the counters, by adding documentation, or by touching anything the
counter does not grade (a frozen counter reads only the lane bytes named above).

## Sourcing (§2b)

C1's rule — a surviving mutant reveals a behaviour the suite does not constrain — rests on one
`SOURCES.md` row opened this round: PIT's "What is mutation testing?" page, pinned under
`corpus/evidence/sources-r83/`, with its located quote recorded in this round's lesson `## Gate`
and cited by `corpus/knowledge/counter-mutation-adequacy-r83.md`.
