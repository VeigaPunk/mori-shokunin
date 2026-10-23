measured 2026-10-23 (attempt 2, wave 2, seat `ExecReC2A`)

# ExecReC2A — re-score the measured claim C2 with a fresh draw

Item attacked: **C2 (operability, measured)** — the frozen counter
`.ufo/waves/round-36/count-c2.py` scoring the landed tip
`bf0df77fee4b6ef54a90aea09335c7617f125151` against the frozen predicate P-C2.

Scope note: this seat re-scored C2 only. It did **not** touch C1 (declared exploratory, no freshness
verdict), did not judge the wave, did not commit/push, and did not modify any lane file other than
this report. The lane repo was read-only for every command below except writing this file.

---

## 1. Full output and exit code (the required paste)

Command:

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin && python3 .ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151
```

Output (verbatim) and exit code:

```
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /tmp/mori-c2-pzu7e172/mori-sources-appendonly.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.6s; coverage: deletions=21 changed-back=14 superseded=8)
real arm: pass (0.4s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=8419795354949530892
EXIT_CODE=0
```

(The run above is the sixth independent draw of this seat; the first, second, third, fourth, fifth and
seventh draws are in §4 and returned the same verdict.)

---

## 2. Verification checklist demanded by the assignment

| # | demanded property | result | evidence |
|---|---|---|---|
| 1 | first line byte-identical to `contract.md:23` | **PASS** | see §2.1 |
| 2 | blind arm 24/24 | **PASS** | `blind arm: 24/24 sandbox histories matched the hidden truth` in every one of 7 fresh draws |
| 3 | real arm pass | **PASS** | `real arm: pass (0.4s)` in every draw |
| 4 | real-arm `ids` lists exactly 18 ids | **PASS** | see §2.2 |
| 5 | final line `C2=met` | **PASS (with a formatting note)** | see §2.3 |
| 6 | a fresh seed printed | **PASS** | 7 distinct fresh seeds; the receipt seed `15440749816798970567` appears only in the deliberate replay of §4.1 |
| 7 | `sha256sum .ufo/waves/round-36/count-c2.py` matches `evidence/freeze-v2.txt` | **PASS** | see §2.4 |

### 2.1 First line vs `contract.md:23` — byte-identical

```
$ head -1 /fast/scratch/hyaku/mori-r36/ExecReC2A/run2.txt > /fast/scratch/hyaku/mori-r36/ExecReC2A/firstline.txt
$ sed -n '23p' .ufo/waves/round-36/contract.md > /fast/scratch/hyaku/mori-r36/ExecReC2A/contract23.txt
$ cmp firstline.txt contract23.txt && echo "BYTE_IDENTICAL=YES"
BYTE_IDENTICAL=YES
$ sha256sum firstline.txt contract23.txt
5bfa852ce057fab1ca4d5c376f8cc65c7abe1babbbffc725898a6914a8998b11  /fast/scratch/hyaku/mori-r36/ExecReC2A/firstline.txt
5bfa852ce057fab1ca4d5c376f8cc65c7abe1babbbffc725898a6914a8998b11  /fast/scratch/hyaku/mori-r36/ExecReC2A/contract23.txt
```

The same line at the landed tip and at the freeze-time contract commit is byte-identical too:

```
$ git show c1a026cb156c5fe84d76dc79190f1885ad11abf4:.ufo/waves/round-36/contract.md | sed -n '23p' | sha256sum
5bfa852ce057fab1ca4d5c376f8cc65c7abe1babbbffc725898a6914a8998b11  -
$ git show bf0df77fee4b6ef54a90aea09335c7617f125151:.ufo/waves/round-36/contract.md | sed -n '23p' | sha256sum
5bfa852ce057fab1ca4d5c376f8cc65c7abe1babbbffc725898a6914a8998b11  -
```

`git diff c1a026c..tip -- contract.md` is a pure 14-line append at the end of the file (the
"C1 declared exploratory before data" section); it does not touch line 23.

### 2.2 Real-arm ids count = 18

```
$ grep -o 'ids=\[[^]]*\]' run2.txt | head -1 | tr ',' '\n' | grep -c 'S[0-9]'
18
```

The 18 ids are `S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193`,
identical in the `tool:` line and the `oracle:` line of every draw, and identical to the ids in the
landed receipt `.ufo/waves/round-36/evidence/c2-after.txt`.

### 2.3 Output layout note (not a defect)

The counter's last **two** lines are `C2=met` and `seed=<n>` — the seed is printed *after* scoring, so
the literal final line is the seed line, not `C2=met`. This is the frozen counter's own format
(`count-c2.py:718-720`: `print("C2=%s" % ...)` then `print("seed=%d" % seed)`), it is identical in the
landed receipt `evidence/c2-after.txt`, and the assignment's "final line `C2=met`" is read here as
"the verdict line is `C2=met`". Nothing to change.

### 2.4 Counter bytes vs `evidence/freeze-v2.txt`

```
$ sha256sum .ufo/waves/round-36/count-c2.py
c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34  .ufo/waves/round-36/count-c2.py
$ grep -n '' .ufo/waves/round-36/evidence/freeze-v2.txt
1:round-36 freeze v2 (L1 MoriR36), 2026-10-23T12:03:04Z; supersedes the v1 counter bytes of evidence/freeze.txt for the claims (v1 receipts stay as C0 history)
2:dbd3f6d793239a2f729f89778847eb47b901167fa7a98f57269621f4273c4127  contract.md
3:86dd3b7ab2d2563bbc811e83717b35dfea3d69717dab4d41d454f8b87c8764c0  count-c1.py
4:c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34  count-c2.py
5:C0 under v2: 25 controls unmet, 0 met (evidence/c0-rescore-v2.txt); REF1 C1=met, REF2 C2=met
```

`count-c2.py` matches freeze-v2 line 4 **exactly**. The counter is also unmodified in the working tree
(`git status --porcelain .ufo/waves/round-36/count-c2.py` → empty) and identical at the landed tip
(`git show <tip>:.ufo/waves/round-36/count-c2.py | sha256sum` → same
`c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34`). `count-c1.py` likewise matches
freeze-v2 line 3 (`86dd3b7a…64c0`).

---

## 3. What the counter actually scored (no substitution of a substitute tool)

The counter extracts the tool from the **landed tip**, not from the working tree:

```
$ git show bf0df77fee4b6ef54a90aea09335c7617f125151:tools/mori-sources-appendonly.py | sha256sum
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  -
$ sha256sum tools/mori-sources-appendonly.py
915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89  tools/mori-sources-appendonly.py
```

Tip bytes == working-tree bytes == the sha recorded by the w1 builder (`w1/BuildAppendTool.md`), so
the scored program is the landed one. The real arm runs on the lane repository itself (v2 design: no
clone), read-only git only (`count-c2.py:624-632` → `clone = os.path.abspath(repo)`), and the oracle is
the counter's own independent `git log` walk (`count-c2.py:527-585`), not the tool's output.

---

## 4. Fresh draws (7 independent) and one deliberate replay

Each scored run draws its seed from `os.urandom` (`count-c2.py:669`), so the blind arm's 24 sandbox
histories are re-drawn every time. All 7 fresh draws: `C2=met`, exit 0, blind 24/24, real arm pass,
identical 18 ids.

| draw | seed | blind arm | coverage (del/chg-back/sup) | verdict |
|---|---|---|---|---|
| 1 | 3496665012100012422 | 24/24 | 23 / 15 / 10 | `C2=met`, exit 0 |
| 2 | 18290729886888114082 | 24/24 | 20 / 13 / 11 | `C2=met`, exit 0 |
| 3 | 8086187816692358836 | 24/24 | 19 / 17 / 9 | `C2=met`, exit 0 |
| 4 | 6004094269588333236 | 24/24 | (see run output) | `C2=met`, exit 0 |
| 5 | 85008167832987007 | 24/24 | (see run output) | `C2=met`, exit 0 |
| 6 | 8419795354949530892 | 24/24 | 21 / 14 / 8 | `C2=met`, exit 0 |
| 7 | 2206341690523803048 | 24/24 | 21 / 14 / 12 | `C2=met`, exit 0 |

The blind-arm coverage counters differ from draw to draw, which shows the histories are genuinely
re-drawn rather than replayed from a fixture; all stay above the frozen minimums the counter itself
enforces (`count-c2.py:703-707`: deletions ≥ 12, changed-back ≥ 12, superseded ≥ 1, else exit 2).

### 4.1 Replay of the landed receipt's seed (determinism check only)

```
$ python3 .ufo/waves/round-36/count-c2.py bf0df77fee4b6ef54a90aea09335c7617f125151 --seed 15440749816798970567
... blind arm: 24/24 sandbox histories matched the hidden truth (5.5s; coverage: deletions=22 changed-back=17 superseded=10)
... real arm: pass (0.7s)
... C2=met
seed=15440749816798970567
EXIT_CODE=0
```

This reproduces the landed receipt `evidence/c2-after.txt` (same coverage triple
`22/17/10`, same 18 ids, same `superseded=[S069,S182,S193]`, same `round_changed=[S182,S193]`,
same seed) — the landed receipt is a receipt of these counter bytes. The replay is *not* a scored
draw; the verdict above rests on the 7 fresh draws.

---

## 5. Falsification attempts on the counter's discriminating power

The counter was run with `--tool` control/mutant paths (never editing the lane's real tool; mutants
were written to `/fast/scratch/hyaku/mori-r36/ExecReC2A/ctrl/`). All three were caught:

| mutant | what it does | counter result |
|---|---|---|
| `j1_empty.py` | prints an empty summary, exit 0 (contract control J1) | `C2=unmet`, exit 1 — `diff: superseded: want=['S069','S182','S193'] got=[]`, `diff: round_changed: want=['S182','S193'] got=[]`, `diff: violations: want=18 got=0` |
| `mut_rev.py` | the real tool with the `ids` list reversed (mutant of the landed tool) | `C2=unmet`, exit 1 — blind arm fails and real arm reports `diff: ids: want=[...S041] got=[...S193]` |
| `mut_hardcode.py` | hardcodes the lane's real-arm answer and ignores its input (overfit to the lane) | `C2=unmet`, exit 1 — the **real arm alone passes** (`real arm: pass`) but the blind arm fails, because the blind truth is drawn at run time and never written where the program can read it |

The third mutant is the important one: a program that simply memorises the lane's answer is rejected,
so the pass is not attributable to a memorised or harness-keyed program.

---

## 6. Cross-checks of the surrounding routed state (read-only)

The counter's real arm is pinned by the frozen predicate to `rev 6bd57097, round base f10a320d`
(`count-c2.py:44-45`), i.e. it exercises the lane's history at the round's **entering** tip, not the
landed tip's own `corpus/SOURCES.md`. The landed round's own registry state was therefore checked
directly with the registered gate:

```
$ python3 tools/mori-sources-appendonly.py bf0df77fee4b6ef54a90aea09335c7617f125151 --round-base 6bd57097
changed S041 superseded_by=S206
changed S044 superseded_by=S207
changed S051 superseded_by=S208
changed S062 superseded_by=S209
changed S064 superseded_by=S210
changed S069 superseded_by=S073
changed S179 superseded_by=S211
changed S180 superseded_by=S212
changed S181 superseded_by=S213
changed S182 superseded_by=S201
changed S183 superseded_by=S214
changed S184 superseded_by=S215
changed S185 superseded_by=S216
changed S186 superseded_by=S217
changed S188 superseded_by=S218
changed S189 superseded_by=S219
changed S190 superseded_by=S220
changed S193 superseded_by=S202
appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
exit=0
```

`round_changed=[]`, exit 0 — reproduces the L1's stated round append-only gate result. All 18
in-place-edited ids carry a superseder at the landed tip (15 of them from the new rows S206–S220,
plus the older S073 → S069, S201 → S182, S202 → S193), which corroborates the routed round-35 repair
"18 in-place-edited ids discharged".

Other read-only gates at the landed tip:

```
$ python3 tools/mori-sources-appendonly.py --selftest
MORI_SOURCES_APPENDONLY_SELFTEST pass=8 fail=0
exit=0

$ bash tools/mori-index-clean.sh /home/vgpnk/Projects/shokunin/mori-shokunin
MORI_INDEX_CLEAN staged=0 intent_to_add=0
exit=0
```

Index state directly: `git diff --cached --name-only | wc -l` → 0; intent-to-add entries
(`git ls-files --debug | grep -c 20000000`) → 0; untracked files under `corpus/` → 0 (the 3647
untracked paths in the repo are all under `.scratch/round22/`, 9 under `.ufo/waves/`, 1 scratch html —
none in `corpus/`). The round-36 gate registry row exists in `SKILL.md:862-865` and the gate table
row at `SKILL.md:873`; QUALITY 103–105 exist at `corpus/QUALITY.md:822`, `:829`, `:837`.

---

## 7. Advisory observations (no defect in C2; reported, not remediated)

1. **`evidence/freeze-v2.txt:2` no longer matches `contract.md`.** Freeze-v2 records
   `dbd3f6d793239a2f729f89778847eb47b901167fa7a98f57269621f4273c4127  contract.md`, but the file at
   the landed tip is `065a17b523b29840df8f1d516ca50eedb0da5e7d614198567439514a099dd93b` (the
   `dbd3f6d7…` bytes are the pre-`5842dc0` version). Cause: the contract was amended **after** the
   freeze, before data, by the pre-declared C1-exploratory section (14 appended lines; line 23
   unchanged, byte-identical sha `5bfa852c…`). The counters — the artifacts the freeze receipt
   actually pins for the claims — are byte-identical to freeze-v2, and P-C2's sentence is unchanged,
   so the landed C2 receipt remains a receipt of this claim. But a reader who hashes `contract.md`
   against freeze-v2 line 2 gets a mismatch. The L1 may want a one-line re-pin (or a note that the
   contract hash is superseded by `5842dc0`); this seat does not edit the lane.
2. **Exit-code wording in `contract.md:76`** — "with `--round-base` exit 1 iff `round_changed` is
   non-empty, else exit 1 iff ids or deleted is non-empty; otherwise 0" reads, under a literal
   chained parse, as exit 1 also when `round_changed` is empty but `ids` is non-empty. The landed tool
   (`tools/mori-sources-appendonly.py:493-495`), the registered gate row (`SKILL.md:873`) and the
   counter's own blind-arm expectation (`count-c2.py:603`,
   `expected_exit = 1 if truth["round_changed"] else 0`) all implement the *mode-exclusive* parse
   (`--round-base` ⇒ exit mirrors `round_changed` only). The mode-exclusive parse is the one the
   round's own gate usage requires (the landed tip has 18 pre-existing endpoint violations, so the
   chained parse would make the round gate always exit 1 and unusable), so this reads as loose
   contract prose rather than a tool defect — but the sentence is ambiguous and worth tightening.
3. The real arm's oracle is fixed to the entering tip by the frozen predicate, so the round-36
   registry additions themselves (rows S205–S220 and the superseders) are verified by the direct
   gate run in §6, not by the counter's real arm. Both agree; no gap in the round's gate coverage.
4. **Stray untracked bytecode in the lane** (not created by this seat): `git status --porcelain`
   lists `?? .ufo/waves/round-36/__pycache__/count-c2.cpython-314.pyc` (mtime 2026-10-23 15:34).
   Running `count-c2.py` as a script never writes a `.pyc` (only `import` does), so this came from
   another seat importing the counter as a module. It is under `.ufo/`, not `corpus/`, so it does
   not affect the C1 real arm's "no untracked file under `corpus/`" condition (`corpus/` untracked
   count = 0, §6), and it is not staged or intent-to-add (index-clean gate: `staged=0
   intent_to_add=0`). Flagged for the L1 only; this seat does not delete it (not this seat's file,
   and the lane is read-only here).

---

## 8. Risk register

- **Provider/network:** none. C2's counter is offline (local git + local sandbox repos); no HTTP was
  performed by this seat.
- **Mutation risk to the lane:** none. Every command was read-only (`git show`, `git log`,
  `git status`, `git diff`, `git ls-files`, `git rev-parse`); the counter and the lane tools are
  read-only git programs by construction (`tools/mori-sources-appendonly.py:44-45`: only `rev-parse`,
  `log`, `show`). No `git add/commit/push/fetch/reset`, no mutating `jj` command, no `pacman`.
- **Tool installs:** none performed by this seat, so nothing to record under the operator's tooling
  authorization. Scratch space used: `/fast/scratch/hyaku/mori-r36/ExecReC2A/` only.
- **Chance of a false pass:** low and bounded — the blind arm's truth is drawn at run time and the
  hardcoded-answer mutant (§5) is rejected, so the pass cannot come from memorisation.

VERDICT: PASS — C2 re-scored with 7 fresh draws (blind arm 24/24 each, real arm pass each,
`C2=met`, exit 0, 18 ids, fresh seed every time); the counter's bytes match
`evidence/freeze-v2.txt:4` exactly, the predicate line is byte-identical to `contract.md:23`
(sha `5bfa852ce057fab1ca4d5c376f8cc65c7abe1babbbffc725898a6914a8998b11`), and three control/mutant
programs (empty summary, reversed ids, hardcoded lane answer) are all scored `C2=unmet` by the same
counter, so the pass is discriminating. No defect found in the C2 claim. Two advisory observations
are reported in §7 (stale `contract.md` hash in `evidence/freeze-v2.txt:2`; ambiguous exit-code
prose in `contract.md:76`) — neither touches the predicate, the counter bytes, or the verdict.
