# SeatNaming — OMP transcript naming map (mori round 17, wave 1)

Seat: `MoriR17.SeatNaming-5`. Leaf member; no subagent dispatch. Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (entering tip `24526ea`). Read-only filename census: the sessions directory was never written, moved or probed with anything but reads. This file is the only write.

## Headline

1. The layout is depth 1: root `<Seat>.jsonl` is a top-level session (L1, closure, or probe); `<Parent>/<Parent>.<Task>-<N>.jsonl` is a subagent transcript of top-level session `<Parent>`; `<pid>.<tool>.log` is a per-tool I/O log. 24/24 nested dirs equal a root L1 stem, 2399/2399 nested stems begin with `<dir>.`, and no nested dir nests further.
2. The C1 prefix rule (`contract.md:33-34`: prefix = text before the first `.`) is exact but **prefix ≠ lane identity** whenever the top-level session was respawned: `SoujiR17-3` carries 150 seats and is the round-17 souji lane, while `--prefix SoujiR17` matches **zero** seats and exits 0 with `MORI_SEAT_TERMINAL_OK` — a silent false clean.
3. The dir is **not round-scoped**: seats split R15 4, R16 625, R17 1190, R18 367, R19 246, R21 1, no-round 76. 69 of 110 prefixes are hyaku-jj probe sessions and 7 are harness probes — not lanes.
4. Trailing `-N` exists on **two independent axes**: lane generation (`SoujiR17-3`, `ClosureKaidokuR18-3`, `ClosureKamaR16-3`) and seat generation (`-2`…`-5`, 735/2399 nested seats). Prior generations are not retained as files except six `KamaR17.Connect*` pairs, so `-N` is a naming tag, not a death count.
5. The `.md` companion is the seat's yield artifact: observed live during this scan, seat `.md` count grew 2395 → 2473 (MoriR17 3 → 49) while jsonl stayed at 2509. Useful as corroboration for `completed`; never as a C1 class input.

## Target and snapshot

- Target (`S`): `/home/vgpnk/.omp/agent/sessions/-Projects-shokunin/2026-10-20T12-57-31-587Z_01a15963-70c3-7390-a1b4-7911b9506d07`
- Interface: `.ufo/waves/round-17/contract.md:32-34` (seat id / prefix / `--prefix` equality) and `:66` ("prefixes are naming conventions, not authenticated lane membership").
- Method: `os.walk(S, followlinks=False)` + filename aggregation only. The single content read is the permitted-field tail of six root sessions (§7.5): `type`, `message.role`, `message.stopReason` only.
- Snapshot `T = 2026-10-20T19:01:17Z`; the directory is live (files 12615 → 12799 and seat `.md` 2395 → 2473 between 18:56Z and 19:01Z). Treat every count below as a point sample.

| measure | value |
|---|---:|
| regular files (walk, depth ≤1) | 12799 |
| directory size | 2.2 GiB |
| `*.jsonl` seats | 2509 (root 110 + nested 2399) |
| `*.md` files | 2494 (root 103 + nested 2370 + url-search 21) |
| seat `.md` coverage | 2473/2509 (missing 36) |
| `*.log` tool logs | 7488 |
| distinct prefixes | 110 (single-seat: 86) |
| symlinks | 0 |
| max dir depth | 1 |
| stems with >1 dot / duplicate stems / odd chars | 0 / 0 / 0 |

Log grammar: `10006.bash.log` — every one of the 7488 logs matches `<pid>.<tool>.log`, tool ∈ {bash 5454, bash-original 1079, read 727, eval 225, async 3}. They are tool I/O, never seat transcripts; a C1 walker filtering `*.jsonl` excludes them correctly.

## 1. Naming grammar (observed)

```
S/<SeatName>.jsonl                          top-level session  (seat id = stem)
S/<SeatName>.md                             yield recap       (same stem; written at yield)
S/<Parent>/<Parent>.<Task>-<N>.jsonl        subagent of <Parent> (seat id = stem)
S/<Parent>/<Parent>.<Task>-<N>.md           its yield recap
S/<pid>.<tool>.log                          tool I/O log (root only)
```

Invariants verified over the whole tree at T:

- `S/SoujiR17-3.jsonl` (L1) ↔ `S/SoujiR17-3/SoujiR17-3.ConnLessonGateSection-2.jsonl` (subagent). Every nested dir has its root L1: 0 dirs without `S/<dir>.jsonl`.
- Every nested stem starts with `<dir>.` (2399/2399); no nested stem is dot-free; no third-level dir.
- Seat id = peer id. Verified against the live roster: `MoriR17.CensusJj-5` → `S/MoriR17/MoriR17.CensusJj-5.jsonl`; `KamaR17.ReopenS046` → `S/KamaR17/KamaR17.ReopenS046.jsonl`; L1 ids `MoriR17`, `TameshiR17`, `MadoR19` → `S/<id>.jsonl`.
- `local/` is empty (0 files); `url-search/` is a web-search cache (329 files: 308 sources + 21 `.md` with opaque stems such as `S/url-search/15oob9dy0jxfj.md`; 0 `.jsonl`).

## 2. Root-level inventory (110 files = 18 lane + 16 closure + 69 jj + 7 probe)

- **Lane L1s (18):** `KaidokuR17`, `KaidokuR18`, `KaidokuR19`, `KamaR16`, `KamaR17`, `MadoR17`, `MadoR18`, `MadoR19`, `MoriR17`, `SoujiR16`, `SoujiR17-3`, `TabiR16`, `TabiR17`, `TabiR18`, `TameshiR16`, `TameshiR17`, `TsukuroiR17`, `TsukuroiR18-2`. Two of them have no subagent dir (`TabiR18`; `TsukuroiR18-2`, which appeared mid-scan).
- **Closure L1s (16):** `ClosureKaidokuR17`, `ClosureKaidokuR18-3`, `ClosureKamaR16-3`, `ClosureSoujiR16`, `ClosureTabiR15`, `ClosureTabiR17`, `ClosureTameshiR16`, `ClosureTsukuroiR17`, plus 8 root-only single-file closures (`ClosureKakeR21`, `ClosureMadoR16/17/18`, `ClosureMoriR16`, `ClosureSoujiR15`, `ClosureTabiR16`, `ClosureTsukuroiR16`). All 8 multi-seat closures have a dir.
- **Hyaku-jj probes (69):** `JjAudit` 27, `JjTrial` 22, `JjDoc` 12, `JjCritic` 2, `JjLane` 2, `JjRevenger` 2, `JjConnector` 1, `JjSentinel` 1 — every one a single-seat root session, all suffixed `-2`/`-3`.
- **Harness probes (7):** `ProbeScoutFlash`, `ProbeTaskFlash`, `SmokeFlashCascade`, `SmokeOpusCascade`, `SmokeZflCascade`, `RuntimeFallbackOwner-2`, `RuntimeRevivedCompletion-2`.

Round split (by `R<digits>` token in the prefix; 110 prefixes / 2509 seats):

| round | prefixes | seats |
|---|---:|---:|
| R15 | 2 | 4 |
| R16 | 11 | 625 |
| R17 | 12 | 1190 |
| R18 | 6 | 367 |
| R19 | 2 | 246 |
| R21 | 1 | 1 |
| no-round (`Jj*`, `Probe*`, `Smoke*`, `Runtime*`) | 76 | 76 |

R17 prefixes are: `KaidokuR17`, `KamaR17`, `MadoR17`, `MoriR17`, `SoujiR17-3`, `TabiR17`, `TameshiR17`, `TsukuroiR17`, `ClosureKaidokuR17`, `ClosureMadoR17`, `ClosureTabiR17`, `ClosureTsukuroiR17`.

## 3. Nested `<Parent>/` directories (24)

All 24 are session subtrees; seat count, `.md` count, and the trailing-`-N` mix (∅ = no suffix):

| dir | kind | seats | seat `.md` | trailing `-N` mix |
|---|---|---:|---:|---|
| `KaidokuR17` | lane | 147 | 147 | -3:78, -∅:69 |
| `KaidokuR18` | lane | 187 | 187 | -∅:187 |
| `KaidokuR19` | lane | 90 | 90 | -∅:90 |
| `KamaR16` | lane | 160 | 160 | -∅:160 |
| `KamaR17` | lane | 162 | 155 | -2:82, -3:6, -∅:74 |
| `MadoR17` | lane | 148 | 148 | -∅:148 |
| `MadoR18` | lane | 167 | 167 | -∅:167 |
| `MadoR19` | lane | 154 | 153 | -2:1, -∅:153 |
| `MoriR17` | lane | 70 | 49 | -5:70 |
| `SoujiR16` | lane | 144 | 144 | -4:79, -∅:65 |
| `SoujiR17-3` | lane | 149 | 149 | -2:71, -∅:78 |
| `TabiR16` | lane | 157 | 157 | -5:84, -∅:73 |
| `TabiR17` | lane | 164 | 164 | -2:86, -∅:78 |
| `TameshiR16` | lane | 144 | 144 | -3:1, -∅:143 |
| `TameshiR17` | lane | 174 | 174 | -2:107, -∅:67 |
| `TsukuroiR17` | lane | 153 | 153 | -2:70, -∅:83 |
| `ClosureKaidokuR17` | closure | 6 | 6 | -∅:6 |
| `ClosureKaidokuR18-3` | closure | 7 | 7 | -∅:7 |
| `ClosureKamaR16-3` | closure | 4 | 4 | -∅:4 |
| `ClosureSoujiR16` | closure | 4 | 4 | -∅:4 |
| `ClosureTabiR15` | closure | 2 | 2 | -∅:2 |
| `ClosureTabiR17` | closure | 4 | 4 | -∅:4 |
| `ClosureTameshiR16` | closure | 1 | 1 | -∅:1 |
| `ClosureTsukuroiR17` | closure | 1 | 1 | -∅:1 |

Every dir holds exactly one prefix and it equals the dir name (24/24); no file is cross-attributed inside a dir.

## 4. `-N` suffixes: two axes, one grammar

- **Lane axis (top-level).** Root stems ending `-N`: 71 at `-2`, 4 at `-3`, 35 unsuffixed. Lane L1s among them: `SoujiR17-3`, `ClosureKaidokuR18-3`, `ClosureKamaR16-3`; `TsukuroiR18-2` appeared mid-scan. Their base names (`SoujiR17`, `ClosureKaidokuR18`, `ClosureKamaR16`, `TsukuroiR18`) have **zero** files anywhere in `S`.
- **Seat axis (nested).** 2399 nested seats: ∅ 1664, `-2` 417, `-3` 85, `-4` 79, `-5` 154 (30.6% suffixed). All 70 `MoriR17` subagents are `-5` (wave-1 generation); `SoujiR17-3` mixes `-2` (71) and ∅ (78), so the seat suffix is independent of the lane suffix on the same file.
- **Meaning.** Trailing `-N` is the spawn occurrence of that name, not a round or dimension: the only same-base multi-file cases in the whole tree are six `KamaR17` pairs (`ConnectTsukuroi`, `ConnectTameshi`, `ConnectKumitate`, `ConnectSouji`, `ConnectKaidoku`, `ConnectKagi`, each `-2` + `-3`), and the live roster names the current instances `-3`. Prior generations left no file in the other cases, so **`-N` cannot be used to count deaths**. [INFERENCE: ordinal = Nth spawn of that name; whether a respawn renames or recreates was not probed — mutation forbidden.]
- **Do not normalize blindly.** `R15`–`R21`, `GameDev2d/3d`, and `V2` contain digits but are not suffixes. Only an anchored `-(\d+)$` on the **first** segment (before the first `.`) is a lane generation; a trailing `-(\d+)$` after the first `.` is a seat generation. Example: `S/SoujiR17-3/SoujiR17-3.ConnLessonGateSection-2.jsonl` → lane `SoujiR17` (generation 3), seat `ConnLessonGateSection` (generation 2).

## 5. Prefix table (complete, 110 rows)

Generated from the same snapshot; `root` + `nested` = `total`.

| prefix | kind | root | nested | total |
|---|---|---:|---:|---:|
| `KaidokuR18` | lane | 1 | 187 | 188 |
| `TameshiR17` | lane | 1 | 174 | 175 |
| `MadoR18` | lane | 1 | 167 | 168 |
| `TabiR17` | lane | 1 | 164 | 165 |
| `KamaR17` | lane | 1 | 162 | 163 |
| `KamaR16` | lane | 1 | 160 | 161 |
| `TabiR16` | lane | 1 | 157 | 158 |
| `MadoR19` | lane | 1 | 154 | 155 |
| `TsukuroiR17` | lane | 1 | 153 | 154 |
| `SoujiR17-3` | lane | 1 | 149 | 150 |
| `MadoR17` | lane | 1 | 148 | 149 |
| `KaidokuR17` | lane | 1 | 147 | 148 |
| `SoujiR16` | lane | 1 | 144 | 145 |
| `TameshiR16` | lane | 1 | 144 | 145 |
| `KaidokuR19` | lane | 1 | 90 | 91 |
| `MoriR17` | lane | 1 | 70 | 71 |
| `TabiR18` | lane | 1 | 0 | 1 |
| `TsukuroiR18-2` | lane | 1 | 0 | 1 |
| `ClosureKaidokuR18-3` | closure | 1 | 7 | 8 |
| `ClosureKaidokuR17` | closure | 1 | 6 | 7 |
| `ClosureKamaR16-3` | closure | 1 | 4 | 5 |
| `ClosureSoujiR16` | closure | 1 | 4 | 5 |
| `ClosureTabiR17` | closure | 1 | 4 | 5 |
| `ClosureTabiR15` | closure | 1 | 2 | 3 |
| `ClosureTameshiR16` | closure | 1 | 1 | 2 |
| `ClosureTsukuroiR17` | closure | 1 | 1 | 2 |
| `ClosureKakeR21` | closure | 1 | 0 | 1 |
| `ClosureMadoR16` | closure | 1 | 0 | 1 |
| `ClosureMadoR17` | closure | 1 | 0 | 1 |
| `ClosureMadoR18` | closure | 1 | 0 | 1 |
| `ClosureMoriR16` | closure | 1 | 0 | 1 |
| `ClosureSoujiR15` | closure | 1 | 0 | 1 |
| `ClosureTabiR16` | closure | 1 | 0 | 1 |
| `ClosureTsukuroiR16` | closure | 1 | 0 | 1 |
| `JjAuditAudio-2` | jj | 1 | 0 | 1 |
| `JjAuditChousa-2` | jj | 1 | 0 | 1 |
| `JjAuditClosurePrompt-2` | jj | 1 | 0 | 1 |
| `JjAuditFleetCommit-2` | jj | 1 | 0 | 1 |
| `JjAuditGameDev2d-2` | jj | 1 | 0 | 1 |
| `JjAuditGameDev3d-2` | jj | 1 | 0 | 1 |
| `JjAuditInlineSh-2` | jj | 1 | 0 | 1 |
| `JjAuditKagi-2` | jj | 1 | 0 | 1 |
| `JjAuditKaidoku-2` | jj | 1 | 0 | 1 |
| `JjAuditKake-2` | jj | 1 | 0 | 1 |
| `JjAuditKama-2` | jj | 1 | 0 | 1 |
| `JjAuditKasegi-2` | jj | 1 | 0 | 1 |
| `JjAuditKengaku-2` | jj | 1 | 0 | 1 |
| `JjAuditKotoba-2` | jj | 1 | 0 | 1 |
| `JjAuditKotodama-2` | jj | 1 | 0 | 1 |
| `JjAuditKumitate-2` | jj | 1 | 0 | 1 |
| `JjAuditLore-2` | jj | 1 | 0 | 1 |
| `JjAuditMado-2` | jj | 1 | 0 | 1 |
| `JjAuditMori-2` | jj | 1 | 0 | 1 |
| `JjAuditPromptText-2` | jj | 1 | 0 | 1 |
| `JjAuditRevenger-2` | jj | 1 | 0 | 1 |
| `JjAuditSouji-2` | jj | 1 | 0 | 1 |
| `JjAuditSourcesCensus-2` | jj | 1 | 0 | 1 |
| `JjAuditTabi-2` | jj | 1 | 0 | 1 |
| `JjAuditTameshi-2` | jj | 1 | 0 | 1 |
| `JjAuditTsukuroi-2` | jj | 1 | 0 | 1 |
| `JjAuditWatchdog-2` | jj | 1 | 0 | 1 |
| `JjConnectorProvinces-2` | jj | 1 | 0 | 1 |
| `JjCriticProtocol-2` | jj | 1 | 0 | 1 |
| `JjCriticRollback-2` | jj | 1 | 0 | 1 |
| `JjDocAutoTrack-2` | jj | 1 | 0 | 1 |
| `JjDocConcurrency-2` | jj | 1 | 0 | 1 |
| `JjDocGitIndex-2` | jj | 1 | 0 | 1 |
| `JjDocHeadAttachment-2` | jj | 1 | 0 | 1 |
| `JjDocHooksAttributes-2` | jj | 1 | 0 | 1 |
| `JjDocIdentity-2` | jj | 1 | 0 | 1 |
| `JjDocImmutable-2` | jj | 1 | 0 | 1 |
| `JjDocLargeRepo-2` | jj | 1 | 0 | 1 |
| `JjDocOpLogGrowth-2` | jj | 1 | 0 | 1 |
| `JjDocPush-2` | jj | 1 | 0 | 1 |
| `JjDocRecovery-2` | jj | 1 | 0 | 1 |
| `JjDocWorktrees-2` | jj | 1 | 0 | 1 |
| `JjLaneHelper-3` | jj | 1 | 0 | 1 |
| `JjLaneHelperV2-2` | jj | 1 | 0 | 1 |
| `JjRevengerLaneJjState-2` | jj | 1 | 0 | 1 |
| `JjRevengerPriorProbe-2` | jj | 1 | 0 | 1 |
| `JjSentinelHelper-2` | jj | 1 | 0 | 1 |
| `JjTrialAudio-2` | jj | 1 | 0 | 1 |
| `JjTrialChousa-2` | jj | 1 | 0 | 1 |
| `JjTrialFleetRoot-2` | jj | 1 | 0 | 1 |
| `JjTrialGameDev2d-2` | jj | 1 | 0 | 1 |
| `JjTrialGameDev3d-2` | jj | 1 | 0 | 1 |
| `JjTrialKagi-2` | jj | 1 | 0 | 1 |
| `JjTrialKaidoku-2` | jj | 1 | 0 | 1 |
| `JjTrialKake-2` | jj | 1 | 0 | 1 |
| `JjTrialKama-2` | jj | 1 | 0 | 1 |
| `JjTrialKasegi-2` | jj | 1 | 0 | 1 |
| `JjTrialKengaku-2` | jj | 1 | 0 | 1 |
| `JjTrialKotoba-2` | jj | 1 | 0 | 1 |
| `JjTrialKotodama-2` | jj | 1 | 0 | 1 |
| `JjTrialKumitate-2` | jj | 1 | 0 | 1 |
| `JjTrialLore-2` | jj | 1 | 0 | 1 |
| `JjTrialMado-2` | jj | 1 | 0 | 1 |
| `JjTrialMori-2` | jj | 1 | 0 | 1 |
| `JjTrialRevenger-2` | jj | 1 | 0 | 1 |
| `JjTrialSouji-2` | jj | 1 | 0 | 1 |
| `JjTrialTabi-2` | jj | 1 | 0 | 1 |
| `JjTrialTameshi-2` | jj | 1 | 0 | 1 |
| `JjTrialTsukuroi-2` | jj | 1 | 0 | 1 |
| `ProbeScoutFlash` | probe | 1 | 0 | 1 |
| `ProbeTaskFlash` | probe | 1 | 0 | 1 |
| `RuntimeFallbackOwner-2` | probe | 1 | 0 | 1 |
| `RuntimeRevivedCompletion-2` | probe | 1 | 0 | 1 |
| `SmokeFlashCascade` | probe | 1 | 0 | 1 |
| `SmokeOpusCascade` | probe | 1 | 0 | 1 |
| `SmokeZflCascade` | probe | 1 | 0 | 1 |

## 6. Flags: where the prefix rule misattributes a lane

| id | severity | name(s) | seats | why the prefix misattributes | evidence |
|---|---|---|---:|---|---|
| F1 | **high** | `SoujiR17-3` | 150 | Lane is `SoujiR17` (fleet lane `souji-shokunin`, round 17); prefix is the respawn identity. `--prefix SoujiR17` → 0 seats, `totals` all zero, exit 0, `MORI_SEAT_TERMINAL_OK`: a false clean. | `S/SoujiR17-3.jsonl`, `S/SoujiR17-3/SoujiR17-3.ConnLessonGateSection-2.jsonl`; no `SoujiR17` prefix exists |
| F2 | **high** | whole dir (110 prefixes) | 2509 | Dir mixes rounds R15–R21 and the hyaku-jj probe wave; a whole-dir scan reports other rounds as current. Prefix is the only round handle (no round field in the path). | §2 round table |
| F3 | med | `ClosureKaidokuR18-3`, `ClosureKamaR16-3` | 8 / 5 | Closures respawned too; base `ClosureKaidokuR18` / `ClosureKamaR16` have zero files. A closure census keyed on the base name misses them. | table rows; `S/ClosureKaidokuR18-3/…` |
| F4 | med | `Closure<Lane>` (16 prefixes) | 45 | Closure is a role, not a lane. Substring joins conflate `ClosureKaidokuR17` (7) with `KaidokuR17` (148); equality is correct but must be documented. | `S/ClosureKaidokuR17.jsonl` vs `S/KaidokuR17.jsonl` |
| F5 | med | `Jj<Role><Lane>-2` (69 prefixes) | 69 | Same lane split by role and generation: 21 labels appear as both `JjAudit*` and `JjTrial*`; 6 Audit-only, 1 Trial-only. A per-prefix lane tally yields 69 “lanes” for 28 lane labels. | e.g. `JjAuditMori-2` vs `JjTrialMori-2` |
| F6 | low | `JjLaneHelper-3`, `JjLaneHelperV2-2` | 1 / 1 | Same helper family across a version tag and a generation; `-2` is a suffix while `V2` is part of the name. | table rows |
| F7 | low | `Probe*`, `Smoke*`, `Runtime*` (7) | 7 | Harness probes, not lanes; each becomes a 1-seat prefix that looks like a lane in `by_prefix`. | table rows |
| F8 | low | all 18 lane prefixes | 2388 | The L1 and its subagents share one prefix (`MoriR17` = 1 L1 + 70 subs). Prefix-level class tallies mix the L1’s terminal state with its children’s; depth distinguishes them. | root vs nested columns |
| F9 | low | `TabiR18`, `TsukuroiR18-2` | 1 / 1 | Lane L1s with no subagent dir; every other lane L1 has one (16/16 dirs; closures 8/8). Not a misattribution, but breaks a “dir ⇔ lane” assumption. | table rows |
| F10 | info | `url-search/`, `local/` | 329 / 0 | Non-session subtrees inside the same dir. C1’s `*.jsonl` filter excludes them today; a broader walker would mint 21 phantom prefixes from the cache `.md` names. | `S/url-search/15oob9dy0jxfj.md` |
| F11 | info | seat-level `-N` | 735 | Must not be folded into the lane. `S/SoujiR17-3/SoujiR17-3.ConnLessonGateSection-2.jsonl` has both axes on one stem. | §4 |
| F12 | info | fleet-dir → prefix join | — | Prefixes are CamelCase lane labels; fleet dirs are kebab (`kama-shokunin`). `game-dev-2d-shokunin` → `GameDev2d` shows the join is not `title(strip(-shokunin))`. | fleet-root listing; `JjAuditGameDev2d-2` |

## 7. Consequences for C1 (`tools/mori-seat-terminal.py`)

1. **`by_prefix` will have 110 keys**, 86 of them single-seat (78%). Top keys: `KaidokuR18` 188, `TameshiR17` 175, `MadoR18` 168. Any acceptance case asserting a prefix set must use the respawn-aware names, not lane names.
2. **False-clean path (F1).** `--prefix SoujiR17` is a legal invocation that selects nothing: `totals` all zero, `seats: []`, exit 0, `MORI_SEAT_TERMINAL_OK`. A fixture pack should pin this explicitly (`SoujiR17` → 0 seats OK; `SoujiR17-3` → 150 seats) so the semantics are chosen, not accidental. The contract’s own caveat at `:66` covers it, but the exit-code consequence does not.
3. **`files_scanned` population.** `S` holds 12799 regular files but only 2509 `*.jsonl`. If `--max-files` is applied before extension filtering, today’s dir already consumes 64% of the 20000 default (12799/20000); after filtering it is 12.5%. The limit should state which population it counts.
4. **Tail truncation is the normal path.** 2269/2509 seats (90.4%) exceed the default `--max-tail-bytes` 262144; 415 exceed 1 MiB; max 5,866,818 B; min 78,925 B; median 648,196 B. The “drop first partial line” rule runs on 90% of real files — fixtures must include a tail whose first line is split, not treat it as an edge.
5. **`.md` pairing (corroboration only).** At T, 2473/2509 seats have a `.md`; the 36 without are the live/incomplete set: root `KamaR17`, `MadoR19`, `MoriR17`, `TameshiR17`, `TsukuroiR18-2`, `RuntimeFallbackOwner-2`, `RuntimeRevivedCompletion-2`; nested `MoriR17` 49/70, `KamaR17` 155/162, `MadoR19` 153/154. All six root sessions that were md-less at 18:56Z (before `TsukuroiR18-2` existed) ended their tail in `assistant/toolUse` or `toolResult` (C1 `incomplete`), and the 38 `KamaR17` seats md-less at 18:56Z all matched live roster peers (7 remained md-less at T). Longitudinal check: between 18:56Z and 19:01Z, `MoriR17` `.md` went 3 → 49 while its jsonl stayed 70 — the file appears at yield. Use as a hint only [INFERENCE: exact writer].
6. **Symlinks.** 0 in `S`, so “never follow symlinks” is untriggered in production; a fixture must synthesize one.
7. **Seat id semantics hold.** Seat id = peer id = file stem; verified against 11 live roster ids and 3 L1 ids. Naming is case-sensitive; `MoriR17` is not `mori-shokunin`.

## 8. Confidence and remaining unknowns

- **Observed (high):** all counts and tables at T; the 24/24 dir↔L1 and 2399/2399 stem-prefix invariants; 0 symlinks / 0 duplicate stems / 0 multi-dot stems; the six `KamaR17` same-base pairs; the live `.md` growth; roster-id equality; exit codes of the commands in §9.
- **[INFERENCE]:** `-N` = Nth spawn occurrence; `.md` written at yield; the directory is a project bucket holding many top-level sessions (the dir name matches none of the 110 root stems; the harness rule was not read from docs).
- **Unknown:** why only six prior-generation files survive; whether a respawn renames the old file or recreates (no mutation allowed, so not probed); whether `session_init`/`customType` records carry a parent or spawn marker (not read — outside the permitted field set for this seat’s need).

## 9. Reproduction (read-only; exit codes recorded)

All run against `S` at ~18:58–19:00Z:

| command | result | rc |
|---|---|---:|
| `find "$S" -maxdepth 1 -type f \| wc -l` | 7695 (7701 at T) | 0 |
| `find "$S" -maxdepth 1 -mindepth 1 -type d \| wc -l` | 26 (24 session + `local` + `url-search`) | 0 |
| `find "$S" -type f -name '*.jsonl' \| wc -l` | 2509 | 0 |
| `find "$S" -type l \| wc -l` | 0 | 0 |
| `find "$S" -maxdepth 1 -type f -name '*.log' \| wc -l` | 7482 (7488 at T) | 0 |
| `find "$S" -maxdepth 1 -type f -name '*.md' \| wc -l` | 103 | 0 |
| `du -sh "$S"` | 2.2G | 0 |

Prefix census (python3, stdlib only, filename-only): walk with `os.walk(S, followlinks=False)`, keep `*.jsonl`, `seat = basename[:-6]`, `prefix = seat.split('.',1)[0]`, count per prefix and compare with the containing dir name. Live drift note: the jsonl population was stable at 2508→2509 across five minutes while `.log` and `.md` grew by ~105 and ~78 files.

## Not edited

No VCS command, no mutating jj command, no pacman transaction, no tool install, no scratch file. The sessions directory, the lane checkout, `.ufo/state`, `MANIFEST.json`, fleet scripts/templates and sibling reports were not modified. Report path: `.ufo/waves/round-17/build/SeatNaming.md`.
