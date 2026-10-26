# Mo50ScribeRowOomKill — round 50 w1 — draft lane SOURCES row S491 and prove it is W04, not E04

Seat: leaf scribe, mori-shokunin lane, wave w1 (build + first falsifiers).
Assignment: draft row S491 for `Linux mm/oom_kill.c at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c`
(11 columns, no `|`, kind `code`, tier `A`, scope = which report block a memcg OOM vs a global OOM prints
(dump_header branch) and the victim line's per-type RSS fields and units, status `mined`, opened `2026-10-26`,
recheck `on-release`, used-by `corpus/knowledge/oom-memcg-stat-r50.md`), and show the row is a W04 warning, not an
E04 error. Report only; no lane file was edited. Report path `Mo50ScribeRowOomKill.md` is written relative to
`/home/vgpnk/Projects/shokunin/mori-shokunin`.

Frozen contract read first: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/contract.md`
(sha256 per `evidence/freeze-sha256.txt` = `8290c6d477adb603a44d36bc3cd1d4930e590bc978f1284520304eac6ed19532`).
Operating posture: `/skill:godspeed`.

Environment: workstation linux 7.2.11-arch1-1 x86_64; shell `/usr/bin/bash`; Python 3 (lane counters), gawk,
coreutils, curl available. No tool installed or upgraded this seat (nothing needed; no pacman transaction run).

Disk guard, before the (light) run:

```
$ /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
root                             use%     free
/tmp                               3%   125.1G
/var/tmp                          37%   576.7G
/fast/scratch/hyaku               28%   584.2G
rc=0
```

## Status

- Draft row: **DONE**, 11 cells, no pipe inside any cell, verified with the frozen counter's own cell splitter.
- W04-not-E04: **PROVEN** by running the census script on a controlled two-scope fixture (same URL, different
  scope → `W04` + `ok`, rc 0; same URL, identical scope → `E04`, rc 1) plus the live lane census, whose existing
  `S476` row already reports this exact URL as `W04`.
- Gate line (URL, date, live sha256, located ≤25-word quote with line numbers): **MET** (below).
- Not done by design: the row was **not** inserted into `corpus/SOURCES.md` (L1 integrates), and the entry
  `corpus/knowledge/oom-memcg-stat-r50.md` was **not** created (wave-1 entry seats). See Finding L1 for the
  ordering consequence.

## Gate line

| item | value |
|---|---|
| URL | `https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c` |
| opened / fetched | 2026-10-26 |
| live fetch | `curl -sS -o live-oom_kill.c --max-time 60 -w 'http=%{http_code} size=%{size_download}\n' <URL>` → `http=200 size=34311`, rc 0 |
| live sha256 | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` |
| frozen sha256 (`corpus/evidence/sources-r50/oom_kill.c.v7.2`, `evidence/freeze-sha256.txt`) | `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` |
| verdict | **byte-identical** (live bytes = committed copy = frozen pin), 1257 lines / 34311 bytes |

Located quote (whitespace-collapsed copy, ≤25 words, single occurrence):

```
dump_stack(); if (is_memcg_oom(oc)) mem_cgroup_print_oom_meminfo(oc->memcg); else {
```

6 words, `corpus/evidence/sources-r50/oom_kill.c.v7.2:464-466` (line 464 `dump_stack();`, 465
`if (is_memcg_oom(oc))`, 466 `mem_cgroup_print_oom_meminfo(oc->memcg);`). Located: `q in normalise_text(copy)`
→ `True`, occurrence count `1`.

Second located quote (the victim line and its units):

```
Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, shmem-rss:%lukB, UID:%u pgtables:%lukB oom_score_adj:%d
```

11 words, `oom_kill.c.v7.2:945`; argument list at `:946-951` (`K(mm->total_vm)`, `K(get_mm_counter_sum(mm,
MM_ANONPAGES))`, `MM_FILEPAGES`, `MM_SHMEMPAGES`, `from_kuid(...)`, `mm_pgtables_bytes(mm) >> 10`). Located: `True`,
occurrence count `1`.

Both quotes were tested against `re.sub(r"\s+", " ", copy)` — the counter's `normalise_text` for a plain-text copy
(`count-c2.py:78-81`, `normalise_text` at `:78` region).

## Draft row (verbatim, one line, 11 cells)

```
| S491 | Linux mm/oom_kill.c at tag v7.2 — https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c | code | A | which OOM report block a memcg kill versus a global kill prints in dump_header, and the per-type RSS fields with their units on the victim line, at tag v7.2; not the memcg stats formatter itself (S490) and not any other tag or kernel | mm/oom_kill.c:456 dump_header, branch :465-471, victim pr_err :945-951, call sites :1031 and :1075; tag v7.2; copy corpus/evidence/sources-r50/oom_kill.c.v7.2 sha256 452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e; live fetch byte-identical 2026-10-26 | A memcg OOM prints the memory cgroup stats block where a global OOM prints __show_mem, and the Killed process line reports total-vm, anon-rss, file-rss and shmem-rss in kB plus UID, pgtables and oom_score_adj. | mined | 2026-10-26 | on-release | corpus/knowledge/oom-memcg-stat-r50.md |
```

Cell audit (0-based, as `count-c2.split_cells` returns them — `count-c2.py:53-59`):

| # | column | value (abridged) | check |
|---|---|---|---|
| 0 | id | `S491` | `S[0-9]{3,}`; max existing id in `corpus/SOURCES.md` is **S488** (261 rows), so S491 is free and S489/S490 stay reserved for the other two frozen sources |
| 1 | source | `Linux mm/oom_kill.c at tag v7.2 — <URL>` | contains the frozen URL **and only that one** of `count-c2.COPIES` (matched set = `['.../mm/oom_kill.c']`) |
| 2 | kind | `code` | in census enum `spec\|docs\|paper\|code\|tool\|dataset\|talk\|book\|community\|own-work` |
| 3 | tier | `A` | not `community`, so E10 cannot fire |
| 4 | scope | dump_header branch (memcg block vs `__show_mem`) + per-type RSS fields and units, minus S490's formatter and other tags | differs from S003's scope and from S476's scope → W04 class |
| 5 | anchor | `:456`, `:465-471`, `:945-951`, `:1031`, `:1075`, tag, copy sha256, live-fetch date | lines verified by direct line print (below) |
| 6 | teaches | one sentence: memcg block vs `__show_mem`; victim line kB fields | no `\|` |
| 7 | status | `mined` | also satisfies `count-c2`'s `srow[7] == "mined"` |
| 8 | opened | `2026-10-26` | equals `count-c2.OPENED`; not in the future for `--today 2026-10-26` |
| 9 | recheck | `on-release` | symbolic cadence accepted by E09 |
| 10 | used-by | `corpus/knowledge/oom-memcg-stat-r50.md` | `count-c2` requires `ENTRY` present in the comma/semicolon split → `True`; non-`—` so W03 cannot fire |

Pipe count 12 ⇒ 11 cells (`count-c2.split_cells` → `n=11`). No cell contains an unescaped `|`.

Anchor line numbers were read from the committed copy, not inferred:

```
456 static void dump_header(struct oom_control *oc)
464 \tdump_stack();
465 \tif (is_memcg_oom(oc))
466 \t\tmem_cgroup_print_oom_meminfo(oc->memcg);
467 \telse {
468 \t\t__show_mem(SHOW_MEM_FILTER_NODES, oc->nodemask, gfp_zone(oc->gfp_mask));
469 \t\tif (should_dump_unreclaim_slab())
470 \t\t\tdump_unreclaimable_slab();
471 \t}
472 \tmem_cgroup_show_protected_memory(oc->memcg);
473 \tif (sysctl_oom_dump_tasks)
474 \t\tdump_tasks(oc);
...
945 \tpr_err("%s: Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, shmem-rss:%lukB, UID:%u pgtables:%lukB oom_score_adj:%d\n",
946 \t\tmessage, task_pid_nr(victim), victim->comm, K(mm->total_vm),
947 \t\tK(get_mm_counter_sum(mm, MM_ANONPAGES)),
948 \t\tK(get_mm_counter_sum(mm, MM_FILEPAGES)),
949 \t\tK(get_mm_counter_sum(mm, MM_SHMEMPAGES)),
950 \t\tfrom_kuid(&init_user_ns, task_uid(victim)),
951 \t\tmm_pgtables_bytes(mm) >> 10, victim->signal->oom_score_adj);
```

Call sites of the block: `dump_header(oc)` at `:1031` (inside `oom_kill_process`) and `:1075` (inside
`out_of_memory`). Prefix of the victim line, which is the `%s` of `:945`: `:1169-1170`
`oom_kill_process(oc, !is_memcg_oom(oc) ? "Out of memory" : "Memory cgroup out of memory");`.

## W04 vs E04 — evidence

### 1. What the census script decides on

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (read-only, not modified):

```
25 #             E03 duplicate id                   E04 duplicate URL+scope (no supersedes)
33 #             W04 same URL across scopes (warnings do not affect clean lanes)
643         scope_key=u SUBSEP scope
644         if (u!="" && (u in url_seen) && !(scope_key in url_scopes))
645           printf "%s\tW04\t%s duplicate url %s across scopes\n",lane,id,u
646         if (u!="" && (scope_key in url_scopes) && status!="rejected" &&
647             url_scope_nonrejected[scope_key] &&
648             teaches !~ /supersedes S[0-9]{3}/)
649           printf "%s\tE04\t%s duplicate url %s within scope %s\n",lane,id,u,scope
```

Reading: the duplicate key for **E04** is `url SUBSEP scope` (line 643, 646) — the same URL **within the same
scope**. The **W04** arm fires when the URL was seen before (`u in url_seen`, 644) but the `url SUBSEP scope` pair
was not (644) — i.e. the same URL **across scopes**. W04 is documented as not affecting lane status (line 33), and
the script's own arms assert exactly that:

```
361   checkline "W04-scope-sensitive-mutant" \
362     $'scope-shokunin\tW04\tS902 duplicate url dup.example/source across scopes' \
363     "$0" validate --today 2026-10-19 "$scope_dir"
364   checkx "W04-does-not-fail-validation" 0 \
...
129   check "E04-duplicate-url"    "E04" "$0" validate --today 2026-10-19 --root "$froot" a
```

S003's scope is `Linux 7.2 kernel OOM counter updates and kernel summary/victim records`; S491's scope is the
dump_header-branch / victim-fields scope above — a different string, so the pair `(url, scope)` is new and only the
URL repeats.

### 2. Fixture proof (both arms, same bytes except the scope cell)

Fixture written by Python `open(...).write()` (no `git` command, no commit; nothing written under the lane). Exact
registry bytes written: the 3-line header

```
# fixture

## Registry
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
```

plus the S003 row (scope = `Linux 7.2 kernel OOM counter updates and kernel summary/victim records`, status
`mined`, opened `2026-10-19`, used-by `corpus/knowledge/oom-kill-counter-kernel-only-r12.md`) plus the S491 draft row
of this report. Both used-by files were created empty inside the fixture so E11 stays silent.

Command (identical for both fixtures except the directory):

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file /fast/scratch/hyaku/mori-r50/Mo50ScribeRowOomKill/fix2-across/corpus/SOURCES.md --today 2026-10-26
```

Fixture A — S491 scope **differs** from S003's:

```
file	W04	S491 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
file	ok	/fast/scratch/hyaku/mori-r50/Mo50ScribeRowOomKill/fix2-across/corpus/SOURCES.md
rc=0
```

Fixture B — S491 scope **replaced by S003's exact scope string** (only difference):

```
file	E04	S491 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c within scope Linux 7.2 kernel OOM counter updates and kernel summary/victim records
rc=1
```

This is the discriminator: the draft row is W04 **because its scope differs**; copy S003's scope into it and the same
bytes become E04. The lane must not do that.

### 3. Live lane census (read-only) and precedent

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
rc=0            22 output lines: 21 × W04, 0 × E-line, 1 × `mori	ok	.../mori-shokunin/corpus/SOURCES.md`
mori	W04	S476 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
```

The same URL is already in the registry twice with different scopes — S003 (line 9, opened 2026-10-19, scope
`Linux 7.2 kernel OOM counter updates and kernel summary/victim records`) and S476 (line 255, a three-URL row whose
first URL is this one, scope `which v7.2 function emits each oom trace event and the order the OOM reaper path emits
them; not the event field schemas (S475)`). S476's duplicate already prints as W04 and the lane's census is `ok` at
rc 0, so admitting S491 as a third, differently-scoped row follows the same precedent. The lane's own start-of-round
receipt agrees: `.ufo/waves/round-50/evidence/census-start.txt` holds 21 W04 lines and `census-rc=0`; landing S491
makes it 22 W04 lines and still rc 0 (`E11` caveat in Finding L1).

Why the census groups them at all: `url_of()` (`sources-census.sh:600`) strips the scheme and the trailing slash and
lowercases only the host, so S003's and S491's identical hrefs normalise to `raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c`.

## Candidate located quotes for the entry seats (suggestions, not claims)

Each was checked as one whitespace-collapsed single-occurrence span inside `oom_kill.c.v7.2`. The entry's own rules
(≥6 words, ≤25 words, ≥3 words of 3+ letters absent from the quote, unique per table) still apply to whatever claim
each is paired with; the beyond-quote count below is only an illustration for one wording I tried.

| lines | words | located | quote |
|---|---|---|---|
| 464-466 | 6 | yes (×1) | `dump_stack(); if (is_memcg_oom(oc)) mem_cgroup_print_oom_meminfo(oc->memcg); else {` |
| 468-470 | 6 | yes (×1) | `__show_mem(SHOW_MEM_FILTER_NODES, oc->nodemask, gfp_zone(oc->gfp_mask)); if (should_dump_unreclaim_slab()) dump_unreclaimable_slab();` |
| 945 | 11 | yes (×1) | `Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, shmem-rss:%lukB, UID:%u pgtables:%lukB oom_score_adj:%d` |
| 947-949 | 6 | yes (×1) | `K(get_mm_counter_sum(mm, MM_ANONPAGES)), K(get_mm_counter_sum(mm, MM_FILEPAGES)), K(get_mm_counter_sum(mm, MM_SHMEMPAGES)),` |
| 1169-1170 | 12 | yes (×1) | `oom_kill_process(oc, !is_memcg_oom(oc) ? "Out of memory" : "Memory cgroup out of memory");` |

Example beyond-quote count: claim `A memcg OOM prefixes the victim line with Memory cgroup out of memory while a
global OOM says Out of memory` against the 1169-1170 quote → `words_beyond(...) = 10` (`count-c2.py:65-67`), above
the floor of 3.

Rejected as too short for a C2 quote (fewer than 6 words), though accurate: `mem_cgroup_show_protected_memory(oc->memcg);
if (sysctl_oom_dump_tasks) dump_tasks(oc);` (4 words, lines 472-474).

## Touched surfaces

- Written: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/w1/Mo50ScribeRowOomKill.md` (this file).
- Read only: the frozen contract, `corpus/SOURCES.md` (rows S003 at line 9, S476 at line 255, max id S488),
  `corpus/evidence/sources-r50/oom_kill.c.v7.2`, `.ufo/waves/round-50/{count-c2.py,evidence/freeze-sha256.txt,evidence/census-start.txt}`,
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`.
- Not modified: `corpus/SOURCES.md`, the entry, `SKILL.md`, `SHONEN.md`, `SCORECARD.md`, `LOG.md`, `tools/`, any frozen
  round-50 file, any other lane. No git or jj mutating command, no `git add/commit/stash/checkout/reset/pull/push`, no
  fixture repo created, no host kernel log message text read, no cgroup or systemd change, no OOM triggered.

## Out of scope (not attempted)

- Inserting S491 into the registry and creating the entry — L1 / entry seats.
- S489 and S490 beyond citing them as the two sibling sources in the scope cell (claims about the HTML page and
  memcontrol.c are other seats' work).
- Whether the memcg block's own key semantics are correctly described — that is S490's scope; this row claims only
  which block prints and which fields the victim line carries.
- Any statement about kernels other than v7.2, cgroup v1, or this host's past kills.

## Findings

- **MED** — `corpus/SOURCES.md` (row to be inserted as S491): the row's `used-by` is
  `corpus/knowledge/oom-memcg-stat-r50.md`. If the row lands before the entry file exists, `sources-census.sh`
  `usedby_findings()` reports `E11 … missing used-by corpus/knowledge/oom-memcg-stat-r50.md` and `validate` exits 1.
  Verified: with the same row in a fixture lacking that file, the run printed
  `file	E11	S003 missing used-by corpus/knowledge/oom-kill-counter-kernel-only-r12.md` (rc 1) until the file was
  created. Integrate the entry and the row in one commit.
- **MED** — same row, scope cell: E04 turns on scope equality, not on "this URL is already registered". Fixture B
  above shows the identical row bytes becoming `E04 … within scope Linux 7.2 kernel OOM counter updates and kernel
  summary/victim records` (rc 1) once S003's scope string is reused. The drafted scope must be landed verbatim; a
  well-meaning "harmonise the scopes" edit converts a warning into a census error.
- **LOW** — drafted scope cell names `(S490)` as the excluded formatter source. That cross-reference is only correct
  if the memcontrol.c row lands as S490; if the renumbering shifts, the cell's parenthetical goes stale and must be
  updated in the same commit.
- **LOW** — `evidence/census-start.txt` records 21 W04 warnings at round start; the S491 row adds a 22nd
  (`duplicate url …/oom_kill.c across scopes`) without changing rc. Any round-end census diff that expects the count
  to stay 21 is misreading the receipt, not a regression.
- **LOW** — `count-c2.py` matches a row's URL by substring over the *whole* source cell and stops at the first match
  in `COPIES` iteration order (`count-c2.py:172-177`). Because S491's source cell carries only the oom_kill.c URL, the
  attribution is unambiguous; a later multi-URL row (like S476) would attach every quote to one URL only.
- **LOW** — the anchor cell's `:1031` and `:1075` are the two `dump_header(oc)` call sites; they are not
  independently quoted in this report, only read from the copy. A wave-2 re-opener should confirm both line numbers
  before the row is treated as re-checked.
