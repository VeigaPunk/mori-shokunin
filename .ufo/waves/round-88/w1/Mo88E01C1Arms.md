# Mo88E01C1Arms — independent C1 measurement

Axes: operability (scoped claim), calibration (honest controls and provenance). Detection/report only; no remediation.

## Provenance

Lane HEAD observed at the beginning: `9c775ac2131da13c4c4cfdf2b14077184076f557`.
All target bytes below came from `git show`, not mutable lane working-tree files.

| Bytes read | Revision | SHA-256 |
|---|---|---|
| r87 count-c1.py, pristine target | d5e2eda494877a85edaa4e287d6ad81843d9a8a1 | 85bc0f29865e3c9a9de49940dcf12eef20977aa77899b6ba3290fcb243c7cc2c |
| r87 count-c1.py, entering | 1bd5ec3fa260458f74eb32a2e5bb157209c5934d | e2ff968721678cc61d6a1674def8da3e27a43f3fed8daab79d53c657ae2c266e |
| r88 count-c1.py, freeze | 2a5e3ad96deb978ed1fb958e87b4be8221fb23b7 | d1048cf06ae31bd15add31858bc204a44b711203dbb2e2bd6057450475baf2a1 |
| r88 count-c1.py, after instrument | d5e2eda494877a85edaa4e287d6ad81843d9a8a1 | 3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2 |
| label-only subject, constructed here | scratch fixture 75c1adbcffaefea72e172171060ad44cbed28a09 | e2882df1db47131053e6f4a1c987367f43b48a8912150c0a2bbefc2cd920f73d |

Authority read: contract P-C1 and arm/population tables at freeze revision. The after receipt was read at `9c775ac2131da13c4c4cfdf2b14077184076f557`; trying that receipt at the freeze revision failed because it did not exist then. That failed read was not a failed measurement.

## Independent measurement (not the r88 grade harness)

The driver imported only the MUTANTS tuple, then independently counted anchors, wrote substituted r87 copies and invoked each copy's own `python3 -I <copy> --selftest`. No r88 `grade`, `selftest_run`, `green` or `killed` helper was used for this measurement. TMPDIR and child cwd were seat scratch directories. MUTANTS from freeze and after instruments compared equal.

Pristine: rc **0**, `C1_COUNTER_SELFTEST pass=24 fail=0`, no FAIL lines.

| Mutant | Anchor occurrences | rc | Selftest pass/fail | Every FAIL arm | Contract-named killer fires? |
|---|---:|---:|---|---|---|
| M1-met-no-guard | 1 | 1 | 22/2 | met_guard_unanchored; met_guard_empty | Yes, both declared M1 killers |
| M2-met-drop-empty | 1 | 1 | 23/1 | met_guard_empty | Yes |
| M3-killed-n | 1 | 1 | 23/1 | killed_tally_mixed | Yes |
| M4-arms-total | 1 | 1 | 23/1 | arms_tally_passed | Yes |
| M5-split-field | 1 | 1 | 23/1 | target_split_killed_not_mutants | Yes |
| M6-anchor-guard | 1 | 1 | 22/2 | met_guard_unanchored; doubled_anchor_counted_type | Yes; additional undeclared overlap |

All six meet the frozen kill rule by nonzero rc and positive failing tally. No setup exits or survivors.

Exact FAIL output retained:

```text
M1:
FAIL met_guard_unanchored mutants=1 killed=1 survivors=0 total=1 arms=2
FAIL met_guard_empty mutants=1 killed=1 survivors=0 total=1 arms=2
M2:
FAIL met_guard_empty mutants=1 killed=1 survivors=0 total=1 arms=2
M3:
FAIL killed_tally_mixed mutants=2 killed=2 survivors=1 total=2 arms=2
M4:
FAIL arms_tally_passed mutants=1 killed=1 survivors=0 total=1 arms=1
M5:
FAIL target_split_killed_not_mutants 5 != 6
M6:
FAIL met_guard_unanchored mutants=2 killed=1 survivors=1 total=2 arms=2
FAIL doubled_anchor_counted_type mutants=1 killed=0 survivors=1 total=1 arms=1
```

Arm-table finding: `met_guard_unanchored` also kills M6, not listed in its contract row. This is an undeclared overlap, not substitution for the promised M6 arm: `doubled_anchor_counted_type` also fails. Every promised killer fires.

## Label-only adversarial control

A shared scratch clone was checked out at entering revision, its r87 bytes hash matched the entering hash above, and six unconditional `cases.append((label, True, "label-only"))` rows were inserted before the unique `ok = sum(...)` line. The labels were exactly the six promised arm names. The resulting subject selftest returned rc 0 and `C1_COUNTER_SELFTEST pass=24 fail=0`.

A fixture-local commit used `user.name=t`, `user.email=t@t`; the fixture top-level was asserted before committing. Both freeze and after r88 instruments independently returned rc **1** with all six mutants surviving rc 0 and the identical summary:

```text
C1=unmet mutants=6 killed=0 survivors=6 total=6 arms=24 detector=green rev=75c1adbcffae
```

Thus neither instrument accepts six labels and a passing 24-arm tally without actual mutant-killing assertions. The scratch fixture revision is ephemeral, not a retained lane commit; its reproducible source recipe is included below.

## Risks and limits

- Instrument freeze drift is real: `git diff 2a5e3ad96deb978ed1fb958e87b4be8221fb23b7 d5e2eda494877a85edaa4e287d6ad81843d9a8a1 -- .ufo/waves/round-88/count-c1.py` shows two added `COUNTER_SELFTEST pass=1 fail=0` fixture tally lines in r88 selfcheck's dup.py and empty.py bodies. Blob IDs are `9b7ebf21015c1bbd8f729de49669f2a290cd5cd9` → `8c607317e9daa6eb0a91679e35b1c2b133597f51`. The after receipt correctly binds the latter hash, not the freeze hash. Population, anchors, grading and kill rule are unchanged. This is a freeze-provenance caveat, not a failure of the independently measured six target kills; no remediation attempted.
- Scoped to C1; no independent C2 verdict asserted.
- No LSP tool is available in this seat's inventory; symbol/refactor operations were unnecessary. No tools installed, host/global state changed, or lane implementation edited.
- Only the named report is retained in the lane. Scratch source/output and shared clone are deleted before handoff. Exact executed drivers are embedded below, so evidence does not depend on deleted scratch artifacts.

## Retained exact drivers

Save the following as `/fast/scratch/hyaku/mori-r88/Mo88E01C1Arms/drive.py`:

```python
#!/usr/bin/env python3
"""Seat Mo88E01C1Arms: independent re-measure of the six C1 mutants (mori r88 w1).

Steps 1-3 of the seat spec. Uses its own harness (no frozen-counter grade() call):
loads pristine r87 counter bytes at d5e2eda, applies each MUTANTS triple taken from
the frozen r88 counter via importlib, asserts exactly-once anchors, runs each mutated
copy's own --selftest, records rc + every FAIL line.
"""
import hashlib
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import tempfile

S = os.path.dirname(os.path.abspath(__file__))
PRISTINE = os.path.join(S, "pristine", "count-c1.py")
FROZEN_R88 = os.path.join(S, "frozen", "count-c1.py")
AFTER_R88 = os.path.join(S, "after-counter", "count-c1.py")

FAILLINE = re.compile(r"(?m)^FAIL .*$")
TALLY = re.compile(r"COUNTER_SELFTEST pass=(\d+) fail=(\d+)")


def load_mutants(path):
    spec = importlib.util.spec_from_file_location("m_" + os.path.basename(path), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.MUTANTS


def run_env(path, work):
    env = dict(os.environ)
    env.update(TMPDIR=work, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)
    p = subprocess.run(["python3", "-I", path, "--selftest"], cwd=work, env=env,
                       capture_output=True, text=True, timeout=600)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def tally_of(out):
    t = TALLY.findall(out)
    return t[-1] if t else None


def main():
    mut_frozen = load_mutants(FROZEN_R88)
    mut_after = load_mutants(AFTER_R88)
    print("MUTANTS frozen==after-counter:", mut_frozen == mut_after)
    print("MUTANTS count:", len(mut_frozen))

    base = open(PRISTINE, encoding="utf-8").read()
    print("sha256 pristine d5e2eda r87 count-c1.py:",
          hashlib.sha256(base.encode("utf-8")).hexdigest())

    work = tempfile.mkdtemp(dir=S, prefix="t-")
    rc, out = run_env(PRISTINE, work)
    shutil.rmtree(work, ignore_errors=True)
    t = tally_of(out)
    print("PRISTINE rc=%d tally=%s fails=%s" % (rc, t, FAILLINE.findall(out)))
    open(os.path.join(S, "out-pristine.txt"), "w").write(out)
    green = rc == 0 and t == ("24", "0")
    print("PRISTINE-GREEN-24:", green)
    if not green:
        return 1

    rows = []
    for path, label, old, new in mut_frozen:
        assert path == ".ufo/waves/round-87/count-c1.py", path
        n = base.count(old)
        print("ANCHOR %s occurrences=%d" % (label, n))
        if n != 1:
            rows.append((label, None, "unanchored", [], out := ""))
            continue
        mutated = base.replace(old, new)
        d = os.path.join(S, "mut-" + label)
        os.makedirs(d, exist_ok=True)
        mp = os.path.join(d, "count-c1.py")
        open(mp, "w", encoding="utf-8").write(mutated)
        work = tempfile.mkdtemp(dir=S, prefix="t-")
        rc, out = run_env(mp, work)
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(d, ignore_errors=True)
        open(os.path.join(S, "out-%s.txt" % label), "w").write(out)
        t = tally_of(out)
        fails = FAILLINE.findall(out)
        verdict = "killed" if (rc != 0 or any(re.search(r"\bfail=[1-9]", f) for f in fails)) else "SURVIVED"
        print("MUTANT %s rc=%d tally=%s verdict=%s" % (label, rc, t, verdict))
        for f in fails:
            print("  " + f)
        rows.append((label, rc, t, fails, verdict))
    print("---SUMMARY---")
    for r in rows:
        print(r)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

Save the following as `/fast/scratch/hyaku/mori-r88/Mo88E01C1Arms/control.py`:

```python
import os, pathlib, subprocess, hashlib
S=pathlib.Path('/fast/scratch/hyaku/mori-r88/Mo88E01C1Arms')
D=S/'label-only'
env=dict(os.environ,TMPDIR=str(S),GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_SYSTEM=os.devnull)
def run(args):
 p=subprocess.run(args,cwd=S,env=env,text=True,capture_output=True)
 print('$ '+' '.join(map(str,args))); print(p.stdout+p.stderr,end=''); print('rc='+str(p.returncode))
 return p
assert run(['git','-C',str(D),'rev-parse','--show-toplevel']).stdout.strip()==str(D)
p=D/'.ufo/waves/round-87/count-c1.py'
base=p.read_text()
assert hashlib.sha256(base.encode()).hexdigest()=='e2ff968721678cc61d6a1674def8da3e27a43f3fed8daab79d53c657ae2c266e'
labels=['met_guard_unanchored','met_guard_empty','killed_tally_mixed','arms_tally_passed','target_split_killed_not_mutants','doubled_anchor_counted_type']
anchor='    ok = sum(1 for _, good, _ in cases if good)'
assert base.count(anchor)==1
rows=''.join('    cases.append((%r, True, "label-only"))\n'%label for label in labels)
p.write_text(base.replace(anchor,rows+anchor))
print('LABEL-ONLY sha256='+hashlib.sha256(p.read_bytes()).hexdigest())
pristine=run(['python3','-I',str(p),'--selftest'])
assert pristine.returncode==0 and 'C1_COUNTER_SELFTEST pass=24 fail=0' in pristine.stdout
assert run(['git','-C',str(D),'rev-parse','--show-toplevel']).stdout.strip()==str(D)
assert run(['git','-C',str(D),'-c','user.name=t','-c','user.email=t@t','commit','-qam','label-only']).returncode==0
rev=run(['git','-C',str(D),'rev-parse','HEAD']).stdout.strip()
for version in ['frozen','after-counter']:
 out=run(['python3','-I',str(S/version/'count-c1.py'),rev,'--repo',str(D),'--scratch',str(S/('control-'+version))])
 assert out.returncode==1 and 'C1=unmet mutants=6 killed=0 survivors=6 total=6 arms=24' in out.stdout
```

## Self-evaluation

Accuracy 4/5: exact rc, hashes and FAIL lines retained; freeze drift prevents treating all instrument bytes as unchanged. Completeness 5/5: pristine, all six mutants, named killers and label-only control measured. Clarity 4/5: exact drivers increase report length; tables summarize their results. Actionability 4/5: recipes retained, but scratch must be rebuilt. Conciseness 4/5: full driver retention is longer than a summary but preserves commands after required cleanup. Overall 4.2/5. Improvements: distinguish immutable population from changed detector fixtures; retain all extra killer arms (both applied here). The user can check the assessment against the measured outputs.

## Measured verdict and exact commands

**C1 agrees**: pristine 24/0, six exactly-once anchors, six killed, zero survivors; every contract-named killer fires. Arm-table overlap and freeze-instrument drift are separately disclosed above.

Exact extraction commands used (S denotes `/fast/scratch/hyaku/mori-r88/Mo88E01C1Arms`; L denotes `/home/vgpnk/Projects/shokunin/mori-shokunin`):

```sh
mkdir -p "$S/pristine" "$S/entering" "$S/frozen" "$S/after-counter"
git -C "$L" show d5e2eda494877a85edaa4e287d6ad81843d9a8a1:.ufo/waves/round-87/count-c1.py > "$S/pristine/count-c1.py"
git -C "$L" show 1bd5ec3f:.ufo/waves/round-87/count-c1.py > "$S/entering/count-c1.py"
git -C "$L" show 2a5e3ad96deb978ed1fb958e87b4be8221fb23b7:.ufo/waves/round-88/count-c1.py > "$S/frozen/count-c1.py"
git -C "$L" show d5e2eda494877a85edaa4e287d6ad81843d9a8a1:.ufo/waves/round-88/count-c1.py > "$S/after-counter/count-c1.py"
cd /fast/scratch/hyaku/mori-r88/Mo88E01C1Arms && python3 -I drive.py
git clone --shared -q /home/vgpnk/Projects/shokunin/mori-shokunin "$S/label-only"
git -C "$S/label-only" checkout -q 1bd5ec3fa260458f74eb32a2e5bb157209c5934d
git -C "$S/label-only" rev-parse --show-toplevel
python3 -I /fast/scratch/hyaku/mori-r88/Mo88E01C1Arms/control.py
```

The exact individual selftest and counter invocations are in the embedded drivers; the label-only counter commands expanded to:

```sh
python3 -I /fast/scratch/hyaku/mori-r88/Mo88E01C1Arms/frozen/count-c1.py 75c1adbcffaefea72e172171060ad44cbed28a09 --repo /fast/scratch/hyaku/mori-r88/Mo88E01C1Arms/label-only --scratch /fast/scratch/hyaku/mori-r88/Mo88E01C1Arms/control-frozen
python3 -I /fast/scratch/hyaku/mori-r88/Mo88E01C1Arms/after-counter/count-c1.py 75c1adbcffaefea72e172171060ad44cbed28a09 --repo /fast/scratch/hyaku/mori-r88/Mo88E01C1Arms/label-only --scratch /fast/scratch/hyaku/mori-r88/Mo88E01C1Arms/control-after-counter
```
