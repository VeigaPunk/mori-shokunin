# Round 24 declaration sizing review (C1 and C2)

Reviewer: MoriR24.ReviewDeclarationSizing (leaf seat, read-only, no subagent dispatch).
Scope: the round-24 declaration in SCORECARD.md (lines 1494 to 1506) and
.ufo/waves/round-24/contract.md, including amendments A1 to A4.

## Anchor

- SCORECARD.md blob 9e81cbb687be399f5f12bf5a3e0c277b0025f172.
- .ufo/waves/round-24/contract.md blob dec35cb103b63947665c30a6227a851e8073f00d (158 lines).
- Both blobs are identical at HEAD 6fce88a3e28278714cff299180f35e29a3e8b529, at 06a7686,
  and in the working copy (git hash-object, no write). The last declaration change is
  commit f38dbbd (amendment A4).
- The lane moved while I reviewed (06d4f4d, f38dbbd, 06a7686, 88f9620, df4db54, 6fce88a).
  The declaration text did not change after f38dbbd. Facts about deliverables are dated
  to the commit named in each finding.

## Rule applied

1. One after-value per claim, re-derivable by one command over committed bytes.
2. No universal clause unless it is enumerated. For an after-value, the enumerated set
   must also be exercised by that after-value.
3. A calibration claim counts mismatches between self-assessment and repo state.

## Verdict

Neither claim is sized to the rule as written.

- C1 (calibration): the after-value command exists with the declared flags and output keys.
  But the calibration count reads no self-assessment sentence (F14), the routed text is
  abridged in ways that change what is counted (F10, F11), and the R4 population is
  defined by file name (F12).
- C2 (coverage): the SCORECARD row names one after-value, but the contract attaches a second
  condition that reads live host state (F1). The sourced list cites a source that the
  registry marks as rejected (F15). Several universal clauses are not exercised by the
  after-value (F5, F6).

Each finding has a fix that keeps the routed or declared target. Two fixes change only what is
counted, not the target: F10 (R1 fallback) and F11 (R4 fallback). Each says so where it appears.

Counts: 25 findings. High 3 (F1, F14, F15). Medium 13. Low 9.

## Findings

### Rule 1: one after-value, one command, committed bytes

**F1 (high). C2 after-value carries a second, host-dependent condition.**
- Where: contract.md:95-98; amendment A2 at contract.md:118-121. SCORECARD.md:1502 states only
  the selftest.
- Exact sentence, contract.md:95-98: "`python3 -I tools/mori-pressure.py --selftest` at the
  landed tip prints `MORI_PRESSURE_SELFTEST: PASS 12/12`, exit 0; plus one live host run
  retained as evidence and a SCORECARD capability row."
- Exact sentence, contract.md:118-119 (A2): "The "live host run retained as evidence" gets a
  pass condition (a bracket check, not part of the 12): read the raw files, run the tool,
  read again; ..."
- Why it violates the rule: the bracket check reads /proc at run time. It is not committed
  bytes. It is also a second pass or fail condition on the same claim. The two declarations
  now disagree about what the after-value is.
- Minimal fix: delete "plus one live host run retained as evidence and a SCORECARD capability
  row" from contract.md:97-98. Restate the bracket check as "Evidence, not counted:" with its
  pass condition text unchanged. The live run and the capability row stay required. Target
  unchanged.

**F2 (medium). C2 ordering and blind-seat clauses sit outside the one command.**
- Where: SCORECARD.md:1502, exact phrase "exit 0, over cases landed before the tool". Contract
  contract.md:80-82: "(12 cases P01-P12, written by a seat that does not see the implementation,
  landed before the tool)".
- Evidence: f6a2970 (cases frozen, 08:22:43Z) precedes 6ee6248 (tool landed, 08:25:21Z), and
  `git log -- tools/fixtures/mori-pressure/cases.json` lists only f6a2970. The ordering holds
  now, but the one command does not check it. The blind-seat clause is not byte-checkable.
- Minimal fix: state the ordering as a labelled precondition with its own command:
  `git merge-base --is-ancestor <commit adding cases.json> <commit adding tools/mori-pressure.py>`
  exits 0, with both commits found by `git log --diff-filter=A --format=%H -1 -- <path>`.
  Move the blind-seat statement to a process note that names its dispatch file. Target
  unchanged.

**F3 (medium). C2 after-value is not over committed bytes as the header promises.**
- Where: contract.md:8, "Each declares one after-value that one command over committed bytes
  re-derives." The C2 selftest reads fixtures from the script directory: tools/mori-pressure.py:398-401
  (`os.path.realpath(__file__)`, then `fixtures/mori-pressure/cases.json`).
- By contrast, tools/mori-routed-check.py:4-6 says every predicate reads git objects and "the
  working tree is never consulted".
- Minimal fix: state that the C2 after-value runs on an extraction of the landed tip, for
  example `git archive <tip> | tar -x -C "$TMPDIR/<dir>"` followed by
  `python3 -I "$TMPDIR/<dir>/tools/mori-pressure.py" --selftest`. Target unchanged.

**F4 (low). C1 after-value is written two ways and has placeholders.**
- SCORECARD.md:1501 writes `--repo <lane>`. Contract contract.md:44-45 writes
  `--repo /home/vgpnk/Projects/shokunin/mori-shokunin`. Both write `--rev <landed tip>`.
- Minimal fix: use the absolute repo path in both documents. Define `<landed tip>` as the
  commit that the round report records as the measured revision. Target unchanged.

### Rule 2: universal clauses must be enumerated, and the after-value must exercise them

**F5 (medium). C2 shape universal is not exercised.**
- Exact sentence, contract.md:62-63: "Duplicate kinds, missing required kinds or any other
  shape → resource state `malformed`."
- Exercised malformed shapes: P08 (non-decimal avg10 in io) and P09 (memory missing full),
  per contract.md:88-89. The frozen file has no duplicate-kind case
  (`git grep -i duplicate` at HEAD finds nothing in tools/fixtures/mori-pressure/cases.json).
- Minimal fix: add frozen cases for the rejected shapes the grammar names (at least duplicate
  kind, extra token, negative total, non-integer total) under a new freeze commit that lands
  before the after-value is re-measured. Keep one after-value (`--selftest`) with the new count.
  Until then, do not read "PASS 12/12" as covering "any other shape". Target unchanged.

**F6 (medium). C2 threshold universal covers six pairs; two are exercised.**
- Exact sentence, contract.md:70-71: "Threshold: `--warn-avg10 X` (default 10.0, labeled local,
  not calibrated): finding `PRESSURE_HIGH` when avg10 ≥ X on `some` of cpu/io/memory or `full`
  of memory/io/irq."
- Firing exercised: P06 (memory some) and P07 (irq full) only. Never shown to fire: cpu some, io
  some, memory full, io full. P01's normal-low values may exercise non-firing, not firing.
- Minimal fix: one frozen case per unexercised pair, under a new freeze commit as in F5.
  Target unchanged.

**F7 (low). C2 bounds are unenumerated, and an enumerable check exists.**
- Exact sentence, contract.md:106-107: "Detection and report only. No host writes, no PSI
  trigger registration, no cgroup writes, no service or package changes."
- Evidence: tools/mori-pressure.py opens files only in read mode (lines 157 and 504,
  `open(path, "r", ...)`). The only other output is stdout (line 390).
- Minimal fix: replace the bound with the check: "The tool opens files only with mode "r"
  (tools/mori-pressure.py:157, 504) and writes only stdout (:390); `git grep -nE
  'open\(|O_WRONLY|O_RDWR|O_CREAT|unlink|mkdir' <tip> -- tools/mori-pressure.py` lists only
  those lines. This does not verify host effects." Target unchanged.

**F8 (low). C2 Before universal is unenumerated; A2 qualifier is not carried into it.**
- Exact sentence, SCORECARD.md:1502: "no mori tool reads system CPU, IO or IRQ pressure".
  Same sentence at contract.md:93-94. Amendment A2 at contract.md:123-124 says it "means by
  default".
- Enumerable check: `git grep -nE 'pressure/(cpu|io|irq|memory)|/proc/pressure' c725aa37 -- tools/`
  prints nothing and exits 1 (checked). The census PSI path is operator-pinnable through
  tools/mori-census.sh:224 and :308 (MORI_CGROUP_PRESSURE).
- Minimal fix: replace the universal with that command and the two pin points. Drop "by
  default" once this is done. Target unchanged.

**F9 (low). "promotion" is undefined, and C2 moves capability to Core.**
- Exact sentence, contract.md:107-108: "No retirement, waiver, exploratory claim or promotion."
  Compare contract.md:55, "This claim moves one-shot system PSI reading to Core."
- The round-23 spot-check uses the term for score or admission changes: corpus/lessons/
  round-23-verifier-spotcheck.md:8, "Scores may hold; no promotion, exploratory conversion,
  frozen-expectation rewrite or capability addition."
- Minimal fix: define the term once, for example "promotion = an axis score change or an
  admission beyond the declared after-value". Name the axes in the retirement clause. State that
  the FR12 move is a capability entry, not a promotion. Target unchanged.

**F10 (medium). C1 R1 "capability absent" is a functional universal that is checked by name.**
- Contract row, contract.md:22: "keep quota capability absent; never alter CaseEscapedSpace's
  expected row". The routed text is abridged. The full routed sentence, corpus/lessons/
  round-23-verifier-spotcheck.md:62, is: "Keep quota detection/capability absent unless a new
  source-derived declaration, independently frozen oracle and prospective proof resolve
  topology, incomplete device enumeration and accounting/enforcement ambiguity." The
  conditional is dropped from the contract. QUALITY.md:314 keeps it ("until a new sourced
  declaration").
- The R1 predicate checks names: tools/mori-routed-check.py:72-75 (two paths) and :85 (the
  word "quota" in a path added under tools/ or corpus/knowledge/). A quota reader added under
  another name passes.
- Minimal fix: quote the routed sentence verbatim in the contract table. State R1's counted
  scope as the enumerated name set and the historical case name. Put the functional capability
  check on the why-not list, with the unless-clause, until a byte-checkable definition exists.
  This changes what is counted, not the routed target. Do not add a content check on added lines
  as a quick fix: tools/mori-routed-check.py itself contains "quota" in lines 66-85 and was added
  under tools/ in 88f9620, so such a check would flag the checker.

**F11 (medium). C1 R4 counts one of four routed clauses as the whole item.**
- Contract row, contract.md:25: "| R4 | bind future dispatches before the call |".
- Routed text, corpus/lessons/round-23-verifier-spotcheck.md:65: "Bind future dispatches before
  the call, keep source writers in separate worktrees and report extra invocations/resource
  units accurately."
- "held 4 of 4" implies the whole item. Only the binding clause is tested. The worktree clause
  and the accurate-reporting clause are neither counted nor listed as why-nots.
- Minimal fix (preferred): add predicates for the other two clauses. For example, the
  worktree value in each source-writer row must differ within a wave, and each wave's reported
  invocation count must equal its ledger rows. Fallback, if neither is byte-checkable before
  landing: list both clauses as "not counted, why-not" in the declaration. The fallback changes
  what is counted, not the routed target, and the declaration should say that.

**F12 (medium). C1 R4 dispatch population is defined by file name, so a dispatch record can escape.**
- Exact sentence, contract.md:144: "every `.ufo/waves/round-N/*-attempts.json` and
  `*-ledger.json` at REV (at least one) verifies clean with `tools/mori-dispatch-ledger.py verify`".
- The tool uses the same population: tools/mori-routed-check.py:480,
  `-(attempts|ledger)\.json$`.
- Evidence: c725aa37:.ufo/waves/round-23/wave2-attempt1-start.json lines 3-4 carry `"at"` and
  `"dispatch_path": ".ufo/waves/round-23/wave2-run.json"`. The name matches neither pattern, so
  this dispatch is outside R4 at round 23.
- Minimal fix: define the population by content, not name. The set of `dispatch_path` values in
  every ledger in `.ufo/waves/round-N/` must equal the set of `.ufo/waves/round-N/wave*-run.json`
  at REV. Adding `start` to the regex would also work but is less robust. Target unchanged.

**F13 (low). C1 R2 does not pin the file that holds its routed value.**
- Contract row, contract.md:23: "blobs ... equal base". Pinned files: tools/mori-routed-check.py:92-93
  pins the two `-final` retention files only. Amendment A1 (contract.md:36-38) excludes `.ufo/**`
  from R2's added-line scan.
- Evidence: `privacy_clearance` appears in neither pinned blob at base (count zero for both). It
  appears at c725aa37:.ufo/waves/round-23/evidence/retention-floor-comparison.json:10,
  `"privacy_clearance": false`.
- Only the whole-tree pins of R1 and R3 (contract.md:153-155) cover that file. A flip there
  turns R1 and R3 red, not R2. The after-value still fails, but the "able to fail" mapping at
  contract.md:46-48 is wrong for that file.
- Minimal fix: add that file to R2's pinned blobs and assert that `"privacy_clearance": false`
  is present in it. Keep the R1 and R3 tree pins. Target unchanged.

### Rule 3: calibration counts mismatches between self-assessment and repo state

**F14 (high). C1 calibration count reads no self-assessment sentence.**
- Exact sentence, contract.md:17-18: "It compares the lane's round-23 self-assessment with
  committed bytes at REV and reports one row per routed item".
- The routed items are not the lane's self-assessment. They come from the outside integrator:
  corpus/lessons/round-23-verifier-spotcheck.md:3, "author: Main, hyaku non-author integrator
  and admission authority", and lines 62-66 are its routing list.
- The four predicates test that bytes equal base (R1 to R3) and that ledger timing holds (R4).
  contract.md:153 says "R1–R3 are regression guards, not repairs." No predicate reads a sentence
  the lane wrote about itself. So "held: 4" is not a calibration count, and the calibration axis
  (SCORECARD.md:1501, "calibration 5") is not measured.
- Minimal fix: for each row, name the lane's own round-23 self-assessment sentence with its
  path and line, and count the rows where that sentence disagrees with committed bytes at REV.
  Example candidate: SCORECARD.md:1426-1427, "Open debt carried: 4 unallowlisted retention hits,
  permission control RED 11/12, two unknown historical dispositions, baseline acceptance blocked,
  no privacy clearance." Keep the guard predicates as additional rows. Target unchanged.

**F15 (high). C2 Sourced list cites a source the registry marks as rejected.**
- Exact sentence, contract.md:99-102: "the knowledge entry ... and the decision table in SKILL.md
  cite `SOURCES.md` rows opened this round (Linux v7.2 PSI documentation and `kernel/sched/psi.c`,
  cgroup-v2 pressure files, PSI Kconfig and boot parameter, proc_pressure(5))."
- corpus/SOURCES.md:103 (S097): "REJECTED: the assigned manual page does not exist" (HTTP 404).
  The knowledge entry, corpus/knowledge/system-pressure-r24.md:185 (U6), says the same and names
  S090 as the format authority. SKILL.md:619 and :630 cite S090, S091, S095 and S096, not S097.
- Minimal fix: replace "proc_pressure(5)" with "S090 (kernel v7.2 Documentation/accounting/psi.rst)".
  "Opened this round" is byte-checkable through the SOURCES `opened` column. I checked that
  S093 to S097 carry 2026-10-22 (corpus/SOURCES.md:99-103). I did not check the S090 to S092
  cells. Target unchanged.

**F16 (medium). C2 row calls a fixture-level after-value a "capability".**
- Exact phrase, SCORECARD.md:1502: "C2 system CPU, IO and IRQ pressure capability (FR12, sourced)".
- The after-value is the 12-case selftest. It uses an in-process errno hook for EOPNOTSUPP and
  EACCES (contract.md:83). It does not read a live host.
- Minimal fix: retitle the row as "fixture-verified system PSI reader (parse and state mapping;
  live reads not counted)". Target unchanged.

**F17 (medium). C2 bounds omit the root-switch limit.**
- The only "not evidence of no stall" bound, contract.md:66-67, is: "System `cpu` `full`: reported
  but labeled `full_system_undefined: true`; never used for a threshold and never read as evidence
  of no stall." It covers one kind.
- Knowledge U7, corpus/knowledge/system-pressure-r24.md:186: "writing 0 to the root cgroup's
  `cgroup.pressure` stops system accounting, so `/proc/pressure` would stay frozen and a one-shot
  read would report `PRESSURE_OK` under real pressure."
- Minimal fix: add to the contract bounds: "PRESSURE_OK is not evidence of no stall; the root
  `cgroup.pressure` switch limit (knowledge U7) is unverified." Target unchanged.

**F18 (low). A2 states a boot-order consequence as fact; the knowledge entry labels it inference.**
- Exact sentence, contract.md:112-113 (A2): "Kernel v7.2 does not create `/proc/pressure` at all
  when PSI is disabled at boot, so a disabled kernel shows every file `absent` (ENOENT), not
  EOPNOTSUPP."
- Knowledge U4, corpus/knowledge/system-pressure-r24.md:181-182: "The relative order of
  `psi_init()` and `psi_proc_init()` was not verified, so the "boot-parameter disable ⇒ absent
  files" statement in F7 is labeled [INFERENCE]."
- My raw read of Linux v7.2 kernel/sched/psi.c supports the sentence. psi_proc_init creates the
  /proc/pressure entries only under `if (psi_enable)` (registry row S091, psi_proc_init:1710-1721),
  and psi_enable's default depends on CONFIG_PSI_DEFAULT_DISABLED (lines 140-160 of the file).
  But A2 gives no citation and drops the label.
- Minimal fix: cite S091 psi_proc_init:1710-1721 in A2, and keep the [INFERENCE] label until the
  boot-order question is verified. Target unchanged.

**F19 (medium). C1 "No tool checked these items" and "no check exists" are contradicted by base tools.**
- Exact sentence, contract.md:43: "No tool checked these items before this round." Exact phrase,
  SCORECARD.md:1501: "no check exists".
- At base c725aa37, tools/mori-retention-reconcile.py:238 emits `'privacy_clearance':False`, and
  its selftest asserts `v.get('privacy_clearance') is False` at :273. tools/mori-dispatch-ledger.py
  defines `_verify` at :200 and the `verify` subcommand at :559, the same tool R4 calls.
- What is new is narrower: no base tool compares a dispatch commit time with a ledger `at` value.
  Base tools do read commit times: tools/mori-census.sh:2254, :2281 and :2430 (launch windows and
  report-path times, from grep hits; I did not read those functions in full). None compares a
  dispatch commit with a ledger row's `at`.
- Minimal fix: "Before this round no tool compared dispatch commit times with ledger `at` values.
  tools/mori-dispatch-ledger.py verify (c725aa37:200, :559) and tools/mori-retention-reconcile.py
  (c725aa37:238, :273) predate the round." Target unchanged.

**F20 (medium). C1 "repair" conflicts with the regression-guard finding, and the Before is stated three ways.**
- Titles: SCORECARD.md:1494, "routed repair and system pressure"; SCORECARD.md:1501, "C1 repair the
  four byte-checkable round-23 routed items"; contract.md:11, "## C1 — repair the round-23 routed
  defects".
- Amendment A4 says the opposite: contract.md:139-141, "the declared before-value (3 of 4 at
  `c725aa37`) was fixed by construction and that R1–R3 had nothing to repair."
- Before, three versions: SCORECARD.md:1501, "expected to report 3 of 4 held (no round-24
  pre-call ledger)"; contract.md:42-43, "expected `held: 3`"; contract.md:150-152 (A4), "**Before,
  measured on the real defect:** ... so R4 is expected red there."
- The A4 heading says "measured", but the sentence says "expected". The prediction matches committed
  bytes. Round-23 rows run from 2026-10-21T17:03:11.644975Z (c725aa37:.ufo/waves/round-23/wave1-ledger.json:4)
  to 17:24:14.626546Z (line 88). The dispatch file's only commit, 22772c1, is at 15:10:59 -0300,
  which is 18:10:59Z. The label is still wrong until a run output is retained.
- Minimal fix: retitle the row and heading to "guard the four byte-checkable round-23 routed items
  and repair R4". Keep one Before statement, labelled "predicted; to be measured by `--round 23` at
  c725aa37", and retain the measured output when it exists. Target unchanged.

### Integrity and consistency

**F21 (medium). Amendment clock labels contradict the commit clock.**
- Headers: contract.md:35 (A1) "08:22Z"; contract.md:110 (A2) "08:30Z, before any C2 tool or case
  landed"; contract.md:126 (A3) "08:33Z, before any C2 tool or case landed"; contract.md:137 (A4)
  "08:37Z, before any C1 tool landed".
- Committer times (UTC): f7eb430 08:17:35Z; 11d8f71 08:19:14Z; f299bd7 08:19:32Z; f38dbbd 08:20:31Z;
  f6a2970 (C2 freeze) 08:22:43Z; 6ee6248 (C2 tool) 08:25:21Z.
- By the text's own clock, A2 and A3 are later than the C2 landings. Their "before" claims hold
  only by commit order. Committer times are self-set, so neither clock is independent evidence.
- Minimal fix: remove the clock labels, and cite commit ids for order, for example "committed in
  11d8f71, before the C2 freeze f6a2970". Target unchanged.

**F22 (medium). The contract predicate table is stale.**
- contract.md:22-25 still define R1 as "tree OID of `.ufo/waves/round-23/frozen` equals base" and
  R4 as "at least one `.ufo/waves/round-24/*-attempts.json` exists". Amendments A1 (contract.md:35-40)
  and A4 (contract.md:143-158) redefine R1 to R4.
- Minimal fix: fold A1 and A4 into the table cells, and keep the amendment log as history. Target
  unchanged.

**F23 (low). The EOPNOTSUPP cause label conflicts with A2.**
- contract.md:68: "EOPNOTSUPP → `unsupported` (PSI disabled);" against contract.md:113-115 (A2): "The
  `unsupported` state stays for an EOPNOTSUPP error, but the tool and the knowledge entry infer no
  cause from it."
- The v7.2 psi_show also returns EOPNOTSUPP for IRQ when IRQ-time accounting is off (S091 rows
  1257-1263), so "PSI disabled" is not the only cause.
- Minimal fix: "EOPNOTSUPP → `unsupported` (no cause inferred)". Target unchanged.

**F24 (low). C2 has no "able to fail" line; C1 has one.** Contract C1 at contract.md:46-48 names
sandbox mutants. C2 names none. This is not a sizing-rule violation. Add one line naming a mutant
for the threshold comparison, to match C1.

**F25 (low). "Reported as a why-not" has no output location.** Contract.md:27-29 says routed
item 5 "is reported as a why-not, not counted". The tool output schema (contract.md:31-33) has no
why-not field, and a search of tools/mori-routed-check.py finds none.
- Minimal fix: name the location, for example "the round report, section Why-not". Target unchanged.

## Checked and not violations

- Each claim has one after-value row in the SCORECARD table. C1 reads "held": 4 of "items": 4,
  exit 0. C2 reads PASS 12/12, exit 0. The defects are in the contract text and the wording
  around the rows (F1, F2).
- The C1 command exists as declared. tools/mori-routed-check.py takes `--repo`, `--rev` and
  `--round` (default 24), and emits `items` and `held` (lines 677-679 and 724-725). Checked
  statically; not run.
- The C2 command exists as declared. tools/mori-pressure.py takes `--selftest` (line 385),
  prints `MORI_PRESSURE_SELFTEST: PASS n/N`, and returns 0 on PASS (lines 540-541). The
  frozen file has 12 P-ids. Checked statically; not run.
- C1 "before" arithmetic holds. At c725aa37, R1 to R3 hold by construction and R4 has no
  round-24 ledger, so held is 3. The count is right, even though the reason is construction
  (F20).
- R4 is attainable for round 24 at HEAD. wave1-run.json has one commit, 06d4f4d at 08:13:57Z,
  and the first wave1 ledger row carries `"at": "2026-10-22T05:14:13.926366-03:00"`
  (wave1-attempts.json:4), which is 08:14:13.9Z. Binding precedes the row by about 16 seconds.
- Round-23 tree, frozen and rejected OIDs are unchanged between c725aa37 and HEAD (both
  pairs equal). No file under .ufo/waves/round-23 changed since base.
- No added line in the R2 scan scope (SCORECARD, PROVINCE, SKILL, LOG, README, corpus/)
  matches the privacy-clearance regex. The count is zero.
- The C2 "before" check holds. `git cat-file -e c725aa37:tools/mori-pressure.py` exits 128.
- "The census reads only the user slice's memory.pressure" (contract.md:54) matches the base
  census. The default is user-slice memory.events and memory.pressure (tools/mori-census.sh:304,
  :308). No io, cpu or irq pressure reader exists at base.
- R2 and R3 pinned blob IDs match base at HEAD: bfcfb2c8, 1411d94a, 4954de42 and ad622617.
- Entering state "round 23 closure: rejected, honest stop" (SCORECARD.md:1496-1497) matches
  corpus/lessons/round-23-verifier-spotcheck.md:8, "Not admitted; rejected-honest-stop."
- The calibration axis choice (score 5, tied with depth and freshness) is consistent with the
  round-23 scores.
- Routed item 5 stays in PROVINCE.md Adjacent (tsukuroi and souji entries at PROVINCE.md:66
  and :69).
- QUALITY.md criteria 72-75 (`routed r23-R1` to `R4`) are present at HEAD (corpus/QUALITY.md:314-327).

## Residual risk (not sizing defects)

- Commit times and the `at` fields are written by the lane. contract.md:149 says so. R4 proves
  recorded ordering, not harness-observed ordering.
- The C2 bracket check reads host state. It can never be a counted after-value.
- P05 and P10 exercise the tool's mapping of errno values through an injected hook, not the
  kernel's behavior (contract.md:83). A2 notes that v7.2 may not produce all four EOPNOTSUPP
  cases.
- A PRESSURE_OK verdict may be wrong under the root-switch limit (F17).

## Verification gaps (what I did not run)

- I ran no lane tool: no selftest, no routed-check, no mutant, no bracket check. Every after-value
  is checked for form and attainability, not for its numeric result.
- Kernel facts: I read Linux v7.2 kernel/sched/psi.c from raw.githubusercontent.com at lines
  140-160, 225-240, 1250-1292 and 1700-1725. I did not check the cgroup root-switch code (U7).
- I did not read QUALITY.md beyond the lines matched by the `routed r23-R` search.
- I did not compare the amendment bodies with the critic reports they cite. The round-24 listing
  at 06a7686 shows no critic report file, so I could not check those citations.
- The lsp device is not in my tool set. No code callers are in scope for a declaration review,
  so no caller analysis was needed.

## Tooling

- No installs or updates. The operator's tooling directive was read and no tool was needed.
- Read-only operations only: git log, show, ls-tree, cat-file, rev-parse, grep, and diff
  between two commits. git hash-object was used without -w. No git status, no index writes,
  no commits, no stash.
- One remote read of raw.githubusercontent.com for the kernel source above.
