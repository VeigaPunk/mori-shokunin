# EvidenceScribe — round 13 wave report (mori-r13-build)

- Seat: `MoriR13.EvidenceScribe` (scribe, leaf). Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
- Assignment: read the report contract and the prior round report; propose the round-13 evidence inventory and an ordered report skeleton. No final report, no LOG edit, no placeholder presented as evidence.
- Pinned state observed by this seat: HEAD `6531ac6` (2026-10-19T22:05:16-03:00). `tools/mori-census.sh` HEAD = working tree, sha256 `3da5b098…`. `tools/mori-silence-cases.sh` HEAD sha256 `448f7723…` (matches the oracle hash in receipt `corpus/evidence/roster-r12-20261019T220912Z-oracle.log`); working tree is **dirty and in flight** (mtime 2026-10-20 01:08 −0300, sha256 `a8824408…`). Also dirty: `LOG.md` (round-13 entry at `:722`), `SHONEN.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`; untracked `.ufo/waves/`. Every oracle anchor below is HEAD-pinned unless marked *working tree*. Anchors move while siblings edit; L1 must re-resolve them at the freeze commit (QUALITY 9).
- Scope boundary: no builds, tests, census or oracle runs, no edits outside this file. Two read-only host queries were made (listed in E10), counts only, no `MESSAGE` text printed.
- Tool installs or updates by this seat: **none**.

## 1. Report contract (read)

| Source | What it requires |
|---|---|
| `templates/round-prompt.md` §4 (fleet root) | Round report at `.ufo/reports/round-<N>/<lane>.md`; ordered sections: Work performed (names the 1–3 claims first), Landed changes (each tied to a LOG entry and a commit hash), Before→after measurements (one per claim, counting command, commit), Sources & frontier, Trend verdicts (`expansion`, `quality`, `discernment`; four values; no scalar), SHONEN (one line per box). Marker rule: a contentless report fails the round. |
| `PROTOCOL.md:146-149` | Path `.ufo/reports/round-<N>/<id>.md`; a report under any other name does not satisfy the contract. |
| `PROTOCOL.md:155-168` | `SHONEN` heading, one `[x]`/`[ ]`/`[~]` line per box; `[x]` only with a named non-author verifier. |
| `PROTOCOL.md:169-175` | Mission open >2 driver ticks: report must say *progressing* or *silent*. |
| `PROTOCOL.md:185-206` | Lane report lands last; cites the lane HEAD; checkable commit-hash citation required for `ok`. |
| `AGENTS.md:4` | Every change appends a LOG.md entry with its motivating evidence. |
| `corpus/QUALITY.md` 1–25 (committed); 26–28 (working tree, uncommitted, `:64-66`) | Admission bar. Criteria cited below: 4 (errata append-only), 7 (no live producer pipe into a match), 9 (pointers resolve at the carrying commit), 13 (pre-registered expected gradient), 15 (journal class counted by MESSAGE_ID or trusted field, never text), 16 (kill vs notice unit and scope, never summed), 17 (delivery paths not seen), 20 (tallies recomputed from delivered artifacts), 21 (four verdict values only), 22 (timestamp ≤ commit), 25 (scope narrowing is an explicit correction). |
| `SCORECARD.md` contract | Move log with before/after, counting command, evidence pointer, measured commit. |

## 2. Prior round report (read)

- Latest lane report in this checkout: `.ufo/reports/round-11/mori-goalwave.md` (r2–r11 use the `mori-goalwave.md` name; the protocol name is `mori.md`; see E16).
- Round-12 fleet report, the one the protocol names: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-12/mori.md` (203 lines). Sections in order: Work performed (`:9`), Landed changes (`:71`), Before → after measurements (`:84-120`), SHONEN (`:122-127`), Sources & frontier (`:129-141`), Mistakes (`:143-156`), Trend verdicts (`:158-171`), L0 questions (`:173-176`), Integrator notes (`:178-191`), Post-review fixes (`:193-203`).
- Facts carried into round 13:
  - Round-12 self-verdicts: depth 4→5 improved; calibration 5→6 improved, ledger score held at 5 because the non-author could not re-derive 6; coverage 5→6 improved; operability unchanged at 6 with cost named; freshness unchanged at 5; adjacency 6 held.
  - Non-author sample: `corpus/lessons/round-12-verifier-spotcheck.md` (table): 4/4 agree, one reviewer (W3ReviewMori), recorded as a single sample, not a universal proof.
  - Harm watch: live census wall time 1.9 s → 4.3 s, no declared budget (`:101`, `:176`, open L0 question).
  - Sentinel LOW items routed to round 13 (`:186-189`): (a) `COREDUMP_SIGNAL=11` JSON read without `--output-fields`; (b) `MORI_ROSTER_LANES` tokens not shape-validated; (c) the surface provenance string `cmd=journalctl --user -b --no-pager` prints `MESSAGE` if re-run.
  - Round-12 mistake rows M13 (text count vs structured field), M19 (kill vs notice, scopes summed), M21 (delivery paths), M3 (SIGPIPE, 141 ≠ 1) in `corpus/lessons/round-12.md`.

## 3. Round-13 evidence inventory

Status key: **OBS** = observed by this seat at the pinned bytes above; **AUD** = carried from audit-r11 or a prior receipt, not re-run here; **PLAN** = to be produced by round-13 seats or L1. A PLAN item is not evidence until its receipt exists.

| ID | Item | Observed value / pointer | Status | Bears on |
|---|---|---|---|---|
| E01 | Pins at freeze | HEAD `6531ac6`; census sha256 `3da5b098…` (HEAD = working); oracle HEAD `448f7723…` vs working `a8824408…` (in flight) | OBS | all |
| E02 | F01 mechanism | `tools/mori-census.sh:1490` window filter (`awk`); `:1494` `printf … \| sed … \| grep -Fxq -- "$lane-shokunin <…>"` under `pipefail`; `grep -Fxq` exits on the first match, so a large `inwin` can SIGPIPE the producer and read as "no subject" (rc 141 ≠ 1). Audit pointer `:1366-1374` is stale (bytes at `d7710981`; roster change moved the block to `:1469-1494`). | OBS | C2 / F01 |
| E03 | F01 defect evidence | `corpus/knowledge/audit-r11.md:156` (F01) and Appendix B `:308-374`: 1 subject line + 12 000 siblings → `progressing-weak … other_authored_commits=12001`, rc 0. Measured at `d7710981`, not at HEAD. | AUD | C2 / F01 |
| E04 | F02 mechanism | HEAD `tools/mori-silence-cases.sh:570` `verdict=$(printf … \| grep -m1 '^MORI_CENSUS:' \|\| true)`; `:580-583` only tests the verdict for emptiness; rc expectation is derived from observed lane state in `assert_case` (`:558-617`); `shape_observe` `:981` repeats the `grep -m1` pattern. Nothing checks the roll word, its count, or roll↔rc agreement. | OBS | C2 / F02 |
| E05 | F02 defect evidence | `audit-r11.md:157` (F02) and Appendix C `:376-396`: wrapper replacing `CLEAN`/`DRIFT` with `BANANA` → `matched=28 total=28`, exit 0, stderr 0. | AUD | C2 / F02 |
| E06 | Text-class counts in the journal probe | HEAD `tools/mori-census.sh:855-867` reads `--user -b --no-pager` into `$text`; `:874` `grep -ciE 'Out of memory\|oom-kill\|oom_reaper\|Killed process'`; `:875` `'status=9/KILL\|…\|SIGKILL'`; `:881` `'segfault\|general protection fault'`; `:890` `'Failed with result\|Unit entered failed state'`. All are MESSAGE-text counts (criterion 15; M13). | OBS | C1 |
| E07 | Structured arm | `:882-885` JSON count `COREDUMP_SIGNAL=11` counts lines containing the field name, with no `--output-fields`; it is skipped entirely when `MORI_FIXTURE` is set (`:882`), so the selftest never exercises it. | OBS | C1 |
| E08 | Scope coverage | Census reads the user journal only (`:855`, findings `scope=user` at `:894`, `:902`). No system scope (audit D08, `audit-r11.md:203`). | OBS | C1 |
| E09 | Provenance string | Surface row `emit_surface journal … cmd=$cmd` at `:911`, where `cmd` = `--user -b --no-pager`; re-running it prints `MESSAGE` (round-12 report `:189`). | OBS | C1 |
| E10 | Kernel records carry no `MESSAGE_ID` | Read-only count this seat: `journalctl -k -b all -q -o json --output-fields=MESSAGE_ID \| grep -c '"MESSAGE_ID"'` → **0**; `… \| wc -l` → **48173**; rc 0. No `MESSAGE` printed. Consequence: kernel victim records cannot be counted by MESSAGE_ID; criterion 15 bars text counting of them. | OBS (host, one boot scope `-b all`) | C1 design |
| E11 | Admitted note uses a text match for the kernel count | `corpus/knowledge/kill-classes-by-message-id-r12.md:3` (recheck line) and `:14` ("Kernel unit": `journalctl -k -b all -q --grep='…Killed process…'`). `--grep` matches `MESSAGE` text inside journald; output is MESSAGE-free, but the count is a text class. Contradicts criterion 15 for that 5-count. | OBS | C1 / criterion 15, 4 |
| E12 | Label conflict | Round-13 spec (CensusFix) and `SCORECARD.md:639-649` call `fe6faa94…` "kernel OOM notices"; `SKILL.md:30` says "unit hit by kernel OOM"; the catalog text (S013 `systemd.catalog.in:604-605`) and the knowledge note describe a per-unit notice emitted by systemd, not a kernel record. Criterion 16 requires the unit to be named. | OBS | C1 / criterion 16 |
| E13 | Selftest stubs cannot express the new query | Dispatcher `.dispatch` (`tools/mori-census.sh:2030-2050`): `journalctl) out_of journal` ignores arguments, so every query returns the same file. Journal fixtures `:2475-2479` (text-only `kernel: Out of memory: Killed process 4242` → DRIFT) and `:2676-2679` (empty → CLEAN). New scope/class queries need an argument-aware stub. | OBS | C1 / C2 selftest |
| E14 | Live-pipe match sweep | Census: one live pipe into an early-exit grep (`:1494`); `:2218` is a comment naming the replaced idiom. Oracle (working tree, in flight): four `printf … \| grep -m1` sites (`:517`, `:525`, `:618`, `:1038`); HEAD verdict sites `:570`, `:981`. HEAD line numbers for `:517`/`:525` were not checked. Criterion 7 sweep = 1 census site + oracle sites. | OBS | C2 / criterion 7 |
| E15 | Stale scorecard row | `SCORECARD.md:10` coverage **5** (`round 1`) vs move log `:611` "coverage 5 → 6" and saturation `:635-636` "owned axes sit at 6 and 6". Top table is not synced. | OBS | criterion 20 / M5 class |
| E16 | Unresolved pointer | `LOG.md` round-12 entry cites `fleet-ledger/.ufo/reports/round-12/mori.md`; the `fleet-ledger/` directory does not exist here. The round-12 report resolves at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-12/mori.md`. Round-13 report must cite the resolving path. | OBS | criterion 9 |
| E17 | Uncommitted criteria cite a missing lesson | `corpus/QUALITY.md:62-66` (working tree) adds criteria 26–28 citing `lessons/round-13.md#M1–M3`; that file does not exist yet. Criteria and lesson must land together or the citation is withdrawn. | OBS | criterion 9 |
| E18 | Drift baseline already red | `corpus/evidence/drift-r12-20261019T2204Z-classification.md` and `drift-r12-20261019T2230Z-after-roster.log`: round 12 left the r10 baseline red (`--drift` names 14 new lane rows and roster fields); "No re-pin (planned r13)" (LOG). Any round-13 change to census output, finding ids or the `cmd=` string adds to that red set. | OBS (receipts) | freshness, C1 |
| E19 | Harm watch baseline | Round-12 live wall time after: 4345 / 4339 / 4278 ms (3+3 interleaved, `corpus/evidence/roster-r12-20261019T220912Z-walltime.log`). Structured system-scope queries add journal calls; the same method must be re-run. | AUD | operability harm rule |
| E20 | Inherited receipts | Selftest 77/77 and oracle 28/28 at `448f7723…` (`roster-r12-…-selftest.log`, `…-oracle.log`); mutation battery 12/12 killed at `3da5b098…` (`roster-r12-…-mutation.md`). | AUD | regression floor |
| E21 | Non-author status | Round-12 spot-check: one reviewer, 4/4 agree. Round-13 non-author check is the orchestrator's post-landing act; none recorded yet. SHONEN boxes: none checked in any round. | AUD / pending | discernment, SHONEN |
| E22 | Round-12 hygiene items | `SHONEN.md` seed pointer `.ufo/waves/round-13/shonen-seed.txt` resolves at the fleet root (378 B). Round-12 SHONEN correction (criterion 28) is in the working tree. | OBS | criterion 28 |

### Planned evidence (PLAN; none exists yet)

| ID | Receipt to produce | Pre-registered expectation (criterion 13) | Owner |
|---|---|---|---|
| P01 | F01 at HEAD census, long-history fixture (Appendix B generator), sizes 1 / 100 / 12 000 sibling lines, repeated N times with N recorded | HEAD: exact subject first ⇒ `progressing-weak` (defect baseline). After: `progressing`; sibling-only ⇒ `progressing-weak`; small-history control unchanged | RegressionHarness, CensusFix |
| P02 | F02 at HEAD oracle: Appendix C BANANA wrapper plus missing, duplicate, `CLEAN`+rc1, `DRIFT`+rc0 wrappers | HEAD: each adversarial wrapper is accepted (defect baseline). After: each exits 1 with a named reason; honest run `matched=28 total=28` exit 0 ×2, byte-identical | RegressionHarness, OracleFix |
| P03 | C1 user/system rows for classes `fe6faa94…`, `d989611b…`, `fc2e22bc…`, boot-scoped, `--output-fields` only | Counts reported per scope, never summed; empty valid query = 0; nonzero producer rc, absent journalctl, or unreadable system scope = `unavailable`. Round-12 values (user 7, system 9, boot `7bd93aee…`) are expectations to re-measure, not evidence | CensusFix, JournalFixtureDesign |
| P04 | Kernel victim class | Expected state under criterion 15: `unavailable` with reason (no structured class), or a text class explicitly disclosed as a criterion exception that needs operator approval. Not a MESSAGE_ID count | L1, operator (L0) |
| P05 | Captured output MESSAGE-free check | Count of `MESSAGE` field occurrences in census stdout = 0 for the new probe | CensusFix |
| P06 | Scope-sum negative | No finding or row adds user and system counts | CensusFix |
| P07 | Drift classification | Every changed non-volatile token named and classified; no re-pin to turn red green (criterion 10) | L1 |
| P08 | Harm watch | 3+3 interleaved wall time against E19 method; reported as a delta; "harmed" requires a declared budget (none exists) | L1 |
| P09 | Selftest count after landing | Measured N (not pre-declared); all cases PASS, exit 0 | L1 |
| P10 | Oracle final bytes | `matched=28 total=28` exit 0 ×2, byte-identical; registry 28 ids unchanged | L1 |
| P11 | Regression harness output JSON | Per-adversary exits and finding ids, retained under the `--output` path | RegressionHarness |
| P12 | SOURCES validation | `scripts/sources-census.sh validate --root <fleet> mori-shokunin` exit 0; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` before→after | JournalKnowledge, L1 |
| P13 | Lesson `corpus/lessons/round-13.md` with `## Mistakes` and `## Gate` | Required by QUALITY 26–28 and the round frontier step | MistakeScribe, L1 |

## 4. Ordered report skeleton (L1 round-13 report)

Target path: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-13/mori.md` (protocol id name; see E16 for the precedent conflict). Cells in brackets are filled only from receipts at the freeze commit.

```
# mori — round 13 report (mori-r13-build)
- Lane / round / wave / entering HEAD 6531ac6 / evidence commit [filled at commit] / no push
- Status line: [ADMIT | ADMIT-with-correction | HOLD], with the reason in one sentence

## Work performed
- Declared claims (1–3), each with target axis: C1 coverage (structured journal scopes); C2 operability (F01 + F02)
- One bullet per work item, each with path:line, command output or commit hash (E02, E04, E06, E10, E13 …)

## Landed changes
- File → LOG entry (`LOG.md` round-13 block) → commit hash. Include the QUALITY 26–28 addition and its lesson.

## Before → after measurements
- Table per claim: counting command | before (HEAD `6531ac6`) | after (commit [..]) | expected gradient (pre-registered, P01–P04)
- Blank cells stay blank until measured; a missing cell is not a pass

## Negative checks (order; run before any count is cited)
- N0 freeze: HEAD, `git status --short`, census and oracle sha256, re-resolved anchors
- N1 F01 baseline defect at HEAD (P01 before side)
- N2 F02 baseline defect at HEAD (P02 before side)
- N3 F01 after: positive, sibling-only negative, control; no pipe into an early-exit match (grep the diff)
- N4 F02 after: each adversary exits 1 with a reason; honest 28/28 ×2
- N5 C1 after: MESSAGE-free output; user and system rows labeled; no sums; kernel class state per P04
- N6 C1 failure arms: absent journalctl, nonzero rc, unreadable system scope → unavailable; valid empty → 0
- N7 harm watch: wall time delta against E19
- N8 drift classification (P07); selftest and oracle final receipts (P09, P10)

## Sources & frontier
- SOURCES rows before→after with command; rows added by tier; rows touched old→new (S013, S014, S015, S031 reopened per LOG)
- Frontier rows advanced: FR1 (system-journal kernel OOM) only as far as P04 allows; FR9 if fixtures are committed

## Mistakes
- Classes mined (count from `corpus/lessons/round-13.md`), captured-by summary, criteria added 26–28 with pointers
- This round's gate misses, recorded as found

## Trend verdicts
- expansion: [verdict, evidence] — four values only
- quality: [verdict, evidence]
- discernment: [verdict, evidence]; non-author spot-check status stated as pending unless a named reviewer exists

## Axis verdicts (owned axes first)
- coverage: [four-value verdict] | score [6→7 only if N1–N8 pass; else unchanged]
- operability: [four-value verdict] | score [same rule]
- depth, freshness, calibration, adjacency: observed for regression, verdict only

## Carried debt and residuals
- F03, F04, F05, F09, F10, F11, F12, F14 status (open or closed with receipt)
- D08 (system journal) partly addressed by C1 system rows; D09; D21 quota abort; kernel victim residual (P04); drift classification; wall-time budget (L0)

## SHONEN
- [ ] Box 1 — pointer
- [ ] Box 2 — pointer
- [ ] Box 3 — pointer
- [ ] Box 4 — pointer
(one line per box; `[ ]` unless a named non-author verifier exists; `[~]` only with a resolvable evidence pointer)

## L0 questions
- Kernel victim class admissibility under criterion 15 (operator decision)
- Wall-time budget for live census (operability verdict cannot be measured without it)

## Integrator notes / boundaries
- Seats committed nothing; fleet root not written; tool installs recorded (none unless used)
- Sibling in-flight edits observed; anchors re-resolved at freeze

## Post-review fixes
- Append-only; empty at filing
```

## 5. Findings for peers (scoped, with owners)

1. **Kernel victim records have no `MESSAGE_ID` (E10).** Planned item 3 in `SCORECARD.md:639-649` ("after: the 5 retained records counted") and the CensusFix label ("kernel OOM notices fe6faa94") are not satisfiable under criterion 15 as written. Owners: CensusFix, JournalKnowledge, CountDesign, L1. Proposed: state the kernel class as `unavailable` with reason, or request an explicit operator exception. No text count is admissible under criterion 15.
2. **`fe6faa94…` is a unit notice, not a kernel record (E12).** Owner: CensusFix, JournalKnowledge. Use "unit notice" in labels and findings (criterion 16).
3. **Admitted note uses a text match for kernel counts (E11).** Owner: JournalKnowledge. Correction must be an append-only erratum (criterion 4), not an edit of the admitted note.
4. **Selftest cannot exercise the structured arm (E07, E13).** Owners: CensusFix, OracleFix. Dispatcher stub must key on arguments; `MORI_FIXTURE` should not hide the JSON arm from fixtures.
5. **Verdict grammar is unchecked (E04).** Owner: OracleFix, HistoryKnowledge. Required: exactly one `^MORI_CENSUS:` line; roll word in {CLEAN, DRIFT}; roll ↔ rc agreement (0 ↔ CLEAN, 1 ↔ DRIFT); absence and duplicates fail. The `grep -m1` capture (E14) should become a single capture with a count.
6. **Pointer and score drift (E15, E16, E17).** Owner: L1. Fix `SCORECARD.md:10`; cite the resolving round-12 path; land criteria 26–28 with `lessons/round-13.md` or withdraw them.
7. **Drift is already red (E18).** Owner: L1. Round 13 must add a classification receipt; any re-pin needs a recorded reason (criterion 10).
8. **Provenance string prints MESSAGE (E09).** Owner: CensusFix. Replace the `cmd=` text with the field-restricted command actually run.
9. **Audit anchors are stale (E02).** Owner: L1, all seats. Use `:1469-1494` for the F01 block and HEAD oracle lines for F02.

## 6. Coordination

- No messages sent. Sibling outputs under `.ufo/waves/round-13/build/` were checked for the kernel `MESSAGE_ID` question only; FrontierConnection and SiblingOverlap already state that kernel records are `_TRANSPORT=kernel` and not catalog-ID notices, which agrees with E10.
- No seat writes to `corpus/` or `tools/` from this file.

## 7. Limits

- E10 is one host read on one boot scope (`-b all`). It shows absence of `MESSAGE_ID` in 48 173 kernel lines, not a proof for every kernel record on every host.
- E03 and E05 are audit-recorded results at older bytes. They are not re-run here.
- The oracle working tree is in flight; HEAD anchors are the only pinned ones in this report.
- Round-12 non-author agreement is one reviewer's sample.
