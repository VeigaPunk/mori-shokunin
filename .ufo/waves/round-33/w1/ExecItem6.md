# mori round 33 wave 1 — ExecItem6: routed defect 6 (round-30 detector FP/FN + FR5 census probe)

Seat `MoriR33.ExecItem6`, leaf. Detection and report only: **no lane file changed** (no edit, no git/jj write in the
lane or the fleet repo; read-only git only). All experiments ran in `/fast/scratch/hyaku/mori-r33/ExecItem6/`
(sandbox `git init` repo, tool copy, census output). Tools used: bash 5.3.20, git, python3 — nothing installed.

Tool digests measured this wave: `tools/mori-census.sh` = `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28`,
`tools/mori-blind-check.sh` = `79b774f7736cc9074fa786ad360553987d92096a3864b07212f7a3127924beb8` (the census prints the first as
`script_sha256=` on every finding line below).

## 1. Census run (read-only) — requested receipt

- Attempt 1: `timeout 120 bash tools/mori-census.sh 2>&1 | grep -Ei 'watchdog|MORI_CENSUS'` → **rc 124, no output**:
  the script buffers every line and prints at the end (`tools/mori-census.sh:2711-2715`), so a bound hit before the end
  yields nothing — the same rc=124/no-output observation as round-31 `ScoutCensusWatchdog.md` §7.
- Attempt 2 (long-scan bound, lane limit ≤600 s): `timeout 480 bash tools/mori-census.sh > /fast/scratch/hyaku/mori-r33/ExecItem6/census.txt 2>&1`
  → **completed, wall 104.45 s, rc=1**, 16948 B. Full file at that path. Watchdog-related lines and the roll:

```
SURFACE watchdog: drift (cmd=pgrep -af shokunin-watchdog; stat /home/vgpnk/Projects/shokunin/.ufo/watchdog.log; ls /home/vgpnk/Projects/shokunin/.ufo/state; pids=0; log=ok; age_s=176; stale_threshold_s=900; state_rounds=21 state_rounds_max=18 state_lag=15 state_ahead=0 state_cmp=21 state_val_unreadable=0 state_val_unread_reasons=file:0 symlink:0 dir:0 other:0; ts=2026-10-23T02:42:41Z)
FINDING WATCHDOG_ABSENT severity=warn obs=no shokunin-watchdog process matched by pgrep -af ts=2026-10-23T02:42:41Z script_sha256=87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28
MORI_CENSUS: DRIFT (findings=30 drift=11 unavailable=1 surfaces=8)
```

All 15 `WATCHDOG_STATE_LAG` lines are `severity=info` and share the suffix ` ts=2026-10-23T02:42:41Z script_sha256=87b8d680…b977ab28`
(verbatim, prefix shown; full lines in the scratch copy): `lane=chousa state_round=1 ledger_round=30`, `kagi 16/28`,
`kaidoku 1/30`, `kake 16/36`, `kama 1/25`, `kasegi 17/23`, `kengaku 13/29`, `kotoba 16/56`, `kumitate 18/44`,
`mado 1/23`, `mori 2/33`, `revenger 1/62`, `tabi 1/22`, `tameshi 1/29`, `tsukuroi 1/32` — each with
`path=/home/vgpnk/Projects/shokunin/.ufo/state/<lane>.round`.

Corroborating host facts (same session): `.ufo/.watchdog.lock` absent, no `shokunin-watchdog` argv visible
(`pgrep -af` → no output), the inline driver's state is fresh (`~/.local/state/shokunin-hyaku/last/chousa`
mtime `2026-10-22T23:39:43Z`; `events.log` mtime `23:39:45Z`, tail `inline launch lane=chousa round=30 attempt=1`),
and 14 claim dirs / 17 `last` files exist. `state_lag=15` reproduces round-31's replay of 15/21 exactly.

## 2. Recorded concrete FP/FN cases of the two round-30 detectors

The **only** place with concrete cases is `.ufo/waves/round-31/w1/ReviewGateR30Lines.md` (committed; fixtures B1–B12 in a
sandbox repo, run against the round-30 gate bytes; clause 6 carries the detectors unchanged). Per-brief judgment table
`:104-115`; findings `:32-96`:

| case | shape | gate output | judgment | record |
|---|---|---|---|---|
| B1 | rule quote: `## Tool output …` heading, then `KILLERS_QUIET` in prose, then "must exit 0." | `B1.md:8:writer-tool-run-output` | real FP (F1) | `ReviewGateR30Lines.md:39-44`, table `:104` |
| B2 | `--inputs` prose, then "may exit 0" 4 lines later | `B2.md:8:writer-tool-run-output` | real FP (F1) | `:45-48`, `:105` |
| B3 | prose "tool lines of stderr" | `B3.md:4:writer-tool-source-citation` | real FP (F3) | `:65-66`, `:106` |
| B4 | prose "tool: 4 fixtures … no tool lines" | `B4.md:4:writer-tool-source-citation` | real FP (F3) | `:67-69`, `:107` |
| B5 | `mori-oom-killers.py, line 42` comma citation | no hit | real FN (F4) | `:75-79`, `:108` |
| B6 | `## Console` + `KILLERS_QUIET` + `exit 0`, no tool word | no hit | real FN (F5) | `:84-88`, `:109` |
| B7 | unclosed ` ```json ` fence in `## Cases`, transcript below | no hit | real FN (F2) | `:55-59`, `:110` |
| B8 | lowercase `killers_quiet … exit 0` on a tool-output line | no hit | real FN (F6) | `:95-99`, `:111` |
| B9, B11, B12 | protected-table citation / window expiry / protected-fence citation | hits as designed / no hit | intended, not defects | `:112,114,115` |

No other concrete case is recorded anywhere. Everywhere else the class is carried by name only: `corpus/lessons/round-31.md:111-112`
("have false positives and negatives (wave-1 ReviewGateR30Lines F1–F6)"), `:115` (census probe), `corpus/lessons/round-31-verifier-spotcheck.md:224-228`,
`corpus/lessons/round-32.md:147` ("carried unchanged —"), `.ufo/waves/round-33/contract.md:100` (third carry). Adjacent but **not**
these two detectors: the round-30 spotcheck D1 FP `CaseA210c.md|writer-missing-files-opened-list` (`round-30-verifier-spotcheck.md:176-178`)
is a files-opened detector; `corpus/lessons/round-31.md:140` maps fixture ids F15/F16 to the two detectors (no FP/FN case);
`.ufo/waves/round-31/w1/RealBriefsR30.md:112-114` records a real-corpus no-fire observation (`tool_run_re` matches only each
brief's last line, so the run-output detector cannot fire) — an FN-class observation, not a judged case.

## 3. `tools/mori-blind-check.sh --help` / self-test (timeout 120 each)

```
$ bash tools/mori-blind-check.sh --help            # rc=2 (stderr)
usage: mori-blind-check.sh <lane-rev> <wave-report-dir> <writer-name-regex> <allow-file> | --selftest
$ bash tools/mori-blind-check.sh --selftest        # rc=0
PASS
```
There is no `--help` branch: `--help` falls into `if (( $# != 4 )); then usage; exit 2; fi` (`tools/mori-blind-check.sh:364`)
and prints usage to stderr (the `--selftest` branch is `:359-363`). The selftest pins 13 expected records (`:224-248`), including the two round-30 detectors
(`CaseR31m.md:2:writer-tool-source-citation`, `:5:writer-tool-run-output`) — **none of the F1–F6 shapes is in the selftest**,
so the six defects are unpinned by the tool's own test.

## 4. First-hand reproduction on the committed tool (falsifier for "still live")

Sandbox repo `/fast/scratch/hyaku/mori-r33/ExecItem6/repo`, rev `3299ed43e34d1e0797251922f2aadf9a3cfe5053`, eight briefs
reproducing B1–B8 (each with a clean `## Files opened` list), run with the committed tool:
```
scanned=8
blind_violations=4
.ufo/waves/round-33/w1/B1.md:8:writer-tool-run-output
.ufo/waves/round-33/w1/B2.md:8:writer-tool-run-output
.ufo/waves/round-33/w1/B3.md:4:writer-tool-source-citation
.ufo/waves/round-33/w1/B4.md:4:writer-tool-source-citation
gate_rc=1
```
Exactly the round-31 F1/F3 hits; B5–B8 silent (F2/F4/F5/F6) — so all six are live in `tools/mori-blind-check.sh`, not only in
the round-30 gate. Mechanisms at the committed lines: `tool_header_re` `:91` fires at `:178-180` **outside** the protected
guard (F3); `cite_file_re` `:90` needs the filename immediately before `:N`/`lines N` (F4); `verdict_re` `:93` is matched
against raw `$line` at `:189` while `exit_re` `:94` is matched against `$lower_line` at `:190` (F6); the case-json latch
`:119-123` is cleared only by a fence line (F2); arming requires `tool_run_re` vocabulary `:96` (F1/F5).

Frozen-predicate audit (python over `.ufo/waves/round-31/c2-fixtures.json`, sha `1442c14e…`, re-running the four regexes):
only F15 (`See tools/mori-oom-killers.py:42 for the parser.`) and F16 (`Tool run output:` / `KILLERS_QUIET` / `exit 0`) touch
these detectors; no fixture contains any fence line, none matches `tool_header_re`, and only F16 line 6 matches a verdict
token (uppercase). **F16 and the FP B1 are structurally identical** (vocabulary heading + verdict + exit), so any narrowing
that removes B1 also removes F16's frozen expected hit.

## 5. Recommendations per sub-item (act / retire, with the minimal change and its test)

### 5a. Round-30 detectors

**Act — F2, F3, F4, F6.** I applied a five-line candidate to a scratch copy
(`/fast/scratch/hyaku/mori-r33/ExecItem6/fixtry/mori-blind-check.sh`, sha `6c58ba65647ed9c3da19117ed2f5f58b722f023d1bc9990fe9dbfb2de2ed337a`):
1. `tool_header_re` `:91` → `'(^|[^[:alnum:]_])tool[[:space:]]+lines?[[:space:]]*[:|]?[[:space:]]*[0-9]+([[:space:]]*[-–][[:space:]]*[0-9]+)?'`
   (drop the bare `tool: N` label form; a number is now required) — fixes F3.
2. `cite_file_re` `:90` → add `|mori-oom-killers[.]py[[:space:],(]+line[[:space:]]+[0-9]+…` — fixes F4.
3. `verdict_re` `:93` → lowercase alternatives, matched against `$lower_line` at `:189` — fixes F6.
4. latch `:119-123` → `if [[ $line =~ $h2_re || $line =~ $fence_re ]]; then in_case_json=0; else protected=1; fi`
   (an H2 ends the case-json block and is itself unprotected, so the heading can arm) — fixes F2.

Measured, same sandbox: selftest **PASS** (13 pinned hits unchanged); B1–B8 now →
`B1:8` and `B2:8` still fire (F1 untouched), `B5:4` fires, `B7:13` fires, `B8:4` fires, B3/B4/B6 silent. Frozen predicate:
`python3 .ufo/waves/round-31/count-c2.py 52435f2f` (control, tool blob `79b774f7…`) → `exact=16/16 C2=met rc=0`; with
`--tool-file <candidate>` → `exact=16/16 C2=met rc=0`, identical per-fixture counts (F15=1, F16=1). **The four fixes do not
flip the frozen C2 predicate.** Test to land with the change: add B3, B4, B5, B7, B8 as selftest fixtures with their expected
sets (B3/B4 no-hit, B5/B7/B8 hit) so the four cases are pinned rather than prose. Cost: clause 6 freezes the detectors
(`.ufo/waves/round-31/rule-text.md:22`, `contract.md:90`), so the L1 should name the change in the round-33 contract as an
amendment, and round-32's frozen gate baseline needs a re-pin (its `verify.sh` reports `mutated tool → exit 1`,
`corpus/lessons/round-32.md:142`).

**Act rule-side, not tool-side — F1.** A regex cannot separate B1 from frozen F16 (identical shape, §4); narrowing arming to
the artifact name (`mori-oom-killers.py`) kills F16. The cheap fix that keeps both is a writer obligation: quote the verdict
clause (`KILLERS_QUIET`, exit 0) only inside a protected derivation table, never in prose — then B1 is a true positive, not an
FP. Evidence that the shape is reachable by an honest writer: the round-30 rule text itself carries the pair
(`.ufo/waves/round-30/rule-text.md:49`). Test: keep B1/B2 as expected-hit fixtures and add one honest control that paraphrases
the clause without the tokens (expected: no hit). **Retire** is the alternative if the L1 prefers no new obligation: then F1
must be recorded as an accepted FP cost in the rule text, not left as an open defect.

**Retire explicitly — F5.** A verbatim transcript under a neutral heading (`## Console`, no tool vocabulary) is
indistinguishable from prose about the rule without keying on writer-controlled vocabulary, and any widening to catch it
re-creates F1 (and breaks F16); the residual is closed only by the §5a-F1 writer obligation, if adopted. Reason, not
oversight: `ReviewGateR30Lines.md:76-82` states the tradeoff; the frozen F16 pins vocabulary arming.

### 5b. FR5 census probe (`WATCHDOG_ABSENT` under the inline driver)

**Act** — the daemon's absence is by design under the current driver (fleet `/home/vgpnk/Projects/shokunin/AGENTS.md:13-14`
"Fleet driver … `scripts/shokunin-watchdog.sh`" / "In-session orchestrator (**current mode**): `scripts/hyaku/inline.sh`",
`:19` "Never run the watchdog and `inline.sh` together"), yet `pid_n=0` alone flips the surface to `drift`
(`tools/mori-census.sh:829-834`) — today that is 1 of the roll's 11 drift findings on a fleet whose rounds are live
(§1; `corpus/knowledge/watchdog-identity-r31.md` "Today on this host" grades this `absent (that query only)`).
Minimal change, in `probe_watchdog` (`:704-853`): when `pid_n=0`, read a second liveness source before grading — the ledger's
tail for a recent `driver=hyaku-inline` launch/complete line (`scripts/hyaku/inline.sh:103`) or the inline state freshness
(`$HYAKU_STATE` default `$HOME/.local/state/shokunin-hyaku`, `last/<lane>` stamps / `events.log`, `inline.sh:19,29,96`); fresh
evidence → info finding naming the driver and surface `ok`; neither source → `WATCHDOG_ABSENT warn` as today. Test: extend the
census selftest (stub pgrep already exists, `tools/mori-census.sh:3205`) with (i) no-match pgrep + a fixture log tail carrying a
fresh `driver=hyaku-inline` line → `^SURFACE watchdog: ok`, no `FINDING WATCHDOG_ABSENT`; (ii) control, no-match pgrep + no
inline line → `WATCHDOG_ABSENT` warn (already pinned at `:3488-3489`). Cost: the finding-id list is a stable compare contract
(`:255-257`), so a new id is a contract addition, and `--pin/--drift` baselines need a re-pin.
**Retire** alternative (if the L1 wants the census literal): one-line severity change `warn` → `info` at `:830` and drop pid
absence from `st=drift` at `:833-834`, with the reason that inline mode makes daemon absence expected — but that also blinds
the surface to a genuinely dead daemon, which is why I recommend act over retire.

## 6. Risks, blockers, not-run

- Both recommendations change frozen/pinned artifacts (round-31 clause 6 + round-32 baseline for the tool; census baseline and
  finding-id contract for the probe) — L1 decisions, not seat decisions. Measured mitigation for the tool: the frozen C2
  predicate still scores `exact=16/16 C2=met`.
- The census's 120 s bound is marginal on this host: rc 124 with no output at 120 s (attempt 1), complete at 104.45 s
  (attempt 2). Any future receipt should use ≥300 s or capture to a file.
- One shell call measured `pgrep -c -f shokunin-watchdog` → 1 while the census measured `pids=0` and a later `pgrep -af`
  printed nothing; the 1 is a wrapper/self argv match, not a daemon [INFERENCE] — the recorded proof of that FP class is
  `ScoutCensusWatchdog.md` §3.1 (decoy) and `corpus/knowledge/audit-r11.md:201` (D06).
- Not run: no lane file edited; the round-33 counter was not run (L1-only); no census/detector change landed; the round-32
  frozen `verify.sh` was not re-run with the candidate tool (its re-pin need is read from `corpus/lessons/round-32.md:142`).
- Privacy/containment kept: no uid, pid, slice name, session id or journal text written; scratch confined to
  `/fast/scratch/hyaku/mori-r33/ExecItem6/`; no process left running (all commands `timeout`-bounded and completed inline).
