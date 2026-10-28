# Mo59Reviewer09 — C2 rows-binding attack report

Scope: `eval_entry` rows-arm of frozen `count-c2.py` (worktree bytes sha256
`2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be` == amended
freeze `60b3a76`; entering `2b9f0397` has no counter — verified via `git show`).
Method: direct `eval_entry(root)` calls on synthetic trees under
`/fast/scratch/hyaku/mori-r59/Mo59Reviewer09` (canonical binding logic —
`count-c2.py:300` calls it on the materialized landed root, `:346` on every
hostile tree), plus `scripts/sources-census.sh validate` on synthetic lanes
(census = the contract's round-end gate). No production edits; lane read-only.

## Assigned cases — verdicts

| Case | Counter verdict | Census verdict | Assessment |
|---|---|---|---|
| 3-space-indented SOURCES row | BINDS (`ok=True`, no reasons) | counted as row, validate exit 0 | CORRECT — ≤3 spaces is valid markdown table indentation and both grammars agree |
| used-by cell = entry + another path (either order) | REJECTS `rows:usedby=S999` | n/a | CORRECT — predicate says "names exactly this entry"; t09 hostile tree covers the one-other-path case |
| mined row, used-by=entry, anchor cell empty (or `—`) | BINDS | exit 0 (no anchor rule exists: E01–E12 don't inspect cells[5]) | LITERAL-predicate pass; semantic weakness — see F5 |

## Findings (severity order)

### F1 — HIGH: row-matcher whitespace/line-split divergence lets a non-registry line bind `rows=ok`

`count-c2.py:83` `ROW = re.compile(r"^\s{0,3}\|\s*(S\d{3,})\s*\|")` iterates
`reg.splitlines()` (`:174`); `\s` matches `\t`, `\v`, `\f`, `\x1c-\x1f`, `\x85`,
NBSP and Python `splitlines()` splits on `\v\f\x85\u2028\u2029`. The registry's
own row grammar — `sources-census.sh` `row_pass`/`usedby_findings`, which the
contract makes the round-end gate — uses space-only `^ {0,3}\|` and `\n` lines.

Empirical (frozen `eval_entry` on synthetic trees; `census validate` on the
same SOURCES.md):

- `\t| S999 | … | mined | … | <entry> |` above `## Registry`, **no real row
  anywhere** → `eval_entry ok=True` (zero reasons); census `validate` exit 0,
  `rows 0`, `status.mined 0`. A hostile landing satisfies `rows=ok` with zero
  registry rows for the cited S-id — falsifying "registry row with status
  mined" while the round-end census gate stays green.
- `\x0b`-prefixed identical row inside `## Registry` → same: counter binds,
  census blind (`\x0b` is a line-break to `str.splitlines`, an in-line byte to
  POSIX `read`/`gawk`).

### F2 — HIGH (compounds F1): first-`hit`-wins binding shadows the real row

`count-c2.py:173-178` scans every line of SOURCES.md and binds the **first**
`ROW` match — not the first Registry-row, and with no duplicate-id check.
Frozen hostile trees t07–t10 each mutate only the real row; none place a
matching earlier line. Empirical: a `\t`-indented shadow `| S999 | mined |
<entry> |` placed before `## Registry` makes `eval_entry ok=True` while the
real in-Registry S999 row is

- `queued` (S2: evades `rows:status`), or
- `mined` with `used-by = corpus/knowledge/other.md` (S5: evades `rows:usedby`),
- or absent entirely (S1/S6: evades `rows:missing`),

and census validates exit 0 (sees only the legit row; shadow invisible).
Round-58's routed S552 duplicate-id defect is the real-world precedent; E03
only fires when both copies are census-visible.

### F3 — MEDIUM (shared defect): fenced code block inside `## Registry` binds

A ` ``` ` fenced block containing `| S999 | … | mined | … | <entry> |` inside
the Registry section: `eval_entry ok=True` **and** census counts it
(`rows 1`, `status.mined 1`, validate exit 0 — S7/fenced-alone lane). Neither
parser is fence-aware; a markdown code block is scored as a registry row.
Landing-viable alone; with a same-id real row census trips E03.

### F4 — LOW: row-grammar divergence — missing trailing pipe

`| S999 | … | <entry>` (no trailing `|`): counter strips/splits to 11 cells and
binds (`ok=True`); census `NF!=13` → `E01 fields=10`, exit 1. Not
landing-exploitable (census is stricter), but proves `rows=ok` can bind a row
the registry declares malformed — the counter never checks table shape beyond
cell count.

### F5 — LOW: rows arm is bookkeeping-only; predicate extras unenforced

- Anchor cell unchecked (assigned case 3): `anchor` empty or `—` binds and
  census has no anchor rule → a "mined" row naming no source evidence
  satisfies `rows=ok`. Literal-predicate pass; weakens "registry rows those
  claims cite".
- "one per cited artifact copy" (contract §2b) unenforced: `sids` is a set of
  cited ids, never compared to `ARTIFACTS`/claimed files — one S-row can back
  claims over 6 files.
- `SID` harvest (`S\d+`, any length) vs `ROW` (`S\d{3,}`): `source: S99` in
  frontmatter → `rows:missing` even if a `| S99 |` row exists (harmless — real
  ids are ≥3 digits).

### Spec-tension note (not a counter defect)

`cells[10] != ENTRY` exact-match is frozen-spec-correct, but the registry's
own convention is comma-separated used-by lists (S002, census
`usedby_findings` splits on `,`). The second legitimate consumer of a
row mined for this entry would invalidate the binding — predicate-mandated
exclusivity, worth a lesson note.

## Residual risk / verification gaps

- All evidence is against `eval_entry` on synthetic trees + census on
  synthetic lanes; no landed tree exists yet (wave in flight), so F1/F2 are
  *capability* counterexamples, not observed landings.
- Fix direction (for the planner, not this seat): reuse the census row
  grammar (space-only `^ {0,3}`, `\n`-split, `## Registry` section
  membership, `NF==13`) for the counter's `ROW`, and bind the *last* or
  *registry-section* row rather than first-hit — but any byte change
  post-freeze trips the kill rule, so F1/F2 stand as predicate
  falsifications for scoring, not fix proposals.
- Hostile-tree gap: t07–t10 cover missing/extra-cell/wrong-used-by/queued on
  the real row only; no tree exercises a shadow/duplicate-id row or a
  non-space-indent row.

## Evidence index

- Counter lines: `ROW` `count-c2.py:83`; line scan/first-hit `:173-178`; cell
  split `:182`; checks `:183-189`; `eval_entry` callers `:300,:346`; SID
  harvest `:161-163`; frontmatter `head=lines[:10]` `:112`.
- Census lines: `row_pass` space-only `^ {0,3}\|` `sources-census.sh:615`;
  E12 `!in_registry` check `:618-622`; `NF!=13`→E01 `:635`; E03 dup-id `:641`;
  `usedby_findings` `^ {0,3}\|` `:541`, comma-split `:562`.
- Commands: `python3` + `importlib` load of the frozen counter (sha256
  `2df3ae84…` = `git show 60b3a76:…count-c2.py` digest); `sources-census.sh
  validate --today 2026-10-28 lanes/<n>` and `census` on synthetic lanes
  under `/fast/scratch/hyaku/mori-r59/Mo59Reviewer09/lanes/` (scratch cleaned
  after copy).

Verdict: C2 rows arm falsifiable — F1+F2 is a concrete counterexample where
`rows=ok` binds a line that is not a registry row per the lane's own row
grammar, and can hide `queued`/`wrong-used-by`/`missing` real rows while the
round-end census gate stays green. Assigned cases: 3-space indent binds
(correct), two-path used-by rejects (correct), empty anchor binds
(literal-pass weakness).
