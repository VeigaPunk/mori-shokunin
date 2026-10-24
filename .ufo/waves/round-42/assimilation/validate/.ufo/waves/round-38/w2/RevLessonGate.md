# Round 38 lesson audit — RevLessonGate

**Verdict: FAIL.** The Gate lists a candidate/admit and explicitly says there are no new rejects, but it does not record or label the required non-author admit/reject spot-check. The Mistakes section is present, but most class labels are outside the cited `mistakes.md` vocabulary. The registry-change statement `none` is true for existing cells at the scored tip.

## Section-by-section conformance

| Section / requirement | Lines | Result | Finding |
|---|---:|---|---|
| Round heading | 1 | PASS | Round 38 lesson heading is present. |
| `## Gate`: candidates and decisions | 3–13 | PASS | Gate exists at line 3; S226 is the single candidate and is marked admitted at line 9; `Rejected: none new` is explicit at lines 11–13. |
| `## Gate`: non-author spot-check | 3–19 | **FAIL — absent and unlabeled** | No verifier, reviewed admit/reject, or pending/absent spot-check statement is recorded. `Rejected: none new` also leaves no new reject candidate to sample. A case-insensitive search for `spot.check|spotcheck|non.author` in the lesson returned **No matches found**. The `corpus/lessons` listing contained `round-38.md` but no `round-38-verifier-spotcheck.md`. Thus the required sample of at least one admit and one reject is not evidenced. |
| Registry-cell change accounting | 14–16; `corpus/SOURCES.md:232` | PASS | The lesson says `none` and limits it to existing rows. The entering-to-scored-tip diff below adds the new S226 row and the round-38 search-log entry, with no deletion/rewrite of an existing row. S226's new row records `mined`, `on-release`, and its `used-by` path at `SOURCES.md:232`; it is an insertion, not an old→new edit. |
| `## Mistakes`: section and row shape | 21–33 | PARTIAL | Heading and table are present; rows M1–M9 have class, evidence, captured-by, and fix columns (lines 23–33). |
| `## Mistakes`: vocabulary | 25–33 | **FAIL** | The cited vocabulary in `corpus/evidence/sources-r36/S205.src:171–178` is `vacuous`, `survivor`, `stale-premise`, `reference-drift`, `number-drift`, `scope`, `attribution`, `landing`, `provider`. M1–M6 (`tooling`, `measurement`, `tooling`, `tooling`, `measurement`, `wave design`) and M7 (`transcription`) are not in that list. M8 and M9 use the allowed class `landing`. Therefore 7 of the 9 rows in the current worktree are off-vocabulary; all six rows present at the scored tip were off-vocabulary. |
| `## Round shape and debts` | 35–53 | PRESENT; not scored | Section is present. Its substance was outside this assignment's requested checks. |
| `## Known residuals` | 55–60 | PRESENT; not scored | Section is present. Its substance was outside this assignment's requested checks. |

## Provenance and exact command outcomes

- Read `corpus/lessons/round-38.md` and `corpus/SOURCES.md`; the line references above are from those files. The cited vocabulary statement is `corpus/evidence/sources-r36/S205.src:171–178`.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --unified=0 e33bb561712b32f46861362a3fa43762fa70ae4f f725f3076972e6e70595b5ac8279be524a111ff8 -- corpus/SOURCES.md` → `1 file changed, 3 insertions(+), 0 deletions(-)`. Its hunks add S226 at line 232 and the round-38 bounded-search log at line 286. This supports the lesson's `none` statement for existing `status`, `recheck`, and `used-by` cells.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show f725f3076972e6e70595b5ac8279be524a111ff8:corpus/lessons/round-38.md | cmp - /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-38.md` → **not equal** (`differ: char 4725, line 31`). `git status --short -- corpus/lessons/round-38.md` returned ` M corpus/lessons/round-38.md`.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --unified=2 f725f3076972e6e70595b5ac8279be524a111ff8 -- corpus/lessons/round-38.md` → 3 insertions, 0 deletions: current worktree-only M7–M9 at lines 31–33. The scored tip contains M1–M6 only; the Gate and registry accounting are unchanged in this diff. Findings above distinguish scored-tip content from these worktree additions.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --shortstat f725f3076972e6e70595b5ac8279be524a111ff8 -- corpus/SOURCES.md` produced no output; no additional `SOURCES.md` worktree delta was observed.
- Search `spot.check|spotcheck|non.author` (case-insensitive) over the lesson → **No matches found**.

## Touched surfaces, limits

Only this audit report is written: `.ufo/waves/round-38/w2/RevLessonGate.md`. Audited surfaces were `corpus/lessons/round-38.md`, `corpus/SOURCES.md`, and the cited taxonomy excerpt in `corpus/evidence/sources-r36/S205.src`. No tool was installed or updated. I did not re-derive the factual correctness of the source quote, the S069 chronology, the lesson's C1–C3 measurements, or the residual claims; those are outside this lesson-structure audit.