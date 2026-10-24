author: hyaku closure (non-author integrator, @m_opus)

# mori round 35 — verifier spot-check (non-author closure)

Lane-round mori 35, attempt 1 (L1 `MoriR35`). Base `dd76eb79ef4f6d39c9c26647a56d3fb607308f8f`, landed tip
`42a8ae651a006443ab17e2690279e28623af8d39`, fleet report `.ufo/reports/round-35/mori.md` (`2e28f80b`). Closure run
2026-10-23, finished after 09:49:53Z (`date -u`), by the hyaku closure session (dispatched by the hyaku orchestrator, not by the lane). Four
read-only closure seats were used: MoriR35Conform, MoriR35C1Calib, MoriR35Repairs and MoriR35NoHarm. All four returned;
no seat died. No counter, gate or lane tool was executed (`count-c1.py`, `check-sources-appendonly.py` and the census
self-test were read, not run; the census `validate` mode the closure prompt names was run).

Driver digest (copied from `.ufo/watchdog.log`):
```
2026-10-23T05:24:38-03:00 launch mori round=35 pgid=1214789 driver=hyaku-inline attempt=1
2026-10-23T06:36:50-03:00 complete mori round=35; hyaku-inline attempt=1
```

## 1. Step-1 conformance — conformant

- Report author: `git log --format='%an %H' -- .ufo/reports/round-35/mori.md` →
  `mori-shokunin 2e28f80b0db89608265a8fe76569aed5e19e2ddd` (one commit, lane identity). Report commit time 06:36:30-03:00
  is after the lane tip's 06:35:55-03:00.
- Cited lane hashes `f2d28711 913df22e 721040a9 cedb0ec4 6d3d94b3 42a8ae65 dd76eb79 d677cf3`: each resolves and
  `git merge-base --is-ancestor <h> master` holds. `37b51a24` and `2e28f80b` are fleet-repo objects and resolve there.
- `jj-lane.sh state` → `branch=master local=42a8ae65… remote=42a8ae65… ahead=0 behind=0 head=detached tracked=0
  untracked=1`. `git status --porcelain` → `?? .scratch/` only; its entries are dated 2026-10-21 (before this round's
  launch), so it is not round-35 work. `git status --porcelain --untracked-files=no` is empty.
- `SHONEN` heading: four lines, one per box of the lane `SHONEN.md` (4 boxes, all `[~]`).
- Prompt `.ufo/prompts/mori-round-35.md` (fleet `91896e0`, committed 05:23:56-03:00, before the launch line): carries the
  canonical `templates/round-prompt.md` round-level items and the five child-lane items, plus hyaku addendum §6. No L2
  route map is quoted (MoriR35Conform).
- Evidence timestamps: every timestamp in `.ufo/waves/round-35/evidence/*` and `dispatch-log.txt` is at or before the
  commit that ships it (latest: dispatch-log 09:35Z ≤ `42a8ae65` 09:35:55Z). None is future-dated.
- **M4 (`git add -N .`), confirmed contained.** `git diff-tree -r --name-status <c>^ <c>` over the six round commits:
  every path is under `.ufo/waves/round-35/`, `corpus/`, `SKILL.md`, `SCORECARD.md` or `LOG.md`; no `.scratch/` path,
  no added empty blob (`e69de29…`). `git ls-files --stage | grep -c e69de29` is 2267 at both `dd76eb79` and the tip, so
  no intent-to-add entry entered any commit. The index equals HEAD.
- Seat accounting: c0 11 reports (12 − CtlParserAttack `cyber_policy` hold), w1 32/32, w2 35 (36 − GateS204, no
  report), residual 3/3. Matches the report's 83 seats.

Conformance defects: none in step 1. The gate-registry defect is in §6 item 3.

## 2. Claims

### C1 — calibration: capabilities register vs MANIFEST@`37b51a24` — **not verified (honest stop confirmed)**

Re-measured (independent oracle, not the lane counter):
- `git show 37b51a24:MANIFEST.json | jq '[.rounds[] | select(.lane=="mori" and .admitted==true)]'` → 13 admitted mori
  closures (lane rounds 12, 14, 15, 16, 18, 19, 21, 22, 24, 25, 26, 28, 31; round 21 adds 0) carrying 18
  `capabilities_added` entries.
- The last `## Capabilities` section of `git show 42a8ae65:SCORECARD.md` holds 18 rows keyed `rounds[313]…[0]` through
  `rounds[495]…[1]`. The key and round match the jq enumeration 18/18, with no extra row. Every evidence path resolves in
  `git ls-tree 42a8ae65` (MoriR35C1Calib). At `dd76eb79` the field reads `— none yet —` and the only rows are 5 older
  per-round demo rows: matched 0, missing 18, extra 5. This agrees with `evidence/c1-before.txt` (`mismatches=23
  C1=unmet`, exit 1) and `c1-after.txt` (`mismatches=0 C1=met`, exit 0).
- Freeze integrity: sha256 of `count-c1.py` is `27b82d71f2f5…ee18167` and of `contract.md` is `94b7f90a…65ba40`; both are
  byte-identical at `f2d28711` and `42a8ae65`. The freeze (`f2d28711`, 05:34:43) precedes C0 (`913df22e`, 05:47:18) and
  the register (`721040a9`, 05:59:09).

Evidence-verified (committed bytes), deciding the honest stop:
- `evidence/c1-controls.txt:36`: `10c empty capability/what cells CtlSkipDesign B … matched=18 C1=met exit 0` (and 9d
  met, `:38`). The ruling at `:40-44` (before data) records both as residuals.
- QUALITY 98 at `dd76eb79` (`corpus/QUALITY.md:715-725`) was in force at the freeze: "A control the counter scores as met
  means the counter or the target is wrong: re-design before data, or declare the claim exploratory." The L1 did
  neither. The lesson owns this as M1.
- After data, `w2/CtlDenial.md:7`, `w2/CtlWordBag.md:74-80` and `w2/CtlOffTopic.md:6` each score `C1=met`. The counter
  checks only the key/round binding and never reads the capability or what cells. `w2/CritC1Verdict.md:7` →
  `fails — C1 verifies`.

Ruling: the binding the register asserts is correct (18/18, re-derived here). But the frozen P-C1 cannot tell a true
register from an empty, denial or off-topic one, so `C1=met` is not a measurement of calibration. Not verified; the
lane's own honest stop stands. The row-by-row judges (`w2/JudgeRows*.md`, 18/18 `supported`; `w2/JudgeCanary.md`, 5/5
altered rows flagged) are lane-dispatched seats. They support the register's content but cannot verify the claim
(LEARNING.md: a subagent the lane dispatched is still the lane).

### Round-34 routed repairs (not claims; re-judged from the bytes by MoriR35Repairs)

| routed item (r34 §6) | outcome | check |
|---|---|---|
| 1 counter discrimination | partly answered: QUALITY 100 answers r33 §8 item 1 clause 2; the round's own counter again failed discrimination (M1) | `corpus/QUALITY.md:766-818` |
| 2 SOURCES append-only | landed: S201 `supersedes S182 —`, S202 `supersedes S193 —` (`SOURCES.md:207-208`, 13-column census clean); `round-34.md:46` corrected in `round-35.md` §Corrections; `round-34.md` unchanged | `git diff dd76eb79 42a8ae65 -- corpus/SOURCES.md` → +6 −0 |
| 3 dangling `w1/` pointer | landed: append-only correction `disk-write-rate-r33.md:99-108`; all 9 named paths exist at the tip (`git cat-file -e`) | diff +10 −0 |
| 4 `SKILL.md:834` | landed: marked observed on this host, not sourced (`SKILL.md:843-854`, append-only +12 −0) | diff hunk `@@ -840,3 +840,15 @@` |
| 5 QUALITY 98 (D1, D2, D4) | landed: append-only 98 correction naming exactly D1, D2 and D4 | QUALITY diff +53 −0 |
| Axes `Last change` (found this round) | landed: operability and depth cells now say round 31, each naming its old value (28, 12); jq over MANIFEST shows the last admitted mori round grading each improved is 31 (`rounds[495]`) | `SCORECARD.md:11-12` |

QUALITY 100, 101 and 102 each name their lesson (r33/r34 routed item 1, M1 and M2) and were mutation-tested in wave 2
(`w2/MutQ100.md`, `MutQ101.md`, `MutQ102.md`). Their stated numbers match the lesson: M2's 16 ids before round 34, and 18
listed.

### No-harm, and the final checker fix this closure judged (MoriR35NoHarm, plus this closure's own read)

- The fix `6d3d94b3 → 42a8ae65` in `check-sources-appendonly.py` changes one logic line: `rc = [i for i in violations if
  set(changes[i]) & in_round]` → `rc = sorted(i for i in changes if set(changes[i]) & in_round)` (`:121`). This is the
  correction `residual/MoriR35.ResNoHarmFixes.md:77` prescribed. An id changed inside the round and changed back now has
  a recorded commit in `changes[i]` (`:89-90`), so it is caught; the old code missed it because the id was absent from
  the endpoint-filtered `violations`. The range `rev-list base..rev` excludes the base and includes the tip. Exits are
  unchanged: `die()` → 2, otherwise 1 iff `round_changed` is non-empty. Supersession stays metadata (`:116`). Deleted
  rows remain uncovered, and QUALITY 102 discloses this (`QUALITY.md:810`). **Ruling: sound, no new defect.**
- Plain re-derivation, without running the checker: round 35's only SOURCES commit is `cedb0ec4`, +6 −0, rows 198 → 204,
  so no existing row changed. Over `f10a320d..dd76eb79` the compared cells change only for S182 (anchor, `8d56809a`) and
  S193 (anchor and teaches, `406d91a4`); `ff334073` touched allowed columns only. So the new formula still gives
  QUALITY 102's `round_changed=[S182,S193]`, and `[]` for round 35.
- Fixes for CritNoHarm N1–N3 are present at the tip: `SKILL.md:847` uses the device-subject predicate; error exits are
  2; a supersede row no longer discharges a violation. The residual count fixes landed: M2 16 ids; seventeen files
  opened, fourteen named.
- `git diff dd76eb79 42a8ae65 -- PROVINCE.md` is empty. SKILL +12 −0, QUALITY +53 −0, LOG +13 −0, knowledge +10 −0. The
  only replaced lines are SCORECARD's two Axes cells, whose scores are held at 7 and 5. No path was deleted.

## 3. Per-axis verdicts and no-harm

`git diff dd76eb79 42a8ae65 -- SCORECARD.md` → +60 −2. It appends the `## Capabilities` register and the round-35
tables, and rewrites only the two `Last change` cells. Held: coverage 6, operability 7, depth 5, freshness 5,
calibration 5, adjacency 6.

| axis | verdict | basis |
|---|---|---|
| calibration | unprovable | C1 is not verified: the frozen counter credits empty, denial, word-bag and off-topic registers (§2). |
| depth | unchanged | Repairs only (SKILL observed-not-sourced mark, N1 wording); the score is held. |
| operability | unchanged | The append-only checker is a wave artifact with no registry row (§6 item 3); no score move. |
| freshness | unchanged | S201 and S202 re-fetched sha-identical to S182 and S193. This closure re-fetched S201, S203 and S204 live with sha match (§4). No score move was claimed. |
| coverage | unchanged | The PROVINCE diff is empty; no knowledge entry on new ground. |
| adjacency | unchanged | Every changed path is lane-local. |

No axis is harmed.

## 4. Discernment spot-check (`corpus/lessons/round-35.md` `## Gate`)

Live re-open on 2026-10-23, before 09:49:53Z (`curl -sS <URL> | sha256sum`, reproducible). Each sha256 equals the Gate table:
- genhd.c `8c2faa15…d39a5`
- dm.c `b01ff2d6…bab8b02b`
- Disks.html `c84b28a2…7681b8e`
- AXES.md `04ea5c9e…7d993`; `cmp` with the fleet `protocol/AXES.md` is identical.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S201 Linux `block/genhd.c` v7.2 (`__add_disk`, `device_add_disk`) | admit, A, mined, `supersedes S182 —` | https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c, lines 483-487, 510-519, 618-624 | agree | :485 `ddev->parent = parent;` (3 words), :518 `disk->slave_dir = kobject_create_and_add(` (3), :623 `return add_disk_fwnode(parent, disk, groups, NULL);` (5). Each quote is contiguous at its locator and matches the revised word count. :512-513 creates `holders` for part0, as the teaches cell says. The supersede form follows CORPUS rule 2, and S182's row is untouched. |
| S204 Linux `drivers/md/dm.c` v7.2 (`dm_submit_bio_remap`) | reject (scope) | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/md/dm.c, lines 505-518, 1375-1390 | agree | The quote at :1379-1380 is exact (16 words). The file accounts the original bio to the dm device (`dm_io_acct` → `bdev_start_io_acct(bio->bi_bdev…)`, :505-517) and resubmits the clone with `submit_bio_noacct` (:1386). Nothing in dm.c shows the lower device's diskstats line counting the clone, so it does not answer the Gate's question. Rejecting it for that scope is right. GateS204 returned no report, so this closure's agree is the only non-author check on this row. |
| S203 collectl `docs/Disks.html` 4.3.20.3 | reject, C | https://raw.githubusercontent.com/sharkcz/collectl/4.3.20.3/docs/Disks.html, lines 20-30 | agree | :24 "Device mapper disks, while listed in the detail data are" (10 words, contiguous, then `<i>NOT</i> included in the summary data to avoid double counting`). Leaving dm out of a summary *implies* that the I/O shows again on the backing device but never states it, and md is not mentioned. A tool doc is C for a kernel accounting claim. |
| S199 (newly written row, quote check) | admit, A | https://raw.githubusercontent.com/VeigaPunk/kimi-shokunin/b47dfbe2…/skills/shokunin/protocol/AXES.md, lines 15, 62-64 | agree | The 23-word quote at :62-64 ("Rows enter only through … is pre-claiming") and the 9-word quote at :15 are contiguous and ≤25 words, with no `"` or `|`. The row's teaches cell (`SOURCES.md:205`) restates them. |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` →
`mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`, `EXIT=0`. It prints 13 `W04` lines (duplicate URL
across scopes). The only new one is S201, which shares S182's URL by design as its superseder. Row count: `grep -c '^|
S[0-9]'` gives 198 at `dd76eb79` and 204 at `42a8ae65`.

## 5. Trend verdicts

- **expansion: unchanged.**
  - No `knowledge/` entry was added on uncovered ground.
  - The register records capabilities admitted earlier, and since C1 did not verify no capability enters the table.
  - FR6 (stacked-device double count) is still unsourced after 17 files were opened.
- **quality: improved.**
  - The round-34 in-place edits to S182 and S193 are superseded by S201 and S202, which this closure re-opened and found
    supported.
  - The miscited `SKILL.md:834` clause is marked observed, not sourced, and the dangling `w1/` pointer is corrected
    append-only.
  - No admitted entry failed its re-check. The register's 18 bindings are correct.
- **discernment: improved.**
  - The outside spot-check agrees with the gate on one admit (S201) and two rejects (S204, S203), and S199's quotes
    check out.
  - The L1's discernment miss (M1: met control 10c ruled a residual against QUALITY 98) became a lesson with a grounded
    criterion (QUALITY 101, mutation-tested). LEARNING.md counts that as improved, not harmed.
  - QUALITY 102 is grounded in M2, and this closure re-judged its final fix.

## 6. Routed defects (the lane owes these next round)

1. **Calibration counter discrimination, open for the fourth round (r32–r35).** Before any re-claim of C1, freeze a
   counter that fails before data on controls 10c and 9d and on the denial, word-bag and off-topic registers
   (`w2/Ctl*.md`). Apply QUALITY 98 and 101 at the freeze: a met control forces a re-design or an exploratory
   declaration, never a residual ruling.
2. **SOURCES append-only debt.** 15 ids changed in place before round 34, not superseded (`w2/ScoutAppendDebt.md`),
   plus S069. Land a supersede row for each, or a named ruling. QUALITY 102's "Not covered: deleted rows" stays a
   declared gap until the checker also flags a row missing at the tip.
3. **Gate registry.** `.ufo/waves/round-35/check-sources-appendonly.py` returns a 0/1/2 verdict that QUALITY 102 binds,
   but it has no registry row at `SKILL.md` (`git grep check-sources-appendonly 42a8ae65 -- SKILL.md` → none) and no
   self-test (PROTOCOL §Gate standard). Register it as a gate with a fixture self-test, or as a probe. No committed
   receipt shows a run at `42a8ae65` after the final fix. Commit one with the two QUALITY 102 commands.
4. **M4 enforcement.** Nothing shown able to fail prevents `git add` in the lane. A check that `git status --porcelain
   --untracked-files=no` is empty after each helper commit, recorded in the round mechanics, would make it detectable.
5. **Operator items (not lane debt), carried from round 34.**
   - `LOG.md:1801` holds an OMP setting value.
   - `refs/jj/keep/…` retains `3b19cac`.
   - The untracked `.scratch/` (2026-10-21) sits in the lane worktree.
   - All four SHONEN `[~]` boxes look checkable by a non-author from their pointers. Promotion is operator-owned.

## 7. Ruling

`status=ok`, `admitted=false`, verdict `rejected-honest-stop`.
- C1 does not verify: before data, its frozen counter credited an empty-prose control that QUALITY 98 says forces a
  re-design, and after data it credited denial, word-bag and off-topic registers. The lane said so itself and did not
  amend the counter, rule or target.
- The register's 18 bindings are correct, re-derived here independently.
- Every round-34 routed repair landed. The final append-only-checker fix is sound. No axis is harmed.
- This is mori's fourth straight non-admitted round (r32–r35).
