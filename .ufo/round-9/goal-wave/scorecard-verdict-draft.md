# Round 9 verdict — integration draft (scribe seat, goal wave)

Integration target: append as a `## Round 9 verdict — 2026-10-15 (goal wave)` section in
`SCORECARD.md` (parent-owned; append-only — the round-8 section `SCORECARD.md:387-437` and
everything above it stay untouched). Verdict vocabulary only (`improved` / `harmed` /
`unchanged` / `unprovable-but-better`); no scalar scores. Every figure below is bound to a
landed artifact, a receipt, or a command run at a pinned SHA; `[PARENT: …]` marks values
only the integration commit or the parent's acceptance re-run can bind; `[PENDING: …]`
marks values unlanded at this draft's clock. Draft status: **v1** by the scribe seat.

- Evidence commit: `[PARENT: wave integration commit hash under the mori identity]`
- Lane baseline entering the wave: `c47c888` (round-8 records; evidence `9738f1a`).
- Round-count claim: `[PARENT: verified-round accounting 8 → 9 on admission]`
- Before-side: first-hand at census
  `390ab9cd2db17b9d71508639f4f61cc61646ae090b61bf48243cda3e7211cae1`
  (`VERSION=census-r5`, 2380 lines) / oracle
  `448f77238c73a5c929a898dad0f0c495fd2a66cc4b90a00ae84ede69a86beeb5`, 21:07–21:16Z.
- After-side: census `1c49238a7fd87277151ff5776acfb4d62fadd9d69764a02f0ede03ef0d3902d2`
  (2394 lines; `git diff` +21/−7), stable from 21:17Z and re-verified unchanged through
  the after-side battery; oracle `448f7723…` **byte-unchanged** (`git diff` empty at every
  check; sha re-verified). Lesson
  `corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md` landed.
  Scratch `/tmp/mori-scribe-r9/{before,after}/`.

## Round 9 verdict

Round scope: the round-8 admission's registered top debt (`SCORECARD.md:413-422`; r8 report
"Defect at admission"; `LOG.md` r8 defect paragraph): the selftest harness grep-over-pipe
SIGPIPE race — measured 1/8 in the parent's determinism battery (55/56, `missing match` on
a silence case) and ~25% in one seat's battery, every false-FAIL a different case, green on
rerun, probe logic untouched.

Registered claim (round brief): before — the selftest false-fails at 1/8–25% on a random
case via the live-pipe-grep race; after — (1) the race class is eliminated at **every**
occurrence (not just the two named lines); (2) two independent ≥20-run batteries (one under
artificial load) show 0 flakes; (3) the production census is **byte-behavior-identical**
(the fix touches only the `--selftest` path: oracle 28/28 with wants UNCHANGED at the new
SHA; live rows additive-identical to r8 receipts); (4) selftest stays 56 cases; (5) no new
bare pipelines; (6) the ORACLE file is byte-frozen.

**Before** (entering bytes; my sweep + the lesson's measured mechanism):

- Harness class sites at HEAD (`390ab9cd…`; `run_selftest()` = `:1571`…`2361`, top-level
  `set -euo pipefail` `:194`): `:1771`, `:1772`, `:1773`, `:1779`, `:1783`, `:1809` —
  `printf '%s\n' "$out" | grep …` shapes whose consumer exits early (`-q`, `-m1`,
  `head -n1`). (Six sites; the lesson table and the note's §2 inventory both enumerate
  five — both omit `:1772`'s `head -n1` from their counts (the note names it in its §3
  archaeology), found by my `grep -n 'printf .*| *head'` sweep. The r8 report named the
  two `-q` loop sites.)
- Mechanism (lesson §A–C and note §1, both first-hand, `corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md`,
  `corpus/knowledge/selftest-flake-r9.md`):
  `grep -q` exits 0 at its first match and closes the pipe; the `printf` element (a forked
  bash subshell — 63 `write(2)` calls for a 2 292-byte payload) takes SIGPIPE mid-stream
  (`strace`: `write … = -1 EPIPE`, `killed by SIGPIPE`); with `pipefail` the pipeline rc is
  141; the `||`/`!` guard reads "missing". Construct-level rate at harness sizes:
  ~1/3000 per assertion (small-early), 3/5000 follow-up; decisive attribution rep
  `ps0=141 ps1=0` (grep matched; printf killed). Instrumented 32-run battery at the
  pre-fix bytes: 32/32 green, 4 256/4 256 assertions rc=0 — the class is rare per
  assertion; r8's live rates are the load-sensitive end of the same distribution. The
  note replays all 56 case payloads × their exact regexes ×100 (13 300 trials → 2 signal
  fires, both with the match present) and reproduces the literal r8 failure string
  end-to-end on a padded tail (2/200 at tail 200, 9/200 at tail 1 000).
- Scribe's own before-battery: 16 × `--selftest` at a frozen `390ab9cd…` copy — **16/16
  green, 0 flakes** (stated as measured; below the battery's resolving power, not evidence
  against the class).
- Production same-class, out of fix scope: `:1322` (`printf | sed | grep -Fxq` inside the
  authorship `if`) — fail-toward-wrong-grade; the lesson measured 88/3000
  pipeline-nonzero-despite-match on its exact shape.

**After** (census `1c49238a…`; oracle `448f7723…` unchanged):

- **The fix.** One capture file `OUT_FILE="$work/.last-out"` (`:1585`), written once per
  case (`printf '%s\n' "$out" > "$OUT_FILE"`, `:1781` / `:1817`); ALL six harness match
  sites now grep the file, never a live pipe: `:1784` (verdict), `:1785` (verdict message,
  `grep -m1 … || true`), `:1786` (diagnostic noise), `:1792` (noise message,
  `grep -m1 … || true`), `:1796` and `:1823` (the per-case want loops, `grep -qE -- "$re"
  "$OUT_FILE" || miss=…`). No `printf … | grep` remains in the harness.
- **Scope proof (the fix touches only the `--selftest` path).** All 8 diff hunks have
  old-line starts `1572 1583 1768 1771 1779 1783 1803 1809` — inside `run_selftest()`.
  Prefix `lines 1–1570` (the whole production path) byte-identical between HEAD and the
  fixed bytes: sha256 `19772ee21887437aad3d97f1b52584d1efbfa5c1119d5cf9d027e06cc912cc8b`
  on both sides. Suffix from `# ---- main` to EOF byte-identical. The diff adds **no**
  pipeline character; it removes three live pipes, file-izes two more, and `|| true`-guards
  the two message substitutions.
- **Post-fix sweep:** the only early-exit-consumer pipe remaining anywhere in the file is
  production `:1322` (named debt below). The untouched message-path `printf '%s' "$out" |
  tail -n3 | tr …` (`:1783`) has EOF-draining consumers — not this class.
- **Verdict machine at the fixed bytes.** selftest `MORI_CENSUS_SELFTEST: PASS (56 cases,
  56 passed, 0 failed)` ×24 (16-run battery + 8-run extension at the frozen bytes; rc=0,
  0 flakes, 0 failure files); oracle `matched=28 total=28` exit 0 ×2 (28 `PASS`
  case-lines each) with the oracle file byte-frozen (`448f7723…`, `git diff` empty); live
  census `MORI_CENSUS: DRIFT (findings=15 drift=14 unavailable=1 surfaces=7)` exit 1,
  stderr 0 B; all 16 surface rows' `key=` sets identical to the r8 live receipt run1
  (`corpus/evidence/residuals-r8-20261015T2040Z-live.log`), finding-id set identical;
  census sha re-verified `1c49238a…` before and after the battery. Negative control
  (fail-path proof): a `/tmp` mutant renaming only the production-side `TMUX_SESSION_IDLE`
  emission yields a deterministic `FAIL … missing match |FINDING TMUX_SESSION_IDLE …|`
  (55/56, rc=1) — the file-based asserts still catch genuine misses; they do not pass
  vacuously.
- **Batteries.** Scribe: **24 runs (16 + 8), 0 flakes** at the frozen bytes (raw logs:
  the session's battery task output + `/tmp/mori-scribe-r9/after-battery2.log`; no
  `fail-*.out` written). Note-writer (`corpus/knowledge/selftest-flake-r9.md` §5, landed
  21:35Z): pre-fix 10/10; post-fix 20 runs unloaded + 20 runs under 4 CPU hogs (load ≈91,
  hogs killed at arm end), 40/40 PASS. Receipts
  (`corpus/evidence/flake-r9-20261015T2119Z-{selftest,selftest-battery-a,selftest-battery-b,oracle,live}.log`,
  landed 21:40:35Z): battery-a 20/20 sequential (host wave load ≈97–101, no added hogs);
  battery-b 20/20 under **12 owned CPU hogs** (started 12, all killed, `gone=yes`; load
  ≈102→121); single canonical selftest run 56/56 exit 0 stderr 0 B; race-class source
  audit 0 hits in `:1571`…`2376`; oracle 28/28 ×2 with a frozen re-check. **104 post-fix
  runs across three seats, 0 flakes.** The note's §6 adds the cost-ordered
  determinism-gate recipe for future admissions.

| axis | verdict | before → after evidence |
|---|---|---|
| operability | **improved** *(selected axis)* | Before: harness assertion rc lied under SIGPIPE (rc 141 vs consumer 0), false-FAILs at 1/8–25% on data-neutral runs. After: no writer process can kill the consumer's answer — all six sites assert off the captured file; 24-run scribe battery 0 flakes (16+8, rc=0); selftest 56/56; oracle 28/28 ×2 at the frozen oracle sha; production path byte-identical (prefix/suffix proof) so the DRIFT/CLEAN contract is untouched. One same-class production site named (`:1322`), honestly out of fix scope. |
| coverage | **unchanged** | No new measured surface; case registry unchanged (56 cases, none added/removed by the diff — the diff modifies the harness assertions only). |
| depth | **improved** | Lessons/notes `2026-10-15-selftest-grep-sigpipe-race.md` + `selftest-flake-r9.md`: the class, every occurrence classified, the mechanism proved (PIPESTATUS attribution + `strace` EPIPE + the note's per-line chunking), the countermeasure measured (here-string 0/3 400; the landed fix uses the capture-file variant), the `:1322` production bound measured (88/3000), git archaeology (the construct since the harness's first commit `7ca17b1`), and a cost-ordered determinism gate (§6). |
| freshness | **unchanged** | Working-tree bytes SHA-pinned through three seats' batteries (sha re-verified before/after); lesson + note landed dated with re-run recipes; r9 receipts landed (`flake-r9-20261015T2119Z-*`, 5 files incl. both batteries + oracle frozen re-check); SKILL.md r9 rows `[PENDING]`; drift pin still carries. |
| calibration | **improved narrowly** | Pre-fix run-level rates measured by three batteries (lesson 32 runs, scribe 16, note 10 — all 0 flakes) and the class proved by construct-level replays (lesson ~1/3000–3/5000 per assertion; note 2 fires / 13 300 all-payload trials, 9/200 on a padded-tail end-to-end repro); the fix's detection power re-proved by two independent /tmp mutants (note `WATCHDOG_STALE`→`WATCHDOG_AGED`; scribe `TMUX_SESSION_IDLE` rename — both 55/56 exit 1). No threshold touched; no probe logic changed. |
| adjacency | **unchanged** | Detection/report only; fixtures `/tmp` only; oracle byte-frozen; no remediation/kill/config content; fleet root read-only for seats. `[PARENT: confirm from the integration diff]` |

Admission: `[PARENT: bind the admission and round-count at integration. Expected disposition
on the evidence above: **ADMIT** — the race class is eliminated at every harness occurrence
(six sites; the lesson table and the note's §2 inventory each enumerate five), the production
path is byte-identical, the oracle is byte-frozen and green, selftest stays 56, and no new
pipelines landed. The two ≥20-run batteries landed and are receipt-backed (note §5 20+20
with hogs; receipt battery-a 20 unloaded + battery-b 20 under 12 owned hogs — all killed;
plus the scribe's 24 runs; 104 post-fix runs across three seats, 0 flakes). The honest
limits: one same-class production site `:1322` stands as named debt (byte-freeze), and
SKILL.md r9 rows were still pending at scribe clock.]`
No scalar score.

Learning trends (lane idiom):

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | **improved** | Lesson `2026-10-15-selftest-grep-sigpipe-race.md` + note `corpus/knowledge/selftest-flake-r9.md` (both landed); `corpus/README.md` r9 index rows + the r8 known-gaps disposition updated; `corpus/knowledge/surfaces-r8.md` defect-2 disposition (r9 root-cause + fix) landed; census r9 comment block citing the lesson; `[PENDING: SKILL.md r9 rows]`. |
| quality | **improved** | The fix is proven correct by scope (prefix/suffix byte-identity), not asserted; the class rate is measured at two independent pre-fix batteries; the fix's necessity is anchored by the lesson's `ps0=141 ps1=0` attribution; the residual `:1322` is named with its measured wrong-grade rate instead of dropped. |
| discernment | **unchanged** | No outside spot-check of an admit/reject exists — the wave's seats are the lane per protocol. `[PARENT: bind]` |

Named debt for round 10:

1. **Production `:1322`** — same SIGPIPE shape (`printf | sed | grep -Fxq` inside `if`;
   fail-toward-wrong-grade). Fixing it changes production bytes — needs a round that owns
   production behavior change (e.g. a rates/coverage round), with the oracle re-verified.
2. A **determinism gate at admission** (r8's registered addition): run the selftest suite
   repeatedly (≥20) and require equal verdicts — r9's batteries supply the rate; the gate
   itself is `[PARENT: admission-procedure item]`.
3. Carried: frozen-behavioral drift pin (`silence-cutover-r3.md:253-254`); tmux
   per-session freshness live-proof (no tmux server); instantaneous disk-rate deferral
   (measured grounds, `surfaces-r8.md` §1); row-6 report-body presence-only residual;
   blocked-attempt receipt-binding and role-routing debts (`SCORECARD.md:128-131`);
   memory thresholds remain labeled-local.

`[PARENT: bind the integration commit and round-count; re-run `bash tools/mori-census.sh
--selftest` (expect 56/56 exit 0), `bash tools/mori-silence-cases.sh` (expect 28/28 exit 0;
oracle sha must equal `448f7723…`), the live census, and a ≥20-run determinism battery at
the final bytes; if the final census SHA moved past `1c49238a…`, re-verify this draft's
scope proof against the final bytes.]`