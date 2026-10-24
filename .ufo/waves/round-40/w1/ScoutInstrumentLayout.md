# ScoutInstrumentLayout — round-40 instrument tree vs contract evidence-paths list

Seat: scout (read-only; no edits). Measured on the scored working tree under
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/` (scored tip
265a955cc… per wave context). This item shipped no `Report:` trailer; the
path follows the wave convention (`reportDir` in `w1-spec.json` =
`.ufo/waves/round-40/w1`, `<SeatName>.md` per round-38/39 w1).

## Commands run (exact) and what they produced

1. `find /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-40/ -type f -o -type d | sort`
   → 75 paths total: contract.md, conform.py, count-c8.py, gen-wave-spec.py,
   w1-spec.json; `evidence/` (41 files), `fixtures/` (2 builders, 4 witness
   payloads, `extracted/` 3 files, `generated/` 12 files), `scratch/` 2 drafts,
   `__pycache__/` 2 pyc. No `w1/` dir yet.
2. `ls -la …/evidence/` → 41 files = 39 `.txt` receipts/plan + **2 dotfiles**
   `.parity-c7.txt`, `.parity-c8.txt`.
3. `cat …/evidence/freeze-r40.txt` → sha256 pins for 9 frozen paths
   (contract.md, count-c8.py, conform.py, tools/mori-sources-appendonly.py,
   fixtures/make-survivor-fixtures.py, fixtures/run-c11-dags.py,
   fixtures/extracted/{conform-v2-r39,count-c7-r39,gate-v2-bb1f2457}.py).
   All 9 exist on disk.
4. `head -5 …/evidence/.parity-c7.txt .parity-c8.txt` → both are P-C7
   drift-corpus receipts ("negative witness-* rejected" verdicts); c7/c8
   runs of the same probe, parked as dotfiles.
5. `cat …/evidence/c10-parity.txt` (306 B) → receipts byte-identical for
   count-c7-r39 vs count-c8 at rev bb1f2457, seed 20261024, exit 0 both.
6. `grep -l 'barecomm' …/evidence/*.txt` → `c10-red-multicounter.txt`,
   `c10-after-multicounter.txt` (barecomm is the audit's second counter).
7. `grep -n … …/fixtures/make-survivor-fixtures.py` → `fixtures[…]` table
   builds 10 names: shadow-none, shadow-neg, cond, inf, divzero, decoy,
   underscore, tuple, second-popen, **barecomm** ("multi-counter control").
8. `grep -n … …/fixtures/run-c11-dags.py` → `Usage: run-c11-dags.py
   <gate-script> <lane-repo> <out.txt> [kind …]`; `P11_KINDS =
   ("dag-n","dag-p","dag-r")`; DAGs built via `tempfile.mkdtemp(…,
   dir=…/.scratch)` — dag-n/p/r are fixture *kinds*, not committed files.
9. `ls tools/mori-sources-appendonly.py corpus/knowledge/conform-scope-r40.md
   corpus/lessons/round-39-erratum.md` → all three exist (contract-cited).
10. `ls …/waves/round-39/w1/ …/waves/round-38/w1/` → `<SeatName>.md` report
    naming convention.

## Contract 'P-C10/P-C11 evidence paths' list (contract.md:151-153) → disk

Every list entry resolves; nothing listed is missing from disk:

| List entry | Disk | Count |
|---|---|---|
| `evidence/freeze-r40.txt` | ✅ present | 1 |
| `evidence/census-start.txt` | ✅ present | 1 |
| `census-end.txt` | ✅ present (bare-name style) | 1 |
| `evidence/c10-red-*.txt` | ✅ cond, conjunct, decoy, divzero, inf, multicounter, second-popen, shadow-neg, shadow-none, tuple, underscore | 11 |
| `c10-after*.txt` | ✅ base `c10-after.txt` + cond, conjunct, decoy, divzero, inf, multicounter, second-popen, selftest, shadow-neg, shadow-none, tuple, underscore | 13 |
| `evidence/c11-red-*.txt` | ✅ firstparent, neveredited, readd | 3 |
| `c11-before-lane.txt` | ✅ present | 1 |
| `c11-after*.txt` | ✅ e37dcc6, fixture-n, fixture-p, fixture-r, lane, selftest | 6 |

Per-file match against the contract's **named** receipts: all named
c10-red/c10-after/c11-red/c11-after files exist (9 survivors + conjunct +
multicounter + selftest + base for c10; lane/e37dcc6/selftest/3 fixtures for
c11). Exact-set match, no orphans, no gaps.

## On disk under `evidence/` but NOT covered by the contract list — 3 cases

1. **`evidence/c10-parity.txt`** — *the* material gap: contract.md:71 cites
   it in prose ("proven in `evidence/c10-parity.txt`") yet the list's globs
   `c10-red-*`/`c10-after*` do not match it. Contract-cited evidence outside
   the declared evidence-paths list.
2. **`evidence/wave-plan.txt`** — wave dispatch-plan JSON (91 KB, schema
   `ufo-swarm-wave-v1`); on disk, unlisted.
3. **`evidence/.parity-c7.txt`, `evidence/.parity-c8.txt`** — hidden dotfile
   receipts of the P-C7 drift probe run on the c7 and c8 counters; unlisted
   and invisible to `*.txt` enumeration. [INFERENCE] likely scratch receipts
   parked before the visible `c10-parity.txt` was committed — their content
   is P-C7, which is out-of-claim this round.

## Tree items outside `evidence/` (list is evidence-scoped; none expected)

- Instruments: `contract.md`, `conform.py`, `count-c8.py`,
  `tools/mori-sources-appendonly.py` (tracked, outside `.ufo`).
- Fixtures: `make-survivor-fixtures.py`, `run-c11-dags.py`, 4 `witness-*`
  payloads, `extracted/` (conform-v2-r39.py, count-c7-r39.py,
  gate-v2-bb1f2457.py — all freeze-pinned), `generated/` (10 survivors
  incl. barecomm + 2 conjunct-gutted checker copies).
- Wave artifacts: `w1-spec.json`, `gen-wave-spec.py`,
  `evidence/wave-plan.txt`; `scratch/selftest-v3-draft{,2}.txt`;
  `__pycache__/{conform,count-c8}.cpython-314.pyc`.

Consistency notes (non-defects):
- `survivor-barecomm.py` has no per-fixture receipt but is exercised as the
  second counter inside `c10-{red,after}-multicounter.txt` — coherent.
- dag-n/dag-p/dag-r payloads are not committed; built ephemerally into
  `.scratch` per run — matches the contract's "`fixtures/run-c11-dags.py`
  output" phrasing.
- Adjacent observation (routed to other seats, flagged not claimed): the
  as-of id count is stated three different ways — contract P-C11
  parenthetical "(19 ids)", wave context/item prose "34 as-of ids", while
  the committed receipt `c11-after-lane.txt` line 22 measures **35**
  (`sed -n '22p' … | sed 's/.*as_of=\[//; s/\] stale.*//' | tr ',' '\n' |
  grep -c 'S[0-9]'` → 35; the same 35 ids appear in line 21's
  `superseded=[…]` field; `stale_supersede=[]`, `EXIT=1`). Before-receipt
  `c11-before-lane.txt` carries the declared 18 ids — so the extension
  added 17 never-edited ids incl. S226, not the 16 implied by "34".
- List prefix style is inconsistent (four entries drop `evidence/`):
  `census-end.txt`, `c10-after*.txt`, `c11-before-lane.txt`,
  `c11-after*.txt` — cosmetic only.

## Verdict

- Missing from disk that the contract lists: **none**.
- On disk missing from the contract list: **`c10-parity.txt`** (cited in
  prose, should be added to the list), `wave-plan.txt`, and the two hidden
  `.parity-c{7,8}.txt` receipts. Classification: list-omission erratum
  class for the first; house-keeping class for the rest.

No tools installed; read-only seat.
