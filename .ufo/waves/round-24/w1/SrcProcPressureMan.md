# Round 24 wave 1 — seat SrcProcPressureMan — proc_pressure(5) source row

Seat: `MoriR24.SrcProcPressureMan` (scribe, leaf, no dispatch).
Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Claim covered: C2 (coverage) sourced step — one SOURCES.md row for the proc_pressure(5)
manual page.

**Headline finding: the assigned URL does not exist.** `https://man7.org/linux/man-pages/man5/proc_pressure.5.html`
returned `HTTP 404 Not Found` on 2026-10-22, and the man-pages project has never
published a `proc_pressure` page (checked in the current release, man-pages 6.20,
released 2026-10-21). No row can honestly be *mined* from that URL. The draft row
below is therefore a **rejected provenance record**, not a support row, and the C2
sourced list must drop `proc_pressure(5)`.

## What I ran (commands and observed output)

Fetch of the assigned URL, with UTC clock around the request:

```
$ date -u +"%Y-%m-%dT%H:%M:%SZ"      # 2026-10-22T08:21:46Z
$ curl -sS -L --max-time 60 -D headers_404.txt -o body_404.html \
      -w "http_code=%{http_code} size=%{size_download} time_total=%{time_total}\n" \
      https://man7.org/linux/man-pages/man5/proc_pressure.5.html
http_code=404 size=196 time_total=0.644408
$ date -u +"%Y-%m-%dT%H:%M:%SZ"      # 2026-10-22T08:21:47Z
```

Response headers (`headers_404.txt`):

```
HTTP/1.1 404 Not Found
Date: Thu, 22 Oct 2026 08:21:47 GMT
Server: Apache/2.4.58 (Ubuntu)
Content-Length: 196
Content-Type: text/html; charset=iso-8859-1
```

Fetched bytes, digest and line anchors:

```
$ sha256sum body_404.html
80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880  body_404.html
```

- SHA256 of the fetched bytes, first 16 hex: **`80c3fe2ae1062abf5`** (full:
  `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`).
- Fetched body is 196 bytes, 7 lines. Anchors verified in the fetched bytes:
  line 3 `<title>404 Not Found</title>`, line 5 `<h1>Not Found</h1>`, line 6
  `<p>The requested URL was not found on this server.</p>`.
- Access date/time (UTC): **2026-10-22T08:21:46Z → 2026-10-22T08:21:47Z**
  (server `Date:` header agrees: 08:21:47 GMT). An earlier independent fetch at
  2026-10-22T08:15:27Z returned the same 404 with the same 196-byte body and the
  same SHA256, so the digest is stable across two fetches.

### Cross-checks that the page does not exist

1. Upstream source tree (raw.githubusercontent, master HEAD):
   `https://raw.githubusercontent.com/mkerrisk/man-pages/master/man/man5/proc_pressure.5.html`
   → `http_code=404`.
2. man7 man5 section index (fetched, 274644 bytes): `grep -io "[a-z0-9_.-]*pressure[a-z0-9_.-]*"`
   returns **no match**; the index contains `proc.5.html`, `proc_meminfo.5.html`,
   `proc_diskstats.5.html`, … but no `proc_pressure` entry.
3. man-pages release tarball (current release):
   `https://mirrors.edge.kernel.org/pub/linux/docs/man-pages/man-pages-6.20.tar.xz`
   (1914692 bytes, sha256 `180f0d16a2142dd9671760ac0afeadcc25e861f695eb420293e1206a87ca083f`).
   `tar -tJf man-pages-6.20.tar.xz | grep -i pressur` → no output (exit 1).
   `grep -rl "/proc/pressure" man-pages-6.20/man/` → no output. `grep -rli "pressure stall" man-pages-6.20/man/` → 0 files.
   `man-pages-6.20/Changes` line 1: `Released: 2026-10-21, Dongo`.
4. `proc(5)` on man7 (fetched, 31125 bytes) — the nearest man page by name — contains
   zero occurrences of `pressure`, `stall` or `PSI`; it does not document
   `/proc/pressure`.
5. URL variants, all 404: `.../man5/proc_pressure.5`, `.../man5/proc-pressure.5.html`,
   `.../man5/psi.5.html`, `.../man5/proc_pressure.html`.
6. Independent web search: "proc_pressure(5) man page" returns no such man page; the
   `/proc/pressure` interface is documented by the kernel PSI documentation
   (`docs.kernel.org/accounting/psi.html`) and by the kernel `/proc` documentation.

## Duplicate and supersession check against corpus/SOURCES.md

Checked `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` (89 rows,
last id S089):

- `grep -c "proc_pressure" corpus/SOURCES.md` → **0**. No row carries this URL or this
  page name.
- `grep -n "man-pages/man5" corpus/SOURCES.md` → no match. The registry holds two
  man-pages rows only: S027 (`man2/pidfd_open.2.html`) and S031 (`man7/pipe.7.html`).
- Pressure-adjacent rows that do exist: **S001** `PSI - Pressure Stall Information —
  https://docs.kernel.org/accounting/psi.html` (docs, tier A, scope: "Linux PSI
  counters, totals, thresholds and per-cgroup files", status mined) and **S002**
  `Control Group v2 — https://docs.kernel.org/admin-guide/cgroup-v2.html` (docs, tier A,
  scope: cgroup-v2 memory events, memory.peak and local versus hierarchical scope,
  status mined). S010 (`systemd.io/PRESSURE/`) is a systemd-side pressure consumer.

**Verdict: the drafted row is a NEW row, and it supersedes nothing.** It cannot
supersede S001 or S002 (it carries no content), and S001/S002 do not cover the assigned
URL either, so there is no pre-existing row to retire. The registry's scope for
"/proc/pressure file format" is already held by S001 (rendered kernel docs) and, from
this round, by the kernel v7.2 raw PSI documentation row owned by seat `SrcPsiRst`;
S002 owns the cgroup-v2 pressure-file scope. A man-page row would have been a third
row for the same scope had the page existed.

## Draft row (exact 11-cell shape; id left as S0xx for the L1)

Draft only — `corpus/SOURCES.md` was **not** edited.

```
| S0xx | proc_pressure(5) candidate manual page — https://man7.org/linux/man-pages/man5/proc_pressure.5.html | docs | C | candidate manual page for the /proc/pressure file format — no such page exists in the man-pages project (current release 6.20, 2026-10-21) | HTTP 404 Not Found fetched 2026-10-22T08:21:47Z; body 196 bytes, sha256 80c3fe2ae1062abf5; man-pages 6.20 contains no man5/proc_pressure page and no page mentioning /proc/pressure; proc(5) on man7 mentions no pressure file | REJECTED: the assigned manual page does not exist, so it supports no claim about the /proc/pressure line grammar or the system-wide CPU full line; flip: the same scope is documented by the kernel PSI documentation (S001; kernel v7.2 Documentation/accounting/psi.rst lines 42-43 and 57-58), where CPU full is undefined at the system level. | rejected | 2026-10-22 | on-release | — |
```

Cell-by-cell rationale:

- **kind** `docs` (what the source was meant to be), **tier** `C` — the page cannot be
  admitted at tier A because it carries no content; rejected rows in this registry are
  tier C (S030, S055, S057, S059, S061, S063, S065, S072).
- **status** `rejected`; **recheck** `on-release` — the page could only appear in a
  future man-pages release, and man7 republishes on release.
- **used-by** `—`, the convention for rejected rows (S030, S054, S055, S057, S059,
  S061, S063, S072); S065 is the one rejected row that carries a lesson in used-by, so
  the L1 may set `corpus/lessons/round-24.md` here if the lesson cites the rejection in
  prose.
- **opened** `2026-10-22` — the date of the fetch recorded above.
- The L1 assigns the real id; the next free id after the current tail S089 is S090.

## Gate block for the round-24 lesson (draft)

To be placed in `corpus/lessons/round-24.md` as `## Gate` (draft only; not written).

```
## Gate

URL: https://man7.org/linux/man-pages/man5/proc_pressure.5.html
Access date (UTC): 2026-10-22T08:21:46Z → 2026-10-22T08:21:47Z (server Date: Thu, 22 Oct 2026 08:21:47 GMT)
Fetched bytes: 196 bytes, HTTP 404 Not Found, sha256 80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880 (first 16 hex 80c3fe2ae1062abf5)
Line anchors verified: fetched body line 3 <title>404 Not Found</title>; line 5 <h1>Not Found</h1>; line 6 <p>The requested URL was not found on this server.</p>
Located quote (9 words, copied exactly from the fetched bytes, line 6):
  "The requested URL was not found on this server."
Cross-checks: raw.githubusercontent man-pages master man/man5/proc_pressure.5.html → 404;
man7 man5 index lists no proc_pressure page; man-pages 6.20 tarball (sha256
180f0d16a2142dd9671760ac0afeadcc25e861f695eb420293e1206a87ca083f, released 2026-10-21)
contains no proc_pressure page and no page mentioning /proc/pressure; man7 proc(5)
contains no occurrence of pressure, stall or PSI.
Decision: no proc_pressure(5) row is mined. The URL is recorded as a rejected
provenance record only, and the C2 sourced list drops "proc_pressure(5)".
```

### Substitute anchor actually verified this round (for the L1's C2 sourced list)

The scope the dead man page was meant to supply is carried by the kernel PSI
documentation. I fetched the v7.2 raw file only to check that the substitute exists
and to give the L1 a verified anchor; the row itself belongs to seat `SrcPsiRst`, and
I did not draft a second SOURCES.md row for it.

```
URL: https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst
HTTP 200, 6792 bytes, sha256 11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692
Line anchors verified: line 34 "Pressure interface"; lines 42-43 the literal format
  some avg10=0.00 avg60=0.00 avg300=0.00 total=0 / full avg10=0.00 avg60=0.00 avg300=0.00 total=0
  (tab-indented); lines 57-58 the CPU-full sentence.
Located quote (23 words, copied exactly, lines 57-58):
  "CPU full is undefined at the system level, but has been reported since 5.13, so it is set to zero for backward compatibility."
```

## Narrow claim the assigned source supports, and what it does not support

- **Supports:** nothing about `/proc/pressure`. The only claim the fetched bytes
  support is negative: *the man-pages project does not publish a `proc_pressure(5)`
  manual page, and man7 therefore serves 404 for it.* That negative claim is enough to
  remove `proc_pressure(5)` from the C2 sourced list.
- **Does NOT support** (each of these was going to be cited from this page and must
  come from the kernel sources instead):
  - the `some`/`full`, `avg10`/`avg60`/`avg300`/`total` line grammar of
    `/proc/pressure/{cpu,memory,io}` — supported by
    `Documentation/accounting/psi.rst:42-43` and by S001;
  - the absence of an `irq` resource from the kernel's own pressure interface
    (`psi.rst:38` names only cpu, memory and io) — a fact about the kernel, not the
    man page;
  - the system-wide CPU `full` line being undefined (`psi.rst:57-58`), which is what
    backs the C2 tool's `full_system_undefined: true` label;
  - cgroup-v2 pressure files — owned by S002 and seat `SrcCgroupV2`;
  - anything about PSI triggers, the PSI Kconfig or the `psi=` boot parameter — owned
    by seats `SrcKconfig` and `SrcKernelParams`.

## Findings for the L1

1. **Contract defect (verbatim):** `.ufo/waves/round-24/contract.md`, C2 "**Sourced:**"
   clause lists `proc_pressure(5)` among the sources the round-24 knowledge entry and
   SKILL.md decision table may cite. No such manual page exists. That citation must be
   removed or replaced (kernel PSI documentation, S001 / `psi.rst`) before the C2
   knowledge entry is written. I did not edit the contract.
2. **The intended scope is already sourced.** S001 covers "Linux PSI counters, totals,
   thresholds and per-cgroup files" from `docs.kernel.org/accounting/psi.html`; the
   version-pinned v7.2 raw file is the same document and is owned by seat `SrcPsiRst`.
   Two sibling PSI-code seats (`SrcPsiC`, `SrcPsiIrqCommit`) cover the code side.
   The man page was a redundant third citation for a scope that already has two.
3. **One-row answer for the registry:** the drafted row is a NEW rejected provenance
   record, `S0xx` (next free id S090), and it supersedes nothing. If the L1 prefers
   the registry to carry no row for a URL that never existed, drop the row and keep
   only this Gate block; both options are consistent with the registry's current
   practice of keeping one rejected row per screened-out candidate (S030, S057, S059).
4. **Not a duplicate of S001/S002.** Zero registry rows mention `proc_pressure`; zero
   reference any `man-pages/man5` page.

## Out of scope / not done

- No edit to `corpus/SOURCES.md`, to the round-24 contract, to the lesson file, or to
  any other lane file. The only file I created inside the lane repo is this report.
- No product code, tool, fixture, or knowledge entry was written or modified.
- No host write of any kind: no `/proc`, `/sys` or cgroup file was written, no PSI
  trigger was registered, no service was restarted, no package was installed or
  upgraded (tooling installs this round: **none**).
- No git/jj mutation in the lane repo; all git state was read-only. My scratch files
  live outside the lane, under `/tmp/mori-r24-src/` (removed on request; harmless
  otherwise).
- I did not open `https://man7.org/linux/man-pages/man5/proc_pressure.5.html` in a
  browser; the fetch was `curl` over HTTPS to man7.org, and the 404 comes from the
  origin server (`Server: Apache/2.4.58 (Ubuntu)`), not from a proxy.

## Artifacts and paths

- Report: `.ufo/waves/round-24/w1/SrcProcPressureMan.md` (this file).
- Fetched 404 body and headers: `/tmp/mori-r24-src/body_404.html`,
  `/tmp/mori-r24-src/headers_404.txt` (196 bytes, sha256 `80c3fe2ae1062abf5…`).
- man-pages 6.20 tarball and tree: `/tmp/mori-r24-src/man-pages-6.20.tar.xz`
  (sha256 `180f0d16a2142dd9671760ac0afeadcc25e861f695eb420293e1206a87ca083f`),
  extracted at `/tmp/mori-r24-src/man-pages-6.20/`.
- Kernel v7.2 PSI docs copy: `/tmp/mori-r24-src/psi_v72.rst` (6792 bytes, sha256
  `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692`).
- Lane files read: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`
  (header line 6, rows S001–S002, S030, S054–S072, S085–S089),
  `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-23.md:34-62,213-232`
  (Gate block style),
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-24/contract.md` (C2
  "Sourced" clause),
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-24/wave1-assignments.json`
  (seat roster).

Report: .ufo/waves/round-24/w1/SrcProcPressureMan.md
