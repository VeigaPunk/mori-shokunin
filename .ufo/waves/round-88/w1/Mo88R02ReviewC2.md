# Mo88R02ReviewC2 — behavioral C2 review

Axes: calibration (primary), operability (no regression). Detection/report only; no remediation.

## Findings by severity

**High — routed defect for round 89: comment-token command binding accepts a fabricated body.** `.ufo/waves/round-87/count-c2.py:140-145` splits shell source on whitespace rather than identifying executed arguments. A bound path inside a shell comment satisfies the check, although bash never executes or passes that path. On `record-sweep-r87.txt`, use:

```text
# cmd: printf 'RECORD_SWEEP fabricated=1\n' # tools/mori-record-sweep.py
# replay: clone
# ---
RECORD_SWEEP fabricated=1
```

Keep all other headers unchanged. Measured fixture `a010047c4819f404146323f23ccc4c24c6719e83` returned rc 0, `RECEIPT record-sweep-r87.txt expect=met met problems=-`, and the exact r87 target tail, including `matched=6 defeated=1 superseded=2 legacy=1 unexpected=0`. The path is not in command argv, contradicting the helper's docstring. This is an unclaimed hole outside the frozen fixture table, not a failure of the narrower frozen r88 predicate. Route as **R89-C2-comment-binding**. No fix made.

## Inputs and evidence boundary

Reviewed requested diff: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 1bd5ec3f d5e2eda494877a85edaa4e287d6ad81843d9a8a1 -- .ufo/waves/round-87/count-c2.py`.

Observed lane HEAD before execution: `9c775ac2131da13c4c4cfdf2b14077184076f557`. Executed pinned blobs, not moving worktree inputs:

| Input | Revision | SHA-256 | Git blob |
|---|---|---|---|
| r87 gate | `d5e2eda494877a85edaa4e287d6ad81843d9a8a1` | `7e577f533e1dac676d3f5b3d601f2c4c622c57c325e6091e6018b5781ae73fc0` | `7acdeb2e8f78116f17c1bf62d2c7a1c25f9c7f1b` |
| frozen r88 instrument | `2a5e3ad96deb978ed1fb958e87b4be8221fb23b7` | `8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7` | `1e162d86b301cd41cbacc9f371a9dbd1b0b8a21c` |

LSP unavailable: `read xd://lsp` returned `No such tool`; therefore references, definitions and diagnostics could not be queried. Line/caller evidence below comes from source inspection and execution, not semantic-index proof. No installs. No lane mutations except this assigned report. All fixture writes/commits were in seat scratch clones. Scratch was deleted by EXIT trap after execution.

## Refusal-path table

All ranges refer to pinned r87 `count-c2.py` above.

| Rule | Exact definition | Production call site | Refusal propagation |
|---|---|---|---|
| `declared_replay_problem` | 133–137 | `grade_population`, 261–263 | Required/clone row with parsed replay `None` appends `missing-replay`; not clean at 303, expected-met failure increments unexpected/clears ok at 312–316. Replay is skipped at 295. |
| `binding_problems` | 140–145 | `grade_population`, 264–266 | Active on declared required/clone or any parsed replay marker. Any missing whitespace token appends `cmd-binding`; same clean/ok failure path. Replay still executes at 295–302; this is grading refusal, not execution prevention. |
| `absent_supersede_targets` | 148–150 | `grade_population`, 323–326 | Target outside present receipt basenames increments unexpected, emits `SUPERSEDE ... absent=1`, clears ok. This was an existing inline check extracted to a helper, not a new rejection policy. |

Canonical run: `main` calls `grade_population` at 479, serializes counts at 482–487, and returns rc 1/C2=unmet if `not ok or tail != TARGET` at 497–499; only 500–501 emits C2=met/rc 0. Selftest helper calls are at 399–415 (six new arms). No alternative runtime or admission path was used.

## Every population row evaluated

Population definition: 39–47. Both row helpers are called for every present row; `declared_replay_problem` only imposes its requirement on required/clone rows, and `binding_problems` immediately skips the three real legacy rows. Supersede helper examines collected declarations after the loop.

| Receipt (under `.ufo/waves/`) | Declared mode | Replay/binding enforcement | Supersedes |
|---|---|---|---|
| `round-85/evidence/after-r85.txt` | legacy | skipped; header-only | none |
| `round-85/evidence/record-sweep-r85.txt` | legacy | skipped; header-only | none |
| `round-85/evidence/claim-sweep-r85.txt` | legacy | skipped; header-only | none |
| `round-86/evidence/after-c1-r86.txt` | required | active | none |
| `round-86/evidence/replay-defeat-r86.txt` | required, expected reject | active; real `replay-mismatch` remains defeated | none |
| `round-87/evidence/record-sweep-r87.txt` | clone | active | `record-sweep-r85.txt` |
| `round-87/evidence/claim-sweep-r87.txt` | clone | active | `claim-sweep-r85.txt` |

## Measured fixture outcomes

All mutations were committed over d5e2eda in `git clone --shared` scratch fixtures, then graded by the same pinned gate using its normal CLI.

| Fixture | Fixture revision | rc | Observed class and verdict |
|---|---|---|---|
| frozen stripped | `0cec57e01b62b44c8af0d58154de0ccd7ff7349d` | 1 | `record-sweep-r87.txt ... failed problems=missing-replay`; C2=unmet; correct class |
| frozen vacuous | `f950b5b35d085651f817feef452343cdf3692923` | 1 | `record-sweep-r87.txt ... failed problems=cmd-binding`; C2=unmet; correct class |
| frozen absent-target | `57159e0b196eb850f45f102f2c27018188560ede` | 1 | `SUPERSEDE claim-sweep-r87.txt target=gone-r88.txt absent=1`; C2=unmet; correct class |
| **new required-none** | `a2f476abbdc8fcef69fa91d1df22fbda6be4b526` | 1 | On after-c1-r86, replace required with `# replay: none` plus `# no-replay: explicit reason words`; `failed problems=missing-replay`; correct declared-required refusal, no replay of this row |
| **new comment-binding** | `a010047c4819f404146323f23ccc4c24c6719e83` | 0 | Fabricated body accepted, `problems=-`; unclaimed hole detailed above |

For both frozen stripped/vacuous fixtures: `matched=5 defeated=1 superseded=1 legacy=2 unexpected=1`, and rc 1. Thus the r87 target line is unreachable for those exact two modifications, individually (and source propagation prevents either failing expected-met row from making `ok` true). The stronger claim that arbitrary vacuous commands are closed is false: the comment variant restores the target line. Missing header closure itself is enforced by declared population mode, independent of body contents.

## No-regression and frozen result

Normal seven-receipt run, rc 0:

```text
C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=d5e2eda49487
```

Frozen instrument run, rc 0 (includes pristine 23-arm selftest check):

```text
REAL rc=0 C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=d5e2eda49487
FX clean rc=0 refused C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=d5e2eda49487
FX stripped rc=1 refused problems=missing-replay
FX vacuous rc=1 refused problems=cmd-binding
FX absent-target rc=1 refused supersede-absent=1
C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23 rev=d5e2eda49487
```

The instrument's `FX clean ... refused` wording means expected fixture outcome matched, not actual rejection of clean data; clean rc is 0.

Residual risk: lexical binding is not execution provenance. Five counterfeit executions do not establish saturation. Resume continuity, runtime rerouting and host remediation are outside this changed receipt-gate scope; no claim is made about them. Verification gap: no LSP device available. All behavioral verdicts above were executed, not copied from siblings.

Self-evaluation: accuracy 4 (LSP unavailable, compensated by pinned execution); completeness 5 (three frozen and two new cases, all rows/calls covered); clarity 4 (long evidence appendix); actionability 5 (concrete R89 bypass); conciseness 4 (reproduction retained for audit). Overall 4.4/5. Improvement priority: preserve semantic diagnostics when the device is available; keep broad provenance claims separate from fixture closure. The measured distinction should be reproducible by the user.

## Exact executed command and driver

The following invocation produced the evidence above; the driver was created in the named seat scratch and removed with all clones by its EXIT trap:

```sh
S=/fast/scratch/hyaku/mori-r88/Mo88R02ReviewC2; trap 'rm -rf -- "$S"' EXIT; TMPDIR="$S" PYTHONDONTWRITEBYTECODE=1 python3 -I "$S/review.py"
```

Executed `review.py` contents:

```python
import os, subprocess, pathlib, importlib.util, hashlib
S=pathlib.Path('/fast/scratch/hyaku/mori-r88/Mo88R02ReviewC2')
R='/home/vgpnk/Projects/shokunin/mori-shokunin'
REV='d5e2eda494877a85edaa4e287d6ad81843d9a8a1'
FREEZE='2a5e3ad96deb978ed1fb958e87b4be8221fb23b7'
os.environ.update(TMPDIR=str(S), PYTHONDONTWRITEBYTECODE='1', GIT_CONFIG_GLOBAL='/dev/null',GIT_CONFIG_SYSTEM='/dev/null')
def cmd(a):
 p=subprocess.run(a,text=True,capture_output=True,env=os.environ); assert p.returncode==0,(a,p.stderr); return p.stdout.strip()
def load(name, rev, path):
 b=subprocess.check_output(['git','-C',R,'show',rev+':'+path]); p=S/(name+'.py');p.write_bytes(b)
 print('INPUT',rev,path,'sha256='+hashlib.sha256(b).hexdigest())
 spec=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m,str(p)
f,fp=load('frozen',FREEZE,'.ufo/waves/round-88/count-c2.py')
g,gp=load('graded',REV,'.ufo/waves/round-87/count-c2.py')
# Guard each checkout performed by the frozen driver before it mutates a scratch clone.
orig=f.run
def guarded(args,**kwargs):
 if args[:2]==['git','-C'] and 'checkout' in args:
  assert cmd(['git','-C',args[2],'rev-parse','--show-toplevel'])==str(pathlib.Path(args[2]).resolve())
 return orig(args,**kwargs)
f.run=guarded
print('FROZEN_MAIN_BEGIN'); rc=f.main([REV,'--repo',R,'--scratch',str(S/'frozen-run')]);print('FROZEN_MAIN_RC',rc)
rc,out=f.run_graded(gp,R,REV,str(S),'real'); print('REAL_RC',rc);print(out)
for kind,path,_,_ in f.FIXTURES:
 if kind=='clean':continue
 d,rev=f.clone_fixture(R,REV,str(S),kind,path)
 assert d is not None,rev
 rc,out=f.run_graded(gp,d,rev,str(S),kind+'-review')
 print('FROZEN_DETAIL',kind,'rev='+rev,'rc='+str(rc));print(out)
for kind in ('required-none','comment-binding'):
 d=S/('new-'+kind);cmd(['git','clone','--shared','-q',R,str(d)])
 assert cmd(['git','-C',str(d),'rev-parse','--show-toplevel'])==str(d)
 cmd(['git','-C',str(d),'checkout','-q',REV])
 if kind=='required-none':
  path='.ufo/waves/round-86/evidence/after-c1-r86.txt';p=d/path
  text=p.read_text().replace('# replay: required\n','# replay: none\n# no-replay: explicit reason words\n')
 else:
  path='.ufo/waves/round-87/evidence/record-sweep-r87.txt';p=d/path
  text=f.mutate_receipt(p.read_text(),'vacuous')
  fields,_=g.header_fields(g.header_and_body(text)[0]);comment=' # '+' '.join(bp for _,bp in fields['bindings'])
  text='\n'.join(line+comment if line.startswith('# cmd:') else line for line in text.splitlines())+'\n'
 print('NEW_MUTATION',kind,'path='+path)
 for line in text.splitlines():
  if line.startswith(('# cmd:','# replay:','# no-replay:')): print(line)
 p.write_text(text)
 assert cmd(['git','-C',str(d),'rev-parse','--show-toplevel'])==str(d)
 cmd(['git','-C',str(d),'add','--',path]);cmd(['git','-C',str(d),'-c','user.name=t','-c','user.email=t@t','commit','-q','-m','C2 reviewer '+kind])
 rev=cmd(['git','-C',str(d),'rev-parse','HEAD'])
 rc,out=f.run_graded(gp,str(d),rev,str(S),kind);print('NEW_RESULT',kind,'rev='+rev,'rc='+str(rc));print(out)
```

**C2 review: agree** against the exact frozen `C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23`; not an assertion of broad counterfeit resistance. Measured rc 0 for the frozen claim; measured rc 0 for the new comment-binding bypass, routed to round 89.
