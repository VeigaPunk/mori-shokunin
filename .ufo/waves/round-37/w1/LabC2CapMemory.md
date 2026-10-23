# LabC2CapMemory — what the 4 MiB cap costs, and what it actually bounds at the client

**Item attacked.** The C2 `huge_cap` arm and the bounded-read policy it exercises:
`tools/mori-source-drift.py:54` (`FETCH_MAX_BYTES = 4 * 1024 * 1024`) and the read at
`tools/mori-source-drift.py:163-166` (`resp.read(FETCH_MAX_BYTES + 1)`, over-cap → `unavailable`),
plus the fixture bodies the arm serves at `tools/mori-source-drift.py:322` (`/huge` = `cap + 64`)
and `:402-403` (`/big` = exactly `cap`). P-C2 asserts the cap is load-bearing; this item measures
what that policy costs in memory and, precisely, what memory bound it enforces at the client.

Scored tip under test: `e57c58b57c025364e79d130fbdf764d2674d83d6`.
Worktree bytes hash-identical to the rev:

```
$ git hash-object tools/mori-source-drift.py
162ee87b5b0789c6815f967f3db93d277bab38d9
$ git rev-parse e57c58b57c025364e79d130fbdf764d2674d83d6:tools/mori-source-drift.py
162ee87b5b0789c6815f967f3db93d277bab38d9
$ sha256sum tools/mori-source-drift.py
453c5d8e260301df7a99daf62b4c16ea08e4a0b4f9e4f53821cdbce447011552
```

No lane byte was modified or added on disk; every command below is read-only against the lane
(`--selftest` writes only to `tempfile.mkdtemp` roots). Scratch root:
`/fast/scratch/hyaku/mori-r37/LabC2CapMemory/`. No tool was installed or upgraded.

## Measurement harness caveat (affects how the numbers must be taken)

`/usr/bin/time` does not exist on this host (`ls: cannot access '/usr/bin/time'`). A GNU time 1.9
binary is pre-existing at `~/.local/bin/time` (`-rwxr-xr-x 44136 Oct 22 08:19`; `time (GNU Time)
1.9`) and was used as the `-v` harness. It reports the **child's** rusage via `wait4`, which is
what is wanted.

In-process `resource.getrusage(RUSAGE_SELF).ru_maxrss` is **unusable in this environment**: a bare
`python3 -c "import resource;print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"` prints
`3805692` (kB) while the same process reports `VmHWM: 10236 kB` in `/proc/self/status`. The kernel
carries `signal->maxrss` across `execve` (it is reset at `fork`, not at `exec`), so any process
exec'd from this session's shell inherits a stale 3.8 GiB high-water mark. Every number below
therefore comes from GNU time (`wait4` rusage, fork-reset) or from `/proc/<pid>/status: VmHWM`
sampled on the child; the two agree.

## 1. Peak RSS of the cap arm's selftest

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ /home/vgpnk/.local/bin/time -v python3 tools/mori-source-drift.py --selftest
```

12 runs, `Maximum resident set size (kbytes)`:

```
36108  37916  38208
37748  36808  36040
37568  36824  37784
37988  36980  38088
```

(sorted: 36040 36108 36808 36824 36980 37568 37748 37784 37916 37988 38088 38208)

| statistic | value |
|---|---|
| min | 36,040 kB (35.2 MiB) |
| median | 37,658 kB (36.8 MiB) (12 samples: mean of the two middle, 37,568 and 37,748) |
| max | 38,208 kB (37.3 MiB) |
| mean | 37,338 kB (36.5 MiB) |

Wall clock 4.54–4.62 s, exit 0, `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)` on every run.
Independent cross-check by sampling the child's `/proc/<pid>/status` every 5 ms:

```
child_rc 0
child_VmHWM_peak_kb 39060
```

Baselines on the same host, same harness: `python3 -c pass` → `Maximum resident set size` **9,588 kB**;
`python3 -c "import urllib.request, http.server, hashlib, threading"` → **20,868 kB**. So the
selftest's own footprint above the imports baseline is ≈ **17 MiB**, and above a bare interpreter
≈ 27 MiB.

Marginal cost of the two 4 MiB fixture bodies alone (scratch copy `drift-shrunk.py`, identical in
every respect except `routes["/huge"] = (200, b"x" * 64)` and `cap_body = 64`):

```
$ /home/vgpnk/.local/bin/time -v python3 drift-shrunk.py --selftest
	Maximum resident set size (kbytes): 24512
```

→ the 4 MiB bodies cost **≈ 11.3–13.4 MiB of peak RSS** (35.2–37.3 MiB − 23.9 MiB), i.e.
**≈ 2.8–3.3 × cap**, consistent with 8 MiB of resident fixture bytes + a 4 MiB client read buffer
+ socket/`urllib` overhead.
(The shrunk copy fails `row_states`/`summary`/`huge_cap` by construction — that is the point; only
its memory profile is used.)

Allocation accounting over the whole `_selftest()` (clean copy `drift-clean.py`, tracemalloc
started before the call):

```
selftest_rc = 0
tracemalloc_peak_over_whole_selftest = 13127564 bytes (12.519 MiB, 3.13 x cap)
tracemalloc_current_at_end = 8643245 bytes
VmHWM before = 23024 kB, after = 39860 kB (delta 16836 kB)
```

Peak decomposes exactly: `cap+64` (`/huge` route body) + `cap` (`/big` route body) + `cap`
(the at-cap body the arm retains) = 12,582,976 B = **3.00 × cap**, plus 544,588 B of interpreter
and `urllib` objects. The route bodies stay resident for the whole selftest (they sit in
`_Handler.routes` / the local `routes` dict); the over-cap read buffer is *not* retained, because
`fetch` returns `("unavailable", None)` and discards it.

## 2. Body sizes the arm serves

Instrumented copy whose handler records `len(body)` per route (`full-selftest-probe.py`, full run):

```
bytes served per route:
  /big         4194304
  /close       close
  /drifted     176
  /excerpt     384
  /fresh       176
  /gone        10
  /huge        4194368
  /redir       redirect
  /trail       176
largest_body_served_bytes = 4194368 (4.0001 MiB)
VmHWM: 39600 kB
```

| route | bytes served | relation to cap (4,194,304 B) |
|---|---|---|
| `/huge` | **4,194,368** | **cap + 64 (largest body served)** |
| `/big` | 4,194,304 | exactly cap |
| `/excerpt` | 384 | 0.00009 × cap |
| `/fresh`, `/drifted`, `/trail` | 176 each | — |
| `/gone` | 10 | — |
| `/close`, `/redir` | no body (reset; 302) | — |

The `/huge` route is fetched twice per selftest (row S109 in `run()`, then the `huge_cap` arm), both
times with the same result. Registry row S109's *copy* is 100 bytes.

## 3. The memory bound the 4 MiB cap actually enforces at the client

**Fixed-length response (the normal case): at most `FETCH_MAX_BYTES + 1` = 4,194,305 bytes are
materialized per fetch, then the row grades `unavailable`.** Verified against a server that sends
64 MiB (16× cap) at the probe (`client-bound-probe.py`):

```
server_body_bytes            = 67108864 (16.0 x cap)
client_outcome               = unavailable
client_materialised_bytes    = None
client_peak_before_kb        = 24172
client_peak_after_kb         = 31324 (delta 7152 kB = 6.98 MiB)
client_rss_before_kb         = 24172
client_rss_after_kb          = 27984 (delta 3812 kB = 3.72 MiB)
```

and the instrumented read of the fixture's own over-cap body reports
`len(body)=4194305` = cap + 1 exactly, never 4,194,368 and never more.

**Chunked response: the transient peak is ≈ 2 × cap, not 1 × cap.** `http.client.HTTPResponse.read(amt)`
dispatches to `_read_chunked(amt)`, which accumulates chunks in a list and then `b"".join(value)` —
so both the chunk list and the joined bytes are live at once. Measured with a chunked server
(`chunked-bound-probe.py`, 16 MiB, and `chunked64-bound-probe.py`, 64 MiB):

```
chunked_server_bytes      = 16777216 (4.0 x cap)     chunked_server_bytes      = 67108864 (16.0 x cap)
chunked_client_outcome    = unavailable              chunked_client_outcome    = unavailable
chunked_materialised      = None                     chunked_materialised      = None
chunked_peak_delta_kb     = 10428 (10.18 MiB)        chunked_peak_delta_kb     = 10532 (10.29 MiB)
```

with `tracemalloc_peak=8389191` bytes (2 × (cap+1) + 581) on the fetch. The delta is **flat in the
served body size** (16 MiB vs 64 MiB → 10.18 vs 10.29 MiB): still O(cap), but 2× the nominal bound.

**The bound is per-fetch, not cumulative.** A registry of N rows whose bodies are each exactly the
cap (`many-rows-probe.py`):

```
rows=1   peak_before= 27228 kB peak_after= 32944 kB delta=  5716 kB (5.58 MiB)
rows=8   peak_before= 32944 kB peak_after= 36888 kB delta=  3944 kB (3.85 MiB)
rows=32  peak_before= 36888 kB peak_after= 36888 kB delta=     0 kB (0.00 MiB)
```

Peak `VmHWM` plateaus at 36,888 kB and does not grow with row count: `body` is rebound each
iteration of `run()` and released after `classify()`.

**Summary of the enforced bound.** The 4 MiB cap bounds *response-body bytes materialized in the
client per fetch* to cap + 1 = 4,194,305 B (4 MiB + 1), with a 2× transient (8,388,610 B) on the
chunked path, and it makes client memory independent of how much a server streams (64 MiB served →
same ~7–10 MiB client delta). It does **not** bound: the fixture's own server-side route bodies in
the selftest (2.00 × cap resident by construction), the local copy-file read
(`copy = fh.read()` at `tools/mori-source-drift.py:232` is unbounded — a local corpus file, not a
remote body), response headers, or kernel socket buffers.

## 4. Acceptance arithmetic

"FAIL if the arm's own fixture allocates more than the cap allows times a small constant."

| allocation | bytes | × cap |
|---|---|---|
| fixture `/huge` body (cap + 64) | 4,194,368 | 1.00002 |
| fixture `/big` body (cap) | 4,194,304 | 1.00000 |
| **fixture total** | **8,388,672** | **2.00** |
| client read buffer, fixed-length, one at a time | 4,194,305 | 1.00 |
| client chunked transient (measured worst case) | 8,389,191 | 2.00 |
| whole-selftest Python-heap peak (tracemalloc) | 13,127,564 | 3.13 |
| marginal peak RSS of the two 4 MiB bodies | ~11.3–13.4 MiB | ~2.8–3.3 |

Everything is a small constant multiple of the cap and constant in served body size (16 MiB vs
64 MiB chunked served identical cost). No allocation is O(body size) and none is O(row count).
Total process peak 35.2–37.3 MiB includes a 20.9 MiB interpreter+`urllib`/`http.server` baseline
that is not attributable to the arm.

## Risks / retained caveats

- The cap bounds *body* bytes, not process memory: the chunked path's `b"".join` doubles the
  transient to ~8.4 MB. Disclosed, bounded, small — not a defect.
- The over-cap path still materializes cap + 1 bytes before rejecting; that is inherent to the
  `read(cap+1)` sentinel design and is 1 byte over the nominal cap.
- The selftest's resident cost is dominated by its own 2 × cap fixture bodies (8 MiB): with those
  two bodies shrunk to 64 B the same selftest peaks at 24.5 MiB instead of 35.2–37.3 MiB, so
  ~11.3–13.4 MiB of the peak is the arm's own fixture cost.
- `ru_maxrss` from `RUSAGE_SELF` in this session is stale-inherited and must not be used as a
  measurement; `/proc/<pid>/status:VmHWM` or GNU time `wait4` rusage are the trustworthy sources.
- The `--selftest` wall clock is ~4.55 s, dominated by the `/huge`, `/close` and `/big` socket
  interactions; memory does not grow with it.

## Blockers

None. No installs, no pacman, no lane mutation, no remediation.

VERDICT: PASS
