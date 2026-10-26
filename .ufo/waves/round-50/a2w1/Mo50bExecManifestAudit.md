# Mo50bExecManifestAudit — fleet record vs mori closure files (round 50, wave a2w1)

Lane: mori-shokunin (detection and report only). Seat: leaf executor, no subagents (labrat not used).
Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bExecManifestAudit/` (created with `TMPDIR` set to its `tmp/`,
removed after the figures were transcribed — see §9). No tool was installed or upgraded this seat.
No file outside this report was written; the lane repo, the fleet repo and `git` indexes were read only.

Frozen inputs read (never edited): `.ufo/waves/round-50/contract.md`, `count-c1.py` (read to learn how the
premise derives N*, not run). Data under test: the fleet `MANIFEST.json` at
`e014499613f63f8a467821219b0296121119ca53`, the lane's `corpus/lessons/round-N-verifier-spotcheck.md`
for rounds 36–49, and the landed `SCORECARD.md` at `487941b9395e89678af0053cc443cdb49cdee6e3`.

## 0. Method and digests

```
$ git -C /home/vgpnk/Projects/shokunin rev-parse --short HEAD
1ce0f8fb
$ git -C /home/vgpnk/Projects/shokunin show e01449961...:MANIFEST.json > manifest-pinned.json   # rc 0
$ git -C /home/vgpnk/Projects/shokunin show HEAD:MANIFEST.json           > manifest-head.json    # rc 0
$ sha256sum manifest-pinned.json manifest-head.json
a94551c5bc8d0cc09a753cf7a8f72708f6b74c8f9b71b4fedb55105f71d4cabc  manifest-pinned.json
870cc64bc731268586dcee38a09606f0263ce35d06b3174ae993c4991fe4fab3  manifest-head.json
$ git -C .../shokunin rev-parse e01449961...:MANIFEST.json
8fb88171a7be7de748ad5ebeacbe05058e24497d
$ git -C .../shokunin hash-object --stdin < manifest-pinned.json
8fb88171a7be7de748ad5ebeacbe05058e24497d
```

The `sha256` of the bytes I analysed is `a94551c5bc8d…`, i.e. exactly the digest the entering receipt prints
(`evidence/control-c1-do-nothing.txt`: `manifest=a94551c5bc8d`), and the blob equals the pinned revision's
blob. **The cross-check below reads the same MANIFEST bytes the frozen premise names.** All comparisons are
between two committed surfaces (fleet `MANIFEST.json` rows and lane `corpus/lessons/*.md` bytes); no claim
grade was re-judged, only whether the two records agree.

## 1. Every mori closure entry in the fleet record

Extraction by `type == "closure"` and mori membership gave **49 mori closure entries**, rounds 1–49, in both
the pinned and the HEAD copy. Two field shapes exist:

| shape | rounds | identifying field | `verdict` / `verdicts` |
|---|---|---|---|
| modern | 12–49 (38 entries) | `"lane": "mori"`, `"lane_round": N` | present |
| legacy | 1–11 (11 entries) | only `"lanes": {"mori": …}` + `"lane_rounds": {"mori": N}` | **absent** — admission is prose in `notes` ("mori round 3 admitted") |

Mori entry key inventory (union over rounds 12–49): `admitted, campaign, capabilities_added, claim_head,
claims, closed_at, commit, date, lane, lane_round, lane_rounds, lanes, minted, notes, producer_commit,
promotions, rejection_streak_impact, report, report_addendum_commit, report_commit, round, trends, type,
verdict, verdicts, verification`. There is **no numeric score field** anywhere in a mori entry — the only
`score` substrings are prose in `notes` / `verification` / `capabilities_added`. This confirms C1's named
limit "MANIFEST holds verdicts, not scores" as a property of the record, not an assumption.

Rounds 36–49 verdicts as recorded:

| round | MANIFEST `verdict` | per-axis `verdicts` (as recorded) |
|---|---|---|
| 36 | admitted | operability=improved; **`freshness-technique`=unprovable-but-better** (1 axis key + 1 non-axis key) |
| 37 | admitted | calibration=improved, operability=improved, coverage/depth/freshness/adjacency=unchanged |
| 38 | admitted | calibration=improved, operability=improved, depth=improved, coverage/freshness/adjacency=unchanged |
| 39 | admitted | calibration=improved, operability=improved, depth=improved (**3/6 keys**) |
| 40 | rejected-honest-stop | operability=unprovable, depth=unprovable, coverage/freshness/calibration/adjacency=unchanged |
| 41 | admitted | operability=improved, depth=improved, calibration=improved, coverage/freshness/adjacency=unchanged |
| 42 | rejected-honest-stop | operability=unprovable, calibration=improved, depth=improved, coverage/freshness/adjacency=unchanged |
| 43 | admitted | operability=improved, calibration=improved, coverage/depth/freshness/adjacency=unchanged |
| 44 | admitted | calibration=improved, operability=improved, depth=improved, coverage/freshness/adjacency=unchanged |
| 45 | rejected-harmed | operability=improved, **calibration=harmed**, depth=improved, coverage/freshness/adjacency=unchanged |
| 46 | admitted | calibration=improved, coverage/operability/depth/freshness/adjacency=unchanged |
| 47 | admitted | calibration=improved, depth=improved, operability=improved, coverage=improved, freshness/adjacency=unchanged |
| 48 | admitted | calibration=improved, depth=improved, coverage/operability/freshness/adjacency=unchanged |
| 49 | admitted | calibration=improved, depth=improved, coverage/operability/freshness/adjacency=unchanged |

Rounds 12–35 (same extraction, for the full record; axis keys C=coverage, O=operability, D=depth,
F=freshness, K=calibration, A=adjacency):

| round | verdict | verdicts |
|---|---|---|
| 12 | admitted | A=unchanged, C=improved, D=improved, F=unchanged, K=improved, O=unchanged |
| 13 | rejected-harmed | A=harmed, C=harmed, D=unchanged, F=unchanged, K=unchanged, O=improved |
| 14 | admitted | A=improved, C=improved, D=unchanged, F=unchanged, K=unchanged, O=unchanged |
| 15 | admitted | A=unchanged, C=improved, D=unchanged, F=unchanged, K=unchanged, O=unchanged |
| 16 | admitted | A=unchanged, C=improved, D=unchanged, F=unchanged, K=unchanged, O=unchanged |
| 17 | rejected-harmed | A=harmed, C=improved, D=unchanged, F=unchanged, K=improved, O=improved |
| 18 | admitted | A=improved, C=unchanged, D=unchanged, F=unchanged, K=improved, O=improved |
| 19 | admitted | A=improved, C=unchanged, D=unchanged, F=unchanged, K=improved, O=unchanged |
| 20 | rejected-harmed | A=unchanged, C=improved, D=unchanged, F=harmed, K=harmed, O=unchanged |
| 21 | admitted | A=unchanged, C=unchanged, D=unchanged, F=improved, K=improved, O=unchanged |
| 22 | admitted | A=unchanged, C=unchanged, D=unchanged, F=unchanged, K=improved, O=unchanged |
| 23 | rejected-honest-stop | A=unchanged, C=unprovable, D=unchanged, F=unchanged, K=improved, O=unchanged |
| 24 | admitted | A=unchanged, C=improved, D=unchanged, F=unchanged, K=improved, O=unchanged |
| 25 | admitted | A=unchanged, C=improved, D=unchanged, F=unchanged, K=improved, O=unchanged |
| 26 | admitted | A=unchanged, C=improved, D=unchanged, F=improved, K=unchanged, O=unchanged |
| 27 | rejected-honest-stop | A=unchanged, C=unchanged, D=improved, F=unchanged, K=unchanged, O=unchanged |
| 28 | admitted | A=unchanged, C=unchanged, D=unchanged, F=improved, K=unchanged, O=improved |
| 29 | rejected-honest-stop | A=unchanged, C=unchanged, D=unchanged, F=unchanged, K=improved, O=unchanged |
| 30 | rejected-honest-stop | A=unchanged, C=unchanged, D=improved, F=unchanged, K=unchanged, O=unchanged |
| 31 | admitted | A=unchanged, C=unchanged, D=improved, F=unchanged, K=unchanged, O=improved |
| 32 | rejected-honest-stop | A=unchanged, C=unchanged, D=unchanged, F=unprovable-but-better, K=unchanged, O=unchanged |
| 33 | rejected-honest-stop | A=unchanged, C=unchanged, D=unprovable, F=unchanged, K=unchanged, O=unchanged |
| 34 | rejected-honest-stop | A=unchanged, C=unprovable, D=unchanged, F=unchanged, K=unprovable-but-better, O=unchanged |
| 35 | rejected-honest-stop | A=unchanged, C=unchanged, D=unchanged, F=unchanged, K=unprovable, O=unchanged |

Rounds 1–11: no `verdict`, no `verdicts`, no `admitted` field — nothing per-axis to extract (F5). Their
`notes` prose records the outcomes ("mori round 1 … closed ok", "mori round 2 admitted", …, "mori round 11
admitted WITH CORRECTION").

## 2. Axis-by-axis comparison, 36–49 (MANIFEST vs spot-check)

Format: round — MANIFEST axes; spot-check source (file:line) and its axis verdicts; delta.
`ok` = every axis the spot-check grades has the same value in MANIFEST.

| round | spot-check source | spot-check grades | MANIFEST vs spot-check |
|---|---|---|---|
| 36 | `round-36-verifier-spotcheck.md:25` (`Verdict: **improved**.`), `:32` (`Verdict: **unprovable-but-better**.`), `:24` (owned axis not harmed) | operability improved; exploratory claim unprovable-but-better, explicitly "never asserted as a freshness verdict" (`:31`) | ok (value agrees; key name differs — F1) |
| 37 | `:38`–`:43` axis table | calibration improved, operability improved, freshness/coverage/depth/adjacency unchanged | ok (6/6) |
| 38 | `:28` C1 "axis improved", `:41` C2 "axis improved", `:51` C3 "axis improved", `:72` score rows identical | calibration/operability/depth improved; other three not graded, score rows unchanged | ok |
| 39 | `:26` C1 improved, `:31` C2 "improved (defects named)", `:33` C3 improved, `:35` "held axes unchanged by declaration" | calibration/operability/depth improved; other three unchanged by declaration | ok (3/6 explicit — F2) |
| 40 | `:128` operability unprovable, `:132` depth unprovable, `:135` four axes unchanged | as MANIFEST | ok (6/6) |
| 41 | `:88`–`:91` | operability/depth/calibration improved; coverage/freshness/adjacency unchanged | ok (6/6) |
| 42 | `:97`–`:102` table | operability unprovable, calibration improved, depth improved, three unchanged | ok (6/6) |
| 43 | `:159`–`:164` table | operability/calibration improved; coverage/depth/freshness/adjacency unchanged | ok (6/6) |
| 44 | `:16`–`:18` claim table ("calibration improved", "operability improved", "depth improved"), `:20` "Other axes unchanged" | three improved; three unchanged (implicit) | ok |
| 45 | `:46`–`:48` claim table, `:66` "**calibration: harmed**", `:70`–`:71` per-axis line | operability improved, calibration harmed, depth improved, coverage/freshness/adjacency unchanged | ok (6/6) |
| 46 | `:45`–`:50` table | calibration improved; operability/depth/coverage/freshness/adjacency unchanged | ok (6/6) |
| 47 | `:65`–`:70` table | calibration/depth/operability/coverage improved; freshness/adjacency unchanged | ok (6/6) |
| 48 | `:67`–`:72` table, `:63` "No axis is harmed" | calibration/depth improved; coverage/operability/freshness/adjacency unchanged | ok (6/6) |
| 49 | `:75`–`:80` table | calibration/depth improved; coverage/operability/freshness/adjacency unchanged | ok (6/6) |

Counts: 14 rounds × 6 axes = **84 axis cells. 76 cells have an explicit MANIFEST value and 76 of 76 agree**
with the spot-check; the other 8 cells (round 36: coverage, depth, freshness, calibration, adjacency; round 39:
coverage, freshness, adjacency) have **no MANIFEST key at all**, and the matching spot-check statement is
"unchanged"/"not harmed" — absence, not contradiction (F2).

Secondary surface, fleet `trends` (`expansion`, `quality`, `discernment`) = 14 rounds × 3 = **42 cells, all
explicit, 42/42 agree**, including the non-trivial ones: round 44 `discernment=unprovable-but-better` (`:36`),
round 45 `quality=harmed` (`:92`), round 46 `expansion/quality=unchanged` (`:56`–`:57`), round 38
`improved (bounded)`×3 (`:103, :106, :110`) normalised to `improved`.

**Result: no axis or trend disagreement in rounds 36–49.**

## 3. Round-level `verdict` comparability

Six spot-checks state the round ruling and all six agree with MANIFEST:

| round | spot-check ruling | line | MANIFEST |
|---|---|---|---|
| 37 | "Admission on the corrected state" | `:115` | admitted |
| 38 | "no axis harmed — **admitted**" | `:141` | admitted |
| 39 | "**Admit.**" | `:56` ("Ruled on the honest-stop framing") | admitted |
| 40 | "**Rejected (rejected-honest-stop).**" | `:11` | rejected-honest-stop |
| 41 | "**Admitted.**" | `:12` | admitted |
| 43 | "**Admit.**" | `:228` | admitted |

The other eight (36, 42, 44, 45, 46, 47, 48, 49) carry **no round-level admit/reject word**: they grade
claims and axes only. MANIFEST's `verdict` for those rounds is therefore not cross-checkable from the closure
file (F3).

## 4. Pinned vs fleet HEAD — did any later closure re-grade a mori round?

Per-entry canonical-JSON comparison of round 12–49 mori rows (and of the 1–11 legacy rows) between
`e0144996` and `1ce0f8fb`:

```
mori row diffs: 0
total round entries pinned/head: 750 751
only pinned: 0   only head: 1
ADDED: {'round': 45, 'lane': 'kama', 'lane_round': 45, 'verdict': 'rejected-honest-stop',
        'type': 'closure', 'date': '2026-10-26'}
top key version/repo/protocol/roster/minting_rule: same
mori mentions with round > 49: []
non-closure mori entries: rounds 0 only ('mint'/'ops')
```

**No mori closure row (rounds 1–49) was re-graded, re-dated, re-verdicted or re-noted between the pinned
revision and fleet HEAD.** The single added entry is another lane's (kama round 45, 2026-10-26). The pinned
revision is therefore a stable read of the mori record for the C1 premise.

## 5. The premise's own derivation, recomputed

Independent recomputation from the pinned MANIFEST (lane `mori`, `lane_round ≤ 49`, grade ∈ {improved, harmed},
max round), then compared with the landed `SCORECARD.md` `## Axes` table at `487941b9`:

| axis | N* recomputed (grade) | landed Last-change first `round N` | agrees | landed Evidence cell names |
|---|---|---|---|---|
| coverage | 47 (improved) | 47 | yes | `corpus/lessons/round-47-verifier-spotcheck.md` (exists at R) |
| operability | 47 (improved) | 47 | yes | `…round-47-verifier-spotcheck.md` |
| depth | 49 (improved) | 49 | yes | `…round-49-verifier-spotcheck.md` |
| freshness | 28 (improved) | 28 | yes | `…round-28-verifier-spotcheck.md` |
| calibration | 49 (improved) | 49 | yes | `…round-49-verifier-spotcheck.md` |
| adjacency | 19 (improved) | 19 | yes | **`MANIFEST.json`** (no `round-19-verifier-spotcheck.md` at R — confirmed absent in `git ls-tree 487941b9 -- corpus/lessons/`) |

Robustness check: recomputing without the `verdict == "admitted"` filter (i.e. letting rejected rounds' grades
count) yields the **identical six N\***. The rejected mori rounds that carry an `improved` or `harmed` grade at
all are 13, 17, 20, 23, 27, 29, 30, 42 and 45; the highest of them per axis is 17 (adjacency, `harmed`), 20
(coverage, `improved`; freshness and calibration, `harmed`), 23/29 (calibration, `improved`), 42/45 (depth,
`improved`; operability, `improved`), and every one of those is below the admitting round for the same axis —
adjacency 19, coverage 47, freshness 28, calibration 49, depth 49, operability 47. So the frozen predicate's
admitted-filter is non-binding at this revision, and
no N* rests on the accept/reject decision of a contested round.

N* rulings independently corroborated in the closure files: round 47 coverage `:68` and operability `:67`
improved; round 49 calibration `:75`, depth `:76` improved; round 28 freshness `:92` improved. For adjacency
`round-19-verifier-spotcheck.md` does not exist, but the lane's own closure record grades it —
`corpus/lessons/round-19.md:10` "C1 adjacency, score 6 held" at
`2061780117e6ca637725004897bd288d3ba7e988` — and the Axes cell's pointer is exact: at fleet commit
`63729047`, `MANIFEST.json` `rounds[398]` is `{"round": 19, "lane": "mori", "lane_round": 19,
"verdict": "admitted", "verdicts": {"adjacency": "improved", …}}`.

## 6. Pointer resolution (fleet record → lane closure files)

For rounds 36–49, every `verification.spotcheck` value is a `path@sha` and all 14 resolve:

```
36..49: ptr_ok  path_in_commit  identical_at_entering_tip      (14/14, no exceptions)
```
i.e. the cited commit exists in the lane, the file exists in it, and the file bytes are byte-identical at the
cited commit and at the entering tip `7197160b927f04db294c9553fb48fadcc7a3f4e3` — no spot-check has been
edited after the fleet record named it.

Every mori entry's `verification.spotcheck`/`report` pointer was checked: **38/38 `report` blobs**
(`.ufo/reports/round-N/mori.md`) resolve at the pinned fleet revision (0 missing), and the 38 closure
`commit` fields split on `@` resolve in the lane and are ancestors of the entering tip:

```
36 4890c2d571  37 afc55a7634  38 13f3db7e5c  39 44151c5bd8  40 ede486b7a0  41 9de7323de4
42 e3a2b58f72  43 1429c791db  44 554ff41645  45 12c89ea634  46 2f04605ab1  47 dd17d927ff
48 14c5110d65  49 43d846669e            (each: cat-file -t = commit; merge-base --is-ancestor → rc 0)
```

## 7. What this cross-check does and does not settle

- Settled: for rounds 36–49 the fleet record's per-axis verdicts, trend verdicts, closure commits and
  spot-check pointers are faithful to the lane's closure files, and the pinned MANIFEST is unchanged at HEAD.
  C1's premise ("MANIFEST is the fleet record of the closures") holds on every row I could compare.
- Not settled: whether any grade is *correct*. I compared records, not evidence: I did not re-open the
  SOURCES rows, quotes, counters or receipts inside any spot-check, and I ran none of the lane's gates.

## 8. Named limits of this check

1. Scope window is rounds 36–49 as assigned. Rounds 12–35 were read only where the premise needs them
   (rounds 28 and 19); a full 12–35 axis comparison was not performed.
2. Rounds 1–11 have no `verdict`/`verdicts` fields, so no per-axis comparison is possible for them (F5).
3. Round-level `verdict` is not stated in 8 of the 14 spot-checks (F3); agreement there is unverified, not
   disputed.
4. Four spot-checks do not present a six-row axis table: 36 (one axis explicit), 39 (three), 38 and 44 (three
   each, the rest implicit) — F2/F4.
5. `verdicts` maps omit unmoved axes for rounds 36 and 39 (F2), so "grade absent" and "grade unchanged" are
   indistinguishable from the fleet record alone for those cells.
6. The counter `count-c1.py` was read, not executed; no figure in this report is a counter output.

## 9. Scratch

`/fast/scratch/hyaku/mori-r50/Mo50bExecManifestAudit/` (two MANIFEST copies, one SCORECARD copy, `tmp/`) was
removed with `rm -rf` after the figures above were transcribed; nothing cited here lives only in scratch.
No clone was made; all git access was `show`/`cat-file`/`rev-parse`/`hash-object`/`diff --quiet`/
`merge-base --is-ancestor`/`ls-tree` on the existing repositories. Disk guard read before work:
`/fast/scratch/hyaku 24% use, 613.3G free`.

## Findings

1. **MED — mori rounds 1–11 are closure entries with no `lane`, `verdict`, `verdicts` or `admitted` field**
   (`MANIFEST.json` at `e01449961…`, rounds 1–11; admission appears only as prose in `notes`). The mori
   closure count is extraction-dependent: **49** by `lanes.mori`/`lane_rounds.mori`, **38** by
   `lane == "mori"`. The frozen counter's `manifest_targets()` keys on `r.get("lane") != lane` and therefore
   sees 38. No N* impact at this revision (those rows carry no per-axis grades), but any future consumer that
   counts mori closures or scans `verdicts` by the `lane` field silently drops 11 rounds.
2. **LOW — round 36's `verdicts` carries the non-axis key `freshness-technique`**
   (`MANIFEST.json` at `e01449961…`, mori round 36). It is the only non-axis key in any mori `verdicts` map
   (checked over rounds 12–49). The value faithfully mirrors `round-36-verifier-spotcheck.md:31`–`:32`, which
   refuses to grade the freshness axis ("never asserted as a freshness verdict"), but a consumer enumerating
   the six axis names sees a ghost entry and finds no `freshness` key for round 36.
3. **LOW — `verdicts` omits unmoved axes for rounds 36 (1/6) and 39 (3/6)** while every round 37–38 and 40–49
   records 6/6 (`MANIFEST.json` at `e01449961…`). The matching spot-checks state the omission's meaning
   (`round-36-…:24` "Owned axis not harmed"; `round-39-…:35` "held axes unchanged by declaration"), so this
   is absence, not contradiction — but the fleet record alone cannot answer "did round 39 grade coverage
   unchanged?", and 8 of the 84 comparison cells are undecidable for that reason.
4. **LOW — 8 of 14 spot-checks carry no round-level admit/reject verdict** (rounds 36, 42, 44, 45, 46, 47, 48,
   49 of `corpus/lessons/round-N-verifier-spotcheck.md`); they grade claims/axes only. MANIFEST's `verdict`
   for those rounds is the fleet closure's own decision and is not cross-checkable at this surface. The six
   that do state a ruling (37 `:115`, 38 `:141`, 39 `:56`, 40 `:11`, 41 `:12`, 43 `:228`) all agree with
   MANIFEST.
5. **LOW — three unmoved axes are graded only implicitly in rounds 38 and 44**
   (`round-38-…:72` score rows identical, `round-44-…:20` "Other axes unchanged"). MANIFEST's
   `unchanged` for those cells is a supported default, not a stated grade; treat them as weaker evidence than
   a row-by-row verdict.
6. **INFO — no disagreement found between MANIFEST and the closure files in rounds 36–49**: 76/76 explicit
   axis cells and 42/42 trend cells agree; 0 mori rows differ between the pinned revision and fleet HEAD
   (the only added round entry is kama round 45); 14/14 spot-check pointers resolve byte-identically at the
   cited commit and at the entering tip; 38/38 `report` blobs and 38/38 closure commits resolve. **This seat
   therefore contributes no calibration finding against C1's premise** — the premise's observed-state side is
   faithful on every comparable row.
7. **INFO — the premise's N\* is invariant to the admitted-filter** (recomputed with and without it: identical
   47/47/49/28/49/19), and the landed Axes cells at `487941b9` match the recomputed N* on all
   six rows, including the `MANIFEST.json`-only fallback for adjacency (verified at `63729047`
   `rounds[398]`, corroborated by `corpus/lessons/round-19.md:10`).
