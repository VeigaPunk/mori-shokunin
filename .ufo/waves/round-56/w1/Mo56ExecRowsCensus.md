# Mo56ExecRowsCensus — registry mechanical validation at the round-56 freeze tip

Seat: Mo56ExecRowsCensus (executor, lane `mori-shokunin`).
Measured revision: `8be2717b0809281d07dffe83dad424a4859e0747` (freeze-receipt commit).
Entering tip (for the before→after pair): `5b295eeebd87ebd610d8d39bfe2035742f740cfa`.
Registry bytes measured: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 8be2717b0809281d07dffe83dad424a4859e0747:corpus/SOURCES.md`
(sha256 `6cf5c51592e8b8e69d50a46d2ff8bfcc9f32873c4e25d10e565c615d60dd7686`, 296 335 bytes, 391 lines — byte-identical to the working-tree file and to `HEAD:corpus/SOURCES.md`).
Scratch (removed at exit): `/fast/scratch/hyaku/mori-r56/Mo56ExecRowsCensus/` — a `git archive` extraction of the freeze revision plus a `git archive` extraction of the entering tip; no clone, no mirror, no fixture repo, no commit anywhere.

All six manual census commands of `CORPUS.md` §"SOURCES.md — where a shokunin learns" were run **verbatim** over the freeze-tip bytes. Outputs are pasted below in the order the contract gives them.

## 1. Row count (spacing-tolerant)

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' tmp/fz.md
318
```

`318` = entering-tip `316` + `S544` + `S545`. Cross-check by the maintained validator (row-count-bearing mode):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --today 2026-10-27 /home/vgpnk/Projects/shokunin/mori-shokunin
mori-shokunin	rows	318
mori-shokunin	tier.A	287
mori-shokunin	tier.B	14
mori-shokunin	tier.C	17
mori-shokunin	status.mined	267
mori-shokunin	status.queued	24
mori-shokunin	status.rejected	27
FLEET	rows	318
FLEET	tier.A	287
FLEET	tier.B	14
FLEET	tier.C	17
FLEET	tier.invalid	0
FLEET	status.queued	24
FLEET	status.mined	267
FLEET	status.rejected	27
FLEET	status.invalid	0
FLEET	missing	0
exit=0
```

Entering tip, same command over the extracted entering-tip tree (the before→after pair):

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --today 2026-10-27 tmp/entering
entering	rows	316
entering	tier.A	285
entering	tier.B	14
entering	tier.C	17
entering	status.mined	265
entering	status.queued	24
entering	status.rejected	27
exit=0
```

Delta entering→freeze: `+2` rows, `+2` tier-A, `+2` mined. Only two row lines changed, both additions (no removals):

```
$ git diff --numstat 5b295eeebd87ebd610d8d39bfe2035742f740cfa 8be2717b0809281d07dffe83dad424a4859e0747 -- corpus/SOURCES.md
2	0	corpus/SOURCES.md
```

## 2. Malformed rows (NF!=13) — expecting 0

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' tmp/fz.md
0
```

No NF!=13 detail rows. Widened to any S-id shape (2+ digits) and to any `^|` line: still 0 malformed; the only non-row `|` lines are the header and the `|---|` separator.

## 3. Tier histogram

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' tmp/fz.md
A=287 B=14 C=17
```

## 4. Status histogram

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' tmp/fz.md
mined=267 queued=24 rejected=27
```

## 5. Duplicate ids — expecting nothing

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' tmp/fz.md | sort | uniq -d
```

(empty output, exit 0)

## 6. Enum violations and tier inflation — expecting nothing

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' tmp/fz.md
```

(empty output, exit 0)

## 7. Mined rows whose used-by paths do not exist — expecting nothing

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' tmp/fz.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
```

(empty output, exit 0)

The same check was run three more ways, all empty: against the **freeze revision tree** rather than the working tree (`git cat-file -e 8be2717b…:<path>` for every mined used-by path — no path missing at the measured revision, so the result is not an artifact of uncommitted files); against **all statuses** (not only `mined`); and with the maintained validator's `E11` arm (no `E11` emitted). Three `rejected`/`queued` rows carry a non-`—` used-by path (`S065`, `S097`, `S211`) — all three paths exist.

No `queued`/`mined`/`rejected` row has used-by `—` (the W03 class), no tier-C mined row carries a non-`—` used-by (W01), no thin rejected row (W02), and no row-shaped line sits outside the `## Registry` section (E12). The maintained validator over the freeze-tip tree emits **only** `23 × W04` plus `ok` — no `E0x`/`E1x` code at all.

## 8. The 23 W04-class duplicate URLs are unchanged

Expected by the seat brief: 23 W04-class duplicates unchanged. Measured:

- W04 count at the entering tip: `23`; at the freeze tip: `23`.
- The W04 **sets are identical**: normalising away the lane-prefix column, the entering-tip and freeze-tip validator outputs differ only in the trailing `ok <path>` line (path differs because the entering run used the scratch extraction).
- Every one of the 23 receipt lines' URL is a substring of that row's `source` cell in the registry (checked one by one — all 23 OK, no mismatch).

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-27 /home/vgpnk/Projects/shokunin/mori-shokunin | cut -f2 | sort | uniq -c
     23 W04
      1 ok
exit=0
```

## 9. Committed receipt `evidence/census-start.txt` — byte reproduction

The committed receipt is a **direct capture** and reproduces byte-for-byte against a fresh run of the same command:

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin --today 2026-10-27 mori > tmp/repro-mori.txt 2>&1; echo "exit=$?"
exit=0
$ grep -E '^mori\b' tmp/repro-mori.txt > tmp/repro-mori-only.txt
$ grep -E '^mori\b' .ufo/waves/round-56/evidence/census-start.txt > tmp/committed-mori-only.txt
$ diff tmp/repro-mori-only.txt tmp/committed-mori-only.txt && echo "BYTE-IDENTICAL to committed census-start.txt"
BYTE-IDENTICAL to committed census-start.txt
```

The receipt ends `exit=0` and uses tab separators throughout (`cat -A` shows `mori^IW04^I…`), so it is a captured byte stream, not a retyped table — QUALITY 152's byte form is satisfied for the 23 W04 lines. What it does **not** contain is a row count (see finding F1).

## 10. The two new rows, read at the freeze tip

```
$ git show 8be2717b…:corpus/SOURCES.md | grep -nE '^\|[[:space:]]*S(544|545)[[:space:]]*\|'
324:| S544 | shokunin driver launch-log grammar — scripts/hyaku/inline.sh and scripts/shokunin-watchdog.sh in the fleet repo | own-work | A | the .ufo/watchdog.log line grammar under the hyaku-inline and legacy daemon drivers | inline.sh launch 149, complete 176, dead 182; shokunin-watchdog.sh launch 266, complete 405, dead 448; extract corpus/evidence/sources-r56/watchdog-log-grammar.txt, sha256 38ba3e6b309e17d3d8038e8986e274bb363ac893d1c325fe145a95882a417796 | The writer source per launch/complete/dead/wrap line shape; the probe grammar is frozen from it | mined | 2026-10-27 | on-release | corpus/knowledge/driver-liveness-r56.md, tools/mori-driver-liveness.py |
325:| S545 | RFC 8259 The JavaScript Object Notation (JSON) Data Interchange Format — https://www.rfc-editor.org/rfc/rfc8259.txt | spec | A | the JSON grammar a seat output may take (a JSON text is one serialized value; a string is quotation-mark *char quotation-mark) | section 1 line 251, section 2 grammar lines 308 and 461; sha256 61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7; copy corpus/evidence/sources-r56/rfc8259.txt | A JSON-wrapped vote binds as a string scalar whose stripped content is the anchored vote line, not as a substring | mined | 2026-10-27 | on-release | corpus/knowledge/vote-binding-r56.md, tools/mori-vote-bind.py |
```

Both rows satisfy the frozen counter predicates (`status mined`, `opened 2026-10-27`, used-by naming the entry). Re-running the frozen counters at the freeze tip (read-only, `git show`/`ls-tree` only):

```
$ python3 .ufo/waves/round-56/count-c1.py 8be2717b0809281d07dffe83dad424a4859e0747 --repo /home/vgpnk/Projects/shokunin/mori-shokunin
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
exit=0
$ python3 .ufo/waves/round-56/count-c2.py 8be2717b0809281d07dffe83dad424a4859e0747 --repo /home/vgpnk/Projects/shokunin/mori-shokunin
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
exit=0
```

### 10a. The S544 pinned extract, byte-verified against the fleet writers

`corpus/evidence/sources-r56/watchdog-log-grammar.txt` (6 lines, sha256 `38ba3e6b…` as pinned in `evidence/freeze-sha256.txt`) was compared line-by-line against the live fleet-repo sources at fleet HEAD `666bc1efcddd4b711173f23def3278cfe54a418f` (both scripts last modified in `5f4fa8d8`, 2026-10-25, working tree clean):

```
OK   inline.sh:149 (src line 149 == extract line 1)
OK   inline.sh:176 (src line 176 == extract line 2)
OK   inline.sh:182 (src line 182 == extract line 3)
OK   watchdog.sh:266 (src line 266 == extract line 4)
OK   watchdog.sh:405 (src line 405 == extract line 5)
OK   watchdog.sh:448 (src line 448 == extract line 6)
```

The six anchor line numbers in the S544 anchor cell are all correct against the fleet sources.

### 10b. The S545 pinned copy, byte-verified against upstream

```
$ curl -sS --max-time 45 -o rfc8259-upstream.txt https://www.rfc-editor.org/rfc/rfc8259.txt ; sha256sum rfc8259-upstream.txt
61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7  rfc8259-upstream.txt
$ cmp rfc8259-upstream.txt corpus/evidence/sources-r56/rfc8259.txt && echo "BYTE-IDENTICAL to upstream"
BYTE-IDENTICAL to upstream
```

sha256 matches the pin in `evidence/freeze-sha256.txt`. The cited line numbers exist and carry the quoted text:

```
$ sed -n '251p;308p;461p' corpus/evidence/sources-r56/rfc8259.txt
   A JSON text is a serialized value.  Note that certain previous
      value = false / null / true / object / array / number / string
      string = quotation-mark *char quotation-mark
```

The section labels attached to those lines are not correct (finding F2).

## 11. Other registry-surface checks run at the freeze tip

- **E12-style**: no row-shaped line (`^| S…`) appears outside `## Registry` (headings: `## Registry` :3, `## Paths` :327, `## Search log` :337, `## Leads (unopened)` :382).
- **Parser divergence**: the maintained parser accepts 0–3 leading ASCII spaces before a Markdown row; the frozen manual examples assume column zero. The freeze-tip file has **0** indented rows (`grep -cE '^[[:space:]]+\|'` = 0), so manual and maintained row counts agree exactly (318 = 318).
- **Id space**: highest id is `S545`; no 1- or 2-digit ids exist, so the `S[0-9]{3,}` row regex misses nothing.
- **Id continuity**: ids are `S001…S545` with no gap and no reuse (duplicates check empty; `S544`/`S545` are the only additions).
- **Lane-repo relocation**: no `used-by` path points outside the lane repo except three that name `SKILL.md` (a lane-root file) — all resolve.

## Findings

| id | severity | file / line | finding |
|---|---|---|---|
| F1 | HIGH | `.ufo/waves/round-56/evidence/census-start.txt` (25 lines) and `.ufo/waves/round-56/contract.md:70` | The round-start census receipt carries **no row count**: `grep -c 'rows' .ufo/waves/round-56/evidence/census-start.txt` = `0`, and validate-mode output never prints one (it emits only `W04`/`ok`/`exit`). The contract's parenthetical "`evidence/census-start.txt` (exit 0, **316 rows**, 23 W04)" and the working-tree `LOG.md` round-56 line ("census start rc 0, **316 rows**, 23 W04 (`evidence/census-start.txt`)") attach a number to a receipt that does not contain it — the QUALITY-152 / round-55-routed-defect-1 "retyped summary" class, in the very receipt the round's own `## Mistakes` table claims to have fixed. The receipt is also the **only** census artefact committed for round 56 and it carries **no `rev=` stamp** (unlike `c1-at-freeze.txt`/`c2-at-freeze.txt`/`c2-old-counter-voted0.txt`, which stamp `rev=`), so nothing in committed bytes binds it to a measured revision; and because the W04 set is byte-identical before and after the `S544`/`S545` append, the receipt cannot distinguish a 316-row from a 318-row registry either. Routed item for round 57 (the contract and counters are frozen and are **not** to be changed): capture the row-count-bearing `census` mode output (it prints `mori rows N`) as the census receipt, or paste `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` next to the receipt, and stamp the measured revision on it. |
| F2 | MED | `corpus/SOURCES.md:325` (S545 anchor cell) and `corpus/knowledge/vote-binding-r56.md:31-33` | The S545 anchor cell reads "section 1 line 251, section 2 grammar lines 308 and 461". Measured against the pinned copy (byte-identical to upstream RFC 8259), the section boundaries are `1. Introduction` :147, `2. JSON Grammar` :246, `3. Values` :296, `7. Strings` :424 — so line 251 is in **§2**, line 308 in **§3**, line 461 in **§7**. All three section labels are off; the line numbers and the quoted text are correct. The same mislabels are propagated into the entry prose ("S545 §1, line 251", "S545 §2 grammar, line 308", "S545 §2, line 461"). SOURCES-contract v1 requires the anchor to name the exact section **and** line, so the anchor cell as written mislocates all three citations. Data correction the L1 may make (the anchor cell is data, not a frozen counter); re-pin consequences are the L1's to weigh. |
| F3 | MED | `corpus/SOURCES.md:324` (S544 anchor cell) vs `tools/mori-driver-liveness.py:24-25` and `corpus/knowledge/driver-liveness-r56.md:38,40` | The frozen grammar the C1 probe parses includes `launch-fail` and `wrap` shapes, and both the tool docstring and the entry attribute them to S544 (`shokunin-watchdog.sh:241-249`, `shokunin-watchdog.sh:398`). The S544 anchor cell names only six line numbers (inline.sh 149/176/182, watchdog 266/405/448) and the pinned extract `corpus/evidence/sources-r56/watchdog-log-grammar.txt` contains no `launch-fail` and no `wrap` line (`grep -cE 'wrap\|launch-fail'` = 0), so two of the five parsed event shapes are not covered by the row's anchor or by its pinned bytes. The fleet sources do contain them (watchdog.sh `:241`, `:242`, `:245`, `:249` `launch-fail`, `:398` `wrap`), so the underlying claim is true against the fleet repo — the registry anchor and the pinned copy are what under-cover it. |
| F4 | MED | `corpus/SOURCES.md:324` (S544 anchor cell) | The anchor cites line numbers of **fleet-repo** files (`scripts/hyaku/inline.sh`, `scripts/shokunin-watchdog.sh`) with no revision for that repo (fleet HEAD at measurement `666bc1efcddd4b711173f23def3278cfe54a418f`; those two scripts last changed in `5f4fa8d8`). SOURCES-contract v1 requires "exact section / heading / page / line **plus revision** (version, commit, or publication date)". The sha256 in the cell pins the lane-local extract, not the fleet scripts those line numbers refer to, so the citation is not anchored against line drift in the writer scripts. |
| F5 | MED | `corpus/README.md` (coverage map / `## Frontier` :345) | The round added two knowledge entries but no index row for either: `grep -nE 'driver-liveness-r56\|vote-binding-r56' corpus/README.md` → exit 1 (no match). Every other r50+ entry (`kernel-v7.3-recheck-r55.md`, `disk-runway-enospc-r55.md`, `memory-failure-kills-r54.md`, `oom-memcg-stat-r50.md`, …) has a README row, and `corpus/README.md` is the corpus index whose "an index row is a claim" rule the corpus contract states. The `FR5` frontier row still reads that reading the driver's `launch`/`complete` lines is "open coverage ground" (`corpus/README.md:345`) although round-56's C1 lands exactly that ground (`corpus/knowledge/driver-liveness-r56.md` names FR5 in its `coverage-map:` line). No round-56 commit touched `corpus/README.md` (`git log 5b295eee..8be2717b -- corpus/README.md` is empty). Data the L1 may add; not a counter change. |
| F6 | LOW | `corpus/SOURCES.md` §"Search log" (:337-391) | SOURCES-contract v1 rule 5 asks for "one prose note per bounded search". There is no search-log note for round 54, round 55 or round 56; the last notes are `Round 53 bounded search` (:377) and `Round 53 bounded search, integration addendum` (:378), plus the round-37/38/39/46 notes. Round 56 opened two new sources (`S544`, `S545`) with no bounded-search note, and rounds 54–55 opened 18 rows likewise without one — a pre-existing gap this round continues rather than introduces. Routed item for round 57. |
| F7 | LOW | `corpus/evidence/README.md` (78 index rows) | The two new pinned copies (`corpus/evidence/sources-r56/rfc8259.txt`, `corpus/evidence/sources-r56/watchdog-log-grammar.txt`) have no row in the evidence index, while `corpus/evidence/sources-r5*` and the r5x evidence files are indexed there. Low impact (the copies are pinned by sha256 in `evidence/freeze-sha256.txt` and named in the S545/S544 anchor cells), but the evidence index is the place a reader looks for what a copy is. Routed item for round 57. |

### Not defects — verified clean

- No duplicate id, no malformed row, no enum violation, no tier inflation, no missing used-by path, no row outside `## Registry`, no W01/W02/W03 class finding, no `E0x`/`E1x` code from the maintained validator.
- The 23 W04 duplicate-URL warnings are unchanged entering→freeze and every receipt URL matches its registry row.
- The committed census receipt is a genuine byte capture that reproduces byte-for-byte.
- The `S544` extract is byte-identical to the cited fleet-writer lines; the `S545` copy is byte-identical to upstream RFC 8259.
- The two new rows satisfy the frozen counter predicates and both frozen counters re-run green at the freeze tip.

### Open / not verified here

- `evidence/census-end.txt` for round 56 does not exist at the freeze tip (rounds 29–55 each have one). The contract requires the end census to exit 0; that is a round-close obligation for the L1, not a freeze-tip defect — but it is the receipt that would carry the "after" row count and would close F1's before→after pair.
- Whether the round-56 report (`.ufo/reports/round-56/`) will carry the counting command output — no round-56 report file exists at the freeze tip (`ls .ufo/reports/round-56/` → no such directory), so the F1 fix point is not yet observable from committed bytes.
- The live-log receipt `evidence/driver-liveness-live.txt` reads `/home/vgpnk/Projects/shokunin/.ufo/watchdog.log` — a gitignored, uncommitted path (`git check-ignore` → `.gitignore:10:.ufo/watchdog.log`); the log now holds 1 730 lines against the 1 728 read at capture. That receipt is therefore a point-in-time observation, not a reproducible artefact — noted for the L1's report, outside this seat's registry scope.

### Reproduction recipe used

```sh
S=/fast/scratch/hyaku/mori-r56/Mo56ExecRowsCensus
mkdir -p "$S/tmp" && export TMPDIR="$S/tmp"
git -C /home/vgpnk/Projects/shokunin/mori-shokunin archive 8be2717b0809281d07dffe83dad424a4859e0747 | tar -x -C "$S"
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 8be2717b0809281d07dffe83dad424a4859e0747:corpus/SOURCES.md > "$S/tmp/fz.md"
cd "$S"   # then the six CORPUS.md commands, verbatim, over tmp/fz.md
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin --today 2026-10-27 mori
```

Scratch removed on exit (`rm -rf /fast/scratch/hyaku/mori-r56/Mo56ExecRowsCensus`); every byte cited above is either reproduced by a command in this report or committed at the measured revision. No file in `/home/vgpnk/Projects/shokunin/mori-shokunin` was written except this report; no git or jj command mutated the lane or the fleet repo.
