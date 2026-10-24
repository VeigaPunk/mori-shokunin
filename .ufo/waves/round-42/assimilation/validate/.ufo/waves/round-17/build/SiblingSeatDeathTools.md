# Sibling seat-death tooling — overlap with C1 (mori round 17)

- Seat: `MoriR17.SiblingSeatDeathTools-5` (scout, read-only, no subagents)
- Date: 2026-10-20
- Question: existing detectors of seat death, `Retry budget exhausted`, `stopReason`,
  `errorStatus` or `429` **in transcripts**, under
  `/home/vgpnk/Projects/shokunin/*-shokunin/tools` and `/home/vgpnk/Projects/shokunin/scripts`.
- Verdict: **No existing tool implements any C1 terminal-status classification.** One sibling
  tool — `mado-shokunin/tools/mado-tripwire.py` — already implements C1's *scan frame* over the
  same `~/.omp/agent/sessions/**/*.jsonl` surface (same record filter, same 0/1/2 + pinned-replay
  posture) for a different question. It is the precedent C1 should align with, and the main
  divergence hazard C1 must not copy blindly.

Confidence: high for every literal hit below (each was read in context, not inferred from the
match text); medium for the negative inventory (bounded to the two named roots, see §7).

## 1. Method

1. Enumerated every tools root under the fleet (8 present: chousa, kama, kotodama, mado, mori,
   souji, tameshi, tsukuroi; 13 lanes have no `tools/`) plus `scripts/` (17 files, 2
   subdirectories) — `ls` loop, exit 2 only for the absent dirs.
2. Literal sweeps for `Retry budget exhausted`, `stopReason`/`stop_reason`,
   `errorStatus`/`error_status`, `429`, `rate_limit`/`RATE_LIMITED`/`resource_exhausted`,
   `quota`/`usage limit`/`402`/`credits`, `aborted`, `message_end`, `credential_pin`,
   `retryRecovery`, `customType`, `.jsonl`, `sessions`, `transcript`, `--max-files`, `tail`.
3. Re-ran the inventory as an independent Python walk (2 MB per file cap, `\0` binary skip,
   `.git`/`.jj` pruned) because the first grep pass capped its output and hid two `.jsonl`
   consumers (`mado-tripwire.py`, `research-gate.sh`). The Python sweep is the authoritative
   inventory; the grep-tool calls were corroboration.
4. Read every candidate's surrounding code before classifying it. No LSP server answers shell or
   Python scripts in this fleet, and no `lsp` device was available in this seat's tool inventory,
   so locations are literal matches grounded by direct source reads — no semantic-absence claim
   rests on a cold/empty LSP result.

## 2. Direct hits and their overlap with C1

### 2.1 `mado-shokunin/tools/mado-tripwire.py` — the near neighbour

Post-hoc tripwire over **OMP session transcripts (JSONL)** that classifies commands a seat
*issued* (`bash` / python `eval` tool calls), never executed. Functional question differs from
C1, but the scan frame is almost exactly C1's.

| C1 clause | mado-tripwire.py | Overlap / difference |
|---|---|---|
| Target surface | `:1484-1488` confines any path under `~/.omp/agent` to `~/.omp/agent/sessions`; refuses elsewhere | Same transcript tree. **C1 must NOT copy**: C1 takes an arbitrary `--sessions-dir DIR`, and its fixtures live under the lane (`.ufo/waves/round-17/fixtures/seat/`), which this guard would refuse. |
| Recursive `*.jsonl`, no symlink follow | `:1494-1513` `os.walk(..., followlinks=False)`, sorted dirs/files, dedupe by `realpath`; `:1476-1492` root `lstat` symlink refusal; `:1489` basename refusal `^agent\.db` | Same shape. No `--max-files` cap (C1 adds one, rc2 `too-many-files`). Walk-reached symlinked files hit `refuse_path` inside `scan_file` (`:1527-1529`) → hard `could_not_evaluate`; the C1 contract says "never follow" without naming skip-vs-rc2 — fixtures must pin one. |
| Consider only `type == "message"` with dict `message` | `:1554-1557` exactly `obj.get("type") != "message": continue`; `msg = obj.get("message")`; `isinstance(msg, dict) and role == "assistant"` | **Exact same record filter** (tripwire further needs role assistant because it reads toolCalls). Tripwire errors on `"type" not in obj` records (`:1552-1553`); C1 skips unparsable lines. |
| Skip malformed JSON lines | No — `:1548-1551` raises `CouldNotEvaluate` on the first invalid line | **Opposite** of C1 (`skip lines that fail`). Do not copy. |
| Tail-bounded read | No — `:1531-1533` `fh.read()` whole file, sha256 over all bytes | C1's `--max-tail-bytes` + drop-partial-first-line has **no** transcript precedent (see §2.4). |
| Terminal-record class rules | None. Scans every assistant message in file order; ignores `toolResult` by design (`:27`) | **Zero overlap** with C1's completed/aborted/dead_*/incomplete/unavailable classes. |
| Privacy on output | `:200-206` only `.jsonl` opened, `agent.db` refused, secret-pattern redaction, `MAX_COMMAND=240` (`:223-227`, applied `:1601`); "Transcript text is data" (`:73`) | Same safety posture. C1 is stricter by contract: **never** emit `errorMessage`/content, only codes and class. |
| Output / exit | `:1625-1629` prints `MADO_TRIPWIRE: <label>` then JSON; rc 0 clean / 1 findings / 2 could-not-evaluate, 2 wins (`:78-90`) | Same 0/1/2 idiom, **two-line** output. C1's contract is JSON-only stdout; do not copy the verdict line. |
| Pinned replay + selftest | `--frozen DIR` digest-pinned replay (`:1631+`, `FROZEN_SCHEMA`), `--selftest DIR`, tamper labels (`:91-95`, `:1845-1953`) | Same gate philosophy as C1's `mori-round17-seat-regressions.py` (input SHA, replay, red controls), but no shared code. |

### 2.2 `scripts/hyaku/probe-alias.sh` — the only `stopReason` reader in the fleet

- `:14` runs `omp -p --mode json`, `:18` matches `type == "message_end"` events, `:20`
  `if m.get("stopReason") == "error"`, `:21` appends
  `tag + " ERR " + (m.get("errorMessage") or "")[:70]`, `:19` tags `provider/model`.
- Overlap with C1: field names `stopReason`, `errorMessage`, `provider`, `model`, and the idea
  of naming the answering hop. Different source (live CLI JSON event stream, not transcript
  tails), no classification, no counts, no exit contract.
- **Hazard:** it prints the first 70 chars of `errorMessage`. C1's contract forbids emitting
  `errorMessage` at all; reuse the field access, never the formatting.

### 2.3 `scripts/hyaku/await-capacity.sh` — the only sessions-dir `*.jsonl` walker

- `:4-6` comment: "Proxy for running subagents: subagent transcripts (`*.jsonl`) under the
  session dir written within the last WINDOW seconds"; `:11`
  `find "$d" -name '*.jsonl' -newermt ... | wc -l`.
- Overlap: same directory convention; file discovery only. No parsing, no tail, no regular-file
  or symlink discrimination, no caps, no classes. C1 cannot reuse it (mtime filter is a
  different question) but should keep the same "transcripts live as `*.jsonl` under a session
  dir" assumption so the two tools do not disagree about what a seat transcript is.

### 2.4 `kama-shokunin/tools/kama-llamacpp-live.py` — the only byte-tail reader (non-transcript)

- `:79` `LOG_TAIL_CAP = 65536`; `:807-815` `fh.seek(0, os.SEEK_END)`, seek to
  `max(0, size - LOG_TAIL_CAP)`, read, decode with `errors='replace'`,
  `out['log_tail_truncated'] = size > LOG_TAIL_CAP`.
- Overlap: the mechanical tail-read-with-truncation-flag pattern C1 needs. Different target
  (llama server log, line filter), and it does **not** drop a partial first line — C1 must add
  that (contract) because a byte-offset seek lands mid-record.

### 2.5 Seat-level but not transcript-based (context, no overlap)

- `souji-shokunin/tools/souji-seat-audit.py:2-8,43-46` reads harness-rendered
  `<SeatName>.txt` exports from `history://<lane>.<SeatName>`, audits tool calls against a wave
  spec. It explicitly "reads no transcript store directly" (`:43`) and has no terminal-status
  notion.
- `tsukuroi-shokunin/tools/check-seat-scope.py:12-15` audits the `Scope: executed=` trailer in
  seat reports; no transcript.
- `scripts/shokunin-watchdog.sh:402` logs `lane-dead-no-report $lane round=$n` after
  `mission_live` (`:227-237`) fails — lane/round granularity from process liveness, not seats
  from transcripts.

### 2.6 Prose that names the exact failure C1 targets (no detector)

- `scripts/hyaku/lane-addendum.md:90-95` — zai `429 Rate limit reached for requests
  (type=1302)`, "~130 seats died with 'Retry budget exhausted after 10 retries'", per-lane
  losses, and the `retry.maxRetries` 10→40 mitigation.
- `:24`, `:63`, `:101` require each closure to report "dead seats" by hand; `:101-102` "A dead
  seat stays dead in the evidence." C1 is the machine capability this prose assumes a human
  provides.
- `:84-89` also documents `402 out of credits` and per-alias cascade facts — C1's
  `dead_quota`/`provider/model` tallies would make those prose claims measurable.

## 3. Tokens with zero code hits (C1 novelty)

Across the named roots, after the independent walk:

| Token / capability | Occurrences |
|---|---|
| `errorStatus` / `error_status` | **0** |
| `retryRecovery`, `credential_pin`, `customType`, `stop_reason` | **0** |
| `429` as a matcher | **0**; only prose `lane-addendum.md:90-95` |
| `rate_limit` / `RATE_LIMITED` / `resource_exhausted` | **0** |
| `quota` / `usage limit` / `402` / `credits` as matchers | **0**; `402 out of credits` prose only (`lane-addendum.md:84-89`) |
| `aborted` as a `stopReason` value | **0**; `aborted` hits are quarantine counters (`souji.../cand-s16-cert.py:1080,1127`, `cand-f1-quarantine.sh:1095`) |
| `Retry budget exhausted` as a matcher | **0**; prose `lane-addendum.md:92-93` only |
| last-message/terminal-record selection | **0** |
| `--max-files` cap | **0** in these roots |
| transcript tail read + partial-first-line drop | **0** |

## 4. Matched `.jsonl` but not overlap (sweep completeness)

- `chousa-shokunin/tools/research-gate.sh:199-200,2639-2646,2787` — `claims.jsonl` /
  `manifest.jsonl` are research-record inputs and receipts, not transcripts. Shares only the
  pin/drift baseline replay idiom.
- `mori-shokunin/tools/mori-journal-window.py:726` — a selftest fixture named `payload.jsonl`
  (journal stub payload), not a session transcript.
- `mori-census.sh:118,2312-2505,3834-4012` — "sessions" are tmux sessions, not OMP transcripts.
- `scripts/hyaku/ufo-wave-policy*.json:199` — "transcript handoff" prose about judge-handoff
  profiles, no reader.

## 5. Consequences for C1 (advisory, not a judgment)

1. **Scope the novelty claim.** "First reader of OMP seat transcripts" is false —
   `mado-tripwire.py` already opens that store. The defensible claim is *first terminal-status
   classifier* over seat transcripts, which is exactly what C1's contract says. If wave-2
   critic seats test an overbroad novelty sentence, it fails.
2. **Do not import tripwire's path guard.** `:1484-1488` (`refused path outside
   ~/.omp/agent/sessions`) would reject the lane fixture packs and any copied fixture tree.
   C1's `--sessions-dir` must accept arbitrary DIRs.
3. **Do not import tripwire's parse strictness or whole-file read.** `:1548-1551`
   hard-fails on a malformed line and `:1531-1533` reads the whole file; both contradict C1's
   "skip lines that fail" and `--max-tail-bytes`.
4. **Keep C1's stricter output.** `probe-alias.sh:21` (prints `errorMessage`) and
   `mado-tripwire.py:223-227,1601` (redact + cap command text) show the house has two
   precedents; C1's "never emit errorMessage/content/usage" is stricter than both and should
   stay that way. The `--help` limits text (last-observed state, seats-not-incidents, naming
   prefixes) has no precedent and must be authored.
5. **Gate conventions.** C1's regression gate can mirror the lane's own `mori-round15/16`
   run-manifest + input-SHA conventions (`.ufo` evidence), and mado's tamper labels are a
   useful vocabulary (`snapshot_tampered`, `frozen_verdict_mismatch`) if a reviewer expects
   consistent failure naming. No code sharing is warranted: the C1 contract fixes its own
   `match|mismatch|capability_absent` vocabulary.
6. **Fixture edge C1 should pin because of this survey:** a symlinked `*.jsonl` (skip vs rc2),
   a malformed JSONL line mid-tail (must skip, unlike tripwire), a tail that begins mid-record
   (drop first line), a file at exactly `--max-files` and one over, and a transcript whose last
   message is a `credential_pin`-adjacent record type (skipped unread).

## 6. Evidence log (commands, exit 0 unless noted)

| Command (summarised) | Result |
|---|---|
| `ls -d <fleet>/*-shokunin/tools <fleet>/scripts` loop | 8 tools dirs present; 13 lanes `No such file or directory` (exit 2 on those iterations, loop continued) |
| grep-tool sweeps over the two roots for the token set | Corroborating; first pass output-capped, so discarded in favour of the Python walk |
| `python3` walk #1 (`.jsonl`, `stopReason`, `errorStatus`, `429`, `message_end`, `rate_limit`, `credential_pin`, `retryRecovery`) | exit 0; 72 hits, of which 2 transcript consumers (`mado-tripwire.py`, `await-capacity.sh`) and the rest `.jsonl` non-transcripts listed in §4 |
| `python3` walk #2 (`transcript`, record filters, `sessions`/tail) | exit 0; surfaced `mado-tripwire.py:2-73`, `souji-seat-audit.py:2-46`, `kama-llamacpp-live.py:79,807-815` |
| `python3` walk #3 (`customType`, `stop_reason`, `stopReason`, `errorStatus`, `retryRecovery`, `credential_pin`, `"aborted"`) | exit 0; 11 hits, only `probe-alias.sh:20` relevant |
| `sed -n`/`grep -n` reads of `mado-tripwire.py:1-100,1470-1690`, `probe-alias.sh`, `await-capacity.sh`, `status.sh`, `shokunin-watchdog.sh:200-260,370-414`, `souji-seat-audit.py`, `check-seat-scope.py`, `lane-addendum.md:84-106` | exit 0 |
| No selftest, gate, or tool was executed. No installs or upgrades (nothing needed). | — |

## 7. Limits and remaining unknowns

- Inventory is bounded to `<fleet>/*-shokunin/tools` and `<fleet>/scripts` as assigned. It does
  not cover `~/.omp` harness code, `.devin/agents` profiles, lane `.ufo` evidence trees, or
  other seats' clones; a detector living there would be missed. [INFERENCE] none is likely,
  since the transcript store is the shared surface and mado's tool is the known consumer.
- Working-tree state was read as found on 2026-10-20; tracked-vs-untracked status was not
  checked (no VCS reads were needed, and no VCS mutation was performed anywhere).
- No LSP was available for these shells/Python scripts; semantic conclusions were drawn from
  reading the cited bodies, not from symbol lookup. No cold-LSP "absence" is claimed.
