# Mo98RevC1 — reviewer, C1 code and content review (round 98, w1)

Scope: `tools/mori-userns-runway.py`, `corpus/knowledge/userns-runway-r98.md`, the SKILL.md registry row
(line 1460), the PROVINCE.md round-98 note, and the pinned sources `corpus/evidence/sources-r98/S629..S632`.
Lane HEAD 379a2f6. `git diff --stat 600deb7 HEAD` over the reviewed paths prints nothing, so the bytes
reviewed are the landing bytes. LSP: not used (single stdlib script; no references to resolve). All
probes ran in `/fast/scratch/hyaku/mori-r98/Mo98RevC1` (TMPDIR set there; removed at the end). No tools
installed. No sudo, no sysctl change, no namespace created.

## Verdict summary

The tool's behaviour matches the knowledge file, the registry row and the PROVINCE note. Every quote
matches its pinned source. The self-test cell matches the tool's output verbatim. The runway read
handles every edge case I tried without a wrong state. The journal classifier misses several
plausible sudo write forms and counts a few reads as writes. The tool docstring lists the forms it
detects, so most misses are documented limits. Three findings are low-severity defects inside the
claimed scope (F1–F3). None of them changes C1's frozen measurement (`cases_ok`).

## (1) Knowledge claims vs pinned sources and tool behaviour

Quotes, checked against the pinned copies (whitespace-normalised for the .rst, tags stripped for the .html):

```
True The files in this directory can be used to overrid      (S629, claim 1)
True The maximum number of user namespaces that any use      (S629, claim 2)
True The creation of per user per user namespace object      (S629, claim 3)
True The creation of objects is also charged to all of       (S629, claim 4)
44:	PROC_USER_INIT_INO	= USER_NS_INIT_INO,                 (S631, claim 6)
50:	USER_NS_INIT_INO	= 0xEFFFFFFDU,                      (S632, claim 7); python3 -c 'print(0xEFFFFFFD)' -> 4026531837
S630: "ENOSPC (since Linux 4.9) One of the values in flags specified the creation of a new user namespace, but doing so
would have caused the limit defined by the corresponding file in /proc/sys/user to be exceeded."   (claim 5)
```

Tool runs used to check the "Observed" and reading-rule rows:

```
$ python3 tools/mori-userns-runway.py --journal .ufo/waves/round-98/evidence/journal-incident-r98.txt
SYSCTL_WRITE ts=2026-11-05T05:14:52-03:00 pid=1302030 key=user.max_user_namespaces value=0 via=sh-echo
SYSCTL_WRITE ts=2026-11-05T05:14:54-03:00 pid=1316549 key=user.max_user_namespaces value=10000 via=sysctl
SYSCTL_WRITE ts=2026-11-05T05:16:04-03:00 pid=1580806 key=user.max_user_namespaces value=15638 via=sysctl
SYSCTL_WRITE ts=2026-11-05T05:16:04-03:00 pid=1580838 key=user.max_user_namespaces value=15638 via=sh-echo
SYSCTL_WRITE ts=2026-11-05T05:22:02-03:00 pid=2322929 key=user.max_user_namespaces value=0 via=sh-echo
SYSCTL_WRITE ts=2026-11-05T05:42:18-03:00 pid=2548588 key=user.max_user_namespaces value=122865 via=sysctl
SYSCTL_WRITES n=6 keys=1 userns_zero=2
rc=1
$ wc -l / grep -c COMMAND=  -> 276 / 276 ; lines 29, 36 are `sysctl -a` (not counted)
$ python3 tools/mori-userns-runway.py            (live, non-root)
USERNS_RUNWAY limit=122865 used_lb=6 pids=3486 unreadable=3223 runway=122859 low=32 state=ok
rc=0
```

- Claims 1–7: each quote matches its pinned source, and each paraphrase stays within its quote. Holds.
- "Observed" incident scan: n=6, keys=1, userns_zero=2, the six timestamps and values, 276 lines, and the
  two `sysctl -a` reads not counted all match the run above. The 05:16:04 "twice" is one `sysctl` write
  without `-w` (line 90) and one `sh -c echo` write (line 91). The parenthetical explains only the first
  of the two, but the count is right. Holds.
- The live read was 7 at landing and 6 now. The value is time-varying and the claim is dated, so this is
  not a defect.
- Reading rules, limit 0 -> exhausted rc 1; runway 0 -> exhausted; runway < low -> low; >= low -> ok;
  limit missing or unparsable -> SETUP rc 2: all reproduced (see section 3, and the selftest). Holds.
- The redaction claim (no user, PWD or command text in the output) holds. The selftest `redaction` case
  passes, and every probe output in section 2 carries fields only.
- Write scope: the only file write is inside `_fake_proc` under `tempfile.mkdtemp` (honours TMPDIR,
  rmtree in `finally`). `journalctl` is read-only. Holds.

## (2) Journal classifier probes

Driver: `printf '%s\n' "2026-11-05T00:00:00-03:00 h sudo[1]:    u : PWD=/w ; USER=root ; COMMAND=<cmd>" | python3 tools/mori-userns-runway.py --journal -`

### Writes that are missed (rc=0, n=0)

```
SYSCTL_WRITES n=0 keys=0 userns_zero=0 rc=0  <= /usr/bin/sh -c 'printf 0 > /proc/sys/user/max_user_namespaces'
SYSCTL_WRITES n=0 keys=0 userns_zero=0 rc=0  <= /usr/bin/sh -c 'printf "%s\n" 0 > /proc/sys/user/max_user_namespaces'
SYSCTL_WRITES n=0 keys=0 userns_zero=0 rc=0  <= /usr/bin/dd of=/proc/sys/user/max_user_namespaces
SYSCTL_WRITES n=0 keys=0 userns_zero=0 rc=0  <= /usr/bin/sh -c 'echo 0 | dd of=/proc/sys/user/max_user_namespaces'
SYSCTL_WRITES n=0 keys=0 userns_zero=0 rc=0  <= /usr/bin/bash -lc 'echo 0 > /proc/sys/user/max_user_namespaces'
SYSCTL_WRITES n=0 keys=0 userns_zero=0 rc=0  <= /usr/bin/sh -ec 'echo 0 > /proc/sys/user/max_user_namespaces'
SYSCTL_WRITES n=0 keys=0 userns_zero=0 rc=0  <= /usr/bin/sh -c 'echo 0 | tee --append /proc/sys/user/max_user_namespaces'
SYSCTL_WRITES n=0 keys=0 userns_zero=0 rc=0  <= /usr/bin/sh -c 'cat <<< 0 > /proc/sys/user/max_user_namespaces'
SYSCTL_WRITES n=0 keys=0 userns_zero=0 rc=0  <= /usr/bin/env sysctl -w user.max_user_namespaces=0
SYSCTL_WRITES n=0 keys=0 userns_zero=0 rc=0  <= /usr/bin/timeout 5 sysctl -w user.max_user_namespaces=0
SYSCTL_WRITES n=0 keys=0 userns_zero=0 rc=0  <= /usr/bin/su -c 'echo 0 > /proc/sys/user/max_user_namespaces'
SYSCTL_WRITES n=0 keys=0 userns_zero=0 rc=0  <= /usr/bin/cp /w/zero /proc/sys/user/max_user_namespaces
SYSCTL_WRITES n=0 keys=0 userns_zero=0 rc=0  <= /usr/bin/python3 -c open('/proc/sys/user/max_user_namespaces','w').write('0')
SYSCTL_WRITES n=0 keys=0 userns_zero=0 rc=0  <= /usr/lib/systemd/systemd-sysctl
```

### Writes that are detected but with the wrong key or value (userns_zero misses the zero)

```
SYSCTL_WRITE ... key=? value=? via=sysctl SYSCTL_WRITES n=1 keys=1 userns_zero=0 rc=1  <= /usr/bin/sysctl -w user.max_user_namespaces = 0
SYSCTL_WRITE ... key=user.max_user_namespaces value=? via=sysctl ... userns_zero=0 rc=1   <= /usr/bin/sysctl -w user.max_user_namespaces= 0
SYSCTL_WRITE ... key=user.max_user_namespaces value=? via=sh-echo ... userns_zero=0 rc=1  <= /usr/bin/sh -c 'v=0; echo $v > /proc/sys/user/max_user_namespaces'
SYSCTL_WRITE ... key=user.max_user_namespaces value=00 via=sysctl ... userns_zero=0 rc=1  <= /usr/bin/sysctl -w user.max_user_namespaces=00
SYSCTL_WRITE ... key=user.max_user_namespaces value=- via=tee ... userns_zero=0 rc=1      <= /usr/bin/tee /proc/sys/user/max_user_namespaces
```

[INFERENCE, procps-ng source not opened] With `-w`, procps-ng sysctl rejects a bare token that has no
`=`, so `key = 0` with spaces probably fails on the host rather than writing. If so, counting it as a
`key=?` write is a harmless over-count, not a miss.

### Correctly handled

`sysctl --write k=0`, `-q -w`, `-qw`, `user/max_user_namespaces=0`, `sh -c 'echo 0 >/proc/sys/...'`,
`/proc/sys//user/...`, `tee -a` in a script, `sysctl -a`, `sysctl -n key`, `cat /proc/sys/...`, and
`sh -c 'cat /proc/sys/... | tee /w/out'` all give the expected result. Also handled correctly:
`sh -c 'echo 0 2>/proc/sys/...'`, which redirects stderr, so the tool rightly does not count it.

### Reads or non-writes counted as writes

```
SYSCTL_WRITE ... key=user.max value=x via=sysctl ... rc=1   <= /usr/bin/sysctl -a -r 'user.max=x'        (-r/--pattern regex arg)
SYSCTL_WRITE ... key=a value=b via=sysctl ... rc=1          <= /usr/bin/sysctl -a --pattern 'a=b'
SYSCTL_WRITE ... key=user.max_user_namespaces value=0 via=sh-echo ... userns_zero=1 rc=1  <= /usr/bin/sh -c 'echo "echo 0 > /proc/sys/user/max_user_namespaces" > /w/note.txt'
SYSCTL_WRITE ... key=user.max_user_namespaces value=0 via=sh-echo ... userns_zero=1 rc=1  <= /usr/bin/sh -c '# echo 0 > /proc/sys/user/max_user_namespaces'
```

### Input format and sudo outcome

```
$ (line in default `journalctl -o short`: "Nov 05 05:14:52 h sudo[1]: ... COMMAND=/usr/bin/sysctl -w user.max_user_namespaces=0")
SYSCTL_WRITES n=0 keys=0 userns_zero=0
rc=0
$ (short-iso-precise timestamp) -> SYSCTL_WRITE ... value=0 ... userns_zero=1 rc=1
$ ("command not allowed ; ... COMMAND=sysctl -w user.max_user_namespaces=0") -> userns_zero=1 rc=1
$ ("3 incorrect password attempts ; ... COMMAND=...")                       -> userns_zero=1 rc=1
```

## (3) Runway edge cases (fake `--proc`; pids 1=init link, 2=`user:[4026533001]`, 3=no ns dir)

```
trail          USERNS_RUNWAY limit=122865 used_lb=1 pids=3 unreadable=1 runway=122864 low=32 state=ok   rc=0
lead-tab       USERNS_RUNWAY limit=5 used_lb=1 ... runway=4 state=low                                   rc=1
huge           USERNS_RUNWAY limit=99999999999999999999999 ... runway=99999999999999999999998 state=ok   rc=0
intmax         USERNS_RUNWAY limit=2147483647 ... runway=2147483646 state=ok                             rc=0
neg|plus|hex|empty   USERNS_RUNWAY_SETUP limit unparsable                                               rc=2
arabic-digits  USERNS_RUNWAY limit=12 ... state=low  (limit file "١٢")                                  rc=1
zero-spaces    USERNS_RUNWAY limit=0 used_lb=1 ... runway=0 state=exhausted                              rc=1
one            USERNS_RUNWAY limit=1 used_lb=1 ... runway=0 state=exhausted                              rc=1
low-neg        USERNS_RUNWAY limit=100 ... low=-5 state=ok                                               rc=0
pid-symlink    (pid entry is a dangling symlink) ... unreadable=1 state=ok                               rc=0
limit-is-dir   USERNS_RUNWAY_SETUP limit unreadable: IsADirectoryError                                   rc=2
race-vanish    (os.readlink patched to raise FileNotFoundError for pid 2, i.e. it vanished after listdir)
               USERNS_RUNWAY limit=1 used_lb=0 pids=3 unreadable=2 runway=1 low=32 state=low
```

Leading and trailing whitespace, huge values, empty input and non-decimal forms all behave sanely, and
no crash surfaced. A pid that vanishes mid-scan falls into `unreadable`, and its namespace drops out of
`used_lb`. The lower bound is still honest, but `unreadable` mixes vanished pids with permission-denied
ones (see F5).

## (4) Registry self-test cell

```
$ python3 tools/mori-userns-runway.py --selftest | tail -1 ; echo rc=$?
MORI_USERNS_RUNWAY_SELFTEST: PASS (11 cases)
rc=0
registry cell 6: `python3 tools/mori-userns-runway.py --selftest` -> `MORI_USERNS_RUNWAY_SELFTEST: PASS (11 cases)` exit 0
```

The cell matches verbatim. The cell 7 pinned value `SYSCTL_WRITES n=6 keys=1 userns_zero=2` matches the
incident run. The cell 5 verdict map and exit codes match `main()`. The PROVINCE note (read-only
boundary, operator and tsukuroi ownership) matches the tool.

## Findings by severity

| id | severity | class | finding (evidence above) |
|---|---|---|---|
| F1 | low | defect-in-claimed-scope | Wrong timestamp format fails open. Sudo lines in default `journalctl -o short` format do not match `TS_PID_RE` and are dropped silently, so the output is `n=0 ... rc=0` ("no write") instead of `SYSCTL_WRITES_SETUP`. The docstring names `-o short-iso` as the input format, but a sudo `COMMAND=` line that is dropped unparsed should not read as "no write". |
| F2 | low | defect-in-claimed-scope | The docstring says reads such as `sysctl -a` are not writes, yet `sysctl -a -r PAT` / `--pattern PAT` count as a write when the regex contains `=`. The classifier does not skip the argument after `-r`/`--pattern`. |
| F3 | low | defect-in-claimed-scope | `ECHO_RE` matches inside quoted text and shell comments: `echo "echo 0 > /proc/sys/..." > file` and `# echo 0 > /proc/sys/...` both give `userns_zero=1`. These are false positives on the very key the tool exists to watch. |
| F4 | medium (coverage) | documented-limit | Missed write forms: `printf`, `dd of=`, `cp`, `cat <<<`, `tee --append`, combined shell flags (`bash -lc`, `sh -ec`), wrappers (`env`, `timeout`, `su -c`), interpreters (`python3 -c`), and `systemd-sysctl`. `sh -c 'v=0; echo $v > …'` is detected but gives `value=?`, so `userns_zero` misses it. The docstring lists the detected forms exhaustively, so the tool's contract is honest. The knowledge file's "Limits" section names only root shells and systemd units, though, so its readers are not told that these sudo-logged forms are missed. `bash -lc` and `sh -ec` are common enough that the next incident could use one. |
| F5 | low | documented-limit | Knowledge line 45 says unreadable links are "other users' processes". Pids that vanish mid-scan land in the same count (race-vanish probe). A root reader counts other users' namespaces against a per-user limit, so `runway=0 -> exhausted` can over-alarm. Lines 45–47 state the per-user nature, but the reading-rule table does not. |
| F6 | info | documented-limit | Lines from sudoers refusals ("command not allowed") and auth failures still count as writes. Covered by the knowledge row "not proof the write succeeded"; the refusal is visible on the line itself. |
| F7 | info | out-of-scope | `\d` accepts non-ASCII digits (`١٢` -> 12). The kernel never emits them. |

No finding falsifies a knowledge claim, the registry row, the PROVINCE note, or the self-test cell.

## Residual risk and unrun checks

- Unrun: the frozen counter `count-c1.py` (C1 measurement: not my seat); any live `unshare -Ur` probe (not
  authorised by this task); procps-ng source check for how `sysctl -w key = 0` parses (marked INFERENCE);
  `--journal-live` against the real journal; an LSP pass.
- Risk: the tool's verdict that the next incident's write was "not seen" holds only for the listed forms
  (F4). F1 can turn a wrong-format capture into a false "no write".

VERDICT C1 holds: tool, knowledge, registry row (self-test cell verbatim) and PROVINCE note agree with each other and with the pinned sources; the classifier gaps are documented limits or low-severity false positives/negatives (F1–F3) outside the frozen cases_ok measurement.
