# RevC5Predicate — `predicate` check verification (round 38, wave 2)

Seat: `MoriR38.RevC5Predicate` (reviewer, falsify lane). Scope: conform.py's `predicate`
check — contract P-C1 blockquote vs `count-c1.py --print-predicate`, plus reproduction of
the r37 defect that motivated the check.

## Verdict

**PASS — no actionable finding.** The r38 pair is equal and the r37 defect reproduces as
the check's motivation.

## Method (every number below derived by running, not read from reports)

Replicated conform.py's extraction verbatim (`.ufo/waves/round-38/conform.py:73-86`):

- `normalise(t) = re.sub(r"\s+", " ", t).strip()`
- `contract_predicate`: `text.find("P-C1 of record")` (else index 0), then
  `re.search(r"^> (P-C1:.*?)\n\n", text[index:], re.M|re.S)`, continuation lines joined
  via `.replace("\n> ", " ")`, then `normalise`.

Commands run:

- `python3 .ufo/waves/round-38/count-c1.py --print-predicate` → exit 0, single-line stdout.
- `python3 .ufo/waves/round-37/count-c1.py --print-predicate` → usage error, **exit 2 —
  the r37 counter has no such flag** (argparse at `round-37/count-c1.py:890-895` accepts
  only `rev`, `--repo`, `--tool`, `--negatives`, `--seed`).
- r37 printed predicate therefore obtained two independent ways, both read-only:
  (a) first stdout line of `python3 .ufo/waves/round-37/count-c1.py deadbeef0000
  --repo <lane>` — the counter prints `PREDICATE` unconditionally
  (`count-c1.py:898`) then exits 2 at `rev-parse` (`:903-909`), before any `mkdtemp`
  (`:940`) — no scratch mutation; (b) `ast.literal_eval` of the `PREDICATE` assignment
  (`count-c1.py:42-52`). The two agree byte-for-byte after normalisation.

## Results

| pair | contract (normalised) | printed (normalised) | equal? |
|---|---|---|---|
| r38 of-record blockquote vs `count-c1.py --print-predicate` | 844 | 844 | **True** |
| r37 **first** P-C1 blockquote (v1, contract.md:20-27) vs r37 printed predicate | 623 | 775 | **False** |
| r37 **second** P-C1 blockquote (A1 amendment, contract.md:132) vs r37 printed predicate | 775 | 775 | True (cross-check) |

Shared tail verified: both r38 sides end
`...published real-arm constant, and prints the lane tip it measured as head_at_measurement=<40-hex>.`

## r37 defect reproduction (the check's motivation)

- `.ufo/waves/round-37/contract.md` contains **two** `> P-C1:` blockquotes: the frozen v1
  (lines 20-27, ends `a constant printer, and a summary-only printer.`) and the post-data
  A1 amendment (line 132, `### A1 predicate of record ... counter v2, 4bfa0490`).
- The committed r37 counter prints the **v2** predicate (775 normalised chars), matching
  the A1 blockquote exactly — but the contract's **first** blockquote is the stale v1
  (623 chars).
- First divergence at normalised char 553:
  - v1: `...negative fixtures: a real-arm memoizer, a constant printer, and a summary-only printer.` (ends)
  - printed: `...negative fixtures (a real-arm memoizer, a constant printer, a summary-only printer) and matches the standing truth on one run-time-drawn ancestor revision...` (continues 152 more chars)
- `contract_predicate` applied to the r37 contract has no `P-C1 of record` marker →
  index 0 → matches the first (v1) blockquote → `623 != 775` → `predicate` FAIL. This is
  exactly the ExecC1Seed43 §6.1 defect the r38 check exists to kill: the
  declared-before-data blockquote matched the v1 counter while the committed counter
  printed the longer v2 predicate.
- Corroboration from lane receipts: `evidence/c5-before.txt:3` —
  `check predicate FAIL (exit=2 equal=False)` (the r37 counter additionally lacks
  `--print-predicate`, so the check also fails on exit); `evidence/c5-after.txt:3` —
  `check predicate PASS (exit=0 equal=True)` on the scored tip.

## r38 structural fix verified

- `contract.md:112` heading `### P-C1 of record (counter v4, printed verbatim)`; the
  `P-C1 of record` marker occurs exactly once, and exactly **one** `> P-C1:` blockquote
  follows it (line 114) — extraction is unambiguous; only one counter version exists.
- The v4 predicate's added tail (`head_at_measurement=<40-hex>`) is present in both the
  blockquote and the counter's `PREDICATE`/`--print-predicate` bytes; the counter's
  source constant (`count-c1.py` PREDICATE, AST-evaluated) equals its printed output, so
  no print-path mutation is being masked.
- Failure direction is honest: missing marker/blockquote → `SetupError` → `predicate`
  recorded FAIL, never a silent pass (conform.py:132-141).

## Residual risk (informational, not findings)

- `predicate` (and `head_pin`/`tool_resolve`/`timeout_state`) audits only `counters[0]`
  (conform.py:129). The contract's canonical command orders count-c1.py first; a swapped
  order fails safe (count-c4 prints its own predicate → `equal=False`), never bypasses.
- If a future amendment appended a second `> P-C1:` blockquote *after* the of-record one
  (the exact r37 A1 pattern), `contract_predicate` keeps the first — that is the frozen
  "of record" semantics, and the contract now forbids post-freeze predicate edits
  (`contract.md:4-6`, freeze pins in `evidence/freeze-r38.txt`).
- r37 figures rest on the counter's unconditional `print(PREDICATE)`; both derivations
  (stdout, AST constant) agree, so the 775/623 numbers are not in doubt.

## Tooling

No installs or upgrades performed. Existing `python3` sufficed; no pacman/uv/cargo
transactions. Lane repo untouched: only read-only counter invocations (early-exit rev,
no mkdtemp reached) and file reads; zero files written outside this report.

Report: .ufo/waves/round-38/w2/RevC5Predicate.md
