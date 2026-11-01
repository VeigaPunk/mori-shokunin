source: S582 (learn.microsoft.com — GetTickCount64, sysinfoapi; pinned copy
`corpus/evidence/sources-r70/S582.html` sha256
580f1935fb47b5c992a48d22299f7452aaeb00099f2ac96ba74c92002a18277f) and the
S581 scale context (docs.aws.amazon.com — Setting timestamp expiration and
token immunity times in AWS WAF, `corpus/evidence/sources-r70/S581.html`,
opened the same round for the C1 window work; carried here only as the
same-round source set, not as ground for this entry)
verified-at: 2026-11-01 (round 70; claims below are line-located against the
pinned S582 copy; live receipt on this host
`.ufo/waves/round-70/evidence/uptime-win-live-r70.txt`)
recheck: 180d, or when a re-fetch of the page changes its sha256 against the
pinned copy

# Reading the Windows host-uptime surface (round 70)

Scope: detection and report only, counts and shapes only. This entry grounds
`tools/mori-uptime-win.py` (round-70 build): a one-shot, read-only probe of
the host tick count — the since-boot context the lane's Linux census reads
from `/proc`-class surfaces, absent on the Windows workspace host (PROVINCE
Round-62 host note). The probe is evidence CONTEXT: the r63 event-log counts
and the r64 runway reads accumulate inside the boot window the count
describes. It never grades liveness (a hung host still accrues uptime),
never names a boot identity (the API returns none; `boot_identity=absent`
travels on every receipt line), and never attributes anything to a boot —
boot-state diagnosis stays tsukuroi/operator (PROVINCE refuses). Claims
(K1–K5, line-located in the pinned S582 copy):

- **K1** — `S582.html:829` — "Retrieves the number of milliseconds that have elapsed since the system was started.": the count is UPTIME (ms since system start); the probe's `uptime_ms` is that count, not wall-clock time, not boot identity, not a session or process age.
- **K2** — `S582.html:831-833` — `ULONGLONG GetTickCount64();` returning "The number of milliseconds.": the API domain is the full unsigned 64-bit range; the probe sets the ctypes restype to `c_ulonglong` explicitly (the default `c_int` restype would truncate) and the selftest pins the exact rendering of the domain maximum so a truncating build cannot pass.
- **K3** — `S582.html:836` — the resolution is "limited to the resolution of the system timer, which is typically in the range of 10 milliseconds to 16 milliseconds" and is "not affected by adjustments made by … GetSystemTimeAdjustment": the printed millisecond digits carry that resolution; the probe rounds nothing and claims no precision beyond it.
- **K4** — `S582.html:842` — "To obtain the time the system has spent in the working state since it was started, use the QueryUnbiasedInterruptTime function.": the doc's own pointer defines the boundary — this count is NOT working-state time and includes sleep/hibernation time; `count=biased` travels on every receipt line so the caveat cannot be lost in a copy.
- **K5** — `S582.html:845` — on debug ("checked") builds "the interrupt-time count and tick count are advanced by approximately 49 days": a shifted count is possible on such builds; the probe prints the raw count and this caveat is carried in this entry — the receipt reader grades the host class before comparing counts across rounds.

Limits (declared): one volatile count, no series — consecutive runs are
separate counts, never a rate or trend (the probe computes nothing between
runs). Uptime alone is not liveness, not health, and not an uptime
prediction; the probe emits no threshold, alarm or DRIFT verdict and is not
a census surface (no `SURFACE` row, no finding id, no baseline re-pin —
`tools/mori-census.sh` names no such row on this host's account). A zero is
a real count (a successful read inside the first tick); a failed read is
`unavailable` with a reason, never zero. No `boot id`, no sleep/hibernation
split, no working-state time (that is QueryUnbiasedInterruptTime's ground,
unopened), no multi-boot history — all stay unmeasured here.

Boundaries: writing boot configuration, diagnosing boot state, sleep/power
behavior and anything preceding the current boot are tsukuroi/operator
ground; mori reads the tick count as fleet-evidence context and reports it.
The probe writes nothing to the host.

Coverage-map: advances the Windows-host liveness-context arm only (the
Round-62 host note's absent Linux surfaces stay absent here; the registered
gates on Linux hosts are unchanged). Owns-scope extension recorded in the
round-70 SCORECARD section and this entry; the PROVINCE.md head stays
byte-frozen (r65 L0 set) and takes no edit this round.

Round-71 correction (append-only block; routed defect D1, r70 closure section 6,
status-neutral) — the K2/K4/K5 located-line pointers above are superseded by
S583 (supersedes S582) and the erratum
`.ufo/waves/round-71/evidence/s582-pointers-erratum-r71.txt`, each pointer
re-verified against the pinned copy (byte-identical live re-open,
`source-s582-reopen-r71.txt`):

- **K2** — read `S582.html:831-834` for `S582.html:831-833`: the return-value
  sentence "The number of milliseconds." is at `:834` (the recorded `:833` is
  the `<h2 id="return-value">` heading). Signature `:831` unchanged.
- **K4** — read `S582.html:841` for `S582.html:842`: the working-state
  boundary sentence is at `:841` (the recorded `:842` is the alert div that
  follows it). The `count=biased` claim and its ground are unchanged.
- **K5** — read `S582.html:842` for `S582.html:845`: the debug-build ~49-day
  alert is at `:842`, inside that alert div (the recorded `:845` is the
  `<h2 id="requirements">` heading). The caveat itself is unchanged.
- K1 (`:829`) and K3 (`:836`) were re-verified exact; the quote texts were
  real throughout (the closure verified them) — only the locations drifted.
The r70 receipt and fleet report bytes carry the same superseded pointers and
stay untouched (frozen history; the erratum names them). Downstream: the
round-71 entry `workstate-win-r71.md` is written against the corrected
pointers, and this entry's working-state boundary now points at the opened
surface (`corpus/knowledge/workstate-win-r71.md`, sourced S584).
