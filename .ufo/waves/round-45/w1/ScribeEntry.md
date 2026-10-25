# ScribeEntry — mori round 45, wave 1

Seat: `L1Mori45.ScribeEntry` (leaf; no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`, tip `3ad8faaa637ae466c61f9427fea1c208bf49ea82`.
Artifact landed: `corpus/knowledge/census-cgroup-levels-r45.md` — **66 lines** (`wc -l`), under the 90-line cap.

## Behavior

Read the two staged shokuknow entries (theme adopted, their `file://` sources rejected), the
opened kernel copy, and `tools/mori-census.sh`; then wrote the round's one admitted entry with
`source: S473`, `verified-at: 2026-10-25`, a two-command `recheck:`, `coverage-map: FR1, FR12`,
`ground: FR12` + boundary, and the five required sections. Also executed the census three times
against fixture cgroup trees, ran the selftest baseline plus three mutants on private copies, and
ran a pin/drift pair. Two files written in total: the entry and this report. The census was read,
never edited; no `git` mutation was run.

## Gates (commands and observed output)

| # | command (abridged) | observed | rc |
|---|---|---|---|
| 1 | `sha256sum .ufo/waves/round-45/assimilation/opened/cgroup-v2.rst.src` | `a9433bb0…b7ad` | 0 |
| 2 | `curl -fsSL --max-time 40 …/cgroup-v2.rst \| sha256sum` | `a9433bb0…b7ad` (URL reproduces the copy) | 0 |
| 3 | `sha256sum tools/mori-census.sh` | `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28` | 0 |
| 4 | census, `MORI_CGROUP_LOCAL_EVENTS=<absent>` + service `oom_kill 3` | `obs=local_oom_kill=3 path=…/absent-memory.events.local` | 1 |
| 5 | census, local mode-000 holding `oom_kill 7` + service `3` | `obs=local_oom_kill=3 path=…/local-memory.events.local` | 1 |
| 6 | census, local and service both absent | `SURFACE cgroup: ok … local_oom_kill=unavailable`; `CGROUP_OOM_KILL` matches `0` | 1 |
| 7 | `bash tools/mori-census.sh --selftest` (TMPDIR = wave tmp) | `MORI_CENSUS_SELFTEST: PASS (134 cases, 134 passed, 0 failed)` | 0 |
| 8 | mutant M1 (delete `:1710-1711`) `--selftest` | `PASS (134 cases, 134 passed, 0 failed)`; live: `local_oom_kill=unavailable` | 0 |
| 9 | mutant M2 (`path=${LOCAL_EVENTS}` → `path=${SERVICE_EVENTS}`) | `PASS (134 cases, 134 passed, 0 failed)`; live: `path=…/service-memory.events` | 0 |
| 10 | mutant M3 (finding value → `local_oom_kill=0`) | `PASS (134 cases, 134 passed, 0 failed)`; live: `local_oom_kill=0` | 0 |
| 11 | `--pin` then `--drift` over one fixture dir, only the local counter changed 1→2 | `MORI_DRIFT: +FINDING:DISK_LOW -FINDING:DISK_CRITICAL`; no cgroup field, no cgroup line | pin 0 / drift 1 |
| 12 | `drift_normalize` (extracted verbatim from the script) on rows differing only `local_oom_kill=1` vs `=2` | two canonical lines identical (`NORMALIZED-EQUAL`) | 0 |
| 13 | verifier: every quote located, counted, and matched against its source file | 17/17 `entry=True src=True`, all ≤25 words, labels match | 0 |
| 14 | `wc -l corpus/knowledge/census-cgroup-levels-r45.md` | `66` | 0 |

Mutants were built on copies under `TMPDIR=.ufo/waves/round-45/tmp/ScribeEntry/{M1,M2,M3}`; the
lane file was never written. Census live mode is documented and observed as write-free (receipts
4–6, 11 wrote nothing outside the wave tmp tree).

## Quotes in the entry, with word count and location

Count method: whitespace-separated tokens (`str.split()`), computed by the verifier in gate 13.

| quote (abridged) | words | location |
|---|---|---|
| `service_oom_kill='' … elif … fi` branch block | 20 | `tools/mori-census.sh:1707-1712` |
| `field must not claim the file does not exist` | 9 | `:1748` (comment block `:1747-1749`) |
| `local_oom_kill=$service_oom_kill path=${LOCAL_EVENTS} (local counter: …)` | 9 | `:1844` |
| `MORI_CGROUP_SERVICE_EVENTS="$FX/cgroup/memory.events"` | 1 | `:3253` |
| `check 'drift: CGROUP_OOM_KILL' 1 DRIFT` | 5 | `:3907` |
| `'FINDING CGROUP_OOM_KILL'` | 2 | `:3908` |
| `ledger_round local_oom_kill max mem_fill_pct mem_peak not_open` | 6 | `:2747` |
| `-e "s/\\b(${cre})=[0-9]+/\\1=<V>/g"` | 2 | `:2791` |
| `MORI_DRIFT: +FINDING:DISK_LOW -FINDING:DISK_CRITICAL` | 3 | this run, gate 11 |
| `all fields in this file are hierarchical … down the hierarchy` | 22 | `cgroup-v2.rst.src:1474-1476` |
| `For the local events at the cgroup level see memory.events.local.` | 10 | `:1476-1477` |
| `Similar to memory.events but the fields in the file are local … not hierarchical.` | 17 | `:1518-1519` |
| `the parent slice's `1` is a propagated count, and `memory.events.local` reads `0`` | 12 | `observability-census-r1.md:135` |
| `the bare `oom_kill=` is still the parent cumulative counter … as `local_oom_kill=`` | 20 | `surfaces-r7.md:88-90` |
| `the read alone separates none of these` | 7 | `pid-probe-conclusion-r44.md:53` |
| `PASS (134 cases, 134 passed, 0 failed)` | 7 | this run, gate 7 |
| `a PSI trigger watcher is resident … is not evidence of no stall` | 20 | `PROVINCE.md:55` |

Receipt lines A/B/C in the entry are ≤13 words each (gate 13 checked the upper bound).

## Touched surfaces

- `corpus/knowledge/census-cgroup-levels-r45.md` — created, 66 lines, 8.4 KB.
- `.ufo/waves/round-45/w1/ScribeEntry.md` — this report.
- Scratch only: `.ufo/waves/round-45/tmp/ScribeEntry/` (fixtures `rA`, `rB`, `rC`, `rD`, mutant
  trees `M1`–`M3`, `selftest-base.txt`, `pinD.txt`, `dn.sh`).

Unchanged, by intent: `tools/mori-census.sh`, `corpus/SOURCES.md`, `corpus/README.md`,
`SKILL.md`, `SCORECARD.md`, `LOG.md`, `corpus/QUALITY.md`, `contract.md`, every other seat's report.

## Findings

1. **Silent preference order.** `:1707-1712`: local `.events.local` → service hierarchical
   `memory.events` → empty. With both files absent the surface is `ok` and only the row's
   `local_oom_kill=unavailable` records anything; no state or path says which file was missing,
   while `:1747-1749` states the opposite discipline for `CGROUP_PRESSURE`.
2. **Constant provenance cell.** `:1844` hard-wires `path=${LOCAL_EVENTS}`. Receipt 5 is the proof:
   the named file's bytes read `oom_kill 7`, the printed value is the service file's `3`.
3. **Level-blind selftest.** `:3253-3254` pin three level paths to one fixture file; the fixture
   creates only `memory.events` (`memory.events.local` appears at `:1698`, `:1701`, `:1705` and
   nowhere as a fixture); the sole cgroup assertion is the bare finding id. Three behaviour-changing
   mutants each keep `PASS (134 cases…)`.
4. **Drift mask.** `local_oom_kill` is in `DRIFT_COUNTER_KEYS` (`:2747`) and is rewritten to `<V>`
   (`:2791`); the end-to-end drift named no cgroup field while the counter moved 1→2 (its only
   reported deltas were unrelated live disk findings, so the drift verdict itself is not evidence
   of cleanliness beyond the absent cgroup line).

## Deviations from the steering message (reported verbatim, not resolved)

- The message named the order at `1705-1712`; the branch itself is `1707-1712`, with defaults at
  `1705-1706`. The entry cites the branch as `1707-1712` and the defaults separately.
- "Nothing is emitted when the local file is absent or unreadable" — measured more narrowly: the
  row does emit `local_oom_kill=unavailable` when both files are missing; what is not emitted is an
  absent/unreadable *state* for either events file. The entry states the narrower form.
- The census's absent-vs-unreadable rule at `:1747-1749` is written for `CGROUP_PRESSURE`, not as a
  general rule. The entry scopes it that way rather than asserting it governs every path.
- The census digest in the entry is `87b8d680…b977ab28`, matching the steering message's `87b8d68…`.

## Out of scope (not written by this seat)

- `corpus/SOURCES.md` row `S473` (`mined`, `used-by corpus/knowledge/census-cgroup-levels-r45.md`).
  `S473` was free at read time: the registry's last row is `S472` (`corpus/SOURCES.md:249-251`).
- `corpus/README.md` coverage-map row naming the entry.
- Any round-45 `count-c3.py` / census arm counter; none exists yet in `.ufo/waves/round-45/`.
- No install, upgrade, or tool change was made, so no tooling record is due.

## Lane state observed (not mine)

`git status --porcelain` at hand-off shows my two files as the only ones I created (`?? corpus/knowledge/census-cgroup-levels-r45.md`, `?? .ufo/waves/round-45/w1/ScribeEntry.md`); `tools/mori-census.sh`, `corpus/SOURCES.md` and `corpus/README.md` are clean. The worktree also carries peer changes I did not make and did not touch: `M .ufo/waves/round-45/contract.md` (+28 lines) and six modified `tools/*` files. The contract diff appends "Correction 1" (C1 `moved>=1`, C2 `tables>=7`, C3 `--entering-rev` requiring the entry absent at that revision); my entry is absent at the entering tip — `git cat-file -e 3ad8faaa…:corpus/knowledge/census-cgroup-levels-r45.md` → `fatal: … not in '3ad8faaa…'`, rc 128 — so Correction 1 item 3 holds for it. Nothing in Correction 1 changes the entry's required fields or sections.

## Limits

- Receipts 4–12 live under the wave tmp tree, not in a committed evidence file; the entry embeds
  their load-bearing bytes instead of a path, and gate 13 re-checked every embedded string.
- The entry's `recheck:` pins the census digest, so it is designed to fail loudly when the census
  changes (an intentional drift detector, not a content check).
- No commit was made in the lane (read-only `git log`/`show`/`diff`/`status`/`ls-files` only).
