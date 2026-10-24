# CritC2ContentFree — P-C2 corpus-binding counterexamples

Attacks: C2's claim that the committed corpus binds the two hardening policies and carries a live sweep receipt. This is a scoped critic result, not an admission or a canonical-runtime judgment.

## Axes

- **Freshness** (C2's declared axis): a summary sentence can substitute for the sweep's row evidence.
- **Depth**: source/commit/arm tokens can substitute for located, source-grounded knowledge.
- **Calibration**: all checks still print PASS after those evidence fields lose their substance.
- **Operability**: a capability's evidence link can be nonexistent.
- Coverage and adjacency are not challenged by these witnesses.

## Construction and provenance

Scored parent: `e57c58b57c025364e79d130fbdf764d2674d83d6`. Each scratch commit inherits that entire tree and changes only its listed artifact(s); the real tool and README remain unchanged. Scratch Git objects/indexes/refs live under `/fast/scratch/hyaku/mori-r37/CritC2ContentFree/`; the scratch bare repository reads the lane object store through a read-only alternate. No lane Git state or source artifact was mutated.

Commands below use the lane as cwd. `$S` denotes `/fast/scratch/hyaku/mori-r37/CritC2ContentFree`; `$LANE` denotes the lane root. These variables abbreviate the absolute paths supplied to the executed commands.

Counter provenance measurements:

```text
command: git -C "$LANE" rev-parse e57c58b57c025364e79d130fbdf764d2674d83d6 e57c58b57c025364e79d130fbdf764d2674d83d6:.ufo/waves/round-37/count-c2.py
observed:
e57c58b57c025364e79d130fbdf764d2674d83d6
6213cf9a5ada709da8cd867581782737b2f06c71

command: git -C "$LANE" hash-object .ufo/waves/round-37/count-c2.py
observed:
6213cf9a5ada709da8cd867581782737b2f06c71
```

Fixture generation:

```text
command: python3 "$S/build-fixtures.py"
observed (revision/path lines):
shape-a revision=7f45924e20ef3114859539f4ec51aeb917792a86 modified=corpus/knowledge/source-drift-hardening-r37.md
shape-b revision=7bc7986e9acb8ac91da5bda8396c778fd4ff1f13 modified=SCORECARD.md
shape-c revision=928726789e342810a4d3a3c8eb3a65151c8f109a modified=.ufo/waves/round-37/evidence/drift-live-r37.txt
shape-abc revision=c7e9a944f4a65d0c226c143387e8adaef5f481d2 modified=corpus/knowledge/source-drift-hardening-r37.md,SCORECARD.md,.ufo/waves/round-37/evidence/drift-live-r37.txt
All other tree entries inherited unchanged from e57c58b57c025364e79d130fbdf764d2674d83d6
```

The four counter runs below were launched concurrently. Every run printed PASS for all eight checks and `C2=met`. Relevant output is quoted per run; the combined run's complete stdout is included below.

## (a) Knowledge: right strings, no located quote — ADMITTED

Entire replacement `corpus/knowledge/source-drift-hardening-r37.md`:

```text
# source-drift hardening
huge_cap redirect_private_refused 8ff9bba S221
```

There is no policy explanation, `source:` record, locator, quote, or evidence pointer. The source ID is genuinely from this round, so this does not rely on an unrelated-ID trick.

```text
command: env TMPDIR="$S/tmp" python3 .ufo/waves/round-37/count-c2.py 7f45924e20ef3114859539f4ec51aeb917792a86 --repo "$S/fixture.git"
observed (selected stdout):
check knowledge      PASS (present=True rows=['S221'] cited_commit=True)
C2=met
```

**Catching check: none. P-C2 admits this shape.** At `.ufo/waves/round-37/count-c2.py:187-193`, `knowledge` requires only file presence, two arm substrings, the commit substring, and any `S2\d\d` token. It does not inspect a quote or locator, or follow a citation. No other check consumes this entry. This is token presence, not evidence of a grounded knowledge entry.

## (b) Capability: names tool, evidence points nowhere — ADMITTED

Replace the capability row at `SCORECARD.md:2059`, preserving the rest of SCORECARD:

```text
| round-37 C2 | source-drift re-fetch probe | Mentions tools/mori-source-drift.py only. | [evidence](.ufo/waves/round-37/evidence/CONTENT_FREE_MISSING_RECEIPT.txt) | 37 |
```

The tool name appears only in the description; the evidence field points to an absent artifact. The builder established that absence before constructing the commits:

```text
command: git -C "$S/fixture.git" cat-file -e e57c58b57c025364e79d130fbdf764d2674d83d6:.ufo/waves/round-37/evidence/CONTENT_FREE_MISSING_RECEIPT.txt
observed: exit=128; stdout empty
stderr: fatal: path '.ufo/waves/round-37/evidence/CONTENT_FREE_MISSING_RECEIPT.txt' does not exist in 'e57c58b57c025364e79d130fbdf764d2674d83d6'
```

That path was not added by any fixture.

```text
command: env TMPDIR="$S/tmp" python3 .ufo/waves/round-37/count-c2.py 7bc7986e9acb8ac91da5bda8396c778fd4ff1f13 --repo "$S/fixture.git"
observed (selected stdout):
check capability     PASS (rows=1 names_tool=True)
C2=met
```

**Catching check: none. P-C2 admits this shape.** At `.ufo/waves/round-37/count-c2.py:195-200`, `capability` selects a pipe-prefixed line containing the capability name, then searches the entire last matching line for the tool path. It neither parses the evidence cell nor resolves its pointer. `tool_present` proves the actual tool exists, not that this row points to evidence. The corpus's existing pointer rule at `corpus/QUALITY.md:17-18` is not exercised by this counter.

## (c) Live receipt: sentence only, no row lines — ADMITTED

Entire replacement `.ufo/waves/round-37/evidence/drift-live-r37.txt`:

```text
MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162
```

This removes every per-row state line and the exit record. The real receipt has the summary at line 221 and `EXIT=1` at line 222; the tool explicitly prints one state line per row (`corpus/knowledge/source-drift-hardening-r37.md:16-21`).

```text
command: env TMPDIR="$S/tmp" python3 .ufo/waves/round-37/count-c2.py 928726789e342810a4d3a3c8eb3a65151c8f109a --repo "$S/fixture.git"
observed (selected stdout):
check live           PASS (present=True sentence=True)
C2=met
```

**Catching check: none. P-C2 admits this shape.** At `.ufo/waves/round-37/count-c2.py:208-211`, `live` is solely file presence plus containment of `LIVE_SENTENCE` (the published constant at line 49). There is no row parser, completeness/tally check, exit check, or provenance check. Selftest row validation at `tools/mori-source-drift.py:384-396` applies to its generated selftest output, not this committed receipt.

## Strongest counterexample: all three simultaneously

```text
command: env TMPDIR="$S/tmp" python3 .ufo/waves/round-37/count-c2.py c7e9a944f4a65d0c226c143387e8adaef5f481d2 --repo "$S/fixture.git"
observed (complete stdout):
P-C2: at revision R, tools/mori-source-drift.py passes its selftest with the named arms `huge_cap` and `redirect_private_refused`, each of those arms fails in a copy with its policy removed (4 MiB read cap; post-redirect public-destination policy), and the committed corpus binds the hardening (knowledge entry citing this round's source rows and commit 8ff9bba, a SCORECARD capability row, two README coverage-map rows) with the round's live sweep receipt present.
check tool_present   PASS (path=tools/mori-source-drift.py)
check selftest       PASS (exit=0 arms=[('exit_code', 'PASS'), ('huge_cap', 'PASS'), ('missing_sources_exit2', 'PASS'), ('redirect_private_refused', 'PASS'), ('row_states', 'PASS'), ('summary', 'PASS')])
check cap_kill       PASS (exit=1 huge_cap=FAIL)
check redirect_kill  PASS (exit=1 redirect_private_refused=FAIL)
check knowledge      PASS (present=True rows=['S221'] cited_commit=True)
check capability     PASS (rows=1 names_tool=True)
check readme         PASS (r36_row=True r37_row=True)
check live           PASS (present=True sentence=True)
C2=met
```

This preserves the genuine policy tests and their mutation kills while removing grounding, a resolving capability-evidence pointer, and all live row evidence together. It is a corpus-binding discrimination defect, not a counterexample to the two fetch policies themselves. It does not establish that the actual scored tip's substantive artifacts are false; it establishes that this measurement cannot require their substance.

## Smallest safe correction (recommendation only)

1. Add these three named content-free controls to the binding measurement. Require each to be rejected; do not classify their current passes as successful corpus binding.
2. Replace only the implicated presence tests: require a structured claim-to-source/locator/quote binding that resolves into the committed source evidence; parse the capability's evidence cell and require its referenced artifact to exist at the measured revision; parse receipt row-state records and require unique IDs, completeness, and summary agreement (including the recorded exit). Row/tally integrity alone still would not prove live provenance, so do not claim it would.
3. The contract is frozen (`.ufo/waves/round-37/contract.md:4-6`): any strengthened predicate/counter needs a new version/re-freeze, not an in-place reinterpretation of P-C2. The current wording and implementation deliberately stop at token/presence checks; this is a fixable measurement/target weakness, not a demonstrated no-harm tradeoff or authority to change the round's judgment.

No remediation performed. No tools installed or updated.

VERDICT: FAIL — all three content-free shapes are admitted; implicated checks: `.ufo/waves/round-37/count-c2.py:187-211`.
