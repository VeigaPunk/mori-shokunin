# Mo52ScoutMistakeSweep — verifier-spotcheck sweep, rounds 47–51

Seat: Mo52ScoutMistakeSweep (scout, round 52 wave w1). Read-only. Read: `contract.md`, the five closures
`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-47-verifier-spotcheck.md` … `round-51-verifier-spotcheck.md`,
`corpus/QUALITY.md` 123–142, the lesson `### Spot-check` / dispositions sections of rounds 48–51, `LOG.md` Round 51, round-52
evidence. Scratch `/fast/scratch/hyaku/mori-r52/Mo52ScoutMistakeSweep/` (only an empty `tmp/`; removed at the end). Line
numbers are at lane tip `075436b1` (data `8524904a`) unless stated. `grep` found no LSP; text search is the only
method and shows presence of a pointer, not that it works.

Disagreements: the five closures record **no admit/reject disagreement** with the lane (every §3 row reads `agree`; the
nearest are r49 `agree, one nuance` on the staged `reach-per-journal` reject, and r47 `not re-opened`). What they route
are conformance defects (D-x), counter limits and wording errors. Those are the rows below.

Reading key: CAPTURED (pointer) = a QUALITY row, a lesson fix/erratum, a tool or a frozen-instrument arm carries it and
the pointer was seen; OPEN = nothing seen carries it (routed or not); OPERATOR = fleet-owned, outside the lane.

## 1. Defect table

| # | closure item | defect (one line) | status | pointer / evidence |
|---|---|---|---|---|
| 47-1 | r47 §1, §5.1 | 53 untracked round paths at the tip; report's seat count not what the repo held | CAPTURED | `round-48.md:98-99` ("committed in `356fb94a`, LOG erratum, `tools/mori-unlanded-check.py`"); `tools/mori-unlanded-check.py` exists, receipt `evidence/selftests/mori-unlanded-check.txt` `UNLANDED_SELFTEST pass=17 fail=0`. No QUALITY row names the rule (§3 below). |
| 47-2 | r47 §5.2 | report filed after the driver `complete` line | CAPTURED (lesson), recurred as 48-b | `round-48.md:99-100`; r48 C-line 20:27:04 < 20:27:28 reads fixed in the r48 closure §1; then became the author-date class (48-b). |
| 47-3 | r47 §5.3 | lane's own routes: successor C2 (used-by arm, 0–3-space rows, one path per cell), selftest arms (symlink, argv, case-insensitive unparsed), line-count/truncated-digest pins, F4 precision | CAPTURED | `round-48.md:100-104` (disposition: "realised in `count-c2.py` … v3 rules R5/R6"); QUALITY 125, 128. F4 citation precision: no pointer seen → **OPEN (LOW)**. |
| 47-4 | r47 §5.4 | lesson `## Spot-check` said none exists yet | CAPTURED | `round-48.md:96` cites the file; the section now exists in 48–52. |
| 47-5 | r47 §5.5 | S478 refetch needs a browser User-Agent; row's recheck must say so | CAPTURED (lesson only) | `round-48.md:14,32,74,82`. Not in the SOURCES row: `grep -n 'Mozilla\|User-Agent' corpus/SOURCES.md` → rc 1 (no hit). The row cannot be edited (append-only, QUALITY 102); a superseding row carries it if ever re-opened → **LOW**. |
| 48-a | r48 §5.1 / D-a | 114 untracked `.scratch/*`; `.scratch` outside the unlanded check | CAPTURED | `.gitignore:5` `.scratch/`; r50 deleted them (`round-50.md:219-227` item 4); producers: pin-check fixed (QUALITY 137, `evidence/selftests/mori-pin-check.txt` pass=125), round-40 `conform.py` fixed (`round-51.md`, LOG 2796-2798). |
| 48-b | r48 §1(b), r49 D-a, r50 D-a, r51 §5.6 | report commit **author** date earlier than the lane tip it cites | OPERATOR | `round-50.md:199-205` item 1 (landing comparison rule) and `round-51.md:226-232` item 6 ("Routed to the operator, unchanged"). Fleet-owned `scripts/hyaku/fleet-commit.sh:84-85`. No QUALITY row, no lane tool; the lane's only control is the comparison it records in the report. OPEN for the lane, expected. |
| 48-c | r48 §5.3 | seven v3 survivors, K2–K8, R11, successor counter hiding variant identity, unique seat names | CAPTURED (mostly) | QUALITY 129 (opaque handle), 130 (renders-as-row), 131 (bound pin); `round-49.md:176-181`. R11 carve-out and randomised handle: `round-50.md:229-235` item 7 says "R11 stays routed", handle "**not met**", restated for r51; no later row seen → **OPEN (MED)**: `grep -rn 'R11' corpus/QUALITY.md` hits only 130/131 limits. |
| 48-d | r48 §5.4 / r49 D-… | SHONEN boxes not checkable by a non-author | OPERATOR | `round-49.md:180-181` "operator-owned, unchanged"; every closure repeats the note, none claims `[x]`. |
| 49-b | r49 D-b | round shape short of the directive (49 seats vs 64–100; two seats with no report) | CAPTURED | `round-50.md:208-218` item 5 ("late, not dead"); `tools/mori-wave-settlement.py` (r50 M3 reports shape only); r51 68 seats (`round-51.md` Round shape). |
| 49-c | r49 D-c | erratum sat in the report (48 vs 47 reports); lesson and LOG kept the wrong number | CAPTURED | `round-50.md` M2 `number-drift`, item 3 (correction entry in lesson and LOG round 50). Class has no QUALITY row: `grep -n -iE 'report count\|directory entries\|number-drift' corpus/QUALITY.md` → rc 1 (QUALITY 77 "a correction sweeps every mention" is the nearest and does cover it in principle). |
| 49-d | r49 D-d | selftest tallies pinned in prose with no committed output file | CAPTURED | QUALITY 134 ("every pin it corrects carries a committed receipt"); `evidence/selftests/*.txt` in r50/r51/r52 (r52 `mori-pin-check.txt` pass=125, unlanded pass=17). |
| 49-e | r49 D-e | `.scratch/` debris, ~183 dirs | CAPTURED | same as 48-a. |
| 49-f | r49 D-f | `variants=26` vs 27 `variant` lines | CAPTURED (explained, not fixed) | `round-50.md:220-225` item 6 (`len(results) - 1`, `count-c1.py:305`); counter frozen, so the off-by-one is a named limit, not a code fix. |
| 49-g | r49 D-g, §3 nuance | lesson said the staged "six boots" capture "understates" the receipt | CAPTURED (erratum-by-entry) | `round-50.md:236-240` item 8; `round-49.md:96` itself not edited (by design). |
| 49-h | r49 §3 S486 disclosure | the receipt obtained limit lines with `journalctl -g` (a MESSAGE filter), so S351's flip is met only on the narrow reading | OPEN (LOW) | `round-49.md:129` records it; QUALITY 15 (`:29`, "never by message text") is about counting a journal *class*; no lesson or row says whether a limit-line read by text conforms. `grep -n 'journalctl -g' corpus/QUALITY.md` → no hit. Not a kill-record grep, so the lane rule is not breached; the boundary is undecided. |
| 49-i | r49 §5.7 | K4 and R11 carve-out open; blinding handle must be random | PARTLY | K4 → this round's C1 arm (C) (QUALITY 141, contract). R11 and "handle is random": see 48-c, OPEN. |
| 50-b | r50 D-b / §5.2 | round over the 100-seat ceiling (104 across attempts); contract's planned wave shape not run; 35 attempt-1 seats with no report | CAPTURED (lesson), policy disagreement OPEN | `round-51.md:143-146` (68 seats, "two seat bands … `:121-122` 64–100 vs `:129` 64–128"). `round-52/contract.md:117-120` states "band 64–128 … Total ≤ 128", while the r50 closure's ceiling is 100; `scripts/hyaku/ufo-wave-policy-v2.json` `waveMaxLanes=128`. No lane text says which governs a residual call → **OPEN (LOW)**; r52 w1 is 68 seats, inside both. |
| 50-c | r50 D-c / §5.5 | frozen contract's considerthese suggestion not taken, deviation only in the lesson, not in LOG | CAPTURED | `round-51.md:204-213` item 5 (rule: deviation named in LOG and lesson together); `LOG.md:2802-2806` names the r51 deviations. No QUALITY row: `grep -n -iE 'deviation' corpus/QUALITY.md` → rc 1 → rule lives in a lesson only (LOW). |
| 50-d | r50 D-d / §5.1 | earlier closure not re-executable hermetically; `round-40/conform.py` writes inside the lane | CAPTURED for pin-check and `round-40/conform.py`; **OPEN** for the rest | QUALITY 137 + `round-51/count-c1.py`. Remaining writers: round-38/39/41/42 `conform.py` (`LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"` at `round-38/conform.py:37`, `mkdtemp` `round-38/conform.py:239`) and round-48/49 `count-c1.py` — stated in QUALITY 137 Not covered (`:1279-1281`) and `LOG.md:2800-2802`; inventory seat `Mo52ExecWritersConform` has not written a report yet (file absent at this read). Fix routed; editing the files is what §5 item 6 forbids → successor-freeze design is the open piece. |
| 50-e | r50 §5.3 | successor C1 counter (verdict substring, second `## Axes`, Score column, vacuous `admitted`, symlinked path), K4 | CAPTURED | `round-52/count-c1.py` (selftest pass=42, `evidence/selftest-c1.txt`); QUALITY 141, 142; contract C1. Limits named in contract. |
| 50-f | r50 §5.4 | entailment must be a committed step | CAPTURED | QUALITY 140 (r51) and, for the hardened arm, `round-52/count-c2.py` (selftest pass=45, `evidence/selftest-c2.txt`). **QUALITY 140's Not-covered cell (`:1349-1351`: "one `entailed` vote meets the arm", non-voter and fenced lines count) is now false for r52's arm and no later row supersedes it** — contract-only pointer (`contract.md:65-69`). OPEN (MED): no QUALITY row 143 for the two-non-author-voter rule; the criterion text stands but its limit paragraph describes the r51 counter. |
| 51-a | r51 D-a / §5.1 | `count-c1.py` has no `--selftest` | CAPTURED | `count-c1.py` and `count-c2.py` ship `--selftest` (`grep -c -- '--selftest'` → 22 / 3); receipts `evidence/selftest-c1.txt` (`C1_SELFTEST pass=42 fail=0`, exit 0), `selftest-c2.txt` (`pass=45`). |
| 51-b | r51 D-b / §5.7 | receipt recorded `--scratch <scratch>` placeholder | CAPTURED for counter receipts; **OPEN (LOW)** for two | r52 receipts record literal commands (`c1-at-data.txt:1`, `c2-at-data.txt:1`, `control-c1-do-nothing.txt:2` with `/fast/scratch/hyaku/mori-r52/l1/…`). But `evidence/selftests/mori-pin-check.txt:1` and `mori-unlanded-check.txt:1` read `$ cd <lane checkout at d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2> && python3 tools/…` — a placeholder, not a literal path. The item 7 ask ("record the actual `--scratch` path, or a reproducible placeholder rule stated in the receipt") — the rule is stated in the line itself (checkout at a named rev), so arguably met; worth one sentence. |
| 51-c | r51 D-c / §5.5 | lesson's S493 locators drift (`:55-57`, `:62`, `:67-69`, `:71-72` should be 54-55, 56, 64-66, 69-70) | OPEN (in flight) | `ls corpus/lessons/*erratum*` → `round-37-erratum.md`, `round-39-erratum.md` only; `round-51-erratum.md` does not exist. `Mo52ScribeErratum51.md` holds a draft (re-derived mapping 55-57→54-55, 62→56, 67-69→64-66, 71-72→69-70) for the L1 to integrate. QUALITY 142 captures the locator class only for SCORECARD/SHONEN, not lesson prose. |
| 51-d | r51 D-d / §5.5 | famzah attribution ("a reader's 2017 comment" is the blog author's reply; hit is the lowercase repo name) | OPEN (in flight) | same draft; not yet in `corpus/lessons/`. |
| 51-e | r51 D-e / §5.6 | `round-40/conform.py` edited in place after the r40 freeze (`5025b966…` → `7f5174d5…`) | PARTLY | `round-51.md` Wave w1 bullet ("Round-40 freeze") discloses it; `round-52/contract.md:109-110` "this round edits none"; `w1/Mo52ConnCrossClaim.md:102-104,148` still reports it MED. No QUALITY row says "a frozen file is never edited in place": the rule is a contract sentence (`contract.md:8-9`) only; `grep -n 'copy-on-change\|successor freeze' corpus/QUALITY.md` → rc 1. OPEN (MED). |
| 51-f | r51 §5.2 | entailment arm: ≥2 non-author votes, unfenced, ENTAILMENT voters | CAPTURED in counter | `contract.md:65-69`, selftest controls; see 50-f for the QUALITY-text gap. |
| 51-g | r51 §5.3 | C1 counter survivors (7 of 9 single-arm mutants keep every control verdict) | OPEN (routed to r53) | `round-51.md` Named limits; r52 contract: "wave mutation seats name each arm-isolating control, recorded as limits and routed". The r52 control set (`control-c1-*.txt`, 8 receipts) is still not arm-isolating by construction for A–D; limit stays. |
| 51-h | r51 §5.4 | successor C1 + K4 | CAPTURED | = 50-e. |
| 51-i | r51 §5.8 | remaining in-lane writers (round-38/39/41/42 `conform.py`, round-48/49 `count-c1.py`) — hermeticity sweep | OPEN (assigned this wave) | = 50-d; inventory seat has no report at this read. |
| 51-op | r51 §6 | fleet-owned dispatcher findings (`scripts/hyaku/inline-dispatcher.py:133` fails open on unreadable `/proc/meminfo`; `MEM_MIN_GB` is GiB; two floors 4 GiB vs 6144 MiB) | OPERATOR | `round-51.md` Named limits ("routed to the operator"); `grep -n 'MEM_MIN_GB\|inline-dispatcher' corpus/QUALITY.md PROVINCE.md corpus/lessons/round-52.md` → rc 1, nothing in the round-52 record repeats it; mori edits nothing there. |

## 2. Commands used (literal, from `/home/vgpnk/Projects/shokunin/mori-shokunin`)

```
grep -rn -iE 'author date|authored|author-date' corpus/QUALITY.md corpus/lessons/round-4[89].md corpus/lessons/round-5[12].md
grep -n -iE 'untracked|\.scratch' corpus/QUALITY.md
grep -n -iE 'untracked|\.scratch|unlanded' corpus/lessons/round-48.md corpus/lessons/round-49.md corpus/lessons/round-50.md
grep -n -iE 'unlanded|\.scratch' .gitignore                          # :5 .scratch/
grep -n -E 'browser UA|User-Agent|Mozilla' corpus/SOURCES.md corpus/lessons/round-48.md corpus/QUALITY.md
grep -n -E 'S351' corpus/QUALITY.md corpus/lessons/round-50.md corpus/lessons/round-51.md
grep -n -E 'journalctl -g|-g ' corpus/lessons/round-49.md corpus/lessons/round-50.md corpus/QUALITY.md
grep -n -E '^ *15\.' corpus/QUALITY.md                               # :29 never by message text
grep -n -iE 'ceiling|seat band|64.128|100 seat|seat count' corpus/QUALITY.md corpus/lessons/round-51.md
grep -n -iE 'report count|directory entries|number-drift' corpus/QUALITY.md       # rc 1
grep -n -iE 'in place|in-place|copy-on-change|successor freeze' corpus/QUALITY.md
grep -n -iE 'deviation|deviat' corpus/QUALITY.md                       # rc 1
grep -n -iE 'two seats|two voters|distinct voter|did not write' corpus/QUALITY.md  # :1350 only
grep -n -E 'entailed|ENTAIL|voter' corpus/QUALITY.md                  # 1335-1350 only (QUALITY 140)
grep -n -E 'MEM_MIN_GB|inline-dispatcher' corpus/QUALITY.md corpus/lessons/round-52.md PROVINCE.md  # rc 1
grep -n -E 'round-4[789]-verifier-spotcheck|round-5[01]-verifier-spotcheck' corpus/QUALITY.md       # :1331 only
ls corpus/lessons/*erratum*                                           # r37, r39 only
grep -c -- --selftest .ufo/waves/round-52/count-c1.py .ufo/waves/round-52/count-c2.py            # 22, 3
head -2 .ufo/waves/round-52/evidence/{selftest-c1,selftest-c2}.txt  # literal commands; pass=42, pass=45
head -2 .ufo/waves/round-52/evidence/selftests/*.txt                 # "cd <lane checkout at …>" placeholder
git grep -n -E 'mkdtemp|LANE *=|/home/vgpnk/Projects/shokunin/mori-shokunin' 8524904a -- .ufo/waves/round-38 .ufo/waves/round-39 .ufo/waves/round-41 .ufo/waves/round-42 .ufo/waves/round-48/count-c1.py .ufo/waves/round-49/count-c1.py
python3 -c '…json…' scripts/hyaku/ufo-wave-policy-v2.json            # waveMinLanes 64, waveMaxLanes 128
```
Exit codes: every `grep` above returned 0 except those marked `rc 1` (no match); `ls`, `git grep` rc 0. No lane gate was
executed; nothing was written outside this report and the scratch dir.

## 3. Cross-cutting observation (frontier input)

Of the 30 table rows, the recurring classes are: (1) fleet-owned author date (48-b) — operator; (2) a rule that lives
in a lesson or a contract sentence only and has no QUALITY row: deviation-named-in-LOG (50-c), never-edit-a-frozen-file
(51-e), the late/untracked-file landing rule (47-1: a tool exists, no criterion cites it), round-count drift (49-c);
(3) a living criterion whose Not-covered cell is stale after a counter hardening (QUALITY 140, now describing a
counter that no longer exists); (4) an erratum in flight that has not landed (51-c, 51-d). Items (2)–(3) are the
same class QUALITY 141 closes for command-tally pins (supersession by a later row, never rewrite); a row 143
superseding 140's Not-covered cell and carrying 51-e/50-c would close them without touching a frozen file. This is a
suggestion for the L1, not a counter change.

## Findings

- **MED** — `corpus/QUALITY.md:1349-1351` (QUALITY 140 "Not covered") still says one `entailed` vote meets the arm, any `.md` can vote and fenced lines count; `round-52/count-c2.py` now needs two non-author ENTAILMENT voters, unfenced. No later row supersedes it (51-f / 50-f). Supersede, never rewrite (QUALITY 141 rule).
- **MED** — no QUALITY criterion forbids editing a frozen file in place; only `contract.md:8-9` and the r51 closure §5.6 say it; `round-40/conform.py` (`7f5174d5…` vs freeze `5025b966…`) still diverges and `w1/Mo52ConnCrossClaim.md:148` repeats it (51-e).
- **MED** — R11 carve-out and the "blinding handle is random" rule (49-i / 48-c) are routed since r49 with no row; r50 item 7 says "not met", r51 never took it up.
- **MED** — in-lane writers outside C1 (round-38/39/41/42 `conform.py` e.g. `.ufo/waves/round-38/conform.py:37,239`, round-48/49 `count-c1.py`) stay open: inventory seat has no report; the fix needs a successor-freeze design (50-d / 51-i).
- **MED** — round-51 erratum for D-c (locators) and D-d (famzah) does not exist in `corpus/lessons/` (`round-51-erratum.md` absent at this read); draft is in `w1/Mo52ScribeErratum51.md`; until the L1 lands it both defects are OPEN.
- **LOW** — 51-b: `evidence/selftests/mori-pin-check.txt:1` and `mori-unlanded-check.txt:1` record `cd <lane checkout at d3a8ea59…> && …`, a placeholder, not a literal path.
- **LOW** — 50-b: contract says band 64–128/≤128 while the r50 closure's ceiling is 100 and `ufo-wave-policy-v2.json` `waveMaxLanes=128`; no lane text says which governs a residual call.
- **LOW** — 50-c: deviation-named-in-LOG rule exists only in `corpus/lessons/round-51.md:204-213`; no QUALITY row.
- **LOW** — 49-h: `corpus/lessons/round-49.md:129` reads daemon limit lines with `journalctl -g` (MESSAGE text); QUALITY 15 (`:29`) covers counting a class, not reading a limit line; undecided boundary, not a kill-record grep.
- **LOW** — 47-3 F4 citation precision and 47-5 S478 browser-UA recheck: carried in lessons only; S478 row cannot be edited (append-only).
- **LOW** — 51-g: the C1 control set is still not arm-isolating (named limit, routed to round 53).
- **LOW** — OPERATOR items with no lane fix: author date (48-b), SHONEN promotion (48-d), `inline-dispatcher.py:133` / `MEM_MIN_GB` (51-op); nothing in the round-52 record repeats the dispatcher item.
