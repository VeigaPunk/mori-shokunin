# ExecDriftLive — live drift sweep re-run vs committed receipt (round 37, w1)

Attacks: **C2's `live` evidence** — `evidence/drift-live-r37.txt` as a reproducible live sweep of the
scored tip. Read-only seat: no lane file was edited; all runs are the lane's own read-only tool and
counter. Scratch only under `/fast/scratch/hyaku/mori-r37/ExecDriftLive/`.

## 1. The assigned command, as run

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin && timeout 900 python3 tools/mori-source-drift.py --root . ; echo EXIT=$?
```

Observed (stdout saved to `/fast/scratch/hyaku/mori-r37/ExecDriftLive/drift-live-now.txt`, stderr empty):

```
MORI_SOURCE_DRIFT rows=225 fresh=53 excerpt=0 drifted=10 unavailable=0 no-copy=162
EXIT=1
```

**Summary line: `MORI_SOURCE_DRIFT rows=225 fresh=53 excerpt=0 drifted=10 unavailable=0 no-copy=162`.  Exit code: 1.**

Reproduced a second time, byte-identical to the first run (`diff` of the two outputs: no output):

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin && timeout 900 python3 tools/mori-source-drift.py --root . > drift-live-rerun2.txt 2>&1; echo EXIT=$?
→ EXIT=1, diff run1 run2 → IDENTICAL
```

## 2. Committed receipt, as committed

```
grep -n 'MORI_SOURCE_DRIFT\|^EXIT=' .ufo/waves/round-37/evidence/drift-live-r37.txt
222:MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162
223:EXIT=1
```

Shape differs between the scored tip and the current working tree, because HEAD advanced while this
seat ran (`git rev-parse --short HEAD` → `1ae1d6d`):

| rev | lines | line 1 | summary | EXIT |
|---|---|---|---|---|
| scored tip `e57c58b` (blob) | 222 | `S001 no-copy` | `:221` | `:222` |
| HEAD `1ae1d6d` (worktree, clean) | 223 | `command: timeout 900 python3 tools/mori-source-drift.py --root .` | `:222` | `:223` |

```
git show e57c58b:.ufo/waves/round-37/evidence/drift-live-r37.txt | wc -lc   → 222 2851
git show e57c58b:…drift-live-r37.txt | sed -n '1p'                        → S001 no-copy
git show HEAD:…drift-live-r37.txt | wc -lc                                 → 223 2916
git show 5631efa -- …drift-live-r37.txt   → +command: timeout 900 python3 tools/mori-source-drift.py --root .
```

The `command:` line was prepended by `5631efa` ("receipt erratum (commands + repo-relative paths)")
— the run itself was **not** regenerated, only a header added; `round-36/evidence/drift-live-r36.txt`
carries no such header (`grep -c '^command:'` → 0), so the two rounds' receipts now have different
shapes over an identical summary.

Receipt summary: `rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162`, exit 1.

## 3. Diff (receipt vs live)

```
diff <(grep -v '^EXIT=' .ufo/waves/round-37/evidence/drift-live-r37.txt) \
     <(grep -v '^EXIT=' /fast/scratch/hyaku/mori-r37/ExecDriftLive/drift-live-now.txt)
1d0
< command: timeout 900 python3 tools/mori-source-drift.py --root .
222c221,226
< MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162
---
> S221 fresh
> S222 fresh
> S223 drifted
> S224 fresh
> S225 fresh
> MORI_SOURCE_DRIFT rows=225 fresh=53 excerpt=0 drifted=10 unavailable=0 no-copy=162
DIFF_EXIT=1
```

The `1d0` is the receipt-only `command:` header: the tool never emits one (`grep -n 'command'
tools/mori-source-drift.py` → no hits; both of my captures start at `S001 no-copy`), so that line is
hand-written into the receipt. Against the scored-tip blob the same diff is `221c221,226` exactly —
the receipt's 220 row lines all match.

Prefix check — the receipt's 220 row lines are byte-identical to the live run's first 220 rows
(receipt rows are blob lines 1-220 at the scored tip, lines 2-221 at HEAD):

```
diff <(sed -n '2,221p' .ufo/waves/round-37/evidence/drift-live-r37.txt) \
     <(sed -n '1,220p' .../drift-live-now.txt)   → PREFIX_220_IDENTICAL_HEAD
diff <(git show e57c58b:…drift-live-r37.txt | sed -n '1,220p') \
     <(sed -n '1,220p' .../drift-tip.txt)        → PREFIX_220_IDENTICAL_TIP
```

Drifted sets:

```
receipt : S156 S157 S158 S159 S160 S176 S177 S210 S211              (9)
live    : S156 S157 S158 S159 S160 S176 S177 S210 S211 S223         (10)
```

`unavailable=0` in receipt and in both live runs — **the count delta is not a network-unavailable
row.** It has two causes, both measured below.

## 4. Cause A — the receipt describes the round-36 registry population, not round 37's

```
git show e57c58b57c025364e79d130fbdf764d2674d83d6:corpus/SOURCES.md | grep -c '^| S[0-9][0-9][0-9] '
225
grep -c '^| S[0-9][0-9][0-9] ' corpus/SOURCES.md      → 225
grep -c '^S[0-9][0-9][0-9] ' .ufo/waves/round-37/evidence/drift-live-r37.txt  → 220
git show 8ff9bba:corpus/SOURCES.md | grep -c '^| S[0-9][0-9][0-9] '  → 220
```

The scored tip's registry has **225** rows (`corpus/SOURCES.md:227-231` = S221–S225); the receipt
carries **220** row lines. Its summary is byte-identical to the round-36 receipt:

```
diff <(sed -n '222p' .ufo/waves/round-37/evidence/drift-live-r37.txt) \
     <(sed -n '221p' .ufo/waves/round-36/evidence/drift-live-r36.txt)  → SUMMARY_IDENTICAL_TO_ROUND36
```
(HEAD line numbering: r37 summary at `:222`, r36 at `:221`; on the scored-tip blob it is `:221`.)

So the round-37 "live" receipt is the round-36-population sweep (the last tree state where
`SOURCES.md` had 220 rows), committed at `e57c58b` in the same commit that appended S221–S225.

Run at the **exact scored tip** (tree extracted read-only via `git archive e57c58b | tar -x -C
scratch/tip`, then `python3 tools/mori-source-drift.py --root .` inside it):

```
EXIT=1
S224 fresh
S225 no-copy
MORI_SOURCE_DRIFT rows=225 fresh=52 excerpt=0 drifted=10 unavailable=0 no-copy=163
```

(`S225 no-copy` at the tip because `corpus/evidence/sources-r37/S225.src` landed later, at
`52d636d`; at HEAD it is `fresh`, giving `no-copy=162`.) Its S001–S220 lines are also identical to
the receipt (`PREFIX_220_IDENTICAL_TIP`). **No tree state of the scored tip reproduces the
receipt's summary line.**

Independent corroboration from another seat's untracked receipt
`.ufo/waves/round-37/evidence/drift-live-r37-tip.txt` (working tree, header: "at the 225-row
registry, all five r37 copies committed"): `MORI_SOURCE_DRIFT rows=225 fresh=53 excerpt=0
drifted=10 unavailable=0 no-copy=162`, `EXIT=1` — it matches my HEAD run on every row and differs
from my exact-tip run only at S225 (`fresh` vs `no-copy`), the copy-presence delta above.

## 5. Cause B — S223 (opened this round) is genuinely drifted, on a build timestamp only

```
sha256sum corpus/evidence/sources-r37/S223.src  → 6576f56d0487d6621d3cca0eae70a278d9ff67d7b1b66bf07d989e714ce31532
curl -sSL -A 'mori-source-drift/1.0' https://docs.python.org/3/library/urllib.request.html  (twice, 20:11 and 20:16 UTC)
  → e0285ef5e3504d75a21d6f190537c282890950b2c3dd2f8109ee1bd7352b5741  (both fetches identical)
diff corpus/evidence/sources-r37/S223.src S223.live.html
1953c1953
<       Last updated on Oct 23, 2026 (19:41 UTC).
---
>       Last updated on Oct 23, 2026 (19:57 UTC).
```

One changed line, a CPython-docs build timestamp; `S223.src:1953` vs the live body. `classify()`
hashes the whole body and only tests `copy.strip() in body` for `excerpt`, so a docs page that
rebuilds its "Last updated" line can never be `fresh`. The row is byte-unreproducible by
construction, and it is one of this round's own admissions (`corpus/SOURCES.md:229`).

Note the receipt's own prose claim is false at the tip: `corpus/knowledge/source-drift-hardening-r37.md:64-66`
("The nine drifted ids … this run reproduces the same nine") and `corpus/README.md:589` ("the same
nine rows as round 36") — at the scored tip it is **ten**, and the tenth is S223. Neither
`corpus/knowledge/source-drift-r36.md` nor `…-hardening-r37.md` discloses volatile-timestamp pages
as a limit (grep for `timestamp|volatile|Last updated` → no hits).

## 6. Cause C — the C2 gate pins the stale sentence

`python3 .ufo/waves/round-37/count-c2.py e57c58b57c025364e79d130fbdf764d2674d83d6` (read-only run) →
`C2=met`, exit 0, all eight checks PASS. But the `live` check is a substring test against a
hardcoded string:

```
.ufo/waves/round-37/count-c2.py:49  LIVE_SENTENCE = "MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162"
.ufo/waves/round-37/count-c2.py:208-211  live = show(repo, args.rev, LIVE_REL); check("live", live is not None and LIVE_SENTENCE in live, ...)
```

An honest regenerated receipt (`rows=225 … drifted=10 …`) would make `check live` **FAIL**. The
gate therefore rewards the stale bytes: it verifies that a frozen round-36 summary string is
present, not that a round-37 sweep reproduces.

## 7. Risks

- C2's `live` binding cannot distinguish "live receipt" from "round-36 receipt renamed". Any future
  registry append leaves it green while the receipt silently diverges from the corpus.
- The erratum pass already exercised that gap: `5631efa` (HEAD ancestry) prepended
  `command: timeout 900 python3 tools/mori-source-drift.py --root .` to the receipt without
  re-running it, and `count-c2.py` stayed green because the pinned sentence was untouched. Round 36's
  receipt has no `command:` header, so the two rounds now present different shapes over a byte-identical
  summary — a header alone is what the wave's "commands" correction added here, not a fresh run.
- S223 sets a permanent floor of `drifted=1` for the probe (exit always 1), which breaks the probe's
  own exit-0-when-nothing-drifted contract as a usable signal for the rest of the corpus.
- Row lines S001–S220 remain trustworthy: they are byte-identical across receipt, tip run and HEAD
  run, so the nine pre-existing drifted rows are unchanged since round 36 — only the population and
  S223 differ.

## 8. Blockers

None. No tool installed or upgraded; no pacman; no lane mutation (only read-only `git log/show/
cat-file/ls-tree/rev-parse/diff/archive`, with `git archive` output written to scratch). No
subagent dispatched.

## 9. What the mismatch is, in one line

The committed round-37 live receipt is the round-36-population sweep (`rows=220`, summary
byte-identical to `round-36/evidence/drift-live-r36.txt:221`), committed at the tip whose registry
has 225 rows and whose own new row S223 is already drifted by a docs build timestamp; the live
re-run is `rows=225 fresh=53 excerpt=0 drifted=10 unavailable=0 no-copy=162`, exit 1
(`rows=225 fresh=52 … no-copy=163` on the exact tip tree), so the summary line does not match.

Acceptance determination: exit code 1 is inside the allowed `1 or 0`, but the summary line is not
the receipt's — and the delta is not a network-unavailable row (`unavailable=0` in all three runs:
receipt, tip tree, HEAD tree). Conjunctive criterion unmet.

**VERDICT: FAIL** — `e57c58b:.ufo/waves/round-37/evidence/drift-live-r37.txt:221` (HEAD
`1ae1d6d:…:222`) reports `rows=220 fresh=49 drifted=9 no-copy=162`, while the same commit's
`corpus/SOURCES.md:227-231` holds 225 rows and the live sweep at that tree yields
`rows=225 fresh=52 drifted=10 no-copy=163` (on the exact tip) / `rows=225 fresh=53 drifted=10
no-copy=162` (at HEAD); the stale sentence is pinned as the pass condition at
`.ufo/waves/round-37/count-c2.py:49`, and S223's timestamp-only drift
(`corpus/evidence/sources-r37/S223.src:1953`) contradicts
`corpus/knowledge/source-drift-hardening-r37.md:64-66` and `corpus/README.md:589`.
