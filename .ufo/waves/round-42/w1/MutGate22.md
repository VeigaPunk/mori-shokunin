# MutGate22 — append-only gate re-run at tip (no-harm) + one mutation probe

Role: mutation-tester (leaf). Lane root: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Lane HEAD at run time: `f3ec09775e9d81ccbba7314372ba546bd2be7e90`; assigned landed tip
`34b926730c30e0251e1aec531863d8355dc491f1` is its parent and a present commit object.
Sandbox: `git clone --no-hardlinks` of the lane into `/tmp/mutgate22/lane` (no lane worktree,
index, jj state or `.ufo/state` touched; no checkout in the lane). Tool bytes at the tip and at
HEAD are the same git blob `887fd85d96fd97f99f1845090cda64cf5e084fa8`
(`git rev-parse 34b92673:tools/mori-sources-appendonly.py HEAD:...`), extracted to
`/tmp/mutgate22/tool-tip.py`, sha256 `75af8f6fc63dc736f07c02617bed4bf6c1ad7f880ffb49849b065b4d40d8f76b`.

## 1. Baseline — selftest at tip bytes

```
$ python3 /tmp/mutgate22/tool-tip.py --selftest
MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0
EXIT=0
```
Matches the expected `pass=22 fail=0`. (Arm counts measured from the tool's own case lists:
9 basic + 6 DAG + 7 r41 DAG = 22 checks.)

## 2. Baseline — lane line, pre-rows vs post-rows vs r41

All runs used the tip bytes (`tool-tip.py`) against the clone; `--repo` only reads.

```
rev 316f3dcf (parent of the data commit; 231 registry rows)
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226,S229] stale_supersede=[]

rev 34b92673 (7 new rows S232,S233,S234,S235,S241,S262,S347; 238 registry rows)
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S069,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226,S229] stale_supersede=[]

rev f3ec0977 (current lane HEAD)
supersede_timing superseded_as_of=[...same 36 ids...] stale_supersede=[]
```

Byte-identical timing lines: 36 as-of ids, `stale_supersede=[]` — the round-41 set (r41
receipts `7450722e`/`9de7323d` and `.ufo/waves/round-41/evidence/control-after.txt:125`
print the same 36-id line; r41's measured lane run at `aa161e99` also exited 1). The 7 new
rows add no `supersedes S###` pair (their `teaches` cells do not match the tool's
`^supersedes\s+(S\d{3})` anchor), so the eligible-pair set is untouched, `superseded=`
stays the same 36 ids, and `appendonly_violations=18` / `changed` lines are unchanged.

Timing canary still discriminates at the older revision:

```
$ ...  e37dcc6 --repo .
supersede_timing superseded_as_of=[S041,S044,S051,S062,S064,S067,S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] stale_supersede=[S069]
```

Gate exit at the tip is `1` (the summary carries 18 pre-existing in-place `changed` rows);
same as the r41 lane receipt (`control-after.txt: EXIT=1`), so this is baseline, not a
round-42 regression. Selftest exit is `0`.

**No-harm verdict: HOLDS.** No supersede verdict (as-of/stale membership, `superseded_by`,
`superseded` order, `round_changed`) changed between 231-row and 238-row tips or versus r41.

## 3. Mutation probe — one plausible defect

Scratch copy `/tmp/mutgate22/mutant-flip.py` (copy of the tip bytes; lane file never edited).

- Mutant: at line 398, invert the as-of classification test
  `if edit_commit is not None and ancestor(edit_commit, landing):`
  → `if edit_commit is not None and not ancestor(edit_commit, landing):`
- Plausible defect: a boundary/negation slip in the ancestry comparison that would swap
  "supersede postdates the edit" (as-of) with "supersede predates it" (stale), silently
  inverting the P-C12 disposition for every eligible id.
- Expected detector: `--selftest`, whose hand-written fixtures assert as-of/stale membership
  on supersede-before-edit, side-branch superseder, never-edited row, delete/re-add
  superseder, and both incomparable-superseder date orders.

Observed:

```
$ python3 mutant-flip.py --selftest
FAIL superseding row: superseded_as_of: want ['S001'] got []; stale_supersede: want [] got ['S001']
FAIL supersede before edit: ...
FAIL side-branch superseder is stale: ...
FAIL merge does not fabricate an edit: ...
FAIL landing is the last edit commit: ...
FAIL never-edited superseded row is as-of: ...
FAIL first-parent-lacks-path merge contributes no edits: ...
FAIL linear delete-then-re-add is not an edit: ...
FAIL per-commit header map prevents fabricated changes: ...
FAIL per-commit teaches map retains permuted superseder: ...
FAIL incomparable superseders resolve independently of early date: ...
FAIL incomparable superseders resolve independently of late date: ...
FAIL deleted/re-added superseder uses the later ancestry landing: ...
MORI_SOURCES_APPENDONLY_SELFTEST pass=9 fail=13
EXIT=1
```

Lane-level detector also flips (mutant run against the tip clone):

```
supersede_timing superseded_as_of=[] stale_supersede=[S041,...,S229]   # all 36 now stale
```

**Verdict: KILLED** — 13 of 22 checks fail, exit 1; the inverted evaluation is not silent.

## 4. Restoration evidence

- Scratch mutated copy hash before mutation: `75af8f6f…d8f76b`; after mutation:
  `d8a0919bf3caa48a0c52dafb9951ef941101124fd61bfb382c307cc3c1d4f340`.
- Restored by copying the pristine tip extraction over the mutant: sha256
  `75af8f6fc63dc736f07c02617bed4bf6c1ad7f880ffb49849b065b4d40d8f76b` for
  `/tmp/mutgate22/mutant-flip.py`, equal to `/tmp/mutgate22/tool-tip.py`. Same detector on the
  restored bytes: `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`, `EXIT=0`. (Second probe copy
  `probe2.py`, used only to capture the full FAIL list, deleted.)
- Lane source file untouched: `sha256sum tools/mori-sources-appendonly.py` =
  `75af8f6fc63dc736f07c02617bed4bf6c1ad7f880ffb49849b065b4d40d8f76b`; git blob at
  `34b92673` and at HEAD both `887fd85d96fd97f99f1845090cda64cf5e084fa8`.
- Lane tracked tree clean (`git status --porcelain --untracked-files=no` → 0 lines); the only
  untracked entries are pre-existing round-42 assimilation artifacts, none created by this
  seat. Lane HEAD still `f3ec0977…`; no index, jj, `.ufo/state` or fleet file written.

Tooling: no installs or upgrades were needed (python3 from the host, git 2.x). No secrets read.
