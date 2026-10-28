# Mo59Scribe50 — LOG.md round-59 entry draft (skeleton)

Seat: `Mo59Scribe50` (scribe) · wave `mori-r59-w1` · report dir `.ufo/waves/round-59/w1`.
Mode: read-only. No edits to product files, corpus, registry, `SCORECARD.md`, `LOG.md`, lane VCS, fleet or
sibling repos. No spawns, no `agent://all`, no installs, no pacman. Scratch
`/fast/scratch/hyaku/mori-r59/Mo59Scribe50` created and removed before yield. Nothing here is a corpus edit;
the section in §3 is a paste-ready draft for the integrating seat, not a landed change.

Every claim below is either (a) read from a committed byte I name, or (b) my own read-only command with its
output quoted. Unobserved post-wave values appear only as `⟨SLOT⟩` with the exact source that must fill them.

---

## 1. Inputs read (exact paths)

| File | Note |
|---|---|
| `.ufo/waves/round-59/contract.md` | frozen contract, 6208 B |
| `.ufo/waves/round-59/count-c1.py` | 277 lines, frozen counter |
| `.ufo/waves/round-59/count-c2.py` | 464 lines, frozen counter |
| `.ufo/waves/round-59/evidence/{c1-at-freeze,c2-at-freeze,control-c1-do-nothing,control-c2-do-nothing,selftests,census-start}.txt` | committed receipts |
| `.ufo/waves/round-59/fixtures-c1/f01…f13/expect.txt` | 13 frozen hostile trees |
| `.ufo/waves/round-59/trees-c2/t01…t12/expect.txt` | 12 frozen hostile trees |
| `.ufo/waves/round-59/w1-spec.json`, `.ufo/waves/round-59/w1/swarm-registry.json` | roster, 64 items / 64 members |
| `.ufo/waves/round-59/assimilation/quarantine-slice` | 3 rows (S244, S262, S268) |
| `SCORECARD.md:10-15` (axes), `:1951-1953` (active `## Capabilities`) | scores + register pointer |
| `corpus/lessons/round-58-verifier-spotcheck.md` §Routed defects for round 59 | routed items 1–5 |
| `LOG.md` (rounds 54–58 sections) | house style of the entry being drafted |

## 2. Verified facts (commands + outputs)

### 2.1 Revision chain

```
$ git rev-parse HEAD
8ff344ff18924c1ea63d46c3b3969f9fea05bc51        # "round-59: validated w1 dispatch payload (64 seats, v2)"
$ git log -1 --format='%H %ci %s' 60b3a76ad0524c8978cc51922940be1c8c388915
60b3a76ad0524c8978cc51922940be1c8c388915  2026-10-28 02:50:48 -0300  round-59: freeze amendment — counter
   scratch-mkdir + ls-tree rev:path + register name boundary; pre-data
$ git log -1 --format='%H %ci %s' 2b9f03975bfb6e508f35074ac8181ec8bf54e805
2b9f03975bfb6e508f35074ac8181ec8bf54e805  2026-10-27 16:36:43 -0300  round-58 verifier spot-check
   (integrator, hyaku): non-author admit/reject
$ git merge-base --is-ancestor 2b9f0397 60b3a76 && echo OK   → entering<freeze OK
$ git merge-base --is-ancestor 60b3a76 8ff344ff && echo OK   → freeze<HEAD OK
$ git log --oneline 60b3a76..HEAD
8ff344ff round-59: validated w1 dispatch payload (64 seats, v2)
```

### 2.2 Frozen bytes are undrifted

```
$ git show 60b3a76:path | sha256sum           # freeze blob
contract.md   427fca0bf2a928133c09b37746e58a2d98c6c551651046f31320531a43de107e
count-c1.py   2be6fda8c54633fd96f9d447e8e78ff4ba4a6d6136670f79a9d622003f0c9dfd
count-c2.py   2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be
$ sha256sum <same paths in working tree>      # identical, byte for byte
$ git diff --stat 60b3a76 HEAD -- <contract, both counters, fixtures-c1, trees-c2>
(empty)
```

Tool pins resolved at the freeze rev and equal to the contract prefixes:

```
$ git show 60b3a76:tools/mori-register-check.py    | sha256sum
38b733d896f880f5b7ecb464848b80798810ab052fcf0a8afb320918151472b8   # contract "38b733d8…472b8"
$ git show 60b3a76:tools/mori-settlement-scan.py   | sha256sum
4c04bf2170b0484192dd157ee04851e8243e030c54046c5e8806d46eea5ac9a9   # contract "4c04bf21…5ac9a9"
```

Fixture/tree counts at the freeze rev: `git ls-tree 60b3a76:.ufo/waves/round-59/fixtures-c1/ | wc -l` → `13`;
`…trees-c2/ | wc -l` → `12`.

### 2.3 Captured measurement receipts (committed bytes, quoted verbatim)

`evidence/c1-at-freeze.txt` (header: "at amended-freeze rev 60b3a76…"):
```
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76ad0524c8978cc51922940be1c8c388915
rc=0
```

`evidence/c2-at-freeze.txt`:
```
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=60b3a76ad0524c8978cc51922940be1c8c388915 failed=copy_absent:corpus/evidence/sources-r59/w1-results-r54.json,corpus/evidence/sources-r59/w1-results-r55.json,corpus/evidence/sources-r59/w1-results-r56.json,corpus/evidence/sources-r59/w1-results-r57.json,corpus/evidence/sources-r59/w1-results-r58.json,corpus/evidence/sources-r59/w1-settlement-r58.json,entry_absent,tree
rc=1
```

`evidence/control-c1-do-nothing.txt` / `control-c2-do-nothing.txt` (entering rev `2b9f0397`):
```
C1=unmet selftest=bad fixtures=bad real=bad pointers=bad rev=2b9f03975bfb6e508f35074ac8181ec8bf54e805 failed=tool_absent,selftest,fixtures_absent,real,pointers
rc=1
C2=unmet selftest=bad scan=bad drift=bad trees=bad entry=bad rows=bad pins=bad tree=bad claims=0 files=0 rev=2b9f03975bfb6e508f35074ac8181ec8bf54e805 failed=copy_absent:corpus/evidence/sources-r59/w1-results-r54.json,corpus/evidence/sources-r59/w1-results-r55.json,corpus/evidence/sources-r59/w1-results-r56.json,corpus/evidence/sources-r59/w1-results-r57.json,corpus/evidence/sources-r59/w1-results-r58.json,corpus/evidence/sources-r59/w1-settlement-r58.json,drift,entry_absent,scan,selftest,tool_absent,tree,trees,trees_absent
rc=1
```

`evidence/selftests.txt` (TMPDIR=`/fast/scratch/hyaku/mori-r59/L1`):
```
C1_SELFTEST pass=6 fail=0
c1 rc=0
C2_SELFTEST pass=9 fail=0
c2 rc=0
REGCHECK_SELFTEST pass=12 fail=0
tool1 rc=0
SETSCAN_SELFTEST pass=10 fail=0
tool2 rc=0
```

### 2.4 Predicate targets, as emitted by the counters

`count-c1.py:239-273` prints exactly `C1=<met|unmet> selftest=<ok|bad> fixtures=<ok|bad> real=<ok|bad>
pointers=<ok|bad> rev=<R>` (+ ` failed=…` when unmet) — the contract's target token list is therefore emitted
verbatim by the counting command (this addresses the target-token clause of round-58 routed defect 3).
`count-c2.py:430-460` prints `C2=… selftest scan drift trees entry rows pins tree claims=N files=F rev=<R>`.

Frozen hostile expectations (concatenated `expect.txt` per tree, `tr '\n' ' '`):

| C1 fixture | expect | C2 tree | expect |
|---|---|---|---|
| f01-stub-only | `binding` | t01-no-frontmatter | `frontmatter` |
| f02-two-declared | `binding` | t02-dup-k | `distinct` |
| f03-dup-key | `keys` | t03-quote-wrong-line | `span` |
| f04-missing-key | `keys` | t04-stale-pin | `pin` |
| f05-pointer-missing | `pointers` | t05-few-claims | `claims_min` |
| f06-pointer-absolute | `pointers` | t06-outside-file | `files` |
| f07-pointer-relative-parent | `pointers` | t07-no-row | `rows:missing` |
| f08-manifest-name-altered | `manifest:name` | t08-extra-cell-row | `rows:bad_row` |
| f09-manifest-substring-only | `manifest:name` | t09-usedby-other | `rows:usedby` |
| f10-manifest-foreign-lane | `manifest:lane` | t10-queued-status | `rows:status` |
| f11-manifest-wrong-index | `manifest` | t11-quote-short | `span` |
| f12-lane-round-mismatch | `manifest:lane_round` | t12-malformed-claim | `grammar` |
| f13-empty-pointer | `pointers` | | |

### 2.5 Wave shape (contract + spec + registry agree)

```
$ python3 -c "…Counter(role)…" .ufo/waves/round-59/w1-spec.json
items 64
reviewer 20, critic 10, mutation-tester 8, executor 8, scribe 4, scout 4,
revenger 4, connector 2, sentinel 2, simplifier 2        # w1/swarm-registry.json: members 64, same counts
```
Attack = reviewer+critic+mutation-tester+sentinel = **40/64 (62.5 %)**, matching contract "40/64"; policy v2
band 64–128 satisfied. Report dir `.ufo/waves/round-59/w1`; `w1-dispatch.json`, `w1-spec.json`, `w1.ready`
committed at `8ff344ff`; `w1.ready.dispatched` untracked at report time.

### 2.6 Frontier baseline

```
$ grep -cE '^\s{0,3}\|\s*S[0-9]{3,}\s*\|' corpus/SOURCES.md      → 325      (at 8ff344ff)
$ grep -c '^mori	W04' .ufo/waves/round-59/evidence/census-start.txt → 25
$ tail -1 …/census-start.txt  → mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

Score row at `8ff344ff` (`SCORECARD.md:10-15`): coverage 6, operability 7, depth 5, freshness 5,
calibration 5, adjacency 6 — consistent with the contract's "C1 score 5, tied lowest non-retired" / "C2 score 5".

`corpus/lessons/round-59.md` does not exist and `LOG.md` has no `## Round 59` heading (`grep -n "Round 59"
LOG.md` → no output); at this seat's read, `.ufo/waves/round-59/w1/` held only `swarm-registry.json` (peer
reports have appeared since; wave work also shows as untracked paths, see F7).

---

## 3. DRAFT — `LOG.md` round-59 entry (paste-ready skeleton)

Convention used: `⟨SLOT: source⟩` = must be replaced from captured bytes of the named artifact; never retyped
from prose (QUALITY-148/152 class). Everything outside `⟨…⟩` is verified above.

```markdown
## Round 59 — Mori (L1 MoriR59a2): C1 calibration (active register checker) and C2 depth (settlement-artifact scan)

Entering tip `2b9f03975bfb6e508f35074ac8181ec8bf54e805` (round-58 verifier spot-check); amended freeze
`60b3a76ad0524c8978cc51922940be1c8c388915` (initial freeze `ccfd554e…` superseded pre-data by a counter
amendment: scratch-mkdir, `ls-tree rev:path`, register name boundary, tool PIN); validated dispatch
`8ff344ff18924c1ea63d46c3b3969f9fea05bc51` (one v2 `w1`, 64 seats); data commit `⟨SLOT: measured data rev⟩`;
integration commit `⟨SLOT: integration rev⟩`. Scores entering: coverage 6, operability 7, depth 5,
freshness 5, calibration 5, adjacency 6. C1 targets calibration, C2 targets depth. No scalar score change is
claimed on either axis and no axis-harm claim is made; a no-harm reviewer seat rides the wave. Frozen bytes
(contract `427fca0b…107e`, `count-c1.py` `2be6fda8…dfd`, `count-c2.py` `2df3ae84…7be`) are unchanged
freeze→HEAD (`git diff --stat 60b3a76 HEAD -- .ufo/waves/round-59/{contract.md,count-c1.py,count-c2.py,
fixtures-c1,trees-c2}` empty).

C1 (calibration): `tools/mori-register-check.py` at sha256 `38b733d8…472b8` verifies the two round-56 admitted
capabilities in the ACTIVE register — the unique `## Capabilities` section that self-declares "current
capabilities register" (`SCORECARD.md:1951-1953` at `8ff344ff`), not the superseded `— none yet —` stub — with
unique-register identity, exact key/name/pointer binding, and MANIFEST `rounds[832]` binding at revision-pinned
fleet commit `2807c6ab8a9b04dcf256682bcd722c695fdd6e14`. Counting command
`python3 .ufo/waves/round-59/count-c1.py R [--scratch DIR]`; target
`C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=R`, exit 0. Tool selftest `REGCHECK_SELFTEST pass=12
fail=0`; counter selftest `C1_SELFTEST pass=6 fail=0`. Thirteen committed hostile trees (`f01`–`f13`) must each
score UNMET covering its frozen expect prefix (`binding`, `keys`, `pointers`, `manifest:name`, `manifest:lane`,
`manifest`, `manifest:lane_round`). Kill rule: any post-freeze change to counter bytes, contract bytes, the
predicate sentence or the target output invalidates the claim.

C2 (depth): `tools/mori-settlement-scan.py` at sha256 `4c04bf21…5ac9a9` validates orchestrator
`*-results.json` settlement artifacts (object/`seats`==`members`/member key-set/name-unique/role enum;
verdict `SETTLEMENT_SCAN_OK` or `FAIL`), and the new entry
`corpus/knowledge/wave-settlement-artifacts-r59.md` carries ≥10 byte-exact pin-bound claims
(`Quote: <q> (<copy>:line:<n>|offset:<n>; pin <sha64>)`) over ≥3 distinct artifacts, with all six copies in
`corpus/evidence/sources-r59/` byte-equal to their named `.ufo` artifacts at R, plus mined registry rows whose
`used-by` is exactly the entry. Counting command `python3 .ufo/waves/round-59/count-c2.py R [--scratch DIR]`;
target `C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=N files=F rev=R`
(N≥10, F≥3), exit 0. Tool selftest `SETSCAN_SELFTEST pass=10 fail=0`; counter selftest `C2_SELFTEST pass=9
fail=0`. Scan arm: the five r54–r58 wave-results files scan OK with `members==seats`; the r53 file scans FAIL
(`report_file` extra keys — schema drift, reported not fixed). Twelve committed hostile trees (`t01`–`t12`) must
each evaluate UNMET covering its frozen expect prefix. Sourced-claim rule: the entry cites only S### rows opened
this round (one per cited artifact copy; a ≥1 admit / ≥1 reject Gate pair lands in the round-59 lesson).

Controlled (§9 do-nothing, at entering `2b9f0397`): both counters UNMET, exit 1 —
`C1=unmet selftest=bad fixtures=bad real=bad pointers=bad … failed=tool_absent,selftest,fixtures_absent,real,
pointers` and `C2=unmet … failed=tool_absent,…,trees_absent` (`evidence/control-c1-do-nothing.txt`,
`evidence/control-c2-do-nothing.txt`). The C1 do-nothing arm is met-proof through the tool/fixture/pointer arms,
not through row absence: the two register rows pre-exist since round 57. Selftests captured in
`evidence/selftests.txt` (6/0, 9/0, 12/0, 10/0, all rc 0).

Measured at `⟨SLOT: data rev⟩`: `⟨SLOT: verbatim C1 line from the data-rev receipt⟩`;
`⟨SLOT: verbatim C2 line from the data-rev receipt⟩`. At the amended freeze itself the two lines are
`C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76ad0524c8978cc51922940be1c8c388915`
(rc 0) and `C2=unmet … claims=0 files=0 … failed=<6×copy_absent>,entry_absent,tree`
(rc 1), because the C2 entry, copies and rows land only during the wave.

Wave: one v2 `w1`, 64 seats: reviewer 20, critic 10, mutation-tester 8, executor 8, scribe 4, scout 4,
revenger 4, connector 2, sentinel 2, simplifier 2; attack roles (reviewer+critic+mutation-tester+sentinel)
40/64. L1 held the canonical planner seat; connector items carried bounded sibling-overlap/planning walks
because `planner` is not a validator role (orchestrator ruling 2026-10-19). `⟨SLOT: settlement receipt — reports
present/missing from w1-results.json; no status/error field exists, so absent reports are not called dead⟩`.

Frontier: census start `evidence/census-start.txt` (25 W04 lines, `mori ok …/SOURCES.md`), registry 325 rows at
`8ff344ff`; end `⟨SLOT: census-end receipt, exit 0 required⟩`, rows `⟨SLOT: n⟩`. New rows: `⟨SLOT: S### list,
one per cited artifact copy, plus the admit/reject Gate pair⟩`. Assimilation: none
`⟨SLOT: confirm or replace from the sweep receipt⟩`. Quarantine slice: S244/S262/S268 re-derived at round time
and hand-checked in `corpus/lessons/round-59.md`; prior verdicts: S244 unverifiable
(`corpus/lessons/round-58.md:30`; `corpus/lessons/round-57.md:45` records only an arXiv carrier with no
quarantine quote or locator), S262 and S268 PRESENT (`corpus/lessons/round-57.md:46-47`); the slice file's "the cited source could not be fetched" is
the register's historical prose class, not a current verdict. considerthese: `⟨SLOT: at most one still-
unimplemented proposal from considerthese/2026-10-26.md, or "none taken"⟩`.

Mistakes `⟨SLOT: corpus/lessons/round-59.md M-rows and QUALITY criteria; routed round-58 defects 1–4 status⟩`.
Tool installations/updates: none; pacman paused host-wide, not run. L0: `⟨SLOT: none, or the committed
question⟩`. Stale-lane: respawn-per-round; no other mori mission open.
```

---

## 4. Findings for the integrating seat (drafting hazards, not defects)

- **F1 — C2 is UNMET at the amended freeze, and that is correct.** `evidence/c2-at-freeze.txt` says
  `entry=bad rows=bad pins=bad tree=bad claims=0 files=0` with six `copy_absent` reasons: the entry, its copies
  and its rows are wave output. A LOG sentence pairing "at freeze: C1=met, C2=met" would be unsupported; the
  met line may only be quoted from the data-rev receipt. The draft above keeps both lines explicit.
- **F2 — tree arm is wider than the claim's file minimum.** The claim is ≥3 cited artifacts, but
  `count-c2.py:55` (`ARTIFACTS`, 6 entries) requires *all six* copies present and byte-equal at R (5
  wave-results + `w1-settlement-r58.json`). The draft states six copies and F≥3 citations separately.
- **F3 — `rows` arm scope is first-ten-lines.** `eval_entry` collects `source: S###` only from `lines[:10]`
  (`count-c2.py:112,171-188`) and demands 11 cells, `cells[7]=="mined"`, `cells[10]==ENTRY` exactly. The LOG must
  not describe row coverage more broadly than that, and the entry's frontmatter must carry the ids inside 10
  lines.
- **F4 — census receipt carries no exit code and no row count.** `census-start.txt` ends with `mori ok <path>`,
  25 W04 lines; the "325 rows" figure is my own `grep -cE` at `8ff344ff`, not a census-output byte. It should
  be labelled as a counted value, and the round-end row count must come from the captured end receipt
  (QUALITY-148/152 retyped-prose class).
- **F5 — receipt commit placement.** `evidence/{c1,c2}-at-freeze.txt` were added at `8ff344ff` (measured at
  `60b3a76`, committed with the dispatch payload); `evidence/{control-*,selftests,census-start}.txt` were added
  at `ccfd554e` and are unchanged since. The freeze commit `60b3a76` alone does not contain the two "at-freeze"
  receipts; cite the commit that holds the bytes.
- **F6 — quarantine slice text vs lane verdicts.** `.ufo/waves/round-59/assimilation/quarantine-slice` lists
  S244/S262/S268 with "the cited source could not be fetched, so no quote was checked", while
  `corpus/lessons/round-57.md:46-47` records S262 and S268 PRESENT on the IEEE full text, `:45` records an
  arXiv carrier for S244, and `corpus/lessons/round-58.md:30` records S244 unverifiable (its quarantine row
  names no quote or locator, so its cited payload cannot be checked).
  Reported verbatim; the draft attributes verdicts to the round-59 re-derivation rather than restating the class.
- **F7 — nothing has been scored yet.** No `corpus/lessons/round-59.md`, no `## Round 59` in `LOG.md`, no
  data/integration commit. At this seat's read `w1/` held only `swarm-registry.json`; peer reports and the
  C2 surfaces (`corpus/evidence/sources-r59/`, `corpus/knowledge/wave-settlement-artifacts-r59.md`) now appear
  as untracked wave work — uncommitted and unscored, so no measured line can be quoted from them. Every
  `⟨SLOT⟩` is deliberate: the entry cannot be completed from context.
- **F8 — roster agreement is exact.** `w1-spec.json` (64 items) and `w1/swarm-registry.json` (64 members) show
  identical role counts; attack share 40/64 matches the contract's figure and the 25 % floor.
- **F9 — two selftest numbers, do not conflate.** Tool-level pins are `REGCHECK_SELFTEST pass=12 fail=0` and
  `SETSCAN_SELFTEST pass=10 fail=0`; counter-level are `C1_SELFTEST pass=6 fail=0` and `C2_SELFTEST pass=9
  fail=0`. The contract quotes the counter-level pair for `--selftest` and both appear in
  `evidence/selftests.txt`.

## 5. Limits

- No counter was re-executed by this seat: the freeze/control/selftest numbers above are the committed receipts'
  bytes, not my runs. `--selftest`/`--scratch` behavior is read from `count-c1.py:214-273` and
  `count-c2.py:365-460`, not exercised.
- The tool-level fixtures/selftests (`tools/mori-register-check.py`, `tools/mori-settlement-scan.py`) were not
  inspected line by line; my statements about them are the pins, the contract predicates and the receipts.
- Post-wave values are unknown to this seat by design; §3 leaves them as slots with named sources.
- Report-only: no corpus registry, `SCORECARD.md`, `LOG.md`, lesson, product or VCS write; no remediation.

## 6. Out of scope (not done)

Product/corpus edits; registry or SCORECARD/LOG landing; counter or fixture mutation; running the lane's
counters at the data rev (does not exist yet); census end run; pytest/lint/build (none applicable); installs.
