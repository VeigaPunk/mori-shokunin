# Round 52 lesson

Entering tip `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d` (round-51 closure); freeze
`d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2` (contract `.ufo/waves/round-52/contract.md`, both counters with
selftests, the C1 data applier and control builder, eight C1 control receipts, census-start, the sweep, the five
v7.2 source copies); data `8524904adb25e44f24d9f25aac7eae909625c18c`; wave spec `075436b1346ca659afb8be7a46f0e67e4170aa83`.
L1 MoriR52, attempt 1. Claims: C1 calibration — the self-assessment agrees with the fleet record, its instruments
and its own pointers, K4 taken beyond SHONEN to the living pins of QUALITY.md and README.md (`count-c1.py`, four
arms); C2 depth — what CommitLimit and Committed_AS are at kernel v7.2 (`corpus/knowledge/overcommit-commit-limit-r52.md`,
S497–S501; `count-c2.py`, whose entailment arm now needs two non-author ENTAILMENT voters per row). One v2 wave `w1`
(68 seats) ran after the data commit, as the contract froze.

## Gate

### New SOURCES rows (each opened this round; rule 1)

Five rows, all opened 2026-10-26, appended after S496, 11 cells each, status `mined`, recheck `on-release`,
`used-by corpus/knowledge/overcommit-commit-limit-r52.md`. The documents were copied into
`corpus/evidence/sources-r52/` at 2026-10-26T20:45 -03 and pinned by sha256 in
`.ufo/waves/round-52/evidence/freeze-sha256.txt` and in `count-c2.py` COPIES; `corpus/SOURCES.md` gains five
lines and loses none between `4f266ef2` and `8524904a` (no earlier row edited).

| id | URL / locator | accessed | ≤25-word located quote | decision |
|---|---|---|---|---|
| S497 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/mm/overcommit-accounting.rst — copy `overcommit-accounting.rst.v7.2` (sha256 `767ab881…4927f`) | 2026-10-26 | "The total address space commit for the system is not permitted to exceed swap + a configurable amount (default is 50%) of physical RAM." (24 words, `:20-22`) | admit, mined, tier A docs |
| S498 | https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/sysctl/vm.rst — copy `vm.rst.v7.2` (sha256 `bf8ca026…f8c1ce`) | 2026-10-26 | "When this flag is 0, the kernel compares the userspace memory request size against total memory plus swap and rejects obvious overcommits." (22 words, `:841-842`) | admit, mined, tier A docs |
| S499 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/util.c — copy `util.c.v7.2` (sha256 `e702754c…3ebe7c`) | 2026-10-26 | "if (percpu_counter_read_positive(&vm_committed_as) < allowed) return 0;" (6 words, `:994-995`) | admit, mined, tier A code |
| S500 | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/mman.h — copy `mman.h.v7.2` (sha256 `d7bf787c…16b058`) | 2026-10-26 | "static inline void vm_acct_memory(long pages) { percpu_counter_add_batch(&vm_committed_as, pages, vm_committed_as_batch); }" (9 words, `:76-79`) | admit, mined, tier A code |
| S501 | https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/mmap.c — copy `mmap.c.v7.2` (sha256 `449b8583…1c4545`) | 2026-10-26 | "We honor MAP_NORESERVE if allowed to overcommit */ if (sysctl_overcommit_memory != OVERCOMMIT_NEVER) vm_flags \|= VM_NORESERVE;" (13 words, `:551-553`) | admit, mined, tier A code |
| — | https://www.kernel.org/doc/html/latest/mm/overcommit-accounting.html (rendered docs, `latest`) | 2026-10-26 | the page header reads "The Linux Kernel 7.3.0" (HTTP 200, 13558 bytes, sha256 `aa436419…e4fd97`) | **reject**: `latest` moves with each release (it renders 7.3.0 today, not the v7.2 bytes the entry pins), so a quote located there today proves nothing about v7.2 tomorrow; the raw tag copy (S497) carries the same text. Flip: a release-pinned rendered URL (`/doc/html/v7.2/…`) would be admissible as a second locator for S497, not as a new row |

The claim table these rows feed holds 28 rows (S497 7, S498 6, S499 9, S500 2, S501 4), so all five sources are
drawn on and no row cites an id this Gate does not carry.

### Assimilation (addendum §10) — none this round

Package `/home/vgpnk/Projects/shokuknow/merge/mori/` read only; no campaign tool run. It holds no staged entry or
row on overcommit (`.ufo/waves/round-52/evidence/sweep-overcommit.txt`: `CommitLimit 0`, `Committed_AS 0`,
`overcommit 0` files). The lane sweep at `4f266ef2` finds 0 files for each of thirteen terms (CommitLimit,
Committed_AS, overcommit_memory, overcommit_ratio, overcommit_kbytes, vm_commit_limit, __vm_enough_memory,
vm_committed_as, user_reserve_kbytes, admin_reserve_kbytes, MAP_NORESERVE, OVERCOMMIT_NEVER,
overcommit-accounting). The frontier ground is chosen on the lowest axis (depth), not by assimilation.


### Assimilation (addendum §10) — none this round (wave re-check)

The wave's `w1/Mo52ConnSiblings.md` re-ran the read-only sweeps: `merge/mori/` has 0 files on overcommit; sibling
lanes hold no CommitLimit/Committed_AS/overcommit rows (only `tsukuroi` adjoins via OS-state triage). No §10
cap is spent.

### Spot-check

- Census `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`: start rc 0, 23 W04
  (`evidence/census-start.txt`); end rc 0 (`evidence/census-end.txt`). Rows: 269 → 274 (S497–S501, all tier A,
  mined, opened 2026-10-26, used-by the entry; `git diff --numstat 4f266ef2 8524904a -- corpus/SOURCES.md` → `5 0`).
- Entailment arm (run at the landed tip): `python3 .ufo/waves/round-52/count-c2.py <tip>` → `C2=met claims=28
  located=28 … entailed=28 dissent=0` (`evidence/c2-at-landed.txt`); `C2_SELFTEST pass=45 fail=0`.
- The two ENTAILMENT dissent/replacement rows: row 3 (`93b4fe285dc7`) replaced by `3c2512af8468`
  (Ent01's text), voted entailed by Ent02/Ent03/Ent04; rows 27/28 replaced by `10ac5a250ac2`/`1cadeed9914b`
  (the literal SZ_128K/SZ_8K caps), voted entailed by Ent10/Ent11/Ent12. Old hashes have no surviving votes; the
  votes were appended to the voters' own reports (unfenced lines).
- Sources: all five URLs re-fetched live during the wave — HTTP 200, sha256 equal to the frozen copies 5/5, and
  all 28 quotes occur in the live bytes (`w1/Mo52ExecSourceRefetch.md`); tag v7.2 resolves to commit
  `8d3ae592` (annotated tag `237a1c39`).

## Mistakes

- M1: a living check pinned at one round's tally and never superseded (QUALITY 112 / README round-39 rows).
  Evidence: `evidence/control-c1-do-nothing.txt` (three living mismatches). Captured-by: none until C1 arm (C);
  fix: QUALITY 141/142 + README `## Round-52 corrections`, shown able to fail by the do-nothing control and
  `control-c1-delete-stale-pins.txt`.
- M2: a scorecard pointer named `:1771` for a pair that lives at `:1781` (round-28 `5 → 6`), and the frozen data
  applier's `axes()` prefix match also rewrote six history rows outside `## Axes` (witness bytes; the landed data
  does not). Evidence: `evidence/m2-history-rows.txt` (`HISTORY_ROWS changed=6` under `--applier`, `changed=0`
  between revisions). Captured-by: none (the counter's locator arm covers the Axes rows and SHONEN boxes only);
  fix: the applier now targets the Axes table (landing), and QUALITY 142 pins the quoted-string rule.
- M3: the wave spec's first validation refused `items[39].role "labrat"` (not a swarm role). Evidence:
  `evidence/w1-validate-refused.txt`. Captured-by: the validator itself; fix: copy-on-change wrapper
  `build-w1-spec-amend.py`.
- M4: a frozen file edited in place with no successor record (round-40 `conform.py` `5025b966…` → `7f5174d5…`,
  round-51 D-e). Evidence: `w1/Mo52RevenRound40Conform.md`, `w1/Mo52ExecWritersConform.md`. Captured-by: none
  (no QUALITY criterion forbids it yet); fix: round-53 successor-freeze design (routed defect 8) and a QUALITY
  criterion candidate in `w1/Mo52ScoutMistakeSweep.md`.
- M5: the round-51 entailment arm took one vote, parsed fenced lines and accepted any `.md` under w1/
  (`w1/Mo52MutC2Arm.md`, `w1/Mo52MutC2Entry.md`). Captured-by: QUALITY 143; fix: P-C2 arm (two non-author voters,
  unfenced, frozen voter list), shown able to fail by `evidence/c2-at-data.txt` and the selftest arms.

## Round-51 closure routed defects (§5) — dispositions

1 counter self-test → both counters ship `--selftest` (`C1_SELFTEST pass=42 fail=0`, `C2_SELFTEST pass=45 fail=0`).
2 entailment hardening → P-C2 arm (≥2 distinct non-author ENTAILMENT voters; unfenced; VOTERS list; REPLACE authorship).
3 round-51 C1 counter survivors → the counter is frozen; wave mutation found M4/M8 survive (`w1/Mo52MutC1Arms.md`); routed.
4 successor calibration counter and K4 → C1 (this round).
5 S493 locators and famzah attribution → `corpus/lessons/round-51-erratum.md` (landed).
6 no in-place edits of frozen files → none edited this round; the wrapper/amendment and the applier's Axes-only
  match avoid new rewrites.
7 literal receipt commands → every round-52 receipt records its literal command line (v). `evidence/sweep-overcommit.txt`
  opens with prose (F3, LOW) — recorded.
8 remaining in-lane writers → inventoried (`w1/Mo52ExecWritersConform.md`, `w1/Mo52ExecWritersCounters.md`);
  successor-freeze design routed to round 53.

## Wave w1 — integrated findings

- ENTAILMENT votes: 28/28 rows have ≥2 voters; row 3 had two overclaims, rows 27/28 were reworded to the literal
  constants; all replacement rows re-voted (see Spot-check).
- C1: controls replay identically (`w1/Mo52ExecC1Controls.md`); the do-nothing and all skip-work controls stay
  unmet; witness met. Named survivor mutants M4/M8 and the junk critic's three `met`-without-measuring classes
  are limits for round 53; `lane_writes` is a quiescent-tree instrument.
- C2: sources/quote refetch all green; counter arm limits (one file per voter assumption; REPLACE-only authorship
  signal) recorded; the host read confirms the formula on this host (precision note: integer division truncation;
  hugetlb branch not exercisable here).
- No-harm: RevNoHarm reports no harmed axis; all six Axes scores unchanged; the only in-place data edits this
  round are the S497/S499 anchor corrections (old → new, logged above in the Gate table), the row-3/27/28
  replacements (new hashes, re-voted) and the entry prose/anchor fixes named in `w1/Mo52ExecProseLines.md` and
  `w1/Mo52CritC2Prose.md`.
- Misroots: none at the fleet root (`w1/Mo52ExecMisrootSweep.md`: fleet root clean). Residue: `.ufo/waves/round-39/scratch/mori-conform-selftest-*` transient dirs created by frozen-instrument runs (the README :728 pin now uses a hermetic wrapper); removed at landing.

## Round shape

One v2 wave `w1` (68 seats), policy v2, validated rc 0 after the copy-on-change amend (role count: reviewer 12,
critic 12, executor 21, mutation-tester 4, connector 2, sentinel 3, revenger 2, scribe 9, scout 2, simplifier 1;
flash-eligible 36/68, attack 28/68). Dead seats: 0. Residual calls: 0 (replacement votes were appended in place
by the seeded voters). Round total: 68.
