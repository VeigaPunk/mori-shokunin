# ScribeLesson — round 45 lesson (`corpus/lessons/round-45.md`)

Seat: `L1Mori45.ScribeLesson` (scribe, wave 1). Lane:
`/home/vgpnk/Projects/shokunin/mori-shokunin`. Measured tip
`3ad8faaa637ae466c61f9427fea1c208bf49ea82` (`git rev-parse HEAD` at write time);
contract entering tip `554ff416`. Scratch:
`.ufo/waves/round-45/tmp/ScribeLesson/` (no `/tmp` write, no tool install, no
git mutation, no campaign tool run in shokuknow). At the start of the write the
worktree held only untracked artifacts; **during** it other seats' edits landed
as modified tracked files (`git diff --stat`: `tools/mori-gate-registry.py` +747,
`mori-routed-r24.py` +588, `mori-routed-check.py` +314,
`mori-round19-regressions.py` +313, `mori-disk-rate.py` +206,
`mori-silence-cases.sh` +168, `mori-round41-calibration.py` +16, `contract.md`
+28). None of those modifications is mine; my writes are the two created files
listed in §7.

Deliverable: **`corpus/lessons/round-45.md`, 214 lines, created** (the file did
not exist at the entering tip; `ls corpus/lessons/round-45.md` → No such file).
Sections in the required order: `## Sources`, `## Gate`, `## Quarantine`,
`## Renumber`, `## Mistakes` (M1-M11), `## Carrier`. Table validator (unescaped
pipes per row, per block): `[]` mismatches.

## 1. Sources — every route opened, with byte receipts

Full table with quotes and word counts is in the lesson §Sources. The receipts
this seat produced (own `curl -sS -L --max-time 40`, sha256 of saved bytes,
mtimes local `-03:00`):

```
cdn.jsdelivr.net  cgroup-v2.rst 200 133236 a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad
raw.githubusercontent         200 133236 a9433bb0… (identical)
git.kernel.org/…plain         200 133236 a9433bb0… (identical)
man.archlinux.org proc.5.zh_TW 200  61889 b8ede81db8d462b46f5312b392caab7c5fe8d125057ca6093c2d3152efba8be7
doi 10.1145/3643916.3644413 -> dl.acm.org   403   5471 19e1e728cc8f452da0d488829d92b8d4b5bcdd2295c742d6d47911b7d63200f8  (Cloudflare "Just a moment...")
doi 10.1109/TSC.2026.3698682 -> ieeexplore  202      0 e3b0c442… (empty)
api.openalex.org S262         200  67270 43beb85ed970e371ab747a633296ff2906d920ef9431300ac4850fa4b40a973f
api.openalex.org S244         200  15977 b5090cd7020463e84d874aa244edc348fb524e9d9eee4574e6a37e6ecc463359
arxiv.org/abs/2403.18832      200  41919 2f302c3cb6c055452cd81d708e1e071b9fc9264681e550724e5a5d90cb771bb4
arxiv.org/pdf/2403.18832      200 1420568 ab8ab19551fb3614307b818e48b49885eca6f8af933b9eddfde8a18e6bf6018e
```

Admitted: **S473** (the jsdelivr copy), quote locations verified by
`grep -n` on that copy: `:1474-1476` (22 w), `:1476-1477` (10 w),
`:1518-1519` (17 w). Re-opened: **S472** (`proc.5.zh_TW`, entity-decoded
`:91-98`, 74 non-space chars) — not re-admitted. Refused at the publisher:
S244 (403) and S262/S268 (202/0 B); S244's span is nevertheless located on its
own declared carrier (arXiv PDF, extracted text `:29-30`, 14 w:
"We find that 98.9% of commits in our dataset contain sentences with rationale
information").

**The item's two "failed routes" did not fail.** The wave item asserted
`raw.githubusercontent.com` HTTP 429 and a `git.kernel.org` bot wall
(`w1-spec.json`, `ScoutKernelDoc`). My GETs and the seat's four scratch copies
(`tmp/ScoutKernelDoc/{cgroup-v2,raw-gh,gko,gitlab-mirror}.rst`) are all
200/133236/`a9433bb0…`. The lesson records this as M7 rather than repeating the
premise; the only walls measured are ACM/Cloudflare 403 and the S268 PDF
endpoints (418/15410, per `ScribeQuarantine.md`).

## 2. Gate decisions

- **Admit (1):** the level-naming theme, re-grounded — entry
  `corpus/knowledge/census-cgroup-levels-r45.md` (122 lines), `source: S473`,
  `coverage-map: FR1, FR12`; new ground is the fallback branch where
  `local_oom_kill` is filled from the service's hierarchical `memory.events`
  (`tools/mori-census.sh:1708-1711`, `:1862`). Prior holdings named in the
  lesson (`surfaces-r7.md:88-90`, `oom-kill-counter-kernel-only-r12.md:12`).
- **Reject (1):** `who-sets-the-scope-cap-r45.md` — own-work `file://` primary
  (S528) plus an issue statement that does not answer "who"; the answer is a
  kumitate-owned runner. Flip condition in the lesson.
- **Reject (2):** `cap-control-wording-r52.md` — a remediation proposal for the
  kumitate runner ("Adding `MemoryHigh=`…"), against `PROVINCE.md` "Detection
  and report only — never remediation". Flip: documentation-only, manual
  source, no recommendation, plus a measured runner receipt.
- **Two `file://`-only staged rows not adopted:** S558
  (`cgroup-surface-two-levels-r49.md:3`), S559
  (`selftest-cannot-tell-levels-r49.md:3`) — both cite
  `file:///…/lanes/mori/round12/.deepresearch/notes/r12-census-two-levels.txt`.
  The theme survives only where the round re-measured it from the lane's bytes.

Register state at write time (stated in the lesson, not worked around): the S473
row is **not appended** (`grep -c 'S473' corpus/SOURCES.md` → 0) and the README
map row is absent (`grep -c 'census-cgroup-levels-r45' corpus/README.md` → 0).
The L1 appends from `ScribeRows.md`.

## 3. Quarantine — three rows, no fabrication

| id | lane row | re-fetch | verdict |
|---|---|---|---|
| S244 | none in any commit (`git log -S'S244' -- corpus/SOURCES.md` → 0); staged `S483` | publisher 403/5471; **PDF 200/1420568**, span at `:29-30` | `quote-present` (own carrier) |
| S262 | `corpus/SOURCES.md:243` (OpenAlex anchor) | publisher 202/0; OpenAlex 200/67270, span words `52-68` | `quote-present` |
| S268 | none; staged `S507` | publisher 202/0; PDF endpoints 418/15410 | `unverifiable` (dated 2026-10-25) |

`unreachable` is not fabrication; the register's class text says the quote *was
not checked*, and the census findings for these three are `fetch-failed` with no
`quote` key. Totals corrected in the lesson: register header **194** rows / **324**
quotes; sections **194 + 109 = 303** rows over 19 lanes; census JSON 1901 rows /
4152 quotes / 78 `fetch_failed`. The slice is 3 of the 109 never-checked rows.

Two supporting findings that change a reader's use of the rows: staged `S483`'s
`used-by` `kernel-oom-line-attribution-r12.md` exists but contains none of the
row's identifiers (`grep -cE '3643916|2403\.18832|98\.9%'` → 0); staged `S507`'s
`used-by` `corpus/knowledge/oom-tracing-tracepoints-r42.md` does not exist.

## 4. Renumber

Own run: 245 registry ids, 136 staged ids, `comm -12` → **collisions S471,
S472** (`assimilation/collisions`). Shadowed by document: staged S471 = gihyo.jp
0061, staged S472 = gihyo.jp 0056; lane S471/S472 = proc(5) ja / zh_TW.
`assimilation/renumber-map.tsv` (delivered): **162 lines** — 26 comment lines
then 136 mapping rows, `:27` `S471→S474` … `:162` `S606→S609`, `S473` reserved
(`:10-14`). Routing only; citations re-pointed by document. M8 was recorded
against the 136-line draft I read at 07:47 (line 1 `S471→S473`) and is **closed**
in the delivered map.

Row arithmetic added as the L1 requested, both numbers re-derived here: **36**
at the entering tip and **39** at the landed tip (`PlanDataWalk.md:231-232`);
**7** eight-cell tables with **43** rows at `SKILL.md:162,524,588,643,718,796,881`
(23+2+1+2+3+1+11), of which v1 reads only the 23 at `:162`.

## 5. Mistakes — what is mine and what is relayed

- **M1, M2:** required by the item, both mined with fresh proofs.
  - M1: v1 auditor first-table scope and byte-grep selftest test; my fixture run
    against `tmp/RevAudit/aud-v1.py` printed
    `PASS (row 'fixture gate': 8 cells, entry resolves, --selftest present)` /
    `REGISTRY=met`, rc 0 for a comment-only tool. Captured-by: **none**
    (QUALITY 118 delegates to the same auditor).
  - M2: my 12-row fixture (8 revision-constant rows + 4 `HEAD` rows with
    `# @REV@`) printed `C1=met mismatches=0`, rc 0 under the r44 counter;
    ExecWitnesses independently scores all three witnesses `C1=met`
    (`w1/ExecWitnesses.md:120-127`). Captured-by: QUALITY 117 "Not covered"
    (`corpus/QUALITY.md:943-957`). **Fix observed:**
    `python3 .ufo/waves/round-45/count-c1.py --selftest` →
    `C1_SELFTEST pass=10 fail=0`, rc 0, including
    `head_reading_row_rejected`, `revision_constant_row_rejected`,
    `witness_dir_one_passing_witness`; the frozen predicate now requires
    `--other-rev` + `--witness-dir` (`:32-36`, `check_witnesses` `:396-437`).
    The full `C1=met` run still needs `figures.tsv`, absent at write time.
- **M3, M4 (relayed by the L1, cited from `tmp/RevAudit/v2-bypass-probes.txt`):**
  E4 a `--selftest` only inside `help=` is accepted (rc 0, `REGISTRY=met`);
  E5 the `selftest-flag: --help` escape is accepted.
- **M5 (mine, same receipt):** E6, a genuine branch with a named argv parameter,
  is **rejected** (rc 1, `no_selftest=1`) — the v2 marker is both over- and
  under-inclusive.
- **M6:** v1's own "good" fixture is a comment (`aud-v1.py:188`).
- **M7:** the failed-route premise (above).
- **M8:** a **draft** map's first target collided with this round's own row;
  the delivered map (162 lines, `:27`-`:162`, `S471→S474`) reserves `S473`, so
  the defect is closed in the delivered bytes. Captured by the census
  executor's cross-check, not by a criterion.
- **M9:** the quarantine item points at `corpus/SOURCES.md` for two ids that file
  never held.
- **M10:** "in two comments" vs the single literal `--selftest` at
  `tools/mori-silence-cases.sh:20`.
- **M11 (relayed, `RevengerAuditorHistory.md:278-296,327-331`):** four
  write-scope cells (`SKILL.md:183-186`) are false under an inherited `GIT_DIR`;
  F8 names four, not two, and the silence-oracle cell (`:166`) is true as
  written. Labelled in the lesson as a seat measurement I did not re-run.

## 6. Conflicts and limits (verbatim, not resolved by assertion)

1. `w1/RevAudit.md` was **absent** at write time; the M3/M4/E6 receipts are read
   from `tmp/RevAudit/v2-bypass-probes.txt` (v2 blob
   `d0aa10e3…`, 600 lines) and `fixtures.py`. If the landed report renumbers
   those probes, the lesson's M3/M4/M5 tags may need re-pointing; the byte
   receipts are unaffected.
2. `ExecWitnesses.md` receipt 2 cites a witness commit
   `b957dad8ddb38bc6b19e255e88a88bd4f912351f`; `git cat-file -e` in the lane
   returns 1 (**absent**), so that receipt is not reproducible from this
   checkout. My M2 repro is independent of it.
3. OpenAlex is **not byte-stable**: my fetch is `43beb85e…` (67270 B);
   `ScribeQuarantine.md` records `f757c4a6…` for the same 67270 B on the same
   day (URL form not recorded there). A digest anchor on that JSON API must be
   paired with a content check.
4. My first quarantine pass graded S244 `unverifiable` (no lane row, census
   finding carries no quote). `ScribeQuarantine.md` found the row's own declared
   carrier is the arXiv PDF; I re-fetched it (200/1420568/`ab8ab195…`) and the
   lesson now says `quote-present` for S244. The S268 verdict is unchanged and
   agrees with that seat.
5. No outside (non-lane) reviewer spot-check of this round's admit/reject is on
   record; the lesson says so in its author line rather than claiming one.
6. **Tracked edits landed mid-write, none of them mine.** `contract.md` gained
   `Correction 1` (`:111-137`, +28 lines: `moved>=1`, `tables>=7`,
   `--entering-rev` absence, the freeze manifest), and seven tools were
   rewritten by other seats (`git diff --stat`, §header). Consequences for a
   reader: (a) the lesson's tool line numbers name the committed bytes at
   `7cb59c68` or the scratch drafts in `tmp/RevAudit/`, never the post-edit
   worktree, so re-checking against the worktree will show moved lines (the
   `mori-silence-cases.sh` comment already moved from `:20` to `:27`); (b) the
   live `mori-silence-cases.sh` now has a real `--selftest` argv branch, so M1's
   "comment only" defect is historical for that row — the class still holds for
   the auditor's rule, which is what M3/M4/M5 probe; (c) `Correction 1` does not
   change any claim's subject and was appended before the after-measurements,
   as the contract requires.

## 7. Touched surfaces

- **Created:** `corpus/lessons/round-45.md` (214 lines).
- **Created:** this report.
- **Scratch only:** `.ufo/waves/round-45/tmp/ScribeLesson/` — fetched bins and
  JSON (`cgroup-v2.*`, `proc5.arch.bin`, `doi.s*`, `oa.s*`, `arxiv.*`,
  `s244.pdf`, `s244.txt`, `s244-raw.txt`), id lists (`reg-ids`, `staged-ids`,
  `collisions`), and two throwaway git repos (`m1/repo`, `m2/repo`) with their
  fixtures.
- **Read-only:** `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/README.md`,
  `corpus/knowledge/*`, `SKILL.md`, `PROVINCE.md`, `.ufo/waves/round-4[45]/**`,
  `/home/vgpnk/Projects/shokuknow/merge/mori/**`, and the campaign
  absent-defect register + `quote-lint-full-v5.json`.
- **Not done:** no edit to `SOURCES.md`, `README.md`, `QUALITY.md`, `SKILL.md`,
  `SCORECARD.md`, `LOG.md`, `contract.md`, or another seat's report; no git write;
  no campaign tool run (no `renumber-staged.py`, `merge-plan.py`,
  `quote-lint.py`, `absent-defect-register.py`); no tool install.

## 8. Out of scope / routed to round 46

- C2 item 4 must be keyed on parser keys / `case` patterns (M3/M4/M5); the
  current v2 rule is a proximity heuristic.
- C1's full `C1=met` receipt awaits `figures.tsv`; the hardened counter's
  selftest is green (10/10) but that is not the verdict.
- Write-scope cells under an inherited `GIT_*` environment (M11).
- The renumber rule (reserve ids named by the round's own admitted rows) is
  applied in the delivered map — M8 closed; the quarantine item must name the
  register when the lane row is absent (M9).
- The register's 109 never-checked rows are a census class, not a fabrication
  class; a future slice should say which of the two tables it came from.
