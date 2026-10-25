# ExecDiffScope — wave w2 scope check of the landed diff (round 47)

Seat: `ExecDiffScope` (executor, leaf). Lane: mori-shokunin.
Landed tip T = `68d66ca53d89be5c34a62f46af7c37449d9f9b63` (master).
Entering tip E = `2d85e33d14198d388fd3cda9cc15ec07e57e7a53`.
Freeze F = `63eecf2738db96f46b0bd02b1b2dfd66787493d0`.

## Assignment

Scope-check the landed diff: confirm that **no pre-existing SKILL.md registry row's entry
cell or command span changed** — only line 912's pinned text + parenthetical, and an appended
section. Report every changed line in pre-existing rows.

## Evidence

### 1. `git diff --stat F T` (F = 63eecf27, T = 68d66ca)

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --stat 63eecf2738db96f46b0bd02b1b2dfd66787493d0 68d66ca53d89be5c34a62f46af7c37449d9f9b63
```
Exit 0. 91 files, +16055 −39. SKILL.md appears in the stat (its own hunk detailed below).
Landed diff is not confined to SKILL.md; this seat's scope is the SKILL.md rows only
(diffstat raw dump: `artifact://26433`).

### 2. `git diff E T -- SKILL.md`

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 68d66ca53d89be5c34a62f46af7c37449d9f9b63 -- SKILL.md
```
Exit 0. Output:

```
SKILL.md | 29 ++++++++++++++++++++++++
1 file changed, 28 insertions(+), 1 deletions(-)

@@ -909,4 +909,31 @@ and 4):
-| SOURCES append-only timing (r38) | gate | `python3 tools/mori-sources-appendonly.py <rev> --round-base REV` | summary exit as before; the extra line `supersede_timing superseded_as_of=[...] stale_supersede=[...]` is the finding | `--selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` (round-40 v3: P-C11 — …) | latest-superseder landing vs last immutable-edit (or first-sighting) commit reachability over the `corpus/SOURCES.md` history | none (read-only git) | mori |
+| SOURCES append-only timing (r38) | gate | `python3 tools/mori-sources-appendonly.py <rev> --round-base REV` | summary exit as before; the extra line `supersede_timing superseded_as_of=[...] stale_supersede=[...]` is the finding | `--selftest` → `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0` (re-measured round 47 by `tools/mori-pin-check.py`: the round-40 bytes at `265a955c` print `pass=15`, the round-41 freeze `d72ac167` added seven arms and the pin was not updated; round-40 v3: P-C11 — …) | latest-superseder landing vs last immutable-edit (or first-sighting) commit reachability over the `corpus/SOURCES.md` history | none (read-only git) | mori |
+
+## Round47 — registry pin reconciler and the OOM tracepoint catalogue counter
+… (appended section, T lines 913–939; full text in `artifact://26432`)
```

The diff has **exactly one deleted line (old line 912) and 28 added lines** (new line 912 +
lines 913–939).

### 3. Independent structural verification (no reliance on diff output alone)

Files exported from the git object store and compared programmatically
(`difflib.SequenceMatcher`, exact string compare including whitespace):

```
git -C … show 2d85e33d14198d388fd3cda9cc15ec07e57e7a53:SKILL.md  > .scratch/r47w2-ExecDiffScope/SKILL-E.md
git -C … show 68d66ca53d89be5c34a62f46af7c37449d9f9b63:SKILL.md  > .scratch/r47w2-ExecDiffScope/SKILL-T.md
```

- E = 912 lines, T = 939 lines.
- **Exactly one** opcode in the whole file: `replace E[911:912] → T[911:939]`. Every other
  line of SKILL.md (E lines 1–911, i.e. all pre-existing content excluding line 912) is
  byte-identical between E and T. No whitespace-only or hidden changes anywhere.
- `git diff E F -- SKILL.md` → empty output, exit 0 ⇒ SKILL.md is identical at E and F, so
  the E→T hunk is exactly the F→T hunk.

### 4. Cell-by-cell comparison of the one changed pre-existing row (old line 912, r38 row)

The row was split on `|` (strip, trim) into its 8 columns and compared:

| cell | status |
|---|---|
| name (`SOURCES append-only timing (r38)`) | same |
| kind (`gate`) | same |
| **entry / command span** (`python3 tools/mori-sources-appendonly.py <rev> --round-base REV`) | **same** |
| verdict map | same |
| **self-test** | **CHANGED** |
| pinned values | same |
| write scope | same |
| owner (`mori`) | same |

Within the self-test cell, exactly two edits:

1. pinned selftest tally: `MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0` →
   `MORI_SOURCES_APPENDONLY_SELFTEST pass=22 fail=0`;
2. parenthetical: a prefix was prepended — `(round-40 v3: P-C11 — …)` →
   `(re-measured round 47 by `tools/mori-pin-check.py`: the round-40 bytes at `265a955c` print
   `pass=15`, the round-41 freeze `d72ac167` added seven arms and the pin was not updated;
   round-40 v3: P-C11 — …)`. The original round-40 v3 parenthetical text is preserved verbatim
   after the new prefix.

## Verdict: **HOLDS**

No pre-existing SKILL.md registry row's entry cell or command span changed. The **only**
changed pre-existing line is line 912 (the r38 SOURCES append-only row), and within it only
the self-test cell's pinned selftest tally (`pass=15` → `pass=22`) and its parenthetical
changed; the row's entry cell/command span, name, kind, verdict map, pinned values, write
scope, and owner are byte-identical. The rest of the diff is the appended `## Round47` section
(T lines 913–939), which adds prose and a new table (header + two new rows: registry pin
reconciler r47 C1, r47 tracepoint catalogue C2) without touching any pre-existing row.

### Changed lines in pre-existing rows (complete list)

- **Old line 912 / new line 912** — r38 SOURCES append-only row, self-test cell only:
  - `pass=15 fail=0` → `pass=22 fail=0` (pinned selftest tally),
  - parenthetical prefix added: `re-measured round 47 by `tools/mori-pin-check.py`: the
    round-40 bytes at `265a955c` print `pass=15`, the round-41 freeze `d72ac167` added seven
    arms and the pin was not updated;`
  - Rest of the row (including the entry cell/command span) unchanged.

No other pre-existing row has any changed line. All other 911 pre-existing lines are
byte-identical between E and T.

## Reproducer

```
D=$(mktemp -d) && git -C "$D" init -q && git -C "$D" config user.name x && git -C "$D" config user.email x@x
git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff 2d85e33d14198d388fd3cda9cc15ec07e57e7a53 68d66ca53d89be5c34a62f46af7c37449d9f9b63 -- SKILL.md
# → 1 deletion (old line 912) + 28 insertions (new line 912 + lines 913–939)
python3 - <<'EOF'
import difflib
E = open('.scratch/r47w2-ExecDiffScope/SKILL-E.md').read().splitlines()
T = open('.scratch/r47w2-ExecDiffScope/SKILL-T.md').read().splitlines()
for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,E,T).get_opcodes():
    if op != 'equal': print(op, i1, i2, j1, j2)
EOF
# → ('replace', 911, 912, 911, 939) — the only non-equal block in the whole file
```

## UNVERIFIED / not checked

- Content of the 90 other files in the F→T diffstat (outside this seat's SKILL.md scope).
- Whether the new `pass=22` tally in the r38 row is itself correct — that is a C1/C2
  calibration question for other seats, not a diff-scope question. This seat verifies only
  that the row edit is confined to the self-test cell.
