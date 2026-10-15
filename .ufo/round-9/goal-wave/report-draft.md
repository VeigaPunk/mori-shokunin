# mori round 9 — goal-wave report draft (scribe seat)

Integration target: the round report (idiom of `.ufo/reports/round-8/mori-goalwave.md`;
final path `[PARENT]`, likely `.ufo/reports/round-9/mori-goalwave.md`). Parent owns the
final path, the identity and the commit binding. Every figure is bound to a landed
artifact, a receipt, or a command run at a pinned SHA; `[PARENT: …]`/`[PENDING: …]` as
elsewhere. Draft status: **v1** by the scribe seat.

- Status: `[PARENT: completion statement + verified-round-count claim 8 → 9]`
- Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
- Baseline: `c47c888` (round-8 records; evidence `9738f1a`)
- Wave: `[PARENT: bind the wave record — batch shape, seat completion/loss counts, any backfill]`
- Report time: `[PARENT]`
- Draft basis: before-side (entering bytes census `390ab9cd…` / oracle `448f7723…`,
  first-hand 21:07–21:16Z); after-side (census `1c49238a…`, stable from 21:17Z, sha
  re-verified through the battery; oracle byte-unchanged). Scratch
  `/tmp/mori-scribe-r9/{before,after}/`.
- **Landing state at scribe clock:** the note (`corpus/knowledge/selftest-flake-r9.md`,
  21:35Z), the r9 receipt set (`corpus/evidence/flake-r9-20261015T2119Z-*`, 21:40Z, incl.
  both ≥20-run batteries and the oracle frozen re-check), the README r9 rows and the
  surfaces-r8 disposition all landed; the only named gap left is the SKILL.md r9 rows
  `[PENDING]`.

## Work performed

- Selected axis **operability** — the round-8 admission's registered top debt
  (`SCORECARD.md:413-422`): the selftest harness grep-over-pipe SIGPIPE race (1/8–25%
  false-FAIL on a random case, green on rerun; named sites `:1783`/`:1809`).
- Registered claim: before — the race false-fails selftest runs; after — the race class is
  eliminated at EVERY occurrence, two independent ≥20-run batteries (one under load) show
  0 flakes, the production census is byte-behavior-identical (fix touches only the
  `--selftest` path: oracle 28/28 with wants UNCHANGED at the new SHA; live rows
  additive-identical to r8 receipts), selftest stays 56, no new bare pipelines, the ORACLE
  file byte-frozen.

## Before → after measurements (scribe first-hand)

| Item | Before at `390ab9cd…` | After at `1c49238a…` |
|---|---|---|
| Class sites (harness) | six: `:1771`, `:1772` (`printf\|grep\|head -n1` — missed by the lesson's five-site table), `:1773`, `:1779`, `:1783`, `:1809` | zero live pipes in the harness; all six grep the captured `OUT_FILE` (`:1784`/`:1785`/`:1786`/`:1792`/`:1796`/`:1823`) |
| False-FAIL rate | parent determinism battery 1/8; admission seat ~25%; lesson construct rate ~1/3000/assertion at 2.3 KB early-match, scaling with size | n/a — no writer process can kill the consumer's answer; 24-run scribe battery 0 flakes (16+8, rc=0) |
| Scope of change | — | all 8 hunks inside `run_selftest()` (`:1571`…`2361`); prefix 1–1570 byte-identical (sha `19772ee2…`); `main()` suffix byte-identical; **no** pipeline added |
| selftest | `PASS (56 cases, 56 passed, 0 failed)` (16/16 runs green in scribe battery) | `PASS (56 cases, 56 passed, 0 failed)` ×24 (16 + 8 runs, rc=0, 0 flakes) |
| oracle `448f7723…` | `matched=28 total=28` exit 0 (r8) | byte-frozen (`git diff` empty); `matched=28 total=28` rc=0 ×2 (28 `PASS` case-lines each) |
| live census | `DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` | `DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` rc=1, stderr 0 B; all 16 surface rows' key-sets identical to `residuals-r8-20261015T2040Z-live.log` run1; finding-id set identical |
| fail-path control | — | `/tmp` mutant renaming only the production-side `TMUX_SESSION_IDLE` emission: `FAIL (56 cases, 55 passed, 1 failed)` rc=1, deterministic `missing match` on exactly that case — the fixed asserts still catch genuine misses, they do not pass vacuously |
| production same-class residue | — | `:1322` (`printf \| sed \| grep -Fxq` in the authorship `if`) remains — out of fix scope under the byte-freeze; lesson measured 88/3000 wrong-grade rate on its shape |

## Landed changes (at scribe clock)

- `tools/mori-census.sh` → `1c49238a7fd87277151ff5776acfb4d62fadd9d69764a02f0ede03ef0d3902d2`
  (2394 lines, +21/−7 vs HEAD): per-case `OUT_FILE` capture + file-based greps at all six
  harness sites (r9 fix comment block cites the lesson); `|| true` on the two message
  substitutions; no other region touched.
- Lesson `corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md` (landed): class,
  every-occurrence table, mechanism (`PIPESTATUS` attribution, `strace` EPIPE), measured
  countermeasure (here-string 0/3 400), `:1322` production bound (88/3000), 32-run
  pre-fix battery (0 flakes).
- Note `corpus/knowledge/selftest-flake-r9.md` (landed 21:35Z): mechanism + the writer's
  per-line chunking (§1a), the all-56-payload replay (2 fires / 13 300 trials; §1b), the
  end-to-end r8-string repro (§1c), git archaeology — the construct since the harness's
  first commit `7ca17b1` (§3), the fix map (§4), the two ≥20-run post-fix batteries
  (40/40; loaded arm with 4 CPU hogs, §5), a detection-power mutation (§4), and the
  cost-ordered determinism-gate recipe (§6).
- `corpus/README.md` r9 index rows + r8 known-gaps disposition landed;
  `corpus/knowledge/surfaces-r8.md` defect-2 disposition landed; receipts
  `corpus/evidence/flake-r9-20261015T2119Z-{selftest,selftest-battery-a,selftest-battery-b,oracle,live}.log`
  landed 21:40:35Z. `[PENDING]` SKILL.md r9 rows.
- Oracle `tools/mori-silence-cases.sh` untouched (`448f7723…`, `git diff` empty at every
  check) — byte-frozen as the round requires.

## Corrections and honest boundaries

1. **The class was rare per assertion, not per-run-common, at this host/load.** Three
   independent pre-fix batteries (lesson 32 runs instrumented; scribe 16 runs; note 10
   runs) read 0 flakes; the r8 live rates (1/8–25%) are the load-sensitive end. The fix
   eliminates the mechanism by construction (no writer process to SIGPIPE), not by
   narrowing a race window.
2. **Six harness sites, not five.** The v1 lesson table enumerates five; `:1772`
   (`got=$(printf … | grep '^MORI_CENSUS:' | head -n1)`) is the same class with a
   `head -n1` early-exit consumer. The landed fix converts it; the round's "every
   occurrence" mandate is met at six. (Message-site races misformat text, they don't flip
   verdicts — but they are the same class.)
3. **One same-class production site stands: `:1322`.** Fixing it changes production bytes;
   the round froze production behavior, so it is named debt with a measured wrong-grade
   rate (88/3000 on its shape), not silently dropped.
4. **The ≥20-run batteries are receipt-backed.** `corpus/knowledge/selftest-flake-r9.md`
   §5 (21:35Z): note-writer arms — 20 runs unloaded + 20 runs under 4 CPU hogs, 40/40
   PASS. Receipts (`corpus/evidence/flake-r9-20261015T2119Z-*`, landed 21:40:35Z):
   battery-a 20/20 unloaded (host wave load ≈97–101), battery-b 20/20 under **12 owned
   CPU hogs** (all killed, `gone=yes`; load ≈102→121), single canonical run 56/56 exit 0,
   oracle 28/28 with a frozen re-check, live 3-run identity. With the scribe's 24:
   **104 post-fix runs across three seats, 0 flakes.**
5. **Post-battery risk named:** the census could be edited after this clock (other seats
   were still landing note/receipts); the acceptance must re-verify the final SHA against
   `1c49238a…` (or re-run the scope proof if it moved).

## SHONEN

- [ ] · [ ] · [ ] · [ ] — all four remain `[ ]`: no named non-author verifier; wave seats
  are the lane per protocol.

Boundaries held: detection and report only; no remediation/kills/config edits; the capture
file and all fixtures live only under the `/tmp` hermetic work tree; oracle byte-frozen;
seats made no commits; fleet root read-only for seats. `[PARENT: confirm from the
integration diff]`