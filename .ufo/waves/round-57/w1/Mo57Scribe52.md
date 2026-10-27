# Mo57Scribe52 — C2 depth: verification of the round-56 driver-live `unclosed` claim

Seat: Mo57Scribe52 (scribe, mori-shokunin lane, round 57 wave w1).
Assignment: reopen the committed round-56 driver-live report, verify its pairing list, and
determine whether `unclosed` counts mean running work. Detection/report only; no product edit,
no git/jj mutation, no host remediation.

Frozen inputs read (absolute paths):

- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-57/contract.md` (C2 predicate:
  eight source-grounded statements on the interpretation and limits of the watchdog `unclosed`
  pairing count, and the statement that `unclosed` is a pairing count rather than a present-running
  count).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-57/controls.txt` (both counters
  `unmet` at the entering revision, exit 1).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/w1/Mo56ExecDriverLive.md`
  (the report under verification).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-56/evidence/driver-liveness-live.txt`
  (committed round-56 evidence capture).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-driver-liveness.py`,
  `/home/vgpnk/Projects/shokunin/scripts/hyaku/inline.sh`,
  `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log`,
  `/home/vgpnk/.local/state/shokunin-hyaku/events.log` (read-only).

Scratch: `/fast/scratch/hyaku/mori-r57/Mo57Scribe52/` (removed at exit; `TMPDIR` pointed there).
Disk gate before work: `bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status`
→ exit 0, no pressure. No tool installed or updated; stock `python3` only, no pacman run.

---

## 1. Commands executed (all read-only)

```
python3 /fast/scratch/hyaku/mori-r57/Mo57Scribe52/pair.py        # independent pairing replay, full log
python3 /fast/scratch/hyaku/mori-r57/Mo57Scribe52/prefix.py 1728 # replay truncated at the round-56 snapshot
python3 /fast/scratch/hyaku/mori-r57/Mo57Scribe52/prefix.py 1742 # replay of the full current log
python3 /fast/scratch/hyaku/mori-r57/Mo57Scribe52/classify2.py   # residual-key classification
python3 /fast/scratch/hyaku/mori-r57/Mo57Scribe52/variants.py    # wrap / lane-round-failed variants
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-driver-liveness.py \
    --fleet-root /home/vgpnk/Projects/shokunin > now.json      # exit 0, stderr 0 bytes
```

The replay was re-implemented from the frozen grammar (regexes transcribed from
`tools/mori-driver-liveness.py:54-62`), not imported from the tool, so the probe is not graded on
its own code.

Log state at read time: `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` — 1742 lines, 164853
bytes, sha256 `96370930e99dac70ade2093fba3aa84850556d732c13a6770b546bc35efe70fb`, append-only (the
round-56 snapshot at line 1728 is an exact prefix of today's file).

## 2. The committed pairing list is reproduced exactly

Replaying the log truncated at line 1728 — the exact snapshot the round-56 evidence file records
(`lines: 1728`, `newest_ts: 1793106516.0`) — gives, for `mori`:

```
mori launches=66 completes=39 deads=17 unclosed=10
mori_open_keys [(2,None), (19,2), (20,1), (21,1), (22,1), (37,1), (38,1), (38,3), (40,1), (56,1)]
```

That is byte-for-byte the set printed in
`.ufo/waves/round-56/w1/Mo56ExecDriverLive.md` §2 ("only `(56,1)` is the currently-live round") and
the count triplet `66 / 39 / 17` in its §2 table and §3 JSON. Independently reproduced: **the
round-56 report's pairing list and mori counts are correct for the log it read.**

Whole-log cross-check at the same prefix: my replay totals **124** open entries across 23 lanes;
summing the 23 `unclosed` values in
`.ufo/waves/round-56/evidence/driver-liveness-live.txt` also gives **124** (kake 13, kama 11,
mori 10, tameshi 8, chousa/tabi/kotoba 7, kagi 10, …). The report's "123" figure is its run1
(line 1729, one `complete kake round=63` more) — consistent, not contradictory.

Replaying the current full log (1742 lines) yields `unclosed` still **10** for mori, with `(56,1)`
replaced by `(57,1)`: `complete mori round=56; hyaku-inline attempt=1` is at log line 1736
(2026-10-27T11:44:43) and `launch mori round=57 … attempt=1` at line 1739 (11:57:01). The counter
did not move when a round demonstrably finished.

## 3. Does `unclosed` mean running work? — No

Verdict: **`unclosed` is a pairing/backlog count and is not a present-running count.** Five
independent counterexamples, each reproducible from the cited lines:

**C-1 — a finished round still counts.** `mori` round 38 and round 40 each have a `complete` line
in the log (`watchdog.log:1104` `complete mori round=38; hyaku-inline attempt=1`,
`watchdog.log:1144` `complete mori round=40; hyaku-inline attempt=1`) and a driver advance row in
`events.log` (`inline round-done lane=mori round=38 outcome=admitted next=39`,
`… round=40 outcome=rejected next=41`), yet both still contribute to `mori.unclosed`:
`(38,1)` and `(40,1)` are residual because each round was launched twice under the same
`attempt=1` key (round 38: launches at `watchdog.log:1081` and `:1099`; round 40: `:1118` and
`:1134`) and one `complete` removes only one list entry (`tools/mori-driver-liveness.py:116-121`).

**C-2 — an idle lane carries ten.** `kagi`: `unclosed=10` but `in_flight=false`; the lane's last
line in the log is `complete kagi round=28; hyaku-inline attempt=1` at `watchdog.log:1270`
(2026-10-25T04:05:19) — roughly two days before the round-56 read. Its ten entries cover only six
distinct rounds `{1,16,24,25,26,28}`, including four identical `(16,None)` entries
(`watchdog.log:311,324,342,374`).

**C-3 — a twelve-day-dead lane reports `in_flight=true`.** `aggregator`: last event is
`launch aggregator round=10 pid=2685182` at `watchdog.log:390` (2026-10-15T01:50:57), so
`in_flight=true` and `unclosed=2` — but the log itself already ended that round eight lines
earlier: `lane-round-failed aggregator round=10 :: marker/contentless report; NOT advancing`
(`watchdog.log:356`, `:389`). The grammar has no `lane-round-failed` event
(`tools/mori-driver-liveness.py:54-55`), so all 35 such lines in the log are counted as
`other_lines` (121 total) and close nothing.

**C-4 — residue can be older than the lane's current round.** Eight lanes have every residual
round strictly behind their latest launch round (`kaidoku` 43 vs max 23, `kotodama` 74 vs 65,
`kengaku` 48 vs 28, `kasegi` 41 vs 23, `kake` 63 vs 46, `souji` 34 vs 22, `tsukuroi` 47 vs 22,
`tameshi` 53 vs 35), and nine of the 23 lanes are `in_flight=false` with `unclosed` between 3 and
12. Oldest residual in the log: `kagi` round 1, `watchdog.log:3`, 2026-09-28T15:50:56 (~29 days).

**C-5 — the counter is insensitive to a round finishing.** `mori.unclosed` is 10 at log prefix
1728 (`(56,1)` live) and 10 at prefix 1742 (`(57,1)` live), with round 56 closed in between.
A field that does not move when work completes is not a live-queue gauge.

Quantified over the full current log: **124 residual entries over 94 distinct `(lane, round)`
pairs** (inflation 124/94 ≈ 1.32×). Classification of the 124 residuals against later closing
evidence in the same lane:

| Class | n | Meaning |
|---|---|---|
| `NEVER-CLOSED` | 97 | no complete/wrap for that round after the launch line |
| `CLOSE-AFTER (consumed by duplicate same-key launch)` | 19 | round DID get a `complete`; a duplicate same-key launch kept one phantom entry (includes `mori r38 a1@1099`, `mori r40 a1@1134`) |
| `ROUND-CLOSED-DIFF-KEY` | 8 | round closed under a different attempt key (includes `mori r38 a3@1068`) |

So **27 of 124 (21.8 %) residuals sit on rounds that received a `complete`/`wrap` after the
launch**. A further 20 would clear if `lane-round-failed` were a parsed event (replay variant:
`total_open` 124 → 104, −16.1 %).

## 4. Corrections to the committed round-56 report (findings still hold; two sentences need narrowing)

The report's Finding 1 direction is correct — `unclosed` is a monotone historical backlog, not a
live-queue count. Two of its supporting sentences are not exactly true and must not be copied
verbatim into a C2 claim row:

1. §2 and Finding 1 say the nine non-current mori keys are "rounds 2–40 whose complete line was
   never written". **Falsified for rounds 38 and 40**: `complete mori round=38; …` exists at
   `watchdog.log:1104` and `complete mori round=40; …` at `:1144`. Their residue is the
   duplicate-same-key phantom of C-1, not a missing complete. For the other seven keys the
   sentence holds at the key level (`(38,1)`'s sibling `(38,3)` also has no closing event).
2. Finding 2 says "the `advance` branch … emits **no** `watchdog.log` line". True for
   `watchdog.log`, but imprecise as a statement of the gap: `advance` emits
   `ev "round-done lane=$lane round=$n outcome=$outcome next=$((n+1))"`
   (`scripts/hyaku/inline.sh:212`) through `ev()` (`inline.sh:34`), which appends to
   `$HYAKU_STATE/events.log` — **not** to `watchdog.log`, and the probe never opens `events.log`
   (`grep -n "events.log\|round-done" tools/mori-driver-liveness.py` → no match). That log does
   close the loop: e.g. `inline round-done lane=mori round=37 outcome=none next=38`
   (2026-10-23T17:09:39) and `… round=22 outcome=admitted next=23` prove rounds 22 and 37 finished
   while their watchdog entries stay `unclosed`. Measured: 41 `round-done lane=mori` rows exist;
   `events.log` begins 2026-10-19T23:10:52, so rounds 2/19/20/21 have no advance row at all.

Findings 3 (wrap is inert), 4 (one unmatched complete), 5 (`lane.with.dot` silently `other_line`),
6 (`--selftest` exit 0 with skips), 10 (`in_flight` is a log-shape fact) were re-checked against
the live log and hold. Finding 3 measured independently: recomputing with "wrap clears the whole
round" gives the identical 124 at prefix 1728 and **0** wrap events leave an attempt-keyed entry
open. Finding 4's live count is unchanged (the kumitate r50 case is still the only one).

## 5. Source-grounded material for the eight C2 claim rows

Each row below is a locatable quote plus its line, usable as one C2 claim ("quote located in the
source copy"). The tool source is the natural newly-opened source row.

| # | Statement | Located quote / line |
|---|---|---|
| 1 | `unclosed` is defined as launches with no matching complete, i.e. a pairing count | `tools/mori-driver-liveness.py:35-36` "unclosed = launches with no same-(lane,round,attempt) complete — a pairing count, not a failure claim" |
| 2 | It counts launch entries, not rounds (re-launch inflates) | `tools/mori-driver-liveness.py:173` `"unclosed": len(row["open_launches"])` over a **list** appended per launch (`:133`); live: aggregator 2 entries / 1 round, kagi 10 / 6 |
| 3 | A close removes exactly one entry; duplicates leave phantoms | `tools/mori-driver-liveness.py:116-121` (`close_round` uses `list.remove`, first match only); live: `mori r38 a1` launches `:1081`,`:1099`, one complete `:1104` |
| 4 | A complete closes only its own attempt key, falling back to `(round,None)` | `:134-143` (`key = (round, attempt)` at `:140`, then `close_round()` at `:143`); live: 8 `ROUND-CLOSED-DIFF-KEY` residuals (e.g. `mori r38 a3@1068` vs complete `a1`) |
| 5 | `lane-dead-no-report` clears *every* open entry of that round (unlike complete) | `:151-157` (`open_launches = [k for k in … if k[0] != round]` at `:157`); live: r38 deads at `:979,1005,1022,1039,1060` wiped all attempts |
| 6 | `wrap` closes only the `(round,None)` key, so an attempt-keyed launch survives it (latent) | `:144-150` + `:116-121`; measured inert today: identical totals (124) under both models, 0 affected wraps |
| 7 | The grammar has no `lane-round-failed` event, so that whole class is invisible to pairing | `:54-55` `LINE_RE` alternation; live: 35 such lines (e.g. `watchdog.log:356,389` for aggregator r10), all in `other_lines` |
| 8 | Round closure is recorded only in `events.log` (`round-done`), which the probe never reads | `scripts/hyaku/inline.sh:212` and `:34`; probe has zero references to `events.log`/`round-done`; live: 41 `round-done lane=mori` rows, 0 in `watchdog.log` |

The contract's required sentence — "`unclosed` is a pairing count rather than a present-running
count" — is **directly supported** by rows 1, 2, 3, 8 and by counterexamples C-1…C-5. No frozen
predicate, counter, kill rule, or claim was changed; nothing was remediated.

## 6. Verdict

- **Round-56 pairing list: verified.** Exact reproduction at the evidence snapshot (prefix 1728),
  including the exact key set and `66/39/17/10` for mori, and the 124-entry fleet total.
- **Round-56 interpretation: right direction, two sentences too broad** (§4 items 1 and 2). A C2
  row must say "residue whose completing line is absent **or was consumed by a duplicate same-key
  launch**", not "complete line was never written"; and it must name `events.log`/`round-done` as
  the unread closure source.
- **`unclosed == running work`: refuted** by five independent counterexamples, including a round
  that completed (`mori` r38/r40) and a lane idle two days (`kagi`).
- **C2 premise for the wave: sound.** Eight source-grounded statements exist (§5), each with a
  located quote, and the required pairing-vs-running statement is demonstrable.

## 7. Hygiene, touched surfaces, out of scope

- Files written by this seat: this report
  (`.ufo/waves/round-57/w1/Mo57Scribe52.md`, relative to
  `/home/vgpnk/Projects/shokunin/mori-shokunin`) and the scratch tree
  `/fast/scratch/hyaku/mori-r57/Mo57Scribe52/` (removed on exit).
- Read-only only: the lane repo, the fleet log, `events.log`, `inline.sh`, the tool source. No git
  or jj mutation, no commit, no host change, no process touched. No production or fixture edit; no
  pacman; no secrets or private URLs reproduced.
- Out of scope (not done, not claimed): writing the C2 entry or counter, altering the frozen
  predicate/counters, judging C1, and any recommendation to change `tools/` — the "route to round
  57" items in the round-56 report remain unscheduled suggestions, not work performed here.
