# SrcKernelParams — round 24, wave 1 (scribe, read-only)

Seat: `MoriR24.SrcKernelParams` · Claim: C2 (sourced frontier step) · Report only, no lane edits.

## What I did

Opened the pinned upstream file once this round, recorded the access time and the digest of
the fetched bytes, located the `psi=` boot parameter entry, checked the lane's
`corpus/SOURCES.md` for an existing row with the same URL or scope, and drafted one row plus
a `## Gate` block. Nothing in the lane repo was modified except this report file.

### Fetch record

| Item | Value |
|---|---|
| URL | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/kernel-parameters.txt |
| Result | HTTP 200, 317993 bytes, 8676 lines |
| Access time | 2026-10-22T08:15:07Z (UTC) |
| SHA-256 (full) | `23b1a690210b6884f040a6b1e5baf1fc18856e844d30d4784470bd210953340c` |
| SHA-256 (first 16 hex) | `23b1a690210b6884` |
| Client | curl 8.23.0 (OpenSSL 3.6.5); digest by coreutils sha256sum 0.8.0 |
| Bytes retained | `/fast/scratch/hyaku/mori-r24-a2/src-kernelparams/kernel-parameters.txt` (round scratch, outside the lane repo) and `/tmp/mori-r24-src/kernel-parameters.txt` |

Disclosure: the first fetch attempt (`curl -sS -L ...` with no user agent, 2026-10-22T08:14:57Z)
returned HTTP 429 and **zero** bytes, so that attempt contributed nothing to the digest. The
accepted fetch is the retry that returned HTTP 200 at 08:15:07Z; the digest above is of those
bytes only. No other copy of the file was consulted.

### Anchors verified

- `psi=` entry: lines **5505–5507** (the only occurrence of `psi=` in the file; `grep -c "^	psi="` = 1).
- Neighbour lines read to confirm the entry is a standalone kernel parameter: 5500–5503
  (`prot_virt=`, ending `Format: <bool>`) and 5509 (`psmouse.proto=`), so 5505–5507 is a whole
  parameter entry, not a fragment of another one.
- `grep -c "CONFIG_PSI"` = **0**: this document does not mention the PSI Kconfig symbol at all.
- `grep -n -i "pressure"` returns 8 hits; only 5505 is a PSI entry. The others (`735`, `887`,
  `5770`, `5822`, `6764`, `6768`, `6771`) are unrelated uses of the word "pressure"
  (cgroup `pressure` mode, page-stealing memory pressure, thermal pressure shift).
- Exact bytes of the entry (`cat -A`, tab shown as `^I`):

```
5505	^Ipsi=^I^I[KNL] Enable or disable pressure stall information$
5506	^I^I^Itracking.$
5507	^I^I^IFormat: <bool>$
```

## Located quote (≤25 words, copied exactly)

Line 5505, verbatim (tabs preserved):

```
	psi=		[KNL] Enable or disable pressure stall information
```

That is 7 words. The full three-line entry (5505–5507), verbatim:

```
	psi=		[KNL] Enable or disable pressure stall information
			tracking.
			Format: <bool>
```

## Duplicate check against `corpus/SOURCES.md`

**This is a NEW row, not a supersession.**

- `grep -n "kernel-parameters" corpus/SOURCES.md` → **no match**. No existing row cites this
  URL or any `Documentation/admin-guide/kernel-parameters.txt` URL.
- PSI-related rows that do exist, and why none of them is superseded:
  - **S001** `https://docs.kernel.org/accounting/psi.html` — scope is PSI counters, totals,
    thresholds and per-cgroup files (the `psi.html` accounting document). It says nothing
    about a boot parameter. Different URL, different document, complementary scope; my row does
    not narrow, reinterpret or replace it.
  - **S002** `https://docs.kernel.org/admin-guide/cgroup-v2.html` — cgroup-v2 memory events and
    `memory.peak`. Unrelated to boot parameters.
  - **S007** `systemd-oomd.service(8)` — userspace consumer of PSI. Different layer.
  - **S010** `https://systemd.io/PRESSURE/` — the systemd pressure-watch protocol. Different
    layer.
  - **S021** LWN BPF OOM article — rejected community-tier candidate about BPF OOM hooks.
- The nearest sibling scope in the registry is the PSI **Kconfig** symbol, which is a *different
  source file* and is covered by a separate seat (`MoriR24.SrcKconfig`); this row neither
  duplicates nor pre-empts it.
- Precedent for how such a row lands: round-23 rows S077/S082/S083/S084 are `docs`/`A` rows for
  `Documentation/...` files at tag v7.2 with anchors of the form `path:lines; tag v7.2;
  sha256 <first16>` (`corpus/SOURCES.md:83-90`).

## Draft SOURCES.md row (11 cells; id left as `S0xx` for the L1)

```markdown
| S0xx | Linux kernel parameters v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/kernel-parameters.txt | docs | A | the psi= kernel boot parameter that enables or disables pressure stall information tracking; parameter name, format and stated effect only, no file layout and no counter semantics; v7.2 only | psi= parameter:5505-5507; tag v7.2; sha256 23b1a690210b6884 | psi= is a [KNL] kernel boot parameter of <bool> format that enables or disables pressure stall information tracking, so PSI tracking is switchable at boot and is not guaranteed merely by running a Linux kernel. | queued | 2026-10-22 | on-release | — |
```

Cell-by-cell check against the header at `corpus/SOURCES.md:6`
(`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`):
11 cells, in order, no extra pipe.

Notes for the L1 when integrating:

- `status: queued` and `used-by: —` are deliberate. Per the round-23 precedent
  (`corpus/SOURCES.md:104-106`), a row becomes `mined` and gains its `used-by` once the note
  that cites it exists. The expected citing note for this round is
  `corpus/knowledge/system-pressure-r24.md`; flip the status and set
  `used-by: corpus/knowledge/system-pressure-r24.md` when that note lands. If the L1 prefers the
  round-23 style of admitting new rows directly as `mined` with the lesson in `used-by`, that
  is a legitimate alternative — I did not assume either.
- The anchor cell follows the round-23 convention (bare line range, `tag v7.2`, first-16
  sha256), matching S085–S089 at `corpus/SOURCES.md:91-95`.
- `recheck: on-release` matches every other kernel-at-v7.2 row in the registry.

## Narrow claim this source supports — and what it does NOT

**Supports (nothing beyond this):**

1. The Linux kernel has a boot parameter named `psi=`, tagged `[KNL]`, whose format is `<bool>`
   (lines 5505–5507).
2. Its stated effect is to enable or disable pressure stall information tracking.
3. Therefore PSI tracking is switchable at boot time; the mere fact that a host runs Linux does
   not guarantee that PSI tracking is on. This is a statement about kernel configuration
   vocabulary, not about any particular host.

**Does NOT support (each would need another source):**

- The layout of `/proc/pressure` — this file never mentions `cpu`, `memory`, `io` or `irq`
  pressure files, nor `/proc/pressure` at all.
- The meaning of the `some` / `full` lines, of `avg10` / `avg60` / `avg300`, or of `total`;
  and therefore no basis for any threshold rule or for interpreting an average as a stall
  microsecond count.
- That the `irq` resource exposes `full` only and no `some` line.
- That the system `cpu` `full` line is undefined or must never be read as "no stall".
- That a disabled PSI yields `EOPNOTSUPP` (or any particular errno) on read — the document
  states no error behaviour at all.
- The existence or semantics of `CONFIG_PSI` (zero occurrences in this file; that symbol
  belongs to the separate Kconfig source and to `kernel/sched/psi.c`).
- The default value of `psi=` when the parameter is not passed.
- Any cgroup-scoped pressure file, trigger, or threshold configuration.

**Adjacency note for the C2 tool:** the tool's state model (`absent` / `unsupported` /
`unreadable` / `malformed`) and its `full_system_undefined` flag are **not** grounded in this
document. They must be grounded in the `psi=`-adjacent code and cgroup sources the other seats
are opening (`kernel/sched/psi.c`, `include/uapi/linux/psi.h`, cgroup-v2 docs). This row may
be cited by `corpus/knowledge/system-pressure-r24.md` for the statement "PSI tracking is a
boot-time switch", and must not be cited as the authority for file layout, counter semantics
or error mapping.

## Draft `## Gate` block for `corpus/lessons/round-24.md`

```markdown
## Gate

| Row | URL | Located quote (≤25 words) | Decision / scope |
|---|---|---|---|
| S0xx | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/kernel-parameters.txt | 5505: “psi=		[KNL] Enable or disable pressure stall information” (entry continues on 5506 “tracking.” and 5507 “Format: <bool>”) | Admit A for the psi= boot parameter's name, format and stated effect only; no /proc/pressure layout, no counter semantics, no error mapping. |

Fetch receipt for the row above: HTTP 200, 317993 bytes, 8676 lines, accessed 2026-10-22T08:15:07Z
UTC; sha256 `23b1a690210b6884f040a6b1e5baf1fc18856e844d30d4784470bd210953340c` (first 16
`23b1a690210b6884`); raw bytes retained at
`.ufo/waves/round-24/evidence/sources/kernel-parameters.txt` if the L1 copies them in.
Verified anchors: 5505–5507 (the only `psi=` occurrence in the file), neighbours 5500–5503 and
5509 confirming a whole parameter entry; `CONFIG_PSI` does not appear in this document
(0 occurrences). A prior fetch attempt returned HTTP 429 with zero bytes and is not the source
of this digest.
```

Replace `S0xx` with the id the L1 assigns, and the evidence path with wherever the L1 actually
retains the bytes — I did not create anything under `.ufo/waves/round-24/evidence/`, since my
write bound is this report file only inside the lane repo.

## Touched surfaces

- **Created:** `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-24/w1/SrcKernelParams.md`
  (this report; the only file I created inside the lane repo).
- **Created outside the lane repo (read-only artifact, no code):**
  `/fast/scratch/hyaku/mori-r24-a2/src-kernelparams/kernel-parameters.txt` and
  `/tmp/mori-r24-src/kernel-parameters.txt` — the fetched upstream bytes.
- **Not touched:** `corpus/SOURCES.md`, `corpus/lessons/`, `corpus/knowledge/`, `tools/`,
  the lane's git index and jj state. No `git add/commit/stash/checkout/reset/pull/push`, no
  mutating `jj` command, no host writes, no `/proc` or `/sys` writes, no PSI trigger
  registration, no service or package changes.

## Out of scope / not done

- No edit to `corpus/SOURCES.md` (draft only, per the seat prompt).
- No `corpus/lessons/round-24.md` written (the L1 owns it; the Gate block above is a draft).
- No `corpus/knowledge/system-pressure-r24.md` written (separate seat).
- I did **not** open `Documentation/admin-guide/psi.rst` or the docs.kernel.org rendering of
  the same kernel-parameters document; the row is scoped to the tag-pinned v7.2 raw file that
  this seat was told to open, and the digest covers exactly those bytes.
- I did not check whether the `docs.kernel.org` rendering of `kernel-parameters.txt` carries
  the same entry; a rendering carries no stable line numbers, so the row anchors to the raw
  file only.
- No host PSI was read (out of the read-only detection scope of this seat; other seats own the
  live capture).

## Tooling

No install, upgrade or configuration change was performed in this seat; the task needed only
tools already present on the host (`curl` 8.23.0, coreutils `sha256sum` 0.8.0, `grep`,
`sed`, `awk`, `cat`, `stat`, Python 3.14.8 for JSON inspection only). Per the pacman guard, no
pacman transaction was attempted, and no host service was restarted.

## Findings summary

1. The `psi=` boot parameter is documented in the pinned v7.2 kernel-parameters file at lines
   5505–5507, and it is the only PSI-related boot parameter in that document.
2. The document supports exactly one narrow claim — `psi=` takes a boolean and switches
   pressure stall information tracking on or off at boot — and nothing about
   `/proc/pressure` files, counter semantics, per-resource kinds, error codes or
   `CONFIG_PSI`.
3. No existing `SOURCES.md` row cites this URL or this scope: the row is **new**, not a
   supersession of S001/S002.
