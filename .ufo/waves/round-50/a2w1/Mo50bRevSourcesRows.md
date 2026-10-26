# Mo50bRevSourcesRows — SOURCES.md rows S489–S491 at 487941b

Seat: Mo50bRevSourcesRows (mori round 50, attempt 2, wave a2w1). Lane repo: mori-shokunin.
Landed data reviewed at `487941b9395e89678af0053cc443cdb49cdee6e3`. Host: MACHINE_ID.

## Method

- All cited bytes were taken from the landing commit via `git show 487941b…:<path>` into scratch
  (`/fast/scratch/hyaku/mori-r50/Mo50bRevSourcesRows/`, TMPDIR under it, removed after the report was
  written). `git diff --stat 487941b… -- corpus/SOURCES.md corpus/knowledge/oom-memcg-stat-r50.md
  corpus/evidence/sources-r50/` was empty, so working-tree reads of those paths equal the landing.
- Line numbers below for `corpus/SOURCES.md` are the line numbers of the file at `487941b` (S002=8,
  S003=9, S004=10, S476=255, S489=268, S490=269, S491=270).
- Ran, read-only: `sources-census.sh validate --today 2026-10-26 <lane>` (writes stdout only), the
  frozen CORPUS.md schema semantics (via a written awk file, not shell-inlined), `sha256sum` of the
  three committed copies, and targeted `grep -n` over the committed copies. No tool installs were
  needed (tooling-authorization record: none). No kernel-log MESSAGE text was read; no config was
  touched; no git/jj mutation.
- One honest correction to my own trail: a first hand-inlined awk attempt produced nonsense counts
  (65/6/1) from shell-escaping artifacts; it was replaced by the written-file run reported below and
  those numbers should be discarded wherever seen.

## Verdict

S489, S490 and S491 all conform to the 11-column SOURCES.md schema; every anchor line range covers the
functions/sections its row names in the committed copies; every teaches cell is grounded in its anchor;
status/opened/recheck/used-by are exact. S491 is a W04 warning, not an E04 error, per the census logic —
shown below from the script text and from an observed run. **No HIGH or MED findings.** Two LOW notes.

## Row-by-row verification

### S489 — `Control Group v2 (v7.2)` — docs, tier A (line 268)

- Schema: 11 columns (NF=13); kind `docs`, tier `A` (official kernel docs — A is correct; not
  community). Whole-file frozen-schema run: `TOTAL rows=264 bad_nf=0 enum_violations=0
  duplicate_ids=0`; census `validate` printed `mori-shokunin ok …` and exited 0.
- Scope: `cgroup v2 memory interface at kernel 7.2: memory.current, memory.stat keys and units,
  memory.events fields, memory.oom.group; not the kernel print formats (S490, S491) and not any host's
  values` — distinct from S002 (line 8), which is the unversioned current page scoped to memory
  events/peak and local-vs-hierarchical. Different URL (`docs.kernel.org/7.2/…` vs
  `docs.kernel.org/admin-guide/…`) → no census collision of any kind.
- Anchor `Memory Interface Files; memory.stat; memory.events; memory.oom.group; copy …; adopts staged
  S533 renumbered by document` — all four named sections exist in the committed copy
  `corpus/evidence/sources-r50/cgroup-v2.7.2.html`: `Memory Interface Files` heading at html:1193,
  `memory.stat` dt at html:1393, `memory.oom.group` dt at html:1332, `memory.events` dt at html:1346.
- Copy integrity: sha256 of the committed copy `2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34`
  equals the sha256 in the row's anchor cell.
- Teaches grounded, all three clauses, in the row's own anchor:
  - "byte-count" / units grounding: html:1194 `All memory amounts are in bytes.  If a value which is
    not aligned to PAGE_SIZE is written,` — also the entry's S489 quote.
  - "keys are looked up by name rather than position": html:1399–1400 `Don't rely on items remaining
    in a fixed position; use the keys to look up specific values!`
  - "conditional on kernel configuration": html:1554 `This counter is not present when
    CONFIG_TRANSPARENT_HUGEPAGE` (inside the memory.stat entry list), corroborated in code by the
    `#ifdef CONFIG_ZSWAP / CONFIG_SWAP / CONFIG_TRANSPARENT_HUGEPAGE / CONFIG_HUGETLB_PAGE /
    CONFIG_NUMA_BALANCING` arms of the `memory_stats[]` table at `memcontrol.c.v7.2:1546–1608`.
- status `mined`, opened `2026-10-26` (today, not future — E08 clean), recheck `on-release`
  (accepted, see census section), used-by exactly `corpus/knowledge/oom-memcg-stat-r50.md`.

### S490 — `Linux mm/memcontrol.c at tag v7.2` — code, tier A (line 269)

- Scope distinct from S004 (line 10): S004 is master commit `c03c1a14…` (2026-10-18); S490 is tag
  `v7.2`; the scope text carries the explicit carve-out `not the master-commit path labels of S004`.
  URL unique in the registry (grep over the dump: only line 269 matches `v7.2/mm/memcontrol.c`) → no
  W04, no E04 possible.
- Anchor `mm/memcontrol.c:1546-1608,1693-1748,1751,1770,1787-1830,4905-4919; tag v7.2` verified
  against `corpus/evidence/sources-r50/memcontrol.c.v7.2` (6068 lines):
  - 1546–1608 = the complete `static const struct memory_stat memory_stats[]` key table
    (1546 `static const struct memory_stat memory_stats[] = {` … closing `};` at 1608), the key-name
    source for name-not-position and the `#ifdef`-conditional keys.
  - 1693–1748 = `memcg_stat_format()` complete: 1693 `static void memcg_stat_format(struct mem_cgroup
    *memcg, struct seq_buf *s)`, body through its closing brace at 1748.
  - 1751 = `static void memory_stat_format(struct mem_cgroup *memcg, struct seq_buf *s)` — the
    dispatcher (`cgroup_subsys_on_dfl` → `memcg_stat_format`, else `memcg1_stat_format`), pin-pointed
    per the registry's existing convention (cf. S476's `:567,578… in oom_reap_task_mm`).
  - 1770 = `void mem_cgroup_print_oom_context(...)` (the `oom_memcg=` / `global_oom` / `task_memcg=`
    labels at 1774–1781).
  - 1787–1830 = `mem_cgroup_print_oom_meminfo()` (def 1791): MEMCG_MAX failcnt override at
    1800–1802, `pr_info("memory: usage %llukB, limit %llukB, failcnt %lu\n",` at 1805, swap line,
    `pr_info("Memory cgroup stats for ");` at 1824, `memory_stat_format(memcg, &s);` at 1828,
    `seq_buf_do_printk(&s, KERN_INFO);` and the closing brace ending the function.
  - 4905–4919 = `memory_stat_show()` (4905 `int memory_stat_show(...)`, `memory_stat_format(memcg,
    &s);` at 4914, `seq_puts(m, buf);`).
- Teaches verified: "The OOM report and the memory.stat file share memory_stat_format" — the same
  `memory_stat_format` call appears in the OOM path (1828) and in the memory.stat file op (4914);
  "on cgroup v2 the printed failcnt is the MEMCG_MAX event counter" — 1800–1802: `if
  (cgroup_subsys_on_dfl(memory_cgrp_subsys)) memory_failcnt =
  atomic_long_read(&memcg->memory_events[MEMCG_MAX]); else memory_failcnt = memcg->memory.failcnt;`.
- Copy integrity: sha256 `8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e` matches
  the anchor cell. status `mined`, opened 2026-10-26, recheck `on-release`, used-by exact.

### S491 — `Linux mm/oom_kill.c at tag v7.2` — code, tier A (line 270)

- Scope distinct from S003 (line 9) and S476 (line 255) despite the same first URL: S003's scope is
  `Linux 7.2 kernel OOM counter updates and kernel summary/victim records`; S476's is `which v7.2
  function emits each oom trace event and the order the OOM reaper path emits them`; S491's is `the
  OOM victim record and the memcg-versus-global report split at tag v7.2 (dump_header, __show_mem,
  the Killed process line); same URL as S003 and S476 with a different scope`. Three distinct scope
  strings over one normalized URL — exactly the W04 shape.
- Anchor `mm/oom_kill.c:400-410,424-431,444-454,456-469,912-951,1169-1170; tag v7.2` verified against
  `corpus/evidence/sources-r50/oom_kill.c.v7.2` (1257 lines):
  - 400–410 = the complete per-task `pr_info("[%7d] %5d %5d %8lu …")` row of the Tasks-state table
    (400–405) through `task_unlock(task);` / `return 0;` / `}` — the pages-unit table the entry
    contrasts with the kB victim line.
  - 424–431 = `dump_tasks()` header block: 422 `static void dump_tasks(struct oom_control *oc)`,
    424–425 `pr_info("Tasks state (memory values in pages):\n");` and the column-header line, the
    `is_memcg_oom` branch.
  - 444–454 = `dump_oom_victim()` complete: 447 `pr_info("oom-kill:constraint=%s,nodemask=%*pbl", …)`
    plus the `task=%s,pid=%d,uid=%d` continuation.
  - 456–469 = `dump_header()` through the report split: 456 `static void dump_header(struct
    oom_control *oc)`, 466 `mem_cgroup_print_oom_meminfo(oc->memcg);` (memcg branch), 468
    `__show_mem(SHOW_MEM_FILTER_NODES, oc->nodemask, gfp_zone(oc->gfp_mask));` (global branch).
  - 912–951 = `__oom_kill_process()` from its definition (912) through 935 `count_vm_event(OOM_KILL);
    memcg_memory_event_mm(mm, MEMCG_OOM_KILL);` and the complete `Killed process` statement —
    945 `pr_err("%s: Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB,
    shmem-rss:%lukB, UID:%u pgtables:%lukB oom_score_adj:%d\n",` with its argument lines ending
    exactly at 951 (`mm_pgtables_bytes(mm) >> 10, victim->signal->oom_score_adj);`). The range end is
    the statement's last line — an exact cut, not a truncation of the named claim.
  - 1169–1170 = `oom_kill_process(oc, !is_memcg_oom(oc) ? "Out of memory" :
    "Memory cgroup out of memory");` — the two message prefixes.
- Teaches verified: "The Killed process line carries the victim's own counters in kB" — every field
  argument passes through `K()` (and `>> 10` for pgtables) at 946–951; "a global OOM prints __show_mem
  where a memcg OOM prints the stats block" — 466 vs 468. `__show_mem` appears as its call site inside
  `dump_header`, which is what the row's scope claims (the split), not the function's definition
  (which lives outside oom_kill.c); consistent with the anchor convention.
- Copy integrity: sha256 `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` matches
  the anchor cell. status `mined`, opened 2026-10-26, recheck `on-release`, used-by exact.

## used-by exactness

- Each of S489/S490/S491 carries exactly one used-by path, `corpus/knowledge/oom-memcg-stat-r50.md`;
  the file exists at R (E11 clean — the validate run's only findings were W04 lines).
- The entry's three `source:` lines at R cite exactly S489, S490, S491 (1:1 with the rows' used-by).
  No other row was repointed: S002/S003/S004/S476 keep their prior used-by lists and do not name the
  new entry, and the new entry does not cite them — no dangling reverse pointers in either direction.

## Census: S491 is W04, not E04 — deciding lines

From `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`:

- Header contract (lines 25, 28, 33, 36):
  `E04 duplicate URL+scope (no supersedes)`; `E09 invalid recheck (ISO date, NNd, or symbolic
  cadence)`; `W04 same URL across scopes (warnings do not affect clean lanes)`; `cadence<SPC>id<SPC>
  recheck=<x> — symbolic cadences (e.g. on-release) are reported, never judged overdue.`
- The decisive gawk in `row_pass()` (lines 643–649):

```gawk
        scope_key=u SUBSEP scope
        if (u!="" && (u in url_seen) && !(scope_key in url_scopes))
          printf "%s\tW04\t%s duplicate url %s across scopes\n",lane,id,u
        if (u!="" && (scope_key in url_scopes) && status!="rejected" &&
            url_scope_nonrejected[scope_key] &&
            teaches !~ /supersedes S[0-9]{3}/)
          printf "%s\tE04\t%s duplicate url %s within scope %s\n",lane,id,u,scope
```

  `u` is the first `https?://` match of the source cell, normalized (fragment stripped, trailing `/`
  stripped, host+path lowercased). For S491: S003 (line 9) registered
  `raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c` in `url_seen`; S476 (line 255) has
  the same first URL but a different scope, so its `scope_key` is new and it already fired W04;
  S491's scope differs from both, so `(scope_key in url_scopes)` is false — the E04 branch cannot
  fire — while `(u in url_seen)` is true, so W04 fires.
- Selftest corroboration (lines 361–364): `checkline "W04-scope-sensitive-mutant"
  $'scope-shokunin\tW04\tS902 duplicate url dup.example/source across scopes' …` and
  `checkx "W04-does-not-fail-validation" 0 …` — W04 is a warning that leaves the lane clean.
- Observed run (`sources-census.sh validate --today 2026-10-26 <lane>`, rc=0, 23 output lines):

```text
mori-shokunin	W04	S476 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori-shokunin	W04	S491 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
mori-shokunin	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

  Warning histogram: `22 W04`, zero E-codes, zero W01/W02/W03. The round-start receipt
  `.ufo/waves/round-50/evidence/census-start.txt` holds exactly 21 W04 lines and no oom_kill-URL line
  for S491 — the delta is exactly S491's one warning, as the contract's "same URL as S003 and S476
  with a different scope — a W04 warning, not an error" predicts.

## Census: `on-release` accepted

- E09 branch (line 665): a recheck fails only if it is neither an ISO date, nor `NNd`, nor symbolic;
  `function symbolic(s) { return s ~ /^[A-Za-z][A-Za-z0-9 _-]*$/ }` (line 582) — `on-release`
  matches. `overdue` mode reports symbolic cadences as `cadence …` lines and sets
  `due=INVALID_EPOCH`, i.e. never overdue (line 36 and the overdue branch); selftest line 148:
  `check "symbolic-on-release-reported" "S015 recheck=on-release" …`.
- Observed: the validate run emitted no E09 anywhere, and all three new rows carry `on-release`.
  (I did not run `overdue` mode; the acceptance shown is from validate semantics plus the script's
  own selftest expectation.)

## Checks with no defect found (recorded so wave 2 does not re-derive them)

- kind/tier against the enum and the tier rules: docs/A and code/A are primary-or-authoritative for
  their scopes; no community-at-A anywhere (E10 clean, whole file).
- Anchor range boundaries are exact, not approximate: S490's 1693–1748 ends at `memcg_stat_format`'s
  closing brace; 1787–1830 ends at `mem_cgroup_print_oom_meminfo`'s closing brace; S491's 912–951
  ends at the `Killed process` statement's final argument line; 1169–1170 is the full ternary.
- Entry quotes I independently located while verifying anchors (sample spanning all three copies):
  `pr_info("memory: usage %llukB…` (1805), the MEMCG_MAX block (1800–1802), `memory_stat_format(memcg,
  &s);` at 1828 and 4914, `oom_memcg=/global_oom/task_memcg` labels (1774–1781), `Tasks state
  (memory values in pages):` (424), `oom-kill:constraint=` (447), `count_vm_event(OOM_KILL)` (935),
  the `Killed process` line (945–951), the message ternary (1169–1170), `__ratelimit(&oom_rs)` (1030),
  html `All memory amounts are in bytes…` (1194), the fixed-position sentence (1399–1400),
  `memory.oom.group` (1332), `memory.events` (1346). Location of every table quote remains count-c2's
  met predicate (`located=22`); this row-level check found no anchor that contradicts them.
- The S489 anchor's trailing `adopts staged S533 renumbered by document` clause and the S489-vs-S002
  overlap are recorded as LOW findings below; everything else in those cells is correct.

## Limits / UNVERIFIED

- Live-URL identity was not re-fetched by me (no `curl` this seat): the committed copies match the
  anchor sha256 values, and the entry's `recheck:` line records a same-day (2026-10-26) successful
  live fetch, but I cannot independently confirm the live pages still equal the copies. UNVERIFIED.
- `sources-census.sh` validate ran against the working tree, whose bytes for the reviewed paths I
  verified equal the landing (empty `git diff --stat`); it was not run against a fresh archive of the
  commit. Given the byte-identity check, this does not weaken the result.
- The census tool's own selftest was not rerun here; its pinned tallies are C1's receipts, not this
  seat's subject.
- I reviewed the SOURCES rows and their anchors, not the entry table's 22 claim/quote pairs as such;
  that re-open is another seat's assignment.

## Findings

1. LOW — `corpus/SOURCES.md:268` (S489, anchor cell, at 487941b): the cell appends assimilation
   provenance (`adopts staged S533 renumbered by document`) to the anchor data. The frozen CORPUS.md
   rule 2 keeps correction/provenance logs in the round lesson, and no sibling r47–r49 row carries a
   staged-id note. Schema- and census-clean (no pipe, no enum issue), so no claim is affected.
   Optional fix: L1 may drop the clause from the row and keep the S533→S489 renumber record in the
   round-50 lesson; not required for C2.
2. LOW — `corpus/SOURCES.md:268` vs `:8` (S489 vs S002): the scopes overlap on the `memory.events`
   facet (both pages carry, at their respective revisions, the oom_kill-field sentence the entry
   quotes). They remain distinct rows — different pinned revision (7.2 vs current), different facet
   set, different URL, and S489's explicit carve-outs — consistent with the lane's version-split
   convention (S003/S491). No change required; wave 2 should treat oom_kill-field wording as
   attested by both revisions, not as a discrepancy.

No HIGH or MED findings. Anchors, teaches, scope distinctness, schema, on-release acceptance, used-by
exactness and the W04-not-E04 classification all verified against the landing bytes.
