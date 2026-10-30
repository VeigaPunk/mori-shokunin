# Mo61RevC2 — bypass hunt on frozen count-c2.py (C2, PSI v7.3 recheck ledger)

Seat: Mo61RevC2 (leaf, read-only). Entering rev `325f7e639916fcbc77fa2ec7475951a1b86bb1cb`.
Counter: `.ufo/waves/round-61/count-c2.py`, sha256 `82d0fee6124685f8a50f93550f3665703a33dce644948958db642a77d5aec2d8`
(equal to the freeze `7370a731` blob). Pinned copies: sha256 re-verified, all six match `PINS`.
All fixtures were built in a scratch repo (`git -C <fixture> init`, identity `t <t@t>` inside fixtures only;
`--show-toplevel` asserted per fixture). No VCS mutation in the lane or fleet. No tools installed.
Scratch removed before yielding; the receipts below are copied in full.

## Verdict

C2 as frozen does **not** bind row status (`same|moved|changed`) to any v7.2 bytes, and it does not bind the
ledger to r24's claims. It only checks that each row's quote is a byte substring of v7.3 at the row's own stated
location, plus pointer-key set equality, a sha pin on six v7.3 copies, a `| mined |` line per copy in SOURCES.md,
and three header bands. A ledger that lies about every row passes. Constructions and exact bytes follow.

## Live receipts (entering rev, default floor)

```
$ count-c2.py 325f7e63… --repo <lane> --scratch …/live
C2=unmet pointers=47 rows=0 same=0 moved=0 changed=0 quotes_ok=0 spans_ok=0 sources=0 failed=entry_absent rev=325f7e63…   rc=1
```
Matches the contract's do-nothing control. Pointer enumeration on the r24 entry at that rev gives 47.

Selftest (default floor) — **red**:
```
$ count-c2.py --selftest --repo <lane> --scratch …/st-default
case good: ok=False want=True FAIL failed=['pointer_floor:6<40']
… (9 other cases pass)
C2_SELFTEST pass=9 fail=1          rc=1
```
Selftest with `--floor 1`, diffed against the committed receipt `.ufo/waves/round-61/evidence/selftest-c2.txt`:
```
$ count-c2.py --selftest --floor 1 …  → C2_SELFTEST pass=10 fail=0   rc=0
$ diff evidence/selftest-c2.txt <floor-1 output>   → only the extra "rc=0" line
```
So the committed receipt (10/0) was produced with a `--floor 1` override that the contract does not record; the
default invocation that dispatch would use is red (9/1). The receipt carries no command line. (Finding F8.)

## Fixture results (all rev = fixture commit; `--floor` default)

| fixture | ledger | sources line | result | rc |
|---|---|---|---|---|
| A-same-or-forced | honest-looking: 33 `same`, 14 `changed` (forced, see F5) | none | `C2=unmet … changed=14 … failed=rows_src:*` | 1 |
| A + stuffed line (D) | same as A | stuffed (App. B) | **`C2=met pointers=47 rows=47 same=33 moved=0 changed=14 quotes_ok=47 spans_ok=47 sources=6 failed=none`** | **0** |
| B-lies-with-stuff | 45 `changed` to far files + 2 `moved` to own range (App. A) | stuffed | **`C2=met pointers=47 rows=47 same=0 moved=2 changed=45 quotes_ok=47 spans_ok=47 sources=6 failed=none`** | **0** |
| C-hidden-with-stuff | B ledger inside `<!-- … -->` | stuffed | **`C2=met … changed=45 … failed=none`** | **0** |
| N1 stitched (negative) | stitched quotes at psi.c:1268-1270, psi.rst:36-38 | stuffed | `C2=unmet … quotes_ok=45 … failed=quote_missing:psi.c:1268-1270;quote_missing:psi.rst:36-38` | 1 |
| N2 in-range stitch (negative) | psi.c:1268-1270 quote `collect_percpu_times(group, PSI_AVGS, NULL); if (now >=` | stuffed | `C2=unmet … failed=quote_missing:psi.c:1268-1270` | 1 |

## Findings

### F1 — status and location are unbound; "moved"/"changed" accept anything (BYPASS, accepted)
- `count-c2.py:117-148`: the quote is checked only against `span_of(anchor)` for `same` and against `span_of(loc)`
  for `moved|changed`. `status` is never compared with anything; `loc` is never compared with the anchor; the
  loc may be any of the six files over its whole length (`loc_oob` only rejects `hi > len(lines)`).
- Accepted constructions (exact rows from App. A, all in fixture B, all rc=0 with the stuffed line):
  - Moved row whose loc is a line inside the ORIGINAL range (identity move, accepted):
    `| psi.c:1538-1550 | moved | psi.c:1538-1550 | `static int psi_io_show(struct seq_file *m, void` |`
    and `| cgroup-v2.rst:1066-1087 | moved | cgroup-v2.rst:1066-1087 | `A read-write single value file that allowed` |`
  - Changed row quoting v7.3 words that sit far from the claim (no relation to the pointer's topic checked):
    `| psi.c:1712 | changed | kernel-parameters.txt:1-8710 | `AGP	AGP (Accelerated Graphics Port)` |`
    `| psi.rst:36-38 | changed | cgroup-v2.rst:1-3581 | `This is the authoritative documentation on` |`
    `| psi.c:1282-1288 | changed | Kconfig:1-2368 | `- Re-run Kconfig when the` |`
  - Every r24 pointer can be given a `changed` row pointing at a whole other file; sources≥4 is met by the loc
    files themselves (sources=6 in B).
- Consequence: the frozen kill rule "a quote not byte-located where its row states" does not fire on these rows.
  Their quotes are located where they state; the lie is in the status/loc relation, which the counter never reads.

### F2 — no v7.2 pin, so "same/moved/changed" is structurally unverifiable (design gap, not fixable under freeze)
- The counter pins six v7.3 copies and nothing from v7.2. The r24 entry cites v7.2 line ranges. Nothing in the
  repo at rev or in the frozen counter supplies v7.2 bytes, so no counter arm can say whether a range "is the same".
  F1 follows directly. [INFERENCE from the counter source and the pin list; no v7.2 copy exists in the repo.]

### F3 — SOURCES arm satisfied by one stuffed line (BYPASS, accepted)
- `count-c2.py` rows_src check (lines ~173-186): a line must contain `corpus/evidence/sources-r61/<f>`, `| S`,
  `| mined |` and `psi-v73-recheck-r61.md`. Nothing checks `opened this round` (the contract's wording), the
  date column, or that the id is new. A single line covering all six copies satisfies all six checks (App. B).
  Confirmed: fixture D (honest-looking A ledger + App. B line) → rc=0; B and C also rc=0 with it.
- Rev SOURCES.md already has 282 `| mined |` rows (`git show <rev>:corpus/SOURCES.md | grep -c '| mined |'`), so the
  token is not discriminating either.

### F4 — pointer enumeration misses r24 citations; those pointers are never required (BYPASS of "anchor-set" arm)
Enumerator is `NAMES = (file):(\d+)(-\d+)?` (count-c2.py:39-40): only a file name directly followed by a colon
is captured. Found by a fuller regex over r24 (`file:N[-M](,N[-M])*` and bare `:N-M` after a backticked file):
- Comma-list tails, not enumerated: `psi.c:1545`, `psi.c:1550` (from `psi.c:1540,1545,1550,1686`, r24 line ~89),
  `psi.c:408-411` and `psi.c:572` (from `psi.c:342-360,408-411,551,572`), `psi_types.h:57-70`.
- Bare-colon forms, not enumerated: `cgroup-v2.rst:1083-1087`, `:1215-1221`, `:1911-1915`, `:2171-2175`
  (r24 line ~143, "`irq.pressure` at `:1083-1087`, `cpu.pressure` at `:1215-1221`…").
- Ledger fixtures contain exactly the 47 enumerated anchors and omit these nine; `rows_missing` is not raised.
  Their content is therefore unchecked by C2 at all. The contract's "expected ≈47" is the enumerator's output,
  not the entry's pointer count.
- Note: `(psi.c:1538-1550)` is the pointer r24's own round-27 correction marks as mis-cited ("1538-1550 holds two
  full readers and a signature, not four readers", r24 line ~241). It is enumerated and requires a row; see F1 for
  the accepted `moved` row.

### F5 — counter-only floor "≥5 words" is not in the frozen contract and makes honest rows impossible for 14 pointers
- Contract C2 Target: "every quote ≤25 words, ≥8 distinct bytes, pairwise distinct". Counter line 137:
  `if not (5 <= wordcount(q) <= 25)`. The ≥5 floor is extra, and the quote must be one line (`\n`-joined hay),
  so a 5-word quote needs one line with ≥5 words inside the stated range.
- Pointers whose range has no single line with ≥5 words (honest `same` impossible; `moved` with in-range loc is
  impossible too): `psi.c:1268-1270, psi.c:1712, psi.c:1017, psi.c:1540, psi.c:1686, psi.c:1710-1721, psi.c:1268,
  psi.c:1269-1270, psi_types.h:41-49, psi.c:1717-1719, psi.c:1257-1258, psi.c:228-240, psi.c:1711-1719,
  psi.c:1596-1598` (14 of 47). For these, the only route to `C2=met` is an off-range `changed` row (variant A
  does exactly that for all 14). The floor therefore pushes the honest ledger into the lie shape.
- Contract/counter mismatch: report to L1; no fix applied.

### F6 — cross-line assembly is rejected (NEGATIVE, verified)
- The hay is `"\n".join(lines[lo-1:hi])` and ROW cannot carry `\n` in a quote, so a quote cannot straddle two copy
  lines. N1 and N2 above show `quote_missing`. A stitched text that is a substring elsewhere in the copy is only
  accepted when its loc range (any range for `changed`) covers that place; that is a far-quote case under F1.

### F7 — provenance and pins (weak arms, recorded)
- Provenance (`provenance_ok`) is a line-start regex for `source:`, `verified-at:`, `recheck:` in the first 2000
  bytes of the ledger; it does not look at values, dates, or whether the lines are in a fence or comment. The
  header of fixture B (3 lines) passes.
- The six sha pins prove the copies equal the bytes pinned inside the frozen counter. They do not prove that those
  bytes are the upstream v7.3 tag; the fetch log is not read by any arm. [INFERENCE: no network check was run.]

### F8 — committed C2 selftest receipt is a non-default-floor run (receipt defect)
- Default `--selftest` is red (`pass=9 fail=1`, rc=1, case `good` fails `pointer_floor:6<40`). The committed receipt
  equals the `--floor 1` run. The receipt records no command. The contract's "a red selftest blocks dispatch" holds
  for the default invocation.

### F9 — rows counted anywhere in the file (HIDE)
- `ROW.match(line.strip())` over all lines: rows inside `<!-- … -->` count (fixture C, rc=0). Rendered, the ledger
  shows no table. Not a counter-arithmetic bypass, but the rendered deliverable and the counted one diverge.

## Things that do NOT bypass (checked)
- Pins: any byte change to a copy fails `copy_pin` (selftest `tampered-copy` also).
- Duplicate anchors, orphans, missing rows: caught (`dup_anchor`, `rows_orphan`, `rows_missing`).
- Duplicate quotes: exact-string equality (`quote_dup`); distinct-by-substring quotes are accepted (not a bypass
  of the frozen arm, which says "pairwise distinct").
- Pipe `|` inside a quote is accepted by ROW (`[^`]*`); no effect on arms.
- Cross-line stitch: rejected (F6).

## Draft lesson lines (for L1; no counter or contract amendment proposed here)
- "C2 measures quote location, not status: a ledger can mark every pointer `changed` at an unrelated v7.3 span
  and meet the frozen predicate. The after-state is therefore not evidence of a recheck."
- "The SOURCES arm checks token presence on one line, not the opened-this-round date; one stuffed line meets all
  six copies."
- "The pointer enumerator captures only `file:N` heads; nine r24 citations (comma tails, bare-colon forms) are
  never required."
- "The ≥5-word quote floor is counter-only and makes 14 of 47 pointers unsatisfiable honestly."
- "The committed selftest receipt was produced with `--floor 1`; the default invocation is red."

## Confidence
- F1, F3, F4, F5, F8: high (exact rc and output captured above).
- F2, F7 pin scope: [INFERENCE] where stated.
- Tooling: none installed; no pacman; no mutating VCS; no fleet or sibling writes.

## Appendix A — accepted ledger (fixture B, exact bytes; accepted with App. B line, rc=0)

```
source: S090-S095 (v7.3 pinned copies, lie fixture)
verified-at: 2026-10-30
recheck: on-release

| anchor | status | loc | quote |
|---|---|---|---|
| psi.rst:60-65 | changed | psi.rst:1-188 | `PSI - Pressure Stall Information` |
| psi.c:342-360 | changed | psi.c:1-1725 | `* Pressure stall information for` |
| psi.c:1268-1270 | changed | psi_types.h:1-216 | `* For IO and CPU` |
| psi.c:1372-1373 | changed | cgroup-v2.rst:1-3581 | `This is the authoritative documentation` |
| psi.c:1379-1380 | changed | Kconfig:1-2368 | `This is used in unclear` |
| psi.c:1712 | changed | kernel-parameters.txt:1-8710 | `AGP	AGP (Accelerated Graphics Port)` |
| psi.c:1017 | changed | psi.rst:1-188 | `When CPU, memory or IO devices` |
| psi.c:1540 | changed | psi.c:1-1725 | `* Pressure stall information for CPU, memory` |
| psi.c:1686 | changed | psi_types.h:1-216 | `* For IO and CPU stalls the` |
| psi.rst:36-38 | changed | cgroup-v2.rst:1-3581 | `This is the authoritative documentation on` |
| psi.c:1710-1721 | changed | Kconfig:1-2368 | `is used in unclear ways:` |
| Kconfig:730-731 | changed | kernel-parameters.txt:1-8710 | `AGP	AGP (Accelerated Graphics Port) is` |
| psi.rst:40-43 | changed | psi.rst:1-188 | `When CPU, memory or IO devices are` |
| psi.c:1290-1296 | changed | psi.c:1-1725 | `* Pressure stall information for CPU, memory and` |
| psi.rst:45-56 | changed | psi_types.h:1-216 | `* For IO and CPU stalls the presence` |
| psi.rst:57-59 | changed | cgroup-v2.rst:1-3581 | `This is the authoritative documentation on the` |
| psi.c:1282-1288 | changed | Kconfig:1-2368 | `- Re-run Kconfig when the` |
| psi.c:1284-1288 | changed | kernel-parameters.txt:1-8710 | `AGP	AGP (Accelerated Graphics Port) is enabled.` |
| psi.c:160-164 | changed | psi.rst:1-188 | `When CPU, memory or IO devices are contended,` |
| psi.c:1268 | changed | psi.c:1-1725 | `Pressure stall information for CPU, memory` |
| psi.c:1269-1270 | changed | psi_types.h:1-216 | `For IO and CPU stalls the` |
| psi.c:600-602 | changed | cgroup-v2.rst:1-3581 | `This is the authoritative documentation on the design,` |
| psi.c:1273-1296 | changed | Kconfig:1-2368 | `- Re-run Kconfig when the compiler` |
| psi.c:1032-1042 | changed | kernel-parameters.txt:1-8710 | `AGP (Accelerated Graphics Port) is` |
| psi.c:1364-1367 | changed | psi.rst:1-188 | `CPU, memory or IO devices` |
| psi_types.h:41-49 | changed | psi.c:1-1725 | `Pressure stall information for CPU, memory and IO` |
| psi.c:1717-1719 | changed | psi_types.h:1-216 | `For IO and CPU stalls the presence of` |
| psi.c:1260-1263 | changed | cgroup-v2.rst:1-3581 | `is the authoritative documentation on` |
| psi.c:1257-1258 | changed | Kconfig:1-2368 | `- Re-run Kconfig when the compiler is updated` |
| psi.c:228-240 | changed | kernel-parameters.txt:1-8710 | `(Accelerated Graphics Port) is enabled.` |
| psi.c:149-158 | changed | psi.rst:1-188 | `CPU, memory or IO devices are` |
| psi.c:1553-1566 | changed | psi.c:1-1725 | `stall information for CPU, memory` |
| psi.c:1711-1719 | changed | psi_types.h:1-216 | `IO and CPU stalls the presence` |
| kernel-parameters.txt:5505-5507 | changed | cgroup-v2.rst:1-3581 | `is the authoritative documentation on the` |
| Kconfig:743-760 | changed | Kconfig:1-2368 | `Re-run Kconfig when the compiler` |
| psi.rst:67-88 | changed | kernel-parameters.txt:1-8710 | `ALSA	ALSA sound support is` |
| psi.rst:102-104 | changed | psi.rst:1-188 | `CPU, memory or IO devices are contended,` |
| psi.c:167 | changed | psi.c:1-1725 | `stall information for CPU, memory and` |
| psi.c:1596-1598 | changed | psi_types.h:1-216 | `IO and CPU stalls the presence of running/oncpu` |
| psi.rst:178-187 | changed | cgroup-v2.rst:1-3581 | `is the authoritative documentation on the design,` |
| cgroup-v2.rst:1066-1081 | changed | Kconfig:1-2368 | `Re-run Kconfig when the compiler is` |
| psi.c:408-410 | changed | kernel-parameters.txt:1-8710 | `ALSA	ALSA sound support is enabled.` |
| psi.rst:70-88 | changed | psi.rst:1-188 | `CPU, memory or IO devices are contended, workloads` |
| psi.c:845-857 | changed | psi.c:1-1725 | `stall information for CPU, memory and IO` |
| psi.c:551 | changed | psi_types.h:1-216 | `and CPU stalls the presence` |
| psi.c:1538-1550 | moved | psi.c:1538-1550 | `static int psi_io_show(struct seq_file *m, void` |
| cgroup-v2.rst:1066-1087 | moved | cgroup-v2.rst:1066-1087 | `A read-write single value file that allowed` |
```

(Tabs inside quotes are literal tab characters in the fixture, as in `AGP<TAB>AGP (Accelerated Graphics Port)`.)

## Appendix B — SOURCES.md line (single line, appended; satisfies all six rows_src checks)

```
| S999 | stuffed | corpus/evidence/sources-r61/psi.rst corpus/evidence/sources-r61/psi.c corpus/evidence/sources-r61/psi_types.h corpus/evidence/sources-r61/cgroup-v2.rst corpus/evidence/sources-r61/Kconfig corpus/evidence/sources-r61/kernel-parameters.txt | x | - | psi | a | b | mined | 2026-10-30 | on-release | psi-v73-recheck-r61.md |
```

## Appendix C — negative quotes (exact bytes; both absent from their copy)
- N2 in-range stitch (psi.c lines 1268|1269): `collect_percpu_times(group, PSI_AVGS, NULL); if (now >=`
- N1 stitch (psi.c lines 1267|1268): `now = sched_clock(); collect_percpu_times(group, PSI_AVGS, NULL);`
- psi.rst stitch (lines 37|38): `exported through the respective file in`
