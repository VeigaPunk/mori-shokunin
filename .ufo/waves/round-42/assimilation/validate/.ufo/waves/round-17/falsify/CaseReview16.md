# CaseReview16 — C1 prefix-filter cases

## Verdict

No actionable falsifier found in the assigned cases `prefix_filter_tsukuroi` and `prefix_filter_souji` in `PrefixAttribution`. This is limited to these two cases; it is not a blanket C1 or round-17 pass.

## Findings

None in scope.

## Evidence

### Independent expectations and input bytes

The expectations are literal case data in `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat/expected.json:829-883`; the gate loads these specs and separately compares subprocess output (`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round17-seat-regressions.py:1598-1601,1737-1747`). The same file pins each fixture byte stream (`:47-53`).

- `TsukuroiR17.X` is a v3 assistant `stop` record; `TsukuroiR17.Y` is a v3 assistant error with `completedAt=1760998000000`, HTTP 429 and `429 rate_limit` (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat/PrefixAttribution/TsukuroiR17.X.jsonl:1-2` and `.../TsukuroiR17.Y.jsonl:1-2`). With pinned `now_ms=1761000000000`, the error is 2,000 seconds old, beyond the contract's 900-second default settle window. Contract rules classify `stop` as completed and the older non-quota 429/rate-limit error as dead_rate_limit (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/contract.md:48-54,112-115`). Thus the two nonzero expected classes and zeroes for the remaining classes are supported.
- `SoujiR17-3.W` is a v3 assistant `stop`; `SoujiR17-3.Z` is a v3 assistant error with `completedAt=1760998000000` and `quota exceeded` (`.../SoujiR17-3.W.jsonl:1-2` and `.../SoujiR17-3.Z.jsonl:1-2`). It is likewise 2,000 seconds old. The contract's quota-token-first rule supports dead_quota, and the stop record supports completed (`contract.md:48-54,112-115`).
- The near-prefix controls are substantive regular transcript fixtures, not empty placeholders: `TsukuroiR17Extra.Xtrap` is completed, `SoujiR17-30.Trap` and `KumitateR17-2.Q` are aborted (`.../TsukuroiR17Extra.Xtrap.jsonl:1-2`, `.../SoujiR17-30.Trap.jsonl:1-2`, `.../KumitateR17-2.Q.jsonl:1-2`). They therefore detect prefix overmatching: exact `prefix` is the stem before the first dot, and the implementation tests membership equality (`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-seat-terminal.py:445-451`), not `startswith`.

### Classifier, comparator, and retained observations

The implementation applies the settle check before the quota/rate/error classification and emits a dead finding for any dead seat (`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-seat-terminal.py:247-273,460-502`). The gate requires exact rc, finding ID, schema, class totals, and the expected seat classes; for these `want.rc=1` cases it is strict and rejects missing or unexpected seat rows (`/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round17-seat-regressions.py:1215-1260,1274-1313,1360-1448`). Each expected totals object enumerates every class, with one completed and one dead seat, so neither an all-zero class table nor an rc2/setup result can satisfy these expectations.

Retained L1 before-case entries show both target cases as `capability_absent`, `observed=null`, `ok=false`—the missing-tool baseline, not a production defect (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json:1`). After-case entries show `status=match`, `ok=true`, `reasons=[]`, rc 1, `MORI_SEAT_TERMINAL_DEAD`, `files_scanned=2`, `seat_count=2`, and the expected totals for each (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json:1`). The retained stdout rows independently show the exact returned seat keys/classes, not just the manifest's projected summary: Tsukuroi has only `TsukuroiR17.X=completed` and `TsukuroiR17.Y=dead_rate_limit` (`.../evidence/seat-after/runs/prefix_filter_tsukuroi.stdout:1`); Souji has only `SoujiR17-3.W=completed` and `SoujiR17-3.Z=dead_quota` (`.../evidence/seat-after/runs/prefix_filter_souji.stdout:1`). Each stdout reports the pinned now, settle 900, scanned two, and all eight totals. The retained manifests also show identical before/after pack digests and `pack_changed=false` for both cases.

L1's retained aggregate count receipt records rc 0 and `[54,0]` for the original capability-absent and delivered mismatch counts (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/count-c1.json:5-20`). This aggregate is consistent with, but does not replace, the two case-level observations above.

### Requested read-only case count

Re-ran a read-only jq count over just these two case IDs in each retained manifest (no tool or selftest was run):

```sh
jq -s 'map({case_ids: ([.cases[] | select(.id == "prefix_filter_tsukuroi" or .id == "prefix_filter_souji") | .id] | sort), total: ([.cases[] | select(.id == "prefix_filter_tsukuroi" or .id == "prefix_filter_souji")] | length), matched: ([.cases[] | select((.id == "prefix_filter_tsukuroi" or .id == "prefix_filter_souji") and .status == "match")] | length), capability_absent: ([.cases[] | select((.id == "prefix_filter_tsukuroi" or .id == "prefix_filter_souji") and .status == "capability_absent")] | length), mismatched: ([.cases[] | select((.id == "prefix_filter_tsukuroi" or .id == "prefix_filter_souji") and .status == "mismatch")] | length)})' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json
```

rc=0; stdout:

```json
[
  {"case_ids":["prefix_filter_souji","prefix_filter_tsukuroi"],"total":2,"matched":0,"capability_absent":2,"mismatched":0},
  {"case_ids":["prefix_filter_souji","prefix_filter_tsukuroi"],"total":2,"matched":2,"capability_absent":0,"mismatched":0}
]
```

## Residual risk and verification gaps

- No live tool or selftest execution was performed, per assignment. This review relies on static source/fixture inspection and retained L1 outputs.
- The `lsp` device is unavailable in this environment: the initial `read xd://lsp` returned `No such tool: xd://lsp`. Text search was used only to locate expected-case IDs; it is not semantic proof. Findings above use the directly read source, contract, fixtures, and retained output.
- No tools were installed or updated.
