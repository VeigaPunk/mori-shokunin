# LegacyFrozen — round-18 frozen retention snapshot: shape, digest limits, no-rewrite constraints

Seat: MoriR22.LegacyFrozen (read-only scout). Scope: `.ufo/waves/round-18/gate-snapshots/retention/retention.json` plus its direct consumer `tools/mori-retention-gate.py` (`frozen_run`, `_blob_hits`, `SNAPSHOT_PINS`), read as Git blobs at entering revision `77a5bbe8a0b41dfbfd2546d024d36e294b814bd0`. No matched text, decoded content, `content_b64` value or regex text appears below.

## Observed facts

Commands run: read-only `git -C` (`log`, `rev-parse`, `ls-tree`, `merge-base --is-ancestor`, `grep`, `show`, `diff --stat`), `sha256sum`, `ls`, and an in-process SHA-256 over the decoded snapshot line (never printed). No gate, selftest, test or build was run. Nothing was installed.

1. **Provenance.** The snapshot was added once, in `b8f5c6c38e591fed20c1e121af187e58c959c1fe` (round-18 C1 retention gate). Its blob is `79b0368b8498785e1b0e660943fa6e0ed0f65a1a` at that commit, at entering revision `77a5bbe8…`, and at HEAD `306e06ec…`. The entering revision is an ancestor of HEAD. `git status` is clean for the file, and `git diff --stat 77a5bbe8 HEAD` is empty for both the gate and the snapshot directory.
2. **Byte pin.** The file's SHA-256 is `55fcdd710d2bec1eef198997b3ccfa4fc584b7c7d44ad447fccf6fa48d8a00e8`, which equals `SNAPSHOT_PINS["retention.json"]` in the gate. The file is 756 bytes and is the only entry in its directory.
3. **Shape (`mori-retention-frozen-snapshot-v1`).**
   - Top-level keys are `schema`, `policy`, `files` and `expected`.
   - `policy` has `classes` (one class, `R4`), `must_redact_paths` (one entry, `fixture/must-redact.md`) and `non_author_paths_glob` (empty). It has no `schema` key, so `frozen_run` calls `validate_policy(..., require_schema=False)`.
   - `files` holds one item with the exact key set `{path, content_b64}`. Its decoded payload is 45 bytes, contains no NUL, and ends in a newline. Splitting on `"\n"` gives two parts, and the last part is empty.
   - `expected` is exactly `{finding_id: RETENTION_FINDINGS, exit_code: 1, metric: 1, routed: 1, hits: [one hit (path, line 1, R4, line_sha256)]}`.
4. **Frozen run semantics (gate lines 331–395 at the entering revision).**
   - The default directory is resolved from the tool's own location: `Path(__file__).parents[1]/.ufo/waves/round-18/gate-snapshots/retention`.
   - The directory's file set must equal `{retention.json}` exactly, and symlinks are rejected.
   - The bytes must match the pin, and the JSON and schema must be valid.
   - Hits come from `_blob_hits` and are scored by `_scan_result(hits, must, non_author, [], None, None)`, with no allowlist and no population.
   - `expected != actual` is an ordered dict/list equality, so hit order matters.
   - Results: `FROZEN_OK` exits 0, `FROZEN_VERDICT_MISMATCH` exits 1, and `snapshot_tampered` exits 2. The selftest's tamper arm appends one byte in a scratch copy and expects exit 2 with `snapshot_tampered`.
5. **Expected digest reproduction.** `line_sha256` equals SHA-256 of decoded line 1 *without* its trailing newline. With the newline it does not match, and the whole blob does not match either. This agrees with `_blob_hits`: skip if the blob has a NUL, decode with `errors="replace"`, `text.split("\n")`, then `sha256(line.encode("utf-8"))` per matching class.

## Limitations of the frozen evidence

- **The digest is not secrecy.** `line_sha256` is an unsalted hash of a short, low-entropy line, so it can be confirmed by guessing. The snapshot also carries the full matched line in `content_b64`; base64 is not redaction. Restating the contract: a source hash is neither secrecy nor authentication.
- **The pin is a self-pin.** The gate pins the snapshot with a constant inside the same file that reads it. If both are edited together, the gate cannot detect it. The only authority is Git history (`b8f5c6c`), and no signature exists.
- **Thin coverage.** It covers one class, one file, no `non_author` globs, no allowlist, no expected population and no Git tree. It exercises none of these: policy-path exclusion, the scanner denominator, non-author partitioning, forbidden allowlist rows, duplicate hits, NUL skipping or provenance binding. A `FROZEN_OK` result therefore says nothing about R03–R24 of the round-22 contract.
- **It is not a receipt.** It has no `measured_revision`, `argv`, `stdout`, `stderr` or wrapper schema, so it is not a `mori-r21-command-receipt-v1` input for `check --repo --rev --receipt`. Its policy is inline rather than a repository path, so `policy_excluded` (the "supplied policy path" exclusion) is undefined for it, not zero.
- **It is red by design.** `exit_code: 1` and `metric: 1` are the frozen expectation. A red frozen verdict is correct behavior, not a defect, and matching it is not privacy clearance.

## Constraints for the new tool (`tools/mori-retention-reconcile.py`)

1. **Never write into the round-18 snapshot directory, not even an added sibling file.** The gate's exact file-set check would turn the historical frozen run into `snapshot_tampered` (exit 2), because `frozen_run` treats any change to the file set as tampering. Round-22 expected values and fixture generators belong under round-22 paths.
2. **Do not edit the gate, `SNAPSHOT_PINS` or `retention.json`.** Do not re-serialize the JSON either; any re-encoding changes the bytes and breaks the pin. The contract also requires the existing retention implementation and history to stay unchanged.
3. **Do not treat the frozen snapshot as a receipt, and do not convert it into one in place.** If a synthetic Git fixture is ever built from it, it must be a new fixture in an executor's `.scratch/round22` clone. That fixture would still lack the policy-path dimension, so it cannot substitute for the R03 fixture (raw_total 5, policy_excluded 1, scanner_total 4).
4. **Reproduce the hashing exactly but independently, without importing the gate.**
   - Skip any blob containing a NUL.
   - Decode with UTF-8 `errors="replace"` and hash the *replaced* text, not the original bytes.
   - Split on `"\n"` only, so a `\r` stays inside the hashed line, and line numbers are 1-based.
   - Emit one hit per matching class per line.
   - Hash each line without its terminator.
   - Comparison must be by multiset identity `(path, line, class, line_sha256)`, not ordered equality; the frozen run's ordered comparison is a gate-specific property.
5. **Copy no snapshot content.** Do not copy `content_b64` or any decoded text into receipts, fixtures, reports or stdout (R23). Reference the snapshot only by path, blob id or SHA-256.

## Confidence

- **High:** items 1–5 (observed directly), and constraint 1. Constraint 1 follows from the file-set check I read, but I did not run it.
- **[INFERENCE]:** that `policy_excluded` is undefined rather than 0 for this snapshot. It follows from the inline policy and the contract wording "exactly the supplied policy path".

## Remaining unknowns

- I did not observe whether `--frozen-run` currently returns `FROZEN_OK` (exit 0) at the entering revision or HEAD, because running it is reserved for L1.
- The disposition of the round-18 wave stays unknown, and baseline acceptance stays blocked. Nothing in this file changes either.

## Checks for L1 after integration

- Before and after integration, run the existing gate's `--frozen-run`. Expect exit 0 and `FROZEN_OK` both times, with `snapshot_sha256` = `55fcdd71…`.
- Run `git -C <repo> diff --stat 77a5bbe8 <integrated>` on `.ufo/waves/round-18/gate-snapshots/` and on `tools/mori-retention-gate.py`. Expect it to be empty.
- Run `git -C <repo> ls-tree <integrated> .ufo/waves/round-18/gate-snapshots/retention/`. Expect exactly one entry, blob `79b0368b…`.
