# Round 93 — mori (L1 MoriR93, attempt 1) — lesson

Entering `7b3fe9d540c98b8b0390a0f9bbe78de4341092a5`. Frozen contract `.ufo/waves/round-93/contract.md`
committed at `6d82b8d7` (with `count-c1.py`, `count-c2.py`, `controls-r93.sh` and the entering receipts).
Wave spec and dispatch at `d8a9b28c`. Landing `1fc921cf75afa6650b9dc9451b33a2ec0610ae0a`. The
post-freeze control extension and the wave evidence follow at `2d14e493`. Wave `w1`: 12 seats,
all returned output, none dead (`.ufo/waves/round-93/w1-results.json`).

## Claims and verdicts

- **C1 — calibration (the round-92 lesson's sentence is true of the repo it describes).** Before at
  `7b3fe9d5`: `C1=unmet trio=98 adm_ok=7 adm_fail=12 patched12=0`. At landing `1fc921cf`:
  `C1=met trio=98 claim_r92_true=1 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok`
  (`.ufo/waves/round-93/evidence/after-c1-1fc921cf75afa6650b9dc9451b33a2ec0610ae0a.txt`). Met as frozen.
  The calibration reading is not established by the lane: the non-author-role attack `Mo93R03Atk` reads the
  repair as bookkeeping. The round-92 sentence was lesson prose, not a SHONEN or SCORECARD box; LEARNING.md
  says `verified-at` is "commit or date", so the commit form is the lane's stricter criterion; and the sentence
  is true of 19 entries only (`7/98` before, 19/98 after; `Mo93R03Atk` §1). The axis verdict is left for the
  non-author closure.
- **C2 — operability (no tool under `tools/` hardcodes a host home path).** Before: `C2=unmet home_literals=18
  vgpnk_refs=18`. At landing: `C2=met home_literals=0 vgpnk_refs=0 tools=3 selftests=3/3 census=ok`
  (`.ufo/waves/round-93/evidence/after-c2-1fc921cf75afa6650b9dc9451b33a2ec0610ae0a.txt`). Met as frozen.
  Named limits (measured by `Mo93R01Atk`, not waived): a host path split by concatenation or built with
  `os.path.join('/home', name)` is not caught by the regex and is named in the contract; Windows and macOS
  forms and trailing-dot forms that carry the username are caught by the byte conjunct only, since the regex
  alone misses them.
- **Not declared:** a digest-gate freshness claim (contract P3; rule 2) and a recheck freshness claim (contract
  P4: zero cadence rows due at 2026-11-05).

## Work the round landed

- `tools/mori-blind-check.sh`, `tools/mori-misroot-sweep.py`, `tools/mori-round17-context-check.py`: functional
  host literals derive from `SHOKUNIN_ROOT` or `$HOME/Projects/shokunin`; prose mentions are placeholders. Patch
  `Mo93E01Vgpnk` (`.ufo/waves/round-93/w1/patches/Mo93E01Vgpnk.patch`). Its heredoc change from `<<'EOF'` to
  `<<EOF` was checked: the body contains no `$` or backtick, so behaviour is unchanged.
- `corpus/knowledge/` (12 files): the `verified-at:` value gains the admission short hash; the original value is
  kept in parentheses. Patch `Mo93E02Verif` (`.ufo/waves/round-93/w1/patches/Mo93E02Verif.patch`); each file's
  other lines are byte-identical.
- `corpus/QUALITY.md` criteria 198–201 (read windows, counted prose, control edits, rule 2 in premises).
- `corpus/SOURCES.md`: S622 (git-log documentation) and S623 (Python `-I` documentation), from scout
  `Mo93Sc01Src` (`.ufo/waves/round-93/w1/Mo93Sc01Src.md`), status `mined`, used-by this lesson.
- `.ufo/waves/round-93/controls-r93-ext.sh`: three post-freeze controls (see M5). The frozen
  `controls-r93.sh` and the frozen counters are byte-identical to `6d82b8d7`.
- Wave evidence: spec, dispatch, registry, seat reports and patches under `.ufo/waves/round-93/w1/`.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `unchecked-rule-2` — the first contract draft planned to complete the recorded digests in place (31 prefix-only rows, S125 unpinned). CORPUS.md rule 2 allows only `status`, `recheck` and `used-by` to change in place | `.ufo/waves/round-93/contract.md` P3; `/home/vgpnk/Projects/shokunin/CORPUS.md` rule 2 (the fleet-root file; there is no `corpus/CORPUS.md` in the lane); `Mo93K01Crit` §1 | QUALITY 201 (drafted this round); CORPUS rule 2 | contract redrafted before its commit (`6d82b8d7`): the digest-gate claim is not taken, no registry row is edited in place, and the debt is routed. Able to fail: the draft's in-place edit would change an anchor cell, which the rule-2 grep in P3 refuses |
| `truncated-read-window` — the first trio counter read 4096 bytes per file and counted 97 of 98 knowledge entries | `.ufo/waves/round-93/evidence/window-demo-r93.txt` (`read 4096 bytes -> trio 97`, `read 65536 bytes -> trio 98`); `count-c1.py` `trio_count` reads `65536` | QUALITY 198 (drafted this round) | 64 KB read in the frozen counter (the first run was 4096 and was caught by the control run). Able to fail: the window-demo file prints 97 and 98 on the same bytes |
| `miscounted-host-literal` — the first contract draft gave 10 occurrences of the host home path; the byte count is 18 and the `git grep -c` line count is 12 | `.ufo/waves/round-93/evidence/measure-c2-entering.txt` (`vgpnk_refs=18`); `git grep -c vgpnk 7b3fe9d5 -- tools` → 12 lines (contract P2) | QUALITY 199 (drafted this round) | contract P2 states both units; the counter prints the byte count. The first draft's figure is not in any committed revision; the record is the L1's account, and P2 is the committed correction |
| `wrapped-sentence-sed-noop` — the first text-only control substituted a pattern that matched a sentence wrapped over two lines, changed nothing, and then produced no fixture commit | `.ufo/waves/round-93/controls-r93.sh` (sed and `grep -q` assertion for the lesson sentence); `.ufo/waves/round-93/evidence/controls-r93.txt` (text-only control, which matched nothing in the first run) | QUALITY 200 (drafted this round) | control matches the first wrapped line and asserts the substitution with `grep`, exiting 2 on a no-op. The current control's fixture commit changes the revision and still reads `C1=unmet adm_fail=12` |
| `control-battery-gap` — mutation testing (`Mo93M01Mut`) found three conjuncts that no frozen control flips: C1 admission prefix test (m1), C1 census clause (m4), C2 bare-username clause (m6). Two other mutants were killed by the frozen battery | `.ufo/waves/round-93/w1/Mo93M01Mut.md` (table); `.ufo/waves/round-93/evidence/mutant-kill-ext-r93.txt` | none — the frozen battery had no control for a wrong-but-same-shape hash, a malformed registry row, or a bare username | post-freeze extension `controls-r93-ext.sh` (three controls on the landed base; the frozen counters and frozen controls are unchanged). Able to fail: under m1 the wrong-hash control reads `C1=met`; under m4 the census-break control reads `C1=met census=rc1`; under m6 the bare-username control reads `C2=met vgpnk_refs=1`. Extension controls on the landed base all read unmet |
| `unplanned-spec-commit-order` — contract ordering step 1 required the wave spec committed together with the frozen set; the spec went in a separate commit `d8a9b28c` before dispatch | `Mo93R04Sweep` §1 (`git show --stat 6d82b8d7` lists 8 files, the spec is absent); `d8a9b28c` | contract ordering step 1 (this round) | disclosed here; the spec was committed before the ready file, so no seat ran on an uncommitted spec. The next round commits spec and contract in one helper call |

## Routed defects (not fixed this round)

- **R02 false-pass path (named, not claimed).** `count-c1.py` tests `ac[:7] in va` as a plain substring with no
  word boundary. A 7-character admission hash embedded in a longer hex token would pass. No current file
  exhibits it (`Mo93R02Atk` (4): `other7=0`), but the counter is frozen and the fix changes its rule. Route:
  the boundary check `(?<![\w])…(?![\w])`, next round, with a control built on the embedding.
- **Counter-owned host path.** `count-c1.py` and `count-c2.py` name `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
  as a constant (`Mo93R04Sweep` D2). This is in the counters, not `tools/`, so C2 does not measure it. Route:
  the next counter amendment.
- **Digest-gate debt** (31 prefix-only rows, S125 unpinned, `.ufo/waves/round-90/…` pinned root): unchanged
  from round 92 and carried (contract P3).
- **Equivalence harness verdict.** `equiv-c2.sh 7b3fe9d5 1fc921cf` reports `different` for the three repaired
  tools, and each line names only `tree/tools/<t>`, the tool's own source bytes. The `--help` and `--selftest`
  artifacts are identical (`.ufo/waves/round-93/evidence/equiv-c2-entering-vs-landing.txt`). The harness
  compares the source tree by design; its verdict is not a behavioural difference. Route: a harness option
  that excludes the tree from the verdict.

## Gate (sources, protocol §2b)

| Row | URL | Access and recomputation | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S622 | https://git-scm.com/docs/git-log (HTTP 200, no redirect, git-log "last updated in 2.56.0") | 2026-11-05; sha256 `f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b`, 375834 bytes; two fetches byte-identical (scout receipt) | "Select only files that are Added (A), Copied (C), Deleted (D), Modified (M), Renamed (R), have their type" (DIFF FORMATTING, `--diff-filter`; `grep -c -F` = 1 in the stripped copy); "abbreviated commit hash" (PRETTY FORMATS, `%h`; = 1) | **admit** (mined; used-by this lesson). Teaches: the `A` filter selects added paths, and `%h` is the short-hash form used for `verified-at` admission commits (C1 sourced claim) |
| S623 | https://docs.python.org/3/using/cmdline.html (HTTP 200, no redirect, Python 3.15.2 docs) | 2026-11-05; sha256 `90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0`, 171073 bytes; two fetches byte-identical | "Run Python in isolated mode. This also implies -E, -P and -s options." (1.1.3 Miscellaneous options, `-I`; = 1) and "All PYTHON* environment variables are ignored, too." (= 1) | **admit** (mined; used-by this lesson). Teaches: `-I` isolates the counters from user site and environment, the basis of their hermetic runs (counters, controls) |
| S621 | (unchanged, round 92) | — | — | not re-opened this round |

Gate decisions this round: S622 and S623 admitted (both re-located by the scout and both quotes confirmed by
the scout's uniqueness counts; neither quote is in the lane's registry before this round). No candidate
rejected. The spot-check is outside: no non-author closure yet.

## Assimilation and considerthese

- **Assimilation: none.** `merge/mori/` was not opened this round; the two claims are calibration and
  host-path portability, and no staged theme was checked against them.
- **considerthese: none taken.** `considerthese/2026-10-26.md` says of its four suggestions that 1 is adopted
  (QUALITY 123), 2 is adopted as a criterion (QUALITY 127), and 3 is adopted (round 49 flagged-fixed count) —
  the file's own status line (suggestion 4). No proposal is "still unimplemented", so none was mined.

## Trend verdicts (lane; the closure rules)

Expansion: unchanged (two source rows, no knowledge entry admitted). Quality: unchanged (12 `verified-at` lines
now name a checkable commit; no entry superseded or re-verified against its source). Discernment: unchanged
(gate decisions above are the lane's own seats; no non-author spot-check exists yet).

## Planned (round 94)

1. The `count-c1.py` word-boundary amendment (R02 routed defect) with a control built on an embedded hash,
   as a new frozen counter revision, not an edit of the frozen one.
2. The counter-owned host path (`count-c1.py`/`count-c2.py` CENSUS constant) under the same amendment.
3. Carry: digest-gate debt (contract P3); round-90 nonce guard (QUALITY 191).
