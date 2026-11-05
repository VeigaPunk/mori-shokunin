# Mo92Conn01 — cross-lane overlap scan (mori round 92, wave w1, attempt 1)

Read-only connector seat. No edits to any lane, sibling, fleet root or shared script. Work was done in
scratch clone `<scratch>/repo` (`git clone --shared`, detached at `f63d1ab030d4179576e494342f48ef8718e497a5`,
`rev-parse --show-toplevel` verified). Scratch removed at yield. Receipts copied to
`.ufo/waves/round-92/w1/Mo92Conn01-receipts/`. Tools installed or upgraded: none.

## 1. Sibling search (lane:path:line)

Search: `grep -l` over `*-shokunin/{tools,corpus}` (mori excluded) for `superseded|supersedes`, `sha256`, `SOURCES`,
`verified-at:`, `recheck:`; then line-level reads of the hits that bear on C1 or C2. Hits on `sha256` inside
`corpus/evidence/*`, `corpus/fixtures/*` and `*.gd`/`*.py` fixtures are numerous and are not overlaps; they are not listed.

| # | Lane:path:line | What it does | Bears on |
|---|---|---|---|
| A1 | tsukuroi-shokunin/tools/check-knowledge-header.py:1-12 | QUALITY 8 gate: every `corpus/knowledge/*.md` must carry column-0 `source:`, `verified-at:`, `recheck:`; `verified-at` needs ISO date, `recheck` needs ISO date or `<N>d`/`on-release`; operative = last occurrence; whole file, no line window | C1 (presence leg is the same check) |
| A2 | tsukuroi-shokunin/corpus/QUALITY.md:12 | QUALITY 8 text the gate implements | C1 |
| A3 | tsukuroi-shokunin/tools/check-knowledge-refs-r68.py:1-12 | QUALITY 101: operative `source:` ids must resolve in `corpus/SOURCES.md` | C1 landing (adjacent) |
| A4 | kama-shokunin/tools/digest-ledger.py:1-40 (`classes:` at :26) | Scans `.md/.tsv` for 64-hex tokens; classes blob / external / unverifiable / wrong; `wrong` carries a `correct` digest; no supersession notion | C2 (detection overlap, not ownership) |
| A5 | kama-shokunin/tools/round40-calibration-audit.py:4-19, :64, :81 | Digest-correction by supersession: row whose `teaches` opens `supersedes S472` carrying the exact evidence digest; "false_corrections == 0" | C2 (same convention, kama corpus) |
| A6 | kama-shokunin/tools/round42-digest-audit.py:1-12 | Counter over digest-ledger (kama round 42) | C2 (adjacent) |
| A7 | chousa-shokunin/tools/digest-in-tree.py:1-12 | Receipt sha256 pins re-derived from committed blobs (chousa R67-C2) | C2 (different surface: receipts) |
| A8 | chousa-shokunin/tools/receipt-pin.py:1-12 | Receipt header vs `git cat-file blob` digest | C2 (different surface) |
| A9 | chousa-shokunin/corpus/SOURCES.md:212-214 (S200–S202 `supersedes S19x`), :413 | Supersession rows in a registry, convention only, no tool | C2 convention |
| A10 | kagi-shokunin/corpus/SOURCES.md:107 | Supersession note, convention only | C2 convention |
| A11 | kotodama-shokunin/tools/check-sources-recheck.py:1-8 | Recheck-cadence auditor on the SOURCES `recheck` cell (registry rows, not knowledge lines) | C1 terminology overlap only |
| A12 | kotodama-shokunin/tools/source-audit-inventory.py:1-12 | Per-file sha256 and `to-verify` marker inventory over `corpus/knowledge` | C1 adjacent (inventory, no trio check) |
| A13 | mori-shokunin/tools/mori-sources-appendonly.py:1-12 | Mori's own CORPUS rule 2 gate (`supersedes S###` in teaches) | C2 (own lane, already exists) |
| A14 | mori-shokunin/tools/mori-anchor-check.py:1-13 | Quote-anchor check against a pinned copy (QUALITY 162) | C2 adjacent; not a digest check |
| A15 | mori-shokunin/tools/mori-source-digest.py:2,5 | Mori's C2 digest tool; docstring names itself `digest-check.py` (name mismatch, no behaviour impact) | C2 (own) |

Found in sibling tools with digest-vs-pinned-copy comparison of a registry row: **none**. The hits for
`prefix-only` / `pinned copy` in chousa `freeze-check.py:414`, kama `round64-c2-counter.py:1811`,
tameshi `bash-witness-study.py:112`, tsukuroi `check-revision-binding.py:1061` are unrelated uses of the words.

Found in sibling tools with the trio on knowledge: tsukuroi A1 (the only checker found whose purpose is the three-key header gate). Other lanes' `verified-at:` hits in tools are mentions inside their own checkers' texts.

## 2. Shared shokunin scripts and templates

- `scripts/sources-census.sh` (fleet, read only):
  - :648 `teaches !~ /supersedes S[0-9]{3}/` — E04 "duplicate URL within scope" is waived only when the
    teaches cell opens `supersedes S###`. This is the fleet supersession rule for URL duplicates.
  - :25 documents E04 as "duplicate URL+scope (no supersedes)".
  - :665-666 E09 recheck must be ISO date, `NNd`, or symbolic cadence. This applies to registry rows.
  - No provenance-trio rule and no digest rule in the script. The script does not read digests.
- Fleet `CORPUS.md:116-117` (rule 2, Append-only): "A correction is a new row whose `teaches` opens
  `supersedes S0NN —`." Mori's CORPUS rule 2 is the same text (the mori lane has no `CORPUS.md`; the fleet one applies).
- Fleet `CORPUS.md:23` (Rules): "`knowledge/` entries cite a source: file path, command output, or URL."
  No `verified-at` or `recheck` rule there.
- `templates/mint` does **not exist** in this checkout (`ls` → no such file). `templates/` holds `agents/` and
  `round-prompt.md`; `grep -i -E 'supersed|verified-at|provenance|sha256' templates` returns only generic
  "provenance" prose in agent role files. No trio or supersession rule in templates.

## 3. PROVINCE adjacency

`mori-shokunin/PROVINCE.md:59-70` (table). Siblings named: kumitate (orchestration/wave semantics), tsukuroi (host
diagnosis), kama (serving health), kagi (secrets), souji (scratch residue).

**None** of these owns registry digests or knowledge provenance. The table is silent on tsukuroi's QUALITY 8 gate
(A1) and on kama's digest ledger (A4). Recommendation (state only, L1 decides): consider an adjacency row for
the knowledge-header gate and the digest ledger so the next round's claims can see them.

## 4. Verdict

**C1 (provenance trio on corpus/knowledge): method overlaps, ownership does not.**
- Evidence: A1 checks the same three keys in `corpus/knowledge`, using the same presence rule. Running A1 on the
  mori entering revision (scratch clone, `--revision f63d1ab0…`, exit 1) produced 49 files with findings: 23 MISSING
  keys across 9 files, 41 VALUE findings across 40 files plus 1 `verified-at` ISO-date finding. This shows the
  sibling gate's value leg is not met by the lane today.
- Sibling `tools/check-knowledge-header.py` is tsukuroi's gate for tsukuroi's lane. Knowledge provenance is a per-lane
  QUALITY convention; 16 lanes cite `verified-at` in their own `corpus/QUALITY.md`. No sibling owns mori's knowledge
  entries. C1 stays mori-local.
- Differences from A1 that the L1 must carry (disclosed, not changed):
  1. Window. C1 counts a key only within the first 12 lines. A1 reads the whole file. Of the 39 keys C1 counts as
     missing in the 19 listed files, 16 are present beyond line 12 (A1 accepts them). 23 keys are absent everywhere.
     Check: 39 = 23 + 16.
  2. Values. C1 checks presence only (named limit). A1 checks value form.
  3. Landing form. The frozen landing constraint says `verified-at` "names the admission commit" and `recheck` "names
     the command or citation … or `manual — <path:line>`". A1 requires `verified-at` to carry an ISO date and
     `recheck` to carry an ISO date or `<N>d`/`on-release`. A landed line in the frozen form would fail A1's value leg.
     Mori's own existing lines use the form `verified-at: 2026-10-19 (lane base 20e2255 …)`, which carries both an
     ISO date and a parenthetical. A landed line in that shape (ISO date plus admission commit, e.g.
     `verified-at: <ISO date> (admitted <commit>)`) satisfies the frozen predicate and A1's value leg. This is a
     landing-form suggestion only; the frozen wording is not changed.
- Notify (state for L1, do not message): **tsukuroi** (owner of A1/A2 and QUALITY 8). The disclosure is that the
  gate's value leg currently fails 40 operative `recheck:` lines in mori's corpus/knowledge, and that C1's landing
  will not clear that leg unless the recheck lines carry ISO dates or cadences. This is adjacency evidence, not a
  request to change A1.

**C2 (registry digest gate with supersession and selftest): no ownership overlap; detection overlap with kama.**
- No sibling compares a SOURCES row's recorded digest to its pinned copy (see §1). The supersession convention
  itself is fleet-wide (§2: `CORPUS.md:116-117`, `sources-census.sh:648`), and mori's supersession logic in
  `mori-sources-appendonly.py` (A13) implements it for rule 2. C2 implements digest verification on top of the
  existing convention. This is not a duplicate of any sibling tool.
- Corroboration (scratch, read-only, sibling tool run on a scratch fixture):
  - `kama-shokunin/tools/digest-ledger.py scan --dir <fixture>` on the mori entering `corpus/SOURCES.md` plus the two
    pinned copies: `wrong_unflagged 7891c588…a1a6f0` and `wrong_unflagged 9855a498…ad8020`, i.e. the recorded
    values of S615 and S235 are flagged as wrong (the same two rows as round 91). Receipt: `Mo92Conn01-receipts/kama-base.out`.
  - With the two successor rows S619/S620 appended after S618 (scratch fixture), `tokens` goes 169→170 and `blob`
    goes 1→2: the successor digests classify as `blob` (`7891c588…42f5` and `9855a498…ad8020` hash to the pinned
    copies). Receipt: `Mo92Conn01-receipts/kama-after.out`.
  - The two `wrong_unflagged` lines remain after the successors land, because kama's tool has no supersession notion
    and mori's registry rows are append-only. Its exit stays 1 for unrelated unknown tokens (166 in both runs).
    kama's tool is therefore not a usable gate for mori's C2 as-is; C2 must keep its own supersession logic.
- Notify (state for L1): **kama** (owner of A4/A5). The fact to report is that digest-ledger does not read
  supersession rows and reports the two superseded recorded values as `wrong_unflagged` after S619/S620 land. No change is requested.

## 5. Overlap table

| Claim | Sibling artifact | Overlap kind | Ownership overlap | Verdict | Notify (state only) |
|---|---|---|---|---|---|
| C1 presence trio | tsukuroi `tools/check-knowledge-header.py` (A1), `corpus/QUALITY.md:12` | same check (method), different window, no values in C1 | none (tsukuroi lane gate; no sibling owns mori knowledge) | method duplicate, stays mori-local | tsukuroi (value leg: 40 operative recheck lines fail on mori today) |
| C1 landing form | same | `verified-at` / `recheck` value forms | — | ISO date + commit form satisfies both | L1 (form choice) |
| C1 source ids | tsukuroi `check-knowledge-refs-r68.py` (A3) | adjacent (ids resolve) | none | adjacent, run after landing as spot check | none |
| C2 digest verification | kama `digest-ledger.py` (A4) | detection of same two wrong digests | none (kama: document classifier) | detection overlap, no duplicate | kama (no supersession notion; residual `wrong_unflagged`) |
| C2 supersession convention | fleet `CORPUS.md:116-117`, `sources-census.sh:648`, kama A5, chousa A9, kagi A10 | shared convention | none (convention, each lane applies it) | consistent with convention | none |
| C2 digest artifacts | chousa `digest-in-tree.py` (A7), `receipt-pin.py` (A8) | receipts, not registry | none | different surface | none |
| Registry recheck cadence | kotodama `check-sources-recheck.py` (A11) | `recheck` cell of registry rows | none | different surface | none |
| PROVINCE adjacency | `PROVINCE.md:59-70` | no row for knowledge provenance or registry digests | — | gap in table | L1 (consider a row) |

## 6. Operability and calibration notes

- Tool version/channel: none installed or upgraded.
- Gate method note: A1 refuses to run unless `tools/_revision.py` exists in the target repo (E-LANE-UNRESOLVED, exit 2 on
  first try). For the scratch run I copied the sibling's `tools/_revision.py` into the scratch working tree only;
  git-object reads do not depend on it. The copy was removed before the receipts were written.
- `mori-source-digest.py` docstring names itself `digest-check.py` (A15). Cosmetic; flag for C2's landing.
- No counter was run on the lane. The `count-c1.py` population/window logic was read (12 lines; `HEAD_LINES = 12`)
  to make the 39/23/16 comparison; the comparison itself was computed on the scratch clone with `git show`.

## Receipts (under .ufo/waves/round-92/w1/Mo92Conn01-receipts/)

- `tsk-header.out` — A1 run on entering rev (exit 1; 49 findings, 23 MISSING, 41 VALUE).
- `kama-base.out`, `kama-after.out` — A4 runs on the scratch fixture before/after S619/S620 (exit 1 each).
- Commands and exit codes: clone + checkout + rev-parse (0); A1 first run (2, E-LANE-UNRESOLVED, fixed as above);
  A1 second run (1); C1-vs-A1 comparison script (0); kama base scan (1); kama after scan (1); `git show | sha256sum` of
  both pinned copies (0, values 7891c588…42f5 and 9855a498…ad8020 match the contract).

## Dead ends

- `templates/mint` absent; `CORPUS.md` lives at fleet root, not in the lane.
- No sibling digest-compare tool found for registry rows.
