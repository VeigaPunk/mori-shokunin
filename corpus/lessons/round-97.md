# Round 97 — lesson (mori, L1 MoriR97, attempt 1)

Fresh-start round (amendment 35). Read first: `corpus/lessons/round-94-verifier-spotcheck.md`,
`round-95-verifier-spotcheck.md`, `round-96-verifier-spotcheck.md` (three rejected-honest-stop closures).
Frozen contract `.ufo/waves/round-97/contract.md` at freeze `dd1ae1150f53df54e7530311b2323368e3c0e5e9`, entering
`973b2af11f41bd362163d7e29ac08286832f546b`. Every control (do-nothing, forgery, positive) ran and was committed
with the freeze: `.ufo/waves/round-97/evidence/controls-r97.txt` (`CONTROLS_DONE unexpected=0`).

## Claims (frozen)

- **C1 operability** — the gate registry (`SKILL.md`) gains rows for the four tools the auditor reported
  unregistered; each row states the selftest outcome the frozen counter re-runs and requires verbatim.
  Before `C1=unmet unregistered=4 registry=unmet targets_ok=0/4`; target `C1=met unregistered=0 registry=met targets_ok=4/4`.
- **C2 freshness** — S615, S616, S623 (flagged stale at r96) are pinned with the exact bytes their recorded digests name
  and re-verified against a fresh live fetch under the r66 stamp grammar. Before `C2=unmet ... unpinned=3 targets_ok=0/3`;
  target `C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass`, live classes in {fresh, time-churn}.

## Gate

New row written this round (CORPUS rule 1):

| row | URL | access (UTC) | located quote (≤25 words) | decision |
|---|---|---|---|---|
| S628 | https://github.com/python/docsbuild-scripts (raw `https://raw.githubusercontent.com/python/docsbuild-scripts/main/README.md`) | 2026-11-05 ~20:45, HTTP 200, 6835 B, sha256 `0ae6b880…c618` | "This repository contains scripts for automatically building the Python documentation on docs.python.org." (pinned copy `corpus/evidence/sources-r97/S628.md` raw lines 6-7, 14 words) | **admit, mined, tier B** (the project's own repository README, not a spec): grounds that docs.python.org bytes are an automated build artifact, so with S577 a stamp-only delta is build churn. Limit named in the row: it does not state the rebuild cadence. |

Re-opened this round (existing rows, no in-place edit; `status`, `recheck`, `used-by` unchanged):

| row | URL | access (UTC) | evidence | decision |
|---|---|---|---|---|
| S615 | https://docs.python.org/3/library/ast.html | 2026-11-05 ~20:45 | live 362,493 B sha256 `d5d9d590…5e8f`, stamp `Last updated on Nov 05, 2026 (12:47 UTC).` at line 3328; replacing only that stamp with `(00:37 UTC)` hashes to `7891c588…42f5` = the r90 copy = S619's recorded correction | **admit pin** `corpus/evidence/sources-r97/S615.html` (the r90 bytes); the digest gate prints `superseded-by S619` (S615's own recorded digest is the r91 C-1 mis-record; not edited) |
| S616 | https://docs.python.org/3/library/tokenize.html | 2026-11-05 ~20:45 | live 53,982 B sha256 `bce32489…da0e`; stamp `(00:37 UTC)` restored → `6842ed0f…cb72` = recorded = the r90 copy | **admit pin** `corpus/evidence/sources-r97/S616.html` (the r90 bytes) |
| S623 | https://docs.python.org/3/using/cmdline.html | 2026-11-05 ~20:45 | live 171,073 B sha256 `57b7f76b…6811`; stamp `(08:02 UTC)` restored → `90ac3b25…31ad0` = recorded | **admit pin** `corpus/evidence/sources-r97/S623.html` (reconstructed bytes; sha256 equality with the recorded digest proves them the recorded fetch) |

Rejected this round: pinning today's live bytes as the copy of a recorded row (the r96 method). Reason: the bytes differ
from what the row recorded, so the digest gate must say `mismatch` (control `C2 forgery: today's live S616 bytes`,
`mismatch=1`). Flip: never for a recorded row — a new row with its own digest would be the route (CORPUS rule 2).

Assimilation: none this round (`/home/vgpnk/Projects/shokuknow/merge/mori/` exists; no theme fits these two claims).

## Mistakes (CORPUS: class · evidence · captured-by · fix)

| # | Class | Evidence | Captured-by | Fix |
|---|---|---|---|---|
| 1 | instrument amnesia: r96 froze a freshness predicate (`live == recorded`) that a per-build page stamp can never meet, while the lane already held the stamp grammar (`tools/mori-drift-recheck.py`, r66, `time-churn`) and a correction row (S619) | `.ufo/waves/round-96/contract.md` P2; `corpus/lessons/round-96-verifier-spotcheck.md:71-89`; `tools/mori-drift-recheck.py:30-80` | none — the tool had no registry row, so nothing in the lane's gate home pointed a freeze at it (r96 routed defect 1) | C1 registers it (row "drift re-check (r66 tool, registry r97)"); C2 binds it as leg (d). Shown able to fail: control `C2 forgery: correct pins, S623 row pointed at another live page` → `content-drift`, `checks_failed=live` |
| 2 | evidence loss: r96 deleted `w2-validator.err` before commit; the refusal survived only as prose | `corpus/lessons/round-96-verifier-spotcheck.md:145-149` | the r96 closure (routed defect 2) | this round commits every validator output under `.ufo/waves/round-97/` (`w1-validator.out`) |
| 3 | supersession hole: the digest gate supersedes a predecessor whose copy merely mismatches, so any 362,493-byte file at S615 escapes `mismatch=` | `.ufo/waves/round-96/w1/digest/DigestExec.md` (note for L1); r96 routed defect 5 | none in the tool | documented in the tool's new registry row; guarded in the frozen C2 counter (`hole_guard`). Shown able to fail: control `C2 forgery: random 362493-byte S615 copy` → `hole_guard=fail` |
| 4 | junk-row false green: the gate-registry auditor accepts any eight-cell row whose entry names the tool | control `C1 forgery: eight-cell junk rows` → auditor `REGISTRY=met`, counter `targets_ok=0/4` | none in the auditor | the frozen C1 counter checks stated selftest outcome + verdict token; the auditor itself is not amended this round (carried) |

## r96 closure routed defects — disposition

1. Unregistered gates → C1. 2. Evidence loss → Mistake 2. 3. `w1-results.json` schema gap → orchestrator-owned file,
not lane-editable; read from results.json as delivered. 4. Lab bookkeeping contradiction (r96 `Lab-digest-stability.md`
S125 label) → recorded here as an erratum of record: the S125 row label `falsified-no-match` compared the entry markdown
digest with the receipt digest; the landing receipt `S125 ok` stands; the r96 file is not edited. 5. Supersession hole →
Mistake 3. 6. Framing: 124 is the digest tool's evaluated-row count, not the registry size (399 rows entering, 400 after S628).
7. Carried debts (mutation sweep of the calibration counter, frozen r79 survivors M2/M5/M6, D1 planner binding,
r95 m8/m10/m11) → carried to round 98; the sweep of the r97 counters runs in this round's wave.

## Frontier step

- Census before: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → exit 0 (`mori ok`,
  42 W04). Census after: see the report (must be exit 0).
- Sourced claim: C2 cites S628 (opened this round) for the build-churn reading of the stamp delta.
- Frontier rows advanced: none.
