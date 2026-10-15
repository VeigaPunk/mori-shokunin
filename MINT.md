# MINT — mori-shokunin (2026-10-14)

**Cause:** operator directive (the 12-hour shokunin fleet program, 2026-10-14),
plus documented demand the roster could not absorb.

**Demand instances (evidence):**

1. **The 2026-10-14 webbridge daemon OOM-death went undetected for hours.** The
   operator reports the kimi-webbridge daemon died and nobody noticed until much
   later. No lane watches daemon liveness. Evidence: operator mission text
   (`.ufo/scopes/shokunin-12h-20261014/operator-demand.md`).
2. **The parallel training fleet runs unsupervised waves.** Waves are dispatched
   by the L1 and settle asynchronously; a wave that never settles is invisible
   unless a human looks. Evidence: the fleet's own `.ufo/waves/*` directory with
   `swarm-registry.json` + dispatch/results pairs and no settlement watcher.
3. **tsukuroi owns OS state but nobody owns fleet health.** tsukuroi's province
   is pacman/systemd/driver/boot; kama's is endpoint identity; kumitate's is
   dispatch mechanism. None of them answers "is the fleet alive right now".

**Roster scan (rejected fit):** 17 lanes scanned
(`.ufo/scopes/shokunin-12h-20261014/mint-roster-scan.json`, per-lane
`PROVINCE.md` sha256 recorded). tsukuroi — OS planes, refuses fleet-process
observability. kumitate — dispatch mechanism, complementary not overlapping.
kama — endpoint identity only. kagi — credential custody only. No province
absorbs standing fleet/host liveness observation.

**Domain boundary:** observe and report only. Refuses dispatch (kumitate) and
OS-package state (tsukuroi). Never remediates.

**Probation:** >=3 verified rounds before a roster row. Roster row withheld.
