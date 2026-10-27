# Mo52ScribeMistakes — round-52 lesson `## Mistakes` draft

Seat: Mo52ScribeMistakes (scribe, round 52 wave `w1`). Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Entering tip `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`; freeze `d3a8ea5957b73bddbde750a8c0af2fba8da8b7c2`; data
`8524904adb25e44f24d9f25aac7eae909625c18c`; the tree I read is at `075436b1346ca659afb8be7a46f0e67e4170aa83`
(wave spec) with the wave's reports untracked. Scratch `/fast/scratch/hyaku/mori-r52/Mo52ScribeMistakes/`, removed
at the end; `TMPDIR` inside it; no clone made (only read-only `git show` / `sha256sum` / `grep` on the lane).

Scope of this seat: the four assigned mistake rows M1–M4, in the round-51 `## Mistakes` shape (columns
`id | class | evidence | captured-by | fix | shown able to fail`). Draft is fenced in §3 for the L1 to integrate;
nothing else in the lane was edited.

What I ran myself: `git show`/`git rev-parse`/`git log`/`git ls-tree` (read-only), `sha256sum`, `grep -n`, two
`python3` reads of the fleet `MANIFEST.json` (working-tree copy and `f0b61b4a`'s blob), and two throwaway draft
checks (§4) in scratch. I re-ran **no** frozen counter; every counter line quoted below is copied from the
committed receipt named with it.

## 1. Shape taken for the draft

`corpus/lessons/round-51.md:103-109` — heading `## Mistakes`, a blank line, then a six-column table whose
`shown able to fail` column is the round's rule that a fix counts only once a check is exhibited failing
(`round-51.md:105` is the header row). I keep that column and fill it per row; a row whose demonstration is a
proposed check names the check and the run that fails it.

## 2. Evidence per row

### M1 — a living check pinned at one round's tally and never superseded

Stale pin bytes at the entering tip `4f266ef2` (`git show 4f266ef2:corpus/QUALITY.md | sed -n '909,910p'`):

```
    source: S227. Check: `python3 tools/mori-sources-appendonly.py --selftest` → `pass=12 fail=0`;
```

`git show 4f266ef2:corpus/README.md | sed -n '607,608p'` gives the two round-39 coverage rows; their Bounded
advance cells pin `--selftest` → `pass=9 fail=0` (line 607, a bare `--selftest` that names no command) and
`python3 tools/mori-sources-appendonly.py --selftest` → `pass=12 fail=0` (line 608). The counter's own readings
(`.ufo/waves/round-52/evidence/control-c1-do-nothing.txt`, exit=1):

```
item living corpus/QUALITY.md:909 expect=pass=12_fail=0 got=MORI_SOURCES_APPENDONLY_SELFTEST_pass=22_fail=0_rc=0 state=mismatch
item living corpus/README.md:607 expect=pass=9_fail=0 got=unrunnable state=mismatch
item living corpus/README.md:608 expect=pass=12_fail=0 got=MORI_SOURCES_APPENDONLY_SELFTEST_pass=22_fail=0_rc=0 state=mismatch
```

The stale tally is the round-39 count; the committed gate has printed 22 since the round-41 freeze `d72ac167`
(`git log --oneline -1 d72ac167` → `round-41: freeze C1-C3 contracts and controls`; the rationale is in the
landed criterion `corpus/QUALITY.md:141`). Nothing executed these pins before this round:

```
$ for f in .ufo/waves/round-48/count-c1.py .ufo/waves/round-49/count-c1.py .ufo/waves/round-50/count-c1.py \
           .ufo/waves/round-51/count-c1.py tools/mori-pin-check.py; do
    printf '%-40s QUALITY=%s README=%s SHONEN=%s\n' "$f" ...; done
.ufo/waves/round-48/count-c1.py          QUALITY=0 README=0 SHONEN=0
.ufo/waves/round-49/count-c1.py          QUALITY=0 README=0 SHONEN=0
.ufo/waves/round-50/count-c1.py          QUALITY=0 README=0 SHONEN=6
.ufo/waves/round-51/count-c1.py          QUALITY=0 README=0 SHONEN=0
tools/mori-pin-check.py                  QUALITY=0 README=0 SHONEN=0
```

So K4 had been closed for `SHONEN.md` only (round 50), and the two living documents' pins were a written promise
that nothing in the lane read. The landed fix is supersession, not rewrite: `corpus/QUALITY.md:1356` (criterion 141, "This
row supersedes 112's check cell only; 112's criterion stands") and `corpus/README.md:722` (`## Round-52 corrections
(living pins)`, two bullets, each one line "on purpose: the counter reads a quoted stale pin as a quotation only
when its replacement pin stands on the same line"). The superseding lines' own pins then run — at the data commit
`item living corpus/QUALITY.md:1360 … got=MORI_SOURCES_APPENDONLY_SELFTEST_pass=22_fail=0_rc=0 state=ok` and
`corpus/README.md:727/:728 … state=ok` (`.ufo/waves/round-52/evidence/c1-at-data.txt`, `C1=met … superseded=4 …`, exit=0).

### M2 — the round-51 lesson's locator drift (closure D-c)

Filed text, `corpus/lessons/round-51.md:83-84`:

```
  `:55-57` `pagecache = … NR_ACTIVE_FILE + … NR_INACTIVE_FILE`, `:62` `pagecache -= min(pagecache / 2,
  wmark_low);`, `:67-69` the reclaimable slab/misc terms under the same `min(… / 2, wmark_low)` cap, `:71-72`
  `if (available < 0) available = 0;`, `:73` `EXPORT_SYMBOL_GPL(si_mem_available);`
```

`grep -n` on the committed copy `corpus/evidence/sources-r51/show_mem.c.v7.2` (my run, read-only):

```
23:unsigned long totalreserve_pages __read_mostly;
32:long si_mem_available(void)
47:	available = global_zone_page_state(NR_FREE_PAGES) - totalreserve_pages;
54:	pagecache = global_node_page_state(NR_ACTIVE_FILE) +
56:	pagecache -= min(pagecache / 2, wmark_low);
64:	reclaimable = global_node_page_state_pages(NR_SLAB_RECLAIMABLE_B) +
66:	reclaimable -= min(reclaimable / 2, wmark_low);
67:	available += reclaimable;
69:	if (available < 0)
70:		available = 0;
73:EXPORT_SYMBOL_GPL(si_mem_available);
```

Four of the bullet's eight locators name a span that does not hold the construct they name: `:55-57` for a
statement that starts at 54, `:62` for a line at 56, `:67-69` for the terms at 64-66 (67 is `available +=
reclaimable;`), `:71-72` for the clamp at 69-70. The same lesson's Gate row and the SOURCES anchor are right
(`copy lines 54-56`; anchor `23,32-73`), so the drift is prose nobody re-greps, not a wrong copy. The lane's
locator criterion is scoped away from lessons: `corpus/QUALITY.md:142` ("In `SCORECARD.md` `## Axes` and in the
`SHONEN.md` boxes, a `path:N` pointer after a quoted string…"), and `count-c1.py`'s arm D reads the Axes rows and
the SHONEN boxes only (`count-c1.py` docstring, arm (D)). The closure found the drift by hand
(`corpus/lessons/round-51-verifier-spotcheck.md:35`).

Fix carrier: the round-52 contract routes an appended erratum (contract §"Round-51 closure routed defects" item 5,
`corpus/lessons/round-51-erratum.md`). At the tip I read, that file is **absent** — `ls corpus/lessons/round-5*.md`
lists only the two round-51 files, and `git log --all --oneline -- corpus/lessons/round-51-erratum.md` is empty.
The wave carries a draft for it (`w1/Mo52ScribeErratum51.md`, whose §1 re-derives the same line numbers by
`grep -nF` on the same copy and by re-fetching the v7.2 raw file: `sha256` `dba76b26…b02f5`, `cmp` identical), so
the erratum is in flight, not landed. That is a finding for the L1's integration, below.

### M3 — the self-assessment lagging the fleet record by one round (Axes cells, round 51)

`## Axes` Last change cells, read with `git show <rev>:SCORECARD.md`:

| rev | operability cell leads | depth cell leads |
|---|---|---|
| `4f266ef2` (entering) | `round 47 (improved, score held); …` | `round 50 (improved, score held); …` |
| `8524904a` (data) | `round 51 (improved, score held); …` | `round 51 (improved, score held); …` |

Fleet record at the counter's pinned fleet revision (`git show f0b61b4ad192bcd95d7a76613a626f71285996ed:MANIFEST.json`
in the fleet repo, read-only; the working-tree copy prints the same three values):

```
pinned-rev 50 admitted unchanged improved
pinned-rev 51 admitted improved  improved
```

So both cells were correct against round 50's snapshot and one round stale at the round-51 tip. The counter's
arm A says it in one line each (`.ufo/waves/round-52/evidence/control-c1-do-nothing.txt`, exit=1):

```
item axis operability expect=round_51_improved got=round=47,evidence_missing:corpus/lessons/round-51-verifier-spotcheck.md state=mismatch
item axis depth expect=round_51_improved got=round=50,evidence_missing:corpus/lessons/round-51-verifier-spotcheck.md state=mismatch
```

This is the recurrence of a defect the Axes table already records in its own "Round-50 correction" paragraph
(cells that had skipped admitted improvements — the paragraph lists operability 36, 37, 38, 39, 41, 43, 44, 47 and
depth 38, 39, 41, 44, 47, 48, 49, plus coverage and calibration, `SCORECARD.md` after the table) — the correction
fixed the backlog, not the lag. The data commit rewrites both cells to lead with round 51
and to name `corpus/lessons/round-51-verifier-spotcheck.md:130` / `:131` in the Evidence cells; arm A then reads
`ok` (`c1-at-data.txt`, `C1=met … axes=6 …`, exit=0).

### M4 — a frozen file edited in place (closure D-e)

```
$ cat .ufo/waves/round-40/evidence/freeze-r40.txt | grep conform
5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf  .ufo/waves/round-40/conform.py
$ sha256sum .ufo/waves/round-40/conform.py
7f5174d542bd983552670b06f6cc424b10e53c81e55ecabcdd919f4043bdfa23  .ufo/waves/round-40/conform.py
```

No later freeze receipt pins that path (the round-52 freeze list
`.ufo/waves/round-52/evidence/freeze-sha256.txt` holds 24 lines: 19 of its own paths and the five `sources-r52`
copies — no `round-40/` path).
Round 51 disclosed the edit (D-e, `round-51-verifier-spotcheck.md:41`) and kept the round-40 receipts measured on
the frozen bytes; the working file and the round-40 claim's instrument are now two files. Round 52's response is a
policy ("this round edits none"), which prevents a new one but detects nothing — see P-M4.

## 3. Draft — `## Mistakes` (fenced; L1 integrates)

````text
## Mistakes

| id | class | evidence | captured-by | fix | shown able to fail |
|---|---|---|---|---|---|
| M1 | living pin frozen at one round's tally, never superseded and never run (K4 outside `SHONEN.md`) | At the entering tip `4f266ef2` `corpus/QUALITY.md:909` (criterion 112's Check) pins `python3 tools/mori-sources-appendonly.py --selftest` → `pass=12 fail=0`, `corpus/README.md:608` pins the same `pass=12`, and `:607` pins a bare `--selftest` → `pass=9 fail=0` that names no command; the committed gate has printed `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` since the round-41 freeze `d72ac167`. The pins were stale from that freeze to the data commit and nothing executed them: `grep -c QUALITY` is 0 in `count-c1.py` of rounds 48, 49, 50 and 51 and in `tools/mori-pin-check.py`, and round 50's K4 closed for `SHONEN.md` only. | none until this round's C1 arm C — the first instrument to enumerate and run the two living documents' single-line pins (`evidence/control-c1-do-nothing.txt`: `item living corpus/QUALITY.md:909 … state=mismatch`, `corpus/README.md:607 … got=unrunnable state=mismatch`, `:608 … state=mismatch`) | supersession by a later line, never an in-place rewrite: criterion 141 (`corpus/QUALITY.md:1356`) supersedes 112's check cell only, and `corpus/README.md:722` (`## Round-52 corrections (living pins)`) carries one one-line bullet per stale pin, because the counter reads a quoted stale pin as a quotation only when its replacement stands on the same line; each superseding line's own pin is then run (`corpus/QUALITY.md:1360`, `corpus/README.md:727`, `:728` read `state=ok` in `evidence/c1-at-data.txt`, `C1=met … superseded=4`, exit 0) | yes, four ways. `control-c1-do-nothing.txt` reads the three stale pins as mismatches; `control-c1-repeat-stale-tally.txt` shows superseding lines that repeat the stale tally are still run as pins and fail (`QUALITY.md:1354 … got=…pass=22… state=mismatch`, `README.md:722 … got=unrunnable state=mismatch`); `control-c1-rewrite-in-place.txt` and `control-c1-delete-stale-pins.txt` read `pin_removed_or_rewritten` ×3 each; `control-c1-living-only.txt` isolates the arm (living 7, superseded 4, all `ok`; `mismatches=5` from the other arms). The witness receipt (`control-c1-witness.txt`, `C1=met`) is disclosed feasibility built by the L1 with the data applier, not the claim's landing |
| M2 | a verification pointer outside every instrument's scope (round-51 closure D-c) | `corpus/lessons/round-51.md:83-84` cites `:55-57`, `:62`, `:67-69`, `:71-72` for S493; in the committed copy `corpus/evidence/sources-r51/show_mem.c.v7.2` the named constructs sit at 54-55, 56, 64-66/67 and 69-70, so four of the bullet's eight locators name a span that does not hold what they name. The same lesson's Gate row (`copy lines 54-56`) and the row anchor (`23,32-73`) are right, so the copy is not the problem. The lane's locator criterion stops short of lesson prose: `corpus/QUALITY.md:142` covers the `SCORECARD.md` Axes rows and the `SHONEN.md` boxes, and `count-c1.py` arm D reads the same two surfaces. The closure found it by hand (`corpus/lessons/round-51-verifier-spotcheck.md:35`). | none — no frozen counter reads lesson prose, so nothing could have caught it; the proposed check is P-M2 (§4 of `w1/Mo52ScribeMistakes.md`), routed to round 53 | the erratum the round-52 contract names (contract §"Round-51 closure routed defects" item 5, `corpus/lessons/round-51-erratum.md`) is drafted in this wave (`w1/Mo52ScribeErratum51.md`, locators re-derived by `grep -nF` on the committed copy, whose sha256 `dba76b26…b02f5` re-fetched and `cmp`-identical to the v7.2 raw file) and is **not yet in the tree** at `075436b1` (`git log --all -- corpus/lessons/round-51-erratum.md` empty); the filed lesson is not rewritten | yes, for the proposed rule: P-M2 run over the five Gate rows passes 5/5 with exact quotes, the S493 Gate quote passes on span `54-56` and fails on the wrong span `62-62`, and the Spot-check bullet's eight locators carry zero exact quotes (8 `unverifiable`) — the rule separates a right span from a wrong one and does not quietly pass the filed prose (`w1/Mo52ScribeMistakes.md` §4, exit 0 on the Gate set, both discriminators as expected) |
| M3 | self-assessment recomputed against the fleet MANIFEST as of the previous round | At `4f266ef2` the `## Axes` Last change cells led with `round 47` (operability) and `round 50` (depth); the fleet `MANIFEST.json` records mori round 51 `admitted` with `verdicts.operability=improved` and `verdicts.depth=improved`, and round 50 as `operability=unchanged`. Both cells were right against round 50's snapshot and one round stale at the tip. It recurs: the table's own "Round-50 correction" paragraph lists the rounds the cells had skipped (operability 36, 37, 38, 39, 41, 43, 44, 47; depth 38, 39, 41, 44, 47, 48, 49). | C1 arm A (the Axis/`MANIFEST` comparison): `control-c1-do-nothing.txt` → `item axis operability expect=round_51_improved got=round=47,evidence_missing:corpus/lessons/round-51-verifier-spotcheck.md state=mismatch` and `item axis depth … got=round=50 … state=mismatch` (2 of that run's 8 mismatches) | the data commit makes each Last change cell lead with `round 51 (improved, score held)` and names the closure's per-axis line in the Evidence cell (`corpus/lessons/round-51-verifier-spotcheck.md:130` and `:131`); arm A re-derives N* from the fleet MANIFEST at the pinned fleet revision on every run, so the lag cannot survive a run | yes: the same arm reads `state=ok` on all six axes at `8524904a` (`evidence/c1-at-data.txt`, `C1=met …`, exit 0) and `mismatch` ×2 on the entering bytes; `control-c1-axes-only.txt` isolates the arm (Axes all `ok`, `mismatches=5` remaining from the other three arms) |
| M4 | a frozen file edited in place, with no successor freeze (round-51 closure D-e) | `.ufo/waves/round-40/evidence/freeze-r40.txt` pins `.ufo/waves/round-40/conform.py` at `5025b9664632…90b83aaf`; at `075436b1` the file hashes `7f5174d542bd…043bdfa23` (`sha256sum`), and no later freeze receipt pins that path (round 52's list holds 24 lines, none under `round-40/`). Round 51 disclosed it (D-e, `corpus/lessons/round-51-verifier-spotcheck.md:41`) and kept the round-40 receipts measured on the frozen bytes, so the round-40 claim's instrument and the standing gate are now different files. Round 52's response is a policy — "this round edits none" — which prevents a new edit and detects none. | none — closure D-e found it by hand; no committed check re-hashes a freeze receipt's paths at the tip | copy-on-change, or record a successor freeze. Proposed check P-M4 (draft, `w1/Mo52ScribeMistakes.md` §4) re-hashes every `freeze*.txt` path at R and accepts a later round's pin for the same path; living documents (`SKILL.md`, `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`) are excluded because they are appended to by design | yes: P-M4 at `075436b1` prints `in_place_edits=10` including `r40 IN-PLACE-EDIT .ufo/waves/round-40/conform.py pinned=5025b9664632 now=7f5174d542bd successor=none`, while the four path/round pairs that did get a re-freeze read `successor-freeze(eq …)` (`tools/mori-sources-appendonly.py` r39 and r40 → r42, `tools/mori-round41-calibration.py` r41 → r45, `tools/mori-gate-registry.py` r44 → r45) and `r51` and `r52` contribute none — the rule passes a re-frozen file and fails an in-place edit (exit 1) |
````

## 4. Proposed checks (drafts; routed to round 53, not part of any frozen predicate)

Both were run read-only against the lane at `075436b1`, in scratch, and the scripts are reproduced verbatim here
so the L1 can re-run them without my tree.

### P-M2 — a lesson's locators carry exact quotes

Rule: apply arm D's quote-in-range test to a lesson's Gate and Spot-check rows. Each locator (`copy lines N-M` or
`:N[-M]`) must be accompanied by an exact double-quoted string, and that string, whitespace-collapsed, must occur
in lines N..M of the named copy; a locator with no exact quote is `unverifiable` and counts against the row.
Code fragments elided with `…` are not an assertion and are not accepted as one — that elision is exactly how the
round-51 drift stayed invisible to a reader who trusted the numbers.

Run (`python3 m2-locator-check.py`, scratch, read-only), output verbatim:

```
row lesson:28 proc.rst.v7.2 span=1128-1130 quote=(in) PASS
row lesson:29 show_mem.c.v7.2 span=54-56 quote=(in) PASS
row lesson:30 meminfo.c.v7.2 span=48-49 quote=(in) PASS
row lesson:31 mm_inline.h.v7.2 span=25-26 quote=(in) PASS
row lesson:32 34e431b0.patch span=11-12 quote=(in) PASS
discriminator span=54-56 want=PASS got=PASS ok
discriminator span=62-62 want=FAIL got=FAIL ok
spotcheck locators=8 exact_quotes=0 -> unverifiable=8
P-M2 gate_pass=5 gate_fail=0 exit=0
exit=0
```

Script body (trimmed to the rules; the full file was in scratch and is not cited as evidence):

```python
rowre   = r"^\| S49[2-6] \|"                       # Gate rows of this lesson
q_re    = r'"([^"]{20,})"'                          # exact quote
copy_re = r"copy `([^`]+)`"; span_re = r"copy lines (\d+)-(\d+)"
def collapsed(lines, n, m): return re.sub(r"\s+", " ", " ".join(lines[n-1:m])).strip()
def quote_in(q, lines, n, m): return re.sub(r"\s+", " ", q).strip() in collapsed(lines, n, m)
# Gate rows: PASS iff quote_in(quote, copy, N, M); discriminators as printed above; Spot-check bullet counted
# for locators vs exact quotes.
```

Limits: it reads one lesson at a time and needs the copy path to be named in the same row (the round-51 Spot-check
bullet names it in the bullet's first line); the rule is silent on whether the quoted words prove the claim — it
only proves the pointer lands on the words, which is the same limit arm D names.

### P-M4 — freeze integrity with a successor-freeze allowance

Rule: for every `sha256  path` line of every `.ufo/waves/round-*/evidence/freeze*.txt` (path resolved
repo-relative, else relative to `.ufo/waves/round-<r>/`), sha256 of the path at R equals the pinned value, or a
later round's receipt pins the same path and R's bytes equal that later pin; otherwise in-place edit. Living
documents excluded.

Run (`python3 m4-freeze-check.py`, output verbatim, exit 1):

```
r36 IN-PLACE-EDIT .ufo/waves/round-36/contract.md pinned=d903c67950a0 now=f88cf4d254c5 successor=none
r36 IN-PLACE-EDIT .ufo/waves/round-36/count-c1.py pinned=ed3f0e5e779e now=86dd3b7ab2d2 successor=none
r36 IN-PLACE-EDIT .ufo/waves/round-36/count-c2.py pinned=302f9aa05b54 now=c7edaacfff02 successor=none
r37 IN-PLACE-EDIT .ufo/waves/round-37/count-c1.py pinned=86699627c762 now=5279ed9df3b4 successor=none
r37 IN-PLACE-EDIT .ufo/waves/round-37/count-c2.py pinned=71c72929f9ac now=f173a642ac67 successor=none
r38 IN-PLACE-EDIT .ufo/waves/round-38/conform.py pinned=6bbcd25854b7 now=580a0bf15a81 successor=none
r38 IN-PLACE-EDIT .ufo/waves/round-38/count-c1.py pinned=4e59eeff33fc now=5aa51556946a successor=none
r38 IN-PLACE-EDIT .ufo/waves/round-38/count-c4.py pinned=5d416a1c5b24 now=8332341c3901 successor=none
r39 successor-freeze(eq r42 75af8f6fc63d) tools/mori-sources-appendonly.py pinned=62cd4132dbe1 now=75af8f6fc63d
r40 IN-PLACE-EDIT .ufo/waves/round-40/conform.py pinned=5025b9664632 now=7f5174d542bd successor=none
r40 successor-freeze(eq r42 75af8f6fc63d) tools/mori-sources-appendonly.py pinned=bde5a9a34c7e now=75af8f6fc63d
r41 successor-freeze(eq r45 8160212a1126) tools/mori-round41-calibration.py pinned=ddeaf5abe6fc now=8160212a1126
r44 successor-freeze(eq r45 8b82ac999091) tools/mori-gate-registry.py pinned=743996b11d19 now=8b82ac999091
r48 IN-PLACE-EDIT tools/mori-pin-check.py pinned=9832e38c3863 now=32685b9306db successor=none
P-M4 in_place_edits=10 freeze_files=14 exit=1
```

The M4 row cites only the `r40 … conform.py` line; the other nine are the in-lane-writer inventory the round-51
closure routed (item 8) and belong to the seat that owns it — I report the count so the two seats do not
double-count, and I claim nothing about those nine here.

Limits: "successor freeze" is inferred from a later receipt listing the same path, so a legitimate later edit with
no re-freeze is indistinguishable from a hazard (the rule errs toward reporting); the living-document exclusion is
a judgement, and three freeze receipts use wave-relative paths (`r36`, `r48`), which the fallback resolves.

## Findings

1. **MED — `corpus/lessons/round-51-erratum.md` is absent at `075436b1`.** The round-52 contract routes closure
   D-c and D-d to that appended erratum (contract §"Round-51 closure routed defects" item 5). The tree has no such
   file (`ls corpus/lessons/round-5*.md`; `git log --all -- corpus/lessons/round-51-erratum.md` empty); the wave's
   draft is `w1/Mo52ScribeErratum51.md`. If the L1's integration does not land it, D-c's fix has no carrier and the
   round-51 lesson keeps the four drifted locators at `corpus/lessons/round-51.md:83-84` as its only text.
2. **MED — lesson-prose locators are outside every instrument.** `corpus/QUALITY.md:142` scopes the locator
   criterion to the Axes rows and the SHONEN boxes, and `count-c1.py` arm (D) reads the same two surfaces, so a
   lesson's Gate/Spot-check pointers are unchecked (the round-51 drift is the measured instance: 4 of 8 locators
   in one bullet). P-M2 (§4) shows the rule is decidable and discriminating; it is not a claim of this round.
3. **MED — ten freeze receipts pin bytes that the tip no longer has, with no successor freeze**, one of them the
   D-e case (`.ufo/waves/round-40/conform.py`, `5025b966…` → `7f5174d5…`). P-M4's sweep at `075436b1` is the
   receipt; the round-52 freeze list does not re-pin any of the ten. The in-lane-writer inventory owns nine; no
   seat owns `round-36/contract.md` or `round-40/conform.py` unless the L1 assigns it with a successor freeze.
4. **MED — the Axes lag recurs.** M3's class is the same one the table's "Round-50 correction" paragraph records
   (skipped admitted improvements); the round-52 data commit fixes the current instance, and arm A now checks it
   every run, but nothing in the record forces the cell to be recomputed against the fleet MANIFEST of the *tip*
   rather than of the round in which it was written. Arm A's own limit is that it trusts the newest closure's
   per-axis table (`count-c1.py` docstring, named limits).
5. **LOW — the arm-C supersession rule is line-shaped.** `corpus/README.md:730-731` has to say "Each bullet is one
   line on purpose: the counter reads a quoted stale pin as a quotation only when its replacement pin stands on
   the same line", and arm C's named limit is that a pin split across lines is not enumerated. A supersession that
   a later edit wraps across lines silently becomes a live pin again (or vanishes from the enumeration). The
   reader-facing text depends on a formatting accident of the counter.
6. **LOW — `control-c1-witness.txt` is disclosed feasibility, not the claim's landing.** The claim's landing
   receipt is `evidence/c1-at-data.txt` at `8524904a` (`C1=met … exit=0`). The lesson text should not cite the
   witness as the round's evidence; M1's draft cites it only for what it is.

## Named limits of this report

- I re-ran no frozen counter, control, or pinned instrument. Every counter line quoted is copied from the receipt
  named beside it, with its exit code; my own runs are the reads, greps, hashes and the two draft checks in §4.
- The two draft checks are mine, not the round's instruments; their rules are stated in full so a reviewer can
  reject them. Neither is a claim of this round and neither is routed as a fix for a frozen predicate.
- The erratum state I report (`absent`) is measured at `075436b1` only; if the L1 lands
  `corpus/lessons/round-51-erratum.md` during integration, finding 1 is discharged and M2's fix column should cite
  the landed file instead of the draft.
- Scratch `/fast/scratch/hyaku/mori-r52/Mo52ScribeMistakes/` contained only the two draft scripts and their
  `TMPDIR`; it is removed. No clone, no fixture repository, no git mutation, no jj command, no file written in the
  lane except this report. No tool installed or upgraded this seat.
