# RevC1Interface — C1 tool / registry / knowledge-note review

Scope: additions at `bf0df77fee4b6ef54a90aea09335c7617f125151` against round base `6bd57097`, limited to `tools/mori-source-drift.py`, the `source drift (r36)` row in `SKILL.md`, and `corpus/knowledge/source-drift-r36.md`.

## Findings

### P2 — `excerpt` omits the classifier's non-empty-copy condition

`tools/mori-source-drift.py:151-154` returns `excerpt` only when the edge-stripped copy is non-empty and present in the body. `corpus/knowledge/source-drift-r36.md:24` says only that the stripped copy occurs contiguously; for a whitespace-only copy that description implies `excerpt`, while the code returns `drifted`.

Measurement:
- Command: `python3 -c 'import importlib.util; p="/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-source-drift.py"; s=importlib.util.spec_from_file_location("mori_source_drift",p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); print(repr(m.classify(b"body", b" \n\t "))) '
- Observed output: `'drifted'`

### P2 — `no-copy` documentation omits an unreadable-copy path

`tools/mori-source-drift.py:176-182` maps an `OSError` while opening an existing selected copy to `no-copy`, and skips fetching it. The table at `corpus/knowledge/source-drift-r36.md:27` defines that state only as no URL or no copy file, then advises saving a copy. An existing but unreadable copy therefore has an undocumented state cause and a potentially misleading reader action.

### P2 — exit-2 cause descriptions are incomplete

The code returns 2 for a non-directory `--root` and for bad usage (`tools/mori-source-drift.py:366-375`), in addition to the missing/unreadable `SOURCES.md` case. The registry row (`SKILL.md:872`) and note (`corpus/knowledge/source-drift-r36.md:28`) describe exit 2 only with the latter cause.

Measurements:
- Command: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-source-drift.py --root /definitely-not-a-directory 2>&1; printf 'exit=%s\n' "$?"`
- Observed output: `MORI_SOURCE_DRIFT_SETUP: /definitely-not-a-directory is not a directory` followed by `exit=2`.
- Command: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-source-drift.py 2>&1; printf 'exit=%s\n' "$?"`
- Observed output: `usage: mori-source-drift.py --root DIR | --selftest` followed by `exit=2`.

The broad “could-not-evaluate” category is correct; its documented causes are not complete.

### P2 — dated drift-row explanation conflicts with the current C1 receipt

`corpus/knowledge/source-drift-r36.md:16-19` says that the seven drifted rows on 2026-10-23 were the five S156–S160 excerpts plus S176/S177. The after receipt for the assigned tip records nine oracle-drifted rows, with none excluded (`.ufo/waves/round-36/evidence/c1-after.txt:3`). Thus the note's dated statement does not account for the complete current measured set; if those seven are from a different run, the note does not identify it as such.

Recorded counter invocation form (from `count-c1.py:4`): `python3 .ufo/waves/round-36/count-c1.py <rev> [--repo DIR] [--tool FILE] [--seed N]`.
- Stored observed output (`evidence/c1-after.txt:3`): `real_rows=220 oracle_fetched=58 oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220 mismatches=0`.

## Checks with no finding

- Entry command matches: `SKILL.md:872` uses `python3 tools/mori-source-drift.py --root <repo>`; tool usage at `tools/mori-source-drift.py:5-7,363-372` accepts `--root DIR`.
- Verdict meanings for 0 and 1 match `tools/mori-source-drift.py:197`. The 2-category caveat is above.
- The `--selftest` claim matches the code: `tools/mori-source-drift.py:229-235` binds its fixture server to `127.0.0.1`; `:240-350` creates temporary roots and removes them in `finally`; `:363-365` dispatches `--selftest`.
- Command: `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-source-drift.py --selftest`
- Observed output:
  ```
  selftest exit_code            PASS
  selftest row_states           PASS
  selftest summary              PASS
  selftest missing_sources_exit2 PASS
  MORI_SOURCE_DRIFT_SELFTEST: PASS (4 cases)
  ```
- The required warning is present in both documents: `SKILL.md:859-861` says read `drifted` never as a changed source; the note says the same at `:15-19`. The note calls the probe exploratory and not a gate (`:5-13`), and limits `fresh` to byte identity rather than correctness of `teaches` (`:15`); no freshness-admission claim was found in these surfaces.

## Residual risk and verification gaps

LSP is unavailable in this environment: `read xd://lsp` returned `No such tool: xd://lsp. Mounted devices: ast_edit, debug.` No LSP references/definition/diagnostics checks were possible. Findings above use the directly read source and documentation, plus the cited runtime probes. The selftest passes but does not cover a whitespace-only copy or an unreadable existing copy.

VERDICT: FAIL — interface/documentation divergences above.