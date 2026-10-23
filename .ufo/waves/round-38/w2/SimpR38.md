# SimpR38 — dead-weight findings (mori round 38, wave 2)

Seat role: simplifier. Scope: dead weight the round added — duplicate receipts,
superseded-but-cited artifacts, redundant fixtures, unused counter flags,
report-only files duplicating a receipt. Detection only; every row below is a
*proposal* with what would be lost. Nothing here deletes a path a committed
claim (contract.md, the frozen counters' fixture loads) or a landed receipt cites.

Axes: (a) byte weight, (b) single-evidence authority, (c) zero harm to
committed claims / the w2 closure gate. Frontier walk: keep rows that improve
(a) or (b) and harm nothing on (c).

## Verified citation map (run, not read)

- Tracked at `HEAD = f725f3076972e6e70595b5ac8279be524a111ff8` (the scored tip):
  `git ls-files .ufo/waves/round-38` lists 32 files; `git ls-files` under
  `scratch/` returns **0** — all 3.8 GB of `scratch/` (`du -sh`) is untracked.
- Contract §Evidence paths (`contract.md:142-146`) cites `evidence/c1-before-rerun.txt`,
  which **does not exist**; the re-emitted receipts are `c1-before-rerun-memo.txt`
  and `c1-before-rerun-summary.txt` (contract.md:34 cites the memo/summary pair's
  round by name; `corpus/lessons/round-38.md:53` cites the glob
  `evidence/c1-before-rerun-*.txt`). Stale citation on a frozen path — flagged,
  not a deletion.
- `freeze-r38.txt` vs `freeze-r38-v2.txt`: v1 pins pre-change counters
  (`count-c1.py 4e59eeff`, `count-c4.py 5d416a1c`), v2 pins the shipped bytes
  (`9ebf10a1`, `3340d594`) plus `fixtures/memo-sha.py`. Contract:7 cites v1
  explicitly; `w1-dispatch.json`/`gen-wave-spec.py:207` cite v2. **Both retained.**
- Fixture duplication measured: `const.py`, `memo-n1.py`, `summary-only.py` are
  **byte-identical** between round-37 and round-38 fixtures (sha256 equal).
  All three are pinned by both freeze files and loaded by `count-c1.py:975-981`
  — frozen, not deletable. `memo-sha.py` is live: `count-c1.py:1104` loads it as
  the content-keyed bound. `hang-after-flush.py` is loaded by `conform.py:42`;
  the three `witness-*` files by `count-c4.py:293-317`.
- Flags audit: every `add_argument` in `count-c1.py` (`--repo`, `--tool`,
  `--negatives`, `--seed`, `--tool-timeout`, `--print-predicate`, `--pin-only`,
  `--print-tool`, `--arms`), `count-c4.py` (`--repo`), `conform.py` (`--repo`,
  `--contract`, `--counter`, `--selftest`) is exercised by `conform.py`'s six
  checks or the counters' own logic. **No unused flags found.**
- Claim-cited but **untracked** (worktree-only, `git status ??`): `c4-witness.txt`,
  `v3-token-control.txt`, `gate-after.txt`, `gate-after-e37dcc6.txt`,
  `gate-selftest-after.txt`, `c5-after-selftest.txt`, `census-end.txt`,
  `gen-wave2-spec.py`, `w2-spec.json`, `w2-dispatch.json`, all `w1/*.md`,
  `w2/*.md`. Retained — losing them loses the receipts the claims under attack
  cite. Freshness risk noted, not a deletion.

## Deletion proposals

| path | why dead | what depends on it | proposal |
|---|---|---|---|
| `.ufo/waves/round-38/scratch/ExecCensusSelftest/` (502 MB) | w1 seat was dispatched (`w1-dispatch.json:386,730`) but never produced a `w1/ExecCensusSelftest.md`; its `snapshot/` is a full repo checkout whose selftest tallies exist in no report. Only `w1/swarm-registry.json` names it (registry metadata, not evidence). | Nothing — no report, no receipt, no claim cites it. | Delete. Lost: a stale checkout + unreported partial artifacts; the seat's task is reproducible from `w1-dispatch.json`. |
| `.ufo/waves/round-38/scratch/ExecR17Battery/` (96 K) | Same shape: dispatched (`w1-dispatch.json:725`), no `w1/ExecR17Battery.md`. Contents: `checkout/tools/mori-round17-jj-regressions.py` copy + `selftest.out`, `selftest-run.out`. | Nothing — `grep` finds no citer outside `w1/swarm-registry.json`/`w1-dispatch.json`. | Delete. Lost: two run logs the seat never reported on. |
| `.ufo/waves/round-38/scratch/ExecWitnessSandbox/repo/` (253 MB) | Duplicate pristine clone inside the witness-sandbox seat dir; `git status` shows the C1-attacked `fabricated-binding/` is the only subdir named by receipts (`v3-token-control.txt`, `c4-witness.txt`, `w1/ExecWitnessSandbox.md:13`) and a w2 report (`w2/RevS226Row.md:30-31`). `repo/` + `c4-scratch/` have zero citers (grep run). | `fabricated-binding/` is receipt-cited → **keep**; `repo/` and `c4-scratch/` (empty dir) are not. | Delete `repo/` and the empty `c4-scratch/`; keep `fabricated-binding/` (claim-receipt subject, regenerable via `fixtures/make-witness-sandbox.py` but cited by committed receipts). |
| `scratch/c1-*` + `scratch/mori-c1-tool-*` leaked mkdtemp dirs (38 dirs, ~5.2 MB total) | `count-c1.py` creates these via `tempfile.mkdtemp(prefix="mori-c1-tool-", dir=_scratch_parent())`; the success path cleans (receipts name `mori-c1-tool-t9yrrg8q`/`_obesxsv`, both absent — proven). The 38 survivors are leaks from killed/erroring runs. | Nothing cited (grep `c1-vqu73jgj` etc. → zero hits). Caveat: `stat` shows dirs as fresh as 20:08 — live w2 seats create them too. | Delete only dirs older than the w2 dispatch timestamp (or after w2 closes). Lost: leaked scratch, nothing else. Also flags a cleanup-defect in the counter's error path for round 39. |
| `.ufo/waves/round-38/evidence/c1-v4-smoke.txt` (tracked) | Smoke receipt of the *pre-v4.1* counter run: prints the P-C1 v4 predicate against a `mori-c1-tool-_obesxsv` tool dir; superseded by `c1-after-r38.txt` (v4.1, `head_at_measurement=daa1d4d…` per `w1/ExecReplay.md:54`). Zero citers: contract's evidence list omits it; `grep` over `.ufo/waves/round-38`, `corpus`, `LOG.md` finds no reference. | Nothing. | Delete (tracked → needs a commit). Lost: provenance that the v4 build was smoke-tested before v4.1; that fact is already implied by the v2 freeze header. |
| `.ufo/waves/round-38/__pycache__/` (116 K) | Stale bytecode cache of `conform`/`count-c4`; gitignored (`git check-ignore` → IGNORED), untracked. | Regenerated on every import. | Delete (hygiene, zero loss). |
| `.ufo/waves/round-38/w2-validate.err` (untracked, 0 bytes) | Validator stderr stub; zero bytes, no citers. | Possibly the live validator's own stderr sink — if a redirect is open, unlink only detaches it. | Delete after the w2 validator run completes; keep if the validator is still writing to it. |

## Retained candidates (probed, rejected as deletions)

| path | why probed | verdict |
|---|---|---|
| `evidence/freeze-r38.txt` (v1 pins) | Superseded by v2 for the shipped counters | KEEP — `contract.md:7` cites it; v2's header names v1 historical. Explicit provenance. |
| `evidence/gate-after-e37dcc6.txt` | Looks like a dup of `gate-before.txt` (same rev `e37dcc6`) | KEEP — distinct: before-gate lacks `supersede_timing` (grep count 0), this one carries `stale_supersede=[S069]` under the *new* gate; w2 context cites it. |
| `fixtures/{const,memo-n1,summary-only}.py` | Byte-identical to round-37 fixtures | KEEP — pinned by both freeze files; loaded by `count-c1.py:975`. Frozen duplication, deletion impossible without breaking pins. |
| `gen-wave-spec.py` vs `gen-wave2-spec.py` | Two spec generators, one untracked | KEEP — different products (`w1-spec.json` vs `w2-spec.json`); neither is a copy (diff shows distinct CONTEXT/items). |
| `w1-run.log`, `w1-validate.log` (tracked, 0 bytes) | Zero-byte logs | KEEP — committed provenance of a completed w1 run; zero cost. |
| `scratch/SentWitnessSandbox/run-20261023/` (~253 MB inside 505 MB dir) | Full repo clone duplicating `fabricated-binding` | KEEP (caveat) — `w1/SentWitnessSandbox.md:7` cites the path and its commit `839e1b23`; different commit than `d2ee053`. Deleting it invalidates the FAIL report's re-derivation ground. Could be proposed once w2 closes, but the sentinel finding stands on it. |
| `scratch/ExecWitnessSandbox/fabricated-binding/` | Largest single artifact subject | KEEP — named by committed receipts `c4-witness.txt`/`v3-token-control.txt` and `w2/RevS226Row.md`. Deleting it is exactly the FAIL case in acceptance. |
| `scratch/RevC4Anchors/mori-source-drift-f725f30.py` | Orphan-looking file | KEEP — w2 spec item `RevMisroot` names it directly (lesson M9's copied artifact). |

## Tradeoffs / residual findings (no deletion proposed)

1. **Stale contract citation**: `contract.md:142-146` names `evidence/c1-before-rerun.txt`; only the `-memo`/`-summary` pair exists. Frozen file → a round-39 erratum should either mint the named file or correct the line.
2. **Counter leak defect (for round 39, not this round's deletion)**: 38 leaked `c1-*`/`mori-c1-tool-*` mkdtemp dirs prove `count-c1.py`/`count-c4.py` don't clean scratch on the killed/error paths. Delete-by-age is a workaround; the fix is a `finally:` cleanup or `TemporaryDirectory`.
3. **w1 dispatch↔report skew**: 70+ seats dispatched in `w1-dispatch.json`; 13 reports landed. The unreported seat dirs (`ExecCensusSelftest`, `ExecR17Battery`, `ExecGateDeterminism` [has report], etc.) are the wave-1 freeze's footprint — the two above have no report at all.
4. **Untracked claim receipts** (list above): the freeze/closure reads them from the worktree; they are *protected*, but a `git clean` would destroy the evidence chain. Recommend committing the `??` evidence files before wave close — out of scope for a leaf seat.
5. **w2-spec vs w2-reports skew**: 43 spec items, 37 reports present (`CritC4Gaming`, `CritC5Gaming`, `RevC5Timeout`, `RevMisroot`, `RevTrends`, `ConnReceipts`, `SimpR38` pending — expected mid-wave, not dead weight).

## Evidence commands run

`git ls-files` / `git status --porcelain` / `git ls-tree` (tracked vs untracked);
`du -sh` per scratch dir; `sha256sum` fixture pairs (r37 vs r38 identical);
`grep -rln` over `w1`, `w2`, `dispatch-log.txt`, `corpus`, `LOG.md` for every
candidate basename; `grep -c 'supersede_timing'` distinguishing the three gate
receipts; `stat`/`find -newer` for leak freshness; `python3 -c json` over
`w2-spec.json` (43 items) vs `w2/` listing (37 reports).

No installs performed. Nothing in the lane repo was modified; the only file
written is this report.

Report: .ufo/waves/round-38/w2/SimpR38.md
