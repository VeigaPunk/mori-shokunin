# Lab: digest stability of the six unpinned SOURCES rows (round 96, w1, seat DigestLab)

Hypothesis H, per row: the live URL's bytes are identical across two fetches at least 60 s apart, AND at least one fetch hashes to the row's recorded digest.
Falsification: a URL whose two fetches differ (falsified-unstable), or whose fetches never hash to the recorded digest (falsified-no-match), falsifies H for that row.
Unreachable (no HTTP 200 body obtained) is NOT falsification of H; it is recorded as unreachable and leaves H untested.

## Method

- Rows and recorded digests: `corpus/SOURCES.md` (S125, S612, S615, S616, S622, S623) and the unpinned list from
  `python3 tools/mori-source-digest.py corpus/SOURCES.md corpus/evidence`, which printed
  `DIGEST_CHECK rows=124 ok=86 mismatch=0 superseded=1 prefix_only=31 unpinned=6` and listed exactly these six as `unpinned`.
- Fetch: `curl -sSL --max-time 90 -o <file> -w '%{http_code} %{size_download} %{url_effective} %{num_redirects}' <url>`, curl 8.23.0 (libcurl 8.23.0), default curl User-Agent, no custom headers.
- Two fetches per URL. Fetch 1 started at 12:20:55 UTC (ms resolution below); fetch 2 started 60.5 s later, at 12:21:55 UTC. Each URL ran in its own thread so no URL's second fetch was early.
- Bytes were saved under `$HYAKU_SCRATCH/mori-r96/DigestLab` (default `/fast/scratch/hyaku`), hashed with sha256, and the scratch dir was removed at exit. Raw bytes are not retained; the sha256 and byte counts below are the receipt.
- All times UTC, HH:MM:SS.mmm.

## Per-row verdicts

| row | URL | stable across fetches | any fetch hashes to recorded | verdict |
|---|---|---|---|---|
| S125 | https://raw.githubusercontent.com/VeigaPunk/tsukuroi-shokunin/157ee255/corpus/knowledge/memory-pressure-r25.md | yes | no | **falsified-no-match** |
| S612 | https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html | yes | yes (both) | **holds** |
| S615 | https://docs.python.org/3/library/ast.html | yes | no | **falsified-no-match** |
| S616 | https://docs.python.org/3/library/tokenize.html | yes | no | **falsified-no-match** |
| S622 | https://git-scm.com/docs/git-log | yes | yes (both) | **holds** |
| S623 | https://docs.python.org/3/using/cmdline.html | yes | no | **falsified-no-match** |

No row is falsified-unstable. No row is unreachable: all twelve fetches returned HTTP 200, 0 redirects, curl exit 0, no stderr.

## Raw table

| row | pass | start UTC | end UTC | HTTP | bytes | sha256 | equals recorded digest |
|---|---|---|---|---|---|---|---|
| S125 | 1 | 12:20:55.426 | 12:20:55.820 | 200 | 27828 | ecafdcdd1cc3417f5da40bf8dc9d46925e39550ec1be5baad0949e2458bdcd25 | no |
| S125 | 2 | 12:21:55.926 | 12:21:55.947 | 200 | 27828 | ecafdcdd1cc3417f5da40bf8dc9d46925e39550ec1be5baad0949e2458bdcd25 | no |
| S612 | 1 | 12:20:55.426 | 12:20:56.633 | 200 | 357953 | 0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd | yes |
| S612 | 2 | 12:21:55.926 | 12:21:56.858 | 200 | 357953 | 0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd | yes |
| S615 | 1 | 12:20:55.426 | 12:20:55.706 | 200 | 362493 | 5e531ef083fe5255fe45b6148bf07eec5d595bf8d9791537aa307242832ab696 | no |
| S615 | 2 | 12:21:55.926 | 12:21:55.980 | 200 | 362493 | 5e531ef083fe5255fe45b6148bf07eec5d595bf8d9791537aa307242832ab696 | no |
| S616 | 1 | 12:20:55.427 | 12:20:55.601 | 200 | 53982 | 91bea7a659ed4cf3ea66d9552480c3f2c4cb02066219c527b2c56f0594106758 | no |
| S616 | 2 | 12:21:55.927 | 12:21:55.956 | 200 | 53982 | 91bea7a659ed4cf3ea66d9552480c3f2c4cb02066219c527b2c56f0594106758 | no |
| S622 | 1 | 12:20:55.427 | 12:20:55.488 | 200 | 375834 | f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b | yes |
| S622 | 2 | 12:21:55.928 | 12:21:55.993 | 200 | 375834 | f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b | yes |
| S623 | 1 | 12:20:55.427 | 12:20:55.565 | 200 | 171073 | f0a033694b4368dad6f54616e94d7f13452a59ce28cc0b29d9bb91ef85a53cdf | no |
| S623 | 2 | 12:21:55.927 | 12:21:55.966 | 200 | 171073 | f0a033694b4368dad6f54616e94d7f13452a59ce28cc0b29d9bb91ef85a53cdf | no |

Recorded digests (from the digest tool / SOURCES.md): S125 `e60f1bbc1feb8f251c8b276f70342da5385d07b9ad747305e1f016e0df447136`; S612 `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd`; S615 `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b8f1a60ad1a6f0`; S616 `6842ed0f53882c5a4d7a852ff969842f62aba92f918e2192db0df6ed23c3cb72`; S622 `f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b`; S623 `90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0`.

Pass-2 minus pass-1 start: 60.500 s for S125, S612, S615; 60.500 s for S616 and S623; 60.501 s for S622. Every URL meets the ≥ 60 s bound.

## Observations (measured, not interpreted beyond the bytes)

- S615: the registry also holds S619, same URL, with digest `7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5` (correction of record C-1). The two recorded digests for one URL differ after 20 hex characters. Live bytes match neither.
- S125: the live file's first line reads `source: Round-25 frozen capture ` + "`.ufo/waves/round-25/capture/capture.txt` (sha256 `e60f1bbc1feb8f251c8b276f70342da5385d0…`". The recorded digest therefore names a different artifact (the capture file), not the served bytes of `memory-pressure-r25.md`. Inference from that header; the capture file was not opened.
- S615, S616, S623: the live titles read "Python 3.15.2 documentation", the same label the rows cite for their pinned copies. The version label is not the cause of the byte difference. The cause was not measured.

## One sentence on the C2 pin route

H holds only for S612 and S622, so only those two rows can be pinned under the frozen rule (live bytes hash to the recorded digest), and S125, S615, S616 and S623 stay unpinned because their live bytes never hash to the recorded digests and the contract forbids replacing a recorded digest, so C2's unpinned=0 cannot be reached by live fetches for those four rows.

## Unrun checks (named)

- Re-running `tools/mori-source-digest.py` after any pin: unrun (no copy was placed under corpus/evidence; out of this seat's write scope).
- Byte-diff of the live Python docs against the round-90 pinned copy (S619) and the S615/S616/S623 pinned copies: unrun.
- Hashing the sibling-repo file `tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md` in the local sibling checkout: unrun (read-only probe not in the seat's claim).
- Fetches with a second User-Agent or after more than two fetches or over a longer interval: unrun.
- Root-causing the Python-docs byte drift (build, sidebar, footer or capture method): unrun.
- Whether the 60 s spacing is sufficient to detect hourly or daily page rebuilds: unrun; H as tested covers only a 60 s window.
