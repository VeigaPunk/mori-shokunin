# Mo61MutC1b — mutation kill table for the frozen r61 `count-c1.py`

Seat: Mo61MutC1b (mori round 61, w1). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Freeze `7370a731abcafc4c803111de7c22cd6264d63be1`, entering `325f7e639916fcbc77fa2ec7475951a1b86bb1cb`.
Frozen counter: `.ufo/waves/round-61/count-c1.py`, sha256
`a6684e697583746e8b6318d6984f3ada5e619c45a0a3449ecf46d79193433e00` (== `PIN_C1` in `count-c3.py`).

Assignment: mutate scratch copies — (M1) accept any row kind (skip the header match, parse ALL
markdown rows); (M2) treat superseded rows as live; (M3) skip the unres arm — drive each through the
frozen `--selftest` and committed control states plus scratch hostile states; a mutant surviving every
committed witness is a ROUTED DEFECT (the arm has no witness). Detection/report only; counters and
contract are frozen and were not modified.

## Method

- All mutants live in `/fast/scratch/hyaku/mori-r61/Mo61MutC1b/mut/` (copies of the frozen bytes,
  mutated in place there). The lane file was never touched: sha256 verified identical before and after
  every run (restoration evidence below).
- Witnesses:
  - **W1** — the frozen `--selftest` battery (committed receipt `.ufo/waves/round-61/evidence/selftest-c1.txt`).
  - **W2** — the committed do-nothing control state: counter at the entering rev against the lane repo
    with the committed manifest (absolute-path mode; the manifest does not exist in-tree at the entering
    rev). Pristine reproduces the committed receipt `evidence/control-c1-do-nothing.txt` byte-for-byte
    (line 1 equal, `rc=1`).
  - **W3** — the committed freeze-rev state (manifest in-tree). `SKILL.md` at the freeze rev is byte
    identical to the entering rev (`diff` empty), so W3 is the same registry content with the manifest
    resolved from git.
  - **H\*** — hostile scratch fixtures, each a git repo created at an explicit scratch path
    (`mktemp`-style dir under the seat scratch; every git call `git -C "$D"`; `git rev-parse
    --show-toplevel` asserted == the fixture dir before any commit; identity `t <t@t>` used only inside
    fixtures). H1: a 4-column non-registry row names the gate path. H2: two registry rows for one path,
    one marked superseded. H3/H5: a registry row names a path absent at the rev. H4: a non-registry
    8-column table (header `decision|surface|path|note|check|pin|scope|who`) carries the only row naming
    the gate path, all cells filled, `--selftest` in the check cell.
- Disk guard checked before runs: `/fast/scratch/hyaku` 54%→56% used, ~356G free (green). No tools
  installed (none needed). TMPDIR set to the seat scratch for all runs.

Disclosed miss: a fourth mutant copy `m1a_noheader8` was created but the edit was never applied — it ran
byte-identical to pristine (sha `a6684e69…`) in the first pass and was dropped before the final table.

## Mutants (scratch copies; lane bytes untouched)

| id | mutation | site (frozen line numbers) | sha256 (mutant copy) |
|---|---|---|---|
| M1_anyrow | `parse_tables` returns every pipe-row (header match dropped, cells padded/truncated to the 8 canonical positions) | `parse_tables` 40–63, header gate at 47 | `336e37199dda988a48f84360a31af7a5892801dac589f03112f6eda067ce874a` |
| M2_superseded_live | supersede filter removed: `live = list(hits)` | 96–98 | `c4ddcc3fb37cbdb0c0a96d9cce47002187d663b5d3905da6d537137406283e4f` |
| M3_no_unres | `unres` arm removed (entry path no longer required to resolve) | 113–116 | `61c5ba6d12c4d5cd461a4216f381ec8124e89a74cc3de3407d647f1b562af343` |

## Kill table

| mutant | W1 selftest | W2 control (entering) | W3 freeze rev | hostile state | verdict |
|---|---|---|---|---|---|
| pristine | PASS 6/6 (== committed receipt) | identical to committed receipt, rc=1 | `C1=unmet gates=25 registered=0 missing=25 …` rc=1 | — | baseline |
| M1_anyrow | PASS 6/6 | identical line, rc=1 | identical line, rc=1 | H1: reason flips (`missing:` → `thin:…`), verdict same; **H4: `C1=unmet` → `C1=met` rc 1→0** | **SURVIVES every committed witness — ROUTED DEFECT** |
| M2_superseded_live | **FAIL**: `case superseded-ok … FAIL failed=['dup:tools/j.py']`, `C1_SELFTEST pass=5 fail=1` rc=1 | identical line, rc=1 | identical line, rc=1 | H2: pristine `C1=met` → mutant `dup=1 … failed=dup:tools/x.py` rc=1 | **KILLED by W1** (supersede arm witnessed) |
| M3_no_unres | PASS 6/6 | identical line, rc=1 | identical line, rc=1 | **H5: pristine `C1=unmet … unres=1 … failed=unres:tools/ghost.py` rc=1 → mutant `C1=met … registered=1 … failed=none` rc=0** | **SURVIVES every committed witness — ROUTED DEFECT** |

Full transcripts: `kill-table.txt`, `driver-out.txt`, `h4-out.txt` in the seat scratch (receipts quoted
below; scratch cleaned after this report was written).

## Findings (routed defects — report only, no fix applied)

### RD-M3 — the `unres` arm has no committed witness; the selftest case named `unres` exercises `missing`

- `CASES` line 157: `("unres", [GOOD], ["tools/nothere.py"], False)`. The only table row (`GOOD`) names
  `tools/g.py`, so `row_hits(rows, "tools/nothere.py")` is empty and the counter exits at the `missing`
  arm (91–95) before `unres` (113–116) can run. The committed receipt states it outright —
  `evidence/selftest-c1.txt:6`: `case unres: ok=False want=False pass failed=['missing:tools/nothere.py']`.
- Committed control states cannot reach the arm either: at entering and freeze revs all 25 gates fail at
  `missing` first (`registered=0 missing=25 unres=0` in `evidence/control-c1-do-nothing.txt`).
- Consequently the M3 mutant prints a byte-identical selftest (pass=6 fail=0) and byte-identical control
  lines — it is invisible to every committed witness.
- On hostile fixture H5 (registry row naming `tools/ghost.py`, file absent at that rev, manifest carries
  the path): pristine `C1=unmet gates=1 registered=0 … unres=1 … failed=unres:tools/ghost.py` rc=1;
  mutant `C1=met gates=1 registered=1 … failed=none` rc=0. The mutant flips unmet→met, i.e. the arm is
  live, contract-load-bearing (contract C1 kill rule: "an unresolved path"), and unwitnessed.
- Suggested witness shape for a future round (frozen here; not applied): a selftest case whose manifest
  path IS named by a table row but is absent from the fixture tree, expecting
  `failed=['unres:tools/<name>.py']`.

### RD-M1 — the registry-table gate (header match) has no committed witness

- All six selftest cases build SKILL.md via `table(*rows)` (`count-c1.py:133-136`), i.e. always the exact
  gate-registry header. No case ever offers a non-registry table row, so a parser accepting any row kind
  is indistinguishable from the frozen parser on the whole battery.
- Committed states are blind too: at the entering and freeze revs no manifest path occurs inside any
  SKILL.md table row (every table row of `git show 325f7e63:SKILL.md` scanned; the only two string
  occurrences, SKILL.md:1203 `.ufo/waves/round-53/count-c1.py` and SKILL.md:1243
  `.ufo/waves/round-54/count-c1.py`, are prose bullets, not table cells). Both committed states print the
  identical `C1=unmet gates=25 registered=0 missing=25 …` line under pristine and mutant.
- Hostile H4 flips the verdict: pristine `C1=unmet … missing=1 … failed=missing:tools/h.py` rc=1; M1
  `C1=met gates=1 registered=1 … failed=none` rc=0 — a file containing zero registry rows passes as met
  once one non-registry 8-column row names the path with a `--selftest` mention. H1 (4-column row)
  changes only the failure reason (`missing:` → `thin:tools/h.py:selftest,pinned,scope,owner`), not the
  verdict — after the registry rows land, any future non-registry table that mentions a gate path in its
  3rd column starts feeding `thin`/`dup`/`registered` arms under M1.
- Suggested witness shape: a selftest case whose SKILL.md carries a wrong-header 8-column table naming
  the path, expecting `failed=['missing:<path>']`.

### WITNESSED — M2 (supersede filter) is killed by the frozen selftest

- Removing the filter flips `case superseded-ok` to `FAIL failed=['dup:tools/j.py']`
  (`C1_SELFTEST pass=5 fail=1`, rc=1): the filter at 96–98 is pinned by the battery. H2 confirms the
  designed semantics (live+superseded pair → `C1=met`, superseded row excluded from `live`).
- Corollary, measured, not a mutant: the same case pins the `hits[0]` fallback (line 103,
  `row = live[0] if live else hits[0]`) — an ALL-superseded pair still yields `registered`/`met`, so the
  counter does not actually check "exactly one non-superseded row" (contract C1 target wording); zero
  non-superseded rows also registers. Surfaced here because M2's kill is what isolates the fallback; a
  "superseded-only row must not register" expectation is absent from the battery.

### Incidental (adjacent, one line)

`res["noowner"]` (lines 75, 214) is initialized and printed (line 127) but never incremented anywhere;
the frozen met line's `noowner=0` conjunct is vacuous — the empty-owner case is caught by `thin`
(receipt line 3: `thin:tools/h.py:owner`).

## Restoration evidence

- Lane counter bytes untouched: `sha256sum .ufo/waves/round-61/count-c1.py` before first run and after
  all runs = `a6684e697583746e8b6318d6984f3ada5e619c45a0a3449ecf46d79193433e00` (matches `PIN_C1` in
  `count-c3.py`; selftest and control receipts reproduce byte-for-byte at the end of the session).
- No writes outside the seat scratch and this report; no commits, no VCS mutation anywhere; every lane
  git call read-only (`show`, `cat-file -e`, `rev-parse`, `status`, `log`, `diff`). Fixture repos created
  only under `/fast/scratch/hyaku/mori-r61/Mo61MutC1b/fx-*`, every git call naming `git -C "$D"`, with
  the toplevel assertion passing before each commit. Scratch removed after this report (receipts above
  are verbatim copies).
