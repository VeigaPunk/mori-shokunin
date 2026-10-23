# RevGateRegistry — SKILL.md gate registry at f725f307

Tip `f725f3076972e6e70595b5ac8279be524a111ff8` (HEAD; `SKILL.md` clean against that commit). Schema: `PROTOCOL.md:401-402` (§Gate standard, Registry). Eight fields: name, `gate|probe`, entry command, verdict map (code → class), self-test command and spelling, pinned-value path, write scope, owner. Lane table header is those eight, renamed `kind` / `self-test` / `pinned values` (`SKILL.md:874`).

Axes: field presence, self-test flag spelling, `supersede_timing` line resolution, r38 instrument rows.

**Verdict: not FAIL.** The append-only gate and all three r38 instruments have a row, and every schema field is non-empty. No field is absent. Content gaps below are unlabeled classes and a probe that can exit 1, not missing cells.

Installs: none.

## Append-only gate — `SKILL.md:877` (r36 row, same tool)

| field | cell |
|---|---|
| name | SOURCES append-only (r36) |
| kind | gate |
| entry | `python3 tools/mori-sources-appendonly.py <rev> [--repo DIR] [--round-base REV] [--path P]` |
| verdict map | with `--round-base`: 0 `round_changed=[]` · 1 non-empty; without: 0 no `ids` and no `deleted` · 1 otherwise; 2 git or parse error |
| self-test | `python3 tools/mori-sources-appendonly.py --selftest` (9 sandbox histories through the CLI, incl. supersede-before-edit) |
| pinned values | git history of `corpus/SOURCES.md`; immutable = every column but status, recheck, used-by |
| write scope | none (read-only git; self-test temp dir removed) |
| owner | mori |

Entry flags match `mori-sources-appendonly.py --help` (`rev`, `--repo`, `--round-base`, `--path`). `--selftest` is the self-test flag (`tools/mori-sources-appendonly.py:560-561`), not a second spelling. Immutable columns match `MUTABLE = ("status", "recheck", "used-by")` (`tools/mori-sources-appendonly.py:66`). `corpus/SOURCES.md` is in the commit.

Self-test spelling resolves. Ran `python3 tools/mori-sources-appendonly.py --selftest` from the lane root: stdout `MORI_SOURCES_APPENDONLY_SELFTEST pass=9 fail=0`, exit 0. Source cases are nine (`tools/mori-sources-appendonly.py:421-451`), including `"supersede before edit"` (`:441`, expects `stale_supersede: ["S001"]`). The row's hyphenated `supersede-before-edit` is that case, not a second flag. The after-edit case in source is named `"superseding row"` (`:437`), not `supersede after edit`; the row does not claim that name.

Code 2 is declared as `git or parse error`, which matches `main` returning 2 on `GateError` (`tools/mori-sources-appendonly.py:47-50`, `:577-579`). The cell does not write the class word `could-not-evaluate`. Codes 0 and 1 are the fleet-wide clean/failed pair (`PROTOCOL.md:380-381`) expressed as lane tokens. The class word for 2 is the only unlabeled half.

## `supersede_timing` description — exists and the printed line matches

Prose, not only the table: `SKILL.md:867-868` states the line ``supersede_timing superseded_as_of=[...] stale_supersede=[...]`` and that it separates a disposition that postdates the edit from one that predates it. `QUALITY 110` resolves at `corpus/QUALITY.md:889-893` (same line, same rule). `QUALITY 102` is `:799`; `QUALITY 104` is `:829` (points at this gate, not the round-35 script). The replaced script `.ufo/waves/round-35/check-sources-appendonly.py` is still in the commit.

The r38 row for the same tool is `SKILL.md:883`:

| field | cell |
|---|---|
| name | SOURCES append-only timing (r38) |
| kind | gate |
| entry | `python3 tools/mori-sources-appendonly.py <rev> --round-base REV` |
| verdict map | summary exit as before; the extra line ``supersede_timing superseded_as_of=[...] stale_supersede=[...]`` is the finding |
| self-test | `--selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=9 fail=0` |
| pinned values | latest-superseder landing index vs last immutable-edit index over the `corpus/SOURCES.md` history |
| write scope | none (read-only git) |
| owner | mori |

Ran `python3 tools/mori-sources-appendonly.py f725f3076972e6e70595b5ac8279be524a111ff8 --round-base f10a320d`. Exit 1. Last two stdout lines:

```
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[S182,S193]
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[]
```

The line matches `TIMING_RE` (`tools/mori-sources-appendonly.py:73-74`) and the prose. S069 is in `superseded_as_of`, not `stale_supersede`. Exit 1 is the r36 map (non-empty `round_changed`), not a timing-list exit: `main` returns on `round_changed` / `ids` / `deleted` only (`:583-585`). `stale_supersede` does not change the code. "Summary exit as before" matches that. The timing row does not restate 0/1/2; the map is the r36 cell by reference.

`SKILL.md:864-865` says land only with `round_changed=[]` (exit 0). This tip does not: `round_changed=[S182,S193]`. That is the landing rule at this revision, not a missing registry cell.

Self-test cell spelling is the same `--selftest` flag, and the finding-id line is the string just run (`pass=9 fail=0`).

## r38 instruments

### content-anchor check — `SKILL.md:881`

| field | cell |
|---|---|
| name | content-anchor check (r38) |
| kind | probe |
| entry | `python3 .ufo/waves/round-38/count-c4.py <rev> [--repo DIR]` |
| verdict map | 0 `C4=met` · 1 `C4=unmet` · 2 setup error |
| self-test | none (the three fabricated witnesses under `.ufo/waves/round-38/fixtures/` are the able-to-fail evidence; the mutation arm `drift_kill` is a check) |
| pinned values | `anchor:` entry lines resolved in `tools/mori-source-drift.py`; repo-relative capability paths; `row_states` arm; `return "drifted"` mutated to `return "excerpt"` |
| write scope | none (read-only; scratch under `.ufo/waves/round-38/scratch`) |
| owner | mori |

`count-c4.py --help` is `[-h] [--repo REPO] rev`. Exit 2 is implemented (`count-c4.py:233`, `:243`, `:304`, `:341`); 0/1 at `:331-333`. Code 2 is not labeled `could-not-evaluate`.

Pins that resolve: `return "drifted"` at `tools/mori-source-drift.py:208`; `row_states` at `:390`; mutant pair `DRIFT_MUTANT_FROM` / `DRIFT_MUTANT_TO` at `count-c4.py:47-48`. Witness files present: `fixtures/witness-token-entry.md`, `witness-dangling-row.md`, `witness-summary-only-live.txt`. No `--selftest` on this program (help has none). The cell says `none` on purpose. Kind is `probe` while the map and the code exit 1, so it can fail. `PROTOCOL.md:378-379` defines a probe as a tool that cannot fail. The cell is filled; the kind value is the mismatch. Self-test spelling is explicitly absent, which the standard requires of a gate (`PROTOCOL.md:385-389`), not of a probe.

### counter conformance — `SKILL.md:882`

| field | cell |
|---|---|
| name | counter conformance (r38) |
| kind | gate |
| entry | `python3 .ufo/waves/round-38/conform.py <rev> [--counter PATH]... [--selftest]` |
| verdict map | 0 `CONFORM=met` · 1 unmet · 2 setup error |
| self-test | `--selftest` (six mutations, each flips exactly its own check) |
| pinned values | contract P-C1 bytes; `head_at_measurement`; lane-relative `--tool`; bounded reads; `tool_timeout` state; lane scratch parent |
| write scope | read-only (runs the counter under test) |
| owner | mori |

`conform.py --help` includes `[rev]`, `--counter`, `--selftest` (also `--repo`, `--contract`, not named in the entry cell). Flag spelling `--selftest` is `conform.py:262`. The printer is `CONFORM_SELFTEST pass=%d fail=%d` (`:252`); the row does not quote that finding-id. Six mutation names are `predicate`, `head_pin`, `tool_resolve`, `bounded_reads`, `timeout_state`, `scratch` (`:215-228`). Exit 0/1 at `:281-283`; exit 2 on `SetupError` (`:275-277`, `:291`). Code 2 is not labeled `could-not-evaluate`.

Pin tokens resolve in `count-c1.py`, not as their own paths in the cell: `head_at_measurement` (`:951`, `:65`), `tool_timeout` (`:715`, `:818`), `SCRATCH_ROOT` under `.ufo/waves/round-38/scratch` (`:70`). No path string is written in the cell. The lane column has long accepted non-path pin text (census, `SKILL.md:164`). Not an empty field.

This seat did not re-run the six-mutation `--selftest`. Flag and finding-id are source-resolved only.

## Schema gaps (not missing cells)

- Code 2 on the r36 gate, the content-anchor row, and the conformance row is declared but not mapped onto the word `could-not-evaluate` (`PROTOCOL.md:380-382`, `:402`).
- The r38 timing verdict map has no codes of its own; it defers with "summary exit as before". That matches the implementation (the timing line is not an exit).
- content-anchor is registered `probe` with self-test `none` even though it exits 1.

Confidence: high on the four cells, the self-test run, and the timing-line run. The six-mutation conformance self-test was not re-executed here.
