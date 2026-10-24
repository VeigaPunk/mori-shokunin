# SimpGateV3 — gate v3 dead-code hunt (mori round 40, w1)

Seat: findings-only simplifier. **No production edits made.** The only lane file written is
this report; the fleet repo was never written; no git/jj mutating command was run.

Target bytes: `tools/mori-sources-appendonly.py` at scored tip `265a955c`
(sha256 `bde5a9a34c7eb3bc…`, 919 lines). Lane worktree verified **byte-identical** to the
scored tip before any run. Baseline for provenance: entering tip `bb1f2457` bytes (v2, 818 lines),
extracted read-only via `git show`.

## Axes

A semantic proof of absence · B coverage (v3-introduced **and** v2-left-behind) ·
C report precision (file:line + exact commands) · D harm-freeze (frozen bytes untouched).

## Method and tooling

- `xd://lsp` does **not exist** on this host (mounted devices: `ast_edit`, `debug` only) —
  no language server answered; per protocol this is recorded, and the text/AST evidence below
  is labeled as fallback, not semantic proof.
- AST cross-check (stdlib `ast`): every top-level def/constant counted against all `Name`/`Attribute`
  uses in the module.
- `uvx ruff@0.8.4 check --select F,ARG,ERA` (uv channel; **pacman untouched** per the host-wide
  pause) → `All checks passed!` — no unused imports (F401), no unused locals (F841), no unused
  arguments, no commented-out code (ERA).
- `uvx vulture@2.14 --min-confidence 0` → single hit: `221: unused function 'superseders' (60%)`.
- Scoped import check `grep '^\s*(import|from)\s+mori_sources_appendonly\b'` over `tools/`,
  `corpus/`, `.ufo/waves/round-40/` → **no matches**: the gate module has zero in-repo importers;
  every consumer drives it as a CLI over stdout (e.g. `.ufo/waves/round-40/fixtures/run-c11-dags.py`,
  the counters). A first unscoped lane-wide grep timed out at 30 s; the scoped rerun completed.
- v2↔v3 diff (`diff -u` of the two `git show` extractions; v3 = +149/−48).

## Findings

### F1 — `superseders()` is dead: tools/mori-sources-appendonly.py:221-230

`def superseders(rows, colmap)` — **zero references** module-wide (AST name count = 0; vulture's
only flag; ruff clean). Not called from anywhere in the lane (no module importers exist; all
consumers are subprocess CLI).

Provenance: orphaned by round-39's v2, not by v3. v2 already built `sup_map` from the
`supersede_landing` walk (`sup_map = {target: by for target, (_, by) in supersede_landing.items()}`,
v2:342 / v3:350) and v2:229 carried the same zero-call def; v3 inherited it unchanged. Its
first-wins semantics ("first one wins", :222) were replaced by the landing walk's **last**-wins
latest-superseder rule (v3:347-350), so it is semantically superseded, not just unreferenced.
≈10 dead lines, behavior-neutral to delete.

### F2 — no-op self-assignment: tools/mori-sources-appendonly.py:660

`shas["c1"] = shas["c1"]` at the end of the `_make_dag_repo` dag-c branch. Pure no-op (inherited
from v2:598).

### F3 — dead store on the error path: tools/mori-sources-appendonly.py:793

`summary = lines[-1] if lines else ""` in `check_one` runs only when `len(summary_lines) != 1`;
`summary` is read solely under `if summary_lines:` (→ `SUMMARY_RE.match(summary)`, :800-801) —
exactly the branch where :793 did **not** execute. (Inherited from v2:692.)

### F4 — unreachable fallback branch: tools/mori-sources-appendonly.py:210-211

`if not colmap: colmap = {name: index …}` in `immutable_indices` is unreachable from its only
caller (analyze:283): `colmap` there is always truthy — `parse_registry` returns `None` (→
`GateError` at :260) or a map built from a header with ≥5 cells, and analyze falls back to the
validated `tip_colmap` (:281-282). With zero in-repo importers, no external caller can reach the
guard either. (Inherited from v2:218.)

### F5 — write-only `analyze()` return keys: tools/mori-sources-appendonly.py:387,393,394

`"rev": rev_full`, `"commits": commits`, `"rows": len(tip)` are never read: `report()` consumes
ids/superseded_by/deleted/violations/superseded/round_changed/superseded_as_of/stale_supersede
(:405-418) and `main()` consumes round_changed/ids/deleted (:913-915); the full `result["…"]` read
set was enumerated by grep. These keys are stdout-invisible, so removing them does not touch the
"byte-identical in shape to v2" output contract. (Inherited from v2:371,380,381.)

### F6 — dead defensive idiom: tools/mori-sources-appendonly.py:291

`teaches_idx = (colmap or {}).get("teaches", …)` — `colmap` cannot be falsy at this point (same
:281-282 guarantee as F4); `or {}` is unreachable. (Inherited from v2:291.)

### F7 — duplicated environment scrubbing: tools/mori-sources-appendonly.py:424-433

`_selftest_env()` re-implements `_clean_env()`'s six-key GIT_* pop loop (:105-110) key-for-key
instead of calling it. A second convention for one job; `_selftest_env` could be
`env = _clean_env(); env["GIT_CONFIG_NOSYSTEM"]="1"; env["GIT_TERMINAL_PROMPT"]="0"`.
(Inherited from v2:411.)

## Checked and alive (non-findings)

- All imports (`argparse os re shutil subprocess sys tempfile`) used — ruff F401 clean.
- v3's P-C11 refactor left no other orphans: `nearest_path_commit` (v2:159) was **deleted** by v3,
  not left dead; the deliberate removal of the `elif not is_merge` re-add branch is commented at
  its site (:336-339), not stubbed.
- The `else: head_text = git_blob(repo, "%s:%s" % (head, path))` branch (:322-325) is reachable —
  first parents of walk commits that never touched the path are absent from the `--full-history`
  walk (common on merge-heavy lane history); not dead.
- All 12 DAG fixture bodies returned by `_selftest_dag_cases` are unpacked and consumed by
  `_make_dag_repo`; all locals of `_selftest_cases` are used by the nine cases; `_dag_merge`,
  `is_ancestor`, `immutable_indices`, `imm_key`, `format_list` each have live callers.

## Preserved-contract proof (commands actually run, cwd = lane repo)

1. `python3 tools/mori-sources-appendonly.py --selftest`
   → `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` (matches the declared C2 receipt shape).
2. `python3 tools/mori-sources-appendonly.py HEAD | grep -v P-C11`
   → 18 `changed …` lines (S041…S193, each with its superseder), then
   `appendonly_violations=18 ids=[S041,…,S193] deleted=[] superseded=[34 ids] round_changed=[]`,
   then `supersede_timing superseded_as_of=[34 ids incl. S226] stale_supersede=[]` —
   matches the tasked tip line (34 as-of ids incl. S226, none stale).

Both ran on worktree bytes proven equal to the scored tip (sha256 match), so these are the scored
tip's verdicts.

## Tradeoff / stop boundary

The gate bytes are contract-frozen (P-C11 verbatim in `PREDICATE`; pins in
`evidence/freeze-r40.txt`; "a change to a predicate after this freeze is a new counter version").
Applying any deletion now would break the freeze and invalidate the C2 receipts, so this seat
stops at findings: F1–F5 (≈16 lines) are behavior-neutral deletion candidates for the **next**
round, each provable afterwards by rerunning the two commands above plus a lane+fixture stdout
byte-comparison. F6/F7 are style-level and optional. No further deletion inside this file would
improve any axis without harming the freeze axis.
