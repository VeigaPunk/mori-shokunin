# OracleHarness — scoped findings

## Files changed

- `.ufo/waves/round-20/build/OracleHarness/c2-oracle.py` — independent stdlib black-box harness. It reads the frozen case file, builds one isolated temporary lane fixture for each case, launches `python3 TOOL scan ...` as a subprocess when the tool exists, and checks each case's expected keys; unsupported expectations become explicit issues (`c2-oracle.py:312-331`). The scan invocation passes explicit `--out` and the fleet root only for the misrooted fixture (`:158-170`). Fixture definitions cover the frozen case IDs (`:46-155`), including malformed JSON (`:94-99`) and repeat-scan determinism (`:143-151`). It does not import or read the candidate tool source.
- `.ufo/waves/round-20/build/OracleHarness/c2-before-candidate.json` — requested absent-capability baseline result, schema `mori-r20-c2-oracle-v1`.

## Behavior and evidence

The harness loads `.ufo/waves/round-20/frozen/c2-expected.json` relative to its own location and writes the requested output schema and counts (`c2-oracle.py:391-414`). Its output records per-case expected/observed values and issues. For an absent tool it still constructs each fixture, marks every case `capability_absent`, and does not attempt a subprocess.

- Frozen input contains 14 cases: `.ufo/waves/round-20/frozen/c2-expected.json:6-20`.
- Requested tool presence check returned `absent` for `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-wave-settlement.py`.
- Final command run: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/OracleHarness/c2-oracle.py --tool /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-wave-settlement.py --out /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/build/OracleHarness/c2-before-candidate.json` — exited successfully.
- Retained output counts (`c2-before-candidate.json`): `matched=0`, `mismatched=0`, `capability_absent=14`; per-case status summary was `capability_absent: 14`.
- SHA-256 of `c2-before-candidate.json`: `e0163e2f67e7b36d3474128ee315d0da41bb79f08adc195d62d5c505d8820f5b`.

The first harness invocation exited 1 because malformed-dispatch fixture text formatting raised `ValueError: unmatched '{' in format spec`; that fixture construction was corrected at `c2-oracle.py:99`, and the final invocation above replaced the output artifact with the 14-case absent-capability result.

## Risks / blockers

- Candidate behavior remains unobserved because the requested tool was absent; the baseline is capability-absent, not evidence that any candidate case passes. [INFERENCE]
- No build, lint, or broader test command was run; the only execution was the expressly requested oracle baseline.
