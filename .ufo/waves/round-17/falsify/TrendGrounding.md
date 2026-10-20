# TrendGrounding — round-17 wave2 falsification

Seat: `MoriR17.TrendGrounding-4` (leaf; no subagent dispatch). Date: 2026-10-20.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. No production file edited. No VCS mutation.
No selftest, build, linter, journalctl, or pacman transaction. No tool installed
(pacman transactions are paused host-wide; this attack is static reads).

Axes named (LEARNING trends, not the C1/C2/C3 scores): **expansion**, **quality**, **discernment**.
Attacked scope: whether those three verdicts are supported by (1) new entries citing mined
sources and FR14, (2) stale clauses marked, (3) outside r16 findings becoming lesson-backed
Q43–Q48, (4) author seats excluded from independent closure. C1/C2/C3 measurement receipts
were not re-counted.

## Strongest finding

The four-part slogan does not support `improved` / `improved` / `improved`.
Round 17 never wrote the three required verdict cells, and the lesson's fleet-report
pointer does not resolve. Treating Q43–Q48 as one outside-r16 discernment block would
**harm discernment** by counting author-dispatched seats as outside agreement.

## Evidence

### Verdict cells are absent; the cited report path does not resolve

`LEARNING.md:26–35` requires one of `improved` / `harmed` / `unchanged` /
`unprovable-but-better` for each trend, every round.

Round 16 recorded them. `corpus/lessons/round-16.md:246–249`: expansion improved,
quality improved, discernment unchanged. `LOG.md:1112–1113` and the round-16 SCORECARD
section repeat that split.

Round 17 does not. `SCORECARD.md` ends at `:1062`. The round-17 section
(`:1002–1062`) records coverage/operability/calibration `improved` with scores held,
and says outside closure is not self-certified (`:1061–1062`). It has no expansion,
quality, or discernment cell. `LOG.md:1118–1182` likewise has none.
`corpus/lessons/round-17.md:3–4` cites fleet report
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/mori.md`.
Directory listing of `.ufo/reports/round-17/` shows 13 sibling reports
(`kagi.md` through `tsukuroi.md`) and no `mori.md`. Sibling reports in that
directory do carry the three trend bullets (for example `tabi.md:90–97`,
`tameshi.md:81–83`). Mori's do not exist to read. QUALITY #9 (path must resolve)
is unmet for that evidence line.

`LOG.md:1156–1157` says the fleet report is where citable hashes follow. The
support facts in the lesson are therefore unbound to a trend verdict.

### Expansion: mined citations and FR14 do not meet

`LEARNING.md:33`: expansion is `improved` when there are net new admitted
`knowledge/` entries on ground the coverage map did not hold, each citing its
coverage-map row, with `source:` citing a mined `SOURCES.md` row.

Two new entries:

| Entry | `source:` mined rows | Names FR14 | Coverage-map ground |
|---|---|---|---|
| `corpus/knowledge/seat-terminal-status-r17.md:1,9` | S041, S043 (mined, `SOURCES.md:47,49`, used-by this note) | body line 9 only; `source:` does not | FR14 was frontier (`PROVINCE.md:57`, `corpus/README.md:345`) |
| `corpus/knowledge/jj-branch-anchor-r17.md:1` | S044–S047 (mined, `SOURCES.md:50–53`) | no | Lane silence already Core (`PROVINCE.md:28`) and already mapped (`corpus/README.md:27`, `lane-silence-r2.md`) |

FR14's registered first evidence is still `corpus/SOURCES.md:28–32` (`PROVINCE.md:57`,
`corpus/README.md:345`). Those lines are S023–S027, every one `queued`, used-by `—`
(`SOURCES.md:28–32`). The new entry does not cite them. Its mined rows are HTTP 429
and Z.AI business codes. The coverage-map additions table
(`corpus/README.md:355`) points FR14 at the knowledge note and does not say the
first-evidence rows remain queued. Mined-source citations and the FR14 row's
evidence do not intersect.

S047 is mined with used-by `jj-branch-anchor-r17.md` (`SOURCES.md:53`; lesson
`:56–60`). The lesson's non-decorative pair is S043 and S046 only (`:59–60`).
The knowledge note's body never states symbolic-ref `-q`, silent nonzero, or
status 1 versus 128. S047's located quote (`corpus/lessons/round-17.md:53`) is
header-only. That is a mined used-by cell without a claim in the entry.

`jj-branch-anchor-r17.md` is a deepening of held lane-silence ground. Under
`LEARNING.md:33` it is not an expansion entry. `SCORECARD.md:1053–1054` admits
two capabilities (terminal-at-scan, misroot witness) and does not admit the
branch-anchor note as a capability row. The misroot capability has no
`knowledge/` entry.

### Quality: some stale clauses are appended; the index cell Q46 names is not

Marked, append-only, historical text left in place:

- `PROVINCE.md:25` still says `(round-16 build; verification pending)`.
  `:98–102` supersedes that phrase by the r16 spotcheck `:9–17`, dated 2026-10-20.
- `corpus/knowledge/journal-cursor-window-r16.md:2` still says host systemd
  version was not verified. `:138–149` supersedes that sentence for the round-16
  observation time and cites 261.2-1 as historical.

Unmarked active index / present tense:

- `corpus/README.md:41`, the coverage-map evidence cell, still reads
  `host systemd 261.2-1` with no historical label in the cell.
  `.ufo/waves/round-17/build/ProvinceFrontier.md:16–19` named this cell as the
  third stale site and required an appended note, not a rewrite.
  The landed sweep (`corpus/README.md:361–364`) says "the r16 host-version
  statement is historical261.2-1" and cites the knowledge note. It does not name
  `README.md:41`.
- `corpus/lessons/round-16.md:114–115` and `:153` still say the host `journalctl`
  **is** 261.2-1, present tense. No round-17 append exists in that file
  (file ends at the round-16 verdicts, `:246–251`). Q46
  (`corpus/QUALITY.md:127–130`) requires a dated appended note and a sweep of
  active index prose. Spotcheck `:223` forbids rewriting history; it does not
  forbid an append. The append is missing at these two loci.

Mis-cited supersession token:

- Knowledge append `:144–146` says today's package log records `261.2-1→262-1`
  inside the `09:16` full-upgrade, citing
  `.ufo/waves/round-17/build/{PacmanTxnToday,ProvinceNotesDraft}.md`.
- `PacmanTxnToday.md:15–16` locates the `-Syu` at **09:15:30** (`pacman.log:2462`).
  `:60` records ``systemd-libs`/`systemd` 261.2 → 262`` (`:2487`, `:2531`).
  That file does not contain the token `262-1`. The `09:16:28` time in that
  file (`:46`) is the btrbk install inside the same transaction.
- The `261.2-1 -> 262-1` spelling and `09:16:27`/`09:16:28` systemd times are
  in `ProvinceFrontier.md:30` and `ProvinceNotesDraft.md:64–66`, as those seats'
  log quotes. Bundling `PacmanTxnToday` as a carrier of `262-1` / "09:16
  full-upgrade" does not match that receipt.

`LEARNING.md:34`: quality is `harmed` when an entry is found stale and left
unmarked. `README.md:41` and `round-16.md:114,153` are that case. The knowledge
header is marked, with a receipt mismatch in the mark.

### Discernment: Q43–Q46 are the outside r16 set; Q47 and Q48 are not

`LEARNING.md:35,40–48`: discernment `improved` when a non-author spot-check of
**this round's** admits and rejects agrees, or a disagreement becomes a lesson
that adds a grounded criterion. A subagent the lane dispatched is still the lane.
`harmed` when a criterion has no lesson, or a disagreement is left unlearned.

| Criterion | Lesson | Spotcheck lines | Who captured it |
|---|---|---|---|
| Q43 `QUALITY.md:114–118` | `round-17.md#M1` | `:202–209` item 1 | outside r16 verifier |
| Q44 `:119–122` | `#M3` | `:216–219` item 3 | outside r16 verifier |
| Q45 `:123–126` | `#M2` | `:210–215` item 2 | outside r16 verifier |
| Q46 `:127–130` | `#M4` | `:220–223` item 4 | outside r16 verifier |
| Q47 `:131–135` | `#M6` only | none | `JjAuditMori.md` F3/F4 (auditor `JjAuditMori-2`, hyaku jj-w1, `:3`) plus author build `{CriticC2,CriticHarm,CensusConsumers}.md` (`round-17.md:71`) |
| Q48 `:136–140` | `#M7` only | none | author build `{CriticC1,TranscriptShapes,SeatNaming,CriticFrontier}.md` (`round-17.md:72`) |

Q43–Q48 each cite a lesson row, so none is a bare criterion (`LEARNING.md:35`
harm clause on "no lesson" does not fire). The outside-r16 claim stops at Q46.

Q43's spotcheck range (`:202–209`) prescribes no pathspec and
`git status --porcelain`. It does not prescribe filename-and-content attribution.
That clause is the lane's M1 elaboration. Lesson M1 and `corpus/README.md:357`
say filename **or** content. Q43 says filename **as well as** content.
`tools/mori-misroot-sweep.py:21–24` says the planted witness is found **by path
alone** because content names neither lane nor round. `:290–305` requires both
lane and round, each from path or content. The counting witness does not require
a content hit. The spotcheck citation range does not contain the content rule.

Round-17 gate (`corpus/lessons/round-17.md:37–38`): "Independent outside
admit/reject spotcheck remains required; author-dispatched seats are not
non-author closure." `SCORECARD.md:1061–1062` repeats that this wave is not
that closure. No agree/disagree sample of this round's admits and rejects is
in the lesson. Clause (4) of the slogan holds **in that sentence**. It is
contradicted if Q48 is used as the outside half of discernment.

Author-seat exclusion is also stated at `corpus/knowledge/seat-terminal-status-r17.md:56`
and `LOG.md:1157` (measurements not inferred from seat selftests). M10
(`round-17.md:74`) records that L1's selftest authorization conflicted with
QUALITY #39 and that seat selftests are not admission evidence. That disclosure
is not a closure.

## Contradictions (not smoothed)

1. `LEARNING.md:42–45` requires a non-author admit-and-reject sample of **this**
   round before discernment can move. Round-13/16 practice also counted a
   **prior** outside disagreement, once it became a criterion, as discernment
   improved, while excluding same-round seats (`LOG.md:752`; `round-16.md:246–249`).
   Round 17 has the prior-disagreement half only for Q43–Q46, and has no this-round
   sample. Either reading rejects "Q43–Q48 ⇒ discernment improved".
2. Lesson `:11–12` says the C3 detector is filename-**or**-content. Q43 says
   filename **as well as** content. The planted witness is path-alone
   (`mori-misroot-sweep.py:21–24`).
3. Lesson `:3–4` cites `mori.md` as evidence. That file is absent. Lesson
   `:37–38` says outside closure is still required. Those two sentences cannot
   both be read as a completed discernment verdict.
4. FR14 first evidence remains queued S023–S027. The admitted FR14 entry cites
   mined S041/S043. Both statements are in the tree; they are not one citation.

## Affected axes

- **Discernment:** the slogan's Q43–Q48 bundle would record a false `improved`.
  That harms discernment under `LEARNING.md:40–48`.
- **Expansion:** counting `jj-branch-anchor-r17.md`, header-only S047, or queued
  S023–S027 as the mined FR14 citation would record a false `improved`.
- **Quality:** `README.md:41` and `round-16.md:114,153` are stale present-tense
  host-version claims left unmarked. Q46 is not met on the index.
- **Coverage, operability, calibration (C1/C2/C3):** not retouched. Score holds
  in `SCORECARD.md:1038–1041` stay outside this move.

## Proposed move (one)

Do not file expansion/quality/discernment from the four-part slogan.

Write three cells, append-only, in the lesson and SCORECARD, and point
`corpus/lessons/round-17.md:3–4` at a report that exists:

- **expansion: `unprovable-but-better`.** One uncovered-ground candidate,
  `seat-terminal-status-r17.md`, cites mined S041/S043 and names FR14 in the body.
  `source:` does not cite the coverage-map row, and that row's first evidence is
  still queued. `jj-branch-anchor-r17.md` stays a quality deepening of lane
  silence, not an expansion entry. S047 stays disclosed as header-only until the
  note states the symbolic-ref status distinction.
- **quality: `unchanged` until the index sweep lands.** Add a dated append that
  names `corpus/README.md:41` and `corpus/lessons/round-16.md:114–115,153` as
  round-16 observation-time text, without rewriting those sentences.
  Retarget the knowledge-note `262-1` / `09:16:28` token to
  `ProvinceNotesDraft.md:64–66` (or `ProvinceFrontier.md:30`). Stop citing
  `PacmanTxnToday.md` for a spelling it does not contain; keep it for the
  `09:15:30` `-Syu` at `:2462`.
- **discernment: `unchanged`.** Credit Q43–Q46 as the outside r16 disagreements
  already lesson-backed. Keep Q47 on the hyaku JjAudit plus author critics.
  Keep Q48 on author seats. Do not treat either as the r16 spotcheck or as this
  round's non-author admit/reject sample. The lesson sentence that author seats
  are not independent closure stays.

No C1/C2/C3 tool, fixture, or score change is part of this move.

## Harm if the slogan is admitted as written

- Discernment is harmed: Q48's author seats (`CriticC1`, `TranscriptShapes`,
  `SeatNaming`, `CriticFrontier`) become outside agreement. `LEARNING.md:45`
  says a dispatched subagent is still the lane.
- Expansion is over-credited: held lane-silence and queued FR14 first-evidence
  rows are counted as new mined frontier ground.
- Quality stays falsely `improved` while `README.md:41` and `round-16.md:114,153`
  still state 261.2-1 as the live host, and the supersession note mis-attributes
  `262-1` to `PacmanTxnToday.md`.

## Risks

- An append that rewrites `round-16.md:114` or `:153` in place would violate
  spotcheck `:223` and Q46's "never rewritten into a claim about the current host".
  The move is an append that names those lines.
- `unprovable-but-better` for expansion still needs a named non-author under
  `LEARNING.md:46–48`. Until that reviewer exists, leaving the cell unwritten is
  the accurate state; inventing `improved` is the harm above.
- ProvinceFrontier's live `systemctl` / `pacman -Q` observations (`:28–29`) are
  that seat's host queries. This seat did not repeat them. The `262-1` spelling
  is used only as text inside those build reports.

## Verification

Static reads only, 2026-10-20. No selftest, no census, no seat-terminal scan,
no misroot probe, no journalctl, no pacman, no tool install. Fleet-report absence
is the glob of `/home/vgpnk/Projects/shokunin/.ufo/reports/round-17/` (13 files,
no `mori.md`). Re-check after an integrator append: the three verdict words exist
once each in the lesson and SCORECARD; `README.md:41` and `round-16.md:114,153`
are named by a dated note; `seat-terminal-status-r17.md` `source:` either cites
the FR14 coverage-map row or the expansion cell stays `unprovable-but-better`;
Q48's captured-by list is still the four author build reports.
