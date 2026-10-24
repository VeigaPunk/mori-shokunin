# ConnectSourceDuplicates — round 24 wave 1 (claim C2, surface: source registries)

Seat: connector, read-only, leaf. No lane file other than this report was written. No installs or
updates were made (none needed; `gh`, `curl`, `gawk`, `rg` were already present).

## Bottom line

- Exactly two existing rows across all 21 lane registries match the eight target sources, and both
  are in mori: **S001** (docs.kernel.org `psi.html`) and **S002** (docs.kernel.org
  `cgroup-v2.html`). No sibling lane registers any of the eight.
- The eight planned round-24 URLs (seven `raw.githubusercontent.com/torvalds/linux/v7.2/...`
  files, man7 `proc_pressure.5.html`, and the PSI_IRQ commit) share no normalized URL with any
  existing row, so adding all eight produces **no W04 and no E04**. Measured on a throwaway copy:
  validate exit 0, zero new findings (probe V8 below).
- Recommendation: **new row for all eight; no supersession of S001 or S002.** Nothing in either
  row is wrong at v7.2; they cover different scopes and are still cited.
- The one non-obvious move (below): the census cannot see that the v7.2 `psi.rst` row and S001 are
  the same document, so the only guard against a round-23-style later correction is the scope
  cell. v7.2 `psi.rst` says nothing about IRQ pressure, yet the SrcPsiRst seat was asked to teach
  "IRQ pressure" from it. Route every IRQ teaching to the `psi.c`, `cgroup-v2.rst`,
  `psi_types.h` and commit rows instead. A second source-level contradiction with the contract
  (PSI disabled reads as ENOENT, not EOPNOTSUPP) belongs in the `psi.c` row's scope.

## 1. Matching rows (every lane)

Method: `rg` over `/home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md` (21 files exist) for
each target pattern, then a broad sweep for `kernel.org|torvalds|elixir|man7.org|Kconfig|cgroup|psi`.

| Target | Pattern searched | Hits |
|---|---|---|
| Linux `psi.rst` | `psi\.(rst\|html)\|accounting/psi` | mori S001 only (`SOURCES.md:7`) |
| `kernel/sched/psi.c` | `sched/psi\.c` | none, any lane |
| `cgroup-v2.rst` | `cgroup-v2` | mori S002 only (`SOURCES.md:8`) |
| `init/Kconfig` | `init/Kconfig\|CONFIG_PSI` | none |
| `kernel-parameters.txt` | `kernel-parameters\|kernel-command-line\|psi=` | none |
| proc_pressure(5) | `proc_pressure\|/proc/pressure` | none |
| `psi_types.h` | `psi_types` | none |
| PSI_IRQ commit | `PSI_IRQ\|IRQ.?pressure\|52b1364` | none |

Matching rows (verbatim key cells):

- `mori-shokunin/corpus/SOURCES.md:7` — **S001** | PSI - Pressure Stall Information —
  `https://docs.kernel.org/accounting/psi.html` | docs | A | scope "Linux PSI counters, totals,
  thresholds and per-cgroup files" | anchor "Pressure interface:74-77; Monitoring for pressure
  thresholds:104-119; Cgroup2 interface; … current page opened 2026-10-19" | teaches "Keep avg10
  trends distinct from absolute stall microseconds; PSI trigger lifetime follows its file
  descriptor." | mined | used-by `corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md`.
- `mori-shokunin/corpus/SOURCES.md:8` — **S002** | Control Group v2 —
  `https://docs.kernel.org/admin-guide/cgroup-v2.html` | docs | A | scope "cgroup-v2 memory events,
  memory.peak and local versus hierarchical scope" | anchor memory.events / memory.peak | mined |
  used-by three r12/r14 knowledge entries.

PSI-adjacent by scope but not one of the eight targets (no action): S007 systemd-oomd
(`SOURCES.md:13`), S010 systemd.io/PRESSURE (`SOURCES.md:16`, queued), S021 LWN BPF OOM
(`SOURCES.md:27`). Sibling lanes' kernel rows are unrelated (kama S048/S049 `tcp_ipv6.c` /
`proc_net_tcp.rst`; mado S112 man-pages user_namespaces; tsukuroi S063 zswap; souji/tameshi man7
proc_pid_* and syscall pages).

Fleet `shared` view (the only census mode that compares lanes):
`bash scripts/sources-census.sh shared --root /home/vgpnk/Projects/shokunin` → 30 lines; the only
kernel/man7 entry is `man7.org/linux/man-pages/man2/open.2.html shared tameshi,souji`. No PSI or
cgroup URL is shared.

## 2. Census run (as assigned)

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc…/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
exit=0
```

Baseline for the round: **6 inherited W04, 0 errors, exit 0.** None involves a PSI or cgroup URL.

## 3. What a duplicate-URL row triggers (W04 and E04)

Code: `scripts/sources-census.sh`.

- URL normalization, `url_of` (`:600-605`): takes the **first** `http(s)://` URL in the source cell
  (stops at whitespace or `|`), strips any `#fragment`, a trailing `/`, and the scheme, lowercases
  the host only. Query strings are kept; path case is kept.
- **W04** (`:644-645`): fires when the normalized URL was already seen in this lane **and** the pair
  (URL, exact trimmed scope text) was not. It is a warning: "warnings do not affect clean lanes"
  (`:33`); the lane still prints `ok` and exits 0 (`:738-745`, `:803-806`; selftest
  `W04-does-not-fail-validation`, `:364`).
- **E04** (`:646-649`): fires when the same (URL, exact scope) pair already has a non-rejected row,
  the new row is not `rejected`, and its `teaches` lacks the regex `supersedes S[0-9]{3}`. It is an
  error: the lane is not `ok` and validate exits 1. A prior `rejected` row with the same pair
  exempts the new row (selftest `E04-rejected-pair-exemption`, `:379-381`).
- Both checks are **per lane**; cross-lane reuse is only reported by `shared` mode, never as a
  finding. Neither check knows that two different URLs carry the same document.

Measured on throwaway copies of mori's registry (in `mktemp -d`, used-by directories symlinked so
E11 resolves, copies deleted after; one row appended after S089, `status=queued`):

| Probe | Appended row | Result |
|---|---|---|
| V0 | none (control) | exit 0, no new finding |
| V1 | raw v7.2 `psi.rst`, new scope | exit 0, no finding |
| V2 | S001's URL with `#pressure-interface` fragment, new scope | `W04 S090 duplicate url docs.kernel.org/accounting/psi.html across scopes`, exit 0 |
| V3 | S001's URL, S001's exact scope, no supersedes | `E04 S090 … within scope Linux PSI counters, totals, thresholds and per-cgroup files`, exit 1 |
| V4 | as V3 with `supersedes S001 —` in teaches | exit 0, no finding |
| V5 | S001's URL, new scope, `supersedes S001 —` | W04 still fires, exit 0 (supersedes does not silence W04) |
| V6 | S002's URL, new scope "cgroup cpu/io/irq/memory.pressure files" | `W04 S090 duplicate url docs.kernel.org/admin-guide/cgroup-v2.html across scopes`, exit 0 |
| V7 | two proc_pressure(5) rows, same scope, no supersedes | `E04 S091 duplicate url man7.org/…/proc_pressure.5.html within scope …`, exit 1 |
| V8 | all eight planned URLs, one row each | exit 0, no finding (W04 count stays 6) |
| V9 | raw v7.2 `psi.rst` twice, same scope, second says `supersedes S090 —` | exit 0, no finding |

So: reusing S001's or S002's docs.kernel.org URL under a new scope adds a seventh W04 (harmless to
exit status, but noise in the inherited-warning count that LOG.md:1120 tracks as "preserved");
reusing them under the identical scope without `supersedes` breaks validation with E04.

## 4. New row versus supersession, per source

Lane rules: rows are append-only and immutable except status/recheck/used-by; "A correction is a
new row whose `teaches` opens `supersedes S0NN —`" (`/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`).
Lane precedent: a new scope on an existing URL is a new row, not a rewrite ("New subject scope does
not rewrite immutable S015 fields", `SOURCES.md:115`; S035 over S013, S037 over S015); supersession
is reserved for corrections of over-reaching teaches (S073→S069, S074→S071, S075→S070, S076→S067,
`SOURCES.md:129`; S087→S083, S088→S084, `SOURCES.md:137`). Round 23 also set the URL convention:
Linux sources pinned as `raw.githubusercontent.com/torvalds/linux/v7.2/…` with a sha256 prefix in
the anchor (S077–S089).

| Planned source (URL from `wave1-spec.json`) | Existing overlap | Census effect | Recommendation |
|---|---|---|---|
| `…/v7.2/Documentation/accounting/psi.rst` | Same document as S001 (docs.kernel.org renders it), different URL | none | **New row.** S001's teaches still holds at v7.2 (`psi.rst:117-119` trigger de-registers on fd close; `:60-65` avg ratios versus total in µs). Do not supersede: S001 is correct and cited. Scope must exclude IRQ (see §5). |
| `…/v7.2/kernel/sched/psi.c` | none | none | **New row.** Carries IRQ-full-only, system CPU full zeroed, `psi=`/default-disabled, proc entry creation and the read-time EOPNOTSUPP paths. |
| `…/v7.2/Documentation/admin-guide/cgroup-v2.rst` | Same document as S002, different URL | none | **New row.** S002 is memory.events/memory.peak; the new scope is the pressure files (`cgroup.pressure`, `irq.pressure`, `cpu.pressure`, `memory.pressure`, `io.pressure`; scratch copy lines 1066, 1083, 1215, 1911, 2171). Not a correction of S002. If instead the docs.kernel.org URL were reused, expect one new W04. |
| `…/v7.2/init/Kconfig` | none | none | **New row.** |
| `…/v7.2/Documentation/admin-guide/kernel-parameters.txt` | none | none | **New row.** |
| `https://man7.org/linux/man-pages/man5/proc_pressure.5.html` | none | none | **New row.** If the page is re-opened for a narrower scope later, the second row needs `supersedes` or a distinct scope (V7 shows E04). |
| `…/v7.2/include/linux/psi_types.h` | none | none | **New row.** |
| PSI_IRQ commit `https://github.com/torvalds/linux/commit/52b1364ba0b105122d6de0e719b36db705011ac1` | none | none | **New row.** Verified via `gh api repos/torvalds/linux/commits/52b1364…`: subject "sched/psi: Add PSI_IRQ to track IRQ/SOFTIRQ pressure", author Chengming Zhou, committed 2022-09-09T09:08:32Z. First release tag: `compare 52b1364…v6.0` → `diverged`, `compare 52b1364…v6.1-rc1` → `ahead`, so first in v6.1-rc1 (v6.1). |

## 5. Proposed move (one, bounded)

**Assign every C2 fact to the row whose v7.2 bytes actually state it, before ids are assigned; in
particular keep IRQ and "PSI disabled" out of the `psi.rst` row.**

Evidence (all from v7.2 bytes; `psi.rst` read from the CriticC2Semantics seat's fetch at
`/fast/scratch/hyaku/mori-r24-a2/critic-c2sem/psi.rst`, sha256 `11c6b7129103b454…`; `psi.c` read from
`/fast/scratch/hyaku/mori-r24-a2/srcpsic/psi.c`, sha256 `452318beaca3e6d1…`, byte-identical to the
critic seat's independent fetch):

1. `psi.rst:37-38` — "exported through the respective file in /proc/pressure/ -- cpu, memory, and
   io." The file never mentions irq (also its cgroup section, `:183-185`, lists only cpu/memory/io).
   The live docs.kernel.org page that S001 points at also has zero "irq" matches
   (`curl -sS https://docs.kernel.org/accounting/psi.html | rg -i -c irq` → no output, 2026-10-22T08:17Z).
   The SrcPsiRst assignment nevertheless lists "IRQ pressure" among its teaches.
2. IRQ facts live elsewhere: `psi.c:1260-1262` (EOPNOTSUPP for irq when irqtime is disabled),
   `:1273-1277` (`only_full = res == PSI_IRQ`), `:1717-1719` (`pressure/irq` created only under
   `CONFIG_IRQ_TIME_ACCOUNTING`); `cgroup-v2.rst` `irq.pressure`; the PSI_IRQ commit message ("Note we
   don't use PSI_IRQ_SOME …").
3. Contradiction with the contract, stated explicitly: the contract maps
   "EOPNOTSUPP → `unsupported` (PSI disabled)" (lines 61-62 at `29c1bf45`; lines 68-69 at
   `f7eb430` and at tip `f38dbbd`, after amendment A1), and P05 uses EOPNOTSUPP on all four
   files. In v7.2, PSI disabled (`psi=0` or `CONFIG_PSI_DEFAULT_DISABLED`) leaves the boot
   boolean `psi_enable` false (`psi.c:149-158`). Two independent consumers read it: `psi_init`
   sets the `psi_disabled` static key (`:230-233`), and `psi_proc_init` checks `if (psi_enable)`
   itself (`:1712`) and creates no `/proc/pressure` entries (`:1710-1722`). It does not consult
   `psi_disabled`. A PSI-disabled host therefore reads as **ENOENT → `absent`**, not EOPNOTSUPP.
   EOPNOTSUPP is returned at read time from `psi_show` (`:1257-1262`), which on `/proc/pressure`
   is reachable for `irq` when IRQ time accounting is runtime-disabled. The SrcPsiC assignment's
   phrase "the disabled-PSI return path (EOPNOTSUPP)" carries the same conflation.
4. `psi.rst:57-58` — system CPU full "is set to zero for backward compatibility", matching
   `psi.c:1282-1288`. A `psi.rst` scope that says only "undefined" is narrower than the source.

Affected axes: **coverage** (C2 sourced step; no change to what is sourced, only which row
carries it), **calibration** (avoids teaches that the cited bytes do not state), **freshness**
(rows pinned to v7.2 bytes with digests). Held axes unaffected: no tool, case, or contract
target changes; census findings stay at the inherited 6 W04 (V8).

Concretely for the L1 at integration:
- `psi.rst` row scope: system `/proc/pressure/{cpu,memory,io}` line format, some/full meaning,
  system CPU full zeroed for compatibility, avg windows versus total µs, trigger bounds. Teaches must
  not name IRQ or EOPNOTSUPP.
- `psi.c` row scope: IRQ full-only output, system CPU full zeroed, `psi=` and default-disabled boot
  switch, proc entries absent when PSI is disabled, read-time EOPNOTSUPP for a disabled read path.
- Do not supersede S001 or S002; add the round's rows to a new `## Paths` route (for example
  "system pressure") rather than editing the existing "fleet runway" route that cites S001/S002.
- The contract's ENOENT/EOPNOTSUPP mapping is already resolved by **Amendment A2**
  (`contract.md:110-117` at tip `f38dbbd`). A disabled kernel shows every file `absent`;
  `unsupported` stays for an EOPNOTSUPP error but carries no inferred cause; P05 and P02 are
  labeled defensive. Consequence for the registry: no round-24 row's scope or teaches may attach
  a cause ("PSI disabled") to EOPNOTSUPP, and the `psi.c` row should cite `:1712` for the
  ENOENT case and `:1257-1262` for the read-time EOPNOTSUPP.
- Keep SrcPsiC's teaches phrasing verbatim when the row is admitted, and reuse it in
  `corpus/knowledge/system-pressure-r24.md` (the seat asked for this at 08:23Z). Full cell,
  byte-matched against `SrcPsiC.md:181`: "psi_show prints one some line and one full line for cpu,
  memory and io but only a full line for IRQ, and the system CPU full line is a fixed zero rather
  than a measurement; psi_show returns EOPNOTSUPP on the psi_disabled branch and, for IRQ, when
  IRQ time accounting is off; the /proc/pressure/* entries are created once at init, so a PSI
  switched off at boot leaves them absent rather than unreadable" (also its §8 item 5).
  Two limits on reuse, from the seat:
  - "switched off at boot" means the `psi=` switch (`psi_enable`, `psi.c:145-158`). It describes
    v7.2's own creation logic; the host's kernel version is a separate fact that is not claimed.
  - The same errno arises for `irq` when IRQ time accounting is off at runtime
    (`psi.c:1260-1263`), so "EOPNOTSUPP means PSI is disabled" over-claims. The source supports
    only "unavailable/unsupported, cause not determined by the read alone", consistent with A2.

## 6. Risks

- If the `psi.rst` row is filed with IRQ or "PSI disabled → EOPNOTSUPP" in teaches, the census will
  stay green (it checks only URL+scope text), and the only later remedy is a round-23-style
  `supersedes` correction row (`SOURCES.md:137`). Census green is not evidence of row correctness.
- If any scribe cites a docs.kernel.org URL (S001/S002) instead of the raw v7.2 pin, even with a
  `#fragment`, expect +1 W04 per row (V2, V6); with S001's exact scope text and no `supersedes`,
  E04 and validate exit 1 (V3).
- A source cell that lists two URLs is keyed only on the first (`url_of`, `:601`); a cell that leads
  with docs.kernel.org and mentions the raw pin second is treated as S001's URL.
- docs.kernel.org renders the current tree, not v7.2; S001's "current page" anchor and the new v7.2
  pin can drift apart on a later kernel release (recheck `on-release` covers this).
- The psi.rst and cgroup-v2.rst bytes I read were fetched by other seats (digests above), not by me;
  the line numbers I cite hold for those bytes.

## 6a. Addendum — seat drafts checked after filing (2026-10-22T08:20Z)

- `SrcKconfig.md:136` (id `S0xx`, raw v7.2 `init/Kconfig`, kind code): new row, consistent with
  §4. Its help text at 730-733 names only cpu/memory/io, while `psi.c:1717-1719` also creates
  `pressure/irq`; the row must not be worded as the complete file list. The `psi=` boot semantics
  belong to `SrcKernelParams.md:90` (raw v7.2 `kernel-parameters.txt`, id `S0xx`); distinct URLs, no
  census effect. **Resolved 08:23Z**, re-checked here: the row is now at `SrcKconfig.md:177`
  (Gate row `:217`), id `S0xx`, and the source cell's first URL is `…/v7.2/init/Kconfig`. The
  teaches says the help text "names only the pressure statistics files cpu, memory, and io"
  (attributed to the help text, not to the kernel), and the Gate reject paragraph (`:232`) states
  that the list is not the complete file set. The seat's own cross-check fetch of `psi.c`
  (08:20:41Z, 48859 bytes, sha256 `452318beaca3e6d1…`) is the third independent fetch with the
  same digest. It claims no row for that URL.
- `SrcPsiIrqCommit.md:159` hard-codes id **`S090`**; all other drafts use `S0xx`, as the wave spec
  asks. If the L1 also assigns S090 to another row, validate reports **E03 duplicate id**
  (`sources-census.sh:641`). Asked the seat to use `S0xx`. Its source cell carries only the
  github commit URL (the git.kernel.org mirror is in the report body), so `url_of` keys it uniquely.
  Its introduction-only scope keeps it distinct from the v7.2 `psi.c` and `psi_types.h` rows; new
  row, no supersession. **Resolved 08:21Z:** the seat changed both table rows to `S0xx`
  (`SrcPsiIrqCommit.md:161`, `:197`), and neither cell contains a git.kernel.org URL. Re-checked
  here with `rg`. The only remaining S090 use is the SrcPsiC seat's /tmp test id, which was
  never a filed value.
- Both seats were answered over the peer channel.
- `SrcPsiC` (raw v7.2 `kernel/sched/psi.c`, sha256 `452318beaca3e6d1…`, 48859 bytes, matching
  the copy read here): new row, no supersession. Its own /tmp validate with id S090 is clean
  only in isolation, because SrcPsiIrqCommit also claims S090, so both together give E03. The
  literal `S0xx` placeholder gives E02, which is expected for an unfiled draft. `mined` with
  used-by `corpus/lessons/round-24.md` gives E11 until that lesson is committed, so it must land
  in the same commit as the status flip or an earlier one. Asked the seat not to word its scope
  as "PSI disabled → EOPNOTSUPP" (see §5 item 3). **Resolved 08:22Z**, re-checked here:
  both table rows are `S0xx` (`SrcPsiC.md:181`, `:242`); no "PSI disabled →" wording remains.
  The teaches now reads "psi_show returns EOPNOTSUPP on the psi_disabled branch and, for IRQ,
  when IRQ time accounting is off; the /proc/pressure/* entries are created once at init, so a
  PSI switched off at boot leaves them absent rather than unreadable". This matches
  `psi.c:1257-1262` and `:1710-1722` and attaches no cause to EOPNOTSUPP, consistent with A2. The
  row is proposed `queued` with used-by `—` until `corpus/lessons/round-24.md` is committed. The
  seat measured E03 on a two-S090 fixture, confirming that the L1 must assign ids across all
  round-24 rows.
- `CriticC2Semantics` (08:21Z) confirmed the ENOENT finding independently (its F1). It corrected
  two details, both verified and fixed in §5: `psi_proc_init` checks `psi_enable` at `:1712`
  and does not use `psi_disabled`; the contract line numbers moved after amendment A1. Its F3
  is a silent-zero case: writing 0 to the root `cgroup.pressure` stops `psi_system` accounting
  while `/proc/pressure` stays readable with frozen totals. Registry consequence: if F3 is
  carried into the knowledge entry, the `cgroup-v2.rst` row's scope should name `cgroup.pressure`
  (scratch copy line 1066). Any row added for `include/linux/psi.h` or `kernel/cgroup/cgroup.c`
  at v7.2 is a new URL, so it adds no W04 and no E04.
- `SrcPsiRst` (raw v7.2 `psi.rst`, 6792 bytes, sha256 `11c6b7129103b454…`, matching the copy
  read here; the seat reports identical bytes at master): new row, no supersession of S001. Re-checked
  here: row `SrcPsiRst.md:143` and Gate row `:195` are `S0xx`; the first URL in the source cell
  is the raw v7.2 pin; neither the scope nor the teaches cell mentions IRQ, EOPNOTSUPP or
  "disabled". The Gate's single "irq" is the exclusion "Not for IRQ pressure". The §5 IRQ re-route
  is therefore satisfied. One optional nit sent to the seat: teaches says "each file is exactly two
  lines". `psi.rst:40-43` shows a two-line format but never says "exactly", and the real `irq` file
  prints one line (`psi.c:1274`). Suggested wording: "each named file (cpu, memory, io) shows a some
  line and a full line".
- CriticC2Semantics (08:22Z) supplied fetch digests for the F3 sources: `psi.h`
  `cd80982f753aa56e` (anchor `:37-40`), `cgroup.c` `3d4a256adea52d7e` (`:4123-4133`,
  `:5585-5589`), `cgroup-v2.rst` `a9433bb0e16a67f0` (`:1066-1081`). The `cgroup-v2.rst` digest
  matches the SrcCgroupV2 scratch copy hashed here. Read here: `cgroup-v2.rst:1066-1081` documents
  `cgroup.pressure` as a non-hierarchical per-cgroup switch ("Writing "0" to the file will disable
  the cgroup PSI accounting", `:1070`). It does **not** say that the root cgroup's switch freezes
  `/proc/pressure`. That link is code-only: `psi.h` maps root to `psi_system`, and `cgroup.c`
  performs the stop. If F3 enters the knowledge entry, it needs `psi.h` and `cgroup.c` rows; the
  `cgroup-v2.rst` row alone would over-reach. Both would be new rows with no census effect. The
  critic reports F3 as still open, and A2's bracket check cannot detect it.

## 6b. Post-landing check (2026-10-22T08:52Z, tip `6fce88a`)

The L1 filed the rows as S090–S097 in `df4db54` ("sources S090-S097, system pressure knowledge
entry, lesson, evidence"): S090 `psi.rst`, S091 `psi.c`, S092 `cgroup-v2.rst`, S093 `init/Kconfig`,
S094 `kernel-parameters.txt`, S095 `psi_types.h`, S096 the PSI_IRQ commit, S097 `proc_pressure.5`.
Each row's first URL is the planned pin; none reuses S001's or S002's docs.kernel.org URL; no
row carries `supersedes`. Census at tip:

```
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
(the same six inherited W04: S035, S037, S073, S074, S075, S076)
mori	ok	…/mori-shokunin/corpus/SOURCES.md
exit=0
```

This matches the §3 V8 prediction: zero new findings.

**S090 residual: recommend no supersession.** S090 was filed with the seat's earlier teaches,
"each file is exactly two lines … exported as zero since 5.13", before the seat tightened its
draft. It is not false within S090's scope ("the /proc/pressure/ file set the document names",
which is cpu, memory and io). For those three files, v7.2 prints both lines (`psi.c:1273-1277`:
the loop runs `full < 2 - only_full`, and `only_full` is true only for IRQ), and `psi.rst:57-58`
says CPU full "has been reported since 5.13, so it is set to zero". CORPUS.md rule 2 reserves
`supersedes S0NN —` for corrections. A narrowing-only row would add a duplicate of S090's URL
under the same or a new scope (E04 without `supersedes`, or W04 under a new scope), for no
change of truth. If the L1 still wants it, V4 and V9 show that the same URL and scope with
`supersedes S090 —` validates clean.

The place where the phrase can actually over-reach is the knowledge note, not the registry.
`corpus/knowledge/system-pressure-r24.md:34` opens F2 with "Each file holds two lines", directly
after F1 (`:29-31`) has introduced the IRQ file. F5 (`:63-69`) then says IRQ has one `full` line.
That is consistent read as a whole, but F2 lifted alone over-claims. Narrowing `:34` to "Each of
cpu, memory and io holds two lines" closes it without touching the registry. That edit belongs to
the L1 (the knowledge note is outside this seat's surface); it is recorded here, not made.
SrcPsiRst concurred at 08:53Z: no supersession row for S090. It will add the `:34` pointer to
its own report beside its §11, so the L1 sees the registry note and the knowledge-note fix together.

## 7. Verification (what I ran, and what I did not)

Ran:
- `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → 6 W04, `ok`, exit 0.
- `sources-census.sh shared --root /home/vgpnk/Projects/shokunin` → no PSI/cgroup shared URL.
- Probes V0–V9 on temporary copies (table in §3); copies removed.
- `gh api` commit lookup and two compare calls for the PSI_IRQ commit.
- `sha256sum` of the scratch `psi.c` copies (identical), `psi.rst`, `cgroup-v2.rst`.

Not run: no fetch of Kconfig, kernel-parameters.txt, proc_pressure(5) or psi_types.h by this seat
(the census result for their URLs does not depend on content); no census run against a lane tree
containing the real drafted rows (they are not integrated yet). The L1 should rerun
`sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` after integration and expect
exactly the six inherited W04 lines and exit 0; any seventh W04 or any E04 means a row reused
S001/S002's URL or duplicated a round-24 row's URL and scope.
