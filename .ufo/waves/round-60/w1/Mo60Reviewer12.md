# Mo60Reviewer12 — lesson-correction audit (round 60, w1)

Seat: Mo60Reviewer12 (reviewer, leaf). Scope: `corpus/lessons/round-60.md`
absent-set correction only. Read-only: no edits, no commits, no VCS mutation.

Frozen contract freeze `ac496c7c…`, entering `ddfb12fb…`, r59 data rev
`7b86704d…`, landing `f091bd77…` (contract.md). The lane moved three times
while this seat ran; every observation is pinned to a revision or to a content
sha256, and the final verdict is stated for the tip at report time.

## Revisions observed (chronological)

| state | lane HEAD | lesson blob at HEAD | worktree | note |
|---|---|---|---|---|
| S0 (audit start, ~13:05) | `b3c256138f…` | `c1da1ca1…` | clean for the path | original C1 data state |
| S1 (~13:15) | `b3c256138f…` | `c1da1ca1…` | modified, sha256 `ebabff29…` (13+/3−) | sibling seat added `f091bd77` to the Critic29/Reviewer16 bullets + a Reading note |
| S2 (report time, 13:2x) | `0f8340cf62…` (`round-60: lesson — distributive pointer lines, wave-found routed instrument defects…`, 13:19:59) | `4b4d60b1…` | content == HEAD blob (`git diff 0f8340cf -- corpus/lessons/round-60.md` empty) | **R for this audit** |

At S2 the index is **not** HEAD: `git rev-parse :corpus/lessons/round-60.md` →
`c1da1ca1…`, i.e. the index is a staged *revert* of the committed pointer
lines; `git status --porcelain` prints `MM corpus/lessons/round-60.md`
(`git diff --cached --stat` → 3 insertions / 49 deletions vs HEAD). See F5.

## Verdict against the three dispatched conditions (at R = `0f8340cf`, blob `4b4d60b1`)

| # | Condition | Result | Evidence at R |
|---|---|---|---|
| 1 | contains `supersedes round-59` | **PASS** | `:44` `## Round-59 absent-set correction (supersedes round-59)`; also `:46`. |
| 2 | a `supersedes` line for Mo59Critic29 and Mo59Reviewer16 | **PASS** | `:50` `- Mo59Critic29 — supersedes the round-59 lesson claim of absent-at-filing:`; `:54` same for `Mo59Reviewer16`. |
| 3 | `late` lines for the other three names carrying `f091bd77` | **PARTIAL (2/3 literal)** | `:60` Executor40 `late: landed post-filing in \`f091bd77\``; `:61` MutationTester31 identical; `:57–59` MutationTester32 carries `f091bd77` but **no `late` token**. `git show 0f8340cf:corpus/lessons/round-60.md \| grep -n late` → only 60, 61, 86 (86 = unbound "late seat files" in Mistakes row 2). |

Same results at S0 (`b3c25613`, blob `c1da1ca1`), except condition 2's lines
were `:50`/`:53` and condition 3's were `:58`/`:59`/`:55–57`. Content of all
five bullets is substantively true at both revisions (truth table below).

## Findings (severity order)

### F1 (MEDIUM) — the scored counter cannot test condition 3: C1's lesson arm is file-global, not name-bound
`count-c1.py:218–230` (landing check at `:228`):

```
            else:
                if not (name in lt and R59_LANDING[:8] in lt):
                    lesson = "bad"
                    failed.append("lesson:%s" % name)
```

Both operands are whole-file `in` tests: any mention of the name anywhere plus
any occurrence of `f091bd77` anywhere satisfies the row. No line binding
(contrast C2's H4 per-copy row binding, which this round adds). The
`supersedes` branch at `:224` has the same aliasing; it is unused this round
because no frozen name is present at `7b86704d`.

Demonstration on the real S0 lesson bytes (predicate replicated verbatim, no
repo mutation):

```
real lesson failed: []
M1 (MT32 pointer removed, others keep f091bd77) failed: []
M2 (all f091bd77 removed) failed: ['Mo59Executor40','Mo59MutationTester31','Mo59MutationTester32','Mo59Critic29','Mo59Reviewer16']
changed lines: [56]
```

Stripping MutationTester32's own landing pointer left every name passing,
because Executor40's line still supplied the global `f091bd77`. So
`lesson=ok` attests only "all five names appear somewhere and `f091bd77`
appears somewhere". The condition-3 `late` miss is invisible to the counter.
This is the same alias class C2's H2/H4 close.

The lane independently records the same fact at R in
`## Wave-found instrument defects` item 2 (`:116–120`): "the pointer check is
file-global; under a distributive reading of the contract sentence the tip
scores 3/5" — accurate for S0 (three of five bullets carried the pointer).

### F2 (LOW at R; was MEDIUM at S0) — contract literal vs. lesson pointers: closed at R, but the "record set completes" definition is lesson-made, not contract-made
`contract.md:54–58`: disposition is `late-committed` **exactly when** the file
was absent at `7b86704d`, else `wrong-superseded`; the lesson must name "every
wrong-superseded name with `supersedes`, every late-committed name with
landing pointer `f091bd77`". All five names were absent at `7b86704d`
(`git cat-file -e` below) → all five are `late-committed` → the literal clause
wants `f091bd77` on all five.

At S0 only three bullets carried it; Critic29/Reviewer16 named `bf6c0ad3`
only, so a literal re-reader could mark C1 unmet for two names even though
`bf6c0ad3` is the *correct* landing commit (`git rev-parse
bf6c0ad3:…/Mo59Critic29.md` = `3f49b8f0…` = HEAD blob, 10712 B; Reviewer16
`97a90571…` = HEAD blob, 10742 B). At R all five bullets carry `f091bd77`
under the Reading note's definition ("the commit at which the round-59 wave
RECORD SET is complete — every one of the five names is covered by it,
directly (two files) or as the completing commit of a record whose earlier
bytes landed in `bf6c0ad3` (three files)", `:65–71`). That definition is sound
and internally consistent, but it is introduced by the lesson, not by the
frozen contract; the contract's "landing pointer" never says "record-complete
commit". Residual interpretation risk only; no false statement.

### F3 (LOW) — the superseded claim no longer exists at R; the lesson does not name the revision that carries it
`bf6c0ad3:corpus/lessons/round-59.md:77–79` carries the claim:
"…Reports absent at filing: Mo59Critic29, Mo59Executor40, Mo59MutationTester31,
Mo59MutationTester32, Mo59Reviewer16". It was already replaced pre-entering by
`a86e5f83` (`round-59: lesson settlement 64/64 post WAVE-DONE`,
committer 07:43:47) with "**All 64 reports landed after WAVE-DONE** … the three
late seats (Mo59Executor40, Mo59MutationTester31/32)".

So `round-60.md:50/:54` corrects a revision that is no longer at tip, and the
lesson names `bf6c0ad3` only as the reports' landing commit, not as the
revision carrying the claim. A reader at R finds no such claim in
`corpus/lessons/round-59.md` (`grep -n "Critic29\|Reviewer16\|absent at
filing" corpus/lessons/round-59.md` → only the `:78–79` "three late seats"
lines). Mitigated because `round-59-verifier-spotcheck.md` defect 3 (committed
at `ddfb12fb`) restates the inconsistency, so the chain is two hops but closed.
Recommendation: cite `bf6c0ad3:corpus/lessons/round-59.md` §Wave w1 explicitly.

### F4 (LOW) — cited timestamps are committer dates, not the default `git log` (author) dates
`round-60.md:51` cites `bf6c0ad3 (2026-10-28 03:12:38 -03)`; `:60` cites
`f091bd77 (07:42:42 -03)`. Both are **committer** stamps; author stamps are
03:00:51 and 03:12:53:

```
bf6c0ad3 ai=2026-10-28 03:00:51 -0300 ci=2026-10-28 03:12:38 -0300
f091bd77 ai=2026-10-28 03:12:53 -0300 ci=2026-10-28 07:42:42 -0300
a86e5f83 ai=2026-10-28 07:42:42 -0300 ci=2026-10-28 07:43:47 -0300
```

`git log --date=iso` prints the author clock, so a verifier eyeballing the log
sees a 4-minute and a 4.5-hour "mismatch". Not a truth error (the stamps
reproduce under `%ci`), but the lesson should label the clock. Related: the
"filed (07:41)" in Mistakes row 2 (`:86`) has no committed evidence; the
pre/post-filing ordering is independently established by topology
(`bf6c0ad3 → 08127c99 → f091bd77 → a86e5f83 → ddfb12fb`), so the minute is
decorative.

### F5 (MEDIUM, hygiene — observed state, not a lesson statement) — the index is staged to revert the correction while HEAD/worktree carry it
At report time: HEAD `0f8340cf` lesson blob `4b4d60b1…`; index
`c1da1ca1…`; worktree content == HEAD blob. `git status --porcelain` →
`MM corpus/lessons/round-60.md`. `git diff --cached --stat` → 3 insertions /
49 deletions (the staged revert), `git diff HEAD` → empty.

Consequence: a bare `git commit` (no pathspec, no `-a`) would commit the
revert and drop the distributive pointer lines and the routed-defects section
from R; `git commit -a` would be a no-op for this file. This seat did not
create the state and did not touch it. Flagged for the settlement owner: the
final round commit should check `git diff --cached --name-status` first.
(This is the state as sampled; a sibling may still be mid-operation.)

## Truth check of the corrections (all agree with git)

`git cat-file -e <rev>:.ufo/waves/round-59/w1/<name>.md`:

| name | 7b86704d | bf6c0ad3 | f091bd77 | tip | lesson claim (at R) | agrees |
|---|---|---|---|---|---|---|
| Mo59Critic29 | absent | present, blob `3f49b8f0…` (= tip) | present | present | `bf6c0ad3` pre-filing (`:50–52`) | yes |
| Mo59Reviewer16 | absent | present, blob `97a90571…` (= tip) | present | present | `bf6c0ad3` pre-filing (`:54–56`) | yes |
| Mo59MutationTester32 | absent | present `00e1208a…` | modified `1fc46af2…` (5 lines) | present | added `bf6c0ad3`, modified `f091bd77` (`:57–59`) | yes |
| Mo59Executor40 | absent | absent | added (+556 lines) | present | late, `f091bd77` (`:60`) | yes |
| Mo59MutationTester31 | absent | absent | added (+111 lines) | present | late, `f091bd77` (`:61`) | yes |

`w1-results.json`: added in `f091bd77` (+392 lines) — lesson `:62` correct.
The two `supersedes` verdicts are earned: Critic29/Reviewer16 were committed —
byte-identical to their final bytes — in the same commit whose lesson claimed
them absent, so the round-59 record was false at filing, not merely stale.

Supporting claims: `SCORECARD.md` at entering `ddfb12fb` lines 2950–2951 each
contain exactly one of `c1-entering.txt`/`c2-entering.txt`
(`git show ddfb12fb:SCORECARD.md | sed -n '2950,2951p' | grep -o "c[12]-entering\.txt"`);
both real receipts exist at HEAD
(`git ls-tree --name-only HEAD .ufo/waves/round-59/evidence/` lists
`control-c1-do-nothing.txt`, `control-c2-do-nothing.txt`); QUALITY criterion
156 exists at `corpus/QUALITY.md:1590` and matches the lesson's description.

## Canonical counter checks (read-only)

Scratch `/fast/scratch/hyaku/mori-r60/Mo60Reviewer12` (TMPDIR set, cleaned at
yield); disk-guard green at start (`/fast/scratch/hyaku` 26%, 600.0 G free).

```
$ S=/fast/scratch/hyaku/mori-r60/Mo60Reviewer12; cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ TMPDIR=$S python3 .ufo/waves/round-60/count-c1.py b3c256138f00c704d5aa56eb0332d74506502ef2 --scratch $S/c1
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=b3c256138f00c704d5aa56eb0332d74506502ef2
rc=0
$ TMPDIR=$S python3 .ufo/waves/round-60/count-c1.py 0f8340cf62b588fd64be8d9176ed7d5444c426b2 --scratch $S/c1b
C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5 lesson=ok rev=0f8340cf62b588fd64be8d9176ed7d5444c426b2
rc=0
```

Both revisions are `met`; the r59 counters re-ran at `7b86704d` and
byte-equalled both receipts, and absent-set 5/5 matches git truth. F1/F2 bound
what `lesson=ok` is allowed to mean; they do not overturn the measurement.

## Residual risk

- Condition 3's literal miss survives only because the counter is aliased; a
  future tighten of `count-c1.py` (name-bound landing pointer + `late` marker)
  would flip `lesson=ok` to `bad` for MutationTester32 at both measured
  revisions. The lane's own routed item 2 acknowledges the pointer half.
- The contract's "landing pointer" is read at R through the lesson's
  "record set completes at" definition (F2). If the closure insists on
  "the commit that added the bytes", Critic29/Reviewer16 are `bf6c0ad3`, which
  the lesson states — so both are defensible, but the closure should say which
  reading governs.
- F5's index state is live: if the round commits without checking the index,
  the correction is reverted in R while the worktree still shows it.

## Verification gaps

- "r59 report filed (07:41)" is not derivable from committed bytes (no mtimes
  in git; ordering comes from topology only).
- The r59 lesson's absent-at-filing set cannot be checked against any
  uncommitted round-59 state (none exists); the check is commit-tree based, as
  the claim itself is.
- Receipt byte-equality is reported from the counter runs, not re-hashed here;
  that arm belongs to the C1 seat.

## Tooling / hygiene

No installs or upgrades (none needed). No git writes; every git invocation was
`-C /home/vgpnk/Projects/shokunin/mori-shokunin` read-only (`rev-parse`,
`cat-file`, `show`, `ls-tree`, `log`, `status`, `diff`, `grep`). Scratch
removed after the run; no fleet/sibling writes; only this report was authored.
