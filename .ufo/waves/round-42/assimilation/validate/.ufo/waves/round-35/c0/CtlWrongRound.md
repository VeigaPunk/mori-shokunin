# CtlWrongRound — control 5: all-false round cells

Probe axes: round discrimination, positive reachability, byte-exact restoration.

## Mutant and expected detector

The wrong-round control retains all 18 admitted MANIFEST keys, capability strings and one strong evidence path per key, but sets every first-working-round cell to the actual closure round + 1. It skips truthful round binding, not the evidence lookup. The frozen P-C1 counter should reject every row solely for `round=actual+1!=actual`, giving `bad=18`, `C1=unmet`, exit 1. The positive form has the identical register with correct round cells: it does the claimed binding work and is **positive, not a skip**; expected `matched=18`, `C1=met`, exit 0.

Observed: **wrong-round unmet; mutant killed**. Both pristine and restored positive forms are **met**. No baseline failure; no evidence-path errors; no surviving skip in this assigned probe.

- Frozen lane base: `f2d28711ee723c969b6c2008d32df498192f9e7b`.
- Frozen fleet MANIFEST: `37b51a243302e8009c7067431e8a47f9a722fd14`.
- Isolated clone: `/fast/scratch/hyaku/mori-r35/CtlWrongRound/clone`, branch `ctl-wrong-round`.
- Counter run: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py`.
- Counter SHA-256 before, during and after: `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` (actual `sha256sum`; never modified or copied for mutation).
- Wrong-round clone commit: `c12964b13d5b6d14aec39aebc120da2d190c5a5d`.
- Pristine positive clone commit: `d6f222cc3114d6da205edbd1f6cd71f7feca66fd`.
- Restored positive clone commit: `7f870fe4b8d9c3523d0e409311939725c58379f1`.
- Wrong-round section: 22 lines; preserved in `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/c0/CtlWrongRound-register.md`.

## Build

Commands executed (all writes by git were confined to the sandbox):

```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE mkdir -p /fast/scratch/hyaku/mori-r35/CtlWrongRound
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone -q /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r35/CtlWrongRound/clone
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r35/CtlWrongRound/clone checkout -qb ctl-wrong-round f2d28711ee723c969b6c2008d32df498192f9e7b
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE PYTHONDONTWRITEBYTECODE=1 python3 /fast/scratch/hyaku/mori-r35/CtlWrongRound/make-register.py
```

The following 55-line generator was written at that scratch path and executed once. It imports the frozen counter read-only, suppresses bytecode writes, reproduces the oracle's previous-mori-closure tracking and closure text, and chooses the first lexicographic artifact satisfying **every** strong-path condition, including tip/closure existence, round change, artifact class, named-path equality and whole-path record occurrence. It emits both sections without modifying any repository.

```python
import importlib.util
import json
import sys
sys.dont_write_bytecode = True
SOURCE = '/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py'
REPO = '/fast/scratch/hyaku/mori-r35/CtlWrongRound/clone'
FLEET = '/home/vgpnk/Projects/shokunin'
BASE = 'f2d28711ee723c969b6c2008d32df498192f9e7b'
spec = importlib.util.spec_from_file_location('frozen_counter', SOURCE)
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
manifest = json.loads(c.git(FLEET, 'show', c.MANIFEST_REV + ':MANIFEST.json').stdout)
entries = [(i, r) for i, r in enumerate(manifest['rounds']) if r.get('lane') == 'mori']
prev = c.git(REPO, 'rev-parse', '--verify', c.FIRST_PREV + '^{commit}').stdout.strip()
at_rev = c.tree_paths(REPO, BASE)
rows = []
for i, r in entries:
    commit = c.git(REPO, 'rev-parse', '--verify', r['commit'].split('@', 1)[1] + '^{commit}').stdout.strip()
    caps = r.get('capabilities_added') or []
    if r.get('admitted') is True and caps:
        changed = set(c.git(REPO, 'diff', '--name-only', '--no-renames', prev, commit).stdout.splitlines())
        vtext = json.dumps(r.get('verification') or {}, ensure_ascii=False)
        records = []
        for p, h in c.SPOT_RE.findall(vtext):
            text = c.show(REPO, h, p)
            if text is not None:
                records.append(text)
        if r.get('report'):
            report = c.git(FLEET, 'show', c.MANIFEST_REV + ':' + r['report'], check=False)
            if report.returncode == 0:
                records.append(report.stdout)
        closure_text = vtext + '\n' + '\n'.join(records) + '\n' + '\n'.join(caps)
        at_commit = c.tree_paths(REPO, commit)
        for j, cap in enumerate(caps):
            named = set(c.NAMED_RE.findall(cap))
            candidates = sorted(p for p in changed & at_commit & at_rev
                                if (p.startswith(c.ARTIFACT_PREFIXES) or p in c.ARTIFACT_FILES)
                                and (not named or p in named) and c.whole_path_in(p, closure_text))
            assert candidates, (i, j, cap)
            rows.append((f'rounds[{i}].capabilities_added[{j}]', cap, candidates[0], int(r['round'])))
    prev = commit
assert len(rows) == 18
header = '## Capabilities (C0 round-cell control)\n\n'
header += '| Key | Capability | What it can now do | Evidence | First-working round |\n'
header += '| --- | --- | --- | --- | --- |\n'
for offset, label in ((0, 'positive'), (1, 'wrong-round')):
    lines = [header.rstrip('\n')]
    for key, cap, path, rnd in rows:
        cap = cap.replace('|', ' / ').replace('\n', ' ')
        lines.append(f'| `{key}` | {cap} | As recorded in the closure capability entry. | `{path}` | {rnd + offset} |')
    register = '\n'.join(lines) + '\n'
    assert len(register.splitlines()) <= 200
    print('BEGIN ' + label)
    print(register, end='')
    print('END ' + label)
```

Using the surgical edit tool, appended the emitted positive section after the frozen SCORECARD bytes (one separating blank line), then committed pristine. Replaced only the 18 fifth-cell round values with the emitted wrong-round values and committed the mutant. After scoring it, restored those same cells to their positive values and committed the restoration. The wrong-round saved section contains only the heading/table, not the `BEGIN`/`END` display markers. No evidence, key, capability prose, heading or other SCORECARD byte changed between the three measured forms.

```sh
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r35/CtlWrongRound/clone -c user.name=ctl -c user.email=ctl@local commit -qam ctl-positive-pristine
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r35/CtlWrongRound/clone -c user.name=ctl -c user.email=ctl@local commit -qam ctl-wrong-round
timeout 120 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /fast/scratch/hyaku/mori-r35/CtlWrongRound/clone -c user.name=ctl -c user.email=ctl@local commit -qam ctl-positive-restored
```

## Behavioral detector: actual stdout and exit codes

All three detector subprocesses used the same command shape, sanitized environment (GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE absent), `timeout 120`, and an outer subprocess timeout of 130 seconds. All completed normally; stderr was empty for all three.

### Pristine positive — met; positive, not a skip

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py d6f222cc3114d6da205edbd1f6cd71f7feca66fd --repo /fast/scratch/hyaku/mori-r35/CtlWrongRound/clone
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
label=P-C1 rev=d6f222cc3114d6da205edbd1f6cd71f7feca66fd manifest_rev=37b51a243302 register='## Capabilities (C0 round-cell control)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```

Exit code: 0. Verdict: **met (positive)**.

### Wrong-round control — unmet; mutant killed

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py c12964b13d5b6d14aec39aebc120da2d190c5a5d --repo /fast/scratch/hyaku/mori-r35/CtlWrongRound/clone
```

```text
row rounds[313].capabilities_added[0] bad round=13!=12
row rounds[339].capabilities_added[0] bad round=15!=14
row rounds[345].capabilities_added[0] bad round=16!=15
row rounds[353].capabilities_added[0] bad round=17!=16
row rounds[386].capabilities_added[0] bad round=19!=18
row rounds[386].capabilities_added[1] bad round=19!=18
row rounds[386].capabilities_added[2] bad round=19!=18
row rounds[398].capabilities_added[0] bad round=20!=19
row rounds[427].capabilities_added[0] bad round=23!=22
row rounds[443].capabilities_added[0] bad round=25!=24
row rounds[443].capabilities_added[1] bad round=25!=24
row rounds[455].capabilities_added[0] bad round=26!=25
row rounds[455].capabilities_added[1] bad round=26!=25
row rounds[462].capabilities_added[0] bad round=27!=26
row rounds[476].capabilities_added[0] bad round=29!=28
row rounds[476].capabilities_added[1] bad round=29!=28
row rounds[495].capabilities_added[0] bad round=32!=31
row rounds[495].capabilities_added[1] bad round=32!=31
label=P-C1 rev=c12964b13d5b6d14aec39aebc120da2d190c5a5d manifest_rev=37b51a243302 register='## Capabilities (C0 round-cell control)' oracle=18 rows=18 matched=0 missing=0 bad=18 extra=0 mismatches=18 C1=unmet
```

Exit code: 1. Verdict: **unmet**. Mutation verdict: **killed**; all 18 row failures are round mismatches only.

### Restored positive — met; positive, not a skip

```sh
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py 7f870fe4b8d9c3523d0e409311939725c58379f1 --repo /fast/scratch/hyaku/mori-r35/CtlWrongRound/clone
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
label=P-C1 rev=7f870fe4b8d9c3523d0e409311939725c58379f1 manifest_rev=37b51a243302 register='## Capabilities (C0 round-cell control)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```

Exit code: 0. Verdict: **met (positive)**, as expected after restoration; not a skip finding.

## Restoration evidence

Actual SHA-256 hashes of `/fast/scratch/hyaku/mori-r35/CtlWrongRound/clone/SCORECARD.md`:

| State | SHA-256 |
| --- | --- |
| Frozen checkout before adding controls | `8fbc058a9f8c5dc42fd75314e95d4bd9a1172d3e250cb86570d81db270052b2a` |
| Pristine positive (mutation baseline) | `70ce0b1a549f2352c2a12ed882abfd85240488757c4be3ee97bc70f232f5c297` |
| Wrong-round mutant | `8588a87a919222d3ba5d82a736aa5809b97b3039e4a10a1c18c7b7c49eaad3d3` |
| Restored positive | `70ce0b1a549f2352c2a12ed882abfd85240488757c4be3ee97bc70f232f5c297` |

The restored SCORECARD hash equals the pristine positive mutation baseline exactly; the restored detector also returned the same counts and exit code. The frozen counter hash stayed unchanged. Saved wrong-round register SHA-256: `f95a373d5fbfdad177fd166a231aab9c7607e10fa50f5aa218133f638501cc71`.

The only lane-repo writes for this probe are this report and `CtlWrongRound-register.md`; no lane/fleet git writes, MANIFEST/state edits, background jobs, installs, updates or other-runtime invocations were made. Tool installs/updates: none. All started detector/generator/git commands completed before this report.
