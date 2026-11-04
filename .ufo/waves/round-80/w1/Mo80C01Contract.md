# Mo80C01Contract — first contract falsifiers (read-only critic)

## 1. Scope, axes and disposition

Reviewed the frozen contract, controls, three r80 counters, r79 contract and closure, SCORECARD axes/capabilities/r79 tail, SKILL registry, QUALITY 90/154/159/161–164 and PROVINCE boundaries. No implementation, counter, contract, pin, fleet or sibling file was edited. These are proposed corrections for L1/canonical judgment, not amendments to the frozen contract or an admission decision.

| Claim | Review verdict | Impacted axes | Smallest safe correction |
|---|---|---|---|
| C1 | needs the named clause | calibration; operability of its verifier | Require all four zero fields, independently check the entering witness, and align the counter/receipt with the actual predicate. Row-only cheating is already rejected. |
| C2 | needs the named clause | operability, with calibration harm if vacuous kills are claimed | Require the unmutated selftest to pass at the exact revision being graded before counting mutant kills. |
| C3 | needs the named clause | coverage; calibration/adjacency if classifications imply ownership | Explicitly bound the automated verdict to path coverage; independently establish class/registry/purpose correctness, or declare those descriptive fields unverified by this counter. |

Axis fit is otherwise sound. `read /home/vgpnk/Projects/shokunin/AXES.md:9-16,25-38` defines calibration as self-assessment matching observed state, operability as executable artifacts, coverage as governed paths/tools. `read .../SCORECARD.md:6-15` gives coverage 6, operability 7, depth/freshness/calibration 5, adjacency 6; `:56-58` says none retired. Thus C1 works a lowest non-retired axis, C2/C3 are distinct. C3 is inventory coverage, not additional host-event coverage. The C1 total cannot establish universal self-assessment correctness: the frozen sweep enumerates only pointer resolution, pinned selftest tallies and chosen stale literals in selected carriers.

## 2. Bytes and commands exercised

All paths below are absolute in the executed commands. In probe snippets, `R` was `/home/vgpnk/Projects/shokunin/mori-shokunin` and `S` was `/fast/scratch/hyaku/mori-r80/Mo80C01Contract`. Python Eval used stdlib `runpy`, `subprocess`, `tempfile`, `pathlib`, `hashlib`, `shutil`; subprocess environments set `TMPDIR=S` and `PYTHONDONTWRITEBYTECODE=1`. Scratch was removed in `finally` after both batches: `SCRATCH_REMOVED=True` each time. No installs/updates.

Executed `git -C R rev-parse HEAD`:

```text
57451ecbbc5a63cfefaab28b1a1b60c08b41bee7
rc=0
```

Executed `hashlib.sha256((R/relative_path).read_bytes()).hexdigest()` before the probes:

```text
.ufo/waves/round-80/contract.md 50b27c7fe893feddcfb9a42fe340a519a73797c7673723dcb73715fb3d5aa03d
.ufo/waves/round-80/count-c1.py efd81f34f7e9e65aaa83548713b4bc257a4343da51e8330d3eddcbba39983645
.ufo/waves/round-80/count-c3.py 6446de67d2b5e6d9f35664d190ec8dde8ddd4d9dead58dd79abc3867aaf7f2d5
.ufo/waves/round-80/mutate-c2.py 16a203b919e33f1cb7d957c1062a559295aa6abe3b9d3e95146871a2998cf7aa
.ufo/waves/round-79/count-c2.py 8d7fae146589341368399b490ae7c5b4bd55ee9d25496202ca8e0f7e010f1d69
```

The r79 counter worktree differs from committed bytes; it was not substituted for a worked revision. Executed `git -C R show REV:.ufo/waves/round-79/count-c2.py` at `d5888922` and `57451ecbbc5a63cfefaab28b1a1b60c08b41bee7`; SHA-256 of stdout was `fed9a8292158b6d69e9d786d48fcbed02cb30772b5a5cb4e0386d0b034472290` at both revisions. Both show commands returned 0.

## 3. C1 — row-only attack fails; predicate/output gap survives

Executed:

```text
$ python3 -I R/.ufo/waves/round-80/count-c1.py d5888922 --repo R --scratch S
C1=unmet tool=absent sweep=- mismatches=- row_tally=- live_tally=- rev=d58889220d3c
rc=1
```

`read count-c1.py:74-96` confirms it exports R, executes the tool from that export, and independently compares the SCORECARD guard tally to the guard's live selftest. A row edit alone cannot pass with the sweep absent. Function-level counterexample attempt: copy a scratch tree containing only a corrected row into `grade`'s export destination; replace only the export helper so no fixture commit is needed. Output:

```text
ROW_ONLY_PROBE (1, 'C1=unmet tool=absent sweep=- mismatches=- row_tally=- live_tally=-')
```

Strongest successful attack: same function-level scratch-tree probe, but with these exact child program bodies:

```python
# tools/mori-claim-sweep.py
print('CLAIM_SWEEP mismatches=0 unresolved=7 tallies=8 stale=9')
# tools/mori-control-receipt.py
print('CONTROL_RECEIPT_SELFTEST pass=19 fail=0')
```

Pins were `{}` and the card row was `| guard `tools/mori-control-receipt.py` | selftest 19 in-memory cases |`. Invoked the loaded frozen `grade` after replacing its export helper with `shutil.copytree(source, dest); return True`. Observed:

```text
(0, 'C1=met tool=present sweep=0 mismatches=0 row_tally=19 live_tally=19')
```

This is a real counter-function false acceptance, not a full CLI/committed-fixture receipt. Lines 83–93 parse all four integers but grade only the total. Even a constant all-zero sweep would be accepted with a correct guard row: that is a named trust boundary, not proof of a working sweep. The counter does not check the sweep's frozen interface/arms, nor replay it over entering bytes.

Contract P-C1 also says “the same sweep at the entering revision ... finds at least one mismatch.” The entering tool is absent, so `count-c1 d5888922` proves absence, not a mismatch count of one. The baseline replay must explicitly mean the landed sweep and pins applied to an entering export; current count-c1 never performs that replay. Do not label `tool=absent mismatches=-` as an observed `mismatches=1`.

Exact recommended clause:

> At revision R, the exported sweep exits 0 and emits exactly one summary whose mismatches, unresolved, tallies and stale fields are all 0; the exported control-receipt capability row's tally equals that tool's successful selftest count. Separately, the same sweep and pins from R, run against an export of d5888922, must report the named 18-versus-19 SCORECARD mismatch and exit 1. The claim covers only the frozen pointer, pinned-tally and stale-literal arms, not every semantic assertion in the carriers.

The replay should be part of the frozen counting command if it is part of the claim. Fixing only prose while continuing to grade the old counter would retain the defect. If rules truly cannot change now, preserve the existing freeze and report the unsupported portion rather than silently treating the recommendation as its rule.

## 4. C2 — vacuous counter-killer reproduced

Loaded the frozen harness with `runpy.run_path`, invoked its own `_fixture(path, True)`, `selftest_verdict(path, S)` and `grade(text, S)`. That fixture retains all six mutation anchors inside a string and always exits 1 on selftest. Actual output:

```text
baseline_red_verdict=('killed', 'rc=1 C2_COUNTER_SELFTEST pass=6 fail=0')
mutant drop_admitted killed rc=1 C2_COUNTER_SELFTEST pass=6 fail=0
mutant raise_ceiling killed rc=1 C2_COUNTER_SELFTEST pass=6 fail=0
mutant count_other_verdicts killed rc=1 C2_COUNTER_SELFTEST pass=6 fail=0
mutant cut_clause_boundary killed rc=1 C2_COUNTER_SELFTEST pass=6 fail=0
mutant any_round_in_cell killed rc=1 C2_COUNTER_SELFTEST pass=6 fail=0
mutant met_ignores_mismatch killed rc=1 C2_COUNTER_SELFTEST pass=6 fail=0
MUTATION_C2 survivors=0 killed=6 total=6
```

The summary above was printed by the probe from the returned verdict list, not represented as an actual `--rev` CLI receipt. The underlying six verdicts are the frozen harness's actual output. Harness `:60-71` calls any missing-summary result killed too, including crashes; `:74-90,158-169` never run an unmutated baseline. Thus zero survivors alone is insufficient. Even an added always-failing arm, with all production predicate bytes untouched, can vacuously kill all mutants; the arms-only restriction does not solve this.

Ran actual committed unmutated bytes: `git show REV:.../count-c2.py`, wrote stdout under S, then `python3 -I S/<REV>-count-c2.py --selftest --scratch S`, once at `d5888922` and once at the observed HEAD. Both emitted:

```text
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=4 fail=0
rc=0
```

This establishes green baseline at the entering and currently committed revision, NOT at an eventual worked r80 revision. The final worked revision did not exist in the observed committed bytes. Closure must rerun there. The r79 contract `:94-100` explicitly requires counter selftests passing before data; r79 closure `:96-102` routes missing mutant arms. I did not find the user-paraphrased exact sentence “a counter that cannot be red ... is broken” in that closure; do not quote it as verbatim provenance.

Exact recommended clause:

> At revision R, before mutation, the unmodified count-c2.py selftest must exit 0 and emit C2_COUNTER_SELFTEST pass=P fail=0 with P>0. Only then may the six frozen single-mutant selftest verdicts establish MUTATION_C2 survivors=0 killed=6 total=6; a baseline failure or missing baseline summary makes C2 unmet/setup, never six kills.

A baseline preflight does not establish broad mutation adequacy; this is exactly six frozen mutants, not all possible mutants. Three added arms are a separate deliverable requiring an arms-only diff and per-survivor mapping; the harness total alone cannot establish that deliverable.

## 5. C3 — false classifications are invisible to the predicate

Executed:

```text
$ python3 -I R/.ufo/waves/round-80/count-c3.py d5888922 --repo R --scratch S
C3=unmet named=14 present=55 missing=41 extra=0 rev=d58889220d3c
missing_first=mori-anchor-check.py,mori-blind-check.sh,mori-cgroup-pressure.py,mori-content-review.py,mori-control-receipt.py,mori-counter-win.py,mori-disk-rate.py,mori-drift-adjudicate.py
rc=1
```

Loaded the frozen counter; `present = present_set(R, 'd5888922')`; constructed its input with this exact expression:

```python
body = '\n'.join('| `tools/'+t+'` | OWNS_OS_REMEDIATION | registry 999 | false |'
                 for t in sorted(present))
print(grade(body, present))
```

Actual result:

```text
{'met': True, 'named': 55, 'present': 55, 'missing': [], 'extra': []}
body_sha256=6d0e408c09138340fab4413f3a21184242bf7748a598054c816c6f63c5473ed8
```

This function-level fixture uses the actual entering committed path set but deliberately false class, registry and purpose fields. No committed CLI fixture was claimed. `grade` examines only path tokens (`:47-58`), anywhere in prose/table, not the inventory section, row count, classifications, registry links or purpose. Therefore the names-only predicate admits the dump; C3's class/registry wording overreaches the executable predicate. Literal path mention is not proof of scope ownership, registration, behavioral correctness or explored surface.

Exact recommended clause:

> C3's automated predicate measures path-inventory completeness only: every direct committed tools/*.py or tools/*.sh basename at R is named and extra=0. Class, registry row (or —) and one-line purpose must be present in the inventory and independently checked against the committed instrument and SKILL registry; the names counter does not verify those annotations. Inventory presence neither promotes a tool to Core nor grants remediation, orchestration, endpoint or credential ownership.

If class/registry correctness remains part of the mechanically graded claim rather than an independent review obligation, the predicate and command need an enumerated metadata check; do not claim the current C3 output certifies it. PROVINCE `:12-18` explicitly refuses OS/systemd/remediation, dispatch, serving and secrets ownership. My false fixture violates those boundaries while still scoring path-complete: that is the calibration/adjacency hazard.

Sizing issue: the entering denominator is 55, but C1 adds a new direct tool. If it lands alongside C3 and no instrument is removed, the final dynamic denominator is 56. “55 of 55” is a stale fixed target; `named=present, missing=0 extra=0` remains the right revision-indexed measure. This is not a dependency on C1 for C3 verification; it is a denominator change across combined landings.

## 6. Same-sentence audit and unenumerated claims

| Claim | Contract sentence / literal target | Counter label | Existing control receipt label | Mismatch |
|---|---|---|---|---|
| C1 | `:27-32`: “prints CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 and exits 0”; entering same-sweep mismatch | `C1=met|unmet tool=... sweep=... mismatches=... row_tally=... live_tally=...` | controls `:33-35`: `C1=unmet tool=absent ... mismatches=- ...` | Counter omits three component fields and does not require them zero; entering replay not executed; extra independent row-equality arm appears in counter docstring `:14-16`, not verbatim P-C1. Absence is not numeric mismatch=1. |
| C2 | `:39-45`: `MUTATION_C2 survivors=0 killed=6 total=6`; entering `survivors=2 killed=4 total=6` | same summary label, suffix `rev=` | controls `:38-46`: entering `survivors=2 killed=4 total=6` | Harness docstring `:10` still says entering 3/3; top claim table `:17` says from 3 of 6, whereas measured entering is 4 kills. No baseline-green clause. Three reported survivor classes versus two frozen-harness survivors are distinct populations, not interchangeable measurements. |
| C3 | `:54-59`: `C3=met named=N present=M missing=0`, entering 14/55/41/extra0; top table `:18` says 15/55 | `C3=met|unmet named=N present=M missing=K extra=E rev=...` | controls `:49-52`: 14/55/41/extra0 | Counter docstring `:10` says entering 15/55/40; contract top table says 15; measured predicate and control say 14. Class/registry absent from graded condition; purpose only in deliverables. Final fixed 55 conflicts with a newly committed sweep tool. |

The controls labels are before receipts, not final worked receipts; no final receipt was available to compare. `extra=0` must remain explicit in a final C3 receipt even though the shorter target omits it. `QUALITY.md:1560-1569` makes literal command/output identity mandatory, not something an auxiliary report-composed string repairs.

Universal clauses not enumerated: C1 “resolves the lane's self-assessment claims” does not mean all prose assertions, every tally absent from pins, or score validity; C2 “one selftest arm per surviving mutant” and “three added arms / production unchanged” require a separate diff/mapping; C3 “every ... with its class and registry row” and purpose correctness are not tested, only path presence. No counter tests “no harm anywhere”; no such universal safety conclusion is warranted from three zero totals.

## 7. Harm and pin lifecycle

No necessary axis trade is established by these designs: read-only detection, counter selftest arms and bounded inventory can coexist. That is not a no-harm verdict. False authority in C3 would harm adjacency/calibration; vacuous C2 kills would harm operability/calibration; false-zero C1 would harm calibration. A canonical no-trade judge must reject actual harm rather than average it against coverage gains. These are fixable predicate defects and review obligations, not a justified tradeoff.

Pins create maintenance work. Frozen contract `:99-103` compares live selftests to pinned integers and treats chosen literals as stale throughout carriers including historical LOG text. A successor must preserve this round's pins/receipts as historical evidence, rederive current tool tallies at its own revision, and deliberately issue a new versioned pin set when expected counts genuinely change. Never silently change historical pins merely to force green; separate intentional selftest growth from an unreconciled self-assessment. No pins file/sweep implementation was available when discovered, so specific pin choices, actual replay behavior, total-one baseline and final zero sweep remain unverified.

## 8. Own defects and limitations

1. My first extraction helper printed the complete `git show` bodies for both r79 baseline revisions, producing unnecessary output. I corrected subsequent extraction to report hashes rather than full source. No output was fabricated.
2. I invoked the existing r79 `--selftest` directly before noticing its internal fixture helper performs `git init/add/commit` without the host-required explicit `rev-parse --show-toplevel` assertion. Its mutations were confined to S and S was removed, but this is my fixture-guard process defect; I cannot retroactively claim compliance. All other probes avoided git mutations entirely. No lane/fleet mutation was invoked.
3. The strongest attacks are explicitly function-level probes, not whole committed-fixture CLI receipts. They establish the precise grading holes at the recorded counter hashes; they do not establish an exploit was landed in the lane. Baseline CLI invocations and extracted real selftests are separately identified above.
4. No final worked-revision green selftest, final mutation total, final inventory or sweep implementation verification is claimed. No build/lint or unrelated verification was run. This is a first-falsifier report before final data, as assigned.

Self-evaluation (output quality, not canonical claim judgment): accuracy 4 (function-level scope and baseline provenance explicit; no final revision); completeness 4 (all five requested review dimensions covered; final receipts unavailable); clarity 4 (separate attacks/receipts, but long report); actionability 4 (exact clauses supplied; freeze authority remains L1); conciseness 3 (full evidence makes this lengthy). Mean 3.8. Highest-impact improvement is to put the baseline-green and metadata-scope clauses into the authoritative contract/counter/receipt together before any scoring, not patch a receipt afterward.
