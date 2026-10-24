# Control 9 — dangling pointers (C0, mori round 35)

- **Control name:** `CtlDangling` — control-list item 9, "dangling: correct keys and rounds, evidence paths that
  do not exist at the tip". Three variants as assigned (A, B, C) plus one format probe (D, allowed by item 10).
- **What work it skips:** the register's evidence lookup. Every row carries a correct MANIFEST key and the correct
  closure round (the cheap half), while the cited artifact is not a resolvable pointer — so the claim "each row
  binds the capability to an artifact the closure landed and names" is not done.
- **Sandbox:** `/fast/scratch/hyaku/mori-r35/CtlDangling/clone`, clone of `/home/vgpnk/Projects/shokunin/mori-shokunin`
  at base `f2d28711ee723c969b6c2008d32df498192f9e7b` on branch `ctl-dangling`. Writes: clone-local git commits only;
  no git in the lane or fleet repo; no installs or updates (nothing installed).
- **Counter run:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py`
  — sha256 `27b82d71f2f591df1833c8de793201475d8f01735b5ed4edd7b74e389ee18167` (frozen, unmodified; only a
  byte-identical read-only copy at `/fast/scratch/hyaku/mori-r35/CtlDangling/counter_copy.py` was imported by the
  oracle probe for its helper functions — never used to score).
- **Oracle:** 18 keys, rounds 12,14,15,16,18×3,19,22,24×2,25×2,26,28×2,31×2, derived by `probe.py` (replicates
  `main()`'s oracle construction over MANIFEST `37b51a2`); strong-path lists cross-checked by the counter output
  below (`missing=0 extra=0` in every variant).

## How built

```
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE
mkdir -p /fast/scratch/hyaku/mori-r35/CtlDangling
git clone -q /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r35/CtlDangling/clone
git -C /fast/scratch/hyaku/mori-r35/CtlDangling/clone checkout -q -b ctl-dangling f2d28711ee723c969b6c2008d32df498192f9e7b
cd /fast/scratch/hyaku/mori-r35/CtlDangling
python3 probe.py > oracle.json            # read-only oracle dump (keys, rounds, strong paths, no deleted-at-tip path)
python3 build.py A && python3 build.py B && python3 build.py C && python3 build.py D
for V in A B C D; do
  REV=$(awk '{print $2}' rev$V.txt)
  timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-35/count-c1.py \
    "$REV" --repo /fast/scratch/hyaku/mori-r35/CtlDangling/clone > score$V.txt 2>&1
  echo "$V exit=$?"
done
```

`build.py` (63 lines, appended verbatim below; each run appends one `## Capabilities register (round 35 C1
control: …)` section and commits it; the counter reads the last such section):

```python
#!/usr/bin/env python3
"""Build control-9 (dangling) register variants into the sandbox clone and commit each."""
import json
import subprocess
import sys

CLONE = "/fast/scratch/hyaku/mori-r35/CtlDangling/clone"
SC = CLONE + "/SCORECARD.md"
oracle = json.load(open("/fast/scratch/hyaku/mori-r35/CtlDangling/oracle.json"))["oracle"]


def cell(s):
    return s.replace("|", "/").replace("\n", " ").strip()


def section(title, ev):
    out = ["## Capabilities register (round 35 C1 control: %s)" % title, "",
           "| Key | Capability | What it can now do | Evidence | First-working round |",
           "|---|---|---|---|---|"]
    for i, (k, o) in enumerate(oracle.items()):
        evs = ev(i, k, o)
        out.append("| `%s` | %s | bound to closure record | %s | %s |"
                   % (k, cell(o["cap"]), evs, o["round"]))
    return "\n".join(out) + "\n"


def ev_a(i, k, o):
    return "`.ufo/waves/round-34/w1/cap-%02d.md`" % i


def ev_b(i, k, o):
    return "`%s:99999`" % o["strong"][0]


def ev_c(i, k, o):
    return "`%s` `.ufo/waves/round-34/w1/aux-%02d.md`" % (o["strong"][0], i)


def ev_d(i, k, o):
    return "`%s` .ufo/waves/round-34/w1/notes-%02d.md" % (o["strong"][0], i)


def commit(tag, title, ev):
    with open(SC, "a", encoding="utf-8") as f:
        f.write("\n" + section(title, ev))
    subprocess.run(["git", "-C", CLONE, "-c", "user.name=ctl", "-c", "user.email=ctl@local",
                    "commit", "-qam", tag], check=True)
    rev = subprocess.run(["git", "-C", CLONE, "rev-parse", "HEAD"], capture_output=True,
                         text=True, check=True).stdout.strip()
    print("%s %s" % (tag, rev))
    return rev


if __name__ == "__main__":
    which = sys.argv[1]
    print(commit(which, {"A": "dangling paths absent at tip",
                         "B": "strong paths, line range past EOF",
                         "C": "one strong path plus one dangling path", "D": "strong path plus unbackticked dangling prose"}[which],
                 {"A": ev_a, "B": ev_b, "C": ev_c, "D": ev_d}[which]))
```

Register bytes (all four appended sections, 91 lines, 72 rows): `c0/CtlDangling-register.md`.
No strong path that changed in a closure round is missing at the tip in this clone (`deleted=0` for all 18
oracle rows), so variant A's dangling paths are the round-34 `w1/` style named by the item.

## Variant A — evidence paths absent at the tip

Commit `bc746cdc207fd8c2313458100733f337a02c860d`.
Command: `timeout 120 python3 …/count-c1.py bc746cdc207fd8c2313458100733f337a02c860d --repo /fast/scratch/hyaku/mori-r35/CtlDangling/clone`

```
row rounds[313].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/cap-00.md
row rounds[339].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/cap-01.md
row rounds[345].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/cap-02.md
row rounds[353].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/cap-03.md
row rounds[386].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/cap-04.md
row rounds[386].capabilities_added[1] bad absent-at-rev:.ufo/waves/round-34/w1/cap-05.md
row rounds[386].capabilities_added[2] bad absent-at-rev:.ufo/waves/round-34/w1/cap-06.md
row rounds[398].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/cap-07.md
row rounds[427].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/cap-08.md
row rounds[443].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/cap-09.md
row rounds[443].capabilities_added[1] bad absent-at-rev:.ufo/waves/round-34/w1/cap-10.md
row rounds[455].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/cap-11.md
row rounds[455].capabilities_added[1] bad absent-at-rev:.ufo/waves/round-34/w1/cap-12.md
row rounds[462].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/cap-13.md
row rounds[476].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/cap-14.md
row rounds[476].capabilities_added[1] bad absent-at-rev:.ufo/waves/round-34/w1/cap-15.md
row rounds[495].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/cap-16.md
row rounds[495].capabilities_added[1] bad absent-at-rev:.ufo/waves/round-34/w1/cap-17.md
label=P-C1 rev=bc746cdc207fd8c2313458100733f337a02c860d manifest_rev=37b51a243302 register='## Capabilities register (round 35 C1 control: dangling paths absent at tip)' oracle=18 rows=18 matched=0 missing=0 bad=18 extra=0 mismatches=18 C1=unmet
```

**Exit 1. Verdict: unmet.** Correct keys and rounds are fully credited (`missing=0 extra=0`); every row is `bad`
on `absent-at-rev`, so the evidence arm holds.

## Variant B — correct strong paths, line range past EOF

Commit `8942fce095919181f302055aaea9669785377166`. Each row cites its first strong artifact with `:99999`
(inside the file only if the file had ≥99999 lines; every cited file has fewer).

```
row rounds[313].capabilities_added[0] bad line-out-of-range:corpus/SOURCES.md:99999
row rounds[339].capabilities_added[0] bad line-out-of-range:corpus/SOURCES.md:99999
row rounds[345].capabilities_added[0] bad line-out-of-range:corpus/SOURCES.md:99999
row rounds[353].capabilities_added[0] bad line-out-of-range:corpus/knowledge/journal-cursor-window-r16.md:99999
row rounds[386].capabilities_added[0] bad line-out-of-range:tools/mori-retention-gate.py:99999
row rounds[386].capabilities_added[1] bad line-out-of-range:tools/mori-freeze-order.py:99999
row rounds[386].capabilities_added[2] bad line-out-of-range:tools/mori-dispatch-ledger.py:99999
row rounds[398].capabilities_added[0] bad line-out-of-range:tools/mori-content-review.py:99999
row rounds[427].capabilities_added[0] bad line-out-of-range:tools/mori-retention-reconcile.py:99999
row rounds[443].capabilities_added[0] bad line-out-of-range:tools/mori-pressure.py:99999
row rounds[443].capabilities_added[1] bad line-out-of-range:tools/mori-routed-check.py:99999
row rounds[455].capabilities_added[0] bad line-out-of-range:tools/mori-job-runway.py:99999
row rounds[455].capabilities_added[1] bad line-out-of-range:tools/mori-routed-r24.py:99999
row rounds[462].capabilities_added[0] bad line-out-of-range:tools/mori-oom-killers.py:99999
row rounds[476].capabilities_added[0] bad line-out-of-range:corpus/SOURCES.md:99999
row rounds[476].capabilities_added[1] bad line-out-of-range:tools/fixtures/mori-oom-killers/cases-a2.json:99999
row rounds[495].capabilities_added[0] bad line-out-of-range:tools/mori-blind-check.sh:99999
row rounds[495].capabilities_added[1] bad line-out-of-range:corpus/knowledge/watchdog-identity-r31.md:99999
label=P-C1 rev=8942fce095919181f302055aaea9669785377166 manifest_rev=37b51a243302 register='## Capabilities register (round 35 C1 control: strong paths, line range past EOF)' oracle=18 rows=18 matched=0 missing=0 bad=18 extra=0 mismatches=18 C1=unmet
```

**Exit 1. Verdict: unmet.** The line-range arm is inside the loop and `continue`s, so an out-of-range pointer is
never credited as evidence (`matched=0` despite the paths being genuinely strong).

## Variant C — one strong path plus one nonexistent path

Commit `d17ceaba904abfac3fe15606d9942fb1267dc931`. Each row cites its first strong artifact and a round-34
`w1/` path; the strong co-cited path passes every strength arm (no `weak-path` is printed), the dangling one fails.

```
row rounds[313].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/aux-00.md
row rounds[339].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/aux-01.md
row rounds[345].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/aux-02.md
row rounds[353].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/aux-03.md
row rounds[386].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/aux-04.md
row rounds[386].capabilities_added[1] bad absent-at-rev:.ufo/waves/round-34/w1/aux-05.md
row rounds[386].capabilities_added[2] bad absent-at-rev:.ufo/waves/round-34/w1/aux-06.md
row rounds[398].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/aux-07.md
row rounds[427].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/aux-08.md
row rounds[443].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/aux-09.md
row rounds[443].capabilities_added[1] bad absent-at-rev:.ufo/waves/round-34/w1/aux-10.md
row rounds[455].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/aux-11.md
row rounds[455].capabilities_added[1] bad absent-at-rev:.ufo/waves/round-34/w1/aux-12.md
row rounds[462].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/aux-13.md
row rounds[476].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/aux-14.md
row rounds[476].capabilities_added[1] bad absent-at-rev:.ufo/waves/round-34/w1/aux-15.md
row rounds[495].capabilities_added[0] bad absent-at-rev:.ufo/waves/round-34/w1/aux-16.md
row rounds[495].capabilities_added[1] bad absent-at-rev:.ufo/waves/round-34/w1/aux-17.md
label=P-C1 rev=d17ceaba904abfac3fe15606d9942fb1267dc931 manifest_rev=37b51a243302 register='## Capabilities register (round 35 C1 control: one strong path plus one dangling path)' oracle=18 rows=18 matched=0 missing=0 bad=18 extra=0 mismatches=18 C1=unmet
```

**Exit 1. Verdict: unmet.** A single dangling citation condemns an otherwise-strong row: `bad=18`.

## Variant D — extra format probe (control item 10): strong path plus unbackticked dangling prose

Commit `813f18d47c805e09ade1d6f603925128ddffc495`. Same strong artifact per row, backticked, plus a nonexistent
round-34 `w1/` path written **without** backticks inside the same evidence cell.

```
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
label=P-C1 rev=813f18d47c805e09ade1d6f603925128ddffc495 manifest_rev=37b51a243302 register='## Capabilities register (round 35 C1 control: strong path plus unbackticked dangling prose)' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
```

Raw row lines end with a trailing space (`row … matched `); that whitespace is not reproduced above — the
summary line is byte-exact, every row line is byte-exact modulo its trailing space.

**Exit 0. Verdict: met.** Stated plainly: a register whose every evidence cell contains a nonexistent path
prints `C1=met`. The mechanism is exact: `TICK_RE` counts only backticked tokens, so the dangling plaintext is
not an evidence citation under the frozen row shape ("evidence paths in backticks") and only the strong
backticked path is scored. This row set does the claimed binding work — one real path per row, changed in that
closure's round, under an artifact prefix, named by the capability string where one is named, and present as a
whole path in that closure's record — so it is a positive-control-plus-litter, **not** a skip-the-work control,
and it does not by itself force amendment A1 under the contract's classification. It is a scope limit worth the
L1's attention: if a plaintext nonexistent path in the evidence cell is to count as a dangling citation, the
counter needs a plaintext path scan (A1 amendment); as frozen, it is correctly treated as prose.

## Risks / blockers

- No blocker. All scoring used the frozen counter at sha256 `27b82d71…`; no counter or contract edit; no git
  write outside `/fast/scratch/hyaku/mori-r35/CtlDangling/clone`; no install/update performed.
- The sandbox clone is a full local clone at base `f2d28711`; its history includes the closure commits the
  oracle reads (`missing=0 extra=0` confirms all 18 keys resolved).
- Residual: variant D shows the evidence cell's citation scope is backtick-only. Contract item 10 invites
  further designs; a genuine skip program that reaches `met` was not found — every `met` path requires a
  strong per-row artifact, i.e. the evidence lookup the claim is about.
