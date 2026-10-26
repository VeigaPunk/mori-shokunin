# Mo50bScribeReadmeSkill — round-50 a2w1: the `README.md` coverage block and the `SKILL.md` Round50 section, drafted

Seat: `Mo50bScribeReadmeSkill` (scribe, leaf; no subagent). Lane: `mori-shokunin`. Scored bytes: the attempt-2 data
commit `487941b9395e89678af0053cc443cdb49cdee6e3`, whose tree is `4548a34dc8b4072abaa4335c1f54a9efcfcc314a`'s
parent-side content plus the wave spec; I read `corpus/`, `SCORECARD.md`, `SHONEN.md` and `SKILL.md` at `4548a34d`.
Read first: `.ufo/waves/round-50/contract.md` (frozen `950e99be`). **Nothing in the lane was edited by this seat** —
the two drafts are fenced in §3/§4 for the L1 to integrate. Scratch
`/fast/scratch/hyaku/mori-r50/Mo50bScribeReadmeSkill/` was removed before this seat ended (§6).

## 1. What the seat asked for, and what was delivered

1. a `## Round-50 coverage additions` block for `corpus/README.md` in the house shape of `## Round-49 coverage
   additions` — one coverage-map row for `corpus/knowledge/oom-memcg-stat-r50.md` on FR1 ground, the sweep proof
   (`evidence/sweep-memcg-stat.txt`) and the Frontier note as a dated superseding sentence → §3;
2. a `## Round50` section for `SKILL.md` in the style of `## Round49`, with gate-table rows (round-49 columns and the
   `self-test` header cell) for `.ufo/waves/round-50/count-c1.py` (`C1_SELFTEST pass=34 fail=0`) and
   `.ufo/waves/round-50/count-c2.py` (`C2_SELFTEST pass=31 fail=0`), both run to confirm → §4, evidence §2;
3. the section's `### Decision row — memcg OOM block (round 50)` table, built from the entry's Reading rules → §4.

## 2. Observed evidence

### 2.1 Both counters' selftests (the assignment's "run both to confirm")

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ TMPDIR=/fast/scratch/hyaku/mori-r50/Mo50bScribeReadmeSkill/tmp \
  python3 .ufo/waves/round-50/count-c1.py --selftest ; echo rc=$?
… 34 `PASS <arm>` lines, no FAIL …
C1_SELFTEST pass=34 fail=0
rc=0
$ TMPDIR=… python3 .ufo/waves/round-50/count-c2.py --selftest ; echo rc=$?
… 31 `PASS <arm>` lines, no FAIL …
C2_SELFTEST pass=31 fail=0
rc=0
```

Both tallies equal the pins the drafts carry and the receipts already on disk (`evidence/selftest-c1.txt` last line
`C1_SELFTEST pass=34 fail=0`; `evidence/selftest-c2.txt` last line `C2_SELFTEST pass=31 fail=0`). Neither counter
accepts `--scratch` on the `--selftest` path: `count-c1.py --selftest --scratch DIR` → `C1_SETUP usage: …` rc 2
(documented, not a defect).

### 2.2 The counters at the landed data commit (the verdict cells the drafts quote)

```
$ TMPDIR=… python3 .ufo/waves/round-50/count-c2.py 487941b9395e89678af0053cc443cdb49cdee6e3 ; echo rc=$?
C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=487941b9395e89678af0053cc443cdb49cdee6e3
rc=0

$ TMPDIR=… python3 .ufo/waves/round-50/count-c1.py 487941b9395e89678af0053cc443cdb49cdee6e3 ; echo rc=$?
item axis coverage expect=round_47_improved got=ok state=ok
… item pin python3_tools/mori-unlanded-check.py_--selftest expect=(17/17) got=UNLANDED_SELFTEST_pass=17_fail=0 state=ok
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=487941b9395e89678af0053cc443cdb49cdee6e3
rc=0
```

Both verdict lines are byte-identical to `evidence/a2-c1-at-data.txt:9` and `evidence/a2-c2-at-data.txt:1` (re-run
here, not copied). The drafts carry `claims=22` and the `C1=met …` line from these reads.

### 2.3 Facts the drafts rest on, re-read at HEAD

- `corpus/README.md` is 683 lines; `## Round-49 coverage additions` at `:677`, its table header at `:679` is
  `| coverage-map row | entry | ground | sweep |` — the shape copied; the block ends the file.
- `SKILL.md` is 1016 lines; `## Round49` at `:981`, gate header at `:1008`
  (`| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |`),
  `### Decision row — journal reach (round 49)` at `:1012`; the file ends with that table.
- `corpus/knowledge/oom-memcg-stat-r50.md`: `coverage-map: FR1`, 22 claim rows (`claims=22` from the frozen counter,
  and a hand count of `| … |` rows in `## Claims` gives 22), Reading rules, limits, boundaries.
- `corpus/SOURCES.md`: S489 `:268`, S490 `:269`, S491 `:270` — all `mined`, opened `2026-10-26`, each naming one of
  the three frozen URLs and citing `corpus/knowledge/oom-memcg-stat-r50.md` in used-by. URL scopes:
  `grep -c 'docs.kernel.org/7.2/admin-guide/cgroup-v2.html' corpus/SOURCES.md` → `1`; `v7.2/mm/memcontrol.c` → S490
  only; `v7.2/mm/oom_kill.c` → S003 `:9`, S476 `:255`, S491 `:270` — the duplicate-URL W04 the contract names, carried
  openly in the draft's entry cell.
- `evidence/sweep-memcg-stat.txt` read in full: seven `git grep -c -F` runs at `7197160b` over `corpus/SOURCES.md`
  `corpus/knowledge` `SKILL.md` return rc 1 (`memory.stat`, `Memory cgroup stats`, `failcnt`, `print_oom_meminfo`,
  `memory_stat_format`, the v7.2 cgroup-v2 URL, the v7.2 memcontrol.c URL); `shmem-rss` and `anon-rss` return one hit
  each (`corpus/knowledge/oom-tracepoints-r47.md:1`); the v7.2 oom_kill.c URL is already in six files. The draft's
  sweep cell states exactly this, including the oom_kill.c line.
- Decision-row grounding, conditional keys: `#ifdef CONFIG_ZSWAP` … `#endif` at
  `corpus/evidence/sources-r50/memcontrol.c.v7.2:1557-1580` (`zswap`, `zswapped`, `zswap_incomp`, `swapcached`,
  `anon_thp`, `file_thp`, `shmem_thp`, `hugetlb`), plus the doc copy's `CONFIG_TRANSPARENT_HUGEPAGE` notes.

### 2.4 The lane's working tree carries another seat's in-flight data edits — disclosed, not touched

At `10:00` the working tree showed four modified files and two untracked wave files, none of them written by me:

```
$ git status --porcelain
 M SCORECARD.md
 M SHONEN.md
 M corpus/SOURCES.md
 M corpus/knowledge/oom-memcg-stat-r50.md
?? .ufo/waves/round-40/scratch/mori-conform-selftest-*/   (transient; see finding 5)
?? .ufo/waves/round-50/a2w1.ready
?? .ufo/waves/round-50/a2w1/
```

The entry revision rewrites the `kernel`, `oom_kill`, `failcnt`, swap-line, rate-limit and Tasks-state claim wordings
and the Reading rules (units split into charge-bytes versus event counts, `pgtables_bytes`, the block's subtree
aggregation, the group-kill order), and adds `## What this changes for mori`. **My decision row follows the
working-tree Reading rules**, because those are the bytes the L1 is landing; every row stays true under the committed
`487941b9` text as well (it is a refinement, not a reversal), and the sources cited (`S489`–`S491`) are unchanged.

Snapshot scored to answer "does the edit still meet the frozen counters": the four working-tree files were copied
into the scratch clone and committed there (`14356bdf`, sha256 of the copied bytes:

```
cdad795e8cae108687fc040b50e1fc87a1dc2b3d7bd4a2c2361d9e008b30e607  SCORECARD.md
dde28e6c7a85bd216f9dc1ac7b613308145c461836ab4680a070937fd1662e0c  SHONEN.md
d55f9badeb89ab516000ad5cc7b43e8bd0d8129f95d09d5ceb06c6435b260fea  corpus/SOURCES.md
8178f8d49df82e6fa4c055b00eef0db8e83a3eb911e5867e5ccb4b33985dff09  corpus/knowledge/oom-memcg-stat-r50.md
```

) and scored with the frozen counters pointed at the clone:

```
$ python3 .ufo/waves/round-50/count-c2.py 14356bdf345854591e73855c5a5da60b90717d81 --repo CLONE
C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok rev=14356bdf345854591e73855c5a5da60b90717d81
$ python3 .ufo/waves/round-50/count-c1.py 14356bdf… --repo CLONE --fleet-repo /home/vgpnk/Projects/shokunin
C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d rev=14356bdf345854591e73855c5a5da60b90717d81
```

So the in-flight edits keep both predicates met (this is a snapshot of bytes mid-edit, not the L1's landing).

### 2.5 Gate compatibility of the two new registry rows — measured

The two registry rows are the only way a landed `SKILL.md` section becomes checkable, so the drafts were run through
the standing reconciler before hand-over, in a `git clone --shared` and a `git archive` export (never in the lane):

| tree measured | command | summary |
|---|---|---|
| pristine `4548a34d`, export, `--root` | `python3 tools/mori-pin-check.py --root TREE --skill TREE/SKILL.md` | `PIN_CHECK=unmet tally_pins=33 digest_pins=8 mismatches=2 unparsed=0 no_command=2 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=- baseline=no` |
| draft on `4548a34d`, same export, `--root` | same | `PIN_CHECK=unmet tally_pins=35 digest_pins=8 mismatches=2 unparsed=0 no_command=2 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=- baseline=no` |
| pristine `4548a34d`, clone, `--rev` | `python3 tools/mori-pin-check.py --rev 4548a34dc8b4072abaa4335c1f54a9efcfcc314a --repo CLONE` | `PIN_CHECK=met tally_pins=33 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=4548a34dc8b4072abaa4335c1f54a9efcfcc314a baseline=no` |
| first draft `427d08af` (on `4548a34d`), clone, `--rev` | `… --rev 427d08afe2d0888a9a46c6c1ba034d8cc30e1936 --repo CLONE` | `PIN_CHECK=unmet tally_pins=35 digest_pins=8 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=427d08afe2d0888a9a46c6c1ba034d8cc30e1936 baseline=no` |
| final draft `11bf4d59` (on the in-flight snapshot), clone, `--rev` | `… --rev 11bf4d5913ae11a72888c035e6be7ba9e1a8a247 --repo CLONE` | `PIN_CHECK=unmet tally_pins=35 digest_pins=8 mismatches=1 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=11bf4d5913ae11a72888c035e6be7ba9e1a8a247 baseline=no` |
| pristine `4548a34d`, clone, `--rev`, repeat (control) | `… --rev 4548a34dc8b4072abaa4335c1f54a9efcfcc314a --repo CLONE` | `PIN_CHECK=met tally_pins=33 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=4548a34dc8b4072abaa4335c1f54a9efcfcc314a baseline=no` |
| the final draft's `SKILL.md` read as registry (`--skill`) while the measured rev is one that exists in the lane | `… --rev 4548a34dc8b4072abaa4335c1f54a9efcfcc314a --repo CLONE --skill SKILL.drafted.md` | `PIN_CHECK=met tally_pins=35 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 misattributed=0 env_unexpanded=0 min_tally_pins=1 rev=4548a34dc8b4072abaa4335c1f54a9efcfcc314a baseline=no` |

Every draft run adds exactly two tally pins (33 → 35) and no parse anomaly: `unparsed=0 hidden=0 duplicate=0
misattributed=0 no_command=0 dropped=0 rebound=0 env_unexpanded=0`. The two new lines measure `state=match` in all
draft runs:

```
pin line=1056 kind=tally prefix=C1_SELFTEST state=match pinned='pass=34 fail=0' observed='pass=34 fail=0' rc=0 cmd='python3 .ufo/waves/round-50/count-c1.py --selftest'
pin line=1057 kind=tally prefix=C2_SELFTEST state=match pinned='pass=31 fail=0' observed='pass=31 fail=0' rc=0 cmd='python3 .ufo/waves/round-50/count-c2.py --selftest'
```

Non-green lines in the final draft `--rev` run:

  - `SKILL.md:911` CONFORM_SELFTEST state=mismatch pinned='pass=11 fail=0' observed='pass=1 fail=10' rc=1 cmd='python3 .ufo/waves/round-40/conform.py 11bf4d5913ae11a72888c035e6be7ba9e1a8a247 --selftest'

Non-green lines in the pristine `--rev` runs (first, then the repeat):

  (none)
  (none)

Reading: `SKILL.md:911` (row `counter conformance v3 (r40)`) is the only non-green line in the draft `--rev` runs, and
its mechanism is measured, not guessed. That row's instrument resolves its paths from a hardcoded lane constant
(`.ufo/waves/round-40/conform.py:69` `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`), so its live
`timeout_state` arm resolves the measured revision **in the lane repo**, not in the measured tree. My draft revisions
exist only in the clone: `git cat-file -e 427d08af…` → absent, `git cat-file -e 4548a34d…` → present. Every arm
therefore gains `timeout_state` as a failure, and the two pristine runs (lane-existing rev) are `met`. The last table
row is the decisive control: the final draft's registry bytes measured at a lane-existing rev are `met`, with the two
new rows `state=match`. So the red line is an artefact of measuring a clone-only commit and does **not** describe what
the L1's gate (candidate bytes at a tip that exists in the lane) will print. The `--root` pair is quoted only to show
the diff is empty there too; four of its lines are export artefacts (no `.git`, `rev=-`), so `--root` is not a reading
of registry health. Column counts were checked by splitting on unescaped `|`: the two gate rows have 8 cells and the
five decision rows 4, matching their headers.

## 3. Draft 1 — `corpus/README.md`, to be appended at the end of the file

```markdown
## Round-50 coverage additions

| coverage-map row | entry | ground | sweep |
|---|---|---|---|
| FR1 event-time attribution — what a memcg OOM burst prints about the charged scope (the usage and swap usage/limit/failcnt lines, a `Memory cgroup stats for <path>:` block written by the same formatter that writes `memory.stat`, the per-victim `Killed process` line) and what a global OOM prints in its place (`__show_mem`, no charged scope) | `knowledge/oom-memcg-stat-r50.md` (S489–S491, opened 2026-10-26; S491 shares its URL with S003 and S476 at a different scope) | FR1 context; states what the kernel prints at the kill, never what a past kill on this host printed, and reports rather than configures (`memory.max`, `memory.oom.group`, `oom_score_adj` are tsukuroi's) | `memory.stat`, `Memory cgroup stats`, `failcnt`, `print_oom_meminfo`, `memory_stat_format` and the v7.2 cgroup-v2 and memcontrol.c URLs → 0 in `corpus/SOURCES.md`, `corpus/knowledge` and `SKILL.md` at `7197160b`; `anon-rss`/`shmem-rss` once, in `oom-tracepoints-r47.md` (the tracepoint schema, not the report block), and the v7.2 `oom_kill.c` URL already present as S003/S476 at another scope (`.ufo/waves/round-50/evidence/sweep-memcg-stat.txt`) |

Dated note (append-only, 2026-10-26): round 50 supersedes the FR1 row's silence about the memcg report block — a
memcg kill prints its charge three ways (the usage and swap lines in kB, the `memory.stat` formatter's stats block
in bytes, the victim's own counters on the `Killed process` line), and a global OOM prints `__show_mem` in place of
the block and names no charged scope (`knowledge/oom-memcg-stat-r50.md`, S489–S491); no frontier row is rewritten.
Still frontier: no host OOM block was read (the lane's no-MESSAGE-grep rule), and attributing a block to a fleet job
rests on the `task_memcg=` token, still [UNKNOWN] in `knowledge/kernel-oom-line-attribution-r12.md`.
```

Integration: one blank line after the current last line (`:683`, end of the round-49 dated note), then the block. It
carries round 49's three elements — heading, a one-row four-column table whose fourth cell is the sweep proof, and one
dated append-only note — and nothing else. A round-48-style `Count: 22 claim rows — … → C2=met claims=22 located=22 …`
sentence was deliberately left out (round 49's shape has no such line); add it between the table and the dated note if
the L1 prefers round 48's extra line. No existing README position is edited.

## 4. Draft 2 — `SKILL.md`, to be appended at the end of the file

```markdown
## Round50 — the calibration counter and the memcg report-block entry (attempt 2)

Round 49's spot-check routed defect 2 — the 114/114 and 17/17 tallies were prose only — and the lane's K4 class
(a pin outside the registry's self-test cell), and round 50 puts both claims on a lowest axis (depth, freshness and
calibration tied at 5; freshness is untouched). Attempt 1 froze the predicates and counters at `950e99be…` and died
in a host crash; attempt 2 landed the data at `487941b9…`. The counters stay frozen: a counter weakness found after
scoring is a named limit, never a repair.

`.ufo/waves/round-50/count-c1.py` (calibration) scores the lane's self-assessment against the fleet record and the
instruments. For each of the six `SCORECARD.md` `## Axes` rows the Last change cell's first `round N` must be the
highest admitted mori round at or before 49 that the fleet `MANIFEST.json` at `e0144996…` grades `improved` or
`harmed` on that axis, the text from that `round N` to the next `;` must name that round's verdict word, and the
Evidence cell must cite that round's spot-check when the file exists at R, else `MANIFEST.json`. Every `SHONEN.md`
tally pin must be a backticked `python3 <path> --selftest` span followed by `(N/M)` or `-> PREFIX pass=N fail=K`,
re-run at R with `git archive`, matching its tally, with a receipt under `.ufo/waves/round-50/evidence/selftests/`
and no stray tally token elsewhere in the file; the floors are 2 pins and 4 boxes. Entering `7197160b` it read `mismatches=6`
(`.ufo/waves/round-50/evidence/control-c1-do-nothing.txt`); at `487941b9…` it reads
`C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d`. Eight controls carry
the reason classes: do-nothing 6, blanket all-latest 6, pins deleted `pins_floor`, corrected number without a
receipt 6, axes-only 2, SHONEN-only 4, box dropped `boxes_floor`, and a witness that is feasibility only. Named
limits: the Score column is not checked (the MANIFEST holds verdicts, not scores); the MANIFEST is trusted, not
re-judged; the hidden-tally scan enumerates `SHONEN.md` only; and a matching tally proves the instrument prints it
at R, not that its arms are good.

`.ufo/waves/round-50/count-c2.py` (depth) scores `corpus/knowledge/oom-memcg-stat-r50.md` against the three frozen
copies under `corpus/evidence/sources-r50/`: at least 10 claim rows, each claim cell 6+ words, unique, carrying 3
words its own quote does not; one mined `SOURCES.md` row per claim, opened 2026-10-26, naming its URL among the
three copies and citing the entry; one backticked 6–25-word quote per row located in that row's copy; all three
copies drawn on and every copy sha256-pinned. At `487941b9…` it reads
`C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok`; entering
`7197160b` it failed with `entry_absent`. Named limits: a located quote proves the words occur in the copy, not
that the claim cell follows from them; the beyond-quote word floor is a floor, not entailment; v7.2 says nothing
about later kernels or cgroup v1; and no host OOM block was read (the no-MESSAGE-grep lane rule), so the entry
states what the kernel prints, not what a past kill on this host printed. Both selftests re-run 2026-10-26:
`C1_SELFTEST pass=34 fail=0` and `C2_SELFTEST pass=31 fail=0`.

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| r50 calibration counter (C1) | gate | `python3 .ufo/waves/round-50/count-c1.py <rev> [--repo DIR] [--fleet-repo DIR] [--fleet-rev REV] [--scratch DIR] [--timeout S]` | 0 → `C1=met items=N axes=6 pins=P boxes=B mismatches=0 errors=0 hidden=0 manifest=<sha12> rev=R` · 1 → `C1=unmet … failed=<reasons>` with one `item` line per axis and pin (expect/got/state) · 2 → `C1_SETUP` (usage, a missing option value, an unresolvable revision on the lane or the fleet repo) | `python3 .ufo/waves/round-50/count-c1.py --selftest` → `C1_SELFTEST pass=34 fail=0` | `FLEET_REV` e0144996…, `THROUGH` 49, `MIN_BOXES` 4, `MIN_PINS` 2, `RECEIPT_DIR` `.ufo/waves/round-50/evidence/selftests/`; limit: the Score column is unchecked and the fleet MANIFEST is trusted | none (read-only `git show` / `git cat-file` / `git archive`; the archive is extracted under `--scratch` and removed) | mori |
| r50 memcg report-block entry counter (C2) | gate | `python3 .ufo/waves/round-50/count-c2.py <rev> [--repo DIR] [--entry PATH]` | 0 → `C2=met claims=N located=N quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok` · 1 → `C2=unmet … failed=<checks>` (entry absent, table, claims floor, bad rows, quote missing, sources floor, pins, provenance) · 2 → `C2_SETUP` (usage, unresolvable revision) | `python3 .ufo/waves/round-50/count-c2.py --selftest` → `C2_SELFTEST pass=31 fail=0` | sha256 of the three copies under `corpus/evidence/sources-r50/` (in-script `COPIES`); `ENTRY` `corpus/knowledge/oom-memcg-stat-r50.md`; `OPENED` 2026-10-26; claims floor 10; quote 6–25 words with 3 words beyond it | none (read-only `git show` / `git rev-parse`) | mori |

### Decision row — memcg OOM block (round 50)

| situation | do | do not | source |
|---|---|---|---|
| a burst carries a usage line, a `Memory cgroup stats for <path>:` block and `Killed process` lines, and their numbers are compared | convert first: the usage and swap lines and the `Killed process` fields are kB, the `Tasks state (memory values in pages)` table is pages except `pgtables_bytes` in bytes, the block prints its charge amounts (`anon`, `file`, `shmem`, `kernel`) in bytes and its `workingset_*`, `pgscan*`, `pgsteal*` keys as counts | compare a block key with a victim-line figure as if both were kB, or read a `workingset_*` count as a byte amount | `corpus/knowledge/oom-memcg-stat-r50.md` (S489–S491) |
| the stats block is read | look keys up by name; read a missing `zswap`, `zswap_incomp`, `anon_thp` or `hugetlb` as not printed under this build's CONFIG (`hugetlb` also at run time), never as zero | index the block by line position, or read a short block as a low charge | `corpus/knowledge/oom-memcg-stat-r50.md` (S489–S490) |
| the block's bytes are totalled | keep `anon`, `file` and `shmem` distinct, and count `kernel_stack`, `pagetables`, `percpu`, `vmalloc` and `slab` once, inside `kernel` as the documentation defines it | add `file` to `shmem` (shmem is the swap-backed part of file), or add the five sub-keys to `kernel` a second time | `corpus/knowledge/oom-memcg-stat-r50.md` (S489) |
| the kill is attributed to a cgroup | read the block as the charged cgroup's charge, aggregated over the cgroup and its descendants, and the `Killed process` counters as the victim's own; read `oom_memcg=` and `task_memcg=` as two labels that can differ when hierarchy is enabled | infer the victim's usage from the block, or read the victim's own cgroup as the cgroup whose limit was hit | `corpus/knowledge/oom-memcg-stat-r50.md` (S490–S491) |
| victim lines print with no stats block, or a group kill is read | read the summary as rate-limited and the victim line as not; order a group kill as the selected victim's line, then `Tasks in <path> are going to be killed due to memory.oom.group set`, then a line per further kill, and keep `oom_kill` (processes) apart from `oom_group_kill` (group events) | read a missing block as proof the kill was global, or expect a line for a process that only shared a victim's mm | `corpus/knowledge/oom-memcg-stat-r50.md` (S491) |
```

Integration: one blank line after `:1016` (last cell of the round-49 decision row), then the section. The gate table
repeats round 49's eight columns and its `self-test` header cell verbatim; the row names are new
(`r50 calibration counter (C1)`, `r50 memcg report-block entry counter (C2)`), so there is no duplicate name and no
`(prefix, argv)` collision with the r44/r45/r48/r49 `C1_SELFTEST`/`C2_SELFTEST` rows (different paths). Neither new
cell carries a hex digest or a line-count pin on purpose: a truncated digest in a cell is a reconciler `mismatch`
risk, so the copy sha256s stay in the counter's `COPIES` and in the SOURCES rows. The `FLEET_REV` cell shows
`e0144996…` in the same truncated shape as round 49's `BASELINE` cell (`2d85e33d…`) and measured green (§2.5).
The decision-row cells follow the entry's *working-tree* Reading rules (§2.4), which refines the committed text.

## 5. Surfaces this seat did not touch

`SCORECARD.md`, `SHONEN.md`, `LOG.md`, `corpus/SOURCES.md`, `corpus/knowledge/`, `tools/`, `considerthese/` and every
file under `.ufo/waves/round-50/` are byte-unchanged by me (the four `M` files in §2.4 are another seat's). C1 reads
`SCORECARD.md`'s Axes table and `SHONEN.md`; C2 reads the entry, its SOURCES rows and the three copies; neither reads
`corpus/README.md` or `SKILL.md`, so the README block rests on the receipts in §2, not on a gate.
`tools/mori-routed-check.py:65` names a `README.md` but as a lane-root fixture path, not as a parser of
`corpus/README.md` (checked; no tool parses that file).

## 6. Limits, unverified, housekeeping

- Reconciler runs were done on a scratch `git clone --shared` and on `git archive` exports, never in the lane repo:
  its `--rev` mode writes its export under `<repo>/.scratch`, outside this seat's write scope. The clone commits
  `427d08af`, `14356bdf` and `11bf4d59` are fixture commits under `/fast/scratch/hyaku/mori-r50/Mo50bScribeReadmeSkill/`
  (toplevel verified equal to the clone dir before the first commit) and are gone with the scratch dir. The lane repo
  was read only (`git show`, `git archive`, `git rev-parse`, `git log`, `git grep`, `git status`, `git diff`).
- The reconciler's measurement of `SKILL.md:911` has a side effect inside the lane tree: that row's selftest creates
  temp dirs under `.ufo/waves/round-40/scratch/` (the tool's hardcoded scratch root) and leaves some behind
  (finding 5: 12 at `10:00:18`, 4 at `10:07:42`, 960K). I did not delete them: deleting under `.ufo/waves/round-40/`
  is outside "write only your own report", and round 49's routed defect 4 owns that count-based cleanup.
- Not run: the L1's own pre-land gate with `--baseline-rev`, the round-end census, any counter other than the two
  round-50 ones. `count-c1.py <rev>` takes ~7 s; both selftests return in under a second.
- No `pacman` transaction (host-wide pause) and nothing installed or upgraded this seat, so there is no tool/version
  record to add. No kernel journal `MESSAGE` text was read, no cgroup limit or unit state touched, no OOM triggered.
- The two drafts are unrendered bytes: no Markdown renderer was run over them, so cell rendering (e.g. `<path>` inside
  a code span) is as on disk, not visually confirmed.

## Findings

1. **LOW — `SKILL.md:911`** (row `counter conformance v3 (r40)`): `tools/mori-pin-check.py --rev` prints
   `CONFORM_SELFTEST pass=1 fail=10` against the pinned `pass=11 fail=0` on both draft commits, while both pristine
   runs print `PIN_CHECK=met`. The cause is measured and is not the draft's content: the row's instrument resolves the
   measured revision in the hardcoded lane repo (`.ufo/waves/round-40/conform.py:69`), and the draft revisions exist
   only in my scratch clone (`git cat-file -e` absent for `427d08af`, present for `4548a34d`), so its live
   `timeout_state` arm fails on every arm. The drafted registry measured at a lane-existing rev is `met` (§2.5, last
   row). No action for the L1; recorded because a clone-based gate run will keep printing this line.
2. **LOW — `corpus/knowledge/oom-memcg-stat-r50.md` Reading rules** (working-tree revision): the CONFIG-conditional
   key statement (`zswap`, `zswap_incomp`, `swapcached`, `anon_thp`, `file_thp`, `shmem_thp`, `hugetlb`, "and others")
   still has no claim-table row; the mechanism is in the frozen copies (`memcontrol.c.v7.2:1557-1580`). My decision
   row cites `(S489–S490)` for it; the frozen counter cannot be changed this round, so this is a named coverage gap.
3. **LOW — `.ufo/waves/round-50/evidence/sweep-memcg-stat.txt`**: the swept set is `corpus/SOURCES.md`,
   `corpus/knowledge` and `SKILL.md` at `7197160b`. The round-50 draft adds `memory.stat` / `Memory cgroup stats` /
   `failcnt` tokens to `corpus/README.md`, which is outside that set — the before-proof stays valid, and the draft's
   sweep cell names the swept paths so the boundary stays visible.
4. **LOW — `corpus/README.md` block**: `claims=22` appears in the draft's SKILL row and in this report but not in the
   README block, because round 49's block shape has no `Count:` line (offered to the L1 in §3 as an optional line).
5. **LOW — `.ufo/waves/round-40/scratch/mori-conform-selftest-*`**: untracked temp dirs appear and disappear under
   the lane's `.ufo/waves/round-40/scratch/` while the reconciler measures the r40 conformance row, whose selftest uses
   the lane's hardcoded scratch root (`.ufo/waves/round-40/conform.py:70`). Observed counts inside this seat's window:
   12 dirs at `10:00:18`, 15 at `10:07:29`, 4 at `10:07:42`; the directory held 960K at `10:07:42`. The tool removes
   its own work dir on the paths that complete, so the residue is the transient class round 49's routed defect 4
   deletes at round end with a before/after count. Left in place deliberately (§6).
6. **LOW (informational) — reconciler modes**: `--root` over an archive export prints four non-green lines from
   pre-existing rows (`R19_SELFTEST` 25/1, two `no_command` rows, r49 `C1_SELFTEST` 0/1) that are export artefacts —
   `--rev` on the clone removes all four. A `--root` run must not be read as registry health.

Artifacts: this report
(`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-50/a2w1/Mo50bScribeReadmeSkill.md`); the two drafts are
inline in §3 and §4 (copied into this report before the scratch dir was removed). Every command whose output is cited
is reproduced verbatim above.
