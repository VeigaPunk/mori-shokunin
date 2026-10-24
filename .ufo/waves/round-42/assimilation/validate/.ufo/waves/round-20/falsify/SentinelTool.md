PARTIAL

Scope: reviewed `tools/mori-wave-settlement.py` for traversal, symlink handling/TOCTOU, resource bounds, report-byte emission, path disclosure, and determinism. No production files were edited and no tools were installed. All probes used fixtures under `.ufo/waves/round-20/falsify/SentinelTool/`.

## Findings

### MEDIUM — pathname checks are raceable; ancestor symlinks are accepted [INFERENCE]

**Exploit path:** a local writer able to modify the scanned lane can swap a checked directory for a symlink between `lstat` and the later path-based `scandir`/`open`. The recursive scanner does not retain directory descriptors (`tools/mori-wave-settlement.py:95-120`); `_read_regular_bytes` reopens the name after `lstat`, and `O_NOFOLLOW` protects only the final component (`:125-149`). Report paths are similarly checked component-by-component and later reopened by pathname (`:173-201`, `:221-234`). A replacement with a FIFO can also block the open because `O_NONBLOCK` is not set and the regular-file `fstat` occurs after open. I did not attempt to win a race.

**Evidence:** static traversal protections worked in scratch: `../../outside/secret.md` was `unsafe`; a symlinked report parent was `missing`; a symlink under `.ufo/waves` pointing to a directory containing a valid external dispatch was not followed (`rc=1 summary={"waves":1,"unreadable_json":0,"wave_names":["sentinel-scratch-probe"]}`). However, a lane root reached through a symlinked ancestor was accepted. The output showed `lane_root` ending in `/alias/lane` and the same wave was scanned. `scan_lane` uses `abspath` and `lstat` of the final root path, which follows intermediate symlinks (`:304-315`).

**Impact:** with concurrent write access, a scan can cross the intended tree boundary, ingest external dispatch metadata (including attacker-controlled `wave`, `name`, and `agent` values that are emitted), or stall on a raced FIFO. Ancestor-symlink acceptance is a boundary mismatch if the caller treats the supplied lexical path as a canonical confinement root.

**Smallest remediation:** anchor traversal at opened directory descriptors and use descriptor-relative `openat`/`scandir`-equivalent operations with `O_DIRECTORY|O_NOFOLLOW` for each component; open candidate files nonblocking and verify their type before reading. Reject or explicitly canonicalize the lane-root ancestry if callers require that boundary.

### MEDIUM — dispatch inputs and aggregate scan work are unbounded

**Exploit path:** a writer of the scanned tree can add very large dispatch JSON, many JSON files, or very large task arrays. `_dispatch_files` materializes all candidate paths (`:92-122`), `_read_regular_bytes` reads each entire file (`:125-149`), `json.loads` parses the complete byte string (`:320-333`), and the result/output is retained and serialized without byte, file, or member limits (`:341-363`, `:669-678`).

**Evidence:** a scratch dispatch of 2,000,454 bytes was accepted; `wc -c` reported `2000454` input bytes and `962` output bytes. The captured scan had `unreadable_json:0` and one discovered wave. The assignment's stated 3,411-JSON-file Kaidoku workload was not re-counted or benchmarked here; that count alone is not evidence of exhaustion, but the implementation has no budget for it or for attacker-sized records.

**Impact:** CPU and memory use scale with total input and generated output; sufficiently large or numerous records can exhaust the scanner process or the host running it.

**Smallest remediation:** impose explicit per-file and aggregate byte, file-count, and member-count budgets before full parsing/serialization, and report a bounded input-limit outcome. The 3,411-file case should be measured against those limits before claiming it is operationally safe.

### LOW — output exposes the absolute host path

**Exploit path:** any consumer of scan stdout or `--out` receives the full `lane_root` value (`:304-315`, `:355-358`).

**Evidence:** scratch output contained `"lane_root":"/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/SentinelTool/probe-20261021/lane"`. The contract explicitly includes `lane_root` (`.ufo/waves/round-20/contract.md:82-86`), so this is a privacy/schema tradeoff rather than an accidental serialization bug.

**Impact:** reports copied to shared artifacts disclose the operator's home path and workspace layout.

**Smallest remediation:** emit a stable lane-relative identifier or redact the absolute prefix by default; make absolute-path disclosure opt-in if consumers need it. This changes the frozen output contract and needs an explicit schema decision.

### LOW — determinism depends on the exact path spelling

**Exploit path:** invoke the scan on the same physical tree through a symlinked parent rather than its direct path. `abspath` preserves the alias spelling (`:305`), which is serialized at `:357`.

**Evidence:** two scans with the same root argument were byte-identical (`cmp` exit 0); the explicit `--out` file also matched stdout (`cmp` exit 0). A scan through `/.../probe-20261021/alias/lane` instead emitted that alias in `lane_root`, unlike `/.../probe-20261021/lane`. Thus stability holds for the same argument/tree state, but not for the same physical tree reached by aliases; the contract's “same tree” wording is broader unless it means same root spelling.

**Impact:** identical underlying lane state can produce different report bytes and digests when automation changes how it addresses the root.

**Smallest remediation:** define determinism as tied to the exact root argument, or serialize a stable canonical/relative root identity (coordinated with the privacy finding).

### LOW, conditional — explicit `--out` follows symlinks and truncates its target

**Exploit path:** a wrapper that supplies an untrusted `--out` value can redirect the write through path traversal or an existing final/parent symlink. `main` opens the supplied path directly with `"wb"` (`:669-677`).

**Impact:** the tool can overwrite any file writable by its caller if the output path is attacker-controlled. This is not an unconditional defect when an operator intentionally supplies a trusted output path; the contract explicitly permits `--out` writes.

**Smallest remediation:** if `--out` can cross a trust boundary, constrain it to a trusted output directory and open relative to a verified directory descriptor without following symlinks.

## What survived

- Lexical traversal and static symlink defenses behaved as expected in the scratch probes; the valid external dispatch behind a symlink was omitted.
- The stub-specific report read was exercised with `STATUS: started\n`: the result counted `stub:1`, and a content search of the serialized output found no `STATUS: started`, report canary, or outside canary. Source compares the bytes only to the stub constants and emits status/counts (`:221-229`); the existing content-not-emitted fixture/assertion is at `:488-490` and `:571-574`.
- For an unchanged tree and identical root argument, output bytes were repeatable and the `--out` bytes matched stdout.
- No TOCTOU race was run; race exploitability above is inferred from the path-based check/use sequence.
