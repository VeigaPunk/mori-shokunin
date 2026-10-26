# Mo51ScoutMistakeSweep — mistake sweep for the frontier step (round 51, wave w1)

Seat: scout, leaf, read-only. Measured at lane tip `b504cb17` (wave spec/dispatch commit; data commit `87e0c374`).
Scratch: `/fast/scratch/hyaku/mori-r51/Mo51ScoutMistakeSweep/` (created, only `tmp/` used, removed before finishing).
No ENTAIL judgments here (not an entailment seat).

## Scope and one deviation from the assignment text

Read in full: `corpus/lessons/round-46-verifier-spotcheck.md` … `round-50-verifier-spotcheck.md`, the `## Mistakes`
tables of `round-46.md` … `round-50.md` (their `captured-by` and `fix` cells), and
`corpus/QUALITY.md` (criteria 120–136 in full, 1–136 by grep).

**There is no `round-*-erratum.md` file from round 40 on.** Command and result:

```
$ find /home/vgpnk/Projects/shokunin/mori-shokunin -name 'round-*-erratum*' -not -path '*/.git/*' -not -path '*/validate/*'
corpus/lessons/round-37-erratum.md
corpus/lessons/round-39-erratum.md
```

Only rounds 37 and 39 have an erratum file. For "from round 40" I therefore swept (a) those two files, because the
round-40+ instruments inherit their defects, and (b) the append-only correction blocks that took the erratum role
after round 40: `LOG.md:2597` (round-43 seat count, appended r44), `LOG.md:2655` (r45 freeze-manifest tally, r46),
`LOG.md:2689` (erratum to the r47 entry, r48), `corpus/lessons/round-50.md:241` (r49 "48 of 49"), and the SCORECARD
round-50 correction paragraph (`round-50.md:280`). The round-40 seat files `w1/RevErratum.md` and
`w1/ScrErratumCheck.md` (and r48 `w1/ScribeLogErratum.md`) are seat reports about those corrections, not errata.

The spot-checks record **no `disagree` verdict** in any Discernment table (r46: 2 agree; r47: 5 agree, 1 not
re-opened; r48: 9 agree; r49: 6 agree, one "agree, one nuance"; r50: 5 agree). The disagreements the closures raise are
conformance defects, claim-ruling limits and routed defects; those are what is listed below.

## Grep commands used (all `git grep -n -I --no-color` at `b504cb17`, run from the lane root)

```
G1  git grep -nE 'author date|%aI|metaedit|update-author|AuthorDate' -- corpus/QUALITY.md corpus/lessons/round-5*.md tools SKILL.md SHONEN.md LOG.md
      -> no hit in corpus/QUALITY.md or SKILL.md/SHONEN.md; hits only in lessons/round-50*.md (:19,:30,:33,:186,:201-204) and
         tools/mori-round17-* (unrelated); LOG.md:2726 is a round-49 entry sentence.
G2  git grep -nE '48 of 49|47 of 49|report count|present=[0-9]+' -- corpus/QUALITY.md        -> no output (exit 1)
G3  git grep -n 'scratch' -- tools/mori-unlanded-check.py .gitignore
      -> .gitignore:5:.scratch/ ; tools/mori-unlanded-check.py:15 ".scratch/ and anything git ignores are outside the scope on purpose"
G4  git grep -nE 'K4|tally pin' -- corpus/QUALITY.md corpus/lessons/round-50.md corpus/lessons/round-49.md .ufo/waves/round-51/contract.md SHONEN.md
      -> QUALITY.md:1196 (Not covered: "a tally pin outside SHONEN.md is not enumerated"); round-50.md:230 (K4 routed); contract.md:122 (K4 beyond SHONEN -> round 52)
G5  git grep -nE 'R11|D7' -- corpus/QUALITY.md tools/mori-pin-check.py SKILL.md
      -> QUALITY.md:1061,1118,1126-1137; pin-check.py:35,349,358,643 (R11 and its fixtures/mutants carve-out); SKILL.md:961,994,1002 ("Still open: K4 …, the fixtures/mutants carve-out of R11, and a content-keyed digest check")
G6  git grep -iE 'randomi[sz]|opaque handle|blinding handle' -- corpus/QUALITY.md .ufo/waves/round-51
      -> only corpus/QUALITY.md:1105 ("the harness does not randomise the edits"); NOTHING under .ufo/waves/round-51
G7  git grep -nE 'S478|S507' -- corpus/SOURCES.md  -> :257 (anchor cell carries "fetched 2026-10-25 with a browser user agent"; recheck cell is the cadence `180d`)
    git grep -niE 'user.agent|S478' b504cb17 -- corpus/lessons/round-48.md -> :14, :31-34 (browser UA note, HTTP 418 without it)
G8  git grep -nE 'unique|duplicate-name|same name' -- corpus/QUALITY.md   -> no criterion on seat-name uniqueness (hits :33,:71,:108,:296,:298 are about other things)
G9  git grep -nE 'negative claim|normalis|normaliz' -- corpus/QUALITY.md  -> :294 heading only (round-23 negative claims = complete enumeration; says nothing about raw HTML vs normalised text)
G10 git grep -niE 'entail' -- corpus/QUALITY.md                            -> :1079 (128 "proves location, not entailment"), :1087, :1157 — a limit, no criterion that requires a reviewer vote
G11 git grep -nE 'E4|counter version|blob pin' -- corpus/QUALITY.md        -> nothing about "a C2=met citation names the counter version and its blob pin" (only :997 unrelated)
G12 git grep -nE '\.scratch|hermetic|TMPDIR|bubblewrap|bwrap' -- corpus/QUALITY.md -> :999,:1003,:1007 (r45 write-scope, 121), :1093 (129). No criterion for hermetic re-execution / SIGKILL residue / relocation
G13 git grep -niE 'in no commit|path resolves|every cited path|cited path' -- corpus/QUALITY.md -> no criterion that a path cited in a contract exists in a commit (:883 is the repo-relative --tool rule)
G14 git grep -nE '^64\.' -- corpus/QUALITY.md ; sed -n '/^64\./,/^65\./p' corpus/QUALITY.md -> 64: settlement receipt for per-seat report presence (:227)
G15 git grep -nE 'used-by|used_by|\{0,3\}' b504cb17 -- .ufo/waves/round-48/count-c2.py -> :9, :92 (`^ {0,3}\|\s*S…`), :316 (arm used_by_missing_unmet)
G16 git grep -nE 'scratch|clone|class=' -- tools/mori-pin-check.py -> v5 docstring :130-139 (shared clone under --scratch, class=env/stale), :713,:741,:826,:843 (class tags)
G17 git grep -nE 'LANE|TMPDIR|mkdtemp' -- .ufo/waves/round-40/conform.py -> :71-72 (LANE derived from __file__), scratch under TMPDIR
G18 git grep -l -F '/home/vgpnk' HEAD -- <tools/*.py|*.sh>  -> tools/mori-blind-check.sh, tools/mori-misroot-sweep.py, tools/mori-round17-context-check.py (the 3 that predate QUALITY 127)
```

## Table 1 — round-46 … round-50 spot-check defects and `Mistakes` rows

Status legend: CAPTURED (pointer) = a QUALITY criterion, a lesson fix, a landed tool or a dated correction carries it;
CAPTURED-partial = carried with a named residue; OPEN = nothing carries it (or only a "routed" sentence).

| id | defect / disagreement (source) | status | pointer / reason |
|---|---|---|---|
| 46-D1 | `count-repins.py` is not a calibration proof: needles are row-wide substrings, no runtime measurement (`round-46-verifier-spotcheck.md:71`; lesson r46 M1) | CAPTURED | QUALITY 123 (`corpus/QUALITY.md:1028`); `tools/mori-pin-check.py`; `SKILL.md:917` "retired as a calibration proof" |
| 46-D2 | `rows=4` is a hard-coded constant, not a measured count (`:72`) | CAPTURED (by retirement) | `SKILL.md:917` retires the counter; the file stays in `.ufo/waves/round-46/` as history. No QUALITY criterion says "a count in a verdict line is measured" beyond 40/CORPUS "a count carries its command" |
| 46-D3 | `.scratch/` leftovers, `MutMissing/` `MutStaleC1/` `MutStaleC2/` (`:73`) | CAPTURED-partial | `.gitignore:5`; removal recorded in r50 lesson `:211`; producers fixed at r51 data (G16, G17; `evidence/c1-at-data.txt` `kill_residue=0`). **QUALITY side OPEN**: G12 shows no criterion for hermetic re-execution; the r51 criteria draft owns it |
| 46-D4 | no promotion claims; all SHONEN boxes `[~]` (`:74`) | not a defect | operator-owned |
| 46-E1 | round-45 freeze manifest "29/29" vs 27 OK (`:35`; lesson r46 M2) | CAPTURED | append-only correction `LOG.md:2655`; QUALITY 40 / "a count carries its command" (cited by r46 M2). No instrument compares a prose tally with its command (see 50-M2) |
| 47-D1 | 53 untracked paths: late `w2` reports uncommitted when the report was filed (`round-47-verifier-spotcheck.md:20,96`) | CAPTURED | `tools/mori-unlanded-check.py` (r48 M1, `UNLANDED_SELFTEST pass=17`); QUALITY 80 (`:368`); `LOG.md:2689` erratum; r48 closure `:20` finds no round file outside `.scratch/` |
| 47-D2 | report filed 2 minutes after the driver's `complete` line (`:97`) | OPEN (not recurring) | `LOG.md:2689` item (2): "carried, this round files after its last wave settles". No criterion/instrument; r48 `:16` (20:27:04 < 20:27:28), r49 and r50 digests show the report before `complete` |
| 47-D3a | successor `count-c2.py`: used-by arm, 0–3-space rows, one path per cell (`:98`; r47 M5) | CAPTURED | `.ufo/waves/round-48/count-c2.py:9,92,316` (G15); `LOG.md:2689` (3); QUALITY 128 |
| 47-D3b | v2 selftest arms: symlink containment, argv sub-checks, case-insensitive unparsed; line-count and truncated-digest pins | CAPTURED | `tools/mori-pin-check.py` v3→v5 (12 symlink/realpath hits, R6/R12; `SKILL.md:994`; `LOG.md:2689`). **Stale text**: QUALITY 123 (`:1039-1040`) still says "Not covered: line-count pins and truncated digests" although R6/R12 now cover them (LOW) |
| 47-D3c | lesson "F4 citation precision" (`:98`) | OPEN / UNVERIFIED | the closure does not say which lesson F4 it means and no later file defines it; I could not resolve it from committed text |
| 47-D4 | lesson says "no spot-check exists yet" (`:99`) | CAPTURED | every lesson from r48 has `### Spot-check` citing the closure (e.g. `round-50.md:172`) |
| 47-D5 | S478 refetch needs a browser UA; say so in the row's recheck (`:100`) | CAPTURED-partial | note lives in `round-48.md:14,31-34` (curl without UA → HTTP 418) and the row's anchor cell (`SOURCES.md:257`); the `recheck` cell stays the cadence `180d`, so the row's recheck cell itself does not carry it |
| 47-M3 | "exactly three tracepoints" from a "such as" sentence | CAPTURED | QUALITY 124 (`:1041`) |
| 47-M4 | mutation seat edited the tracked `tools/mori-pin-check.py` | CAPTURED-partial | unlanded check lists modified `tools/` files; r47 M4 fix (frozen sha256 compare, seats `cp` the target to scratch); residue named in r48 M5: "a seat can still edit and restore between two runs" |
| 47-M5 | `count-c2` survivors (used-by arm, indented row, extra path) | CAPTURED | see 47-D3a |
| 48-D1 | 114 untracked `.scratch` dirs; unlanded check cannot see them (`round-48-verifier-spotcheck.md:23,100`; r49 M2) | CAPTURED-partial | `.gitignore:5` (`24ebc799`); r50 deletion (`round-50-verifier-spotcheck.md:48`); producers fixed r51 data. `tools/mori-unlanded-check.py:15` still excludes `.scratch/` "on purpose"; no QUALITY criterion (G12) |
| 48-D2 | report **author** date earlier than the lane tip it cites (`:25,101`; r49 M3, r49 D-a, r50 D-a) | OPEN (operator-owned) | G1: no QUALITY criterion, no instrument. `round-50.md:201-206` dispositions it as a procedure (compare `%aI` with `%cI`) and `fleet-commit.sh:84-85` is fleet-owned (r50 §5.6). Recurred in r48, r49, r50 |
| 48-D3a | seven v3 survivors; K2–K8; R11 for D7 (`:102`; r49 M4) | CAPTURED-partial | N1–N7 in r49 `count-c1.py`; QUALITY 130, 131; `SKILL.md:994` (v4: F1–F5, K2, K5, K8, X1, R12–R14). **OPEN**: K4 (pins outside the self-test cell) and the `fixtures/mutants` carve-out of R11 — G5 `SKILL.md:1002` "Still open"; QUALITY 131 `:1136-1138` |
| 48-D3b | successor C1 counter hiding variant identity, with an honest pin-updating edit | CAPTURED | QUALITY 129 (`:1091`); r49 `count-c1.py` (opaque sha256 handle, H5) |
| 48-D3c | unique seat names in wave 1 (M6) | CAPTURED-partial | r51 spec: 68 names, 68 unique, all `Mo51…` prefix (`w1-spec.json` items; checked with Python). No QUALITY criterion (G8) and no duplicate-name instrument: r48 M6 itself says "not shown able to fail … needs the orchestrator's registry" |
| 48-D4 | SHONEN boxes `[~]`, not fully checkable (`:103`) | not a defect | operator-owned |
| 48-M4 | truncated digest `c39e5a73…` pinned a historic blob | CAPTURED | pin-check v3 R6, v4 R12; the row repaired (`LOG.md:2689` ff.). QUALITY 123 not updated (see 47-D3b) |
| 48-M7 | negative claim made on raw HTML where tags split the words | OPEN | G9: no QUALITY criterion for "a negative claim about a copy is made on the normalised text". Only the lesson fix sentence (`round-48.md` M7). QUALITY 71 (`:296`) is a different rule |
| 49-D-b | one v1 wave of 49 seats against the 64–100 band; two seats with no report (`round-49-verifier-spotcheck.md:25,114`) | CAPTURED | r50 §Round shape (`round-50.md:250-260`, the two seats were late, not dead, `:219-224`); QUALITY 64 (settlement receipt `:227`); r51 contract fixes one v2 wave |
| 49-D-c / 50-M2 | lesson count "48 of 49 reports" counted directory entries (`:26`; r50 M2) | CAPTURED-partial | correction `round-50.md:241-248` and `LOG.md` round-50 entry. **OPEN as an instrument**: r50 M2 says "not yet shown"; G2: QUALITY has no criterion comparing a prose report count with `w1/*.md`; QUALITY 64's receipt is the natural carrier |
| 49-D-d | tool selftest tallies had no committed output file (`:27,111`) | CAPTURED | r50 `evidence/selftests/*.txt`; QUALITY 134 (`:1178`), whose check names the committed receipt |
| 49-D-e | ~183 `.scratch` dirs left (ignoring is not removal) | CAPTURED-partial | see 48-D1 |
| 49-D-f | `variants=26` against 27 lines | CAPTURED (lesson) | `round-50.md:225-229` (`len(results) - 1`, counter frozen). The counter text stays as is |
| 49-D-g | "understates" wording on the staged `six boots` capture | CAPTURED (lesson) | `round-50.md:236-239`; the Gate wording for staged rejects is not a QUALITY criterion |
| 49-#7 | handle randomisation, "a blinding handle given to an instrument under test is random" | **OPEN** | G6: restated for round 51 in `round-50.md:232-235`, but `contract.md` §"Round-50 closure routed defects — carriers" (`:119-125`) carries items 1,2,3,4,5,6 and item 3 only as "successor calibration counter and K4 beyond SHONEN → round 52"; the randomised handle is named nowhere under `.ufo/waves/round-51`. The rule can be lost |
| 49-M5 | plan text pinned `C1_SELFTEST pass=42` while the counter prints 44 | CAPTURED | QUALITY 134 + the reconciler; r50 `a2-pin-check-at-landed.txt` |
| 49-M6 | `jj` snapshot failed on churning `.scratch` | CAPTURED | `.gitignore:5` (`24ebc799`); producers removed in r51 data |
| 50-D-d / r50 §5.1 | re-execution not hermetic: `mori-pin-check.py:884-887` exported a tree under `<repo>/.scratch`, `conform.py:69` hardcoded the lane path | CAPTURED (r51 data) | contract P-C1; `evidence/c1-at-data.txt` `C1=met kill_residue=0 relocated=met`; pin-check v5 (G16), `conform.py:71-72` (G17). **QUALITY criterion not yet written** (G12) — r51 criteria draft |
| 50-§5.2 | round shape: stay within the 100-seat ceiling across attempts (r50 ran 104) | CAPTURED-partial | r51 contract `:127-133`: one v2 wave, total ≤ 128; `w1-dispatch.json` `total=68`. The contract's own numbers disagree: `:122` "(64–100 seats) … total <= 128" vs `:129` "band 64–128" vs r50 closure "100 ceiling" (`round-50-verifier-spotcheck.md:39`) — LOW, ambiguity not a breach at 68 |
| 50-§5.3 | successor C1 counter: verdict-word substring, second `## Axes`, Score column unread, vacuous `admitted` arm, symlinked pin path; K4 beyond SHONEN | OPEN (routed to r52) | `contract.md:122` "not claimed this round"; QUALITY 134 `:1194-1198` lists the same not-covered items |
| 50-§5.4 / 50-M4 | C2 counter passed six overclaims; entailment needs a reviewer step or counter arm | CAPTURED-partial (in progress) | r51 P-C2 entailment arm (`contract.md:78-82`), `count-c2.py`; at data `entailed=0` (`evidence/c2-at-data.txt`). QUALITY 128 (`:1079`) still says "proves location, not entailment" and G10 shows no criterion requiring the vote; the r51 criteria draft owns it |
| 50-§5.5 | name contract deviations in `LOG.md`, not only the lesson (D-c) | OPEN (until r51 LOG lands) | G-batch: `LOG.md` has no "deviation" heading after `:1724`; r50's own D-c deviation is in the lesson (`round-50.md:250ff`) — the r51 LOG entry must name it. Contract `:123-125` says it will |
| 50-§5.6 | fleet-owned `fleet-commit.sh:84-85` author date | OPEN (operator) | see 48-D2; contract `:125` "operator's (report notes it)" |
| 50-M1 | self-assessment drift (SHONEN 60/60, 13/13; Axes cells) | CAPTURED | QUALITY 134 (`:1178`), r50 `count-c1.py`; r51 data re-pins (SKILL/SHONEN diff). Not covered: tally pins outside `SHONEN.md` (K4) |
| 50-M3 | dispatch before landing the data; attempt died, 35 seats unknown | CAPTURED by behaviour | r51 landed data `87e0c374` before dispatch `b504cb17`; QUALITY 64 (receipt). No QUALITY criterion states "data lands before dispatch" (the only carrier is `round-50.md` M3 fix) — LOW |
| 50-M4 | counter-passing overclaim | see 50-§5.4 | |
| 50-§3 limits | C1/C2 counter named limits (`round-50.md:284-300`) | CAPTURED as limits | stay named in the lesson; QUALITY 134, 135 "Not covered" |

## Table 2 — erratum files (rounds 37 and 39, inherited) and post-40 correction blocks

| id | defect | status | pointer / reason |
|---|---|---|---|
| E37-1 | hardening commit `8ff9bba` touches no tool byte; real commit `1caa242` | CAPTURED-partial | the r38 counter v4 reconstructs the commit and requires it to touch the tool (erratum text). G13: no QUALITY criterion for "an attributed commit touches the named file" |
| E37-2 | live receipt 220 rows vs 225 | CAPTURED | QUALITY 105 (`:837`; neither number is a freshness verdict) |
| E37-3 | before-receipt command not runnable as printed (`--tool` from `cwd="/"`) | CAPTURED | QUALITY `:883` (resolve a repo-relative `--tool`), r38 counter `tool_resolve` |
| E37-4 | `C2=met` is true for counter v1 only; "a `C2=met` citation names the counter version and its blob pin" | OPEN as criterion | G11: the rule sits only in `round-37-erratum.md:40-45`. In practice r46–r50 closures print counter sha256 (`grep -c sha256` → 6, 3, 3, 8, 6), but nothing requires it |
| E37-5 | `LOG.md` entry rewritten in place (`5631efa`) | CAPTURED | QUALITY item 4 "Errata are append-only blocks" (`QUALITY.md:6,60`); QUALITY 102 for SOURCES rows |
| E37-6 | mistakes list M1–M5 vs M1–M10; debt (f) re-filed operator-owned | CAPTURED | QUALITY 40 / "a count carries its command"; the debt stays operator-owned (no lane action) |
| E37-7 | capability first-working round | CAPTURED | SCORECARD correction; QUALITY 134 reconciles Axes/pins only, not the capability table — LOW |
| E37-8 | axes cell points at the wrong axis | CAPTURED | QUALITY 134 (r50 `count-c1.py` Last-change reconciliation) |
| E39-1 | r39 report said r38 printed `CONFORM=met` on bypass-wait; receipt says `unmet` | CAPTURED-partial | the erratum itself and r40's genuine before-control (`c10-red-decoy.txt`); QUALITY has no "before-control must be a committed receipt of the named tool" line (G-batch: `before-control`/`red-before` → 0 hits) |
| E39-2 | quote labelled "(18 words)" is 17 | CAPTURED | QUALITY 90 (`:526`) |
| E39-3 | contract prose `pass=11` (gate prints 12); a cited fixture path in no commit | CAPTURED-partial | pins: QUALITY 40, 123, 134. The "cited path in no commit" half: G13 — no criterion; the pin reconciler requires a path under `tools/` or `.ufo/waves/round-N/` (pin-check docstring `:93`) only for registry rows |
| X44 | round-43 "34 of 64" seats rate-limited vs 8 (`LOG.md:2597`) | CAPTURED | QUALITY "a count carries its command" + QUALITY 64 for seat counts; correction is append-only |
| X46 | round-45 "29/29" vs 27 OK (`LOG.md:2655`) | CAPTURED | same as 46-E1 |
| X48 | r47 report said three late seats "had not returned" (`LOG.md:2689`) | CAPTURED | `tools/mori-unlanded-check.py`, QUALITY 80 |
| X50 | r49 "48 of 49" (`round-50.md:241`) | CAPTURED-partial | see 49-D-c |

## Findings

1. **MED** — `.ufo/waves/round-51/contract.md:119-125` — the randomised-handle rule (r50 routed item 7, restated for round 51 at `corpus/lessons/round-50.md:232-235`) is in no carrier: no claim, no instrument, no `## Frontier step`/mistake line names it, and the "successor calibration counter" item is deferred to round 52 without it. Status OPEN; the r51 lesson/LOG must carry it explicitly or it is dropped for the third time.
2. **MED** — `corpus/QUALITY.md` (G12, G10) — the two r51 behaviours with a landed tool and no criterion: hermetic re-execution (no residue in the repo read, no host path needed; `tools/mori-pin-check.py` v5, `conform.py:71-72`) and a recorded non-author entailment vote per claim row (QUALITY 128 `:1079,1087` still says "proves location, not entailment"). Both are CAPTURED by tool only, OPEN as criteria; they belong in the r51 QUALITY draft with their counter receipts as the "shown able to fail" arm.
3. **MED** — report **author date** before the cited lane tip: round 48 (`round-48-verifier-spotcheck.md:25`), round 49 (`round-49-verifier-spotcheck.md:24`), round 50 (`round-50-verifier-spotcheck.md:30`). OPEN for three rounds, no QUALITY criterion (G1), fleet-owned cause (`scripts/hyaku/fleet-commit.sh:84-85`). The lane can only compare `%aI` with `%cI` at filing and report both values (`round-50.md:201-206`).
4. **MED** — `round-50.md:241` M2 / 49-D-c — a prose report count in a lesson has no instrument (G2). Round 51 must state its own report count; the settlement scan (`tools/mori-wave-settlement.py scan`, QUALITY 64) is the carrier. The count moves while the wave runs (`ls .ufo/waves/round-51/w1 | wc -l` printed 38 mid-wave and 49 a few minutes later, of 68 dispatched, counting `swarm-registry.json`-style non-report entries if present); any count in the lesson written before settlement is the same class.
5. **LOW** — `corpus/QUALITY.md:1039-1040` (criterion 123) says line-count pins and truncated digests are "Not covered"; `SKILL.md:994` (v4 R12–R14) and `LOG.md:2689` (3) say they are covered. Stale cell, not a wrong tool.
6. **LOW** — `SKILL.md:1002` and `corpus/QUALITY.md:1136-1138`: K4 (pins outside the self-test cell), the `fixtures/mutants` carve-out of R11 and a content-keyed digest check stay OPEN (routed to round 52, `contract.md:122`).
7. **LOW** — QUALITY has no rule that a negative claim about a source copy is made on the normalised text (r48 M7, G9), none for seat-name uniqueness (r48 M6, G8; r51 satisfies it in fact: 68/68 unique, all `Mo51` prefixed), none that a `C2=met` citation names its counter version (E37-4, G11), none that a contract-cited path exists in a commit (E39-3, G13).
8. **LOW** — `contract.md:122` ("64–100 seats … total <= 128"), `:129` ("band 64–128") and the r50 closure's "100 ceiling" (`round-50-verifier-spotcheck.md:39`) disagree; 68 seats breach none.
9. **LOW** — `corpus/SOURCES.md:257` (S478): the browser-User-Agent note is in the anchor cell and `round-48.md:31-34`; the `recheck` cell is `180d`, so r47 routed item 5 ("say so in the row's recheck") is met by prose elsewhere, not in the cell.
10. **LOW** — `round-47-verifier-spotcheck.md:98` "lesson F4 citation precision" names an F4 that no committed file defines (UNVERIFIED: could not resolve).
11. **Observed, no action** — erratum files exist only for rounds 37 and 39; from round 40 corrections are append-only blocks in `LOG.md` and the next round's lesson (Table 2), which a `round-*-erratum.md` glob does not find.

Report: .ufo/waves/round-51/w1/Mo51ScoutMistakeSweep.md
