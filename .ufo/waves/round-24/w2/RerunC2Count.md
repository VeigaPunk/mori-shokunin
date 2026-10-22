# RerunC2Count — wave 2 falsify, C2 counting command and freeze order

Seat: `MoriR24.RerunC2Count` (leaf reviewer, no subagents). Date: 2026-10-22.
Scope: independently re-run the C2 after-value counting command and the freeze-order
measurement, attack both for rubber-stamping, and verify the freeze order from git
bytes. Lane tip measured: `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`.

Environment: fresh clone `git clone --no-hardlinks` of the lane repo into
`/fast/scratch/hyaku/mori-r24-a2/w2/RerunC2Count`, then
`git checkout a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`. HEAD verified
`a730ecfefbdb5c31b1db13aca2c40eecd5e97abc 2026-10-22T05:56:21-03:00 round-24: wave-1
seat reports, S090 wording correction, contract amendment A5`; `git status --porcelain`
empty. All commands below ran inside that clone. Nothing was written outside the
scratch seat directory and this report; the lane repo, its index and its jj state were
never mutated (read-only git only).

Tooling: **nothing installed or upgraded.** Pre-existing `python3` 3.14.8, `git`
2.56.0, `jq`. No pacman transaction was attempted.

## 1. The three declared commands — exact outputs and exit codes

### 1.1 `python3 -I tools/mori-pressure.py --selftest`

```
MORI_PRESSURE_SELFTEST: PASS 12/12
EXIT:0
```

Matches the declared after-value exactly (string and exit code).

### 1.2 `git cat-file -e c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130:tools/mori-pressure.py`

```
fatal: path 'tools/mori-pressure.py' exists on disk, but not in 'c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130'
EXIT:128
```

Matches the declared before-value (exit 128, tool absent at the round-23 tip).
Additional presence checks, same clone:

- `git cat-file -e f6a29702e5b0…:tools/mori-pressure.py` → exit 128 (tool also absent
  at the freeze commit).
- `git cat-file -e 6ee624872de…:tools/mori-pressure.py` → exit 0 (tool present at its
  landing commit).
- `git cat-file -e c725aa37…:tools/fixtures/mori-pressure/cases.json` → exit 128; at
  `f6a29702` → exit 0. No C2 bytes existed before round 24.
- `git grep -c '/proc/pressure' c725aa37 -- tools/` → no hits, exit 1; at `a730ecfe`
  the only hit is `tools/mori-pressure.py` (3 occurrences). The before-value "no mori
  tool reads system CPU, IO or IRQ pressure" holds (default behavior; the A2
  operator-pinning caveat is unchanged).

### 1.3 Freeze-order check

```
python3 -I tools/mori-freeze-order.py check \
  --repo /fast/scratch/hyaku/mori-r24-a2/w2/RerunC2Count \
  --rev 06a7686ed40f53a7455fe526dadf821757bea98a \
  --register .ufo/waves/round-24/evidence/c2-freeze-check-register.json \
  --tip-for r24-C2=6ee624872deafe2aab7001c0ba01bb2ef1f5cdce
```

Output (one JSON line, truncated here for width), `EXIT:0`:

```
{"claims":[{"base_revision":"29c1bf45dde6af48fc9a07aef447bd7d7f822cc5",
"co_committed":false,"effective_label":"pre-build","id":"r24-C2",
"oracle_disagreement":false,"overclaim":false,
"tip_revision":"6ee624872deafe2aab7001c0ba01bb2ef1f5cdce",
"verdict":"pre-build"}],"provenance":{...,"measured_revision":
"06a7686ed40f53a7455fe526dadf821757bea98a","register_sha256":
"44739a26c9ed647893f1242d0144e5c5ed06a0836cbc930a210425218b498c6f",
"script_sha256":"ec1be305d9fbf81d8169554cdb8f681a819f97ee89bb1362f08c4de0b427b547",
"status":"bound",...},"schema":"mori-freeze-order-v1","totals":{"claims":1,
"could_not_evaluate":0,"oracle_disagreements":0,"overclaims":0}}
```

The provenance hashes bind to real bytes: my `sha256sum` over the clone gives
`ec1be305…` for `tools/mori-freeze-order.py` and `44739a26…` for the register — equal
to the recorded values. Field-level comparison (`jq -S 'del(.provenance.command_argv)'`
on both sides) of my output against the lane's retained evidence
`.ufo/waves/round-24/evidence/freeze-order-c2.json` (committed at the tip) diffs clean
(`diff` exit 0); the only byte difference in the raw outputs is the `--repo` path in
`command_argv` (my clone path vs the lane path).

## 2. Cases blob equality and freeze order from git bytes

- Blob OIDs (`git rev-parse REV:tools/fixtures/mori-pressure/cases.json`):
  `39cc96ab4c689ceb54e7cfaf64420056e6a289f7` at `f6a29702`, at `6ee62487`, at
  `06a7686e`, and at `a730ecfe` — **all four identical**.
- `git diff --quiet f6a29702 a730ecfe -- tools/fixtures/mori-pressure/cases.json` →
  exit 0. The cases blob at the freeze commit equals the cases blob at the measured
  tip. The file SHA256 is `aeb80ea080436cb344df8dba7ec19eeecc639e347ae87a14bc6835631f28ca94`,
  equal to the hash recorded in the frozen register note.
- Committer times (`git show -s --format='%H %cI %s'`):
  - `29c1bf45` 05:10:55-03 — declare claims and contract before implementation (the
    register's `base`)
  - `f6a29702` 05:22:43-03 — adds only `tools/fixtures/mori-pressure/cases.json` and
    `.ufo/waves/round-24/frozen/c2-freeze-register.json`
  - `6ee62487` 05:25:21-03 — adds only `tools/mori-pressure.py` and
    `w1/BuildPressureTool.md`
  - `06a7686e` 05:25:54-03 — adds only the measurement register copy
  - `a730ecfe` 05:56:21-03 — wave tip
- `git merge-base --is-ancestor`: f6a29702→6ee62487 exit 0; f6a29702→a730ecfe exit 0;
  6ee62487→a730ecfe exit 0; 06a7686e→a730ecfe exit 0. Everything is on the measured
  tip's first-parent history; `git log --merges` over `29c1bf45..06a7686e` is empty, so
  the freeze-order walk is over linear history (8 commits; only `f6a29702` touches a
  frozen path and only `6ee62487` an impl path).
- Frozen register blob `.ufo/waves/round-24/frozen/c2-freeze-register.json` =
  `319da9c87a567e9069adbb970d0af555bc87b7ab` at both `f6a29702` and `a730ecfe` — the
  frozen copy is unchanged since the freeze.
- The measurement register (evidence copy) differs from the frozen register exactly as
  its own note discloses (`diff` of the two git blobs): `frozen_by` wording, `tip`
  null→`6ee62487…`, the register self-path dropped from `frozen`, replaced note, and a
  dropped trailing newline. `base`, `impl`, `declared`, `declared_at` are identical.
  The tool cannot consume the frozen copy directly (its `tip` is null and the tool
  rejects that as invalid-register), so the measurement copy is the intended input;
  the ordering facts above close the gap independently.
- The `--tip-for` override is not load-bearing: rerunning without it (register's own
  `tip` = `6ee62487…`) gives the same verdict `pre-build`, exit 0.

## 3. Attacks — both checks are able to fail, and the counter counts

- **N1, wrong tip:** `--tip-for r24-C2=c725aa37aa3c9ec4f34e3c2abc8ca1b616c7c130` →
  `"verdict":"absent"`, `"overclaim":true`, `EXIT:1`. The check goes red when the
  implementation is absent.
- **N2, measured revision without the register:** `--rev 6ee624872de…` (one commit
  before the register copy landed) →
  `{"claims":[],"error":"input-revision-mismatch",…}`, `EXIT:2`. The tool reads the
  register from git at the measured revision and requires SHA256(disk bytes) ==
  SHA256(`git show rev:path`) (`tools/mori-freeze-order.py:126-160`); measurement over
  committed bytes is enforced, not decorative.
- **M1, fixture mutation:** changed P06's injected memory `avg10` from `25.00` to
  `2.50` in the working copy of `cases.json`:

  ```
  MORI_PRESSURE_SELFTEST: FAIL 11/12
  P06: exit 0 != 1; verdict PRESSURE_OK != PRESSURE_HIGH; memory.some.avg10 is 2.5, expected 25.0; finding PRESSURE_HIGH on memory missing
  EXIT:1
  ```

  Restored with `git checkout -- tools/fixtures/mori-pressure/cases.json`; tracked
  tree clean again (0 diffs vs HEAD). This proves the selftest derives from the frozen
  fixture bytes on disk (`tools/mori-pressure.py:397-407` resolves the cases file next
  to the script) and that the counter reports real passes (`FAIL 11/12`, not `FAIL`).
- **M2, tool mutation:** `DEFAULT_WARN_AVG10 = 10.0` → `30.0`
  (`tools/mori-pressure.py:88`):

  ```
  MORI_PRESSURE_SELFTEST: FAIL 10/12
  P06: exit 0 != 1; verdict PRESSURE_OK != PRESSURE_HIGH; finding PRESSURE_HIGH on memory missing
  P07: exit 0 != 1; verdict PRESSURE_OK != PRESSURE_HIGH; finding PRESSURE_HIGH on irq missing
  EXIT:1
  ```

  Restored; `sha256sum tools/mori-pressure.py` back to
  `852d1ea7508004dc44690bb6e358625fbd07d89c26d4196793133559d8a773a5` — which also
  equals the builder seat's declared build hash in `w1/BuildPressureTool.md`, so the
  landed bytes are the built bytes (569 lines, matches).
- **Freeze-order tool's own selftest:** `PASS 12/12`, exit 0, run in a nested clone at
  the same commit with `TMPDIR` inside that checkout. First attempt printed
  `SELFTEST freeze-order FAIL 0/11`, exit 1 — my precondition error, not a defect: the
  tool requires `TMPDIR` to resolve inside the script's checkout
  (`tools/mori-freeze-order.py:509-514`). See Low-2 below for the message bug this
  exposed.
- **Counting semantics:** `_selftest` prints `PASS n/total` with `total = len(cases)`
  read from the fixture; the tool does not hard-code 12. The `12/12` in the
  after-value is pinned by the frozen fixture blob (12 cases, blob `39cc96ab…`,
  SHA-pinned in the frozen register note), not by tool logic. That is sound given the
  blob freeze, but any future fixture edit changes the printed denominator — the
  declared string is a fixture property.
- **Fixture fidelity:** the 12 cases are `P01`–`P12` and their topics match the
  contract's frozen topic list one for one (P01 four normal low; P02 nonzero system
  cpu full flagged undefined; P03 irq `full`-only `some` null; P04 irq absent PARTIAL
  exit 0; P05 EOPNOTSUPP all four UNAVAILABLE exit 2; P06 memory some 25 HIGH exit 1;
  P07 irq full 15 HIGH exit 1; P08 io `avg10=abc` malformed; P09 memory missing
  `full`; P10 EACCES io unreadable; P11 interval deltas and ratios incl. null cpu
  `full` delta; P12 decreasing total → `counter_regressed` PARTIAL exit 0). The
  expectation engine (`tools/mori-pressure.py:435-494`) compares exit code, verdict,
  per-resource state, and `some`/`full` subfields and `findings_include` — a real
  oracle, and the selftest returns exit 1 with per-case diagnostics on any failure.

## 4. Live host bracket run (my own, detection only)

`2026-10-22T09:14:47.043Z → 09:14:47.070Z`, raw `cat` of all four
`/proc/pressure/{cpu,memory,io,irq}` before and after a one-shot tool run. Tool:
`"verdict":"PRESSURE_OK"`, exit 0, all four resources `ok`, `irq` `some` null, cpu
`full_system_undefined: true` with `full.total` 0. Bracket check: cpu.some
13152724 ≤ 13152744 ≤ 13152749; io.some 168222514 ≤ 168225514 ≤ 168225925; io.full
162336929 ≤ 162339869 ≤ 162340279; irq.full 28084820 ≤ 28085019 ≤ 28085065;
memory.some/full static (28116067 / 27764257 on both sides); cpu.full 0 throughout.
Every A2 bracket condition holds on this host at this time.

## 5. Findings by severity

**Kill: none.** The C2 counting command and the freeze-order claim both survive
independent re-derivation and mutation attacks.

- **Low-1 (retention timing):** the retained selftest evidence file
  `.ufo/waves/round-24/evidence/c2-selftest-after.txt` is **not committed at the
  measured tip** (`git cat-file -e a730ecfe:…` → exit 128). It first lands in
  `89849a76322a5d79cd45d5f87cf34229ecf41f75` (05:59:07-03), after the wave-2 bind
  commits `753d2273`/`13208d2a`. Not a false claim — the after-value is re-derivable
  at the tip (Section 1.1) and live-run evidence *is* committed at the tip in
  `w1/LivePressureCapture.md` — but the dedicated evidence file postdates the
  measurement tip it supports.
- **Low-2 (cosmetic defect):** `tools/mori-freeze-order.py` early-abort selftest
  messages print the literal `FAIL 0/11` while the suite has 12 cases
  (`tools/mori-freeze-order.py:500,507,513` vs the correct `FAIL %d/12` at :666).
  Observed on a precondition abort. Verdict and exit behavior are correct; only the
  denominator in the three abort messages is stale.
- **Info-1 (post-tip evolution):** `89849a76` ("wave-2 survivors") modifies
  `tools/mori-pressure.py` after the measured tip. The declared after-value is
  correctly scoped to the landed tip (tool blob `4e08739a…` identical at `6ee62487`
  and `a730ecfe`), but the lane's current tool is no longer the measured bytes; the
  after-value must be re-run at whatever head settles round 24.
- **Info-2 (open rider):** `SCORECARD.md` at the tip contains the round-24
  declaration (`SCORECARD.md:1494-1502`, explicitly "targets, not results") but no
  round-24 capability row. The contract's rider "plus … a SCORECARD capability row"
  is unmet at the tip; this is consistent with the settlement convention
  (`SCORECARD.md:588`: rows enter only through a round that demonstrates the
  capability running) and `PROVINCE.md:236` marks FR12 "admission pending". It is an
  obligation to verify at round settlement, not a false statement today.
- **Info-3 (checker semantics):** the freeze-order check verifies path-touch ordering
  over `base..tip`, existence at base and tip, and co-commit detection
  (`tools/mori-freeze-order.py:250-320`); it does not compare frozen-path blob
  identity across revisions. Blob identity is what makes "frozen" meaningful, and I
  verified it independently (Section 2). Settlement reviewers should keep doing one
  of the two.
- **Info-4 (authorship blindness is procedural):** committed bytes can prove order
  only; the frozen register's own note says so. `w1/FreezePressureCases.md` documents
  the protocol (contract + kernel sources only, no file named `mori-pressure.py`
  opened, validator run from `$TMPDIR`), and both wave-1 seats explicitly did **not**
  run the selftest ("PASS 12/12 is not claimed"). PASS 12/12 was first measured at
  integration; my rerun confirms it against the frozen blob.

## 6. Residual risk and verification gaps

- The A2 bracket condition is time-of-day: `io.some avg10` was 5.45 in my window and
  crossed the 10.0 default during the wave-1 capture (`w1/LivePressureCapture.md`
  records `avg10=10.57` at 08:22:34Z). A live `PRESSURE_HIGH` on this host is a
  reachable, honest outcome under fleet load, not a tool defect.
- `EOPNOTSUPP` and `EACCES` are not reachable on this host for `/proc/pressure/*`
  (world-writable, PSI on by default — `w1/LivePressureCapture.md` §3, §6); P05/P10
  remain defensive in-process-hook cases, as A2 labels them. Not falsifiable live
  here.
- Threshold calibration: `--warn-avg10 10.0` is declared local, not calibrated; the
  selftest asserts against the default only. Out of scope for this seat.
- Kernel-source citations S090–S096 and the knowledge entry content are other seats'
  slices; not checked here.
- Sandbox commit `51b64436…` (case seat's wt-cases commit, named in the frozen
  register note) is not an object in the lane repo (expected — never pushed); the
  blob OID `39cc96ab…` is the binding identity and it checks out everywhere.

## Verification summary

Every command above was executed by me in the fresh clone at `a730ecfe`; outputs and
exit codes are quoted as observed. Mutations ran only inside the scratch clone and
were reverted with verified byte-exact restoration (tracked diffs 0; tool SHA256
re-hashed). The lane repo was only read. Scratch remains under
`/fast/scratch/hyaku/mori-r24-a2/w2/RerunC2Count/` (main clone, nested `fo-clone/`
used for the freeze-order selftest, empty `fo-tmp/`).
