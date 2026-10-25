# PlanDataWalk — round-45 bounded planning data walk (C2 population sizing)

Seat: `L1Mori45.PlanDataWalk`. Read-only. Lane =
`/home/vgpnk/Projects/shokunin/mori-shokunin`.
Measured at the contract's frozen revision `554ff416`; every `SKILL.md` line number below is
valid at that revision, at `HEAD` and in the worktree (proof in §0).
Tools installed: **none** (nothing was needed; no `pacman`, no `uv`, no downloads).
Scratch: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/PlanDataWalk`
(created by me; `TMPDIR` pointed there for every run).

---

## §0 Revision and byte identity of the audited surface

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && git rev-parse HEAD
3ad8faaa637ae466c61f9427fea1c208bf49ea82
$ echo "blob@554ff416: $(git rev-parse 554ff416:SKILL.md)"; echo "blob@HEAD: $(git rev-parse HEAD:SKILL.md)"
blob@554ff416: e2f1550ab5663156555541a34ca3c2d2fd11d686
blob@HEAD:     e2f1550ab5663156555541a34ca3c2d2fd11d686
$ git diff --stat 554ff416 -- SKILL.md    ;  diff_rc=0        # empty diff
$ git merge-base --is-ancestor 554ff416 HEAD && echo "554ff416 is ancestor of HEAD"
554ff416 is ancestor of HEAD
$ git log --oneline 554ff416..HEAD
3ad8faaa round-45: frozen contract, wave-1 spec and dispatch, opened sources
b1d7269f round-44 verifier spot-check (integrator, hyaku): non-author admit/reject
$ git status --porcelain
?? .ufo/waves/round-45/assimilation/quarantine-slice
?? .ufo/waves/round-45/evidence/
?? .ufo/waves/round-45/tmp/
?? .ufo/waves/round-45/w1/
```

`SKILL.md` is byte-identical in all three places (same blob `e2f1550a…`, working tree clean for
that path), so line numbers measured here apply to `--rev 554ff416`, `--rev HEAD` and `WORK`.

At the moment of this walk, `tools/` was unmodified relative to `554ff416` in the worktree (the
`git status --porcelain` above lists only untracked round-45 paths). Sibling executors have begun
editing the worktree since then — later `git status` shows ` M tools/mori-gate-registry.py`,
` M tools/mori-round19-regressions.py`, ` M tools/mori-routed-check.py` — which is peer work I did
not touch and which does not affect a single number below: every measurement here reads git
objects at `--rev 554ff416` (`git ls-tree`, `git show`) or the byte-identical `SKILL.md`, never a
modified tool body. The `--selftest` runs in §2/§3 and the `tools/mori-gate-registry.py`
invocations in §4b/§5 were executed against the worktree copies while they were still byte-equal
to `554ff416`.

---

## §1 The C2 population and the total N

### 1a. `tools/` at the frozen revision

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree --name-only 554ff416 tools/
tools/fixtures
tools/mori-blind-check.sh
tools/mori-census.sh
tools/mori-content-review.py
tools/mori-disk-rate.py
tools/mori-dispatch-ledger.py
tools/mori-evidence-loss.py
tools/mori-freeze-order.py
tools/mori-gate-registry.py
tools/mori-index-clean.sh
tools/mori-job-runway.py
tools/mori-journal-window.py
tools/mori-misroot-sweep.py
tools/mori-oom-killers.py
tools/mori-pressure.py
tools/mori-retention-gate.py
tools/mori-retention-reconcile.py
tools/mori-round13-regressions.py
tools/mori-round14-regressions.py
tools/mori-round15-regressions.py
tools/mori-round16-context-check.py
tools/mori-round16-regressions.py
tools/mori-round17-context-check.py
tools/mori-round17-jj-regressions.py
tools/mori-round17-seat-regressions.py
tools/mori-round19-regressions.py
tools/mori-round41-calibration.py
tools/mori-routed-check.py
tools/mori-routed-r24.py
tools/mori-seat-terminal.py
tools/mori-silence-cases.sh
tools/mori-source-drift.py
tools/mori-sources-appendonly.py
tools/mori-wave-settlement.py
```

34 entries = 33 files + `tools/fixtures/`. (`tools/__pycache__` is absent at that revision; it is
untracked and exists in the worktree only.) Split by extension, and the "other" bucket:

```
$ grep -c '\.py$' all.txt   # all.txt = the ls-tree output minus the tools/fixtures entry (33 lines)
29
$ grep -c '\.sh$' all.txt
4
$ grep -vE '\.(py|sh)$' all.txt     # → no output, rc=1
```

* **29 `.py`**: content-review, disk-rate, dispatch-ledger, evidence-loss, freeze-order,
  gate-registry, job-runway, journal-window, misroot-sweep, oom-killers, pressure,
  retention-gate, retention-reconcile, round13/14/15-regressions, round16-context-check,
  round16-regressions, round17-context-check, round17-jj-regressions,
  round17-seat-regressions, round19-regressions, round41-calibration, routed-check,
  routed-r24, seat-terminal, source-drift, sources-appendonly, wave-settlement.
* **4 `.sh`**: mori-blind-check.sh, mori-census.sh, mori-index-clean.sh,
  mori-silence-cases.sh.
* Extensionless executables in `tools/`: **none**.

Recursive check (so an auditor that walks instead of globbing cannot inflate N):

```
$ git ls-tree -r --name-only 554ff416 tools/ | grep -cE '\.(py|sh)$'
33
$ git ls-tree -r --name-only 554ff416 tools/ | grep -E '\.(py|sh)$' | grep '^tools/fixtures/'   # → empty
fixtures_py_sh_count=0
$ git ls-tree -r --name-only 554ff416 tools/fixtures/
tools/fixtures/mori-job-runway/cases.json
tools/fixtures/mori-job-runway/supplementary-cases.json
tools/fixtures/mori-oom-killers/cases-a2-r29.json
tools/fixtures/mori-oom-killers/cases-a2-r30.json
tools/fixtures/mori-oom-killers/cases-a2.json
tools/fixtures/mori-oom-killers/cases-r31-dryrun-flips.json
tools/fixtures/mori-oom-killers/cases-supplementary.json
tools/fixtures/mori-oom-killers/cases.json
tools/fixtures/mori-pressure/cases.json
tools/fixtures/mori-pressure/supplementary-cases.json
```

`tools/fixtures/` holds 10 `.json` case files and **zero** `.py`/`.sh`, so glob-walk and shallow
glob agree: **33**.

### 1b. Round counters

```
$ git ls-tree --name-only 554ff416 .ufo/waves/round-44/ | grep 'count-c'
.ufo/waves/round-44/count-c1.py
.ufo/waves/round-44/count-c2.py
.ufo/waves/round-44/count-c3.py
rc=0

$ ls -1 .ufo/waves/round-44/count-c*.py .ufo/waves/round-45/count-c*.py
ls: cannot access '.ufo/waves/round-45/count-c*.py': No such file or directory
.ufo/waves/round-44/count-c1.py
.ufo/waves/round-44/count-c2.py
.ufo/waves/round-44/count-c3.py
```

```
$ git ls-tree --name-only 554ff416 .ufo/waves/round-45/          # → empty output, exit 0
$ ls -1 .ufo/waves/round-45/
assimilation
contract.md
evidence
tmp
w1
w1-dispatch.json
w1-spec.json
$ find .ufo -name 'count-c*' -not -path '*/tmp/*' | grep round-45   # → empty
```

The frozen predicate's population expression is `.ufo/waves/round-4[45]/count-c*.py`, i.e. a
**one-level glob inside each round directory**. At `554ff416` that matches exactly 3 files, all
from round 44. Round 45 has none yet. The glob is deliberately shallow, which matters because
the repo has many deeper `count-c*` names that must **not** enter the population:

```
$ git ls-tree -r --name-only 554ff416 | grep -E 'count-c'
.ufo/waves/round-17/evidence/count-c1.json
.ufo/waves/round-17/evidence/count-c2.json
.ufo/waves/round-17/evidence/count-c3.json
.ufo/waves/round-17/evidence/final/count-c1.json
.ufo/waves/round-17/evidence/final/count-c2.json
.ufo/waves/round-17/evidence/final/count-c3.json
.ufo/waves/round-26/count-c1.sh
.ufo/waves/round-26/count-c2.sh
.ufo/waves/round-27/count-c1.sh
.ufo/waves/round-27/count-c2.sh
.ufo/waves/round-28/count-c1.sh
.ufo/waves/round-28/count-c2.sh
.ufo/waves/round-28/evidence/tip-count-c1.txt
.ufo/waves/round-28/evidence/tip-count-c2.txt
.ufo/waves/round-29/count-c1.sh
.ufo/waves/round-29/count-c2.sh
.ufo/waves/round-30/count-c1.sh
.ufo/waves/round-30/count-c2.sh
.ufo/waves/round-31/count-c1-a1.py
.ufo/waves/round-31/count-c1.py
.ufo/waves/round-31/count-c2-a1.py
.ufo/waves/round-31/count-c2.py
.ufo/waves/round-32/count-c1.py
.ufo/waves/round-33/count-c1-a1.py
.ufo/waves/round-33/count-c1.py
.ufo/waves/round-34/count-c1-a1.py
.ufo/waves/round-34/count-c1.py
.ufo/waves/round-35/count-c1.py
.ufo/waves/round-36/count-c1.py
.ufo/waves/round-36/count-c2.py
.ufo/waves/round-37/count-c1.py
.ufo/waves/round-37/count-c2.py
.ufo/waves/round-38/count-c1.py
.ufo/waves/round-38/count-c4.py
.ufo/waves/round-38/scratch/red-receipts/count-c4-m1-red.py
.ufo/waves/round-39/count-c7.py
.ufo/waves/round-40/count-c8.py
.ufo/waves/round-40/fixtures/extracted/count-c7-r39.py
.ufo/waves/round-41/fixtures/c1/count-c8.py
.ufo/waves/round-42/count-c1.py
.ufo/waves/round-42/count-c2.py
.ufo/waves/round-42/count-c3.py
.ufo/waves/round-43/count-c1s.py
.ufo/waves/round-43/count-c2.py
.ufo/waves/round-44/count-c1.py
.ufo/waves/round-44/count-c2.py
.ufo/waves/round-44/count-c3.py
.ufo/waves/round-44/fixtures/mutants/count-c1.py
.ufo/waves/round-44/fixtures/mutants/count-c2.py
.ufo/waves/round-44/fixtures/mutants/count-c3.py
```

### 1c. N — the number the audit must reach `unregistered=0` / `no_selftest=0` over

| component | glob | count |
|---|---|---|
| lane tools, Python | `tools/*.py` | 29 |
| lane tools, shell | `tools/*.sh` | 4 |
| round-44 counters | `.ufo/waves/round-44/count-c*.py` | 3 |
| round-45 counters | `.ufo/waves/round-45/count-c*.py` | **0 today** |
| **N at `554ff416` (and at `HEAD`)** | | **36** |
| **N at the round's closing revision, if the three r45 counters land as `count-c*.py`** | | **39** |

Population is revision-invariant between the freeze rev and `HEAD` (nothing under `tools/` or the
three r44 counters changed):

```
$ git diff --stat 554ff416 HEAD -- tools/ .ufo/waves/round-44/count-c1.py .ufo/waves/round-44/count-c2.py .ufo/waves/round-44/count-c3.py
(empty)                                   diff_empty_rc=0
$ git diff --name-only 554ff416 HEAD
.ufo/waves/round-45/assimilation/opened/cgroup-v2.rst.src
.ufo/waves/round-45/assimilation/opened/proc5-zhTW.src
.ufo/waves/round-45/contract.md
.ufo/waves/round-45/w1-dispatch.json
.ufo/waves/round-45/w1-spec.json
corpus/lessons/round-44-verifier-spotcheck.md
```

**State the number as 36 at the freeze rev, 39 at closure.** The 33-tool arm is fixed; only the
counter arm can still move, and only in steps of 1 per `count-c*.py` file the round-45 executors
commit. This is the single sizing dependency the L1 must pin before scoring C2: if C2 is scored
at a revision where the r45 counters exist, `N=39`, and the frozen predicate's regex
`round-4[45]/count-c*.py` must be applied with a **non-recursive** directory glob: the tree at
`554ff416` holds **50** names matching `count-c` (measured:
`git ls-tree -r --name-only 554ff416 | grep -cE 'count-c'` → `50`), of which only the 3
top-level round-44 `.py` files belong to the population — the other 47 (`.sh`, `.json`,
`-a1`/`-a2` variants, `fixtures/extracted/`, `fixtures/mutants/`, `scratch/`) must stay out.

---

## §2 The three tools with no 8-cell row anywhere — confirmed

Method: enumerate every 8-cell table (header exact match
`| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |`), take
its span (`header+1` separator … last consecutive `|` row), then test each tool's every
occurrence in `SKILL.md` for membership in one of those spans.

```
$ for t in mori-disk-rate.py mori-wave-settlement.py mori-round41-calibration.py; do echo "--- $t"; grep -n -- "$t" SKILL.md | cut -c1-150; echo "grep_rc=${PIPESTATUS[0]}"; done
--- mori-disk-rate.py
830:## Round34 — two-sample disk write rate tool (FR6; tools/mori-disk-rate.py)
835:- Round34 rule: for a current write rate run `python3 tools/mori-disk-rate.py --interval-ms N` (live: read, wait N ms, read again) or add `--a FIL
grep_rc=0
--- mori-wave-settlement.py
482:| When to run the settlement scan | `python3 tools/mori-wave-settlement.py scan --lane-root <lane> [--fleet-root <fleet>] [--out FILE]` (the `--ou
grep_rc=0
--- mori-round41-calibration.py
grep_rc=1
```

Programmatic membership test over the seven spans:

```
mori-disk-rate.py in-8cell-table-lines= NONE
   L830 cells=None first120='## Round34 — two-sample disk write rate tool (FR6; tools/mori-disk-rate.py)'
   L835 cells=None first120='- Round34 rule: for a current write rate run `python3 tools/mori-disk-rate.py --interval-ms N` (live: read, wait N ms, r'
mori-wave-settlement.py in-8cell-table-lines= NONE
   L482 cells=4 first120='| When to run the settlement scan | `python3 tools/mori-wave-settlement.py scan --lane-root <lane> [--fleet-root <fleet>'
mori-round41-calibration.py in-8cell-table-lines= NONE
```

Per-tool verdict, with the reason each miss is a miss:

| tool | occurrences | why it is not an 8-cell row |
|---|---|---|
| `tools/mori-disk-rate.py` | L830 (`## Round34 —` heading), L835 (a `- Rule:` bullet) | both are prose, not table rows at all (`cells=None`) |
| `tools/mori-wave-settlement.py` | L482 | L482 is a row of the **4-cell** table `\| Intent \| Correct surface \| Never \| Expected output \|` (header L480, separator L481) |
| `tools/mori-round41-calibration.py` | none (`grep_rc=1`) | the string does not occur in `SKILL.md` anywhere |

L482's cell count, measured:

```
$ awk 'NR==482{n=gsub(/\|/,"|"); print "L482 pipes="n" cells="n-1}' SKILL.md
L482 pipes=5 cells=4
$ awk 'NR>=478 && NR<=482' SKILL.md | cut -c1-100
Detection only. The settlement scan is read-only; the re-pin is an L1 ritual. Neither starts, steers

| Intent | Correct surface | Never | Expected output |
|---|---|---|---|
| When to run the settlement scan | `python3 tools/mori-wave-settlement.py scan --lane-root <lane> [--fleet-root <fleet>] [
```

**Confirmed: all three are orphans under the frozen predicate.** The r44 inventory claim holds
byte-for-byte at `554ff416`.

Note the asymmetry the L1 must not lose: `mori-wave-settlement.py` **does** implement a real
`--selftest` argv branch, and it passes — measured, `tools/mori-wave-settlement.py:687`
`if args_list == ["--selftest"]:`:

```
$ export TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/PlanDataWalk
$ timeout 180 python3 tools/mori-wave-settlement.py --selftest
MORI_WAVE_SETTLEMENT_SELFTEST: PASS (23 cases, 23 passed, 0 failed)
rc=0
```

so its repair is a **registry row only**. `mori-disk-rate.py` and `mori-round41-calibration.py`
need **both** a row and a selftest branch.

---

## §3 The three tools with a row but no real `--selftest` argv branch — rc measured

Each was executed with the argv the task names, from the lane root, with `TMPDIR` set to my
scratch dir, `timeout 240`:

```
$ export TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/PlanDataWalk
$ for f in tools/mori-silence-cases.sh tools/mori-round19-regressions.py tools/mori-routed-check.py; do echo "##### $f --selftest"; if [ "${f##*.}" = sh ]; then timeout 240 bash "$f" --selftest; else timeout 240 python3 "$f" --selftest; fi; echo "rc=$?"; done
##### tools/mori-silence-cases.sh --selftest
mori-silence-cases: census not readable: --selftest
rc=2
##### tools/mori-round19-regressions.py --selftest
usage: mori-round19-regressions.py [-h] --content-tool PATH --freeze-tool PATH
                                   --expected PATH --output PATH
                                   --mode {before,after}
mori-round19-regressions.py: error: the following arguments are required: --content-tool, --freeze-tool, --expected, --output, --mode
rc=2
##### tools/mori-routed-check.py --selftest
usage: mori-routed-check.py [-h] --repo REPO --rev REV [--round ROUND_NUMBER]
mori-routed-check.py: error: the following arguments are required: --repo, --rev
rc=2
```

All three: **rc=2**, no selftest tally printed. Root causes, from the bytes:

* `mori-silence-cases.sh` has **no** argument parser for `--selftest`; `--selftest` is consumed as
  the positional census path:
  ```
  $ sed -n '176,182p' tools/mori-silence-cases.sh
  CENSUS=${1:-$SCRIPT_DIR/mori-census.sh}
  [ $# -gt 1 ] && { printf 'usage: mori-silence-cases.sh [path-to-census]\n' >&2; exit 2; }
  [ -f "$CENSUS" ] && [ -r "$CENSUS" ] || { printf 'mori-silence-cases: census not readable: %s\n' "$CENSUS" >&2; exit 2; }
  ```
  hence `census not readable: --selftest`, rc 2. Its only `--selftest` string is a **comment**
  (`tools/mori-silence-cases.sh:20`, “… runs the actual census CLI (bash "$CENSUS", no
  --selftest) and …”) — exactly the r44 silence-oracle false positive named in P-C2(4).
* `tools/mori-round19-regressions.py` contains **no** `--selftest` string at all; argparse rejects
  the unknown flag and also lists its five required arguments (rc 2).
* `tools/mori-routed-check.py` contains **no** `--selftest` string at all; argparse rejects the
  unknown flag and demands `--repo`/`--rev` (rc 2). Its row (L646) already admits this:
  self-test cell = “none built in; able-to-fail evidence is thirteen sandbox mutants in
  `.ufo/waves/round-24/w1/BuildRoutedCheck.md`”.

Substring census of the flag across the three (the measure the *current* auditor uses, §4):

```
$ for f in tools/mori-silence-cases.sh tools/mori-round19-regressions.py tools/mori-routed-check.py; do printf '%s: ' "$f"; grep -c -- '--selftest' "$f" || true; done
tools/mori-silence-cases.sh: 1
tools/mori-round19-regressions.py: 0
tools/mori-routed-check.py: 0
```

**Confirmed: all three are `no_selftest` under the frozen predicate.** Note the current
`tools/mori-gate-registry.py` PASSes `mori-silence-cases.sh` on that single comment line:

```
$ python3 tools/mori-gate-registry.py --rev 554ff416 --audit tools/mori-silence-cases.sh
audit tools/mori-silence-cases.sh              PASS (row 'silence oracle': 8 cells, entry resolves, --selftest present)
```

That `PASS … --selftest present` on a comment-only occurrence is the live reproduction of the r44
false positive P-C2(4) forbids, from the tool's own stdout.

---

## §4 The eight-standard-cell tables, with line numbers, and which the auditor reads

### 4a. Inventory — 7 tables carry the eight standard cells

Header, verbatim, in all seven: `| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |`

| # | header line | first row | last row | data rows | enclosing section (heading line) | read by current auditor? |
|---|---|---|---|---|---|---|
| 1 | **162** | 164 | 186 | 23 | `## Gates` (L156) | **YES — the only one** |
| 2 | 524 | 526 | 527 | 2 | `## Round21 retained-loss observation and policy-test registry` (L522) | no |
| 3 | 588 | 590 | 590 | 1 | `## Round23 — current reconciliation API; quota attempt withdrawn` (L571) | no |
| 4 | 643 | 645 | 646 | 2 | `## Round24 — one-shot system pressure read (C2)` (L615) | no |
| 5 | 718 | 720 | 722 | 3 | `## Round26 — userspace OOM killers (C1/C2)` (L680) | no |
| 6 | 796 | 798 | 798 | 1 | `## Round32 — blind-writer gate registry row and frozen run (round-31 routed defect 2)` (L788) | no |
| 7 | 881 | 883 | 893 | 11 | `## Round36 — source drift probe, SOURCES append-only gate, index check` (L860) | no |

Totals: **7 tables, 43 data rows**. All 43 rows have exactly 8 non-empty cells (checked below), so
“carries the eight standard cells” is literal, not approximate.

```
$ grep -n 'name | kind | entry | verdict map | self-test | pinned values | write scope | owner' SKILL.md
162:| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
524:| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
588:| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
643:| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
718:| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
796:| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
881:| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
```

```
$ grep -n '^## ' SKILL.md
11:## Decision table
23:## Error patterns
47:## Positive evidence vs an unavailable aggregate (r15)
105:## Window probe (r16) — exact retained anchor, no census change
139:## Boundaries (hard)
149:## Checklist (executable)
156:## Gates
346:## Finding → owner routing (two tiers — a deadlock was measured here)
378:## Secret-exposure exclusions (measured by a sentinel audit)
401:## Disk thresholds are a PROPOSAL, not a measurement
432:## Lane-silence grading is launch-aware and authorship-aware (r2 contract)
476:## Wave settlement scan and drift re-pin (r20)
522:## Round21 retained-loss observation and policy-test registry
539:## Round22 retention receipt reconciliation (accounting agreement only)
571:## Round23 — current reconciliation API; quota attempt withdrawn
615:## Round24 — one-shot system pressure read (C2)
648:## Round25 — harness background-job cap (C2)
680:## Round26 — userspace OOM killers (C1/C2)
724:## Round27 — OOM victim selection (oom-victim-selection-r27.md)
748:## Round30 — earlyoom invocation scope (earlyoom-invocation-scope-r30.md)
761:## Round31 — watchdog identity from a pid probe (watchdog-identity-r31.md)
776:## Round31 — blind-writer gate (`tools/mori-blind-check.sh`)
788:## Round32 — blind-writer gate registry row and frozen run (round-31 routed defect 2)
800:## Round32 — live recheck of mutable-URL sources (freshness)
815:## Round33 — disk write rate from /proc/diskstats (FR6; corpus/knowledge/disk-write-rate-r33.md)
830:## Round34 — two-sample disk write rate tool (FR6; tools/mori-disk-rate.py)
860:## Round36 — source drift probe, SOURCES append-only gate, index check
```

Span/row-count computation (`[a,b,rows]` = header line, last row line, data rows):

```
$ python3 - <<'EOF'
lines=open('SKILL.md',encoding='utf-8',errors='replace').read().split('\n')
hdr='| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |'
tables=[]
for i,l in enumerate(lines,1):
    if l.strip()==hdr:
        k=i+1
        while k<=len(lines) and lines[k-1].startswith('|'): k+=1
        tables.append((i,k-1))
print("tables:",[(a,b,b-a-1) for a,b in tables])
EOF
tables: [(162, 186, 23), (524, 527, 2), (588, 590, 1), (643, 646, 2), (718, 722, 3), (796, 798, 1), (881, 893, 11)]
```

Row-shape check, using the auditor's own escaped-pipe-aware splitter
(`CELL_SPLIT = re.compile(r"(?<!\\)\|")`, `tools/mori-gate-registry.py:63`) — two registry rows
contain a literal `\|` in prose (L172 `journal window (r16)`, L720 `userspace OOM killers (r26,
C2)`), and a naive `str.split('|')` mis-parses exactly those two, so the parser matters:

```
$ python3 -    # split_row copied from tools/mori-gate-registry.py:63-78
rows: 43 cell-count histogram: {8: 43}
violations: none
```

Duplicate row-name check (same parser, same run — relevant to the frozen `duplicate=0`
requirement):

```
total rows: 43
duplicate name cells: none
```

### 4b. Which table(s) the current `tools/mori-gate-registry.py` reads

**It reads table #1 only** — the table directly under `## Gates` (header L162, rows L164–186,
23 rows). Tables #2–#7 (L524, L588, L643, L718, L796, L881) are never parsed.

Code evidence, `tools/mori-gate-registry.py:81-107`:

```python
def parse_gate_table(text):
    """Rows of the `## Gates` table, header located by its field names."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().lower() == "## gates":
            start = i
            break
    if start is None:
        return None, None
    header, rows = None, []
    for line in lines[start + 1:]:
        stripped = line.strip()
        if stripped.startswith("## "):
            break
        if not stripped.startswith("|"):
            continue
        cells = split_row(stripped)
        low = [c.lower() for c in cells]
        if header is None:
            if len(cells) >= 8 and low[0] == "name" and low[1] == "kind":
                header = low
            continue
        ...
    return header, rows
```

Three independent reasons #2–#7 cannot be seen: (a) the only accepted section is the one whose
heading equals `## gates` verbatim, and there is exactly one; (b) the loop `break`s at the next
`## ` — L346 `## Finding → owner routing …` — so nothing after L345 is reachable; (c) even inside
that section the header must be ≥8 cells with `name`/`kind`. And `audit()` at
`tools/mori-gate-registry.py:110-116` calls `parse_gate_table` once and raises
`no gate table with a name/kind header in %s` when it is absent — there is no multi-table walk.

Empirical confirmation — a tool whose **only** row is table #7 (L883, “source drift (r36)”) is
reported `unregistered` by the current tool, which is impossible if #7 were read:

```
$ for t in tools/mori-census.sh tools/mori-disk-rate.py tools/mori-source-drift.py tools/mori-wave-settlement.py; do echo "##### --audit $t"; python3 tools/mori-gate-registry.py --rev 554ff416 --audit "$t"; echo "rc=$?"; done
##### --audit tools/mori-census.sh
audit tools/mori-census.sh                     PASS (row 'drift pin': 8 cells, entry resolves, --selftest present)
rev=554ff416459c92f0dea9762f834a556df2990187
REGISTRY=met
rc=0
##### --audit tools/mori-disk-rate.py
audit tools/mori-disk-rate.py                  FAIL (unregistered: no row names mori-disk-rate.py)
rev=554ff416459c92f0dea9762f834a556df2990187
REGISTRY=unmet
rc=1
##### --audit tools/mori-source-drift.py
audit tools/mori-source-drift.py               FAIL (unregistered: no row names mori-source-drift.py)
rev=554ff416459c92f0dea9762f834a556df2990187
REGISTRY=unmet
rc=1
##### --audit tools/mori-wave-settlement.py
audit tools/mori-wave-settlement.py            FAIL (unregistered: no row names mori-wave-settlement.py)
rev=554ff416459c92f0dea9762f834a556df2990187
REGISTRY=unmet
rc=1
```

`mori-source-drift.py` **does** have a row naming it, at L883, inside table #7 — and the tool still
says `unregistered`. That `tables=1` behaviour is precisely what P-C2(1) (“`tables=<n>`, not 1”)
targets.

Two side observations from the same run that the C2 executor will have to decide, both inside
table #1:

* `mori-census.sh` is named by **two** rows of table #1 — L164 `census` (entry
  `bash tools/mori-census.sh …`) and L165 `drift pin` (entry `bash tools/mori-census.sh --drift …`).
  The current `sorted(matches, key=lambda r: len(r[2]))[0]` picks `drift pin` (shorter entry cell),
  i.e. the attribution it prints is *a* row that names the path, not *the* canonical one. P-C2(2)
  requires the attribution be printed and be earned; it does not by itself forbid two naming rows,
  but the executor should pin a deterministic rule before the audit is scored.
* Row names are unique across all 7 tables (`duplicate name cells: none`), but **paths** are not
  unique: `mori-dispatch-ledger.py` is named by L162-table and L643-table; `mori-pressure.py` by
  the L643 and L718 tables; `mori-census.sh` twice within table #1. So a path→row attribution must
  be deterministic per path, and `duplicate=` semantics need to be stated as *name*-duplication
  (which is 0 today) rather than path-duplication (which is not).

---

## §5 Sizing deltas the L1 needs (derived from the bytes above)

Full-population run of the current auditor over the 36-member population at `554ff416`:

```
$ W=.ufo/waves/round-45/tmp/PlanDataWalk
$ python3 - "$W" <<'EOF' > $W/audit-all.txt 2>&1
import subprocess, re
rev = '554ff416'
pop = [l.strip() for l in subprocess.run(['git','ls-tree','--name-only',rev,'tools/'],
       capture_output=True, text=True).stdout.split('\n') if re.search(r'\.(py|sh)$', l)]
pop += [l.strip() for l in subprocess.run(['git','ls-tree','--name-only',rev,'.ufo/waves/round-44/'],
        capture_output=True, text=True).stdout.split('\n') if 'count-c' in l]
args = ['python3','tools/mori-gate-registry.py','--rev',rev]
for p in pop: args += ['--audit',p]
r = subprocess.run(args, capture_output=True, text=True)
print(r.stdout, end=''); print('rc=%d' % r.returncode)
fails = [l for l in r.stdout.split('\n') if ' FAIL ' in l]
print('SUMMARY population=%d fail=%d pass=%d' % (len(pop), len(fails), len(pop)-len(fails)))
for l in fails: print('FAILROW', l.strip())
EOF
# auditor stdout is saved at $W/audit-all.txt; the derived tail it printed:
<...36 'audit …' lines, then>
rev=554ff416459c92f0dea9762f834a556df2990187
REGISTRY=unmet
rc=1
SUMMARY population=36 fail=15 pass=21
FAILROW audit tools/mori-blind-check.sh                FAIL (unregistered: no row names mori-blind-check.sh)
FAILROW audit tools/mori-disk-rate.py                  FAIL (unregistered: no row names mori-disk-rate.py)
FAILROW audit tools/mori-evidence-loss.py              FAIL (unregistered: no row names mori-evidence-loss.py)
FAILROW audit tools/mori-index-clean.sh                FAIL (unregistered: no row names mori-index-clean.sh)
FAILROW audit tools/mori-job-runway.py                 FAIL (unregistered: no row names mori-job-runway.py)
FAILROW audit tools/mori-oom-killers.py                FAIL (unregistered: no row names mori-oom-killers.py)
FAILROW audit tools/mori-pressure.py                   FAIL (unregistered: no row names mori-pressure.py)
FAILROW audit tools/mori-retention-reconcile.py        FAIL (unregistered: no row names mori-retention-reconcile.py)
FAILROW audit tools/mori-round19-regressions.py        FAIL (row 'r19 finite regressions' tool has no --selftest mode)
FAILROW audit tools/mori-round41-calibration.py        FAIL (unregistered: no row names mori-round41-calibration.py)
FAILROW audit tools/mori-routed-check.py               FAIL (unregistered: no row names mori-routed-check.py)
FAILROW audit tools/mori-routed-r24.py                 FAIL (unregistered: no row names mori-routed-r24.py)
FAILROW audit tools/mori-source-drift.py               FAIL (unregistered: no row names mori-source-drift.py)
FAILROW audit tools/mori-sources-appendonly.py         FAIL (unregistered: no row names mori-sources-appendonly.py)
FAILROW audit tools/mori-wave-settlement.py            FAIL (unregistered: no row names mori-wave-settlement.py)
```

So today: **15/36 fail** (14 “unregistered” + 1 “no --selftest”), and 21 pass — including the
false-positive PASS of `mori-silence-cases.sh`.

Break the 36 down under the **frozen** predicate (rows in *any* of the 7 tables, real argv
branch), from the registration matrix and the flag census:

| bucket | count | files |
|---|---|---|
| registered by a row in one of the 7 tables | 33 | all except the three orphans |
| **unregistered (orphan)** | **3** | `mori-disk-rate.py`, `mori-wave-settlement.py`, `mori-round41-calibration.py` |
| registered but only in a post-`## Gates` table (invisible to the current tool) | 11 | blind-check, evidence-loss, index-clean, job-runway, oom-killers, pressure, retention-reconcile, routed-check, routed-r24, source-drift, sources-appendonly |
| no `--selftest` occurrence at all | 4 | `mori-disk-rate.py`, `mori-round19-regressions.py`, `mori-round41-calibration.py`, `mori-routed-check.py` |
| only a **comment**-line `--selftest` occurrence | 1 | `mori-silence-cases.sh` (L20) |
| **`no_selftest` under P-C2(4)** | **5** | the four above + `mori-silence-cases.sh` |
| registered **and** real-branch clean | 30 | 33 registered − 3 registered-but-`no_selftest` (`mori-round19-regressions.py`, `mori-routed-check.py`, `mori-silence-cases.sh`) |

Flag census producing the last three rows:

```
$ python3 -  # over the 36 population files at rev 554ff416, git show, classify occurrences
population N = 36

NO '--selftest' occurrence at all (4):
   tools/mori-disk-rate.py
   tools/mori-round19-regressions.py
   tools/mori-round41-calibration.py
   tools/mori-routed-check.py

ONLY comment-line occurrences (1):
   tools/mori-silence-cases.sh lines [20]
```

Distinct files with repair work to reach `unregistered=0` and `no_selftest=0`:
**6** — `mori-disk-rate.py` (row + branch), `mori-wave-settlement.py` (row), `mori-round41-calibration.py`
(row + branch), `mori-round19-regressions.py` (branch), `mori-routed-check.py` (branch),
`mori-silence-cases.sh` (branch). Plus the auditor itself must go from `tables=1` to `tables=7`
(§4b) and from substring-containment to real-argv-branch detection (§3) before those six can be
measured rather than asserted. Rows to add: 3; branches to add: 5 (two files need both).

Rows whose **self-test cell** (index 4) contains no `selftest`/`self-test` token at all — 6 rows,
measured with the escaped-pipe-aware splitter:

```
self-test cell (index 4) lacking selftest token:
  table@162 L166 name='silence oracle' cell='itself (hermetic case table, 28 cases)'
  table@162 L182 name='r19 finite regressions' cell='Same CLI over isolated synthetic Git fixtures (`--mode after`); before'
  table@643 L646 name='routed round-23 items (r24, C1)' cell='none built in; able-to-fail evidence is thirteen sandbox mutants in `.'
  table@881 L887 name='C1 counter challenge arm (r37)' cell='none (the three negative fixtures are the able-to-fail evidence)'
  table@881 L888 name='content-anchor check (r38)' cell='none (the three fabricated witnesses under `.ufo/waves/round-38/fixtur'
  table@881 L890 name='fabricated-content check v2 (r39)' cell='none (the four fabricated witnesses under `.ufo/waves/round-39/fixture'
```

**Trap for the executor:** the naive `str.split('|')` reports **8** such rows, adding L172
(`journal window (r16)`) and L720 (`userspace OOM killers (r26, C2)`) — both have a `\|` inside an
earlier cell, so a naive split shifts the self-test cell by one and reports a false selftest-less
row. Only the escaped-pipe-aware `CELL_SPLIT` gives the true 6. Of those 6, only L166 and L182 are
in the `no_selftest` set above; L646/L887/L888/L890 name rows whose tools do carry `--selftest`
(the cells are prose-only). The auditor must judge the tool body, not the cell text, per P-C2(4).

---

## §6 What I did not confirm

1. **The r45 counter filenames.** `.ufo/waves/round-45/` contains no `count-c*.py` at `554ff416`
   and none in the worktree. `N=39` is conditional on them being committed as
   `.ufo/waves/round-45/count-c{1,2,3}.py` (the predicate's `count-c*.py` would also accept
   `count-c1s.py`-style names, as round 43 did). I cannot state the closing N without them.
2. **The r45 counter paths' own registry status.** They do not exist, so `unregistered` for them
   is undefined rather than 0 — the audit cannot be scored `unregistered=0` over N=39 until they
   land.
3. **`tables=<n>` in the current tool's stdout.** The current tool prints no `tables=` field at
   all (see its `main()` at `tools/mori-gate-registry.py:273-304`); P-C2(1) requires one. I
   confirmed the *read set* (1 table) but the required `tables=<n>` output field does not exist
   yet, so there is no printed value to quote.
4. **Whether `mori-disk-rate.py` / `mori-round41-calibration.py` can carry a selftest at all.** I
   did not read either beyond the flag census; I know only that neither contains the string
   `--selftest`. Their selftest design is the executor's call, not a datum I can supply.
5. Nothing was run against live host surfaces, and no network read was needed; no `git` write, no
   `jj`, no `pacman` transaction, and no file outside this report and
   `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-45/tmp/PlanDataWalk` was written.

Confirmed by execution and therefore **not** in the unconfirmed list: `mori-wave-settlement.py
--selftest` is a real argv branch and passes (§2, 23/23, rc 0).


---

## §7 Follow-up answer (L1 request): the `no_selftest` set is **6**, not 5

**Correction of record.** §5 above printed `no_selftest` = 5 and “registered and real-branch
clean = 30”. Both are wrong; this section supersedes them. The correct figures, from the byte
evidence below, are **`no_selftest` = 6** over the population and **29** registered-and-clean.
Root cause of my error: my first pass counted *any* `--selftest` occurrence on a non-comment line
as “the tool's own branch”. `tools/mori-routed-r24.py` passes `--selftest` to **another** tool, so
it was falsely credited with a branch. RevAudit's inclusion of `routed-r24` is correct and my §5
omitted it.

Scope arithmetic that reconciles the two numbers (this is `[INFERENCE]` about their internals —
I can only see my own bytes):

| set | members | count |
|---|---|---|
| no own selftest branch, **whole population** | disk-rate, round19-regressions, round41-calibration, routed-check, routed-r24, silence-cases | **6** |
| no own selftest branch, **registered paths only** | round19-regressions, routed-check, routed-r24, silence-cases | **4** |
| the two that differ | `mori-disk-rate.py`, `mori-round41-calibration.py` — both **unregistered**, so a registered-only `no_selftest` arm cannot see them | — |

RevAudit's `no_selftest=4` **with routed-r24 included** is exactly the registered-only set above.
P-C2(5) requires `no_selftest=0` over “the whole declared population”, so **6 is the number the
predicate must reach**, and a `no_selftest` arm that reports 4 is scoped to registered rows only.

### 7a. Q1 — all six, with the occurrence list and why none is the tool's own argv branch

Evidence method: `git show 554ff416:<path>`, then every line matching `self[-_]?test` (case-
insensitive), then a check for the seven own-dispatch idioms the population actually uses
(inventory in §7c). None of the six matches any of them.

| # | file | `self[-_]?test` token lines | what the occurrence actually is |
|---|---|---|---|
| 1 | `tools/mori-disk-rate.py` | **none** (0) | no flag; options are `--a`, `--b`, `--sysfs`, `--interval-ms` (L263-269) |
| 2 | `tools/mori-round19-regressions.py` | **none** (0) | no flag; options are `--content-tool`, `--freeze-tool`, `--expected`, `--output`, `--mode {before,after}` (L1106-1110) |
| 3 | `tools/mori-round41-calibration.py` | **none** (0) | no flag; usage is `<revision> --repo DIR --reference-rev REV` (L4, L88-90) |
| 4 | `tools/mori-routed-check.py` | **none** (0) | no flag; options are `--repo`, `--rev`, `--round` (L704-706). Its only `--verify` strings are arguments to `git rev-parse --verify` (L163, L180), not a tool flag |
| 5 | `tools/mori-routed-r24.py` | **10** — L16, L19, L93, L96, L398, L399, L422, L432, L514, L901 | every one names **`mori-pressure.py`'s** flag, not its own: `EVIDENCE_COMMAND = "python3 -I -B tools/mori-pressure.py --selftest"` (L96), `def _run_pressure_selftest(...)` running `[sys.executable, "-I", "-B", script, "--selftest"]` (L422) where `script` is the extracted `tools/mori-pressure.py`; L901 is the `--rerun` help text |
| 6 | `tools/mori-silence-cases.sh` | **2** — L20, L290 | both **comments**: L20 “Each case runs the actual census CLI (bash "$CENSUS", no --selftest) and”, L290 “# idiom the census selftest uses; git deliberately NOT stubbed — real repos)”. Its argv is one optional positional census path (L179 `[ $# -gt 1 ] && … exit 2`) |

`mori-routed-r24.py` is the interesting one: its own options are `--repo`, `--rev`, `--rerun`
(L896-901), and `--rerun` “also re-execute[s] the named revision's pressure selftest and report
byte equality” — i.e. it verifies **`mori-pressure.py`**, not itself. No row could honestly
declare that as its own selftest, and row L721 does not claim one.

`tools/mori-source-drift.py` is **not** in this set and never was: it has a real branch,
`if argv == ["--selftest"]: return _selftest()` (L451-452).

### 7b. Q2 — the two files that need BOTH a row and a branch

* `tools/mori-disk-rate.py`
* `tools/mori-round41-calibration.py`

Both are in the orphan set (no 8-cell row anywhere, §2) **and** in the 0-token set above.

The other four need a branch only: `mori-round19-regressions.py`, `mori-routed-check.py`,
`mori-routed-r24.py`, `mori-silence-cases.sh` are each named by a row (L182, L646, L721, L166).
`mori-wave-settlement.py` needs a row only (its `--selftest` is real and passes, §2).

Revised work list to reach `unregistered=0` **and** `no_selftest=0`: **3 rows**, **6 branches**
(unless an escape flag is accepted, §7d), **7 distinct files**; plus §4b's `tables=1 → 7` and
§3's substring → own-branch detection.

### 7c. Q3 — is any of the six a real selftest under another spelling? **No.**

Checked against every alternate spelling named in the request (`--self-test`, `--self_test`, `-S`)
plus `--check`, `--verify`, and the bare `selftest` token:

```
$ for f in <the six>; do printf '%-38s ' "$(basename $f)"; git show 554ff416:$f | \
    grep -cE -- '--self[-_]?test|"-S"|(^|[[:space:]])-S([[:space:]]|$)|--check\b|--verify\b|selftest'; done
mori-disk-rate.py                      0
mori-round19-regressions.py            0
mori-round41-calibration.py            0
mori-routed-check.py                   2      # both = git rev-parse --verify (L163, L180)
mori-routed-r24.py                    10      # all = mori-pressure.py's flag (§7a row 5)
mori-silence-cases.sh                  2      # both = comments (L20, L290)
```

So the alternate-spelling set that a row could honestly declare via an escape flag is **empty**.

Two are close but do not qualify, and the L1 should decide them explicitly rather than by
accident:

* `mori-round19-regressions.py` — `--mode after` is its documented self-verification arm, and row
  L182 already declares exactly that CLI. But it is not an internal branch: it needs five
  caller-supplied absolute paths (`--content-tool`, `--freeze-tool`, `--expected`, `--output`) and
  verifies the *content-review* tool, not itself. Honest only as an *escape declaration of a full
  argv*, never as “has `--selftest`”.
* `mori-silence-cases.sh` — `bash tools/mori-silence-cases.sh` with no argument is a hermetic
  28-case harness (real temp git repos, pinned clock, exit 0 iff all cases matched), which is why
  row L166 says self-test = “itself (hermetic case table, 28 cases)”. But again it verifies the
  **census**, not itself; a `--selftest` for it would be circular. An escape flag naming the
  default invocation is defensible; adding `--selftest` that just runs the default invocation is
  not a selftest at all.

### 7d. Own-dispatch idiom inventory (what a correct detector must accept)

Measured over the 36-member population; these are the spellings that *are* real branches, so a
detector that only looks for `add_argument("--selftest")` produces false `no_selftest` verdicts,
and one that looks for any non-comment occurrence produces false clean verdicts (the routed-r24
case above):

```
own-branch idiom frequencies (files): {'argparse_decl': 18, 'dest_read': 23, 'argv_equality_py': 4, 'bash_test': 2}
```

* `case "$1" in --selftest) selftest=1; shift ;;` — `tools/mori-census.sh:4721` (a spelling my own
  first regex missed, which is why census briefly appeared in the miss list)
* `if [[ ${1-} == --selftest ]]; then` — `tools/mori-blind-check.sh:359`
* `if (( $# == 1 )) && [[ $1 == '--selftest' ]]; then` — `tools/mori-index-clean.sh:218`
* `if argv == ["--selftest"]:` — `mori-dispatch-ledger.py:547`, `mori-source-drift.py:451`,
  `mori-wave-settlement.py:687`
* `if arguments == ["--selftest"]:` — `mori-content-review.py:471`
* argparse `add_argument("--selftest"…)` + `if args.selftest:` — 18 files
* `ns.selftest` dest read — e.g. `tools/mori-job-runway.py:673`

Verified split of the six idioms over the population (`git show` at `554ff416`, one regex each):

```
clean: 30  no_branch: 6
   NO-BRANCH tools/mori-disk-rate.py
   NO-BRANCH tools/mori-round19-regressions.py
   NO-BRANCH tools/mori-round41-calibration.py
   NO-BRANCH tools/mori-routed-check.py
   NO-BRANCH tools/mori-routed-r24.py
   NO-BRANCH tools/mori-silence-cases.sh
```

Detection rule that matches all 30 clean files and rejects all 6: an occurrence counts only when
it is the **dispatch condition or the option declaration of the containing file**, i.e. on a line
matching one of the idioms above; an occurrence inside a comment, a docstring, or a subprocess
argument list (`[sys.executable, …, "--selftest"]`, `EVIDENCE_COMMAND = "… --selftest"`) does not
count.
