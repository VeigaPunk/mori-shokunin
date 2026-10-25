# RevLedgerVsReport — does the C1 ledger back the report's numbers?

Seat: `L1Mori44-4.RevLedgerVsReport` (reviewer, leaf — no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering tip `1429c791db5891c484684feef893799909d2d6a8`; freeze `7cb59c68…`;
**landed ledger commit `5157cdda41ca711da280a85e7d3ec13da6ec85d3`**; lane tip at this reading
`5102022a3978e167eaf34dbaecad68ae320a5fbe`.

Objects reviewed:

- **The landed ledger** `.ufo/waves/round-44/figures.tsv` at `5157cdda`, sha256
  `21fe80dd24bc0e310063aa9c11fc4be4b08e5451e2c9d2ccc802564caf7ace2b` — 16 rows, 5 classes.
  Byte-identical at `5102022a`.
- **The proposal** `.ufo/waves/round-44/w1/ExecLedger.md`, 365 lines, sha256
  `e9e86a3d7766df9338a8bb7b16e7b9f9496b2424bf85c5f5081a427bf4eb1a27` — 20 rows. The landed
  ledger is not this draft; it drops eight draft rows and adds seven of its own.
- Instrument `.ufo/waves/round-44/count-c1.py`, sha256
  `9477824d5eee45f47d49be52902f7bb0cd67a4d038e0ec7e79094c1e71999f83` (matches the freeze pin).

This version supersedes the 402-line version carried in `5102022a`; that version reviewed only
ExecLedger's proposal because the landed ledger did not exist when it was written.

No file was edited except this one. No frozen byte, corpus file, SKILL.md, SCORECARD, LOG or
figures.tsv was written. Scratch ran under `/home/vgpnk/revledger-*` because `/tmp` was full
(100%, 392 KB free); the lane checkout was read-only. No installs.

---

## 1. Verdict

**The landed ledger is a good-faith sample of the report's figures, not "one row per numeric
assertion the round report makes". It is arithmetically sound and materially better than the
proposal, but it leaves the report's before-values and most of the claim-verdict evidence
outside the ledger, and `C1=met` still certifies only ledger arithmetic at one revision.**

- **16/16 rows reconcile at `5157cdda` and again at `5102022a`** (I ran each command and the
  counter at both revisions). `C1=met mismatches=0`, exit 0, at both.
- **11 rows are load-bearing**, 3 are proxies, 2 are decorative (`F09`, `F16`). Removing the two
  decorative rows still leaves 14 rows and all five class labels, so they are padding, not floor
  necessity.
- The landed ledger **fixes the proposal's worst rows**: it drops the `.ufo/waves/` round-dir
  count that looked like a seat count, the `.md`-report count mislabeled "seat logs" (a false
  zero while `w1` is absent), the corpus/evidence file count and the spotcheck-lesson count; it
  adds the report's real figures — 32 seats, 3 sweep files, 3 new criteria, 14 check lines,
  8 mistakes, 2 rows naming the entry.
- But it **drops four load-bearing proposal rows**: the 10 freeze pins, the 3 do-nothing
  controls, the 3 counters, and the 6 C1 selftest arms. The report's C1/C2 evidence sentences
  ("10 pinned artifacts", "three controls", "three counters", "`pass=6 fail=0`") are now
  uncovered.
- **Uncovered and required**: every before-value (243, 116, 53, 72, 0 sweep), the census
  (245 rows / exit 0 / findings 20), the README frontier row, the role mix (12 attack roles,
  37.5%), dead seats, the 31 reports returned, the witness's 12 rows / 15 / 34 / 2 mismatches,
  the other three selftest tallies (5 / 6 / 6), the gate table total (23), the gate inventory
  (33 / 18 / 15), the round-44 evidence count (11), and the ledger's own 16 rows / 5 classes.
- **Rev identity is honest**: the receipt names `5157cdda`; `C1=met` also holds at the later tip
  `5102022a` because no counted path changed. The report must name `5157cdda`, not "the tip".
- **`C1=met` does not mean "the round's reported counts are reconciled."** It means the 16-row
  ledger parses, spans five labels, and each row's own command equals its asserted integer at
  the measured revision. The report's own measured-outcome cell already discloses the vacuity
  half; this review adds the coverage, rev-identity and `@REV@`-use limits (§8).

---

## 2. What I ran (receipts)

### 2.1 The landed ledger, both revisions

```
$ python3 .ufo/waves/round-44/count-c1.py 5157cdda
check ledger_present       PASS (1321 bytes)
check rows_parse           PASS (16 rows)
check row_floor            PASS (rows=16 min=12)
check class_floor          PASS (classes=checks,corpus,evidence,registry,wave min=4)
check commands_reconcile   PASS (all rows match)
rev=5157cdda41ca711da280a85e7d3ec13da6ec85d3
C1=met mismatches=0        (exit 0)

$ python3 .ufo/waves/round-44/count-c1.py 5102022a
… same five PASS lines …
rev=5102022a3978e167eaf34dbaecad68ae320a5fbe
C1=met mismatches=0        (exit 0)
```

`git diff --stat 5157cdda 5102022a -- corpus SKILL.md .ufo/waves/round-43
.ufo/waves/round-44/figures.tsv .ufo/waves/round-44/w1-spec.json .ufo/waves/round-44/fixtures`
is empty, and the ledger's sha256 is identical at both revisions. The after commit added
`after/` receipts, `evidence/census-end.txt`, late `w1/` reports and `SCORECARD.md` — no counted
path. That is why `C1=met` survives the tip move.

Row-by-row at `5157cdda` (counter invocation: `@REV@` → rev, `2>/dev/null | head -c 64`,
cwd = lane):

```
F01 245=245  F02 2=2    F03 3=3    F04 54=54
F05 119=119  F06 3=3    F07 4=4    F08 72=72
F09 10=10    F10 8=8    F11 14=14  F12 32=32
F13 4=4      F14 8=8    F15 73=73  F16 15=15
```

**16/16 reconcile.** The arithmetic half is sound at both revisions.

### 2.2 The proposal, at the freeze commit

I extracted the 20 draft rows (`ExecLedger.md:48-67`) and ran each exactly as `run_row` does:

```
F01 72=72  F02 10=10  F03 8=8   F04 39=39  F05 32=32
F06 0=0    F07 243=243 F08 192=192 F09 6=6  F10 3=3
F11 10=10  F12 72=72  F13 116=116 F14 53=53 F15 195=195
F16 28=28  F17 4=4    F18 3=3   F19 4=4    F20 6=6
```

**20/20 reconcile at `7cb59c68`.** I also rebuilt the freeze tree plus the draft in scratch and
reproduced the proposal's green run at `ff4e2ae2…`: `C1=met`, 20 rows, 5 classes — at a revision
whose registry is 243 and whose criteria are 116, i.e. the **before** values.

### 2.3 Witness, selftest, after receipts

```
$ python3 .ufo/waves/round-44/count-c1.py 7cb59c68 --ledger .ufo/waves/round-44/fixtures/figures-r43.tsv
check commands_reconcile   FAIL (F03 asserted=15 observed=14; F04 asserted=34 observed=8)
C1=unmet mismatches=2        (exit 1)

$ python3 .ufo/waves/round-44/count-c1.py --selftest
… C1_SELFTEST pass=6 fail=0  (exit 0)
```

`after/c1-after.txt` (13 lines), `after/c2-after.txt` (12), `after/c3-after.txt` (13) and
`evidence/census-end.txt` are committed at `5102022a`. Their measured rev is `5157cdda`:
C1 16 rows / 5 classes / `C1=met`; C2 five checks PASS / `C2=met` (tallies c1 6, c2 5, c3 6);
C3 five checks PASS / `C3=met` under `TMPDIR=<lane>`; census `ok`, `exit=0`, `rows=245`,
`findings=20`.

---

## 3. The landed ledger, row by row

Legend: **L** load-bearing (a figure a required report section or the measured-outcome cell
states), **P** proxy (counts a required artifact but not the stated figure), **D** decorative
(no required section states it).

| id | asserted | class | what the command measures | verdict |
|---|---|---|---|---|
| F01 | 245 | registry | `corpus/SOURCES.md` registry rows | **L** — Sources & frontier after-value |
| F02 | 2 | registry | lines naming `corpus/knowledge/pid-probe-conclusion-r44.md` | **L** — the two `used-by` rows |
| F03 | 3 | corpus | files matching `Z ゾンビ` under `corpus/` | **L** — the corrected sweep after-value |
| F04 | 54 | corpus | knowledge `.md` files | **P** — report states "one entry" |
| F05 | 119 | corpus | numbered criteria in `QUALITY.md` | **L** — criteria after-value |
| F06 | 3 | corpus | criteria numbered `117`–`119` | **L** — three new criteria |
| F07 | 4 | registry | gate rows whose name begins `r44 ` in `SKILL.md` | **L** — four r44 rows |
| F08 | 72 | wave | round-43 seat logs | **L** — erratum "8 of 72" |
| F09 | 10 | wave | round-43 w1 reports | **D** — round-43's wave record |
| F10 | 8 | wave | round-43 logs carrying `provider.rate_limit` | **L** — routed defect 3 |
| F11 | 14 | checks | `^check` lines in round-43 `c1s-after.txt` | **L** — 14 checks (defect 3) |
| F12 | 32 | wave | `"role"` entries in `w1-spec.json` | **L** — 32 seats |
| F13 | 4 | evidence | files under `.ufo/waves/round-44/fixtures` | **P** — witness + 3 mutants |
| F14 | 8 | corpus | mistake rows `M1`–`M8` in `corpus/lessons/round-44.md` | **L** — M1–M8 |
| F15 | 73 | corpus | lesson `.md` files | **P** — report states the lesson, not the total |
| F16 | 15 | evidence | files under `.ufo/waves/round-43/evidence` | **D** — round-43's evidence count |

Counts: **L 11**, **P 3**, **D 2**. Drop F09 and F16 and the ledger still has 14 rows and
classes `registry, corpus, wave, checks, evidence` — both floors hold without them. They are
padding by construction.

### 3.1 What the landed ledger covers well

It backs the figures the report's **Sources & frontier** and **Trend verdicts** sections state:
245 registry rows, the two rows naming the entry, the 3-file `Z ゾンビ` sweep, 119 criteria, the
3 new criteria, 4 r44 gate rows, 72/8 round-43 seat-log figures, 14 check lines, 32 seats, and
M1–M8. That is a real improvement on the proposal, which had none of 32 seats, 3 sweep files,
3 criteria, 14 checks or 8 mistakes.

### 3.2 What it dropped from the proposal (coverage regression)

The proposal carried four load-bearing rows the landed ledger does not:

| proposal row | figure | report sentence it backs | landed? |
|---|---|---|---|
| F10 | 3 | three do-nothing controls (`evidence/control-c{1,2,3}-donothing.txt`) | **dropped** |
| F11 | 10 | 10 pinned artifacts (`RevEnteringBaseline.md` "10/10 pinned artifacts match") | **dropped** |
| F18 | 3 | three round counters (C2's object) | **dropped** |
| F20 | 6 | `C1_SELFTEST pass=6 fail=0` (C1's own evidence) | **dropped** |

The measured-outcome cell says "16 rows, 5 classes", "five checks PASS" for C2, "five checks
PASS" for C3 and cites the tallies. None of those is a ledger row. The landed ledger is strong on
**corpus/registry content** and weak on **claim-verdict evidence**.

### 3.3 The proposal's defects, for the record

The landed ledger avoided them, but the proposal is still the document a round-45 author will
read, so they are recorded here:

1. **"every row a count the round's report will cite"** (`ExecLedger.md:15`) is false for 4 of
   its 20 rows: F02 (round-43 reports), F05 (round dirs), F15 (`corpus/evidence` 195 files),
   F16 (spotcheck lessons). The report contract requires the wave's seat count/role mix
   (`prompt:215-216`), not these.
2. **F05 is a decoy.** It counts 32 *round directories* (`.ufo/waves/round-13` … `round-44`), not
   seats. It equals 32 today by coincidence and would stay 32 for a 31- or 33-seat wave.
3. **F06 is mislabeled and is a false zero.** The proposal calls it "round-44 wave-1 seat logs"
   (`ExecLedger.md:101`), but the command counts `*.md` **reports**; at the freeze and entering
   tips the `w1` subtree is absent, so `git ls-tree -r … | grep '\.md$' | wc -l` prints `0` with
   **rc 0** — not "zero reports". The proposal's §8.3 justification (`F05` proves the
   `.ufo/waves/` tree exists) does not prove the `w1` subtree exists.
4. **Two landing predictions are wrong by one commit.** The proposal says "`245 / 194 / 54 /
   119 / 29 / 74` are the arithmetic consequences" (`ExecLedger.md:212`). `F16`=29 and `F12`=74
   assume the closure spotcheck lesson lands with the round; it does not. Round-43's closure
   lesson landed at `1429c791`, one commit **after** the round-43 tip `91cb221f`
   (`git log --oneline -3 1429c791`; `git show --stat 1429c791` adds only that lesson). At the
   round-44 landing the lesson count is 73 (landed `F15`), and no spotcheck lesson is present.
5. **Seven cells were stale at landing** (F06, F07, F08, F09, F12, F13, F14). The proposal said
   so and gave a re-derivation recipe; the landed ledger executed the equivalent.

---

## 4. Figures the report states that no landed row covers

Grounded in the report contract (`prompt:104-118`, `prompt:215-216`) and the measured-outcome
cell (`SCORECARD.md`, "Round 44 measured outcome"). Values are from the committed receipts at
`5102022a` / the integration tip.

| figure the report states | value | row? |
|---|---|---|
| SOURCES rows **before** | 243 | **no** — F01 yields 245 at the measured rev |
| criteria **before** | 116 | **no** — F05 yields 119 |
| knowledge entries **before** | 53 | **no** — F04 yields 54 |
| lessons **before** | 72 | **no** — F15 yields 73 |
| C3 sweep **before** | 0 files | **no** — F03 yields 3 |
| rows touched old→new | 0 | **no** |
| census rows / exit / findings | 245 / 0 / 20 (`evidence/census-end.txt`) | **no** — F01 is the registry, not the census |
| README frontier row | 1 (`## Round-44`) | **no** |
| knowledge entry delta | 1 | **no** — F04 is the total |
| wave seat count | 32 | **F12** |
| attack roles / share | 12 / 37.5% | **no** |
| reports returned | 31 at landing; 32 at `5102022a` | **no** |
| seat still running at landing | 1 (`RevLedgerVsReport`) | **no** |
| dead seats | 0 named | **no** |
| round total | 32 | **F12** (seats) |
| C1 ledger size | 16 rows / 5 classes | **no** — no self-row |
| C1 witness fixture rows | 12 | **no** — F13 counts 4 fixture files |
| C1 witness asserted/observed | 15→14, 34→8 | **partial** — F11 gives 14, F10 gives 8; 15 and 34 uncovered |
| C1 witness mismatches | 2 | **no** |
| C2 checks PASS | 5 | **no** — F11 is 14 c1s check lines |
| C3 checks PASS | 5 | **no** |
| selftest tallies | 6 / 5 / 6 / 6 | **no** |
| freeze pins | 10 | **no** — proposal F11, dropped |
| do-nothing controls | 3 | **no** — proposal F10, dropped |
| round counters | 3 | **no** — proposal F18, dropped |
| gate table rows total | 23 | **no** — F07 is the 4 r44 rows |
| gate inventory | 33 tools / 18 PASS / 15 FAIL | **no** |
| round-44 evidence files | 11 | **no** — F16 is round-43 evidence (15) |
| C3 sweep after | 3 | **F03** |

The ledger therefore backs **the content half of the report** (registry, corpus, gate rows,
seats, the sweep) and leaves **the claim-evidence half** (C1/C2/C3 check counts, tallies,
controls, pins, witness mismatch, before-values, census, inventory) to prose and receipts.

Two of these deserve emphasis.

**The C3 sweep is 3 files.** Contract P-C3 says "After … → 1 file". The landed ledger carries 3
(`F03`), the SCORECARD correction records the contract sentence as wrong, and the three files are
`corpus/README.md`, `corpus/SOURCES.md` and `corpus/knowledge/pid-probe-conclusion-r44.md`. That
is now consistent — but it means the report must not repeat the frozen contract's "1 file".

**The witness numbers are outside the ledger.** The report's routed-defect-3 sentence is "15
checks observed 14; 34 seat logs observed 8". The ledger carries 14 (F11) and 8 (F10), not 15 or
34; the fixture row count (12) and the mismatch count (2) are also outside. The witness is
evidenced by running `fixtures/figures-r43.tsv` through the counter, not by the ledger.

---

## 5. Rev identity, stability and the drift the landed ledger avoided

- The receipt `after/c1-after.txt` names `5157cdda`; the SCORECARD measured outcome names the
  same rev. The lane tip is `5102022a`. `C1=met` holds at both because no counted path moved
  (`§2.1`). The report must say **"measured at 5157cdda"**, not "at the landed tip", unless it
  re-runs the counter at `5102022a` and receipts that run. QUALITY 119 is satisfied as filed;
  it would be violated by a sentence that swaps the two revs.
- **The 31→32 report growth is the drift the proposal would have hit.** `w1` has 31 `*.md` at
  `5157cdda` and 32 at `5102022a` (this report). The proposal's F06 counted those files; a
  ledger filed at `5157cdda` with F06=31 would be `C1=unmet` at `5102022a` with
  `F06 asserted=31 observed=32`. I demonstrated the mechanism in scratch: a re-derived 20-row
  ledger was `C1=met` at B, then one late report at C produced
  `check commands_reconcile FAIL (F06 asserted=17 observed=18)` → `C1=unmet mismatches=1`. The
  landed ledger has **no** report-count row, so it is stable — but that also means the report's
  "31 reports returned / 1 still running" sentence has no ledger row.
- The proposal's §6 fallback spine (12 rows, no registry) could not support the mandatory
  **Sources & frontier** section ("`SOURCES.md` rows before→after with the counting command",
  `prompt:111-112`). The landed ledger correctly kept F01 and did not use the spine.

---

## 6. The grammar still does not enforce "re-derived at the measured revision"

The counter checks that `@REV@` is *present* in the command text (`count-c1.py:100`), not that the
command consumes it. Two demonstrations in scratch:

1. **HEAD-reading row.** Measured rev B has `data.txt` = 3 lines; one row
   `git show HEAD:data.txt | grep -c x # @REV@` asserted 4 (true only at the later commit C).
   At B: `check commands_reconcile PASS (all rows match)` → `C1=met`, although B's own value is 3.
2. **Hard-coded old revision.** A row `git show <A>:data.txt | grep -c x # @REV@` asserted 3 at
   measured rev B (whose value is 4) and passed because `@REV@` sits in a comment.

The landed 16 rows do **not** exploit this: I inspected each command and every effective read
names `@REV@` (no `HEAD`, no literal rev). So the landed ledger's `C1=met` is, by inspection,
a genuine measured-revision result. The instrument still cannot certify that for the next
ledger; MutC1's attack #2 (SURVIVED) and ExecJunkLedger's 12 tautologies remain the round's
disclosed limits.

---

## 7. Does `C1=met` mean what the report says?

The claim wording is "a committed figure ledger reconciles the round's reported counts …
re-derived at the measured revision" (`SCORECARD.md:2410`; `contract.md:23-28`). The measured
outcome already narrows it: "the content half — that each row is a figure the report states — is
**not** machine-checked" (SCORECARD, C1 row).

**What `C1=met` certifies** (code + my runs):

1. `.ufo/waves/round-44/figures.tsv` exists at the measured rev and parses into ≥12 four-cell
   rows whose ids, classes and command grammar pass `parse_ledger`.
2. The rows span ≥4 distinct class strings (the string need not match what the command reads).
3. For each row, the row's own pipeline prints the asserted integer at the measured rev.

**What it does not certify:**

1. That the rows are the report's figures. No row→sentence linkage exists; 2 of 16 are
   decorative and 3 are proxies.
2. That every report figure is covered. §4 is most of the claim-evidence half.
3. That the measured rev is the tip the report names (§5).
4. That each row actually reads `@REV@` (§6).
5. That the figures are non-trivial (ExecJunkLedger; QUALITY 117's "Not covered" cell).
6. That the report's prose equals the ledger's numbers — the counter never reads the report.

**Verdict.** A report sentence of the form "C1=met — the round's reported counts are reconciled"
is **false as a universal**. The true sentence is: "the ledger's 16 figures reconcile at
`5157cdda`; the remaining report figures are cited with their own commands and receipts and are
outside the ledger." That is a real, measured improvement over round 43's unaudited counts, and
it is narrower than the claim's title. The closure should read it that way.

---

## 8. Residual risk and verification gaps

- **Before-values are structurally outside a single-`@REV@` ledger.** The report's
  before→after table (243→245, 116→119, 53→54, 72→73, 0→3) is half-covered. The only way to put
  a before-value in this ledger is to hard-code the old rev and park `@REV@` in a comment
  (§6.2), which is a snapshot, not a reconciliation. The SCORECARD's separate before-cells and
  the `control-*-donothing.txt` receipts are the right vehicle; the report should say so.
- **The report is not written.** Every "figure the report states" in §4 is derived from the
  measured-outcome cell and the report contract, not from prose. A report that omits some
  sections would shrink the gap; `Sources & frontier` and `Before → after measurements` are
  required.
- **C3's `TMPDIR` requirement is a disclosed instrument defect.** `after/c3-after.txt` runs with
  `TMPDIR=<lane>`; the default staging under `/tmp` makes `used-by` resolve against `/tmp` and
  exits 1 (`RevEnteringBaseline.md` F-1; SCORECARD correction 6). `C3=met` is true only under
  that override. This is C3, not C1, but the report must not present `C3=met` as the default
  invocation.
- **C2's default `--mutants-dir` does not exist.** The runnable form passes
  `--mutants-dir .ufo/waves/round-44/fixtures/mutants`; the SKILL.md entry cell carries the same
  gap (SCORECARD correction 4). Again not C1, but it is a claim-evidence figure the ledger does
  not carry.
- **I did not re-run the proposal's sandbox revisions** (`85fc3bca`, `55703287`, `729ed5ac`); I
  reproduced the freeze-tree case at `ff4e2ae2` and the drift/hole cases independently. The
  landed ledger's 16 rows I re-ran at both real revisions.

---

## 9. Routed recommendations (no edits made)

1. **Keep the 16 rows; add only report-stated figures**: the census (`rows=245`, `exit=0`,
   `findings=20` from `evidence/census-end.txt`), the README Round-44 row (1), the attack-role
   count (12 / 37.5%), the witness mismatch count (2) and fixture row count (12), the other
   selftest tallies (5 / 6 / 6), the gate table total (23), the round-44 evidence count (11), and
   the ledger's own 16/5. Do not add more proxies.
2. **Restore the four dropped claim-evidence rows**: 3 controls, 10 freeze pins, 3 counters,
   6 C1 selftest arms — or state those figures in prose with their receipts and say they are
   outside the ledger.
3. **Drop F09 and F16.** They are round-43 artifacts the round-44 report contract does not
   state; 14 rows and 5 classes remain.
4. **Name the measured rev.** The report must say `5157cdda` for C1 (the receipt's rev), not
   `5102022a`, unless it re-runs and receipts the counter at `5102022a`.
5. **Report the C3 sweep as 3 files**, not the frozen contract's 1; the SCORECARD correction
   already records the contract sentence as wrong.
6. **Round 45 instrument tightening** (frozen bytes are not amended this round): a
   revision-sensitivity arm, rejection of rows whose effective read is `HEAD`/the working tree,
   an absent path as FAIL not zero, distinct ids/commands, and a row→report-anchor manifest —
   the only way "reconciles every reported count" becomes machine-checkable.

Report: `.ufo/waves/round-44/w1/RevLedgerVsReport.md`
