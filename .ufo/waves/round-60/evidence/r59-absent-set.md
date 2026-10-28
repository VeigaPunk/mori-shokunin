# r59 absent-at-filing reconciliation (round 60, C1 ABSENT-SET ARM)

Truth source: `git -C <lane> cat-file -e <rev>:.ufo/waves/round-59/w1/<name>.md`
at the r59 data revision `7b86704d` and at the round-60 tip. The r59 report's
missing set {Executor40, MutationTester31, MutationTester32} and the r59
lesson's absent-at-filing set (which wrongly added Critic29 and Reviewer16)
are superseded by this table; corrections in `corpus/lessons/round-60.md`.

| name | at 7b86704d | at r60 tip | disposition | landing pointer |
|---|---|---|---|---|
| Mo59Executor40 | absent | present | late-committed | `f091bd77` (07:42:42 -03, post-filing) |
| Mo59MutationTester31 | absent | present | late-committed | `f091bd77` (07:42:42 -03, post-filing) |
| Mo59MutationTester32 | absent | present | late-committed | added `bf6c0ad3` (03:12:38, pre-filing), modified `f091bd77` |
| Mo59Critic29 | absent | present | late-committed | added `bf6c0ad3` (03:12:38, pre-filing) — the r59 lesson's absent claim was wrong |
| Mo59Reviewer16 | absent | present | late-committed | added `bf6c0ad3` (03:12:38, pre-filing) — the r59 lesson's absent claim was wrong |

Disposition grammar note: `late-committed` is bound to absence at the r59
DATA revision (`7b86704d`) per count-c1's frozen predicate; the pre-filing vs
post-filing nuance lives in the landing-pointer cells and the lesson
correction (Critic29/Reviewer16 were committed at filing time in `bf6c0ad3`,
so the lesson's absent-at-filing claim about them was false — the report's
missing set was correct about which files were late, not about the count).
