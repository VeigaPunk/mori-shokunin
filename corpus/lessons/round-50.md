# Round 50 lesson

Entering tip `7197160b927f04db294c9553fb48fadcc7a3f4e3`; freeze `950e99be6757a52b00e9eb70ae1a1a7bbe2ea379` (attempt 1,
L1 MoriR50: contract `.ufo/waves/round-50/contract.md`, both counters, controls, receipts, the three source copies);
orchestrator salvage of attempt 1 `9b8562a371dc916fdc0fc686619ea1e271a3e118`; attempt-2 data
`487941b9395e89678af0053cc443cdb49cdee6e3` (L1 MoriR50a2). Claims (frozen at `950e99be`, run unchanged): C1 calibration —
the self-assessment (`SCORECARD.md` `## Axes` Last change/Evidence cells, `SHONEN.md` tally pins) agrees with the fleet
`MANIFEST.json` and the instruments (`count-c1.py`); C2 depth — the memcg OOM report block and `memory.stat` entry
`corpus/knowledge/oom-memcg-stat-r50.md`, every claim a located quote (`count-c2.py`). Wave: attempt 2 ran one v2 wave,
`a2w1` (64 seats, `.ufo/waves/round-50/a2w1/`), after the data commit, so it attacked landed bytes.

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
| S489 | https://docs.kernel.org/7.2/admin-guide/cgroup-v2.html — copy `cgroup-v2.7.2.html` (sha256 `2d716cb7…bf34`) | 2026-10-26 | "The entries are ordered to be human readable, and new entries can show up in the middle." (17 words) — §Memory Interface Files, `memory.stat` entry, copy lines 1398-1399; the same sentence also occurs at 1604-1605 under `memory.numa_stat`, so the entry and the lines are named (quote seat `a2w1/Mo50bScribeGateQuotes.md`) | admit, mined, kind docs, tier A, recheck `on-release`; scope is the page's memory interface (memory.current, memory.stat keys and units, memory.events fields, memory.oom.group) and explicitly not the kernel print formats (S490, S491) nor any host's values; adopts staged S533 renumbered by document |
| S490 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/memcontrol.c — copy `memcontrol.c.v7.2` (sha256 `8a28e0bc…1fd5e`) | 2026-10-26 | "if (cgroup_subsys_on_dfl(memory_cgrp_subsys)) memory_failcnt = atomic_long_read(&memcg->memory_events[MEMCG_MAX]); else memory_failcnt = memcg->memory.failcnt;" (9 words) — copy lines 1800-1803, inside `mem_cgroup_print_oom_meminfo()` (quote seat `a2w1/Mo50bScribeGateQuotes.md`) | admit, mined, kind code, tier A, recheck `on-release`; scope is the memcg OOM report path at tag v7.2 (usage/limit/failcnt lines, the `Memory cgroup stats` block, the `memory_stat_format` formatter shared with `memory.stat`), not S004's master-commit path labels (`corpus/SOURCES.md:10`, a different revision of the same file) |
| S491 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c — copy `oom_kill.c.v7.2` (sha256 `452f1348…6b4e`) | 2026-10-26 | `pr_err("%s: Killed process %d (%s) total-vm:%lukB, anon-rss:%lukB, file-rss:%lukB, shmem-rss:%lukB, UID:%u pgtables:%lukB oom_score_adj:%d\n",` (12 words) — copy line 945, arguments 946-951 (quote seat `a2w1/Mo50bScribeGateQuotes.md`) | admit, mined, kind code, tier A, recheck `on-release`; the URL already stands at S003 (`:9`) and inside S476 (`:255`), so the row is a **W04** warning (same URL across scopes), not an error — the scope is the victim record and the memcg-versus-global report split, which neither earlier row carries |

Changed in place (rule 2), old → new, for rows added this round only (between the data commit `487941b9` and the
landing; no earlier row is touched): S490 anchor `mm/memcontrol.c:1546-1608,1693-1748,1751,1770,1787-1830,4905-4919`
→ `mm/memcontrol.c:629,1546-1608,1628-1665,1693-1748,1751,1770-1784,1787-1830,1994-1999,4905-4919` (three claim rows'
quotes sat at 1774-1782 and 1996-1998, outside the listed ranges, and the corrected Reading rules cite 629 and
1628-1665 — `a2w1/Mo50bExecC2Rerun.md` Findings 1, `Mo50bCritStagedClaims.md` Finding 1); S490 teaches "not a per-page
charge count" → "not the page counter's own failcnt" (`Mo50bRevRowsMemcgA.md` LOW, `Mo50bCritReadingRules.md` 7);
S491 anchor `…,912-951,1169-1170` → `…,912-985,1008-1054,1146-1170` (the rate-limit guard 1030-1033 and the
mm-sharing kill loop 954-985 were outside every listed range — `Mo50bExecC2Rerun.md` Finding 2). Each range now
covers the object its scope cell names and every quote the entry draws on that row. `sources-census.sh validate`
stays rc 0 after the change.

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
  - The block's body is the `memory.stat` breakdown written by one formatter (`memory_stat_format`), aggregated over
    the cgroup and its descendants, so the keys are looked up by name, the key set is conditional (CONFIG and, for
    `hugetlb`, run time), and a missing key is not a zero.
  - On cgroup v2 the printed failcnt is the `MEMCG_MAX` event counter, not the page counter's own failcnt.
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
  evidence-verified"; opened 2026-10-26, the latest reflection; still unimplemented at the entering tip) — three
  executor seats re-ran rounds 47, 48 and 49's frozen counters, controls and registered selftests in `git archive`s at
  the revisions their receipts name (`a2w1/Mo50bExecReexecR47.md`, `Mo50bExecReexecR48.md`, `Mo50bExecReexecR49.md`;
  method review `Mo50bRevReexecMethod.md`). Round 48: every run AGREE, six byte-identical to the committed receipt,
  two "AGREE modulo `rev=`" at the scored tip (no tip receipt was committed). Round 49: every run AGREE, including
  `count-c1.py` at `64c2d5fc` → `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26` and its seven tool
  controls; no DIVERGE, no CANNOT-RUN. Round 47: every run AGREE after one rerun — one junk-variant run first printed
  `mismatches=2` because the pinned `conform.py --selftest` exited 2 (setup error) under load while sibling seats ran
  the same selftest in the same lane path, then reproduced the receipt's `mismatches=1` on rerun; the divergence is
  transient, recorded, not smoothed. Lesson: the three closures' evidence-verified verdicts re-execute; the one
  instrument that makes a re-execution non-hermetic is `.ufo/waves/round-40/conform.py` (hardcoded lane path, selftest
  scratch inside the lane), which is also the `.scratch`/`round-40/scratch` producer of routed defect 4. QUALITY 136
  records the check. The 2026-10-25 suggestion 2 named in the frozen contract was not taken: the 2026-10-26 file
  superseded it as the latest reflection, and `Mo50bSentHostPaths.md` found its baseline count (13) is not
  reproducible (32 files at the diary's own HEAD).
- **Census at R:** `sources-census.sh validate --file` on a `git archive` of R → 22 `W04` and one `ok`, rc 0;
  the entering census had 21 `W04` and `census-rc=0`. The round therefore adds exactly one warning — S491, the
  same URL a third time — and no error: `E04` does not fire because the scopes differ.

### Attempt-1 and attempt-2 material

The round froze once, died in a host crash, and restarted from the freeze; the table records what of the dead
attempt was reused after re-verification and what was discarded.

| material | where attempt 1 left it | re-verification | disposition |
|---|---|---|---|
| entry body, 22 claims | `corpus/knowledge/oom-memcg-stat-r50.md` in the salvage `9b8562a3` | byte-identical at the data commit `487941b9` (the frozen counter printed `claims=22 located=22 … sources=3`, reproduced by `a2w1/Mo50bExecC2Rerun.md`); wave a2w1 then re-opened every row against its source context and found overclaims, corrected before landing (see `## Wave a2w1 — integrated findings`) | reused after re-verification; five claim cells, the intro rule and four Reading-rules bullets rewritten; quotes unchanged |
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

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | self-assessment drift (survivor) | `SHONEN.md`'s tally pins read `(60/60)` and `(13/13)` from round 48's wave-2 commit `91fbbc2a` (2026-10-25T20:25:44) through the round-49 closure `7197160b` and attempt 1's freeze `950e99be`; run from `git archive 91fbbc2a` both tools printed exactly those tallies (`PIN_CHECK_SELFTEST pass=60 fail=0`, `UNLANDED_SELFTEST pass=13 fail=0`, rc 0 each), so the pins were true when written and went stale at the round-49 data commit `64c2d5fc` (2026-10-25T22:49:54), where the same two tools print `pass=114` and `pass=17` while SHONEN still said 60/60 and 13/13 — the round-49 closure and attempt 1's freeze carried the stale pin (`evidence/control-c1-do-nothing.txt`: `item pin python3_tools/mori-pin-check.py_--selftest expect=(60/60) got=PIN_CHECK_SELFTEST_pass=114_fail=0 state=mismatch`, the `(13/13)`/`pass=17` line likewise, `C1=unmet items=8 axes=6 pins=2 boxes=4 mismatches=6 errors=0 hidden=0 manifest=a94551c5bc8d rev=7197160b927f04db294c9553fb48fadcc7a3f4e3 failed=mismatch`, exit 1). The `## Axes` Last change cells at `7197160b` read `round 26 (improved, score held)` (coverage), `round 31` (operability), `round 31` (depth) and `round 25` (calibration) against the fleet `MANIFEST.json` at `e014499613f63f8a467821219b0296121119ca53`, whose latest admitted mori closures grading those axes improved are 47, 47, 49 and 49; the improvements each cell skipped are coverage 47 (one), operability 36, 37, 38, 39, 41, 43, 44, 47 (eight), depth 38, 39, 41, 44, 47, 48, 49 (seven) and calibration 37, 38, 39, 41, 43, 44, 46, 47, 48, 49 (ten), so two of the four cells had been wrong since the round-36 and round-37 closures. | `corpus/QUALITY.md:1028-1040` criterion 123: "A registry pin is calibrated only when an instrument re-runs it from committed bytes and reads it from its own cell. … `SKILL.md:912` pinned `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` from round 40 to round 47 while the committed tool printed `pass=22` from the round-41 freeze `d72ac167` on. Check: `python3 tools/mori-pin-check.py --rev <rev> --baseline-rev <entering>` exits 0 before a round that edits a registry row or a registered tool lands." That check runs `tools/mori-pin-check.py`, whose own docstring is "re-measure the self-test pins of SKILL.md's gate registry" (`tools/mori-pin-check.py:2`) — `grep -c 'SHONEN' tools/mori-pin-check.py` → `0` — so the criterion reads SKILL.md's registry and never SHONEN.md's tally pins; and the Axes Last change column's only reader, `tools/mori-routed-r24.py` D5, uses it solely to reject a score-carrying row that says `round 1` (`axis_stale_round_1`, `:44-51`, `:760-800`) and never compares it with the latest admitted closure. | The round froze `count-c1.py`, which re-runs every SHONEN tally pin at R (`git archive`, TMPDIR in scratch), requires the observed `PREFIX pass=P fail=F` line as a committed receipt under `.ufo/waves/round-50/evidence/selftests/`, and requires each Axes Last change cell's first `round N` to be the MANIFEST's latest admitted round grading the axis improved or harmed, with that round's closure named in the Evidence cell. **Shown able to fail**: do-nothing at the entering tip prints `C1=unmet … mismatches=6` exit 1 (`evidence/control-c1-do-nothing.txt`); all-latest `mismatches=6`, pins-updated-no-receipt `mismatches=6`, axes-only `mismatches=2`, shonen-only `mismatches=4`, pins-deleted `pins=0 … failed=mismatch,pins_floor`, box-dropped `boxes=3 … failed=boxes_floor,mismatch,pins_floor` — each exit 1 (`evidence/control-c1-*.txt`); the landed tip prints `C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0` exit 0 (`evidence/a2-c1-at-data.txt`). Named limits (contract): the Score column is not checked, and the MANIFEST is fleet-written, so the counter inherits its verdicts. |
| M2 | number-drift | The round-49 lesson counted directory entries as reports: `corpus/lessons/round-49.md:7` "`(48 of 49 reports on disk when this lesson was written)`" and `:212` "49 seats dispatched; 48 reports on disk at writing". The lesson was committed as `64c2d5fc` (2026-10-25T22:49:54), when `.ufo/waves/round-49/w1/` held 47 report files plus `swarm-registry.json` (48 entries; the 48 is the entry count, not the report count); the fleet report filed 22:54-22:57 already said "47 of 49 on disk at filing" and carried a trailing erratum (`.ufo/reports/round-49/mori.md:9,58`). The two missing seats' reports landed later: `Mo49SimpCounters.md` first at `7197160b` (2026-10-25T23:04:10), `Mo49ExecCounterTiming.md` only at the round-50 salvage `9b8562a3` (2026-10-26T09:05:31) — `git ls-files .ufo/waves/round-49/w1 | wc -l` → 50 (49 reports + registry), and `tools/mori-wave-settlement.py scan` gives `members=49 present=49`. | none — no QUALITY criterion reads a seat count written in a lesson: QUALITY 64 covers only "the per-seat report presence … counted by `tools/mori-wave-settlement.py scan` and the receipt … committed before the round reports that wave's settlement" (`corpus/QUALITY.md:227-232`), and round 49 committed no such receipt (no settlement receipt under `.ufo/waves/round-49/`), so the prose number was never compared with the filesystem. | Corrected wording: `:7` → "(47 report files of 49 seats on disk when this lesson was written; the directory held 48 entries, the 48th being `swarm-registry.json`)"; `:212` → "49 seats dispatched; 47 report files on disk at writing (`Mo49SimpCounters.md` landed at `7197160b`, `Mo49ExecCounterTiming.md` only at the round-50 salvage, so the directory now holds 49 report files)". Sweep: `grep -rn '48'` over `corpus/lessons/round-49.md` (43 hits), `LOG.md` (48), `SCORECARD.md` (52) and `.ufo/reports/round-49/mori.md` (11) leaves only the two lesson lines to correct — `LOG.md`'s round-49 entry carries no report count at all (`grep -n '48 reports\|48 of 49\|47 reports\|47 of 49' LOG.md` → only `LOG.md:1356`, an older round), and `SCORECARD.md`'s round-49 section has none (its two hits, `:2641` `round-48 counter` and `:2648` `round 48`, are not counts). **Shown able to fail: not yet shown.** No instrument compares a lesson's prose count with a report directory; the number is checkable by `ls .ufo/waves/round-49/w1 | wc -l` (50 entries) or the settlement scan (present 49), but no control goes red on a wrong prose count — the natural carrier is QUALITY 64's settlement receipt, which round 49 did not commit. |
| M3 | landing (attempt died mid-round) | Attempt 1 (`MoriR50`) dispatched a 40-seat wave at `2026-10-26T05:58:49` (`.ufo/waves/round-50/w1.ready.dispatched`; `w1-dispatch.json` `counts={"spawn":40,…total":40}`) after landing only the freeze `950e99be` (2026-10-26T05:45:42), then died in the orchestrator host crash (~08:50 -03, driver record `.ufo/watchdog.log:1518`), leaving 5 reports: `w1/` holds `Mo50ScoutCoverageFR1.md`, `Mo50ScribeEntryA.md`, `Mo50ScribeEntryB.md`, `Mo50ScribeRowMemcontrol.md`, `Mo50ScribeRowOomKill.md` plus `swarm-registry.json`, and `python3 tools/mori-wave-settlement.py scan` prints `w1-dispatch.json members=40 … present=5, missing=35` (a missing report is not a dead seat — the tool reports filesystem shape only, `tools/mori-wave-settlement.py:18`). No data was landed: both frozen counters are unmet at the freeze/dispatch revision — `count-c1.py 950e99be` → `C1=unmet … mismatches=6` rc 1; `count-c2.py 950e99be` → `C2=unmet claims=0 located=0 … failed=entry_absent` rc 1 — so the attempt's only durable work was the freeze plus what the orchestrator salvaged into `9b8562a3` (the unlanded entry draft `corpus/knowledge/oom-memcg-stat-r50.md` and the wave state). Attempt 2 inverted the order: data commit `487941b9` (2026-10-26T09:05:32/09:27:40) precedes its wave artifacts (`a2w1-dispatch.json` 09:31:31, `a2w1.ready` 09:31:39). | none in the lane for this shape. The bare L1-death class is recorded twice as a driver digest — `corpus/lessons/round-32-verifier-spotcheck.md:16` ("attempt 1 landed nothing: lane tip = base") and `corpus/lessons/round-34-verifier-spotcheck.md:14,16` — but both cover a death with **no** wave dispatched, and neither says what a half-run wave leaves. No lesson row and no QUALITY criterion reads the landing-before-dispatch order for a wave: QUALITY 75 (`corpus/QUALITY.md:330-337`) compares attempt/ledger `at` with the commit that changed the dispatch file, and round 50 holds no `*-attempts.json` or `*-ledger.json` (`ls .ufo/waves/round-50 | grep -c 'attempts\|ledger'` → 0); QUALITY 64 would have recorded `present=5, missing=35` before settlement, and no receipt was committed. | Land the round's data before the dispatch marker is written, so a dead L1 leaves landed work: the observable is that both frozen counters print `met` at the dispatch revision. **Partly shown able to fail**: as a state observable, red at attempt 1's dispatch revision — `C1=unmet … mismatches=6` rc 1 and `C2=unmet … entry_absent` rc 1 at `950e99be` — and green at attempt 2's pre-dispatch data commit — `evidence/a2-c1-at-data.txt` `C1=met … mismatches=0` rc 0, `evidence/a2-c2-at-data.txt` `C2=met claims=22 located=22 … sources=3` rc 0. **Not yet shown as a rule**: nothing in `tools/` or `.ufo/waves/round-50/` reads the dispatch revision's counters, so no committed receipt fails a round because its data was unlanded at dispatch. |
| M4 | overclaim survived the counter | At the data commit `487941b9` the C2 entry met its frozen counter (`evidence/a2-c2-at-data.txt`, `claims=22 located=22`) while wave a2w1 found claims its quotes do not carry: row "the block carries two usage lines" (the usage lines print before the block header, `memcontrol.c.v7.2:1805,1809` vs `:1824-1829`; `a2w1/Mo50bRevRowsMemcgA.md`); row 19 "the victim line is not [rate-limited]" quoting a guard that wraps the `oom-kill:` context line (`oom_kill.c.v7.2:1030-1033,444-454`; `Mo50bSimpEntry.md` F1, `Mo50bCritNoHarm.md` F1); "the stats block prints bytes" (event keys print counts, `memcontrol.c.v7.2:1628-1665,1739-1748`; `Mo50bCritReadingRules.md` 1); "one victim line per killed mm" (`oom_kill.c.v7.2:954-985`); "a stats block means the kill was charged" (`dump_header` also prints before a panic and when nothing is killable, `:1075`, `:1158`); and the `oom_kill` row read the docs sentence against the lane's own `oom-kill-counter-kernel-only-r12.md:12,27` (`Mo50bScribeWhatChanges.md` F1) | none — P-C2 locates quotes and counts beyond-quote words; it does not read entailment or the prose sections (`count-c2.py` docstring limits; `Mo50bSimpEntry.md` F3: front matter plus table alone scores met) | The wave ran after the data commit, with six row-entailment reviewers (`Mo50bRevRows*.md`) and a prose critic; every MED was corrected in the entry before landing and the corrected entry still prints `C2=met claims=22 located=22`. Shown able to fail: the six findings above are the failures; the frozen counter printed met on both the wrong and the corrected text, so the counter is not the check — the row-review seats are, and they are not an instrument. |

## Round-49 routed defects (spot-check §5) — dispositions

1. **Report author date at or after the cited lane tip** (D-a). The report is written and filed after the last lane
   commit, through one `fleet-commit.sh` call; before filing, the L1 compares
   `git -C <fleet> log -1 --format=%aI -- .ufo/reports/round-50/mori.md` (after filing) with
   `git -C <lane> log -1 --format=%cI <lane tip>`; both values go in the report. `a2w1/Mo50bExecAuthorDate.md` found
   the defect present in rounds 48 and 49 and that `scripts/hyaku/fleet-commit.sh:84`'s comment states an invariant
   its code does not produce (fleet-owned; recorded, not edited).
2. **Selftest output files** (D-d): `.ufo/waves/round-50/evidence/selftests/mori-pin-check.txt` and
   `mori-unlanded-check.txt` (attempt-1 receipts, re-run by attempt 2 in a `git archive` of `9b8562a3`: identical but
   for the header line). They are C1's receipts.
3. **48-vs-47 report count** (D-c): the correction entry is below and in `LOG.md` round 50.
4. **`.scratch/` residue and `round-40/scratch/mori-conform-selftest-*`** (D-e): deleted after the wave settled; the
   before/after counts are in the round report and `LOG.md`. Two producers are live and keep refilling it:
   `tools/mori-pin-check.py:884-887` exports a full `git archive` into `<lane>/.scratch/pin-check-*` and removes it
   only in `finally` (56 killed runs left 17G), and `.ufo/waves/round-40/conform.py:69` hardcodes the lane path and
   `mkdtemp`s `mori-conform-selftest-*` inside the lane (`a2w1/Mo50bExecScratchInventory.md` Findings 2-3,
   `Mo50bExecRound49Seats.md` CT-2). 225 `.scratch/` files are tracked and stay; `git clean -fdX -- .scratch` removes
   only the ignored half. The producers are routed to round 51 (a tool change is an instrument change, not this
   round's claim).
5. **Round shape and the two report-less round-49 seats** (D-b): see `## Round shape` below. The two round-49 seats
   were late, not dead: `Mo49SimpCounters.md` was written at 23:02:40, six minutes after the round-49 tip `43d84666`,
   and entered the tree in the snapshot `7197160b`; `Mo49ExecCounterTiming.md` was written at 23:39:03 and entered the
   tree in the salvage `9b8562a3`. Neither changes a round-49 verdict; both add limits (the round-49 counter's "the
   lane repo is only read" sentence is false because `conform.py --selftest` writes into the lane; the `plan_ok` arm
   cannot fail) (`a2w1/Mo50bExecRound49Seats.md`).
6. **`variants=26` against 27 lines** (D-f): `variants` is the number of executed runs minus the single `real`
   control (`.ufo/waves/round-49/count-c1.py:305`, `len(results) - 1`), not the number of edits: the 27 printed
   `variant name=…` lines are 25 frozen edits plus `real-opaque`, a byte-identical opaque-named copy of the unedited
   `SKILL.md`, so `variants=26` and the one line the arithmetic leaves out is `variant name=real`
   (`a2w1/Mo50bExecVariantsCount.md` §5).
7. **K4, the R11 carve-out, the randomised handle**: C1 closes K4 for `SHONEN.md` only — `count-c1.py` never opens
   `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`, `LOG.md` or `PROVINCE.md`, so a tally pin there stays unbound
   (`a2w1/Mo50bScribeRoutedNotes.md` F1). R11 stays routed. The handle rule is **not met** this round: a2w1's seat
   names are role- and claim-bearing (`build-a2w1-spec.py`, `n = P + name`); no instrument this round reads a seat
   name, so the leak reaches no score, and the rule is restated for round 51 as "a blinding handle given to an
   instrument under test is random", not a rule about seat names (`Mo50bScribeRoutedNotes.md` F2).
8. **D-g wording**: `corpus/lessons/round-49.md:96` says the staged `six boots` capture "understates what the receipt
   shows"; the reading order the closure asks for is "a different capture (another day, another note), which also
   shows fewer boots than the receipt" — provenance first. `corpus/knowledge/journal-reach-r49.md` carries no
   "understates" (`grep -c` → 0). The round-49 lesson is not edited; this entry is the correction.

## Correction — the round-49 "48 of 49" report count (D-c)

`corpus/lessons/round-49.md:7` ("48 of 49 reports on disk when this lesson was written") and `:212` ("48 reports on
disk at writing") counted directory entries, not reports: when the lesson was committed (`64c2d5fc`,
2026-10-25T22:49:54) `.ufo/waves/round-49/w1/` held 47 report files plus `swarm-registry.json`. The fleet report
already said 47 at filing. The population then grew to 48 at `7197160b` and 49 at `9b8562a3` (item 5 above).
`LOG.md` carries no round-49 report count, so the `LOG.md` round-50 entry adds the correction rather than fixing a
sentence (`a2w1/Mo50bScribeMistakes.md` M2, `Mo50bScribeLogScorecard.md` Finding 1).

## Round shape

Attempt 1 (L1 MoriR50) dispatched one v1 wave `w1` of 40 seats at 2026-10-26T05:58:49 and died in the orchestrator
host crash; `w1/` holds 5 reports, the registry carries null agent ids and no `w1-results.json` exists, so the other
35 seats' outcomes are **unknown** (not dead, not complete). Attempt 2 (L1 MoriR50a2) ran one v2 wave `a2w1` of 64
seats (policy `ufo-wave-policy-v2.json`, validated rc 0; executor 17, reviewer 15, critic 9, scribe 8, connector 4,
mutation-tester 3, scout 3, sentinel 2, simplifier 2, revenger 1; m_flash roles 39/64, attack roles 27/64). Seats
dispatched across both attempts: 104, above the 100 ceiling; attempt 2 alone is 64, the floor. The contract's
"two v1 waves" shape was not run: attempt 2 integrated the data before its one wave, so that a dead L1 would leave
landed work, and the wave attacked landed bytes (`a2w1/Mo50bCritRoundShape.md`, `Mo50bRevPromptConformance.md` F1).
The L1 held the planner seat.

## Wave a2w1 — integrated findings

Applied to the data before landing (each re-scored: `C2=met claims=22 located=22` holds):

- entry claim cells: the `kernel` row now says the documentation defines the total; the `oom_kill` row no longer
  reads the docs sentence as "any killer" (it agrees with `oom-kill-counter-kernel-only-r12.md`); the failcnt row
  says "not the page counter's own failcnt"; the swap row drops "so the block carries two usage lines"; the
  rate-limit row names the summary header and the `oom-kill:` context line as the guarded prints; the `Tasks state`
  row says "byte-valued charge keys" (`Mo50bRevRowsMemcgA.md`, `Mo50bSimpEntry.md`, `Mo50bCritReadingRules.md`,
  `Mo50bScribeWhatChanges.md`, `Mo50bCritNoHarm.md`).
- entry prose: the intro rule (a block means a memcg OOM, not by itself a kill; `CONSTRAINT_MEMCG`; the two
  no-kill `dump_header` paths); units by key class; the conditional-key list; `kernel` as a documented total that
  the code counts separately; subtree aggregation; group-kill order and the mm-sharing kills without a line; the v1
  failcnt wording; a `## What this changes for mori` section linking r12, r41, r47 and the kernel-only counter entry
  (`Mo50bScribeWhatChanges.md`, `Mo50bConnFR1Frontier.md`, `Mo50bConnSalvage.md`).
- `SOURCES.md` S490/S491 anchors and S490 teaches (see Gate).
- `SHONEN.md` box 4: the unresolvable `w2/R48ConnSiblings.md` pointer → `.ufo/waves/round-48/w2/R48ConnSiblings.md`
  (`Mo50bRevShonen.md`).
- `SCORECARD.md` round-50 correction paragraph: "lagged four admitted closures" was wrong — the four cells skipped 26
  admitted improvements across eleven closures; the paragraph now lists them and names the Last-change convention as
  a limit (`Mo50bScribeMistakes.md` §3 item 2, `Mo50bCritAxesSemantics.md` F1-F2).

Named limits, not repaired (the counters are frozen; a weakness found after scoring is a limit):

- C1 (`count-c1.py`): the verdict word is a substring test, so `round 47 (unimproved)` passes (`Mo50bCritC1Counter.md`
  S1, `Mo50bRevC1Counter.md` 4); a second `## Axes` section is ignored (S4); an Evidence pointer inside an HTML
  comment counts (S2); a pinned path may be a symlink (S8); the selftest cannot detect a broken `admitted` filter
  (`Mo50bMutC1Counter.md` HIGH, `Mo50bRevC1Counter.md` 1); `run()`/`main()` have no selftest coverage; the Score
  column is unread — coverage 6 → 1 still prints met (`Mo50bCritAxesSemantics.md` F3); the counter executes the tool
  SHONEN names, so a committed stub could satisfy the SHONEN half (`Mo50bSentCopies.md` 2); the selftest receipts are
  stamped with the `950e99be` archive and checked by line membership (`Mo50bCritContractFreeze.md` F7); "Last change"
  means the latest admitted improved/harmed closure, not the latest score move (`Mo50bCritAxesSemantics.md`).
- C2 (`count-c2.py`): substring location (boilerplate, mid-word starts and quotes crossing a function boundary
  locate); a claim padded with three new words passes; overlapping windows of one paragraph pass
  (`Mo50bCritC2Counter.md` 1-5); prose sections are unread (`Mo50bSimpEntry.md` F3); the provenance condition the
  counter enforces is not in P-C2's sentence (`Mo50bCritContractFreeze.md` F1).
- Contract and controls: "Met iff mismatches=0 and errors=0" (`count-c1.py:16`) omits the floors and the hidden scan;
  the `box-dropped` control deletes the pin line too (`Mo50bCritContractFreeze.md` F2-F3); `c2-controls.py:20` and
  `c1-controls.py:29,85` cannot be replayed off-host (`Mo50bSentHostPaths.md`).
- Sibling overlap: tsukuroi registers the same v7.2 `oom_kill.c` bytes (S119/S149/S182) at a different scope —
  adjoins, no collision (`Mo50bConnSiblings.md`).

Attempt-1 material re-verified: `w1/Mo50ScoutCoverageFR1.md` (re-checked by `Mo50bConnFR1Frontier.md`; its must-link
list is now carried by the entry's links section), `w1/Mo50ScribeEntryA.md` (the landed entry and rows came from it),
`w1/Mo50ScribeEntryB.md` (its `CONSTRAINT_MEMCG` row was missing from the landed entry and is now in the intro rule,
`Mo50bConnSalvage.md`), `w1/Mo50ScribeRowMemcontrol.md` and `w1/Mo50ScribeRowOomKill.md` (row material, rewritten).
Discarded: none of the five; the 35 attempt-1 seats without a report left nothing to reuse.
