# Mo81C01Contract — frozen-contract attack

Scope: critic only; no admission or axis judgment. Axes considered: operability, calibration, coverage, depth, freshness, adjacency. Read the frozen contract, required record sections, r80 lessons and counter fixtures. All implementation reads used freeze `6b021d29`; record cheats used an export of entering `44bc941a`. No lane implementation, contract, git metadata, OS/service/credential/orchestration state changed. Only this report was produced in the lane. No installs; Python and git already present.

## 1. Do-nothing reachability — literal controls resist; HIGH semantic bypass

A literal do-nothing C2 run is red (independently executed):
`C2=unmet pending=3 pinned=1 tool=absent agree=0 rev=44bc941a0e3e`, rc 1.
C1's committed control (`evidence/controls-r81.txt:21-30`) is red wrong=7; I did not rerun its git-creating fixture machinery. This is receipt evidence, not independent C1 remeasurement.

Scratch attempts, using frozen C2 `grade()` on the exported tree:

| attempt | pending | pinned | tool | agree | met |
|---|---:|---:|---|---:|---|
| entering, no modification | 3 | 1 | absent | 0 | false |
| add all-zero record-sweep stub only | 3 | 1 | present | 0 | false |
| delete pinned capability rows + stub | 3 | 1 | present | 0 | false |
| correct pin to measured 233 + lowercase `pending` + stub | 0 | 0 | present | 1 | **true** |
| correct pin + delete the three unresolved claim rows + stub | 0 | 0 | present | 1 | **true** |
| lowercase pending + empty bindings + stub, leave original stale numeric claim | 0 | 0 | present | 1 | **true** |

**HIGH:** P-C2 can pass without measured after-values, and even with `pointers=232` still present by erasing bindings. `count-c2.py:73` exact-uppercase matching is deliberately frozen (`contract.md:104-105`); lowercase is a named tradeoff, NOT grounds to silently change the predicate. Deleting the pending rows is not blocked by the row-retention language at `contract.md:98-100`, which only protects the pinned capability row. Mutable binding population (`count-c2.py:101-111,125`) creates a second authority for what must be checked. The stub demonstrates `tool=present agree=1` is not proof of a conformant gate.

Smallest safe correction: keep frozen counter output honest and add an explicit independent acceptance check for the original three claim identities, measured values/revisions, retained capability row, and frozen binding population; exercise the tool's dirty fixtures. If those are intended predicate requirements, canonical authority must reject/resolve the claim-vs-predicate gap, not rewrite this freeze. Literal do-nothing is excluded; non-work masquerading as record correction is not.

## 2. Vacuous / over-broad arms — mixed fixtures discriminate; HIGH rc omission

The exact frozen seven expectations include four unmet and three met; always-met stub yields wrong=4; always-unmet yields wrong=3. Thus refusal of everything cannot reach wrong=0. The discrimination selftest was executed with only fixture git creation replaced by ordinary file writes: stub counters never inspect revisions. Output: `C1_COUNTER_SELFTEST pass=7 fail=0`, rc 0. Forcing the grader to return unmet for every fixture made that same selftest print `pass=6 fail=1`, rc 1. The check can fail; this is not arithmetic-only assurance.

**HIGH:** `count-c1.py:168-170,178-180,270-275` records but ignores child exit status. A scratch counter chose expected verdict by fixture directory (`a2/a3/a4/b1` -> unmet, others -> met) and exited **2 for every call**. Observed: `C1_EXIT2_EXPECTATION_STUB wrong=0`, all seven rc=2, and `C1_EXIT2_REAL {'C1': 'met', 'C3': 'met'}`. Consequently the exact aggregation condition would report C1 met, despite `contract.md:58` saying “setup (rc 2) never satisfies a met expectation.” This is a contract/implementation defect, not a named tradeoff. It also permits fixture-aware identity cheating: the finite fixture suite does not prove general correctness. I did not claim an actual lane defect or execute a whole CLI synthetic revision.

Smallest safe correction: require `(met, rc=0)` or `(unmet, rc=1)` for each graded call, classify rc=2 as setup regardless of text, and add an able-to-fail rc=2+met arm. Frozen-grade changes require canonical authority, not this seat. Impact: operability, calibration, coverage.

**MEDIUM:** C2 additionally accepts a second stale matching row after a correct first one: `pending=0 pinned=0 tool=present agree=1 met=True` with appended `| tools/mori-claim-sweep.py | pointers=999 |`. Evidence: `count-c2.py:78-86`, with a selftest explicitly endorsing first-row behavior at :187-189. This repeats the exact first-row exposure being repaired in C1 A4. `contract.md:96-98` promises conflicts in readings of the same key mismatch, but its explicit `live_value` example only covers command stdout. Smallest safe correction: report this ambiguity and independently reject conflicting matching carrier rows; do not silently broaden the frozen first-row grade. Impact: calibration, depth.

## 3. Freeze order — LOW, no tracked freeze defect observed

Executed:

```text
git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --format='%h %ct %cI %s' -- .ufo/waves/round-81/
19765553 1793774630 2026-11-04T03:43:50-03:00 round-81: w1 wave spec (14 seats, validated) + dispatch + ready handoff
6b021d29 1793774514 2026-11-04T03:41:54-03:00 round-81: freeze contract + two revision-agnostic counters + do-nothing controls

stat -c '%n mtime=%Y %y' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/w1.ready
/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/w1.ready mtime=1793774623 2026-11-04 03:43:43.985380195 -0300

git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 6b021d29 19765553 -- .ufo/waves/round-81/contract.md .ufo/waves/round-81/count-c1.py .ufo/waves/round-81/count-c2.py .ufo/waves/round-81/record-pins.json .ufo/waves/round-81/evidence/controls-r81.txt
(no output)
```

Freeze predates ready by 109 seconds (mtime has fractional seconds). No tracked graded-value changes through observed dispatch commit. This does not prove future commits or uncommitted worktree bytes are frozen; all adversarial grading above deliberately used `git show 6b021d29:...`. No correction needed to observed chronology. Filesystem mtime is evidence of ordering, not cryptographic provenance.

## 4. Causal separability — MEDIUM, directional dependency

Commands (not executed here for landed R):

```text
python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c1.py R --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch /fast/scratch/hyaku/mori-r81/L1
python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c2.py R --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch /fast/scratch/hyaku/mori-r81/L1
```

C1 does not require C2's tool to exist (the entering committed control already has real_c1=met and real_c3=met while the tool is absent). C2 does not invoke C1's new counter or need its fixes. However, adding C2's tool without its PROVINCE inventory row makes C1's real C3 arm fail; this is expressly acknowledged by `contract.md:135-136`. Also C2's pinned command invokes the r80 sweep; correcting a pointer-bearing row can change its own pointer count. Thus implementations are separable with the inventory obligation honored, not independent of all C2 tree changes. Smallest safe correction: describe that directional no-harm obligation explicitly in the lesson/report; no freeze rewrite. Impact: coverage, calibration, operability.

## 5. No-harm — HIGH observability limit; MEDIUM undefined battery scope

- Historical real bytes at entering are testable with the **landed r80 counters** plus entering rev and explicit `--repo/--scratch`. C1's `grade_real` currently uses R, not entering (`count-c1.py:271`); this cannot certify `contract.md:131-133`'s historical unchanged requirement by itself. Cheapest check: separately run landed count-c1/count-c3 at `44bc941a`, and compare expected receipt fields. Not run here.
- Frozen r80 contract identity is testable: `git diff --exit-code 44bc941a R -- .ufo/waves/round-80/contract.md`. No ambiguity; not run at a landed R here.
- “Standing instrument battery stays green” (`contract.md:134`) has no enumerated battery or environment in this contract. Cheapest check: use the thirteen commands in `.ufo/waves/round-80/evidence/battery-r80.txt`, pin that list in the new receipt, set allowed scratch/TMPDIR, retain per-command rc and setup diagnostics. A selftest returning 0 after SETUP is not a pass (QUALITY 167). No battery executed here.
- Census exit 0 and PROVINCE inventory are testable at landed bytes with the existing census and r80 C3 counter. Neither run at landed bytes by this seat.
- **HIGH:** “no lane ... state changed” (`contract.md:137`) literally contradicts intended lane code/record changes. The useful interpretation is no operational state remediation outside allowed source/report changes. A final git tree cannot prove no transient host/unit/credential/orchestration write occurred. Cheapest useful check: append a precise scope interpretation, retain before/after scoped tree diffs and command/process-write audit evidence; do not claim this proves all transient host behavior absent. This seat made no such changes, but cannot attest other seats. Impact: adjacency, calibration.

## 6. Claim-vs-counter drift — HIGH acceptance gap; LOW documentation drift

C1 contract P-C1 (`contract.md:40-42`):
`C1=met wrong=0 fixtures=7 real_c1=met real_c3=met rev=<sha12>`; entering `C1=unmet wrong=7`, rc 1.
Counter printer (`count-c1.py:272-275`):
`C1=%s wrong=%d fixtures=%d real_c1=%s real_c3=%s rev=%s`.
Successful label matches the frozen sentence. But rc=2 children can populate the exact successful label (§2), so the printed identity exceeds what was checked. Docstring :11 says entering `wrong>=6`, whereas the contract says `wrong=7`: **LOW** documentation drift; append an erratum to lesson/report rather than edit freeze.

C2 contract P-C2 (`contract.md:80-83`):
`C2=met pending=0 pinned=0 tool=present agree=1 rev=<sha12>`; entering `C2=unmet pending=3 pinned=1 tool=absent agree=0`, rc 1 with frozen pins.
Counter printer (`count-c2.py:313-316`):
`C2=%s pending=%d pinned=%d tool=%s agree=%d rev=%s`.
Labels match; entering line was independently reproduced exactly. But Claim at `contract.md:71-76` also promises D80-2 pending-wording and D80-4 precision discharge “as append-only corrections” plus measured r80 after-values. The counter checks neither wording, correction attribution, measured revision, nor claim-row survival. D80-4 is explicitly excluded at :104; exact-cell scope is explicit at :105. **HIGH:** a passing label is evidence for P-C2's narrow fields, not evidence that the whole prose claim was completed. Deleting/rewording after-cells (§1) demonstrates this, rather than merely inferring it. Smallest safe correction: independently check the promised corrections and report their evidence separately; canonical judge must distinguish that fulfillment from the narrow keeper.

## Commands, evidence boundaries, own defects

Actual entry-control command executed:

```text
python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c2.py 44bc941a0e3e9676fa33a882b43d6e9793cbf74d --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch /fast/scratch/hyaku/mori-r81/Mo81C01Contract --pins /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/record-pins.json
C2=unmet pending=3 pinned=1 tool=absent agree=0 rev=44bc941a0e3e
rc=1
```

Created scratch with `mkdir -p /fast/scratch/hyaku/mori-r81/Mo81C01Contract` (no output, rc 0). Executed `python3 -I /fast/scratch/hyaku/mori-r81/Mo81C01Contract/probe.py` (rc 0), whose durable source is below. This initial invocation ran through `C1_RC_CONTRADICTION`; final appended lines were executed by the continuation command below. The initial run mistakenly sampled live=229 **after deleting capability rows**, then called it a corrected pin: those initial `C2_CORRECTED_PIN_ONLY`, `C2_LOWERCASE_PENDING`, `C2_DELETE_PENDING_ROWS`, and `C2_SECOND_STALE_ROW` red readings did not isolate the intended changes. Corrected continuation restored the entering record first and remeasured 233. Do not use 229 as the entering count.

An initial continuation used `s[:10]`, cut at a function opener, and failed with `IndentationError: expected an indented block after function definition on line 10`, rc 1, before executing probes. Successful exact continuation (rc 0):

```sh
python3 -I -c 'from pathlib import Path; p=Path("/fast/scratch/hyaku/mori-r81/Mo81C01Contract/probe.py"); s=p.read_text().splitlines(); exec("\n".join(s[:9])); tree=S/"tree"; pins=tree/c2.DEFAULT_PINS; card=tree/"SCORECARD.md"; original=subprocess.check_output(["git","-C",str(L),"show",R+":SCORECARD.md"],text=True); bind=json.loads((L/c2.DEFAULT_PINS).read_text())["bindings"][0]; grade=lambda label: print(label,c2.grade(str(tree),str(pins))); fixtures=[(label,counter,expected,str(S/"stubs-fixtures"/part),"unused-for-stubs") for label,counter,expected,part in [("A2","count-c1","unmet","a2"),("A3","count-c1","unmet","a3"),("A4","count-c1","unmet","a4"),("A5","count-c1","met","a5/dir with space/lane"),("B1","count-c3","unmet","b1"),("B2","count-c3","met","b2"),("B6","count-c3","met","b6")]]; exec("\n".join(s[50:]))'
```

Successful continuation output:
```text
RESTORED_PINNED_LIVE 233 rc=0
ISOLATED_LOWERCASE_PENDING ({'pending': 0, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': True}, None)
ISOLATED_DELETE_PENDING_ROWS ({'pending': 0, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': True}, None)
ISOLATED_SECOND_STALE_ROW ({'pending': 0, 'pinned': 0, 'tool': 'present', 'agree': 1, 'met': True}, None)
C1_EXIT2_EXPECTATION_STUB wrong=0 [('A2', 'unmet', 'unmet', 2), ('A3', 'unmet', 'unmet', 2), ('A4', 'unmet', 'unmet', 2), ('A5', 'met', 'met', 2), ('B1', 'unmet', 'unmet', 2), ('B2', 'met', 'met', 2), ('B6', 'met', 'met', 2)]
C1_EXIT2_REAL {'C1': 'met', 'C3': 'met'}
```

No actual C1 full-CLI synthetic revision, landed revision keeper, battery, census, or host-write audit was executed. Synthetic exports are not committed lane revisions; findings concern frozen grader logic, not an assertion that L1 has landed those cheats. No defects alleged in a sibling's in-flight bytes: all cited defects are in frozen contract/counters and entering records. No git mutation was run, even in scratch. Scratch removed with the cleanup command recorded in the terminal handoff.

Self-evaluation: accuracy 4 (C1 full CLI intentionally not exercised); completeness 4 (landed no-harm remains unmeasured, stated explicitly); clarity 4 (distinguishes named tradeoffs from implementation breach); actionability 4 (minimal corrections named but frozen-authority decisions remain canonical); conciseness 4 (source appendix retained for reproducibility). Overall 4.0. Highest-impact next check is rc-sensitive C1 discrimination at the canonical review, not retroactive claim expansion. User should agree with this bounded evidence assessment.

## Durable scratch probe source

Reconstruction: save the following under the same allowed scratch directory and run in a fresh directory; the source below includes the appended isolation probes. It replaces git fixture construction only for revision-ignoring stub checks. All record reads still use the frozen counter functions and actual exported entering bytes.

```python
import pathlib, subprocess, types, json, os
L=pathlib.Path('/home/vgpnk/Projects/shokunin/mori-shokunin')
S=pathlib.Path('/fast/scratch/hyaku/mori-r81/Mo81C01Contract')
R='44bc941a0e3e9676fa33a882b43d6e9793cbf74d'
def load(name):
    source=subprocess.check_output(['git','-C',str(L),'show','6b021d29:.ufo/waves/round-81/'+name],text=True)
    m=types.ModuleType(name); m.__file__=str(L/'.ufo/waves/round-81'/name);exec(compile(source,name,'exec'),m.__dict__);return m,source
c1,src=load('count-c1.py');c2,_=load('count-c2.py')
# Avoid all git mutations: stub counters never inspect fixture revisions.
def repo_without_git(base, files):
    base=pathlib.Path(base);base.mkdir(parents=True,exist_ok=True)
    for name,body in files.items():
        p=base/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body)
    return 'unused-for-stubs'
c1.make_repo=repo_without_git
st=S/'discrimination';st.mkdir()
print('NORMAL_DISCRIMINATION');print('rc='+str(c1.selftest(str(st))))
mut=types.ModuleType('mutant');exec(compile(src,'mutant','exec'),mut.__dict__);mut.make_repo=repo_without_git
# A broken grader that calls every expected-met fixture unmet must make selftest red.
mut.grade_fixtures=lambda counters,fixtures,scratch:[(label,expected,'unmet',1) for label,_,expected,_,_ in fixtures]
ms=S/'mutant';ms.mkdir();print('BROKEN_GRADER_SELFTEST');print('rc='+str(mut.selftest(str(ms))))
fixtures=c1.build_fixtures(str(S/'stubs-fixtures'))
for value,rc in [('met',0),('unmet',1)]:
    p=S/('always-'+value);p.mkdir()
    for counter,word in [('count-c1','C1'),('count-c3','C3')]:
        (p/(counter+'.py')).write_text("import sys\nprint('%s=%s stub')\nsys.exit(%d)\n"%(word,value,rc))
    rows=c1.grade_fixtures(str(p),fixtures,str(S));print('STUB',value,'wrong='+str(sum(expected!=got for _,expected,got,_ in rows)), 'results='+repr(rows))
# Export entering tree, without writing git metadata.
tree=S/'tree';print('EXPORT_ENTERING',c2.export(str(L),R,str(tree)))
pins=tree/c2.DEFAULT_PINS;pins.parent.mkdir(parents=True,exist_ok=True);pins.write_text((L/c2.DEFAULT_PINS).read_text())
def grade(label):
    verdict,error=c2.grade(str(tree),str(pins));print(label,json.dumps(verdict,sort_keys=True),repr(error))
grade('C2_ENTERING')
card=tree/'SCORECARD.md';original=card.read_text()
# Sole extra change for these record cheats is a vacuous all-zero sweep.
tool=tree/c2.TOOL;tool.write_text("print('RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=1')\n")
grade('C2_STUB_ONLY')
card.write_text('\n'.join(line for line in original.splitlines() if 'tools/mori-claim-sweep.py' not in line));grade('C2_DELETE_PINNED_ROWS')
# Use the live pinned number from the unchanged command, not a forged replacement.
bind=json.loads(pins.read_text())['bindings'][0]
live=c2.run(bind['command'],cwd=str(tree));value=c2.live_value(live.stdout,'pointers');print('PINNED_LIVE',value,'rc='+str(live.returncode))
corrected=original.replace('pointers=232','pointers='+str(value))
card.write_text(corrected);grade('C2_CORRECTED_PIN_ONLY')
card.write_text(corrected.replace('| PENDING |','| pending |'));grade('C2_LOWERCASE_PENDING')
card.write_text('\n'.join(line for line in corrected.splitlines() if '| PENDING |' not in line));grade('C2_DELETE_PENDING_ROWS')
# Conflicting claim rows, first correct, later stale.
card.write_text(corrected.replace('| PENDING |','| measured |')+'\n| tools/mori-claim-sweep.py | pointers=999 |\n');grade('C2_SECOND_STALE_ROW')
# Preserve all entering debt but erase the binding authority.
card.write_text(original.replace('| PENDING |','| pending |'));pins.write_text(json.dumps({'schema':'mori-record-pins-v1','bindings':[]}));grade('C2_EMPTY_BINDINGS')
print('C1_RC_CONTRADICTION',c1.verdict('C1=met\n','C1'),'child_rc=2 (grade_fixtures and grade_real ignore rc)')
card.write_text(original)
pins.write_text((L/c2.DEFAULT_PINS).read_text())
live=c2.run(bind['command'],cwd=str(tree));value=c2.live_value(live.stdout,'pointers')
print('RESTORED_PINNED_LIVE',value,'rc='+str(live.returncode))
corrected=original.replace('pointers=232','pointers='+str(value))
card.write_text(corrected.replace('| PENDING |','| pending |'));grade('ISOLATED_LOWERCASE_PENDING')
card.write_text('\n'.join(line for line in corrected.splitlines() if '| PENDING |' not in line));grade('ISOLATED_DELETE_PENDING_ROWS')
card.write_text(corrected.replace('| PENDING |','| measured |')+'\n| tools/mori-claim-sweep.py | pointers=999 |\n');grade('ISOLATED_SECOND_STALE_ROW')
bad=S/'exit2';bad.mkdir()
for counter,word in [('count-c1','C1'),('count-c3','C3')]:
    (bad/(counter+'.py')).write_text("import sys,pathlib\np=pathlib.Path(sys.argv[sys.argv.index('--repo')+1]);v='unmet' if p.name in ('a2','a3','a4','b1') else 'met'\nprint('%s='+v)\nsys.exit(2)\n"%word)
rows=c1.grade_fixtures(str(bad),fixtures,str(S))
print('C1_EXIT2_EXPECTATION_STUB','wrong='+str(sum(expected!=got for _,expected,got,_ in rows)),repr(rows))
print('C1_EXIT2_REAL',c1.grade_real(str(bad),str(L),R,str(S)))

```
