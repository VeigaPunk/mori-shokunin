# ExecScorecardRows — the two new capability rows: resolution and key uniqueness

Item attacked: the two capability rows added by round 37 in the
`Capabilities register — rows demonstrated running this round` table,
`SCORECARD.md:2058` (key `round-37 C1`) and `SCORECARD.md:2059` (key `round-37 C2`).
Question: does each cited evidence path exist, does each named receipt print the verdict the
row claims, and is each key cell unique in the register.

Two bases, because the wave is in flight and the lane tip moved under me:

- **scored tip** `e57c58b57c025364e79d130fbdf764d2674d83d6` — the revision the round-37
  measured outcome names (`SCORECARD.md:2061`) and the tip under attack in the wave contract.
- **lane tip measured here** `e33bb561712b32f46861362a3fa43762fa70ae4f`
  (`git rev-parse HEAD`, taken at measurement time; HEAD advanced three times during the seat:
  `1ae1d6d` → `4bfa049` → `afc55a76` → `e33bb561`).

The two rows are byte-identical at both bases (same text, same evidence cells):

```
$ git show e57c58b5:SCORECARD.md | grep -n 'round-37 C'
2058:| round-37 C1 | real-arm challenge counter | ... | `.ufo/waves/round-37/count-c1.py`; `evidence/c1-after.txt`; fixtures under `.ufo/waves/round-37/fixtures/` | 37 |
2059:| round-37 C2 | source-drift re-fetch probe | ... | `tools/mori-source-drift.py`; `.ufo/waves/round-37/evidence/c2-after.txt`; `evidence/drift-live-r37.txt` | 37 |
```

---

## Row 1 — `round-37 C1` (SCORECARD.md:2058), "real-arm challenge counter"

Row claim (what it can now do): the counter "rejects a real-arm memoizer and a summary-only
printer while the honest gate passes".

### Evidence paths

| cited path | base as written | at scored tip `e57c58b5` | at lane tip `e33bb561` |
|---|---|---|---|
| `.ufo/waves/round-37/count-c1.py` | repo-relative | EXISTS (blob `7518fef8…`, = freeze pin) | EXISTS (blob `3e15f9fd…`, v2 amendment) |
| `evidence/c1-after.txt` | wave-relative | **MISSING** | exists as `.ufo/waves/round-37/evidence/c1-after.txt` |
| `fixtures under .ufo/waves/round-37/fixtures/` | repo-relative dir | EXISTS — `const.py`, `memo-n1.py`, `summary-only.py` (all three blobs = freeze pins) | same |

```
$ for rev in e57c58b5 1ae1d6d; do echo "=== $rev ==="; for p in .ufo/waves/round-37/count-c1.py \
  .ufo/waves/round-37/evidence/c1-after.txt .ufo/waves/round-37/fixtures/const.py \
  .ufo/waves/round-37/fixtures/memo-n1.py .ufo/waves/round-37/fixtures/summary-only.py \
  tools/mori-source-drift.py .ufo/waves/round-37/evidence/c2-after.txt \
  .ufo/waves/round-37/evidence/drift-live-r37.txt; do
  git cat-file -e "$rev:$p" 2>/dev/null && echo "EXISTS $p" || echo "MISSING $p"; done; done
=== e57c58b5 ===
EXISTS .ufo/waves/round-37/count-c1.py
MISSING .ufo/waves/round-37/evidence/c1-after.txt
EXISTS .ufo/waves/round-37/fixtures/const.py
EXISTS .ufo/waves/round-37/fixtures/memo-n1.py
EXISTS .ufo/waves/round-37/fixtures/summary-only.py
EXISTS tools/mori-source-drift.py
MISSING .ufo/waves/round-37/evidence/c2-after.txt
EXISTS .ufo/waves/round-37/evidence/drift-live-r37.txt
=== 1ae1d6d ===   (all eight EXISTS)
```

`evidence/c1-after.txt` is also absent under a repo-root base at every revision — the repo has
no top-level `evidence/` directory (`[ -d evidence ]` → `ROOT evidence/ MISSING`). It resolves
only wave-relative.

### Does the receipt print the claimed verdict?

Yes, at the tip where it exists. `.ufo/waves/round-37/evidence/c1-after.txt` (unchanged from
`bcf6550` to `e33bb561`):

```
4:blind arm: 24/24 sandbox histories matched the hidden truth (1.8s; coverage: deletions=19 changed-back=17 superseded=10)
5:real arm: pass (0.3s)
9:challenge arm (real-arm clothing): pass (0.1s)
12:negative memo-n1.py     rejected (challenge: lists differ: ...)
13:negative const.py       rejected (blind 4/4 (repo200: lists differ))
14:negative summary-only.py rejected (blind 3/4 (repo200: per-id lines differ (malformed=0)))
15:C1=met
17:EXIT=0
```

That is exactly the row's claim: memoizer and summary-only printer rejected, honest gate
(real + challenge arms, 24/24 blind) passing. `command: python3 .ufo/waves/round-37/count-c1.py e57c58b5`
is the receipt's recorded provenance.

The row's cited counter also still prints the claimed verdict at the scored tip under the
amended (v2) bytes now committed at the tip:

```
$ timeout 900 python3 .ufo/waves/round-37/count-c1.py e57c58b5   # tip counter, blob 3e15f9fd
...
negative memo-n1.py     rejected (challenge: lists differ: ...)
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 4/4 (repo200: per-id lines differ (malformed=0)))
C1=met
seed=13416093612133834278
EXIT=0
```

Resolution: **row C1 resolves at the lane tip, does not resolve at the scored tip** (receipt
absent at `e57c58b5`).

---

## Row 2 — `round-37 C2` (SCORECARD.md:2059), "source-drift re-fetch probe"

Row claim: "Re-fetches every registry row with a committed copy and classifies the copy against
today's body under a 4 MiB bounded read and a post-redirect public-destination policy;
`--selftest` 6 cases with two named, mutation-killable arms".

### Evidence paths

| cited path | base as written | at scored tip `e57c58b5` | at lane tip `e33bb561` |
|---|---|---|---|
| `tools/mori-source-drift.py` | repo-relative | EXISTS (blob `162ee87b…`, = freeze pin) | EXISTS (blob `162ee87b…`, unchanged) |
| `.ufo/waves/round-37/evidence/c2-after.txt` | repo-relative | **MISSING** | EXISTS |
| `evidence/drift-live-r37.txt` | wave-relative | exists as `.ufo/waves/round-37/evidence/drift-live-r37.txt` | EXISTS |

Note the cell mixes bases: one repo-relative path and one wave-relative path in the same
evidence list.

### Does the receipt print the claimed verdict?

The counter receipt does (`.ufo/waves/round-37/evidence/c2-after.txt`, unchanged `bcf6550` →
`e33bb561`):

```
1:command: python3 .ufo/waves/round-37/count-c2.py e57c58b5
4:check selftest       PASS (exit=0 arms=[('exit_code','PASS'), ('huge_cap','PASS'), ('missing_sources_exit2','PASS'), ('redirect_private_refused','PASS'), ('row_states','PASS'), ('summary','PASS')])
5:check cap_kill       PASS (exit=1 huge_cap=FAIL)
6:check redirect_kill  PASS (exit=1 redirect_private_refused=FAIL)
7:check knowledge      PASS (present=True rows=['S205','S221','S222','S223','S224','S225'] cited_commit=True)
8:check capability     PASS (rows=1 names_tool=True)
10:check live           PASS (present=True sentence=True)
11:C2=met
12:EXIT=0
```

Six selftest arms with `huge_cap` and `redirect_private_refused` named, each killed by its own
mutation (`cap_kill`, `redirect_kill`) — the row's claim.

The **live** receipt does not print that claim at the scored tip: it covers 220 registry rows
while the registry at `e57c58b5` has 225 rows and S221–S224 have committed copies there:

```
$ git cat-file -p e57c58b5:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} '   → 225
$ git ls-tree -r --name-only e57c58b5 corpus/evidence/sources-r37/
corpus/evidence/sources-r37/S221.src … S224.src          (four committed copies)
$ git cat-file -p e57c58b5:.ufo/waves/round-37/evidence/drift-live-r37.txt | tail -2
MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162
EXIT=1
```

At the lane tip the same receipt is refreshed and does cover them:

```
222:S221 fresh
223:S222 fresh
224:S223 drifted
225:S224 fresh
226:S225 fresh
227:MORI_SOURCE_DRIFT rows=225 fresh=53 excerpt=0 drifted=10 unavailable=0 no-copy=162
```

Resolution: **row C2 resolves at the lane tip; at the scored tip its counter receipt is absent
and its live receipt predates the five rows the same commit opened.**

---

## Key uniqueness

Key cells are unique. Measurement over the committed file at `e33bb561`
(`git show $H:SCORECARD.md`, first table cell, keys matching `rounds[…]` or `round-N CM`):

```
2023: [round-36 C2]
2058: [round-37 C1]
2059: [round-37 C2]
1961-1978: [rounds[313]…rounds[495].capabilities_added[0..2]]   (18 canonical keys, all distinct)
```

21 key cells, 21 distinct values. `round-37 C1` and `round-37 C2` each occur once as a key cell;
their second textual occurrence is prose at `SCORECARD.md:2071`, not a key. No collision with
`round-36 C2` or with the canonical `## Capabilities` register keys, and the canonical register
still binds cleanly at both tips:

```
$ python3 .ufo/waves/round-35/count-c1.py e33bb561712b32f46861362a3fa43762fa70ae4f
label=P-C1 rev=e33bb561712b32f46861362a3fa43762fa70ae4f manifest_rev=37b51a243302 register='## Capabilities' oracle=18 rows=18 matched=18 missing=0 bad=0 extra=0 mismatches=0 C1=met
EXIT=0
```
(same result at `e57c58b5`).

Key uniqueness: **PASS at both bases.**

---

## Defects

**D1 (row resolution at the scored tip) — receipts absent.**
`SCORECARD.md:2058` cites `evidence/c1-after.txt` and `SCORECARD.md:2059` cites
`.ufo/waves/round-37/evidence/c2-after.txt`; neither file exists at the scored tip
`e57c58b5` (table above). Both were added only in `bcf6550`, a descendant
(`git log --oneline --diff-filter=A -- .ufo/waves/round-37/evidence/c1-after.txt` → `bcf6550`).
The round-36 precedent landed the capability row and its receipt in the *same* commit
(`9ca8f2e`, both `SCORECARD.md` row and `evidence/c2-after.txt`); round 37 breaks it. A closure
re-running the counters at `e57c58b5`, as `SCORECARD.md:2061` says was done, therefore cannot
read either receipt the rows cite.

**D2 (path base) — two conventions in one table.**
`SCORECARD.md:2058` and `:2059` mix bases: `.ufo/waves/round-37/evidence/c2-after.txt` is
repo-relative, `evidence/c1-after.txt` and `evidence/drift-live-r37.txt` are wave-relative.
Under a repo-root base (the base the canonical register uses — r35 P-C1: evidence "exists at the
measured revision" as a whole path under `tools/`, `corpus/knowledge/`, `corpus/evidence/`), 2 of
the 6 cited paths fail at every revision. The round-36 row (`SCORECARD.md:2023`) uses the bare
form too, so this is a lane-wide convention, but a *single cell* carrying both bases is new.
Commit `5631efa` ("receipt erratum (commands + repo-relative paths)") normalised receipt paths
and did not touch these two cells (`git show 5631efa -- SCORECARD.md | grep 'round-37 C'` → no
hunks).

**D3 (stale live receipt at the scored tip).**
`.ufo/waves/round-37/evidence/drift-live-r37.txt` at `e57c58b5` reports `rows=220` while
`corpus/SOURCES.md` at that same revision has 225 rows and S221–S224 have committed copies
(`corpus/evidence/sources-r37/S221.src`…`S224.src`, all in `e57c58b5`). The receipt therefore
does not demonstrate the row's "every registry row with a committed copy" at the tip it is cited
against. Both the receipt and the frozen `LIVE_SENTENCE` were later re-based to `rows=225`
(`5631efa`, `count-c2.py` v3).

**D4 (receipt vs tip counter at the scored tip).**
The counter now committed at the tip is amended (`count-c1.py` v2 blob `3e15f9fd` vs frozen
`7518fef8`; `count-c2.py` v3 blob `0eb8ff4` vs frozen `6213cf9a`, both pinned in
`evidence/freeze-r37.txt`). Run against the scored tip, C1 still reproduces (`C1=met`, exit 0),
but C2 does not:

```
$ python3 .ufo/waves/round-37/count-c2.py e57c58b5        # tip counter (v3) at the scored tip
check knowledge      FAIL (present=True rows=[...] cited_commit=False touches_tool=True)
check live           FAIL (present=True sentence=False)
C2=unmet
EXIT=1

$ python3 .ufo/waves/round-37/count-c2.py e33bb561        # tip counter at the lane tip
check knowledge      PASS (... cited_commit=True touches_tool=True)
check live           PASS (present=True sentence=True)
C2=met
EXIT=0
```

Cause: `corpus/knowledge/source-drift-hardening-r37.md` cites `8ff9bba` at `e57c58b5` and
`1caa242` at the tip (`grep -c '8ff9bba'` → 2 at `e57c58b5`, 0 at HEAD; `1caa242` → 0 then 2),
and v3 requires `1caa242`. The row does not name a counter version, so the receipt's
`C2=met` and the tip counter's verdict at the row's revision disagree.

---

## Risks / not defects

- The rows' own claims and receipts are consistent: C1's receipt (line 15) and C2's receipt
  (line 11) print `C1=met` / `C2=met` with `EXIT=0` and the three / two named negatives, which is
  what the row text asserts. D1/D3 are about *revision binding*, not about falsified verdicts.
- Every frozen artifact the rows name matches its freeze pin at the scored tip: `count-c1.py`
  `7518fef8`, `memo-n1.py` `19324701`, `const.py` `2f3993a0`, `summary-only.py` `2d62f742`,
  `tools/mori-source-drift.py` `162ee87b` (= `evidence/freeze-r37.txt`).
- The lane tip is moving while this seat runs (HEAD `1ae1d6d` → `4bfa049` → `afc55a76` →
  `e33bb561`); every measurement above names the sha it used. Re-run the checks at the final
  integration tip before closing.
- No tool was installed or upgraded for this seat (python3 and git only).

VERDICT: FAIL — both rows resolve and both keys are unique at the lane tip `e33bb561`, but at the
scored tip `e57c58b5` the two receipts they cite do not exist (`SCORECARD.md:2058` →
`evidence/c1-after.txt`; `SCORECARD.md:2059` → `.ufo/waves/round-37/evidence/c2-after.txt`), and
the C2 live receipt there (`rows=220`) predates the 225-row registry of that same revision.
