# RevS226Row — scoped record audit

**Verdict: FAIL (receipt trail incomplete).** The Gate quote is present and under the limit; the M1–M6 table is structurally complete. Only M2’s specific “shown able to fail” claim is directly backed by the cited before/control receipts. M1 and M3–M6 lack receipts for their stated red-before/failure state. Evidence below is read from the named source/receipts and counter runs, not inferred from a summary report.

## Gate quote

`corpus/lessons/round-38.md:9` records S226’s URL `https://docs.python.org/3/library/os.path.html#os.path.realpath`, opened **2026-10-23**, and the quote:

> “Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path (if they are supported by the operating system).”

It is **24 words**. Reopened `corpus/evidence/sources-r38/S226.src`: the `os.path.realpath` definition begins at line 655 and this sentence is at lines **657–659**. The lesson currently locates it as `S226.src:657-658`, which omits the final word `system` on line 659; the quote itself is present and within the 25-word limit. `corpus/SOURCES.md:232` independently records the same URL and page-fetched date, 2026-10-23.

## Mistake table

`corpus/lessons/round-38.md:23-30` contains all six IDs M1–M6. Each row supplies a class, evidence, captured-by, and fix; **table completeness: PASS**.

| ID | Receipt check of “shown able to fail” / red-before | Result |
|---|---|---|
| M1 | The claimed pre-fix path without its leading dot is not shown in `evidence/c4-before.txt:6-12`; that receipt instead lists `.ufo/waves/round-37/evidence/c2-after.txt` and reports only `evidence/drift-live-r37.txt` missing (`:7`). `c4-after.txt:6-12` is the fixed C4 result, not a receipt for the path-stripping failure. | **Not backed.** No receipt for the stated pre-fix token-stripping output. |
| M2 | `evidence/v3-token-control.txt:1-12` records the round-37 counter accepting the fabricated-binding clone (`C2=met`, exit 0); `evidence/c4-witness.txt:1-13` records C4 rejecting it (`C4=unmet`, exit 1). | **Backed.** The control supplies the red/green discrimination missing from the ordinary before receipt. |
| M3 | `evidence/gate-before.txt:1-20` has no timing field. `gate-after-e37dcc6.txt:1-3` records the corrected `stale_supersede=[S069]`; `gate-after.txt:21-23` is the scored tip and has `stale_supersede=[]`. The lesson’s claimed pre-fix `stale_supersede=[]` at `e37dcc6` is not in these receipts, and its cited `gate-after.txt` does not show the stated post-fix output at that revision. | **Not backed.** The after-at-e37 receipt exists, but the claimed buggy before output does not. |
| M4 | `gate-selftest-before.txt:1-2` says `pass=8 fail=0`; `gate-selftest-after.txt:1-3` says `pass=9 fail=0`. Neither records the reported 9/9 failure or `per-id line malformed: "P-C6: …"`. | **Not backed.** The specific red-before failure has no receipt. |
| M5 | `c5-before.txt:1-10` records `CONFORM=unmet` with six checks failing on the old counters, but not the claimed `CONFORM_SELFTEST pass=2 fail=4`. `c5-after-selftest.txt:1-8` records the corrected six-mutation selftest passing. | **Not backed for this mistake.** A general conformance red state is not a receipt for the claimed non-load-bearing mutations. |
| M6 | The claimed validator rejection has no cited execution receipt. `corpus/lessons/round-37.md:44` identifies M8 as evidence hygiene, not planner-role rejection; `.ufo/waves/round-37/dispatch-log.txt:15` says planner is the L1’s canonical seat but does not record a validator rejection. | **Not backed.** No red-before/rejection receipt supports this row’s stated evidence. |

## Commands re-run

- `python3 .ufo/waves/round-38/count-c4.py f725f3076972e6e70595b5ac8279be524a111ff8` → `C4=met`; all four content checks pass and all three witnesses are rejected. Matches `evidence/c4-after.txt:1-12`.
- `python3 .ufo/waves/round-38/count-c4.py e37dcc6` → `C4=unmet`; anchors fail and the mixed-base live-receipt path is missing. The printed path includes `.ufo/`, so this does not reproduce M1’s claimed stripped-dot line. Matches `evidence/c4-before.txt:1-12`.
- `python3 .ufo/waves/round-37/count-c2.py d2ee0532b716b963623fb421aaa571c54c754aad --repo .ufo/waves/round-38/scratch/ExecWitnessSandbox/fabricated-binding` → `C2=met`.
- `python3 .ufo/waves/round-38/count-c4.py d2ee0532b716b963623fb421aaa571c54c754aad --repo .ufo/waves/round-38/scratch/ExecWitnessSandbox/fabricated-binding` → `C4=unmet`.
- `python3 tools/mori-sources-appendonly.py e37dcc6 --round-base f10a320d` → timing line has `stale_supersede=[S069]`; `python3 tools/mori-sources-appendonly.py f725f3076972e6e70595b5ac8279be524a111ff8 --round-base f10a320d` → `stale_supersede=[]`. Both runs also report 18 append-only violations and exit 1; timing output is not an overall gate pass. Corresponding receipts: `gate-after-e37dcc6.txt:1-3`, `gate-after.txt:1-23`.
- `python3 tools/mori-sources-appendonly.py --selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=9 fail=0`.
- `python3 .ufo/waves/round-38/conform.py f725f3076972e6e70595b5ac8279be524a111ff8 --selftest --counter .ufo/waves/round-38/count-c1.py` → `CONFORM_SELFTEST pass=6 fail=0`.

## Surfaces, bounds, and provenance

Read-only surfaces inspected: `corpus/lessons/round-38.md`, `corpus/evidence/sources-r38/S226.src`, `corpus/SOURCES.md`, and the cited round-38/round-37 receipts. No product, gate, counter, configuration, or source file was edited; no tool was installed. No subagent was dispatched (leaf-member bound). Full C1–C3 round acceptance and unrelated round work are out of scope; the commands above are the only checks reported as run. This report is the sole authored artifact.

Report: .ufo/waves/round-38/w2/RevS226Row.md
