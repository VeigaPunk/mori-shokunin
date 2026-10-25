# RevRowIdentity — mori round 46 calibration repair falsification

Seat: `RevRowIdentity` (leaf reviewer, no subagent dispatch)
Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`
Predicate under test: `.ufo/waves/round-46/count-repins.py` (frozen)
Scope: exact row identity matching, and behavior when a target row is missing.
Method: ran the frozen predicate (unmodified) against synthetic SKILL.md fixtures and against the two live snapshots (current `SKILL.md`, prior committed control `control-skill.md`). `python3 .ufo/waves/round-46/count-repins.py <fixture>` subprocesses; stdout + exit code recorded. No repo files edited; fixtures written under a scratch tmpdir.

## 1. Verified live states

| Input | Exit | stdout |
|---|---|---|
| current `SKILL.md` (repo root) | 0 | `MORI_R45_REPINS mismatches=0 rows=4` |
| `control-skill.md` (prior committed snapshot) | 1 | `MORI_R45_REPINS mismatches=4 rows=4` + 4 per-row `stale/missing … pin(s)` lines (C2 base 1, C1 2, C2 conformance 5, superseded 3) |

The repaired snapshot is green; the do-nothing control remains red. Matches the frozen claim.

## 2. Exact row identity matching — verified behavior

Mechanism: `line.startswith("| " + row + " |")` (count-repins.py:29). Probes on synthetic green baseline (all four ROWS keys present with needles):

| Probe | Construction | Result |
|---|---|---|
| Prefix-pair cross-match, A→B | Remove base row `r44 gate registry (C2)`; keep superseded row (which contains the same `GATE_REGISTRY_SELFTEST pass=15 fail=0` needle) | found 0 → red. The superseded line does NOT satisfy the base query (`startswith` terminator `" |"` does not match `" —"`), and the shared needle never rescues a missing row. |
| Prefix-pair cross-match, B→A | Remove superseded row; keep base row | found 0 → red (base line does not satisfy the superseded query). |
| Duplicate row | Insert second identical base row | `expected one row, found 2` → red. |
| Whitespace variance | `| r44 gate registry (C2)|` (no space before final pipe) | found 0 → red (exact on the ` |` terminator). |
| Case swap | `R44 gate registry (C2)` | found 0 → red (case-sensitive). |
| Leading indentation | ` | r44 gate registry (C2) | …` | found 0 → red (must begin at column 0 with `|`). |
| CRLF file | same lines, `\r\n` endings | green (`splitlines()` tolerates). |
| Non-table prose | row text mid-line, not line-leading | never matches (startswith `|`). |

Finding: identity matching is strict and unambiguous for the four frozen ROWS keys — including the deliberately overlapping pair `r44 gate registry (C2)` / `r44 gate registry (C2) — write scope superseded`, which cannot cross-satisfy one another. No single line can satisfy two row queries. No false green produced by any identity variant.

## 3. Behavior when target row is missing

| Case | Result |
|---|---|
| One row missing, other three green | `mismatches=1 rows=4`, `expected one row, found 0`, exit 1. `rows=4` stays constant (from `len(ROWS)`); the verdict signal is `mismatches`. |
| All four rows missing (empty file) | `mismatches=4 rows=4`, four `found 0` lines, exit 1. |
| Row present, needles stale | `stale/missing N pin(s)` (count only; the error line does not name which needle(s) failed). |
| Needle present in a *different* row | never satisfies the missing row (P2/P9) — pin presence cannot rescue identity failure. |
| Argument file absent | uncaught `FileNotFoundError` traceback; no `MORI_R45_REPINS` verdict line emitted; exit 1. No `rc2`-style setup classification. |

Finding: a missing target row always turns the predicate red; there is no path from a missing row to `mismatches=0`. The only non-reporting case is a missing *file*, which crashes without a verdict (robustness gap, not a false-green avenue).

## 4. Findings by severity

**Medium — pin check is contains-semantics, not cell/column-verified (weakness, not false green).**
Needles are checked as `needle not in matches[0]`, i.e. plain substring anywhere on the matched row line. Concretely verified:
- Needle text in the *verdict-map* cell (pinned-values cell empty) still passes: `mismatches=0 rows=4`, exit 0.
- `743 lines` is satisfied by `1743 lines`; `fail=0` is satisfied by `fail=00`.

So "the four rows match measured pins" holds in the sense "each required needle string appears somewhere inside a uniquely matched row line" — not "the pinned-values cell equals the pin". The identity portion of the claim is sound; the pin portion is looser than the cell-level wording suggests.

**Low — diagnostics.** `stale/missing N pin(s)` reports a count without naming the failing needle(s); `expected one row, found N` is precise. Missing file → traceback, no verdict line.

## 5. Residual risk / verification gaps

- Fixtures are minimal markdown tables; however the two live full-file runs (current SKILL.md green, control red) execute the real byte streams end-to-end.
- The wrong-column and substring-acceptance behaviors (section 4) are the only ways the predicate could stay green while a pin/pin-cell is not literally in place; none of them apply to a missing/deleted row (always red).
- No claim is made about unverifiable semantics (e.g. whether the matched row's gate entry actually resolves); identity is judged purely syntactically — which is all the frozen predicate can encode.

## 6. Tooling directive

No installs/upgrades performed; none were needed (no pacman transactions; per lane constraints).
