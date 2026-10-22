# ReRunCountC1 — wave-2 falsify findings (leaf seat)

Scope: rerun the C1 counter at the three revisions, compare with evidence, and read the
counter against contract Amendments A1 (kinds 1–5) and A2 (kind 2b), flagging rules not
implemented or implemented looser, including L1's edits to lines 70 and 173–174 after the
BuildCountC1 draft.

## 1. Rerun results (command: `bash count-c1.sh <lane-rev> 63729047644f839fe4c8cc97abd0d8bf741a5787`)

| Lane rev | Output | Exit | Compared to |
|---|---|---|---|
| 7118f320a5ef18d20c1e361eff77db0e1a97b2d6 | mismatches=11, C1=unmet, per-row kinds=1,2 (depth 1) | 1 | byte-identical to evidence/c1-before.txt |
| 420d05ad7945e865ac6560289e5470f09409a9a1 | mismatches=0, C1=met, all kinds=none | 0 | byte-identical to evidence/c1-after.txt |
| 8809a3fe1eaa87a0afa177a15263d174378e7462 (lane tip) | mismatches=0, C1=met, all kinds=none | 0 | no evidence file; equals c1-after.txt output |

- Counter binary used: sha256 `a26604ee9c70b17be00318eba1a7bba841cbf8c1e1bed8d71971823239d4e791`,
  matches the hash recorded in the c1-before.txt header — before and after are measured with the
  same (final) counter.
- `SCORECARD.md` at 420d05ad is byte-identical to the one at 8809a3fe (diff empty), so the
  declared after-value holds unchanged at the landed tip.
- Commit order (git log 7118f320..8809a3fe): A1 `3a14713` → A2 `6612516` → A3 `69349c2` →
  A4 `c321696` → counter `e1c6bbe` → Axes-table rewrite `420d05a` → C2 counter → freeze → tip.
  The counter landed before any Axes-table edit, per contract.md:45.

## 2. Amendment rule → counter line mapping

### A1 closure authority (contract.md:109-112)
- Imp(a) = {N in 12..28: admitted ∧ verdicts.a=="improved"}: count-c1.sh:100-103. Verified against
  fleet MANIFEST at 63729047 in R values printed (coverage 26, operability 28, depth 12, freshness
  28, calibration 25, adjacency 19) — all match hand computation from `rounds[].verdicts`.
- R(a) = max Imp(a): count-c1.sh:103.
- Cite(N) = lane file when it exists at <rev>, else literal token `MANIFEST.json@63729047 mori
  round N`: count-c1.sh:11-12, 155-157. Rounds 19–22 have no lane spot-check file (verified via
  `git ls-tree` at tip); adjacency uses the literal token.

### Kind 1 — stale closure (contract.md:113-114): count-c1.sh:151-164
- No lane file: mismatch unless the literal token substring is present (line 157). OK.
- Lane file exists: requires ≥1 backticked `path:L` cite of `round-R-verifier-spotcheck.md` (cite_lines,
  lines 113, 159); when the file has a per-axis table, at least one cited L must match `^| a | improved |`
  (lines 162-163). OK.
- Verified live: coverage cites `round-26...md:133` (`| coverage | improved | ...`), operability
  `round-28...md:93`, freshness `round-28...md:92`, calibration `round-25...md:124`, adjacency literal
  MANIFEST token; depth cites `round-12...md:17` (round-12 file has no per-axis table → no line-content
  requirement, lines 159-161 — consistent with the amendment).

### Kind 2 — last change (contract.md:115-117): count-c1.sh:166-176
- Cell opens with `round N`: line 166 (`^round\s+(\d+)\b`). OK.
- N is an admitted round: line 169 (admitted_rounds over all mori entries). OK.
- N ≥ R(a) when R(a) exists: line 169 (`recent is None or last_n >= recent[0]`). OK.
- If the cell carries (X → Y), Y equals the score cell: lines 171-172. OK.
- Held score written `round N (improved, score held)`: line 175 (fires when score==baseline, no arrow,
  and the literal string is absent). OK.
- **Note N1 (minor, only hypothetical rows):** the arrow regex lookup at line 171 requires
  `(X → Y)` to be followed by `;`, `)` or end-of-cell. A cell like `round 14 (6 → 7, improved)`
  (comma inside the parens) is not matched, so it would evade both the Y==score check and kind 2b.
  None of the six current rows use that shape (all are `round N (improved, score held)` or
  `round N (X → Y)`); verified by regex probes.

### Kind 2b — A2 (contract.md:136-137): count-c1.sh:173-174 (added by L1)
- When the Last-change cell states (X → Y) for round N, the pinned MANIFEST `verdicts.a` of mori
  round N must be `improved` (line 174). End-to-end test in a sandbox clone under my scratch
  (sb-lane, commit e98458cd): changing depth's last cell to `round 14 (4 → 5)` (round 14 admitted,
  verdicts.depth="unchanged") yields `axis=depth ... kinds=2`, mismatches=1, exit 1 — without the
  2b line this row passes kind 2 (N=14 admitted, 14 ≥ R=12, Y=5==score). The branch works.

### Kind 3 — dead pointer (contract.md:118-119): count-c1.sh:178-185
- Every backticked token containing `/` or ending `.md/.json/.py/.sh` must name a file existing at
  <rev>: lines 179-183. OK.
- `path:L` / `path:L-M` also need max(L,M) lines: line 184. OK.
- Verified live pointers at tip: `observability-surfaces-r2.md` (395 lines), `round-24...md:88`
  (148), `round-26...md:133` (195), `round-28...md:92/93` (135), `round-25...md:124` (210),
  `round-12...md:17` (17), `SCORECARD.md:1771` (1775), `corpus/README.md` (524). All pass.

### Kind 4 — score without basis (contract.md:120-124): count-c1.sh:187-196 + 116-146
- Score cell must be integer 0..10 (line 190) or `unprovable-but-better` with a named non-author
  reviewer citing an admitted closure that records that verdict for the axis (lines 193-194; helpers
  71-75, 130-146). OK.
- A numeric score may differ from its 7118f320 value only via a cited `Cite(N):L` whose line L
  states X → Y for that axis with X = baseline score, Y = new score (score_basis, lines 116-129).
  OK — note the cited line must contain the axis name (line 69) and the exact ordered pair
  (line 70).
- "An improved verdict alone, or a number a declaration proposed, is never a basis": enforced by the
  ordered-pair requirement; sandbox negative case in w1/BuildCountC1.md:28 (freshness 5→6 citing
  round-28 line 92 → basis=none, kinds=4) confirms.
- Checked: score_basis/unprovable_basis iterate over the same mori list, which contains exactly
  rounds 12–28 (17 entries verified from MANIFEST) — no out-of-range rounds can license a change.

### Kind 5 — closure disagreement (contract.md:125-126): count-c1.sh:104-110, 197
- For every N in 12..28 with a lane per-axis table, each `| a | <verdict> |` line must equal the
  MANIFEST verdicts.a for round N. Independent recheck at tip with the same regex over all 13
  spot-check files: zero disagreements (rounds 12 and 23 have files but no table lines; rounds 19–22
  have no file). OK.

### Output/exit contract (contract.md:128, 39)
- One line per row (axis, score, basis, R, kinds hit), then `mismatches=<n>`, `C1=met|unmet`:
  lines 199-203. Exit 0 met / 1 unmet / 2 bad revision or missing input: lines 205-207, 27-30, 38, 3.
  All observed in the reruns.

## 3. L1 edits to lines 70 and 173–174 (after BuildCountC1)
Draft: w1/BuildCountC1.md:43-248 (206-line fenced script, SHA-256 `72caa16d...`). Diff against the
committed count-c1.sh (208 lines) shows exactly two changes:
1. Line 70: `score_line` accepted `((old, new), (new, old))` (either ordered pair); committed
   requires `(old, new)` exactly. This is a tightening, matching A1 kind 4's definition
   ("X = the 7118f320 score, Y = the new score"): a cited line must state baseline→new, not the
   reverse. Direction probes confirm `(5,6)` matches, `(6,5)` does not.
2. Lines 173–174: inserted the A2 kind 2b check (with comment). Absent in the draft.
Both edits make C1 harder to meet, are in the same commit as the before value (e1c6bbe), and are
carried by the orphan copies 8ba7a936 / f4303e3a (identical files). No further drift exists.

## 4. Findings
- No amendment rule is unimplemented. No rule is implemented looser than the amendment text in a
  currently observable way.
- N1 (minor, latent): kind-2 arrow detection misses `(X → Y, …)` shapes (comma after Y), which
  would bypass arrow-related checks. Unobservable in the current table; worth keeping in mind for
  future rows.
- N2 (informational): kind-1 literal-token test (line 157) is a substring check, not backtick-bound;
  the amendment does not require backticks for the MANIFEST literal token, so this is not a
  deviation. If a future row places the token inside backticks, kind 3 would additionally probe it
  as a file path (now: not backticked, harmless).

## 5. Verification gaps
- Kind 4's positive basis path (a real score change with a valid X→Y citation) is not exercised at
  any of the three revisions because every score equals baseline; it is verified by code reading and
  the sandbox negative case only.
- The `unprovable-but-better` basis path is not exercised live (no row uses the form); verified by
  code reading only.
- Kind 3's negative path (a truly dead pointer) was not re-run on a mutated table; live tables all
  pass.

Tooling: no tools installed or updated (no LSP endpoint for this standalone script; git (read-only),
bash, sha256sum, python3 used). No writes outside this report and my scratch dir
(/fast/scratch/hyaku/mori-r29/w2/ReRunCountC1/).
