# OracleLoss — round 21 scoped report

## Files changed

- `.scratch/round21/OracleLoss/oracle-loss.py` — standalone stdlib black-box receipt harness, in the isolated `e9f340ce986f82a60baad1b8e5ead655ab818a1c` clone.
- `.ufo/waves/round-21/build/OracleLoss.md` — this advisory report.

No production files, fleet state, or sibling files were edited. No tool was installed.

## Behavior implemented

The required CLI accepts `--tool --root --required --before-accounting --after-accounting --before-rule --after-rule --cases --out`. It makes four real target subprocess calls (before/after `audit`, before/after `classify`) concurrently, without importing target code or using a shell. Each receipt preserves the exact argv, cwd, return code, decoded stdout/stderr, and base64 stdout/stderr bytes; launch failures are retained explicitly.

For classify, it compares the target's observed per-case class and pin decision against the supplied frozen expected pairs, records per-case matches/mismatches and independently tallies mismatches. It also records and compares CLI summary claims when present. It does not infer a verdict from the before/after phase or rule value.

For audit, it reads the supplied required/accounting JSON independently, computes missing required IDs, and compares its omitted count with the CLI result. When a missing required observation (or a represented unresolved required observation) is present, it also records whether the CLI kept `pin_allowed` false. It preserves the CLI result and all process receipts in the JSON report at `--out`. The harness's own status indicates only whether it wrote that report; target return codes are per-run fields.

## Retained evidence

- `.ufo/waves/round-21/contract.md:13-16` — shared audit/classify interface and behavior.
- `.ufo/waves/round-21/frozen/cases.json:1-53` — six frozen classifier expectations.
- `.ufo/waves/round-21/frozen/required.json:1-23` — required IDs `aggregator-r10` and `aggregator-r10-resume`.
- `.ufo/waves/round-21/frozen/before-accounting.json:1-4` — currently empty observations array.
- `.ufo/waves/round-21/frozen/before-rule.json:1-6` and `after-rule.json:1-5` — explicit old and superseding rule objects.
- Read-only clone identity: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round21/OracleLoss rev-parse HEAD` returned `e9f340ce986f82a60baad1b8e5ead655ab818a1c`.
- Read-only target availability check at that base: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/round21/OracleLoss cat-file -e e9f340ce986f82a60baad1b8e5ead655ab818a1c:tools/mori-evidence-loss.py` returned exit 128 with `fatal: path 'tools/mori-evidence-loss.py' does not exist in 'e9f340ce986f82a60baad1b8e5ead655ab818a1c'`.
- A read-only listing showed a candidate at `.scratch/round21/ImplLoss/tools/mori-evidence-loss.py`; it was not executed or imported.

## Risks and blockers

- No test, build, lint, formatter, or target CLI invocation was run. Thus no actual target subprocess receipts or observed before/after decisions are claimed in this report; the harness records them when invoked.
- The OracleLoss clone is the requested base commit and lacks the target CLI at `tools/mori-evidence-loss.py`. The frozen-directory listing contained `before-accounting.json` but no `after-accounting.json`; a complete four-call run needs the implementation path and after-accounting input supplied by integration.
- No claim of settlement or pin permission is made here. Main owns post-integration verification.
