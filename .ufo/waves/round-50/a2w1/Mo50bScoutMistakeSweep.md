# Mo50bScoutMistakeSweep — mistake sweep for the frontier step (round 50, attempt 2, wave a2w1)

Scope: every disagreement or routed defect in `corpus/lessons/round-45-verifier-spotcheck.md` … `round-49-verifier-spotcheck.md`
(+ each round's `## Mistakes` table, which the spot-checks feed) and every `round-*-erratum.md` from round 40.
Read-only: no clone, no fixture, no tool executed, nothing written under `/fast/scratch` (the dir I created was removed empty).
Landed tip read: `487941b9` (entering `7197160b`). All paths relative to `/home/vgpnk/Projects/shokunin/mori-shokunin`.

## 0. Inputs observed

- `ls corpus/lessons | grep -i erratum` → `round-37-erratum.md`, `round-39-erratum.md`. `find . -name '*erratum*' -not -path './.git/*' -not -path './.scratch/*'` adds only the copies under `.ufo/waves/round-4[23]/assimilation/validate/` and `.ufo/waves/round-23/evidence/tmpfs-source-provenance-erratum.json`.
  **There is no `round-*-erratum.md` from round 40 on.** Rounds 45–49 carry their errata inside the lesson (r48 `round-48.md:150-157`, `## Wave 2 … Errata to this lesson`; r47 `round-47.md` w2 `RevLesson.md` F1 note at `:74`) or inside the spot-check (r49 D-c). r37/r39 errata are covered in §3 only because they are the only erratum files that exist.
- `corpus/QUALITY.md`: criteria 1–133 (`grep -nE '^1[0-3][0-9]\. ' corpus/QUALITY.md | tail -3` → 131/132/133 headings at `:1124`, `:1140`, `:1159`). `corpus/CORPUS.md` does not exist in the lane; `CORPUS.md` and `PROTOCOL.md` are at the fleet root (`/home/vgpnk/Projects/shokunin/CORPUS.md:179` "A fix is shown able to fail before it counts").
- Round-50 lesson `corpus/lessons/round-50.md` is absent at `487941b9` (`ls corpus/lessons | grep 50` → empty), so nothing below is "captured" by a round-50 lesson yet; the only round-50 carriers are `contract.md` ("Round-49 closure routed defects … carriers", `:` section near the end) and the landed data/receipts.
- Live state at `487941b9`: `git status --porcelain | wc -l` → 9 (6 are `.ufo/waves/round-40/scratch/mori-conform-selftest-*`; the rest are this wave's own files); `ls -d .scratch/*/ | wc -l` → 187; `du -sh .scratch` → 26G; `git ls-files .scratch | wc -l` → 225 (tracked); `git status --porcelain --ignored | grep -c '^!! .scratch'` → 170. (The untracked round-40 count moved 10 → 6 between two of my reads: another seat or the host is deleting them; I did not touch them.)

## 1. The list — rounds 45–49 spot-checks and lesson Mistakes

Status: **CAPTURED** (pointer) = a QUALITY criterion, a tool, or a landed round-50 datum now fails/records it; **PARTIAL** = captured for one instance, a named hole remains; **OPEN** = nothing in QUALITY.md, lessons, tools or the round-50 data discharges it.

| id | round | defect (source line) | status | pointer / reason |
|---|---|---|---|---|
| S45-1 | 45 | SCORECARD carried no round-45 claim rows (`round-45-verifier-spotcheck.md:31`) | CAPTURED | `LOG.md:2665` (r46 added the rows); this round's C1 counts Axes cells against MANIFEST (`.ufo/waves/round-50/count-c1.py`, `contract.md` C1 P-C1 (a)) |
| S45-2 | 45 | freeze-manifest tally 29/29 vs 27 OK (`:33-37`) | CAPTURED | `LOG.md:2657` named correction; `round-46.md` M2; QUALITY 40 + 117 (`:1`/`:943`). Class recurs (see S49-3) |
| S45-3 | 45 | two residual executor seats outside the committed spec/dispatch (`:38-41`) | OPEN | no QUALITY criterion on dispatch-vs-spec seats (`grep -nEi 'residual' corpus/QUALITY.md` hits 15, 760, 793, 939 — none about seats); QUALITY 64 counts report presence only |
| S45-4 | 45 | four stale `SKILL.md` registry cells (`:184,190,191,194`), calibration harmed (`:50-68`) | CAPTURED | QUALITY 123 (`:1028`), 133 (`:1159`), `tools/mori-pin-check.py`; r46 re-pin verified `round-46-verifier-spotcheck.md:26-31`; this round's C1 pins 114/114, 17/17 (`evidence/selftests/`) |
| M3-45 | 45 | `--selftest` accepted inside another arg's `help=` string | PARTIAL | `tools/mori-gate-registry.py:292,332,436` (parser key / `case` pattern); selftest arms list (`grep -oE 'arm\("[a-z_0-9]+"'`) has `comment_only_selftest_rejected`, `escape_flag_*` but **no arm named for the help-string probe E4**. QUALITY 120 (`:983-997`) still says "Not covered … routed to round 46" — never amended |
| M4-45 | 45 | `selftest-flag=--help` escape | CAPTURED | `escape_flag_name_rejected`, `escape_flag_mention_rejected` arms (`tools/mori-gate-registry.py:660-661`) |
| M5-45 | 45 | named-parameter argv branch rejected (over-narrow) | PARTIAL | tool docstring `:292` ("a membership test against argv") suggests widening landed; no arm names E6 (named-parameter positive). UNVERIFIED by execution |
| M6-45 | 45 | v1 positive control encodes the defect | CAPTURED | `comment_only_selftest_rejected` arm (`:655`), QUALITY 120 shown-able-to-fail clause |
| M7-45 | 45 | wave item asserted two failed routes (429/bot wall) as fact | OPEN | `grep -nEi 'hypothesis\|route claim\|wave item' corpus/QUALITY.md` → no hit; no rule that a route claim in a wave item carries a receipt |
| M8-45 | 45 | draft renumber map collided with the round's own admitted id | CAPTURED (per-round practice only) | this round's `assimilation/{reg-ids,staged-ids,collisions}` + guard proof (`contract.md` "Frontier step, assimilation"); not a QUALITY criterion |
| M9-45 | 45 | quarantine item said "read the row in `SOURCES.md`" for ids it never held | CAPTURED | r48/r49 lessons carry the register-class wording (`round-48.md:77`, `round-49.md:139`); r50 contract quarantine slice names S244/S262/S268 as "register" rows |
| M10-45 | 45 | prose count not re-derived from its own grep ("two comments" vs 1) | CAPTURED, but recurs | QUALITY 117 (`:943`), 124 (`:1041`). Recurrences: r47 M3, r48 M7, r49 48-vs-47 (S49-3), r49 M5 (`pass=42`). No instrument reads lesson/LOG prose counts → class stays alive. OPEN as "prose count in a lesson/LOG not re-derived" |
| M11-45 | 45 | write-scope cells false under inherited `GIT_DIR`; selftests must scrub `GIT_*` | PARTIAL | `tools/mori-gate-registry.py:106-108` scrubs `GIT_*`. `tools/mori-pin-check.py:535` (`env = dict(os.environ, TMPDIR=…)`) and `tools/mori-unlanded-check.py:38` (`dict(os.environ, GIT_OPTIONAL_LOCKS="0")`) inherit the caller's `GIT_DIR`. `grep -nE 'GIT_' tools/mori-pin-check.py` → no hit. QUALITY 121 states the write-scope rule but its check (`write-scope-run.py`) is r45/instrument-specific. UNVERIFIED by execution |
| R45-r44ledger | 45 | make round-44 ledger admissible or supersede (routed 4) | CAPTURED | r45 `count-c1.py` (`round-45.md` M2 "observed fixed"); QUALITY 117 "Not covered … routed to round 45" text still stale (never amended) |
| S46-1 | 46 | frozen `count-repins.py` is a row-wide substring check; claim `unprovable` (`round-46-verifier-spotcheck.md:39`, routed 1) | CAPTURED | `round-46.md` M1; QUALITY 123, 125; `tools/mori-pin-check.py` (parses cells, re-measures live) |
| S46-2 | 46 | `rows=4` hard-coded constant (routed 2) | CAPTURED (by retirement) | counter is frozen r46; superseded by `mori-pin-check.py`; no further use. No explicit "retired" note found: `grep -rn 'count-repins' SKILL.md` not run — UNVERIFIED |
| S46-3 | 46 | `.scratch/` leftovers (`MutMissing/` etc.) (routed 3) | PARTIAL | see S48-1 |
| S47-1 | 47 | 53 untracked paths incl. late `w2/*` reports at tip; report's 79-seat accounting not what the repo held (`round-47-verifier-spotcheck.md:20,96`) | CAPTURED | `tools/mori-unlanded-check.py` (`UNLANDED_SELFTEST`), QUALITY 80 (`:368`), `round-48.md` M1; receipt `evidence/selftests/mori-unlanded-check.txt` |
| S47-2 | 47 | report filed after the driver's `complete` line (17:27:24 vs 17:25:39) (routed 2) | OPEN | `grep -nE 'complete' corpus/QUALITY.md` hits only criteria 26/33 (census); no criterion or tool reads report-vs-driver-complete time |
| S47-3 | 47 | successor `count-c2.py`: used-by arm, 0–3-space rows, one path per cell (routed 3) | CAPTURED | r50 `count-c2.py` P-C2 requires `used-by` to list the entry (contract P-C2); contract assimilation guard proof for 0–3-space rows; one-path-per-cell is the "source cell is one S-id" clause |
| S47-4 | 47 | v2 selftest arms: symlink containment, argv sub-checks, case-insensitive unparsed; truncated-digest pins; lesson F4 citation precision (routed 3) | CAPTURED (partly) | r48 v3 R6 (truncated digests) found the stale `SKILL.md:168` pin (`round-48.md` M4); r49 `Mo49ExecArmsHeader` arms (`SKILL.md:994`). Symlink containment arm: not found — UNVERIFIED |
| S47-5 | 47 | S478 IEEE refetch needs a browser UA, say so in `recheck` (routed 5) | CAPTURED | `corpus/SOURCES.md:257` (the S478 row matches `grep -nE 'User-Agent\|browser UA'`) |
| S47-6 | 47 | lesson `## Spot-check` said "no spot-check exists yet" (routed 4) | CAPTURED | `round-48.md:95`, `round-49.md:173-190` cite the spot-check |
| M4-47 | 47 | a seat edited the tracked `tools/mori-pin-check.py` instead of its scratch copy (survived into r48 M5) | PARTIAL | unlanded-check lists modified `tools/` files; frozen-sha256 compare; `round-48.md` M5 says "Not prevented: a seat can still edit and restore between two runs". Recurred r47 → r48; wave context "Write ONLY your own report file" is stated not enforced. OPEN as prevention |
| M5-47 | 47 | `count-c2.py` r47 survivors (used-by arm, indented rows, one path per cell) | CAPTURED | see S47-3; QUALITY 114 (`:927`) requires survivors to enter a committed fixture — **PARTIAL in practice**: r47 survivors were "Not fixed: the counter is frozen", no fixture committed (check `ls .ufo/waves/round-47/fixtures` — not run, UNVERIFIED) |
| S48-1 | 48 | 114 untracked `.scratch/*` dirs; `mori-unlanded-check.py` excludes `.scratch` (`round-48-verifier-spotcheck.md:20,100`) | PARTIAL | `.gitignore:` `.scratch/` landed (`24ebc799`, `round-49.md` M6); deletion not done. Observed now: 187 `.scratch` dirs, 26G, 225 **tracked** `.scratch` files, 6 untracked `round-40/scratch/mori-conform-selftest-*` at `487941b9`. Contract carrier 4 says delete at round end with before/after count — not yet done. `tools/mori-unlanded-check.py:15` still excludes `.scratch/` "on purpose"; QUALITY 80's pathspec is `.ufo/waves/round-<N>/` only. OPEN until the end-of-round removal + count is recorded |
| S48-2 | 48 | report author date (20:22:17) earlier than the lane tip it cites (20:26:17); recurs r49 D-a (`:24-25`, routed 2 / r49 routed 1) | OPEN | `grep -nE 'author date\|%aI' corpus/QUALITY.md tools/*.py` → no instrument; `round-49.md` M3 "Not yet shown"; QUALITY 75 states the limit "both times are lane-written". Carrier is procedural: contract "Round-49 closure routed defects" item 1 (file the report in two fleet commits). Seat `Mo50bExecAuthorDate` is checking the identity half |
| S48-3 | 48 | seven v3 survivors (HTML comment, ZWSP, tab fence, 4-space row, dup authority, split tally, HTML table) | CAPTURED | QUALITY 130 (`:1107`), r49 `count-c1.py` N1–N7, v4 tool |
| S48-4 | 48 | K2–K8 command-binding classes; R11 for D7 (routed 3) | PARTIAL | QUALITY 131 (`:1124`), v4 (`SKILL.md:994`) closes K2,K5,K8,X1,R12–R14; **K4 (pins outside the self-test cell) and the `fixtures/mutants` carve-out of R11 stay open** (`SKILL.md:1002`; `LOG.md:2730`); r50 C1 closes K4 for `SHONEN.md` only (`contract.md` carrier 7) |
| S48-5 | 48 | successor C1 counter must hide variant identity and include an honest pin-updating edit | CAPTURED | QUALITY 129 (`:1091`), r49 `count-c1.py` opaque handle + H1–H9 |
| S48-6 | 48 | unique seat names in wave 1 (M6: eight results carried other lanes' same-name seats) | PARTIAL | this wave uses a `Mo50b…` prefix; `round-48.md` M6 itself says "Not shown able to fail: a duplicate-name check needs the orchestrator's registry"; `tools/mori-wave-settlement.py` / `mori-seat-terminal.py` (`:60` "Duplicate stems in different directories are separate") do not check cross-lane name collisions. OPEN as check |
| S48-7 | 48 | mutation seats' surviving mutants in the v3 selftest (`R48MutV3Header` 3/6, `…Bind` 2/8, `…Hidden` 6/12, `…Unlanded` 2/8) — "none was added this round" | PARTIAL | QUALITY 114 (`:927`) is the rule; r49 landed arms (`SKILL.md:994`). Whether each named survivor now has an arm: not measured here, UNVERIFIED. The c2-counter survivors (4 of 10) are frozen limits |
| S48-8 | 48 | errata to the r48 lesson (M7 wrong mechanism; M3 "four rows" vs three; census line count; SCORECARD After cells appended after review; freeze-sha256 pins 4 of 6 copies) sit as an appended block while the wrong text stays in the table | OPEN | `grep -nE 'four legitimate\|four rows' corpus/lessons/round-48.md` → `:113` (M3) and `:152` (the erratum) both present; `:117` (M7) still states the wrong mechanism. QUALITY 77 (`:349-355`) says "superseded wording is removed, not shadowed … a banner is not a fix"; QUALITY 6 (`:6`) says "Errata are append-only blocks". The two rules conflict for lesson files and no criterion says which wins |
| S49-a | 49 | D-a author date (= S48-2) | OPEN | as S48-2 |
| S49-b | 49 | D-b round shape: one v1 wave of 49 seats vs 64–100; no wave 2/WAVE-DONE; two seats with no report | PARTIAL | contract "Round shape" (`two v1 waves … 64–100`); r49 lesson `:212` accounts seats. No QUALITY criterion for round shape (`grep -nEi 'round shape\|WAVE-DONE' corpus/QUALITY.md SKILL.md` → no hit). **This attempt deviates from the frozen contract**: one v2 wave a2w1 of 64 seats after a host crash, and attempt 1's w1 left 5 reports — the deviation needs a named line in `## Mistakes` |
| S49-c / S49-3 | 49 | D-c "48 wave-1 reports" vs 47; erratum sits in the report, lesson and `LOG.md` still carry it | OPEN | owed in round 50: `corpus/lessons/round-49.md:212` ("48 reports on disk at writing") still holds; `LOG.md` Round 49 entry (`:2724-2730`) — no correction entry yet. Contract carrier 3 names it. Also see QUALITY 77 (sweep every mention) |
| S49-d | 49 | D-d tool selftest tallies 114/17 had no committed output file | CAPTURED | `.ufo/waves/round-50/evidence/selftests/mori-pin-check.txt`, `mori-unlanded-check.txt` (header: `$ python3 tools/… --selftest (git archive of 950e99be…; TMPDIR=<scratch>; 2026-10-26T05:49)`); QUALITY 76 (`:340`) is the rule it recurred against; C1 counter pins them. Note: receipts were measured at the freeze `950e99be`, not the landed tip; `git diff --stat 950e99be 487941b9 -- tools` → empty, so the tool bytes are identical (QUALITY 76's "tool blob identical at named revision and carrying revision" holds) |
| S49-e | 49 | D-e `.scratch` residue + `round-40/scratch/mori-conform-selftest-*` dirs; "ignoring is not removal" | OPEN (see S48-1) | the seven round-40 scratch dirs are now 6 untracked (live); registered selftests (`mori-conform` r40) keep creating them — root cause (selftest tempdir under the wave tree, not `TMPDIR`) is not addressed by any criterion. UNVERIFIED which tool creates them |
| S49-f | 49 | D-f `variants=26` vs 27 `variant` lines | CAPTURED (cause observed, not documented) | `.ufo/waves/round-49/count-c1.py:304`: `variants=%d … len(results) - 1` — the `real` result is a result line but not counted; `grep -c '^variant ' .ufo/waves/round-49/evidence/after-c1-at-tip.txt` → 27. Contract carrier 6 says document it in the lesson; the lesson line is not written yet → the *documentation* is OPEN, the mechanism is closed |
| S49-g | 49 | K4 + R11 carve-out stay open; randomise the handle (`Mo49CritC1Counter`: handle is `sha256(rev, body)[:12]`, recomputable) | OPEN | QUALITY 129 states "names stay opaque only while the variant bytes are unknown to the tool" (`:1105`) — disclosed, not closed. r50 C1 does not randomise anything (it reads SCORECARD/SHONEN) |
| S49-h | 49 | D-g wording: say "different capture" before "understates" | OPEN | contract carrier 8 (lesson note); nothing landed yet. Spot-check `:117` is the only record |
| S49-M2 | 49 | `.scratch` M2 (= S48-1) | PARTIAL | as S48-1 |
| S49-M3 | 49 | report author date (= S48-2) | OPEN | as S48-2 |
| S49-M5 | 49 | dispatch text told a seat to pin `pass=42` vs 44 (plan text not run) | PARTIAL | the seat measured; QUALITY 123/133 cover SKILL pins, not wave-spec prose. This round's `a2w1-spec.json`/dispatch text carrying pin numbers has not been checked by me — UNVERIFIED |
| S49-M6 | 49 | `jj` snapshot failed on `.scratch` temp dirs; selftests leave `round-40/scratch` dirs | CAPTURED (first half) | `.gitignore` `.scratch/`; operator directive 2026-10-25 moves seat scratch to `/fast/scratch/hyaku/mori-r50/<seat>/` (this wave's context). Second half = S49-e OPEN |

## 2. Cross-cutting patterns (for the `## Mistakes` framing)

1. **Prose number drift is the most-repeated class and nothing reads prose.** r45 (29/29, "two comments", `pass=10`), r46 (M2), r47 (M1 `pass=15`, M3 "exactly three"), r48 (M4 truncated digest, M7, "four rows", 20 census lines), r49 (M5 `pass=42`, 48 vs 47, 26 vs 27). QUALITY 40/117/123/124/133 each cover a slice: registry cells, ledger figures, kernel-object counts, flagged defects. Lesson/LOG/report prose counts are covered by no instrument. This round's C1 extends the reconcile idea to SCORECARD/SHONEN — a prose-count reader for lessons stays OPEN.
2. **Stale "Not covered … routed to round N" text in QUALITY.** QUALITY 117 (`:943`, "routed to round 45") and 120 (`:983`, "routed to round 46") were discharged in later rounds but never amended; a reader today cannot tell which holes are still open. QUALITY's own append-only discipline allows an appended note (see `:761`, `:813` "Notes after … (append-only)") — none was appended. OPEN.
3. **Recurring operational slips with detection but no prevention**: seat edits tracked tool (r47 M4 → r48 M5), untracked residue (r45–r49), author-date back-dating (r48 → r49). All three have a detector or a procedural carrier at most; none has a check that fails the round.
4. **Survivor discipline**: QUALITY 114 requires every named survivor to become a fixture + arm, but r47 M5 and r48's mutation survivors were explicitly "not fixed/frozen" and the round-49 data does not show a ledger of them.
5. **Erratum placement**: after round 39, no standalone erratum file; r48 and r49 corrected inside the lesson/report, leaving the wrong sentence in place — the QUALITY 6 vs 77 tension (S48-8).

## 3. Errata files that do exist (all pre-round-40; for completeness)

| id | defect | status | pointer |
|---|---|---|---|
| E37-1 | hardening commit `8ff9bba` vs `1caa242` | CAPTURED | lane `4bfa0490`; r38 counter v4 reconstructs the cited commit (`round-37-erratum.md:10-19`) |
| E37-2 | live receipt 220 vs 225 rows | CAPTURED | QUALITY 105 (`:837`) |
| E37-3 | before-receipt command not runnable as printed (`cwd="/"`) | CAPTURED | QUALITY 78 (`:356`), r38 counter `tool_resolve`; QUALITY 108-111 (`:872-905`) |
| E37-4 | `C2=met` citation must name counter version + blob pin | OPEN | `grep -nEi 'counter version\|names the counter\|blob pin' corpus/QUALITY.md` → no hit; QUALITY 119 (`:972`) covers "receipt names the revision it measured", not the counter version. Pre-round-40, not routed since |
| E37-5 | `LOG.md` append-only breach (in-place rewrite) | PARTIAL | erratum E5 records it; `grep -nE 'append-only' corpus/QUALITY.md` hits 6 (Errata), 761, 769, 813 — no check that `LOG.md` diff is append-only (r50 contract: LOG is appended; `git diff <entering> <tip> --numstat -- LOG.md` can show it). Not shown by a tool. OPEN as an instrument |
| E37-6 | LOG "M1–M5" vs lesson M1–M10 | CAPTURED by erratum text only | QUALITY 77 |
| E37-7/8 | first-working row and axes cell pointer | CAPTURED | SCORECARD corrected in r38 (`round-37-erratum.md:62-74`) |
| E39-1 | r39 report/SCORECARD C2 claim not reproduced (r38 checker `CONFORM=unmet`) | CAPTURED | re-claimed r40 C1 with a genuine before control (`round-39-erratum.md:10-14`); QUALITY 101 (`:788`) |
| E39-2 | `(18 words)` label vs 17 | CAPTURED | QUALITY 90 (`:526`) |
| E39-3 | stale `pass=11` in contract prose; absent `fixtures/make-ancestry-dags.py` | CAPTURED | QUALITY 40/123; contract frozen |

## 4. OPEN list → feeds `## Mistakes`

(Each row: class · what · evidence · proposed fix direction, no counter/predicate/kill-rule change.)

1. **O1 · landing/author date** — filed report's author date earlier than the lane tip it cites (r48 → r49 D-a, M3). No instrument. Fix: the round-50 report is filed in two fleet commits (contract carrier 1); state the measured `git log -1 --format='%aI %cI'` of report commit vs tip. `Mo50bExecAuthorDate` owns the identity half.
2. **O2 · landing/driver time** — report filed after the driver's `complete` line (r47 D2). No criterion. Record the two times in the lesson; low severity.
3. **O3 · round shape** — r49 D-b (49 seats, no wave 2) and **this attempt** (one v2 wave a2w1 of 64 seats, attempt 1's w1 left 5 reports; contract promised two v1 waves). Name the deviation and the host crash; no criterion exists.
4. **O4 · number-drift erratum owed** — "48 wave-1 reports" vs 47 in `corpus/lessons/round-49.md:212` (and any `LOG.md` Round 49 mention). Named correction entry in the round-50 lesson and `LOG.md`, sweeping every mention (QUALITY 77); the r49 `LOG.md` section is `:2724-2730`.
5. **O5 · scratch residue** — 187 `.scratch` dirs, 26G, 225 tracked files, 6 untracked `round-40/scratch/mori-conform-selftest-*`; deletion not done in r49; end-of-round removal with before/after counts owed (contract carrier 4). Root cause of the round-40 dirs (a registered selftest writing under the wave tree) is unaddressed.
6. **O6 · open instrument holes carried** — K4 (SKILL pins outside the self-test cell; C1 here closes it for SHONEN.md only), `fixtures/mutants` carve-out of R11, content-keyed digest check, randomised/non-recomputable handle (`SKILL.md:1002`, `LOG.md:2730`, QUALITY 129 `:1105`).
7. **O7 · no prevention for seats editing tracked tools** — r47 M4, r48 M5; detection by `mori-unlanded-check.py` + sha256 compare only. Mutation seats in this wave (`Mo50bMutC1Counter`, `Mo50bMutCollisionGuard`) are the live exposure; `a2w1/` wave-end sha256 compare of `tools/` and `.ufo/waves/round-50/count-c*.py` against `evidence/freeze-sha256.txt` should be recorded.
8. **O8 · M3-45 help-string and M5-45 named-parameter arms** — rule landed in the tool (`tools/mori-gate-registry.py:292,332,436`) but no selftest arm is named for E4/E6, and QUALITY 120's "Not covered" is stale.
9. **O9 · GIT_* scrub only in gate-registry** — `tools/mori-pin-check.py:535` and `tools/mori-unlanded-check.py:38` inherit `GIT_DIR`; r45 routed defect 4 asked for selftest scrubbing (M11). UNVERIFIED by execution (read-only seat).
10. **O10 · wave-item assertions carry receipts** — M7-45 (two failed routes asserted as fact); no criterion.
11. **O11 · seat-name uniqueness across lanes** — r48 M6; no check (orchestrator registry needed).
12. **O12 · QUALITY 6 vs 77 for lesson errata** — r48 lesson left wrong M3/M7 text in the table with a trailing errata block (`corpus/lessons/round-48.md:113,117,150-157`); decide which rule governs lessons.
13. **O13 · stale "Not covered/routed to round N" text in QUALITY 117, 120** — append a dated note (QUALITY precedent `:761`, `:813`).
14. **O14 · prose counts in lessons/LOG not re-derived** — class recurs r45–r49 (§2.1); only SKILL/SCORECARD/SHONEN cells and ledger figures are mechanically reconciled.
15. **O15 · survivor fixtures** — QUALITY 114 vs r47 M5 / r48 mutation-seat survivors left "not added"; whether they are now arms: unmeasured.
16. **O16 · `variants=26` vs 27 lines** — mechanism read at `.ufo/waves/round-49/count-c1.py:304` (`len(results) - 1`, the `real` line excluded); document in the round-50 lesson (contract carrier 6).
17. **O17 · D-g wording** — "different capture" before "understates"; spot-check `round-49-verifier-spotcheck.md:117`; lesson note owed (contract carrier 8).
18. **O18 · E37-4 / E37-5** (pre-40) — counter version beside `C2=met`; LOG append-only has no instrument. Carry only if the L1 wants the pre-40 list.

## 5. Grep commands used (paste-ready; run from `/home/vgpnk/Projects/shokunin/mori-shokunin`)

```
ls corpus/lessons | grep -i erratum
find . -name '*erratum*' -not -path './.git/*' -not -path './.scratch/*'
ls corpus/lessons | grep 50
grep -nE '^(#|[0-9]+\.)' corpus/QUALITY.md | tail -30
grep -nEi 'author date|author-date|%aI|authored' corpus/QUALITY.md
grep -nEi 'untracked|\.scratch' corpus/QUALITY.md
grep -nEi 'erratum|correction entry|named correction' corpus/QUALITY.md
grep -nEi 'GIT_DIR|GIT_\*|scrub' corpus/QUALITY.md
grep -nEi 'parser key|add_argument\("--selftest' corpus/QUALITY.md
grep -nEi 'variants=|variant line' corpus/QUALITY.md
grep -nEi 'residual' corpus/QUALITY.md
grep -nEi 'randomi[sz]' corpus/QUALITY.md
grep -nEi 'hypothesis|route claim|wave item' corpus/QUALITY.md
grep -nEi 'counter version|names the counter|v1 counter|HARDENING_COMMIT|counter (bytes|blob)' corpus/QUALITY.md
grep -nEi 'round shape|WAVE-DONE|64.100' corpus/QUALITY.md SKILL.md
grep -nE 'GIT_' tools/mori-gate-registry.py tools/mori-pin-check.py tools/mori-unlanded-check.py
grep -nE 'environ' tools/mori-pin-check.py tools/mori-unlanded-check.py
grep -oE 'arm\("[a-z_0-9]+"' tools/mori-gate-registry.py
grep -nE 'four legitimate|four rows' corpus/lessons/round-48.md SKILL.md corpus/QUALITY.md
grep -nE '48 wave-1|47 wave-1|48 reports|47 reports' LOG.md corpus/lessons/round-49*.md
grep -nE 'K4|R11' SKILL.md LOG.md SCORECARD.md
grep -nE 'S478' corpus/SOURCES.md | grep -oE 'User-Agent|browser UA'
grep -c '^variant ' .ufo/waves/round-49/evidence/after-c1-at-tip.txt
git diff --stat 950e99be 487941b9 -- tools
git status --porcelain | grep -c 'round-40/scratch'
git status --porcelain --ignored | grep -c '^!! .scratch'
git ls-files .scratch | wc -l ; du -sh .scratch
```

## Findings

- **MED** — `corpus/lessons/round-49.md:212` (and any `LOG.md` Round 49 mention near `:2724-2730`) still carries "48 reports"; the round-49 spot-check D-c owes a named correction (47). Open until the round-50 lesson/LOG entry lands (O4).
- **MED** — Author-date back-dating of the filed report (r48 defect 2, r49 D-a/M3) has no instrument; carrier is procedural only (contract carrier 1). Round-50 report must show `%aI` ≥ lane tip time (O1).
- **MED** — Scratch residue (O5): 187 `.scratch` dirs / 26G / 225 tracked `.scratch` files / 6 untracked `.ufo/waves/round-40/scratch/mori-conform-selftest-*`; deletion with before/after counts still owed; `tools/mori-unlanded-check.py:15` excludes `.scratch/` so it cannot see them.
- **MED** — Round shape deviates from the frozen contract (one v2 wave a2w1 + attempt-1 w1's 5 reports vs "two v1 waves summing to 64–100"); needs a named `## Mistakes` line (O3); no criterion covers round shape.
- **MED** — Prose-count drift is a recurring class (r45–r49, five rounds) with no instrument reading lesson/LOG prose (O14); each QUALITY criterion covers only a slice.
- **LOW** — `tools/mori-pin-check.py:535` and `tools/mori-unlanded-check.py:38` inherit `GIT_*` from the caller; only `tools/mori-gate-registry.py:106-108` scrubs (r45 M11 / routed 4). UNVERIFIED by execution.
- **LOW** — `corpus/QUALITY.md:117-ff` ("routed to round 45") and `:983-997` ("routed to round 46") "Not covered" text is stale after later rounds discharged it; append a dated note.
- **LOW** — `corpus/lessons/round-48.md:113,117` keep the wrong M3 ("four rows") and M7 (mechanism) text with an errata block at `:150-157`; QUALITY 6 vs 77 conflict for lesson errata (O12).
- **LOW** — K4, the `fixtures/mutants` carve-out of R11, content-keyed digest check and a non-recomputable handle remain open (`SKILL.md:1002`, `LOG.md:2730`, QUALITY 129 `:1105`) — this round's C1 closes K4 for SHONEN.md only.
- **LOW** — No standalone `round-*-erratum.md` exists from round 40 (only 37 and 39); the sweep's erratum scope is empty beyond those two, and their open items (E37-4 counter version beside `C2=met`, E37-5 LOG append-only) have no instrument.
- **LOW** — Receipts `evidence/selftests/mori-pin-check.txt` and `mori-unlanded-check.txt` were measured at the freeze `950e99be`, not the landed `487941b9`; `git diff --stat 950e99be 487941b9 -- tools` is empty so the bytes agree (QUALITY 76 holds), but the header names the freeze revision, not the tip.
