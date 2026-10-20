# MistakeScribe — round 13 (wave mori-r13-build)

Seat: `MoriR13.MistakeScribe` (leaf scribe). Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Axes judged: coverage, operability. Milestone: round13 structured scopes and verdict integrity.

Boundaries held: read-only inspection only. No build, test, lint, format, or smoke run. No source,
corpus, LOG, SCORECARD, or MANIFEST edit. No journal output opened; no raw journal MESSAGE, process
environment, or credential material read or quoted. Tool installs: none (read/grep plus read-only
`git status`/`git log`). Only this file is written.

Observation vs inference: anchors below are observed by this seat unless tagged `[INFERENCE]` or
`[UNKNOWN]`. Working-tree state is as of this read: `git status --short` showed
`M tools/mori-silence-cases.sh` (in-flight OracleFix edit, uncommitted) and `?? .ufo/waves/round-13/`;
`tools/mori-census.sh` is unmodified at HEAD `1f07f1d`.

## 1. Sources read

- `AGENTS.md` (5 lines); `corpus/QUALITY.md` criteria 1–25 (`#647A`).
- `corpus/lessons/round-12.md` (Mistakes M1–M26, Gate, Post-review addendum);
  `corpus/lessons/round-12-verifier-spotcheck.md`.
- `SCORECARD.md:594-656` (round-12 section, post-review corrections, planned round 13 at `:639-649`).
- `LOG.md:643-714` (round-12 block and post-review corrections).
- `SHONEN.md:1-8`; canonical seed grep across the fleet (see §3, N4).
- `corpus/knowledge/audit-r11.md` §4 F01–F09 (`:156-164`), D01/D02/D20 (`:196-197`, `:215`), §6 (`:224-228`), Appendix B (`:308-374`), Appendix C (`:376-396`).
- `tools/mori-census.sh`: `:853-911` (probe_journal), `:1469-1506` (authorship window), `:1733-1740` (roll and exit), `:1366-1374` (pointer check).
- `tools/mori-silence-cases.sh` (working tree): header `:41-55`, `verdict_grade` `:552-575`, `assert_case` verdict and rc `:617-649`, shape guard `:1033-1058`, readonly guard `:989-1004`, live pipes `:500`, `:508`, `:618`, `:1029`.
- `.ufo/waves/round-13/dispatch.json:537-540` (this assignment).

## 2. Mistakes table — round 13

`captured-by` names a QUALITY criterion number (`corpus/QUALITY.md`), or `none` with the reason.
No new criterion is proposed here as admitted; "none" rows carry a protocol-level fix for the operator.

| # | class | evidence pointer (path:line or command → output) | captured-by | fix |
|---|---|---|---|---|
| N1 | Two scores of record for one axis. Calibration row reads `5 → 6` ("improved"); the post-review block says "score held at 5, not 6". The row was not marked superseded in place. | `SCORECARD.md:610` (row) vs `:654` (post-review); `LOG.md:711`; `round-12.md:184` | 25 (narrowing recorded as a correction, met in the append) + 9 (the `:610` row not swept to point at the correction) | Next scorecard: each axis has one score-of-record. Any superseded cell gets an appended marker naming the superseding line. L1 counts score-of-record lines per axis; expected 1. |
| N2 | Verdict asserted without a counting command, and verdict/score decoupled. Adjacency: "improved" with score 6 (held), later "unchanged". Calibration: "improved" with score held at 5. The round-12 record itself calls the adjacency verdict "unsupported". | `SCORECARD.md:610`, `:614` vs `:654-655`; `LOG.md:711`; `round-12.md:184` | none. Criterion 20 covers tallies (counted universe), 21 covers the four-value vocabulary; no criterion requires a counting command for a verdict cell. | Operator decision: every verdict other than `unchanged` names a counting command and a score move, or an explicit "held" reason. Not admitted as a criterion here. |
| N3 | Owned-axis operability verdict `unchanged` (score 6) is contested and unresolved in the record. Critic disputes it for want of a budget; the record says "operator to rule"; the verifier adjudication nonetheless carries "unchanged". Measured cost: live census wall time 1884/1830/1930 ms → 4345/4339/4278 ms (≈2.3×) after roster change; no runtime budget declared. Operability is an owned axis for round 13. | `SCORECARD.md:612`; `LOG.md:691`; `round-12-verifier-spotcheck.md` (adjudication line, "Runtime 1.9→4.3s is an explicit cost with no declared budget"); walltime receipt `corpus/evidence/roster-r12-20261019T220912Z-walltime.log` (named in `SCORECARD.md:612`) | none (criterion 10/12 cover baselines and counters, not a runtime budget) | Operator declares a wall-time budget before round 13 counts operability. L1 measures before/after on the same host with the same command form and records medians. Without a declared budget, operability cannot move to `improved` on this evidence; use `unprovable-but-better` only if the operator accepts it. |
| N4 | "Byte-identical to the canonical seed" was asserted without a diff. Six nonblank lines differ (leading indent, and `<name>` substitution). The seed anchor is also cited at three different line ranges. Whether the 4-space indentation is seed content is `[UNKNOWN]` in the record. | `LOG.md:710` (correction); `round-12-verifier-spotcheck.md:17` ("false byte-identical-SHONEN assertion"); seed anchors: `exec-verifier.md:223-231` (`PROTOCOL.md:400-407`), `audit-game-dev-2d.md:163` (`PROTOCOL.md:439-448`), `mori-state.md` C1 (`PROTOCOL.md:417, 423-432`) | 2 (every claim carries a measured anchor) + 9 (anchors must resolve at the carrying commit; three ranges name one seed) | Diff the seed block with the gate's stated extraction rule at the PROTOCOL carrying commit, and record the diff. Rule first on indentation, then claim identity. Keep one seed anchor in any new record. |
| N5 | Non-author gate independence undetermined. The round-12 "non-author" spot-check (W3ReviewMori, 4/4 agree) is described as "fresh agents dispatched by the orchestrator". Audit D20 requires "a named reviewer who did not author the changes and is not a dispatched lane seat". The reviewer name carries the Mori lane prefix. The calibration verdict rests on this sample. | `round-12-verifier-spotcheck.md:3-5`; `round-12.md:93-96` (gate "pending"), `:180-182`; `audit-r11.md:215` (D20); `LOG.md:712` | none (recurrence of M10, which is `none`) | Record the dispatch chain verbatim in the `## Gate` section. L1 rules whether the reviewer qualifies under D20 before any calibration or SHONEN count uses it. Until ruled, it is not counted as independent. |
| N6 | F01 — long-history authorship grade inverted by a producer pipe into an early-exit match. `printf … \| sed … \| grep -Fxq` under pipefail: when the subject line is seen first in a window larger than the pipe buffer, grep exits, sed gets SIGPIPE (141), the `if` takes the sibling branch, and the lane grades `progressing-weak` despite its own commit. Only one live `grep -q`-class pipe exists in the census (this site). | `tools/mori-census.sh:1490-1491` (window), `:1494` (pipe, `subj=1` branch); `audit-r11.md:156` (F01); Appendix B `:308-374` (12,001 lines → `progressing-weak`, `basis=row-C other_authored_commits=12001`, rc 0, stderr 0); lesson `2026-10-15-selftest-grep-sigpipe-race.md:202-203` (141 ≠ 1, cited in `QUALITY.md` criterion 7) | 7 (the criterion exists and was admitted in r12; the production site was not swept — M3 recurrence, the r9 fix covered only selftest) | Capture the sed output once into a variable; match with `grep -Fxq -- "$pat" <<<"$names"` or a pure-bash exact-line test. No live producer into an early-exit match. Gate with negative checks A1, B1–B3. |
| N7 | F02 — oracle verdict check was presence-only. The in-flight edit adds `verdict_grade` (exactly one line, regex, rc consistency) and calls it only from `assert_case`. The shape-invariance guard still uses substring presence and compares the verdict text across two runs. The readonly guard grades no verdict at all. The header states "closes audit-r11 F02" before any integrated measurement. | `tools/mori-silence-cases.sh:41-55` (claim), `:552-575` (new), `:618-619` (caller), `:1035`, `:1047-1048` (shape presence-only), `:1029` (verdict text in shape grade), `:989-1004` (readonly, no verdict); `audit-r11.md:157`, `:376-396` | 8 (channels enumerated; untested channels named as residuals) + 13 (pre-registered expected gradient against the frozen gate SHA) | Route every case, including both guards, through the same final-roll grammar. Remove "closes F02" from the header until L1 measures it, or keep it with the measured run cited. Negative checks A2–A3, B5–B6. |
| N8 | The F02 proof used a mutant wrapper saved only under `/tmp`; the reproduction is not a committed artifact. | `audit-r11.md:378-391` ("Save this wrapper only under `/tmp`") | 23 (a `/tmp` path is never evidence; commit the generator plus digest) | Commit the BANANA/mutant wrapper generator under `tools/` or `corpus/evidence/`, with a digest. L1 runs the committed copy. |
| N9 | Journal class counted by message text in shipped census code — M13 recurrence. Kill/OOM/unit classes are regex counts over journal text. Segfault count adds an unfiltered `-o json` count gated to live hosts (`MORI_FIXTURE` unset), which no fixture reaches. | `tools/mori-census.sh:874-875`, `:881`, `:883` (live-only JSON branch), `:890-891`; `round-12.md:36` (M13) | 15 (criterion exists; the census still violates it) + 17 (the live-only JSON branch is a delivery path the fixtures cannot see; the recipe must say so) | Replace text counts with MESSAGE_ID counts. Restrict JSON output to the needed fields (`--output-fields`) so MESSAGE is not captured. Add a fixture-reachable path for the structured branch. Negative checks B8–B10. |
| N10 | Notice counted as kill, scope not labeled as a unit. The finding `OOM_KILL_JOURNAL` is labeled `class=oom_kill` but counts text matches of "Out of memory / oom-kill / oom_reaper / Killed process" — notices, not kill events. Scope is `user` only; the system scope is absent and not disclosed as unavailable. Kernel-OOM is not visible to the census (FR1, `SCORECARD.md:647-649`). | `tools/mori-census.sh:893-894`, `:897-898`; `round-12.md:42` (M19); `SCORECARD.md:647-649` (planned FR1) | 16 (kill count names unit and scope; scopes never summed) + 17 (the user-only recipe cannot see system-journal kernel OOM — say so) + 24 (an absent surface is disclosed as empty-by-removal or unavailable, never as zero) | Emit notice-unit counts per scope (user, system) as separate labeled fields; never sum them; system unreadable → `unavailable`. No fleet-caused kill attribution from these counts (criterion 18). Negative checks B8–B9. |
| N11 | Pointer rot in our own round-12 record. M2 cites the F01 pipe at `tools/mori-census.sh:1366-1374`. At HEAD that range holds `ps_walk` and the start of `ps_report_closed`; the pipe is at `:1494`. The stale pointer was copied from the audit. | `round-12.md:25` (M2); `tools/mori-census.sh:1366-1374` (no `sed`/`grep -Fxq`), `:1494` (the pipe); `audit-r11.md:156` | 9 (every pointer resolves at the carrying commit) + 4 (errata append-only) | Append a correction block to `round-12.md` naming `:1494` at `1f07f1d`. Do not rewrite the M2 row. Sweep F01 mentions in active records. |
| N12 | Live producer pipes feed match tests in the oracle. `printf … \| grep -m1` and `grep -m1 -E` at the listed sites; `|| true` masks the pipeline rc. Values are captured from grep's stdout, so the verdict is value-safe today `[INFERENCE]`; the literal criterion-7 rule is violated. | `tools/mori-silence-cases.sh:500`, `:508`, `:618`, `:1029`; `grep -c` at `:524` reads all input (no early exit) | 7 | Capture once (`CASE_OUT` already is) and match with here-strings, as `verdict_grade` already does. Negative check A4 before, B4 after. |
| N13 | The drift pin will move with round-13 output. The current pin is aging and red; round-13 changes add journal fields and finding IDs. Any re-pin must be a recorded act, never a way to turn red green. | `round-12.md:38` (M15); `SCORECARD.md:613`; `corpus/evidence/baseline-r10-20261015T2231Z.json` (volatile contract) | 10 (baseline declares volatile set and window; re-pin recorded with a reason) | Before round-13 counts: classify every changed token from `--drift` against the pre-round-13 census. Re-pin only with a recorded reason; keep the old file. Negative check B11. |
| N14 | Gate SHA moves under the fix. Criterion 13 pins the expected tally to a frozen gate SHA, but the oracle is the file being repaired. Both the pre-fix pair (`448f7723…`, 28/28 with BANANA) and the post-fix pair must be recorded, each with its own pre-registered tally. | `SCORECARD.md:644-646` (planned before/after); `LOG.md:713` | 13 | Record the pre-fix run at the HEAD bytes `1f07f1d` (not the dirty tree), then the post-fix run at the new SHA. Both pre-registered before the run. |

## 3. Round-12 score / SHONEN disagreement — reconciled record

Disputed items, as the record states them. Status is the scribe's reading, not a ruling.

| item | record A | record B | status for round 13 |
|---|---|---|---|
| calibration | `SCORECARD.md:610` "5 → 6, improved" | `SCORECARD.md:654`; `LOG.md:711`; `round-12.md:184` "held at 5 — non-author reviewer could not re-derive 6" | Open record conflict (N1). Post-review text is the later statement; it governs only by its own wording. Count 5 until an explicit ruling. |
| adjacency | `SCORECARD.md:614` "improved", score 6 (held) | `SCORECARD.md:655` "unchanged, score 6 held" | Resolved toward "unchanged" by the later correction (N2). Score unchanged. |
| operability | `SCORECARD.md:612` "unchanged", score 6, "operator to rule" | `LOG.md:691` critic: "≈2.3× wall time, no budget"; verifier adjudication: "unchanged" | Open (N3). Owned axis for round 13. Not counted as settled. |
| coverage | `SCORECARD.md:611` "improved", 5 → 6 | — | Not disputed in the record, but no non-author re-derivation of coverage 5→6 is shown `[INFERENCE]`. Round-13 coverage counts start from a base that no non-author has checked. |
| freshness | `SCORECARD.md:613` "unchanged", 5 | — | No dispute. Drift pin already red (N13). |
| SHONEN "byte-identical" | round-12 report's byte-identical seed assertion (report text not read here; named by `round-12-verifier-spotcheck.md:17`) | `LOG.md:710` six lines differ | Corrected in the record (N4). Diff still not recorded. |
| non-author reviewer | `round-12.md:180-182`, 4/4 agree | `round-12-verifier-spotcheck.md:3-5` "fresh agents dispatched by the orchestrator"; D20 `audit-r11.md:215` | Open (N5). |
| SHONEN boxes | four `[ ]` in `SHONEN.md:5-8` | `audit-r11.md:226-228` (no self-attestation) | Unchecked; no box is checked by any round-12 record. Promotion count is 0/4 and must stay 0/4 until a qualifying reviewer rules. |

## 4. F01 and F02 mechanism anchors

F01 (`audit-r11.md:156`, `D01` `:196`):
- Window and branch: `tools/mori-census.sh:1490-1499`. Subject detection is `printf | sed | grep -Fxq` at `:1494`; the `else` takes `sib=1`.
- Mechanism: `grep -q` exits on the first match; sed writes the rest of the window into a closed pipe; SIGPIPE 141; pipefail rc 141; the `if` is false; the subject is lost. Requires the subject line to appear before the rest of a window larger than the pipe buffer. Appendix B used subject-first, 12,001 lines.
- Same class and same lesson as r9 (selftest only). Production was never swept.

F02 (`audit-r11.md:157`, `D02` `:197`, Appendix C `:376-396`):
- Old check: presence of `^MORI_CENSUS:` (`tools/mori-silence-cases.sh` HEAD `:569-585`). A proxy renaming CLEAN/DRIFT to BANANA scored 28/28.
- Census contract: exactly one line `MORI_CENSUS: CLEAN|DRIFT (findings=N drift=M unavailable=U surfaces=S)`, rc 0 CLEAN / 1 DRIFT / 2 setup (`tools/mori-census.sh:352-354`, `:1733-1740`).
- Gap after the in-flight edit: N7 (shape and readonly guards).

## 5. Negative checks L1 must run before any fix count

Run once, after integration, at the bytes stated. Expected outcomes are pre-registered from the
contracts above. Any outcome not matching the pre-registration makes the row it gates `open`.

Pre-fix (run at HEAD `1f07f1d`, census `3da5b098…`, oracle `448f7723…`, before any round-13 commit is applied; use a committed copy or `git show` into a scratch tree, not the dirty working tree):

- A1 — F01 defect reproduces. Long-history fixture, subject line first, 12,000 sibling lines (12,001 in-window). Expected: `SURFACE lane.<lane>: progressing-weak`, rc 0, stderr 0 B. If it grades `progressing`, F01 is not open at these bytes; stop and report. Gates N6.
- A2 — F02 defect reproduces. Appendix C wrapper (CLEAN and DRIFT → BANANA, rc unchanged) against the pre-fix oracle. Expected: `MORI_SILENCE_CASES: matched=28 total=28`, exit 0, stderr 0 B. Gates N7, N8.
- A3 — Guard gap. Same wrapper. Expected: `shape-invariance` and `readonly-no-mutation` both PASS (no verdict grammar applied). Confirms N7's guard part. Gates N7.
- A4 — Source scan, before. `grep -nE 'printf .*\| *grep' tools/mori-silence-cases.sh` → record every hit (N12). `grep -nE '\| *grep -q|grep -Fxq' tools/mori-census.sh` → expect exactly `:1494` (N6). Gates N6, N12.
- A5 — Journal baseline. Record the text-regex lines `tools/mori-census.sh:874-891` and the unfiltered `-o json` line `:883`. Gates N9, N10.
- A6 — Drift baseline. `bash tools/mori-census.sh --drift corpus/evidence/baseline-r10-20261015T2231Z.json`: record the current token list before any round-13 change. Gates N13.
- A7 — Wall-time baseline. Three live runs of the census on this host at `1f07f1d` with the same command form; record each wall time. Gates N3 (requires the operator's budget before the after-run is judged).

Post-fix (run once at the round-13 commit; each row below must match its pre-registered outcome):

- B1 — F01 positive. Subject-first 12,001 window. Expected: `progressing`, rc 0, stderr 0 B.
- B2 — F01 control, both before and after. Subject-last 12,001 window (subject appears after the sibling lines). Expected: `progressing`, rc 0 in both A-era and B-era runs. Confirms the grade is not an artifact of the subject position.
- B3 — F01 negative. Sibling-only 12,001 window, no subject commit. Expected: `progressing-weak` or the pre-registered row-C grade, never `progressing`. Confirms no false progress from the fix.
- B4 — Source scan, after. `grep -nE '\| *grep -q|grep -Fxq' tools/mori-census.sh` → expect 0 hits in the authorship window. `grep -nE 'printf .*\| *grep -m1' tools/mori-silence-cases.sh` → expect 0 hits (N12).
- B5 — F02 mutant set. Each mutant wrapper must yield `matched < total` and exit 1. Pre-registered: each mutant's cases all fail (`matched=0 total=28`) because every case, including both guards, routes through the final roll. Any case that still passes under a mutant is an ungraded channel and F02 stays open for it. Mutants: (m1) CLEAN/DRIFT → BANANA, rc kept; (m2) verdict line deleted; (m3) duplicate `MORI_CENSUS:` line; (m4) CLEAN text with rc 1; (m5) DRIFT text with rc 0; (m6) valid DRIFT line with rc 2; (m7) verdict tail mangled, `(findings=…)` removed.
- B6 — Honest oracle, frozen-SHA pair. Honest census through the post-fix oracle, run twice with pinned `MORI_SHUFFLE_SEED` and `MORI_RUN_NONCE` so stdout is comparable; expected `matched=28 total=28`, exit 0, byte-identical stdout across the two runs. Record the oracle SHA before and after.
- B7 — Selftest tally. `bash tools/mori-census.sh --selftest`. Pre-registered: `PASS (77 cases, 77 passed, 0 failed)` at HEAD plus the exact number of cases the round adds, declared before the run. Any unexplained delta is FAIL (criterion 13).
- B8 — Journal source scan. In `probe_journal`, no `grep -c[i]?E` over journal text for kill/OOM/segfault/unit classes; every `-o json` call restricted with `--output-fields`; zero `COREDUMP_SIGNAL` line-count substitutes for record counts. Expected 0 hits.
- B9 — Journal decoy fixture. Journal text containing kill/OOM words under a non-kill `MESSAGE_ID` → kill and notice counts 0 for those words. A fixture with the notice `MESSAGE_ID` → counted once, labeled `unit=notice scope=user`. Absent system scope → `unavailable`, never `0`. No field sums scopes (grep the emitted finding text for `scope=` pairs; expected none combined).
- B10 — No MESSAGE in output. Plant a sentinel string in a fixture MESSAGE; census stdout must not contain it. Expected: sentinel absent (N9, the "raw journal MESSAGE" rule).
- B11 — Drift pin. `--drift` against the R10 baseline after the change: token list must equal the pre-declared set of changed fields (new journal fields and finding IDs). No re-pin during round 13 unless a reason is recorded and the old file is kept (N13).
- B12 — Wall time, after. Same host, same command form as A7, three runs; record medians beside the operator's declared budget. Operability is not moved without the budget (N3).
- B13 — Regression sentinel, conditional. If any roster code is touched, re-run the r12 roster mutation battery; expected 12 killed / 0 survived / 0 inconclusive (`corpus/evidence/roster-r12-20261019T220912Z-mutation.md`).

Counting rule for the Mistakes table: a row is `fixed` only when its gating checks match the
pre-registered outcome at the carrying commit. `captured-by` changes only when a QUALITY criterion
exists; `none` rows stay `none` until the operator admits a criterion.

## 6. Proposed decisions for L1 / operator (not executed here)

1. Declare the operability wall-time budget before the round-13 operability count (N3).
2. Rule whether W3ReviewMori qualifies as a non-author under D20 before any calibration or SHONEN count (N5).
3. Rule the seed indentation question before "byte-identical" is claimed either way (N4).
4. Decide whether N2 needs a criterion (verdict requires a counting command). Not proposed as admitted here.
5. Append (do not rewrite) the round-12 correction for the stale F01 pointer (N11) and the SCORECARD `:610` supersession marker (N1).

## 7. Not verified, out of scope, open

- No negative check in §5 was run (assignment forbids verification in this seat). Every expected outcome is a pre-registration; where it rests on reading rather than measurement it is `[INFERENCE]` in the claim above.
- Oracle working-tree edit is mid-flight (OracleFix). Line numbers in §2 for `tools/mori-silence-cases.sh` are the working tree as read; HEAD numbers differ (e.g., HEAD `:569-585` vs working tree `:552-575`/`:618`). Re-anchor after the seat finishes.
- The canonical SHONEN seed bytes were located in a fleet `PROTOCOL.md` copy and in `.ufo/waves/round-13/shonen-seed.txt` only through grep; the carrying commit of the seed was not confirmed `[UNKNOWN]`.
- Coverage 5→6 (`SCORECARD.md:611`) has no non-author re-derivation in the record I read; not re-measured here.
- The F01 and F02 reproductions in audit Appendices B and C were not re-run; the audit's reported outputs are cited as recorded.
- No raw journal content, process environment, or credential was read, and none is quoted here.
