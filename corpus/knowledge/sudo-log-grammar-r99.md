# Reading sudo's COMMAND= log as argv, and a shell -c script as commands

source: S635 — https://raw.githubusercontent.com/sudo-project/sudo/v1.9.17p2/lib/eventlog/eventlog.c — code, tier A, sudo eventlog.c at tag v1.9.17p2 (COMMAND= rendering, syslog line split), committed copy `corpus/evidence/sources-r99/S635-sudo-eventlog.c`, opened 2026-11-05
source: S636 — https://raw.githubusercontent.com/sudo-project/sudo/v1.9.17p2/lib/util/lbuf.c — code, tier A, sudo lbuf.c at tag v1.9.17p2 (control-character and quote escapes), committed copy `corpus/evidence/sources-r99/S636-sudo-lbuf.c`, opened 2026-11-05
source: S633 — https://man7.org/linux/man-pages/man8/sysctl.8.html — docs, tier A, sysctl(8) procps-ng (OPTIONS -p/--load, -r/--pattern), committed copy `corpus/evidence/sources-r99/S633-sysctl.8.html`, opened 2026-11-05
source: S634 — https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html — spec, tier A, POSIX.1-2024 XCU chapter 2 (2.2 Quoting, 2.3 Token Recognition), committed copy `corpus/evidence/sources-r99/S634-posix-shell.html`, opened 2026-11-05
source: S014 — https://www.freedesktop.org/software/systemd/man/latest/journalctl.html — docs, tier A, journalctl(1) Output Options (short, short-iso), re-opened 2026-11-05, committed copy `corpus/evidence/sources-r99/S014-journalctl-r99.html`
verified-at: 2026-11-05
recheck: on-release — `python3 tools/mori-userns-runway.py --selftest`; at the next sudo release fetch S635/S636 at the new tag and diff the COMMAND= block (`Wrap args containing spaces`) and `should_quote`; the host runs sudo 1.9.17p2
coverage-map: resource runway (user namespaces, round 98) — the write-event scan's input grammar, round 99

The round-98 write scan read sudo's `COMMAND=` text with a POSIX shell splitter and the `-c` script with two
regexes. Neither is the grammar sudo writes. sudo renders the command path, then each argument after one
space; an argument that holds a space is wrapped in single quotes, `'` and `\` are backslash-escaped in every
argument, and control characters become `#0nn` octal escapes, so a newline in a `sh -c` script is logged as
`#012`. A POSIX splitter reads `\'` inside single quotes as the end of the quote: on the 2026-11-05 incident
capture 24 of the 276 `COMMAND=` values failed that splitter and fell back to whitespace
splitting (`w1/Mo99ScribeLesson.md` Mistake 4). A line longer than sudo's
`syslog_maxlen` is cut at a space and the rest is logged under the same pid as `user : (command continued) REST`;
a capture filtered on `COMMAND=` keeps the first part and drops the rest. Inside the recovered `-c` argument, a
shell reads quotes and comments before it reads redirections, so `/proc/sys` text inside quotes or after a word-
initial `#` is not a write. `sysctl -r PATTERN` takes a filter argument, not a setting.

## Claims

| claim | source | quote |
|---|---|---|
| sudo logs the command path, then each argument; an argument containing a space is wrapped in single quotes. | S635 | `/* Wrap args containing spaces in single quotes. */` (eventlog.c:202) |
| Arguments without a space are escaped the same way, so `'` and `\` are backslash-escaped everywhere. | S635, S636 | `/* Escape quotes here too for consistency. */` (eventlog.c:208); `(ISSET(flags, LBUF_ESC_QUOTE) && (ch == '\'' || ch == '\\'))` (lbuf.c:163) |
| Control characters, including newline, are logged in octal as `#0nn`. | S636 | `Any non-printable characters are escaped in octal as #0nn.` (lbuf.c:145) |
| A long log line is split at a space and the rest is logged as a continuation of the same entry. | S635 | `fmt = _("%8s : (command continued) %s");` (eventlog.c:1042) |
| An exit event appends ` ; EXIT=` / ` ; SIGNAL=` after the argv; those words are not arguments. | S635 | `sudo_lbuf_append_esc(lbuf, LBUF_ESC_CNTRL, " ; EXIT=%s",` (eventlog.c:223) |
| Single quotes keep every enclosed character literal, so `/proc/sys` text inside quotes is an argument, not a redirection target. | S634 | `Enclosing characters in single-quotes ('') shall preserve the literal value of each character within the single-quotes.` (2.2.2) |
| A `#` that starts a token begins a comment that runs to the newline. | S634 | `If the current character is a '#', it and all subsequent characters up to, but excluding, the next <newline> shall be discarded as a comment.` (2.3 rule 9) |
| `-p[FILE]`/`--load` loads settings from a file (default /etc/sysctl.conf): a write whose keys the log does not show. | S633 | `Load in sysctl settings from the file specified or /etc/sysctl.conf if none given.` (OPTIONS, tags stripped) |
| `-r`/`--pattern` takes a regex that filters settings: its argument is never a key=value write. | S633 | `Only apply settings that match pattern.` (OPTIONS, tags stripped) |
| `journalctl -o short` (the default) prints classic syslog timestamps; `short-iso` prints RFC 3339 ones, so a scan must accept both or fail closed. | S014 | `is the default and generates an output that is mostly identical to the formatting of classic syslog files` (Output Options, `short`) |

## How the tool applies it (round 99)

`tools/mori-userns-runway.py` `split_cmd` inverts the sudo rendering (quote, `\'`, `\\`, `#0nn`, exit suffix);
`scan_journal` joins `(command continued)` parts by pid before reading; `shell_tokens`/`script_writes` read a
`-c` script as POSIX words, quotes, comments and operators, then report a write for an output redirection to
`/proc/sys/...`, a `tee` into it, or a nested `sysctl`/shell `-c`. A line counts as a sudo entry only when it
carries the identifier `sudo[PID]:` (text that merely mentions `sudo[N]`, such as systemd's `Started sudo[108]`, is
ignored; post-landing fix, `w1/Mo99ExecReplay.md`). Any sudo line it cannot read (an unknown
timestamp shape, a quote still open at the end, an orphan continuation) is counted and the scan exits 2 with
`SYSCTL_WRITES_SETUP unparsed=U`: an unreadable line is never reported as "no write".

Evidence: the round-98 capture `.ufo/waves/round-98/evidence/journal-incident-r98.txt` was filtered on
`COMMAND=` and lost one continuation line; read with the round-99 tool it scores the same six writes but exits 2
(`unparsed=1`). The full round-99 capture `.ufo/waves/round-99/evidence/journal-incident-r99.txt` (every
`sudo[` line, 05:14–05:43 -03) keeps the continuation and scores `n=6 keys=1 userns_zero=2`, exit 1.

## Limits

- sudo does not escape a literal `#0` followed by a digit, so such text in an argument decodes as a control
  character. No write shape in the capture depends on it.
- The script reader covers words, quotes, comments, backslash-newline, `;` `&&` `||` `&` `|` newlines,
  `>` `>>` `>|` `&>` `&>>` `>&` `<&` `<`, and skips here-document bodies (`<<`, `<<-`). It does not expand
  variables, command substitution or functions: `echo 0 > $F` with `F=/proc/sys/...` is not seen. (`>|`,
  backslash-newline, here-documents, `#040` and quoted ` ; EXIT=` text were added after the landing measurement,
  from the w1 review `w1/Mo99RevC1.md` F1–F6.)
- sudo renders an empty argument as nothing between two spaces (`tee '' /proc/sys/x` logs like `tee /proc/sys/x`),
  so the scan reports such a `tee` as a write: over-reporting, never a missed write (`w1/Mo99RevC1.md` F7).
- When sudo found no space to split at, the continuation was cut mid-word; the tool rejoins with one space.
- JSON-format sudo logs (`@cee:` lines) and sudo_logsrvd I/O logs are not read.

## Boundaries

Detection and report only. Which sysctl writes are allowed on the host is operator policy, and restoring a value
is tsukuroi's work. The scan never runs sudo and never writes a sysctl.
