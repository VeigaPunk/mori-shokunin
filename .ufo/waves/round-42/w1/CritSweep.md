# CritSweep — attack the errata sweep (lane-wide census of the three false r41 phrasings)

Seat: MoriR42.CritSweep (critic). Read-only sweep; judgment on whether any
occurrence of `'8/8 mutants killed'` / `'34 attack seats (53%)'` /
`'2 scouts, 4 scribes'` outside the LOG/SCORECARD round-42 records needs its
own correction.

Revisions: assigned tip `34b926730c30e0251e1aec531863d8355dc491f1` (ancestor
of HEAD — verified `git merge-base --is-ancestor`); working HEAD is
`f3ec0977` = tip + one receipts commit (`evidence/c{1,2,3}-after.txt`,
`c1-noharm-manual.txt`, `w1-spec.json`, `wave-plan.json`, LOG/SCORECARD
measured-outcome blocks). Judgment holds at both revs; deltas noted.

## Verdict

**No occurrence outside the LOG/SCORECARD round-42 records asserts a false
value; none needs its own correction.** Every lane-side hit is either (i) the
errata records themselves, (ii) the frozen claim/counter that *names* the
phrasings to kill them, (iii) the originating routed-defect record quoting
them as the defect, (iv) verbatim task strings inside the wave spec/plan, or
(v) byte-copies inside the committed `assimilation/validate/` mirror. The
only records that still *assert* the false values live in the fleet repo
(`/home/vgpnk/Projects/shokunin/.ufo/reports/round-41/mori.md`), which the
append-only protocol deliberately leaves untouched — the lane errata are the
correction, exactly as routed.

## Occurrence inventory (lane, all three phrases)

| Where | Phrase | Judgment |
|---|---|---|
| `LOG.md:2397-2409` | all three | the errata records themselves — correct |
| `SCORECARD.md:2334-2338` | all three | the errata records themselves — correct |
| `.ufo/waves/round-42/contract.md:55-61` (frozen claim) | all three | quoted to *define* the supersession; `:89` kill rule uses them as detection patterns — not assertions |
| `.ufo/waves/round-42/count-c2.py:6-12,143-144` | all three | docstring restates the frozen predicate; `:143` regexes are the detector — tool code, not records |
| `corpus/lessons/round-41-verifier-spotcheck.md:96,101-103` | all three | the *originating* routed-defect record; quoting the wrong text to name the defect is its function. `:96` even self-flags: `"8/8 mutants killed" parenthetical is wrong — 5/8`. No correction. |
| `.ufo/waves/round-42/w1-spec.json`, `evidence/wave-plan.json` | all three (inside `\n` task strings) | verbatim copies of seat prompts (mine, RevC2Errata's, MutC2Record's) quoting the phrases as attack targets — directives, not assertions |
| `.ufo/waves/round-42/assimilation/validate/**` | all three | committed mirror snapshot (11 001 files); byte-identical copies of contract/counter/lesson — same provenance as their originals |
| `.ufo/waves/round-42/w1/*.md` (untracked sibling reports, observed mid-flight) | `8/8`, `4 scribes` | all in corrective/mutation-test context (e.g. `MutC2Record.md:61` shows the counter *failing* on a planted `8/8 mutants killed` — evidence it detects) |
| `corpus/lessons/round-42.md`, `corpus/knowledge/*r42*.md`, `corpus/SOURCES.md`, `QUALITY` | — | zero hits on any phrase or variant |

Variants swept: `9/34`, `8/8 killed`, `34 attack`, `53%`, `2 scouts`,
`4 scribes` — the only lane hits are the quoted/errata contexts above plus
unrelated historical data (r26/r27/r32/r34/r40 seat counts, memory-`53%`
fixture comments; all true in their own round's terms).

## Counterexample tested

Strongest available: **`assimilation/validate/` mirror.** A byte-copy of
`contract.md`/`count-c2.py`/`round-41-verifier-spotcheck.md` exists inside
the committed mirror; a naive sweep would flag it as duplicate authority.
Fails the attack: the copies carry the same contradiction context
("superseded") and are labeled mirror-evidence, not independent records.
Second-strongest: **w1-spec/wave-plan task strings** — my own prompt, which
*lists* the false phrasings, is committed at `f3ec0977`; they are attack
targets inside directives, not asserted values. The sweep survives both.

## Residual findings (for the closure, none block the verdict)

1. **Kill-rule soundness gap (the real attack surface).**
   `count-c2.py:152-155` runs `sweep_log_clean`/`sweep_score_clean` only over
   the `r42_log`/`r42_score` *slices*, but P-C2's clause 3 says "no
   lane-owned round-42 record re-asserts a superseded value uncontradicted."
   A record added tomorrow in `.ufo/waves/round-42/evidence/*.txt` or
   `w1/*.md` asserting `8/8 mutants killed` verbatim would pass `C2=met`
   undetected — the claim is wider than its instrument. No violation exists
   today (verified `evidence/c2-after.txt` all-PASS at `34b9267`), so this is
   an instrument-coverage defect, not a false verdict. Smallest safe
   correction: extend `bad()` over `git_ls(REV, ".ufo/waves/round-42")` text
   files; all existing quoted occurrences carry `superseded`/`correct` within
   the existing ±200-char marker rule, so the widened sweep stays green.
2. **Marker looseness:** `"correct" not in ctx.lower()` accepts any
   "incorrect"/"correction" prose within 200 chars. Suggest an explicit
   allowlist (`superseded`, `erratum`, `correction`).
3. **Unnamed superseded token `9/34`:** the routed defect also quoted
   `"attack seats returned 9/34"` (`mori.md:143`). The errata name
   `34 attack seats (53%)` but not `9/34` verbatim; the fix is nonetheless
   complete because 9 is the *correct* numerator (9 attack seats of 31 did
   return) and `9/34` occurs in no lane record outside the spotcheck quote.
   Hygiene, not correctness: naming `9/34 → 9/31` in (b) would close it.
4. **Out-of-lane residue:** the fleet report itself still reads
   `8/8 mutants killed`, `= 34 attack seats (53%)`, `2 scouts, 4 scribes`,
   `attack seats returned 9/34` (`/home/vgpnk/Projects/shokunin/.ufo/reports/
   round-41/mori.md:127,143`). Per protocol this is corrected by the appended
   lane errata, not edited — noted so the closure knows the superseded text
   persists by design in the fleet.

## Tooling

None installed or updated (sweep used in-repo git/grep only).

Report: .ufo/waves/round-42/w1/CritSweep.md
