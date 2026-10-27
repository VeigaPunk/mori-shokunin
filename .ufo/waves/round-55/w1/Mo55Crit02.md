# Mo55Crit02 — C1 status-arm attack: same/moved/changed derivation and source pins

Seat: Mo55Crit02 (critic, leaf). Lane: mori-shokunin. Round 55, wave w1.
Assignment: attack the C1 same/moved/changed derivation and source pins; find a concrete
false-green control or counter branch uncovered by selftest; scratch only; no C1/C2 votes.
Scratch: /fast/scratch/hyaku/mori-r55/Mo55Crit02 (removed at yield; evidence summary EVIDENCE.txt).
Measured revision: b8b7064c2b54c8b6b22c288232a96c43fae1af47 (contract data pin); HEAD b8a70adf re-checked.
Counter/contract/controls/selftest read in full: `.ufo/waves/round-55/count-c1.py` (479 lines),
`checks/selftest-c1.py`, `controls/c1data.py`, `evidence/freeze-sha256.txt`, `corpus/knowledge/kernel-v7.3-recheck-r55.md`.
I am a non-voter: this report emits no lines beginning RECHECK/ENTAIL/REPLACE/QUOTE.

## 1. Baseline counter runs (status arm currently all green; only votes open)

Command: `python3 .ufo/waves/round-55/count-c1.py b8b7064c2b54c8b6b22c288232a96c43fae1af47`
Output: `C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 rev=b8b7064c... failed=votes` — exit 1.
Command: `python3 .ufo/waves/round-55/count-c1.py HEAD` — identical line, exit 1.
Scope stability: `count-c1.py --scope` output diffs clean against frozen `evidence/c1-scope.txt` (78/78 identical).
Selftest rerun on this host: `count-c1.py --selftest` → `C1_SELFTEST pass=44 fail=0`, exit 0.

## 2. Pin attack — bilateral external re-fetch (positive)

Local: all 22 COPIES entries (11 paths × v7.2/v7.3) hash-match git objects at b8b7064c (0/22 mismatch);
all 35 `evidence/freeze-sha256.txt` entries match git objects (0/35 mismatch).
External (independent seat re-fetch, counter limit: "wave seats re-fetch them independently"):
all 11 v7.3 URLs `https://git.kernel.org/.../plain/<path>?h=v7.3` return bytes whose sha256 equals the
frozen pins — 11/11 match (e.g. kernel/sched/psi.c c4edc1e7..., mm/page_alloc.c 315ef97b...).
All 11 v7.2 URLs `?h=v7.2` also match — 11/11 (e.g. fs/proc/base.c cef1a2cf...).
Consequence: the four byte-identical-across-release files (`mm/oom_kill.c` 452f1348...,
`include/trace/events/oom.h` 82f04ad4..., `Documentation/accounting/psi.rst` 11c6b712...,
`include/linux/psi_types.h` 483269b2...) are unchanged upstream between v7.2 and v7.3; their `same`
rows are upstream-true, not a pinned-copy artifact. No false provenance detectable on either side.
Seven older copies (sources-r47/r50/r51/r53/r54) are not re-listed in the r55 freeze table but are
pinned by the frozen COPIES table and byte-match the upstream fetches; chain of custody intact.
Registry hygiene: no duplicate v7.3 URLs in `corpus/SOURCES.md`; the 11 C1 rows (S502, S516, S526–S534)
are each mined, opened 2026-10-26/27, used-by names the ledger.

## 3. Independent re-derivation of the 9 non-same rows (own code, pinned copies, per-row sha256 identity)

- 7 moved rows (b50f210b822a page_alloc 4630→4689; db108c1ad61c page_alloc 4265→4311;
  eee4454705c0 kernel-parameters 5505-5507→5540-5542; edd8b8c361b4 cgroup-v2 1215-1221→1240-1246;
  9a8d29e96280 proc.rst 1811-1812→1812-1813; 07a985363937 cgroup-v2 1450-1466→1477-1493;
  4eea9d9f5ae5 fork.c 1768-1769,1949-1966→1795-1796,1976-1993): v7.2 block equals v7.3 block at the
  claimed v7.3 lines, and each v7.2 block occurs exactly once in its v7.3 copy — no occurrence-choice
  ambiguity in the current data.
- 2 changed rows: 02b8d2d11094 (`memory.pressure` 1911-1915→1938-1942) and 77bd396cffd3
  (`io.pressure` 2171-2175→2202-2206): v7.2 text "A read-only nested-keyed file." became
  "A read-write nested-keyed file." in v7.3; the v7.2 blocks occur nowhere in the v7.3 copy
  (`changed` correct per the frozen rule), and the claimed v7.3 ranges contain the true successor
  blocks — the locations are honest, not decorative.
All 69 `same` rows are equal-at-same-numbers under the counter's normalized comparison; the counter's
full re-derivation (status_ok=78) and this seat's independent pass agree.

## 4. False-green control run — uncovered branch demonstrated (F2)

Selftest covers the adjacent case "changed rows pinned at v7.2 numbers derive changed (accepted)".
It does not cover arbitrary relocation. This seat ran the frozen `evaluate()` on a synthetic layer of
the real b8b7064c files with only the two changed rows' v7.3-lines cells rewritten to bogus but
in-bounds ranges (`1-5` and `7-11`, inside the file's comment header):

    FALSE-GREEN CONTROL ... C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 source_rows=ok
    pins=ok provenance=ok same=69 moved=7 changed=2 broken=0 holds=78 stale=0 voted=0 dissent=0 failed=votes
    HONEST BASELINE       ... C1=unmet scope=78 rows=78 matched=78 status_ok=78 line_ok=78 ... failed=votes

The two outputs are byte-identical on the status arm. For `changed` rows the predicate constrains the
v7.3-lines cell only by piece count and bounds ("every piece lies inside the committed v7.3 copy"),
never by content, because `changed` means the v7.2 block occurs nowhere. The column is therefore
decorative for changed rows, and a lazily built ledger could fabricate those locations without
mechanical detection. The frozen counter is predicate-faithful (the docstring defines exactly this),
so this is a frozen-predicate evidential limit, not counter disloyalty; the current data is verified
honest (§3). Smallest safe correction (only when the predicate next thaws): require changed-row v7.3
lines to contain a normalized successor block (e.g. ≥1 equal line) or rename the column value to an
explicit "approx" marker for changed rows; until then the 2 changed rows' successor locations must be
attested by the RECHECK voters' own re-derivation, not by the counter.

## 5. Secondary latent branches (no current exposure)

- Moved-row occurrence latitude: the counter accepts any occurrence of the block; selftest tests
  off-by-one (fails) but not "a different valid occurrence" (would pass). All 7 real moved blocks occur
  exactly once, so no current exposure; noted as a future control.
- Wrapped header-line group (cross-confirmed with Mo55Crit01): `oom-tracepoints-r47.md:17-18` cites
  "header lines 12, 34," / "76, 118, 134, 150, 166, 183" across a hard line wrap; the frozen per-line
  extractor scopes only `12,34` (row 7b2d297eec60), leaving 6 of the 8 S475 header lines unrechecked.
  Latent because oom.h is verified unchanged between v7.2 and v7.3 (§2); the extractor is frozen.
- `line_ok` semantics: for the 2 changed rows, `line_ok` certifies only in-bounds + piece-count, not
  location correctness — the receipt's `line_ok=78` overstates location verifiability for changed rows
  by exactly these 2 rows (same limit as F2).

## 6. Vote-arm note (observed, not my attack scope)

`w1-results.json` is absent and no RECHECK reports are present at measurement time, so `voted=0` is
the only failing arm; the status arm needs no further build work. Sibling seats report live vote-arm
defects (fence-delimiter toggling, non-anchored vote regex) outside this seat's status-arm scope.

## Findings

- MEDIUM (latent, scope completeness; frozen extractor) — Wrapped S475 header-line group: only 2 of 8
  cited oom.h header lines are in the frozen scope. Evidence: corpus/knowledge/oom-tracepoints-r47.md:17-18
  at ENTER; scope row 7b2d297eec60 (`include/trace/events/oom.h:12,34`); frozen `HEADER_LINES` regex in
  count-c1.py:99. Latent: oom.h v7.2==v7.3 verified upstream (§2).
- LOW-MEDIUM (latent false-green control, demonstrated) — Changed-row v7.3-lines cells are mechanically
  unconstrained: relocated to bogus in-bounds ranges 1-5 / 7-11, the frozen counter's status arm stays
  green with output identical to the honest baseline. Evidence: scratch run §4 (transcript above);
  frozen rule in count-c1.py derive(); selftest's nearest control `checks/selftest-c1.py`
  ("changed row at v7.2 numbers still derives changed"). Current data honest: claimed v7.3 lines
  1938-1942 / 2202-2206 contain the true successor blocks (verified §3).
- LOW (latent) — Moved rows accept any occurrence; no occurrence-choice control in selftest; all 7 real
  moved blocks occur exactly once, so no current exposure. Evidence: §3 occurrence scans.
- INFO (positive evidence) — All 22 pins verified locally and by bilateral upstream re-fetch
  (11/11 v7.3, 11/11 v7.2); the four identical-across-release files are genuinely unchanged upstream;
  no duplicate v7.3 URLs; scope extraction matches frozen evidence exactly. Evidence: §2, §3.
