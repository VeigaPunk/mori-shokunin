# Mo55Scribe01 — round-54 D1–D6 mapped to append-only fixes and evidence

Seat: scribe, report-only. Lane `mori-shokunin`, round 55, wave `w1`.
Measured revision: data commit `b8b7064c2b54c8b6b22c288232a96c43fae1af47` (lane HEAD `b8a70adf` adds only
`.ufo/waves/round-55/{w1-dispatch.json,w1-input.json,w1-plan.json,w1.ready}` — `git diff --stat b8b7064c b8a70adf`,
4 files, +1824/−0). No production file was edited by this seat; the only file written is this report. Scratch
`/fast/scratch/hyaku/mori-r55/Mo55Scribe01` (disk-guard `/fast/scratch/hyaku` 26% used, 594.6 G free) removed
before yield. No installs, no pacman, no git/jj mutation, no counter or census re-run.

The six defects are the round-54 verifier spot-check's `Conformance defects (status-neutral)`:
`corpus/lessons/round-54-verifier-spotcheck.md:41-58` (D1 census receipt, D2 Gate locators, D3 correction sweep,
D4 leftover marker, D5 seat-report count, D6 M-label pointer). The round-55 contract routes them at
`.ufo/waves/round-55/contract.md:45-47`.

## Mapping (measured at `b8b7064c`)

| defect | routed ask (contract:45-47 / spot-check) | append-only fix present at `b8b7064c` | evidence | independent check this seat ran | status |
|---|---|---|---|---|---|
| D1 | capture census output mechanically; old receipt not rewritten | r55 census receipts are raw command output (tab-separated, trailing newline, `exit=0`), S349 URL correct; r54 receipt left byte-identical; disclosure appended | `.ufo/waves/round-55/evidence/census-start.txt:1-25`, `census-end.txt:1-25`; `corpus/lessons/round-54.md:115` | tabs on 24/25 lines, newline at EOF, `exit=0`, S349 URL compared to `corpus/SOURCES.md:246`; r54 blob unchanged across commits | landed, with a receipt-identity limitation (F3) |
| D2 | correct the four S515/S520/S522/S525 Gate locators | errata appended; original Gate rows retained | `corpus/lessons/round-54.md:109-111`; original rows `:27`, `:32`, `:34`, `:37` | corrected lines verified to start the quoted text; original lines verified not to | landed, correct |
| D3 | sweep `SCORECARD.md:2874` "Ten control clone revisions" with an appended correction line | **absent** — `SCORECARD.md` unchanged since `0c926fdf`; still reads "Ten"; no "12/14" text anywhere in it | `SCORECARD.md:2874`; `git diff --numstat 0c926fdf b8b7064c -- SCORECARD.md` → empty; `corpus/lessons/round-54.md:116` says "is appended in Round 55" (future tense); `corpus/lessons/round-55.md:58` asserts it as done | `grep -n "12/14\|Twelve" SCORECARD.md` → no control-clone hit; `grep -c SCORECARD w1-plan.json w1-dispatch.json` → `0`, `0` (no owner in the 64-seat plan) | **open** (F1) |
| D4 | commit the r54 dispatcher marker | `ca52426e` tracks `.ufo/waves/round-54/w1.ready.dispatched` (2 lines: `2026-10-27T02:04:34` + seat map) | `git show ca52426e --stat` (1 file, +2); `git ls-tree -r HEAD .ufo/waves/round-54/` lists both `w1.ready` and `w1.ready.dispatched` | tracked at HEAD; round-55's own equivalent is untracked (F2) | landed for r54; same defect recurs for r55 |
| D5 | correct the seat-report count | correction appended in the r54 lesson; r55 lesson states 73/74 | `corpus/lessons/round-54.md:117`; `corpus/lessons/round-55.md:58` | set difference over `w1-results.json` vs `w1/*.md`: 74 results, 73 reports, exactly `Mo54RevC1Counter` missing, no report without a result | landed on lane surfaces; two stale mentions survive uncorrected (F4) |
| D6 | add resolvable M1/M2 labels for the QUALITY 148/149 pointers | two M-headings appended to the r54 lesson; original `Mistakes` rows 67/68 identified | `corpus/lessons/round-54.md:101`, `:105`; originals at `0c926fdf:corpus/lessons/round-54.md:67-68` | headings exist; cited rows verified to be the number-drift and landing rows; strict fragment form differs from the citation (F5) | landed textually |

## Per-defect evidence

### D1 — census receipt

Round-55 receipts are the validator's raw output, not a transcription:

- `cat -A .ufo/waves/round-55/evidence/census-start.txt` → `mori^IW04^IS035 duplicate url …`; 24 of 25 lines carry a
  tab separator; line 24 is `mori\tok\t/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`; line 25 is
  `exit=0`; file ends with `0a` (newline), unlike the round-54 receipt which ends `exit=0` with no newline.
- Both receipts hold 23 `W04` lines and exit 0, matching the round-55 lesson's `## Census` statement
  (`corpus/lessons/round-55.md:68-70`).
- The S349 URL named in D1 is correct in both round-55 receipts
  (`…%E6%8A%80%E6%9C%AF%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf`, `census-start.txt:17`, `census-end.txt:17`) and equals the
  registry cell `corpus/SOURCES.md:246`; the round-54 receipt still carries the wrong
  `…%E7%99%BD%E6%96%87%E6%9C%AC.pdf` (`b8b7064c:.ufo/waves/round-54/evidence/census-end.txt:18`), which is
  append-only correct.
- Append-only proof: `git rev-parse 0c926fdf:.ufo/waves/round-54/evidence/census-end.txt` and the same at
  `b8b7064c` both print `366b03be5d9003d28e2cd73d10b3316c9033f18b` — the old receipt was not rewritten.
- Disclosure appended: `corpus/lessons/round-54.md:115`.

Limitation (F3): `sha256sum` of `census-start.txt` and `census-end.txt` both print
`611391325d4d0d20955c8939cc9688dc0fa54d329c11eac7fa25abfc1ef9c61b`, while the registry grew 298 → 316 rows
(`git show c9b908f0:corpus/SOURCES.md | grep -cE '^ {0,3}\| *S[0-9]{3,} '` → 298; same at `b8b7064c` → 316). The
warning-only output makes identity expected, but the end receipt then cannot evidence that it was produced after
the last registry edit, and neither receipt carries the `command:` header the round-54 receipt had.

### D2 — Gate locators

Original Gate rows retained (`corpus/lessons/round-54.md:27` "line 1819"; `:32` "rendered text, line 1225";
`:34` "line 68"; `:37` "line 7"). Errata at `:111` names 1850 / 1409 / 70 / 3. Verified against the committed
copies under `corpus/evidence/sources-r54/`:

| row | original | corrected | this seat's read |
|---|---|---|---|
| S515 | `memcontrol.c.v7.3:1819` | `:1850` | `sed -n '1819p'` → `\tif (memcg) {` (not the quote); `sed -n '1850p'` → `\tpr_info("memory: usage %llukB, limit %llukB, failcnt %lu\n",` — the quote starts there |
| S520 | rendered line 1225 | rendered line 1409 | `cgroup-v2.7.3.html:1225` → `<p>All memory amounts are in bytes. …`; `:1409` → `<dt>oom_kill</dt><dd><p>The number of processes belonging to this cgroup` — the sentence starts there |
| S522 | `hwpoison.rst.v7.3:68` | `:70` | `:68` is blank; `:70` → `\tSend SIGBUS when the application runs into the corrupted page.` |
| S525 | `ras_event.h.v7.3:7` | `:3` | `:7` → `#define _TRACE_HW_EVENT_MC_H`; `:3` → `#define TRACE_SYSTEM ras` |

Append-only proof: `git diff --numstat 0c926fdf b8b7064c -- corpus/lessons/round-54.md` → `24  0`; the single
`^-` line from `git diff | grep -c "^-"` is the `--- a/…` header. No original line was deleted.

### D3 — correction sweep (open)

`SCORECARD.md:2874` still reads "… Ten control clone revisions were removed and could not be replayed
independently; receipts are first-run observations, not durable revision proofs." at `b8b7064c` and at HEAD.
`git diff --numstat 0c926fdf b8b7064c -- SCORECARD.md` prints nothing, and `grep -n "12/14" SCORECARD.md` finds no
control-clone correction. `git diff --stat b8b7064c b8a70adf` shows SCORECARD is untouched after the data commit.

Two lesson lines state the opposite of the tree:

- `corpus/lessons/round-54.md:116` — "The scorecard correction is appended in Round 55; this historical line is
  retained." (describes a future action)
- `corpus/lessons/round-55.md:58` — "D3: appended correction says the r54 control receipt limitation is 12/14
  unresolvable revisions, not ten." (states it as done)

The only 12/14 text in the tree is `corpus/lessons/round-54.md:79` (the round-54 closure's own lesson correction),
which is not the routed SCORECARD sweep. No seat in the dispatched plan carries the sweep:
`grep -c SCORECARD .ufo/waves/round-55/w1-plan.json` → `0`, same for `w1-dispatch.json`; the plan's only D1–D6
mention is this seat's report-only task.

### D4 — marker

`git show ca52426e --stat` → `1 file changed, 2 insertions(+)` on
`.ufo/waves/round-54/w1.ready.dispatched`; the file holds the dispatch timestamp `2026-10-27T02:04:34` and the
74-name seat map. `git ls-tree -r --name-only HEAD .ufo/waves/round-54/ | grep ready` lists `w1.ready` and
`w1.ready.dispatched`. The r54 marker is tracked at the entering tip `ca52426e`.

### D5 — seat-report count

Own recount over `b8b7064c`:

```
python3 - <<'EOF'
import json,os,glob
r=json.load(open('.ufo/waves/round-54/w1-results.json'))['results']
names={x.get('name') for x in r}
md={os.path.basename(p)[:-3] for p in glob.glob('.ufo/waves/round-54/w1/*.md')}
print(len(r),len(names),len(md),sorted(n for n in names if n not in md),sorted(md-names))
EOF
```

prints `74 74 73 ['Mo54RevC1Counter'] []` — matching `corpus/lessons/round-54.md:117` and
`corpus/lessons/round-55.md:58`. The original statement is retained append-only at
`corpus/lessons/round-54.md:75` and `LOG.md:2910-2911` ("four other seats lack report files").

### D6 — M labels

Appended headings `corpus/lessons/round-54.md:101` (`### M1 — number-drift (QUALITY 148)`) and `:105`
(`### M2 — landing / misroot strays (QUALITY 149)`); the cited rows are the originals at
`0c926fdf:corpus/lessons/round-54.md:67` (number-drift) and `:68` (landing), as the errata states. The pointers
that needed them are `corpus/QUALITY.md:1480` (`lessons/round-54.md#M1`) and `:1493` (`#M2`). Round-53's own labels
are bullets (`corpus/lessons/round-53.md:79`, `:99`), so the repo's M-label citations are textual, not strict HTML
fragments; see F5.

## Findings

**F1 — MEDIUM (contract conformance, no claim impact).** Routed defect D3 is unlanded at the measured data commit
and at HEAD: `SCORECARD.md:2874` still says "Ten control clone revisions", no correction line exists, and
`corpus/lessons/round-55.md:58` asserts the correction as already appended. The 64-seat plan assigns no owner
(`w1-plan.json`, `w1-dispatch.json` contain zero `SCORECARD` mentions). Evidence: `SCORECARD.md:2874`;
`corpus/lessons/round-55.md:58`; `corpus/lessons/round-54.md:116`; `git diff --numstat 0c926fdf b8b7064c --
SCORECARD.md` (empty).

**F2 — MEDIUM (recurrence of the fixed defect).** Round 55's own dispatcher marker
`.ufo/waves/round-55/w1.ready.dispatched` (contents `2026-10-27T03:42:31` + seat map) is present in the working tree
and untracked at HEAD (`git status --porcelain` → `?? .ufo/waves/round-55/w1.ready.dispatched`;
`git ls-tree HEAD .ufo/waves/round-55/` lists `w1.ready` but not `w1.ready.dispatched`). The r54 fix does not
prevent the same leftover unless closure commits it. Evidence: `git status --porcelain`; `git show --stat b8a70adf`.

**F3 — LOW (evidence limitation, D1).** `census-start.txt` and `census-end.txt` are byte-identical
(sha256 `611391325d4d0d20955c8939cc9688dc0fa54d329c11eac7fa25abfc1ef9c61b`) with no command/timestamp header,
while the registry grew 298 → 316 rows; the end receipt therefore cannot show it was captured after the last
registry edit beyond "no new warnings". Not a transcription like the round-54 defect (tabs, newline and exit token
are correct). Evidence: `.ufo/waves/round-55/evidence/census-start.txt:1-25`, `census-end.txt:1-25`;
`corpus/lessons/round-55.md:68-70`.

**F4 — LOW (incomplete correction sweep, D5).** The stale "four other seat reports are absent" sentence survives
with no appended correction on two surfaces the lane left untouched: `LOG.md:2910-2911` and the fleet report
`.ufo/reports/round-54/mori.md:8` (outside the lane's write scope). The lane's own correction is
`corpus/lessons/round-54.md:117`. Evidence: `LOG.md:2910`; `.ufo/reports/round-54/mori.md:8`.

**F5 — LOW (locator precision, D6).** The appended heading `### M1 — number-drift (QUALITY 148)` yields the
fragment `#m1--number-drift-quality-148`; the citation `lessons/round-54.md#M1` does not resolve as a literal
fragment. This matches the repo's existing loose convention (`corpus/QUALITY.md:27` cites `round-12.md#M20`, whose
`M20` is a table cell at `corpus/lessons/round-12.md:43`), so the label is now findable but still not an anchor.
Evidence: `corpus/lessons/round-54.md:101,105`; `corpus/QUALITY.md:1480,1493`.

**F6 — LOW (documentation).** The errata section that carries the D2/D1/D3/D5 corrections is titled
`## Round-55 append-only errata (outside spot-check D1–D6)` (`corpus/lessons/round-54.md:99`), which contradicts its
own contents. Evidence: `corpus/lessons/round-54.md:99-117`.

## Not verified here

- The census was not re-executed (no decoration re-runs); D1's verdict rests on receipt format, exit token, URL
  token and blob immutability, not on a fresh validator run.
- C1/C2 counters and their receipts were not read for scoring; this seat emits no votes.
- The contract's additional routed item "narrow panic switch wording" (`.ufo/waves/round-55/contract.md:45-47`,
  round-54 closure routed defect 3) and the S508/S520 anchor superseders (`SCORECARD.md:2878`) are outside the
  D1–D6 assignment and were not assessed.
- No claim about whether closure will land D3 or commit the r55 marker; both are open at the measured revision.

## Findings (summary)

| severity | finding | evidence |
|---|---|---|
| MEDIUM | D3 unlanded; lesson asserts it landed; no plan owner | `SCORECARD.md:2874`; `corpus/lessons/round-55.md:58`; `corpus/lessons/round-54.md:116` |
| MEDIUM | D4 recurs: r55 dispatcher marker untracked | `git status --porcelain`; `git show --stat b8a70adf` |
| LOW | D1 end receipt byte-identical to start, no command header | `.ufo/waves/round-55/evidence/census-{start,end}.txt` sha256 `61139132…` |
| LOW | D5 stale mention uncorrected in `LOG.md` and fleet report | `LOG.md:2910`; `.ufo/reports/round-54/mori.md:8` |
| LOW | D6 citation is not a literal fragment | `corpus/QUALITY.md:1480,1493`; `corpus/lessons/round-54.md:101` |
| LOW | errata heading mislabels its own D1–D6 content | `corpus/lessons/round-54.md:99` |
