# Mo80E01SweepTool — C1 implementation handoff

## 1. Scope and work

Axes: calibration (C1 claim/reality agreement), operability (read-only interface and setup failures), coverage (all frozen graded-row classes). No scalar change or frozen claim is asserted met here.

Created only:
- `tools/mori-claim-sweep.py`: standard-library single-file sweep, isolated-Python compatible; no files, sockets or scratch paths created by the tool. Only pins-listed `.py`/`.sh` tools are spawned with `--selftest`; Python uses the current interpreter with `-I`, shell uses `bash`; child cwd is root and environment including TMPDIR is inherited.
- `.ufo/waves/round-80/claim-pins.json`: schema `mori-claim-pins-v1`, control-receipt tally 19, one stale literal `selftest 18 in-memory cases`; no self-pin.
- This exclusive advisory report.

Implemented `--root DIR`, `--pins FILE`, `--carriers A[,B]`, `--selftest`, `--help`; value options also accept `=VALUE`. Root is required except help/selftest. Setup diagnostics go to stdout. Successful scans print mismatch records, then `CLAIM_SWEEP mismatches=M unresolved=U tallies=T stale=S carriers=C pointers=P`; rc 0 clean, 1 mismatches, 2 setup. Selftest prints case results and `CLAIM_SWEEP_SELFTEST pass=P fail=F`.

The source declares 25 in-memory cases: 17 sweep cases and 8 count-grammar cases. This is a source count, NOT an executed passing tally. Sweep cases include all twelve named minimum acceptance arms, plus malformed pins, capability-table detection, checklist embedded commands, ungraded prose and repeated stale literals. Grammar cases cover all four success forms, nonzero fail, unequal PASS fraction, unparseable output and conflicting counts. No physical fixture directory is created by selftest.

## 2. Exact retained executed evidence

Ran before noticing the fleet instruction to skip tests during the editing wave:

```sh
python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py --selftest; echo "rc=$?"
```

Output:

```text
case 01 bound section ($ cmd above count)      pass
case 02 unbound section (count, no command)    pass
case 03 comment line neither command nor claim pass
case 04 inline cmd= line binds the section     pass
case 05 split across two ## headings           pass
case 06 non-integer key=value not a claim      pass
case 07 negative integer claim                 pass
case 08 empty file                             pass
case 09 missing path rc 2, diagnostic on stdout pass
case 10 receipt with no claims rc 0            pass
case 11 verb-led first token binds             pass
case 12 indented comment/claim handled         pass
case 13 claim key character class              pass
case 14 bare cmd= without space does not bind  pass
case 15 summary aggregates across files        pass
case 16 dir collection filters and sorts       pass
case 17 unreadable file rc 2, diagnostic on stdout pass
case 18 unbound line carries heading text      pass
case 19 rc 2 diagnostics on stdout only        pass
CONTROL_RECEIPT_SELFTEST pass=19 fail=0
rc=0
```

Tool reads retained these entering facts, not newly executed counter results:
- Frozen contract names P-C1/P-C2/P-C3 and entering `d5888922`.
- SCORECARD read at snapshot `8EFD`, line 4016, contains the stale literal in the control-receipt capability row.
- SKILL read at snapshot `DC64`, line 1365, already states landed control-receipt `pass=19 fail=0`, while explaining historical 18-arm bytes.
- `controls-r80.txt` records entering missing sweep, control-receipt 19, and the frozen counters' receipts. Those are pre-existing evidence, not this seat's reruns.

## 3. Required receipts deferred to L1

No sweep selftest, live sweep, corrected-scratch sweep, build, lint or formatter was run. Fleet executor instructions prohibit tests during the editing wave; this conflicts with the seat's requested acceptance runs. L1 was notified. No passing tally or zero-mismatch result is fabricated.

Post-wave commands (NOT EXECUTED here):

```sh
python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-claim-sweep.py --selftest
python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-claim-sweep.py --root /home/vgpnk/Projects/shokunin/mori-shokunin --pins /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-80/claim-pins.json
```

The requested before receipt must use SCORECARD bytes from before the sibling's correction: they were stale at my read but are concurrently owned by Mo80E02Correct. To preserve that falsifier after integration, L1 should export entering `d5888922` to its permitted scratch, overlay the new sweep and pins, run it there, and retain the first mismatch and rc 1. For the corrected-scratch receipt, copy that SCORECARD to another scratch tree (or correct only the first tree's copied SCORECARD), replace the exact stale literal with its 19-case equivalent, then run with `--carriers SCORECARD.md`; retain stdout and rc. These receipts remain unverified here. All fixture directories must follow the assignment's explicit scratch-root and cleanup rules.

## 4. Frozen-spec interpretation

1. Optional pins defaults to `ROOT/.ufo/waves/round-80/claim-pins.json`; explicitly relative pins resolve under root. Absolute pins are accepted. Pins require the named schema; absent optional collections mean empty collections.
2. Carrier selection limits both pointer grading and stale scanning. Defaults preserve frozen order. Mismatches are sorted carrier-order, line, class, detail; the stale SCORECARD row therefore precedes later carriers when it is the only mismatch.
3. Capability tables are recognized structurally by `What it can now do` plus a `Capability`, `Name` or `key` column, case-insensitively; this includes tables under round headings without a separate capabilities heading. Header/separator rows are not graded. The Axes table is specifically under `## Axes`.
4. Pointer extraction supports commands inside backticks (`python tools/... --selftest`) but excludes absolute/sibling-prefixed paths, and strips revision/line suffixes in either order. It checks current existence, not historical revisions or line contents. Paths resolving outside root are refused.
5. Fenced blocks are excluded from pointer grading, not from stale scanning: the stale rule says each literal must occur zero times in carriers. Each literal occurrence counts separately, including repeated occurrences on one line.
6. A tally is a mismatch only when a successful, parseable live count differs. Nonzero child status, explicit nonzero `fail=`, unequal PASS fraction, missing/conflicting counts and missing pinned tools are setup errors. Children inherit TMPDIR; the frozen CLI has no `--scratch` flag, so none was added.

## 5. Limits, defects and blockers

- Own defect: I initially emitted an unnecessarily verbose narrative and ran the control selftest before applying the fleet's no-tests-during-editing instruction. Caught by rereading the role constraints; no further tests ran. The measured 19 remains genuine evidence, but this workflow deviation is disclosed.
- Actual LSP unavailability: no LSP tool is exposed in this seat's tool inventory. Used direct file/regex context, not a guessed symbol-reference result. This is a new standalone script with no pre-existing symbol callers to refactor.
- No installations, global configuration changes, git mutations, external state changes, scratch directories or credential reads.
- Pending: actual acceptance receipts and independent falsification belong to the post-integration L1 gate. Sibling SCORECARD/SKILL edits and province inventory are intentionally not touched.

## 6. Self-evaluation (advisory, not a gate)

Accuracy 4: only the control selftest is executed; sweep behavior is implementation intent pending L1 receipts. Completeness 4: implementation and pins landed, acceptance execution deferred by higher-priority fleet instruction. Clarity 4: explicit parsing/default decisions, but the report is longer because it preserves full observed output. Actionability 4: exact post-wave commands supplied; stale-before scratch reconstruction still needs L1 execution. Conciseness 4: full receipt retained rather than duplicating it in a second artifact. Average 4.0. Highest-impact improvement: L1 execute and retain all three acceptance receipts. Would the user agree? Only if pending verification is kept visibly distinct from a pass.

## 7. L1/reviewer falsifier and requested wildcard correction

The preceding implementation description's 25 declared cases describes the first version. Final source declares **27** (19 sweep fixtures + 8 grammar cases), still NOT locally executed.

L1 MoriR80 supplied this observed command/output on the initial implementation after the sibling corrected SCORECARD (peer evidence, not an execution by this seat):

```sh
python3 -I tools/mori-claim-sweep.py --root . --pins .ufo/waves/round-80/claim-pins.json
```

```text
CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:1558 .ufo/waves/round-24/w2/Mut*.md
CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:1559 .ufo/waves/round-24/evidence/c1-*.json
CLAIM_SWEEP_MISMATCH unresolved SCORECARD.md:1593 .ufo/waves/round-25/evidence/routed-r24-*-a5.txt
CLAIM_SWEEP mismatches=3 unresolved=3 tallies=0 stale=0 carriers=4 pointers=228
rc=1
```

Independent reviewer Mo80R02Probe reported initial sweep SHA-256 `a481cd28371273d899cbbbe52322c1a1f545cfdead8a6a600abfa884222abe99`: entering export had four mismatches (three unresolved patterns plus stale literal); corrected SCORECARD alone still had three unresolved patterns. This falsifies my first implementation's literal-only pointer treatment.

At L1's explicit request, added `glob.glob` resolution when a pointer contains `*` or `?`, requiring at least one existing in-root match with no symlink components. Literal pointers retain the original existence check. Two selftest cases now exercise matching `corpus/li?e*.md` and nonmatching `corpus/dead*.md`. The docstring expressly limits this: a matching pattern does not prove that its matches are the intended evidence. All unrelated tool bytes remain unchanged.

Own substantive defect: treated citation patterns as literal paths, creating three false positives and preventing the corrected-byte zero target. Caught by actual independent L1/reviewer runs, not inferred from a selftest. Corrected the tool, not SCORECARD or any frozen predicate. No correction was made to the historical evidence.

No post-fix selftest or acceptance command was executed by this seat because the fleet editing-wave prohibition still applies; L1 and the registry seat were told the final declared count is 27, not a proven passing tally. This appendix supersedes the first-version 25-case source count. Pending acceptance remains explicit.

## 8. Mutation-survivor correction requested by L1

After initial handoff, MoriR80 relayed mutation evidence on pre-glob SHA-256 `a481cd28…`: five of six mutants killed; `C1f_count_unresolved_only` survived because no fixture asserted the reported total when only stale or tally fired. This is independent supplied evidence, not a command executed by this seat.

Added three arms asserting the complete summary line, including all four mismatch numbers and carrier/pointer counts: stale-only `mismatches=1 unresolved=0 tallies=0 stale=1`, tally-only `mismatches=1 unresolved=0 tallies=1 stale=0`, and stale plus dead-pointer `mismatches=2 unresolved=1 tallies=0 stale=1`. Production code is unchanged by this correction.

Final declared source tally is now **30 cases** (22 sweep fixtures + 8 grammar cases), superseding both 25 and 27. Still no local execution due the fleet editing-wave test prohibition. L1 owns actual selftest receipt and mutation remeasurement. Own defect: initial assertions checked per-arm counts/rc but not additive summary integrity; mutation evidence exposed that blind spot.
