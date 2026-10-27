# Mo57Scribe54 — C2 counter attack (`count-c2.py`)

**Verdict: the frozen C2 counter is satisfiable by a blob that is not the predicate's entry, and it rejects a well-formed entry.** Fixtures `fx1` and `fx12` both return `C2=met claims=8 source=ok quotes=ok` and exit 0 for an entry that has no `source:`/`verified-at:`/`recheck:` opener, no source copy anywhere in the tree, fabricated quotes, `"pairing count"` present only inside a negation, `S548` present only as a negated string inside the token `S5480`-style prose, and a registry row that pre-exists the round and is not `mined`. Controls `fx10` and `fx11` show the reverse: a substantively correct eight-claim entry scores `claims=7` after one leading space, and a real `S548` registry row written `|S548|` scores `source=bad`. The counter is a marker scan over two `git show` blobs; it verifies none of the evidentiary content the C2 predicate names, in either direction.

## Counter under test

`.ufo/waves/round-57/count-c2.py` (sha256 `0fe9e6f4cdde0ac14bd8cad907e948edcb8a51f7c950622cf84cae5f1f75f742`, 17 lines):

| line | code | what it actually enforces |
| --- | --- | --- |
| 8-9 | `entry=show(knowledge/watchdog-unclosed-r57.md)`, `registry=show(SOURCES.md)` | the two blobs exist at revision `R` |
| 12 | `claims=[x for x in entry.splitlines() if x.startswith("| K")]` | count of lines whose first three characters are `| K` |
| 13 | `source_ok="S548" in entry and "| S548 |" in registry and "mined" in registry` | three unanchored substring tests, one per blob, no row parsing |
| 14 | `quote_ok=all("`" in x and "`" in x for x in claims)` | at least one backtick character per claim line (the test is literally duplicated) |
| 15 | `ok=len(claims)==8 and source_ok and quote_ok and "pairing count" in entry` | exact eight, three markers, one substring |

The frozen predicate it must enforce (`.ufo/waves/round-57/contract.md`, C2 paragraph) has seven elements: entry exists; opens with `source:`/`verified-at:`/`recheck:`; cites a **newly opened** source row; **eight claim rows**; **each with a located quote in the source copy**; and states `unclosed` is a **pairing count rather than a present-running count**. Lines 12-15 do not touch four of those seven (opener, newness, source copy, quote location) and mis-handle the other three (row identity, citation identity, semantic direction).

## Method

A byte-identical copy of the counter, parameterized only in the repository path, so the checks are unchanged:

```
4c4
< R=sys.argv[1]; repo="/home/vgpnk/Projects/shokunin/mori-shokunin"
---
> R=sys.argv[1]; repo=sys.argv[2]  # ONLY the repo literal is parameterized; all checks byte-identical
```

Copy sha256 `e6278d67dece28d55ffb2631d37989a9ac886079aea0be36079333e653c37429`; original `0fe9e6f4cdde0ac14bd8cad907e948edcb8a51f7c950622cf84cae5f1f75f742`. Every fixture is a one- or two-commit git repo created only under scratch (`/fast/scratch/hyaku/mori-r57/Mo57Scribe54/`), each verified with `git -C <abs fixture> rev-parse --show-toplevel` printing that fixture directory. Nothing in the lane repo was written, and no commit/jj mutation was made anywhere. Environment: `Python 3.14.8`, `git 2.56.0`. Fixture repositories were removed after this report (reproduce from the appendix, which was run end-to-end and reproduced every row below).

## False-positive evidence — eight "located claims" without a source

`fx1` (synthetic registry; `S548` row pre-exists the entry commit and is **not** `mined`; word `mined` carried by an unrelated `S001` row):

```
$ python3 .../bin/count-c2-param.py $(git -C fx1 rev-parse HEAD) fx1
C2=met claims=8 source=ok quotes=ok rev=2e01a75f...
exit=0
```

The entry (`fx1/corpus/knowledge/watchdog-unclosed-r57.md`) violates the predicate six ways while scoring met:

1. No `source:`, `verified-at:` or `recheck:` line exists (predicate element 2). The counter never reads a header.
2. No source copy exists in the fixture at all — `fx1/corpus/` contains `SOURCES.md` and `knowledge/` only; the fixture equalling `fx12` has no `corpus/evidence/sources-r57/` either, so **not one "located quote" can resolve** (element 5). Line 14 only asks whether a backtick character occurs.
3. `claims=8` is reached with seven data rows: `grep -c '^| K'` = 8 while `grep -c '^| K[0-9]'` = 7. The eighth "claim" is the table header `| Key \`hdr\` | Meaning |` — `startswith("| K")` cannot distinguish a header from a claim (element 4).
4. Claim `K1` carries a single, unbalanced backtick — `| K1 | fabricated quote \`a1 that resolves nowhere and is unbalanced |` — and still satisfies line 14. Control `fx7` (all claim lines with zero backticks) gives `quotes=bad`; so the test is "≥1 backtick", never "a closed, located quotation".
5. `"pairing count"` appears only in the negation "`unclosed` is explicitly **not** a pairing count ... no present-running statement is made" (element 6). Line 15 is a bare substring test with no polarity.
6. `S548` is cited only as "No S548 row was opened this round" (element 3): the counter cannot tell citation from denial.

`fx12` — the same entry against the **real** round-57 registry, so the finding does not depend on a synthetic registry:

```
$ git -C mori-shokunin show 53e2b47...:corpus/SOURCES.md  # 298109 bytes, max id S547
$ printf '%s\n' '| S548 | fixture row appended in scratch, never opened from any source — https://example.invalid/none | ... | placeholder | none | none | none |' >> fx12/corpus/SOURCES.md
$ tail -1 fx12/corpus/SOURCES.md | grep -c mined
0
$ python3 .../count-c2-param.py $(git -C fx12 rev-parse HEAD) fx12
C2=met claims=8 source=ok quotes=ok rev=ff2df835...
exit=0
```

The appended `S548` row (fixture line 394) is not `mined` and was never opened from any source, yet `source=ok`: `"mined" in registry` is satisfied by **270 pre-existing occurrences** in rows opened in earlier rounds (`grep -c mined corpus/SOURCES.md` = 270 at the entering tip). `source_ok` therefore never binds the word `mined` to the `S548` row, and `S548` never has to be a row *opened this round*.

Remaining entries, all met with exit 0:

| fixture | what it proves | output |
| --- | --- | --- |
| `fx3` | no newness check: entry **and** `S548` row are present in the seed commit, the "round" commit touches only `README.md`, yet met | `C2=met claims=8 source=ok quotes=ok` |
| `fx4` | registry has **no table at all**; `S548` and `mined` occur only in prose ("A row would look like \| S548 \| but none exists… nothing here was mined") — `grep -c mined` = 1, `grep -c '\| S548 \|'` = 1 | `C2=met claims=8 source=ok quotes=ok` |
| `fx6` | entry never cites `S548`; it contains only `S5480` (an unrelated token), yet `"S548" in entry` is true | `C2=met claims=8 source=ok quotes=ok` |
| `fx8` | entry asserts the **inversion** — "`unclosed` counts drivers that are present and currently running … 'pairing count' is a misreading this entry rejects" — and is met | `C2=met claims=8 source=ok quotes=ok` |
| `fx9` | the eight `| K` lines live inside a fenced code block; the document has no table | `C2=met claims=8 source=ok quotes=ok` |
| `fx13` | one statement repeated eight times (`grep '^| K' … \| sort -u \| wc -l` = 1) satisfies "eight claim rows" | `C2=met claims=8 source=ok quotes=ok` |

Controls that isolate single checks: `fx5` (proper `S548` row, word `mined` absent anywhere) → `C2=unmet claims=8 source=bad quotes=ok`; `fx7` (zero backticks) → `C2=unmet claims=8 source=ok quotes=bad`.

## False-negative evidence — a correct entry fails

| fixture | condition | output |
| --- | --- | --- |
| `fx10` | fully formed entry: `source:`/`verified-at:`/`recheck:` opener, eight claim rows with backticked quotes, explicit "a pairing count, not a present-running count"; row 8 is indented by exactly one space at line 16 (`cat -A` shows ` | K8 | quote \`q8\` |$`) | `C2=unmet claims=7 source=ok quotes=ok` → exit 1 |
| `fx11` | registry writes the row as `\|S548\|…\|mined\|…\|corpus/evidence/sources-r57/S548.src\|` with no padding spaces | `C2=unmet claims=8 source=bad quotes=ok` → exit 1 |

So a seat that formats its table with aligned/indented rows, or a registry row without padding, is failed for formatting while a fabricated entry passes. `S548` is also hard-coded on line 13 with no reservation: at the freeze revision no `S548` row exists (max id `S547`), so if a sibling opens `S548` for any other purpose in this wave, a correct C2 entry would have to move to an id the counter rejects.

## Lane state (read-only, for the record)

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD
618562c72a03dc4d17386b715357f863fd327274
$ python3 .ufo/waves/round-57/count-c2.py 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2
C2=unmet claims=0 source=bad rev=53e2b476...   exit=1     # matches controls.txt
$ python3 .ufo/waves/round-57/count-c2.py 618562c72a03dc4d17386b715357f863fd327274
C2=unmet claims=0 source=bad rev=618562c7...   exit=1
```

Neither revision contains `corpus/knowledge/watchdog-unclosed-r57.md` (`git ls-tree -r --name-only HEAD -- corpus/knowledge | grep -c watchdog-unclosed-r57` = 0), and `git show 618562c7...:corpus/SOURCES.md | grep -n S548` exits 1 with no output. The before/after asymmetry in the contract is therefore intact at measurement time; the attack above is a counter-quality finding, not an assertion about a landed entry. No sibling report was used as evidence here; the fixtures and all verdicts above were derived independently.

## Limits

- The patched counter differs from the frozen one only at line 4 (diff shown). No check, constant, path string (other than the repo root), or branch was altered, so conclusions transfer to the lane counter; but the lane counter itself was exercised only against the real lane at two revisions, where it is correctly unmet because the entry is absent.
- Nothing here remediates: no edit to `count-c2.py`, the contract, the entry path, or `SOURCES.md`; no commit, no jj mutation, no product-code change; no provider-health inference.
- C1 (`count-c1.py`) was not attacked — out of this seat's scope.
- Scratch repositories were deleted after the report; the appendix rebuilds all eleven fixtures and was executed end-to-end, printing the same eleven outcomes reproduced above (commit ids differ because commits are fresh).

## Reproduce (verbatim; run as `sh reproduce.sh <scratch-root>`)

```sh
#!/bin/sh
# Rebuilds the Mo57Scribe54 C2-counter fixtures in <root>. Nothing outside <root> is written.
set -eu
ROOT=${1:?usage: reproduce.sh <scratch-root>}
LANE=/home/vgpnk/Projects/shokunin/mori-shokunin
mkdir -p "$ROOT/bin"
python3 - "$LANE/.ufo/waves/round-57/count-c2.py" "$ROOT/bin/count-c2-param.py" <<'PY'
import sys
src = open(sys.argv[1]).read()
old = 'R=sys.argv[1]; repo="/home/vgpnk/Projects/shokunin/mori-shokunin"'
new = 'R=sys.argv[1]; repo=sys.argv[2]  # ONLY the repo literal is parameterized; all checks byte-identical'
assert src.count(old) == 1, "counter literal changed upstream"
open(sys.argv[2], "w").write(src.replace(old, new))
PY
C="python3 $ROOT/bin/count-c2-param.py"
commit() { [ -d "$1/.git" ] || git -C "$1" init -q
            git -C "$1" -c user.name=fx -c user.email=fx@invalid add -A
            git -C "$1" -c user.name=fx -c user.email=fx@invalid commit -qm "$2"; }
registry_fake() { mkdir -p "$1/corpus"; cat > "$1/corpus/SOURCES.md" <<'EOF'
# SOURCES (fixture — synthetic rows only, no real source)

| id | title | kind | grade | scope | anchor | note | status | opened | recheck | copy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S001 | fixture baseline — https://example.invalid/baseline | docs | A | carries the word mined | none | baseline | mined | 2026-09-01 | on-release | none |
| S548 | fixture row, not mined, not opened this round — https://example.invalid/x | docs | A | none | none | placeholder | placeholder | 2026-01-01 | none | none |
EOF
}
entry_bad() { mkdir -p "$1/corpus/knowledge"; cat > "$1/corpus/knowledge/watchdog-unclosed-r57.md" <<'EOF'
# Watchdog `unclosed` (fixture entry — proves counter gaps, no real claim)

No S548 row was opened this round and no source copy exists anywhere in this fixture.

The phrase "pairing count" appears in this entry only as a negation: `unclosed` is
explicitly **not** a pairing count, and no present-running statement is made.

| Key `hdr` | Meaning |
| K1 | fabricated quote `a1 that resolves nowhere and is unbalanced |
| K2 | fabricated quote `a2` that resolves nowhere
| K3 | fabricated quote `a3` that resolves nowhere
| K4 | fabricated quote `a4` that resolves nowhere
| K5 | fabricated quote `a5` that resolves nowhere
| K6 | fabricated quote `a6` that resolves nowhere
| K7 | fabricated quote `a7` that resolves nowhere
EOF
}
# fx1: fake registry; S548 row pre-exists and is not mined; entry has no headers, no source copy,
#      a negated "pairing count", an unbalanced backtick, and a table header counted as a claim.
mkdir -p "$ROOT/fx1"; registry_fake "$ROOT/fx1"; commit "$ROOT/fx1" base
entry_bad "$ROOT/fx1"; commit "$ROOT/fx1" entry
echo "fx1  $($C "$(git -C "$ROOT/fx1" rev-parse HEAD)" "$ROOT/fx1" || true)"
# fx12: the real round-57 registry + one fabricated, unmined S548 row (word "mined" comes from 270 old rows)
mkdir -p "$ROOT/fx12/corpus/knowledge"
git -C "$LANE" show 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2:corpus/SOURCES.md > "$ROOT/fx12/corpus/SOURCES.md"
printf '%s\n' '| S548 | fixture row appended in scratch, never opened from any source — https://example.invalid/none | docs | A | nothing | none | none | placeholder | none | none | none |' >> "$ROOT/fx12/corpus/SOURCES.md"
entry_bad "$ROOT/fx12"; commit "$ROOT/fx12" real-registry-plus-fabricated-row
echo "fx12 $($C "$(git -C "$ROOT/fx12" rev-parse HEAD)" "$ROOT/fx12" || true)"
# fx3: entry and S548 row both exist before any round commit; later commit touches only README
mkdir -p "$ROOT/fx3"; cp -r "$ROOT/fx12/corpus" "$ROOT/fx3/"; printf 'seed\n' > "$ROOT/fx3/README.md"
commit "$ROOT/fx3" "entry and row already ancient"
printf 'unrelated\n' >> "$ROOT/fx3/README.md"; commit "$ROOT/fx3" "later: README only"
echo "fx3  $($C "$(git -C "$ROOT/fx3" rev-parse HEAD)" "$ROOT/fx3" || true)"
# fx4: registry has no table at all; S548 and "mined" occur only in prose
mkdir -p "$ROOT/fx4/corpus/knowledge"; cp "$ROOT/fx1/corpus/knowledge/watchdog-unclosed-r57.md" "$ROOT/fx4/corpus/knowledge/"
printf '%s\n' '# SOURCES (fixture)' '' 'Prose only, no table anywhere. A row would look like | S548 | but none exists.' 'Nothing here was mined from any source and nothing was opened this round.' > "$ROOT/fx4/corpus/SOURCES.md"
commit "$ROOT/fx4" prose-only
echo "fx4  $($C "$(git -C "$ROOT/fx4" rev-parse HEAD)" "$ROOT/fx4" || true)"
# fx5: proper S548 row but the word mined appears nowhere -> control, source=bad
mkdir -p "$ROOT/fx5/corpus/knowledge"; cp "$ROOT/fx1/corpus/knowledge/watchdog-unclosed-r57.md" "$ROOT/fx5/corpus/knowledge/"
printf '%s\n' '# SOURCES (fixture)' '' '| id | title | kind | grade | scope | anchor | note | status | opened | recheck | copy |' '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |' '| S548 | fixture row with no mining status | docs | A | none | none | none | none | 2026-01-01 | none | none |' > "$ROOT/fx5/corpus/SOURCES.md"
commit "$ROOT/fx5" no-mined-word
echo "fx5  $($C "$(git -C "$ROOT/fx5" rev-parse HEAD)" "$ROOT/fx5" || true)"
# fx6: entry never cites S548, only the unrelated token S5480
mkdir -p "$ROOT/fx6/corpus/knowledge"; cp "$ROOT/fx1/corpus/SOURCES.md" "$ROOT/fx6/corpus/"
printf '%s\n' '# Watchdog `unclosed` (fixture — no citation of S548)' '' 'S5480 is an unrelated fixture token. No source row is cited.' '`unclosed` is not presented as a pairing count anywhere in this entry.' '' '| Key `hdr` | Meaning |' '| K1 | fabricated `a1` |' '| K2 | fabricated `a2` |' '| K3 | fabricated `a3` |' '| K4 | fabricated `a4` |' '| K5 | fabricated `a5` |' '| K6 | fabricated `a6` |' '| K7 | fabricated `a7` |' > "$ROOT/fx6/corpus/knowledge/watchdog-unclosed-r57.md"
commit "$ROOT/fx6" s5480-token
echo "fx6  $($C "$(git -C "$ROOT/fx6" rev-parse HEAD)" "$ROOT/fx6" || true)"
# fx8: entry asserts the inversion (present-running) yet keeps the substring "pairing count"
mkdir -p "$ROOT/fx8/corpus/knowledge"; cp "$ROOT/fx1/corpus/SOURCES.md" "$ROOT/fx8/corpus/"
printf '%s\n' '# Watchdog (fixture — asserts the inversion)' '' '`unclosed` counts drivers that are present and currently running. The phrase' '"pairing count" is a misreading this entry rejects. S548 is cited as a string only.' '' '| Key `hdr` | Meaning |' '| K1 | present-running count `a1` |' '| K2 | present-running count `a2` |' '| K3 | present-running count `a3` |' '| K4 | present-running count `a4` |' '| K5 | present-running count `a5` |' '| K6 | present-running count `a6` |' '| K7 | present-running count `a7` |' > "$ROOT/fx8/corpus/knowledge/watchdog-unclosed-r57.md"
commit "$ROOT/fx8" inverted-semantics
echo "fx8  $($C "$(git -C "$ROOT/fx8" rev-parse HEAD)" "$ROOT/fx8" || true)"
# fx9: the eight rows live inside a fenced code block; there is no table
mkdir -p "$ROOT/fx9/corpus/knowledge"; cp "$ROOT/fx1/corpus/SOURCES.md" "$ROOT/fx9/corpus/"
{ printf '%s\n' '# Watchdog (fixture — claims inside a code fence)' '' 'S548 is cited as a string. `unclosed` is a pairing count, allegedly.' '' '```'; i=1; while [ "$i" -le 8 ]; do printf '| K%s | not a claim `a%s` |\n' "$i" "$i"; i=$((i+1)); done; echo '```'; } > "$ROOT/fx9/corpus/knowledge/watchdog-unclosed-r57.md"
commit "$ROOT/fx9" fenced-claims
echo "fx9  $($C "$(git -C "$ROOT/fx9" rev-parse HEAD)" "$ROOT/fx9" || true)"
# fx13: one statement repeated eight times
mkdir -p "$ROOT/fx13/corpus/knowledge"; cp "$ROOT/fx12/corpus/SOURCES.md" "$ROOT/fx13/corpus/"
{ printf '%s\n' '# Watchdog (fixture — one statement eight times)' '' 'S548 is cited as a string. `unclosed` is described as a pairing count.' ''; i=1; while [ "$i" -le 8 ]; do echo '| K'"$i"' | the same single statement `q` |'; i=$((i+1)); done; } > "$ROOT/fx13/corpus/knowledge/watchdog-unclosed-r57.md"
commit "$ROOT/fx13" duplicated-statement
echo "fx13 $($C "$(git -C "$ROOT/fx13" rev-parse HEAD)" "$ROOT/fx13" || true)"
# fx10: a well-formed eight-claim entry whose eighth row is indented by one space -> claims=7
mkdir -p "$ROOT/fx10/corpus/knowledge"; cp "$ROOT/fx1/corpus/SOURCES.md" "$ROOT/fx10/corpus/"
{ printf '%s\n' '# Watchdog (fixture — one row indented by one space)' '' 'source: S548' 'verified-at: 2026-10-27' 'recheck: on-release' '' '`unclosed` is a pairing count, not a present-running count.' ''; i=1; while [ "$i" -le 7 ]; do echo '| K'"$i"' | quote `q'"$i"'` |'; i=$((i+1)); done; echo ' | K8 | quote `q8` |'; } > "$ROOT/fx10/corpus/knowledge/watchdog-unclosed-r57.md"
commit "$ROOT/fx10" indented-row
echo "fx10 $($C "$(git -C "$ROOT/fx10" rev-parse HEAD)" "$ROOT/fx10" || true)"
# fx11: registry row written |S548| with no padding -> source=bad although the row is real
mkdir -p "$ROOT/fx11/corpus/knowledge"; cp "$ROOT/fx8/corpus/knowledge/watchdog-unclosed-r57.md" "$ROOT/fx11/corpus/knowledge/"
printf '%s\n' '# SOURCES (fixture)' '' '| id | title | kind | grade | scope | anchor | note | status | opened | recheck | copy |' '| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |' '|S548|fixture row without padding|docs|A|none|none|none|mined|2026-10-27|on-release|corpus/evidence/sources-r57/S548.src|' > "$ROOT/fx11/corpus/SOURCES.md"
commit "$ROOT/fx11" unpadded-registry-row
echo "fx11 $($C "$(git -C "$ROOT/fx11" rev-parse HEAD)" "$ROOT/fx11" || true)"
```

Verified end-to-end output of the appendix (`sh reproduce.sh /fast/scratch/hyaku/mori-r57/Mo57Scribe54/verify-run`):

```
fx1  C2=met claims=8 source=ok quotes=ok rev=2e01a75f...
fx12 C2=met claims=8 source=ok quotes=ok rev=ff2df835...
fx3  C2=met claims=8 source=ok quotes=ok rev=83833311...
fx4  C2=met claims=8 source=ok quotes=ok rev=558c0770...
fx5  C2=unmet claims=8 source=bad quotes=ok rev=13b4e6c3...
fx6  C2=met claims=8 source=ok quotes=ok rev=6058163e...
fx8  C2=met claims=8 source=ok quotes=ok rev=16383a8b...
fx9  C2=met claims=8 source=ok quotes=ok rev=dce7116f...
fx13 C2=met claims=8 source=ok quotes=ok rev=1ff44fdd...
fx10 C2=unmet claims=7 source=ok quotes=ok rev=b9908a75...
fx11 C2=unmet claims=8 source=bad quotes=ok rev=35a1ec8c...
```

Report: .ufo/waves/round-57/w1/Mo57Scribe54.md
