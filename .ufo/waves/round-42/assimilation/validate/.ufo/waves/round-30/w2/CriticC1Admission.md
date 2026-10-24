Verdict: defect found — the C1 counter prints `C1=met` with every shape cell, every source cell and the whole Facts section replaced by non-content (F1); entry §3 and SKILL.md:754 misdescribe the round-30 tool on a stopped unit (F3). Every table row still agrees with the tip tool on its cited fields (F4).

# CriticC1Admission — round 30, wave 2 (falsify C1 admission)

Seat: MoriR30.CriticC1Admission. Lane tip measured: `ad0f04745ced2194e58c22a0d6b38131bee3e230`.
Scratch: `/fast/scratch/hyaku/mori-r30-w2/CriticC1Admission/` (tool copies, case copies, re-fetched sources, sandbox clone).
Tool installs: none. No installed `godspeed` skill under `~/.omp` or the fleet tree. A later full-disk search found
copies only in another lane's scratch (`/fast/scratch/hyaku/kake-r33/w1/*/marketplace/plugins/myagents/skills/godspeed/`);
its `directive.md` (name the axes, iterate cheap in parallel, keep moves that improve an axis and harm none) matches the
method used here. Its delegation-prefix rule does not apply: this seat dispatches no subagents.
`/home/vgpnk/.omp/agent/RULES.md` read (14 lines, tooling directive only).

## Baseline (re-derived, not trusted from receipts)

- Counter blob unchanged since its commit: `git rev-parse 6c47dd0:.ufo/waves/round-30/count-c1.sh ad0f0474:…` →
  both `325168f62c68…`. `git merge-base --is-ancestor 6c47dd0 ee61010` → true; ee61010 is the commit that adds the entry
  and `corpus/evidence/sources-r30/`.
- `bash <(git show ad0f0474:.ufo/waves/round-30/count-c1.sh) ad0f0474` → `rows=13 rows_ok=13 new_ids=5 new_id_rows=13
  excerpts_ok=5/5 skill_rows=4`, `C1=met`, exit 0. Same output from the 6c47dd0 blob at ee61010, which matches
  `evidence/c1-after.txt`. Between ee61010 and ad0f0474 only `corpus/SOURCES.md` changes (+2 lines).
- Sources re-fetched with curl from the URL in each excerpt header: S156–S160 sha256 all equal the header values, and
  0 of 162 excerpt lines differ from the fetched line with the same number (S156 73, S157 17, S158 6, S159 27,
  S160 39). The contract residual F3 (`contract.md` A1, "re-fetch every S156+ URL") passes. No defect here.

## F1 — high (tradeoff, not a counter bug): `C1=met` does not depend on the claim's substance

Attacks: the claim that `C1=met` shows depth on invocation scope sourced on rows opened this round.
Evidence (sandbox clone; the only counter change is `REPO=` pointing at the clone, line 8):
- Mutation commit `8bd862d9` in `/fast/scratch/hyaku/mori-r30-w2/CriticC1Admission/clone`: every `shape` cell becomes
  `unrelated row N`; every `sources` cell becomes one id that does not carry that row (S158, the journald
  suppression notice, on the stamp-boundary rows `c03`/`c04`; S159, `Restart=always`, on the stamp-0 row
  `a2-05-monotonic-zero-active-quiet`; S156, the property printer, on the suppression row `a2-01`); the whole
  `## Facts` section is deleted.
- `bash count-c1-sandbox.sh HEAD` → `rows=13 rows_ok=13 new_ids=4 new_id_rows=13 excerpts_ok=4/4 skill_rows=4`, `C1=met`.
Why: `source_ids` (count-c1.sh:84) and `so` (:208-217) only check that a cited id exists and that each S156+ id passes
its own Gate. Shape needs to be non-empty and distinct (:202). Nothing ties a source to its row, and no prose is read.
The contract does this on purpose: "Uncounted residual … whether each row's shape text describes its case and
whether each cited quote supports it" (`contract.md:52-53`). So substance is decided only by wave-2 reading
(F3, F5–F8 below), never by the counter.
Impacted axes: depth (C1), provenance.
Smallest safe correction: none to the counter this round, because the residual is declared. The judge must not treat
`C1=met` as evidence that rows are sourced or shapes are correct. It should admit on the residual findings below.

## F2 — medium: the counter's tool check repeats the expect values, and A1's "nothing is narrowed" is false

Attacks: entry line 2, "every decision-table row re-derived by `count-c1.sh`", and the opening sentence of A1 at
`contract.md:124`.
Evidence:
- The base tool's selftest passes every eligible file: `python3 -I -B tool-base.py --selftest --cases …` → `PASS 32/32`
  (cases.json), `PASS 32/32` (supplementary), `PASS 30/30` (a2). Selftest compares verdict, exit and every
  `expect.fields` value (`58b61681:tools/mori-oom-killers.py:720-740`). That is the same check as `run_tool`
  (count-c1.sh:173-179), and row fields must already equal `expect.fields` (:204). So `tool=ok` cannot fail on its
  own: every row restates a frozen expect value by construction.
- Original condition 3 (`a66751b:…/contract.md:32-37`) ran the tool at `<rev>`. A1 3a runs the 58b61681 blob instead,
  which is weaker against a tip-tool regression. The loss is covered because C2 requires a tip selftest PASS, and I
  measured the tip tool: `PASS 32/32, 32/32, 30/30, 8/8`. Wave-1 F10 says the same
  (`w1/CriticC1Design.md:125-127`). No outcome changes.
- Original condition 3 also said "exists in exactly one of" the three files. A1 3a allows identical copies.
  `c02`, `c03` and `c04` each sit in both `cases.json` and `cases-supplementary.json` (my scan), so 3 of 13 rows rely on
  this relaxation (requested by `w1/CriticC1Design.md:139-147`, F12). A1 5a also drops the original per-row
  `Round30` token (count-c1.sh:225 checks only the heading).
- [INFERENCE] Dropping c02–c04 still leaves 10 rows and every threshold met (2 or more verdicts; 6 rows with two or
  more version lines; S157 is still cited by the a2-05 inactive and a2-06 inactive rows, and S160 by a2-09 and a2-10).
Impacted axes: provenance (amendment text), depth (what "re-derived" means).
Smallest safe correction: change entry line 2 to say the rows copy frozen `expect` values that the entering-tip tool
passes. In the lesson, record that A1 3a loosened two parts of condition 3 (tool revision, the "exactly one" rule),
both disclosed through wave-1 F10/F12.

## F3 — medium (defect): entry §3 and SKILL.md:754 misdescribe the round-30 tool for a stopped unit

Attacks: the entry relying on tool behaviour that the round-30 fix changed.
Evidence. Scratch variants of `a2-06-inactive-earlier-invocation-sends-acted` (`ActiveState=inactive`, stamp
`70000000`) with one send line moved or added after the last version line at `70100000`:
- V1, the only send is in the last invocation. Base tool: exit 1, `KILLER_ACTED`, `earlier_invocation_send_lines: 1`.
  Tip tool: exit 1, `KILLER_ACTED`, `earlier_invocation_send_lines: 0`, `actions: null`, `dryrun_send_lines: 0`,
  `process_group_lines: 0`. The send that causes the verdict appears in no output field.
- V2, the original three earlier sends plus one in the last invocation. Base prints `earlier_invocation_send_lines: 4`;
  tip prints `3`.
- The entry says "Sends and escalations outside the current invocation go to
  `earlyoom.earlier_invocation_send_lines`" and, for a non-active unit, "a non-zero count is `KILLER_ACTED` while
  `actions` stays `null`" (`earlyoom-invocation-scope-r30.md:48-51`). It then says the change "reports its version and
  its zero line counters" (:53-54). A reader concludes that a non-active `KILLER_ACTED` always comes with a non-zero
  count. The tip tool breaks that, and nothing says the last-invocation send goes uncounted. SKILL.md:754 carries the
  same omission.
- No table row covers it: in the only stopped-unit row with a stamp, the last invocation holds just a version line
  (case inputs: send lines at 40.1M–40.3M, last version line at 70.0M). The counter runs the base blob
  (count-c1.sh:186), so it cannot see the change.
Impacted axes: C1 correctness of prose; C2 operability (the tool now reports `KILLER_ACTED` while every count is 0).
Smallest safe correction: add one sentence to entry §3 and to SKILL.md:754. For a non-active unit with a retained
non-zero stamp, a send inside the last invocation is not counted in `earlier_invocation_send_lines` or any other
field; the verdict is `KILLER_ACTED` with every count 0 and `actions: null`. Route the missing count to the tool as a
C2 residual. Do not change the table.

## F4 — agree: no table row disagrees with the tip tool

Attacks: the risk that a row which passes under the 58b61681 tool fails under the tip tool.
Evidence: both blobs run on the inputs of all 13 cited cases (`cmp.py`, flattened full-output diff). Verdict and exit
are identical everywhere, and every cited field is identical. One row differs only in fields it does not cite:
`a2-06-inactive-earlier-invocation-sends-acted` changes `version` null→`"1.9.0"`, `grammar` `unverified`→`verified-1.9.0`,
and `process_group_lines`/`dryrun_send_lines` null→0. Its `expect.fields` does not pin these
(`cases-a2.json`: `state`, `actions`, `earlier_invocation_send_lines`, `oomd.*`). tool-base sha256 `41464957…`, tool-tip `9c88ef27…`.

## F5 — low-medium: two rows rely on a new source that does not carry their decision

Attacks: the claim that rows are sourced on rows opened this round.
Evidence (reading the cited excerpt lines):
- `a2-09-removed-unit-two-invocations-mixed-sends` cites only S160 (entry:105). S160 is journalctl's `-b`/`-u` option
  grammar (`S160.txt` lines 512-517, 543-547). It does not show that `LoadState=not-found` maps to `absent`, and it does
  not cover where a removed unit's sends are counted (A2-06/A2-09 rule text).
- `a2-10-malformed-action-line-uncounted` cites S154 (old) and S160 (entry:107). The decision is "a non-numeric
  `__MONOTONIC_TIMESTAMP` is left uncounted" (A2-10). S160 does not carry it.
- `c03` cites S157 and S160. S157 (`unit.c:2773-2774`) shows what the stamp is. The inclusive boundary is a reader rule
  (`rule-text.md:25-26`, entry:39-40), which no source carries. The same partial support applies to `c02` and `c04`.
- Supported: a2-05 rows (S156 bare decimal and `=0`), a2-01 (S158 notice wording matches the case line
  `Suppressed 42 messages from earlyoom.service`), a2-06/a2-07 rows (S159 restart → several invocations; S155 dry-run).
Impacted axes: depth, provenance.
Smallest safe correction: remove S160 from the a2-09 and a2-10 rows, or replace it with a source that carries the
decision. Mark both rows as grounded in rule text (A2-09, A2-10), not in a round-30 source. new_id_rows stays ≥3.

## F6 — low: novelty is checked by exact URL match, so a same-fact or same-file source passes

Attacks: S-ids whose URL duplicates an older row's companion file or fact.
Evidence:
- Companion files cited "by path only" (`systemctl-show.c` in S156; `journalctl-filter.c` and `journalctl-util.c` in
  S160) appear in no older SOURCES row (rg over `ad0f0474:corpus/SOURCES.md`: hits only at :162 and :166). No
  duplicate companion file.
- S159 (`edd3d943.patch`) carries `Restart=always`. S120 already anchors the same directive
  (`corpus/SOURCES.md:126`, "`:17 (Restart=always)`"). The Gate rejects S120's URL as a duplicate
  (`corpus/lessons/round-30.md:136`) and admits a 2020 commit patch that carries the same directive (:135). The only new
  content is the commit-message purpose sentence, which entry:23-24 quotes.
- S157 reopens `src/core/unit.c` (v262), which S036 already carries at commit `cf8ebfc6` (`corpus/SOURCES.md:42`).
  The function differs (`unit_notify` against `unit_log_failure`).
- The novelty test compares exact URL strings only (count-c1.sh:141, :195), so both pass.
Impacted axes: provenance. Smallest safe correction: in the S159 row, state that the `Restart=always` fact is S120's and
that S159 adds only the purpose sentence. No count change.

## F7 — low: the disputed shape has no table row; SKILL counts it through a case that doesn't show it

Evidence: among eligible cases (blob equal to 58b61681), only two are `ActiveState=active` with stamp 0 or missing,
`a2-05-monotonic-zero-active-quiet` and `a2-05-monotonic-missing-active-oomd-notices`. Each has 1 version line (my
scan), so no eligible case has the disputed shape. SKILL.md:753, the disputed-shape row, counts toward 5a through
`a2-06-active-earlier-invocation-sends-quiet`. That case is bounded (stamp `64000000`, `scope_complete=true`) and does
not show the shape. Entry §4's own claim does hold: both tools print `PASS 8/8` on
`cases-a2-r30.json`, and all 8 expect `KILLERS_UNKNOWN` exit 2 with `scope_complete: false` and `sigterm: 0`.
[INFERENCE] S157 says each entry into active overwrites the stamp (`unit.c:2773-2774`), and that includes
`Restart=always` restarts. So an active unit with a readable stamp of 0 and two or more version lines needs a path
outside normal transitions; the entry does not say this (entry:32-35, :59-71).
Impacted axes: depth. Smallest safe correction: state in §4 that this shape is a robustness input which no eligible
case pins and which normal transitions do not produce; name `cases-a2-r30.json` as SKILL.md:753's grounding, not the a2-06 case.

## F8 — low: the recheck instruction can't be followed as written

Evidence: entry:3 says to re-run `count-c1.sh <rev>` "against the new blob by hand" after a tool change. The counter
hardcodes `BASE` (count-c1.sh:8) and reads the tool from it (:186). There is no tool argument.
Smallest safe correction: change the recheck text to "run `--selftest` on the three eligible files and the C2 file
with the new tool".

## Summary for the judge

The counter is correct to its text (F4, baseline) and the sources reproduce byte-for-byte. Its met value carries no
substance on its own (F1, F2). On the residual reading, the decision table is accurate, but the round-30 stopped-unit
behaviour is misdescribed in the prose and SKILL (F3), and two rows have decorative new sources (F5). All are fixable
in text; none requires rejecting C1 outright. F3 should be fixed before the entry is cited as current tool behaviour.
