# Round 44 lesson

author: L1 lane subagent (mori-r44, in-session hyaku round). Seats this lane
dispatched are still the lane, not a non-author reviewer.

Inherited: nothing. The lane checkout was clean at the entering tip
`1429c791db5891c484684feef893799909d2d6a8` (`jj-lane.sh state` →
`ahead=0 behind=0`, `git status --porcelain` empty, no `.ufo/waves/round-44/`
tree). No earlier attempt of this round had landed, so no inherited output was
reused or discarded.

## Gate

Opened 2026-10-25. One theme, one admitted entry (item 10).

- S471 — https://manpages.ubuntu.com/manpages/focal/ja/man5/proc.5.html —
  opened 2026-10-25 by this L1: HTTP 200, `text/html; charset=utf-8`, 376399
  bytes. Quote (節「/proc/[pid]/cmdline」): 「ただし、そのプロセスがゾンビプロセスの場合は、
  このファイルは空となる。つまり、このファイルを読み出しても一文字も返らない。」 (28
  non-space characters). State alphabet (節「/proc/[pid]/stat」):
  「Z ゾンビ (Zombie)」「X 死亡 (Dead) (Linux 2.6.0 以降)」. Grounds the zombie world
  and the `X` version qualifier. used-by
  `corpus/knowledge/pid-probe-conclusion-r44.md`. recheck `180d`. status mined.
- S472 — https://man.archlinux.org/man/proc.5.zh_TW — opened 2026-10-25 by this
  L1: HTTP 200 (`--http1.1`; a first attempt died at the TLS handshake),
  `text/html; charset=utf-8`, 61889 bytes. Quote (「cmdline」段): 「如果該程序已經被
  交換出記憶體, 或者該程序已經僵死, 那麼就沒有任何東西在該檔案裡，這時候對該檔案的讀操作將
  返回零個字元。」 (44 non-space characters). Also 「該檔案是否可見取決於該檔案是否已被
  交換出記憶體」 for `comm`, which S471 contradicts (「スワップアウトされているかどうか
  によらず、見ることができる。」). Translation of Linux 1.3.11-era man-pages (last
  Chinese update 2000-11-26) → tier B. used-by
  `corpus/knowledge/pid-probe-conclusion-r44.md`. recheck `180d`. status mined.

Admit: `probe-absent-vs-dead-r39.md` (theme: what a pid probe may conclude) —
re-grounded in-round on S471/S472 by this L1; the entry was rewritten to assert
only what the opened pages ground, and the campaign's "three worlds" framing is
recorded as superseded in `SCORECARD.md` (round-44 correction).

Reject (from the assimilation set, kept with reason and flip):
- `failed-scope-keeps-limit-r50.md` — recheck is `systemctl reset-failed` after
  creating a scope: host mutation, outside `PROVINCE.md` (read-only probes;
  detection and report). Flip: a read-only `MemoryMax` show of an already-failed
  scope, no `reset-failed`, no scope creation. Row S350 stays `rejected` (round
  43); not re-opened this round, no new row.
- `journal-reach-at-ceiling-r46.md` — grounds itself in a shokuknow `file://`
  note plus a kernel `MESSAGE` grep, neither admissible. Flip: the public
  `--vacuum-size=` sentence plus a committed read-only disk-usage receipt, no
  MESSAGE grep. Row S351 stays `rejected` (round 43); not re-opened.

Quarantine slice (register read-only, derived from the register's second table
because all 109 of its id cells are malformed — `S244\`` instead of `S244 |`):
S244, S262, S268 — all three carry the prose class "the cited source could not be
fetched". Verdicts (`w1/ScoutRegisterSlice.md`): S244 and S262 are **clean**
(the row's own companion URL serves the quote: arXiv:2403.18832 for S244, the
OpenAlex deposited abstract for S262); S268 is **unverifiable, not fabrication**
(every endpoint 418/202/0 B, no committed PDF, `mark_victim` absent from the
abstract). No row in the slice is fabrication-class, and none is appended this
round: the adopted entry cites neither.

Search log: proc(5) Japanese/Chinese translations (admitted S471, S472);
`failed-scope-keeps-limit` and `journal-reach-at-ceiling` re-checked and refused;
the campaign's absent-defect register slice (3 rows, verdicts above).

### Assimilation (item 10)

One theme, one entry, two rows. The package
`/home/vgpnk/Projects/shokuknow/merge/mori/` was read read-only; no campaign tool
was run there; no byte was written into it.

- Collision check before the append: registry 245 ids (after the two new rows) vs
  staged 136 ids → **2 collisions**, `S471` and `S472`
  (`.ufo/waves/round-44/assimilation/collisions`). The lane's ids stand
  (append-only, CORPUS.md rule 2) and the staged ids are **shadowed by document**:
  staged `S471` = gihyo.jp article 0061 (cgroup v2 memory controller),
  staged `S472` = gihyo.jp article 0056. The campaign's own ids for this round's
  two documents are `S490`/`S491` and were re-pointed **by document** (URL and
  anchor are the evidence; the id follows it) to lane `S471`/`S472`.
- Indented-row guard proven before the append
  (`assimilation/guard/`): a fixture with `| S001 |` and `  | S001 |` gives
  `col0-ids` = 1 id and `wide-ids` = 2, so the column-zero-only pattern misses the
  indented collision.
- Transformation before the append: the staged rows' `recheck` prose cells were
  normalized to a bare `180d` (the re-verify commands live in the entry's
  `recheck:` line and in this Gate); `used-by` lists exactly the admitted entry;
  `status` is `mined`; `opened` is 2026-10-25; the two `teaches` cells are <= 25
  words; neither row contains a literal or escaped `|` (`awk -F'|'` → 11 cells).
- Validate-before-append: **the frozen `count-c3.py` census arm is the defect
  here** (M3). `sources-census.sh --file` resolves `used-by` against
  `dirname(file)/..` (`scripts/sources-census.sh:499-503`), and the counter stages
  the registry at `$TMPDIR/c3-*/SOURCES.md`, so `dir` is `$TMPDIR` and every
  `used-by` path resolves nowhere → 279 `E11` findings, exit 1. The registry
  itself is clean: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin
  mori` → `exit 0`, 245 rows (`evidence/census-start.txt` has the 243-row start
  receipt; `after/c3-after.txt` the 245-row one). The after-measurement therefore
  runs the frozen counter with `TMPDIR=<lane>` so its census arm resolves against
  the measured tree, and that requirement is disclosed rather than patched into
  the frozen bytes.
- Post-append guard: `comm -12` registry-vs-staged gives the same 2 ids; the two
  adopted rows keep the lane ids.

### considerthese (item 10, one proposal)

`considerthese/2026-10-24.md` (operator-authored, read-only, not edited) —
"Reproduce headline numbers mechanically" (P4). Still unimplemented in general
before this round: `tools/mori-round41-calibration.py` is round-40-only and
`.ufo/waves/round-44/figures.tsv` was absent at the entering tip
(`w1/ScoutConsider.md` §1). Mined as **QUALITY 117**, whose check is this round's
C1 counter and whose rationale names the pointer. P3 ("watch repository growth
from scratch output") remains unimplemented and is routed to round 45; P1 and P2
are already criteria (115, 114) whose residual artifacts are absent.

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M1 | a wave item named a tool at the wrong root (the seat had to correct the argv) | `w1/ExecMisrootSweep.md` §2: the documented `python3 tools/mori-misroot-sweep.py …` exits 2 from the fleet root because the tool lives at `<lane>/tools/` | none before dispatch | the sweep ran from the lane cwd and returned `MORI_MISROOT_CLEAN`; the guard for round 45 is to resolve every path in a wave item against the checkout before dispatch (a seat catching it is luck, not a control) |
| M2 | the C1 predicate as frozen is reachable by a vacuous ledger | `w1/ExecJunkLedger.md` (12× `git diff @REV@ @REV@ \| wc -l` → `C1=met`), `w1/MutC1.md` attacks 1/2/4 (HEAD reads, `# @REV@` comment, 12 rows one id), `w1/CritC1Vacuity.md` (a) | none at freeze — the phase-4 "cheapest do-nothing control" rule was applied to the ledger's *presence*, not to its *content* | disclosed as the claim's limitation (QUALITY 117 "Not covered"); tightening routed to round 45 (revision-sensitivity arm, distinct ids/commands, no `WORK`, absent path ⇒ FAIL) |
| M3 | the C3 counter's census arm cannot resolve `used-by` (staged registry in `$TMPDIR`) | `count-c3.py:132-145` stages at `$TMPDIR/c3-*/SOURCES.md`; `sources-census.sh:499-503` takes `dirname(file)/..` → 279 E11, exit 1; `w1/RevEnteringBaseline.md` F-1, `w1/ScribeFrontierRow.md` finding 1 | the counter's own `--selftest` uses a fake census, so no arm can see it (CritSelftestHonesty class) | the after-measurement runs it with `TMPDIR=<lane>` (disclosed); round 45 must mirror the registry at `<repo>/corpus/SOURCES.md` or pass `--root`, and the registry row's entry cell must name the env requirement until then |
| M4 | a CJK quote greps to zero in the served HTML because the page entity-encodes it | this L1's first recheck attempts: `curl -fsSL <ja page> \| grep -c 'ゾンビ'` → 0 and `… \| grep -c '僵死'` → 0, while `html.unescape(...).count(...)` → 3 and 2 | none — no criterion required a recheck to be *demonstrated* before it was written | the entry's `recheck:` lines unescape before counting (QUALITY 116's family: a verdict must carry the probe that could have failed) |
| M5 | the gate auditor reads only the first standard-header table under `## Gates` | `w1/ExecGateInventory.md` §3: 11 of the 14 "unregistered" tools carry a complete 8-cell row in one of six secondary tables under `## RoundNN` headings | none before the audit | reported as the auditor's own limit (QUALITY 118 "Not covered"); the audit's `REGISTRY=unmet` for those tools is a reader defect, not a registration gap; routed to round 45 |
| M6 | the round's first README frontier row named the entry by a relative path and exceeded the counter's requirement | `w1/ScribeFrontierRow.md` finding 2 (`readme_row FAIL` on `knowledge/…`); this L1's `count-c3.py WORK` run showed the same FAIL | `count-c3.py` `readme_row` | the row now names `corpus/knowledge/pid-probe-conclusion-r44.md` verbatim and `readme_row` PASSes |
| M7 | a claim's ground sentence asserted a world its sources do not ground | `w1/ScoutSources490.md` §5 (only two worlds; the swap-out branch is 1.3.11-era and contradicted by the same desk's `comm` sentence) | the seat, after the contract was frozen | the contract's P-C3 sentence is left byte-unchanged; `SCORECARD.md` carries an append-only correction naming the superseded phrase, and the entry asserts the two grounded worlds plus the contradiction |
| M8 | the auditor's selftest arm named for "entry does not resolve" actually exercises the *unregistered* branch | `w1/RevVerdictMap.md` observation: the branch is reachable and correct when built by hand, but no arm covers it | none | routed to round 45 with the fixture that shows the branch works (so the fix is an arm, not a code change) |

M9 (appended after the wave): the entry's first text called S471 and S472 a clean
contradiction on swap-out visibility, but the two sentences concern **different
objects** — `stat`'s comm field (ja) versus the `comm` file (zh) — so it is a
divergence, not a contradiction, and neither page dates the retirement of the
swap-out branch. Evidence: `w1/ScribeEntryDraft.md` F6; fixed in the entry and in
the README map row. Captured by: none at authoring time; the seat read the
sections, this L1 had read the sentences.

M10 (appended after the wave): three more entry defects, all found by
`w1/CritAssimilationGate.md` after the entry had landed — (a) the Boundaries
section still said the entry "adds the state alphabet" while the Claim disclosed
it is already held; (b) the mm discriminator was asserted inside a receipt whose
method never read an `mm` indicator (a `/proc/<pid>/maps` reading was added; note
that procfs reports `st_size = 0` for both files, so a size-based check reads zero
for every pid); (c) the S170 negative in S472's `scope` cell is imprecise —
S170's source carries the swap-out sentence as a roff comment at `:15`. (a) and
(b) are fixed in the entry; (c) is recorded here because the S472 row is
append-only and is not rewritten. Captured by: none at authoring time.

M2 and M3 are the round's two load-bearing mistakes: both are instrument
properties discovered only by attack, and both are disclosed in the report rather
than patched into frozen bytes.

## Wave findings (the round's own seats — still the lane, not a reviewer)

One v1 wave, 32 seats, 12 attack roles (reviewer 5, critic 4,
mutation-tester 2, sentinel 1). Reports under `.ufo/waves/round-44/w1/`.

| seat | attack | verdict | what it establishes |
|---|---|---|---|
| `ExecJunkLedger` | the cheapest ledger that passes the floor | **SURVIVED** — 12 constant rows print `C1=met` | C1 measures ledger well-formedness, not informativeness (M2) |
| `MutC1` | HEAD reads, `# @REV@` comment, one-id rows, `head -c 64` truncation | 3 KILLED (empty/trailing output, floors, two integers), 3 **SURVIVED** | the grammar blocks lies about bytes, not vacuity about bytes (M2) |
| `CritC1Vacuity` | is a do-nothing state reachable, and is the class set a dimension | reachable (618-byte ledger) and the class set is a quota | `C1=met` and the round-43 slips can coexist at one rev: the witness fires because its asserted column was transcribed from prose |
| `MutRegistry` | duplicate rows, embedded basenames, absent entry paths, 9-cell rows | 4 KILLED, 2 **SURVIVED** (duplicate-row verdict flip; embedded-basename acceptance) | the auditor's row selection is weak under crafted input (QUALITY 118 "Not covered") |
| `ExecGateInventory` | the lane's whole gate inventory | 33 gate/probe tools: 18 PASS, 15 FAIL; 11 of the 15 are a reader defect | the standard is not met fleet-wide, and the auditor under-reads (M5) |
| `RevVerdictMap` | every documented failure class | all classes trigger; one exit-code gap | rev-parse sits outside the `try`, so a git timeout exits 1 with a traceback where `*_SETUP` exit 2 is documented (routed) |
| `CritSelftestHonesty` | is a `pass=` tally evidence the checks ran | **SURVIVED** — `-O` strips every `assert` and all four tallies still print; a failure-shaped tally scores `selftest_tally PASS`; a mutant that disables no check is recorded killed | a `pass=` line is printed, never asserted, so the tally is weaker evidence than it reads |
| `SentTools` | path handling, subprocess bounds, trust boundary | 3 HIGH, 5 MEDIUM, 3 LOW | `bash -c` ledger rows can write outside the repo, so `C1=met` is not a read-only claim; `GIT_*` is inherited by children; the C3 census default is a fleet file not in the lane; the registry write-scope cells are false as written |
| `ExecOffHostReplay` | replay from a scratch clone at another path | clone replays the four selftests and `count-c2` off-host; the instruments resolve their repo by walking up | QUALITY 115's practice holds for the round's own instruments |
| `ScoutSources490` | open both C3 pages | both GET 200; JA carries `Z`/`X`, zh_TW carries the swap-out disjunct; only two worlds grounded | M7, and the entry's boundaries |
| `RevStagedClaims` | which staged sentences hold | quotes accurate, conclusions not: the `comm` rule is a translation inversion; swap-out is a retired 2.3.26 roff comment; a nonexistent pid gives `ENOENT`; the real non-zombie empty-read class is mm-less kernel threads | the entry's world list, rewritten accordingly |
| `CritAssimilationGate` | is the entry in-province and new ground | in-province (detection and report, no remediation); the `Z` row and the zero-character read are **already held** | C3's novelty narrowed to the measured mm-less world (SCORECARD correction 2) |
| `ScoutRegisterSlice` | the campaign's absent-defect slice | 3 rows, none fabrication-class; S268 unverifiable | the quarantine verdicts above |
| `ScribeFrontierRow` | the README map row and its bounds | `readme_row` FAIL on a relative path (M6) | the row's shape is machine-checked |
| `RevEnteringBaseline` | re-derive the five before-values | all five match the contract; F-1 = M3 | the before-state is independently reproduced |
| `ExecC1STip` | the r43 C1S counter at the round-44 tip | `C1S=met`, 14 checks PASS, exit 0 | round-43 routed defect 5 is closed |
| `ScoutR43Wording` | the exact r43 wording the witness reproduces | "15" ×3 in the report, "34" ×2 in the report and ×1 in the lesson | the witness is transcribed from filed bytes |
| `ExecMisrootSweep` | fleet-root sweep | `MORI_MISROOT_CLEAN`, 0 candidates | no seat wrote to the fleet root |
| `ExecLedger` | the honest ledger | 20 rows reconcile at the freeze; two falsifiers forced corrections (a bare `git ls-tree` tree pathspec yields 1, and QUALITY.md was not stable) | a ledger row can be silently off by 31 |
| `ScoutConsider` | considerthese mining | P4 unimplemented in general; P3 unimplemented | QUALITY 117 |
| `RevScorecardPlanned` | the round's record-keeping obligations | C2's declared after-command lacks `--mutants-dir`; C2 was met at the freeze commit; the `Z ゾンビ` sweep is 3 files not 1; the round-43 SCORECARD cells carried no erratum | SCORECARD corrections 3-7 |
| `CritPredicates` | the three predicates as written | P-C1 narrow (constant-row ledger); P-C2 reword (audited set is caller-supplied, met at freeze); P-C3 reword (novelty falsified; axis attribution contradicted by the lane's own r31 ruling) | C3 re-attributed to depth; the rest routed |
| `SimpCounters` | dead weight in the instruments | 28 items, 0 removable before the after-measurement; `count-c2.py`'s auditor-absent branch raises `UnboundLocalError`; the `--mutants-dir` default has never existed | round-45 items |
| `ConnSiblings` | sibling overlap | no sibling holds a figure ledger or a gate-registry auditor; the closest patterns are kumitate's wave lifecycle and protocol's gate integrity | mori keeps the instruments local this round |
| `ScribeCriteria` | QUALITY 117-119 drafts | the draft's 118 check command omitted `--mutants-dir` and 119 cited an absent receipt | both corrected before the append |
| `ScribeLesson` | this lesson's draft | the draft's census mirror reached exit 0 with 245 rows; its three pending seat rows are filled from the returned reports | this file |
| `ScribeEntryDraft` | the C3 entry draft | ten quotes verified on entity-decoded pages; F6: the two pages' swap-out sentences concern different objects | M9 |
| `ScribeRowsDraft` | the two SOURCES rows | 11 cells each (`awk -F'|'` gives 13), no escaped pipe, `teaches` 20/21 words, census green on a mirror | rows S471/S472 as landed |
| `ExecCollisionGuard` | the id-collision guard | 0 collisions at the entering registry, 2 after the append; indented-row guard 1 vs 2; the staged block needs de-pipe and cadence fixes before any bulk append | the shadow map by document |

Wave-2 seats were not dispatched: the wave returned fewer than 32 *distinct*
attack items on landed bytes by the time the round had to land, so the residual
attack surface is enumerated as round-45 routing instead of padded seats (the
contract's "never pad" rule). Round total: 32 seats, one v1 wave.

## Resource runway observed this round

`/tmp` reached 100% (1.1 GiB free of 128 GiB, 167 GiB used, 33 812 entries) during
wave 1, reported first by a seat's own scratch pressure and measured read-only by
this L1 (`evidence/resource-runway.txt`). Detection and report only: mori names
the reading, souji proposes residue handling, the operator owns removal. The
round's own seats moved their scratch to `/var/tmp` rather than delete anything.
