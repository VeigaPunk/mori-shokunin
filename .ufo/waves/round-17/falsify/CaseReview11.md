# Round 17 C1 review — unavailable cases

## Verdict

No actionable falsifier found for the requested C1 class/setup assertions in `unavailable_empty_file` and `unavailable_malformed_and_shape`. This is limited to these two cases; it is not a blanket C1 or wave-closure pass.

## Evidence

- The scoped committed diff from entering tip `24526ea9617cd020fee16c28fe4d4a2789dc28cb` to measured tip `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7` adds the expected table, terminal tool, and regression gate; the scoped files are new additions. No existing C1 callers were changed in this range.
- Inputs/expected values are independently pinned. `expected.json:80-81` pins the empty-file bytes to the SHA-256 of empty content and pins the 121-byte malformed fixture; the whole expected table is separately pinned by `PINNED_INPUTS.json:13`. The after receipt records 81 verified fixture pins, with no missing, extra, or mismatched inputs (`evidence/seat-after/run-manifest.json:1`).
- The expectations are source-supported. The empty file has no session header, so `_header_ok` rejects it and `_analyze` returns `unavailable/schema` (`tools/mori-seat-terminal.py:302-316,392-405`); A1 requires absent/unsupported schema to be unavailable (`contract.md:117`). The malformed fixture begins with a valid version-3 session header and then contains malformed JSON, non-object JSON, and message records with invalid/missing message shapes; those records are skipped and produce no selected message (`tools/mori-seat-terminal.py:207-220,302-316,354-405`; `contract.md:45-46,116`).
- Both independent expected cases assert `rc:0`, `MORI_SEAT_TERMINAL_OK`, all eight class totals, and exactly one named unavailable seat (`fixtures/seat/expected.json:590-637`). The retained after stdout shows the corresponding seat key/class, one unavailable total, no other classes, matching `now_ms`, and the expected subreason (`evidence/seat-after/runs/unavailable_empty_file.stdout:1` and `.../unavailable_malformed_and_shape.stdout:1`). The retained after manifest marks both `match`, `ok:true`, `reasons:[]`, and reports rc 0 (`evidence/seat-after/run-manifest.json:1`).
- Neither class nor setup is vacuously accepted: the gate compares rc/finding against the wanted values (`tools/mori-round17-seat-regressions.py:1274-1313`), requires the full strict result shape and validates totals (`:1364-1378`), cross-checks derived totals and declared wants (`:1399-1448`), and compares named seat classes while rejecting missing/extra seats (`:1215-1259`). An rc-2 setup result cannot satisfy these rc-0 cases.
- Negative controls are concrete and retained. `EmptyDir/README.txt:1` says there are no `*.jsonl` files; its expected case wants zero seats/unavailable (`fixtures/seat/expected.json:695-`), and the after receipt matches with `files_scanned:0` (`evidence/seat-after/run-manifest.json:1`). The separate `MalformedLineSkip/malformed-then-completed.jsonl` fixture contains parse noise followed by a valid assistant-stop message; its expected case requires completed=1/unavailable=0 (`fixtures/seat/expected.json:1414-`), and the after receipt matches (`evidence/seat-after/run-manifest.json:1`). These distinguish an empty directory from a zero-byte transcript, and malformed noise from a stream with a valid terminal message.

## Retained before/after count

Read-only count command (no tool or selftest run):

```sh
jq -s 'map([.cases[] | select(.id == "unavailable_empty_file" or .id == "unavailable_malformed_and_shape")]) | map({case_count:length, matched:([.[] | select(.status=="match")] | length), mismatched:([.[] | select(.status=="mismatch")] | length), capability_absent:([.[] | select(.status=="capability_absent")] | length)})' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-before/run-manifest.json /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/seat-after/run-manifest.json
```

rc=0; stdout:

```json
[
  {"case_count":2,"matched":0,"mismatched":0,"capability_absent":2},
  {"case_count":2,"matched":2,"mismatched":0,"capability_absent":0}
]
```

The before receipt is capability-absent for both cases, not a prior behavioral classification; the after receipt matches both. The retained aggregate receipt independently records C1 `[54,0]`, rc 0 (`evidence/count-c1.json:16-19`).

## Residual risk and verification gaps

- `want` pins class, not the diagnostic `reason`; the gate only checks that a reason is among the allowed values (`tools/mori-round17-seat-regressions.py:1087-1089`), and `compare_want` compares the class (`:1238-1258`). Thus the receipts show the correct `schema` and `no-message` reasons, but the two expected cases do not regression-pin that distinction. This does not undermine the requested unavailable-class or setup assertions.
- LSP is unavailable in this environment: `read xd://lsp` returned “No such tool” and the mounted-device list contained no LSP device. I used literal grep only to locate code/receipt lines and did not treat it as semantic proof; the cited behavior was checked in the source ranges above.
- Per wave context, I did not run the terminal tool, gate, or any selftest. I inadvertently opened the synthetic `UnavailableNonMessage/non-message-only.jsonl` control, which contains a `credential_pin`-typed record; I do not reproduce its payload. This was contrary to `wave1-context.txt:9` and is disclosed here.

Report: `.ufo/waves/round-17/falsify/CaseReview11.md`
