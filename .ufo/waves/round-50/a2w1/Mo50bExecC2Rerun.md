# Mo50bExecC2Rerun — C2 independent re-run (round 50, wave a2w1)

Seat: executor, leaf. Assigned job: re-run `count-c2.py` at the landed data revision in a `git archive`, run its
`--selftest`, run it at `7197160b` and `9b8562a3`, verify `evidence/freeze-sha256.txt`, and re-run
`controls/c2-controls.py` in a **copy** of `.ufo/waves/round-50` and diff its receipts. Plus (this wave) an
independent attack on the landed data.

Nothing was edited in `.ufo/waves/round-50`, `corpus/`, `tools/`, `SKILL.md`, `SHONEN.md`, `SCORECARD.md` or
`LOG.md`; this file is the only write. The frozen counter, predicate, controls and kill rules were used as
committed and are not proposed for change. No pacman transaction, no tool install, no subagent, no host-state
change; `/home/vgpnk/Projects/shokuknow*` was read only.

## 0. Environment

| item | value |
|---|---|
| lane repo | `/home/vgpnk/Projects/shokunin/mori-shokunin` |
| lane HEAD during this run | `4548a34dc8b4072abaa4335c1f54a9efcfcc314a` |
| landed data revision (R) | `487941b9395e89678af0053cc443cdb49cdee6e3` |
| entering tip | `7197160b927f04db294c9553fb48fadcc7a3f4e3` |
| attempt-1 salvage | `9b8562a371dc916fdc0fc686619ea1e271a3e118` |
| ancestry | `7197160b` → `950e99be` (freeze) → `649e14cf` → `9b8562a3` → `487941b9`; `git merge-base --is-ancestor 7197160b 487941b9` → 0, `--is-ancestor 487941b9 HEAD` → 0 |
| scratch | `/fast/scratch/hyaku/mori-r50/Mo50bExecC2Rerun/` (`TMPDIR` set there for every call; removed at the end) |
| disk guard | `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` → rc 0; `/fast` 24% used, 614.0G free; `/tmp` 2%, 126G free |
| working tree vs HEAD, C2 paths (`corpus/knowledge`, `corpus/SOURCES.md`, `corpus/evidence/sources-r50`, `count-c2.py`, `controls/`, `evidence/`) | `git status --porcelain` empty → the bytes I measured are the committed bytes |
| landed tip vs HEAD, C2 paths | `git diff --stat 487941b9 HEAD -- <those paths>` empty → C2 data unchanged since landing |

## 1. Freeze integrity — all 34 entries OK

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && sha256sum -c .ufo/waves/round-50/evidence/freeze-sha256.txt
corpus/evidence/sources-r50/cgroup-v2.7.2.html: OK
corpus/evidence/sources-r50/memcontrol.c.v7.2: OK
corpus/evidence/sources-r50/oom_kill.c.v7.2: OK
.ufo/waves/round-50/assimilation/collisions: OK
... (34/34 lines, every one "OK", no FAILED line)
.ufo/waves/round-50/evidence/sweep-memcg-stat.txt: OK
exit=0
```

Corroborating: `wc -l < evidence/freeze-sha256.txt` → 34; the list itself is unchanged since the freeze commit
(`git diff --stat 950e99be -- …/freeze-sha256.txt` empty; `sha256sum` of the working-tree file and of
`git show 950e99be:…/freeze-sha256.txt` are both `a0887775aed0ebfb68cc6aa70b6c94b8dff2ebf95056072e7d08d2f984d00c8b`);
`count-c2.py` pin in the list is `533c8403b90e650c786381bbf1394cf327b331936a4111b9faba4abd068ee55d`, which is the
sha256 of the file in both the lane and the scratch clone. The three copy pins in the list equal the `COPIES`
table inside the counter (`2d716cb7…`, `8a28e0bc…`, `452f1348…`).

## 2. The counter at the three revisions (lane repo, `git show` reader)

```
$ python3 .ufo/waves/round-50/count-c2.py 487941b9395e89678af0053cc443cdb49cdee6e3
C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9395e89678af0053cc443cdb49cdee6e3
exit=0

$ python3 .ufo/waves/round-50/count-c2.py 7197160b927f04db294c9553fb48fadcc7a3f4e3
C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad rev=7197160b927f04db294c9553fb48fadcc7a3f4e3 failed=entry_absent,pins
exit=1

$ python3 .ufo/waves/round-50/count-c2.py 9b8562a371dc916fdc0fc686619ea1e271a3e118
C2=unmet claims=22 located=0 quote_missing=0 bad_rows=22 sources=0 source_rows=bad pins=ok provenance=ok rev=9b8562a371dc916fdc0fc686619ea1e271a3e118 failed=bad_rows,source_rows,sources_floor
exit=1
```

Both frozen receipts reproduce byte-exactly:

```
$ diff <(head -1 .ufo/waves/round-50/evidence/control-c2-donothing-git.txt) <(counter 7197160b | head -1)
(empty)  -> "ENTERING LINE IDENTICAL to control-c2-donothing-git.txt"
$ diff <(head -1 .ufo/waves/round-50/evidence/a2-c2-at-data.txt) <(counter 487941b9 | head -1)
(empty)  -> "DATA LINE IDENTICAL to a2-c2-at-data.txt"
```

Determinism and exit-code contract: two runs at R give identical lines; `count-c2.py` with no argument → rc 2,
with an unresolvable rev → rc 2, unmet → rc 1, met → rc 0 (matches the header's `Exit 0 met, 1 unmet, 2 setup`).

Why `pins=bad` at the entering tip (not a counter defect): `git ls-tree 7197160b corpus/evidence/sources-r50`
prints nothing (path absent at the entering tip); the copies first exist at the freeze commit
(`git ls-tree --name-only 950e99be corpus/evidence/sources-r50` → the directory). So a pin check against R's tree
is genuinely bad before the freeze — the receipt says what it should.

Why `9b8562a3` is unmet although `claims=22`: `git diff 9b8562a3 487941b9 -- corpus/knowledge/oom-memcg-stat-r50.md`
is empty (**the entry is byte-identical in both revisions**), while `git show 9b8562a3:corpus/SOURCES.md | grep -c
'^| S489\|^| S490\|^| S491'` → `0` and at `487941b9` → `3`. The salvage had the entry but not its SOURCES rows, so
every row failed its source-cell check (`bad_rows=22`, `sources=0`). The data commit's `--stat` shows exactly that
difference: 3 lines added to `corpus/SOURCES.md` (plus `SCORECARD.md`, `SHONEN.md` and the three
`assimilation/a2/` receipts, which are C1's half).

## 3. Independence: `git archive` + a repo built from the archive

```
$ git archive 487941b9395e89678af0053cc443cdb49cdee6e3 | tar -x -C $S/arc487        # extract_exit=0, 12388 files
$ D=$(mktemp -d -p $S fixture.XXXXXX); git -C "$D" init -q; cp -a "$S/arc487/." "$D"/
$ git -C "$D" rev-parse --show-toplevel     -> /fast/scratch/hyaku/mori-r50/Mo50bExecC2Rerun/fixture.5KoB3q  (== $D)
$ git -C "$D" -c user.name=Mo50bExecC2Rerun -c user.email=seat@fixture.invalid commit -q -m "archive of 487941b…"
$ git -C "$D" rev-parse HEAD                -> a1034377cadb3354abb260870d9637efa0a420e1

$ python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/count-c2.py a1034377… --repo "$D"
C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=a1034377cadb3354abb260870d9637efa0a420e1
exit=0
```

Archive bytes vs `git show` bytes (sha256, all five C2 paths): `MATCH` for `cgroup-v2.7.2.html` `2d716cb7…`,
`memcontrol.c.v7.2` `8a28e0bc…`, `oom_kill.c.v7.2` `452f1348…`,
`corpus/knowledge/oom-memcg-stat-r50.md` `0fac741cce21d76e…`, `corpus/SOURCES.md` `33f294439e479f38…`.
The counter therefore reads only committed bytes and gives the same verdict over an independently materialised
tree that shares no objects, no refs and no working-tree state with the lane. The archive copy's own
`count-c2.py --selftest` (script located inside the extracted tree, so its `lane` is the archive) → `C2_SELFTEST
pass=31 fail=0`, exit 0.

## 4. Selftest

```
$ python3 .ufo/waves/round-50/count-c2.py --selftest
PASS honest_met … PASS normalise_keeps_visible_text      (31 PASS lines, no FAIL)
C2_SELFTEST pass=31 fail=0
exit=0
$ diff .ufo/waves/round-50/evidence/selftest-c2.txt <rerun>
(empty)  -> receipt byte-identical
```

Arm count matches the frozen receipt (31 checks, `evidence/selftest-c2.txt`), including the two round-49 critic
classes (`breadcrumb_identical_claims_unmet` expecting `bad_rows=9`, `claim_echoes_quote_unmet`).

## 5. Controls re-run in a copy (never in the real wave dir)

```
$ git clone --shared -q /home/vgpnk/Projects/shokunin/mori-shokunin $S/clone      # clone_exit=0, HEAD 4548a34d
$ sha256sum $S/clone/.ufo/waves/round-50/count-c2.py …/clone/…/controls/c2-controls.py
533c8403…count-c2.py (both identical)   641eecc5…c2-controls.py (both identical)
$ git -C $S/clone status --porcelain | wc -l  -> 0
$ cd $S/clone && python3 .ufo/waves/round-50/controls/c2-controls.py 7197160b927f04db294c9553fb48fadcc7a3f4e3
do-nothing   C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=ok provenance=bad rev=7197160b… failed=entry_absent
staged-r46   C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=ok provenance=bad rev=7197160b… failed=claims_floor,provenance,source_rows,sources_floor,table
staged-r47   C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=ok provenance=bad rev=7197160b… failed=claims_floor,provenance,source_rows,sources_floor,table
staged-rows  C2=unmet claims=0 located=0 quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=ok provenance=bad rev=7197160b… failed=claims_floor,provenance,source_rows,sources_floor,table
controls_exit=0
```

Receipt diff, clone vs frozen `evidence/`:

```
IDENTICAL control-c2-do-nothing.txt
IDENTICAL control-c2-staged-r46.txt
IDENTICAL control-c2-staged-r47.txt
IDENTICAL control-c2-staged-rows.txt
```

All four receipts are reproduced byte-for-byte; nothing was written into the lane's wave directory. The
`pins=ok` in these receipts (vs `pins=bad` in `control-c2-donothing-git.txt`) is the documented difference of
the overlay reader: it supplies the frozen copies from the tree, the `git` run reads R's tree.

## 6. Independent re-implementation of the predicate (no import of `count-c2.py`)

My own parser + my own HTML normaliser (`html.parser`, `convert_charrefs`, script/style/comments dropped) over
the working-tree copies (which `sha256sum -c` proved equal to the frozen bytes):

```
header=['claim','source','quote'] rows=22
row  src   claim_words quote_words beyond(counter-class) beyond(strict) occurrences_in_copy spans
  1  S489           24          17                    16             15                   1     1
  2  S489           21          16                    10             10                   1     1
  3  S489           17          14                     7              7                   1     1
  4  S489           19          17                     5              5                   1     1
  5  S489           22          21                    13             13                   1     1
  6  S489           17          17                    14             14                   2     1
  7  S489           22          15                    12             12                   1     1
  8  S490           19           7                     9              9                   1     1
  9  S490           21           9                    14             13                   1     1
 10  S490           19           7                    10             10                   1     1
 11  S490           22           7                    15             15                   1     1
 12  S490           22           7                    15             13                   1     1
 13  S490           19           8                    12             10                   1     1
 14  S490           20           7                    13             10                   1     1
 15  S490           20          14                    12             12                   1     1
 16  S491           16          12                     5              5                   1     1
 17  S491           20          12                    15            14                   1     1
 18  S491           16           8                    11            10                   1     1
 19  S491           25           7                    19            18                   1     1
 20  S491           18          13                     9              9                   1     1
 21  S491           21          15                    13            10                   1     1
 22  S491           20          20                    11            11                   1     1
pins: all three copies match their frozen sha256
sid_use: {'S489': 7, 'S490': 8, 'S491': 7}
min claim words=16  min quote words=7 max=21  min beyond=5  min beyond_strict=5  min occurrences=1
```

So under an independent implementation: 22 rows, 22 located, 3 sources, every claim ≥ 16 words (floor 6), every
quote 7–21 words (band 6–25), every row ≥ 5 words beyond its quote even under a stricter `[A-Za-z]{3,}`
tokenisation (floor 3), every quote a single span, no duplicate claim, no duplicate quote. The counter's
`claims=22 located=22 sources=3` is an accurate description of the landed bytes; it is not double counting.

## 7. Mutation battery on the landed data (fixture repo only)

Six edits applied to the archived tree, each committed in the fixture, each scored by the frozen counter with
`--repo "$D"`, then restored:

| mutation (fixture commit) | counter line | rc | expected reason |
|---|---|---|---|
| baseline (archive of R) | `C2=met claims=22 located=22 … sources=3 … pins=ok provenance=ok` | 0 | — |
| one word changed inside a located quote | `C2=unmet … located=21 quote_missing=1 … failed=quote_missing` | 1 | quote no longer in copy |
| one claim cell copied over the next (breadcrumb) | `C2=unmet … located=21 bad_rows=1 … failed=bad_rows,source_rows` | 1 | duplicate claim |
| one source cell changed `S489`→`S992` | `C2=unmet … bad_rows=1 … provenance=bad … failed=bad_rows,provenance,source_rows` | 1 | no such SOURCES row |
| `verified-at:` line removed | `C2=unmet … bad_rows=0 … provenance=bad failed=provenance` | 1 | header requirement |
| S489's SOURCES status `mined`→`queued` | `C2=unmet … located=15 bad_rows=7 sources=2 … failed=bad_rows,source_rows,sources_floor` | 1 | row not mined |
| one quote truncated to 4 words | `C2=unmet … located=21 bad_rows=1 … failed=bad_rows,source_rows` | 1 | quote length band |
| restore both files | `C2=met claims=22 located=22 …` | 0 | — |

6/6 mutations flip the verdict with the specific reason, and the restore returns `met`: the predicate binds on
this entry's actual bytes, not only on the selftest's synthetic rows.

## 8. Attack on the landed data

### 8.1 Five quoted rows sit outside the anchor cell of their own SOURCES row (data defect, predicate-blind)

I mapped every quote to source line numbers whitespace-flexibly and compared with the S490/S491 `anchor` cells:

```
=== S490 anchor 'mm/memcontrol.c:1546-1608,1693-1748,1751,1770,1787-1830,4905-4919' (180 lines)
row 8  (usage line)                    1805-1805     inside
row 9  (MEMCG_MAX failcnt)             1800-1803     inside
row 10 (swap line)                     1809-1809     inside
row 11 (stats block -> KERN_INFO)      1827-1829     inside
row 12 (memory.stat same formatter)    4913-4915     inside
row 13 (oom_memcg / global_oom)        1774-1778     OUTSIDE  (anchor jumps 1770 -> 1787)
row 14 (task_memcg)                    1779-1782     OUTSIDE  (same gap)
row 15 (Tasks in … going to be killed) 1996-1998     OUTSIDE  (mem_cgroup_print_oom_group body, 1994-1999 unlisted)
=== S491 anchor 'mm/oom_kill.c:400-410,424-431,444-454,456-469,912-951,1169-1170' (86 lines)
row 16 (Killed process)                945           inside
row 17 (message chosen)                1169-1170     inside
row 18 (memcg block vs __show_mem)     465-468       inside
row 19 (ratelimit guard)               1030-1033     OUTSIDE  (oom_kill_process body 1008-1054 unlisted)
row 20 (oom-kill: constraint line)     446-449       inside
row 21 (counters before the signal)    934-936       inside
row 22 (Tasks state in pages)          424-425       inside
```

The lines are real (`memcontrol.c.v7.2:1774-1782` = `if (memcg) { pr_cont(",oom_memcg="); … if (p) {
pr_cont(",task_memcg="); …`; `1996-1998` = `pr_info("Tasks in "); …`; `oom_kill.c.v7.2:1030-1033` =
`if (__ratelimit(&oom_rs)) { dump_header(oc); dump_oom_victim(oc, victim); }`). P-C2 never reads the anchor
cell, so `C2=met` is unaffected, but four table rows point a reader at an anchor that does not contain their
quote. Draft for the L1 (data correction only; I changed nothing):

```diff
-| S490 | … | mm/memcontrol.c:1546-1608,1693-1748,1751,1770,1787-1830,4905-4919; …
+| S490 | … | mm/memcontrol.c:1546-1608,1693-1748,1751,1770-1786,1787-1830,1994-1999,4905-4919; …
-| S491 | … | mm/oom_kill.c:400-410,424-431,444-454,456-469,912-951,1169-1170; …
+| S491 | … | mm/oom_kill.c:400-410,424-431,444-454,456-469,912-951,1008-1054,1169-1170; …
```

### 8.2 Four S489 quotes are only findable because the normaliser inserts a space per tag

The counter's HTML rule is `re.sub(r"<[^>]+>", " ", …)`. The page marks the keys as `<dt>anon</dt><dd><p>Amount …`,
and the `brk()`/`sbrk()` words as `<code …><span class="pre">brk()</span></code>,`:

```
S489 row 1 tags-as-space=True  tags-deleted=True
S489 row 2 tags-as-space=True  tags-deleted=False <- needs inserted spaces at tag boundaries
S489 row 3 tags-as-space=True  tags-deleted=False <- needs inserted spaces at tag boundaries
S489 row 4 tags-as-space=True  tags-deleted=False <- needs inserted spaces at tag boundaries
S489 row 5 tags-as-space=True  tags-deleted=False <- needs inserted spaces at tag boundaries
S489 row 6 tags-as-space=True  tags-deleted=True
S489 row 7 tags-as-space=True  tags-deleted=True
```

Concretely, table row 3's quote reads `… such as brk() , sbrk() , and mmap(MAP_ANONYMOUS).` while the document
renders `… such as brk(), sbrk(), and mmap(MAP_ANONYMOUS).` (verified against
`cgroup-v2.7.2.html:1406-1407`). The words are all present, so `located` is honest under the frozen rule; but a
reader who greps a plain-text rendering of the page (tags deleted, no separator) gets no hit for rows 3–6, and
row 3's quoted punctuation is not the page's. Reading: quote-location is a whitespace-and-markup-tolerant
match, not a literal-text match.

### 8.3 Row 6's quote occurs twice in the copy

`Don’t rely on items remaining in a fixed position; use the keys to look up specific values!` occurs at
normalised offsets 54102 and 61620 of `cgroup-v2.7.2.html`, both preceded by the same 90 characters, i.e. the
page repeats that paragraph. The counter's uniqueness is table-local, so a quote repeated in the document still
counts as one anchor. Harmless here (both occurrences say the same thing), but "unique in the table" is not
"unique in the copy".

### 8.4 `claims=` counts raw rows, so the claims floor passes on rows that are all bad

At `9b8562a3` the counter prints `claims=22 … bad_rows=22` and does **not** raise `claims_floor`; the floor is
`claims < MIN_CLAIMS` where `claims = len(rows)` before any validation. `claims=22` in a receipt therefore means
"22 parsed rows", not "22 valid claims"; `located`/`bad_rows` are the quality numbers. No false `met` results
from this in my runs (`bad_rows` always fires), but the receipt label reads stronger than the measurement.

### 8.5 The three staged controls are one control, not three

`staged-r46`, `staged-r47` and `staged-rows` print *identical* lines (`claims=0 … failed=claims_floor,
provenance,source_rows,sources_floor,table`): none of the staged entries parses as a table, so appending row
S533 changes nothing observable. The receipt set cannot distinguish "too few rows" from "entry without a
parseable table" from "entry plus a staged SOURCES row"; all three land on the same `claims=0` path. The
contract already predicts those three failure names, so this is a limit of the control set, not a breach.

### 8.6 The beyond-quote floor is implemented broader than its sentence

P-C2 says "3 words of 3+ **letters**"; the counter uses `[A-Za-z][A-Za-z0-9_]{2,}`, so tokens such as
`PAGE_SIZE`, `memcg`, `v7` (2 chars, excluded) or `2d716cb` (starts with a digit, excluded) are counted as
"words" when they are ≥ 3 characters and start with a letter. Measured effect on this data: none —
`min beyond=5` under the counter's class and `min beyond_strict=5` under my stricter `[A-Za-z]{3,}` — but the
implementation's floor is marginally easier than the predicate text for other entries.

### 8.7 The entry's most distinctive marker is prose-only

The lead paragraph says a memcg OOM prints "a `Memory cgroup stats for <path>:` block". The source line is
`memcontrol.c.v7.2:1824-1826` (`pr_info("Memory cgroup stats for "); pr_cont_cgroup_path(memcg->css.cgroup);
pr_cont(":");`) — inside S490's anchor, but **no table row quotes it**; rows 11–12 quote the formatter calls at
1827-1829 / 4913-4915. P-C2 cannot see prose, so the claim rests on prose alone. (True as stated — I read the
code — but unpinned by the instrument.)

### 8.8 Semantic spot-check of all 22 rows — no contradiction found

I re-opened each quote against its surroundings, not only its existence:

- rows 1, 7: `cgroup-v2.7.2.html` "All memory amounts are in bytes. If a value which is not aligned to PAGE_SIZE
  is written, the value may be rounded up to the closest PAGE_SIZE multiple when read back." and the
  `memory.events` `oom_kill` sentence — both claims faithful (including "when read back").
- rows 2–5: the `memory.stat` `<dt>/<dd>` definitions of `anon`, `file`, `shmem`, `kernel (npn)` — claims
  faithful (see 8.2 for the markup artefact in the quoting).
- rows 6: the "keys, not position" paragraph — faithful (see 8.3).
- rows 8–15: `memcontrol.c.v7.2:1800-1809`, `1824-1830`, `4913-4915`, `1770-1786`, `1994-1999`; `MEMCG_MAX` is the
  `max` memory event (`memory_stat` events printer: `seq_printf(m, "max %lu\n",
  atomic_long_read(&events[MEMCG_MAX]))` at 4879), so row 9's "MEMCG_MAX event counter, not a per-page charge
  failure count" is right for the default hierarchy; rows 13–15 correct.
- rows 16–22: `oom_kill.c.v7.2:945` (fields and units as claimed), `1169-1170` (the two message strings),
  `465-468` (`__show_mem` for global OOM vs the memcg block), `1030-1033` with `__oom_kill_process` called at
  1042 outside the ratelimit guard (row 19's "victim line is not rate-limited" holds: the `Killed process`
  `pr_err` is inside `__oom_kill_process`, not inside the guard), `446-449`, `934-936` (counters before
  `do_send_sig_info` at 943), `424-425` (`Tasks state (memory values in pages)`).

Entailment beyond "the words are there and the surrounding text agrees" is still not machine-checked — that
limit stands in the contract and stands here.

## Named limits of this re-run

- Three revisions only (`7197160b`, `9b8562a3`, `487941b9`). I did not re-fetch the three upstream URLs
  (no network use); copy fidelity is asserted from the frozen sha256 list, not measured against the live web.
- I verified the predicate as implemented and by an independent re-implementation of the same sentence; I did not
  attempt a second, differently-worded predicate.
- The anchor and markup findings are data/metadata defects the frozen predicate is blind to; they change no
  verdict and I changed no file.
- `located` proves document occurrence, not entailment; my 8.8 reading is a reviewer's judgement, not an
  instrument.
- No host kill record was read (lane rule: no MESSAGE-text grep), so nothing here speaks to any past host OOM.

## Findings

- **MED — `corpus/SOURCES.md` S490 anchor cell (line 269) under-declares where three of its rows' quotes live.**
  Table rows 13, 14 (`memcontrol.c.v7.2:1774-1778`, `1779-1782`) fall in the gap between the listed `1770` and
  `1787-1830`; row 15 (`1996-1998`) is in `mem_cgroup_print_oom_group`, whose range `1994-1999` is not listed.
  P-C2 does not read anchors, so `C2=met` stands; the anchor is a reader's route to the evidence and it misses.
- **MED — `corpus/SOURCES.md` S491 anchor cell (line 270) omits `oom_kill_process`'s body.** Table row 19's
  quote (`oom_kill.c.v7.2:1030-1033`, the `__ratelimit(&oom_rs)` guard) is outside every listed range
  (`400-410,424-431,444-454,456-469,912-951,1169-1170`); `1008-1054` is missing.
- **LOW — `corpus/knowledge/oom-memcg-stat-r50.md` row 3 (and rows 4–6) quote text that only exists after the
  counter's tag→space substitution.** `brk() , sbrk() ,` is not the page's `brk(), sbrk(),`
  (`cgroup-v2.7.2.html:1406-1407`); four of seven S489 quotes are absent from a tag-deleted rendering. Located
  under the frozen rule, but not literal text, and not greppable in a plain-text extraction.
- **LOW — `corpus/knowledge/oom-memcg-stat-r50.md` row 6 quote occurs twice in its copy**
  (`cgroup-v2.7.2.html`, normalised offsets 54102 and 61620). Table-local uniqueness is satisfied; copy-local
  uniqueness is not, so the quote does not by itself pin one location.
- **LOW — `count-c2.py` `claims` is a raw row count, not a valid-row count.** Evidence: at `9b8562a3` it prints
  `claims=22 … bad_rows=22` and raises no `claims_floor`. The receipt's `claims=N` overstates what N measures;
  `located`/`bad_rows` carry the quality. (No false `met` observed.)
- **LOW — the three staged C2 controls are indistinguishable.** `staged-r46`, `staged-r47` and `staged-rows`
  produce identical output (`claims=0 … failed=claims_floor,provenance,source_rows,sources_floor,table`), so the
  receipts exercise one failure path (no parseable table) three times, not three defects.
- **LOW — `count-c2.py` `words_beyond()` uses `[A-Za-z][A-Za-z0-9_]{2,}`**, broader than P-C2's "words of 3+
  letters" (counts tokens containing digits/underscores, e.g. `PAGE_SIZE`, `memcg`). No effect measured on this
  data (`min beyond` 5 both ways).
- **LOW — the entry's `Memory cgroup stats for <path>:` marker is prose-only.** `memcontrol.c.v7.2:1824-1826` is
  inside S490's anchor but no table row quotes it, so the round's FR1 attribution marker is not pinned by the
  instrument.
- **INFO — the C2 claim holds on my independent re-run.** `C2=met claims=22 located=22 quote_missing=0
  bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok` at `487941b9`, exit 0, reproduced over a
  `git archive` tree in a separate repo (fixture `a1034377…`), with its selftest at 31/0, the freeze list 34/34 OK,
  the four control receipts byte-identical, and 6/6 mutations on the landed data flipping it to `unmet` with the
  right reason. The pre-state behaves as the contract says (`7197160b` → `failed=entry_absent,pins`, because the
  copies do not exist before the freeze commit).
