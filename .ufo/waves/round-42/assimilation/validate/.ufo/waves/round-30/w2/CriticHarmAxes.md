Verdict: defect found — no regression on any of the six axes at `ad0f0474` vs `58b61681`; two small fixable defects
(dangling SCORECARD receipts; a stale tool comment) and one disclosed-worthy tradeoff in the tool fix.

# CriticHarmAxes — no-harm attack, round 30, tip ad0f04745ced2194e58c22a0d6b38131bee3e230 vs 58b61681

Seat: MoriR30.CriticHarmAxes (critic, leaf). Item attacked: the round-30 diff as a whole, on six axes.
Sandbox: clone plus `base`/`tip` worktrees under `/fast/scratch/hyaku/mori-r30-w2/CriticHarmAxes/`.
Scratch scripts: `diff.py` (full-output differential), `cx.py` (synthetic counterexamples), same directory.
Tools installed or updated: none. Lane writes: this file only.

## Shape of the diff

- `git diff --stat 58b61681 ad0f0474`: 73 files, 9726 insertions, 28 deletions. Only three files lose lines
  (`git diff --numstat ... | awk '$2>0'`): `PROVINCE.md` 29/13, `SKILL.md` 14/1, `tools/mori-oom-killers.py` 28/14.
  Every other touched file, including SCORECARD, LOG, QUALITY and SOURCES, only gains lines.
- All 73 paths sit inside the lane repo. No sibling-lane or fleet-root file is in the diff.

## Axis 1: coverage (PROVINCE and SKILL) — no harm

- The PROVINCE edits replace lines one for one in every hunk (`git diff -U1 ... -- PROVINCE.md`: hunks
  `-24,3 +24,3`, `-46,3 +46,3`, `-65,5 +65,5`, `-89,3 +89,3`, `-93,3 +93,3`, `-235,3 +235,3`, `-282,3 +282,3`,
  `-293,3 +293,3`, `-352,4 +352,4`, `-358,3 +358,3`, `-374,3 +374,3`). The new block is appended at `PROVINCE.md:386-400`,
  so existing citations into PROVINCE keep their line numbers.
- I checked every line pointer the correction block uses (`:22,25,28,44,47,57,66,68,90,94,103,108,125,132,134,145,236,
  283,294,321,353,354,359,375`, via `sed -n Np` on `git show ad0f0474:PROVINCE.md`). Each one lands on the bullet or
  row the block names.
- Admission states are confirmed by fleet `git show 63729047:MANIFEST.json`: mori round 16 `admitted`, 24 `admitted`,
  25 `admitted`, 26 `admitted`, 27 `rejected-honest-stop`. These match the new wording at `:25,236,283,294,353-354,359,375`.
- Repointed paths resolve:
  - `../.ufo/waves/kaika-w1/mori-state.md` exists (297 lines). `:31` is the driver-counter row and `:190` is C15.
  - `:180` (the C5 row) does contain "`/scratch` is absent (`ls /scratch` → No such fil…".
  - `../.ufo/waves/kaika-w1/mori-art.md:91-124` is the S001–S030 table. `fleet-ledger/` does not exist at the fleet root.
  - `../tsukuroi-shokunin/PROVINCE.md:8-14` is tsukuroi's "Owns" block.
  - `SKILL.md:374` is `## Secret-exposure exclusions`.
  - `corpus/lessons/round-16-verifier-spotcheck.md:11` reads "admitted: true · verdict: admitted".
- SKILL: one changed line, `:661`, now cites `.ufo/waves/round-25/contract.md:83-85`. Line 85 carries "The live
  running-job count is not readable from outside the session", the claim being cited. The other 14 lines are
  the appended `## Round30` section at `SKILL.md:744-755` (plus one blank line). No older row changed.
- [INFERENCE] Not a harm, a gap: PROVINCE gains no round-30 Core/FR10 note for the new entry or for the tool's
  non-active scoping change. The round-26 bullet at `PROVINCE.md:359-364` stays true at the tip (it describes inputs,
  schema and verdict names, not non-active field values).

## Axis 2: operability (older verdicts, differential) — no harm on frozen inputs; one unpinned divergence

- Selftests, base tool vs tip tool, over every fixture file at the tip:
  - Base tool: `cases.json` PASS 32/32, `cases-supplementary.json` PASS 32/32, `cases-a2.json` PASS 30/30,
    `cases-a2-r30.json` PASS 8/8. `cases-a2-r29.json` fails, first problem
    `r29-a2-10-not-found-earlier-stamped-positive: earlyoom.version: got null expected "1.9.0"`.
  - Tip tool: 32/32, 32/32, 30/30, 24/24, 8/8.
- My own differential (`python3 -I -B diff.py`) runs both `read_inputs` over every case input of the five files.
  Output: `total=126 changed=5 verdict_changed=0`. The five changes are the same five ids listed in the author's
  `.ufo/waves/round-30/evidence/c2-differential.txt`. Every change is a non-active unit (state `inactive`, `unavailable`
  or `absent`) gaining `version`/`grammar` and moving `dryrun_send_lines`/`process_group_lines` from null to 0.
  One field moves in a way worth noting: `r29-a2-10-failed-stamped-positive` has
  `earlier_invocation_send_lines: 1 -> 0`, because the send is now inside the last invocation. Its verdict stays
  `KILLER_ACTED` either way.
- Counterexample (unpinned shapes). The fix (`tools/mori-oom-killers.py:304-321`, `:471-483`) moves a stopped
  unit's lines at or after the retained stamp out of the earlier-line path, where each version segment is dry-run
  aware for sends and escalations (`:343-358`). They go into the scoped path, where escalations are counted outside the
  per-segment dry-run split (`:409-410`) and the segment opened before the stamp is lost. Synthetic inputs built from
  the `a2-06-inactive-earlier-invocation-sends-acted` template (`python3 -I -B cx.py`, inactive unit, stamp 1000):
  - X1, dry-run invocation (version, `dryrun mode enabled`, send) plus one `escalating to SIGKILL after` line, all after
    the stamp: base `KILLERS_QUIET 0`, tip `KILLER_ACTED 1`.
  - X2, version and `dryrun mode enabled` logged before the stamp, send after it: base `KILLERS_QUIET 0`, tip
    `KILLER_ACTED 1`.
  - X3, dry-run invocation with sends only, and X4, real send after the stamp: same verdicts on base and tip.
- Reachability: neither flip can come from stock earlyoom 1.9.0.
  - In dry-run, `kill_wait` returns at `kill.c:271-273`, before the escalation message at `kill.c:318`
    (https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c, fetched with curl this session).
  - The shipped unit sets no `Type=` (`earlyoom.service.in:7` ExecStart, `:17` Restart=always;
    https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/earlyoom.service.in), so [INFERENCE] it is `Type=simple`
    and the active-enter stamp comes before earlyoom's first log line. `userspace-oom-killers-r26.md:119-121` flags the
    same dependency.
  - An active unit already behaved like X2 at the base. The scoped path's segment starts at the stamp, and frozen `c04`
    pins `KILLER_ACTED` for "version before stamp, send after".
  - Classification: a tradeoff, not harm. The author's differential gate counts only `acted_lost`
    (`.ufo/waves/round-30/c2-differential.py:69-70`), so it could not see an ACTED gain. No frozen input produces one.
- Smallest safe correction: disclose X1/X2 as unpinned in the round-30 lesson or the entry's Limits. Optional: freeze
  them as cases, so the scoped path's dry-run handling for stopped units is pinned.

## Axis 3: depth (contradiction with older entries) — no harm; one stale code comment

- `corpus/knowledge/userspace-oom-killers-r26.md:200` says an inactive or absent earlyoom has "no current invocation:
  its action counts are `null` … send lines earlier in the same boot are still positive evidence". This still holds:
  `actions` stays null for non-active units (`tools/mori-oom-killers.py:442-449`), and a send either side of the stamp
  still makes the unit `KILLER_ACTED` (`:474-482`).
- The new entry speaks of the stopped unit's *last* invocation, not a current one
  (`earlyoom-invocation-scope-r30.md:52`), so it does not conflict with r26 F6 (`:112-121`). No entry in
  `userspace-oom-killers-r12.md`, `oom-victim-selection-r27.md` or `structured-journal-scopes-r13.md` speaks to
  invocation bounds (grep for `ActiveEnter|restart|invocation`: only r27 `:135`, unrelated).
- C1 counter re-run from its blob at the tip: `bash <(git show ad0f0474:.ufo/waves/round-30/count-c1.sh) ad0f0474` →
  `rows=13 rows_ok=13 new_ids=5 new_id_rows=13 excerpts_ok=5/5 skill_rows=4`, `C1=met`, exit 0.
  - The counter runs the entering-tip tool blob (`count-c1.sh:186` `tool_data=blob(BASE,TOOL)`), as the entry's
    `verified-at` line discloses (`:2`).
  - Under the tip tool, the only table row whose case changed is `a2-06-inactive-earlier-invocation-sends-acted`. Its
    tabled fields (`earlier_invocation_send_lines=3`, `state="inactive"`) are unchanged (differential above), so all
    13 rows also hold for the shipped tool.
- Defect, fixable: the comment at `tools/mori-oom-killers.py:323-329` still says "For an earlyoom that is not active,
  every boot line belongs to an earlier invocation". The fix makes that false whenever a non-zero stamp is retained
  (`:304-321`).
  - Smallest correction: reword it to "lines before the retained stamp, or every line when no stamp is retained".

## Axis 4: freshness (older SOURCES rows) — no harm

- `git diff 58b61681 ad0f0474 -- corpus/SOURCES.md | grep '^-[^-]'` prints nothing: no older row is removed or edited.
- The diff adds rows S156–S160 after S155 (hunk `@@ -159,6 +159,11 @@`) and one append-only correction paragraph
  after Round 24's bounded-search paragraph (`@@ -205,6 +210,8 @@`). That paragraph states no S153–S155 cell is edited.
- No new URL duplicates an older mori row. `grep -oE 'https://…' corpus/SOURCES.md | sort | uniq -d` lists only
  pre-existing duplicates (earlyoom tree API, pathlib, bash tarball, …), none from S156–S160.
- S157's `src/core/unit.c` is at tag v262. S036's `unit.c` is at commit `cf8ebfc6…` (`SOURCES.md:42`). Different
  revision and scope.
- No sibling `corpus/SOURCES.md` contains any of the five new source paths (grep for `bus-print-properties.c`,
  `src/core/unit.c`, `journald-manager.c`, `src/journal/journalctl.c`, `edd3d9438dc5` across `*/corpus/SOURCES.md` hits
  only mori). The PROVINCE "Source overlap: no shared URL" note (`:90`) stays true.

## Axis 5: calibration (SCORECARD) — scores unchanged; one dangling-receipt defect

- The SCORECARD diff is a single hunk `@@ -1798,3 +1798,28 @@` with no removed line. The `## Axes` table at
  `SCORECARD.md:6-20` is untouched.
- The declared "Held and observed" line (`:1813`) gives freshness 5, calibration 5, coverage 6, adjacency 6. The
  measured "Held" line (`:1823`) gives depth 5, freshness 5, coverage 6, operability 7, adjacency 6, calibration 5. These equal the round-29 held line (`:1799`). No score moved; C1 is
  "improved, pending closure" and C2 is reported as a miss (`:1820-1821`).
- Retention no-harm re-run (`tools/mori-retention-gate.py scan --repo <clone> --rev R --policy
  .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json`):
  `58b61681 metric 4 non_author 5`, `ad0f0474 metric 4 non_author 5`. The metric did not rise, matching `:1824`.
- QUALITY and LOG gain lines only (QUALITY `@@ -462,3 +462,202 @@`, LOG `@@ -1948,3 +1948,41 @@`); no older
  criterion is rescored.
- Defect (false provenance at the measured tip): `SCORECARD.md:1824-1825` cites "Tip receipts:
  `.ufo/waves/round-30/evidence/tip-c1.txt`, `tip-c2.txt`, `tip-retention.txt`". None of the three exists at
  `ad0f0474` (`git cat-file -e` fails for each). The lane working tree at HEAD `713be29` does not have them either
  (`ls .ufo/waves/round-30/evidence/`).
  - QUALITY criterion 84 (`corpus/QUALITY.md:401`) requires the last lane batch to carry exactly these receipts.
  - Smallest correction: land the three receipts in the receipts-only batch before closure, or mark the sentence
    "to land in the receipts-only batch" until then.

## Axis 6: adjacency (sibling files) — no harm

- No sibling or fleet file is in the diff (see Shape). Sibling citations only changed in PROVINCE `:66` (tsukuroi
  range) and `:47/:90/:94` (fleet-root `kaika-w1` files), all verified above.
- These sibling citations are still not pinned to a revision (`../tsukuroi-shokunin/PROVINCE.md:8-14` has no `@rev`,
  unlike souji's at `:69`). That is carried drift risk, not a new harm.
- No sibling knowledge entry mentions `ActiveEnterTimestampMonotonic` (`grep -rln` over `*/corpus/knowledge`,
  mori excluded: no hits). The new entry's invocation-boundary claim duplicates no sibling authority. Its
  "host OOM configuration stays with tsukuroi" line (`earlyoom-invocation-scope-r30.md` `## Adjacent`) keeps
  tsukuroi's ownership.

## Privacy observation (outside the six axes; retention metric unchanged)

- Three new tracked files carry a literal user-manager unit name of the form `user@<this host's uid>.service`. The
  digits equal `id -u` here; the value is withheld per bounds. The files are
  `.ufo/waves/round-30/wave1-dispatch.json:55`, `wave1-run.json:292` and `wave1-spec.json:50`, each inside the
  RetentionBase seat prompt as a "synthetic service-manager-style token" example.
- Files matching `user@[0-9]+\.service`: 86 at base, 89 at tip (`git grep -lE`). The frozen scan does not count this
  form (metric 4 → 4), which is its disclosed recall limit (`.ufo/waves/round-18/frozen/c1-policy.json:29`, per
  RetentionBase).
- Smallest correction: in future dispatch payloads, use a placeholder such as `user@<uid>.service` instead of the
  host's digits.

## Checks run (all in the sandbox; none unrun counted as pass)

- `--selftest --cases <file>` × 5 files × {base, tip}; `diff.py`; `cx.py`.
- `count-c1.sh` from blob at the tip.
- Retention scan at both revisions.
- MANIFEST read at fleet `63729047`.
- Line checks on PROVINCE, SKILL, SCORECARD and the fleet `kaika-w1` files.
- curl of two earlyoom v1.9.0 files.

Not checked: the five word counts in the SOURCES correction note (owned by ReviewCorrectionsR2R3); C2's counter
(owned by other seats).
