# SrcPgrepC — S162 candidate: procps-ng v4.0.7 `src/pgrep.c`

Verdict: **admit** (`code`, tier A, `mined`). Three of the four assigned sub-questions are
carried by the saved bytes and are quoted below. The fourth (what pgrep uses when
`/proc/<pid>/cmdline` is empty) is **not** carried by this file: it lives one layer down in
`library/readproc.c`, so it is reported as a gap with a pointer and is *not* quoted as if it
came from S162.

## 1. Fetch record

| field | value |
|---|---|
| URL | https://gitlab.com/procps-ng/procps/-/raw/v4.0.7/src/pgrep.c |
| command | `curl -sSL --fail -m 60 -o S162.src <url>` |
| access time (UTC, `date -u +%FT%TZ` around the fetch, same second) | 2026-10-22T23:43:06Z |
| byte size | 45 309 |
| sha256 | `af711983209fa083eef970f045104397b0d1406b9aacad2be0747e966e584e16` |
| saved copy (byte-for-byte as fetched) | `/fast/scratch/hyaku/mori-r31/SrcPgrepC/S162.src` |
| response sanity | first bytes are the pgrep/pkill copyright banner (`S162.src:1-6`), 1 487 lines, no challenge page |
| host package studied version | `pacman -Q procps-ng` → `procps-ng 4.0.7-1` |

`sha256sum S162.src` after the fetch printed exactly the hash above; no re-encode, no
normalisation, no line-ending change was applied.

## 2. Located quotes (verbatim, from the saved file, word counts from `wc -w`)

**Q1 — which string is matched, `-f` versus no `-f`.** `src/pgrep.c:909-912`, 13 words:

> `if (opt_full) strncpy (cmdsearch, task_cmdline, cmdlen -1); else strncpy (cmdsearch, PIDS_GETSTR(CMD), cmdlen -1);`

Fact for a pid probe: the match key is the **task name** (`PIDS_CMD`, the `stat` name) unless
`-f` is given, in which case it is the **full command line** (`PIDS_CMDLINE`, bound at
`src/pgrep.c:888` as `task_cmdline = PIDS_GETSTR(CMDLINE);`). A probe result is therefore
meaningless until it states which of the two keys it searched. The help text names the same
two keys at `src/pgrep.c:189` (`--full`: the full command line) and `src/pgrep.c:203`
(`--exact`: the command name).

**Q2 — the probe cannot match itself.** `src/pgrep.c:851-852`, 5 words:

> `if (PIDS_GETINT(PID) == myself) continue;`

with `pid_t myself = getpid();` at `src/pgrep.c:819`. Fact for a pid probe: pgrep skips its own
pid before any filter runs, so a `-f` probe whose pattern would match its own argv (for example
a probe carrying the watchdog path on its command line) cannot produce a false positive from
itself; a reported match is always some other process.

**Q3 — long patterns against the task name yield nothing.** `src/pgrep.c:962-963`, 21 words:

> `if ((!matches) && (!opt_full) && is_long_match(opt_pattern)) warnx(_("pattern that searches for process name longer than 15 characters will result in zero matches\n"`

Fact for a pid probe: without `-f`, a pattern longer than 15 characters produces **zero
matches** and only a warning — so an empty result from a name-shaped probe such as
`pgrep shokunin-watchdog.sh` is an artefact of the pattern length, not evidence that the
watchdog is dead. `is_long_match` at `src/pgrep.c:783-796` gives the threshold
(`if (15 >= (len = strlen(str)))`) and deliberately excludes `|`/`[` patterns.

Quantities I checked myself rather than assumed: `shokunin-watchdog.sh` is 20 bytes
(`printf '%s' 'shokunin-watchdog.sh' | wc -c` → 20), the fleet script exists at
`/home/vgpnk/Projects/shokunin/scripts/shokunin-watchdog.sh` (17 846 bytes) and its first line
is `#!/usr/bin/env bash` (`:1`).

## 3. The fourth sub-question — what pgrep uses when cmdline is empty: **not in S162**

`src/pgrep.c` never special-cases an empty command line. It reads the value the library hands
it (`:888`) and matches it under `-f` (`:910`). The fallback is in the library, so it cannot be
admitted on this row. Evidence from probes I fetched the same way but did **not** admit (no
pre-assigned id):

- `https://gitlab.com/procps-ng/procps/-/raw/v4.0.7/library/readproc.c`, fetched
  2026-10-22T23:44:56Z, 58 191 B, sha256
  `6d40b02dfd57faeb85e1471eed0a03cbf6573805255e6f6e8a8de58f53f7cdde`:
  `library/readproc.c:973-983` `fill_cmdline_cvt` defines
  `uFLG ( ESC_BRACKETS | ESC_DEFUNCT )` and calls
  `escape_command(dst_buffer, p, MAX_BUFSZ, uFLG)` when `read_unvectored(... "cmdline" ...)`
  fails.
- `https://gitlab.com/procps-ng/procps/-/raw/v4.0.7/library/escape.c`, fetched
  2026-10-22T23:46:39Z, sha256
  `c0bc6505ab7426178241202bd7815de8a34c4e1cc6dd31c1eafa7438d2a7ce2f`:
  `library/escape.c:139-164` writes `'['`, then `pp->cmd`, then `']'`, then
  `" <defunct>"` for a `Z` state.

Observed: the two library functions render an empty cmdline as the bracketed task name.
`[INFERENCE]`: because pgrep matches `PIDS_CMDLINE` under `-f`, a `-f` probe against such a
process is matching `[comm]`, not an empty string — no single file I opened states that
composition. The L1 decides whether that deserves its own new id; it should not be credited to
S162.

## 4. Ready to paste — Gate row

Exactly one physical line, sha in single backticks, three quotes (13, 5, 21 words), last cell
starts with `admit` — all required by the C1 counter parser. Validated by re-running that
parser's own regexes over this string.

```text
| S162 | https://gitlab.com/procps-ng/procps/-/raw/v4.0.7/src/pgrep.c | 2026-10-22T23:43:06Z | `af711983209fa083eef970f045104397b0d1406b9aacad2be0747e966e584e16` | `src/pgrep.c:909-912` (13 words): "if (opt_full) strncpy (cmdsearch, task_cmdline, cmdlen -1); else strncpy (cmdsearch, PIDS_GETSTR(CMD), cmdlen -1);"; `src/pgrep.c:851-852` (5 words): "if (PIDS_GETINT(PID) == myself) continue;"; `src/pgrep.c:962-963` (21 words): "if ((!matches) && (!opt_full) && is_long_match(opt_pattern)) warnx(_(\"pattern that searches for process name longer than 15 characters will result in zero matches\n\"" | admit, A, mined |
```

## 5. Ready to paste — SOURCES row

11 cells, column order copied from `corpus/SOURCES.md:5`. Add exactly one S162 row: the counter
fails a source when `source_rows.get(sid) != 1`.

Destination split: the Gate row (section 4) goes into `corpus/lessons/round-31.md`; this row
goes into `corpus/SOURCES.md`. The counter only counts this row in `SOURCES.md` and only counts
`admit`-suffixed rows as gates, so the two must not be swapped and the registry row must not be
duplicated.

```text
| S162 | procps-ng v4.0.7 pgrep process-selection source — https://gitlab.com/procps-ng/procps/-/raw/v4.0.7/src/pgrep.c | code | A | how pgrep v4.0.7 picks the string it matches: the task name without `-f`, the command line with `-f`, its own-pid exclusion and the long-pattern warning; not the library's empty-cmdline fallback, not pkill's signalling | src/pgrep.c:819,851-852,888,909-912,962-965; 45 309 B at tag v4.0.7, opened 2026-10-22 | Without `-f` pgrep matches the task name, so a pattern longer than 15 characters yields zero matches and a warning; with `-f` it matches the full command line; pgrep always skips its own pid, so a `-f` probe cannot match itself. | mined | 2026-10-22 | on-release | corpus/knowledge/watchdog-identity-r31.md |
```

## 6. Admit or reject

**Admit.** None of the three reject triggers fires.

- Bytes carry the fact: Q1/Q2/Q3 are literal in `S162.src` at the quoted lines, re-checked with
  `grep -n` and with a substring test of the whitespace-normalised file.
- URL is live and is not a challenge page: HTTP 200 via `--fail`, body is the C source.
- No duplicate row: `grep -n "gitlab.com/procps" corpus/SOURCES.md` → no match (rc=1);
  `grep -n "procps" corpus/SOURCES.md` → no match; `grep -n "v4\.0\.7\|pgrep" corpus/SOURCES.md`
  → only S126 (`gitlab.archlinux.org` earlyoom packaging, a different URL). Checked against
  SOURCES.md as of this run; if a sibling seat lands the same URL first, this row becomes a
  duplicate and must be merged.

Copy step for the L1: `cp /fast/scratch/hyaku/mori-r31/SrcPgrepC/S162.src
corpus/evidence/sources-r31/S162.src` — the counter hashes that committed file and requires
`af711983…584e16`, and requires every Gate quote to be a substring after whitespace
normalisation.

## 7. What this row can licence in the decision table (for C1's owner; not my call)

- A row reading "`pgrep shokunin-watchdog.sh` printed nothing" → verdict "no evidence of
  death", citing `src/pgrep.c:962-963` (20-character pattern, no `-f`).
- A row reading "`pgrep -f …` matched" → verdict "some other process's command line contains
  the string", citing `src/pgrep.c:909-912` plus `:851-852` (the probe cannot match itself).
- A row reading "`pgrep …` matched the task name" → verdict "a process whose 15-character task
  name matches", citing `src/pgrep.c:909-912` and `:783-796`.
- A row reading "`pgrep -f` returned nothing" must not be read as absence by itself without
  also saying which argv the target is expected to carry — S162 does not decide that; the
  script and `binfmt_script` rows do.

## 8. Housekeeping and bounds

- No tool installed, upgraded or removed; no pacman transaction attempted; no host service
  touched. `pgrep -V` is not a valid option (`rc=2`), so the version came from
  `pacman -Q procps-ng`.
- No git or jj command run in the lane or the fleet repo; read-only file reads only.
- Two short-lived `curl` processes, each under `timeout 60`; both exited before this report;
  nothing left running. Probe files were moved out of `/tmp` into my scratch dir, so `/tmp` is
  clean.
- Wrote only this report plus files under `/fast/scratch/hyaku/mori-r31/SrcPgrepC/`.
- No pid, uid, slice name, journal message text, OMP setting or session path appears here.

## 9. Remaining unknowns

- The `-f` argv shape of a `#!/usr/bin/env bash` script (whether the comm becomes `bash` and the
  argv carries the path) is a kernel/`binfmt_script` fact owned by the S164/S165 seats; S162
  says only which field is read.
- Whether the library's `[comm]` fallback becomes its own registry row (L1 decision).
- The exact `pgrep.1` wording for these behaviours belongs to the S161 seat; I did not open it.
