# CritLaneLine — random sample verification of the C2 lane line

Axes: membership correctness (eligible set), provenance (supersede marker), timing truth (edit-before-landing), count/prose consistency.

Verdict: **the lane line holds on substance; the wave brief's "34 as-of ids" count is wrong — the committed receipt carries 35.** Per-id verdicts below.

## Finding 1 — claim prose undercounts the as-of set: 35, not 34

`evidence/c11-after-lane.txt` timing line (verbatim, committed at `8d3badd`):

```text
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226] stale_supersede=[]
```

Count of that bracket: **35** (also `superseded=[35 ids]` on the summary line, identical set).
The wave context brief and the ExeGateLane item both say "34 as-of ids"; the frozen contract's
P-C11 parenthetical says "(19 ids)". All three misstate the committed receipt:

- The 19-id arithmetic (`18 edit-bounded + S226`) was already flagged erratum-class
  (ScrScorecardRow's M24 "parenthetical arithmetic"). The true decomposition is
  **24 edited + 11 never-edited = 35**:
  - edited (first-parent imm diffs somewhere in the walk): S041 S044 S051 S062 S064 S069
    S090 S093 S096 S097 S101 S124 S179 S180 S181 S182 S183 S184 S185 S186 S188 S189 S190 S193
  - never-edited (first sighting is the last imm touch): S067 S070 S071 S083 S084 S127
    S128 S129 S131 S140 S226 — *eleven* join the line under the eligible-set extension,
    not just S226.
- The brief's 34 matches nothing: e37dcc6 carries 33 superseded (`as_of=[33], stale=[S069]`),
  the tip carries 35. Off-by-one in the claim prose, not in the gate or the receipt.

Defect class: **claim-sizing/prose**, same family as the "(19 ids)" erratum — the claim's
real counter (the receipt, 35) is self-consistent; the counting words around it are not.

## Finding 2 — duplicate supersede claims on S069 (resolved, but worth noting)

At the tip, **two** live rows' teaches open `supersedes S069 —`: S073 (historical,
"string-only containment (relative…") and S226 ("containment is decided on the resolved
canonical path…"). P-C11's "latest superseding row's landing" rule resolves the tie to
S226 (landing `daa1d4d250`, the later first-sighting); S069 is as_of via S226. Not a
defect under the frozen words — but the gate's `superseded_by=S226` silently picks one of
two equally-marked rows. If a future round wants singular provenance, that's a spec gap,
not a v3 bug.

## Sampled verification — draw

Method: `secrets.SystemRandom().sample(<receipt as_of list>, 5)` over the 35 ids.
Draw: **S128, S093, S129, S183, S051** (sample space noted: brief says 34, actual list 35).

Independent check (not the gate): replayed `git log --format=%H%x09%P --reverse
--full-history 265a955cc -- corpus/SOURCES.md` (55 commits), parsed every state's
registry, tracked first sightings, first-parent-only imm diffs (cols
id,source,kind,tier,scope,anchor,teaches,opened — status/recheck/used-by mutable),
superseder sightings per teaches cell, and ran `git merge-base --is-ancestor` between
each id's last edit/first sighting and its superseder's landing.

| id | (i) tip | (ii) superseder row, teaches opens `supersedes S<ID> —` | (iii) history | as-of? |
|----|---------|--------------------------------------------------------|---------------|--------|
| S128 | yes | S149 (`f2de0eedcd`), verbatim `supersedes S128 — the old row said the pages' inheritance…` | never-edited since `126e192d1f`; **zero** drift commits | last sighting `126e192d1f` ancestor of `f2de0eedcd` → **PASS** |
| S093 | yes | S144 (`df886be1cc`), `supersedes S093 — anchor only: the help-text file list is lines 730-731…` | edited: imm diffs at `7c77fba329`, `df886be1cc`; drift restored by `b89ac342a9` (tip == first sighting, so absent from `ids` — consistent) | last edit `df886be1cc` is ancestor-or-equal of landing `df886be1cc` (same commit edited S093 *and* landed S144; `is-ancestor` rc=0 on self) → **PASS** |
| S129 | yes | S150 (`f2de0eedcd`), `supersedes S129 — the old row's clause "so user units inherit manager+100…"` | never-edited since `126e192d1f`; zero drift | `126e192d1f` ancestor of `f2de0eedcd` → **PASS** |
| S183 | yes | S214 (`bf0df77fee`), `supersedes S183 — part_stat_add applies an add made to a partition…` | edited `ab8f4cfe81`; tip still differs from first sighting `62db24c01d` (in `ids`, consistent) | `ab8f4cfe81` ancestor of `bf0df77fee` → **PASS** |
| S051 | yes | S208 (`bf0df77fee`), `supersedes S051 — Retention needs a current-business-purpose test…` | edited `62db24c01d`; drift persists to tip (in `ids`) | `62db24c01c`-era edit ancestor of `bf0df77fee` → **PASS** |

All five: (i) present, (ii) superseded by a tip row whose teaches opens exactly
`supersedes S<ID> —` (em dash; stronger than the gate's `^supersedes\s+(S\d{3})\b`),
(iii) never-edited or last edit before/at the superseder's landing. **Per-id verdicts: PASS ×5.**

## Full sweep (beyond the sample)

All 35 receipt ids independently satisfy (i)+(ii)+(iii): every one is present at the tip,
its tip superseder's teaches opens `supersedes <id> —` (zero loose matches lacking the
em dash anywhere at the tip), and `merge-base --is-ancestor(last_edit|first_sighting,
landing)` holds — including the self-ancestor cases (S090/S093/S096/S124 where one commit
both edited the row and landed its superseder; `git merge-base --is-ancestor df886be1cc
df886be1cc` → rc 0). `stale_supersede=[]` independently confirmed: no superseded tip id
whose last edit postdates its superseder's landing. The receipt's `changed S0xx
superseded_by=S2xx` lines and `appendonly_violations=18` also match my replay.

## Commands run

Working dir `/home/vgpnk/Projects/shokunin/mori-shokunin` throughout.

1. `git rev-parse HEAD` → `ede486b7a09afbacfb380d5871c46a8051a6dc2e` (two commits past the
   scored tip: `8d3badd` evidence, `ede486b` S229-repair). Verified the repair changed
   nothing relevant: tip-superseded set at HEAD identical (35), all 35 rows' immutable
   cells unchanged vs `265a955cc`.
2. `git show 265a955cc:corpus/SOURCES.md` (inspected header + S226/S228/S229 rows).
3. Python (stdlib `re/subprocess/secrets`, run via eval cell — no files written): parsed
   `evidence/c11-after-lane.txt`; replayed the `--full-history` walk; computed first
   sightings, first-parent imm diffs, superseder sightings, landings; ran
   `git merge-base --is-ancestor` per id; drew the 5-id sample; swept all 35.
   Embedded git calls: `log --format=%H%x09%P --reverse --full-history <rev> --
   corpus/SOURCES.md`, `show <rev>:corpus/SOURCES.md` (per commit),
   `merge-base --is-ancestor <a> <b>` (per id), `rev-parse HEAD`.
4. Read `tools/mori-sources-appendonly.py` (analyze(), parse_registry, SUPERSEDES_RE) to
   mirror semantics and deliberately diverge where the claim's words diverge (em-dash
   check, drift-from-first-sighting check that catches gate-invisible revert edits —
   found: every edited id's last *drift* state is honestly reported; no pick hid an
   unrecorded post-landing edit).

## Residual notes

- HEAD is now `ede486b` (S229 row-placement repair) — the claim measured `265a955cc`.
  The repair is post-scored-tip; the 35-id line is unchanged at HEAD (verified above),
  so no receipt invalidation.
- No tools installed. No mutations: only `write` to this report; all git calls read-only.
- Peer note: CritPredParenthetical's "34" enumeration will hit the same arithmetic —
  actual never-edited join set is **11 ids** (S067 S070 S071 S083 S084 S127 S128 S129
  S131 S140 S226), of which the contract's 19-id math missed 16 overall.
