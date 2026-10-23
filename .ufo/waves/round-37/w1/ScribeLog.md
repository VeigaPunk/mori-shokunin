# Round-37 LOG receipt audit

**Target:** `LOG.md` lines 2139–2167. **Axes:** evidence fidelity; gate/result fidelity; provenance. I compared the logged measurements with the receipts named in those lines. I did not rerun counters, census validation, or selftests; outcomes below are transcribed from the existing receipts.

| Command / invocation as recorded | Logged value / observed output | Cited receipt | Present? |
|---|---|---|---|
| Freeze generator command is not shown; hash artifact only | Counter blob prefixes `7518fef8` / `6213cf9a`; SHA-256 prefixes `86699627` / `71c72929` | `evidence/freeze-r37.txt` lines 4–5, 13–14 | Yes |
| `count-c2.py bf0df77 --tool fixtures/memo-n1.py --seed 11` | `C2=met`, exit 0; seed 11 | `evidence/c1-before-memo.txt` lines 8–10 | Yes |
| `count-c2.py bf0df77 --tool fixtures/summary-only.py --seed 12` | `C2=met`, exit 0; seed 12 | `evidence/c1-before-summary.txt` lines 8–10 | Yes |
| `count-c1.py e57c58b5` | Blind `24/24`; real and challenge pass; memoizer, constant, and summary-only negatives rejected; `C1=met`, exit 0; seed `13985344346805549517` | `evidence/c1-after.txt` lines 3–16 | Yes |
| `count-c2.py 842a320` | Logged selftest, knowledge, capability, README, and live failures; `C2=unmet`, exit 1 | `evidence/c2-before.txt` lines 3–11 | Yes |
| `count-c2.py e57c58b5` | Eight checks pass; `C2=met`, exit 0 | `evidence/c2-after.txt` lines 2–11 (eight named checks, all `PASS`) | Yes |
| Live-sweep invocation not recorded in LOG or receipt | `rows=220 fresh=49 drifted=9 unavailable=0 no-copy=162`, exit 1 | `evidence/drift-live-r37.txt` lines 221–222 | Output yes; command absent |
| `count-c2.py e57c58b5` (knowledge check) | Five row IDs `S221–S225` listed | `evidence/c2-after.txt` line 6 | Yes (IDs listed; does not attest that no existing registry row changed) |
| `sources-census.sh validate mori` | Start and end validation exit 0; only W04 duplicate-URL warnings | `evidence/census-start.txt` lines 1–17; `evidence/census-end.txt` lines 1–17 | Yes |
| `sources-census.sh validate mori` | Census total `225 rows` | Same census receipts show W04 warnings, `mori ok`, and `EXIT=0`, but no row total | **No** |
| r17 selftest invocation not recorded in LOG or receipt | Selftest exit 0 | `evidence/r17-jj-selftest-r37.txt` lines 1–2 | Output yes; command absent |
| Pre-fix command not recorded; LOG points to a round-36 collateral note | Pre-fix `9/204 red` | `evidence/r17-jj-selftest-r37.txt` lines 1–2 report the post-fix selftest and `EXIT=0`; neither contains `9/204` | **No** |
| Size-measurement command not recorded | S225 copy size `1.9 MiB` | No evidence receipt cited for this value at `LOG.md` line 2165 (the cited source is the lesson) | **No** |
| Score-measurement command not recorded | Held scores `coverage 6, operability 7, depth 5, calibration 5, freshness 5, adjacency 6` (including the C1/C2 score 5 claims) | No receipt for these scores is cited; the C1/C2 receipts report gate outcomes, not scores | **No** |

## Findings

- `LOG.md:2159–2160` reports `225 rows`, but neither cited census receipt prints that total.
- `LOG.md:2161–2162` reports the historical `9/204` result alongside the r17 receipt; the receipt contains only the post-fix selftest list and exit 0.
- `LOG.md:2165` reports `1.9 MiB` without a cited evidence receipt.
- `LOG.md:2167` reports six held scores without a cited receipt supporting those values. The C1/C2 measurement receipts establish gate results, not score values.

## Gates, surfaces, limits

- **Behavior / gates:** all receipt-backed counter and live-sweep result values checked above match their receipts. The census receipts support successful validation and the warning class, but not the logged row total.
- **Touched surfaces:** read `LOG.md`, the cited round-37 evidence files, and the contract for scope; created this report only. No lane files were edited. No tools were installed.
- **Out of scope:** rerunning measurements, adjudicating whether the scored values are substantively correct, and checking unrelated round-37 claims not expressed as measured values.
- **Provenance:** source observations are the existing local receipts named above; no new execution evidence was generated.
- **Artifact:** `.ufo/waves/round-37/w1/ScribeLog.md`.

VERDICT: FAIL — unsupported/missing receipt values at `LOG.md:2159–2160`, `LOG.md:2161–2162`, `LOG.md:2165`, and `LOG.md:2167`.
