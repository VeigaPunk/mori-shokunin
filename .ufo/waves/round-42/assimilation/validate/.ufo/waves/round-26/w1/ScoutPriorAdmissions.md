# Scout prior admissions — what mori rounds 20–25 ruled, and the pitfalls round 26 must avoid

Seat: MoriR26.ScoutPriorAdmissions (leaf scout). Date 2026-10-22. Lane root
`/home/vgpnk/Projects/shokunin/mori-shokunin`. Sources read: the round-24 and round-25 verifier
spot-checks, `MANIFEST.json` entries for mori rounds 20–25, `corpus/QUALITY.md` 76–77,
`corpus/lessons/round-{20,23,24,25}.md`, `corpus/lessons/round-23-verifier-spotcheck.md`,
`SCORECARD.md`, `PROVINCE.md`, `corpus/SOURCES.md`, the r12 FR10 entry and `corpus/README.md`,
and the sibling `tsukuroi-shokunin` r25 entry at `157ee255`. I ran only read-only git, jq, grep and
stdlib reads plus one scratch git demo. No lane tool, gate or selftest. No tool installs.
Files written: this report and `/fast/scratch/hyaku/mori-r26/ScoutPriorAdmissions/` (scratch demo).
Contract read first: `.ufo/waves/round-26/contract.md`.

Confidence: high on the rulings and counts below (each re-derived from committed bytes or a named
file line). Medium on two judgment calls, marked [INFERENCE].

## A. Admission and width rulings, rounds 20–25

| Round | Claim | Ruling as recorded | Source |
|---|---|---|---|
| 20 | C1 freshness (classify drift, re-pin) | **Rejected-harmed.** Numbers verified; the re-pin absorbed unresolved old-wave evidence loss. Freshness harmed, calibration harmed. | `MANIFEST.json:10539` (`trend_ruling`), `corpus/lessons/round-20.md:12-14,23` |
| 20 | C2 coverage (14 frozen cases) | Verified by an independent oracle and 23/23 selftest, **but no capability admission because the round was rejected**. | `MANIFEST.json:10544` (`notes`) |
| 21 | C1/C2 | Admitted, bounded; C1 repairs evidence retention without settling the old waves; outside labels are non-author. | `MANIFEST.json:10981` (`verification.C1_remeasurement`, `outside_authority`) |
| 22 | capability (24 frozen cases) | Admitted **at held score**. The 24 frozen cases weigh highest; 52 co-evolved controls and 22 mutants weigh lower. | `MANIFEST.json:12021` (`notes`, `verification.rechecks`) |
| 23 | C2 coverage (30 sealed cases) | **Unprovable.** 29/30 at the prototype; the governing pre-seal rule contradicts one frozen expected row; both kept, no special-case, no retroactive rule. | `corpus/lessons/round-23-verifier-spotcheck.md:25,38,62` |
| 24 | C1 calibration | **Improved, bounded.** Denominator 2 rows; both times are lane-written so a backdated commit would pass; a routed clause unchecked; score 5 → 5. | `corpus/lessons/round-24-verifier-spotcheck.md:65-73` |
| 24 | C2 coverage | **Improved, bounded.** 10 mutants killed, 6 survived; co-evolved supplementary not counted; score 6 → 6. | `corpus/lessons/round-24-verifier-spotcheck.md:79-88` |
| 25 | C1 calibration | **Statement wider than counter.** The counter checks scores and the `round 1` rule only; an Axes row credits a rejected round; excess routed R4. | `corpus/lessons/round-25-verifier-spotcheck.md:58-62` |
| 25 | C2 coverage | **Statement wider than counter.** "never turns an unreadable … input into a number" is false for 72 of 307 probe configs; the capability still moves because it ran on the host's block-style file; excess routed R1/R2. | `corpus/lessons/round-25-verifier-spotcheck.md:84-90,180-181` |
| 25 | retention | **No axis harmed at the head** (4 → 88 → 4). The round-17 rejection turned on material retained at the tip; history disposition is the operator's. | `corpus/lessons/round-25-verifier-spotcheck.md:92-107,116` |

## B. How each closure re-derived evidence (no lane gate executed)

| Closure | Method | Source |
|---|---|---|
| r24 | Plain git and JSON reads; before = `cat-file` exit 128; freeze order = tool absent at the freeze commit, cases blob equal to the tip, 12 cases; the tally was **evidence-verified, not re-run**, because the tool is a registered gate; the later tool diff was read statically. | `round-24-verifier-spotcheck.md:13-16,79-88` |
| r25 | Plain git reads under both the amended and the original predicates; `cat-file`/`rev-parse`; Python over `git show` blobs with emphasis stripped and whitespace folded; retention re-implemented as a regex scan over `ls-tree`/`cat-file` printing counts only; upstream re-opened with `curl`, sha256 compared to the row. | `round-25-verifier-spotcheck.md:14-17,40-56,92-104,131-142` |
| r21 | Independent stdlib over `git show <rev>:<path>`; "No lane-owned gates or selftests executed"; provenance digests for the deleted tree. | `MANIFEST.json:10981` (`verification.scope`, `C1_remeasurement`, `C1_provenance`) |
| r22 | Author driver re-run in a throwaway clone; plain `cat-file` and freeze-time checks; `jq -S` identity of the summary. | `MANIFEST.json:12021` (`verification.rechecks`) |
| r23 | Main git-counted registry rows; probe absence exit 128; native checker and generator hashes at parent commits; incomplete analysis refused. | `MANIFEST.json:12237` (`verification.rechecks`, `native_gate`) |
| r20 | Recount with a whole-pipeline C locale after the locale bug; independent Python set differences; oracle run black-box against both revisions. | `MANIFEST.json:10497` (`verification.C1_remeasurement`, `C2_remeasurement`) |

Two binding consequences for r26. A registered gate's tally is evidence-verified, not re-run
(`round-24-verifier-spotcheck.md:15-16`); an unregistered verdict tool is "not graded conformant as
a gate" (`round-25-verifier-spotcheck.md:33-36`). And the closure itself runs no lane gate — it
measures with git, grep, jq, curl and Python over committed blobs
(`round-25-verifier-spotcheck.md:10-12`).

## C. Checklist for round 26 (15 items)

1. **Measure every clause of the statement, not only the headline number.** r24 recorded the
   boundary explicitly: "R4's 'every row' is enumerated by the counting command. No other universal
   clause carries the result" (`round-24-verifier-spotcheck.md:93`); r25 routed two statements that
   were wider than their counters (`:58-62`, `:84-90`).
   *r26 action:* the contract's C1 command measures phrase absence and entry presence only. The
   statement also says the stale lines become "dated past-tense records that name the superseding
   entry" (`.ufo/waves/round-26/contract.md` C1) and that the r26 entry's `source:` cites a row
   opened in round 26. Add counted clauses for both (for example a per-file count of lines carrying
   `userspace-oom-killers-r26.md` and a `2026-10-22` token, and a grep of the r26 `source:` line for
   an id whose `SOURCES.md` `opened` cell reads 2026-10-22), or trim the statement.

2. **A frozen case and the governing rule must agree before the freeze; never special-case a case.**
   Round 23's C2 died because the pre-seal rule demanded one answer and a frozen expected row said
   another; the verdict kept both bytes and refused to touch the row
   (`round-23-verifier-spotcheck.md:25,38`), and the route forbade special-casing that case
   (`:62`).
   *r26 action:* the case seat derives every expectation from the contract's grammar and verdict
   rules; a case that contradicts a rule is fixed, or the rule is narrowed, in a commit that lands
   before the freeze. No case-specific branch in the tool and no edit of a frozen row.

3. **Freeze order and authorship are shown by git, and the tool seat never sees the cases.** The
   freeze order and the before-value were re-measured from `cat-file`, `rev-parse`, commit times and
   blob equality (`round-24-verifier-spotcheck.md:15-16`). Round 24's M8 is the exact failure r26
   can repeat: the tool seat read the frozen cases from the cases seat's clone, so the contract could
   show order but not independence; the fix is to withhold the case writer's clone path from the
   tool seat's prompt (`corpus/lessons/round-24.md:67`). Co-evolved evidence weighs lower than
   frozen cases (`MANIFEST.json:12021`).
   *r26 action:* commit the freeze-order check as one command (cases blob equal at the freeze
   commit and at the tip; tool absent at the freeze commit; the cases commit a strict ancestor of
   the tool's first commit), keep the two seats' clone paths out of each other's context, and label
   mutants and matcher controls as co-evolved.

4. **Register the tool as a gate before citing its tally, and give the receipt a full header.**
   Two round-25 verdict tools with no `SKILL.md` registry row were "not graded conformant as a
   gate" (`round-25-verifier-spotcheck.md:33-36`). QUALITY 76 requires the measured full revision,
   the command, the tool blob, the fixture tree, the exit code and the complete stdout
   (`corpus/QUALITY.md:340-347`); round 24's D1 shows a tally without a revision is stale
   (`round-24-verifier-spotcheck.md:137`).
   *r26 action:* the contract's C2 asks for no registry row and no receipt header. Add a Round26
   registry table under `SKILL.md` (the round-24 pattern is `SKILL.md:637`; `SKILL.md` currently ends
   at line 673 with no round-25 registry rows) with kind, verdict map 0/1/2, self-test command,
   pinned values, write scope and owner, and commit the selftest output with that header.

5. **Scope the capability wording; no promissory universal.** Round 25's capability row claimed the
   tool "never turns an unreadable, ambiguous or unparseable input into a number"; 72 of 307 probe
   configs made it read a false number, and the row was routed (`round-25-verifier-spotcheck.md:84-90`,
   `:180-181`).
   *r26 action:* the SCORECARD capability row states what the frozen cases and earlyoom 1.9.0's
   grammar lines cover, names `KILLERS_UNKNOWN` for unreadable input, and lists the limits (no
   `MESSAGE` text, no kill history, no other killer). No "never", no "any".

6. **Disclose survivors; they bound an admitted capability without voiding it.** Six wave-2 mutants
   survived round 24 and were named, and the claim was still admitted, bounded
   (`round-24-verifier-spotcheck.md:87-88`).
   *r26 action:* run at least one mutant per verdict rule and per grammar line, record kills and
   survivors, and put the survivors in the entry's Limits and in the report. Do not claim behaviour
   a surviving mutant disproves.

7. **Capability credit exists only in an admitted round.** Round 20's C2 was verified by an
   independent oracle at 14/14 and by a 23/23 selftest, and the notes still read "no capability
   admission in rejected round" (`MANIFEST.json:10544`), because freshness and calibration were
   harmed (`:10539`).
   *r26 action:* C1's hygiene decides C2's credit. Finish the sweep and both receipts before the
   report; a freshness defect sinks the coverage capability.

8. **A refresh that absorbs unresolved evidence loss harms freshness.** Round 20's freshness harm
   was a "premature re-pin" (`MANIFEST.json:10539`); the SCORECARD freshness row still reads "the
   round-20 re-pin was rejected" (`SCORECARD.md:13`).
   *r26 action:* supersede, do not re-pin. Carry r12's `[UNKNOWN]`s forward unchanged (no oomd xattrs
   read, xattr lifetime unmeasured, earlyoom action lines are not a stable `MESSAGE_ID` class,
   `corpus/knowledge/userspace-oom-killers-r12.md:24`), date the new capture, and record the host
   versions it was taken on.

9. **Correct every mention in place; a banner is not a fix.** QUALITY 77 requires the corrected
   wording at every place that states the fact, with the superseded wording removed, not shadowed
   (`corpus/QUALITY.md:349-356`). Round 24's D2 left three body lines standing beside a corrections
   banner (`round-24-verifier-spotcheck.md:138-143`); quality moved in round 25 only after the
   statements were corrected in place and the banner removed
   (`round-25-verifier-spotcheck.md:164-166`).
   *r26 action:* the measured mentions at `248408f5` are `userspace-oom-killers-r12.md:6`, `:14`,
   `:18` and `corpus/README.md:34` (the four frozen phrases). Two more carriers are not in the
   frozen list but state the same fact and will be read as an incomplete sweep: the `recheck:`
   recipe at `userspace-oom-killers-r12.md:3`, whose recorded output ends `inactive; inactive; 0; 0`,
   and the snapshot sentence at `:8`. The recipe is the worse one: `systemctl is-active
   earlyoom.service` prints `active` today (observed), so the entry would carry a recipe that
   contradicts its own record.

10. **The counter must not be satisfiable by a quote or a deletion.** Demonstrated in scratch: a
    past-tense line that quotes the frozen phrase still matches `git grep -q -F`, while a paraphrase
    does not; a missing path also exits 1, the same code as "phrase absent" (command and output in
    `/fast/scratch/hyaku/mori-r26/ScoutPriorAdmissions/grepdemo`).
    *r26 action:* paraphrase in the past-tense record and never quote a frozen phrase; add
    `git cat-file -e "$R:$f"` per file plus a positive-presence count so a deletion or rename cannot
    read as a correction.

11. **Receipts name the revision and carry the full output.** QUALITY 76
    (`corpus/QUALITY.md:340-347`); round 25's D1 held only when the header's tool blob and fixture
    tree were equal at the named revision and at the head (`round-25-verifier-spotcheck.md:40-46`).
    *r26 action:* `c1-before.txt`, `c1-after.txt` and the selftest receipt each carry revision,
    command, exit code and full stdout; the after receipt is measured at the landed tip the report
    names.

12. **Counting commands must be fail-capable and environment-proof.** Round 20's M9 set `LC_ALL=C`
    on `comm` only and printed 37/33 instead of 8/0 (`corpus/lessons/round-20.md:30`); round 25's
    first D2 predicate passed four paraphrased copies that kept the false statements
    (`corpus/lessons/round-25.md:45-48`).
    *r26 action:* show the C1 command red once (one phrase restored gives `stale_present=1`) and
    show the quoted-line false negative; state that `.ufo/waves/round-26/c1-phrases.txt` has four
    lines and ends in `0x0a` (verified), so the `read` loop cannot drop the last phrase. No
    locale-sensitive tool is used by the command; the before-value reproduces (observed:
    `stale_present=4`, `r26_entry=absent` at `248408f5`).

13. **A knowledge entry earns expansion credit only with rows opened this round, marked limits and a
    coverage-map row.** Round 25's new entry was credited with a new coverage-map row and a `source:`
    citing rows all `mined`, tier A, opened that round (`round-25-verifier-spotcheck.md:159-163`);
    the census must exit 0 (`:31`).
    *r26 action:* the r26 entry cites new `S1xx` rows. `corpus/SOURCES.md` holds `S001`–`S113`, and
    the only earlyoom row is the old README at commit `8477c902` (`corpus/SOURCES.md:22`), so a
    tag-`v1.9.0` raw URL is a new row, not a duplicate-URL warning. Each new row carries a Gate line
    (access date 2026-10-22, quote at most 25 words with its location). Add the `corpus/README.md`
    knowledge row: all 34 files under `corpus/knowledge/` have one today (loop over the basenames,
    no misses).

14. **Host and unit state belongs to tsukuroi; cite, never absorb.** `PROVINCE.md:53` keeps the FR10
    boundary, `PROVINCE.md:66` gives tsukuroi systemd-unit diagnosis, and r12 already recorded its
    readings as "a 2026-10-19 availability snapshot only"
    (`corpus/knowledge/userspace-oom-killers-r12.md:8`). The sibling r25 entry says "The frozen
    capture never read earlyoom" and cites mori's own entries rather than absorbing them
    (`tsukuroi-shokunin` at `157ee255`, `corpus/knowledge/memory-pressure-r25.md` "Sibling lane" and
    "Userspace killers").
    *r26 action:* cite that sibling entry as adjacency, keep C1's "not claimed" list (no host-wide
    unit census, no kill history), and write no OS diagnosis and no enable or tune action.

15. **The report names the true final tip, and every cited hash is an ancestor.** Round 25's report
    opened with `e0e33c11` while the true tip `829d8c90` appeared only in addendum 8
    (`round-25-verifier-spotcheck.md:33`); round 24's closure checked every 8–40 hex token with
    `git merge-base --is-ancestor` and had to explain one upstream hash that was not a lane hash
    (`round-24-verifier-spotcheck.md:25`).
    *r26 action:* name the landed tip in the report opening and in both receipts; check every hash
    token; label the earlyoom tag commit and any Linux hash as upstream.

## D. Remaining unknowns

- Whether the closure will place the r12 `recheck:` recipe (`:3`) inside the QUALITY 77 sweep is a
  judgment call. QUALITY 77 says "every place that states it", and the recipe's recorded output now
  contradicts the host, so I grade it in scope. [INFERENCE]
- Recording a dated earlyoom activation in a mori entry follows the precedent at r12:8, which
  already recorded `systemctl` readings with a timestamp. Whether the closure treats the new dated
  state as ordinary adjacency or as absorbed diagnosis is not settled by any prior ruling I found.
  [INFERENCE]
- The ids the r26 entry will cite are unassigned (`SOURCES.md` ends at `S113`). I did not open any
  earlyoom file this round, so I verify no quote, anchor, sha256 or line number from the upstream
  sources; the grammar anchors in the contract are taken as given.
- The contract does not say whether `PROVINCE.md:53`'s "First evidence" pointer should move to the
  r26 entry. No prior ruling covers a supersession that leaves the frontier pointer on the
  superseded file.
- I did not run the lane census or the retention scan (lane tools are the L1's and the executors'
  work), so I state no value for either at the entering tip.
