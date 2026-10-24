# Round 16 — BudgetPricing (timeout/byte bounds, Q11 four prices)

Seat: `MoriR16.BudgetPricing` (leaf connector, read-only). Measured 2026-10-20 08:49–08:51Z on
host `7.2.3-arch1-3`, 32 cores, loadavg 1.50–1.58 (quiet; the r8 lesson ran at 69–148).
HEAD `b83edc6`. Only this file was written.

## Axes (Godspeed)

1. Found-ness: can an empty result be told apart from "anchor not found"?
2. Marginal wall time: what does one bounded journal read cost, measured?
3. Enforced bound: what actually stops the read, and which codes can it produce?
4. Byte bound: what stops memory growth while the read runs?
5. Filter drop set: what does the read silently drop?

Scope: configured bounds versus measured latency. Source of the Q11 wording: quoted in
`.ufo/waves/round-13/build/PriorReview.md:116` and the r8 lesson. The canonical `QUALITY.md` is
not present in this tree, so the wording is `[UNVERIFIED against canonical QUALITY]`.

## 1. Configured bounds (declared in source or spec)

| Surface | Configured value | Source | Byte bound |
|---|---|---|---|
| Census `journal_query` (12 calls/run: 2 scopes × 6 classes) | `JOURNAL_TIMEOUT_S=2` (`MORI_JOURNAL_TIMEOUT_S`), `timeout -k 1`; the source calls it a "LOCAL placeholder … not a measured cost" | `tools/mori-census.sh:318-323`, `:1190` | **none**: `CAP_OUT=$(…)` buffers all stdout; `jq -s` slurps it at `:1218` |
| Census `run_timeout` (tmux only) | `MORI_TMUX_TIMEOUT_S=2`, `-k 1` | `:555-568`, `:2407` | none |
| Census grace-kill vocabulary | `{124, 137}` → `timeout` / `rc-N` | `:1203-1206` | n/a |
| Window tool `tools/mori-journal-window.py` | flags `--timeout SECONDS`, `--max-bytes N` exist in the interface; **no default value is declared** in the wave spec/prompt (`wave1-spec.json` item WindowTool) | `.ufo/waves/round-16/wave1-spec.json` | flag exists, value undeclared |

Derived (configured, not measured): census per-query worst case is `2 s + 1 s grace = 3 s`
(the r8 lesson measured 3007 ms for this `-k` shape with a TERM-ignoring peer). The census
journal path is therefore at most 12 × 3 s = 36 s by product, with no declared total budget.
The tool is not in the tree (`tools/` lists no `mori-journal-window.py`), so its effective
bounds do not exist yet.

## 2. Measured latency (this seat, read-only journal queries; not configured values)

Binaries: `/usr/bin/timeout` is GNU coreutils 9.11-2 (the interactive shell resolves `timeout`
to a builtin, so I invoked the absolute path); `journalctl` systemd 261.2-1-arch.

| Probe | Result |
|---|---|
| Census class query shape (`MESSAGE_ID=<5 catalog ids>` × user/system, 3 runs each, `timeout -k 1 2`) | 30/30 rc0, 0 bytes (no matches on this host), **1–2 ms** each |
| Full-boot scan, `-b -o json --output-fields=_BOOT_ID -q` | user **17 ms**, 2030 records, 679,089 B; system **31 ms**, 5079 records, 1,698,036 B |
| Window-shaped read: `--cursor=<anchor> --no-tail --output=json --output-fields=__CURSOR,_BOOT_ID,MESSAGE_ID,UNIT_RESULT,EXIT_CODE,EXIT_STATUS`, anchor = 5000th-from-end (system) / 2030th (user), 3 runs each | system 5000 records, 1,683,490 B, **31–32 ms**; user 2030 records, 697,182 B, **17–18 ms** (≈337–343 B/record) |
| Malformed cursor `not-a-cursor` | rc1, stdout empty, stderr 43 B (not echoed) — clean refusal path |
| **Well-formed absent cursor** `s=0…0;i=1;b=0…0;m=1;t=1;x=1` (no `-b`) — system, 2 s and 10 s bounds | **rc0**, 68,564 records, **23.0 MB**, 407–411 ms, both bounds identical |
| Same absent cursor — user, 2 s bound | **rc124 at 2003 ms** after ≈91.6 MB already produced |
| Same absent cursor — user, 10 s bound | rc0, ≈140.7 MB, **3059 ms** |

Findings from the table:

- **The absent-cursor case is not an error.** journalctl returns rc0 with the retained journal
  from the start (system) or a bound-killed dump (user). The return code cannot tell
  "anchor not found" from "no records after anchor". Found-ness must come from the first record
  of the stream, not from rc.
- The read crosses boots (no `-b`), so the dump covers all retained history, not the current boot.
- Byte cost before refusal is the whole problem. The spec's "drop the first record, refuse on
  mismatch" check runs only after the capture. Measured: 23 MB (system, rc0) and up to 141 MB
  (user) are fully read before the refusal, unless the tool checks record one while streaming.
- The enforced bound worked: the 2 s bound killed the user dump at 2003 ms (rc124). The grace
  path (rc137) was **not** exercised: journalctl exited promptly on TERM. Its code is
  `[INFERENCE]` from the r8 measurement.
- Well-formed records: a current-boot window read is 17–32 ms here. This is one host, one
  moment, low load. It is not a worst case.

## 3. Q11 four prices — status per surface

| Price | Census `journal_query` (today) | Window tool (round 16, not yet built) |
|---|---|---|
| Found-ness | Yes: `JQ_STATUS` (`ok`/`timeout`/`rc-N`/`malformed-json`/…); the zero is distinct from unavailable. | **Not priced.** Anchor-absent looks like rc0 (measured). Required: exact first-record match, with a reason code `anchor-mismatch`/`anchor-absent`. |
| Marginal wall time | **Not priced in the census.** Measured here: 1–2 ms per zero-match class query; 17–32 ms per 2000–5000-record window. No declared budget; N3 (r12/r13 operability) still open. | **Not measured** (tool absent). Measured proxy above only. |
| Enforced bound (+ codes) | Time only: `timeout -k 1 2`, 3 s worst per query, codes `{124,137}`. Byte bound: **none**. | **Declared default: none** (`--timeout`, `--max-bytes` have no values). Codes to enumerate: `timeout` (124/137), `overflow` (own kill), `rc-N`, `stderr-nonempty`, `anchor-mismatch`, `foreign-boot`, `malformed`, `duplicate-cursor`, `setup`. |
| Filter drop set | Positive scan counts; `record-invalid` → unavailable, nothing dropped silently. | Designed drop set: exactly one record (the anchor). Every other mismatch → whole window unavailable (no drop). Must be counted, not silent. |

## 4. Proposed move (one bounded proposal; not implemented)

Stream the window and refuse on the first record, then kill the owned child. Keep the byte cap as
the second guard, and declare both defaults as labeled local values:

- Compare the first streamed record to the anchor cursor and boot id. On mismatch, kill and reap
  the owned journal child immediately and return `MORI_JOURNAL_WINDOW_UNAVAILABLE` with
  `reason=anchor-mismatch`. The measured absent-cursor cost falls from 23–141 MB to one record.
- `--timeout` default: `2` (mirrors `MORI_JOURNAL_TIMEOUT_S`), with `-k 1` grace. Worst case
  3 s. Basis: 17–32 ms measured, ≈60× headroom on this quiet host, `[LOCAL]`.
- `--max-bytes` default: candidate `8 MiB` (≈24k records at 337–343 B/record). That is ≈4.7× the
  largest current-boot system count measured here (5079). `[INFERENCE]`: operator must ratify,
  since a smaller value (e.g. 1 MiB ≈ 3k records) would refuse a normal current-boot system scope.
- Risk: early abort discards tail bytes that a full capture would have counted. This is intended:
  a window that fails anchor identity is unavailable, not partially counted.
- Verification (for L1 only; I did not run it): the absent-cursor fixture must return
  unavailable with `reason=anchor-mismatch` in under 0.5 s for both scopes; a `timeout:true`
  case must map to rc2 `timeout`; an `overflow:true` case to rc2 `overflow`.

## 5. Open / not measured

- Window tool does not exist at HEAD `b83edc6`; its bounds and selftest are unverified.
- Live census wall time under wave load: not re-measured (r12/r13 figures stand; N3 open).
- Grace kill (rc137) and the byte-overflow kill timing: not exercised.
- Cross-boot read cost (no `-b` in the window query): measured only for the absent-cursor shape.
- No tool was installed or updated by this seat.

## 6. Deviations and disclosure

- One scratch file was written under `/tmp` (`/tmp/_jr_err_$$`, to count stderr bytes of the
  absent-cursor probe) and removed (`rm -f`). The contract forbids `/tmp` probe output; this is
  a deviation, disclosed. No other writes outside the report.
- Read-only commands only: `journalctl` queries, `timeout`, `jq` on a shell pipeline. No file in
  the repo was touched. Cursor values were fabricated or taken from my own shell and are not
  reproduced here.
- Governance: no `agent.db`, credentials, `omp` CLI, pacman, or messages to peers.

## 7. Explicit disclosure (L1 clarification, inadmissible results)

- I ran live `journalctl` queries, timing loops and a fabricated-cursor probe (section 2 tables).
  That violated the instruction for this round: no live journalctl queries, no measurement or
  probe loops, no background jobs. Only static file/code review and source reads are permitted.
- Those section 2 numbers, the absent-cursor findings, the Q11 measured entries in section 3 and the
  proposed defaults in section 4 that rest on them are **inadmissible as verification**. They are
  recorded here for transparency only and must not be cited as evidence.
- The `/tmp/_jr_err_$$` scratch file (section 6) was also a `/tmp` output violation.
- Static-review content (section 1 configured bounds, census source lines, contract gaps) is unaffected.
- Disclosure routed to `MoriR16.Lesson` and `MoriR16`.
