# NoHarmReview — round 14 C1 repair vs six axes and the no-harm rule

Seat: `MoriR14.NoHarmReview` (critic, leaf). Report only: these are challenges, not verdict certification. No production, test, or gate files were edited, and no gate/selftest/census run happened. Tools installed: none.

Inputs read: `corpus/lessons/round-13-verifier-spotcheck.md` (all of it); the CensusRepair assignment in `.ufo/waves/round-14/spec.json`; the working-tree L1 plan text (`LOG.md` r14 entry, `PROVINCE.md:24`, `SCORECARD.md:733–758`, `corpus/lessons/round-14.md`, `corpus/QUALITY.md` Q29–Q32). Frozen B census: `.ufo/waves/round-13/frozen/mori-census.sh` (sha `3da5b098…`, B=`6531ac6`, the last admitted state). Entering H census: `tools/mori-census.sh` (sha `39abda0a…`, unchanged at the time of review; no repair bytes had landed yet). Pinned systemd sources at `cf8ebfc6`. Read-only `journalctl` structured-field queries ran without MESSAGE output.

## Axes named

coverage (claimed) · operability · depth · freshness · calibration · adjacency. No-harm rule: an improvement on one axis does not admit harm on another (spotcheck:7). Q29 sets the bar for replacing an alarm: same positive fixture → same stable id, severity no lower than before, same roll effect, same owner route.

## Evidence base (new, measured by this seat)

1. **B's OOM alarm never matched an OOM *notice*.** B `probe_journal` :874 counts `Out of memory|oom-kill|oom_reaper|Killed process` (case-insensitive) over `journalctl --user -b`. The pinned notice text is `cgroup.c:3100` "The kernel OOM killer killed some processes in this unit." (fe6faa94). The older catalog wording, the oomd text (`cgroup.c:3043–3047`) and the unit-result text (`unit.c:6339` "Failed with result '%s'.") were checked too:
   `printf '%s\n' "The kernel OOM killer killed some processes in this unit." "A process of this unit has been killed by the OOM killer." "systemd-oomd killed some process(es) in this unit." "Failed with result 'oom-kill'." | grep -ciE 'Out of memory|oom-kill|oom_reaper|Killed process'` → `1`.
   Only the unit-result line matches. In practice B's user-journal OOM alarm fired on **`UNIT_RESULT=oom-kill`** (d9b373ed, `unit.c:6333–6342`), plus any free text. It did not fire on kernel-OOM notices. Kernel `Killed process` lines go to the system journal, which B never read. Host `systemd 261 (261.2-1-arch)`.
2. **B's KILL_SIGNAL_JOURNAL warn had a second trigger.** B :875 regex `status=9/KILL|Failed with result .signal|SIGKILL` → "Failed with result 'signal'" means **`UNIT_RESULT=signal`** raised warn/DRIFT in B. H keeps warn only for 98e32220 `EXIT_CODE=killed EXIT_STATUS=9`. The r14 plan restores OOM and unit routing only.
3. **Real positive records exist in a retained boot.** `7bd93aee71144017b870212161a3dabf`, the 2026-10-18 M19 boot. Commands: `journalctl <scope> -b <boot> -o json --output-fields=_BOOT_ID,MESSAGE_ID,UNIT,USER_UNIT[,UNIT_RESULT] MESSAGE_ID=<id> | jq` (counts/grouping only):
   - user fe6faa94: 7 = `-.slice` 1, `app.slice` 2, `arc2-r10-mid.service` 1, `arc2-r8-ctl.service` 1, two `run-p…-i….scope` 1 each.
   - system fe6faa94: 9 = **`user@N.service` 4**, `user-N.slice` 1, `user.slice` 1, `system.slice` 1, `systemd-coredump@….service` 1, coredump slice 1.
   - d9b373ed `UNIT_RESULT`: user `exit-code` 4591, `oom-kill` 4, `core-dump` 1, `start-limit-hit` 1. System: `oom-kill` 1.
   - Subject field present on every record: user=`USER_UNIT` and system=`UNIT`. 0 missing, 0 both.
   - Across all 11 retained boots, `UNIT_RESULT=signal` = 0 and `oom-kill` exists only in 7bd93aee (4 user / 1 system). The current boot `430d3038…` has 0 d9b373ed records in both scopes.
4. **The B fleet predicate matches none of these units, including fleet-lane workloads.** `shokunin|ufo-sighting|tmux-spawn|the-tick|fleet` applied to `USER_UNIT`/`UNIT` → user `nonfleet` 4597/4597 (incl. all 4 oom-kill) and system `nonfleet` 1/1. `systemctl --user list-units --all` matching the tokens → 0. Fleet sessions run in `app-Hyprland-xdg-terminal-exec-*.scope`, per `/proc/self/cgroup`. The oom-killed `arc2-r*-*.service` and `run-*.scope` units are kaidoku lane workloads. `kaidoku-shokunin/corpus/lessons/2026-10-18-caller-independent-services.md:8–17` says they were launched with `systemd-run --user --scope`, then as transient services, and were OOM-killed at their own MemoryMax caps.
5. **H's alarm loop is per class, so OR semantics survive partial unavailability.** `tools/mori-census.sh:1088–1107` skips only non-ok classes. `emit_finding` warn/crit flips ROLL at :392–405. B also set the surface state to `st=drift` (:895,:899). H journal surfaces are only `ok|unavailable` (:1110–1128).

## Challenges (counterexample → evidence → axes → smallest safe correction)

### NH1 — "retain"/"restore" hides an alarm *extension*: silent scope and severity drift (calibration, adjacency, depth)
- **Counterexample.** A system service OOM with no user-scope record, e.g. `UNIT=packagekit.service` fe6faa94 only. B: never read the system journal → CLEAN. H: `KERNEL_OOM_NOTICE_JOURNAL_SYSTEM` info → CLEAN. Plan ("either journal scope … crit"): **DRIFT that latches for the whole boot.** The same applies to a user-scope notice-only kill (e.g. a delegated or `OOMPolicy=continue` unit, which produces no `oom-kill` result: `service.c:4712`, `scope.c:583`). B stayed CLEAN there; the plan goes DRIFT.
- **Evidence.** Evidence 1: B's real trigger set was user `UNIT_RESULT=oom-kill` plus free text. `PROVINCE.md:24` (working tree) says notices and `UNIT_RESULT=oom-kill` "retain critical OOM_KILL_JOURNAL/DRIFT alarms". That is true only for user-scope `oom-kill`. Notices in either scope and system-scope `oom-kill` are new DRIFT triggers. The lane's own history rejected an analogous move: `tools/mori-census.sh:1146–1150` says parent-scope OOM crit "forced a permanent false DRIFT and absorbed tsukuroi's OS triage into mori".
- **Axes.** Not a Q29 violation, because severity is not lower. But it is false provenance (depth/calibration) and a candidate adjacency/calibration harm, because system-wide OS OOMs become mori DRIFT.
- **Smallest correction.** Split the claim wording and evidence into *restored* (user `UNIT_RESULT=oom-kill` → crit, B parity) and *extended* (kernel-OOM notices in both scopes, system-scope `oom-kill`). The extension needs a declared rationale plus its own positive/negative fixtures, and L1/judge must weigh it explicitly. Do **not** fix NH1 by partitioning the OOM alarm with the fleet token predicate (see NH3). If the extension is kept, every system-scope crit should carry `scope=system` and an explicit adjacency note. Otherwise, restrict system-scope crit to the fleet user's envelope `UNIT=user@<uid>.service` (evidence 3: 4/9 system notices) and leave other system units at the r13 info severity with `owner=tsukuroi`.

### NH2 — B's `UNIT_RESULT=signal` warn/DRIFT is still lost after the planned repair (coverage, Q29)
- **Counterexample.** A user unit whose main process dies on SIGTERM/SIGABRT/SIGHUP, so d9b373ed `UNIT_RESULT=signal` with no 98e32220 `EXIT_STATUS=9`. B: "Failed with result 'signal'" → `KILL_SIGNAL_JOURNAL` warn → DRIFT. H and the plan: `unit_failure_record` info at most → CLEAN.
- **Evidence.** Evidence 2; B :875,:897–900; H :1095 only `user:unit_sigkill_record` warns. The verifier's routed defects #1–#3 do not name this trigger. It is exactly the Q29 class ("every alarm it replaces"). Live frequency is 0 across 11 boots, so this is a contract loss, not an observed miss.
- **Axes.** coverage (the claimed axis) is not harm-free under Q29; calibration if it is described as resolved.
- **Smallest correction.** Read `UNIT_RESULT` once from the existing d9b373ed query. Raise user-scope `UNIT_RESULT=signal` to `KILL_SIGNAL_JOURNAL` warn, B parity, with system scope following the same restore/extend split as NH1. Alternatively, declare the trade in the claim and the unmeasured list as an *unimplemented structured class* (fixing defect #3's wording at the same time). The trade must not stay silent.

### NH3 — The mirrored fleet predicate is B-parity but empirically misroutes fleet-lane units to tsukuroi (adjacency, calibration)
- **Counterexample.** The only real failed-unit OOM records retained (4 user `oom-kill`, kaidoku `systemd-run` workloads) classify nonfleet → `UNIT_FAILURE_OUT_OF_SCOPE owner=tsukuroi`. Applying the same predicate to system-scope OOM notices or failures would also class `UNIT=user@N.service`, the envelope containing the whole fleet, as nonfleet.
- **Evidence.** Evidence 3–4. B behaved identically (its substring grep over the default short line adds only hostname `plazir27`, identifier `systemd` and fixed text, none of which matches a token), so this is **parity, not new harm**.
- **Axes.** Restoring the route is a semantic restoration, not new fleet coverage: on this host `UNIT_FAILURE_JOURNAL` (fleet) is structurally ~always 0. Claiming "fleet unit failures now detected" would be count inflation.
- **Smallest correction.** Mirror B exactly (case-insensitive token match on the subject `UNIT`/`USER_UNIT` value only) and label it on the finding/surface, e.g. `predicate=b-token-v1`. Disclose the observed misroute (`systemd-run` scopes and transient services launched by lanes) as a calibration limit. Do not silently "improve" the predicate this round; that would be an undeclared semantic change. Never use the predicate to demote an OOM alarm.

### NH4 — Validating new subject/result fields "all-or-unavailable" would regress the r13 counters (coverage harm)
- **Counterexample.** One d9b373ed record without `USER_UNIT` (or `UNIT_RESULT`) in the user journal. H: `unit_failure_record=1` ok. A repair that adds these fields to the `all(...)` validator (the H pattern `JOURNAL_JQ_*` :926–929) grades the whole class `unavailable:record-invalid`. That loses the count and both alarms derived from it, and the r13 scoped gain silently regresses. It is also a cheap denial-of-alarm vector for client-supplied records (S015 user fields).
- **Evidence.** H `journal_query` :985–1011. Missing subject fields were 0 of 4602 in boot 7bd93aee, so honest data seldom hits this, but forged or odd records can.
- **Smallest correction.** Keep only `_BOOT_ID`/`MESSAGE_ID` (and existing class-defining fields) as class-gating. Classify subject and result **per record**, with the invariant `fleet + nonfleet + unknown == unit_failure_record` per scope, and `UNIT_RESULT` missing → result unknown (never `oom-kill`, never 0). Gate fixture: one valid record plus one subject-less record → count 2, `unknown=1`, class still `ok`.

### NH5 — Count gain vs alarm semantic gain must not be double-credited (coverage scoring, calibration)
Relative to the last admitted state **B**:
| Element | Status vs B | Credit kind |
|---|---|---|
| 6 classes × 2 scopes scoped record counters | new (r13), must stay 12/12 identical in name, value and unavailability semantics | count gain (already earned; r13 point withdrawn per SCORECARD:739) |
| user `UNIT_RESULT=oom-kill` → crit/DRIFT | parity restored | harm removal, no gain |
| user `UNIT_RESULT=signal` → warn | **still lost** (NH2) | outstanding harm unless declared |
| user fleet/nonfleet + tsukuroi route | parity restored (structurally ~all nonfleet on host) | harm removal, no gain |
| notices → crit (both scopes), system `oom-kill` → crit, system routing | **new semantics** | needs separate evidence and harm check (NH1) |
| `unknown` subject bucket | new honesty (0 observed) | calibration detail, not coverage |
The current-boot live run has 0 records in every class (evidence 3), so a live 12/12 comparison again cannot exercise any alarm or route. Positive evidence will be fixture-only unless a real-shape fixture is drawn from the retained 7bd93aee structured fields (no MESSAGE). Any rubric must count restoration as zero and keep the extension separate. SCORECARD:753 already says this; the PROVINCE/knowledge wording must match.

### NH6 — Stable-identity drift for `OOM_KILL_JOURNAL` / `UNIT_FAILURE_OUT_OF_SCOPE` (calibration, freshness)
- B emitted `OOM_KILL_JOURNAL crit "class=oom_kill count=<text lines> boot=current scope=user"` and `UNIT_FAILURE_OUT_OF_SCOPE` for user scope only.
- **Risks:**
  - (a) A single summed `count=` over notices + `oom-kill` results, or over scopes. One kill produced 7 user + 9 system notices plus 4 + 1 results in evidence 3, so that is a false kill count (Q16, M19).
  - (b) The same id reused for system scope without a `scope=` token. Consumers previously read B's ids as user-only, so this repeats routed defect #2's "different counted universe" defect.
  - (c) The surface stays `ok` while crit fires; B surfaced `journal: drift`.
- **Smallest correction.** Emit one finding per scope with per-source fields (`kernel_oom_notice=N unit_result_oom_kill=M`, `unit=record`, `trust=client-supplied`, `attribution=none`) and no summed total. Keep `scope=` on every reused id. Either set the scope surface state to `drift` on warn/crit (B parity) or name the deviation. Freshness: these intentionally change canonical output, so the red r10 baseline gets more red tokens. Classify them; no silent re-pin.

### NH7 — Migration must keep the negative witnesses and historical receipts (operability)
- Keep H selftest `journal: legacy text ids are not counted (Q15)` (:2776–2790). With `OOM_KILL_JOURNAL` emitted again, it becomes the guard that text never triggers the restored id. Do not delete it as "obsolete id".
- Update `journal-matrix` (:2747–2771) by *adding* the B-parity pair: a d9b373ed record with `UNIT_RESULT=oom-kill` → crit, and with `UNIT_RESULT=signal` → warn (NH2). Do not just flip the notice-only expectation.
- The r13 receipts (`regressions-*/evidence.json` at `c13df48`) stay as-is. HarnessMigration changes to `tools/mori-round13-regressions.py` must cite the new revision and not be described as re-validating r13.
- Budget: reuse the existing d9b373ed query (adding `UNIT,USER_UNIT,UNIT_RESULT` to `--output-fields`) rather than a new query class. That adds 0 journal scans versus +2 bounded scans (≤3 s each with `-k 1`, :961). r12 already disputes "unchanged" operability without a budget.

### NH8 — Depth/provenance wording to correct before closure
- `PROVINCE.md:24`: "retain" → "restore (user `UNIT_RESULT=oom-kill`) and extend (kernel-OOM unit notices; system scope)".
- `lessons/round-14.md` M1 fix says "same positive structured-notice fixture … before and after". B never alarmed on a notice. The true Q29 equivalence witness is the `UNIT_RESULT=oom-kill` fixture versus B's "Failed with result 'oom-kill'" text. The notice fixture proves only the extension (and red-at-H).
- Host-source skew: user-scope notices for `-.slice`/`app.slice` were observed on 261.2 even though pinned `cgroup.c:2075–2078` skips `UNIT_SLICE`. Knowledge must not present pinned-source behavior as host behavior.
- No-harm statements must name B (last admitted) and H (entering) separately. H→r14 being "no lower" does not imply B→r14 equivalence (NH2).

## Per-axis challenge summary (not a verdict)

| Axis | Risk if the plan lands as written | Blocking for no-harm? |
|---|---|---|
| coverage | NH2 B signal-warn loss; NH4 counter regression if validation is all-or-nothing | NH2 yes unless declared; NH4 yes if implemented that way |
| operability | NH7 negative-witness deletion, extra scans | fixable |
| depth | NH1/NH8 "retain" false provenance | fixable wording |
| freshness | NH6 more red tokens; no re-pin | no, if classified |
| calibration | NH1 system/notice DRIFT latch; NH3 predicate misroute; NH6 summed counts | judge must weigh NH1; NH6 yes if summed |
| adjacency | NH1 system-wide OOM absorbs tsukuroi triage (contradicts :1146–1150); NH3 lane units routed to tsukuroi (B parity) | NH1 is a tradeoff the judge must rule on; NH3 disclosure only |

Checks for L1 after integration (not run here):
- census `--selftest`
- the r14 gate with the B-parity `oom-kill`/`signal` fixtures over entering H bytes (expect red) and repaired bytes (expect green)
- the `jq` scan from spotcheck:77, extended with `emit_finding KILL_SIGNAL_JOURNAL` and per-scope `OOM_KILL_JOURNAL` emissions
- a 12-counter parity diff of the `SURFACE journal.*` class tokens between H and repaired output on the same fixture
