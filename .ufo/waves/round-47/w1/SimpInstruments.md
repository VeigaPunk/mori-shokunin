# SimpInstruments — w1 simplicity pass (round 47)

Seat: `SimpInstruments` (leaf member; no subagents dispatched). Mandate: simplicity pass over
`tools/mori-pin-check.py` and `.ufo/waves/round-47/count-c2.py` — identify dead code, duplicated
helpers, or options not needed by the frozen predicate. No edits made; proposals below apply to a
future version only (counters are frozen at `63eecf2738db96f46b0bd02b1b2dfd66787493d0`).

## Scope integrity

- Working-tree bytes equal the frozen instrument bytes (sha256, run 2026-10-25):
  - `tools/mori-pin-check.py` = `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1` ✓ (contract pin)
  - `.ufo/waves/round-47/count-c2.py` = `fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e` ✓ (contract pin)
- No production file was edited. Scratch only under `.scratch/r47-SimpInstruments/`.
- Tooling: no installs/updates performed (none required for static analysis; RULES.md read).
- LSP: no language server device is mounted in this session (`xd://lsp` → "No such tool"; mounted
  devices: ast_edit, debug, mcp__tripo_*, mcp__unity_cli_status). No server answers these files, so
  caller-absence evidence below is text grep (literal), not semantic proof — recorded here per seat
  rules. Candidate *parameters/options* are intra-file (single function/argparse surface), so grep
  corroborates rather than proves.

## Baseline (narrow existing checks, before any proposal)

Both frozen counters pass their own self-tests at the measured working tree (TMPDIR set to the seat
scratch dir):

- `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=22 fail=0`, rc=0.
- `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0`, rc=0.

Proposals below preserve every exercised path, including these two self-test surfaces.

---

## Findings — `tools/mori-pin-check.py`

### F1. Dead parameter `scratch` on `run_cmd()` and `check()` (real dead code)

- `run_cmd(words, root, scratch, timeout)` at `tools/mori-pin-check.py:183` never reads `scratch`
  anywhere in its body (184–199): it derives `tmp_parent = os.path.join(root, ".scratch")` and
  builds its own temp dir there. The parameter is dead.
- `check(text, root, scratch, rev, timeout, min_tally, baseline_text=None)` at `:221` accepts a
  `scratch` parameter used only to forward it (unused) to `run_cmd` at `:256`.
- Call sites: selftest cases `:454` and `:461` fabricate fresh per-case dirs solely for this dead
  path; `main` `:367` forwards the scratch dir it already uses for `export_rev` (`:338`, `:342`,
  `:370`).
- Proposal (future version): remove the `scratch` parameter from `run_cmd` and `check`, and drop the
  argument at `:256`, `:454`, `:461`, `:367`. Behavior preserved: all created temp dirs are already
  independent of `scratch` (self-test green with the parameter ignored; `main`'s scratch remains
  needed for `export_rev` tar extraction).

### F2. Option `--timeout` is never exercised (option not needed by the frozen predicate)

- `--timeout` argparse entry at `:327`; `TIMEOUT_S = 600` default at `:65`.
- No caller in the frozen material passes it: contract P-C1 command (`contract.md:30`), all three C1
  control receipts (`.ufo/waves/round-47/evidence/control-c1-*.txt:1`), `w1-spec.json` prompts
  (ExecC1Controls, CritC1Predicate), and `QUALITY.md:1035` use only `--rev`, `--min-tally-pins`,
  `--baseline-rev`, `--skill`. Fleet-wide grep for `mori-pin-check` shows no other caller.
- The tool's own selftest calls `check(...)` directly with a hard-coded `5` (`:454`, `:461`) and the
  CLI arms (`:467`, `:470`) run with default args — neither supplies `--timeout`.
- Proposal (future version): drop `--timeout` and hard-code `TIMEOUT_S`. Behavior identical on every
  exercised path (the default is the only value ever effective). Tradeoff: loses a tuning knob for
  third-party invocation; if the maintainers want to keep a knob, at minimum document it as unused.

### F3. Not proposals (examined and rejected)

- `--skill` (`:323`) is **used**: C1 control receipts run `--skill .ufo/waves/round-47/controls/control-c1-{deleted,moved,truncated}.md` (`evidence/control-c1-*.txt:1`), and `w1-spec.json` ExecC1Controls/CritC1Predicate prompt with and without it. Keep.
- `--root` (`:321`) is used by the tool's own selftest CLI arm (`:467`). Keep (part of the test surface).
- `--repo` (`:322`) is required by `--rev`/`--baseline-rev` and by `export_rev`. Keep.
- `--min-tally-pins`, `--baseline-rev`, `--selftest`: frozen predicate surface. Keep.

---

## Findings — `.ufo/waves/round-47/count-c2.py`

### F4. (Cross-file) duplicated helpers, not dead code

None of count-c2's own code is dead: `ROW_ID`, `ENTRY`, `SRC_DIR`, `OOM_H`, `PINS`, `COPY_OF`,
`SPAN`, `parse_events`, `split_cells`, `parse_table`, `sources_row`, `evaluate`, `git_reader`,
`main`, `fake_tree`, `selftest` are all reachable and exercised (self-test 13/13 green). Three
helpers are duplicated against `tools/mori-pin-check.py` with near-identical semantics:

1. `split_cells` — `count-c2.py:70-72` vs `mori-pin-check.py:73-82`. Same unescaped-pipe split
   regex `(?<!\\)\|`; the two differ in edge handling (mori strips, guards a leading `|`, and
   normalizes a missing trailing pipe; count unconditionally slices `[1:-1]`).
2. Backtick span regex — `SPAN` at `count-c2.py:47` vs `SPAN_RE` at `mori-pin-check.py:68`
   (identical pattern `` `([^`]+)` ``).
3. Markdown separator matcher — `count-c2.py:88` inlines `re.fullmatch(r":?-{3,}:?", c)` where
   `mori-pin-check.py:85-86` has `is_separator()`.

Proposal (optional, future): if the lane wants to fight duplication, extract one small shared
`md-table` helper module (split on unescaped `|`, separator detection, span regex) and import it
from both tools. Behavior preservation requires keeping each file's exact edge semantics (the two
`split_cells` are not interchangeable as-is), so this is a real integration cost for a cosmetic win;
for a wave-local counter, the duplication may be the cheaper trade.

### F5. Not proposals (examined and rejected)

- `--entry` (`:195-196`) is **used**: C2 control receipts run `--entry .ufo/waves/round-47/controls/control-c2-{staged,three}.md` (`evidence/control-c2-*.txt:1`), and `w1-spec.json` ExecC2Controls/CritC2Predicate rely on it. Keep.
- `--repo` (`:193-194`) is used by the selftest CLI arm (`:281`). Keep.
- `--selftest` (`:188`): lane instrument self-assessment surface. Keep.

---

## Summary

| # | File | Line(s) | Kind | Proposal |
|---|------|---------|------|----------|
| F1 | `tools/mori-pin-check.py` | 183, 221, 256, 367, 454, 461 | dead parameter | drop `scratch` param from `run_cmd`/`check` |
| F2 | `tools/mori-pin-check.py` | 65, 327 | option not needed by frozen predicate | drop `--timeout` (hard-code `TIMEOUT_S`) |
| F4 | both tools | count 47,70-72,88; mori 68,73-82,85-86 | duplicated helpers (cross-file) | optional shared md-table helper; keep per-file edge semantics |
| F3/F5 | both tools | `--skill`, `--entry`, `--root`, `--repo`, `--min-tally-pins`, `--baseline-rev`, `--selftest` | kept | all have live callers in the frozen predicate/controls/selftest surface |

Tradeoffs: F1 is a pure deletion (no observable change). F2 removes an unexercised knob; the only
cost is losing flexibility for hypothetical future callers. F4 is optional and costs integration
effort, so it is offered as a considered option rather than a recommendation. No other deletion
candidate survives scrutiny: the two counters are tight — every remaining helper, constant, and
option has a live caller in the frozen predicate, its controls, or the tool's own selftest.

Evidence recorded: `sha256sum` of both tools (match freeze), both `--selftest` transcripts (green),
fleet-wide grep for `mori-pin-check` / `count-c2.py`, and round-47 control receipts
`evidence/control-c1-*.txt` / `evidence/control-c2-*.txt` showing `--skill`/`--entry` usage.
LSP unavailable (recorded above); grep is literal fallback. No files changed.
