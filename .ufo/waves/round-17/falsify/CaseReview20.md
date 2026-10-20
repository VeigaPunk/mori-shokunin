# CaseReview20 — C1 TailBoundary / NonJsonlIgnored

## Verdict

The assigned cases’ current class expectations are source-supported and the retained L1 after-results match every asserted field. `non_jsonl_files_ignored` has effective negative controls. I found two coverage-contract defects: the TailBoundary “A1 default” case accepts the old default, and the current cases/gate cannot express the additional independent metadata wants required by Amendment A2.

## Findings (severity order)

### P2 — `tail_a1_default_window` does not distinguish the A1 default from the old 262144-byte default

Amendment A1 requires default `--max-tail-bytes 524288` (`.ufo/waves/round-17/contract.md:116`); the implementation currently has that value (`tools/mori-seat-terminal.py:98`, used by argparse at `:1761-1765`). But `expected.json:1046-1068` invokes the case without `--max-tail-bytes` and expects all three seats completed. A static mutant changing only the default back to 262144 still satisfies this case:

- `TailBoundary/tail-far.jsonl` is 12,765 bytes, with its v3 header and completed message at lines 1-2; 262144 reads the entire file.
- `tail-partial.jsonl` is 6,186 bytes and its completed message is line 3; 262144 reads the entire file.
- `tail-near.jsonl` is 482,025 bytes, but its completed message is the final 104-byte line 3002. Under 262144 the tail begins at byte 219,881; that final message remains in the tail. Its v3 header is line 1.

Read-only `stat -c '%s %n'` over TailBoundary returned 12765 / 482025 / 6186 bytes for far / near / partial. A static byte-window calculation (not an invocation of the tool) produced:

```
window=64 tail-far.jsonl:unavailable tail-near.jsonl:unavailable tail-partial.jsonl:unavailable
window=1000 tail-far.jsonl:unavailable tail-near.jsonl:completed tail-partial.jsonl:completed
window=262144 tail-far.jsonl:completed tail-near.jsonl:completed tail-partial.jsonl:completed
window=524288 tail-far.jsonl:completed tail-near.jsonl:completed tail-partial.jsonl:completed
```

This is also exposed by the sibling case: `expected.json:988-1014` explicitly passes the pre-A1 value 262144 and pins the *same* three completed classes. The 1000-byte and 64-byte cases (`:959-985`, `:1017-1043`) are real small-window negative controls, but they do not distinguish 262144 from 524288. Thus the observed L1 `match` for the default case does not establish the A1 default change; a default=262144 mutant is accepted. A discriminating fixture needs a message/terminal outcome inside the extra range available at 524288 but absent after truncation at 262144.

### P2 — Assigned C1 wants do not implement current Amendment A2 metadata assertions

Amendment A2 says C1 fixture expectations gain independent `want.reason`, `want.records`, and `want.top` assertions (`contract.md:142-144`). Both assigned `want` objects still contain only `rc`, `finding_id`, `totals`, and `seats` (`expected.json:1046-1070`, `:1073-1095`). The gate allows only those four keys (`tools/mori-round17-seat-regressions.py:214-216`) and rejects any other want key (`:639-645`), so these A2 assertions cannot currently be expressed.

Static counterexample for `non_jsonl_files_ignored`: `good.jsonl:1-2` has no `provider` or `model`, and the retained output correctly reports both null and `reason:null` (`evidence/seat-after/runs/non_jsonl_files_ignored.stdout:1`). A mutant can instead return `reason:"schema"` for this still-completed seat. `schema` is an allowed reason (`mori-round17-seat-regressions.py:191`); the seat validator only checks that the reason is in that enum (`:1087-1090`), while `compare_want` compares seat classes, not reason/record metadata (`:1215-1260`). With class/totals unchanged, this case has no independent want that rejects the wrong reason. Likewise, output record metadata is only shape-checked (e.g. provider/model may be any string or null at `:1053-1055`), and the current want has no `records` field. This is a concrete A2 contract/evidence gap, not a claim that the observed L1 output is wrong.

## Case checks that passed

- `tail_a1_default_window` values are independently derivable from its fixture bytes: all headers are version 3; each last message is `role=assistant`, `stopReason=stop`; therefore each class is `completed`, all other declared totals are zero, and no dead seat implies rc 0 / `MORI_SEAT_TERMINAL_OK`. The pinned `--now-ms` is present. The L1 after stdout contains exactly the three expected completed rows, totals, `files_scanned=3`, and consistent scan metadata (`evidence/seat-after/runs/tail_a1_default_window.stdout:1`).
- `non_jsonl_files_ignored` is source-supported: `good.jsonl:1-2` is a v3 transcript with an assistant stop; the expected one-completed-seat want is at `expected.json:1073-1095`. The decoys `UPPER.JSONL`, `data.jsonl.bak`, `other.json`, `notes.txt`, and `Fake.jsonl/inner.txt` each contain a v3 header and an error message with `errorStatus=429`, `rate_limit`, and `completedAt=1760998000000` (their lines 1-2). Relative to pinned now 1761000000000, that error is 2000 seconds old, beyond the 900-second settle window, so wrongly ingesting any decoy would add a `dead_rate_limit` seat and flip rc. `Fake.jsonl` is a directory, not a transcript file. The tool walks filenames ending case-sensitively in `.jsonl`, lstat-checks regular files, and uses `followlinks=False` (`tools/mori-seat-terminal.py:420-433`).
- The gate’s own `fixture_scan_bounds` counts only regular non-symlink `*.jsonl` files (`mori-round17-seat-regressions.py:778-800`); its strict no-prefix `files_scanned`/row-count check is at `:1428-1436`, and `compare_want` rejects any extra seat (`:1249-1260`). Thus this pack is not an inert extension-only control: any of the four regular decoys parsed as a seat is observable and fails the exact want.
- L1 after retained outputs and manifest agree: tail case `rc=0`, OK finding, completed=3, 3 seats; non-JSONL case `rc=0`, OK finding, completed=1, 1 seat; both run-manifest entries are `status=match`, `reasons=[]`, and unchanged pack hashes (`evidence/seat-after/run-manifest.json:1`). The retained `runs/*.stdout:1` JSON also confirms every actual seat class and all totals. Before-manifest records both cases as `capability_absent`, not as an observed mismatch (`evidence/seat-before/run-manifest.json:1`).

## Required count and verification limits

Read-only command (selecting only the two requested IDs) returned rc 0:

```
expected_count=2 ids=non_jsonl_files_ignored,tail_a1_default_window
before_count=2 ids=non_jsonl_files_ignored,tail_a1_default_window
before_statuses=tail_a1_default_window:capability_absent,non_jsonl_files_ignored:capability_absent
after_count=2 ids=non_jsonl_files_ignored,tail_a1_default_window
after_statuses=tail_a1_default_window:match,non_jsonl_files_ignored:match
command_rc=0
```

No tool invocation or selftest was run. The Python work was read-only fixture-byte parsing/window arithmetic and the manifest count above. No `lsp` device is mounted: `read xd://lsp` returned “No such tool”; therefore references/definition/diagnostics were unavailable, and conclusions here use direct source/fixture reads (grep was used only to locate symbols). No tools were installed or updated.

Report: `.ufo/waves/round-17/falsify/CaseReview20.md`
