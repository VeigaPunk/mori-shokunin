# Round 44 lesson (draft — the integration owner finalizes)

author: mori round-44 L1 lane, scribe seat `ScribeLesson`. Seats this lane
dispatches are still the lane. Everything below is either a command this seat
ran and quotes, or a named seat/evidence file it read; nothing is upgraded from
"reported" to "measured".

Inherited: entering tip `1429c791db5891c484684feef893799909d2d6a8`, whose
round-43 closure (non-author integrator, hyaku) is **Admit**. The freeze commit
`7cb59c6891d4f5d0266fe062565f094da835dc84` pins the contract, the three counters,
`tools/mori-gate-registry.py` and the fixtures by sha256, and records the four
selftest tallies (C1 6/0, C2 5/0, C3 6/0, registry 6/0) before the first data
seat (`.ufo/waves/round-44/evidence/freeze-r44.txt`). Round-43 routed defects 3,
4 and 5 are this round's C1, C2 and receipt work; items 1, 2 and 6 are durable
records or operator-side and are named, not fixed. The two round-43 count slips
still stood in the filed bytes at the entering tip; C1's witness reproduces
them and the working tree carries errata **appended after** those bytes
(`LOG.md`, `corpus/lessons/round-43.md`) — no filed byte is rewritten. The
campaign package `/home/vgpnk/Projects/shokuknow/merge/mori/` was read
read-only; no campaign tool was run there and no byte was written into it. The
round-43 lesson's M1–M5 stand as recorded; M1's fix was re-run at the tip
(`C1S=met`, exit 0, 14 `check` lines — `w1/ExecC1STip.md`).

## Gate

Opened 2026-10-25. Both pages were fetched by GET; the scout's headers record
HTTP 200, `text/html; charset=utf-8` (`w1/ScoutSources490.md` §1.1), and this
seat's own fetches returned the same sha256 values. CJK quotes are held to ≤25
CJK characters because whitespace word-counting does not apply.

- S471 — https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html —
  376399 B, sha256
  `f64b0cded10f755e6135f8d9d4aba8f5c769290128572f92faad1dc5a2c6364b`.
  Quote, 節「/proc/[pid]/cmdline」: 「ゾンビプロセスの場合は、このファイルは空となる」
  with the consequence 「このファイルを読み出しても一文字も返らない」; and 節
  「/proc/[pid]/stat」 state 欄: 「Z ゾンビ (Zombie)」「X 死亡 (Dead) (Linux 2.6.0 以降)」.
  Grounds the `Z`/`X` alphabet and the zombie empty-read rule. used-by
  `corpus/knowledge/pid-probe-conclusion-r44.md`. recheck `180d`. status mined.
- S472 — https://man.archlinux.org/man/proc.5.zh_TW — 61889 B, sha256
  `b8ede81db8d462b46f5312b392caab7c5fe8d125057ca6093c2d3152efba8be7`.
  Quote, 「cmdline」段: 「如果該程序已經被交換出記憶體, 或者該程序已經僵死」 and
  「這時候對該檔案的讀操作將返回零個字元」; the `comm` sentence
  「該檔案是否可見取決於該檔案是否已被交換出記憶體」; alphabet `;RSDZT`, no `X`.
  tier B — a translation of Linux 1.3.11-era man-pages (last Chinese update
  2000-11-26). used-by `corpus/knowledge/pid-probe-conclusion-r44.md`. recheck
  `180d`. status mined.

Admit: `pid-probe-conclusion-r44.md` on one theme — what a zero-character
`/proc/<pid>/cmdline` read is consistent with. Two source rows, one theme.

Reject: the staged entry's world "swapped out ⇒ empty `cmdline`, current".
Reason: S472 is a 1.3.11-era translation, and S471 states the opposite for the
same neighbouring field — 「実行形式がスワップアウトされているかどうかによらず、
見ることができる」 — while S471's `cmdline` section carries no swap-out clause at
all. Flip: the entry records the swap-out world as **retired, translation-only**,
and grounds two worlds (the pid never existed; the pid exists and is zombie or
`X` dead). Row S472 stays mined at tier B with the version caveat in its scope
cell. (`w1/ScoutSources490.md` §5, §6.1–6.2.)

Reject: the staged entry's recheck commands as written. Reason: both pages serve
CJK as numeric character references (`&#x…;`), so a literal grep returns 0 on
both — measured: `grep -c '僵死'` → 0 and `grep -c 'ゾンビプロセス'` → 0 on the
served bytes, against 2 and 1 after decoding. Flip: decode before counting; the
landed recheck is `html.unescape(sys.stdin.read()).count("ゾンビ")` → 3 and
`.count("僵死")` → 2, both re-run 2026-10-25.

S170 (`proc_pid_cmdline(5)`, man-pages 6.20) is **not** re-opened: the held
modern English row already carries the zombie/0-character rule, and the entry
cites it as held ground rather than re-asserting it.

Opened read-only by the quarantine seat and **not** written as lane rows: `S244`,
`S262`, `S268` — the campaign register's three mori rows. `S244` and `S262` are
clean (quote located in a fetchable source each row names); `S268` is
unverifiable, not fabrication; none is a C3 source (`w1/ScoutRegisterSlice.md`
§3–§4).

Search log: proc(5) ja `cmdline`/`stat` (admitted S471); proc(5) zh_TW
`cmdline`/`comm`/`stat` (admitted S472); swap-out cross-check (rejected as
current, retired); staged recheck reproduction (rejected as written, decoded
flip).

### Assimilation (item 10)

One theme, one entry: what a zero-character `/proc/<pid>/cmdline` read is
consistent with — `corpus/knowledge/pid-probe-conclusion-r44.md`. The package
`/home/vgpnk/Projects/shokuknow/merge/mori/` was read read-only; no campaign
tool was run there; no byte was written into it.

- Id lists. Lane: **243** ids at `7cb59c68` (max `S470`; gaps `S236–S240`,
  `S242–S261`, `S263–S346`, `S352–S469` were never allocated). Staged:
  **136** ids, contiguous `S471–S606`.
- Collision count. `comm -12` at the entering registry (243 ids) → **0**;
  neither `S471` nor `S472` was allocated there. At the live tree (245 rows) →
  **2**, ids `S471` and `S472` (`w1/ExecCollisionGuard.md` §3; this seat
  reproduced 243/136 and 0/2).
- Renumber map, by document and never by arithmetic: staged `S490` (Ubuntu ja
  proc(5)) → lane **S471**; staged `S491` (Arch zh_TW proc(5)) → lane **S472**.
  The staged block's own `S471`/`S472` (gihyo.jp 61 and 56) are shadowed and
  move: `S471→S473`, `S472→S474`, … `S489→S491`, with `S492–S606` identity
  (134 rows appended at `S473–S606`). The staged block carries 56 in-cell id
  references; under this map 0 change value, but the map must still be run over
  cell text.
- Transform before the append: the entry's `source:` lines renumbered
  `S490/S491 → S471/S472` (the counter's `entry_meta` now prints
  `sources S471,S472`); rows' `opened` `2026-10-23` → `2026-10-25` (the lane's
  own open); `used-by` → `corpus/knowledge/pid-probe-conclusion-r44.md`;
  `status` `mined`; `recheck` `180d`; tier A/B kept; scope/anchor/teaches
  rewritten to the two-world conclusion; recheck commands entity-decoded; no
  cell holds a literal or escaped `|`.
- Validate before the append: a scratch mirror (full `HEAD` tree + the append
  block inside the Registry table + the entry at its path) →
  `sources-census.sh validate --file …/corpus/SOURCES.md` **exit 0**, 19 W04
  warnings, 0 errors, **245 rows**. The same mirror with the two rows but no
  entry → `E11` on both rows, exit 1: the entry must exist before the append.
  The live working tree validates identically (exit 0, 19 W04, 0 errors, 245
  rows).
- Quarantine slice of the campaign's absent-defect register: mori's rows are
  `S244`, `S262`, `S268` (staged `S483`, `S501`, `S507`). `S244` and `S262` are
  clean (the quote is in a fetchable source the row itself names); `S268` is
  unverifiable, not fabrication; none is fabrication-class. Intersection with
  C3's `S471`/`S472`: zero (`w1/ScoutRegisterSlice.md` §3, §5).
- Post-append guard: both rows `mined` with `used-by` naming the entry, census
  245 rows, and the counter's `rows_present` PASS.

### considerthese (item 10, one proposal)

`considerthese/2026-10-24.md` (operator-authored, read-only, not edited) —
"Reproduce headline numbers mechanically" (`:24`) — mined as **QUALITY 117** in
the working tree, whose rationale cites that line; the instance is this round's
C1 ledger. P1 is already QUALITY 115 and P2 is QUALITY 114; P4 was the one with
only a round-specific instance (`tools/mori-round41-calibration.py`) before this
round.

Conflict recorded, not resolved here: `w1/ScoutConsider.md` holds **P3** ("Watch
repository growth from scratch output") to be the only wholly-unimplemented
proposal and proposed P3 for 117. P3 is indeed unimplemented — `grep -n growth
corpus/QUALITY.md` → no hit, no tool, and the proposal's own pointer has grown:
**225** tracked `.scratch/` files at `HEAD` (its note said 71), while the freeze
commit alone added 16 files / 2619 insertions. Which proposal the round claims
is the integration owner's call; pending command: `grep -n considerthese
corpus/QUALITY.md`.

## Mistakes

Only rows with an evidence pointer that exists are listed.

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | reported count wrong by one (round 43) | `.ufo/reports/round-43/mori.md` L45/L123 ("15 checks PASS", "15 PASS lines"); `git show 91cb221f:.ufo/waves/round-43/evidence/c1s-after.txt \| grep -cE '^check'` → 14; witness F03 asserted 15 observed 14 | round-43 closure routed defect 3; r44 C1 witness (`w1/ExecWitnessReceipt.md`) | erratum appended to `corpus/lessons/round-43.md`; F03 in the witness ledger |
| M2 | reported count wrong by 26 (round 43) | `git grep -l 'provider.rate_limit' 91cb221f -- .ufo/waves/round-43/logs \| wc -l` → 8; `git grep -l '429' … \| wc -l` → 39; witness F04 asserted 34 observed 8 | round-43 closure routed defect 3; r44 C1 witness | erratum appended to `LOG.md`; F04 in the witness ledger |
| M3 | counters shipped without the gate standard (round 43) | `evidence/witness-r43-gates.txt` → `REGISTRY=unmet` naming both round-43 counters as unregistered and without a selftest mode | round-43 closure routed defect 4; r44 C2 | `SKILL.md` rows L183–L186, `--selftest` on each counter, committed mutants |
| M4 | receipt revision ≠ verdict revision (round 43) | round-43 spotcheck §Routed defects item 5 (`dde525ea` vs "the landed tip"); tip run `C1S=met`, exit 0, 14 check lines | round-43 closure; `w1/ExecC1STip.md` | tip-run receipt names its revision; QUALITY 119 |
| M5 | a recheck command that cannot reproduce | `grep -c '僵死'` → 0 and `grep -c 'ゾンビプロセス'` → 0 on the served pages; decoded → 2 and 1 | this Gate | entity-decoded recheck (landed: `html.unescape(...).count(...)` → 3, 2) |
| M6 | a frozen check that no correct lane can pass | `count-c3.py WORK` → `census_ok FAIL (exit=1)` while `sources-census.sh validate --file corpus/SOURCES.md` → exit 0, 245 rows; the counter writes `SOURCES.md` to a temp dir and the census resolves every `used-by` against that dir's parent (`scripts/sources-census.sh:501`, `usedby_findings`) | this seat (the `--census` stub in the selftest cannot see it; `w1/SentTools.md` F3 is the same check's other face) | post-freeze defect: recorded here, routed to round 45, never patched in place |
| M7 | map row that does not name the entry the counter checks | `count-c3.py WORK` → `readme_row FAIL (no line names the entry)`; `corpus/README.md` says `knowledge/pid-probe-conclusion-r44.md`, the counter requires `corpus/knowledge/pid-probe-conclusion-r44.md` | this seat; `w1/ScribeFrontierRow.md` §5 X2 | respell the path in `corpus/README.md` |
| M8 | contract after-value contradicted by the round's own bytes | `git grep -l 'Z ゾンビ' 1429c791 -- corpus/ \| wc -l` → 0; `grep -rl 'Z ゾンビ' corpus/ \| wc -l` → 3 (`SOURCES.md`, `README.md`, the entry) — the contract says 1 | this seat | report and ledger assert the measured value at the landing tip, not 1 (pending: `git grep -l 'Z ゾンビ' <tip> -- corpus/ \| wc -l`); if the 60-word frontier row replaces the README prose the count can drop to 2 |
| M9 | declared after-command cannot reach the declared value | `count-c2.py WORK --counter …` (no option) → `mutant_kill FAIL (… mutant absent)` → `C2=unmet`; with `--mutants-dir .ufo/waves/round-44/fixtures/mutants` → `C2=met`, exit 0 | this seat | report names the met command with its `--mutants-dir`; the declaration's command is incomplete |
| M10 | predicate names more than the sources ground and the counter checks | P-C3's sentence "the three worlds …"; `w1/ScoutSources490.md` §5 (two worlds grounded, third absent); `count-c3.py` checks no world count | this Gate | entry states two worlds and the retired third; contract wording routed to round 45 |

## Wave findings (the round's own seats — still the lane, not a reviewer)

Placeholder: the wave was still running when this draft was written; the
integration owner finalizes this section from `.ufo/waves/round-44/w1/`.

| seat | attack / finding | verdict | what it establishes |
|---|---|---|---|
| `ExecWitnessReceipt` | round-43 figures against the frozen counter | `C1=unmet mismatches=2`, exit 1, naming F03 15/14 and F04 34/8 | the witness is the contract's declared one, not a shape rejection |
| `ExecLedger` | 20-row ledger (all five classes), sandbox rev `85fc3bca` | `C1=met mismatches=0` | a reconciliation ledger is reachable; it must be re-derived at the landing tip |
| `ExecJunkLedger` | 12 copies of `git diff @REV@ @REV@ \| wc -l` | `C1=met` | P-C1 scores arithmetic agreement, not informativeness |
| `MutC1` | trivial figures; rows reading HEAD/worktree/parent; 12 rows 1 id 1 command | **SURVIVED** (three shapes) | the grammar constrains the producer, not the revision |
| `CritC1Vacuity` | do-nothing lane; a ledger transcribed from the prose while the prose still says 15/34 | `C1=met` both times | P-C1 does not route routed-defect 3; it routes "ledger vs prose" |
| `ExecGateInventory` | 33 tools audited against 23 `## Gates` rows | 18 PASS, 15 FAIL (14 unregistered + 1 thin), `REGISTRY=unmet`; six auditor findings incl. a `--selftest` false positive on `mori-silence-cases.sh` | the lane's gate gap is wider than this round's four rows |
| `MutRegistry` | crafted registry rows | 4 **SURVIVED** (ghost suffix, prefix tool, dir-prefix, nine cells) | the auditor's selection and cell rules are weak under crafted input |
| `CritSelftestHonesty` | per-check mutation sweep of the four instruments | C1 `class_floor` and C2 `tool_selftest` mutations **survive**; all five C3 checks are caught; `exists_at()` forced True undetected | a tally is printed, not asserted |
| `SentTools` | path/subprocess/write-scope review | F1–F11; F3 the census program is uncommitted and outside the lane; F8 the declared write scope is false as written | the instruments' scope claims need tightening in round 45 |
| `SimpCounters` | dead weight in the four instruments | 28 items (3 unreachable, 1 vacuous, 10 duplication, 13 unarmed) | none removed before the measurements |
| `RevVerdictMap` | each named failure class against its documented verdict | named classes honest; findings F1–F6 (a git timeout exits 1 with a traceback, not the documented 2; a grammar-rejected ledger prints `commands_reconcile PASS` with zero rows scored) | the maps under-describe, they do not lie |
| `ExecC1STip` | C1S at the round-44 tip | `C1S=met`, exit 0, 14 check lines | routed defect 5 closed |
| `ExecCollisionGuard` | id collision and renumber | 0 pre-append, 2 post-append; 136-entry map | the map follows the document |
| `ScoutRegisterSlice` | quarantine slice | 3 rows, none fabrication-class, zero intersection with C3 | the slice does not gate C3 |
| `ExecMisrootSweep` | fleet-root untracked files | `MORI_MISROOT_CLEAN`, 0 candidates | no misroot attributable to this lane |
| `ScoutConsider` | the four proposals | P1/P2 criteria, P4 in flight, P3 unimplemented | the considerthese conflict above |
| `ScoutR43Wording` | round-43 verbatim sentences and hashes | "15 checks PASS", "15 PASS lines" located | the witness's authority |
| `ScoutSources490` | the two pages | sha256 and quotes as in this Gate | the Gate's quotes |
| `ScribeFrontierRow` | README row | 60-word draft; the relative path fails the counter | M7 |
| `ScribeCriteria` | QUALITY 117–119 | 117 ledger, 118 gate standard, 119 receipt revision | the round's criteria |

Current instrument verdicts measured by this seat on the working tree:
`count-c1.py WORK` → `ledger_present FAIL (absent)` → `C1=unmet` (no
`.ufo/waves/round-44/figures.tsv` yet); `count-c2.py WORK` → `C2=met` only with
`--mutants-dir .ufo/waves/round-44/fixtures/mutants` (M9);
`count-c3.py WORK` → `entry_present PASS`, `entry_meta PASS`, `rows_present
PASS`, `census_ok FAIL (exit=1)`, `readme_row FAIL` → `C3=unmet` (M6, M7).

Pending, with the command that settles each:

- C1 after — `python3 .ufo/waves/round-44/count-c1.py <landed tip>`, once the
  ledger is committed (draft in `w1/ExecLedger.md`).
- C2 after — `python3 .ufo/waves/round-44/count-c2.py <landed tip> --counter
  .ufo/waves/round-44/count-c1.py --counter .ufo/waves/round-44/count-c2.py
  --counter .ufo/waves/round-44/count-c3.py --mutants-dir
  .ufo/waves/round-44/fixtures/mutants`.
- C3 after — `python3 .ufo/waves/round-44/count-c3.py <landed tip> --entry
  corpus/knowledge/pid-probe-conclusion-r44.md --row S471 --row S472`, after the
  README respell (M7) and the census decision (M6).
- Ten seat reports not yet in `w1/`: `ScribeEntryDraft`, `ScribeRowsDraft`,
  `RevStagedClaims`, `CritAssimilationGate`, `RevLedgerVsReport`,
  `RevRegistryRows`, `ExecOffHostReplay`, `ConnSiblings`,
  `RevScorecardPlanned`, `CritPredicates`.
