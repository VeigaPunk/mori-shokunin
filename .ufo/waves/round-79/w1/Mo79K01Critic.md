# Mo79K01Critic — C2 independent falsification

## 1. Scope and outcome

Review axes: operability, calibration, freshness. Derivation axes: coverage, operability, depth, freshness, calibration, adjacency.

Requested review classification: **holds-with-named-limit**, for the proposed Last-change cells, not an admission or a landed-revision verdict. No canonical judge was invoked. The candidate matches all six independently derived expectations. The frozen entering counter is unmet with five mismatches, so doing nothing does not reach the target. Final committed integration was not available or tested in this seat.

Named, checkable limit: P-C2 does not establish Evidence-pointer existence, provenance, or agreement with the new leading closure. In particular the round-19 lane spotcheck is absent, yet adjacency passes; an in-memory candidate with that nonexistent file as its Evidence pointer still returns met. This is a predeclared scope tradeoff, not grounds to pretend P-C2 failed. The canonical judge must decide whether the limited improvement is admissible.

## 2. What I did (numbered)

1. Read the frozen contract, SCORECARD axes and round-78 tail, QUALITY 159/161/162/163, and SKILL registry. Read the counter before calling it. No counter selftest was invoked (its fixtures mutate git and were unnecessary to this assignment).
2. Independently selected highest admitted mori improved/harmed rounds through 78 using Python JSON parsing, without calling the counter's expectations function. Printed every mori round for every axis, selected or rejected with reasons; grouped rendering below retains every round.
3. Read the entering SCORECARD using git show, parsed its cells independently, and read the candidate table after it appeared. All six candidate “current cell” values equal the entering values.
4. Ran the entering counter CLI explicitly against the specified lane and manifest. Parsed the candidate independently, then additionally exercised the frozen grade function against an in-memory SCORECARD with only Last-change replacements. No fixture repo or lane SCORECARD edits.
5. Tested the actual round-19 path on disk and at entering; both absent. Replaced just adjacency's Evidence pointer in memory with that nonexistent path and exercised grade again.
6. Removed my scratch and accidental import bytecode. Only this report remains from my seat.

## 3. Commands and evidence

Python Eval was used as the command runner for read-only derivation and in-memory probes. Absolute path variables in the following executed expressions:

```python
root = pathlib.Path('/home/vgpnk/Projects/shokunin/mori-shokunin')
mp = root.parent / 'MANIFEST.json'
rev = '84c6cbc3b47c536a504aaee329c77897d389935e'
mb = mp.read_bytes()
manifest = json.loads(mb)
records = [r for r in manifest['rounds'] if r.get('lane') == 'mori']
# For each axis, descending round order; reject when:
if r.get('admitted') is not True: reasons.append('not_admitted_true')
if n > 78: reasons.append('beyond_78')
if v not in ('improved','harmed'): reasons.append('verdict_'+v)
# First row with no rejection reasons is N*; later qualifying rows are lower.
```

This derivation uses boolean true exactly, rather than the counter's truthiness filter. Observed expectations agree. Grouped output (all rejected candidate rounds retained, not just selected maxima):

```text
AXIS coverage
REJECT verdict_unchanged: 78,76,75,74,73,72,71,70,69,68,67,66,65,64,63,62,54,52,51,50,49,48,46,44,43,41,38,37,31,28,22,21,19,18
REJECT not_admitted_true,verdict_unchanged: 77,61,60,59,58,57,55,45,42,40,35,33,32,30,29,27
SELECT improved: 56
REJECT lower_than_selected improved: 53,47,26,25,24,16,15,14,12
REJECT verdict_absent: 39,36
REJECT not_admitted_true,verdict_unprovable: 34,23
REJECT not_admitted_true: 20,17,13
AXIS operability
SELECT improved: 78
REJECT not_admitted_true,verdict_unprovable: 77,60,42,40
REJECT verdict_unchanged: 76,75,74,68,66,65,64,62,54,53,52,50,49,48,46,26,25,24,22,21,19,16,15,14,12
REJECT lower_than_selected improved: 73,72,71,70,69,67,63,56,51,47,44,43,41,39,38,37,36,31,28,18
REJECT not_admitted_true: 61,45,17,13
REJECT not_admitted_true,verdict_unchanged: 59,58,57,55,35,34,33,32,30,29,27,23,20
AXIS depth
REJECT verdict_unchanged: 78,72,53,46,43,37,28,26,25,24,22,21,19,18,16,15,14
REJECT not_admitted_true: 77,57,45,42,30,27
SELECT improved: 76
REJECT lower_than_selected improved: 75,74,73,71,70,69,68,67,66,65,64,63,62,54,52,51,50,49,48,47,44,41,39,38,31,12
REJECT not_admitted_true,verdict_unchanged: 61,55,35,34,32,29,23,20,17,13
REJECT not_admitted_true,verdict_unprovable: 60,40,33
REJECT not_admitted_true,verdict_unprovable-but-better: 59,58
REJECT verdict_absent: 56,36
AXIS freshness
SELECT improved: 78
REJECT not_admitted_true: 77,20
REJECT lower_than_selected improved: 76,75,74,72,66,65,64,54,53,28,26,21
REJECT verdict_unchanged: 73,71,70,69,68,67,63,62,52,51,50,49,48,47,46,44,43,41,38,37,31,25,24,22,19,18,16,15,14,12
REJECT not_admitted_true,verdict_unchanged: 61,60,59,58,57,55,45,42,40,35,34,33,30,29,27,23,17,13
REJECT verdict_absent: 56,39,36
REJECT not_admitted_true,verdict_unprovable-but-better: 32
AXIS calibration
SELECT improved: 78
REJECT not_admitted_true,verdict_unchanged: 77,58,57,55,40,33,32,30,27,13
REJECT lower_than_selected improved: 76,75,74,73,72,71,69,68,63,62,52,50,49,48,47,46,44,43,41,39,38,37,25,24,22,21,19,18,12
REJECT verdict_unchanged: 70,67,66,65,64,54,53,51,31,28,26,16,15,14
REJECT not_admitted_true: 61,60,59,45,42,29,23,20,17
REJECT verdict_absent: 56,36
REJECT not_admitted_true,verdict_unprovable: 35
REJECT not_admitted_true,verdict_unprovable-but-better: 34
AXIS adjacency
REJECT verdict_unchanged: 78,76,75,74,73,72,71,70,69,68,67,66,65,64,63,62,54,53,52,51,50,49,48,47,46,44,43,41,38,37,31,28,26,25,24,22,21,16,15,12
REJECT not_admitted_true,verdict_unchanged: 77,61,60,59,58,57,55,45,42,40,35,34,33,32,30,29,27,23,20
REJECT verdict_absent: 56,39,36
SELECT improved: 19
REJECT lower_than_selected improved: 18,14
REJECT not_admitted_true: 17,13
```

Exact subprocess commands executed:

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 84c6cbc3b47c536a504aaee329c77897d389935e:SCORECARD.md
git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e 84c6cbc3b47c536a504aaee329c77897d389935e:corpus/lessons/round-19-verifier-spotcheck.md
python -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/count-c2.py 84c6cbc3b47c536a504aaee329c77897d389935e --repo /home/vgpnk/Projects/shokunin/mori-shokunin --manifest /home/vgpnk/Projects/shokunin/MANIFEST.json --scratch /fast/scratch/hyaku/mori-r79/mo79k01critic
```

The git show returned rc 0; its full output was parsed, not inferred from the contract's abbreviated before-list. Selected output from the derivation/probes, including byte bindings:

```text
MANIFEST sha256=86a82240bbb183b17811b9974de1cad83bd9c58a9b2f84a2a4b310a9d373f1b7

CANDIDATE sha256=4161ad1b83ecb3a36ed4f849f6f4245d749c8e5a7319cf92ab16e49e97bff409
ENTERING SCORECARD sha256=a4a488c2355a7389db8c5db24ba0efa347eb3f1fa154de59459abeab331a5c69
CANDIDATE current_matches_entering coverage=True
CANDIDATE current_matches_entering operability=True
CANDIDATE current_matches_entering depth=True
CANDIDATE current_matches_entering freshness=True
CANDIDATE current_matches_entering calibration=True
CANDIDATE current_matches_entering adjacency=True
COMPARE coverage entering=47 candidate=56 expected=(56, 'improved') candidate_match=True
COMPARE operability entering=51 candidate=78 expected=(78, 'improved') candidate_match=True
COMPARE depth entering=51 candidate=76 expected=(76, 'improved') candidate_match=True
COMPARE freshness entering=28 candidate=78 expected=(78, 'improved') candidate_match=True
COMPARE calibration entering=50 candidate=78 expected=(78, 'improved') candidate_match=True
COMPARE adjacency entering=19 candidate=19 expected=(19, 'improved') candidate_match=True
ADJACENCY disk_exists=False
ADJACENCY entering_cat_file rc=128 stderr=fatal: path 'corpus/lessons/round-19-verifier-spotcheck.md' does not exist in '84c6cbc3b47c536a504aaee329c77897d389935e'
COUNTER sha256=fed9a8292158b6d69e9d786d48fcbed02cb30772b5a5cb4e0386d0b034472290
FROZEN grade candidate Last-change-only in_memory={"errors": 0, "items": [["coverage", "round_56_improved", "round_56_improved", "ok"], ["operability", "round_78_improved", "round_78_improved", "ok"], ["depth", "round_76_improved", "round_76_improved", "ok"], ["freshness", "round_78_improved", "round_78_improved", "ok"], ["calibration", "round_78_improved", "round_78_improved", "ok"], ["adjacency", "round_19_improved", "round_19_improved", "ok"]], "met": true, "mismatches": 0, "rows": 46}
FROZEN grade missing_Evidence_pointer in_memory={"errors": 0, "items": [["coverage", "round_56_improved", "round_56_improved", "ok"], ["operability", "round_78_improved", "round_78_improved", "ok"], ["depth", "round_76_improved", "round_76_improved", "ok"], ["freshness", "round_78_improved", "round_78_improved", "ok"], ["calibration", "round_78_improved", "round_78_improved", "ok"], ["adjacency", "round_19_improved", "round_19_improved", "ok"]], "met": true, "mismatches": 0, "rows": 46}
ENTERING COUNTER rc=1
axis coverage cell=round_47_improved expect=round_56_improved state=mismatch
axis operability cell=round_51_improved expect=round_78_improved state=mismatch
axis depth cell=round_51_improved expect=round_76_improved state=mismatch
axis freshness cell=round_28_improved expect=round_78_improved state=mismatch
axis calibration cell=round_50_improved expect=round_78_improved state=mismatch
axis adjacency cell=round_19_improved expect=round_19_improved state=ok
C2=unmet axes=6 mismatches=5 errors=0 rows=46 through=78 rev=84c6cbc3b47c

```

In-memory probe operations executed after loading the counter with importlib:

```python
for a in axes:
    patched = patched.replace('| '+old[a]+' |', '| '+proposed[a]+' |', 1)
g = counter.grade(patched, str(mp), 78)
# For the adjacency row only:
parts = l.split('|')
parts[3] = ' `corpus/lessons/round-19-verifier-spotcheck.md` '
lines[i] = '|'.join(parts)
g2 = counter.grade('\n'.join(lines), str(mp), 78)
```

These are function-level probes, not successful CLI runs at a committed candidate revision. Disk existence was tested with `path.exists()` on the absolute round-19 path. Candidate and counter hashes above bind the reviewed bytes; MANIFEST is a live external input, so the findings apply to its recorded hash, not an unspecified future fleet tip.

## 4. Counterexamples and smallest safe correction

### (a) Leading-round semantics

For `round 51 (improved, score held); ...`, the first `round N` is the intended closure attribution, despite no score movement. The r50 correction explicitly defines that distinction. Independently parsed entering operability and depth both lead with 51, not 47/49. The contract's prose before-control list says 47/47/49/28/50/19, which is stale for operability/depth; the actual CLI reports 47/51/51/28/50/19. This documentation defect does not kill C2: the measured entering state still has five mismatches. Smallest correction is a new report erratum naming those actual rounds, not an edit to the frozen contract.

### (b) Missing evidence passes

The missing round-19 spotcheck is the concrete counterexample to any broader claim of closure-evidence reconciliation. The actual adjacency Evidence cell already honestly says there is no lane spotcheck and cites fleet MANIFEST instead; absence is not proof of a fabricated current pointer. Nevertheless, planting the nonexistent pointer into a fully conformant in-memory candidate leaves mismatches=0. The predicate cannot distinguish honest fleet-only provenance from a broken local pointer, and unchanged Evidence cells can still describe older “latest” closures after new leading cells land.

Impacted axes: calibration (scope of the reconciliation), operability (traceability), freshness (old Evidence descriptions). No numeric axis grade is asserted by this critic.

Smallest safe correction in this wave: keep the frozen predicate intact, retain honest fleet-only wording for adjacency, and explicitly report that only Last-change metadata is reconciled. Do not claim Evidence cells are current or locally validated. Evidence checking would require a separately frozen claim, not a widened success assertion here.

### (c) Premature saturation / do-nothing

The strongest available do-nothing counterexample fails to falsify the claim: entering is `C2=unmet axes=6 mismatches=5 errors=0 rows=46 through=78`. Only adjacency already conforms. The candidate corrects five distinct rows rather than claiming an already-saturated whole table.

## 5. Negative results, own defects, cleanup

- No incorrect candidate leading round or verdict found; candidate current-cell equality checked six times, all True.
- No claim of committed after-state, full Evidence reconciliation, source freshness, score increase, or canonical admission. No host remediation, network requests, credential access, installs, or tool upgrades.
- My initial reads incorrectly used shell ls/grep/awk/cat/head and copied the counter into scratch instead of using the specialized read/search tools. I caught this against the tooling directive and switched to specialized tools and Python Eval. These were process defects, not independent evidence of repository correctness.
- I also emitted verbose planning and read the godspeed skill late; neither is part of the claim evidence.
- Importlib created `count-c2.cpython-314.pyc` under the counter directory, violating the intended read-only boundary. Glob caught the artifact; I removed my own bytecode and the now-empty cache directory. Future read-only loads must set `sys.dont_write_bytecode=True` before importing, or execute compiled source in memory. No counter source was edited.
- Cleanup command: `S=/fast/scratch/hyaku/mori-r79/mo79k01critic; trap 'rm -rf -- "$S"' EXIT; rm -- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/__pycache__/count-c2.cpython-314.pyc && rmdir -- /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-79/__pycache__ && printf 'Removed own import bytecode and cache directory; scratch cleanup armed on exit\n'` returned rc 0 and printed that message. The shell exited and executed the trap; no scratch tree intentionally retained.

Self-evaluation: accuracy 4 (candidate function probe is not committed integration); completeness 4 (all assigned attacks covered; final landing unavailable); clarity 4 (full rejection inventory is dense); actionability 4 (scope correction named, canonical decision reserved); conciseness 4 (evidence inventory retained for reproducibility). Overall 4.0/5. Highest-value improvements: preserve the limited claim label; avoid import side effects; keep tooling reads specialized. A reader can check every named limit above.
