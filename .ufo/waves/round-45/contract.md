# Round 45 contract — frozen before the first data seat

Lane: mori (`/home/vgpnk/Projects/shokunin/mori-shokunin`). Entering tip
`554ff416459c92f0dea9762f834a556df2990187` (round-44 closure admitted, 2026-10-25).
This file freezes the three claims' predicates, counters, floors and kill rules
**before** any seat scores them. After the freeze commit, an edit here is a
round-45 correction section, never a rewrite of a predicate.

## Declared claims (3, distinct axes)

| # | claim | axis (score at entry) | type |
|---|---|---|---|
| C1 | the round's ledger gate stops being vacuous: a committed ledger must be revision-sensitive, its rows distinct, and each named vacuity witness must be **rejected** | operability 7 | capability hardening |
| C2 | the lane's gate registry stops overstating: one audit over **every** registry table in `SKILL.md` attributes each audited path to the row that names it, rejects duplicate rows, requires a real `--selftest` argv branch, and reports `unregistered=0` over the whole declared population | calibration 5 (tied lowest) | self-assessment reconciliation |
| C3 | shokuknow assimilation, level-naming theme: one admitted entry grounded in a source this lane opened, one `mined` row whose `used-by` names it, a census-green registry reached **without** a `TMPDIR` override, and a README coverage-map row | depth 5 (tied lowest) | assimilation + knowledge |

Lowest non-retired axis at entry: calibration 5, tied with depth 5 and
freshness 5. C2 and C3 work it; C1 works operability (7). Nothing is claimed on
coverage, freshness or adjacency.

## P-C1 — the ledger predicate (frozen)

A ledger is **admissible** iff every row is one `git` pipeline naming `@REV@`,
its `id` is unique within the ledger, its command text is unique within the
ledger, and the row declares either a value that **differs** between the
measured revision and `--other-rev`, or `CONST=<reason>`.

`C1=met` requires, in one run:
1. the ledger is admissible and its floors hold (`--min-rows`, `--min-classes`
   are hard floors: a value below the floor is clamped up, never honoured);
2. every declared value recomputes exactly at the measured revision
   (`mismatches=0`);
3. every ledger in `--witness-dir` is **rejected** (`witnesses=<n>/<n>`);
4. `--selftest` passes with its own single-check mutant caught.

`C1=unmet` when any of 1–3 fails. `C1_SETUP` (exit 2) for usage, an
unresolvable revision or a git timeout — never a traceback exit 1.

Witness classes (each must be rejected): `W-REVCONST` (a real command whose
value does not move between two revisions and carries no `CONST=`), `W-HEAD`
(a row that resolves the tip with `git rev-parse HEAD` instead of `@REV@`),
`W-DUP` (two rows sharing an id or a command).

## P-C2 — the registry predicate (frozen)

`C2=met` requires, in one run over the committed bytes at `--rev`:
1. **every** registry table in `SKILL.md` whose header is the eight standard
   cells is read (`tables=<n>`, not 1);
2. every audited path is attributed to the row **that names it**, and the
   attribution is printed (`row='<name>'`); a row that does not name the path is
   not an attribution, and the substring fallback may not stand in for one;
3. a registry name occurring twice is a finding (`duplicate=<n>` must be 0);
4. a row's `self-test` cell counts only with a real argv branch: an occurrence
   of `--selftest` inside a comment line does not count (the `r44` silence-oracle
   false positive);
5. the whole declared population (`tools/*.py`, `tools/*.sh`, and the round
   counters `.ufo/waves/round-4[45]/count-c*.py`) audits `unregistered=0` and
   `no_selftest=0`;
6. the audited write-scope cells make no false claim: the write-scope arm's
   `writescope_mismatch` is 0 against `fixtures/write-scope.json`.

`C2=unmet` on any finding; `C2_SETUP` (exit 2) for usage, unresolvable revision,
absent registry or gate table.

## P-C3 — the assimilation predicate (frozen)

`C3=met` requires, in one run at `--rev` with `--root <fleet root>`:
1. the admitted entry exists and carries `source:`, `verified-at:`, `recheck:`
   and `coverage-map:` lines;
2. every `--row S###` exists, is `mined`, and names the entry in its `used-by`
   cell;
3. `sources-census.sh validate --root <fleet root> mori` exits 0 **without** any
   `TMPDIR` override;
4. `corpus/README.md` carries a map row naming the entry;
5. the census script the arm invoked is pinned by digest in the run's stdout.

`C3=unmet` otherwise; `C3_SETUP` (exit 2) for usage/unresolvable revision.

## Kill rules (a control that skips the work must not print met)

- A do-nothing control at the entering tip prints `C1=unmet`, `C2=unmet`,
  `C3=unmet` (the three entering-tip receipts).
- C1: a ledger of revision-constant figures, a HEAD-reading row, or a duplicate
  id/command must not print `C1=met`.
- C2: a junk row that does not name the audited path, or a row whose only
  `--selftest` occurrence is a comment, must not print `C2=met`.
- C3: an entry with no `used-by` on its row, or a census run that needs a
  `TMPDIR` override, must not print `C3=met`.

## Floors and knobs are not overridable

`--min-rows`/`--min-classes` are clamped **up** to the frozen floors
(12 rows, 4 classes). A run that passes a smaller value is clamped, and the
verdict line prints the frozen floors, the measured revision and the repo path,
so the receipt is self-describing.

## Frozen instruments (digest manifest)

Written by the L1 at the freeze commit; each entry is `sha256  path`. The
manifest is `evidence/freeze-r45.txt`. Post-freeze defects are lessons routed to
round 46, not patches.

## Claims are causally separable

- C1 lands and verifies with C2/C3 untouched (its counter, witnesses, ledger).
- C2 lands and verifies with C1/C3 untouched (the auditor, the three orphan
  rows, the three selftest modes, the superseding row).
- C3 lands and verifies with C1/C2 untouched (one entry, one row, one README
  row, the census arm in a separate counter).
