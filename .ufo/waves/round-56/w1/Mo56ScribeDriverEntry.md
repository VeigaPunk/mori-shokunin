# Mo56ScribeDriverEntry — w1 scribe: entry vs code, side by side

Seat: Mo56ScribeDriverEntry (scribe, leaf). Lane mori-shokunin.
Freeze tip read: `8be2717b0809281d07dffe83dad424a4859e0747`.
Entry: `corpus/knowledge/driver-liveness-r56.md` (byte-identical at `8be2717b` and in the
working tree — `git diff 8be2717b -- corpus/knowledge/driver-liveness-r56.md` printed nothing).
Tool: `tools/mori-driver-liveness.py` at `8be2717b`, sha256
`6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997` (= the C1 counter `PIN`).
Everything below is read-only; no product file was touched. Report file is the only write.

## Method and inputs

| input | how obtained | value |
|---|---|---|
| tree at freeze tip | `git -C <lane> archive 8be2717b \| tar -x -C $S/tree` | 479-line tool, 9 fixture dirs |
| S544 extract | `git show 8be2717b:corpus/evidence/sources-r56/watchdog-log-grammar.txt` | sha256 `38ba3e6b309e17d3d8038e8986e274bb363ac893d1c325fe145a95882a417796` (header's `38ba3e6b…` ✓) |
| live log | `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log`, read-only | 1729 non-blank lines, 0 blank |
| committed receipt | `git show 8be2717b:.ufo/waves/round-56/evidence/driver-liveness-live.txt` | 304 lines, JSON body + `exit=0` trailer |
| writer source | `sed -n '149p;176p;182p' scripts/hyaku/inline.sh`, `sed -n '241,249p;266p;398p;405p;448p' scripts/shokunin-watchdog.sh` (fleet repo) | all cited lines exist |

Scratch: `/fast/scratch/hyaku/mori-r56/Mo56ScribeDriverEntry/` (archive tree, `tmp/`); removed at exit.
No tool install or upgrade; no pacman; nothing written outside the report path.

## What the probe does (verified against the code)

`LINE_RE` (`tools/mori-driver-liveness.py:54-55`) is
`^(\S+) (launch|complete|lane-dead-no-report|launch-fail|wrap) ([A-Za-z0-9_-]+) round=(\d+)(.*)$`.
Per-event rest grammars: `:56-62`. `parse_log` (`:77-176`) counts `lines` = non-blank lines,
`malformed` (non-ts first token, or an event line whose rest fails its regex; at most
`MAX_MALFORMED_EXAMPLES = 3` examples, `:63`), `other_lines` (ts-first line that `LINE_RE`
does not match, `:100-101`), and per-lane `launches/completes/deads/launch_fails/wraps/rounds_seen/
last_launch_ts/in_flight/unclosed`. `close_round` (`:116-121`) removes `(round,attempt)` when a
`complete` names an attempt, else `(round,None)`; `wrap` closes the round the same way; a
`lane-dead-no-report` drops every open key of its round (`:157`). `state_shapes` (`:179-197`)
counts `*.round` names as regular/symlink/dir/other, testing `islink` first (`:188-189`).
`run` (`:201-247`) returns rc 2 `DRIVER_LIVENESS_UNAVAILABLE` on absent/unreadable/empty log,
otherwise rc 0 `DRIVER_LIVENESS_OK`; it writes nothing.

Executed evidence:

```
$ python3 tools/mori-driver-liveness.py --selftest
DRIVER_LIVENESS_SELFTEST pass=13 fail=0 skipped=0
exit=0
```

Per-fixture run at `8be2717b` (`--fixture <dir> --now 1800000000`), verdict always
`DRIVER_LIVENESS_OK`:

```
attempt-rollover malformed=0 other=0 lines=4      in-flight       malformed=0 other=0 lines=1
fails-and-dead   malformed=0 other=0 lines=2      legacy-grammar  malformed=0 other=0 lines=2
hyaku-pairing    malformed=0 other=0 lines=2      malformed       malformed=5 other=1 lines=7
state-shapes     malformed=0 other=0 lines=1      two-lanes       malformed=0 other=0 lines=3
variants         malformed=0 other=2 lines=12
```

These are exactly the nine names and the nine frozen malformed counts in `count-c1.py:40-43`.
The entry names no fixture, so no fixture claim in the entry needs correction.

Receipt cross-check (JSON body, trailer stripped at `\nexit=`):

```
lines=1728 malformed=0 other_lines=121 lanes=23
mori: launches=66 completes=39 deads=17 wraps=0 launch_fails=0 in_flight=true unclosed=10
launch_fails total=7  wraps total=22  inflight lanes=14  unclosed total=124
```

Entry lines 48-51 state `1728 lines, 0 malformed, 121 other_lines, 23 lanes` and
`mori: 66 / 39 / 17 / in_flight / unclosed 10` — all five match the committed receipt. ✓

## Sentence-by-sentence verdicts

| entry line | claim | verdict | basis |
|---|---|---|---|
| 3 | `source: S544 (the driver scripts that write the log — grammar authority)` | over-broad | three ts-first line families in the log are not written by those two scripts (see finding F2) |
| 4 | extract sha256 `38ba3e6b…` | ✓ | recomputed |
| 5 | `recheck: on-release` | ✓ | registry S544 recheck cell `on-release` |
| 6 | FR5 open ground named in `corpus/README.md` | ✓ | `corpus/README.md:345` |
| 10-11 | inline driver → no daemon → `WATCHDOG_ABSENT` every round | inherited, not re-observed | repeated from `corpus/README.md:345`; `evidence/census-start.txt` is a W04 duplicate list, 0 WATCHDOG occurrences (`grep -c WATCHDOG_ABSENT` → 0) |
| 13-18 | per-lane fact list, log shape, `other_lines` = driver prose | partly wrong | `rounds_seen` is a per-lane field the entry omits; `other_lines` is not prose-only (F1) |
| 16-17 | `unclosed` = "launches with no same-round close" | gloss | attempt keying and dead/wrap closes are dropped (F7) |
| 19-20 | "Every field is a shape fact; no health verdict; never remediates" | ✓ (verdict = data-availability) | `run` writes nothing; JSON has `verdict=DRIVER_LIVENESS_OK/…UNAVAILABLE` only |
| 24 | "Two writers share one log" | wrong | F2 |
| 25 | "every variant observed in the committed live log" | wrong twice | the log is **not committed** (F3) and event-shaped families are unmodeled (F1) |
| 27-30 | launch grammar and optionality order | order wrong | code order is `pgid`, `driver`, `slot`, `attempt`, `mission` (`:56-58`); entry puts `attempt` before `slot` (F4) |
| 31-33 | complete forms | ✓ grammar; `advancing to round=` unobserved in the log | log: 473 `; hyaku-inline attempt=N`, 98 `; respawning`, 0 `; advancing to round=` |
| 34-37 | dead wrapper + varying inner text | ✓ | 156 `(hyaku-inline attempt=N: …)`, 3 `(hyaku: headless attempt ended …)`, 7 bare |
| 38 | launch-fail ` :: reason` | ✓ grammar + 7 log lines | but not in the extract (F5) |
| 39-40 | wrap ` landed`/` complete`, `shokunin-watchdog.sh:398` | partly | 398 emits `landed` only; the log's 22 wraps are all ` complete`, whose writer the extract does not name (F10) |
| 41-44 | other_line vs malformed rule | code-true, characterisation wrong | 35 event-shaped lines land in `other_lines` (F1); a malformed event line still creates a lane row (F6) |
| 49-51 | measured numbers | ✓ | receipt |
| 51-52 | "full receipt is committed; re-running reproduces it modulo ages" | wrong for counts and input | log grew (F3) |
| 56-57 | in_flight/unclosed are pairing facts | ✓ | code |
| 58-59 | "never follows symlinks" | over-scoped | state entries are not followed (`:188-189`), but `os.path.isfile(log_path)`/`open` follow a symlinked log path (`:204`, `:210`) (F8) |
| 60-62 | driver-authored shape, rewritten log rewrites reading | ✓ | code reads text only |
| 63-64 | age from log timestamp, clock moves change age only | ✓ | `parse_ts`→`fromisoformat(...).timestamp()`, `now - ts` |

## S544 anchor-quote check

The seat asks whether two S544 anchor quotes are true substrings of the extract and ≤25 words.
The entry contains no verbatim located quote from the extract; its two S544 line-anchored
quotations that read as literal writer text are the `complete` templates at entry lines 31-32.
Both fail literal substring equality, and both are well under 25 words:

| candidate | words | substring of extract? | extract text |
|---|---|---|---|
| `; hyaku-inline attempt=a` (inline.sh:176) | 3 | **no** | `; hyaku-inline attempt=$(claim "$lane" attempt)` |
| `; advancing to round=n+1` (watchdog:405) | 4 | **no** | `; advancing to round=$((n+1))` |

Both are renderings of the writer template with the shell expansion replaced by a value;
`=a` and `=n+1` are not in the bytes. Every other S544-attributed fragment in the entry:

| fragment (entry line) | in extract | in live writer source |
|---|---|---|
| `pgid=` (27) | yes | yes, 149 and 266 |
| `driver=` (27) | yes | yes, 149 |
| `slot=` (27) | no | no (log-only: 3 lines) |
| `mission=` (27-28) | no | no (log-only: 3 lines) |
| `runId=` (28) | no | no (log-only: 93 lines) |
| `pid=` (28) | no | no (log-only: 50 lines) |
| `; retry same round` (34) | yes | yes, 182 and 448 |
| ` :: reason` (38) | no | yes, 241-249 |
| ` landed` (39) | no | yes, 398 |
| ` complete` (39) | no | no (log-only: 22 lines) |
| `; NOT respawning (fleet-wrap)` (39) | no | yes, 398 |
| `hyaku-inline attempt=a: reason` (36) | no | yes, 182 (`$a`/`$why`) |

The extract carries exactly the six registry anchors (`inline.sh` 149/176/182,
`shokunin-watchdog.sh` 266/405/448); the entry additionally cites 241-249 and 398, which the
committed copy does not contain (F5).

## Proposed replacement text (for the L1; data may be corrected, pins are the L1's call)

Proposal A — replace entry lines 27-30 (launch bullet):

```
* `launch` — `pgid=N` followed, in this fixed order, by optional `driver=…`,
  `slot=N`, `attempt=N`, `mission=…`; or bare `pid=N`; or `mission=…` alone; or
  `runId=…`; or no rest at all (S544 `inline.sh:149` emits `pgid=$$ driver=hyaku-inline
  attempt=$a`, `shokunin-watchdog.sh:266` emits `pgid=$pid`; the `pid=`,
  `mission=`-alone and `runId=` forms are log-observed variants whose writers the
  committed extract does not carry). The pgid-chain fields are order-fixed:
  `attempt=N` before `slot=N` is malformed (probe input 2026-10-27).
```

Proposal B — replace entry lines 24-25:

```
The five event families below are frozen from the driver source; the live log
also carries line families the probe does not model (`tick=N` heartbeats,
`shokunin-watchdog.sh:452`, 70 of 1729 non-blank lines; `steer`, 15;
`watchdog tick …`, 1; `lane-round-failed <lane> round=N :: <reason>`, 35). The
grammar below covers every variant of those five families observed in the live
log on this host (2026-09-28..2026-10-27), not every line shape.
```

Proposal C — replace entry lines 41-44:

```
* A ts-first line that the event regex does not match is an `other_line`:
  counted, no examples kept, never malformed. That bucket mixes driver prose
  (`steer`, `watchdog tick`) with event-shaped lines the grammar does not know:
  an unknown event name (`lane-round-failed`), a lane character outside
  `[A-Za-z0-9_-]`, a doubled space, or a missing/bad `round=` all land there. A
  non-ts first token, or an event line whose rest is unrecognized, is malformed
  — counted with at most 3 examples, never silent; but a malformed event line
  still creates its lane row and adds its round to `rounds_seen`.
```

Proposal D — replace entry lines 51-52:

```
(receipt `evidence/driver-liveness-live.txt`). The receipt is committed; its
input is not — `.ufo/watchdog.log` is gitignored in the fleet repo
(`.gitignore:10`) and the last commit that touched it untracked it (`7930399e`),
so the reading is not replayable from the repository. Re-running on the live log
reproduces the counts only for the same bytes: one appended `complete` line since
the receipt moved completes 570 → 571 and non-blank lines 1728 → 1729.
```

Proposal E — add to the Limits section:

```
* `other_lines` is not a prose-only bucket: it absorbs event-shaped lines the
  grammar does not model (`lane-round-failed` 35, `tick=N` 70 in the frozen
  reading). A lane event can therefore be invisible as an event and visible only
  as an aggregate count.
* `unclosed` pairs a launch against a close of the same round: a `complete`
  closes the `(round, attempt)` it names (falling back to a bare launch of that
  round), a `wrap` closes the round, and a `lane-dead-no-report` clears every
  open launch of its round. It is a pairing count, not a failure claim.
* The no-symlink guarantee is scoped to state entries; the log path itself is
  opened normally and a symlinked log would be followed.
* `line count` is the non-blank line count.
* A malformed event line still creates a lane row (with `launches=0`) and adds
  its round to `rounds_seen`.
```

## Findings

1. **HIGH** — `corpus/knowledge/driver-liveness-r56.md:18,41-42` describe `other_lines` as
   "ts-first driver prose" and say such a line is "never a lane event". In the frozen reading,
   121 other_lines = 70 `tick=N` (written by `shokunin-watchdog.sh:452`, one of the two S544
   writers, and absent from the frozen grammar), 35 `lane-round-failed <lane> round=N :: …`
   (event-shaped, 35 in the log), 15 `steer`, 1 `watchdog tick`. Three event-shaped inputs I
   constructed were each classified other_line and none malformed: double space
   (`launch  mori round=1 pgid=1`), dotted lane (`launch game.dev round=1 pgid=1`),
   unknown event (`lane-round-failed mori round=1 :: x`); the tool printed
   `malformed=1 other=3` for that four-line log, the single malformed being the
   `weird=2` rest. Code: `tools/mori-driver-liveness.py:100-101`.
2. **MED** — `corpus/knowledge/driver-liveness-r56.md:3,24` ("the driver scripts that write the
   log", "Two writers share one log"). The log writer set is larger: `steer` and
   `watchdog tick` writers are not in `scripts/` (grep over `scripts/` and
   `scripts/hyaku/*.py,*.sh` found none), and `lane-round-failed` appears in the fleet tree
   only as a reader token at `mori-shokunin/tools/mori-census.sh:1999`. The claim is strongest
   as "two writers for five event families", not "two writers for the log".
3. **MED** — `corpus/knowledge/driver-liveness-r56.md:25,51-52` and the tool docstring
   `tools/mori-driver-liveness.py:13` call `.ufo/watchdog.log` "the committed live log" and say
   re-running "reproduces it modulo ages". Verified: `.gitignore:10` is
   `.ufo/watchdog.log`; `git check-ignore -v .ufo/watchdog.log` → `.gitignore:10`;
   `git ls-files .ufo/watchdog.log` prints nothing; commit `7930399e` is the one that
   untracked it. The reading is not replayable from the repo. Counts drift too: the log is now
   1729 non-blank lines with completes 571 (receipt: 1728 / 570), the added line being
   `2026-10-27T10:56:54-03:00 complete kake round=63; hyaku-inline attempt=1`.
4. **MED** — `corpus/knowledge/driver-liveness-r56.md:27` gives the launch optional-field order
   as "driver=… attempt=…, optional slot=…" while the code order is
   `driver`, `slot`, `attempt`, `mission` (`tools/mori-driver-liveness.py:56-58`). Input
   `launch kagi round=7 pgid=999 attempt=3 slot=2` is malformed (it appeared in the examples
   list, `malformed` count 1). A writer emitting the entry's order would be counted malformed.
5. **MED** — the committed S544 extract does not carry the entry's wrap and launch-fail anchors
   (`shokunin-watchdog.sh:398`, `241-249`) nor the `slot=`/`mission=`/`runId=`/`pid=` forms,
   so those S544 attributions are not byte-backed by the copy; and the entry's two line-anchored
   quotes are template renderings, not substrings (table above). Live writer source does contain
   241-249 and 398 (read via `sed`), so the facts are true of the source, not of the extract.
6. **MED** — malformed event lines leak into per-lane rows: `parse_log` creates the lane row and
   records its round before validating `rest` (`tools/mori-driver-liveness.py:109-113` vs
   `:123-124`). Input `launch ghost round=5 pgid=1 attempt=2 slot=3` plus a valid `real` launch
   gave `malformed=1` and a `ghost` row with `launches=0, rounds_seen=1`. The entry's per-lane
   field list (`:15-17`) omits `rounds_seen` and does not say a lane can appear with zero
   launches.
7. **LOW** — `corpus/knowledge/driver-liveness-r56.md:16-17` glosses `unclosed` as "launches with
   no same-round close", dropping attempt keying and that a `lane-dead-no-report` clears the
   round (`tools/mori-driver-liveness.py:116-121,157`).
8. **LOW** — `corpus/knowledge/driver-liveness-r56.md:58-59` says the probe "never follows
   symlinks". State entries are not followed (`:188-189`), but the log path is checked with
   `os.path.isfile` and opened (`:204,210`), both of which follow a symlinked log.
9. **LOW** — tool docstring `tools/mori-driver-liveness.py:22` says `respawning` is "(120 in log)";
   120 is the count of the `respawning` substring including the 22 `wrap … NOT respawning`
   lines. Actual `complete …; respawning` lines: 98.
10. **LOW** — `corpus/knowledge/driver-liveness-r56.md:39` attributes the ` complete` wrap form to
    `shokunin-watchdog.sh:398`, which emits ` landed` only; the log's 22 wraps are all
    ` complete; NOT respawning (fleet-wrap)` and zero ` landed` wraps exist, so the
    ` complete` form's writer is not identified anywhere in the citations.
11. **LOW** — `corpus/knowledge/driver-liveness-r56.md:10-11` ("census watchdog surface fires
    `WATCHDOG_ABSENT` every round") is inherited from `corpus/README.md:345` and not re-observed
    here: `evidence/census-start.txt` carries 0 `WATCHDOG_ABSENT` occurrences. Stated as
    current fact without a receipt.
12. **LOW** — `corpus/knowledge/driver-liveness-r56.md:18` calls the log-shape counter "line
    count"; it is the non-blank count (`:92-94`, blank lines skipped), and the entry's
    `mtime_age_s`/`newest_ts`/`examples` fields are unmentioned.

## UNVERIFIED / out of scope

- Whether `WATCHDOG_ABSENT` actually fires each round (no census receipt in round 56 shows it);
  inherited claim only.
- Identity of the `steer`, `watchdog tick` and `lane-round-failed` writers (not present in the
  fleet tree read; no fleet-wide binary search performed).
- The C1 counter result itself (no counter run by this seat — other seats own it); the entry's
  presence/name row checks are the counter's, not this seat's.
- Tier defensibility of S544 and the vote-binding entry: other seats' scope.
- No product, tool, fixture, contract, counter or pin was modified; the two proposed source
  corrections in Findings 5 and 9 carry re-pin consequences and are the L1's decision.

## Findings

| # | severity | concern |
|---|---|---|
| 1 | HIGH | `corpus/knowledge/driver-liveness-r56.md:18,41-42` — `other_lines` described as driver prose; 35 event-shaped `lane-round-failed` lines and 70 `tick=N` lines land there; code `tools/mori-driver-liveness.py:100-101` |
| 2 | MED | `corpus/knowledge/driver-liveness-r56.md:3,24` — "two writers share one log" understates the writer set |
| 3 | MED | `corpus/knowledge/driver-liveness-r56.md:25,51-52`; `tools/mori-driver-liveness.py:13` — "committed live log" is false (`.gitignore:10`) and re-running does not reproduce counts (570→571) |
| 4 | MED | `corpus/knowledge/driver-liveness-r56.md:27` — launch optional-field order wrong vs `tools/mori-driver-liveness.py:56-58` |
| 5 | MED | `corpus/evidence/sources-r56/watchdog-log-grammar.txt` — lacks the entry's wrap (398) and launch-fail (241-249) anchors and the log-only variant anchors |
| 6 | MED | `tools/mori-driver-liveness.py:109-113` — malformed event lines create lane rows/rounds; undocumented in the entry |
| 7 | LOW | `corpus/knowledge/driver-liveness-r56.md:16-17` — `unclosed` gloss drops attempt keying and dead/wrap closes |
| 8 | LOW | `corpus/knowledge/driver-liveness-r56.md:58-59` — "never follows symlinks" over-scoped to the log path |
| 9 | LOW | `tools/mori-driver-liveness.py:22` — "(120 in log)" counts the `NOT respawning` substring; 98 real respawn completes |
| 10 | LOW | `corpus/knowledge/driver-liveness-r56.md:39` — ` complete` wrap form attributed to a writer that emits ` landed` only; 0 landed wraps in the log |
| 11 | LOW | `corpus/knowledge/driver-liveness-r56.md:10-11` — `WATCHDOG_ABSENT` every round inherited, not evidenced this round |
| 12 | LOW | `corpus/knowledge/driver-liveness-r56.md:15-18` — `rounds_seen`/`mtime_age_s`/`newest_ts` unlisted; "line count" is non-blank count |
