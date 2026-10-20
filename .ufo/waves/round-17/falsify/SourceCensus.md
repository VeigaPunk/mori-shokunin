# SourceCensus-4 — independent recount of `corpus/SOURCES.md` (round 17, wave 2)

Seat: `MoriR17.SourceCensus-4` (leaf scout; no dispatch, no VCS mutation, no writes outside this
report). Assignment: independently recount SOURCES rows, tier/status histograms and
immutable/mutable changes from entering `24526ea` to the measured branch; run the maintained
source-census command read-only and record rc/stdout; check all old→new transitions are logged.

Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Measured commit per
`.ufo/waves/round-17/PINNED_INPUTS.json` is `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7`
(`refs/heads/master`); the branch tip at recount time is
`5c1dfb8d0530c74eb0e1630c2b522b735b486274` (one later commit: "committed claim measurements
and preservation receipts"). The two revisions carry byte-identical `corpus/SOURCES.md`
(both sha256 `59c6d4a14a258037125eaced3b828a132cbc45ce758aad791dc0455e91cc381f`, equal to the
working-tree file), so the recount is valid at the measured commit and at the current tip.

## Commands run (all read-only; no installs/upgrades were needed)

| # | Command | rc | stdout (exact) |
|---|---|---|---|
| 1 | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` | 0 | `mori\tW04\tS035 duplicate url …systemd.catalog.in across scopes` / `mori\tW04\tS037 duplicate url …journal-fields.html across scopes` / `mori\tok\t/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` |
| 2 | same command, output piped to `sha256sum` | 0 | `72ffb4bfdef8ec5bc67bd21444a3a3fd88527d7f09ee21ffd9e03c7d639a6231  -` |
| 3 | `scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin mori` | 0 | `mori rows 48`; `tier.A 45 tier.B 2 tier.C 1`; `status.mined 25 status.queued 22 status.rejected 1`; FLEET identical plus `tier.invalid 0 status.invalid 0 missing 0` |
| 4 | independent Python parse of `git show <rev>:corpus/SOURCES.md` (regex `^\| S[0-9]{3,}`, split on `|`, assert NF=11) | 0 | table below |
| 5 | independent `awk -F'\|' 'NF==13 && $2 ~ /^ *S[0-9]{3,} *$/'` histogram | 0 | `24526ea rows=40 A=37 B=2 C=1 mined=19 queued=20 rejected=1`; `273aa74 rows=48 A=45 B=2 C=1 mined=25 queued=22 rejected=1`; `5c1dfb8` identical to `273aa74` |
| 6 | `git --no-optional-locks diff --numstat 24526ea 273aa74 -- corpus/SOURCES.md` | 0 | `11\t0\tcorpus/SOURCES.md` |

Command 1's stdout hash equals the recorded `stdout_sha256` in
`.ufo/waves/round-17/evidence/sources-census-end.json`; the recorded argv there is byte-identical
to command 1. Command 3's numbers equal the `stdout` recorded in
`.ufo/waves/round-17/evidence/source-count.json` and the lesson/LOG claim.

Attempted-but-impossible without a write: running `validate` against the `24526ea` blob. The
maintained tool has no revision selector and `--file` requires a regular file
(`scripts/sources-census.sh:498`); no write/scratch is permitted for this seat. See Limits.

## Independent recount (commands 4+5; three implementations agree)

| Revision | rows | tier A | tier B | tier C | mined | queued | rejected |
|---|---|---|---|---|---|---|---|
| `24526ea` (entering) | 40 | 37 | 2 | 1 | 19 | 20 | 1 |
| `273aa74` (measured) | 48 | 45 | 2 | 1 | 25 | 22 | 1 |
| `5c1dfb8` (branch tip) | 48 | 45 | 2 | 1 | 25 | 22 | 1 |

Delta: +8 rows, all tier A; +6 mined, +2 queued, rejected held at 1. This is exactly the
lesson claim at `corpus/lessons/round-17.md:56-57` and the LOG claim at `LOG.md:1144-1145`
(`SOURCES40→48 … six mined by two new knowledge entries and two queued`) and `LOG.md:1178-1179`
(`count40→48/A37→45/mined19→25`). `source-count.json` records the same two histograms with rc0.
No id reuse/removal: added `S041`–`S048`, removed none, zero duplicate ids in both revisions.

## Append-only and mutable-cell check

Contract definition — CORPUS.md:116 (`## SOURCES.md … Rules`, rule 2): "**Append-only.** Only
`status`, `recheck` and `used-by` change in place, and each change is logged old→new in the round
lesson." Prompt `/.ufo/prompts/mori-round-17.md:52-54` repeats: every status/recheck/used-by change
is logged old→new in the lesson.

Observed at row/cell granularity (command 4, all 11 columns compared after stripping cell
padding; command 6 confirms line-level):

- Immutable cells (`id`, `source`, `kind`, `tier`, `scope`, `anchor`, `teaches`, `opened`): **0
  changes** on the 40 pre-existing rows.
- Mutable cells (`status`, `recheck`, `used-by`): **0 in-place changes** on the 40 pre-existing
  rows. The lesson sentence "No existing status, recheck or used-by cell changes. Thus there are
  no old→new mutable-cell transitions on existing rows" (`corpus/lessons/round-17.md:57-58`) is
  true.
- The entire file diff is 11 insertions, 0 deletions (command 6): the 8 new rows plus one
  `## Paths` line and one `## Search log` line. Nothing before them was modified, not even
  whitespace.

## Old→new transition logging

The only "transitions" this round are the 8 row creations; there are no in-place old→new cell
transitions to log. The creations are fully logged:

| New row | tier | status | used-by (exists on disk) | lesson status statement |
|---|---|---|---|---|
| S041 | A | mined | corpus/knowledge/seat-terminal-status-r17.md | `:56` S041 mined |
| S042 | A | queued | — | `:57` S042 queued |
| S043 | A | mined | corpus/knowledge/seat-terminal-status-r17.md | `:56` S043 mined |
| S044 | A | mined | corpus/knowledge/jj-branch-anchor-r17.md | `:56` S044 mined |
| S045 | A | mined | corpus/knowledge/jj-branch-anchor-r17.md | `:56` S045 mined |
| S046 | A | mined | corpus/knowledge/jj-branch-anchor-r17.md | `:56` S046 mined |
| S047 | A | mined | corpus/knowledge/jj-branch-anchor-r17.md | `:56` S047 mined |
| S048 | A | queued | — | `:57` S048 queued |

- `corpus/lessons/round-17.md:56` reads byte-exactly `S041/S043/S044/S045/S046/S047 enter mined`,
  `:57` `S042/S048 enter queued` — all eight statuses are stated; 6+2 reconciles with the
  histogram delta.
- The Gate table at `corpus/lessons/round-17.md:43-50` carries URL, access date ("All access dates
  are **2026-10-20**", `:42`), location and verbatim quote for all eight; quote word counts
  measured from the lesson are 21/21/5/25/21/11/24/13, all ≤25.
- Opening receipts exist for all eight as `build/Src{Rfc6585,Rfc9110,ZaiErrorCodes,JjGitCompat,
  JjMetaedit,GitMergeBase,GitSymbolicRef,PacmanLog}.md`, each with URL, 2026-10-20 access date and
  quote.
- The registry's own `## Search log` entry (added line, member of the 11) states "identified 8,
  screened 8, included 8 as S041–S048, excluded 0. Six are mined by the two new knowledge notes;
  Retry-After and LogFile remain queued" — consistent with the rows and histograms.
- `used-by` citations are real: `seat-terminal-status-r17.md:1` cites S041/S043;
  `jj-branch-anchor-r17.md:1` cites S044/S045/S046/S047.
- Status semantics hold (CORPUS.md:103): every `mined` row has a non-`—` used-by (no W03), every
  `queued` row has `—`; all used-by paths exist (E11 clean, `validate` rc0).

## Controls against a shared-parser artifact

- Maintained awk census (rows 48/A45/B2/C1/25/22/1) and my Python parse agree at the tip, and the
  Python parse agrees with the recorded entering histogram. The two parsers are independent
  implementations.
- Row-shape edge cases checked in both revisions: zero rows indented 1–3 spaces, zero rows at
  4+ spaces (the maintained parser's 0–3 vs 4+ rule cannot change the count); rows are all in
  `## Registry`, so no E12 row-shaped source outside it.
- Duplicate-URL control: exactly the two pre-existing URLs (S035, S037) duplicate in both
  revisions — the same two `W04` warnings appear in the recorded start receipt
  (`evidence/sources-census-start.txt:1-2`, `exit=0`) and in my rerun. No new URL collision is
  introduced by S041–S048.
- Kinds of the 8 new rows are `spec`/`docs`, never `community`; E10 (community at tier A) cannot
  apply, and `validate` rc0 confirms no E01–E12.

## Limits / unresolved

1. **Entering-side `validate` rc0 is receipt-observed, not re-executed.** The start receipt
   (`evidence/sources-census-start.txt`) records the identical two W04 lines and `exit=0`, and my
   independent parse of the committed `24526ea` blob shows every validate precondition holds
   (40 rows NF=11, unique `S###` ids, enums {A,B,C}/{mined,queued,rejected}, opened dates are
   past/present ISO 2026-10-19 ×34 and 2026-10-20 ×6, used-by targets present). Re-executing the
   maintained validator on the old bytes
   needs a materialized file, which this seat may not write. Conclusion "start rc0" is therefore
   `[INFERENCE]` on receipt + parse, not a direct observation.
2. The measured commit (`273aa74`, PINNED_INPUTS) is one commit behind the branch tip
   (`5c1dfb8`). SOURCES bytes are identical at both (`59c6d4a1…`), so no count is tip-sensitive.
3. The census claim is about registry counts and transition logging only; quote/source fidelity of
   the eight pages was sampled (receipts present, word bounds measured) but not re-fetched — those
   network reads are outside this seat's read-only receipt scope.

## Verdict

**No defect found in the attacked scope.** Independently reproduced: 40→48 rows; tier
A37→45/B2/C1; status mined19→25/queued20→22/rejected1; append-only diff 11/0 with zero changes
to immutable cells and zero in-place mutable-cell transitions; all eight new-row statuses and
opening receipts logged; maintained `sources-census.sh validate` rc0 with stdout byte-identical
(hash `72ffb4bf…`) to the recorded end receipt, and `census` rc0 with the same histograms. This is
not a blanket pass: it covers row counts, tier/status histograms, cell mutability/append-only,
transition logging, and maintained-census reproducibility for the two pinned revisions and the
current tip — not source-content re-opening, not other lanes, not the separate `tools/mori-census.sh`
C2 instrument.
