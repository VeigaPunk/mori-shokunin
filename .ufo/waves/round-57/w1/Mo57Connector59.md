# Round 57 coverage cross-check — Mo57Connector59

## Evidence and verdict

The frozen contract defines C1 solely as two SCORECARD capability rows and C2 solely as eight source-grounded statements about `unclosed` (`.ufo/waves/round-57/contract.md:5-7`). Neither predicate requires another runtime surface. FR5, however, is still explicitly watchdog daemon identity/degraded-pgrep visibility, whose boundary says unavailable pid probe is not absence and argv-substring matches do not establish identity (`PROVINCE.md:48`).

The round-56 driver probe is a separate, genuinely distinct observability surface: its docstring says inline mode has no daemon, making census `WATCHDOG_ABSENT` fire each round, and it reads driver launch/complete/dead records from `.ufo/watchdog.log` instead (`tools/mori-driver-liveness.py:4-10`). It emits per-lane counts, ages, `in_flight` and pairing-count `unclosed`; explicitly no lane health verdict (`tools/mori-driver-liveness.py:32-40,172-173,238-242`). The knowledge entry sharpens novelty: census had already consumed launch epochs for silence grading, so this probe's new surface is strict per-event pairing and grammar/error classification, not first access to the log (`corpus/knowledge/driver-liveness-r56.md:10-26`).

Counterexample / boundary: the legacy census watchdog probe still uses `pgrep -af shokunin-watchdog` and text filtering (`tools/mori-census.sh:710-720`); driver-log facts cannot establish daemon process identity or repair that ambiguity. Conversely, the new probe does not claim to replace that daemon probe: it labels its output as log-shape facts and its unavailable verdict for missing/unreadable/empty logs (`tools/mori-driver-liveness.py:38-40,201-221`). The knowledge entry also names historical `lane-round-failed` lines as unattributed `other_lines`, a concrete grammar-coverage limitation (`corpus/knowledge/driver-liveness-r56.md:69-75`).

**Verdict:** an outside-core observational surface is evidenced (strict driver-event pairing from the shared driver log), while FR5 daemon identity remains open. This supports considering the capability as a distinct observability capability, but neither the round-57 C1/C2 predicates nor the evidence justify claiming FR5 closed, daemon liveness, or a production behavior change.

## Axes / bounded move

Potentially advances **coverage** by recording the separate driver-log event-pairing surface alongside the still-open FR5 daemon-identity boundary; it does not warrant a score delta. No depth/calibration/operability harm is evidenced if phrased narrowly as a distinction, not a replacement or health claim. Recommended move: retain explicit two-surface distinction in capability/frontier reporting: (1) daemon PID/pgrep identity remains FR5; (2) driver-authored event-log pairing is a separate read-only source with its own grammar and attribution limits. This is report-only and does not alter frozen counters.

Risks: conflating both meanings of “liveness” would falsely imply daemon identity or lane health; treating `unclosed` as current running work contradicts the implementation's pairing-count definition. Verification: read the cited code and knowledge lines; no commands or runtime probes executed by this seat.

Report: .ufo/waves/round-57/w1/Mo57Connector59.md
