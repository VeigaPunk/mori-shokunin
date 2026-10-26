# Mo49ExecCensusMirror — w1 (round 49, mori lane)

Seat: `Mo49ExecCensusMirror`, executor, leaf (no dispatch; no subagents used).
Scope: build the scratch mirror-validation harness that the round prompt's assimilation contract
(`/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-49.md` §10, *Scratch transformation and validation,
before any append*), prove it can pass and can fail, re-run the id-collision guard on the live files, list
the fourteen collisions, and record the renumber-by-document map with each staged row's URL checked
against it.

Lane worktree at the time of writing: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD`
= `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115` (the freeze commit); the entering tip
`b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86` is an ancestor
(`git merge-base --is-ancestor b3e3453d… HEAD` → exit 0). No git or jj mutation was run. Files written:
this report and `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecCensusMirror/` only
(`git status --porcelain` shows my entries only under `.scratch/`; nothing in `corpus/`, `tools/`,
`SKILL.md`, `SOURCES.md`, `LOG.md`, `SCORECARD.md`, or the frozen `.ufo/waves/round-49/` files).

## 1. Deliverable — `mirror-validate.sh`

- Path: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecCensusMirror/mirror-validate.sh`
- 158 lines, executable; `sha256sum` = `0432c8ce4e39906daf984786def882a39d7da368aabd8c2fccf1937fc391861a`
  (`bash -n` clean).
- Interface: `mirror-validate.sh <rows-file> <entry-file> [evidence-path ...]`
  - `rows-file` — the census-schema registry rows (11 columns each) that would be appended;
  - `entry-file` — the admitted entry, placed at `corpus/knowledge/journal-reach-r49.md` in the copy;
  - `evidence-path` — optional file/dir copied to `corpus/evidence/sources-r49/` in the copy.
- Env: `MIRROR_LANE` (default the mori lane), `MIRROR_DIR` (default `$TMPDIR/mirror`; refuses to run
  without `MIRROR_DIR`/`TMPDIR`, so nothing lands in `/tmp`), `CENSUS_BIN`.
- Steps: (1) copy `<lane>/corpus` into a fresh mirror; (2) insert the rows at the end of the `## Registry`
  table of the copied `corpus/SOURCES.md`; (3) place the entry at its repo-relative path; (4) copy any
  evidence paths; (4b) symlink (read-only) the used-by targets that live outside `corpus/` — rationale and
  evidence in §4; (5) run
  `sources-census.sh validate --file <mirror>/corpus/SOURCES.md`, print `MIRROR/ROWS/ENTRY/CMD`, the census
  output verbatim, `EXIT=<rc>`, and exit with that rc.
- Fail-closed paths: missing rows/entry/lane/census → exit 3 with a named reason; rows file with no
  non-blank row → exit 3; no `## Registry` header → exit 3; `gawk` absent → exit 3.
- No write path touches the lane: the only lane reads are `cp -a corpus` and `ln -s` targets.

```bash
#!/usr/bin/env bash
# mirror-validate.sh — scratch mirror gate for a registry append (round 49, C2 assimilation).
#
# Usage: mirror-validate.sh <rows-file> <entry-file> [evidence-path ...]
#
#   rows-file      one or more census-schema registry rows (11 columns, pipe-delimited),
#                  exactly the block that would be appended to the lane registry
#   entry-file     the admitted knowledge entry; mirrored to
#                  corpus/knowledge/journal-reach-r49.md inside the scratch copy
#   evidence-path  optional file/dir copied to corpus/evidence/sources-r49/ in the copy
#
# What it does (no writes inside the lane):
#   1. copies $LANE/corpus into a fresh scratch mirror
#   2. inserts the rows at the end of the ## Registry table of the copied corpus/SOURCES.md
#   3. places the entry at its repo-relative path in the copy
#   4. runs:  sources-census.sh validate --file <mirror>/corpus/SOURCES.md
#   5. prints the command, its output and the exit code, and exits with that code
#
# Env: MIRROR_LANE (lane root, default the mori-shokunin lane)
#      MIRROR_DIR  (scratch mirror, default $TMPDIR/mirror; $TMPDIR must be set)
#      CENSUS_BIN  (default /home/vgpnk/Projects/shokunin/scripts/sources-census.sh)
set -uo pipefail

LANE=${MIRROR_LANE:-/home/vgpnk/Projects/shokunin/mori-shokunin}
CENSUS=${CENSUS_BIN:-/home/vgpnk/Projects/shokunin/scripts/sources-census.sh}
ENTRY_REL=corpus/knowledge/journal-reach-r49.md
EVID_REL=corpus/evidence/sources-r49

die() { printf 'mirror-validate: %s\n' "$*" >&2; exit 3; }

[ $# -ge 2 ] || die "usage: $0 <rows-file> <entry-file> [evidence-path ...]"
ROWS=$1; ENTRY=$2; shift 2

[ -f "$ROWS" ] || die "rows file not found: $ROWS"
[ -f "$ENTRY" ] || die "entry file not found: $ENTRY"
[ -d "$LANE/corpus" ] || die "lane corpus not found: $LANE/corpus"
[ -x "$CENSUS" ] || die "census tool not executable: $CENSUS"
command -v gawk >/dev/null 2>&1 || die "gawk not found; the census parser requires it"

if [ -n "${MIRROR_DIR:-}" ]; then
  M=$MIRROR_DIR
elif [ -n "${TMPDIR:-}" ]; then
  M=$TMPDIR/mirror
else
  die "neither MIRROR_DIR nor TMPDIR is set; lane tools must not mirror into /tmp"
fi

# 1. fresh copy of the lane corpus -------------------------------------------
rm -rf "$M" || die "cannot clear mirror: $M"
mkdir -p "$M/corpus" || die "cannot create mirror: $M"
cp -a "$LANE/corpus/." "$M/corpus/" || die "cannot copy $LANE/corpus into $M/corpus"

# 2. append the rows to the Registry table of the copy ------------------------
SOURCES=$M/corpus/SOURCES.md
[ -f "$SOURCES" ] || die "mirror has no SOURCES.md: $SOURCES"
work=$(mktemp "${MIRROR_DIR:-$M}/.insert.XXXXXX") || work=$M/.insert.$$
awk -v rowsfile="$ROWS" '
  BEGIN {
    nr = 0
    while ((getline l < rowsfile) > 0) {
      gsub(/\r$/, "", l)
      if (l ~ /[^ \t]/) rows[++nr] = l
    }
    if (nr == 0) { print "mirror-validate: rows file has no non-blank row" > "/dev/stderr"; fatal = 1; exit 3 }
  }
  { line[NR] = $0 }
  END {
    if (fatal) exit 3
    sec = 0
    for (i = 1; i <= NR; i++) {
      t = line[i]; sub(/^ {0,3}/, "", t)
      if (t ~ /^##[ \t]+Registry[ \t]*$/) { sec = i; break }
    }
    if (sec == 0) { print "mirror-validate: no ## Registry section in SOURCES.md" > "/dev/stderr"; exit 3 }
    hdr = 0; last = 0
    for (i = sec + 1; i <= NR; i++) {
      if (line[i] ~ /^ {0,3}\|/) {
        if (!hdr && line[i] ~ /\|[ \t]*id[ \t]*\|[ \t]*source[ \t]*\|/) hdr = i
        if (hdr) last = i
      } else if (hdr) break
    }
    if (!hdr || !last) { print "mirror-validate: no Header row in ## Registry" > "/dev/stderr"; exit 3 }
    for (i = 1; i <= NR; i++) {
      print line[i]
      if (i == last) for (j = 1; j <= nr; j++) print rows[j]
    }
  }
' "$SOURCES" > "$work"
ins=$?
if [ "$ins" -ne 0 ]; then rm -f "$work"; die "row insertion failed (awk rc=$ins)"; fi
cat "$work" > "$SOURCES" || { rm -f "$work"; die "cannot rewrite $SOURCES"; }
rm -f "$work"

# 3. place the entry at its repo-relative path --------------------------------
mkdir -p "$M/corpus/knowledge" || die "cannot create mirror knowledge dir"
cp "$ENTRY" "$M/$ENTRY_REL" || die "cannot place entry at $ENTRY_REL"

# 4. place evidence copies ----------------------------------------------------
mkdir -p "$M/$EVID_REL" || die "cannot create mirror evidence dir"
for p in "$@"; do
  if [ -d "$p" ]; then
    cp -a "$p/." "$M/$EVID_REL/" || die "cannot copy evidence dir $p"
  elif [ -f "$p" ]; then
    cp -a "$p" "$M/$EVID_REL/" || die "cannot copy evidence file $p"
  else
    die "evidence path not found: $p"
  fi
done

# 4b. read-only links for used-by targets that live outside corpus/ -----------
# E11 resolves every mined row's used-by path against the directory that holds the
# registry's parent (here: the mirror root). This lane's registry cites SKILL.md,
# PROVINCE.md, SCORECARD.md and two tools/ paths, so a corpus-only mirror is red on
# pre-existing rows through no fault of the appended block. Link those targets from
# the lane (read-only) instead of copying them; print what was linked.
linked=0
unresolved=0
while IFS= read -r p; do
  case "$p" in corpus/*) continue ;; esac
  [ -n "$p" ] || continue
  [ -e "$M/$p" ] && continue
  if [ -e "$LANE/$p" ]; then
    mkdir -p "$M/$(dirname -- "$p")" || die "cannot create $M/$(dirname -- "$p")"
    ln -s "$LANE/$p" "$M/$p" || die "cannot link $p"
    printf 'LINKED=%s\n' "$p"
    linked=$((linked + 1))
  else
    printf 'UNRESOLVED=%s\n' "$p"
    unresolved=$((unresolved + 1))
  fi
done < <(gawk -F'|' '
  /^ {0,3}##[ \t]/ { t=$0; sub(/^ {0,3}/,"",t); inreg = (t ~ /^##[ \t]+Registry[ \t]*$/); next }
  /^ {0,3}#[ \t]/ { inreg=0; next }
  !inreg { next }
  !/^ {0,3}\|/ { next }
  {
    if ($0 ~ /\|[ \t]*id[ \t]*\|[ \t]*source[ \t]*\|/) next
    if (split($0, c, "|") < 12) next
    s = c[9]; gsub(/^[ \t]+|[ \t]+$/, "", s); if (s != "mined") next
    u = c[12]; gsub(/^[ \t]+|[ \t]+$/, "", u)
    k = split(u, parts, ",")
    for (i = 1; i <= k; i++) {
      q = parts[i]; gsub(/^[ \t]+|[ \t]+$/, "", q)
      if (q != "" && q != "—") print q
    }
  }' "$SOURCES" | sort -u)

# 5. gate on the mirror with the fleet census ---------------------------------
printf 'LINKED_COUNT=%d\n' "$linked"
printf 'UNRESOLVED_COUNT=%d\n' "$unresolved"
printf 'MIRROR=%s\n' "$M"
printf 'ROWS=%s\n' "$ROWS"
printf 'ENTRY=%s\n' "$ENTRY_REL"
printf 'CMD=%s validate --file %s\n' "$CENSUS" "$SOURCES"
"$CENSUS" validate --file "$SOURCES"
rc=$?
printf 'EXIT=%d\n' "$rc"
exit "$rc"
```

Fixtures (scratch, same dir): `fixtures/entry-journal-reach.md`, `fixtures/rows-ok.md` (the four
well-formed rows), `fixtures/row-bad-dupe.md`, `fixtures/row-bad-recheck.md`, `fixtures/row-bad-pipe.md`,
`fixtures/row-bad-usedby.md`, `guard/SOURCES.md` (indented scratch registry). Test inputs are composed
with `cat` into `runs/rows-*.md`; receipts are `receipts/*.txt`.

## 2. Behaviour — what the harness does, observed

Insertion fidelity (`runs/mirror-a`, four rows):

```
$ grep -n '^| S48[5-8] \|^## Paths' runs/mirror-a/corpus/SOURCES.md
264:| S485 | journald.conf(5) — system…
265:| S486 | journalctl(1) — systemd v…
266:| S487 | systemd-journald.service(8)…
267:| S488 | own-work: this host's journ…
269:## Paths

$ diff <(grep -v '^| S48[5-8] ' runs/mirror-a/corpus/SOURCES.md) \
       /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
(no output)  → the mirror is byte-identical to the lane registry except the four appended rows
```

Entry and evidence placement in the same mirror:

```
$ ls -l runs/mirror-a/corpus/knowledge/journal-reach-r49.md      → the fixture entry, 1209 B
$ ls runs/mirror-a/corpus/evidence/sources-r49/
host-journal-reach.txt  journalctl.1.html  journald.conf.5.html  systemd-journald.service.8.html
```

## 3. Proof battery — exact commands, output, exit codes

All runs used `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecCensusMirror`
and a distinct `MIRROR_DIR` per test.

| # | input (rows) | command | exit | census line that decides it | receipt |
|---|---|---|---|---|---|
| a | 4 rows S485–S488, used-by `corpus/knowledge/journal-reach-r49.md` | `./mirror-validate.sh runs/rows-a.md fixtures/entry-journal-reach.md` | **0** | `file	ok	…/mirror-a/corpus/SOURCES.md` (21 W04 above it) | `receipts/test-a.txt` |
| b | rows-a + a second `S485` row | same, `runs/rows-b.md` | **1** | `file	E03	S485 duplicate id` | `receipts/test-b.txt` |
| c1 | rows-a + a row whose recheck is prose | same, `runs/rows-c1.md` | **1** | `file	E09	S489 recheck=2026-10-23 — re-verify after the size drop-in changes` | `receipts/test-c1.txt` |
| c2 | rows-a + a row whose recheck holds a literal `\|` | same, `runs/rows-c2.md` | **1** | `file	E01	S489 fields=12` (and `file	E11	S489 missing used-by re-verify`) | `receipts/test-c2.txt` |
| d | rows-a + a row whose used-by names an absent entry | same, `runs/rows-d.md` | **1** | `file	E11	S489 missing used-by corpus/knowledge/journal-reach-r49-typo.md` | `receipts/test-d.txt` |
| co | rows-a against a corpus-only lane root | `MIRROR_LANE=$PWD/co-lane …` | **1** | 26 `E11` lines, `UNRESOLVED=5` | `receipts/corpus-only-e11.txt` |
| ev | rows-a + the host receipt as an evidence argument | same, evidence arg on the cmdline | **0** | evidence file lands in the mirror | `receipts/test-evidence-arg.txt` |
| — | empty rows file | — | **3** | `mirror-validate: rows file has no non-blank row` then `row insertion failed (awk rc=3)` | `receipts/test-empty.txt` |
| — | no `TMPDIR`, no `MIRROR_DIR` | `env -u TMPDIR -u MIRROR_DIR …` | **3** | `mirror-validate: neither MIRROR_DIR nor TMPDIR is set; lane tools must not mirror into /tmp` | `receipts/test-notmpdir.txt` |

Test (a) full census body (22 lines: 21 `W04` + the `ok` line), head of the warnings and the last lines:

```
file	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc…/catalog/systemd.catalog.in across scopes
… (20 more W04, identical to the lane's own baseline)
file	W04	S486 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
file	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecCensusMirror/runs/mirror-a/corpus/SOURCES.md
EXIT=0
```

Baseline comparison, same tool, read-only on the live registry:

```
$ sources-census.sh validate --file /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
(20 W04 + 1 ok)   rc=0                              # receipts/live-baseline.txt
mirror-a:         21 W04 + 1 ok                    # exactly one new warning, S486's journalctl URL
$ comm -13 <(W04 baseline) <(W04 mirror-a) →
file	W04	S486 duplicate url www.freedesktop.org/software/systemd/man/latest/journalctl.html across scopes
```

`S486` is `E04`-exempt because its `teaches` cell opens `supersedes S351 —` (`sources-census.sh:646-649`);
the same URL is already on S014, S351 (rejected) and S470, so the third occurrence is a `W04` warning only.

## 4. Structural finding the harness had to work around — corpus-only mirror is red on this lane

A mirror built exactly as §10 describes (copy of `corpus/` + appended block + knowledge files) and gated with
`validate --file <mirror>/corpus/SOURCES.md` is **red on pre-existing rows**: `--file` derives the used-by root
as the mirror root (`sources-census.sh` `resolve_targets`: `dir_abs=$(realpath dirname(file)/..)`), and this
lane's registry has 61 distinct used-by paths of which **56 are under `corpus/` and 5 are lane-root paths**:

```
$ awk -F'|' '…mined rows…print used-by paths…' corpus/SOURCES.md | sort -u | awk -F/ '{print $1}' | sort | uniq -c
     56 corpus
      2 tools
      1 SKILL.md
      1 SCORECARD.md
      1 PROVINCE.md
```

Corpus-only receipt (`MIRROR_LANE` pointed at a `corpus/`-only lane root, so nothing can be linked):

```
UNRESOLVED=PROVINCE.md
UNRESOLVED=SCORECARD.md
UNRESOLVED=SKILL.md
UNRESOLVED=tools/fixtures/mori-oom-killers/cases-a2-r29.json
UNRESOLVED=tools/mori-disk-rate.py
… 26 `file	E11	…` lines …
EXIT=1                                    # receipts/corpus-only-e11.txt
```

The same count is reproducible from the live registry alone (26 `(row, external path)` pairs). Step 4b of the
harness therefore symlinks those five targets from the lane, read-only, and prints `LINKED=`/`UNRESOLVED=`;
with that step, tests (a) and (ev) are green and the E11 arm still fires on any *appended* row that names a
path the mirror does not carry (test d). Nothing in the lane is copied or written for those five paths.

## 5. Id-collision guard re-run on the live files (0–3 leading spaces)

```
S=/home/vgpnk/Projects/shokuknow
A=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ExecCensusMirror
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md \
  | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$S/merge/mori/SOURCES.append.md" \
  | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
```

Observed: `reg-ids` 257 ids (S001–S484, no internal duplicate), `staged-ids` 136 ids (S471–S606, no internal
duplicate), `collisions` **14**:

```
S471 S472 S473 S474 S475 S476 S477 S478 S479 S480 S481 S482 S483 S484
```

This is byte-identical (`diff` → no output) to the seat artifact already at
`.ufo/waves/round-49/assimilation/collisions`. Registry max id is `S484`, so the next free id is `S485`.

Adopted staged rows collide with none:

```
$ for id in S516 S532 S560; do printf '%s reg=%s staged=%s\n' "$id" \
    "$(grep -cx "$id" reg-ids)" "$(grep -cx "$id" staged-ids)"; done
S516 reg=0 staged=1
S532 reg=0 staged=1
S560 reg=0 staged=1
```

Guard-fails-when-indented proof (`guard/SOURCES.md`, a 2-space-indented scratch registry):

```
$ sources-census.sh validate --file guard/SOURCES.md
file	ok	…/guard/SOURCES.md            rc=0           # the indented row is census-valid
$ grep -oE '^\|[[:space:]]*S[0-9]{3,}' guard/SOURCES.md | … | comm -12 - staged-ids
col0 ids=[] collisions=0                            # column-zero-only pattern: FALSE GREEN
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' guard/SOURCES.md | … | comm -12 - staged-ids
ind ids=[S485] collisions=1 -> S485                 # 0–3-space pattern: caught
```

(`receipts/guard-proof.txt`.) The guard is not broken: an indented collision produces a nonempty
`collisions`, and the column-zero-only variant would have missed it.

## 6. Renumber-by-document map, checked against the staged rows

The map is by document: the id follows the URL/anchor evidence, never arithmetic. Each staged row was opened
in `/home/vgpnk/Projects/shokuknow/merge/mori/SOURCES.append.md` (read-only) and its URL compared with the
adopted id:

| staged row (line) | staged URL | adopted id | document the id will name | check |
|---|---|---|---|---|
| S516 (line 52) | `…/man/latest/journald.conf.html` | **S485** | journald.conf(5) — size limits, time retention, archived-vs-active | URL matches the document assigned S485 |
| S532 (line 68) | `…/man/latest/journalctl.html` | **S486** (new row whose `teaches` opens `supersedes S351 —`) | journalctl(1) — vacuum order, `--disk-usage` | URL matches S486; S351 is the lane's rejected row on **the same URL** (`grep '^| S351 ' corpus/SOURCES.md` → `…/journalctl.html`, `status=rejected`), so the successor row is the same page, not a new one |
| S560 (line 96) | `…/man/latest/systemd-journald.service.html` | **S487** | systemd-journald.service(8) — persistent vs volatile store | URL matches S487 |
| — (no staged row; this round's host receipt) | `corpus/evidence/sources-r49/host-journal-reach.txt` | **S488** | own-work: this host's journal reach, read-only 2026-10-25 | the receipt is committed at that path; the staged package's own-work rows (S524/S537/S544) are not adopted |

Order of ids is document order `journald.conf → journalctl → systemd-journald.service → host receipt`; it is
not the order of `count-c2.py`'s `COPIES` dict, which is irrelevant to the registry.

The four fixture rows in `fixtures/rows-ok.md` were written to this map (S485 journald.conf, S486 journalctl
with `supersedes S351 —`, S487 systemd-journald.service, S488 own-work receipt), so test (a) is also a dry run
of the intended append block **as worded by this seat** — it is not the scribe's final block.

## 7. State touched, tooling, limits

- Written: this report; `.scratch/r49-Mo49ExecCensusMirror/**` (harness, fixtures, guard fixture, runs,
  receipts). Nothing else. No `git add/commit/stash/checkout/reset/pull/push`; no jj command; nothing written
  under `/home/vgpnk/Projects/shokuknow` (read-only) or the fleet repo.
- Tooling: nothing installed or upgraded; `sources-census.sh`, `awk`/`gawk`, `bash` were already present.
- Scratch trimmed after the receipts were captured: `runs/mirror-a` (the green mirror, for inspection) and
  `co-lane` (the corpus-only counter-example) are kept; the other mirrors were deleted. Scratch is 50M
  (was 199M during the battery). `corpus/` is 25M, copied once per run.
- UNVERIFIED by this seat: `count-c2.py` was not run (the entry is not landed and the counter belongs to the
  claim); the scribe's final row block was not gated (the harness must be re-run on it); the round-end
  conformance command is `sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`, not the
  `--file` form used here.

## Findings

- **MED — F1 (`/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-49.md` §10, scratch-mirror step):** the
  recipe as written ("mirror the lane in scratch (copy of its `corpus/` …)" then
  `sources-census.sh validate --file "$A/validate/corpus/SOURCES.md"`) cannot exit 0 on this lane: `--file`
  resolves used-by against the mirror root, and 5 of the lane's 61 used-by paths are lane-root paths
  (`SKILL.md`, `PROVINCE.md`, `SCORECARD.md`, two `tools/` files), producing 26 `E11` lines before any
  append (`receipts/corpus-only-e11.txt`, exit 1). Any seat that gates the append this way will read a red
  gate for a reason unrelated to its rows. Fix used here: read-only symlinks for out-of-`corpus/` used-by
  targets, with `LINKED=`/`UNRESOLVED=` printed (`mirror-validate.sh` step 4b).
- **MED — F2 (`mori-shokunin/.gitignore`):** `.scratch/` is still not ignored — round 48's routed defect is
  open. Observed: `git status --porcelain | grep -c '^?? .scratch/'` = 152 untracked entries from other
  seats, and `.gitignore` has no `scratch` line. This round's scratch hygiene depends on the L1/closure
  adding the entry and cleaning residue; this seat may not edit `.gitignore`.
- **LOW — F3 (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:635-650`):** a literal `|` inside a
  cell yields `E01 … fields=12` *and* a second, misleading `E11` finding on the trailing fragment
  (`file	E11	S489 missing used-by re-verify`, `receipts/test-c2.txt`). Non-zero either way, so the gate is
  safe; but a seat cleaning a pipe will see two findings for one defect. The §10 normalization rule (no
  literal or escaped `|` in a cell) is the correct fix, not a parser change.
- **LOW — F4 (registry row S486 to be appended):** the successor row re-uses the `journalctl` URL already
  held by S014, S351 and S470, so the append adds exactly one `W04` (21 mirror warnings vs 20 baseline).
  Benign and expected (`E04` is exempt via `supersedes S351`); recorded so the L1 does not read the new
  warning as a defect.
- **LOW — F5 (`mirror-validate.sh` step 4b):** the green gate depends on the five lane-root targets
  existing at run time; three of them (`SKILL.md`, `PROVINCE.md`, `SCORECARD.md`) are files other wave seats
  may rewrite while the gate runs. A path deleted mid-round flips the gate red with `UNRESOLVED=`/`E11`
  although the append block is unchanged — fail-closed, but the cause must be read from the `UNRESOLVED=`
  lines, not from the E11s.
- **LOW — F6 (`mori-shokunin/.scratch/r49-Mo49ExecCensusMirror/`):** each harness run copies the 25M corpus;
  the battery peaked at 199M across seven mirrors. The seven were pruned to two (`runs/mirror-a`, `co-lane`,
  50M). Round-end cleanup must remove this directory with the rest of `.scratch/`.
