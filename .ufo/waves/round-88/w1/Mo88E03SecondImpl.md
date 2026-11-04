# Independent verdict implementation — Mo88E03SecondImpl

Axes: operability and calibration. Detection/report only.

Revision measured: `d5e2eda494877a85edaa4e287d6ad81843d9a8a1`; every source and receipt was fetched with `git show REV:path`, not from changing worktree bytes. SHA-256 hashes are retained below.

## Result and interpretation

- **C1 AGREE:** independent AST/literal-only table parsing, exactly-once anchor checks, pristine `pass=24 fail=0`, and six separate mutated subprocess selftests yielded **6 killed / 0 survived**. All six returned rc=1 and printed named FAIL arms; no timeout/setup death supplied a kill.
- **C2 AGREE on the specified population-header cross-check:** 4/7 receipts carry replay headers; 8/9 binding paths are command tokens; all supersedes targets are in the seven-receipt population. Raw counts are `missing_replay=3 cmd_unbound=1 absent_targets=0`. The three missing replay headers are the explicitly legacy population rows; the unbound path is in legacy `after-r85.txt`. Applying the frozen declared-mode exemption gives `missing_replay=0 cmd_unbound=0`, consistent with its real-population target. These raw nonzero fields are **not** silently normalized or asserted as counterfeit refusals.
- Frozen C1 and C2 counters were separately executed over that revision; both returned rc=0 and their target lines. Their complete printed output is retained below. In particular they measured missing-replay refusal, cmd-binding refusal and absent-target refusal.

### Scope and limitations

The assignment's first bullet names the r87 MUTANTS table, but that table contains the six **r86** mutation anchors, not the frozen r88 six-clause population. The implementation independently parses that r87 table (six rows), then parses the frozen **r88** table and applies its six anchors to the committed **r87** subject. This preserves the requested frozen claim instead of substituting the prior round's claim.

The independent C2 implementation is the requested header parser, not an independent replay engine or counterfeit-fixture runner. Thus agreement covers its specified header invariants, while the full counterfeit behavioral verdict is observed through the separately executed frozen counter, not independently reconstructed. No disagreement was measured, so no disagreement needed a second check. No counter was imported or executed to parse its data; only the explicitly requested subprocess selftests and frozen comparison runs executed counters.

LSP was unavailable: this seat exposes no LSP tool. No symbol edits/refactors were needed. No tools installed, no host remediation, no lane implementation changes, no commits. Only this report persists; the scratch source and all experiment artifacts were removed by the shell EXIT trap.

## Independent parser source (106 lines)

```python
import ast
import hashlib
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

REPO = '/home/vgpnk/Projects/shokunin/mori-shokunin'
REV = 'd5e2eda494877a85edaa4e287d6ad81843d9a8a1'
ROOT = Path(__file__).resolve().parent
ENV = dict(os.environ, TMPDIR=str(ROOT), GIT_CONFIG_GLOBAL=os.devnull,
           GIT_CONFIG_SYSTEM=os.devnull, PYTHONDONTWRITEBYTECODE='1')

def run(argv):
    return subprocess.run(argv, cwd=ROOT, env=ENV, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=900)

def blob(path):
    p = run(['git', '-C', REPO, 'show', REV + ':' + path])
    assert p.returncode == 0, p.stdout
    print('SHA256', path, hashlib.sha256(p.stdout.encode()).hexdigest())
    return p.stdout

def table(text, name, names=None):
    for node in ast.parse(text).body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and
                t.id == name for t in node.targets):
            value = node.value
            if names:
                class Resolve(ast.NodeTransformer):
                    def visit_Name(self, n):
                        return ast.Constant(names[n.id])
                value = Resolve().visit(value)
            return ast.literal_eval(value)
    raise ValueError('table absent: ' + name)

def selftest(label, text):
    path = ROOT / (label + '.py')
    path.write_text(text)
    p = run(['python3', '-I', str(path), '--selftest', '--scratch', str(ROOT)])
    lines = p.stdout.splitlines()
    failures = [s for s in lines if s.startswith('FAIL ')]
    tally = [s for s in lines if '_COUNTER_SELFTEST pass=' in s][-1]
    print('SELFTEST', label, 'rc=' + str(p.returncode), tally, *failures, sep=' | ')
    return p.returncode, failures, tally

subject = '.ufo/waves/round-87/count-c1.py'
base = blob(subject)
# Parse, but never import or execute, the r87 MUTANTS table too.
old_table = table(base, 'MUTANTS', {f'C{i}': f'.ufo/waves/round-86/count-c{i}.py'
                                  for i in (1, 2, 3)})
print('R87_TABLE rows=' + str(len(old_table)))
frozen = [blob(f'.ufo/waves/round-88/count-c{i}.py') for i in (1, 2)]
mutants = table(frozen[0], 'MUTANTS', {'C1': subject})
rc, failures, tally = selftest('pristine', base)
pristine = rc == 0 and not failures and tally == 'C1_COUNTER_SELFTEST pass=24 fail=0'
killed = survived = 0
for path, label, old, new in mutants:
    assert path == subject and base.count(old) == 1 and old != new, label
    rc, failures, tally = selftest(label, base.replace(old, new, 1))
    dead = rc != 0 or bool(failures) or any(int(n) for n in re.findall(r'fail=(\d+)', tally))
    killed += dead
    survived += not dead
print(f'SECOND_C1={killed} killed / {survived} survived')
rows = table(blob('.ufo/waves/round-87/count-c2.py'), 'POPULATION')
known = {Path(row[0]).name for row in rows}
missing = unbound = absent = replay_count = binding_count = 0
policy_missing = policy_unbound = 0
for path, expect, mode, token in rows:
    text = blob(path)
    fields = {}
    for line in text.splitlines():
        if line.strip() == '# ---':
            break
        if line.startswith('#') and ':' in line:
            key, value = line[1:].split(':', 1)
            fields.setdefault(key.strip(), []).append(value.strip())
    has_replay = bool(fields.get('replay'))
    tokens = set(shlex.split(fields['cmd'][0]))
    paths = [value.split(maxsplit=1)[1] for value in fields.get('counter-sha256', [])]
    bad = sum(path not in tokens for path in paths)
    missing += not has_replay
    replay_count += has_replay
    unbound += bad
    binding_count += len(paths)
    absent += sum(t not in known for t in fields.get('supersedes', []))
    policy_missing += not has_replay and mode in ('required', 'clone')
    policy_unbound += bad if mode in ('required', 'clone') or has_replay else 0
    print(f'HEADER {Path(path).name} mode={mode} replay={int(has_replay)} '
          f'bindings={len(paths)} cmd_unbound={bad}')
print(f'SECOND_C2 missing_replay={missing} cmd_unbound={unbound} absent_targets={absent}')
print(f'C2_POLICY missing_replay={policy_missing} cmd_unbound={policy_unbound} '
      f'replay_headers={replay_count} bindings={binding_count}')
for index, source in enumerate(frozen, 1):
    path = ROOT / f'frozen-c{index}.py'
    path.write_text(source)
    p = run(['python3', '-I', str(path), REV, '--repo', REPO, '--scratch', str(ROOT)])
    print(f'FROZEN_C{index} rc={p.returncode}\n{p.stdout}', end='')
    if index == 1:
        agree = pristine and (killed, survived) == (6, 0) and p.returncode == 0
        print('C1 ' + ('AGREE' if agree else 'DISAGREE killed/survived/pristine'))
    else:
        agree = (policy_missing, policy_unbound, absent) == (0, 0, 0) and p.returncode == 0
        print('C2 ' + ('AGREE' if agree else 'DISAGREE receipt-header-policy'))
```

## Retained measurement output

```text
SHA256 .ufo/waves/round-87/count-c1.py 85bc0f29865e3c9a9de49940dcf12eef20977aa77899b6ba3290fcb243c7cc2c
R87_TABLE rows=6
SHA256 .ufo/waves/round-88/count-c1.py 3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2
SHA256 .ufo/waves/round-88/count-c2.py 8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7
SELFTEST | pristine | rc=0 | C1_COUNTER_SELFTEST pass=24 fail=0
SELFTEST | M1-met-no-guard | rc=1 | C1_COUNTER_SELFTEST pass=22 fail=2 | FAIL met_guard_unanchored mutants=1 killed=1 survivors=0 total=1 arms=2 | FAIL met_guard_empty mutants=1 killed=1 survivors=0 total=1 arms=2
SELFTEST | M2-met-drop-empty | rc=1 | C1_COUNTER_SELFTEST pass=23 fail=1 | FAIL met_guard_empty mutants=1 killed=1 survivors=0 total=1 arms=2
SELFTEST | M3-killed-n | rc=1 | C1_COUNTER_SELFTEST pass=23 fail=1 | FAIL killed_tally_mixed mutants=2 killed=2 survivors=1 total=2 arms=2
SELFTEST | M4-arms-total | rc=1 | C1_COUNTER_SELFTEST pass=23 fail=1 | FAIL arms_tally_passed mutants=1 killed=1 survivors=0 total=1 arms=1
SELFTEST | M5-split-field | rc=1 | C1_COUNTER_SELFTEST pass=23 fail=1 | FAIL target_split_killed_not_mutants 5 != 6
SELFTEST | M6-anchor-guard | rc=1 | C1_COUNTER_SELFTEST pass=22 fail=2 | FAIL met_guard_unanchored mutants=2 killed=1 survivors=1 total=2 arms=2 | FAIL doubled_anchor_counted_type mutants=1 killed=0 survivors=1 total=1 arms=1
SECOND_C1=6 killed / 0 survived
SHA256 .ufo/waves/round-87/count-c2.py 7e577f533e1dac676d3f5b3d601f2c4c622c57c325e6091e6018b5781ae73fc0
SHA256 .ufo/waves/round-85/evidence/after-r85.txt 9ff6c459fe6f81640f00f3209734b9aedafe73cd6d1b8f20706e347831a38d71
HEADER after-r85.txt mode=legacy replay=0 bindings=3 cmd_unbound=1
SHA256 .ufo/waves/round-85/evidence/record-sweep-r85.txt a4b4d0da21d3f8a869d2f919d1990bb1d6ac89026022fde32a2fdbdde755d2f3
HEADER record-sweep-r85.txt mode=legacy replay=0 bindings=1 cmd_unbound=0
SHA256 .ufo/waves/round-85/evidence/claim-sweep-r85.txt 7b209ba39591df9e5020199997b9b55c29fe2a8fc3c56e415c158e8aef7ed061
HEADER claim-sweep-r85.txt mode=legacy replay=0 bindings=1 cmd_unbound=0
SHA256 .ufo/waves/round-86/evidence/after-c1-r86.txt dba7eb7aadf0d99c80420a6ec223a31cdf8f86460f95cf9ef312bc3b448a2946
HEADER after-c1-r86.txt mode=required replay=1 bindings=1 cmd_unbound=0
SHA256 .ufo/waves/round-86/evidence/replay-defeat-r86.txt 055523561733ed0cd005e02a756df8e53ce8724ef57fd22625eacab02c8036a3
HEADER replay-defeat-r86.txt mode=required replay=1 bindings=1 cmd_unbound=0
SHA256 .ufo/waves/round-87/evidence/record-sweep-r87.txt 213a7558e155ea4eaeec8472767fa8371b44948e40b59cf9ac8437954641f4ac
HEADER record-sweep-r87.txt mode=clone replay=1 bindings=1 cmd_unbound=0
SHA256 .ufo/waves/round-87/evidence/claim-sweep-r87.txt 429a5dca94d32e14bd3614524fd9c441d682ba3986bceda4a98a0a4354a296b8
HEADER claim-sweep-r87.txt mode=clone replay=1 bindings=1 cmd_unbound=0
SECOND_C2 missing_replay=3 cmd_unbound=1 absent_targets=0
C2_POLICY missing_replay=0 cmd_unbound=0 replay_headers=4 bindings=9
FROZEN_C1 rc=0
MUTANT count-c1.py M1-met-no-guard killed rc=1
MUTANT count-c1.py M2-met-drop-empty killed rc=1
MUTANT count-c1.py M3-killed-n killed rc=1
MUTANT count-c1.py M4-arms-total killed rc=1
MUTANT count-c1.py M5-split-field killed rc=1
MUTANT count-c1.py M6-anchor-guard killed rc=1
C1=met mutants=6 killed=6 survivors=0 total=6 arms=24 rev=d5e2eda49487
C1 AGREE
FROZEN_C2 rc=0
REAL rc=0 C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=d5e2eda49487
FX clean rc=0 refused C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=d5e2eda49487
FX stripped rc=1 refused problems=missing-replay
FX vacuous rc=1 refused problems=cmd-binding
FX absent-target rc=1 refused supersede-absent=1
C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23 rev=d5e2eda49487
C2 AGREE
```

## Self-evaluation

Accuracy 4/5: concrete hashes, rc values and failure arms retained; C2 is header-only independent evidence, not a second replay engine. Completeness 4/5: all assigned outputs and source retained; the r87/r88 table naming mismatch required an explicit interpretation. Clarity 4/5: raw legacy exceptions are distinguished from claim failure; the required full source/output makes this report long. Actionability 4/5: commands and complete source reproduce the measurement, though scratch must be recreated. Conciseness 4/5: source is 106 lines; required raw output dominates length. Overall 4.0/5. Highest-impact improvement: a separately scoped independent replay/fixture engine would strengthen C2 beyond the requested header cross-check. The user should agree with the bounded evidence distinction.

## Verdict and exact commands

**Measured verdict: C1 AGREE; C2 AGREE for the requested header invariants (not an independent full counterfeit behavioral proof).** Frozen full claims both printed `met` with rc=0.

After recreating the pasted source at the scratch path, the exact executed driver was:

```sh
S=/fast/scratch/hyaku/mori-r88/Mo88E03SecondImpl; trap 'rm -rf -- "$S"' EXIT; TMPDIR="$S" python3 -I "$S/second.py"
```

Its subprocess comparison commands were:

```sh
python3 -I /fast/scratch/hyaku/mori-r88/Mo88E03SecondImpl/frozen-c1.py d5e2eda494877a85edaa4e287d6ad81843d9a8a1 --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch /fast/scratch/hyaku/mori-r88/Mo88E03SecondImpl
python3 -I /fast/scratch/hyaku/mori-r88/Mo88E03SecondImpl/frozen-c2.py d5e2eda494877a85edaa4e287d6ad81843d9a8a1 --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch /fast/scratch/hyaku/mori-r88/Mo88E03SecondImpl
```
