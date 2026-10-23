# MutQuality97 — criterion 97 mutation probe

Measured revision: `62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`.
Axes: literal-rule sensitivity; whitespace invariance; concession sensitivity; reproducibility and byte restoration.
Scope: detection only, not a C1 judgment. Criterion attacked: `corpus/QUALITY.md:702-711`.
Scratch prefix **S** below means `/fast/scratch/hyaku/mori-r33/MutQuality97`.

## Detector and limits

Created `S/check-quality97.py`; interface: `python3 -I -B S/check-quality97.py RULE DISPATCH RECEIPT`.
It requires the supplied nonempty rule to be a substring of each file after `" ".join(text.split())`.
Comparison is case- and punctuation-sensitive, over raw UTF-8 file text, not JSON-decoded strings.
The synthetic rule is R-J from `.ufo/waves/round-33/contract.md:47-50`, with Markdown quote markers removed.

A conceded-gap **candidate** is detected as follows:
- Recognize keyed lines `- S###: ...` or `row N: ...` (optional list marker; case-insensitive).
- Record keys with verdict `agree` or `supported`; word boundaries exclude `disagree` and `unsupported`.
- Scan that verdict's trailing reason and separately keyed reasons for the same positive key, including reasons below a separate heading. Explicit negative verdict lines are not positive reasons.
- Flag these case-insensitive patterns: `unsupported|unsourced|unsubstantiated`; `not` followed by `on|in|supported|carried|stated|established`; `caveat|gap`; `nothing ... contradicts` (up to 100 intervening characters) or `contradicted nowhere`; `companion|sibling` followed by `doc|document|page`; `half|part|parts` followed by `cite|cites`.
- PASS requires both rule matches and zero flagged lines; exits are 0 PASS, 1 FAIL, 2 input error. Actual outputs and commands are retained in `S/results.json:4-302`.

**Major — not fully checkable without a human.** The exact-rule substring condition is mechanical, but “concedes any unsupported part” is semantic and has no complete grammar in `corpus/QUALITY.md:703-708`. This script is a lexical screen, not an implementation of all that language's meaning. Observed ambiguity: the historical screen also flags S074's phrase “controllers close the gap,” where `gap` describes the controller subject, not an evidentiary concession (`.ufo/waves/round-32/judge/JudgeRecheck.md:71`; `S/results.json:21`). It flags S073's “symlink-caveat” too (`JudgeRecheck.md:70`). These seven flags are not seven adjudicated violations.

[INFERENCE] Other paraphrases, unkeyed/multiline reasons, and alternative receipt formats can evade this screen; quoted or negated gap vocabulary can cause false positives. Raw JSON escape sequences and Markdown quote prefixes are not whitespace and therefore are not normalized away. Those variants were not tested. Source-support adjudication remains human work; a lexical PASS cannot certify the entire criterion.

## Execution and cases

Executed once, synchronously:

```sh
timeout 90s prlimit --as=268435456 --cpu=60 -- python3 -I -B /fast/scratch/hyaku/mori-r33/MutQuality97/probe-quality97.py
```

Observed outer exit 0, wall time 1.48 seconds. Every detector subprocess used `timeout 5s prlimit --as=268435456 --cpu=8 -- python3 -I -B ...`; read-only Git subprocesses used 10-second limits. Commands, exits, stdout and stderr are recorded in `S/results.json`; all detector stderr strings were empty in that recorded run.

| Case | Expected | Observed |
|---|---|---|
| Round-32 `r1-dispatch.json` + `judge/JudgeRecheck.md` | FAIL | FAIL, exit 1; dispatch rule yes, receipt rule no; 7 lexical gap candidates |
| Round-31 judge pair, if present | N/A when absent | NOT RUN: receipt exists, but no paired committed judge dispatch found |
| Synthetic pristine pair, before each of 4 changes | PASS | PASS ×4, exit 0; both rule matches yes, gaps 0 |
| Remove rule from receipt only | FAIL | FAIL, exit 1; receipt rule no, gaps 0 — killed |
| Change receipt's `every fact` to `some fact` | FAIL | FAIL, exit 1; receipt rule no, gaps 0 — killed |
| Rewrap rule at 64 columns in both files | PASS | PASS, exit 0; both rule matches yes, gaps 0 — benign control passes |
| Receipt line `- S058: agree — the diff-tree half is not on the page` | FAIL | FAIL, exit 1; both rule matches yes, gap `S058:5` — killed |
| Restore exact pristine bytes after each change | PASS | PASS ×4, exit 0; both rule matches yes, gaps 0 |

Actual round-32 output (`S/results.json:20-25`):

```text
dispatch_rule=yes receipt_rule=no conceded_gaps=7 gap_lines=S058:63,S073:70,S074:71,S117:73,S128:74,S137:75,S149:76 result=FAIL
```

Actual missing-rule/changed-word output:

```text
dispatch_rule=yes receipt_rule=no conceded_gaps=0 gap_lines=- result=FAIL
```

Actual conceded-gap mutant output (`S/results.json:274-278`):

```text
dispatch_rule=yes receipt_rule=yes conceded_gaps=1 gap_lines=S058:5 result=FAIL
```

Pristine, rewrapped and restored output:

```text
dispatch_rule=yes receipt_rule=yes conceded_gaps=0 gap_lines=- result=PASS
```

Historical reference qualification: the round-32 comparison uses the full `Reject (disagree) a row when: ... failed fetches.` sentence extracted from its dispatch (`.ufo/waves/round-32/r1-dispatch.json:7`), matching criterion 97's own historical example (`corpus/QUALITY.md:709-711`). It is not represented here as a verbatim sentence from the frozen round-32 contract, whose verdict definition is at `.ufo/waves/round-32/contract.md:25-27`. This historical FAIL is not a killed mutant or proof of frozen-contract parity.

Round-31 search: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r --name-only 62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 .ufo/waves/round-31` found only `wave1-dispatch.json` among dispatch-named files. Its 41 task names include no judge; the receipt is present. Evidence: `S/round31-inventory.txt` and `S/round31-search.json:3-54`; targeted repository search for `JudgeC1Rows|non-author.*judge|You are.*judge` in round-31 JSON files returned `No matches found`. An unrelated writer dispatch was not substituted for a judge pair.

## Hashes and restoration

All four mutations used the same two scratch files. Before and after **every** case:

- Dispatch **D**: `63b90e98a8d2280174c1351903f8b8c891ef511d031fc1389f608d4cff40c5c9`
- Receipt **R**: `15f3f4026f88ee3650057fa2dd79f8ee182efa9408519702d196f08211f1e281`

| Case | Mutated dispatch sha256 | Mutated receipt sha256 | Restored |
|---|---|---|---|
| Rule removed | D | `901f06e4c8b30df5d59dc78fae30b7f31b0fdc442b2c80f31c477468a70421dc` | D / R, exact bytes |
| One word changed | D | `3d4bd975bd5343b7e487a858f3c2986c8938811d84301b5254d8e8310551f779` | D / R, exact bytes |
| Rewrapped | `4947687aba359aed0b83e62fd4bd70fcaef6de3e56da32a869d1ff2db5c77fa3` | `f2524ed4b94c73487bfa08770e1bd289b9bdc19d34a5e14f755aaab4577d3c87` | D / R, exact bytes |
| Conceded gap | D | `03d6871cf873bd8ba955593ceee45df6e45ab1a66bc30c4dda63d30b866e1a5e` | D / R, exact bytes |

Restoration used `finally`, checked direct byte equality as well as hashes, and reran the same detector on restored files. Evidence: `S/results.json:304-372`. All three harmful mutants were killed; no harmful survivor or inconclusive mutation case. The whitespace-only case is a positive invariance control, not an escaped defect.

Revision snapshots were obtained with read-only `git show <revision>:<path>`; their hashes (`S/results.json:374-382`) include:
- Round-32 dispatch: `fb4934ba655ea93ad73a0998323036e8b4b103eb8857fc404957802485007492`
- Round-32 receipt: `65a3787111374228f3674e945577fdee167f56f9be68f5f46b78c856d678bc77`
- Detector: `2da2e468a6dd342cf625eed405c7b066957ac42e41b970742cb627b8355f17bf`

Only this report was written in the lane; all fixtures/scripts/results are under S. No lane source, index, settings, services or device settings were changed. No subagents or background jobs were started; the bounded synchronous probe exited. No tools were installed or updated. The existing round-33 counter was not run; no C1 verdict is offered.
