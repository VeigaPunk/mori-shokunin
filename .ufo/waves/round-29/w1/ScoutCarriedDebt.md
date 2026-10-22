# ScoutCarriedDebt — inventory of the debt carried at round-28-verifier-spotcheck.md:132-133

Seat: MoriR29.ScoutCarriedDebt (scout, leaf — no subagents, no background jobs). Measurements are reads at the
entering tip `7118f320` (lane HEAD was `8a45cef`), read-only git only, plus one run of the runway tool's own
self-test on committed fixture bytes. Nothing written but this file; the oom-killers tool was neither read nor
run (blindness held). Round-29 C1/C2 files, for the last column: C1 = `SCORECARD.md` `## Axes` table and
`.ufo/waves/round-29/count-c1.sh`; C2 = `tools/fixtures/mori-oom-killers/cases-a2-r29.json`,
`.ufo/waves/round-29/count-c2.sh` and the oom tool only on a judged tool error (`contract.md:20-24,36-44`).
Disposition for D1–D5: round-29's C1 counter does not consume the row-identity half, so F1/F2/F3/F6/F10 cannot
touch a round-29 claim; editing the admitted round-28 counter would make its gate output unreproducible.

## Summary

| # | item | open at 7118f320 | smallest fix | one hour, no C1/C2 file |
|---|---|---|---|---|
| D1 | F1 separate-repo halves | yes | rewrite the fetched check's LANE (1 line) | yes (~5 min); rewrites admitted evidence |
| D2 | F2 whitespace-blind restore | yes | raw compare of the 8 immutable cells | yes (~20 min), needs a new check rev |
| D3 | F3 rows outside the registry table | yes | bound the scan to `## Registry` | yes (~10 min), counter-local |
| D4 | F6 source/anchor/opened unchecked | yes | 2 non-empty checks + Gate-URL prefix match | yes (~20 min), counter-local |
| D5 | F10 mutable-cell restore | yes; its stated fix is wrong | same fix as F2, used-by stays exempt | yes, only as the F2 fix |
| D6 | S146 `teaches` self-contradiction | yes | new superseding row (cell immutable) | yes (~35 min) except the S153+ block |
| D7 | reader-sweep range citations | yes, 4 sites | 4 one-line rewrites | yes (~10 min) |
| D8 | "opened this round" dating | yes at :257, partial at :318 | 2 one-line rewrites | yes (~5 min) |
| D9 | old rows' `used-by` cells | yes, 8 stale cells | one cell rewrite per row | yes (~15 min) |
| D10 | r25 R1 | headline closed; 3 residuals | 3 small edits in the runway tool | yes (~20 min) |
| D11 | r25 R5 | registry closed; self-test + fail-opens open | new `--selftest` + D1/D5 hardening | no (>1 h) |

## D1 — MutCountC1 F1: the two halves can measure different repositories

`count-c1.sh:12` sets `LANE`, but the check it fetches at `:25` is run unmodified at `:28` and carries its own
hardcoded path at `check-row-identity.py:19`; the baseline walk (`:64-67`) then reads that other repository, and
in a truncated-history copy the baseline collapses onto the current row (`:73`).

```
$ git show 7118f320:.ufo/waves/round-28/count-c1.sh | sed -n '12p;25p;28p'
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
git -C "$LANE" show "df886be1…:$CHECK" > "$T/check.py" || { echo "check_absent"; exit 2; }
ri=$(python3 -I -B "$T/check.py" "$R" 2>/dev/null | grep -E '^rows=[0-9]+ changed=' | tail -n 1)
$ git show 7118f320:.ufo/waves/round-27/check-row-identity.py | sed -n '19p'
LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"
```

Smallest fix: one added line after the fetch rewriting the temp copy's assignment to `$LANE`
(`sed -i "s|^LANE = .*|LANE = \"$LANE\"|" "$T/check.py"`). The measured fail-open chain is MutCountC1's
F1-a/F1-b/F1-c table (`w1/MutCountC1.md`, "F1 measured directly"); both constants name the same path at the
real lane, so it bites exactly the copy-the-counter workflow the probe used. Fits: yes, minutes — but it edits
the admitted round-28 counter, so carry it and let a successor counter (D2) hold the redirect.

## D2 — MutCountC1 F2: a restored row may differ from its first-published bytes by whitespace

`check-row-identity.py:37` strips every cell; `:74` compares the stripped values, while round-28 contract
`:19` requires "restored byte-equal to their first-published cells". Mutants m08/m08b/m08c survive.

```
$ git show 7118f320:.ufo/waves/round-27/check-row-identity.py | sed -n '37p;74p'
        cells = [c.strip() for c in SEP.split(line.strip())]
        diff = [NAMES[i] for i in range(len(NAMES)) if NAMES[i] not in MUTABLE and base[i] != now[rid][i]]
```

Smallest fix: keep a second, unstripped split and compare the eight immutable columns on raw bytes (stripped
split stays for parsing). The check is imported by blob from the frozen `df886be1` (`count-c1.sh:25`), so this
needs a new check file and a one-line pin bump; the counter cannot do it from its own heredoc. Fits: yes, ~20 min
including a re-run that must still print `changed=0` at `7118f320`; land the new check and name the old one
superseded in the lesson rather than rewriting `df886be1`.

## D3 — MutCountC1 F3: superseding rows may sit outside the registry table

The counter scans every line of `corpus/SOURCES.md` for the row shape (`count-c1.sh:36-40`) and never bounds
the scan to the table; f01 (rows under `## Drafts`) and f14 (rows in a code fence) read met.

```
$ git show 7118f320:.ufo/waves/round-28/count-c1.sh | sed -n '36,40p'
for line in open(sources, encoding="utf-8").read().split("\n"):
    if re.match(r" {0,3}\|[ \t]*S[0-9]{3,}[ \t]*\|", line):
$ git show 7118f320:corpus/SOURCES.md | grep -n '^## '
3:## Registry
160:## Paths
```

The real new rows are at 151-158, inside 3-159, so the defect is latent at the tip. Smallest fix: compute the
Registry span before the loop and skip lines outside it — about four lines in the heredoc, no new check rev; fits
in ~10 min.

## D4 — MutCountC1 F6: source, anchor and opened are never inspected

The counter reads only `r[7]` teaches, `r[8]` status and `r[11]` used-by (`count-c1.sh:51-66`); source (`c[2]`),
anchor (`c[6]`) and opened (`c[9]`) are unchecked, so f04/f13 (empty cells) and f08 (`example.invalid`) read
met. Open at `7118f320`: the same lines contain no reference to those indices.
Real-tree check, so a fix does not red the lane: all eight new rows have source/anchor/opened non-empty; source
cell equality with the superseded row holds for S145, S147, S148, S150 and fails for S146, S149, S151, S152.
So a blanket equality rule is wrong: S146 is an absence row citing the man-pages tarball, not S097's 404 URL,
and S149/S151/S152 each merge several upstream files. Smallest fix: require the three cells non-empty (closes
f04/f13), and require one Gate-line URL to prefix-match a URL in the source cell, allowing a `.patch`/`.diff`
suffix (closes f08; S145 needs the allowance because its Gate URL is the source URL plus `.patch`); fits in
~20 min, counter-local.

## D5 — MutCountC1 F10: mutable-cell restore — and a wrong fix in the carried text

`check-row-identity.py:22` exempts status, recheck and used-by, applied at `:74`; the counter adds no separate
comparison, so f02 reads changed=0 — still open at `7118f320`. Correction: F10's stated fix ("compare the three
restored ids' full raw lines") would **fail the real tree**. S097's used-by is not byte-equal to first-published:
`df4db54a` holds `corpus/lessons/round-24.md` only, the live reader path was added at `7c77fba3`
(2026-10-22T06:11:03-03:00, round 24), and all eight old rows' used-by cells were identical at `6ebd518f` and
`7118f320`. QUALITY 81 (`corpus/QUALITY.md:373-375`) makes used-by mutable, so this is legitimate. Smallest fix:
the D2 raw immutable-cell comparison alone; keep the three mutable cells exempt. Fits: yes, as part of D2.

## D6 — S146 `teaches` self-contradiction in its first-published cell

`corpus/SOURCES.md:152`, teaches cell. Three clauses conflict: (a) it faults S097 for citing S001 for
`psi.rst:42-43,57-58` "which belong to S090"; (b) it asserts "as a rejected row it stated no flip at all" —
false, because S097's teaches (`SOURCES.md:103`) opens `REJECTED: … flip: the same scope is documented by the
kernel PSI documentation (S001; …psi.rst lines 42-43 and 57-58)`, i.e. it states the very flip (a) faults;
(c) the same S146 cell then says the scope "are documented by the kernel documentation (S090, … lines 42-43 and
57-58 …; S001 is the rendered page)", citing S001 for the lines it just faulted S097 for citing.

```
$ git show 7118f320:corpus/SOURCES.md | awk -F'|' '/^\| S146 /{… teaches cell …}'   # (a),(b),(c) present
$ git show 7118f320:corpus/SOURCES.md | awk -F'|' '/^\| S097 /{… teaches cell …}'   # "REJECTED: … flip: …"
```

Smallest fix: the cell is immutable (`QUALITY.md:373-375`: "any other correction is a new row whose `teaches`
opens `supersedes S0NN —`"), so add one new row with that prefix, the corrected reading, its lesson line and a
Gate line from a re-opened URL. Fits: yes in work (~35 min) **except the id block**: round-29 C2 reserves
"S153 onward" (`contract.md:25-27`), so assign the correction's id at closure, above C2's allocation.

## D7 — ReviewReaderSweep F3: range citations still reach superseded rows

All four lines unchanged at `7118f320`; the ranges cover S101 and S140, whose live rows are S147 and S152.

```
$ git show 7118f320:corpus/knowledge/harness-job-capacity-r25.md | sed -n '3p;232p'  # "re-open S098–S103, S112–S113 and S138–S141"; "re-open S098–S103"
$ git show 7118f320:SKILL.md | sed -n '646p'                                          # "(sources S098–S104, S112–S113; …)"
$ git show 7118f320:PROVINCE.md | sed -n '318p'                                       # "sources opened this round are S098–S103 and S112–S113"
```

Smallest fix, four one-line rewrites:

```text
harness :3    re-open S098–S100, S102–S103, S112–S113 and S147, S152
harness :232  re-open S098–S100 and S102–S103
SKILL  :646   (sources S098–S100, S102–S104, S112–S113 and S147; …)
PROVINCE:318  sources opened in round 25 are S098–S100, S102–S103 and S112–S113 (`corpus/SOURCES.md:104-106,108-110,118-119`); the entry also rests on S147 (round 28)
```

Fits: yes, ~10 min, live readers only, no counter and no C1/C2 file.

## D8 — ReviewReaderSweep F4: "opened this round" misdates the new rows

`PROVINCE.md:257` calls S145 one of the sources "opened this round" inside the round-24 landing section; S145
was opened 2026-10-22T17:59:57Z in round 28 (`corpus/lessons/round-28.md:65`). The same shape at `:318` is real
but understated: the round-25 section lists only S098–S103/S112–S113 although the entry now rests on S147
(opened 17:59:03Z, lesson `:67`, named at `harness-job-capacity-r25.md:1`); the tip sentence does not name S147
at all. Open at `7118f320`:

```
$ git show 7118f320:PROVINCE.md | sed -n '255,258p'   # "(S090–S095, S145)" on :257
$ git show 7118f320:PROVINCE.md | sed -n '318p'
```

Smallest fix: two one-line edits — "…; S145 opened in round 28" at `:257`, and the S147 clause shown in D7 at
`:318`. Fits: yes, ~5 min.

## D9 — old rows' `used-by` cells

The eight superseded rows still name live knowledge files that no longer cite them; the round-28 lesson carries
the move explicitly (`corpus/lessons/round-28.md:88-90`). Word-match counts in the named file at `7118f320`:

```
$ for id in S096 S097 S101 S127 S128 S129 S131 S140; do git grep -c -w -F "$id" 7118f320 -- <used-by path>; done
S096/S097  system-pressure-r24.md -> 0        S128/S129/S131  oom-victim-selection-r27.md -> 0
S101/S140  harness-job-capacity-r25.md -> 0   S127  oom-victim-selection-r27.md -> 1, :204, "tsukuroi S115, S118, S120 and S127"
```

All eight are stale; S127's single hit is a sibling-lane id (ReviewReaderSweep's own exclusion). Smallest fix:
rewrite each cell to the history lessons that do carry the id (used-by is mutable, QUALITY 81):

```text
S096 -> corpus/lessons/round-24.md, corpus/lessons/round-28.md
S097 -> corpus/lessons/round-24.md, corpus/lessons/round-28.md
S101 -> corpus/lessons/round-25.md, corpus/lessons/round-28.md
S127 -> corpus/lessons/round-27.md, corpus/lessons/round-28.md
S128 -> corpus/lessons/round-27.md
S129 -> corpus/lessons/round-27.md
S131 -> corpus/lessons/round-27.md
S140 -> corpus/lessons/round-27.md
```

Candidate sets verified with `git grep -l -w -F <id> 7118f320 -- '*.md' ':!.ufo' ':!corpus/SOURCES.md'`; S128,
S129, S131 and S140 have no round-28 lesson hit, hence the shorter lists. Fits: yes, ~15 min, one line each, and
the counter's new-row used-by rule is untouched.

## D10 — r25 R1: false numbers and the probe corpus

Headline **closed** at `7118f320`: `_parse_config` (`tools/mori-job-runway.py:241-368`) returns `malformed` for
a quoted or spaced `async` key (`:297`), a key not written exactly `maxJobs:` (`:344`), a tab indent, a
document marker, a complex or merge key, an inline value, a quoted value and a block scalar; the fixture file
exists (24 cases, frozen with the round-25 contract) and its self-test passes:

```
$ python3 -I -B tools/mori-job-runway.py --selftest --cases tools/fixtures/mori-job-runway/supplementary-cases.json
MORI_JOB_RUNWAY_SELFTEST: PASS 24/24        exit=0
```

Residuals still open: (1) no regular-file guard — `_read_config_text` (`:221-238`) opens any path, so a FIFO
blocks and `/dev/zero` reads forever; (2) `--selftest --cases ""` silently runs the frozen cases —
`_resolve_cases` (`:517-521`) treats the empty string as no override; (3) `main` (`:666-687`) wraps only
argument parsing, so an uncaught exception exits 1, not 2. Smallest fix: three small edits in that file (stat
and require a regular file; reject empty `--cases`; wrap `evaluate` and return the unavailable code). Fits: yes,
~20 min, tools file only; a routed repair, not a claim — close only if a tool seat is free.

## D11 — r25 R5: gate conformance

- Registry rows: **closed** — `SKILL.md:717` registers `tools/mori-routed-r24.py`; `:718` registers the runway tool.
- Committed self-test for the routed check: **open** — the CLI declares only `--repo`, `--rev` and one further
  flag (`tools/mori-routed-r24.py:896-898`); the `selftest` hits in the file are D1's pressure rerun (`:398-422`).
- D1 constant compare: **open** — `EVIDENCE_COMMAND` (`:96`) and the expected PASS line (`:99`) are constants and
  the rerun is "reported only" (`:511`), so a forged PASS with a correct header passes.
- D5 positional columns: **open** — the Axes table is read positionally (`:664-666`, score `cells[1]`, last
  change `cells[-1]`).
- D3: the state R5 named is now disclosed — `corpus/lessons/round-24.md:100` appends the round-25 correction
  beside the `PASS 6/6` line at `:80`; whether the check rejects a stale line beside a correction was not
  re-read ([INFERENCE] unchanged). Missing-baseline exit code, promisor-clone writes, sub-directory `--repo`:
  not re-measured.

Smallest fix: `--selftest` with a small in-memory fixture set for the routed check (~45-60 min alone), then D1
(compare against a committed artefact checksum) and D5 (select columns by header name). Fits: **no**, over an
hour for the bundle; only the registry half was closable and it is done.

## Corrections to the carried list

1. F10's fix as written would red the real tree on S097's used-by; use the F2 raw immutable-cell compare and keep
   used-by exempt. F6 cannot use source-cell equality (S146, S149, S151, S152 legitimately differ); non-empty plus
   a Gate-URL prefix match passes the tip and kills f04/f08/f13.
2. r25 R1's headline is closed — three residuals remain. r25 R5's registry half is closed — the self-test and the
   D1/D5 fail-opens remain.
3. The S146 correction row collides with C2's reserved S153+ block; assign its id at closure.

## Verification gaps

- No fix was applied (detection and report only); every "fits one hour" is estimated from the code read. The
  round-28 counter was not executed; its behaviour is cited from `w1/MutCountC1.md` plus the source lines above.
- The only non-git command run was the runway self-test on committed fixture bytes; R5's D3 logic, the
  missing-baseline path, promisor-clone writes and sub-directory `--repo` were not re-read.
- ReviewReaderSweep's F5 (`systemd-system.conf.xml:305-306` vs `:305-307`) is not in the carried list and was not
  inventoried.

## Tooling

No installs, upgrades or system changes; no pacman transaction attempted (host-wide pause respected). Used git
2.56.0 (read-only `show`, `grep`, `log`, `rev-parse`), bash 5.3.20 and Python 3.14.8 (`python3 -I -B`), all pre-existing.
