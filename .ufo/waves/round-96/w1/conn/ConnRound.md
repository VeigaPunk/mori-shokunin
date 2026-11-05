# ConnRound — sibling-overlap scan for mori round 96 attempt 1, wave w1

Seat: ConnRound (connector). Read-only. Only file written: this one. No tool installs. No git/jj run. No subagents.
Scope: `/home/vgpnk/Projects/shokunin/*-shokunin/` except `mori-shokunin`, plus `/home/vgpnk/Projects/shokunin/scripts`.
Method: `grep -rn` / `grep -rln` with explicit paths, `--include` limited to code extensions (`.py .sh .mjs .js .ts .json .tsv`), `.git`/`.jj` excluded, `corpus/live` and `corpus/evidence` excluded where they flooded results. Wave artifacts are listed but are sibling-owned.

## Verdicts

- **C1 (calibration, `Last change` vs MANIFEST admitted mori rows):** a new `tools/mori-scorecard-calibration.py` does **not** duplicate a sibling counter. No sibling code file compares a SCORECARD `Last change` cell against MANIFEST admitted rows; the nearest siblings compare a SCORECARD calibration/capability row against MANIFEST closure verdicts, a different cell.
- **C2 (freshness, pinned-copy digests vs `SOURCES.md`):** a new C2 counter **would** duplicate in-lane `tools/mori-source-digest.py`, which already emits the `DIGEST_CHECK … unpinned=` line the contract measures; no sibling hashes pinned copies against `SOURCES.md` recorded digests (sibling digest code checks registry-internal or in-tree digests only).

## (a) Hits: SCORECARD `Last change` / admitted / MANIFEST comparators

Overlap column: C1 = overlaps the `Last change`-vs-MANIFEST predicate; C2 = digest; "conceptual" = same method family, different object.

| # | path:line | what it does | overlap | owner |
|---|---|---|---|---|
| a1 | `kama-shokunin/tools/round58-c2-counter.py:2-18` | Frozen round-58 counter: SCORECARD **calibration row**'s "latest outside closure" pointer must equal the highest `round-N-verifier-spotcheck.md` and its verdict token must equal the MANIFEST.json `verdict` of the kama closure row for that round. | C1 conceptual (SCORECARD row vs MANIFEST closure verdict); different cell (prose pointer, calibration row only, not `Last change`); no `Last change` string. | kama (sibling) — route, do not absorb |
| a2 | `kama-shokunin/tools/round64-c2-counter.py:27-29` | Calibration row's latest outside closure equals newest `corpus/lessons/round-N-verifier-spotcheck.md`; reconciler turns false on stale pointer. | Low: compares to a lesson file, not MANIFEST. | kama — route |
| a3 | `kaidoku-shokunin/tools/round-32/c2-capability-calibration-v3.py:2-26` (also `-v2`, `-v1`) | MANIFEST round `capabilities_added` items (admitted rows) matched to SCORECARD `## Capabilities` table rows, forward and reverse. | C1 structural (MANIFEST admitted rows vs SCORECARD table); different table (capabilities, not axes `Last change`). | kaidoku — route |
| a4 | `kaidoku-shokunin/tools/round-44/c2-counter.py:52-144` | Frozen-subject counter; `SCORECARD.md`, `MANIFEST.json`, `corpus/SOURCES.md` appear only as frozen-path lists. | None (no comparison of cells to MANIFEST). | kaidoku — route |
| a5 | `tsukuroi-shokunin/tools/check-self-assessment.py:1-30` | Round-26 C2 calibration: each SCORECARD axes-table claim needs a dated "measured outcome" move record inside SCORECARD (`no dated move record`). `MANIFEST` count = 0 in this file. | C1 conceptual (axis table vs record); reference is SCORECARD prose, not MANIFEST admitted rows. Only `Last change` hit is a fixture-embedded table at line 864. | tsukuroi — route |
| a6 | `kake-shokunin/.ufo/waves/round-59/c59_axis_evidence.py:2-9` | Round-59 C1 counter: SCORECARD axis-table evidence cells (header includes `Last change`) resolve to committed state at a revision. `MANIFEST` count = 0. | Low: same table header, evidence cells, no MANIFEST. | kake wave artifact — route |
| a7 | `kagi-shokunin/corpus/claim-ledger.sh:76-88` | `cells` mode: every SCORECARD axis-row needs a resolving row-id or `corpus/stamps.tsv` pointer. | Low: pointer validity, not `Last change`, not MANIFEST. | kagi — route |
| a8 | `kama-shokunin/tools/round78-selfrecord-round77.py`, `round81-selfrecord-round80.py`, `round82-selfrecord-round81.py` (header lines 1-6) | Self-record fact re-derivation for prior rounds; grep counts MANIFEST 0/0/0, admitted 1/1/0, `Last change` 1/1/1. | Low: does not read MANIFEST. | kama — route |
| a9 | `scripts/hyaku/append-closure.py:2-7,25,126-147`; `scripts/hyaku/closure-prompt.md:79-92` | Producer of MANIFEST `rounds[]` closure entries (`admitted` true/false). Writes; does not compare. | C1 input only (the rows C1 reads are written here); no comparator. | fleet L1/operator — route |
| a10 | `kotoba-shokunin/verifiers/check_r64_routed_repairs.py:614,619`; `kumitate-shokunin/scripts/proxy-check.mjs:1594` | String templates that generate a `| Axis | … | Last change |` table header. | None (template text). | kotoba / kumitate — route |

Not C1 overlap, recorded for completeness: `kake-shokunin/scripts/source_recheck.py` (MANIFEST only as a size constant, line 46; no sha256).

## (b) Hits: source-digest / pinned-copy / `DIGEST_CHECK` / `unpinned` verifiers

- `DIGEST_CHECK` fleet-wide: **no sibling code or artifact emits it.** Hits are in mori's own tree (`mori-shokunin/.ufo/waves/round-91/w1/candidates/digest-check.py:17`, `round-92/count-c2.py:47`, `mori-shokunin/LOG.md`, `mori-shokunin/.ufo/waves/round-96/...`) and in fleet-root `MANIFEST.json` / `.ufo/reports/round-91,92/mori.md` (mori lane records).
- `unpinned=`: sibling hits are prose, wave reports, or unrelated `unpinned` usages (for example audio/game-dev `unpinned` diagnostics). No sibling verifier prints `unpinned=` as a digest count.
- `mori-source-digest` references in siblings: none.

| # | path:line | what it does | overlap | owner |
|---|---|---|---|---|
| b1 | `kagi-shokunin/corpus/sources-census.sh:1-20, 62-75, 240-320` | Registry gate for `corpus/SOURCES.md`: runs the contract census awk, and checks in-row `Fetch sha256:` digests against capture rows (`SC_FETCH`, `SC_INROW`, `reproduces-raw`). Header states "no network". Hashes row identity and capture rows only, not live bytes or pinned copies. | C2 partial (digest consistency inside the registry). Not pinned-copy verification. | kagi — route |
| b2 | `chousa-shokunin/corpus/evidence/round25-sources-census.sh:2-6` | Census of `corpus/SOURCES.md` rows; "does not fetch sources". `sha`/`digest` counts 0. | None for C2. | chousa — route |
| b3 | `game-dev-2d-shokunin/reports/round-105/r105-sources-census.sh:2-17` | Row-count and column-count awk over `corpus/SOURCES.md`. `sha`/`digest` counts 0. | None for C2. | game-dev-2d — route |
| b4 | `game-dev-3d-shokunin/reports/round-108/census.sh:1-7` | Same awk census as b3. `sha`/`digest` counts 0. | None for C2. | game-dev-3d — route |
| b5 | `kaidoku-shokunin/tools/round-35/c2-calibration-counter.py:10,71,168-198` | Counts timing of the first `corpus/SOURCES.md` change of a round against base. No digest. | None for C2. | kaidoku — route |
| b6 | `chousa-shokunin/tools/digest-in-tree.py` | `sha256` count 9, `pinned` 3; in-tree file digest. Not read beyond counts. | Unread; name as possible C2 neighbour only. | chousa — route |
| b7 | `scripts/sources-census.sh` (fleet root) | Grep for `sha256`, `pinned`, `digest`, `DIGEST`, `SCORECARD`, `MANIFEST`, `admitted`, `Last change`: **zero hits**. This is the census the contract's frontier step runs. | None: no digest check, no C1 comparator. | fleet — route |
| b8 | `kumitate-shokunin/scripts/cite-check.mjs:37-38,155,1116` | `sha256`/pin markers for git revisions in citations. Not a registry digest check. | None for C2. | kumitate — route |

## In-lane context (mori-owned; not sibling-owned; for the duplicate judgment only)

- `mori-shokunin/tools/mori-source-digest.py:1-21,466,565` — emits `DIGEST_CHECK rows=… unpinned=…`. **This is the C2 verifier the contract measures.** A new C2 counter duplicates it.
- `mori-shokunin/tools/mori-round41-calibration.py:1-16` — counts round-40 self-assessment mismatches against SCORECARD/LOG/lesson, not MANIFEST (per header; body not read).
- `mori-shokunin/tools/mori-claim-sweep.py:207`, `mori-routed-r24.py:51` — table template and prose mention of `Last change`; not counters.
- `mori-shokunin/tools/mori-scorecard-calibration.py` — absent (`ls` exit 2); C1 counter is new as the contract states.

## Conclusion

A new C1 counter does not duplicate a sibling: no sibling compares SCORECARD `Last change` cells against MANIFEST admitted rows; the closest (kama round-58, kaidoku round-32 v1-v3) compare a calibration row or capabilities table against MANIFEST closure verdicts, a different cell and predicate. A new C2 counter would duplicate `tools/mori-source-digest.py`, which already emits the measured `DIGEST_CHECK … unpinned=` line, so C2 work is pinning copies, not writing a second verifier.

## Unrun checks (named, not performed)

- No sibling counter was executed (grep and header reads only). kama round-59/62/63/64 bodies, kaidoku round-44 body, tsukuroi `check-self-assessment.py` body, chousa `digest-in-tree.py` body, kumitate `cite-check.mjs` body, and kagi `sources-census.sh` digest code paths were not read beyond the lines cited.
- Not run: `scripts/sources-census.sh validate`, `tools/mori-source-digest.py`, `tools/mori-scorecard-calibration.py` (absent), any `--selftest`.
- Not run: `git -C` reads of sibling history; no sibling tree content was verified at a revision.
- No C1 or C2 number was re-measured here; the `before` values (5 and unpinned 6) come from the frozen contract, not this seat.

## Notes for Main

- Write location: the seat task says write only `.ufo/waves/round-96/w1/conn/ConnRound.md`, while its Report line names `.ufo/waves/round-96/w1/ConnRound.md`. I followed the explicit "do not write anything except conn/ConnRound.md" bound; if the report path must be the second, the L1 should copy it.
- Scratch dir not used; no receipts kept. Nothing written outside this file.
