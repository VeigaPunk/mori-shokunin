# ReopenS147 — wave-2 attack on row S147 (supersedes S101)

**Verdict: partial** — S147 is correct where it exists, but it does not exist at the dispatched revision
`f2de0eed`: the row, the Gate line and the `supersedes S101` entry landed one commit later in `6b695b0`. At
`f2de0eed` the live reader already cites a row that is not in the registry, and the official counter prints
`C1=unmet`. At the landing commit and at tip `84abe93` every content check holds, with one formatting defect:
the landed Gate line has 7 cells against the 6-column table (the sha256 cell is duplicated), deviating from the
drafting seat's line. Seat: MoriR28.ReopenS147 (leaf). Lane writes: this file only.

## Check verdicts

| # | check | verdict |
|---|---|---|
| 1 | Source URL(s) re-opened by curl now | holds — HTTP 200, sha256 identical to Gate/anchor digest |
| 2 | Gate line in `corpus/lessons/round-28.md` (verbatim quote, ≤25 words, sha256 vs fetch) | breaks at `f2de0eed` (line absent); at `6b695b0`/`84abe93` quote+sha256 hold, but the row is malformed (7 cells vs 6 columns) |
| 3 | Every cell of S147 against the bytes | breaks at `f2de0eed` (row absent); holds at `6b695b0`/`84abe93` (all 11 cells verified) |
| 4 | Named defect fixed in S147, not copied | holds (at landed row) — the defective teaches is quoted only to be refuted |
| 5 | Every used-by path cites S147; no live reader states defective wording (QUALITY 77) | holds at `6b695b0`/`84abe93`; at `f2de0eed` used-by paths cite S147 but the row is absent (one-commit dangling citation) |

## 1. Fresh fetch

`curl https://raw.githubusercontent.com/can1357/oh-my-pi/45c35e40c46166dc726ccc52f5d27f40f2449f99/docs/settings.md`
→ HTTP 200, 148,359 bytes, sha256 `0b2e1457021fa526f2c35015672f1d7ccbac95e7b9f217528ab8022c55ed5883`, accessed
2026-10-22T18:55:47Z. Identical to the Gate-line digest and to the anchor cell — no upstream drift.
Cross-sources for the teaches cell: `docs/tools/eval.md` sha256 `fb2fc4a1…e495c` (28,027 B), `sdk.ts` sha256
`c0228add…be6957` (255,525 B). Tag check: `api.github.com/repos/can1357/oh-my-pi/git/refs/tags/v18.12.6` →
`sha 45c35e40c46166dc726ccc52f5d27f40f2449f99`, fetched 18:58:25Z.

## 2. Gate line

- At `f2de0eed`: `corpus/lessons/round-28.md` Gate table lists S145, S146, S148–S152 only — **no S147 line**
  (`git grep S147 f2de0eed` hits the file only at `:11` prose). Breaks.
- At `6b695b0` and `84abe93` (`corpus/lessons/round-28.md:67`):
  `| S147 | https://raw.githubusercontent.com/…/docs/settings.md | 2026-10-22T17:59:03Z | `0b2e…5883` | `0b2e…5883` | `:623` "`async.maxJobs` \| number \| `100` \| Running background-job cap, floored to at least 1" (11 words) | admit, A, mined (SupersedeS101) |`
  - Quote: 11 words (`async.maxJobs number 100 Running background-job cap floored to at least 1`), ≤25 ✓; the
    words match `settings.md:623` verbatim (`| \`async.maxJobs\` | number | \`100\` | Running background-job cap,
    floored to at least 1; …`), pipes rendered as `\|`. Holds.
  - sha256 `0b2e…5883` equals my 18:55:47Z fetch. Holds, no drift.
  - **Defect (low):** the line has **7 cells** — the sha256 is duplicated into the "located quote" column —
    against the 6-column header (`| id | source | access time | sha256 | located quote | decision |`; S145,
    S146 hold 6). The drafting seat's line (`.ufo/waves/round-28/w1/SupersedeS101.md` §4) has 6 cells and the
    lesson claims "Each line is copied from the drafting seat's report" — it was not copied verbatim. The
    counter's gate check (URL + 64-hex + quoted span) still passes, so `C1=met` stands; the table is malformed.

## 3. Row cells at the landed bytes (S147 = `corpus/SOURCES.md:153`, 11 fields)

- **source** — same URL as S101, fetch 200 (above). Holds.
- **kind docs / tier A** — same as S101. Holds.
- **scope** — "declared type, the default, the floor it states and the maximum it does not state; the ceiling is
  documented on the eval page (S103) and enforced in the code (S099)": `:623` states type `number`, default
  `100`, floor 1, no maximum (verified verbatim). Holds.
- **anchor** — `### Tools and approvals` is `settings.md:593` verbatim; `:623` is the file's only `maxJobs`
  mention (`grep -c -i maxjobs` = 1); "first committed upstream 2026-09-30 (1b3222187919, absent from its
  parent 30aec05d)" verified: `maxJobs` lines = 1 at `1b3222187919`, = 0 at `30aec05d`, commit date
  `2026-09-30T17:57:16Z` (API); file sha256 in cell = fresh digest; "(148,359 bytes)" = download size. Holds.
- **teaches** — opens `supersedes S101 — ` (em dash); differs from S101's cell; quotes the old wording
  ("states no upper bound", "reads as honoured", "docs and code disagree for values above 100") and refutes it;
  corrected facts verified below. Holds.
- **status mined, opened 2026-10-22, recheck on-release** — S101's convention. Holds.
- **used-by** — `corpus/knowledge/harness-job-capacity-r25.md, corpus/lessons/round-28.md`; both cite S147 at
  `6b695b0` and `84abe93` (`git grep -q -w S147 <rev> -- <path>`). Holds.
- At `f2de0eed`: `git grep -w S147 f2de0eed -- corpus/SOURCES.md` → no match; id sequence skips S147
  (`:152` S146, `:153` S148). Breaks (row_absent).

## 4. Named defect — fixed, not copied

The round-27 closure (`corpus/lessons/round-27-verifier-spotcheck.md:148`, via `corpus/lessons/round-27.md:35`)
and wave-1 `SupersedeS101.md` §1 name S101's first-published teaches: "…but states no upper bound, so a
configured value above 100 reads as honoured; the code clamps it, so docs and code disagree for values above
100" (`corpus/SOURCES.md:107`, restored cell — still present by QUALITY 81 design). S147's teaches names all
three claims as false, then states the corrected teaching, which I re-verified: `eval.md:258` documents the cap
"default and maximum 100"; `sdk.ts:2284` is `maxRunningJobs: () => Math.min(100, cfgAsyncMaxJobs.get(settings)),`.
The correction is new wording, not a copy of either the defective or the round-25 edited cell. Holds.

## 5. Used-by and QUALITY 77

- Used-by: both cells cite S147 at `6b695b0` and `84abe93` (above). Holds.
- Live readers at `f2de0eed`: `git grep -n -w S101` in `SKILL.md PROVINCE.md corpus/README.md corpus/knowledge/`
  → 0 lines; `git grep -n -i 'docs and code disagree|states no upper bound|reads as honoured'` → 0 lines;
  `git grep -n -w S147` → `harness-job-capacity-r25.md:1,:47` only. `readers_left=0` (counter). QUALITY 77
  wording-wise holds, but the reader was repointed **before** the row existed: at `f2de0eed` S147 is a dangling
  citation (absent row). Breaks at the pin; harmless at tip.
- Live readers at `84abe93`: identical greps → clean. Holds.

## Official receipts

```
$ bash .ufo/waves/round-28/count-c1.sh f2de0eed
row_identity=rows=151 changed=0 removed=0 bad=0
superseding=7/8 ids=S096,S097,S127,S128,S129,S131,S140
fail S147 row_absent
readers_left=0
C1=unmet   exit=1

$ bash .ufo/waves/round-28/count-c1.sh 6b695b0   # identical at 84abe93
row_identity=rows=152 changed=0 removed=0 bad=0
superseding=8/8 ids=S096,S097,S101,S127,S128,S129,S131,S140
readers_left=0
C1=met   exit=0
```

## Findings

1. **Dispatch pin predates the row (medium, sequencing).** At `f2de0eed` C1 is unmet (`fail S147 row_absent`)
   and `corpus/knowledge/harness-job-capacity-r25.md:1,:47` cites an id with no row — a one-commit dangling
   citation window (`f2de0eed` … `6b695b0`). The row lands in `6b695b0` ("last C1 row"); the wave-2 attack
   target does not carry the claimed state.
2. **Gate line malformed (low).** `corpus/lessons/round-28.md:67` has a duplicated sha256 cell (7 cells vs
   6-column header), not verbatim-copied from `SupersedeS101.md` §4. Counter accepts it; table shape is off.
3. **Residual risk:** none found in row content — every claim cell verified against fresh upstream bytes
   (`settings.md` 200/identical digest, `eval.md:258`, `sdk.ts:2284`, first-commit claim at `1b3222187919` vs
   `30aec05d`, tag→commit mapping). Verification gap: the counter accepts a 7-cell Gate line — a stricter
   cell-count check would catch defect 2.

No installs; pacman untouched. Fetches: plain `curl` GETs on the URLs and GitHub API shown, all recorded above.
