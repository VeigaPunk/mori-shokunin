source: S572 (learn.microsoft.com — Application or service memory leaks
troubleshooting; pinned copy `corpus/evidence/sources-r63/S572.html` sha256
3f2fd8a26e9258ecb8e5456819992338a96343adb456affc248fe56892f71bf6) and S573
(learn.microsoft.com — wevtutil command reference; pinned copy
`corpus/evidence/sources-r63/S573.html` sha256
e6dc117481252ddf9aa7f21c125517233e7eee4cd42f7ab755ca4a3cb1dfd758)
verified-at: 2026-10-31 (round 63; claims below are line-located against the
pinned copies; live receipt on this host
`.ufo/waves/round-63/evidence/host-events-live-win-r63.txt`)
recheck: 180d, or when a re-fetch of either page changes its sha256 against
the pinned copies

# Reading the Windows event-log kill/exhaustion surface (round 63)

Scope: detection and report only, counts and shapes only. This entry grounds
`tools/mori-host-events-win.py` (round-63 build): a one-shot, read-only probe
of the Windows event log for kill/exhaustion events — the surface class the
lane's Linux instruments read through journalctl and cgroup pressure files,
which are absent on the Windows workspace host (PROVINCE Round-62 host note).
The probe executes `wevtutil qe` (a read) per surface and prints counts,
pinned table names and state words; never pids, user names, computer names,
message text or timestamps. Claims (K1–K4 ground the 2004 row from S572;
K5–K9 ground the query mechanics from S573):

- **K1** — `S572.html:757` — "You see Event ID 2004 repeatedly in the system log.": the System log's event id 2004 is the documented memory-exhaustion diagnosis signal; the probe's `System/2004` row is that signal, not an extrapolation.
- **K2** — `S572.html:763` — sample event `Source: Microsoft-Windows-Resource-Exhaustion-Detector`: the provider name the probe's XPath filter binds is the document's own `Source:` value for the 2004 event.
- **K3** — `S572.html:766` — sample event `Task Category: Resource Exhaustion Diagnosis Events`: the event's task category names the diagnosis class, so the probe's label `memory-exhaustion-diagnosis` is the surface's own vocabulary.
- **K4** — `S572.html:768` — sample event `Keywords: Events related to exhaustion of system commit limit (virtual memory).`: the semantics are commit-limit exhaustion (resource runway), which is the lane's OOM/runway observability object on this host.
- **K5** — `S573.html:752` — `qe` (query-events) grammar carries `/q:<Query>`, `/rd:<Direction>`, `/c:<Count>`: the probe's argv shape is the command's documented grammar.
- **K6** — `S573.html:888` — `/q:<Query>` "Defines the XPath query to filter the events that are read or exported.": the provider+event-id XPath filter is the documented filter mechanism, so per-surface counts are filter-scoped reads.
- **K7** — `S573.html:901-902` — `/rd:<Direction>` "Specifies the direction in which events are read." with "If true, the most recent events are returned first.": the probe's `recent_first=true` is the documented semantics of `/rd:true`.
- **K8** — `S573.html:907-908` — `/c:<Count>` "Sets the maximum number of events to read.": counts are bounded reads — `matched=N` means N within the most recent window, never a total; the summary prints `window=N` so the bound travels with every receipt.
- **K9** — `S573.html:982` — documented example `wevtutil qe Application /c:3 /rd:true /f:text`: reading the Application log with a count cap, recent-first, is the reference pattern, grounding the probe's `Application/1000` and `Application/1001` rows as the same documented read class.

Limits (declared): the probe counts events and never infers a cause — an
exhaustion-event count is evidence the host diagnosed exhaustion, not a
diagnosis of which process leaked (attribution stays with the event text the
probe deliberately does not read; the redaction rule). The 1000/1001/6008
table rows are the host's standard provider/event-id conventions,
live-verified by the receipt (`AVAILABLE ok=4`), not line-located in the
pinned docs — K1–K4 ground the 2004 row only. High-volume providers saturate
the window (live receipt: 1001 matched=200=window), so a saturated row
measures saturation, not volume. `wevtutil` missing or a failing query is
`unavailable`, never zero (honest-unavailable rule; selftest arm 5). No
`wevtutil epl`/`cl` (export/clear) is ever invoked; the probe is a read.
Coverage-map: advances the Windows-host kill/exhaustion arm only; the Linux
journal/pressure instruments remain the registered gates on Linux hosts.
