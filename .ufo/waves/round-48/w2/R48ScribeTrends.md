# R48ScribeTrends — round 48 trend verdicts (draft for the L1 report)

Seat: R48ScribeTrends. Lane: mori-shokunin. Leaf seat, no subagents dispatched. Read-only against the
lane: no tracked file edited, no git/jj mutation, scratch under `.scratch/r48w2-R48ScribeTrends/`. This
report is the only file I wrote.

**Attacked:** whether the three trend verdicts of round 48 (`expansion`, `quality`, `discernment`) are
supportable from the landed bytes at `e4dfff32d4f97c7ef250e9a7538fa75d4f284492`, the lesson's `## Gate`,
`corpus/knowledge/quota-observability-r48.md`, the wave-1 corpus and the round-47 non-author closure — and
what would make each verdict `harmed`.

**Verdict: BREAKS at the landed tip — class ADMISSION-BAR (one claim row the page contradicts; a false
provenance locator in the entry header and in `corpus/SOURCES.md:258`) plus one RECORD defect (two of the
three recorded grounds for the `quota-id-mapping-files-r41.md` reject do not reproduce on the package
bytes).** Expansion and quality must not be filed `improved`/`unchanged` at this tip; both flip on the named
corrections in §6, and nothing else in the round blocks them. Discernment HOLDS at `unchanged`: the outside
spot-check of this round's gate is not on record.

Definitions used verbatim from `LEARNING.md` §*The three trends* (lines 31–37) and
`templates/round-prompt.md:116`.

## 1. Verdict table

| trend | verdict at `e4dfff32` | verdict once §6 corrections land | what makes it `harmed` |
|---|---|---|---|
| **expansion** | **harmed** (one of 15 claim rows fails the reviewer bar the round wrote in QUALITY 128; false locator in the entry header and `SOURCES.md:258`) | **improved** | an admitted entry fails the bar it was admitted under — the case here (row 5, §3.1); or a new row is shown not `mined`/not opened 2026-10-25 (all six verified as claimed); or a closure rules the FR2 map pointer at `README.md:342` already "held" ground, which would make this round `unchanged`, not improved |
| **quality** | **harmed** (a claim row of the new entry is contradicted by its own page and its provenance cell is wrong, and at this tip neither is marked in the entry — marked only in wave-2 reports) | **unchanged** | an entry found false or stale and left unmarked; also harmed if a copy drifts and its recheck is not re-run (the Aliyun page is not byte-stable — a byte-identity recheck there is the wrong test, disclosed in the entry) |
| **discernment** | **unchanged** (pending; the round-47 closure's agree/disagree record is round 47's) | **improved** iff the non-author closure agrees with this round's gate on ≥1 admit **and** ≥1 reject | a closure disagreement left unlearned; a QUALITY criterion with no lesson behind it (125–128 all cite round-48 lesson rows); or the r41 reject shipping with its two non-reproducing grounds uncorrected (§7.2, §7.3) |

Trajectory from the round-47 closure §4 (`corpus/lessons/round-47-verifier-spotcheck.md`): r47 was
expansion `improved`, quality `unchanged`, discernment `improved`. Round 48 keeps the same expansion work
shape but lands a defective row, so it cannot inherit `improved` without the repair.

## 2. Expansion

Observables (each with the command I ran):

- SOURCES rows 251 → 257, six appended, no row edited in place:
  `git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` → `251` at `e5dbac05`,
  `257` at `e4dfff32`. `git diff e5dbac05 e4dfff32 -- corpus/SOURCES.md` is `+6` lines, 0 deletions; all
  six (S479–S484, `SOURCES.md:258-263`) carry `mined`, `2026-10-25`, a cadence (`180d` / `on-release`) and
  `corpus/knowledge/quota-observability-r48.md` in `used-by` (re-derived by parsing all six rows to 11 cells).
- Admitted entries 57 → 58: `git ls-tree -r --name-only <rev> -- corpus/knowledge/ | wc -l` → `57` → `58`;
  `git diff --stat` over `corpus/knowledge` is one added file (+93), zero modifications.
- Coverage map: `corpus/README.md` +20 lines — block at `:657`, row at `:667`, dated FR2 frontier note at
  `:672` (append-only; the FR2 row at `:342` is not rewritten).
- Capabilities admitted to `SCORECARD.md` (`:2610`, `:2611`, first-working round 48). I ran both selftests
  myself: `count-c1.py --selftest` → `C1_SELFTEST pass=34 fail=0`, rc 0;
  `tools/mori-unlanded-check.py --selftest` → `UNLANDED_SELFTEST pass=13 fail=0`, rc 0.

Ground check (is it uncovered?): the map's FR2 row before this round (`README.md:342`) pointed at
`knowledge/audit-r11.md:218-222`, whose text is a *non-claim* ("No closure is claimed for … quota
observability"), and five entries mention quota at entry level
(`git grep -l -i quota e5dbac05 -- corpus/knowledge/` → `audit-r11.md`, `observability-surfaces-r2.md`,
`oom-evidence-loss-r38.md`, `oom-victim-selection-r27.md`, `seat-terminal-status-r17.md`) — the symptom
and a provider-API token, not the filesystem quota reporting/error surface. I judge the ground genuinely
new: the map held a limit, not the state and its vocabulary.

**Why `harmed` and not `improved`:** the admitted entry carries row 5, which asserts a fact its own page
falsifies (§3.1), and a locator that names the wrong section in both the entry header and the registry row
(§3.4). Under the definition, an admitted entry that fails the bar it was admitted under makes expansion
`harmed` — and `LEARNING.md` forbids filing `expansion: improved` with `quality: harmed` as if it were an
improvement (a trade is reported as a trade).

## 3. The entry, row by row — what the reviewers found, and what I re-derived

Two independent wave-2 seats read the same entry: `w2/R48RevEntryXfs.md` (S479 rows: 6 HOLDS, row X5
OVERCLAIM), `w2/R48RevEntryQuotactl.md` (S480: 4 HOLDS), `w2/R48RevEntryErrnoAliyun.md` (S481/S482: HOLDS,
and the S482 quotes are rendered page text, not JSON-only), `w2/R48CritEntryClaims.md` (all 15 rows plus
prose: row 5 BREAKS, row 10 BREAK-lite, row 3 PARTIAL, four prose defects),
`w2/R48ScoutEntryContext.md` (all 15 quotes located; `quot` under §ADMINISTRATOR COMMANDS).

I re-derived the two findings my verdict rests on, from the committed copy, with the counter's own
normalisation:

### 3.1 Row 5 (entry line 30) — the page contradicts it

Claim cell: `Limits are never enforced on the superuser or on group and project ID zero, so a root-owned
workload cannot hit a quota.` Quote: `limits are never enforced on the superuser (nor are they enforced for
group and project ID zero)`.

My reads of `corpus/evidence/sources-r48/xfs_quota.8.html` (tags stripped, entities decoded, whitespace
collapsed):

- offset `9294` — item 8: the exemption is scoped to **ids** (uid 0, gid 0, project id 0);
- offset `16420` — §DIRECTORY TREE QUOTA: "new files created in the tree will automatically be accounted to
  the tree based on their project identifier";
- offset `18010` — §EXAMPLES: `# xfs_quota -x -c 'limit -p bhard=1g logfiles' /var`.

A root-owned write into a project-quota'd tree is charged to that tree's nonzero project id, whose hard
limit is enforced — so the consequence clause is false as stated, on the page's own three sentences. The
entry's Boundaries section scopes the exemption by *filesystem*, not by id, so it does not rescue the row.

### 3.2 Row 3 (line 28) and row 10 (line 35) — unmarked inference, and the mechanism the page supplies

`w2/R48CritEntryClaims.md` §3.2/§3.3 report row 10 as narrowing a two-sentence `ESRCH` gloss to "quotas are
not turned on" and hardening it in §Probe shape ("never as zero"), and row 3's second clause as an
unmarked inference with the page's §Default Quotas mechanism missing. I read the same page sentences myself
— §Default Quotas at offset `6144` ("These limits are stored in and displayed as ID 0's limits, although
they do not actually limit ID 0"), the `ESRCH` gloss in §ERRORS — so the sentences exist as cited; the
*judgment* that the claims exceed them is the critic's, and I did not re-derive it independently.

### 3.3 Prose defects (seat-reported, source text present)

Unsourced Solaris sentence, `S480` cited for "its reporting tools are not [common]", unsourced cost claim
"a syscall read per id is cheap" (`w2/R48CritEntryClaims.md` §5.1–§5.3). The first is checkable as
unsourced: `grep -cE 'Solaris|errno=49' corpus/SOURCES.md` → 0 (exit 1), i.e. no lane row carries it.

### 3.4 False locator — I verified this independently

The entry's first `source:` line and `corpus/SOURCES.md:258` both place `quot` in `§USER COMMANDS`. My own
normalised-offset scan of the copy: `USER COMMANDS top` 6245, `ADMINISTRATOR COMMANDS top` 9790, the `quot`
paragraph 14748, `DIRECTORY TREE QUOTA top` 15676 — `quot` sits in **§ADMINISTRATOR COMMANDS**. The quote
still locates (so C2 stays `met`), which is the blind spot: the counter checks the words, not the locator
(contract §C2 named limit).

## 4. Quality

- No entry was re-verified, deepened or superseded: `git diff e5dbac05 e4dfff32 -- corpus/knowledge` is one
  added file, 0 modifications; no `verified-at` moved; SOURCES changed-in-place: none (lesson Gate says the
  same, and the diff agrees).
- Source-level re-verification did happen and held: S478 re-opened with a browser User-Agent —
  `w1/ExecS478Recheck.md` §2–§3: HTTP 200, 2,357,114 B, sha256 `1603404d…`, page count 14. That is a
  source recheck, not an entry re-verification.
- The one new entry's copies are dated 2026-10-25 and three of the four are byte-identical to the fetched
  pages (`cmp` in the lesson Gate); the Aliyun page is not byte-stable and the entry says so.

**Verdict `unchanged` is not supportable at this tip** because the new entry is found false in one row and
mislocated in its provenance, and at this tip the entry itself marks neither (the findings live in wave-2
reports only). That is the definition's harmed clause. Once the corrections are in the entry (append-only
claim-cell repair + locator fix), quality is `unchanged`: nothing was superseded and nothing stale
re-verified.

## 5. Discernment

Gate decisions on record (`corpus/lessons/round-48.md` §Gate, each with a reason):

- **admits:** six rows S479–S484 (`mined`, opened 2026-10-25) and one entry;
- **rejects:** staged `quota-id-mapping-files-r41.md`, `quota-path-listing-r42.md`,
  `quota-counter-freshness-r39.md`, `quota-id-to-path-r40.md`, `alarm-latency-model-r39.md`; Solaris
  `errno=49` stays rejected; the RHEL 9 Japanese PDF is classified `unreachable` at the freeze and not
  adopted;
- **collisions:** registry 251 ids vs staged 136 → 8 (`S471`–`S478`), renumbered by document (I re-derived
  both halves: rows `S471`–`S606` in `SOURCES.append.md` = 136, and the lane holds all eight of
  `S471`–`S478` at `corpus/SOURCES.md:250-257`);
- **quarantine slice:** S244 / S262 / S268 hand-checked, all PRESENT, none appended.

In-lane falsification worked: `w1/CritEntryRisk.md` built a fixture on which the frozen counter prints
`C2=met` for six claim/quote pairs a reader rejects, and that became QUALITY 128 with a reviewer checklist;
`w1/CritC1Counter.md` F1's harness leak became QUALITY 126's second arm; the wave-2 reviewer pass is what
found §3.1 and §3.4. `w2/R48RevQuality.md` re-ran the checks behind criteria 125–128 and reports all four
HOLD.

**Verdict `unchanged`, pending.** The definition's `improved` arm needs the *outside* spot-check to agree on
admits and rejects; the lesson says "Round-48 gate decisions are awaiting this round's non-author closure"
and offers a sample (admit S479–S482 and the rewritten entry; reject staged `quota-id-mapping-files-r41.md`).
A subagent the lane dispatched is still the lane (`LEARNING.md` §*Discernment is checked from outside*), so
neither the wave-2 reviewers nor this seat can move it. Note for the closure: two of the three recorded
grounds for the r41 reject do not reproduce (§7.2, §7.3) — the reject verdict still stands on RHEL 7
currency, but the recorded reason needs the correction or the closure will find it first.

## 6. Corrections that flip expansion → `improved` and quality → `unchanged` (drafts; the L1 owns the edit)

1. **Entry line 30** — drop the consequence clause, keep the id-scoped sentence:
   `| Limits are never enforced on the superuser or on group and project ID zero. | S479 | \`limits are never
   enforced on the superuser (nor are they enforced for group and project ID zero)\` |`
   If the workload sentence is wanted it must be `[INFERENCE]`-marked and say what it assumes (writes
   charged to uid 0, no project quota on the target tree) — `w2/R48CritEntryClaims.md` §3.1.
2. **Entry header line 1 and `corpus/SOURCES.md:258`** — `§USER COMMANDS quot` → `§ADMINISTRATOR COMMANDS
   quot`.
3. **Rows 3 and 10** — mark the inference clauses (or drop them), and name the default-quota store in row 3
   (`w2/R48CritEntryClaims.md` §3.2–§3.3).
4. **Prose** — mark or drop the Solaris sentence and the "cheap" cost claim; cite S479 or drop `(S480)` for
   the reporting-tools sentence (`w2/R48CritEntryClaims.md` §5.1–§5.3).
5. **Lesson Gate, r41 line** — see §7.2/§7.3 below: strike the 12-cell and S260/S261 grounds or replace them
   with the grounds that do reproduce.

### 6.1 Where the corrections must land

Append-only: a new commit correcting the entry's claim cells/locator and the S479 locator cell, a LOG note,
and (for 5) an append-only erratum line in the lesson. The round's report may then say `expansion: improved`,
`quality: unchanged`, `discernment: unchanged (pending)`.

## 7. Conflicts for the canonical judge (verbatim, unresolved by me)

1. **Empty C1 receipt vs SCORECARD's promise.**
   `wc -c .ufo/waves/round-48/evidence/after-c1-at-e4dfff32.txt` → `0`; `git status` → the file is untracked.
   `SCORECARD.md:2594` and `:2595` both end their "After" cell with "measured at the landed tip, appended
   below"; nothing is appended below in the round-48 block, and only the C2 receipt carries a measurement
   (`after-c2-at-e4dfff32.txt`, 152 B, `C2=met claims=15 located=15 …`). Not a claim failure: one seat
   re-ran the C1 counter — `w2/R48RevQuality.md` §126 reports
   `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12`, rc 0 at `e4dfff32` — and two more
   re-ran C2 (`w2/R48RevC2Counter.md`, `w2/R48RevEntryQuotactl.md` §0). **I re-ran it myself**:
   `TMPDIR=.scratch/r48w2-R48ScribeTrends python3 .ufo/waves/round-48/count-c1.py --tool
   tools/mori-pin-check.py --rev e4dfff32… --scratch …/r48w2-R48ScribeTrends/c1 --jobs 6` →
   `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32…`, rc 0, 695 s wall
   (J1–J8 `got=unmet` rc 1, H1–H4 and `real` `got=met` rc 0). That observation does not repair the record:
   the receipt file the round points at is still empty and untracked, and the round's own after-measurement
   must be committed, not supplied by a seat's scratch run.
2. **Lesson Gate, r41 reject ground (a):** recorded as "rows S502–S505 carry an unescaped `|` in the recheck
   cell (12 cells, not 11: the used-by value is displaced, `w1/ScoutStagedQuota.md` §4)". Observed on
   `SOURCES.append.md` (sha256 `4f69b2df…`, mtime 2026-10-24 23:33, i.e. unchanged since before the scout
   read): the pipe is **escaped** (`… pdftotext -enc UTF-8 g.pdf - \| grep -c …`); the counter's own
   `split_cells` (`count-c2.py:49-56`, `re.split(r"(?<!\\)\|", s)`) yields **11 cells** and cell 10 is
   `corpus/knowledge/quota-id-mapping-files-r41.md`; a naive `split('|')` yields 12 — the scout's count.
   Command: importing `split_cells` from the frozen counter → `counter_cells= 11 naive_cells= 12` for each of
   the four rows.
3. **Lesson Gate, r41 reject ground (b):** recorded as "cite `S260/S261` rows this lane does not have".
   Observed: neither the r41 entry nor rows S502–S505 contain `S260`/`S261`
   (`grep -n "260\|261" quota-id-mapping-files-r41.md` → no output; `awk 'NR>=38&&NR<=41' SOURCES.append.md |
   grep -o "S26[01]"` → no output). Those references are in `quota-path-listing-r42.md:45-49`, i.e. the r42
   reject. The r41 reject's ground (c) (RHEL 7 currency) does reproduce: S502/S503 URLs are RHEL 7 PDFs.
4. **Page count of the round-47 closure's S478 record:** `corpus/lessons/round-47-verifier-spotcheck.md` §3
   says "sha256 `1603404d…6add2`, 4 pages"; `w1/ExecS478Recheck.md` §3 says `Pages: 14` with the same sha256
   and the same byte size (2,357,114). The same bytes cannot carry two page counts; the measured figure is
   14. Round 48's lesson records 14 and calls the 4 the round-47 mistake.
5. **Reading guard, not a conflict:** the six pairs P1–P6 in `w1/CritEntryRisk.md` are synthetic attack
   claims on a temp fixture, not rows of the landed entry. They must not be read as entry defects; the
   landed rows are the ones reviewed in §3.
6. **Landing state at write time:** `tools/mori-unlanded-check.py --repo … --round 48` →
   `UNLANDED=dirty round=48 paths=23`, rc 1 (14 wave-2 reports on disk at that run plus this one, the
   wave-2 dispatch files, and the two after-receipts are untracked). They must be committed before the
   report is filed (round-47 routed defect 1 / lesson M1). Observed, not a defect: untracked `.scratch/c1-*`
   and `.scratch/pin-check-*` directories at the repo root from wave-2 tool runs.

## 8. UNVERIFIED (by me)

- The claim verdicts themselves (C1 `met`, C2 `met`): other seats own them. I observed `C1=met` in my own
  re-run and in `w2/R48RevQuality.md` §126, and `C2=met` in the committed receipt and in two seats' re-runs;
  I did not score either predicate.
- Rows 3 and 10's entailment judgments (§3.2) — sentences verified present, the judgment is the critic's.
- The six new rows' live URLs: I did not re-fetch. I verified their `mined` / `2026-10-25` / `used-by`
  cells and the frozen copy digests only through the seats' reports and the lesson Gate.
- The absence of an earlier FR2 admitted entry rests on the map row + `git grep -l -i quota` at `e5dbac05`;
  I did not read all five matching entries in full.
- Axis scores: not my scope; I score nothing, and the closure rules.

## 9. Evidence log

Read: `LEARNING.md` (trend table), `templates/round-prompt.md:100-125`, `contract.md`, `v3-spec.md`,
`corpus/lessons/round-48.md`, `corpus/lessons/round-47-verifier-spotcheck.md`,
`corpus/knowledge/quota-observability-r48.md`, `corpus/README.md:655-676`, `corpus/QUALITY.md:1050-1088`,
`SCORECARD.md:2585-2612`, `LOG.md:2689-2724`, w1 `CritEntryRisk.md`, `RevAssimPlan.md`,
`ScoutStagedQuota.md` §4–§5, `ExecS478Recheck.md`, `CritC1Counter.md`, `CritC2Counter.md`; w2
`R48RevEntryXfs.md`, `R48RevEntryQuotactl.md`, `R48RevEntryErrnoAliyun.md`, `R48CritEntryClaims.md`,
`R48RevQuality.md`, `R48RevC2Counter.md`, `R48ScoutEntryContext.md`.

Ran (all read-only; `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48ScribeTrends`
unless noted):

- `git show <rev>:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` → 251 / 257, rc 0.
- `git ls-tree -r --name-only <rev> -- corpus/knowledge/ | wc -l` → 57 / 58, rc 0.
- `git diff --stat e5dbac05 e4dfff32 -- corpus/knowledge corpus/README.md corpus/QUALITY.md PROVINCE.md
  SCORECARD.md LOG.md corpus/SOURCES.md` → 6 files, 221 insertions, 0 deletions (PROVINCE.md absent), rc 0.
- `git grep -l -i quota e5dbac05 -- corpus/knowledge/` → 5 files, rc 0.
- `python3 .ufo/waves/round-48/count-c1.py --selftest` → `C1_SELFTEST pass=34 fail=0`, rc 0.
- `python3 .ufo/waves/round-48/count-c1.py --tool tools/mori-pin-check.py --rev
  e4dfff32d4f97c7ef250e9a7538fa75d4f284492 --scratch …/r48w2-R48ScribeTrends/c1 --jobs 6` →
  `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32…`, rc 0, 695 s.
- `python3 tools/mori-unlanded-check.py --selftest` → `UNLANDED_SELFTEST pass=13 fail=0`, rc 0;
  `… --repo /home/vgpnk/Projects/shokunin/mori-shokunin --round 48` → `UNLANDED=dirty round=48 paths=23`,
  rc 1.
- Python normalise+offset probes on `corpus/evidence/sources-r48/xfs_quota.8.html` → item 8 at 9294,
  §Default Quotas 6144, §DIRECTORY TREE QUOTA 16420, `limit -p bhard=1g` 18010, section headings
  6245/9790/15676, `quot` paragraph 14748.
- Frozen `count-c2.py` `split_cells` imported and applied to `SOURCES.append.md` rows 38–41 →
  `counter_cells=11 naive_cells=12`, used-by cell intact; `sha256sum SOURCES.append.md` → `4f69b2df…`.
- `grep -cE '^ {0,3}\| *S26[01] *\|' corpus/SOURCES.md` → `0`; `grep -n S233 corpus/SOURCES.md` → the gihyo
  cgroup article at `:239`.
- `wc -c .ufo/waves/round-48/evidence/after-c1-at-e4dfff32.txt` → `0`; `after-c2-at-e4dfff32.txt` → 152.

Tooling: nothing installed or upgraded; pacman untouched (paused host-wide); operator RULES.md read, no
install needed.

Report: .ufo/waves/round-48/w2/R48ScribeTrends.md
