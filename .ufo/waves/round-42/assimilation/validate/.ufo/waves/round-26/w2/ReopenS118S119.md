# Re-open S118 and S119 — wave 2, seat ReopenS118S119 (2026-10-22)

Lane tip under attack: 16935e24c93fa7e7567413d7ec091339a5df1474. All registry facts below were read
from that revision with read-only `git show`; the working tree was never trusted. Files were fetched
by ordinary means only: `curl -fsSL` from the public raw URLs, hashed with `sha256sum`, sized with
`wc -c`. Tag dereference used the public GitHub API (no browser, no auth, no challenge bypass).
No tools were installed or upgraded (system curl/git/awk sufficed).

Scratch (fetched bytes, hashes): `/fast/scratch/hyaku/mori-r26/ReopenS118S119/`.

## Verdicts

| Row | Verdict |
|---|---|
| S118 | holds (one minor observation, see below) |
| S119 | holds |

## S118 — earlyoom kill.c and msg.c at v1.9.0 (corpus/SOURCES.md:124 at 16935e24)

Registry columns: kind `code`, tier `A`, status `mined`, opened `2026-10-22`, recheck `on-release`
— match the header semantics at corpus/SOURCES.md:5. PASS.

Fetch and hash comparison (row claims vs. my fetch, 2026-10-22):

| File | Row claim | Fetched | Result |
|---|---|---|---|
| kill.c | 21,169 B sha256 b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3 | 21,169 B, same sha256 | match |
| msg.c | 6,864 B sha256 a771c91529053341c290ede2a7df1d9fdf16e07fb9584db8a64604a45dea5197 | 6,864 B, same sha256 | match |

Tag claim: row says tag `v1.9.0` = commit `202d4db0d308ca6478f68de68b46cae34896ddaf`. Verified via
`GET /repos/rfjakob/earlyoom/git/ref/tags/v1.9.0` → annotated tag `66d78843fd675859a09a52d3f17b1c408a827a34`,
whose object is `202d4db0d308ca6478f68de68b46cae34896ddaf`, type `commit`. PASS.

Anchor line numbers, each read from the fetched bytes:

- kill.c:272 `warn("dryrun, not actually sending any signal\n");` — dryrun text. PASS
- kill.c:282 `warn("killing whole process group %d (-g flag is active)\n", res);` — process-group. PASS
- kill.c:318 `warn("escalating to SIGKILL after %.3f seconds\n", secs);` — escalation. PASS
- kill.c:329 `warn("process %d exited after %.3f seconds\n", pid, secs);` — post-kill outcome. PASS
- kill.c:338 `warn("process %d did not exit\n", pid);` — kill-failure text. PASS
- kill.c:609 `warn("Could not find a process to kill. Sleeping 1 second.\n");` — victim-selection. PASS
- kill.c:617-627 sig-name selection ending in the action literal at :627 `warn("sending %s to process %d uid %d \"%s\": oom_score %d, oom_score_adj %d, VmRSS %lld MiB, cmdline \"%s\"\n",` — supports the teaches claim (format string naming uid, process, cmdline). PASS
- kill.c:654 `warn("kill failed: %s\n", strerror(saved_errno));` — kill-failure. PASS
- msg.c:14 `static int use_syslog = 0;` — PASS
- msg.c:66-73 `logger()` branches `vsyslog` (syslog) vs `color_log(f, ...)` (handed stream). PASS
- msg.c:75-82 `earlyoom_syslog_init()` with `openlog("earlyoom", LOG_PID | LOG_NDELAY, LOG_DAEMON)`. PASS
- msg.c:99-107 `warn()` calls `logger(LOG_WARNING, stderr, yellow, fmt, vl)` — supports "warn() writes to stderr unless --syslog". PASS

Lesson Gate quote for S118 (corpus/lessons/round-26.md:71): `:318 "escalating to SIGKILL after %.3f seconds\n"` —
verbatim substring of kill.c:318 as fetched (the C literal, backslash-n included), located at :318,
6 words (≤25). PASS. Gate header pin (round-26.md:61-62) matches the row's tag claim. PASS.

used-by: `corpus/knowledge/userspace-oom-killers-r26.md` — at the rev its `source:` line (line 1)
names S118 exactly once (`grep -o 'S118' | wc -l` = 1). PASS.

Observation (minor, not a defect): the anchor list ends with a bare `msg.h:10`, but msg.h is not one
of S118's two URLs (kill.c, msg.c) and `PRIPCT` (msg.h:10, `#define PRIPCT "%5.2lf%%"`) appears zero
times in kill.c or msg.c, so the entry attests nothing in this row's own scope. The line number itself
is correct, and the bytes it points at are pinned elsewhere: S119's row records the identical msg.h
sha256 `e3660498…de56c`, and the wave-1 seat's Gate block hashes msg.h at 1,027 B
(.ufo/waves/round-26/w1/SrcEarlyoomKillC.md:74, whose ready-to-paste row at :89 already carried the
`msg.h:10` entry). Cross-file anchors are existing registry practice — S117, admitted this same round,
line-anchors `README.md:283` and `main.c:161,:414,:416` although its URL is the API endpoint
(corpus/SOURCES.md anchor column of S117 at the rev) — and no registry rule restricts anchors to the
row's own URLs. Recommendation (optional, integrator's call): drop `msg.h:10` from S118 or label it
("PRIPCT format", as S119 does) so a reader of S118 alone knows what it attests. No hash, quote,
tier, status or used-by fact is affected.

## S119 — earlyoom main.c and msg.h at tag v1.9.0 (corpus/SOURCES.md:125 at 16935e24)

Registry columns: kind `code`, tier `A`, status `mined`, opened `2026-10-22`, recheck `on-release`. PASS.

Fetch and hash comparison (row records sha256 only, no byte sizes — the registry requires neither;
pre-2026-10-21 rows record no hashes at all):

| File | Row sha256 | Fetched sha256 | Result |
|---|---|---|---|
| main.c | 08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4 | same | match |
| msg.h | e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c | same | match |

(For reference my fetch sizes: main.c 21,053 B, msg.h 1,027 B.) Tag claim: same commit as S118, verified
above. PASS.

Anchor line numbers, each read from the fetched bytes:

- main.c:161 `fprintf(stderr, "earlyoom " VERSION "\n");` — version line. PASS
- main.c:295 `warn("dryrun mode enabled, will not kill anything\n");` — dry-run flag text. PASS
- main.c:346-372 `-M` merged with `-m` and `-S` with `-s`, lower-value `min()` in both cases — "-M/-S conversion and lower-value merge". PASS
- main.c:414-417 the two `fprintf(stderr, ... PRIPCT ...)` threshold lines — "threshold prints". PASS
- main.c:498-504 `lowmem_sig()` returns SIGKILL / SIGTERM / 0 by the both-below rule — "act rule". PASS
- main.c:507-552 `poll_loop()` body — "poll loop". PASS
- main.c:519 and :523 `warn("low memory! at or below SIGKILL/SIGTERM limits: mem " PRIPCT ", swap " PRIPCT "\n", ...)` — low-memory warnings. PASS
- msg.h:10 `#define PRIPCT "%5.2lf%%"` — supports the teaches claim "rounded to two decimals and space-padded, so 5.00 renders as a space then 5.00" (width 5, precision 2). PASS

Lesson Gate quote for S119 (corpus/lessons/round-26.md:72): `:414 "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT ",\n"` —
verbatim substring of fetched main.c:414 (`fprintf(stderr, "sending SIGTERM when mem avail <= " PRIPCT " and swap free <= " PRIPCT ",\n",`),
located at :414, 13 words (≤25). PASS.

used-by: `corpus/knowledge/userspace-oom-killers-r26.md` names S119 exactly once at the rev
(`grep -o 'S119' | wc -l` = 1). PASS.

## Residual risk and verification gaps

- Single fetch per URL on 2026-10-22, the same day the rows were opened; upstream drift between the
  wave-1 fetch and mine is excluded by sha256 equality with the rows and with the w1 Gate blocks.
- S119 byte sizes are not recorded in the registry row, so no size comparison was possible for it
  (sha256 equality is the binding check and it passed); sizes above are my own fetch measurements.
- I verified anchors and quoted lines, not the full byte-level reading of every function body; the
  teaches columns' interpretive sentences were spot-checked only where an anchor line carries the
  literal (all such literals matched).
- The S118 `msg.h:10` observation is judged against registry practice as found at the rev; no written
  anchor-scope rule exists in corpus/SOURCES.md to violate, so I cannot upgrade it beyond "minor".
