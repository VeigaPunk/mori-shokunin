# Mo61ScoutTableShape — gate-registry table recon: exemplars, header, style sheet

Seat: mori r61 wave-1 scout, 2026-10-30. Read-only: no production file, registry, or VCS
state touched; no counters executed live (recon seat — nothing to count); no tool
installs (none needed). Scratch `/fast/scratch/hyaku/mori-r61/Mo61ScoutTableShape-2/`
was created as TMPDIR only (no counter run needed it) and removed before yield.
Disk guard seen before work: `/fast` 384G free (53%).

Evidence base (all absolute paths, working tree at entering revision):
- `/home/vgpnk/Projects/shokunin/mori-shokunin/SKILL.md` — 1256 lines, 193131 bytes.
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/count-c1.py` — 224 lines (frozen C1 counter).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-gate-registry.py` — 743 lines (v2 auditor, round 45).
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-61/gate-manifest.json` — 25 paths.
- Measured checks: the frozen `count-c1.py` module was imported in a throwaway
  interpreter (defs only; `main()` guarded) and its `parse_tables`/`row_hits` were run
  against synthetic rows. Findings F1–F4 below are measured outputs, not inference.

## 1. Exact header cells (byte-for-byte)

Every registry table in SKILL.md opens with this header row and this separator row
(SKILL.md:162-163, identical at :543-544, :607-608, :662-663, :737-738, :815-816,
:900-901, :936-937, :969-970, :1007-1008, :1054-1055, :1110-1111, :1207-1208 — 13
registry-shaped tables):

```
| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
```

- `count-c1.py:21-22` `HEADER_CELLS` and `mori-gate-registry.py:70-71` `FIELDS` both
  compare the header lower-cased and whitespace-stripped; exactly these eight words.
- Any table anywhere in the file with exactly this header is a registry table (auditor
  docstring, `mori-gate-registry.py:3-7`; `count-c1.py:40-59` scans the whole file).
  Drafted rows may therefore live in a new per-round table.
- `count-c1.py:47` skips exactly one line (`i += 2`) after the header — the separator
  row must be the immediately following line; data rows follow and must start with `|`.
- Each data row must split into **exactly 8 cells** (`count-c1.py:49-50`): rows with
  7 or 9 cells are silently dropped from parsing (see F3).

## 2. The three exemplar rows (verbatim)

### r44 — `r44 figure ledger (C1)` (SKILL.md:183)

```
| r44 figure ledger (C1) | gate | `python3 .ufo/waves/round-44/count-c1.py <rev>` (`--ledger PATH`, `--repo PATH`, `--min-rows N`, `--min-classes N`, `--selftest`) | 0 `C1=met mismatches=0` · 1 `C1=unmet` (a row's recomputed value differs from its asserted value, or a row/class floor fails) · 2 `C1_SETUP` (usage, unresolvable revision, git timeout); a ledger whose rows are not single `git` pipelines naming `@REV@` is rejected, never scored | `python3 .ufo/waves/round-44/count-c1.py --selftest` → `C1_SELFTEST pass=6 fail=0` over isolated throwaway git repos: honest ledger, off-by-one row, junk producer, below-floor ledger, absent ledger, compound command | ledger bytes at the measured revision (default `.ufo/waves/round-44/figures.tsv`); witness fixture `.ufo/waves/round-44/fixtures/figures-r43.tsv`; mutant `.ufo/waves/round-44/fixtures/mutants/count-c1.py` | stdout only; reads the repo at `--rev`; the selftest writes only under the caller TMPDIR | mori |
```

### r50 — `r50 calibration counter (C1)` (SKILL.md:1056)

```
| r50 calibration counter (C1) | gate | `python3 .ufo/waves/round-50/count-c1.py <rev> [--repo DIR] [--fleet-repo DIR] [--fleet-rev REV] [--scratch DIR] [--timeout S]` | 0 → `C1=met items=N axes=6 pins=P boxes=B mismatches=0 errors=0 hidden=0 manifest=<sha12> rev=R` · 1 → `C1=unmet … failed=<reasons>` with one `item` line per axis and pin (expect/got/state) · 2 → `C1_SETUP` (usage, a missing option value, an unresolvable revision on the lane or the fleet repo) | `python3 .ufo/waves/round-50/count-c1.py --selftest` → `C1_SELFTEST pass=34 fail=0` | `FLEET_REV` e0144996…, `THROUGH` 49, `MIN_BOXES` 4, `MIN_PINS` 2, `RECEIPT_DIR` `.ufo/waves/round-50/evidence/selftests/`; limit: the Score column is unchecked and the fleet MANIFEST is trusted | none (read-only `git show` / `git cat-file` / `git archive`; the archive is extracted under `--scratch` and removed) | mori |
```

### r51 — `r51 operability counter (C1)` (SKILL.md:1112)

```
| r51 operability counter (C1) | gate | `python3 .ufo/waves/round-51/count-c1.py <rev> [--repo DIR] [--hide PATH] [--scratch DIR] [--keep]` (`--hide` is the path bubblewrap hides, default the lane; `--scratch` must lie outside the source repo) | 0 → `C1=met kill_residue=0 relocated=met reloc_mismatch=0 classified=ok selftest=pass=N,fail=0 rev=<full> failed=-` · 1 → `C1=unmet … failed=<arms>` (kill_residue, relocated, classified, selftest), plus a `kill_residue_first:` line and the classifier's `prefix=` lines and summary echoed as `classified:` lines · 2 → argparse usage error, or `C1_SETUP <reason>` (unresolvable revision, scratch inside the source repo) | no mode of its own: `--selftest` is an argparse usage error (exit 2); the arms are exercised by the five controls in `.ufo/waves/round-51/controls/` (receipts `evidence/control-c1-<name>.txt`), and arm D pins R's pin-check selftest at ≥ 114 arms | `ENTERING_SELFTEST` 114; the five-row fixture registry (`enva`/`envb` → env, `stla`/`stlb` → stale, `okay` → match) and the ` env=2 stale=2` summary are in-script; the kill lands 3 s after the first write; limits: one kill moment, one hidden path (the lane), five fixture rows, and a tool that prints a tally then fails for an environmental reason is classed stale | scratch only: `--scratch DIR` (default a `mkdtemp` under TMPDIR) is refused inside the source repo and removed on exit unless `--keep`; each arm clones the repo fresh with `--no-local` and writes nothing into the tree it reads | mori |
```

Supplementary verbatim rows the drafters will want open: `r44 gate registry (C2)` at
SKILL.md:184 (auditor row; pins the auditor sha256 in the self-test cell),
`r51 MemAvailable entry counter (C2)` at SKILL.md:1113 (C2 entry-counter shape),
`commit runway (r53, C2)` at SKILL.md:1209 (the newest registry row on disk, r53
additions table).

## 3. What the frozen C1 counter demands (count-c1.py, line-cited)

For each of the 25 manifest paths (`measure`, `count-c1.py:73-120`):

1. **Found**: ≥1 parsed row whose entry cell names the path (`row_hits`, :62-70:
   tokens of the entry cell with backticks/`()`/`,` stripped must contain the path, or
   the path is a substring of the entry cell).
2. **Exactly one live row**: rows whose `name` **or** `write scope` cell contains
   `supersed` (case-insensitive) are excluded; two live rows → `dup:N` (:82-85).
3. **All eight cells non-empty** (`:87-90`): any empty cell → `thin:<path>:<cells>`.
   An empty owner fails here (see F2).
4. **Self-test cell contains the literal `--selftest`** (`:91-93`) → else
   `noselftest:<path>`.
5. **Path resolves at the measured revision** (`cat(repo, rev, path)`, :94-96) → else
   `unres:<path>`.
6. `ok` requires `registered == gates` and `failed` empty (`:116-118`).

Parsing gates before all that (`parse_tables`, :40-59): header row (lower-cased,
stripped) must equal `HEADER_CELLS`; separator skipped; each row re-split on `|` and
must yield exactly 8 cells — anything else is silently not a row.

## 4. What the auditor standard adds (mori-gate-registry.py, round-45 v2)

The C1 counter is the scoring instrument, but the auditor (`tools/mori-gate-registry.py`,
row at SKILL.md:184) is the written lane standard a reviewer will hold rows to:

- **Attribution**: the row for a path is the row whose entry cell's *first backticked
  command* invokes that path (`entry_target`/`entry_names`, :233-253, wrapper words in
  `WRAPPERS` :74-75). Prose or a later mention never attributes (docstring :7-9).
- **Entry path hygiene**: repo-relative, never absolute, never `..`-escaping
  (`safe_relpath` :118-128); must resolve at the revision (`exists_at` :137-140).
- **Real self-test branch**: `--selftest` must appear in the tool's argv handling, not
  only in a comment/docstring (`mask_python`/`mask_shell` :256-289, `selftest_flag`
  :304-321). A non-`--selftest` flag must be declared in the self-test cell as
  `selftest-flag=<flag>` (`FLAG_DECL` :78-79), and the flag name must contain `test`
  (`escape_branch` :330-344).
- **Duplicate registry names file-wide are findings** (docstring :28-29).
- **Seven-cell rows are malformed** (selftest arm `seven_columns`, :565-571).

## 5. Style sheet (per cell, conventions that made r44–r51 conformant)

- **name** — `<short instrument name> (rNN, C<k>)` or `rNN <thing> counter (C<k>)`
  (r44–r51 pattern: `r48 junk-variant counter (C1)` :971, `r50 calibration counter
  (C1)` :1056, `r51 operability counter (C1)` :1112; tools take
  `<function> (rNN, C<k>)`: `registry pin reconciler (r47, C1)` :938). Names are
  unique across the whole file (auditor duplicate rule). Superseding rows append
  ` — <cell> superseded` to the name (SKILL.md:193-196).
- **kind** — plain `gate` for every wave counter (all r44–r51 counter rows) and for
  most tools; `probe` for observation-only instruments (SKILL.md:172, :902). Scope
  qualifiers go in parentheses right after the word, never as a separate sentence:
  `gate (host-surface verdict; not a census or fleet-admission gate)` :664/:1209,
  `gate (committed-bytes consistency gate over the lane's own round-24 evidence; not a
  fleet-admission gate)` :740, `gate, artifact accounting only` :609,
  `probe (one dated self-assessment measurement, not a standing gate)` :189. The 25
  manifest paths are all counters/gates → `gate` (plain) is the conformant choice.
- **entry** — first backticked span is ONE complete invocation naming the exact
  repo-relative manifest path: `` `python3 .ufo/waves/round-50/count-c1.py <rev>
  [--repo DIR] [--scratch DIR]` ``. Option glosses/defaults go in a second
  parenthetical backticked span (`r44` :183, `r51` :1112 style). Never absolute paths
  (auditor `safe_relpath`). **Never a `|` character anywhere in the cell** (F1).
- **verdict map** — `0 <met template> · 1 <unmet template> · 2 <setup>`; r44 style
  `` 0 `C1=met mismatches=0` · 1 `C1=unmet` (reasons) · 2 `C1_SETUP` (reasons) ``;
  r50+ adds `→`: `` 0 → `C1=met … failed=-` ``. Quote the frozen output template
  literally, list per-arm reasons parenthetically, and add one clause for the
  instrument's rejection rule (r44: "a ledger whose rows are not single `git`
  pipelines naming `@REV@` is rejected, never scored").
- **self-test** — `` `<invocation> --selftest` → `<TALLY>` ``; the literal string
  `--selftest` must appear (counter rule 4); the tally is measured and spelled as the
  tool prints it: `C1_SELFTEST pass=6 fail=0` (:183), `C2_SELFTEST pass=31 fail=0`
  (:1057), optional provenance suffix `(re-run 2026-10-26; receipt
  `evidence/selftest-c2.txt`)` (:1113). Honest no-mode fallback is allowed if the cell
  still names `--selftest` and says what exercises the arms instead (r51 C1 :1112:
  "`--selftest` is an argparse usage error (exit 2); the arms are exercised by the five
  controls in …"). A different flag must be declared `selftest-flag=<flag>` (auditor).
- **pinned values** — name the in-script constant that holds each pin plus the value:
  `COPIES`/`PINS` sha256 sets (`sha256 of the three copies under
  `corpus/evidence/sources-r50/` (in-script `COPIES)` :1057), scalars
  (`` `FLEET_REV` e0144996…, `THROUGH` 49 `` :1056), paths, floors, dates
  (`` `OPENED` 2026-10-26 ``), and end with an explicit `limits:` clause naming what
  the counter does **not** check (:1056 "limit: the Score column is unchecked and the
  fleet MANIFEST is trusted"; :1112 "limits: one kill moment, one hidden path …").
  sha256s are written full or 12-hex.
- **write scope** — lead with the strongest claim: `none (read-only `git show` /
  `git cat-file` / `git archive`; the archive is extracted under `--scratch` and
  removed)` (:1056); `stdout only; … nothing in the repo is written` (:183 family);
  `scratch only: … removed on exit unless `--keep`` (:1112). Name where bytes land,
  what is cleaned, and the refusal rule. The word `superseded:` here (or in the name)
  is what makes a row non-live for C1 (:193-196).
- **owner** — every historical r44–r53 row reads `mori`. The frozen counter accepts
  any non-empty owner (its selftest fixture uses `MoriR61`, count-c1.py GOOD :139).
  Drafters should pick one token and use it for all new rows; both pass the counter.
- Minimal conformant shape, straight from the frozen counter's own `GOOD` selftest
  fixture (`count-c1.py:139-141`):
  ``| r61 t (C1) | gate | `tools/g.py` (`--x`) | 0 met · 1 unmet | `python3 tools/g.py --selftest` → pass=1 | sha 00 | read-only | MoriR61 |``

## 6. Placement and prose conventions

- Precedent for a new batch of rows: a `### Round NN registry additions` section with
  the standard 8-cell table directly under it (SKILL.md:1205-1209, r53). Rounds 54–55
  have sections without registry tables; there are **no** SKILL.md sections for rounds
  56–60 (file ends at :1256, mid-round-55) — where the r52–r60 rows go is L1's call;
  both parsers find standard tables anywhere in the file.
- A dated prose refresh note after the table naming what was added and re-measured
  (SKILL.md:198-202 pattern, round-45 refresh).
- The 25 paths the rows must name (gate-manifest.json, in order): the 18 wave counters
  `.ufo/waves/round-{52..60}/count-c{1,2}.py`, `.ufo/waves/round-60/count-c3.py`,
  `.ufo/waves/round-57/verify-c2-source.py`, and
  `tools/{mori-vote-bind,mori-driver-liveness,mori-register-check,mori-settlement-scan,mori-entry-claims-check}.py`.
  None of them is registered today (the r53 table registers only
  `tools/mori-commit-runway.py`, which is not in the manifest) — consistent with the
  frozen before-control `registered=0`.

## 7. Findings (frozen surfaces — reported, not fixed)

- **F1 — `\|` divergence between the two parsers (measured).** `count-c1.py:49`
  splits rows with a naive `split("|")`; the auditor uses `CELL_SPLIT =
  re.compile(r"(?<!\\)\|")` (`mori-gate-registry.py:80`). A row containing an escaped
  pipe in a cell (existing precedent: `--scope user\|system`, SKILL.md:172) yields 9
  cells under C1 and is **silently dropped** → its path counts `missing`. Verified by
  running the frozen `parse_tables` on such a row: row absent, `row_hits` empty.
  Drafter rule: no pipe character, not even `\|`, in any cell of a manifest-path row
  (write `user or system`).
- **F2 — `noowner` is a dead counter (measured).** `res["noowner"]` is initialised
  (`count-c1.py:75`) and printed (:129) but never incremented: an empty owner cell is
  caught by the generic empty-cell check as `thin:<path>:owner` (:87-90). The frozen
  met line prints `noowner=0` either way. No action possible (frozen); drafters just
  never leave the owner cell empty.
- **F3 — ≠8-cell rows are invisible (measured).** A 7-cell row is dropped by
  `parse_tables` (`count-c1.py:49-50`) rather than flagged; the path then reads as
  `missing`, not `thin`. Always emit exactly 8 cells.
- **F4 — C1 attribution is looser than the auditor's.** `row_hits` also matches a
  path as a bare substring of the entry cell (`count-c1.py:69`), while the auditor
  only attributes the first backticked command (:233-253). A row can satisfy C1 while
  failing the written standard. To be conformant under both: put the manifest path in
  the first backticked span and do not mention it elsewhere in the cell.
- **F5 — surface observation.** The contract's "registry tables end at r51" is
  accurate for manifest coverage only: an r53 additions table exists (SKILL.md:1205)
  and rounds 54–55 have prose sections, but no r52–r60 manifest path has a row and no
  SKILL.md section exists beyond round-55 (file ends :1256).

## Receipt

- `wc -l` SKILL.md → 1256 lines / 193131 bytes; `df -h /fast` → 384G free before work.
- Table-header inventory (grep `write scope`): 13 tables at lines 162, 543, 607, 662,
  737, 815, 900, 936, 969, 1007, 1054, 1110, 1207.
- Verbatim rows extracted from the file bytes via interpreter read (read tool truncates
  long lines); none altered.
- Synthetic parse test (frozen module, sandbox interpreter, no writes): 7-row table →
  4 parsed; `\|` row and 7-cell row dropped; superseded-name and superseded-scope rows
  parse but are excluded from the live set by `measure`'s `supersed` filter; empty
  owner parses (fails later as `thin`).
- Scratch `/fast/scratch/hyaku/mori-r61/Mo61ScoutTableShape-2/` removed at yield; no
  other writes than this report.
