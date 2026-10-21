PARTIAL. The set-level counts hold: 8→0 (entering capture, r13→r20) and 7→0 (r10 pre-pin first line). The frozen counting command, run as written on this host (LANG=en_US.UTF-8, LC_ALL unset), does not produce them: it returns 37/33 and 36/32, and `comm` rejects its first input as unsorted. It returns 8/0/7/0 only when `LC_ALL=C` reaches the first `sort`. `check-register.py` on the r20 register is clean (rc 0). The zero `census-regression` count is a judgement, not a measurement. Two tokens are disputed, and the mechanism behind one is confirmed by the watchdog log.

Seat CountC1, leaf (no subagents). Read-only on lane inputs, fleet repo, `.ufo/watchdog.log`. Census not run. No installs or updates. Scratch: `.ufo/waves/round-20/falsify/CountC1/`.

## 1. Claim by claim

| Claim (contract C1) | Verdict | Basis |
|---|---|---|
| 8 unclassified, entering vs r13 | HOLDS (set count) | Python set difference 8; C-locale pipeline 8 |
| 0 unclassified, entering vs r20 | HOLDS (set count) | Python 0; C-locale 0; check-register `unclassified=0` |
| 7 → 0, r10 pre-pin first line | HOLDS (set count) | Python 7 / 0; C-locale 7 / 0 |
| Frozen command reproduces 8 / 0 | BROKEN under default locale | As typed: 37 / 33 (§2a) |
| check-register clean on r20 | HOLDS | rc 0 (§3) |
| No census-regression, so re-pin is legal | NOT ESTABLISHED | §5 (judgement, contested) |

## 2. Counting command, exact outputs

Contract text, DRIFT and REG substituted, `| wc -l`:
```
LC_ALL=C comm -23 <(tr ' ' '\n' < DRIFT | grep -v '^MORI_DRIFT:$' | grep . | sort -u) <(jq -r '.tokens|keys[]' REG | LC_ALL=C sort -u) | wc -l
```
DRIFT_A = `/usr/bin/jq -r .stdout c1-drift-entering.json` (scratch `drift-entering.stdout.txt`). DRIFT_B = line 1 of `c1-drift-r10-prepin.txt` (scratch `drift-r10-prepin.line1.txt`).

| Run | A vs r13 | A vs r20 | B vs r13 | B vs r20 | Notes |
|---|---|---|---|---|---|
| (a) As typed in the agent shell. Bare names are builtins (`type -a`); `jq` = jaq 3.1.1; LANG=en_US.UTF-8 | 37 | 33 | 36 | 32 | comm stderr 71 B: `comm: file 1 is not in sorted order` / `comm: input is not in sorted order`. Re-run identical. Exit 0 is `wc`'s |
| (b) (a) with `export LC_ALL=C` for the whole pipeline | 8 | 0 | 7 | 0 | stderr 0 B |
| (c) Contract text with GNU `/usr/bin` tools (coreutils 9.12, jq 1.8.2) | 47 | 44 | 46 | 43 | comm rc 1; stderr 71 B; first input fails `LC_ALL=C sort -c` (rc 1) |
| (d) GNU tools, `LC_ALL=C` on every stage | 8 | 0 | 7 | 0 | comm rc 0; stderr 0 B; first input C-sorted (rc 0) |
| (e) Minimal fix: `LC_ALL=C` on the first `sort -u` only, builtins | 8 | 0 | 7 | 0 | |
| (f) Python set difference (check-register token model) | 8 | 0 | 7 | 0 | `scratch/oracle.py` |

Root cause: `LC_ALL=C` prefixes `comm` and only the second `sort`. The first `sort -u` sits in a process substitution and inherits `en_US.UTF-8`. Its order (as-typed output begins `+conf_dropped_n +conf_n +FINDING:COREDUMP_NOTICE_JOURNAL_USER …`) is not C order, and `comm` requires C order.

Controls, C-locale GNU (runs in `repro-count.sh`):
- Whole r10 pre-pin file, including `rc=1`: r13 8, r20 1.
- Post-pin capture: 2 and 2 (`none`, `rc=0`).
- Raw entering JSON as DRIFT: 108 and 100. The `.stdout` extraction is load-bearing.

The 8 unclassified vs r13 are `+FINDING:COREDUMP_NOTICE_JOURNAL_USER +FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER +FINDING:UNIT_FAILURE_OUT_OF_SCOPE +path -FINDING:WATCHDOG_STALE age_s io_avg_unavailable round`. This equals the entering JSON's `unclassified_vs_prior_register` (oracle: True).

## 3. check-register.py, exact outputs

Mandated:
```
$ python3 …/build/RegisterCheck/check-register.py …/corpus/evidence/drift-classification-r20.json …/.ufo/waves/round-20/evidence/c1-drift-entering.json
MORI_DRIFT_REGISTER: unclassified=0 invalid=0 regression=0 tokens=50
rc=0
```
Controls:

| Drift input | Output | rc |
|---|---|---|
| r10 pre-pin, first line (raw text) | `unclassified=0 invalid=0 regression=0 tokens=49` | 0 |
| r10 pre-pin, whole file | `unclassified=1 invalid=0 regression=0 tokens=50` | 1 (`rc=1` counted) |
| post-pin capture | `unclassified=2 invalid=0 regression=0 tokens=2` | 1 (`none`, `rc=0` counted) |
| r13 register vs entering | `unclassified=50 invalid=43 regression=0 tokens=50` | 1 (no schema; string values) |

## 4. Token-splitting assumptions attacked

| # | Assumption | Test and evidence | Verdict |
|---|---|---|---|
| T1 | Space is the only delimiter (`tr ' '`) | Census joins tokens with one space (`tools/mori-census.sh:2872`, `:2917`; header at `:3001`). No tab, CR, or non-ASCII/control char in any of the 4 captures. Contract model equals `str.split()` model in all 4 | HOLDS for these inputs |
| T2 | `grep -v '^MORI_DRIFT:$'` removes the header | Entering 51 words → 50 tokens; r10 line 1 50 → 49 | HOLDS |
| T3 | A capture is one line | r10 pre-pin file line 2 is `rc=1`. Whole-file input adds it as a token (r20: 1) | BROKEN as written. The frozen text does not say to drop the trailer |
| T4 | `MORI_DRIFT: none` means zero tokens | Census prints it at `:2995`. Both tools count `none` and `rc=0` as tokens; post-pin reads as 2 unclassified | BROKEN. A clean capture cannot be expressed |
| T5 | `sort -u` and `comm` share one collation | §2 | BROKEN under default locale |
| T6 | Bare names are GNU tools | They are builtins; `jq` is jaq 3.1.1. Key lists match jq 1.8.2 exactly (42/42, 50/50, `diff` rc 0). C-mode counts match GNU C-mode | HOLDS for counts. Not reproducible unless binaries are named |
| T7 | `comm -23` catches stale register keys | r20 keys equal entering tokens (50 = 50). r13 keys all present in entering (42). A key orphaned by a future capture is never reported | HOLDS now. Gap by construction |
| T8 | Two captures are "the same captured drift output" | Entering − pre-pin = `{-FINDING:WATCHDOG_STALE}`; pre-pin − entering = ∅. The 8 and the 7 are counts on different states | BROKEN as stated (§5.1) |

## 5. Classification judgement (what the count cannot settle)

5.1 Mechanism, observed:
- Census STALE rule, `tools/mori-census.sh:733-736`. Text identical in the r10 blob `5be8943:522-525`: `age = now − mtime(watchdog.log)`; `age > 900` → `FINDING WATCHDOG_STALE`. No other input.
- `.ufo/watchdog.log` (fleet root): last `tick=` is line 402, `2026-10-15T01:58:27-03:00 tick=2`. 70 `tick=` lines total, none later. Last line 585, `2026-10-21T07:23:21-03:00 launch kagi … driver=hyaku-inline`. Log mtime 07:23:21.68. `scripts/hyaku/inline.sh:103` writes these launch lines (96 total).
- Timeline (`stat`): entering capture written 07:22:34; last append 07:18:05, so age ≤ 269 s, STALE absent, token `-FINDING:WATCHDOG_STALE`. Pre-pin written 07:53:07; last append 07:23:21, age ~1700–1790 s, STALE present, token absent. Post-pin 07:55:31: `MORI_DRIFT: none`. Both windows sit on the same side of 900 s whatever the probe's exact instant.
- The r20 baseline records `FINDING WATCHDOG_STALE` present (line 39; `pinned_ts=2026-10-21T10:53:07Z`).
- So a daemon with no tick since 2026-10-15 reads "not stale" after any unrelated append inside 900 s. [INFERENCE: mechanism from code and timestamps. Census output for those instants was not retained.]

5.2 Register: `-FINDING:WATCHDOG_STALE` is `live-state`. Its `blind_spot` concedes that the log-mtime proxy "no longer measures daemon liveness once another writer appends". The top-level `dissent` (VolatileContract H2/H3, C1Critic) argues `census-regression`. `-FINDING:WAVE_UNSETTLED_AGE` is also `live-state` (not verified here, §8).

5.3 The contract names the four classes but does not define them (`contract.md` lines 24-28). The live-state / census-regression boundary is therefore an undocumented L1 choice.

5.4 The rebuttal's premise is false at file level. The register's `dissent` says "census code byte-identical since r10". The census blob at the r10 pin (`5be8943`, `d7710981…`) was changed by seven later commits (`1f07f1d`, `18d7d55`, `8d22d18`, `26f6589`, `273aa74`, `2be8294`, `fe9fa90`), ending at `87b8d680…`. The narrower claim, that the STALE rule text is unchanged since r10, holds.

5.5 Forward risk [INFERENCE]: the next `hyaku-inline` launch makes STALE absent and drift non-`none`. The r20 baseline is therefore not stable for this token. "Post-pin none" (07:55:31, about 1 minute after the baseline write at 07:54:21) is a same-state check, not a stability window.

## 6. Evidence pointers

- Path pointers: 18 lane-relative. 15 resolve under the lane root. 3 resolve only under the fleet root (`scripts/hyaku/inline.sh`, `scripts/shokunin-watchdog.sh`, `.ufo/reports/round-24/kagi.md`). The pointer base is undeclared.
- Hash-like pointers: 17. 16 resolve as commits. Lane: 1439c47, 18d7d55, 1f07f1d, 26f6589, 5be8943, 8d22d18, d30b4e4. Fleet: 01d1c22, 1bcf59e, 1eed508, 204807e, 417b1c2, 4487889, 7bf2b1a, 9a28017, e20f4fa. The 17th is the date `20261018` inside a directory name.
- `check-register.py` checks only non-empty `reason` and `evidence` strings. It does not resolve any pointer.
- Register: 29 census-schema-change, 19 live-state, 2 roster-change, 0 census-regression. Declared `class_counts` equals computed. No empty or multi-line entries.
- No retained round-20 evidence records a counting-command output. `c1-drift-entering.json` records `unclassified_count: 8` with no producing command or locale. The 0 is reproduced here, not retrieved.
- Low: baseline file name `…20261021T1051Z` versus header `pinned_ts=…T10:53:07Z`.

## 7. Recommendations (nothing applied; contract is frozen)

1. Add `export LC_ALL=C` to the counting command, or put `LC_ALL=C` on the first `sort` (variant e is the tested minimum). Record the amendment and re-run.
2. Define DRIFT as the first stdout line. Exclude `rc=` lines. Treat `MORI_DRIFT: none` as zero tokens, in the command or in the checker.
3. Write the live-state / census-regression criterion into the register. Replace "census code byte-identical since r10" with the rule-level identity actually shown (STALE text). Record the STALE blind spot in the re-pin reason.
4. Record the entering capture's start second (its JSON says it was not recorded). Declare the pointer base.

## 8. Residual risk and gaps

- Not verified: the `WAVE_UNSETTLED_AGE` dissent ("probe_waves byte-identical since r10"). Its evidence, fleet commit `e20f4fa` and `souji-shokunin/census/operator-sweep-20261018/approval-list.tsv:56-73`, was not opened.
- Census not executed (bounds). Entering and pre-pin STALE states are inferred from code and timestamps, not observed.
- Locale of the L1's original count run is unknown. No frozen artifact records it.
- At 08:08 -03 the log age was ~45 min, so STALE would be emitted now. Not confirmed by running the census.

## 9. Bounds and tooling

- No installs or updates. Binary identities recorded in §2a and T6.
- Read-only. Lane inputs untouched. Git used only for `show`, `log`, `rev-parse`, `cat-file`. No `.jj/`, `.ufo/interactive-sessions/`, `.ufo/worktrees/` or session logs read. Fleet `.ufo/watchdog.log` and `scripts/hyaku/inline.sh` read only.
- Scratch under `.ufo/waves/round-20/falsify/CountC1/`: `repro-count.sh`, `oracle.py`, `census-history.sh`, `pointer-hashes.sh`, `census-r10-5be8943.sh` (git blob copy), `drift-entering.stdout.txt`, `drift-r10-prepin.line1.txt`, `unclassified.*`, `stderr.*`, `first-input.*`.
