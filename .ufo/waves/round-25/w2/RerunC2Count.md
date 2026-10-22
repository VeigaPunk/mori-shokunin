# RerunC2Count: C2 selftest rerun, freeze order, default-scope check

Seat: MoriR25.RerunC2Count (leaf, read-only on the lane). Scope: rerun C2's selftest from fresh clones, verify the frozen cases blob and freeze order, and verify the supplementary file is not loaded by default.

## Verdict

**Held for the declared after-value, the freeze and the default scope. Weakened in coverage (finding 1 Medium, finding 2 Low), and one wording issue (finding 3 Low).**

- The declared after-value re-derives. From fresh clones, `python3 -I -B tools/mori-job-runway.py --selftest` prints `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` and exits 0 at the lane tip `e0e33c118e1eea2d40241a58861b7d0ad536e062` (`e0e33c1`) and at the first tool commit `09f55b628c21399fc6e6f00bd795d1510f9efb83` (`09f55b62`).
- The freeze holds. `tools/fixtures/mori-job-runway/cases.json` is git blob `48df844a22d74a57204f55a62e54760c7038c60f` at `7634be75`, at `09f55b62` and at the tip. The only commit that ever touched it is `7634be7`. `7634be75` has no `tools/mori-job-runway.py` (exit 128).
- The supplementary file is not loaded by default. Static reading, an audit-hook trace, strace, and deletion or corruption of the file all agree.
- Withdrawn from my first snapshot: the "C2 evidence file missing" point. It was true at lane tip `07a31ae8`. Since then `47b2b93` landed `runway-selftest.txt`, `runway-selftest-supplementary.txt` and `runway-live-run.txt`. They reproduce (finding 4).

## What I ran

- Lane HEAD moved during my run: `07a31ae8e22514bbc603afa13f2de7c8b2424cca` at the start, `e0e33c118e1eea2d40241a58861b7d0ad536e062` at the end. I re-ran everything at `e0e33c1` from a second fresh clone. Earlier results are noted where they differ.
- Private clones (not the lane): `/fast/scratch/hyaku/mori-r25/w2-RerunC2Count` (from `07a31ae8`) and `/fast/scratch/hyaku/mori-r25/w2-RerunC2Count-tip2` (from `e0e33c1`, `git status --porcelain --ignored` empty).
- `git archive` extracts under `/fast/scratch/hyaku/mori-r25/w2-RerunC2Count-x/`: `t0962` (09f55b62), `t7634` (7634be75), `tip` (07a31ae8), `tip2` (e0e33c1), plus scratch copies for perturbation.
- The lane was read only: `git rev-parse`, `git diff --stat`, `ls`, `sha256sum`. Nothing was written to the lane except this report. No jj command was run.

## Selftest results

| # | Revision | Tree | Command (cwd = tree root) | Output | Exit |
|---|---|---|---|---|---|
| 1 | `e0e33c1` (lane tip) | fresh clone 2 | `python3 -I -B tools/mori-job-runway.py --selftest` | `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21` | 0 |
| 2 | `e0e33c1` | `git archive` extract | same | `PASS 21/21` | 0 |
| 3 | `07a31ae8` (earlier tip) | fresh clone 1 | same | `PASS 21/21` | 0 |
| 4 | `09f55b62` (first tool commit) | `git archive` extract | same | `PASS 21/21` | 0 |
| 5 | `7634be75` (freeze) | `git archive` extract | same | `python3: can't open file ... mori-job-runway.py: No such file or directory` | 2 |
| 6 | `e0e33c1`, supplementary | fresh clone 2 | `... --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json` | `PASS 24/24` | 0 |

Label note: in my first batch I ran three commands under one working directory. Two of the three lines I labelled "tip" and "7634be75" actually ran in the `09f55b62` extract. Those lines are discarded. Rows 1 to 5 come from separately labelled calls.

## Freeze order (commands and outputs)

Read-only git against the private clones only.

```
git log --reverse --topo-order --format='%h | parents=%p | %cI | %s' 7634be75^..HEAD
git rev-list --count 7634be75^..HEAD                                  -> 33
git log --diff-filter=A --format='%h | %cI | %s' -- tools/fixtures/mori-job-runway/cases.json
   -> 7634be7 | 2026-10-22T06:49:49-03:00
git log --diff-filter=A --format='%h | %cI | %s' -- tools/mori-job-runway.py
   -> 09f55b6 | 2026-10-22T07:02:38-03:00
git log --diff-filter=A --format='%h | %cI | %s' -- tools/fixtures/mori-job-runway/supplementary-cases.json
   -> 9a3d511 | 2026-10-22T07:15:49-03:00
git log --format='%h' -- tools/fixtures/mori-job-runway/cases.json     -> 7634be7 (only)
git log --format='%h' -- tools/mori-job-runway.py                      -> fbecc59, 9a3d511, 09f55b6
git log --format='%h' -- tools/fixtures/mori-job-runway/supplementary-cases.json -> d3b7af2, 9a3d511
git merge-base --is-ancestor 7634be75 09f55b62   -> exit 0
git merge-base --is-ancestor 09f55b62 HEAD       -> exit 0
git merge-base --is-ancestor fbecc59 d3b7af2     -> exit 0
git merge-base --is-ancestor 47b2b93 HEAD        -> exit 0
git cat-file -e 28b79d3:tools/mori-job-runway.py                       -> exit 128 (the contract's "Before")
git cat-file -e 28b79d3:tools/fixtures/mori-job-runway/cases.json      -> exit 128
git cat-file -e 7634be75:tools/mori-job-runway.py                      -> exit 128
git cat-file -e 09f55b62:tools/fixtures/mori-job-runway/supplementary-cases.json -> exit 128
git rev-parse 7634be75:tools/fixtures/mori-job-runway/cases.json       -> 48df844a22d74a57204f55a62e54760c7038c60f
git rev-parse 09f55b62:tools/fixtures/mori-job-runway/cases.json       -> 48df844a22d74a57204f55a62e54760c7038c60f
git rev-parse HEAD:tools/fixtures/mori-job-runway/cases.json           -> 48df844a22d74a57204f55a62e54760c7038c60f
sha256 of those cases bytes (three revisions and lane working copy)    -> 7098b008d614e84c4328af96d15badef700ea84b75a43ba4a375264a01755fb4
git show 09f55b62:tools/mori-job-runway.py | sha256sum                 -> 08217582fdad69cf224bfc63d289c85196a96f3ee63ac10690eb4344cfbffe69
git rev-parse HEAD:tools/mori-job-runway.py                            -> 239dd8ebe630400a2739151260e482ad83dea459 (unchanged since fbecc59)
git diff --numstat 7634be75 HEAD -- .ufo/waves/round-25/contract.md    -> 101 0 (additions only since the freeze)
```

Order in words: the cases file and the contract were committed together at `7634be7` (06:49:49). The first tool commit is `09f55b6` (07:02:38), the fourth commit in the list and three commits after the freeze. Amendments A1 and A2 sit between the first tool commit and the first tool change (`9a3d511`). The last tool change is `fbecc59` (07:19:08). For the tool and the frozen cases, `d3b7af2` changes nothing; it touches only the supplementary file. The evidence commit is `47b2b93`. The clock text in the contract does not match these commit times (finding 3); the parent chain is the evidence I rely on.

## Supplementary file is not loaded by default

- Static (`tools/mori-job-runway.py`): `_cases_path()` (lines 505 to 514) resolves only `fixtures/mori-job-runway/cases.json`. The word "supplementary" appears only in the docstring (lines 59 to 60). The `--cases` option (lines 643 to 648) is the only route to it.
- Audit-hook trace (`audit-tip2-default.json`, default selftest at `e0e33c1`): the only file opened under `fixtures` is `cases.json`. No supplementary file, no `~/.omp`, no real omp binary, no subprocess, no socket. Writes go only to `/tmp/mori-job-runway-*` (plus the standard library's temp-directory probe).
- strace (`strace-tip2-default.txt`, 374 lines): one `openat` of `.../tools/fixtures/mori-job-runway/cases.json` (line 164). No supplementary open, one `execve`, no `connect`, no `.omp` path.
- Perturbation, default run, at `e0e33c1` copies: supplementary file deleted gives `PASS 21/21`, exit 0. Supplementary file replaced by invalid JSON gives `PASS 21/21`, exit 0.
- Explicit only: `--selftest --cases <supplementary>` gives `PASS 24/24`, exit 0. `--cases` without `--selftest` gives exit 2.

Result: held.

## What the 21/21 pins

Frozen file: 21 cases, ids J01 to J21, all unique. Every expect has the same six keys (`clamp`, `configured`, `effective`, `exit`, `setting_default`, `verdict`). Counted with python at `e0e33c1`:

| Field | Frozen 21 | Supplementary 24 |
|---|---|---|
| `verdict`, `effective`, `exit` | every case | every case |
| `configured.state` / `value` | 21 / 21 | 24 / 24 |
| `clamp.state` / `value` | 21 / 21 | 24 / 24 |
| `setting_default.state` / `value` | 21 / 21 | 24 / 24 |
| `clamp.sites` | 2 (J01, J11) | 20 |
| `setting_default.sites` | 0 | 0 |
| `schema` | 0 | 0 |
| `binary_sha256` | 0 | 0 |

Verdicts in the frozen set: `RUNWAY_CLAMPED` 6, `RUNWAY_UNKNOWN` 7, `RUNWAY_DEFAULT` 5, `RUNWAY_AS_CONFIGURED` 3.

Mutation probe (scratch copy of `e0e33c1`): one line changed, `tools/mori-job-runway.py:492`, `"sites": setting_default[2] + 5`.
- Frozen selftest: `PASS 21/21`, exit 0.
- Supplementary selftest: `PASS 24/24`, exit 0.
- Live payload (`--config` pointing at a nonexistent file, `--binary` reading omp's bytes only): `setting_default.sites` changes from 1 to 6.

So the selftest does not measure that field (finding 2).

## Findings

Severity is per finding. Smallest fix given for each.

### 1. Medium: a valid root flow mapping gives a wrong number with exit 0 (disclosed, not counted)

- Config text `{async: {maxJobs: 50}}` on one line. The tool reports `configured {absent, null}`, `setting_default {found, 100}`, `effective 100`, `RUNWAY_DEFAULT`, exit 0 (run with `--config` pointing at that file and `--binary /home/vgpnk/.local/bin/omp`).
- Bun 1.4.3, the parser omp embeds (per the wave-1 CriticC2Rules probe), parses the same text to `{"async":{"maxJobs":50}}` (`bun -e 'console.log(JSON.stringify(Bun.YAML.parse("{async: {maxJobs: 50}}\n")))'`). So omp would use 50. The tool states a number omp does not use, with exit 0.
- Why: rule 1 says `absent` when there is no `async:` line at column 0. The contract's literal wording forces that. Amendment A2's abstention list (`tools/mori-job-runway.py` docstring, lines 63 to 75) does not cover a root flow collection (first significant character `{` or `[`), a JSON-style root, or a quoted root key.
- Coverage: none of the 45 cases (21 frozen, 24 supplementary) starts with `{` or `[`. The knowledge entry `corpus/knowledge/harness-job-capacity-r25.md` line 211 discloses the case: a file written as a flow mapping "still reads `RUNWAY_DEFAULT`, effective 100 (a false number; …)". It is not in the after-value.
- Smallest fix: first a contract change, because the literal rule 1 says `absent`. Then the tool abstains (`malformed`, exit 2) when the first significant character is `{` or `[`, with one uncounted supplementary case pinning `RUNWAY_UNKNOWN`. None of the 21 frozen values moves. Until then the bound stays in the knowledge entry's verdict row, as it is now.

### 2. Low: the selftest does not measure `setting_default.sites`, `schema` or `binary_sha256`

- No case in either file pins them, so the mutation above passes both selftests (counts in the table).
- These fields do not feed `effective`, `verdict` or `exit`, so the declared after-value is unaffected. But "21/21 over the frozen cases" should not be read as checking the whole rule-6 output.
- Smallest fix: add uncounted supplementary cases that pin `setting_default.sites` and `schema`, or narrow the wording in the knowledge entry and evidence to "verdict, effective, exit, state and value". The frozen file cannot change without breaking the blob pin.

### 3. Low: contract clock stamps conflict with commit times (wording and provenance)

- Contract heading for A1 says `10:12Z`. Its commit `51ddd01` is `10:05:20Z`.
- Contract heading for A2 says `10:22Z, before any change to the landed C2 tool`. Its commit `6a92d5e` is `10:09:22Z`. The first tool change after the landing, `9a3d511`, is `10:15:49Z`, so the stamp is later than the change it says came after.
- The order itself holds by parent chain: `09f55b6` to `51ddd01` to `6a92d5e` to `9a3d511`. No tool commit lies between `09f55b62` and `6a92d5e` (`git log 09f55b62..6a92d5e -- tools/mori-job-runway.py` is empty).
- Commit dates are settable. `09f55b6` has author time `06:58:30` and committer time `07:02:38`.
- Smallest fix: drop the clock text from the amendment headings and cite the parent chain instead.

### 4. Info: the evidence leg is present at the new tip, with two small deviations

- `runway-selftest.txt` (commit `47b2b93`) names `revision: d3b7af2a287339c5d94655d741f83e5af07090cc`. That is after the last tool change `fbecc59` and an ancestor of the tip. Its `tool_blob` (`239dd8eb`) and `fixtures_tree` (`eddd10fb27a4495abe1da5d4dd3e7fe4202aacff`) match HEAD. Its stdout line matches my row 1.
- `runway-selftest-supplementary.txt` names the same revision and gives `PASS 24/24`, matching my row 6.
- Deviations: the header has two extra lines (`tool_blob`, `fixtures_tree`) between `command` and `exit`, while the contract's C2 text names three header lines. The `fixtures_tree` covers both case files, so the evidence does not pin the cases blob by itself. `git rev-parse HEAD:tools/fixtures/mori-job-runway/cases.json` gives `48df844a` directly.
- `runway-live-run.txt` says `RUNWAY_CLAMPED`, exit 1, at `run_at 2026-10-22T11:43:14Z`. A live run on this host now gives the same values (configured 200, clamp 100, effective 100, `RUNWAY_CLAMPED`, exit 1). It is not the after-value.

### 5. Info: the tool does not check its own freeze

- The selftest loads whichever `cases.json` it finds and does not check its blob. The freeze holds by git history and by the blob check in this report. No change to the tool is needed for the claim; recording the blob in the evidence header, as above, makes it re-derivable.

## Verified (positive)

- Both private clones are clean. The three runway files in the lane working copy match HEAD at `e0e33c1` (sha256 `5d90d7d4…`, `7098b008…`, `6c5d5251…`).
- Frozen cases: 21 unique ids, the same six expect keys in every case, all four verdicts represented. The zero-case guard (tool lines 596 to 597) and the missing-verdict guard (lines 587 to 588) from `fbecc59` are present.
- Temp directories are created and removed under `/tmp/mori-job-runway-*` (audit and strace agree).
- The `09f55b62` tool file's sha256 (`08217582…`) is the value the wave-1 BuildJobRunwayTool report gives for its pre-A2 sandbox commit. I did not open that sandbox.
- The contract changed only by additions since the freeze (`101 0`).

## Residual risk and gaps (not run, or not checked)

- The live running-job count is not readable from outside the session (contract frontier). Not measured.
- I did not open the upstream oh-my-pi source or re-run the full Bun probe of rule 1. I ran `Bun.YAML.parse` on one root flow case only.
- Mutation probing beyond the one field above is other seats' work and not repeated here.
- Audit hooks and strace cover the selftest path only. The live path was exercised with `--config` pointing at a nonexistent file and `--binary` reading omp's bytes, plus one default live run.
- Lane HEAD may move again. The tip measured here is `e0e33c1`. If it moves, re-check the tool blob (`239dd8eb`) and the cases blob (`48df844a`); those are what the claim depends on.

## Process notes

- Early batch label mistake (see the table note). Discarded and re-run.
- One later check aborted because a shell option from an earlier call was still set. Re-run with `set +e`.
- The lane working copy of `supplementary-cases.json` differed from HEAD at my first snapshot (`07a31ae8`: working copy sha256 `6c5d5251…`, HEAD `8d09756d…`). The change was committed as `d3b7af2`. All rows above use committed bytes.

## Tooling record

- No tool was installed, upgraded or removed. Used what was already on the host: `/usr/bin/python3` 3.14.8, `git` 2.56.0, `jq` (reports `jaq 3.1.1`; counts cross-checked with python), `/usr/bin/strace` 7.2, and `~/.local/bin/bun` 1.4.3 (installed by wave 1; used here only to parse one YAML string).
- No pacman, no omp run, no jj command, no edits to `~/.omp`.

## Cleanup

- Removed the two private clones and the extracts (about 2.8 GB).
- Kept small scratch artifacts under `/fast/scratch/hyaku/mori-r25/w2-RerunC2Count-x/`: `audit_driver.py`, `audit-tip-default.json` (at `07a31ae8`), `audit-tip2-default.json` (at `e0e33c1`), `strace-tip-default.txt`, `strace-tip2-default.txt`, `live-now.json`, `flow-case.yml`.
