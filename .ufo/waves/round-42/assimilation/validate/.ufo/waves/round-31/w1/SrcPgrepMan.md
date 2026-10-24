# S161 — procps-ng v4.0.7 pgrep(1) (source scout report)

Seat: MoriR31.SrcPgrepMan. Question: what the procps-ng 4.0.7 pgrep(1) page carries
about what a `pgrep` probe matches (name versus `-f` full command line), `-x`, `-a`,
the exit status values, and the self-exclusion sentence — evidence for whether a pid
probe can establish that the fleet watchdog under the fleet root is alive.

## 1. Fetch

| field | value |
|---|---|
| URL | https://gitlab.com/procps-ng/procps/-/raw/v4.0.7/man/pgrep.1 |
| access time (UTC) | 2026-10-22T23:43:06Z (`date -u +%FT%TZ` run immediately before and after the fetch; both read this value) |
| HTTP | 200, 9702 bytes downloaded (`curl -w '%{http_code} %{size_download}'`) |
| saved unchanged | /fast/scratch/hyaku/mori-r31/SrcPgrepMan/S161.src |
| bytes / lines | 9702 bytes, 378 lines (`wc -c -l`) |
| sha256 | c2024c384dd88df2a4d5093d4726e57f38c5fee378dc7ed4c99c70c2f6341e35 |
| content type | `text/troff; charset=us-ascii` (`file -i`); `grep -n '^\.TH'` → `13:.TH PGREP 1 2025-12-29 procps-ng` |
| challenge check | 0 matches for `captcha\|challenge\|Just a moment\|Cloudflare`; real roff with the upstream copyright block at :1-12 |
| re-fetch stability | a second fetch of the same URL is byte-identical (`cmp` → identical, same sha256), so the C1 counter's own fetch will reproduce the hash |

Command run:
`curl -sSL --fail -m 60 -o S161.src -w '%{http_code} %{size_download}\n' '<URL>'` → `200 9702`.

## 2. Located anchors (line numbers from `grep -n` / `sed -n` on S161.src)

| point | lines | what sits there (my words; only §3 quotes verbatim) |
|---|---|---|
| default match vs `-f` | 103-108 | `-f/--full`: the pattern is normally matched only against the process name; with `-f` the full command line is used |
| `-x/--exact` | 230-234 | matches only processes whose names — or command lines when `-f` is given — exactly match the pattern |
| `-a/--list-full` | 70-73 | lists the full command line as well as the pid (pgrep only) |
| `-l/--list-name` | 139-143 | lists the process name as well as the pid (pgrep only) |
| EXIT STATUS | 294-311 | `0` one or more matched (:296-302), `1` no processes matched or none could be signalled (:304-305), `2` syntax error in the command line (:307-308), `3` fatal error, out of memory etc. (:310-311) |
| name source and 15-char cap | 313-316 | matching name is limited to the 15 characters present in the output of `/proc/<pid>/stat`; `-f` covers the complete `/proc/<pid>/cmdline`; threads may share cmdline but not name |
| self-exclusion | 318-324 | the running pgrep, pkill or pidwait process never reports itself as a match |
| ancestors are not excluded by default | 75-80 | `-A/--ignore-ancestors` exists to ignore all ancestors, so without it ancestors are eligible |
| pattern grammar | 261-265 | operand `pattern` is an Extended Regular Expression matched against process names or command lines |

## 3. Located verbatim quotes

Line numbers are from `grep -n`/`sed -n` on the saved file; each quote is the exact bytes of
the span with the line breaks rendered as single spaces (the C1 counter compares
whitespace-normalised text, `norm`, .ufo/waves/round-31/count-c1.py:45 and :154, so the
multi-line spans survive the check). Word counts are `wc -w` of the flattened span.

**Q1 — S161.src:105-108 (21 words).**

```
.I pattern is normally only matched against the process name.  When .B \-f is set, the full command line is used.
```

Fact it supports: without `-f` the probe matches only a process name, so
`pgrep shokunin-watchdog` is not looking at the script path at all; `-f` is the only
documented way to match `/proc/<pid>/cmdline`.

**Q2 — S161.src:305 (10 words).**

```
No processes matched or none of them could be signalled.
```

Fact it supports: exit `1` is the page's "no match" answer (its signalling clause is about
pkill/pidwait), so a probe must read `1` as "no match", while `2` and `3` (:307-308,
:310-311) are command-line syntax and fatal errors — not evidence about the target.

**Q3 — S161.src:318-324 (19 words).**

```
The running .BR pgrep , .BR pkill , or .B pidwait process will never report itself as a match.
```

Fact it supports: self-exclusion covers only the pgrep/pkill/pidwait process itself, so the
probe never counts itself but the shell or wrapper that carries the pattern in its own
argv remains matchable — the page's `-A/--ignore-ancestors` option at :75-80 exists because
ancestors are otherwise eligible.

## 4. Ready-to-paste rows

Gate row (one physical line, for corpus/lessons/round-31.md; paste exactly once so the
counter sees one admit row for S161):

```
| S161 | https://gitlab.com/procps-ng/procps/-/raw/v4.0.7/man/pgrep.1 | 2026-10-22T23:43:06Z | `c2024c384dd88df2a4d5093d4726e57f38c5fee378dc7ed4c99c70c2f6341e35` | `man/pgrep.1:105-108` (21 words): ".I pattern is normally only matched against the process name.  When .B \-f is set, the full command line is used."; `man/pgrep.1:305` (10 words): "No processes matched or none of them could be signalled."; `man/pgrep.1:318-324` (19 words): "The running .BR pgrep , .BR pkill , or .B pidwait process will never report itself as a match." | admit, A, mined |
```

SOURCES row (11 columns, order taken from corpus/SOURCES.md:5):

```
| S161 | procps-ng v4.0.7 pgrep(1) — https://gitlab.com/procps-ng/procps/-/raw/v4.0.7/man/pgrep.1 | docs | A | the pgrep/pkill/pidwait manual page at the v4.0.7 release tag: matching against the process name by default and the full command line under -f, -x exact matching, -a and -l output forms, exit status 0/1/2/3, the 15-character process-name limit taken from /proc/<pid>/stat versus the full /proc/<pid>/cmdline, and the self-exclusion rule | man/pgrep.1:70-73,75-80,103-108,139-143,230-234,261-265,294-311,313-316,318-324; procps-ng v4.0.7 tag | A pgrep hit or miss is a statement about the /proc view only: the default match is a name capped at 15 characters from /proc/<pid>/stat, -f reaches the whole command line, exit 2/3 are probe errors rather than absence, and self-exclusion covers only the pgrep process itself. | mined | 2026-10-22 | on-release | corpus/knowledge/watchdog-identity-r31.md |
```

Copy to land: `cp /fast/scratch/hyaku/mori-r31/SrcPgrepMan/S161.src
<lane>/corpus/evidence/sources-r31/S161.src` — sha256 must stay
`c2024c38…6341e35`; the counter checks the copy's hash against the Gate row and re-fetches
the URL.

## 5. Decision

**admit.**

- The bytes carry every assigned fact in its own words: name-versus-`-f` (:105-108), `-x`
  (:230-234), `-a` (:70-73), exit status (:294-311), the 15-character name cap and the
  `/proc/<pid>/stat` versus `/proc/<pid>/cmdline` split (:313-316), and self-exclusion
  (:318-324). None of the three quotes is a mention; each is the operative sentence.
- Not a 404 and not a challenge page: HTTP 200, 9702 bytes of real roff, `.TH PGREP 1
  2025-12-29 procps-ng` at :13, upstream copyright block at :1-12, zero challenge markers,
  and a second fetch is byte-identical.
- Not already registered: `grep -n 'pgrep' corpus/SOURCES.md` → no match; `grep -n '| S161 '
  corpus/SOURCES.md` → no match; `grep -c 'gitlab.com' corpus/SOURCES.md` → 0, so no
  GitLab-hosted row exists at all and this exact URL cannot be a duplicate. The registry
  holds 160 `| S###` rows, so S161 is free in this read.
- It is a docs-tier primary source (the shipped manual page at the release tag), which is the
  right tier for a rule about how the command reads `/proc`, not how the kernel sets the
  fields.

## 6. Facts for the C1 decision table (verdict wording left to the L1)

All lines below are S161.src unless marked [INFERENCE] or "host".

1. `pgrep <pattern>` matches the process name only (:105-108), and that name is the
   15-character field from `/proc/<pid>/stat` (:313-314). A shell script executed by bash
   shows comm `bash`, not the script name: host command `printf 'cat /proc/$$/comm\n' >
   comm-probe.sh && bash comm-probe.sh` printed `bash`. [INFERENCE] A bare
   `pgrep shokunin-watchdog` therefore cannot find a bash-run watchdog script.
2. `pgrep -f <ere>` matches the whole `/proc/<pid>/cmdline` (:105-108, :315) with an ERE
   (:261-265), so any process whose argv contains the string matches — an editor, a `tail`,
   or the invoking `bash -c` wrapper — not just the watchdog interpreter. [INFERENCE] from
   :75-80 (ancestors eligible unless `-A`) and :318-324 (only the pgrep process is excluded).
3. `pgrep -f -x '<whole cmdline>'` needs the entire command line to match exactly (:230-234);
   an extra argument or a different interpreter changes the cmdline and the probe misses a
   live watchdog.
4. Exit `0` means at least one match, `1` means no match (:296-302, :304-305), `2` and `3`
   are syntax/fatal errors (:307-311). A probe that maps "nonzero" to "watchdog down"
   misreads a malformed or failing probe as evidence of death.
5. Self-exclusion (:318-324) means the probe process cannot vouch for itself; the fact says
   nothing about a *second* pgrep or a wrapper started by the same command.
6. Zombie or racily-exiting processes and `/proc` visibility (pid namespace, hidepid) are
   not covered by S161; leave those rows to S166/S167/S168 and mark them [INFERENCE] until
   those copies land.

Host observation worth one line for the tool seats (not a source fact): in this seat's
harness bash, `type -a pgrep` prints `pgrep is a shell builtin` before `/usr/bin/pgrep`, and
that builtin answers `pgrep --version` with `pgrep 0.2.0` and a reduced option set (no `-a`,
no `-l`), while `/usr/bin/pgrep --version` prints `pgrep from procps-ng 4.0.7` and
`--help` lists `-a, --list-full`. Any probe or gate script must call `/usr/bin/pgrep` (or a
resolved absolute path) or it may exercise a different implementation than S161 documents.

## Bounds and tooling

- Wrote only this report and files under /fast/scratch/hyaku/mori-r31/SrcPgrepMan/
  (`S161.src`; temporary `refetch.tmp` and `comm-probe.sh` removed). No lane file written,
  no git or jj command run, nothing signalled, no unit touched, no pacman run.
- No tool installed or updated; curl, sha256sum, file, grep, sed, wc were already present.
- Processes: every command bounded (`curl -m 60`, probes under `timeout 5`); nothing left
  running.
- Privacy: no uid, real pid (the probe used `$$` inside its own process and only reported a
  comm string), unit name, journal text, settings value or session path in this report.
