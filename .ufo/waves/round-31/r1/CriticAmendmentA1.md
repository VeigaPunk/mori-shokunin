# r1 — CriticAmendmentA1 (non-author critic of contract Amendment A1)

Seat: MoriR31.CriticAmendmentA1. Judged committed bytes at `a29f3e3f7f7259afb07df29c5ee8f68882712e96`.
Scratch: `/fast/scratch/hyaku/mori-r31/CriticAmendmentA1/`. Times are local (-03:00).

## Verdict

**A1 is a before-data amendment, not an after-data rule change. For C1 it is a pure tightening. For C2 it is
not a pure tightening.** P-C2-A1 changes the inputs the tool runs on: it appends a nonce line to every brief.
That removes the end-of-file coverage that 10 of the 16 frozen fixtures exercise. So a tool that fails P-C2
can meet P-C2-A1. This contradicts A1's preamble ("nothing in P-C1 or P-C2 is removed or loosened",
`contract.md:115-116`). It is the same class of defect as round-30 D2 (a relaxation the amendment did not
disclose). It is fixable. It does not change the outcome at this tip, because the tip tool also meets the
frozen count-c2.py.

**Strongest counterexample (run).** I copied the tip tool and made the classic bash mistake that drops the last
line of a file. The `while` loop condition (`mori-blind-check.sh:113`) loses `|| [[ -n $line ]]`, and
`done <<< "$content"` (`:203`) becomes `done < <(printf '%s' "$content")`. The mutant is saved as
`.../CriticAmendmentA1/tool-eofdrop.sh`, and the diff is those 2 lines.

| tool | `count-c2.py a29f3e3f --tool-file` | `count-c2-a1.py a29f3e3f --tool-file` |
|---|---|---|
| tip tool bytes (`tool-tip.sh`) | exact=16/16, C2=met, exit 0 | 27/27 in both runs, runs_met=2/2, C2=met, exit 0 |
| last-line-drop mutant | **exact=7/16, C2=unmet**, exit 1 (F02 F06 F07 F08 F10 F11 F13 F15 F16 diff) | **27/27 in both runs, C2=met**, exit 0 |

Receipts: `.../CriticAmendmentA1/tool-eofdrop.c2.txt`, `tool-eofdrop.c2a1.txt`, `tool-tip.c2.txt`,
`tool-tip.c2a1.txt`.

**Mechanism.** `count-c2-a1.py:55` writes each brief as `lines + "\n<!-- nonce … -->\n"`, so no brief's last
real line is ever the file's last line. Ten frozen fixtures end on an entry line: F02, F06, F07, F08, F09,
F10, F11, F12, F13 and F14. All 11 A1 fixtures do too, but the nonce covers them as well. The contract's
reason for the nonce, "under rule clause 3 it changes no expected hit" (`contract.md:156-157`), is true about
expected hits. It is false about what the tool is tested on: with the nonce, no block ever reaches end of
file.

**Smallest safe correction.**
- Judge C2 as met only if both `count-c2.py <tip>` and `count-c2-a1.py <tip>` print `C2=met`. Both counters
  were committed before any tool existed (`2124cbcd`, `7973034b`), so requiring both is not a new after-data
  rule.
- Record the undisclosed loosening as a D2-class mistake row next to QUALITY 25.
- At `458ff1c3` both counters meet: `evidence/c2-after.txt:64` (A1) and `:89` (frozen). My runs on the
  tool bytes at `a29f3e3f` agree. So the verdict does not flip.
- Impacted axes: operability (C2's evidence is weaker than stated) and calibration/provenance (the
  preamble's "nothing loosened" is false).

## (1) Was any round-31 entry, Gate row or tool scored before 7973034b?

Commits (`git log a12c68ae..a29f3e3f`):

- `2124cbcd` 20:37:48: freeze.
- `8baccf4a` 20:38:46: before and control receipts.
- `1d94055d` 20:46:54: repairs and the wave-1 spec.
- `7973034b` 20:52:48 (author 20:52:47): A1.
- `3b92ccbb` 20:53:24: A1 controls.
- `5b728304` 20:59:45: the C1 entry first enters the lane.
- `458ff1c3` 21:04:52: the C2 tool first enters the lane.
- `a29f3e3f` 21:05:28: wave-1 reports and after-receipts.

Wave 1 had 41 seats, including BuildBlindTool and BuildBlindToolAlt (`wave1-spec.json` items). The registry
was created at 23:42:20Z (20:42 local, `w1/swarm-registry.json`). Every counter run I found before
7973034b scored a control or a probe, not the claim's entry or tool:

- **Committed controls**:
  - `evidence/c1-before.txt` scores a12c68ae.
  - `evidence/c1-controls.txt` scores 2124cbcd plus sandbox shortcuts eddaa8d5 and 9d91f953. Its line 1
    label "do-nothing: the entering tip" is attached to a 2124cbcd run (`:2`). This is a harmless mislabel;
    the receipt that really scores a12c68ae is c1-before.
  - `evidence/c2-before-base.txt` and `evidence/c2-controls.txt` score the tool-absent state and three
    control scripts.
- **CriticSizing** (report born 20:48:17):
  - count-c1.py on the junk sandbox 1f5710a8: C1=met (`w1/CriticSizing.md:100-108`).
  - count-c2.py `--tool-file oracle-c2.sh`: C2=met (`:123-128`).
  - Both are falsifier controls.
- **CriticC1Counter** (20:48:52): count-c1.py on the falsifier sandbox 9140d11c: C1=met
  (`w1/CriticC1Counter.md:22-37`). This is a control.
- **CriticC2Counter** (20:49:05): falsifiers a, b and c, and a partial parser, scored at 2124cbcd: C2=met
  (`w1/CriticC2Counter.md:28-32,72-74`). These are controls.
- **MutFixturePower** (scratch 20:44:55–20:46:39): a full rule implementation `reference.sh`, written by the
  seat from the rule text, scored 16/16 C2=met (`M1-pristine.txt`), plus 6 mutants (`w1/MutFixturePower.md:27-29,96-101`).
  - Its role was a power probe, so I class it as a control.
  - It is also a complete C2-meeting implementation that was scored before A1. I re-scored it under A1:
    `count-c2-a1.py a29f3e3f --tool-file .../MutFixturePower/reference.sh` gives 27/27 in both runs,
    C2=met (`.../CriticAmendmentA1/ref.c2a1.txt`).
- **SrcPidMax** (report 20:45:26–20:47:29) imported `count-c1.py` and ran its `cells`/`norm` on its S173
  Gate row (`w1/SrcPidMax.md:93-104`). This is a partial format check of data, not a score of P-C1. It does
  mean the contract's phrase "no … Gate row … scored by either counter" (`contract.md:113-114`) is slightly
  overstated.
- **No full counter run scored a round-31 entry or tool before A1.**
  - The entry first exists at 5b728304 and the tool at 458ff1c3.
  - The first runs on lane data are `evidence/c1-after-prejudge.txt` (at 458ff1c3, born 21:05:04) and
    `evidence/c2-after.txt` (21:05:04).
  - The builder scratch directories were born after A1: BuildBlindTool at 20:57:51 and BuildBlindToolAlt
    at 20:58:04.
- **Data the L1 could see before A1** (not scored): all 13 Src* reports, born 20:43:53–20:48:38;
  DraftSkillRowsC1 (20:44:38); and DraftEntryC1 (born 20:48:23). So the A1 C1 thresholds were chosen with
  candidate Gate rows and drafts in view. That does not loosen anything, and §9's trigger is "scored", not
  "seen". `[INFERENCE]` A tightening calibrated on visible drafts is weaker evidence of independence than one
  set blind.

## (2) Does A1 remove or loosen any condition?

**C1: no.** I compared `count-c1.py:80-170` with `count-c1-a1.py:89-239` line by line.
- These conditions are re-implemented identically: head lines, table detection, `len(row)==len(hdr)`, ids
  resolving, the ≥8 / ≥6 / ≥4 counts, exactly one SOURCES row, exactly one admit row, https URL, 64-hex sha,
  quotes ≤25 words, copy sha and quote containment, and the fetch sha.
- The quote regex is the same (`ANY_QUOTE_RE` `:30` equals `count-c1.py:147`). A1 additionally requires that
  each quote is located and that the located count equals the total count (`:182`).
- The fence toggle (`:111-114`) adds a flag without changing which tables are found.
- The SKILL check is stricter: it requires the `\bRound31\b` word boundary, the full `corpus/knowledge/...`
  path rather than `knowledge/...`, at least 12 words, and distinct lines (`:236` vs `count-c1.py:167`).
- New conditions: no HTML comment, table not in a fence, distinct rows, readings of at least 8 words, status
  mined, URL not registered at the entering tip, distinct URL and sha, at least 2 shared quote words, and the
  judge receipt.
- Receipts agree: at 458ff1c3 the frozen counter gives C1=met while A1 is unmet only on `judge`
  (`evidence/c1-after-prejudge.txt:20,45`). Two falsifiers flip from met to unmet
  (`evidence/c1-a1-controls.txt:66-69,87-90`).

**C2: yes, one exercised condition is lost (counterexample above).**
- Unlike P-C1-A1, P-C2-A1 does not include "P-C2 holds" as a conjunct (compare `contract.md:127` with
  `:141`). It re-runs the checks on modified briefs.
- Stricter: randomized order and mtimes, bwrap, PATH-only environment, answer-key byte scan, duplicate check,
  2 runs, and extra `scanned=` lines counted as stray.
- Exit check: equivalent. `count-c2.py:135` derives 1 from the fixtures; `count-c2-a1.py:110` hard-codes 1.
- Looser: the end-of-file block case.
- `[INFERENCE]` The bwrap PATH-only environment is a second, smaller input change. A tool could depend on
  that environment and pass under A1 but not under count-c2.py's full environment. I did not build such a
  tool.

## (3) Were the A1 fixtures written before any builder tool existed?

**What I can establish, from birth times (`stat %w`, xfs):**
- `c2-fixtures-a1.json` was born at 20:50:54. Its sha256 at the tip is `133547ee…5fc`, matching
  `contract.md:152` and `count-c2-a1.py:21`. It was committed at 20:52:48.
- `count-c2-a1.py` was born at 20:51:27 and `count-c1-a1.py` at 20:52:10.
- The builder files were born later:
  - `BuildBlindTool/`: directory 20:57:51, `mori-blind-check.sh` 20:57:51, `allow-r30.txt` 20:58:02.
  - `BuildBlindToolAlt/`: directory 20:58:04, `mori-blind-check.sh` 20:58:50, `run-differential.sh`
    21:00:39.
  - Builder reports: BuildBlindTool.md at 21:03:53; BuildBlindToolAlt.md at 21:05:59, uncommitted at the
    tip (`git status`: `?? w1/BuildBlindToolAlt.md`, `?? evidence/c2-alt-implementation.txt`).
- The lane tool first appears at 458ff1c3. So no builder artifact existed on disk in scratch or in the lane
  before the A1 fixtures.

**What I cannot establish:**
- What the builders held before 20:57. They were dispatched around 20:43 and wrote nothing under their
  scratch for about 14 minutes. Writes elsewhere (/tmp self-test directories self-delete) or messages to the
  L1 are not visible to me. I did not read session transcripts.
- Whether the L1 checked the A1 expectations against MutFixturePower's `reference.sh`. That is a complete
  seat-written implementation, born 20:44:55, before the A1 fixtures. It agrees 27/27 with them, which is
  consistent both with correct fixtures and with fixtures validated against it.
- The A1 fixture shapes (`+ ` markers, lowercase or other-level "opened files" openers, prose closing a
  block) match MutFixturePower's unkilled M1–M3. This suggests A1 used that report, which is legitimate
  before data.
- The contract's claim "before any builder seat's tool was read" (`contract.md:153`) is consistent with the
  timestamps but cannot be fully proven. It leaves out the existence of `reference.sh`.

## (4) Same sentence in contract, docstring and receipt label?

I compared the sentences with whitespace and backticks normalized (python difflib, run at a29f3e3f):

- P-C1-A1: `contract.md:127-135` and `count-c1-a1.py:6-15` are **identical**.
- P-C2-A1: `contract.md:141-146` and `count-c2-a1.py:6-11` are **identical**.
- P-C1: identical to `count-c1.py:6-14`.
- P-C2 (frozen, before A1, not changed by A1): the docstring `count-c2.py:6-9` **omits** "no hit line outside
  the 16 briefs". The code enforces it (`:144 not stray`). CriticC2Counter already found this
  (`w1/CriticC2Counter.md:140-141`).
- Labels: the A1 counters print the same `C1=met` / `C2=met` token as the frozen counters (`count-c1-a1.py:244`,
  `count-c2-a1.py:172`). A receipt line alone does not say which predicate it reports. Only the command line
  and comments in `evidence/c2-after.txt:1,67` and `c1-after-prejudge.txt:1,23` disambiguate. The closure
  should cite the command, not the bare label.

## Commands run (all under timeout; nothing in the lane except this report)

- `git log`, `git show --stat` and `git show <rev>:<path>` on the lane (read-only). `git diff --stat 2124cbcd a29f3e3f`
  over the count-c1.py, count-c2.py, c2-fixtures.json and rule-text.md paths produced empty output, so the
  frozen files are byte-identical at the tip.
- `stat -c %w/%y` on the w1 reports, evidence, A1 files and seat scratch directories.
- `TMPDIR=<scratch> python3 count-c2.py a29f3e3f --tool-file {tool-tip,tool-eofdrop}.sh`.
- `python3 count-c2-a1.py a29f3e3f --tool-file {tool-tip,tool-eofdrop,MutFixturePower/reference.sh}`. Each run
  created and removed its own `/tmp/c2a1.*` sandbox (hard-coded at `count-c2-a1.py:40`). No `/tmp/c2a1.*`
  directory remains. `/tmp/c2a1.out` (born 20:52:58) is not mine and was left untouched.
- I did not run count-c1.py or count-c1-a1.py, which need network fetches. The C1 comparison is from the
  code and the committed receipts.
- No tools were installed or updated. bwrap 0.13.1 was already present. No processes are left running.
