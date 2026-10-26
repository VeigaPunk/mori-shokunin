# Mo49ExecFlaggedFixed — flagged versus fixed: does a round-48 wave-1 critic flag change the landing?

Seat: Mo49ExecFlaggedFixed (round 49, wave 1). Leaf seat; no subagents; no skill changes; no writes
outside this report and `.scratch/r49-Mo49ExecFlaggedFixed/`.
Assignment: `considerthese/2026-10-25.md` suggestion 3 — "Track whether in-round critic flags get fixed
... A simple flagged-versus-fixed count per round would show whether critic seats change outcomes."
Author date 2026-10-25; the landing commit it measures is dated `Sun Oct 25 19:30:50 2026 -0300`.
Tooling: nothing installed or upgraded; pacman untouched (host-wide pause); no lane tool run outside
`TMPDIR=.scratch/r49-Mo49ExecFlaggedFixed`; all git use read-only (`show`, `diff`, `rev-parse`).

## 1. Scope and inputs (all read at absolute paths, read-only)

| input | identity |
|---|---|
| freeze | `4387cf94b69ddce455051a1ff38e93795c2e6cde` (round-48 contract freeze) |
| landing | `e4dfff32d4f97c7ef250e9a7538fa75d4f284492` (round-48 data commit, `git log -1` observed) |
| landing diff | `git diff --name-status 4387cf94 e4dfff32` → 59 files (20 non-`w1/`), incl. `M SKILL.md`, `M tools/mori-pin-check.py`, `M corpus/SOURCES.md`, `M corpus/QUALITY.md`, `M LOG.md`, `M SCORECARD.md`, `M corpus/README.md`, `A corpus/lessons/round-48.md`, `A corpus/knowledge/quota-observability-r48.md`, `A tools/mori-unlanded-check.py` |
| reports | `.ufo/waves/round-48/w1/CritC1Counter.md`, `CritC2Counter.md`, `CritContractFreeze.md`, `CritEntryRisk.md`, `CritJunkClasses.md`, `CritV3Spec.md`, `RevAssimPlan.md`, `RevPromptHonesty.md` (the eight `Crit*.md`/`Rev*.md` files in that directory; `ls` shows exactly 6 `Crit` + 2 `Rev`) |
| datum | `corpus/lessons/round-48.md` at the landing (the round's own `## Wave 1 — integrated findings` disposition), `LOG.md` round-48 entry, `corpus/QUALITY.md` 125-128 |

## 2. Method: extraction rule, verdict rule

**Extraction rule (stated so the count can be re-derived).** From each of the eight reports, take every
labeled finding: `## F<n>`/`**F<n> —` sections, `**O<n>**` observation bullets, `### P<n> —` pairs,
`## D<n> —` classes (including the one the report titles "Attempted but unrealizable"), and the numbered
"Counterexample and contradictions" items plus the three named junk edits (`J9`-`J11`) of `CritV3Spec`.
That yields 45 items: CritC1Counter 8, CritC2Counter 2 (the counterexample plus its "second, separate
known limitation"), CritContractFreeze 4, CritEntryRisk 6, CritJunkClasses 9, CritV3Spec 7, RevAssimPlan 5,
RevPromptHonesty 4.

*Not extracted* (read, and deliberately not counted): prose blocks that restate or extend a counted item —
"Smallest safe corrections" lists in CritC1Counter/CritC2Counter/CritJunkClasses/CritV3Spec,
CritEntryRisk §4's four "quirks a wave-2 reviewer should also watch", CritJunkClasses' R-rule matrix, and
the requirement matrices of `RevPromptHonesty`/`RevAssimPlan`. The count is therefore a floor on flags
raised, not a ceiling.

**Verdict rule.** Each item is decided once from committed bytes at `e4dfff32` plus the landing diff:

- **FIXED** — every stated check passes: the landing diff lists the named file, and/or `git show
  e4dfff32:<path>` carries the repair the finding asked for (a rule, a selftest arm, a registry repair,
  a Gate line).
- **UNFIXED** — at least one check fails: the named artifact is not in the landing diff, or the landed
  bytes still lack the repair.
- **NA** — the report itself records the item as a precision note, a positive verification, a named limit
  of the frozen predicate, an information item, or an unrealizable case. NA is not a soft UNFIXED: it
  says the item was never a defect claim against the landed artifacts.

Where a finding's named artifact is a **frozen** file (`count-c1.py`, `count-c2.py`, `v3-spec.md`), the
verdict follows the observable defect, not the file: a frozen instrument cannot be edited after seats
score (contract, freeze preamble), so a spec-text finding is FIXED only when the landed implementation
resolves the ambiguity the text left open — and the table says so per item.

## 3. Table — 45 flags, 18 fixed, 9 unfixed, 18 not applicable

`report:line` is a line of the named round-48 report. Line numbers inside the evidence column are lines
of the artifact under discussion at `e4dfff32`: `count-c1.py` / `count-c2.py` (byte-identical to the
freeze), `tools/mori-pin-check.py` (the landed v3 blob), `SKILL.md`, `corpus/lessons/round-48.md`.

| # | item | report:line | target | verdict | evidence at `e4dfff32` |
|---|---|---|---|---|---|
| 1 | C1-F1 | CritC1Counter.md:26 | `count-c1.py` leaks variant identity via `--skill` basename and per-variant `TMPDIR` | **UNFIXED** | file absent from the landing diff; `variant-%s.md` (:238) and `c1-%s-` (:247) still name each variant |
| 2 | C1-F2 | CritC1Counter.md:83 | real registry red under a literal R4 (row 939 rebinds `C2_SELFTEST`) | **FIXED** | tool changed; docstring `rows new since REV are not compared` (:78) + new-row single-instrument branch (:542-548); re-run at `e4dfff32`: `rebound=0`, `pin line=939 … state=match` |
| 3 | C1-F3 | CritC1Counter.md:109 | `SKILL.md:168` carries a stale truncated digest `c39e5a73…` that resolves to no named path | **FIXED** | row rewritten: "git `5601d12`, sha256 prefix c39e5a73, since changed … current … `533218a5…`"; `git show 5601d12:tools/mori-round14-regressions.py \| sha256sum` → `c39e5a7352666d09dc662293e1ea7be47ee3523b53247a5a6ae02e7dda19288d`; run: `pin line=168 kind=digest state=match digest=533218a566030fda…` |
| 4 | C1-F4 | CritC1Counter.md:122 | literal R3 over-broad (non-ASCII first token / casefolded `selftest` fires on ordinary command spans) | **FIXED** | `span_kind` (:278) classifies digest/truncated/tally/command before the ASCII-strict rules; re-run real: `unparsed=0` |
| 5 | C1-F5 | CritC1Counter.md:136 | J1/J5/J6 are detectable only by executing the bound instrument | NA | the report states all eight junk edits are red under the rules and "the blockers are all on the honest/real side"; no change requested |
| 6 | C1-F6 | CritC1Counter.md:149 | missing `--tool` and bad `--min-tally` end in a traceback (exit 1), not `C1_SETUP` (exit 2) | **UNFIXED** | file absent from the diff; `run_tool` catches only `TimeoutExpired` (:212), `int(opts["--min-tally"])` unguarded (:294) |
| 7 | C1-F7 | CritC1Counter.md:160 | pool/shared-scratch races | NA | positive finding: none found; the only interference surface is the F1 naming |
| 8 | C1-F8 | CritC1Counter.md:170 | the counter measures working-tree bytes (`os.path.abspath(--tool)`), not bytes at `--rev` | **UNFIXED** | file absent from the diff; `tool = os.path.abspath(opts["--tool"])` (:300) unchanged. The report's requested action (commit the candidate) did land, so the hazard is mitigated, but the read path is the same |
| 9 | C2-F1 | CritC2Counter.md:3 | `normalise` keeps `<script>`/`<style>` text, so page script passes as a located quote | **UNFIXED** | `count-c2.py` absent from the diff; `normalise` (:59-62) strips tags, unescapes and collapses only |
| 10 | C2-L1 | CritC2Counter.md:9 | claim/quote entailment is not checked | NA | contract C2 named limit ("does not check that the claim cell follows from the quote"); the report says it is not a counter defect against P-C2 |
| 11 | CF-O1 | CritContractFreeze.md:123 | `junk_met` also counts a crash/timeout | NA | precision note, not a defect ("no freeze defects found") |
| 12 | CF-O2 | CritContractFreeze.md:128 | counter measures `--tool` disk bytes, not rev bytes | NA | precision note (same subject as C1-F8, counted there) |
| 13 | CF-O3 | CritContractFreeze.md:132 | "opens with" implemented as first 14 non-blank lines | NA | precision note |
| 14 | CF-O4 | CritContractFreeze.md:134 | the C2 selftest "staged entry byte-exact" arm is a synthetic stand-in | NA | precision note |
| 15 | ER-P1 | CritEntryRisk.md:36 | claim stronger than the quote | NA | named limit of the frozen predicate; the report asks for a wave-2 reviewer checklist, not a counter edit |
| 16 | ER-P2 | CritEntryRisk.md:48 | quote from a negation context | NA | as above |
| 17 | ER-P3 | CritEntryRisk.md:59 | example-scoped quote generalized | NA | as above |
| 18 | ER-P4 | CritEntryRisk.md:71 | claim about another filesystem | NA | as above |
| 19 | ER-P5 | CritEntryRisk.md:82 | Linux claim from a vendor product page | NA | as above |
| 20 | ER-P6 | CritEntryRisk.md:94 | number lifted from an example manifest | NA | as above |
| 21 | JC-D1 | CritJunkClasses.md:30 | full 64-hex digest satisfied by a decoy file named in another cell | **FIXED** | `R10` (:587) binds a digest to the nearest preceding in-tree path of its own cell; arm `r10_digest_decoy_file_in_other_cell` (:867) |
| 22 | JC-D2 | CritJunkClasses.md:68 | tally pin on a continuation line (no pipe) | **FIXED** | `R9b` (:247); arm `r9b_continuation_line_tally` (:878) |
| 23 | JC-D3 | CritJunkClasses.md:99 | second table headed `Self-test results` is invisible | **FIXED** | row-shaped line outside a parsed table carrying a `*SELFTEST` token → `hidden`; arm `r2_hidden_row_outside_table` (:832) |
| 24 | JC-D4 | CritJunkClasses.md:138 | `~~~`-fenced replacement of the two gate rows | **FIXED** | fences are not exempt; arm `r2_hidden_fenced` (:833) |
| 25 | JC-D5 | CritJunkClasses.md:171 | empty self-test cell, tally claim in pinned-values | **FIXED** | `R9a` (:245); arm `r9a_tally_in_pinned_values_cell` (:874) |
| 26 | JC-D6 | CritJunkClasses.md:298 | unconditional `echo` tally from a committed script | NA | report records it as unrealizable at R and an unverified w2 limit |
| 27 | JC-D7 | CritJunkClasses.md:202 | entry names instrument A, self-test cell runs instrument B | **UNFIXED** | no entry-instrument rule in the tool; `SKILL.md:960-962` records it as "Known survivor, not closed"; QUALITY 125 "Not covered" repeats it |
| 28 | JC-D8 | CritJunkClasses.md:237 | all-ASCII lowercase tally prefix | **FIXED** | casefold-selftest-prefix → `unparsed` (:292-293); arm `r3_lowercase_prefix` (:836) |
| 29 | JC-D18 | CritJunkClasses.md:269 | tally written outside backticks in a self-test cell | **FIXED** | `R9c` (:519); arm `r9c_tally_outside_backticks` (:881) |
| 30 | V3-1 | CritV3Spec.md:7 | R1 header variants vs R2 visibility/precedence | **FIXED** | `HEADER_CELLS = ("self-test", "selftest", "self test")` (:113) used by one tokenizer pass; arms `r1_header_selftest_spelling` (:830), `r1_header_self_test_spelling` (:831) |
| 31 | V3-2 | CritV3Spec.md:9 | R4 prose vs `(row name, prefix, ordinal)` identity | **FIXED** | baseline rows compared per row name + new rows compared when the prefix has one canonical argv (:542-548); arm `r4_rebound_new_row_same_prefix` (:838) |
| 32 | V3-3 | CritV3Spec.md:11 | R5 multi-path cells underspecified and inconsistent with R6 | **FIXED** | one binding rule for R5 (:309), R6/truncated (:319) and R10/full digest (:589): nearest preceding in-tree path of the cell; no path → `unparsed` (R5) / `mismatch` (R6, R10) |
| 33 | V3-4 | CritV3Spec.md:13 | R3 span boundary / accepted tally grammar undefined | **FIXED** | one reason per span (`span_kind` returns on first match, :278-296); grammar in `PINLIKE_T0_RE` (:117), `TALLY_PIN_RE` (:116), `TALLY_TEXT_RE` (:121); arm `r3_fullwidth_prefix` (:835) |
| 34 | V3-J9 | CritV3Spec.md:30 | new row reuses a baseline prefix with another binding | **FIXED** | arm `r4_rebound_new_row_same_prefix` (:838) + the new-row branch (:547-548) |
| 35 | V3-J10 | CritV3Spec.md:42 | ASCII-dot truncated digest (`37fd7c24ff52...`) | **UNFIXED** | `TRUNC_DIGEST_RE = re.compile(r"[0-9a-f]{8,63}\u2026")` (:115) — U+2026 only; an ASCII-dot pin matches no pin rule and is ignored |
| 36 | V3-J11 | CritV3Spec.md:54 | alternate line-count syntax `(742-line file)` | **UNFIXED** | `LINE_COUNT_RE = re.compile(r"(\d+) lines")` (:118) — the hyphenated spelling is invisible |
| 37 | RA-F1 | RevAssimPlan.md:26 | plan commits no Gate reject | **FIXED** | lesson `**Reject, with flip:**` block records 7 refusals (`corpus/lessons/round-48.md:55-76`); lesson:131 names F1 as met |
| 38 | RA-F2 | RevAssimPlan.md:39 | refused sources carry no flip condition | **UNFIXED** | half landed: RHEL 9 PDF has a flip (lesson:75-76); Solaris `errno=49` still has none (lesson:72) even though lesson:131-132 claims "F2 … is met above" |
| 39 | RA-F3 | RevAssimPlan.md:45 | MERGE-REPORT checklist conflicts; deviation unstated | **FIXED** | lesson:133-135 states the four conflicts and "This round followed §10, not the checklist" |
| 40 | RA-F4 | RevAssimPlan.md:61 | MERGE-REPORT "243 rows" stale; re-run the collision check at append | NA | info on read-only package bytes; the actionable half (pre-append collision check) is landed at lesson:44-49 |
| 41 | RA-F5 | RevAssimPlan.md:69 | quarantine verdicts must be `unverifiable` unless fetched | NA | info obligation; lesson:78-84 records three fetched hand-checks, all PRESENT |
| 42 | RH-F1 | RevPromptHonesty.md:36 | `tools/mori-pin-check.py` overwritten mid-wave, restored | **FIXED** | the tool is in the landing diff (v3, the claimed artifact); lesson:141 records `ExecV3ImplA` "aborted after editing the tracked tool and restoring it"; `w1/ExecSkillRowsRun.md:3` records the sha it measured (`9832e38c…` = v2), closing the contamination question |
| 43 | RH-F2 | RevPromptHonesty.md:52 | `evidence/census-start.txt` records no exit code | **UNFIXED** | `git show e4dfff32:.ufo/waves/round-48/evidence/census-start.txt` is 21 lines, no `rc=`; the landing adds no `census-end.txt` (`git ls-tree e4dfff32 .ufo/waves/round-48/evidence/` = 9 files) |
| 44 | RH-F3 | RevPromptHonesty.md:56 | `w1-spec.json` is not the dispatched text | NA | info; `w1-dispatch.json` is committed at `e4dfff32`, so the audit guidance holds without a change |
| 45 | RH-F4 | RevPromptHonesty.md:60 | w2 sizing residual (32-51 seats) | NA | residual constraint on a later wave, not a landing defect |

Per report: CritC1Counter 3/3/2, CritC2Counter 0/1/1, CritContractFreeze 0/0/4, CritEntryRisk 0/0/6,
CritJunkClasses 7/1/1, CritV3Spec 5/2/0, RevAssimPlan 2/1/2, RevPromptHonesty 1/1/2 (fixed/unfixed/na).

## 4. Counting command, observed output, control

Script `.scratch/r49-Mo49ExecFlaggedFixed/count-flagged.py` (python3, stdlib only, read-only git); defect
list `.scratch/r49-Mo49ExecFlaggedFixed/defects.jsonl` (45 JSONL objects: `{id, report, line, target,
note?, na?, checks?}`). The script reads the list, runs `git diff --name-only <freeze> <landing>`, fetches
each named blob with `git show <landing>:<path>`, evaluates the item's ANDed checks, and prints one line
per item plus the summary.

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ TMPDIR=$PWD/.scratch/r49-Mo49ExecFlaggedFixed \
  python3 .scratch/r49-Mo49ExecFlaggedFixed/count-flagged.py | tail -10
report CritC1Counter.md fixed=3 unfixed=3 na=2
report CritC2Counter.md fixed=0 unfixed=1 na=1
report CritContractFreeze.md fixed=0 unfixed=0 na=4
report CritEntryRisk.md fixed=0 unfixed=0 na=6
report CritJunkClasses.md fixed=7 unfixed=1 na=1
report CritV3Spec.md fixed=5 unfixed=2 na=0
report RevAssimPlan.md fixed=2 unfixed=1 na=2
report RevPromptHonesty.md fixed=1 unfixed=1 na=2
flagged=45 fixed=18 unfixed=9
na=18
rc=0
```

(`na` is printed on its own line so the required `flagged=fixed+unfixed+na` arithmetic is explicit:
18 + 9 + 18 = 45. The full 45-line transcript, including each item's check results, is
`.scratch/r49-Mo49ExecFlaggedFixed/count-run.txt`.)

**Negative control (shown able to fail).** Same command, same list, with the freeze substituted for the
landing:

```
$ python3 .scratch/r49-Mo49ExecFlaggedFixed/count-flagged.py \
    --landing 4387cf94b69ddce455051a1ff38e93795c2e6cde | tail -2
flagged=45 fixed=0 unfixed=27
na=18
rc=0
```

The count tracks the landing diff rather than the list: with no landing, nothing is fixed.

## 5. Behavioural check behind the FIXED verdicts (not only blob predicates)

The script's checks are presence predicates. Four of the five substantive C1 verdicts are additionally
observed by running the landed tool:

```
$ TMPDIR=<scratch> python3 -I -B <scratch>/rev/e4dfff32-tools_mori-pin-check.py \
    --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
    --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
…
pin line=168 kind=digest state=match digest=533218a566030fda… file=tools/mori-round14-regressions.py
pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=match pinned='pass=60 fail=0' observed='pass=60 fail=0'
pin line=939 kind=tally prefix=C2_SELFTEST state=match pinned='pass=13 fail=0' observed='pass=13 fail=0'
PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes
rc=0
Wall time: 92.57 seconds
```

(31 pins ≥ the 26 floor; the tool ran the bound instruments from the lane tree. This single run is the
direct evidence for C1-F2 `rebound=0`, C1-F3 `line=168 … match`, and C1-F4 `unparsed=0`; it does not
re-run the counter.)

### 5a. Five D-class variants against the landed tool

The report `CritJunkClasses` measured eight junk edits against **v2**. The landed v3 was then run on
five rebuilt variants in this seat's scratch, each a copy of the landing `SKILL.md` with exactly the
report's edit (the registry row text is the report's), same CLI as above plus `--skill <variant>`:

```
$ printf '%s\n' D1 D2 D5 D18 D7 | xargs -P 3 -I{} sh -c 'TMPDIR=<scratch>/run-{} \
    python3 -I -B <scratch>/rev/e4dfff32-tools_mori-pin-check.py \
      --rev e4dfff32… --repo <lane> --min-tally-pins 26 --baseline-rev 2d85e33d… \
      --skill <scratch>/var/{}.md > <scratch>/var/{}.out 2>&1; echo "{} rc=$?"'
D1 rc=1   D2 rc=1   D5 rc=1   D18 rc=1   D7 rc=0        (wall 275.38 s)
```

| variant (report edit) | landed v3 | verdict line (observed) |
|---|---|---|
| D1 decoy full digest, decoy path in another cell | `unmet` | `pin line=940 kind=digest state=mismatch digest=e0c4c39b2804 file=tools/mori-pin-check.py` (`mismatches=1`) |
| D2 tally on a continuation line | `unmet` | `pin line=941 kind=row state=hidden row='→ \`PIN_CHECK_SELFTEST pass=999 fail=0\''` (`hidden=1`) |
| D5 empty self-test cell, tally in pinned values | `unmet` | `pin line=940 kind=row state=hidden row='\| r48 junk empty cell \| …'` (`hidden=1`) |
| D18 tally as plain text in a self-test cell | `unmet` | `pin line=940 kind=span state=unparsed reason=tally-outside-backticks` (`unparsed=1`) |
| D7 entry names `mori-source-drift`, self-test binds pin-check at its true tally | **`met`** | `PIN_CHECK=met tally_pins=32 … hidden=0` (rc 0) — the survivor reproduces |

Each run's full line: `… min_tally_pins=26 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492 baseline=yes`.
D1-D18 are `PIN_CHECK=unmet`, rc 1; D7 is `PIN_CHECK=met`, rc 0, which is exactly the UNFIXED verdict the
table gives JC-D7. The three D-class not run here (D3, D4, D8) rest on their own arms inside
`PIN_CHECK_SELFTEST pass=60 fail=0`, itself pinned at `SKILL.md:938` and re-observed by the real run in
§5. The variants were rebuilt from the report's row text against the *landing* `SKILL.md` (981 lines),
not the entering 939-line file the report measured, so they are class reproductions, not byte-identical
replays.

## 6. QUALITY.md criterion wording (draft, text only — the L1 integrates)

Next free id at the round-49 entering tip `b3e3453d`: **129** (`corpus/QUALITY.md` ends at 128 at
`b3e3453d`; `rg -c '^[0-9]+\. '` on the file's criteria sections gives 128, last section
`## Criteria added round 48 — hidden pins, junk next to honest edits, host paths, a located quote per
claim`). Wording, in the style of 125-128:

```markdown
129. **A round counts its own critic flags against the landing, and names every unfixed one.**
    Lesson: `considerthese/2026-10-25.md` suggestion 3 (operator-authored reflection, opened 2026-10-25);
    `corpus/lessons/round-48.md` "Wave 1 — integrated findings". Rationale: round 45 raised a calibration
    flag before `baabc992` landed and shipped it unfixed, and the round recorded no count, so "a critic
    seat changed the outcome" could be neither claimed nor refuted. Round 48's landing fixes 18 of the 45
    labelled findings of its eight wave-1 critic/reviewer reports and leaves 9 unfixed, five of them
    instruments the round nonetheless scored a claim with. Check: `python3 <dir>/count-flagged.py
    --defects <dir>/defects.jsonl` prints `flagged=45 fixed=18 unfixed=9` (and `na=18`) for freeze
    `4387cf94` → landing `e4dfff32`, with one line per item carrying its check results, the defect list
    built by the stated extraction rule (labelled findings only). Shown able to fail: the same command
    with `--landing 4387cf94` (the freeze as landing) prints `flagged=45 fixed=0 unfixed=27`, and a
    single planted row with an ASCII-dot truncated digest or an `(N-line file)` count still prints
    `PIN_CHECK=met` on the landed tool (`w1/CritV3Spec.md` J10, J11). Not covered: whether a landed
    repair is adequate — the checks are presence/absence predicates over committed bytes, not re-runs;
    claim/quote entailment; and any defect the extraction rule did not label.
```

The command's inputs (`count-flagged.py`, `defects.jsonl`) live in
`.scratch/r49-Mo49ExecFlaggedFixed/`; if the L1 keeps the criterion it must copy both to a durable path
and re-point `<dir>` (scratch is cleaned at round end).

## 7. What the script cannot judge (stated plainly)

- **Adequacy.** Every check is a presence/absence predicate over committed bytes: "the landed file
  contains the rule/arm/line" or "the landing diff touched the file". A repair can be present and still
  be wrong; the script cannot tell a rule that closes a class from one that only names it. The
  behavioural checks in §5 and §5a cover 7 of the 18 fixed verdicts (C1-F2, C1-F3, C1-F4 and JC-D1,
  JC-D2, JC-D5, JC-D18) plus the one UNFIXED survivor (JC-D7); the other 11 rest on blob predicates.
- **Extraction.** The item list is hand-extracted from labelled headings. A finding the seat did not
  label (prose bullets, corrections lists, the R-rule matrix) is not counted; the count is a floor.
- **Predicate authorship.** The checks were written by this seat after reading the landed bytes. Each one
  names a literal string or arm from the landing, and the negative control shows the number follows the
  diff, but a reader who disputes a predicate must re-score that item from the table's evidence column.
- **NA boundary.** 18 of 45 items are NA because the report itself disclaims them (precision notes,
  positive verifications, named limits, info, unrealizable). A reader who counts the C2 named-limit
  items (ER-P1..P6, C2-L1) as unfixed would read `fixed=18 unfixed=15`; a reader who also counts the
  freeze observations (CF-O1..O4) would read `fixed=18 unfixed=19`. The primary reading is the one
  stated in §2.
- **Judge independence.** This seat is dispatched, not an independent judge; the counts are evidence for
  the closure, not a verdict on the round.

## 8. Findings

1. **MED — the two frozen counters kept the two defects the round routed to round 49, and the round's
   own claim was scored with them.** `count-c1.py` still names every variant in `--skill` and `TMPDIR`
   (`.ufo/waves/round-48/count-c1.py:238,247`) and still dies on a missing tool or bad `--min-tally`
   (:201-224, :294); `count-c2.py` still keeps `<script>`/`<style>` text in `normalise`
   (`.ufo/waves/round-48/count-c2.py:59-62`). The lesson calls the leak "a limit of the frozen
   predicates" (`corpus/lessons/round-48.md:121-126`), which is accurate about the freeze rule but means
   C1's `met` at `e4dfff32` was produced by a harness a filename-keyed tool could have passed.
2. **MED — the landing records RevAssimPlan F2 as met, but the Solaris refusal still has no flip
   condition.** `corpus/lessons/round-48.md:72` ("Solaris `errno=49` … stays rejected") states a reason
   and no flip, while :131-132 says "F2 (flip conditions for the RHEL PDF and Solaris `errno=49`) is met
   above". The RHEL half is met (:75-76). The round's self-accounting overstates one refusal record.
3. **MED — two CritV3Spec junk classes survive the landed v3 unchanged.**
   `tools/mori-pin-check.py:115` recognises truncated digests only with U+2026, and :118 recognises line
   counts only as `(N lines)`. A registry row that writes `37fd7c24ff52...` (ASCII dots) or
   `(742-line file)` is not parsed as a pin, so a stale assertion in those spellings prints
   `PIN_CHECK=met` — the class the round was built to close (`.ufo/waves/round-48/w1/CritV3Spec.md:42,54`).
4. **LOW — the round-48 census receipt carries no exit code and the landing commits no round-end
   census.** `.ufo/waves/round-48/evidence/census-start.txt` (21 lines, no `rc=`) and the absence of
   `census-end.txt` at `e4dfff32` leave the prompt's §2b.2 before/after pair half-recorded
   (`RevPromptHonesty.md:52`).
5. **LOW — the one D-class the landing did not close is disclosed, not silently dropped.**
   `SKILL.md:960-962` calls the misattributed-verification row "Known survivor, not closed" and QUALITY
   125 repeats "Not covered"; the class stays open at `e4dfff32`.
6. **LOW — the flags that changed the process most are the ones with zero fixable items.**
   CritContractFreeze raised 4 notes and CritEntryRisk 6 pairs, all NA; the entry-risk flag was routed to
   wave 2 as a reviewer checklist and executed there, where `w2/R48CritEntryClaims.md:8` returns
   "BREAKS (class: overclaim from a scoped exemption to a universal)" on row 5. So "did critic seats
   change outcomes" has two answers — 18 of 27 defect-class flags fixed in the landing, and one routed
   flag that found a live defect after it.
7. **INFO — the fixed share by seat:** CritJunkClasses 7 of 8, CritV3Spec 5 of 7, CritC1Counter 3 of 6,
   RevAssimPlan 2 of 3, RevPromptHonesty 1 of 2, CritC2Counter 0 of 1. The report that measured the
   landing's own tool (CritJunkClasses) is the one whose flags the landing acted on most.

## Tooling record

Nothing installed or upgraded; no pacman invocation; no `uv`/`npm`/binary fetch. Instruments used:
`python3` (stdlib), `git` read-only, `xargs`/`rg` for the spot-check. Lane tools ran with
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecFlaggedFixed` (created for this
seat). Writes: this report, `.scratch/r49-Mo49ExecFlaggedFixed/{defects.jsonl,count-flagged.py,count-run.txt,count-control.txt,rev/,var/,run-*/}`.
No credential material read or copied; no host state read (no host tools were needed).
Residue note: the landed tool creates its own `tempfile.mkdtemp(prefix="pin-check-")` directories under
the lane's `.scratch/` even when `TMPDIR` is redirected (observed `git status --porcelain` at 21:53:
220 untracked `.scratch/` entries, this seat's runs among them, plus concurrently running round-49
seats). Round 49's contract already carries `.scratch/` residue as a round-end cleanup item; this seat's
entry (`r49-Mo49ExecFlaggedFixed/`) is part of it and can be removed once the L1 relocates the criterion
inputs.

Report: .ufo/waves/round-49/w1/Mo49ExecFlaggedFixed.md
