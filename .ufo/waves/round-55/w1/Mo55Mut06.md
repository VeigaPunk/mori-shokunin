# Mo55Mut06 — counter selftest mutation probe

Scratch: `/fast/scratch/hyaku/mori-r55/Mo55Mut06/lane` (removed after probe). No lane production file was modified.

## Probe

- Target: C1 `derive()` changed-status branch, scratch `count-c1.py:237-238`; the branch returns `("changed", True)` when a compared v7.2 piece differs and is not found in the v7.3 copy.
- Mutant: replaced the predicate `if "changed" in st:` with `if "changed" in []:`. This makes changed status unreachable while retaining the return body.
- Detector: `python3 .ufo/waves/round-55/count-c1.py --selftest`, invoked from the scratch lane copy; same bounded detector on pristine, mutant, and restored bytes.

## Evidence

- Pristine output: `C1_SELFTEST pass=44 fail=0`, exit 0. Counter SHA-256 `e30658be34bfbf866860b20c9bde4117d467e351bb79e523131424cd5061e20b`.
- Mutated output: `FAIL witness met (scope 78)`; `FAIL changed row at v7.2 numbers still derives changed (block absent in v7.3)`; `FAIL reused row opened 2026-10-26 accepted`; `FAIL last line wins (stale then holds)`; `FAIL derive changed`; `C1_SELFTEST pass=39 fail=5`, exit 1. Mutant SHA-256 `db8b07c8589fa1379ba00e272abb7e495cddab8937f8686d2237c1bcf3bef90c`.
- Restored output: `C1_SELFTEST pass=44 fail=0`, exit 0. Restored counter SHA-256 equals pristine exactly: `e30658be34bfbf866860b20c9bde4117d467e351bb79e523131424cd5061e20b`.
- Scratch directory removal was included in the successful final command.

## Verdict

**Killed.** The selftest detects the behavior-bearing changed-status branch mutation (including its unit check and full witness behavior). Other predicate branches were not probed; no inference about their mutation coverage.

## Findings

- **Informational** — The changed-status branch mutant is killed by the frozen C1 selftest; outputs and byte hashes above are the evidence. Source branch location: `count-c1.py:237-238`; test definitions: `checks/selftest-c1.py:78-91,112-115,201-207`.
