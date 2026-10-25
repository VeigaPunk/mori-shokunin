# R48RevV3Code — line-by-line review of the landed v3 diff

Attacked: `tools/mori-pin-check.py` diff `e5dbac05..e4dfff32` (v2 → v3, +357/−73), reviewed at the
landed tip with a synthetic `check()` harness and a throwaway fixture repo under
`.scratch/r48w2-R48RevV3Code/`. Every finding below was reproduced against the landed bytes
(`git show e4dfff32:tools/mori-pin-check.py`), not just read off the diff.

Verdict: the landed v3 **HOLDS** on the frozen predicate — observed live:
`count-c1.py --tool tools/mori-pin-check.py --rev e4dfff32` printed
`C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12` in 990 s under my TMPDIR
(all 8 junk unmet, all 4 honest met, real registry met, zero errors). The diff **introduces one
crash path**, **leaves one v2-inherited rebound blind spot the R4 patch half-fixed**, and **opens
three new survivor/limit classes**. P-C1's kill rule is not triggered; these are wave-2 limits and
successor defects.

## Findings by severity

### HIGH — F1. `norm=None` rebound crashes `check()` (regression, introduced by the v3 edit)
`tools/mori-pin-check.py:543,551-552`. When a row that had a baseline binding loses its bound
command (command span deleted, or the span no longer parses to `argv_ok`), `norm` is `None`;
line 543 `norm != base_bind[bkey]` is `True` → `rebound = True` → line 552 `" ".join(norm)` raises
`TypeError: can only join an iterable`. v2 guarded with `" ".join(norm) if norm else None`; the v3
hunk dropped the guard.
Evidence: `check(cur, …, baseline=base)` with the command span removed → traceback at line 552.
Through `main()` on a two-commit fixture repo (`--rev CUR --baseline-rev BASE`):
`PIN_CHECK_SETUP can only join an iterable`, exit 2 — observed, no traceback, but the run is
`errors`, never `unmet`. If any of the counter's variants tripped this path, C1 could not meet
`errors=0`; none of J1–J8/H1–H4 does (UNVERIFIED against the live counter — see below; verified
independently on synthetic trees).
Fix direction: restore the `if norm else None` guard, or short-circuit the `elif`/first branch on
`norm is None` and report `state=rebound cmd=None`.

### HIGH — F2. Rebound blind spot for `<rev>`-placeholder entry rows (v2-inherited, R4 did not close it)
`tools/mori-pin-check.py:472` (`base_bind = pin_bindings(baseline_text, "<REV>")`), 543.
For a row whose bound argv is derived from a bare `` `--selftest` `` span plus an entry cell
containing `<rev>`/`<REV>`/`REV`, `derive_command` called with `rev="<REV>"` re-substitutes the
placeholder and then rejects it (`any(w.startswith("<"))`, line 387) → `base_bind[bkey] = None` →
line 543's `is not None` guard never fires for that **existing** row. The two real baseline rows
affected: `counter conformance v3 (r40)` → `CONFORM_SELFTEST`, `SOURCES append-only timing (r38)`
→ `MORI_SOURCES_APPENDONLY_SELFTEST` (verified: `pin_bindings(SKILL.md@2d85e33d, "<REV>")` gives
`None` for exactly these two keys).
Evidence: T5 — rebinding `conf`'s pin to `python3 tools/evil.py --selftest` (rigged tool printing
the same tally) against a baseline containing the `<rev>`-entry row scores
`PIN_CHECK=met … rebound=0`. The pinned command was swapped and no rule objected.
Note the R4 placeholder pass (lines 476-480) repairs `base_bind_prefix` for **new** rows of these
prefixes, so the gap is exactly: existing rows whose baseline argv contains a `<rev>` word.
Pre-existing in v2; the v3 rewrite consciously re-derived the prefix map but left the per-key map
with `None` sentinels — worth an R-successor since J-class "re-pin an existing row to a rigged
instrument" survives on these rows.

### MEDIUM — F3. `len(base_bind_prefix[prefix]) == 1` gate deviates from spec R4 (namespace carve-out)
`tools/mori-pin-check.py:545-548`. Spec R4: "a row, new or old, that uses a baseline prefix with an
argv not in that prefix's baseline set is `rebound`." The implementation only checks new rows when
the prefix's baseline set has exactly one argv; for multi-argv prefixes (`C1_SELFTEST`×3,
`C2_SELFTEST`×2, `C3_SELFTEST`×3 at the real baseline) a new row may bind **any** argv.
Evidence: T4 — new row `evil | python3 tools/evil.py --selftest → C1_SELFTEST pass=6 fail=0` under
a 2-argv baseline scores `met … rebound=0`. This is load-bearing for H4 (the honest variant binds
`C2_SELFTEST` to round-47's `count-c2.py`, an argv outside the baseline set — a strict R4 would
false-red H4), so the carve-out is deliberate, but as written it also lets a junk row pin any
controllable instrument to `C1_SELFTEST`/`C3_SELFTEST`. A tighter rule that keeps H4 green: admit
new argvs only when the argv's path resolves to a file that exists at the measured rev (a rigged
`.scratch` path already fails `argv_ok`).

### MEDIUM — F4. `hidden_rows` R9b fires on any `other` line after ANY row-shaped line — false-red
`tools/mori-pin-check.py:262-264`. The continuation-line rule checks only `prev_raw` for
`^ {0,3}\|`, so a plain prose line mentioning `--selftest` or a `*SELFTEST pass=` token is `hidden`
when it sits directly under a table row, a header line, a separator line, or a non-registry
candidate row — including rows of unrelated non-self-test tables.
Evidence: T3 — `…row…\nThis gate runs with the `--selftest` flag.\n` → `hidden=1`, `PIN_CHECK=unmet`
on an honest document. Spec R9b says "directly under a table row"; implementation broadens it to
"directly under anything row-shaped". A blank line between row and prose disarms it (gap or grace,
depending on intent).

### MEDIUM — F5. Hidden-row `row_shaped` grammar is narrower than the row parser — junk escapes `hidden`
`tools/mori-pin-check.py:253` (`re.match(r"^ {0,3}\|", raw)`) vs `split_cells:144` (`line.strip()`
— strips TAB, vertical tab, form feed, NBSP). A `|`-row indented with a TAB, 4+ spaces, or
`\f`/`\v`/NBSP and carrying a `*SELFTEST` token outside a parsed table is classified `candidate`
(or `fence_body`) yet skipped by the `hidden` rule.
Evidence: T2 — `\t| h | … `PIN_CHECK_SELFTEST pass=1 fail=0` … |` after a blank line →
`hidden_rows: []`, `PIN_CHECK=met`. T10 — same with 4-space indent → `[]`, `met`. The pin text is
visible in the document, never measured, never flagged — an R2 survivor class. (Spec R2's own
regex is also space-only, so this is a spec-shaped limit as well as a code limit; the parser side
is the asymmetry — `split_cells` accepts what `hidden_rows` then skips.)

### MEDIUM — F6. `LINE_COUNT_RE` binds digit-suffixes of grouped numbers — false-red on prose counts
`tools/mori-pin-check.py:118` (`(\d+) lines`, no left boundary). `1,006 lines` binds `006` (the
greedy `finditer` match starts inside the number); any `N lines` substring in a self-test cell —
including quoted output like `scanned 42 lines` or a size in words — becomes a hard pin on the
nearest preceding in-tree path.
Evidence: T6 — `(the doc says 1,006 lines)` after the `tools/foo.py` command span →
`pin kind=lines state=mismatch pinned='6 lines' observed=3`, `unmet`. The landed registry's only
pin (`(743 lines)` at SKILL.md:184) is clean, but any future prose count containing `N lines`
false-reds. Fix direction: `(?<![\d,])(\d+) lines` plus, per R5's "pin" intent, possibly requiring
it inside or adjacent to a path mention.

### LOW — F7. R9a flags any tally-shaped token in non-self-test cells of a parsed row — false-red
`tools/mori-pin-check.py:257-261`, `TALLY_TEXT_RE` line 121. An honest row that quotes its own
expected tally in `entry`, `verdict map`, or `pinned values` (e.g. `expects `FOO_SELFTEST pass=3
fail=0``) is `hidden`. Spec-derived (CritJunkClasses D5), but it means the registry can never
quote a tally outside the measured cell — worth a named limit.
Evidence: T7 → `hidden=1`, `unmet`.

### LOW — F8. `TRUNC_DIGEST_RE` overlaps a full 64-hex digest followed by `…` — phantom second pin
`tools/mori-pin-check.py:115`. `[0-9a-f]{8,63}\u2026` has no right-edge guard; on
`` `<64-hex>…` `` it matches hex chars 2-64 + `…` (the shifted, wrong prefix), so a decorative
ellipsis after a correct full digest produces `state=mismatch digest=0c769…` alongside the real
match — `unmet` on an honest-ish cell.
Evidence: T15 → one `match` (full hex) plus one `mismatch` (shifted trunc), `unmet`.
Fix direction: `(?<![0-9a-f])[0-9a-f]{8,63}\u2026` or `[0-9a-f]{8,63}(?![0-9a-f])\u2026`.

### LOW — F9. Digit-led and bare `SELFTEST` tokens escape every tally/visibility regex
All four grammars require `[A-Z]` first and ≥1 char before `SELFTEST`
(`[A-Z][A-Z0-9_]*SELFTEST`, lines 114-117, 121): `9SELFTEST`, `SELFTEST`, `_SELFTEST` are
invisible to `hidden`, `tally`, `unparsed`, and `TALLY_TEXT_RE` alike.
Evidence: T9/T16 — a candidate row `…`9SELFTEST pass=9 fail=0`…` → `hidden_rows: []`, `met`; the
same span inside a self-test cell is `ignore`d (not `unparsed`). Survivor/limit class — the pin
token grammar has a one-character hole.

### LOW — F10. Doc drift / dead weight
- `tools/mori-pin-check.py:81-82` — the docstring's output example still omits `hidden=N`
  (line 600 prints it).
- `trunc_digest_pins(st, raw, root)` at line 313 — `raw` is a dead parameter (cell-only binding
  since R10); callers pass `row["raw"]` for nothing.
- `span_kind` return values `"digest"|"trunc"|"tally"|"command"` are never consumed (only
  `"unparsed"` is) — dead classification work, harmless.

## Explicitly checked, no defect

- **Variant/TMPDIR/filename keying** (the F1 harness-leak class from `w1/CritC1Counter.md`):
  `grep` for `variant|TMPDIR|basename|count-c1` — TMPDIR appears only as `run_cmd`'s env setup
  (line 406) and selftest fixtures; no branch keys on the variant filename, the scratch dir name,
  or the counter's bytes. Clean.
- **`hidden_rows` ↔ `parse_registry` ordering**: both consume `scan_lines` fresh; kinds are
  consistent; the only asymmetry is the `row_shaped` regex vs `split_cells` strip (F5).
- **`scan_lines` candidate-under-live-header** (a row followed by a separator starts a new table):
  identical to v2; T8 shows such candidates are still caught as `hidden` when they carry a token.
- **`hidden_rows` kinds covered**: `candidate`, `fence_body`, well-formed `row` (R9a), `other`
  (R9b). Malformed rows (`state=unparsed`) skip R9a but are covered by the pre-existing
  `(?i)selftest` unparsed check (line 496) — no gap.
- **Continuation adjacency**: blank line between row and tally-prose disarms R9b (noted under F4;
  attacker-usable for hiding prose, but the prose is already invisible prose).
- **Real registries**: `hidden_rows(SKILL.md@e4dfff32) = 0`, `hidden_rows(SKILL.md@2d85e33d) = 0`;
  `parse_registry` over the landed SKILL.md: 58 rows, all `ok`. The `(743 lines)` pin at
  SKILL.md:184 resolves to `tools/mori-gate-registry.py` and was measured green (counter run, below).
- **CRLF rows** still caught (`\r` rides along as `other`, the row line itself is `candidate`).
- **Header lines carrying tallies** (T19): classified `header`, invisible to `hidden` — a cosmetic
  oddity, since such a line creates a live self-test table but the tally sits in a header *name*
  cell; attacker-usable only to plant unmeasured text, consistent with F9-class survivors.
- **`met` formula** line 595-598: `hidden` fatal, `tally_pins >= min_tally` unchanged; `PIN_CHECK`
  line prints `hidden=` before `min_tally_pins=` as the spec requires.

## Verification gaps

- None material to the scoped claim. The live `count-c1.py` run finished mid-review and is quoted
  in the verdict above. J-variant byte-level replay was covered by the counter itself; my synthetic
  `check()` runs exercised every class shape plus the escapes listed as findings.

