# mori-shokunin — corpus

## Coverage map

| Note | Holds | Sources |
|---|---|---|
| `knowledge/observability-census-r1.md` | the six census surfaces, the live receipt, and the finding-id compare contract | `tools/mori-census.sh`, live run 2026-10-15 |
| `knowledge/observability-surfaces-r2.md` | one note per surface family (7, incl. tmux) with Measures/Status/Gaps + six measured census defects | round-2 wave, 2026-10-15 |
| `knowledge/silence-grading-r2.md` | launch-aware, authorship-aware silence-grading decision table with proven/proposed labels (implemented by census r2 — see the cutover note) | round-2 wave, derived from `lane-silence-r2.md` |
| `knowledge/progressing-weak-r2.md` | authorship discrimination proof (extractable 10-case check, 10/10) + named deferral preconditions | round-2 wave |
| `knowledge/silence-cutover-r3.md` | the r3 cutover receipt: spec-row map for census r2 `fe22a14f…`, named deltas, `:517`/`:283` hardening, selftest 25/25, frozen-oracle re-baseline 25/27 per case | round-3 wave, 2026-10-15 |
| `knowledge/verdict-machine-r4.md` | the r4 verdict machine at oracle `be0e28b8…` / census `af2d4e79…`: the matcher defect and its `want_match` fix, the sniffer channels and the named order-replay residual, the `:227` rc-gate, per-anchor-round close tracking, final tallies | round-4 wave, 2026-10-15 |
| `knowledge/verdict-machine-r5.md` | the r5 run-order close at oracle `7143ccc2…` / census `af2d4e79…` (frozen): seeded shuffle + per-run nonce, the enumerated attack-class tallies, and the residual seed channels R1–R4 | round-5 wave, 2026-10-15 |
| `knowledge/verdict-machine-r6.md` | the r6 verdict machine at oracle `3307761a…` / census `af2d4e79…` (frozen): the r5 stdout-backchannel (fd/1 header + pinned environ) and naive content-keyed classes closed — header printed only after the case loop, pins scrubbed from the exec-time environ by a one-time self re-exec, per-run salt woven into fixture content — with the attack tallies and the two named residuals (full-grammar normalizing memorizer; surviving-ancestor pin) | round-6 wave, 2026-10-15 |
| `knowledge/surfaces-r7.md` | the r7 closure of the four r2 surface Gaps (tmux relevance, memory pressure, disk write-rate, `state_rounds` values): per-gap probe design, hermetic proofs + live rows, named limits, and the additive-only oracle re-pin at census `c7c3569b…` / oracle `448f7723…` | round-7 wave, 2026-10-15 |
| `knowledge/surfaces-r8.md` | the r8 disposition of the four r7 residuals — instantaneous disk write-rate deferral now carrying its measured cost (the 50 ms condition fails), timeout-bounded tmux per-session freshness, `*.round` symlink/dir reason codes, memory-probe residuals measured — plus the sampling-cost adjudication, the open items, and the pinned pair census `390ab9cd…` / oracle `448f7723…` (no re-baseline needed) | round-8 wave, 2026-10-15 |
| `knowledge/selftest-flake-r9.md` | the r9 selftest-determinism close: the live-pipe SIGPIPE race in the harness's `printf`-into-`grep -qE` assertions under `pipefail` (rc 141 read as "missing match"), its mechanism replays (13 300 trials → 2 real rc=141 fires; the fixed form 0/2 000) and git archaeology (present since the r1 landing, not a regression), the capture-file fix at all five harness sites (`:1771`/`:1773`/`:1779`/`:1783`/`:1809` at r5) with `+21/−7` hunks confined to `run_selftest()`, the 50-run battery evidence (pre-fix 10/10; arm A 20/20; arm B 20/20 under 4 CPU hogs) at census `1c49238a…` (a revision of `census-r5`), the byte-frozen oracle `448f7723…` held at 28/28, and the named same-class production debt `:1322` | round-9 wave, 2026-10-15 |
| `knowledge/drift-pin-r10.md` | the r10 drift pin at the **settled** census `d7710981…` (revision of `census-r5` distinguished by SHA; `+475/−36`, deletions confined to the usage text, the selftest runner and `main()` — no `run_census`/`emit_*` edit): `--pin` writes a normalized full-output baseline whose header records `census_sha256`, `pinned_ts` and the declared `volatile_fields` list (six special rules + `DRIFT_COUNTER_KEYS`, `:1636-1647`; the pin exits 0 whatever the census's roll is); `--drift` compares behaviorally (`MORI_DRIFT: none` exit 0 / named changed non-volatile fields incl. `-FINDING:<id>`/`+key`/`output-order`/`volatile_fields` exit 1 / missing-unreadable-malformed exit 2); the adopted lane baseline `evidence/baseline-r10-20261015T2231Z.json` (sha `0993b235…`, pinned at the settled `d7710981…` bytes; supersedes the round's interim `…T2210Z` file, deleted during receipt regeneration); the over-mask blind spots (counter magnitudes read `none` by construction; ≈47% of the schema sits in the counter class) and the under-mask env caveat (no `MORI_*` env recorded); and the per-round admission ritual (pin on admit, drift first, re-pin as a recorded act with a reason) | round-10 wave, 2026-10-15 |
| `lessons/2026-10-15-errexit-pipefail-silent-crash.md` | the pipefail silent-crash class (rc 1 collides with DRIFT, no verdict line); `:517`/`:283` hardened (r3), `:227` rc-gated (r4, `verdict-machine-r4.md` §3) | round-3 wave, `/tmp` canaries |
| `lessons/2026-10-15-forgeable-oracle-visible-fixtures.md` | the forgeable-oracle class: visible case identity + a matcher taking expanded alternation literally let a no-logic census reach the ceiling (27/27); r4 opaque case dirs drop the same sniffer to 1/28 | round-4 wave, `/tmp` canaries |
| `lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md` | the r5 lesson: the seeded shuffle + per-run nonce close the enumerated replay classes, and the two forgers that still reach 28/28 (content memorizer; `/proc` run-header leak), with countermeasures | round-5 wave, `/tmp` canaries |
| `lessons/2026-10-15-run-secret-timing-and-content-freshness-limits.md` | the r6 lesson: when a run secret is emitted is part of the secret (timing), and freshness woven into fixture content re-prices memorization rather than closing it — the pattern-normalizing memorizer still reaches 28/28; fingerprint size drift as a derived component | round-6 wave, `/tmp` canaries |
| `lessons/2026-10-15-probe-pricing-dwell-bounds-filter-drop.md` | the r8 lesson: a deferred probe's four prices — the counter's found-ness (an unfound counter reads `0 B/s`), marginal wall time (resolvable only when the instrument's noise is under budget; serial +212 ms vs overlapped 0 ms), the enforceable vs nominal bound (`timeout 0.3` bound at 1510 ms against a SIGTERM-ignoring peer; `-k 1 2` → rc 137), and an enumeration filter's drop set (a count means only what survived the filter) | round-8 wave, `/tmp` canaries |
| `lessons/2026-10-15-selftest-grep-sigpipe-race.md` | the r9 lesson: under `pipefail` a producer-piped `grep -q` assertion's rc answers "did every element exit 0", not "did the consumer match" — grep exited 0 while the producer died of SIGPIPE (141); construct sweep, `PIPESTATUS` attribution, strace, the production-shaped 3-stage variant, and the here-string countermeasure (0 misses) | round-9 wave, `/tmp` canaries |
| `lessons/2026-10-15-volatile-contract-behavioral-baselines.md` | the r10 lesson: a behavioral baseline is (raw artifact) + (explicit per-field volatile set) + (derivation window/host) — measured live churn (79 field tokens, 6 churning in 72 s, 32/33 lines; `segfault=` 104→225 over ~69 min; `mem_peak` + anchor moved within ~7 min), why line-granularity masking is vacuous (32/33 lines carry a volatile token) and field-granularity keeps detection power, the count-only change behind an existing finding id reading `none` by construction (37/79 tokens in the counter class), the exit-2 third value for absence, and the re-pin discipline (never to silence red) | round-10 wave, `/tmp` canaries |
| `knowledge/audit-r11.md` | the round-11 capstone audit of evidence/receipt coverage, current-byte re-executions, consolidated defects, and carried debt | committed round-2–10 reports and receipts; `tools/mori-census.sh`; `tools/mori-silence-cases.sh`; `SCORECARD.md`; `LOG.md` |
| `knowledge/lane-silence-r2.md` | launch-anchored, authorship-aware silence-grading inputs, states, decision order, and evidence-status limits | `PROTOCOL.md`; `scripts/shokunin-watchdog.sh`; `.ufo/watchdog.log`; `tools/mori-census.sh`; round-2 live-before receipt |
| `lessons/2026-10-15-free-lunch-measurements-counter-baselines.md` | the one-shot gate's measurement-cost rule: use source-maintained aggregates, price added dwell, and anchor cumulative counters | kernel PSI docs; `/proc/pressure/*`; cgroup `memory.pressure`; `/proc/diskstats`; `/proc/uptime`; `tools/mori-census.sh` |
| `lessons/2026-10-15-oracle-honesty-crash-masking.md` | setup-crash masking and genuine fixture repair can yield the same tally; pre-register gradients and assert fixture preconditions | `tools/mori-silence-cases.sh`; round-2 fixture/oracle evidence; mutant and read-only canaries |
| `lessons/2026-10-15-settle-evidence-references-with-artifacts.md` | resolve active recipes against delivered replacement artifacts and record what replacements do not verify retroactively | `LOG.md:477-500`; round-10 report; evidence index; committed baseline and pin receipt; `tools/mori-census.sh --drift` |
| `knowledge/oom-kill-counter-kernel-only-r12.md` | `memory.events`/`.local` and `/proc/vmstat` `oom_kill` move only at the kernel victim site (v7.2 `oom_kill.c:935-936`); userspace killers move neither — `oom_kill=0` is "no kernel OOM kills", not "no memory kills"; tsukuroi overlap cited | S002, S003, S004, S007, S011, S016 (`SOURCES.md`); host counts 2026-10-19 |
| `knowledge/kill-classes-by-message-id-r12.md` | kill/OOM journal classes counted by catalog `MESSAGE_ID` (`fe6faa94…`, `d989611b…`, `fc2e22bc…`) with non-`MESSAGE` output fields; notice ≠ kill or unique victim — the historical 5/7/9 one-boot samples are **not MESSAGE-free kernel kills**: 5 are `--grep`-selected kernel `Killed process` text matches and 7 user + 9 system are catalog-ID notice records; scopes never summed | S003, S013, S014, S015; catalog-ID counts + MESSAGE-selected historical samples 2026-10-19 |
| `knowledge/kernel-oom-line-attribution-r12.md` | the kernel `oom-kill:constraint=…task_memcg=…pid=…uid=…` record as event-time attribution (5 retained samples, 2026-10-18, MESSAGE-selected by `--grep` — historical text matches, not a structured MESSAGE-free victim count); token-only output, never a `MESSAGE` echo; fleet attribution [UNKNOWN] without a validated `task_memcg` token | S003, S004, S014, S015 |
| `knowledge/userspace-oom-killers-r12.md` | systemd-oomd (`user.oomd_ooms`/`user.oomd_kill` xattrs, D-Bus `Killed`, `d989611b…`) and earlyoom kill paths; on 2026-10-19 both killer services were inactive here → `unavailable (inactive)`, never 0; the 2026-10-22 reading (earlyoom 1.9.0 active and enabled, systemd-oomd inactive and disabled) is `knowledge/userspace-oom-killers-r26.md`; OS/unit state is tsukuroi's | S002, S003, S007, S011, S012, S013, S016 |
| `knowledge/userspace-oom-killers-r26.md` | earlyoom 1.9.0 as this host's running userspace killer: its two-condition act rule (available memory and free swap both at or below the limits; SIGTERM at the first pair, SIGKILL at the second), the startup lines that state its limits, the eight message prefixes stable enough to count, and why its kills never move kernel `oom_kill` counters; systemd-oomd inactive with the captured units `auto` (sibling cited); read by `tools/mori-oom-killers.py`; supersedes the r12 host-state reading | S114–S126 (range corrected in round 27, routed D5; was "S114–S125"); `.ufo/waves/round-26/capture/capture.txt`, `capture-boots.txt` |
| `knowledge/oom-victim-selection-r27.md` | how earlyoom 1.9.0 and the Linux 7.2 kernel choose an OOM victim (`oom_score`, `oom_score_adj` scaled by memory size, `--prefer`/`--avoid` ±300, `--sort-by-rss`, `memory.oom.group`), the fleet's `oom_score_adj` 200 traced to systemd's per-user manager (100 + 100) and not the harness, the process classes of earlyoom's 39 boot -1 sends, and what fleet records cannot attribute | S148, S149, S150, S130, S151, S132, S142 (S148–S151 supersede the round-27 rows, round 28); `.ufo/waves/round-27/evidence/oom-score-classes.txt`, `boot-send-classes.txt` |
| `knowledge/roster-truth-r12.md` | the three lane-roster sets (census default 9, `shokunin.conf` 20, `.ufo/state` 21 → union 23) and the r12 census roster derivation (`roster_source=`, `ROSTER_SET_MISMATCH` info; conf rows read only inside `LANES="…"`) at census `3da5b098…` | `shokunin.conf`, `scripts/shokunin-watchdog.sh:14`, `PROTOCOL-APPENDIX.md` 'Lane universe', `evidence/roster-r12-*` |
| `lessons/round-12.md` | round-12 lesson: `## Mistakes` (M1–M26 mined from the lane's own errata, each with captured-by), pointer re-verification, and `## Gate` (candidates, admits, rejects with reasons, SOURCES access records) | LOG round-12 entries; dossiers `kaika-w1/mori-{state,art}.md` |
| `knowledge/structured-journal-scopes-r13.md` | independently scoped MESSAGE-free catalog-ID record counts, structured unit results and numeric signal-11 records; client-set IDs are not authenticated kills; FR1 notice/result plane advances without claiming kernel victim attribution | S013/S014/S015 reopened, S035/S036 added round 13; `.ufo/waves/round-13/evidence/live-measurement.json` |
| `knowledge/verdict-contract-r13.md` | capture-safe long-history author membership and strict single final-verdict grammar/rc validation; tested invalid wrappers, not universal forgery resistance | S031 reopened round 13; audit-r11 F01/F02; round-13 behavioral receipts |
| `knowledge/journal-alarm-routing-r14.md` | measured structured OOM/legacy signal alarms and fleet/non-fleet/unattributed subject triage; one OOM critical line with separate scope/path counters, not a victim count; `UNIT`/`USER_UNIT` name-token rule, not membership proof; cgroup-local is not a substitute and unavailable is not an alarm; six named acceptance failures 6 → 0 at 5601d12, 12/12 all-zero live counter parity, nonzero fixture parity retained | S002/S013/S015/S035/S036/S037/S038; `.ufo/waves/round-14/evidence/c1-measurement.json`; measured receipt appended to the note |
| `knowledge/journal-positive-evidence-r15.md` | mixed-class positive preservation for the journal alarms: per-scope `positive_kernel_oom` / `positive_unit_oom` / `positive_unit_signal` / `positive_process_sigkill` count only object records with scalar matching `MESSAGE_ID` and scalar current `_BOOT_ID` (unit result exactly `oom-kill`/`signal`; process exactly `killed`+status 9) from the same single captured stream, so a valid current-boot witness still raises the one critical OOM line or the one user signal WARN while any malformed/nonmatching/foreign-boot neighbour leaves the raw aggregate/split class `unavailable:<reason>`; raw counters and the INFO routing partition keep authority, positives are additive evidence — decision table only, not full parsing/completeness, authenticated ids, unique victims or fleet membership | S014/S015/S037/S038 reopened round 15 (`corpus/SOURCES.md` used-by updated); no live journal read, census run or tally measured by this note |
| `knowledge/journal-cursor-window-r16.md` | exact-anchor, same-boot, MESSAGE-free new-since-anchor window: the first parsed record must byte-match the anchor cursor and `_BOOT_ID` and is dropped; later records must be same-boot scalar-cursor objects; byte-mismatch false unavailable under aliases is accepted; no dedup, no completeness, no unique victims; rotation/vacuum and cross-boot stay unavailable; `-q`-hidden inaccessible-journal partial reads are not detected — an OK window may be partial — [UNKNOWN] | S014/S015/S039/S040; host systemd 261.2-1 `--help`/`man` checks only, no journal read |
| `knowledge/earlyoom-invocation-scope-r30.md` | which current-boot earlyoom invocation a send line belongs to: version-line segmentation, the systemd active-enter bound, earlier-invocation and dry-run separation, incomplete-scope limits; added round 31 (routed D5: the round-30 entry had no map row) | S118–S120, S122, S154–S160; `.ufo/waves/round-30/rule-text.md`; `tools/fixtures/mori-oom-killers/cases-a2.json` |
| `knowledge/source-drift-r36.md` | the source-drift byte probe: per-state classification semantics, the dated nine-row drifted enumeration with open-time shas, and the reader-action classes; `drifted` is a representation difference, never a freshness verdict | `tools/mori-source-drift.py`; S205; `.ufo/waves/round-36/evidence/drift-live-r36.txt` |
| `knowledge/source-drift-hardening-r37.md` | the probe's two hardening policies — a 4 MiB bounded read and a post-redirect public-destination check — with their named selftest arms, mutation kills, live run and disclosed limits | S221–S225; `tools/mori-source-drift.py`; `.ufo/waves/round-37/count-c2.py` |
| `knowledge/source-drift-content-anchor-r38.md` | the content half of the drift-corpus binding: named `anchor:` code strings that must resolve in the probe's bytes, capability paths that must resolve from the repo root, one named drifted row per summary count, and a named-row selftest arm killed by its own mutation; three fabricated token witnesses rejected | S205; S221–S226; `.ufo/waves/round-38/count-c4.py`; `.ufo/waves/round-38/evidence/c4-after.txt` |
| `knowledge/containment-timed-supersede-r38.md` | containment decided on the resolved canonical path (S226), and the timed supersede reading: a disposition postdates the edit or the gate lists it in `stale_supersede`; S069's disposition at the round-38 tip | S226; S069; `tools/mori-sources-appendonly.py`; `.ufo/waves/round-38/evidence/gate-after.txt` |
| `knowledge/conform-bindings-r41.md` | source-ordered timeout binding inventory for `Assign`/`AnnAssign`, `NamedExpr`, tuple/list targets, and loop/with targets; multiple or unsupported bindings fail closed within a named static subset | S230/S231; `.ufo/waves/round-41/conform.py`; `.ufo/waves/round-41/evidence/control-before.txt` |
| `knowledge/census-cgroup-levels-r45.md` | the census's `SURFACE cgroup` row prints one OOM count from the user slice's hierarchical `memory.events` and a second named `local_oom_kill` filled from the slice's `memory.events.local` or, on the fallback, from the session service's hierarchical `memory.events`, while the kernel text defines `.local` as not hierarchical (`:1518-1519`); FR1 (a count whose counting scope is unnamed cannot be attributed to a cgroup) and FR12 (the one-shot pressure surface carried by the same row); boundary: no census change, no cgroup v1, no remediation, and no FR1 or FR12 advance — FR12's resident-watcher boundary stands | S473; `tools/mori-census.sh:1705-1712,1862`; `.ufo/waves/round-45/assimilation/opened/cgroup-v2.rst.src` |

## Known gaps

- One note per surface family: **landed round 2** — `knowledge/observability-surfaces-r2.md`
  (seven surfaces incl. tmux; the r1 "six surfaces" framing is superseded) together with
  `knowledge/silence-grading-r2.md` (decision table) and
  `knowledge/progressing-weak-r2.md` (authorship discrimination check).
- `progressing-weak`: the discrimination proof **landed round 2** (runnable check,
  10/10); the r2 grading **landed round 3 in census r2** (bullet below). The
  parent-owned admission/receipt binding is the one spec precondition still open
  (`knowledge/silence-grading-r2.md:229-230`).
- **Silence probe cutover (landed round 3):** `tools/mori-census.sh` r2
  (`VERSION=census-r2`, sha `fe22a14f…`) implements the
  `knowledge/silence-grading-r2.md` contract — launch-anchored, authorship-aware
  per-lane rows (`silent` / `progressing` / `progressing-weak` / `young` /
  `not-open` / `unavailable`), the closure predicate, `LANE_SILENT` only for row D,
  `unavailable` ≠ unhealthy, strict age gate, no fixture branching in the silence
  path. Receipts under `corpus/evidence/cutover-r3-*`; spec-row map and named
  deltas in `knowledge/silence-cutover-r3.md`. The r4 oracle `be0e28b8…`
  supersedes the frozen `505a7504…`, and the r5 oracle `7143ccc2…` supersedes
  that in turn (anti-sniff round-5 bullet below); the r6 working-tree revision
  `3307761a…` supersedes the r5 bytes in turn (anti-sniff round-6 bullet below).
- **Oracle tally (round-3 residual, closed in round 4):** the frozen oracle's
  matcher (`tools/mori-silence-cases.sh:362-365` at `505a7504…`) compared the
  `|`-joined want string literally, pinning the honest census at `matched=25
  total=27` exit 1; the fix is the exact-string `want_match()` helper
  (`be0e28b8…:342-348`, call `:389`). At oracle `be0e28b8…` / census `af2d4e79…`:
  `MORI_SILENCE_CASES: matched=28 total=28`, exit 0 — the 27 case ids and
  want-strings byte-identical to the frozen revision, plus the new
  `shape-invariance` case (`corpus/evidence/verdict-r4-20261015T173551Z-oracle.log`;
  mechanism in `knowledge/verdict-machine-r4.md` §1).
- **`:227` pipefail instance (closed in round 4):** the watchdog `state_n` pipeline
  is rc-gated at census `af2d4e79…` (`cap find` + `state_read` branch, `:233-241`,
  `:256-260`): an unreadable `.ufo/state` now renders `state_rounds=unavailable
  state_unreadable=1` in a full verdict (at the r2 bytes: rc 1, header only, 0
  verdict lines). Receipt
  `corpus/evidence/verdict-r4-20261015T173551Z-canary227.log`; class in
  `lessons/2026-10-15-errexit-pipefail-silent-crash.md`.
- **Round-4 verdict machine (oracle `be0e28b8…`, census `af2d4e79…` =
  `VERSION=census-r3`):** all four registered defects addressed — matcher, `:227`,
  the fixture-identity leak, and close tracking keyed per anchor round (a later
  `complete … round=5` no longer erases a closed r7 anchor; `:653-661`). selftest
  25 → 30 cases, `PASS (30 cases, 30 passed, 0 failed)` exit 0
  (`…-selftest.log`); live census honest: `MORI_CENSUS: DRIFT (findings=15
  drift=14 unavailable=1 surfaces=7)` exit 1, 9/9 roster lanes `progressing`,
  zero `LANE_SILENT`, the 1 `unavailable` is tmux (`…-live.log`).
- **Anti-sniff (round 4): case-id channel closed, order-replay residual named.**
  Opaque `mktemp` case dirs, no `MORI_FIXTURE` export and the `shape-invariance`
  case drop the verbatim round-3 case-id sniffer from `matched=27 total=27`
  exit 0 to `matched=1 total=28` exit 1 (`…-sniffer-v2.log`). **At the r4 oracle
  only:** an invocation-order replay that agreed with itself on both shape runs
  still reached `28/28` exit 0 (`knowledge/verdict-machine-r4.md` §2.4); the r5
  oracle's seeded shuffle drops the same replay class to `0/28` exit 1 (next
  bullet).
- **Anti-sniff (round 5): the enumerated position-keyed replay classes fail at
  oracle `7143ccc2…` (census frozen `af2d4e79…`); the residual seed channels
  stay named.** The 28 cases run in a seeded-shuffled order
  (Fisher-Yates/xorshift32; run header `SHUFFLE_SEED=` / `RUN_NONCE=` /
  `CASE_ORDER=`; same seed ⇒ same order; `MORI_SHUFFLE_SEED` / `MORI_RUN_NONCE`
  pins) and every case requires the current run's nonce token (`nonce-<N>`,
  echoed by the frozen census's disk row) in its output. Receipts
  `corpus/evidence/order-r5-20261015T180431Z-*.log`: the round-4 forgers drop
  `28/28` exit 0 (r4 snapshot) → `0/28` exit 1; a live-nonce echo with a fixed
  positional table scores `6/28` exit 1; stale/recorded replay `0/28` exit 1;
  honest census unaffected — `28/28` exit 0 at three seeds with byte-identical
  per-case grade tuples (sha `a70af583…`). **Not closed — "cannot fake a pass"
  is not claimed:** a seed-reading attacker reaches `28/28` exit 0 whenever it
  can reach the seed — `/proc/<ppid>/environ` on a `MORI_SHUFFLE_SEED`-pinned
  run (R1), or the oracle's own captured stdout (`CASE_ORDER=` in a
  regular-file capture, i.e. the `> log` receipt pattern; pipe captures do not
  expose it, 0–1/28 — R2); the nonce alone is echo-able by design and gates
  staleness only (R3); a fixture-content memorizer still reaches `28/28` (R4,
  carried from round 4) (`knowledge/verdict-machine-r5.md` §4;
  `lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md`). The
  oracle-reachable seed channels (R1/R2) and the naive content memorizer (R4)
  are closed at the r6 oracle `3307761a…`; the surviving-ancestor pin and the
  full-grammar normalizer stay named (round-6 bullet below).
- **Anti-sniff (round 6): the r5 stdout-backchannel and content-keyed classes
  closed at oracle `3307761a…` (census frozen `af2d4e79…`); two residuals stay
  named.** The run header (`SHUFFLE_SEED=` / `RUN_NONCE=` / `CASE_ORDER=`) now
  prints only **after** the case loop (`tools/mori-silence-cases.sh:1066-1072`),
  per-case lines redact the nonce token (`:545`), and a pinned
  `MORI_SHUFFLE_SEED`/`MORI_RUN_NONCE` is scrubbed from the exec-time
  environment by a one-time self re-exec that passes the pins on a pipe fd
  (`:207-220`); every fixture's content is per-run — committed bodies and commit
  messages carry `[nonce-<N> <salt>]` (`:417`,`:419`) and the case dir gains
  salt/blob files (`:309`,`:314-315`), with four cases binding the marker into
  untracked/dirty content (`:823`,`:836`,`:899`,`:921`). Receipts
  `corpus/evidence/backchannel-r6-20261015T{190229,190453,191216}Z-*.log` (the
  `T191216Z` set binds the final sha): fd/1 `CASE_ORDER` replay `28/28` exit 0
  (r5 bytes) → `0/28` exit 1; pinned-environ reader `28/28` → `0/28`; r5-learned
  content table `28/28` → `0/28`; fresh learn-then-replay `0/28`; honest census
  unchanged — `28/28` exit 0 across shuffles, per-case tuples byte-identical
  (sha `a70af583…`). **Not closed — named residuals:** a full-grammar
  normalizing memorizer (strips both marker grammars; a bracket-only normalizer
  dies at `24/28`, the four untracked/dirty-marker cases) reaches `28/28` exit
  0, and a pin in a *surviving ancestor's* exec-time environ (wrapper-CI
  pattern) stays readable for the whole run (`knowledge/verdict-machine-r6.md`
  §4-§5; `lessons/2026-10-15-run-secret-timing-and-content-freshness-limits.md`).
- **Surface gaps closed (round 7): census `c7c3569b…` (`VERSION=census-r4`), oracle
  `448f7723…`.** All four `knowledge/observability-surfaces-r2.md` Gaps are measured
  probes now: tmux sessions classified by pane current path under the fleet root
  (`sessions= relevant= foreign= unclassified= rule=pane_cwd_under_fleet_root`;
  `TMUX_FOREIGN_SESSION` names the session); memory graded — PSI `some`/`full` avg10
  (`MEM_PRESSURE_HIGH`) and fill `current/max` or a named host-ram floor
  (`MEM_FILL_HIGH`/`MEM_AVAIL_LOW`), thresholds labeled local; disk gains a since-boot
  write average (`io_basis=since-boot io_avg_since_boot=<dev>:<rate>Bps/<uptime>s`,
  unmeasurable targets named with a reason, never 0 B/s); `state_rounds` VALUES read
  and compared with the lane's last ledger launch round (`state_rounds_max state_lag
  state_ahead state_val_unreadable`; `WATCHDOG_STATE_LAG`/`_AHEAD` info-only). Machine
  green: selftest 30 → 45, `PASS (45 cases, 45 passed, 0 failed)` exit 0; oracle
  re-pin additive-only — 8 inserted lines, 0 deletions, 28 ids/wants byte-identical —
  `matched=28 total=28` exit 0; live `DRIFT (findings=15 drift=14 unavailable=1
  surfaces=7)` exit 1; every r6 field name still present (field-set diff). Method,
  live rows and per-gap limits: `knowledge/surfaces-r7.md`; receipts
  `corpus/evidence/surfaces-r7-20261015T1948Z-*.log`.
- **Round-7 named limits:** the instantaneous disk write rate is a bounded deferral
  (precondition: measure the wall-time a second sample adds —
  `tools/mori-census.sh:48-52`); the since-boot average counts every write to the
  device, not fleet-attributable, and the second default target `/tmp` is tmpfs on
  this host (`io_avg_unavailable=`); tmux relevance is fixture-proved only (no tmux
  server live this round, so the live row keeps the r6 unavailable shape) and
  per-session freshness stays unmeasured; the three memory thresholds are local
  placeholders that **do** flip the roll; `state_cmp` can be smaller than
  `state_rounds` for a lane with no ledger launch line. Round 8 closes the two
  unmeasured items in this list (tmux freshness, the disk deferral's cost) — next
  bullet; the rest (attribution, tmpfs, the still-local memory thresholds,
  `state_cmp`) carry unchanged.
- **Surface residuals closed (round 8): census `390ab9cd…` (`VERSION=census-r5`,
  2380 lines), oracle `448f7723…` byte-unchanged — no re-baseline was needed and
  `matched=28 total=28` held at the new census bytes.** Each r7 residual is
  disposed of. Instantaneous disk write-rate **stays deferred, now
  receipt-backed**: isolated n=30 arms price the two extra `diskstats` reads at
  16 ms median / 27 ms p90 and the two-sample reads + 0.2 s dwell at min 210 /
  median 229 ms, with the minimum across the three independent isolations 208 ms
  — 4.16× the round's 50 ms bar — so the windowed rate stays unimplemented by the
  round's own condition; gate-level wall time (≥5 s drift under wave load) is
  reported unusable as a decision instrument; the disk row keeps the since-boot
  average, `warn_pct=85 crit_pct=95` untouched. tmux per-session freshness
  **implemented, timeout-bounded**: one `display-message '#{session_activity}'`
  per fleet-relevant session under `run_timeout` (`MORI_TMUX_TIMEOUT_S=2`; rc
  124 / non-integer output / probe rc≠0 / a missing `timeout` binary each yield
  `freshness=unavailable` with its reason, never `idle=0` — the missing-binary
  arm refuses the probe rather than run it unbounded), graded INFO-only against
  the labeled-local `TMUX_IDLE_WARN_S=3600` (`TMUX_SESSION_IDLE`); the row
  carries `freshness= probed= idle= freshness_unavailable= idle_warn_s=`;
  fixture-proved only (no tmux server live again this round). `*.round`
  non-regular entries are **classified with reason codes**: the state walk no
  longer filters on `-type f`, symlinks are never followed, a FIFO is classified
  and never opened, and the row splits `state_val_unreadable=` into
  `state_val_unread_reasons=file:N symlink:N dir:N other:N`
  (`WATCHDOG_STATE_ENTRY_UNREADABLE reason=symlink-not-followed|is-directory|non-regular`);
  `state_rounds` keeps its regular-file meaning so existing state dirs read
  unchanged. Memory-probe residuals are **closed for scope/live-evidence**: the
  local placeholders now sit behind a measured window (21 PSI/avail samples 3 s
  apart — `psi_some_avg10` 0.00–0.39 against 10, host avail 49–53% against the
  10% floor, i.e. 15–25× / ~4.9× away; still labeled local), the row gains
  `mem_peak`/`mem_peak_source`/`mem_peak_anchor` (anchor = scope-dir mtime; live
  slice `28812898304`), and a 108-scope `memory.max` walk (107 the literal
  `max`, 1 numeric, 0 unreadable) explains why the closed-container fill ratio
  never exists on this host. Machine green at the pair: selftest 45 → 56,
  `PASS (56 cases, 56 passed, 0 failed)` exit 0 (+11, none removed), oracle
  `matched=28 total=28` exit 0 ×2, live `DRIFT (findings=15 drift=14
  unavailable=1 surfaces=7)` exit 1, stderr 0 B; field-set diff adds exactly 9
  names on one fixture (4 live) and removes none; interleaved old-vs-new on one
  fixture +14 ms median. Open items stay named: the pre-existing unbounded-FIFO
  hang class (unpinned `MORI_DISKSTATS`/`MORI_UPTIME`) is not fixed; one of 16
  selftest runs during the write window failed intermittently (`CGROUP_OOM_KILL`
  missing-match; root-caused in round 9 as the live-pipe-grep SIGPIPE race —
  next bullet; frozen-bytes repeats green); and
  gate-level timing is not a decision instrument under load. Method, arms, open
  items: `knowledge/surfaces-r8.md`; lesson
  `lessons/2026-10-15-probe-pricing-dwell-bounds-filter-drop.md`; receipts
  `corpus/evidence/residuals-r8-20261015T2040Z-*.log` (7 logs, every one naming
  the frozen pair; the note's own pointer still says `surfaces-r8-*.log`).
- **Selftest determinism closed (round 9): census `1c49238a…` — a revision of
  `census-r5` (`:201`; same version label, distinguished by SHA) — and the oracle
  `448f7723…` byte-frozen.** The r8 flake class: under `set -euo pipefail`
  (`:194`), `printf '%s\n' "$out" | grep -qE -- "$re"` lets `grep -q` exit 0 at
  the first match while the printf producer is still writing; the producer dies
  of SIGPIPE (rc 141), `pipefail` makes that the pipeline rc, and the `|| miss=`
  guard records a false `missing match` on a random case (green on rerun). The
  fix rewrites all five harness sites (`:1771`/`:1773`/`:1779`/`:1783`/`:1809`
  at r5 numbering) to grep one capture file (`OUT_FILE`, declared `:1572`, set
  `:1585`; `check()` writes it once at `:1781`, `check_cli()` at `:1817`) — no
  live piped early-exit consumer remains in the selftest path and the `+21/−7`
  diff adds no pipe, with every hunk inside `run_selftest()` (reached only from
  the `--selftest` branch, so production probe bytes are untouched). Machine
  evidence at the new bytes: the identical `PASS (56 cases, 56 passed, 0
  failed)` exit 0 in all 50 battery runs (pre-fix 10/10; post-fix arm A 20/20
  and arm B 20/20 under 4 owned-and-killed CPU hogs); replays of the 56 real
  payload/pattern pairs fired the race 2× in 13 300 trials — real cases, match
  present — while the fixed form fired 0/2 000; a detection-power mutant still
  fails (`55/56`, exit 1). The oracle returns `matched=28 total=28` exit 0 at
  the new bytes with want-sets unchanged; live `DRIFT (findings=15 drift=14
  unavailable=1 surfaces=7)` with the 16 surface key-sets and the finding-id set
  identical to the r8 receipt run1 (`.ufo/round-9/goal-wave/measurements-ledger.md`
  after-side; a durable r9 receipt set was not yet in `corpus/evidence/` at the
  note's clock). Git
  archaeology: the idiom is as old as the harness (r1 landing `7ca17b1`), so
  this was not an r8 regression; the production silence path `:1322` carries the
  same class and stays **named debt** under this round's production byte-freeze,
  and r8's second "random case, green on rerun" cause (reading the census while
  it was still being written) stays distinguished from this class. Method,
  mechanism replays, gate recommendation: `knowledge/selftest-flake-r9.md`;
  lesson `lessons/2026-10-15-selftest-grep-sigpipe-race.md`.
- **Row-6 closure is presence + window only (spec residual):** a fresh,
  contentless committed marker satisfies it while the running driver would reject
  that shape (`knowledge/silence-grading-r2.md:191-197`). The census-output
  frozen-behavioral drift pin **landed round 10** (next bullet); this presence +
  window residual itself stays open.
- **Census drift pin landed (round 10): census `d7710981…` (still
  `VERSION=census-r5`, sha-distinguished; `+475/−36`, deletions confined to the
  usage text, the selftest runner and `main()` — no `run_census`/`emit_*` edit),
  oracle `448f7723…` byte-frozen.** `--pin <path>` runs the live census read-only,
  normalizes its full output and writes it with a header carrying `census_sha256`,
  `pinned_ts` and the declared `volatile_fields` list
  (`tools/mori-census.sh:1636-1647`); the pin exits 0 whatever the census's own
  roll is (a DRIFT host still pins), write failure → exit 2. `--drift <path>`
  re-runs, re-normalizes with the current list and byte-compares the canonical
  block: equal → `MORI_DRIFT: none` exit 0; changed non-volatile fields are named
  (changed keys, `-FINDING:<id>`/`+FINDING:<id>`, `output-order`, `volatile_fields`)
  exit 1; baseline missing/unreadable/malformed → exit 2. The adopted lane baseline
  `corpus/evidence/baseline-r10-20261015T2231Z.json` (sha `0993b235…`; pinned
  `2026-10-15T22:26:29Z` at the settled census bytes; `mori-drift-baseline v1` text despite the
  `.json` suffix) reads `MORI_DRIFT: none`; selftest 56 → 66
  (10 pin/drift arms, `:2722-2798`), `PASS (66 cases, 66 passed, 0 failed)` exit 0;
  the no-flag output is byte-unchanged (no production-path hunk). Named blind
  spots: counter magnitudes inside an existing finding id (a count-only change
  reads `none` by construction — ≈47% of the schema sits in the counter class),
  watermarks/gauges, `*_epoch`/`round=`, `example=`, `script_sha256` and the
  verdict tallies; the baseline records no env, so pin and drift must share the
  invocation (a `MORI_*` override difference reports as drift, measured). Re-pin is
  a recorded act with a reason, never a way to make red green. Method, masking
  risks, ritual: `knowledge/drift-pin-r10.md`; churn/masking lesson:
  `lessons/2026-10-15-volatile-contract-behavioral-baselines.md`; the
  receipts-writer's committed drift-leg set lands under `corpus/evidence/` as
  `pin-r10-*.log` (at this README's clock the baseline is the round's only r10
  evidence file in place).

- **Journal scope correction (round 13, qualified in round 14):** the old
  user-only/text-signature census is superseded by independently labeled
  user/system structured journal record counts
  (`knowledge/structured-journal-scopes-r13.md`). The r12 historical samples
  indexed above are **not** MESSAGE-free kernel kills: their five kernel records
  are `--grep`-selected over journal `MESSAGE` text and the 7/9 user/system
  records are catalog-ID notices, so none is a current measurement or a
  unique-victim count. Structured process-result SIGKILL and unit-failure records
  preserve the supported class paths; arbitrary unreported signal paths and
  kernel victim attribution remain unmeasured (FR1). **The r13 cutover is
  rejected-harmed, not admitted:** it demoted the OOM notice classes to INFO,
  away from the critical `OOM_KILL_JOURNAL`/DRIFT behavior, and collapsed the
  fleet/non-fleet `UNIT_FAILURE_*` split together with its tsukuroi owner routing
  (`lessons/round-13-verifier-spotcheck.md`, routed defects 1–2 and 6). Round
  14's C1 claim retains the scoped counts and restores the alarm and routing
  over structured journal metadata — one global `OOM_KILL_JOURNAL` critical
  alarm (DRIFT) per census with separate, never-summed notice/unit counters and
  no unique-victim claim; fleet `UNIT_FAILURE_JOURNAL` and non-fleet
  `UNIT_FAILURE_OUT_OF_SCOPE` (owner tsukuroi) split on `UNIT=`/`USER_UNIT=`
  subject presence under a named heuristic rule
  (`classification_rule=unit-name-token`, not membership proof), while
  unattributed records stay `UNIT_FAILURE_UNATTRIBUTED_JOURNAL` info (owner
  unresolved), never invented non-fleet membership. L1 measured the repair at
  `5601d12`: six named alarm/routing acceptance arms fail **6 → 0** and the
  complete gate passes 44 assertions (43 cases plus frozen-red control).
  `.ufo/waves/round-14/evidence/c1-measurement.json` records the command and
  independent positive scoped-counter parity; live 12/12 cells were all zero.
  The source set, signal warning restoration, trust limits and measured receipt
  are in `knowledge/journal-alarm-routing-r14.md`.

- **Mixed-class positive preservation (round 15, decision table):** the r14 residual
  `R14_SEC_DUP_MSGID_MIXED` is the failure mode this contract narrows
  (`knowledge/journal-positive-evidence-r15.md`). A class total is all-or-nothing, but an
  independently valid current-boot object record is a separate existential claim: the four
  per-scope `positive_kernel_oom` / `positive_unit_oom` / `positive_unit_signal` /
  `positive_process_sigkill` tokens preserve the existing critical `OOM_KILL_JOURNAL` line or
  user `KILL_SIGNAL_JOURNAL` WARN when an adjacent malformed, nonmatching or foreign-boot record
  makes the aggregate class unavailable. Raw class/split counts keep their
  `unavailable:<reason>` values and stay authoritative; positives are never written into a raw
  slot, never summed across scopes or sources, and never repair the aggregate-only
  fleet/non-fleet/unattributed INFO partition. **This is FR1 failure-mode coverage only — not
  full parsing, not completeness, not authenticated `MESSAGE_ID`s, and not unique victims;** a
  stream-level parse/capture failure or an identity-invalid sole positive still loses the alarm,
  and arbitrary malformed JSON is not repaired. No measurement is claimed here: the note
  predicts no tally and L1 owns the delivered census and gate bytes.

## Frontier

| id | frontier | first evidence | boundary |
|---|---|---|---|
| FR1 | Kernel OOM event-time attribution and fleet correlation | `knowledge/kernel-oom-line-attribution-r12.md:10-16`; `knowledge/audit-r11.md:203-204` | Structured system-journal notice records advance round 13; kernel victim/summary token validation and fleet task correlation remain frontier. Catalog-ID records are not authenticated unique kills. Round 15 adds mixed-class failure-mode coverage only: a validated current-boot positive record can still fire the alarm while the aggregate class is unavailable, which is alarm preservation, not full parsing and not completeness. |
| FR2 | Quota/EDQUOT observability | `knowledge/audit-r11.md:218-222` | `df` capacity percentages cannot detect quota exhaustion; observe and report only, never change quota state. |
| FR3 | Authoritative wave settlement and emptied-by-hygiene versus never-written | `knowledge/audit-r11.md:202`; `../../kumitate-shokunin/corpus/knowledge/swarm-wave-lifecycle.md:28-34,91-120` | Mori reports filesystem shape; kumitate owns orchestration/result semantics; `empty` alone does not prove never-written, and receipt review stays offline. |
| FR4 | Driver-state versus MANIFEST versus lane-LOG round reconciliation | `../../fleet-ledger/.ufo/waves/kaika-w1/mori-state.md:31,190`; `knowledge/observability-surfaces-r2.md:118-125` | Census compares driver state with watchdog launch lines only; it does not establish MANIFEST admission or lane-LOG agreement. |
| FR5 | Watchdog daemon identity and degraded-pgrep visibility | `knowledge/audit-r11.md:200-201` | An unavailable pid probe is not absence, and argv-substring matches do not establish daemon identity. Round 33: under the hyaku inline driver no daemon runs, so `WATCHDOG_ABSENT` fires every round; reading the driver's `launch`/`complete` lines in `.ufo/watchdog.log` as a second liveness source is open coverage ground (`lessons/round-33.md` Round-32 repair §6). |
| FR6 | Instantaneous disk write-rate | `knowledge/surfaces-r8.md:75-89` | Keep the since-boot average distinct; a two-sample rate stays deferred until its added latency meets the stated budget. Round 33 adds the sourced reading rules (`knowledge/disk-write-rate-r33.md`, S180–S190); still frontier: a two-sample census arm, and the device-mapper double count, observed on this host but not sourced. |
| FR7 | Live tmux relevance/freshness arm | `knowledge/surfaces-r8.md:120-124` | Host arm is fixture-proved only; do not create or steer sessions, and unavailable is not unhealthy. |
| FR8 | Alert-threshold calibration | `knowledge/audit-r11.md:205` | Thresholds remain labeled local; a quiet window is not a workload distribution or an alert-cost rule. |
| FR9 | Durable fixture evidence | `knowledge/audit-r11.md:41-46` | Scratch paths and unreconstructable fingerprints are not durable evidence; retain a reproducible fixture generator and digest before making replay claims. |
| FR10 | Userspace OOM killers (systemd-oomd and earlyoom) | `knowledge/userspace-oom-killers-r12.md:10-15`; `knowledge/userspace-oom-killers-r26.md` | Inactive killers are unavailable, not zero; `memory.events oom_kill` does not cover every userspace kill; never enable or tune a killer. Round 26 moves the one-shot earlyoom/oomd read to Core (`tools/mori-oom-killers.py`); still frontier: earlier invocations of an active earlyoom in the same boot (reported, not a verdict input), previous boots, oomd cgroup xattrs and D-Bus signals, and fleet attribution of a victim. Round 27 adds the victim-selection knowledge (`knowledge/oom-victim-selection-r27.md`); still frontier: which `omp` process an `omp`-class send hit, and seat-level attribution. |
| FR11 | New-since-anchor journal record/notice subsets via cursors | `SOURCES.md:20-21`; `knowledge/journal-cursor-window-r16.md` | Cursor queries stay read-only and anchor-scoped. Round 16 advances FR11 only to an exact-retained, same-boot window: the first record must byte-match the anchor cursor and `_BOOT_ID`; a byte mismatch can be a false unavailable under cursor aliases and is never proof of vacuum; no dedup or completeness claim. Counts are record/notice subsets, not kill counts. [UNKNOWN] behavior after cursor rotation/vacuum, unreadable later journal files under `-q` (not detected; an OK window may be partial), and ordering across boots remains open. |
| FR12 | Event-driven pressure and CPU/IRQ PSI | `SOURCES.md:7-8,16`; `lessons/2026-10-15-free-lunch-measurements-counter-baselines.md:57-73` | A PSI trigger watcher is resident, not a one-shot census probe; system CPU `full=0` is not evidence of no stall. |
| FR13 | eBPF kill/OOM tracing | `SOURCES.md:11-12,23-26` | Privilege and version matter; a resident tracer is outside the census, so retain this as knowledge/frontier only. |
| FR14 | Agent-workload telemetry | `SOURCES.md:28-32` | Mori is consume-only; telemetry emission belongs to the emitting lanes and orchestration. |

## Known gaps — round-12 note

The existing Known gaps list mixes closed history with open gaps. Open items now live in `## Frontier`; the historical list above is unchanged.

## Round-17 coverage additions and corrections

| Ground | Entry | Bounded advance |
|---|---|---|
| FR14 consume-only agent telemetry | `knowledge/seat-terminal-status-r17.md` | Version-3 transcript terminal-at-scan classes, bounded field-limited observation; aged errors can resume, prefixes are names, totals are observations not incidents |
| Lane-silence VCS provenance | `knowledge/jj-branch-anchor-r17.md` | Local branch rather than bare HEAD for jj-colocated progress; warn on off-branch HEAD or ambient author, no VCS repair or remote-publication proof |
| Fleet-root blind-sweep calibration | `lessons/round-17.md#M1` | Byte-exact r16 filename-only misroot witness; no-pathspec filename-or-content detection, candidate ownership reviewed before moving anything |

FR14 emission and authoritative orchestration semantics remain kumitate-owned;
schema drift, concurrent scan consistency and permanent termination remain frontier.
The round-16 window's pending wording is superseded by
`lessons/round-16-verifier-spotcheck.md:9–17`, only at its exact-anchor, anchor-boot
scope. The r16 host-version statement is historical261.2-1, not today's262-1
package-log state (`knowledge/journal-cursor-window-r16.md` appended correction).
R10 drift pin remains red debt without a re-pin. Package transaction detections
are handed to tsukuroi/operator, not absorbed as OS state ownership.


Round-17 precision superseding the r16 coverage-map row's “no journal read”:
that phrase described the draft seat, not the delivered lane capability. L1
later ran one bounded user and one bounded system journal query at the r16
measured revision; both were anchor-only with zero records after anchor
(`knowledge/journal-cursor-window-r16.md:127–136`, r16 live receipts).
This proves path reachability, not no events, complete access or positive load.
The r16 host version remains historical 261.2-1; primary version rows are
`lessons/round-16.md:69,73,153`, before today's package-log upgrade to 262-1.


## Round19 retrospective index repair (not new growth)

The round18 entries existed before this index repair. Their missing rows
did not justify the old author expansion verdict; the outside closure's
round18 trends remain unchanged / unchanged / improved.

| Existing ground | Existing entry | Scope retained |
|---|---|---|
| Own evidence retention | `knowledge/evidence-minimization-r18.md` | Frozen regex floor plus content adjudication; line digests are provenance, not secrecy; history action remains operator/kagi-owned |
| Own freeze-label calibration | `knowledge/freeze-order-r18.md` | Commit ordering, historical correction versus prospective verification, and explicit input-revision binding correction |
| Passive dispatch evidence | `knowledge/dispatch-ledger-r18.md` | Per-attempt payload identity, distinct from whole-ledger sequencing; no orchestration authority |

Round19's bounded content-review population is additional to the unchanged
R1–R9 all-blob retention scope. An incomplete review is not clean, and a
complete review is not an automated privacy classifier or a proof that
private material is absent everywhere. Retrospective index/table repairs
are not newly explored frontier ground.

## Round-20 coverage additions

| Ground | Entry | Bounded advance |
|---|---|---|
| Per-seat wave settlement (FR3) | `knowledge/wave-settlement-r20.md` | Dispatch members vs report files for every lane wave, misrooted/stub/unsafe distinguished; lane and fleet scans reproduce independent ground truth. Hygiene-vs-never-written, dispatch authenticity and successor reports stay frontier. |
| Drift baseline re-pin | `knowledge/drift-repin-r20.md` | Closed-class classification of all 50 r10 drift tokens with evidence, and a new baseline; comparator blind spots (first-word values, duplicate keys, positional pairing) named, not fixed. |

## Round21 correction — loss accounting before baseline acceptance

The round20 drift re-pin coverage-map row is historical, not an acceptance
endorsement. CloseMori20 rejected the pin and QUALITY67's universal permission;
QUALITY69 now supersedes67. `knowledge/drift-repin-r20.md` carries the erratum.
The r20 baseline remains byte-unchanged but invalid for acceptance. Both
aggregator-r10 identities are retained as unresolved historical observations,
not inferred settled/unsettled/dead. The minimized removal/preservation
provenance is `.ufo/waves/round-21/evidence/historical-provenance.json`.
FR3 independent lifecycle disposition remains frontier; retaining unknowns
does not grow authoritative settlement coverage.

## Round22 calibration of existing retention ground (not expansion)

| Existing ground | Entry | Bounded change |
|---|---|---|
| Own-evidence retention accounting | `knowledge/retention-reconciliation-r22.md` | Independent committed-tree recount and exact receipt comparison; explicitly distinguishes policy non-author exclusions from source-file subtraction. Agreement is not clearance; no frontier row advanced. |

The original round22 declaration misread “policy-excluded”; corrected
pre-implementation v2 requirements retain the original bytes and error.
R21's95raw−5non-author=90scanner population still has4unallowlisted hits.
Original permission control11/12 remains red, two historical dispositions
remain unknown, and the invalid r20 baseline is not accepted or re-pinned.

## Round23 disposition — C1 cutover, rejected quota attempt

| Ground | Current disposition | Evidence |
|---|---|---|
| Existing retention accounting | Schema-v2 API removes raw_unallowlisted; use scanner_unallowlisted for the in-scope count and raw_not_allowlisted for the raw complement. No privacy or baseline clearance. | `knowledge/retention-reconciliation-r22.md` Round23 correction; round23 original26 and exact-source/identity/output controls |
| FR2 quota visibility | Strict target unprovable/not admitted; prototype and note withdrawn, no Core/frontier closure or admitted capability. | `lessons/round-23.md`; `.ufo/waves/round-23/rejected/` beneath the lane root |
| Non-author round23 verification | C1 bounded improvement; original C2 unprovable, no capability addition or privacy clearance. Native accounting closure remains separately required. | `lessons/round-23-verifier-spotcheck.md` |

Original quota29/30 and its contradictory frozen row/rule remain immutable evidence,
not a narrowed pass. Permission-truncated mapping and accounting/enforcement ambiguity
make the rejected prototype unsuitable for confident runtime statements. The former
quota knowledge file is intentionally absent, not a dangling admitted index entry.
The Frontier table remains unchanged. Configuration/diagnosis route to tsukuroi/
operator; reclamation approval is operator-owned, with souji proposing within its
scope. Four inherited hits, permission11/12red, two unknown dispositions, blocked
baseline acceptance and privacy_clearance=false remain.

## Round-24 coverage additions — C2 one-shot system pressure (admission pending)

| Ground | Entry | Bounded advance |
|---|---|---|
| One-shot system pressure read (FR12 partial advance) | `knowledge/system-pressure-r24.md` | System `/proc/pressure/{cpu,memory,io,irq}` read once per resource with per-resource states (`ok`, `absent`, `unsupported`, `unreadable`, `malformed`, `counter_regressed`), a `PRESSURE_OK`/`PRESSURE_HIGH`/`PRESSURE_PARTIAL`/`PRESSURE_UNAVAILABLE` verdict and `PRESSURE_HIGH` findings against a labeled-local, uncalibrated `--warn-avg10` (default 10.0). System CPU `full` is reported undefined and is never evidence of no stall; `irq` carries `full` only, so its absent `some` is expected, not malformed; unavailable is never zero and no cause is inferred from it. Host scope: a system-wide high reading is not evidence that the fleet caused it. Read-only: no PSI trigger, no write to `/proc`, `/sys` or a cgroup, no service or package change. No census surface, no census finding id, no baseline re-pin. The resident PSI trigger watcher and cgroup-scoped CPU/IO/IRQ pressure stay frontier, as does the two-sample `--interval` stall rate (its added cost is about S seconds and it misses the round-8 dwell budget). |

## Round-24 Frontier note — FR12 narrowed, not closed

The FR12 row above (`corpus/README.md:343`) and its PROVINCE counterpart (`PROVINCE.md:55`)
are byte-unchanged by this round. This appended note records what the round-24 C2 advance
changes about FR12's scope:

- **Advanced to Core (pending admission):** the one-shot read of the **system** pressure
  files `/proc/pressure/{cpu,memory,io,irq}` (`tools/mori-pressure.py`). This is the
  reading the frontier row always excluded from a *census* probe; it is a separate
  read-only probe, not a census surface, and it adds no `SURFACE` row, no census finding
  id, no DRIFT verdict and no baseline re-pin.
- **Still frontier, unchanged:** the resident, event-driven PSI trigger watcher — a
  threshold written into `/proc/pressure/*` plus a polling process — and the
  **cgroup-scoped** CPU/IO/IRQ pressure files. Neither is observed by the new probe. The
  two-sample `--interval` stall rate also stays frontier with FR6: its added cost is
  about S seconds and it does not meet the round-8 dwell rule
  (`corpus/knowledge/surfaces-r8.md:47-48`).
- **Boundaries that travel with the Core row:** the system CPU `full` line stays
  undefined (`full_system_undefined: true`) and is never read as evidence of no stall; a
  missing, unsupported or unreadable file is an unavailable state and never a zero
  reading, with no cause inferred from it (boot and kernel configuration diagnosis is
  tsukuroi's); the threshold is a labeled-local placeholder, so FR8 stays open; the
  reading is host scope, so a high value is evidence to correlate, never proof that a
  lane, a wave or the fleet caused it.
- **Open at the FR12 boundary:** the root-cgroup `cgroup.pressure` switch can stop
  `psi_system` accounting while `/proc/pressure/*` stays readable, so a zero or
  non-advancing `total` is not evidence of no stall and the probe does not detect that
  case (wave-1 finding `CriticC2Semantics.md` F3; the upstream anchors belong to
  `knowledge/system-pressure-r24.md`).

No frontier row is closed by this round, and no quota, retention, wave-settlement or
telemetry ground is touched.

## Round-25 coverage additions — C2 harness background-job capacity runway (admission pending)

| Ground | Entry | Bounded advance |
|---|---|---|
| Harness background-job capacity runway (new FR15) | `knowledge/harness-job-capacity-r25.md` | One JSON object (`schema: mori-job-runway-v1`) naming the **configured** `async.maxJobs` read from one settings file (default the operator's OMP settings file), the **clamp** compiled into the installed harness binary (default the real path of `omp` on `PATH`), and the **setting default** from that binary's settings table, with `effective = max(1, min(clamp, base))` and the verdicts `RUNWAY_AS_CONFIGURED` / `RUNWAY_CLAMPED` / `RUNWAY_DEFAULT` / `RUNWAY_UNKNOWN` (exit 0 / 1 / 0 / 2). On this host: configured 200, clamp 100 at one site, default 100 at one site, effective 100, `RUNWAY_CLAMPED` — the configured value is clamped by the binary, not honoured. The read is a cap, never a count: no job list is read, and the live running-job count is not readable from outside a session. `RUNWAY_UNKNOWN` means this tool cannot derive a number from the bytes it was pointed at, never "unlimited" or "no clamp". Read-only: one file and one binary, no `omp` run, no settings write, no other configuration surface. Not a census surface: no `SURFACE` row, no finding id, no DRIFT verdict, no baseline re-pin. Sources S098–S103 and S112–S113 (`SOURCES.md:104-110,118-119`), all at oh-my-pi tag `v18.12.6`. |

## Round-25 Frontier note — FR15 added, no existing row closed

The FR1–FR14 rows above (`corpus/README.md:332-345`) and their PROVINCE counterparts
(`PROVINCE.md:44-57`) are byte-unchanged by this round. This appended note registers the new
frontier row and records what it does and does not cover.

- **FR15 — Harness background-job capacity runway.** First evidence:
  `knowledge/harness-job-capacity-r25.md:36-221`; `SOURCES.md:104-110,118-119`. Boundary: the
  bounded Core advance above reads the cap the harness would compute from one settings file and
  the installed binary's bytes. **Still frontier:** the live running-job count in any session
  (not readable from outside that session); the scope of the counted population — one manager per
  root session tree, children borrowing their parent's, so the same number applies to every
  manager while the population is per tree, and a refusal cannot be attributed to a session from
  outside it; and every settings layer the tool does not read — the project layer (`<cwd>/.omp/`),
  `--config` / `PI_CONFIG_FILES` overlays, runtime overrides, and agent-dir relocation by
  `OMP_PROFILE`/`PI_PROFILE` or `PI_CODING_AGENT_DIR`. The tool reads one file while the runtime
  resolves a stack, so `configured` is that file's value and `effective` is the cap that would
  apply if it were the effective one. Also frontier: why the ceiling is 100, what filled a runway
  when a refusal appeared, and any behaviour of other harness versions.
- **FR15 is distinct from FR14.** FR14 is agent-workload telemetry: mori is consume-only and the
  emission belongs to the emitting lanes and orchestration; its round-17 advance is a passive
  transcript terminal-at-scan observation (`knowledge/seat-terminal-status-r17.md`). FR15 reads no
  transcript, no telemetry and no lane-emitted record: it reads a settings file and a compiled
  binary to state the harness's own concurrency ceiling, and its interesting content is the
  mismatch between an operator's configured value and the binary's clamp. FR14 is not advanced,
  narrowed or closed by C2, and no other FR1–FR14 row covers this ground.
- **Adjacent, not absorbed:** the mechanism behind the clamp is kumitate's OMP task/hub ground;
  writing harness configuration is operator-owned; mori reports the read and changes nothing.
  The fleet seat gate counts a different population under a different number and is not judged
  here.

No frontier row is closed by this round, and no quota, retention, wave-settlement or telemetry
ground is touched.

## Round-31 coverage additions

| Ground | Entry | Bounded advance |
|---|---|---|
| Watchdog daemon identity and degraded-`pgrep` visibility (FR5 partial advance) | `knowledge/watchdog-identity-r31.md` | A sourced decision table (S161–S165, S167, S169–S174) of what each pid-probe observation — `pgrep` with and without `-f`, `comm`, `cmdline`, `stat` state and start time, pid reuse, pgrep exit codes, `/proc/locks` on the watchdog's singleton lock — does and does not establish about the fleet watchdog, with host measurements on throwaway processes. It changes no probe and claims no host liveness. |

## Round-31 Frontier note — FR5 narrowed, not closed

The FR5 row above (`corpus/README.md:338`) is byte-unchanged. The entry narrows FR5 to a decision table; the census probe
is unchanged (`tools/mori-census.sh:711-715` still counts `pgrep -af` lines), the watchdog writes no pid file, and the
read-only `/proc/locks` anchor is knowledge, not a probe. D06 (`knowledge/audit-r11.md:201`) stays open and is shared
with kumitate for ufo-fsd-alpha's own watchdogs.

## Round-34 Frontier note — FR6 narrowed, not closed

The FR6 row above is byte-unchanged by this round. Round 34 lands the two-sample write-rate operation as a separate
read-only tool, `tools/mori-disk-rate.py` (two `/proc/diskstats` readings, `/sys/class/block` classes, per-device
states and rates, a whole-disk host total; rules R1–R7 in `.ufo/waves/round-34/contract.md`, sources S180–S198). It is
an operator-run probe, not a census surface: `tools/mori-census.sh` does not call it and keeps its since-boot average.
Its claim did not verify: a post-data shortcut met the frozen counter (`lessons/round-34.md` M2), and rule-order
mutants survive that counter (M3), so the tool's correctness rests on the seat attacks recorded in the lesson, not on
the counter.

- **Still frontier:** a two-sample census arm. Re-measured in round 34 (`.ufo/waves/round-34/wb/ExecLatencyRemeasure.md`,
  20 runs per interval, load 15–27 on 32 CPUs): the tool's median wall time is about 129 ms at a 100 ms interval and
  about 232 ms at 200 ms, against the round-8 bar of 50 ms (`knowledge/surfaces-r8.md:47-48`); only intervals of
  10 ms or less fit, and at 10 ms most readings are zero while a few catch a load burst (6 of 40 nonzero), so a
  fitting interval does not give a usable rate.
- **Still unsourced:** the device-mapper double count. Round 34 observed it again on this host
  (`.ufo/waves/round-34/wb/ExecStackedRemeasure.md`: over 30 s, dm-0, its slave partition and that partition's disk
  each moved by the same 219728 write sectors), so a write through dm-0 appears once in the whole-disk total and three
  times in a sum over every line (twice if partition lines are left out); no admitted source states it, so the tool's
  host total excludes stacked devices by class, not by a sourced rule.

## Round-36 coverage additions

| Ground | Entry | Bounded advance |
|---|---|---|
| Source-row drift re-fetch (freshness technique; the first reusable whole-registry sweep over the committed `sources-r<N>` copies with per-state classification — round 32 re-fetched specific row URLs once for a live-recheck claim, a different, narrower scope, w2/CritC1Axis) | `knowledge/source-drift-r36.md`; `tools/mori-source-drift.py` (probe, `SKILL.md` Round36 registry row) | The lane's first programmatic re-fetch of every `corpus/SOURCES.md` row with a committed copy, classifying `fresh` / `excerpt` / `drifted` / `unavailable` / `no-copy` against `corpus/evidence/sources-r<N>/<id>.<ext>` (newest N). Byte classification only: `drifted` means the copy is not reproducible from today's body. On
2026-10-23 the nine drifted rows were (`python3 tools/mori-source-drift.py --root .` →
`.ufo/waves/round-36/evidence/drift-live-r36.txt`, exit 1): five annotated excerpts
(S156–S160) and two docs.python.org build-footer rebuilds (S176, S177) — representation differences,
sources unchanged — plus S210 (git-scm.com asset-bundle redeploy with dropped integrity attributes;
post-copy change that misses the taught passage) and S211 (PMC page varying per fetch, csrf/ncbi_phid
tokens; a rejected row; never `fresh`). None names a source change to a taught claim; the dated
enumeration with open-time shas is in `corpus/knowledge/source-drift-r36.md`.
Self-test `python3 tools/mori-source-drift.py --selftest` — PASS 4 cases at `bf0df77`. |
| SOURCES append-only enforcement with deleted-row detection (operability; r35 spotcheck §6 items 2–3 routed debt) | `tools/mori-sources-appendonly.py` (gate, `SKILL.md` Round36 registry row; QUALITY 104); capability row enters `SCORECARD.md` this round | One command reports in-place immutable-cell edits, deleted rows, superseders and per-round changed ids of `corpus/SOURCES.md`: `python3 tools/mori-sources-appendonly.py <tip> --round-base <entering tip>` exits 0 with `round_changed=[]`. At `bf0df77` it records a disposition for each of the 18 in-place-edited ids (15 pre-round-34 + S069 + S182/S193) via the S205–S220 supersede rows. Self-test PASS 8 cases. The violations stay listed — a superseding row is a disposition, not a discharge (QUALITY 102). |

The production census, silence oracle and all pre-existing gates are byte-unchanged by this round
(`w2/SentCensus` finding; `git diff 6bd57097..bf0df77 --name-status` lists no `tools/mori-census.sh`,
`tools/mori-silence-cases.sh` or prior `tools/mori-round*` path). Neither new tool is a census
surface: no `SURFACE` row, no DRIFT verdict, no threshold. The C1 row above is exploratory —
it moves coverage ground and technique, and its probe's byte predicate passed
(`evidence/c1-after.txt`), but no freshness verdict is claimed from it (w1 `CritAxisFit.md`).

## Round-37 coverage additions

| Ground | Entry | Bounded advance |
|---|---|---|
| Source-drift hardening (freshness technique, verification): the two fetch policies that round 36 landed at `1caa242` are now named selftest arms, each with a mutation that must kill it, and the capability has a verified register row | `knowledge/source-drift-hardening-r37.md`; `tools/mori-source-drift.py` (`--selftest` 6 cases); `.ufo/waves/round-37/count-c2.py` | `python3 .ufo/waves/round-37/count-c2.py <tip>` runs the probe, the two policy mutants and the corpus binding; `huge_cap` and `redirect_private_refused` pass on the real bytes and each fails in its own mutant (`C2=met`). Live runs 2026-10-23: the entering 220-row registry gives `rows=220 fresh=49 … drifted=9 …` (`evidence/drift-live-r37-start.txt`); the scored 225-row tip gives `rows=225 fresh=53 excerpt=0 drifted=10 unavailable=0 no-copy=162`, exit 1 (`evidence/drift-live-r37.txt`) — the nine round-36 rows plus S223, whose page footer clock changes between fetches (S211 class, never `fresh`). Named limits: final-destination-only redirect check, DNS-resolved private addresses unchecked, over-cap bodies grade `unavailable`. |

## Round-38 coverage additions

| Ground | Entry | Bounded advance |
|---|---|---|
| Content-anchor verification (calibration/discrimination): a corpus binding is checked for resolvability — named code anchors, capability paths, one named drifted row per summary count, and a named-row arm killed by its own mutation — not for token presence (r37 M9) | `knowledge/source-drift-content-anchor-r38.md`; `.ufo/waves/round-38/count-c4.py` | `python3 .ufo/waves/round-38/count-c4.py <rev>` rejects three fabricated token witnesses and prints `C4=met` on the real binding; the r37 counter prints `C2=met` on the same fabricated binding (`evidence/v3-token-control.txt`). Bounded: an anchor proves presence in the bytes, not semantics; the mutation arm is the separate statement. |
| Timed supersede disposition (depth/gate): a supersede row only disposes an edit when its landing commit postdates the edit; presence is not disposition | `knowledge/containment-timed-supersede-r38.md`; `tools/mori-sources-appendonly.py` (`supersede_timing`); S226 | `python3 tools/mori-sources-appendonly.py <rev> --round-base f10a320d` prints `supersede_timing superseded_as_of=[...] stale_supersede=[...]`; at `e37dcc6` S069 is stale, at the round-38 tip it is as-of. Bounded: commit order in the path's history; the in-place change stays listed (QUALITY 102). |

## Round-39 coverage additions

| Ground | Entry | Bounded advance |
|---|---|---|
| Fabricated-content discrimination v2 (calibration): the drift-corpus binding's checks now demand code-position anchors (≥8 chars, non-comment), file-not-directory capability paths, committed copies for named drifted rows, and a structural got-vs-want drift-kill whose expected post-state is drawn at run time (r38 M18) | `knowledge/source-drift-content-anchor-r38.md` (checks v2 in `.ufo/waves/round-39/count-c7.py`) | `python3 .ufo/waves/round-39/count-c7.py <rev>` rejects the three round-38 witnesses plus a comment-parked-anchor entry and prints `C7=met` on the real binding; the r38 counter accepts all four bypass classes (`evidence/c7-red-*.txt`) and accepts a fabricated self-consistent clone that v2 rejects via the committed-copy rule (`evidence/c7-red-clone.txt`). Bounded: a verbatim-real clone (real anchors, real tool, copied receipt) is indistinguishable from real work under static checks — the same limit QUALITY 105 records; the drawn drift arm is the live-work binding. |
| Counter conformance v2 (operability): timeout keywords are read as values (constant-folded through module assignments, parameter defaults, list subscripts), drains must be used `communicate(timeout=…)` calls, and the shipped selftest's conjunct mutation exercises the communicate-timeout rule (r38 M19) | `.ufo/waves/round-39/conform.py`; `.ufo/waves/round-39/count-c7.py` (the counter of record) | `python3 .ufo/waves/round-39/conform.py <rev>` → `CONFORM=met` on count-c7; both r38-M19 bypass fixtures (`communicate(timeout=None-valued name)`, `wait(timeout=…)+stdout.read()`) print `CONFORM=unmet` with `timeout_value`/`drain_shape` FAIL where the r38 checker printed `CONFORM=met` (`evidence/c8-red-*.txt`, `c8-after-*.txt`); `--selftest` → `pass=9 fail=0`, each mutation flipping exactly its own check. Bounded: static folding reads initial bindings; runtime rebinding of a budget list is not tracked (disclosed in the checker's resolver). |
| Ancestry-based timed supersede (depth/gate): "descends from" is reachability (`git merge-base --is-ancestor`), edits compare against the first parent, the walk carries parents with `--full-history`; S227 grounds the relation; S228 supersedes S226 with the corrected located quote (r38 F1/F2 + routed quote fix) | `knowledge/gate-ancestry-r39.md`; `tools/mori-sources-appendonly.py` (P-C9); S227, S228 | `python3 tools/mori-sources-appendonly.py --selftest` → `pass=12 fail=0`; the r38 gate bytes fabricate `round_changed=[S001]` on fixture C and print `stale` on fixture D where the predicate's words read as-of (`evidence/c9-red-a.txt`); the v2 gate prints the predicate-word verdicts and byte-identical lane-history lines at the tip and `e37dcc6` (`evidence/c9-after-*.txt`). Bounded: latest-superseder selection on incomparable branches and same-id edits on incomparable commits stay walk-order (QUALITY 112). |

## Round-42 coverage additions

FR1 gains the runtime-layer lossy-link entry (`knowledge/oom-evidence-loss-r38.md`,
admitted from the shokuknow package, sources S232–S235 + S241): the absence
of an OOM record is not evidence no OOM occurred — three named loss
mechanisms sit below the journal, and `memory.events`/`memory.events.local`
read as a pair is the checkable survivor. FR1/FR13 gain the victim-context
abstract anchor (`knowledge/oom-victim-context-r41.md`, S262): the kernel's
victim selection has no container context, so a host observer cannot
attribute an OOM to a container from the kernel record alone. The FR13
tracepoints entry was refused this round (source S268 unreachable; flip
condition in `.ufo/waves/round-42/assimilation/refused-oom-tracing.md`).
Frontier rows stay frontier; no Core move is claimed.

## Round-43 coverage additions

Resource-runway ground the map did not hold as a core reading: `journalctl --disk-usage` is a total over archived and active files the command can see, not a per-journal share (`knowledge/journal-disk-usage-total-r51.md`, S470, page re-opened 2026-10-24). A live read-only invocation printed `Archived and active journals take up 269M in the file system.` No vacuum, rotate, or journald change. Two assimilation entries on adjacent ground were refused (campaign file:// plus a MESSAGE grep; `reset-failed` host mutation) — reasons and flips in `corpus/lessons/round-43.md`.

## Round-44 coverage additions

FR5 ground the map held only as row scopes: the zero-character `/proc/<pid>/cmdline`
read and the `Z` state were already carried by `corpus/knowledge/watchdog-identity-r31.md:27,29`
(S170, S167/S171), and S171's scope already names `X`. What round 44 adds is the
**measured mm-less world** — 1698 of 1931 `/proc` entries read a zero-length
`cmdline` and every one was state `I` (1489) or `S` (209), so the state letter does
not separate an mm-less kernel thread from a sleeping user process
(`corpus/evidence` reading: `.ufo/waves/round-44/evidence/cmdline-empty-by-state.txt`)
— plus the two translations' divergence on swap-out visibility, which concerns
**different objects** (S471's `stat` comm field vs S472's `comm` file, the latter a
Linux-1.3.11-era translation), and the `ENOENT` boundary for a pid that does not
exist. Entry: `corpus/knowledge/pid-probe-conclusion-r44.md` (S471, S472,
both pages opened 2026-10-25). No probe, census surface or finding id is added;
FR5 stays open — a state read does not establish daemon identity.

## Round-47 coverage additions

FR13 ground the map held only as a peer-reviewed abstract (`knowledge/oom-victim-context-r41.md`,
S262) and one queued field-schema row (S005): the **full v7.2 `oom` trace-event set** — eight
events, each with its `TP_STRUCT__entry` field set and the function that emits it — and the
reaper lifecycle (`mark_victim` → `wake_reaper` → `skip`/`start`/`finish_task_reaping`, all
pid-only after the mark). Entry: `corpus/knowledge/oom-tracepoints-r47.md` (S475 header, S476
call sites, S477 this host's tracefs listing; S005 re-opened, byte-identical to v7.2). Count:
8 — `grep -c '^TRACE_EVENT(' corpus/evidence/sources-r47/include_trace_events_oom.h` 2026-10-25.
FR13 stays frontier: no tracer is enabled, installed or proposed (the host's `events/oom/enable`
reads `0` and stays untouched); the entry names what the kernel's own event says (victim pid,
comm, uid, memory) and what it never says (cgroup path, culprit).
