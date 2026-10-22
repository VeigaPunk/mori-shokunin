# Round 26 — non-author verifier spot-check (mori)

author: hyaku closure (non-author integrator, @m_opus)

Runtime model as exposed to this closure session: `anthropic/claude-opus-5-5` (configured `task` route, no
model parameter passed). Closure dispatched by the hyaku orchestrator, not by the lane. Measured 2026-10-22
(UTC ~14:50Z) against base `248408f5b6610a85bcbdebe7ac0b4fa7ed51422a` and head
`ef9dbee136d6ed2ef98687f5cb0c0a16506a5155` (`master` = `origin/master`). Report: `.ufo/reports/round-26/mori.md`
(fleet repo). No review seats were dispatched; every re-check below was run by this closure. No lane tool or gate
was executed (PROTOCOL §Gate standard, Closure consequence): the measurements are git, grep, jq, curl and a
Python regex re-implementation of the frozen retention policy over committed blobs. The lane's committed
`count-c1.sh` (git reads only, not a gate) was also run, for comparison with the plain grep.

**Admitted.** Both declared claims re-derive against committed bytes and no owned or held axis is harmed at the
head. C1 was re-measured with a plain fixed-string grep per frozen phrase (4 → 0) and with the committed counter
(same values). C2's before-value, freeze order, case count and frozen-file identity were re-measured; its
`PASS 32/32` is evidence-verified, not re-run. The retention scan was re-implemented from the frozen policy and
reads 4 at base and 4 at head. This note checks no SHONEN box.

## Conformance (step 1)

| Check | Command | Observed |
|---|---|---|
| report lands under the lane identity | `git -C <fleet> log --format='%an %H %ci' -- .ufo/reports/round-26/mori.md` | 1 commit, `mori-shokunin` `e9943445` at 11:41:05-03:00: after the lane tip (11:40:06) and before the driver `complete` line (11:41:32) |
| driver digest (copied from mutable `.ufo/watchdog.log`) | `grep 'mori round=26' .ufo/watchdog.log` | `2026-10-22T10:05:13-03:00 launch mori round=26 pgid=1826598 driver=hyaku-inline attempt=1`; `2026-10-22T11:41:32-03:00 complete mori round=26; hyaku-inline attempt=1` |
| SHONEN heading, one line per box | report `## SHONEN`; `SHONEN.md` | 4 report lines (`[~]`, `[~]`, `[ ]`, `[~]`) for 4 boxes; `SHONEN.md` all `[ ]` |
| cited commits exist and are ancestors | every backticked 8–40 hex token; `git merge-base --is-ancestor <h> refs/heads/master` | 27 distinct tokens (24 distinct commits, two cited both short and full); 26 resolve to ancestors of `master`; `deadbeef` is the counter's deliberate bad-revision probe, not a citation. `28b04940` carries author date 09:28:23 (inherited by jj from the change) but committer date 10:10:20, after the launch |
| pushed | `scripts/hyaku/jj-lane.sh state <lane>`; `git ls-remote origin refs/heads/master` | `local=remote=ef9dbee1… ahead=0 behind=0 head=detached tracked=1 untracked=4` |
| uncommitted leftovers | `git status --porcelain`; `stat` mtimes | 5 paths; ruled below |
| prompt carries the template contract | `diff <(sed -n 1,140p .ufo/prompts/mori-round-26.md) templates/round-prompt.md` | 22 differing lines: 11 template placeholder lines (`{{…}}`) against their 11 substitutions; §6 hyaku addendum appended at line 141 (prompt 350 lines) |
| seat shape | `wave{1,2}-run.json` `tasks[].agent`; `git ls-tree` of `w1/`, `w2/` | wave 1: 35 (16 scribe, 6 reviewer, 3 executor, 3 scout, 3 critic, 2 connector, 2 mutation-tester), 35 reports committed; wave 2: 34 (22 reviewer, 6 critic, 5 mutation-tester, 1 scout), 17 reports committed. Totals 69 and 44 attack, as reported |
| sources census | `scripts/sources-census.sh validate --root <fleet> mori` | exit 0, `ok`; 6 W04 warnings (S035, S037, S073–S076), all pre-existing rows, as the report says |

**The five uncommitted paths — rulings.**

| Path | Evidence | Ruling |
|---|---|---|
| `.scratch/` | newest mtime 2026-10-21 | inherited, not round work (same as round 25) |
| `.ufo/waves/round-26/w2/OperabilityNoHarm.md` (modified) | mtime 11:39:59, after the commit that landed it (`ea4c92f6`, 11:39:09–11:39:43); `git diff` is 8 lines of prose rewording; verdict, method, the five exit codes and every tally are unchanged | a late rewrite by the returned seat. Not new round work; the committed version is the evidence this note uses |
| `.ufo/waves/round-26/w2/ReopenS116S117.md` (new) | mtime 11:40:05; a returned seat (one of the 19); the report cites its S117 finding ("Wave-2 ReopenS116S117 found S117's description … differs") | **round work, uncommitted.** A report statement rests on a file that is not in committed bytes. Conformance defect (status-neutral); routed D1 |
| `.ufo/waves/round-26/w2/ReopenS118S119.md` (new) | mtime 11:40:05; seat listed as cancelled in the report; the file is a complete report with a verdict table (S118 holds, S119 holds) | late output of a seat the report counts as cancelled; not cited, not integrated. Not counted as round work here; routed D1 |
| `.ufo/waves/round-26/w2/ReviewEntryOomdFacts.md` (new) | mtime 11:40:05; seat listed as cancelled; complete report (21 statement verdicts, 4 low wording defects, 0 overturned claims) | as above; its findings are not counted for or against the round; one of them (O10) is re-checked below and routed as D4 |

All three new files carry mtimes within 70 ms of each other, 1 s before the final lane commit `ef9dbee1` (11:40:06),
which committed only the withholding change. The regex classes of the frozen retention policy match 0 lines in
each of the four w2 files.

**Attack share on returned seats.** Wave 1: 11 of 35 attack seats (31%), all returned. Wave 2: 19 returned (17
committed, `RetentionTip` withheld, `ReopenS116S117` uncommitted); 18 of them are attack seats (reviewer, critic or
mutation-tester; the 19th is `ScoutMisroot`): 95%. Counting the two late complete reports as returned gives 20 of
21. Round, returned seats: 29 of 54 attack (54%). The ≥25% rule holds per wave and for the round, on returned
seats. Cancellation: 15 of 34 wave-2 seats (44%) by the L1 at its run budget, not dead seats.

**Drift rule.** `MANIFEST.json` closures for mori rounds 23, 24 and 25 each grade `calibration: improved` (the
routed repair). Round 26 claims freshness (C1) and coverage (C2), both on FR10 userspace OOM killers, and counts
no calibration claim: the round is on a new frontier area, not a third routed-repair round. Watch item, not a trip:
coverage via a new one-shot read tool is now three rounds running (r24 pressure, r25 job runway, r26 OOM killers),
each on a different surface.

## Claims (step 2)

### C1 — freshness: stale FR10 host-state statements 4 → 0, superseding entry present (re-measured)

Declared after (contract `28b04940`, C1): at the landed tip none of the four frozen phrases remains, and
`corpus/knowledge/userspace-oom-killers-r26.md` exists whose `source:` line cites at least one SOURCES row opened in
round 26.

```
for R in 248408f5 ef9dbee1; do while IFS='|' read -r f p; do git show "$R:$f" | grep -c -F -- "$p"; done \
  < <(git show 28b04940:.ufo/waves/round-26/c1-phrases.txt); done
```

Observed: base `1 1 1 1` (4 present); head `0 0 0 0` (0 present). The committed counter
`bash .ufo/waves/round-26/count-c1.sh <rev>` prints `stale_present=4 r26_entry=absent r26_new_source_ids=0
r12_names_r26=0` at base and `stale_present=0 r26_entry=present r26_new_source_ids=13 r12_names_r26=4` at head,
both exit 0; the committed receipt `evidence/c1-count.txt` holds the same values at `327fbcca` and `950d8a56`.
The r26 `source:` line names S114–S126 (13 ids, all above S113).

The phrases were corrected, not hidden. `git diff 248408f5 ef9dbee1 -- corpus/knowledge/userspace-oom-killers-r12.md
corpus/README.md` shows each stale line rewritten as a dated 2026-10-19 reading that names the r26 entry. The
counter cannot see a phrase inside markup or in another file (MutC1Script, 4 of 19 mutants), so this closure swept
the head tree independently:
`git grep -i -E 'earlyoom[^.|]{0,80}(inactive|not[- ]found|not installed)|(inactive|not[- ]found)[^.|]{0,60}earlyoom|both (killer|userspace|service)[^.|]{0,40}inactive' ef9dbee1 -- corpus SKILL.md PROVINCE.md SCORECARD.md`
gives 11 lines; every one is dated, conditional (a decision-table row about an inactive earlyoom), a registry or
limits row, or lesson narrative. No undated present-tense "inactive" statement about this host's earlyoom remains.

Host truth behind the claim (read-only probes this closure ran): `systemctl is-active/is-enabled earlyoom.service`
→ `active`, `enabled`; `systemd-oomd.service` → `inactive`, `disabled`; `pacman -Q earlyoom systemd` →
`earlyoom 1.9.0-1`, `systemd 262-1`. These match the r26 entry.

**C1 verified.** Freshness: `improved` (bounded to the four frozen phrases plus the superseding entry, as declared).

### C2 — coverage: `tools/mori-oom-killers.py`, PASS 32/32 on frozen cases (before and freeze re-measured, after evidence-verified)

- Before: `git show 248408f5:tools/mori-oom-killers.py` → `fatal: … exists on disk, but not in '248408f5'` (absent).
- Freeze order: `git log --diff-filter=A ef9dbee1 -- <cases> <tool>` → cases first added at `5b10649d`, tool at
  `c2fdd929`; `git merge-base --is-ancestor 5b10649d c2fdd929` holds; `c2fdd929` adds only the tool (734 lines).
- Frozen file unchanged: `git diff --name-only 5b10649d ef9dbee1 -- tools/fixtures/mori-oom-killers/cases.json` → 0
  lines; blob `5b4dcee7…` at both revisions. `jq '.cases|length'` → 32 at both.
- Separate seats: `wave1-run.json` lists `WriteOomKillersCases` and `BuildOomKillersTool` as two executor seats;
  both reports are committed under `w1/`. That the tool seat never read the cases rests on the seat reports and
  the commit order, not on anything a closure can re-derive.
- Committed evidence: `evidence/c2-selftest.txt` names revision `950d8a56`, tool blob `3fb78bbc…`, cases blob
  `5b4dcee7…`, `MORI_OOM_KILLERS_SELFTEST: PASS 32/32`, exit 0; `evidence/c2-count.txt` at `950d8a56`:
  `freeze_order=ok cases_changed_since_freeze=0 N=32 … PASS 32/32 exit=0`. `git rev-parse ef9dbee1:tools/mori-oom-killers.py`
  → `3fb78bbc…` and `git diff --stat 950d8a56 ef9dbee1 -- tools` is empty, so the receipt's revision is the head's
  tool and cases bytes.
- Registry: `SKILL.md:716` carries a row for the tool (gate, entry command, self-test spelling).

Limits, as the lane disclosed (SCORECARD "Round 26 wave-2 corrections"): `PASS 32/32` certifies the pre-freeze
rules only. The amendment-A2 rules (process-group and dry-run lines, journald suppression, non-steady states,
earlier invocations, the readability probe, unplaceable timestamps) are pinned by no committed case file; they are
shown by detector inputs under `evidence/a2-detectors/`. `count-c2.sh` exits 0 even when the self-test fails
(RerunC2Count, low). The capability row states these limits.

**C2 verified (evidence-verified after-value).** Coverage: `improved` (bounded: agreement with 32 cases written by a
separate seat before the tool).

## No-harm checks (re-measured)

| Axis / rule | Measurement | Observed |
|---|---|---|
| privacy (retention scan, binding) | Python re-implementation of `.ufo/waves/round-18/frozen/c1-policy.json` (9 regex classes over every non-binary tracked blob, `non_author_paths_glob` excluded) against `corpus/evidence/retention-allowlist.json` (path, class, line sha256) at each revision | base: 109 hits, 5 excluded, 100 allowlisted, **4 unallowlisted** (matches `evidence/retention-scan-base.txt`); head: 113 hits, 5 excluded, 104 allowlisted, **4 unallowlisted**. The same 4 lines in one round-20 file at both revisions. Not higher at head |
| privacy, what was added | hits present at head and absent at base | 4 new hits, all class R7 (a path name of the operator's harness configuration file): `SKILL.md` (the round-25 runway registry row's `--config` default), `wave1-spec.json`, `wave1-run.json` (a never-edit boundary), `w1/DraftSkillFr10.md`. Each is name-only; 4 new name-only allowlist rows cover them. 0 new hits in the session-identity, session-store, routing-key or session-record classes. No settings value and no session identifier added |
| operability | committed `w2/OperabilityNoHarm.md` | five assigned selftests exit 0 with their recorded tallies; no tool or fixture byte changed (`git diff --stat 16935e24 -- tools/` empty in that report). The later uncommitted rewrite changes no number |
| SCORECARD axes | `git diff 248408f5 ef9dbee1 -- SCORECARD.md` | no score changes; the operability evidence cell gains the routed R4 correction ("first admitted in round 14"); the round-26 sections hold freshness 5 → 5 and coverage 6 → 6 pending closure |

## Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| freshness | improved | C1 re-measured 4 → 0 with dated corrections and a superseding entry; three r14 `systemd 261` lines dated too |
| coverage | improved | C2 capability evidence-verified, before and freeze re-measured |
| operability | unchanged | selftests and tallies hold (committed wave-2 report) |
| depth | unchanged | held |
| calibration | unchanged | held; no calibration claim |
| adjacency | unchanged | sibling tsukuroi cited as S125 (tier B), not absorbed; PROVINCE adjacency unchanged |

## Discernment spot-check (step 3)

The lesson's `## Gate` admits 13 rows and rejects none. The reject sampled here is the seat-level reject recorded
in the wave-1 Gate block the lesson points to.

| Item | Decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S114 earlyoom README at v1.9.0 | admit, A, mined | `curl -fsSL https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md`; line 28; `sha256sum` | agree | line 28 is the Gate quote verbatim (15 words); sha256 `23411dbf…74dd` equals the entry's `source:` line; tags API: `v1.9.0` → annotated tag `66d78843…` → commit `202d4db0…`, as recorded |
| S118 earlyoom kill.c at v1.9.0 | admit, A, mined | same tag, `kill.c` line 318 | agree | `warn("escalating to SIGKILL after %.3f seconds\n", secs);` holds the Gate literal at :318 |
| S124 systemd v262 resource-control and oomd man pages | admit, A, mined; `teaches` corrected same round | `systemd.resource-control.xml` lines 1545–1548; `systemd-oomd.service.xml` lines 42–53 | agree with the admit and the corrected `teaches` | :1545–1546 hold the Gate quote (16 words, markup stripped); :1546–1548 and oomd.service.xml (only descendants of a `kill` unit are candidates) ground "a unit at `auto` becomes a kill candidate only under a `kill` ancestor". The in-place `teaches` edit is a rule defect (D3) |
| S117 earlyoom tag and release history | admit, A, mined | `https://api.github.com/repos/rfjakob/earlyoom/releases/tags/v1.9.0` | agree with the admit; the Gate record is weak | `tag_name` `v1.9.0`, `published_at` `2025-09-16T19:11:03Z`, as quoted; but the quote is a JSON field, not a line, and grounds the date, not `teaches` (grammar stability across v1.7–v1.9.0). The entry's `source:` line describes S117 as the releases page plus a `commits?path=main.c` query about the kernel-oom history, which is not the row's scope or URL set (D2) |
| S126 Arch PKGBUILD at `704e0571` | admit, A, mined | GitLab raw PKGBUILD lines 5–6 | agree | `pkgver=1.9.0` / `pkgrel=1`, as quoted; matches `pacman -Q earlyoom` on this host |
| `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service` | reject as a citation target (unopenable), wave-1 SrcEarlyoomUnit Gate block | `curl -sS -o /dev/null -w '%{http_code} %{size_download}'` | agree | `404 14`; the tag carries the template `earlyoom.service.in` instead (S120), which was admitted |

New SOURCES row re-opened: S124 (`corpus/SOURCES.md:130`). Its anchor (`:1545-1548`, oomd.service.xml `:44`,
`:48-52`) resolves to the cited text at tag v262, and its Gate quote has 16 words (≤25). `git diff` of
`corpus/SOURCES.md`: 13 rows added, 0 removed. All 13 are `mined` with `used-by`
`corpus/knowledge/userspace-oom-killers-r26.md`. Census validate exit 0 (above).

## Trend verdicts

- **expansion: improved.** A new entry on FR10 ground the r12 entry did not hold (earlyoom 1.9.0 act rule, startup
  thresholds, message grammar, the kernel-counter split), each `source:` id a `mined` row opened this round (S114–S126);
  README coverage row and FR10 frontier row updated; one capability row (C2) evidence-verified.
- **quality: improved.** The stale r12 host-state reading is superseded and its four stale lines dated (C1, re-measured);
  r12 line 6 now scopes `--kernel-oom` to the master README (QUALITY 79); three `systemd 261` lines in
  `journal-alarm-routing-r14.md` dated (`cb5c2f78`). No admitted entry failed its re-check here. The S117 citation
  mismatch (D2) is a citation defect, not a false statement: the kernel-oom fact it is cited for is also anchored in S114.
- **discernment: improved.** This spot-check agrees with the gate on 5 admits and 1 reject. The round mined four
  mistakes (M1–M4) and each new QUALITY criterion cites one (78 ← M1, 79 ← M4). The gate's weak spots are routed
  (D2, D3), not disagreements with an admit or reject decision.

## SHONEN (operator note, promotion is operator-owned)

Boxes 1 and 2 look checkable from committed bytes by a non-author (SKILL.md "Round26 — userspace OOM killers" table
with cited rows; `LOG.md` round-26 outcome plus the committed live run). Box 4 rests on the PROVINCE adjacency note.
Box 3 was not assessed. This note writes no `[x]`.

## Routed defects (the lane fixes these in round 27; this note changes no target)

- **D1 (medium) — uncommitted round work.** `w2/ReopenS116S117.md` is cited by the report but uncommitted;
  `w2/ReopenS118S119.md` and `w2/ReviewEntryOomdFacts.md` are complete reports from seats the report counts as
  cancelled; `w2/OperabilityNoHarm.md` has a later prose rewrite. Commit them as late wave-2 reports (after the
  retention scan) or record their disposition in the round-27 lesson, and correct the returned/cancelled tally.
- **D2 (medium) — S117 citation.** The r26 entry's `source:` line describes S117 as a different source than the row
  (URLs and scope); the Gate quote is unlocated and does not ground `teaches`. Align the entry's description with the
  row or open a new row for the kernel-oom history.
- **D3 (low) — S124 `teaches` changed in place.** CORPUS.md Rules 2 allows in-place changes only to `status`, `recheck`
  and `used-by`; a correction is a new row opening `supersedes S124 —`. The old → new is logged in the lesson.
- **D4 (low) — r26 entry wording.** The decision-table row reads the oomd xattrs as "accounting of its kill attempts and
  killed pids"; `oomd-util.c` (v262) `:306` adds a count of processes killed, and no pid is stored. Say "a count of kill
  attempts and a count of processes killed". Other low wording items are in the uncommitted ReviewEntryOomdFacts report.
- **D5 (low) — README r26 row** names `S114–S125`; the entry cites S114–S126.
- **D6 (low) — `count-c2.sh` exits 0 when the self-test fails** (RerunC2Count); its result line is the only signal.
- **D7 (low) — C2 coverage gap.** No case file pins the amendment-A2 rules or the mem/swap threshold order; the
  supplementary file kills only one of those mutants. Freeze new cases by a separate seat before claiming them.
- Still open from round 25 (named debt in the lesson): R1, R3, R7, and R5's routed-check self-test.
