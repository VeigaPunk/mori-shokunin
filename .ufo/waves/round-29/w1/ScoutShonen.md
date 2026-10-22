# Round-29 w1 — ScoutShonen: SHONEN.md status at `7118f320`

Question: for each of the four boxes of `SHONEN.md:5-8`, how far is the lane at `7118f320`, and what recommendation
follows. Method: contract read first; read-only git/read only; no edits outside this report and
`/fast/scratch/hyaku/mori-r29/ScoutShonen/`.

Blindness kept: I did not open, grep, copy or run `tools/mori-oom-killers.py`, and I opened no round-26/27/28
`w1`/`w2` report. I did read the non-author closure records `corpus/lessons/round-26/27/28-verifier-spotcheck.md`
(lesson files, not wave directories) and the round-28 report at the path my item names.

Tip identity: lane `HEAD` = `8a45cefe84af0557b457308e4e0f679ca490f9e9` (contract commit, which adds only
`.ufo/waves/round-29/`); `git rev-parse 7118f320` = `7118f320a5ef18d20c1e361eff77db0e1a97b2d6`. `SHONEN.md`,
`SKILL.md`, `LOG.md`, `PROVINCE.md` and `SCORECARD.md` are byte-identical between `7118f320` and the working tree
(sha256 equal for all five; e.g. `SKILL.md` `bab0440d60132fc06552aec6fb02f193235e02a063a0b4b8cb50b5a5c8360098`).

Lane position (context): axes 6/7/5/5/5/6 at `SCORECARD.md:10-15`; `corpus/SOURCES.md` holds 152 rows;
pinned fleet MANIFEST at `63729047` records mori rounds 12-28 as admitted except 13, 17, 20, 23, 27
(rejected-harmed ×3, rejected-honest-stop ×2).

## Box 1 — "SKILL.md contains real decision tables, error patterns, checklists, cited sources"

Observed, all at `7118f320`:

- Decision table `SKILL.md:11-21` (9 table lines = header + separator + 7 intent rows; columns Intent / Correct
  surface / Never / Expected output, concrete verdict tokens such as `WATCHDOG_STATE_LAG`, `MORI_CENSUS: CLEAN|DRIFT`).
- Further decision tables: lane-silence binding table `SKILL.md:428-470`; pressure `:621-634`; userspace OOM killers
  `:689-701`; OOM victim selection `:725-733`; harness job cap `:649-660`. Counting commands: `grep -c '^|' SKILL.md`
  → `133`; `grep -c '^|---' SKILL.md` → `15` (15 markdown tables, 133 table lines).
- Error patterns: `SKILL.md:23-45` (21 table lines = 19 reading rows), userspace OOM killers `:704-710` (5 lines),
  OOM victim selection `:736-741` (4 lines).
- Checklist: `SKILL.md:149-154`, four executable items (name the command and revision; `unavailable` not unhealthy;
  no remediation; stable id).
- Cited sources: 24 distinct `S###` ids in `SKILL.md`, every one present in `corpus/SOURCES.md` (152 rows; script
  printed `cited but absent: []`); 34 inline URLs; the knowledge entries cited by the r24-r27 sections all exist at
  the tip (`system-pressure-r24.md`, `harness-job-capacity-r25.md`, `userspace-oom-killers-r26.md`,
  `oom-victim-selection-r27.md`, `retention-reconciliation-r22.md`, ... verified with `git cat-file -e`).
- Gate registry rows carry entry, verdict map, self-test, pinned values, write scope, owner (`SKILL.md:156-205`,
  `:611-643`, `:712-718`).

Non-author verification on record is partial: `corpus/lessons/round-27-verifier-spotcheck.md:47` measured the
`Round27` section at `df886be1` as 15 table lines with 8 decision rows and 3 error-pattern rows; `:115` re-opened
S127 and located its quote; `corpus/lessons/round-28-verifier-spotcheck.md:103-107` re-opened S145, S147, S150 and
S152 with sha256 and verbatim located quotes. No verifier checked the `:11-45` tables, the four-item checklist, or
table-versus-tool conformance; the round-28 report says the same at `:91`.

Recommendation: **`[~]`**, pointer `SKILL.md:11-45` + `:149-154` + `:676-742` and
`corpus/lessons/round-28-verifier-spotcheck.md:103-107`. Content is real and sourced; what is missing is a named
non-author check of the tables/checklist themselves, which `[x]` requires.

## Box 2 — "At least one end-to-end domain task executed and logged in LOG.md"

Observed:

- `LOG.md:1838-1846` (round-26 outcome): the tool was built blind to 32 frozen cases written by another seat,
  `PASS 32/32`, then a live run printed `KILLERS_QUIET` and the previous boot held 38 SIGTERM and 1 SIGKILL earlyoom
  send lines. The live receipt exists at the tip: `.ufo/waves/round-26/evidence/c2-live-run.txt` (872 bytes).
- `LOG.md:1889-1890` (round-28 measured outcome): `Measured at 6b695b02: ... first tool run PASS 30/30 (exit 0),
  C2=met exit 0, tool unchanged`; receipt `.ufo/waves/round-28/evidence/c2-freeze-selftest.txt` exists.
- A third, older example with a measured number: `LOG.md:1060-1066` (round-16 window selftest `16/16`, context
  selftest 15 arms).

Non-author: `corpus/lessons/round-26-verifier-spotcheck.md:171-175` says boxes 1 and 2 "look checkable from
committed bytes by a non-author ... `LOG.md` round-26 outcome plus the committed live run" and explicitly "writes no
`[x]`"; `corpus/lessons/round-28-verifier-spotcheck.md:93` verifies the round-28 operability claim (ten A2 rules
pinned, PASS 30/30, tool unchanged).

Recommendation: **`[~]`**, pointer `LOG.md:1838-1846` + `.ufo/waves/round-26/evidence/c2-live-run.txt` (and
`LOG.md:1889-1890`). Substance is met in my reading; the only gap is that the non-author verifier calls it
"checkable" rather than checked, and the operator owns promotion. A verifier note saying "box 2 checked, met"
would support `[x]`.

## Box 3 — "Instructions executable by an agent without oral context"

Observed:

- I executed the primary documented entry from the lane root with no environment but a scratch `TMPDIR`
  (`TMPDIR=/fast/scratch/hyaku/mori-r29/ScoutShonen timeout 240 bash tools/mori-census.sh --selftest`,
  2026-10-22T19:59Z): `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)`, `exit=0` (17 s wall).
  This is an execution by an agent without oral context, and it matches the documented claim at `SKILL.md:159-163`
  and the scorecard's "census `--selftest` PASS (134 cases)" (`SCORECARD.md:11`).
- All 13 default input paths I extracted from the gate rows exist at `7118f320`: `.ufo/waves/round-18/frozen/c1-policy.json`,
  `.ufo/waves/round-14/frozen/mori-census.sh`, `.ufo/waves/round-15/{fixtures,expected.json}`,
  `.ufo/waves/round-16/{fixtures,expected.json}`, `.ufo/waves/round-17/fixtures/seat`,
  `.ufo/waves/round-19/frozen/content-population.json`, `corpus/evidence/baseline-r10-20261015T2231Z.json`,
  `corpus/evidence/retention-allowlist.json`, `.ufo/waves/round-18/frozen/c2-register.json`,
  `corpus/evidence/freeze-register.json`, `.ufo/waves/round-19/content-reviews.json` — 13/13 checked OK.
- Residual defects found: `SKILL.md:661` cites `contract.md:83-84` with no directory; it resolves only from the
  section context to `.ufo/waves/round-25/contract.md:83-85` (checked: scope bounds and the unreadable live count —
  the claim is accurate). `SKILL.md:717` cites wave-2 reports with a directory prefix then bare filenames
  (`.ufo/waves/round-25/w2/MutRoutedD1.md`, `MutRoutedD2.md`, ...), which resolves. `PROTOCOL.md:351-352` in
  `LOG.md:544` is a fleet-root file (`../PROTOCOL.md` exists). One "this round" phrase survives at `SKILL.md:532`
  inside the dated Round21 section.
- No non-author execution was on record before this run: `corpus/lessons/round-27-verifier-spotcheck.md:139-140`
  ("no non-author execution exists").

Recommendation: **`[~]`**, pointer: the run above plus `SKILL.md:156-205`. It flips to `[x]` when a named verifier
records two or more documented entries executed clean from the lane root, and `SKILL.md:661` names the round-25
contract directory.

## Box 4 — "No cross-domain bleed (PROVINCE.md still accurate)"

Bleed: none found in the sections that matter.

- `SKILL.md:678-683` states host/unit diagnosis and any killer tuning stay operator-owned (`PROVINCE.md:53`, FR10);
  `SKILL.md:666-675` refuses action on the harness cap and names kumitate and the operator; the refused action is
  also named at `PROVINCE.md:335`. The secret-exclusion practice (`SKILL.md:374-395`) is count-only and matches
  `PROVINCE.md:15`. Adjacency rows `PROVINCE.md:65-69`, `:357-371`, `:373-384` state the tsukuroi/operator
  boundaries, including that mori corrects tsukuroi's `+200 band first` model "without absorbing them".

PROVINCE accuracy defects observed at the tip (so "still accurate" is not fully true):

1. `PROVINCE.md:32` still says the journal window is "(round-16 build; verification pending)", while
   `LOG.md:1060-1066` records the window selftest `16/16` and the pinned MANIFEST records round 16 `admitted`.
2. "admission pending" survives at `PROVINCE.md:236` (round 24), `:294` (round 25), `:359` (round 26) and `:375`
   (round 27). At `63729047`, rounds 24, 25 and 26 are `admitted` and round 27 is `rejected-honest-stop` — none is
   pending.
3. `PROVINCE.md:68` cites `SKILL.md:49` for the kagi/credential boundary. At the tip `SKILL.md:49-51` is the r15
   mixed-class alarm prose; the actual secret rule is `SKILL.md:374-395`.
4. `PROVINCE.md:66` cites `../tsukuroi-shokunin/PROVINCE.md:21-24,35-44` for tsukuroi's ownership. Tsukuroi's owns
   statement is at `tsukuroi-shokunin/PROVINCE.md:3-14`; `:21-24` are surface-table rows (Arch News, pacnew) and
   `:35-44` is refuses/adjacent. The claim is true; the pointers are wrong.
5. The top Frontier list `PROVINCE.md:44-57` runs FR1-FR14; FR15 exists only inside the round-25 appended note at
   `:321`. Likewise the Core list `:20-34` names six surfaces while four later Core additions live only in appended
   notes (`:236`, `:294`, `:359`, `:375`) — disclosed per round, but the head of the file no longer states the full
   Core.

Recommendation: **`[~]`**, pointer: "no bleed; fix the five stale pointers above". A strict reading of "PROVINCE.md
still accurate" would leave `[ ]` until they are fixed. `[x]` is not available: no non-author accuracy audit exists
(the round-28 spotcheck's adjacency line is "unchanged, held, no claim", `corpus/lessons/round-28-verifier-spotcheck.md:97`).

## Mismatches between `SHONEN.md` and the round-28 report's SHONEN lines

1. Status divergence: `SHONEN.md:5-8` carries four bare `[ ]`; `/home/vgpnk/Projects/shokunin/.ufo/reports/round-28/mori.md:91-94`
   carries `[ ]`, `[~]`, `[ ]`, `[~]`. Boxes 2 and 4 disagree between the checklist and the report.
2. The checklist is unmaintained: `SHONEN.md` was last changed by `1f07f1d` (round 12, 2026-10-19). Sixteen rounds
   (13-28) have not touched it; every status mark lives only in a round report, so no status is durable at the tip.
3. The report's box-1 line adds "(not verified by a non-author this round)" (`report:91`); `SHONEN.md:5` has no such
   qualifier, so the checklist overstates what is known when read alone.
4. The report's box-4 evidence (`report:94`, wave-1 ConnSiblingOverlap, "no shared rows; S151/S145/S152 scope notes")
   speaks to SOURCES-row overlap, not to `PROVINCE.md` accuracy, which `SHONEN.md:8` requires. The accuracy half is
   unaddressed by that line, and I found five stale points (above). I could not re-check ConnSiblingOverlap because
   that round-28 wave file is outside my blindness allowance.
5. The report's box-2 pointer omits its wave prefix (`report:92`, `evidence/c2-freeze-selftest.txt`); it resolves to
   `.ufo/waves/round-28/evidence/c2-freeze-selftest.txt`, which exists, but it is the round-28 fixture receipt, not
   the round-26 live-run receipt at `.ufo/waves/round-26/evidence/c2-live-run.txt`.
6. The round-28 verifier's own summary is consistent with my findings: "two boxes `[~]`, two `[ ]`; not fully
   checkable by a non-author this round (no promotion note)"
   (`corpus/lessons/round-28-verifier-spotcheck.md:135`).

## Ready-to-paste (replaces `SHONEN.md:5-8`)

```md
- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — `SKILL.md:11-45`,
      `:149-154`, 15 tables, 24 of 152 SOURCES rows cited, all resolving; sources partly re-opened by non-authors
      (`corpus/lessons/round-27-verifier-spotcheck.md:47,115`; `round-28-verifier-spotcheck.md:103-107`); tables and
      the checklist themselves not yet non-author checked (round-28 report:91)
- [~] At least one end-to-end domain task executed and logged in LOG.md — `LOG.md:1838-1846` (blind 32-case build,
      PASS 32/32, live `KILLERS_QUIET`) with `.ufo/waves/round-26/evidence/c2-live-run.txt`; `LOG.md:1889-1890`
      (PASS 30/30 at `6b695b02`); verifier calls it "checkable", not checked (`round-26-verifier-spotcheck.md:171-175`)
- [~] Instructions executable by an agent without oral context — measured: `bash tools/mori-census.sh --selftest`
      from the lane root, PASS 134/134, exit 0, 2026-10-22T19:59Z; 13/13 sampled default input paths exist;
      one unqualified pointer `SKILL.md:661` (`contract.md:83-84` → `.ufo/waves/round-25/contract.md:83-85`);
      no non-author execution before this one (`round-27-verifier-spotcheck.md:139-140`)
- [~] No cross-domain bleed (PROVINCE.md still accurate) — no bleed found (`SKILL.md:374-395`, `:666-683`;
      `PROVINCE.md:65-69`, `:357-384`); accuracy stale at `PROVINCE.md:32` ("verification pending"), `:236/:294/:359/:375`
      ("admission pending" for admitted 24/25/26 and rejected 27), `:68` (dead `SKILL.md:49` cite), `:66` (mispointed
      tsukuroi range; owns statement is `tsukuroi-shokunin/PROVINCE.md:3-14`), and `:44-57` omits FR15 (at `:321`)
```

## Remaining unknowns

- Whether the operator considers a closure MANIFEST verdict (`round-26 admitted`) equivalent to a named verifier for
  box 2. I did not treat it as one; the verifier documents themselves decline to write `[x]`
  (`round-26-verifier-spotcheck.md:175`).
- The round-28 ConnSiblingOverlap report's reasoning is outside my blindness allowance; I checked bleed directly
  against `SKILL.md` and `PROVINCE.md` instead.
- I read `PROVINCE.md:1-92` and `:234-384`; the round-17/18/20/21/22/23 notes (`:92-233`) were skimmed only for
  round/harness/oomd/retention mentions, not line-audited.

Tooling: nothing installed or upgraded (pacman paused host-wide); one read-only selftest executed with `TMPDIR` in
`/fast/scratch/hyaku/mori-r29/ScoutShonen/`; no other writes.
