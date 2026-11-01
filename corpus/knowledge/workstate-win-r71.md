source: S584 (learn.microsoft.com — QueryUnbiasedInterruptTime, realtimeapiset;
pinned copy `corpus/evidence/sources-r71/S584.html` sha256
d0bcbba945e7cf29d4664feb28a35aa31c1f80cadb5191644a33ab84464f9136, 54774
bytes) and S582 (learn.microsoft.com — GetTickCount64, sysinfoapi; pinned copy
`corpus/evidence/sources-r70/S582.html` sha256
580f1935fb47b5c992a48d22299f7452aaeb00099f2ac96ba74c92002a18277f — re-opened
this round byte-identical, receipt
`.ufo/waves/round-71/evidence/source-s582-reopen-r71.txt`; its located-line
pointers are the S583-corrected ones: :834/:841/:842, see
`.ufo/waves/round-71/evidence/s582-pointers-erratum-r71.txt`)
verified-at: 2026-11-01 (round 71; claims below are line-located against the
pinned S584 copy; live receipt on this host
`.ufo/waves/round-71/evidence/workstate-live-r71.txt`)
recheck: 180d, or when a re-fetch of either page changes its sha256 against
the pinned copies

# Reading the Windows working-state surface (round 71)

Scope: detection and report only, counts and shapes only. This entry grounds
`tools/mori-workstate-win.py` (round-71 build): a one-shot, read-only probe
reading the two counters the pair of API pages defines — the biased tick
count (GetTickCount64, S582:834 "The number of milliseconds.", the r70
uptime probe's count, which INCLUDES time asleep or hibernating per the
S582-corrected boundary pointer :841) and the unbiased interrupt-time count
(QueryUnbiasedInterruptTime, S584), printed side by side with their derived
delta. The r70 probe carried `count=biased` and named this surface
"unopened"; this round opens it as its own detection surface. It is
evidence CONTEXT like the uptime read: it never diagnoses power behavior,
never attributes a sleep or hibernation episode, never names a boot
identity, and stays outside census surfaces. Sleep/power behavior and
boot-state diagnosis remain tsukuroi/operator ground (PROVINCE refuses).

Claims (K1–K6, line-located in the pinned S584 copy):

- **K1** — `S584.html:817` — "Gets the current unbiased interrupt-time count, in units of 100 nanoseconds.": the UNITS ground. The raw unbiased count is 100-ns units, not milliseconds; the probe converts to ms by integer floor division by 10000 and names the conversion on the line (`conversion=unbiased_ms-floor(10000)`). A naive ms-reading of this count is a 10000x unit error — the selftest's `unit_math` arm pins the correct conversion.
- **K2** — `S584.html:819-820` — `BOOL QueryUnbiasedInterruptTime(PULONGLONG UnbiasedTime)`: the call SHAPE differs from GetTickCount64's return-value shape (S582:831 `ULONGLONG GetTickCount64();`); the count arrives through an out-parameter. The live reader pins `argtypes=[POINTER(c_ulonglong)]`, passes `byref`, and pins the `c_int` BOOL restype — the selftest's `uint64_max_rendered` arm pins the exact rendering of the unsigned-64 maximum for both counts so a truncating binding cannot pass.
- **K3** — `S584.html:826-827` — "If the function succeeds, the return value is nonzero. If the function fails because it is called with a null parameter, the return value is zero.": the named error signature. A zero RETURN is a failed call and maps the whole surface `unavailable` (`reason=qunbiased_return_zero`) — never to a zero count.
- **K4** — `S584.html:828` — "The interrupt-time count begins at zero when the system starts": a zero count is real near a boot; the selftest's `zero_is_real` arm pins it.
- **K5** — `S584.html:830` — "reflects only the time that the system is in the working state" and "not 'biased' by time the system spends in sleep or hibernation": the working-state boundary this probe reports. The pair (biased, unbiased) and their delta are printed as counts; the probe never decomposes the boot into episodes and never claims a sleep event — a strongly positive delta would bound accrued non-working time within the boot window, and nothing more.
- **K6** — `S584.html:833` — on debug ("checked") builds "the interrupt-time count and tick count are advanced by approximately 49 days": BOTH counters shift together there, so the delta shape is preserved while both absolutes shift; `debug_build_caveat=carried` travels on every line (same caveat as the r70 uptime entry).

The derived delta — declared read model: the two counts are TWO SEPARATE
read instants (`read_model=two-separate-reads` travels on the line), so the
delta is biased_ms(t1) minus unbiased_ms(t2), t2 > t1. On a host awake for
its whole boot, both counters tick in lockstep and the delta is a small
SIGNED remainder of read skew plus floor conversion — the round-71 live
receipt shows exactly that shape on this host: deltas -7, -12, -11 ms at a
biased count near 493.6e9 ms (~5.7 days into ONE boot window, the same
window the r70 uptime read opened; uptime_ms=489381578 at the r70 closure,
493623375 here ~1.2 h later). A small negative is expected noise, printed
as-is; the selftest's `delta_signed_shape` arm pins the honest signed
rendering. The probe claims no trend: consecutive runs are separate counts,
never a rate.

Limits (declared): one-shot volatile counts, no series; no episode
attribution, no sleep/hibernation decomposition, no wake/sleep timestamps,
no power-state diagnosis (tsukuroi/operator); no boot identity (neither API
returns one — `boot_identity=absent`, never inferred); not a liveness
verdict; not a census surface (no `SURFACE` row, no finding id, no baseline
re-pin); the Precise variant (QueryUnbiasedInterruptTimePrecise,
`S584.html:876`) stays UNOPENED. A failed call is `unavailable` with a
reason, never zero.

Boundaries: writing power configuration, diagnosing sleep/hibernation or
boot state, and anything preceding the current boot are tsukuroi/operator
ground; mori reads the two counters as fleet-evidence context and reports
them. The probe writes nothing to the host.

Coverage-map: advances the Windows-host liveness-context arm only (the
Round-62 host note's absent Linux surfaces stay absent; registered gates on
Linux hosts unchanged). Owns-scope extension recorded in the round-71
SCORECARD section and this entry; the PROVINCE.md head stays byte-frozen
(r65 L0 set) and takes no edit.
