# Mo81R02C2Attack — adversarial C2 review

Recommendation: **DISAGREE with C2 closure on the reviewed bytes**. Not an admission or integration decision.

Axes: operability, calibration, coverage, depth, freshness, adjacency. Detection/report only; no tool, counter, record, git state, host state or PATH entry changed. No subagents or installations. Produced only `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/w1/Mo81R02C2Attack.md`. All fixture writes were under `/fast/scratch/hyaku/mori-r81/Mo81R02C2Attack`, deleted in Python `finally: shutil.rmtree(S)` after every execution batch. No fixture git mutations were needed.

## Findings, by severity

| Severity | Check | Verdict and evidence |
|---|---|---|
| HIGH / closure blocker at observation | Corrections and landed C2 | DISAGREE: master `197655534b4a47a3c26149462e78752a6ea03eda` returns pending=3 pinned=1 tool=absent agree=0. The subsequently arrived uncommitted tool correctly reads the unchanged worktree dirty: pending=3 pinned=1; counter worktree grade tool=present agree=0 met=False. SCORECARD.md:4036 still states 232; :4048–4050 remain PENDING. The final requested read of `.ufo/waves/round-81/w1/Mo81S01Corrections.md` returned not found. This is an observed wave-in-flight gap, not a prediction about final integration. |
| MEDIUM | Conflicting stated values evade both implementations | DISAGREE: a matching row `| echo pointers=233 pointers=232 |` with live `pointers=233` passes the real sweep rc0 and counter grade met=True with the zero stub. `.ufo/waves/round-81/count-c2.py:78–86` and `tools/mori-record-sweep.py:49–61` select the first match, not the set. The contract kill rule says a conflict between two readings of the same key is a mismatch; its explicit live-value guarantee is implemented for stdout but not contradictory statements in the bound row. |
| MEDIUM | Round-section boundary disagreement | DISAGREE: `## Round 7\n| a | clean |\n# Appendix\n| a | PENDING |\n` gives counter pending=1 versus tool pending=0. Counter :67 only recognizes `## ` boundaries; tool :35 recognizes H1/H2. A table after a new document-level heading is outside the preceding Round section; the counter produces a false red and violates the required agreement on that fixture. |
| LOW / scope ambiguity | Second matching stale row | DISAGREE with broad claims of all matching claims checked; the frozen binding language is singular and does not explicitly require uniqueness. `| echo pointers=233 |` followed by `| echo pointers=232 |`, live 233, passes both. Same first-row sites above. Tool :11 documents first-row semantics and :160 tests it; the frozen authority does not name this limit. Do not describe this gate as auditing every repeated occurrence. |

## Required checks

| Check | Result | Recommendation |
|---|---|---|
| Exact PENDING in round table | both read pending=1; real tool rc1 | AGREE |
| PENDING prose | both pending=0; tool rc0 | AGREE |
| PENDING table under `## Notes` | both pending=0; tool rc0 | AGREE |
| Fenced pending row under Round | both pending=1; tool rc1 | AGREE with literal lexical grammar; residual Markdown false-positive risk |
| stated 232 / live 233 | pinned=1; tool rc1 | AGREE |
| command prints 233 but exits 1 | pinned=1; tool rc1 | AGREE |
| stdout prints 233 and 234 | pinned=1; tool rc1 | AGREE |
| binding row deleted | pinned=1; tool rc1 | AGREE: contract explicitly says deleting the row is not a pass; binding must still fire |
| dirty stub attack | agreeing dirty-count stub can produce agree=1, but met=False | AGREE with independent cleanliness defense; agree alone is not cleanliness |
| D80-2 live reproduction | own pinned runs at master 19765553, entering 44bc941a, and measured 97ce0c96 all print pointers=233 rc0 | AGREE with numerical correction 232→233, DISAGREE that the still-unmodified record has discharged it |
| D80-2 named revision and output in correction | correction report absent at final read; SCORECARD/SKILL diff empty | NOT VERIFIED / DISAGREE with a claim it already landed |
| D80-1 fill byte-for-byte against after-r80.txt | no fill exists in reviewed bytes | NOT VERIFIED / DISAGREE with closure; expected exact three counter lines quoted below |

Fence interpretation: frozen pending grammar expressly says an exact cell in a Round section, without the fence exclusion used by the r80 pointer sweep. Both implementations count a fenced pipe row. Under strict rendered-Markdown semantics it is not a table and this is a false positive; under the frozen lexical reading it is not a demonstrated contract breach. Report this limit instead of silently adding a new exclusion.

## Fixture reconstruction and output

Counter calls were executed in Python Eval using `runpy.run_path('/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c2.py')`, then `grade(str(base), str(pp))`. This executes the actual grade function, not a rewrite; avoids committing synthetic repositories. `base` was `/fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/counter-fixtures`. Each fixture wrote SCORECARD.md, tools/echo.py, tools/mori-record-sweep.py, and `.ufo/waves/round-81/record-pins.json` there. The pins schema was `mori-record-pins-v1`; bound cases had one binding `carrier=SCORECARD.md,row_contains=echo,key=pointers,command=["python3","-I","tools/echo.py"]`; other cases had no bindings. The initial stub source was `print('RECORD_SWEEP pending=0 pinned=0')`.

Inputs (Python string representation, literal newlines after unescaping):

- round pending: SCORECARD='## Round 7\n| x | PENDING |\n'; echo.py=''; bindings=False
- prose pending: SCORECARD='## Round 7\nPENDING\n'; echo.py=''; bindings=False
- outside table: SCORECARD='## Notes\n| x | PENDING |\n'; echo.py=''; bindings=False
- fenced pending: SCORECARD='## Round 7\n```markdown\n| x | PENDING |\n```\n'; echo.py=''; bindings=False
- stale binding: SCORECARD='## Round 7\n| echo pointers=232 |\n'; echo.py="print('pointers=233')\n"; bindings=True
- failing command: SCORECARD='## Round 7\n| echo pointers=233 |\n'; echo.py="print('pointers=233');raise SystemExit(1)\n"; bindings=True
- conflicting stdout: SCORECARD='## Round 7\n| echo pointers=233 |\n'; echo.py="print('pointers=233 pointers=234')\n"; bindings=True
- deleted row: SCORECARD='## Round 7\n| other |\n'; echo.py="print('pointers=233')\n"; bindings=True
- conflicting stated row: SCORECARD='## Round 7\n| echo pointers=233 pointers=232 |\n'; echo.py="print('pointers=233')\n"; bindings=True
- second stale matching row: SCORECARD='## Round 7\n| echo pointers=233 |\n| echo pointers=232 |\n'; echo.py="print('pointers=233')\n"; bindings=True

Actual counter outputs:
```text
round pending: {'pending': 1, 'pinned': 0, 'tool': 'present', 'agree': 0, 'met': False}
prose pending: {'pending': 0, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': True}
outside table: {'pending': 0, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': True}
fenced pending: {'pending': 1, 'pinned': 0, 'tool': 'present', 'agree': 0, 'met': False}
stale binding: {'pending': 0, 'pinned': 1, 'tool': 'present', 'agree': 0, 'met': False}
failing command: {'pending': 0, 'pinned': 1, 'tool': 'present', 'agree': 0, 'met': False}
conflicting stdout: {'pending': 0, 'pinned': 1, 'tool': 'present', 'agree': 0, 'met': False}
deleted row: {'pending': 0, 'pinned': 1, 'tool': 'present', 'agree': 0, 'met': False}
conflicting stated row: {'pending': 0, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': True}
second stale matching row: {'pending': 0, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': True}
all-zero dirty stub: {'pending': 1, 'pinned': 0, 'tool': 'present', 'agree': 0, 'met': False}
truthful counts but rc0 dirty stub: {'pending': 1, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': False}
contradictory clean stub: {'pending': 0, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': True}
H1 boundary counter=[(4, '## Round 7', 1)] tool=[]
```

Stub attack sources, each rc0: all-zero stub above against pending=1; dirty-count stub `print("RECORD_SWEEP pending=1 pinned=0")` against pending=1; contradictory stub `print("RECORD_SWEEP pending=0 pinned=0"); print("RECORD_SWEEP pending=9 pinned=9")` against clean input. The dirty-count stub proves agree=1 while dirty, **not** C2=met. The contradictory clean stub proves only the first summary is checked (`count-c2.py:140–143`); no full dirty-record bypass was found for an independently recognized debt. This is a reporting-integrity limit, not a claim that a genuine known pending cell becomes met.

Real-tool fixtures used identical bodies/pins/echo commands at `/fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/fixtures` and invoked the lane tool by CLI, with no stub. Exact CLI commands and stdout/exit statuses are in the transcript below.

## Commands and outputs

Read-only revision exports used `git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive <rev>` (rc0), piped as captured bytes into `tar -x -C <scratch>/<sha8>` (rc0), through subprocess argv rather than a shell. No shared clone or git mutation was used.

```text
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD
197655534b4a47a3c26149462e78752a6ea03eda
rc=0

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c2.py 197655534b4a47a3c26149462e78752a6ea03eda --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack --pins /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/record-pins.json
C2=unmet pending=3 pinned=1 tool=absent agree=0 rev=197655534b4a
rc=1

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c2.py 44bc941a0e3e9676fa33a882b43d6e9793cbf74d --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack --pins /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/record-pins.json
C2=unmet pending=3 pinned=1 tool=absent agree=0 rev=44bc941a0e3e
rc=1

worktree grade: ({'pending': 3, 'pinned': 1, 'tool': 'absent', 'agree': 0, 'met': False}, 'C2=unmet pending=3 pinned=1 tool=absent agree=0')

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py --root /home/vgpnk/Projects/shokunin/mori-shokunin
RECORD_SWEEP_MISMATCH pending SCORECARD.md:4048 cell=4 value=PENDING
RECORD_SWEEP_MISMATCH pending SCORECARD.md:4049 cell=4 value=PENDING
RECORD_SWEEP_MISMATCH pending SCORECARD.md:4050 cell=4 value=PENDING
RECORD_SWEEP_MISMATCH pinned SCORECARD.md:4036 pointers stated=232 live=233 command_rc=0
RECORD_SWEEP pending=3 pinned=1 carriers=1 bindings=1
rc=1

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py --root /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/fixtures
RECORD_SWEEP_MISMATCH pending SCORECARD.md:2 cell=1 value=PENDING
RECORD_SWEEP pending=1 pinned=0 carriers=1 bindings=0
rc=1

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py --root /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/fixtures
RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=0
rc=0

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py --root /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/fixtures
RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=0
rc=0

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py --root /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/fixtures
RECORD_SWEEP_MISMATCH pending SCORECARD.md:3 cell=1 value=PENDING
RECORD_SWEEP pending=1 pinned=0 carriers=1 bindings=0
rc=1

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py --root /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/fixtures
RECORD_SWEEP_MISMATCH pinned SCORECARD.md:2 pointers stated=232 live=233 command_rc=0
RECORD_SWEEP pending=0 pinned=1 carriers=1 bindings=1
rc=1

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py --root /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/fixtures
RECORD_SWEEP_MISMATCH pinned SCORECARD.md:2 pointers stated=233 live=233 command_rc=1
RECORD_SWEEP pending=0 pinned=1 carriers=1 bindings=1
rc=1

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py --root /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/fixtures
RECORD_SWEEP_MISMATCH pinned SCORECARD.md:2 pointers stated=233 live=missing-or-conflicting command_rc=0
RECORD_SWEEP pending=0 pinned=1 carriers=1 bindings=1
rc=1

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py --root /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/fixtures
RECORD_SWEEP_MISMATCH pinned SCORECARD.md:1 pointers stated=missing live=233 command_rc=0
RECORD_SWEEP pending=0 pinned=1 carriers=1 bindings=1
rc=1

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py --root /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/fixtures
RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=1
rc=0

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py --root /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/fixtures
RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=1
rc=0

$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/44bc941a/tools/mori-record-sweep.py --root /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/44bc941a
python3: can't open file '/fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/44bc941a/tools/mori-record-sweep.py': [Errno 2] No such file or directory
rc=2

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-record-sweep.py --root /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/44bc941a --pins /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/record-pins.json
RECORD_SWEEP_MISMATCH pending SCORECARD.md:4048 cell=4 value=PENDING
RECORD_SWEEP_MISMATCH pending SCORECARD.md:4049 cell=4 value=PENDING
RECORD_SWEEP_MISMATCH pending SCORECARD.md:4050 cell=4 value=PENDING
RECORD_SWEEP_MISMATCH pinned SCORECARD.md:4036 pointers stated=232 live=233 command_rc=0
RECORD_SWEEP pending=3 pinned=1 carriers=1 bindings=1
rc=1

$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/44bc941a/tools/mori-claim-sweep.py --root /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/44bc941a --pins /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/44bc941a/.ufo/waves/round-80/claim-pins.json
CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=4 pointers=233
rc=0

$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/97ce0c96/tools/mori-claim-sweep.py --root /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/97ce0c96 --pins /fast/scratch/hyaku/mori-r81/Mo81R02C2Attack/97ce0c96/.ufo/waves/round-80/claim-pins.json
CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=4 pointers=233
rc=0

worktree grade after tool arrival: ({'pending': 3, 'pinned': 1, 'tool': 'present', 'agree': 0, 'met': False}, 'C2=unmet pending=3 pinned=1 tool=present agree=0')

$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff -- SCORECARD.md SKILL.md .ufo/waves/round-81/count-c2.py
rc=0
```

The separately executed live pinned command (cwd `/home/vgpnk/Projects/shokunin/mori-shokunin`) was:
```text
git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse master && python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-claim-sweep.py --root /home/vgpnk/Projects/shokunin/mori-shokunin --pins /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/claim-pins.json
197655534b4a47a3c26149462e78752a6ea03eda
CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=4 pointers=233
rc=0
```
The worktree tool was absent on initial read and present on final read. It is absent in entering revision: executing that revision's path gives rc2 (not a passed check). Running the arrived implementation over the entering export with external frozen pins correctly detects 3/1. Revision-counter CLI exports committed bytes; direct `grade()` over the worktree separately reviews uncommitted integration bytes and is not mislabeled as a committed result.

## D80-1 expected byte identity / D80-4 precision

`after-r80.txt:3,57,62` carries these exact lines:
```text
C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=97ce0c96c779
MUTATION_C2 survivors=0 killed=6 total=6 unmutated=green rev=97ce0c96c779
C3=met named=56 present=56 missing=0 extra=0 rev=97ce0c96c779
```
All corresponding receipt rc lines are 0. Measured revision is `97ce0c96c779278baa8e8bb45ade642f9fabf1e2`, not 44bc941a. I independently reran only the pinned pointer sweep at those revisions, not the three historical r80 counters; I do not claim those three lines independently remeasured. No drafted fill existed to compare byte-for-byte. A later fill must preserve these lines or explicitly label genuinely remeasured outputs at a different revision, rather than silently change `rev=` while claiming receipt identity.

## Residual risk and verification gaps

- `read xd://lsp` returned “No such tool”; there is no mounted LSP device, so status/references/definition/diagnostics could not be obtained. Source reads and executed function/CLI fixtures are the fallback evidence, not semantic-reference proof.
- No runtime/rerouting/saturation/resume implementation is changed in this assigned diff; `resume_continuity_v1` and canonical orchestration-run behavior are outside this C2 review. No orchestration claim is certified.
- The arriving tool and record drafts are concurrent wave work. Only the observed bytes are graded; this report does not assert final branch C2 remains red after L1 integration.
- Tests exercised here are explicit assignment checks only. No standing battery, selftest suite, source census, OS/service check, build, formatter or unrelated validation was run. No installed tools to report.
- The counter trusts bound commands and record tool stdout; command read-only provenance is an external precondition, not a sandbox guarantee. The tool documents this honestly.

Self-evaluation: accuracy 4 (worktree arrival versus committed revision explicitly distinguished); completeness 4 (all reachable fixture checks run, missing correction draft honestly blocks byte comparison); clarity 4 (fixture inputs and raw transcripts retained); actionability 4 (two precise parser defects and correction obligations); conciseness 3 (long transcript required for reproducibility). Mean 3.8. Improvements: review final integrated correction bytes and retain these falsifiers in main-agent validation. No unrun check is marked passed.
