# Mo54RevNoHarm — round 54 w1 no-harm audit

Seat: Mo54RevNoHarm (leaf, read-only audit). Comparison: entering tip `39dcf4d7e410d362781a47e8365ca23b5c807598` to data commit `78295c764093ff1f6cee08d7246679900bde7265`. The frozen contract was read first from `.ufo/waves/round-54/contract.md`. The requested diff stat is 50 files, +17,871/-4; the four deletions are relocations: seven round-28 stray files and `0` from round 38 move beneath their respective `misroot-lane-root/` directories (R100); all other changes are additions except `corpus/SOURCES.md`.

LSP protocol: no `lsp` command or `xd://lsp` device is mounted/available (the tool registry lists no LSP; `read xd://lsp` returned “No such tool”). Thus caller/pointer checks below are literal text/corpus checks, not semantic LSP proof.

## Axes

| Axis | Verdict | Evidence / scope |
|---|---|---|
| Coverage | Not harmed | New memory-failure entry adds a kill class outside the OOM path and the README coverage map links it; the C1 ledger and README identify the bounded scope of 31 claim-table rows. `corpus/README.md:775-784`, `PROVINCE.md:464-475`. No deleted live entry or source row observed. |
| Operability | Not harmed | No tool or instrument was changed in the committed diff; an independent in-wave pin check reports 47 pins, 37 tally/8 digest, all match, no dropped/rebound/hidden/stale pins and same pin set at entering and data rev (`Mo54ExecPinCheckNoHarm.md:25-49, 52-68, 140-200`). The counter receipts at data explicitly remain unmet only because votes had not yet landed (`evidence/c1-at-data.txt`, `c2-at-data.txt`, contract lines 39-47, 80-93). |
| Depth | Not harmed | The memory-failure entry covers SIGBUS/SIGKILL, recovery outcome, per-node counters, HardwareCorrupted, sysctls and tracepoint; it explicitly limits itself to source-derived detection knowledge and prohibits injection/writes (`memory-failure-kills-r54.md:11-19, 47-86`). Its structured-counter-vs-text distinction honors QUALITY 15 (`:49-60`). |
| Freshness | Not harmed | The C1 ledger has 31 one-per-hash rows and v7.3 source/line/quote/disposition columns; the corpus data audit reports line/quote claims agree and all moves table rows validated (`Mo54RevLedgerProse.md:9-26`). SOURCES rows S515-S524 and used-by references exist (`corpus/SOURCES.md:294-303`). |
| Calibration | Not harmed | Entry explicitly distinguishes signal from death, outcome from kill, poison counters from process counts, and source claims from live observations; host version and zero values are qualified (`memory-failure-kills-r54.md:53-74, 76-86`). |
| Adjacency | Not harmed | The new knowledge rows are cross-linked from README, PROVINCE, SKILL and SOURCES. The release-drift leads remain leads, not expanded claims (`corpus/README.md:775-784`, `PROVINCE.md:464-476`, `SKILL.md:1213-1244`, `SOURCES.md:364-369`). |

## Relocation and pointers

The round-54 contract names all eight moved paths at lines 113-117. The D3 receipt records each source/destination SHA and `cmp=ok` (`.ufo/waves/round-54/evidence/d3-relocation.txt`). A scoped literal search of round-28 and round-38 found no live references to `misroot-lane-root`; historical reports and the original hash-check script are expected to retain the historical path/content names. The separate pin audit found the moved blobs byte-identical at their new paths and no instrument/tool reader of the old lane-root paths (`Mo54ExecPinCheckNoHarm.md:140-200`). `corpus/SOURCES.md` changes add used-by links and source rows, not pointers to lane-root copies (same report :197-200).

Potential prose precision concern: `kernel-v7.3-recheck-r54.md:63` says anchors “that `oom-memcg-stat-r50.md` and its rows S490/S491 give in prose”; the dedicated prose review found the cited anchors are in SOURCES rows, not in the entry prose, and that the statement also overgeneralizes the shift to S491's unchanged `oom_kill.c` anchors (`Mo54RevLedgerProse.md:30-32`). This is a factual wording/precision issue rather than damage to the underlying row evidence or any of the six axes. Reported for integration consideration; no edit made.

## Residual risk and verification gaps

- Wave was in flight; C1/C2 votes and settled-wave results are outside the data commit examined here. No verdict on final predicate outcome is made.
- No LSP available, so cross-file reference checks are literal searches and cited in-wave reports, not semantic references/definition results.
- The independent pin audit did not run every live collection instrument; its stated limit is selftest pins plus inspected instruments/tools (`Mo54ExecPinCheckNoHarm.md:202-212`).
- Audit did not independently re-fetch upstream source copies; freshness and source-row verification relies on the cited v7.3 data audits and corpus evidence.

## Findings

- LOW — `corpus/knowledge/kernel-v7.3-recheck-r54.md:63`: prose misattributes where S490/S491 anchors are recorded and implies all cited anchors moved; S491's `oom_kill.c` lines remain at the same positions. See `Mo54RevLedgerProse.md:30-32`. No broader axis harm observed.