# Round 17 C1 case review — assigned two cases

Axes reviewed: contract fidelity, fixture/control discrimination, retained-result integrity.

## Findings

### P2 — `duplicate_stems_two_entries` does not assert the duplicate counter

The fixture and class expectations are source-supported: both inputs are pinned byte-identical `version:3` sessions at `DuplicateStems/d1/stem.jsonl` and `d2/stem.jsonl` (`fixtures/seat/expected.json:12-13`; input records at `fixtures/seat/DuplicateStems/d1/stem.jsonl:1-2` and `.../d2/stem.jsonl:1-2`). Each has an assistant error with status 429, `rate_limit`, and `completedAt=1760998000000`; the pinned `--now-ms=1761000000000` and 900-second settle window make each error old enough to be `dead_rate_limit` (contract `contract.md:113-114`; classifier `tools/mori-seat-terminal.py:247-273`). The expected `rc=1`, finding, all eight totals, and both distinct relative keys/classes at `fixtures/seat/expected.json:1361-1383` are independently derivable from those bytes.

The retained after stdout agrees with every asserted field: two seats (`d1/stem`, `d2/stem`), both `dead_rate_limit`; `dead_rate_limit=2`, all other totals zero; `MORI_SEAT_TERMINAL_DEAD`, rc 1 (`evidence/seat-after/runs/duplicate_stems_two_entries.stdout:1`). Its observed `duplicate_stems` is also correctly 1. However, the case never asserts that field. `WANT_KEYS` permits only `rc`, `finding_id`, `totals`, and `seats` (`tools/mori-round17-seat-regressions.py:214-216`); the gate only type-checks `duplicate_stems` when present and does not derive/compare its expected value (`:1332-1354`; the required output keys also omit it at `:1366-1369`). Thus a static mutant output with `duplicate_stems: 0`—or with the field omitted—would still satisfy this case. That fails to test A1's explicit “counted in `duplicate_stems`” behavior (`contract.md:114`), despite the current observed output being correct.

### P2 — `schema_version_unavailable` does not assert `reason: schema`

These three inputs are real schema-negative fixtures, not setup-only or empty-file cases: `absent.jsonl:1` has a valid message but no session header; `version2.jsonl:1-2` has a valid message after version 2; `late.jsonl:1-3` has a valid version-3 header and terminal message after a 5,049-byte first line (`wc -L .../SchemaVersionUnavailable/late.jsonl` → `5049`). The implementation reads at most 4096 bytes and only accepts version 3 (`tools/mori-seat-terminal.py:95-97,276-316`); its schema failure branch returns `unavailable`/`schema` (`:392-405`). Contract A1 requires that reason (`contract.md:117`). The suite also has a real supported-version control: `Completed/completed-after-error.jsonl:1-4` begins with version 3 and its expectation is `completed` (`fixtures/seat/expected.json:389-410`).

The current retained output is correct and matches the asserted `rc=0`, `MORI_SEAT_TERMINAL_OK`, all eight totals, and all three seat classes (`evidence/seat-after/runs/schema_version_unavailable.stdout:1`; expected at `fixtures/seat/expected.json:1387-1410`). The output actually gives each seat `reason: "schema"`. But the expected seats encode only class strings; `REQUIRED_SEAT_KEYS` does not require `reason` (`tools/mori-round17-seat-regressions.py:199-209`), `_validate_seat_item` only checks an optional reason is in its enum (`:1083-1089`), and `compare_want` compares only class values (`:1215-1258`). Therefore a static mutant that omitted `reason` or reported `reason: "no-message"` for these readable, message-bearing inputs while leaving class/totals unchanged would pass. This case does not enforce the A1 reason contract.

## Retained results and non-vacuity

`evidence/seat-before/run-manifest.json:1` records both cases as `capability_absent` with `observed: null`; this is not a baseline behavior result. `evidence/seat-after/run-manifest.json:1` records both as `status: "match"`, `ok: true`, `pack_changed: false`, with observed scans of 2 and 3 files respectively. The after stdout records are the retained full observations cited above.

The classes and scan outcomes are not vacuously accepted: these are regular, pinned inputs with valid message records; the duplicate case requires two path-keyed seats; the schema case requires three scanned seat rows and unavailable totals. Both want rc values are strict scan outcomes (1 and 0), not setup rc 2, and the gate checks the expected finding/totals/seats. The schema pack's absent, wrong-version, and beyond-window header variants are genuine discriminating inputs; a supported-v3 control exists in the broader fixture suite. The gap is specifically that the current case/gate does not assert the additional A1 fields described above.

Read-only recount command (no tool or selftest run):

```sh
jq -s 'map([.cases[] | select(.id == "duplicate_stems_two_entries" or .id == "schema_version_unavailable")] | {total:length, match:(map(select(.status == "match")) | length), capability_absent:(map(select(.status == "capability_absent")) | length), mismatched:(map(select(.status == "mismatch")) | length)})' \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json
```

rc=0; output:

[
  {
    "total": 2,
    "match": 0,
    "capability_absent": 2,
    "mismatched": 0
  },
  {
    "total": 2,
    "match": 2,
    "capability_absent": 0,
    "mismatched": 0
  }
]

## Verification gaps / residual risk

The `lsp` device is not mounted: `read xd://lsp` returned `No such tool: xd://lsp`. Thus no semantic references/definition/diagnostics were available; literal search was used only to locate the relevant source and the cited files were read directly, not represented as semantic proof. No build, test, selftest, or live tool run was performed. The after observations are correct for these records, but the retained green cases do not prove the duplicate counter or schema reason contract because of the two acceptance gaps above.

The read-only diff from `24526ea9617cd020fee16c28fe4d4a2789dc28cb` to measured `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7` shows the C1 tool, gate, and expected table as full-file additions (1,835, 2,529, and 1,467 lines respectively). This is consistent with the before manifests' `capability_absent` results; they do not provide a prior implementation behavior for these cases.
