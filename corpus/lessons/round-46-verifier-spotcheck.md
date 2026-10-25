# Round 46 — mori verifier spot-check

author: hyaku closure (non-author integrator, @m_flash)

Lane: mori-shokunin · Round: 46 · Lane commit: `2f04605ab1d113ecf27e77adc0202a21c9bb6ec7`
Report: `.ufo/reports/round-46/mori.md` (committed `c438180e0319b9da123c3b1f95911cbfb3c0d0b8` by `mori-shokunin`).
Dispatch/complete digest (from `.ufo/watchdog.log`):
`2026-10-25T10:00:01-03:00 launch mori round=46 pgid=2011258 driver=hyaku-inline attempt=1`;
`2026-10-25T10:16:48-03:00 complete mori round=46; hyaku-inline attempt=1`.

## 1. Conformance

- Report committed by the lane identity: `git log --format='%an %H' -- .ufo/reports/round-46/mori.md` → `mori-shokunin c438180e…`. ✓
- Report carries the `SHONEN` heading with one line per box: four `[~]` lines, each with a resolvable pointer, no `[x]`. ✓
- Every cited lane commit exists and is an ancestor of the branch ref `master`: `git -C mori-shokunin merge-base --is-ancestor` rc 0 for `2f04605…`, `12c89ea…`, `baabc992…`. ✓ (jj-colocated repo: HEAD is detached; ancestry tested against `master`.)
- Lane repo pushed, no uncommitted round work: `scripts/hyaku/jj-lane.sh state` → `ahead=0 behind=0`; `git ls-remote origin refs/heads/master` = `2f04605…`; `git status --porcelain` shows only untracked `.scratch/` leftovers (no tracked modifications). ✓
- Dispatched prompt carries the template contract: sections 1–5 of `.ufo/prompts/mori-round-46.md` match `templates/round-prompt.md` with the substitutions (mori / 46 / `/home/vgpnk/Projects/shokunin` / axes); hyaku addendum §6 appended. ✓
- Report is a real report, not a marker: named committed work, evidence pointers, bounded measurements, trend verdicts, SHONEN. Status `ok`.

## 2. Claims — re-derivation

One declared claim, C1 (calibration). I re-measured against `2f04605…` with plain commands run by me in the lane root.

### C1 — re-pinned registry cells (SKILL.md:184/190/191/194)

| Row | Pinned values (committed row) | My measured values | Match |
|---|---|---|---|
| `:184` r44 gate registry (C2) | `GATE_REGISTRY_SELFTEST pass=15 fail=0`; auditor sha256 `8b82ac999091ebe65e765ed69f759910a57049ff0e7c5c4aa56df9c7168f5832`; `743 lines` | auditor selftest `pass=15 fail=0` rc 0; `sha256sum tools/mori-gate-registry.py` = `8b82ac99…`; `wc -l` = 743 | ✓ |
| `:190` r45 ledger counter (C1) | `C1_SELFTEST pass=16 fail=0`; counter sha256 `5f2deea0b35c5e1346229d265aa0c07bf7f365bf6c5acda87648045bce658d23` | `python3 .ufo/waves/round-45/count-c1.py --selftest` → `C1_SELFTEST pass=16 fail=0` rc 0; sha256 `5f2deea0…` | ✓ |
| `:191` r45 gate conformance (C2) | `C2_SELFTEST pass=14 fail=0`; counter sha256 `153423c48ca90466e85b02707828f5c6b2cf39c87c68ee67e3f9abee956baf93`; mutant sha256 `9850b3fcc8885456c3e71458b34184d716d54880a91ae5b29c7d003f26708703`; auditor `8b82ac99…`; `743 lines` | `python3 .ufo/waves/round-45/count-c2.py --selftest` → `C2_SELFTEST pass=14 fail=0` rc 0; sha256 `153423c48…`; mutant sha256 `9850b3fcc…`; auditor `8b82ac99…`; `wc -l` = 743 | ✓ |
| `:194` r44 gate registry (C2) — write scope superseded | `GATE_REGISTRY_SELFTEST pass=15 fail=0`; auditor `8b82ac99…`; `743 lines` | as above | ✓ |

Frozen counter (report's counting command): `python3 .ufo/waves/round-46/count-repins.py` → repaired `SKILL.md` `MORI_R45_REPINS mismatches=0 rows=4` rc 0; committed control `control-skill.md` (byte-identical to `12c89ea:SKILL.md` = `baabc992:SKILL.md`, sha256 `ed71e8f6…`) `mismatches=4 rows=4` rc 1; counter sha256 `ebb6a6d3fe08d78791a45643d1ebda2243e5fff271eaada1d7f682317c673327`. All match the report.

Freeze-manifest correction: at the round-45 landing `baabc992…`, `git archive baabc992… | tar -x -C $(mktemp -d)` then `grep -v '^#' .ufo/waves/round-45/evidence/freeze-r45.txt | sha256sum -c` → **27 OK, rc 0** (28 non-comment lines include one blank: the header separator). Confirms the appended `LOG.md` correction (`LOG.md:2655-2657`), which supersedes the original 29/29 wording without rewriting it.

No owned axis harmed: `git diff 9834fed4dd8a2ee201ebc4183e2435f4c7272674 2f04605ab1d113ecf27e77adc0202a21c9bb6ec7 -- SCORECARD.md` is purely additive (round-45 reconciled rows + round-46 calibration row); no score changed.

**Verdict on the claim and the axis.** The lane self-graded C1 `unprovable` because the frozen counter has a reachable false-green path: its needles are whole-row substrings, so stale receipt strings appended to a row's other cells turn it green, and it performs no runtime measurement (`w1/CritControl.md`, `w1/CritVerdict.md`). I re-opened both falsifier reports and reproduce the reasoning; the counter is indeed not a calibration-grade proof, so the claim's proof vehicle stays unprovable. However, **my own direct re-measurement of the four pins against the committed instruments shows every pinned tally, digest and line count matches observed instrument state**. The round-45 harm (four stale registry cells at SKILL.md:184/190/191/194) is therefore repaired, even though the counter is weak. I grade the **calibration axis on my own measurement: improved**, and say so explicitly — the lane's verdict is respected for its predicate, not for the repaired cells, which are independently corroborated.

## 3. Axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| calibration | **improved** | four registry pins re-measured vs committed tools: all match (§2); round-45 stale-cell harm repaired |
| operability | unchanged | no runnable artifact changed this round |
| depth | unchanged | no knowledge entry landed |
| coverage | unchanged | no new surface governed |
| freshness | unchanged | no re-verification claim other than the pins |
| adjacency | unchanged | no cross-domain contact reported |

## 4. Trend verdicts

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | unchanged | only a SOURCES row (S474) was added; no admitted `knowledge/` entry on uncovered coverage-map ground |
| quality | unchanged | no knowledge entry re-verified or superseded |
| discernment | **improved** | the outside spot-check (§5) agrees with the gate on the sampled admit and reject; the honest-stop on C1 is itself a calibration-correct decision that matches observed state |

## 5. Discernment spot-check (LEARNING.md — checked from outside)

| Item | Gate decision | Re-opened source | Agree/Disagree | Reason |
|---|---|---|---|---|
| S474 (own-work row: calibration criterion from fleet AXES.md) | admit (mined, tier A) | `/home/vgpnk/Projects/shokunin/AXES.md:15` | agree | The located quote “Self-assessment quality: gaps named honestly, confidence graded, overreach caught.” (11 words ≤ 25) exists verbatim at `AXES.md:15`; row shape conformant (anchor, teaches, opened 2026-10-25, status mined, used-by `corpus/lessons/round-46.md`); census green |
| C1 claim admission | reject (unprovable honest-stop) | `w1/CritControl.md`, `w1/CritVerdict.md` | agree | Replay demonstrates green while the receipt cell stays stale (needle substring anywhere in the row; no runtime measurement); the claim cannot be admitted under its frozen predicate, and the lane says so |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → `mori ok`, rc 0, pre-existing W04 duplicate-URL warnings only. SOURCES rows 246 → 247 (`git show 12c89ea…:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` = 246; same grep on current = 247). Both match the report.

## 6. Routed defects for mori next round

1. **Replace or retire `count-repins.py` as a calibration proof.** It must parse designated cells (`split("|")`), require each needle inside its own semantic cell, re-measure instruments live at check time (selftest tally, sha256, line count), count mismatches per pin, and ship a red-before stale-string control before it is used to declare any claim again (per `w1/CritControl.md`, `w1/CritVerdict.md`; the lesson M1 fix direction agrees).
2. **`rows=4` is a hard-coded constant, not a measured count** — rename it (`targets=4`) or count matched rows.
3. **Clean up `.scratch/` leftovers**, including round-46 mutation-seat dirs `MutMissing/`, `MutStaleC1/`, `MutStaleC2/` (untracked debris; not committed round work, but the repo is left dirty).
4. No promotion claims: all SHONEN boxes are `[~]`; promotion is operator-owned.
