# Mo53ScoutMistakeSweep — verifier-spotcheck sweep, rounds 48–52

Seat: Mo53ScoutMistakeSweep (scout, round 53 wave w1). Read-only; no lane gate, counter or selftest executed; nothing
written but this file. Read: `contract.md`, the five closures
`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-48-verifier-spotcheck.md` … `round-52-verifier-spotcheck.md`
(in full), the round-50/51/52 lessons' routed-defect sections, `round-51-erratum.md`, `corpus/QUALITY.md` rows 125–143,
`SKILL.md` §Round49–Round52, `LOG.md` Round 50–52, `SCORECARD.md` Round 52 section, the round-52 sweep
`.ufo/waves/round-52/w1/Mo52ScoutMistakeSweep.md` (rounds 47–51; used as a cross-check, every status below was
re-derived at the current tip). Lane tip at read: `95cf78eef71979f9b740ef6bc3c5299b6beff86e` (data `2a4213bf`).
Scratch `/fast/scratch/hyaku/mori-r53/Mo53ScoutMistakeSweep/` (created and removed, nothing cited from it). No LSP
server answers markdown, so text search is the only method: a grep hit shows a pointer exists, not that the pointer works.

## 0. Disagreements

The five closures record **zero admit/reject disagreements** with the lane. Every discernment-table row reads
`agree` (one `agree, one nuance` in r49; one `agree (unprovable to differ)` in r48):

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons
for f in round-4[89]-verifier-spotcheck.md round-5[012]-verifier-spotcheck.md; do
  echo "$f: disagree-cells=$(grep -cE '\|\s*\*{0,2}disagree' $f) agree-cells=$(grep -cE '\|\s*\*{0,2}agree' $f)"; done
→ r48 0/10, r49 0/7, r50 0/6, r51 0/4, r52 0/4   (exit 0)
grep -nE '\*\*disagree|\| disagree' round-4[89]-verifier-spotcheck.md round-5[012]-verifier-spotcheck.md  → rc 1 (no hit)
```

What the closures route are conformance defects (D-x), counter limits and wording errors. Those are the rows below.
Key: CAPTURED (pointer) = a QUALITY row, lesson fix, erratum or tool carries it and the pointer was seen at the tip;
OPEN = nothing seen carries it; OPERATOR = fleet-owned, outside the lane; ROUTED = named for a later round, not yet a
carrier.

## 1. Defect table

| # | closure item | defect | status | pointer / evidence |
|---|---|---|---|---|
| 48-1 | r48 §1(a), §5.1 | 114 untracked `.scratch/*` dirs; `.scratch` outside the unlanded check | CAPTURED | `.gitignore:5` `.scratch/`; deleted in r50 (`round-50.md` routed item 4); producers: pin-check fixed (QUALITY 137 `:1254`, `SKILL.md` r51 `--scratch` rule), `round-40/conform.py` fixed (`round-51.md` Wave w1). At this tip `git status --porcelain --ignored \| grep -c '\.scratch'` → 0. Remaining producers: see 50-4 (OPEN). |
| 48-2 | r48 §1(b), §5.2; r49 D-a; r50 D-a; r51 §5.6 | report commit author date earlier than the lane tip it cites | OPERATOR | `round-50.md` item 1 (landing comparison rule, both values go in the report), `round-51.md:226-232` item 6 ("Routed to the operator, unchanged"); mechanism is `scripts/hyaku/fleet-commit.sh:84-85`. No QUALITY row (`grep -n -iE 'author date\|authored\|author-date' corpus/QUALITY.md` → only operator-authored-reflection hits, none about commit dates). The lane can only record the comparison. Not repeated in the r52 closure, so unchanged-or-fixed is UNVERIFIED. |
| 48-3a | r48 §5.3 | seven v3 survivors; K2–K8 classes; filename-sniff leak; successor C1 hiding variant identity | CAPTURED | QUALITY 129 (opaque handle), 130 (renders-as-row), 131 (bound pin); `SKILL.md:994-1000` v4 adds F1–F5, K2, K5, K8, X1, R12–R14 (K3, K6, K7 = R12–R14 per `round-49/w1/Mo49ExecK3K6K7.md`); `round-49.md:179`. |
| 48-3b | r48 §5.3 | K4 (pins outside the self-test cell) | CAPTURED (r52), partly | QUALITY 141 (living pins in QUALITY.md and README.md), `round-52/count-c1.py` arm C. Still not armed: pins in `PROVINCE.md`, `SKILL.md`, `LOG.md` — `SCORECARD.md:2771` "Planned (round 53) … PROVINCE/SCORECARD present-tense tally pins (K4 scope)"; not in the r53 contract → ROUTED. |
| 48-3c | r48 §5.3; r49 §5.7 | rule R11 carve-out (`fixtures/mutants`) | OPEN | `SKILL.md:1002` "Still open: … the `fixtures/mutants` carve-out of R11"; `round-50.md:229-235` item 7 "R11 stays routed"; QUALITY mentions R11 only inside 130/131 limits (`grep -n -E 'R11\|random' corpus/QUALITY.md` → `:1105,:1118,:1134`). No row, no lane tool arm. |
| 48-3d | r48 §5.3; r49 §5.7 | blinding handle must be random, not content-derived | OPEN | `round-50.md:229-235`: "The handle rule is **not met** this round … restated for round 51 as 'a blinding handle given to an instrument under test is random'". QUALITY 129 `:1105` carries only the "stay opaque while the variant bytes are unknown" limit. r51 and r52 closures and lessons do not mention it again (`grep -n -iE 'randomi[sz]e\|recomputable' corpus/lessons/round-5[12].md` → rc 1). The round-53 counters take no opaque-handle input, so the rule is dormant, not closed. |
| 48-3e | r48 §5.3; r49 §4 (M6) | unique seat names in wave 1 (attribution) | CAPTURED | `round-48.md:116` (M6, eight duplicate seat names); r49–r53 use the `Mo<NN>` prefix and distinct names (`ls .ufo/waves/round-53/w1/` → unique). No QUALITY row (`grep -n -iE 'unique seat\|seat name' corpus/QUALITY.md` → rc 1); the rule lives in the wave-spec convention. |
| 48-3f | r48 §5.3 | selftest arms from the three mutation seats | CAPTURED | `PIN_CHECK_SELFTEST` 60 → 114 → 125 (`evidence/selftests/mori-pin-check.txt`), `round-49.md:208` integrated merged witness and arms. |
| 48-4 | r48 §5.4; r49 §6; r50 §6; r51 §6 | SHONEN boxes all `[~]`, promotion operator-owned | OPERATOR | every closure repeats the note; none wrote `[x]`. |
| 49-b | r49 D-b | round shape short of the directive (49 seats vs 64–100; two seats with no report) | CAPTURED | `round-50.md` item 5 ("late, not dead", `Mo49SimpCounters.md` 23:02:40, `Mo49ExecCounterTiming.md` 23:39:03); `tools/mori-wave-settlement.py` exists (`ls` → present); r51 68 seats, r52 68 seats, r53 67 seats (`w1-spec.json` length 67). |
| 49-c | r49 D-c | erratum sat in the report (48 vs 47 reports); lesson and LOG kept the wrong number | CAPTURED | `round-50.md` item 3 ("48-vs-47 report count" correction entry in lesson and LOG round 50). No QUALITY row for the class (`grep -n -iE 'number-drift\|report count\|directory entries' corpus/QUALITY.md` → rc 1); QUALITY 77 ("a correction sweeps every mention in place", `:349`) covers it in principle. |
| 49-d | r49 D-d | selftest tallies prose-only, no committed output file | CAPTURED | QUALITY 134 `:1178` (every pin it corrects carries a committed receipt); `evidence/selftests/*.txt` in r50/r51/r52 (r53 `evidence/selftests/` is untracked at this read, still being written). |
| 49-e | r49 D-e | ~183 `.scratch/` dirs left | CAPTURED | = 48-1. |
| 49-f | r49 D-f | `variants=26` vs 27 `variant` lines | CAPTURED (explained, counter not changed) | `round-50.md` item 6 (`count-c1.py:305` `len(results) - 1`; 25 frozen edits + `real-opaque` + `real`). A frozen counter's convention, so a named limit, not a fix. |
| 49-g | r49 D-g / §3 nuance | lesson said the staged "six boots" capture "understates" the receipt | CAPTURED (correction by entry) | `round-50.md` item 8; `round-49.md:96` itself not edited by design. |
| 49-h | r49 §3 S486 disclosure | the S351 flip reads two daemon limit lines with `journalctl -g` (a MESSAGE filter), met only on the narrow reading | OPEN (LOW) | `round-49.md:129` records it. QUALITY 15 (`:29`, "never by message text") covers counting a journal class; `grep -n 'journalctl -g' corpus/QUALITY.md` → no hit. Not a kill-record grep, so the lane rule is not breached; whether a limit-line read by text conforms is undecided. |
| 49-i | r49 §5.7 | K4 and R11 carve-out; randomise the handle | = 48-3b / 48-3c / 48-3d | — |
| 50-b | r50 D-b / §5.2 | round over the 100-seat ceiling (104 across attempts); contract's wave shape not run; 35 attempt-1 seats with no report | CAPTURED (lesson), policy ROUTED | `round-51.md:143-148` ("outcome unknown, not dead"; two seat bands 64–100 vs 64–128). The r53 contract says `band 64–128 … Total ≤ 128` (`contract.md` Round shape) while the r50 closure's ceiling was 100; no lane text says which governs a residual call. r53 w1 is 67 seats, inside both. |
| 50-c | r50 D-c / §5.5 | frozen contract's considerthese suggestion not taken; deviation only in the lesson, not LOG | CAPTURED (lesson rule + LOG practice) | `round-51.md:204-213` item 5 (deviation named in LOG and lesson together); `LOG.md:2800-2801` names the r51 deviations; r52 LOG entry lists its routed-defect dispositions (`LOG.md:2837`). No QUALITY row (`grep -n -iE 'deviat' corpus/QUALITY.md` → rc 1). |
| 50-d | r50 D-d / §5.1; r51 §5.8 | an earlier closure not re-executable hermetically; instruments write inside the lane or hardcode the lane path | PARTLY → OPEN | Fixed: `tools/mori-pin-check.py` (`--scratch`, QUALITY 137 `:1254`), `round-40/conform.py` (`LANE = dirname(...)`). Still present at HEAD: `git grep -nE 'LANE *= *"/home\|mkdtemp\|/home/vgpnk/Projects/shokunin/mori-shokunin' HEAD -- .ufo/waves/round-38 … round-42 .ufo/waves/round-48/count-c1.py .ufo/waves/round-49/count-c1.py` → `round-38/conform.py:37` `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`, `:239` `mkdtemp(... dir=SCRATCH_ROOT)`, `round-38/count-c1.py:68` `DEFAULT_REPO = "/home/…/mori-shokunin"`, `:847` `mkdtemp`. QUALITY 137 Not-covered names them; QUALITY 127 (`:1070`, no absolute host path) states the rule and the count. `SCORECARD.md:2768` "Planned (round 53): the in-lane writers' successor freeze"; **the r53 contract carries no item for it** (`grep -nE -i 'conform\|writers\|successor' .ufo/waves/round-53/contract.md` → no hit). ROUTED, not scheduled. |
| 50-e | r50 §5.3 | successor C1 counter: verdict-word substring, second `## Axes`, Score column, vacuous `admitted`, symlinked pin | CAPTURED | `round-52/count-c1.py` (`C1_SELFTEST pass=42`); QUALITY 141, 142; r52 limits named: arm A `startswith`-pinned to `admitted`, receipts pure text (`SCORECARD.md` Round 52 "Limits"). QUALITY 134 `:1194` "Not covered: the Score column" stays. |
| 50-f | r50 §5.4 | entailment must be a committed step, not location alone | CAPTURED | QUALITY 140 (r51) and QUALITY 143 `:1379` (two non-author voters, supersedes 140's "Not covered" only); `round-52/count-c2.py` `C2_SELFTEST pass=45`. The r52 sweep's MED ("140's cell describes a counter that no longer exists") is closed by 143. |
| 50-g | r50 §5 routed 6; r49 D-a | operator-owned: `fleet-commit.sh:84-85` `jj metaedit --update-author` | OPERATOR | = 48-2. |
| 51-a | r51 D-a / §5.1 | `count-c1.py` had no `--selftest` | CAPTURED | `C1_SELFTEST pass=42`, `C2_SELFTEST pass=45` receipts (`round-52/evidence/selftest-c1.txt`, `selftest-c2.txt`); r53 counters ship selftests per the contract. |
| 51-b | r51 D-b / §5.7 | receipt command recorded as `--scratch <scratch>` placeholder | CAPTURED (counter receipts), LOW residue | r52 counter receipts print literal commands (`round-52.md` dispositions item 7 "every round-52 receipt records its literal command line", with `sweep-overcommit.txt` opening in prose, recorded LOW). `round-52/evidence/selftests/*.txt:1` read `cd <lane checkout at …>`: a placeholder, arguably the stated rule. r53 contract Frozen-bytes paragraph and the L1's receipts: UNVERIFIED here. |
| 51-c | r51 D-c / §5.5 | S493 locators in the lesson drifted (`:55-57` etc.) | CAPTURED | `corpus/lessons/round-51-erratum.md` §D-c (`ls corpus/lessons/*erratum*` → r37, r39, r51); `round-52.md:94`; `LOG.md:2837`. QUALITY 142 captures locator class only for SCORECARD/SHONEN pointers, not lesson prose: the erratum, not a criterion, carries it. |
| 51-d | r51 D-d / §5.5 | famzah attribution ("a reader's 2017 comment") | CAPTURED | `round-51-erratum.md` §D-d (author reply, lowercase repo name, `MemAvailable` 0 hits, sha256 recorded). |
| 51-e | r51 D-e / §5.6; r52 M4 | `round-40/conform.py` edited in place after the r40 freeze (`5025b966…` → `7f5174d5…`) | OPEN | `sha256sum .ufo/waves/round-40/conform.py` → `7f5174d5…`; `.ufo/waves/round-40/evidence/freeze-r40.txt:9` still pins `5025b966…`. `round-52.md` M4: "Captured-by: none (no QUALITY criterion forbids it yet); fix: round-53 successor-freeze design … and a QUALITY criterion candidate in `w1/Mo52ScoutMistakeSweep.md`". `grep -n -iE 'in place\|in-place\|copy-on-change\|successor.freeze' corpus/QUALITY.md` → `:349` (77), `:374`, `:799-810` (102, SOURCES rows only), `:918` (113, SOURCES anchors), `:1365` (141, living pins): **no row covers a frozen counter or instrument file**. The only carrier is `contract.md:8-9` ("a frozen file is never edited in place") and `round-52/contract.md`. The r53 contract does not take the criterion. |
| 51-f | r51 §5.2 | entailment arm hardening | CAPTURED | = 50-f (QUALITY 143). |
| 51-g | r51 §5.3; r52 limits | C1 counter survivors: 7 of 9 single-arm mutants keep every control verdict; M4/M8 survive; no control isolates one arm | ROUTED, deferred again | `round-52.md` Wave w1 findings ("named survivor mutants M4/M8 … limits for round 53"); `SCORECARD.md:2769` "Planned (round 53) … the C1 arm-isolating controls". The r53 contract says "this round's counters are new and inherit none of them" (Round-52 routed defects item 3) and its C1/C2 are new claims; `Mo53MutC1.md` exists in w1 as a probe of the new counter. No carrier for the r52 counter's survivors. |
| 51-op | r51 §6 | fleet-owned: `scripts/hyaku/inline-dispatcher.py:133` fails open on unreadable `/proc/meminfo`; `MEM_MIN_GB` is GiB; two floors 4 GiB vs 6144 MiB | OPERATOR | `round-51.md:296-297` ("routed to the operator"); `grep -n -E 'MEM_MIN_GB\|inline-dispatcher' corpus/QUALITY.md corpus/lessons/round-52.md PROVINCE.md` → rc 1 (nothing repeats it after r51); mori edits nothing there. |
| 52-D1 | r52 D1 | report lines carry `[FILL]` where the report's own commit hash belongs | ROUTED (this round) | `contract.md:115` and Round-52 routed item 2: the r53 report names its commit by `git log --format=%H -- .ufo/reports/round-53/mori.md` on the fleet repo, "never a placeholder", convention recorded in the lesson. `grep -n FILL /home/vgpnk/Projects/shokunin/.ufo/reports/round-52/mori.md` → `:5` (as a quoted placeholder in a sentence) and `:46` (`\| [FILL] \| receipts at landed tip …`). The filed r52 report cannot be edited; no erratum yet. No QUALITY row. Open until the r53 lesson lands. |
| 52-D2 | r52 D2 | SCORECARD Round 52 C1 row prints `items=42 … locators=27` and cites `c1-at-landed.txt` (`items=43 … locators=28`) | ROUTED (this round) | `SCORECARD.md:2746` still reads `items=42 … locators=27 … — evidence/c1-at-landed.txt`; `sed -n 2772,2800p SCORECARD.md` → empty, no correction line yet. `contract.md` Round-52 routed item 1: "an appended correction line naming the superseded text, this round". Counter evidence: `grep -rn 'items=42' .ufo/waves/round-52/evidence/*.txt` → `c1-at-data.txt:44` and three controls (the at-data tally). Open until the L1 appends it. QUALITY 142 (pointer on its words) covers the quoted-string class for Axes rows and SHONEN boxes only; a Round-N *claim table* cell is outside its arm. |
| 52-L1 | r52 §Routed 3 | locator arm covers only Axes rows and SHONEN boxes; QUALITY/README hold 78 more pointers | ROUTED | `SCORECARD.md` Round 52 "Limits" and `Planned (round 53)` item 2 ("the locator sweep beyond the Axes rows"); not in the r53 contract (its C1 is the v7.3 recheck, C2 the runway tool). |
| 52-L2 | r52 §Routed 3 | receipts are pure text (a handwritten receipt passes) | ROUTED | `SCORECARD.md` Round 52 "Limits". No carrier. |
| 52-L3 | r52 §Routed 3 | arm-A verdict pinned only to `admitted` (`startswith` mutant survived) | ROUTED | same; `contract.md` item 3 carries these in `Planned (round 54)`. |
| 52-op | r52 §Routed | MANIFEST pinned at `f0b61b4a`, later kama/kengaku appends only | NOT A DEFECT | closure notes provenance, no action. |

Counts (`awk` over the first word of the status cell): 37 rows = CAPTURED 20 (incl. LOW residues and the "CAPTURED, policy ROUTED" 50-b), ROUTED 6,
OPEN 4 (48-3c, 48-3d, 49-h, 51-e), PARTLY 1 (50-d: pin-check and round-40 conform fixed, round-38/39/41/42 writers open), OPERATOR 4
(48-2/50-g share a mechanism), NOT A DEFECT 1, alias 1 (49-i = 48-3b/c/d). The OPEN rows plus 50-d are the frontier candidates; see §3.

## 2. Commands (literal, from `/home/vgpnk/Projects/shokunin/mori-shokunin` unless stated; every grep returned rc 0 except those marked rc 1)

```
git rev-parse HEAD                                                         → 95cf78eef71979f9b740ef6bc3c5299b6beff86e
grep -n -iE 'in place|in-place|copy-on-change|successor freeze|successor-freeze' corpus/QUALITY.md   → :349 :374 :799 :801 :807 :810 :918 :923 :1365 (none about frozen counters)
grep -n -iE 'deviat' corpus/QUALITY.md                                       → rc 1
grep -n -E 'R11|random' corpus/QUALITY.md                                    → :1105 :1118 :1134
grep -n -iE 'author date|authored|author-date' corpus/QUALITY.md             → :260 :932 :938 :946 :1015 :1030 :1072 (all unrelated)
grep -n -iE 'number-drift|report count|directory entries' corpus/QUALITY.md  → rc 1
grep -rn -iE 'unique seat|seat name' corpus/QUALITY.md SKILL.md corpus/lessons/round-4[89].md corpus/lessons/round-5*.md → round-48.md:116, round-50.md:235
grep -n 'journalctl -g' corpus/QUALITY.md                                    → rc 1 (QUALITY 15 at :29 is the nearest)
grep -nE 'author date|author-date|metaedit|update-author' corpus/lessons/round-5[0-3].md LOG.md → round-50.md:201, round-51.md:226-232, LOG.md:2726,2758,2800
grep -nE -i 'conform|writers|successor|hermetic|survivor|M4|M8' .ufo/waves/round-53/contract.md  → rc 1 (none)
git grep -nE 'LANE *= *"/home|mkdtemp|/home/vgpnk/Projects/shokunin/mori-shokunin' HEAD -- .ufo/waves/round-38 .ufo/waves/round-39 .ufo/waves/round-41 .ufo/waves/round-42 .ufo/waves/round-48/count-c1.py .ufo/waves/round-49/count-c1.py → hits include round-38/conform.py:37,239 and round-38/count-c1.py:68,847
sha256sum .ufo/waves/round-40/conform.py | cut -c1-16                         → 7f5174d542bd9835
grep -n conform .ufo/waves/round-40/evidence/freeze-r40.txt                  → :9 5025b9664632d01063…
ls corpus/lessons/*erratum*                                                  → round-37-erratum.md round-39-erratum.md round-51-erratum.md
grep -n FILL /home/vgpnk/Projects/shokunin/.ufo/reports/round-52/mori.md     → :5 :46
sed -n 2744,2771p SCORECARD.md                                              → C1 row items=42 … locators=27, cites c1-at-landed.txt; "Planned (round 53)" paragraph
sed -n 2772,2800p SCORECARD.md                                              → empty (no correction line)
grep -rn 'items=42' .ufo/waves/round-52/evidence/*.txt                       → c1-at-data.txt:44 + three control receipts
git status --porcelain --ignored | grep -c '\.scratch'                        → 0
grep -n 'scratch' .gitignore                                                 → :5 .scratch/
git ls-files .ufo/waves/round-39/scratch | wc -l                             → 0
sed -n 990,1006p SKILL.md                                                    → "Still open: K4 … the fixtures/mutants carve-out of R11 …"
sed -n 1354,1379p corpus/QUALITY.md                                          → rows 141, 142, 143
ls tools/mori-wave-settlement.py tools/mori-unlanded-check.py                → both present
python3 -c 'json.load(open(".ufo/waves/round-53/w1-spec.json"))' (len)       → 67 items
```

## 3. Frontier input (suggestions for the L1, not counter changes)

Classes the rows share:

1. **A rule that lives in a lesson or a contract sentence only, with no QUALITY row**: never edit a frozen file in place
   (51-e), a contract deviation is named in LOG (50-c), unique seat names (48-3e), report-count drift (49-c), the
   report names its own commit by command (52-D1). Same shape as QUALITY 141 closes for pins: a row that supersedes by a
   later row, never rewriting. A candidate **row 144 — "a frozen instrument, counter, contract or control file is never
   edited in place; a change is a copy beside it plus a successor freeze line, and the old freeze line stays"**
   (carrier 51-e; shown able to fail: `sha256sum .ufo/waves/round-40/conform.py` → `7f5174d5…` against
   `freeze-r40.txt:9` → `5025b966…`; check: for every `freeze-*.txt` / `freeze-sha256.txt` line, the working file's
   sha256 equals the line or a later successor line names the file; Not covered: `controls/` data applied in a throwaway
   clone). The r52 lesson names this as its M4 "Captured-by: none"; r53 can land the criterion without touching the
   frozen file.
2. **Self-citation and numbers-vs-citation drift** (52-D1, 52-D2, 49-c, 49-f): each is a number or a hash written before
   the thing it cites existed. One row covering "a cell that cites a receipt carries the receipt's printed values, and
   a report names its own commit by command" would capture D1, D2 and the 48-vs-47 class at once; QUALITY 142's arm
   reads Axes rows and SHONEN only, so the Round-N claim tables are unarmed (named limit 52-L1).
3. **Routed, deferred twice**: in-lane writers' successor freeze (50-d), arm-isolating C1 controls (51-g), the locator
   sweep (52-L1): each appears in `Planned (round 53)` of the r52 SCORECARD and in no r53 contract item. The r53
   contract's considerthese suggestion (follow unfixed critic flags forward, `contract.md` §Frontier step) is the
   channel: the sweep above says which of these were "fixed, routed or silently dropped" at `20edafa5`. None was
   silently dropped (all five OPEN or ROUTED rows have a named line in `SCORECARD.md`/`SKILL.md`/lesson); none is
   scheduled with a claim.
4. **Ceiling ambiguity** (50-b): 100 (r50 closure) vs 128 (policy `waveMaxLanes`, r53 contract). A one-sentence LOG
   entry saying which governs a residual call settles it; r53's 67 seats do not test it.

## Findings

- **MED** — `corpus/QUALITY.md` (no row): no criterion forbids editing a frozen instrument file in place; `.ufo/waves/round-40/conform.py` sha256 `7f5174d5…` vs `.ufo/waves/round-40/evidence/freeze-r40.txt:9` `5025b966…` (51-e). `corpus/lessons/round-52.md` M4 says "Captured-by: none"; candidate row 144 in §3. The r53 contract does not take it.
- **MED** — `SCORECARD.md:2746` (and `LOG.md` round 52): the Round 52 C1 row prints `items=42 … locators=27` and cites `evidence/c1-at-landed.txt` (`items=43 … locators=28`); no correction line exists after `SCORECARD.md:2771` (52-D2). Contract item 1 owes it this round.
- **MED** — `corpus/lessons/round-50.md:229-235`, `corpus/QUALITY.md:1105` (49-i / 48-3d): "a blinding handle given to an instrument under test is random" was restated for round 51 and never taken; r51/r52 lessons do not mention it; QUALITY 129 carries only the "opaque while variant bytes are unknown" limit.
- **MED** — `SKILL.md:1002` (48-3c): R11 `fixtures/mutants` carve-out still listed "Still open"; no QUALITY row; routed since r49.
- **MED** — `.ufo/waves/round-38/conform.py:37,239` and `.ufo/waves/round-38/count-c1.py:68,847` (50-d): hardcoded lane path and `mkdtemp` still present in the in-lane writers; `SCORECARD.md:2768` plans a successor freeze for round 53 but `contract.md` has no item for it. ROUTED a second time.
- **MED** — `SCORECARD.md:2769` (51-g): arm-isolating C1 controls and M4/M8 survivors deferred a second time; `contract.md` states the r53 counters "inherit none of them".
- **LOW** — `/home/vgpnk/Projects/shokunin/.ufo/reports/round-52/mori.md:5,46` (52-D1): `[FILL]` self-citation in a filed report; only the forward convention (r53 names its commit by command) exists, no erratum, no QUALITY row.
- **LOW** — `SCORECARD.md` Round 52 "Limits" (52-L1..L3): locator arm covers Axes rows and SHONEN boxes only (78 pointers unarmed), receipts are pure text, arm-A verdict pinned to `admitted`; ROUTED to `Planned (round 54)` per `contract.md`.
- **LOW** — `corpus/lessons/round-49.md:129` (49-h): reading limit lines with `journalctl -g`; QUALITY 15 (`:29`) leaves a limit-line read by MESSAGE text undecided.
- **LOW** — `contract.md` Round shape vs `corpus/lessons/round-51.md:143-146` (50-b): ceiling 128 vs 100 unresolved for a residual call.
- **LOW** — `corpus/QUALITY.md` (no row) for deviation-named-in-LOG (50-c), unique seat names (48-3e), report-count drift (49-c): the rules live in lessons/LOG practice; captured in practice, not by criterion.
- **LOW** — `round-52/evidence/selftests/*.txt:1` (51-b): `cd <lane checkout at …>` placeholder command lines.
- **OPERATOR (no lane fix)** — `scripts/hyaku/fleet-commit.sh:84-85` author date (48-2); SHONEN promotion (48-4); `scripts/hyaku/inline-dispatcher.py:133` fail-open / `MEM_MIN_GB` GiB / two floors (51-op, not repeated in the r52 record).
- **INFO** — zero admit/reject disagreements across rounds 48–52 (§0); all 31 discernment rows read `agree` (r49 one nuance, r48 one "unprovable to differ").
