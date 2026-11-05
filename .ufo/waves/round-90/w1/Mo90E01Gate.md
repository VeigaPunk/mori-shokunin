# Mo90E01Gate — candidate receipt gate

Axes: operability (assigned), calibration (unchanged).

## Deliverable

Complete candidate: `.ufo/waves/round-90/w1/candidates/r87-gate.py`, copied from verified entering commit `d1c8488986512a6a0475af88cc52779ce4703e00` and changed only for reachability and its explanatory docstring. SHA-256: `ab0c9104b6e7c65be1e6ecc4dc31409ae63cc5b403fde850a25155e487bfd4a6`.

The subtract-only pre-pass retains raw spelling alongside the existing shlex token stream, parses a deliberately narrow shell-list grammar, and blanks only words in provably dead simple commands before the existing invocation/exclusion logic runs. It tracks success/failure through left-associative `&&`/`||`, semicolon lists, subshells and `if`/`then`/`else`/`fi`; unconditional literal `exit`/`return` terminates only its current level. Literal false fails; true/colon/printf/echo succeed for this recorded-text rule. Unknown status retains both outcomes. Quoted/escaped operators never become syntax. Unsupported constructs, mismatched lexing, functions, braces, loops and heredocs conservatively leave the committed token stream unchanged. No command text is executed. The eight frozen commands are not matched by name or literal text.

## Measured evidence

`git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD` printed `d1c8488986512a6a0475af88cc52779ce4703e00`.

Final grading command (rc=0):

```sh
python3 -I /fast/scratch/hyaku/mori-r90/Mo90E01Gate/measure.py
```

```text
CASE R03:N-A08-exit-before class=branch expect=reject entering=bound after=refused ok
CASE R03:N-A09-or-short-circuit class=branch expect=reject entering=bound after=refused ok
CASE R03:N-A10-false-and class=branch expect=reject entering=bound after=refused ok
CASE C02:H01-or-short-circuit class=branch expect=reject entering=bound after=refused ok
CASE C02:H02-false-and class=branch expect=reject entering=bound after=refused ok
CASE C02:H03-exit-before class=branch expect=reject entering=bound after=refused ok
CASE C02:H04-if-false class=branch expect=reject entering=bound after=refused ok
CASE C02:H09-heredoc-or-subshell-false class=branch expect=reject entering=bound after=refused ok
POPULATION cases=78 branch_cases=8 branch_open=0 harm=0 newopen=0 open=22 gained=0
NOHARM cases=34 branch_cases=0 branch_open=0 harm=0 newopen=0 open=0 gained=0
REPAIR cases=56 branch_cases=0 branch_open=0 harm=0 newopen=0 open=21 gained=0
```

The 78 counted cases comprise 56 repair cases plus 22 heldout claim cases. All 59 repair rows were exercised; the existing `reach` marker excludes three rows from its tally. Those three also retained their prior result (two met bound, heredoc reject bound). The noharm battery exercises all 34 non-void rows in both files named by `noharm-c1.py`. Every retained met binding stays bound. N-E08-PWD-absolute remains refused by both gates, not a new harm. Residual open=22 is the frozen provenance population, intentionally untouched.

## Exact reproducible harness

Create the scratch directory below, write this as `measure.py`, and execute the command above. It only imports the gates and compares bindings; it never replays a receipt command. The harness and full final output are retained here because the scratch directory was removed before delivery.

```sh
mkdir -p /fast/scratch/hyaku/mori-r90/Mo90E01Gate
```

```python
import sys
sys.dont_write_bytecode = True
import importlib.util, json, pathlib, subprocess
L = pathlib.Path('/home/vgpnk/Projects/shokunin/mori-shokunin')
W = pathlib.Path(__file__).parent
REV = 'd1c8488986512a6a0475af88cc52779ce4703e00'
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
(W/'before.py').write_bytes(subprocess.check_output(['git','-C',str(L),'show', REV+':.ufo/waves/round-87/count-c2.py']))
before = load('before', W/'before.py')
after = load('after', L/'.ufo/waves/round-90/w1/candidates/r87-gate.py')
counter = load('counter', L/'.ufo/waves/round-90/count-c1.py')
all_lines=[]
def tally(cases,label):
    _, lines=counter.tally(cases,before,after,str(L),label)
    all_lines.extend(lines)
    print('\n'.join(lines))
tally(counter.load_cases(),'POPULATION')
noharm=[]
for filename in ('cases.json','cases2.json'):
    for c in json.load(open(L/'.ufo/waves/round-89/w1/Mo89R01C1-evidence'/filename)):
        if c['name'] != 'E15-semicolon-in-quoted-arg':
            noharm.append(dict(c,source='NOHARM'))
tally(noharm,'NOHARM')
tally([dict(c,source='R03') for c in json.load(open(counter.R03))],'REPAIR')
(W/'results.txt').write_text('\n'.join(all_lines)+'\n')
```

## Risks and boundaries

This is recorded-text reachability, not proof against function/PATH/interpreter substitution or runtime I/O failure. Unsupported shell syntax deliberately falls back to the existing rule. Redirect-bearing simple commands do not prove status or termination. L1 still owns integration and the independent committed battery gate; no production counter, selftest, build, formatter or linter was run for this assignment. No tools installed. No LSP interface was exposed, so symbol inspection used the existing source.

Process defects disclosed: initial exploration imported the production gate without disabling bytecode and created `round-87/__pycache__/count-c2.cpython-314.pyc`; that generated file was removed. A temporary committed copy was initially written under `/tmp` (32 KB) and removed. Initial harness execution had a quoting SyntaxError; corrected before the successful measurements. No tracked production source was edited. Scratch cleanup completed.

Self-evaluation: accuracy 4 (finite battery, not full shell semantics); completeness 4 (all assigned populations and eight classes measured; independent battery owned by another seat); clarity 4 (explicit conservative grammar, parser is 170+ lines); actionability 5 (complete candidate plus exact harness and outputs); conciseness 4 (full evidence retained to make deleted scratch reproducible). Overall 4.2. Would the user agree: all frozen requested numbers are directly retained, with scope limits explicit.

## Full final transcript

```text
CASE R03:N-E01-IB-combined class=prov expect=met entering=bound after=bound ok
CASE R03:N-E02-X-dev class=prov expect=met entering=bound after=bound ok
CASE R03:N-E03-W-error-category class=prov expect=met entering=bound after=bound ok
CASE R03:N-E04-timeout class=prov expect=met entering=bound after=bound ok
CASE R03:N-E05-env-i-PATH class=prov expect=met entering=bound after=bound ok
CASE R03:N-E06-cd-dot-and class=prov expect=met entering=bound after=bound ok
CASE R03:N-E07-double-slash class=prov expect=met entering=bound after=bound ok
CASE R03:N-E08-PWD-absolute class=prov expect=met entering=refused after=refused refused-both
CASE R03:N-E09-stderr-merge class=prov expect=met entering=bound after=bound ok
CASE R03:N-E10-pipe-amp-cat class=prov expect=met entering=bound after=bound ok
CASE R03:N-E11-subshell class=prov expect=met entering=bound after=bound ok
CASE R03:N-E12-brace-group class=prov expect=met entering=bound after=bound ok
CASE R03:N-E13-sh-c-string class=prov expect=met entering=bound after=bound ok
CASE R03:N-E14-escaped-path-chars class=prov expect=met entering=bound after=bound ok
CASE R03:N-E15-eval class=prov expect=met entering=bound after=bound ok
CASE R03:N-E16-stdbuf class=prov expect=met entering=bound after=bound ok
CASE R03:N-E17-env-C-dot class=prov expect=met entering=bound after=bound ok
CASE R03:N-E18-env-S class=prov expect=met entering=bound after=bound ok
CASE R03:N-E19-nice-dashdash class=prov expect=met entering=bound after=bound ok
CASE R03:N-E20-setsid class=prov expect=met entering=bound after=bound ok
CASE R03:N-E21-sh-c-dollar0 class=prov expect=met entering=bound after=bound ok
CASE R03:N-E22-escaped-space-hash class=prov expect=met entering=bound after=bound ok
CASE R03:N-E23-stdin-redirect class=prov expect=met entering=bound after=bound ok
CASE R03:N-E24-command-prefix class=prov expect=met entering=bound after=bound ok
CASE R03:N-E25-time-p class=prov expect=met entering=bound after=bound ok
CASE R03:N-E26-Xdev-glued class=prov expect=met entering=bound after=bound ok
CASE R03:N-E27-ionice class=prov expect=met entering=bound after=bound ok
CASE R03:N-E28-newline-separated class=prov expect=met entering=bound after=bound ok uncounted
CASE R03:N-E29-line-continuation class=prov expect=met entering=bound after=bound ok uncounted
CASE R03:N-A01-path-as-dollar0 class=prov expect=reject entering=bound after=bound open
CASE R03:N-A02-c-dashdash-data class=prov expect=reject entering=refused after=refused ok
CASE R03:N-A03-echo-path class=prov expect=reject entering=refused after=refused ok
CASE R03:N-A04-cat-path class=prov expect=reject entering=bound after=bound open
CASE R03:N-A05-m-runpy class=prov expect=reject entering=refused after=refused ok
CASE R03:N-A06-bash-n class=prov expect=reject entering=bound after=bound open
CASE R03:N-A07-bash-o-noexec class=prov expect=reject entering=bound after=bound open
CASE R03:N-A08-exit-before class=branch expect=reject entering=bound after=refused ok
CASE R03:N-A09-or-short-circuit class=branch expect=reject entering=bound after=refused ok
CASE R03:N-A10-false-and class=branch expect=reject entering=bound after=refused ok
CASE R03:N-A11-function-shadow class=prov expect=reject entering=bound after=bound open
CASE R03:N-A12-hash-p class=prov expect=reject entering=bound after=bound open
CASE R03:N-A13-function-never-called class=prov expect=reject entering=bound after=bound open
CASE R03:N-A14-set-n class=prov expect=reject entering=bound after=bound open
CASE R03:N-A16-fake-python-PATH class=prov expect=reject entering=bound after=bound open
CASE R03:N-A17-fake-python-relative class=prov expect=reject entering=bound after=bound open
CASE R03:N-A18-overwrite-bound class=prov expect=reject entering=bound after=bound open
CASE R03:N-A19-builtin-cd class=prov expect=reject entering=bound after=bound open
CASE R03:N-A15-sitecustomize class=prov expect=reject entering=bound after=bound open
CASE R03:N-A20-command-cd class=prov expect=reject entering=bound after=bound open
CASE R03:N-A21-env-combined-C class=prov expect=reject entering=bound after=bound open
CASE R03:N-A22-env-combined-S class=prov expect=reject entering=bound after=bound open
CASE R03:N-A23-uv-run-module class=prov expect=reject entering=bound after=bound open
CASE R03:N-A24-uv-run-directory class=prov expect=reject entering=bound after=bound open
CASE R03:N-A25-prod-absolute class=prov expect=reject entering=refused after=refused ok
CASE R03:N-A26-bash-runs-python-file class=prov expect=reject entering=bound after=bound open
CASE R03:N-A27-heredoc-data class=prov expect=reject entering=bound after=bound open uncounted
CASE R03:N-A28-dollar-quoted-cd class=prov expect=reject entering=bound after=bound open
CASE R03:N-A29-command-v class=prov expect=reject entering=bound after=bound open
CASE R03:N-A30-glued-hash class=prov expect=reject entering=refused after=refused ok
CASE C02:H01-or-short-circuit class=branch expect=reject entering=bound after=refused ok
CASE C02:H02-false-and class=branch expect=reject entering=bound after=refused ok
CASE C02:H03-exit-before class=branch expect=reject entering=bound after=refused ok
CASE C02:H04-if-false class=branch expect=reject entering=bound after=refused ok
CASE C02:H05-echo-as-data class=prov expect=reject entering=refused after=refused ok
CASE C02:H06-colon-noop class=prov expect=reject entering=refused after=refused ok
CASE C02:H07-bash-c-echo class=prov expect=reject entering=refused after=refused ok
CASE C02:H08-function-def-never-called class=prov expect=reject entering=bound after=bound open
CASE C02:H09-heredoc-or-subshell-false class=branch expect=reject entering=bound after=refused ok
CASE C02:H11-dotslash-comment class=prov expect=reject entering=refused after=refused ok
CASE C02:H12-dotslash-selfprint class=prov expect=reject entering=refused after=refused ok
CASE C02:H13-echo-dotslash class=prov expect=reject entering=refused after=refused ok
CASE C02:M01-env-usr-bin class=prov expect=met entering=bound after=bound ok
CASE C02:M02-timeout class=prov expect=met entering=bound after=bound ok
CASE C02:M03-command-builtin class=prov expect=met entering=bound after=bound ok
CASE C02:M04-O-flag class=prov expect=met entering=bound after=bound ok
CASE C02:M05-IB-combined class=prov expect=met entering=bound after=bound ok
CASE C02:M06-env-i class=prov expect=met entering=bound after=bound ok
CASE C02:M07-cd-subshell class=prov expect=met entering=bound after=bound ok
CASE C02:M08-pipe-tail class=prov expect=met entering=bound after=bound ok
CASE C02:M09-stderr-redirect class=prov expect=met entering=bound after=bound ok
CASE C02:M10-Wignore-glued class=prov expect=met entering=bound after=bound ok
POPULATION cases=78 branch_cases=8 branch_open=0 harm=0 newopen=0 open=22 gained=0
CASE NOHARM:E01-equiv-dotslash class=- expect=met entering=bound after=bound ok
CASE NOHARM:E02-plain-control class=- expect=met entering=bound after=bound ok
CASE NOHARM:E03-I-B-flags class=- expect=met entering=bound after=bound ok
CASE NOHARM:E04-usr-bin-python3 class=- expect=met entering=bound after=bound ok
CASE NOHARM:E05-direct-exec class=- expect=met entering=bound after=bound ok
CASE NOHARM:E06-quoted-script class=- expect=met entering=bound after=bound ok
CASE NOHARM:E07-python3.14 class=- expect=met entering=bound after=bound ok
CASE NOHARM:E08-env-assign-prefix class=- expect=met entering=bound after=bound ok
CASE NOHARM:E09-env-command class=- expect=met entering=bound after=bound ok
CASE NOHARM:E10-dashdash class=- expect=met entering=bound after=bound ok
CASE NOHARM:E11-W-flag class=- expect=met entering=bound after=bound ok
CASE NOHARM:E12-dotdot-normpath class=- expect=met entering=bound after=bound ok
CASE NOHARM:E13-usr-bin-python3-u class=- expect=met entering=bound after=bound ok
CASE NOHARM:E14-nice-prefix class=- expect=met entering=bound after=bound ok
CASE NOHARM:E16-and-chain class=- expect=met entering=bound after=bound ok
CASE NOHARM:E17-exec-prefix class=- expect=met entering=bound after=bound ok
CASE NOHARM:E18-uv-run class=- expect=met entering=bound after=bound ok
CASE NOHARM:E19-bash-c-wrapper class=- expect=met entering=bound after=bound ok
CASE NOHARM:E20-interp-trailing-comment class=- expect=met entering=bound after=bound ok
CASE NOHARM:A01-comment-named class=- expect=reject entering=refused after=refused ok
CASE NOHARM:A02-selfprint-data class=- expect=reject entering=refused after=refused ok
CASE NOHARM:A03-W-value-selfprint class=- expect=reject entering=refused after=refused ok
CASE NOHARM:A04-X-value-selfprint class=- expect=reject entering=refused after=refused ok
CASE NOHARM:A05-c-value-lookalike class=- expect=reject entering=refused after=refused ok
CASE NOHARM:A06-m-value-lookalike class=- expect=reject entering=refused after=refused ok
CASE NOHARM:A07-path-as-data-after-other-script class=- expect=reject entering=refused after=refused ok
CASE NOHARM:A08-semicolon-split-invocation class=- expect=reject entering=refused after=refused ok
CASE NOHARM:A09-hash-glued class=- expect=reject entering=refused after=refused ok
CASE NOHARM:A10-tab-comment class=- expect=reject entering=refused after=refused ok
CASE NOHARM:E15b-semicolon-in-quote-before-script class=- expect=met entering=bound after=bound ok
CASE NOHARM:E21-quoted-semicolon-harmless-arg-then-chain class=- expect=met entering=bound after=bound ok
CASE NOHARM:E22-hash-inside-quotes-not-comment class=- expect=met entering=bound after=bound ok
CASE NOHARM:A11-W-value-then-script-other class=- expect=reject entering=refused after=refused ok
CASE NOHARM:A12-X-value-then-c-selfprint-plus-script class=- expect=reject entering=refused after=refused ok
NOHARM cases=34 branch_cases=0 branch_open=0 harm=0 newopen=0 open=0 gained=0
CASE R03:N-E01-IB-combined class=- expect=met entering=bound after=bound ok
CASE R03:N-E02-X-dev class=- expect=met entering=bound after=bound ok
CASE R03:N-E03-W-error-category class=- expect=met entering=bound after=bound ok
CASE R03:N-E04-timeout class=- expect=met entering=bound after=bound ok
CASE R03:N-E05-env-i-PATH class=- expect=met entering=bound after=bound ok
CASE R03:N-E06-cd-dot-and class=- expect=met entering=bound after=bound ok
CASE R03:N-E07-double-slash class=- expect=met entering=bound after=bound ok
CASE R03:N-E08-PWD-absolute class=- expect=met entering=refused after=refused refused-both
CASE R03:N-E09-stderr-merge class=- expect=met entering=bound after=bound ok
CASE R03:N-E10-pipe-amp-cat class=- expect=met entering=bound after=bound ok
CASE R03:N-E11-subshell class=- expect=met entering=bound after=bound ok
CASE R03:N-E12-brace-group class=- expect=met entering=bound after=bound ok
CASE R03:N-E13-sh-c-string class=- expect=met entering=bound after=bound ok
CASE R03:N-E14-escaped-path-chars class=- expect=met entering=bound after=bound ok
CASE R03:N-E15-eval class=- expect=met entering=bound after=bound ok
CASE R03:N-E16-stdbuf class=- expect=met entering=bound after=bound ok
CASE R03:N-E17-env-C-dot class=- expect=met entering=bound after=bound ok
CASE R03:N-E18-env-S class=- expect=met entering=bound after=bound ok
CASE R03:N-E19-nice-dashdash class=- expect=met entering=bound after=bound ok
CASE R03:N-E20-setsid class=- expect=met entering=bound after=bound ok
CASE R03:N-E21-sh-c-dollar0 class=- expect=met entering=bound after=bound ok
CASE R03:N-E22-escaped-space-hash class=- expect=met entering=bound after=bound ok
CASE R03:N-E23-stdin-redirect class=- expect=met entering=bound after=bound ok
CASE R03:N-E24-command-prefix class=- expect=met entering=bound after=bound ok
CASE R03:N-E25-time-p class=- expect=met entering=bound after=bound ok
CASE R03:N-E26-Xdev-glued class=- expect=met entering=bound after=bound ok
CASE R03:N-E27-ionice class=- expect=met entering=bound after=bound ok
CASE R03:N-E28-newline-separated class=- expect=met entering=bound after=bound ok uncounted
CASE R03:N-E29-line-continuation class=- expect=met entering=bound after=bound ok uncounted
CASE R03:N-A01-path-as-dollar0 class=- expect=reject entering=bound after=bound open
CASE R03:N-A02-c-dashdash-data class=- expect=reject entering=refused after=refused ok
CASE R03:N-A03-echo-path class=- expect=reject entering=refused after=refused ok
CASE R03:N-A04-cat-path class=- expect=reject entering=bound after=bound open
CASE R03:N-A05-m-runpy class=- expect=reject entering=refused after=refused ok
CASE R03:N-A06-bash-n class=- expect=reject entering=bound after=bound open
CASE R03:N-A07-bash-o-noexec class=- expect=reject entering=bound after=bound open
CASE R03:N-A08-exit-before class=- expect=reject entering=bound after=refused ok
CASE R03:N-A09-or-short-circuit class=- expect=reject entering=bound after=refused ok
CASE R03:N-A10-false-and class=- expect=reject entering=bound after=refused ok
CASE R03:N-A11-function-shadow class=- expect=reject entering=bound after=bound open
CASE R03:N-A12-hash-p class=- expect=reject entering=bound after=bound open
CASE R03:N-A13-function-never-called class=- expect=reject entering=bound after=bound open
CASE R03:N-A14-set-n class=- expect=reject entering=bound after=bound open
CASE R03:N-A16-fake-python-PATH class=- expect=reject entering=bound after=bound open
CASE R03:N-A17-fake-python-relative class=- expect=reject entering=bound after=bound open
CASE R03:N-A18-overwrite-bound class=- expect=reject entering=bound after=bound open
CASE R03:N-A19-builtin-cd class=- expect=reject entering=bound after=bound open
CASE R03:N-A15-sitecustomize class=- expect=reject entering=bound after=bound open
CASE R03:N-A20-command-cd class=- expect=reject entering=bound after=bound open
CASE R03:N-A21-env-combined-C class=- expect=reject entering=bound after=bound open
CASE R03:N-A22-env-combined-S class=- expect=reject entering=bound after=bound open
CASE R03:N-A23-uv-run-module class=- expect=reject entering=bound after=bound open
CASE R03:N-A24-uv-run-directory class=- expect=reject entering=bound after=bound open
CASE R03:N-A25-prod-absolute class=- expect=reject entering=refused after=refused ok
CASE R03:N-A26-bash-runs-python-file class=- expect=reject entering=bound after=bound open
CASE R03:N-A27-heredoc-data class=- expect=reject entering=bound after=bound open uncounted
CASE R03:N-A28-dollar-quoted-cd class=- expect=reject entering=bound after=bound open
CASE R03:N-A29-command-v class=- expect=reject entering=bound after=bound open
CASE R03:N-A30-glued-hash class=- expect=reject entering=refused after=refused ok
REPAIR cases=56 branch_cases=0 branch_open=0 harm=0 newopen=0 open=21 gained=0
```
