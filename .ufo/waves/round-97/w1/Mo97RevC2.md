# Mo97RevC2 — C2 landed-bytes review (mori round 97, w1)

Reviewer seat. Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`. Freeze `dd1ae1150f53df54e7530311b2323368e3c0e5e9`, landing `e85ed91249953094b067554bfa79fcdc65791f8e`.
Lane HEAD = `e85ed912…` and `git status --porcelain` is empty for `corpus/SOURCES.md`, `corpus/lessons/round-97.md`, `corpus/evidence/sources-r97` → working tree bytes == landed bytes. All commands read-only; no repo mutation; no installs.

## (1) SOURCES.md diff adds exactly one row, no existing byte changed — PASS

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin diff --numstat dd1ae1150f53df54e7530311b2323368e3c0e5e9 e85ed91249953094b067554bfa79fcdc65791f8e -- corpus/SOURCES.md
1	0	corpus/SOURCES.md
```

Full diff body: exactly one hunk `@@ -406,6 +406,7 @@`, zero `-` lines; the single `+` line is the S628 registry row, inserted after S627 and before the blank line + `## Paths`. No existing byte changed; CORPUS rule 2 append-only held — S615's own row still carries its mis-recorded digest (`…8f1a60ad1a6f0`, the r91 C-1 record) and was correctly NOT edited (contract: "edits no recorded digest"). S628 is the next unused id (max existing S627). Row cells: kind=code, tier=B, status=mined, opened=2026-11-05, recheck=90d, used-by=`corpus/lessons/round-97.md` (exists; the lesson cites S628) — enums valid, `mined` backed by its used-by path.

## (2) Pinned bytes vs recorded digests — PASS

```
$ sha256sum corpus/evidence/sources-r97/{S615,S616,S623}.html S628.md
7891c58897fe9f78cf16d15fd3464b746a187214c82587ac94b0f83b9a8a42f5  S615.html   362493 B
6842ed0f53882c5a4d7a852ff969842f62aba92f918e2192db0df6ed23c3cb72  S616.html    53982 B
90ac3b25cb2dd28192a5d1c7d45da5ef966d32666d0c583a13eb2ec6f4831ad0  S623.html   171073 B
0ae6b8806cbb28edd4f8b1ae98ac5045ced71234ba8c81dfa3bf7312eccac618  S628.md       6835 B
```

Recorded digests: row S619 `7891c588…42f5` (= S615 pin ✓, the correction of record), row S616 `6842ed0f…cb72` ✓, row S623 `90ac3b25…31ad0` ✓, row S628 `0ae6b880…c618` ✓. All four byte sizes match the counts recorded in the rows. 4/4 match, 0 mismatch.

## (3) `superseded-by S619` legitimate — PASS

- Row S619 `teaches` opens verbatim `supersedes S615 — the registry should record this full diges…` — the CORPUS rule 2 correction form.
- `cmp /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r97/S615.html /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-90/w1/Mo90S01Sources/sources/python-ast-3.15.2.html` → identical (S619's pinned copy IS the S615 pin; S619's recorded full digest equals both).
- Independent reconstruction of the Gate's S615 live-fetch claim, from local bytes only: pin stamp at line 3328 is `Last updated on Nov 05, 2026 (00:37 UTC).`; replacing only that stamp with `(12:47 UTC)` yields
  `d5d9d590abfda6b55a9469b9330e42f25bdb0bc28f2e6490f18797d671265e8f`, 362493 B — exactly the lesson's live claim `d5d9d590…5e8f`, 362,493 B.

## (4) Lesson Gate block — PASS, three nits (none blocking)

Backed by bytes: S628 URL + raw URL; access 2026-11-05 ~20:45 UTC, HTTP 200, 6835 B, sha `0ae6b880…c618` (all match the pin); located quote present at raw lines 6-7 of the pin. S615 row fully reconstructed locally (§3). S616 stamp `(00:37 UTC)` present at pin line 704; S623 stamp `(08:02 UTC)` at pin line 1911. S616's live digest `bce32489…da0e` independently corroborated by `controls-r97.txt` (`copy_sha=bce324892ae8b1c3` in the "today's live S616 bytes" forgery control). The rejection paragraph's three controls appear in `controls-r97.txt` with exactly the cited outcomes (`mismatch=1`; `hole_guard=fail`; `content-drift` + `checks_failed=live`). `landing-c2.txt` prints `C2=met mismatch=0 unpinned=0 targets_ok=3/3 hole_guard=pass live=S615:time-churn,S616:time-churn,S623:time-churn` at rev `e85ed912…` with frozen `count-c2.sha256=957a7be6…` — the contract target line, verbatim.

Nits:
1. Number-drift: Gate says the S628 quote is "14 words"; the sentence is **12** words (`wc -w` on raw lines 6-7 = 12). The ≤25-word rule is still met; only the stated count is wrong.
2. The quote is a flattened rendering, not a verbatim byte substring: the pin wraps the sentence across lines 6-7 and renders the host as a markdown link `[docs.python.org](https://docs.python.org)`. The named location (raw lines 6-7) is accurate.
3. Unverified-by-me: S623's live digest prefix `57b7f76b…6811` in the Gate table is not corroborated by any committed byte I read (it is a live-fetch claim; no committed receipt line prints it). Its `(08:02 UTC)` stamp restoration is consistent with the pin.

## (5) Census — PASS

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
rc=0
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```
(43 W04 lines = the 42 before the round + the new S628 row; no other diagnostics.)

## Unrun checks

- Live re-fetch: this seat did not re-run `tools/mori-drift-recheck.py` against the network; the live leg is taken from `landing-c2.txt` (all three rows `time-churn` at 2026-11-05T20:50:05Z).
- S623 live digest equality not independently verified (see §4 nit 3).
- Assimilation claim `/home/vgpnk/Projects/shokuknow/merge/mori/` exists — outside the Gate table, not checked.

## VERDICT

C2 holds.
