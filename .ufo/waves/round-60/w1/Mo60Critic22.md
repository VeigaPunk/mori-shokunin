# Mo60Critic22 — grammar-orphan hunt (r60 C2 / H1)

Seat type: critic (attack). Read-only on the lane; no counter, contract,
SCORECARD, LOG or VCS mutation. Report only.

## Verdict

**Bypass confirmed — two classes, one scored end-to-end through the frozen
counter.**

1. **Orphan class (H1 false negative).** A line that any reader parses as a
   claim (bullet, ``K<n>``, em dash, ``Quote:``, backticked span, ``(file:line:N; pin <sha>)``) is
   silently skipped when it does not contain the byte substring `**K` *and*
   does not start (after `lstrip()`) with `-` while containing `Quote:`.
   The tool returns `ok=True` and the counter's line is **byte-identical to
   the frozen target** (`claims=13 files=6 spans=13`), so a false claim with
   a false quote leaves no trace in the scored output.
2. **Smuggle-past-the-grammar class (false quote while counting).** The
   claim *text* field `(.+?)` is never inspected. A claim's visible text can
   carry a fabricated quote, and a line may even embed a complete
   canonical-looking false claim + citation before the real citation; the
   regex swallows the false half as text and verifies only the last one.

Four secondary defects (H2/H3 reachability, not scoring falsifications) are
listed below. Nothing here falsifies the frozen C2 sentence as written
(capability-only this round); it shows the **routed r59 defect
"`grammar:` orphaning" is narrowed, not closed**, and the 13-tree hostile
set does not cover the class.

## Revisions and pins (every derivation pinned)

| Item | Value |
|---|---|
| Entering rev (contract) | `ddfb12fb0838b4307c445194a844f0c4b1950195` |
| Freeze rev (contract) | `ac496c7cde8cad965079858accae3bedfe4a73f2` |
| Lane HEAD at probe time (pinned for all runs) | `b3c256138f00c704d5aa56eb0332d74506502ef2` |
| Entry blob sha at `ac496c7c` and at `b3c25613` | `441a751de67f1cef9db265666a6f77734d7a9d964fe2efcf3756e4394716ce21` (identical — entry unchanged since freeze) |
| Tool blob sha | `cffe9f3359097277a7ea39729309efdc5831a1738994ceb30ee023ac0eae6e69` = `PIN_EC` (`count-c2.py:46`) |
| Tool at `ddfb12fb` | absent (`git show` empty → `e3b0c442…`, the empty-input sha) |

The lane working tree is dirty from other seats (C1 data landing:
`M corpus/lessons/round-60.md`, untracked `evidence/c1-at-data.txt`, `w1/`).
Every lane byte is read with `git -C <lane> show <rev>:<path>` or
`ls-tree`. The single working-tree read (the `h01` tree probe in F6) was
`git status`-clean against `b3c25613` before use
(`git diff --stat b3c25613 -- .ufo/waves/round-60/trees-c2h` printed nothing).

Scratch: `/fast/scratch/hyaku/mori-r60/Mo60Critic22/` (`TMPDIR` set there;
disk guard green before and after: `/fast` 26% used, 601G free before / 596G
after).
No tools installed or updated.

## Method

1. Materialized the frozen entry + `corpus/SOURCES.md` + the six pinned
   copies at `b3c25613` into a scratch root, with the **pin-verified** tool
   blob (`sha256 == PIN_EC`, asserted in the driver before every run).
2. Baseline (must reproduce the C2 target's claim statistics):
   `ok=True stats={'claims': 13, 'files': 6, 'spans': 13, 'min_span': 12}`,
   `reasons=[]`.
3. Inserted one probe line at a time after the last claim line and re-ran
   the same pinned tool with the same arguments the counter uses
   (`--min-claims 10 --min-files 3`).
4. End-to-end: `git clone --no-hardlinks <lane> <scratch>/endtoend/clone`,
   committed each probe there (throwaway repo; `git rev-parse --show-toplevel`
   asserted as the clone), and ran the **frozen counter** from the lane root
   with `--repo <clone> --scratch <scratch>`.
5. Tool selftest from the pinned blob: `ENTRYCLAIMS_SELFTEST pass=13 fail=0`,
   exit 0 — confirms the probed instance is the frozen one.

## F1 — Orphan class (primary bypass)

Predicate, verbatim (`tools/mori-entry-claims-check.py:114`):

```python
if "**K" in ln or (ln.lstrip().startswith("-") and "Quote:" in ln):
    reasons.append("grammar:%.40s" % ln.strip()[:40])
```

Both clauses are literal substring tests. Neither the bullet, the label
weight, the dash, nor `Quote`-with-a-lookalike-colon is normalised. A
claim-shaped line escapes whenever it misses **both**:

| Probe | Line (abridged) | Tool | Counter line |
|---|---|---|---|
| P01 | ``* K15 — … holds 99. Quote: ` "seats": 99,` (r54:line:5; pin ea48…)`` | `ok=True claims=13 reasons=[]` | unchanged |
| P02 | ``+ K15 — … Quote: ` "seats": 99,` (…)`` | `ok=True claims=13` | unchanged |
| P03 | ``- K15 — … Quote：` "seats": 99,` (…)`` (U+FF1A fullwidth colon) | `ok=True claims=13` | unchanged |
| P07 | ``* **k15** — … Quote: ` "seats": 99,` (…)`` (lowercase bold `**k`) | `ok=True claims=13` | unchanged |
| P09 | ``• K15 — … Quote: ` "seats": 99,` (…)`` (U+2022 bullet) | `ok=True claims=13` | unchanged |
| P10 | ``- **<ZWSP>K15** — … ` "seats": 99,` … (…)`` (bold broken by U+200B) | `ok=True claims=13` | unchanged |
| P15 | ``- K15 — … ` "seats": 99,` … (…)`` (no ``Quote:`` token, backticked false quote) | `ok=True claims=13` | unchanged |
| P22 | ``  * K15 — … Quote: ` "seats": 99,` (…)`` (indented) | `ok=True claims=13` | unchanged |
| ORD | ``1. K15 — … Quote: ` "seats": 99,` (…)`` | `ok=True claims=13` | unchanged |
| NNBSP | ``* **<U+202F>K15** — … Quote: …`` | `ok=True claims=13` | unchanged |
| TABSEP | ``* K15<TAB>— … Quote: …`` | `ok=True claims=13` | unchanged |
| DASHUD | ``— K15 — … Quote: …`` (em dash as bullet) | `ok=True claims=13` | unchanged |

Controls (the guard is genuinely narrow, not absent):

| Probe | Line variant | Result |
|---|---|---|
| P04 | `- **K15** – …` (U+2013 en dash separator) | `grammar:` |
| P06 | ``- `**K15**` — …`` (label inside a code span) | `grammar:` |
| P08 | `- K15 — … Quote:<ZWSP> …` (literal `Quote:` still present) | `grammar:` |
| P12 | `- **K15** — … pin EA48…` (uppercase hex) | `grammar:` |
| P05 | `- **K15** — …` + trailing spaces | counts (`claims=14`), fails `span:15` |
| HBAR | `– **K15** — …` (en dash bullet) | `grammar:` (contains `**K`) |
| CODEAST | ``* `**K15**` — …`` | `grammar:` |

So the named probes in the seat spec behave as follows: unicode lookalike
**separator** dashes → caught (only because `**K` is present); **double-star
variants** → caught unless the bullet is also non-`-`; **trailing spaces** →
caught; **K-label inside a code span** → caught. The hole is the *joint*
avoidance of `**K` and `-`+`Quote:`.

### End-to-end (scored path)

Sandbox clone, entry + one orphan line (`P01` form) committed:

```
$ git -C $S/clone rev-parse HEAD
71713cc177d4f8a65cb2597e014bc76d066e1cb9
$ cd <lane> && python3 .ufo/waves/round-60/count-c2.py 71713cc1… --repo $S/clone --scratch $S/s-orphan
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=71713cc177d4f8a65cb2597e014bc76d066e1cb9
exit=0
```

Baseline on the same clone at `b3c25613`:

```
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=b3c256138f00c704d5aa56eb0332d74506502ef2
exit=0
```

The two lines differ **only** in `rev=`. The entry at the scored revision
carries a false claim ("the seats field holds 99", quoting a non-existent
` "seats": 99,`) and the counter cannot tell.

## F2 — False quote smuggled while counting (text field unverified)

Regex (`ec.py:52-54`):

```
^- \*\*K(\d+)\*\* — (.+?) Quote: `([^`]+)` \((\S+?):(line|offset):(\d+); pin ([0-9a-f]{64})\)\s*$
```
The text group is non-greedy free text; only the **last** quote clause is
bound — ``Quote:`` plus a backticked span plus the
`` (…:line|offset:N; pin <64hex>)`` tail at end-of-line.

| Probe | Line (abridged) | Result |
|---|---|---|
| S1 | ``- **K1** — … holds 99 (quoted: ` "seats": 99,`). Quote: ` "seats": 74,` (r54:line:5; pin ea48…)`` | `ok=True claims=13 files=6 spans=13 min_span=12` |
| S3 | ``- **K15** — seats holds 99 Quote: ` "seats": 99,` (r54:line:5; pin ea48…) and Quote: ` "round": 55,` (r55:line:3; pin 2e5b…)`` | `ok=True claims=14 spans=14` |

S3 is the sharper form: the text contains a **complete canonical false
claim including its own well-formed citation**; the parser backtracks past it
and binds the trailing true citation. Both halves carry real 64-hex pins, so
nothing looks malformed.

End-to-end with S1 committed (`41d892ae7faea8a16e1ac302f29f7a5902dc3945`):

```
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=41d892ae7faea8a16e1ac302f29f7a5902dc3945
exit=0
```

Identical to the frozen target except `rev=`. The entry text now asserts a
false fact and prints a fabricated quote; every machine check passes.

## F3 — `spans == claims` is satisfiable with overlapping windows

`ec.py:162` keys distinctness on the exact triple `(cfile, start, end)`;
partial overlap is not detected. Two offset claims at `n` and `n+1` over the
same 12-byte region of `w1-results-r55.json` line 3 (both byte-true, both
8+ bytes):

```
ok=True stats={'claims': 15, 'files': 6, 'spans': 15, 'min_span': 11}
```

`count-c2.py:332` (`spans == claims`) therefore certifies "13 distinct
spans" even when every span is a shifted window over a handful of bytes.
Whether this is a defect depends on reading "distinct byte spans"; exact
aliasing collapsing is implemented, overlapping-window collapsing is not.

## F4 — `MIN_SPAN` is length, not distinct bytes

`ec.py:49`: `MIN_SPAN = 8     # H2: minimum distinct bytes per claim span`;
`ec.py:168`: `if end - start < MIN_SPAN`. The byte *content* is never
counted. Minimal fixture (4 claims quoting `xxxxxxxx` / `yyyyyyyy` at offsets
0 and 4, each spanning **one distinct byte**):

```
ok=True reasons=[] stats={'claims': 4, 'files': 2, 'spans': 4, 'min_span': 8}
```

Contract H2 says "≥8 distinct bytes per span". Either the wording must read
"≥8 bytes", or the check must add `len(set(q)) >= MIN_SPAN`. As frozen, a
span of 8 identical characters certifies a claim.

## F5 — Claim-label identity is not `int`-closed

`ec.py:119-121` compares `kid` as the raw string; `\d` in the regex is
Unicode-aware. `- **K１** …` (U+FF11, fullwidth one) at a fresh span:

```
ok=True stats={'claims': 14, 'files': 6, 'spans': 14}
```

The entry now has two claims a reader renders as "K1". `distinct:dup_kid`
never fires. Not a quote-integrity break, but the unique-label invariant H1
implies is bypassable.

## F6 — Hostile-tree coverage gap and lower-bound expect matching

Scanned all 13 committed tree entries (`trees-c2h/*/corpus/knowledge/…r59.md`):
every claim-shaped line is canonical `- **K…**`. Only two trees carry a
malformed line and both are canonical-spelled: for `h01` the line
``- **K99** — dangling claim with no pin or span``; for `h02` the line
``- **K77** — malformed claim line missing quote and pin``.
**No tree exercises an orphan-shaped line**, i.e.
the class in F1 — so `FROZEN_EXPECTS` (`count-c2.py:83-98`) cannot see it.

Reason matching in the tree arm is a **prefix/lower bound**
(`count-c2.py:397-403`: `all(any(r.startswith(e) …))`). Demonstrated live on
`h01`: its frozen expect is `["distinct:dup_span", "text:short"]`, but the
tool also emits `grammar:- **K99** …`, and the counter still reports
`trees=ok`. Consequence: `h02`'s `["grammar"]` certifies "some grammar block
happened", not "K77 was blocked". Adding an F1 orphan next to K77 would not
change the tree's verdict.

## Over-block (not a bypass, one line)

`- **K1**` prose mentioning the grammar in a code span blocks the entry
(``grammar:The claim grammar is - **K1** — text Qu…``, truncated at 40 chars).
The entry cannot
document its own claim syntax. Also `selftest(scratch=None)` (`ec.py:242`)
ignores the `--scratch` value the counter passes; it only works because
`run_pinned` exports `TMPDIR` (`count-c2.py:151`). Dead parameter, no
security effect.

## Impacted axes

* **C2 depth** — H1 token "`grammar:` reasons block the verdict": true for
  the strings it recognises, false as a closure of r59's "grammar: orphaning"
  defect. H2 token "distinct byte spans": exact-alias only (F3), and
  "≥8 distinct bytes" is implemented as length (F4). H3 unchanged.
* **C3 operability / G3 expectgate** — frozen expect tables are complete for
  their own trees but do not cover the F1 class, and reason matching is a
  lower bound (F6), so a tree can pass with the intended cause unexercised.
* **C1** — not implicated; this seat touched no C1 arm.
* Current state is **not** a live exploit: the r59 entry at `b3c25613` has
  13 canonical claims, **zero** orphan-shaped lines, and zero lines
  containing `**K` outside claims.

## Smallest safe correction (proposal only — nothing edited)

Counter bytes, contract and predicates are frozen after scoring, so these
are round-61 (or pre-scoring amendment) items, not edits I made.

1. **H1 made structural, not lexical** (one predicate). Fire `grammar:` when
   a line is a list item (`^\s*\d+\.|^\s*[-*+•–—]`), **or** contains a
   64-hex token, **or** contains `Quote`/`quote` adjacent to a backtick —
   unless `CLAIM` matches. All 12 orphan probes in the F1 table are caught
   by the first two hooks (and P22's indented `*` by the list-item hook);
   the three real prose lines in the entry (`K1–K5…`,
   `K11's absence…`, `K12–K14 quote…`) are not list items, carry no 64-hex
   token and no backticked quote, so they stay clean.
   Measured on the frozen blobs: `honest entry false-positive lines: 0`,
   `orphans caught=15 missed=0` over the 15 non-canonical claim-shaped probe
   lines in the batch, including ORD, DASHUD, NNBSP, TABSEP.
2. **One new hostile tree** `h13-orphan-claim` = `h00` bytes + one line
   ``* K15 — … Quote: ` "seats": 99,` (r54:line:5; pin ea48…)``, frozen
   expect `["grammar"]`. This is the tree that F1 needs and the current set
   lacks; it must be added with the amendment, before scoring.
3. **Bind the text field**: reject a claim text containing a backticked
   8+ byte span, or reject any `Quote:`/`quote:` token inside the text group
   (one regex change, `ec.py:52-54`). Kills F2 (S1/S3) without touching the
   pinned-quote path.
4. **Distinctness**: key on overlapping intervals, not the exact triple
   (`ec.py:162`), if "distinct byte spans" means disjoint evidence; or
   restate the token as "non-identical spans".
5. **`MIN_SPAN`**: use `len(set(q))` or change the comment/contract wording
   from "distinct bytes" to "bytes" (F4).
6. **Label identity**: `kid = str(int(kid))` before the `seen_kids` compare
   (F5).
7. **Expect matching**: make `FROZEN_EXPECTS` cause-specific (e.g.
   `grammar:- **K77**`) and require exact reason-set equality, so a tree
   cannot pass on an unrelated cause (F6).

## Disposition

Fixable defect, not a tradeoff the canonical Rust judge must reject, and not
a falsification of the frozen C2 sentence (which is capability-only this
round and whose verdicts on the 13 frozen trees + the real r59 entry are
reproduced exactly). The routed r59 item "`grammar:` orphaning" is
**partially closed**: the canonical-spelling forms are blocked, the
non-canonical spellings are not, and the counter's output is unchanged in
both directions.

## What was not done

No edits to the lane (other than this report), counter, contract, SCORECARD,
LOG or `corpus/`; no commits in the lane; the only git writes happened in
`/fast/scratch/hyaku/mori-r60/Mo60Critic22/endtoend/clone` (throwaway clone,
toplevel asserted before each mutation). No pacman, no installs, no
`agent://all`, no seat spawns. Scratch removed after this report was written.
