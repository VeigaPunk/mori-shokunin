source: S031 — https://man7.org/linux/man-pages/man7/pipe.7.html — man-pages 6.19, “I/O on pipes and FIFOs” (write after every read end closes generates SIGPIPE) and “Pipe capacity” (default 16 pages), opened 2026-10-20; `tools/mori-census.sh` sha256 `3da5b098dc23aeb3e1c31ce82664b24a22c2847a168308a755525593881b3164` (r12 base, wave base commit `6531ac6`): `:7-8,236,329-333,352-353,360-372,503-508,1469,1490-1494,1503,1530-1533,1733-1740,1745-1749,2196-2231,3008-3010`; `tools/mori-silence-cases.sh` sha256 `448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5` (r11 final): `:141,458-495,500-524,535-548,552-618,939-953,976-1006,1016,1074-1080`; `corpus/knowledge/audit-r11.md:156-157` (F01/F02 rows), `:308-374` (Appendix B), `:376-395` (Appendix C)
verified-at: 2026-10-20 — original source analysis at the pinned frozen bytes and S031; L1's appended implementation receipt measures c13df48. Historical figures in sections 1–6 retain audit-r11's own pins; they are not retroactively re-observed.
recheck: python3 tools/mori-round13-regressions.py --jobs 1 --output .ufo/waves/round-13/recheck; source archaeology uses the committed frozen scripts under .ufo/waves/round-13/frozen/ with their inputs.json digests, not the moved numeric line positions in current production files.

# The verdict contract, round 13 — attribution membership and the final roll are two different gates

## Claim

Round 11 filed two defects that survive at the r12 base bytes. **F01**: the production
authorship row decides “is this lane's exact identity present in the launch window?” with
a live producer pipeline whose status is read as the answer, so a *present* identity can
be scored absent and the lane downgraded to `progressing-weak`. **F02**: the oracle grades
lane rows, finding presence and process rc but never the final `MORI_CENSUS: CLEAN|DRIFT`
word itself, so an invalid, duplicated or rc-contradictory roll is still green.

They are one contract failure seen at two ends: the census must produce attribution from
**captured bytes**, and the oracle must read the **whole admitted roll grammar**, not a
prefix. Neither finding is an anti-forgery claim; the classes each check can see are
enumerated in §5.

Derivation: both mechanisms are taken from audit-r11's measured traces (Appendix B, the
quiet long-history fixture; Appendix C, the verdict-word proxy) and re-read in the pinned
source. The traces were not re-executed here.

## 1. F01 — capture membership

### Mechanism, at `mori-census.sh` `3da5b098…`

1. The window's commits are already a capture: `cap env … git log …` stores stdout+stderr
   and rc in `CAP_OUT`/`CAP_RC` (`:503-508`), and `inwin` filters that string to the strict
   `(launch, NOW]` interval with `awk` (`:1490-1491`). Both readers consume to EOF; neither
   can kill its producer.
2. The membership test is the only deciding pipeline (`:1494`):
   `printf '%s\n' "$inwin" | sed -E 's/^[0-9]+ //' | grep -Fxq -- "$lane-shokunin <$lane@shokunin.local>"`.
3. `grep -Fxq` returns at the first exact line and closes its stdin. `sed` is still writing
   whenever the stream exceeds the pipe buffer — pipe(7) gives the default capacity as 16
   pages, 65,536 bytes at a 4 KiB page size (S031, “Pipe capacity”).
4. `sed`'s next `write(2)` meets a closed read end, so the kernel generates SIGPIPE for it
   (S031: “If all file descriptors referring to the read end of a pipe have been closed,
   then a write(2) will cause a SIGPIPE signal to be generated for the calling process”).
   `sed` exits 141.
5. The census runs `set -euo pipefail` (`:236`), so the pipeline's status is the rightmost
   non-zero element: 141. But the pipeline is an `if` condition, so errexit does not abort;
   the status is simply read as “no exact subject line”.
6. `subj` stays 0 and `sib` becomes 1 (`:1492-1498`), which grades row-C
   `progressing-weak` (`:1530-1533`). The `other_authored_commits` field prints `sibn`
   (computed at `:1493`, emitted at `:1532`), the **whole window's** line count.

The inversion is exact: a successful match destroys its own producer, `pipefail` promotes
the producer's death certificate to the pipeline verdict, and the site reads the verdict as
a missing match. This is the same class as the r9 selftest finding
(`corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md`), except the r9 repair landed in
the harness while this site is the production grading path.

### What the audit measured (observation, audit pins)

Appendix B built one exact subject line followed by 12,000 sibling lines and ran unmodified
census bytes with stubbed `git`; expected `progressing`, observed:

```text
SURFACE lane.kagi: progressing-weak (… basis=row-C other_authored_commits=12001; …)
MORI_CENSUS: CLEAN (findings=0 drift=0 unavailable=1 surfaces=7)
RC=0
```

`12001` is the window size (one subject plus twelve thousand siblings), so the field name is
wrong by the subject's own line whenever the match is lost. The audit's own reading: “The
size widens the SIGPIPE window; the fact that ordinary short fixtures pass is not a negative
control for a large-history bug.”

### Why r2–r12 batteries never saw it

Every oracle fixture history is a few commits by construction (`gc()` `:414-419` commits a
fixed small file set per case, with `mori-silence-cases.sh` using the real `git` binary).
Short streams drain before the consumer closes, the pipeline status is 0, and the row is
correct. The defect needs a window larger than the pipe capacity, which no fixture builds.

### The repair principle: capture, then match

- The fact that decides a row must be produced by a matcher whose input is **already
  captured**, so the only process status in play belongs to the matcher.
- Two in-repo precedents do exactly this. The census selftest writes the run's output to
  `$OUT_FILE` once and greps the file (`:2227-2230`), with the r9 rationale spelled out at
  `:2217-2226` (“Once the text is in a file there is no writer left for grep to kill”). The
  drift reader captures and feeds one `sed` pass by here-string, and states its constraint
  as “NO live pipes in this section” (`:1745-1749`).
- The count must stay independent of the membership test: `sibn` remains a full-read
  `awk 'END { print NR }'`, never the number of lines a matcher happened to consume.
- The admitted identity grammar is not the defect and must not be relaxed to dodge it: the
  test is an exact full-line (`-Fx`) match of `"<lane>-shokunin <<lane>@shokunin.local>"`.
  Substring or word-boundary matching would be a different, weaker rule.

This is QUALITY criterion 7 applied to the production path: “No live producer pipe feeds a
match test; capture once and assert over the captured bytes (SIGPIPE 141 ≠ 1).”

## 2. F02 — the roll is read for presence, not for meaning

### What the oracle does at `448f7723…`

| step | line | effect |
|---|---|---|
| capture first `^MORI_CENSUS:` line | `:570` | `verdict=$(printf … \| grep -m1 '^MORI_CENSUS:' \|\| true)` |
| reject setup rc | `:572-576` | `CASE_RC > 1` is a setup FAIL, before any roll reading |
| reject no roll | `:582-586` | empty capture = mid-run crash, never a phantom grade |
| grade state word | `:588-591` | from the `SURFACE lane.<lane>:` row (or aggregate fallback) |
| grade finding | `:592-597` | presence/absence of `FINDING LANE_SILENT` |
| grade rc | `:598-601` | against the case's want, `auto` = rc 1 iff state silent |
| grade nonce | `:602-606` | current run's token must appear somewhere in the output |

The captured roll is used only in failure text (`:600`) and in the differential shape grade
(`:981-982`). No line compares the word to `CLEAN`/`DRIFT`, counts roll lines, parses the
counters tuple, or couples the word to the process rc.

Consequences. Vocabulary is measured by Appendix C; the other three are read directly from
the source lines cited above and were not separately executed here.

- **Vocabulary.** A wrapper that runs the real census, preserves rows, nonce and rc, and
  rewrites only the final word to `BANANA` scores `matched=28 total=28`, exit 0, stderr 0 B.
  It is a proxy, not a zero-logic forger — the rows are real; only the roll is unverified.
- **rc coupling.** A `DRIFT` word with rc 0 passes a CLEAN-want case, and a `CLEAN` word
  with rc 1 passes a silent-want case. The word and the status are graded independently, so
  a contradiction between them is invisible.
- **Cardinality.** `grep -m1` takes the first line; a second, contradictory roll line is
  never read. Shape-invariance cannot cover this: it compares two runs of the *same* SUT
  (`:1002-1004`), so a consistently wrong word passes both sides.
- **Guards outside `assert_case`.** The read-only check hashes the fixture tree and tests the
  nonce only (`:939-953`); `shape_has_verdict` is a substring test for `MORI_CENSUS:`
  (`:985`). Neither reads the roll grammar.

### The asymmetry worth naming

The census's own selftest is stricter than its outside oracle: each case asserts
`^MORI_CENSUS: ${wverdict} ` against a captured file (`:2230`). So the producer already had
an internal check on the word while the external check did not — and even that internal
check counts nothing (`grep -qE` matches any line, so a duplicate roll survives). The r13
repair is therefore not a new bar; it is the bar the census already published in its usage
block (`:352-353`) applied from outside.

## 3. The admitted roll grammar

| element | admitted form | producer anchor |
|---|---|---|
| marker and word | `MORI_CENSUS: ` followed by exactly `CLEAN` or `DRIFT` | `:7-8`, `:352`, `:1733` |
| counters | `(findings=N drift=M unavailable=U surfaces=S)`, decimal integers, no trailing text | `:1733` |
| cardinality | exactly one such line per live run (the summary is printed once, at the end of `run_census`) | `:1729-1734` |
| rc coupling | `CLEAN ⇒ 0`, `DRIFT ⇒ 1`; rc 2 is setup/usage and carries no roll | `:353`, `:1736-1740`, `:358` |
| derivation | only `warn`/`crit` findings flip `ROLL`; `info` never does | `:329-333`, `:360-372` |
| namespace | `MORI_CENSUS_SELFTEST:` is the harness tally and is **not** a roll; `--drift` prints `MORI_DRIFT:` | `:3008-3010`, `:1994,1997,2003` |

Two derived invariants follow from the derivation row and are labelled inference, not
measurement: a `DRIFT` roll implies `drift ≥ 1`, and a `CLEAN` roll implies `drift = 0`,
because `emit_finding` increments `N_DRIFT` exactly when it flips `ROLL`. A roll check can
enforce these without recomputing findings; whether it should is a scope decision, not a
source fact.

A repair must keep four properties that are easy to lose:

1. Both arms stay live. The oracle has rc-1 wants (e.g. `assert_case silent-open silent 1 1`
   at `:645`), so a check that only accepts `CLEAN` fails its own suite.
2. “Missing roll” stays the crash signature. A run that never reached the summary must fail
   as a crash, not be graded as an absent-but-consistent roll.
3. rc 2 stays setup. A crash is never DRIFT (`:572-576`), and the repair must not reorder
   that gate after roll parsing.
4. The prefix must not become a substring. `^MORI_CENSUS:` deliberately excludes
   `MORI_CENSUS_SELFTEST:`; a looser match would accept the harness tally as a verdict.

## 4. Scope coupling with the round's structured counts (C1)

The roll is derived from findings, not from counters: only an explicit `emit_finding … warn|crit`
flips it (`:360-372`). New structured journal counts may therefore change SURFACE/FINDING
payloads and must not:

- introduce a third word or a second `MORI_CENSUS:` line (that would break cardinality);
- move the roll as a side effect of a counter being non-zero, with no named severity;
- change the meaning of a count cell from notice units to kill units.

Notice counts are unit notices, never victim counts, and user and system journal scopes are
never summed (`kill-classes-by-message-id-r12.md`; QUALITY criteria 15–16). A notice count
belongs in the observation text of a SURFACE or FINDING line; the roll moves only when a
named severity says so.

## 5. Tested class limitations

These bound what an F02 repair can claim, and they bound this note.

| class | visible to the repaired oracle? | basis |
|---|---|---|
| substituted roll word (`BANANA`) | yes — vocabulary | Appendix C trace |
| roll word contradicting rc | yes — coupling | `:598-601` + `:1736-1740` |
| two or more roll lines | yes — cardinality | single emission at `:1733` |
| malformed or truncated counters tuple | yes — whole-line grammar | `:1733` |
| no roll at all | yes — crash signature retained | `:582-586` |
| counters that are well formed but untrue | **no** — no recomputation from emitted FINDING/SURFACE lines | oracle grades declared wants |
| F01's size-dependent wrong grade | **no** — fixtures' windows are short; the defect needs > pipe capacity | §1 |
| `--selftest`, `--pin`, `--drift` modes | **no** — the oracle drives `bash "$CENSUS"` with no arguments (`:458-495`) | mode contract `:352-353` |
| live host and journal delivery paths | **no** — journalctl/tmux/df are stubs, cgroup files are fixtures | oracle header `:11-30` |
| duplicate roll inside the census's own selftest | **not closed there** — `grep -qE` over a file matches any line | `:2230` |

The `yes` rows state the coverage the repair must provide, not behavior verified here; the
in-flight script is not measured in this note (§6).

## 6. Pointer status

This note binds to the base SHAs named in the provenance header. The audit's own F01/F02
anchors (`census :1366-1374`, `oracle :569-585`) are at its r11 pins; the same constructs sit
at `:1490-1494` and `:570` after r12 edits, and the quoted expressions match. Post-repair
script SHAs, line anchors, the measured case tally and the receipt pointers are L1's to add
after integration; **no final count is asserted here**, and no figure in this note was
produced by running either tool.

## What this changes for mori

- Treat `MORI_CENSUS:` as a contract with four parts — word, tuple, cardinality, rc — and
  cite §3 when deciding whether a green run means anything.
- Before a r13 repair is cited, the oracle's own green must be read as “rows + rc + roll
  grammar”, not “rows + rc”. A pre-r13 green never meant the roll was valid.
- When a membership test decides attribution, capture first and match second; a pipeline
  status is not a match result.
- Counts do not create verdicts: a counter can be reported without moving the roll, and a
  notice is not a kill.

## Delivery paths this cannot see

- S031 explains SIGPIPE generation and pipe capacity; it does not model bash's pipeline
  status rule, the `if`-context errexit exemption, or the fill timing that makes the
  misgrade deterministic above capacity. Those are the r9 lesson and the in-repo comments,
  not the man page.
- No live lane was measured. This note does not claim any real lane's window currently
  exceeds the pipe capacity, nor that a large history always produces the defect — only
  that the audit reproduced it at a measured size on a synthetic history.
- The oracle is graded as a black box. Nothing here claims intent, and nothing here says how
  a repair is implemented; the capture/here-string shape is the principle, not a diff.

## [UNKNOWN]

Whether the live fleet presently has a lane whose post-launch window is large enough to open
the F01 window; whether any wrapper outside `/tmp` has ever substituted a roll word; and what
the counters tuple would show if compared against the emitted FINDING/SURFACE lines. None of
these was established here.

## Measured implementation — round 13

The source analysis above is historical at its named hashes; L1 measured the
repair at c13df48. Receipt:
`.ufo/waves/round-13/evidence/regressions-accepted/evidence.json`,
command `python3 tools/mori-round13-regressions.py --mutation both --jobs 1
--output .ufo/waves/round-13/evidence/regressions-accepted` → 19 passed,
2 mutation-red, exit 0.

- F01: exact subject followed by 12,000 siblings is `progressing/row-A`;
  sibling-only control remains `progressing-weak/row-C`, count 12,000.
  Reverting only grade_lane reproduces row-C with 12,001 records.
- F02: honest oracle remains 28/28. BANANA, duplicate, missing, trailer and
  verdict-first proxies each score 0/28, exit 1. CLEAN-only/DRIFT-only tally
  or rc mutations correctly preserve their unaffected cases: 7/28 or 21/28,
  never a green suite. They are not asserted to reject every unaffected case.
  Reverting only verdict validation makes BANANA green 28/28 again.
- Final rolls must be terminal, unique, grammatically complete and rc-consistent;
  CLEAN has drift=0 and DRIFT has a positive canonical decimal drift count.
  Arbitrary finding-total corruption, aggregate fallback/registry-count
  vacuity, duplicate lane rows and full adaptive forgery remain outside this
  demonstrated fix; audit debt D02 is only partially addressed.

The new evidence harness initially rejected correct C1 output because of its
own schema and expected-fixture mistakes. Both red runs remain committed;
LOG.md round-13 and lesson M7 identify the exact corrections. No production
census/oracle bytes changed to accommodate an inaccurate expected result.
