author: hyaku closure (non-author integrator, @m_opus)

# mori round 31 — verifier spot-check (non-author closure)

Lane-round mori 31 (L1 `MoriR31`). Base `a12c68ae81257fb6f918bb165bcb39c73f82d212`, landed tip
`52435f2f425c2b4a5e7ba63d7abc1292b8736367`, fleet report `.ufo/reports/round-31/mori.md` (`58133def`). Closure run
2026-10-23 (from 00:27Z) by a fresh hyaku closure session that did not author the round. Seven read-only seats
re-checked parts of the round (TimelineA1, A1Loosening, C1Remeasure, C2Evidence, HarmAxes, SpotGate, Conformance).
The C2 verdict below rests on committed evidence; the closure did not run `tools/mori-blind-check.sh` itself. Two seats
(A1Loosening, HarmAxes) did run `count-c2.py`/`count-c2-a1.py` (which execute the tool) inside the counters' own
`/tmp` sandboxes. Those runs are reported as corroboration only. No tool was installed.

Driver digest (copied from `.ufo/watchdog.log`):
`2026-10-22T20:27:52-03:00 launch mori round=31 pgid=1476880 driver=hyaku-inline attempt=1`;
`2026-10-22T21:26:46-03:00 complete mori round=31; hyaku-inline attempt=1`.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by the lane identity | `git log --format='%an %ae %H %ad' -- .ufo/reports/round-31/mori.md` | `mori-shokunin mori@shokunin.local 58133def… 21:26:29 -0300`, one commit. The lane tip `52435f2f` was committed at 21:25:33, before the report | pass |
| `SHONEN` heading | report `:101-109`; `grep -cE '^- \[.\] ' SHONEN.md` | 4 lines, one per box, all `[~]`; `SHONEN.md` has 4 boxes | pass |
| Cited hashes exist and are ancestors of `master` | `cat-file -t` + `merge-base --is-ancestor <h> master` for every hex token in the report | 13/13 unique commits (`a12c68ae 2124cbcd 8baccf4a 1d94055d 7973034b 3b92ccbb 5b728304 458ff1c3 a29f3e3f efcb7324 d0cac478 fde0b0b0 52435f2f`; 15 spellings including full-length duplicates) are ancestors. `1442c14e…` is the C2 fixture sha256 prefix, not a commit, and the report labels it that way | pass |
| Pushed, nothing ahead | `scripts/hyaku/jj-lane.sh state <lane>` | `branch=master local=remote=52435f2f… ahead=0 behind=0 head=detached tracked=0 untracked=1` | pass |
| Uncommitted round work | `git status --porcelain`; `find .scratch -type f -newermt '2026-10-22 20:27:52' \| wc -l` | only `?? .scratch/`. The count is `0`; the newest mtime is 2026-10-21 12:30:50 (`round22/measure3/…`, 151 344 files). This is pre-round scratch, not round work, and the report names it | pass (named) |
| Prompt carries the template contract | Conformance seat: rendered `kimi-shokunin/templates/round-prompt.md` vs prompt `:1-140`; substituted `lane-addendum.md` vs prompt `:141-365` | 1 hunk (`<mori-repo>` → `mori-shokunin`, the documented legacy fill); addendum is verbatim (diff exit 0), including §9 with the do-nothing-control and `(kumitate r42)` bullets. The prompt was committed `64550ad` at 20:27:51 | pass |
| Report minimum content | PROTOCOL `:150-175` | work performed, landed changes each tied to a LOG entry (LOG `:1990`, `:2009`, `:2013` exist at the tip), Sources & frontier, Trend verdicts, Stale-lane line | pass |

The report records real, checkable work. It is not a marker, so the status is `ok`.

Observation (not a defect): the freeze commit `2124cbcd` has author date 19:54:19, before the 20:27:52 launch, and
committer date 20:37:48. The author date is the jj change's creation time. No evidence is future-dated.

## 2. Ruling on amendment A1 (before data or not)

The orchestrator asked whether A1 (`7973034b`, committed 20:52:48 -03 = 23:52:48Z) counts as declared before data. Addendum §9 says:
"The claim is judged on the counter, kill rule and predicate declared before data. A rule changed after any seat has
scored is not the claim's rule". Precedents: kumitate r42 rejected an A1 that came after build seats had scored real
work. kake r35 accepted an amendment that "landed before any build measure, after control-only data".

Seat TimelineA1 listed every counter run before 23:52:48Z. Sources: round session transcripts, scratch mtimes and
commit times.

| Pre-A1 run | Input scored | Kind |
|---|---|---|
| L1 23:38Z, `count-c1.py`/`count-c2.py` | entering tip, controls a/b, do-nothing port, shortcuts 1–2 (`evidence/c1-controls.txt`, `c2-controls.txt`) | control |
| MutFixturePower 23:45Z, `count-c2.py 8baccf4a --tool-file` | its own rule-text reference script and mutants M1–M6 | mutant/control |
| CriticSizing 23:48Z | `oracle-c2.sh` (answer-key oracle) → `C2=met`; junk table `1f5710a8` → `C1=met` | shortcut |
| CriticC1Counter 23:49Z | falsifier `9140d11c` (HTML-commented, duplicate rows, renumbered ids) → `C1=met` | shortcut |
| CriticC2Counter 23:49Z | falsifiers a/b/c/e/p → `C2=met` | shortcut |
| ReviewLessonGateFormat 23:51–23:52Z | synthetic `https://fixture.invalid/…` Gate rows; round-30 committed rows | synthetic / prior round |
| SrcPidMax 23:46–23:47Z | imported `count-c1.py` helpers (`cells`, `unescape`, `norm`) on its own drafted S173 Gate row: "cells 6 … quotes 3 [21, 9, 17] in_copy True" | real draft, format check only, no `main()`, no predicate verdict |

Committed corroboration: the C1 entry first lands at `5b728304` (20:59:44) and the C2 tool at `458ff1c3` (21:04:51),
both after A1. `git rev-parse 7973034b:tools/mori-blind-check.sh` fails because the path is absent there. The builder
tool files were first written at 23:57:51Z and 23:58:50Z, and the entry draft at 23:56:57Z (scratch mtimes), all after A1.
No transcript shows the L1 reading builder output or `SrcPidMax.md` before A1. The A1 fixtures (`c2-fixtures-a1.json`,
sha `133547ee…`) were written at 23:50:54Z by an eval that runs no tool.

**Ruling: A1 counts as declared before data.** Before A1, only controls, shortcuts, mutants and synthetic fixtures
had been scored. That is the kake r35 case, not kumitate r42. Two caveats are on record:
- SrcPidMax ran a per-row format check of one real draft with the counter's helper functions. It printed no C1
  verdict, A1 changes nothing that this row's check bears on, and the L1 had not read it.
- The lane's own M3 addendum says A1's C1 thresholds were set while wave-1 drafts existed, though unscored. A1 only
  adds conditions, so setting them with drafts in view cannot make "met" easier.

**M5, verified.** A1's C2 counter appends a nonce line to every brief (`count-c2-a1.py:55`), so it cannot see a
tool that drops a brief's last line. A1Loosening built that mutant from the tip tool. Results: `count-c2.py` →
`exact=7/16`, `C2=unmet`; `count-c2-a1.py` → `runs_met=2/2`, `C2=met`. A1's text "nothing in P-C1 or P-C2 is removed
or loosened" is therefore false for C2. The lane disclosed this as M5. One correction to M5: the masked set is the
9 fixtures with an expected hit on their last line (F02, F06–F08, F10, F11, F13, F15, F16), not "ten end on a list
entry".

Consequence: P-C2-A1 alone is weaker than P-C2 at end-of-file, and P-C2 alone is met by answer-key oracles. Both
predicates were declared before data. **C2 is therefore judged on both, and the tool must meet each.** Every
committed control fails at least one of them. The EOF-drop mutant fails P-C2. The oracles and lookups fail P-C2-A1
(`evidence/c2-a1-controls.txt`).

## 3. Claims

### C1 — depth: watchdog identity decision table — **verified (re-measured)**

Re-measured at `52435f2f` by seat C1Remeasure, in a clean clone and over committed bytes:

- Entry `corpus/knowledge/watchdog-identity-r31.md`: `source:`/`verified-at:`/`recheck:` present; 0 HTML comments,
  0 fence lines. One table with header `observation|reading|verdict|sources`. 14 data rows, 14 distinct. Reading cells
  have 28–77 words.
- Cited ids ≥ S161: 12 distinct (S161–S165, S167, S169–S174). S166 and S168 are not cited.
- Each of the 12 has exactly one SOURCES row with status `mined`. None of the 12 URLs is in
  `git show a12c68ae:corpus/SOURCES.md` (count 0), and the URLs are pairwise distinct.
- Each has one admit Gate row (`corpus/lessons/round-31.md:72-85`) with an https URL and a 64-hex sha. The 14 located
  quotes have 3–22 words.
- `sha256sum` of each committed `corpus/evidence/sources-r31/S###.src` equals its Gate sha (12/12).
- SKILL.md has 6 lines of ≥12 words naming `Round31` and the entry path.
- `.ufo/waves/round-31/r1/JudgeC1Rows.md` (`judged-revision: efcb7324`) names rows 1–14 once each: 13 supported,
  row 9 unsupported, and every supported row cites a new id. `git diff efcb7324 d0cac478 -- <entry>` is empty. At the
  tip, row 9 additionally carries an `[INFERENCE]` marker (`fde0b0b0`), which the report discloses.
- `python3 .ufo/waves/round-31/count-c1-a1.py 52435f2f` → "… supported=13 supported_new=13 unsupported=[9]
  skill_rows=6 C1=met exit=0", `fetch=ok` ×12. `count-c1.py 52435f2f` → "rows=14 rows_ok=14 new_ids=12 … gates_ok=12/12
  copies_ok=12/12 fetch_ok=12/12 skill_rows=6 C1=met exit=0". Both counters at `a12c68ae` → `entry=absent C1=unmet
  exit=1`.

Before → after under P-C1-A1 is `unmet` → `met`, and the same under P-C1. These match the report
(`evidence/c1-before.txt`, `c1-after.txt`). Do-nothing and shortcut controls are unmet under P-C1-A1 (5/5,
`evidence/c1-a1-controls.txt`, `3b92ccbb`). C1 is the round's sourced claim. The rows are substantive (the judge
receipt cites quote lines and live-probe lines per row), and the claim works a new surface (FR5 ground with no prior
entry), not a re-score.

### C2 — operability: `tools/mori-blind-check.sh` — **verified (evidence-verified)**

Committed evidence, per PROTOCOL §Gate standard (Closure consequence); seat C2Evidence did not execute the gate.

- The tool is absent at `a12c68ae`, `8baccf4a` and `7973034b`. Its only commit is `458ff1c3`. The blob is
  `3c26ef69…` at `458ff1c3`, `d0cac478`, `fde0b0b0` and `52435f2f`.
- `git show 52435f2f:tools/mori-blind-check.sh | sha256sum` → `79b774f7…beb8`. That equals `blob_sha256` in
  `evidence/c2-after.txt` and `c2-tip.txt`.
- `c2-tip.txt` (measured at `d0cac478`, the same tool blob): under A1, "scanned=27 blind_violations=24 hit_lines=24
  duplicate=0 stray=0 fixtures=27 exact=27/27" in both runs, `C2=met exit=0`. Under the original counter,
  "scanned=16 … exact=16/16 C2=met exit=0".
- Fixtures: `c2-fixtures.json` → `1442c14e…` and `c2-fixtures-a1.json` → `133547ee…`. Both equal the contract digests
  and are unchanged since they were committed.
- Answer-key strings in the tool bytes: `c2-fixtures` 0, `count-c2` 0, `fixtures-a1` 0.
- Controls:
  - `evidence/c2-controls.txt`: do-nothing 10/16, shortcut1 3/16, shortcut2 4/16, all `C2=unmet`.
  - `evidence/c2-a1-controls.txt`: 8 A1 controls, all `C2=unmet`. The do-nothing control scores 15/27.
  - Before value: `count-c2.py a12c68ae` → `C2=error exit=2` (fixtures absent). This is M1, and an appended
    SCORECARD correction discloses it. At the freeze `2124cbcd`, `tool=absent C2=unmet`.
- Self-test: `--selftest` → `PASS exit=0` (`evidence/c2-tool-selftest-and-r30.txt`). The round-30 writer wave at
  `5c99f2d4` gives `scanned=4 blind_violations=3 exit=1`.
- Corroboration only: seat runs at `52435f2f` gave `count-c2.py` → `exact=16/16 C2=met`, `count-c2-a1.py` →
  `runs_met=2/2 C2=met`, and a no-nonce copy of the A1 counter → `exact=27/27` twice. The tip tool is not affected by
  the M5 hole.

Before → after is `tool absent / unmet` → `met` under both P-C2 and P-C2-A1. This is a new permanent tool surface:
the pre-existing blindness checks were only wave-local `.ufo/waves/round-{29,30}/check-blind-wave.sh`. The claim
supersedes the round-30 gate (routed D1), whose bytes are unchanged.

## 4. Per-axis verdicts and no-harm

Command: `git diff a12c68ae 52435f2f -- SCORECARD.md` → +41/−0. It holds the round-31 declaration and appended
corrections, including the C2 before cell (M1), and no score changes. `git diff --diff-filter=D a12c68ae 52435f2f` is
empty. `git diff a12c68ae 52435f2f -- .ufo/waves/round-30/ tools/mori-oom-killers.py tools/mori-census.sh PROVINCE.md`
is empty.

Append-only files:
- LOG.md: 51/0, one end hunk.
- SKILL.md 27/0, QUALITY.md 16/0 (94 supersedes 93 by name), README.md 14/0.
- SOURCES.md 15/1: the one touched row is S120, where only `used-by` gains the r30 entry.
- `earlyoom-invocation-scope-r30.md` 24/7: the D4 in-place sweep that QUALITY 77 mandates, with the old text quoted in
  an appended correction section.

| Axis | Verdict | Evidence |
|---|---|---|
| depth | improved | C1 verified (§3); score stays 5 unless a closure states the move. This closure states none |
| operability | improved | C2 verified (§3); the score stays 7 |
| coverage | unchanged | no coverage claim. The frontier step (+14 SOURCES rows, README FR5/D5 map rows) is not an axis claim |
| freshness | unchanged | no claim; the D4 correction is a quality repair |
| calibration | unchanged | the declared before cells reproduce, except M1. M1 was disclosed by an appended correction before closure, so it is not a standing mismatch |
| adjacency | unchanged | `PROVINCE.md` is unchanged; sibling prior art (souji, tameshi, kumitate) appears in prose only and is not cited as mori rows |

No axis was harmed.

## 5. Discernment spot-check (`corpus/lessons/round-31.md` `## Gate`)

Seat SpotGate re-fetched each source live with `curl -sSL --fail -m 60 <url> | sha256sum` and compared quotes against
the stated lines.

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S161 | admit, A, mined | gitlab procps-ng v4.0.7 `man/pgrep.1` → `c2024c38…1e35` | agree | live sha = Gate sha = `S161.src`; quotes exact at `:105-108`, `:305`, `:318-324`; `wc -w` 21/10/19 = labels, all ≤25 |
| S164 | admit, A, mined | torvalds/linux v7.2 `fs/exec.c` → `44e4185b…72c7` | agree | live sha = Gate sha = `S164.src`; quotes exact at `:1096`, `:1257`; 7/3 words = labels |
| S171 | admit, A, mined | man-pages-6.20 `proc_pid_stat.5` → `cba82e47…0bcd` | agree | live sha = Gate sha = `S171.src`; quotes exact at `:43`, `:228-229`, `:39`; 8/17/10 words = labels |
| S166 | reject (duplicate URL) | torvalds/linux v7.2 `fs/proc/base.c` → `cef1a2cf…15c6` | agree | same URL and sha as S127 (`SOURCES.md:133`) and S148 (`:154`); no copy committed |
| S168 | reject (duplicate URL) | torvalds/linux v7.2 `Documentation/filesystems/proc.rst` → `e760f716…d126` | agree | same URL as S082 (`SOURCES.md:88`), whose recorded prefix `e760f716f8278dee` the live sha extends; no copy committed |

Newly written SOURCES row S171 (`corpus/SOURCES.md:177`): its anchors `:35-39,42-43,49-50,56-57,69-70,227-233` were
each confirmed in the fetched bytes. The row has no quote cell (this lane's SOURCES schema keeps quotes in the Gate
row). Its Gate quotes have 8, 17 and 10 words, all ≤25. Two quotes were also re-checked with `sed -n`: the S172
`:34-35` and S173 `:1092-1093` locators that the lane kept against the row judge are correct.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → twelve `W04` (ten
pre-existing plus S166 and S168, both `rejected` duplicates) and `mori ok`, exit 0. This matches
`evidence/census-end.txt`.

Agreement: 5/5 (3 admits, 2 rejects).

## 6. Trend verdicts

- **expansion: improved.** One new entry on FR5 ground the coverage map did not hold (`corpus/README.md` FR5 rows).
  It cites 12 `mined` tier-A rows (S161–S165, S167, S169–S174), and the D5 map row was added for the round-30 entry.
  No entry was removed.
- **quality: improved.** The new gate has a self-test (C2). The round-30 entry's false "reports its version" was
  corrected at every mention (D4). QUALITY 94 supersedes the unfalsifiable 93 by name. No admitted entry failed its
  re-check: row 9 is marked `[INFERENCE]` and counted unsupported.
- **discernment: improved.** The outside spot-check agrees with the Gate on both admits and both rejects (5/5). The
  lane's own critics caught the counter shortcuts before data (M3). The M1 and M5 mistakes are mined into lessons with
  fixes. The lane graded itself `unchanged`; per LEARNING.md the observable (spot-check vs gate) is agreement on both
  sides.

## 7. Ruling

Status `ok`. C1 verified (re-measured) and C2 verified (evidence-verified), each on the predicates declared before data:
A1 counts as before data (§2), and C2 meets both its original predicate and A1. No axis harmed. **Admitted.**

SHONEN: all four boxes are `[~]` (asserted by author). Box 1 (SKILL decision tables with cited sources) and box 4
(PROVINCE accurate) look checkable by a non-author from this round's artifacts. Promotion is operator-owned and is not
decided here.

## 8. Routed defects (the lane owes these next round)

1. **M5 correction:** append a correction to lesson M5. The nonce masks a dropped last line on the 9 fixtures with an
   expected last-line hit (F02, F06–F08, F10, F11, F13, F15, F16), across every rule, not "ten end on a list entry".
   Any future perturbing amendment keeps the original predicate as an explicit conjunct in the counter.
2. **Gate registry row:** `SKILL.md:772-780` lists the blind-writer gate without a pinned-value path, write scope or
   owner field (PROTOCOL §Gate standard, Registry). The gate also has no frozen-run baseline whose `expected.json` pins
   snapshot digests (§Two evidences); the r30 regression receipt is not digest-pinned.
3. **Frozen wording:** the `count-c2.py` docstring omits P-C2's "no hit line outside the 16 briefs" (the code enforces
   it; contract `:6` promises the same sentence). Record it in the next contract and do not edit the frozen file.
4. **Judge-vs-tip drift:** the tip entry differs from the judged `efcb7324` by row 9's `[INFERENCE]` marker. Have the
   judge receipt name the measured tip bytes, or re-judge after the last entry edit.
5. **Counter code on real drafts:** a wave-1 seat (SrcPidMax) imported `count-c1.py` helpers on a real Gate-row draft
   while the counter was still open to amendment. Keep counter code away from real drafts until the counters are
   final, so that "before data" stays clean.
6. **Carried (lane-named, still open):** C2 rule ambiguities on round-29 briefs (RealBriefsR29); tool edge cases outside
   the 27 fixtures (setext/indented headings, CRLF, tab after `-`, `../` through allow globs, fenced openers); the
   round-30 detectors' false positives/negatives; and the FR5 census probe unchanged (`WATCHDOG_ABSENT` under the
   inline driver).
