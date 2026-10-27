# Mo52ExecCensusCounts — frontier-step census before → after (registry rows by status and tier)

Seat: executor, leaf. Round 52, wave w1. Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Measured revisions: before `4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d` (entering tip), after
`8524904adb25e44f24d9f25aac7eae909625c18c` (data). Lane HEAD during the run: `075436b1` (wave dispatch,
SOURCES.md unchanged from the data commit — proven below).
Scratch: `/fast/scratch/hyaku/mori-r52/Mo52ExecCensusCounts/` (created, used, removed at the end).
Disk guard before the run: `/fast/scratch/hyaku` 26 % used, 602.0G free; no ENOSPC.
No tool installed or upgraded (nothing was needed); no pacman transaction attempted.

## Instruments and bytes

| what | sha256 |
|---|---|
| `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` | `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30` |
| `corpus/SOURCES.md` @ `4f266ef2` (= archive copy) | `a7256ba52f788582ad5096d8a9a891cdfeabf726cd79e3fafbcd82edfa227156` |
| `corpus/SOURCES.md` @ `8524904a` (= my `git show` copy) | `43b282ebfade7c24d114e9fa679c0f899d088832f8db6f967b3dc96eb484f03b` |
| `corpus/SOURCES.md` in the lane working tree | `43b282eb…f03b` (identical to the data commit) |

Frozen-bytes check (read-only, in the lane): `sha256sum -c` over all 24 entries of
`.ufo/waves/round-52/evidence/freeze-sha256.txt` → no mismatch lines, `sha_check_exit=0`. This includes
`evidence/census-start.txt` (`4a4e81a0d37f9485…`), so the baseline receipt's bytes are attested.

## 1. Row census by status and tier — awk over `git show <rev>:corpus/SOURCES.md`

Parser (accepts 0–3 leading spaces, as the maintained `sources-census.sh` parser does; registry columns
`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`):

```awk
function trim(x){ gsub(/^[ \t]+|[ \t]+$/,"",x); return x }
/^[ ]{0,3}\|[ ]*S[0-9][0-9][0-9][ ]*\|/ {
  n = split($0, f, "|"); if (n < 10) { bad++; next }
  id = trim(f[2]); kind = trim(f[4]); tier = trim(f[5]); status = trim(f[9])
  if (id !~ /^S[0-9][0-9][0-9]$/) { bad++; next }
  rows++; seen[id]++
  tier_n[tier]++; status_n[status]++; combo[tier " / " status]++
}
END { … rows, malformed, per-tier, per-status, cross-tab, duplicate ids … }
```

Run (both revs, one pipeline each, output piped through `sort` — hence the field order below):

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 4f266ef2…:corpus/SOURCES.md > SOURCES-<rev>.md
$ awk -f census.awk SOURCES-<rev>.md | sort
```

Before — `4f266ef2` (262362 bytes), `exit=0`:

```
  A / mined      209
  A / queued     22
  A / rejected   7
  B / mined      10
  B / queued     2
  B / rejected   2
  C / rejected   17
cross:
duplicate_ids=(count=0)
rows=269 malformed=0
status: mined=219 queued=24 rejected=26
tier: A=238 B=14 C=17
```

After — `8524904a` (265640 bytes), `exit=0`:

```
  A / mined      214
  A / queued     22
  A / rejected   7
  B / mined      10
  B / queued     2
  B / rejected   2
  C / rejected   17
cross:
duplicate_ids=(count=0)
rows=274 malformed=0
status: mined=224 queued=24 rejected=26
tier: A=243 B=14 C=17
```

Delta: `rows 269 → 274 (+5)`, `tier A 238 → 243 (+5)`, `status mined 219 → 224 (+5)`; B=14, C=17, queued=24,
rejected=26 unchanged; malformed=0 and duplicate ids=0 at both revs. Exactly the expected +5 tier-A mined rows.

## 2. The +5 rows are exactly S497–S501, and nothing else moved

```
$ comm -13 ids-before.txt ids-after.txt      # ids added
S497
S498
S499
S500
S501
$ comm -23 ids-before.txt ids-after.txt      # ids removed
                                     (empty)
$ git -C … diff 4f266ef2… 8524904a… -- corpus/SOURCES.md | grep -cE '^\+[^+]'
5
$ git -C … diff 4f266ef2… 8524904a… -- corpus/SOURCES.md | grep -cE '^-[^-]'
0
```

Highest id before: `S496`; after: `S501` (ids continue the registry, no gap, no renumbering).

Per-field read of the five added rows at the data commit (`S497` at file line 276 through `S501` at line 280,
inside `## Registry` which spans lines 3–281; `## Paths` begins at 282 — so no row lands outside the section,
and `validate` raised no E12):

```
S497 kind=docs tier=A status=mined opened=2026-10-26 recheck=on-release
S498 kind=docs tier=A status=mined opened=2026-10-26 recheck=on-release
S499 kind=code tier=A status=mined opened=2026-10-26 recheck=on-release
S500 kind=code tier=A status=mined opened=2026-10-26 recheck=on-release
S501 kind=code tier=A status=mined opened=2026-10-26 recheck=on-release
```

`used-by` on all five is `corpus/knowledge/overcommit-commit-limit-r52.md` (single path each), and the same commit
adds that file plus the five copies under `corpus/evidence/sources-r52/` (mman.h.v7.2 4265 B, mmap.c.v7.2 51223 B,
overcommit-accounting.rst.v7.2 2647 B, util.c.v7.2 43913 B, vm.rst.v7.2 42424 B).

## 3. `sources-census.sh validate` — rc and W04 count, after vs. the frozen baseline

After (lane working tree = data commit bytes), run from the fleet root as specified:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6…/catalog/systemd.catalog.in across scopes
… 23 W04 lines, ids S035 S037 S073 S074 S075 S076 S147 S148 S149 S150 S166 S168 S201 S218 S220 S228
  S349 S351 S470 S476 S486 S491 S492 …
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
exit=0
```

- `W04=23`, `E-codes=0`, `ok` line present, `exit=0`.
- Diff against `evidence/census-start.txt` (24 TSV lines): identical; the only differing lines are that receipt's
  own framing lines (`$ <command>` first line and `exit=0` last line). `diff` → those two lines, nothing else.
- The same 23 W04 ids and texts as the baseline: `S497–S501` introduce **no new** W04 (their five URLs are new
  paths under `raw.githubusercontent.com/torvalds/linux/v7.2/`).

Before, measured with the same instrument in the same mode family (so the W04 baseline is re-derived, not assumed):

```
$ git -C …/mori-shokunin archive 4f266ef2… | tar -x -C $S/root-before/mori-shokunin   # archive_exit=0, 12581 files
$ sha256sum $S/root-before/mori-shokunin/corpus/SOURCES.md
a7256ba52f788582ad5096d8a9a891cdfeabf726cd79e3fafbcd82edfa227156
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate $S/root-before/mori-shokunin
23 × W04 (same ids), 1 × ok, exit=0
```

Difference against `census-start.txt`: only the lane label (`mori-shokunin`, the archive directory name, instead of
`mori`, which `--root`+conf resolves) and the path prefix. Same 23 W04 ids, same texts, same `ok`, same rc.
`E-codes=0` there too, so the entering tip was also E-clean and the +5 rows added no E code.

## 4. Independent cross-check of the awks with the maintained parser (`census` mode)

```
$ sources-census.sh census --file $S/SOURCES-4f266ef2….md   # before
file	rows	269   file	tier.A	238   tier.B 14   tier.C 17
file	status.mined	219   status.queued 24   status.rejected 26
$ sources-census.sh census --file $S/SOURCES-8524904a….md   # after
file	rows	274   file	tier.A	243   tier.B 14   tier.C 17
file	status.mined	224   status.queued 24   status.rejected 26
FLEET	rows	274  tier.A 243  tier.B 14  tier.C 17  tier.invalid 0
	status.queued 24  status.mined 224  status.rejected 26  status.invalid 0  missing 0
```

And with `--root` at the data commit: `mori rows 274, tier.A 243, tier.B 14, tier.C 17, status.mined 224,
status.queued 24, status.rejected 26, exit=0`. Every number agrees with my awk at both revisions, and the
`--file` mode's `E11` output (304 / 309 lines, every `used-by` resolving as missing) is a property of `--file`
mode, not of the data: the same bytes under a directory/`--root` target give `E=0`. That mode's E11 lines are
therefore not evidence either way and are not used above.

### Frontier-step delta (single table)

| measure | @ `4f266ef2` | @ `8524904a` | delta |
|---|---|---|---|
| registry rows | 269 | 274 | **+5** |
| tier A / B / C | 238 / 14 / 17 | 243 / 14 / 17 | **A +5** |
| status mined / queued / rejected | 219 / 24 / 26 | 224 / 24 / 26 | **mined +5** |
| malformed rows | 0 | 0 | 0 |
| duplicate ids | 0 | 0 | 0 |
| E codes (`validate`) | 0 | 0 | 0 |
| W04 (`validate`) | 23 | 23 | **0** |
| ids added / removed | — | S497–S501 / none | +5 / 0 |

## Findings

1. **LOW — registry delta is exactly as the contract expected; no residue.**
   `.ufo/waves/round-52/contract.md` §C2 announces rows `S497–S501`; the data commit adds exactly those five ids,
   five `+` lines and zero `-` lines in `corpus/SOURCES.md`, all `tier=A`, `status=mined`, `kind` two docs + three
   code, `opened=2026-10-26`, `recheck=on-release`, `used-by=corpus/knowledge/overcommit-commit-limit-r52.md`.
   Counts `269→274`, `A 238→243`, `mined 219→224` confirmed by two independent parsers. Nothing else in the
   registry moved (no id renaming, no status churn, no tier churn, no duplicate ids).
2. **MED — `validate` is a warning/error census, not a row census, so the frozen start/end receipts cannot show
   the +5 rows.** `.ufo/waves/round-52/evidence/census-start.txt` (sha256 `4a4e81a0…`) prints the command, 23
   W04 lines and `exit=0`. Re-running the identical command at the data commit yields 24 TSV lines that are
   identical to those 24 lines: W04 stays at 23 and no E code is added, so **the round-end census output will be
   byte-identical to the round-start output while the registry grew by five rows**. The frontier step's row-level
   movement is only visible through `census` mode (`rows 269 → 274`) or a direct row count, which the round shape
   does not receipt. Routed to round 53 as a receipt-shape item (record the measured tip and the `census`-mode
   totals alongside `validate`), not as a change to any frozen counter or predicate.
3. **LOW — the baseline receipt does not name the revision it measured.** `census-start.txt` records the literal
   command (satisfying round-51 closure item 7) but not a rev or a SOURCES.md hash, so a reader cannot tie it to a
   tip by inspection. I closed the gap by measurement instead: the same command over an archive of `4f266ef2`
   reproduces the receipt's 23 W04 ids and texts and its `ok` line exactly (only the lane label differs, by
   construction of the directory target), and the archived `corpus/SOURCES.md` hashes to
   `a7256ba5…227156`. So the baseline is consistent with the entering tip, but that fact lives in a wave report,
   not in the receipt. Same round-53 routing as finding 2.
4. **LOW — `--file` mode cannot be used for `E11` comparisons and invites a false alarm.** Running
   `sources-census.sh validate --file …` emits E11 for every `used-by` path (304 lines for the 269-row file, 309
   for the 274-row file) because relative `used-by` paths are resolved against the file's own directory. The same
   bytes under `--root` yield `E=0`. Any future seat comparing `--file` runs across revisions will see an E11
   count that tracks only the row count and must not read it as a data defect; this is a named limit worth
   recording with the census route.
5. **LOW (informational) — frozen bytes are intact at the measured tip.** `sha256sum -c` over all 24 entries of
   `evidence/freeze-sha256.txt`, run in the lane, produced no mismatch (`exit=0`), including both counters, the
   contract, the controls, the seven C1 control receipts, both selftest receipts, `census-start.txt`, the sweep and
   the five `corpus/evidence/sources-r52/` copies. My census therefore measured the frozen instrument and did not
   edit any frozen file.

## Scope compliance

Reads only: `git show`/`git archive`/`git diff`/`git ls-tree`/`git log`/`git status --porcelain` in the lane,
`sha256sum`, `awk`, `wc`, `comm`, `diff`, `grep`, and `scripts/sources-census.sh` (rc captured). No mutation of the
lane, the fleet root, jj state or any git index; no pacman; no PATH writes; no config or sysctl write; no kernel
log MESSAGE grep. Files written: this report and `/fast/scratch/hyaku/mori-r52/Mo52ExecCensusCounts/**` only (the
archive root, 332M, and the scratch tree removed after the run). The lane's `corpus/SOURCES.md` is clean in the
working tree (`git status --porcelain -- corpus/SOURCES.md` printed nothing). I did not verify any counter
(`count-c1.py`/`count-c2.py`) and make no claim about C1 or C2 beyond the SOURCES/freshness facts above; the +5
mined rows say nothing about whether the entry's text is correct — that is the entailment seats' arm.
