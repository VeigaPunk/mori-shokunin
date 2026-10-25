# round-44 w1 — mutation probe of `count-c1.py` (C1 figure reconciliation)

**Instrument.** `.ufo/waves/round-44/count-c1.py`, frozen at
`7cb59c6891d4f5d0266fe062565f094da835dc84`.
sha256 before probe `9477824d5eee45f47d49be52902f7bb0cd67a4d038e0ec7e79094c1e71999f83`,
after probe `9477824d…f83` — identical, and identical to the pin in
`evidence/freeze-r44.txt`. The frozen bytes were never edited; every probe ran
against a copy in `mktemp -d` (`/tmp/mutc1.bpfV9J/bin/count-c1.py`, same sha256),
and every probe repo is a throwaway git repo created by a scratch harness under
that sandbox. No `pacman`, `uv`, `npx` or binary install was needed or performed.

**Verdict semantics used below.** SURVIVED = the defect-carrying ledger still
printed `C1=met mismatches=0` (rc 0); KILLED = the counter rejected it
(`C1=unmet`, naming the row).

**Baselines (so no verdict below rests on an unknown instrument state).**

- Copy selftest: `python3 bin/count-c1.py --selftest` →
  `C1_SELFTEST pass=6 fail=0`, rc 0 (matches the freeze tally).
- Lane tip, read-only: `python3 bin/count-c1.py 7cb59c68… --repo <lane>` →
  `check ledger_present FAIL (absent)` … `C1=unmet mismatches=?`, rc 1 —
  the contract's **Before** state, reproduced.
- Positive control, the round-43 witness through the frozen copy:
  `--ledger .ufo/waves/round-44/fixtures/figures-r43.tsv` →
  `commands_reconcile FAIL (F03 asserted=15 observed=14; F04 asserted=34 observed=8)`,
  `C1=unmet mismatches=2`, rc 1. The arithmetic half of the counter works.

**Summary.**

| # | Attack | Verdict |
|---|--------|---------|
| 1 | 12 rows of trivially true figures | **SURVIVED** (`C1=met`) |
| 2 | row reads HEAD / working tree / parent rev instead of `@REV@` | **SURVIVED** (`C1=met`) |
| 3 | exit 0 + empty output / number + trailing text | **KILLED** (both) |
| 4 | 12 rows 3 classes / 4 classes 11 rows | **KILLED** (both); 12 rows 1 id 1 command → **SURVIVED** |
| 5 | row runs past timeout | **KILLED as hang — bounded**, but leaks orphans |
| 6 | row prints two integers | **KILLED, deterministic**; 64-byte window is a real hole |

---

## 1. Twelve trivially true figures — SURVIVED

Grammar needs: 4 TSV cells, id `F\d{2,3}`, integer asserted, class in
`{registry,evidence,wave,corpus,checks}`, command starting `git ` with a read
verb in `{show,grep,ls-tree,rev-list,cat-file,log,diff}`, `@REV@` textually
present, no `;`/`&&`, no `echo|printf|true`. None of that constrains what the
number *means*.

**(a) 12 identical tautologies** `git diff @REV@ @REV@ | wc -c` = 0, classes
cycling over 4 labels:

```
check rows_parse           PASS (12 rows)
check row_floor            PASS (rows=12 min=12)
check class_floor          PASS (classes=corpus,evidence,registry,wave min=4)
check commands_reconcile   PASS (all rows match)
C1=met mismatches=0                                    (rc=0)
```

**(b) 12 identical tautologies** `git show @REV@ -s --format=%H | wc -l` = 1 →
`C1=met mismatches=0` (rc 0).

**(c) revision-invariance.** The same ledger (a) measured at two different
commits (`10b1a77…` and `dbb8baa…`, `data.txt` changed between them) →
`C1=met mismatches=0` **at both**. A figure that is constant under every
revision cannot reconcile anything about a revision.

**(d) realistic form.** One genuine measurement — `git show @REV@:data.txt |
grep -c x` = 3 — copied into 12 rows and labelled across 4 classes →
`C1=met mismatches=0` (rc 0).

**Precise statement of the limit.** `count-c1.py` is a *self-consistency*
checker, not a calibration checker. Its whole relation set is:

1. textual grammar on the row (above);
2. integer equality between column 2 and the recomputed stdout;
3. line count ≥ 12 and count of distinct **typed class labels** ≥ 4.

It never checks that (i) a row's class label names the artifact class its
command actually reads, (ii) the 12 commands or the 12 ids are distinct,
(iii) the figure varies with the revision, (iv) the row's number corresponds to
any sentence in the round report, or (v) the command's `@REV@` is the operand
that determines the bytes. Consequence: **`C1=met` proves that twelve
self-consistent integer equalities exist under four typed labels — not that the
round's reported counts were reconciled.** The contract's witness
(`figures-r43.tsv`) is caught only because its rows are non-tautological; the
witness demonstrates the arithmetic, not the calibration. A reviewer must read
`figures.tsv`; the verdict alone cannot distinguish 12 real figures from one
figure labelled 12 ways.

## 2. Row reads the working tree instead of the revision — SURVIVED

There is no check for `HEAD`, `^`, `~`, `--` pathspecs, `git diff <rev>`
(two-ended, hence working-tree-inclusive), or nested command substitution.

**(a) HEAD read, `@REV@` textually present but unused.** Row
`git show HEAD:data.txt | grep -c x # @REV@` in a repo whose commit A has
3 `x` lines and whose HEAD (commit B) has 5. Measured at **A**:

```
rev-faithful  git show A:data.txt | grep -c x   -> 3
HEAD read     git show HEAD:data.txt | grep -c x -> 5
rows_parse PASS … commands_reconcile PASS (all rows match)
C1=met mismatches=0                                    (rc=0, rev=494a3703…)
```

The row asserts 5 and is scored `met` at a revision whose true value is 3: the
counter executed the row and reconciled a number that belongs to another commit.
Two defects compose here: `#` is not rejected, and the appended
`2>/dev/null | head -c 64` guard is swallowed by the comment (proved in §6d/§6e:
the same 70-digit row passes with `# @REV@` and fails without it, because the
guard truncates).

**(b) working-tree read.** Row `git diff @REV@ -- data.txt | wc -l`, asserted 0:

```
clean tree            -> commands_reconcile PASS (all rows match), C1=met (rc=0)
one uncommitted line  -> commands_reconcile FAIL (F01 asserted=0 observed=9)
                         C1=unmet mismatches=1 (rc=1), rev unchanged, git status: M data.txt
```

The ledger is admitted and passes at a clean tree; the identical ledger becomes
a mismatch the moment an uncommitted byte changes. So the row's value is not a
function of the measured revision at all — the counter has no way to say so, and
whether it catches the row depends on the state of somebody's working tree at
scoring time.

**(c) parent-revision read.** Row `git show @REV@^:data.txt | grep -c x`,
measured at `7b3061ee…` (`@REV@:data.txt` = 5, `@REV@^:data.txt` = 3), asserted 3
→ `commands_reconcile PASS (all rows match)`, `C1=met mismatches=0` (rc 0).

**(d) a second git pipeline nested inside the "single" pipeline.** Row
`git show @REV@:data.txt | grep -c "$(git show HEAD:data.txt | head -1)"`,
asserted 3 → `rows_parse PASS`, `C1=met mismatches=0` (rc 0). `$(…)` is not
scanned, so the contract's "one `git` pipeline" grammar admits an arbitrary
number of additional git reads of any ref.

## 3. Empty output, and number with trailing text — both KILLED

```
row: git ls-tree @REV@ -- no/such/path          (rc 0, stdout empty)
 -> commands_reconcile FAIL (F01 <- output '' is not an integer), C1=unmet mismatches=1 (rc=1)

row: git show @REV@:data.txt | wc -l | awk '{print $1" lines"}'   (stdout "3 lines")
 -> commands_reconcile FAIL (F01 <- output '3 lines' is not an integer), C1=unmet mismatches=1 (rc=1)
```

Control: a bare `wc -l` whose stdout is `3` plus trailing whitespace/newline →
`C1=met` (correct; `strip()` then `^\d+$`). Note the detail string truncates the
offending body to 40 chars (`body[:40]`), which is why a multi-line body can be
reported as a bare 40-char sha (seen in §6c).

## 4. Class floor and row floor — both KILLED; row identity is not checked

```
12 rows, 3 classes -> class_floor FAIL (classes=evidence,registry,wave min=4), C1=unmet (rc=1)
11 rows, 4 classes -> row_floor   FAIL (rows=11 min=12),                       C1=unmet (rc=1)
```

**Surviving sibling — the row floor counts lines, not figures.** 12 rows, 4
class labels, every row the same id `F01` and the same command:

```
rows_parse PASS (12 rows) · row_floor PASS (rows=12 min=12)
class_floor PASS (classes=corpus,evidence,registry,wave min=4)
C1=met mismatches=0                                    (rc=0)
```

There is no id-uniqueness check (`ID_RE` only validates shape) and no
command-uniqueness check, so "12 rows" is satisfiable by one row repeated.

**Caveat — the floors are caller-supplied flags.** `--min-rows` / `--min-classes`
default to 12/4 but are overridable, and the verdict string does not encode them:

```
1 tautology row, --min-rows 1 --min-classes 1
 -> rows_parse PASS (1 rows) · row_floor PASS (rows=1 min=1)
    class_floor PASS (classes=registry min=1) · C1=met mismatches=0   (rc=0)
```

`C1=met mismatches=0` is byte-identical to the 12/4 verdict; only the
`ledger=… rows=1 classes=registry` line distinguishes them. The contract's kill
rule "a ledger below the row floor is rejected" therefore holds at the default
flags only, and the printed verdict cannot be audited without reading the
`row_floor` detail line.

**Minor internal inconsistency (cannot produce a false `met`).**
`parse_ledger` appends every row to `rows` even when it records a problem, so
`row_floor` and `class_floor` are computed over unvalidated rows — and a bogus
class label such as `bogus` would count toward the class floor. It is
unreachable as a false pass only because any problem fails `rows_parse`.

## 5. Row running past the timeout — KILLED as a hang (bounded), orphans leak

Row `git show @REV@:data.txt | sleep 30` (grammar-clean: `show`, `@REV@`, no
`;`/`&&`/banned producer).

```
default (--timeout 20): wall 20.1s, rc 1
  commands_reconcile FAIL (F01 <- timeout after 20s), C1=unmet mismatches=1
--timeout 2:            wall 2.1s,  same FAIL
3 sleeping rows, --timeout 1:  wall 3.0s, mismatches=3
12 sleeping rows, --timeout 1: wall 12.0s, mismatches=12
```

So: **bounded, not a hang** — the wall clock equals rows × timeout, serially (no
parallelism), i.e. a 12-row ledger of blocking commands costs 240 s at the
default. Two real defects remain:

- **Orphan leak.** `subprocess.run(timeout=…)` SIGKILLs only the direct
  `bash -c` child; the pipeline grandchildren survive. Immediately after the
  12-row run, `pgrep -af 'sleep 30'` listed **12** live `sleep 30` processes and
  `pgrep -af 'head -c 64'` **12** live `head -c 64` processes, still holding
  their pipes after the counter returned (e.g. pids 4116129/4116130,
  4116185/4116186, 4116281/4116282). A row can therefore leave a process behind
  for every invocation. Cleaned up in the sandbox with `pkill`.
- **A timed-out row is scored as a mismatch, not as an infrastructure error.**
  `timeout after 20s` lands in `mismatches`, so an unreachable/hung command is
  indistinguishable from an off-by-one figure in the `C1=unmet mismatches=N`
  line.

## 6. Two integers — deterministic rejection, with a 64-byte hole

**Deterministic.** `run_row` takes the *whole* stdout, `strip()`s it, and anchors
`^\d+$`; there is no first-line/first-token pickup.

```
git ls-tree @REV@ | awk 'END{print NR, NR}'      -> body "2 2"
   commands_reconcile FAIL (F01 <- output '2 2' is not an integer), C1=unmet (rc=1)
git grep -c x @REV@ -- data.txt other.txt        -> body "ee4a…:data.txt:3\nee4a…:other.txt:3"
   raw:  'ee4a0140…:data.txt:3\nee4a0140…:other.txt:3'
   commands_reconcile FAIL (F01 <- output 'ee4a01404a11f852f1044657a14ba212a67da7a5' is not an integer)
   (detail truncated at 40 chars, so the second line is not visible in the message)
```

A `;`-separated two-print awk is rejected one layer earlier, by the textual
`;` filter:

```
git ls-tree @REV@ | awk 'END{print NR; print NR}'
   rows_parse FAIL (row 1: command is not a single pipeline), C1=unmet mismatches=? (rc=1)
```

That is a false positive of the grammar (the `;` is inside a quoted awk program,
not a shell separator), and it is the only reason this variant did not reach the
integer parser. Same run shows a reporting defect: `rows_parse FAIL` yet
`commands_reconcile PASS (all rows match)` is printed although **zero** commands
ran (`evaluate` only records `commands_reconcile` inside `if not problems`, and
the empty detail defaults to "all rows match"). A reader scanning for PASS lines
is misled.

**The 64-byte hole.** Every row is executed as
`<cmd> 2>/dev/null | head -c 64`, so the parsed integer is the first ≤ 64 bytes,
not the command's output:

```
nums.txt = 63 nines + "\n" + "junk\n"; row asserts the 63-nine integer
   commands_reconcile PASS (all rows match), C1=met mismatches=0      (rc=0)   <- trailing text invisible
nums.txt = 65 nines (one line); row asserts the true 65-nine integer
   commands_reconcile FAIL (asserted=999…9 [65] observed=999…9 [64]), C1=unmet (rc=1)  <- true figure mangled
nums.txt = 70 nines; row `git show @REV@:nums.txt # @REV@` asserts the 70-digit value
   C1=met mismatches=0  (guard swallowed by the comment; full output read)
nums.txt = 70 nines; same row without the comment
   FAIL (observed = 64 digits)
```

So multi-line output *can* reconcile when the truncation boundary falls at or
after the newline, and a correct figure ≥ 64 digits is a guaranteed mismatch.
Deterministic given the bytes, but the value is a function of the 64-byte window
rather than of the output. For this lane's real figures (< 64 bytes, single
line) the hole is inert; it matters as a latent hazard and as proof that the
`#`-comment bypass (§2a) disables a guard the instrument believes it has.

---

## Findings, ranked

1. **The verdict does not verify the claim.** `C1=met` is satisfiable by 12
   tautologies, by one figure labelled 12 ways, or by 12 rows sharing one id and
   one command (§1, §4). The instrument verifies arithmetic self-consistency
   only; the class column and the row count are author-typed metadata with no
   binding to the bytes read. This is the calibration axis the round is claiming
   to move, so the limit belongs in the record: a reviewer must read
   `figures.tsv`; `C1=met` alone is not evidence that the round's counts were
   reconciled.
2. **`@REV@` presence is textual, not semantic.** HEAD, `@REV@^`, `git diff
   <rev>` (working tree), and nested `$(git show HEAD:…)` all reconcile (§2). A
   row can therefore be true of a different commit than the one measured, and
   `git diff <rev>` rows make the verdict a function of the working tree at
   scoring time.
3. **`#` is unvalidated and swallows the instrument's own guard.** `# @REV@`
   satisfies the `@REV@` test while removing `2>/dev/null | head -c 64` (§2a,
   §6).
4. **Timeouts are bounded but leak orphaned grandchildren and are scored as
   mismatches** (§5).
5. **`head -c 64` makes the parsed value window-dependent** — a false pass for
   ≥64-byte digit-prefixed output, a false fail for a correct ≥64-digit figure
   (§6).
6. **Reporting defects:** `commands_reconcile PASS (all rows match)` printed when
   `rows_parse` failed and no command ran (§6); the verdict string hides which
   floors were used (§4); the mismatch detail truncates the body to 40 chars
   (§6c); the `;` filter rejects legal quoted `;` (§6).

## What the instrument gets right (for the record)

`read_at` reads the ledger from committed bytes (`cat-file -e` then `show`), so
the ledger cannot be swapped under it; `rc != 0` and non-integer stdout are
hard rejections; empty/absent ledger, sub-floor ledgers and the two off-by-one
witness rows are caught (witness: `mismatches=2` naming F03/F04); the selftest
runs 6 arms over isolated repos and passes 6/6 on the frozen copy.

## Restoration

- Frozen bytes: sha256 `9477824d…f83` before and after, equal to the
  `freeze-r44.txt` pin; `contract.md` likewise `0c261cb3…55d`. Neither file was
  opened for writing.
- All probes ran on copies under `/tmp/mutc1.bpfV9J` and throwaway repos under
  `/tmp/mutc1.bpfV9J`-derived `mktemp -d` roots; the lane repo was only read
  (`git show`, `git rev-parse`, `git cat-file -e`, and the read-only counter run
  at the tip).
- No `git add/commit/push/checkout/stash/reset`, no `jj`, no writes outside this
  report.
- Leftover `sleep`/`head` probe processes killed (`pkill -f 'sleep 30'`,
  `pkill -f 'head -c 64'`).
- No tools installed or upgraded.
