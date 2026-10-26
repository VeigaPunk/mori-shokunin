# Mo51ConnSiblings — Sibling-overlap scan (round-51 wave w1)

Item: read-only scan across `/home/vgpnk/Projects/shokunin/*-shokunin` (skipping `.scratch` and `.ufo/waves`) for (1) MemAvailable / meminfo / memory-runway knowledge and its owners per lane PROVINCE.md, versus mori's new `corpus/knowledge/memavailable-estimate-r51.md`; and (2) pin or selftest re-execution tools carrying an env-versus-stale distinction or hermetic re-run rules in sibling lanes.

MACHINE_ID: redacted (per rule).

Method and evidence: this seat ran read-only `grep` (and `read`) probes from the fleet root. Each probe is listed below with the pattern, the paths scanned, and the notable output lines; a probe that returned no matches is reported as `(no matches)`. All probes were read-only; no sibling file was written, no git/jj mutation was performed, and the scan excluded `.ufo/waves` and `.scratch` content (one kama pointer under `.ufo/waves` is reported only as an excluded observation). Scratch `/fast/scratch/hyaku/mori-r51/Mo51ConnSiblings/` was created; the scan wrote nothing there and it is removed at exit.

## Part 1 — MemAvailable / meminfo / memory-runway knowledge

Probe: pattern `MemAvailable|meminfo|memory runway|runway|MEM_MIN_GB` over every `*-shokunin/PROVINCE.md`; pattern `MemAvailable|meminfo|memory runway|runway|MemTotal|available memory|estimate of how much memory` over every `*-shokunin/corpus/knowledge`. Also single-lane follow-up reads.

### 1.1 tsukuroi-shokunin — the only sibling holder of retained meminfo knowledge

- Owns/direction per PROVINCE.md:
  - `PROVINCE.md:30-33`: "Host memory and kill-event measurements support OS triage; they do not establish which fleet wave caused pressure or whether an endpoint works … fleet correlation belongs to mori (`../mori-shokunin/PROVINCE.md:6-16`)."
  - `PROVINCE.md:49` (ADJ-04): host pressure / kill signal needing fleet-wave attribution is routed to mori.
  - `PROVINCE.md:121` (OUT-001): "Mori owns kill/OOM and cgroup memory evidence; fleet correlation of host pressure is mori's, not OS triage."
- Holds meminfo knowledge (no definition of what MemAvailable is):
  - `corpus/knowledge/kill-event-deep-r8.md:3-7,182`: reads `/proc/meminfo` in OS triage; row 182 records MemTotal / MemAvailable / Shmem / SwapFree with temporal class "live only — no".
  - `corpus/knowledge/oom-event-plane.md:302-303,350`: free-memory surface read via `free -h` / `/proc/meminfo` (live only); row 7 (tmpfs discipline) names `Shmem` as memory that competes with anon.
  - `corpus/knowledge/memory-arm-ver-s8.md:65-67`: C6 meminfo live shape (`MemAvailable`/`Shmem`); "live counters drift between instants … the difference is the known drift, not a disagreement".
  - `corpus/knowledge/adjacency-handoffs-fleet-r1.md:99`: interpretation "meminfo fields are instantaneous gauges".
  - `corpus/knowledge/kill-oom-boundary-r33.md:28-30`: explicit overlap/gap table. Row 28: "declared shared surface with a split stated on both sides: mori reports runway, this lane explains the OS cause." Row 30: "live available and shared memory … memory fill/availability at class level (mori `PROVINCE.md:26`); Shmem not named | **partial overlap on availability; Shmem is this lane's alone**."
- Relation to `memavailable-estimate-r51.md`: **ADJOINS — no conflict found.** Tsukuroi reads MemAvailable as an instantaneous gauge and never defines the number; mori's entry supplies the definition (kernel estimate, formula, units, model-vs-measurement caveat) that tsukuroi's C6/`MEM_AVAIL_LOW` threshold surface leaves open. Both already share the split (mori reports fleet runway; tsukuroi explains OS cause). No statement in tsukuroi's entries contradicts the new entry.
- One nuance for the L1 (severity LOW): tsukuroi's boundary row 30 justified "Shmem is this lane's alone" on "Shmem not named [by mori]". The new mori entry now names Shmem for (rows 4, 5, 7, 17, 20 of the entry plus the reading rule). This does not conflict semantically — both treat Shmem as tmpfs/shared-memory contents that feed `Cached` but not the estimate — but it changes the basis of tsukuroi's "alone" exclusivity claim, so the next adjacency pass over `kill-oom-boundary-r33.md:30` should re-read that cell.

### 1.2 kama-shokunin — no retained knowledge, no ownership

- `PROVINCE.md` contains no memory/meminfo/runway row.
- `corpus/knowledge/` has no MemAvailable/meminfo match (probe returned no matches).
- The only MemAvailable readings in the lane live under `.ufo/waves/round-16/build/advice/ScoutHostRuntimeFacts.md:67-71` and `falsify/advice/ConnectMoriFootprint.md:52-56` — excluded from this scan by scope and not retained knowledge. Kama neither owns nor conflicts; mori's new entry does not adjoin any kama knowledge.

### 1.3 Other lanes

- `souji-shokunin/PROVINCE.md:50-52`: states mori observes fleet/host health incl. runway and that souji routes resource findings to mori. No knowledge entry.
- `kumitate-shokunin/corpus/knowledge/reconcile-and-cycle.md:219`: `manifest_runway_low` is an OMP manifest-size budget (25 % of a 1 MiB bound), not host memory runway — a different "runway" concept; no overlap.
- `lore-shokunin/PROVINCE.md:23` "character knowledge/memory state over time" is narrative fiction memory, not host memory.
- All other lanes: no matches in PROVINCE.md or corpus/knowledge for any meminfo/memory-runway term.

### 1.4 Part-1 conclusion (sentence mori's report should carry)

Mori's `memavailable-estimate-r51.md` adjoins tsukuroi's existing meminfo surface (the only sibling holder), which already declares a split — mori reports runway, tsukuroi explains OS cause — and the new entry fills the definitional gap tsukuroi leaves open; it conflicts with no sibling, and kama holds no qualified ownership at all.

## Part 2 — Pin / selftest re-execution tools with env-versus-stale or hermetic re-run rules

Probe A: pattern `class=env|class=stale` over all `*-shokunin/corpus` → `(no matches)` anywhere outside mori. Probe B: pattern `class=env|class=stale|env-versus-stale|hermetic|bubblewrap|bwrap|--tmpfs|git archive|TMPDIR` over all sibling `SKILL.md`, `tools/`, `scripts/`, `verifiers/`, `quality/`, `reports/` dirs; plus follow-up reads of the cited lines.

Hits (lane — path:line — kind — one sentence for mori's report):

1. **souji-shokunin** — `tools/cand-a1-quarantine.sh:439,441`, `cand-a2-quarantine.sh:399`, `cand-b1-quarantine.sh:402`, `cand-b2-quarantine.sh:437`, `cand-c1-quarantine.sh:418`, `cand-c2-quarantine.sh:374`: verdict lines already tokenize staleness — `class=stale-via-prong1`, `class=stale-reverified`, `class=FAIL` — for receipt re-derivation. **Adjoins C1 arm C's vocabulary**: the sibling has a stale-class token set but no env class, and it is scoped to receipts, not to pin mismatch lines.
2. **tsukuroi-shokunin** — `tools/tsukuroi-census.sh` `--selftest` is a hermetic fixture-tree run; `SKILL.md:307-310`: "The `TSUKUROI_*` env overrides exist to make the selftest hermetic … a live verdict produced with overrides would not be a measurement of the host — fixture runs only." `tools/check-self-assessment.py` runs the census selftest from a `git archive <REV>` extraction under scratch with the child's TMPDIR inside that private dir (round-41 R40-TMP-MISROOT fix). `corpus/knowledge/memory-arm-mutants-s8.md:68-70,130-131` (defect D10): an unreadable meminfo must surface as `unknown=[C6-meminfo]`, never as a clean zero. **Adjoins C1**: the archive-outside-repo + scratch-TMPDIR move is structurally the same fix as C1's relocated arm, and D10 is an env-vs-measured-zero naming rule.
3. **kama-shokunin** — `tools/round47-live-replay-audit.py:50-54` and `tools/kama-live-replay.py` (`SKILL.md:1450-1462`): fresh-HOME replay from `git archive <tip>` under `--scratch`, inputs re-acquired under scratch, receipts with flipped recorded digests refused, every evaluated check must match with equal server/model sha256. The round-42/43/46/47/48 audit counters (`round42-digest-audit.py:55-57`, `round43-hexrun-audit.py:55-56`) add a "hygiene" leg: the tool run with TMPDIR pointed at an empty private dir must leave it empty. **Strongest sibling analogue of hermetic re-execution with content-vs-environment separation** — but it is a replay-equality mechanism, not a `class=env`/`class=stale` tag on mismatch lines.
4. **kumitate-shokunin** — `scripts/cap-run.mjs` (`SKILL.md:618`): children run under a transient user scope with `MemoryMax` plus `env -i` and `bwrap --unshare-pid --die-with-parent --new-session --clearenv`; `scripts/plan-before-ready.sh` (`SKILL.md:635`) runs inner gates from `git archive PLAN` so the corpus map is judged at the freeze commit; `scripts/counter-rerun.mjs` (`SKILL.md:621`) prints `AGREE|DISAGREE`. **Adjoins**: hermetic re-run rules with env-clearing, no stale taxonomy.
5. **kaidoku-shokunin** — `SKILL.md:832` (`revexec.py`): re-executes scripts under a systemd-run sandbox (`PrivateNetwork=yes`, `ProtectSystem=strict`, `ProtectHome=read-only`). Hermetic re-execution infrastructure; no stale taxonomy.
6. **kengaku-shokunin** — `SKILL.md:498-499`: "a hermetic gate must never read `/proc` — pin committed bytes instead"; `SKILL.md:577` (`git-webserver-probe`): bubblewrap sandbox for its 22 cases. Hermetic-by-construction rules, including a negative rule on host reads.
7. **mado-shokunin** — `SKILL.md:693-695,1771,1869`: `mado-verify.sh --selftest` (268/268 hermetic assertions), `--no-live` explicitly skips the live layer, `--snapshot`/`--snapshot-diff` receipts, and QUALITY 29 (any harness stubbing a host binary must fail closed). Live-vs-hermetic split; no stale taxonomy.
8. **tabi-shokunin** — `SKILL.md:2543,2558-2559,2575,2626`: multiple gates state "self-test writes and deletes only its own temporary repositories under TMPDIR"; `check-measurement-binding.mjs --reproduce` re-runs only the recorded argv of a bound measurement (`SKILL.md:2476`). Hermetic self-test rules; no stale taxonomy.
9. **tameshi-shokunin** — `SKILL.md:58-74`: explicit gate-shape decision table (hermetic suite vs live gate vs audit lane), with an env-poisoning proof (`UFO_SRC=/nonexistent … --selftest` → PASS) and the rule that a live assertion may never be smuggled into a hermetic suite (must stay behind `--integrations`). A methodology rule that directly embodies the env-vs-measurement split.
10. **kake-shokunin** — `scripts/citing_set_hostile_selftest.py` and `scripts/citing_set_selftest.py:227-242`: child env gets isolated HOME and TMPDIR/TMP/TEMP and `GIT_*` stripping; `scripts/id_resolver.py:62-65` strips inherited `GIT_*` from child gits; `scripts/corpus-contract.mjs:31-35` and `scripts/freshness-sweep.mjs:18-23` prove read-only-by-construction with write-confinement marker pairs. Hermetic fixtures + hostile shapes; no stale taxonomy.
11. **kasegi-shokunin** — `SKILL.md:1043`: round-29 selftest completeness recorded with "hermetic git-free behavior for that measurement". Minor hit.

Probe A result (evidence for novelty): the pattern `class=env|class=stale` has **zero** matches in every sibling corpus; the exact env-versus-stale split of C1 arm C exists only in mori's new tool.

### Part-2 conclusion (sentence mori's report should carry)

No sibling implements mori's `class=env` vs `class=stale` split on pin-mismatch lines — the closest neighbors are souji's `class=stale-*` receipt tokens, tsukuroi's `unknown=[C6-meminfo]` env handling and archive-outside-repo scratch TMPDIR, and kama's fresh-home replay hygiene — so C1 arm C is novel, not duplicated, and its vocabulary rhymes with existing sibling conventions.

## Findings

- **HIGH** — `tsukuroi-shokunin/corpus/knowledge/kill-oom-boundary-r33.md:30`: tsukuroi declares "partial overlap on availability; Shmem is this lane's alone", grounded on "Shmem not named" by mori. Mori's `memavailable-estimate-r51.md` now names Shmem (rows 4, 5, 7, 17, 20 and the reading rule). No semantic conflict, but the exclusivity rationale changes; the next adjacency pass must re-read the cell. Mori's report should carry the shared-split wording ("mori reports runway, tsukuroi explains the OS cause") when citing tsukuroi.
- **MED** — `tsukuroi-shokunin/corpus/knowledge/` (kill-event-deep-r8.md, oom-event-plane.md, memory-arm-ver-s8.md): tsukuroi is the only sibling holder of retained meminfo knowledge and reads MemAvailable as an instantaneous gauge without defining it. Mori's entry adjoins by supplying the definition; no conflict found.
- **LOW** — `kama-shokunin`: no retained MemAvailable/meminfo/runway knowledge and no PROVINCE ownership row; its only readings sit under `.ufo/waves` (out of scope). Do not cite kama as an owner.
- **LOW** — `souji-shokunin/tools/cand-*-quarantine.sh:374,399,402,418,437,439,441`: `class=stale-via-prong1` / `class=stale-reverified` / `class=FAIL` are stale-class tokens but carry no env class and concern receipts, not pin matches; adjoins C1 arm C without duplicating it.
- **LOW** — `tsukuroi-shokunin/tools/check-self-assessment.py:176-197` and `tools/tsukuroi-census.sh` (`SKILL.md:307-310`): the archive-outside-repo scratch-TMPDIR move and the fixture-vs-live env rule mirror C1's relocated arm; sibling precedent exists (round 41).
- **LOW** — `chousa-shokunin/SKILL.md:734-736`: chousa's env-poisoning covers `BASH_ENV` only; `ENV`/`SHELLOPTS`/`TMPDIR` are explicitly named debt — an env-channel gap already acknowledged in a sibling, not a conflict with C1.
- **LOW** — `kumitate-shokunin/corpus/knowledge/reconcile-and-cycle.md:219`: `manifest_runway_low` is OMP manifest-budget, not host memory runway; keep the two "runway" senses distinct in mori's report.
