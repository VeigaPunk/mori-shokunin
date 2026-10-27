# Mo58Scribe52 — independent registry census (round 58, committed corpus)

Seat: scribe/census, leaf (no dispatch). Read-only: no production file, corpus,
SCORECARD, LOG, lessons, or lane VCS was modified. No commits, no fleet/sibling writes.

## Frozen inputs and revisions read

| item | value |
|---|---|
| contract | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-58/contract.md` (read in full) |
| counters read | `.ufo/waves/round-58/count-c1.py`, `.ufo/waves/round-58/count-c2.py` (read, not modified; `measure` bodies inspected) |
| freeze rev | `fe8801120a67c1a6b8899d7d0423839caa09e7d0` |
| entering rev | `b783d0b892637ce8d20f188cad20e4d8913ca635` |
| lane working-tree HEAD | `4272736cfc5147586e1543413772f80daf44b04b` ("round-58: freeze validated w1 dispatch payload") |
| census authority | `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (SOURCES-CONTRACT-v1; 11 columns ⇒ `NF=13`) |

`corpus/SOURCES.md` is byte-identical at all three revisions:

```
$ for r in b783d0b8… fe880112… 4272736c…; do git -C <lane> show $r:corpus/SOURCES.md | sha256sum; done
3b40fb637a78f54ea7082f04003ed7d21386f44a6f126420235ebb0b25be5d6e  -
3b40fb637a78f54ea7082f04003ed7d21386f44a6f126420235ebb0b25be5d6e  -
3b40fb637a78f54ea7082f04003ed7d21386f44a6f126420235ebb0b25be5d6e  -
```

So the round-start census target and the freeze content are the same bytes; the
committed registry did not move between entering and freeze.

## Method — four independent derivations (no shared code with the census tool)

Counting rule used for the "manual" passes, stated explicitly because the census
predicate is row-based, not id-based: rows are counted **inside the `## Registry`
section only** (level-2 heading whose text is exactly `Registry`, ≤3 leading
spaces), header row (`| id | …`) and dash-separator rows excluded, every other
`|`-leading row counted.

Path A — purpose-written parser (written from scratch for this seat,
`scribe52_census.py`, neither importing nor copying `sources-census.sh`):

```
$ TMPDIR=<scratch> python3 scribe52_census.py SOURCES.freeze.md
{
  "registry_rows": 322,
  "first_row_line": 7,
  "last_row_line": 329,
  "first_id": "S001",
  "last_id": "S549",
  "tier": {"A": 290, "B": 14, "C": 18, "invalid": 0},
  "status": {"queued": 24, "mined": 270, "rejected": 28, "invalid": 0},
  "tier_sum": 322, "status_sum": 322,
  "nf_not_11": [], "dup_ids": [], "bad_id_format": [],
  "rowshape_outside_registry": {}
}
INTEGRITY ok rows==tier_sum==status_sum 322      # exit 0
```

Path B — hand-written awk histogram over the section's line range, second
independent field-split implementation:

```
$ awk 'NR>=5 && NR<=329' SOURCES.freeze.md | awk -F'|' '…'   # trims cells; skips id header, separator, empty
rows=322 tierA=290 tierB=14 tierC=18 status_queued=24 status_mined=270 status_rejected=28
```

Path C — grep triangulation on the same committed bytes:

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' SOURCES.freeze.md   → 322
$ grep -cE '^\| S[0-9]{3,} \|.*\| A \|' …   → 290
$ grep -cE '^\| S[0-9]{3,} \|.*\| B \|' …   → 14
$ grep -cE '^\| S[0-9]{3,} \|.*\| C \|' …   → 18
$ grep -cE '^\| S[0-9]{3,} \|.*\| mined \| 20' …    → 270
$ grep -cE '^\| S[0-9]{3,} \|.*\| queued \| 20' …   → 24
$ grep -cE '^\| S[0-9]{3,} \|.*\| rejected \| 20' … → 28
```

Path D — fleet tool as a cross-check only (different implementation, run
read-only on the extracted freeze bytes; it writes stdout only):

```
$ bash scripts/sources-census.sh census --file <scratch>/SOURCES.freeze.md; echo exit=$?
file	rows	322
file	tier.A	290
file	tier.B	14
file	tier.C	18
file	status.mined	270
file	status.queued	24
file	status.rejected	28
FLEET	rows	322
FLEET	tier.A	290 / tier.B 14 / tier.C 18 / tier.invalid 0
FLEET	status.queued 24 / status.mined 270 / status.rejected 28 / status.invalid 0
FLEET	missing	0
exit=0
```

All four paths agree. The only disagreement seen during the work was in my own
awk pass, which first counted a blank line and the separator row; both are
parser artefacts of that pass, not registry facts (documented here so the numbers
are auditable).

## Result — round-start census

- **Registry rows (committed, at freeze = entering = dispatch): 322.** Matches the
  contract's round-start census figure.
- **Tier histogram: A = 290, B = 14, C = 18, invalid = 0.**
- **Status histogram: queued = 24, mined = 270, rejected = 28, invalid = 0.**
- Both histograms sum to the row count; no malformed row (every counted row
  splits into 11 cells ⇒ `NF=13` under the contract's pipe split), no duplicate id,
  no bad id format, and **no row-shaped `S###` line outside `## Registry`**
  (`rowshape_outside_registry: {}`).
- Tier × status cross-tab (derived, not claimed by the contract):

  | tier | mined | queued | rejected |
  |---|---|---|---|
  | A | 260 | 22 | 8 |
  | B | 10 | 2 | 2 |
  | C | 0 | 0 | 18 |

  All 18 tier-C rows are `rejected`, so the W01 predicate (tier C mined with a
  used-by) has no candidate at round start.

## Registry shape observations (evidence for reviewers, not a scoring claim)

1. Id space ≠ row count. Ids run `S001`…`S549` over 322 rows: 227 ids are absent
   (earliest gaps start at `S236`; `S241` is present). `S550` does **not** exist at
   the freeze rev.
   Any census that infers the count from the maximum id (549) or from id
   contiguity would be wrong; the row-shape method used here and by the evidence
   file is the correct one.
2. The registry section spans lines 3–330 of the freeze file; data rows occupy
   lines 7–329. A **blank line at line 305 splits the Markdown table** between
   `S525` (line 304) and `S526` (line 306). A section-scoped counter (both the
   fleet tool and my parser) still counts 322 across the split; a strict
   "one contiguous table" reader would see two tables and 322 rows overall.
   Flagged only because the census predicate is section-scoped, not table-scoped.
3. The round-start evidence `.ufo/waves/round-58/evidence/census-start-rows.txt`
   derives 322 with `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` at
   `b783d0b8…`. That grep is **section-blind**; here it happens to be exactly
   correct (whole-file row-shaped count = in-section count = 322, and I verified
   0 row-shaped lines outside `## Registry`), but the method would overcount if a
   row-shaped line ever appeared under `## Search log` / `## Leads`.

## Working-tree contrast (uncommitted state — landed-tip impact)

`git status --porcelain corpus/` at `4272736c…`:

```
 M corpus/README.md
 M corpus/SOURCES.md
?? corpus/evidence/sources-r58/
?? corpus/knowledge/driver-events-r58.md
?? corpus/lessons/round-58.md
```

`corpus/SOURCES.md` diff is `+3` lines: the `S550` registry row, one Search-log
paragraph, and a blank line. Independent re-parse of the working-tree file:

- 323 rows; tier A 291 / B 14 / C 18; mined 271 / queued 24 / rejected 28.
- `S550` row present, 11 cells, `kind=own-work`, `tier=A`, `status=mined`,
  `opened=2026-10-27`, `recheck=90d`,
  `used-by=corpus/knowledge/driver-events-r58.md` — i.e. the round-end 323-row
  expectation and the C2 row shape both hold **in the working tree only**.
- `bash scripts/sources-census.sh census --file <lane>/corpus/SOURCES.md` → 323
  rows, `tier.invalid 0`, `status.invalid 0`, exit 0.
- `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
  → exit 0, W04 warnings only, final line `mori  ok  …/corpus/SOURCES.md`. Diffed
  byte-for-byte against the round-start evidence file `census-start.txt`:
  **IDENTICAL** (S550 introduces no new validator finding).

## Observations handed to reviewers/critics (verbatim, no adjudication)

Read-only counter runs at the dispatch revision (no scoring claim; reviewer,
critic and mutation-tester seats own adjudication):

```
$ python3 .ufo/waves/round-58/count-c1.py 4272736cfc5147586e1543413772f80daf44b04b
C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=4272736cfc5147586e1543413772f80daf44b04b
$ echo $?   → 0
$ python3 .ufo/waves/round-58/count-c2.py 4272736cfc5147586e1543413772f80daf44b04b
C2=unmet entry=absent failed=entry rev=4272736cfc5147586e1543413772f80daf44b04b
$ echo $?   → 1
```

1. **C2 is unmet at every committed revision so far.** `count-c2.py:measure` reads
   the entry, the pinned copy and `corpus/SOURCES.md` via `_show(rev, …)`
   (`git show rev:path`), so untracked files are invisible. The entry, the copy
   `corpus/evidence/sources-r58/mori-driver-liveness.py`, and the `S550` row are
   all currently uncommitted; the rows arm additionally requires
   `cells[8] == "mined"` and the entry path inside `cells[11]`, which the
   working-tree `S550` row does satisfy. Consequence: C2 can only score after a
   commit carries entry + copy + registry row. [INFERENCE from counter source +
   `git status`]
2. **C1 measure output text differs from the contract's stated frozen target
   output.** Contract §C1 target: `C1=met rows=2 pointers=ok manifest=ok
   binding=ok selftest=ok rev=R`. Observed at dispatch rev: `C1=met rows=2
   pointers=ok manifest=ok binding=ok failed=none rev=4272736c…` — the token
   `failed=none` appears and `selftest=ok` does not (the counter exposes selftest
   only in `--selftest` mode, printing `C1_SELFTEST pass=N fail=0`, per its
   `__main__` dispatch). Reported verbatim for the canonical judge; no conclusion
   drawn about the claim, since the kill rule's "target output" wording is
   adjudication, not census.
3. Census contract line "round end (exit 0 required; S550 expected → 323 rows)" is
   satisfied **in the working tree** (323 rows, validate exit 0) and will be
   satisfied at the landed tip only if the `S550` row and the search-log paragraph
   are committed.

## Out of scope / deliberately not done

- No counter selftest runs (`--selftest`), no counter mutation, no control-fixture
  replay: those are the C1/C2 counter seats' and mutation-tester's assignments;
  the frozen counters were read, not exercised beyond the read-only `measure` runs
  above.
- No `corpus/README.md` audit (its `+7` working-tree lines are outside the
  registry census predicate).
- No repo/VCS mutation, no tool installation, no pacman, no subagent dispatch.

## Scratch

Scratch root `/fast/scratch/hyaku/mori-r58/Mo58Scribe52/` (disk guard status read
before work: `/fast/scratch/hyaku` 32% used, 553.5G free; `/tmp` 4% used).
Contents during the seat: `SOURCES.freeze.md` (freeze extraction, sha256
`3b40fb63…`), `scribe52_census.py`, `validate-worktree.txt`. All removed before
yielding; every cited output is reproduced in this report.
