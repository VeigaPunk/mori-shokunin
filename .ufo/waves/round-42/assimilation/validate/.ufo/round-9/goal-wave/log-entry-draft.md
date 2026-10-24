# Round 9 log-entry draft (scribe seat, goal wave)

Integration target: append as a `## Round 9 — … (goal wave)` entry at the end of `LOG.md`
(parent-owned; append-only — nothing above the new section changes). `[PARENT: …]` marks
what only the integration commit/acceptance can bind; `[PENDING: …]` marks values unlanded
at this draft's clock (v1, 2026-10-15T21:31Z).

---

## Round 9 — operability: the selftest grep-over-pipe SIGPIPE race eliminated at every harness site (goal wave)

**Round 9 — goal-wave admission (2026-10-15).** Motivating evidence: the round-8 admission's
registered top debt (`SCORECARD.md:413-422`; r8 report "Defect at admission") — the selftest
harness false-failed 1/8 (parent determinism battery: 55/56, `missing match` on a silence
case) to ~25% (one seat's battery), a random case each time, green on rerun, probe logic
untouched; named sites `tools/mori-census.sh:1783/:1809`. Entering bytes: census
`390ab9cd…` (r5, 2380 lines), oracle `448f7723…` (byte-frozen).

Scribe's own before-side, first-hand: (a) full-file sweep at HEAD found **six** harness
class sites — `:1771`, `:1772` (a message site with `printf | grep | head -n1` the lesson's
five-site table misses), `:1773`, `:1779`, `:1783`, `:1809` (`printf '%s\n' "$out" | grep …`
with an early-exit consumer under top-level `set -euo pipefail` `:194`); (b) 16 × `--selftest`
at a frozen copy: 16/16 green, 0 flakes (stated as measured — below the battery's resolving
power, not evidence against the class). The lessons-distiller seat measured the mechanism
first-hand (`corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md`): `grep -q` exits 0 at
its match and closes the pipe, the `printf` subshell takes SIGPIPE mid-payload
(`strace`: `write … = -1 EPIPE` → `killed by SIGPIPE`), `pipefail` makes the pipeline rc 141,
and the guard reads "missing" — with `ps0=141 ps1=0` attribution and construct rates
~1/3000 per assertion at harness sizes (both pre-fix batteries — lesson 32 runs, scribe 16
runs — read 0 flakes, bounding the rate).

Landed (evidence commit `[PARENT]`): `tools/mori-census.sh` `1c49238a…` (2394 lines, +21/−7
vs HEAD) — the fix captures each case's output to `OUT_FILE="$work/.last-out"` (`:1585`,
`/tmp` fixture tree) and all six harness match sites grep the **file** (`:1784`, `:1785`,
`:1786`, `:1792`, `:1796`, `:1823` — including the two message substitutions now
`grep -m1 … "$OUT_FILE" || true`); no live pipe remains in the harness. Scope proof:
all 8 diff hunks are inside `run_selftest()` (`:1571`…`2361` at HEAD); prefix lines 1–1570
(production path) byte-identical (sha256 `19772ee2…` both sides); suffix from `# ---- main`
to EOF byte-identical; the diff adds no pipeline character. Post-fix sweep: the only
early-exit-consumer pipe left in the file is production `:1322` (`printf | sed | grep -Fxq`
in the authorship `if`) — same class, out of the fix scope under the byte-freeze, named
debt (the lesson measured 88/3000 pipeline-nonzero-despite-match on its shape). Oracle
`448f7723…` **byte-unchanged** throughout (`git diff` empty). Selftest stays **56 cases**
(none added/removed — the diff changes assertions only). No new bare pipelines. Note
`corpus/knowledge/selftest-flake-r9.md` landed 21:35Z: mechanism §1 (incl. per-line write
chunking), all-56-payload replay (2 fires / 13 300), §3 git archaeology (the construct
since the harness's first commit `7ca17b1`), §5 the two ≥20-run post-fix batteries
(40/40; loaded arm with 4 CPU hogs, killed at arm end), §6 determinism-gate recipe. `corpus/README.md` r9 index rows + the r8 known-gaps
disposition landed; `corpus/knowledge/surfaces-r8.md` defect-2 disposition (r9 root-cause
+ fix) landed; SKILL.md r9 rows `[PENDING at scribe clock]`.

**Scribe battery at the fixed bytes (`1c49238a…`, frozen copy, sha re-verified
`1c49238a…` before and after):** 24 × `--selftest` (16-run battery + 8-run extension) —
all `MORI_CENSUS_SELFTEST: PASS (56 cases, 56 passed, 0 failed)`, rc=0, **0 flakes**; oracle
`matched=28 total=28` rc=0 ×2 (28 `PASS` case-lines each) at the frozen `448f7723…`; live
census `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` rc=1, stderr
0 B, with all 16 surface rows' key-sets identical to the r8 live receipt run1 and the
finding-id set identical. Fail-path control: a `/tmp` mutant renaming only the
production-side `TMUX_SESSION_IDLE` emission yields deterministic
`FAIL (56 cases, 55 passed, 1 failed)` rc=1 with `missing match |FINDING TMUX_SESSION_IDLE
…|` — the fixed asserts still catch genuine misses.

**Parent acceptance (`[PARENT: 2026-10-15T__Z]`).** `[PARENT: re-run — selftest 56/56 exit 0;
oracle 28/28 exit 0 (oracle sha must equal `448f7723…`); live census; ≥20-run determinism
battery at the final bytes; verify the final census sha equals or supersets `1c49238a…`
(this draft's scope proof binds those bytes).]` The two ≥20-run post-fix batteries
required by the round's claim landed in `corpus/knowledge/selftest-flake-r9.md` §5
(note-writer: 20 runs unloaded + 20 under 4 CPU hogs it killed, 40/40 PASS, lane sha
re-verified before/after; cross-referencing the scribe's 24-run battery) — 64 post-fix
runs across two seats, 0 flakes; receipts landed 21:40:35Z —
`corpus/evidence/flake-r9-20261015T2119Z-{selftest,selftest-battery-a,selftest-battery-b,oracle,live}.log`
(battery-a 20/20 unloaded; battery-b 20/20 under 12 owned CPU hogs, all killed, `gone=yes`;
single canonical run 56/56 exit 0; oracle 28/28 with frozen re-check; live 3-run
identity) — **104 post-fix runs across three seats, 0 flakes**.

**Verdicts.** `[PARENT: bind — expected ADMIT on the evidence above; no scalar score.]`
Read: operability **improved** (the race class is eliminated at every harness occurrence —
six sites, one more than the v1 lesson table; production path byte-identical; oracle
byte-frozen and green; selftest 56), coverage **unchanged** (no new surface; registry
unchanged), depth **improved** (lesson with the class, every occurrence, the mechanism and
a measured countermeasure), freshness **unchanged** (bytes SHA-pinned through three seats'
batteries; r9 receipts landed `flake-r9-20261015T2119Z-*`), calibration **improved
narrowly** (three pre-fix battery rates measured — lesson 32 runs, scribe 16, note 10; the
fix's necessity anchored by the `ps0=141 ps1=0`
attribution), adjacency **unchanged**; none harmed. Named debt for round 10: production
`:1322` (same class; needs a production-touching round + oracle re-verification); an
admission-time determinism gate (run the suite ≥20×, require equal verdicts); carried —
frozen-behavioral drift pin, tmux freshness live-proof, instantaneous disk-rate deferral,
row-6 report-body residual, receipt-binding and role-routing debts, memory thresholds stay
labeled local.

**Boundaries held.** Detection/report only; no remediation/kills/config edits; fixtures and
capture file live only under the `/tmp` hermetic work tree; oracle touched by no seat
(byte-frozen); seats committed nothing; parent integrated under the mori identity.
`[PARENT: confirm from the integration diff]`

Round report: `[PARENT: .ufo/reports/round-9/mori-goalwave.md]` · Verified lane rounds:
`[PARENT: 8 → 9]`.