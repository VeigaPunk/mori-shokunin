# Round 88 — mori (L1 MoriR88), attempt 1, wave w1 — lesson

round: 88
date: 2026-11-04
entering: `1bd5ec3fa260458f74eb32a2e5bb157209c5934d`
freeze: `2a5e3ad96deb978ed1fb958e87b4be8221fb23b7` (contract, both counters, the controls)
subjects: `4d0f7bf0b0a0d978fa65d9b93edc37a2e6556550` (first landing), `d5e2eda494877a85edaa4e287d6ad81843d9a8a1`
(fixture tally fix — the revision every after-value is measured at)
after receipt: `.ufo/waves/round-88/evidence/after-r88.txt` at `9c775ac2131da13c4c4cfdf2b14077184076f557`
seat scope: this lesson and its `## Gate`. The wave seats write their own reports under
`.ufo/waves/round-88/w1/`; they do not commit.

Axes this round: **operability** (six surviving r87-counter clauses get their arms) and
**calibration** (the receipt gate refuses two counterfeit bodies). Detection and report only.

## What the round did

Two claims, frozen at `2a5e3ad9` before any after-value existed, each with a named do-nothing
control in `.ufo/waves/round-88/evidence/controls-r88.txt`:

- **C1 operability (7)** — six arms land in `.ufo/waves/round-87/count-c1.py` (selftest 18 → 24),
  each the failing arm for one clause the r87 mutation matrix
  (`.ufo/waves/round-87/w1/Mo87M01Mut.md`) measured surviving: `M1-met-no-guard`,
  `M2-met-drop-empty`, `M3-killed-n`, `M4-arms-total`, `M5-split-field`, `M6-anchor-guard`. The
  new counter `.ufo/waves/round-88/count-c1.py` re-derives the six mutants at any revision and
  requires the pristine 24-arm selftest plus each mutant killed. Target `C1=met mutants=6 killed=6
  survivors=0 total=6 arms=24`. Entering control: `C1=unmet ... survivors=6 total=6 arms=18` (rc 1);
  a label-only fixture that reaches 24 arms with six passing no-op rows still reads `survivors=6`.
- **C2 calibration (5, tied lowest)** — the r87 receipt gate gains three refusal paths
  (`declared_replay_problem`, `binding_problems`, `absent_supersede_targets`) and six arms
  (selftest 17 → 23). The new counter `.ufo/waves/round-88/count-c2.py` builds four fixtures inside
  `--shared` clones and replays the graded gate at each: `clean` met, `stripped` → `missing-replay`,
  `vacuous` → `cmd-binding`, `absent-target` → `SUPERSEDE ... absent=1`, while the real seven-receipt
  population still prints the r87 target tail. Target `C2=met real=met fx=4 clean=1 refused=2
  absent=1 arms=23`. Entering control: `C2=unmet ... refused=0 ... arms=17` (rc 1) — both
  counterfeits printed the exact r87 target tail, so the after value is not reachable by doing
  nothing.

Wave shape: one v1 wave, 12 seats (3 executor, 1 simplifier, 1 scout, 2 scribe, 2 reviewer,
1 critic, 1 mutation-tester, 1 connector; attack 4/12 = 33.3 %), validated under policy v1
(`w1-dispatch.json` counts `spawn 12`), reports under `.ufo/waves/round-88/w1/`.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix delivered and what makes it able to fail |
|---|---|---|---|
| `fixture-satisfied-for-the-wrong-reason` — the six-arm witness population reached `met is False` through `pristine-ok`, not through the guard the arm names. `dup.py` and `empty.py` printed `FAKE pass=1 fail=0` but no `COUNTER_SELFTEST` line, so `arms_of` read `(-1,-1)` and `pristine_ok` was false before the guard was ever consulted; the arm asserted `not met` and passed for that reason. The only thing that noticed was the claim's own kill rule: at the first landing `4d0f7bf0` the frozen counter read `C1=unmet mutants=6 killed=4 survivors=2`, with `M1-met-no-guard` and `M2-met-drop-empty` surviving. | `.ufo/waves/round-88/evidence/after-r88.txt` is the after; the before is the run at `4d0f7bf0` (`C1=unmet ... killed=4 survivors=2`), reproducible by `python3 -I .ufo/waves/round-88/count-c1.py 4d0f7bf0`; the fixture lines are `.ufo/waves/round-87/count-c1.py` `write(d, "dup.py", …)` / `write(d, "empty.py", …)`. | The claim's kill rule (P-C1: a mutant that survives keeps the claim unmet), not a prose review. | `d5e2eda4` gives both fixtures a `COUNTER_SELFTEST pass=1 fail=0` line, so `pristine_ok` is true and the guard is the sole reason `met` is false. Able to fail: with the mutant applied, the arm now flips (it printed `FAIL met_guard_unanchored` / `FAIL met_guard_empty` at `4d0f7bf0`), and at `d5e2eda4` the same six mutants are all killed. |
| `anchor-not-unique-in-its-own-file` — `M1-met-no-guard`'s first anchor string (`and not any(e.startswith(("empty-mutation", "unanchored")) for e in extras)`) also occurs in the counter's own `MUTANTS` table, which stores the same clause text as data; `base.count(old)` read 2 and the frozen counter refused it as `unanchored` (`EXTRA unanchored ... occurrences=2`), so the population read `mutants=5` instead of 6 before any grading. | First control run at `1bd5ec3f`: `EXTRA unanchored .ufo/waves/round-87/count-c1.py M1-met-no-guard occurrences=2` and `C1=unmet mutants=5 ...`. | The exactly-once anchor guard (`if base.count(old) != 1`), which is the same rule the round's C1 claim arms. | The anchor now starts at the newline before the continuation line (`\\n           and not any(...`), which occurs exactly once; the entering control then reads `mutants=6`. Able to fail: the doubled-anchor fixture (`dup.py`) is refused with `unanchored` in both the r87 and r88 selftests, and `doubled_anchor_counted_type` pins that a doubled anchor is excluded rather than graded. |

Nothing else was mined this round. The r87 spot-check's eight routed defects are inherited: 2–4
are what C2 closes, 1 is discharged by the two SKILL.md gate rows (registry rows 21 and 22), and
5–8 are carried in the report. They are listed, not re-litigated.

## Gate

Sources opened this round. One new row, one rejected candidate.

| Candidate | Decision | Evidence / flip condition |
|---|---|---|
| **S604** — The Update Framework Specification v1.0.37, `https://theupdateframework.github.io/specification/v1.0.37/` | **ADMIT** (tier A, `spec`, `mined`; row after S603, `used-by corpus/knowledge/receipt-counterfeit-r88.md`, recheck `on-release`) | Accessed **2026-11-04**; two fetches byte-identical (`cmp` clean): HTTP 200, `redirects=0`, final URL identical to the requested directory URL, **248698 bytes**, **4997 lines**, sha256 `f20fda0dda7128f3b9cc1f12f3d90301b0f6e163576ba285bfe485d1671e8def`; copy `.ufo/waves/round-88/evidence/sources-r88/tuf-spec-v1.0.37.html`. Located quote in the tag-stripped joined text, occurring **exactly once**: "If the version of the new root metadata file is not N+1, discard it, abort the update cycle, and report the rollback attack." (**23 words**, raw HTML lines 3502-3506, §5.3, step 5.3.5). Page carries `dt-updated datetime="2026-10-08"`. |
| the same page as a second row (`index.html`) | **REJECTED** (duplicate URL and scope of S604) | The two paths returned the same bytes (sha256 equal), so a second row would be a within-scope duplicate (E04-class). Flip condition: a *different* scope on that page (for example the delegations/timestamp section) newly pinned and quoted. |
| `considerthese/2026-10-26.md` suggestion 4 — keep a suggestion-adoption status line | **ADOPTED this round** as the section below; grounded by reading the latest reflection file and by the r87 lesson's absence of any such line (its `## What the round did` names S603 and the routed defects but no prior suggestion's status). | Flip: if the status table is not carried into the next round's lesson, the adoption has lapsed and the suggestion reopens with a reason. |

Registry census, both runs on this worktree:

```text
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md          # before: rc 0, 376 rows
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md          # after:  rc 0, 377 rows
```

Row counts by the contract grammar `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`:
**376 → 377**; warnings 35 → 35 (all `W04` duplicate-URL, the entering tolerance), zero `E` codes
both times.

Gate limits, named: the quote is a raw-HTML line range and a reader must strip tags to see it as
one sentence; the spec's own version is pinned by the URL path (`v1.0.37`) and the page's
`dt-updated` date, not by a git tag. **Assimilation: none** — no `merge/mori/` package was read or
adopted this round; `/home/vgpnk/Projects/shokuknow` was not touched.

**S604 locator correction, in place and disclosed (old → new).** The row's anchor cell first read
`§5.3.7 Update the root role, step Check for a rollback attack (raw HTML lines 3502-3506)`. The
wave's knowledge reviewer (`w1/Mo88S02Knowledge.md` §2) measured that the heading containing those
lines is `<h3 id="update-root">` at raw line 3465 — *§5.3, Update the root role* — and that the
quoted paragraph is the **fifth** ordered-list item (`<li>` at raw line 3501, paragraph
3502-3506); `grep -c '5\.3\.7'` over the stored copy prints **0**. The cell now reads `§5.3
Update the root role, step 5.3.5 (fifth ordered-list item, raw line 3501; quoted paragraph raw
lines 3502-3506)`; the URL, sha256, byte/line counts and quote are unchanged, and no `status`,
`recheck` or `used-by` value moved. The same number was corrected in `corpus/README.md` and in
`corpus/knowledge/receipt-counterfeit-r88.md`. **Named contract deviation:** `CORPUS.md` rule 2
asks a correction to be a new row whose `teaches` opens `supersedes S0NN —`, but a second row for
the same URL and scope would be an E04 within-scope duplicate, so the locator cell is corrected in
place and this paragraph is the old→new record.

## Suggestion-adoption status (considerthese)

| Suggestion | Status | Evidence |
|---|---|---|
| 2026-10-25 #1 pin-check tool | adopted (r47) | `tools/mori-pin-check.py`; QUALITY 123 |
| 2026-10-25 #2 no absolute host path in instruments | adopted as a criterion, not acted on | QUALITY 127 |
| 2026-10-25 #3 flagged-versus-fixed count | adopted (r49) | `flagged=45 fixed=18 unfixed=9 na=18` (2026-10-26 daily) |
| 2026-10-26 #1 split pin-check mismatches into environmental vs stale | open | this round's instruments added no pin-check mismatch class |
| 2026-10-26 #2 follow unfixed critic flags forward | open | the r88 wave's critic report is the next input |
| 2026-10-26 #3 re-execute what closures only evidence-verified | adopted in spirit (r87 C2 rule, r88 counter) | `count-c2.py` replays the graded gate; the after receipt replays byte-identically |
| 2026-10-26 #4 keep this status line | adopted (this round) | this table |

## Seat findings merged at integration (wave w1)

All twelve seats settled; every report is merged below. None of them authored the round and none wrote the corpus.

1. **Mo88E02C2Gate (executor, C2 re-measurement by hand).** Built the counterfeits with `write`/`edit`
   only, never importing the r88 counter's `mutate_receipt`. Verdict **C2 agrees**: clean `C2=met`
   on the real repo and on an unmutated clone; `stripped` → `problems=missing-replay`; `vacuous` →
   `problems=cmd-binding`; `absent-target` → `SUPERSEDE … absent=1`; and the entering gate accepts
   stripped and vacuous whole (`C2=met … unexpected=0`). Its fixtures are scratch clone commits
   (`01edadbf…`, `e9198e2c…`, `c75e7a04…`), not citable evidence bytes.
2. **Mo88E03SecondImpl (executor, second implementation).** Own AST-based parser, no counter import:
   `SECOND_C1=6 killed / 0 survived` → **C1 agree**; `SECOND_C2 missing_replay=3 cmd_unbound=1
   absent_targets=0` raw, with the frozen declared-mode exemption `missing_replay=0 cmd_unbound=0` →
   **C2 agree on the header invariants**. It named the scope limit itself: its C2 half is a header
   parser, not an independent counterfeit runner. It also corrected the seat spec: the r87 counter's
   `MUTANTS` table holds the r86 anchors, so the r88 population had to be parsed from the r88
   counter — a spec imprecision in this round's item, not a defect in the gate.
3. **Mo88Sc01Scope (scout, rule scope).** `SCOPE_TABLE rows=7 applied=4 would_refuse=0`; no real
   receipt is falsely refused, and the one unbound binding path sits in a legacy row the rule skips.
   It measured **four contradictions in the first draft of `corpus/knowledge/receipt-counterfeit-r88.md`**,
   all corrected before the entry was committed: (a) rule 1 said "no `# replay:` line" while
   `# replay: none` also raises `missing-replay`; (b) rule 2 said "on a replayed row" while the rule
   is keyed on the declared mode and can fire on a row that never replays; (c) the entry's
   `after-r88.txt` provenance line named `d5e2eda4` while the receipt is committed at `9c775ac2`;
   (d) the `cmd-binding` sentence implied execution provenance while the rule checks naming only.
4. **Mo88R02ReviewC2 (reviewer, behavioral).** **C2 review agrees** on the frozen predicate and the
   no-regression line, and routes **R89-C2-comment-binding**: a bound path named only inside a shell
   comment satisfies `binding_problems` — fixture `a010047c` (cmd `printf 'RECORD_SWEEP fabricated=1\n'
   # tools/mori-record-sweep.py`) reproduces the exact r87 target tail. It also names the FX-line
   wording ambiguity (`FX clean … refused` means "expected outcome matched", not "rejected clean
   data") as a legibility fix for round 89.
5. **Mo88M01Mut (mutation-tester, r88 counter clauses).** 32 mutants, **20 killed, 12 survived**;
   ranked survivors and the witness each needs are in `.ufo/waves/round-88/w1/Mo88M01Mut.md`
   §"Ranked survivors". The sharpest is `C2-target`: the printed target is a constant, so mutating
   its `real=met` field still prints a met line; the counter's acceptance does not derive the line.
6. **Mo88K01Conn (connector, cross-lane).** Rule 1 is a fixed instance of tameshi's required-line
   refusal and of mado's unpinned-input refusal; rules 2–3 are mechanically disjoint fleet-wide; the
   rev leg is a weakened form of kotodama's sequence leg. Complements named (tameshi
   `count-recheck.py` value binding; tameshi `receipt-revision-gate.py` positive rev binding; mado's
   unpinned refusal and its provenance disclaimer; kotodama's three-revision equality; chousa's
   command/body-binding limit). `absorption: none`.
7. **Mo88S01Lesson (scribe).** Draft at `.ufo/waves/round-88/w1/Mo88S01Lesson.md`, including a
   byte-hash table that independently confirms the freeze/after hashes (`count-c1.py` `d1048cf0` at
   the freeze → `3ba0f97b` at the after; `count-c2.py` `8904a3d0` both). It wrote no Gate, no
   SOURCES row and no QUALITY criterion, as instructed.

8. **Mo88E01C1Arms (executor, independent C1 re-measurement).** **C1 agrees**: pristine 24/0, six
   exactly-once anchors, six killed, zero survivors, and every contract-named killer fires. It also
   measured an arm-table overlap (`met_guard_unanchored` also kills `M6`, whose promised arm
   `doubled_anchor_counted_type` fires too — an undeclared overlap, not a substitution) and a
   freeze-instrument drift: the counter bytes at the freeze (`d1048cf0`) differ from the after bytes
   (`3ba0f97b`) by the two fixture literals changed in `d5e2eda4`. Both byte sets were run against
   the same label-only fixture and both read `C1=unmet … survivors=6 total=6 arms=24`, so the drift
   changes neither the refusal nor the target. Disclosed as the contract's appended Erratum E1; it
   is also row 1 of `## Mistakes` above.

9. **Mo88R01ReviewC1 (reviewer, surgical C1).** **C1 review agrees** with the frozen predicate: all
   six new arms pass pristine and fail their intended mutant; none passes for a wrong reason. Two
   residuals are routed, not fixed here: (a) two *inherited* r87 arms (`unanchored_excluded`,
   `unanchored_plus_killed_unmet` at `.ufo/waves/round-87/count-c1.py:240,246`) still accept the
   substring `"unanchored"` from the mutant label as evidence — the same class the r88 counter
   repaired in its own copy (`missing_tally_refused`), routed as **R89-C1-label-substring**; (b) a
   documentation discrepancy: the contract's M5 fixture sketch said `arms=24` while the landed arm
   correctly uses `arms=54` (the r87 counter's own `TARGET_ARMS`), disclosed as contract
   **Erratum E2** — the code is right, the cell was wrong.

10. **Mo88C01Critic (critic, adversarial).** Reproduced both after lines first, then attacked. **C2
    blocked on every vacuity probe**: zero replays cannot reach the target line at `d5e2eda4` or at
    the entering bytes (the entering `defeated=1` itself needs a real failed replay), and a
    `# replay: none` waiver on a clone row, a stripped `required` header and a `true` command each
    read `unmet`. **C1 falsified as evidence**: an arms-free checksum canary subject (fixture
    `79143f94`) makes the frozen counter print the exact target line, because the frozen kill rule
    (rc≠0 or `fail=<n>`) cannot attribute a kill to a declared arm. Accepted and routed as
    **R89-C1-subject-identity** (pin the subject digest; count a kill only when the declared arm
    label appears in the mutant's FAIL lines). Two further C2 limitations were measured and routed:
    a self-printing command that also names the bound path passes (**R89-C2-selfprint-evasion**,
    fixture `3e84f588` prints the full target line), and the token rule is spelling not path
    identity (`./tools/mori-record-sweep.py` is falsely refused; **R89-C2-path-identity**). Contract
    **Erratum E3** records all five scope statements; the pinned predicates and the real-population
    readings are unchanged.
11. **Mo88Si01Simplify (simplifier, YAGNI).** 33 deletion candidates, 12 target-preserving, one
    recommended: the dead assignment `want_met = …` at `.ufo/waves/round-87/count-c2.py:121`
    (ruff F841). It correctly declines to delete it now — the after receipt binds the counter's
    sha256 `8904a3d0…`, and the deletion changes the bytes to `27121850…`, so the edit belongs to
    round 89 with a superseding receipt. Every new arm and helper was shown load-bearing by
    deletion (each deletion flips the target or the subject arm gate); the fixture tally lines are
    the only post-freeze edit and are disclosed as Erratum E1.

12. **Mo88S02Knowledge (scribe, entry review).** Verdict **ENTRY needs-changes**, on a mid-round
    snapshot of the entry. Its load-bearing defects were accepted and fixed before the entry was
    committed: (a) rule 1's "no `# replay:` line" missed the `# replay: none` normalization (the
    entry now says both); (b) rule 2's "replayed row" did not say the rule is keyed on the declared
    mode (now stated); (c) the after-receipt `source:` line named the measured revision instead of
    the commit that carries the receipt (now `9c775ac2` measuring `d5e2eda4`); (d) the S604
    locator said §5.3.7 while the heading is §5.3 and the quoted paragraph is its fifth step
    (corrected in `SOURCES.md`, `README.md` and the entry, disclosed above); (e) the "both
    problems" example was false for the frozen `stripped` fixture (its command still names the
    bound path, so only `missing-replay` fires — corrected); (f) rule 3's "outside the population"
    was both narrower and wider than the code (now "not a present basename", with the
    present-but-not-legacy limit named). Its `--selftest` and both counter runs reproduced the
    after lines from its own scratch.
