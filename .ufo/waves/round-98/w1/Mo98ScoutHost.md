# Mo98ScoutHost: read-only host reconnaissance for C1 (round 98, attempt 1, wave w1)

Scope: read-only. No sysctl, service, sudo, or namespace-creation action was taken. No repo file was written. Scratch: /fast/scratch/hyaku/mori-r98/Mo98ScoutHost (removed before yield).

## (1) Journal COMMAND recapture, 05:14:00 to 05:43:00

Command: `journalctl --since '2026-11-05 05:14:00' --until '2026-11-05 05:43:00' -o short-iso --no-pager | grep -F ' COMMAND='`

```
$ wc -l jc.txt journal-incident-r98.txt
   276 jc.txt
   276 .ufo/waves/round-98/evidence/journal-incident-r98.txt
$ sha256sum jc.txt journal-incident-r98.txt
978504134c53a4a4b404bf5175b51aa31f5afd27ad62cd517e4a2fbc2cd79738  jc.txt
978504134c53a4a4b404bf5175b51aa31f5afd27ad62cd517e4a2fbc2cd79738  .ufo/waves/round-98/evidence/journal-incident-r98.txt
$ diff -u journal-incident-r98.txt jc.txt && echo DIFF_EMPTY_IDENTICAL
DIFF_EMPTY_IDENTICAL
```

Result: the recapture is byte-identical to the frozen incident capture (same sha256, 276 lines).

## (2) Journal search for ENOSPC / namespace failure text, 05:00:00 to 06:00:00

```
$ journalctl --since '2026-11-05 05:00:00' --until '2026-11-05 06:00:00' -o short-iso --no-pager | grep -i -E 'ENOSPC|No space left|namespace'
(6 lines; all are sudo COMMAND= lines, none is a bwrap/unshare error)
2026-11-05T05:14:52-03:00 ... COMMAND=/usr/bin/sh -c 'echo 0 > /proc/sys/user/max_user_namespaces'
2026-11-05T05:14:54-03:00 ... COMMAND=/usr/bin/sysctl -w user.max_user_namespaces=10000
2026-11-05T05:16:04-03:00 ... COMMAND=/usr/bin/sysctl user.max_user_namespaces=15638
2026-11-05T05:16:04-03:00 ... COMMAND=/usr/bin/sh -c 'echo 15638 > /proc/sys/user/max_user_namespaces'
2026-11-05T05:22:02-03:00 ... COMMAND=/usr/bin/sh -c 'echo 0 > /proc/sys/user/max_user_namespaces'
2026-11-05T05:42:18-03:00 ... COMMAND=/usr/bin/sysctl -w user.max_user_namespaces=122865
$ journalctl ... | grep -i -E 'bwrap|unshare' | grep -i -v ' COMMAND='
(no output)
$ journalctl ... -p err..alert   (window error-priority lines: systemd-coredump "g++ ... terminated abnormally", 05:16:49-05:16:50, unrelated)
```

Finding: the journal contains NO ENOSPC or "No space left" text, and no bwrap or unshare error line, in the window. The bwrap ENOSPC failure the incident describes is not logged to the journal; it lives in the sandbox's stderr, which this scan cannot see. The only in-journal evidence is the sysctl write sequence. The sequence is consistent with the incident: limit set to 0 at 05:14:52 and again at 05:22:02, restored to 15638 at 05:16:04 and to 122865 at 05:42:18. I did not confirm the bwrap ENOSPC message text itself; that is `[INFERENCE]` from the incident description only.

## (3) Tool runs versus lsns

```
$ python3 tools/mori-userns-runway.py       (run 1, exit 0)
USERNS_RUNWAY limit=122865 used_lb=6 pids=3673 unreadable=3409 runway=122859 low=32 state=ok
$ python3 tools/mori-userns-runway.py       (run 2, exit 0)
USERNS_RUNWAY limit=122865 used_lb=6 pids=3671 unreadable=3409 runway=122859 low=32 state=ok
$ python3 tools/mori-userns-runway.py       (run 3, exit 0)
USERNS_RUNWAY limit=122865 used_lb=6 pids=3671 unreadable=3409 runway=122859 low=32 state=ok

$ id -un; id -u
vgpnk
1000
$ lsns -t user -n -o NS,PID,USER
4026531837    1505 vgpnk      <- initial user namespace (excluded by both)
4026533674    2697 vgpnk
4026533741   12188 vgpnk
4026533750    2571 vgpnk
4026533813   91310 vgpnk
4026533826 2424163 vgpnk
4026533936 3412520 vgpnk
```

Comparison: lsns shows 7 user namespaces. One is the initial namespace (4026531837), which both sides exclude. That leaves 6 non-initial namespaces, all owned by uid vgpnk. The tool's `used_lb=6` matches exactly.

Difference explanation: there is none in count. The `pids` figure varies between runs (3671 to 3673) because processes come and go, but the distinct-namespace count is stable at 6. `unreadable=3409` are processes whose `ns/user` link the uid cannot read (other users' processes); lsns is bounded by the same /proc visibility, so both count from the same readable set. Caveat: `used_lb` is a lower bound by name. Namespaces held only by unreadable processes are not counted, so the true usage can be higher. This is a visibility limit, not a disagreement.

## (4) Host sysctls (read only)

```
$ cat /proc/sys/user/max_user_namespaces /proc/sys/kernel/threads-max
122865
245730
```

`max_user_namespaces` is 122865, which equals the last write (`sysctl -w user.max_user_namespaces=122865` at 05:42:18). The tool's runway is 122859 (limit minus 6), state ok.

## Unrun checks

- The tool's `--scan` journal mode was not run; it was outside this seat's assignment. Its sysctl write parsing was not exercised by this seat.
- `--selftest` not run (not in assignment).
- No check of the bwrap ENOSPC stderr text (not in any journal this seat can read).

VERDICT C1 holds: `used_lb=6` equals lsns's distinct non-initial user-namespace count (6 = 6), and the tool exits 0 on 3 of 3 runs. Scope limit: the incident's ENOSPC text is absent from the journal, so the journal confirms only the sysctl writes, not the bwrap failure.
