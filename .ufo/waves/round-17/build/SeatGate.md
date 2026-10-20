# SeatGate — round 17 wave 1 (C1 gate build)

- Seat: `MoriR17.SeatGate-5` (executor, leaf).
- Clone: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatGate`
  (separate clone at entering tip `24526ea9617cd020fee16c28fe4d4a2789dc28cb`).
- Deliverable: `tools/mori-round17-seat-regressions.py` (the only file written in the clone).
- sha256: `c29fa210ed2dd74956ebeb1baa3629b82f34c4bdd63a05f1b85300d64a608017`
- Lines: 1749. Python 3 stdlib only.
- No tool installs or upgrades; no VCS mutation; lane checkout, `MANIFEST.json`, `.ufo/state` untouched.

## Axes named

1. **Contract fidelity** — every graded field the C1 contract names is checked and
   cross-derived, not merely echoed from the fixture want.
2. **Falsifier independence** — mismatch, forbidden-key and files-scanned arms prove the gate
   can go red on a wrong-but-well-formed tool.
3. **Isolation/safety** — real subprocess, minimal environment, `HOME` pinned to the case dir,
   output guard, TMPDIR-only scratch, no `/tmp`, no live sessions.
4. **Integration compatibility** — tolerant projections for the two documented ambiguities
   (`retry_exhausted` type, seat list vs map, rc2 diagnostics) while staying strict on
   contract-defined shape.
5. **Operability** — `run-manifest.json` carries per-case status, reasons, hashes, argv, and
   before/after input digests; retained stdout/stderr bytes.

## Interface implemented

```
tools/mori-round17-seat-regressions.py --tool PATH --fixtures DIR --output DIR
tools/mori-round17-seat-regressions.py --selftest
```

- `--tool` defaults to `tools/mori-seat-terminal.py`; `--fixtures` defaults to
  `.ufo/waves/round-17/fixtures/seat`; `--output` must be absent or empty.
- Expected table is always `<fixtures>/expected.json`; packs are `<fixtures>/<pack>/`.
- Case args: `{pack}` and `{fixtures}` expand to absolute paths; if the args carry no
  `--sessions-dir`/`--sessions-dir=...`, the gate prepends `--sessions-dir <fixtures>/<pack>`.
  Duplicate `--sessions-dir` or an empty value is a setup error (rc2).
- Per case the tool runs once as a real subprocess: `sys.executable <tool> <args>`, cwd
  `output/cases/<case-id>`, environment exactly `PATH=/usr/bin:/bin`, `LC_ALL=C`, `TZ=UTC`,
  `PYTHONIOENCODING=utf-8`, `PYTHONDONTWRITEBYTECODE=1`, `HOME=<case dir>`, stdin
  `/dev/null`, per-stream cap 4 MiB, deadline 30 s. Timeout/cap become case mismatches,
  never setup.
- stdout/stderr bytes are written to `output/runs/<case-id>.stdout|.stderr`; the manifest
  records their sha256 and byte counts.

## Manifest (`output/run-manifest.json`)

Schema `mori-round17-seat-regressions-manifest-v1`; keys: `gate`, `gate_sha256`, `tool`
(path/present/sha256), `fixtures` (dir, expected path+sha256, `inputs_before`,
`inputs_after`, `inputs_changed`), `git` (head/branch, read-only), `cases[]`, `summary`,
`verdict`, `exit_code`. Each case row records `id`, `pack`, expanded `argv`,
`sessions_dir`, `status` (`match|mismatch|capability_absent`), `ok`, `reasons` (stable
slugs, no transcript text), safe `observed` fields, per-case pack digests before/after,
`pack_changed`, and stdout/stderr hashes/sizes.

Input pinning: every fixture entry is hashed before and after the run
(`snapshot_tree`, `tools/mori-round17-seat-regressions.py:256`). Symlinks hash their link
text and are never followed; directories get presence markers; unreadable regular files
hash a stat fingerprint (mode/size/mtime/ctime). Any before/after difference, including a
restored per-case pack, yields `verdict=tamper:inputs-changed` and rc2.

## Grading performed per case (`evaluate`, :835)

Independent of the want table:

- stdout must be exactly one strict JSON object (duplicate keys and NaN/Infinity rejected).
- `schema == mori-seat-terminal-v1`, `finding` must match rc (0 OK, 1 DEAD, 2 SETUP).
- rc0/rc1: exactly the nine contract top-level keys; no unknown keys; no forbidden
  transcript fields anywhere (`errorMessage`, `content`, `usage`, `message`, `raw`, ...);
  `sessions_dir` must resolve to the case sessions dir.
- `totals` must carry all seven classes as non-bool ints >= 0 and equal the tally
  re-derived from `seats`; rc0 requires zero `dead_*`, rc1 requires at least one.
- `seats` accepts the contract's sorted list of per-seat objects **or** an equivalent
  `seat -> object` map (projected to `seat -> class`). Each seat must carry exactly the
  eight contract fields, `prefix == id.split(".", 1)[0]`, ids sorted, `provider`/`model`
  string-or-null, `error_status` int-or-null, `retry_exhausted` bool, `retries` int-or-null,
  `error_code` int or digit string. The projected map must equal `want.seats` exactly.
- `by_prefix` must equal the prefix tally re-derived from the seats; `by_provider_model`
  class sums must equal `totals` (key format not pinned); top-level `retry_exhausted` must
  be the flagged-seat count (int) or the boolean aggregate and agree with the seats.
- `files_scanned`: exact walked-`*.jsonl` count and seat count when no `--prefix` is passed
  and every fixture file is readable; for a prefix-filtered or unreadable-bearing pack it
  must stay within `[len(seats), walked-file count]` (the contract does not pin whether a
  filtered-out or unreadable file counts as scanned).
- Fixture `errorMessage`/`content` strings (bounded 2 MiB/file scan, message records only)
  must not appear on stdout or stderr; strings contained in output keys, class tokens,
  seat ids/prefixes or provider/model values are exempt so legitimately emitted metadata
  cannot be a false leak.

Want comparison: rc/finding exact; for rc0/rc1 the want must carry a `totals` subset and a
`seats` map (the loader also checks that the seats tally agrees with every declared totals
class); every declared totals class and every seat id/class is compared exactly, and an
unexpected seat id is a mismatch. For rc2 only `rc`/`finding` are required; absent
totals/seats are unasserted; declared ones are graded leniently, and implementation-defined
setup diagnostics (e.g. `reason`, `files_seen`, `max_files`) are tolerated while forbidden
transcript fields are still rejected.

Exit codes: 0 every case matched; 1 any mismatch, or the tool path is absent (all cases
`capability_absent`, never green); 2 setup/tamper (bad args, unreadable/symlinked fixture
root or expected table, invalid case table, unsafe/non-empty output, inputs changed).

Output guard (`guard_output`, :496): refuses a symlink output, a non-empty output, output
that equals/contains or sits under the fixture tree, the expected table, the tool file, the
repository root, `tools/`, `.git/`, `.jj/` or `corpus/`. Guarding happens before any
directory creation.

## Selftest

Command actually run (own clone, own `.scratch` only):

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatGate
TMPDIR=$PWD/.scratch python3 tools/mori-round17-seat-regressions.py --selftest
```

Result: **rc=0**, `SELFTEST ok` with 11 arms (each a real subprocess run of the gate
against a tiny fake tool and generated fixtures under `$TMPDIR`):

| arm | proves |
|---|---|
| `green_rc0_and_manifest` | 3/3 match, rc0, verdict ok, manifest schema/gate/tool/expected digests, retained stdout hash + stderr file, observed totals, stable inputs |
| `capability_absent_rc1` | missing `--tool` records every case `capability_absent`, verdict `capability_absent`, rc1 |
| `mismatch_rc1` | a factually wrong but coherent want goes red with `want.*` reasons, rc1 |
| `forbidden_key_rc1` | a leaked `errorMessage` seat key goes red (`forbidden_key:`/`unknown_key`), rc1 |
| `seats_map_projection_rc0` | `seat -> object` map projects cleanly and matches want |
| `prefix_filter_rc0` | `--prefix` allows walked files > retained seats |
| `files_scanned_falsifier_rc1` | two walked files but one emitted seat without `--prefix` goes red |
| `unreadable_fixture_rc0` | chmod-000 fixture file hashed via stat fingerprint; run stays green |
| `fixture_drift_rc2` | fake tool mutates its pack mid-run; rc2 `tamper:inputs-changed`, per-case pack flag set |
| `output_guard_rc2` | outputs under lane `tools/`, `.git/`, `.jj/`, `corpus/`, the fixture tree and a pack are refused before creation |
| `nonempty_output_rc2` | non-empty output refused |

TMPDIR discipline: `--selftest` refuses unset TMPDIR and TMPDIR resolving to `/tmp` or
`/var/tmp` (`SELFTEST SETUP`, rc2). The selftest temporary tree is removed; `.scratch`
contained 0 entries after the final run.

## Read-only cross-checks against sibling wave artifacts

Not executed; inspected as data only, per seat rules.

- `../SeatFixtures/.ufo/waves/round-17/fixtures/seat/expected.json`: 42 cases, keys
  `{id,pack,args,want}`, want keys exactly `{rc,finding,totals,seats}`. An independent
  read-only validator replicating the gate loader's invariants reported **0 defects**:
  ids/packs/args valid, rc/finding coherent, totals all seven classes, seats tally equals
  totals, rc0 has no dead seats, rc1 has dead seats, every rc0/rc1 pack exists. Distribution
  21 rc0 / 19 rc1 / 2 rc2; only `MissingDir` is absent (rc2); both rc2 wants carry only
  `rc` + `finding`. Packs contain no duplicate seat basenames (the tool keys seats by
  basename), including `NestedDirs`.
- `../SeatTool/tools/mori-seat-terminal.py` (read-only): emits exactly the nine graded
  top-level keys (`:322-330`), `seats` as a sorted list, top-level `retry_exhausted` as an
  int seat count (`:327`), `error_code` as a digit string (`_seat_record`), setup payloads
  with `reason` plus diagnostics such as `files_seen`/`max_files` (`_setup`, `:124`), and
  counts `files_scanned` only after `--prefix` filtering (`:293-305`). The gate's
  tolerances cover each of these. [INFERENCE] End-to-end green on the integrated lane is
  expected from this static alignment; the actual integration run belongs to L1.
- Canary simulation over the 33-pack / 42-case tree (read-only replication of
  `collect_canaries`) leaves only synthetic content/errorMessage phrases (e.g.
  `synthetic answer`, `429 rate_limit`, `RATE_LIMITED`); none can appear in the tool's
  nine-key output, so no false leak is expected.

## Retained evidence

- Final selftest line:
  `SELFTEST ok: green_rc0_and_manifest,capability_absent_rc1,mismatch_rc1,forbidden_key_rc1,seats_map_projection_rc0,prefix_filter_rc0,files_scanned_falsifier_rc1,unreadable_fixture_rc0,fixture_drift_rc2,output_guard_rc2,nonempty_output_rc2`
  (rc0, run 2026-10-20).
- `sha256sum tools/mori-round17-seat-regressions.py` =
  `c29fa210ed2dd74956ebeb1baa3629b82f34c4bdd63a05f1b85300d64a608017`.
- `wc -l` = 1749; `python3 -c "ast.parse(...)"` = `AST OK`.
- No installs/upgrades performed, so no tool/version/channel row is owed.

## Risks and limits

- The gate was **not** run end-to-end against the real fixture tree + SeatTool (seat rule:
  own selftest only); integration is L1's run. Static loader/widget compatibility is
  verified above.
- rc0/rc1 rejects unknown top-level keys; a tool adding an undocumented field will go red
  by design. rc2 tolerates diagnostics because the contract does not enumerate them.
- `by_prefix` values must be full seven-class totals (SeatTool does this); unknown
  `by_provider_model` key conventions are accepted, but their class sum must equal
  `totals`.
- `files_scanned` is exact only where the contract is unambiguous (unfiltered, all files
  readable); filtered/unreadable packs use the documented inclusive bounds.
- Leak canaries scan at most 2 MiB per fixture file and skip non-message record types;
  strings shorter than 8 bytes are not canaries.
- The tool digest is recorded in the manifest but not pinned (the contract defines input
  pinning only); a tool change between runs is visible, not refused.
- Fixture drift detection covers content, symlink targets, directory presence, and stat
  fingerprints for unreadable files; a pure mode/ownership change on a readable file is not
  detected.

## Amendment A1 + persisted pins (2026-10-20, L1 directives) — supersedes the grading details above

Implemented in the same file, still the only clone file written:

- **`finding_id`** replaces `finding` in expected wants and output grading: values
  `MORI_SEAT_TERMINAL_OK`/`_DEAD`/`_SETUP`, rc agreement 0/1/2. Legacy `finding` is no
  longer a want key.
- **Case args pass through unchanged**, including `--now-ms` and `--settle-seconds`; the
  only additions remain `{pack}`/`{fixtures}` substitution and the prepended
  `--sessions-dir`.
- **New top-level keys accepted and validated when present**: `now_ms`,
  `settle_seconds`, `main_sessions`, `duplicate_stems` (int or string list). `now_ms` /
  `settle_seconds` must echo a pinned `--now-ms` / `--settle-seconds` argument when one is
  supplied.
- **Eight totals classes**, adding `error_unsettled`; rc0 still requires zero `dead_*`,
  rc1 at least one. Forbidden-key check (`errorMessage`, `content`, `usage`, `message`,
  …) retained over the whole stdout document and stderr canary scan.
- **A1 per-seat fields**: `key`, `kind`, `terminal_ms`, `reason` accepted and validated
  (the original nine fields remain required). Entries with `kind == "main"` are counted in
  `main_sessions` and excluded from totals, `by_prefix`, `by_provider_model`,
  `retry_exhausted` and want.seats grading, while still counting in `files_scanned` and the
  seat list. want.seats keys may be seat stems or key paths (key lookup first, then stem);
  seat ordering may be by stem or by key.
- **Persisted pins (Two evidences)**: expected.json must carry top-level
  `pins = {fixture-relative path: 64 lowercase hex sha256}` covering every non-directory
  entry except expected.json. Regular file = sha256(content); symlink (including a link to
  a directory) = sha256(link target text UTF-8, no newline); FIFO = sha256(b"fifo");
  directories omitted; a chmod-000 file must be empty and is pinned as sha256(b"") (a
  non-empty unreadable fixture is setup). Pins are verified against the actual tree
  **before any tool run**. Missing, extra or mismatched pins yield manifest
  `verdict=snapshot_tampered`, `fixtures.pins.verified=false` with the differing paths,
  rc2, and no case runs. Runtime before/after hashes remain a second, non-independent
  signal (`tamper:inputs-changed`). `snapshot_tree` now lstat-tolerates FIFOs and ignores
  other special entries (sockets/devices) instead of failing the gate.
- Exact pin shape was sent to `MoriR17.SeatFixtures-5` (FIFO convention confirmed).

Selftest (own clone, own `.scratch` only):

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatGate
TMPDIR=$PWD/.scratch python3 tools/mori-round17-seat-regressions.py --selftest
```

Result: **rc=0**, 13 arms:

`green_rc0_and_manifest, capability_absent_rc1, mismatch_rc1, forbidden_key_rc1,
seats_map_projection_rc0, a1_main_sessions_rc0, pinned_snapshot_tamper_rc2,
prefix_filter_rc0, files_scanned_falsifier_rc1, unreadable_fixture_rc0,
fixture_drift_rc2, output_guard_rc2, nonempty_output_rc2`

New arms: `a1_main_sessions_rc0` (main-kind seat excluded from totals/breakdowns but
counted in `main_sessions`/`files_scanned`, `now_ms` echoed), and
`pinned_snapshot_tamper_rc2` (tree mutated after pinning => rc2 `snapshot_tampered`, pins
unverified with the exact mismatched path, zero case runs). Green also asserts persisted
pins verified and the symlink pin (a symlink is present in the green pack).

Retained evidence:

- `sha256sum tools/mori-round17-seat-regressions.py` =
  `b28bf42971afc985cb8e4bf62181a2640713e7a53b2340616b1429dc5f5406e6`
- `wc -l` = 2131; `python3 -c "ast.parse(...)"` = `AST OK`; `.scratch` = 0 entries after
  the run.
- Read-only static note: the sibling expected.json (42 cases) is still pre-A1 (no `pins`,
  `finding`, seven classes) and the sibling SeatTool is still pre-A1 (no `finding_id`,
  `now_ms`). The gate now enforces A1, so both will be rejected/red until their A1
  updates land; this is the intended amendment cutover, not a gate regression.
- No installs/upgrades.

Risks specific to the amendment:

- All pre-A1 fixture packs are now setup-red by design (missing `pins`, `finding` want
  key); the fixture seat must re-pin the tree after its A1 update.
- `duplicate_stems` is type-checked (non-bool int >= 0 or string list) but not
  recomputed, because the amendment does not say whether it counts extra copies or
  distinct duplicated stems.
- Gate reading: main-kind entries are excluded from every aggregate (totals,
  by_prefix, by_provider_model, retry count) and from want.seats, not only from totals.
- Superseded by the sandbox section below: source fixtures must stay readable; chmod 000
  is recreated only in the per-case copy.

## Per-case sandbox for unreadable files (L1 reproducibility directive)

Implemented after the A1/pins cutover; supersedes the earlier direct-pack execution.

- Source fixtures stay fully readable. Pins are computed on **source bytes only**; no
  mode-000 state is required in the clone, and Git/jj mode loss is irrelevant.
- expected.json cases may carry `"unreadable_files": ["<pack-relative path>", ...]`
  (added to CASE_KEYS). Each path must be a regular non-symlink file inside the pack and
  readable at load time; otherwise the gate exits 2 as a fixture setup defect. Duplicate
  or escaping paths are rejected.
- For every case whose pack exists, the gate copies the pack into
  `output/cases/<case-id>/sessions` and runs the tool against that sandbox:
  regular files by content copy, symlinks recreated with their original target text,
  FIFOs via `os.mkfifo` (never `copyfile`, which would block), other special entries
  skipped. Chmod 000 is applied only to the listed paths **inside the sandbox**, after the
  copy; the sandbox is discarded with the output tree.
- Only the `--sessions-dir` value is rewritten to the sandbox; every other case arg
  (`--now-ms`, `--settle-seconds`, `--prefix`, …) still passes unchanged.
- A case whose pack is absent (the rc2 unavailable-directory fixture, e.g. `MissingDir`)
  gets no sandbox: the nonexistent source path is passed through so the tool still reports
  setup.
- Pins are verified on the source tree before any sandbox is created. Runtime before/after
  hashes also cover source only; a tool writing inside its sandbox is legitimate and is
  not treated as fixture drift. Each manifest case now records `sandbox` and
  `unreadable_files`; the absent-tool baseline records `sandbox: null`.
- Exact key/path base and FIFO copy rule were agreed with `MoriR17.SeatFixtures-5`
  (case-level `unreadable_files`, pack-relative, source 0644).

Selftest changes and result (own clone, own `.scratch`):

- `unreadable_fixture_rc0` now proves the whole path: source file stays 0644 and empty,
  sandbox copy has mode 000, the fake tool classifies by sandbox mode bits (000 =>
  `unavailable`), and the manifest records the sandbox + `unreadable_files`.
- The green pack now also contains a symlink and a FIFO, so persisted pin hashing,
  symlink recreation and `os.mkfifo` copying are exercised without blocking.
- `fixture_drift_rc2` now writes to the **source** pack through a selftest-only
  `--source {pack}` argument, so runtime input-drift detection remains exercised while the
  real tool can only see its sandbox.

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatGate
TMPDIR=$PWD/.scratch python3 tools/mori-round17-seat-regressions.py --selftest
```

rc=0, 13 arms:
`green_rc0_and_manifest, capability_absent_rc1, mismatch_rc1, forbidden_key_rc1,
seats_map_projection_rc0, a1_main_sessions_rc0, pinned_snapshot_tamper_rc2,
prefix_filter_rc0, files_scanned_falsifier_rc1, unreadable_fixture_rc0,
fixture_drift_rc2, output_guard_rc2, nonempty_output_rc2`

Retained evidence:

- `sha256sum tools/mori-round17-seat-regressions.py` =
  `43e129c7d3070b42c3d8bf0bef5e961021a0dfde2d15f8f39bec8bb3caddb660`
- `wc -l` = 2327; `python3 -c "ast.parse(...)"` = `AST OK`; `.scratch` = 0 entries.
- No installs/upgrades; no VCS mutation; only the gate file in the clone and this report
  were written.

Sandbox-specific risks:

- A non-readable source fixture (even empty) now fails setup at copy time; the source tree
  must remain 0644. The real `locked.jsonl` is being converted to 0644 by the fixture seat.
- Sandbox setup metadata is limited to `unreadable_files` (chmod 000); other transient
  metadata would need an explicit extension.
- Each case copies its pack under `output/`, so disk use scales with cases; fixture packs
  are small (largest observed ~482 KB).

## Branch-anchored revision receipts + guard docs (L1 final migration fix)

`capture_revision()` rewritten so the manifest receipt is branch-anchored, never bare
HEAD:

- Branch resolution order: attached `symbolic-ref -q HEAD` -> `refs/remotes/origin/HEAD`
  -> unique existing `refs/heads/master` / `refs/heads/main`. Each candidate is confirmed
  with `rev-parse --verify --quiet refs/heads/<branch>`; `branch_source` records
  `attached`, `origin-head`, `unique-master-main` or `unresolved`.
- Receipt fields: `branch`, `receipt_ref = refs/heads/<branch>`, and
  `branch_tip = rev-parse refs/heads/<branch>`. `head = rev-parse HEAD` is recorded as a
  diagnostic only; receipts are measured against `branch_tip`, never `head`.
- Every git call runs with `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE` scrubbed from
  the environment and with `--no-optional-locks -c core.fsmonitor=false`, so metadata
  collection cannot be redirected by an ambient repository and cannot take index locks.
- Observed in the clone (read-only, `PYTHONDONTWRITEBYTECODE=1`):
  `{"branch":"master","branch_source":"attached","branch_tip":"24526ea9617cd020fee16c28fe4d4a2789dc28cb","head":"24526ea9617cd020fee16c28fe4d4a2789dc28cb","receipt_ref":"refs/heads/master"}`
  — branch tip equals the entering tip, and `head` is diagnostic only.

Output-guard documentation corrected: `--output` **may** sit under the repository's
`.ufo/` tree; it must not equal or contain the repository root and must not sit under the
fixture tree, the tool file, `tools/`, `.git/`, `.jj/` or `corpus/`. Code behavior was
already this; only docstring/help wording changed.

Selftest rerun (metadata change only, but the green arm now asserts the receipt shape):

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatGate
TMPDIR=$PWD/.scratch python3 tools/mori-round17-seat-regressions.py --selftest
```

rc=0, same 13 arms. Retained:

- `sha256sum tools/mori-round17-seat-regressions.py` =
  `1060d55b30abc7001676f1d6259455c498268b867f524da87e75f09b58523a89`
- `wc -l` = 2397; `ast.parse` = `AST OK`; no `__pycache__` created by the read-only
  metadata probe; `.scratch` = 0 entries.

## Generated-FIFO fixtures (`fifo_files`) — no untrackable source entries

L1 commit-blocking migration: a real FIFO cannot be tracked by Git/jj, so the
`FifoSkip` fixture is represented by case metadata instead of a source entry.

- New case key `fifo_files: ["pipe.jsonl", ...]` (pack-relative). Validation: safe
  relative paths only (no leading `/`, no `..`, no backslash/control characters), no
  duplicates, no overlap with `unreadable_files`, pack must exist, and every listed path
  **must be absent** (not a file and not a symlink) from the source pack. A source FIFO or
  a stale entry is a setup error (rc2).
- The gate creates each FIFO with `os.mkfifo` only inside the per-case sandbox, after the
  pack copy and any chmod-000 setup. Missing parent directories are created inside the
  sandbox only, with a containment check; nothing is ever written to the source tree.
- Because the source path is absent, persisted `pins` exclude generated FIFOs and source
  pin verification stays stable across runs. `files_scanned` and the walked-file count
  consider only regular source `*.jsonl` files, so a correct ignored-FIFO result
  (`files_scanned: 0`, zero seats, zero totals, rc0) is not rejected.
- Manifest case rows now record `fifo_files` alongside `sandbox`/`unreadable_files`; the
  absent-tool baseline records the list too. No production repo writes: the clone contains
  0 FIFOs after the run (`find . -type p`).

Selftest changes and result:

- The green pack no longer contains an actual FIFO (untrackable); its first case now uses
  `fifo_files: ["Pipe.jsonl"]`. The green arm asserts the sandbox contains a real FIFO at
  that path, the source path stays absent, and the normal one-seat result still passes
  (`files_scanned` 1).
- New arm `generated_fifo_rc0`: pack with only generated `pipe.jsonl`; the fake tool sees
  the sandbox FIFO, ignores it, and returns zero seats/files/totals. The arm asserts rc0,
  verdict ok, FIFO type in the sandbox, `files_scanned == 0`, zero totals, and absent
  source path.

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/SeatGate
TMPDIR=$PWD/.scratch python3 tools/mori-round17-seat-regressions.py --selftest
```

rc=0, 14 arms:
`green_rc0_and_manifest, capability_absent_rc1, mismatch_rc1, forbidden_key_rc1,
seats_map_projection_rc0, a1_main_sessions_rc0, generated_fifo_rc0,
pinned_snapshot_tamper_rc2, prefix_filter_rc0, files_scanned_falsifier_rc1,
unreadable_fixture_rc0, fixture_drift_rc2, output_guard_rc2, nonempty_output_rc2`

Retained evidence:

- `sha256sum tools/mori-round17-seat-regressions.py` =
  `21285c2b7000bf63cd9fd679f4b88a7d5d4ff250eee0279576d6d0dcb3b97f7a`
- `wc -l` = 2529; `ast.parse` = `AST OK`; `.scratch` = 0 entries; clone FIFO count = 0.
- Key/path base and semantics confirmed with `MoriR17.SeatFixtures-5`: case-level
  `fifo_files`, pack-relative, source path absent, pins exclude, sandbox-only creation.
- Read-only validation of the delivered fixture table after the migration
  (`SeatFixtures/.ufo/waves/round-17/fixtures/seat/expected.json`, sha256
  `b684c63bf3cebe70f24d3d02f3f0df4f63aad3f547a365a3ca1864f5f57cb01f`): 54 cases,
  81 pins with 0 missing / 0 extra / 0 mismatched (no `FifoSkip/pipe.jsonl` pin),
  `fifo_skipped.fifo_files == ["pipe.jsonl"]` with the source path absent,
  `unavailable_unreadable_file.unreadable_files == ["locked.jsonl"]` at mode 0644,
  every case pins `--now-ms`, wants use `finding_id` and the eight A1 classes, and the
  loader-invariant check reports 0 defects. Gate file unchanged by this check.

No blockers.
