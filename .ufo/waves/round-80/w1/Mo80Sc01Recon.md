# Mo80Sc01Recon — read-only data-walk for round 80 (C1, C2, C3)

Seat: scout, read-only. Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering revision: `d5888922` (`d58889220d3c6a18d461f2d31b5ab162ffef1e4e`).
Lane tip while reading: `57451ecb` (round-80 freeze); `git log --reverse d577b3d3..HEAD` = `d5888922`, `57451ecb`.
Fleet repo: `/home/vgpnk/Projects/shokunin`.
Scratch: `/fast/scratch/hyaku/mori-r80/Mo80Sc01Recon` (deleted before yield). Nothing else written.

**State warning that governs every number below.** Peers are landing all three claims in the
worktree while this seat reads. `git status --porcelain` at 03:11 (-03:00) read clean except
`?? .ufo/waves/round-80/*`; the same command minutes later read
`M .ufo/waves/round-79/count-c2.py`, `M PROVINCE.md`, `M SCORECARD.md`, `M corpus/QUALITY.md`,
`M corpus/README.md`, `M corpus/SOURCES.md`, `?? tools/mori-claim-sweep.py`,
`?? .ufo/waves/round-80/claim-pins.json`, `?? corpus/evidence/sources-r80/`,
`?? corpus/knowledge/mutation-adequacy-r80.md`, `?? corpus/lessons/round-80.md`.
Every "entering" figure below is taken from the **blob at `d5888922`** via `git show`, never
from the worktree; §1.5, §2.5 and §3.5 give the worktree snapshot separately, labelled as such.

---

## 1. C1 population

### 1.1 Pointer census over the three graded populations

Command (script kept only in scratch; method copied verbatim into this report):

```
$ python3 -I pointers.py /home/vgpnk/Projects/shokunin/mori-shokunin
{"populations": {"axes": [7, 24, 24], "capabilities": [60, 122, 119], "shonen": [4, 48, 48]}, ...}
TOTAL pointers=194 resolved=191 unresolved=3
```

Populations: the `## Axes` table (SCORECARD.md:8-15), every contiguous table whose header
contains `capabilit` (29 tables, 60 data rows — the register at SCORECARD.md:1983-2004 has 20 of
them, the rest are per-round capability tables), and every `- [` line of SHONEN.md (4 lines).
Tokens counted = backticked spans whose body starts `corpus/…`, `tools/…` or `.ufo/…`, with a
`:N`/`:N-M` and an `@<sha>` suffix stripped, fenced blocks skipped.

| population | rows | pointers | resolve | do not resolve |
|---|---|---|---|---|
| `## Axes` | 7 | 24 | 24 | 0 |
| capabilities tables (29) | 60 | 122 | 119 | 3 |
| SHONEN `- [` | 4 | 48 | 48 | 0 |
| **total** | | **194** | **191** | **3** |

Register table alone (`SCORECARD.md:1983`, header `| key | capability | what it can now do |
evidence | first-working round |`): 20 rows, 23 pointers, 23 resolve, 0 unresolved.

The three that do not resolve are all **glob patterns**, not missing files:

```
SCORECARD.md:1558  `.ufo/waves/round-24/w2/Mut*.md`                        -> 16 files match
SCORECARD.md:1559  `.ufo/waves/round-24/evidence/c1-*.json`                -> 3 files match
SCORECARD.md:1593  `.ufo/waves/round-25/evidence/routed-r24-*-a5.txt`      -> 2 files match
$ ls -d '.ufo/waves/round-24/w2/Mut*.md' | wc -l            -> 16
$ ls -d '.ufo/waves/round-24/evidence/c1-*.json' | wc -l    -> 3
$ ls -d '.ufo/waves/round-25/evidence/routed-r24-*-a5.txt' | wc -l -> 2
```

Risk for C1: the frozen arm text ("a backticked token … that does not exist under `--root`")
does not say "expand globs", so a literal implementation makes the sweep report 3 mismatches at
every revision and C1 can never be met. The in-flight `tools/mori-claim-sweep.py` resolves this
by declaring glob support in its help text ("Patterns containing `*` or `?` resolve when at least
one existing path matches", `tools/mori-claim-sweep.py:18-19`) and its selftest carries
`case wildcard existing match` / `case wildcard no match`. That reading is defensible but is a
decision the C1 executor must state in the report, because it narrows "does not exist".

**Second-order finding: my 194 is a lower bound of a *narrower* population.** The sweep's own
pointer regex is not backtick-scoped (`POINTER = re.compile(r'(?<![\w./-])(?:corpus|tools|\.ufo)/[^\s`,;|)\]}]+')`,
`tools/mori-claim-sweep.py:44`); run live it reports `pointers=232` (§1.5) versus my 194. Glob
handling is therefore load-bearing for the tool as built, not just for my census.

### 1.2 Superseded control-receipt arm count (`18`)

Exhaustive search at `d5888922` (same bytes at `57451ecb` for these files — the freeze commit
touched only `.ufo/waves/round-80/*`):

```
$ for f in SCORECARD.md SKILL.md SHONEN.md LOG.md README.md; do
    echo "$f: $(git show d5888922:$f | grep -c 'selftest 18\|18/18\|18 arms\|18 in-memory')"; done
SCORECARD.md: 2
SKILL.md: 1
SHONEN.md: 0
LOG.md: 0
README.md: 0
```

Occurrences, each line read:

| file:line | text | class |
|---|---|---|
| `SCORECARD.md:4016` | "… selftest 18 in-memory cases; stdout only …" | **stale tally** (live `--selftest` = `pass=19 fail=0`) |
| `SCORECARD.md:4016` | "`.ufo/waves/round-79/evidence/after-r79.txt` (selftest 18/18, both live dirs)" | **stale evidence claim** in the same row |
| `SKILL.md:1365` | "… the wave seat froze 18 arms at sha `b3b2f9e2` and added the nineteenth after the reviewer's BOM/CRLF probes — the landed bytes `531d6b52` carry 19, so this cell states the landed count" | **disclosure of history**, not a stale tally; `CONTROL_RECEIPT_SELFTEST pass=19 fail=0` is what the cell states |
| `SCORECARD.md:1462` | "alias-bearing outputs8/18→0/18; schema-v2 outputs0/18→18/18" | unrelated r15 alias counts, matched only by my broad `18/18` pattern |

So exactly **one row (SCORECARD.md:4016) carries the superseded count, twice**. That matches the
r79 verifier spot-check's D79-1, which names both halves of the row. The pins file's single
`stale_literals` entry is `"selftest 18 in-memory cases"` — it catches the prose half, and the
`18/18` half is caught by the corrected row text, not by a pin; if the row is edited so that
only `18/18` survives, the pinned literal will not catch it.

### 1.3 Every stated selftest tally in the graded rows, and its live value

43 tally statements sit in graded rows (regex over `pass=N fail=0`, `PASS (N cases)`, `PASS N/N`,
`selftest N/N`, `selftest N … cases`, `pass=N`; this is a lower bound — prose forms like
"selftest 18 in-memory cases" needed the extra alternative). They name 24 distinct selftest
commands; I ran every one with `TMPDIR=<scratch>` and `--selftest`:

```
$ while read interp path; do timeout 180 $interp -I "$path" --selftest; done < selftest-cmds.txt
.ufo/waves/round-48/count-c1.py                     rc=0  C1_SELFTEST pass=34 fail=0
.ufo/waves/round-49/count-c1.py                     rc=0  C1_SELFTEST pass=44 fail=0
.ufo/waves/round-49/flagged-fixed/count-flagged.py  rc=2  (argparse: unrecognized arguments: --selftest)
.ufo/waves/round-61/count-c3.py                     rc=0  C3_SELFTEST pass=8 fail=0
tools/mori-anchor-check.py                          rc=0  ANCHOR_CHECK_SELFTEST: PASS (11 cases)
tools/mori-cgroup-pressure.py                       rc=0  MORI_CGROUP_PRESSURE_SELFTEST: pass=12 fail=0
tools/mori-claim-sweep.py                           rc=0  CLAIM_SWEEP_SELFTEST pass=27 fail=0
tools/mori-counter-win.py                           rc=0  COUNTER_WIN_SELFTEST: PASS (12 cases)
tools/mori-drift-adjudicate.py                      rc=0  MORI_DRIFT_ADJUDICATE_SELFTEST: PASS (5 cases)
tools/mori-drift-recheck.py                         rc=0  MORI_DRIFT_RECHECK_SELFTEST: PASS (10 cases)
tools/mori-events-context-win.py                    rc=0  EVENTS_CONTEXT_SELFTEST: PASS (10 cases)
tools/mori-host-events-win.py                       rc=0  HOST_EVENTS_WIN_SELFTEST pass=10 fail=0
tools/mori-pin-check.py                             rc=0  PIN_CHECK_SELFTEST pass=125 fail=0
tools/mori-receipt-complete.py                      rc=0  RECEIPT_COMPLETE_SELFTEST pass=8 fail=0
tools/mori-register-check.py                        rc=0  REGCHECK_SELFTEST pass=12 fail=0
tools/mori-rotation-schedule.py                     rc=0  MORI_ROTATION_SCHEDULE_SELFTEST: PASS (13 cases)
tools/mori-runway-win.py                            rc=0  RUNWAY_WIN_SELFTEST: PASS (9 cases)
tools/mori-settlement-scan.py                       rc=0  SETSCAN_SELFTEST pass=10 fail=0
tools/mori-ua-variance.py                           rc=0  MORI_UA_VARIANCE_SELFTEST: PASS (14 cases)
tools/mori-unlanded-check.py                        rc=0  UNLANDED_SELFTEST pass=17 fail=0
tools/mori-uptime-win.py                            rc=0  UPTIME_WIN_SELFTEST: PASS (8 cases)
tools/mori-vote-bind.py                             rc=0  VOTE_BIND_SELFTEST pass=16 fail=0
tools/mori-workstate-win.py                         rc=0  WORKSTATE_WIN_SELFTEST: PASS (10 cases)
```

Findings, in order of consequence for C1:

1. **Named stale tally confirmed.** `tools/mori-control-receipt.py --selftest` →
   `CONTROL_RECEIPT_SELFTEST pass=19 fail=0` (rc 0); `SCORECARD.md:4016` states 18.
2. **A second, unnamed stale tally exists in a graded capabilities row.**
   `SCORECARD.md:2637` states "`python3 tools/mori-unlanded-check.py --selftest` →
   `UNLANDED_SELFTEST pass=13 fail=0`", but the tool's own blob at `d5888922` prints 17:
   ```
   $ git show d5888922:tools/mori-unlanded-check.py > $S/unlanded-at-d5888922.py
   $ python3 -I $S/unlanded-at-d5888922.py --selftest | tail -1
   UNLANDED_SELFTEST pass=17 fail=0      rc=0
   ```
   `SKILL.md:973` for the same tool deliberately states `pass=<N>`, a placeholder. The frozen
   `count-c1.py` grades only the control-receipt row ("Named limit … it does not independently
   re-derive every pinned tally the sweep checks", `.ufo/waves/round-80/count-c1.py:18-19`), so
   `C1=met` is reachable with this stale figure standing. It is a calibration finding for the
   closure, not a predicate violation.
3. **Two register tallies are structurally unverifiable from a bounded scratch dir** — both
   demand `TMPDIR` inside the lane checkout, and the round bounds forbid writing there:
   ```
   $ python3 -I tools/mori-retention-gate.py --selftest   ; echo rc=$?
   SELFTEST retention-gate FAIL 0/21                       rc=2
     (tools/mori-retention-gate.py:457-468: requires TMPDIR == <root>/.scratch, else FAIL 0/21 rc 2)
   $ python3 -I tools/mori-freeze-order.py --selftest     ; echo rc=$?
   SELFTEST freeze-order FAIL 0/11                         rc=1
     (tools/mori-freeze-order.py:497-512: requires TMPDIR under the lane checkout and not /tmp, /var/tmp)
   ```
   `SCORECARD.md:1989` pins retention-gate at `selftest 21/21` and `:1990` pins freeze-order at
   `selftest 12/12`. These are **not measurable at this seat's scratch**, so I record them as
   unverified, not red. Consequence: never add these two to `claim-pins.json` — the sweep treats
   a failing selftest as a setup error (rc 2), so pinning either makes C1 unreachable from any
   legal TMPDIR. The current pins file pins only `tools/mori-control-receipt.py: 19`.
4. **`tools/mori-dispatch-ledger.py` (pinned `selftest 14/14` at `SCORECARD.md:1991`) passes only
   when `TMPDIR` names a scratch directory:**
   ```
   $ python3 -I tools/mori-dispatch-ledger.py --selftest     (TMPDIR unset)
   {"error":"TMPDIR must name the executor scratch directory","finding_id":"SELFTEST_SCRATCH_REQUIRED", ...} rc=2
   $ TMPDIR=<scratch> python3 -I tools/mori-dispatch-ledger.py --selftest
   SELFTEST mori-dispatch-ledger PASS 14/14                  rc=0
   ```
   The sweep declares it inherits `TMPDIR` into children, so this is compatible as long as the
   invocation exports one.
5. **`count-flagged.py` is a false positive of my tally regex**, corrected by reading the row:
   `SCORECARD.md:2668` cites `python3 .ufo/waves/round-49/flagged-fixed/count-flagged.py` as a
   *live run* (`flagged=45 fixed=18 unfixed=9`), never `--selftest`. Its rc=2 under `--selftest`
   is argparse rejecting an unknown flag, not a stale pin.
6. Every other tally in the graded rows is green at the bytes it names (table above), including
   the register's `21/21`, `12/12`, `14/14` neighbours that I could run (none of the three above
   is in that set) and SHONEN's twelve.

### 1.4 C1 risk — the adjacency `## Axes` cell

The cell at `d5888922:SCORECARD.md:15` (read whole):

> refuses dispatch (kumitate), OS state (tsukuroi) and harness configuration (operator) in
> PROVINCE and in its tools; score stated at `corpus/lessons/round-14-verifier-spotcheck.md:87`;
> latest admitted closure grading adjacency improved has no lane spot-check file:
> MANIFEST.json@63729047 mori round 19 (fleet MANIFEST.json rounds[398], verdicts.adjacency improved)

Checks, each with its command:

```
# (a) the phantom token alleged by r79 D79-3
$ git show d5888922:SCORECARD.md | sed -n 15p | grep -c 'round-19-verifier-spotcheck'   -> 0
$ git show 84c6cbc3:SCORECARD.md | sed -n 15p | grep -o 'round-19-verifier-spotcheck[^`]*' -> (no match, rc 1)
$ git log --all --oneline -S 'round-19-verifier-spotcheck' -- SCORECARD.md | wc -l      -> 0

# (b) the in-root pointer the cell does carry
$ ls corpus/lessons/round-14-verifier-spotcheck.md
corpus/lessons/round-14-verifier-spotcheck.md                                            (exists)

# (c) the fleet-revision pointer the cell carries
$ git -C /home/vgpnk/Projects/shokunin cat-file -e 63729047:MANIFEST.json ; echo rc=$?
rc=0
$ python3 -c "... MANIFEST.json rounds[397..399] ..."
398 {'lane': 'mori', 'round': 19, 'verdicts': {'adjacency': 'improved', 'calibration': 'improved',
     'depth': 'unchanged', 'coverage': 'unchanged', 'operability': 'unchanged', 'freshness': 'unchanged'}}

# (d) is MANIFEST.json in-root?
$ ls MANIFEST.json
ls: cannot access 'MANIFEST.json': No such file or directory
```

**Verdict.** D79-3's premise is **false at the bytes it was written against**: the cell does not
cite `corpus/lessons/round-19-verifier-spotcheck.md`, and that token has **never** occurred in
`SCORECARD.md` on any ref (`git log -S` = 0 commits). The cell in fact *discloses the absence*
("has no lane spot-check file") and points at the fleet MANIFEST row instead. The r79 verifier
spot-check appears to have inherited the token from the earlier r29/r33 audits that describe the
missing file (`.ufo/waves/round-29/w1/AxisAdjacency.md:129`,
`.ufo/waves/round-33/w1/ConnectorSiblings.md:104`), not from the cell. So the cell has **no dead
lane pointer**: `corpus/lessons/round-14-verifier-spotcheck.md:87` resolves, and
`MANIFEST.json@63729047` resolves in the fleet repo where `rounds[398]` is lane `mori`, round 19,
`verdicts.adjacency = improved` — everything the cell asserts is true.

Residual, smaller risks the cell does carry: (i) `MANIFEST.json@63729047` is a **fleet-root**
path, so it does not resolve under a lane-root `--root`; the frozen sweep is immune only because
its token classes are `corpus|tools|.ufo`, and the round contract's counter exports the lane
repo. Do not widen the pointer regex to bare `MANIFEST.json` — that would convert this cell into
a permanent unresolved. (ii) The revision `63729047` is now 479 rounds old; it is a legitimate
pinned historical reference, and the cell says so.

### 1.5 C1 worktree snapshot (in-flight, NOT a receipt)

Read-only, for the main agent's situational awareness only; nothing here is verified as landed:

```
$ TMPDIR=<scratch> python3 -I tools/mori-claim-sweep.py --selftest | tail -1
CLAIM_SWEEP_SELFTEST pass=27 fail=0
$ TMPDIR=<scratch> python3 -I tools/mori-claim-sweep.py --root . --pins .ufo/waves/round-80/claim-pins.json
CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=4 pointers=232   rc=0
```

`claim-pins.json` (untracked) pins exactly one tally (`tools/mori-control-receipt.py: 19`) and
one stale literal (`selftest 18 in-memory cases`). The worktree `SCORECARD.md` is +35/−1 with a
correction paragraph at `:4026` that reads "18/18 annotation is superseded here by 19/19".

---

## 2. C2 population

### 2.1 Selftest arm labels at the entering bytes

```
$ git show d5888922:.ufo/waves/round-79/count-c2.py | grep -n 'cases.append'
152:    cases.append(("conformant_met", good, rounds, True))
155:    cases.append(("stale_cell_unmet", stale, rounds, False))
158:    cases.append(("verdict_word_missing_unmet", noverdict, rounds, False))
161:    cases.append(("subsumed_by_higher_round_unmet", low, rounds, False))
```

**Four arms at `d5888922`**, and the base selftest over that blob would read
`C2_COUNTER_SELFTEST pass=4 fail=0`. (The worktree file at the time of reading has 7 — §2.5.)

### 2.2 The r79 mutation seat's three survivors, mapped to the harness's six

`Mo79M02MutantCounter.md` records M1/M4/M5 as the survivors (its §4, line 366-370: "All three
survivors leave the real entering mismatch count at 5"). Its diff hunks map onto the frozen
harness labels:

| r79 label | r79 diff (verbatim from `w1/Mo79M02MutantCounter.md`) | harness label | at `d5888922` |
|---|---|---|---|
| M1 | `- if r.get("lane") != LANE or not r.get("admitted"):` → `if r.get("lane") != LANE:` | `drop_admitted` (byte-identical) | **survives** |
| M4 | `- tail = cell[m.end():].split(";")[0]` → `tail = cell[m.end():]` | `cut_clause_boundary` (byte-identical) | **survives** |
| M5 | `- m = ROUND.search(cell)` → `m = next((candidate for candidate in ROUND.finditer(cell) if want and int(candidate.group(1)) == want[0]), ROUND.search(cell))` | `any_round_in_cell` — **a *different* substitution** (`_ms = list(ROUND.finditer(cell)); m = _ms[-1] if _ms else None`) | harness label **killed**; r79's exact M5 **survives** |

The last row is the one worth carrying into the C2 executor's report. I applied r79's exact M5
text to the `d5888922` blob:

```
$ git show d5888922:.ufo/waves/round-79/count-c2.py > $S/c2-base.py
$ python3 - <<'PY'   # replace the single anchor line with r79's M5 line
...
$ TMPDIR=$S python3 -I $S/c2-base.py.m5 --selftest --scratch $S
PASS conformant_met met=True
PASS stale_cell_unmet met=False
PASS verdict_word_missing_unmet met=False
PASS subsumed_by_higher_round_unmet met=False
C2_COUNTER_SELFTEST pass=4 fail=0        rc=0     -> SURVIVED
```

So "the three r79 survivors" and "the harness's six mutants" are **not** the same set: two of the
three r79 survivors (`drop_admitted`, `cut_clause_boundary`) survive at entering and are in the
harness; the third r79 survivor (M5) is **not** in the harness's six, and the harness's nearest
label (`any_round_in_cell`) is already killed at entering. After the three new arms, r79's exact
M5 should be re-tested independently — the frozen harness will not grade it.

### 2.3 Frozen harness measurement at the entering revision

```
$ TMPDIR=<scratch> python3 -I .ufo/waves/round-80/mutate-c2.py --rev d5888922
mutant drop_admitted survived rc=0 C2_COUNTER_SELFTEST pass=4 fail=0
mutant raise_ceiling killed rc=1 C2_COUNTER_SELFTEST pass=3 fail=1
mutant count_other_verdicts killed rc=1 C2_COUNTER_SELFTEST pass=3 fail=1
mutant cut_clause_boundary survived rc=0 C2_COUNTER_SELFTEST pass=4 fail=0
mutant any_round_in_cell killed rc=1 C2_COUNTER_SELFTEST pass=3 fail=1
mutant met_ignores_mismatch killed rc=1 C2_COUNTER_SELFTEST pass=1 fail=3
MUTATION_C2 survivors=2 killed=4 total=6 rev=d58889220d3c     rc=1
```

Reproduces the contract's `survivors=2` exactly.

**Defect in a frozen file (report, do not edit).** `mutate-c2.py`'s own docstring, line 12,
states "At the entering revision the same harness prints `survivors=3 killed=3 total=6`". The
contract (§ P-C2) says 2, and the run prints 2. The harness grades correctly; its prose is
stale. `mutate-c2.py --selftest` → `MUTATE_C2_SELFTEST pass=3 fail=0` rc 0 (it asserts `green
stub all survive`, `red stub all killed`, `real_counter_anchors absent=[]`), so the harness's
self-check does not cover its own docstring. Bounds forbid editing it; the L1 must either leave
the stale sentence and disclose it, or authorise a one-line correction.

### 2.4 What the added arms must do (data for the executor)

The three surviving r79 classes are exactly: (a) drop the `admitted` filter, (b) search past the
first `;`, (c) accept a matching round anywhere in the cell. §2.2 shows (c)'s phrasing matters:
r79's "first round whose number equals `want`" and the harness's "last round in the cell" are
different mutants with different survival at entering.

### 2.5 C2 worktree snapshot (in-flight, NOT a receipt)

`M .ufo/waves/round-79/count-c2.py`; worktree sha256 `8d7fae146589341368399b490ae7c5b4bd55ee9d25496202ca8e0f7e010f1d69`
against committed blob `84f15b0ae653e3bdaf329321648b4e731c527337`. The diff is +16 lines and
adds exactly the three arms the deliverable names (`nonadmitted_below_ceiling_ignored_met`,
`verdict_after_clause_boundary_unmet`, `later_round_in_cell_ignored_unmet`). I graded those
bytes in a scratch repo containing only that file, so the harness's `--repo`/`--rev` path was
exercised against a pinned copy:

```
$ sha256sum f/repo/.ufo/waves/round-79/count-c2.py
8d7fae14…  (same as the worktree file)
$ TMPDIR=$S python3 -I .ufo/waves/round-80/mutate-c2.py --repo $S/f/repo --rev HEAD --scratch $S
mutant drop_admitted killed rc=1 C2_COUNTER_SELFTEST pass=6 fail=1
mutant raise_ceiling killed rc=1 C2_COUNTER_SELFTEST pass=5 fail=2
mutant count_other_verdicts killed rc=1 C2_COUNTER_SELFTEST pass=5 fail=2
mutant cut_clause_boundary killed rc=1 C2_COUNTER_SELFTEST pass=6 fail=1
mutant any_round_in_cell killed rc=1 C2_COUNTER_SELFTEST pass=5 fail=2
mutant met_ignores_mismatch killed rc=1 C2_COUNTER_SELFTEST pass=2 fail=5
MUTATION_C2 survivors=0 killed=6 total=6 rev=2ecfdb69a847     rc=0
```

Beware the worktree base selftest is now 7 arms + the mutants remove 4 → `pass=6`/`pass=5`
figures above are *not* the entering `pass=4`. The worktree file is uncommitted, so the C2 grade
must be re-derived at the committed R by the counter, not from this line.

---

## 3. C3 population

### 3.1 The instrument set at `d5888922`

```
$ git ls-tree -r --name-only d5888922 -- tools/ | wc -l                        -> 121
$ git ls-tree -r --name-only d5888922 -- tools/ | grep -cE '^tools/[^/]+\.(py|sh)$'  -> 55
$ git ls-tree -r --name-only d5888922 -- tools/ | grep -cvE '^tools/[^/]+$'    -> 66
```

55 top-level `tools/*.py|*.sh` (the frozen counter's population, `TREE = re.compile(r"^tools/([A-Za-z0-9_.-]+\.(?:py|sh))$")`)
and 66 nested paths under `tools/fixtures/…` (case JSON, PSI fixture trees) that the counter's
regex cannot match. So **fixture data needs no exclusion decision**: P-C3's "every path that
`git ls-tree -r --name-only R -- tools/` reports **with that shape**" already excludes nesting.
`tools/mori-claim-sweep.py` is not in the 55 at `d5888922` (it lands this round); it will make 56
at R and must be added to the inventory in the same commit, or `extra`/`missing` will move.

### 3.2 What `PROVINCE.md` already names

The frozen counter's own parse, recomputed independently on the `d5888922` blob (its
`SIBLING = re.compile(r"[A-Za-z0-9_-]+-shokunin/$")` 40-character lookback applied):

```
$ git show d5888922:PROVINCE.md > $S/province-at-entering.md
distinct named 14
mori-census.sh  mori-commit-runway.py  mori-dispatch-ledger.py  mori-freeze-order.py
mori-host-events-win.py  mori-job-runway.py  mori-journal-window.py  mori-oom-killers.py
mori-pressure.py  mori-retention-gate.py  mori-runway-win.py  mori-seat-terminal.py
mori-source-drift.py  mori-wave-settlement.py
--- sibling-skipped 1 ['tsukuroi-census.sh']
```

and `python3 -I .ufo/waves/round-80/count-c3.py d5888922` →
`C3=unmet named=14 present=55 missing=41 extra=0  rev=d58889220d3c` rc 1, matching the control
receipt. The one `extra`-shaped token (`tools/tsukuroi-census.sh`) is correctly excluded by the
sibling rule — that is the contract's "a sibling lane's `tools/...` path named in PROVINCE is not
a lane instrument".

### 3.3 The 55, with class data the inventory needs

Derived from each blob's own docstring at `d5888922`; `selftest` = the string `--selftest` occurs
in the source; registry row = first `SKILL.md` table row (at `d5888922`) whose cells contain the
basename. **`registry row` is my first-match heuristic, not the C3 executor's ruling** — a tool
mentioned in prose tables (e.g. `mori-evidence-loss.py`) may deserve `—`, and the executor must
decide. One fact is unambiguous and worth carrying: **`tools/mori-cgroup-pressure.py` has zero
occurrences in `SKILL.md` at `d5888922`** (`grep -c` on the blob = 0), so it is the only
instrument that certainly needs `—`.

| instrument | selftest | SKILL row (line: label) | purpose (docstring) |
|---|---|---|---|
| tools/mori-anchor-check.py | yes | 1326: anchor checker (r72 tool) | located-line and word-count verification |
| tools/mori-blind-check.sh | yes | 817: blind-writer gate (r31) | blind-writer path gate |
| tools/mori-census.sh | yes | 164: census | read-only fleet/host observability census |
| tools/mori-cgroup-pressure.py | yes | **—** | per-cgroup PSI survey (cpu, memory, io, irq) |
| tools/mori-commit-runway.py | yes | 1209: commit runway (r53, C2) | CommitLimit/Committed_AS by overcommit mode |
| tools/mori-content-review.py | yes | 181: r19 content review (C1) | bounded content-review gate |
| tools/mori-control-receipt.py | yes | 1365: control-receipt guard (r79 tool) | control-receipt binding guard |
| tools/mori-counter-win.py | yes | 1328: counter probe (r77 tool) | Windows memory/paging counters |
| tools/mori-disk-rate.py | yes | 187: disk write rate (r34) | two-sample disk write-rate arm |
| tools/mori-dispatch-ledger.py | yes | 180: r18 dispatch ledger (C3) | per-attempt dispatch payload identities |
| tools/mori-drift-adjudicate.py | yes | 1320: drift-finding adjudicator (r65 tool) | resolve drift findings to a closed set |
| tools/mori-drift-recheck.py | yes | 1321: standing drift re-check (r66/r67 tool) | recheck with as-of stamps |
| tools/mori-driver-liveness.py | yes | 1294: driver-liveness probe (r56 tool) | per-lane watchdog log facts |
| tools/mori-entry-claims-check.py | yes | 1297: entry-claims checker (r60 tool) | quote-bound entry-claims verifier |
| tools/mori-events-context-win.py | yes | 1325: events-context pairing (r71 tool) | events window paired with boot context |
| tools/mori-evidence-loss.py | yes | 545: retained-loss audit | classify retained-evidence loss |
| tools/mori-freeze-order.py | yes | 179: r18 freeze-order (C2) | frozen inputs vs implementation history |
| tools/mori-gate-registry.py | yes | 184: r44 gate registry (C2) | gate-registry auditor v2 |
| tools/mori-host-events-win.py | yes | 1318: host-events probe (r63 tool) | Windows event-log read |
| tools/mori-index-clean.sh | yes | 904: index clean (r36) | is a repo's git index clean |
| tools/mori-job-runway.py | yes | 741: harness background-job runway (r25, C2) | async.maxJobs + clamp/default |
| tools/mori-journal-window.py | yes | 172: journal window (r16) | MESSAGE-free same-boot journal window |
| tools/mori-misroot-sweep.py | yes | 176: misroot sweep (r17) | fleet-root misroot candidates |
| tools/mori-oom-killers.py | yes | 739: userspace OOM killers (r26, C2) | earlyoom/oomd state + counts |
| tools/mori-pin-check.py | yes | 938: registry pin reconciler (r47, C1) | re-measure SKILL self-test pins |
| tools/mori-pressure.py | yes | 664: system pressure (r24, C2) | one-shot PSI read |
| tools/mori-receipt-complete.py | yes | 1317: receipt-complete guard (r63 tool) | `failed=` anchor-list guard |
| tools/mori-register-check.py | yes | 1295: register checker (r59 tool) | capabilities-register checker |
| tools/mori-retention-gate.py | yes | 178: r18 retention (C1) | retention policy scan |
| tools/mori-retention-reconcile.py | yes | 609: retention reconciliation schema-v2 (r23) | independent retention recount |
| tools/mori-rotation-schedule.py | yes | 1327: rotation-schedule probe (r74 tool) | rotation-recurrence protocol |
| tools/mori-round13-regressions.py | yes | 167: r13 regressions | round-13 regression gate |
| tools/mori-round14-regressions.py | yes | 168: r14 regressions | round-14 C1 repair gate |
| tools/mori-round15-regressions.py | yes | 169: r15 regressions | round-15 fixture-pack gate |
| tools/mori-round16-context-check.py | yes | 171: r16 context check | wave-spec contract context |
| tools/mori-round16-regressions.py | yes | 170: r16 regressions | round-16 fixture-pack gate |
| tools/mori-round17-context-check.py | yes | 177: r17 context check | wave-spec contract context |
| tools/mori-round17-jj-regressions.py | yes | 175: r17 jj regressions | jj-colocation correctness of census |
| tools/mori-round17-seat-regressions.py | yes | 174: r17 seat regressions | round-17 C1 fixture gate |
| tools/mori-round19-regressions.py | yes | 182: r19 finite regressions | round-19 synthetic regressions |
| tools/mori-round41-calibration.py | yes | 189: r41 calibration | round-40 C2 mismatch count |
| tools/mori-routed-check.py | yes | 665: routed round-23 items (r24, C1) | round-23 routed items |
| tools/mori-routed-r24.py | yes | 740: routed round-24 items (r25, C1) | round-24 defects D1..D5 |
| tools/mori-runway-win.py | yes | 1319: runway probe (r64 tool) | Windows resource-runway read |
| tools/mori-seat-terminal.py | yes | 173: seat terminal status (r17) | seat transcript terminal census |
| tools/mori-settlement-scan.py | yes | 1296: settlement scanner (r59 tool) | wave-settlement results scan |
| tools/mori-silence-cases.sh | yes | 166: silence oracle | census lane-silence counting driver |
| tools/mori-source-drift.py | yes | 902: source drift (r36) | re-fetch SOURCES rows with anchors |
| tools/mori-sources-appendonly.py | yes | 903: SOURCES append-only (r36) | CORPUS rule-2 gate |
| tools/mori-ua-variance.py | yes | 1322: UA-variance probe (r68/r69 tool) | per-response vs stable chrome |
| tools/mori-unlanded-check.py | yes | 973: unlanded check (r48) | uncommitted round work |
| tools/mori-uptime-win.py | yes | 1323: uptime probe (r70 tool) | Windows host-uptime read |
| tools/mori-vote-bind.py | yes | 1293: vote binder (r56 tool) | dual-shape vote binding |
| tools/mori-wave-settlement.py | yes | 188: wave settlement (r20) | per-seat settlement scan |
| tools/mori-workstate-win.py | yes | 1324: workstate probe (r71 tool) | working-state pair with bias flag |

Class split that the inventory will have to choose (data only, no exclusion is admissible under
P-C3): 15 are round-scoped gates/drivers (`mori-round13/14/15/16-context/16-regressions/17-context/17-jj/17-seat/19/41`,
`mori-routed-check`, `mori-routed-r24`, `mori-entry-claims-check`, `mori-unlanded-check`,
`mori-evidence-loss`); the other 40 are standing instruments (`gate` / `probe` / `driver`).
All 55 carry `--selftest` in source — no tool needs a "no selftest" note.

### 3.4 C3 worktree snapshot (in-flight, NOT a receipt)

`M PROVINCE.md` (+66 lines, one appended `## Instrument inventory (round 80)` section, 56 table
rows = the 55 + `tools/mori-claim-sweep.py`). Graded in a scratch repo holding the worktree
`PROVINCE.md` plus the 55 blobs:

```
$ TMPDIR=$S python3 -I .ufo/waves/round-80/count-c3.py HEAD --repo $S/g/repo --scratch $S
C3=met named=55 present=55 missing=0 extra=0 rev=88aba19cabc0     rc=0
```

(The scratch repo has 55 tools, so `mori-claim-sweep.py`'s inventory row would become `extra`
once it is committed; the counter is applied at R, not here.) The counter's own selftest:
`C3_COUNTER_SELFTEST pass=3 fail=0` (`complete`, `missing_one`, `extra_stale`).

---

## 4. Assimilation check (status only; nothing adopted)

```
$ ls -la /home/vgpnk/Projects/shokuknow/merge/mori/
MERGE-REPORT.json 35006  MERGE-REPORT.md 20896  SOURCES.append.md 154847
amendments/  knowledge/                              (all mtime Oct 24 23:33)
$ find /home/vgpnk/Projects/shokuknow/merge/mori -type f | wc -l   -> 83
$ du -sh /home/vgpnk/Projects/shokuknow/merge/mori                 -> 592K
```

The staged package is still there, unchanged since 2026-10-24. The fleet L0 record still holds
the collision, and **no later mori L0 line closes it**:

```
$ grep -n 'mori' /home/vgpnk/Projects/shokunin/.ufo/l0-questions.md | grep -E 'merge/mori|round-61'
210:mori | round-61 | merge/mori staged ids (136 rows, S471+) collide with 94 live registry ids
    (extraction 0-3-space-tolerant per CORPUS census clause; collisions at
    mori-shokunin/.ufo/waves/round-61/assimilation/collisions, freeze 7370a731) — a renumber map
    keyed by document URL is needed before any adoption; mori adopts nothing this round.
211:mori | round-61 | merge/mori staging mass id drift: 94/136 staged ids (S471-S564 contiguous)
    collide with the lane registry; ... renumber the staged package upstream ... or authorize
    per-document id re-pointing at adoption time? mori adopted nothing this round.
```

Lane-side corroboration that the ids were *not* adopted: `corpus/SOURCES.md` already owns `S471`
("proc(5) 日本語訳 … docs/A") and `S564` ("mori round-59 w1 sentinel report Mo59Sentinel58 —
own-work/B"), i.e. different documents under the same ids. Status: **staged, blocked on the r61
L0, nothing adopted.** The round-80 contract's "Assimilation: `merge/mori/` stays closed behind
the round-61 L0 (94/136 id collisions)" is consistent with the record. No action taken.

---

## 5. What I could not verify (and why)

1. `tools/mori-retention-gate.py --selftest` and `tools/mori-freeze-order.py --selftest` — both
   hard-require `TMPDIR` inside the lane checkout; the round bounds put scratch under
   `/fast/scratch/…`, and the host guard forbids writing lane-side, so their pinned `21/21` and
   `12/12` are **unverified, not red**. If the L1 wants them verified it must run them from a
   lane-side scratch dir it is authorised to write.
2. The graded rows' 43 tally statements were enumerated with a regex; forms I did not model
   (e.g. "selftest 18 in-memory cases", caught only by the added alternative; "`pass=<N>`"
   placeholders) are not counted. The list is a lower bound.
3. `SCORECARD.md:2000` pins `PASS 30/30` for `tools/fixtures/mori-oom-killers/cases-a2.json` —
   a fixture pack, not a tool selftest; I did not execute the fixture driver that would re-run it.
4. `count-c1.py`'s second arm parses the control-receipt capability row; I did not run
   `count-c1.py` at a post-landing revision (no such revision exists yet), only at `d5888922`
   (control receipt: `C1=unmet tool=absent …`).
5. The in-flight worktree measurements in §1.5/§2.5/§3.4 are snapshots of uncommitted bytes that
   peers may still be editing; they are not receipts and must not be quoted as the round's
   after-state.

## 6. My own defects (and how I caught them)

1. **Worktree/entering aliasing.** My first `git status` was clean except round-80 untracked
   files, and I began measuring the *worktree*. Minutes later the same command showed
   `M .ufo/waves/round-79/count-c2.py`, so a "7-arm selftest" I had measured was a peer's
   in-flight work, not the entering bytes. Caught by comparing blob ids:
   `HEAD:…count-c2.py` = `84f15b0a…` vs worktree sha256 `8d7fae14…`. Every entering figure in
   this report is re-derived with `git show d5888922:<path>`; the worktree figures are quarantined
   in the "in-flight" subsections.
2. **Exit codes read from the wrong process.** My first per-tool loop captured `$?` after a
   pipeline ending in `tail`, so `mori-retention-gate.py` appeared to exit 0 while its selftest
   had failed. Caught by re-running with `${PIPESTATUS[0]}` and a bare invocation: rc 2 with
   `SELFTEST retention-gate FAIL 0/21`.
3. **Tally regex over-match.** My first pass reported `count-flagged.py` as a red selftest in a
   graded row; reading `SCORECARD.md:2668` shows the row cites a live run, not `--selftest`, so
   its argparse rc 2 is irrelevant. Corrected before it reached this report's findings.
4. **D79-3 taken at face value first.** I initially looked for the phantom token in the adjacency
   cell because the r79 spot-check asserted it was there; it is not, at `84c6cbc3` or `d5888922`,
   and `git log -S` shows it never was. Caught by grepping the cell itself instead of trusting
   the spot-check's description.
5. **My "unresolved" count is population-narrow.** 194 pointers/3 unresolved is the
   backticked-token population; the sweep's own regex sees 232 pointers. I have labelled it a
   lower bound rather than presenting it as the sweep's population.

## 7. Tooling

No installs, no upgrades, no `pacman` use. `python3` (3.x host), `git`, `sha256sum`, `diff`, `find`
were sufficient.

## 8. Scratch

`/fast/scratch/hyaku/mori-r80/Mo80Sc01Recon` held the census script, the two fixture repos
(`f/repo` for the C2 counter copy, `g/repo` for the C3 PROVINCE copy), the extracted blobs and
the tables above; removed with `rm -rf` before yield.
