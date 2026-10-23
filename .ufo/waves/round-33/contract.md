# mori round 33 — claim contract (attempt 1, L1 MoriR33)

Entering tip `7d382043016e8854e3be2ee523a095b409c3d8a1` (round 32 closed `rejected-honest-stop`, MANIFEST rounds[498],
`corpus/lessons/round-32-verifier-spotcheck.md`). Written before any round-33 entry, source row or seat output.
Targets, not results. A declared claim is never withdrawn, narrowed, re-scaled or amended after data; a miss is
reported as a miss. The predicate below is the same sentence here, in the counter's docstring and in the receipt label
(`C1=met` / `C1=unmet`). Parity level, stated once (round-32 M3): the sentence extracted from each file is compared
after collapsing whitespace runs to one space, `diff <(tr -s ' \n' ' ' < A) <(tr -s ' \n' ' ' < B)`.

## Why this claim

- Lowest-scoring active axes: depth, freshness, calibration (5 each, `SCORECARD.md:12-14`). C1 works depth.
- Anti-loop: round 31 worked depth and operability on FR5 (watchdog identity), round 32 freshness on the source rows.
  C1 works a different frontier area: FR6, the instantaneous disk write-rate (`corpus/README.md:340`,
  `PROVINCE.md`), the resource-runway part of the lane's axes.
- Surface it changes: `corpus/knowledge/` and `SKILL.md` gain a sourced decision table on reading `/proc/diskstats`
  (and the per-device `stat` file) as a write rate. At the entering tip the lane has the census's since-boot average
  only (`corpus/knowledge/surfaces-r7.md:122-129`, `observability-surfaces-r2.md:271`) and one SOURCES row on the
  field list (S033, a mutable docs.kernel.org page); no entry states the sector unit, completion-time accounting,
  counter wrap and reset, the partition/whole-disk and stacked-device double count, or the version-dependent field
  count. The command that shows it unmoved: `count-c1.py 7d382043` → `entry=absent`, `C1=unmet`.
- Sourced claim: C1 rests on new SOURCES rows S180 or higher opened this round.

## C1 — depth (5): how to turn /proc/diskstats into a disk write rate (FR6)

Predicate P-C1: C1=met iff at <lane-rev> the entry corpus/knowledge/disk-write-rate-r33.md carries source:,
verified-at: and recheck: lines, holds no HTML comment, and has exactly one table outside any code fence whose header
holds the cells observation, reading, verdict and sources, with at least 10 pairwise-distinct data rows, each with a
reading cell of at least 8 words and naming at least one S### that is a corpus/SOURCES.md row; at least 8 rows cite an
id S180 or higher and at least 5 such ids are cited; every such id has exactly one corpus/SOURCES.md row with status
mined, a URL that no corpus/SOURCES.md line at the entering tip 7d382043 carries and that no other new id carries,
exactly one admit Gate row in corpus/lessons/round-33.md with that https URL, a 64-hex sha256 distinct from every other
new id's and 1-4 quotes of 3-25 words each behind a `file:L` or `file:L-M` locator, and a committed copy
corpus/evidence/sources-r33/S###.src whose sha256 equals the Gate sha256 and which contains every quote; the URL
fetched at measurement time hashes to the same sha256; every row citing a new id shares at least 2 distinct words of 4
or more letters with the Gate quotes of the new ids it cites; the committed judge dispatch
.ufo/waves/round-33/judge/dispatch.json and the committed judge receipt .ufo/waves/round-33/judge/JudgeC1Rows.md each
contain the judge rule R-J, the receipt carries a `judged-sha256:` line equal to the sha256 of the entry at
<lane-rev>, and it names every data row once as `row N: supported` or `row N: unsupported`, each supported row
followed on the same line by `span: "<text>"` of at least 6 words that is located in the committed copy of a new id
that row cites; at least 10 rows are supported, of which at least 8 cite a new id; and SKILL.md has at least 4
distinct lines of at least 12 words naming the word Round33 and corpus/knowledge/disk-write-rate-r33.md.

Judge rule R-J (frozen; the judge's dispatch and receipt each quote it word for word; a seat's own reading never
counts):

> A row is supported only when the quotes located in the committed copies of the sources it cites state every fact its
> observation and reading cells assert, and its verdict cell follows from that reading without any further fact; a row
> any part of which is not so stated is unsupported, including a row the judge would accept only with a caveat or
> through a source the row does not cite.

Counting command (exit 0 met, 1 unmet, 2 bad revision or usage):

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-33/count-c1.py <lane-rev>
```

Gate quote syntax the counter reads: `` `file:L-M` (N words): "quote" `` inside the Gate row, where `\"`, `\|` and
`\\` stand for `"`, `|` and `\`; matching collapses whitespace runs and nothing else, so copies should be plain text
(tag-pinned raw files, `.patch` commit views). One URL per new id; the URL must be byte-stable so the measurement-time
fetch hashes to the committed copy.

Declared before → after: `count-c1.py 7d382043` → `entry=absent`, `C1=unmet`, exit 1 → at the landed tip
`C1=met`, exit 0.

Controls (adversarial control wave C0, fresh critic and mutation-tester seats, before any data seat; receipts committed
at `.ufo/waves/round-33/evidence/c1-controls.txt`): do-nothing (the entering tip), junk rows, all-false judge,
no-reader judge (no spans or spans not in a cited copy), a receipt without R-J or with a loosened rule, a stale
`judged-sha256`, fabricated sources (consistent Gate/SOURCES/copy whose bytes are not upstream), sources already
registered at the entering tip, and a shortcut keyed on ids or labels. Each must print `C1=unmet`. A control that
meets the counter means the counter or target is wrong: the claim is re-designed before data or declared exploratory.

Uncounted residual (named, not hidden): the counter cannot tell an honest judge receipt from a fabricated one with the
same shape; receipt integrity rests on the committed dispatch, the judge seat's transcript and the closure's own
re-judgement.

Score policy: depth stays 5 unless an admitted closure states the move.

## Repairs routed by the round-32 closure (not claims; each lands with a LOG entry)

Rule R-R for the repair judge (frozen; quoted word for word in the repair judge's dispatch and receipt). It restates
the round-32 frozen verdict definition, contract `.ufo/waves/round-32/contract.md:25`: "`current` (the live page still
supports the teaches cell)", and applies it per clause:

> A teaches-cell clause is supported only when a quote located in the committed copy of a page that the row's own
> source cell names states it; a row is current under the round-32 definition only when its population page alone
> supports every clause of its teaches cell; a clause the judge would accept only with a caveat, through absence of
> contradiction, or through a page the row's source cell does not name is unsupported.

1. Five unsupported `current` rows (S058, S117, S128, S149, S137): an append-only correction names each unsupported
   clause and re-checks it on the row's own other source URLs, with committed copies under
   `corpus/evidence/recheck-r33/`; round 32's C1 stays a miss.
2. Judge rule drift: the lesson's "`JudgeRecheck` finding 1" citation is corrected append-only; a QUALITY criterion
   requires the frozen rule word for word in every judge dispatch and receipt (shown able to fail on round 32's
   receipt); R-J and R-R above apply it this round.
3. Six critic-flagged rows (S041, S044, S051, S062, S064, S069): each lane-application clause is declared as lane
   doctrine in the cell or sourced; the S062 and S069 judge-reason misstatements are recorded.
4. Cut quotes S128 Q3 and S149 Q2: re-quoted as whole sentences from the committed round-32 copies.
5. Unchecked second URLs of the 34 population rows: named and counted by a committed script.
6. Round-30 detector false positives/negatives and the FR5 census probe (`WATCHDOG_ABSENT`), carried three times:
   acted on or retired explicitly with a reason.
