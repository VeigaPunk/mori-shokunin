# ReviewCounterData — mori round 33, wave 2

Scope: run `count-c1-a1.py` and `count-c1.py` at measured data revision
`62db24c01d5b7c2247f43852ea2b28d0ae5e40c8`, paste outputs, then review the outputs line by line
against the P-C1-A1 sentence (contract `.ufo/waves/round-33/contract.md:119-123`) for any
condition that passed for a wrong reason. No receipt created. No lane writes outside this file.

## 1. Counter outputs (verbatim) and exit codes

### `count-c1-a1.py` — exit 1, `C1=unmet`

```
rev=62db24c01d5b7c2247f43852ea2b28d0ae5e40c8 repo=/home/vgpnk/Projects/shokunin/mori-shokunin
entry=present entry_sha256=8e04b9efc391d5c5e1764e796f6731e59cb12a758bd652bf822cb715891b8d15 head_lines=yes html_comments=0
tables=1 decision_tables=1 unfenced_decision_tables=1
rows=14 rows_ok=14 distinct_rows=14 distinct_observations=14 short_readings=0
new_id_rows=14 new_ids=11 (S180,S181,S182,S183,S184,S185,S186,S187,S188,S189,S190)
S180 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/block/stat.rst
S181 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst
S182 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/block/genhd.c
S183 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/part_stat.h
S184 gate=ok quotes=3 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-core.c
S185 gate=ok quotes=2 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c
S186 gate=ok quotes=3 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/blk_types.h
S187 gate=ok quotes=4 copy=ok fetch=ok url=https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/ABI/testing/procfs-diskstats
S188 gate=ok quotes=3 copy=ok fetch=ok url=https://github.com/torvalds/linux/commit/b6866318657717c8914673a6394894d12bc9ff5e.patch
S189 gate=ok quotes=2 copy=ok fetch=ok url=https://github.com/torvalds/linux/commit/bdca3c87fb7ad1cc61d231d37eb0d8f90d001e0c.patch
S190 gate=ok quotes=3 copy=ok fetch=ok url=https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/iostat.c
gates_ok=11/11 copies_ok=11/11 fetch_ok=11/11 distinct_sources=yes
rows_without_quote_overlap=0
readings_copying_quotes=0
dispatch_rule=no judge=absent
skill_rows=5
unmet_conditions=judge
C1=unmet
EXIT_A1=1
```

### `count-c1.py` (frozen original) — exit 1, `C1=unmet`

Identical output except: no `distinct_observations` field in the rows line, no
`readings_copying_quotes` line, `distinct_rows=14` computed with `norm` instead of `canon`, and
`EXIT_ORIG=1`. Diff of the two scripts (command output, section 4) matches amendment A1's three
additions exactly: canon-based row and observation distinctness, the 6-word copied-run check, and
`spans_bad` hard-failing the judge condition. `count-c1.py` unchanged, per contract line 109.

Both runs: `unmet_conditions=judge` only — the expected pre-judge state (`judge=absent`,
`.ufo/waves/round-33/judge/` absent at the rev; verified by `git ls-tree`: no `judge/` entry).
`dispatch_rule=no` is consistent: `dispatch.json` is also absent, so there is nothing to test R-J
against. Honest fail: the counter did not fake a dispatch pass.

## 2. Line-by-line review against P-C1-A1 — any condition passed for a wrong reason?

I reproduced the counter's parsing (same regexes) and computed the overlap sets and longest common
canon runs myself. Findings below; full per-row overlap table in section 3.

**No condition passed for a wrong reason.** Detail:

- `entry=present head_lines=yes html_comments=0`: legitimate. `source:`/`verified-at:`/`recheck:`
  are lines 3-5 of the entry; no `<!--` anywhere (entry lines 1-59). Right reason.
- `decision_tables=1 unfenced_decision_tables=1`: the file holds exactly one table (lines 17-32)
  with header cells `observation`, `reading`, `verdict`, `sources`, outside any fence. Right reason.
- `rows=14 rows_ok=14 distinct_rows=14 distinct_observations=14 short_readings=0`: all 14 rows are
  5-cell (verified independently: `awk -F'|'` gives 14 rows x 5 cells); every sources cell names
  S### ids that exist in SOURCES.md (11 rows, S180-S190, verified `grep -c` = 11); every reading >=
  8 words by inspection (all are >= 24 words); observations are distinct even under `canon`. Right
  reason.
- `new_id_rows=14 new_ids=11`: all 14 rows cite only new ids; 11 distinct >= threshold of 8/5.
- `gates_ok/copies_ok/fetch_ok=11/11`: each new id has exactly one `admit` Gate row
  (`lessons/round-33.md:15-25`) carrying one https URL, a 64-hex sha, 1-4 located quotes of 3-25
  words (S183 has 2, S185 has 2, S189 has 2 — all >= 1); each committed copy
  `corpus/evidence/sources-r33/S###.src` sha256-matches and contains every quote; each live URL
  fetched at measurement time sha256-matches. Right reason — this is the strongest part of the
  claim: pinned tags/commit patches hashed identically on re-fetch.
- `distinct_sources=yes`: 11 distinct URLs, 11 distinct shas, no new id's URL appears inside
  another new id's SOURCES cell. Right reason. Separately verified: the entering tip's SOURCES.md
  carries other `raw.githubusercontent.com/torvalds/linux/v7.2/` URLs (31 lines) but none of the
  11 exact new paths — the novelty check is a real pass, not a substring accident.
- `rows_without_quote_overlap=0`: see section 3. Pass is genuine for every row, but rows 9 and 3
  pass at minimal margin (2 and 3 words), and row 9's pass leans on the generic word `sectors`.
  Not a wrong-reason pass (each has a source-specific identifier too), flagged as minor.
- `readings_copying_quotes=0`: longest common canon run between any reading and any cited Gate
  quote is 4 (row 12, "the same 17 statistics" vs S181 quote), well under 6. Right reason.
- `skill_rows=5`: 5 lines qualify (SKILL.md:815-819, each >= 12 words, `Round33` + entry path). The
  section heading at SKILL.md:811 does NOT qualify (10 words) — the count is exactly the predicate
  count, no padding. Right reason.
- `dispatch_rule=no judge=absent` -> `unmet_conditions=judge`: correct and expected pre-judge.

## 3. Quote-overlap margin table (my reproduction, words4 intersection)

```
row  1 n=14  (S187,S180,S186)  dense: sector/512-byte vocabulary, all grounded
row  2 n=8   (S180,S184,S185)  bdev_end_io_acct, blk_account_io_completion, part_stat_add + 5
row  3 n=3   (S183,S184)       bdev_whole, part_stat_add, sectors          <- thin
row  4 n=7   (S181)            boot, counter, cumulative, device, field, overflows, when
row  5 n=5   (S187,S182)       bdev_count_inflight, currently, line, progress, total
row  6 n=6   (S184,S181,S182)  field, io_ticks, jiffies_to_msecs, nonzero, stamp, when
row  7 n=12  (S187,S180)       1000, requests, second, waiting, writing, ...
row  8 n=7   (S187)            discard, fields, flush, four, line, sectors, written
row  9 n=2   (S182)            bdev_nr_sectors, sectors                    <- thinnest
row 10 n=6   (S189,S182)       discard, four, reads, same, stat_discard, writes
row 11 n=10  (S188,S187)       barriers, disk, executed, flush(es), layer, partitions, requests
row 12 n=10  (S181,S180)       both, decimal, file, line, same, stat, statistics, whitespace
row 13 n=6   (S181)            boot, counter, cumulative, reattachment, reset, which
row 14 n=5   (S190,S181)       current, device, previous, sample, when
```

Margin notes (minor, informational for the C1 judge, not counter defects):

- **Row 9 (n=2)**: one of the two words is `sectors`, the generic example named in the assignment.
  The other, `bdev_nr_sectors`, is the exact kernel function in S182's located quote
  (`S182.src:1371-1372`), so the pass is grounded — but if `sectors` were noise this row sits at
  the minimum. Severity: minor.
- **Row 3 (n=3)**: `bdev_whole` and `part_stat_add` are quote-specific identifiers (S183.src:61-63);
  `sectors` is the third. Legitimate, thin margin. Severity: minor.
- **Row 5**: `bdev_count_inflight` carries it; `progress`, `currently`, `line`, `total` are
  generic. Grounded. Minor.
- **Row 14**: all five words (`current`, `device`, `previous`, `sample`, `when`) are generic — none
  is an identifier like `ioi`/`ioj`/`wsectors`/`S_VALUE`. The reading does name `ioi`/`ioj`; they
  are < 4 canonical letters (`ioi` len 3 → filtered by len>=4? `ioi` is len 3, yes filtered;
  `ioj` len 3 filtered). So the check passes purely on generic vocabulary. The cited quotes do
  state the row's facts, so content-wise it is honest, but the lexical check here is weakest in
  the table. Severity: minor (worst case in table).
- **Rows 4, 13**: overlaps include `when`, `which`, `device`, `field` (generic), but
  `cumulative`/`reattachment`/`overflows`/`reset` are content words. Fine.
- **Row 12 near-miss under the A1 copy check**: shares the 4-run "the same 17 statistics" with
  S181's quote verbatim. Limit is 6, so legal; 2 words of slack. Informational.

## 4. Checks run (all commands executed, no unrun "pass")

- Both counters at `62db24c0...`, exit codes 1/1, outputs above (network fetches live, ~2.7 s each).
- `diff count-c1.py count-c1-a1.py` — additions confined to A1's three stated changes.
- `git show <rev>:corpus/lessons/round-33.md` Gate rows 15-25 — 11 admit rows, fields verified.
- `git show <rev>:corpus/SOURCES.md` — exactly 11 new-id rows, cell 7 = `mined` on each.
- `git show <entering>:corpus/SOURCES.md` — none of the 11 exact new URLs present (URL novelty real).
- `git ls-tree <rev> .ufo/waves/round-33/` — no `judge/` directory; receipt genuinely absent.
- Python reproduction of `cells/QUOTE_RE/canon/words4/6-gram` logic — matched counter results.
- `awk` cell-arity check on all 14 data rows; SKILL.md qualifying-line word counts (815-819).

## 5. Residual risk

- The counter cannot test verdict-cell truthfulness or R-J semantics; that is the C1 judge's job,
  and the receipt is correctly absent now. Rows 9, 3, 14 are the rows a strict judge should read
  first: their counter overlap is thin (row 14 entirely generic vocabulary).
- `fetch_ok` was measured against live URLs at review time and passed 11/11, so byte-stability
  holds today; it remains a fetch-time dependency by design.
- Nothing else in scope was found failing. No tools installed (none needed; stock python3/git/curl
  used by the counter itself). Report under 200 lines; no receipt created; no lane edits beyond
  this file.
