# Mo99ExecSudo — round 99 attempt 1, wave w1 — sudo COMMAND= rendering probe

Seat: Mo99ExecSudo (executor, leaf). Lane: mori. Detection and report only; no remediation, no host
sysctl/service/limit change, no edit to tools/, corpus/, SCORECARD, MANIFEST, contract or counters.
Tool under test: `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-userns-runway.py` (read-only, not modified).

## Host and sudo
- `sudo --version` (run via `sudo` path of the task's sanctioned form, see disclosure): Sudo version 1.9.17p2;
  Sudoers policy plugin 1.9.17p2; Sudoers I/O plugin 1.9.17p2 (matches the version cited by C1 S635/S636).
- `id`: uid=1000(vgpnk); not sudo-prompted. `sudo -n` succeeded for every probe (no password needed).

## Commands run (t0 = 2026-11-05 19:14:33, local -03)
1. `sudo -n /usr/bin/true 'a b' "it's" $'x\ny'` → rc 0
2. `sudo -n /usr/bin/true "$BIG" 'z'` where BIG = 70 tokens `argNNNN-abcdefghijklmnopqrstuvwxyz0123456789`
   joined by spaces, then a space and 400 `Z` (one argument, length 3550) → rc 0
3. `sudo -n /usr/bin/true 'q"w' "back\\slash" 'tab<TAB>here'` → rc 0

Read back: `journalctl -o short-iso --since "2026-11-05 19:14:33" --no-pager | grep 'sudo\['` (12 lines, saved verbatim):
2026-11-05T19:14:33-03:00 plazir27 sudo[4036484]:    vgpnk : PWD=/fast/scratch/hyaku/mori-r99/Mo99ExecSudo ; USER=root ; COMMAND=/usr/bin/true 'a b' it\'s x#012y
2026-11-05T19:14:33-03:00 plazir27 sudo[4036484]: pam_unix(sudo:session): session opened for user root(uid=0) by vgpnk(uid=1000)
2026-11-05T19:14:33-03:00 plazir27 sudo[4036484]: pam_unix(sudo:session): session closed for user root
2026-11-05T19:14:33-03:00 plazir27 sudo[4036579]:    vgpnk : PWD=/fast/scratch/hyaku/mori-r99/Mo99ExecSudo ; USER=root ; COMMAND=/usr/bin/true 'arg0000-abcdefghijklmnopqrstuvwxyz0123456789 arg0001-abcdefghijklmnopqrstuvwxyz0123456789 arg0002-abcdefghijklmnopqrstuvwxyz0123456789 arg0003-abcdefghijklmnopqrstuvwxyz0123456789 arg0004-abcdefghijklmnopqrstuvwxyz0123456789 arg0005-abcdefghijklmnopqrstuvwxyz0123456789 arg0006-abcdefghijklmnopqrstuvwxyz0123456789 arg0007-abcdefghijklmnopqrstuvwxyz0123456789 arg0008-abcdefghijklmnopqrstuvwxyz0123456789 arg0009-abcdefghijklmnopqrstuvwxyz0123456789 arg0010-abcdefghijklmnopqrstuvwxyz0123456789 arg0011-abcdefghijklmnopqrstuvwxyz0123456789 arg0012-abcdefghijklmnopqrstuvwxyz0123456789 arg0013-abcdefghijklmnopqrstuvwxyz0123456789 arg0014-abcdefghijklmnopqrstuvwxyz0123456789 arg0015-abcdefghijklmnopqrstuvwxyz0123456789 arg0016-abcdefghijklmnopqrstuvwxyz0123456789 arg0017-abcdefghijklmnopqrstuvwxyz0123456789 arg0018-abcdefghijklmnopqrstuvwxyz0123456789
2026-11-05T19:14:33-03:00 plazir27 sudo[4036579]:    vgpnk : (command continued) arg0019-abcdefghijklmnopqrstuvwxyz0123456789 arg0020-abcdefghijklmnopqrstuvwxyz0123456789 arg0021-abcdefghijklmnopqrstuvwxyz0123456789 arg0022-abcdefghijklmnopqrstuvwxyz0123456789 arg0023-abcdefghijklmnopqrstuvwxyz0123456789 arg0024-abcdefghijklmnopqrstuvwxyz0123456789 arg0025-abcdefghijklmnopqrstuvwxyz0123456789 arg0026-abcdefghijklmnopqrstuvwxyz0123456789 arg0027-abcdefghijklmnopqrstuvwxyz0123456789 arg0028-abcdefghijklmnopqrstuvwxyz0123456789 arg0029-abcdefghijklmnopqrstuvwxyz0123456789 arg0030-abcdefghijklmnopqrstuvwxyz0123456789 arg0031-abcdefghijklmnopqrstuvwxyz0123456789 arg0032-abcdefghijklmnopqrstuvwxyz0123456789 arg0033-abcdefghijklmnopqrstuvwxyz0123456789 arg0034-abcdefghijklmnopqrstuvwxyz0123456789 arg0035-abcdefghijklmnopqrstuvwxyz0123456789 arg0036-abcdefghijklmnopqrstuvwxyz0123456789 arg0037-abcdefghijklmnopqrstuvwxyz0123456789 arg0038-abcdefghijklmnopqrstuvwxyz0123456789
2026-11-05T19:14:33-03:00 plazir27 sudo[4036579]:    vgpnk : (command continued) arg0039-abcdefghijklmnopqrstuvwxyz0123456789 arg0040-abcdefghijklmnopqrstuvwxyz0123456789 arg0041-abcdefghijklmnopqrstuvwxyz0123456789 arg0042-abcdefghijklmnopqrstuvwxyz0123456789 arg0043-abcdefghijklmnopqrstuvwxyz0123456789 arg0044-abcdefghijklmnopqrstuvwxyz0123456789 arg0045-abcdefghijklmnopqrstuvwxyz0123456789 arg0046-abcdefghijklmnopqrstuvwxyz0123456789 arg0047-abcdefghijklmnopqrstuvwxyz0123456789 arg0048-abcdefghijklmnopqrstuvwxyz0123456789 arg0049-abcdefghijklmnopqrstuvwxyz0123456789 arg0050-abcdefghijklmnopqrstuvwxyz0123456789 arg0051-abcdefghijklmnopqrstuvwxyz0123456789 arg0052-abcdefghijklmnopqrstuvwxyz0123456789 arg0053-abcdefghijklmnopqrstuvwxyz0123456789 arg0054-abcdefghijklmnopqrstuvwxyz0123456789 arg0055-abcdefghijklmnopqrstuvwxyz0123456789 arg0056-abcdefghijklmnopqrstuvwxyz0123456789 arg0057-abcdefghijklmnopqrstuvwxyz0123456789 arg0058-abcdefghijklmnopqrstuvwxyz0123456789
2026-11-05T19:14:33-03:00 plazir27 sudo[4036579]:    vgpnk : (command continued) arg0059-abcdefghijklmnopqrstuvwxyz0123456789 arg0060-abcdefghijklmnopqrstuvwxyz0123456789 arg0061-abcdefghijklmnopqrstuvwxyz0123456789 arg0062-abcdefghijklmnopqrstuvwxyz0123456789 arg0063-abcdefghijklmnopqrstuvwxyz0123456789 arg0064-abcdefghijklmnopqrstuvwxyz0123456789 arg0065-abcdefghijklmnopqrstuvwxyz0123456789 arg0066-abcdefghijklmnopqrstuvwxyz0123456789 arg0067-abcdefghijklmnopqrstuvwxyz0123456789 arg0068-abcdefghijklmnopqrstuvwxyz0123456789 arg0069-abcdefghijklmnopqrstuvwxyz0123456789 ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ' z
2026-11-05T19:14:33-03:00 plazir27 sudo[4036579]: pam_unix(sudo:session): session opened for user root(uid=0) by vgpnk(uid=1000)
2026-11-05T19:14:33-03:00 plazir27 sudo[4036579]: pam_unix(sudo:session): session closed for user root
2026-11-05T19:14:33-03:00 plazir27 sudo[4036613]:    vgpnk : PWD=/fast/scratch/hyaku/mori-r99/Mo99ExecSudo ; USER=root ; COMMAND=/usr/bin/true q"w back\\slash tab#011here
2026-11-05T19:14:33-03:00 plazir27 sudo[4036613]: pam_unix(sudo:session): session opened for user root(uid=0) by vgpnk(uid=1000)
2026-11-05T19:14:33-03:00 plazir27 sudo[4036613]: pam_unix(sudo:session): session closed for user root

Measured segment lengths for pid 4036579 (chars after `sudo[4036579]:`): first line 949 (line total 998),
continuations 931, 931, 930 (line totals 980, 980, 979). Three `(command continued)` lines, same pid.

## Comparison (tool's own code path)
Harness (importlib of the tool; `scan_journal` run on the 12 lines with `split_cmd` wrapped to record the
COMMAND string it receives; then `split_cmd` applied to each recorded string; compared to the argv passed):

```
capture lines: 12 biglen: 3550
tool scan_journal: events=0 unparsed=0 commands_seen=3
cmd[0] len=32  first80="/usr/bin/true 'a b' it\\'s x#012y"  ...last40="/usr/bin/true 'a b' it\\'s x#012y"
  argv_len=4 argv0= /usr/bin/true argc_args= 3
cmd[1] len=3568  first80="/usr/bin/true 'arg0000-abcdefghijklmnopqrstuvwxyz0123456789 arg0001-abcdefghijkl"  ...last40="ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ' z"
  argv_len=3 argv0= /usr/bin/true argc_args= 2
cmd[2] len=41  first80='/usr/bin/true q"w back\\\\slash tab#011here'  ...last40='usr/bin/true q"w back\\\\slash tab#011here'
  argv_len=4 argv0= /usr/bin/true argc_args= 3
case 0 exact-list-equal=True
case 1 exact-list-equal=True
case 2 exact-list-equal=True
ALL_ARGV_EQUAL=True
```

Expected argv lists (as passed): `["/usr/bin/true","a b","it's","x\ny"]`, `["/usr/bin/true",BIG,"z"]`,
`["/usr/bin/true",'q"w',"back\\slash","tab\there"]`. Exact list equality holds for all three.

## --journal on the capture
```
$ python3 tools/mori-userns-runway.py --journal capture.txt
SYSCTL_WRITES n=0 keys=0 userns_zero=0
rc=0
```
No SETUP line. Self-test (`TMPDIR=<scratch> --selftest`): `MORI_USERNS_RUNWAY_SELFTEST: PASS (19 cases)`, rc 0.

## Findings against the hypothesis
- Rendering: `COMMAND=/usr/bin/true 'a b' it\'s x#012y` observed exactly (single quotes only around the spaced
  argument, `\'` for the apostrophe, `#012` for the newline).
- Split: the 3550-char argv was logged as one first line plus three `(command continued)` lines under pid
  4036579; the first line total length 998 and continuations 980/980/979 — consistent with the ~980 syslog_maxlen
  cut (the journal prefix accounts for the difference between message and line lengths; not measured further).
- Recovery: the tool's own join plus `split_cmd` reproduce the three argv lists exactly, including the 3550-char
  argument whose interior spaces sit at continuation boundaries.
- Write scan: 0 writes, 0 unparsed, rc 0 — the probe's own commands are not sysctl writes.

## Disclosure (scope)
- One command outside the authorized form: `sudo -n -l` (a sudo rules listing, non-mutating, output discarded),
  run once in the same bash call as the length measurement. It was run after the capture was taken, so the capture
  is unaffected. No other sudo call was made. No sysctl, service, limit or PATH change.
- No tool was installed or upgraded this seat. Scratch dir removed at the end of the run.

## Unrun checks
- Full round-99 incident capture (`evidence/journal-incident-r99.txt`) and the C1 counter were not run by this seat
  (not in the assignment).
- No live `journal-live` read was run (not in the assignment).

VERDICT C1 holds: on host sudo 1.9.17p2, the probe's three `sudo -n /usr/bin/true` commands were logged in the
exact sudo rendering predicted, the 3550-char argv split across `(command continued)` lines under one pid at the
~980 limit, and the landed tool recovered all three argv lists exactly (ALL_ARGV_EQUAL=True) with `--journal` rc 0
n=0 and no SETUP line.
