# ScoutWaveSpec — w1-spec distinctness

Attack: `.ufo/waves/round-37/w1-spec.json` item distinctness and padding (73 items). No tools installed.

## Measurement

```
python3 - <<'PY'
import json, re, difflib
from collections import defaultdict
from pathlib import Path
p = Path("/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-37/w1-spec.json")
data = json.loads(p.read_text())
def sections(prompt):
    m = re.search(r"# Target\n(.*)\n# Acceptance\n(.*)\Z", prompt, re.S)
    return m.group(1).strip(), m.group(2).strip()
rows = [(it["name"], *sections(it["prompt"])) for it in data["items"]]
print("n", len(rows), "unique names", len({n for n,_,_ in rows}))
by = defaultdict(list)
for n,t,a in rows:
    by[(t,a)].append(n)
print("exact target+acceptance collisions", [v for v in by.values() if len(v)>1])
acc = defaultdict(list)
for n,t,a in rows:
    acc[a].append(n)
print("exact acceptance collisions", [(v, a) for a,v in acc.items() if len(v)>1])
prompts = {it["name"]: it["prompt"] for it in data["items"]}
for x,y in [("ExecC1Seed41","ExecC1Seed42"),("ExecC1Seed41","ExecC1Seed43")]:
    ch = [ln for ln in difflib.ndiff(prompts[x].splitlines(), prompts[y].splitlines())
          if ln.startswith(("+ ","- "))]
    print(x, y, "diff lines", len(ch))
    for ln in ch:
        print(ln[-90:])
PY
```

Observed:

- `n 73`, `unique names 73`
- exact `(target, acceptance)` string collisions: `[]`
- exact acceptance collisions: only `ExecC1Seed41`, `ExecC1Seed42`, `ExecC1Seed43`, all `Paste the full output and exit code. VERDICT: PASS iff C1=met and exit 0.`
- `ExecC1Seed41` vs `42` and vs `43`: one changed line each, the `--seed` integer (`41` / `42` / `43`). Nothing else in the prompt differs.

Normalized (`--seed <int>` → `--seed N`) those three targets are identical:

`cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed N; echo EXIT=$?`

## Duplicates / filler

**ExecC1Seed41, ExecC1Seed42, ExecC1Seed43** (`w1-spec.json:128-140`, prompts on lines 130, 135, 140) share one target and one acceptance. The acceptance text is byte-identical and does not mention the seed. The target is the same command at the same rev; the only token that changes is `--seed`. That is one measurement copied three times, not three pieces of work.

They are also the body of **RevC1Predicate** (`w1-spec.json:8-10`), whose target is `for s in 41 42 43; do python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6 --seed $s`. RevC1Predicate does **not** share the acceptance: it also requires the first printed line to be byte-identical to P-C1 in `contract.md`. The three executor items add no acceptance the reviewer item does not already cover, and they drop the predicate-byte check.

## Overlaps that do not share a target and an acceptance

Checked and not counted as duplicates (different question or different artifact; role layering on one claim is not a renamed copy):

- RevC2Docs (`:28-30`) vs ExecLessonGate (`:228-230`): both touch S221–S225 copies, but anchors differ. Lesson Gate cites the short quotes (`corpus/lessons/round-37.md:9-13`, e.g. S221 `7230-7234`). SOURCES rows cite wider anchors (`corpus/SOURCES.md:227-231`, e.g. S221 `7230-7252`) plus a teaches sentence. Acceptances differ (teaches-sentence support vs contiguous and ≤25 words).
- ExecLessonGate vs ScribeLesson (`:248-250`): Gate contiguity/word-count vs Gate-plus-Mistakes evidence resolution.
- ScoutSentData (`:268-270`) vs SentData (`:348-350`): both scan for operator paths and credentials. Scout names `.ufo/waves/round-37/evidence/` and `corpus/evidence/sources-r37/` and passes on no `/home/vgpnk` and no credentials. Sent covers committed evidence, adds lane-external paths and private-data, and passes on no secrets and no absolute operator paths.
- RevR17JJ (`:38-40`) vs ExecR17JJBattery (`:163-165`): same selftest binary, different scratch (`scratch-rev` vs `scratch-exec`). Rev requires a mutant that moves `XDG_CONFIG_HOME` to fail; Exec only requires exit 0 and `jj_config_redirected` in the ok list.
- RevScratch (`:48-50`) vs LabC1Concurrent (`:113-115`): both run concurrent `count-c1` at seed 11. Rev also requires repo-relative paths and `_scratch_parent` / `mkdtemp` inspection; Lab repeats the race three times and does not check paths.
- RevTimeout (`:43-45`) vs LabTimeoutBoundary (`:118-120`): one 300s sleep vs sleeps at `TOOL_TIMEOUT_S±5`.
- CritDebtDisposition (`:83-85`) vs RevDebtR36 (`:338-340`) vs ScoutPriorRound (`:288-290`): disposition tables over different source pairs (r37 contract+lesson, r36 residuals+contract, r36 spotcheck+lesson).
- ExecSourceCensus (`:183-185`) vs ScoutCorpusCensus (`:293-295`): shared row-count and duplicate-id check; Exec adds malformed/enum, Scout adds tier histogram, `used-by` resolution, and a 225-row pass.
- MutC2RedirectArm (`:103-105`, "Same as MutC2CapArm") and SimpC2 (`:363-365`, "Same for …"): same sentence shape, different arm/file (`redirect_kill` vs `cap_kill`; `count-c1.py` vs `mori-source-drift.py` + `count-c2.py`).
- ExecGateRegistry (`:223-225`) vs ScribeSkill (`:253-255`): name missing SKILL.md rows vs draft those rows. Different acceptance.

No other normalized target collision and no other exact acceptance collision.

VERDICT: FAIL