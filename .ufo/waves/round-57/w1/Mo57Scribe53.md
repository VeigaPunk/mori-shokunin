# Mo57Scribe53 — C2 source-grounding (one quote, tested)

Seat: Mo57Scribe53, leaf, detection/report only. Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`,
entering tip `53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`, freeze commit `618562c72a03dc4d17386b715357f863fd327274`
(= current `HEAD`). No product code, counter, contract, or jj/git state was modified.

## Quote under test

Exact, from the committed source report (`corpus/knowledge/driver-liveness-r56.md`, sha256
`ce438eeb42ac92b5ad9b4a2058d9256cb17b411db5d964c041e8c5caaa0866b2`):

- **:22-23** — "`unclosed` (launches\nwith no same-round close)" — the definition the round-57 C2 entry
  must cite for its central statement.
- **:62-63** (limits) — "`in_flight`/`unclosed` are pairing facts over log lines, not health verdicts;\na lane
  with an unclosed launch is *in flight by the log*, not \"stuck\"."
- **:56** — "mori: 66 launches / 39 completes / 17 deads / in_flight / unclosed 10" (note: the `in_flight`
  token carries no value between the slashes).

Claim it supports (C2 predicate): **`unclosed` is a pairing count over log lines, not a present-running
count.** Tested by reconstructing the count from the log independently and by reproducing the committed
receipt.

## Method (read-only, scratch only)

Frozen log snapshot `/fast/scratch/hyaku/mori-r57/Mo57Scribe53/watchdog.log`, sha256
`96370930e99dac70ade2093fba3aa84850556d732c13a6770b546bc35efe70fb`, 1742 physical lines, mtime
2026-10-27 12:46:16 -03:00, copied from `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log`.

1. Wrote an independent parser from the S544/S547 line grammar (no import of `tools/mori-driver-liveness.py`),
   then diffed it field-by-field against the shipped tool on the same snapshot.
2. Ran the shipped tool on the first 1728 lines to reproduce the committed receipt exactly:
   `python3 tools/mori-driver-liveness.py --log <snapshot> --state-dir /nonexistent`.
3. Enumerated every launch left open, its round vs the lane's max round, whether any later same-round
   close line exists, and which close kind retired it.

Committed receipt read: `.ufo/waves/round-56/evidence/driver-liveness-live.txt` (JSON body + trailing
`exit=0`; parsed up to that suffix).

## Result 1 — the central claim holds (pairing, not present-running)

- Independent parser vs shipped tool on the same snapshot: **0 differences** over 23 lanes ×
  {launches, completes, deads, wraps, launch_fails, unclosed, in_flight}. Log shape agrees on both:
  1742 lines, `malformed 0`, `other_lines 121`, 23 lanes.
- **106 of 124 open launches (85.5%) belong to a round earlier than their lane's max round** — historical
  residue, not current work.
- **9 lanes have `unclosed > 0` while `in_flight` is false**: kake 12, kagi 10, tameshi 7, kaidoku 6,
  kasegi 6, kengaku 6, tsukuroi 5, kotodama 4, souji 3.
- Four lanes (`audio`, `game-dev-2d`, `game-dev-3d`, `lore`) have `unclosed 1` with a single launch
  1 076 499 s (~12.46 d) old and zero completes.
- `mori` at the snapshot: 67 launches / 40 completes / 17 deads / `in_flight true` / `unclosed 10`; the 10
  open launches are rounds **{2, 19, 20, 21, 22, 37, 38, 38, 40, 57}** — oldest
  `2026-10-15T01:50:57-03:00 launch mori round=2 pid=2685430`, newest
  `2026-10-27T11:57:01-03:00 launch mori round=57 pgid=302171 driver=hyaku-inline attempt=1`.

So the statement "`unclosed` is a pairing count over log lines, not a present-running count" is
**confirmed and reproducible**.

## Result 2 — the quoted definition is materially wrong (27/124 cases)

The literal phrase "launches with no same-round close" is false for **27 of the 124** launches counted
unclosed: each has a *later, same-round* `complete`/`wrap` line in the log. The tool's actual rule is a
running launch-minus-close ledger where **one close retires at most one previously open launch of the same
round** (same `attempt` for completes), and a close that arrives with nothing open retires nothing
(`tools/mori-driver-liveness.py:116-121` `close_round()` removes one list element; `:173`
`"unclosed": len(row["open_launches"])`).

Two exact instances:

- `kagi round=28`, three `attempt=1` launches and one complete:
  `621 launch ... attempt=1`, `1089 launch ... attempt=1`, `1260 launch ... attempt=1`,
  `1270 complete kagi round=28; hyaku-inline attempt=1` → **2** residue for that round alone.
- `kagi round=16`, wrap-then-relaunch:
  `257 launch ... runId=...`, `282 wrap kagi round=16 complete; NOT respawning (fleet-wrap)` (retires 257),
  `292 wrap ...` (retires nothing), then `311`, `324`, `342`, `374 launch kagi round=16 pid=...` → **4**
  residue; kagi's 10 = {round 1:1, 16:4, 24:1, 25:1, 26:1, 28:2}.

`unclosed` is therefore "launches not retired by a close that arrived after them", not "rounds lacking a
close". A round can be wrapped *twice* and still contribute 4. The tool docstring
(`tools/mori-driver-liveness.py:34-36`, "launches with no same-(lane,round,attempt) complete") is closer but
still incomplete: duplicate or post-wrap relaunches at the *same* attempt stay open even though a matching
complete exists (kagi 621/1089 vs 1270).

Close kinds are also asymmetric: `lane-dead-no-report` retires **all** opens of its round
(`tools/mori-driver-liveness.py:151-153`), unlike completes/wraps which retire one. Two measured events clear
two opens apiece: `tameshi round=33` (launches 940, 953 → dead 955) and `kake round=59` (launches 1612, 1614
→ dead 1627). Any eight-claim entry that says "one close per launch" must carve out the dead case.

## Result 3 — "a lane with an unclosed launch is *in flight by the log*" is refuted by the same output

`in_flight` is only `last_event == "launch"` (`tools/mori-driver-liveness.py:172`). Nine lanes have
`unclosed > 0` and `in_flight` false (list in Result 1), e.g. kagi: last event `complete` at line 1270,
`unclosed 10`, `in_flight false`. The sentence at `driver-liveness-r56.md:62-63` conflates a cumulative
ledger with a last-event predicate; a C2 entry must not repeat it.

## Result 4 — receipt reproduction is exact at its own snapshot, not on a live rerun

- Shipped tool on the **first 1728 lines** reproduces the committed receipt verbatim where it matters:
  mori 66 launches / 39 completes / 17 deads / in_flight true / unclosed 10; total `unclosed` 124; 23 lanes;
  malformed 0; other_lines 121.
- On the **current** log (1742 lines, +14 from round-56/57 activity) the same command yields mori
  67/40/17/true/10 and total `unclosed` 124 (e.g. line 1739 `2026-10-27T11:57:01-03:00 launch mori round=57`).
  The report's "re-running the command reproduces it modulo ages" (`:57-58`) holds for `unclosed`, but
  launches/completes advance with the log. Adjacent seats should score against the frozen receipt, not a
  live rerun.

## Verdict

- **Central C2 claim (pairing count, not present-running): supported, independently reproduced**
  (124 total / 106 historical / 9 `unclosed>0 & in_flight=false`).
- **Quoted definition at `:22-23`: not exact — 27/124 counted-unclosed launches have a later same-round
  close.** The C2 entry should state the ledger form: per lane, a launch adds one; a `complete` retires one
  open launch of the same round and attempt (fallback: unkeyed); a `wrap` retires one unkeyed open launch of
  the round; a `lane-dead-no-report` retires every open launch of the round; an unmatched close is discarded.
- **`:62-63` second clause: refuted** by the same run; use "an unclosed launch is a historical launch with no
  later close, not evidence the lane is running".
- **`:56` formatting:** `in_flight` is printed without a value; cite `in_flight true` from the receipt body
  instead.

## Limits of this seat

- One host, one log snapshot (sha256 above); the log is append-only and keeps growing, so counts move.
- The grammar itself was taken as frozen from S544/S547; re-deriving it from `inline.sh` / `shokunin-watchdog.sh`
  writer lines was not this seat's scope.
- Independent reimplementation is semantic, not code-diverse: it mirrors the documented grammar and was
  validated by a 0-diff comparison against the shipped tool, so it cannot catch a defect the tool shares with
  its own docstring (the 27-case gap was found by cross-checking against the *log*, not the code).
- Scratch (`/fast/scratch/hyaku/mori-r57/Mo57Scribe53/`) held the snapshot, the independent parsers, and the
  three result JSONs; it was removed after the numbers above were transcribed. `/tmp` unused.

## Touched surfaces

- Wrote: `.ufo/waves/round-57/w1/Mo57Scribe53.md` (this file).
- Read: contract, controls, counters, `corpus/knowledge/driver-liveness-r56.md`, `corpus/SOURCES.md`,
  `tools/mori-driver-liveness.py`, `.ufo/waves/round-56/evidence/driver-liveness-live.txt`, fleet
  `.ufo/watchdog.log` (read-only copy).
- No installs, no pacman, no git/jj mutation, no fleet-root tracked files.
