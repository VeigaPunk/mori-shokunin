# Mo53RevenR52Row — how the round-52 SCORECARD C1 row came to carry the at-data tally while citing the at-landed receipt

seat: Mo53RevenR52Row · round 53 · wave w1 · lane mori-shokunin
report: `.ufo/waves/round-53/w1/Mo53RevenR52Row.md`
mode: read-only reconstruction. Lane repo untouched (`git status --porcelain` empty before and after; only this
file written). Scratch `/fast/scratch/hyaku/mori-r53/Mo53RevenR52Row/` (`TMPDIR` set there), removed at the end.
No packages installed, nothing upgraded, no host setting read besides the git objects and the two receipts.

Answer in one line: the row was written at integration `2f245af7` from the **at-data** run
(`8524904a`, `c1-at-data.txt`, `items=42 … locators=27`) and pointed at a receipt path that did not exist yet;
the receipt that path later received was measured at a tip whose SHONEN boxes carry **one more locator**, so it
reads `items=43 … locators=28`. One added locator: `corpus/knowledge/overcommit-commit-limit-r52.md:68-75`.

## 1. Commands read (all read-only)

```
git -C <lane> log --format='%h %ad %s' --date=iso -- SCORECARD.md .ufo/waves/round-52/evidence/c1-at-landed.txt
git -C <lane> log --format='%h %p %ad %s' --date=iso -6 37af57f2
git -C <lane> show <rev>:SCORECARD.md | grep -n "round-52/count-c[12].py"
git -C <lane> show <rev>:.ufo/waves/round-52/evidence/c1-at-landed.txt
git -C <lane> cat-file -e 2f245af7:.ufo/waves/round-52/evidence/c1-at-landed.txt   # rc 128
git -C <lane> diff e7e056b8 37af57f2 -- .ufo/waves/round-52/evidence/c1-at-landed.txt
sed -n '1,45p' .ufo/waves/round-52/count-c1.py        # arms A-D of the frozen counter
<scratch>/receipt_fidelity.py                          # §6, runs over HEAD and 2f245af7
```

`git log` on the two paths (exit 0, trimmed to the round-52 range):

```
37af57f2 2026-10-26 21:54:51 -0300 round-52: receipts at landed tip e7e056b8 — c1-at-landed, c2-at-landed, census-end
e7e056b8 2026-10-26 21:52:13 -0300 round-52: wave close — Mo52MutC1Controls report, w1-results.json, at-landed receipts (re-run at final tip)
2f245af7 2026-10-26 21:09:24 -0300 round-52: integration — SKILL Round52, SHONEN boxes, QUALITY 141-143, README corrections+coverage, LOG and SCORECARD round 52, ...
8524904a 2026-10-26 21:06:45 -0300 round-52: data — C1 Axes cells lead with round 51, SHONEN round-52 receipts, ...; C2 overcommit entry and S497-S501
```

Per path (exit 0): `SCORECARD.md` is last touched by `2f245af7`; `c1-at-landed.txt` by `37af57f2` and, before it,
`e7e056b8`; `c1-at-data.txt` by `075436b1` only. So the row is **older** than the receipt it cites.

## 2. Timeline (parent chain verified linear)

`git log --format='%h %p …' -6 37af57f2` prints `37af57f2 e7e056b8`, `e7e056b8 2f245af7`, `2f245af7 075436b1`,
`075436b1 8524904a`, `8524904a d3a8ea59`, `d3a8ea59 4f266ef2` — one line, no merges.

| # | commit | time (-0300) | what it did to this row |
|---|---|---|---|
| 0 | `d3a8ea59` freeze | 20:39:35 | contract + frozen counters |
| 1 | `8524904a` data | 21:06:45 | C1 Axes cells lead with round 51; C2 entry `overcommit-commit-limit-r52.md`. **No round-52 claim row yet** (`git show 8524904a:SCORECARD.md \| grep -n "round-52/count-c1.py"` → no output, rc 1). |
| 2 | `075436b1` w1 spec | 21:07:40 | adds `evidence/c1-at-data.txt`: run at **`8524904a`**, `C1=met items=42 … locators=27 … rev=8524904a…`, `exit=0` |
| 3 | `2f245af7` integration | 21:09:24 | adds the two round-52 claim rows (`SCORECARD.md:2746`, `:2747`) whose After cells cite `evidence/c1-at-landed.txt` / `c2-at-landed.txt`, **neither of which exists at this commit**; rewrites the four `SHONEN.md` boxes to round-52 pointers |
| 4 | `e7e056b8` wave close | 21:52:13 | **creates** `evidence/c1-at-landed.txt` with a run at its parent **`2f245af7`**: `C1=unmet items=43 … errors=1 … lane_writes=1 … rev=2f245af7… failed=errors,lane_writes`, `exit=1`. Also adds `w1-results.json` (416 lines) — the untracked file that reddened that very run. |
| 5 | `37af57f2` receipts at landed tip | 21:54:51 | **replaces** `c1-at-landed.txt` with a run at its parent **`e7e056b8`**: `C1=met items=43 … locators=28 … rev=e7e056b8…`, `exit=0`. This is the content the row's citation points at today. |

Integration precedes both at-landed receipts by 43 and 45 minutes. `git ls-tree --name-only 2f245af7
.ufo/waves/round-52/evidence/` lists `c1-at-data.txt`, `c2-at-data.txt`, … and **no** `c1-at-landed.txt`
(`git cat-file -e 2f245af7:.ufo/waves/round-52/evidence/c1-at-landed.txt` → `fatal: path … exists on disk, but
not in '2f245af7'`, **rc 128**; the same call for `c1-at-data.txt` → **rc 0**).

## 3. The row and the two receipts

`SCORECARD.md:2746` (identical at `2f245af7` and at HEAD — `cmp` of the single line: IDENTICAL; `git log -1 --
SCORECARD.md` → `2f245af7`):

```
| C1 the self-assessment agrees with the fleet MANIFEST, ... | calibration 5 | `python3 .ufo/waves/round-52/count-c1.py R` |
  `C1=unmet items=37 … living=4 superseded=1 locators=25 mismatches=8 … failed=mismatch`, rc 1 — `evidence/control-c1-do-nothing.txt` |
  `C1=met items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0 lane_writes=0`, rc 0 — `evidence/c1-at-landed.txt` |
```

Summary lines (verbatim; sha256 of the files at HEAD below each):

```
c1-at-data.txt   C1=met items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=8524904adb25e44f24d9f25aac7eae909625c18c
c1-at-landed.txt C1=met items=43 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=28 mismatches=0 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=e7e056b8a17e54516a3c17798221c30e9902c250
```

`sha256sum` (exit 0): `4720c4697190f22dafa0302d32a11683e89cfedab5da0ec56b9b24a21273cd72  c1-at-data.txt`,
`b5e5ee45a9fc91184a2cb1eccec27a115083e454687a7bd0e14d549190d375aa  c1-at-landed.txt` (45 and 46 lines).

Provenance of the row's numbers, tested as string containment:

```
quoted='C1=met items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0 lane_writes=0'
  substring of c1-at-data.txt  : True
  substring of c1-at-landed.txt: False
```

The row's After cell is a verbatim prefix of the **at-data** summary and occurs nowhere in the file it cites.
**Attribution: the After cell was filled from the at-data run while the citation names the intended landed
receipt.** `[INFERENCE]` on the filling act itself (the scribe draft `.ufo/waves/round-52/w1/Mo52ScribeScorecard.md`
left both After cells as `[L1 fills]` and its item 7 records the at-data summary as the receipt of record; the
integration commit is the L1's). The byte-level containment above is observed.

Both Before cells match their cited control receipts field for field (verified by the same check, §6 — line 2746's
`items=37 …` pairing against `control-c1-do-nothing.txt` produces no finding).

## 4. Why the tally is one higher at the landing: the locator source is the SHONEN boxes

Arm D of the frozen counter (`.ufo/waves/round-52/count-c1.py` docstring, lines 32-35) takes its locators from
"every backticked `path:N[-M]` in the six Axes rows and the SHONEN boxes"; `check_locators` implements exactly
that (rows of the `## Axes` table whose first cell is an axis name, columns `r[2:]`, plus every `BOX`-matching
`SHONEN.md` line). Split at the two revisions, using the counter's own regex
``LOC = re.compile(r"`([A-Za-z0-9_][A-Za-z0-9_./-]*):(\d+)(?:-(\d+))?`")`` and its `axes_table` parser:

```
data 8524904a:      axes-row locators=21 shonen-box locators=6  total=27
integration 2f245af7: axes-row locators=21 shonen-box locators=7  total=28
```

The Axes arm is identical (21/21); the whole delta is the `SHONEN.md` rewrite in the integration commit
(`git diff 8524904a 2f245af7 -- SHONEN.md`, four box lines replaced):

```
- SKILL.md box: `SKILL.md:1069-1141`, `SKILL.md:1018-1067`, `corpus/QUALITY.md:1252-1352`
+ SKILL.md box: `SKILL.md:1144`, `SKILL.md:1069-1141`, `corpus/QUALITY.md:1252-1373`
- LOG.md box:   `LOG.md:2765-2805`, `LOG.md:2732-2763`
+ LOG.md box:   `LOG.md:2808`, `LOG.md:2765-2805`
- boundaries box: `PROVINCE.md:3-16`; `corpus/knowledge/quota-observability-r48.md` Boundaries; `.ufo/waves/round-48/…`
+ boundaries box: `PROVINCE.md:3-16`; `corpus/knowledge/overcommit-commit-limit-r52.md:68-75` Boundaries
```

So the **one added locator** is `corpus/knowledge/overcommit-commit-limit-r52.md:68-75` — the C2 entry's
`Boundaries` span, cited by the "no cross-domain bleed" box to show the new entry claims v7.2 bytes only. Three
spans were re-pointed in the same edit (`SKILL.md:1018-1067`→`SKILL.md:1144`; `LOG.md:2732-2763`→`LOG.md:2808`;
`QUALITY.md:1252-1352`→`QUALITY.md:1252-1373`), which changes no count. The receipt's one extra `item` line is
therefore the new locator's line, which lands last in file order:

```
at-data   (45 lines): … item locator PROVINCE.md:3-16 …                       → items=42 locators=27
at-landed (46 lines): … item locator PROVINCE.md:3-16 …
                        item locator corpus/knowledge/overcommit-commit-limit-r52.md:68-75 expect=range got=ok state=ok  → items=43 locators=28
```

Arithmetic agrees: `items = axes(6) + pins(2) + living(7) + locators`; `6+2+7+27 = 42`, `6+2+7+28 = 43`
mechanical counts of `^item axis|pin|living|locator` lines: 6/2/7/27 and 6/2/7/28, total `^item` 42 and 43).
`boxes=4` comes from the SHONEN parse and is unchanged. One living item changed only its pointer,
`item living corpus/QUALITY.md:1360` → `corpus/QUALITY.md:1362` (QUALITY rows 141-143 were appended above it);
the count stays 7.

Two independent reasons make the at-data tally structurally stale for a **self-assessment** row:
1. at `8524904a` the row did not exist (step 1 above), so the run measured a document without the row;
2. the locator source it reads (`SHONEN.md` boxes) was rewritten after the run, adding a locator.

## 5. The at-landed receipt was red first

The first committed content of the cited path is not the green run. `git diff e7e056b8 37af57f2 --
.ufo/waves/round-52/evidence/c1-at-landed.txt` (4 deletions, 3 insertions):

```
-$ python3 .ufo/waves/round-52/count-c1.py 2f245af7d6dd6878de266f3436d12f47df900144 --scratch …/c1land2
-lane_write ?? .ufo/waves/round-52/w1-results.json
+$ python3 .ufo/waves/round-52/count-c1.py e7e056b8a17e54516a3c17798221c30e9902c250 --scratch …/c1fin
 …
-C1=unmet items=43 … errors=1 … lane_writes=1 … rev=2f245af7… failed=errors,lane_writes
-exit=1
+C1=met items=43 … errors=0 … lane_writes=0 … rev=e7e056b8…
+exit=0
```

`git show --stat e7e056b8`: `c1-at-landed.txt | 47 +`, `c2-at-landed.txt | 3 +`, `w1-results.json | 416 +`,
`w1/Mo52MutC1Controls.md | 130 +`. `git ls-tree --name-only 2f245af7 .ufo/waves/round-52/w1-results.json` →
nothing (absent at the measured rev, present at `e7e056b8`): the "at-landed" run was made from a worktree holding a
file the same commit then added, so `lane_writes` fired on the lane's own pending evidence.

That single untracked file is reported twice. `grep -c "state=error"` on the red receipt → `0`, while
`count-c1.py` computes `errs = sum(state=="error") + (1 if writes else 0)`, so one `??` line yields both
`errors=1` and `lane_writes=1` and `failed=errors,lane_writes` names one cause twice. The counter is **frozen**:
recorded here as a named limit, not a proposed change.

## 6. The check that would have caught it

Three arms, all read-only, all cheap. Implemented as one script over the git objects (`git show`, worktree read
for HEAD) and run at HEAD and at the integration commit. Output (exit 0):

```
rev=HEAD(37af57f2) pairs checked=36 findings=2
  SCORECARD.md:2340 C1 no-summary-in-receipt .ufo/waves/round-42/evidence/c1-after.txt
  SCORECARD.md:2746 C1 field-mismatch .ufo/waves/round-52/evidence/c1-at-landed.txt
      items: row=42 receipt=43
      locators: row=27 receipt=28
rev=2f245af7       pairs checked=36 findings=3
  SCORECARD.md:2340 C1 no-summary-in-receipt .ufo/waves/round-42/evidence/c1-after.txt
  SCORECARD.md:2746 C1 cited-receipt-absent .ufo/waves/round-52/evidence/c1-at-landed.txt
  SCORECARD.md:2747 C2 cited-receipt-absent .ufo/waves/round-52/evidence/c2-at-landed.txt
```

- **A1 existence-at-write** (rows added in a commit must cite receipts that exist in that commit): fires at
  `2f245af7` for **both** round-52 rows, 43 minutes before either receipt existed. Cheapest arm; needs no field
  list. A plain `git cat-file -e <commit>:<cited path>` (rc 128 / rc 0, §2) is the whole test.
- **A2 field-match** (every `key=value` in the row's quoted summary must equal the named field of the
  `TAG=` summary line in the cited receipt at the same revision): fires at HEAD on `items` (42≠43) and `locators`
  (27≠28), and only there among 36 summary↔citation pairs.
- **A3 verbatim-substring** (the row's quoted text, minus the `, rc N` marker, must be a substring of the cited
  receipt's summary line): equivalent to §3's containment test and catches it with no field list, which is why the
  row's elision of `manifest=… rev=…` matters — carrying `rev=8524904a…` in the row would have shown the measured
  revision at a glance.

Why the lane's own instruments cannot: arm (D) of `count-c1.py` validates the **files the row points into** (they
exist at R, `M ≤ len(lines)`, the quoted string or `proposed A → B` pair occurs at N..M) and never reads the
receipt a row cites; arm (A) reads only the `## Axes` table against `MANIFEST.json` and the newest closure. The
round-52 wave's locator-sweep seat even reproduced the counter's `locators=27` exactly
(`.ufo/waves/round-52/w1/Mo52ExecLocatorSweep.md:201`: "21 Axes-row + 6 SHONEN-box locators = the counter's
`locators=27`") — a faithful replication of a number that was already stale by the time the row was written.

Two precision caveats for the script (recorded, not defects of the lane): citations are relative to the wave dir
of the counter named in the same row, and a row may name more than one (`SCORECARD.md:2054` names round-36's c2
counter and round-37's c1 counter; resolving against the first match alone produced two false
`cited-receipt-absent` findings until the script tried every wave dir named in the row). And one row quotes a
command's inline output rather than a receipt summary (`SCORECARD.md:2340` → `evidence/c1-after.txt` holds only
`check … PASS` lines), which the field arm must special-case.

The whole check, as run:

```python
import re, subprocess, os, sys

LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"

def git(*a):
    return subprocess.run(["git","-C",LANE]+list(a),capture_output=True,text=True)

def blob(rev, path):
    if rev is None:
        try:
            return open(os.path.join(LANE,path), encoding="utf-8", errors="replace").read()
        except OSError:
            return None
    r = git("show", f"{rev}:{path}")
    return r.stdout if r.returncode == 0 else None

SUM = re.compile(r"^([A-Z][A-Z0-9_]*)=(.+)$")
FIELD = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)=([^\s,]+)")

def parse_summary(text):
    text = text.strip()
    text = re.split(r",\s*rc\s*=", text)[0]
    m = SUM.match(text)
    if not m:
        return None, None
    return m.group(1), dict(FIELD.findall(m.group(2)))

def receipt_summary(body, tag):
    for line in body.split("\n"):
        if line.startswith(tag+"="):
            return line, parse_summary(line)[1]
    return None, None

def cells_of(line):
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]

def resolve(rev, waves, cited):
    for w in waves:
        p = w + "/" + cited
        b = blob(rev, p)
        if b is not None:
            return b, p
    return None, "|".join(w + "/" + cited for w in waves)

def check(rev, only_rounds=None):
    sc = blob(rev, "SCORECARD.md")
    findings, checked = [], 0
    for lineno, line in enumerate(sc.split("\n"), 1):
        if not line.startswith("|"):
            continue
        waves = []
        for c in re.findall(r"`(python3[^`]*)`", line):
            m = re.search(r"(\.ufo/waves/round-\d+)/count-c[12]\.py", c)
            if m and m.group(1) not in waves:
                waves.append(m.group(1))
        if not waves:
            continue
        if only_rounds and not any(any(w.endswith(r) for w in waves) for r in only_rounds):
            continue
        for cell in cells_of(line):
            # pair each backticked summary with the evidence citation that follows it in this cell
            tokens = re.findall(r"`([^`]+)`|(evidence/[A-Za-z0-9_.\-/]+\.txt)", cell)
            pending = None
            for quoted, plain in tokens:
                if plain:
                    if pending is None:
                        continue
                    tag, fields = pending
                    pending = None
                    checked += 1
                    body, path = resolve(rev, waves, plain)
                    if body is None:
                        findings.append((lineno, tag, path, "cited-receipt-absent", {}))
                        continue
                    sline, rf = receipt_summary(body, tag)
                    if rf is None:
                        findings.append((lineno, tag, path, "no-summary-in-receipt", {}))
                        continue
                    bad = {k: (v, rf.get(k)) for k, v in fields.items() if k not in rf or rf[k] != v}
                    if bad:
                        findings.append((lineno, tag, path, "field-mismatch", bad))
                    continue
                if quoted:
                    if re.fullmatch(r"evidence/[A-Za-z0-9_.\-/]+\.txt", quoted):
                        if pending is None:
                            continue
                        tag, fields = pending
                        pending = None
                        checked += 1
                        body, path = resolve(rev, waves, quoted)
                        if body is None:
                            findings.append((lineno, tag, path, "cited-receipt-absent", {}))
                            continue
                        sline, rf = receipt_summary(body, tag)
                        if rf is None:
                            findings.append((lineno, tag, path, "no-summary-in-receipt", {}))
                            continue
                        bad = {k: (v, rf.get(k)) for k, v in fields.items() if k not in rf or rf[k] != v}
                        if bad:
                            findings.append((lineno, tag, path, "field-mismatch", bad))
                        continue
                    tag, fields = parse_summary(quoted)
                    if tag and fields is not None:
                        pending = (tag, fields)
    return checked, findings

for rev in [None, "2f245af7"]:
    checked, f = check(rev)
    print("rev=%-14s pairs checked=%d findings=%d" % (rev or "HEAD(37af57f2)", checked, len(f)))
    for lineno, tag, path, kind, bad in f:
        print("  SCORECARD.md:%d %s %s %s" % (lineno, tag, kind, path))
        for k,(row,rec) in bad.items():
            print("      %s: row=%s receipt=%s" % (k, row, rec))
```

## 7. Relation to round-52 closure D2 / round-53 routed defect 1

`corpus/lessons/round-52-verifier-spotcheck.md` §Conformance defects D2 already states the numbers (42/27 vs 43/28)
and the attribution ("written at integration `2f245af7`, before `c1-at-landed.txt` existed; its numbers are
verbatim from `c1-at-data.txt` (measured `8524904a`)"). This reconstruction confirms both claims by direct byte
comparison and adds four facts the closure did not record:

1. the citation's **nonexistence at write time is testable and fails hard** (`cat-file -e` rc 128 on both round-52
   receipts at `2f245af7`), so this class is catchable before any wave runs;
2. the cited path's **first committed content was a red run** (`C1=unmet … errors=1 lane_writes=1`, exit 1 at
   `e7e056b8`), replaced 2m38s later; the row's citation therefore pointed, for that interval, at an unmet receipt;
3. the exact provenance of the +1: the `SHONEN.md` box rewrite contributing
   `corpus/knowledge/overcommit-commit-limit-r52.md:68-75` (Axes arm unchanged at 21, SHONEN arm 6 → 7);
4. an arm that catches it (A1–A3, §6) with the reading at both revisions.

## 8. Reconstructed contract, invariant, divergences, confidence

**Contract as the lane practices it.** A SCORECARD claim row is `claim | axis | counting command | before
(tally, rc N — receipt) | after (tally, rc N — receipt)`. The After cell's quoted summary is meant to be a
run of the named command at the landed tip, and its citation is meant to be the receipt holding that run, with
citations resolved relative to the wave dir of the counter named in the same row.

**Last-known-good invariant.** The row's quoted summary equals — field for field, and including `rev=` — the
summary line of the receipt it cites at the revision the row was written. Round-51's row (`SCORECARD.md:2716`,
`kill_residue=0 relocated=met … selftest=pass=125`) satisfies it: the pairing against
`.ufo/waves/round-51/evidence/c1-at-landed.txt` produces no finding in §6 at HEAD.

**Where current behavior diverges.** `SCORECARD.md:2746` violates it in two fields (`items`, `locators`) and in
the implied revision (`8524904a` vs `e7e056b8`); the invariant is unenforced because neither the frozen counter
(arms A-D) nor any `tools/` instrument compares a row's numbers with the receipt it names.

**Confidence.** HIGH on the timeline, hashes, parent chain, receipt bytes, the 21+6/21+7 locator split, the added
locator, the red-first receipt and the check's readings — each is a command output quoted above. MED on the
authorship step (the L1 filling the After cell from the at-data run): the byte containment and the scribe's
`[L1 fills]` draft support it, but the act itself is not observable.

## Findings

- **MED** — `SCORECARD.md:2746` (round-52 C1 row): After cell carries `items=42 … locators=27`, a verbatim
  substring of `evidence/c1-at-data.txt` (run at `8524904a`) and **absent** from the cited
  `evidence/c1-at-landed.txt` (`items=43 … locators=28`, `rev=e7e056b8`). Verdict unaffected (both receipts
  `C1=met`, rc 0); the evidence cell is false as written. Fix path already ruled: an appended correction line
  naming the superseded text (round-52 closure routed defect 1 / round-53 contract §Round-52 closure).
- **MED** — `SCORECARD.md:2746` and `SCORECARD.md:2747`: both round-52 rows cite `evidence/c1-at-landed.txt` /
  `evidence/c2-at-landed.txt`, which do not exist at the commit that wrote them (`git cat-file -e 2f245af7:…` →
  rc 128; created 43 and 45 minutes later). No instrument in the lane checks cite-existence at write time.
- **LOW** — `.ufo/waves/round-52/evidence/c1-at-landed.txt`: first committed at `e7e056b8` with a **red** run
  (`C1=unmet … errors=1 lane_writes=1 … rev=2f245af7`, `exit=1`) and replaced at `37af57f2`; the redness came from
  the untracked `w1-results.json` that `e7e056b8` itself added, i.e. an at-landed run taken from a worktree that
  was not yet the commit it landed in.
- **LOW** — `.ufo/waves/round-52/count-c1.py:432` region (frozen): one untracked path yields both `errors=1` and
  `lane_writes=1`, so `failed=errors,lane_writes` names one cause twice. Named limit for round 54, not a change.
- **LOW** — `.ufo/waves/round-52/count-c1.py` arms (A) and (D) (docstring lines 21-35): arm D validates the files a
  row points into, arm A only the `## Axes` table against `MANIFEST.json`; neither reads a cited receipt's numbers,
  so the row↔receipt fidelity class is outside the frozen counter's reach. Round-53's `count-c1.py`/`count-c2.py`
  measure other surfaces and inherit no such arm.
- **LOW** — `SCORECARD.md:2746`: the quoted summary elides `manifest=` and `rev=`, which is exactly what lets a
  different run's numbers pass as the cited one; an A3 verbatim-substring arm closes it without a field list.
- **LOW** — citation resolution is unstated: `SCORECARD.md:2054` names two wave dirs (`round-36/count-c2.py`,
  `round-37/count-c1.py`), so any fidelity checker must try every wave dir named in the row (a single-dir rule
  produced two false `cited-receipt-absent` findings here).
- **LOW** — `SCORECARD.md:2340`: quotes a command's inline output while citing
  `.ufo/waves/round-42/evidence/c1-after.txt`, which holds only `check … PASS` lines and no `TAG=` summary; the
  field arm needs an explicit rule for inline quotes (pre-existing, round 42, not this round's defect).
