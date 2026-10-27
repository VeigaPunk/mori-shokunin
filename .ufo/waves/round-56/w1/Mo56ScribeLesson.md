# Mo56ScribeLesson — round-56 lesson skeleton (round 56, wave w1)

Seat: scribe for the round-56 lesson skeleton. Scope: draft the fenced skeleton
the L1 lands at `corpus/lessons/round-56.md` — (a) Gate table for S544/S545,
(b) Mistakes rows for round-55 routed defects 1 and 2, (c) census before→after
placeholders. No round-56 mistake is invented; the L1 fills those after the wave.

Read-only seat: no file in the lane was modified except this report. All writes
lived in `/fast/scratch/hyaku/mori-r56/Mo56ScribeLesson/` (removed before yield).
No tool installed, no pacman run, no git/jj mutation, no fleet-host write.

State observed at start: `mori-shokunin` worktree HEAD `acc62f54` with
`corpus/lessons/round-56.md` present but **untracked** (`git status --porcelain`
→ `?? corpus/lessons/round-56.md`; `git cat-file -e HEAD:corpus/lessons/round-56.md`
→ fatal: not in `HEAD`), i.e. the draft on disk is not yet landed. The skeleton
below is the landable version; deltas against that untracked draft are in
Findings F2–F4.

## Evidence (command → output, exit code)

All commands read-only; `cps` = `corpus/evidence/sources-r56/`.

| # | command | output (verbatim where short) | exit |
|---|---|---|---|
| 1 | `sha256sum $cps/watchdog-log-grammar.txt $cps/rfc8259.txt` | `38ba3e6b309e17d3d8038e8986e274bb363ac893d1c325fe145a95882a417796  watchdog-log-grammar.txt` · `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7  rfc8259.txt` | 0 |
| 2 | `grep -n 'launch \$lane\|A JSON text is a serialized value\|quotation-mark \*char' $cps/*.txt` | `watchdog-log-grammar.txt:1:  log "launch $lane round=$n pgid=$$ driver=hyaku-inline attempt=$a"` · `watchdog-log-grammar.txt:4:  log "launch $lane round=$n pgid=$pid"` · `rfc8259.txt:251:   A JSON text is a serialized value.  Note that certain previous` · `rfc8259.txt:461:      string = quotation-mark *char quotation-mark` | 0 |
| 3 | python substring + word-count check over the four quotes | `:1 substring=True words=7` · `:4 substring=True words=5` · `rfc8259.txt:251 substring=True words=7` · `:461 substring=True words=5` | 0 |
| 4 | `git diff --stat 5b295eee 8be2717b -- corpus/SOURCES.md` | `corpus/SOURCES.md \| 2 ++` / `1 file changed, 2 insertions(+)`; added lines begin `\| S544 \| …` and `\| S545 \| …` | 0 |
| 5 | `git diff 5b295eee 8be2717b -- corpus/SOURCES.md \| grep -E '^[+-]\|'` | two `+` rows (S544, S545), no `-` rows | 0 |
| 6 | `git show <rev>:corpus/SOURCES.md \| grep -cE '^\|[[:space:]]*S[0-9]{3,}'` at `5b295eee` / `3f494b49` / `8be2717b` / `acc62f54` | `316` / `318` / `318` / `318` | 0 |
| 7 | `git show <rev>:corpus/SOURCES.md \| grep -cE …` at `ca52426e` / `d27d943a` (r55 routed defect 1) | `298` / `316` | 0 |
| 8 | `grep -n 'S544\|S545' corpus/SOURCES.md` | line 324 `\| S544 \| shokunin driver launch-log grammar — scripts/hyaku/inline.sh and scripts/shokunin-watchdog.sh in the fleet repo \| own-work \| A \| … \| mined \| 2026-10-27 \| on-release \| corpus/knowledge/driver-liveness-r56.md, tools/mori-driver-liveness.py \|`; line 325 `\| S545 \| RFC 8259 … — https://www.rfc-editor.org/rfc/rfc8259.txt \| spec \| A \| … \| section 1 line 251, section 2 grammar lines 308 and 461; sha256 61a5378f… \| … \| mined \| 2026-10-27 \| on-release \| corpus/knowledge/vote-binding-r56.md, tools/mori-vote-bind.py \|` | 0 |
| 9 | `sources-census.sh census --file $S/../SOURCES-5b295eee.md` (copy of `SOURCES.md` at entering tip) | `file	rows	316` … `FLEET	rows	316` | 0 |
| 10 | `sources-census.sh census --root /home/vgpnk/Projects/shokunin mori` (live worktree = HEAD) | `mori	rows	318`, `FLEET	rows	318`, `mori	status.mined	267` | 0 |
| 11 | `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` into scratch; `diff -u` vs `evidence/census-start.txt` | exit 0, 23 `W04` lines; the diff is exactly `-exit=0` (only the receipt's appended exit line) | 0 |
| 12 | `grep -n 'rows' .ufo/waves/round-56/evidence/census-start.txt` | no match (`grep` exit 1) — the start receipt carries **no row-count line** | 1 |
| 13 | `git log --diff-filter=A --format='%h %s' -- .ufo/waves/round-56/evidence/census-start.txt` | `c419fe6d round-56 data: …` | 0 |
| 14 | `git show c419fe6d:corpus/SOURCES.md \| grep -cE …` / `grep -c 'S544\|S545'` | `318` / `2` | 0 |
| 15 | `grep -o 'rev=[0-9a-f]*' .ufo/waves/round-55/evidence/c1-at-landed.txt c2-at-landed.txt` | `rev=a27ec48210b136d9f2fd1b71c5e64f65f5a30e22` (both) | 0 |
| 16 | `sed -n '34,35p' .ufo/reports/round-55/mori.md`; `sed -n '41p'` | r55 report: "After at `d27d943a`" (C1, C2); "start rc 0, 298 rows, 23 W04 … end rc 0, 298 rows … Registry 298→298 rows" | 0 |
| 17 | `sed -n '60,61p' corpus/lessons/round-55-verifier-spotcheck.md` | routed defects 1 and 2 verbatim (fix texts quoted in the skeleton) | 0 |
| 18 | `grep -n '152\.' corpus/QUALITY.md`; `sed -n '972,982p' corpus/QUALITY.md` | QUALITY 152 ("A census receipt is the command's captured bytes, not a retyped summary"); QUALITY 119 ("A receipt names the revision it measured, and the verdict names that same revision") | 0 |
| 19 | byte-origin cross-check of the extract lines against the fleet writers | `inline.sh:149 True`, `inline.sh:176 True`, `inline.sh:182 True`, `shokunin-watchdog.sh:266 True` | 0 |
| 20 | `git diff --stat 8be2717b acc62f54 -- corpus/SOURCES.md` | empty output — registry unchanged from freeze receipts through the validated dispatch | 0 |
| 21 | `scripts/hyaku/disk-guard.sh status` | `/fast/scratch/hyaku 28% use, 583.2G free` (no heavy run attempted) | 0 |

Catalog pins used in the skeleton are the ones the freeze recorded:
`evidence/freeze-sha256.txt` carries `61a5378f…` (rfc8259 copy) and `38ba3e6b…`
(watchdog extract) and `6ced9da9b1f9c65065a8158735e0331938e8a599` as data commit.

## Skeleton (fenced — for the L1 to land at `corpus/lessons/round-56.md`)

````markdown
# Round 56 lesson (L1 MoriR56)

Entering tip `5b295eeebd87ebd610d8d39bfe2035742f740cfa`; round-55 closure
rejected-honest-stop (both claims unmet on recorded causes). Freeze tip
`3f494b49cde612d929e82887a48e1660c022c359`; data commits `c419fe6d`, `6ced9da9`;
receipts `8be2717b`. Claims: C1 coverage (FR5 driver-liveness probe), C2
operability (dual-shape vote binder). One v2 wave `w1` (64 seats). Receipts and
seat outcomes under `.ufo/waves/round-56/`.

## Gate

### New source rows (S544, S545)

Both rows are new and carry `opened` = 2026-10-27 in `corpus/SOURCES.md`. Each
quote below is a byte substring of the committed copy at the cited line.

| id | URL / source | accessed | ≤25-word located quote | decision |
|---|---|---|---|---|
| S544 | own-work — fleet repo `scripts/hyaku/inline.sh` and `scripts/shokunin-watchdog.sh`; extract `corpus/evidence/sources-r56/watchdog-log-grammar.txt`, sha256 `38ba3e6b309e17d3d8038e8986e274bb363ac893d1c325fe145a95882a417796` | 2026-10-27 | `log "launch $lane round=$n pgid=$$ driver=hyaku-inline attempt=$a"` — extract line 1, byte-equal to `inline.sh:149` (7 words) | admit, tier A — the hyaku-inline writer's launch line, the shape the probe parses |
| S544 | own-work — same row, second writer | 2026-10-27 | `log "launch $lane round=$n pgid=$pid"` — extract line 4, byte-equal to `shokunin-watchdog.sh:266` (5 words) | admit, tier A — the legacy daemon's launch line: one log, two writers |
| S545 | https://www.rfc-editor.org/rfc/rfc8259.txt — copy `corpus/evidence/sources-r56/rfc8259.txt`, sha256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7` | 2026-10-27 | `A JSON text is a serialized value.` — copy line 251 (7 words) | admit, tier A — a JSON text is one value, so the JSON channel reads string scalars |
| S545 | https://www.rfc-editor.org/rfc/rfc8259.txt — same row, grammar production | 2026-10-27 | `string = quotation-mark *char quotation-mark` — copy line 461 (5 words) | admit, tier A — the scalar grammar the binder anchors votes to |

Rejected rows this round: <!-- L1 fills; the draft records none — no reject
candidate was opened -->

### Reused source rows and row changes

`git diff 5b295eee 8be2717b -- corpus/SOURCES.md` → `1 file changed, 2
insertions(+)`: only the S544 and S545 rows are added (registry 316 → 318 rows),
and `git diff --stat 8be2717b acc62f54 -- corpus/SOURCES.md` is empty. No old
row changed. Used-by: S544 → `corpus/knowledge/driver-liveness-r56.md`,
`tools/mori-driver-liveness.py`; S545 → `corpus/knowledge/vote-binding-r56.md`,
`tools/mori-vote-bind.py`.

## Mistakes

The two rows below are the round-55 routed defects carried into this round;
round-56 mistakes are appended by the L1 after the wave, not claimed here.

| class | evidence pointer | captured-by | fix / shown able to fail |
|---|---|---|---|
| number-drift (retyped summary) | `corpus/lessons/round-55-verifier-spotcheck.md` routed defect 1: the r55 report wrote "Registry 298→298 rows: zero rows added or dropped" (`.ufo/reports/round-55/mori.md:41`), while the committed bytes hold 298 rows at `ca52426e` → 316 at `d27d943a`; `validate`-mode receipts print no row count, so "298" was retyped | QUALITY 152 — "A census receipt is the command's captured bytes, not a retyped summary" — plus the spot-check's own fix: paste `census`-mode output (`mori rows N`) or the counting command | this lesson's Census section pastes the command and its output: `sources-census.sh census --root /home/vgpnk/Projects/shokunin mori` → `mori rows 318`, `FLEET rows 318` (exit 0), and the entering-tip value from `census --file` on `SOURCES.md` at `5b295eee` → `file rows 316`. Shown able to fail: the r55 spot-check re-counted the committed bytes and found 298→316. |
| attribution (receipt revision) | routed defect 2: the r55 report's before→after line said "After at `d27d943a`" while the committed receipts are stamped `rev=a27ec48210b136d9f2fd1b71c5e64f65f5a30e22` (`.ufo/waves/round-55/evidence/c1-at-landed.txt`, `c2-at-landed.txt`); SCORECARD had it right | QUALITY 119 — "A receipt names the revision it measured, and the verdict names that same revision" | every After cell quotes the receipt's own `rev=` field: both round-56 freeze receipts carry `rev=3f494b49cde612d929e82887a48e1660c022c359` (`evidence/c1-at-freeze.txt`, `c2-at-freeze.txt`), and the end receipts must stamp the revision they measure. Shown able to fail: r55's receipts read `a27ec482…` while the report text read `d27d943a`. |

<!-- L1: append round-56 mistakes mined by the wave below, same four columns -->

## Census

Before (entering tip `5b295eee`): 316 rows. Captured with
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file <copy of
corpus/SOURCES.md at 5b295eee>` →

```
file	rows	316
FLEET	rows	316
exit=0
```

Cross-check: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show
5b295eee:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}'` → `316`.
The round-start `validate` receipt
`.ufo/waves/round-56/evidence/census-start.txt` is a direct capture (`exit=0`,
23 `W04` lines, final line `mori	ok	…/corpus/SOURCES.md`), but `validate` mode
prints no row count and the receipt carries no revision; it was committed in
`c419fe6d`, whose registry already holds 318 rows. The before count therefore
comes from the command above, never from a number typed beside the receipt.

After: PENDING — L1 fills from the integration tip, capturing bytes:

```
scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin mori \
  > .ufo/waves/round-56/evidence/census-end-rows.txt 2>&1; echo "exit=$?" >> .ufo/waves/round-56/evidence/census-end-rows.txt
scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori \
  > .ufo/waves/round-56/evidence/census-end.txt 2>&1; echo "exit=$?" >> .ufo/waves/round-56/evidence/census-end.txt
```

→ `mori rows <after>`, `FLEET rows <after>`, validate exit `<rc>` (expect 0);
row delta `<before> → <after>` read from the two `rows` lines. The After cell
cites the end receipts' measured `rev=` (QUALITY 119).

<!-- L1: sections below are named and unfilled: wave findings and their
resolutions, assimilation and quarantine, spot-check. -->
````

## Findings

- **MED — the round-start census receipt does not carry the before row count,
  and cannot evidence 316.** `evidence/census-start.txt` has no `rows` line
  (evidence row 12, grep exit 1), no revision stamp, and was committed in
  `c419fe6d` whose `corpus/SOURCES.md` already has 318 rows with S544/S545
  present (rows 13–14). The contract's "316 rows" (`contract.md`, "Start census
  receipt" clause) is the entering-tip count, verified independently at
  `5b295eee` (rows 6, 9). Writing "316 rows" beside that receipt would repeat
  routed defect 1's class, so the skeleton's Census section pastes the counting
  command and its output instead, and names the receipt's limitation.
  File: `.ufo/waves/round-56/evidence/census-start.txt`, `contract.md`.
- **MED — the untracked draft `corpus/lessons/round-56.md` cites a section it
  does not contain.** Its Mistakes fix cell says "this round's Sources &
  frontier section pastes the counting command and its output" (draft line 39),
  but the draft has no such section (`grep -n 'Sources & frontier'` → exit 1);
  the counting command appears nowhere in the draft. The skeleton moves that
  function into `## Census`, where the values actually live.
  File: `corpus/lessons/round-56.md:39`.
- **LOW — the draft's S544 Gate row cites the writer line but not the committed
  copy line or pin.** It reads `(inline.sh:149, in the extract)` with no extract
  line, no copy sha256, and no second-writer row; origin is only checkable by
  byte-matching the extract against the writers (row 19: `inline.sh:149`,
  `inline.sh:176`, `inline.sh:182`, `shokunin-watchdog.sh:266` all byte-equal).
  The skeleton gives extract line 1 / line 4 with the frozen sha256 and states
  the byte-equality that establishes origin. File: `corpus/lessons/round-56.md`
  Gate table.
- **LOW — the watchdog-log extract has no provenance header.** The committed
  copy is six bare log-statement lines: it names neither the writer files nor
  their line numbers, so the copy alone cannot establish that it came from
  `scripts/hyaku/inline.sh` / `scripts/shokunin-watchdog.sh`. Named limit of the
  Gate row, which pairs each quoted extract line with its verified writer line.
  File: `corpus/evidence/sources-r56/watchdog-log-grammar.txt:1-6`.
- **LOW — the draft's Gate quotes are correct but as a copy stand alone;
  verified anyway.** All four quotes I propose are byte substrings of the
  committed copies at the cited lines (row 3, all `True`) and each is ≤7 words,
  inside the 25-word ceiling. No correction to the draft's quotes was needed.
- **INFO — no round-56 mistake is claimed by this seat**, per the assignment;
  the Mistakes table carries only routed defects 1 and 2, and the census block
  carries placeholders, not derived numbers.

## Out of scope / not done

- Did not run either claim counter (`count-c1.py`, `count-c2.py`), the tools, or
  the fixtures — verification of C1/C2 belongs to the wave's executor and
  reviewer seats; my Gate rows are quote/registry checks only.
- Did not edit `corpus/lessons/round-56.md`, the registry, the counters, the
  controls, or any evidence file; did not commit.
- Did not re-fetch rfc-editor.org or the writer scripts over the network: every
  Gate quote is taken from the committed copies, as the assignment requires.
- UNVERIFIED: whether the L1 intends the `--file` census form in the lesson; the
  placeholder commands are the shape that produced the cited output here
  (`file rows 316`).
- This report starts no line with a vote verb; it carries no vote items.

## Report

Report: .ufo/waves/round-56/w1/Mo56ScribeLesson.md
