# CritPredicates — round-44 P-C1/P-C2/P-C3 falsification (wave 1, pre-after-measurement)

Role: UFO-FSD critic. Instruments frozen at `7cb59c6891d4f5d0266fe062565f094da835dc84`; all ten
sha256 pins in `evidence/freeze-r44.txt` were re-verified byte-identical before any probe (§6.5).
Every counter run below is read-only against the lane; every adversarial ledger, mutant and stub
counter was built in a fresh `mktemp -d` sandbox (`/tmp/critpred-cro_k032`) and never in the lane.
No frozen instrument, `SKILL.md`, `SCORECARD.md`, `LOG.md` or `corpus/` byte was edited. A defect
reported here is not a fix: per the contract's Freeze paragraph the corrections in §7 are routed
to round 45.

## 0. Verdict summary

| Predicate | Axis claimed | Verdict | Reason |
|---|---|---|---|
| P-C1 | calibration | **narrow** | The code measures ledger self-consistency, not the report's figures. Twelve rows over paths that do not exist, each asserting `0`, print `C1=met mismatches=0`. |
| P-C2 | operability | **reword** | The audited set is caller-supplied: `C2=met` prints with one of the round's three counters, and it already prints at the freeze commit. A fabricated tally plus a "mutant" that disables nothing both pass. |
| P-C3 | coverage | **reword — unattainable as instrumented** | `census_ok` is structurally red (staged copy makes every `used-by` an E11): `C3=met` cannot print at any revision. The novelty clause is falsified by ground the lane already held, and the axis attribution is contradicted by the lane's own admitted round-31 ruling. |

The single most consequential finding: **P-C3's after-state is unreachable.** Whatever the round
lands, `python3 .ufo/waves/round-44/count-c3.py <landed tip> --entry … --row S471 --row S472`
prints `census_ok FAIL (exit=1)` and `C3=unmet`, exit 1. Evidence in §3.2.

---

## 1. P-C1 — figure reconciliation (calibration 5)

### 1.1 (a) The exact condition the counter's code evaluates

`count-c1.py:124-162` (`evaluate`) returns met iff all five `record()` checks pass:

| Check | Code condition |
|---|---|
| `ledger_present` | `git cat-file -e <rev>:<ledger>` succeeds (worktree file when `rev == "WORK"`) |
| `rows_parse` | every non-blank, non-`#` line splits into exactly 4 TSV cells; id matches `^F\d{2,3}$`; asserted matches `^\d+$`; class ∈ {registry, evidence, wave, corpus, checks}; command starts `git `, its second word ∈ {show, grep, ls-tree, rev-list, cat-file, log, diff}; contains `@REV@`; contains neither `;` nor `&&`; does not match `\b(echo|printf|true)\b` |
| `row_floor` | `len(rows) >= --min-rows` (default 12) |
| `class_floor` | `len({distinct class labels}) >= --min-classes` (default 4) |
| `commands_reconcile` | per row: `bash -c "<cmd, @REV@→rev> 2>/dev/null \| head -c 64"` exits 0, its stripped stdout matches `^\d+$`, and the integer equals the asserted value |

`C1=met mismatches=0` is printed iff `fails` is empty (`main`, :336-340).

Gaps between the frozen English and that code:

| Frozen sentence | Code | Gap |
|---|---|---|
| "one row per numeric assertion the round report makes" | no report input; `argparse` has `rev, --repo, --ledger, --min-rows, --min-classes, --timeout, --selftest` only | the report is never read; a ledger may omit every figure the report states and still pass |
| "about a committed artifact class" | `cls` is a free-text label chosen by the author | labels are never bound to what the command reads (demonstrated: 12 rows all reading one file, labelled with four classes → `class_floor PASS`) |
| "each row's command is a single `git` pipeline over `@REV@`" | prefix/verb/`@REV@`/`;`/`&&`/three banned words | `git diff @REV@` compares rev→**worktree**; `$(cat …)`, `$(date …)`, `$(curl …)` are legal |
| "executes every row at the measured revision" | `run_row(repo, cmd_rev or rev, …)` | true for a revision; `WORK` mode accepts an **uncommitted** ledger and runs rows at the tip |
| "every row's recomputed value equals its asserted value" | pipeline rc + integer equality | `git show @REV@:<absent> \| wc -l` exits 0 and prints `0`: absence is scored as a number |
| "at least 12 rows … at least 4 of the declared classes" | defaults 12 / 4, both CLI-overridable | the floors are not invariants: `--min-rows 1 --min-classes 1` → `C1=met` with one row |

### 1.2 (b) Cheapest do-nothing state, and reachability

**Ghost ledger** — twelve rows over paths that do not exist at the revision, each asserting `0`:

```
F01	0	registry	git show @REV@:no/such/path-1.md | wc -l
…
F12	0	corpus  	git show @REV@:no/such/path-12.md | wc -l
```

Observed (sandbox `l`): `ledger_present PASS`, `rows_parse PASS (12 rows)`, `row_floor PASS`,
`class_floor PASS`, `commands_reconcile PASS (all rows match)` → **`C1=met mismatches=0`, exit 0**,
while `git cat-file -e <rev>:no/such/path-1.md` returns 128 (absent). No committed byte is read and
no report figure is asserted. Reachable in this round: **yes** — one commit of
`.ufo/waves/round-44/figures.tsv`, no other work.

Two cheaper/nearer variants, also observed:

- 12 identical rows (`git show @REV@:data.txt | grep -c x`, asserted 3) with the four class labels
  cycled → `C1=met`. This is the tautology at the heart of the check: the author derives each
  asserted value with the same command, so reconciliation can only fail if the bytes move.
- one row plus `--min-rows 1 --min-classes 1` → `C1=met` (with defaults the same ledger prints
  `C1=unmet mismatches=0`, which is honest but confusing: a floor failure is reported with
  `mismatches=0`).

### 1.3 (c) Universal / unmeasurable clauses

- "one row per numeric assertion the round report makes" — a universal over the report's text; the
  report does not exist at freeze and the counter has no input for it. Unmeasurable by construction.
- "a committed artifact class" — the five classes are labels, not artifact classes; nothing prevents
  a `corpus` label on a row that reads `.ufo/waves/…`.

### 1.4 (d) Axis attribution — calibration: correct

`AXES.md`: calibration = "Self-assessment quality: gaps named honestly, confidence graded, overreach
caught. SHONEN.md/SCORECARD entries match observed repo state." A ledger that re-derives reported
counts from committed bytes is exactly an "overreach caught" instrument, and the routed r43 defect
(`15 checks` observed 14; `34 seat logs` observed 8) is an overreach. Keep the axis. Caveat: the
counter measures the ledger, not `SHONEN.md`/`SCORECARD.md`; the axis move is only as strong as the
ledger's coverage of the report's figures, which is the unmeasured clause above.

### 1.5 (e) Causal separability

C1 does not require C2 or C3 to be *met*: everything it can read (corpus registry, gates table, wave
dirs) exists at the entering tip and at the freeze commit. But the class floor pushes the author
toward `registry`/`corpus` rows, and the natural corpus row is the C3 entry. Demonstrated: a ledger
whose twelfth row is `git show @REV@:corpus/knowledge/pid-probe-conclusion-r44.md | wc -l` asserted
`1` prints `C1=unmet mismatches=1` before that file lands and `C1=met` after it lands. The
contract's "No claim's verification depends on another claim having landed" is therefore not
enforced; it holds only if the ledger avoids C3-owned paths. Smallest correction: a ledger rule that
rows may read only artifacts C1 owns (the report, the ledger, wave evidence), or an explicit
coupling declaration.

### 1.6 Verdict — **narrow**

Reason: the sentence promises report coverage the code cannot see, and the code's own five checks
are satisfiable without reading a single committed byte. Narrow the sentence to what is measured
("a committed ledger of ≥12 single-`git`-pipeline rows reconciling at the revision, with ≥4 distinct
class labels"), or add the missing `--report` input and row→assertion map. Separately close the
three grammar holes (producer failure masked by `| wc -l`, `diff`/command substitution reading
non-committed bytes, `WORK` accepting an uncommitted ledger).

---

## 2. P-C2 — gate-standard conformance (operability 7)

### 2.1 (a) The exact condition the counter's code evaluates

`count-c2.py:112-186` (`evaluate`) returns met iff all five checks pass:

| Check | Code condition |
|---|---|
| `counters_present` | each `--counter` path exists at the rev |
| `registry_rows` | `tools/mori-gate-registry.py --rev <rev> --repo <repo> --audit <c1> … --audit <cn>` exits 0 and its stdout contains `REGISTRY=met` for the whole list |
| `tool_selftest` | the auditor's `--selftest` exits 0 and its **last** `pass=N fail=M` has `M == 0` and `N >= 4` |
| `selftest_tally` | each counter materialized from the rev, run `--selftest`, exits 0 and its **last** `pass=N fail=M` has `M == 0`, `N >= --min-arms` (default 2) |
| `mutant_kill` | `<mutants-dir>/<basename>` materialized from the rev, run `--selftest`, exits **1** with `M >= 1` |

The auditor (`tools/mori-gate-registry.py:96-142`) itself checks only: a `## Gates` table row whose
entry cell *invokes* the path (`entry_names`, with a fallback `base in r[2] or name in r[2]`), the
eight named cells non-empty after header mapping, `git cat-file -e <rev>:<path>`, and the literal
string `--selftest` in the tool's bytes.

Gaps:

| Frozen sentence | Code | Gap |
|---|---|---|
| "Each of the round's counters" | the set is the `--counter` argument list | nothing in committed bytes declares the round's counter set; `C2=met` prints with one counter (observed at the freeze tip) |
| "a row whose entry cell names its repo-relative path" | `entry_names` then fallback substring match | a row for a **different** gate that merely passes the path as an argument registers it (observed: one row made both `tools/fx-one.py` and `tools/audit.py` `REGISTRY=met`) |
| "eight standard cells … non-empty" | non-empty only | no cell semantics (`kind` may say anything); header names must match exactly or every cell reads as missing |
| "the named path resolves at the measured revision" | `git cat-file -e` | faithful |
| "`--selftest` runs over isolated fixtures and prints a `pass=/fail=` tally with fail 0" | exit code + last tally string | isolation and assertion execution are invisible; a stub printing `FIX_SELFTEST pass=2 fail=0` passes |
| "a committed mutant … whose one check is disabled, is caught by that counter's own selftest" | any file at the mutants path whose `--selftest` exits 1 with fail ≥ 1 | no byte relation to the counter is required; a stub that shares no code and disables no check is "killed" |
| "prints `C2=met` only when every one of those holds" | true of the five checks | the kill rule "A counter that prints `C2=met` from a registry row alone fails `selftest_tally` and `mutant_kill`" is **not** enforced: a counter that fabricates its tally passes both |

The shipped mutants *are* honest one-line disables (verified by diff: `row_floor→True`,
`mutant_kill→True`, `census_ok→True`). The defect is that nothing binds a mutant to its counter, so
the property is unverifiable in general.

### 2.2 (b) Cheapest do-nothing state, and reachability

**Already reached at the freeze commit.** At `7cb59c68`, with the round's three counters and the
round's mutant directory:

```
check counters_present   PASS (3 counters)
check registry_rows      PASS (REGISTRY=met)
check tool_selftest      PASS (pass=6 fail=0)
check selftest_tally     PASS (count-c1.py pass=6; count-c2.py pass=5; count-c3.py pass=6)
check mutant_kill        PASS (count-c1.py killed (fail=1); count-c2.py killed (fail=1); count-c3.py killed (fail=1))
C2=met   exit 0
```

So a data wave that does nothing passes C2. The claim's move is the instrument commit itself, which
the round made before wave 1; the after-measurement at the landed tip is a re-run, not a new
measurement, and cannot discriminate.

The same three-counter run with the **default** `--mutants-dir fixtures/mutants` (repo-root-relative,
but the mutants live under `.ufo/waves/round-44/fixtures/mutants`) prints
`mutant_kill FAIL (… mutant absent)` → `C2=unmet`, exit 1. The After line must pass
`--mutants-dir .ufo/waves/round-44/fixtures/mutants`.

Cheapest state that meets the code alone (sandbox `e`, `f`): one stub counter whose `--selftest`
prints a tally it does not earn, plus a "mutant" that is a lying stub → **`C2=met`**. With
`--min-arms 0`, a counter whose selftest prints `pass=0 fail=0` (no assertions at all) → **`C2=met`**.

Reachability in this round: **yes, now**; no round work is needed.

### 2.3 (c) Universal / unmeasurable clauses

- "Each of the round's counters" — universal over a set that exists nowhere in committed bytes.
- "runs over isolated fixtures" — unmeasurable from a tally string.
- "whose one check is disabled" — unmeasurable: no diff or byte relation is checked.

### 2.4 (d) Axis attribution — operability: correct, with a caveat

`AXES.md`: operability = "Runnable artifacts: checklists that are executable, commands that exist,
scripts that run. A checklist item can be run and produces the stated outcome." Registry row +
resolvable entry + selftest + mutant is a runnable artifact with a stated outcome; the lane's
round-38 correction already re-attributed a C2-shaped claim to operability. Caveat: the mutant-kill
clause is a test-effectiveness property (calibration-shaped); it rides on operability only because
the "stated outcome" is the selftest verdict — and that verdict is exactly what the counter cannot
see. Not a mis-attribution, but the strongest clause is the unverified one.

### 2.5 (e) Causal separability

Independent of C1 and C3: the counters and the auditor are frozen instruments present at the freeze
commit; no C1/C3 byte is read. Observed: `C2=met` at `7cb59c68` with no `figures.tsv` and no entry.
Separable — but pre-satisfied (§2.2).

### 2.6 Verdict — **reword**

Reason: the universal over "the round's counters" is not in the artifact; the tally and mutant
clauses are satisfiable by unearned strings; the contract's After line (`count-c2.py <landed tip>`)
omits `--counter` and exits 2 (observed), and the default mutants dir makes the honest three-counter
form fail. Reword to a caller-declared set with a committed declaration, require the mutant to be a
byte-diff of its counter (reviewer-verified, since a text tally cannot establish it), and fix the
After invocation.

---

## 3. P-C3 — pid-probe conclusion ground (coverage 6)

### 3.1 (a) The exact condition the counter's code evaluates

`count-c3.py:84-160` (`evaluate`):

| Check | Code condition |
|---|---|
| `entry_present` | the entry path exists at the rev |
| `entry_meta` | entry text contains `verified-at:` and `recheck:`; every `--row` id appears as `^source:\s*(S\d{3,})`; `coverage-map:` is present and the `--coverage-map` string occurs in the first line after the first `coverage-map:` |
| `rows_present` | in `corpus/SOURCES.md` at the rev, each `--row` id has cell 7 == `mined` and cell 10 contains the entry path |
| `census_ok` | `bash <census> validate --file <tmp>/SOURCES.md` (cwd = repo) exits 0 |
| `readme_row` | the entry path bytes occur **anywhere** in `corpus/README.md` |

Gaps:

| Frozen sentence | Code | Gap |
|---|---|---|
| "one **admitted** knowledge entry" | no admission marker is read | admission is a closure verdict, never checked |
| "on FR5 ground it **did not hold**" | no novelty check at all | the contract's proxy is `git grep -l 'Z ゾンビ'` — a Japanese literal no English entry would carry; falsified below |
| "the `Z`/`X` process-state alphabet and the three worlds …" | body never read | any body passes (observed: body `body`) |
| "its `source:` ids present as `mined` registry rows whose `used-by` names that entry" | only the `--row` subset is looked up | an entry citing `S999` (not a registry row) passes with `--row S901` (observed) |
| "a `coverage-map:` naming FR5" | substring on one line | `coverage-map: FR5-superseded` passes (observed) |
| "the registry census validates at the measured revision with exit 0" | live fleet script `<repo>/../scripts/sources-census.sh`, not bytes at the revision, not in the freeze pins | unpinned external authority; and the staged invocation is structurally red (§3.2) |
| "`corpus/README.md` carries a frontier-map **row** naming the entry" | any occurrence anywhere | a line in a "Removed / superseded" section passes (observed) |

**The novelty clause is falsified by local evidence.** At the entering tip `1429c791`,
`corpus/knowledge/watchdog-identity-r31.md` already holds, with mined sources:

- `:27` — "`/proc/<pid>/cmdline` reads empty | … unless the process is a zombie, when a read will
  return 0 characters; an empty read gives no identity and is not by itself proof that the process
  exited | unavailable | S170"
- `:29` — "`/proc/<pid>/stat` third value (state) is `Z` | … `Z (zombie)` is the zombie state | …
  | S167, S171"

and `S171`'s scope cell at the entering tip already names "field 3 state letters (S at :49-50, **Z**
at :56-57, **X** at :69-70)". So the `Z` alphabet, the empty-`cmdline` read and their sources were
held since round 31. The genuinely new bytes are the `X` letter and the retired "swapped out" world
carried by two translations (`S471`, `S472`). The Before sweep measures a language token, not ground.

### 3.2 The blocking defect: `census_ok` is structurally red

`count-c3.py` stages `SOURCES.md` into a fresh temp dir and runs
`census validate --file <tmp>/SOURCES.md` with `cwd = <repo>`. The census resolves a `--file`
target as `dir_abs = realpath(dirname(file)/..)` (`scripts/sources-census.sh:497-502`) and checks
each `used-by` path as `[ ! -e "$dir/$path" ]` (`:566`). For a file in `/tmp`, every repo-relative
`used-by` is looked up under `/tmp`, so **every mined row is E11 and validate exits 1**.

Observed:

| Invocation | Result |
|---|---|
| `bash ../scripts/sources-census.sh validate --file corpus/SOURCES.md` (live) | `file ok /home/vgpnk/…/corpus/SOURCES.md`, **exit 0** |
| the same committed file copied to `$(mktemp -d)/SOURCES.md`, then `validate --file <that>` | 279 `E11 … missing used-by …` lines (298 output lines), **exit 1** |
| `count-c3.py WORK --entry corpus/knowledge/pid-probe-conclusion-r44.md --row S471 --row S472` on the in-flight state | `entry_present PASS (4261 bytes)`, `entry_meta PASS (sources S471,S472)`, `rows_present PASS (rows S471,S472 mined)`, **`census_ok FAIL (exit=1)`**, `readme_row FAIL`, `C3=unmet`, exit 1 |

Therefore `C3=met` cannot print at **any** revision, and the contract's After ("registry 245 rows
(S471, S472) with census exit 0") is unattainable with this instrument. The after-measurement will
print `C3=unmet`, exit 1, regardless of what the round lands.

### 3.3 (b) Cheapest do-nothing state, and reachability

With a stub census (the only way to make the code green): a 267-byte entry whose body is `body`, a
`coverage-map: FR5-superseded` line, an unregistered `source: S999`, and a README line inside a
"Removed / superseded" section → **`C3=met`, exit 0** (observed, sandbox `g`).

Reachability: with the real census, **no state is reachable**; with a stub census the state is
reachable but is not the registry census, so it is not the predicate. The code-level do-nothing state
is therefore reachable only by dishonesty.

### 3.4 (c) Universal / unmeasurable clauses

- "one **admitted** entry" — admission unmeasured.
- "ground it did not hold" — unmeasured by the counter, and the contract's proxy is a Japanese
  literal that cannot distinguish new ground from already-held ground expressed in English.
- "the `Z`/`X` alphabet and the three worlds" — content unmeasured.
- "a frontier-map **row**" — location unmeasured.

### 3.5 (d) Axis attribution — coverage: **mis-attributed**

`AXES.md`: coverage = "Fraction of the domain's real surfaces the skill governs (repo paths, tools,
edge classes). PROVINCE.md lists every surface; none unexplored without reason."

The identical artifact shape was already graded in this lane, in an **admitted** closure:
`corpus/lessons/round-31-verifier-spotcheck.md:156` — "coverage | unchanged | no coverage claim. The
frontier step (+14 SOURCES rows, README FR5/D5 map rows) is not an axis claim". The same closure
moved the *expansion trend* instead (`:189`, "One new entry on FR5 ground the coverage map did not
hold") and graded *depth* improved (`:154`). Three consequences:

1. One entry + mined SOURCES rows + a README frontier row on FR5 is not a coverage move by this
   lane's own admitted ruling.
2. C3 is a **partial** advance that leaves FR5 open — `corpus/knowledge/pid-probe-conclusion-r44.md:61`
   ("FR5 stays open"), `watchdog-identity-r31.md:62` ("FR5 stays frontier"). `AXES.md`'s frontier
   paragraph makes a coverage move out of "move `PROVINCE.md` frontier ground into core"; a partial
   advance that keeps FR5 on the frontier does not move it.
3. The ground was already held (§3.1).

The move is depth-shaped (a sourced decision table on two new pages) and the r31 closure graded its
FR5 decision table as depth. Mis-attributed; re-attribute to depth or show a coverage-fraction change.

### 3.6 (e) Causal separability

No C1/C2 byte is read, so the claim is separable from C1 and C2 — but two qualifications:

- The census check depends on an **unpinned external** script
  (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`, absent from `freeze-r44.txt`): the
  verdict can change with no lane byte changing.
- If the C1 ledger cites the entry (the natural corpus row), C1's after-state depends on C3's land
  (§1.5). One-directional coupling the contract denies.
- Routed-defect-5 recurrence: `verified-at:` is only required to exist. The in-flight entry names
  `7cb59c68` while it would be committed at a later tip, and the counter would not notice — the same
  shape as "receipt measured at `dde525ea` while the verdict claims the landed tip".

### 3.7 Verdict — **reword** (blocked until the census invocation is fixed)

Reason: the instrument cannot reach `C3=met`; the novelty clause is false on committed evidence; the
attribution repeats a move the lane's admitted closure refused; and three content checks are
substring tests. Fix the census invocation, check every declared `source:` id, match `FR5` as a
token, require the README line inside the frontier table, and re-attribute.

---

## 4. Cross-cutting findings

1. **C2 is pre-satisfied at the freeze commit.** `C2=met` at `7cb59c68` with all three counters and
   the round's mutant dir (§2.2). The claim's move is the instrument commit, not the data wave; the
   after-measurement cannot discriminate a wave that does nothing.
2. **The contract's After commands are not runnable as written.** P-C2's omits `--counter` →
   `usage: count-c2.py <rev|WORK> --counter PATH …`, exit 2 (observed). P-C1's is runnable. P-C3's
   names no counter invocation at all, and its stated outcome is unattainable (§3.2).
3. **The P-C1 witness is not runnable at the entering tip.** The fixture landed at `7cb59c68`, so at
   `1429c791` the counter prints `ledger_present FAIL (absent)` / `C1=unmet mismatches=?` — not the
   contract's `mismatches=2`. At `7cb59c68` it prints exactly `C1=unmet mismatches=2`, naming
   `F03 asserted=15 observed=14` and `F04 asserted=34 observed=8`. The witness is honest at the
   freeze tip only.
4. **The census script is not in the freeze pins**, yet P-C3's `census_ok` rests on it.
5. **Freeze integrity verified.** All ten sha256 pins in `evidence/freeze-r44.txt` match the current
   bytes (`0c261cb3…`, `9477824d…`, `0095d0c6…`, `a12170f1…`, `743996b1…`, `51e63f01…`,
   `f37bd18b…`, `919bc783…`, `27cbed5a…`, `f9b1e2bf…`). No instrument was amended.

## 5. Predicate-level answers in one line each

- **P-C1 (a)** code = five checks over a self-authored ledger; the English's report-coverage clause
  has no counterpart. **(b)** 12 ghost rows asserting `0` over absent paths → met; reachable now.
  **(c)** "one row per numeric assertion the round report makes" is universal and unmeasurable.
  **(d)** calibration correct. **(e)** separable unless the ledger cites C3-owned paths (demonstrated
  coupling). **Verdict: narrow.**
- **P-C2 (a)** code = five checks over a caller-supplied counter list; the isolation and
  one-check-disabled clauses have no counterpart. **(b)** met at the freeze commit with the round's
  three counters; reachable now. **(c)** "each of the round's counters" and "whose one check is
  disabled" are unmeasurable. **(d)** operability correct with a caveat. **(e)** separable and
  pre-satisfied. **Verdict: reword.**
- **P-C3 (a)** code = five checks, three of them substring tests; the novelty, content and admission
  clauses have no counterpart; `census_ok` is structurally red. **(b)** no state is reachable with
  the real census. **(c)** "admitted", "ground it did not hold", "the Z/X alphabet and the three
  worlds", "a frontier-map row" are all unmeasured. **(d)** coverage mis-attributed against
  `round-31-verifier-spotcheck.md:156`. **(e)** separable from C1/C2, but depends on an unpinned
  fleet census. **Verdict: reword (blocked).**

## 6. Smallest safe corrections (routed to round 45; not applied)

**C1**
1. Run rows with `set -o pipefail` (or run the `git` producer alone and require rc 0) so
   `git show @REV@:<absent> | wc -l` is *unreadable*, not `0`.
2. Drop `diff` from `GIT_VERBS` and reject `$(`/backtick substitution — otherwise rows read
   worktree and host state (demonstrated: met → 12 mismatches from one uncommitted file).
3. Make the 12/4 floors non-overridable for the scored run, or print the flags in the verdict line.
4. Add a `--report` input with a row→assertion map, or delete "one row per numeric assertion the
   round report makes" from the sentence.

**C2**
1. Require the counter set to be committed (a list file, or the gate-table rows whose `kind` is
   `gate`), not CLI-supplied.
2. Require each mutant to be a byte-diff of its counter (one hunk, one check) — a text tally cannot
   establish this; a reviewer or a `diff`-based check must.
3. Fix the default mutants dir, or pass `--mutants-dir .ufo/waves/round-44/fixtures/mutants` in the
   After line; add `--counter` ×3.
4. Require `--min-arms` ≥ the arm count the counter declares in its own tally.

**C3**
1. Validate the committed registry in place: `git diff --quiet @REV@ -- corpus/SOURCES.md` then
   `census validate --file <repo>/corpus/SOURCES.md`; or stage the file under a temp tree that
   preserves `<lane>/corpus/…` and symlink the referenced `used-by` paths.
2. Check **every** declared `source:` id, not the `--row` subset.
3. Match `coverage-map:` on the exact token `FR5` with a delimiter.
4. Require the README line to be inside the frontier table.
5. Re-attribute to depth, or show a coverage-fraction change (and reconcile with
   `round-31-verifier-spotcheck.md:156`).
6. Bind `verified-at:` to the measured revision (the routed defect-5 shape).

## 7. Evidence index

All lane commands were run read-only at `1429c791db5891c484684feef893799909d2d6a8` (entering tip) or
`7cb59c6891d4f5d0266fe062565f094da835dc84` (freeze). Sandbox = `/tmp/critpred-cro_k032`.

| # | Command | Observed |
|---|---|---|
| 1 | `count-c1.py 1429c791` (default ledger) | `ledger_present FAIL (absent)`, `C1=unmet mismatches=?`, exit 1 |
| 2 | `count-c1.py 1429c791 --ledger …/fixtures/figures-r43.tsv` | `ledger_present FAIL (absent)` — the fixture is absent at that rev |
| 3 | `count-c1.py 7cb59c68 --ledger …/fixtures/figures-r43.tsv` | `C1=unmet mismatches=2`; `F03 asserted=15 observed=14`; `F04 asserted=34 observed=8` |
| 4 | sandbox A: 12 identical rows, 4 labels | `C1=met mismatches=0`, exit 0 |
| 5 | sandbox B: 1 row + `--min-rows 1 --min-classes 1` | `C1=met`; with defaults `C1=unmet mismatches=0` |
| 6 | sandbox D: `git diff @REV@` row, clean → dirty → restored worktree | met → `F01 asserted=0 observed=2` → met, same revision |
| 7 | sandbox E: id `F01` twice (13 rows) | `C1=met` (ids are not unique-checked) |
| 8 | sandbox L: `WORK` with an untracked ledger | `C1=met`; `git ls-files --error-unmatch` fails (untracked) |
| 9 | sandbox N: rows `… \| grep -c "$(cat /tmp/…/outside.txt)"` | `C1=met`; changing only the outside file → 12 mismatches |
| 10 | sandbox O: ledger row reads the C3 entry path | absent → `C1=unmet mismatches=1`; after the entry lands → `C1=met` |
| 11 | sandbox P: 12 rows `git show @REV@:no/such/path-N.md \| wc -l` asserted 0 | `C1=met mismatches=0`, exit 0; `git cat-file -e` returns 128 |
| 12 | `count-c2.py 1429c791 --counter c1 --counter c2 --counter c3` | all five checks FAIL, `C2=unmet`, exit 1 |
| 13 | `count-c2.py 7cb59c68 --counter c1 --counter c2 --counter c3` (default mutants dir) | `mutant_kill FAIL (… mutant absent)`, `C2=unmet` |
| 14 | `count-c2.py 7cb59c68 --counter c2 --mutants-dir .ufo/waves/round-44/fixtures/mutants` | `C2=met`, exit 0 (one of three counters) |
| 15 | `count-c2.py 7cb59c68 --counter c1 --counter c2 --counter c3 --mutants-dir .ufo/waves/round-44/fixtures/mutants` | `C2=met`, exit 0 (pre-satisfied at the freeze commit) |
| 16 | `count-c2.py 7cb59c68` (no `--counter`) | usage, exit 2 |
| 17 | sandbox F: stub counter + lying "mutant" (no shared code) | `C2=met`, exit 0 |
| 18 | sandbox G: `pass=0 fail=0` selftest + `--min-arms 0` | `C2=met`, exit 0 |
| 19 | sandbox K: another gate's row passes the counter path as an argument | `REGISTRY=met` for **both** `tools/fx-one.py` and `tools/audit.py` |
| 20 | `count-c3.py 1429c791 --entry … --row S471 --row S472` | `entry_present FAIL (absent)`, `C3=unmet`, exit 1 |
| 21 | `count-c3.py WORK --entry corpus/knowledge/pid-probe-conclusion-r44.md --row S471 --row S472` | `entry_meta PASS`, `rows_present PASS`, `census_ok FAIL (exit=1)`, `C3=unmet` |
| 22 | census `validate --file corpus/SOURCES.md` (live) vs a `/tmp` copy | live exit 0 (`file ok`); staged exit 1 with E11 on every mined row |
| 23 | sandbox H/I/J: `S999` unregistered, `coverage-map: FR5-superseded`, README "Removed" line, stub census | `C3=met`, exit 0 |
| 24 | `git grep -l 'Z ゾンビ' <rev> -- corpus/` at 1429c791 and 7cb59c68 | `0` and `0` |
| 25 | `git show 1429c791:corpus/knowledge/watchdog-identity-r31.md` lines 27, 29 | empty-`cmdline` row (S170) and `Z` state row (S167, S171) already held |
| 26 | `git show 1429c791:corpus/SOURCES.md` S170/S171 | S170 "zombie exception and its 0-character read"; S171 "state letters (S … Z … X at :69-70)" |
| 27 | `corpus/lessons/round-31-verifier-spotcheck.md:156,189` | coverage "unchanged … not an axis claim"; expansion trend "improved" |
| 28 | `sha256sum` over the ten pinned files | all match `evidence/freeze-r44.txt` |

No tool was installed or upgraded for this assignment; no package manager was invoked.
