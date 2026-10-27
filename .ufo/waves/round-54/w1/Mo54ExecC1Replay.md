# Mo54ExecC1Replay — independent replay of the round-54 C1 counter, scope and landed ledger

Seat: Mo54ExecC1Replay (executor, leaf). Lane: mori-shokunin. Date: 2026-10-27.
Revisions: entering tip `39dcf4d7e410d362781a47e8365ca23b5c807598`; freeze `6830f3af992d906bfa1e17e3743e631ab834f67c`;
landed data `78295c764093ff1f6cee08d7246679900bde7265`; wave-spec tip `2d0347a32b6befd7fd946a83319e04f6d8f004b9`.
Scratch: `/fast/scratch/hyaku/mori-r54/Mo54ExecC1Replay/` (removed at the end; nothing cited below depends on it).

Work scope: re-run the frozen C1 counter at the data commit, its selftest, its scope listing and the
do-nothing control; compare each with the frozen receipts; and re-derive the scope set independently
without importing or reusing `count-c1.py`. I also re-derived the landed ledger's rows, pins,
SOURCES cells and the ledger's own "moved"/drift prose from the committed bytes. I did not judge the
claims' meaning (not a voter), did not read any wave seat's report, and did not read or score any vote.

## Commands run (cwd = scratch, nothing written outside it)

```
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-54/count-c1.py 78295c764093ff1f6cee08d7246679900bde7265
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-54/count-c1.py --selftest
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-54/count-c1.py --scope
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-54/count-c1.py 39dcf4d7e410d362781a47e8365ca23b5c807598
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-54/count-c1.py 39dcf4d7e410d362781a47e8365ca23b5c807598 --repo <scratch clone>
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-54/count-c1.py 2d0347a32b6befd7fd946a83319e04f6d8f004b9
```

### At the data commit (data receipt reproduces byte-for-byte)

```
C1=unmet scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok provenance=ok held=31 absent=0 holds=31 changed=0 voted=0 dissent=0 rev=78295c764093ff1f6cee08d7246679900bde7265 failed=votes
exit=1
```

`diff` of this against `evidence/c1-at-data.txt` (its `command:` line excluded) prints nothing: IDENTICAL.

### Selftest (57 assertions, all pass; receipt reproduces byte-for-byte)

```
ok   honest_met
...
ok   scope_reader
C1_SELFTEST pass=57 fail=0
exit=0
```

`diff` against `evidence/selftest-c1.txt` (its trailing `exit=` line excluded) prints nothing: IDENTICAL.
The full check list matched line for line; every named arm of the predicate (ledger absence, table shape,
row set, status, line, quote, sources row, provenance, pins, votes, dissent, replacement, results binding,
scope) has a passing fixture and the failing fixtures read `unmet`.

### Scope (31 rows; identical to the frozen receipt)

`diff evidence/c1-scope.txt scope-mine.txt` prints only `33d32 < exit=0` — the receipt captured the
shell exit line, the counter's own output ends at `scope=31`; the 31 row lines and the total are identical.
Exit code 0. Re-run against a `git clone --shared` of the lane at the same entering rev gave a
byte-identical scope file and the same control reading (below), so the listing is derived from committed
blobs, not from the working tree.

### Do-nothing control (entering tip)

```
C1=unmet scope=31 rows=0 matched=0 status_ok=0 line_ok=0 quote_ok=0 source_rows=bad pins=bad provenance=bad held=0 absent=0 holds=0 changed=0 voted=0 dissent=0 rev=39dcf4d7e410d362781a47e8365ca23b5c807598 failed=ledger_absent,pins
exit=1
```

Identical to the `C1=` line of `evidence/control-c1-do-nothing.txt`, including the failure list
`ledger_absent,pins`. The L1's receipt ran it through a control clone that no longer exists; `evaluate()`
reads only `git show <rev>:<path>` blobs, so the lane at `39dcf4d7` is the same input, and I reproduced it
both on the lane and on a fresh `--shared` clone in scratch (`--repo`), with the same line and the same scope.

### Spec tip (stability)

```
C1=unmet scope=31 rows=31 matched=31 status_ok=31 line_ok=31 quote_ok=31 source_rows=ok pins=ok provenance=ok held=31 absent=0 holds=31 changed=0 voted=0 dissent=0 rev=2d0347a32b6befd7fd946a83319e04f6d8f004b9 failed=votes
exit=1
```

`git diff --stat 78295c7 2d0347a3 -- corpus/ .ufo/waves/round-54/count-c1.py .ufo/waves/round-54/count-c2.py`
is empty: the data and both counters are unchanged between the data commit and the wave-spec tip.

### Frozen counter bytes

`sha256sum` of the working-tree `count-c1.py` is `e97a11986694b60f3a5d9d50b151553072f08a8a8d46cbea8f4b63a90dff433c`,
equal to the `evidence/freeze-sha256.txt` pin and to the blob at all three of `6830f3af`, `78295c76`,
`2d0347a3`. `contract.md` (`1e06f99f…`), `c1-scope.txt` (`40de6cd2…`) and `selftest-c1.txt` (`ad76c31c…`)
also equal their pins. The predicate actually measured is the frozen one.

## Receipt comparison summary

| artifact | expected | observed | verdict |
|---|---|---|---|
| at-data line | `rows=31 … voted=0 … failed=votes`, exit 1 | same, byte-identical | PASS |
| selftest | `pass=57 fail=0`, exit 0 | same, byte-identical | PASS |
| scope | 31 rows + `scope=31`, exit 0 | same (receipt's captured `exit=0` line only) | PASS |
| do-nothing control | `rows=0 … pins=bad … failed=ledger_absent,pins`, exit 1 | same, byte-identical | PASS |
| no-votes control shape | `rows=31 … voted=0 failed=votes` | at-data line equals it with the rev elided | PASS |

## Independent scope enumeration (my own parser, no counter import)

Method: `git show 39dcf4d7:corpus/knowledge/<entry>.md` for every entry `git ls-tree` names, my own
markdown-table reader (header cells lowercased `claim|source|quote`, alignment row skipped, unescaped-pipe
splitting), SOURCES row per `S<id>` at the same tip, URL test **over every cell of the SOURCES row** (broader
than the counter's cell 1), hash = first 12 hex of sha256 of the whitespace-collapsed claim, minus the hashes
in the round-53 ledger read at the same tip.

Observed:

- 63 `corpus/knowledge/*.md` entries at the entering tip; 6 claim|source|quote tables; 0 table rows with a
  cell count other than 3 (so no row is silently skipped by the shape test).
- 127 claim rows in those tables; **77** carry a SOURCES row whose URL names Linux v7.2
  (raw.githubusercontent `v7.2/`, cgit `?h=v7.2`, `docs.kernel.org/7.2/`). The registry does hold one
  jsdelivr v7.2 row (S473, `Documentation/admin-guide/cgroup-v2.rst`), but no claim|source|quote table row
  cites it — `census-cgroup-levels-r45.md` names it only in a `source:` line and prose, and that entry has
  no such table — so the jsdelivr arm of the URL test is exercised by the counter's selftest (`scope_reader`,
  fixture S005), not by this dataset.
- Per entry: `oom-memcg-stat-r50.md` 22, `commit-runway-read-r53.md` 8, `quota-observability-r48.md` 1,
  `memavailable-estimate-r51.md` 18, `overcommit-commit-limit-r52.md` 28. The last two (46 rows) are the
  round-53 ledger's set.
- Round-53 ledger hashes at the entering tip: 46, all 46 present among the 77 pinned rows, no duplicate
  hashes in the pinned set. Identity holds exactly: 77 − 46 = 31.
- My 31 rows == the counter's `--scope` output: same hash set, same entry, same path for each hash, same
  quote text (after normalising the counter's `docs:` path prefix). No row was found with a v7.2 URL outside
  the SOURCES row's source column, so the counter's narrower URL scan loses nothing on this dataset.

## Independent verification of the landed data at `78295c7`

Re-derived from committed blobs, again without reading the ledger's own verdicts:

- Ledger: provenance lines `source:`, `verified-at:`, `recheck:` present; one table with the exact 7-cell
  header; 31 rows; hash set equals the scope set exactly (no extra, no duplicate, no missing).
- Per row: entry cell names the entry that holds the hash (31/31); status equals my own derivation from the
  committed v7.3 copy, quote collapsed and HTML stripped (31/31 — all `held`); quote is exactly one
  backticked span of 6–25 words (31/31); quote equals the row's v7.2 quote verbatim (31/31); quote occurs in
  the v7.3 copy (31/31); line cell is a line on which that quote begins in the raw v7.3 copy (31/31);
  disposition cell is `holds` or `changed` (31/31, all `holds`).
- SOURCES: each row's S-id exists at R, has 11 cells, carries the frozen v7.3 URL of that path, `mined`,
  `opened` 2026-10-26/27, and lists the ledger in `used-by` (31/31). The ledger's `source:` line cites all
  eight ids used by rows. All eight rows' own `sha256 <prefix>` and `copy <path>` cells agree with the
  pinned blobs (`S508 4dfcce2b8fa8`, `S514 678410005f88`, `S515 bdb6159cc237`, `S516 452f1348e79c`,
  `S517 2c26e67751f9`, `S518 4a107bc381b3`, `S519 66a5ad60566f`, `S520 b478c1bae998`).
- Pins: each of the eight v7.3 copies hashed at R equals its `freeze-sha256.txt` pin, and each copy's bytes
  are unchanged from the freeze commit to the data commit.
- "Where the quotes moved" table: 31 rows; every path resolves to a committed v7.2 copy; the stated v7.2
  lines are lines where the v7.2 quote begins in that copy; the first listed v7.3 line equals the ledger's
  line cell; every listed delta (`+0`, `+4`, `+31`, `+45`, `+84`) equals v7.3 line minus v7.2 line. The
  two-occurrence row (`460b0cafc999`, v7.2 `1399,1605` → v7.3 `1430,1636`) checks out on both occurrences.
- "Four of the eight files did not change at all": `mm/oom_kill.c`, `lib/percpu_counter.c`,
  `include/linux/percpu_counter.h`, `include/uapi/asm-generic/errno.h` are byte-identical between the two
  committed copies; the errno.h v7.3 copy has the same sha256 as S481's v7.2 copy.
- `git diff --no-index --numstat` on the other copies: `mm/util.c` +7/−7 (= the ledger's "14 changed
  lines", with the three quoted lines at +0), `mm/memcontrol.c` +204/−54 (= the ledger's "258 changed
  lines"; the quoted lines move +45 and +84), `mm/mm_init.c` +74/−137 (the quoted block moves +4 as stated;
  the file is churned far more widely, which the ledger does not claim otherwise).
- Drift prose: word diff of my tag-stripped, entity-decoded copies gives exactly **32** non-equal opcodes
  (16 replace, 16 insert) — the ledger's "changed in 32 places". Both pressure files are documented
  `read-only` in 7.2 and `read-write` in 7.3; the throttle field is `use_delay`/`delay` in **microseconds**
  in 7.2 and `use_delay`/`delay_nsec` in **nanoseconds** in 7.3; `non-hierarchical` occurs 0 times in the
  7.2 page and once in the 7.3 page, in the CFS-bandwidth note. The first raw html hunk is the new
  top-level toc captions before the quoted rows, consistent with "+31 from the new top-level navigation".

## Vote arm state at the measured revisions

`git ls-tree 78295c7 .ufo/waves/round-54/w1/` is empty and `git cat-file -e 78295c7:…/w1-results.json`
exits 128; the same holds at `2d0347a3`. Hence `voted=0`, `dissent=0`, `failed=votes` is the only possible
reading at the data commit and at the spec tip, and it is exactly the frozen no-votes control's reading with
the rev elided. This is the contract's expected pre-vote state (`count-c1.py` reads vote files with
`git show <R>:…`, so uncommitted seat reports cannot move any reading). I did not open any seat report and
make no statement about whether the votes required by P-C1 will be cast.

## Findings

**F1 — LOW — the status arm is degenerate on this dataset; only votes carry meaning.**
`count-c1.py:270-363` (vote arm 346-352), `contract.md:51-53`. All 77 v7.2-pinned quotes of the round-53 entries were already
held, and I independently confirm all 31 remaining v7.2 quotes occur verbatim in the v7.3 copies
(`held=31 absent=0`). A ledger that copies every v7.2 quote and labels every row `held`/`holds` satisfies
status, quote equality, quote location and the line arm as long as the line is real; the pins only separate
v7.2 bytes. The claim's freshness content therefore rests entirely on the two-voter disposition arm — a
named limit, confirmed empirically rather than argued. Routed item for round 55.

**F2 — LOW — the line arm accepts any occurrence, so "line" is not a unique anchor.**
`count-c1.py:153-164` and the line test at `count-c1.py:330-332`. For hash `460b0cafc999` the quote begins
at v7.3 lines 1430 **and** 1636 (the ledger's moved table itself lists both); the predicate is satisfied by
citing 1430. A line cell proves the words begin somewhere on that line, not that the cited occurrence is
the one the claim is about.

**F3 — LOW — the S-id is bound to a copy by the frozen URL, not by the SOURCES row's own copy/digest cells.**
`count-c1.py:212-236` (scope) with the row test at `count-c1.py:333-342`: the counter builds the expected
URL from its own path→copy map and never reads the row's `copy` cell or `sha256` prefix. A row citing the
correct v7.3 URL but a different copy path (or a stale prefix) still scores `source_rows=ok`. On the landed
data all eight rows agree with the pinned blobs (prefixes listed above), so there is no divergence now.
Routed item for round 55.

**F4 — LOW — the scope URL test reads only the SOURCES row's source cell.**
`count-c1.py:212-236`. I repeated the test over every cell of every SOURCES row: the same five entries and
the same 77 rows match, so the narrower scan loses nothing at the entering tip. Limit only, no divergence.

**F5 — LOW — scope D excludes prose, and the round-50 entry's prose anchors are still v7.2 positions.**
`contract.md:53-55`; `corpus/knowledge/oom-memcg-stat-r50.md` (unchanged at the data commit). The ledger
records the offsets (`memcontrol.c` +45 and +84, the rendered page +31) but the entry's in-prose anchors
(e.g. `memcontrol.c:1774-1830`) still name v7.2 lines, so a reader following the prose at v7.3 lands on the
wrong lines. Disclosed in the contract as outside D; a candidate for the round-55 routing list rather than a
C1 defect.

**F6 — LOW (state note) — `C1=unmet failed=votes` at the data commit is not evidence against C1.**
`count-c1.py:58-61`, `238-268`, `346-352`. Both possible pre-settlement inputs (data commit, spec tip) lack the
`w1/` directory and `w1-results.json`, so the at-data reading is the no-votes control by construction.
Whoever scores the landed tip must measure a revision that contains the twelve seat reports **and** the
orchestrator's `w1-results.json`; otherwise this same line reappears regardless of the votes actually cast.

## Limits of this replay

Read-only throughout: `git show`/`ls-tree`/`diff`/`rev-parse`/`cat-file`/`clone --shared` in scratch, plus
Python over those bytes. No host reads were needed for this seat and none were made; no network fetch was
needed (the v7.2/v7.3 bytes are pinned in the lane); no pacman, no system change, no mutation of the lane or
any other repo; nothing written under `~/.local/bin`; no tools installed. I did not verify the servers'
v7.3 bytes (the contract's named limit: pins prove the fetched bytes, not the tag). Claim truth at v7.3 is
the voters' judgement, not mine. Skipped per instruction: no build/test/lint gate was run (editing wave).

## Cleanup

Scratch `/fast/scratch/hyaku/mori-r54/Mo54ExecC1Replay/` (clone, scripts, temporary copies) removed after
this report was written; the receipts above quote the outputs, so no evidence path depends on it.
