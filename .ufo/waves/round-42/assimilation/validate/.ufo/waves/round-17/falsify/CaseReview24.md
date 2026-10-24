# CaseReview24 — C1 code-priority cases

## Verdict

**Scoped pass; no actionable falsifier found** for `code_quota_1308_beats_429` and `code_rate_1302_beats_quota_token`. This is not a blanket C1 or lane pass. No tool or selftest was run; the assessment uses the static contract/code/fixture review and retained L1 outputs.

## Evidence

- Contract A1 says codes `1113`/`1308` mean usage/balance and `1302` means rate limit, with code checks before token checks (`contract.md:123`). The independently opened S043 source receipt records the underlying official Z.AI table: `1302 / 429 / Rate limit reached for requests` and `1308 / 429 / Usage limit reached for ...` (`.ufo/waves/round-17/build/SrcZaiErrorCodes.md:16-18`). Thus the expected classes are supported independently of the classifier's hard-coded sets.
- The synthetic bytes are distinct counterexamples to generic-token precedence and match the fixture pins: `CodeQuota1308/code-1308.jsonl` has `errorStatus:429`, `(type=1308)`, and “insufficient balance” (no quota token); `CodeRate1302QuotaWord/code-1302-quota.jsonl` has `errorStatus:429`, `(type=1302)`, and “quota exceeded” (`.../fixtures/seat/CodeQuota1308/code-1308.jsonl:2`; `.../fixtures/seat/CodeRate1302QuotaWord/code-1302-quota.jsonl:2`). `sha256sum` rc0: `c9517ccff713adfeeb434847f3e1bbf977bfc253550a777d8e74c785dda643b7` and `9e9ca057cd448b360210e9be71fc0b843b9cadfab9a29edd3247c3259358c30d`; these equal the `expected.json` pins at lines 7-8.
- Both want records pin `--now-ms 1761000000000`, rc 1 / `MORI_SEAT_TERMINAL_DEAD`, all eight class totals, and a nonempty one-seat class map (`expected.json:1261-1307`). The selected terminal timestamp is `1760998000000`, older than the default 900-second settle window. The 1308 case expects exactly one `dead_quota`; the 1302 case expects exactly one `dead_rate_limit`.
- The current classifier checks the quota-code set, then rate-code set, before text tokens and HTTP 429 fallback (`tools/mori-seat-terminal.py:86-88,247-273`). This makes both negative controls effective: without the 1308 code override its 429 would classify as rate-limit; without the 1302 code override its quota text would classify as quota. The code precedence yields the documented meanings.
- The gate does not accept these as empty/vacuous class assertions: for rc 0/1 it requires totals and seats, derives the totals from the seat map, rejects rc1 without a dead seat, and checks the declared values against every output total and seat class; it also rejects unexpected output seats (`tools/mori-round17-seat-regressions.py:657-678,1215-1260,1364-1448`). The two wants explicitly supply every class count and one expected seat. They expect DEAD, not SETUP; a wrong rc/finding is rejected (`.../tools/mori-round17-seat-regressions.py:1274-1313`). Capability-absent is separately recorded as failure/rc1, not green (`.../tools/mori-round17-seat-regressions.py:1697-1707`).
- Retained L1 result: before, both rows have `status: capability_absent`, `ok: false`, and `observed: null`; this is not a prior implementation behavior comparison. After, both are `status: match`, `ok: true`; full stdout at `evidence/seat-after/runs/code_quota_1308_beats_429.stdout:1` and `.../code_rate_1302_beats_quota_token.stdout:1` matches rc/finding/totals and the single expected seat class. The retained manifest observations also show `files_scanned:1`, `seat_count:1`, and the pinned `now_ms` (`evidence/seat-before/run-manifest.json:1`; `evidence/seat-after/run-manifest.json:1`).

## Requested read-only count

Command (jq only reads the two retained manifests):

```sh
jq -s '[.[] | [.cases[] | select(.id == "code_quota_1308_beats_429" or .id == "code_rate_1302_beats_quota_token")] | {count: length, cases: map({id, status, ok})}]' \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json
```

rc 0; output:

```json
[
  {"count":2,"cases":[
    {"id":"code_quota_1308_beats_429","status":"capability_absent","ok":false},
    {"id":"code_rate_1302_beats_quota_token","status":"capability_absent","ok":false}
  ]},
  {"count":2,"cases":[
    {"id":"code_quota_1308_beats_429","status":"match","ok":true},
    {"id":"code_rate_1302_beats_quota_token","status":"match","ok":true}
  ]}
]
```

## Residual risk and verification gap

- S043 documents the numeric business codes and HTTP status, but explicitly does **not** document the transcript token syntax `(type=NNNN)`; it labels linking that token to a transcript as `[INFERENCE]` (`build/SrcZaiErrorCodes.md:35`). These fixtures verify the contract's synthetic token parser, not that real OMP transcripts use that representation.
- LSP was unavailable: `read xd://lsp` returned “No such tool” and listed mounted devices without `lsp`. I therefore used targeted path/line reads and literal grep only; no semantic LSP references/definition/diagnostics were available.