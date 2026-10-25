author: hyaku closure (non-author integrator, @m_opus)

# mori round 30 — verifier spot-check (non-author closure)

Lane-round mori 30 (L1 `MoriR30`). Base `58b61681a0e3f3b821a17d38a4e713ccd9921615`, landed tip
`5c99f2d4213b41966d670d10006a2ff5135273e4`, fleet report `.ufo/reports/round-30/mori.md` (`02419cfb`). Closure run
2026-10-22 by a fresh hyaku closure session that did not author the round. Seven read-only seats re-checked parts of
the round (C1OriginalRule, C2Evidence, SpotAdmits, SpotRejects, NoHarmAxes, PromptConformance, CriticVerdict). No
lane gate, counter or self-test was executed. The lane's domain tool `tools/mori-oom-killers.py` was run only from a
`/tmp` copy, on the 13 C1 case inputs. No tool was installed.

Driver digest (copied from `.ufo/watchdog.log`):
`2026-10-22T18:01:21-03:00 launch mori round=30 pgid=45266 driver=hyaku-inline attempt=1`;
`2026-10-22T19:45:25-03:00 complete mori round=30; hyaku-inline attempt=1`.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by the lane identity | `git log --format='%an %ae %H %ad' -- .ufo/reports/round-30/mori.md` | `mori-shokunin mori@shokunin.local 02419cfb… 19:45:07 -0300`, one commit; the lane tip was committed at 19:44:17, before the report | pass |
| `SHONEN` heading | read the report `:107-114` | 4 lines, one per box, all `[~]`; lane `SHONEN.md` at the tip has 4 boxes | pass |
| Cited hashes exist and are ancestors of `master` | `git merge-base --is-ancestor <h> refs/heads/master` for 23 hashes (58b61681, 5c99f2d4, a66751b1, 05db57ed, 3767108e, 55f9a694, 95cd794e, d03203c5, 926ac146, af42101d, 6c47dd03, ee61010d, b039dd4f, 32e287ff, 8ac9535e, db1ec469, 7aa77484, 2ec25cc1, 0b828c27, ad0f0474, 713be294, e936482a, d6d5cb0a) | 23/23 `ok` | pass |
| Pushed, nothing ahead | `scripts/hyaku/jj-lane.sh state <lane>` | `local=remote=5c99f2d4… ahead=0 behind=0 head=detached tracked=0 untracked=1` | pass |
| Uncommitted round work | `git status --porcelain`; `find .scratch -newermt '2026-10-22 18:00'` | only `?? .scratch/`, not gitignored. It holds 151 344 files (`SrcGitCommit-git-rev-parse.html` and `round22/`). The newest mtime is 2026-10-21 and none is newer than the round-30 launch, so this is pre-round round-22 scratch, not round work | pass (named) |
| Prompt carries the template contract | seat PromptConformance: placeholder-substituted diff of `.ufo/prompts/mori-round-30.md` against `kimi-shokunin/templates/round-prompt.md` | 2 hunks, both intended placeholder fills (`<mori-repo>`, `{{AXES}}`); hyaku addendum §6 present; round-level and five child-lane embed items present; no L2 route map quoted | pass |
| Report minimum content | PROTOCOL `:150-175` | all present except one: the landed change `713be294` (wave-2 spec/run/dispatch) has LOG entry `—` and no round-30 LOG entry names it | defect D7 (status-neutral) |

The report records real, checkable work. It is not a marker, so the status is `ok`.

## 2. Claims

### C1 — depth: invocation-scope decision table — **verified (re-measured under the pre-data rule)**

The orchestrator's instruction and the disclosure in A1 bind here. A1 (`05db57ed`) rewrote condition 3a. It moved
tool provenance to the entering-tip blob, added an `expect.exit` comparison, and allowed a case id to appear in more
than one eligible file when the copies are identical. That last change relaxed the original "exactly one", while the A1
preamble said nothing was narrowed. C1 is therefore judged only on the original contract
`git show a66751b1:.ufo/waves/round-30/contract.md:23-54`, conditions 1–5, using my own checker and not the lane
counter.

- **Condition 3, my re-measure.** Python over committed bytes:
  - The three eligible fixture blobs at the tip equal their `58b61681` blobs: `cases.json True`,
    `cases-supplementary.json True`, `cases-a2.json True`.
  - All 13 table rows were checked. Each case id occurs in exactly one eligible file: 12 in `cases-a2.json` and
    `c34-escalation-only-incomplete-scope` in `cases-supplementary.json`. No id occurs in two files.
  - `expect.verdict` equals the row verdict, and every `fields` item equals the case's `expect.fields` value, for 13/13
    rows.
  - The tip tool `5c99f2d4:tools/mori-oom-killers.py`, copied to `/tmp` and run as `python3 -I -B <tool> --inputs
    <case inputs>`, prints the row's verdict and field values for 13/13 rows, with exit codes 1/0/1/2/0/0/1/1/0/1/1/2/2.
    The base tool gives the same result, 13/13.
- **Conditions 1, 2, 4 and 5.** Seat C1OriginalRule, using an independent checker, found all four met:
  - the trio lines are present;
  - there is one table with the five header cells and 13 data rows;
  - the rows cite 4 distinct ids at or above S156 (S156–S159), and 12 rows cite them;
  - each of those ids has a Gate `admit` line with a 64-hex sha256, an excerpt whose header sha256 and URL match, and
    every quote verbatim inside its labelled excerpt lines;
  - `SKILL.md` has 4 table rows containing `Round30` and the entry path.

  My own spot-check agrees: each of S156–S160 has exactly one SOURCES row, exactly one Gate `admit` line and one
  excerpt file, and `grep -c` finds 5 SKILL lines that carry both `Round30` and the entry path.
- **The three re-pointed rows.** They were re-pointed in `95cd794e` (`c03`, `c02`, `c04` → `a2-03-…`, `a2-01-…`,
  `c34-…`), and that re-pointing is what makes the original exactly-one rule hold. The rows were moved during the
  round, before the tip. They are measured against the pre-data rule, not a rule changed after the data. The tip meets
  the original condition 3 without relying on A1.
- **Lane evidence.** `evidence/tip-c1.txt`, measured at `926ac146`: `rows=13 rows_ok=13 new_ids=4 new_id_rows=12
  excerpts_ok=4/4 skill_rows=4`, `C1=met`, exit 0. It matches my result.

Before → after: entry absent, `C1=unmet` (`evidence/c1-before.txt`, exit 1) → met. **depth: improved.** The score
stays at 5 under the contract's score policy and the round-27 precedent.

### C2 — operability: residual, blind disputed-shape pins, gate fix — **miss (evidence-verified; agrees with the report)**

- **Counter output.** `git show 5c99f2d4:.ufo/waves/round-30/evidence/tip-c2.txt`, measured at `926ac146` with counter
  blob `f4f86b0d`, the same blob at `8ac9535e`, `db1ec469` and `2ec25cc1`, prints:
  - `r29 PASS 24/24`, older `PASS 32/32 / 32/32 / 30/30`, `differential=94/94 changed=2 disallowed=0 acted_lost=0`;
  - `gate_selftest=PASS`, `gate_mutants=4/4`, `scanned=4`;
  - `blind_violations=1`, `C2=unmet`, exit 1.
- **The blindness hit, re-read by me.** `5c99f2d4:.ufo/waves/round-30/w1/CaseR30a.md:105` is the brief's closing
  sentence, "The scratch JSON passed python3 json.load; I opened no lane tool source…". It sits after the `## Files
  opened` list and the gate parses it as a files-opened entry. Condition 4 requires `blind_violations=0` at the freeze,
  so it is unmet.
- **The A3 change.** A3 (`55f9a694`) widened the allowlist after the A2 gate output had been seen. It is moot for the
  verdict: the A2 gate flags 4 hits (`evidence/gate-a2-prefreeze.txt`) and the A3 gate flags 1.
- **The judge ruling, re-read by me.** `w2/ReviewR30Cases.md:3,57` rules `unclear text` on the `verdict`/`exit` pins of
  all 8 frozen cases. The original contract (`a66751b1:99-100`) says "Any `case error` or `unclear text` is a C2 miss".
  That is a second, independent ground for the miss.
- **Integrity checks, by seat C2Evidence:**
  - The freeze file `cases-a2-r30.json` has blob `a05863cc` at both `db1ec469` and the tip.
  - The older fixtures are blob-identical between base and tip, and `cases-a2-r29.json` equals its freeze blob at
    `d6d5cb0a`.
  - Commit order is gate `32e287f` → A3 `55f9a69` → counter `8ac9535` → freeze `db1ec46`.
  - The tool diff is limited to the Judge11–13 fix (42 lines), and the differential receipt shows `acted_lost=0`.

Before → after: `C2=unmet`, residual `FAIL 21/24` → `C2=unmet`, residual `PASS 24/24`. A declared claim was not met.
It was reported as a miss and not withdrawn. **operability: unchanged** (round-29 precedent). Not harmed: no older
verdict was lost, and no older fixture changed.

Re-measured by me: C1 condition 3 in full, C1 conditions 4–5 in part, and the C2 blind hit and judge ruling from
committed text. Evidence-verified, without executing any gate: the C2 counter, gate self-test, mutants, differential
and retention receipts.

## 3. Per-axis verdicts and no-harm

| Axis | Verdict | Evidence |
|---|---|---|
| depth | improved | C1 re-measured under the original rule (above) |
| operability | unchanged | C2 miss; the residual fix holds older verdicts (`acted_lost=0`, old fixtures blob-identical) |
| coverage | unchanged | SOURCES `+7/-0` (S156–S160 only); census at start and end shows ten pre-existing W04 and `mori ok` |
| freshness | unchanged | `LOG.md +38/-0`; no re-verification claim was made |
| calibration | unchanged | SCORECARD diff (below) holds every score; outcome rows match the observed C1 met / C2 miss |
| adjacency | unchanged | PROVINCE R7 substitutions checked against real targets (seat NoHarmAxes); no sibling surface newly claimed |

- `git diff 58b61681 5c99f2d4 -- SCORECARD.md` is `+25/-0`: the declaration and measured-outcome blocks are appended,
  and the "Held" line is unchanged (depth 5, freshness 5, coverage 6, operability 7, adjacency 6, calibration 5).
- `git diff --diff-filter=D --name-only 58b61681 5c99f2d4` is empty. The 28 removed lines are all in-place
  substitutions in PROVINCE (13), SKILL (1, the `:661` citation) and the tool (14).
- Retention metric: 4 at the tip (`evidence/tip-retention.txt`, at `926ac146`) against base 4 (`w1/RetentionBase.md`).
- No axis is harmed.

## 4. Discernment spot-check (`corpus/lessons/round-30.md` `## Gate`)

Each source was re-fetched with `curl` and its sha256 compared with the Gate cell.

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S158 `journald-manager.c` (re-opened by me) | admit | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c | agree | sha256 `428dc830…a2` matches; `:1291-1294` holds the `rl > 1` guard and `LOG_MESSAGE("Suppressed %i messages from %s", rl - 1, c->unit)` verbatim; the quote is 16 words (≤25); the `SOURCES.md` S158 row anchor `:1290-1296` at v262 grounds `teaches` |
| S157 `unit.c` | admit | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c | agree | sha256 `47e98d39…b7` matches; `:2773-2776` is the active-enter assignment on entry and the active-exit stamp on leaving, verbatim; quotes are 7 and 8 words; the excerpt header matches; `used-by` paths exist |
| S158 candidate `man/journald.conf.xml` | reject (does not carry the fact) | https://raw.githubusercontent.com/systemd/systemd/v262/man/journald.conf.xml | agree | sha256 matches; `grep -ci suppress` → 0, while `ratelimit` → 7: the page documents the limit but not the notice |
| S157 candidate `src/core/service.c` | reject (does not carry the fact) | https://raw.githubusercontent.com/systemd/systemd/v262/src/core/service.c | agree | sha256 matches; `:1731` is the quoted `unit_notify` call; `grep -c 'u->active_enter_timestamp ='` → 0 (the assignment is in `unit.c`) |
| S160 candidate `src/shared/journal-util.c` | reject (does not carry the fact) | https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/journal-util.c | agree | sha256 matches; `add_matches_for_unit_full` occurs 0 times; the builder is at `logs-show.c:1729`, already under S123 |
| S159 candidate `earlyoom.service.in` v1.9.0 | reject (duplicate URL) | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service.in | agree | sha256 matches; 1 340 B, `:17 Restart=always`; the exact URL is already S120 (`corpus/SOURCES.md:126`) |

SOURCES row check: I read the `5c99f2d4:corpus/SOURCES.md` S158 row in full (kind `code`, tier A, revision-pinned
anchor, `mined`). Its ≤25-word Gate quote reproduces from the re-fetched bytes. Seat SpotAdmits did the same for S157.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
→ ten W04 (S035, S037, S073–S076, S147–S150, all pre-existing duplicate-URL warnings), `mori ok`, exit 0. None
names S156–S160.

The spot-check agrees on 2/2 admits and 4/4 rejects.

## 5. Trend verdicts

- **expansion: unprovable-but-better.**
  - Gains: 5 new tier-A `code` rows, all `mined` and re-fetched byte-identical. There is also one new knowledge entry,
    citing S156–S159, on which earlyoom invocation a send line belongs to. The round-26 and round-27 entries leave that
    question open.
  - Why not `improved`: LEARNING's `improved` requires each new entry to cite its coverage-map row. `corpus/README.md`
    is unchanged in the round (`git diff --stat` is empty) and has no row for
    `knowledge/earlyoom-invocation-scope-r30.md`. Its ground sits under FR10, which is already mapped.
  - Not harmed: no entry fails the bar it was admitted under (C1 re-measured).
- **quality: unprovable-but-better.**
  - Gains: the round-29 residual tool errors are fixed (`FAIL 21/24` → `PASS 24/24`, `acted_lost=0`), the R7 stale
    PROVINCE statements are corrected, and the R2/R3 corrections are appended.
  - Why not `improved`: the new entry `:53` still says the reader "reports its version". Wave-2 ReviewEntryProse found
    this holds only for a version line at or after the retained stamp (lesson `:231-232`, carried, not corrected in
    the entry). QUALITY 93 cannot fail on its stated property (lesson `:215`). QUALITY 92 is unmet at the tip (lesson
    `:228`). So "no admitted entry failing its re-check" is not shown cleanly.
  - Not `harmed`: each item is marked in the lesson and carried to round 31.
- **discernment: improved.**
  - The outside spot-check agrees with the gate on admits and rejects (§4).
  - The process breaches are real, and they are routed as defects. A1 loosened 3a without saying so, and A3 changed
    the gate after its output was seen. They were caught by wave 2 and disclosed in the contract. Neither changed an
    outcome, because C1 holds under the original rule and C2 fails under both gate versions.
  - LEARNING's harm conditions (a spot-check disagreement left unlearned, or a criterion with no lesson behind it) do
    not apply.

## 6. Ruling

Status `ok`; **not admitted**. Verdict `rejected-honest-stop`: C1 verifies, C2 is a declared, honestly reported miss,
and no axis is harmed. AXES.md admits a round only if every claim verifies. The SHONEN boxes are all `[~]` with no
non-author promotion verdict, so they are not fully checkable by a non-author and are not promotion-ready.

## 7. Routed defects (the lane owes these next round)

- **D1** — The blindness gate parser reads past the `Files opened` list (`CaseR30a.md:105`). It reports only the first
  forbidden hit per file. Its self-test locks in a known false positive (`CaseA210c.md|writer-missing-files-opened-list`).
  Fix the parser and report every hit (lesson M6).
- **D2** — A1 relaxed condition 3a ("exactly one" became duplicates allowed) while its preamble said nothing was
  narrowed. No lesson `## Mistakes` row records this. Add one, citing QUALITY 25. A3 was an after-data change whose
  first disclosure was incomplete; it must not be used as a precedent.
- **D3** — QUALITY 93 cannot fail on its stated property. Supersede it with a new row that names it (LEARNING: criteria
  are superseded by new rows, never rewritten). QUALITY 92 is unmet at the tip (`limit_stated=no`).
- **D4** — Correct the entry `corpus/knowledge/earlyoom-invocation-scope-r30.md:53` "reports its version" (ReviewEntryProse
  LOW-2) at every mention, per the lane's QUALITY 77 (a contradicted line left standing is a defect). Also handle the
  S159/S120 `Restart=always` overlap.
- **D5** — Add the coverage-map row for `knowledge/earlyoom-invocation-scope-r30.md` in `corpus/README.md`.
- **D6** — Pin the dry-run flips from w2/CriticHarmAxes (X1, X2: `KILLERS_QUIET` at base → `KILLER_ACTED` at tip;
  unreachable from stock earlyoom 1.9.0) as cases. Name them in the carry list.
- **D7** — The report's landed change `713be294` (wave-2 dispatch) has no LOG entry. Append one.
- **D8** — Append a SCORECARD correction. The round-30 outcome row cites `count-c1.sh ee61010d` (`new_ids=5 …
  excerpts_ok=5/5`), but the tip measures `new_ids=4 new_id_rows=12 excerpts_ok=4/4` after the S160 citations were
  removed. Also, contract C2 condition 4's parenthetical "reports 0 on the round-29 writer wave" is stale against A2's
  expected set of 9.
- **D9** — Note only: the two redacted policy tokens remain in pushed history at `d03203c5`, and the unredacted
  original lives on `/fast/scratch`, which is not durable. These are policy pattern names, not secrets.
