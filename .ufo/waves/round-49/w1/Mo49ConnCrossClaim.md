# Mo49ConnCrossClaim — cross-claim pattern finding (round 49, wave w1)

Seat: `Mo49ConnCrossClaim` (connector, leaf — no subagents). Lane: mori-shokunin.
Round: 49, wave w1. Machine: MACHINE_ID. Date: 2026-10-25.
Method: read-only inspection of the frozen contract, both frozen counters, the round-48/47/45
lessons, the round-48 w1 crit reports, `corpus/QUALITY.md`, `corpus/SOURCES.md` and the committed
source copies at the freeze `0df17b7b`. No tool was installed (nothing was needed; all reads were
`read`/`grep`/read-only `git ls-tree`). No lane tool was executed; no scratch was used; TMPDIR was
not needed. All line numbers below name the frozen bytes at `0df17b7b` (counters) or the entering-tip
bytes of `corpus/lessons/` and `corpus/QUALITY.md` as read from the worktree (unchanged by this seat).

## 1. What connects C1 and C2 (shared architecture)

Both claims are **verdict conjunctions over a named sample set**, scored by a frozen counter that a
wave seat measures only after all data is committed:

- C1 (`count-c1.py`) stages 26 variants — 18 junk (J1-J8, N1-N10), 7 honest (H1-H7), plus the real
  registry twice — and demands `junk_met=0 honest_unmet=0 real=met errors=0` (`count-c1.py:298-306`).
- C2 (`count-c2.py`) demands an entry with ≥8 rows, ≥3 distinct sources, every quote located in the
  committed copy, every S-row mined/opened/used-by correct, and provenance pins (`count-c2.py:99-193`).

The shared design invariants:

1. **Both counters accept shape without entailment.** C1's junk variants are all *well-formed
   surface shapes* (a gates-table row, a backticked tally, `pass=N fail=0`) that state wrong
   contracts — the do-nothing control scores `junk_met=9` (N1-N9 all `met`, contract freeze table).
   C2's predicate proves a quote *occurs* in a copy (`located`), not that the claim cell follows from
   it — the contract names this limit verbatim ("a located quote proves the quoted words occur in the
   committed copy, not that the claim cell follows from them", contract §C2 named limits; QUALITY
   128 "the counter proves location, not entailment"). The round-48 C2 crit demonstrated the union:
   eight script/config fragments scored `C2=met` with claims that assert unrelated facts
   (`w1/CritC2Counter.md:5-9`).
2. **Both counters are scored by a harness the object under test can see.** Round 48 proved the
   C1 harness leaked its variant filenames and scratch names (`w1/CritC1Counter.md:26-45` — `tool_a_filename_keyed.py`
   scores `C1=met` by reading `skill`'s basename). Round 49 closes it with opaque handles: stag files
   and scratch dirs are named by sha256 prefixes of their bytes, run order follows the hash, and the
   fixture variants live in a throwaway repo (`count-c1.py:216-245, 248-278`); the selftest arm
   `filename_sniffer_not_met` proves a filename-keyed tool is blind (`count-c1.py:392-402`). C2's
   harness-visible surface is the **source set itself**: the entry author sees the four pinned copies
   and their URLs (`COPIES`, `count-c2.py:36-45`) and the S-row shape, so a quote can be borrowed
   from anywhere in a copy (`quote_from_wrong_copy_unmet` arm, `count-c2.py:295-297`) or from
   structural text. The sources cannot be made opaque (rows must cite public S-ids), so C2's residual
   exposure is its named limits: located ≠ entailment, and the host receipt is a one-day capture
   (contract: journal total moved 269M → 56M within one day).
3. **Both predicates are floors over a countable sample, not certificates of the open class.** C1's
   "a tool can pass by being narrower than the junk" and C2's "not that the page is unchanged today"
   are the same epistemic shape: green certifies the frozen named set under the frozen counter, never
   the class (contract §C1/§C2 named limits).
4. **Both include a mandatory honest/real leg.** C1: H1-H7 plus the real registry must be `met`
   (`stub-always-unmet` → `honest_unmet=8 real=unmet`, contract freeze table). C2: the entry itself
   must parse and the provenance pins must hold (`entry_absent`, `provenance` failures). A grader
   that rejects everything fails both.

## 2. Shared failure classes (with evidence pointers)

**F-A. Shape-without-entailment — textual presence accepted as semantic role.**
- C1: junk variants N1-N9 are shape-valid rows that misstate the contract (e.g. N5 a second
  authority for the same command with a contradicting exit map; N6 a pin-less row plus prose
  `fail=0` and a continuation `fail=3`; N8 the reconciler row re-pointed to the unlanded check)
  (`count-c1.py:80-145`). Precedent: round-47 M2 "it checked values, not visibility"; round-48 M2
  identical wording (`round-47.md:65`, `round-48.md:112`).
- C2: a located-but-not-entailed quote passes (QUALITY 128; `w1/CritC2Counter.md:9`; contract named
  limit). Precedent: round-47 M3 "exactly three named tracepoints" from a sentence that says "such
  as" (`round-47.md:66`); round-48 w1 six claim/quote pairs a reader rejects (`round-48.md:138-139`).

**F-B. Structural hiding — token placed where the parser does not look.**
- C1: N1 (gate row inside an HTML comment), N3 (tab-indented row in a fence), N4 (four-space
  indented pipe outside a table), N7 (HTML table markup), N2 (NBSP in the header, ZWSP in the pin
  token) (`count-c1.py:80-123`). Ancestors: round-47 M2 v8 "hidden row plus duplicate"
  (`round-47.md:65`); round-48 v3 survivors "an HTML comment around a row … a tab-indented row … a
  row indented four spaces outside a table … HTML table markup" (`round-48.md:164-165`).
- C2: `normalise()` drops script/style/comment blocks and the parser skips fences — the round-48
  survivor "script/style/comment text in a copy" is a named C2 control, and the selftest arms
  `normalise_drops_script_text/style_text/comment_text` and `table_inside_fence_unseen_unmet` exist
  (`count-c2.py:59-64, 338-346`). Same hiding surface as C1 N1/N3/N7, one counter later.

**F-C. Harness-visible scoring surface (identity instead of content).**
- C1: round-48 F1 (variant filename sniffer) closed this round by opaque handles (`count-c1.py:216-245`;
  selectedftest arm at `:392-402`).
- C2: the author-controlled surface is the S-row + quote cells; the counter verifies shape/provenance
  but cannot verify that the quote was chosen because it supports the claim (`w1/CritC2Counter.md:9`).
  The round-48 F1 class's C2 analogue is therefore *not closed* — it is the named limit.

**F-D. Below-floor neutrality / padding.**
- C2: `claims_floor=8`, `sources_floor=3` — rows beyond the floor carry no substance requirement; the
  round-48 eight-script-row example used exactly 8 rows across 3 sources to reach `met`
  (`w1/CritC2Counter.md:5`).
- C1: 26 variants and a 26-pin floor; the frozen set is the whole predicate, so "narrower than the
  junk" is a named pass mode (contract §C1 named limits).

## 3. The class that appears in rounds 45, 47 and 48

Grep of the three lessons shows one class in all three: **a graded token is credited for its
textual/structural placement rather than its semantic content** — in two sub-forms:

- *Presence/shape credited as semantics:* round-45 M2 — the round-44 ledger counter accepted rows
  that merely contain `@REV@` ("`@REV@` presence is textual, not semantic", `round-45.md:169`; QUALITY
  117 "not informativeness"); round-47 M2/M3 — "checked values, not visibility" and a count-shaped
  phrase from "such as" (`round-47.md:65-66`); round-48 M2/M3 — "it checked values, not visibility"
  and hidden/decoys tallies (`round-48.md:112-113`), plus script fragments in the C2 copy
  (`round-48.md:126`).
- *Hidden-in-comment / structural placement:* round-45 M1 — the auditor credited a `--selftest`
  inside a comment (`round-45.md:168`; QUALITY 120); round-47 M2 v8 — hidden row plus duplicate
  (`round-47.md:65`); round-48 — N1/v3 survivors (HTML comment around a row, etc.)
  (`round-48.md:164-165`).

Round 45's Carrier section states the class for the entry counters ("none reads the prose a figure was
transcribed from or the carrier a quote came from … still passes all three", `round-45.md:207-214`),
which is the direct ancestor of round 48's C2 crit and this round's C2 named limits.

## 4. The single QUALITY.md sentence stating the shared rule

Proposed lead sentence (for a "Criteria added round 49" criterion in the existing numbered style, cf.
QUALITY 125-128):

> **A counter's `met` is a false green when it certifies a token's textual shape or location — a
> well-formed junk row (C1) or a located-but-not-entailed quote (C2) — rather than the semantic role
> the claim assigns that token.**

This unifies QUALITY 125 ("counts what it cannot see"), 126 (junk + honest together) and 128
("proves location, not entailment") into one rule that both round-49 counters already instantiate:
C1's opaque handles remove the harness-identity channel and C2's located rows still leave the
entailment channel open, so the sentence is the shared, not-yet-stated invariant of the two claims.

## 5. Where the two claims' fixes could interfere

- **No direct file interference — verified.** C2's reader touches only `corpus/knowledge/journal-reach-r49.md`,
  `corpus/SOURCES.md` and `corpus/evidence/sources-r49/*` (`count-c2.py:29-45, 196-201`); the C1
  tool reads only SKILL.md tables (`controls/tool-v3-entering.py:35-47`) and the C1 counter stages
  SKILL.md text (`count-c1.py:248-278`). The literal "a SKILL.md edit for one that moves a pin the
  other reads" does not exist: C2 reads zero SKILL.md bytes. The only shared artifact is the revision
  R itself — each counter must be run at the landed tip R where its own files are committed
  (Separability holds; contract §Separability).
- **C1's fix is self-anchored (HIGH).** `count-c1.py` imports round-48 variants J1-J8/H1-H4 and
  adds N5/N8/N9, which anchor on SKILL.md tokens: N8 hard-requires *exactly one* row containing both
  `python3 tools/mori-pin-check.py --selftest` and a `PIN_CHECK_SELFTEST pass=\d+ fail=0` pin
  (`count-c1.py:126-137`); N5/N9 require a `PIN_CHECK_SELFTEST` pin (`:101-107, 140-145`);
  `_cur_pin` raises `Anchor` when the prefix is absent (`:73-77`). A C1 tool fix that renames,
  merges or removes that row turns variants into setup errors (`Anchor` → `C1_SETUP`, `errors≠0`) and
  fails the claim. The fix must preserve the reconciler's own row shape and the
  `UNLANDED_SELFTEST` pin N8 reads.
- **C2's S-ids are a reservation hazard (MED).** The contract names S485-S488 as the entry's rows
  and S351 stays a rejected row with a *new* superseding row (`teaches` opens "supersedes S351 —").
  The round's assimilation renumbers staged rows (S516/S532/S560) by document; if the renumber map is
  computed before S485-S488 are appended/reserved, staged rows could land on them — the round-45 M8
  class exactly (`round-45.md:175`). Also, the S351 flip must be a new append-only row, not an
  in-place edit (QUALITY 113).
- **Census duplicate-url W04 growth (LOW).** The journalctl(1) URL already occurs in S351 and S470
  (`corpus/SOURCES.md:247-249`); the new `journalctl.1.html` S-row repeats the page URL. The round
  start census is 21 lines (20 W04 + ok); the round end census will carry more W04 lines — no receipt
  should pin 21 lines. Census exit 0 is unaffected (warnings are non-fatal).
- **No scratch/TMPDIR conflict.** C1 writes under `.scratch/c1-*` (and its fixture repos); C2 writes
  nothing. Both are `git show`-only against the lane.

## Findings

- **HIGH** — C1's fix is self-anchored: N5/N8/N9 and the imported round-48 variants anchor on
  SKILL.md tokens (`PIN_CHECK_SELFTEST`, `UNLANDED_SELFTEST`, the reconciler row); renaming them
  turns variants into `C1_SETUP` (`count-c1.py:73-77, 101-107, 126-137, 140-145`).
- **MED** — C2's S485-S488 must be reserved before the assimilation renumber map is computed, or
  staged rows could land on them (round-45 M8 class; `round-45.md:175`; contract §C2).
- **MED** — The S351 flip must be a new append-only row superseding S351 (QUALITY 113), never an
  in-place edit of the rejected row (`corpus/SOURCES.md:248`).
- **LOW** — The journalctl(1) URL is already duplicated (S351, S470); the new journalctl.1.html row
  adds more census W04 warnings — the round-end census line count will exceed the start's 21
  (`corpus/SOURCES.md:247-249`; contract §Frontier).
- **LOW** — No cross-claim file interference exists by construction (C2 reads no SKILL.md byte; C1
  reads no SOURCES/entry byte); the shared artifact is revision R only (`count-c2.py:29-45, 196-201`;
  `controls/tool-v3-entering.py:35-47`).
- **LOW** — The round-48 harness-leak class (F1 filename sniffer) is closed for C1 by opaque handles
  but persists for C2 as the named entailment/freshness limit — it is not a defect, it is the
  predicate's boundary (`count-c1.py:216-245, 392-402`; `w1/CritC2Counter.md:9`).
