# ScoutConsider — considerthese mining audit (mori round 44, wave 1)

Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`, HEAD `7cb59c68` (round-44
freeze). Read-only pass: no file edited except this report, no git mutation, no
tool installed.

## 0. Input files

`considerthese/` holds six reflections: `2026-10-19.md` … `2026-10-24.md`.
**No `2026-10-25.md` exists** — `ls -la considerthese/` shows the newest file as
`2026-10-24.md` (mtime Oct 24 10:01, committed at `e4293ad9`). So the newest
file is `2026-10-24.md`, window "commits since the 2026-10-23 review (`6bd5709`,
round-35 spot-check) through `d72ac16` (round-41 freeze)".

Marker note (observed): the literal string "not implemented" does **not** occur
in `2026-10-24.md`. The section that carries the proposals is line 19:

```
## Suggestions for improving my own reviews (proposals only)
```

The "not implemented" wording lives in the older files
(`2026-10-19/20/21.md`: "proposals only, not acted on"; `2026-10-22.md`:
"proposals only, not acted on"). For the newest file the operative corroboration
is `corpus/lessons/round-42.md:73-75` — "one unimplemented proposal mined … **No
other proposal was implemented**; the file was not edited" — and the round-43
lesson's identical section. I therefore treat all four bullets under that
heading as the live proposal set. Nothing else in the file is a proposal (the
"Things I could not verify" bullet is a finding; the three lessons are
lessons).

## 1. The four proposals and their verdicts

| # | proposal (quoted headline) | verdict | pointer |
|---|---|---|---|
| P1 | "Check that frozen instruments replay off-host" | **implemented as a criterion** (QUALITY 115); the mechanical daily sweep is **unimplemented** | `corpus/QUALITY.md:938` (added `dde525ea`, r43); no sweep tool; 10 instruments still hardcode the home path |
| P2 | "Keep a cumulative survivor ledger" | **implemented as a criterion** (QUALITY 114); the cumulative-ledger artifact is **unimplemented** | `corpus/QUALITY.md:927` (added `34b92673`, r42); survivors exist in three round trees, no tool re-runs them together |
| P3 | "Watch repository growth from scratch output" | **unimplemented** — no criterion, no lesson, no tool | absent everywhere: `grep -n growth corpus/QUALITY.md` → no hit; `grep -rn growth corpus/lessons/*.md` → only unrelated round-19/23 prose |
| P4 | "Reproduce headline numbers mechanically" | **unimplemented in general**; one round-specific instance exists, and the general form is this round's C1 (not yet landed) | `tools/mori-round41-calibration.py` (r40-only); `.ufo/waves/round-44/figures.tsv` **absent** at HEAD |

## 2. Evidence per proposal

### P1 — "Check that frozen instruments replay off-host"

Observed implementation. QUALITY 115 (`corpus/QUALITY.md:938`) reads: "A frozen
instrument's green control must replay with `--repo` pointing at a scratch
clone, not only a hardcoded home path. … Rationale: considerthese/2026-10-24.md,
'Check that frozen instruments replay off-host' (operator-authored reflection,
mined round 43; not edited)." Added by `dde525ea` (round-43), confirmed with
`git log -S "115. A frozen instrument's green control" -- corpus/QUALITY.md`.
`corpus/lessons/round-43.md:107-114` records the mining and the r43 evidence
(`count-c1s.py <scratch-rev> --repo <scratch-clone>` → `C1S=met`).

Residual, observed and still open: no committed artifact performs the proposed
daily sweep. The proposal's own diagnosis is still reproducible — at HEAD these
committed instruments hardcode `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`:

```
.ufo/waves/round-40/conform.py            .ufo/waves/round-42/count-c1.py
.ufo/waves/round-41/conform.py            .ufo/waves/round-42/count-c2.py
.ufo/waves/round-42/conform.py            .ufo/waves/round-42/count-c3.py
.ufo/waves/round-40/count-c8.py           .ufo/waves/round-43/count-c1s.py
.ufo/waves/round-40/gen-wave-spec.py      .ufo/waves/round-43/count-c2.py
```

The round's own instruments apply the practice: `.ufo/waves/round-44/count-c1.py:36-50`
resolves its repo by walking up to the nearest `.git` / `tools/mori-gate-registry.py`
(`repo_default()`), and `grep -n "LANE\|home/vgpnk" .ufo/waves/round-44/count-c*.py`
returns nothing. `tools/` contains three files that *mention* the home path
(`mori-misroot-sweep.py`, `mori-round17-context-check.py`, `mori-blind-check.sh`)
but none is a host-path scanner. Inference (labelled): the criterion is
discharged per-round by the round that mints the instrument, not by a cumulative
sweep; the r40 `conform.py` pointer in QUALITY 115 still fails off-host at HEAD.

### P2 — "Keep a cumulative survivor ledger"

Observed implementation of the criterion: QUALITY 114 (`corpus/QUALITY.md:927-936`)
requires that "every named checker-selftest survivor … enters a committed fixture
under the round's wave tree, and the next checker version's selftest must kill it
via an arm named for the survivor class; a cumulative ledger re-runs every
committed survivor fixture against the newest conformance checker and reports any
that still pass." Added by `34b92673` (r42). Its Check cell is
`python3 .ufo/waves/round-42/conform.py … --counter .ufo/waves/round-41/fixtures/c1/count-c8.py --selftest`
→ `CONFORM_SELFTEST pass=17 fail=0`, with the three r41 survivor arms
(walrus-positive, tupleunpack-positive, source-order).

Residual, observed: the cumulative ledger itself has no committed artifact.
`git ls-files | grep -i survivor` shows the fixtures scattered across rounds —
`.ufo/waves/round-40/fixtures/generated/survivor-*.py` (10),
`.ufo/waves/round-41/fixtures/c1/survivor-{walrus,tupleunpack,deadloop}*.py` (3),
plus `.ufo/waves/round-42/fixtures/counter-*.py` (3) and `fixtures/mutants/` (6) —
and `grep -rln survivor tools/*.py` matches only `tools/mori-round17-context-check.py`
(a different, round-17 survivor). No tool enumerates and re-runs the set. The only
"ledger" name in the tree is `tools/mori-dispatch-ledger.py`, unrelated. The
round-40 survivor copies under `.scratch/CritFreezeTiming/survivors/` and
`.scratch/CritNewSurvivor/` are tracked scratch duplicates, not a ledger.

### P3 — "Watch repository growth from scratch output"

Unimplemented, observed. `grep -n "growth" corpus/QUALITY.md` → no hit;
`grep -rn "repository growth|tracked scratch|scratch output|growth" corpus/lessons/*.md`
→ only unrelated prose in `round-19.md:17` and `round-23-verifier-spotcheck.md:52`;
no tool under `tools/` computes file or line growth (`mori-disk-rate.py` samples
`/proc/diskstats`, a different quantity). The proposal is cited by no criterion,
lesson or SOURCES row.

The premise is still measurable, and the number has moved since the reflection:

```
$ for rev in d72ac16 1429c791 HEAD; do
    git ls-tree -r --name-only $rev -- .scratch | sort -u > /tmp/t.txt
    git grep -ohE '\.scratch/[A-Za-z0-9_./-]+' $rev -- '*.md' '*.py' '*.sh' '*.json' '*.txt' \
      | sed 's/[.,)]*$//' | sort -u > /tmp/m.txt
    echo "$rev tracked_scratch=$(wc -l < /tmp/t.txt) uncited=$(comm -23 /tmp/t.txt /tmp/m.txt | wc -l)"
  done
d72ac16   tracked_scratch=71  uncited=40
1429c791  tracked_scratch=225 uncited=3
HEAD      tracked_scratch=225 uncited=3

$ for rev in d72ac16 1429c791 HEAD; do echo "$rev $(git ls-tree -r --name-only $rev | wc -l)"; done
d72ac16   10893
1429c791  11762
HEAD      11777
```

So the reflection's "71 files under `.scratch/` are now tracked" is exactly the
`d72ac16` count; the tree now tracks 225, and all +154 arrived in one commit:

```
$ git log --oneline d72ac16..HEAD -- .scratch
aa161e99 round-41: C3 correction records (35/17), r41 lesson, S230/S231 source copies, freeze verify + attempt-1 receipt, round22 strays
```

`git show --stat aa161e99 -- .scratch` shows `.scratch/round22/measure1/…` and
siblings; `git ls-files .scratch | grep -c scratch/round22` → 154. The uncited
set shrank 40 → 3 because the same round's receipts cite the strays by path; the
three that no tracked text names are, observed:

```
.scratch/round22/trial1.json
.scratch/round22/trial2.json
.scratch/round22/trial3.json
```

`.gitignore` exists (62 bytes) and lists only `.ufo/interactive-sessions/`,
`.ufo/worktrees/`, `__pycache__/`, `*.pyc` — no `scratch` entry
(`grep -n scratch .gitignore` → no output), so the tracked-vs-temp tension the
reflection names is real. Nothing judges whether these files belong — the
reflection explicitly does not.

### P4 — "Reproduce headline numbers mechanically"

Partially implemented, observed. One round-specific instance exists:
`tools/mori-round41-calibration.py`, added at `d72ac16` (r41) — the only
`calibrat*` tool in `tools/`. It is hard-wired to round 40:

```
$ grep -n "round-40\|round-4" tools/mori-round41-calibration.py
2:"""Count round-40 C2 self-assessment mismatches against the frozen r40 gate.
16:RECORD_PATHS = ("SCORECARD.md", "LOG.md", "corpus/lessons/round-40.md")
```

Its CLI is `python3 tools/mori-round41-calibration.py <revision> --repo DIR --reference-rev REV`;
it loads the reference gate byte-for-byte and reads the three recorded files, so
it cannot be pointed at another round's headline counts.

The general form is this round's C1 and is not landed yet:
`ls .ufo/waves/round-44/figures.tsv` → `No such file or directory` at HEAD;
`SCORECARD.md:2410` already declares the C1 row (12-row / 4-class floors,
`git`-pipeline rows naming `@REV@`), and `SKILL.md:183` registers
`r44 figure ledger (C1)`. So P4 is in flight as C1, not implemented at HEAD.

## 3. Recommendation — exactly one

**P3, "Watch repository growth from scratch output"**, is the only proposal in
`considerthese/2026-10-24.md` with no landing anywhere: P1 is QUALITY 115, P2 is
QUALITY 114, P4 is (a) the r41 calibration instance and (b) this round's C1.
Grounding P3 therefore adds coverage instead of duplicating a criterion.

**Concrete artifact: a new QUALITY criterion 117 in `corpus/QUALITY.md`**, appended
after 116 (117 and 118 are unused; 119 is already reserved by the round-44
declaration at `SCORECARD.md:2405` for the routed revision mismatch, so 117 is the
first free number). Follow the 114/115 house shape — statement, `Rationale:`
citing the operator reflection by title (never editing it), `Check:`, `Shown able
to fail:`, `Not covered:`.

Proposed criterion text (append-only, no existing row rewritten):

> 117. A round's report carries a committed-artifact growth census: the tracked
> file count, the tracked `.scratch/` count, and the set of tracked `.scratch/`
> paths that no committed receipt names — growth is reported, never judged.
> Rationale: `considerthese/2026-10-24.md`, "Watch repository growth from scratch
> output" (operator-authored reflection, mined round 44; not edited). Check:
> `git ls-tree -r --name-only <rev> | wc -l` → `11777`; `git ls-files .scratch | wc -l`
> → `225`; the uncited set is `comm -23 <(git ls-files .scratch | sort) <(git grep -ohE
> '\.scratch/[A-Za-z0-9_./-]+' -- '*.md' '*.py' '*.sh' '*.json' '*.txt' | sed 's/[.,)]*$//' | sort -u)`
> → the three `.scratch/round22/trial{1,2,3}.json` paths. Shown able to fail: the
> same census at `d72ac16` prints `10893` / `71` / `40` uncited, so a report that
> claims "no growth" or "no uncited scratch" is falsified by the entering-tip and
> `d72ac16` numbers, and the `aa161e99` commit adds 154 tracked `.scratch/` files
> in one step. Not covered: whether any tracked scratch file belongs; line-count
> growth (the reflection's "about 40k lines") is not measured by this check.

Why not the others: P1 and P2 would restate QUALITY 115/114 (duplicate criteria,
and both have a Check cell that runs), and P4's general artifact is already this
round's frozen C1 — adding a QUALITY row for it would claim as landed a ledger
that `ls` shows absent.

## 4. Commands run (verbatim, all read-only)

```
ls -la considerthese/                                  # newest = 2026-10-24.md, no 10-25
grep -rn "not implemented\|proposals only\|unimplemented" considerthese/
grep -n "considerthese" corpus/SOURCES.md              # no SOURCES row cites it
grep -rn "considerthese" corpus/lessons/               # r42:73, r43:107
git log --oneline --all --grep considerthese
git log --oneline -S "114. Every named checker-selftest survivor" -- corpus/QUALITY.md
git log --oneline -S "115. A frozen instrument's green control" -- corpus/QUALITY.md
grep -n "growth\|considerthese\|figure ledger\|figures.tsv" corpus/QUALITY.md
grep -rn "repository growth\|tracked scratch\|scratch output\|growth" corpus/lessons/*.md
grep -n "home/vgpnk" .ufo/waves/round-4*/conform.py .ufo/waves/round-4*/count-c*.py .ufo/waves/round-4*/gen-wave-spec.py
grep -n "LANE\|home/vgpnk" .ufo/waves/round-44/count-c*.py     # no output
git ls-files | grep -i survivor ; grep -rln survivor tools/*.py
git log --oneline --follow -- tools/mori-round41-calibration.py
sed -n '1,60p' tools/mori-round41-calibration.py ; grep -n "round-4" tools/mori-round41-calibration.py
ls -la .ufo/waves/round-44/figures.tsv                 # No such file or directory
git log --oneline d72ac16..HEAD -- .scratch            # aa161e99
git show --stat aa161e99 -- .scratch ; git ls-files .scratch | grep -c scratch/round22   # 154
# growth census at d72ac16 / 1429c791 / HEAD (71/40, 225/3, 225/3) and tracked totals (10893/11762/11777)
```

No tool was installed or upgraded this pass.

## 5. Remaining unknowns

- Whether the round's own after-report will count as a "committed receipt" for the
  P3 criterion's uncited set: the check above counts only tracked `.md/.py/.sh/.json/.txt`
  mentions, so a scratch file cited only from a commit message counts as uncited.
  That boundary must be fixed when the criterion is written (recommended: exact
  path string in a tracked text file, as measured here).
- The reflection's "about 40k lines" for the r41 freeze was not re-derived (a
  line-count census was out of scope for this question); only file counts were
  measured.
- Whether QUALITY 118 is spoken for elsewhere: no `QUALITY 11[78]` reference exists
  in `SCORECARD.md`, `LOG.md`, `SKILL.md` or `corpus/QUALITY.md` at HEAD (inference:
  free, but the r44 declaration may reserve it later).
