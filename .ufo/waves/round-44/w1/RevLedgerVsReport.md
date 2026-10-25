# RevLedgerVsReport — does the proposed C1 ledger back the report's numbers?

Seat: `L1Mori44-4.RevLedgerVsReport` (reviewer, leaf — no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering tip `1429c791db5891c484684feef893799909d2d6a8`; freeze / lane HEAD at reading
`7cb59c6891d4f5d0266fe062565f094da835dc84`.

Draft reviewed: `.ufo/waves/round-44/w1/ExecLedger.md`, 365 lines, sha256
`e9e86a3d7766df9338a8bb7b16e7b9f9496b2424bf85c5f5081a427bf4eb1a27` (read 2026-10-25T05:28-03;
the seat was still running, so a later revision of the draft can differ).
Instrument: `.ufo/waves/round-44/count-c1.py`, sha256
`9477824d5eee45f47d49be52902f7bb0cd67a4d038e0ec7e79094c1e71999f83` — matches the
`evidence/freeze-r44.txt` pin.

**State of the object under review.** No `.ufo/waves/round-44/figures.tsv` exists in the lane or
in any commit; the 31 wave-1 reports are untracked; the round report is not written. The
integration worktree carries uncommitted corpus changes (`corpus/SOURCES.md`, `QUALITY.md`,
`README.md`, `knowledge/pid-probe-conclusion-r44.md`, `SCORECARD.md`, `LOG.md`). Everything below
about "the report's figures" is therefore derived from the report contract
(`/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-44.md` §4, §6), the round's SCORECARD
declaration (`SCORECARD.md:2394-2426`) and the committed/uncommitted artifacts — not from a
report that exists.

No file was edited except this one. No frozen byte, corpus file, SKILL.md, SCORECARD, LOG or
figures.tsv was written. Scratch ran under `/home/vgpnk/revledger-*` because `/tmp` was full
(100%, 392 KB free); the lane checkout was read-only. No installs.

---

## 1. Verdict in one paragraph

The draft is **honest but partial, and its green runs are not at a landed tip.** All 20 rows
reconcile at the freeze commit — I re-ran every command and got the asserted integer 20/20. But
12 rows are load-bearing for report sentences, 4 are proxies, and 4 are padding that no required
report section states (`F02`, `F05`, `F15`, `F16`). Seven cells are stale at the landed tip by the
draft's own admission (`F06`, `F07`, `F08`, `F09`, `F12`, `F13`, `F14`), and two of its landing
predictions are wrong by one commit (`F16`=29 and `F12`=74; the closure lesson lands *after* the
round tip — `F16` stays 28, `F12` is 73). The ledger cannot cover the report's before-values, the
wave shape, the census, the witness's 15/14/34/8/12/2, the other three selftest tallies, the gate
table total, the gate inventory or the c1s receipt. The C3 sweep figure the report must cite is
**3 files at the integration tip, not the contract's 1**. The draft's only executed `C1=met` runs
are at the freeze tree (where it reconciles the *before* values 243/116/53/0/6) and at fabricated
simulations; no landed-tip run exists. As specified, `C1=met` certifies ledger well-formedness and
arithmetic agreement at one revision — not that the report's numbers are reconciled.

---

## 2. What I ran (receipts)

### 2.1 Every draft row, at the freeze commit

I extracted the 20 rows from `ExecLedger.md:47-67` and ran each command exactly as `run_row`
does (`@REV@` → `7cb59c68`, `2>/dev/null | head -c 64`, cwd = lane):

```
F01 72=72  F02 10=10  F03 8=8   F04 39=39  F05 32=32
F06 0=0    F07 243=243 F08 192=192 F09 6=6  F10 3=3
F11 10=10  F12 72=72  F13 116=116 F14 53=53 F15 195=195
F16 28=28  F17 4=4    F18 3=3   F19 4=4    F20 6=6
```

**20/20 reconcile at `7cb59c68`.** The arithmetic half of the draft is sound.

### 2.2 The draft's green run is a before-state run

I rebuilt the freeze tree in scratch (`git archive 7cb59c68 corpus .ufo/waves SKILL.md`), added
the draft verbatim, and ran the counter:

```
$ python3 .ufo/waves/round-44/count-c1.py ff4e2ae2… --repo <scratch>
check ledger_present       PASS (1671 bytes)
check rows_parse           PASS (20 rows)
check row_floor            PASS (rows=20 min=12)
check class_floor          PASS (classes=checks,corpus,evidence,registry,wave min=4)
check commands_reconcile   PASS (all rows match)
rev=ff4e2ae22669b0c52151ebd0491374d809a39cc3
C1=met mismatches=0
rc=0
```

At that revision the ledger asserts `F07=243`, `F13=116`, `F14=53`, `F06=0`, `F09=6` — the
**before** values. The report's after-values are 245, 119, 54, N, N. So the draft's own
demonstrated `C1=met` does not back a single headline after-figure until the re-derivation in its
§5 is executed at a landed tip. ExecLedger's §1 (`rev=85fc3bca`) and §4 (`rev=55703287`,
`rev=729ed5ac`) are the same shape: freeze tree, or fabricated artifacts.

### 2.3 Witness and selftest (instrument sanity)

```
$ python3 .ufo/waves/round-44/count-c1.py 7cb59c68 --ledger .ufo/waves/round-44/fixtures/figures-r43.tsv
check commands_reconcile   FAIL (F03 asserted=15 observed=14; F04 asserted=34 observed=8)
C1=unmet mismatches=2        (exit 1)

$ python3 .ufo/waves/round-44/count-c1.py --selftest
… C1_SELFTEST pass=6 fail=0  (exit 0)
```

### 2.4 The after-state I could measure (integration worktree, uncommitted)

```
grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md   -> 245
grep -c '| mined |' corpus/SOURCES.md                          -> 194
grep -cE '^[0-9]+\. ' corpus/QUALITY.md                        -> 119
ls corpus/knowledge/*.md | wc -l                               -> 54
ls corpus/lessons/*.md | wc -l                                 -> 72   (round-44.md not yet written)
grep -c '^## Round-44' corpus/README.md                        -> 1
ls .ufo/waves/round-44/w1/*.md | wc -l                         -> 31   (32 seats; this report is the last)
ls .ufo/waves/round-44/evidence | wc -l                        -> 6    (no after receipts yet)
```

Census on the same bytes:

```
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
… 19 × W04 … mori ok …      EXIT=0
$ bash scripts/sources-census.sh census --file mori-shokunin/corpus/SOURCES.md
file rows 245 / file status.mined 194 / FLEET rows 245 / FLEET status.mined 194   EXIT=0
```

---

## 3. Row-by-row verdict

Legend: **L** load-bearing (a figure a required report section states), **P** proxy (counts a
required artifact but not the figure the report states), **D** decorative (no required section
states it), **S** stale at the landed tip as drafted.

| id | asserted | observed@freeze | class | what the command measures | verdict |
|---|---|---|---|---|---|
| F01 | 72 | 72 | wave | round-43 seat logs (`.ufo/waves/round-43/logs`) | **L** — the erratum's "8 of 72" |
| F02 | 10 | 10 | wave | round-43 w1 reports (4 `Exec*` + 6 `ResCrit*`) | **D** — round-43 wave record, not r44 |
| F03 | 8 | 8 | wave | round-43 logs carrying `provider.rate_limit` | **L** — routed defect 3 |
| F04 | 39 | 39 | wave | round-43 logs containing `429` | **L** — erratum's "39 logs" |
| F05 | 32 | 32 | wave | children of `.ufo/waves/` = round-13…round-44 | **D** — decoy: equals the seat count |
| F06 | 0 | 0 | wave | `.md` reports under `.ufo/waves/round-44/w1` | **L/S** — mislabeled "seat logs" |
| F07 | 243 | 243 | registry | `corpus/SOURCES.md` registry rows | **L/S** — after 245 |
| F08 | 192 | 192 | registry | rows whose status cell is `mined` | **P/S** — after 194; report states total |
| F09 | 6 | 6 | evidence | files under `.ufo/waves/round-44/evidence` | **L/S** — N unknown |
| F10 | 3 | 3 | evidence | `control-c{1,2,3}-donothing.txt` | **L** — three controls |
| F11 | 10 | 10 | evidence | sha256 pins in `freeze-r44.txt` | **L** — 10/10 pinned |
| F12 | 72 | 72 | corpus | lesson files | **P/S** — after 73; report states the lesson |
| F13 | 116 | 116 | corpus | numbered criteria in `QUALITY.md` | **L/S** — after 119 |
| F14 | 53 | 53 | corpus | knowledge `.md` files | **P/S** — after 54; report states "one entry" |
| F15 | 195 | 195 | corpus | files under `corpus/evidence` | **D** — no required section states it |
| F16 | 28 | 28 | corpus | `*verifier-spotcheck*` lessons | **D** — no required section states it |
| F17 | 4 | 4 | checks | `^| r44 ` rows in `SKILL.md`'s gate table | **L** — four r44 rows |
| F18 | 3 | 3 | checks | round-44 counters | **L** — three counters |
| F19 | 4 | 4 | checks | files under `.ufo/waves/round-44/fixtures` | **P** — witness + 3 mutants |
| F20 | 6 | 6 | checks | `count-c1.py` selftest arm calls | **L** — `pass=6` |

Counts: **L 12** (F01, F03, F04, F06, F07, F09, F10, F11, F13, F17, F18, F20), **P 4** (F08,
F12, F14, F19), **D 4** (F02, F05, F15, F16).

### 3.1 Padding, with the reason it is padding

- **F05 is the dangerous one.** It counts 32 *round directories* (`.ufo/waves/round-13` …
  `round-44`), not seats. The report contract requires "each wave's seat count, role mix"
  (`prompt:215-216`). Both are 32 today, so a reader could mistake F05 for the seat count; it
  would still be 32 if the wave had 31 or 33 seats, because the wave spec has 32 items
  (`python3 -c "json.load(open('.ufo/waves/round-44/w1-spec.json'))"` → 32; roles: executor 8,
  scribe 5, reviewer 5, scout 4, critic 4, mutation-tester 2, revenger 1, sentinel 1,
  simplifier 1, connector 1). No row counts seats or roles.
- **F15** counts 195 files under `corpus/evidence` (109 `.src`, 56 `.log`, 10 `.json`, …). No
  required section states a corpus-evidence file count.
- **F16** counts 28 verifier-spotcheck lessons. The report states that a closure lesson will be
  written, not how many exist.
- **F02** counts round-43's 10 reports. That is round-43's wave record; round-44's report states
  its own wave.

The draft's own sentence "every row a count the round's report will cite"
(`ExecLedger.md:15`) is therefore false for 4 of 20 rows.

### 3.2 Rows whose asserted value is wrong, stale or mislabeled

1. **F06 is mislabeled and is a false zero.** The draft's table calls it "round-44 wave-1 seat
   logs" (`ExecLedger.md:101`), but the command counts `*.md` **reports**
   (`.ufo/waves/round-44/w1`), not logs. At the freeze and entering tips the `w1` subtree does
   not exist, and `git ls-tree -r … | grep '\.md$' | wc -l` prints `0` with **rc 0** — a false
   zero, not "zero reports". The draft's §8.3 justification ("`F05` independently proves the
   `.ufo/waves/` tree exists") does not prove the `round-44/w1` subtree exists. If the ledger is
   filed before the reports land, F06 passes as 0 while the report claims N reports. The report's
   routed-defect-3 sentence is about *seat logs* (round-43's 72 `.log` files); F06 cannot back it.
2. **Seven cells are stale at the landed tip as drafted**: F06 0→N, F07 243→245, F08 192→194,
   F09 6→N, F12 72→73, F13 116→119, F14 53→54. The draft says so (§4) and gives a re-derivation
   recipe (§5); the defect is only if the recipe is not executed before filing.
3. **Two landing predictions are wrong by one commit.** The draft says "`245 / 194 / 54 / 119 /
   29 / 74` are the arithmetic consequences" (`ExecLedger.md:212`). `F16`=29 and `F12`=74 assume
   the round-44 closure spotcheck lesson lands with the round. It does not: round-43's closure
   lesson `corpus/lessons/round-43-verifier-spotcheck.md` landed at `1429c791`, one commit after
   the round-43 lane tip `91cb221f` (`git log --oneline -3 1429c791` → `1429c791` →
   `91cb221f`; `git show --stat 1429c791` adds only that lesson). At the round-44 landed tip
   `F16` stays 28 and `F12` is 73. The recipe re-derives, but the prediction table and the
   arithmetic sentence are wrong and should not be quoted in the report.
4. **F05 is not the seat count** (see §3.1). If the report writes "32 seats" beside F05, the row
   does not back it.

---

## 4. Figures the report must cite that no row covers

Grounded in the report contract (`prompt:104-118` required sections; `prompt:215-216` wave
record) and the round's own SCORECARD declaration (`SCORECARD.md:2410`). "No row" means the
draft has no row whose command yields that figure at the measured tip.

| figure the report must state | value at the integration tip | command I ran | row? |
|---|---|---|---|
| SOURCES rows **before** | 243 | `git show 1429c791:corpus/SOURCES.md \| grep -cE …` | **no** — F07 yields 245 at tip |
| criteria **before** | 116 | same regex on `1429c791` | **no** — F13 yields 119 |
| knowledge entries **before** | 53 | `git ls-tree -r 1429c791 corpus/knowledge` | **no** — F14 yields 54 |
| lessons **before** | 72 | `git ls-tree -r 1429c791 corpus/lessons` | **no** — F12 yields 73 |
| C3 sweep before → after | 0 → **3** | `git grep -l --untracked 'Z ゾンビ' -- corpus/` | **no**, and the contract says 1 |
| rows added by tier | 2 (S471 A, S472 B) | `grep -cE '^\| S47[12] '` | **no** |
| rows touched old→new | 0 | — | **no** |
| census rows before → after | 243 → 245 | `sources-census.sh` / `census --file` | **no** — F07 is the registry, not the census |
| census exit codes / W04 | 0 / 0, 19 W04 | `sources-census.sh validate …` | **no** |
| README frontier row | 1 (`## Round-44`) | `grep -c '^## Round-44' corpus/README.md` | **no** |
| knowledge entry delta | 1 | `ls corpus/knowledge/pid-probe-conclusion-r44.md` | **no** — F14 is the total |
| QUALITY criteria added | 3 (117–119) | `grep -cE '^[0-9]+\. '` 116→119 | **partial** — only 119 |
| lesson mistakes | M1..Mn (lesson not yet written) | — | **no** |
| wave seat count | 32 | `grep -c '"role"' w1-spec.json` | **no** — F05 is round dirs |
| role mix | 8/5/5/4/4/2/1/1/1/1 | same spec | **no** |
| reports returned | 31 at reading, N at landing | `ls w1/*.md \| wc -l` | **F06 only if pinned at the final tip** |
| dead seats | unknown at reading | seat roster/logs | **no** |
| round total | 32 | spec | **no** |
| witness fixture rows | 12 | `grep -c '^F' fixtures/figures-r43.tsv` | **partial** — F19 counts 4 fixture *files* |
| witness asserted/observed | 15→14, 34→8 | counter over the fixture | **no** — ledger F03/F04 assert 8/39, not 15/34/14 |
| witness mismatches | 2 | `C1=unmet mismatches=2` | **no** |
| selftest tallies | 6 / 5 / 6 / 6 | four `--selftest` runs; `freeze-r44.txt` | **partial** — F20 covers c1's 6 arms only |
| gate table rows total | 23 | `SKILL.md` `## Gates` | **no** — F17 counts the 4 r44 rows |
| gate inventory | 33 tools, 18 PASS, 15 FAIL | `ExecGateInventory.md` | **no** |
| c1s tip receipt | 14 check lines, `C1S=met`, exit 0 | `ExecC1STip.md` | **no** |
| C1 ledger rows/classes | 20 / 5 | the counter's own output | **no** — no self-row |

Two of these deserve emphasis.

**The C3 sweep is 3 files, not 1.** Contract P-C3 says "After: the same sweep at the landed tip →
1 file". At the integration tip the token `Z ゾンビ` appears in three corpus files:

```
$ git grep -l --untracked 'Z ゾンビ' -- corpus/
corpus/README.md
corpus/SOURCES.md
corpus/knowledge/pid-probe-conclusion-r44.md
→ 3
```

`corpus/README.md:631` quotes `Z ゾンビ (Zombie)` in the Round-44 coverage row;
`corpus/SOURCES.md` S471 quotes it in `teaches`; the entry quotes it in `source:`. If the report
repeats the contract's "1 file", it is false; if it reports 3, the frozen contract's after-value
is falsified and belongs in the lesson (not a patch). No ledger row covers the sweep either way.

**The witness numbers are outside the ledger.** The report's routed-defect-3 sentence is
"15 checks observed 14; 34 seat logs observed 8" (`ScoutR43Wording.md`, `ExecWitnessReceipt.md`).
The ledger asserts 8 (F03) and 39 (F04) and 72 (F01); it has no row for 15, 14 or 34. The witness
is evidenced by running the fixture through the counter (`C1=unmet mismatches=2`), not by the
ledger.

---

## 5. Rev identity, drift, and the fallback spine

### 5.1 The draft's recipe is mechanically right; the ordering is the risk

The draft's §5 order — land all wave artifacts (A), re-derive, commit the ledger alone (B), run
the counter at B — is the only order that both keeps the ledger filed once and lets the counter
read it at the measured rev. But every row that counts wave files is pinned to B. I demonstrated
the drift in scratch: a re-derived 20-row ledger was `C1=met` at B, then one late seat report
was committed as C:

```
$ python3 .ufo/waves/round-44/count-c1.py B --repo <scratch>
check commands_reconcile   PASS (all rows match)     → C1=met mismatches=0
$ python3 .ufo/waves/round-44/count-c1.py C --repo <scratch>
check commands_reconcile   FAIL (F06 asserted=17 observed=18)
→ C1=unmet mismatches=1
```

This is the QUALITY 119 shape the round is answering (receipt rev vs verdict rev). At the time of
this review 31 of 32 seats had filed; **this report is itself the 32nd `*.md` and will move F06
by +1.** If the ledger is committed before the last seat, `C1=met` at the final tip is false. The
report must name the exact `rev=` line the counter printed and that rev must be the lane tip it
cites; otherwise the claim is "C1=met at B" while the report says "at the landed tip".

### 5.2 The fallback spine cannot support a conformant report

The draft's §6 spine is 12 rows `F01 F02 F03 F04 F05 F10 F11 F15 F17 F18 F19 F20` — no registry
row, no `corpus/knowledge` or `corpus/lessons` row. The draft itself says "use it only if … and
then do not cite those numbers" (`ExecLedger.md:259`). But the report contract **requires**
`Sources & frontier` with "`SOURCES.md` rows before→after with the counting command, rows added
by tier" (`prompt:111-112`). Dropping F07/F14 makes that section unciteable. The spine is
therefore not a conformant fallback for this round; the full ledger must be pinned at the final
tip.

---

## 6. The grammar does not enforce "re-derived at the measured revision"

The counter checks that `@REV@` is *present* in the command text (`count-c1.py:100`), not that the
command consumes it. Two consequences, both demonstrated in scratch:

1. **A HEAD-reading row passes at a different measured rev.** In a scratch repo with `data.txt`
   = 3 lines at measured rev B, one row `git show HEAD:data.txt | grep -c x # @REV@` asserted 4
   (true only at the later commit C). At B the counter printed:

   ```
   check commands_reconcile   PASS (all rows match)
   rev=<B>                    → C1=met mismatches=0
   ```

   The measured revision's own value is 3; the row never read B.
2. **A hard-coded old revision passes.** A row `git show <A>:data.txt | grep -c x # @REV@`
   asserted 3 at measured rev B (whose value is 4); it passed because `@REV@` sits in a comment.

So `C1=met` does **not** prove that any row was re-derived at the measured revision. It proves
that each row's *effective* read (whatever rev it actually names) equals the asserted integer.
This is the same family as ExecJunkLedger's "12 tautologies" and MutC1's attack #2 (SURVIVED),
but it is sharper: the report's own phrase is "re-derived at the measured revision"
(`SCORECARD.md:2410`), and the instrument cannot see the difference.

---

## 7. Does `C1=met` mean what the report says it means?

The SCORECARD/contract wording is "a committed figure ledger reconciles the round's reported
counts … re-derived at the measured revision" (`SCORECARD.md:2410`; `contract.md:23-28`).

**What `C1=met` certifies** (from the code and my runs):

1. `.ufo/waves/round-44/figures.tsv` exists at the measured rev and parses into ≥12 four-cell
   rows whose ids, classes and command grammar pass `parse_ledger`.
2. The rows span ≥4 distinct class strings (the string need not match what the command reads).
3. For each row, the row's own pipeline prints the asserted integer at the measured rev.

**What it does not certify:**

1. That the rows are the report's figures. There is no linkage from a row to a report sentence;
   4 of the draft's 20 rows are decorative (§3.1).
2. That every report figure is covered. The uncovered list in §4 is most of the report's numeric
   assertions, including every before-value and the whole wave-shape record.
3. That the measured rev is the landed tip the report cites (§5.1).
4. That each row actually reads `@REV@` (§6).
5. That the figures are non-trivial (ExecJunkLedger: `C1=met` on 12 copies of `git diff @REV@
   @REV@ | wc -l`; QUALITY 117's own "Not covered" cell says exactly this, `QUALITY.md:943-956`).
6. That the report's prose equals the ledger's numbers — the counter never reads the report. A
   row may assert 245 while the report says 250 and `C1=met` still holds.

**Verdict.** If the report writes "C1=met — the round's reported counts are reconciled", that is
**false as a universal**. If it writes "the ledger's 20 figures reconcile at `<rev>`; the
remaining report figures are cited with their own commands and are outside the ledger", that is
true **only if** (a) the seven rev-sensitive cells are re-derived at the final tip, (b) the ledger
is the last lane commit, and (c) the report names the counter's `rev=` line. QUALITY 117 already
records the informativeness limit; this review adds the coverage, rev-identity and
`@REV@`-use limits. The honest report sentence is narrower than the claim's title.

---

## 8. Residual risk and verification gaps

- **No landed tip and no ledger exist.** Every after-value in §2.4 is read from the integration
  worktree (uncommitted), not from a commit. `F06` and `F09` are unknown until the seats and the
  L1 file. The draft is live (sha256 may change after this reading).
- **The report is unwritten.** The figure list in §4 is derived from the report contract and the
  integration state; a report that omits some of those sections would shrink the gap, but
  `Sources & frontier` and `Before → after measurements` are required.
- **The C3 claim is separately blocked** by `RevEnteringBaseline.md` finding F-1 (`count-c3.py`'s
  `census_ok` stages the registry under `/tmp`, so `used-by` resolves against `/tmp` and exits 1).
  That is a C3 instrument defect, not a C1 one; it does not change this review's C1 findings, but
  it means a "C3=met" sentence is not reachable as frozen.
- **The ledger's own row/class count is not asserted by a row.** The counter prints `rows=20
  classes=5`; if the report states that, no row backs it (a self-row would).
- **I did not verify the report's final prose** (it does not exist) and did not re-run the
  draft's sandbox revisions (`85fc3bca`, `55703287`, `729ed5ac`) — I reproduced the freeze-tree
  case at `ff4e2ae2` and the drift/hole cases independently.

---

## 9. Routed recommendations (no edits made)

1. **File the ledger last, and name the printed rev.** Commit all reports, evidence, corpus and
   lesson changes first; re-derive F06–F16; commit `figures.tsv` alone; run the counter at that
   commit; quote its `rev=` line in the report. Do not file the draft's freeze values.
2. **Add rows only for report figures the draft misses**: seat count and role mix (spec), rows
   added by tier (2), README frontier row (1), census rows/exit/W04, witness check lines and
   mismatch count, the other three selftest tallies, gate table total (23), c1s check lines (14),
   and the ledger's own row/class count. Do not add more proxies.
3. **Drop or relabel the four decorative rows**: F02, F05, F15, F16. In particular, do not let
   F05 stand beside a "32 seats" sentence.
4. **Relabel F06** as wave-1 seat **reports**, not logs; if the report must cite seat **logs**,
   there is no round-44 log tree at the tip and the row cannot exist.
5. **Correct the landing predictions**: at the round-44 landed tip `F16` = 28 and `F12` = 73 (the
   closure lesson lands after the tip, as round-43's did at `1429c791`). Do not quote
   "29 / 74".
6. **State the coverage limit in the report**: the ledger reconciles the landed-state figures it
   carries; the before-values are cited at `1429c791` with their own commands; the C3 sweep is 3
   files (or the contract sentence is recorded as falsified in the lesson, never patched).
7. **Round 45 instrument tightening** (frozen bytes are not amended this round): a
   revision-sensitivity arm (each row's value must differ at a second revision, or be declared a
   constant), rejection of rows whose effective read is `HEAD`/the working tree, and a
   report-linkage manifest (row id → report anchor) — the only way "reconciles every reported
   count" becomes machine-checkable.

Report: `.ufo/waves/round-44/w1/RevLedgerVsReport.md`
