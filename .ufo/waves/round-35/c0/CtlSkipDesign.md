# C0 CtlSkipDesign — three cheap register programs

## Result and scope

Counter verdicts: A **unmet**, B **met**, C **unmet**. **No tested program both skips the frozen capability-binding work and meets P-C1.** B meets with empty capability/what cells, but still performs the specifically claimed key/round/strong-artifact binding. This is not a softened skip finding; the distinction follows the frozen positive-control classification (`contract.md:95-99`).

Probe axes: frozen-counter compliance; actual per-capability binding versus shortcut; exact-byte restoration/containment. No semantic prose or best-pointer requirement was retroactively added to P-C1.

Pristine baseline fails (exit 1), so these are control-program observations, not claims of killed mutants: formal pristine/mutated/restored mutation verdict is **inconclusive**. A and C are rejected attempted shortcuts; B is a positive-control-style meet.

## Frozen inputs and containment

- Lane base: `f2d28711ee723c969b6c2008d32df498192f9e7b`.
- Fleet MANIFEST revision: `37b51a243302e8009c7067431e8a47f9a722fd14`.
- Counter executed at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py`.
- Counter SHA-256, from `sha256sum`, before, every scored control/restoration, and after: `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167`.
- Frozen contract SHA-256 before/after: `94b7f90a352c96a0b8be17cef62f95647aad06fa84c83d4540751d888d65ba40`.
- Only scratch clone SCORECARD was changed/committed. No git writes in lane/fleet repos; no counter, contract, MANIFEST or sibling edits.
- Only lane writes are this report and `c0/CtlSkipDesign-register.md` (under `.ufo/waves/round-35/`).
- Tools installed/updated: none. All subprocesses bounded with `timeout`; no background jobs or agents started.

## Construction and scoring

Actual clone setup:

```sh
timeout 10 mkdir -p /fast/scratch/hyaku/mori-r35/CtlSkipDesign
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r35/CtlSkipDesign/clone
timeout 20 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r35/CtlSkipDesign/clone checkout -q -b ctl-skip-design f2d28711ee723c969b6c2008d32df498192f9e7b
```

Each standalone program below was saved as `/fast/scratch/hyaku/mori-r35/CtlSkipDesign/program-{A,B,C}.py` and executed once with `timeout 120 python3 <absolute-program-path>` in an environment with `GIT_DIR`, `GIT_WORK_TREE`, `GIT_INDEX_FILE` absent. Every generator exited 0 and emitted exactly 22 lines to stdout. Programs only print register bytes; stdout was appended once to scratch `SCORECARD.md`, after one separating newline, with the edit tool. Each register is the sole appended section; original SCORECARD bytes are unchanged.

For each variant, the exact sandbox commit invocation was `timeout 20 git -C /fast/scratch/hyaku/mori-r35/CtlSkipDesign/clone -c user.name=ctl -c user.email=ctl@local -c commit.gpgsign=false commit -qam ctl-<variant>` with the same three environment variables removed. The same bounded detector was run on each committed revision:

```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py <commit> --repo /fast/scratch/hyaku/mori-r35/CtlSkipDesign/clone
```

After each score, exactly the 23 appended lines (separator plus register) were removed with the edit tool, committed with message `ctl-restore-<variant>`, hashed and scored by the identical detector. Each restored state was the next program's pristine baseline.

## Pristine output

Full stdout; exit **1**:

```text
row source registry extra 
row live census extra 
row census self-test extra 
row silence oracle extra 
row drift pin extra 
row rounds[313].capabilities_added[0] missing
row rounds[339].capabilities_added[0] missing
row rounds[345].capabilities_added[0] missing
row rounds[353].capabilities_added[0] missing
row rounds[386].capabilities_added[0] missing
row rounds[386].capabilities_added[1] missing
row rounds[386].capabilities_added[2] missing
row rounds[398].capabilities_added[0] missing
row rounds[427].capabilities_added[0] missing
row rounds[443].capabilities_added[0] missing
row rounds[443].capabilities_added[1] missing
row rounds[455].capabilities_added[0] missing
row rounds[455].capabilities_added[1] missing
row rounds[462].capabilities_added[0] missing
row rounds[476].capabilities_added[0] missing
row rounds[476].capabilities_added[1] missing
row rounds[495].capabilities_added[0] missing
row rounds[495].capabilities_added[1] missing
label=P-C1 rev=f2d28711ee723c969b6c2008d32df498192f9e7b manifest_rev=37b51a243302 register='## Capabilities (round 12 demonstrations)' oracle=18 rows=5 matched=0 missing=18 bad=0 extra=5 mismatches=23 C1=unmet
```

## Program A — capability-blind alphabetic artifact

**Attempted skip; counter verdict unmet (exit 1).** This omits capability-specific evidence selection: every capability of a round gets its alphabetically first changed, extant, closure-mentioned artifact, regardless of paths named by the capability. It still performs the MANIFEST-key/round and round-artifact lookup portions of the claimed work. Twelve rows fail the explicitly frozen named-path requirement; e.g. all three round-18 capabilities receive `corpus/evidence/freeze-register.json` rather than their different named tools. The six matched rows do not establish a skip: for capabilities without named paths, an arbitrary otherwise-strong artifact is allowed by the contract. Expected detector: `weak-path` on named-path mismatches; observed 12 such bad rows. No skip-the-work meet.

Clone commit: `4e334893abfeb0ddad3943d10f3f689a42e3f147`. Generator: 47 lines; register: 22 lines; register SHA-256: `e9277fb1d4b54bba8aa11691223e14a372492685bf5e0a0a3811ba334a931775`.

```python
import json, os, re, subprocess
FLEET = "/home/vgpnk/Projects/shokunin"
REPO = "/fast/scratch/hyaku/mori-r35/CtlSkipDesign/clone"
REV = "37b51a243302e8009c7067431e8a47f9a722fd14"
BASE = "f2d28711ee723c969b6c2008d32df498192f9e7b"
ENV = {k: v for k, v in os.environ.items()
       if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")}
def git(repo, *args, optional=False):
    p = subprocess.run(["timeout", "20", "git", "-C", repo, *args],
                       env=ENV, text=True, capture_output=True, timeout=25)
    if p.returncode and not optional:
        raise RuntimeError(p.stderr)
    return p.stdout if p.returncode == 0 else ""
def whole(path, text):
    return re.search(r"(?<![A-Za-z0-9_./-])(?:mori-shokunin/)?" +
                     re.escape(path) + r"(?![A-Za-z0-9_/-])", text)
NAMED = re.compile(r"((?:tools|corpus/knowledge)/[A-Za-z0-9_./-]*[A-Za-z0-9_])")
SPOT = re.compile(r"mori-shokunin/([A-Za-z0-9_./-]+)@([0-9a-f]{7,40})")
manifest = json.loads(git(FLEET, "show", REV + ":MANIFEST.json"))
at_tip = set(git(REPO, "ls-tree", "-r", "--name-only", BASE).splitlines())
print("## Capabilities (CtlSkipDesign A)")
print("\n| key | capability | what it can now do | evidence | first-working round |")
print("|---|---|---|---|---|")
prev = "20e2255"
for i, row in enumerate(manifest["rounds"]):
    if row.get("lane") != "mori":
        continue
    commit = row["commit"].split("@", 1)[1]
    caps = row.get("capabilities_added") or []
    if row.get("admitted") is True and caps:
        changed = set(git(REPO, "diff", "--name-only", "--no-renames",
                          prev, commit).splitlines())
        tree = set(git(REPO, "ls-tree", "-r", "--name-only", commit).splitlines())
        vtext = json.dumps(row.get("verification") or {}, ensure_ascii=False)
        record = [vtext, "\n".join(caps)]
        for path, rev in SPOT.findall(vtext):
            record.append(git(REPO, "show", rev + ":" + path, optional=True))
        if row.get("report"):
            record.append(git(FLEET, "show", REV + ":" + row["report"], optional=True))
        text = "\n".join(record)
        paths = sorted(p for p in changed & tree & at_tip
                       if (p.startswith(("tools/", "corpus/knowledge/", "corpus/evidence/"))
                           or p == "corpus/SOURCES.md") and whole(p, text))
        picked = [paths[0]] * len(caps)
        for j, path in enumerate(picked):
            print(f"| `rounds[{i}].capabilities_added[{j}]` | junk | junk | `{path}` | {row['round']} |")
    prev = commit
```

Full counter stdout; exit **1**; stderr empty:

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] bad weak-path:corpus/evidence/freeze-register.json
row rounds[386].capabilities_added[1] bad weak-path:corpus/evidence/freeze-register.json
row rounds[386].capabilities_added[2] bad weak-path:corpus/evidence/freeze-register.json
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] bad weak-path:corpus/knowledge/retention-reconciliation-r22.md
row rounds[443].capabilities_added[0] bad weak-path:corpus/knowledge/system-pressure-r24.md
row rounds[443].capabilities_added[1] bad weak-path:corpus/knowledge/system-pressure-r24.md
row rounds[455].capabilities_added[0] bad weak-path:corpus/evidence/retention-allowlist.json
row rounds[455].capabilities_added[1] bad weak-path:corpus/evidence/retention-allowlist.json
row rounds[462].capabilities_added[0] bad weak-path:corpus/SOURCES.md
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] bad weak-path:corpus/SOURCES.md
row rounds[495].capabilities_added[0] bad weak-path:corpus/SOURCES.md
row rounds[495].capabilities_added[1] bad weak-path:corpus/SOURCES.md
label=P-C1 rev=4e334893abfeb0ddad3943d10f3f689a42e3f147 manifest_rev=37b51a243302 register='## Capabilities (CtlSkipDesign A)' oracle=18 rows=18 matched=6 missing=0 bad=12 extra=0 mismatches=12 C1=unmet
```

## Program B — minimum strong binding with empty prose

**Does the frozen binding work; counter verdict met (exit 0).** This is the cheapest meeting candidate tested: one lexicographically first strong path per key, with both human-readable capability and what cells empty. It deliberately skips writing useful repertoire prose and choosing the best semantic pointer, but it does NOT skip the work as this assignment/contract defines it. Each MANIFEST key identifies the capability; its correct round and independently checked landed/closure-mentioned artifact are present, and named-path capabilities get a path they name. `corpus/SOURCES.md` is reused for rounds 12, 14, 15 and one round-28 capability only after the per-round checks; reuse alone is not a bypass. Contract lines 95–99 explicitly classify an oracle-derived register with one strong artifact per row as doing the work and reserve prose/pointer quality to reviewers. P-C1 imposes no additional natural-language name/what equality requirement. Empty cells expose the limit of P-C1 relative to the broader AXES repertoire usability contract, not a demonstrated skip of the frozen binding claim. Expected detector: all 18 matched; observed all 18 matched. This met result is a positive-control result, not a surviving skip mutant.

Clone commit: `3336047c1be4e0ed5217ec57abcbd8df693224f2`. Generator: 48 lines; register: 22 lines; register SHA-256: `299e7fe27ef829a0846d603f632ff4f61d6864e97f719c732389126ce8769178`.

```python
import json, os, re, subprocess
FLEET = "/home/vgpnk/Projects/shokunin"
REPO = "/fast/scratch/hyaku/mori-r35/CtlSkipDesign/clone"
REV = "37b51a243302e8009c7067431e8a47f9a722fd14"
BASE = "f2d28711ee723c969b6c2008d32df498192f9e7b"
ENV = {k: v for k, v in os.environ.items()
       if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")}
def git(repo, *args, optional=False):
    p = subprocess.run(["timeout", "20", "git", "-C", repo, *args],
                       env=ENV, text=True, capture_output=True, timeout=25)
    if p.returncode and not optional:
        raise RuntimeError(p.stderr)
    return p.stdout if p.returncode == 0 else ""
def whole(path, text):
    return re.search(r"(?<![A-Za-z0-9_./-])(?:mori-shokunin/)?" +
                     re.escape(path) + r"(?![A-Za-z0-9_/-])", text)
NAMED = re.compile(r"((?:tools|corpus/knowledge)/[A-Za-z0-9_./-]*[A-Za-z0-9_])")
SPOT = re.compile(r"mori-shokunin/([A-Za-z0-9_./-]+)@([0-9a-f]{7,40})")
manifest = json.loads(git(FLEET, "show", REV + ":MANIFEST.json"))
at_tip = set(git(REPO, "ls-tree", "-r", "--name-only", BASE).splitlines())
print("## Capabilities (CtlSkipDesign B)")
print("\n| key | capability | what it can now do | evidence | first-working round |")
print("|---|---|---|---|---|")
prev = "20e2255"
for i, row in enumerate(manifest["rounds"]):
    if row.get("lane") != "mori":
        continue
    commit = row["commit"].split("@", 1)[1]
    caps = row.get("capabilities_added") or []
    if row.get("admitted") is True and caps:
        changed = set(git(REPO, "diff", "--name-only", "--no-renames",
                          prev, commit).splitlines())
        tree = set(git(REPO, "ls-tree", "-r", "--name-only", commit).splitlines())
        vtext = json.dumps(row.get("verification") or {}, ensure_ascii=False)
        record = [vtext, "\n".join(caps)]
        for path, rev in SPOT.findall(vtext):
            record.append(git(REPO, "show", rev + ":" + path, optional=True))
        if row.get("report"):
            record.append(git(FLEET, "show", REV + ":" + row["report"], optional=True))
        text = "\n".join(record)
        paths = sorted(p for p in changed & tree & at_tip
                       if (p.startswith(("tools/", "corpus/knowledge/", "corpus/evidence/"))
                           or p == "corpus/SOURCES.md") and whole(p, text))
        picked = [next(p for p in paths if not NAMED.findall(cap)
                       or p in NAMED.findall(cap)) for cap in caps]
        for j, path in enumerate(picked):
            print(f"| `rounds[{i}].capabilities_added[{j}]` |  |  | `{path}` | {row['round']} |")
    prev = commit
```

Full counter stdout; exit **0**; stderr empty:

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
label=P-C1 rev=3336047c1be4e0ed5217ec57abcbd8df693224f2 manifest_rev=37b51a243302 register='## Capabilities (CtlSkipDesign B)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```

## Program C — one artifact per round, first-capability selection

**Attempted skip; counter verdict unmet (exit 1).** This chooses a strong artifact only for the first capability of each round, then reuses it for every other capability of that round without reading their named-path constraints. It therefore omits per-capability binding for six later rows (two in round 18, one each in 24, 25, 28 and 31), while retaining the real key/round/closure-artifact lookup for the first row of every round. Expected detector: `weak-path` for those six reused-but-wrong paths; observed exactly six bad rows. No skip-the-work meet.

Clone commit: `84f58fad8cde3254cf6d37114865d09895ca1573`. Generator: 48 lines; register: 22 lines; register SHA-256: `1677d0cdcb51bc07a86dcf9d6115f652ab28a3d527a2a0de162f68c5583c423a`.

```python
import json, os, re, subprocess
FLEET = "/home/vgpnk/Projects/shokunin"
REPO = "/fast/scratch/hyaku/mori-r35/CtlSkipDesign/clone"
REV = "37b51a243302e8009c7067431e8a47f9a722fd14"
BASE = "f2d28711ee723c969b6c2008d32df498192f9e7b"
ENV = {k: v for k, v in os.environ.items()
       if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")}
def git(repo, *args, optional=False):
    p = subprocess.run(["timeout", "20", "git", "-C", repo, *args],
                       env=ENV, text=True, capture_output=True, timeout=25)
    if p.returncode and not optional:
        raise RuntimeError(p.stderr)
    return p.stdout if p.returncode == 0 else ""
def whole(path, text):
    return re.search(r"(?<![A-Za-z0-9_./-])(?:mori-shokunin/)?" +
                     re.escape(path) + r"(?![A-Za-z0-9_/-])", text)
NAMED = re.compile(r"((?:tools|corpus/knowledge)/[A-Za-z0-9_./-]*[A-Za-z0-9_])")
SPOT = re.compile(r"mori-shokunin/([A-Za-z0-9_./-]+)@([0-9a-f]{7,40})")
manifest = json.loads(git(FLEET, "show", REV + ":MANIFEST.json"))
at_tip = set(git(REPO, "ls-tree", "-r", "--name-only", BASE).splitlines())
print("## Capabilities (CtlSkipDesign C)")
print("\n| key | capability | what it can now do | evidence | first-working round |")
print("|---|---|---|---|---|")
prev = "20e2255"
for i, row in enumerate(manifest["rounds"]):
    if row.get("lane") != "mori":
        continue
    commit = row["commit"].split("@", 1)[1]
    caps = row.get("capabilities_added") or []
    if row.get("admitted") is True and caps:
        changed = set(git(REPO, "diff", "--name-only", "--no-renames",
                          prev, commit).splitlines())
        tree = set(git(REPO, "ls-tree", "-r", "--name-only", commit).splitlines())
        vtext = json.dumps(row.get("verification") or {}, ensure_ascii=False)
        record = [vtext, "\n".join(caps)]
        for path, rev in SPOT.findall(vtext):
            record.append(git(REPO, "show", rev + ":" + path, optional=True))
        if row.get("report"):
            record.append(git(FLEET, "show", REV + ":" + row["report"], optional=True))
        text = "\n".join(record)
        paths = sorted(p for p in changed & tree & at_tip
                       if (p.startswith(("tools/", "corpus/knowledge/", "corpus/evidence/"))
                           or p == "corpus/SOURCES.md") and whole(p, text))
        named = set(NAMED.findall(caps[0]))
        picked = [next(p for p in paths if not named or p in named)] * len(caps)
        for j, path in enumerate(picked):
            print(f"| `rounds[{i}].capabilities_added[{j}]` | junk | junk | `{path}` | {row['round']} |")
    prev = commit
```

Full counter stdout; exit **1**; stderr empty:

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] matched 
row rounds[386].capabilities_added[0] matched 
row rounds[386].capabilities_added[1] bad weak-path:tools/mori-retention-gate.py
row rounds[386].capabilities_added[2] bad weak-path:tools/mori-retention-gate.py
row rounds[398].capabilities_added[0] matched 
row rounds[427].capabilities_added[0] matched 
row rounds[443].capabilities_added[0] matched 
row rounds[443].capabilities_added[1] bad weak-path:tools/mori-pressure.py
row rounds[455].capabilities_added[0] matched 
row rounds[455].capabilities_added[1] bad weak-path:tools/mori-job-runway.py
row rounds[462].capabilities_added[0] matched 
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] bad weak-path:corpus/SOURCES.md
row rounds[495].capabilities_added[0] matched 
row rounds[495].capabilities_added[1] bad weak-path:tools/mori-blind-check.sh
label=P-C1 rev=84f58fad8cde3254cf6d37114865d09895ca1573 manifest_rev=37b51a243302 register='## Capabilities (CtlSkipDesign C)' oracle=18 rows=18 matched=12 missing=0 bad=6 extra=0 mismatches=6 C1=unmet
```

## Exact restoration evidence

Pristine SCORECARD SHA-256: `8fbc058a9f8c5dc42fd75314e95d4bd9a1172d3e250cb86570d81db270052b2a` (`sha256sum` before mutation).

| Program | Mutated SCORECARD SHA-256 | Restored commit | Restored SCORECARD SHA-256 |
|---|---|---|---|
| A | `7f2ee39ff8fc428ddeb8806feed433a2316d9780213d7c7b96124e6663b570f6` | `b67ee1ee387dc8507199ccb5d2b7f0082e7aeab1` | `8fbc058a9f8c5dc42fd75314e95d4bd9a1172d3e250cb86570d81db270052b2a` |
| B | `162cb1db1c86d5fe0de84d932482c507181e83dbbe9f022bc5eacb06c6c00b1c` | `343016632b8b159ccc0f983f3fe995d2b59e637d` | `8fbc058a9f8c5dc42fd75314e95d4bd9a1172d3e250cb86570d81db270052b2a` |
| C | `f0728b837eaea55f8a98b64f87ab714bd22407989cd66c590a833e24c6aae33b` | `cf3554cb67f0ad0723c4649b4867f256945e4748` | `8fbc058a9f8c5dc42fd75314e95d4bd9a1172d3e250cb86570d81db270052b2a` |

All three restored hashes equal the pristine hash. The final clone is restored, at `cf3554cb67f0ad0723c4649b4867f256945e4748`. The same failing pristine detector behavior returned after each removal; no baseline failure is counted as a killed mutant. Full restoration stdout follows.

### Restored A

Exit **1**; stderr empty:

```text
row source registry extra 
row live census extra 
row census self-test extra 
row silence oracle extra 
row drift pin extra 
row rounds[313].capabilities_added[0] missing
row rounds[339].capabilities_added[0] missing
row rounds[345].capabilities_added[0] missing
row rounds[353].capabilities_added[0] missing
row rounds[386].capabilities_added[0] missing
row rounds[386].capabilities_added[1] missing
row rounds[386].capabilities_added[2] missing
row rounds[398].capabilities_added[0] missing
row rounds[427].capabilities_added[0] missing
row rounds[443].capabilities_added[0] missing
row rounds[443].capabilities_added[1] missing
row rounds[455].capabilities_added[0] missing
row rounds[455].capabilities_added[1] missing
row rounds[462].capabilities_added[0] missing
row rounds[476].capabilities_added[0] missing
row rounds[476].capabilities_added[1] missing
row rounds[495].capabilities_added[0] missing
row rounds[495].capabilities_added[1] missing
label=P-C1 rev=b67ee1ee387dc8507199ccb5d2b7f0082e7aeab1 manifest_rev=37b51a243302 register='## Capabilities (round 12 demonstrations)' oracle=18 rows=5 matched=0 missing=18 bad=0 extra=5 mismatches=23 C1=unmet
```

### Restored B

Exit **1**; stderr empty:

```text
row source registry extra 
row live census extra 
row census self-test extra 
row silence oracle extra 
row drift pin extra 
row rounds[313].capabilities_added[0] missing
row rounds[339].capabilities_added[0] missing
row rounds[345].capabilities_added[0] missing
row rounds[353].capabilities_added[0] missing
row rounds[386].capabilities_added[0] missing
row rounds[386].capabilities_added[1] missing
row rounds[386].capabilities_added[2] missing
row rounds[398].capabilities_added[0] missing
row rounds[427].capabilities_added[0] missing
row rounds[443].capabilities_added[0] missing
row rounds[443].capabilities_added[1] missing
row rounds[455].capabilities_added[0] missing
row rounds[455].capabilities_added[1] missing
row rounds[462].capabilities_added[0] missing
row rounds[476].capabilities_added[0] missing
row rounds[476].capabilities_added[1] missing
row rounds[495].capabilities_added[0] missing
row rounds[495].capabilities_added[1] missing
label=P-C1 rev=343016632b8b159ccc0f983f3fe995d2b59e637d manifest_rev=37b51a243302 register='## Capabilities (round 12 demonstrations)' oracle=18 rows=5 matched=0 missing=18 bad=0 extra=5 mismatches=23 C1=unmet
```

### Restored C

Exit **1**; stderr empty:

```text
row source registry extra 
row live census extra 
row census self-test extra 
row silence oracle extra 
row drift pin extra 
row rounds[313].capabilities_added[0] missing
row rounds[339].capabilities_added[0] missing
row rounds[345].capabilities_added[0] missing
row rounds[353].capabilities_added[0] missing
row rounds[386].capabilities_added[0] missing
row rounds[386].capabilities_added[1] missing
row rounds[386].capabilities_added[2] missing
row rounds[398].capabilities_added[0] missing
row rounds[427].capabilities_added[0] missing
row rounds[443].capabilities_added[0] missing
row rounds[443].capabilities_added[1] missing
row rounds[455].capabilities_added[0] missing
row rounds[455].capabilities_added[1] missing
row rounds[462].capabilities_added[0] missing
row rounds[476].capabilities_added[0] missing
row rounds[476].capabilities_added[1] missing
row rounds[495].capabilities_added[0] missing
row rounds[495].capabilities_added[1] missing
label=P-C1 rev=cf3554cb67f0ad0723c4649b4867f256945e4748 manifest_rev=37b51a243302 register='## Capabilities (round 12 demonstrations)' oracle=18 rows=5 matched=0 missing=18 bad=0 extra=5 mismatches=23 C1=unmet
```

## Strongest register saved

`c0/CtlSkipDesign-register.md` is program B's exact 22-line emitted register (SHA-256 `299e7fe27ef829a0846d603f632ff4f61d6864e97f719c732389126ce8769178`), scored at clone commit `3336047c1be4e0ed5217ec57abcbd8df693224f2`. It is the strongest adversarial prose-omission candidate here, but it still does the frozen binding work. No skip-the-work C1=met finding is claimed.
