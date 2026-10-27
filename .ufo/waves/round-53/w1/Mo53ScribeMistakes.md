# Mo53ScribeMistakes — round-53 lesson `## Mistakes` draft (M1–M3)

Seat: scribe, `mori-shokunin` round 53 wave `w1`. Reads at the frozen freeze commit (`f4da3fd400fa88a6db8ea544a4f7045c15d2410e`
contract), the data commit `2a4213bf8da72f7cd78189baa5bb9be825dca1df`, the entering tip
`20edafa59b38dac1ca358893f0259b1f436372d3` and lane HEAD `95cf78eef71979f9b740ef6bc3c5299b6beff86e` (read-only `git show`/
`git grep`/`git log`). Scratch `/fast/scratch/hyaku/mori-r53/Mo53ScribeMistakes/` (created, used, removed at the end of this
seat). No tool installed, no pacman transaction, no counter run, no network fetch except one 4247-byte cgit tag page. Wrote
only this file.

## What I checked (commands, exit codes, revisions)

| # | command (cwd, rev) | rc | output carried below |
|---|---|---|---|
| 1 | `sed -n '2746p' SCORECARD.md` (lane, 95cf78ee) | 0 | the round-52 C1 row: After cell `C1=met items=42 … locators=27`, citing `evidence/c1-at-landed.txt` |
| 2 | `grep -n 'C1=' .ufo/waves/round-52/evidence/c1-at-landed.txt` | 0 | `:45 C1=met items=43 … locators=28 … rev=e7e056b8…` |
| 3 | `grep -n 'C1=' .ufo/waves/round-52/evidence/c1-at-data.txt` | 0 | `:44 C1=met items=42 … locators=27 … rev=8524904a…` — the numbers the row actually carries |
| 4 | `python3 -I -B numdrift_probe.py` (scratch; `git -C <lane> show <rev>:SCORECARD.md`, reads only) | 0 | MISMATCH 0 for round-51's row, MISMATCH 2 for round-52's row (quoted below) |
| 5 | `sed -n '1,8p;44,48p' .ufo/reports/round-52/mori.md` (fleet repo) | 0 | `Report commit \`[FILL]\`.` at `:5`; a `| \`[FILL]\` | …` table row at `:46` |
| 6 | `git log --format=%H -- .ufo/reports/round-52/mori.md` (fleet repo) | 0 | `aacd7a83027cdee8e950a2c39d490feaed3be13c` |
| 7 | `grep -rl '\[FILL\]' .ufo/reports --include='mori.md'` (fleet repo) | 0 | 1 file of 42 (`round-52/mori.md`, 2 hits) |
| 8 | `grep -n 'recheck: on-release' corpus/knowledge/memavailable-estimate-r51.md corpus/knowledge/overcommit-commit-limit-r52.md` | 0 | `:9` in both |
| 9 | `curl -fsSL 'https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tag/?h=v7.3'` (scratch) | 0 | 4247 bytes; `tag name v7.3 (091b0638…)`, `tag date 2026-10-18 13:14:58 -1000`, `tagged object commit c03c1a1450…`, tag message `Linux 7.3` |
| 10 | `grep -n 'v7.3\|7.3.0'` over the round-52 wave seat and LOG (lane, 20edafa5) | 0 | `.ufo/waves/round-52/w1/Mo52ScribeGate.md:139-148,197,202`; `LOG.md:2054` |
| 11 | `git grep -c 'v7\.3|7\.3\.0' 20edafa5 -- corpus/knowledge corpus/SOURCES.md SKILL.md` (as recorded in `evidence/sweeps.txt:7-8`) | 1 (no match) | no recheck in the lane at the entering tip |
| 12 | `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` | 0 | `/fast/scratch/hyaku` 25 % used, 607.5 G free; no ENOSPC risk, no heavy run |

Read, not run: `.ufo/waves/round-53/evidence/c1-at-data.txt`, `control-c1-do-nothing.txt`, `sweeps.txt`,
`corpus/lessons/round-52.md` `## Mistakes`, `corpus/lessons/round-52-verifier-spotcheck.md` §Conformance defects and
§Routed defects, `corpus/QUALITY.md` 9/119/134/141/142, `.ufo/waves/round-53/count-c1.py` docstring and `:6`.

## Draft — the lesson `## Mistakes` section (fenced block; the L1 integrates)

```markdown
## Mistakes

- M1: number-drift — a claim row's tally was transcribed from the *earlier* receipt and then the cell was pointed at
  the *later* one. `SCORECARD.md:2746` (round-52 C1 row) After cell reads `C1=met items=42 … locators=27`, rc 0 —
  `evidence/c1-at-landed.txt`; the receipt at that path prints `C1=met items=43 … locators=28 …
  rev=e7e056b8a17e54516a3c17798221c30e9902c250` (`.ufo/waves/round-52/evidence/c1-at-landed.txt:45`), while 42/27 is
  verbatim the at-data receipt (`evidence/c1-at-data.txt:44`, `rev=8524904a…`) written before the row. Evidence:
  the two receipts and the row above; `corpus/lessons/round-52-verifier-spotcheck.md` D2 for attribution (the row was
  written at integration `2f245af7`, before `c1-at-landed.txt` existed). Captured-by: none — no instrument compares a
  claim-table row with the receipt its own cell names: `count-c1.py` reads no `SCORECARD.md` byte (grep for
  `SCORECARD` in both round-53 counters → 0 hits), QUALITY 141 scopes living pins to `corpus/QUALITY.md` and
  `corpus/README.md`, QUALITY 142 scopes pointers to `## Axes` and the SHONEN boxes, and the SCORECARD-reading tools
  (`tools/mori-routed-check.py`, `tools/mori-round41-calibration.py`, `tools/mori-census.sh`) read other cells. The
  non-author closure found it by reading. Fix (proposed, routed to round 54 — no frozen counter changes this round): a
  row-vs-citation arm that parses each After cell's `C1=…` span and the verdict line of the file the same cell names,
  and requires every `k=v` of the row to occur in that receipt with the same `v`. Shown able to fail by a seat probe
  over the two neighbouring rows: round-51's row (`SCORECARD.md:2716`, `kill_residue=0 relocated=met reloc_mismatch=0
  classified=ok selftest=pass=125,fail=0`) reads `MISMATCH 0` against `.ufo/waves/round-51/evidence/c1-at-landed.txt`,
  round-52's row reads `MISMATCH 2: {'items': ('42','43'), 'locators': ('27','28')}`. The appended correction line of
  routed defect 1 is not in the tree at the data commit `2a4213bf` or at lane HEAD `95cf78ee` (grep for `items=42`,
  `42/27`, `43/28` finds only the row itself; `corpus/README.md` `## Round-52 corrections` covers living pins only).

- M2: landing — `[FILL]` left where the report's own commit hash belongs, and the placeholder row duplicated a real
  one. Fleet report `.ufo/reports/round-52/mori.md:5` ends ``Report commit `[FILL]`.``; `:46` is the table row
  `` | `[FILL]` | receipts at landed tip: `c1-at-landed.txt`, `c2-at-landed.txt`, `census-end.txt` | Round 52 | ``,
  identical in description to `:45`'s `37af57f2` row. The hash that exists is
  `aacd7a83027cdee8e950a2c39d490feaed3be13c` (`mori-shokunin <mori@shokunin.local> 2026-10-26T21:56:32-03:00`,
  `git log --format=%H -- .ufo/reports/round-52/mori.md` on the fleet repo). Evidence: those two lines; closure D1.
  Captured-by: none — QUALITY 9 states the obligation ("a report names the commit that carries its work") and no
  instrument reads report bytes; the closure found it. Fix: the round-53 convention, landed as a convention and not
  as an instrument — the report names its own commit by command, never by placeholder:
  `git log --format=%H -- .ufo/reports/round-53/mori.md` on the fleet repo, run after the report's commit (contract
  §Round-52 closure routed defects 2). Shown able to fail by a placeholder arm: `grep -rl '\[FILL\]'
  .ufo/reports --include='mori.md'` exits 0 on the round-52 report (2 hits) and finds 0 hits in the other 41 of 42
  mori reports, so the check fails exactly where the convention was broken and passes everywhere else. Not covered:
  the arm reads the placeholder token only; a report that names no commit at all passes it.

- M3: stale premise — an `on-release` recheck was authored *after* its release had been tagged, and the trigger sat
  unanswered for two rounds. `corpus/knowledge/memavailable-estimate-r51.md:9` and
  `corpus/knowledge/overcommit-commit-limit-r52.md:9` carry `recheck: on-release` over v7.2 URLs and both are
  `verified-at: 2026-10-26`; the release is older: cgit `tag/?h=v7.3` prints `tag date 2026-10-18 13:14:58 -1000`,
  `tag name v7.3 (091b06388b117fefdcb63336ac09956a4914b961)`, `tagged object commit c03c1a1450…`, message
  `Linux 7.3` — eight days before both entries. The lane's own bytes carried the sign twice and neither was followed:
  `LOG.md:2054` (round 32) records `docs.kernel.org renders 7.3.0`, and the round-52 wave seat wrote the banner
  difference into its rejection of the `latest` locator (`.ufo/waves/round-52/w1/Mo52ScribeGate.md:139-148`:
  `latest-overcommit-accounting.html:7.3.0`; `:202`: "the banner has already done (7.2.0 → 7.3.0) while the row's
  claim stayed at v7.2") without turning it into a recheck of its own v7.2 pins. The entering tip holds no recheck:
  `git grep -c -E 'v7\.3|7\.3\.0' 20edafa5 -- corpus/knowledge corpus/SOURCES.md SKILL.md` → exit 1, no match
  (`evidence/sweeps.txt:7-8`). Evidence: the two `recheck:` lines, the tag page, the two in-lane sightings, the sweep.
  Captured-by: none before round 53 — the `recheck:` line is prose and no instrument reads a kernel tag
  (`count-c1.py:6` asserts "that trigger has fired" as a premise, nothing on disk derived it). Fix: the round-53
  ledger `corpus/knowledge/kernel-v7.3-recheck-r53.md` (46 rows over S502–S510 with pinned v7.3 copies) and the C1
  ledger arm. Shown able to fail by `python3 .ufo/waves/round-53/count-c1.py <rev>`: at the entering tip
  `20edafa5` it reads `C1=unmet scope=46 rows=0 … source_rows=bad pins=bad provenance=bad … failed=ledger_absent,pins`,
  exit 1 (`.ufo/waves/round-53/evidence/control-c1-do-nothing.txt:3`), and at the data commit `2a4213bf` it reads
  `C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44
  absent=2 holds=46 changed=0 voted=0 dissent=0 … failed=votes` (`.ufo/waves/round-53/evidence/c1-at-data.txt:2`) —
  the omission fails, the recheck passes every arm the votes do not carry. Not covered: the fix reads no remote tag,
  so the trigger stays prose; the next tag still has to be noticed by a seat. Routed to round 54.
```

## Capture and fix state (so the L1 does not overclaim)

| mistake | class | captured-by (criterion) | instrument that fails on it today | fix state |
|---|---|---|---|---|
| M1 number-drift | LOW (verdict unaffected; cited receipt is the correct one) | none — QUALITY 141/142 scope excludes claim-table tallies; `count-c1.py` reads no SCORECARD byte | none; demonstrated only by a seat probe (`MISMATCH 2`, and `MISMATCH 0` on the matching round-51 row) | proposed arm, routed to round 54; the append-only SCORECARD correction of routed defect 1 is **not** in the tree at `2a4213bf` or `95cf78ee` |
| M2 `[FILL]` | LOW (bookkeeping; body text is complete) | QUALITY 9 states the rule; no instrument reads report bytes → captured-by: none | none committed; the grep arm discriminates 1/42 | convention landed for round 53 (name the commit by command); the arm itself is not an instrument — routed |
| M3 stale premise | MED (a freshness recheck was owed for two rounds over 46 claim rows) | none before round 53 (regex sweep found nothing; `recheck:` prose) | the round-53 C1 ledger arm, `failed=ledger_absent` at the entering tip | landed with C1's data (`rows=46 status_ok=46 quote_ok=46 pins=ok provenance=ok`); trigger detection still prose — routed to round 54 |

The two probes are seat probes: a read-only Python probe (`git -C <lane> show <rev>:SCORECARD.md` + file reads, no
write) and a two-command grep; neither is committed as an instrument, and I did not add anything to `tools/` or to a
frozen counter. The probe source, because its scratch directory was removed after the run:

```python
import re, subprocess
LANE="/home/vgpnk/Projects/shokunin/mori-shokunin"
def row(rev, lineno):
    t=subprocess.run(["git","-C",LANE,"show",f"{rev}:SCORECARD.md"],capture_output=True,text=True,check=True).stdout.splitlines()
    return t[lineno-1]
def tokens(s):
    return {m.group(1):m.group(2) for m in re.finditer(r'\b([a-z_]+)=([^\s,|`]+)', s)}
for name, lineno, cited in [
    ("round-51 C1", 2716, ".ufo/waves/round-51/evidence/c1-at-landed.txt"),
    ("round-52 C1", 2746, ".ufo/waves/round-52/evidence/c1-at-landed.txt")]:
    after=[c for c in row("95cf78ee", lineno).split("|")][-2]
    frag=re.findall(r'`(C1=[^`]*)`', after)
    rowtok=tokens(frag[0]) if frag else {}
    reci=re.findall(r'^C1=[^\n]*', open(f"{LANE}/{cited}").read(), re.M)[-1]
    reci_tok=tokens(reci)
    diffs={k:(v,reci_tok.get(k)) for k,v in rowtok.items()
           if k in ('items','locators','kill_residue','relocated','reloc_mismatch','classified','selftest')
           and reci_tok.get(k)!=v}
    print(f"{name}: MISMATCH {len(diffs)}: {diffs if diffs else '{}'}")
```

Its output (verbatim): `round-51 C1: MISMATCH 0: {}`; `round-52 C1: MISMATCH 2: {'items': ('42', '43'),
'locators': ('27', '28')}`.

## Named limits of this draft

1. M1's fix is not shown able to fail *as a committed instrument* — only as a probe over two rows (one passing, one failing).
   A pair is not a population: rows citing receipts with a different field set (round 49's `junk_met=`, round 50's
   `manifest=`) were not exercised, and an arm keyed on `C1=` would skip a row whose After cell quotes any other verdict stem.
2. M2's arm reads the literal token `[FILL]`; a differently spelled placeholder (`TODO`, `TBD`, an empty commit cell) passes.
   The convention itself is unenforced: nothing in `scripts/hyaku/` or the lane's tools reads `.ufo/reports/**`.
3. M3's evidence for "no round noticed" is a regex sweep over three paths (`corpus/knowledge`, `corpus/SOURCES.md`,
   `SKILL.md`) plus the two in-lane sightings I could name; a notice inside a wave report other than `Mo52ScribeGate.md`
   would not appear in that sweep. I did not enumerate every round-51/52 report for the string.
4. The tag date is read from the cgit `tag/?h=v7.3` page fetched 2026-10-26 (4247 bytes, no sha256 pin recorded for
   it); a tag forged later with an earlier date would not be detected by that read.
5. I ran no counter and re-scored nothing: every counter line quoted here is copied from a committed receipt at the
   revision named, not re-executed by this seat.

## Out of scope / routed

- `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `PROVINCE.md`, `corpus/`, `tools/`, `considerthese/` untouched; no edit to any
  frozen round-53 file; the C1/C2 counters, predicates, controls and kill rules untouched.
- Routed to round 54: (a) a committed row-vs-citation arm for SCORECARD claim rows (M1); (b) a placeholder/report-identity
  arm over `.ufo/reports/*/mori.md` (M2); (c) a readable release trigger for `recheck: on-release` entries so the next tag
  is detected by an instrument rather than by a seat (M3). None of the three is a fix to a frozen counter of this round.

## Findings

- **MED** — M3, `corpus/knowledge/memavailable-estimate-r51.md:9` and `corpus/knowledge/overcommit-commit-limit-r52.md:9`:
  `recheck: on-release` was written eight days after v7.3 was tagged (tag date `2026-10-18 13:14:58 -1000`) and no
  instrument reads a kernel tag; the omission stood for two rounds until round 53's ledger.
- **MED** — `.ufo/waves/round-52/w1/Mo52ScribeGate.md:139-148,197,202` and `LOG.md:2054`: the lane's own bytes recorded
  the rendered docs moving to 7.3.0 (round 52 used it only to reject a `latest` locator), so the release signal was in
  hand while the v7.2 `on-release` pins went unrechecked — the miss was one of follow-through, not of visibility.
- **LOW** — `SCORECARD.md:2746` (round-52 C1 row): After cell carries `items=42 … locators=27` while citing
  `evidence/c1-at-landed.txt`, whose verdict line prints `items=43 … locators=28`; the numbers are the at-data receipt's
  (`.ufo/waves/round-52/evidence/c1-at-data.txt:44`). Routed correction (defect 1) still unlanded at `2a4213bf` and
  `95cf78ee`; no instrument in `tools/` or the round-53 counters reads a claim row against its citation.
- **LOW** — fleet report `.ufo/reports/round-52/mori.md:5` (`Report commit \`[FILL]\``) and `:46` (a placeholder table row
  duplicating `:45`): the hash that exists is `aacd7a83027cdee8e950a2c39d490feaed3be13c`. Placeholders appear in 1 of 42
  mori reports; QUALITY 9 names the rule and nothing enforces it.
- **LOW** — capture gap, lane-wide: three of the three mistakes below have `captured-by: none` at the time they occurred,
  and all three were found by a non-author human read (closure D1/D2) or by the next round's seat. The round-53 convention
  for M2 and the C1 ledger arm for M3 narrow this; M1's arm remains a proposal.
