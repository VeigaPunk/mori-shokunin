# ReviewC1Metric — round 17 C1

## Verdict

**Conditionally yes.** The two axes are (1) finite synthetic-fixture conformance and (2) one live, bounded seat-file snapshot. The honest claim is: “all **N named fixture cases** moved from `capability_absent` under an intentionally missing-tool control to `match` with the delivered tool, and this timestamped scan reported these seat-file classes.” It is not a measure of all OMP behavior, the share of every real seat covered, or incidents.

The before/after must reuse the exact same gate, fixture tree, expected file, and case IDs. The “before” command below is a missing-capability control using the delivered gate and fixtures; it is **not** a historical execution of the entering revision’s gate (the entering revision has neither gate nor fixtures). Record the fixture/expected-file digests for both runs and compare them.

## Proposed commands (not run)

Run only after the C1 gate, fixtures, and tool have landed. Use fresh output directories. The first tool path is an explicit absent sentinel; retain the `test` guard so the control cannot silently become an actual tool run.

```sh
test ! -e /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/build/c1-no-tool || exit 90
/usr/bin/python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round17-seat-regressions.py \
  --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/build/c1-no-tool \
  --fixtures /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat \
  --output /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/build/c1-before
before_rc=$?
/usr/bin/python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-round17-seat-regressions.py \
  --tool /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-seat-terminal.py \
  --fixtures /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/fixtures/seat \
  --output /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/build/c1-after
after_rc=$?
printf 'before_rc=%s after_rc=%s\n' "$before_rc" "$after_rc"
```

Expected: `before_rc=1`, with `N` `capability_absent` rows; `after_rc=0`, with `N` `match` rows and no `mismatch` or `capability_absent`. Count the delivered manifest rows, not a percentage inferred from the live scan. If the gate emits `run-manifest.json` as `.cases[].status`, the exact count is:

```sh
/usr/bin/python3 -c 'import collections,json,sys; r=json.load(open(sys.argv[1])); c=collections.Counter(x["status"] for x in r["cases"]); print(" ".join(f"{k}={c[k]}" for k in ("capability_absent","match","mismatch")))' \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/build/c1-before/run-manifest.json
/usr/bin/python3 -c 'import collections,json,sys; r=json.load(open(sys.argv[1])); c=collections.Counter(x["status"] for x in r["cases"]); print(" ".join(f"{k}={c[k]}" for k in ("capability_absent","match","mismatch")))' \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/build/c1-after/run-manifest.json
```

**Schema caveat:** contract.md:75-78 specifies per-case statuses but not the run-manifest JSON member path. The two runner commands follow the contract; the counting expressions are exact only if the delivered manifest uses `cases[].status`. Pin that shape in the gate/output documentation or adapt the expressions to the actual manifest before reporting counts.

For one live observation, an authorized operator can run (not run by this reviewer):

```sh
/usr/bin/python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-seat-terminal.py \
  --sessions-dir /home/vgpnk/.omp/agent/sessions
```

Record the scan time, exact sessions directory, exit code/finding, `files_scanned`, and class totals. Treat this as a point-in-time tally only; do not combine it with `N` to form a “coverage percent.”

## Falsifiers / acceptance conditions

- `N` must be nonzero, and every expected case ID must appear exactly once in each manifest. A zero-case suite is vacuous, not coverage.
- Any pre-control status other than `capability_absent`, or a pre-control rc other than 1, falsifies the claimed baseline.
- Any post status other than `match`, any missing/extra case, or an after rc other than 0 falsifies the all-cases-match claim.
- Different fixture IDs, fixture bytes, or `expected.json` between runs invalidate the comparison. Verify the gate’s recorded input hashes and separately retain/compare the expected-file and fixture-set identities.
- The named missing-tool path must remain absent. Otherwise `capability_absent` is not evidence of the intended control.
- A live scan with setup/unavailable-directory rc2 is not a completed tally. The per-seat rows and `files_scanned` should reconcile for a complete scan; an incomplete/truncated population must be reported as such, not silently included as complete coverage.
- To use “C1 coverage” for more than these cases, fixture inventory must actually include the claimed class branches and boundaries. In particular, `want` values in contract.md:73-74 enumerate only `rc`, `finding`, `totals`, and `seats`; require the gate to reject unexpected output fields and test non-emission of sensitive content (e.g. a synthetic sentinel) before claiming the field-limited/privacy contract is covered. A `match` on those listed projections alone does not prove that no extra output leaked.

## Overclaims to avoid

- A `dead_*` total is a **seat count**, not a distinct incident count; multiple seats may reflect one upstream event. The tool does not group events.
- `dead_*` is the last observed error state, not proof the session cannot later resume.
- A prefix is a filename convention, not authenticated lane membership.
- A complete scan with exit 0 means no `dead_*` class was observed; it is not a health claim. `incomplete` and `unavailable` are distinct classes and must remain visible.
- A tally describes files found under this directory and the contract’s limits (regular `*.jsonl`, no symlink traversal, bounded tail, max-files limit). It does not establish the total live-seat population, incident rate, causality, or classifier accuracy on untested real transcripts.

## Findings by severity

**Low — exact status counting is not reproducible from the written gate contract alone.** The manifest’s per-case statuses are required, but their JSON path is unspecified (contract.md:75-78). Document the stable member path or have the gate emit an explicit deterministic aggregate alongside its case rows.

**Verification gap — privacy/output shape is not explicitly part of the fixture `want` contract.** The expected projection names `rc`, `finding`, `totals`, and `seats` (contract.md:73-74), while the tool contract forbids emitting message text/content/usage and limits output fields (contract.md:52-60). Until the delivered gate’s comparator is inspected, a `match` must not be cited as proof that unexpected fields or sensitive output are rejected.

No C1 implementation defect was observed because the implementation was absent from the lane snapshot; this is not a pass on the tool or gate.

## Evidence and verification gaps

- C1’s axis is capability acquisition/coverage (contract.md:9-15); fixture and gate semantics are contract.md:69-78; the live output/limit claims are contract.md:31-67.
- Read-only lane status/diff command completed with exit 0: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin status --short && git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --stat && git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --name-only`. It showed `.gitignore` modified and `.ufo/waves/round-17/` untracked; the tracked diff summary was only `.gitignore` (one added ignore line). No C1 tool code was in the tracked diff.
- Baseline presence check against `24526ea9617cd020fee16c28fe4d4a2789dc28cb` returned `git cat-file -e` rc128 (absent) for each of `tools/mori-seat-terminal.py`, `tools/mori-round17-seat-regressions.py`, and `.ufo/waves/round-17/fixtures/seat/expected.json`. The current tools listing likewise did not contain either C1 tool; reading the fixture directory returned not found.
- No C1 gate, tool, selftest, or live tally was run; no OMP transcript was read and no URL was opened. No tools were installed or updated.
- The mounted `xd://` inventory has no LSP device. No LSP status/references/definition/diagnostics were available; no grep was used as semantic proof.
