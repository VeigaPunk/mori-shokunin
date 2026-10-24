# SrcEarlyoomMeminfo — SOURCES row draft (earlyoom v1.9.0 `meminfo.c` + `meminfo.h`)

Scope: open the earlyoom v1.9.0 memory-accounting source at the released tag and answer three
questions: how the `mem avail` and `swap free` percentages are computed (MemAvailable or a
fallback), what `user mem total` is, and what the fatal exit codes 102–104 mean. Draft one
`corpus/SOURCES.md` row plus its Gate. `corpus/SOURCES.md` was **not** edited (draft only).
No lane commit, no jj command, no product-code edit, no unit touched.

## Verdict in one line

`mem avail %` is a share of **`user mem total`** (`MemAvailable` + `AnonPages`), not of
`MemTotal`; `MemAvailable` falls back to `MemFree + Cached + Buffers - Shmem` on kernels without
it; `swap free %` is a share of total swap and is `0` when there is no swap; and a
`/proc/meminfo` read problem is **fatal** (102 open, 103 read, 104 missing entry), never a quiet
zero.

## Facts the round can rest on (each with its line number)

1. `MemAvailable` is read from `/proc/meminfo` by a **non-fatal** lookup —
   `meminfo.c:101` `m.MemAvailableKiB = get_entry("MemAvailable:", buf);`. The lookup is a plain
   substring search over the file buffer (`meminfo.c:25` `char* hit = strstr(buf, name);`) that
   returns `-ENODATA` when the name is absent (`meminfo.c:26-28`).
2. When that lookup yields a negative value, earlyoom uses a **guesstimate** and warns once —
   `meminfo.c:102-103` (`if (m.MemAvailableKiB < 0) { m.MemAvailableKiB = available_guesstimate(buf);`),
   warning text at `meminfo.c:105-106` "Warning: Your kernel does not provide MemAvailable data
   (needs 3.14+)". The guesstimate formula is `meminfo.c:60`
   `return MemFree + Cached + Buffers - Shmem;` over `Cached:`, `MemFree:`, `Buffers:`, `Shmem:`
   read at `meminfo.c:55-58`. The kernel-version note is at `meminfo.c:51-52`.
3. The four entries read fatally are `MemTotal:`, `SwapTotal:`, `AnonPages:`, `SwapFree:` —
   `meminfo.c:96-99`, each through `get_entry_fatal` (`meminfo.c:41-49`).
4. **`user mem total`** is `UserMemTotalKiB = MemAvailableKiB + AnonPagesKiB` —
   `meminfo.c:112`. The struct comment states the intent: `meminfo.h:18-19`
   "UserMemTotalKiB = MemAvailableKiB + AnonPagesKiB." / "Represents the total amount of memory
   that may be used by user processes." The manual gives the same definition and the version that
   introduced it: `MANPAGE.md:33-34` "`user mem total`, introduced in earlyoom v1.8, is the memory
   accessible by userspace (`MemAvailable`+`AnonPages` as reported in `/proc/meminfo`)." The
   changelog entry is `README.md:299-300` (v1.8, 2024-04-15).
5. **`mem avail %`** is `MemAvailablePercent = MemAvailableKiB * 100 / UserMemTotalKiB` —
   `meminfo.c:115`. The denominator is *user mem total*, **not** `MemTotalKiB`. The threshold
   comparison uses that field: `main.c:500` and `main.c:502`.
6. The struct comment above that field is stale relative to the code: `meminfo.h:22`
   `double MemAvailablePercent; // percent of total memory that is available` — since v1.8 the
   denominator is `UserMemTotalKiB` (`meminfo.c:115`), as `README.md:300` records. A reader must
   take the code, not that comment.
7. **`swap free %`** is `SwapFreePercent = SwapFreeKiB * 100 / SwapTotalKiB` —
   `meminfo.c:117`, and it is forced to `0` when there is no swap —
   `meminfo.c:116` `if (m.SwapTotalKiB > 0) {` … `meminfo.c:119` `m.SwapFreePercent = 0;`. The
   comparison field is `main.c:500`/`:502` (`m->SwapFreePercent`).
8. [INFERENCE] With `SwapTotalKiB == 0`, `SwapFreePercent` is `0` (`meminfo.c:119`), which is at or
   below any non-negative swap threshold, so the swap half of the conjunction in `main.c:500`/`:502`
   is always satisfied and the decision rests on memory alone. earlyoom separately warns about a
   zero swap total for the `-S` option (`main.c:238`).
9. The `-m`/`-M`/`-s`/`-S` **thresholds** are denominated differently from the runtime
   percentages: `-M` (KiB) is converted against `MemTotalKiB` (`main.c:348-349`) and `-S` against
   `SwapTotalKiB` (`main.c:362-363`), while the printed `mem avail` percentage is over
   `UserMemTotalKiB`. The manual says so: `MANPAGE.md:66-70` "the percentage of `mem total` as
   reported on startup. `user mem total` is NOT used for the startup calculation". The threshold
   line itself (`main.c:412-417`) therefore does not by itself reveal which denominator the
   operator configured; the startup line `main.c:412` ("mem total: … user mem total: … swap
   total: …") reports both totals.
10. **Fatal exit codes.** `fatal(code, …)` prints `fatal: <message>` to stderr and exits with that
    code — `msg.c:86-95` (`snprintf(fmt2, sizeof(fmt2), "fatal: %s", fmt);` at `:90`,
    `exit(code);` at `:95`). The three meminfo exits are:
    - **102** — could not open `/proc/meminfo`: `meminfo.c:84`
      `fatal(102, "could not open /proc/meminfo: %s\n", strerror(errno));`
    - **103** — could not read `/proc/meminfo`: `meminfo.c:90` (read error) and `meminfo.c:93`
      (`fatal(103, "could not read /proc/meminfo: 0 bytes returned\n");`)
    - **104** — a required entry is missing: `meminfo.c:46`
      `fatal(104, "could not find entry '%s' in /proc/meminfo: %s\n", name, strerror((int)-val));`
      (covers `MemTotal:`, `SwapTotal:`, `AnonPages:`, `SwapFree:` at `meminfo.c:96-99` and the
      guesstimate inputs at `meminfo.c:55-58`).
11. The manual documents exactly those three — `MANPAGE.md:244` "102: Could not open /proc/meminfo",
    `MANPAGE.md:246` "103: Could not read /proc/meminfo", `MANPAGE.md:248` "104: Could not find a
    specific entry in /proc/meminfo".
12. **Discrepancy between the manual and the code at v1.9.0:** the manual also lists
    `MANPAGE.md:250` "105: Could not convert number when parse the contents of /proc/meminfo", but
    no `fatal(105)` exists in the v1.9.0 tree. A numeric conversion failure returns `-errno` from
    `get_entry` (`meminfo.c:32-36`), and for the four required entries that negative value reaches
    `get_entry_fatal` and exits **104** (`meminfo.c:44-47`), while for `MemAvailable:` the same
    negative value only triggers the guesstimate and a warning (`meminfo.c:101-103`). So at
    v1.9.0 a malformed number surfaces as 104 (required entries) or as a guesstimate
    (`MemAvailable:`), never as 105.
13. Because 102/103/104 end the process, an earlyoom that dies this way leaves **no** version line
    and **no** threshold line in the journal — the absence of those lines is the observable
    consequence, not a quiet zero. [INFERENCE] The journal confirms the inverse on this host: the
    version line `earlyoom 1.9.0` precedes the threshold lines, so both are present when the
    reader starts normally.
14. Percentages are printed with `PRIPCT` = `"%5.2lf%%"` (`msg.h:10`), i.e. width 5, two decimals.
    A value below 10 is space-padded, so the raw threshold text is e.g.
    `mem avail <=  5.00%` (two spaces after `<=`) while `10.00%` has none. This host's journal
    shows both shapes.
15. The startup summary line prints both denominators —
    `main.c:412-413` `fprintf(stderr, "mem total: %4lld MiB, user mem total: %4lld MiB, swap
    total: %4lld MiB\n", m.MemTotalKiB / 1024, m.UserMemTotalKiB / 1024, m.SwapTotalKiB / 1024);`
    and the periodic report prints `mem avail: <avail> of <user mem total> MiB (<pct>), swap free: …`
    — `meminfo.c:277-285` (`m.UserMemTotalKiB / 1024` at `meminfo.c:281`).
16. Version-pinning matters: upstream `master` (commit `8477c902fce09be26e5668acba05df216871e7ae`,
    the commit pinned by the existing row S016) is **newer than** the v1.9.0 tag and differs in
    exactly this file's fatal behaviour — at `master` `SwapFree:` is read non-fatally and a bogus
    value is warned about instead of aborting, while at tag v1.9.0 `meminfo.c:99` is
    `m.SwapFreeKiB = get_entry_fatal("SwapFree:", buf);`. Anchors in this row are tag-only.
17. This host runs the same upstream release: `pacman -Qi earlyoom` → version `1.9.0-1`, and the
    binary prints `earlyoom 1.9.0`; the journal line shapes observed here match the code
    (`sending SIGTERM when mem avail <= 10.00% and swap free <= 10.00%,`,
    `        SIGKILL when mem avail <=  5.00% and swap free <=  5.00%`,
    `mem total: 30978 MiB, user mem total: 28862 MiB, swap total: 30979 MiB`). No process name,
    command line, uid, or `--avoid`/`--prefer` expression was copied.

## Draft row (exact column order of `corpus/SOURCES.md`)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S??? | earlyoom v1.9.0 memory accounting — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.c ; https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.h | code | A | how earlyoom computes the two percentages its thresholds compare against and the fatal exits of its `/proc/meminfo` reader: the `MemAvailable` source and its fallback, the `user mem total` denominator, the swap-free denominator, and the 102/103/104 exits; v1.9.0 tag only; not the `main.c`/`kill.c` message grammar, not host service state, not kill history, not the manual's exit-status table | meminfo.c:101 (`MemAvailable:` read), :102-106 (guesstimate + warning), :60 (guesstimate formula), :55-58 and :96-99 (fatally read entries), :112 (`UserMemTotalKiB`), :115 (`MemAvailablePercent`), :116-119 (`SwapFreePercent`), :46 (fatal 104), :84 (fatal 102), :90 and :93 (fatal 103); meminfo.h:18-23 (struct fields and the stale `percent of total memory` comment); tag v1.9.0 = commit 202d4db0d308ca6478f68de68b46cae34896ddaf; raw sha256 meminfo.c 526e512c89c58cb0b1db2ae98ea62d287cdc1516846be80c9173bdc4bf0edfeb, meminfo.h 5b709094c507ba418a5284034614141bd48893b5a8fe1863214c46396aefb52f; HTTP 200 on 2026-10-22 | The `mem avail` percentage is a share of `user mem total` (`MemAvailable`+`AnonPages`), not of `MemTotal`; `MemAvailable` falls back to `MemFree`+`Cached`+`Buffers`-`Shmem` when the kernel lacks it; `swap free` is a share of total swap and is 0 when there is no swap; a `/proc/meminfo` read failure is fatal, not a quiet zero. | mined | 2026-10-22 | on-release | corpus/knowledge/userspace-oom-killers-r26.md |

Tier A — reason: upstream release source code at a released tag (`v1.9.0`, commit
`202d4db0d308ca6478f68de68b46cae34896ddaf`), fetched from the project's own raw endpoint with the
bytes hashed, and the same upstream release is what this host runs (`earlyoom 1.9.0-1`); the
observed host journal line shapes match the code line for line.

Status `mined` — reason: these facts are what the superseding round-26 entry
`corpus/knowledge/userspace-oom-killers-r26.md` and the C2 tool's threshold semantics rest on, so
the row has a consumer this round. (If the L1 prefers the registry's "admitted but not yet used"
spelling, the same row text with status `queued` and used-by `—` is equally consistent; the
facts and the Gate do not change.)

Split option — the registry keeps one row per URL for code files (S011, S013). If the L1 wants
that shape, the row above splits into two rows with the same cells: the `meminfo.c` row keeps the
code as its source and the anchors `:46, :55-58, :60, :84, :90, :93, :96-99, :101-106, :112, :115,
:116-119`; the `meminfo.h` row keeps the header as its source and the anchors `:18-23`. Both are
tier A and `on-release`.

Registry note — `corpus/SOURCES.md` currently holds **113** registry rows, the last one `S113`
(file line 119). The assignment text mentions "the last rows S098–S127"; rows **S114–S127 do not
exist yet**, so the next free id is `S114`. The row above keeps the id as `S???` as instructed;
the L1 assigns the final number.

## Gate

Source 1 — `meminfo.c`

- URL: https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.c
- Access date: 2026-10-22 (HTTP 200)
- Bytes: 8,344 B, 286 lines; sha256
  `526e512c89c58cb0b1db2ae98ea62d287cdc1516846be80c9173bdc4bf0edfeb`
- Tag provenance: `refs/tags/v1.9.0` → tag object
  `66d78843fd675859a09a52d3f17b1c408a827a34` → commit
  `202d4db0d308ca6478f68de68b46cae34896ddaf`
- Quote, `meminfo.c:115` (verbatim, 13 words):
  > `m.MemAvailablePercent = (double)m.MemAvailableKiB * 100 / (double)m.UserMemTotalKiB;`
- Quote, `meminfo.c:112` (verbatim, 5 words):
  > `m.UserMemTotalKiB = m.MemAvailableKiB + m.AnonPagesKiB;`
- Quote, `meminfo.c:60` (verbatim, 7 words):
  > `return MemFree + Cached + Buffers - Shmem;`
- Quote, `meminfo.c:84` (verbatim, 8 words):
  > `fatal(102, "could not open /proc/meminfo: %s\n", strerror(errno));`
- Quote, `meminfo.c:46` (verbatim, 10 words):
  > `fatal(104, "could not find entry '%s' in /proc/meminfo: %s\n", name, strerror((int)-val));`

Source 2 — `meminfo.h`

- URL: https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.h
- Access date: 2026-10-22 (HTTP 200)
- Bytes: 1,341 B, 49 lines; sha256
  `5b709094c507ba418a5284034614141bd48893b5a8fe1863214c46396aefb52f`
- Tag provenance: same tag/commit as Source 1
- Quote, `meminfo.h:18-19` (verbatim, 19 words):
  > `// UserMemTotalKiB = MemAvailableKiB + AnonPagesKiB.`
  > `// Represents the total amount of memory that may be used by user processes.`
- Quote, `meminfo.h:22` (verbatim, 8 words):
  > `double MemAvailablePercent; // percent of total memory that is available`
- Quote, `meminfo.h:23` (verbatim, 7 words):
  > `double SwapFreePercent; // percent of total swap that is free`

Corroborating sources (not new rows; cited for the exit-status and format facts)

- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md — 2026-10-22, HTTP 200,
  10,114 B, 288 lines, sha256
  `cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda`.
  Quotes: `:244` "102: Could not open /proc/meminfo"; `:248` "104: Could not find a specific entry
  in /proc/meminfo"; `:31` "set available memory minimum to PERCENT of `user mem total` (default
  10 %)."
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.c — 2026-10-22, HTTP 200, 6,864 B,
  sha256 `a771c91529053341c290ede2a7df1d9fdf16e07fb9584db8a64604a45dea5197`. Quote `:95`
  "exit(code);"
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h — 2026-10-22, HTTP 200, 1,027 B,
  sha256 `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c`. Quote `:10`
  `#define PRIPCT "%5.2lf%%"`
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c — 2026-10-22, HTTP 200,
  21,053 B, sha256 `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4`. Quotes
  `:412` `fprintf(stderr, "mem total: %4lld MiB, user mem total: %4lld MiB, swap total: %4lld MiB\n",`
  and `:500` `if (m->MemAvailablePercent <= args->mem_kill_percent && m->SwapFreePercent <= args->swap_kill_percent)`.
- https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c — 2026-10-22, HTTP 200, 21,169 B,
  sha256 `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3`. Quote `:627` the
  `sending %s to process %d uid %d "%s"` action line.

## Flags for the L1 / contract

- **No contradiction with the contract.** Every contract line number that this seat could check
  against the v1.9.0 bytes holds: `main.c:161` (version line), `main.c:414`/`:416` (threshold
  lines), `kill.c:627` (action line), `kill.c:318` (escalation), `kill.c:654` (kill failed),
  `main.c:519-523` (low-memory warnings), `main.c:295` (dryrun). The contract's grammar shapes
  also survive the `PRIPCT` padding: percentages are `"%5.2lf%%"` (`msg.h:10`), so the raw text
  can carry a space-padded number (e.g. `<=  5.00%`).
- **The contract's threshold grammar is silent on the denominator, and the denominator matters.**
  The C2 tool reports `thresholds` numbers taken from the journal threshold line
  (`main.c:414`/`:416`). Those numbers are *configured* percentages; the runtime comparison
  (`main.c:500`/`:502`) is against `MemAvailablePercent`, whose denominator is `user mem total`
  (`meminfo.c:115`), while the `-M`/`-S` conversions use `MemTotalKiB`/`SwapTotalKiB`
  (`main.c:348-349`, `:362-363`; `MANPAGE.md:66-70`). The r26 entry should say which denominator
  the reported threshold refers to, or say that the journal line does not disclose it (fact 9).
- **A stale upstream comment is a live trap.** `meminfo.h:22` still says "percent of total memory
  that is available", but the code divides by `UserMemTotalKiB` (`meminfo.c:115`). If the r26
  entry or the tool's comments copy the comment, the entry states a denominator the code does not
  use. Suggest the entry cite `meminfo.c:115` and `meminfo.h:18-19` instead.
- **The manual lists an exit code the v1.9.0 code cannot produce.** `MANPAGE.md:250` lists 105;
  no `fatal(105)` exists in the v1.9.0 tree and a conversion failure exits 104 (or takes the
  guesstimate path). The r26 entry should not list 105 as an earlyoom exit code, and the tool
  should not key on it.
- **Fatal-vs-quiet is the C2-relevant consequence.** 102/103/104 terminate earlyoom, so a host
  whose earlyoom died on one of them shows no version line and no threshold line at all. The C2
  verdicts already separate "unavailable" from "zero"; this row gives the reason the two are
  different (facts 10 and 13).
- **A startup self-test line exists that is not an action.** `kill.c:617-624` can render
  `sending 0 (no-op signal) to process …` (the startup self-test at `main.c:67-72`,
  `main.c:419`), printed only when debug is enabled (`kill.c:626` "sig == 0 is used as a
  self-test during startup. Don't notify the user."). It does not match the contract's
  signal-specific action prefixes (`sending SIGTERM to process ` / `sending SIGKILL to process `),
  so it cannot be miscounted — but a matcher that keyed on the bare `sending ` prefix would
  miscount it. Worth one line in the C2 knowledge entry; the landed tool is safe as written.
- **Tag pinning is load-bearing.** At upstream `master` (`8477c902…`, the commit behind the
  existing row S016) `SwapFree:` is read non-fatally and a bogus value is warned about; at tag
  v1.9.0 it is `get_entry_fatal` (`meminfo.c:99`) and a missing entry exits 104. Anchors and
  exit-code claims in this round must name the tag, not master.
- **Adjacency, not absorption.** S016 (earlyoom README at `8477c902…`) stays valid and is not
  superseded by this row: it covers the README and master; this row covers the tagged code.
  The v1.9.0 README is a different byte sequence from S016's pinned README (sha256
  `23411dbfd8b409d433f984a5d6677830e86a383ec76935fc1e1d675e6b4374dd` vs
  `b2a34e354d122fd756672a1a4014ec5382144e41451291c9d84fd6458c30826c`), so the two rows do not
  duplicate each other.
- **Coverage left open (other seats / not claimed here):** the `main.c`/`kill.c` message grammar
  in full, the systemd-oomd side at v262 (SOURCES row for `src/oom/oomd-util.c` is a sibling
  seat's scope), any host kill history, and any host-wide unit census. This row says nothing
  about whether earlyoom ever killed anything on this host.

## Verification trail

- `curl -sS -o meminfo.c -w '%{http_code} %{size_download}' https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/meminfo.c`
  → `200 8344`; `sha256sum` → `526e512c…edfeb` (as recorded). Same for `meminfo.h` → `200 1341`,
  `5b709094…b52f`; `MANPAGE.md` → `200 10114`, `cc48b02e…dfeda`; `msg.c` → `200 6864`,
  `a771c915…5197`; `msg.h` → `200 1027`, `e3660498…de56c`; `main.c` → `200 21053`,
  `08656b0b…d0e4`; `kill.c` → `200 21169`, `b32e0fad…0bf3`; `Makefile` → `200 2898`,
  `b852cb9b…27ae`; `globals.h` → `200 133`, `8cc122f9…8668`; `globals.c` → `200 127`,
  `a8b8fb8f…159b5`; `proc_pid.c` → `200 2682`, `e5b65446…12d5`; `proc_pid.h` → `200 312`,
  `b8adf99f…dcd90`; `kill.h` → `200 1440`, `abf8577b…b0d78`. All fetched 2026-10-22.
- `git ls-remote https://github.com/rfjakob/earlyoom` → `refs/tags/v1.9.0` =
  `66d78843fd675859a09a52d3f17b1c408a827a34`, peeled `refs/tags/v1.9.0^{}` =
  `202d4db0d308ca6478f68de68b46cae34896ddaf`, `refs/heads/master` =
  `8477c902fce09be26e5668acba05df216871e7ae`.
- `curl -sS https://raw.githubusercontent.com/rfjakob/earlyoom/8477c902fce09be26e5668acba05df216871e7ae/meminfo.c`
  → sha256 `e365e1f48cdf47904f93c03a1b4fe44e91668bac0797690d0511664d4255fa6a`;
  `diff -u` against the tag file shows the master-only `SwapFree:` tolerance block and the
  `strtoll` warning rewording — the tag/master difference behind fact 16.
- `grep -n "fatal(" *.c` over the fetched v1.9.0 sources → no `fatal(105)`; the only meminfo
  exits are `102` (`meminfo.c:84`), `103` (`:90`, `:93`), `104` (`:46`).
- `grep -n "" meminfo.c` / `meminfo.h` / `MANPAGE.md` / `msg.c` / `msg.h` / `main.c` / `kill.c`
  → every line number quoted above was read from the fetched bytes.
- Host (read-only): `pacman -Qi earlyoom` → `Version: 1.9.0-1`; `systemctl show earlyoom.service
  -p LoadState,ActiveState,UnitFileState,ActiveEnterTimestampMonotonic` → `loaded`, `active`,
  `enabled`, `19964362`; `systemctl show earlyoom.service -p ActiveEnterTimestamp` → `Thu 2026-10-22
  04:55:44 -03`; `systemctl show systemd-oomd.service -p LoadState,ActiveState,UnitFileState` →
  `loaded`, `inactive`, `disabled`. Journal read used only the `MESSAGE` and
  `__MONOTONIC_TIMESTAMP` fields; journal lines were classified by prefix, and the
  `--prefer`/`--avoid` regex lines were counted but never reproduced. No process name, command
  line or uid was copied. No unit was started, stopped, enabled or restarted; no journal entry was
  edited or removed.

## Out of scope

- Editing `corpus/SOURCES.md`, `corpus/knowledge/userspace-oom-killers-r12.md`,
  `corpus/knowledge/userspace-oom-killers-r26.md` or any other lane file (draft only).
- The `main.c`/`kill.c` message grammar in full and the `tools/mori-oom-killers.py` interface
  (other seats' scope).
- Host kill history, host-wide unit census, and the C1/C2 claim counting.
- The systemd v262 side (sibling seat's scope) and the sibling tsukuroi lane entry.

## Tooling

- No install, upgrade or downgrade was performed; no tool was needed beyond what the host already
  provides (`curl`, `git ls-remote`, `python3` for JSON parsing, `grep`, `sed -n`, `awk`, `cmp`,
  `diff`, `wc`, `sha256sum`, `journalctl`, `systemctl show`).
- All pacman transactions are PAUSED host-wide per the round bounds, so none was attempted.
- Scratch copies of the fetched bytes live under
  `/fast/scratch/hyaku/mori-r26/MoriR26.SrcEarlyoomMeminfo/` (`meminfo.c`, `meminfo.h`, `MANPAGE.md`,
  `msg.c`, `msg.h`, `main.c`, `kill.c`, `Makefile`, `globals.c`, `globals.h`, `proc_pid.c`,
  `proc_pid.h`, `kill.h`, `tree.json`, plus the `8477c902` comparison copies).
- Writes: this report file only. No jj command was run anywhere; no git write command was run in
  the lane; no lane commit was made; no sibling lane was touched.
