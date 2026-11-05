# Mo94E01Replay — round-94 w1: independent replay of the C1 battery + four extra fixture classes

Seat: executor (leaf). Freeze `6b65e7c11f318481d5efa0429cdabb50743a2cc2`, entering base
`84b152308fa6c2f224ad75dff68e525dab9057ac`. All runs 2026-11-05 on this host, `python3 -I`,
`TMPDIR` pointed at the seat scratch `$S=/fast/scratch/hyaku/mori-r94/Mo94E01Replay` (deleted
before yield). One seat clone `$S/clone` at the freeze commit (`--shared --no-checkout`); the
battery's transient `controls-*` clone and my `$S/fixclone` are the frozen scripts' own method,
toplevel-asserted, inside scratch only. No tool installs. Lane untouched.

## 1. C1 counter v2 replay at the freeze commit

```
SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin TMPDIR=$S python3 -I \
  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-94/count-c1v2.py \
  6b65e7c11f318481d5efa0429cdabb50743a2cc2 --repo $S/clone
```
Observed (exit 0):
`C1=met trio=98 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=6b65e7c11f31`
Matches the contract expectation (`adm_ok=19`, exit 0). REPRODUCED.

## 2. Frozen controls battery

```
TMPDIR=$S python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-94/controls-r94.py \
  /home/vgpnk/Projects/shokunin/mori-shokunin /home/vgpnk/Projects/shokunin
```
Observed (exit 0):
```
CTRL do-nothing v1=C1=met v2=C1=met
CTRL do-nothing v1_line=C1=met trio=98 claim_r92_true=1 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=84b152308fa6
CTRL do-nothing v2_line=C1=met trio=98 files=19 adm_ok=19 adm_fail=0 patched12=12 seven_same=7 census=ok rev=84b152308fa6
CTRL left   rev=d003b8db899a v1=C1=met v2=C1=unmet v2_line=C1=unmet trio=98 files=19 adm_ok=18 adm_fail=1 patched12=12 seven_same=7 census=ok checks_failed=admission rev=d003b8db899a
CTRL right  rev=31cdda539014 v1=C1=met v2=C1=unmet v2_line=C1=unmet trio=98 files=19 adm_ok=18 adm_fail=1 patched12=12 seven_same=7 census=ok checks_failed=admission rev=31cdda539014
CTRL middle rev=89349e8ce95c v1=C1=met v2=C1=unmet v2_line=C1=unmet trio=98 files=19 adm_ok=18 adm_fail=1 patched12=12 seven_same=7 census=ok checks_failed=admission rev=89349e8ce95c
EMBED_FALSE_PASS v1=3/3 v2=0/3 live_v2=met do_nothing_v1=C1=met do_nothing_v2=C1=met
```
Matches the frozen expectation (`v1=3/3 v2=0/3`, exit 0). REPRODUCED.

## 3. Extra fixture classes (a)–(d)

Method = `controls-r94.py` exactly: fixture clone of the lane, `git checkout -q --detach 84b15230`
before each class, ONE commit per class changing only the single `verified-at:` line of
`corpus/knowledge/counter-win-r77.md` (identity `Mo94E01Replay <replay@fixture.invalid>`,
`rev-parse --show-toplevel` asserted equal to the fixture dir before every commit; verified after:
each fixture rev's sole parent is `84b152308fa6…`). The admission hash is `ac=6a230c4b`
(`log --diff-filter=A --format=%h 7b3fe9d5… -- <rel>`), replaced once in the line with:
(a) deleted entirely; (b) `"0"+ac`; (c) `ac.upper()`; (d) `ac+ac`.
Frozen v1 read from the base revision (`git -C $S/clone show 84b15230…:.ufo/waves/round-93/count-c1.py`
→ 181 lines, its `/home/vgpnk` CENSUS literal at line 39 intact), run WITHOUT `--census`;
v2 = frozen `count-c1v2.py` WITH `--census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh`.

| class | forged token in `verified-at:` | fixture rev | v1 verdict (rc) | v2 verdict (rc) |
|---|---|---|---|---|
| a | hash deleted → line starts `verified-at:  (2026-…` | `1b6d99c5aca4` | `C1=unmet … adm_fail=1 … checks_failed=admission` (1) | `C1=unmet … adm_fail=1 … checks_failed=admission` (1) |
| b | `0`+ac = `06a230c4b` | `75255a15bf96` | `C1=met trio=98 claim_r92_true=1 … adm_ok=19 …` — **FALSE PASS** (0) | `C1=unmet … adm_fail=1 … checks_failed=admission` (1) |
| c | ac uppercased = `6A230C4B` | `e9163c973e4c` | `C1=unmet … adm_fail=1 … checks_failed=admission` (1) | `C1=unmet … adm_fail=1 … checks_failed=admission` (1) |
| d | ac twice = `6a230c4b6a230c4b` | `e3ae4e9f0ab3` | `C1=met trio=98 claim_r92_true=1 … adm_ok=19 …` — **FALSE PASS** (0) | `C1=unmet … adm_fail=1 … checks_failed=admission` (1) |

Every fixture run also carried `trio=98 files=19 patched12=12 seven_same=7 census=ok`, i.e. the
one-commit lineage held and only counter-win-r77.md's `verified-at:` line moved vs ENTERING.

**v2 false passes: none — 0/4.** v2 rejected every forged token, including the ≥7-char tokens
`06a230c4b` and `6a230c4b6a230c4b`, so the boundary it enforces is the prefix relation
(`ac.startswith(first_token)`, S624), not token length. Classification of the forged values:

- **b — admission forgery.** The token names `06a230c4b`, which is not the admission commit
  `6a230c4b…`; v1 false-passes because `6a230c4` is a substring of `06a230c4b` (P1 shape,
  leading-char variant of the battery's `left` fixture `f6a230c4b0`).
- **d — admission forgery.** The token embeds the admission hash inside a longer non-admission
  object name; v1 false-passes on the same substring defect (battery `right` shape).
- **a — omission, not a forgery.** No admission is named; nothing false is certified; both
  counters read the file unmet so the failure surfaces. Not a pass for either counter.
- **c — mangled admission name.** Uppercase names no valid git object spelling; rejected by both
  counters — but note v1's rejection here is incidental (case-sensitive `in`), not boundary-aware,
  and would flip to a false pass on any case-preserving corruption (as b and d show).

Adjacency: among (a)–(d) v1's only correct verdicts are rejections it reaches for the wrong
reason (substring absence, case); its false passes on (b)/(d) plus the battery's 3/3 confirm the
substring predicate cannot see token boundaries, while v2's rejections are all `checks_failed=admission`.

## Exact per-class command shape (class b shown; a/c/d identical modulo transform)

```
git clone --shared -q --no-checkout /home/vgpnk/Projects/shokunin/mori-shokunin $S/fixclone
git -C $S/fixclone rev-parse --show-toplevel            # printed $S/fixclone (asserted before any commit)
git -C $S/fixclone checkout -q --detach 84b152308fa6c2f224ad75dff68e525dab9057ac
ac=$(git -C $S/fixclone log --diff-filter=A --format=%h 7b3fe9d540c98b8b0390a0f9bbe78de4341092a5 -- corpus/knowledge/counter-win-r77.md)   # 6a230c4b
# line rewrite, same replace-once as controls-r94.py (scratch fixture only, not a lane edit):
python3 -I - $S/fixclone corpus/knowledge/counter-win-r77.md $ac leadzero   # lines[idx].replace(ac, "0"+ac, 1)
git -C $S/fixclone add corpus/knowledge/counter-win-r77.md
git -C $S/fixclone -c user.name=Mo94E01Replay -c user.email=replay@fixture.invalid -c commit.gpgsign=false commit -q -m "r94 replay fixture b"
python3 -I $S/count-c1-r93.py 75255a15bf96eb8af6ec9f1a5425dc6eb7e0cfa6 --repo $S/fixclone
python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-94/count-c1v2.py \
  75255a15bf96eb8af6ec9f1a5425dc6eb7e0cfa6 --repo $S/fixclone --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
```
Driver preserved verbatim during the run as `$S/run-fixtures.sh` (scratch, removed at cleanup).

## Result

- Step 1 reproduced: v2 reads `C1=met adm_ok=19` at the freeze commit, exit 0.
- Step 2 reproduced: battery `EMBED_FALSE_PASS v1=3/3 v2=0/3`, exit 0.
- Step 3: v1 false-passes 2/4 extra classes (b, d — both admission forgeries); v2 false-passes 0/4;
  no claim-kill condition observed (no v2 false pass, live data still met, census ok everywhere).
- NOT RUN: none. No destructive lane/host operation; no installs to record.
