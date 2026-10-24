# Round-32 W1 scout — frontier step reconnaissance (read-only)

Measured revision: lane HEAD `8ab61af` (`git rev-parse HEAD` → `8ab61affbd2fc59030040bf80cddc08f7c60ad82`;
`git log -1` → `8ab61af 2026-10-22T22:27:50-03:00 round-32: C0 control receipts (no negative control met), seat
helper, wave-1 spec and dispatch`), after the frozen base `641a6e86` named in
`.ufo/waves/round-32/contract.md:1-5`. Read-only: no fetch, no counter run, no tool install, no write outside
this file.

## 1. Frontier / coverage-map advance

Observation. The recheck is declared as a freshness-axis claim, not a coverage claim:
`contract.md:8-13` ("One claim, freshness") and `contract.md:15-18` ("Surface changed: the lane's mutable-URL
source rows"). No FR1–FR15 row covers source-registry freshness: the README table is
`corpus/README.md:331-348` (FR1 `:335` … FR14 `:348`) and PROVINCE's list `PROVINCE.md:42-57` (FR1 `:44` …
FR14 `:57`), with FR15 appended at `PROVINCE.md:321`; none mentions SOURCES rechecks, source-page freshness or
registry cadence. The Coverage map (`corpus/README.md:5-44`) has no row for `corpus/SOURCES.md` or the source
registry; its last row is `corpus/README.md:44` (`knowledge/earlyoom-invocation-scope-r30.md`).

Ruling. A live recheck of the 34 rows advances **no frontier row and no coverage-map row**. QUALITY 59
(`corpus/QUALITY.md:202-205`: re-verification of an old entry does not establish new covered-ground knowledge)
forbids presenting it as coverage growth. Nearest-but-not-advanced boundaries: FR9 (`PROVINCE.md:52`) is
durable *fixture* evidence, not source-page bytes; FR8 (`PROVINCE.md:51`) is threshold calibration. The
measurable delta is the freshness axis itself (`contract.md:8-13`), gated by `count-c1.py`
(`contract.md:31-34,46-49`).

Append-only option (recommended only if the L1 wants the round artifact indexed in README; exact text, the
three-column format of `corpus/README.md:527-531`):

```markdown
## Round-32 coverage additions

| Ground | Entry | Bounded advance |
|---|---|---|
| Source-registry freshness (34 mutable-URL SOURCES rows, 29 URLs) | `corpus/evidence/recheck-r32/README.md`; `corpus/lessons/round-32.md` `## Recheck` | Live re-open of the 34 non-pinned mined rows with unchanged fetched bytes, located quotes and per-row `current`/`drifted`/`unreachable` verdicts; a freshness-axis receipt only — re-verification of existing entries advances no FR1–FR15 row and adds no covered ground (QUALITY 59). |
```

Placement: after the last README section, which ends at `corpus/README.md:538` (Round-31 Frontier note). This
row is optional: the frozen after-state is counter-only (`contract.md:46-49`). I recommend against adding a
Coverage-map row (`corpus/README.md:5-44`): that table indexes knowledge notes, not evidence receipts, and such
a row would read as coverage growth that QUALITY 59 rules out.

## 2. QUALITY criteria that already govern a recheck

- **QUALITY 81** (`corpus/QUALITY.md:373-376`): a landed SOURCES row keeps its first-published cells; only
  `status`, `recheck` and `used-by` change in place; any other correction is a new row whose `teaches` opens
  `supersedes S0NN —`, with the old→new logged in the lesson; `check-row-identity.py <rev>` must print
  `changed=0`, exit 0. Consequence: a `current` verdict changes nothing in SOURCES; a `drifted` verdict cannot
  edit `teaches`/`scope`/`anchor` — the correction is the contract's appended `Round32` paragraph in each
  `used-by` knowledge entry, and a superseding row is required if the row itself is replaced.
- **QUALITY 22** (`QUALITY.md:44`): an evidence timestamp is no later than the commit that carries it, so the
  `accessed` cell is the real fetch clock and the row lands later.
- **QUALITY 9** (`QUALITY.md:17`): every path/line/commit pointer resolves at the carrying commit and a
  replacement artifact lands with a sweep of every mention — `corpus/evidence/recheck-r32/<id>.src` and its
  README pointer must resolve at the tip.
- **QUALITY 60** (`QUALITY.md:207-210`): a rejected/unopened row needs a located quote ≤25 words, or an explicit
  unavailable/screening-only limitation with the access attempts — an `unreachable` verdict needs its
  `<id>.fetch.txt` transcript; never imply the body was read.
- **QUALITY 90** (`QUALITY.md:526-529`): every `(N words)` label in SOURCES.md equals `wc -w` of the carried
  quote (`\|` counts as a token). It binds only if the recheck writes labelled quotes into SOURCES; the round's
  quotes live in `round-32.md ## Recheck` and are sized by the counter's 3–25-word rule
  (`contract.md:31-34`).
- **QUALITY 59** (`QUALITY.md:202-205`): re-verification of an old entry is not new covered ground — the
  governing reason this round is freshness-only.
- **QUALITY 46** (`QUALITY.md:127-130`): a stale statement is superseded by a dated appended note, never
  rewritten — the required form of a drift correction.
- No criterion imposes a recheck cadence or makes a row overdue by date. QUALITY 41 (`QUALITY.md:104-105`)
  governs census drift-pin freshness, not source-row freshness: a green fixture or sibling gate never
  establishes drift freshness.

## 3. `recheck` cells of the 34 population rows

The cell exists at `corpus/SOURCES.md:5` (`… | status | opened | recheck | used-by |`). The frozen population
JSON carries no `recheck` field — all 34 rows in `.ufo/waves/round-32/c1-population.json` have only
id/url/scope/anchor/teaches/used_by — so the counter does not read cadence.

Counts: on-release 24 · 90d 2 · 180d 2 · 365d 6 (34 total).

Per id (SOURCES line, opened, recheck):
- on-release (24): S001:7 2026-10-19; S002:8 2026-10-19; S007:13 2026-10-19; S014:20 2026-10-19; S015:21
  2026-10-19; S031:37 2026-10-19; S037:43 2026-10-20; S039:45 2026-10-20; S040:46 2026-10-20; S043:49
  2026-10-20; S044:50 2026-10-20; S045:51 2026-10-20; S046:52 2026-10-20; S047:53 2026-10-20; S052:58
  2026-10-21; S058:64 2026-10-21; S064:70 2026-10-21; S068:74 2026-10-21; S069:75 2026-10-21; S073:79
  2026-10-21; S117:123 2026-10-22; S128:134 2026-10-22; S137:143 2026-10-22; S149:155 2026-10-22.
- 90d (2): S012:18 2026-10-19 → due 2027-01-17; S049:55 2026-10-21 → due 2027-01-19.
- 180d (2): S071:77 2026-10-21 → due 2027-04-19; S074:80 2026-10-21 → due 2027-04-19.
- 365d (6): S041:47 2026-10-20 → due 2027-10-20; S051:57, S056:62, S062:68, S067:73 and S076:82, all opened
  2026-10-21 → due 2027-10-21.

Overdue as of 2026-10-23: **0 of 34**. Every row is 1–4 days old; the ten interval rows are overdue no earlier
than 2027-01-17. The 24 `on-release` rows have no date deadline (recheck triggered by an upstream release), and
no row records a post-open upstream release, so none is date-overdue. The live re-open is therefore voluntary
freshness work under the round claim, not a cadence obligation: the population's defect is that every row was
last opened in the round that added it (`contract.md:15-18`), not that any is late.

## 4. Mistake sweep — spot-check disagreements vs `## Mistakes`

Scope: all `corpus/lessons/round-2*.md` and `corpus/lessons/round-3*.md` — rounds 20–31 lessons plus their
`-verifier-spotcheck.md` files (the glob matches no round-2/round-3 files). Run through the harness grep tool,
case-insensitive, over those two globs; shell-equivalent patterns:

```
disagree|dissent|disputed
\*\*disagree|disagree\*\*|\| *disagree *\||disagree *\|
```

Result: **no unmined decision disagreement.** The second (decision-cell) pattern matched only the six table
headers — `round-24-verifier-spotcheck.md:118`, `round-26…:144`, `round-27…:113`, `round-28…:101`,
`round-29…:119`, `round-31…:168` — whose cell reads `Agree / disagree`; no data row has a `disagree` or
`**disagree**` cell; every row is `agree` (or `agree (partial)`, below). Prose hits and their mining status:

- `corpus/lessons/round-20.md:27` — "open disagreement for the non-author closure": it **is** Mistakes row M6,
  later mined again by `round-21.md:14-16` (M1/M2).
- `corpus/lessons/round-21.md:15` — M2 "self-ratified disputed criterion" (mined).
- `corpus/lessons/round-22.md:16` — M3 "contradictory wrapper provenance" (mined).
- `corpus/lessons/round-29-verifier-spotcheck.md:50` — "Rows disagreeing with the closure record on 'Last
  change': 5/6 before → 0/6 after": the same stale-Axes defect is `round-29.md:26-32` (M1), with before/after
  receipts (`evidence/c1-before.txt`, `evidence/tip-c1.txt`).
- `corpus/lessons/round-29-verifier-spotcheck.md:77` and `round-29.md:157` — the disputed-harm ruling; the
  spot-check rules "not harmed" and the lesson records it as forwarded to the closure — recorded on both
  sides, not a lane mistake.
- `corpus/lessons/round-30-verifier-spotcheck.md:165` — states no spot-check disagreement was left unlearned
  ("do not apply"); nothing to mine.
- `corpus/lessons/round-24-verifier-spotcheck.md:86-87` — surviving mutants and tool-case dependence disclosed
  and tied to "(lesson M8)"; mined.

One unmined **qualification** (not a decision disagreement): `corpus/lessons/round-25-verifier-spotcheck.md:138`
marks S105 `agree (partial)` — the verifier could not re-verify the row's "in any file" clause because the
GitHub tree API was rate-limited. `round-25.md` `## Mistakes` (M1–M3, `round-25.md:25-50`) and its
"Corrections appended" section do not record this caveat; `corpus/SOURCES.md:111` still says "in any file". The
reject decision itself is agreed and unaffected; this unverified scope clause is the only item the sweep
leaves unmined.

## Tooling and unrun checks

No tool installed or updated this seat. Not run (read-only reconnaissance): no source fetch, no `count-c1.py`
run, no build, selftest or formatter.
