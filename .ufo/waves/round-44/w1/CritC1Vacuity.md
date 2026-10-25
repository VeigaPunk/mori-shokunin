# CritC1Vacuity — attack on P-C1 (round 44, wave 1)

Target: P-C1 in `.ufo/waves/round-44/contract.md` and its counter
`.ufo/waves/round-44/count-c1.py`.

Frozen bytes read (sha256 recomputed here, matching `evidence/freeze-r44.txt`):

```
9477824d5eee45f47d49be52902f7bb0cd67a4d038e0ec7e79094c1e71999f83  .ufo/waves/round-44/count-c1.py
51e63f0186c5d8edcfd283edd29de1e6df95a65959611302c03491128f2ce953  .ufo/waves/round-44/fixtures/figures-r43.tsv
```

All probes ran in a throwaway clone (`git clone --shared --no-checkout`,
`/tmp/c1vac.32cK7b/repo`, checked out at `7cb59c68`), never in the lane checkout.
Sandbox revisions quoted below are local to that clone; each is one commit that
adds only `.ufo/waves/round-44/figures.tsv`. Nothing in the lane was written
except this file. No tool was installed.

The witness works as advertised — first, so the attack is not aimed at a straw man:

```
$ python3 count-c1.py 7cb59c68 --repo /tmp/c1vac.32cK7b/repo \
      --ledger .ufo/waves/round-44/fixtures/figures-r43.tsv
check ledger_present       PASS (1518 bytes)
check rows_parse           PASS (12 rows)
check row_floor            PASS (rows=12 min=12)
check class_floor          PASS (classes=checks,corpus,evidence,registry,wave min=4)
check commands_reconcile   FAIL (F03 asserted=15 observed=14; F04 asserted=34 observed=8)
C1=unmet mismatches=2
exit=1
```

The counter is arithmetically sound and the fixture isolates the two slips. The
defect is what the predicate *means*, not whether the arithmetic runs.

---

## (a) A do-nothing lane reaches `C1=met`

**Yes, with one commit and zero round-44 artifacts.**

Cheapest ledger observed (618 bytes, `S14b`, sandbox rev `03df5d84`):

```
F01  893  corpus    git show @REV@:SKILL.md | grep -c .
F01  893  evidence  git show @REV@:SKILL.md | grep -c .
...                     (12 rows, one id, one command, four class labels)
```

```
check ledger_present       PASS (618 bytes)
check rows_parse           PASS (12 rows)
check row_floor            PASS (rows=12 min=12)
check class_floor          PASS (classes=corpus,evidence,registry,wave min=4)
check commands_reconcile   PASS (all rows match)
C1=met mismatches=0
exit=0
```

That is one numeric assertion, repeated twelve times, over a file this round did
not touch. It satisfies every clause the counter can see.

The stronger form — a ledger that *looks* like the round's work and still does
none of it (`S1`, sandbox rev `3ffdc89e`): take `fixtures/figures-r43.tsv`, set
F03 to the observed `14` and F04 to the observed `8`, commit it as
`.ufo/waves/round-44/figures.tsv`. Result: `C1=met mismatches=0`, exit 0, with
**0 of 12 rows reading any `.ufo/waves/round-44/` path** and 12 of 12 reading
round-43 bytes. A lane that only commits a ledger of the previous round's figures
is scored as having reconciled this round's.

**Would it have caught the two round-43 slips? No — and the demonstration is
direct.** At the same `S1` rev, `C1=met` and the slips coexist:

```
$ git show 3ffdc89e:corpus/lessons/round-43-verifier-spotcheck.md | grep -n '15 checks'
111:`control-c1s-green.txt` is also **14**. The report's "15 checks PASS" (and
$ git show 3ffdc89e:corpus/lessons/round-43.md | grep -n '34 seat logs'
132:The 64-seat v2 wave was starved by the provider's rate limit (34 seat logs
```

The ledger says 14 and 8; the committed prose still says 15 and 34; the counter
prints `C1=met`. So P-C1 does not route routed-defect item 3. It routes a
*different* defect: "a ledger transcribed from prose disagrees with the
artifacts". The round-43 slip was "prose disagrees with the artifacts, with no
ledger in existence".

**Why the witness cannot be extrapolated.** The witness fires only because its
asserted column was copied from the report. The natural way to author a ledger —
run the command, write what it printed — makes `mismatches=0` true by
construction. For any ledger whose asserted column is produced from its own
commands, C1 is guaranteed met. C1 therefore measures agreement between two
columns the same author writes in the same commit, and it fails only when the
author did not run the command. The kill rule "a do-nothing control cannot print
`C1=met` (no ledger at the entering tip)" is true only because the entering tip
has no ledger file; it is a statement about file absence, not about the
predicate's discriminating power. `evidence/control-c1-donothing.txt` shows
exactly this: `check ledger_present FAIL (absent)`. That control produces the
identical output for a fully honest round, so it distinguishes nothing.

**Second do-nothing path, no commit required** (`S10`, rev `WORK`):

```
$ git status --porcelain -- .ufo/waves/round-44/figures.tsv
?? .ufo/waves/round-44/figures.tsv
$ python3 count-c1.py WORK --repo /tmp/c1vac.32cK7b/repo
check ledger_present       PASS (618 bytes)
...
rev=WORK
C1=met mismatches=0
exit=0
```

The predicate says "a **committed** figure ledger"; the instrument's own usage
string advertises `<rev|WORK>` and prints the same success line for an untracked
file. `read_at` reads the worktree when `rev == "WORK"` and the row commands run
against `HEAD`, so an uncommitted ledger is scored against committed bytes and
passes.

**Third path, floors are caller-supplied** (`S9`, rev `85225165`):

```
$ python3 count-c1.py 85225165 --min-rows 1 --min-classes 1
check row_floor            PASS (rows=1 min=1)
check class_floor          PASS (classes=wave min=1)
C1=met mismatches=0
exit=0
```

The contract's 12-row / 4-class floor lives only in the argparse defaults. The
verdict string `C1=met mismatches=0` is byte-identical at one row. The detail
cell leaks the floor, but nothing in the verdict does.

---

## (b) `{registry, evidence, wave, corpus, checks}` is not a coverage dimension

It is a free-text label column with a 4-of-5 quota. Four independent findings:

1. **The frozen instrument's own selftest proves the labels are decorative.**
   `_honest_rows` assigns `cls = list(CLASSES)[i % len(CLASSES)]` while every row
   runs the identical command `git show @REV@:data.txt | grep -c x`. Twelve rows,
   one file, one assertion, five labels — and `honest_ledger_met` passes. The
   instrument asserts, in its own fixture, that a class carries no relation to the
   bytes a row reads.

2. **Mislabeling is unchecked.** `S2b` (rev `6bdc2632`) labels a row `registry`
   whose command reads `corpus/QUALITY.md`; `C1=met`.

3. **The witness fixture itself does not partition artifacts by class.**
   Per-class rows and the artifact root each class actually reads:

   | class | rows | artifact root |
   |---|---|---|
   | wave | 6 | `.ufo/waves/round-43/logs` (2), `.ufo/waves/round-43/w1` (4) |
   | corpus | 3 | `corpus/` |
   | registry | 1 | `corpus/SOURCES.md` |
   | checks | 1 | `.ufo/waves/round-43/evidence/c1s-after.txt` |
   | evidence | 1 | `.ufo/waves/round-43/evidence/` (directory) |

   `checks` and `evidence` are two labels over one directory. `wave` carries half
   the ledger. `registry` is a subset of `corpus`. So the set is not orthogonal:
   one axis (`wave`) dominates, and two labels (`checks`, `evidence`) are the same
   artifact distinguished by whether the command counted lines or files.

4. **No denominator exists.** Nothing enumerates the numeric assertions the round
   report makes, so "coverage" has no total to be a fraction of. The floor is on
   rows (12), not on assertions, and the 4-of-5 quota means a lane may drop one
   whole class — including the class where a slip lives — and still pass. A report
   with forty numbers can ship a twelve-row ledger covering four convenient
   labels.

Verdict: the class set is a **decorative quota**, not a coverage dimension. It
records author intent, and the counter grades the record, not the artifact.

---

## (c) The `git`-pipeline grammar is a lexical filter, not a byte-provenance check

`parse_ledger` anchors on the first two tokens (`git` + a verb in `GIT_VERBS`) and
rejects the literal words `echo|printf|true` and the characters `;`/`&&` anywhere
in the string. Everything after the first pipe is unconstrained. Probes, all
observed:

| probe | row command | verdict |
|---|---|---|
| S3 | `git config --get x` | **rejected** — `rows_parse FAIL (git verb 'config' is not a read verb; command does not name @REV@)` |
| S4 | `git show @REV@:SKILL.md \| awk 'BEGIN{print 7}'` asserted 7 | **`C1=met`** |
| S5 | `git show @REV@:SKILL.md \| sed -n '1s/.*/42/p'` asserted 42 | **`C1=met`** |
| S6 | `git show @REV@:.ufo/waves/round-44/figures.tsv \| grep -c '^F'` asserted 12 | **`C1=met`** (self-referential) |
| S7 | `git show @REV@:no/such/file \| wc -l` asserted 0 | **`C1=met`** |
| S8 | `git grep -l 'zzz' @REV@ -- no/such/dir \| wc -l` asserted 0 | **`C1=met`** |
| S12a | `git show @REV@:SKILL.md \| wc -l \| xargs -I{} expr {} - {}` asserted 0 | **`C1=met`** |
| S12b | `git show @REV@:.gitignore \| wc -l \| awk -v n="$(git show 1429c791:.ufo/waves/round-44/contract.md \| wc -l)" 'END{print n}'` asserted 0 | **`C1=met`** (number from a fixed rev) |
| S13 | `git show @REV@:SKILL.md \| sh -c 'python3 -c "print(5)"'` asserted 5 | **`C1=met`** (arbitrary interpreter) |
| S15 | `git show @REV@:SKILL.md \| git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 1429c791:SKILL.md \| wc -l` | **`C1=met`** (bytes from a *different repo* at a fixed rev) |
| S16 | `awk '{for(i=0;i<40;i++) printf "%d", $1}'` | **rejected** — `not a single pipeline` + `non-byte producer`, because `;` and `printf` occur *inside a quoted program* |

So the grammar is both under- and over-inclusive:

- **Under**: `sed`, `awk`, `sh -c`, `xargs`, `expr`, `tr`, `yes`, `$()`, `||`,
  and a second `git -C <other repo>` stage are all admitted. The ban list is
  cosmetic: `print` in awk is not `printf`, and `sh -c 'python3 -c …'` is neither.
  `@REV@` may appear in the command while the number comes from somewhere else
  entirely (S12b, S15).
- **Over**: a legitimate `awk`/`sed` program containing `;` or `printf` is refused,
  so the grammar punishes quoting style rather than provenance.

**Absence reads as zero.** `run_row` appends `2>/dev/null | head -c 64`, so the
pipeline's exit status is the last stage's. A missing file or a nonexistent
directory prints `0` with rc 0 (S7, S8). The counter cannot distinguish "this
class has zero members" from "this artifact does not exist", and an asserted `0`
is therefore unfalsifiable.

**Truncation is a match.** `head -c 64` silently cuts the row's output. `S16b`
(rev `17daa1a3`): a row emitting 120 digits, asserted to the first 64, prints
`C1=met`. A truncated prefix is accepted as the complete value.

---

## (d) What the counter does not catch — the closure reviewer's manual list

The word `report` does not occur in `count-c1.py` (`grep -c report` → 0, `grep -c
corpus/lessons` → 0). Nothing in the instrument opens the round report. These are
the gaps, each with the probe that shows it:

1. **Report ↔ ledger correspondence.** No row is anchored to a sentence. Demonstrated
   in (a): `C1=met` while the committed prose still says 15 and 34. A closure
   reviewer must diff every numeric assertion in the report against a ledger row
   by hand — which is the entire claim P-C1 makes, delegated back to the human.
2. **Completeness.** Twelve is a floor, not a census (S14b: one assertion twelve
   times). Reviewer must enumerate the report's numbers and check each has a row.
3. **Row ↔ class semantics.** Labels are unverified (S2b, and `_honest_rows`).
4. **Round relevance.** No row must read a round-44 path (S1: 0 of 12).
5. **Committedness.** `rev=WORK` prints the same success string over an untracked
   ledger (S10). Reviewer must confirm the printed `rev=` is a sha and that
   `git cat-file -e <sha>:<ledger>` succeeds.
6. **Floor enforcement.** `--min-rows`/`--min-classes` are caller-supplied (S9).
   Reviewer must record the exact argv; the verdict line does not encode it.
7. **Byte dependence.** A row may be a constant, a fixed-rev read, or a different
   repo (S4, S5, S12a, S12b, S13, S15). Reviewer must confirm each number moves
   with the artifact — cheapest manual test: re-run the ledger at `rev^` and
   require most values to change, and read every command for `awk BEGIN`,
   `sed s/.*/N/`, `sh -c`, `$(`, `||`, and bare sha literals.
8. **Absence vs zero.** Every path a row names must exist at the rev (S7, S8);
   otherwise an asserted `0` proves nothing.
9. **Self-reference.** A row may count the ledger itself (S6). Reviewer must check
   no command names `figures.tsv`.
10. **Provenance and order.** The ledger and the report land in the same commit
    series; nothing shows the number was measured before it was asserted, so
    command shopping after the fact is undetectable. Reviewer must check the
    ledger commit precedes the report commit, or that a recorded run produced it.
11. **Misleading PASS.** When `rows_parse` fails, no row executes but the counter
    still prints `check commands_reconcile PASS (all rows match)` (S3, and the
    S16 output). A reviewer reading only the five check lines is misled; the
    `mismatches=?` in the verdict is the tell.
12. **Duplicate ids.** `ID_RE` checks shape only; twelve rows with the same `F01`
    parse and pass (S14b).

The frozen `--selftest` (6 arms, `pass=6 fail=0`, run here) covers honest,
off-by-one, junk producer, below-floor, absent ledger, compound command. It has no
arm for any of S4–S16.

---

## Round-45 tightening (named, not applied — no frozen byte was touched)

Ordered by leverage; T1 alone converts C1 from a self-consistency check into the
claim P-C1 actually makes.

- **T1 — anchor + denominator.** Fifth TSV cell `anchor`: `<report path>#<literal
  sentence fragment>`. Counter checks the fragment occurs in that file at `@REV@`,
  that the fragment contains the asserted integer as a token, and that
  `rows == numeric_assertions(report)` for a fixed extraction regex (or an explicit
  `#assertions-total N` header the counter verifies). This is the smallest safe
  correction and the one that routes item 3.
- **T2 — class binds to bytes.** Every path in a row's command must sit under the
  class's declared root (`registry` → the registry file, `evidence` →
  `.ufo/waves/round-44/evidence/`, `wave` → `.ufo/waves/round-44/`, `corpus` →
  `corpus/`), and the class set must be an artifact partition, not a relabeling
  (`checks` folded into `evidence`).
- **T3 — round relevance and no self-reference.** At least one row per covered
  class reads a `.ufo/waves/round-44/` path; no command may name `figures.tsv`.
- **T4 — byte dependence.** Run each row at `@REV@` and at `@REV@^`; require the
  output multiset to change for at least half the rows, and whitelist the
  pipeline (git read verb + path + `grep -c` / `wc -l` / `ls-tree … | wc -l`),
  denying `awk`, `sed`, `sh`, `xargs`, `expr`, `tr`, `yes`, `$()`, `||`, and any
  sha literal.
- **T5 — absence is a failure.** `git cat-file -e @REV@:<path>` for every path a
  row names; absent ⇒ `row_unreadable` FAIL, never `0`.
- **T6 — committedness and floors in the verdict.** Refuse `WORK` (or print
  `C1=unmet mode=work`), and make the verdict line
  `C1=met rows=12/12 classes=5/4 mismatches=0` so the floor is inside the string
  the contract quotes.
- **T7 — distinctness.** Unique ids; ≥ N distinct (command, asserted) pairs.
- **T8 — no PASS without execution.** `commands_reconcile` must FAIL (or print
  `skipped`) when `problems` is non-empty.
- **T9 — pre-registration.** `figures-pre.tsv` committed at round start, or a
  `--emit` mode writing `evidence/figures-run.txt`, so the asserted column cannot
  be authored after the numbers are known.
- **T10 — exact output.** Drop `head -c 64`, or treat `len(stdout) > 64` as
  `row_unreadable`, so a truncated prefix cannot match.

Impacted axes: C1's calibration claim is overstated as filed — it measures
instrument arithmetic (which holds) plus a practice it cannot observe. C2 is
unaffected. If C1 lands as specified it should be scored as *instrument built,
claim partially discharged*: the ledger will reconcile, but the round's prose will
not be bound to it, and a reviewer must still diff them by hand.

## Repro index

Sandbox `/tmp/c1vac.32cK7b/repo` (shared clone at `7cb59c68`); each `S*` is one
commit adding only `.ufo/waves/round-44/figures.tsv` on top of `7cb59c68`, run as
`python3 <lane>/.ufo/waves/round-44/count-c1.py <rev> --repo /tmp/c1vac.32cK7b/repo`.

| probe | rev | verdict |
|---|---|---|
| S1 corrected r43 fixture, 0 round-44 rows | `3ffdc89e` | `C1=met` |
| S2 / S14b cheapest ledger (618 B, 1 assertion ×12) | `e85a64f8` / `03df5d84` | `C1=met` |
| S2b mislabeled class | `6bdc2632` | `C1=met` |
| S3 `git config --get x` | `713431d2` | `rows_parse FAIL` |
| S4 / S5 / S12a constant producers | `39c65d45` / `ea3e22eb` / `35243e60` | `C1=met` |
| S6 self-referential | `bcade955` | `C1=met` |
| S7 / S8 absent artifact as 0 | `a0d4ddb3` / `4223c062` | `C1=met` |
| S9 floors overridden to 1/1 | `85225165` | `C1=met` |
| S10 `WORK`, untracked ledger | `WORK` | `C1=met` |
| S12b fixed-rev literal | `b2f6ffc0` | `C1=met` |
| S13 `sh -c 'python3 -c …'` | `2c5f020a` | `C1=met` |
| S15 bytes from another repo | `bfa9dd29` | `C1=met` |
| S16 `;`/`printf` inside a quoted program | `53ad8118` | rejected (false positive) |
| S16b 120-digit output truncated to 64 | `17daa1a3` | `C1=met` |
