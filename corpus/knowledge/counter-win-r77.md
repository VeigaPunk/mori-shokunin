verified-at: 2026-11-02 (round 77; the S592 command claims below are
line-located against the pinned copy and machine-verified — PASS items=3
with the able-to-fail arm FAIL rc 1 in the same receipt; the counter PATHS
are not doc-located — they are enumerated on THIS host by the documented
`-q` listing, receipted `.ufo/waves/round-77/evidence/counter-enum-r77.txt`
enumeration_matched=4 rc 0 — and the declaration below names which claims
are doc-grounded and which are live-verified)
recheck: 180d
source: S592 (learn.microsoft.com — typeperf, Windows Commands reference;
pinned copy `corpus/evidence/sources-r77/S592.html` sha256
5f2e58ad44160bc35bb52be688812047f09bd5bab81c2959f32682c586ee2bfe, 50980
bytes, opened 2026-11-02; duplicate sweep receipted BEFORE the fetch in
`.ufo/waves/round-77/evidence/source-s592-r77.txt` — no registry row is the
typeperf command-reference page: 0 rows name the URL or the word, and the
nearest rows S573 (wevtutil) and S572 (the exhaustion-event troubleshooter)
are sibling pages, not this one; resolved page `<title>` checked before the
pin per the r75 lesson rule; all three located-line anchors machine-verified
by the r72 anchor-checker — PASS items=3 rc 0, able-to-fail mislocation arm
FAIL rc 1, `.ufo/waves/round-77/evidence/s592-anchor-check-r77.txt`).
Supporting rows the entry reads: S572 (the exhaustion-event semantics —
Event 2004 is commit-limit exhaustion, its K4), S573 (the wevtutil
child-command probe pattern this instrument follows), S574 (the volatility
boundary for one-shot reads).

# Reading the Windows performance-counter surface (round 77): the commit gauge pair and the paging rate

Scope: detection and report only, counts and shapes only. Round 77 fills the
surface class between two landed reads: the r63 event-log probe reads the
host's EXHAUSTION-EVENT history (Event 2004 — a record that exhaustion was
DIAGNOSED in the past), and the r64 probe reads API-side totals
(GlobalMemoryStatusEx: load percent and the paging-file/commit totals in one
struct). The surface between them — the OS performance counters the
exhaustion diagnosis itself reads — was unprobed on this host. This entry
grounds `tools/mori-counter-win.py` (round-77 build): a one-shot, read-only
read of four Memory counters through the documented `typeperf` command. The
commit gauge pair is the same quantity the lane reads on Linux hosts
(`tools/mori-commit-runway.py`, r53: CommitLimit/Committed_AS from
/proc/meminfo) — continued here on the Windows workspace host where the
/proc instruments are absent (PROVINCE Round-62 host note). Claims (K1–K3
ground the command mechanics from S592; K4–K5 ground the read's object from
the held S572 ground; K6–K7 are the one-shot and availability boundaries,
live-verified by the round-77 receipts):

- **K1** — `S592.html:749` — "command writes performance data to the command
  window or to a log file." (13 words; the sentence subject typeperf sits
  inside a strong tag on the same line, so the located contiguous span starts
  at "command"): the probe's transport is the documented command; the probe
  reads the command window (stdout bytes) and never asks for the log-file arm
  (`-o` is not in its argv), so a receipt is a captured read, not a written
  file.
- **K2** — `S592.html:806` — "Specifies the number of samples to collect."
  (7 words; the option row's default, collecting until CTRL+C, is the rest of
  the same cell): the probe's `-sc 2` sample bound is the documented option —
  a bounded read, not an unbounded monitor. Two samples so the OS-side rate
  counter has its collection interval; the parser takes the LAST sample row
  only and every receipt carries `samples=2` so the bound travels with it.
- **K3** — `S592.html:798` — "Display a list of installed counters (no
  instances). To list counters for one object, include the object name."
  (18 words): the `-q` enumeration is the documented way to list installed
  counters, and it is how the probe's four counter paths are grounded — NOT
  from documentation prose. The four paths are live-enumerated on this host
  (receipt: enumeration_matched=4 rc 0) and pinned in the instrument; a
  counter path is a locale-sensitive string, so on a non-English host the
  same read resolves different paths — absence there is a named unavailable,
  never a zero (K7).
- **K4** — the read's object is the commit gauge pair: `\Memory\Committed
  Bytes` and `\Memory\Commit Limit`, plus the in-use share
  (`\Memory\% Committed Bytes In Use`) and the paging-activity rate
  (`\Memory\Pages/sec`). The object is doc-linked through held ground: S572's
  exhaustion event is explicitly "exhaustion of system commit limit (virtual
  memory)" (its K4, `S572.html:768`), so the live pair is the same quantity
  the r63 probe sees only as an event history — the lane's commit-runway
  object (r53, Linux) continued on this host. The PATHS are live-verified
  (the enumeration receipt), the SEMANTICS of the exhaustion link are
  S572's held claim.
- **K5** — the rate is OS-computed, not lane-built: `\Memory\Pages/sec`
  arrives as a per-second figure computed by the counter system over
  typeperf's own collection interval. The lane builds no two-sample
  instrument of its own (FR6 stays open — a lane-made rate stays frontier)
  and a rate sample is not a stall proof: the Linux PSI instruments remain
  the registered pressure gates (FR12 stays open; PROVINCE Round-62 host
  note).
- **K6** — a sample is volatile and one-shot (the S574:846-847 boundary
  carries to the counter surface): consecutive runs are separate counts,
  never a series, a trend or an average beyond the OS's own collection
  interval. The observed live read (`counter-win-live-r77.txt`: AVAILABLE
  surfaces=4 ok=4, the in-use gauge at 75.265670 percent) is one reading, not
  a baseline.
- **K7** — availability is honest at every layer: missing typeperf, nonzero
  child rc, timeout, no PDH-CSV header, zero sample rows (observed once in
  the round-77 exploration: rc 0 with an EMPTY stdout sample set — and the
  sweep caught the CAUSE, which was the exploration's own argv: `-f csv`
  without `-o` redirects the samples into typeperf's DEFAULT log file
  `output.csv` in the working directory; the stray file was found at the lane
  root, receipted, and removed, and the probe never passes `-f`), a missing
  column, or a value token outside the
  dot-decimal grammar (`^[0-9]+(\.[0-9]+)?$` — a thousands-comma token is
  refused, not misparsed) all read `unavailable` with a named reason, never
  zero. The CSV header's machine-name prefix and every sample timestamp are
  redacted by the parser — the selftest proves neither reaches stdout.

Limits (declared): the probe counts and never infers a cause — an exhaustion
gauge reading high is evidence to correlate, never a diagnosis of which
process leaked or why (attribution stays with the event text the probe
deliberately does not read; the r63 redaction boundary carries). The counter
paths are pinned from ONE host's enumeration; another host's localization can
resolve different strings, and only an enumeration receipt from that host
re-pins them. The `-sc 2` last-row selection discards the first sample by
design; a reader who wants the first row has left the grammar. Not a census
surface: no `SURFACE` row, no census finding id, no DRIFT verdict, no
baseline re-pin — `tools/mori-census.sh` names none of these counters.

Boundaries: alerting on any gauge or rate (thresholds, watchers, triggers)
stays FR8-frontier and is not this instrument; changing page-file, commit or
memory configuration is the operator's (host repair → tsukuroi); the probe
never writes a counter, log or registry value. Coverage-map: advances the
Windows-host resource-runway arm (the commit gauge pair) and adds the
paging-rate read; the Linux commit-runway/PSI instruments remain the
registered gates on Linux hosts.
