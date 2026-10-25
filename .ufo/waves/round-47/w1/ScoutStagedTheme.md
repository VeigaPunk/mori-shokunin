# ScoutStagedTheme — the FR13 / OOM-tracing theme in the staged shokuknow package

Round 47 · wave w1 · seat ScoutStagedTheme · lane `mori-shokunin`
Scope: survey `/home/vgpnk/Projects/shokuknow/merge/mori` for every staged knowledge file and
`SOURCES.append.md` row touching OOM tracepoints / eBPF / LSM; say what the lane already holds;
recommend ≥1 admit and ≥1 reject with reasons.
Read-only seat: no production file was touched. Scratch only under
`/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47-ScoutStagedTheme/`.

---

## 0. Method (commands, all read-only)

```
cd /home/vgpnk/Projects/shokuknow/merge/mori
grep -rn -i -E 'tracepoint|ebpf|mark_victim|lsm' .          # the assignment's pattern, recursive
grep -rn -i -o -E 'tracepoint|ebpf|mark_victim|lsm[a-z_]*' . | awk -F: '{print $1":"$2":"$3}' | sort -u
```

Supplementary (theme-adjacent, not the assignment's pattern, reported separately):
`grep -rn -i -E 'bpf|trace point|bpftrace|\bperf\b' --include='*.md' .` → only `SOURCES.append.md:28`
(S492, AgentCgroup) and the files already in the table; S492's only `bpf` token is the artifact URL
`github.com/eunomia-bpf/agentcgroup` — no OOM-tracepoint claim, so it is **not** a theme hit.

Lane-side state read with `git log/show/status`, `git ls-files`, `grep` on the working tree.

---

## 1. Every staged theme hit, with path:line

### 1.1 Staged knowledge files (75 new-file entries + 5 amendments)

| path | lines matching the pattern | token |
|---|---|---|
| `knowledge/corpus/knowledge/oom-tracing-tracepoints-r42.md` | 2 | `tracepoint` (title: "three named tracepoints") |
| | 4 | `eBPF`, `LSM` (source: S507 … §design (eBPF/LSM paragraph)) |
| | 6 | `mark_victim` (recheck: `pdftotext … grep -c 'mark_victim'` -> 3) |
| | 8 | `eBPF` (ground: FR13 "eBPF kill/OOM tracing") |
| | 12 | `tracepoint` (claim: "**exactly three named tracepoints**") |
| | 15 | `mark_victim`, `tracepoint` (quoted paper sentence) |
| | 17 | `eBPF` ("the concrete form of what FR13 calls eBPF kill/OOM tracing") |
| | 31 | `LSM`, `lsm_oom_kill_check` |
| | 33 | `lsm_oom_cleanup_container` |
| | 35 | `LSM` ("installed via standard LSM points …") |
| | 51 | `LSM` (boundary) |
| | 52 | `eBPF` (boundary) |
| `knowledge/corpus/knowledge/host-oom-activity-r42.md` | 39 | `tracepoint` — cross-reference only: "the kernel picks a victim by **per-process score**, with no notion of which workload it belongs to (`oom-tracing-tracepoints-r42.md`)" |
| `amendments/corpus/knowledge/oom-victim-context-r41.md` | 10 | `eBPF` (ground FR13) |
| | 25 | `eBPF` ("combining **eBPF-based monitoring with two") |
| | 26 | `LSM` ("lightweight LSM hooks**") |
| | 55 | `eBPF`, `LSM` ("install LSM hooks or eBPF programs") |

No other staged knowledge file matches. (For completeness: 52 of the 75 staged new-file entries
mention "OOM" at all — the OOM-family set is much wider than the tracepoint theme and is out of this
seat's scope.)

### 1.2 Staged `SOURCES.append.md` rows (136 rows, S471–S606)

| row | file:line | theme tokens | subject |
|---|---|---|---|
| **S501** | `SOURCES.append.md:37` | `eBPF`, `LSM` | ROMA paper, **abstract-level** claims via publisher Semantic Scholar record + OpenAlex; teaches the victim-selection claim; used-by `corpus/knowledge/oom-victim-context-r41.md` |
| **S507** | `SOURCES.append.md:43` | `tracepoint`, `mark_victim`, `lsm_oom_kill_check`, `lsm_oom_cleanup_container`, `eBPF`, `LSM` | ROMA paper, **full text** as deposited by the publisher; teaches "The OOM lifecycle an observer can hook is **named**: `mark_victim`, `start_task_reaping`, `finish_task_reaping`" + the two LSM hooks; used-by `corpus/knowledge/oom-tracing-tracepoints-r42.md` |
| S511 | `SOURCES.append.md:47` | (none — adjacent) | own-work host cgroup co-tenancy census; source of `host-oom-activity-r42.md` |

### 1.3 Package metadata (not staged content, listed for completeness)

`MERGE-REPORT.md:35` (the `oom-tracing-tracepoints-r42.md` new-file row), `MERGE-REPORT.md:111`
(the "row whose source the lane already holds" table: **S501 → S262**), `MERGE-REPORT.md:112`
(**S507 → S262**); `MERGE-REPORT.json:183-185` (the entry record: `kind: new-file`,
`collides_with_existing: false`, `duplicate_target: false`).

---

## 2. What the lane already holds

| staged item | lane holds it? | evidence |
|---|---|---|
| `oom-victim-context-r41.md` (amendment) | **YES, already held** — `corpus/knowledge/oom-victim-context-r41.md`, committed in round 42 (`git ls-files` confirms), sourced to **S262** (`corpus/SOURCES.md:243`, used-by `corpus/knowledge/oom-victim-context-r41.md`, 9 mentions of S262). The held file already carries a "Round-42 adoption provenance" block and a "Round-42 erratum (wave-1 CritS262Scope)" block. | `diff` staged-amendment vs held file → **no new claim**: the only differences are the row id (`S501`→`S262` in two sentences), `verified-at` (2026-10-23 vs 2026-10-24), the recheck line, the S262/S501 tokens, one boundaries sentence, and the held file's extra provenance/erratum sections. |
| `oom-tracing-tracepoints-r42.md` (new file) | **NO** — refused in round 42: `.ufo/waves/round-42/assimilation/refused-oom-tracing.md` (source S268 unreachable: ieeexplore HTTP 202 + 0-byte body), re-stated in `corpus/lessons/round-42.md:16` and `corpus/lessons/round-45.md:117`. Not in `git ls-files corpus/knowledge`. | `ls corpus/knowledge/oom-tracing-tracepoints-r42.md` → absent. |
| `host-oom-activity-r42.md` (new file) | **NO** — absent from `corpus/knowledge/` and from `git ls-files`. Its subject (per-cgroup OOM counters, local vs hierarchical scope) is partly adjacent to held `census-cgroup-levels-r45.md` and `observability-census-r1.md:134-140` (propagated-count / `memory.events.local` reads 0). | `ls` → absent; `grep -c 'S511' corpus/SOURCES.md` → 0. |
| S501 | **NO** as a row — but the *same paper/abstract* is already held as **S262** (`corpus/SOURCES.md:243`). `MERGE-REPORT.md:111` itself flags S501 as a row "whose source the lane's registry already holds" (→ S262). | `grep -c '^\| S501 \|' corpus/SOURCES.md` → 0; `grep -c '10.1109/TSC.2026.3698682' corpus/SOURCES.md` → 1. |
| S507 | **NO** — the lane holds only the abstract-level S262 for this DOI; no ROMA full-text row at the entering tip `2d85e33d` (`git show 2d85e33…:corpus/SOURCES.md` → 0 rows for S507, 0 rows for S475/S476/S477/S478, 1 ROMA row). The working tree (uncommitted) has a draft **S478** for exactly this source. | `grep -c '^\| S507 \|' corpus/SOURCES.md` → 0; `git status` → ` M corpus/SOURCES.md` with S475/S476/S477/S478 added. |
| S511 | **NO** — `grep -c 'S511' corpus/SOURCES.md` → 0. | |

---

## 3. Falsifiers for the staged theme (measured, not asserted)

**F1 — the staged headline is false at the kernel level.** The committed v7.2 copy of
`include/trace/events/oom.h` defines **eight** `TRACE_EVENT`s, not three:

```
$ grep -c '^TRACE_EVENT(' corpus/evidence/sources-r47/include_trace_events_oom.h
8
$ grep -n 'TRACE_EVENT(' corpus/evidence/sources-r47/include_trace_events_oom.h
12:TRACE_EVENT(oom_score_adj_update,
34:TRACE_EVENT(reclaim_retry_zone,
76:TRACE_EVENT(mark_victim,
118:TRACE_EVENT(wake_reaper,
134:TRACE_EVENT(start_task_reaping,
150:TRACE_EVENT(finish_task_reaping,
166:TRACE_EVENT(skip_task_reaping,
183:TRACE_EVENT(compact_retry,
```
(sha256 `82f04ad4108ba949…`, matching the frozen pin in `.ufo/waves/round-47/count-c2.py`.)

**F2 — the staged entry's own recheck does not measure what its headline claims.**
`recheck: 180d — pdftotext … | grep -c 'mark_victim' -> 3` counts *lines of the paper's text* that
mention `mark_victim`; it says nothing about how many tracepoints the kernel defines. The paper names
exactly three because it says **"such as"**:

```
$ pdftotext -enc UTF-8 <roma.pdf> - | sed -n '139,141p'
cleanup to within the correct container boundary. It leverages eBPF to hook into OOM-related kernel tracepoints such
as mark_victim, start_task_reaping, and finish_task_reaping to record OOM-triggering process
metadata. ROMA introduces two lightweight LSM hooks: (1)
```
The same PDF's design section (§"OOM Context Capture and Correlation") names the same three with the
`oom:` prefix — `oom:mark_victim`, `oom:start_task_reaping`, `oom:finish_task_reaping`
(`grep -o 'oom:[a-z_]*' | sort -u` → exactly those three, each ×2). A non-exhaustive example list
is not an inventory.

**F3 — the staged S507 row's own page-count cell is wrong.** S507 says the deposited PDF is
"2 357 114 B, **4 pages**". The byte count is right; the page count is not:

```
$ pdfinfo roma.pdf | grep -i pages      → Pages:           14
$ pdftotext roma.pdf - | tr -cd '\f' | wc -c  → 14
$ strings roma.pdf | grep -c '/Type */Page[^s]' → 14
```
(`file roma.pdf` prints "4 page(s)" — that heuristic misreads this file; `pdfinfo` and the text
extraction both say 14, and the published article spans pp. 3015–3028 = 14 pages.)

**F4 — the staged S501 row's pinned recheck is flaky, not reproducible.** S501 pins
`aaron papers fetch 10.1109/TSC.2026.3698682 -m s2 -> rc 0, 2213 bytes`. Measured today, 12 runs:

```
$ for i in $(seq 1 12); do aaron papers fetch 10.1109/TSC.2026.3698682 -m s2 > t.json; done
ok=6 fail=6      # failures: rc=1, 44 bytes, {"error":"s2: DOI not in Semantic Scholar"}
```
`auto` mode behaves the same way (8 runs: 4 ok / 4 fail). So the pinned recheck returns the recorded
result ~50 % of the time — the same "written-down receipt that was never reliably re-runnable"
class the round-46 closure flagged for `count-repins.py`.

**F5 — the held r41 entry's own recheck does not reproduce.** (Defect inside the theme the lane
already holds; reported, not fixed — outside my remit.)
`corpus/knowledge/oom-victim-context-r41.md:6` pins
`curl -fsSL 'https://api.openalex.org/works/…' | grep -c 'lack sufficient container context'` -> 1.
Today:

```
$ curl -fsSL 'https://api.openalex.org/works/https://doi.org/10.1109/TSC.2026.3698682' | grep -c 'lack sufficient container context'
0        # exit 1
$ grep -c 'lack sufficient container context' corpus/evidence/sources-r42/S262.oa.json
0        # exit 1
```
The literal phrase is absent because OpenAlex serves the abstract only as
`abstract_inverted_index`; the phrase exists solely after reconstructing the inverted index
(`python3` reconstruction → "…lack sufficient container context when selecting victim processes…",
offset 245). This is the round-42 `RevLesson.md` HIGH finding, still unrepaired at the entering tip
(`corpus/lessons/round-42.md` M3, `corpus/lessons/round-45.md:116-117`). The lane's own S262 recheck
cell (`corpus/SOURCES.md:243`, recheck `180d`) does not carry a command either.

---

## 4. Recommendations — ≥1 admit, ≥1 reject

### 4.1 REJECT (primary): the staged entry `oom-tracing-tracepoints-r42.md`, byte-exact

*Reasons* — F1, F2, and lane history agree:
1. Its headline claim ("**exactly three** named tracepoints", title line 2, claim line 12) is
   contradicted by the committed v7.2 header (eight `TRACE_EVENT`s, F1) and by the paper's own
   non-exhaustive "such as" (F2). Admitting it would install a false count into the corpus; the
   lane's own new criterion 124 (`corpus/QUALITY.md:1043-1046`) is written against exactly this row.
2. Its recheck (`grep -c 'mark_victim'` on the PDF) counts paper prose, not kernel events — a
   green receipt that cannot fail for the reason its headline asserts.
3. The lane already refused this file in round 42 with a written flip condition
   (`.ufo/waves/round-42/assimilation/refused-oom-tracing.md`); the flip condition was "a fetchable
   copy of the VOR PDF" — that condition is now met for the *source*, but the *claim* still fails
   (F1/F2). A flipped source does not revive a false claim.
4. The lane's own working tree already contains the corrected replacement,
   `corpus/knowledge/oom-tracepoints-r47.md` (untracked), with the eight-row catalogue.
5. It is byte-identical to the round-47 control `.ufo/waves/round-47/controls/control-c2-staged.md`
   (sha256 `b1d0aa8174f9ce5792cedd1f50b3a0febc29b6628e8a94d0657d775b2a916d71`, 3851 B, both) — i.e.
   the staged file *is* the "staged entry" counter-control.

### 4.2 REJECT: the staged amendment `amendments/corpus/knowledge/oom-victim-context-r41.md`

*Reasons* — the lane already holds this file (S262, round 42) and the amendment adds **no new
claim** (§2 diff). Worse, it would re-import the provenance the held entry's own erratum already
retired: its `source:` line claims "the publisher's Semantic Scholar record" and its recheck is
`aaron papers fetch … -m s2` — the very leg the held entry's round-42 erratum names as dead
(`{"error":"s2: DOI not in Semantic Scholar"}`, reproduced today, and flaky at ~50 % — F4). Its
claim sentence is also identical to the held one with the row id swapped. Admitting it would
duplicate the entry and downgrade a corrected provenance line to a stale one.

### 4.3 REJECT: staged row **S501** as a new registry row

*Reasons* — duplicate of a held row: `MERGE-REPORT.md:111` itself classifies S501 under "Rows
whose source the lane's registry already holds" (→ S262), and the lane holds S262 at
`corpus/SOURCES.md:243` with the same abstract-level scope and a located committed copy
(`corpus/evidence/sources-r42/S262.oa.json`). S501's only additions over S262 are a Semantic
Scholar carrier the lane's erratum already killed and a non-reproducible recheck (F4). Nothing new.

### 4.4 REJECT: staged row **S511** and its entry `host-oom-activity-r42.md`

*Reasons* — two independent grounds.
1. **Locator class.** S511's locator is `file:///home/vgpnk/Projects/shokuknow/lanes/mori/round5/.deepresearch/notes/cgroup-cotency.txt` — a sibling repo's own-work note. The lane has already refused rows on exactly this ground: S350 ("the staged failed-scope entry grounds its recheck in `systemctl reset-failed`…") and S351 ("grounds itself in a shokunow file:// note and a kernel MESSAGE grep, neither of which this lane may treat as evidence") — `corpus/SOURCES.md:247-248`.
2. **The measurement no longer reproduces.** The staged row claims `user.slice` "events[low 0 high 0 max 2677 oom 80 oom_kill 80 oom_group_kill 0 sock_throttled 360806]", captured 2026-10-23. Read-only on this host today:

```
$ cat /sys/fs/cgroup/user.slice/memory.events
low 0 / high 0 / max 0 / oom 0 / oom_kill 0 / oom_group_kill 0 / sock_throttled 11341
$ cat /sys/fs/cgroup/system.slice/memory.events   → all zero
$ cat /sys/fs/cgroup/init.scope/memory.events     → all zero
$ uptime -s        → 2026-10-25 13:36:19   (boot 0 began 13:36; prior boot ended 13:35:39)
$ journalctl --list-boots → 2 boots
```
The host rebooted after the capture, so the cgroup tree and its counters were recreated: the staged
"80 kills / 80 oom" figures are boot-scoped and are gone. The entry's own headline ("the subtree
that carries the kills is the subtree the lane's seats are in") rests on exactly those figures.

### 4.5 ADMIT (one genuine theme source): staged row **S507**'s substance, in corrected form

*Reasons* — S507 is the only staged theme item that carries something the lane does **not** hold:
the ROMA **full text** as opposed to the abstract-level S262. Concretely it adds the paper's own
two LSM hook names (`lsm_oom_kill_check()`, `lsm_oom_cleanup_container()`) and the paper's
eBPF-tracepoint sentence, which the abstract does not contain, and it is what makes the staged
entry's *wording* checkable at all.

But admit it **only after three corrections**, or it repeats the defects it is meant to fix:

| staged cell | staged value | correction |
|---|---|---|
| anchor | "the VOR PDF deposited by the publisher (2 357 114 B, **4 pages**)" | page count is **14** (F3); keep the byte count 2 357 114 B and pin sha256 `1603404dd25b3a0dff93f2dcb23c75b671d4e2d78da3cce8f461e87ebde6add2` (my own `sha256sum` of the sibling-repo copy `lanes/mori/round5/.deepresearch/notes/roma.pdf` — byte-identical to the working-tree S478 pin) |
| scope / teaches | "The OOM lifecycle an observer can hook is **named**: `mark_victim`, `start_task_reaping`, `finish_task_reaping`" | must read *the paper's own example list*, not an inventory of the kernel's tracepoints — the paper says "such as" (F2); the kernel's set at v7.2 is eight (F1). The lane's working-tree draft S478 already words it correctly: "The paper names three OOM tracepoints as examples (such as), not as the kernel's complete set" |
| used-by | `corpus/knowledge/oom-tracing-tracepoints-r42.md` | that file is refused (§4.1) — the row must name the entry that exists: `corpus/knowledge/oom-tracepoints-r47.md` (the working-tree draft). A used-by pointing at a refused file is a dangling citation |
| id | S507 | the lane's id space already reaches **S478**; S507 must not be re-used as a fresh id if the staged block is appended blindly (see §5) |

### 4.6 Also admissible (adjacent, not theme): nothing else in the theme needs admitting

`host-oom-activity-r42.md` and S511 could be re-offered as a *fresh lane-owned own-work row* on this
host after a new capture (the claim "OOM counters are per subtree, and the subtree the seats occupy
is the busy one" is exactly the kind of thing the lane's own `observability-census-r1.md` and
`census-cgroup-levels-r45.md` already approach) — but that is a new measurement, not an admission of
the staged package.

---

## 5. Hazard the L1 must not walk into: staged id space vs the lane's id space

The staged block assigns **S471–S606** (136 rows), because at staging time "lane registry currently
holds **243** rows; first staged id is `S471`" (`MERGE-REPORT.md:10`). The lane has since grown.
Comparison of the seven overlapping ids:

| id | staged subject | lane's own subject (entering tip / working tree) |
|---|---|---|
| S471 | gihyo 61st installment (cgroup v2 ⑥) | `proc(5)` 日本語訳 (Ubuntu focal) |
| S472 | gihyo 56th installment (cgroup v2 ①) | `proc(5)` 中文翻譯 (Arch) |
| S473 | iSulad `supervisor.c` | Linux cgroup-v2.rst @ v7.2 |
| S474 | openEuler 24.03 白皮书 | mori AXES calibration criterion |
| **S475** | **流程实例（分布式任务调度 XXL-JOB 版）(Aliyun)** | **Linux `include/trace/events/oom.h` @ v7.2 (the C2 source row)** |
| S476 | 阿里云 分布式多步骤事务 | v7.2 `mm_oom_kill.c` / `mm/page_alloc.c` / `fs/proc/base.c` (C2 call sites) |
| S477 | `xfs_quota(8)` | own-work host tracefs oom events (C2 host row) |

Appending the staged `SOURCES.append.md` verbatim would therefore **overwrite seven live lane rows**,
including **S475** — and `count-c2.py` requires S475 to be a `code`/tier-`A`/`mined` row whose source
cell names `v7.2` and `include/trace/events/oom.h` and whose used-by names the entry
(`.ufo/waves/round-47/count-c2.py:172-179`). Staged S475 is an Aliyun workflow doc: C2 would score
`source_row=bad`. **Take theme rows individually and re-id them; never append the staged block
wholesale.**

---

## 6. Tooling

No install or upgrade was needed or performed. `aaron` was already present
(`/home/vgpnk/.local/bin/aaron`, Node 24.21.0 via fnm) and was used read-only per `skill://aaron`;
`pdftotext`/`pdfinfo` (poppler), `curl`, `python3`, `git` (read-only) came from the host. No pacman
transaction was attempted (host-wide pacman pause).

---

## 7. Limits / UNVERIFIED

* **UNVERIFIED by me:** the fetch route for the publisher-deposited VOR PDF. My own measurement is of
  the byte-identical copy already on disk in the sibling repo
  (`/home/vgpnk/Projects/shokuknow/lanes/mori/round5/.deepresearch/notes/roma.pdf`,
  sha256 `1603404d…`, 2 357 114 B); the "IEEE opens it with a browser User-Agent" route is reported
  by the sibling seat `.ufo/waves/round-47/w1/ScoutROMA.md` and I did not re-run it.
* **UNVERIFIED:** whether the paper's "4 pages" in staged S507 came from `file` (which prints
  "4 page(s)" for this PDF) or from another tool — the staged cell is simply wrong against
  `pdfinfo`/`pdftotext` (F3).
* Not checked: the whole staged package outside the FR13 theme (135 other rows, 52 other OOM-family
  knowledge files, and the four sibling lanes' merge packages).
* Not checked: `corpus/lessons/round-47.md` (does not exist yet at the entering tip) and the
  round-47 `controls/` semantics beyond the byte-identity of `control-c2-staged.md` noted in §4.1(5).

---

## 8. Summary for the L1

1. Theme scope = 2 staged knowledge files + 1 staged amendment + 2 staged SOURCES rows (S501, S507);
   S511 is adjacent.
2. The lane already holds the r41 victim-context entry (S262) with a corrected provenance line and an
   erratum; the staged amendment is a duplicate of it that would re-import the dead Semantic-Scholar
   leg → **reject**.
3. The staged tracepoints entry claims "exactly three" where the committed v7.2 header defines
   **eight** and the paper says "such as" → **reject** (and it is byte-identical to the round-47
   staged control).
4. The one admissible staged source is the ROMA **full text** (S507), admitted only with the page
   count corrected to **14**, the scope re-worded as "the paper's own example list", the used-by
   repointed at `corpus/knowledge/oom-tracepoints-r47.md`, and a fresh lane id — the working tree's
   draft **S478** already satisfies this.
5. Two live defects found in the theme the lane already holds: the r41 recheck pin
   (`grep -c 'lack sufficient container context'`) returns 0, not 1 (F5), and the `aaron -m s2`
   recheck the staged S501 pins is ~50 % flaky (F4).
6. **Do not append the staged `SOURCES.append.md` wholesale** — staged S471–S477 collide with seven
   live lane rows, and staged S475 would destroy the C2 source row.
