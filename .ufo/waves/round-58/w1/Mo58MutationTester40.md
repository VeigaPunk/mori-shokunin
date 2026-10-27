# Mo58MutationTester40 — cross-claim no-harm probe (round 58 w1)

Seat: Mo58MutationTester40 (mutation-tester, leaf — no subagents). Scope: falsifier, axis
overlap, frozen-rule drift, and detection/report boundary bleed across the frozen round-58
contract + counters and the round-56/57 records. Method: read-only inspection of the lane at
freeze `fe8801120a67c1a6b8899d7d0423839caa09e7d0` plus bounded mutation probes that run the
**pristine frozen counter bytes** against throwaway fixture repos under
`/fast/scratch/hyaku/mori-r58/Mo58MutationTester40/` (every git op `git -C <fixture>` after
asserting `rev-parse --show-toplevel` == fixture dir). No production byte, VCS, registry,
SCORECARD, or LOG mutation; no fleet/sibling writes; no tool installs. Disk guard checked
green before work (`/fast/scratch/hyaku` 553.5G free).

## 1. Frozen-rule drift — NO COUNTEREXAMPLE

All five frozen round-58 files are byte-identical between the freeze revision and the working
tree (sha256, frozen `git show fe88011:<path>` vs working file):

| file | sha256 (frozen == working) |
|---|---|
| `.ufo/waves/round-58/contract.md` | `3aeff1d1766f4ddcc8732924a77ea48767fb9695515c71e76ea175546d2e5223` |
| `.ufo/waves/round-58/count-c1.py` | `6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b` |
| `.ufo/waves/round-58/count-c2.py` | `aab888ad787964f7a153d64d85dafa58f652f977e21e22eaa492706a691010d3` |
| `.ufo/waves/round-58/evidence/controls.txt` | `044f7082b0a069ef10b6d80936d8bfaeac4956a8dcbfe35dcd962bef527e475f` |
| `.ufo/waves/round-58/evidence/census-start.txt` | `80f4abf0a423ca9e47ce4f8ba18661d0d403e93292f52b7a8b88e661291c0a2c` |

`git status --porcelain .ufo/waves/round-58` shows only untracked sibling w1/evidence outputs;
no frozen file modified. Counters absent at entering revision (contract's before-control
honest): `git cat-file -e b783d0b8…:{count-c1,count-c2}.py` → rc=128 both. Contract
cross-references verified at freeze: `corpus/lessons/round-57-verifier-spotcheck.md:70-74`
routed defects 1–3 match the contract's summary (active-register identity; pointer
`git cat-file -e` resolution + quote-substring pinning; byte-faithful quotes) — no misquote
drift. `SCORECARD.md` at freeze carries the stub `## Capabilities` and the active register
whose preamble contains the exact binding sentence; register rows at :1989–1990 carry the two
`rounds[832]` keys with `.ufo/waves/round-56/evidence/{c2,c1}-at-landed.txt` pointers. Fleet
`MANIFEST.json` `rounds[832].capabilities_added[0]` contains "vote binding" and `[1]`
contains "driver-liveness" — the C1 manifest arm is honestly satisfiable as written.

## 2. Axis overlap — NO COUNTEREXAMPLE

C1 reads `SCORECARD.md` at R plus fleet `MANIFEST.json`; C2 reads
`corpus/knowledge/driver-events-r58.md`, the pinned copy, `tools/mori-driver-liveness.py`, and
`corpus/SOURCES.md` — all at R. Distinct artifacts, distinct predicates, no shared acceptance
artifact and no mutual predicate dependency (matches the r57 scout's finding at
`.ufo/waves/round-57/w1/Mo57Scout55.md`). The only shared surface is the existence of
`tools/mori-driver-liveness.py` (C1: bare `cat-file -e` on the register-row pointer; C2:
sha256 self-consistency copy==tool **at the same R**). Neither counter scores the same
evidence twice; killing one claim's instrument does not touch the other's. Falsifier history
is consistent: the two r57-routed defects (wrong-table binding; unverified pointers/quotes)
are exactly the arms the r58 counters add, and the r58 controls
(`evidence/controls.txt`) reproduce the r57 counter's `C1=unmet rows=0 evidence=bad` contrast.

## 3. Detection/report boundary bleed — NO COUNTEREXAMPLE (one live-input note, F3)

Neither counter reads anything under `.ufo/waves/round-58/w1/` (no seat report, receipt, or
`w1-results.json` input); neither writes into the repo — outputs are stdout only, and all
writes (selftest fixtures) go under `tempfile.mkdtemp(TMPDIR)` with `shutil.rmtree` cleanup;
all measured-repo git ops are read-only (`show`, `cat-file -e`). Fixture git ops in both
selftests are `git -C <tempdir>` with throwaway identity. The one live (non-rev-pinned)
external input: C1's manifest arm reads the **working-tree** fleet
`/home/vgpnk/Projects/shokunin/MANIFEST.json` regardless of the measured `rev=R` — see F3.

## 4. Mutation probes (pristine counters, throwaway fixtures)

Detector: `python3 <fixture>/.ufo/waves/round-58/count-{c1,c2}.py <fixture-rev>` — the frozen
bytes copied unchanged (hashes above, verified identical pre/post). Fixture register mimics
the landed row shape (BIND_SENT preamble, `| key | capability |` header, 10 pad key-rows, two
`rounds[832]` rows); fixture manifest carries the two hints; C2 fixture pins copy==tool bytes
and an S550 row with used-by.

| # | mutant input (smallest behavior-bearing point) | expected per frozen contract | observed (rc) | verdict |
|---|---|---|---|---|
| base | C1 rows, evidence `` `tools/…`; `.ufo/waves/round-56/evidence/c2-at-landed.txt` `` | `C1=met` rc 0 | `C1=met rows=2 pointers=ok manifest=ok binding=ok` (0) | baseline honest |
| M-A | row[0] evidence → `` `evidence/absent.txt` `` (absent at R, prefix **not** in `.ufo/|tools/|corpus/`) | §9: "nonexistent evidence path MUST score `C1=unmet … failed=pointers`" | **`C1=met rows=2 pointers=ok … failed=none` (0)** | **SURVIVED** |
| M-B | row[0] evidence → `` `absent.txt` `` (absent at R, no `/`, `.txt` suffix) | same §9 requirement | **`C1=met rows=2 pointers=ok … failed=none` (0)** | **SURVIVED** |
| M-C | row[0] evidence → `` `tools/no-such-tool.py` `` (absent, covered prefix) | `C1=unmet failed=pointers` rc 1 | `C1=unmet rows=2 pointers=bad … failed=pointers` (1) | KILLED — detector alive on covered prefixes |
| M-D | pristine rows; manifest caps[1] hint "driver-liveness" removed | `C1=unmet manifest=bad` rc 1 | `C1=unmet rows=2 pointers=ok manifest=bad … failed=manifest` (1) | KILLED — and demonstrates the live-input flip (F3) |
| base2 | C2 entry, needles at top, 8 quote-bound K-lines | `C2=met` rc 0 | `C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok` (0) | baseline honest |
| M-E | same claims, but `source:/verified-at:/recheck:/coverage-map:` moved to the entry **bottom** (no frontmatter) | (c): "frontmatter missing … MUST score `sources=bad`" | **`C2=met claims=8 located=8 … sources=ok failed=none` (0)** | **SURVIVED** |
| M-F | 8 K-lines with fabricated quotes | `C2=unmet failed=quotes` rc 1 | `C2=unmet claims=8 located=0 … failed=quotes` (1) | KILLED — quote binding alive |

Incidental fail-closed observation (first run): two paths inside ONE backtick span
(`` `tools/x.py; .ufo/y.txt` ``) resolve as a single nonexistent path and fail `pointers` —
the arm fails closed on that malformation, so the landed rows' per-path backticked style is
the only resolving shape.

### Receipt (verbatim probe output, probe-run2)

```json
{
 "pre_hashes":  {"count-c1.py": "6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b",
                 "count-c2.py": "aab888ad787964f7a153d64d85dafa58f652f977e21e22eaa492706a691010d3"},
 "post_hashes": {"count-c1.py": "6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b",
                 "count-c2.py": "aab888ad787964f7a153d64d85dafa58f652f977e21e22eaa492706a691010d3"},
 "frozen_paths_porcelain_after": "(empty — untouched)",
 "results": [
  {"case": "c1.baseline.pristine", "rc": 0, "out": "C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=c2ab2c53819a356c1b6a95fac20fc35144552aa9"},
  {"case": "c1.M-A.uncovered_prefix_absent_ptr", "rc": 0, "out": "C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=903a5fc693122e61c19a2448b6debe3003b4c17f"},
  {"case": "c1.M-B.root_rel_absent_ptr", "rc": 0, "out": "C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=0c0a4a8734503e534ad93297468bc3fd93820ebc"},
  {"case": "c1.M-C.covered_prefix_absent_ptr.control", "rc": 1, "out": "C1=unmet rows=2 pointers=bad manifest=ok binding=ok failed=pointers rev=ad07d9ffd9c9d6c5e5a2ec0771851c636fcdc323"},
  {"case": "c1.M-D.live_manifest_hint_flip", "rc": 1, "out": "C1=unmet rows=2 pointers=ok manifest=bad binding=ok failed=manifest rev=c2ab2c53819a356c1b6a95fac20fc35144552aa9"},
  {"case": "c1.restore.baseline_rerun", "rc": 0, "out": "C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=c2ab2c53819a356c1b6a95fac20fc35144552aa9"},
  {"case": "c2.baseline.frontmatter_top.control", "rc": 0, "out": "C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none rev=48d6d29470276dbd14157708eee2323d3abed050"},
  {"case": "c2.M-E.needles_not_in_frontmatter", "rc": 0, "out": "C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none rev=b10b75a7a88c2522cdbff7779b5d0a798f5f18f9"},
  {"case": "c2.M-F.fabricated_quotes.control", "rc": 1, "out": "C2=unmet claims=8 located=0 copy=ok tree=ok rows=ok sources=ok failed=quotes rev=7a5b719f4dd95e28b79be4f47ecf2f9d2ef0d649"}
 ]
}
```

## 5. Findings (coverage findings on frozen instruments — no remediation proposed; kill rules forbid byte edits)

- **F1 (MED, falsifier coverage) — C1 pointer arm silently skips any backticked evidence span
  not starting `.ufo/`, `tools/`, or `corpus/`** (`count-c1.py` pointer loop: the second
  `startswith` filter gates `cat-file -e`). M-A/M-B: a fixture register whose row names a
  nonexistent evidence path **outside those prefixes prints `C1=met pointers=ok`**, against
  contract §9's unconditional "a fixture register whose two rows name a nonexistent evidence
  path MUST score `C1=unmet … failed=pointers`". The selftest's only bad-pointer case uses
  `tools/no-such-tool.py` (covered prefix), so the do-nothing control battery does not cover
  this class. Bounded to adversarial/junk trees: the landed rows' pointers are all under
  covered prefixes and do resolve (controls.txt `C1=met rows=2 pointers=ok` at entering), so
  the landed claim itself is honestly verified. Named limit for L1 routing.
- **F2 (LOW, falsifier coverage) — C2 "frontmatter" arm is presence-only, not
  position-scoped.** M-E: the four required needles placed after the claims (no frontmatter at
  all) still print `sources=ok`, against contract control (c)'s "frontmatter missing … MUST
  score `sources=bad`". Landed entry shape is unaffected (fields at top, fixture-verified
  baseline `sources=ok`); the gap is on adversarial trees only.
- **F3 (LOW, detection/report boundary) — C1's manifest arm reads the live working-tree fleet
  `MANIFEST.json`, unpinned and uncovered by the kill rule** (which freezes only counter
  bytes, predicate sentence, target output). M-D shows the verdict flipping on manifest bytes
  alone with zero lane-VCS or frozen-byte change, so the printed `rev=R` understates the
  input surface for C1 (C2 is fully rev-pinned). Contract wording ("bound to fleet
  MANIFEST.json …") arguably sanctions the live read; recorded as a boundary note, not a
  violation.
- **No-counterexample results:** frozen-rule drift — none (§1); axis overlap — none (§2);
  report-boundary bleed — none (§3, F3 noted). Detector-alive controls (M-C, M-F) and honest
  baselines (base, base2, restore) all behaved as contracted.

## 6. Restoration and cleanup evidence

- Production counters never written: sha256 before == after all probes (both rows of the
  receipt above); `git status --porcelain` over the three frozen round-58 files → empty.
- All mutants/fixures existed only under
  `/fast/scratch/hyaku/mori-r58/Mo58MutationTester40/`; fixture commits used throwaway
  identity strictly inside `git -C <fixture>` repos; TMPDIR pointed at the seat scratch `tmp/`.
- Scratch directory removed after this report was written (cleanup line at seat end).

Report: .ufo/waves/round-58/w1/Mo58MutationTester40.md
