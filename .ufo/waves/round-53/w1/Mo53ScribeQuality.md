# Mo53ScribeQuality — QUALITY.md drafts from 144 (four criteria, fenced)

Seat: scribe. Task: draft the round-53 admission criteria from 144 onward in the house style of
`corpus/QUALITY.md` (Lesson / Rationale / Check / Shown able to fail / Not covered), one per item:
(a) a `recheck: on-release` entry answered by a recheck ledger (C1); (b) a runway verdict that names the
enforcement mode and the error band (C2); (c) a SCORECARD row whose numbers are the numbers of the receipt it
cites (round-52 D2); (d) a report that never carries a placeholder where its own commit belongs (round-52 D1).

Tree read: lane work tree at `95cf78ee` (`git log --oneline -3` → `95cf78ee` wave spec, `2a4213bf` data,
`f4da3fd4` freeze). `corpus/QUALITY.md` ends at criterion 143 on line 1379, so the drafts start at 144. I wrote
only this report; nothing under `corpus/`, `tools/`, `.ufo/waves/round-53/` (except this file) or any PATH
directory was written. Scratch `/fast/scratch/hyaku/mori-r53/Mo53ScribeQuality/` was created, used and removed
(§6). No tool was installed or upgraded; no pacman transaction was run. Host reads only (`/proc` was read by the
tool itself, not by me).

## 1. House style taken from the tail of QUALITY.md

`wc -l corpus/QUALITY.md` → `1379`; `grep -n '^1[4-9][0-9]\.\|^## ' corpus/QUALITY.md | tail -40` ends with
`1354:## Criteria added round 52 — a living pin is current or superseded, and a self-assessment pointer lands on
its words`, `1356:141.`, `1368:142.`, `1379:143.`. Shape of 141–143: bold lead sentence; `Lesson:` naming the
round mistake and its carrier; `Rationale:`; `Check:` with literal commands and the exact line they print;
`Shown able to fail:` naming a committed receipt or a live reading; `Not covered:` naming what the check does
not prove. Each cites its counter by path and its receipt under `.ufo/waves/round-<N>/evidence/`.

## 2. Evidence I read for the drafts (no re-execution of committed work)

| item | source read | what it says |
|---|---|---|
| C1 at data | `.ufo/waves/round-53/evidence/c1-at-data.txt` | `C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2 holds=46 changed=0 voted=0 dissent=0 rev=2a4213bf… failed=votes`, `exit=1` |
| C1 do-nothing | `evidence/control-c1-do-nothing.txt` | `rows=0 … source_rows=bad pins=bad provenance=bad … failed=ledger_absent,pins`, exit 1, at `20edafa5` |
| C1 all-held | `evidence/control-c1-all-held.txt` | `status_ok=44 quote_ok=44 … held=44 absent=2 holds=46 … voted=46 … failed=quote,status`, exit 1 |
| C1 v72-copies | `evidence/control-c1-v72-copies.txt` | `status_ok=44 quote_ok=44 … pins=bad … held=46 absent=0 … failed=pins,quote,status`, exit 1 |
| C1 no-votes | `evidence/control-c1-no-votes.txt` | `status_ok=46 quote_ok=46 … voted=0 … failed=votes`, exit 1 (the data-commit shape) |
| C1 selftest | `evidence/selftest-c1.txt` | `C1_SELFTEST pass=37 fail=0`, exit 0 (arms include `author_vote_not_counted_unmet`, `fenced_votes_unmet`, `dissent_unmet`, `revised_dissent_met`) |
| C2 at data | `evidence/c2-at-data.txt` | `C2=met tool=present selftest=pass n=23 fixtures=80 agree=80 disagree=0 registry=ok live=ok`, exit 0 |
| C2 mode-blind | `evidence/control-c2-mode-blind.txt` | `agree=53 disagree=27`, exit 1, `selftest=pass n=12` |
| C2 no-band | `evidence/control-c2-no-band.txt` | `agree=71 disagree=9`, exit 1, incl. `mode2-band-edge-low want=COMMIT_LOW got=COMMIT_OK` |
| C2 memoriser | `evidence/control-c2-memoriser.txt` | `agree=71 disagree=9`, exit 1, `selftest=pass n=12` |
| C2 selftest | `evidence/selftest-c2.txt` | `C2_SELFTEST pass=30 fail=0`, exit 0 |
| tool selftest | `evidence/selftests/mori-commit-runway.txt` | `MATCHER: rejected 23/23 corrupted expectations` / `MORI_COMMIT_RUNWAY_SELFTEST: PASS 23/23`, exit 0, run from a `git archive` of `2a4213bf` |
| ledger | `corpus/knowledge/kernel-v7.3-recheck-r53.md` | `source:` S502–S510, `verified-at: 2026-10-26`, one `recheck: on-release` line (line 13) that states the next-tag procedure; header `| h | entry | status | source | quote | disposition |`; 46 data rows; 44 `held`, 2 `absent` (`0fbd62f51ce8`, `d7a1dc88dcb3`, both `mm/mmap.c`), 46 `| holds |`, 0 `| changed |`; title says "two quotes respelled" |
| tag trigger | `evidence/sweeps.txt:19` | `c03c1a14507dfaf8b856c2608f9ac216021fc222  refs/tags/v7.3^{}` (line 18: tag object `091b0638…`) |
| pins | `grep -c 'recheck: on-release'` on both round-51/52 entries | `1` each — the promise is one provenance line per entry, not per row |
| C2 entry | `corpus/knowledge/commit-runway-read-r53.md` | `source:` S499 (round 52), S511–S513; 7-row claims table; band paragraph (`usable_kb`, `band_kb`, `COMMIT_LOW` inside the band) |
| SKILL row | `SKILL.md:1178` (`## Round53`), `SKILL.md:1208` | registry row naming `tools/mori-commit-runway.py [--selftest …]`, exits `0/1/2`, selftest `PASS 23/23`, fixtures `cases.json` (23 cases) |
| D2 | `SCORECARD.md:2746` vs `evidence/c1-at-landed.txt` | row after-cell `items=42 … locators=27`, cited receipt `items=43 … locators=28`; the same tokens equal `c1-at-data.txt` (42/27, measured `8524904a`) |
| D1 | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-52/mori.md:5,46` | line 5 `… Report commit `[FILL]`.`; line 46 `| `[FILL]` | receipts at landed tip: …`; `git log --format=%H -- .ufo/reports/round-52/mori.md` → `aacd7a83027cdee8e950a2c39d490feaed3be13c` |

Checks I ran myself (so that every Check cell in the drafts is a command I have executed at least once):

```
$ python3 -I -B tools/mori-commit-runway.py                       # lane work tree, host defaults
{"band_kb": null, "batch_pages": null, "commit_limit_kb": 47583772, "committed_as_kb": 41147900,
 "cpus_present": 32, "enforced": false, "findings": [], "headroom_kb": 6435872, "limit_consistent": true,
 "limit_recomputed_kb": 47583772, "mode": 0, "notes": ["mode 0 (guess): … CommitLimit is printed, not
 enforced"], "reserve_kb": null, "schema": "mori-commit-runway-v1", "single_request_cap_kb": 63444672,
 "usable_kb": null, "verdict": "COMMIT_HEURISTIC"}
exit=0
```

```
# band-edge pair materialised from tools/fixtures/mori-commit-runway/cases.json into my scratch, then:
$ python3 -I -B tools/mori-commit-runway.py --meminfo …/mode2-band-edge-equal-is-low/meminfo \
    --vm-dir …/mode2-band-edge-equal-is-low/vm --cpu-present …/present --page-kb 4
### mode2-band-edge-equal-is-low exit= 1
{"verdict": "COMMIT_LOW", "mode": 2, "enforced": true, "usable_kb": 32768, "band_kb": 32768,
 "batch_pages": 256, "cpus_present": 32, "commit_limit_kb": 4194304, "committed_as_kb": 4022272}
expect_verdict= COMMIT_LOW expect_exit= 1 expect_usable= 32768 expect_band= 32768
### mode2-band-edge-one-page-above exit= 0
{"verdict": "COMMIT_OK", "mode": 2, "enforced": true, "usable_kb": 32772, "band_kb": 32768,
 "batch_pages": 256, "cpus_present": 32, "commit_limit_kb": 4194304, "committed_as_kb": 4022268}
expect_verdict= COMMIT_OK expect_exit= 0 expect_usable= 32772 expect_band= 32768
```

```
$ n=2746; row=$(sed -n "${n}p" SCORECARD.md); rec=$(printf '%s' "$row" | grep -o 'evidence/[a-z0-9-]*\.txt' | tail -1)
row=2746 receipt=evidence/c1-at-landed.txt
items row=42 receipt=43 mismatch
locators row=27 receipt=28 mismatch
# same loop against .ufo/waves/round-52/evidence/c1-at-data.txt: row=42 receipt=42, row=27 receipt=27
$ grep -nE 'Report commit `?\[FILL\]|^\| `\[FILL\]` \|' .ufo/reports/round-52/mori.md     # fleet repo
5:… Report commit `[FILL]`.
46:| `[FILL]` | receipts at landed tip: `c1-at-landed.txt`, `c2-at-landed.txt`, `census-end.txt` | Round 52 |
$ grep -n 'count-c1.py R' SCORECARD.md | tail -1 | cut -d: -f1
2746          # today the last C1 row; after integration it is the round-53 row
```

`ROUND=52` in the loop reproduced the mismatch; the round-53 instantiation cannot be run until the L1 lands the
round-53 row and its landed receipt (see §5).

## 3. Draft — four criteria, for insertion after 143 (fenced; nothing outside this block was edited)

```markdown
## Criteria added round 53 — a release recheck answers a pin, a runway verdict names its mode and band, a scorecard row matches the receipt it cites, a report names its own commit

144. **An entry whose claim rows pin a tag and whose provenance line says `recheck: on-release` is answered by a
    recheck ledger once a newer tag exists: one row per claim hash, the counter-derived status, a quote located in
    the new tag's copy, a disposition, and two votes that did not propose that row's quote.** Lesson: round-53 C1
    (the round-51 and round-52 entries pin 46 of their 49 claim rows to v7.2 files and each carries one
    `recheck: on-release` line; `evidence/sweeps.txt:19` reads `refs/tags/v7.3^{}` → `c03c1a14507d…`, so the
    trigger fired with no answer in `corpus/knowledge`). Rationale: a `recheck: on-release` line is a promise the
    entry makes about itself; without a ledger the promise is prose, and a reader of the round-51/52 tables cannot
    tell a quote that still holds from one the release respelled. Check: `python3 .ufo/waves/round-53/count-c1.py
    <R>` exits 0 and prints `C1=met scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok
    provenance=ok … voted=46 dissent=0`; the ledger `corpus/knowledge/kernel-v7.3-recheck-r53.md` carries the same
    next-tag procedure on its own `recheck:` line (line 13), so the entry that answers one trigger states how the
    next is answered. At the data commit `2a4213bf` the counter printed `… voted=0 dissent=0 … failed=votes`,
    exit 1 (`.ufo/waves/round-53/evidence/c1-at-data.txt`) — rows and located quotes before votes. Shown able to
    fail: `.ufo/waves/round-53/evidence/control-c1-do-nothing.txt` (`rows=0 … pins=bad provenance=bad …
    failed=ledger_absent,pins`, exit 1); `control-c1-all-held.txt` (`status_ok=44 quote_ok=44 … failed=quote,status`)
    fails exactly the two `mm/mmap.c` rows whose quote v7.3 respelled to `vma_flags_set(&vma_flags,
    VMA_NORESERVE_BIT)`; `control-c1-v72-copies.txt` (`pins=bad … failed=pins,quote,status`) fails v7.2 bytes
    presented as v7.3; `control-c1-no-votes.txt` reproduces the data line. Not covered: `held` proves the v7.2
    quote's words still occur somewhere in the v7.3 file, not at the same place nor with the same meaning; the two
    `absent` rows carry disposition `holds` because the rule survived a respelling, so `holds=46 changed=0` must not
    be read as "no quote moved" (the entry title says "two quotes respelled"); 3 of the 49 rows cite the 2014 commit
    patch and are out of scope; D is the two entries' claim tables only — not `oom-tracepoints-r47.md`, the
    round-50 memcg entry, prose outside the tables, or the SOURCES anchors; the votes are lane seats, not outside
    verification; and the pins prove the copies are the bytes fetched from cgit, not that cgit served the tag.

145. **A runway verdict names the enforcement mode, and under mode 2 the error band that decides `COMMIT_LOW`; a
    band field that the verdict does not use is not the rule.** Lesson: round-53 C2 (the commit ledger moves from
    `corpus/knowledge/overcommit-commit-limit-r52.md` into `tools/mori-commit-runway.py`; the band is
    `mm_compute_batch` × present CPUs × page size, rows S511–S513). Rationale: one "commit headroom" number
    misleads in every mode — under mode 0 nothing below RAM + swap is refused, under mode 1 nothing is refused at
    all, and under mode 2 the enforced value is the global part of a per-CPU counter that lags the printed exact
    sum by up to one batch per CPU, so printed room can coexist with a refusal. A tool that prints `band_kb` but
    declares `COMMIT_LOW` only below zero usable room is band-blind and its fields look honest. Check:
    `python3 -I -B tools/mori-commit-runway.py` prints one JSON object in which `mode` and `enforced` name the
    policy (host 2026-10-26: `"mode": 0, "enforced": false, "band_kb": null, "verdict": "COMMIT_HEURISTIC"`,
    exit 0), and under mode 2 `usable_kb` and `band_kb` are numbers; the frozen edge pair decides the rule —
    `mode2-band-edge-equal-is-low` prints `usable_kb 32768 = band_kb 32768`, `COMMIT_LOW`, exit 1, and
    `mode2-band-edge-one-page-above` prints `usable_kb 32772 > band_kb 32768`, `COMMIT_OK`, exit 0 (both cases
    materialised from `tools/fixtures/mori-commit-runway/cases.json` and run with `--meminfo --vm-dir
    --cpu-present --page-kb`); `python3 .ufo/waves/round-53/count-c2.py <R> --scratch DIR` exits 0 printing
    `C2=met tool=present selftest=pass n=23 fixtures=80 agree=80 disagree=0 registry=ok live=ok`. Shown able to
    fail: `control-c2-mode-blind.txt` (`agree=53 disagree=27`), `control-c2-no-band.txt` (`agree=71 disagree=9`,
    including `mode2-band-edge-low want=COMMIT_LOW got=COMMIT_OK`) and `control-c2-memoriser.txt` (`71/9`); all
    three print `selftest=pass n=12`, so the fixture arm and not the selftest is what separates them. Not covered:
    REF and the tool share one author, so a shared misreading of the kernel passes both; the band is an upper bound
    from the batch rule with present CPUs and totalram at read time, not a measured deviation; `COMMIT_LOW` is
    "inside the counter's own band", not a calibrated alarm (FR8 stays open); the live leg compares stable fields
    only, and on a mode-0 host — this one — the band fields are `null` live, so the mode-2 rule is exercised by
    fixtures alone; the tool reads no cgroup-level commit and sets no alert threshold.

146. **A SCORECARD row's numbers are the numbers of the receipt it cites.** Lesson: round-52 closure D2 — row
    `SCORECARD.md:2746` records `items=42 … locators=27` while citing `evidence/c1-at-landed.txt`, which prints
    `items=43 … locators=28`; the digits are verbatim from `evidence/c1-at-data.txt` measured at `8524904a`, so the
    citation anticipates the later receipt (the verdict is unaffected — both receipts print `C1=met …
    mismatches=0 errors=0`, rc 0). Rationale: a scorecard row is where a reader checks a round's arithmetic; a row
    whose citation names one receipt and whose digits come from another silently rewrites the round in the
    direction of whichever receipt the author last had open. Check: the loop below takes, for each tally key, the
    row's last occurrence and the `^C1=` line of the receipt named last in the row (the after-cell), and prints
    `ok|mismatch`:

    n=2746; row=$(sed -n "${n}p" SCORECARD.md)
    rec=$(printf '%s' "$row" | grep -o 'evidence/[a-z0-9-]*\.txt' | tail -1)
    for k in items locators; do
      a=$(printf '%s' "$row" | grep -o "$k=[0-9]*" | tail -1 | cut -d= -f2)
      b=$(grep -h '^C1=' ".ufo/waves/round-52/$rec" | grep -o "$k=[0-9]*" | tail -1 | cut -d= -f2)
      printf '%s row=%s receipt=%s %s\n' "$k" "$a" "$b" "$([ "$a" = "$b" ] && echo ok || echo mismatch)"
    done

    on the round-52 pair it prints `items row=42 receipt=43 mismatch` and `locators row=27 receipt=28 mismatch`,
    while the same row against `c1-at-data.txt` prints `row=42 receipt=42` and `row=27 receipt=27` — which names
    the attribution; for the round-53 row, `n=$(grep -n 'count-c1.py R' SCORECARD.md | tail -1 | cut -d: -f1)` and
    the receipt prefix `.ufo/waves/round-53/`. Shown able to fail: that reading, and the round-53 instantiation is
    the appended correction line the round-52 closure requires (routed defect 1). Not covered: only the keys the
    row displays are compared, so a count the row omits is unchecked; the receipt side is read at whatever bytes
    the tree holds, so an edit to the receipt after the row moves the comparison silently (no pin binds it); a row
    citing no `evidence/*.txt` path is skipped by the selector; the selector takes the last path in the cell, so a
    row naming its after-receipt before its before-receipt compares the wrong pair.

147. **A report names its own commit by command, never by a placeholder.** Lesson: round-52 closure D1 — the report
    carries `[FILL]` at line 5 (`… Report commit `[FILL]`.`), where its own commit hash belongs, and at line 46
    (`| `[FILL]` | receipts at landed tip: …`); the hash that exists is
    `aacd7a83027cdee8e950a2c39d490feaed3be13c` (`git log --format=%H -- .ufo/reports/round-52/mori.md` on the fleet
    repo). Rationale: a report is written before its own commit exists, so the commit cell is the one value the
    author cannot know while writing; a placeholder left there survives every later reading and makes the report
    unverifiable from its own text. The round-53 convention replaces it with the command that prints the value.
    Check: on the fleet repo `git log --format=%H -- .ufo/reports/round-53/mori.md` prints a 40-hex hash and that
    hash occurs in the report; `grep -nE 'Report commit `?\[FILL\]|^\| `\[FILL\]` \|' .ufo/reports/round-53/mori.md`
    prints nothing, rc 1. Shown able to fail: the same grep on `.ufo/reports/round-52/mori.md` prints
    `5:… Report commit `[FILL]`.` and `46:| `[FILL]` | receipts at landed tip: `c1-at-landed.txt`,
    `c2-at-landed.txt`, `census-end.txt` | Round 52 |`. Not covered: the grep matches the two positions round 52
    used (a metadata line and a commit-table row); a placeholder spelled `TBD`, `<hash>` or `pending`, or one placed
    in prose, is not matched; the positive arm holds only after the report is committed, so at writing time only the
    negative arm runs; the criterion binds the report to a commit that touched it, not to the commit the author
    intended.
```

## 4. What each draft is anchored to, and where it could be wrong

- 144's target line is the contract's target (`voted=46 dissent=0`), not a landed reading: the landed receipt does
  not exist at `95cf78ee`. Its "shown able to fail" arms are four committed control receipts, all read verbatim
  above. The C1 counter's own `--selftest` (`pass=37 fail=0`) carries the arms the draft leans on:
  `no_votes_unmet`, `one_voter_unmet`, `same_voter_twice_unmet`, `fenced_votes_unmet`, `dissent_unmet`,
  `revised_dissent_met`, `author_vote_not_counted_unmet`.
- 145 is anchored to two commands I ran (§2) plus the at-data receipt; the pair `32768 / 32772` is the exact
  boundary the `no-band` control fails on, so the Check cell is not a restatement of the field list.
- 146's Check cell was executed on the round-52 pair and reproduces the defect with the attribution
  (`42/27` = `c1-at-data.txt`, `43/28` = `c1-at-landed.txt`). Its round-53 form needs the row and the landed
  receipt to exist; until then only the historical arm runs.
- 147's Check cell was executed on the round-52 report (fleet repo, read-only `git log` and `grep`); the round-53
  report does not exist yet (`ls .ufo/reports/round-53/` lists `chousa.md kake.md kotoba.md kotodama.md
  kumitate.md`, no `mori.md`).
- Non-duplication: 142 checks that a pointer lands on the words it reports; 141 checks a living pin's tally or its
  supersession; 84 checks that a round's last batch carries tip receipts and that the report cites them. None of
  them compares a row's digits with the receipt it names (146) or forbids a placeholder for the report's own
  commit (147). 139/140/143 are runway-reading and entailment-vote rules; 144/145 are the release-recheck and
  mode/band rules.

## 5. Limits of this seat's drafts

- 144 and 145 rest on committed receipts, not on my re-execution of the counters; I did not run `count-c1.py` or
  `count-c2.py`. The two commands I did run are the tool on host defaults and on two fixtures I materialised from
  `cases.json` myself (independent of the counter's fixture arm, but the same fixture bytes the tool ships).
- 146's and 147's round-53 arms are UNVERIFIED by construction: the round-53 SCORECARD row and the round-53 report
  do not exist at `95cf78ee`. Their historical arms are verified.
- 145's `Not covered` keeps the contract's own limits (shared author, upper-bound band, no calibrated alarm); I
  did not add a limit I had not seen stated or observed.
- The drafts assume the L1 inserts them under a `## Criteria added round 53 — …` heading matching 1354's shape;
  the heading text in §3 is a draft, not a claim about wording.
- No claim is made about whether 144–147 should be admitted; that is the L1's and the wave's decision.

## 6. Scratch and side effects

- `mkdir -p /fast/scratch/hyaku/mori-r53/Mo53ScribeQuality/{tmp,fx}`, `TMPDIR` exported to `…/tmp`; the two
  fixture directories (`meminfo`, `present`, `vm/` five files) were written there and the tool was run against
  them; the whole seat directory was then removed with `rm -rf -- "$S"`. Nothing was copied out because every
  output cited here is quoted in §2.
- Disk guard before the run: `bash scripts/hyaku/disk-guard.sh status` rc 0, `/fast/scratch/hyaku` 609.3G free,
  `/tmp` 123.4G free. No ENOSPC. No clone was made (none was needed): every read was of the lane work tree, the
  fleet repo, or the tool's own fixture file.
- `git status --porcelain` in the lane at read time: only other seats' outputs
  (`?? .ufo/waves/round-53/evidence/selftests/`, `w1.ready`, `w1.ready.partial`, `w1/`); no tracked file changed by
  me. No git/jj mutation anywhere; no pacman; nothing installed.

## Findings

1. **MED — `corpus/QUALITY.md` draft 145 vs `tools/mori-commit-runway.py` and `.ufo/waves/round-53/controls/controls.py:46-47`.**
   The `no-band` control keeps the reference reading's `band_kb` intact and rewrites only `verdict` and the exit
   code (`if MUT == "no_band" and out["mode"] == 2: out["verdict"] = …`). A criterion that only required a non-null
   `band_kb` under mode 2 would therefore pass a band-blind tool; draft 145 binds the verdict to the band-edge pair
   (`32768 → COMMIT_LOW`, `32772 → COMMIT_OK`) for that reason. Any future check written from this criterion must
   read the verdict, not the field. Concerns `tools/mori-commit-runway.py` (field `band_kb`) and draft 145.
2. **MED — `SCORECARD.md:2746` still carries the superseded numbers at the tree I read (`95cf78ee`).**
   The round-52 C1 row reads `items=42 … locators=27` while citing `evidence/c1-at-landed.txt` (`items=43 …
   locators=28`); the round-53 contract (routed defect 1) requires an appended correction line this round, and no
   round-53 SCORECARD section exists yet (`grep -n '^## Round 53' SCORECARD.md` → no match). Outstanding, not
   wrong-by-design: it is the defect 146 exists to prevent and the round-53 integration owes the correction.
3. **LOW — `corpus/knowledge/kernel-v7.3-recheck-r53.md:81,84` and the C1 disposition vocabulary.** The two
   `absent` rows carry disposition `holds`, so the counter's `holds=46 changed=0` at the data commit reads as "no
   rule changed" while two quotes were respelled. The entry title ("two quotes respelled") and line 40 carry the
   distinction, but the disposition cell alone does not: a reader comparing `absent=2` with `changed=0` has to know
   that `holds` means "the rule survived", not "the words survived". Draft 144's `Not covered` states this; a
   one-sentence gloss on the ledger's `disposition` column would remove the ambiguity (L1's call, data may be
   corrected).
4. **LOW — draft 146's receipt selector.** The loop compares only the tally keys the row displays and takes the last
   `evidence/*.txt` path in the cell as the receipt; a row that omits a count, cites no `evidence/` path, or names
   its after-receipt before its before-receipt is unchecked or mis-paired. Recorded in the criterion's `Not
   covered`; a round-54 counter arm over SCORECARD rows would close it, and no counter change is proposed here.
5. **LOW — `.ufo/reports/round-52/mori.md:5,46` (fleet repo).** The two `[FILL]` placeholders remain in the
   historical report. They are the "shown able to fail" arm for 147 and are not to be rewritten in place (the
   round-52 report is a committed artifact); the convention lands in the round-53 report and the lesson, as the
   contract's routed defect 2 requires.
