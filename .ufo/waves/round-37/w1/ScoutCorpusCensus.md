# ScoutCorpusCensus — registry census (round 37)

Attacks: frontier claim that `corpus/SOURCES.md` is 225 rows with S221–S225 opened and `used-by` set. Acceptance gate: PASS iff row count is 225 and there is no duplicate id.

Tool installs: none.

## Pin

Measured file: `corpus/SOURCES.md` (worktree, clean vs HEAD).

| rev | commit | `corpus/SOURCES.md` blob |
|---|---|---|
| scored tip | `e57c58b57c025364e79d130fbdf764d2674d83d6` | `2dad136f61a199edb39fc4d1db241fe7afdbf605` |
| HEAD | `c31076ed85b3aadf2454637747343e0ab97eb58f` | `2dad136f61a199edb39fc4d1db241fe7afdbf605` |
| entering tip | `842a32074b5c7972e9728f3f629d83eb92f127c2` | `793ca8fcd2cb812fad7b14c93b68dccb86844d70` |

Worktree sha256: `f65bd84d72ffe07019fe7a3e2b335a2afc67df6aa85e25251c8f2195e0cb1c8e`. `git diff --stat e57c58b… HEAD -- corpus/SOURCES.md` empty. Census below is the scored-tip registry, not the entering tip.

Parser: CORPUS.md SOURCES contract v1 (`CORPUS.md:134-147`): a row is `^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|`, 11 cells ⇒ `NF==13`, tier `$5`, status `$9`, id `$2`, used-by `$12`. Not an LSP query; the contract is a textual table. No language server was asked.

## Commands and outputs

Cwd: `/home/vgpnk/Projects/shokunin/mori-shokunin`.

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
```
```
225
```

```
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
```
```
0
```

```
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d\n", k, n[k]}' corpus/SOURCES.md | sort
```
```
mined=176
queued=25
rejected=24
```
Sum 176+25+24=225.

```
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d\n", k, n[k]}' corpus/SOURCES.md | sort
```
```
A=200
B=8
C=17
```
Sum 200+8+17=225.

```
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
```
```
(no output)
```
Unique id count: 225. Set difference against `S001`–`S225`: missing `[]`, extra `[]`.

Independent Python split (`line.split('|')[1:-1]`, 11 cells) on the same file: `nrows 225`, `nf_bad 0`, `status {'mined': 176, 'queued': 25, 'rejected': 24}`, `tier {'A': 200, 'B': 8, 'C': 17}`, `dups []`.

Enum check (CORPUS.md:145, kind/tier/status/tier-inflation): no output.

A first status awk printed `mined=queued=rejected=176`. That was `n[s]` (last bucket) instead of `n[k]`. Discarded. The command above and the Python split agree.

## Five new rows — `used-by` resolves

Delta vs entering tip `842a320` (blob `793ca8fc`, 220 rows, ids through S220, 0 duplicate ids, status mined=171 queued=25 rejected=24, tier A=196 B=7 C=17): only scored-tip extras are S221–S225. Entering tip has no id the scored tip lacks.

| id | line | kind | tier | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|
| S221 | `corpus/SOURCES.md:227` | spec | A | mined | 2026-10-23 | 180d | `corpus/knowledge/source-drift-hardening-r37.md` |
| S222 | `corpus/SOURCES.md:228` | docs | B | mined | 2026-10-23 | 180d | same |
| S223 | `corpus/SOURCES.md:229` | docs | A | mined | 2026-10-23 | 180d | same |
| S224 | `corpus/SOURCES.md:230` | docs | A | mined | 2026-10-23 | on-release | same |
| S225 | `corpus/SOURCES.md:231` | spec | A | mined | 2026-10-23 | 90d | same |

```
test -f corpus/knowledge/source-drift-hardening-r37.md → exists, size 5854
```
Absolute path `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/source-drift-hardening-r37.md` is a regular file. The note's `source:` cites S221–S225 (`corpus/knowledge/source-drift-hardening-r37.md:3-6`).

Contract mined-path sweep (CORPUS.md:147, every mined `used-by` token except `—`): no `missing:` lines.

`opened=2026-10-23` is not unique to these five (S175–S225 share that date). "New this round" is the id-set delta vs the entering tip, not the opened date.

## Facts / inference / gaps

- Observed: 225 rows, contiguous S001–S225, no duplicate id, histograms sum to 225, malformed 0, enum check empty, S221–S225 `used-by` is one existing file.
- [INFERENCE] W04 same-URL-across-scopes warnings in `evidence/census-end.txt` are not duplicate ids. This seat did not re-run `scripts/sources-census.sh`.
- Unresolved: none for the acceptance gate.

VERDICT: PASS
