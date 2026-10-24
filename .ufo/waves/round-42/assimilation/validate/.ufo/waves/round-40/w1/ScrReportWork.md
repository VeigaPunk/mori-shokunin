# ScrReportWork — seat report (scribe, round 40 w1)

## Behavior

Produced the report's **Work performed** section prose from the landed receipts,
as the item names: claim → target axis → evidence pointer, numbers quoted from
receipts (or counted over committed bytes with the method stated). No instrument
was rerun; no production file, judge, git/jj state, or fleet path was touched.

Deliverable:

- `.ufo/waves/round-40/w1/ScrReportWork-work-performed.md` (12,587 bytes) —
  sections: C1 (operability 7), C2 (depth 5), frontier/surroundings,
  **Conflicts** (3 items, verbatim), **Replay bounds** (3 items).

Coverage of the frozen contract: C1's nine checks, eleven selftest arms, nine
survivor fixtures + two-counter audit, gutted-conjunct control, parity; C2's
lane line at the tip and at `e37dcc6`, three fixture DAGs, selftest; S229, census
pair, lesson, erratum.

Report path: my seat prompt carried no `Report:` path (the generator emits a
generic trailer, `gen-wave-spec.py:44`), so this report is written to
`reportDir/ScrReportWork.md` — the same convention as the 18 sibling seat
reports already present in `.ufo/waves/round-40/w1/`.

## Commands run and outputs

Working directory `/home/vgpnk/Projects/shokunin/mori-shokunin` unless noted.
All read-only.

| command | output |
|---|---|
| `ls -la .ufo/waves/round-40/ .ufo/waves/round-40/w1/ .ufo/waves/round-40/evidence/` | `w1/` absent at first listing; `evidence/` = 41 `.txt` files; `w1/` later held 18 sibling reports |
| `python3 -c "…json.load(open('.ufo/waves/round-40/w1-spec.json'))…"` | 66 items, `reportDir=.ufo/waves/round-40/w1`, `maxLanes=66`; my item is `ScrReportWork`/`scribe`; its prompt carries the fragment instruction but **no `Report:` path** (generator trailer is generic, `gen-wave-spec.py:44`) |
| `sha256sum` over the nine paths in `evidence/freeze-r40.txt` | all nine matched the receipt: contract `6514914885…`, `count-c8.py` `4e4d50eb…`, `conform.py` `5025b966…`, gate `bde5a9a3…`, `make-survivor-fixtures.py` `8ff91db7…`, `run-c11-dags.py` `0cd7f1d2…`, `conform-v2-r39.py` `fe0be179…`, `count-c7-r39.py` `b92c65f2…`, `gate-v2-bb1f2457.py` `62cd4132…` |
| `sha256sum evidence/census-start.txt evidence/census-end.txt` | both `d823173352f740d3495cbf6ebcab456a775e22133d84ffad1661275318d14319` |
| AST compare of each `PREDICATE` literal against the contract blockquote (python, `ast.literal_eval`) | `P-C10 equal (whitespace-normalized): True` (1564/1564 chars); `P-C11 equal …: True` (1036/1036) |
| count of the **last** `supersede_timing …` line per c11 receipt (the first match is the predicate prose) | before-lane as_of=18 stale=[] S226=False EXIT=1; after-lane as_of=35 stale=[] S226=True EXIT=1; e37dcc6 as_of=33 stale=['S069'] EXIT=1; fixture-n 1/[]/0; fixture-p 1/[]/1; fixture-r 1/[]/1; red-n 0/[]/0; red-p 0/['S001']/1; red-r 0/[]/1 |
| set difference of the before/after as-of lists | added 17: `S067,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S226`; removed 0; `superseded` list 18→35; e37dcc6 `superseded` 34 |
| `git show 265a955cc:corpus/SOURCES.md \| grep -oE "supersedes S[0-9]+" \| sort -u` | 36 distinct tokens including the literal `S0` (from prose `supersedes S###`) → 35 real ids, identical to the receipt's list; `git show ede486b7:… \| grep -v "S0$" \| sort -u \| wc -l` = 35; `grep -c` = 39 both revs |
| `diff <(grep '^changed ' c11-before-lane.txt) <(grep '^changed ' c11-after-lane.txt)` | no output → the 18 `changed … superseded_by=…` lines are identical before/after |
| `grep -n "pin_only\|pin == tip\|head_at_measurement" conform.py count-c8.py` | `count-c8.py:404` (`if args.pin_only:`), `:409` (`print("head_at_measurement=%s"…)`); `conform.py:520` (regex), `:524` (`results["head_pin"] = (… pin == tip …)`) |
| `grep "FAIL" evidence/c10-after-multicounter.txt \| cat -A`; `grep -h "FAIL (survivor" …` | exact column spacing of the quoted `check … FAIL` lines verified (`check drain_bind` + 9 spaces, `check timeout_scope` + 6) |
| `grep -c "PASS " c10-after-selftest.txt`; `grep -c "^check .*PASS" c10-after.txt`; `wc -l c11-after-selftest.txt` | 11; 9; 3 |
| `grep -n S229 corpus/SOURCES.md` | `235:\| S229 \| Python execution model — Naming and binding — https://docs.python.org/3/reference/executionmodel.html#naming-and-binding \| …` |
| `ls -la corpus/evidence/sources-r40/S229.src`; `grep -c "" …` | 63,374 bytes / 869 lines |
| `cat corpus/lessons/round-40.md`; `git log --oneline -2 -- corpus/lessons/round-40.md` | 59 lines; committed at `8d3badd`; Mistakes M23, M24 present |
| `git diff --stat bb1f2457 265a955cc` | 29 files, `10980 insertions(+), 49 deletions(-)`; `SKILL.md \| 3 +-` (2 insertions, 1 deletion) |
| `git rev-parse HEAD`; `git log --oneline -3 HEAD` | `ede486b7a09afbacfb380d5871c46a8051a6dc2e`; `ede486b7`, `8d3badd`, `265a955` |
| `git status --porcelain` (head) | ` M .ufo/waves/round-40/evidence/c10-after-conjunct.txt`, ` M …c10-after-selftest.txt`, ` M …c10-red-conjunct.txt`, `?? .scratch/`, `?? .ufo/waves/round-39/scratch/` |
| `git diff -- .ufo/waves/round-40/evidence/` | sibling appends only: absolutised `command:` paths; `c10-after-selftest.txt` gains `wall_seconds: 57.371` + `real/user/sys` lines |
| `git show HEAD:.ufo/waves/round-40/evidence/{c10-after-selftest,c10-after-conjunct,c10-red-conjunct}.txt` | committed bytes quoted in the fragment (`pass=11 fail=0`; `pass=0 fail=10`; `pass=8 fail=0`) |
| `sed -n '1,40p' .ufo/waves/round-40/conform.py`; `awk 'NR>=500 && NR<=535'` | `head_pin` = counter `--pin-only` hex **equal to the lane tip**; evaluator line: `results["head_pin"] = (… pin == tip …)` |
| `awk 'NR>=392 && NR<=415' .ufo/waves/round-40/count-c8.py` | `--pin-only` runs `git_out(repo, ["rev-parse","HEAD"])` and prints `head_at_measurement=%s` |
| read-tool reads of 37 receipts under `evidence/`, `run-c11-dags.py`, `conform-scope-r40.md`, `round-39-erratum.md`, peer `ExeGateLane.md` | receipt text quoted in the fragment |

**Not run by this seat** (no check claimed as passed): `conform.py` (any mode),
`tools/mori-sources-appendonly.py` (any mode), `run-c11-dags.py`, the census
script, `make-survivor-fixtures.py`. They are the executor seats' receipts; this
seat quotes them and does not decorate them with a rerun.

## Touched surfaces

- Written: `.ufo/waves/round-40/w1/ScrReportWork-work-performed.md` (only file).
- Temp only: `/tmp/scrreportwork-prompt.txt` (scratch extraction of my seat prompt).
- No edits to product code, instruments, receipts, SCORECARD, lesson, fleet repo,
  `.ufo/state/`, watchdog log, Git index or jj state. No commit/push.

## Findings (for the canonical judge; reported verbatim, not adjudicated)

1. **C2 lane count: three numbers, none matching the receipt.** Contract
   `contract.md:137` declares `superseded_as_of=[19 ids incl. S226]`, kill rule
   `contract.md:145` keys on "the declared 19 ids"; the wave context and the
   ExeGateLane routing entry say 34; `corpus/lessons/round-40.md` M24 and the
   SCORECARD after-cell say "**34** as-of ids" with the class "16 rows: S226 plus
   15 earlier". `c11-after-lane.txt` lists **35** ids; the before→after delta is
   **17** ids; the static registry count at `265a955cc` is also 35. Same conflict
   reaches the kill rule's discriminator: 35 ≠ 19 and 35 ≠ 34.
2. **dag-p "no fabricated changed line" is not what the receipts show.** Both
   `c11-red-firstparent.txt` and `c11-after-fixture-p.txt` print
   `changed S001 superseded_by=S002` and `appendonly_violations=1`; the v2→v3
   difference is `stale_supersede=[S001]`→`[]` and `superseded_as_of=[]`→`[S001]`.
   The gate's own dag-p selftest row also expects `"round_changed": ["S001"]`.
3. **dag-r changed-event claim is not discriminated by the pair.** The contract's
   before-cell says v2 "prints a `changed` event"; `c11-red-readd.txt` has no
   `changed` line, only `round_changed=[S008]`/`EXIT=1`, and
   `c11-after-fixture-r.txt` carries the same `round_changed=[S008]`/`EXIT=1`.
   The observable discriminator is `superseded`/`as_of` `[]`→`[S008]`.
4. **Census "exit 0" is not in the receipts.** `census-start/end.txt` carry the
   16 `W04` rows and `mori ok …`, no exit-status line; their byte-identity is
   verified (sha above), the exit code is the lesson's sentence.
5. **`head_pin` is HEAD-vs-HEAD and therefore not byte-replayable.** Both sides
   read `git rev-parse HEAD`; the receipt's `pin=265a955cc… tip=265a955cc…`
   records measurement-time HEAD. Lane HEAD is now `ede486b7`, so a replay prints
   different hex on both sides while still passing. This is a replay bound, not a
   claim failure — reported because the receipt line cannot be re-derived
   verbatim after HEAD advances.
6. **C2 selftest receipt is summary-only** (3 lines): `pass=15` is not
   individually evidenced by 15 arm lines in the landed receipt.
7. **C1 divzero receipt cascades**: five `FAIL` lines (predicate, head_pin,
   tool_resolve, timeout_scope, timeout_state) because the crashing counter is
   the instrument under test; the contract's before/after contrast (exit 2, no
   FAIL line → timeout_scope violation) is still visible.
8. **Worktree drift by siblings**: three evidence receipts carry uncommitted
   appends (absolute `command:` paths; `wall_seconds: 57.371` on
   `c10-after-selftest.txt`). All fragment quotes are from committed blobs.

## Out of scope / not done

- No production edits, no SCORECARD/lesson/erratum edits, no commits, no judge
  invocation, no fleet-repo writes, no sibling-lane reads/writes beyond the
  named peer report.
- The round's "≥1 mined mistake" requirement is satisfied on paper by
  `corpus/lessons/round-40.md` M23/M24; I did not verify the lesson's content
  beyond reading it.
- Performance/wall-time numbers (e.g. `wall_seconds: 57.371`) are a sibling's
  uncommitted append and are not used in the fragment.

## Artifact paths

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/w1/ScrReportWork-work-performed.md`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/w1/ScrReportWork.md` (this report)
