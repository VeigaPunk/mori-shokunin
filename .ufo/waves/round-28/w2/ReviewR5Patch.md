# ReviewR5Patch — wave 2, attack on routed r25 R5 fix for tools/mori-routed-r24.py

Verdict: **holds (carry is correct; the named draft is missing and every R5 defect is still live, one worse than routed).**

## What was attacked

`git diff 6ebd518f f2de0eedcd60d2e354da75265ea6122bc3896073 -- tools/mori-routed-r24.py tools/fixtures tools/mori-routed-check.py` is **empty** (`git diff --stat`, zero output). `SKILL.md` diff is only the S096/S145 and S127/S148-150 reader repoints; no selftest file under `tools/` exists at the tip (`git ls-tree -r f2de0ee` grep `routed` → only `tools/mori-routed-check.py`, `tools/mori-routed-r24.py`). The wave-1 draft `.ufo/waves/round-28/w1/FixR5RoutedSelftest.md` is **absent** at the tip and in the w1/ listing — the FixR5 seat (`agent://MoriR28.FixR5RoutedSelftest`) is still running ("build the sandbox implementation — first the fixture files"); its sandbox `/fast/scratch/hyaku/mori-r28/FixR5RoutedSelftest/lane` is a clean clone at `6ebd518f` with zero modified files.

## Carried: right call

Contract `.ufo/waves/round-28/contract.md:70-71`: r25 R5 lands "only when a non-author check passes; otherwise carried with the reason." With no patch and no report at `f2de0ee`, carrying is the only compliant state. Findings below show all six R5 items remain reproducible, so nothing was silently declared fixed. The carry reason is not yet recorded in LOG.md (LOG tail at `f2de0ee` ends at the C2 freeze batch) — it is owed by the closing batch along with the R1 reason.

## R5 item status at the attack revision (all still broken)

R5 text: `corpus/lessons/round-25-verifier-spotcheck.md:189-193`.

1. **Registry rows** — already satisfied pre-round: `SKILL.md:717` (mori-routed-r24) and `:718` (mori-job-runway) exist at `6ebd518f`; added in round 26, nothing to fix.
2. **Committed self-test** — absent; no `--selftest` flag in the tool (`tools/mori-routed-r24.py:896-902` accepts only `--repo/--rev/--rerun`), no fixtures dir. OPEN.
3. **D1 forged PASS** — reproduced: in a sandbox clone I sabotaged `tools/fixtures/mori-pressure/cases.json` (case P01 expects `PRESSURE_STALLED`; real run `FAIL 10/11`), committed it (`21fa8aec`), then committed an evidence file claiming `PASS 12/12` with the true `tool_blob`/`fixtures_tree` of `21fa8aec` (`6d7bf1d3`). Tool at `6d7bf1d3`: exit 0, `status: held`, D1 reasons `[]`. **With `--rerun` the same: exit 0, held**; the rerun (`body_byte_equal: false`, `exit: 1`) lands only in `detail`, matching the code comment "The rerun is reported only: it never decides whether D1 holds" (`tools/mori-routed-r24.py:511`). R5 said "only --rerun detects a forged PASS" — measured, even --rerun does not flip the verdict. OPEN, worse than routed.
4. **D2 skipped headings** — reproduced: appended `## refreshed on each read` (a `D2_NEGATIVE_PATTERNS` phrase, `mori-routed-r24.py:110`) as a heading to `corpus/knowledge/system-pressure-r24.md` in the same forge clone (`cc36d855`); tool exit 0, D2 held. Cause: `outside_text` is built from block *bodies* only (`:589-599`); headings never enter it. OPEN.
5. **D3 beside uncorrected `PASS 6/6`** — code-confirmed: the marker is just `PASS total/total` from the base case count (`:772`) plus a hex token; no pass/fail distinction, exactly as routed. OPEN. (Not separately exercised — the D3 scan shape was already exercised benignly in the runs above.)
6. **Missing baseline exits 1, not 2** — reproduced: `git clone --depth 4` of the lane (no `28b79d3d`/`4f05dd5a` objects; `git cat-file -t` → "could not get object info"); tool exits **1** `status: failed` with `base_knowledge_entry_unreadable`, `supplementary_cases_unreadable`, `base_scorecard_unreadable`. The spec (`:64-65`) reserves 1 for failed checks and 2 for unreadable objects; a missing baseline is the latter. OPEN.
7. **Promisor clone gets objects written** — code-confirmed: `_git_env()` (`:186-196`) sets `GIT_OPTIONAL_LOCKS=0` but not `GIT_NO_LAZY_FETCH`; `cat-file`/`ls-tree` on a filtered clone lazy-fetches into `.git/objects`, breaking the "read-only" claim in the docstring (`:67`). Dynamic repro not run: `file://` transport refuses `--filter` ("filtering not recognized by server, ignoring") and bounds forbid touching host git services. OPEN [INFERENCE for the fetch-writing part; the missing env var is committed code].
8. **Sub-directory `--repo` changes results** — reproduced on the lane itself: `--repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev f2de0ee` → exit 0 `held 4/4`; `--repo .../mori-shokunin/tools` same rev → exit **1**, D1 `pressure_tool_missing, pressure_fixtures_missing`. Cause: `ls-tree -- <path>` pathspecs are cwd-relative (`:259`); `cat-file rev:path` is root-relative, so the two disagree under a subdir. OPEN.

## Findings for the integrator

- The wave-2 spec and my assignment both cite `w1/FixR5RoutedSelftest.md`, which does not exist because the executor is still mid-flight; reviewing the draft was impossible — reviewed the committed state instead (the spec's empty-diff branch).
- When the fix lands, its selftest must cover the **measured** shapes above, including: `--rerun` must fail the verdict on `body_byte_equal: false` (currently report-only), heading-only banned phrases, baseline-absent → exit 2, subdir `--repo`, and lazy-fetch suppression (`GIT_NO_LAZY_FETCH=0` or equivalent).
- Unrun checks: no promisor fetch repro; D3 not separately mutanted; no claim about the eventual patch quality (none exists yet).

Tooling: none installed; sandbox clones under `/fast/scratch/hyaku/mori-r28-w2/ReviewR5Patch` (forge/shallow/partial removed after runs).
