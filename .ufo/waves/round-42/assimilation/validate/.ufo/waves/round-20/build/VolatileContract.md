# C1 volatile contract and masking risk, round 20

- Seat: `MoriR20.VolatileContract` (leaf; no subagents).
- Scope: what a C1 re-pin would launder, which evidence rules each case out, and whether any token family should be declared volatile. Recommendation only.
- Bounds kept: no census run, no `--pin` or `--drift`, no selftest, no edits, no git or jj mutation, no installs. Live values come from files and read-only commands (section 9).
- Measured commit `2061780117e6` (lane entering tip). Census SHA `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28` matches the blob at that commit, the working tree, and HEAD (`e4d9384`).

## 1. Bottom line

1. **Declare no token family volatile this round.** The 50 entering tokens fall into six families (section 5). Each carries a signal the drift exists to show. A volatile declaration would also need an edit to `tools/mori-census.sh`, which C1 forbids and which would change the SHA the gate rests on.
2. **A re-pin under the current gate would launder at least 13 kinds of regression (section 3).** The gate counts changed tokens only. It cannot see standing warnings, input loss, positional pairing, first-word truncation, row-level content, environment, or a failing capture. Object-level, raw-value classification with an explicit acceptance rule would address most of them; the contract requires neither.
3. **Two tokens are not `live-state` on the evidence.**
   - `-FINDING:WATCHDOG_STALE`: the staleness check is fed by writes from launch drivers. The watchdog daemon has not ticked since 2026-10-15T01:58:27-03:00 and has no process (`pgrep -af shokunin-watchdog` rc 1 at 2026-10-21T10:35:15Z).
   - `-FINDING:WAVE_UNSETTLED_AGE`: commit `e20f4fa` deleted 17 `aggregator-r10*` paths, and the census now counts the remaining directories as empty.
   - Under the contract's closed set both are `census-regression`, which blocks the re-pin. This is my recommendation; the L1 decides. Labelling them `live-state` is the laundering the contract exists to prevent.
4. **Post-pin `--drift` would read `none` while the census rolls DRIFT.** The candidate carries 11 warn findings: `WATCHDOG_ABSENT` and ten `WAVE_UNSETTLED_AGE`. After a re-pin, `none` would mean "unchanged since pin", not "healthy".

## 2. How the comparison works (code facts)

- **Normalize** (`drift_normalize`, `tools/mori-census.sh:2776-2792`). Counter keys (`DRIFT_COUNTER_KEYS`, `:2744-2764`) are masked by `\b(KEYS)=[0-9]+` (`:2791`). `ts=`, `boot=` and `example=` use value-agnostic classes (`:2782`, `:2786`, `:2790`), so any value, including a sentinel, is masked. `age_s`, `mtime_age_s`, `*_epoch`, PSI, rates and `script_sha256` are masked by digit or hex shape (`:2781`, `:2783-2789`).
- **Recorded contract** is a string: `DRIFT_VOLATILE_SPECIAL` (`:2771`) plus the counter array (`:2772`). The sed rules are a separate hard-coded program. `volatile_fields` compares only the header string (`:2981`), so a rule change without a list change is invisible once re-pinned.
- **Capture.** `cap_census` stores `CENSUS_RC` (`:2798-2803`); nothing reads it. `run_census` exits 0, 1 or 2 by roll (`:2717-2721`). `run_pin` writes whatever it captured and exits 0 (`:2920-2938`).
- **Field scan** (`drift_scan`, `:2826-2843`). Each line is split on whitespace. Tokens without `=` are dropped (`:2836`), so only the first word of a multi-word value is compared. Duplicate keys are concatenated (`:2840`).
- **Pairing** (`drift_report`, `:2874-2918`). Pass 1: exact multiset match. Pass 2: same-id lines paired first-unused (`:2895-2896`). Pass 3: unmatched new lines reported by id only (`:2907-2910`). Tokens are sorted and de-duplicated (`:2916`). A field-free difference falls back to the line id (`:2866`).
- **Selftest drift arms** (`:4633-4705`): pin then drift, volatile churn, one `warn_pct` mutant, one finding-removal mutant, missing baseline, volatile-list rewrite. The only `--pin` run is on the healthy fixture (`:4654`).

## 3. Regression kinds a re-pin would launder

Each entry gives what hides the regression, the evidence that would rule it out, and status.

**K1. Standing warnings become the reference.** The r10 baseline pinned 14 warn lines (`corpus/evidence/baseline-r10-20261015T2231Z.json:24-38`: STALE, ABSENT, 11 WAVE, KILL). The candidate has 11 (`c1-pin-probe-scratch.json:52-62`: ABSENT and ten WAVE), and its roll is `DRIFT` (`:68`). The gate counts only changed tokens, so these become expected. *Ruled out by:* nothing in the current gate. It needs a per-finding acceptance with its own check (ABSENT: `pgrep` rc and last tick; each WAVE: directory listing), named in the round record, and a refusal to pin with an unaccepted warn or crit line.

**K2. The liveness check is blinded by a non-daemon writer.** `WATCHDOG_STALE` is `age > 900` on `.ufo/watchdog.log`, with age taken from mtime (`:733-736`). The same log receives launch-driver lines (`scripts/hyaku/inline.sh:103,130,136`). The first line after the last daemon tick is a `driver=hyaku` launch at `.ufo/watchdog.log:403` (2026-10-19T23:10:53-03:00). The last `tick=` line is `:402` (2026-10-15T01:58:27-03:00); no later line matches `tick|watchdog`. `pids=` and `age_s=` are masked (`:2745-2748`, `:2783`). After masking, the watchdog SURFACE line is identical to r10. *Ruled out by:* classifying `-FINDING:WATCHDOG_STALE` as `census-regression` (observability loss), not `live-state`. The census SHA cannot help: the gap is in the design. The arm at `:3500` covers STALE on a fixture log, not a driver-written log.

**K3. Input loss mapped to live state.** A wave is `WAVE_UNSETTLED_AGE` only if it has a launch marker and no settlement marker. Directories without markers count as `empty` (`:890-926`). `empty=`, `age_unreadable=` and `aged_unsettled=` are masked (`:2745`). Commit `e20f4fa` deleted 17 `aggregator-r10*` paths (`corpus/lessons/round-12.md:40`; `corpus/evidence/drift-r12-20261019T2204Z-classification.md:30`). Today `aggregator-r10-resume/` has no files and `aggregator-r10/` holds only `seats/` (glob). The r12 receipt already says the disappearance "does not prove settlement" (`:33`). *Ruled out by:* `census-regression` (coverage loss) with a per-wave listing taken at measurement time. A `live-state` label launders it. The selftest checks the empty-directory rule on fixtures, not the live inputs.

**K4. Positional pairing turns an appearance into a field change.** Pass 2 pairs the base `aggregator-r10` row with the new `shokunin-train-20261016-w24` warn row (appendix A). The only token is `obs`; there is no `+FINDING:WAVE_UNSETTLED_AGE`. A new unsettled warn therefore reads as an `obs` edit. *Ruled out by:* none of the three evidence types. It needs register rows keyed by (line id, object key `wave=`/`lane=`, field).

**K5. First-word truncation and co-occurrence suppression.** The `io_avg_since_boot` tail `nvme0n1p1:<V>Bps/<V>s` is dropped (`:2836`). The only token on that line is `io_avg_unavailable`. A tail-only change reports the bare line id, and nothing if another field on the line changed (`:2866`). I verified this offline with synthetic and live cases. The `targets=` tail `/tmp` is equally invisible. `corpus/knowledge/drift-pin-r10.md:97` says device changes are drift; that holds only for the first device. *Ruled out by:* nothing. It needs raw-line diffs for multi-entry values in the register; the fix is a later census change.

**K6. Row granularity.** Added and removed lines are reported by id only (`:2907-2910`), and tokens are de-duplicated (`:2916`). The 34 added rows collapse to 22 tokens. The 13 `WATCHDOG_STATE_LAG` rows collapse to one token. `journal.user` and `journal.system` each carry dozens of unmasked fields and become one token each. *Ruled out by:* classifying each row with every field enumerated. Neither per-token class nor SHA reaches it.

**K7. Mask-list and rule widening absorbed by the re-pin.** Between r10 and now the recorded list lost three counters (`kill_signal`, `segfault`, `unit_failure`; none is emitted now) and gained 36 counters (`18d7d552b4`: +6/-3, plus `boot` in the special list; `8d22d18fb4`: +20; `26f6589dfa`: +10). The sed program gained one rule (`boot=`, `:2786`). The new header records only the new list. After a re-pin, the r10 delta survives only in the frozen r10 file and in the register. *Ruled out by:* classifying the `volatile_fields` token and the list delta, with commit pointers, before the pin (they are visible until then). The SHA fixes the list for this measurement only. The `volatile_fields` arm (`:4701-4703`) proves detection, not correctness. A future sed-only change is invisible after a re-pin.

**K8. Retired ids and a declared coverage reduction.** `KILL_SIGNAL_JOURNAL` is emitted only when positive (`:1630`, inside a conditional closed at `:1631`). `SEGFAULT_JOURNAL` is retired. Its successor `SEGFAULT_SIGNAL11_JOURNAL_USER` counts a structured field (`:1327`), not the retired text heuristic. `JOURNAL_CLASSES_UNMEASURED` (`:1377`, unconditional, info) states that four classes are unmeasured. A re-pin turns "unmeasured" into normal. *Ruled out by:* successor pointers and an explicit acceptance of the coverage reduction. Positive arms exist for KILL (`:3600`, `:3601`, `:3678`, `:3833`, `:3844`), SEGFAULT_SIGNAL11 (`:3598`, `:3599`), COREDUMP (`:3596`, `:3597`) and UNIT_FAILURE_OUT_OF_SCOPE (`:3646`, `:3663`). None exists for JOURNAL_CLASSES_UNMEASURED; it appears only at `:1377` and as an exclusion at `:3737`.

**K9. Attribution strength read as state.** `basis` changes per lane, and `attribution`, `example`, `rowb_files`, `subject_commits` and `window` appear or disappear with it (appendix A). The aggregator went row-B (inference, in r10) to row-C (r12, the evidence downgrade the r12 receipt records) to row-A now (subject commits in window). Kagi, kake and kengaku moved to row-6 (committed report), kumitate to row-4 (ledger close), and kama to row-8 (young). *Ruled out by:* per-lane pointers that re-derive the basis from the lane's own read-only `cmd=`. The r13 register's `[INFERENCE] ... no re-pin/admission claim` reasons are not pointers.

**K10. A failing or partial capture is accepted.** `CENSUS_RC` is never read. A roll other than CLEAN or DRIFT exits 2, but `run_pin` still writes the capture and exits 0 (`:2717-2721`, `:2936-2937`). *Ruled out by:* an rc and verdict-line check before writing, plus classifying the pinned capture itself (section 6, O3). The contract requires neither.

**K11. Environment baked into thresholds and roster.** The header records no environment (`:2925-2930`). `MORI_*` overrides change unmasked values: `stale_threshold_s`, `warn_pct`, `crit_pct`, `psi_warn_avg10`, `window_s`, `gate_s`, and the roster (`:350-369`). Observed: this seat's shell has no `MORI_*` variables, and the candidate's threshold tokens equal the source defaults (900, 85, 95, 10, 7200, 7200). *Ruled out by:* recording the pin run's environment. The selftest runs under `env -i` (`:3296`), so it does not reach the live environment.

**K12. Masked magnitudes and sentinel masks.** Counters are masked by `\b(KEYS)=[0-9]+` (`:2791`), including `pids` (`:2748`), `empty`, `age_unreadable`, `aged_unsettled`, `unavailable` (`:2751`), `positive_*` (`:2760-2763`) and `unit_*` (`:2753-2759`). Observed: the `waves` SURFACE line is byte-identical to r10 after masking, while two aggregator directories stopped counting as unsettled (no markers; r12 section A). *Ruled out by:* nothing; magnitudes never reach drift output. The r10 doc requires the raw capture beside the baseline (`corpus/knowledge/drift-pin-r10.md:250-252`); none is retained for r20.

**K13. Masked logic changed in the seven census commits since r10.** `git log 5be89432ab..2061780 -- tools/mori-census.sh` lists seven commits: `1f07f1dd1e`, `18d7d552b4`, `8d22d18fb4`, `26f6589dfa`, `273aa74ab7`, `2be8294082`, `fe9fa9083d`. They changed journal classifiers, unit routing and counters. Drift is structurally blind to masked logic. *Ruled out by:* only the selftest, for the fixtures it covers (121 `check` call sites by static count; the executed count is not observed; the r10 PASS count was 66). It needs a review of those seven diffs for counter-producing paths, which this seat did not do.

## 4. Which evidence rules each kind out

| Kind | Per-token classification | Census SHA unchanged | Selftest PASS |
|---|---|---|---|
| K1 standing warnings | No | No | No |
| K2 liveness blinded | Only if classed census-regression | No | Partly (fixture arm) |
| K3 input loss | Only if census-regression | No | Partly (fixtures) |
| K4 positional pairing | No (no object identity) | No | No |
| K5 tail truncation | No | No | No |
| K6 row granularity | Only per row | No | No |
| K7 list and rule widening | Yes, before the pin; no trace after | Partly (this measurement) | Partly (detects, does not judge correctness) |
| K8 retired ids and coverage | Yes, with successor pointers and acceptance | Partly | Partly (none for JOURNAL_CLASSES_UNMEASURED) |
| K9 attribution | Yes, only with per-lane pointers | No | Not checked |
| K10 failing capture | Partly (only if the pinned capture is classed) | No | No |
| K11 environment | No | No | No (hermetic `env -i`) |
| K12 masked magnitudes, sentinels | No | No | No (by design) |
| K13 masked logic | No | Fixes the measured version only | Partly (fixtures) |

Summary: K1, K4, K5, K11 and K12 are reached by none of the three evidence types. The SHA gate is necessary, but it does not show the code is correct. The selftest proves the mechanism, and a re-pin passes it by construction, because the pin-then-drift arms are self-referential.

## 5. Volatile-family recommendation

All 50 tokens (`.ufo/waves/round-20/evidence/c1-drift-entering.json:12-63`) fall into six families. Provenance comes from the offline reproduction in section 6 (O3).

| Family | Tokens | Volatile? | Proposed class (L1 to confirm) | Reason |
|---|---|---|---|---|
| F1 roster and silence fields | 21: `+FINDING:ROSTER_SET_MISMATCH`, 14 `+SURFACE:lane.*`, six `+` silence keys | No | roster-change; census-schema-change for new keys | Roster is behaviour by design (`tools/mori-census.sh:2738-2739`). Live: conf 23, state 21 (silence row). |
| F2 journal surfaces, finding ids, version, mask contract | 11: `±SURFACE:journal*`, journal `±FINDING` ids, `JOURNAL_CLASSES_UNMEASURED`, `HEADER`, `volatile_fields` | No | census-schema-change; `-FINDING:KILL_SIGNAL_JOURNAL` is live-state | Finding ids are the compare contract (`:254`). `HEADER` is the version marker (`VERSION=census-r6`, `:281`). `volatile_fields` must stay visible. KILL absence means no kill events this boot (`:1630`). |
| F3 attribution strength: `basis`, `subject_commits`, `window`, `attribution`, `example`, `rowb_files` | 8 | No | live-state with per-lane pointers | These carry evidence strength. `example` stays masked as it is now (`drift-pin-r10.md:152`). |
| F4 lane lifecycle shape: `age_s`, `round`, `reason`, `path`, `gate_s` | 5 | No | census-schema-change (`reason`, `path`, `gate_s`, second `round=`); live-state (`age_s=-`) | Counter values are already masked. The `-` shape must stay visible; `:2783` matches digits only. The second `round=` key is a census naming defect to fix later, not a volatility question. |
| F5 watchdog and wave state: `WATCHDOG_STATE_LAG`, `WATCHDOG_STALE`, `WAVE_UNSETTLED_AGE`, `obs` | 4 | No; do not mask `obs` | LAG: live-state. STALE: census-regression (K2). WAVE: census-regression (K3). `obs`: decompose into rows (K4). | These are the only visible liveness signals. Masking them hides the daemon outage. |
| F6 device | 1: `io_avg_unavailable` | No | live-state | `/tmp` is now xfs on `/dev/nvme0n1p1` (`findmnt`); r10 recorded `tmpfs:not-a-block-device`. Device identity is the signal (`drift-pin-r10.md:97`). |

**Decision: declare none.**
- The families that churn (F3 `basis`, F4 `round`, F5 LAG and `obs`, F6) churn and carry signal. Masking them would turn red into green, which `drift-pin-r10.md:243-246` forbids.
- The defects that matter (K4, K5, K6, and the duplicate key in F4) can only be fixed in the census, which C1 does not allow this round.
- Masked families that already exist (ts, age_s, epochs, PSI, rates, counters, script_sha256, example) stay as they are.
- Candidates for a later census revision, not C1: rename the second `round=` key on not-open rows; key pairing by object identity; parse multi-entry values to the next key; record a fingerprint of the normalize rules in the header and compare it; tighten the `ts=`, `boot=` and `example=` masks to shapes; add positive arms for standing-warn pins, non-daemon log writers, same-id remove-and-add pairing and multi-entry tails; give the daemon-liveness check its own heartbeat and expose `pids`; record `CENSUS_RC` and refuse pins on a non-CLEAN/DRIFT roll or a missing verdict line.

## 6. Verified observations

- **O1. SHA gate.** `git show 2061780:tools/mori-census.sh | sha256sum` gives `87b8d680...ab28`, the same as the working tree. `2061780` is an ancestor of HEAD `e4d9384`. The newest census commit, `fe9fa9083d`, is at or before `2061780` and has the same blob.
- **O2. Revision count.** Seven census commits lie between `5be89432ab` (d7710981, the r10 pin) and `2061780`. The contract says "nine census revisions" (`.ufo/waves/round-20/contract.md:12`). Not reconciled.
- **O3. Offline reproduction.** A Python port of `drift_scan`, `drift_report` and the `run_drift` equality test, applied to the r10 baseline and to the 10:22:12Z candidate pin (`c1-pin-probe-scratch.json`, same SHA), yields exactly the 50 entering tokens, with no difference. The token set did not change over the 3.2-hour gap. Values were not compared: the entering stdout is one JSON line, and no raw capture is retained. The port passes its sanity check (candidate against itself gives `none`).
- **O4. List consistency.** The r10 header equals the r10 source list. The candidate header equals the current source list (103 tokens). The recorded-list mechanism works; its content is what K7 concerns.
- **O5. Daemon.** Last tick at `.ufo/watchdog.log:402` (2026-10-15T01:58:27-03:00). The session began with `tick=1` at 01:50:57 (`:401`). No tick line follows. `pgrep -af shokunin-watchdog` returned rc 1 at 2026-10-21T10:35:15Z. The 21 `.ufo/state/*.round` files (equal to `state_n=21`) were last written 2026-10-15 01:45:42 to 01:50:57 -03:00, on the same clock as the `tick=1` lines (`:364`, `:401`). Log writers include `scripts/shokunin-watchdog.sh:66` and `scripts/hyaku/inline.sh:103,130,136`. The log mtime is 2026-10-21 07:23:21 -03:00, set by a `launch kagi` line (`:585`).
- **O6. Waves.** `aggregator-r10-resume/` has no files. `aggregator-r10/` has only `seats/` (glob with `gitignore: false`). The candidate has one new unsettled warn (`w24`) and ten warn WAVE rows in total.
- **O7. /tmp.** `findmnt` gives `/tmp xfs /dev/nvme0n1p1`. `df -P /tmp` shows 71% used. The r10 baseline recorded `tmpfs:not-a-block-device`. The date of the change is not observed.
- **O8. Retired counters.** No candidate line contains `kill_signal=`, `segfault=` or `unit_failure=`. Removing their masks changes nothing today.
- **O9. Newly masked r10-era field.** `boot=current` on the r10 KILL and SEGFAULT findings (`baseline-r10:37-38`) falls under the round-13 `boot=` rule. Those lines no longer exist, so no current token results.
- **O10. Static counts.** The current census has 121 `check`, `check_cli` or `pd_check` call sites. The executed count is not observed.
- **O11. Threshold tokens.** Candidate values: `stale_threshold_s=900`, `warn_pct=85`, `crit_pct=95`, `psi_warn_avg10=10`, `window_s=7200`, `gate_s=7200`. Source defaults: `:351`, `:358-359`, `:367`, `:360`. All equal.
- **O12. Cross-check.** `.ufo/waves/round-20/build/C1Critic.md:9-12` reaches the same per-wave identity conclusion. Not relied on here.

## 7. Gate additions for the L1 (procedure only; no edits)

1. **Classify the capture you pin.** Commit the candidate file that was classified; do not capture again before pinning. The contract's counting command runs on an earlier capture, so its zero says nothing about the content that gets pinned.
2. **Classify rows, not tokens.** Use appendix A's object-level rows (id, object key, field, old value, new value).
3. **Name every standing warn or crit line,** with its own check and an acceptance reason. Refuse the pin while any is unaccepted.
4. **Verify pointers mechanically.** `git cat-file -e <commit>` and `test -e <path>` must succeed. For each schema token, `git log -S'<id or field>' --oneline -- tools/mori-census.sh` must include the claimed commit.
5. **Record the mask deltas.** Put the `volatile_fields` list delta (K7) and the sed-rule diff (one `boot=` rule) in the round record, with their commits.
6. **Record the pin's invocation.** `CENSUS_RC`, the `MORI_*` environment, and confirmation that the captured canonical block ends with the verdict line.
7. **Retain the raw capture** beside the baseline (`drift-pin-r10.md:250-252`).
8. **Report the post-pin `none` as "unchanged since pin,"** and restate the standing warns beside it.
9. **Expected outcome.** My recommended classes for two tokens, STALE (K2) and WAVE (K3), are `census-regression`, which blocks the re-pin this round. Report that as the result. Do not relabel the tokens to pass the gate.

## 8. Gaps, discrepancies, unobserved

- Not run: the census (`--drift`, `--pin`), the selftest, and any live capture. The LSP device the role describes is not in this seat's device list, so I used read, grep and the offline port.
- The entering stdout is a single JSON line; I used its 50-token array. Entering row values are not visible to me. The 10:22:12Z candidate is the only full canonical block I could read.
- "Nine census revisions" in the contract versus seven commits (O2).
- The line numbers in `drift-pin-r10.md` refer to d7710981's 2833-line file. The current file is 4744 lines. Cite functions, not numbers.
- The date and cause of the /tmp mount change, and of the watchdog daemon's stop, are not observed. I state only the last tick and the process state.
- The r13 register (42 keys) has no evidence pointers and cannot be reused as evidence.
- The 121 selftest call sites are a static count, not the executed PASS count.

## 9. Tooling record

- No installs or updates. No pacman, uv, npm or cargo.
- Read-only commands run: `sha256sum`; `git log`, `git show`, `git merge-base --is-ancestor` and `git rev-parse` (from Python with `GIT_OPTIONAL_LOCKS=0`; no `status`, `add`, `checkout` or index writes); `stat`; `pgrep -af`; `findmnt`; `df -P`; glob and grep on the fleet repo; `read` on the watchdog log (last five lines, plus targeted ranges).
- Python 3 standard library only, for the offline port and the diffs. No census execution.

## Appendix A. Object-level diff, r10 baseline to the 10:22:12Z candidate (same census SHA)

```
exact after masking, 18 rows: SURFACE watchdog, waves, cgroup, tmux, lane.protocol, lane.kasegi, lane.kotoba;
  FINDING WATCHDOG_ABSENT; 9 x FINDING WAVE_UNSETTLED_AGE; VERDICT (DRIFT)
paired, base row -> candidate row:
  HEADER              census-r5 -> census-r6 (line text only; no field changed)
  SURFACE:disk        io_avg_unavailable 'tmpfs:not-a-block-device' -> 'none'
                      [io_avg_since_boot gains a nvme0n1p1 tail: not compared, K5]
  SURFACE:lane.aggregator   basis row-B -> row-A; -rowb_files; -attribution; -example;
                      +subject_commits=yes; +window=launch..NOW
  SURFACE:lane.kagi   round '<V>' -> '<V><V>'; basis row-A -> row-6; -subject_commits; -window;
                      +reason=committed-report; +path=.ufo/reports/round-24/kagi.md
  SURFACE:lane.kake   round dup; basis row-A -> row-6; -subject_commits; -window;
                      +reason=committed-report; +path=.ufo/reports/round-23/kake.md
  SURFACE:lane.kengaku  round dup; basis row-A -> row-6; -subject_commits; -window;
                      +reason=committed-report; +path=.ufo/reports/round-26/kengaku.md
  SURFACE:lane.kumitate round dup; age_s '<V>' -> '-'; basis row-A -> row-4; -subject_commits; -window;
                      +reason=ledger-close
  SURFACE:lane.kama   basis row-A -> row-8; -subject_commits; -window; +reason=age_le_gate; +gate_s=7200
  SURFACE:silence     +roster_source=conf+state; +roster_n=23; +conf_n=23; +state_n=21;
                      +conf_dropped_n=0; +state_dropped_n=0
  FINDING:WAVE_UNSETTLED_AGE  base 'wave=aggregator-r10' <-> new 'wave=shokunin-train-20261016-w24':
                      obs changed; the new warn is not reported as an addition (K4)
removed, base only (5): SURFACE:journal; FINDING:WATCHDOG_STALE;
  FINDING:WAVE_UNSETTLED_AGE (wave=aggregator-r10-resume); FINDING:KILL_SIGNAL_JOURNAL; FINDING:SEGFAULT_JOURNAL
added, candidate only (34): SURFACE:journal.user; SURFACE:journal.system;
  SURFACE:lane.{audio, chousa, game-dev-2d, game-dev-3d, kaidoku, kotodama, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi};
  FINDING:WATCHDOG_STATE_LAG x13 (chousa, kagi, kaidoku, kake, kama, kasegi, kengaku, kumitate, mado, mori, tabi, tameshi, tsukuroi);
  FINDING:ROSTER_SET_MISMATCH; FINDING:COREDUMP_NOTICE_JOURNAL_USER; FINDING:SEGFAULT_SIGNAL11_JOURNAL_USER;
  FINDING:UNIT_FAILURE_OUT_OF_SCOPE; FINDING:JOURNAL_CLASSES_UNMEASURED
```
