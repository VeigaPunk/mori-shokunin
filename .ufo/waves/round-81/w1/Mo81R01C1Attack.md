# Mo81R01C1Attack — adversarial C1 review

Axes: operability, calibration, coverage, depth, freshness, adjacency. Detection/report only; recommendation, not admission.

## Findings by severity

| Severity | Finding | Evidence / action |
|---|---|---|
| HIGH | Setup exits can satisfy `met` expectations | `.ufo/waves/round-81/count-c1.py:169-170,180,270`: verdict extraction reads labels without binding rc; final aggregation discards rc. Fault injection leaves all actual counter stdout intact, changes Python-child rc to 2, and still prints `C1=met wrong=0` rc 0. Frozen contract :57-59 explicitly excludes this. Bind labels to their matching exits in fixture and real arms. |
| LOW | Aggregation mutation is not guarded by discrimination selftests | A single in-memory replacement at `.ufo/waves/round-81/count-c1.py:270`, `wrong = 0`, yields met at entering with all seven observed fixture failures. This is mutation evidence, NOT a claim that pristine line 270 currently does this. |

No BLOCKER or MEDIUM finding established. The original B2_attack result is NOT an implementation defect: its checkout basename was B2_attack, not mori-shokunin. A corrected independent fixture with the same commit under mori-shokunin passes.

## Numbered verdicts

1. VERDICT: DISAGREE — canonical revision run at observed HEAD `197655534b4a47a3c26149462e78752a6ea03eda` still reads wrong=7; entering reads wrong=7. These commands export revision bytes and therefore do not grade uncommitted fixes. The separate explicit --counters worktree run subsequently reads wrong=0 with both real arms met. This is NOT a landed-revision pass.
2. VERDICT: AGREE — fourteen independent shapes, with the B2 identity correction, behave as expected at the observed worktree. See the table and complete driver/output below. Boundary `CLAIM_SWEEP_MISMATCH` plus exit 1 and a zero summary correctly gives unmet, not setup; a single nonzero unresolved summary correctly gives unmet. Neither is a legitimate green C1 result.
3. VERDICT: AGREE — exact requested r80 contract diff is empty, rc 0. Actual diff inspection shows unchanged r80 graded output token order and return/print templates; logic and selftest changes do not add/remove result fields. Multiple contradictory summaries now report component maxima instead of silently choosing the first; token grammar remains unchanged.
4. VERDICT: DISAGREE — false greens are constructible: exact one-line aggregation mutant at r81 count-c1.py:270 and a more meaningful exit/status consistency fault described above. Neither experiment writes a counter or counter fixture.

## Independent fixture table

| Fixture | Shape | Expected | Observed |
|---|---|---|---|
| A2 attack | unresolved mismatch line then zero summary, rc 0 | unmet | unmet rc 1 |
| A2 boundary | same protocol, producer rc 1 | unmet, not setup | unmet rc 1 |
| A3 attack | zero summary then mismatches=2 summary | unmet | unmet rc 1 |
| A3 boundary | single summary unresolved=2, mismatches=0 | unmet | unmet rc 1 |
| A4 attack | two rows with tallies 19 then 17 | unmet | unmet rc 1 |
| A4 boundary | two identical rows, tally 19 | met | met rc 0 |
| A5 attack | conformant repo AND scratch paths with spaces | met | met rc 0 |
| A5 boundary | same clean fixture, no spaces | met | met rc 0 |
| B1 attack | docs/tools/x.py only, real tools/x.py | unmet | unmet rc 1 |
| B1 boundary | tools/x.py only in fenced block | met | met rc 0 |
| B2 attack corrected | mori-shokunin/tools/x.py in checkout mori-shokunin | met | met rc 0 |
| B2 boundary | other-shokunin/tools/x.py only | unmet | unmet rc 1 |
| B6 attack | real tools/x.py and directory tools/y.sh holding child | met | met rc 0 |
| B6 boundary | same names in fenced block | met | met rc 0 |

NAMED LIMIT: own identity = basename of the graded repo path; a lane whose checkout directory name differs from the repo name it uses in PROVINCE will reject its own tool path. Identity agreement holds for this lane today (the directory is mori-shokunin); mismatching checkout names fail safe (red, never green). The raw B2_attack transcript below intentionally preserves my initially incorrect expected met; the corrected same-commit run resolves it.

## Scope, freshness, verification gaps

Produced only `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/w1/Mo81R01C1Attack.md` permanently. Scratch driver and direct loose-object fixture repositories are removed at completion. No tool installs/updates. No direct mutating git commands were issued by this reviewer; requested canonical harness itself creates and commits its scratch fixture repos. Independent variants construct their own loose Git objects and use only read-only git subprocesses.

The r80 counter files were unmodified on the first diff/read; E01/E02 changes arrived during the review and are reflected in the variant probes. The B2 canonical fixture path was changed by L1 during review to b2/mori-shokunin; I did not change it. Expected verdict and frozen contract remain unchanged. This chronology is why revision and worktree results differ.

LSP unavailable: reading xd://lsp returned `No such tool`; no semantic server status/references/definition/diagnostics could be requested. Text inspection is not semantic proof. No resume/runtime-routing/saturation implementation is changed in these files; those review axes are not applicable here. No standing battery, fleet state or live host instrumentation exercised. No final landed SHA was supplied before report production: required integration command is `python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c1.py <landed-sha> --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch <owned-scratch>`. Such an after-run remains L1-owned unless separately appended as actually exercised evidence.

Hash snapshot after worktree probes (files can continue changing under other owners):
- `.ufo/waves/round-80/count-c1.py`: `45830b52dd153b6295beab435a3116cfd3aa0b54b6f75cf366db06301c323d6f`
- `.ufo/waves/round-80/count-c3.py`: `3d91cb77864ad5eea82b5013a2e9f8bbc2632c30e6064c512f707a0a877273ba`
- `.ufo/waves/round-81/count-c1.py`: `32c8f3af2f42fce5ebccec0b5df1f1c74a77e4b02c567b882dae0398c0f812d8`

## Independent driver (retained source for reproduction)

```python
import os, pathlib, hashlib, zlib, subprocess, concurrent.futures, json
L=pathlib.Path('/home/vgpnk/Projects/shokunin/mori-shokunin')
S=pathlib.Path('/fast/scratch/hyaku/mori-r81/Mo81R01C1Attack')
# Construct isolated git object stores directly: no mutating git command.
def repo(name,files):
 p=S/name; (p/'.git/objects').mkdir(parents=True); (p/'.git/refs/heads').mkdir(parents=True)
 (p/'.git/HEAD').write_text('ref: refs/heads/probe\n'); (p/'.git/config').write_text('[core]\n repositoryformatversion = 0\n bare = false\n')
 def obj(kind,data):
  raw=kind.encode()+b' '+str(len(data)).encode()+b'\0'+data; h=hashlib.sha1(raw).hexdigest(); q=p/'.git/objects'/h[:2]/h[2:]; q.parent.mkdir(exist_ok=True); q.write_bytes(zlib.compress(raw)); return h
 root={}
 for path,body in files.items():
  d=root; parts=path.split('/')
  for part in parts[:-1]: d=d.setdefault(part,{})
  d[parts[-1]]=body
 def tree(d):
  out=b''
  for n,v in sorted(d.items(),key=lambda kv:kv[0]+('/' if isinstance(kv[1],dict) else '')):
   kind='40000' if isinstance(v,dict) else '100644'; h=tree(v) if isinstance(v,dict) else obj('blob',v.encode()); out+=kind.encode()+b' '+n.encode()+b'\0'+bytes.fromhex(h)
  return obj('tree',out)
 h=obj('commit',('tree '+tree(root)+'\nauthor probe <probe@invalid> 1 +0000\ncommitter probe <probe@invalid> 1 +0000\n\nindependent fixture\n').encode()); (p/'.git/refs/heads/probe').write_text(h+'\n'); return p,h
Z='CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=2 pointers=9'
M='CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:7 tools/absent.py'
R='| independent (`tools/mori-control-receipt.py`) | x | selftest %d in-memory cases | 79 |\n'
def af(lines,rc=0,rows=(19,)):
 return {'tools/mori-claim-sweep.py':'import sys\n'+''.join('print('+repr(x)+')\n' for x in lines)+'sys.exit(%d)\n'%rc,'tools/mori-control-receipt.py':"print('CONTROL_RECEIPT_SELFTEST pass=19 fail=0')\n",'.ufo/waves/round-80/claim-pins.json':'{}','SCORECARD.md':'| Capability | What | Evidence | First |\n|---|---|---|---|\n'+''.join(R%x for x in rows)}
def bf(text,files=('x.py',)):
 return dict({'PROVINCE.md':text},**{'tools/'+x:'# independent\n' for x in files})
cases=[('A2_attack','c1','unmet',af([M,Z])),('A2_boundary','c1','unmet',af([M,Z],1)),('A3_attack','c1','unmet',af([Z,Z.replace('mismatches=0','mismatches=2')])),('A3_boundary','c1','unmet',af([Z.replace('unresolved=0','unresolved=2')])),('A4_attack','c1','unmet',af([Z],rows=(19,17))),('A4_boundary','c1','met',af([Z],rows=(19,19))),('A5 space attack','c1','met',af([Z])),('A5_boundary','c1','met',af([Z])),('B1_attack','c3','unmet',bf('`docs/tools/x.py`')),('B1_boundary','c3','met',bf('```text\ntools/x.py\n```')),('B2_attack','c3','met',bf('`mori-shokunin/tools/x.py`')),('B2_boundary','c3','unmet',bf('`other-shokunin/tools/x.py`')),('B6_attack','c3','met',bf('`tools/x.py` and `tools/y.sh`',('x.py','y.sh/child'))),('B6_boundary','c3','met',bf('```text\ntools/x.py\ntools/y.sh\n```',('x.py','y.sh/child')))]
def probe(case):
 name,c,expect,files=case; p,h=repo(name,files); work=S/(name+'-scratch'); work.mkdir(); cmd=['python3','-I',str(L/('.ufo/waves/round-80/count-'+c+'.py')),h,'--repo',str(p),'--scratch',str(work)]; r=subprocess.run(cmd,cwd=S,capture_output=True,text=True); return '$ '+' '.join(cmd)+'\n'+r.stdout+r.stderr+'rc='+str(r.returncode)+' expected='+expect+'\n'
with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
 for result in pool.map(probe,cases): print(result)
```

## Exact executed command/output transcript

`$` lines render argv separated by spaces, not a shell-escaped executable script; driver source above supplies exact argument boundaries. No output elided below. Failed attempts are retained, not counted as passes.

```text
$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c1.py 44bc941a0e3e9676fa33a882b43d6e9793cbf74d --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack
A2_summary_contradicts_mismatch_line expected=unmet got=met rc=0
A3_two_contradicting_summaries expected=unmet got=met rc=0
A4_second_carrier_row_stale expected=unmet got=met rc=0
A5_repo_path_with_space expected=met got=setup rc=2
B1_subdir_path_counts_as_naming expected=unmet got=met rc=0
B2_own_lane_prefix_excluded expected=met got=unmet rc=1
B6_directory_named_as_tool expected=met got=unmet rc=1
C1=unmet wrong=7 fixtures=7 real_c1=met real_c3=met rev=44bc941a0e3e
rc=1
```

```text
$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c1.py HEAD --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack
A2_summary_contradicts_mismatch_line expected=unmet got=met rc=0
A3_two_contradicting_summaries expected=unmet got=met rc=0
A4_second_carrier_row_stale expected=unmet got=met rc=0
A5_repo_path_with_space expected=met got=setup rc=2
B1_subdir_path_counts_as_naming expected=unmet got=met rc=0
B2_own_lane_prefix_excluded expected=met got=unmet rc=1
B6_directory_named_as_tool expected=met got=unmet rc=1
C1=unmet wrong=7 fixtures=7 real_c1=met real_c3=met rev=197655534b4a
rc=1
```

```text
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 44bc941a -- .ufo/waves/round-80/contract.md
rc=0
```

```text
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD
197655534b4a47a3c26149462e78752a6ea03eda
rc=0
```

```text
$ python3 -I /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/probe.py
$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c1.py 96b8b701ebf6e030799ebe76ab323f8aaf7a7f48 --repo /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/A2_attack --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/A2_attack-scratch
C1=unmet tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=96b8b701ebf6
rc=1 expected=unmet

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c1.py deba15963e89dce8e3debf7a8b2607f5d6d26824 --repo /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/A2_boundary --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/A2_boundary-scratch
C1=unmet tool=present sweep=1 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=deba15963e89
rc=1 expected=unmet

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c1.py 3bc13fb0fbadc950a3e1dc3479d4c8497a59c2b6 --repo /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/A3_attack --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/A3_attack-scratch
C1=unmet tool=present sweep=0 mismatches=2 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=3bc13fb0fbad
rc=1 expected=unmet

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c1.py c25ce616aff941e460b815a02945b4c148ff2b1b --repo /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/A3_boundary --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/A3_boundary-scratch
C1=unmet tool=present sweep=0 mismatches=0 unresolved=2 tallies=0 stale=0 row_tally=19 live_tally=19 rev=c25ce616aff9
rc=1 expected=unmet

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c1.py fed35369205b83879816f672b4d8e152d4d8309b --repo /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/A4_attack --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/A4_attack-scratch
C1=unmet tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=None live_tally=19 rev=fed35369205b
rc=1 expected=unmet

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c1.py 07195d431e74dda16917e62a16d95e419c75e7cc --repo /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/A4_boundary --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/A4_boundary-scratch
C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=07195d431e74
rc=0 expected=met

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c1.py dd0824b1842e50ba5ff6e7ea92e3dc981dcc6800 --repo /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/A5 space attack --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/A5 space attack-scratch
C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=dd0824b1842e
rc=0 expected=met

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c1.py dd0824b1842e50ba5ff6e7ea92e3dc981dcc6800 --repo /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/A5_boundary --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/A5_boundary-scratch
C1=met tool=present sweep=0 mismatches=0 unresolved=0 tallies=0 stale=0 row_tally=19 live_tally=19 rev=dd0824b1842e
rc=0 expected=met

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c3.py 042bd289a93606e68a1d0e291a617a54833735d3 --repo /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/B1_attack --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/B1_attack-scratch
C3=unmet named=0 present=1 missing=1 extra=0 rev=042bd289a936
missing_first=x.py
rc=1 expected=unmet

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c3.py 881fadf0b96270b254f89e0bb297ba08e65d5da8 --repo /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/B1_boundary --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/B1_boundary-scratch
C3=met named=1 present=1 missing=0 extra=0 rev=881fadf0b962
rc=0 expected=met

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c3.py 18824d7eef1454d2c80945063a72dced4b23e0da --repo /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/B2_attack --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/B2_attack-scratch
C3=unmet named=0 present=1 missing=1 extra=0 rev=18824d7eef14
missing_first=x.py
rc=1 expected=met

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c3.py d3361564642698277249668183d078623b0b343b --repo /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/B2_boundary --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/B2_boundary-scratch
C3=unmet named=0 present=1 missing=1 extra=0 rev=d33615646426
missing_first=x.py
rc=1 expected=unmet

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c3.py 8f7e9302dd45efa620ddaa7451f458b67d424658 --repo /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/B6_attack --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/B6_attack-scratch
C3=met named=1 present=1 missing=0 extra=0 rev=8f7e9302dd45
rc=0 expected=met

$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c3.py 4b648f9e43ee119fbdbc09f6b1c2ac6086bc20f8 --repo /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/B6_boundary --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/B6_boundary-scratch
C3=met named=1 present=1 missing=0 extra=0 rev=4b648f9e43ee
rc=0 expected=met

rc=0
```

```text
$ python3 -I -c import sys; p='/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c1.py'; s=open(p).read(); old='wrong = sum(1 for _, expected, got, _ in results if expected != got)'; assert s.count(old)==1; s=s.replace(old,'wrong = 0'); sys.argv=[p,'44bc941a0e3e9676fa33a882b43d6e9793cbf74d','--repo','/home/vgpnk/Projects/shokunin/mori-shokunin','--scratch','/fast/scratch/hyaku/mori-r81/Mo81R01C1Attack']; exec(compile(s,p,'exec'),{'__name__':'__main__','__file__':p})
Traceback (most recent call last):
  File "<string>", line 1, in <module>
    import sys; p='/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c1.py'; s=open(p).read(); old='wrong = sum(1 for _, expected, got, _ in results if expected != got)'; assert s.count(old)==1; s=s.replace(old,'wrong = 0'); sys.argv=[p,'44bc941a0e3e9676fa33a882b43d6e9793cbf74d','--repo','/home/vgpnk/Projects/shokunin/mori-shokunin','--scratch','/fast/scratch/hyaku/mori-r81/Mo81R01C1Attack']; exec(compile(s,p,'exec'),{'__name__':'__main__','__file__':p})
                                                                                                                                                                                                      ^^^^^^^^^^^^^^^
AssertionError
rc=1
```

```text
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 44bc941a -- .ufo/waves/round-80/count-c1.py .ufo/waves/round-80/count-c3.py
diff --git c/.ufo/waves/round-80/count-c1.py w/.ufo/waves/round-80/count-c1.py
index 1f1c860b..469f03c4 100755
--- c/.ufo/waves/round-80/count-c1.py
+++ w/.ufo/waves/round-80/count-c1.py
@@ -11,11 +11,11 @@ receipt label are the same sentence):
   SCORECARD.md's control-receipt capability row stating 18 while the committed
   `tools/mori-control-receipt.py --selftest` prints `pass=19 fail=0`.
 
-Second arm (independent of the sweep's pins): the capabilities row that names
+Second arm (independent of the sweep's pins): every capabilities row that names
 `tools/mori-control-receipt.py` states a selftest tally equal to the live `--selftest` count
 of that tool at R. An unparseable or failing tool selftest is a setup error, never a pass.
 
-Named limit (before data): the counter grades the sweep's own verdict plus that one row; it
+Named limit: the counter grades all sweep summaries and mismatch lines plus those rows; it
 does not independently re-derive every pinned tally the sweep checks.
 
 Usage: count-c1.py <rev> [--repo DIR] [--scratch DIR] | count-c1.py --selftest
@@ -42,21 +42,28 @@ def run(cmd, cwd=None):
 
 def export(repo, rev, dest):
     os.makedirs(dest, exist_ok=True)
-    p = subprocess.run(f"git -C {repo} archive {rev} | tar -x -C {dest}",
-                       shell=True, capture_output=True, text=True)
+    archive = subprocess.run(["git", "-C", repo, "archive", rev], capture_output=True)
+    if archive.returncode != 0:
+        return False
+    p = subprocess.run(["tar", "-x", "-C", dest], input=archive.stdout,
+                       capture_output=True)
     return p.returncode == 0
 
 
 def row_tally(text):
-    """The selftest tally stated in the capabilities row naming CAPTOOL, or None."""
+    """Return the common tally across every matching row, or None on disagreement."""
+    readings = []
     for line in text.splitlines():
         if not line.startswith("| "):
             continue
-        if CAPTOOL not in line or "Capability" in line:
+        if CAPTOOL not in line:
             continue
-        m = re.search(r"selftest\s+(\d+)\s+in-memory", line)
-        if m:
-            return int(m.group(1))
+        matches = re.findall(r"selftest\s+(\d+)\s+in-memory", line)
+        if not matches:
+            return None
+        readings.extend(int(value) for value in matches)
+    if readings and len(set(readings)) == 1:
+        return readings[0]
     return None
 
 
@@ -80,17 +87,28 @@ def grade(repo, rev, scratch):
         return 1, "C1=unmet tool=absent sweep=- mismatches=- row_tally=- live_tally=-"
     pins = os.path.join(tree, PINS)
     p = run(["python3", "-I", tool, "--root", tree, "--pins", pins])
-    m = re.search(r"CLAIM_SWEEP mismatches=(\d+) unresolved=(\d+) tallies=(\d+) stale=(\d+)",
-                  p.stdout)
-    if not m:
+    summary_lines = [line.strip() for line in p.stdout.splitlines()
+                     if line.startswith("CLAIM_SWEEP ")]
+    summaries = []
+    for line in summary_lines:
+        m = re.match(r"CLAIM_SWEEP mismatches=(\d+) unresolved=(\d+) "
+                     r"tallies=(\d+) stale=(\d+)(?:\s|$)", line)
+        if m:
+            summaries.append(tuple(int(value) for value in m.groups()))
+    if not summaries:
         return 2, f"C1_SETUP sweep produced no summary rc={p.returncode}"
-    mismatches, unresolved, tallies, stale = (int(m.group(i)) for i in (1, 2, 3, 4))
+    mismatches, unresolved, tallies, stale = map(max, zip(*summaries))
+    sweep_consistent = (len(set(summary_lines)) == 1
+                        and len(summaries) == len(summary_lines)
+                        and not any(line.startswith("CLAIM_SWEEP_MISMATCH")
+                                    for line in p.stdout.splitlines()))
     card = open(os.path.join(tree, "SCORECARD.md"), encoding="utf-8").read()
     stated = row_tally(card)
     live, why = live_tally(tree)
     if live is None:
         return 2, f"C1_SETUP control-receipt selftest {why}"
-    met = (p.returncode == 0 and mismatches == 0 and unresolved == 0
+    met = (p.returncode == 0 and sweep_consistent
+           and mismatches == 0 and unresolved == 0
            and tallies == 0 and stale == 0 and stated == live)
     tail = (f"tool=present sweep={p.returncode} mismatches={mismatches} "
             f"unresolved={unresolved} tallies={tallies} stale={stale} "
@@ -105,15 +123,25 @@ def selfcheck(scratch):
             ("conformant", 0, 19, 19, True),
             ("stale_row", 0, 18, 19, False),
             ("sweep_mismatch", 1, 19, 19, False),
-            ("inconsistent_summary", "0s", 19, 19, False)):
+            ("inconsistent_summary", "0s", 19, 19, False),
+            ("contradicting_summaries", "double", 19, 19, False),
+            ("mismatch_line", "line", 19, 19, False),
+            ("second_stale_row", 0, (19, 18), 19, False),
+            ("repo_path_with_space", 0, 19, 19, True)):
         d = tempfile.mkdtemp(dir=scratch)
-        repo = os.path.join(d, "r")
+        repo = os.path.join(d, "repo with space" if label == "repo_path_with_space" else "r")
         os.makedirs(repo)
         os.makedirs(os.path.join(repo, "tools"))
         os.makedirs(os.path.join(repo, ".ufo/waves/round-80"))
         if sweep == "0s":
             body = ("import sys\nprint('CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 "
                     "stale=1')\nsys.exit(0)\n")
+        elif sweep in ("double", "line"):
+            body = "print('CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0')\n"
+            if sweep == "double":
+                body += "print('CLAIM_SWEEP mismatches=1 unresolved=0 tallies=0 stale=0')\n"
+            else:
+                body = "print('CLAIM_SWEEP_MISMATCH tally SCORECARD.md:1 stale')\n" + body
         else:
             body = ("import sys\n"
                     f"print('CLAIM_SWEEP mismatches={0 if sweep == 0 else 1} "
@@ -123,11 +151,15 @@ def selfcheck(scratch):
         open(os.path.join(repo, CAPTOOL), "w").write(
             "print('CONTROL_RECEIPT_SELFTEST pass=%d fail=0')\n" % live)
         open(os.path.join(repo, ".ufo/waves/round-80/claim-pins.json"), "w").write("{}")
+        rows = stated if isinstance(stated, tuple) else (stated,)
         open(os.path.join(repo, "SCORECARD.md"), "w").write(
             "# t\n\n| Capability | What | Evidence | First |\n|---|---|---|---|\n"
-            f"| guard (`{CAPTOOL}`) | x | selftest {stated} in-memory cases | 79 |\n")
+            + "".join(f"| guard (`{CAPTOOL}`) | x | selftest {value} in-memory cases | 79 |\n"
+                      for value in rows))
         env = ["-c", "user.name=t", "-c", "user.email=t@t"]
         run(["git"] + env + ["-C", repo, "init", "-q"])
+        top = run(["git", "-C", repo, "rev-parse", "--show-toplevel"])
+        assert top.returncode == 0 and top.stdout.strip() == repo, top.stdout
         run(["git"] + env + ["-C", repo, "add", "-A"])
         run(["git"] + env + ["-C", repo, "commit", "-qm", "f"])
         rev = run(["git", "-C", repo, "rev-parse", "HEAD"]).stdout.strip()
diff --git c/.ufo/waves/round-80/count-c3.py w/.ufo/waves/round-80/count-c3.py
index 5e598171..2178e30c 100755
--- c/.ufo/waves/round-80/count-c3.py
+++ w/.ufo/waves/round-80/count-c3.py
@@ -28,7 +28,9 @@ import subprocess
 import sys
 import tempfile
 
-TOKEN = re.compile(r"tools/([A-Za-z0-9_.-]+\.(?:py|sh))(?![\w.-])")
+TOKEN = re.compile(
+    r"(?<![\w./-])(?:([A-Za-z0-9_.-]+)/)?tools/"
+    r"([A-Za-z0-9_.-]+\.(?:py|sh))(?![\w.-])")
 TREE = re.compile(r"^tools/([A-Za-z0-9_.-]+\.(?:py|sh))$")
 
 
@@ -36,23 +38,27 @@ def run(cmd, cwd=None):
     return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
 
 
-def present_set(repo, rev):
-    p = run(["git", "-C", repo, "ls-tree", "-r", "--name-only", rev, "--", "tools/"])
+def tree_sets(repo, rev):
+    p = run(["git", "-C", repo, "ls-tree", "-r", "-t", rev, "--", "tools/"])
     if p.returncode != 0:
         return None
-    return {m.group(1) for line in p.stdout.splitlines() if (m := TREE.match(line.strip()))}
+    present, directories = set(), set()
+    for line in p.stdout.splitlines():
+        metadata, path = line.split("\t", 1)
+        m = TREE.match(path)
+        if m:
+            target = directories if metadata.split()[1] == "tree" else present
+            target.add(m.group(1))
+    return present, directories
 
 
-SIBLING = re.compile(r"[A-Za-z0-9_-]+-shokunin/$")
-
-
-def grade(text, present):
+def grade(text, present, directories, own):
     named = set()
     for m in TOKEN.finditer(text):
-        before = text[max(0, m.start() - 40):m.start()]
-        if SIBLING.search(before):
-            continue          # a sibling lane's tool named by path, not a lane instrument
-        named.add(m.group(1))
+        if m.group(1) is not None and m.group(1) != own:
+            continue          # only the lane's own prefix may qualify tools/
+        if m.group(2) not in directories:
+            named.add(m.group(2))
     missing = sorted(present - named)
     extra = sorted(named - present)
     met = not missing and not extra
@@ -77,31 +83,57 @@ def selfcheck(scratch):
         open(os.path.join(d, "PROVINCE.md"), "w").write("# p\n\n" + body)
         env = ["-c", "user.name=t", "-c", "user.email=t@t"]
         run(["git"] + env + ["-C", d, "init", "-q"])
+        assert run(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip() == d
         run(["git"] + env + ["-C", d, "add", "-A"])
         run(["git"] + env + ["-C", d, "commit", "-qm", "f"])
         rev = run(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()
-        pres = present_set(d, rev)
+        pres, directories = tree_sets(d, rev)
         text = run(["git", "-C", d, "show", f"{rev}:PROVINCE.md"]).stdout
-        r = grade(text, pres)
+        r = grade(text, pres, directories, os.path.basename(d))
         cases.append((label, r["met"] == expects[label],
                       f"named={r['named']} present={r['present']} "
                       f"missing={len(r['missing'])} extra={len(r['extra'])}"))
     # mutation-seat survivors (r80 M01): a sibling-lane path and a directory must not count
     d = tempfile.mkdtemp(dir=scratch)
     os.makedirs(os.path.join(d, "tools", "fake-dir.py"))
+    open(os.path.join(d, "tools", "fake-dir.py", "child"), "w").write("# x\n")
     for tname in tools:
         open(os.path.join(d, "tools", tname), "w").write("# x\n")
     open(os.path.join(d, "PROVINCE.md"), "w").write(
         "# p\n\n" + "".join(f"- `tools/{t}` probe\n" for t in tools)
+        + "- `tools/fake-dir.py` is a directory, not an instrument\n"
         + "- `../tsukuroi-shokunin/tools/tsukuroi-census.sh` reads the same file\n")
     env = ["-c", "user.name=t", "-c", "user.email=t@t"]
     run(["git"] + env + ["-C", d, "init", "-q"])
+    assert run(["git", "-C", d, "rev-parse", "--show-toplevel"]).stdout.strip() == d
     run(["git"] + env + ["-C", d, "add", "-A"])
     run(["git"] + env + ["-C", d, "commit", "-qm", "f"])
     rev = run(["git", "-C", d, "rev-parse", "HEAD"]).stdout.strip()
-    r = grade(run(["git", "-C", d, "show", f"{rev}:PROVINCE.md"]).stdout, present_set(d, rev))
+    pres, directories = tree_sets(d, rev)
+    r = grade(run(["git", "-C", d, "show", f"{rev}:PROVINCE.md"]).stdout,
+              pres, directories, os.path.basename(d))
     cases.append(("sibling_and_directory_ignored", r["met"],
                   f"named={r['named']} present={r['present']} extra={r['extra']}"))
+    # r80 reviewer MEDIUM-6, LOW-11 and LOW-12: one arm per routed exposure.
+    own = os.path.basename(os.path.abspath(os.path.join(
+        os.path.dirname(__file__), "..", "..", "..")))
+    r = grade("`corpus/tools/mori-census.sh`", {"mori-census.sh"}, set(), own)
+    cases.append(("subdir_path_not_naming",
+                  not r["met"] and r["named"] == 0
+                  and r["missing"] == ["mori-census.sh"] and not r["extra"],
+                  f"named={r['named']} missing={r['missing']}"))
+    r = grade(f"`{own}/tools/mori-census.sh` "
+              "`kata-shokunin/tools/sibling.py`",
+              {"mori-census.sh"}, set(), own)
+    cases.append(("own_lane_prefix_allowed",
+                  r["met"] and r["named"] == 1 and not r["extra"],
+                  f"named={r['named']} extra={r['extra']}"))
+    r = grade("`tools/mori-census.sh` `tools/pkg.py` `tools/gone.py`",
+              {"mori-census.sh"}, {"pkg.py"}, own)
+    cases.append(("named_directory_ignored",
+                  not r["met"] and r["named"] == 2
+                  and not r["missing"] and r["extra"] == ["gone.py"],
+                  f"named={r['named']} extra={r['extra']}"))
     ok = sum(1 for _, good, _ in cases if good)
     for label, good, line in cases:
         print(f"{'PASS' if good else 'FAIL'} {label} {line}")
@@ -133,15 +165,16 @@ def main(argv):
             print(f"C3_SETUP unresolvable revision {a.rev}", file=sys.stderr)
             return 2
         rev = p.stdout.strip()
-        pres = present_set(repo, rev)
-        if pres is None:
+        tree = tree_sets(repo, rev)
+        if tree is None:
             print("C3_SETUP ls-tree failed", file=sys.stderr)
             return 2
         text = run(["git", "-C", repo, "show", f"{rev}:PROVINCE.md"]).stdout
         if not text:
             print("C3_SETUP PROVINCE.md unreadable at rev", file=sys.stderr)
             return 2
-        r = grade(text, pres)
+        pres, directories = tree
+        r = grade(text, pres, directories, os.path.basename(os.path.realpath(repo)))
         print(f"C3={'met' if r['met'] else 'unmet'} named={r['named']} present={r['present']} "
               f"missing={len(r['missing'])} extra={len(r['extra'])} rev={rev[:12]}")
         if r["missing"]:
rc=0
```

```text
$ python3 -I -c import sys; p='/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c1.py'; s=open(p).read(); old='        wrong = sum(1 for _, expected, got, _ in results if expected != got)'; assert s.count(old)==1; s=s.replace(old,'        wrong = 0'); sys.argv=[p,'44bc941a0e3e9676fa33a882b43d6e9793cbf74d','--repo','/home/vgpnk/Projects/shokunin/mori-shokunin','--scratch','/fast/scratch/hyaku/mori-r81/Mo81R01C1Attack']; exec(compile(s,p,'exec'),{'__name__':'__main__','__file__':p})
A2_summary_contradicts_mismatch_line expected=unmet got=met rc=0
A3_two_contradicting_summaries expected=unmet got=met rc=0
A4_second_carrier_row_stale expected=unmet got=met rc=0
A5_repo_path_with_space expected=met got=setup rc=2
B1_subdir_path_counts_as_naming expected=unmet got=met rc=0
B2_own_lane_prefix_excluded expected=met got=unmet rc=1
B6_directory_named_as_tool expected=met got=unmet rc=1
C1=met wrong=0 fixtures=7 real_c1=met real_c3=met rev=44bc941a0e3e
rc=0
```

```text
$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c1.py HEAD --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack --counters /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80
A2_summary_contradicts_mismatch_line expected=unmet got=unmet rc=1
A3_two_contradicting_summaries expected=unmet got=unmet rc=1
A4_second_carrier_row_stale expected=unmet got=unmet rc=1
A5_repo_path_with_space expected=met got=met rc=0
B1_subdir_path_counts_as_naming expected=unmet got=unmet rc=1
B2_own_lane_prefix_excluded expected=met got=met rc=0
B6_directory_named_as_tool expected=met got=met rc=0
C1=met wrong=0 fixtures=7 real_c1=met real_c3=met rev=197655534b4a
rc=0
```

```text
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 44bc941a -- .ufo/waves/round-80/contract.md
rc=0
```

```text
$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/count-c3.py HEAD --repo /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack/B2_valid/mori-shokunin --scratch /fast/scratch/hyaku/mori-r81/Mo81R01C1Attack
C3=met named=1 present=1 missing=0 extra=0 rev=18824d7eef14
rc=0
```

```text
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 44bc941a -- .ufo/waves/round-81/count-c1.py
diff --git c/.ufo/waves/round-81/count-c1.py w/.ufo/waves/round-81/count-c1.py
new file mode 100755
index 00000000..bfd84259
--- /dev/null
+++ w/.ufo/waves/round-81/count-c1.py
@@ -0,0 +1,281 @@
+#!/usr/bin/env python3
+"""mori round-81 C1 counter (operability): are the r80 counters' routed exposures closed?
+
+Frozen predicate P-C1 (contract `.ufo/waves/round-81/contract.md`, this counter and the
+receipt label are the same sentence):
+
+  At revision R, `.ufo/waves/round-80/count-c1.py` and `count-c3.py` at R grade the seven
+  frozen defeated fixtures below to their expected verdicts (wrong=0), and both still grade
+  the real lane bytes `C1=met` / `C3=met`; the counter prints
+  `C1=met wrong=0 fixtures=7 real_c1=met real_c3=met` and exits 0. At the entering revision
+  `44bc941a` the same command prints `C1=unmet wrong>=6` rc 1.
+
+Fixtures (the r80 wave's own defeated shapes, Mo80R01Counter MEDIUM-6/7/8, LOW-10/11/12):
+  A2 summary_contradicts_mismatch_line  expect unmet
+  A3 two_contradicting_summaries        expect unmet
+  A4 second_carrier_row_stale           expect unmet
+  A5 repo_path_with_space               expect met
+  B1 subdir_path_counts_as_naming       expect unmet
+  B2 own_lane_prefix_excluded           expect met
+  B6 directory_named_as_tool            expect met
+
+`setup` (rc 2) never satisfies a `met` expectation. `--counters DIR` substitutes the graded
+counter scripts (the harness's own discrimination selftest uses always-met / always-unmet
+stubs); the default exports them from R.
+
+Usage: count-c1.py <rev> [--repo DIR] [--scratch DIR] [--counters DIR] | --selftest
+Output: `C1=met|unmet wrong=N fixtures=7 real_c1=met|unmet real_c3=met|unmet rev=<sha12>`
+Exit 0 met, 1 unmet, 2 setup. Read-only: `git archive`/`git show` into --scratch; every
+fixture repo is created under --scratch and removed on exit.
+"""
+import argparse
+import os
+import re
+import shutil
+import subprocess
+import sys
+import tempfile
+
+C1 = ".ufo/waves/round-80/count-c1.py"
+C3 = ".ufo/waves/round-80/count-c3.py"
+CAPTOOL = "tools/mori-control-receipt.py"
+SWEEP = "tools/mori-claim-sweep.py"
+
+ZERO_SUMMARY = "CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=1 pointers=0"
+ONE_SUMMARY = "CLAIM_SWEEP mismatches=1 unresolved=0 tallies=1 stale=0 carriers=1 pointers=0"
+MISMATCH_LINE = "CLAIM_SWEEP_MISMATCH tally .ufo/waves/round-80/claim-pins.json:1 tools/x.py pinned=19 live=20"
+
+
+def run(cmd, cwd=None):
+    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
+
+
+def verdict(text, word):
+    """Read `C1=met|unmet` / `C3=met|unmet`, falling back to a setup verdict."""
+    match = re.search(r"\b%s=(met|unmet)\b" % word, text)
+    if match:
+        return match.group(1)
+    return "setup" if "SETUP" in text or not text.strip() else "unknown"
+
+
+def make_repo(base, files):
+    os.makedirs(base, exist_ok=True)
+    for name, body in files.items():
+        path = os.path.join(base, name)
+        os.makedirs(os.path.dirname(path), exist_ok=True)
+        open(path, "w", encoding="utf-8").write(body)
+    env = ["-c", "user.name=t", "-c", "user.email=t@t"]
+    run(["git"] + env + ["-C", base, "init", "-q"])
+    run(["git"] + env + ["-C", base, "add", "-A"])
+    run(["git"] + env + ["-C", base, "commit", "-qm", "fixture"])
+    return run(["git", "-C", base, "rev-parse", "HEAD"]).stdout.strip()
+
+
+def fake_sweep(body):
+    return "import sys\n" + body + "\n"
+
+
+def card(rows):
+    return ("# card\n\n### Capabilities (round 80)\n\n"
+            "| Capability | What it can now do | Evidence pointer | First-working round |\n"
+            "|---|---|---|---|\n" + rows)
+
+
+def fixture_a2(root):
+    files = {SWEEP: fake_sweep("print(%r)\nprint(%r)\nsys.exit(0)"
+                               % (MISMATCH_LINE, ZERO_SUMMARY)),
+             CAPTOOL: "print('CONTROL_RECEIPT_SELFTEST pass=19 fail=0')\n",
+             ".ufo/waves/round-80/claim-pins.json": "{}",
+             "SCORECARD.md": card("| guard (`%s`) | x | selftest 19 in-memory cases | 79 |\n"
+                                  % CAPTOOL)}
+    return make_repo(root, files)
+
+
+def fixture_a3(root):
+    files = {SWEEP: fake_sweep("print(%r)\nprint(%r)\nsys.exit(0)"
+                               % (ZERO_SUMMARY, ONE_SUMMARY)),
+             CAPTOOL: "print('CONTROL_RECEIPT_SELFTEST pass=19 fail=0')\n",
+             ".ufo/waves/round-80/claim-pins.json": "{}",
+             "SCORECARD.md": card("| guard (`%s`) | x | selftest 19 in-memory cases | 79 |\n"
+                                  % CAPTOOL)}
+    return make_repo(root, files)
+
+
+def fixture_a4(root):
+    files = {SWEEP: fake_sweep("print(%r)\nsys.exit(0)" % ZERO_SUMMARY),
+             CAPTOOL: "print('CONTROL_RECEIPT_SELFTEST pass=19 fail=0')\n",
+             ".ufo/waves/round-80/claim-pins.json": "{}",
+             "SCORECARD.md": card(
+                 "| guard (`%s`) | x | selftest 19 in-memory cases | 79 |\n"
+                 "| guard again (`%s`) | y | selftest 18 in-memory cases | 79 |\n"
+                 % (CAPTOOL, CAPTOOL))}
+    return make_repo(root, files)
+
+
+def fixture_a5(root):
+    files = {SWEEP: fake_sweep("print(%r)\nsys.exit(0)" % ZERO_SUMMARY),
+             CAPTOOL: "print('CONTROL_RECEIPT_SELFTEST pass=19 fail=0')\n",
+             ".ufo/waves/round-80/claim-pins.json": "{}",
+             "SCORECARD.md": card("| guard (`%s`) | x | selftest 19 in-memory cases | 79 |\n"
+                                  % CAPTOOL)}
+    spaced = os.path.join(root, "dir with space", "lane")
+    os.makedirs(spaced, exist_ok=True)
+    head = make_repo(spaced, files)
+    return head, spaced
+
+
+def province_repo(root, names, tool_files):
+    files = {name: "# tool\n" for name in tool_files}
+    files["PROVINCE.md"] = "# province\n\n" + "".join("- `%s` probe\n" % name for name in names)
+    return make_repo(root, files)
+
+
+def build_fixtures(scratch):
+    """Return [(label, counter, expected, repo_dir, head)]."""
+    out = []
+    for label, builder, counter, expected in (
+            ("A2", fixture_a2, "count-c1", "unmet"),
+            ("A3", fixture_a3, "count-c1", "unmet"),
+            ("A4", fixture_a4, "count-c1", "unmet")):
+        repo = os.path.join(scratch, label.lower())
+        out.append((label + "_" + {"A2": "summary_contradicts_mismatch_line",
+                                   "A3": "two_contradicting_summaries",
+                                   "A4": "second_carrier_row_stale"}[label],
+                    counter, expected, repo, builder(repo)))
+    head, repo = fixture_a5(os.path.join(scratch, "a5"))
+    out.append(("A5_repo_path_with_space", "count-c1", "met", repo, head))
+    repo = os.path.join(scratch, "b1")
+    out.append(("B1_subdir_path_counts_as_naming", "count-c3", "unmet", repo,
+                province_repo(repo, ["corpus/tools/mori-census.sh"], ["tools/mori-census.sh"])))
+    repo = os.path.join(scratch, "b2", "mori-shokunin")
+    out.append(("B2_own_lane_prefix_excluded", "count-c3", "met", repo,
+                province_repo(repo, ["mori-shokunin/tools/mori-census.sh"],
+                              ["tools/mori-census.sh"])))
+    repo = os.path.join(scratch, "b6")
+    out.append(("B6_directory_named_as_tool", "count-c3", "met", repo,
+                province_repo(repo, ["tools/mori-census.sh", "tools/mori-pressure.py",
+                                     "tools/mori-runway-win.py", "tools/pkg.py"],
+                              ["tools/mori-census.sh", "tools/mori-pressure.py",
+                               "tools/mori-runway-win.py", "tools/pkg.py/inner.py"])))
+    return out
+
+
+def grade_fixtures(counters, fixtures, scratch):
+    results = []
+    for label, counter, expected, repo, head in fixtures:
+        script = os.path.join(counters, counter + ".py")
+        work = tempfile.mkdtemp(dir=scratch)
+        result = run(["python3", "-I", script, head, "--repo", repo, "--scratch", work])
+        got = verdict(result.stdout + result.stderr, "C1" if counter == "count-c1" else "C3")
+        results.append((label, expected, got, result.returncode))
+    return results
+
+
+def grade_real(counters, repo, rev, scratch):
+    out = {}
+    for counter, word in (("count-c1", "C1"), ("count-c3", "C3")):
+        work = tempfile.mkdtemp(dir=scratch)
+        result = run(["python3", "-I", os.path.join(counters, counter + ".py"),
+                      rev, "--repo", repo, "--scratch", work])
+        out[word] = verdict(result.stdout + result.stderr, word)
+    return out
+
+
+def export_counters(repo, rev, dest):
+    os.makedirs(dest, exist_ok=True)
+    ok = True
+    for counter in (C1, C3):
+        result = run(["git", "-C", repo, "show", "%s:%s" % (rev, counter)])
+        if result.returncode != 0:
+            ok = False
+            continue
+        path = os.path.join(dest, os.path.basename(counter))
+        open(path, "w", encoding="utf-8").write(result.stdout)
+    return ok
+
+
+def selftest(scratch):
+    passed = failed = 0
+
+    def check(label, ok, detail=""):
+        nonlocal passed, failed
+        passed += int(bool(ok))
+        failed += int(not ok)
+        print("case %s %s %s" % (label, "pass" if ok else "FAIL", detail))
+
+    check("verdict met", verdict("C1=met wrong=0", "C1") == "met")
+    check("verdict unmet", verdict("C3=unmet named=0", "C3") == "unmet")
+    check("verdict setup", verdict("C1_SETUP archive failed", "C1") == "setup")
+
+    fixtures = build_fixtures(scratch)
+    check("seven fixtures", len(fixtures) == 7, str(len(fixtures)))
+    check("expectation mix", sum(1 for row in fixtures if row[2] == "met") == 3)
+
+    always_met = tempfile.mkdtemp(dir=scratch)
+    for counter, word in (("count-c1", "C1"), ("count-c3", "C3")):
+        open(os.path.join(always_met, counter + ".py"), "w", encoding="utf-8").write(
+            "import sys\nprint('%s=met stub')\nsys.exit(0)\n" % word)
+    results = grade_fixtures(always_met, fixtures, scratch)
+    wrong = sum(1 for _, expected, got, _ in results if expected != got)
+    check("always-met stub is wrong", wrong == 4, "wrong=%d" % wrong)
+
+    always_unmet = tempfile.mkdtemp(dir=scratch)
+    for counter, word in (("count-c1", "C1"), ("count-c3", "C3")):
+        open(os.path.join(always_unmet, counter + ".py"), "w", encoding="utf-8").write(
+            "import sys\nprint('%s=unmet stub')\nsys.exit(1)\n" % word)
+    results = grade_fixtures(always_unmet, fixtures, scratch)
+    wrong = sum(1 for _, expected, got, _ in results if expected != got)
+    check("always-unmet stub is wrong", wrong == 3, "wrong=%d" % wrong)
+
+    print("C1_COUNTER_SELFTEST pass=%d fail=%d" % (passed, failed))
+    return 0 if not failed else 1
+
+
+def main(argv):
+    ap = argparse.ArgumentParser()
+    ap.add_argument("rev", nargs="?")
+    ap.add_argument("--repo", default=os.path.abspath(
+        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
+    ap.add_argument("--scratch")
+    ap.add_argument("--counters")
+    ap.add_argument("--selftest", action="store_true")
+    a = ap.parse_args(argv)
+    base = a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()
+    os.makedirs(base, exist_ok=True)
+    scratch = tempfile.mkdtemp(prefix="count-c1-r81-", dir=base)
+    try:
+        if a.selftest:
+            return selftest(scratch)
+        if not a.rev:
+            print("C1_SETUP usage: count-c1.py <rev> | --selftest", file=sys.stderr)
+            return 2
+        top = run(["git", "-C", a.repo, "rev-parse", "--show-toplevel"])
+        repo = top.stdout.strip() if top.returncode == 0 else a.repo
+        p = run(["git", "-C", repo, "rev-parse", "--verify", a.rev + "^{commit}"])
+        if p.returncode != 0:
+            print("C1_SETUP unresolvable revision " + a.rev, file=sys.stderr)
+            return 2
+        rev = p.stdout.strip()
+        if a.counters:
+            counters = a.counters
+        else:
+            counters = os.path.join(scratch, "counters")
+            if not export_counters(repo, rev, counters):
+                print("C1_SETUP counters absent at rev=" + rev[:12], file=sys.stderr)
+                return 2
+        fixtures = build_fixtures(scratch)
+        results = grade_fixtures(counters, fixtures, scratch)
+        for label, expected, got, rc in results:
+            print("%s expected=%s got=%s rc=%d" % (label, expected, got, rc))
+        wrong = sum(1 for _, expected, got, _ in results if expected != got)
+        real = grade_real(counters, repo, rev, scratch)
+        print("C1=%s wrong=%d fixtures=%d real_c1=%s real_c3=%s rev=%s"
+              % ("met" if wrong == 0 and real["C1"] == "met" and real["C3"] == "met"
+                 else "unmet", wrong, len(results), real["C1"], real["C3"], rev[:12]))
+        return 0 if wrong == 0 and real["C1"] == "met" and real["C3"] == "met" else 1
+    finally:
+        shutil.rmtree(scratch, ignore_errors=True)
+
+
+if __name__ == "__main__":
+    sys.exit(main(sys.argv[1:]))
rc=0
```

```text
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 44bc941a -- .ufo/waves/round-80/contract.md
rc=0
```

```text
$ python3 -I -c import sys; p='/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c1.py'; s=open(p).read(); old='    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)'; assert s.count(old)==1; s=s.replace(old,'    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)\n    if cmd[0] == "python3": p.returncode = 2\n    return p'.replace('\n','
')); sys.argv=[p,'HEAD','--repo','/home/vgpnk/Projects/shokunin/mori-shokunin','--scratch','/fast/scratch/hyaku/mori-r81/Mo81R01C1Attack','--counters','/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80']; exec(compile(s,p,'exec'),{'__name__':'__main__','__file__':p})
  File "<string>", line 1
    import sys; p='/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c1.py'; s=open(p).read(); old='    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)'; assert s.count(old)==1; s=s.replace(old,'    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)\n    if cmd[0] == "python3": p.returncode = 2\n    return p'.replace('\n','
                                                                                                                                                                                                                                                                                                                                                                                          ^
SyntaxError: unterminated string literal (detected at line 1)
rc=1
```

```text
$ python3 -I -c import sys; p='/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-81/count-c1.py'; s=open(p).read(); old='    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)'; assert s.count(old)==1; s=s.replace(old,'    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)\n    if cmd[0] == "python3": p.returncode = 2\n    return p'); sys.argv=[p,'HEAD','--repo','/home/vgpnk/Projects/shokunin/mori-shokunin','--scratch','/fast/scratch/hyaku/mori-r81/Mo81R01C1Attack','--counters','/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80']; exec(compile(s,p,'exec'),{'__name__':'__main__','__file__':p})
A2_summary_contradicts_mismatch_line expected=unmet got=unmet rc=2
A3_two_contradicting_summaries expected=unmet got=unmet rc=2
A4_second_carrier_row_stale expected=unmet got=unmet rc=2
A5_repo_path_with_space expected=met got=met rc=2
B1_subdir_path_counts_as_naming expected=unmet got=unmet rc=2
B2_own_lane_prefix_excluded expected=met got=met rc=2
B6_directory_named_as_tool expected=met got=met rc=2
C1=met wrong=0 fixtures=7 real_c1=met real_c3=met rev=197655534b4a
rc=0
```


## Self-review

Accuracy 4/5: identity mis-expectation is disclosed and corrected by an actual same-commit run. Completeness 4/5: final landed SHA unavailable; worktree and entering evidence are distinct. Clarity 4/5: complete required transcripts are long. Actionability 4/5: precise rc-consistency sites and reproducible fault supplied. Conciseness 4/5: source retained to make deleted scratch reproducible. Overall 4.0/5. Highest-impact improvement: bind rc to verdict and perform the landed-revision keeper. Would the user agree? The material gaps are explicit rather than called passing.

## Closure addendum — counter-side HIGH CLOSED

The HIGH finding was fixed by L1 during review. L1 reports the added selftest arm `met-with-rc2 stub is wrong everywhere`, `C1_COUNTER_SELFTEST pass=8 fail=0`, and re-measured entering `C1=unmet wrong=7 fixtures=7`; these selftest/control statements are attributed, not independently rerun here.

I inspected the new rc2-to-setup mapping at r81 count-c1.py:170-171 and its grade_real counterpart, then reran the identical `python3 -I -c` exit-injection command printed above. Full new output:

```text
A2_summary_contradicts_mismatch_line expected=unmet got=setup rc=2
A3_two_contradicting_summaries expected=unmet got=setup rc=2
A4_second_carrier_row_stale expected=unmet got=setup rc=2
A5_repo_path_with_space expected=met got=setup rc=2
B1_subdir_path_counts_as_naming expected=unmet got=setup rc=2
B2_own_lane_prefix_excluded expected=met got=setup rc=2
B6_directory_named_as_tool expected=met got=setup rc=2
C1=unmet wrong=7 fixtures=7 real_c1=setup real_c3=setup rev=197655534b4a
rc=1
```

Status: HIGH counter-side CLOSED at the observed worktree gate, independently reproduced. This was the round gate's defect, not E02's implementation defect. Earlier verdicts and output remain chronological evidence. Arbitrary `wrong=0` source corruption remains only a LOW mutation-resistance observation, not an assertion of a pristine production bug. Final landed-revision keeper remains L1-owned.
