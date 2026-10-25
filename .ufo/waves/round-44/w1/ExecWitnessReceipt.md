# Exec — C1 witness receipt: the round-43 closure's two count slips, caught by the counter

lane: mori · round: 44 · wave: 1 · role: executor (leaf, no dispatch) · date: 2026-10-25
lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin` · lane tip `7cb59c6891d4f5d0266fe062565f094da835dc84`
freeze commit `7cb59c6891d4f5d0266fe062565f094da835dc84` (`round-44: frozen contract and instruments`)
fleet repo: `/home/vgpnk/Projects/shokunin` (read-only, nothing written)

Scope: reproduce the contract's P-C1 witness (`.ufo/waves/round-44/contract.md`, "**Witness**")
at the freeze commit and at the lane tip, then check every one of the fixture's twelve asserted
values against what round 43 actually asserted. Nothing was edited except this report; no frozen
instrument, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/` file or fixture was touched; no
`git add/commit/push/checkout/stash/reset` and no jj mutation was run.

---

## 1. The bytes I measured

Both invocations resolve to the same revision: the freeze commit *is* the lane tip at
measurement time.

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin && git rev-parse HEAD
7cb59c6891d4f5d0266fe062565f094da835dc84
$ git log --oneline -2
7cb59c68 round-44: frozen contract and instruments — C1 figure ledger, C2 gate standard, C3 corpus coverage
1429c791 round-43 verifier spot-check (integrator, hyaku): non-author admit/reject
$ git status --porcelain | head
?? .ufo/waves/round-44/w1-spec.json
```

The counter, the fixture and the contract are the frozen bytes pinned by
`evidence/freeze-r44.txt` (recorded before any data seat was dispatched):

```
$ sha256sum .ufo/waves/round-44/count-c1.py .ufo/waves/round-44/fixtures/figures-r43.tsv .ufo/waves/round-44/contract.md
9477824d5eee45f47d49be52902f7bb0cd67a4d038e0ec7e79094c1e71999f83  .ufo/waves/round-44/count-c1.py
51e63f0186c5d8edcfd283edd29de1e6df95a65959611302c03491128f2ce953  .ufo/waves/round-44/fixtures/figures-r43.tsv
0c261cb310c63e093d0cff3c71455a4d3ac7fe8d7e6ee162ee2190732e17555d  .ufo/waves/round-44/contract.md
```

All three equal the pins (`9477824d…`, `51e63f01…`, `0c261cb3…`). The fixture is 1518 bytes,
12 rows, classes `checks,corpus,evidence,registry,wave` — the counter's own `ledger_present`
check reports the same size.

Every line pointer in this receipt is a **committed** line: lane files were read with
`git show 7cb59c68:<path>` and the fleet report with `git show 0c9e9999:<path>` (byte-identical
to the working-tree copy at the time of reading). The lane working tree concurrently carries
sibling wave-1 edits (`LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/README.md`,
`corpus/SOURCES.md`, `corpus/lessons/round-43.md`, a new `corpus/knowledge/` entry); none is
mine, none was read as a source for a quote, and none changes the committed bytes scored here.

---

## 2. The two runs — freeze commit and lane tip

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ python3 .ufo/waves/round-44/count-c1.py 7cb59c6891d4f5d0266fe062565f094da835dc84 \
      --ledger .ufo/waves/round-44/fixtures/figures-r43.tsv
check ledger_present       PASS (1518 bytes)
check rows_parse           PASS (12 rows)
check row_floor            PASS (rows=12 min=12)
check class_floor          PASS (classes=checks,corpus,evidence,registry,wave min=4)
check commands_reconcile   FAIL (F03 asserted=15 observed=14; F04 asserted=34 observed=8)
rev=7cb59c6891d4f5d0266fe062565f094da835dc84
ledger=.ufo/waves/round-44/fixtures/figures-r43.tsv rows=12 classes=checks,corpus,evidence,registry,wave
C1=unmet mismatches=2
EXIT=1

$ TIP=$(git rev-parse HEAD); echo "TIP=$TIP"
TIP=7cb59c6891d4f5d0266fe062565f094da835dc84
$ python3 .ufo/waves/round-44/count-c1.py "$TIP" --ledger .ufo/waves/round-44/fixtures/figures-r43.tsv
check ledger_present       PASS (1518 bytes)
check rows_parse           PASS (12 rows)
check row_floor            PASS (rows=12 min=12)
check class_floor          PASS (classes=checks,corpus,evidence,registry,wave min=4)
check commands_reconcile   FAIL (F03 asserted=15 observed=14; F04 asserted=34 observed=8)
rev=7cb59c6891d4f5d0266fe062565f094da835dc84
ledger=.ufo/waves/round-44/fixtures/figures-r43.tsv rows=12 classes=checks,corpus,evidence,registry,wave
C1=unmet mismatches=2
EXIT=1
```

**Verdict: exactly the contract's declared witness.** `C1=unmet mismatches=2`, exit 1, naming
`F03 asserted=15 observed=14` and `F04 asserted=34 observed=8`; the row floor (12) and class
floor (4) pass, so the verdict is the reconciliation failure and not a shape rejection. Because
freeze commit == lane tip, the two runs are the same invocation on the same bytes and are
byte-identical in output.

---

## 3. The two figures really are what round 43 asserted

### 3.1 The "15 checks" figure — report only, never the lesson

Fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-43/mori.md` is unmodified and
byte-identical to its final fleet revision `0c9e9999` (`sha256 ea6ac0f6a3ed0d8e49d7bd14789d6a85c3dadd4ee028ae7feead4959ffb0b10a`
for both the working-tree file and `git show 0c9e9999:…`).

**Sentence 1 — the Before→after table (L109), the claim F03 reproduces against `c1s-after.txt`:**

```
| **C1S** — operability | `python3 .ufo/waves/round-43/count-c1s.py e3a2b58…` → `check self_at_rev FAIL (absent)` → `C1S=unmet`, exit 1 | `python3 .ufo/waves/round-43/count-c1s.py <tip>` → 15 checks PASS (incl. `noharm_cwd PASS (rc=0 MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0)`, `v5_selftest_17 PASS (pass=17 fail=0 rc=0)`, three `mutant_kill_* PASS (pass=16 fail=1)` on exactly their own arms, `frozen_still_crashes PASS (rc=1 crash=True C1_line=False)`) → `C1S=met`, exit 0 | `dde525ea4a7fca365e8ff2f3c486bccf28b94e52`; receipts `evidence/c1s-after.txt`, `evidence/c1s-clause-map.txt` |
```

The same figure is restated at **L45**:

```
  a scratch clone → 15 checks PASS, `C1S=met` exit 0 (`evidence/control-c1s-green.txt`);
```

and at **L123** (`landed tip the counter prints 15 PASS lines, …`), and outside the report in
`SCORECARD.md:2381` ("→ 15 checks PASS, then `C1S=met` exit 0 (`evidence/c1s-after.txt`)"),
`LOG.md` §"Round 43" ("green control on a scratch clone carrying the counter → 15 checks
PASS") and `evidence/c1s-mutants.txt:19,32` ("the healthy counter prints 15", "the counter
printed 15").

**`corpus/lessons/round-43.md` carries no "15 checks" wording at all:**

```
$ grep -n '15 checks' corpus/lessons/round-43.md || echo "NO '15 checks' in lesson"
NO '15 checks' in lesson
```

Its only `15` substrings are `15410` (L62, L144) and `QUALITY 115` (L110, L120). So the
contract's phrase "as the round-43 report **and** lesson assert them" holds per-figure: F03's
authority is the report (plus SCORECARD/LOG/mutant receipt), F04's is the report *and* the
lesson.

**Observed 14, and why 14 is the honest number (not a truncated receipt):**

```
$ git show 7cb59c68:.ufo/waves/round-43/evidence/c1s-after.txt
command: python3 .ufo/waves/round-43/count-c1s.py dde525ea4a7fca365e8ff2f3c486bccf28b94e52
when: 2026-10-24T22:53:03-03:00
check self_at_rev            PASS (match)
check frozen_sha             PASS (105ce075f331)
check frozen_sig             PASS (run params argv, timeout)
check v5_present             PASS (.ufo/waves/round-42/conform.py)
check sandbox_clone          PASS
check noharm_cwd             PASS (rc=0 MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0)
check v5_selftest_17         PASS (pass=17 fail=0 rc=0)
check mutant_present_walrus-branch PASS (.ufo/waves/round-42/fixtures/mutants/conform-mut-walrus-branch.py)
check mutant_kill_walrus-branch PASS (pass=16 fail=1 fails=['timeout_scope_walrus_positive'])
check mutant_present_tuple-extract PASS (.ufo/waves/round-42/fixtures/mutants/conform-mut-tuple-extract.py)
check mutant_kill_tuple-extract PASS (pass=16 fail=1 fails=['timeout_scope_tupleunpack_positive'])
check mutant_present_sort-deletion PASS (.ufo/waves/round-42/fixtures/mutants/conform-mut-sort-deletion.py)
check mutant_kill_sort-deletion PASS (pass=16 fail=1 fails=['timeout_scope_source_order'])
check frozen_still_crashes   PASS (rc=1 crash=True C1_line=False)
C1S=met
exit=0
```

14 `^check` lines, then the verdict line. The counter that produced it emits exactly 14 by
construction: 10 `check(` call sites in `count-c1s.py`, two of which (L145 `mutant_present_%s`,
L152 `mutant_kill_%s`) sit inside `for name, arm in V5_MUTANTS:` over three mutants — 8 + 6 =
14. The generated `evidence/c1s-clause-map.txt` also lists 14 clauses, one per check line.
So "15" is a prose over-count, not a 15th check hidden by a prefix mismatch. Note the L45
attribution is off by one as well: `evidence/control-c1s-green.txt` also has 14 check lines
(`grep -cE '^check'` → 14).

### 3.2 The "34 seat logs" figure — report and lesson

**Sentence 2 — report L11–L12 (opening round-shape paragraph):**

```
in the round. The 64-seat wave was starved by the provider's rate limit (34 seat logs carry
`provider.rate_limit: 429`); 60 of its seats are dead seats and are not credited and were not
```

**Sentence 3 — `corpus/lessons/round-43.md` L132–L133** (from `git show 7cb59c68:corpus/lessons/round-43.md`;
the lesson is byte-identical at `efb92cd5`, `91cb221f`, `1429c791` and the freeze commit):

```
The 64-seat v2 wave was starved by the provider's rate limit (34 seat logs
carry `provider.rate_limit: 429`); 52 of its seats were then killed by the
```

(Working-tree note: `corpus/lessons/round-43.md` now carries a **sibling's appended round-44
erratum** — 21 added lines after the filed bytes, `git diff 7cb59c68 -- corpus/lessons/round-43.md`.
It is not mine and I did not touch it; it appends, it does not rewrite, and it leaves L132–L133
and the absence of any "15 checks" wording exactly as committed.)

The report restates it at **L210**:

```
  34 seat logs carrying `provider.rate_limit: 429 Rate limit reached for requests`. Those 60
```

and `LOG.md` §"Round-43 seat logs" restates it twice ("34 of the 64 seat logs carry …",
"`provider.rate_limit: 429` in 34 of the 64 wave seats").

**Observed 8, under both wordings, so the fixture's looser command is not the discrepancy:**

```
$ git ls-tree -r --name-only 7cb59c68 .ufo/waves/round-43/logs | wc -l      -> 72
$ git grep -l 'provider.rate_limit'     7cb59c68 -- .ufo/waves/round-43/logs | wc -l -> 8
$ git grep -l 'provider.rate_limit: 429' 7cb59c68 -- .ufo/waves/round-43/logs | wc -l -> 8
$ git grep -l '429' 7cb59c68 -- .ufo/waves/round-43/logs | wc -l            -> 39
$ git grep -c 'provider.rate_limit' 7cb59c68 -- .ufo/waves/round-43/logs | awk -F: '{s+=$3} END {print s}' -> 8
```

The eight logs are `wave64/{Crit11,Rev11,Rev7,Rev8,Scout10,Scout2,Scribe1,Scribe6}.log`. The 34
figure is not reproducible from any obvious count: 8 logs carry `provider.rate_limit`, 8 carry
the exact `provider.rate_limit: 429` text, 39 logs merely contain the string `429` (matching
the closure's own note), and 72 logs exist in total. F04's command is the closure's own
command (`git grep -l 'provider.rate_limit' 91cb221f -- .ufo/waves/round-43/logs`, routed
defect 3) plus an explicit `| wc -l`.

---

## 4. Row-by-row verification of all twelve asserted values

Method: for every row, the round-43 assertion was located in committed bytes (fleet report at
`0c9e9999` — working tree verified byte-identical; lane lesson/LOG/SCORECARD at `7cb59c68`);
the observed value is the counter's own output at the freeze revision (all twelve rows ran;
only F03/F04 failed). "Round-43 asserted" = a sentence round 43 actually wrote about that
artifact class.

| row | asserted | round-43's own words (file:line) | observed @`7cb59c68` | verdict |
|---|---|---|---|---|
| F01 | 243 | `mori.md:138` "→ **238 → 243** rows"; also `:64` "(`…validate-receipt.txt`, 243 rows)" | 243 (and 238 at the entering tip `e3a2b58`, the report's before-value) | matches |
| F02 | 72 | `mori.md:98` "\| the 72 seat logs (each dead seat's last error text), the frozen-sha mutant receipt \|"; `LOG.md:2591` "The 72 seat logs (64 wave seats … 8 residual seats …)" | 72 | matches |
| F03 | 15 | `mori.md:109` "→ 15 checks PASS (incl. …) → `C1S=met`, exit 0" (also `:45`, `:123`; `SCORECARD.md:2381`) | **14** | **mismatch — the slip the witness exists to catch; the row is faithful** |
| F04 | 34 | `mori.md:11-12` "The 64-seat wave was starved by the provider's rate limit (34 seat logs carry `provider.rate_limit: 429`)"; `:210`; lesson `:132-133`; `LOG.md` §"Round-43 seat logs" | **8** | **mismatch — the second slip; the row is faithful** |
| F05 | 10 | `mori.md:97` "…, the 10 seat reports, both settle tables, …" | 10 (4 wave + 6 residual `.md`, listed below) | matches |
| F06 | 116 | `mori.md:78` "A residual seat's S268 attack added **QUALITY 116**"; `:97` "QUALITY 116" | 116 numbered items, last item numbered `116.` | matches |
| F07 | 64 | `mori.md:199-200` "**One v2 wave**: 64 seats — attack 31 (48.4%: reviewer 12, critic 11, mutation-tester 8); build 33 (scout 12, scribe 8, executor 8, sentinel 2, connector 1, simplifier 1, revenger 1)" | 64 `"role"` fields, histogram exactly `scout 12, reviewer 12, critic 11, scribe 8, mutation-tester 8, executor 8, sentinel 2, simplifier 1, revenger 1, connector 1` (= attack 31 / build 33) | matches (see note N1) |
| F08 | 52 | `mori.md:209` "8 seats exited 1 and **52 were killed by the 540 s seat timeout**"; `LOG.md` "Settlement (`w1-settle.tsv`): 4 seats exit 0, 8 exit 1, 52 exit 124" | 52 rows with `$3==124`; histogram over 64 rows: `0→4, 1→8, 124→52` | matches |
| F09 | 6 | `mori.md:213` "**6 reports** — `ResCritDoNothing.md` …"; `LOG.md` names the same six, plus 2 dead at the timeout | 6 rows with `$3==0` of 8 (`ResCritBulkAppend`, `ResCritDeclaration` at `124`) | matches |
| F10 | 15 | **no round-43 sentence asserts an evidence-file count** (see §5) | 15 | **provenance defect — value honest, assertion not round 43's** |
| F11 | 5 | `mori.md:172` "The lesson's mistakes M1–M5 each name the criterion that should have caught them"; `SCORECARD.md:2392` "Mistakes M1–M5 in `corpus/lessons/round-43.md`" | 5 rows (`| M1 …` … `| M5 …`, lesson L120–L124) | matches |
| F12 | 3 | `mori.md:96` "registry rows S348–S351 + S470, three knowledge entries, …" (also `:18`) | 3 occurrences of `corpus/knowledge/`, one per entry (`c1s-cwd-r43.md`, `s235-sha-correction-r43.md`, `journal-disk-usage-total-r51.md`, lesson L19/L25/L30) | matches (see note N1) |

`F05`'s ten reports, observed: `Exec2.md`, `Exec4.md`, `Exec5.md`, `Exec6.md`,
`ResCritDoNothing.md`, `ResCritInPlace.md`, `ResCritJunk.md`, `ResCritNoHarm.md`,
`ResCritS268.md`, `ResCritScope.md` (the directory also holds the non-report
`swarm-registry.json`, which the row's `grep -c '\.md$'` correctly excludes).

Note N1 (not defects, recorded so the derivation is not mistaken for a direct quote): F07 and
F12 measure an artifact different from the sentence that carries the figure. F07's 64 is the
report's seat/role count, and the spec's role histogram reproduces the report's exact
breakdown, so the figure is the report's. F12's 3 is the report's "three knowledge entries"
count measured as mentions in the lesson, and each mention names one of those three entries.

---

## 5. The one defect in the witness: F10

F10 asserts `15` for `git ls-tree -r --name-only @REV@ .ufo/waves/round-43/evidence | wc -l`.
The value is honest — the directory holds 15 files at `efb92cd5`, at `91cb221f` and at the
freeze revision — but **round 43 never asserted that count anywhere**, so F10 is not a
reproduction of a round-43 figure. That contradicts the fixture's own header claim, "The other
ten rows are figures the round-43 report asserted correctly".

Evidence:

1. The report names evidence files but never counts them. Every `15` substring in it is a
   sha256 (`:40`), the check count (`:45`, `:109`, `:123`), QUALITY `115`/`116` (`:78`, `:96`,
   `:173`) or `15410` bytes (`:81`, `:243`) — never an evidence-file total. The landed-changes
   table counts receipts only piecewise (`:95` "the 5 control receipts, the census-start
   receipt, the S268 header receipt, the disk-usage receipt, the wave plan" = 9 files; `:97`
   adds 5 more; `:98` one more).
2. Searching every round-43 record for an evidence-count assertion returns nothing:

```
$ git grep -n -E '(15 (evidence|receipts)|(evidence|receipts)[^0-9]{0,20}15)' 7cb59c68 -- \
      LOG.md SCORECARD.md corpus/ .ufo/waves/round-43/
(only unrelated round-15 material under .ufo/waves/round-43/assimilation/validate/)
```

3. Per-file check of whether the report names each of the 15 committed evidence files: 12 are
   named by filename, `disk-usage-r43.txt` and `wave-plan.json` are named descriptively ("the
   disk-usage receipt", "the wave plan"), and `control-c2-junk.txt` is **never mentioned** — so
   even an inferred count from the report's prose would be 14, not 15.

Consequence: F10 reconciles, so it does not perturb the `C1=unmet mismatches=2` verdict and it
cannot mask either slip; but it means the fixture is 11-for-12, not 12-for-12, on "figures round
43 asserted", and the witness's claim to isolate the two slips rests on 9 honest asserted rows
plus 1 honest-but-unasserted row (F01, F02, F05–F09, F11, F12 = 9 asserted rows that reconcile;
F03, F04 = 2 asserted rows that do not).

Since the fixture is frozen, I did not patch it; the repair belongs to a routed round-45 item.
Two replacement rows were measured, and each restates a sentence round 43 wrote:

- `2` / wave / `git show @REV@:.ufo/waves/round-43/w1-settle-residual.tsv | awk -F'\t' '$3==124' | wc -l`
  ← `mori.md:219` "**2 dead seats** (`ResCritBulkAppend`, `ResCritDeclaration`) were killed at
  the timeout"; observed 2 at `7cb59c68`.
- `8` / wave / `git show @REV@:.ufo/waves/round-43/w1-settle.tsv | awk -F'\t' '$3==1' | wc -l`
  ← `mori.md:209` "8 seats exited 1"; observed 8 at `7cb59c68`.

The obvious candidate is **not** safe: `mori.md:95`'s "the 5 control receipts" describes five
controls, but six `control-*` receipts are committed at that same commit `dde525ea`
(`control-c2-junk.txt` is the sixth, and the report never mentions it), so a row asserting `5`
against the committed `control-*` set would observe 6 — a third off-by-one of the same family,
not a replacement. **Blocking note for C1's own ledger:** the same trap applies to
`.ufo/waves/round-44/figures.tsv` — every row there must be a figure this round's report
actually asserts, not a convenient count of a committed directory.

---

## 6. Stability and evaluability of the witness

All twelve rows replayed by hand at round 43's own final lane tip (`91cb221f`, the revision the
report cites for the 72 seat logs) produce the same 12 results — 10 matches, F03 `15→14`,
F04 `34→8`:

```
$ # rows extracted from the fixture, @REV@ -> 91cb221f35f7cb9afeff99ef1959512dabddfc46
F01 asserted=243 observed=243 MATCH      F07 asserted=64  observed=64  MATCH
F02 asserted=72  observed=72  MATCH      F08 asserted=52  observed=52  MATCH
F03 asserted=15  observed=14  MISMATCH   F09 asserted=6   observed=6   MATCH
F04 asserted=34  observed=8   MISMATCH   F10 asserted=15  observed=15  MATCH
F05 asserted=10  observed=10  MATCH      F11 asserted=5   observed=5   MATCH
F06 asserted=116 observed=116 MATCH      F12 asserted=3   observed=3   MATCH
```

So the two mismatches are not artifacts of commits landed after round 43.

The frozen counter itself cannot be pointed at `91cb221f`, because it reads the ledger *at the
measured revision* (`read_at(repo, rev, ledger)`); measured, not inferred:

```
$ python3 .ufo/waves/round-44/count-c1.py 91cb221f35f7cb9afeff99ef1959512dabddfc46 \
      --ledger .ufo/waves/round-44/fixtures/figures-r43.tsv
check ledger_present       FAIL (absent)
rev=91cb221f35f7cb9afeff99ef1959512dabddfc46
ledger=.ufo/waves/round-44/fixtures/figures-r43.tsv rows=0 classes=-
C1=unmet mismatches=?
EXIT=1
```

That is the instrument working as specified (the ledger must be committed at the revision it
scores), but it bounds where the witness is evaluable: revs at or after the freeze commit. At
`efb92cd5`/`dde525ea` the fixture's F02/F04 classes do not even exist (`.ufo/waves/round-43/logs`
is added by `91cb221f`), so those rows would read 0 — the witness is revision-bound to
`≥ 91cb221f` for content and `≥ 7cb59c68` for the ledger.

---

## 7. Result, risks, blockers

- **Result.** The witness reproduces exactly as the contract declares: `C1=unmet mismatches=2`,
  exit 1, naming F03 (`15` asserted / `14` observed) and F04 (`34` asserted / `8` observed),
  with the row and class floors passing. Both asserted values are what round 43 wrote: "15
  checks PASS" (report L109, also L45/L123, SCORECARD 2381, LOG, `c1s-mutants.txt`) and "34 seat
  logs carry `provider.rate_limit: 429`" (report L11–L12, L210; lesson L132–L133; LOG). The
  lesson carries no "15 checks" wording, so the contract's "report **and** lesson" phrase holds
  per-figure only.
- **Defect reported (one).** F10's `15` is a correct file count but not a round-43 assertion;
  the fixture's "the other ten rows are figures the round-43 report asserted correctly" is false
  for F10. It does not change the verdict; it is a provenance defect for a round-45 route (the
  fixture is frozen and was not touched).
- **Risks.** (a) Any round-44 `figures.tsv` row that counts a directory or file set rather than
  restating a sentence the report makes repeats F10's defect — and the counter cannot detect
  that, since it only compares numbers. (b) F07/F12-type rows whose figure is asserted about a
  different artifact than the one measured are legitimate here only because the artifact's
  measurement equals the asserted figure exactly; a looser one would be silently wrong.
- **Blockers.** None. No tool was installed or upgraded this wave (no pacman/uv/npx/curl
  invocation); all work was read-only `git` plus the frozen Python counter, run from the lane
  repo with absolute paths. Scratch use: one `mktemp -d` (`/tmp/tmp.rer5tllYHG`) holding a copy
  of the fixture for the 12-row replay at `91cb221f`; nothing in the checkout was mutated.
