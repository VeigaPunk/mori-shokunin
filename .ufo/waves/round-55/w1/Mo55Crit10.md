# Mo55Crit10 — C2 counter/source attack (round 55, wave w1)

Seat: Mo55Crit10 (critic, C2 attack lane). Lane mori-shokunin. Scope: attack the C2
table parser, quote normalization, source-row matching/used-by and source pins;
demonstrate false greens in scratch only. No C1/C2 votes are emitted by this seat
(non-voter); no line in this report starts with a vote keyword.

Frozen references: contract `.ufo/waves/round-55/contract.md`; counter
`.ufo/waves/round-55/count-c2.py` (frozen, unmodified); entry
`corpus/knowledge/disk-runway-enospc-r55.md`; data revision
`b8b7064c2b54c8b6b22c288232a96c43fae1af47`; entering tip
`ca52426ea496bc6592e3e867cc9d28843e45f196`.

## Method

- Read the frozen counter in full (357 lines) and the C2 selftest
  (`.ufo/waves/round-55/checks/selftest-c2.py`), which exercises the counter
  in-process via `evaluate(read, rev, ls=...)` against synthetic file dicts.
- Reused that exact harness pattern in scratch
  (`/fast/scratch/hyaku/mori-r55/Mo55Crit10/attack_driver.py`): loaded the frozen
  counter read-only via importlib, built fixtures from committed bytes
  (`git show b8b7064c:...` for the entry, `corpus/SOURCES.md` and the nine source
  copies), and closed the entailment arm with synthetic scratch ballots attributed
  to frozen voter names Mo55En01/Mo55En02. Those scratch ballots exist only in
  memory inside the fixture; they were never written to `w1/` and are not lane
  votes.
- Disk guard before work: `scripts/hyaku/disk-guard.sh status` exit 0,
  `/fast/scratch/hyaku` 27% used, 594.2G free. No installs. Scratch removed at yield.

## Baseline evidence (commands and observed output)

1. Pin check on the nine committed copies at the data revision — all match the
   frozen digests in `count-c2.py` `COPIES` (command: `sha256sum` over
   `corpus/evidence/sources-r55/{errno-base.h.v7.3,statfs.c.v7.3,xfs_super.c.v7.3,
   btrfs_super.c.v7.3,btrfs_sysfs.c.v7.3,tmpfs.rst.v7.3,statfs.2.man-pages-6.19,
   statvfs.3.man-pages-6.19,coreutils.texi.v9.12}`; observed: nine hashes identical
   to the frozen table; exit 0).
2. Counter at entering tip:
   `python3 .ufo/waves/round-55/count-c2.py ca52426ea496bc6592e3e867cc9d28843e45f196`
   → `C2=unmet claims=0 ... failed=entry_absent,pins`, exit 1 (matches contract "before" state).
3. Counter at data revision:
   `python3 .ufo/waves/round-55/count-c2.py b8b7064c2b54c8b6b22c288232a96c43fae1af47`
   → `C2=unmet claims=23 located=23 quote_missing=0 bad_rows=0 sources=9
   source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 ... failed=entailment`, exit 1.
   Mechanical arms fully green; the arm still open is entailment (votes in flight
   in w1; `w1-results.json` not yet present at the time of reading).
4. Harness honesty witness (fixture = frozen entry + frozen SOURCES + honest
   bound scratch ballots): counter returned
   `C2=met claims=23 located=23 ... entailed=23 dissent=0`. The fixture wiring is
   faithful.

Observation (not a defect): the lane working tree is dirty
(`SCORECARD.md`, `corpus/QUALITY.md`, the r55 knowledge entry, round-54/55 lesson
files modified; `.ufo/waves/round-55/w1/` untracked). The counter reads committed
state via `git show R:path`, so scoring is pinned to the committed revision and is
unaffected by the dirty tree.

## Attack results (all demonstrated in scratch only)

Attack IDs below reference the driver log kept in scratch during the run; the
counter output lines are quoted verbatim inline.

### A1 — first-table-wins decoy (table parser)

`parse_claims` (count-c2.py:111-130) latches the first `claim|source|quote`
header, consumes pipe rows, and `break`s at the first non-pipe line once any row
was seen (count-c2.py:121). Fixture: the frozen front-matter followed by a 16-row
mechanically-valid hollow decoy table, a blank line, then the real frozen 23-row
table. Ballots bound only for the decoy rows' hashes. Counter output:
`C2=met claims=16 located=16 quote_missing=0 bad_rows=0 sources=7 source_rows=ok
pins=ok provenance=ok entailed=16 dissent=0`. FALSE GREEN: the entry's actual
23-row knowledge table was never read; the decoy was certified instead. Root
cause: the arm validates the first markdown table, not the entry's claim table.

### A2 — silent blank-line truncation (table parser)

Fixture: frozen entry with one blank line inserted after the 16th claim row. The
same `break` at count-c2.py:121 drops rows 17-23 with no signal — they are not
counted as bad, missing, or dissent. Document still visually presents 23 rows.
Counter output: `C2=met claims=16 located=16 ... entailed=16 dissent=0`.
FALSE GREEN: certified scope is 16 rows while the table presents 23; seven rows
silently escaped every mechanical arm (parser silently shrinks the checked set).

### A3 — fenced rows skipped (table parser / fence handling)

Fixture: rows 17-23 wrapped in a fenced block. `parse_claims` toggles on fences
(count-c2.py:115) and skips fenced lines entirely. Counter output:
`C2=met claims=16 located=16 ... entailed=16 dissent=0`. FALSE GREEN, same class
as A2: fence status is a second silent-drop path for table rows.

### A4 — source-row URL substring pinning (source matching)

The row→URL match is a bare substring test `if u in srow[1]` (count-c2.py:248),
and `row_ok` then requires only `srow[7]=="mined"`, opened date in `OPENED`
(count-c2.py:52), and used-by membership (count-c2.py:253). Fixture 4a: the real
S537 row with `?h=v7.3` suffixed to `?h=v7.3&provenance=attacker`. Counter
output: `C2=met claims=23 located=23 ... pins=ok provenance=ok entailed=23
dissent=0`. Fixture 4b: S537 URL cell rewritten to a foreign host that merely
embeds the canonical URL
(`https://mirror.invalid/hosted/?u=<canonical xfs_super.c URL>`); the row still
pins to the canonical copy and every quote still locates. FALSE GREEN: a source
row claiming a different origin is certified as one of the nine frozen sources;
quote location is then checked against the frozen copy, not the URL the row
actually names. Identity of the pinned source is not verified.

Real-data disposition: for each of S535-S543 the canonical URL is cell-terminal
in `corpus/SOURCES.md` (trailing text after the URL within the cell: empty for
all nine rows; driver check `all-real-urls-terminal=True`). The landed rows name
exactly the frozen URLs, so the landed data does not exploit this hole; the hole
is in the rule.

### A5 — located quote, negated semantics (quote normalization / location)

The located arm is exact substring on whitespace-collapsed copy text
(`q in norm[url]`, count-c2.py:257; `normalise_text` collapses whitespace only).
Fixture: a new first row whose claim asserts the opposite of the statvfs.3 source
("Filesystems reserve inodes for the superuser ..."), paired with a 6-25-word
quote that exists verbatim in the copy and even contains the source's own
correction ("This is not an issue, since no filesystems with an inode root
reservation exist."). Mechanically the row passes every gate (quote located,
beyond-quote words 9 ≥ 3, 16 words ≥ 6). Counter output:
`C2=met claims=23 located=23 ... entailed=23 dissent=0`. FALSE GREEN: the
located arm cannot see negation or context; located-ness proves the words exist,
not that they support the claim. The counter docstring itself disclaims this
("a located quote proves the quoted words exist in the copy"), so this is a
calibration limit, not a contract violation.

### A6 — entailment output binding is substring-only (vote binding)

The binding check is a raw substring test on the orchestrator-captured output:
`("ENTAIL %s %s" % (h, kind)) in out` (count-c2.py:169), after only a `\\n`
unescape. Fixture: voter Mo55En01's report carries the genuine entailed lines,
but the captured `output` string contains the first vote line solely inside a
`#`-prefixed comment (`# ENTAIL <h> entailed`); voter Mo55En02 is bound honestly.
Counter output: `C2=met claims=23 ... entailed=23 dissent=0`. FALSE GREEN: a
captured-output string that merely contains the vote token — commented, fenced,
or embedded in a longer token — satisfies the binding. The report side is
fence-aware (count-c2.py:164); the output side is not. The docstring disclaims
the depth of this binding ("the results binding proves the orchestrator recorded
... not who wrote the report's bytes"), so this is a trust-boundary looseness
rather than a full break.

### Control — pins arm fails closed (positive control)

Fixture: one byte appended to `errno-base.h.v7.3`. Counter output:
`C2=unmet ... pins=bad ... failed=entailment,pins`. The pin arm (sha256 of the
committed copy vs the frozen digest, count-copies loop in `evaluate`) has no
false-green path among the attacks tried; a mutated, missing, or symlinked copy
all fail closed. Not a finding.

## Smallest safe corrections (proposed, not applied — counter is frozen)

- A1/A2/A3: make the parser fail closed on dropped rows — e.g. count every
  pipe-row between the claim header and the next section heading and treat any
  non-separator row that is not consumed as a claim as `bad`, and reject a
  document whose first table ends before the section ends. Minimum viable change:
  remove the silent `break` (count-c2.py:121) in favor of paragraph-aware
  continuation, or emit `failed=table_truncated` when a later `claim|source|quote`
  table exists that was ignored.
- A4: replace the substring test at count-c2.py:248 with an anchored equality
  check after splitting the title prefix (e.g. require the cell to end with the
  canonical URL, or match `re.escape(u) + r'\s*$'`). Preserves real-data behavior
  (all nine real URLs are cell-terminal) and closes suffix/wrapper forgery.
- A6: bind on full-line anchored match in the output, e.g.
  `re.search(r'(?m)^\s*' + re.escape("ENTAIL %s %s" % (h, kind)) + r'\s*$', out)`,
  mirroring the report-side `ENTAIL_RE` discipline.
- A5: no counter change possible without semantic analysis; keep the disclaimer
  and rely on the two-voter entailment arm — noted as residual risk.

## Findings

- HIGH (counter soundness) — A1 decoy table: counter certifies the first table
  only; the entry's real claim table can go entirely unvalidated while C2 reads
  met. Evidence: count-c2.py:111-130 (parse_claims), :121 (break); driver log
  section ATTACK-1 (counter line `C2=met claims=16 ...` with the real 23-row
  table present but ignored).
- MEDIUM — A2 blank-line truncation: scope silently shrinks to the rows above
  the first gap; document presents more rows than were checked. Evidence:
  count-c2.py:121; driver ATTACK-2 (`C2=met claims=16` on a 23-row document).
- MEDIUM — A3 fence skipping: fenced claim rows are silently dropped. Evidence:
  count-c2.py:115; driver ATTACK-3 (`C2=met claims=16`).
- MEDIUM — A4 URL substring pin: source identity is not verified; suffix or
  foreign-host-wrapper URLs still pin to the frozen copy. Evidence:
  count-c2.py:248; driver ATTACK-4/4b (`C2=met claims=23` on mutated S537 rows);
  real data clean (nine canonical URLs cell-terminal, `all-real-urls-terminal=True`).
- LOW (disclaimed calibration limit) — A5 located quote cannot detect negation
  context. Evidence: count-c2.py:257 and docstring "Limits"; driver ATTACK-5.
- LOW-MEDIUM (trust-boundary looseness) — A6 output binding is substring-only.
  Evidence: count-c2.py:169; driver ATTACK-6.
- POSITIVE CONTROL — pins arm fails closed on a 1-byte copy mutation; no
  false-green path found in the pin check. Evidence: count-c2.py pin loop;
  driver CONTROL (`pins=bad`, unmet).

Residual call for the lane: A2/A3 and A1 are the same root rule ("first table,
stop at first gap"); one parser fix closes all three. None of the demonstrated
holes are exploited by the landed r55 data (mechanical arms green at the data
revision; nine URLs terminal; single unfenced 23-row table). The residual risk
that survives any parser fix is A5 (semantic location), which the contract
already assigns to the entailment voters.
