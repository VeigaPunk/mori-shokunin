# RevC7Live — live_rows_v2 at 13bfba23

**Verdict: PASS. No mismatch with the counter's detail; every named drifted id is a
registry row with exactly one committed copy. No FAIL condition triggered.**

Scored revision: `13bfba23b7ca063c76d3504a2ff6eb7b6a294932`. Audited artifact
`.ufo/waves/round-37/evidence/drift-live-r37.txt`, blob
`66c17a2fe47e831ee36edf7d6b9b43ababa76c1f` at the scored tip; worktree bytes
sha256 `82d79f0d550412313765f440981e7a60acefb4e32b0cee6f008e584535686c16`,
identical to `git show 13bfba23:…` (checked). No lane file was modified.

## 1. Counts (per-row vs summary)

Parsed with the counter's own anchored patterns (`count-c7.py:94-96`):

| quantity | per-row lines | summary field |
|---|---|---|
| rows | 225 (`S001`–`S225`, contiguous, no gaps, 225 unique) | `rows=225` |
| fresh | 53 | `fresh=53` |
| excerpt | 0 | `excerpt=0` |
| drifted | **10** | `drifted=10` |
| unavailable | 0 | `unavailable=0` |
| no-copy | 162 | `no-copy=162` |

Summary at `.ufo/waves/round-37/evidence/drift-live-r37.txt:227`; `EXIT=1` at `:228`.
Both reconcile exactly (53+10+162 = 225). `EXIT=1` matches the tool's exit contract
`return 1 if counts["drifted"] else 0` (`tools/mori-source-drift.py:251`), so the
recorded exit is consistent with `drifted=10`.

The only non-row, non-summary line is the command annotation at `:1`
(`# at the 225-row registry, all five r37 copies committed`); it contains no
`S### drifted` text and cannot pad the count.

## 2. Named drifted ids → committed copy

The ten per-row `drifted` lines (`:157-161,177-178,211-212,224`) are unique. Each is
a registry row under the counter's registry pattern (`^\| (S\d{3}) `,
`count-c7.py:287-288`) against the 228-row `corpus/SOURCES.md` at the tip — 228 rows,
228 unique ids, no duplicate registry ids (`unknown=[]`).

| id | evidence line | committed copy at tip (highest `N`, unique) | bytes | `git cat-file -t` |
|---|---|---|---|---|
| S156 | :157 | `corpus/evidence/sources-r30/S156.txt` | 4249 | blob |
| S157 | :158 | `corpus/evidence/sources-r30/S157.txt` | 1181 | blob |
| S158 | :159 | `corpus/evidence/sources-r30/S158.txt` | 633 | blob |
| S159 | :160 | `corpus/evidence/sources-r30/S159.txt` | 1219 | blob |
| S160 | :161 | `corpus/evidence/sources-r30/S160.txt` | 2389 | blob |
| S176 | :177 | `corpus/evidence/sources-r32/S176.src` | 55620 | blob |
| S177 | :178 | `corpus/evidence/sources-r32/S177.src` | 20100 | blob |
| S210 | :211 | `corpus/evidence/sources-r36/S210.src` | 122463 | blob |
| S211 | :212 | `corpus/evidence/sources-r36/S211.src` | 196972 | blob |
| S223 | :224 | `corpus/evidence/sources-r37/S223.src` | 216510 | blob |

**Ids without a copy: none.** Each of the ten has exactly one `sources-r<N>/<id>.<ext>`
path; no older decoy copy competes, so "highest N" is unambiguous. Copies are
non-empty (633 B–216510 B), and `drifted` requires non-empty differing bytes
(`tools/mori-source-drift.py:200-208`: fresh iff sha256 equal, excerpt iff non-empty
stripped copy is contained in the body, otherwise drifted) — the drifted verdicts are
not satisfied by empty copies.

## 3. Canonical predicate, run at the scored tip

I did not restate my hand count as proof: I imported the frozen counter
(`.ufo/waves/round-39/count-c7.py`, sha256
`b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520`, matching
`evidence/freeze-r39.txt:2`) and executed its own `registry_ids`, `copy_paths_at`,
`check_live_rows_v2` (`:287,223,313`) on the tip's bytes:

```
canonical ids: 228 | copies: 66
canonical check: (True, 'named=10 summary_drifted=10 unknown=[] unique=True no_copy=[]')
```

This is byte-for-byte the detail recorded at
`.ufo/waves/round-39/evidence/c7-after.txt:9`
(`check live_rows_v2     PASS (named=10 summary_drifted=10 unknown=[] unique=True no_copy=[])`).
**No mismatch with the counter's detail.**

Negative controls on an in-memory copy (no lane mutation) all reject:

| mutation | predicate detail |
|---|---|
| duplicate `S156 drifted` | `named=11 … unique=False` → FAIL |
| rename one drifted line to `S103` (registry row, no copy) | `no_copy=['S103']` → FAIL |
| summary `drifted=9` | `named=10 summary_drifted=9` → FAIL |
| summary only, drifted lines deleted | `named=0 summary_drifted=10` → FAIL |
| replace with unregistered `S999` | `unknown=['S999'] no_copy=['S999']` → FAIL |

So the PASS is not vacuous: the arm kills count, uniqueness, copy and membership
mutations.

## 4. Runtime / receipt identity

- The receipt is a genuine 225-row sweep, not a splice: at its generating commit
  `4bfa0490264c342db8f5304bac059a32ac2cb20b` ("drift receipt regenerated at 225
  rows") the registry has exactly 225 ids (`S001`–`S225`), and the receipt's 225 row
  ids equal that registry **as an ordered list**, not just as a set.
- `4bfa049` is an ancestor of the scored tip; the receipt blob is identical at
  `4bfa049`, at `f920eaf7`, and at `13bfba23` (`66c17a2f…`), so no post-generation
  edit exists.
- One canonical runtime: `tools/mori-source-drift.py` is blob
  `162ee87b5b0789c6815f967f3db93d277bab38d9` / sha256
  `453c5d8e260301df7a99daf62b4c16ea08e4a0b4f9e4f53821cdbce447011552` at both
  `4bfa049` and the scored tip, matching the r37 freeze pin
  (`.ufo/waves/round-37/evidence/freeze-r37-v3.txt:13`).
- Closure of `no-copy`: 66 ids have a `sources-r<N>` copy at the tip; 63 are receipt
  rows (53 fresh + 10 drifted) and the other 3 are `S226,S227,S228` — rows added
  after the receipt. No `no-copy` row has a source copy, and no fresh/drifted row
  lacks one (checked programmatically).

## 5. Findings by severity

- **High / Medium: none.**
- **Low L1 — `rows=225` vs the 228-row registry at R.** `live_rows_v2` does not
  constrain `rows` against the registry size (`count-c7.py:313-327` reads only
  `drifted` and the named lines), so `S226`–`S228` are outside this receipt's sweep.
  This is not a P-C7 violation (P-C7 constrains one drifted line per counted drifted
  row, registry membership, and copies) and the receipt's own `:1` annotation scopes
  it to "the 225-row registry". Recorded so the receipt is not read as a full-tip
  census; the three new rows' copies exist (`sources-r38/S226.src`,
  `sources-r39/S227.src`, `sources-r39/S228.src`) but their per-row states are not
  evidenced here.
- **Low L2 — non-drifted per-row states are not cross-checked by the arm.** The
  predicate compares only `len(named)` with `drifted`; it would accept a receipt
  whose `fresh`/`no-copy` lines were altered as long as the drifted lines stayed
  consistent. In this receipt the non-drifted lines reconcile exactly (53/162/0/0),
  which I verified, but that reconciliation is reviewer-side, not counter-enforced.
- **Low L3 — receipt-run revision differs from the claim's revision.**
  `c7-after.txt:1` records `count-c7.py f920eaf7 --seed 20261024`, not the scored
  `13bfba23`. It is harmless for this arm: `f920eaf7` is an ancestor of the tip and
  the live receipt, `SOURCES.md`, `count-c7.py`, and `tools/mori-source-drift.py`
  are blob-identical at both revisions (checked). My own run at `13bfba23`
  reproduces the PASS, so the claim does not rest on the stale revision — but the
  receipt itself does not state the equivalence.
- **Low L4 — no LSP device.** `read xd://lsp` returned "No such tool"; only
  `ast_edit` and `debug` are mounted. Caller/definition checks were done by
  importing the frozen predicate and locating its call sites by text
  (`count-c7.py:473` real arm, `:539` negative fixture wiring). Recorded as a
  tooling gap, not semantic-LSP-verified.

## 6. Residual risk

- No network re-fetch at the tip: the `fresh`/`drifted` classification was not
  independently reproduced from today's source bodies. P-C7 is a receipt-coherence
  plus copy-existence check by design, not a truth check.
- **Disclosed clone bound, corroborated in-repo.** The arm cannot distinguish the
  real receipt from a self-consistent fabricated one that *also* commits a copy for
  every id it names: `.ufo/waves/round-39/scratch/RevC7Clone/logs/clone2-c7.log:8`
  records `live_rows_v2 PASS (named=11 summary_drifted=11 unknown=[] unique=True
  no_copy=[])` on the clone whose receipt adds `S103` plus a matching copy, while the
  same clone without that copy is rejected (`clone1-c7.log:8`,
  `no_copy=['S103']`). Copy existence raises the fabrication cost; it is not
  provenance. The real receipt has independent corroboration — ordered registry-exact
  equality with the 225-row registry at its generating commit `4bfa049` and blob
  identity across `4bfa049`/`f920eaf7`/tip — but neither proves a live fetch occurred.
- The 228-row registry at R makes membership easy to satisfy for any old id; ruled
  out here by the exact ordered set equality with the 225-row registry at the
  generating commit.
- Negative mutations were applied to an in-memory string only; the lane file was
  never written.

## 7. Verification gaps

- Live re-execution of `tools/mori-source-drift.py --root .` (63 fetches, up to
  `timeout 900`) was not run; out of the assigned scope and unnecessary for
  `live_rows_v2`, which binds the receipt.
- LSP unavailable (L4), so "no other callers" is a text-search claim.
- I ran the canonical predicate at `13bfba23` in `$TMPDIR`/scratch only; the counter
  `main()` (which writes its own scratch) was not invoked.

## 8. Tooling

No tools installed or upgraded. Scratch: empty directory
`.ufo/waves/round-39/scratch/RevC7Live/` created; temporary `/tmp/SOURCES-tip.md`
removed. Exactly one file written: this report.
