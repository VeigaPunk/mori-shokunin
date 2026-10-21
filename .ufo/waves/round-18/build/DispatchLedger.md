# DispatchLedger — Round 18 C3

## Files changed

- Added `tools/mori-dispatch-ledger.py` in the assigned `DispatchLedger` clone.
- Added this report at `.ufo/waves/round-18/build/DispatchLedger.md`.
- No tooling was installed or updated.

## Behavior implemented

The tool reads committed blobs at the requested revision through read-only Git object operations. `bind` selects the validator run object, computes the frozen canonical UTF-8 payload identity (`json.dumps({"context", "tasks"}, ensure_ascii=False, sort_keys=True, separators=(',', ':'))`), and emits only its SHA-256, byte length, and task count. The helper is at `tools/mori-dispatch-ledger.py:120-180`.

`verify` checks each non-legacy row's digest, byte count, and task count against the committed dispatch payload; missing-digest legacy rows are individually unbound. It reports per-row reasons, attempt-sequence/timestamp/start-state findings, totals, and exit status (`0` clean, `1` findings, `2` unavailable/invalid input). The checks and output are at `tools/mori-dispatch-ledger.py:200-338`. The sandbox selftest uses the caller's `TMPDIR`, refuses `/tmp` and `/var/tmp`, and creates disposable fixture repositories for 11 CLI arms (`tools/mori-dispatch-ledger.py:413-509`).

## Required evidence

Commands were run from `/home/vgpnk/Projects/shokunin`; all target reads used revision `29b0dc7`.

1. `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/DispatchLedger/tools/mori-dispatch-ledger.py verify --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev 29b0dc7 --ledger .ufo/waves/round-17/wave1-dispatch-attempts.json` — exit **1**; totals: 5 rows, 0 bound, **5 unbound**. Each row is `LEGACY_ROW_UNBOUND`; ledger findings also include `ATTEMPTS_NONCONTIGUOUS` and `STARTED_MISSING`.
2. `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/DispatchLedger/tools/mori-dispatch-ledger.py verify --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev 29b0dc7 --ledger .ufo/waves/round-17/wave2-dispatch-attempts.json` — exit **1**; totals: 4 rows, 0 bound, **4 unbound**. Each row is `LEGACY_ROW_UNBOUND`; ledger findings also include `ATTEMPTS_NONCONTIGUOUS` and `STARTED_MISSING`.
3. `python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/DispatchLedger/tools/mori-dispatch-ledger.py bind --repo /home/vgpnk/Projects/shokunin/mori-shokunin --rev 29b0dc7 --dispatch .ufo/waves/round-17/wave1-dispatch.json` — exit **0**; `payload_sha256=cd5c9a64cf1a76634b61272479a6141fcaf71205e93dcc18cf6a0d979f506a57`, `payload_bytes=75629`, `tasks_count=70`.
4. `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/DispatchLedger/.scratch python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/DispatchLedger/tools/mori-dispatch-ledger.py --selftest` — exit **0**; `SELFTEST mori-dispatch-ledger PASS 11/11`. Arms: clean ledger, tampered payload byte, wrong digest, missing started, started not last, two started, non-contiguous attempt, decreasing time, started-ID mismatch, legacy row, and missing dispatch path (exit 2).
5. `sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-18/DispatchLedger/tools/mori-dispatch-ledger.py` — **4d8c7bf55b142569750f909ab3e9f7ef261d6d99672c55413027746c02c427b4**.

The command evidence corresponds to C3 in `.ufo/waves/round-18/contract.md:39-53,66-69` and the frozen identity/verification rule in `.ufo/waves/round-18/frozen/c3-ledger-format.json:4-21`.

## Risks and blockers

No blocker observed. As stated by the frozen known limit (`.ufo/waves/round-18/frozen/c3-ledger-format.json:21`), binding proves equality with the committed payload identity; it cannot independently prove which exact bytes the external task tool received. No builds, linters, or other tests were run.
