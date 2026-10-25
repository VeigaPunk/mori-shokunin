# ScoutSiblings — sibling-overlap scan, round 45 wave 1

Seat: `L1Mori45.ScoutSiblings` (leaf scout). Read-only across the fleet; the only file this seat
wrote is this report. Lane reads at mori `HEAD = 3ad8faaa` (round-45 freeze commit); the contract's
entering tip is `554ff416459c92f0dea9762f834a556df2990187`.

Assignment scope: (1) the two sibling instrument classes found in round 44 — kama's
`tools/gate-registry-check.py` and kumitate's `scripts/gate-mutants.mjs` predicate K43; (2) whether
any lane already holds the cgroup `memory.events` vs `memory.events.local` distinction or the
"census row must name its level" rule; (3) report scope held.

---

## 1. Gate-registry auditors

### 1.1 kama `tools/gate-registry-check.py` (385 lines, last touched round 34)

**Population — git-derived, not caller-supplied.** There is no `--audit <path>` flag; the whole
population comes from git, and the `--rev` flag switches working tree to committed bytes:

```python
# kama-shokunin/tools/gate-registry-check.py:105-118
def tracked_counters(root: str, rev: str | None) -> tuple[list[str] | None, str]:
    if rev is None:
        rc, out, err = run_git(root, ["ls-files", "-z"])
    else:
        rc, out, err = run_git(root, ["ls-tree", "-r", "-z", "--name-only", "--full-tree", rev])
    ...
    return sorted(p for p in paths if COUNTER_RE.match(p)), ""
```

The population is then **narrowed by regex** to round counters only:

```python
# :67-69
COUNTER_RE = re.compile(
    r"^(?:\.ufo/waves/round-[^/]+/count-[^/]+|tools/round[0-9]+-[A-Za-z0-9._-]+)\.py$"
)
```

**Does it read every table? No — it hard-codes a 5-cell header shape.** `registry_rows()` walks
every `|` block but admits a block only when `len(hdr) == 5` with positional token tests:

```python
# :166-176
if (len(hdr) == 5
        and all(set(s) <= set(":- ") for s in sep)
        and hdr[0].lower() == "name"
        and ("kind" in hdr[1].lower() or "entry" in hdr[1].lower())
        and "exit" in hdr[2].lower()
        and ("self-test" in hdr[3].lower() or "selftest" in hdr[3].lower())
        and "write" in hdr[4].lower()):
```

Measured, by importing kama's own function unmodified (`Spec` loader, kama's file untouched):

```
$ python3 - <<'EOF'   # imports kama tools/gate-registry-check.py, calls registry_rows()
kama: rows_matched=22 five_cell_lines=34
mori: rows_matched=0  five_cell_lines=1
EOF
RC=0
```

kama's own `SKILL.md` carries **19** registry-like headers in two shapes — 6 five-cell and 13
seven-cell (`| Name | Kind / entry command | Verdict map | Self-test | Pinned values | Write scope
| Owner |` at `:396,430,470,495,533,570,652,699,739,783,818,866,886`) — so kama reads its 5-cell
subset and silently skips its 13 seven-cell tables. Against mori's seven 8-cell tables it reads
**zero**.

Counted: `grep -nE '^\| *(Name|name) *\|' SKILL.md | awk -F'|' '{print NF-2}' | sort | uniq -c` →
`6 5` / `13 7`.

**Attribution — substring fallback, no `row='<name>'`.** This is precisely the fallback P-C2 arm 2
forbids:

```python
# :184-186
matched = [r for r in rows if any(path in c for c in r)]
if not matched:
    unregistered.append(path)
```

Any cell containing the path string counts, and the label is only a sort key
(`row = sorted(matches, key=lambda r: len(r[2]))[0]`), printed as `row %r` only in the *good* branch,
never as `row='<name>'` on an unregistered/defective path. No `duplicate=` counter exists in the
file at all.

**`--selftest` branch — real for the instrument, absent as a row predicate.** kama's own argv branch
is genuine (`add_argument("--selftest", action="store_true")` → `return selftest()`), with five
`arm(...)` fixtures (valid-row, thin-row, empty-exit-map, missing-path, prose-only) plus a lane-tip
arm — six checks, `grep -c 'arm("'` = 5 plus the lane-tip block. But the audit never inspects the
*row's* self-test cell for a real branch: row[3] is scanned only for cited paths
(`for c in (row[1], row[3], row[4])`). A row whose self-test cell names `--selftest` only inside a
comment passes kama.

**Write scope — no fixture comparison.** row[4] is path-existence-checked, nothing else; there is no
`writescope_mismatch` and no `fixtures/write-scope.json` in kama.

### 1.2 kumitate `scripts/gate-mutants.mjs` — K43 (1294 lines)

**K43 is a kill-determinism predicate, not a registry predicate.** It contains no `SKILL.md`
reader; it never opens a registry table. Quoted from the header:

```
K43: a mutant is KILLED iff its run is evaluable (no timeout, no overflow, clean process group,
no spawn error, a parseable case summary whose total equals the control's), the selftest exits
with a numeric non-zero status, stdout carries the exact line `VERDICT: FAIL`, and an immediate
second run of the same mutated bytes meets the same conditions with the same sorted FAIL case
names.
```

**Population — git tree at `--rev`, frozen target set, no caller-supplied paths.**

```javascript
// :743
const tree = gitRun(repo, ['ls-tree', '-r', '-z', '--full-tree', resolved, '--', 'scripts'], ...)
// :781-782
const rev = opts.rev ? loadRevisionScripts(opts.repo, opts.rev, tempRoot, scripts) : 'working-copy';
if (!opts.rev) copyScriptTree(join(opts.repo, 'scripts'), scripts);
```

`--target` is validated against `TARGETS = Object.freeze(['cite-check', 'wave-census'])`; the mutant
population is `MANIFEST` — 43 entries, of which 41 are the frozen ids and 2 are declared extras
(`guard-outer-ne-1`, `guard-outer-eq-undefined`) — checked against `FROZEN_IDS` (41).

**Duplicate detection exists — over mutant ids, not registry rows.** `manifestIssues()` marks
repeated `target:id` strings (`const duplicates = ids.filter((id, index) => ids.indexOf(id) !== index)`),
and `manifestExitCode()` returns 2 with `DUPLICATE_IDS ...` printed.

**Real `--selftest` argv branch — both for itself and for its targets.** Its own branch is parsed at
`:298` (`else if (arg === '--selftest') opts.selftest = true;`) and dispatched at `:1184`
(`if (opts.selftest) return runSelftest();`). For each target it does not grep text; it **executes**
the branch:

```javascript
// :415
const child = spawn('/usr/bin/prlimit', [
  `--nproc=${processLimitForCurrentUid()}`, '--', process.execPath,
  '--require', parentGuard, '--max-old-space-size=128', file, '--selftest',
], { ... detached: true, ... });
```

and judges numeric exit + exact `VERDICT: FAIL` + stable FAIL-name set on a second run. That is
strictly stronger than an argv-branch *reading*.

### 1.3 Overlap map against mori's six frozen C2 arms

| P-C2 arm | kama | kumitate K43 | held by a sibling? |
|---|---|---|---|
| 1. every table read, `tables=<n>` | reads every **5-cell** table only; no `tables=` counter; 0 rows on mori's 8-cell shape | no table reader | **no** (shape-locked, uncounted) |
| 2. attribution to the naming row, printed `row='<name>'`, no substring fallback | substring in any cell (`any(path in c for c in r)`) | n/a | **no — this is the arm kama violates** |
| 3. `duplicate=0` over registry names | absent | duplicate ids over the 43-entry mutant manifest only (41 frozen + 2 extras) | **mechanism yes, domain no** |
| 4. row's self-test counts only with a real argv branch (comment excluded) | own branch real; row's self-test cell never checked | executes `--selftest` and judges exit/stdout (K43) | **mechanism yes (kumitate), registry-row predicate no** |
| 5. whole population `unregistered=0` and `no_selftest=0` | counters only (`COUNTER_RE`), no `no_selftest` counter | n/a | **partial (subset, no second counter)** |
| 6. `writescope_mismatch=0` against `fixtures/write-scope.json` | absent; no fixture | absent | **no** |

So: **no sibling holds the C2 conjunction, and for arms 1 and 2 the sibling is the counter-example,
not the precedent.** What is borrowed-adjacent and must be named rather than claimed as new:
git-sourced population at `--rev` (kama `:105-118`, kumitate `:743`), multi-table block walking
(kama `registry_rows`), duplicate-id detection (kumitate `manifestIssues`), and runtime `--selftest`
evidence (kumitate K43 spawn at `:415`).

Mori's own instrument at HEAD is the third data point, and it is worse than both on arm 4:
`tools/mori-gate-registry.py:146` is a byte-substring test —

```python
if b"--selftest" not in body:
```

— which is exactly the r44 false positive, and its population is caller-supplied (`--audit <path>`).
The class is live at HEAD: a scan of `tools/*.py` and `tools/*.sh` (29 files mention `--selftest`)
finds one file whose only occurrence is a comment:

```
$ grep -n -- '--selftest' tools/mori-silence-cases.sh
20:#   Each case runs the actual census CLI (bash "$CENSUS", no --selftest) and
RC=0
```

## 2. Level-naming ground (`memory.events` vs `memory.events.local`)

Command run (read-only), as assigned:

```
$ grep -rln 'events\.local' --include='*.md' --include='*.py' --include='*.sh' --include='*.mjs' \
    --include='*.json' */ | grep -v '/\.git/'
```

**The distinction is already held, in two lanes, and already mined in mori.** `grep -c 'events\.local'`
over every `*/SKILL.md` in the fleet returns **0 for all of them** — no lane's SKILL states it.

- tsukuroi `corpus/knowledge/oom-event-plane.md:233` tabulates both files per cgroup path
  (`memory.events` oom_kill / oom / sock_throttled against `memory.events.local` oom_kill), and
  `:248` reads the two levels to date a kill wave.
- tsukuroi `corpus/knowledge/memory-arm-mutants-s8.md:53` carries a **defect exactly of the
  level-naming class**: `@defect D5 | memory.events.local merged into the .events presence count |
  @old *.local) localp=$((localp + 1)) ;; / @new *.local) present=$((present + 1)) ;;` — a mutant
  that must be killed. `memory-arm-ver-s8.md:61` sweeps both names in one `find`.
- mori's own corpus holds it in at least seven entries: `oom-evidence-loss-r38.md:45`
  ("`memory.events` counts a cgroup **and its descendants**, `memory.events.local` counts only the
  cgroup's own events"), `journal-alarm-routing-r14.md:35`, `observability-census-r1.md:135`,
  `observability-surfaces-r2.md:206`, `oom-kill-counter-kernel-only-r12.md:6`,
  `userspace-oom-killers-r12.md:1`, and — missed by the `events.local` grep — `surfaces-r7.md:88-90`,
  which names the *row's* two counters by field: "the bare `oom_kill=` is still the parent cumulative
  counter, and the session-service reading is printed next to it as `local_oom_kill=` (`:754`)". The
  assigned `grep -rln 'events\.local'` therefore undercounts: the level distinction is already in the
  census row's own field names, not only in prose. `grep -rl 'local_oom_kill' corpus/` returns four
  knowledge entries (surfaces-r2, surfaces-r7, audit-r11, census-cgroup-levels-r45).
- The distinction is also **already admitted and mapped**: `oom-evidence-loss-r38.md` carries
  `source: S232…S241`, `verified-at:`, `recheck:`, and `corpus/README.md:611` maps it; registry
  rows `S002` and `S232` are both `mined` with `used-by` naming the entries (S002 →
  `oom-kill-counter-kernel-only-r12.md, userspace-oom-killers-r12.md, journal-alarm-routing-r14.md`;
  S232 → `oom-evidence-loss-r38.md`). `tools/mori-census.sh:1705` already selects
  `LOCAL_EVENTS=${MORI_CGROUP_LOCAL_EVENTS:-${CGROUP_EVENTS%.events}.events.local}`.
- kama holds it only as a round-16 cross-lane advice file (`.ufo/waves/round-16/build/advice/ConnectMori.md`),
  not as knowledge.

**The rule "a census row must name its level" is held by no lane.** Greps for
`census[^.]{0,80}level|level[^.]{0,80}census`, `name( its|s the)? level`, `must name` across
`*/corpus/` and `*/SKILL.md` return no cgroup-level census rule. Closest extant prose, and the
honest ceiling of it:

- mori `oom-evidence-loss-r38.md:73-75` — "report a *pair* (`memory.events` delta,
  `memory.events.local` delta) rather than a single 'was there an OOM' bit".
- tsukuroi D5 (above) — a killed mutant, not a stated rule.

So C3's theme splits: the **distinction is prior art in mori's own corpus** (and tsukuroi's), while
the **attribution rule** — each census row names the level it reads — is unclaimed. A C3 report that
presents level naming as new ground would overstate. The entry as landed does not: see the addendum,
where it cites the S002-grounded prior art and claims only the rule.

## 3. Report scope held

- **No sibling tool imported into the lane.** `grep -rln 'kama-shokunin\|kumitate-shokunin\|tsukuroi-shokunin' tools/`
  returns nothing; `SKILL.md` names those lanes only as refusal provinces (`:349-350`, `:671`).
  The kama function was imported **in a scratch process only** (`.ufo/waves/round-45/tmp/ScoutSiblings`)
  to measure its reader; nothing was copied into `tools/`.
- **No sibling file edited.** Every command against `kama-shokunin/`, `kumitate-shokunin/` and
  `tsukuroi-shokunin/` was `git log/show/status`, `grep`, `read`, or `sed -n`. `git -C tsukuroi-shokunin
  status --porcelain` is empty; kama and kumitate show modifications that predate this read
  (`round-35` seat logs, `.ufo/pins/*`, `corpus/QUALITY.md`) and were not made by this seat.
  Lane-side, the first `git status --porcelain` showed only untracked `round-45/` wave directories;
  a later re-check shows the two executing seats' tracked edits (`tools/mori-gate-registry.py`,
  `tools/mori-round19-regressions.py`) and the new corpus entry, none of them this seat's.
- **No cross-domain claim absorbed.** K43's kill-determinism conditions, tsukuroi's D5 mutant and
  kama's counter registry are reported as adjacency; none is asserted as a mori result.

---

## Affected axes

- **calibration 5** (C2's axis) — primary: the overlap map decides which of the six arms can be
  claimed as new and which are precedents that must be cited.
- **depth 5** (C3's axis) — secondary: the level-naming distinction is prior art; only the
  attribution rule is unclaimed.
- **operability 7** (C1) — untouched; nothing here bears on revision-sensitive ledgers or witnesses.
- coverage, freshness, adjacency — not claimed.

## Proposed move (one, bounded)

**Shape-dispatch the table reader and print `tables=<n>`, then make arm 4 a code-token test rather
than a byte-substring test.** Concretely: read the committed `SKILL.md` at `--rev`, admit every block
whose header is the eight standard cells (mori HEAD: **7 tables, 43 rows** — 162/23, 524/2, 588/1,
643/2, 718/3, 796/1, 881/11), print the count, attribute each audited path to the row whose *name*
cell matches and print `row='<name>'`, and count `--selftest` occurrences only where the token is an
argv element in code (rejecting `tools/mori-silence-cases.sh:20`, comment-only) — the mechanism
kumitate's K43 demonstrates in its strongest form (execute and judge) without adopting its cost.

This is a synthesis, not an import: kama supplies git-population-at-`--rev` and block walking but is
the counter-example for arms 1–2; kumitate supplies duplicate-id detection and runtime self-test
evidence but has no registry reader; mori's `b"--selftest" in body` supplies the defect the arm
exists to kill.

## Risks

1. **Spawning `--selftest` on every declared tool is not free and not safe here.** K43 does it in a
   detached process group with an allowlisted env and a write-free temp copy. A C2 audit that
   *executes* each registry row's self-test would run lane tools during a read-only wave; the arm
   therefore has to be a static argv-token check, and the report should say so rather than implying
   K43-grade runtime evidence.
2. **A shape-locked reader is the exact defect being audited.** If the new reader also pins one
   width (kama's `len(hdr) == 5`), it repeats the error inverted. `tables=<n>` must be printed so a
   silently dropped table is visible, and the selftest must include a mutated-header arm.
3. **Whole-file duplicate detection may collide with section-scoped reuse.** P-C2 arm 3 says a name
   occurring twice is a finding, so duplicates are counted across all 7 tables; if any legitimate
   row name is reused across sections, the arm will fire. That is a contract consequence, not a bug,
   but the executor should quote the contract before "fixing" it.

## Verification (run here; commands and exit codes)

| check | command | result |
|---|---|---|
| kama reader against both trees | import `registry_rows`, feed `git show HEAD:SKILL.md` for kama and mori | kama 22 rows; mori **0 rows**; rc=0 |
| mori table census at HEAD | block walker over `git show HEAD:SKILL.md`, 8-cell headers | `tables= 7`, rows 23/2/1/2/3/1/11; rc=0 |
| comment-only `--selftest` at HEAD | scan `tools/*.py`+`tools/*.sh` for comment-only occurrences | 1 file (`mori-silence-cases.sh:20`); rc=0 |
| `events.local` in SKILL.md | `grep -c` over every `*/SKILL.md` | 0 in all lanes |
| lane write scope | `git status --porcelain` in mori | only untracked `round-45/` dirs |
| sibling write scope | `git -C <sibling> status --porcelain` | tsukuroi empty; kama/kumitate pre-existing mods, none from this seat |

No tool install or upgrade was performed this seat.

---

## Copy-paste Markdown for the L1 (name the overlap; do not claim novelty)

```markdown
### Overlap, named (round 45)

Two sibling instruments from round 44 bound what C2 can claim as new.

- **kama `tools/gate-registry-check.py`** already derives its population from git
  (`git ls-files`, or `git ls-tree` at `--rev`) and walks registry blocks — but only blocks whose
  header is five cells (`len(hdr) == 5`, kama `:166`). Measured with kama's own reader: 22 rows in
  kama's `SKILL.md`, **0 rows in mori's** (all seven of mori's tables are eight cells). Its
  attribution is the substring fallback P-C2 arm 2 forbids (`any(path in c for c in r)`, `:184`),
  it has no `duplicate=` and no `tables=` counter, and it never inspects a row's self-test cell.
- **kumitate `scripts/gate-mutants.mjs` K43** is a kill-determinism predicate, not a registry
  auditor: no `SKILL.md` reader at all. It contributes two mechanisms — duplicate-id rejection over
  a 43-entry manifest, 41 frozen (`manifestIssues`, exit 2) and *executed* `--selftest` evidence
  (spawn at `:415`, numeric exit, exact `VERDICT: FAIL`, stable second run). Both are mechanisms in
  another domain, not C2 results.
- **This lane's own** `tools/mori-gate-registry.py:146` tests `b"--selftest" in body`, the exact r44
  false positive; the class is live (`tools/mori-silence-cases.sh:20` carries the token only in a
  comment).

C2's conjunction is therefore unclaimed, but four of its mechanisms have prior art and are cited
above; arms 1 (shape-dispatched, counted `tables=<n>`) and 2 (`row='<name>'` attribution) are
defended by the sibling counter-example rather than by novelty.
```

```markdown
### Level naming — prior art and the unclaimed rule (round 45)

`memory.events` vs `memory.events.local` is **already held**: tsukuroi
`corpus/knowledge/oom-event-plane.md:233` tabulates both per path and `:248` dates a kill wave from
the two levels; tsukuroi `memory-arm-mutants-s8.md:53` carries a killed mutant (D5) that merges
`.local` into the `.events` presence count. This lane's own corpus holds it in six entries —
`oom-evidence-loss-r38.md:45` states the descendant-vs-own semantics, `journal-alarm-routing-r14.md:35`
states the local counter cannot substitute, `surfaces-r7.md:88-90` already names the row's two
counters by field (`oom_kill=` parent cumulative, `local_oom_kill=` session-service), and
`corpus/README.md:611` already maps the r38 entry (`S002` and `S232` are `mined` with `used-by`
naming the entries). `tools/mori-census.sh:1705` already selects the `.events.local` path.

Not held by any lane, and the only honest novelty: **the rule that a census row must name the level
it reads.** Closest extant prose is r38's "report a *pair* … rather than a single bit"
(`oom-evidence-loss-r38.md:73-75`). The round-45 entry does name its prior art — see the addendum
below — so the distinction stays cited and only the rule is claimed.
```

---

## Addendum — concurrent landing observed at 07:45–07:47 (worktree, uncommitted)

Between the HEAD measurements above and this write, two executors landed working-tree edits. Both
were read, neither edited.

**C2 executor, `tools/mori-gate-registry.py` (+447/−155).** The design matches §"Proposed move": the
new docstring declares the stance explicitly —

```
:7  wherever it sits in the file; a table with a different header is not a registry
```

— `parse_tables()` admits only `is_standard_header(split_row(...))` blocks (`:178`, `:192`), the
summary prints `tables=%d` (`:590`) and the counter line carries
`registered=… unregistered=… no_selftest=… duplicate=… wrong_row=… tables=…` (`:592`), and the
self-test is judged by a `selftest-flag`/argv-token parse (`FLAG_DECL`, `selftest_flag(body, entry,
flag)`) rather than `b"--selftest" in body`. No spawn: the K43 cost risk is avoided.

**One residual, second-order to arm 1:** `tables=<n>` is printed, never asserted. Because a table
whose header deviates stops being a registry table *by declaration*, a header regression removes a
table from the population while `unregistered=0` still holds and `tables` merely drops 7→6. P-C2
arm 1's wording — `tables=<n>`, not 1 — is satisfied by any n ≥ 2, so a single-header mutant would
still print `C2=met`. The frozen kill-rule set has no table-drop witness. This is a predicate
consequence to record for round 46, not a patch here.

**C3 executor, `corpus/knowledge/census-cgroup-levels-r45.md` (new).** It grounds on a source this
lane opened — `S473`, linux v7.2 `cgroup-v2.rst`, sha256 `a9433bb0…` — and it **names its prior art**
in a §"What is already held":

```
:36  surfaces-r7.md:88-90 already holds the row's two counters …
:37  oom-kill-counter-kernel-only-r12.md:12 already holds the local-vs-hierarchical distinction from
     S002. That the two files differ is **not** new here; what is new is that this row's fallback can
     break the distinction its own field name …
```

That is stricter than §2 above required, and it sharpens the finding beyond both lanes' corpora: the
level mislabel is in **this lane's own code**. `tools/mori-census.sh:1862` prints one surface name
over two counters, and the fallback at `:1710-1711` fills `local_oom_kill` from the *service's
hierarchical* `memory.events` while keeping the word `local`. So the "census row must name its
level" rule is not an abstract import from tsukuroi — it is violated at a measurable line in mori.

