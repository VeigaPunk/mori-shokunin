# SrcEarlyoomMainC — earlyoom v1.9.0 `main.c` startup/threshold emission (SOURCES row draft)

Seat: `MoriR26.SrcEarlyoomMainC` (wave 1, scribe). Date: 2026-10-22.
Scope: open `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c` and draft one
`corpus/SOURCES.md` row (id left as `S???`) plus a Gate line for the round-26 lesson.
No lane commit, no jj command, no mutation of any repo outside my report file.

## 1. Fetch receipt (Gate)

```
URL            https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c
HTTP           200
Bytes          21053
Lines          552
sha256         08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4
git blob sha   e695f375f80be80a3eef963b7a5222a25899d494
Access date    2026-10-22
Tag            v1.9.0 -> annotated tag object 66d78843fd675859a09a52d3f17b1c408a827a34
                 -> commit 202d4db0d308ca6478f68de68b46cae34896ddaf
                 (`git ls-remote --tags` shows refs/tags/v1.9.0 = 66d78843…, peeled 202d4db0…)
```

The L1's local copy at `/fast/scratch/hyaku/mori-r26/main.c` is byte-identical to my fetch
(same sha256 `08656b0b…f9d0e4`), so the lane already holds these exact bytes. My own copy and
every side file I cite are under `/fast/scratch/hyaku/mori-r26/MoriR26.SrcEarlyoomMainC/`.

Verbatim quotes (each at most 25 words, with line numbers in `main.c` at tag v1.9.0):

- main.c:414 — `fprintf(stderr, "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT ",\n",`
- main.c:416 — `fprintf(stderr, "        SIGKILL when mem avail <= " PRIPCT " and swap free <= " PRIPCT "\n",`
- main.c:161 — `fprintf(stderr, "earlyoom " VERSION "\n");`

Side files fetched at the same tag (digests for the L1):

```
msg.h        sha256 e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c  (blob 4b1fc2bda21708146264a7f71aefb8696fde8a32)
msg.c        sha256 a771c91529053341c290ede2a7df1d9fdf16e07fb9584db8a64604a45dea5197  (blob 3b7270f94cf7a45857244d3949571e5af6b647f1)
globals.h    sha256 8cc122f9006bbad159082b0532299f4e2caee25dd556db28d4149642559c8668
globals.c    sha256 a8b8fb8ff8d93a488c7c95ec0ed91e2758128eee7cfcd101a48af5dc0d1559b5
meminfo.c    sha256 526e512c89c58cb0b1db2ae98ea62d287cdc1516846be80c9173bdc4bf0edfeb
Makefile     sha256 b852cb9b832729f37f2b19fe93956720a5a58017aa8f76a6036cc928d96127ae
earlyoom.default sha256 c0770413a180e0731583f643fc4e84f4a0dac57efb8f575b74ee9a971df984a2
Arch PKGBUILD  sha256 f48dc3f99aee5d6a93f8cad4e4b6286dab014745aa6f85b1c3582c3db46dd4a2
```

## 2. The assigned question: do the threshold lines print the effective percentages after `-M`/`-S` conversion?

**Yes — and the value that reaches the comparison is the same number that was printed.** The
chain: `-m`/`-s` write `args.mem_term_percent` etc. **directly** during option parsing
(main.c:209-210, 219-220); `-M`/`-S` instead stash KiB values and set only the `have_M`/`have_S`
flags (main.c:228-230, 241-243). **After** the option loop, the `-M`/`-S` values are converted to
percentages (main.c:348: `M_term_percent = 100 * mem_term_kib / (double)m.MemTotalKiB`;
main.c:362: same for swap) and merged — when both `-m` and `-M` are given, the **lower** wins
(`min(...)`, main.c:352-353, 366-367; the `min` helper is main.c:57-62). Only then are the
thresholds printed (main.c:414-417), from those same `args.*_percent` fields that `lowmem_sig`
later compares against (main.c:500-503). So the printed number is the effective threshold, not
the raw option value. Two consequences the round can rest on:

- **The printed percentage is rounded and padded, not the raw double.** `PRIPCT` is
  `"%5.2lf%%"` (`msg.h:10`): two decimals in a five-column right-aligned field, so `5.00` renders
  as `" 5.00"` and `10.00` as `"10.00"`. The host's live line is `mem avail <=  5.00%` —
  **two** spaces, one from the literal `"<=" "` and one from the `%5.2lf` padding. Any parser
  that assumes a single space after `<=` will miss the SIGKILL threshold.
- **The `-M`/`-S` conversion basis differs from the `-m`/`-s` basis.** `-M` converts KiB against
  `m.MemTotalKiB` (main.c:348) and `-S` against `m.SwapTotalKiB` (main.c:362), whereas the
  runtime percentages are computed against `UserMemTotalKiB` (meminfo.c:112, 115) and
  `SwapTotalKiB` (meminfo.c:117). This is upstream's documented intent, not a defect: the
  `MANPAGE.md` at v1.9.0:65-70 says `-M` is "internally converted to the percentage of
  `mem total` as reported on startup. `user mem total` is NOT used for the startup calculation
  because that would make the outcome dependent on how filled tmpfs is at that moment." The
  printed `-M`-derived percentage is therefore a *mem-total* percentage while the printed
  `-m`-derived one is a *user-mem-total* percentage; both are the numbers the poll loop compares,
  but they are not the same unit.

Defaults are the built-in `10 / 10 / 5 / 5` (main.c:137-140), and `-m`'s kill value defaults to
`PERCENT/2` (msg.c:200-203), which is why the host's defaults land on 10.00/10.00/5.00/5.00.

## 3. Ready-to-paste `corpus/SOURCES.md` row

Id left as `S???` per the item; the L1 assigns the number. Column shape matches the existing
registry (rows S098–S113 read for shape; `corpus/SOURCES.md:7` is the column-header row, `:104`
is S098 and `:119` is the last row S113 — the item said "S098–S127", but the file ends at S113,
as the meminfo and tag-history seats also found).

```
| S??? | earlyoom main.c at tag v1.9.0 — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h | code | A | earlyoom v1.9.0 startup and poll-loop emission only: the version line, the two effective threshold lines, the low-memory warnings, the dry-run flag, the poll-loop act rule and the -M/-S percent conversion; not kill.c action lines, not meminfo percentage accounting, not host unit state | version line main.c:161; threshold prints main.c:414-417; -M/-S conversion and lower-value merge main.c:346-372; low-memory warnings main.c:519 and :523; dry-run flag main.c:295; poll loop main.c:507-552; act rule main.c:498-504; PRIPCT format msg.h:10; tag v1.9.0 = commit 202d4db0d308ca6478f68de68b46cae34896ddaf; main.c sha256 08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4; msg.h sha256 e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c; opened 2026-10-22 | The two threshold lines print the effective percentages after the -M/-S conversion and the lower-value merge, so a reader of the log sees the thresholds the poll loop will compare against; the printed value is rounded to two decimals and space-padded, so 5.00 renders as a space then 5.00. | mined | 2026-10-22 | on-release | corpus/knowledge/userspace-oom-killers-r26.md |
```

**Tier reason (A):** the release-matched upstream project source, fetched by direct URL from the
canonical `raw.githubusercontent.com` ref, with the byte digest and the tag's commit recorded. It
is primary for what the tool emits about itself; the registry already treats the upstream master
README of the same project as tier A (S016, `corpus/SOURCES.md:22`) and upstream `systemd`
source at a pinned tag as tier A (S011, `corpus/SOURCES.md:19`).

**Status reason (`mined`):** the file is in scope, quotable and useful, and it is the artifact
that answers the round's open question about the effective thresholds. It is not a re-open of a
rejected row, and it does not repeat S016 (different ref, different bytes, different claims).

**Flip (the condition that would reverse this):** if the round's entry cites this row for the
*message grammar* as a whole — the action, escalation and kill-failure prefixes, which live in
`kill.c` — the row's scope is wrong and the entry must cite the `kill.c` row instead. See finding
F2. If the entry cites this row for the *percentage accounting* (what the percentages are
measured against), the `meminfo.c` row is the correct citation; see finding F3.

`used-by` is written as `corpus/knowledge/userspace-oom-killers-r26.md` because the contract
requires that entry's `source:` line to cite at least one row opened in round 26
(`.ufo/waves/round-26/contract.md:24`, and the A1 amendment's `r26_new_source_ids` counter,
`.ufo/waves/round-26/count-c1.sh:12`, which counts S-ids **greater than 113**). If the L1 wires a
different consumer, that cell changes only.

**Validation of the drafted row.** I ran the fleet's own registry validator against a scratch
copy of this row (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file …`):
with the `corpus/knowledge/userspace-oom-killers-r26.md` file present it reports `ok` and exits 0;
without it, it reports `E11 … missing used-by corpus/knowledge/userspace-oom-killers-r26.md` and
exits 1. So the row must land **after or with** the r26 entry, not before it. The scratch dirs
were removed; nothing outside my report file was written.

## 4. Facts the round can rest on (each with its v1.9.0 `main.c` line)

| # | Fact | Line(s) |
|---|---|---|
| A1 | The startup version line is `earlyoom <VERSION>` written to **stderr** with a bare `fprintf`, before any option parsing — the first line earlyoom emits in an invocation. The two threshold lines are likewise printed once, at startup, from `args.mem_term_percent`, `args.swap_term_percent`, `args.mem_kill_percent`, `args.swap_kill_percent`. | 161 (version line; `getopt_long` only starts at 195); 414-415 (term thresholds), 416-417 (kill thresholds) |
| A2 | `VERSION` is a compile-time `-DVERSION=` define, not a runtime string: `Makefile:3` sets `VERSION ?= $(shell GIT_DIR=… git describe --tags --dirty)` and `Makefile:8` passes `-DVERSION=\"$(VERSION)\"`. The Arch package builds with `VERSION=$pkgver` = `1.9.0`, so the token has **no leading "v"**. | Makefile:3, Makefile:8; Arch PKGBUILD:5 (`pkgver=1.9.0`) and :27 (`VERSION=$pkgver earlyoom`) |
| A3 | The **term** line's literal ends with a comma and no trailing period; the **kill** line's literal has **eight leading spaces** and no trailing comma. Both are plain `fprintf(stderr, …)`. | 414 (`… PRIPCT ",\n",`) vs 416 (`"        SIGKILL when mem avail <= "`) |
| A4 | The printed percentages are the **effective** ones: `-M`/`-S` KiB values are converted to percentages at 346-372, *before* the print at 414-417, and the poll loop compares those same fields. | 346-372 (conversion), 414-417 (print), 500-503 (comparison) |
| A5 | When both `-m` and `-M` are given (or `-s` and `-S`), the **lower** of the two percentages is kept, not the later option. The percentage values are bounded: `-m` at 99, `-s` at 100, `-M` at `m.MemTotalKiB * 100 / 99`, `-S` at `m.SwapTotalKiB * 100 / 99`. | 352-353 and 366-367 (merge, `min` helper at 57-62); 205 (`-m` limit), 215 (`-s` limit), 224 (`-M` limit), 233 (`-S` limit) |
| A6 | `-M` converts against `m.MemTotalKiB` and `-S` against `m.SwapTotalKiB`; the runtime percentages are computed against `UserMemTotalKiB` and `SwapTotalKiB`. The `-M` basis differs from the `-m` basis on purpose. | 348, 362 (conversion) vs meminfo.c:112, 115, 117 (accounting); MANPAGE.md:65-70 states the `mem total` choice and its tmpfs rationale |
| A7 | The printed number is formatted by `PRIPCT` = `"%5.2lf%%"` (`msg.h:10`): two decimals, right-aligned in five columns. A value below 10 therefore carries a leading space, so the rendered line has `<=` followed by **two** spaces before `5.00`. | msg.h:10; 414, 416 (uses `PRIPCT`) |
| A8 | The default thresholds are 10/10 (term) and 5/5 (kill), set in the `poll_loop_args_t` initializer; `-m`/`-s` alone give a kill value of `PERCENT/2`; a term value below the kill value is raised to the kill value with a warning. | 137-140; msg.c:200-203 (kill = term/2), msg.c:205-209 (raise term to kill) |
| A9 | The **dry-run** flag line is `dryrun mode enabled, will not kill anything`, emitted once while the `-d`/`--dryrun` option is parsed — i.e. *before* the threshold lines. It goes to **stderr** through `warn()`, which adds a yellow ANSI colour only when stderr is a TTY. | 295 (`warn("dryrun mode enabled, will not kill anything\n")`); msg.c:99-107 (`warn`), msg.c:17-64 (`color_log`, TTY-gated), msg.c:33-45 and 49-52 (colour is dropped when not a TTY) |
| A10 | The low-memory warning comes in two variants and the SIGKILL one is checked first: `low memory! at or below SIGKILL limits: mem <pct>, swap <pct>` and `low memory! at or below SIGTERM limits: mem <pct>, swap <pct>`. Each is immediately preceded by a `mem avail: …` stats line from the same function. | 519-520 (SIGKILL variant), 523-524 (SIGTERM variant), 518 and 522 (the preceding `print_mem_stats(warn, m)`) |
| A11 | A low-memory warning means the limits were crossed, **not** that anything was killed. After printing it, the loop selects the victim, **re-reads** `/proc/meminfo` and **re-evaluates** the limits; if the situation recovered it logs `memory situation has recovered while selecting victim` and kills nothing. | 517-525 (warning), 526-540 (select, re-read at 535, re-evaluate at 536), 537 (recovered message), 539 (the kill) |
| A12 | The act rule is a conjunction on both axes: SIGKILL only when available memory **and** free swap are both at or below their kill limits; SIGTERM when both are at or below the term limits; otherwise nothing. | 498-504 (`lowmem_sig`), 500 (SIGKILL test), 502 (SIGTERM test), 504 (return 0) |
| A13 | The poll loop never returns and re-reads `/proc/meminfo` on every iteration; it sleeps an adaptive 100–1000 ms derived from the headroom to the limits. | 507-508 ("Never returns"), 514-515 (`while (1)` / `parse_meminfo`), 466-491 (`sleep_time_ms`, clamp at 472-473), 545-550 (sleep) |
| A14 | A periodic report line `mem avail: … , swap free: …` is written to **stdout** (via `info()`), while the warnings go to **stderr** (via `warn()`). Both land in the journal under systemd. | 541-543 (`print_mem_stats(info, m)` on stdout), 518 and 522 (`print_mem_stats(warn, m)` on stderr); msg.c:124-131 (`info` → stdout), msg.c:99-107 (`warn` → stderr); meminfo.c:277-285 (the format string) |
| A15 | The startup self-test performs a **signal-free** dry-run kill (`kill_process(args, 0, &victim)`). With `sig == 0` the victim line at `kill.c:627` is printed only when `--debug` is on (the guard is `sig != 0 \|\| enable_debug`), and then its signal name is `0 (no-op signal)`, not `SIGTERM`/`SIGKILL` — so it matches none of the contract's action prefixes either way. No signal is sent: `kill_wait` is called with `sig == 0`, so `kill(pid, 0)` is a liveness check, not a signal. | 64-73 (`startup_selftests`, the `kill_process(args, 0, &victim)` call at 72), kill.c:617-630 (`sig_name` for `sig == 0` at 622-623, the guarded `warn` at 626-629), kill.c:640 and 271-273 and 293 (no signal is sent) |
| A16 | The version line is **not** the first journal entry for the unit. On this host the unit's first entry is systemd's own `Started Early OOM Daemon.` at monotonic 19964370, and earlyoom's version line follows at 19981126. The unit's `ActiveEnterTimestampMonotonic` is 19964362, so **all** 13 unit entries are in scope. | host reads (see §6); unit file `Description=Early OOM Daemon` |
| A17 | The `-S` zero-swap branch is guarded by `m.SwapTotalKiB == 0`, but it is **unreachable in practice**: `parse_term_kill_tuple` is called with the limit `m.SwapTotalKiB * 100 / 99`, which is `0` when there is no swap, so any non-zero `-S` value is rejected first with `value … exceeds limit 0` and `fatal(16)`. I compiled and ran the upstream `msg.c` parser to confirm: `-S 100` with limit 0 → `value 100.000000 exceeds limit 0`; `-S 0` → `both SIGTERM and SIGKILL values are zero`; `-S 0,5` → `value 5.000000 exceeds limit 0`. The "using default percentages" warning therefore never prints on a swapless host. The `-M`/`-S` KiB values use the same `term[,kill]` helper, so a single `-M SIZE` gives a kill value of `SIZE/2`. | 233-240 (the branch), msg.c:136-162 (`parse_part` upper-limit check at 151-155), msg.c:211-215 (both-zero check), msg.c:166-217 (the helper) |

## 5. Flags against the round-26 contract

**F1 — the contract's low-memory line range is imprecise; the two warnings are at `main.c:519`
and `main.c:523`.** The contract writes "`low memory! at or below SIGTERM limits` / `... SIGKILL
limits` → low-memory warning (`main.c:519-523`)"
(`.ufo/waves/round-26/contract.md:88`). The two `warn()` statements are `main.c:519-520`
(SIGKILL limits) and `main.c:523-524` (SIGTERM limits): the range `519-523` covers both
statements' first lines but truncates the SIGTERM statement's argument line (`524`). The grammar
prefixes themselves are correct. The reviewer seat `ReviewContractGrammar`
(`.ufo/waves/round-26/w1/ReviewContractGrammar.md:87,91-92`) independently reached the same
conclusion and proposed `main.c:519,523`. My row uses the precise pair. No contradiction in
substance — a citation-precision defect only.

**F2 — the contract's grammar cites `kill.c` for three lines that my row deliberately does not
cover, and the `kill.c` references the contract gives are correct.** The contract's grammar block
(`contract.md:85-87`) attributes `sending SIGTERM to process ` / `sending SIGKILL to process ` to
`kill.c:627`, `escalating to SIGKILL after ` to `kill.c:318` and `kill failed: ` to `kill.c:654`.
I re-fetched `kill.c` at the tag (sha256 `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3`,
identical to the L1's copy) and checked each line: `kill.c:627` is the
`warn("sending %s to process %d uid %d \"%s\": …")` call, `kill.c:318` is
`warn("escalating to SIGKILL after %.3f seconds\n", secs)`, `kill.c:654` is
`warn("kill failed: %s\n", strerror(saved_errno))`. All three anchors are exact. My row's scope
excludes `kill.c` (the `SrcEarlyoomKillC` seat's territory); the entry should cite that seat's
row for the action/escalation/failure prefixes and mine for the version line, the two threshold
lines, the low-memory warnings and the dry-run flag.

**F3 — the contract's "grammar" is not the same thing as the *effective percentage* a reader
will see, and no contract line claims otherwise; I flag the boundary so the entry does not
overreach.** The contract's C2 interface requires the tool to report `thresholds` as four
percentages taken from the two threshold lines (`contract.md:74-76`). Those numbers are the
effective comparison thresholds (A5), but their *unit* depends on the option path (A7): a
`-m`-derived value is a percentage of `user mem total`, a `-M`-derived value is a percentage of
`mem total`, and the two are not interchangeable even though they print in the same field. On
this host no `-M`/`-S` is configured (the packaged `earlyoom.default` ships only
`EARLYOOM_ARGS="-r 3600"`, and the Arch `PKGBUILD` adds only `-n` and an `--avoid` expression),
so the live thresholds are the defaults 10.00/10.00/5.00/5.00 and the unit question does not
arise here. The entry should not claim a general "percentage of user memory" for the printed
thresholds.

**F4 — the contract's threshold grammar placeholder tolerates the padding only if the reader
strips whitespace after `<=`; the padding is real and I confirmed it on the host.** The contract
writes `sending SIGTERM when mem avail <= <a>% and swap free <= <b>%,` and
`SIGKILL when mem avail <= <c>% and swap free <= <d>%` (`contract.md:83-84`). The literal
`<= ` in the source is followed by `PRIPCT`'s five-column field (A8), so the SIGKILL line reads
`mem avail <=  5.00%` with two spaces. The committed tool already handles this
(`tools/mori-oom-killers.py:103,106` use `<=\s*`), and the frozen cases carry the two-space form
(`tools/fixtures/mori-oom-killers/cases.json`, `c01-host-quiet-thresholds`). No defect to fix — I
record it because a future fixture written from the contract text alone would carry one space and
would silently fail to match. The same applies to the eight leading spaces on the SIGKILL line
(A4): the contract's `contract.md:80-81` says the grammar is "matched after stripping leading
whitespace", which is correct.

**F5 — the contract's dry-run rule (A6) is consistent with the source, and the source adds one
detail the contract does not mention.** The contract's adopted rule A6
(`contract.md:166`) says that when the invocation logged `dryrun mode enabled`, send lines go to
a separate counter and are never positive evidence. The source agrees and explains why:
`kill.c:271-273` (`if (args->dryrun && sig != 0) { warn("dryrun, not actually sending any
signal\n"); return 0; }`) short-circuits before any signal is sent, while the `sending … to
process` line at `kill.c:627` is emitted **before** `kill_wait` is called (`kill.c:640`), so the
log line appears even though nothing was signalled. The contract does not mention the second
message `dryrun, not actually sending any signal` (`kill.c:272`); it is not in the tool's grammar
(`tools/mori-oom-killers.py` has 0 hits for `not actually sending`) and it falls into
`unclassified`, which is the correct outcome — but a future reader of the journal should know
that line exists, since it is the strongest direct evidence that a dry-run invocation sent no
signal.

Two further orderings I checked for the contract's benefit: the dry-run flag line
(`main.c:295`) is printed **during** option parsing, so it precedes the two threshold lines
(`main.c:414-417`) in the journal; and the `sending … to process` victim line (`kill.c:627`)
precedes the `dryrun, not actually sending any signal` line (`kill.c:272`), because `kill_wait`
is called afterwards (`kill.c:640`).

**F6 — nothing in the contract's C1 or C2 wording is contradicted by `main.c`.** I re-checked the
contract's host claims independently and they hold: `systemctl show earlyoom.service -p
LoadState,ActiveState,UnitFileState,ActiveEnterTimestampMonotonic` →
`LoadState=loaded`, `ActiveState=active`, `UnitFileState=enabled`,
`ActiveEnterTimestampMonotonic=19964362`; `systemctl show systemd-oomd.service` →
`loaded`/`inactive`/`disabled`. `main.c` says nothing about unit state, so it neither supports
nor contradicts C1's host reading. The contract's `earlyoom <version>` rule (`contract.md:82`)
and `main.c:161` agree, including the `VERSION` build-time origin (A2): the installed binary
prints `earlyoom 1.9.0` with no leading "v" (`/usr/bin/earlyoom -v` → `earlyoom 1.9.0`;
`pacman -Q earlyoom` → `earlyoom 1.9.0-1`; the live journal line is `earlyoom 1.9.0`). The
`SrcEarlyoomReadme` seat reached the same conclusion from the README side (its F3).

**F7 — the version line is not the first journal entry for the unit, so "the first line of an
invocation" must mean earlyoom's own first line.** The contract says
"`earlyoom <version>` → version (the first line of an invocation; `main.c:161`)"
(`contract.md:82`). That is true of earlyoom's own output: `main.c:161` is the first `fprintf`
in `main()` and precedes the getopt loop at 195. But on this host the unit's **first journal
entry** is systemd's own `Started Early OOM Daemon.` (monotonic 19964370), and earlyoom's
version line follows at 19981126 (A17). The tool's scope rule
(`__MONOTONIC_TIMESTAMP` ≥ `ActiveEnterTimestampMonotonic` = 19964362) therefore admits both, and
the systemd message classifies as `unclassified`. No rule is broken, but the phrase "first line
of an invocation" should be read as "earlyoom's first line", not "the unit's first line".

**F8 — the ANSI colour question is settled in favour of plain text, and the entry should say so
rather than leave it open.** `warn()` writes a yellow escape sequence when stderr is a TTY
(`msg.c:99-107` with `msg.c:17-64`), which would break a prefix-anchored grammar match on a
terminal. Under systemd, stderr is not a TTY, so `color_log` drops the colour (`msg.c:49-52`).
I confirmed on the host: `systemctl show earlyoom.service -p StandardOutput -p StandardError` →
`StandardOutput=journal`, `StandardError=inherit`, and **0** of the 13 unit journal entries
contain an escape byte. The contract's prefix-anchored grammar (`contract.md:80-81`) is
therefore sound for this host's journal, and the entry can state that the lines are plain text.

## 6. Host-side corroboration (read-only, count-only, no MESSAGE text)

I ran the contract's own journal scope to check that the grammar `main.c` emits is what the host
actually emits. Counts and the two threshold values only; no process name, uid, command line or
avoid/prefer expression is reproduced here (the `--prefer`/`--avoid` regex echoes at
`main.c:379`/`386` are visible in the journal and are deliberately not quoted).

```
journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE,__MONOTONIC_TIMESTAMP
  → 13 boot lines for the unit; all 13 have __MONOTONIC_TIMESTAMP >= 19964362 (ActiveEnterTimestampMonotonic)
  → by class: 1 version line, 1 term-threshold line, 1 kill-threshold line,
                0 "sending SIG…to process", 0 "escalating to SIGKILL",
                0 "kill failed", 0 "low memory!", 0 "dryrun",
                10 other (1 systemd "Started Early OOM Daemon." + 1 mem-total line
                + 1 prefer echo + 1 avoid echo + 6 periodic "mem avail:" reports)
  → the term-threshold line carries 10.00 / 10.00 and the kill-threshold line 5.00 / 5.00,
    matching the built-in defaults at main.c:137-140
  → the kill-threshold line is rendered with TWO spaces after "<=" ("mem avail <=  5.00%"),
    confirming the %5.2lf padding of msg.h:10 (A8)
  → 0 entries contain an ANSI escape byte (F8)
```

This is corroboration for the tool and case seats, not a claim of my own: I did not build or run
`tools/mori-oom-killers.py` and I did not write to the cases file.

## 7. Side files opened, and one upstream fact that does not belong to this row

`earlyoom.default` (sha256 `c0770413…984a2`) at the tag ships `EARLYOOM_ARGS="-r 3600"` at line
5; the Arch `PKGBUILD` (sha256 `f48dc3f9…4dd4a2`) rewrites that file at line 22 to append
`-n` and an `--avoid` expression, and builds with `VERSION=$pkgver` at line 27. I record these as
provenance for the *host configuration* claim in F6 and for the `VERSION` origin in A2; they are
**not** part of my row's scope and my row cites neither file.

`meminfo.c` is cited in A7 only as the counterpart of the conversion basis; the percentage
accounting itself belongs to the `SrcEarlyoomMeminfo` seat's row, and my row explicitly excludes
it. `kill.c` is cited in F2 only for the contract's anchor check; the action/escalation/failure
prefixes belong to the `SrcEarlyoomKillC` seat's row.

## 8. Tooling and environment

No tool was installed or upgraded by this seat: the task needed only `curl`, `python3`,
`sha256sum`, `gcc` and `git` (read-only `ls-remote`). Per the operator directive I would have
installed through pacman/uv, but the host-wide pacman pause in the round-26 item bounds makes
pacman unavailable, and no missing tool blocked the work, so nothing was installed. Nothing needs
installing for the L1. Versions used: curl 8.23.0, Python 3.14.8, git 2.56.0, gcc (system),
sha256sum (GNU coreutils) 0.8.0.

I compiled the upstream `msg.c` + `globals.c` (tag bytes, sha256 as in §1) in a scratch directory
under `/tmp` to execute `parse_term_kill_tuple` directly for A19, then removed the scratch
directory. No repo file was written, and no upstream source was modified.

## 9. Out of scope for this seat

The C1 rewrite of `corpus/knowledge/userspace-oom-killers-r12.md`, the r26 entry text, the tool
and its fixtures, the registry id allocation, and any row other than the one in §3 are L1 or
sibling-seat work; I report the facts and let the owner act. I did not edit any file in the
lane other than this report.
