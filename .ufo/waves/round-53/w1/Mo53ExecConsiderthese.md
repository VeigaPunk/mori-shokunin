# Mo53ExecConsiderthese — round-52 critic flags carried forward (considerthese/2026-10-26.md, suggestion 2)

Seat: Mo53ExecConsiderthese (executor, round-53 wave w1). Derived-only: every disposition below is read from
committed bytes; nothing outside this report was written.

Reference tip: `20edafa59b38dac1ca358893f0259b1f436372d3` (round-52 closure = entering tip of round 53), as the
assignment fixes it. Window of "fixed": `git -C <lane> log --oneline 4f266ef2..20edafa5` = seven commits
(`d3a8ea59` freeze, `8524904a` data, `075436b1` w1 spec, `2f245af7` integration, `e7e056b8` wave close,
`37af57f2` receipts-at-landed, `20edafa5` closure). Round-53 work is reported separately (§5–§7) because it
lands after the reference tip (`f4da3fd4`, `2a4213bf`, `95cf78ee`) and is not part of the ledger's accounting.

## 1. Method and the route inventory used for "routed"

A flag counts as:

- **fixed** — a commit in `4f266ef2..20edafa5` changed committed bytes so the flagged defect no longer holds at
  `20edafa5`; evidence is the commit plus the before/after bytes.
- **routed** — the flag or its subject is named in a forward-looking lane artifact that exists at `20edafa5`:
  SCORECARD `Planned (round 53)` (`SCORECARD.md:2768-2771`), the round-52 lesson's `## Mistakes` M-rows and
  `## Round-51 closure routed defects (§5) — dispositions`, or the round-52 closure's `## Routed defects for the
  lane's next round` (`corpus/lessons/round-52-verifier-spotcheck.md:122-132`). Route target quoted per row.
- **dropped** — no commit fixes it and no route names it. Two sub-cases are marked in the evidence column:
  "(recorded limit only)" = named in the round-52 lesson/SCORECARD as a limit of a frozen instrument, but with no
  planned line and no owner, so it is not scheduled anywhere; and plain silence.

The four route sources, quoted once here:

- `SCORECARD.md:2768-2771` — "Planned (round 53): the in-lane writers' successor freeze (round-38/39/41/42
  `conform.py`, round-48/49 `count-c1.py`); the locator sweep beyond the Axes rows; the C1 arm-isolating controls
  for M4/M8 and the receipt/closure trust gaps; a commit-ledger census line (CommitLimit/Committed_AS) and a
  mode-2 error band; the PROVINCE/SCORECARD present-tense tally pins (K4 scope)."
- Round-52 lesson `## Mistakes` M1–M5 (each with a `fix:`), `## Wave w1 — integrated findings`, and
  `## Round-51 closure routed defects (§5) — dispositions` items 1–8 (`item 8`: "successor-freeze design routed
  to round 53").
- Closure `## Routed defects for the lane's next round` 1–3: SCORECARD correction (at-data vs at-landed tally);
  report self-citation; standing limits (locator arm scope, pure-text receipts, arm-A `admitted` pin).
- The round-53 contract's own `Round-52 closure routed defects` section (`f4da3fd4`) re-routes those three
  standing limits to a `Planned (round 54)` line.

Keyword test used to avoid false "routed" calls: each dropped row was grepped in the lesson, the SCORECARD
round-52 section and the round-53 contract. Terms that occur zero times in all three — `hidden_rows`, `stray`,
`R11`, `blinding`, `S490`, `no L1`, `source-drift`, `PASS 4 cases`, `QUALITY 115`, `QUALITY 122`, `receipt
corpus` — mark rows that no route names.

Commands (literal, run from `/fast/scratch/hyaku/mori-r53/Mo53ExecConsiderthese` unless absolute):

```
git -C <lane> log --oneline 4f266ef2..20edafa59b38dac1ca358893f0259b1f436372d3
git -C <lane> show 20edafa5:SCORECARD.md | sed -n '2737,2790p'
git -C <lane> show 20edafa5:corpus/lessons/round-52.md
git -C <lane> show 20edafa5:corpus/lessons/round-52-verifier-spotcheck.md | sed -n '122,132p'
git -C <lane> show f4da3fd4:.ufo/waves/round-53/contract.md
grep -cE '^\s*[-*]?\s*\**(HIGH|MED)\b' <wave>/*.md          # 97 bullet lines
grep -nE '\|\s*(HIGH|MED)\s*\|' <wave>/*.md                  # 5 table rows
git -C <lane> diff 8524904a 2f245af7 -- corpus/SOURCES.md corpus/knowledge/overcommit-commit-limit-r52.md \
                                               corpus/QUALITY.md SHONEN.md corpus/README.md
cd <lane-archive-at-20edafa5> && python3 tools/mori-source-drift.py --selftest   # PASS (6 cases)
```

## 2. Inventory of what the round-52 wave actually raised

`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-52/w1/` holds 68 seat reports; 34 of them carry
severity-tagged lines: 102 HIGH/MED lines (97 bullet findings + 5 table-format findings — `Mo52CritC2Prose.md`
rows 1–2, `Mo52SentBoundary.md` F1/F2/F3). Four of the 97 are not defects and are excluded from the ledger:
`Mo52Ent09.md` "HIGH: none" and `Mo52ExecSourceRefetch.md`'s three "HIGH (verified…)" confirmations (frozen
copies byte-identical, 28/28 quotes present, tag v7.2 resolves). That leaves **98 genuine HIGH/MED entries**,
which collapse to **61 distinct flags** (the same defect is routinely raised by two to five seats; the ledger
lists every raising seat).

## 3. Carry-over ledger — every round-52 HIGH/MED flag, disposition at `20edafa5`

| id | sev | flag (condensed) | raising seats (finding #) | status at 20edafa5 | evidence |
|---|---|---|---|---|---|
| L01 | HIGH | the receipt arm reads pure text: a one-line hand-written receipt in `evidence/selftests/*.txt` satisfies it | CritC1Junk 1; ScribeLog 4 | ROUTED | `SCORECARD.md:2769-2770` "receipt/closure trust gaps"; closure §Routed 3; r53 contract re-routes to `Planned (round 54)` |
| L02 | HIGH | the newest closure file at R is trusted verbatim, so a fabricated closure sets every axis score | CritC1Junk 2; ScribeLog 4 | ROUTED | same line ("closure trust gaps") |
| L03 | HIGH | check_living accepts a supersede line whose replacement pin is not tied to the stale claim's subject | CritC1Junk 3; ScribeLog 4 | ROUTED | same line + `SCORECARD.md:2758-2767` limits paragraph names it |
| L04 | MED | 17 of 91 whole-file locators do not resolve lane-root-relative (SCORECARD 6, LOG 11) | ExecLocatorSweep 1 | ROUTED | `SCORECARD.md:2769` "the locator sweep beyond the Axes rows" |
| L05 | MED | three pointers name files that never existed (`PROTOCOL.md` ×2, `AXES.md`) | ExecLocatorSweep 2 | ROUTED | same |
| L06 | MED | the quote/pair arm reads backwards only: a quote written after its pointer is never checked | ExecLocatorSweep 3 | **DROPPED** | no fix; not named in lesson/SCORECARD-r52/contract |
| L07 | MED | a locator pointer may target a semantically unrelated line that happens to contain the string | CritC1Junk 4 | **DROPPED** | the planned locator item is scope-only; the semantics weakness is unnamed everywhere |
| L08 | MED | arm (D) scope: 78 backticked `path:N` pointers in QUALITY/README unread | ScribeScorecard 4 | ROUTED | `SCORECARD.md:2769`; closure §Routed 3 ("locator arm scope") |
| L09 | HIGH | "distinct voters" is distinct filenames; one judgment under two names counts twice | CritC2Voters 1 | **DROPPED** | (recorded limit only) lesson `## Wave w1`; `SCORECARD.md:2766-2767` "voter distinctness is by filename" |
| L10 | HIGH | authorship signalled only by a `REPLACE` line; an author's own `entailed` vote counts when it is absent/stale | ConnCrossClaim 2; CritC2Voters 3 | **DROPPED** | (recorded limit only) same sentence ("a REPLACE line is the only authorship signal") |
| L11 | HIGH | dissent is cleared by deleting the dissented row (kill-rule violation); dissent counted on survivors only | CritC2Voters 2 | **DROPPED** | (recorded limit only); not named in any planned line |
| L12 | MED | "unfenced" is a bare three-backtick/tilde toggle; 4-space-indented and tab-indented vote lines still count | CritC2Voters 4; RevC2Counter 2 | **DROPPED** | (recorded limit only); and the r53 counter keeps `^\s*RECHECK`/`^\s*QUOTE` plus the same toggle (`count-c1.py:80-81,102-103`) |
| L13 | MED | the docstring's "no L1 file counts" clause is unenforceable; voter identity is frozen-filename membership | RevC2Counter 1 | **DROPPED** | (recorded limit only); r53 C1 `VOTERS` list is filename membership too |
| L14 | MED | r52 C2 selftest has no arm for a mid-line `REPLACE` token or uppercase-hex vote hashes (mutants 7, 9) | MutC2Arm 1,2 | **DROPPED** | (recorded limit only) |
| L15 | HIGH | r51 counter arms A–D lack arm-isolating controls; the m1/m8 survivors admit no single-arm control | ExecR51ArmControls 1,2,3,4,5 | ROUTED | `SCORECARD.md:2769` "the C1 arm-isolating controls for M4/M8"; lesson `## Wave w1` "limits for round 53" |
| L16 | HIGH | `README.md:728` published a runnable pin whose frozen instrument hardcodes `LANE` and writes selftest fixtures into the real lane | MisrootSweep 1; MutC1Controls 1; ScribeLog 1; SentHostPaths 2; SentReceipts 3; PinCheckNoHarm 2; RevenStalePins 3; SentBoundary F1 | FIXED (pin) | `2f245af7`: README:728 now runs `.ufo/waves/round-52/r39-conform-selftest.sh` (clone + bwrap bind-mount); the frozen r38/r39 instruments still hardcode `LANE` → residual ROUTED by `SCORECARD.md:2768-2769` |
| L17 | HIGH | `lane_writes` samples `git status` once on a clone: transient/empty-dir writes invisible, sibling seat reports read as lane writes, 4-way concurrency flips the conform pin to rc=2 | ScribeLog 2; SentBoundary F2; SentHostPaths 3; RevenStalePins 3; MutC1Controls 2 | **DROPPED** | (recorded limit only) "`lane_writes` is a quiescent-tree instrument"; no planned line; r53 counters have no such arm |
| L18 | HIGH | round-40 `conform.py` diverges from `freeze-r40.txt` (`7f5174d5…` vs `5025b966…`); old bytes fail silently off-tree; no successor record | RevenRound40Conform 1,2; ConnCrossClaim 4; ScribeLog 6; ScoutMistakeSweep 2 | ROUTED (partial) | lesson M4 "fix: round-53 successor-freeze design (routed defect 8)" + §5 item 8; but `Planned (round 53)` enumerates round-38/39/41/42 and **omits round-40**; still divergent at tip |
| L19 | MED | QUALITY:115's rationale sentence is false at HEAD; needs an appended supersession naming `87e0c374` | RevenRound40Conform 3 | **DROPPED** | QUALITY 115 unchanged at tip (`QUALITY.md:938`); `87e0c374` appears only in round-51 criteria; term absent from lesson/SCORECARD/contract |
| L20 | MED | r48/r49 `count-c1.py` default `--scratch` to `<repo>/.scratch` (residue 2.2 MB / 4.6 MB, never removed); the round-51 in-lane inventory was not landed | ConnCrossClaim 3; ExecWritersCounters 1; ScoutMistakeSweep 4 | ROUTED (inventory fixed) | inventory landed `2f245af7` (`w1/Mo52ExecWritersConform.md`, `w1/Mo52ExecWritersCounters.md`); scratch default routed by `SCORECARD.md:2768-2769` (names round-48/49 `count-c1.py`); `round-49/count-c1.py:332` unchanged |
| L21 | MED | r49 `count-c1.py` is date-dependent on the measured document's tail and cannot be a standing gate at a later tip | ExecWritersCounters 3 | ROUTED | successor-freeze route (lesson §5 item 8; `SCORECARD.md:2768-2769`) |
| L22 | MED | `tools/mori-pin-check.py` `hidden_rows`: an HTML-comment pin after prose is invisible, gate reads `met` | ExecWritersCounters 2 | **DROPPED** | seat wrote "routed to round 53", but `hidden_rows` occurs 0 times in lesson/SCORECARD-r52/contract and the tool is unchanged `20edafa5..HEAD` |
| L23 | MED | eight tracked lane-root strays (`0`, `MANPAGE.md`, `base.c`, `main.c`, `meminfo.c`, `oom_kill.c`, `sd-main.c`, `user@.service.in`) | ExecMisrootSweep 3 | **DROPPED** | all eight still in the tree at `20edafa5` and at `HEAD 95cf78ee`; no route names them |
| L24 | MED | empty-directory lane writes are invisible to a porcelain sweep | ExecMisrootSweep 2 | **DROPPED** | no route |
| L25 | HIGH | r52 `controls/c1-controls.py` fixes the fleet root, returns 0 on failure, and writes receipts into its own `evidence/` with no `--out` (defect-6 class) | SentHostPaths 1,4; SentBoundary F3 | **DROPPED** | r52 file frozen/unchanged; and the r53 builder repeats it (`round-53/controls/controls.py:78` writes `W/evidence`, no `--out`) |
| L26 | MED | the wave spec's cited round-51 baseline line (`PIN_CHECK=met tally_pins=36`) is not in the receipt it cites | PinCheckNoHarm 1 | **DROPPED** | round-52 spec text artifact; no route |
| L27 | MED | `git ls-remote https://github.com/torvalds/linux` did not complete on this host (rc=124 at 100 s and 60 s) | SourceRefetch 4 | N/A (environment) | not a lane defect; closure re-fetched via API + blob ids; the r53 contract routes GitHub raw around via git.kernel.org cgit (429 note) |
| L28 | HIGH | `corpus/SOURCES.md` rows S490/S491/S492 were rewritten in place after first sighting; the append-only gate lists them (`appendonly_violations=21`, exit 1 at the data tip) | ConnCrossClaim 1 | **DROPPED** | no superseding row at `20edafa5` or `HEAD` (`supersedes S49` count = 0, three rows still present); term `S490` absent from lesson/SCORECARD/contract; no script under the fleet `scripts/` invokes the gate |
| L29 | HIGH | `SCORECARD.md:1070-1071` present-tense tally ("Existing census125/125, oracle28/28, r13 24/24 …") outside every arm, stale since round 17 | CritC1Scope 1 | ROUTED | `SCORECARD.md:2770-2771` "PROVINCE/SCORECARD present-tense tally pins (K4 scope)"; text still present at tip |
| L30 | HIGH | `README.md:607-608` living pins are dated records; K4's file-role dichotomy is not the actual basis | CritC1Scope 2 | ROUTED (design) | same K4-scope line; the two pins already carry dated supersession notes (`README.md:722-733`, `8524904a`), so what remains is the criterion, which is unamended |
| L31 | MED | `PROVINCE.md:280-283` and `:350-355` carry present-tense instrument tallies (12/12, 21/21) no arm reads | CritC1Scope 3 | ROUTED | same; still present at tip |
| L32 | MED | the r52 contract says `CommitLimit`/`Committed_AS` "are undefined in the lane", overstating the sweep; the sweep-scope limit was to be recorded | CritC2Coverage 1 | **DROPPED** | r52 contract frozen and unamended; no erratum; limit unrecorded (the r53 contract's own wording is accurate, but that is outside the window) |
| L33 | MED | entry row 3 asserts the mode-2 failure unconditionally, dropping "in most situations" / "Depending on the amount you use" | Ent01 1; Ent02 2; Ent03 1 | FIXED | `2f245af7`: row 3 → "The documentation says that under mode 2, in most situations, …", new hash `3c2512af8468`, re-voted by Ent02/03/04 |
| L34 | MED | entry rows 27/28 conflate `SZ_128K`/`SZ_8K` bytes with kB (effective 128 MiB / 8 MiB) | Ent10 1; Ent12 1 | FIXED | `2f245af7`: rows → "the byte constant SZ_128K - 128 KiB, while the documented default is 128 MiB" (`10ac5a250ac2`, `1cadeed9914b`); S501 scope cell updated |
| L35 | MED | kernel docs (min(3 % of process size)) and code (`free_kbytes / 32`) disagree on the reserve default's first operand | Ent10 2 | **DROPPED** | not recorded at tip anywhere |
| L36 | MED | row 1's "refuses only allocations that are plainly too large" infers "only" | Ent02 1 | **DROPPED** | voter judged entailed; row text unchanged at tip |
| L37 | MED | row 5's "still charged against the commit limit" is universal while S501 keeps a hugetlb carve-out | Ent02 3 | **DROPPED** | claim row unchanged; the carve-out lives only in Boundaries |
| L38 | MED | row 13 omits the quote's "under the default overcommit 'guess' mode" and adds "when memory runs short" | Ent06 1 | **DROPPED** | seat-level watch item; row 13 unchanged; no lane route |
| L39 | MED | row 18's "fast approximate read" is a gloss, not a source word | Ent07 1 | **DROPPED** | voter judged entailed; row 18 unchanged |
| L40 | MED | entry Boundaries asserts a batch-size bound no copy contains; reading-rules row 2 makes an unsourced `MemAvailable` ordering claim | ScribeLog 9; CritC2Prose 1,2 | FIXED | `2f245af7`: bound labelled own-work host check (3.78 MiB mode 2 / 121.0 MiB loose); reading-rules row 2 → "independently of how much MemAvailable reports" |
| L41 | MED | SOURCES anchor cells wrong for S497 (45→48, 83-84→83-85) and S499 (`901-1006` overrun) | ScribeLog 8 | FIXED | `2f245af7` SOURCES diff: S497 `7-29,33-38,48,54-64,83-85`; S499 `781-786,806-840,901-1003`; S501 `546-558,1579-1619` |
| L42 | MED | QUALITY 141 cites "(QUALITY 128)" for a fact in QUALITY 123; 141/142 lack the house `Lesson:` citation | RevQualityRows 1,2 | FIXED | `2f245af7`: now "(QUALITY 123)" and "Lesson: round-52 M1 / M2 …" |
| L43 | MED | QUALITY 140's "Not covered" text still says one vote / any `.md` / fenced lines count | ScoutMistakeSweep 1 | FIXED | `2f245af7` QUALITY 143 supersedes 140's "Not covered" text only |
| L44 | MED | round-51 erratum absent: S493 locators drift and the famzah attribution are wrong | ScoutMistakeSweep 5; ScribeErratum51 1,2 | FIXED | `corpus/lessons/round-51-erratum.md` landed `2f245af7` |
| L45 | MED | QUALITY:909 `pass=12` pin and `README.md:608` dated-record pin sat stale 2 d 19 h / 12 rounds | RevenStalePins 1,2 | FIXED | `8524904a`: QUALITY 141 supersedes 112's check cell; README `## Round-52 corrections` 722-733 |
| L46 | HIGH | C2 row 3 contested: two distinct replacement texts for one hash, so "which replacement the counter takes" was undecided | ScribeLog 3 | FIXED | `2f245af7`: row 3 replaced once (`3c2512af8468`) and re-voted by three non-author voters; `c2-at-landed` `entailed=28 dissent=0` |
| L47 | MED | arm (C) enumerates fewer pins than the contract's "every single-line pin" claim: `README.md:579` pins `PASS 4 cases` (tool prints 6), `:580` pins `Self-test PASS 8 cases`, `SCORECARD.md:2209,2238` | ScribeLog 5 | **DROPPED** | verified at tip: `tools/mori-source-drift.py --selftest` → `PASS (6 cases)`, README:579 still `PASS 4 cases`; both terms absent from every route source; README unchanged to HEAD |
| L48 | MED | the three at-data receipts are not in the data commit (they land in the spec/dispatch commit) | SentReceipts 1; ScribeLog 7; SentBoundary F5 | **DROPPED** | not fixed, not routed; **recurs** in r53 (§6) |
| L49 | MED | the m2-history-rows receipt and its instrument were untracked (receipt not reproducible from committed bytes) | SentReceipts 2 | FIXED | `2f245af7` committed `.ufo/waves/round-52/check-history-rows.py` and `evidence/m2-history-rows.txt` |
| L50 | MED | the C1 witness receipt reproduced 4 of 5 times (one `no_tally_rc=2`); the counter captures but never prints the failing output | SentReceipts 4 | **DROPPED** | no route; the shared-scratch mechanism went away with the wrapper, the diagnosability gap is recorded nowhere |
| L51 | MED | `SCORECARD.md:2701` round-50 "Planned (round 51)" paragraph pins two producers that no longer exist in that form | ScribeScorecard 3 | FIXED (convention) | `SCORECARD.md:2768-2771` names live producers; the dated paragraph stays unedited by the append-only rule |
| L52 | MED | the round-52 After cells must not report the data commit as the landed tip — they quote 42/27 while citing `c1-at-landed.txt` | ScribeScorecard 1 | ROUTED | closure §Routed 1 + r53 contract §routed 1 ("an appended correction line … this round"); still uncorrected at `20edafa5` **and** at `HEAD` (`SCORECARD.md:2746` unchanged: `items=42 … locators=27` vs receipt `items=43 … locators=28`) |
| L53 | MED | `SHONEN.md:7` pins cited round-51 receipt paths while the counter reads round-52 selftests | ScribeScorecard 2 | FIXED | `2f245af7` SHONEN diff: now cites `.ufo/waves/round-52/evidence/selftests/…` |
| L54 | MED | no lane instrument read `CommitLimit`/`Committed_AS`/`overcommit_memory` (G1); the new entry had no instrument behind it | ScoutRunwaySurfaces 1; ScribeReadme 2 | ROUTED | `SCORECARD.md:2770` "a commit-ledger census line (CommitLimit/Committed_AS) and a mode-2 error band"; executed in r53 (§5) |
| L55 | MED | swap (`SwapTotal`/`SwapFree`) unread by any tool (G2) | ScoutRunwaySurfaces 2 | **DROPPED** | no route; r53's tool requires `SwapTotal` but exposes no paired swap figure (post-window partial pickup only) |
| L56 | MED | host PSI and slice PSI have no joint report or two-sample delta (G3) | ScoutRunwaySurfaces 3 | **DROPPED** | no route |
| L57 | MED | the census 10 % floor and the dispatcher 6144 MB floor are unlabelled and unreconciled (G4) | ScoutRunwaySurfaces 4 | **DROPPED** | no route |
| L58 | MED | `README.md:348` FR8 `first evidence` cell still names only `audit-r11.md:205` | ScribeReadme 1 | ROUTED (frontier) | FR8 stays open by design (r52 entry Boundaries; r53 contract keeps FR8 open); frontier rows are append-only |
| L59 | MED | the SCORECARD operability cell names round-47 as "latest admitted closure" while round-51 is later and admitted | RevAxesCells 1 | ROUTED (adjacent) | K4-scope line (`SCORECARD.md:2770-2771`); the false superlative itself is unnamed and still present at tip |
| L60 | MED | QUALITY 122's discharge-self fix is admission-only; the narrower receipt corpus is unbuilt and no tool enforces it | ConnCrossClaim 5 | **DROPPED** | QUALITY 122 itself says "the proposal itself is not implemented and stays open" / "Not covered: the narrower corpus is not yet built"; `QUALITY 122`/`receipt corpus` absent from every route source |
| L61 | MED | no QUALITY criterion forbids editing a frozen file in place (only the contract and a closure say it) | ScoutMistakeSweep 2 | ROUTED | lesson M4 "fix: round-53 successor-freeze design (routed defect 8) and a QUALITY criterion candidate"; the criterion is still absent at tip (QUALITY ends at 143) |
| L62 | MED | the R11 carve-out and the "blinding handle is random" rule have been routed since round 49 with no row | ScoutMistakeSweep 3 | **DROPPED** | absent from QUALITY, the r52 lesson, `Planned (round 53)` and the r53 contract |

## 4. Counts

| bucket | distinct flags | share |
|---|---|---|
| flagged | **61** | 100 % |
| fixed (commit `≤ 20edafa5`) | **13** | 21 % |
| routed (named forward route) | **18** | 30 % |
| dropped (no fix, no route) | **30** | 49 % |

Plus one environment observation (L27) that is not a lane defect. Raw-entry accounting: 102 HIGH/MED lines in
34 wave reports → 98 genuine entries (4 are "no defect"/"none" lines) → 61 distinct flags.

Of the 30 dropped, 8 are recorded *somewhere* as a limit with no owner — seven in the round-52 lesson/SCORECARD
as limits of the frozen counters (L09–L14, L17) and one inside the rule itself (`QUALITY 122` "Not covered: the
narrower corpus is not yet built", L60) — and 22 are silent, including two HIGHs a gate would catch today (L28
registry append-only, L22 pin-check `hidden_rows`).

## 5. Routed items round 53 then actually took up (observed after the reference tip)

These are not in the ledger's accounting (they land after `20edafa5`) but they are the only proof that the
routing worked:

- **L54 → done.** `Planned (round 53)` promised "a commit-ledger census line (CommitLimit/Committed_AS) and a
  mode-2 error band". The r53 data commit `2a4213bf` lands `tools/mori-commit-runway.py` (316 lines), its
  fixture file (754 lines), the `SKILL.md` Round53 registry row and `corpus/knowledge/commit-runway-read-r53.md`
  (rows S511–S513). That is the planned line, executed.
- **L55 → partial.** The same tool requires `SwapTotal` (`MEMINFO_REQUIRED` includes it) and computes the mode-0
  single-request cap from RAM+swap, but exposes no paired swap figure, so G2's actual complaint stands.
- Nothing else in the 62 rows shows post-tip movement: `SCORECARD.md`, `PROVINCE.md`, `corpus/README.md`,
  `corpus/QUALITY.md`, `LOG.md` and `tools/mori-pin-check.py` are byte-unchanged between `20edafa5` and
  `95cf78ee` (`git diff --name-only 20edafa5..95cf78ee -- <those paths>` prints nothing).

## 6. Dropped flags that recur in round 53 (evidence the drop was not harmless)

- **L48 (at-data receipts outside the data commit) — repeated.** r53's `evidence/c1-at-data.txt` is absent from
  both the freeze `f4da3fd4` and the data commit `2a4213bf` (`git ls-tree` → 0 rows for each) and present only
  at the wave-spec commit `95cf78ee`. The r53 contract nevertheless cites it as the C1 reading path.
- **L25 (controls receipts written into the lane, no `--out`) — repeated.** `round-53/controls/controls.py:78`
  writes `W/evidence/control-<claim>-<name>.txt` where `W = .ufo/waves/round-53`, i.e. the frozen control
  receipts' own paths, and the builder has no `--out` option. One unqualified run rewrites the freeze receipts.
- **L12/L13 (filename-keyed voter identity, `^\s*` vote lines, three-backtick/tilde toggle) — inherited.** The r53 C1
  counter keeps `RECHECK_RE = ^\s*RECHECK\s+<hex>\s+(holds|changed)` and `QUOTE_RE = ^\s*QUOTE …`, and the same
  fence toggle at `count-c1.py:80-81,102-103`. It does add one new authorship signal (a `QUOTE <h> :: <text>`
  line disqualifies a voter for that row), which addresses L10's class in the new instrument while leaving the
  r52 counter's weakness untouched.
- **L28 (SOURCES S490–S492 in-place rewrite) — still open.** Three rows present, no `supersedes S49x` row, and
  no fleet script runs `tools/mori-sources-appendonly.py`.
- **L47 (stale `PASS 4 cases` pin) — still open.** `tools/mori-source-drift.py --selftest` prints
  `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)` at `20edafa5`; `README.md:579` still says `PASS 4 cases`.
- **L23 (lane-root strays) — still open.** All eight files are in `git ls-tree 95cf78ee`.
- **L22 (pin-check `hidden_rows`) — still open.** `git log 20edafa5..HEAD -- tools/mori-pin-check.py` is empty.

## 7. Route defects in the carry-over machinery itself

1. **A promised route target does not exist.** The r53 contract says the three standing limits "→ carried in
   `Planned (round 54)`", but `SCORECARD.md` has no `Planned (round 54)` paragraph at `20edafa5` or at `HEAD`
   (`grep -c "Planned (round 54)"` → 0); the only one is `Planned (round 53)` at :2768. The closure, for its
   part, says the lane "already carries these in `Planned (round 53)`". Two committed documents disagree about
   where three standing limits live, and neither is fully right at the tip.
2. **The successor-freeze plan omits round-40.** `Planned (round 53)` enumerates "round-38/39/41/42
   `conform.py`, round-48/49 `count-c1.py`". The one conform.py the wave proved divergent from its own freeze
   record is round-40 (L18, HIGH). It is routed only through lesson M4's prose, not through the plan line a
   reader would consult.
3. **Seat-level "routed" claims without a lane route.** `Mo52ExecWritersCounters.md` (L22) wrote "routed to
   round 53 as a counter defect" in its own prose; the phrase appears in no lane artifact and the tool is
   unchanged. A seat's routing sentence is not a route.
4. **Body count vs plan capacity.** Of the 61 flags, the five `Planned (round 53)` items cover 14 of the 18
   routed rows; the other four route through the round-52 lesson (L18, L61), the closure (L52) or the FR8
   frontier row (L58). The 30 dropped rows would each need a plan line or an explicit "won't fix" record, and
   the lane carries neither.

## 8. Draft lesson section (fenced; for `corpus/lessons/round-53.md`, L1 to land)

```markdown
## Wave w1 — considerthese item: round-52 critic flags carried forward

Source: `considerthese/2026-10-26.md` suggestion 2; seat `w1/Mo53ExecConsiderthese.md`; reference tip
`20edafa5` (round-52 closure), window `4f266ef2..20edafa5`.

Inventory: 34 of 68 round-52 w1 reports carry HIGH/MED lines — 102 lines (97 bullets + 5 table rows), 98
genuine entries after removing four "no defect"/"none" lines — which collapse to 61 distinct flags.

Disposition at `20edafa5`: **13 fixed** by the round-52 landing (S497/S499/S501 anchors, entry rows 3/27/28
and the Boundaries/reading-rules prose, QUALITY 141/142/143, the round-51 erratum, the two stale living pins,
SHONEN pin paths, the at-data instrument commit, the README:728 hermetic wrapper); **18 routed** (five
`Planned (round 53)` items, lesson M4/§5, closure §Routed 1–3); **30 dropped**, of which 8 were recorded somewhere
with no owner and 22 were silent — including the SOURCES S490–S492 in-place rewrite (HIGH)
and the `mori-pin-check.py hidden_rows` blindness (MED).

Three route defects: the r53 contract routes three standing limits to a `Planned (round 54)` line that does not
exist in `SCORECARD.md`; `Planned (round 53)`'s successor-freeze list omits round-40 `conform.py`, the one the
wave proved divergent; and two seats' "route to round 53" sentences (the pin-check `hidden_rows` clause and the C2 docstring clause) have no lane artifact behind them.

Two dropped flags repeated in round 53 and can be checked: the at-data receipt is again outside the data commit
(`c1-at-data.txt` only at the wave-spec commit `95cf78ee`), and the new controls builder again writes receipts
into the lane's own `evidence/` with no `--out` (`round-53/controls/controls.py:78`). Two old counter
weaknesses were inherited verbatim by the new C1 counter (filename-keyed voter identity; `^\s*` vote lines with
a bare three-backtick/tilde fence toggle).

Lesson: a flag that is neither fixed nor named in a planned line is not "known" — it is unscheduled. Before a
wave closes, the L1 should reconcile the wave's HIGH/MED list against the next round's `Planned` paragraph and
either route each flag or record a "won't fix" with a reason; carry a count (`flagged / fixed / routed /
dropped`) in the round section so the drop rate is visible.
```

## 9. Limits of this ledger

- "Routed" is judged on artifacts that exist at `20edafa5`; a flag routed only in a seat's own report is counted
  dropped, which is deliberate but makes two seats' self-routing look worse than their prose (L22 from `Mo52ExecWritersCounters.md`, L13 from `Mo52RevC2Counter.md`).
- "Fixed" means the bytes changed so the flagged defect no longer holds; it does not mean the fix was verified
  by a closure. Three of the thirteen (L16, L33/L34, L40) were re-voted or re-attested in the same round, which
  the ledger does not re-audit.
- Classification of the six duplicated findings (row 3, rows 27/28, entry prose, stale pins, `lane_writes`,
  conform.py) into one flag per defect is a judgement; a per-finding redaction would raise the flagged count to
  98 and keep the same fixed/routed/dropped ratios within one point.
- I did not run the round-52 frozen counters at `20edafa5` (they write scratch and the assignment forbids
  re-running checks); every counter claim above is read from committed receipts or from the 3.78 MiB / 121.0 MiB
  host figures the round-52 entry already carries.

## Tooling and scratch

- Tools installed or upgraded: **none**. Commands used: `git` (read-only: log/show/diff/ls-tree/clone
  `--shared`), `python3` (three-line parsers over the wave reports), `grep`/`awk` via the shell.
- Scratch `/fast/scratch/hyaku/mori-r53/Mo53ExecConsiderthese/`: one `git archive` of the tip (`lane/`), one
  `git clone --shared` (`lane-clone/`, verified `rev-parse --show-toplevel` = the clone), the parsed inventory,
  all under `TMPDIR=…/tmp`. Removed before this report was closed; nothing cited above lives only in scratch —
  every claim is a commit hash or a path in the lane.
- No pacman, no network fetch, no write outside this report.
- The lane working tree was already dirty when this seat ran and I did not touch those paths: `PROVINCE.md`,
  `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md` (S502–S514 anchor/wording refinements, incl. a
  new S514 row) and `corpus/knowledge/kernel-v7.3-recheck-r53.md` are modified by another live seat or the L1
  (`git status --porcelain`; `git diff --stat` 5 files, +194/−15). Every disposition above reads committed bytes
  at `20edafa5` or `HEAD 95cf78ee`, never that working tree.

Report: `.ufo/waves/round-53/w1/Mo53ExecConsiderthese.md`

## Findings

| # | severity | file / line it concerns | finding |
|---|---|---|---|
| 1 | HIGH | `corpus/SOURCES.md:269-271` (rows S490–S492) | The registry's append-only violation from rounds 50–51 was never repaired: no `supersedes S49x` row exists at `20edafa5` or `HEAD`, the term `S490` appears in no lesson, SCORECARD plan or contract, and no fleet script runs `tools/mori-sources-appendonly.py`. The wave's HIGH is silently dropped. |
| 2 | HIGH | `tools/mori-pin-check.py:316-345` | The `hidden_rows` blindness was written up as "routed to round 53" but is not in any lane route, and the tool is byte-unchanged `20edafa5..HEAD`. Silent drop, with the gate still reading `met` on a prose-adjacent HTML-comment pin. |
| 3 | HIGH | `.ufo/waves/round-53/controls/controls.py:78` | The defect the r52 wave raised against the controls builder — receipts written into the lane's own `evidence/` with no `--out` (defect-6 class) — was dropped and is re-created here: one unqualified run rewrites the frozen round-53 control receipts. |
| 4 | HIGH | `.ufo/waves/round-53/contract.md` (`Round-52 closure routed defects` item 3) vs `SCORECARD.md:2768-2771` | The contract routes three standing limits to a `Planned (round 54)` line that does not exist (`grep -c` → 0 at `20edafa5` and `HEAD`), while the closure says the same limits are carried in `Planned (round 53)`. The route target is missing or contradictory. |
| 5 | HIGH | `.ufo/waves/round-52/evidence/c1-at-data.txt`, `c2-at-data.txt`, `c2-hashes-at-data.txt` / `.ufo/waves/round-53/evidence/c1-at-data.txt` | Dropped in r52 and repeated in r53: the "at data" receipts are not in the data commit (r52 `8524904a`; r53 `2a4213bf`), landing only in the wave-spec commits (`075436b1`, `95cf78ee`). The r53 contract cites the missing path as the C1 reading. |
| 6 | MED | `SCORECARD.md:2768-2769` | `Planned (round 53)`'s successor-freeze enumeration is "round-38/39/41/42 `conform.py`, round-48/49 `count-c1.py`" and omits **round-40** `conform.py`, the one the wave proved divergent from `freeze-r40.txt` (HIGH, `w1/Mo52RevenRound40Conform.md`). Routed only through lesson M4 prose. |
| 7 | MED | `SCORECARD.md:2746` | Round-52 C1 After cell still carries `items=42 … locators=27` while citing `c1-at-landed.txt` (which prints `items=43 … locators=28`). Routed as closure defect 1 for "this round", but `SCORECARD.md` is byte-unchanged at `HEAD`, so the correction is still owed. |
| 8 | MED | `corpus/README.md:579` | The stale living pin survives: `tools/mori-source-drift.py --selftest` prints `PASS (6 cases)` at `20edafa5`, the README row still says `PASS 4 cases`, and neither `source-drift` nor `PASS 4 cases` appears in any route source. Same class for `:580` and `SCORECARD.md:2209,2238`. |
| 9 | MED | lane root: `0`, `MANPAGE.md`, `base.c`, `main.c`, `meminfo.c`, `oom_kill.c`, `sd-main.c`, `user@.service.in` | Eight tracked misroot strays remain at `20edafa5` and `HEAD`; the wave's MED asked for a successor-freeze relocation and no plan line names them. |
| 10 | MED | `.ufo/waves/round-53/count-c1.py:80-81,102-103` | Two r52 counter weaknesses were inherited unchanged by the new C1 counter — voter identity by frozen filename, and `^\s*` vote lines with a bare three-backtick/tilde fence toggle (also tabs/4-space indents count) — although both were flagged MED/HIGH in r52 and recorded only as limits. |
| 11 | MED | `corpus/QUALITY.md:938` (criterion 115) | The rationale sentence the wave showed false at HEAD is unchanged and no supersession row naming `87e0c374` was appended; `QUALITY 115` appears in no route source. Silent drop. |
| 12 | MED | `.ufo/waves/round-52/controls/c1-controls.py:54` (and r53 successor) | The builder's fleet-root derivation and always-0 exit were dropped; the r53 builder still returns 0 regardless of control verdicts and still derives `LANE` from its own path. |
| 13 | LOW | `corpus/lessons/round-52.md` `## Wave w1 — integrated findings` | The section records limits but carries no per-flag disposition and no counts; a reader cannot tell 30 flags were dropped. The draft lesson section in §8 supplies the missing shape. |
