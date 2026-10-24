# SelftestC2 — C2 selftest attack (round 20)

**Verdict: PARTIAL.**

- **Frozen oracle, loaded unchanged at runtime: HOLDS.** The 14 frozen expectations are read from `frozen/c2-expected.json`; the checker's in-memory copies equal the file (0 diffs); the file's sha256 was identical at every check in this run; corrupting one expectation flips the verdict to FAIL.
- **Frozen oracle, enforced: NOT.** No count, hash, or unknown-key guard. Trimming the file to 13 frozen cases, weakening an expectation, or misspelling a key still prints PASS.
- **Refinement cases: 2 of 9 hold** (`r6-taskcall-missing`, `r7-dotdot-inside-lane`). **7 of 9 assert only part of the refinement they name** (`r1-godspeed-trailer`, `r1-crlf-trailer`, `r2-stub`, `r5-duplicate-report-path`, `r8-symlinked-parent` partial; `r3-name-hint`, `r4-duplicate-dispatch` weak). Of 35 refinement mutants, 18 survive. Spec-visible survivors are confirmed by differential probes (section 5).
- **The selftest has no negative control.** `_check_case` forced to `return True` still prints `PASS (23 cases, 23 passed, 0 failed)`. Each refinement's only assertion is a single checker line with no redundancy.

## 0. Target, pins, and version drift

- Analysed: `tools/mori-wave-settlement.py`, sha256 `79e7f9dedb8a16a9d9257644045c56c57ca97b27ab94640ca487b330527b28f9`, 714 lines, mtime 08:17:22 (-0300). Pinned copy: `falsify/SelftestC2/pinned3/`. Still at this sha after the final run.
- Frozen: `.ufo/waves/round-20/frozen/c2-expected.json`, sha256 `0984806922da727a02a7944c00154df7a5aaff356c91c6fb36f47467c4f7d2af`, mtime 07:23:14. Same hash at every check, before and after all runs. The contract (`.ufo/waves/round-20/contract.md`) pins no hash for it, so "unchanged since freeze" rests on mtime plus this session's hashes [INFERENCE beyond that].
- **The tool changed six times during this falsify window (not by me).** I re-ran the full attack matrix on each pinned version:
  - `c6e6091937e4…` (07:45:51): 21 cases. My first run here, 21/21, is superseded.
  - `e5c06dad…` (08:04:26): adds `r7-dotdot-inside-lane`.
  - `203c716e…` (08:11:12): docstring-only fix (R2 "64 bytes" → "16 bytes"; R6/R7 documented).
  - `5027bdc7…` (08:13:06): adds R8 code plus `r8-symlinked-parent`.
  - `c134c57b…` (08:15:31): `name_hint` token `undispatched-name:` → `filename:`; fleet root `realpath` plus isdir check.
  - `79e7f9de…` (08:17:22): vocabulary guard added to the `_selftest` loop (lines 660–661).
- Exact run on the final version: `python3 tools/mori-wave-settlement.py --selftest` → `MORI_WAVE_SETTLEMENT_SELFTEST: PASS (23 cases, 23 passed, 0 failed)`, exit 0. The module-level text lines 41–56 hold 9 refinement entries, and the frozen loader (`_selftest` lines 635–638) is unchanged across these versions (diffs reviewed).

## 1. Frozen oracle (`frozen/c2-expected.json`)

Evidence:
- `_selftest` reads `oracle["cases"]` and runs `cases + REFINEMENT_CASES` (`tools/mori-wave-settlement.py:635`, `:638`). `_check_case` only reads `expect` (lines 566–620).
- In-memory comparison (`e5c06dad…` run, harness snapshot): frozen cases differing from file = `[]` of 14; refinement cases differing from `REFINEMENT_CASES` = `[]`.
- Tamper controls (copies under `falsify/SelftestC2/final3-tamper/`, run with `python3 <copy> --selftest`):

| control | change to oracle copy | exit | result |
|---|---|---|---|
| T0 | none | 0 | `PASS (23 cases, 23 passed, 0 failed)` |
| T1 | `one-missing` exit 1 → 0 | 1 | `FAIL (23 cases, 22 passed, 1 failed)` (file drives outcome) |
| T2 | delete frozen case `deterministic` | 0 | `PASS (22 cases, 22 passed, 0 failed)` (no count pin; contract says 14) |
| T3 | delete `exit` key from `traversal` | 0 | `PASS (23 cases, 23 passed, 0 failed)` (weakened case still passes) |
| T4 | rename key `missing_names` → `missing_namez` | 0 | `PASS (23 cases, 23 passed, 0 failed)` (unknown keys silently ignored) |

- Frozen `setup` texts vs `_fixture` branches (manual reading, all 14 consistent): the setups are re-implemented in the tool, not loaded, so the oracle only supplies expectations.
- Checker interpretations not stated in the frozen file: `not_followed` ⇒ member status `missing` (checker lines 599–603); `no_vocab` excludes `dispatch_sha256` (lines 611–620).

## 2. Refinement cases: would each still pass without its refinement?

Method: 35 refinement mutants built by exact string replacement on the pinned source (each pattern asserted unique), each run through the selftest in-process and via CLI. Killed = at least one case FAILs.

| case (line) | refinement | mutants that FAIL the case | mutants that PASS it | verdict |
|---|---|---|---|---|
| r1-godspeed-trailer (:42) | R1 trailer = last matching line | R1-A final-line-only | R1-B first-match (frozen contract says "the LAST line"; probe P2 differs); R1-C no-rstrip (P1 differs); R1-E split("\n")+rstrip | PARTIAL |
| r1-crlf-trailer (:43) | R1 CR/trailing strip | R1-D no split, no rstrip | R1-C (`splitlines` removes CR anyway; trailing-space case never tested) | PARTIAL |
| r2-stub (:44) | R2 stub | R2-A no stub; R2-B prefix match unbounded; R2-D 15-byte bound | R2-C drop bare `STATUS: started` form (P12 differs) | PARTIAL |
| r3-name-hint (:45) | R3 name hint | R3-A no hint; R3-F drop "preview" | R3-B always-hint (P9); R3-C drop validation (P10); R3-D drop undispatched (P10); R3-E drop not-dispatched (P10); R3-G case-sensitive (P11); R3-H basename → relative path (P8) | WEAK |
| r4-duplicate-dispatch (:46–47) | R4 duplicate_of / unique | R4-A no duplicate_of; R4-B unique = len(waves) | R4-C unique constant (P4: 2 vs 1); R4-D previous-not-first (P3); R4-E wave-keyed (P4); R4-F self-duplicate (P5) | WEAK |
| r5-duplicate-report-path (:48) | R5 duplicate_report_paths | R5-A zero; R5-B member-sum (P6: 3 vs 2) | R5-C distinct-paths (P6: 1 vs 2); R5-D cross-wave (P7) | PARTIAL |
| r6-taskcall-missing (:49) | R6 missing taskCall → unavailable | R6-A absent → no-spawn; R6-B absent → settled | none | HOLDS |
| r7-dotdot-inside-lane (:52) | `..` anywhere is unsafe (pins frozen rule) | R7-A allow `..` (P13 differs) | none | HOLDS |
| r8-symlinked-parent (:55) | R8 symlinked parent → unsafe, never followed | R8-A no parent-symlink check; R8-B follow all components (also kills frozen `symlink-report`); R8-C unsafe not returned | R8-D unsafe-not-a-safe-path (state: P14 `unsettled` vs `unavailable`; r8 has no `state` key); R8-F resolve-inside allowed (P15) | PARTIAL |

Totals: refinement mutants 35, killed 17, survived 18 (R1-B, R1-C, R1-E, R2-C, R3-B, R3-C, R3-D, R3-E, R3-G, R3-H, R4-C, R4-D, R4-E, R4-F, R5-C, R5-D, R8-D, R8-F). Clearly spec-visible survivors: all except R1-E and R5-C (edge/ambiguous).

## 3. Frozen cases (14)

- 11 frozen cases (`all-present`, `one-missing`, `none-present`, `empty-report`, `misrooted`, `malformed-dispatch`, `no-trailer`, `traversal`, `absolute-path`, `other-schema-ignored`, `no-spawn`) are killed only by the "no discovery" mutant. No refinement mutant changes them.
- `symlink-report` is killed by R8-B (following symlinks), the only frozen case that touches a refinement.
- `content-not-emitted` is killed only by the "emit report content" mutant, and `deterministic` only by the "reverse wave order" mutant. Both PASS when zero waves are discovered (mutant `X-no-discovery` survives both): they assert nothing about discovery. Knowledge §4 documents "zero discovered waves exit 0" as a limit.

## 4. Selftest-level findings

- **C1 (no negative control):** `_check_case` forced `return True` → PASS 23/23 (CLI rc 0).
- **C2–C4 (single-line dependence):** removing one checker line plus its implementation mutant still passes: `name_hint` check (lines 588–589) + R3-A; `duplicate_report_paths` check (590–592) + R5-A; `unique_dispatch_sha256` check (593–595) + R4-B. Each refinement's sole assertion is one line.
- **Vocabulary guard (new at 79e7f9de, lines 660–661):** applies to all fixture outputs. No mutant of mine emits those words, so no kill/survive result changed.
- **Wave-state for symlink-unsafe members (R8-D, probes P13 vs P14):** a lexical `..` member gives `unavailable` (P13) while a symlinked-parent member gives `unsettled` (P14), both rc 1. The frozen contract defines `unavailable` as "no member had a parseable safe path" and "safe" as resolving inside the lane root (`contract.md:70–73`, `:78–81`); by that wording the symlink member would be `unavailable`. `r8-symlinked-parent` omits `state`, so this is unpinned. [INFERENCE: this is a spec-reading inconsistency, not a confirmed intent.]
- **In-lane symlink (P15):** a parent symlink resolving inside the lane is `unsafe` under R8, which is stricter than the frozen "resolve inside the lane root" wording. R8 text supports it ("never followed"), but no case pins the in-lane variant (R8-F survives).

## 5. Spec-visible probes (REAL vs mutant, final version 79e7f9de)

Each probe runs `scan_lane` on a fixture the selftest never builds; "DIFFERS" = the mutant gives a different result.

| probe | REAL (current tool) | mutant | result |
|---|---|---|---|
| P1 trailing spaces on trailer | settled, present 1 | R1-C: unavailable, unparsed 1 | DIFFERS |
| P2 two trailers, last missing | unsettled (LAST = B missing), rc 1 | R1-B: settled, rc 0 | DIFFERS |
| P3 three identical dispatches | b→a, c→a | R4-D: c→b | DIFFERS |
| P4 same wave id, different bytes | unique 2, no duplicate | R4-E: b→a, unique 1; R4-C: unique 1 | DIFFERS |
| P5 first file self-duplicate | a.duplicate_of = null | R4-F: a→a | DIFFERS |
| P6 three tasks share one report | duplicate_report_paths 2 | R5-C: 1; R5-B: 3 | DIFFERS |
| P7 same report across two waves | 0 and 0 | R5-D: second wave 1 | DIFFERS |
| P8 "preview" only in a directory name | hint null | R3-H: `filename:preview` | DIFFERS |
| P9 ordinary name | hint null | R3-B: `filename:preview` | DIFFERS |
| P10 validation / undispatched / not-dispatched | three `filename:` hints | R3-C/D/E: one hint lost each | DIFFERS |
| P11 `Dispatch-PREVIEW.json` | `filename:preview` | R3-G: null | DIFFERS |
| P12 report content `STATUS: started` (no newline) | stub, unsettled, rc 1 | R2-C: present, settled | DIFFERS |
| P13 lexical `..` in trailer | unsafe, unavailable, rc 1 | R7-A: settled | DIFFERS |
| P14 parent symlink → outside lane | unsafe, **unsettled**, rc 1 | R8-D: **unavailable**; R8-A/C: missing; R8-B: present | DIFFERS |
| P15 parent symlink → inside lane | unsafe, unsettled, rc 1 | R8-F: present, settled | DIFFERS |
| P16 symlinked `--fleet-root` | misrooted + present, partial | F2 (abspath): missing | DIFFERS (F1 same) |
| P17 `--fleet-root` is a file | `ScanError` raised | F1 (no isdir check): partial, rc 1 | DIFFERS (F2 same) |

Mutants F1 and F2 (fleet-root checks added at 79e7f9de, lines 327–329) survive: no case covers them.

## 6. Disclosure and documentation drift

- `corpus/lessons/round-20.md:35–39`: lists R1–R7 and states "Eight refinement selftest cases". The final tool has nine (R8, `r8-symlinked-parent`), so the lesson is stale and does not disclose R8.
- `corpus/knowledge/wave-settlement-r20.md:22` ("14 frozen + 9 refinement cases") is current. `:34` discloses the R8 decision row. Its §3 list (`:52–58`) stops at R7.
- `tools/mori-wave-settlement.py:39` comment still says "R1–R5 (+ missing taskCall)"; the docstring already lists R1–R8.
- R5 wording (docstring line 15, "counts members sharing one report path") is ambiguous: the code computes excess (`count - 1`), which `r5` pins as 1 for two members. Member-count reading would give 2.
- Fleet-root behaviour (realpath plus isdir check, lines 327–329) is not asserted by any case. Whether it is documented was not checked.
- `totals.name_hinted_waves` (line 369) is emitted and no case asserts it. [INFERENCE: a mutant dropping it would survive.]

## 7. Limits

- Mutation survival is evidence of weak assertions, not a proof of coverage; kills are only as strong as the mutants chosen.
- The lane file changed during the run; results are for the pinned copies above, and the final matrix is on `79e7f9de…`.
- [INFERENCE, not probed] `str.splitlines()` (line 218) also splits on `\v`, `\f`, `\x1c–\x1e`, `\x85`, `\u2028`, `\u2029`, so a trailer after those separators would be accepted; the contract's "line" presumably means `\n`.
- [INFERENCE] `main()` maps `ScanError` to exit 2 (not re-read at 79e7f9de).
- Lesson evidence path `.ufo/waves/round-20/evidence/mut-r7/` not opened.

## 8. Suggested discriminators (not implemented; no edits to lane files)

1. r1: two-trailer body with the last trailer missing (expect unsettled); trailing-space trailer (expect settled).
2. r2: bare `STATUS: started` report (expect stub).
3. r3: negative (ordinary name → no hint); one case per alternative; uppercase name; directory-only match (expect none).
4. r4: three identical copies (no chain); two same-wave different-bytes files (unique 2, no duplicate); first file's duplicate_of null.
5. r5: three tasks sharing one path (expect 2); cross-wave pair (per-wave 0).
6. r8: pin `state` for the symlink case; add an in-lane symlink case with the decided policy.
7. Fleet root: symlinked fleet root → misrooted; fleet-root file → exit 2.
8. Discovery assertion (`waves >= 1`) for `content-not-emitted` and `deterministic`.
9. Oracle pin: sha256 and `len(cases) == 14`; reject unknown expect keys; a negative control case that must FAIL.

## 9. Artifacts and bounds

- Scratch (all under `falsify/SelftestC2/`): `pinned/` (`5027bdc7…`), `pinned2/` (`c134c57b…`), `pinned3/` (`79e7f9de…`, final), `mutants/`, `final/`, `final2/`, `final3/` (mutant copies), `*-tamper/` (oracle controls), `c2-selftest-attack-kills.json` (first-pass kills, `e5c06dad…`).
- Tooling: no installs. Used `python3` stdlib, `sha256sum`, `stat`, `diff`, `wc`, and read-only greps of named files.
- Bounds: no edits to lane files; no git/jj commands; no reads of `.jj/`, `.ufo/interactive-sessions/`, or `.ufo/worktrees/`; no subagents; no messages to peers; `mori-census.sh` not run.
