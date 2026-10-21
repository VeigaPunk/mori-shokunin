# LiveTabi — C2 falsification: live settlement-scan accuracy on lane tabi

**Verdict: HOLDS.** The scan of 2026-10-21 08:01:39-03:00 reproduces the independent wave-1 ground
truth (GtLaneTabi, T2 = 07:36:48–07:36:54) and the committed fleet evidence
(c2-live-fleet.json, written 07:46:53; captured 10:46:50Z per knowledge §5) exactly, after
attributing every difference to live lane change with file mtimes. **Zero tool errors found.**
No installs or updates were performed (none needed). Read-only bounds respected; leaf seat, no subagents.

## 1. What I ran

```
python3 mori-shokunin/tools/mori-wave-settlement.py scan \
  --lane-root /home/vgpnk/Projects/shokunin/tabi-shokunin \
  --fleet-root /home/vgpnk/Projects/shokunin \
  --out mori-shokunin/.ufo/waves/round-20/falsify/LiveTabi/scan.json
```
Start 08:01:39-03:00, finished same second, **EXIT=1** (partial/unsettled waves exist — contract
"1 any other state", correct, matches committed evidence `exit:1`). Second run into `scan2.json`
at ~08:04–08:05, EXIT=1. Tool sha256 = `e5c06dad076b8e5aebbebcd53cf7c32de41592b4899319502b8cca003d4b8a48`
= the hash pinned in `corpus/knowledge/wave-settlement-r20.md` — the bytes reviewed are the claimed bytes.
`--selftest`: **PASS (22 cases, 22 passed, 0 failed)**, exit 0 (14 frozen + 8 refinement cases,
grep counts 8 `{"id": "r` entries). Note: with `TMPDIR` pointing at a nonexistent dir the selftest
prints FAIL(0/22) — selftest-only TMPDIR dependency, not on the scan path.

## 2. Three snapshots of the same lane

| metric | GT T2 07:36:54 | committed fleet 07:46:50 | my scan 08:01:39 |
|---|---|---|---|
| dispatch waves | 67 | 67 | **16** |
| members | 3932 | 3932 | **1007** |
| present | 3357 | 3371 | **891** |
| missing | 575 | 561 | **116** |
| empty / misrooted / unparsed / unsafe | 0/0/0/0 | 0/0/0/0 | **0/0/0/0** |
| canonical-only present / missing | 876 / 131 | 890 / 117 | 891 / 116 |

Canonical = the 16 dispatch files directly under `.ufo/waves/` (GT §3 rows 1–14, 66, 67); the
other 51 GT rows were clones under `.ufo/waves/round-20/final-clones/{ExecFixtures,ExecFrozen,ExecCounter}/`.

## 3. Per-file comparison, my scan vs GT canonical (16 files)

members/present/missing/misrooted/stub/state **equal GT on 15 of 16 files**, including all counts:
r12w1 32/0/32 unsettled; r13w1 32/0/32 unsettled; r14w1 32/32/0 settled; r15w1 64/49/15 partial;
r15w2 32/32/0 settled; r16w1 84/78/6 partial; r16w2 73/73/0 settled; r17w1 86/86/0 settled;
r17w2 78/52/26 partial; r18w1 70/70/0 settled; r18w2 80/80/0 settled; r19w1 72/72/0 settled;
r19w2 dispatch 72/70/2 partial and its byte-identical twin validation.json (`duplicate_of` dispatch,
`unique_dispatch_sha256` 15 — GT F5); r20w1 64/63/1 partial, missing=[ExecFixtures].
One differing file: **r20w2 64/64/0 settled (GT: 49/15)** — explained in D2.
Member-level join against `build/GtLaneTabi/members.tsv`: 1007/1007 canonical rows compared,
**0 status mismatches**; exactly 15 rows went GT-missing→present, all in r20w2, and the 15 names
are exactly GT F8's in-flight list. All 16 `dispatch_sha256` equal GT `files.tsv` — no dispatch
file changed since T2. `name_hinted_waves` 10 = GT name-suspect canonical 10, all
`undispatched-name:validation`; committed `dispatch_filename_flags` lists 43 tabi paths = GT
name-suspect 43 (10 canonical + 33 clone).

## 4. Every difference explained (live lane change, cited; no tool error)

- **D1 — waves 67→16, members 3932→1007, ignored_json 5093→219 (GT/fleet → mine): the clone
  trees were deleted.** `.ufo/waves/round-20/final-clones` is ENOENT now (stat), while the
  committed evidence (mtime 07:46:53) still records 67 waves / 3932 members and lists the clone
  validation paths in `dispatch_filename_flags`. Deletion window 07:46:53→08:01:39. Arithmetic is
  exact: 5160−235=4925 JSON removed = 51 clone dispatch + 4874 clone non-dispatch; 5093−219=4874.
  Same tool discovered the clones at 07:46 (fleet run), so this is tree state, not a walk failure.
  Who performed the cleanup: not determined [INFERENCE: round-20 scratch clone cleanup].
- **D2 — canonical present 876→891, missing 131→116; r20w2 49→64: the 15 in-flight reports
  landed.** All 15 `.md` files exist now, sizes 11.7–19.4 KB, mtimes 07:37:04 (CounterSourceIdentity)
  … 07:50:35 (ReviewBundles); e.g. WaveMembership 07:38:01, WaveTracked 07:39:03, SemanticLC07
  07:39:12, ReviewReturnBoundary 07:43:24. Fourteen landed before the fleet snapshot (07:46:50 →
  3371 = 3357+14, r20w2 63/64) and ReviewBundles.md landed 07:50:35, before my scan (→ 64/64).
  The three snapshots are one monotone timeline; GT F8's "treat the 15 as in flight" predicted this.
- **D3 — GT no-spawn 3 → my scan 0:** all three `taskCall:null` files were clone copies of
  `rounds/fleet-r1/wave-validation.json` inside final-clones (GT F4); removed with D1. Canonical
  waves have no no-spawn file, matching GT canonical column (0).
- **D4 — GT "unparsed 96 under final-line rule" → my scan unparsed 0:** all 96 are clone
  `wave.dispatch.json` rows with a trailing `| godspeed` envelope (GT F1), removed with D1; the
  tool's disclosed refinement R1 (last matching trailer line,
  tools/mori-wave-settlement.py:231-243) parses them anyway. Canonical scope: 1007/1007 trailers
  parse — no divergence in either reading.
- **D5 — scan1 vs scan2 byte difference:** the only diff is top-level `ignored_json` 219→221
  (two non-dispatch JSON files appeared under `.ufo/waves/` between 08:01:39 and ~08:05;
  `round-20/` dir mtime 08:04:04). Every wave object and every total is byte-identical
  (`diff` of `jq -S` output shows the single ignored_json line). Determinism holds on the
  unchanged portion of the tree; the delta is live churn, not tool nondeterminism.
- **stub = 0** in my scan; GT has no stub column but the same files are >0 bytes, so present/stub
  cannot diverge; spot-checked landed reports are 11–19 KB, not 16-byte stubs.
- **misrooted = 0 is a live, non-vacuous check:** `/home/vgpnk/Projects/shokunin/.ufo/waves`
  exists, and the spot check `stat …/.ufo/waves/round-12/w1/ApgSource.md` → ENOENT (GT F7: no
  trailer path exists under the fleet root; the `.txt` siblings live only in the lane).

## 5. Tool-error hunt (none found)

Mechanisms verified in the sha-pinned source: `.ufo/waves`-only recursive lstat discovery without
symlink follow (`tools/mori-wave-settlement.py:97-131`); trailer = last matching line after rstrip
(:231-243); status incl. stub read ≤16 B and fleet-root misrooted fallback (:245-259); state
machine settled/partial/unsettled/no-spawn/unavailable (:262-308); duplicate_of + unique sha
(:344-348); rc 0 iff all settled/no-spawn (:~370); `--out` write plus stdout emission (:676-685).
Observed behavior on tabi matches each. Exit codes, ordering (sorted by path bytes), vocabulary
(no dead/failed/killed), and counts all conform to the frozen contract. The disclosed residuals
(lstat/open race on live trees; no size cap; path-spelling determinism) are in
knowledge/wave-settlement-r20.md §4 and did not bite here.

## 6. Residual risk / verification gaps

- The lane is live: r20w1 is 63/64 (ExecFixtures still absent, size 0 check impossible — ENOENT),
  and any count can change after 08:01:39; my numbers are bounded by the scan timestamps, and
  scan2 at ~08:05 confirms stability over that window.
- Who deleted final-clones and whether any clone content mattered: unobserved (out of my scope).
- I did not re-run the 14-case oracle (covered by the C2 claim evidence and other seats); the
  selftest and the two live runs above are the checks I exercised.

## 7. Artifacts

- `mori-shokunin/.ufo/waves/round-20/falsify/LiveTabi/scan.json` (scan 08:01:39)
- `mori-shokunin/.ufo/waves/round-20/falsify/LiveTabi/scan2.json` (scan ~08:05)
- Compared against `mori-shokunin/.ufo/waves/round-20/build/GtLaneTabi/{members.tsv,files.tsv}`,
  `build/GtLaneTabi.md`, and `evidence/c2-live-fleet.json` (read-only).
