# ReviewSkill: round-20 section of SKILL.md vs tools/mori-wave-settlement.py

VERDICT: PARTIAL. Commands, flags and the enumerated states match the tool. Several claims do not hold as written: zero-discovery and crash exit codes, the "no dead/failed/killed words in output" rule, two preconditions the tool or census cannot measure, and the pin overwrite/reason guidance. The runbook also omits the scan receipt that QUALITY criterion 64 requires.

## Scope, versions, bounds
- Claim under test: SKILL.md `## Wave settlement scan and drift re-pin (r20)` (L471-500) is executable without oral context; its exit map matches tools/mori-wave-settlement.py; it claims nothing the tool does not implement.
- Reviewed snapshot (copies in /tmp/ReviewSkill/snap, taken 11:11Z):
  - tools/mori-wave-settlement.py sha256 203c716e1dc55fa6ac912335e15516c63a46d4d4bc7f6cd9554a2e45212061a9 (690 lines)
  - SKILL.md sha256 f0d5dcbf41523474... (round-20 section at the same lines, L471-500)
  - tools/mori-census.sh sha256 87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28 (unchanged since 2026-10-20 17:39)
  - corpus/knowledge/wave-settlement-r20.md sha256 0c4a2aa23efb385b55ee...
- Files changed during this review: tool 682 -> 689 -> 690 lines; SKILL L498 S067 -> S076; knowledge doc "7 refinement" -> "8" (L22), zero-wave caveat added (L69-72); tool docstring 64 -> 16 bytes (L10) and R6/R7 now listed (L16). Findings below are against the snapshot.
- Method: full read of the tool; fixture probes under /tmp/ReviewSkill (fx, fx2, fx-unreadable2); selftest; one guarded read-only live scan (`--out` to /tmp); census usage paths only; named files and `.ufo/waves` only.
- Bounds: no live census run (not authorized for this item); no reads under .ufo/interactive-sessions, .ufo/worktrees, .jj or ~/.omp. The guard found one lexically unsafe `../../` trailer in a sibling probe fixture; the tool rejects it before any stat. No lane edits, no installs or updates, no subagents.
- Tools used, already present, nothing installed: python3 3.14.8, bash, /usr/bin/jq 1.8.2, jaq 3.1.1 (~/.local/bin/jq).

## Verified HOLDS
1. Flags exist: `scan --lane-root --fleet-root --out` (tool L651-658). Census `--drift <path>`, `--pin <path>`, `--help` exist (census L397, L4722-4724). `bash tools/mori-census.sh --drift` -> "requires a baseline path", rc 2; same for `--pin`.
2. `python3 tools/mori-wave-settlement.py --selftest` -> `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (22 cases, 22 passed, 0 failed)`, rc 0 (14 frozen + 8 refinement).
3. Schema `mori-wave-settlement-v1` (tool L32). Two runs byte-identical; `--out` bytes equal stdout (fixture T15; live scan).
4. State -> exit mapping for every state the SKILL names: settled/no-spawn -> 0; partial/unsettled/unavailable -> 1 (L367; T6, T10-T14).
5. `unreadable_json > 0` with rc 0 occurs (T3), so the L487 warning is accurate.
6. Stub read bound is size <= 16 (L230); stub content is never emitted (oracle case `content-not-emitted`).
7. `unsafe` for absolute or `..` trailers is decided before any stat (L156-164, L219-221; oracle `traversal`, `absolute-path`; R7 case).
8. `unparsed` = no trailer (L209-217); `empty` = size 0 (L228-229); `misrooted` only with `--fleet-root` (L234-237; T12).
9. Census SHA: `sha256sum tools/mori-census.sh` = 87b8d680...ab28 = SKILL L493 = contract L19, L47.
10. Census writes: `--pin` writes only its path (census L2932); `--drift` writes nothing. Grep of `>`, `>>`, tee, mktemp, mkdir, touch, cp, mv: every other hit is in run_selftest (from L3006). [grep-verified]
11. Drift classes (SKILL L495) equal the contract closed set (contract L26).
12. Comm recipe runs: bare jq and /usr/bin/jq both return 50 for `.tokens|keys[]` on corpus/evidence/drift-classification-r20.json.
13. Named files exist: both knowledge docs, baseline-r10-20261015T2231Z.json, drift-classification-r20.json, QUALITY criteria 64-67, contract, frozen/c2-expected.json. S076 is defined at corpus/lessons/round-20.md:50, so the L498 citation resolves.
14. The scan is read-only apart from `--out` (tool L677-684).

## Findings (severity order)

### H1. Exit 0 when nothing is discovered; SKILL states no caveat (tool L367; SKILL L487)
- Tool: `rc = 0 if all(...)` is vacuously true for `waves: []`. Discovery drops are silent: `_wave_root` returns None for absent or symlinked `.ufo`/`.ufo/waves` (L82-83, L87-88, L91-92); `_dispatch_files` skips symlinked or non-regular `*.json` (L121-122) and lstat-failed `.json` entries (L113-115); suffix match is case-sensitive (L121); `unreadable_json` counts only read/parse failures (L324-333).
- Fixture results (snapshot): `.ufo/waves` absent -> rc 0, waves []. `.ufo/waves` symlink to a dir holding an unsettled wave -> rc 0, waves []. Only a malformed dispatch -> rc 0, unreadable_json 1. Dispatch JSON as symlink -> rc 0, ignored 0, unreadable 0. `DISPATCH.JSON` -> rc 0, waves [].
- SKILL L487 says "0 all discovered waves settled or no-spawn" with no zero-discovery caveat. The knowledge doc now carries it (wave-settlement-r20.md:69-72: "read `totals.waves` before trusting exit 0"). The frozen oracle has no zero-wave case.
- Remedy: exit 2 when no dispatch file is discovered or the waves root is a symlink; count symlinked and uppercase JSON as unreadable; SKILL: require `totals.waves >= 1`.

### H2. The exit code is lane-wide and recursive; the SKILL gives no scoping (tool L96-126, L367, L651-658)
- Discovery walks all of `.ufo/waves/**`; rc aggregates every dispatch-schema file; the CLI has no wave or round selector.
- Live scan 11:13:29Z, snapshot tool, `scan --lane-root /home/vgpnk/Projects/shokunin/mori-shokunin --out /tmp/ReviewSkill/live-scan-final.json`: rc 1; 14 waves; states settled 8, partial 4, unsettled 1, no-spawn 1.
  - Not settled: round-18/wave1-dispatch.json (15 missing); round-19/wave1-run.json (48 missing); round-19/wave2-run.json (22 missing); round-20/wave2-run.json (present 42, stub 25); round-20/falsify/SentinelTool/probe-20261021/lane/.ufo/waves/round-1/dispatch.json (unsettled, unsafe 1); round-20/falsify/SentinelTool/probe-20261021/outside/secret.json (no-spawn).
  - round-20/wave1-run.json is settled.
- Consequence: rc cannot reach 0 while the r18/r19 partials or the sibling probe files sit under `.ufo/waves`. The round-20 answer must come from `waves[]` selected by `dispatch_path`. SKILL L477/L487 imply a per-wave closure check and never say so. The knowledge doc reports historical waves (L86-89) but not the rc consequence.
- Remedy: add a `--wave` or round selector, or state in the SKILL that rc is lane-wide. Keep probe and scratch JSON out of `.ufo/waves` or exclude `falsify/`.

### H3. The receipt required by QUALITY criterion 64 is absent; the tool cannot emit scan time (QUALITY.md:227-233; SKILL L475; tool L359-366)
- Criterion 64 requires a committed receipt (scan time, dispatch path and sha256, present/stub/missing counts) before a round reports a wave's settlement; "no receipt" fails.
- SKILL L475 says only "before any closure note that says a wave settled".
- Payload keys are schema, lane_root, waves, totals, ignored_json, unreadable_json, with no time (deliberate, for byte-identity; T15). Knowledge L77 says "cite the scan time" with no mechanism.
- Remedy: add a receipt step to the SKILL (`date -u`, `--out`, commit with the listed fields) or write time in a sidecar.

### M1. "The output must not contain those words" is false (SKILL L489)
- The tool echoes dispatch-controlled strings: member name and agent (L264-265, L276), wave (L297), lane_root (L361).
- Fixture T9: member named `dead-seat` -> stdout contains `dead` twice (state partial; missing ["dead-seat"]).
- Oracle `no_vocab` (c2-expected.json case 20; tool L595-604) checks one fixture only. Knowledge L73 already limits the guarantee to the tool's own state words; the SKILL does not.

### M2. Two SKILL preconditions cannot be executed as written (SKILL L477, L481)
- L477 "after the census `SURFACE waves` age shows no recent writes": census `probe_waves` (census L865-932) emits total/settled/unsettled/aged_unsettled/empty/age_unreadable/threshold_s and `ts=` (L931). No age or newest-write field. Per-wave age appears only in WAVE_UNSETTLED_AGE findings for unsettled waves over threshold (L921-923). The census `settled` counter is marker-based (results.json, closeout.md, ...; L890), not per-seat. The SKILL does not warn; knowledge L13-16 does.
- L481 "re-scan after the stall threshold": the settlement tool has no threshold. The only candidate is census `WAVE_UNSETTLED_S`, default 7200 (census L352), which the SKILL does not name.

### M3. Exit 1 also covers crashes (SKILL L487 "1 ... never failed"; knowledge L43 "not an error")
- Fixture T7: a 100000-deep JSON array in a dispatch file -> `RecursionError` traceback on stderr, rc 1. The tool catches only UnicodeDecodeError, JSONDecodeError and ValueError (L330-331).
- Remedy: catch RecursionError and MemoryError and exit 2.

### M4. `settled` (exit 0) can hide a shared report path (SKILL L478)
- Fixture T8: two members share `reports/A.md` -> state settled, present 2, duplicate_report_paths 1, rc 0 (tool L273, L303; R5 case L47 expects exit 0).
- SKILL L478 defines settled as "every member present" and never mentions `duplicate_report_paths`.

### M5. Stub rule narrower than stated; unreadable markers count as present (SKILL L483; QUALITY 66)
- Tool accepts exactly two byte strings (L36), reads only when size <= 16 (L230-231), and falls through to `present` when the read fails (L233).
- Fixture T6: `STATUS: started\r\n`, `STATUS: started\n\n`, `STATUS: started \n` -> present (present 3, stub 2). Unreadable 16-byte marker (mode 000) -> present; readable marker -> stub (U1, snapshot).
- SKILL L483 says "whole content is the seat start marker" and forbids "counting a marker as a delivered report"; QUALITY 66 (QUALITY.md:241-244) says the same.

### M6. `--pin` overwrites silently; no reason field; r10 protection is instruction-only (SKILL L491, L497, L500)
- census `run_pin` (L2920-2938) writes `"$path"` unconditionally at L2932 with no existence check. The header (L2925-2931) has census_sha256, pinned_ts, volatile_fields and volatile_note, and no reason.
- SKILL L497 says "recording the reason" without a field or file. L491 says the r10 file "stays byte-unchanged", but nothing prevents `--pin corpus/evidence/baseline-r10-20261015T2231Z.json`.
- [code-verified, not executed: the pin runs the live census, which this seat may not run.]
- Remedy: refuse an existing path in run_pin (census change, L1 decision), or add a SKILL rule to use a fresh UTC name only; name where the reason goes (drift-repin-r20.md).

### M7. The contract's comm recipe counts `MORI_DRIFT: none` as an unclassified token (contract L38-41; SKILL L498)
- With DRIFT containing `MORI_DRIFT: none`, the recipe prints `1` (the token `none`). Observed.
- SKILL L498 says "record rc and tokens whatever they are" after a re-pin. A `none` result would show a phantom unclassified token.
- Remedy: filter `none` in the recipe (for example `grep -v '^none$'`), or document it.

### L1. "unsafe ... escapes the lane root" (SKILL L485)
- The check is lexical (tool L156-174). A symlinked-directory escape reads `missing`, not `unsafe` (T10: missing 1, unsafe 0, state unsettled). Knowledge L54-57 states this; the SKILL does not.

### L2. Overlapping states (SKILL L481-482)
- "unsettled: zero present, at least one member" also describes an all-unparsed wave, which the tool calls `unavailable` (T11; check at tool L283 precedes L289). Precedence exists only in code.

### L3. Wording (SKILL L477-478)
- "per-member counts": counts are per wave (tool L250, L299); members carry only `status` (L276).
- "counts non-empty files only": stubs are excluded, and duplicate paths double-count (M4).

### L4. Oral-context gaps (SKILL L477, L493-497)
- `<lane>`, `<fleet>` (L477) and `<UTC>` (L497) have no value or format.
- `tools/...` and `corpus/...` assume cwd = lane root; not stated.
- "the r20 contract" (L494) has no path; it is `.ufo/waves/round-20/contract.md`, recipe at L38-41.
- "the measured commit" (L493) is undefined.
- `> DRIFT` (L493) leaves an untracked DRIFT file in cwd.
- rc 0/1/2 for `--drift` (census L405) is not stated where step 6 uses rc.
- "census SHA" (L493) has no command; `sha256sum tools/mori-census.sh` matches 87b8d680...ab28.

### L5. `--lane-root` as a symlink exits 2 with "lane root is unreadable" (fixture T5; tool L314-315, L673-675)
- A readable path is reported as unreadable; not documented.

### L6. Ambiguous citation (SKILL L483)
- "(`corpus/QUALITY.md` 66)" means criterion 66 (QUALITY.md:241-244), not line 66 (criterion 27).

### L7. Stale knowledge verification stamp
- wave-settlement-r20.md L8 cites tool sha e5c06dad...; the current tool is 203c716e....

## Fixture evidence (snapshot tool, /tmp/ReviewSkill/fx2)
| case | rc | result |
|---|---|---|
| T1 no .ufo | 0 | waves [] |
| T2 waves dir symlink | 0 | waves [] |
| T3 malformed only | 0 | unreadable_json 1, waves [] |
| T4 dispatch file symlink | 0 | ignored 0, unreadable 0, waves [] |
| T4b `.JSON` suffix | 0 | waves [] |
| T5 lane-root symlink | 2 | "lane root is unreadable" |
| T6 stub variants | 1 | present 3, stub 2 |
| T7 100000-deep JSON | 1 | RecursionError traceback |
| T8 shared report path | 0 | settled, duplicate_report_paths 1 |
| T9 member "dead-seat" | 1 | stdout contains "dead" x2 |
| T10 dir symlink escape | 1 | missing 1, unsafe 0, unsettled |
| T11 all trailers missing | 1 | unavailable, unparsed 2 |
| T12 misrooted | 1 | misrooted 1, unsettled |
| T13 tasks [] | 1 | unavailable |
| T14 taskCall null | 0 | no-spawn |
| T15 two waves | 1 | byte-identical; --out == stdout |
| T16 missing lane | 2 | "lane root is unreadable" |
| U1 unreadable markers | 1 | stub 1, present 2 |
| selftest | 0 | PASS 22/22 |

## Unverified / [INFERENCE]
- Census `--drift` runtime ("about 2 min, heavy CPU", L493) and the r20 register result of 0 (contract L43-44): not run; live census not authorized for this seat.
- `--pin` overwrite (M6) and the census SURFACE waves output (M2): code-read only.
- Whether zero-wave exit 0 (H1) is intentional: unknown; treated as a gap.

## Remedies (not applied; L1 decides)
1. Tool: exit 2 for zero discovered dispatch files or a symlinked waves root; count symlinked and uppercase JSON as unreadable; catch RecursionError and MemoryError; add a wave or round selector (or exclude falsify/); report unreadable markers as `unreadable`, not `present`.
2. SKILL: rewrite L487 (zero-wave, lane-wide rc, crash); narrow L489 to the state words; replace the L477 SURFACE precondition with a per-wave mtime check; add the receipt step (QUALITY 64); name or drop the L481 threshold; list marker variants at L483; say "lexically" at L485; at L497 forbid reuse of an existing path and name the reason file; add the `none` artifact note at L498; give cwd, DRIFT location and rc meanings at L493-494.
3. Contract recipe (L39-40): filter `none`.
4. Knowledge doc: refresh the verified-at sha (L8); cite the lane-wide rc and probe-tree caveats.
