# SrcPsiRst — round-24 C2 sourced frontier step (draft only; lane file NOT edited)

Seat: `MoriR24.SrcPsiRst` (leaf, no subagents). Surface claimed: **one** `SOURCES.md` row
for the Linux v7.2 `Documentation/accounting/psi.rst`, plus a `## Gate` block for the
round-24 lesson.

Lane file status: **not edited.** `corpus/SOURCES.md` is byte-unchanged on disk; this
report carries the draft row and the draft `## Gate` block for the L1 to admit. No `git`
or `jj` command was run against the lane repo, its index or its history by this seat.

---

## 1. Fetch record (provenance)

| Item | Value |
|---|---|
| URL | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst |
| UTC access time (first fetch) | **2026-10-22T08:14:33Z** (`date -u` printed immediately before the `curl` in the same command) |
| UTC access time (second, metadata-bearing fetch) | 2026-10-22T08:36:10Z |
| HTTP status (second fetch) | `http_code=200`, `url_effective` identical to the request URL, `content_type=text/plain; charset=utf-8` |
| Bytes | 6792 (both fetches; `size_download=6792`) |
| Lines | 188 |
| SHA-256 (full, both fetches) | `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692` |
| **SHA-256 (first 16 hex)** | **`11c6b7129103b454`** |
| Fetch reproducibility | `cmp` of the two independent fetches → identical bytes |
| Tool | `curl 8.23.0` (system package, **no install performed**), `sha256sum 0.8.0` (coreutils, system), `python3 3.14.8` (system), `awk`/`grep`/`sed`-free numbered reads |
| Local copy (outside the lane repo) | `/tmp/mori-psi-rst/psi.rst` (+ `psi-second.rst`, `master-psi.rst`, `psi.c`, `psi-docs.html`) |

Commands actually run:

```
$ mkdir -p /tmp/mori-psi-rst && curl -fsSL -o /tmp/mori-psi-rst/psi.rst \
    https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst \
    && date -u +%Y-%m-%dT%H:%M:%SZ && sha256sum /tmp/mori-psi-rst/psi.rst
2026-10-22T08:14:33Z
11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692  /tmp/mori-psi-rst/psi.rst

$ date -u +"%Y-%m-%dT%H:%M:%SZ" && curl -sS -f -o psi-second.rst \
    -w "http_code=%{http_code}\nsize=%{size_download}\nurl_effective=%{url_effective}\ncontent_type=%{content_type}\n" \
    https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst
2026-10-22T08:36:10Z
http_code=200
size=6792
url_effective=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst
content_type=text/plain; charset=utf-8
$ sha256sum psi-second.rst && cmp psi.rst psi-second.rst
11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692  psi-second.rst
IDENTICAL to first fetch
```

**Version-stability note (fetched, not assumed):** the same path at
`https://raw.githubusercontent.com/torvalds/linux/master/Documentation/accounting/psi.rst`
fetched 2026-10-22T08:14Z has the **identical SHA-256**
(`11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692`) and `diff` against
the v7.2 bytes reports no difference. The document text has not changed between the
`v7.2` tag and `master` as of the access date, so the line anchors below are stable
across both refs.

## 2. Line anchors verified in the fetched bytes

Anchors were established by printing the fetched file with its own line numbers
(`awk 'NR>=a && NR<=b {printf "%d: %s\n", NR, $0}'`), so every number below is the fetched
file's numbering. Quoted strings are byte-exact, whitespace-normalized across the
source's own line wraps.

| Anchor | Lines | Verified content |
|---|---|---|
| `Pressure interface` heading | 34–35 | section heading |
| documented `/proc/pressure/` file set | 37–38 | "Pressure information for each resource is exported through the respective file in /proc/pressure/ -- cpu, memory, and io." — **no `irq`** |
| line format | 40–43 | `some avg10=0.00 avg60=0.00 avg300=0.00 total=0` / `full avg10=0.00 avg60=0.00 avg300=0.00 total=0` |
| `some` meaning | 45–46 | share of time in which at least some tasks are stalled on a given resource |
| `full` meaning | 48–55 | share of time in which all non-idle tasks are stalled on a given resource simultaneously; thrashing |
| system CPU `full` undefined | 57–58 | "CPU full is undefined at the system level, but has been reported since 5.13, so it is set to zero for backward compatibility." |
| avg windows and units | 60–65 | "The ratios (in %) are tracked as recent trends over ten, sixty, and three hundred second windows" … "The total absolute stall time (in us) is tracked and exported as well" |
| trigger write format | 81–83 | `<some\|full> <stall amount in us> <time window in us>` |
| trigger examples | 85–88 | `"some 150000 1000000"` into `/proc/pressure/memory`; `"full 50000 1000000"` into `/proc/pressure/io` |
| trigger window bounds | 102–103 | "The kernel accepts window sizes ranging from 500ms to 10s, therefore min monitoring update interval is 50ms and max is 1s." |
| unprivileged window rule | 108–110 | unprivileged monitors: window size must be a multiple of 2s |
| trigger lifetime | 118–119 | "The trigger will de-register when the file descriptor used to define the trigger is closed." |
| cgroup2 file set | 181–185 | per-cgroup `cpu.pressure, memory.pressure, and io.pressure` files, "the format is the same as the /proc/pressure/ files" |

**Negative checks performed on the fetched bytes (both empty):**

```
$ grep -n -i 'irq' psi.rst          → exit 1, no output
$ grep -n -i 'eopnotsupp\|EACCES\|EPERM\|ENOENT' psi.rst → exit 1, no output
```

(The only `errno` occurrences in the file are inside the C usage example, lines 126–164.)

## 3. Duplicate / supersession check against `corpus/SOURCES.md`

Registry read: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` — 141 lines,
89 rows S001–S089 (registry table at lines 7–95), 11 columns, `NF=13` for every row.

- `grep -rn 'accounting/psi.rst' corpus/` → **no match**. No row in this lane uses the
  raw v7.2 psi.rst URL.
- S001 = `https://docs.kernel.org/accounting/psi.html` — the **rendered** docs page for
  the *same upstream document*; scope "Linux PSI counters, totals, thresholds and
  per-cgroup files"; anchors "Pressure interface:74-77; Monitoring for pressure
  thresholds:104-119; Cgroup2 interface"; status `mined`; opened 2026-10-19;
  used-by `corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md`.
- S002 = `https://docs.kernel.org/admin-guide/cgroup-v2.html` — different document
  (cgroup-v2 memory events / `memory.peak`), not the PSI interface.
- Other pressure-adjacent rows: S007 (`systemd-oomd.service(8)`), S010
  (`systemd.io/PRESSURE/`), S021 (LWN BPF OOM proposal), S033 (`iostats.html`) — none
  names psi.rst.
- Sibling lanes: `grep -rn 'accounting/psi\|sched/psi.c' /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md`
  returns **only** the mori lane's S001 line. No other lane has a psi.rst row.
- Read-only census run (not a mutation):
  `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
  → for mori: `W04` for six pre-existing same-URL pairs (S035/S037/S073/S074/S075/S076),
  then `ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`. **No W04/E04
  would be triggered by a row using the raw psi.rst URL**, because that URL is unique in
  the lane (E04 is "duplicate url **within scope**"; W04 is "same url across scopes" —
  neither applies to a URL no row carries).

**Determination: NEW row, not a supersession.** S001's claims are not corrected or
withdrawn by the v7.2 file — the same text is still true; S001 also keeps a live
`used-by` (the 2026-10-15 free-lunch lesson) and its own distinct scope (rendered-page
anchors, per-cgroup files, trigger lifetime). Under CORPUS.md rule 2 a supersession row
must open `supersedes S0NN —` because it *corrects* an earlier inference, and nothing here
corrects S001. The new row is **adjacent** to S001, and is scoped to what only the
version-pinned, byte-anchored source gives: the v7.2 line grammar, the unit semantics of
`avg10/60/300` (percent) and `total` (microseconds), the system-CPU-`full` undefined-and-
zeroed-for-compat rule, and the trigger **bounds**. The overlap with S001 is at the
document level and is declared in the row's own scope cell; the row does not restate
S001's trigger-lifetime teaching as its own claim.

Coordination: peer `MoriR24.ConnectSourceDuplicates` independently reported the same
"psi.rst never mentions IRQ" fact and the same new-row/no-supersession determination
before this report was written; it was confirmed here from the fetched bytes (§2) and
adopted. The same peer then reviewed this draft and proposed one tightening, which is
applied: the `teaches` cell said "each file is exactly two lines", but psi.rst:40–43
shows the two-line format for the resources the document names and never says "exactly"
— and the real IRQ file emits one line (`only_full = res == PSI_IRQ`, psi.c:1274). The
cell now reads "each named file (cpu, memory, io) shows a some line and a full line", and
the matching sentences in §6 item 2 and in finding F-2 were reworded the same way. The
peer also noted that 57–58 ties "since 5.13" to CPU `full` *being reported*, with zero
as the backward-compatibility value; the `teaches` cell and the anchor cell now say
"reported as zero since 5.13" rather than tying the zero itself to 5.13. No other peer is
asked for anything by this seat.

## 4. Draft row for `corpus/SOURCES.md` (id left as `S0xx` for the L1)

Header (line 5), for shape reference — 11 cells:
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`

Draft row (one line, 11 cells, in the S077–S089 style; **no `|` inside any cell**):

```
| S0xx | Linux PSI accounting documentation v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst | docs | A | the v7.2 system PSI interface only: the /proc/pressure/ file set the document names, the some/full line grammar, the unit and window semantics of avg10/avg60/avg300 and total, the system-level CPU full rule, and the trigger format and window bounds; v7.2 only | pressure interface heading:34-35; documented file set:37-38; line format:40-43; some meaning:45-46; full meaning:48-55; system CPU full undefined, reported as zero since 5.13:57-58; avg windows and total unit:60-65; trigger format and examples:81-88; trigger window bounds:102-110; trigger lifetime:118-119; cgroup2 file set:181-185; tag v7.2; sha256 11c6b7129103b454 | The document names only cpu, memory and io as the /proc/pressure/ files; each named file (cpu, memory, io) shows a some line and a full line, some for time in which at least some tasks are stalled and full for time in which all non-idle tasks are stalled; avg10/60/300 are percentages over 10/60/300-second windows and total is absolute stall time in microseconds; system-level CPU full is undefined and, since 5.13, has been reported as zero for backward compatibility, so a zero full value carries no information; trigger windows are accepted from 500ms to 10s, so the minimum monitoring update interval is 50ms and the maximum 1s. | queued | 2026-10-22 | on-release | — |
```

Cell-by-cell justification:

| cell | value | why |
|---|---|---|
| id | `S0xx` | id left for the L1 to assign. The registry's next free id is **S090**, and round-24 needs at least eight more source rows (psi.c, cgroup-v2.rst, init/Kconfig, kernel-parameters.txt, proc_pressure(5), psi_types.h, the PSI_IRQ commit, plus this one) — so the L1 should assign from S090 upward in a single block. |
| source | `Linux PSI accounting documentation v7.2 — <raw URL>` | matches the S077–S089 naming shape (`Linux <file> at v7.2 — <raw URL>`); the URL is pinned to tag `v7.2` |
| kind | `docs` | precedent: S077 (`xfs.rst`), S082 (`proc.rst`), S083 (`ext4.rst`), S084 (`tmpfs.rst`) are all `Documentation/**.rst` files with kind `docs`; the registry's kind vocabulary is fixed (`docs`=48, `code`=20, `spec`=9, `tool`=4, `community`=3, `book`=2, `paper`=2, `own-work`=1) and `docs` introduces no new value |
| tier | `A` | primary upstream kernel documentation at a pinned tag, for its stated scope only — same tier basis as S077–S089 |
| scope | the v7.2 system PSI interface only, with the file set, line grammar, unit/window semantics, system-CPU-`full` rule and trigger bounds; `v7.2 only` | narrow by design: it does not claim IRQ pressure (absent from the document, §2), does not claim cgroup2 `irq.pressure`, does not claim error/errno semantics, and does not claim host state. The `; v7.2 only` marker matches S087–S089's convention |
| anchor | the ten verified line ranges + `tag v7.2` + `sha256 11c6b7129103b454` | every line number was printed from the fetched bytes; digest style matches S077–S089 (16 hex chars) |
| teaches | one grounded benefit covering the file set, the two-line grammar, the unit semantics, the zero-for-compat CPU-full rule and the trigger bounds | each clause is tied to a verified anchor in §2; the "only cpu, memory and io" wording is the document's own list (37–38) and does not claim the kernel's complete file set |
| status | `queued` | the draft state, matching the round-23 draft precedent (`.ufo/waves/round-23/build/DraftSourceRows.md`: `status=queued`, `used-by=—`). **`corpus/lessons/round-24.md` does not exist yet**, so a `mined` row citing it would fail the registry census check "mined rows whose used-by paths do not exist — must print nothing" (CORPUS.md:146-147) |
| opened | `2026-10-22` | UTC fetch date (§1) |
| recheck | `on-release` | the URL is pinned to the `v7.2` tag; recheck on a kernel release bump (same cadence as S077–S089) |
| used-by | `—` | no citing artifact exists yet |

**Exact post-landing cell values for the L1** (apply only once the citing files exist):

- `status`: `queued` → `mined` once `corpus/lessons/round-24.md` exists and its `## Gate`
  records this row.
- `used-by`: `—` → `corpus/lessons/round-24.md`; then append
  `corpus/knowledge/system-pressure-r24.md` after that knowledge note exists and cites
  the row (it does not exist today — `corpus/knowledge/` has no `system-pressure-r24.md`).
  Log each old→new change in the round-24 lesson, per CORPUS.md rule 2.

## 5. Draft `## Gate` block for `corpus/lessons/round-24.md`

Round-23 lesson Gate shape is `| Row | URL | Located quote (≤25 words) | Decision / scope |`;
the round-24 Gate additionally needs the access date and the verified line anchors, both
of which are given here.

```markdown
## Gate

One new source row for the C2 pressure step; no supersession. `corpus/SOURCES.md` has no
row for `Documentation/accounting/psi.rst` (`grep -rn 'accounting/psi.rst' corpus/`
returns nothing), and S001 (docs.kernel.org/accounting/psi.html) keeps its scope: the
rendered page's counters, thresholds and per-cgroup files. This row is adjacent to S001,
not a correction of it. The row is scoped to the v7.2 system PSI interface and, per the
document's own file list, does not cover IRQ pressure.

URL: https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst
Access date: 2026-10-22 (UTC), first fetch 2026-10-22T08:14:33Z, second fetch
2026-10-22T08:36:10Z; HTTP 200; 6792 bytes; 188 lines; both fetches byte-identical.
SHA-256 of the fetched bytes: 11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692
(first 16 hex: 11c6b7129103b454).

| Row | URL | Located quote (≤25 words) | Decision / scope |
|---|---|---|---|
| S0xx | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst | 57–58: "CPU full is undefined at the system level, but has been reported since 5.13, so it is set to zero for backward compatibility." (23) | Admit A for the v7.2 system PSI interface: file set, some/full grammar, unit semantics, system CPU full rule, trigger bounds. Not for IRQ pressure, not for errno states, not for host state. |

Line anchors verified in the fetched bytes (line numbers are the fetched file's own):
documented file set 37–38; line format 40–43; `some` meaning 45–46; `full` meaning
48–55; system CPU full undefined, reported as zero since 5.13 57–58; avg windows and total unit
60–65; trigger write format 81–83; trigger examples 85–88; trigger window bounds
102–103; unprivileged window rule 108–110; trigger lifetime 118–119; cgroup2 file set
181–185.

Additional located quotes (≤25 words each, same fetch):
- 37–38: "Pressure information for each resource is exported through the respective file
  in /proc/pressure/ -- cpu, memory, and io." (18)
- 102–103: "The kernel accepts window sizes ranging from 500ms to 10s, therefore min
  monitoring update interval is 50ms and max is 1s." (21)
- 45–46: "The "some" line indicates the share of time in which at least some tasks are
  stalled on a given resource." (20)

Reject: that this document describes the kernel's complete `/proc/pressure/` file set —
it names only `cpu`, `memory` and `io` (`grep -n -i irq psi.rst` is empty), so IRQ
pressure is not taught here; that a zero system-CPU `full` line means no stall — the
document says the value is zero only for backward compatibility; that the trigger window
bounds describe a read interval or a sampling cadence — they bound trigger registration
windows, and the doc says nothing about how a reader should space two reads.

No existing immutable registry row is edited. The row enters `mined` with used-by this
lesson and gains the knowledge note only after `corpus/knowledge/system-pressure-r24.md`
exists and cites it.
```

## 6. The narrow claim this source supports — and what it does NOT support

**Supports (each clause tied to a verified line):**

1. **The file set this document names** (37–38): pressure information is exported per
   resource through the respective file in `/proc/pressure/` — `cpu`, `memory` and `io`.
   The same format is used by the per-cgroup files `cpu.pressure`, `memory.pressure`,
   `io.pressure` (181–185).
2. **The line grammar** (40–43): the format shown for each named resource is a `some`
   line and a `full` line, each `avg10=… avg60=… avg300=… total=…`. The document
   presents this two-line format for the resources it names; it does not state that
   every file is two lines, and it says nothing about any other file's line count.
3. **`some` vs `full` semantics** (45–55): `some` = share of time in which at least some
   tasks are stalled on the resource; `full` = share of time in which all non-idle tasks
   are stalled on the resource simultaneously (thrashing), tracked and exported
   separately.
4. **Units and windows** (60–65): the `avg10/60/300` values are **ratios in percent**,
   tracked as trends over 10-, 60- and 300-second windows; `total` is **absolute stall
   time in microseconds**, exported separately precisely so latency spikes do not have to
   show up in the averages.
5. **System-level CPU `full`** (57–58): undefined at the system level; since 5.13 it has
   been reported, and it is set to zero for backward compatibility.
6. **Trigger registration** (81–88, 102–110, 118–119): the write format
   `<some|full> <stall amount in us> <time window in us>`; examples `some 150000 1000000`
   on `memory` and `full 50000 1000000` on `io`; accepted window sizes 500ms–10s, hence
   a minimum monitoring update interval of 50ms and a maximum of 1s; unprivileged
   monitors need a window that is a multiple of 2s; a trigger de-registers when its file
   descriptor is closed.

**Does NOT support (explicit limits for the L1, the C2 knowledge note and the tool's
decision table):**

- **IRQ pressure.** The document never mentions `irq` (`grep -n -i 'irq'` is empty) and
  its file list is `cpu, memory, and io` only. Nothing here supports a claim that IRQ
  pressure exists, that it is exported as a `full`-only file, or that a missing `some`
  line for IRQ is normal. Those facts live in `kernel/sched/psi.c` v7.2
  (`only_full = res == PSI_IRQ` at psi.c:1274, the `full`-only emission at
  psi.c:1277/1290–1291, `psi_irq_show` at psi.c:1684–1687, and
  `proc_create("pressure/irq", …)` at psi.c:1717–1719) — the `SrcPsiC` row's scope, not
  this one.
- **Error and errno semantics.** The document contains no `EOPNOTSUPP`, `EACCES`,
  `EPERM` or `ENOENT` and says nothing about a PSI-disabled kernel, a missing file, a
  permission failure or a malformed line. The contract's absent / unsupported /
  unreadable / malformed / counter_regressed mapping is **not** sourced from this
  document.
- **A calibrated threshold.** No threshold value, no verdict rule and no notion of a
  "high" pressure level appears. The `--warn-avg10` default is a local choice; the
  document only fixes the *unit* (percent, line 60).
- **Which `some`/`full` kind to threshold on.** The document defines both kinds but
  prescribes no thresholding rule; the contract's choice of kinds per resource is a
  local decision, not a documented one.
- **The `total` aggregation semantics.** The document calls `total` "absolute stall time
  (in us)" and does not say whether it is a per-CPU sum or a normalized wall-clock
  quantity. (For the record, `kernel/sched/psi.c` normalizes per-CPU buckets by
  non-idle time before adding them to the group total — psi.c:372–411 — which is a
  psi.c fact, not a psi.rst fact.) A `stall_ratio = total_delta_us / (S * 1e6)` reading
  therefore rests on the code row, not on this document.
- **cgroup-scoped CPU/IO/IRQ pressure and any resident trigger watcher.** The cgroup2
  section (178–188) only says per-cgroup files exist and share the format.
- **Host state.** This is upstream documentation; it says nothing about whether any
  particular host exposes PSI, and no live host read is evidence for it. (Read-only
  observation on this host, recorded as host state and **not** as a source claim:
  `/proc/pressure/irq` exists and contains only a `full` line — consistent with the
  psi.c row, and not derivable from this document.)
- **Version generality.** The anchors and digest are v7.2-only.

## 7. Findings reported to the canonical Rust judge (verbatim, no interpretation added)

- **F-1 — the wave prompt's "Teaches" list for this row overreaches on IRQ.** The
  dispatch text asks this row to teach "the PSI interface: file format, some/full
  meaning, system-level CPU full, **IRQ pressure**, total units, avg windows, trigger
  bounds". The v7.2 `Documentation/accounting/psi.rst` does not document IRQ at all:
  `grep -n -i 'irq'` over the fetched bytes is empty, and the file list at 37–38 reads
  "cpu, memory, and io". The drafted row therefore excludes IRQ from both scope and
  teaches, and the IRQ part of the C2 claim must be carried by the `kernel/sched/psi.c`
  row and the PSI_IRQ commit row.
- **F-2 — the C2 contract's "irq needs `full` only" rule has no support in this
  document.** The grammar at 40–43 is presented for the resources the document names
  as a `some` line then a `full` line; the document never carves out a `full`-only
  resource and never states a line count for any other file. The
  carve-out is `kernel/sched/psi.c` v7.2 (`only_full = res == PSI_IRQ`, psi.c:1274;
  loop bound `full < 2 - only_full`, psi.c:1277). Peer `MoriR24.ConnectSourceDuplicates`
  reported the same absence from the same URL.
- **F-3 — the contract's absent/unsupported/unreadable/malformed/counter_regressed
  vocabulary is not taught by this document.** No errno name and no malformed-line rule
  appears in it (only the C usage example mentions `errno`, lines 126–164).
- **F-4 — `avg10` is a percentage, not a microsecond count.** Lines 60–65: "The ratios
  (in %) are tracked as recent trends over ten, sixty, and three hundred second
  windows"; `total` is the microsecond quantity. The contract's `--warn-avg10 10.0`
  therefore compares a percent value, and the tool's threshold unit should say so.
- **F-5 — system CPU `full` is zero for backward compatibility, not because there is no
  stall.** Lines 57–58: "CPU full is undefined at the system level, but has been reported
  since 5.13, so it is set to zero for backward compatibility." This supports the
  contract's `full_system_undefined: true` label and its rule that system CPU `full` is
  never evidence of no stall — and it also shows the zero is a compatibility value, so
  "no stall" cannot be inferred from it either.
- **F-6 — the trigger bounds are registration-window bounds, not read-interval bounds.**
  Lines 102–103: "The kernel accepts window sizes ranging from 500ms to 10s, therefore
  min monitoring update interval is 50ms and max is 1s." The document says nothing
  about how a reader should space two reads of `/proc/pressure/*`, so it does not
  constrain the contract's `--interval S` range or justify `stall_ratio` as a
  wall-clock fraction.
- **F-7 — the document text is identical at `v7.2` and `master` as of 2026-10-22.**
  Same SHA-256 `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692`,
  `diff` reports no difference. The `v7.2` anchors are therefore stable against
  `master` today, but the digest must still be re-checked before reuse.
- **F-8 — no `## Gate` wording may imply a complete file list.** Both the row's scope
  cell and the Gate block say the document *names* `cpu`, `memory` and `io`; the kernel's
  complete set at v7.2 also includes `pressure/irq` (psi.c:1717–1719), which this
  document does not mention.
- **F-9 — registry shape facts for the L1.** `corpus/SOURCES.md` currently holds 89 rows
  (S001–S089), the next free id is S090, every row is `NF=13` (11 cells), and the
  read-only census `validate --root /home/vgpnk/Projects/shokunin mori` reports only the
  six pre-existing W04 same-URL pairs and then `ok` for this lane — a new row using the
  raw psi.rst URL raises neither W04 nor E04.

## 8. Out of scope (deliberately not done)

- `corpus/SOURCES.md` was **not** edited; no registry row was appended, no id assigned,
  no search-log or `## Paths` entry written. Registry writes are the L1's.
- `corpus/lessons/round-24.md` was **not** created or edited — the `## Gate` text above
  is a draft for the L1 to paste.
- `corpus/knowledge/system-pressure-r24.md` was **not** written (it belongs to seat
  `DraftKnowledgeEntry`); no `SKILL.md` decision table was drafted.
- No `tools/mori-pressure.py` was written, read, run or located; the tool and the frozen
  case fixture are other seats' surfaces.
- No PSI trigger was registered, no `/proc`, `/sys` or cgroup file was written, no
  service was restarted, no package was installed or updated.
- No `git add/commit/stash/checkout/reset/pull/push` and no mutating `jj` command was run
  in the lane repo; no sibling lane was touched. Read-only git was not needed.
- No subagent was dispatched (leaf seat).

## 9. Touched surfaces

| path | write | note |
|---|---|---|
| `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-24/w1/SrcPsiRst.md` | created | this report — the only file created inside the lane repo |
| `/tmp/mori-psi-rst/` | created | fetched upstream bytes (psi.rst, second fetch, master psi.rst, psi.c, rendered psi.html) and derived text — outside the lane repo, untracked, disposable |
| `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` | **not written** | L1 owns the registry |

## 10. Tooling record (tooling directive)

No tool was installed or updated by this seat — none was needed. The work used only
preinstalled system tools: `curl 8.23.0` (system package), `sha256sum 0.8.0` (coreutils,
system), `python3 3.14.8` (system), `awk`/`grep`/`cmp`/`diff`/`wc`/`date` (system).
No `pacman`, `uv`, `npm` or `cargo` transaction was executed, so no pacman-guard
consideration arises and nothing needs to be recorded against the update-safety gate.

## 11. Post-landing reconciliation (2026-10-22, after the wave-1 integration)

The L1 integrated this seat's row **during** this round, before the peer-review tightening
in §3 landed. The committed registry now carries the row as **S090** (commit `df4db54`
"round-24: sources S090-S097, system pressure knowledge entry, lesson, evidence"; also in
`HEAD:corpus/SOURCES.md`), with `status=mined`, `opened=2026-10-22`, `recheck=on-release`,
`used-by=corpus/knowledge/system-pressure-r24.md, corpus/lessons/round-24.md`. The lesson
Gate (`corpus/lessons/round-24.md:25`) records the same URL, access time
2026-10-22T08:14:33Z, digest `11c6b7129103b454`, the anchors 37–38, 40–43, 57–58,
60–65, 102–110, 181–185, and the 23-word quote from 57–58 — matching this report's §1/§2.

**The landed cells were integrated from the pre-tightening wording.** Two cells differ from
this report's final draft:

| cell | landed in S090 (pre-tightening) | this report's tightened wording |
|---|---|---|
| anchor | `system CPU full undefined and zeroed since 5.13:57-58` | `system CPU full undefined, reported as zero since 5.13:57-58` |
| teaches | `… each file is exactly two lines, some for … and full for …` | `… each named file (cpu, memory, io) shows a some line and a full line, …` |

**Residual wording judgment (for the L1 / judge).** The phrase "each file is exactly two
lines" in the landed teaches cell is scoped by the row's own scope cell ("the file set the
document names" — cpu, memory, io only), and for those three documented files the source
shows exactly the two-line format. The word "exactly" is a small overstatement relative to
psi.rst:40–43, which *shows* the format rather than stating line counts; it is safe within
scope but would be wrong if a reader lifted it onto the undoc'd IRQ file (which emits one
`full` line — psi.c:1274, 1277, 1290–1291). The derived knowledge entry
`corpus/knowledge/system-pressure-r24.md` states "Each file holds two lines" in F2 (line
34) but immediately delimits IRQ in F5 (line 63: "An IRQ file therefore carries one `full`
line") and F1 (lines 29–32: "the documentation is not an inventory of the file set"), so
the note is internally consistent; the only phrase worth narrowing is F2's "Each file

**Final coordination with `MoriR24.ConnectSourceDuplicates` (2026-10-22).** The
duplicate-connector peer re-verified at tip `6fce88a` that S090–S097 landed in
`df4db54`, the census still reports exactly the six inherited W04s and exits 0, and it
**recommends against** a supersession row for S090: within S090's scope (the files the
document names — cpu/memory/io) the two-line claim is true in v7.2 (psi.c:1273–1277,
`only_full` is IRQ-only), and "zero since 5.13" matches psi.rst:57–58; CORPUS.md rule 2
reserves `supersedes` for corrections, and a narrowing-only row would add a same-URL row
with no change of truth. The peer concurs that the **real** over-reach risk is the
knowledge note `corpus/knowledge/system-pressure-r24.md:34` ("Each file holds two lines",
stated right after F1 introduces the undoc'd IRQ file); the agreed fix is an L1 knowledge
edit narrowing that sentence to "Each of cpu, memory and io", which the peer records in
its report §6b. This seat adopts that recommendation: no supersession row is proposed,
and this report's §11 remains the registry-side record of the landed wording only.


Census after integration (read-only): 97 rows, 0 malformed (`NF!=13`), no duplicate ids,
kind/tier/status enums clean; `git status --porcelain` shows 0 modified tracked files
(integration is committed); `corpus/SOURCES.md` is unchanged by this seat.

## 12. Known limits of this seat's work


- The row is a **draft**. Nothing was admitted to the registry by this seat; the L1
  assigned `S090` and integrated it (see §11). No `mined` status was claimed here, no
  id was assigned here, and no `used-by` path was asserted here for a file that did not
  exist at drafting time.
- Anchor line numbers are the **fetched file's own** numbering for the bytes whose
  SHA-256 is `11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692`. A
  re-fetch must be digest-checked before the anchors are trusted again.
- Tier A is scoped to the row's own `scope` cell, not a global claim about the
  document's authority.
- §7 is source reading only. It is not a verdict on the frozen C2 contract: F-1 through
  F-6 are inputs for the L1, for the C2 knowledge note and for the wave-2
  falsification, not changes to the contract.
- The `used-by` cell proposed for the landing moment (`corpus/lessons/round-24.md`)
  referred to a lesson that did not exist at drafting time; the L1 created it before
  flipping `status` to `mined` (see §11), so the census check "mined rows whose used-by
  paths do not exist" passes for the integrated row.

