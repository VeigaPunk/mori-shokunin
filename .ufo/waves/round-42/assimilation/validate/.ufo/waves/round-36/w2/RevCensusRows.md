# RevCensusRows — SOURCES.md census self-check at the tip

Seat: `mori-r36-w2-RevCensusRows-23` (reviewer, UFO-FSD, leaf — no subagent dispatch)
Attack: `corpus/SOURCES.md` at `bf0df77fee4b6ef54a90aea09335c7617f125151` — frozen census from `CORPUS.md` (SOURCES.md contract v1, section "Census").
Date: 2026-10-23. Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.

## Identity of the measured artifact

- `git rev-parse HEAD` = `bf0df77fee4b6ef54a90aea09335c7617f125151` = the round data tip.
- `corpus/SOURCES.md` is NOT among the 15 dirty working-tree entries; `git diff HEAD --stat` shows no `corpus/SOURCES.md` change.
- `git show bf0df77:corpus/SOURCES.md > /fast/scratch/hyaku/mori-r36/mori-r36-w2-RevCensusRows-23/SOURCES.md@bf0df77` then
  `cmp` against working-tree `corpus/SOURCES.md` → identical (`WORKING-TREE-MATCHES-TIP`, rc=0). Census below therefore applies exactly to the tip blob.
- Working tree file: 277 lines.

## Frozen census commands and outputs (run verbatim from CORPUS.md, at lane root)

All commands executed with `cd /home/vgpnk/Projects/shokunin/mori-shokunin`; `F=corpus/SOURCES.md`.

### CMD1 — rows (expect 220)
```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
220
rc=0
```

### CMD2 — malformed rows (must print 0)
```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
rc=0
```

### CMD3 — tier histogram
```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
A=196 B=7 C=17 
rc=0
```
Sum = 220, consistent with CMD1.

### CMD4 — status histogram
```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
mined=171 queued=25 rejected=24 
rc=0
```
Sum = 220, consistent with CMD1.

### CMD5 — duplicate ids (must print nothing)
```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
(no output)
rc=0
```

### CMD6 — enum violations and tier inflation (must print nothing)
```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md
(no output)
rc=0
```

### CMD7 — mined rows whose used-by paths do not exist (must print nothing)
```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
(no output)
rc=0
```

## Supplementary probes (review diligence, same table/commands as frozen)

1. Mined rows with empty or `—` used-by (contract: mined ⇒ cited by ≥1 path):
   ```
   $ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; u=$12; gsub(/[[:space:]]/,"",s); gsub(/^[[:space:]]+|[[:space:]]+$/,"",u); if (s=="mined" && (u=="" || u=="—")) print $2, "used-by=[" u "]"}' corpus/SOURCES.md
   (no output) rc=0
   ```
2. Mined rows by used-by path count (sum must equal 171):
   ```
   1 119
   2 35
   3 7
   4 5
   5 4
   6 1
   ```
   Total = 119+35+7+5+4+1 = 171 = CMD4 mined count. Consistent.
3. Routed round-35 repair rows S205–S220 present, ids unique, teaches carry `supersedes S0NN —`; statuses: S205–S210, S212–S220 mined; S211 rejected (teaches `supersedes S179 — Rejected round 32: duplicate URL already …`). No census violation.

## Tooling installs

None. No tools installed/upgraded this seat.

## VERDICT

**PASS** — no defect found in `corpus/SOURCES.md` at `bf0df77fee4b6ef54a90aea09335c7617f125151`.

Census self-check summary: rows=220 (expect 220), malformed=0, tier A=196/B=7/C=17, status mined=171/queued=25/rejected=24, duplicates=none, enum/tier-inflation violations=none, mined used-by missing paths=none. Every frozen command exited 0 where 0 is required. Working-tree file verified byte-identical to the tip blob.

Residual risk / verification gaps: frozen census covers table shape and used-by path existence, not whether cited `knowledge/` entries actually reference the mined rows back (directionality of `used-by`); that is outside this seat's census scope. No actionable finding remains in scope.
