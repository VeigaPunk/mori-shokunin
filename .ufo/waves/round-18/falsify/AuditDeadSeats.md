# Wave-1 dead-seat cross-check

## Evidence and method

- Record: `.ufo/waves/round-18/evidence/wave1-dead-seats.json:2-3,5-22`. SHA-256: `0c7c2da40bfd69ff30a028b842d4683f313d3f0038e6aa29a615e64a8dc88f5f`.
- The record assigns all 15 listed seats the same aggregate error class: **provider capacity / rate limit**. No error text is reproduced here.
- Read the `.ufo/waves/round-18/build/` listing and checked targeted report-name globs for each seat below; every targeted glob returned no files. No matching seat report was present.
- Attempted only the final-line selector (`:-1`) for each `history://MoriR18Recovery.<Seat>` pointer. The returned tail was not an error line, so the last error line could not be compared. No wider transcript range was requested. Consequently each comparison is **unverified**, not a mismatch.

| Seat | Report present under `build/`? | Error class in record | Record text matches transcript? |
|---|---:|---|---|
| `SweepR17Build1` | No | Provider capacity / rate limit | Unverified — last error line unavailable |
| `AdjSeatNaming` | No | Provider capacity / rate limit | Unverified — last error line unavailable |
| `AdjSeatBreachDetect` | No | Provider capacity / rate limit | Unverified — last error line unavailable |
| `AdjSeatLiveEvidence` | No | Provider capacity / rate limit | Unverified — last error line unavailable |
| `SweepR17Falsify3` | No | Provider capacity / rate limit | Unverified — last error line unavailable |
| `SweepR15Md1` | No | Provider capacity / rate limit | Unverified — last error line unavailable |
| `AdjRetryRecoveryShape` | No | Provider capacity / rate limit | Unverified — last error line unavailable |
| `AdjDeadSeatCrossCheck` | No | Provider capacity / rate limit | Unverified — last error line unavailable |
| `ScoutAttemptReceipts` | No | Provider capacity / rate limit | Unverified — last error line unavailable |
| `SweepR1314Md` | No | Provider capacity / rate limit | Unverified — last error line unavailable |
| `SweepR17Falsify1` | No | Provider capacity / rate limit | Unverified — last error line unavailable |
| `SweepR16Md1` | No | Provider capacity / rate limit | Unverified — last error line unavailable |
| `AdjOmpRetryDocs` | No | Provider capacity / rate limit | Unverified — last error line unavailable |
| `AdjTranscriptTailBounds` | No | Provider capacity / rate limit | Unverified — last error line unavailable |
| `AdjWave1SpecDispatch` | No | Provider capacity / rate limit | Unverified — last error line unavailable |

## Command record

- `sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-18/evidence/wave1-dead-seats.json` — exit 0.
- Report-presence checks were read-only `read`/`glob` operations; each of the 15 targeted globs returned “No files found matching pattern.” No VCS operation or tool installation was performed.
