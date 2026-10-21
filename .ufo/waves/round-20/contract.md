# mori round 20 — frozen claim contract (written before any implementation)

Author: MoriR20 (L1). Entering lane tip `2061780117e6ca637725004897bd288d3ba7e988`.
Active scores entering: coverage 6, operability 7, depth 5, freshness 5, calibration 5,
adjacency 6. Lowest non-retired tie: depth / freshness / calibration at 5. Calibration
was selected in rounds 17, 18 and 19; freshness has not been claimed since round 10 and
its re-pin has been the carried `Planned` debt since round 12. No retirement, no
stagnation waiver.

## C1 — freshness (lowest-score tie): classified re-verification and re-pin of the drift baseline

Problem. `corpus/evidence/baseline-r10-20261015T2231Z.json` is the only behavioral
baseline; it is six days and nine census revisions old. Every round since 12 re-ran it,
saw exit 1, and declined to re-pin. The newest machine-readable classification
(`.ufo/waves/round-13/evidence/drift-classification.json`) no longer covers the live
drift: at the entering tip 8 of 50 drift tokens have no classification
(`evidence/c1-drift-entering.json`).

Before (entering tip, census SHA-256 `87b8d680…ab28`): `--drift baseline-r10` rc 1,
50 tokens, 8 unclassified against the latest committed register.

After:
1. A new register `corpus/evidence/drift-classification-r20.json`
   (`schema: mori-drift-classification-v1`) assigns every token of the measured drift
   output one class from the closed set
   `census-schema-change | roster-change | live-state | census-regression`, each with an
   evidence pointer (commit, path:line or receipt) and a one-line reason. A token classed
   `census-regression` blocks the re-pin and is reported, not hidden.
2. Only if zero tokens are `census-regression`: a new baseline
   `corpus/evidence/baseline-r20-<UTC>.json` is pinned with `--pin` by the L1 at the
   measured commit, with a recorded reason; the r10 file is kept byte-unchanged.
3. `--drift <new baseline>` is re-run by the L1 after pinning; its rc and tokens are
   recorded whatever they are (a non-`none` result is reported as the measured
   stability window, never suppressed).

Counting command (lane root; DRIFT = a captured drift stdout file, REG = register):

```sh
LC_ALL=C comm -23 <(tr ' ' '\n' < DRIFT | grep -v '^MORI_DRIFT:$' | grep . | sort -u) \
  <(jq -r '.tokens|keys[]' REG | LC_ALL=C sort -u) | wc -l
```

Expected: 8 with the round-13 register, 0 with the round-20 register, on the same
captured drift output at the measured commit. Falsified by any unclassified token, any
classification lacking an evidence pointer, or a re-pin made while any token is
`census-regression`. The census script is NOT edited this round (C1 is re-verification,
not a census change); its SHA must equal `87b8d680…ab28` at the measured commit.

## C2 — coverage: per-seat wave settlement (FR3 advance, capability acquisition)

Problem. `SURFACE waves` reports registry/dispatch presence and age only. Nothing in
the lane counts which dispatched seats left their report. Round 19 wave 1 returned 64
IDs and retained 16 reports; the 48 missing reports were found only by hand at recovery
and closure (MANIFEST round-19 closure notes). That is the round's mined mistake.

New read-only tool `tools/mori-wave-settlement.py` (stdlib Python 3, no network, no
writes outside an explicit `--out`):

```
mori-wave-settlement.py scan --lane-root DIR [--fleet-root DIR] [--out FILE]
mori-wave-settlement.py --selftest
```

- Discovery: every regular `*.json` file under `<lane-root>/.ufo/waves/` whose top-level
  `schema` equals `ufo-swarm-wave-dispatch-v1`. Other JSON is counted as
  `ignored_json`; unparseable JSON is counted `unreadable_json`. Symlinks are not
  followed.
- Members: `taskCall.tasks[*]` (`name`, `agent`). `taskCall: null` → wave state
  `no-spawn`.
- Expected report path: the LAST line of a task matching
  `^Report: write your scoped findings to (\S+)$`. The path must be relative, contain no
  `..` component and resolve inside the lane root; otherwise the member is `unsafe`
  (never read). A task without the trailer is `unparsed`.
- Member status: `present` (regular non-symlink file, size > 0), `empty` (size 0),
  `missing`, `unsafe`, `unparsed`. If missing under the lane root but the same relative
  path is a regular file under `--fleet-root`, the member is `misrooted` (counted as not
  present). Report bytes are never emitted; only status and counts.
- Wave state: `settled` (every member present), `partial` (≥1 present, ≥1 not),
  `unsettled` (0 present, ≥1 member), `no-spawn`, `unavailable` (no member had a
  parseable safe path). A missing report is NOT a dead seat: the output never says
  `dead`, `failed` or `killed`.
- Output JSON (`schema: mori-wave-settlement-v1`): `lane_root`, `waves` (sorted by
  dispatch path bytes) each with `dispatch_path`, `dispatch_sha256`, `wave`, `members`,
  counts per status, `state`, `missing` (sorted member names, never paths outside the
  lane); `totals`; `ignored_json`; `unreadable_json`. Byte-identical across two runs on
  the same tree.
- Exit: 0 every discovered wave `settled` or `no-spawn`; 1 any other state;
  2 usage error or unreadable lane root.

Finite requirements: `frozen/c2-expected.json` (14 cases). Before: the tool is absent at
the entering tip (`git cat-file -e 2061780:tools/mori-wave-settlement.py` rc 128), so all
14 are capability-absent — capability red, not 14 historical production defects.
After: 14/14 matched by an oracle harness written independently of the tool.

Live demonstration (not part of the finite count): `scan` on the mori lane must
reproduce round-19 wave-1 `reports_present = 16` of 64 members recorded by the
non-author closure, and the fleet-wide run over every lane's dispatch files is recorded
with its totals. Counting command:

```sh
jq -s '[.[].counts.capability_absent]' .ufo/waves/round-20/evidence/c2-before.json .ufo/waves/round-20/evidence/c2-after.json
```

Expected `[14,0]`, plus `jq '.counts.matched'` on the after file = 14.

## Separation

C1 touches only drift evidence and a new baseline; it does not need the C2 tool. C2
needs no new baseline and no census change. Each is verifiable with the other reverted.

## Write and safety bounds (all seats)

Read-only on the fleet repo, every sibling lane, `.ufo/state/*`, the watchdog log and
host services. No seat edits `tools/mori-census.sh`, any committed baseline, MANIFEST or
lane jj/git state. Candidate code goes only under a seat's own
`.ufo/waves/round-20/build/<SeatName>/` directory; the L1 is the single integration
owner. No retained interactive-session transcripts are opened (round-19 M7).
