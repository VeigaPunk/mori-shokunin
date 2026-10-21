# HistR12: C1 census-regression hunt, commit 1f07f1d (`tools/mori-census.sh`)

Scope: read-only review of round-12 commit `1f07f1d` (census SHA `d7710981…` to `3da5b098…`) against c1 drift evidence measured at `2061780` (census SHA `87b8d680…`, which equals the working-tree file, the contract pin, and HEAD `e4d9384`, which has no later census commit). Nothing was executed except one bash regex test on sample strings. The census, selftest, oracle and drift were not run.

Citation conventions: `path:line` is the committed file at `1f07f1d` unless marked `@2061780`. Declarations are the `1f07f1d` versions of the round-12 records. `a7f1ecb` (post-review, same round) later added text to `roster-truth-r12.md`, `LOG.md` and `SCORECARD.md`; those additions are not counted as declarations. Scratch copies and saved diffs are in `.ufo/waves/round-20/build/HistR12/at-1f07f1d/` (byte copies of `git show` output).

## 1. Result

1. `1f07f1d` changes default census output in three ways, all declared in round 12: 14 new `SURFACE lane.*` rows (roster 9 to 23), six new keys on the `SURFACE silence` row, and one new info finding `ROSTER_SET_MISMATCH`. No existing default line is removed. The only default-output consequence not stated in round 12 is the verdict count (C-1). **On the evidence, no token attributable to 1f07f1d is a census regression.**
2. Of the 50 c1 tokens, **21 are introduced by 1f07f1d** (section 3.1). Eight more were already present in the pre-round-12 live state and were classed as non-regressions at the time (section 3.2). The other 21 first appear after 1f07f1d (section 3.3); round-13 commit `18d7d55` explains nine of them.
3. Candidate census-regressions, none observed in the measured run:
   - **C-1 (low, undeclared):** the verdict `findings=` count rises by one per roster mismatch. Round 12 never states it, and `--drift` cannot see it.
   - **C-2 (latent, contradicts a declaration):** conf rows can be skipped with no count (IDs outside `[a-z0-9-]`, indented rows, rows after an in-block quote). The declaration says invalid IDs are "dropped and counted".
   - **C-3 (latent, roll-affecting, undeclared):** 14 newly graded lanes can now raise warn-level `LANE_SILENT`, which flips DRIFT.
4. Undeclared non-output defects: N-1, `LANE_SILENT` removed from the stable finding catalogue although still emitted; N-2, `MORI_ROSTER_LANES` removed from the env catalogue although still honored; N-3, an erratum saying every token is classified, which the same commit's after-roster run contradicts. N-1 and N-2 are still present at `2061780`.

## 2. Behavior changes in 1f07f1d and their declarations

The 214-insertion, 6-deletion diff of `tools/mori-census.sh` has nine hunks. Each is listed below.

| ID | Change at 1f07f1d | Affects default output | Declared at 1f07f1d | c1 tokens |
|---|---|---|---|---|
| B1 | Silence roster now comes from env override, else conf plus state (`ROSTER_SOURCE`); `ROSTER_LANES` default is empty (`:313`, `:386-497`, `:472-473`). | Yes: `SURFACE lane.*` rows 9 to 23 | `LOG.md:661-663`; `SCORECARD.md:605`, `:628`; `corpus/knowledge/roster-truth-r12.md:3,13,19`; `SKILL.md:20`; `corpus/README.md:35` | +SURFACE:lane.* x14 |
| B2 | New `ROSTER_SET_MISMATCH` info when both sources are readable and differ (`:494`; catalogue `:232`). | Yes: 1 info finding. Live: conf_only=kotodama,souji; state_only=audio,game-dev-2d,game-dev-3d | `LOG.md:662-663`; `SCORECARD.md:605`; `roster-truth-r12.md:21`; `SKILL.md:20` | +FINDING:ROSTER_SET_MISMATCH |
| B3 | `SURFACE silence` detail gains `roster_source roster_n conf_n state_n conf_dropped_n state_dropped_n` ahead of `silent=` (`:1571`). | Yes | `roster-truth-r12.md:19`; `LOG.md:662`; `SKILL.md:20` | +roster_source, +roster_n, +conf_n, +state_n, +conf_dropped_n, +state_dropped_n |
| B4 | Roster fields deliberately non-volatile (comment `:1757-1758`). Not added to `DRIFT_COUNTER_KEYS` (`:1763-1772`) or `DRIFT_VOLATILE_SPECIAL` (`:1774`). | Visibility only | `roster-truth-r12.md:21` | none; keeps B1 to B3 visible |
| B5 | Every emitted finding, info included, increments `N_FINDINGS`; only warn or crit increments `N_DRIFT` (`:360-369`). Verdict printed at `:1733-1734`. | Yes: `findings=` +1 per B2 | **Not declared.** `LOG.md:643-673` and `SCORECARD.md:594-631` contain no findings-count statement. | none; `findings` is masked (`:1764`) |
| B6 | Lane rows follow config order, then state-only IDs sorted (`:472-473`). | Yes, order only | `roster-truth-r12.md:19` | none; drift compares multisets first |
| B7 | Builtin nine used only when neither source gives a valid ID (`:466-470`). | Only if both empty; not live | `roster-truth-r12.md:19` | none |
| B8 | Conf read as data, only inside `LANES="..."` blocks; state symlinks skipped; invalid state IDs counted (`:404-438`). | Parse rules | `roster-truth-r12.md:19,27-36`; roster selftest cases | none |
| B9 | `MORI_ROSTER_LANES` used without validation (`:397-402`; still `:455-458` at `2061780`). | Env only | `LOG.md:693` (routed to r13) | none |
| B10 | Silence probe grades 23 lanes; wall time about 1.9 s to 4.3 s (follows B1). | Runtime only | `SCORECARD.md:612`: "unchanged" score disputed by the critic seat, "operator to rule" | none |
| B11 | Selftest +11 roster cases (66 to 77). Fixture pins `MORI_FLEET_CONF` and drops explicit `MORI_WATCHDOG_LOG` and `MORI_STATE_DIR` (`:2166-2169`; parent `:2040-2043`). | Selftest only | Cases: `LOG.md:664`, `SCORECARD.md:629`; selftest log ends `77 cases, 77 passed, 0 failed`. The fixture edit is **not declared** (N-5). | none |
| B12 | Header docs: `MORI_ROSTER_LANES` line replaced by `MORI_FLEET_CONF` (`:219`); `LANE_SILENT` line replaced by `ROSTER_SET_MISMATCH` (`:232`). | Docs only | **Not declared** (N-1, N-2) | none |

## 3. Drift-token attribution (c1, 50 tokens, `.ufo/waves/round-20/evidence/c1-drift-entering.json` lines 13-62)

The round-12 "after-roster" run is the direct test. It is `drift-r12-20261019T2230Z-after-roster.log` line 2, with `census_sha256=3da5b098…` (the 1f07f1d census). Tokens in c1 but absent from that line were not introduced by 1f07f1d. Tokens in that line are either roster tokens (3.1) or pre-existing (3.2).

### 3.1 Introduced by 1f07f1d: 21 tokens, all explained by B1 to B3

- B2: `+FINDING:ROSTER_SET_MISMATCH`.
- B1: `+SURFACE:lane.audio`, `chousa`, `game-dev-2d`, `game-dev-3d`, `kaidoku`, `kotodama`, `lore`, `mado`, `mori`, `revenger`, `souji`, `tabi`, `tameshi`, `tsukuroi`. That is 14 rows: 9 extra conf IDs, 2 conf-only (kotodama, souji), and 3 state-only (audio, game-dev-2d, game-dev-3d). Sets are in `roster-truth-r12.md:9-13`.
- B3: `+roster_source`, `+roster_n`, `+conf_n`, `+state_n`, `+conf_dropped_n`, `+state_dropped_n`.

None of the 21 is in the round-13 "unclassified" list (c1 lines 65-74). The round-13 register classifies all 21 as "r12 roster schema carried since r10" (`.ufo/waves/round-13/evidence/drift-classification.json:7,11-32`). That label is inaccurate: the fields did not exist at the r10 pin (census `d7710981`, which is `1f07f1d^`). It also has no evidence pointer.

Why these are not regressions: all 9 builtin lanes remain (no `-SURFACE:lane.*` token). The 1f07f1d run shows `drift=12` both before and after, so the info finding does not change the roll. The round-12 classification (`drift-r12-20261019T2230Z-after-roster.log:3`) calls the 14 rows and roster fields "the intended round-12 roster change (claim 3)". Nothing is removed from the silence row. The 1f07f1d selftest passes 77/77 (`roster-r12-20261019T220912Z-selftest.log`).

### 3.2 Pre-existing live state, carried through 1f07f1d: 8 tokens, not introduced by 1f07f1d

`+FINDING:UNIT_FAILURE_OUT_OF_SCOPE`, `-FINDING:KILL_SIGNAL_JOURNAL`, `-FINDING:WAVE_UNSETTLED_AGE`, `-attribution`, `-example`, `-rowb_files`, `basis`, `obs`.

All eight appear on the after-roster line. `drift-r12-20261019T2204Z-classification.md:29-39` classifies each as live-state or aging ("No" regression, or "evidence-strength downgrade"), and line 4 states "no token is a census regression". `SCORECARD.md:613` and `LOG.md:670-672` say the same. Caveat: the `UNIT_FAILURE_OUT_OF_SCOPE` emitter was rewritten later. `18d7d55` removes the old emission (saved diff line 396), and `@2061780` emits it again under new semantics (`:1493-1495`). The token still reflects a live-state change against the r10 baseline.

### 3.3 First seen after 1f07f1d: 21 tokens

Traced to `18d7d55` (round 13), 9 tokens. Line numbers are in the saved diff `at-1f07f1d/18d7d55-census.diff`.
- `HEADER`: `VERSION=census-r5` to `census-r6` (diff lines 69-70).
- `volatile_fields`: `DRIFT_VOLATILE_SPECIAL` gains `boot` (diff 516-517); counter list edited (diff 503-513).
- `+SURFACE:journal.system`, `+SURFACE:journal.user`, `-SURFACE:journal`: per-scope journal surfaces (diff 400-419).
- `+FINDING:JOURNAL_CLASSES_UNMEASURED` (diff 285); `+FINDING:COREDUMP_NOTICE_JOURNAL_USER` (diff 260); `+FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER` (diff 262); `-FINDING:SEGFAULT_JOURNAL` (diff 390).

Not traced by this seat, 12 tokens: `+FINDING:WATCHDOG_STATE_LAG`, `-FINDING:WATCHDOG_STALE`, `+gate_s`, `+path`, `+reason`, `+window`, `-window`, `+subject_commits`, `-subject_commits`, `age_s`, `io_avg_unavailable`, `round`. None is introduced by 1f07f1d. No 1f07f1d hunk touches their emitters or keys (section 2 enumerates all nine hunks), and none is on the after-roster line. `age_s` is volatile at 1f07f1d (`:1774`).

## 4. Default-output changes not declared: flagged as candidate census-regressions

**C-1 (low, undeclared): verdict `findings=` +1 per roster mismatch.**
- Code: `:363` (`N_FINDINGS` increments on every emit), `:1733-1734` (printed), `:1764` (`findings` is a DRIFT counter key, so `--drift` masks it).
- Measured: before-live (`roster-r12-20261019T220912Z-before-live.log`) `findings=13 drift=12`; after-roster final line `findings=15 drift=12`. The +2 is B2 (+1) plus the live `SEGFAULT_JOURNAL count=1` (+1), which the after-roster log discloses at line 3.
- Declared: no round-12 narrative statement (`LOG.md:643-673`, `SCORECARD.md:594-631`).
- Disposition: not a regression by construction (info, `drift` unchanged). L1 should declare it as roster-change or classify it. It must not block the re-pin.

**C-2 (latent, contradicts a declaration): conf rows silently skipped.**
- Declaration: `roster-truth-r12.md:19` says "Invalid IDs are dropped and counted."
- Code: `:415` matches only lines beginning `[a-z0-9]` followed by `[a-z0-9-]*|`. `:417-418` count only rows that match `:415` and fail the 48-character check. Rows with uppercase, underscore, dot, or leading whitespace are never matched and never counted.
- Test, bash `[[ =~ ]]` on sample rows (not the census): `kagi|x|y` MATCH; `My_lane|x|y`, `kagi_x|x|y`, `Kagi|x|y` NOMATCH, so silently skipped.
- Code reading, `:424`: any `"` in a row closes the LANES block. Rows after it in the same block are skipped with no count. This follows the documented rule (`roster-truth-r12.md:31-32`) but the skips are uncounted.
- The state side is sound: `:435-437` counts every invalid `*.round` name.
- Selftest gap: the only invalid-ID case is a 50-character lowercase ID (`:2382`, `:2390`). The charset path is untested.
- Not triggered at 1f07f1d: all 20 live conf IDs match the class (`roster-truth-r12.md:9`), and `conf_dropped_n=0` in `roster-r12-20261019T220912Z-live.log`.
- Risk: a lane can vanish from the roster with no count and no finding. L1 needs a ruling on whether this is a candidate census-regression.

**C-3 (latent, roll-affecting, undeclared): LANE_SILENT exposure for 14 new lanes.**
- Code: the loop at `:1548-1550` grades every roster lane. Row D emits `LANE_SILENT` as warn at `:1554`, which increments `N_DRIFT` (`:367-369`) and flips the roll. 1f07f1d grades 23 lanes instead of 9.
- Declared: `LOG.md:661-667` and `SCORECARD.md:605`, `:611` claim coverage ("14 lanes graded") but never state the roll consequence.
- Observed: no `LANE_SILENT` in the before or after logs (`silent=0`) and none among the c1 tokens.
- [INFERENCE] none of the 14 is silent at `2061780`. This is latent, not measured.

## 5. Non-output findings

- **N-1 (undeclared, doc contract).** `LANE_SILENT` is missing from "Finding ids (stable compare contract)" (`:224-234`). The hunk at `@@ -229` replaces the `LANE_SILENT` line with `ROSTER_SET_MISMATCH` rather than inserting it. Emission is unchanged at `:1554`, and `:1228` calls it "the ONLY LANE_SILENT emission". Still absent from the header at `@2061780` (header lists `ROSTER_SET_MISMATCH` at `:271`; emission at `:2525`).
- **N-2 (partly declared).** `MORI_ROSTER_LANES` is removed from the env list (`:216-219`) but still honored (`:397-402`; `@2061780` `:455-458`). It is documented only in `SKILL.md:20`. The residual, that the value is unvalidated, is open in `LOG.md:693`. At `@2061780` `:455-458` still has no validation.
- **N-3 (stale declaration).** `corpus/knowledge/drift-pin-r10.md:299-300`, added in 1f07f1d, says every token "is classified in drift-r12-...-classification.md — no census regression". The same commit's after-roster run adds 21 tokens that doc does not cover. `SCORECARD.md:613` and `LOG.md:670-673` state this correctly.
- **N-4 (stale pointer).** `roster-truth-r12.md:1` cites `tools/mori-census.sh:312-319,383-489,1530-1563`. The code is at `:312-319`, `:386-497`, `:1541-1548`, and the silence row at `:1571`, which is outside the cited range. Line 36 of the same file gives the correct `386-497`.
- **N-5 (undeclared, neutral).** B11 fixture edit. Removing `MORI_WATCHDOG_LOG` and `MORI_STATE_DIR` is behavior-neutral: defaults derive from `MORI_UFO_DIR`, which the fixture still sets (`:2168`; defaults `:259`, `:264`).
- **N-6 (declared, disputed).** B10 runtime: about 1.9 s to 4.3 s (`roster-r12-20261019T220912Z-walltime.log`). `SCORECARD.md:612` keeps operability "unchanged" while the critic disputes it. It is not a census output change.

## 6. Proposed classes for the 21 section-3.1 tokens (L1 decides; contract classes per `contract.md:23-28`)

| Tokens | Proposed class | Evidence pointer |
|---|---|---|
| 14 `+SURFACE:lane.*` rows | roster-change | `1f07f1d:tools/mori-census.sh:386-497`; `LOG.md:661-663`; `roster-r12-20261019T220912Z-live.log` (`count=23`) |
| 6 roster keys | census-schema-change | `1f07f1d:tools/mori-census.sh:1571`; `roster-truth-r12.md:19` |
| `+FINDING:ROSTER_SET_MISMATCH` | census-schema-change (trigger is live conf/state disagreement) | `1f07f1d:tools/mori-census.sh:494`; `roster-truth-r12.md:21` |

None of the 21 is a census-regression on this evidence. The register should not repeat "carried since r10" (section 3.1).

## 7. Gaps and [INFERENCE]

- Nothing was executed: no census, selftest, oracle or drift run. Values at `2061780` were not re-measured. The 23-lane roster at `2061780` is inferred from the token set (14 added lane tokens, no removals) [INFERENCE].
- Declarations cited are the `1f07f1d` snapshots. `a7f1ecb` later added text to `roster-truth-r12.md`, `LOG.md` and `SCORECARD.md`; those additions are not counted.
- C-2 and C-3 come from code reading. C-2's regex behavior was checked on sample strings, not against the census.
- Twelve post-1f07f1d tokens (section 3.3) are not traced to a commit.
- The live fleet has moved since the round-12 measurement. Roster counts in section 2 are the round-12 values.

## 8. Artifacts and actions

- Git: read-only use only (`git show`, `git log`, `git rev-parse`, `git show --stat`). No index, ref or working-tree change by this seat.
- Scratch under `.ufo/waves/round-20/build/HistR12/at-1f07f1d/`: census copies at `1f07f1d` and its parent; `LOG.md`, `SCORECARD.md`, knowledge notes, `SKILL.md` and the corpus README snapshots; the roster selftest log; saved diffs of `1f07f1d` and `18d7d55`.
- Fleet reads: `shokunin.conf` (grep) and `.ufo/state` (entry count only). No writes.
- Tool installs or updates: none. The pacman guard was respected and nothing needed installing.
- For L1: rule on C-1 and C-2 before any re-pin decision. C-3 needs a declaration or a fix. N-1 and N-2 are doc-contract fixes that do not change output.
