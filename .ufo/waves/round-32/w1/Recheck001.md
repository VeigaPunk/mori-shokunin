# Recheck001 — S001 (C1, round 32 attempt 2)

Seat: MoriR32A2.Recheck001. Scope: one population id, S001. Verdict: **current**.
No tools installed or updated this seat (nothing needed; curl/python3/git already present).

## 1. Fetch

| field | value |
|---|---|
| id | S001 |
| population url | `https://docs.kernel.org/accounting/psi.html` |
| accessed (UTC, at fetch) | `2026-10-23T01:31:22Z` |
| HTTP | `200`, `final=https://docs.kernel.org/accounting/psi.html` (no redirect, no bot challenge) |
| tries | 1 of 3 (exit=0) |
| byte size | 19726 |
| sha256 | `f752c8d5447760a315048037eb8f53007f8e4862d58617264f587cccd8798258` |
| scratch copy (bytes unchanged) | `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck001/S001.src` |
| normalised text (seat-check) | `/fast/scratch/hyaku/mori-r32/MoriR32A2.Recheck001/S001.text` (7943 bytes) |

Command used:
`curl -sSL --fail -m 60 https://docs.kernel.org/accounting/psi.html -o S001.src -w 'HTTP %{http_code} final=%{url_effective} size=%{size_download}\n'`
→ `HTTP 200 final=https://docs.kernel.org/accounting/psi.html size=19726`, `sha256sum S001.src` → the digest above.

Page metadata observed in the fetched bytes: `Date: April, 2018`, `Author: Johannes Weiner`, rendered against `The Linux Kernel 7.3.0` docs build, `Powered by Sphinx 5.3.0 & Alabaster 0.7.16`. The `April, 2018` field matches the population anchor `kernel documentation date 2018-04`.

## 2. Ready-to-paste row

```markdown
| S001 | https://docs.kernel.org/accounting/psi.html | 2026-10-23T01:31:22Z | f752c8d5447760a315048037eb8f53007f8e4862d58617264f587cccd8798258 | "The ratios (in %) are tracked as recent trends over ten, sixty, and three hundred second windows"; "The total absolute stall time (in us) is tracked and exported as well"; "The trigger will de-register when the file descriptor used to define the trigger is closed" | current |
```

## 3. Quote → teaches-cell mapping

Teaches cell: *"Keep avg10 trends distinct from absolute stall microseconds; PSI trigger lifetime follows its file descriptor."*

1. `The ratios (in %) are tracked as recent trends over ten, sixty, and three hundred second windows`
   Bears on the first clause: the `avg10`/`avg60`/`avg300` fields are **percent ratios over 10/60/300 s windows** — i.e. trend indicators, not amounts. Supports keeping `avg10` reading as a trend signal.
2. `The total absolute stall time (in us) is tracked and exported as well`
   Bears on the same clause, from the other side: the `total=` field is **absolute stall time in microseconds**, exported alongside the windowed ratios. Together with quote 1 this is exactly the "distinct" claim — one field is a windowed ratio, the other an absolute µs count.
3. `The trigger will de-register when the file descriptor used to define the trigger is closed`
   Bears on the second clause directly: trigger lifetime is bound to the fd; closing it removes the trigger.

Row-level topic words shared with teaches/anchor/scope (seat-check): `absolute`, `descriptor`, `stall`, `trends`, `trigger`.

## 4. seat-check output

```
$ timeout 300 python3 .ufo/waves/round-32/seat-check.py row S001 S001.src '"The ratios (in %) are tracked as recent trends over ten, sixty, and three hundred second windows"; "The total absolute stall time (in us) is tracked and exported as well"; "The trigger will de-register when the file descriptor used to define the trigger is closed"'
sha256=f752c8d5447760a315048037eb8f53007f8e4862d58617264f587cccd8798258
quotes=3 words=[17, 13, 15] in_copy=[True, True, True]
shared_tokens=['absolute', 'descriptor', 'stall', 'trends', 'trigger'] topic_ok=True
live_quotes_ok=True
ROW_CHECK=pass (judge R4 and R5 not checked here)
exit=0
```

`live_quotes_ok=True` means the counter's own fetch of the live URL still contains all three quotes, so the row is not resting on my saved copy alone.

## 5. Drift check — none found

Every element of the teaches/scope cells is still stated by the live page:

- Format line (`Pressure interface`): `some avg10=0.00 avg60=0.00 avg300=0.00 total=0` / `full avg10=0.00 ... total=0`, and the `some`/`full` definitions — normalised text @2703–2960.
- Trend vs absolute distinction — @3655: "The ratios (in %) are tracked as recent trends over ten, sixty, and three hundred second windows ... The total absolute stall time (in us) is tracked and exported as well, to allow detection of latency spikes".
- Thresholds (`Monitoring for pressure thresholds`) — @4018–5330: poll()/select()/epoll(), `<some|full> <stall amount in us> <time window in us>`, one `open()` per trigger, `EBUSY` on rewrite.
- Trigger lifetime — @6330: "The trigger will de-register when the file descriptor used to define the trigger is closed."
- Per-cgroup files (`Cgroup2 interface`) — @7360: each cgroup subdirectory contains `cpu.pressure`, `memory.pressure`, `io.pressure`, same format as `/proc/pressure/`.

No correction paragraph is drafted because the verdict is `current`. One non-drift observation for the integration owner: the docs build banner now reads `The Linux Kernel 7.3.0` and the renderer is `Sphinx 5.3.0`, where the anchor only records the document date `2018-04`; the document body text is unchanged, so the anchor's `2018-04` date still holds and no cell needs editing. [INFERENCE] The anchor's cited line numbers (74-77, 104-119) refer to a local copy this seat was not given, so they were not re-verified here; they are anchor provenance, not part of the teaches check.

## 6. Leftover unknowns

- None affecting the verdict. Line-number anchors not re-verified (no local copy in scope).
- No background processes left running; every command was wrapped in `timeout`, and no git/jj write was performed in the lane.
