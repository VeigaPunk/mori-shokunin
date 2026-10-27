# Mo55Crit06 — C1 malformed-ledger attack (mori round 55, wave w1)

Seat: Mo55Crit06 (attack/critic, leaf — no dispatch, no subagents).
Assignment: attack the C1 freshness counter's count/hash handling, duplicate/extra/missing-row
detection, and source-row/provenance parsing, using scratch-only fixtures; report evidence +
severity. This seat is a non-voter: no `RECHECK`/`ENTAIL`/`REPLACE`/`QUOTE` lines are emitted.

## Method and bounds

- Frozen counter `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-55/count-c1.py`
  imported read-only via importlib; no repo, git, or jj mutations anywhere.
- Real frozen scope (78 pointers at entering tip `ca52426ea496bc6592e3e867cc9d28843e45f196`)
  and the real committed v7.2/v7.3 copy bytes were read from the lane tree (read-only) so the
  pins arm could pass; every ledger / `corpus/SOURCES.md` row / voter output under test is
  synthetic and lived only in memory.
- Fixtures were executed through the frozen `c1.evaluate(read, rev, read_enter, ls=..., copies=...)`
  entry point — the same code path the scored run uses.
- Scratch: `/fast/scratch/hyaku/mori-r55/Mo55Crit06/` (driver `fixtures.py`, results
  `fixture-results.txt`); removed before yield, so all evidence is quoted inline below.
- Disk guard before work: `/fast/scratch/hyaku` 27% used, 594.2G free — OK. No installs.
  No sysctl/mount/cgroup writes. No production edits.

## Frozen data read (live counter, read-only)

Command: `python3 .ufo/waves/round-55/count-c1.py b8b7064c2b54c8b6b22c288232a96c43fae1af47`
Output: `C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=b8b7064c2b54c8b6b22c288232a96c43fae1af47 failed=votes`
Exit: 1. Matches the seat brief exactly (`w1-results.json` absent at run time, so 0 votes).

## Witness sanity (harness reproduces a passing state)

W0 — synthetic bound two-voter support over the real 78-row scope:
`C1=met scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=78 dissent=0`
Every "MET" below is therefore a genuine acceptance by the frozen counter, not a harness artifact.

## Findings — soundness gaps (counter accepts malformed input)

### F1 (MEDIUM) — rows after the first non-table line are never parsed; phantom tables/rows are invisible to count, hash, duplicate and extra-row checks

Counter code: `parse_ledger` breaks at the first line not starting with `|` once the header and
at least one row exist (`count-c1.py:252-255`); `rows`, `dup` and `extra` are computed only over
that first contiguous block (`count-c1.py:349-353`, gate at `count-c1.py:390`).

- **A1 — phantom second table after a blank line** (3 fabricated 12-hex-hash rows appended in an
  `## Errata` table): `MET ... rows=78 ... voted=78 dissent=0`. Direct count demonstration on the
  same bytes: physical data rows = 81, `parse_ledger` returned 78 — the 3 phantom rows are never
  hashed, counted, status-checked or voted.
- **A2 — phantom duplicate of row 1 with disposition flipped `holds`→`stale`** in a second block:
  `MET ... holds=78 stale=0`. The ledger physically contradicts itself; the counter evaluates only
  the first block.
- **D1 — phantom table inside a ` ``` ` fence after the real table**: `MET ... rows=78`. Fenced
  content is skipped by the same loop, extending the blind spot to fenced dumps.

Impact: the mechanical predicate's "exactly one row for every pointer in SCOPE" is enforced only
within the first table block. An appended errata/corrections table — a plausible authorial shape —
carrying extra or contradictory rows passes `C1=met` with those rows never evaluated. The kill
rule's "missing row" arm is unaffected, but extra/duplicate detection has a structural blind spot.
**Live data is not affected**: the landed ledger is one contiguous 78-row table
(physical = parsed = 78; file ends at line 88, tail bytes `...holds |\n`).
Smallest safe correction: continue scanning after non-table lines (or fail if a pipe-table
restarts later / a second header-matching table appears), and report physical-vs-parsed row counts
so reviewers see any delta.

### F2 (LOW-MEDIUM) — duplicate S-ids in `corpus/SOURCES.md` are silently first-wins; a poisoned duplicate after the good row is never consulted and never flagged

Counter code: `registry()` keeps the first row per S-id (`count-c1.py:113-119`,
`if m and m.group(1) not in rows`); no duplicate detection exists.

- **B0 — poisoned S516 row placed BEFORE the good row**: `unmet ... source_rows=bad` — fails
  closed, but which physical row is authoritative depends on file order alone.
- **B1 — good S516 first, poisoned duplicate (`opened 2026-10-20`) after**: `MET ... source_rows=ok`.
  The poisoned duplicate is dead text the counter never reads and never flags.

Impact: the source-row arm is sound for a single row but blind to registry duplication; conflicting
duplicate rows create a silent alternate authority over pins/opened/used-by. **Live data is clean**:
each of the 11 cited S-ids (S502, S516, S526–S534) occurs exactly once in `corpus/SOURCES.md`
(`grep -c "^| <sid> |"` = 1 for all eleven).
Smallest safe correction: detect duplicate S-ids in `registry()` and add a failing token (or define
last-wins explicitly); surface the conflict either way.

### F3 (LOW) — a header `source:` citation of a nonexistent S-id is harmless and unchecked

- **C1 — header cites used ids plus phantom `S999`**: `MET ... provenance=ok`. Cited ids are only
  checked as a superset over `used_ids` (`count-c1.py:407`); no registry-existence check runs on
  cited ids.

Impact: dead citations in the provenance header go unnoticed and do not affect the mechanical
outcome. Provenance hygiene only.
Smallest safe correction: verify each cited S-id resolves in the registry (warn non-fatally on
unknown ids).

## Fails-closed inventory (attack shapes the counter does reject)

| Fixture | Mutation | Counter output (tail) | Failure class |
|---|---|---|---|
| A3 | one 7-cell row truncated to 6 cells | `rows=78 matched=77 ... failed=line,matched,status,votes` | matched |
| A4 | one hash uppercased | `failed=line,matched,rows,status,votes` | rows+matched |
| A5 | one hash lengthened to 13 hex | `failed=line,matched,rows,status,votes` | rows+matched |
| A6 | duplicate of row 3 appended in-table | `rows=79 ... failed=rows` | rows (dup) |
| A12 | extra row with empty hash cell | `rows=79 ... failed=rows` | rows (extra) |
| A13 | header row repeated inside the table | `rows=79 ... failed=rows` | rows (parsed as data) |
| A14 | last row dropped | `rows=77 matched=77 ... failed=line,matched,rows,status,votes` | matched |
| A15 | pointer cell `342-360, 408-411` (space after comma) | `matched=77 ... failed=line,matched,status,votes` | matched (strict equality vs normalised spec — note for hand-edits) |
| B0 | poisoned duplicate S-row placed first | `failed=source_rows` | source_rows |
| B3 | S-row with 12 cells | `failed=provenance,source_rows` | source_rows (strict `len==11`, `count-c1.py:363`) |
| B4 | used-by space-separated instead of `,`/`;` | `failed=provenance,source_rows` | source_rows (`re.split(r"[,;]")`, `count-c1.py:364`) |
| C2 | used S516 dropped from header citation | `failed=provenance` | provenance |
| D2 | blank line splitting the table after row 38 | `rows=38 ... failed=line,matched,rows,status,votes` | rows (first block only) |
| D3 | one row gains an 8th cell | `rows=78 matched=77 ... failed=line,matched,status,votes` | matched |

Frozen-selftest shapes (missing/extra/duplicate rows, wrong URL/date/status/provenance, bad pins,
unbound/dissenting/fenced votes, last-wins) are reconfirmed by the frozen `--selftest`; this seat
extended them to the edge shapes above.

## Count/hash binding

- `sha256("<entry>|<v7.2 path>|<lines>")[:12]` recomputed over three real scope rows matches the
  ledger hashes exactly (`7b2d297eec60`, `909839af93ac`, `64dc96352472`); the row hash binds
  entry+path+spec and the pointer cell is compared with strict equality, so in-table hash
  substitution or pointer rewrite is caught (A4/A5/A15).
- Scope uniqueness is keyed on `(entry, path, normalised spec)`; scope hash uniqueness is asserted
  by the frozen selftest ("scope hashes unique", pass).

## Live-data hygiene (read-only checks on the landed data)

- `corpus/SOURCES.md`: the 11 cited S-ids each appear exactly once — no live duplicate-authority
  exposure.
- `kernel-v7.3-recheck-r55.md`: single contiguous table, 78 physical = 78 parsed rows, ends at
  line 88 (`...holds |\n`); no phantom content.
- Frozen counter at `b8b7064c`: `provenance=ok source_rows=ok pins=ok` (quoted above).

## Limits

- Fixture voters/outputs are synthetic in-memory objects passed to the frozen `evaluate()`; no lane
  files were written. Vote-binding/quorum internals and all of C2 are outside this seat.
- F1 is a parser-completeness limitation: exploiting it in scoring would still require 16 RECHECK
  voters to ignore a visibly appended table, so practical exploitability is low — but the coded
  predicate does not enforce what its docstring claims over the ledger it accepts.

## Findings

- **MEDIUM — F1 phantom rows/tables outside the first contiguous table block are invisible to
  count/hash/duplicate/extra detection** (A1, A2, D1 all scored MET). Evidence: this report §F1;
  counter `count-c1.py:244-267` (break at 252-255), `count-c1.py:349-353`, gate `count-c1.py:390`.
- **LOW-MEDIUM — F2 duplicate S-ids in `corpus/SOURCES.md` silently first-wins; poisoned later
  duplicate neither consulted nor flagged** (B1 MET; B0 order-dependent fail-closed). Evidence:
  §F2; counter `count-c1.py:113-119`.
- **LOW — F3 header citation of a nonexistent S-id unchecked** (C1 MET). Evidence: §F3; counter
  `count-c1.py:407`.
- No HIGH findings: every in-table mutation attempted (hash case/length, cell-count 6/8, duplicate,
  extra, missing, header repeat, strict pointer string, poisoned-first S-row, 12-cell S-row,
  space-separated used-by, uncited used sid, blank-split table) fails closed with a specific
  `failed=` token (evidence: fails-closed inventory table above).
