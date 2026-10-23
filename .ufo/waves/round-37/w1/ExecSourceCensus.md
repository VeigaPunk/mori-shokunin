# ExecSourceCensus — SOURCES registry census (r37, W1)

Seat: `mori-r37-w1-ExecSourceCensus` (leaf). Lane repo read-only; no lane file edited,
no VCS command run, no install performed.

**What this attacks:** the integrity of the `corpus/SOURCES.md` registry at the scored tip —
that the four frozen-contract census commands in `/home/vgpnk/Projects/shokunin/CORPUS.md`
(SOURCES contract v1, "Census — run from the lane root") are clean *over the exact scored
content*, and that each such command is capable of failing (red-before), so the clean result
is not vacuous.

## Subject pin

Census target: `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`

```
$ cd /home/vgpnk/Projects/shokunin/mori-shokunin
$ git rev-parse e57c58b57c025364e79d130fbdf764d2674d83d6:corpus/SOURCES.md
2dad136f61a199edb39fc4d1db241fe7afdbf605
$ git hash-object corpus/SOURCES.md
2dad136f61a199edb39fc4d1db241fe7afdbf605
$ sha256sum corpus/SOURCES.md
f65bd84d72ffe07019fe7a3e2b335a2afc67df6aa85e25251c8f2195e0cb1c8e  corpus/SOURCES.md
```

The worktree blob equals the scored-tip blob (`2dad136…`), so the census below measures the
scored content, not a drifted working copy. `git status --porcelain corpus/SOURCES.md` → empty.

## The five required outputs (verbatim)

All commands run from the lane root, exactly as written in `CORPUS.md`.

**1. Row count**
```sh
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
```
```
225
```

**2. Malformed rows (NF!=13) — must print 0**
```sh
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
```
```
0
```

**3. Duplicate ids — must print nothing**
```sh
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
```
```
```
(empty — no duplicate ids)

**4. Enum violations and tier inflation — must print nothing**
```sh
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md
```
```
```
(empty — no tier/status/kind violations, no community-at-tier-A)

**5. Status histogram**
```sh
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
```
```
mined=176 queued=25 rejected=24 
```

Totals reconcile: 176 + 25 + 24 = 225 = row count.

## Supplementary contract census (also clean)

Tier histogram:
```
A=200 B=8 C=17 
```
200 + 8 + 17 = 225.

Mined rows whose `used-by` paths do not exist on disk (contract's seventh census line),
run from the lane root so relative paths resolve:
```sh
awk -F'|' '...' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
```
```
```
(empty — every mined row's `used-by` path exists)

Structural checks:
- id width: all 225 ids are `S` + 3 digits (length 4); first `S001`, last `S225`.
- id sequence: contiguous `S001…S225`, zero gaps.
- frontier rows `S221`–`S225`: all 5 present.
- rows inside `## Registry` (lines 3–232): 225. Rows shaped like S-rows outside the
  Registry section (contract E12 class): 0.
- no leading-whitespace-indented S-rows (maintained-parser indentation class): 0.

## Independent cross-check: maintained fleet CLI

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census /home/vgpnk/Projects/shokunin/mori-shokunin
mori-shokunin	rows	225
mori-shokunin	tier.A	200
mori-shokunin	tier.B	8
mori-shokunin	tier.C	17
mori-shokunin	status.mined	176
mori-shokunin	status.queued	25
mori-shokunin	status.rejected	24
FLEET	rows	225
FLEET	tier.A	200
FLEET	tier.B	8
FLEET	tier.C	17
FLEET	tier.invalid	0
FLEET	status.queued	25
FLEET	status.mined	176
FLEET	status.rejected	24
FLEET	status.invalid	0
FLEET	missing	0
census exit=0
```

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-23 /home/vgpnk/Projects/shokunin/mori-shokunin
...
mori-shokunin	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
exit=0
```

Validate verdict: `ok`, exit 0, **zero E-codes** (E01 malformed, E02 id grammar, E03 duplicate
id, E04 duplicate URL+scope, E05 kind, E06 tier, E07 status, E08 opened date, E09 recheck,
E10 community-at-A, E11 dangling used-by, E12 row outside Registry — all absent). 15 × `W04`
(duplicate URL across differing scopes) are warning-class by the CLI's own contract and do not
change clean status. Independent parser agrees with the frozen manual census on every number.

## Red-before controls (frozen commands are not vacuous)

Lane file untouched; mutants are copies under
`/fast/scratch/hyaku/mori-r37/ExecSourceCensus/` (each a copy of the pinned blob, sha256
`f65bd84d…` before mutation).

| Mutant | Delta | Command | Observed |
|---|---|---|---|
| `mut-rows.md` | append one well-formed `S226` row | row count | `226` (real: 225) |
| `mut-malformed.md` | delete the `anchor` cell of `S001` (NF 13→12) | malformed | `1` (real: 0) |
| `mut-dup.md` | duplicate the byte-identical `S042` row | duplicate ids | `S042` (real: empty) |
| `mut-enum.md` | `S001` kind→`website`; `S005` status→`watch`; `S021` tier→`D`; `S030` community→tier `A` | enum/tier-inflation | `kind S001 website`, `status S005 watch`, `tier S021 D`, `tier-inflation S030` (real: empty) |
| `mut-usedby.md` | `S002` used-by→`corpus/knowledge/does-not-exist-r37.md`, checked from lane root | used-by existence | `missing: corpus/knowledge/does-not-exist-r37.md` (real: empty) |

Maintained CLI on the same mutants (correct lane-root resolution, true exit status captured):
```
mut-malformed-shokunin  exit=1  E01(S001 fields=10)
mut-dup-shokunin        exit=1  E03(S042 duplicate id) E04(S042 duplicate url …)
mut-enum-shokunin       exit=1  E05(S001 kind=website) E07(S005 status=watch) E06(S021 tier=D) E10(S030 community-at-A)
```
Both the frozen manual commands and the maintained CLI detect each injected defect, so the
clean result on the real registry is measured, not vacuous.

Process note (recorded, not a lane defect): an earlier cross-check ran the maintained CLI with
`. ` from a scratch cwd, which produced a spurious E11 flood against paths resolved outside the
lane; re-run with the explicit lane path it returns `ok`, exit 0, zero E-codes. The frozen
used-by command is likewise cwd-sensitive and was run from the lane root for the retained result.

## Risks / observations

1. **15 × W04 duplicate-URL-across-scopes warnings** (e.g. `S035`, `S037`, `S073`–`S076`,
   `S147`–`S150`, `S166`, `S168`, `S201`, `S218`, `S220`). Contract-sanctioned (different
   scopes may legitimately share a source), do not affect clean status, but they are the only
   non-`ok` output from validate. Not a violation.
2. The frozen census regexes are column-zero-only. The registry currently has zero indented
   S-rows, so the maintained parser's 1–3-space tolerance changes no count today; a future
   indented row would silently undercount under the frozen command while the maintained CLI
   would still see it.
3. No tool installs or upgrades were performed; nothing to record.

## Acceptance

- malformed = 0 ✓
- duplicate ids: none ✓
- enum violations / tier inflation: none ✓
- all five outputs pasted above ✓

VERDICT: PASS
