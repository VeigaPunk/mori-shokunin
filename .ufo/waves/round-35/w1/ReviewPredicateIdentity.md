measured 2026-10-23T09:08:28Z

# w1 — ReviewPredicateIdentity: P-C1 sentence vs count-c1.py code (mori round 35)

Seat MoriR35.ReviewPredicateIdentity (leaf: no subagents, no background jobs, no installs). Scope: identity of the
frozen predicate — the P-C1 sentence (contract.md:35-44, docstring count-c1.py:5-23) against the conditions `main()`
actually checks. Detection/report only; only write is this file; read-only git in the lane; no lane/fleet mutation.

## Ground truth verified before the clause map
- Counter byte-identity: `sha256sum .ufo/waves/round-35/count-c1.py` → `27b82d71…ee18167`, equal to
  `.ufo/waves/round-35/evidence/c1-freeze.txt:2`; freeze receipt also pins contract.md sha (:3) and
  MANIFEST.json@37b51a24 sha (:6).
- Docstring ≡ sentence (independent check, not the receipt's claim): whitespace-normalized span from "At the measured
  lane revision" to "missing == bad == extra == 0." is byte-equal in contract.md:35-44 and count-c1.py:5-23
  (1079 normalized chars both). Confirms c1-freeze.txt:4 `predicate_identity: … True`.
- Oracle: `git show 37b51a243302e8009c7067431e8a47f9a722fd14:MANIFEST.json` → 525 rounds, 23 with `lane=="mori"`,
  21 `capabilities_added` strings total, 18 under `admitted: true` (round 17's 3 excluded, `admitted: false`);
  admitted rounds 12, 14, 15, 16, 18(×3), 19, 22, 24(×2), 25(×2), 26, 28(×2), 31(×2) — exactly contract.md:15-16.
  All 23 mori entries carry boolean `admitted` and a `mori-shokunin@<sha>` commit; verdict strings agree with the flag.
- Counter rerun: `python3 .ufo/waves/round-35/count-c1.py dd76eb79` → exit 1, summary line identical to
  evidence/c1-before.txt: `register='## Capabilities (round 12 demonstrations)' oracle=18 rows=5 matched=0
  missing=18 bad=0 extra=5 mismatches=23 C1=unmet`. Reproduces control 1 (c1-controls.txt:11).
- Matcher edges: loaded the frozen file via importlib (no mutation) and scanned the real record text of all 18
  admitted entries; eligible strong-path universe (at_closure_commit ∩ changed-in-window ∩ prefix allowlist) = 106
  paths. Lenient-vs-strict whole-path comparison over those: zero divergent acceptances (see D3/D4).

## Clause → code map (sentence clause → counter line → match/diverge)

| # | Clause (contract.md:35-44 ≡ docstring :5-23) | Code (count-c1.py) | Match/diverge |
|---|---|---|---|
| 1 | last level-2 section whose heading begins "## Capabilities" | :67-71 (`startswith("## ")`, `## Capabilities`, `cap[-1]`, section ends at next `## `) | match (caveat D7) |
| 2 | one row per capability, keyed `rounds[i].capabilities_added[j]` | oracle keys from enumerate :127-132; row key parse :142-143; unknown key → extra :144-146; duplicate → extra :147-149 | match |
| 3 | recorded by MANIFEST@MANIFEST_REV in capabilities_added of an admitted mori closure | `lane=="mori"` :104, `admitted is True` :110, non-empty caps :111-112 | match |
| 4 | naming that closure's round | exactly 5 cells :157; cell 5 stripped of backticks/spaces equals MANIFEST round :158-160 | match |
| 5 | citing one or two evidence paths | only backticked tokens parse :161; `1 <= len(toks) <= 2` :179-180 | diverge-narrow (D1) |
| 6 | exists at the measured revision | `p not in at_rev` :169-171 (ls-tree at `full` :102,137) | match |
| 7 | any cited line range inside the file | `1 <= lo <= hi <= n` at measured rev :172-177 | match |
| 8 | exists at that closure's commit | `p in o["at_commit"]` :182 (tree at MANIFEST commit :108-109,126) | match |
| 9 | changed between the previous mori closure commit and that closure's commit | `git diff --name-only prev commit` :113; `prev = commit` per mori entry :133; FIRST_PREV for r12 :32,106 | diverge-boundary, first entry only (D2) |
| 10 | lies under tools/ \| corpus/knowledge/ \| corpus/evidence/ or is corpus/SOURCES.md | :183 + :33-34 (exact sets) | match |
| 11 | equals a tools//corpus/knowledge/ path the capability string names (when it names one) | NAMED_RE :35, `named` per key :131, `not o["named"] or p in o["named"]` :184 | match (edge D6) |
| 12 | appears as a whole path in that closure's record text (verification object, capabilities_added strings, spot-check files the object names, fleet report; all at MANIFEST_REV) | ctext = vtext + spot files + report + caps :114-125; whole_path_in :54-57; conjunction :182-186 | diverge ×3 (D3, D4, D5) |
| 13 | and it holds no other row | unknown/duplicate keys → extra :144-149; separator rows dropped :80-81; `Key`/`Capability` first-cell header dropped :83-86 | match with tolerance (D8) |
| 14 | C1=met iff matched == oracle and missing == bad == extra == 0 | `met = matched == len(oracle) and not missing and not bad and not extra` :193 | match |

## Findings by severity

### D4 — trailing-dot right anchor breaks "whole path" (latent, low; the one defect)
count-c1.py:56 is `(?<![A-Za-z0-9_./-])(?:mori-shokunin/)?<p>(?![A-Za-z0-9_/-])` — the trailing lookahead omits `.`,
although `.` IS in the leading lookbehind class. So `whole_path_in("tools/x.py", "see tools/x.py.bak")` is True
(reproduced), and the docstring's own description at :55 ("not preceded or followed by a path character") is wrong for
the trailing side. A register row citing `p` passes the record-text arm when the closure text contains only a
dot-extended neighbor of `p` (`p.bak`, `p.old`, `p.orig`); trailing punctuation (`p.`, `p:12`, `p,`) is the intended
and benign case. Direction: widening (could print met where the sentence's "appears as a whole path" says unmet).
Empirical bound: 0 of the 106 eligible paths in the frozen oracle rely on the gap; no control in c1-controls.txt
escapes through it (all skip controls unmet :11-30, mutation m11 whole-path-in-closure-text killed :47-48).
VERDICT: defect (latent, low; frozen post-data, no A1 trigger since no control met — record, do not amend).

### D2 — first-entry diff base 20e2255 (no defect found)
The sentence's "previous mori closure commit" is undefined for round 12 (mori's first MANIFEST entry); the code
substitutes FIRST_PREV=20e2255 (:32,106), commented as `1f07f1d^`. Verified in the lane: `git rev-parse 1f07f1d^` =
20e2255e7…; `git merge-base --is-ancestor 1f07f1d bf7cdc478` rc 0; 1f07f1d subject begins "round-12: source
registry…"; MANIFEST r12 closure commit is bf7cdc478 (parent a7f1ecbcb, itself a descendant of 20e2255);
`git rev-list --count 20e2255..bf7cdc478` = 3 — the window is exactly round-12's own three commits, so r12 rows
cannot be validated against pre-round-12 changes. For r14+ the code diffs against the previous mori entry's closure
commit including rejected rounds (r13 dbe85009 rejected-harmed sits between r12 and r14) — consistent with
"previous mori closure", since rejected rounds also close. The comment at :32 is accurate (1f07f1d is r12's first
commit, not the closure commit). Divergence is definitional, sentence-silent, and exact-round-scoped.
VERDICT: no defect found.

### D3 — `mori-shokunin/` prefix accepted as a whole-path occurrence (no defect found)
:56 optionally matches `mori-shokunin/<p>`; the sentence says "appears as a whole path". Documented at :55.
Strict-bare vs lenient over the 106-path universe: no path is accepted only in prefixed form (all have bare
occurrences in record text).
VERDICT: no defect found (documented widening, zero bites on frozen oracle).

### D5 — spot-check files read at embedded hash, @hash-form only (no defect found)
:116-119 reads only `mori-shokunin/<path>@<hex>` occurrences of the verification object (:39) and shows each file at
the embedded hash, not at MANIFEST_REV; the sentence's "the lane spot-check files that object names … all at
MANIFEST_REV" reads broader (any naming form, at MANIFEST_REV). Direction: narrower — missing content can only cause
weak-path/unmet, never a false met. Empirics: in every mori entry's verification JSON, every `mori-shokunin/`
mention carries `@hash` and all resolve (spot-mention count == @hash-mention count per entry, 0 unresolved). Four
bare lane-path mentions exist that the code does not ingest as file content — r22 `corpus/lessons/round-22.md`,
r22 `corpus/knowledge/freeze-order-r18.md:51`, r26 `corpus/SKILL/PROVINCE/SCORECARD`, r31 `tools/PROVINCE` — whether
these are "spot-check files" in the sentence's sense is a reading judgment; their contents are additionally absent
from ctext only if quoted nowhere else. The report file is read at MANIFEST_REV (:120-124) and all 14 admitted-entry
reports resolve; unresolvable report/spot refs are silently skipped (fail-safe).
VERDICT: no defect found (narrower than sentence; fail-safe; divergence recorded).

### D1 — evidence parsing counts only backticked tokens (no defect found)
The sentence body says "citing one or two evidence paths" with no backtick qualifier; the code parses the evidence
cell exclusively as backticked `path[:N[-M]]` tokens (:37,161,163-180), so unbackticked path-like prose is invisible
(control 9d printed C1=met and was ruled a residual, not a skip: c1-controls.txt:38-43). The backtick requirement is
supplied by the Row shape clause, contract.md:46-47, part of the same frozen contract.
VERDICT: no defect found (sentence under-specifies; contract row shape + recorded residual cover it).

### D6 — NAMED_RE final-character class (no defect found)
:35 requires the named path to end `[A-Za-z0-9_]`; a capability string naming a path with a trailing `-`, `.` or `/`
would yield an empty `named` set and loosen the named-path arm for that row. All 18 real capability strings name
well-formed paths where they name any (checked per entry). VERDICT: no defect found.

### D7 — heading detection and section boundaries (no defect found)
:67-68 counts any line starting `## `, including one inside a fenced code block, as a heading; rows under `### `
subheadings inside the section still count (sentence's "section" reading covers subsections). At base, the only
`## Capabilit…` lines in SCORECARD.md are :586 and :627 (grep), so selection is unambiguous today; a fenced
`## Capabilities` at a future tip would corrupt selection toward unmet (fail-safe).
VERDICT: no defect found (residual noted).

### D8 — header/separator tolerance (no defect found)
:80-81 drops separator rows; :83-86 drops the first row only when its first cell is `key`/`capability`
(case-insensitive). Any other header (e.g. `Manifest key`, verified synthetically: 3 rows kept) becomes an extra row
→ false unmet, the safe direction. Dropped rows can never match, so no skip program benefits.
VERDICT: no defect found.

## Code conditions the sentence body omits (all supplied elsewhere in the frozen contract or fail-safe)
1. Evidence tokens must be backticked (:161; contract.md:47). 2. Exactly 5 cells (:157; contract.md:46). 3. Header/
separator tolerance (:80-86). 4. `mori-shokunin/` prefix acceptance (:56). 5. Trailing-dot anchor gap (:56, D4).
6. Spot files only in `path@hash` form at the embedded hash (:39,116-119). 7. FIRST_PREV base for r12 (:32,106).

## Sentence clauses the code does not fully check
"appears as a whole path" — right anchor lets dot-neighbors count (D4). "…all at MANIFEST_REV" — spot files are read
at their embedded hashes, not MANIFEST_REV (D5). Both bounded empirically above; neither flips any outcome on the
frozen oracle.

## Residual risk
- D4 is the only widening gap; exploitation would require a row whose cited path is changed-in-round, at the closure
  commit, allowlisted, named-if-named, yet occurs in record text only as a dot-extended neighbor — and wave-2
  non-author reviewers read every evidence cell per the L1 ruling (c1-controls.txt:40-43). Kill rule still requires
  the byte-identical counter (verified :2 of freeze receipt).
- A future register whose header first cell is not exactly `Key`/`Capability` false-unmets (honest stop, wasted
  round) — data-seat risk, not a counter defect.
- The r12 base interpretation and MANIFEST index keys are frozen with MANIFEST_REV; any fleet-side re-baseline would
  shift keys, but the revision is pinned (:31).

## Verification gaps
- I reproduced control 1 only; the other C0 results are taken from the receipt c1-controls.txt:11-30, not rerun.
- Per-entry positive reachability (≥1 strong path per entry) is taken from CtlPositive e1463e8b matched=18
  (c1-controls.txt:33), not independently recomputed per entry.
- The CtlParserAttack seat's parser-trick battery was refused by its provider and remains unrun
  (c1-controls.txt:52-55); my synthetic header/heading/backtick/key-format tests cover part of that ground only.
- Whether the four bare lane-path mentions (D5) are "spot-check files" in the sentence's sense is reported as code
  behavior, not ruled on — that reading belongs to the L1.

Tooling installs: none (work done with stock git/python3).

Overall: VERDICT: predicate identity — no outcome-changing sentence↔code divergence found; one latent low defect
recorded (D4 trailing-dot anchor); counter sha, docstring≡sentence, oracle=18 shape and the before-receipt rerun all
verified. Counter fit for the kill rule as frozen.
