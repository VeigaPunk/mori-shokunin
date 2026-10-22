# Round 28, wave 1 — CriticC1Design: attack on claim C1 (freshness) before data

Seat: MoriR28.CriticC1Design (critic, leaf). Measured 2026-10-22 between 17:58:45Z and about 18:05Z, against
entering tip `6ebd518f` and declaration commit `079a47c6` (committed 2026-10-22T14:56:06-03:00). All lane reads are
read-only git object reads. The only lane write is this report. The sandbox is under
`/fast/scratch/hyaku/mori-r28/CriticC1Design/` (a `git clone --no-hardlinks` detached at `6ebd518f`; one sandbox
commit there, never pushed). Tools installed or updated: none.

## Verdict in one paragraph

C1 as declared can be met by bookkeeping alone. In the sandbox, eight rows that copy the old defective wording behind
a `supersedes S0NN — ` prefix, with `used-by` set to `—`, plus the three restores, make the committed counter print
`C1=met` and exit 0 (finding 1). Restoring S096, S097 and S101 leaves every live reader citing the restored rows,
which now carry the wrong wording again. The contract's own scope sentence ("C1 touches `corpus/SOURCES.md` only")
rules out the reader sweep that would fix this. The round-27 precedent (S143, S144) already shows the failure: their
`used-by` cells name files that cite neither id (finding 2). The S097 superseding row cannot honestly be `mined`
(finding 3). The S140 carried finding lives in a knowledge file, not in the S140 row (finding 4). As written, the move
is the same one the round-27 judge rated "freshness unchanged" (finding 5). Each defect can be fixed before data.

## Findings, ranked

### 1. HIGH — the counter is satisfiable by bookkeeping: no source opened, no defect fixed, `C1=met` (parts c, d)

Counterexample (sandbox): `falsify.py` restores S096, S097, S101 to their first-published cells (S096 and S097 from
`df4db54`, S101 from `90ed9b7`). It then appends S145–S152. Each new row is the superseded row's own cells with the id
changed, `teaches` prefixed `supersedes S0NN — ` and the old defective text kept, status `mined`, `used-by` `—`. The
committed counter was run unchanged except that `LANE` and the frozen check's `LANE` point at the sandbox:

```
$ bash count-c1-sandbox.sh HEAD
row_identity=rows=152 changed=0 removed=0 bad=0
superseding=8/8 ids=S096,S097,S101,S127,S128,S129,S131,S140
C1=met
exit=0
$ bash count-c1-sandbox.sh 6ebd518f      # control, equals evidence/c1-before.txt
row_identity=rows=144 changed=3 removed=0 bad=0
superseding=0/8 ids=none
C1=unmet
exit=1
```

The CORPUS census does not catch it either. On the sandbox it reports malformed=0, status-enum violations 0 and
missing used-by paths 0, because `—` is skipped.

Why: `count-c1.sh:36-43` checks only the cell count, an id above 144, the `supersedes (S[0-9]{3}) — ` prefix and
status in (`mined`, `verified`). The contract's other conditions (`contract.md:21-22`: "re-opened against the upstream
bytes in round 28 and recorded in the lesson `## Gate` with URL, access time and a located quote") are not counted.
The `opened` cell cannot tell the rounds apart, because rounds 24–28 are all dated 2026-10-22. The counter also
accepts `verified`, which is not a CORPUS status (`CORPUS.md` `status` enum: queued, mined, rejected); the census
would flag such a row.

Impacted axes: freshness (false move), calibration (the after-value overstates the work).

Smallest correction: a dated amendment before data that adds four checks to `count-c1.sh`, all on committed bytes
at `<rev>`:

```
for each new row S145..S152 (map fixed by the contract):
  a. teaches after the "supersedes S0NN — " prefix != the superseded row's teaches at <rev>
  b. status == mined with used-by non-empty and not "—", or (S146 only) status == rejected   (see finding 3)
  c. every used-by path exists at <rev> and contains the new id as a word (git grep -w)
  d. the round-28 lesson "## Gate" has one line per new id with an https URL, an access time later than
     079a47c6's committer time (2026-10-22T17:56:06Z), a 64-hex sha256, and a quoted span of at most 25 words with a line number
print gate=<k>/8 readers_ok=<k>/8; C1=met needs 8/8 on both
```

Drop `verified` from the accepted statuses. The quote can only be checked against the bytes by a non-author
re-opening a sample (CORPUS Rules 1); name that sample in the amendment.

### 2. HIGH — restoring three rows points every live reader back at wrong wording; contract scope forbids the sweep (part b)

What the restore brings back (cell diff, first-published compared with `6ebd518f`):
- S096 `teaches`: first "…so an absent irq file is a build-configuration fact and never a zero reading". This is the
  overclaim that wave-2 ReopenS094S097 F1 refuted (`.ufo/waves/round-24/w2/ReopenS094S097.md:17`). The tip wording names
  three causes: no IRQ time accounting at build time, PSI disabled at boot, or a kernel older than 6.1.
- S097 `teaches` flip: first "(S001; kernel v7.2 Documentation/accounting/psi.rst lines 42-43 …)". This is the
  wrong-row flip of ReopenS094S097 F5 (`:43`): the bytes are S090's, now S143's. The first flip also lacks the
  "man-pages publishes a proc_pressure page" condition.
  The S097 `anchor` restore is harmless. The 17-character prefix `80c3fe2ae1062abf5` matches the live body:
  `curl https://man7.org/linux/man-pages/man5/proc_pressure.5.html` at 2026-10-22T18:01:02Z returned HTTP 404,
  196 bytes, sha256 `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`.
- S101 `teaches`: first "…the code clamps it, so docs and code disagree for values above 100". This is the overclaim
  corrected in `d3b7af2` ("S101 teaches cell no longer overclaims"); the tip reads "The page omits the maximum; it
  does not contradict it."

Live readers at `6ebd518f` (`git grep -n -E '\bS(096|097|101)\b' 6ebd518f -- . ':!.ufo'`). Each must cite the
superseding row:

| Superseded → new | File:line that must change | Depends on corrected wording? |
|---|---|---|
| S096 → S145 | `SKILL.md:619` "S096 (PSI_IRQ commit)" | cited as source of the decision table |
| S096 → S145 | `PROVINCE.md:257` "(S090–S096)" | range; also S090→S143, S093→S144 |
| S096 → S145 | `corpus/SOURCES.md:159` Paths "S090 → S091 → S095 → S096 → S092 → S093 → S094" | the study path leads to three restored rows |
| S096 → S145 | `corpus/knowledge/system-pressure-r24.md:1` (source header), `:30`, `:41`, `:61` (URL-to-row map), `:110`, `:177` | yes: F6 and F7 (`:112-122`) say an absent or failing irq read has more than one cause; restored S096 says build configuration only |
| S097 → S146 | `PROVINCE.md:258`; `corpus/knowledge/system-pressure-r24.md:1`, `:224` (U6) | yes: U6 names S090 as the format authority; the restored flip names S001 |
| S101 → S147 | `corpus/knowledge/harness-job-capacity-r25.md:1`, `:47` | yes: `:51` "states a default and a floor but no maximum" matches the tip reading; the restored row says the docs contradict the code |

Leave these as history (append-only records): `LOG.md:1789`, `SCORECARD.md:1525`, `corpus/SOURCES.md:195` (round-24
search log), `corpus/lessons/round-24*.md`, `round-25*.md`, `round-27*.md`, and every `.ufo/waves/` file.

The same reader rule applies to the five rows that are superseded without being restored. Their defects stay in the
first-published cells, so readers must move off them as well:
- S127 → S148: `SKILL.md:722`, `PROVINCE.md:377`, `corpus/README.md:36`, `corpus/knowledge/oom-victim-selection-r27.md:1,37,55,63,72,84,89`.
  Line 203 is tsukuroi's S127, not mori's; leave it.
- S128 → S149: `oom-victim-selection-r27.md:1,66`.
- S129 → S150: `SKILL.md:722`, `oom-victim-selection-r27.md:1,72,78`.
- S131 → S151: `oom-victim-selection-r27.md:1,48`.
- S140 → S152: `harness-job-capacity-r25.md:1,277,330`.

The precedent is already broken. Round 27 restored S090 and S093 and landed S143 and S144. At `6ebd518f`, both rows'
`used-by` cells name `corpus/knowledge/system-pressure-r24.md` and `corpus/lessons/round-24.md`, and S144 also names
`round-24-verifier-spotcheck.md`. `git show 6ebd518f:<path> | grep -c '\bS14[34]\b'` prints 0 for all six pairs. No
live file cites S143 or S144 (the only hits are `LOG.md:1868` and the round-27 lessons). The knowledge entry, SKILL
and PROVINCE still cite S090 and S093, so `mined` on S143 and S144 is false provenance. The contrast case S133 was
done right: `userspace-oom-killers-r26.md` cites it twice.

Contract conflict: `contract.md:13` "C1 touches `corpus/SOURCES.md` only". The sweep needs `SKILL.md`, `PROVINCE.md`,
`corpus/README.md` and three knowledge entries. As written, C1 can only land by leaving readers on the wrong rows.

Impacted axes: freshness and depth (a reader acting on SKILL.md's cited row gets the overclaim), calibration (false
`used-by`).

Smallest correction (dated amendment before data):
1. Replace `:13` with: "C1 touches `corpus/SOURCES.md` and repoints the live readers listed in the amendment; history
   files are untouched".
2. Repoint each line in the table and list above in the same commit as the new rows. Per QUALITY 77, rewrite the
   wording that depends on the old row; do not shadow it.
3. Change each old row's `used-by` in place so it names only the history lessons that still cite it, for example
   S096 → `corpus/lessons/round-24.md`. Log each change old → new in the round-28 lesson (CORPUS Rules 2).
4. Fix S143 and S144 the same way, since `PROVINCE.md:257`, `SOURCES.md:159` and the knowledge header are edited
   anyway.
5. Log the three restores themselves old → new in the lesson: a restore is an in-place change too.
6. Counter check: no file in `SKILL.md PROVINCE.md corpus/README.md corpus/knowledge/` cites any of the eight
   superseded ids or S090/S093 (`git grep -w` at `<rev>`).

### 3. HIGH — S097's superseding row cannot honestly be `mined`; the contract and counter force a false status or a miss (parts c, d)

S097 is `rejected` (tier C, a 404 page). The flip condition, "the man-pages project publishes a proc_pressure page",
does not hold: the re-fetch above is still a 404, byte-for-byte the same body. `contract.md:21` requires every new row
to have "status `mined`". `count-c1.sh:42` accepts only `mined` or `verified`. A truthful S146,
`supersedes S097 — REJECTED: …; flip: …` with status `rejected`, scores 7/8 and `C1=unmet`. A row that scores 8/8
calls a 404 page `mined`: that reverses the rejection with no new evidence.

Smallest correction: the amendment lets S146 carry status `rejected`, with teaches opening
`supersedes S097 — REJECTED:`. The counter accepts `rejected` for S146 only, as in finding 1b.

### 4. MEDIUM-HIGH — the S140 carried finding is not in the S140 row, so `superseding=8/8` can hold with it unfixed (part d)

Routed defect 4 says "the low finding in ReopenS140" (`round-27-verifier-spotcheck.md:150-151`). ReopenS140 has two:
- Low-1 is knowledge prose: `corpus/knowledge/harness-job-capacity-r25.md:330` and `:282`
  (`.ufo/waves/round-27/w2/ReopenS140.md:137-142`, with exact old → new text).
- Low-2 is a whitespace rendering note, "No change required" (`:144-145`).

No change to the S140 row fixes Low-1, so S152 counts while the finding stays unfixed by construction. The same is
partly true of S127: ReopenS127 F5 is a defect in S128's cell (`ReopenS127.md:154`), so it belongs to S149, not S148.

Smallest correction: apply ReopenS140 Low-1's old → new text in place at `harness-job-capacity-r25.md:330`, and its
`:282` head clause, with a dated correction block, as round 27 did for U1. The counter greps the new wording at
`<rev>`. Add a finding-to-row map to the lesson that lists every routed finding: S096 F1, S097 F5, S101 overclaim,
S127 F1–F5, S128 F1, S129 M2, S131 F1 (tree URL), F2, F3, F4, and S140 Low-1. Each entry gets its superseding row or
file:line, old wording, new wording and evidence. The counter checks that all 15 entries are present.

### 5. MEDIUM — as written, C1 is correctness hygiene, not freshness; the round-27 judge already ruled so (part a)

- AXES.md:14 defines freshness as "skill claims re-verified against live surfaces; stale items flagged or fixed", with
  signal "Each round LOG entry includes a re-verification result".
- The round-27 closure rated the identical move (S090, S093 and S124 restored with S133, S143 and S144) "freshness |
  unchanged | corrections to older entries are hygiene (routed defects), not a declared claim"
  (`round-27-verifier-spotcheck.md:105`), and booked it under the quality trend (`:131-133`). `contract.md:4-5`
  itself calls both claims "repairs routed by" that note.
- The eight defects are first-publication errors: overclaims, wrong pointers and a wrong URL. They are not drift; they
  were never true. Re-opening a pinned ref cannot detect drift, because it returns the same bytes and the same sha256.
  The pinned refs are the v7.2 tag, v262, v1.9.0 and commits `45c35e40`, `6962d5cd` and `52b1364b`.
- The live surfaces have moved, and that is what freshness should test:

| Surface | Row anchor | Live at access (UTC) | Host installed (`pacman -Q`) |
|---|---|---|---|
| Linux | v7.2 (S127, S128 code) | mainline 7.3 released 2026-10-18; stable 7.2.12 (`https://www.kernel.org/releases.json`, 18:01:03Z, sha256 `a789c77c…bf23`) | linux 7.2.11.arch1-1 |
| systemd | v262 (S129) | release v262.1 published 2026-10-16T21:57:14Z (GitHub releases/latest, 18:01:03Z, sha256 `9f6417c9…17cd`) | systemd 262-1 |
| man-pages | S097 says current 6.20; S128 says served from 6.19 | 6.20 not re-checked here | man-pages 6.19-1 |
| oh-my-pi | v18.12.6 (S101, S140) | latest release v18.12.6, published 2026-10-21T21:02:53Z (18:01:02Z, sha256 `15fc3625…b06b`) | not checked (seat bound: omp not run) |
| earlyoom | v1.9.0 (S131) | latest release v1.9.0 (18:01:03Z, sha256 `757a58a3…ea86`) | earlyoom 1.9.0-1 |

  Example of a real freshness result, measured here: S127's anchor holds at v7.3.
  `https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/fs/proc/base.c?h=v7.3` (18:01:29Z,
  98216 bytes, sha256 `fb419e9a64d617039d5e90d53f0d634a0a2d4d1d9b1e99698b04e9412df38d5c`) line 597 reads
  "points = (1000 + badness * 1000 / (long)totalpages) * 2 / 3;". That is the same as v7.2 (98196 bytes, sha256
  `cef1a2cf…15c6`). The `proc_oom_score` body, compared with line numbers stripped, is identical; the file differs
  elsewhere by 20 bytes.
  S129 also holds at v262.1: `raw.githubusercontent.com/systemd/systemd/v262.1/man/systemd-system.conf.xml`
  (18:01:23Z) has the same sha256 as v262 (`16135998…0b58`), and line 306 reads "…OOM adjustment value plus 100…".

Smallest correction: the amendment requires a recheck line for each superseding row in the lesson Gate. It names the
pinned ref, the newest upstream release or tag at access time, and the host's installed version (package query or
version line). It ends with `unchanged at <ref>` or `drifted: <old> → <new>`, and drift gets fixed or flagged. One
`LOG.md` line carries the result, `re-verified 8/8: <k> unchanged, <m> drifted`, which is the AXES signal. The counter
prints `rechecked=<k>/8`, and `C1=met` needs 8/8. Without this, report C1 as quality hygiene and expect
"freshness unchanged" [INFERENCE: from the `:105` precedent; the judge decides].

### 6. MEDIUM — QUALITY 77 against QUALITY 81: the restored rows are contradicted lines left standing (tradeoff for the judge)

QUALITY 77 (`corpus/QUALITY.md:349-355`) says a contradicted line left standing is a defect. QUALITY 81 (`:373-377`)
freezes the first-published cells. CORPUS v1 has no `superseded` status and no forward pointer: only `status`,
`recheck` and `used-by` may change, and the status enum has no slot for it. So a reader who lands on S096 by id
cannot find S145 except by grepping `supersedes S096`. The lane cannot fix this inside the frozen contract v1.

Smallest correction: the amendment states the reading "a superseded row is a history record once no live reader
cites it and its `used-by` names only history lessons". Finding 2 makes that reading true. Route the missing forward
pointer to the protocol owner as a contract-v2 item; that is not lane work.

### 7. LOW — "byte-equal" overstates what the check compares

`contract.md:19` says "restored byte-equal". `check-row-identity.py` (frozen blob in `df886be1`) compares cells
after `.strip()` (its `rows()`, `cells = [c.strip() …]`), so padding differences pass. Smallest correction: say
"cell-equal (whitespace-trimmed)" in the amendment, or compare the raw row line with the mutable cells masked.

## What would make `superseding=8/8` a real move (part c, summary)

It becomes a real move when all of the following hold at `<rev>`:
- Each new row differs in substance from its old row (finding 1a).
- Each new row is cited by the readers it names, and no live reader cites the old row (1c, 2).
- Each new row has a round-28 Gate line with a 64-hex sha256 of the bytes fetched and an access time after the
  declaration commit (1d).
- Each routed finding is mapped and fixed where it actually lives (4).
- Each row is rechecked against the live release, not only the pinned ref (5).
- S146 stays `rejected` (3).

## Part d answer

Yes. As committed, C1 can be met while all 15 routed findings remain: the sandbox proves this for the row cells.
Even with honest rows, S140 Low-1 is unfixed by construction (finding 4), and readers stay on the restored wrong
wording (finding 2).

## Checks not run

- I did not run the lane's own check against the lane tip. It ran only inside the sandbox, through a copy with
  `LANE` repointed.
- I did not re-fetch the round-27 Gate quotes for S127–S140.
- I did not check man-pages 6.20 upstream.
- I did not check the omp version installed on the host.

Sandbox and fetch artifacts: `/fast/scratch/hyaku/mori-r28/CriticC1Design/{falsify.py,count-c1-sandbox.sh,fetch/,lane/}`.
