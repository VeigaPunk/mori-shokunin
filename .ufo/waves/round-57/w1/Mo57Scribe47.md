# Mo57Scribe47 — coverage cross-check (FR5 + driver-liveness probe)

Lane: mori-shokunin, round 57. Seat scope: *inspect FR5 and the driver-liveness probe for one
new observability surface genuinely outside current core; report only.*
Entering tip `53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`; freeze `618562c72a03dc4d17386b715357f863fd327274`.
No file outside this report was written; no commit/jj/pacman/tool install; no remediation.

## Verdict

1. **The round-56 claim is real at the entry level.** `tools/mori-driver-liveness.py` is a strict
   per-event reader that Core did not have before, and FR5's named open ground (`corpus/README.md:345`)
   is where it lands. No counterexample found against the *pairing* fields themselves.
2. **One observability surface genuinely outside Core exists, and it is on the active driver path:
   `.ufo/state/<lane>.report-baseline` (`"<dispatch-round> <sha256>"`).** It is written at every
   inline dispatch, tracks the log's last launch round for 17/17 lanes, and **no observer in
   `mori-shokunin/tools/` reads it** (0 grep hits). It is a log-independent per-lane dispatch epoch.
   Details and counterexamples below.
3. **The phrase "full writer-grammar coverage" (`corpus/README.md:345`, `knowledge/driver-liveness-r56.md`)
   over-reads the source.** The probe models 5 event families; the daemon writer emits 20+ (`hoisted
   below`). Zero of the unmodelled ones exist in today's live log, so today's `malformed=0` does not
   evidence writer coverage — it evidences that the daemon path is not writing.

## What FR5 core actually reads (ground check)

| Reader | Surface read | Not read |
|---|---|---|
| `tools/mori-census.sh` (watchdog arm) | pid probe; `stat` of the log; `*.round` **values**, each compared to the ledger's last `launch <lane> round=N` (`:744-760`, `:818-821`) | `*.report-baseline`; every writer event except launch/close verbs |
| `tools/mori-driver-liveness.py` | per-lane launch/complete/dead/launch-fail/wrap pairing; `*.round` entry **shapes** only (`:179-199`, filter `name.endswith(".round")` at `:185`) | `*.report-baseline`; state values; log identity |
| FR5 boundary text | `PROVINCE.md:48`, `corpus/README.md:345` | — |

Measured live (2026-10-27, read-only):
`python3 tools/mori-driver-liveness.py` → `DRIVER_LIVENESS_OK`, `lines=1742`, `malformed=0`,
`other_lines=121`, `lanes=23`, `state_dir={regular:21, symlink:0, dir:0, other:0}`;
mori: `launches=67 completes=40 deads=17 launch_fails=0 wraps=0 in_flight=true unclosed=10`.
Re-run reproduced the round-56 receipt modulo ages (`last_launch_age_s` 2899.6).

`other_lines` decomposed with the probe's own `LINE_RE` (same regexes imported, not re-written):
`lane-round-failed` 35, `steer` 15, `tick=N` 70, `watchdog …` 1 = 121.

## The new surface: per-lane dispatch-epoch / report-identity baseline

Provenance (writer authority, same source family as S544):

- `scripts/shokunin-watchdog.sh:163-181` — `record_report_baseline` writes `<round> <sha256>\n`
  atomically (`tmp` + `mv -fT`) to `$UFO/state/<lane>.report-baseline`; digest is `sha256` of the
  report bytes, and `report_digest` (`:151-161`) hashes the **empty stream** when the report does not
  exist.
- `scripts/hyaku/inline.sh:29` sources the daemon script, so the **active** inline driver uses the
  same function; it is called at `inline.sh:146`, i.e. immediately **before** the launch line at
  `inline.sh:149`.
- The file is *not* a log line: it is a file write, so it survives log truncation/rotation and is
  unaffected by writer-grammar drift.

No reader (the actual coverage gap):

- `grep -rn "report-baseline" --include=*.py --include=*.sh mori-shokunin/` → **0 hits**.
- Census `state_rounds` globs `*.round` only (`mori-census.sh:780-786`); probe filters
  `name.endswith(".round")` (`mori-driver-liveness.py:185`). A `*.report-baseline` entry is therefore
  invisible to both readers: not counted, not named, not disclosed.

Measured on the live fleet (read-only; baseline round vs. census-visible `.round` vs. the log's last
launch round for that lane):

```
lane             bl_round  round_file  last_launch  digest
chousa                 58           1           58  empty
kagi                   28          16           28  empty
kaidoku                43           1           43  empty
kake                   63          16           63  empty
kama                   56           1           56  empty
kasegi                 41          17           41  empty
kengaku                48          13           48  empty
kotoba                 75          16           75  empty
kotodama               74           -           74  empty
kumitate               68          18           68  empty
mado                   53           1           53  empty
mori                   57           2           57  empty
revenger               71           1           71  empty
souji                  34           -           34  empty
tabi                   38           1           38  empty
tameshi                53           1           53  empty
tsukuroi               47           1           47  empty
baseline files: 17 | .round files: 21 | lanes in log: 23
```

Every baseline round equals that lane's last launch round (17/17). Every digest is the empty-stream
digest `e3b0c442…`, which is the expected value: the baseline is captured at dispatch, before the lane
writes anything.

### Counterexamples against current core

**C-a — log unavailable ⇒ the probe reports no per-lane epoch at all.**
`run()` returns early on absent/unreadable/empty log (`tools/mori-driver-liveness.py:205-217`), *before*
`report["state_dir"] = state_shapes(state_dir)` at `:236`. Reproduction (log copies under scratch only):

```
$ python3 tools/mori-driver-liveness.py --log $SCRATCH/empty.log
rc=2  verdict=DRIVER_LIVENESS_UNAVAILABLE  lanes=0  state_dir=None
```
At that moment 17 baseline files still carried a round and a dispatch mtime
(`mori` baseline `57`, age 3024 s; `souji` `34`, age 25366 s; `kotodama` `74`, age 143906 s).
So "log unavailable" currently means "no liveness evidence", although a non-log epoch source is on disk.

**C-b — two lanes have a baseline but no census-visible state row.**
`souji` and `kotodama` have no `*.round` file (census walk has no row for them) but hold baselines
`34` and `74`. The dispatch epoch exists; core cannot see it.

**C-c — core's only state-value read is stale under the active driver.**
`.round` is written **only** by the daemon (`shokunin-watchdog.sh:265`); `inline.sh` never writes it
(no `.round` write in `scripts/hyaku/inline.sh`). Live `.round` values are 1–18 while baseline/ledger
rounds are 28–75. [INFERENCE — not measured, census not run]: census `WATCHDOG_STATE_LAG` rows under
the inline driver are structural, not lane misbehaviour. The baseline round is the value that agrees
with the ledger.

## Secondary finding: grammar boundedness (affects the r56 wording, not the counters)

`tools/mori-driver-liveness.py:63-70` models exactly `launch|complete|lane-dead-no-report|launch-fail|wrap`.
The daemon writer emits at least these further event lines (`log "…"` in `scripts/shokunin-watchdog.sh`):
`disk-guard-warn:81`, `disk-sweep:91`, `disk-defer:104`, `state-corrupt:139`,
`report-baseline-fail:167,173,178`, `cap:238,420`, `kill-fail:318,325`, `kill-escalate:322`,
`kill-timeout:329`, `sources-conformance-defect:355,359`, `sources-gate-skip:370`,
`sources-gate-warn:374,382`, `sources-gate-fail:380`, `advance-blocked:395,402,408,410,417`,
`lane-report-not-accepted:445`, `tick=:452`.
All of them are ts-first and non-matching, so they land in `other_lines` — counted, never an event,
never malformed. Live count of that family: **0** (`grep -cE '^\S+ (advance-blocked|lane-report-not-accepted|state-corrupt|cap|sources-gate|kill-|disk-)' .ufo/watchdog.log` → 0).

Reproduced pairing artifact under the daemon shape (scratch fixture, explicit `--log`):

```
2026-10-20T10:00:00-03:00 launch mori round=5 pgid=1111
2026-10-20T10:20:00-03:00 lane-report-not-accepted mori round=5 :: …; NOT advancing
2026-10-20T10:20:01-03:00 launch mori round=5 pgid=2222
2026-10-20T10:40:00-03:00 complete mori round=5; advancing to round=6
→ lanes.mori = {launches:2, completes:1, unclosed:1, in_flight:false}, other_lines=1
```

Cause: `open_launches` is a list appended per launch (`:136`), while `close_round()` removes one
matching key (`:109-113`, `:143`); `launch_lane` after `lane-report-not-accepted`
(`shokunin-watchdog.sh:445-446`) re-launches the same round. The round **closed**, yet `unclosed=1`.
This is a second, source-grounded reason `unclosed` is a pairing count and not a present-running count
(complements the inline-driver reason already documented).

## Limits of the proposed surface (named before any use)

- Last-write-wins: the file is overwritten at each dispatch and keeps no history; a reader gets one
  epoch per lane, not a series.
- Driver-authored, same trust level as the log: a rewritten state file rewrites the reading.
- Written *before* the launch line, so a crash between `inline.sh:146` and `:149` leaves a baseline
  round with no spawn. Round alone is therefore not proof that a process started.
- The digest describes report bytes at dispatch; under the live driver it is normally the empty-stream
  digest. It supports "same-round unchanged bytes" reasoning, not freshness or quality.
- The reading must stay shape/epoch only (no values beyond the round integer and digest comparison);
  `.round` value semantics belong to the census.

## Out of scope / not done

No census run, no counter run, no code change, no fixture committed, no remediation of host state.
`lane-round-failed` (35 lines, kimi-port driver) was **not** claimed as the new surface: it is
already named as a probe gap in `knowledge/driver-liveness-r56.md` and is deliberately ignored by
silence grading (`corpus/knowledge/silence-cutover-r3.md:36`, `tools/mori-census.sh:1999`).

## Artifacts

Scratch `/fast/scratch/hyaku/mori-r57/Mo57Scribe47/` was used for every fixture and was removed after
measurement (nothing outside this report persists). Every number above is reproducible from the
commands shown inline; the pairing counterexample is the four-line log quoted in place, fed with
`--log` and `--state-dir` pointing at scratch paths.
