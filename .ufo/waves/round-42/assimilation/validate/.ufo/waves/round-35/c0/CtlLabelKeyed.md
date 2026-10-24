# CtlLabelKeyed — Control 4, correct keys/rounds without evidence lookup

## Control and skipped work

One plausible defect: fill the admitted-capability register from MANIFEST labels and round numbers, then substitute a mechanically chosen generic evidence path for every capability instead of looking up the closure's strong artifact.

The 18 keys are full `rounds` array indices at fleet revision `37b51a243302e8009c7067431e8a47f9a722fd14`, restricted to `lane == "mori"`, `admitted is True`, and non-empty `capabilities_added`. Capability text is copied verbatim. All rows have correct rounds and exactly one backticked evidence path.

- A: `SCORECARD.md` for every row.
- B: `LOG.md` for every row.
- C: mechanically derive `corpus/lessons/round-N-verifier-spotcheck.md` from the round (no existence or artifact lookup).
- D: `corpus/SOURCES.md` for every row.

Expected detector: the frozen P-C1 counter must report `C1=unmet`, exit 1 for each generic-evidence control; keys and rounds alone must not suffice.

## Result

All four skip controls report **unmet**, exit 1. A/B/C match 0/18; D is closest, matching 4/18 with 14 bad rows. No control reports `C1=met`. D's accepted keys are `rounds[313].capabilities_added[0]`, `rounds[339].capabilities_added[0]`, `rounds[345].capabilities_added[0]`, and `rounds[476].capabilities_added[0]`. The saved register is exactly D's appended section (23 lines), not the full SCORECARD.

Mutation-kill classification: **inconclusive**, not a killed mutant, because the required pristine frozen revision itself reports unmet. The observed skip-control verdicts are nevertheless all unmet. This probe makes no wider contract or counter-validity judgment.

## Frozen counter and containment

Executed directly: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py`.

Before and after `sha256sum` both returned:

```text
27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py
```

All git writes were confined to `/fast/scratch/hyaku/mori-r35/CtlLabelKeyed/clone`; GIT_DIR, GIT_WORK_TREE, and GIT_INDEX_FILE were omitted from subprocess environments. No frozen contract, counter, fleet MANIFEST, sibling lane, or state file was edited. These two requested report/register files are this seat's only lane writes. No tools were installed or updated. All child commands were timeout-bounded, foreground, and finished before this report; no background jobs or subagents were started.

## Build

Actual clone/check-out commands (all successful, exit 0):

```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE mkdir -p /fast/scratch/hyaku/mori-r35/CtlLabelKeyed
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r35/CtlLabelKeyed/clone
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r35/CtlLabelKeyed/clone checkout -qb ctl-label-keyed f2d28711ee723c969b6c2008d32df498192f9e7b
```

Actual SCORECARD modifications used hashline edits: append A at EOF; replace only rows 1945–1962 for B, C, and D; finally cut appended lines 1940–1962 to restore. Every state was committed with `timeout 60 git -C /fast/scratch/hyaku/mori-r35/CtlLabelKeyed/clone -c user.name=ctl -c user.email=ctl@local commit -qam ctl` in the sanitized environment.

Equivalent bounded reproduction generator below (not separately executed; reproduces the same SCORECARD bytes after the fresh clone above; commit identities depend on timestamps). Every write replaces a fixed-size file once; there is no append-to-log loop. The actual pristine detector invocation and all actual scored revisions/stdout are recorded below.

```python
import os, json, hashlib, subprocess
from pathlib import Path
R = "/fast/scratch/hyaku/mori-r35/CtlLabelKeyed/clone"
F = "/home/vgpnk/Projects/shokunin"
C = F + "/mori-shokunin/.ufo/waves/round-35/count-c1.py"
B = "f2d28711ee723c969b6c2008d32df498192f9e7b"
M = "37b51a243302e8009c7067431e8a47f9a722fd14"
E = {k:v for k,v in os.environ.items()
     if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")}
def run(args, check=True):
    return subprocess.run(["timeout", "120", *args], env=E,
                          capture_output=True, timeout=125, check=check)
def git(*args):
    return run(["git", "-C", R, *args]).stdout
base = git("show", B + ":SCORECARD.md")
manifest = json.loads(run(["git", "-C", F, "show", M+":MANIFEST.json"]).stdout)
rows = [(i,j,r["round"],cap) for i,r in enumerate(manifest["rounds"])
        if r.get("lane")=="mori" and r.get("admitted") is True
        for j,cap in enumerate(r.get("capabilities_added") or [])]
header = ("\n## Capabilities (label-keyed control)\n\n"
          "| Key | Capability | What it can now do | Evidence | First-working round |\n"
          "|---|---|---|---|---|\n")
for label in ("A", "B", "C", "D", "restored"):
    register = header
    for i,j,rnd,cap in rows:
        p = {"A":"SCORECARD.md", "B":"LOG.md",
             "C":f"corpus/lessons/round-{rnd}-verifier-spotcheck.md",
             "D":"corpus/SOURCES.md"}.get(label)
        register += (f"| `rounds[{i}].capabilities_added[{j}]` | {cap} | "
                     f"Recorded capability; evidence lookup skipped. | `{p}` | {rnd} |\n")
    data = base if label=="restored" else base + register.encode()
    Path(R+"/SCORECARD.md").write_bytes(data)
    git("-c", "user.name=ctl", "-c", "user.email=ctl@local", "commit", "-qam", "ctl")
    rev = git("rev-parse", "HEAD").decode().strip()
    print(label, rev, hashlib.sha256(data).hexdigest())
    scored = run(["python3", C, rev, "--repo", R], check=False)
    print(scored.stdout.decode(), end="")
    print("exit="+str(scored.returncode))
```

## Committed states and SCORECARD SHA-256

| State | Clone commit | SCORECARD SHA-256 |
|---|---|---|
| pristine | `f2d28711ee723c969b6c2008d32df498192f9e7b` | `8fbc058a9f8c5dc42fd75314e95d4bd9a1172d3e250cb86570d81db270052b2a` |
| A | `850241d834fd0080f2efe28ed051942e1b72dfcb` | `4cfa3e6937a18bcdf96d1f988699bb00d0bb8f0a758cd066a535842ac22d9a52` |
| B | `ef5ac6000d3f6c2667bfe8eb6ef3565f07487b47` | `a5523761be88bcf45c32b60ea02e139262b90169a009392d79d64edec973dd35` |
| C | `b3349d77a06d00046a09f069b398db069a8c7e35` | `cbc5e62af54e6fb12879e3200f759824a25469a16cc7a267759e96f21c55def5` |
| D | `f7750ba8d7f452493281db264241cf9f727f49cc` | `5721b191524bce3422c6fade48d93c2fa19ac1c20bf8f8647e49a98dda059547` |
| restored | `3d5c6173431cf188461a7a7abf1731a6f33edca5` | `8fbc058a9f8c5dc42fd75314e95d4bd9a1172d3e250cb86570d81db270052b2a` |

## Exact detector outputs

All stderr streams were empty. Each command below used the sanitized environment described above.

### pristine

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py f2d28711ee723c969b6c2008d32df498192f9e7b --repo /fast/scratch/hyaku/mori-r35/CtlLabelKeyed/clone
```

Full stdout:

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

Exit: `1`. Verdict: **unmet**.

### A

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py 850241d834fd0080f2efe28ed051942e1b72dfcb --repo /fast/scratch/hyaku/mori-r35/CtlLabelKeyed/clone
```

Full stdout:

```text
row rounds[313].capabilities_added[0] bad weak-path:SCORECARD.md
row rounds[339].capabilities_added[0] bad weak-path:SCORECARD.md
row rounds[345].capabilities_added[0] bad weak-path:SCORECARD.md
row rounds[353].capabilities_added[0] bad weak-path:SCORECARD.md
row rounds[386].capabilities_added[0] bad weak-path:SCORECARD.md
row rounds[386].capabilities_added[1] bad weak-path:SCORECARD.md
row rounds[386].capabilities_added[2] bad weak-path:SCORECARD.md
row rounds[398].capabilities_added[0] bad weak-path:SCORECARD.md
row rounds[427].capabilities_added[0] bad weak-path:SCORECARD.md
row rounds[443].capabilities_added[0] bad weak-path:SCORECARD.md
row rounds[443].capabilities_added[1] bad weak-path:SCORECARD.md
row rounds[455].capabilities_added[0] bad weak-path:SCORECARD.md
row rounds[455].capabilities_added[1] bad weak-path:SCORECARD.md
row rounds[462].capabilities_added[0] bad weak-path:SCORECARD.md
row rounds[476].capabilities_added[0] bad weak-path:SCORECARD.md
row rounds[476].capabilities_added[1] bad weak-path:SCORECARD.md
row rounds[495].capabilities_added[0] bad weak-path:SCORECARD.md
row rounds[495].capabilities_added[1] bad weak-path:SCORECARD.md
label=P-C1 rev=850241d834fd0080f2efe28ed051942e1b72dfcb manifest_rev=37b51a243302 register='## Capabilities (label-keyed control)' oracle=18 rows=18 matched=0 missing=0 bad=18 extra=0 mismatches=18 C1=unmet
```

Exit: `1`. Verdict: **unmet**.

### B

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py ef5ac6000d3f6c2667bfe8eb6ef3565f07487b47 --repo /fast/scratch/hyaku/mori-r35/CtlLabelKeyed/clone
```

Full stdout:

```text
row rounds[313].capabilities_added[0] bad weak-path:LOG.md
row rounds[339].capabilities_added[0] bad weak-path:LOG.md
row rounds[345].capabilities_added[0] bad weak-path:LOG.md
row rounds[353].capabilities_added[0] bad weak-path:LOG.md
row rounds[386].capabilities_added[0] bad weak-path:LOG.md
row rounds[386].capabilities_added[1] bad weak-path:LOG.md
row rounds[386].capabilities_added[2] bad weak-path:LOG.md
row rounds[398].capabilities_added[0] bad weak-path:LOG.md
row rounds[427].capabilities_added[0] bad weak-path:LOG.md
row rounds[443].capabilities_added[0] bad weak-path:LOG.md
row rounds[443].capabilities_added[1] bad weak-path:LOG.md
row rounds[455].capabilities_added[0] bad weak-path:LOG.md
row rounds[455].capabilities_added[1] bad weak-path:LOG.md
row rounds[462].capabilities_added[0] bad weak-path:LOG.md
row rounds[476].capabilities_added[0] bad weak-path:LOG.md
row rounds[476].capabilities_added[1] bad weak-path:LOG.md
row rounds[495].capabilities_added[0] bad weak-path:LOG.md
row rounds[495].capabilities_added[1] bad weak-path:LOG.md
label=P-C1 rev=ef5ac6000d3f6c2667bfe8eb6ef3565f07487b47 manifest_rev=37b51a243302 register='## Capabilities (label-keyed control)' oracle=18 rows=18 matched=0 missing=0 bad=18 extra=0 mismatches=18 C1=unmet
```

Exit: `1`. Verdict: **unmet**.

### C

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py b3349d77a06d00046a09f069b398db069a8c7e35 --repo /fast/scratch/hyaku/mori-r35/CtlLabelKeyed/clone
```

Full stdout:

```text
row rounds[313].capabilities_added[0] bad weak-path:corpus/lessons/round-12-verifier-spotcheck.md
row rounds[339].capabilities_added[0] bad weak-path:corpus/lessons/round-14-verifier-spotcheck.md
row rounds[345].capabilities_added[0] bad weak-path:corpus/lessons/round-15-verifier-spotcheck.md
row rounds[353].capabilities_added[0] bad weak-path:corpus/lessons/round-16-verifier-spotcheck.md
row rounds[386].capabilities_added[0] bad weak-path:corpus/lessons/round-18-verifier-spotcheck.md
row rounds[386].capabilities_added[1] bad weak-path:corpus/lessons/round-18-verifier-spotcheck.md
row rounds[386].capabilities_added[2] bad weak-path:corpus/lessons/round-18-verifier-spotcheck.md
row rounds[398].capabilities_added[0] bad absent-at-rev:corpus/lessons/round-19-verifier-spotcheck.md
row rounds[427].capabilities_added[0] bad absent-at-rev:corpus/lessons/round-22-verifier-spotcheck.md
row rounds[443].capabilities_added[0] bad weak-path:corpus/lessons/round-24-verifier-spotcheck.md
row rounds[443].capabilities_added[1] bad weak-path:corpus/lessons/round-24-verifier-spotcheck.md
row rounds[455].capabilities_added[0] bad weak-path:corpus/lessons/round-25-verifier-spotcheck.md
row rounds[455].capabilities_added[1] bad weak-path:corpus/lessons/round-25-verifier-spotcheck.md
row rounds[462].capabilities_added[0] bad weak-path:corpus/lessons/round-26-verifier-spotcheck.md
row rounds[476].capabilities_added[0] bad weak-path:corpus/lessons/round-28-verifier-spotcheck.md
row rounds[476].capabilities_added[1] bad weak-path:corpus/lessons/round-28-verifier-spotcheck.md
row rounds[495].capabilities_added[0] bad weak-path:corpus/lessons/round-31-verifier-spotcheck.md
row rounds[495].capabilities_added[1] bad weak-path:corpus/lessons/round-31-verifier-spotcheck.md
label=P-C1 rev=b3349d77a06d00046a09f069b398db069a8c7e35 manifest_rev=37b51a243302 register='## Capabilities (label-keyed control)' oracle=18 rows=18 matched=0 missing=0 bad=18 extra=0 mismatches=18 C1=unmet
```

Exit: `1`. Verdict: **unmet**.

### D

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py f7750ba8d7f452493281db264241cf9f727f49cc --repo /fast/scratch/hyaku/mori-r35/CtlLabelKeyed/clone
```

Full stdout:

```text
row rounds[313].capabilities_added[0] matched 
row rounds[339].capabilities_added[0] matched 
row rounds[345].capabilities_added[0] matched 
row rounds[353].capabilities_added[0] bad weak-path:corpus/SOURCES.md
row rounds[386].capabilities_added[0] bad weak-path:corpus/SOURCES.md
row rounds[386].capabilities_added[1] bad weak-path:corpus/SOURCES.md
row rounds[386].capabilities_added[2] bad weak-path:corpus/SOURCES.md
row rounds[398].capabilities_added[0] bad weak-path:corpus/SOURCES.md
row rounds[427].capabilities_added[0] bad weak-path:corpus/SOURCES.md
row rounds[443].capabilities_added[0] bad weak-path:corpus/SOURCES.md
row rounds[443].capabilities_added[1] bad weak-path:corpus/SOURCES.md
row rounds[455].capabilities_added[0] bad weak-path:corpus/SOURCES.md
row rounds[455].capabilities_added[1] bad weak-path:corpus/SOURCES.md
row rounds[462].capabilities_added[0] bad weak-path:corpus/SOURCES.md
row rounds[476].capabilities_added[0] matched 
row rounds[476].capabilities_added[1] bad weak-path:corpus/SOURCES.md
row rounds[495].capabilities_added[0] bad weak-path:corpus/SOURCES.md
row rounds[495].capabilities_added[1] bad weak-path:corpus/SOURCES.md
label=P-C1 rev=f7750ba8d7f452493281db264241cf9f727f49cc manifest_rev=37b51a243302 register='## Capabilities (label-keyed control)' oracle=18 rows=18 matched=4 missing=0 bad=14 extra=0 mismatches=14 C1=unmet
```

Exit: `1`. Verdict: **unmet**.

### restored

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py 3d5c6173431cf188461a7a7abf1731a6f33edca5 --repo /fast/scratch/hyaku/mori-r35/CtlLabelKeyed/clone
```

Full stdout:

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
label=P-C1 rev=3d5c6173431cf188461a7a7abf1731a6f33edca5 manifest_rev=37b51a243302 register='## Capabilities (round 12 demonstrations)' oracle=18 rows=5 matched=0 missing=18 bad=0 extra=5 mismatches=23 C1=unmet
```

Exit: `1`. Verdict: **unmet**.

## Restoration evidence

The appended control section was removed in the scratch clone and committed as `3d5c6173431cf188461a7a7abf1731a6f33edca5`. The restored SCORECARD SHA-256 is byte-identical to pristine: `8fbc058a9f8c5dc42fd75314e95d4bd9a1172d3e250cb86570d81db270052b2a`. The hashline snapshot also returned to `#584F`. The same frozen detector ran on the restored committed bytes and reproduced the pristine counts (`rows=5 matched=0 missing=18 bad=0 extra=5 mismatches=23 C1=unmet`, exit 1). The before/after counter SHA-256 is unchanged, as recorded above.

Register: `.ufo/waves/round-35/c0/CtlLabelKeyed-register.md`

Report: `.ufo/waves/round-35/c0/CtlLabelKeyed.md`
