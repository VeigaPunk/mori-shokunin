# MoriR20.TokSilenceA — C1 token classification

Tokens: `+subject_commits -subject_commits +window -window -attribution -rowb_files`
(drift receipt `.ufo/waves/round-20/evidence/c1-drift-entering.json`, census `--drift corpus/evidence/baseline-r10-20261015T2231Z.json`, measured commit `2061780117e6…`, rc 1).

## Method and bounds

Read-only throughout; `tools/mori-census.sh` was **not** run (lane bounds; the receipt's captured output is the ground truth being explained). No tools installed. Verified before analysis:

- `sha256sum tools/mori-census.sh` → `87b8d680b9b2572e89977a10ff9b91630fbaf689f23f4892e06be427b977ab28` = the receipt's `census_sha256` (working tree ≡ measured script).
- `git show 5be8943:tools/mori-census.sh | sha256sum` → `d7710981aa1c…` = the baseline header's `census_sha256` (baseline-r10 file line 2). So pin census = 5be8943's, measured census = 87b8d680.

## How these six tokens are produced (mechanics, path:line)

- `--drift` token grammar: `tools/mori-census.sh:195-201` — "a changed value names its key; a removed/added field names -key/+key; a removed/added line names -\<id\>/+\<id\>".
- Line pairing: `drift_report()` `tools/mori-census.sh:2874-2910` (pass 1 exact strings, pass 2 same-id; `SURFACE:lane.X` ids are unique per lane, so each ±field token localizes to one lane's baseline-vs-current line pair).
- Field diff: `drift_field_report()` `tools/mori-census.sh:2849-2868`; `-$k` at `:2862`, `+$k` at `:2866`.

⇒ All six tokens are **field-presence changes on matched `SURFACE:lane.X` lines**, i.e. lane-row transitions. Row emit sites (current 87b8d680 / pinned d7710981 — byte-identical pairs):

| row | fields emitted | current | pinned (5be8943) |
|---|---|---|---|
| row-A progressing | `subject_commits=yes window=launch..NOW` | :2472-2473 | :1379-1380 |
| row-B progressing | `rowb_files=<V> attribution=inference example=<V>` | :2493-2494 | :1400-1401 |
| row-6 not-open | `reason=committed-report round=<V> path=…` (dup `round` ⇒ changed-value token) | :2410-2411 | :1339-1340 |
| row-8 young | `reason=age_le_gate gate_s=7200` | :2377 | :1325-1326 |

`ps_report_closed()` `tools/mori-census.sh:2274-2291` (identical rule at 5be8943, only the rev moved HEAD→`refs/heads/<branch>` in r17 `273aa74`, documented in-script :2288-2297): report must exist at the root rev **and** the newest commit touching `.ufo/reports/round-<N>/<lane>.md` must have ct ∈ (launch, NOW]. This is why the aggregator's September round-10 report (`f5d8507`, 2026-09-28T23:41:38-03) does **not** close its 2026-10-15T01:50:57-03 launch — at both pin and measurement.

## The three lane transitions that produce all six tokens

Anchor = last `launch <lane> round=<N>` in `.ufo/watchdog.log` (ledger), measurement window 2026-10-21 07:18:05–07:19:49-03 (receipt `observed_at`).

1. **aggregator row-B → row-A** (baseline line :14 → row-A). Trigger: subject commit `1bcf59e` 2026-10-19T22:17:33-03 "aggregator round 12: review all physical lane corpora" by `aggregator-shokunin <aggregator@shokunin.local>` on `refs/heads/master`, inside (launch 1792039857, measurement] — verified via `git log refs/heads/master --since=@1792039857 … -- . ':(exclude).ufo' ':(exclude,glob)**/*-shokunin/**'` (aggregator is a root lane, `is_root_lane` :2016). Pair emits: `+subject_commits +window -rowb_files -attribution -example` (+ shared `basis` change).
2. **kagi / kengaku / kake / kumitate row-A → row-6** (baseline lines :20/:16/:17/:18). Each has an anchor-round report at `refs/heads/master` whose newest commit is in (launch, measurement]: kagi round-24 (`01d1c22` 03:32:37, later amended by `1eed508` 07:07:09; launch 02:43:10), kengaku round-26 (`9a28017` 05:54:27; launch 02:22:27), kake round-23 (`4487889` 06:01:39; launch 03:26:44), kumitate round-38 (`204807e` 05:09:07; launch 04:04:24). Pair emits per lane: `-subject_commits -window +reason +path` + changed dup-`round` + `basis`. (Excludes row-4 `ledger-close` — no `+path` — and row-7 `round-advanced` — would add `+anchor_round`, absent from the receipt.)
3. **kama row-A → row-8 young** (baseline line :21). Relaunched `2026-10-21T07:17:03-03 launch kama round=21` (ledger), age ≈ 62–106 s ≤ gate 7200 (`:360`), so row-8 fires before the report check (ladder order :2377 < :2410). Pair emits: `-subject_commits -window +reason +gate_s` + `basis`.

protocol (:13), kotoba (:19), kasegi (:15) stayed row-A: kasegi has **no** round-23 report (absent from master tree), protocol round-14 (`ef36757`, 09-28) and kotoba round-16 (`17c1fad`, 09-29) reports predate their 10-15 launches → not closed. Their lines pair identically (pass 1) and emit nothing. Token-set closure: any other row would add tokens (`+other_authored_commits`, `+no_subject_commits`, `+anchor_round`, `+repo`) that the receipt does not contain.

## Classification (JSON-ready)

| token | class | reason | evidence |
|---|---|---|---|
| `+subject_commits` | live-state | aggregator (root lane) gained a subject commit by its lane author inside the ledger window; row-B→row-A flip adds the row-A field. Census emission text unchanged since the pin. | baseline-r10:14; mori-census.sh:2472-2473 ≡ 5be8943:1380; :2866; commit `1bcf59e` (2026-10-19T22:17:33-03, aggregator-shokunin, refs/heads/master); ledger `launch aggregator round=10` 2026-10-15T01:50:57-03; `git log -Ssubject_commits -- tools/mori-census.sh` → 1439c47 only (r3, ancestor of pin) |
| `+window` | live-state | same aggregator pair; `window=launch..NOW` rides row-A, absent from the baseline row-B line. | same as above (mori-census.sh:2472-2473, :2866, commit `1bcf59e`) |
| `-attribution` | live-state | aggregator leaves row-B, dropping the row-B inference disclosure (key absence, :2862). The r13/r14 commits that touch `attribution=` (18d7d55, 8d22d18) add `attribution=none` to *journal* findings, not the lane row — not the cause. | baseline-r10:14; mori-census.sh:2493-2494 ≡ 5be8943:1401; :2862; `git log -Sattribution` → {1439c47, 18d7d55, 8d22d18} all excluded by byte-identity of the lane-row emitter; state trigger `1bcf59e` |
| `-rowb_files` | live-state | key absence via the same row-B→row-A flip. `rowb_files` value-masking (added at 5be8943, r10-documented) cannot produce this token — a mask-list change emits only the separate `volatile_fields` token (also observed). | baseline-r10:14; mori-census.sh:2493-2494 ≡ 5be8943:1401; :2862; `git log -Srowb_files` → {5be8943 (mask), 1439c47 (emit line, pre-pin)}; state trigger `1bcf59e` |
| `-subject_commits` | live-state | five row-A lanes left row-A on state alone: kagi/kengaku/kake/kumitate → row-6 (anchor-round report committed in (launch, NOW] on master), kama → row-8 young (relaunch 07:17:03, ≤7200 s gate). Report-check rule identical at pin. | baseline-r10:13,15-21; mori-census.sh:2862, :2410-2411, :2377, :360, :2274-2291 ≡ 5be8943 ps_report_closed; commits `01d1c22`+`1eed508` (kagi r24), `9a28017` (kengaku r26), `4487889` (kake r23), `204807e` (kumitate r38); ledger kama relaunch line |
| `-window` | live-state | same five pairs lose the row-A window field. | same as `-subject_commits` |

```json
[
  {"token":"+subject_commits","class":"live-state","reason":"aggregator row-B->row-A: subject commit by aggregator-shokunin inside the ledger window (launch 2026-10-15T01:50:57-03); row-A emission text byte-identical since the r10 pin","evidence":["corpus/evidence/baseline-r10-20261015T2231Z.json:14","tools/mori-census.sh:2472-2473","5be8943:tools/mori-census.sh:1380","tools/mori-census.sh:2866","commit 1bcf59e 2026-10-19T22:17:33-03 on refs/heads/master",".ufo/watchdog.log launch aggregator round=10","git -Ssubject_commits -> 1439c47 only (pre-pin ancestor)"]},
  {"token":"+window","class":"live-state","reason":"same aggregator pair; window=launch..NOW rides row-A, absent from the baseline row-B line","evidence":["tools/mori-census.sh:2472-2473","5be8943:tools/mori-census.sh:1380","tools/mori-census.sh:2866","commit 1bcf59e"]},
  {"token":"-attribution","class":"live-state","reason":"aggregator leaves row-B, dropping the inference disclosure; r13/r14 attribution= commits (18d7d55, 8d22d18) touch journal findings, not the lane row","evidence":["corpus/evidence/baseline-r10-20261015T2231Z.json:14","tools/mori-census.sh:2493-2494","5be8943:tools/mori-census.sh:1401","tools/mori-census.sh:2862","commit 1bcf59e (state trigger)"]},
  {"token":"-rowb_files","class":"live-state","reason":"key absence via row-B->row-A; value masking (5be8943, r10) cannot emit this token — a mask change emits volatile_fields only","evidence":["corpus/evidence/baseline-r10-20261015T2231Z.json:14","tools/mori-census.sh:2493-2494","5be8943:tools/mori-census.sh:1401","tools/mori-census.sh:2862","commit 1bcf59e (state trigger)"]},
  {"token":"-subject_commits","class":"live-state","reason":"kagi/kengaku/kake/kumitate -> row-6 (anchor-round report committed in (launch,NOW] on master), kama -> row-8 young (relaunched 2026-10-21T07:17:03, age <= 7200 s gate); field removal is key-absence on matched lines","evidence":["corpus/evidence/baseline-r10-20261015T2231Z.json:13,15-21","tools/mori-census.sh:2862,2410-2411,2377,360","tools/mori-census.sh:2274-2291 and 5be8943 ps_report_closed (same (launch,NOW] rule)","commits 01d1c22+1eed508 kagi r24, 9a28017 kengaku r26, 4487889 kake r23, 204807e kumitate r38",".ufo/watchdog.log launch kama round=21 2026-10-21T07:17:03-03"]},
  {"token":"-window","class":"live-state","reason":"same five pairs lose the row-A window field","evidence":["corpus/evidence/baseline-r10-20261015T2231Z.json:13,15-21","tools/mori-census.sh:2472-2473","tools/mori-census.sh:2862","same report commits and kama relaunch as -subject_commits"]}
]
```

**Regression check:** zero `census-regression` among the six. Every emitting row's `GL_EXTRA` text is byte-identical between the pin census (d7710981) and the measured census (87b8d680), and the report-closure rule is identical; only the grading revision moved HEAD→branch in r17 (`273aa74`, intended/documented), and all four row-6 flips are corroborated by commits present under either revision.

## Intent citations (round LOG / knowledge)

- LOG.md:479-492 — r10 landed the drift pin (`5be8943`, census `d7710981…`, this baseline); "unmasked state words flip with host state — red drift may be baseline aging; re-pin policy documented in `drift-pin-r10.md`".
- corpus/knowledge/drift-pin-r10.md:167-168 (aging findings are "baseline aging, not masking failure"), :232 ("re-pin deliberately, with a reason"), :243-244 ("it either explains an intended change (then re-pin) or is a regression the round must address … never re-pinning to make red green").
- LOG.md:239 — r3 rows A–D ladder intent (`1439c47`).
- tools/mori-census.sh:169-171 (SCORECARD r9: baseline + `--drift` with declared volatile list), :2738-2739 (roster fields intentionally non-volatile).
- For the six tokens themselves **no round states intent** — they record live fleet activity (a subject commit, four report closings, one relaunch), which the drift contract explicitly expects to surface; hence `live-state`, not `census-schema-change`.

## Comparison with the round-13 register

`.ufo/waves/round-13/evidence/drift-classification.json` (measured at `c13df48`, same r10 baseline) classed all six under `"[INFERENCE] current watchdog/wave/lane activity or finding context; no re-pin/admission claim"`.

- **Agree on class, all six.** That bucket ≙ `live-state` under the r20 closed set; r13 correctly put none of the six in its schema-change or roster buckets, and none is a regression.
- **Refine the reasons (r13 under-specified).** The actual mechanism is three concrete transitions with named commits — aggregator row-B→row-A (`1bcf59e`), four lanes row-A→row-6 (report commits), kama row-A→row-8 (relaunch) — not generic watchdog/wave/finding context. r13 offered no evidence pointers (it predates the mandatory-evidence contract); its hedge was correct but unanchored.
- r13's verdict "red retained; categories are not a regression-free proof; no re-pin" is consistent with the entering state the r20 contract records (8 of 50 tokens unclassified at `2061780`).

## Caveats and residual unknowns

- Census not re-run (bounds). Per-lane rows at measurement are reconstructed from the token set + ledger + git; protocol/kotoba/kasegi remaining row-A is proven by token-set closure (any other row would emit tokens absent from the receipt), not by re-execution — mark `live-state` supporting evidence for those three as [INFERENCE]-by-closure, though nothing in my six tokens depends on them.
- Fleet state moved after the measurement (master tip `7fd7c78` 2026-10-21T07:35:42-03 "round-20: tameshi report"); post-measurement commits cannot have influenced the receipt. The kagi report was amended post-add (`01d1c22` → `1eed508` 07:07:09), still pre-measurement, so row-6 holds for kagi at measurement.
- `git show`/`git log` read-only only; no mutating git/jj command run; no pacman/uv/npm installs performed (none needed).
