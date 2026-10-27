# Mo57Simplifier64 — round-56 `unclosed` pairing list reopened: reproduced, and its interpretation bounded

Seat: Mo57Simplifier64 (simplifier, mori-shokunin lane, round 57 wave w1).
Assignment: C2 depth — reopen the committed round-56 driver-live report, verify its pairing list, and
decide whether `unclosed` counts mean *running work*. Detection and report only: no production edit,
no counter change, no commit/jj mutation, no host remediation.

Frozen inputs read:
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-57/contract.md` (C2 predicate).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/w1/Mo56ExecDriverLive.md` (the report under audit).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/evidence/driver-liveness-live.txt` (committed receipt).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/driver-liveness-r56.md` (round-56 entry).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-driver-liveness.py` (probe; sha256 `6b3dba74…be997`, equal to `count-c1.py:46 PIN`).
- `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` (live log, read-only), `scripts/hyaku/inline.sh` (writer).

Scratch: `/fast/scratch/hyaku/mori-r57/Mo57Simplifier64/` with `TMPDIR` under it; removed at exit.
Disk gate before work: `scripts/hyaku/disk-guard.sh status` → exit 0, `/fast/scratch/hyaku` 27% used,
591.9G free. No tool was installed or updated (stock `python3` 3.14 only), so no tool row is owed.

---

## 1. The pairing list: reproduced exactly

The log is append-only, so the round-56 run is reconstructible by cutting at the receipt's own
`log.newest_ts` (`1793109414.0`). Cuts were made with an explicit absolute path:

```
$ awk -v CUT=1793109414 '{cmd="date -d "$1" +%s"; cmd|getline e; close(cmd); if (e+0<=CUT+0) print}' \
      /home/vgpnk/Projects/shokunin/.ufo/watchdog.log > cut.log     # 1729 lines
$ head -1728 cut.log > cut1728.log                                   # 1728 lines
$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-driver-liveness.py \
      --log cut.log --state-dir /home/vgpnk/Projects/shokunin/.ufo/state --now 1793109500
```

Three independent artifacts agree:

| Artifact | log.lines | mori launches/completes/deads | mori unclosed | mori in_flight |
|---|---|---|---|---|
| committed receipt `evidence/driver-liveness-live.txt` | 1728 | 66 / 39 / 17 | 10 | true |
| re-run at 1728 lines (`--log cut1728.log`) | 1728 | 66 / 39 / 17 | 10 | true |
| report §2 run-1 table and §3 verbatim JSON | 1729 | 66 / 39 / 17 | 10 | true |
| re-run at 1729 lines (`--log cut.log`) | 1729 | 66 / 39 / 17 | 10 | true |

Re-run against the committed receipt, all lanes, every emitted field except the wall-clock age:

```
$ python3 -c '…json compare tool-1728.json vs receipt…'
1728-line rerun vs receipt: diffs= [] shape= {'lines': (1728, 1728), 'malformed': (0, 0), 'other_lines': (121, 121)}
```

The **pairing list itself reproduces as a multiset** for `mori` at the round-56 cut:

```
[(2,None), (19,2), (20,1), (21,1), (22,1), (37,1), (38,1), (38,3), (40,1), (56,1)]      (10 entries, 10 distinct)
```

The report §2 prints the same ten entries (ordering `(38,1),(38,3)` vs `(38,3),(38,1)` is the only
difference). An independently written parser (not importing the tool) agrees with the tool on
23/23 lanes × the 8 count/state fields (`launches, completes, deads, launch_fails, wraps,
rounds_seen, in_flight, unclosed`) and on log shape `lines=1729 malformed=0 other_lines=121`. Those
8 fields are the whole evidential content of the pairing claim; `last_launch_ts`/`last_launch_age_s`
were not re-derived by the independent parser (they are timestamp echoes, and the second parser
reproduced `mtime_age_s`/`newest_ts=1793109414.0` from the cut instead).
**Verdict on the list: accurate, complete, and reproducible.**

One off-by-one worth naming: the receipt (1728 lines) and the report run-1 (1729 lines) are two
adjacent log states, separated by one appended line — `complete kake round=63; hyaku-inline
attempt=1` (`cut.log:1729`). That single line is why the receipt says `kake completes=50,
in_flight=true, unclosed=13` and the report says `51 / false / 12`. Everything else — including all
mori fields — is identical. The round-56 knowledge entry quotes the receipt state (`1728 lines`), so
a C2 claim must not mix the entry's 1728 with the report's 1729.

## 2. What `unclosed` actually counts

Mechanism, from the frozen probe (`tools/mori-driver-liveness.py`):

- `:114` `key = (int(round_s), None)`; `:127-129` a launch with `attempt=N` re-keys to `(round,N)`;
  `:133` `row["open_launches"].append(key)` — **one entry per launch line**;
- `:116-120` `close_round()` removes **at most one** matching entry per close;
- `:143` complete and `:150` wrap both call `close_round()`; `:157` `lane-dead-no-report` removes
  **every** entry whose round matches;
- `:173` `"unclosed": len(row["open_launches"])`.

Measured budget at the round-56 cut (all 23 lanes, my independent re-derivation):

```
launches 842 − exact closes 546 − keys removed by dead lines 164 − wrap closes 9 = 123 = Σ unclosed
```

with 571 completes of which **25 closed nothing**, 22 wraps of which **13 closed nothing**, and 166
dead lines of which 163 removed ≥1 key, 3 removed nothing, and 1 removed two keys.
So `unclosed` is a booking residual over *launch lines*: it moves only when an unmatched launch is
appended or an open key is removed, and it is not a function of how many things are running.

## 3. Eight limits on reading the count (each with evidence)

**L1 — it is a multiset over launch lines, not a set of rounds or attempts.**
At cut, Σ`unclosed` = 123 entries but only **99 distinct** `(round, attempt)` keys: 24 entries are
duplicate copies. Worst case `kagi (16,None)` is counted four times:
`cut.log:311,324,342,374` (`launch kagi round=16 pid=…` ×4, none closed). Inline-driver rounds show
the same shape even where closes exist: `mori (38,1)` has 4 identical launch lines and `(38,3)` has
2, and after the available closes each still contributes exactly one counted entry (trace in §4).

**L2 — residue is monotone: an advance that writes no `complete` leaves a permanent entry.**
For `mori` at cut, 9 of the 10 entries are old rounds whose work is long over:
`r19,20,21,22,37` = one launch, zero closes; `r38` = 8 launches / 5 dead-clears / 1 complete → 2
residue; `r40` = 2 launches / 1 complete → 1; `r2` = one legacy `pid=` launch, zero closes.
Every one of these rounds is superseded (`mori` reached round 56 at cut, 57 now).

**L3 — closes can outnumber opens, so the counters are not complements.**
`tameshi round=18` is launched once (`cut.log:506`) and completed twice (`cut.log:522`,
`cut.log:531`); the second close finds nothing. 25 completes and 13 wraps at cut removed nothing,
and 72 `(lane, round, attempt, event)` groups in the cut log are duplicated lines (115 extra lines;
64 of them inline-driver launches, 16 inline completes, 35 legacy `pid=`/`runId=` launches). Across
the fleet, `launches − completes − deads − wraps` = **83**, not 123.

**L4 — `lane-dead-no-report` clears the whole round, so a still-open attempt can vanish.**
`:157` drops every key with that round. Live measurement: `kake round=59` had two open `(59,1)`
entries and the single dead line at `cut.log:1627` removed both.

**L5 — `wrap` closes only the bare `(round, None)` key.** `:150` calls `close_round()` while `key`
is still `(round, None)`; an attempt-keyed launch is untouched. Latent on the live log (0 wrap events
met an attempt-keyed open), active in a fixture (§4 F4).

**L6 — `in_flight` is "last event is a launch", an independent fact.** `:172` and the notes at
`:239` (`"in_flight/unclosed are log-shape facts, not health verdicts"`). At the round-56 cut both
numbers were "live-looking" for a lane whose live round then closed with no new launch:
`launch mori round=56` (`watchdog.log:1728`) → `complete mori round=56; hyaku-inline attempt=1`
(`:1736`) → `launch mori round=57` (`:1739`). `unclosed` went 10 → 10 across that whole turnover:
the live key changed identity and the count did not move.

**L7 — advances are journaled outside the log, so residue is unrecoverable from the log.**
Only three lines reach `watchdog.log`: `inline.sh:149` launch, `:176` complete, `:182`
lane-dead-no-report. The `advance` branch (`inline.sh:203-210`) writes `$STATE/outcome/<lane>-r<n>`
and `$STATE/next/<lane>` and reports closure debt through `ev()` (`inline.sh:34`), which appends to
`$STATE/events.log` — a file the probe never opens. Consequences measured on this host:
`$HOME/.local/state/shokunin-hyaku/outcome/mori-r{19,20,21,22,37,38,40}` all exist (rounds provably
closed), and `events.log` carries `2026-10-23T17:09:39-03:00 inline CLOSURE-DEBT lane=mori round=37
(advanced without a hyaku closure row)` — the exact residue key `(37,1)`.

**L8 — the probe never reads state values, so the driver's real round pointer is invisible.**
`:179-199` `state_shapes()` counts `*.round` entry *shapes* only. The lane's true pointer lives in
`$STATE/next/mori` (= `57`), while `.ufo/state/mori.round` still reads `2` (mtime 2026-10-15 01:50).
No field of the probe can contradict that stale value, and nothing in the probe can tell an
unmatched launch from a finished round.

## 4. Counterexamples, both directions

All five fixtures were run through the **real** probe (`--log` on a file in scratch, `--now` fixed);
numbers below are tool output, not mine.

| Fixture | Log content | Tool emits | Reading |
|---|---|---|---|
| F1 duplicate launches | 3 × `launch mori round=7 … attempt=1` | `unclosed=3 launches=3 completes=0` | one key, three counted |
| F2 advance without close | `round=1`, `round=2`, `round=3` launches, no closes | `unclosed=3` | three consecutive rounds cannot all be live |
| F3 dead clears the round | `attempt=1`, `attempt=2`, then `lane-dead-no-report round=5` | `unclosed=0 launches=2 deads=1`, `in_flight=false` | running work can be invisible |
| F4 wrap vs attempt key | `attempt=1` launch, then `wrap … fleet-wrap` | `unclosed=1 wraps=1` | overcount direction, activates L5 |
| F5 duplicate key, one close | two `attempt=1` launches, one `complete … attempt=1` | `unclosed=1` | one close cancels one line |

Live counterexamples:

- **Not running though counted (9 of 10 at cut):** `mori` rounds 2/19/20/21/22/37/38/40 are 3–12 days
  old; 7 of those 8 rounds have an explicit `outcome` row proving closure (L7). Round 38 trace
  (`cut.log:969,979,998,1005,1012,1022,1030,1039,1051,1060,1068,1081,1099,1104`): eight launches,
  five dead-clears, one complete → two residue entries, and the round advanced at
  `cut.log:1106` (`launch mori round=39`, 00:02:49) ten minutes after r38's last close (23:52:57) —
  nothing of r38 was still running.
- **Running though the count is uninformative:** the current round-57 wave runs dozens of seats
  under a single line, `2026-10-27T11:57:01-03:00 launch mori round=57 pgid=302171
  driver=hyaku-inline attempt=1`. The grammar has no seat, wave or subagent key: `LINE_RE` is
  `(event) (lane) round=N (rest)` (`tools/mori-driver-liveness.py:54-55`), and of the 1608 event
  lines in the cut log, all 35 that mention `w1`/`seat`/`subagent`/`wave` are `lane-dead-no-report`
  lines carrying those words inside the unparsed free-text reason
  (e.g. `cut.log:568` "171 seats already spawned, no live descendant"); **0** lines have a
  seat/wave identifier in the lane position. Per-worker concurrency is structurally outside the
  counter's domain.

**Verdict on the question asked:** `unclosed` is **not** a present-running count and must not be read
as one. It is a multiset count of launch lines that no later close removed from the same
`(lane, round, attempt)` key, minus keys removed wholesale by a dead line. The only fields that speak
to liveness are `in_flight` (last event is a launch) and `last_launch_age_s` (age of the last launch
line) — and even those are log-shape facts, not process probes.

## 5. Corrections to the round-56 report

1. **Finding 4 undercounts by 24.** It states "exactly 1 case in the whole log" of a `complete …
   attempt=N` with no matching open. Measured at the same cut: 546 exact matches, 0 round-level
   fallbacks, 0 wrong-attempt closes, and **25 completes that closed nothing** (16 attempt-keyed,
   9 `; respawning`). The report's single example (`kumitate round=50 attempt=2`) is written three
   times — `cut.log:1053` (which matches the open key), `cut.log:1070` and `cut.log:1091` (both close
   nothing) — so it is a duplicate-close triple, not one stray line. The conclusion
   ("latent mis-pairing channel") stands; its magnitude is 4.4% of closes, not one event.
2. **Finding 1's cause is narrower than stated.** "Rounds 2–40 whose `complete` line was never
   written" fits r19–r22 and r37, but not r38 (one complete written, residue from duplicate
   launches) or r40 (one complete for two launches). Two mechanisms, not one.
3. **Finding 3 verified, including its inertness claim.** Wrap events with an attempt-keyed open at
   the same round: **0** at the cut and 0 in the full log; 9 wraps closed `(round,None)`, 13 closed
   nothing. The asymmetry is latent and only fixture-reachable (F4).
4. **Receipt vs report line count (§1):** 1728 vs 1729, one appended `complete kake round=63`.

## 6. Eight source-grounded statements available for the C2 entry

`corpus/knowledge/watchdog-unclosed-r57.md` is **absent** at this tip, and `corpus/SOURCES.md` has no
`S548` row yet (`S547` is the highest id; `S548` is free). `count-c2.py` requires eight lines
starting `| K`, each carrying backticked quotes, `S548` present in entry **and** registry with status
`mined`, and the phrase `pairing count` in the entry. These eight statements are each anchored on a
located quote and are independent of this seat's prose:

| id | statement (one line) | located quote |
|---|---|---|
| K1 | `unclosed` is defined as launches with no same-`(lane,round,attempt)` close and is declared "a pairing count, not a failure claim" | `tools/mori-driver-liveness.py:34-36` — ``unclosed = launches with no same-(lane,round,attempt) complete — a pairing count, not a failure claim)`` |
| K2 | every launch line appends exactly one open entry, so duplicates are counted as separate entries | `:133` — ``row["open_launches"].append(key)`` |
| K3 | a close removes at most one entry, so one `complete` cannot cancel duplicate launches | `:116-120` — ``if key in row["open_launches"]: row["open_launches"].remove(key)`` |
| K4 | `lane-dead-no-report` removes every open key of the round, so an unmatched count can drop to zero while attempts remain open | `:157` — ``row["open_launches"] = [k for k in row["open_launches"] if k[0] != int(round_s)]`` |
| K5 | `wrap` reuses the bare round key, so an attempt-keyed launch survives a fleet-wrap | `:114` + `:150` — ``key = (int(round_s), None)`` … ``close_round()`` |
| K6 | `in_flight` is only "last event was a launch", and both fields are declared log-shape facts | `:172` — ``"in_flight": row["last_event"] == "launch"``; `:239` — ``"in_flight/unclosed are log-shape facts, not health verdicts"`` |
| K7 | the writer logs only launch/complete/dead; the round advance is journaled to the driver state dir, so a closed round can leave a permanent residue entry | `scripts/hyaku/inline.sh:149,176,182` and `:203-210` with `:34` — ``ev() { printf '%s inline %s\n' "$(date -Is)" "$*" >> "$STATE/events.log"; }`` |
| K8 | the probe reads `*.round` entry shapes only, never values, so the driver's true round pointer is outside its inputs | `:179-199` `state_shapes()` — shapes counted, ``values never read`` (`:37` docstring) |

Each statement is independently evidenced in §2–§4 above; no statement depends on the probe's own
verdict string.

## 7. Simplifier output

**Deletion candidate (proven behaviour-neutral, not applied — no edit scope):**
`row["attempts"]` is write-only dead state. Declared at `tools/mori-driver-liveness.py:112`
(`"attempts": {}`), populated at `:129` (`row["attempts"].setdefault(int(m2.group(4)), 0)`), and
never read: `grep -n attempts` returns exactly those two lines, the emitted lane dict (`:165-176`)
has no `attempts` key, and no field of any run contains the string. Proof of retained behaviour on a
patched scratch copy (`$SCRATCH/x/tools/patched.py`, both lines removed):

```
baseline --selftest : DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0
patched  --selftest : DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0
patched vs baseline on cut.log: lanes identical: True | log shape identical: True | verdict: True
```

Server note: no `lsp` device is mounted in this session, so the "no reader" proof is textual plus
the emitted-schema check above; it is not presented as semantic reference proof.
Tradeoff: the field is a plausible future hook for attempt-rollover accounting, but nothing consumes
it today and `t_attempt_rollover` passes without it.

**Second candidate, docs-only (stale invocation string carried forward):** both frozen counters take
a revision argument and call `git show f"{R}:…"`. The round-57 contract's commands
`python3 .ufo/waves/round-57/count-c1.py R` and `… count-c2.py R` pass the literal `R`, and
`git rev-parse R` in the lane exits **128**, so the documented command cannot produce a receipt as
written (`git show R:SCORECARD.md` fails → `C1=unmet`). The round-56 report already logged this wart;
it has now been copied into the live round's contract. The fix is an invocation string (a concrete
sha, e.g. the freeze commit `618562c7…`), never a predicate or counter change.

**Preserved contract:** C2's predicate, evidence targets, controls and counters were not touched;
the ten-entry pairing list and every round-56 receipt still reproduce (§1). No file outside this
report was written; the probe, the log, the driver state and the lane repo are byte-untouched.

**Where I stopped:** the next deletion (the `elif` at `:119-120`) would remove the only round-level
fallback that keeps a legacy `launch round=N` paired with an attempt-keyed `complete`; it is reachable
on the complete path even though it is inert for wrap/dead, so deleting it would trade a real
(lenient) contract for two lines. That harms an axis, so it stays.

## 8. Hygiene

- Files written: this report only
  (`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-57/w1/Mo57Simplifier64.md`).
- Scratch `/fast/scratch/hyaku/mori-r57/Mo57Simplifier64/` (fixtures, cut logs, patched copy under a
  symlinked fixture dir) — removed before yielding; `TMPDIR` pointed inside it.
- No git/jj mutation; only `git -C … rev-parse/status/show`, `sha256sum`, `grep`, `awk`, read-only
  `python3`. No write to `watchdog.log`, `.ufo/state`, `$HOME/.local/state/shokunin-hyaku` or any
  PATH directory. No pacman, no tool install. No host state remediated; no lane declared dead from a
  missing report. No secrets, credentials, session tokens or private URLs reproduced.
