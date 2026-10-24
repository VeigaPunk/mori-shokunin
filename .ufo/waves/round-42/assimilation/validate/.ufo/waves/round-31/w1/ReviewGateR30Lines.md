# mori round 31 wave 1 — ReviewGateR30Lines: round-30 detector defects carried by clause 6

Seat: MoriR31.ReviewGateR30Lines (leaf; no subagents used). Scope: the two kept detectors
`writer-tool-source-citation` and `writer-tool-run-output` of `.ufo/waves/round-30/check-blind-wave.sh:76-162`.
Round-31 rule clause 6 carries both unchanged into `tools/mori-blind-check.sh`
(`.ufo/waves/round-31/rule-text.md:22`), so every defect below is inherited verbatim. Contract P-C2 demands
exact hit sets on the 16 frozen fixtures and says later freezes depend on this gate
(`.ufo/waves/round-31/contract.md:59-62`, `:25`), so false positives and false negatives both flip future
counted outcomes. The files-opened detectors are out of scope (routed D1, `corpus/lessons/round-30-verifier-spotcheck.md:176-178`).

## Method

Sandbox per the gate's own selftest setup (`check-blind-wave.sh:190-196`): `git init` a scratch repo, commit
synthetic briefs, run the committed round-30 gate bytes against that rev. Harness kept at
`/fast/scratch/hyaku/mori-r31/ReviewGateR30Lines/repo` (scratch dir; lane untouched, read-only git only).

```sh
cd /fast/scratch/hyaku/mori-r31/ReviewGateR30Lines/repo
bash /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-30/check-blind-wave.sh \
    <rev> .ufo/waves/round-31/w1 '^B[0-9]+\.md$'
```

- Baseline: `check-blind-wave.sh --selftest` → `PASS`, exit 0, at the entering tip; the script behaves as pinned.
- Commit 1 (B1–B10, rev `6d39e4b0b731dd9897604b4c1dc8094d6c737d7e`): `scanned=10 blind_violations=5`, exit 1 —
  exactly the 5 predicted lines, no others.
- Commit 2 (B11–B12): `scanned=2 blind_violations=1`, exit 1 — B11 silent, B12 hit at line 5, as predicted.
- Every brief carries `## Files opened` / `- .ufo/waves/round-30/rule-text.md` so the (out-of-scope) list
  detectors stay quiet and only the two kept detectors can fire.

## Findings by severity

### F1 HIGH — run-output detector fires on quoted rule text and idle prose (false positive)

Mechanism: any line matching `tool_run_re` (`check-blind-wave.sh:82`: `tool run/output/result`, `run tool`,
or the tool filename) arms a pending window of 8 (`:139`); a verdict token seen in the window arms
`seen_run_verdict` (`:145`); the next `exit [012]` line fires (`:146`). `--inputs` arms a second window where
any verdict-or-exit line fires (`:138`, `:143`). Nothing distinguishes pasted output from prose about the rule.

- B1 (verdict in a quoted rule sentence): heading `## Tool output (rule paraphrase, nothing ran)` arms the
  window; `The rule says the tool prints KILLERS_QUIET ...` arms the verdict; `and a quiet probe must exit 0.`
  fires. Output: `.ufo/waves/round-31/w1/B1.md:8:writer-tool-run-output`. Real defect: an honest writer who
  paraphrases the verdict clause under a "tool output" heading is accused. The rule text itself contains
  "`KILLERS_QUIET`, exit 0" (`.ufo/waves/round-30/rule-text.md`, verdict clause 3), so verbatim quoting hits
  the same shape.
- B2 (`--inputs` prose): `We re-ran the fixture harness with --inputs cases.json once, for comparison only.`
  arms `pending_inputs`; eight lines later `an idle wrapper may exit 0 without printing anything.` fires.
  Output: `B2.md:8:writer-tool-run-output`. Real defect: no output was quoted.

### F2 HIGH — one unclosed json fence silences the run-output detector for the rest of the file (false negative)

Mechanism: a ```json / ~~~ json fence inside a `case` heading latches `in_case_json=1` (`:109-110`); only a
fence line clears it (`:105-108`); H2 processing (`:112-118`) runs while latched but never clears the latch,
and the latched state forces `protected=1` (`:105-108`), skipping the whole run-output block (`:136-151`).

- B7: `## Cases`, ```json, one case line, then a real pasted transcript
  (`## Tool run output (pasted)` / `KILLERS_QUIET` / `exit 0`) with the fence never closed. Output: no hit at
  all. Real defect: a stray or malformed fence line anywhere in a case section disarms the tripwire for the
  entire remainder of the report; a blindness-violating output needs no cleverness, only a missing fence.

### F3 MEDIUM — citation detector fires on ordinary prose (false positive)

Mechanism: `tool_header_re` (`:77`) is `tool lines?` followed by space/colon/pipe, or `tool: N` — no
`mori-oom-killers.py` needed; the fire at `:121-123` is not guarded by `protected`.

- B3: `Counting tool lines of stderr across the fixture runs showed nothing unusual;` →
  `B3.md:4:writer-tool-source-citation`. Real defect: "tool lines of stderr" cites no source.
- B4: `Our packaging tool: 4 fixtures were regenerated this wave; the helper gained no tool lines.` →
  `B4.md:4:writer-tool-source-citation`. Real defect: "tool: 4" is a label with a count.

### F4 MEDIUM — citation detector misses comma/paren citation styles (false negative)

Mechanism: `cite_file_re` (`:76`) requires `mori-oom-killers.py` to be immediately followed by `:N` or
`lines N`; a comma or a word between the filename and the line number breaks both alternatives.

- B5: `the counted rule lives at mori-oom-killers.py, line 42; we read the file tools/mori-oom-killers.py
  around line 42` — an open, explicit admission of a source read with line numbers. Output: no hit. Real
  defect: the files-opened allowlist does not catch it either, because nothing forces the source file into the
  list (B5 lists only rule-text.md and passes the list checks); the writer escapes both detectors with a comma.

### F5 MEDIUM — pasted transcript under a heading without the tool vocabulary is invisible (false negative)

Mechanism: the verdict+exit pair needs `pending_tool > 0`, armed only by `tool_run_re` vocabulary (`:82`, `:139`).

- B6: `## Console` / `KILLERS_QUIET` / `exit 0` — a verbatim two-line transcript, no "tool" word anywhere.
  Output: no hit. Real defect: the tripwire keys on heading vocabulary the writer controls; the selftest's own
  positive shape (`Tool run output:`, `check-blind-wave.sh:193`) shows the design assumption, and one word of
  renaming defeats it.

### F6 LOW — case asymmetry between the verdict and exit matches (false negative)

Mechanism: `verdict_re` is tested against the raw `$line` (`:141`, uppercase-only tokens) while `exit_re` is
tested against `lower_line` (`:142`); both the window pair (`:144-146`) and the same-line rule (`:148`) need a
verdict.

- B8: `Per the tool output convention a quiet run prints killers_quiet and would exit 0` — one line that
  matches `tool_run_re` and `exit_re`, but the lowercase verdict escapes. Output: no hit. Real defect
  (inconsistency): the citation detector lowercases its input (`:121`) but the run-output verdict does not, so
  lowercase-quoted output passes.

## Per-brief log (all lines observed, none inferred)

| Brief | Shape | Gate output | Judgment |
|---|---|---|---|
| B1 | rule quote: KILLERS_QUIET then "must exit 0" under "Tool output" heading | `B1.md:8:writer-tool-run-output` | real FP (F1) |
| B2 | `--inputs` prose then "may exit 0" 4 lines later | `B2.md:8:writer-tool-run-output` | real FP (F1) |
| B3 | prose "tool lines of stderr" | `B3.md:4:writer-tool-source-citation` | real FP (F3) |
| B4 | prose "tool: 4 fixtures" | `B4.md:4:writer-tool-source-citation` | real FP (F3) |
| B5 | "mori-oom-killers.py, line 42" comma citation | no hit | real FN (F4) |
| B6 | pasted KILLERS_QUIET + exit 0 under "## Console" | no hit | real FN (F5) |
| B7 | unclosed ```json fence in Cases, transcript below | no hit | real FN (F2) |
| B8 | lowercase "killers_quiet ... exit 0" on a tool-output line | no hit | real FN (F6) |
| B9 | `mori-oom-killers.py:42` inside a protected derivation table | `B9.md:6:writer-tool-source-citation` | intended, not a defect |
| B10 | closed case-json fence with expect verdicts + selftest marker | no hit, exit path clean | control, matches selftest carve-out |
| B11 | `--inputs` line, "exit 0" 9 lines below | no hit | window expiry works; effective window is the 7 following lines (same-line decrement, `:152-153`) |
| B12 | `mori-oom-killers.py:42` inside a protected case-json fence | `B12.md:5:writer-tool-source-citation` | intended: citations are checked everywhere (`:121-123` outside the protected guard) |

B9/B12 are the correct behavior for a blindness gate: any citation of the tool source is evidence of access,
wherever it appears; the run-output detector, by contrast, is deliberately silenced in derivation tables and
case-json fences (the selftest pins both: CaseR30a fires, CaseR30z's table must not — `check-blind-wave.sh:192,197,211`).

## Inheritance statement

Clause 6 (`.ufo/waves/round-31/rule-text.md:22`) keeps both detectors unchanged, so F1–F6 carry into
`tools/mori-blind-check.sh` unless the L1 amends clause 6. F1 and F2 are the ones most likely to flip a
future freeze: F1 accuses honest briefs (counted `blind_violations` rises, exit 1 on an honest wave); F2 lets
a real violation through silently. F3/F4 are one-line regex tightenings (`tool lines?` → require the tool
filename or a line-number context; allow `,`/`(` between filename and number); F5/F6 need a decision about
how aggressive the tripwire should be, not just a regex fix. These are carried limits, not part of C2's
frozen predicate — the 16 frozen fixtures decide round-31's own counted value.

## Residual risk and verification gaps

- I did not inspect the 16 frozen fixtures in `.ufo/waves/round-31/c2-fixtures.json` for F1–F6 shapes; whether
  round-31's own counted run is affected is open. The defects are established against the detector bytes
  themselves, which clause 6 freezes.
- Window boundary tested only at 4 lines (fires, B2) and 9 lines (cold, B11); the 7-line effective cutoff is
  read from `:152-153`, not separately run. `~~~` fences, both detectors firing on one line, and
  verdict/exit tokens inside files-opened entries are untested.
- Only the round-30 gate bytes at the round-31 entering tip were exercised (selftest PASS pins them); I did
  not diff them against the round-30 wave commit that originally ran.
- The real round-29/30 writer corpora were not scanned for accidental F1/F3 shapes; the observed round-30
  results agree with the selftest's exact-set assertions.

## Process notes

- Bounds kept: writes only to this report and `/fast/scratch/hyaku/mori-r31/ReviewGateR30Lines/`; lane touched
  read-only; every command under `timeout` 120 s; no processes left running (all runs completed inline; the
  selftest removed its own tempdir via its EXIT trap).
- Tooling directive: nothing installed or updated (bash, git, coreutils sufficed).
