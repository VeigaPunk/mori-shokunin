# Control 8 — stale pointers (mori r35, pre-data control wave C0)

- **Control name:** `CtlStalePointer` (contract.md controls list, item 8: stale pointers).
- **What work it skips:** every closure lookup. The register has the correct 18 MANIFEST keys
  (`rounds[i].capabilities_added[j]`) and correct round cells, but each evidence cell cites a path
  that exists at the measured tip and (for 13 of 18 rows) appears in that closure's record text
  while **not** having changed in that closure's round — so it never verifies "the round landed
  this artifact". Five rows have no record-text stale path at all (every path the closure record
  names was changed in that round); for those the contract fallback applies: cite a path changed
  in a *different* round.
- **How built:** sandbox clone of the lane at the frozen tip, one appended register commit,
  scored read-only by the frozen counter.
- **Clone commit:** `4959715428bf7dae38ff62818dd5d39cd93c4bfe` (parent
  `f2d28711ee723c969b6c2008d32df498192f9e7b`, branch `ctl-stale`, one commit "ctl",
  `SCORECARD.md | 23 ++++`).
- **Counter sha256 run:** `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167`
  (frozen `count-c1.py`, `sha256sum` before and only use; contract sha256
  `94b7f90a352c96a0b8be17cef62f95647aad06fa84c83d4540751d888d65ba40` untouched).
- **Verdict:** **unmet — correct for a skip-the-work control** (all 18 rows `bad`, no row matched,
  `C1=unmet`).
- **Exit code:** `1`.

## Summary line (full, verbatim)

```
label=P-C1 rev=4959715428bf7dae38ff62818dd5d39cd93c4bfe manifest_rev=37b51a243302 register='## Capabilities (round 12–31 closures, stale-pointer control 8)' oracle=18 rows=18 matched=0 missing=0 bad=18 extra=0 mismatches=18 C1=unmet
```

## Full counter stdout

```
row rounds[313].capabilities_added[0] bad weak-path:tools/mori-silence-cases.sh
row rounds[339].capabilities_added[0] bad weak-path:corpus/evidence/baseline-r10-20261015T2231Z.json
row rounds[345].capabilities_added[0] bad weak-path:tools/mori-silence-cases.sh
row rounds[353].capabilities_added[0] bad weak-path:tools/mori-census.sh
row rounds[386].capabilities_added[0] bad weak-path:tools/mori-census.sh
row rounds[386].capabilities_added[1] bad weak-path:tools/mori-census.sh
row rounds[386].capabilities_added[2] bad weak-path:tools/mori-census.sh
row rounds[398].capabilities_added[0] bad weak-path:tools/mori-retention-gate.py
row rounds[427].capabilities_added[0] bad weak-path:corpus/knowledge/freeze-order-r18.md
row rounds[443].capabilities_added[0] bad weak-path:tools/mori-dispatch-ledger.py
row rounds[443].capabilities_added[1] bad weak-path:tools/mori-dispatch-ledger.py
row rounds[455].capabilities_added[0] bad weak-path:tools/mori-pressure.py
row rounds[455].capabilities_added[1] bad weak-path:tools/mori-pressure.py
row rounds[462].capabilities_added[0] bad weak-path:tools/mori-census.sh
row rounds[476].capabilities_added[0] bad weak-path:tools/mori-oom-killers.py
row rounds[476].capabilities_added[1] bad weak-path:tools/mori-oom-killers.py
row rounds[495].capabilities_added[0] bad weak-path:tools/mori-census.sh
row rounds[495].capabilities_added[1] bad weak-path:tools/mori-census.sh
label=P-C1 rev=4959715428bf7dae38ff62818dd5d39cd93c4bfe manifest_rev=37b51a243302 register='## Capabilities (round 12–31 closures, stale-pointer control 8)' oracle=18 rows=18 matched=0 missing=0 bad=18 extra=0 mismatches=18 C1=unmet
```

## Per-row path choice

Flags measured by importing the frozen counter's own oracle construction (same `git diff`, same
record text, same tip tree). "record-text" = whole-path occurrence in the closure's record text;
"stale" = absent from `diff(prev closure commit, closure commit)`; "changed in" = admitted mori
closures whose diff (prev closure → closure) did change the path.

| # | key (round) | cited path | record-text | stale in round | changed in | other arms |
|---|---|---|---|---|---|---|
| 1 | `rounds[313].capabilities_added[0]` (12) | `tools/mori-silence-cases.sh` | yes | yes | no admitted closure (pre-r12 artifact) | none — stale arm only |
| 2 | `rounds[339].capabilities_added[0]` (14) | `corpus/evidence/baseline-r10-20261015T2231Z.json` | yes | yes | no admitted closure (round-10 evidence) | none — stale arm only |
| 3 | `rounds[345].capabilities_added[0]` (15) | `tools/mori-silence-cases.sh` | yes | yes | none | none — stale arm only |
| 4 | `rounds[353].capabilities_added[0]` (16) | `tools/mori-census.sh` | **no** | yes | 12, 14, 15 | record-text arm also fails; **no record-text stale path exists** |
| 5 | `rounds[386].capabilities_added[0]` (18) | `tools/mori-census.sh` | **no** | yes | 12, 14, 15 | named arm (capability names `tools/mori-retention-gate.py`, changed r18); **no record-text stale path** |
| 6 | `rounds[386].capabilities_added[1]` (18) | `tools/mori-census.sh` | **no** | yes | 12, 14, 15 | named arm (`tools/mori-freeze-order.py`, changed r18); **no record-text stale path** |
| 7 | `rounds[386].capabilities_added[2]` (18) | `tools/mori-census.sh` | **no** | yes | 12, 14, 15 | named arm (`tools/mori-dispatch-ledger.py`, changed r18); **no record-text stale path** |
| 8 | `rounds[398].capabilities_added[0]` (19) | `tools/mori-retention-gate.py` | yes | yes | 18 | none — stale arm only |
| 9 | `rounds[427].capabilities_added[0]` (22) | `corpus/knowledge/freeze-order-r18.md` | yes | yes | 18, 19 | named arm (`tools/mori-retention-reconcile.py`, changed r22) |
| 10 | `rounds[443].capabilities_added[0]` (24) | `tools/mori-dispatch-ledger.py` | yes | yes | 18 | named arm (`tools/mori-pressure.py`, changed r24) |
| 11 | `rounds[443].capabilities_added[1]` (24) | `tools/mori-dispatch-ledger.py` | yes | yes | 18 | named arm (`tools/mori-routed-check.py`, changed r24) |
| 12 | `rounds[455].capabilities_added[0]` (25) | `tools/mori-pressure.py` | yes | yes | 24 | named arm (`tools/mori-job-runway.py`, changed r25) |
| 13 | `rounds[455].capabilities_added[1]` (25) | `tools/mori-pressure.py` | yes | yes | 24 | named arm (`tools/mori-routed-r24.py`, changed r25) |
| 14 | `rounds[462].capabilities_added[0]` (26) | `tools/mori-census.sh` | **no** | yes | 12, 14, 15 | named arm (`tools/mori-oom-killers.py`, changed r26); **no record-text stale path** |
| 15 | `rounds[476].capabilities_added[0]` (28) | `tools/mori-oom-killers.py` | yes | yes | 26 | none — stale arm only |
| 16 | `rounds[476].capabilities_added[1]` (28) | `tools/mori-oom-killers.py` | yes | yes | 26 | named set includes this path → named arm passes; stale arm only |
| 17 | `rounds[495].capabilities_added[0]` (31) | `tools/mori-census.sh` | yes | yes | 12, 14, 15 | named arm (`tools/mori-blind-check.sh`, changed r31) |
| 18 | `rounds[495].capabilities_added[1]` (31) | `tools/mori-census.sh` | yes | yes | 12, 14, 15 | named arm (`corpus/knowledge/watchdog-identity-r31.md`, changed r31) |

Notes on the fallback rows (4–7, 14):
- r16 record text names exactly 5 artifact paths (`corpus/SOURCES.md`,
  `corpus/knowledge/journal-cursor-window-r16.md`, `tools/mori-journal-window.py`,
  `tools/mori-round16-context-check.py`, `tools/mori-round16-regressions.py`); all changed in r16,
  so no record-text stale pointer exists. `corpus/SOURCES.md` additionally occurs only inside a
  longer path (not whole).
- r18 names 6 artifact paths, r26 names 6; all changed in their round (r18 and r26 respectively).
- For these 5 rows the contract fallback is used: a path that exists at the tip **and at the
  closure commit** but changed in a different round (`tools/mori-census.sh`, rounds 12/14/15).
- For rows 9–13, 17–18 the capability string names a tool/knowledge path that changed in its own
  round, so no named path can be a stale pointer; the stale arm is therefore measured with a
  different, record-text stale path and the named arm trips alongside. Rows 1–3, 8, 15–16 isolate
  the stale arm alone (`whole_in_ctext=true`, path in tip and closure commit, artifact prefix,
  named constraint empty or satisfied), so the counter's `changed-in-round` conjunct is exercised
  independently of the named-path conjunct.

## How built — exact commands

```bash
mkdir -p /fast/scratch/hyaku/mori-r35/MoriR35.CtlStalePointer
cd /fast/scratch/hyaku/mori-r35/MoriR35.CtlStalePointer
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git clone -q /home/vgpnk/Projects/shokunin/mori-shokunin clone
cd clone
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git checkout -q -b ctl-stale f2d28711ee723c969b6c2008d32df498192f9e7b
cd ..
python3 gen.py                      # builds the frozen counter's oracle, emits section.md
cd clone
cat ../section.md >> SCORECARD.md
env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE \
  git -c user.name=ctl -c user.email=ctl@local commit -qam ctl   # -> 4959715...
cd ..
timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py \
  4959715428bf7dae38ff62818dd5d39cd93c4bfe \
  --repo /fast/scratch/hyaku/mori-r35/MoriR35.CtlStalePointer/clone
# exit 1
```

`gen.py` imports the frozen counter read-only (`importlib` from
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py`, `__main__` not run)
and reproduces its oracle loop verbatim, then picks per row:

```python
import importlib.util, json, re, subprocess
spec = importlib.util.spec_from_file_location("countc1", CTL)
cc = importlib.util.module_from_spec(spec); spec.loader.exec_module(cc)
repo, fleet = ".../clone", "/home/vgpnk/Projects/shokunin"
tip = subprocess.run(["git","-C",repo,"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
m = json.loads(cc.git(fleet,"show",cc.MANIFEST_REV+":MANIFEST.json").stdout)
at_tip = cc.tree_paths(repo, tip); oracle = {}
prev = cc.git(repo,"rev-parse","--verify",cc.FIRST_PREV+"^{commit}").stdout.strip()
entries = [(i, r) for i, r in enumerate(m["rounds"]) if r.get("lane") == "mori"]
for i, r in entries:
    commit = cc.git(repo,"rev-parse","--verify",r["commit"].split("@",1)[1]+"^{commit}").stdout.strip()
    if r.get("admitted") is True and (r.get("capabilities_added") or []):
        changed = set(cc.git(repo,"diff","--name-only","--no-renames",prev,commit).stdout.splitlines())
        vtext = json.dumps(r.get("verification") or {}, ensure_ascii=False)
        extra = [cc.show(repo,h,p) for p,h in cc.SPOT_RE.findall(vtext)]
        extra = [c for c in extra if c is not None]
        rp = cc.git(fleet,"show","%s:%s" % (cc.MANIFEST_REV, r.get("report")), check=False)
        if r.get("report") and rp.returncode == 0: extra.append(rp.stdout)
        ctext = vtext + "\n" + "\n".join(extra) + "\n" + "\n".join(r["capabilities_added"])
        for j, cap in enumerate(r["capabilities_added"]):
            oracle["rounds[%d].capabilities_added[%d]" % (i,j)] = dict(
                round=r["round"], changed=changed, ctext=ctext,
                at_commit=cc.tree_paths(repo, commit), named=set(cc.NAMED_RE.findall(cap)))
    prev = commit
CAND = re.compile(r"(?:tools/|corpus/knowledge/|corpus/evidence/)[A-Za-z0-9_./-]*[A-Za-z0-9_]|corpus/SOURCES\.md")
for key, o in oracle.items():
    ok = lambda p: p in at_tip and (p.startswith(cc.ARTIFACT_PREFIXES) or p in cc.ARTIFACT_FILES)
    cands = sorted({p for p in CAND.findall(o["ctext"])
                    if ok(p) and cc.whole_path_in(p, o["ctext"]) and p not in o["changed"]})
    if cands:
        pick = cands[0]                      # record-text stale pointer
    else:                                    # contract fallback: changed in another round
        pick = sorted(p for p in o["at_commit"] if ok(p) and p not in o["changed"])[0]
    # row: | `key` | capability | ... | `pick` | round |
```

(The real `gen.py` additionally ranks candidates: at-commit first, `tools/` first, non-named first,
deterministic tie-break. No file outside `/fast/scratch/hyaku/mori-r35/MoriR35.CtlStalePointer/`
and the two `c0/` deliverables was written; the frozen counter/contract were read-only;
`GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset for every clone git call.)

## Reading

- A skip-the-work control that builds the *correct* key/round skeleton and only fakes the evidence
  binding is caught: `matched=0`, `bad=18`, `C1=unmet`, exit 1. The stale-pointer arm has a live
  lower bound (rows 1–3, 8, 15–16 fail on that conjunct alone) and no skip program printed
  `C1=met`.
- Caveat recorded for the L1, not softening: for 7 rows (9–13, 17–18) the named-path conjunct also
  trips because the path the capability names is by construction changed in its own round; those
  rows cannot isolate the stale arm. For 5 rows (4–7, 14) no record-text stale path exists and the
  contract's "changed in a different round" fallback is used, so those rows additionally fail the
  record-text conjunct. The control remains a valid skip-the-work probe: nothing here binds a
  capability to the artifact its closure landed.
