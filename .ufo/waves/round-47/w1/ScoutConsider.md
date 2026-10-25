# ScoutConsider — considerthese mining audit (mori round 47, wave 1)

Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Frozen contract:
`.ufo/waves/round-47/contract.md` at freeze `63eecf2738db96f46b0bd02b1b2dfd66787493d0`;
entering tip `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`.

Seat scope (read-only): read `considerthese/` (all seven files, never edited), `LOG.md`,
`corpus/lessons/`, `corpus/QUALITY.md`, `SCORECARD.md`, and the lane's tools. No file
outside this report was written; no git/jj mutation; no tool installed; no lane tool
executed (the C1/C2 counters are other seats' work); `/home/vgpnk/Projects/shokuknow` was
not read (out of this seat's scope).

`considerthese/` is byte-unmodified at the entering tip: `git status --porcelain
considerthese/` → empty; `git diff --stat fdb8b561 -- considerthese/` → empty.

---

## 0. The question, and the short answer

**Q1 — Was 2026-10-25.md suggestion 1 (the registry pin check) implemented by any earlier
round? NO.** No committed instrument at or before the entering tip compares a `SKILL.md`
registry row's pinned sha256 / selftest tally against the committed bytes of the named
instrument. The nearest prior art is round 46's `count-repins.py`, which the round-46
non-author closure explicitly routed for replacement; the instrument that actually does
what suggestion 1 asks for, `tools/mori-pin-check.py`, first appears in this round's
freeze commit.

**Q2 — Which other `considerthese/` suggestions did earlier rounds adopt?** Six, with a
citable trail each (§2). Everything else in the seven files is criterion-only,
present-but-unwired, or absent (§3).

---

## 1. Q1 — the registry pin check: no earlier implementation

### 1.1 Chronology (why no earlier round could have)

| rev | commit | time (−03:00) | what |
|---|---|---|---|
| `9834fed4dd8a` | round-45 non-author spot-check | 2026-10-25 08:35:38 | last commit before the reflection |
| `fdb8b561d1a0` | **considerthese 2026-10-25 daily reflection** | **2026-10-25 08:43:38** | suggestion 1 opens here |
| `2f04605ab1d1` | round-46 landing | 2026-10-25 10:15:37 | r46 counter `count-repins.py` |
| `2d85e33d1419` | round-46 non-author spot-check | 2026-10-25 10:19:06 | routed defect 1 = replace `count-repins.py` |
| `63eecf2738db` | **round-47 freeze** | 2026-10-25 16:32:10 | `tools/mori-pin-check.py` first lands |

- `git log --format='%h %cI %s' -- considerthese/` → the reflection is the newest
  operator file; `fdb8b561` is an **ancestor** of the r46 landing (`git merge-base
  --is-ancestor fdb8b561 2f04605a` → exit 0).
- Round 46's wave registry `.ufo/waves/round-46/w1/swarm-registry.json:3` records
  `createdAt 2026-10-25T13:09:29.566Z` (= 10:09:29 −03:00) — **1 h 26 min after** the
  reflection landed, so r46's seats could have read it.
- They did not mine it. `corpus/lessons/round-46.md:6` cites the **previous** day's file
  instead — `considerthese/2026-10-24.md:24` (P4, "Reproduce headline numbers
  mechanically") — and concludes the broader proposal is "**not implemented** this round".
  `.ufo/waves/round-46/w1/ScribeLesson.md:98-99` records the round-46 Gate detail
  verbatim: "No considerthese directory was inspected".
- Round 45 could not have seen it either: the r45 freeze is `3ad8faaa` (07:40:05), and
  the r45 census states outright that the newest reflection is the 10-24 file —
  `.ufo/waves/round-45/w1/ScoutConsider.md:11`: "**No `2026-10-25.md` exists**".

### 1.2 What the lane actually had before this round (nearest prior art)

Exhaustive read-only sweep at the entering tip: every committed `.py`/`.sh` under `tools/`
and `.ufo/waves/` that mentions `SKILL.md`, cross-checked for re-running a selftest and
for comparing a pinned value.

| candidate | rev | what it actually does | why it is not suggestion 1 |
|---|---|---|---|
| `tools/mori-gate-registry.py` | r44 `7cb59c68`, rewritten r45 `18fd68b0` | audits registry **shape**: eight standard cells, entry path resolves at `--rev`, tool carries a **real** `--selftest` argv branch, duplicate names, wrong rows (`tools/mori-gate-registry.py:5-6`, `:39-43`, `:70-71`) | the `pinned values` cell is checked only for **non-emptiness** (`:541-543`); the auditor never executes the audited instrument and never compares a pinned digest/tally to observed bytes. `subprocess` appears once (`:113`) and runs only `git`. |
| `.ufo/waves/round-46/count-repins.py` | r46 `2f04605a` | the closest prior art: row-wide substring match of 4 **hard-coded** rows against hard-coded needles (`:9-20`, `:33`) | (a) row-wide substring, not cell-scoped; (b) **never re-runs anything** — `import subprocess` at `:5` is unused, `grep -n 'subprocess\.'` → no hits; (c) hard-coded to 4 rows and **does not cover the `SOURCES append-only timing (r38)` row at `SKILL.md:912`** (`grep -c 'MORI_SOURCES_APPENDONLY' .ufo/waves/round-46/count-repins.py` → 0); (d) `rows=4` is a constant, not a measurement. Routed for replacement by `corpus/lessons/round-46-verifier-spotcheck.md:71` (defect 1): "must parse designated cells (`split(\"|\")`), require each needle inside its own semantic cell, re-measure instruments live at check time (selftest tally, sha256, line count), count mismatches per pin, and ship a red-before stale-string control". |
| `tools/mori-round41-calibration.py` | r41 `d72ac167` | re-derives the **r40** gate's recorded numbers from `SCORECARD.md` / `LOG.md` / `corpus/lessons/round-40.md` (`:16-17`) | round-40 headline numbers, not registry pins; no `SKILL.md` read. |
| `tools/mori-source-drift.py` | r36 `bf0df77f` | re-fetches each `corpus/SOURCES.md` row's copy and classifies fresh/excerpt/drifted | different surface (corpus source copies), not the `SKILL.md` registry. |
| `tools/mori-routed-r24.py` D1 | r25 `e54b644b` | one named selftest evidence file: header fields + byte-equal stdout at a named revision (`:16-24`, `:509-598`) | single-file byte check of a *receipt*, not a registry-row pin re-measurement. This is 2026-10-22 P22-1 (§2.5). |
| `tools/mori-round13-regressions.py` | r13 | `registry_row_status` = name-only matcher on the `SKILL.md` row (`:529-546`) | presence of the row name, never the pinned values. |

The only committed file that reads `SKILL.md`, re-runs the named instrument, and compares
the pinned digest/tally is `tools/mori-pin-check.py` — and `git log --format='%h %cI %s'
-- tools/mori-pin-check.py` returns exactly one commit: **`63eecf27` (the round-47 freeze,
2026-10-25 16:32:10)**. Frozen sha256 `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`
= `contract.md:14`; verified `git show 63eecf27:tools/mori-pin-check.py | sha256sum` →
same value.

> Working-tree note (read-only observation, not mine to change): the working copy of
> `tools/mori-pin-check.py` has **already drifted** from the frozen bytes —
> `sha256sum tools/mori-pin-check.py` → `381fa1a073b99a97ecb4c5e2068329a11f3605d7904838e3134cc7fdea635e1`,
> and `git diff --stat tools/mori-pin-check.py` → `135 insertions(+), 24 deletions(-)`
> (a "v2" header block describing new constraints). Per `contract.md:16-17` the claim is
> measured on the frozen bytes (`git show <freeze>:<path>`), so this drift does not
> change C1's instrument; it is recorded so the L1 knows the working tree and the frozen
> bytes differ.

### 1.3 Why the stale pin survived (the calibration hole, with dates)

- The pin `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` entered `SKILL.md` at commit
  `265a955c` (round-40, 2026-10-24 02:47:29) — `git log -S 'MORI_SOURCES_APPENDONLY_SELFTEST
  pass=15' -- SKILL.md`.
- The instrument's own tally grew to 22 at the round-41 freeze `d72ac167`
  (2026-10-24 04:46:03) — `git log -S 'ARM' -- tools/mori-sources-appendonly.py` shows the
  selftest arm set changing at `d72ac167`.
- So the registry cell went stale within ~2 hours and stayed stale through rounds
  42–46. `SKILL.md:912` at the entering tip still reads
  "`--selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0`"
  (`git show 2d85e33:SKILL.md | sed -n '912p'`), while the committed tool prints `pass=22`
  (contract.md:33-35; receipt `evidence/control-c1-donothing.txt:32`).
- The correct value was **already inside the lane's own committed counter**: round 43's
  `.ufo/waves/round-43/count-c1s.py:131-134` asserts the observed tally is exactly
  `(22, 0)`. The number was known at r43 (committed `dde525ea`, 2026-10-24 22:50:57) and
  still nothing compared it to the registry cell. That is precisely the gap suggestion 1
  names, and it is the strongest evidence that no earlier round implemented it.
- The four rows that *were* repaired at r46 (`:184`, `:190`, `:191`, `:194`) were flagged
  by the r45 non-author closure, `corpus/lessons/round-45-verifier-spotcheck.md:50-66`
  ("Calibration ruling … **calibration: harmed**"), and repaired by hand at r46
  (`LOG.md:2663`). `:912` was outside that routed set, so it was never repaired.

---

## 2. Q2 — the adoptions trail (path:line for every claim)

### 2.1 2026-10-24.md:21 — "Check that frozen instruments replay off-host" → **QUALITY 115**
- Proposal text: `considerthese/2026-10-24.md:21`.
- Criterion: `corpus/QUALITY.md:938` — "Rationale: considerthese/2026-10-24.md, 'Check
  that frozen instruments replay off-host' (operator-authored reflection, mined round 43;
  not edited)".
- Lesson record: `corpus/lessons/round-43.md:107-114` (§ heading at :107).
- LOG record: `LOG.md:2534-2536` — "**considerthese (item 10):** one still-unimplemented
  proposal mined — 'Check that frozen instruments replay off-host'
  (`considerthese/2026-10-24.md`, read-only, not edited) → QUALITY 115."
- Added by `dde525ea` (2026-10-24 22:50:57) — `git log -S '115. A frozen instrument' -- corpus/QUALITY.md`.
- Residue: the *daily sweep* the proposal asks for is still absent — `.ufo/waves/round-44/w1/ScoutConsider.md:36`
  and `.ufo/waves/round-45/w1/ScoutConsider.md:107` both record "criterion-only; no sweep tool".
  This is the one the task statement names as "off-host replay → QUALITY 115".

### 2.2 2026-10-24.md:22 — "Keep a cumulative survivor ledger" → **QUALITY 114**
- Proposal: `considerthese/2026-10-24.md:22`.
- Criterion: `corpus/QUALITY.md:927-932` — rationale at `:931-932` cites
  `considerthese/2026-10-24.md, "Keep a cumulative survivor ledger" … mined round 42`.
- Lesson record: `corpus/lessons/round-42.md:73-75` — "one unimplemented proposal mined —
  'Keep a cumulative survivor ledger' → QUALITY 114, cited there. No other proposal was
  implemented; the file was not edited."
- Added by `34b92673` (2026-10-24 20:25:43).
- Residue: the cumulative-ledger artifact is still absent — `.ufo/waves/round-45/w1/ScoutConsider.md:108`.

### 2.3 2026-10-24.md:23 — "Watch repository growth from scratch output" → **routed to r45, landed as QUALITY 122**
- Proposal: `considerthese/2026-10-24.md:23`.
- Routed: `corpus/lessons/round-44.md:108-110` — "P3 … remains unimplemented and is routed
  to round 45".
- Criterion: `corpus/QUALITY.md:1013-1017` (QUALITY 122, added `18fd68b0`) — rationale at
  `:1015-1016` cites "considerthese/2026-10-24.md proposal P24-3 … mined 2026-10-25 — the
  proposal itself is not implemented and stays open".
- Still carried as unimplemented: `SCORECARD.md:2524-2525` — "**Carried**: `considerthese`
  P3 (repository growth from scratch output) is still unimplemented".
- Grounded in depth by the r45 census: `.ufo/waves/round-45/w1/ScoutConsider.md:120` (§3).

### 2.4 2026-10-24.md:24 — "Reproduce headline numbers mechanically" → **QUALITY 117**
- Proposal: `considerthese/2026-10-24.md:24`.
- Criterion: `corpus/QUALITY.md:943-948` — rationale at `:946` cites the proposal as
  "mined round 44 on 2026-10-25 — the general form had no artifact".
- Lesson record: `corpus/lessons/round-44.md:103-110` — "Mined as **QUALITY 117** … P3 …
  remains unimplemented and is routed to round 45; P1 and P2 are already criteria
  (115, 114)".
- Round-46 re-opened and re-routed it: `corpus/lessons/round-46.md:6` — "Attempted only
  for the four routed registry cells; the frozen substring counter's observed false green
  means the broader mechanical-reproduction proposal is **not implemented** this round.
  Flip condition: a future round freezes a semantic-cell parser and dynamic digest/selftest
  measurement before scoring, and the stale-string mutation goes red."
- Added by `5157cdda` (2026-10-25 05:28:48).

### 2.5 2026-10-22.md:26 — "Re-run each committed selftest output at the revision it names" → **implemented**
- Proposal: `considerthese/2026-10-22.md:26`.
- Artifact: `tools/mori-routed-r24.py` — `--rerun` re-executes the named revision's own tool
  and reports byte equality (`tools/mori-routed-r24.py:11-12`, `:584-597`, `:1471-1475`);
  the D1 arm is `:509-598`. Registered at `SKILL.md:721`.
- Status record: `.ufo/waves/round-45/w1/ScoutConsider.md:88` — "P22-1 | re-run each
  committed selftest output at its named revision | **implemented**".
- Landed at r25 (`e54b644b`, 2026-10-22 07:44:02).

### 2.6 2026-10-23.md:20 — "Point out tools without self-tests" → **implemented**
- Proposal: `considerthese/2026-10-23.md:20`.
- Artifact: `tools/mori-gate-registry.py`'s `no_selftest` bucket
  (`tools/mori-gate-registry.py:42`, `:439-442`), registered at `SKILL.md:184`.
- Status record: `.ufo/waves/round-45/w1/ScoutConsider.md:100` — "P23-4 | point out tools
  without self-tests | **implemented**".
- Effect at r45: `LOG.md:2644` — "`C2=met tables=7 registered=39 unregistered=0
  no_selftest=0 duplicate=0 wrong_row=0`" (from 3 unregistered / 5 missing `--selftest`
  flags per `considerthese/2026-10-25.md:29-30`).

### 2.7 The "where do my own suggestions end up" track (2026-10-25.md:53-55) — this seat is that track
The r47 seat asked for exactly this. Precedents, all in-lane and read-only:
- r42: spec seat `ScConsider` (`.ufo/waves/round-42/w1-spec.json`, prompt "…report which
  other proposals remain unimplemented"); the planned report `.ufo/waves/round-42/w1/ScConsider.md`
  is **absent** from the tree (`find .ufo -name 'ScConsider*'` → no hits) — the finding
  survives only via `corpus/lessons/round-42.md:73-75`.
- r43: spec seat `Scout5` ("considerthese 2026-10-24 unimplemented proposals other than the
  one mined"); `.ufo/waves/round-43/w1/Scout5.md` is **absent** (only the raw seat log
  `.ufo/waves/round-43/logs/wave64/Scout5.log` survives).
- r44: `.ufo/waves/round-44/w1/ScoutConsider.md` — committed (`5157cdda`); verdict table at
  `:36-39`; "Recommendation — exactly one" at `:173-207`.
- r45: `.ufo/waves/round-45/w1/ScoutConsider.md` — committed (`baabc992`); per-file proposal
  census §2 at `:43-118`, "Net: of 29 proposals…" at `:112-118`.
- r47: this seat.

So the tracking practice is established but its **reports were only committed from r44
onward**; the r42/r43 instances are lost as files.

---

## 3. The rest of the seven files — census of non-adoptions

The r45 census (`.ufo/waves/round-45/w1/ScoutConsider.md:43-118`) is the most recent
complete census and it covers 2026-10-19 … 2026-10-24 (29 proposals). Its net at
`:112-118`: **2 implemented** (P22-1, P23-4), **4 criterion-only** (P22-3, P24-1, P24-2,
P24-4), **5 present-but-unwired** (P19-2, P19-5, P20-2, P21-1, P23-2), **1 partial**
(P19-6), **1 opened-not-instrumented** (P21-5), **1 practice-only** (P20-3), **15 absent**.

Nothing in `corpus/QUALITY.md` cites the 2026-10-19, -20, -21 or -23 files:
`grep -n 'considerthese/2026-10-1[9]\|considerthese/2026-10-2[0-3]' corpus/QUALITY.md` → no
hits. The only lesson-level citations of those files are as *operator material, not round
work*: `corpus/lessons/round-16-verifier-spotcheck.md:46-48` (2026-10-20),
`corpus/lessons/round-41-verifier-spotcheck.md:106` (2026-10-24 as operator-authored),
`LOG.md:738` (2026-10-19 read, proposals not taken as actions), `LOG.md:2137`
(2026-10-23 "operator material, not round work").

2026-10-25.md's other four suggestions (the file opens all five as "proposals only, not
acted on", `:42`):

| # | proposal | observed state at the entering tip |
|---|---|---|
| 1 (`:44-46`) | registry pin check | **not implemented before r47** — §1. The only committed instance is this round's frozen `tools/mori-pin-check.py` (`63eecf27`), plus the working-tree v2. Criterion drafted in the working tree as `corpus/QUALITY.md:1028-1040` (QUALITY 123, cites the 10-25 file at `:1029-1031`) — uncommitted at my read time. |
| 2 (`:47-49`) | host-path portability list | no tracking artifact exists (`grep -rn 'portability' corpus/QUALITY.md corpus/lessons/*.md LOG.md` → no hits). The reflection's own count of **13 files** reproduces exactly at both `9834fed4` and `2d85e33` under the scope `tools/*.py`/`tools/*.sh` + `.ufo/waves/round-4{0,1,2,3}/{count-*,conform.py,gen-wave*}.py|sh` → 13 (3 tools + 10 wave files: `tools/mori-blind-check.sh`, `tools/mori-misroot-sweep.py`, `tools/mori-round17-context-check.py`, `round-40/conform.py`, `round-40/count-c8.py`, `round-40/gen-wave-spec.py`, `round-41/conform.py`, `round-42/conform.py`, `round-42/count-c{1,2,3}.py`, `round-43/count-c1s.py`, `round-43/count-c2.py`). Wider scopes give 36 (all `count-*`/`conform` counters, rounds 26-43) and 61 (all wave `.py`/`.sh`), so the scope must be stated with the number. |
| 3 (`:50-52`) | track whether in-round critic flags get fixed | no artifact. The r45 instance the proposal cites is real and documented: `considerthese/2026-10-25.md:36-37` ("`w1/CritAxisHarm.md` §1b seat flagged these cells before `baabc992` landed, but nothing in the round enforced that flag") and `corpus/lessons/round-45-verifier-spotcheck.md:62-66` ("`w1/CritAxisHarm.md` §1b flagged these cells inside the round, before `baabc992` landed, and they shipped unmarked in `SKILL.md`"). |
| 5 (`:56-58`) | track retries | no artifact. The r45 attempt-2 refusal is recorded in `LOG.md:2615-2619` (`.ufo/watchdog.log:1325`, content-policy refusal) and `corpus/lessons/round-45-verifier-spotcheck.md:15` (`lane-dead-no-report mori round=45; retry same round … invalid_prompt`); the same watchdog line appears in the r24/r32/r34/r36/r38/r41 spot-checks — but only inside closure files, not in a lane-owned tracker (`grep -n 'lane-dead-no-report' LOG.md` → no hits). |

---

## 4. Boundaries, commands, and what I did not check

- Read-only throughout: `git log/show/diff/ls-tree/status/rev-parse/merge-base` only. No
  `git add/commit/stash/checkout/reset/pull/push`; no mutating `jj` command
  (`jj log` read-only). No file outside this report was written; the only scratch path
  created is the empty directory `.scratch/r47-ScoutConsider/`.
- `considerthese/` verified byte-unmodified (§ opening).
- **Not executed:** `tools/mori-pin-check.py`, `.ufo/waves/round-47/count-c2.py`, and every
  other lane tool. C1/C2 measurement belongs to the executor seats. Consequently the
  "PIN_CHECK=met / C2=met" verdicts are **UNVERIFIED by this seat**.
- **Not checked (out of lane scope):** sibling lanes. A cross-lane pointer exists at
  `.ufo/waves/round-29/w1/ConnSiblingOverlap.md:24`, which names a sibling lane's
  "calibration pin check" tool and calls it "reuse identity-bearing checks and negative
  controls". Whether a sibling implements the same pin-re-measurement class is
  **UNVERIFIED** here (that is the `ConnSiblings` seat's task).
- **Not checked:** whether the r42/r43 `considerthese`-audit seat reports were ever
  produced and then not committed (only their absence is observed), and the fate of the
  r43 raw seat log beyond its presence.
- **Tools installed:** none. No `pacman`, no `uv tool install`, no binary download. The
  tooling directive (`/home/vgpnk/.omp/agent/RULES.md`) was read first; nothing in this
  seat's task needed an install, and the host-wide pacman pause was respected by not
  touching pacman at all.
- Host reads: none beyond the repo. No tracing enabled, no tracefs write, no host state
  change; no `sudo` use.

---

## 5. Bottom line for the L1

1. **Suggestion 1 (2026-10-25.md:44-46) is genuinely new to the lane.** Nothing at or
   before `2d85e33` re-measures a registry pin from committed bytes; the r46 predecessor
   was routed for replacement (`corpus/lessons/round-46-verifier-spotcheck.md:71`) and the
   r47 contract sources C1 from exactly that routed defect plus this proposal
   (`contract.md:22-25`). QUALITY 123 in the working tree (`corpus/QUALITY.md:1028-1040`)
   should keep that wording.
2. **Six prior adoptions exist** and are already citable: QUALITY 114 (§2.2), 115 (§2.1),
   117 (§2.4), 122 (§2.3), plus the two implemented instruments for 2026-10-22 P22-1 (§2.5)
   and 2026-10-23 P23-4 (§2.6).
3. **Three adoptions are criterion-only with no instrument** (115's sweep, 114's ledger,
   117's general form) and one is a criterion that explicitly leaves its proposal open
   (122 / P24-3). If a round claims it "implemented" one of those, the trail to check is
   the one named in each §2 row.
4. **The 2026-10-19 → 2026-10-23 files have no adoption at all** — no QUALITY criterion
   cites them, and the only lesson citations call them operator material.
5. **The `considerthese` audit reports were only committed from r44 onward**; the r42 and
   r43 instances are missing as files, so the "where my suggestions end up" trail has a
   two-round hole before r44.
6. The stale `SKILL.md:912` pin was knowable inside the lane since r43
   (`.ufo/waves/round-43/count-c1s.py:133` asserts the true `(22, 0)`) — worth naming in the
   lesson as the concrete cost of the missing check.
