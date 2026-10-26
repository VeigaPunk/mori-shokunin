# Mo50bScribeLessonGate — draft `## Gate` of `corpus/lessons/round-50.md` (round 50, wave a2w1)

Seat: scribe, leaf. Assignment: draft the `## Gate` section of `corpus/lessons/round-50.md` in the house
shape of `corpus/lessons/round-49.md`, with the content named in the ticket (rows S489–S491 with quote cells
from the quote scribe; assimilation theme FR1 / memcg OOM block composition; collision check, guard proof,
scratch mirror validation, quarantine slice, considerthese 2026-10-26 suggestion 3; a `### Spot-check` offering
one admit and one reject; the attempt-1/attempt-2 reuse list). Nothing outside this report was written; no
product file, no lesson file, no `corpus/`, `tools/`, `SKILL.md`, `SHONEN.md`, `SCORECARD.md`, `LOG.md`, and no
file under `.ufo/waves/round-50` except this one. No subagent, no pacman, no host-state change, no kernel-log
MESSAGE read. `shokuknow` was read only. The frozen counters, predicates, controls and kill rules were used as
committed and are not proposed for change.

| item | value |
|---|---|
| lane | `/home/vgpnk/Projects/shokunin/mori-shokunin`, HEAD `4548a34dc8b4072abaa4335c1f54a9efcfcc314a` |
| landed data revision (R) | `487941b9395e89678af0053cc443cdb49cdee6e3` (`git merge-base --is-ancestor 487941b9 HEAD` → 0) |
| freeze | `950e99be6757a52b00e9eb70ae1a1a7bbe2ea379`; entering tip `7197160b…`; attempt-1 salvage `9b8562a3…` |
| scratch | `/fast/scratch/hyaku/mori-r50/Mo50bScribeLessonGate/` (`TMPDIR` set there for every call; removed at the end) |
| disk guard | `scripts/hyaku/disk-guard.sh status` → rc 0; `/fast/scratch/hyaku` 24% used, 618.3G free |
| tooling | none installed or upgraded this seat |

## Behavior

Delivered: the fenced `## Gate` draft in §3 — three new SOURCES rows with located ≤25-word quotes and their
line locations, the assimilation theme with candidates / collision check / guard proof / mirror validation /
renumber-by-document / admit / reject-with-flip / quarantine slice / considerthese / census-at-R, a
`### Spot-check` with one admit and one reject, and a subsection recording which attempt-1 material was reused
after re-verification and which was discarded.

What this seat did not do: it did not touch the entry, its rows, the copies, `SCORECARD.md` or `SHONEN.md`
(the L1 integrates the draft); it did not re-score C1 or C2 (the ticket line and the wave's executor reports
carry those runs); it did not read the round-48/49 closure verdicts as its own. Every claim in the draft below
rests on a command in §2, on a committed bytes match, or is marked UNVERIFIED.

## Verification runs (command → observed output, exit code)

All commands read-only. `S=/fast/scratch/hyaku/mori-r50/Mo50bScribeLessonGate`.

**Freeze integrity** — `sha256sum -c .ufo/waves/round-50/evidence/freeze-sha256.txt` → 34 lines, every one
`OK`, no `FAILED` line, rc 0 (`.ufo/waves/round-50/evidence/sweep-memcg-stat.txt: OK` is the last line).
The three copies: `sha256sum corpus/evidence/sources-r50/*` →
`2d716cb798eacf8fbcf431b52697fbb8c5ed8ea9f58ac15b2b55351247c0bf34 cgroup-v2.7.2.html` (168438 B),
`8a28e0bc010e0575fbf9d1739643686e271bcf5a76c0284081df537a4041fd5e memcontrol.c.v7.2` (160768 B, 6068 lines),
`452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e oom_kill.c.v7.2` (34311 B, 1257 lines),
rc 0 — each equals the sha256 in its row's anchor cell and in `assimilation/a2/live-sha-L1.txt`
(2026-10-26T09:26:36/37-03:00, three lines, `-` diff column).

**Gate quotes locate** — python3, whitespace-collapsed substring on the raw copy plus the HTML normalisation
(comment/script/style blocks dropped, tags stripped, entities decoded):

```
S489 words= 17 raw_hits= 2 norm_hits= 2 file= corpus/evidence/sources-r50/cgroup-v2.7.2.html
S490 words=  9 raw_hits= 1 norm_hits= 1 file= corpus/evidence/sources-r50/memcontrol.c.v7.2
S491 words= 12 raw_hits= 1 norm_hits= 1 file= corpus/evidence/sources-r50/oom_kill.c.v7.2
   raw line hits: S491 [945]   (S489/S490 spans break across raw lines: html 1398-1399, c 1800-1803)
rc=0
```

`html 1397: <p>All memory amounts are in bytes.</p>` / `1398: <p>The entries are ordered to be human readable,
and new entries` / `1399: can show up in the middle. Don’t rely on items remaining in a` — so the S489 sentence
sits in §Memory Interface Files, `memory.stat`, and the same sentence recurs at 1604-1605 under
`memory.numa_stat` (the quote seat's caveat).

**Row structure** — rows at `corpus/SOURCES.md:268-270` after S488 at `:267`; 11 cells each; `status=mined`,
`opened=2026-10-26`, `used-by=corpus/knowledge/oom-memcg-stat-r50.md` for all three; frozen URL present in each
source cell. Claim rows in the entry by source: `{'S489': 7, 'S490': 8, 'S491': 7} total= 22` (all three
sources drawn on). S003 at `:9` and S476 at `:255` carry the `oom_kill.c` URL; S004 at `:10` is
`memcontrol.c` at master commit `c03c1a14…`.

**Anchor lines read in the copies** — `mc 1546: static const struct memory_stat memory_stats[] = {`;
`mc 1608: #endif`, `mc 1609: };`; `mc 1693: static void memcg_stat_format(...)`; `mc 1748: }`, `1749: }`;
`mc 1751: static void memory_stat_format(...)`; `mc 1757: if (seq_buf_has_overflowed(s))`; `mc 1770: void
mem_cgroup_print_oom_context(...)`; `mc 1791: void mem_cgroup_print_oom_meminfo(...)`; `mc 1800/1803` the
failcnt branch; `mc 1805` the usage `pr_info`; `mc 1824: pr_info("Memory cgroup stats for ")`; `mc 1830: }`;
`mc 4905: int memory_stat_show(...)`; `mc 4914: memory_stat_format(memcg, &s);`; `mc 4918: }`, `4919:` blank.
`ok 400/424` the Tasks state `pr_info` lines; `ok 444: static void dump_oom_victim(...)`; `ok 456: static void
dump_header(...)`; `ok 465: if (is_memcg_oom(oc))`; `ok 912: static void __oom_kill_process(...)`;
`ok 945` the victim `pr_err`; `ok 951` last argument; `ok 1169-1170` the two message strings.

**Collision check** — `wc -l .ufo/waves/round-50/assimilation/{reg-ids,staged-ids,collisions}` → `261 136 18`;
`comm -12 <(sort reg-ids) <(sort staged-ids)` → `S471 … S488` (18 ids, rc 0);
`grep -cx S533 reg-ids` → `0`, `S534` → `0`, `S539` → `0`;
`git show 950e99be:corpus/SOURCES.md | grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' | grep -oE 'S[0-9]{3,}' | sort`
→ 261 ids, `diff` against `reg-ids` empty, rc 0 (so the committed id list re-derives from the frozen registry);
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` → `264` (261 + S489–S491);
`grep -cE '^ {0,3}\|[[:space:]]*S(533|534|539)[[:space:]]*\|' corpus/SOURCES.md` → `0`;
the staged rows behind the four latest collisions are other documents:
`S485 阿里云 MaxCompute 作业洞察`, `S486 … Logview`, `S487 阿里云 文件存储CPFS 配额管理`,
`S488 阿里云 可观测监控 CloudMonitor … 告警规则`; the package's own row count
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' SOURCES.append.md` → `136`.

**Guard proof** — on `assimilation/guard-proof/registry.md` with `staged.md` as the staged set:
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` → `3` (ids `S533 S534 S900`, i.e. the 2-space, 3-space and
column-0 rows; the 4-space `| S539 |` is read as code), column-0-only `grep -cE '^\|[[:space:]]*S[0-9]{3,}'`
→ `1` (`S900`); the intersection under the 0–3 pattern is `S533 S534`, which is exactly the committed
`guard-proof/collisions`, and under the column-0-only pattern it would be empty.

**Scratch mirror validation** — committed `assimilation/a2/mirror-validate.txt`: 22 `W04` lines, one
`file ok …/corpus/SOURCES.md` line, `rc=0`, and the 22nd warning is
`file W04 S491 duplicate url …/v7.2/mm/oom_kill.c across scopes`; `diff` of its W04 id set against
`evidence/census-start.txt` (21 `W04`, `census-rc=0`) → `21a22 > W04 S491`, rc 1 (one added warning, nothing
else). Independent re-run at R on my own archive: `git archive 487941b9 | tar -x -C $S/mirror` then
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/mirror/corpus/SOURCES.md` →
22 `W04`, 1 `ok`, codes `22 W04` only, `census rc=0`, S491 W04 line present. (A corpus-only partial copy first
gave rc 1 with 26 `E11 missing used-by SKILL.md` lines — the census resolves `used-by` targets against the
lane tree, so the mirror must carry it; the committed mirror does.)

**Quarantine slice** — `grep -cE '^ {0,3}\|[[:space:]]*S244[[:space:]]*\|' corpus/SOURCES.md` → `0`;
`S268` → `0`; `sed -n 243p corpus/SOURCES.md` → `| S262 | ROMA: Enhancing Container OOM Resilience … | paper | A | …
|` (mined); `grep -nE 'S244|S262|S268' corpus/knowledge/oom-memcg-stat-r50.md` → no output, rc 1; round-48
verdicts at `corpus/lessons/round-48.md:77-84` (`S244 PRESENT`, `S262 PRESENT`, `S268 PRESENT`).

**Attempt-1 material** — `.ufo/waves/round-50/w1/dispatch`: 40 seats; `ls .ufo/waves/round-50/w1/*.md` → 5
reports (`Mo50ScoutCoverageFR1`, `Mo50ScribeEntryA`, `Mo50ScribeEntryB`, `Mo50ScribeRowMemcontrol`,
`Mo50ScribeRowOomKill`); `git ls-tree -r --name-only 9b8562a3 -- corpus/lessons/` → ends at round-49 (no
`round-50.md` anywhere in the salvage);
`git diff 9b8562a3 487941b9 -- corpus/knowledge/oom-memcg-stat-r50.md` → empty (entry bytes carried unchanged);
`git diff --stat 9b8562a3 487941b9 -- …` → `SCORECARD.md | 14 ++++----`, `SHONEN.md | 2 +-`,
`corpus/SOURCES.md | 3 +++`.

## Draft — `## Gate` (integrate into `corpus/lessons/round-50.md` as-is)

````markdown
## Gate

### New SOURCES rows (each opened this round; rule 1)

Three rows, all opened 2026-10-26, appended after S488 (`corpus/SOURCES.md:268-270`), 11 cells each, status
`mined`, recheck `on-release`, `used-by corpus/knowledge/oom-memcg-stat-r50.md`. The three documents were copied
into `corpus/evidence/sources-r50/` at the freeze `950e99be` and pinned by sha256 in
`evidence/freeze-sha256.txt` (`sha256sum -c` → 34/34 `OK`, rc 0); the live bytes re-fetched on
2026-10-26T09:26:36-03:00 matched all three (`assimilation/a2/live-sha-L1.txt`), so each row is grounded in
bytes this lane holds and the page it names still serves them. Every quote below was located by this wave's
quote seat in the committed copy and re-located here (whitespace-collapsed substring; the HTML copy also after
`count-c2.py`'s `normalise()`, rc 0).

| id | URL / locator | accessed | ≤25-word located quote | decision |
|---|---|---|---|---|
| S489 | https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html — copy `cgroup-v2.7.2.html` (sha256 `2d716cb7…bf34`) | 2026-10-26 | "The entries are ordered to be human readable, and new entries can show up in the middle." (17 words) — §Memory Interface Files, `memory.stat` entry, copy lines 1398-1399; the same sentence also occurs at 1604-1605 under `memory.numa_stat`, so the entry and the lines are named `[from ScribeGateQuotes]` | admit, mined, kind docs, tier A, recheck `on-release`; scope is the page's memory interface (memory.current, memory.stat keys and units, memory.events fields, memory.oom.group) and explicitly not the kernel print formats (S490, S491) nor any host's values; adopts staged S533 renumbered by document |
| S490 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c — copy `memcontrol.c.v7.2` (sha256 `8a28e0bc…1fd5e`) | 2026-10-26 | "if (cgroup_subsys_on_dfl(memory_cgrp_subsys)) memory_failcnt = atomic_long_read(&memcg->memory_events[MEMCG_MAX]); else memory_failcnt = memcg->memory.failcnt;" (9 words) — copy lines 1800-1803, inside `mem_cgroup_print_oom_meminfo()` `[from ScribeGateQuotes]` | admit, mined, kind code, tier A, recheck `on-release`; scope is the memcg OOM report path at tag v7.2 (usage/limit/failcnt lines, the `Memory cgroup stats` block, the `memory_stat_format` formatter shared with `memory.stat`), not S004's master-commit path labels (`corpus/SOURCES.md:10`, a different revision of the same file) |
| S491 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c — copy `oom_kill.c.v7.2` (sha256 `452f1348…6b4e`) | 2026-10-26 | `pr_err("%s: Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, shmem-rss:%lukB, UID:%u pgtables:%lukB oom_score_adj:%d\n",` (12 words) — copy line 945, arguments 946-951 `[from ScribeGateQuotes]` | admit, mined, kind code, tier A, recheck `on-release`; the URL already stands at S003 (`:9`) and inside S476 (`:255`), so the row is a **W04** warning (same URL across scopes), not an error — the scope is the victim record and the memcg-versus-global report split, which neither earlier row carries |

Changed in place (rule 2), old → new: none. The anchor cells were re-read line by line: S490 names
`memory_stats[]` (1546-1608, closing brace 1609), `memcg_stat_format` (1693-1748, closing brace 1749),
`memory_stat_format` (1751, overflow check 1757), `mem_cgroup_print_oom_context` (1770),
`mem_cgroup_print_oom_meminfo` (1787-1830; failcnt branch 1800-1803, usage line 1805, `Memory cgroup stats
for` 1824) and `memory_stat_show` (4905-4919, function closes at 4918 — the range carries one blank line);
S491 names the Tasks-state table (400, 424), `dump_oom_victim` (444), `dump_header` (456; the
memcg/`__show_mem` branch 465-468), `__oom_kill_process` (912; victim line 945-951) and the two message
strings (1169-1170). Every range covers the object its scope cell names.

### Assimilation (addendum §10) — theme FR1, the memcg OOM report block's composition

Package `/home/vgpnk/Projects/shokuknow/merge/mori/` read only; no campaign tool run; nothing written there.
The package states 136 proposed rows from S471 and 80 proposed entries (`MERGE-REPORT.md:5,13`;
`MERGE-REPORT.json`: `accepted=136 entries=80 first_id=S471` — 75 entry files under
`knowledge/corpus/knowledge/` plus 5 under `amendments/corpus/knowledge/`), and the adopt checklist is not
followed for the reasons round 49 recorded: step 1 names a `SOURCES-PROPOSED.md` the package does not contain,
step 3's bulk append would import every staged id, step 4 would exceed §10's 1–3 entry cap. One theme, one
entry, three rows; one row adopted by document, two own-work rows rejected.

- **Candidates considered** (two staged entries, three rows). Both entries are in the FR1 theme and each cites
  an own-work `file:///home/vgpnk/Projects/shokuknow/lanes/mori/round{9,10}/.deepresearch/notes/…` receipt —
  r46 beside its docs row, r47 as its only source. The two notes exist (2643 and 3151 bytes), read-only, and
  neither is a lane file.

  | staged entry | rows | what it claims | verdict |
  |---|---|---|---|
  | `scope-charge-fields-r46.md` | S533 (docs), S534 (own-work) | a cgroup's charge is typed; `file` includes tmpfs and shared memory; the runner mounts fresh tmpfs on `/tmp` and `/run`, so a child can hit the cap without the victim growing; the journal block carries none of the breakdown | reject as an entry; its field rule is rewritten into the admitted entry, its host half and its tmpfs hypothesis are not adopted |
  | `scope-composition-in-the-block-r47.md` | S539 (own-work) | the block continues past the usage line with `Memory cgroup stats for <path>:` and the scope's stat fields; in its one block the composition was the victim's own anon and the r46 tmpfs hypothesis is refuted (`file 0`, `shmem 0`) | reject as an entry; the structure it reads is stated in the admitted entry from S490, its numbers and its refutation are not evidence here |

  S534 is also cited by a third staged entry, `scope-limit-per-kill-r46.md` (the limit's value, outside this
  theme); it is not a candidate and nothing here changes it.

- **Collision check** (before any append; `assimilation/{reg-ids,staged-ids,collisions}`): registry **261** ids,
  staged **136** ids → **18 collisions `S471 S472 S473 S474 S475 S476 S477 S478 S479 S480 S481 S482 S483 S484
  S485 S486 S487 S488`**, reproducible from the two committed lists (`comm -12 <(sort reg-ids) <(sort
  staged-ids)` → those 18, rc 0); the committed `reg-ids` is identical to the ids re-derived from
  `git show 950e99be:corpus/SOURCES.md` under the 0–3-space pattern (261, `diff` empty, rc 0). The four latest
  collisions are **the lane's own round-49 rows against four unrelated staged documents** — lane S485–S488 are
  the journal rows (`journald.conf(5)`, `journalctl(1)`, `systemd-journald.service(8)`, this host's
  `host-journal-reach` receipt), while staged S485–S488 are 阿里云 MaxCompute 作业洞察, MaxCompute Logview,
  CPFS 配额管理 and CloudMonitor 告警规则; none of the staged four was appended. None of the candidate rows
  collides: `grep -cx` of S533, S534 and S539 against `reg-ids` → `0` each, and the lane holds no row for any
  of the three ids (`grep -cE '^ {0,3}\| *S(533|534|539) *\|' corpus/SOURCES.md` → `0`). `SOURCES.md` at R
  holds 264 ids: the 261 of the freeze plus S489–S491.
- **0–3-space guard proof** (`assimilation/guard-proof/`; the pattern the census and the id lists share): a
  fixture registry with rows at column 0, at two spaces, three spaces and four spaces against a staged set of
  S533/S534/S539 — `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` → `3` (ids `S533 S534 S900`) and the
  column-0-only pattern → `1` (`S900`). The 0–3 pattern's intersection with the staged set is **S533 S534**,
  exactly the committed `guard-proof/collisions`, while the column-0-only pattern sees no collision at all. So
  a 2–3-space indented row cannot hide from the collision check, and a 4-space row is treated as code, not as a
  row.
- **Scratch mirror validation** (`assimilation/a2/mirror-validate.txt`): a copy of the lane's `corpus/` plus
  `SKILL.md PROVINCE.md SCORECARD.md tools/` at `9b8562a3`, with the three rows appended after S488, run
  through `scripts/sources-census.sh validate --file` → **22 `W04`**, one `file ok …/corpus/SOURCES.md` line,
  **rc 0**. The 22nd warning is S491 (the third scope for the `oom_kill.c` URL after S003 and S476); the other
  21 are the entering census's (`evidence/census-start.txt`: 21 `W04`, `census-rc=0`). An independent re-run at
  R gives the same 22 `W04`, one `ok`, rc 0.
- **Renumber by document** (the URL is the evidence, the id follows it; no staged id is kept): staged **S533**
  (`cgroup-v2` at 7.2) → lane **S489**. The lane's scope for that page is wider than staged S533's: the staged
  row held the limit semantics and the events/peak files out, while the lane row covers `memory.events` and
  `memory.oom.group`; the claims drawn on it are the stat-key and events semantics, and no limit claim is
  drawn. The two own-work rows S534 and S539 get no lane id.
- **Admit:** one rewritten entry, `corpus/knowledge/oom-memcg-stat-r50.md`, replacing both staged entries with
  one claims table grounded in S489–S491 — 22 claims, all three sources drawn on (7 S489, 8 S490, 7 S491),
  every claim a located quote (`C2=met claims=22 located=22 … sources=3` at R). What it states and what it
  must not inherit:
  - The block is three prints in one burst: the usage/limit/failcnt line and its swap sibling (both kB), the
    `Memory cgroup stats for <path>:` block, and the per-victim `Killed process` line (kB, plus pgtables and
    `oom_score_adj`), while a global OOM prints `__show_mem` instead of the block.
  - The block's body is the `memory.stat` breakdown written by one formatter (`memory_stat_format`), so the
    keys are looked up by name, the key set is compile-time conditional, and a missing key is not a zero.
  - On cgroup v2 the printed failcnt is the `MEMCG_MAX` event counter, not a per-page charge failure count.
  - Not inherited: "the sandbox's fresh tmpfs on `/tmp` and `/run` was the missing charge" (r46's hypothesis)
    — nothing this lane holds speaks about a particular kill, and the entry says in Limits that no host block
    was read; "the block carries none of the breakdown" (r46) — the kernel path shows the block *is* the
    breakdown, so the entry states the format, not one host's swept block; "the composition was the victim's
    own anonymous memory, `file 0`, `shmem 0`" and its refutation of the tmpfs hypothesis (r47) — a host
    reading from an outside note, so the field semantics are taken from S489 and the reading is not adopted.
- **Reject, with flip:**
  - staged own-work rows **S534** and **S539**: their locator is a `file://` note under
    `/home/vgpnk/Projects/shokuknow/lanes/mori/round{9,10}/.deepresearch/notes/`, outside this lane. The lane's
    rule, written into S351's rejection and kept in round 49, is that a note in another repo is a lead, not
    evidence. Flip: capture the block again read-only into `corpus/evidence/sources-r50/`, pin its sha256 in
    the row, and cite the command, the boot and the time; until then no host claim enters the entry. The lane
    has not done that this round, so the two rows are not adopted and the entry carries no host line.
  - the r46 **tmpfs hypothesis** as a claim: rejected for the same reason — the only reading that would decide
    it is outside this lane — and because the admitted entry is about what the kernel prints, not about one
    kill. The field rule it leaned on survives through S489 (`file` includes tmpfs and shared memory; `shmem`
    is the swap-backed subset), which is a sentence this lane holds.
  - the two staged entries as entries: their host halves are asserted rather than located, and r47's
    "six seconds of polling found the scope is shorter than the read cycle" is a capture this lane cannot
    re-open. Flip: state the rule from the committed page or code row, and keep host readings out until a
    lane receipt exists.
- **Quarantine slice** (`assimilation/quarantine-slice`; register class "the cited source could not be
  fetched, so no quote was checked"): S244, S262, S268 keep their round-48 verdicts and none is cited by the
  admitted entry.
  - S244 — no lane row (`grep -cE '^ {0,3}\| *S244 *\|'` → `0`); the round-48 verdict PRESENT stands.
  - S262 — a lane row (`corpus/SOURCES.md:243`, `mined`, the ROMA paper); the round-48 verdict PRESENT and the
    round-41 citation predate this slice and are unchanged. It is **not** cited by `oom-memcg-stat-r50.md`
    (`grep` → no output, rc 1) and is not a row of this round's theme.
  - S268 — no lane row (`0`); the round-48 verdict PRESENT stands, with its note recorded in
    `corpus/README.md`.
  - None of the three was appended and none was edited.
- **considerthese:** `considerthese/2026-10-26.md` suggestion 3 ("re-execute what closures only
  evidence-verified") → `[from ExecReexecR47]`, `[from ExecReexecR48]`, `[from ExecReexecR49]` (three executor
  seats, `.ufo/waves/round-50/a2w1/`): each re-runs its closure's frozen counters in a `git archive` at the
  revision its receipt names and reports the final line with its exit code, so the unit is one closure × its
  frozen counter and "agreement" is the receipt's line reproduced. This is the second carrying of the idea
  (round 49 adopted suggestion 3 of 2026-10-25 as the flagged-versus-fixed count); the results are those three
  seats', not this scribe's.
- **Census at R:** `sources-census.sh validate --file` on a `git archive` of R → 22 `W04` and one `ok`, rc 0;
  the entering census had 21 `W04` and `census-rc=0`. The round therefore adds exactly one warning — S491, the
  same URL a third time — and no error: `E04` does not fire because the scopes differ.

### Attempt-1 and attempt-2 material

The round froze once, died in a host crash, and restarted from the freeze; the table records what of the dead
attempt was reused after re-verification and what was discarded.

| material | where attempt 1 left it | re-verification | disposition |
|---|---|---|---|
| entry body, 22 claims | `corpus/knowledge/oom-memcg-stat-r50.md` in the salvage `9b8562a3` | byte-identical to R (`git diff 9b8562a3 487941b9 -- <entry>` empty); the frozen counter at R prints `claims=22 located=22 … sources=3` and the wave executor reproduced that line | reused unchanged |
| three source copies and their sha256 | committed at the freeze `950e99be`, before any seat ran | `sha256sum -c evidence/freeze-sha256.txt` → 34/34 `OK`, rc 0; live re-fetch 2026-10-26T09:26:36-03:00 identical | reused unchanged |
| row material S489/S490/S491 | drafts in `w1/Mo50ScribeEntryA`, `w1/Mo50ScribeEntryB`, `w1/Mo50ScribeRowMemcontrol`, `w1/Mo50ScribeRowOomKill` | landed rows are rewrites: scope wording shortened, anchor cells replaced by line ranges, the copy sha256 and the `adopts staged S533` note added, all three in the 11-cell shape the counter reads | reused after re-verification and rewrite; no draft is carried byte-for-byte |
| located quotes | the row scribes' Gate lines (usage `pr_info` at `:1805`; `dump_stack(); if (is_memcg_oom(oc)) …` at `:464-466`) and the entry's 22 quote cells | this wave's quote seat pinned one ≤25-word span per row and this scribe re-located all three (17/9/12 words, 2/1/1 hits); the attempt-1 spans still locate and stand as alternates | the table uses this wave's spans; attempt 1's are alternates, not discarded work |
| a `## Gate` draft | the attempt-1 wave dispatched a `Mo50ScribeLessonGate` seat (40 seats) and it wrote no report; `git ls-tree 9b8562a3 corpus/lessons/` ends at round-49, so no lesson file was ever drafted | — | nothing to reuse; this is the first Gate draft |
| per-quote executor seats | `Mo50ExecQuotesCgroup` / `Mo50ExecQuotesMemcontrol` / `Mo50ExecQuotesOomKill` were dispatched and left no report (5 of 40 reports on disk) | — | not cited |
| C1 data (admitted, not this section's) | `SCORECARD.md` / `SHONEN.md` changed at R, not in the salvage (`git diff --stat 9b8562a3 487941b9` → those two files) | the C1 half is attempt 2's work and the C1 seats' evidence | outside this draft; recorded here so the lesson does not read attempt 1 as having landed it |

### Spot-check

The round-49 Gate decisions went to the round-49 non-author closure; these round-50 decisions await the same
(`LEARNING.md`). Sample offered:

- **admit, re-open one:** S490 — open `corpus/evidence/sources-r50/memcontrol.c.v7.2` and confirm the row's
  anchor ranges name what the scope cell says: `memory_stats[]` at 1546, `memcg_stat_format` at 1693,
  `memory_stat_format` at 1751, `mem_cgroup_print_oom_meminfo` at 1791 with the usage line at 1805 and
  `Memory cgroup stats for` at 1824, `memory_stat_show` at 4905 calling the formatter at 4914; then check that
  the scope text differs from S004's (`corpus/SOURCES.md:10`, the same file at master commit `c03c1a14…`) and
  re-locate the Gate quote (9 words, lines 1800-1803) under the counter's whitespace collapse.
- **reject, re-open one:** staged `scope-composition-in-the-block-r47.md` — read its `source:` line (S539, a
  `file:///home/vgpnk/Projects/shokuknow/lanes/mori/round10/.deepresearch/notes/r10-oom-composition.txt`) and
  its decisive claim (`anon 266723328`, `file 0`, `shmem 0`, hence "the tmpfs hypothesis is refuted"), then
  look for that evidence inside this lane: `grep -c 'source: S539' corpus/knowledge/*.md` → `0`, no committed
  copy under `corpus/evidence/sources-r50/`. It is a reject on provenance — the reading may well be right; the
  lane cannot cite it — and the entry states the block's structure from S490 instead.
````

That is the draft to integrate. It is written to stand alone in the lesson; the enclosing report's §2 commands
are the evidence record for it.

## Out of scope / not measured

- C1 and C2 scoring: not re-run by this seat. The landed lines are the ticket's and the wave executors'
  (`Mo50bExecC1Rerun`, `Mo50bExecC2Rerun`); this draft quotes the C2 line only to ground the entry.
- The `[from ExecReexec*]` result: the three re-execution seats are in the a2w1 dispatch as tasks 44–46
  (`Mo50bExecReexecR47/R48/R49`, with `Mo50bRevReexecMethod` at 47 beside them), but had no report on disk and
  were not addressable when this seat finished (`write agent://Mo50bExecReexecR47|R48|R49` → `not running.
  Unknown agent`). **UNVERIFIED by this seat**; the marker stands for the L1 to fill from those reports.
- Row review (kind/tier/scope vs S002/S003/S004/S476, teaches grounding) is the wave's reviewer seats'
  (`Mo50bRevSourcesRows`, `Mo50bRevRowsCgroupA/B`, `Mo50bRevRowsOomB`); this draft only records what I read
  myself (anchor lines, cells, quote locations).
- No host OOM block, no kernel-log MESSAGE text, no live cgroup read; no pacman; no fleet-repo write.
- The package's adopt checklist steps 1/3/4 were not attempted (no writes to `shokuknow`).

## Findings

1. **LOW — `corpus/SOURCES.md:269` (S490 row, anchor cell):** the cell reads
   `mm/memcontrol.c:1546-1608,1693-1748,1751,1770,1787-1830,4905-4919`. `4905-4919` ends on a **blank line** —
   the function `memory_stat_show` closes at 4918 — so the range should read `4905-4918`. Likewise `1546-1608`
   stops at the last `#endif` before the table's closing brace at 1609, and `1693-1748` before the closing brace
   at 1749. Every range still covers the object its scope cell names, so no claim is wrong; the ends are one
   line off.
2. **LOW — `corpus/SOURCES.md:268` (S489 row, scope cell vs staged S533):** the row says it "adopts staged
   S533 renumbered by document", but its scope is wider than staged S533's: staged S533 held the limit
   semantics and the events/peak files out, while the lane row covers `memory.events` and `memory.oom.group`.
   This is a legitimate re-scope of the same page, not a contradiction; it is recorded so a reader does not
   take the staged row's exclusions for the lane row's.
3. **LOW — attempt-1 report loss:** the attempt-1 wave dispatched 40 seats and 5 reports are on disk; the Gate
   seat and the three per-quote executor seats left nothing, and the salvage carries no `corpus/lessons/round-50.md`.
   The Gate's quote cells are therefore this wave's, and attempt-1 quote work is recoverable only inside the five
   surviving reports (the entry and row scribes). Not a defect of the landing; a coverage limit of the lesson.
4. **LOW — `assimilation/a2/mirror-validate.txt` (instrument behaviour, not a lane defect):**
   `sources-census.sh validate --file` resolves `used-by` targets against the tree it is pointed at, so a
   `corpus/`-only mirror prints 26 `E11 missing used-by SKILL.md` lines and rc 1 although the registry is
   sound (my first run). The committed mirror carries `SKILL.md PROVINCE.md SCORECARD.md tools/` and prints
   rc 0; the Gate states the requirement.
5. **LOW — `corpus/SOURCES.md:268-270` (census delta):** the round adds one `W04` (S491, the `oom_kill.c` URL
   a third time after S003 and S476) and no error. Expected, disclosed in the Gate table rather than left for a
   census reader to find.
6. **INFO — `considerthese/2026-10-26.md` suggestion 3:** the `## Gate` line depends on
   `Mo50bExecReexecR47/R48/R49`; until those reports land the marker `[from ExecReexec*]` is unfilled and the
   lesson must not read it as a measurement. Named as UNVERIFIED in this report.

Scratch `/fast/scratch/hyaku/mori-r50/Mo50bScribeLessonGate/` (mirror archive, census outputs, derived id
list, `tmp/`) was removed after the last command (`rm -rf`), leaving no seat artifacts outside this report.
