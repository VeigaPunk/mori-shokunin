# Scout — every item routed or carried into round 31

Seat `MoriR31.ScoutCarriedDebt`, read-only. Read 2026-10-22 after the wave-1 dispatch (`.ufo/waves/round-31/wave1-run.json`,
20:42). No tool installed; no file written outside this report; no git command beyond `status --porcelain`.

Sources read: spotcheck §7 (`corpus/lessons/round-30-verifier-spotcheck.md:176-196`), the carry lines in
`corpus/lessons/round-30.md:221-224,226-235`, the round-30 sections of `SCORECARD.md:1802-1825` plus the new round-31
appended corrections `SCORECARD.md:1843-1846`, and contract `Repairs` `.ufo/waves/round-31/contract.md:100-108`.

## 1. Observed state at read time

- `git status --porcelain` → ` M LOG.md`, ` M SCORECARD.md`, `?? .scratch/`, `?? .ufo/waves/round-31/{w1/,evidence/census-start.txt,wave1-*}`.
  The only landed repair text at this moment is uncommitted: D7 in `LOG.md:2009-2011`, D8 in `SCORECARD.md:1843-1846`.
- Absent (`ls` exit 2): `tools/mori-blind-check.sh`, `corpus/knowledge/watchdog-identity-r31.md`,
  `corpus/lessons/round-31.md`, `corpus/evidence/sources-r31/`. Both count claims are therefore still `unmet`.
- The round-30 sections of `SCORECARD.md` (`:1802-1825`) carry no separate carry list. The declaration `:1802-1814` and the
  measured outcome `:1816-1825` name only the C1/C2 counters, the "Held" axes and the tip receipts; the only
  "carried" wording just above is the round-**29** row's "counter holes carried: lesson M1" (`:1796`).

## 2. Routed defects D1–D9 (spotcheck §7)

| # | Item (spotcheck line) | Owner file | What closes it | Contract `Repairs` routes it? |
|---|---|---|---|---|
| D1 | Blindness gate parser reads past the files-opened list, reports only the first hit per file, self-test locks in the `CaseA210c`/missing-list false positive (`:176-178`) | `tools/mori-blind-check.sh` (new) | Predicate P-C2 (`contract.md:59-75`): run on the 16 frozen fixtures, `exact=16/16`, `blind_violations` equal to hit count, exit 1. Fixtures F01/F02/F03 encode the prose-after-list, multi-hit and label-form shapes (`c2-fixtures.json`). Counted. | Yes — "D1 is C2's substance" (`contract.md:102-103`) |
| D2 | A1 silently loosened condition 3a; A3 is no precedent; no `## Mistakes` row (`:179-181`) | `corpus/lessons/round-31.md` `## Mistakes` [INFERENCE: file does not exist; contract names no file] | One mistake row citing QUALITY 25 (`corpus/QUALITY.md:50`). No counter; `LOG.md` entry per `contract.md:100`. | Yes (`:103-104`) |
| D3 | QUALITY 93 cannot fail; supersede by a new row naming it; QUALITY 92 unmet at tip (`:182-183`) | `corpus/QUALITY.md` (new row after `:656`) [INFERENCE: contract names no file] | New row naming 93; "QUALITY 92's unmet state recorded". No counter. The location of the 92 record is not named (lesson? SCORECARD? the new row?). | Yes, but the 92 half is under-specified (`:104`) |
| D4 | Entry `:53` "reports its version" corrected at every mention; S159/S120 `Restart=always` overlap handled (`:184-186`) | `corpus/knowledge/earlyoom-invocation-scope-r30.md:53` (append); S159 half likely `corpus/SOURCES.md` S159 row [INFERENCE: not named] | Appended corrected text at the single real mention (grep for the phrase hits only `:53` outside the lessons that quote the defect), QUALITY 77. No counter. | Yes (`:104-105`) |
| D5 | Coverage-map row for `knowledge/earlyoom-invocation-scope-r30.md` (`:187`) | `corpus/README.md`, `## Coverage map` (header `:3`, rows from `:26`) | Row present. No counter; grep for the entry name in `README.md` still prints nothing. | Yes (`:105`) |
| D6 | Pin the X1/X2 dry-run flips (`KILLERS_QUIET` → `KILLER_ACTED`, unreachable from stock earlyoom 1.9.0) as cases, named in the carry list (`:188-189`) | "a new fixture file" — **no path named** (`contract.md:105-106`) | Cases present and pinned in a new file, no existing fixture changes. Not read by C1 or C2; no counter. | Yes, but owner path unnamed and unmeasured |
| D7 | LOG entry for landed change `713be294` (`:190`) | `LOG.md` | Appended entry. Present already in the working tree, `LOG.md:2009-2011` (uncommitted). | Yes (`:107`) |
| D8 | SCORECARD correction: round-30 C1 counts (`new_ids=5` vs tip `4`) and the stale C2 condition-4 parenthetical (`:191-194`) | `SCORECARD.md` | Appended correction. Both halves present, `SCORECARD.md:1843-1846` (uncommitted): C1 at `:1845`, parenthetical note at `:1846`. | Yes (`:107-108`) |
| D9 | Note only: redacted policy tokens in pushed history `d03203c5`; scratch original not durable (`:195-196`) | None | No repair; a note. Contract says "D9 noted" with no anchor file or line. | Yes, as note-only (`:108`) |

All nine D-items are named by the contract's `Repairs` paragraph. `Repairs` itself names an explicit file only for D4,
D5 and D8; D1's tool path sits in the C2 section (`contract.md:59`); D2, D3, D6, D7 and D9 name no path.

## 3. Carried items outside D1–D9

| # | Item (source line) | Owner file | What closes it | Routed? |
|---|---|---|---|---|
| B1 | Gate parser / M6 (`round-30.md:221`) | same as D1 | same as D1 | Yes (= D1) |
| B2 | QUALITY 93 (`round-30.md:221`) | same as D3 | same as D3 | Yes (= D3) |
| B3 | Uncounted last-invocation send: a non-active `KILLER_ACTED` can show every counter at 0 (`round-30.md:221`; entry `:56-58`, "Routed to the tool as a named residual") | `tools/mori-oom-killers.py` | A counter for that send, or a stated limit in the tool's docs. | **No** — absent from `contract.md:100-108`; C1 is watchdog identity, C2 is the blindness gate |
| B4 | Retention policy blind to unit/pid/cmdline shapes (SentinelPrivacy F1, `round-30.md:222`) | retention scan (fleet/lane scripts) | A shape rule with a red control. The round-31 privacy bound only says "must not rise" (seat bounds), which is no-harm, not a repair. | **No** |
| B5 | S159/S120 `Restart=always` overlap (`round-30.md:223`) | S159 SOURCES row | Overlap noted/merged. | Yes (= D4 second half) |
| B6 | `corpus/README.md:337` stale `fleet-ledger` pointer (ReviewProvinceFix, `round-30.md:223-224`) | `corpus/README.md:337` (FR4 row) | Repointed link. Observed: the row cites `../../fleet-ledger/.ufo/waves/kaika-w1/mori-state.md:31,190` and `/home/vgpnk/Projects/shokunin/fleet-ledger` does not exist (`ls -d` → No such file or directory). | **No** — D5 routes a different README edit (the coverage row) |
| B7 | QUALITY 92 unmet at tip, `limit_stated=no` (`round-30.md:228-229`) | `corpus/QUALITY.md:599` | Either the missing limit line is added, or the unmet state is recorded. | Only the "recorded" half (D3, `:104`); the criterion itself is not repaired and the record's location is unnamed |
| B8 | QUALITY 89 vacuous on an absence-free lesson (`round-30.md:229`) | `corpus/QUALITY.md:486` | A red control or a superseding row. Not in the `:221` residual list and not a D-number. | **No** |
| B9 | `ReviewR30Cases` rules `unclear text` on the `verdict`/`exit` pins of all eight frozen r30 cases (`round-30.md:226-228`) | freeze file + later freeze | A later freeze with clear pins. Contract `:25` says "Not re-claimed: the round-29/30 disputed-shape blind-case freeze. C2 is the gate a later freeze would depend on." | Deferred by decision, not routed as a repair |
| B10 | Gate verdict depends on the caller's checkout path (lane 1 hit vs clone 4; `round-30.md:229-230`) | new gate | Explicit inputs rather than cwd-relative discovery. The C2 interface passes lane-rev and wave dir as arguments (`contract:59-75`), which addresses it [INFERENCE: not named in the contract]. | **No** as a line item |
| B11 | `ReviewSkillRound30` F1/F2, SKILL `## Round30` row 4 over-claim (`round-30.md:230-231`) | `SKILL.md` | Fixed in the round-30 batch, per the lesson. | Closed in round 30 |
| B12 | Retention redaction at `d03203c5` (`round-30.md:233-235`) | none | Note only. | Yes (= D9) |

## 4. Flags

1. **B3, B4, B6 and B8 are carried but not routed.** They appear in the round-30 lesson's "Residuals carried to round 31"
   (`round-30.md:221-224`) or in the late wave-2 findings (`:229`) and have no D-number and no sentence in
   `contract.md:100-108`. B6 is still open on disk (the referenced sibling repo is absent). B8 is not even in the
   lesson's own residual sentence, so it exists only in the prose above it.
2. **QUALITY 91 is the highest-severity gap, and it hits C2 rather than a repair.** `corpus/QUALITY.md:580-592` says a gate
   enters a counted condition "only with a committed `--selftest`", and "a gate without it may be an observation, never a
   counted condition, and its result can neither certify nor sink a claim." C2 is a counted condition whose gate is the
   new `tools/mori-blind-check.sh`; the contract's interface for it is four positional arguments with no `--selftest`
   (`contract.md:71-74`), `count-c2.py` contains zero occurrences of `selftest` (`grep -c` → 0), and `rule-text.md` does
   not mention it. So C2 as frozen may be uncountable under the lane's own quality row. Fix: either add a committed
   `--selftest` to the tool, or amend the contract before data to state the QUALITY 91 argument.
3. **D1's self-test clause is asserted but unmeasured.** `contract.md:102-103` says "its self-test drops the locked-in
   `CaseA210c|writer-missing-files-opened-list` false positive", but neither P-C2 nor its controls run a self-test. The
   round-30 gate's selftest really does expect that false positive (`check-blind-wave.sh:176` lists both the
   missing-list and forbidden-path rules for `CaseA210c.md`). Fixture F03 (`c2-fixtures.json`, label-form list, expected
   hits `[]`) covers the parser outcome; the self-test mechanism is not covered.
4. **No repair is measured.** `contract.md:100` binds each repair to a `LOG.md` entry only; neither counter reads
   `corpus/QUALITY.md`, `corpus/README.md`, the entry, the S159 row or the D6 fixture file. Repair compliance is
   therefore prose plus LOG, not a receipt.
5. **D7 and D8 are already solved in the working tree but not committed.** `LOG.md:2009-2011` cites `713be294` with a
   `git show --stat` summary; `SCORECARD.md:1845-1846` carries both D8 halves. If the wave-1 batch commits, they close;
   if not, both remain open at any lane revision.
6. **D3's "QUALITY 92 unmet state recorded" has no named destination,** and B3's entry already says it is "routed to the
   tool" — a reader may mistake that for a round-31 route. It is not one: the contract never mentions it.
7. **D9 has no note anchor.** "D9 noted" (`contract.md:108`) names no file; unlike D7/D8 there is no append-only line a
   closure can point at.

## 5. Remaining unknowns

- Whether the L1 intends `tools/mori-blind-check.sh` to ship `--selftest` outside the frozen contract (a pre-data
  amendment would be needed; none exists at read time).
- Where D2, D3 and D6 are expected to land (`corpus/lessons/round-31.md`, `corpus/QUALITY.md` and a new fixture file are
  inferences from lane convention, not contract text).
- Whether B3/B4/B6/B8 are deliberately dropped or accidentally missing from the `Repairs` paragraph; nothing in the
  contract says either way. Confidence that they are unrouted: high (direct read of `:100-108`).
