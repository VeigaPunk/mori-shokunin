# SimpCounters — round-39 wave 1 deletion report (mori-r39.SimpCounters)

Date: 2026-10-24. Target bytes: `.ufo/waves/round-39/count-c7.py` (sha256 `b92c65f2…f324ef0520`) and
`.ufo/waves/round-39/conform.py` (sha256 `fe0be179…d46ef7987`), both byte-identical to
`evidence/freeze-r39.txt` pins at reporting time (verified by `sha256sum` + grep of the pin file).
Line numbers below are 1-based on those pinned bytes. All work was done on copies under
`.ufo/waves/round-39/scratch/SimpCounters/`; the lane files were never edited.

## Deletion list (routed to round 40 — the freeze pins these bytes)

| # | File | Lines | What | Why dead |
|---|------|-------|------|----------|
| D1 | count-c7.py | 98 | `ROWSTATES_RE = re.compile(r"^selftest row_states (PASS\|FAIL) (\(.*\))$")` | Zero references anywhere in the file after definition. The v2 parser `parse_rowstates` (count-c7.py:333-340) intentionally uses its own, more lenient inline regex `^selftest row_states (PASS\|FAIL)(?:\s+\((.*)\))?$` (detail group optional; ROWSTATES_RE requires the ` (...)` suffix). D1 is the superseded v1 pattern left behind by the v2 rewrite. |
| D2 | count-c7.py | 441-444 | `table = None` / `if arm and arm[0] == "FAIL":` / `parsed = parse_got_want(arm[1])` / `table = parsed[0] if parsed else None` | `table` is assigned and never read anywhere after (the `--arms selftest` branch ends at the `PASS`/fail prints; the name `table` at 359/366 is an unrelated local function inside `parse_got_want`). `parse_got_want` is pure (literal_eval + dict building) and remains used by the `drift_kill_v2` block, so removing this call orphans nothing. |
| D3 | conform.py | 289-293 | `"has_communicate_timeout": …` dict entry in `static_checks`' return | Computed (an extra AST walk) but never read. `evaluate` and `selftest` consume only `comm_violations` (conform.py:408,416,418), `bounded_violations`, `value_violations`, `drain_violations`, `mkdtemp_ok`, `scratch_root`, `blob_cap` (conform.py:246-421) — all nine CHECK_NAMES verdicts derive from those. |
| D4 | conform.py | 294, 296-300 | `"first_communicate_segment": _first_communicate_segment(source)` dict entry and `def _first_communicate_segment` (298-300) | The key is never read and the function has no other caller: the `selftest_conjunct` check does its own `re.subn(r"proc\.communicate\(timeout=[^)]+\)", …)` (conform.py:411-412) instead of reusing it. Delete the key line, the two blank lines at 296-297 and the 3-line def; two blank lines remain between `static_checks` and `evaluate` (PEP8-clean, exactly what the verified diff produces). |

Total: 1 + 4 + 5 + 6 = 16 lines removed across two files.

## Behavior-preservation argument

1. **No semantic callers.** No `lsp` device is available in this session (tool inventory lacks it) —
   text sweep used as the recorded fallback: a regex sweep of the whole round-39 wave dir for
   `ROWSTATES_RE|has_communicate_timeout|first_communicate_segment` hits only (a) the definition
   sites, (b) sibling seats' pristine copies under `scratch/` (byte copies, not importers), and
   (c) `gen-wave1-spec.py:182`, which quotes my own tasking text. Neither file can be imported as a
   module (dashes in filenames); the only inter-file coupling is conform.py reading count-c7.py as
   *text* (static audit + 9 mutation anchors), handled next.
2. **Mutation-anchor safety (the FAIL condition).** All nine textual mutation anchors that
   conform.py's `--selftest` applies to count-c7.py bytes (conform.py:351-376, drain anchors
   382-384) live outside D1-D4: the docstring phrase (14-15), `print("head_at_measurement=%s"`
   (464), the abspath print (471), the git-run block (192-193), `GIT_TIMEOUT_S = 120` (67), run()'s
   communicate/raise block (105-136), `proc = run_tool(args.tool, ["--selftest"], args.tool_timeout)`
   (437), the `SCRATCH_ROOT = os.path.join(DEFAULT_REPO, …)` line (61), and the first
   `out, err = proc.communicate(timeout=timeout)` (106). D1-D4 touch none of them, and static
   checks don't depend on the deleted text: `blob_cap` needs `MAX_BLOB_BYTES` + `"-s"` (kept, 69/188),
   `scratch_root` needs the SCRATCH_ROOT 4-segment string (kept), `timeout_value` resolution only
   maps names referenced by `timeout=` kwargs (ROWSTATES_RE is never so referenced).
3. **No printed line changes.** Every deleted line is assignment/definition-only control- or
   data-flow that produces no output; the receipts (`C7=met`, `CONFORM=met`,
   `CONFORM_SELFTEST pass=9 fail=0`), check/negative lines, and `--print-predicate` bytes are
   unchanged — proven byte-for-byte below.

## Verification (all run 2026-10-24, repo /home/vgpnk/Projects/shokunin/mori-shokunin)

Baseline = lane scripts at the pinned bytes; variant = scratch copies with D1-D4 applied
(diff artifacts: `scratch/SimpCounters/count-c7.del.diff`, `conform.del.diff` — exactly the 16 lines above, nothing else).
`R = 13bfba23b7ca063c76d3504a2ff6eb7b6a294932`, `--seed 20261024`.

| Check | Command | Result |
|---|---|---|
| C1 main run | `count-c7.py $R --seed 20261024` (variant) vs baseline | exit 0 both; stdout **byte-identical** (`C7STDOUT-IDENTICAL`): 4 negatives rejected, 5 checks PASS, `C7=met` |
| predicate print | `--print-predicate` variant vs baseline | **byte-identical** (`PP-IDENTICAL`) |
| pin print | `--pin-only` back-to-back pristine vs variant | **byte-identical** (`PIN-IDENTICAL`) — see note (a) |
| tool print | `--print-tool <fixture rel>` variant vs baseline | **byte-identical** (`PT-IDENTICAL`) |
| C2 plain | `conform.py $R` (variant, defaults → lane counter) vs pristine run seconds earlier | exit 0; **byte-identical** (`C8STDOUT-IDENTICAL`), `CONFORM=met` |
| C2 selftest | `conform.py $R --selftest --counter <variant counter>` (both files deleted) | exit 0, `CONFORM_SELFTEST pass=9 fail=0`; stdout **byte-identical** to baseline selftest (`C8SELFTEST-IDENTICAL`) — all nine mutations still flip exactly their own check |

Notes: (a) the first variant/conform runs showed a `head_pin` hash difference only, because the
lane tip moved during the session (HEAD `ebc61f47…` → `143d2d32…`, another seat landing); the
back-to-back pairs show that with a stable tip the outputs are byte-identical. C7's main run is
rev-pinned and unaffected by HEAD. (b) A variant counter copy run from a directory without a
`fixtures/` neighbor exits 2 (`counter setup error: … fixtures/witness-token-entry.md`) because
count-c7.py resolves witnesses relative to `__file__` — a copy-location artifact, not a deletion
effect; round-40 appliers should run the edited file in place.

## Retained duplication — flagged, NOT proposed (would fail or trade away anchors)

- `run()` vs `run_tool()` in count-c7.py share the SIGTERM→grace→SIGKILL ladder (105-136 vs 138-180):
  merging would move/rewrite bytes that are the drain_shape extraction block and the
  bounded_reads/selftest_conjunct anchors. Flagged as duplication; no deletion proposed.
- conform.py `run()` (85-96) inlines the env-clean loop that count-c7.py factors as `clean_env()`:
  cross-file helper sharing would create an import between counter and checker — rejected.

## Bounds compliance

Exactly one non-scratch file written (this report). Lane repo untouched — verified by sha256
equality with the freeze pins above. No tool installs or upgrades were needed (tooling directive:
nothing to record). Not sent to any peer; this report is the result.
