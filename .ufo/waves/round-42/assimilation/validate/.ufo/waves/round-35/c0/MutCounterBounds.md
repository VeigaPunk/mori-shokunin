# C0 MutCounterBounds — twelve single-bound counter mutants
**Result: 10 killed; m1 and m12 survived. The claim that every check is independently load-bearing is unmet.** All twelve malformed registers scored `C1=unmet`, exit 1, under the actual frozen counter. No frozen skip-the-work control passed in this probe.
## Scope and expected detector
- Seat: `MoriR35.MutCounterBounds`; axes: isolated predicate discrimination, bounded observed outcomes, exact restoration.
- Frozen lane revision: `f2d28711ee723c969b6c2008d32df498192f9e7b`; frozen fleet MANIFEST: `37b51a243302e8009c7067431e8a47f9a722fd14`.
- Sandbox: `/fast/scratch/hyaku/mori-r35/MutCounterBounds/clone`; all Git writes occurred there with `GIT_DIR`, `GIT_WORK_TREE`, and `GIT_INDEX_FILE` removed from the environment.
- Frozen counter SHA-256, observed with `timeout 10 sha256sum`: `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167`. Its bytes were never edited.
- Expected distinguishing detector: positive sanity control exits 0; malformed register exits 1 on pristine bytes and frozen path, 0 with its one-check mutant, then 1 on byte-restored bytes. A rejection exit 1 is the expected baseline success here, not a failed detector. No timeout, error exit 2, or nonempty stderr occurred in the 49 counter invocations.
- Each mutant removes exactly one specified behavior point. m3 removes only `extra.append(key)` from the duplicate branch, retaining its diagnostic and `continue`; m7 removes only the range comparison/rejection block, retaining range parsing. Exact patches are below.
- Representative saved register: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/c0/MutCounterBounds-register.md`, exactly the last section extracted from committed m5 SCORECARD bytes; 22 lines, SHA-256 `e672be34b8ef7ac4b471041c75ccb9d78a7aeddafdec2e9c80cef13971fb17f3`. It skips the evidence lookup for one capability; all other rows are unchanged from the positive control.
- Tools installed or updated: none. No subagents, background jobs, models, or other runtime were invoked.
## Mutant discrimination table
The frozen and mutant columns contain the exact final stdout lines. The four exit codes are pristine-copy / frozen-path / mutant / restored-copy.
| Mutant (removed check) | Killing register or surviving probe (one line) | Frozen summary | Mutant summary | Exits | Verdict |
| --- | --- | --- | --- | --- | --- |
| m1 — missing == 0 term | No killing register: omit rounds[313].capabilities_added[0]; matched=17 still prevents met. | `label=P-C1 rev=ca205042a68fb7c25e0dc016acc4190b87d51792 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=17 matched=17 missing=1 bad=0 extra=0 mismatches=1 C1=unmet` | `label=P-C1 rev=ca205042a68fb7c25e0dc016acc4190b87d51792 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=17 matched=17 missing=1 bad=0 extra=0 mismatches=1 C1=unmet` | 1/1/1/1 | **survived** |
| m2 — extra == 0 term | Positive register plus one rounds[999999].capabilities_added[0] row (19 rows). | `label=P-C1 rev=0e3abbdc26a9c2a3cc31336f11880e82402af16f manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=19 matched=18 missing=0 bad=0 extra=1 mismatches=1 C1=unmet` | `label=P-C1 rev=0e3abbdc26a9c2a3cc31336f11880e82402af16f manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=19 matched=18 missing=0 bad=0 extra=1 mismatches=1 C1=met` | 1/1/0/1 | **killed** |
| m3 — duplicate-key extra increment | Positive register plus an exact duplicate of rounds[313].capabilities_added[0] (19 rows). | `label=P-C1 rev=a762b10f9829af260caa7f27a6b2d4a3e580b54c manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=19 matched=18 missing=0 bad=0 extra=1 mismatches=1 C1=unmet` | `label=P-C1 rev=a762b10f9829af260caa7f27a6b2d4a3e580b54c manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=19 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met` | 1/1/0/1 | **killed** |
| m4 — round equality | Change rounds[313].capabilities_added[0] round cell from 12 to 13. | `label=P-C1 rev=cf1bbd50e78cfe1d883504fbb4234ef8e1ef2017 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet` | `label=P-C1 rev=cf1bbd50e78cfe1d883504fbb4234ef8e1ef2017 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met` | 1/1/0/1 | **killed** |
| m5 — 1..2 evidence-count bound | Empty the evidence cell of rounds[313].capabilities_added[0]; saved representative register. | `label=P-C1 rev=ecce9f0d53dae0a92830477da27352dc333fb0a0 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet` | `label=P-C1 rev=ecce9f0d53dae0a92830477da27352dc333fb0a0 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met` | 1/1/0/1 | **killed** |
| m6 — absent-at-rev check | Positive register; omit its cited r12 classification artifact from the measured git tree only. | `label=P-C1 rev=a0e64dd81c63bef3d143b15d9dcf12663be5622a manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet` | `label=P-C1 rev=a0e64dd81c63bef3d143b15d9dcf12663be5622a manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met` | 1/1/0/1 | **killed** |
| m7 — line-range check | Cite r12 classification artifact with :0 on rounds[313].capabilities_added[0]. | `label=P-C1 rev=d73e32d7f2ad91b07f6664da1c2d581c0e385bf8 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet` | `label=P-C1 rev=d73e32d7f2ad91b07f6664da1c2d581c0e385bf8 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met` | 1/1/0/1 | **killed** |
| m8 — changed-in-round check | Cite tools/mori-silence-cases.sh for rounds[313].capabilities_added[0] (not changed in r12). | `label=P-C1 rev=3cde9343a1563503b1bd49dd9fb12aa9690886e2 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet` | `label=P-C1 rev=3cde9343a1563503b1bd49dd9fb12aa9690886e2 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met` | 1/1/0/1 | **killed** |
| m9 — artifact-prefix rule | Cite LOG.md for rounds[313].capabilities_added[0] (non-artifact). | `label=P-C1 rev=1abed06626a9a6c831dbb387fce15c30982149f3 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet` | `label=P-C1 rev=1abed06626a9a6c831dbb387fce15c30982149f3 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met` | 1/1/0/1 | **killed** |
| m10 — named-path rule | Cite corpus/evidence/freeze-register.json for rounds[386].capabilities_added[0] (wrong named path). | `label=P-C1 rev=449a58949eba34017929f8530d84c93fc9d1c0f9 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet` | `label=P-C1 rev=449a58949eba34017929f8530d84c93fc9d1c0f9 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met` | 1/1/0/1 | **killed** |
| m11 — whole-path-in-closure-text rule | Cite corpus/evidence/README.md for rounds[313].capabilities_added[0] (absent from closure text). | `label=P-C1 rev=a2ba0ba4dbdae3f84ddc0c6d591b793cb580db74 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet` | `label=P-C1 rev=a2ba0ba4dbdae3f84ddc0c6d591b793cb580db74 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met` | 1/1/0/1 | **killed** |
| m12 — exists-at-closure-commit check | No killing register: r12 row cites later tools/mori-blind-check.sh; unchanged-in-round still rejects. | `label=P-C1 rev=56fee54c0956f79ce9e0249d1dd52d414bac7fd7 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet` | `label=P-C1 rev=56fee54c0956f79ce9e0249d1dd52d414bac7fd7 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet` | 1/1/1/1 | **survived** |

## Surviving mutants — no independent distinguishing register
**m1 survived (structurally redundant).** The unchanged duplicate-key guard permits at most one `matched` detail per oracle key, and non-oracle keys never become matched. Therefore `matched == len(oracle)` already implies that every oracle key was seen and `missing == 0`. Removing only `and not missing` cannot change any C1 result. The one-missing-row probe observed `matched=17 missing=1 C1=unmet` on pristine, frozen, mutant, and restored bytes. This is a genuine survivor, not a kill.
**m12 survived (redundant for this frozen oracle/history).** An exhaustive set difference for every capability-bearing admitted closure found `changed - at_commit == empty`. There are no deleted paths in these twelve frozen round diffs. Thus the remaining `p in changed` already implies `p in at_commit`; no register at any measured tip can distinguish the sole removal while these oracle commits stay fixed. The later-tool probe is rejected by both counters. This does not prove the existence check redundant for a different MANIFEST/history containing deletions. It does prove that this fixed task cannot demonstrate its independent load-bearing behavior with register edits alone.
Neither survivor changes the contract. The bounds remain frozen; the finding is the lack of independent discrimination, not permission to remove them.
| Round | Closure commit | Changed paths | Changed paths absent at closure |
| --- | --- | --- | --- |
| 12 | `bf7cdc4783d0748d525fbfe3ba8fb3d285eb929a` | 27 | `[]` |
| 14 | `0fa5e0de194bcc270a927a166664113e6821442b` | 398 | `[]` |
| 15 | `b83edc6ee3db6822382ab673d7e6e984e420f22f` | 1417 | `[]` |
| 16 | `24526ea9617cd020fee16c28fe4d4a2789dc28cb` | 579 | `[]` |
| 18 | `3786f3f1bde2fbcc5ce617e35e8c9becdbf9d9e8` | 208 | `[]` |
| 19 | `2061780117e6ca637725004897bd288d3ba7e988` | 148 | `[]` |
| 22 | `1bfe708a170c877db3319060d0ab38771efe03ac` | 379 | `[]` |
| 24 | `4f05dd5a32055e85a9297eb8fc8dfec7dfc4625e` | 108 | `[]` |
| 25 | `829d8c9072d5907b9050d06c16cc34b0bb73d0f8` | 116 | `[]` |
| 26 | `ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` | 111 | `[]` |
| 28 | `1fc6bb0eaab40d9ea4fe996b64d140282b76337d` | 112 | `[]` |
| 31 | `52435f2f425c2b4a5e7ba63d7abc1292b8736367` | 113 | `[]` |

## Sandbox build and clone commits
The positive register used the actual oracle capability strings, matching keys and rounds, and one strong path per row. Its r12 path is `corpus/evidence/drift-r12-20261019T2204Z-classification.md`. All other witnesses are the one-line deltas in the table, independent of each other. m6 additionally stages only that r12 path out of its measured commit with `git update-index --force-remove`; the worktree file is never removed and is staged back in the next commit.
Initial executed setup command (exit 0):

```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE /bin/bash -c 'mkdir -p /fast/scratch/hyaku/mori-r35/MutCounterBounds && git clone -q /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone && git -C /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone checkout -q -b ctl-mutcounterbounds f2d28711ee723c969b6c2008d32df498192f9e7b'
```
All commits used the following exact command shape, wrapped by `timeout 120` and the sanitized environment; `LABEL` is positive, m1 through m12, or restored:

```sh
git -C /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone -c user.name=ctl -c user.email=ctl@local commit -qm ctl-LABEL
```
| Control | Clone commit | Register verdict under frozen counter |
| --- | --- | --- |
| positive | `90a8e8136d317f94cb86976fd7641c66dbc2ecbe` | met (positive sanity) |
| m1 | `ca205042a68fb7c25e0dc016acc4190b87d51792` | unmet |
| m2 | `0e3abbdc26a9c2a3cc31336f11880e82402af16f` | unmet |
| m3 | `a762b10f9829af260caa7f27a6b2d4a3e580b54c` | unmet |
| m4 | `cf1bbd50e78cfe1d883504fbb4234ef8e1ef2017` | unmet |
| m5 | `ecce9f0d53dae0a92830477da27352dc333fb0a0` | unmet |
| m6 | `a0e64dd81c63bef3d143b15d9dcf12663be5622a` | unmet |
| m7 | `d73e32d7f2ad91b07f6664da1c2d581c0e385bf8` | unmet |
| m8 | `3cde9343a1563503b1bd49dd9fb12aa9690886e2` | unmet |
| m9 | `1abed06626a9a6c831dbb387fce15c30982149f3` | unmet |
| m10 | `449a58949eba34017929f8530d84c93fc9d1c0f9` | unmet |
| m11 | `a2ba0ba4dbdae3f84ddc0c6d591b793cb580db74` | unmet |
| m12 | `56fee54c0956f79ce9e0249d1dd52d414bac7fd7` | unmet |

The following 58-line bounded reproduction generator reconstructs all registers and exactly the twelve mutations from the saved representative register. It is provided for reproducibility, not claimed as separately exercised. It expects an unused `/fast/scratch/hyaku/mori-r35/MutCounterBounds-replay/clone`. The observed runs below used the tool-applied edits in the assigned clone, not a second replay. Save the generator outside the lane and invoke it with an outer `timeout 1800 python3 /absolute/path/to/generator.py`.

```python
import os, pathlib, subprocess
L = pathlib.Path('/home/vgpnk/Projects/shokunin/mori-shokunin')
D = pathlib.Path('/fast/scratch/hyaku/mori-r35/MutCounterBounds-replay')
R = D / 'clone'; F = L / '.ufo/waves/round-35/count-c1.py'
E = {k:v for k,v in os.environ.items() if k not in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE')}
def run(*args, check=True):
    p = subprocess.run(['timeout','120',*map(str,args)], env=E, capture_output=True, text=True, timeout=125)
    if check and p.returncode: raise RuntimeError(p.stderr)
    return p
D.mkdir(parents=True, exist_ok=True)
run('git','clone','-q',L,R)
run('git','-C',R,'checkout','-q','-b','ctl-mutcounterbounds','f2d28711ee723c969b6c2008d32df498192f9e7b')
base = run('git','-C',R,'show','HEAD:SCORECARD.md').stdout
src = F.read_text(); artifact = 'corpus/evidence/drift-r12-20261019T2204Z-classification.md'
seed = (L / '.ufo/waves/round-35/c0/MutCounterBounds-register.md').read_text()
seed = seed.replace('|  | 12 |','| `'+artifact+'` | 12 |',1)
changes = {
 1:(194,194,'    met = matched == len(oracle) and not bad and not extra'),
 2:(194,194,'    met = matched == len(oracle) and not missing and not bad'),
 3:(149,149,None), 4:(159,160,None), 5:(179,180,None),
 6:(169,171,None), 7:(175,177,None),
 8:(182,182,'                if not (p in o["at_commit"]'),
 9:(183,183,None), 10:(184,184,None),
 11:(184,185,'                        and (not o["named"] or p in o["named"])):'),
 12:(182,182,'                if not (p in o["changed"]')}
def commit(label):
    run('git','-C',R,'-c','user.name=ctl','-c','user.email=ctl@local','commit','-qm','ctl-'+label)
    return run('git','-C',R,'rev-parse','HEAD').stdout.strip()
def score(counter,rev):
    p=run('python3',counter,rev,'--repo',R,check=False)
    print(p.stdout,end=''); print('exit='+str(p.returncode)); print(p.stderr,end='')
(R/'SCORECARD.md').write_text(base+'\n'+seed)
run('git','-C',R,'add','--','SCORECARD.md'); score(F,commit('positive'))
try:
    for i in range(1,13):
        rows=seed.splitlines(); first=next(j for j,x in enumerate(rows) if x.startswith('| rounds[313]'))
        named=next(j for j,x in enumerate(rows) if x.startswith('| rounds[386].capabilities_added[0]'))
        if i==1: del rows[first]
        if i==2: rows.append('| rounds[999999].capabilities_added[0] | Not an oracle capability | Skips no-extra bound | `'+artifact+'` | 12 |')
        if i==3: rows.append(rows[first])
        if i==4: rows[first]=rows[first].replace('| 12 |','| 13 |')
        if i==5: rows[first]=rows[first].replace('`'+artifact+'`','')
        paths={7:artifact+':0',8:'tools/mori-silence-cases.sh',9:'LOG.md',11:'corpus/evidence/README.md',12:'tools/mori-blind-check.sh'}
        if i in paths: rows[first]=rows[first].replace('`'+artifact+'`','`'+paths[i]+'`')
        if i==10: rows[named]=rows[named].replace('`tools/mori-retention-gate.py`','`corpus/evidence/freeze-register.json`')
        (R/'SCORECARD.md').write_text(base+'\n'+'\n'.join(rows)+'\n')
        run('git','-C',R,'add','--','SCORECARD.md',artifact)
        if i==6: run('git','-C',R,'update-index','--force-remove','--',artifact)
        rev=commit('m'+str(i)); C=D/('count-c1-m'+str(i)+'.py'); C.write_text(src)
        score(C,rev); score(F,rev)
        lines=src.splitlines(True); a,b,text=changes[i]
        lines[a-1:b]=[] if text is None else [text+'\n']
        try: C.write_text(''.join(lines)); score(C,rev)
        finally: C.write_text(src)
        score(C,rev)
finally:
    (R/'SCORECARD.md').write_text(base)
    run('git','-C',R,'add','--','SCORECARD.md',artifact); commit('restored')
```
## Exact counter mutations

### m1

```diff
--- frozen-count-c1.py
+++ count-c1-m1.py
@@ -191,7 +191,7 @@
             details.append({"row": key, "status": "matched"})
     missing = sorted(k for k in oracle if k not in seen)
     matched = sum(1 for d in details if d["status"] == "matched")
-    met = matched == len(oracle) and not missing and not bad and not extra
+    met = matched == len(oracle) and not bad and not extra
     summary = ("label=%s rev=%s manifest_rev=%s register=%r oracle=%d rows=%d matched=%d missing=%d bad=%d "
                "extra=%d mismatches=%d C1=%s") % (
         LABEL, full, MANIFEST_REV[:12], heading, len(oracle), len(rows), matched, len(missing), len(bad),
```

### m2

```diff
--- frozen-count-c1.py
+++ count-c1-m2.py
@@ -191,7 +191,7 @@
             details.append({"row": key, "status": "matched"})
     missing = sorted(k for k in oracle if k not in seen)
     matched = sum(1 for d in details if d["status"] == "matched")
-    met = matched == len(oracle) and not missing and not bad and not extra
+    met = matched == len(oracle) and not missing and not bad
     summary = ("label=%s rev=%s manifest_rev=%s register=%r oracle=%d rows=%d matched=%d missing=%d bad=%d "
                "extra=%d mismatches=%d C1=%s") % (
         LABEL, full, MANIFEST_REV[:12], heading, len(oracle), len(rows), matched, len(missing), len(bad),
```

### m3

```diff
--- frozen-count-c1.py
+++ count-c1-m3.py
@@ -146,7 +146,6 @@
             details.append({"row": cells[0] if cells else "", "status": "extra"})
             continue
         if key in seen:
-            extra.append(key)
             details.append({"row": key, "status": "extra-duplicate"})
             continue
         seen[key] = True
```

### m4

```diff
--- frozen-count-c1.py
+++ count-c1-m4.py
@@ -156,8 +156,6 @@
             why.append("cells=%d" % len(cells))
         else:
             rnd = cells[4].strip("` ")
-            if rnd != str(o["round"]):
-                why.append("round=%s!=%s" % (rnd, o["round"]))
             toks = TICK_RE.findall(cells[3])
             paths = []
             for t in toks:
```

### m5

```diff
--- frozen-count-c1.py
+++ count-c1-m5.py
@@ -176,8 +176,6 @@
                         why.append("line-out-of-range:%s" % t)
                         continue
                 paths.append(p)
-            if not 1 <= len(toks) <= 2:
-                why.append("evidence-paths=%d" % len(toks))
             for p in paths:
                 if not (p in o["at_commit"] and p in o["changed"]
                         and (p.startswith(ARTIFACT_PREFIXES) or p in ARTIFACT_FILES)
```

### m6

```diff
--- frozen-count-c1.py
+++ count-c1-m6.py
@@ -166,9 +166,6 @@
                     why.append("not-a-path:%s" % t)
                     continue
                 p, a, b = pm.group(1), pm.group(2), pm.group(3)
-                if p not in at_rev:
-                    why.append("absent-at-rev:%s" % p)
-                    continue
                 if a:
                     n = len((show(repo, full, p) or "").splitlines())
                     lo, hi = int(a), int(b or a)
```

### m7

```diff
--- frozen-count-c1.py
+++ count-c1-m7.py
@@ -172,9 +172,6 @@
                 if a:
                     n = len((show(repo, full, p) or "").splitlines())
                     lo, hi = int(a), int(b or a)
-                    if not (1 <= lo <= hi <= n):
-                        why.append("line-out-of-range:%s" % t)
-                        continue
                 paths.append(p)
             if not 1 <= len(toks) <= 2:
                 why.append("evidence-paths=%d" % len(toks))
```

### m8

```diff
--- frozen-count-c1.py
+++ count-c1-m8.py
@@ -179,7 +179,7 @@
             if not 1 <= len(toks) <= 2:
                 why.append("evidence-paths=%d" % len(toks))
             for p in paths:
-                if not (p in o["at_commit"] and p in o["changed"]
+                if not (p in o["at_commit"]
                         and (p.startswith(ARTIFACT_PREFIXES) or p in ARTIFACT_FILES)
                         and (not o["named"] or p in o["named"])
                         and whole_path_in(p, o["ctext"])):
```

### m9

```diff
--- frozen-count-c1.py
+++ count-c1-m9.py
@@ -180,7 +180,6 @@
                 why.append("evidence-paths=%d" % len(toks))
             for p in paths:
                 if not (p in o["at_commit"] and p in o["changed"]
-                        and (p.startswith(ARTIFACT_PREFIXES) or p in ARTIFACT_FILES)
                         and (not o["named"] or p in o["named"])
                         and whole_path_in(p, o["ctext"])):
                     why.append("weak-path:%s" % p)
```

### m10

```diff
--- frozen-count-c1.py
+++ count-c1-m10.py
@@ -181,7 +181,6 @@
             for p in paths:
                 if not (p in o["at_commit"] and p in o["changed"]
                         and (p.startswith(ARTIFACT_PREFIXES) or p in ARTIFACT_FILES)
-                        and (not o["named"] or p in o["named"])
                         and whole_path_in(p, o["ctext"])):
                     why.append("weak-path:%s" % p)
         if why:
```

### m11

```diff
--- frozen-count-c1.py
+++ count-c1-m11.py
@@ -181,8 +181,7 @@
             for p in paths:
                 if not (p in o["at_commit"] and p in o["changed"]
                         and (p.startswith(ARTIFACT_PREFIXES) or p in ARTIFACT_FILES)
-                        and (not o["named"] or p in o["named"])
-                        and whole_path_in(p, o["ctext"])):
+                        and (not o["named"] or p in o["named"])):
                     why.append("weak-path:%s" % p)
         if why:
             bad.append(key)
```

### m12

```diff
--- frozen-count-c1.py
+++ count-c1-m12.py
@@ -179,7 +179,7 @@
             if not 1 <= len(toks) <= 2:
                 why.append("evidence-paths=%d" % len(toks))
             for p in paths:
-                if not (p in o["at_commit"] and p in o["changed"]
+                if not (p in o["changed"]
                         and (p.startswith(ARTIFACT_PREFIXES) or p in ARTIFACT_FILES)
                         and (not o["named"] or p in o["named"])
                         and whole_path_in(p, o["ctext"])):
```

## Hashes and exact restoration
All copies had pristine SHA-256 `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167`. The table records each actual mutated byte hash; every restored hash was re-read and also observed with `sha256sum`. The frozen lane counter retained the same hash before and after.
| Mutant | Before SHA-256 | Mutated SHA-256 | Restored SHA-256 |
| --- | --- | --- | --- |
| m1 | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` | `993912c4f4b414399d9442a30ed391194db1074cfe81219ba2f8d6b141b0ff32` | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` |
| m2 | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` | `300b71f659dcae0f588399f560f60acea6aa3310884bb1880fe19de36db97b39` | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` |
| m3 | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` | `116e9d79c7d06f9126bcece1dfa2173b03509a8aa691705ca35b8e022787e950` | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` |
| m4 | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` | `2506c9c283df3619a9f92b9ea2cecaf94c86077ff177bd3d0fb348f34947f066` | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` |
| m5 | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` | `c39a83b5c1bf7b35fa9f350d61ba0f6f9bcf5941f28dc1d2260f7581096ebab4` | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` |
| m6 | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` | `4bcbb650edf217bee961ad27823a34f891f2697d1bdc8fa76ea8e99f678e132e` | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` |
| m7 | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` | `22eb52b84292690e291d89e58410c0c437d42a48f5bfabc42aaba302fb01eda0` | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` |
| m8 | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` | `73a717fd941b5fcbf21c3ce29fe4e850bc6520306d638336316b3c68edf1db29` | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` |
| m9 | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` | `8b7b88051d5d063578007bbb87038d72fffc1d7fa1f8a66e4fe105626de347c8` | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` |
| m10 | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` | `7b024889e31bc331f0e0c37363902068fe260b0860c00a90b3144c7781ab4d76` | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` |
| m11 | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` | `69acc2d6b313328c379da3cfd8e803e3842a0f4e48ddbfb6e534cb273895c83e` | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` |
| m12 | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` | `52da3059d7236fd3b23c32cb5b655750732d53bab0e60154bf67d1c269296c0a` | `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` |

The original scratch `count-c1.py` copy also remains byte-identical. All twelve mutated copies were restored in a `finally` block before the restored detector phase. For each probe, restored stdout equals pristine stdout byte-for-byte and restored exit equals 1.
Clone SCORECARD SHA-256 before and after removing the entire appended probe section: `8fbc058a9f8c5dc42fd75314e95d4bd9a1172d3e250cb86570d81db270052b2a` = `8fbc058a9f8c5dc42fd75314e95d4bd9a1172d3e250cb86570d81db270052b2a`. Sandbox restoration commit: `106fcb3b743e1ad16393f162f6c55e1755202349`; the named control commits remain available as evidence.
m6 artifact worktree SHA-256 before and after staged-only omission: `ceba4b68b018e9cd212cb54b4b98e32ccbdcb60eb2d82d74fa10bf9afd6ba388`. The file bytes never changed. No processes are left running: every spawned process was synchronous and bounded with `timeout`.
The only lane files written by this seat are this report and `MutCounterBounds-register.md`. The lane/fleet repositories, frozen contract/counter, MANIFEST, sibling sources, and `.ufo/state/` were not mutated.
## Full observed stdout and exits
Every command below was executed with the three Git environment overrides absent. Stderr was empty in every case. No summary or stdout was synthesized.

### positive — frozen

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py 90a8e8136d317f94cb86976fd7641c66dbc2ecbe --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=90a8e8136d317f94cb86976fd7641c66dbc2ecbe manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```

Exit: `0`. Stderr: empty.

### m1 — pristine

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m1.py ca205042a68fb7c25e0dc016acc4190b87d51792 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
row rounds[313].capabilities_added[0] missing
label=P-C1 rev=ca205042a68fb7c25e0dc016acc4190b87d51792 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=17 matched=17 missing=1 bad=0 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m1 — frozen

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py ca205042a68fb7c25e0dc016acc4190b87d51792 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
row rounds[313].capabilities_added[0] missing
label=P-C1 rev=ca205042a68fb7c25e0dc016acc4190b87d51792 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=17 matched=17 missing=1 bad=0 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m1 — mutated

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m1.py ca205042a68fb7c25e0dc016acc4190b87d51792 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
row rounds[313].capabilities_added[0] missing
label=P-C1 rev=ca205042a68fb7c25e0dc016acc4190b87d51792 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=17 matched=17 missing=1 bad=0 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m1 — restored

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m1.py ca205042a68fb7c25e0dc016acc4190b87d51792 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
row rounds[313].capabilities_added[0] missing
label=P-C1 rev=ca205042a68fb7c25e0dc016acc4190b87d51792 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=17 matched=17 missing=1 bad=0 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m2 — pristine

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m2.py 0e3abbdc26a9c2a3cc31336f11880e82402af16f --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
row rounds[999999].capabilities_added[0] extra 
label=P-C1 rev=0e3abbdc26a9c2a3cc31336f11880e82402af16f manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=19 matched=18 missing=0 bad=0 extra=1 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m2 — frozen

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py 0e3abbdc26a9c2a3cc31336f11880e82402af16f --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
row rounds[999999].capabilities_added[0] extra 
label=P-C1 rev=0e3abbdc26a9c2a3cc31336f11880e82402af16f manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=19 matched=18 missing=0 bad=0 extra=1 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m2 — mutated

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m2.py 0e3abbdc26a9c2a3cc31336f11880e82402af16f --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
row rounds[999999].capabilities_added[0] extra 
label=P-C1 rev=0e3abbdc26a9c2a3cc31336f11880e82402af16f manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=19 matched=18 missing=0 bad=0 extra=1 mismatches=1 C1=met
```

Exit: `0`. Stderr: empty.

### m2 — restored

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m2.py 0e3abbdc26a9c2a3cc31336f11880e82402af16f --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
row rounds[999999].capabilities_added[0] extra 
label=P-C1 rev=0e3abbdc26a9c2a3cc31336f11880e82402af16f manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=19 matched=18 missing=0 bad=0 extra=1 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m3 — pristine

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m3.py a762b10f9829af260caa7f27a6b2d4a3e580b54c --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
row rounds[313].capabilities_added[0] extra-duplicate 
label=P-C1 rev=a762b10f9829af260caa7f27a6b2d4a3e580b54c manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=19 matched=18 missing=0 bad=0 extra=1 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m3 — frozen

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py a762b10f9829af260caa7f27a6b2d4a3e580b54c --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
row rounds[313].capabilities_added[0] extra-duplicate 
label=P-C1 rev=a762b10f9829af260caa7f27a6b2d4a3e580b54c manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=19 matched=18 missing=0 bad=0 extra=1 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m3 — mutated

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m3.py a762b10f9829af260caa7f27a6b2d4a3e580b54c --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
row rounds[313].capabilities_added[0] extra-duplicate 
label=P-C1 rev=a762b10f9829af260caa7f27a6b2d4a3e580b54c manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=19 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```

Exit: `0`. Stderr: empty.

### m3 — restored

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m3.py a762b10f9829af260caa7f27a6b2d4a3e580b54c --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
row rounds[313].capabilities_added[0] extra-duplicate 
label=P-C1 rev=a762b10f9829af260caa7f27a6b2d4a3e580b54c manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=19 matched=18 missing=0 bad=0 extra=1 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m4 — pristine

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m4.py cf1bbd50e78cfe1d883504fbb4234ef8e1ef2017 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad round=13!=12
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=cf1bbd50e78cfe1d883504fbb4234ef8e1ef2017 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m4 — frozen

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py cf1bbd50e78cfe1d883504fbb4234ef8e1ef2017 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad round=13!=12
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=cf1bbd50e78cfe1d883504fbb4234ef8e1ef2017 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m4 — mutated

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m4.py cf1bbd50e78cfe1d883504fbb4234ef8e1ef2017 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=cf1bbd50e78cfe1d883504fbb4234ef8e1ef2017 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```

Exit: `0`. Stderr: empty.

### m4 — restored

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m4.py cf1bbd50e78cfe1d883504fbb4234ef8e1ef2017 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad round=13!=12
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=cf1bbd50e78cfe1d883504fbb4234ef8e1ef2017 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m5 — pristine

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m5.py ecce9f0d53dae0a92830477da27352dc333fb0a0 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad evidence-paths=0
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=ecce9f0d53dae0a92830477da27352dc333fb0a0 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m5 — frozen

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py ecce9f0d53dae0a92830477da27352dc333fb0a0 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad evidence-paths=0
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=ecce9f0d53dae0a92830477da27352dc333fb0a0 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m5 — mutated

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m5.py ecce9f0d53dae0a92830477da27352dc333fb0a0 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=ecce9f0d53dae0a92830477da27352dc333fb0a0 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```

Exit: `0`. Stderr: empty.

### m5 — restored

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m5.py ecce9f0d53dae0a92830477da27352dc333fb0a0 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad evidence-paths=0
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=ecce9f0d53dae0a92830477da27352dc333fb0a0 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m6 — pristine

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m6.py a0e64dd81c63bef3d143b15d9dcf12663be5622a --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad absent-at-rev:corpus/evidence/drift-r12-20261019T2204Z-classification.md
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=a0e64dd81c63bef3d143b15d9dcf12663be5622a manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m6 — frozen

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py a0e64dd81c63bef3d143b15d9dcf12663be5622a --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad absent-at-rev:corpus/evidence/drift-r12-20261019T2204Z-classification.md
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=a0e64dd81c63bef3d143b15d9dcf12663be5622a manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m6 — mutated

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m6.py a0e64dd81c63bef3d143b15d9dcf12663be5622a --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=a0e64dd81c63bef3d143b15d9dcf12663be5622a manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```

Exit: `0`. Stderr: empty.

### m6 — restored

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m6.py a0e64dd81c63bef3d143b15d9dcf12663be5622a --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad absent-at-rev:corpus/evidence/drift-r12-20261019T2204Z-classification.md
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=a0e64dd81c63bef3d143b15d9dcf12663be5622a manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m7 — pristine

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m7.py d73e32d7f2ad91b07f6664da1c2d581c0e385bf8 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad line-out-of-range:corpus/evidence/drift-r12-20261019T2204Z-classification.md:0
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=d73e32d7f2ad91b07f6664da1c2d581c0e385bf8 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m7 — frozen

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py d73e32d7f2ad91b07f6664da1c2d581c0e385bf8 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad line-out-of-range:corpus/evidence/drift-r12-20261019T2204Z-classification.md:0
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=d73e32d7f2ad91b07f6664da1c2d581c0e385bf8 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m7 — mutated

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m7.py d73e32d7f2ad91b07f6664da1c2d581c0e385bf8 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=d73e32d7f2ad91b07f6664da1c2d581c0e385bf8 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```

Exit: `0`. Stderr: empty.

### m7 — restored

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m7.py d73e32d7f2ad91b07f6664da1c2d581c0e385bf8 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad line-out-of-range:corpus/evidence/drift-r12-20261019T2204Z-classification.md:0
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=d73e32d7f2ad91b07f6664da1c2d581c0e385bf8 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m8 — pristine

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m8.py 3cde9343a1563503b1bd49dd9fb12aa9690886e2 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad weak-path:tools/mori-silence-cases.sh
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=3cde9343a1563503b1bd49dd9fb12aa9690886e2 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m8 — frozen

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py 3cde9343a1563503b1bd49dd9fb12aa9690886e2 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad weak-path:tools/mori-silence-cases.sh
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=3cde9343a1563503b1bd49dd9fb12aa9690886e2 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m8 — mutated

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m8.py 3cde9343a1563503b1bd49dd9fb12aa9690886e2 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=3cde9343a1563503b1bd49dd9fb12aa9690886e2 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```

Exit: `0`. Stderr: empty.

### m8 — restored

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m8.py 3cde9343a1563503b1bd49dd9fb12aa9690886e2 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad weak-path:tools/mori-silence-cases.sh
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=3cde9343a1563503b1bd49dd9fb12aa9690886e2 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m9 — pristine

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m9.py 1abed06626a9a6c831dbb387fce15c30982149f3 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad weak-path:LOG.md
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=1abed06626a9a6c831dbb387fce15c30982149f3 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m9 — frozen

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py 1abed06626a9a6c831dbb387fce15c30982149f3 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad weak-path:LOG.md
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=1abed06626a9a6c831dbb387fce15c30982149f3 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m9 — mutated

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m9.py 1abed06626a9a6c831dbb387fce15c30982149f3 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=1abed06626a9a6c831dbb387fce15c30982149f3 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```

Exit: `0`. Stderr: empty.

### m9 — restored

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m9.py 1abed06626a9a6c831dbb387fce15c30982149f3 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad weak-path:LOG.md
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=1abed06626a9a6c831dbb387fce15c30982149f3 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m10 — pristine

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m10.py 449a58949eba34017929f8530d84c93fc9d1c0f9 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] bad weak-path:corpus/evidence/freeze-register.json
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=449a58949eba34017929f8530d84c93fc9d1c0f9 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m10 — frozen

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py 449a58949eba34017929f8530d84c93fc9d1c0f9 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] bad weak-path:corpus/evidence/freeze-register.json
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=449a58949eba34017929f8530d84c93fc9d1c0f9 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m10 — mutated

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m10.py 449a58949eba34017929f8530d84c93fc9d1c0f9 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=449a58949eba34017929f8530d84c93fc9d1c0f9 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```

Exit: `0`. Stderr: empty.

### m10 — restored

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m10.py 449a58949eba34017929f8530d84c93fc9d1c0f9 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] bad weak-path:corpus/evidence/freeze-register.json
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=449a58949eba34017929f8530d84c93fc9d1c0f9 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m11 — pristine

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m11.py a2ba0ba4dbdae3f84ddc0c6d591b793cb580db74 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad weak-path:corpus/evidence/README.md
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=a2ba0ba4dbdae3f84ddc0c6d591b793cb580db74 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m11 — frozen

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py a2ba0ba4dbdae3f84ddc0c6d591b793cb580db74 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad weak-path:corpus/evidence/README.md
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=a2ba0ba4dbdae3f84ddc0c6d591b793cb580db74 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m11 — mutated

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m11.py a2ba0ba4dbdae3f84ddc0c6d591b793cb580db74 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=a2ba0ba4dbdae3f84ddc0c6d591b793cb580db74 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```

Exit: `0`. Stderr: empty.

### m11 — restored

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m11.py a2ba0ba4dbdae3f84ddc0c6d591b793cb580db74 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad weak-path:corpus/evidence/README.md
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=a2ba0ba4dbdae3f84ddc0c6d591b793cb580db74 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m12 — pristine

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m12.py 56fee54c0956f79ce9e0249d1dd52d414bac7fd7 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad weak-path:tools/mori-blind-check.sh
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=56fee54c0956f79ce9e0249d1dd52d414bac7fd7 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m12 — frozen

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py 56fee54c0956f79ce9e0249d1dd52d414bac7fd7 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad weak-path:tools/mori-blind-check.sh
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=56fee54c0956f79ce9e0249d1dd52d414bac7fd7 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m12 — mutated

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m12.py 56fee54c0956f79ce9e0249d1dd52d414bac7fd7 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad weak-path:tools/mori-blind-check.sh
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=56fee54c0956f79ce9e0249d1dd52d414bac7fd7 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

### m12 — restored

```sh
timeout 120 python3 /fast/scratch/hyaku/mori-r35/MutCounterBounds/count-c1-m12.py 56fee54c0956f79ce9e0249d1dd52d414bac7fd7 --repo /fast/scratch/hyaku/mori-r35/MutCounterBounds/clone
```

```text
row rounds[313].capabilities_added[0] bad weak-path:tools/mori-blind-check.sh
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] matched 
row rounds[386].capabilities_added[2] matched 
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] matched 
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] matched 
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] matched 
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] matched 
label=P-C1 rev=56fee54c0956f79ce9e0249d1dd52d414bac7fd7 manifest_rev=37b51a243302 register='## Capabilities (C0 MutCounterBounds probe)' oracle=18 rows=18 matched=17 missing=0 bad=1 extra=0 mismatches=1 C1=unmet
```

Exit: `1`. Stderr: empty.

Report: .ufo/waves/round-35/c0/MutCounterBounds.md
