# DigestLab (round 96, w1) — digest stability of the six unpinned SOURCES rows

Evidence file: `.ufo/waves/round-96/w1/lab/Lab-digest-stability.md`

## Verdicts (hypothesis H: two fetches ≥60 s apart identical AND one hashes to recorded digest)

- S612: **holds**. Both fetches HTTP 200, 357953 bytes, sha256 `0889867a53fe12508a71e8739ec23ecdddc95e6f67697c98e26acc8ff0ec1acd` = recorded.
- S622: **holds**. Both fetches HTTP 200, 375834 bytes, sha256 `f206647fba42b627f46d29993490fbb585adedaa5d27b9ed575f50ef9002f69b` = recorded.
- S125: **falsified-no-match**. Stable (27828 bytes, sha256 `ecafdcdd1cc3417f5da40bf8dc9d46925e39550ec1be5baad0949e2458bdcd25` both); recorded `e60f1bbc…447136` never matched.
- S615: **falsified-no-match**. Stable (362493 bytes, sha256 `5e531ef0…2ab696` both); recorded `7891c588…1a6f0` never matched (S619's correction digest `7891c588…0f83b9a8a42f5` also not matched).
- S616: **falsified-no-match**. Stable (53982 bytes, sha256 `91bea7a6…106758` both); recorded `6842ed0f…cb72` never matched.
- S623: **falsified-no-match**. Stable (171073 bytes, sha256 `f0a03369…3cdf` both); recorded `90ac3b25…1ad0` never matched.
- No row is falsified-unstable. No row is unreachable: all twelve fetches returned HTTP 200.

## Command outputs supporting the verdicts

- Digest tool (before): `DIGEST_CHECK rows=124 ok=86 mismatch=0 superseded=1 prefix_only=31 unpinned=6`; unpinned S125 S612 S615 S616 S622 S623.
- Fetch pass 1 / pass 2 start times (UTC): 12:20:55.4xx and 12:21:55.9xx for every URL (gap 60.5 s).
- Per-fetch `curl -sSL -w '%{http_code} %{size_download} …'`: every line `200 <bytes> <url> 0`, curl exit 0, empty stderr.
- S125 live first line: "source: Round-25 frozen capture `.ufo/waves/round-25/capture/capture.txt` (sha256 `e60f1bbc…`" — the recorded digest names a different artifact (inference; capture not opened).
- Live titles for S615/S616/S623: "Python 3.15.2 documentation" — same label as the pinned copies, so version label is not the cause of the byte drift (cause not measured).

## What H means for the C2 pin route

Only S612 and S622 can be pinned under the frozen rule; S125, S615, S616 and S623 cannot be pinned from live bytes without replacing a recorded digest, which the contract forbids, so C2's unpinned=0 is not reachable from live fetches for those four rows.

## Not established

- Unreachable: none observed. Falsification verdicts above are about digest mismatch, not fetch failure.
- Scope of H: a 60 s window only; hourly or daily page rebuilds are not tested.

## Unrun checks

- Digest tool re-run after any pin (no pins placed; outside write scope).
- Byte-diff of live Python docs against S619 and the S615/S616/S623 pinned copies.
- Hash of the sibling-repo file in the local tsukuroi checkout (S125).
- Alternate User-Agent, more than two fetches, longer intervals, drift root cause.

## Installs and writes

- No tool installed or upgraded (curl 8.23.0 already present).
- Wrote only `.ufo/waves/round-96/w1/lab/Lab-digest-stability.md` and this report. Scratch dir `$HYAKU_SCRATCH/mori-r96/DigestLab` (raw bytes) removed after hashing.
