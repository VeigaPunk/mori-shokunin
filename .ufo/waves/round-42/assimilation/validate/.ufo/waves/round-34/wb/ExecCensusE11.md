measured 2026-10-23T07:48:53Z

# M6 reproduction — multi-path `used-by` cells vs the census (seat MoriR34A3.ExecCensusE11)

Attacks: draft mistake M6, `/fast/scratch/hyaku/mori-r34/a3-L1/drafts/corpus_lessons_round-34.md:109-113`
("the census reads a used-by cell as one path, and attempt 1's integration had written `a; b` and
annotated cells"). Detection only: no lane file, registry, tool, counter or rule was edited.

## Verdicts

VERDICT: M6 reproduced
VERDICT: no defect found — code `scripts/sources-census.sh` E11 path (it rejects the cell loudly, by design)

## Sandbox

`/fast/scratch/hyaku/mori-r34/a3-ExecCensusE11` (7.0M, `/usr/bin/du -sh`). `root/` mirrors exactly
what the census reads for lane mori under `--root`: `shokunin.conf` holding
`LANES="mori|mori-shokunin|..."`, plus `mori-shokunin/corpus/SOURCES.md` (byte copy of the draft
registry) and all 42 distinct comma-split `used-by` paths, copied read-only from the lane
(`placeholders=0` — every referenced path exists in the lane today, so (a) is not passing on stubs).
`root-{b,c,d,e,f}` are copies of `root/` with exactly one cell or file changed.

## Runs

Command form: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <root> mori`,
each under `timeout 120`; exit codes captured with `if/else` because this session shell runs `set -e`.

| # | registry | change | exit | finding lines |
|---|---|---|---|---|
| a | draft copy | none | **0** | `mori ok` + 12 W04 warnings |
| b | draft copy | S191 used-by := `tools/mori-disk-rate.py; SKILL.md` | **1** | `E11 S191` |
| c | draft copy | S194 used-by := `SKILL.md Round34` | **1** | `E11 S194` |
| d | draft copy | S191 used-by := `tools/mori-disk-rate.py, SKILL.md` (comma) | **0** | `mori ok` |
| e | draft copy | b's cell + a file literally named `tools/mori-disk-rate.py; SKILL.md` | **0** | `mori ok` |
| f | `git show HEAD:corpus/SOURCES.md` | none | **1** | nine E11 lines |

### (a) exit 0

```
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
… 11 further identical W04 rows (S037 S073 S074 S075 S076 S147 S148 S149 S150 S166 S168) …
mori	ok	/fast/scratch/hyaku/mori-r34/a3-ExecCensusE11/root/mori-shokunin/corpus/SOURCES.md
```

### (b) exit 1

```
mori	E11	S191 missing used-by tools/mori-disk-rate.py; SKILL.md
```

### (c) exit 1

```
mori	E11	S194 missing used-by SKILL.md Round34
```

### (f) exit 1 — the retained committed registry, nine E11 lines

```
mori	E11	S182 missing used-by corpus/knowledge/disk-write-rate-r33.md; tools/mori-disk-rate.py
mori	E11	S191 missing used-by tools/mori-disk-rate.py; SKILL.md Round34
mori	E11	S192 missing used-by tools/mori-disk-rate.py; SKILL.md Round34
mori	E11	S193 missing used-by tools/mori-disk-rate.py; SKILL.md Round34
mori	E11	S194 missing used-by SKILL.md Round34
mori	E11	S195 missing used-by SKILL.md Round34
mori	E11	S196 missing used-by SKILL.md Round34
mori	E11	S197 missing used-by corpus/knowledge/disk-write-rate-r33.md (Round-34 row 8 correction)
mori	E11	S198 missing used-by corpus/knowledge/disk-write-rate-r33.md (Round-34 row 8 correction)
```

## The census line that emits E11

`scripts/sources-census.sh`:

```
538  usedby_findings() {
561      paths=()
562      IFS=',' read -r -a paths <<< "$usedby"
563      for path in "${paths[@]}"; do
564        path=$(trim_cell "$path")
565        [ -n "$path" ] && [ "$path" != "—" ] || continue
566        if [ ! -e "$dir/$path" ]; then
567          printf '%s\tE11\t%s missing used-by %s\n' "$lane" "$id" "$path"
```

The cell is split on **commas only**; each element is trimmed and tested as one literal path under
the lane dir. `;` and parentheticals are ordinary characters, so `tools/mori-disk-rate.py; SKILL.md`
is one token. Control (d) shows a comma cell with two real paths passes; control (e) shows E11 is a
pure `[ -e ]` on the whole token — creating a file with the semicolon in its name silences it.

## Precision against the M6 text

1. **"the census reads a used-by cell as one path" — too strong, needs rewording.** It reads a
   *comma-separated list*. The draft registry itself depends on that: 53 rows carry comma cells
   (139 elements) and (a) passes. Correct wording: "a `;`-joined or annotated cell is not split, so
   it becomes one path". As a causal account of the 06:09:50Z failure the sentence is right; as a
   statement of the census's format it would mislead a reader into splitting multi-path rows.
2. **"nine E11 lines" — verified exactly.** Blobs `git show HEAD:corpus/SOURCES.md` and
   `git show 8d56809:corpus/SOURCES.md` are the same object (sha256 `78437f68…cab6d`) and yield
   exactly nine, composed of 4 `;` cells (S182, S191-S193), 3 `SKILL.md Round34` (S194-S196) and 2
   `corpus/knowledge/disk-write-rate-r33.md (Round-34 row 8 correction)` (S197, S198). So the failing
   state M6 calls "shown able to fail" *is* retained — as the committed registry, not as a separate
   run receipt.
3. **"Fix: … `mori ok`, exit 0 (evidence/census-end.txt)" — corroborated; its header clause is not.**
   `census-end.txt` does record `mori ok` and `EXIT=0`, and the working-tree registry (sha256
   `d893c6b9…94485`, mtime 03:10:48-0300 = 06:10:48Z, 3 s before that receipt's 06:10:51Z stamp)
   passes (real-lane check below). But `census-end.txt:1` also says "committed in the round-34
   integration commit": no commit carries the fix — `git log -- corpus/SOURCES.md` ends at 8d56809,
   and HEAD (5216d78) still holds `78437f68…`, the nine-E11 blob. The fixed registry is **uncommitted**
   and byte-identical to the draft snapshot `corpus_SOURCES.md`. Reword to "working tree; not yet
   committed" or the receipt's provenance is false when read against history.

Real-lane read-only confirmations (no writes): working tree sha256 `d893c6b9…` == draft sha256;
`validate --root /home/vgpnk/Projects/shokunin mori` → `mori ok`, exit 0; `validate <lane dir>` → `ok`, exit 0.

## Files changed

Only this report. Lane scratch left at `/fast/scratch/hyaku/mori-r34/a3-ExecCensusE11` (7.0M:
`root`, `root-{b,c,d,e,f}`, `out-*.txt`, `err-*.txt`, `paths.txt`, `head-SOURCES.md`,
`rev8d-SOURCES.md`); no load files were written. No tools installed or updated; no process left running.

## Risks / blockers

- The fix being uncommitted means the next census against HEAD (e.g. a fresh clone or post-commit CI)
  will emit the nine E11s again. This is L1's integration decision, not a defect in the tool.
- (a)'s pass depends on the 42 referenced paths existing in the lane; a stale registry referencing a
  deleted file would fail (a) for an unrelated reason. [INFERENCE] the draft registry's path set is
  current as of the run above (all 42 resolved).
