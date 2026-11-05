# Mo99ExecTrial — end-to-end journal trial of the landed write scan (round 99, wave w1)

Seat: Mo99ExecTrial (executor, leaf). Date: 2026-11-05, host time zone -03 (America/Sao_Paulo).
Task: run the landed tool `tools/mori-userns-runway.py --journal-live --since S --until U` on this host's real
journal over the 2026-11-05 incident window (05:14–05:43 -03) and full days 2026-11-03/04/05 (to now); record
rc/summary/unparsed per run; classify any unparsed sudo lines; count sudo corpus shapes over the 3 days; compare
the entering tool (`git show 73308ff6…:tools/mori-userns-runway.py`) on the same windows and attribute every
difference to the correct tool by reading the lines. Detection/report only; no sudo run by this seat; no host or
repo mutation; scratch `/fast/scratch/hyaku/mori-r99/Mo99ExecTrial` removed before finishing.

## 0. Bytes under trial

- landed: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 5013f0be8ac9e7fce3c08b680e43cf9cbd49620d:tools/mori-userns-runway.py`
  (lane HEAD = 5013f0be, so also the working-tree bytes), sha256 `4ef3108f171dc5fa0b42c8dc1cf4f374cb223ab0bb9411c1e992e255e46abc0b`, 647 lines.
- entering: `git -C … show 73308ff6e5c933f53498e9501ef95917b0ef7171:tools/mori-userns-runway.py`,
  sha256 `5ab134ee036f83851eb98a9027db699a5800130c5c13598cb37aeb2abe452db2`, 342 lines.
- `python3 landed.py --selftest` → `MORI_USERNS_RUNWAY_SELFTEST: PASS (19 cases)`, rc 0 (host TMPDIR set to scratch).
- Journal access: uid vgpnk (wheel); `journalctl` reads the system journal (829 sudo lines visible in the incident window).

## 1. Trial runs (all `--journal-live --since/--until`, journalctl `-o short-iso` internally)

Run wall-clock: 2026-11-05 19:11–19:15 -03. Day-5 `--until now` taken at 19:14:52.

| window (local -03) | journal lines | sudo COMMAND= | tool | rc | summary | unparsed |
|---|---|---|---|---|---|---|
| incident 2026-11-05 05:14:00–05:43:00 | 1138 | 276 | landed | 1 | `SYSCTL_WRITES n=6 keys=1 userns_zero=2` | 0 |
| incident (same) | | | entering | 1 | `SYSCTL_WRITES n=6 keys=1 userns_zero=2` | n/a |
| day 2026-11-03 00:00–24:00 | 22829 | 477 | landed | 0 | `SYSCTL_WRITES n=0 keys=0 userns_zero=0` | 0 |
| day 2026-11-03 (same) | | | entering | 0 | identical | n/a |
| day 2026-11-04 00:00–24:00 | 60027 | 20 | landed | 0 | `SYSCTL_WRITES n=0 keys=0 userns_zero=0` | 0 |
| day 2026-11-04 (same) | | | entering | 0 | identical | n/a |
| day 2026-11-05 00:00–19:14:52 | 48641 | 8018 | landed | 1 | `SYSCTL_WRITES n=6 keys=1 userns_zero=2` | 0 |
| day 2026-11-05 (same) | | | entering | 1 | identical | n/a |

No window scored `SYSCTL_WRITES_SETUP unparsed=U` with U>0: **no offending sudo lines to extract**; every window the
landed tool read was fully parseable (rc 2 never fired on live journal text). Determinism cross-check: running both
tools with `--journal` on the byte-equal `journalctl -o short-iso` captures of the same windows reproduced the live
outputs exactly (`diff` rc 0, 8/8).

## 2. Counts over the 3 days (2026-11-03 00:00 → 2026-11-05 19:14:52 -03)

- sudo lines (`sudo[`): 25555; lines carrying ` COMMAND=`: 8515.
- `(command continued)` lines: **4**, belonging to 2 commands:
  - pid 1749648, 2026-11-05T05:16:59-03:00 — 1 first part + 1 continuation; a `sh -c 'cat > …/runns.sh <<\'EOF\'#012…'`
    heredoc-writing script (writes a scratch script + runs bwrap/python3; **no kernel-tunable write**). First 160 chars:
    `2026-11-05T05:16:59-03:00 plazir27 sudo[1749648]:    vgpnk : PWD=/home/vgpnk/Projects/shokunin ; USER=root ; COMMAND=/usr/bin/sh -c 'cat > /fast/scratch/hyaku/k`
  - pid 4036579, 2026-11-05T19:14:33-03:00 — 1 first part + 3 continuations; seat Mo99ExecSudo's `/usr/bin/true` with
    69 padded args (landed tool joined all 4 lines by pid and stayed unparsed=0 in my day-5 window, which includes 19:14:33).
- ` ; EXIT=` lines: **0**; ` ; SIGNAL=` lines: **0** — sudo exit/signal events are not present on this host in the window,
  so the exit-event skip (S633/S635) is exercised by fixtures only (see §6 unrun checks).
- sudo `COMMAND=` lines containing sudo escapes: `\'` 25 (incident window; all 26 in day-5, +1 non-COMMAND line → 27
  unrestricted over 3 days) and `#0nn` 19 (incident; 21 in day-5; 22 unrestricted). Shapes: kengaku-r89 seat's
  `bwrap … python3 -c '#012import os#012os.chdir(\'/app\')…'` probes (05:17:36–05:20:42, inside the incident window as
  well) and Mo99ExecSudo's deliberate `'a b' it\'s x#012y` / `q"w back\\slash tab#011here` probes (19:14:33). None of
  them carries a kernel-tunable write; landed tool tokenizes all of them with unparsed=0, and entering's whitespace
  fallback happens to reach the same (no-write) answer on them.
- `sysctl` inside sudo `COMMAND=`: **5 lines over 3 days, all in the incident window**: 2 reads (`COMMAND=/usr/bin/sysctl -a`,
  pids 1225103 @05:14:39 and 1279792 @05:14:48 — correctly reported as no write by both tools) and the 3 `sysctl` writes
  below. Note one write uses implicit `-w` (`COMMAND=/usr/bin/sysctl user.max_user_namespaces=15638`, no flag) — procps
  sysctl writes on bare `key=value`; both tools report it.

## 3. Kernel-tunable writes reported (landed tool; entering identical on these windows)

All 6 over the 3 days, single key `user.max_user_namespaces`, all inside the incident window:

| # | ts (-03) | pid | value | via | source line (≤160 chars) |
|---|---|---|---|---|---|
| 1 | 2026-11-05T05:14:52 | 1302030 | 0 | sh-echo | `… ; COMMAND=/usr/bin/sh -c 'echo 0 > /proc/sys/user/max_user_namespaces'` |
| 2 | 2026-11-05T05:14:54 | 1316549 | 10000 | sysctl | `… ; COMMAND=/usr/bin/sysctl -w user.max_user_namespaces=10000` |
| 3 | 2026-11-05T05:16:04 | 1580806 | 15638 | sysctl | `… ; COMMAND=/usr/bin/sysctl user.max_user_namespaces=15638` |
| 4 | 2026-11-05T05:16:04 | 1580838 | 15638 | sh-echo | `… ; COMMAND=/usr/bin/sh -c 'echo 15638 > /proc/sys/user/max_user_namespaces'` |
| 5 | 2026-11-05T05:22:02 | 2322929 | 0 | sh-echo | `… ; COMMAND=/usr/bin/sh -c 'echo 0 > /proc/sys/user/max_user_namespaces'` |
| 6 | 2026-11-05T05:42:18 | 2548588 | 122865 | sysctl | `… ; COMMAND=/usr/bin/sysctl -w user.max_user_namespaces=122865` |

`userns_zero=2` (writes 1 and 5) matches the incident narrative (limit zeroed twice; restored to 10000/15638 then 122865).

## 4. Landed vs entering on the same windows — every difference

- On all four `--journal-live` windows the two tools' outputs are **byte-identical** (`diff` rc 0 in 4/4; §1 table).
  Reading the in-window lines explains the tie: the only grammar shapes present (heredoc+continuation pair, `\'`,
  `#012`) sit in commands with no kernel-tunable write, and `--journal-live` passes `-o short-iso` to both tools, so
  entering's timestamp weakness never engages in live mode. Both tools are right on these windows.
- Real-data divergence 1 — `journalctl -o short` (default format) text of the same incident window (1138 lines):
  - entering: rc 0, `SYSCTL_WRITES n=0 keys=0 userns_zero=0` — the six real writes are read as "no write" because the
    `Nov 05 05:14:52` timestamp shape is unrecognized. **Entering is wrong.**
  - landed: rc 1, `SYSCTL_WRITES n=6 keys=1 userns_zero=2` — **landed is right**; the six lines quoted in §3 carry the
    writes at those exact timestamps/pids.
- Real-data divergence 2 — the truncated r98 capture `.ufo/waves/round-98/evidence/journal-incident-r98.txt`
  (276 lines, all `COMMAND=`, 0 continuation lines — the filter dropped pid 1749648's continuation):
  - landed: rc 2 with the same 6 writes plus `SYSCTL_WRITES_SETUP unparsed=1` — **right**: the capture's pid 1749648
    line ends mid-quote (`…--symlink usr/lib` with the `'` still open, tail verified byte-exact); its continuation is
    absent, so the command cannot be read completely and the scan fails closed. Classification: **truncated-capture
    edge**, exactly as the frozen contract discloses — not an unknown sudo line shape, not a tool defect.
  - entering: rc 1, no unparsed, silently accepts the truncated capture (whitespace-split fallback). Wrong-by-design
    for an untrustworthy input; in this instance it happens to report the same 6 writes.
- Net: **no reported write differs between the tools on any live window**; the landed tool's advantages on real host
  bytes are (a) correct reads under `journalctl`'s default `-o short`, and (b) fail-closed honesty on truncated input.

## 5. Cross-check against the frozen claim inputs

- `diff <(git-show-pinned capture .ufo/waves/round-99/evidence/journal-incident-r99.txt) <(journalctl -o short-iso
  --since '2026-11-05 05:14:00' --until '2026-11-05 05:43:00' | grep 'sudo\[')` → rc 0: the pinned full capture is
  **byte-identical** to what this host's journal yields for the same window today (i.e. it was not filtered; it
  contains the 277 command-bearing lines incl. the continuation).
- `landed.py --journal .ufo/waves/round-99/evidence/journal-incident-r99.txt` → rc 1,
  `SYSCTL_WRITES n=6 keys=1 userns_zero=2`, no setup line: matches the frozen claim's scoring of the full capture and
  my live runs line-for-line.

## 6. Unrun checks (named, not inferred)

- No `sudo`/`sysctl` execution by this seat (task forbids; not needed for read-only journal scans).
- ` ; EXIT=` / ` ; SIGNAL=` skip: not exercised on real data — the host journal contains **zero** such lines in the
  3-day window; covered by the frozen counter battery/fixtures only.
- `sysctl -r/--pattern` skip, `env`/`NAME=` prefixes, `printf`, `tee`, `-p FILE`/`--system` load forms: none of these
  appear in the 3-day real sudo corpus; untested against this host's live journal (fixture coverage per counter P1).
- Runway (`--proc`/fake-/proc) side: not trialed — task scope was the journal windows.
- Counters (`count-c1.py`/`count-c2.py`) and gates: not run by this seat (parent owns the post-integration gate).
- Boundary caveat: day-5 window end was taken at 19:14:52; events after that instant (if any) are outside this trial.

## 7. Receipts (verbatim)

Landed tool, incident window (`--journal-live --since '2026-11-05 05:14:00' --until '2026-11-05 05:43:00'`), rc 1:
```
SYSCTL_WRITE ts=2026-11-05T05:14:52-03:00 pid=1302030 key=user.max_user_namespaces value=0 via=sh-echo
SYSCTL_WRITE ts=2026-11-05T05:14:54-03:00 pid=1316549 key=user.max_user_namespaces value=10000 via=sysctl
SYSCTL_WRITE ts=2026-11-05T05:16:04-03:00 pid=1580806 key=user.max_user_namespaces value=15638 via=sysctl
SYSCTL_WRITE ts=2026-11-05T05:16:04-03:00 pid=1580838 key=user.max_user_namespaces value=15638 via=sh-echo
SYSCTL_WRITE ts=2026-11-05T05:22:02-03:00 pid=2322929 key=user.max_user_namespaces value=0 via=sh-echo
SYSCTL_WRITE ts=2026-11-05T05:42:18-03:00 pid=2548588 key=user.max_user_namespaces value=122865 via=sysctl
SYSCTL_WRITES n=6 keys=1 userns_zero=2
```
Entering tool, same window, rc 1: the same 7 lines byte-identical (`diff` rc 0). Landed/entering on day 3 and day 4:
`SYSCTL_WRITES n=0 keys=0 userns_zero=0`, rc 0, identical. Landed/entering on day 5 (00:00–19:14:52): the same 7
lines as the incident window, rc 1, identical.
Self-test: `MORI_USERNS_RUNWAY_SELFTEST: PASS (19 cases)`, rc 0.
`-o short` same window: landed rc 1 `n=6 keys=1 userns_zero=2`; entering rc 0 `n=0 keys=0 userns_zero=0`.
r98 truncated capture: landed rc 2 `n=6 … userns_zero=2` + `SYSCTL_WRITES_SETUP unparsed=1`; entering rc 1 `n=6 … userns_zero=2`.
Pinned full capture vs live extract: `diff` rc 0; landed on pinned capture rc 1 `n=6 keys=1 userns_zero=2`.

No tool installs/upgrades were needed or made (operator authorization unused). Scratch removed.
