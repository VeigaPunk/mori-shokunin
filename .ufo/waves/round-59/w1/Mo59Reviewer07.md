# Mo59Reviewer07 — C2 claim-grammar attack (mori round 59, wave w1)

Seat: reviewer (attack seat, C2 grammar). Date: 2026-10-28.
Scope: feed `eval_entry`-shaped entries with claims that dodge the frozen C2
claim regex; report what parses. Detection only; no production edits, no VCS
mutation, no fleet/sibling writes.

## Verdict

**Partial counterexample found at grammar level; no frozen verdict flips.**
The counter is robust against the four assigned dodge forms at the hostile-tree
level, but two grammar-acceptance defects exist (`F1`, `F2`) and one arm
asymmetry (`F3`). The real landed entry and all 12 committed hostile trees are
unaffected today.

## Method (bounded)

- Frozen counter `.ufo/waves/round-59/count-c2.py` copied to scratch; byte
  verified: working tree == freeze rev `60b3a76a` ==
  `sha256 2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be`
  (kill rule intact at review time).
- Do-nothing control consistent: `tools/mori-settlement-scan.py` and
  `corpus/knowledge/wave-settlement-artifacts-r59.md` both ABSENT at entering
  rev `2b9f0397` (`git show` fails) → `C2=unmet … tool_absent` path holds.
- All experiments ran the frozen `eval_entry` (imported from the byte-verified
  copy) against synthetic roots and `git show`-materialized trees under
  `$HYAKU_SCRATCH/mori-r59/Mo59Reviewer07/` (TMPDIR set there). Lane accessed
  read-only (`git show` / `ls-tree` / `rev-parse` only). Drivers:
  `attack_c2.py`, `attack_c2_p2.py` (deleted with scratch after receipts below).
- HEAD moved during review (`8ff344ff…` → `7b86704d…`, L1 committing evidence);
  real-entry/tree results pinned to `7b86704d7c0754a09958d131b64dbfa2a6d3eaed`.

## Findings by severity

### F1 — MODERATE: "distinct claims" predicate bypassed by zero-padded labels

`eval_entry` dedups on the raw `K(\d+)` capture text (`seen[kid]`, kid is the
string), so `**K01**` duplicating `**K1**`'s full content counts as a distinct
claim toward `MIN_CLAIMS`.

```
B_zero_pad_label_dup_K01_vs_K1:  K1..K9 + K01(=K1 content duplicated)
    eval_entry.ok=True claims=10 files=3 reasons=[]
B2_exact_dup_label (contrast):   K1..K9 + K1 again
    eval_entry.ok=False claims=10 reasons=['distinct:dup=K1']
```

An entry with only 9 distinct claim contents scores MET-grade (10 parsed, no
reasons). Hostile set covers only exact-dup (`t02-dup-k` → `distinct`); the
padding form is uncovered. Real entry at `7b86704d` has no padding (raw labels
`1..10, 12, 13, 14`), so no present-tense impact.

### F2 — MODERATE: multi-quote lines parse; only the LAST locator group is enforced

`CLAIM`'s non-greedy `.+?` plus backtracking rebinds a claim to the LAST
`` Quote: `…` (file:kind:n; pin hex) `` group on the line:

```
C2a_two_quotes_second_valid:
  line = "- **K1** … Quote: `A` (r54:line:2; pin sha54)"
       + " - **K2** … Quote: `B` (r55:line:2; pin sha55)"
  → parses as K1 with quote=B, file=r55, pin sha55
    ok=True claims=10 reasons=[]
  K1 parsed: quote=' "seats": 3,' cfile=…/w1-results-r55.json kind=line n=2
C2b_stale_first_pin:  same shape, FIRST group's pin = 0*64 (stale)
  → ok=True claims=10 reasons=[]   (stale pin never validated)
```

A displayed quote+pin pair can be stale or foreign with zero counter reasons;
"byte-exact pin-bound" is enforced only for the final group. No frozen verdict
flips: `t12-malformed-claim` still UNMET (its line lacks a trailing valid
locator — replay below) and the real entry contains no double-`Quote:` lines
(`grep -n 'Quote:.*Quote:'` → none).

### F3 — LOW-MODERATE: `grammar:` reasons never fail the real-entry arm

`measure()` computes `entry_ok` excluding prefixes `("frontmatter",
"distinct", "claims_min", "files", "span", "entry_absent")` — `"grammar"` is
absent, and grammar feeds neither `rows_ok` nor `pins_ok`. The landed entry may
carry any number of grammar-broken claim lines while ≥10 lines parse. Observed
across cases A/D/E/F (below): `eval_entry.ok=False` but measure-style
`entry_ok=True rows_ok=True pins_ok=True`. Asymmetric with the tree arm, which
uses the strict all-reasons boolean. Real entry currently clean (0 claim-ish
non-parsing lines), so impact is latent strictness only.

### F4 — INFORMATIONAL: silent-skip class is invisible

A claim-shaped line with no `**K` substring and lowercase `quote:` is neither
counted nor flagged:

```
I_lowercase_quote_no_bold: "- K99 — stealth. quote: ` … ` (file:line:2; pin hex)"
    eval_entry.ok=True claims=10 reasons=[]
```

Under-count-only risk; cannot inflate MET by itself.

### No-counterexample results (counter robust, as designed)

- Leading whitespace before a claim → `grammar:` reason, ok=False (A).
- Empty quote `` `` `` → `grammar:` reason, ok=False (D).
- Uppercase-hex pin → `grammar:` reason, ok=False (E) (`[0-9a-f]{64}` is
  lowercase-only).
- Two claims on one line WITHOUT a trailing valid locator → `grammar:`
  (via the `**K` tripwire) + claims under-count (C variant).
- Exact duplicate `**K1**` → `distinct:dup=K1`, ok=False (B2).

### Hostile-tree replay at HEAD `7b86704d` — 12/12 PASS

Each committed tree materialized via `git show` into scratch and evaluated with
the frozen `eval_entry`; verdict and expect-prefix coverage:

```
t01-no-frontmatter  ok=False expect=[frontmatter]        covered PASS
t02-dup-k           ok=False expect=[distinct]           covered PASS
t03-quote-wrong-line ok=False expect=[span]              covered PASS
t04-stale-pin       ok=False expect=[pin]                covered PASS
t05-few-claims      ok=False expect=[claims_min]         covered PASS
t06-outside-file    ok=False expect=[files]              covered PASS
t07-no-row          ok=False expect=[rows:missing]       covered PASS
t08-extra-cell-row  ok=False expect=[rows:bad_row]       covered PASS
t09-usedby-other    ok=False expect=[rows:usedby]        covered PASS
t10-queued-status   ok=False expect=[rows:status]        covered PASS
t11-quote-short     ok=False expect=[span]               covered PASS
t12-malformed-claim ok=False expect=[grammar]            covered PASS
```

None of the committed malformed forms is rescuable by the F2 rebind quirk.

### Real entry at HEAD `7b86704d`

`eval_entry` → `ok=True claims=13 files=6 reasons=[]` (≥10 / ≥3 satisfied with
margin). No zero-padded labels, no double-`Quote:` lines, no lowercase-`quote:`
silent-skip lines, 13 pin-bearing claim lines. The `K11` occurrence (entry line
43) is prose, not a claim. Registry `used-by`/`mined` bindings validated inside
`eval_entry` (zero `rows:` reasons).

## Residual risk and verification gaps

- Findings are grammar-level against the frozen counter; fixes require a future
  round (frozen bytes immutable — kill rule respected here).
- `measure()` end-to-end post-landing (tool sha/selftest/scan/drift arms) was
  not exercised; out of this seat's grammar scope.
- L1 was committing while I reviewed; HEAD moved once (`8ff344ff` →
  `7b86704d`). Tree/entry results are pinned to `7b86704d`; a later evidence
  commit is not covered.

## Recommendation to L1 (advisory only — no edits made by this seat)

For a future counter revision: (1) normalize duplicate detection on
`int(kid)`; (2) reject any claim line containing more than one `Quote:`
occurrence or any second locator group; (3) add `"grammar"` to the `entry_ok`
exclusion prefixes; (4) optionally flag silent-skip shapes (bullet-like lines
carrying `quote:`-style locators that fail to parse).

## Cleanup receipt

Scratch `$HYAKU_SCRATCH/mori-r59/Mo59Reviewer07/` (drivers, counter copy,
synthetic trees, materialized HEAD roots) removed after this report was
written. Disk guard was green at start (`/fast/scratch/hyaku` 27% used, 592.6G
free). No pacman use; no tools installed; no secrets or session material
exposed.
