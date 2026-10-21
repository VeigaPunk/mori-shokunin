# C2 before state: `SURFACE waves` (seat CensusWavesSurface)

Lane mori-shokunin · round 20 · read-only. The census was not run. Its SHA-256 `87b8d680…ab28` matches the contract, and I checked it before and after my work. Evidence and reproduction scripts are in `.ufo/waves/round-20/build/CensusWavesSurface/`.

## 1. Answer in brief

- The probe is `probe_waves()`, `tools/mori-census.sh:865-932`. Its settlement rules are at `:856-864` and its emit is at `:931`.
- It reads the **fleet** wave root `/home/vgpnk/Projects/shokunin/.ufo/waves`, not this lane's `.ufo/waves`. `DEFAULT_ROOT` resolves to the parent of a `*-shokunin` lane (`:289-292`), and `WAVES_DIR` is `$ROOT/.ufo/waves` (`:295-296`, `:303`).
- Today it emits one row, `state=drift`: `total=49 settled=13 unsettled=10 aged_unsettled=10 empty=26`, plus 10 `WAVE_UNSETTLED_AGE` findings. Settled, young and empty waves get no per-wave output at all.
- It never counts per-seat reports. Its inputs are directory names at depth 1, the existence of seven named top-level files, one line-regex over four JSON files, and the newest mtime of each wave's files. It never parses dispatch members or reads report files. Confirmed statically (§5) and by fixture runs.

## 2. The probe as coded

| Step | Lines | Behaviour |
|---|---|---|
| Enumerate | `:876-879` | `for d in "$WAVES_DIR"/*`; keep directories; skip names matching `round-*` and dot names. The displayed `cmd=` text at `:866` says `find … -maxdepth 1 -mindepth 1 -type d` and does not disclose either skip. |
| Presence markers | `:881-884` | flags `has_reg`, `has_disp`, `has_run` from `swarm-registry.json`, `dispatch.json`, `run.json`. |
| Settle decision | `:890-898` | settled if `results.json`, `closeout.json`, `mission-result.json` or `closeout.md` exists at top level. Otherwise settled if the regex `"(closed\|settled)"[[:space:]]*:[[:space:]]*true` or `"status"[[:space:]]*:[[:space:]]*"closed"` matches anywhere in `swarm-registry.json`, `dispatch.json`, `run.json` or `spec.json` (line grep, no JSON parse). |
| Age | `:907-915` | `find "$d" -type f -printf '%T@\n'` (recursive, metadata only). Age = `NOW_EPOCH` − newest mtime. A failed walk increments `age_unreadable` and leaves age 0. |
| Classify | `:917-928` | settled → `n_settled`. Else, if any marker → `n_unsettled`; if age `-gt` `WAVE_UNSETTLED_S` (`:921`) → `n_aged`, a `WAVE_UNSETTLED_AGE` finding and `st=drift`. Else → `n_empty`. |
| Emit | `:931` | one row; state word is `ok` (`:875`) or `drift` (`:924`). |
| Unavailable | `:870-873` | only when `WAVES_DIR` is not a directory. |

Threshold: `WAVE_UNSETTLED_S=${MORI_WAVE_UNSETTLED_S:-7200}` (`:352`).

## 3. What it reports today (measured)

Method: `build/CensusWavesSurface/probe-waves-harness.sh` holds the probe's own lines, copied with `sed` from the census (ranges `288-303, 352, 379-393, 419-440, 561-566, 856-932`), and runs them once against the live directory. The census's `main` is neither copied nor run. Output: `waves-live-before.txt`.

```
SURFACE waves: drift (cmd=find /home/vgpnk/Projects/shokunin/.ufo/waves -maxdepth 1 -mindepth 1 -type d; total=49 settled=13 unsettled=10 aged_unsettled=10 empty=26 age_unreadable=0 threshold_s=7200; ts=2026-10-21T10:31:51Z)
```

Ten findings, all from the same run (wave, `age_s`, `reg/disp/run`):

| wave | age_s | reg/disp/run |
|---|---|---|
| shokunin12h-20261014-p1-audit | 554054 | 0/0/1 |
| shokunin12h-20261014-p2-kumitate | 553734 | 0/0/1 |
| shokunin12h-20261014-p3-kengaku | 555315 | 0/0/1 |
| shokunin12h-20261014-p4-mori-r1 | 552949 | 0/0/1 |
| shokunin12h-20261014-p5-chousa-r1 | 552036 | 0/0/1 |
| shokunin-train-20261013 | 649638 | 1/1/0 |
| shokunin-train-20261013-w2 | 643859 | 1/1/0 |
| shokunin-train-20261013-w3 | 638689 | 1/1/0 |
| shokunin-train-20261013-w4 | 635827 | 1/1/0 |
| shokunin-train-20261016-w24 | 412571 | 0/1/0 |

Per-directory classes. The companion `per-wave-breakdown.sh` applies the same predicates in the same order (`per-wave-live.txt`). Its totals are 13 / 10 / 26, with 10 aged, matching the verbatim run. It is documentation only, because the probe never emits this list.

- **settled, 13.** `shokunin12h-20261014-p1-repair` (`results.json`). `shokunin-train-20261013-w5` (top-level `"closed": true` in `swarm-registry.json`; jq path `["closed"]`). `shokunin-train-20261014-w6` to `w9`, `shokunin-train-20261101-w10` and `w11` (`closeout.json`). `shokunin-train-20261101-w12`, `w13`, `w14`, `w17`, `w18` (`closeout.md`).
- **unsettled, 10, all aged.** `shokunin12h-20261014-p1-audit`, `p2-kumitate`, `p3-kengaku`, `p4-mori-r1`, `p5-chousa-r1` (`run.json` only). `shokunin-train-20261013`, `-w2`, `-w3`, `-w4` (registry and dispatch). `shokunin-train-20261016-w24` (dispatch only).
- **empty, 26.** `aggregator-r10`, `aggregator-r10-resume`, `aggregator-r11`, `arc3-loop1-round1`, `arc3-loop1-round3`, `hyaku`, `kaidoku-r1` to `r5` (six, including `r4u`), `kaika`, `kaika-aggregate`, `kaika-w1`, `kaika-w2j`, `kaika-w3`, `luna-round-5`, `shokunin-train-20261015-w17`, `-w22`, `-w23`, `shokunin-train-20261101-w15`, `-w16`, `-w19`, `-w20`, `-w21`.
- **excluded by name, 13.** `round-9`, `round-10` to `round-17`, `round-20`, `round-21`, `round-25`, `round-89`. The lane's own `round-13` to `round-20` are not under this root.
- Non-directory entries are ignored: `.gitkeep`, `round-1.json`, `rogue-edit-audit.md`.

## 4. Presence, age and settled/unsettled: what is visible

| Fact | Computed at | Emitted as | Per-wave visible? |
|---|---|---|---|
| wave directories present | `:876-880` | `total=` | no |
| marker presence (registry, dispatch, run) | `:881-884` | folded into `unsettled=`; flags `reg/disp/run` | only for aged unsettled waves, in the finding |
| settled | `:890-898` | `settled=` | no |
| unsettled and young | `:919-925` | `unsettled=` minus `aged_unsettled=` | no |
| unsettled and aged | `:921-925` | `aged_unsettled=`, `WAVE_UNSETTLED_AGE`, `drift` | yes: `wave`, `age_s`, flags |
| empty | `:927` | `empty=` | no |
| age of a settled wave | `:915` | nowhere | no |
| unreadable age | `:909-913` | `age_unreadable=` | no |
| state word | `:875`, `:924`, `:871` | `ok` / `drift` / `unavailable` | not per wave |

The C2 contract's Problem statement (`contract.md:51-54`: "reports registry/dispatch presence and age only") is accurate in substance but incomplete. The probe also makes a wave-level settle decision (`:890-898`), and that decision is what every `settled` count means.

## 5. Per-seat reports: confirmed never counted

Yes. The full input set of `probe_waves` is:

- directory names at depth 1 (`:876-879`);
- existence of `swarm-registry.json`, `dispatch.json`, `run.json` (`:882-884`), and of `results.json`, `closeout.json`, `mission-result.json`, `closeout.md` (`:890`);
- one line regex over `swarm-registry.json`, `dispatch.json`, `run.json`, `spec.json` (`:893-895`);
- the newest mtime over all regular files under each wave directory (`:907-910`). Only the maximum is used, and no file is counted.

It never reads `taskCall`, `tasks[*]`, member `name` or `agent`, `Report:` trailers, report file names or report file counts. In the census, no `taskCall|tasks|Report:|report` match falls inside `:856-932`, and there are zero references to `mori-dispatch-ledger` or to any wave-settlement tool. The one `seat` match is a comment at `:160` about a 32-seat wave. The only report-aware check in the census is per-lane (`ps_report_closed`, `:2274-2279`, the lane's own `.ufo/reports/round-N/<lane>.md`), not a wave-seat count.

Fixture evidence (verbatim probe, fixed clock `MORI_NOW_EPOCH=1700000000`, under `/tmp`, saved as `fixture-*.txt`):

- **A → B.** A dispatch-only wave aged past the threshold, then with two seat report files added at the same old mtime: `diff` is empty (`fixture-seqA-*`, `fixture-seqB-*`).
- **B → C.** One fresh seat report added: the only changes are `aged_unsettled 1→0`, the finding disappears, and the row goes `drift→ok`. `total` and `unsettled` do not move, so report files affect only age.
- **T1.** `results.json` present and no seat reports (0 of 3): its wave is classed settled. In the combined run (`fixture-T1-T2-T4.txt`, `total=3 settled=2 unsettled=1 aged_unsettled=1`), T1 is one of the two settled waves.
- **T4.** `dispatch.json` in which `SeatA` has `"status":"closed"` while `SeatB` and `SeatC` are `running`, with no reports. The wave is classed settled.

## 6. Before-state gaps relevant to C2 (not fixed here; design inputs)

1. **Settlement is one file-level token, not a seat count.** T1 and T4 above show a wave settled with 0 of 3 reports, and with 2 of 3 members not closed. In the live tree the only grep-based settle is `shokunin-train-20261013-w5`, a wave-level `"closed": true`, so no live false settle from a member token was found. The structure still allows one.
2. **Dispatch shape is not uniform.** `shokunin-train-20261013-w3` and `-w4` have no `taskCall` key at all (`has_taskCall: false`; top-level keys `count, dispatched_at, lanes, wave` and `agent_count, agents, dispatched, wave`). `shokunin-train-20261013` and `-w2` have 26 `taskCall.tasks`, and `shokunin-train-20261016-w24` has 20 (`checks-dispatch-discovery.txt`). The contract's `taskCall: null` rule (`contract.md:68`) covers a null value, not an absent key. [INFERENCE: the C2 tool needs an explicit rule for an absent key.]
3. **Report-path trailers are absent from probe-visible dispatches.** None of the 11 depth-2 `dispatch.json` files contains `Report: write your scoped findings to`. The only fleet JSON with that text is `hyaku/jj-w1/dispatch.json`, at depth 3, outside the probe's view. The lane's own `.ufo/waves/round-*` JSON carries the trailer in 20 files (for example `round-13/dispatch.json`).
4. **Discovery is name-based and shallow.** The probe sees 11 depth-2 `dispatch.json` names: 8 without a `schema` key, 3 with `ufo-swarm-wave-dispatch-v1`. Across 330 fleet JSON files at any depth, 10 carry that schema. The C2 contract discovers by schema at any depth (`contract.md:64-67`).
5. **Markers can vanish into `empty`.** `aggregator-r10` and `aggregator-r10-resume` were unsettled in the r10 baseline and are `empty` now. The drift-r12 classification records this and says disappearance does not prove settlement (`corpus/evidence/drift-r12-20261019T2204Z-classification.md:33,41`). `empty` also holds `kaika-w3` (80 files, including `canonical-closeout.md`; the exact-name test at `:890` does not match it) and the container `hyaku`.
6. **Age is not settlement.** Any write to any file in a wave directory resets the clock (`:907-915`). `corpus/knowledge/audit-r11.md:202` (D07) records this as an open calibration boundary.
7. **The displayed command is not the traversal.** `cmd=` names `find … -type d`, which lists 62 depth-1 directories today. The probe counts 49, because `:879` skips 13 `round-*` names and the row does not say so. There is also a latent symlink defect. `[ -d "$d" ]` (`:877`) follows links, but `find` without `-L` does not descend a symlinked start point. In the fixture (`fixture-symlink-wave.txt`), `link-wave` is counted in `total` and `unsettled` and is not aged, although its only file has the same old mtime as `plain-wave`, which is aged. [INFERENCE: the read returned nothing, so age is 0; age is not emitted.] No symlinks exist at wave depth today (count 0).
8. **Typed-token branches have no selftest.** The census selftest exercises `results.json` (fixture `wave-settled`, `:3185-3188`) and aged, young and unreadable unsettled waves (`:3532-3547`, `:3550-3555`, `:4355-4367`). No fixture creates `closeout.json`, `closeout.md`, `mission-result.json`, or a `"closed"`, `"settled"` or `"status":"closed"` token. The census matches for `closeout|mission-result|"closed"` fall only at `:885-895`, all in the probe itself.
9. **Blank output line.** `:2711-2712` loops over `"${arr[@]:-}"`, which prints one empty line when no `FINDING` row exists. I observed this in the harness on a zero-finding fixture (`fixture-seqC-*`). The live census's clean-run output is [INFERENCE]. This does not touch the waves row, but it may matter for C1 line pairing, which I did not analyse.

## 7. Knowledge notes against the code

| Note | What it says | Status |
|---|---|---|
| `corpus/knowledge/observability-surfaces-r2.md:141-165` (§2 waves) | Typed tokens; `round-*` and dot exclusion; newest-mtime age; aged finding; "never called failed"; gaps. | Matches the code. Stale pointers: `:4-7` (waves probe `:247`, `run_census :568-574`) and `:143-149` (`:258-261`, `:272-281`, `:283-285`, `:291-295`, `:87`, `:246`). The current probe is `:856-932` and the threshold `:352`. Gap at `:161-165` (no typed-token fixture) is still true (§6.8). "Counted but neither classified nor explained" (`:161-162`) is still true: `empty` is count-only. |
| `corpus/knowledge/observability-census-r1.md:12-13, 107-118, 128-130` | Table row; typed-token erratum; `w1`–`w4` "surface silence" caveat; "must not auto-settle a wave still being written". | Consistent with the code. The `w1`–`w4` caveat is still open. |
| `corpus/knowledge/audit-r11.md:202` (D07) | Open calibration boundary: age is newest mtime, not dispatch or terminal history. | Still accurate. |
| `corpus/knowledge/surfaces-r7.md:223-225` | Waves field set unchanged in r7. | The keys in §8 match the current emitters at `:871` and `:931`. |
| `corpus/evidence/drift-r12-20261019T2204Z-classification.md:33,41` | Deleted markers make waves drop out without proving settlement. | Still true (§6.5). |
| `corpus/knowledge/dispatch-ledger-r18.md` | Dispatch attempts bound to payload (`tools/mori-dispatch-ledger.py`). | Not referenced by the census (zero hits); not part of this surface. |

No knowledge note defines a per-seat settlement rule. The C2 contract is the first.

## 8. Emitted key names (quoted from the emitters)

- SURFACE row, `:931`: `cmd`, `total`, `settled`, `unsettled`, `aged_unsettled`, `empty`, `age_unreadable`, `threshold_s`, `ts`.
- SURFACE unavailable row, `:871`: `cmd`, `waves_dir`, `path`, `ts`.
- FINDING `WAVE_UNSETTLED_AGE`, `:923`: `wave`, `age_s`, `threshold_s`, `reg`, `disp`, `run`, `settle`. Envelope, `:424`: `severity`, `obs`, `ts`, `script_sha256`.
- Verdict, `:2714-2715`: `MORI_CENSUS: <ROLL> (findings= drift= unavailable= surfaces=)`.

## 9. Commands, outputs and installs

- Harness: `probe-waves-harness.sh` → `waves-live-before.txt`. Census SHA before and after: `87b8d680…ab28`.
- Companion: `per-wave-breakdown.sh` → `per-wave-live.txt`.
- Fixtures (under `/tmp`, removed; copies kept): `fixture-T1-T2-T4.txt`, `fixture-seqA-dispatch-only.txt`, `fixture-seqB-plus-2-old-seat-reports.txt`, `fixture-seqC-plus-fresh-seat-report.txt`, `fixture-symlink-wave.txt` (via `link-fixture.sh`).
- Checks: `checks.sh` → `checks-dispatch-discovery.txt`.
- Not run: `tools/mori-census.sh` in any mode, any selftest, any build or linter.
- Tool installs or updates: none. Host tools used as already present: `bash`, `find`, `grep`, `sed`, `sha256sum`, `touch`, `mktemp`, `jq`.

## 10. Verification gaps

- The harness reproduces the probe's own lines, but its stdout is not the census's stdout. The census roll with the other surfaces is not shown here.
- Per-seat coverage of the 13 settled waves was not evaluated; that is the C2 tool's scope. I did not compare the 10 aged waves' declared report paths with files on disk, because they carry no trailers (§6.3).
- The blank-line behaviour of a live census (§6.9) is [INFERENCE].
