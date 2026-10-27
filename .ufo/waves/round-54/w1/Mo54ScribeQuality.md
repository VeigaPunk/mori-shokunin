# Mo54ScribeQuality — QUALITY.md drafts (round 54, wave w1)

Seat: Mo54ScribeQuality (scribe). Lane: mori-shokunin. Read-only over the lane; the only file this seat wrote
outside its scratch is this report. No tool installed or upgraded (nothing was needed); no pacman transaction.
Host as seen: kernel 7.2.11-arch1-1, single NUMA node (`/sys/devices/system/node/node0`).

Rev read: lane worktree HEAD `2d0347a32b6befd7fd946a83319e04f6d8f004b9`, data commit
`78295c764093ff1f6cee08d7246679900bde7265`, entering tip `39dcf4d7e410d362781a47e8365ca23b5c807598`, first data
commit `1116c092`.

Deliverable: four QUALITY.md criteria continuing the numbering at 148, in the fenced block below, each with
Lesson / Rationale / Check / Shown able to fail / Not covered and a receipt for every arm. The L1 integrates.

## State found before drafting (uncommitted, not this seat's)

`git status --porcelain` (lane): `M PROVINCE.md`, `M SCORECARD.md`, `M SKILL.md`, `M corpus/QUALITY.md`,
`M corpus/README.md`, and untracked `.ufo/waves/round-54/checks/`, `evidence/gate-rejects.txt`,
`evidence/receipt-stage-before.txt`, `w1.ready`, `w1.ready.partial`, `w1/`.

- `corpus/QUALITY.md` at `78295c76` is 1477 lines and ends with row 147. The working tree is 1518 lines
  (`git diff --stat` → `41 insertions(+)`, mtime `2026-10-27 01:41:20 -0300`): rows **148–151 already exist** there,
  starting at lines 1479, 1492, 1504, 1511, covering the same four criteria this seat was asked to draft. They were
  not written by this seat; this seat did not edit the file. My draft below is the independent version; the
  divergences from those bytes are listed under **Divergences** so the L1 can pick or merge rather than duplicate.
- `SKILL.md` `## Round54` exists only in the working tree (line 1211; committed `78295c76` stops at `## Round53`,
  line 1178). `SCORECARD.md` carries, also uncommitted, a `**Round-53 correction:**` and a `**Round-50 correction:**`
  paragraph (+15 lines), both pointing at "lesson `corpus/lessons/round-54.md` M1".
- `corpus/lessons/round-54.md` does **not** exist: `git cat-file -e 78295c76:corpus/lessons/round-54.md` fails and
  `ls corpus/lessons/` has no round-54 file. Every `lessons/round-54.md#M1|#M2` anchor in the working-tree rows and in
  the SCORECARD corrections is therefore unresolvable until the lesson lands.
- `.ufo/waves/round-54/checks/receipt-stage.py` and `.ufo/waves/round-54/evidence/receipt-stage-before.txt` are
  **untracked** at `78295c76` (and absent from `evidence/freeze-sha256.txt`, `grep 'checks/'` rc 1). The tracked
  round-54 receipts I cite are: `d3-relocation.txt`, `control-c1-no-line.txt`, `c1-at-data.txt`, `c2-at-data.txt`,
  `sweeps.txt`, `c1-scope.txt`, `c1-claims.txt`, `c2-claims.txt` (all present in
  `git ls-tree --name-only 78295c76 .ufo/waves/round-54/evidence/`).

## Draft (fenced; numbering continues from 147, house style: bold statement, Lesson, Rationale, Check, Shown able to fail, Not covered)

```markdown
148. **A SCORECARD claim row cites the receipt measured at the landed revision, never an intermediate one.** Lesson:
    round-53 closure D2 (routed as D2 in `.ufo/waves/round-54/contract.md`, `## Frontier step, assimilation,
    mistakes, considerthese, routed defects`): the round-53 C1/C2 After cells cite `c1-at-salvage.txt` and
    `c2-at-salvage.txt` (R = `0df80303`), while the report measures `0b36d23e` (`c1-at-landed.txt`,
    `c2-at-landed.txt`); the round-50 C1/C2 rows repeat the pattern with `a2-c1-at-data.txt`/`a2-c2-at-data.txt`
    beside existing `a2-c1-at-landed.txt`/`a2-c2-at-landed.txt`. Rationale: in both rounds the intermediate and the
    landed lines agree token for token, which is why QUALITY 146 stays silent — the numbers cannot expose the stage,
    so the citation is the only place a reader is told which measurement the row was written against. Check:
    `python3 .ufo/waves/round-54/checks/receipt-stage.py <rev>` flags every claim row (`| C…` carrying a
    `C<n>=met|unmet` tally) of a `## Round N` section whose After cell cites `evidence/<x>-at-data.txt` or
    `evidence/<x>-at-salvage.txt` while `.ufo/waves/round-N/evidence/<x>-at-landed.txt` exists at that revision and
    no later paragraph opening `**Round-N correction:**` names `<x>-at-landed`; it prints one `FLAG line …` per
    citation and `RECEIPT_STAGE rev=<rev8> cited_intermediate=N flagged=N`, exit 1 while any flag remains, exit 0
    when the set is empty. Shown able to fail: at `39dcf4d7` it prints `flagged=5`, exit 1 —
    `FLAG line 2668 round 50 cites a2-c1-at-data …`, `line 2669` (round 50 C2), `line 2796` (round 53 C1),
    `line 2797` twice (round 53 C2, `c2-at-salvage` and the `c2-at-data` aside) — and the body is byte-identical to
    the filed receipt `.ufo/waves/round-54/evidence/receipt-stage-before.txt` (re-run by this seat, 2026-10-27). The
    pass arm is a re-run at a revision that contains the two `**Round-… correction:**` paragraphs this round appends
    to `SCORECARD.md`: carried into a scratch clone over `78295c76` they read `RECEIPT_STAGE rev=08f434e6
    cited_intermediate=5 flagged=0`, exit 0 — at the lane tip itself the paragraphs are still uncommitted, so
    `flagged=0` is fixture evidence, not a lane reading. Not covered: receipts named in another style
    (`after-c1.txt`, `c1-tip.txt`) are not classed as intermediate; a correction line is matched by name, not by
    content, and only when it opens a paragraph; rows before the `*-at-landed` naming (rounds ≤ 49) are out of
    reach; the script reads `git show <rev>:SCORECARD.md`, so a correction sitting in a working tree is invisible to
    it and the script itself must be committed for the Check to resolve at a revision; a row that names the landed
    receipt while its digits come from another file still passes this check (that half is QUALITY 146).

149. **A misroot relocation lands under the wave directory of the round that swept it, never at the lane root.**
    Lesson: round-53 closure D3 (routed as D3 in the round-54 contract, `## Mistakes to mine`): seven round-27 seat
    fetches (`base.c`, `main.c`, `meminfo.c`, `oom_kill.c`, `sd-main.c`, `user@.service.in`, `MANPAGE.md`) were
    relocated by round 28 and one file (`0`) by round 38 "into the same relative path under the lane" — the lane
    root — and stayed tracked there for 26 rounds. Rationale: a lane-root `.c` file is indistinguishable from the
    lane's own material to every later sweep, while a wave directory names both the round that produced the file and
    the sweep that moved it. Check: `git ls-tree --name-only <rev>` at the lane root lists only the lane's own
    entries (`.gitignore .scratch .ufo AGENTS.md LOG.md MINT.md PROVINCE.md README.md SCORECARD.md SHONEN.md
    SKILL.md considerthese corpus tools`), and each relocated file resolves at
    `.ufo/waves/round-28/misroot-lane-root/<name>` or `.ufo/waves/round-38/misroot-lane-root/0`. Shown able to fail:
    at `39dcf4d7` the root listing adds all eight (`0 MANPAGE.md base.c main.c meminfo.c oom_kill.c sd-main.c
    user@.service.in`); at the data commit `1116c092` and at its correction commit `78295c76` (the landed data
    commit) it lists none of them. The targets are byte-identical to the strays: each receipt line
    `.ufo/waves/round-54/evidence/d3-relocation.txt` carries a sha256 and `cmp=ok`, and `git show 78295c76:<target>`
    piped through `sha256sum` reproduces the eight receipt hashes line for line (this seat, 2026-10-27). Not covered:
    a misroot deeper in the tree (under `corpus/`, `tools/`) is not caught by a root listing; the allowed set is this
    round's list and must be amended when the lane adds a root entry on purpose (`.scratch` is a tree there today);
    the check proves placement, not that the file came from the round whose directory now holds it.

150. **A release recheck says where each quote now begins, not only that its words survive.** Lesson: the round-53
    named limit ("`held` proves the v7.2 quote's words still occur somewhere in the v7.3 file"), carried as C1's line
    arm in the round-54 contract and in `knowledge/kernel-v7.3-recheck-r54.md`. Rationale: every one of the 31 v7.2
    quotes still occurs in the v7.3 copy, so a status-only recheck passes a relabel; a line number is the cheapest
    statement of place that another seat can check against the pinned copy, and it is what makes "held" falsifiable.
    Check: `python3 .ufo/waves/round-54/count-c1.py <rev>` requires, per ledger row, a `line` cell that is a line
    number of the committed v7.3 copy on which an occurrence of that row's quote begins (predicate P-C1; `line_ok`
    counts the rows that pass, `failed=line` names the arm). Shown able to fail:
    `.ufo/waves/round-54/evidence/control-c1-no-line.txt` — every row held, quoted and voted, `line` blank — reads
    `C1=unmet scope=31 rows=31 matched=31 status_ok=31 line_ok=0 quote_ok=31 … voted=31 dissent=0 … failed=line`,
    `exit=1`. The arm separates from the vote arm at the data commit:
    `.ufo/waves/round-54/evidence/c1-at-data.txt` reads `line_ok=31 quote_ok=31 … voted=0 … failed=votes`, `exit=1`.
    Not covered: the line proves place, not meaning — the disposition and its votes carry meaning, and the counter
    derives the line from the same committed copy the ledger author pinned, so a moved quote with unchanged
    semantics and an unchanged quote with changed semantics read the same; a quote occurring twice in the copy
    passes on either line; the no-line control is the L1's own fixture in its own clone, not an independent
    construction; a line at v7.3 says nothing about prose anchors that still spell v7.2 positions.

151. **A death with no OOM record is not called unexplained until the memory-failure counters are read.** Lesson:
    C2 this round (`knowledge/memory-failure-kills-r54.md`, `## Claim`): `mm/memory-failure.c` signals SIGBUS —
    forced `BUS_MCEERR_AR` for the task that consumed the page, ordinary `BUS_MCEERR_AO` for the other mappers — or
    SIGKILL when the unmap failed, raises no `oom_kill` count in `memory.events`, prints no `Out of memory` line and
    emits no `oom:mark_victim` event, so OOM evidence alone cannot exclude a kernel kill. Rationale: "unexplained"
    is a claim that the evidence was looked for and not found; the second evidence source is two reads away and the
    word is used before them. Check: a kill/death reading that reports no cause names the values it read of
    `/sys/devices/system/node/node*/memory_failure/total` and `HardwareCorrupted` in `/proc/meminfo` (SKILL
    `## Round54`, first decision-table row: `not yet explained … next read` those two, never `unexplained` before
    them); a non-zero counter sends the reader to the `Memory failure:` lines for attribution, never to a tally
    (QUALITY 15). Shown able to fail: the round-54 sweep at `39dcf4d7` (`evidence/sweeps.txt`) finds no mori tool,
    SKILL row or PROVINCE line naming either surface — `git grep -ilE
    "memory.failure|hwpoison|HardwareCorrupted|BUS_MCEERR"` over `corpus/knowledge SKILL.md PROVINCE.md tools`
    returns only a quote in `knowledge/kernel-v7.3-recheck-r53.md` — so every kill reading the lane held before this
    round fails the check; the same receipt records the host reads `node0/memory_failure/total:0`,
    `HardwareCorrupted: 0 kB`, `memory_failure_recovery: 1`, `memory_failure_early_kill: 0`, and
    `panic_on_unrecoverable_memory_failure` absent on 7.2.11 (re-read 2026-10-27: `node0` is the only node, all five
    per-node files present, `/proc/meminfo:40` `HardwareCorrupted:     0 kB`). Not covered: no tool enforces it, so
    compliance is a reviewer's reading, not a counter arm; the counters are cumulative since boot and split by
    outcome (`ignored failed delayed recovered total`), so a zero does not prove no error was detected on another
    node or before the last boot; corrected errors (EDAC) are not counted by these surfaces; nothing here was
    observed firing — mori never injects poison and never writes a memory-failure sysctl.
```

## Verification (every arm above, command → reading → exit)

| # | command | reading | exit |
|---|---|---|---|
| 148 fail | `python3 .ufo/waves/round-54/checks/receipt-stage.py 39dcf4d7e410d362781a47e8365ca23b5c807598` | 5 `FLAG line …` + `RECEIPT_STAGE rev=39dcf4d7 cited_intermediate=5 flagged=5`; body `diff` against `evidence/receipt-stage-before.txt` → identical | 1 |
| 148 pass | same script at a scratch-clone rev (`08f434e61e9f34b0c2744e862e7f8c393b26b081`) = `78295c76` + the working-tree `SCORECARD.md` corrections | `RECEIPT_STAGE rev=08f434e6 cited_intermediate=5 flagged=0` | 0 |
| 149 fail | `git ls-tree --name-only 39dcf4d7` | 22 entries, including `0 MANPAGE.md base.c main.c meminfo.c oom_kill.c sd-main.c user@.service.in` | 0 |
| 149 pass | `git ls-tree --name-only 1116c092` and `… 78295c76` | 15 entries each, none of the eight | 0 |
| 149 bytes | `git show 78295c76:.ufo/waves/round-28/misroot-lane-root/<name>` / `…round-38…/0` → `sha256sum`, diffed against the receipt hashes | 8/8 identical string sets | 0 |
| 150 fail | `cat .ufo/waves/round-54/evidence/control-c1-no-line.txt` (tracked at `78295c76`) | `line_ok=0 quote_ok=31 … voted=31 dissent=0 … failed=line` | receipt `exit=1` |
| 150 split | `cat .ufo/waves/round-54/evidence/c1-at-data.txt` | `line_ok=31 quote_ok=31 … voted=0 … failed=votes` | receipt `exit=1` |
| 151 fail | `cat .ufo/waves/round-54/evidence/sweeps.txt` | `git grep` hit only `kernel-v7.3-recheck-r53.md`; host: node0 counters 0, `HardwareCorrupted: 0 kB`, recovery 1, early kill 0, v7.3 panic sysctl absent | recorded in receipt |
| 151 surface | `ls -d /sys/devices/system/node/node*`; `ls /sys/devices/system/node/node0/memory_failure/`; `grep -n HardwareCorrupted /proc/meminfo` | `node0` only; `delayed failed ignored recovered total`; `40:HardwareCorrupted:     0 kB` | 0 |

Read-only throughout: `git log/show/cat-file/ls-tree/ls-files/status/diff`, `git clone --shared` from the lane
into scratch, `sha256sum`, `grep`, `diff`, plain reads of `/sys` and `/proc`. No git/jj mutation in the lane or the
fleet root; the single commit made (the 148-pass fixture) is inside
`/fast/scratch/hyaku/mori-r54/Mo54ScribeQuality/fixture`, whose `rev-parse --show-toplevel` printed that path before
the commit.

## Divergences from the pre-existing working-tree rows 148–151

1. Both pre-existing rows 148 and 149 cite `lessons/round-54.md#M1` / `#M2`; that file does not exist at `78295c76`
   or in the working tree. My draft cites the contract's routed-defect text (tracked at `78295c76`) and leaves the
   lesson file to record the narrative. If the L1 lands `corpus/lessons/round-54.md` in the same integration commit,
   either citation is fine; until then the working-tree anchors are dangling.
2. Pre-existing 148 asserts "after this round's appended corrections it prints `flagged=0`" as a reading. At the lane
   tip the corrections are uncommitted and the script reads `git show <rev>:SCORECARD.md` only, so that arm cannot
   have been observed there. My draft states it as fixture evidence at rev `08f434e6` and says so.
3. Pre-existing 148's Check and Shown-able-to-fail paths (`checks/receipt-stage.py`, `evidence/receipt-stage-before.txt`)
   are untracked at `78295c76`: a reader at a revision cannot resolve either. The draft names the dependency in
   `Not covered`, and the L1 should commit both files with the rows.
4. Pre-existing 149 calls `1116c092` "the round-54 data commit"; the assignment and the C1/C2 receipts use
   `78295c76` as the data commit (`c1-at-data.txt`, `c2-at-data.txt`, both with `rev=78295c76…`), of which
   `1116c092` is an ancestor. Both roots are clean of the strays, so the fact holds; the label is imprecise. My draft
   names both and marks `78295c76` as the landed one.
5. Pre-existing 149 states the byte-exactness from the receipt alone. My draft adds the independent sha256 agreement
   of all eight blobs at `78295c76`.
6. Pre-existing 151's failure arm is an inference from absence ("so any earlier 'no cause' reading fails the check").
   My draft keeps the sweep reading and states it as the check's only current failure instance, with "no tool
   enforces it" in `Not covered`.
7. Pre-existing 150 matches the receipts exactly; my draft adds the separability reading (`line_ok=31` with
   `voted=0` at the data commit) and the shared-author limit.
8. None of the four pre-existing rows carries a `Rationale` paragraph; rows 145–147 do. My draft adds one per row.

## Named limits of this seat's work

- This is a drafting seat, not an independent judge: rows 148/149/150 rest on the L1's frozen scripts and receipts
  (I re-ran 148's failure arm and read the others). The 148 pass arm was measured in a clone of the lane, not in the
  lane; the clone rev `08f434e6` exists only in scratch.
- I did not verify the C1/C2 counters' own correctness; the four criteria are about citation discipline and the two
  arms the counters expose, and a counter weakness would be a routed item for round 55, not an amendment here.
- I read no C1 RECHECK vote or C2 ENTAILMENT vote; whether the wave settles is outside this seat.
- I could not verify that the pre-existing working-tree rows were not themselves mirrored from a prior seat attempt;
  their mtime (`01:41:20`, before the first w1 report at `01:42`) suggests the L1's own drafting pass.

## Out of scope (untouched)

Product code, `SKILL.md`, `SHONEN.md`, `SCORECARD.md`, `LOG.md`, `PROVINCE.md`, `corpus/`, `tools/`,
`considerthese/`, every other file under `.ufo/waves/round-54/`, the counters and predicates, the controls, the
frozen sources, the host (read-only), and `/home/vgpnk/Projects/shokuknow`.

## Findings

- **HIGH — `.ufo/waves/round-54/checks/receipt-stage.py` and `evidence/receipt-stage-before.txt` are untracked at
  `78295c76`.** Working-tree QUALITY row 148 (line 1479) and the SCORECARD corrections cite them; at any committed
  revision those paths do not resolve. Fix is an integration-commit decision, not a counter change.
- **MED — `corpus/lessons/round-54.md` is absent** (`git cat-file -e 78295c76:corpus/lessons/round-54.md` fails;
  no round-54 file in `corpus/lessons/`). Working-tree QUALITY rows 148 (line 1479) and 149 (line 1492), and both
  appended SCORECARD correction paragraphs, cite `lessons/round-54.md` `M1`/`M2`.
- **MED — working-tree QUALITY row 148 states `flagged=0` as observed** while the corrections that produce it are
  uncommitted and the script reads only `git show <rev>:SCORECARD.md`; the observed lane reading is `flagged=5`,
  exit 1 (`evidence/receipt-stage-before.txt`, re-run and byte-identical).
- **LOW — working-tree QUALITY row 149 (line 1492) calls `1116c092` "the round-54 data commit"**; the data commit the
  C1/C2 receipts name is `78295c76` (of which `1116c092` is the ancestor). Root listings are clean at both.
- **LOW — no row of the four carries a `Rationale` paragraph**, which rows 145–147 do; the draft adds one per row.
- **LOW — working-tree QUALITY row 151 (line 1511) has no executable arm**; the draft keeps "no tool enforces it" in
  `Not covered` and states the sweep reading as the check's only failure instance.
- **INFO — the four pre-existing working-tree rows cover the same four criteria as this draft**, so the L1 should
  integrate one version (draft, or those rows with divergences 1–3 applied) rather than appending a second set.
