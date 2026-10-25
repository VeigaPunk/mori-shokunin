# ScribeTrends — round-47 wave w2: Trend verdicts

Seat: ScribeTrends (scribe). Lane: mori-shokunin. Landed tip T = `68d66ca5` (branch master);
entering tip E = `2d85e33d`; freeze F = `63eecf27`. This file drafts the report's **Trend verdicts**
per `LEARNING.md` (three trends, one verdict each: `improved` / `harmed` / `unchanged` /
`unprovable-but-better`), with evidence pointers into the lane at T. All reads were read-only;
no tools installed; no instruments re-run (receipts cited are committed artifacts).

| Trend | Verdict | Evidence at T |
|---|---|---|
| **expansion** | **improved** | `corpus/knowledge/oom-tracepoints-r47.md` is a new admitted entry on FR13 ground (frontier-only at E), citing mined rows S475/S476/S477/S478 + S005; holds under the frozen counter (`evidence/after-c2.txt` → `C2=met … rc=0`). |
| **quality** | **unchanged** | no held `knowledge/` entry was superseded or re-verified this round (E→T diff touches only the new entry); no admitted entry fails its re-check; no capability added to `SCORECARD.md` (unchanged E→T). |
| **discernment** | **unchanged** (pending the outside spot-check) | no non-author spot-check of round-47 gate decisions exists at T (`corpus/lessons/round-47.md` §Spot-check); new criteria 123/124 are lesson-backed — no harmed condition. |

No trade condition: `expansion: improved` with `quality: unchanged` is not the
growth-without-quality trade (`LEARNING.md` "Growth without quality…").

---

## 1. Expansion — improved

**Attack:** the round's net new admitted `knowledge/` entries and whether each sits on ground the
coverage map did not hold, with every `source:` citing a mined `corpus/SOURCES.md` row.

**Observed (at T):**

- Exactly one new admitted entry this round: `corpus/knowledge/oom-tracepoints-r47.md` (80 lines;
  new in E→T; `git diff --stat 2d85e33d..68d66ca5 -- corpus/knowledge/` → only
  `oom-tracepoints-r47.md | 80 +`).
- **Uncovered ground:** the entry declares `coverage-map: FR13` and
  `ground: frontier item **FR13** — "eBPF kill/OOM tracing … a resident tracer is outside the
  census, so retain this as knowledge/frontier only" (corpus/README.md Frontier table)`. At E, the
  map held FR13 only as a frontier row (`git show 2d85e33d:corpus/README.md` line 353: FR13
  "retain this as knowledge/frontier only"); `corpus/README.md` round-47 coverage additions
  (lines 644–655) confirm the ground was held only as a peer-reviewed abstract
  (`knowledge/oom-victim-context-r41.md`, S262) plus one queued field-schema row (S005) — the full
  v7.2 `oom` trace-event set was not held.
- **Mined rows, each citing the entry's coverage-map row:** `corpus/SOURCES.md` lines 11, 254–257
  — S475, S476, S477, S478 all `mined`, tier A, `used-by corpus/knowledge/oom-tracepoints-r47.md`;
  S005 `queued → mined` with `used-by` the same entry (lesson Gate table, rule 2). The entry's
  `source:` field cites S475/S476/S477/S478/S005.
- **Holds under the gate's own counter:** `evidence/after-c2.txt` (measured at `af2250d8`):
  ```
  $ python3 .ufo/waves/round-47/count-c2.py af2250d80033ded23ec34af328068eeb85007d1c
  C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=af2250d8…
  rc=0
  ```
  Measured files are identical between `af2250d8` and T (`git diff --stat af2250d8..68d66ca5 --`
  on `count-c2.py`, `tools/mori-pin-check.py`, `SKILL.md`, `corpus/` → empty).
- Frontier entered: FR13 stays frontier (no tracer enabled; README:653–655) but the *entry* lands
  on its ground, which is the ordinary frontier→knowledge move.

**Verdict: holds — improved** (net +1 admitted entry on uncovered coverage-map ground, citing its
coverage-map row and mined source rows; no admitted entry fails the bar it was admitted under —
C2 met).

## 2. Quality — unchanged

**Attack:** whether a weaker held entry was superseded by a stronger one, stale entries re-verified,
or any admitted entry found false/stale and left unmarked.

**Observed (at T):**

- E→T diff over `corpus/knowledge/` contains only the new entry; **no held entry was edited,
  superseded, or re-verified** this round. `verified-at` freshness was not a round activity.
- The staged `oom-tracing-tracepoints-r42.md` headline was **rejected** (lesson §Gate), not an
  admitted entry superseded — a gate decision, not a quality of held entries.
- No admitted entry fails its re-check: C2 met (above); the only stale-pin harm found
  (`SKILL.md:912`) was an *instrument registry cell*, repaired under claim C1 (calibration axis),
  not corpus knowledge.
- `SCORECARD.md` unchanged E→T (no capability admission).

**Verdict: holds — unchanged** (improved condition unmet: no supersession/re-verification; harmed
condition absent: nothing found false or stale left unmarked).

## 3. Discernment — unchanged (pending the outside spot-check)

**Attack:** gate decisions vs the outside spot-check; whether `QUALITY.md` criteria are grounded.

**Observed (at T):**

- Round-47 gate decisions: admits S475–S478 (+ S005 status change); rejects the staged entry's
  "exactly three named tracepoints" headline and staged S501; quarantine slice S244/S262/S268
  stays closed (lesson §Gate).
- **No outside spot-check exists yet at T** — lesson §Spot-check: "No non-author spot-check of
  this round's gate decisions exists yet; the hyaku closure session is the outside check
  (LEARNING.md). Sample offered: admit S478, reject the staged entry's count." The `improved`
  condition (spot-check agrees on admits *and* rejects, or a disagreement becomes a lesson that
  adds a grounded criterion) therefore **cannot be verified at T**; the offered sample is still
  unjudged by a non-author.
- Harm condition checked and absent: `corpus/QUALITY.md` criteria 123–124 (lines 1026–1048) each
  cite a lesson or 123 cites `round-47.md` M1/M2 and the operator's `considerthese/2026-10-25.md`
  suggestion 1; 124 cites M3. Both show "shown able to fail":
  - `evidence/control-c1-donothing.txt` (entering E) → `PIN_CHECK=unmet … mismatches=1` (line
    912), `rc=1`;
  - `evidence/control-c2-three-at-freeze.txt` → `C2=unmet … name_mismatch=5 failed=name_mismatch,source_row`, `rc=1`.
  No criterion was added without a lesson behind it.
- Prior round's spot-check agreement remains on record (`corpus/lessons/round-46-verifier-spotcheck.md`
  §5: agree on admit S474 and reject C1), but that checks round-46 decisions, not round-47's.

**Verdict: holds — unchanged** (strictly: neither improved nor harmed condition is met at T; the
round's own lesson flags the missing outside check). Upgradable to `improved` iff the hyaku closure
spot-check agrees with the offered sample — an unobserved future event, not claimed here.

---

## UNVERIFIED

- The hyaku closure (non-author) spot-check of round-47 gate decisions — does not exist at T; the
  offered sample is admit S478 / reject the staged entry's count.
- Re-running the frozen counters/`mori-pin-check.py` myself — not done (leaf seat; committed
  receipts cited above are the measured evidence; claim re-scoring is other seats' work). All
  receipt commands/quotes above are verbatim from committed files.
- Host tracefs readability today — cited only via the committed own-work receipt
  `evidence/host-tracefs.txt` (S477, 2026-10-25); not re-read.

## Out of scope

- C1/C2 claim verdicts (predicate/counter seats), SCORECARD scores, SHONEN boxes, LOG/README edits.
- No files other than this report were written.
