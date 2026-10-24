# ReviewR1Patch — routed r25 R1 fix, `tools/mori-job-runway.py`

**Verdict: partial** — the routed r25 R1 fix already sits below the base `6ebd518f`, so the assigned diff is empty; the primary false-number fix holds at the target, but two secondary R1 items (`--cases ""`, FIFO/`/dev/zero`) are still open at `f2de0eed` and the seat is still working, not carried.

## Assigned-diff check

- `git diff 6ebd518f f2de0eed -- tools/mori-job-runway.py tools/fixtures/mori-job-runway` → **0 lines**.
- Tool is byte-identical at both revisions: `sha256 5d90d7d43df0fc91f398f971c2e53419d1e8d100503f08193e968b5fe12c3411`.
- `git merge-base --is-ancestor` confirms the whole R1 chain is under the base: `7634be7` (freeze), `09f55b6` (tool), `9a3d511` (abstain + R01–R18), `fbecc59` (selftest strictness), `d3b7af2` (R19–R24) — all committed 2026-10-22 during round 25.
- Per contract `.ufo/waves/round-28/contract.md:69-71`, r25 R1 is routed hygiene "landed only when a non-author check passes; otherwise carried with the reason".

## R1 items vs committed code at `f2de0eed`

Temp extract at `/fast/scratch/hyaku/mori-r28-w2/ReviewR1Patch/extract/` (git-show of target blobs). Selftests run there:

- `--selftest` → `MORI_JOB_RUNWAY_SELFTEST: PASS 21/21`, exit 0.
- `--selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json` → `PASS 24/24`, exit 0.

| R1 item (lesson lines 174-179) | State at target | Evidence |
|---|---|---|
| Rule 1 abstains on quoted/spaced/anchored `async` headers, flow children/roots, indented roots | **fixed** | `_parse_config` returns `malformed` for quoted/spaced `async`, merge keys, complex keys, `---`/`...`, tabs, multi-async, non-plain values (tools/mori-job-runway.py:241-367); cases R01–R18 pin each form to `RUNWAY_UNKNOWN` exit 2 |
| Probe corpus committed as fixtures | **fixed** | `tools/fixtures/mori-job-runway/supplementary-cases.json` (24 cases, ids R01–R24 with `what` + `expect`) |
| `set` for files Bun refuses to parse | **fixed** | every non-plain form maps to `malformed` → `configured.state="malformed"` → `RUNWAY_UNKNOWN`, never `set` |
| `--selftest --cases ""` silently runs frozen cases | **still open** | `_resolve_cases` uses `if cases_override:` (truthy) at tool line 519, so `""` falls to `_cases_path()`; live run: `--selftest --cases ""` → `PASS 21/21`, exit 0. A nonexistent path correctly fails (`FAIL 0/0`, exit 2), proving the empty-string path is inconsistent, not a policy |
| Uncaught exceptions exit 1 (collides with `RUNWAY_CLAMPED`) | **still open** | `main` (tool lines 666-690) wraps only `parse_args`; `evaluate`, `_emit`, `_selftest` run unwrapped. `BrokenPipeError`, `RecursionError`, `fstat`/`mmap` races still escape as exit 1 |
| No guard on FIFO or `/dev/zero` | **still open — reproduced** | `--config <fifo>` → killed by `timeout 3` (exit 124; blocking `read()`); `--config /dev/zero` → exit 124 (unbounded `handle.read()`, tool line 228); `/dev/null` correctly returns `absent`/`RUNWAY_UNKNOWN` exit 2. Binary side: `_binary_sites` opens FIFOs blocking (line 393) though `mmap` on size-0 raises `ValueError` → `unreadable`; a binary FIFO with a writer could still block on `open` |
| Untested CLI exit and unreadable-binary paths | **partially open** | no CLI-exit cases in either committed corpus; live check: unreadable binary → `binary_sha256: null`, clamp `unreadable`, `RUNWAY_UNKNOWN` exit 2 (correct behavior, but not pinned by a fixture) |

## Was carrying right?

Not yet a carry: `agent://MoriR28.FixR1Runway` is still running — latest text "tighten the remaining false-number paths (parse-error class) and fix `--cases ""`", which matches the two items above. The empty diff therefore does **not** mean "already fixed": the seat's remaining work is real, and the primary abstention fix being pre-baked into the base is the reason the assigned diff is empty (base was cut after the round-25 wave-2 commits). Carrying would only be right if the non-author check fails; my reproduction shows genuine defects, so a sandboxed fix remains warranted.

## Findings by severity

1. **F1 (medium): tool hangs on FIFO config and `/dev/zero` config** — unbounded/blocking `read()` at tool line 228; reproduced exit 124 under `timeout 3`. R1 named this explicitly.
2. **F2 (medium): `--selftest --cases ""` silently reports `PASS 21/21`** against the frozen corpus (tool line 519 truthiness check); a caller passing an empty var gets a false pass. Explicitly named in R1.
3. **F3 (low): uncaught exceptions still exit 1**, indistinguishable from `RUNWAY_CLAMPED` — no `try`/`except` around `evaluate`/`_emit` in `main`.
4. **F4 (low): CLI-exit and unreadable-binary paths unpinned** — behavior is correct live (unreadable binary → `RUNWAY_UNKNOWN` exit 2) but no committed case covers it.

## Residual risk / verification gaps

- [INFERENCE] Bun's exact YAML acceptance may differ from the supplementary corpus on forms not yet probed; only the pinned 24 forms are verified.
- Did not exercise the binary-side FIFO with a live writer (bounded-time risk only); `_sha256`'s unbounded `read` on `/dev/zero` as `--binary` is the same defect class as F1 — `timeout 3` on `--binary /dev/zero` was not run to keep probes short [unrun].
- I did not verify whether FixR1Runway's in-flight patch resolves F1–F3; verdict applies to committed bytes at `f2de0eed` only.

## Tooling

No installs; used system `python3`, `git`, `mkfifo`, `timeout`. Report path per bounds: `.ufo/waves/round-28/w2/ReviewR1Patch.md`.
