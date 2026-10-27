# Mo57Executor46 — round 57, wave w1 (executor, arm C1)

Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`; entering tip
`53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`; freeze
`618562c72a03dc4d17386b715357f863fd327274`. Assignment: inspect the round-56
routed receipt path/wording defects, execute the frozen C1 counter on the
entering revision, inspect the C1 counter implementation, and give an
independent recheck plan. Detection only: no edits, no commits, no
remediation. Every command below was run read-only (`git show`/`git cat-file`)
or inside seat scratch.

## 1. Frozen counter identity and entering-state execution

- Freeze-time bytes equal the working tree, so the counter I ran is the frozen
  one: `git show 618562c7:.ufo/waves/round-57/count-c1.py | sha256sum` →
  `7156fb4bb29f27881091b22dfa7ef3d661b1e955a1ec9a4d13e48013f1b368ec`;
  `sha256sum .ufo/waves/round-57/count-c1.py` → same. `count-c2.py` likewise
  `0fe9e6f4cdde0ac14bd8cad907e948edcb8a51f7c950622cf84cae5f1f75f742`.
- Command: `python3 .ufo/waves/round-57/count-c1.py 53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`
- Output (single line): `C1=unmet rows=0 evidence=bad rev=53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2`
- Exit: **1**.
- The line is **byte-identical** to the frozen control
  (`.ufo/waves/round-57/controls.txt`, `Output: C1=unmet rows=0 …`; `diff`
  of the two lines prints nothing; `Exit: 1` matches).
- Same result at the freeze tip: `python3 .ufo/waves/round-57/count-c1.py 618562c72a03dc4d17386b715357f863fd327274`
  → `C1=unmet rows=0 evidence=bad rev=618562c7…`, rc 1; and
  `git diff 53e2b476 618562c7 -- SCORECARD.md` is empty, so the freeze commit
  did not move the before-state.
- Before-state is real, not a counter artifact: the section the counter binds
  to (SCORECARD.md:596-604 at `53e2b476`) is the placeholder table
  `| — none yet — | | | |` with "none enter through this rollout". The only
  `driver-liveness`/`vote-binding` mention in SCORECARD at that revision is the
  round-56 **claim** row (5-column `| Claim | Axis | … |` schema, SCORECARD.md
  under `## Round 56 …`), which this counter never reads.

## 2. Counter map (`count-c1.py`, exact lines)

| line | behavior |
|---|---|
| 6 | repo path hard-coded to the lane worktree |
| 7 | `git -C repo show R:SCORECARD.md` — only committed bytes at `R` |
| 9 | `git show` failure → `C1=unmet rows=0 evidence=bad`, exit 1 |
| 10 | `split("## Capabilities",1)[1].split("## Saturation",1)[0]` — **first** `## Capabilities` section only |
| 11 | row = any line starting `|` containing `driver-liveness` **or** `vote-binding` |
| 12 | `ok = len(rows)==2 and all(".ufo/waves/round-56/" in x and "| 56 |" in x)` |
| 13-14 | verdict line, exit 0/1 |

Consequences to keep in view: `rows=0 evidence=bad` conflates "no rows" with
"rows present but pointers rejected"; there is no `failed=` token and no
`--selftest`, so the lane's usual arm-attribution and self-test conventions do
not apply to this counter.

## 3. Predicate vs implementation — measured discrimination defects

Predicate (contract): *"two rows naming `driver-liveness` and `vote-binding`,
each with a resolvable round-56 evidence pointer and first-working round 56."*

Method: one scratch git repo per case under
`/fast/scratch/hyaku/mori-r57/Mo57Executor46/fixN`, containing only
`SCORECARD.md`; the counter was copied to scratch with **only** the `repo`
constant replaced (frozen lane bytes untouched); each run used an explicit
`R = git -C fixN rev-parse HEAD`.

| case | planted shape | output | rc | contradicts predicate? |
|---|---|---|---|---|
| F1 `fe731910…` | two rows, pointers in the round-56 SCORECARD style `evidence/c1-at-landed.txt`, `evidence/tally-r55.txt` | `C1=unmet rows=2 evidence=bad` | 1 | yes — both files resolve under `.ufo/waves/round-56/`, yet rejected |
| F2 `fa8fb8da…` | two rows, pointers `.ufo/waves/round-56/evidence/does-not-exist.txt`, `…/also-absent.txt` | `C1=met rows=2 evidence=ok` | 0 | yes — "resolvable" is never checked, a fabricated pointer passes |
| F3 `a411c643…` | two rows **both** naming `driver-liveness` (second: `driver-liveness again`), no `vote-binding` row | `C1=met rows=2 evidence=ok` | 0 | yes — set coverage of the two required names is never tested |
| F4 `9ded4b30…` | the two correct rows placed under `## Capabilities (round 56 demonstrations)` after the empty top table | `C1=unmet rows=0 evidence=bad` | 1 | yes — correct placement in a per-round capability table is invisible |
| F5 `a6ae57d2…` | correct two rows under `## Capability register` | no stdout | 1 | yes — `IndexError: list index out of range` at line 10 instead of a verdict line |
| F6 `cc3594e0…` | two correct rows in the top table, full-form pointers | `C1=met rows=2 evidence=ok` | 0 | positive control: the intended after-shape does pass |

Detail and evidence:

- **D1 — "resolvable" implemented as a literal prefix.** SCORECARD.md at
  `53e2b476` cites `evidence/c1-at-landed.txt` and `evidence/tally-r55.txt`
  (short form, the round-56 convention). Resolution proof:
  `git cat-file -e 53e2b476:.ufo/waves/round-56/evidence/c1-at-landed.txt` →
  PRESENT; `git cat-file -e 53e2b476:evidence/c1-at-landed.txt` → `fatal: path
  'evidence/c1-at-landed.txt' does not exist` (there is no lane-root
  `evidence/`). F1 shows the counter rejects the form that actually resolves
  under the wave directory.
- **D2 — no resolution at all.** Line 12 only tests the substring
  `.ufo/waves/round-56/`. F2 shows two non-existent paths score `C1=met`.
  Variant not run but implied: `.ufo/waves/round-56/contract.md` (exists, is
  not capability evidence) also passes.
- **D3 — no name coverage.** Line 12 counts lines, it does not require
  `{driver-liveness, vote-binding} ⊆ names`. F3: two driver-liveness rows,
  `vote-binding` absent, `C1=met`. Substring matching also means the token may
  sit in any cell (the `What` or `Evidence` column), not necessarily the
  `Capability` cell.
- **D4 — undocumented table binding.** SCORECARD at the entering tip has
  **20** headings matching `^#{2,3} .*[Cc]apabilit`
  (`git show 53e2b476:SCORECARD.md | grep -cE '^#{2,3} .*[Cc]apabilit'`),
  including round-12/13/15/16/17/19/20/24/25/53 demonstration tables, one with
  a different schema (`| key | name | what it can now do | evidence | first
  working |`). `AXES.md:57-63` says only "SCORECARD.md … carries a separate
  `capabilities:` table". Line 10 silently binds to the first bare
  `## Capabilities` heading; F4 shows a row entered in a round-scoped table
  (the shape round 53 used) reads `rows=0`.
- **D5 — crash instead of unmet.** Renaming the bound heading makes line 10
  raise `IndexError`; stdout is empty, rc 1. Any "after" receipt for such a
  tree cannot be a `C1=…` verdict line.

The counter does accept the intended fix (F6), so C1 is reachable; the defects
are about **which** trees it accepts and rejects, not about unreachability.

## 4. Round-56 routed path/wording defects, verified

4.1 **Short-formed evidence pointers (defect 1).** The round-56 report
(`/home/vgpnk/Projects/shokunin/.ufo/reports/round-56/mori.md`) cites
`evidence/driver-liveness-live.txt` (line 21), `evidence/tally-r55.txt`,
`evidence/c2-old-counter-voted0.txt` (26), `evidence/controls.txt` ×2 (54, 59),
`evidence/c1-at-landed.txt` (56), `evidence/c2-at-landed.txt` (61),
`evidence/census-end.txt` (71, 81); line 123 mixes a full lane path with a
bare `c2-at-landed.txt`. The SCORECARD round-56 cell repeats the same form
(`evidence/c1-at-freeze.txt`, `evidence/c1-at-landed.txt`). No lane-root
`evidence/` exists; the committed location is `.ufo/waves/round-56/evidence/`.
LOG.md's round-56 entry (starts LOG.md:2950) uses the short form at :2954 for
four pointers (`evidence/c1-at-freeze.txt`, `evidence/c2-at-freeze.txt`,
`evidence/controls.txt`, `evidence/census-start.txt`) and the full form only
at :2960 (`.ufo/waves/round-56/evidence/census-end.txt`) — one entry, two
conventions.

4.2 **Receipt-shape phrasing (defect 2).** Report line 21: pointer
`evidence/driver-liveness-live.txt` then "(1728 lines, 0 malformed, 23 lanes)".
The receipt is a 304-line JSON document (`wc -l` → 304) whose fields are
`"log": {"lines": 1728, "malformed": 0}` and 23 keys under `"lanes"`
(`python3` json load of the file minus the trailing `exit=0`). The numbers are
right as fields; the parenthetical reads as a line count of the file.

4.3 **Asserted exit status with no receipt token.** `.ufo/waves/round-56/evidence/controls.txt`
carries **no** `exit=`/`rc=` token at all (`grep -c 'exit=\|rc='` → 0), yet
both SCORECARD round-56 Before cells and report lines 54/59 say "rc 1". The
control line is
`do-nothing-c1 PASS C1=unmet … failed=tool_absent rev=5b295eee…` — a
`PASS`/`FAIL` comparison result, not the counter's exit code.

4.4 **Truncated revision stamps.** The two do-nothing lines are each 144 chars
(`controls.py:92` does `verdict[:110]`, a character cut, not a token cut).
The result is `rev=5b295eeebd87ebd610d8d39b` (24 hex) on the C1 line and
`rev=5b295eeebd87ebd610d8d39bfe2035742` (33 hex) on the C2 line — the same
measured revision stamped at two different lengths, neither the full 40-hex
form. Both happen to resolve (`git rev-parse` on either prefix returns
`5b295eeebd87ebd610d8d39bfe2035742f740cfa`), but a rechecker diffing stamps
sees unequal revisions.

4.5 **Early-return arm labels (defect 3), read-only confirmation.**
`.ufo/waves/round-56/count-c2.py:65-69` returns `["tool_absent"]`; the printer
at 155-165 maps only the four named arms, so every other arm prints `ok`
(`do-nothing-c2 PASS C2=unmet selftest=ok tally=ok … entry=ok row=ok`). Not
re-executed — receipt bytes already show the shape.

**Coupling that matters for round 57:** 4.1 and 4.4 are the citation style the
lane actually uses, and the frozen C1 counter rejects exactly that style (F1)
while accepting a fabricated full-form pointer (F2). A capability row written
by copying the round-56 SCORECARD wording would be *true* and read `C1=unmet`;
a row with a plausible but non-existent path reads `C1=met`.

## 5. Independent recheck plan (for the C1 after-state; no edits)

Run from any cwd with `LANE=/home/vgpnk/Projects/shokunin/mori-shokunin` and
`R=<candidate revision>`:

1. **Frozen counter, verbatim.**
   `python3 $LANE/.ufo/waves/round-57/count-c1.py $R; echo rc=$?`
   Expected after-state: `C1=met rows=2 evidence=ok rev=$R`, rc 0.
2. **Bind the table the frozen counter binds** (do not guess which of the 20
   capability headings is meant):
   `git -C $LANE show $R:SCORECARD.md | awk '/^## Capabilities$/{f=1} f&&/^## Saturation$/{exit} f'`
   → exactly two data rows, both in the 4-column schema
   `| Capability | What it can now do | Evidence pointer | First-working round |`.
3. **Name coverage by column, not substring.**
   `… | awk -F'|' '/^\|/{gsub(/^ +| +$/,"",$2); print $2}' | sort | uniq -c`
   → one `driver-liveness`, one `vote-binding`, nothing else.
4. **Column-4 position check.**
   `… | awk -F'|' '/^\|/{gsub(/^ +| +$/,"",$5); print $5}'` → `56` twice
   (rejects `| 56 |` appearing in another cell).
5. **Resolve every pointer at `R`** (path relative to the lane root):
   `git -C $LANE show $R:SCORECARD.md | … | grep -oE '`\.ufo/waves/round-56/[^`]+`' | tr -d '`' | while read -r p; do git -C $LANE cat-file -e "$R:$p" || echo "UNRESOLVED $p"; done`
   → no `UNRESOLVED` lines.
6. **Tie each pointer to its capability's receipt, not just any round-56
   file.** For `driver-liveness`: `git -C $LANE show $R:.ufo/waves/round-56/evidence/c1-at-landed.txt`
   → `C1=met … rev=097c342b…`, `exit=0`; for `vote-binding`:
   `git -C $LANE show $R:.ufo/waves/round-56/evidence/c2-at-landed.txt` (or
   `tally-r55.txt`) → the matching `C2=`/`TALLY` line.
7. **Cross-check the stamps.** `git rev-parse` each stamped revision in the
   cited receipts; require the full 40-hex form and that the receipt's verdict
   tokens equal a fresh run of that round's own counter at the stamped
   revision (round-56 receipts: `c1-at-freeze.txt`, `c1-at-landed.txt`).

If the intent is instead to land the rows in a round-scoped capability table,
steps 1-2 disagree with the counter today (F4); that is a contract/counter
wording question for the L1, not something a rechecker can resolve by choosing
a reading.

Minimal counter corrections implied (recommendation only, not applied): require
`{"driver-liveness","vote-binding"} ⊆` the set of parsed column-2 cells; resolve
each pointer with `git cat-file -e R:<path>`; name the bound heading explicitly
(or scan all capability tables with the 4-column schema); emit
`C1=unmet … failed=section_absent` on a missing heading instead of raising;
distinguish `rows=0` from `evidence=bad`.

## 6. Limits and risks

- The five adversarial cases are **patched-copy** runs (only the `repo`
  constant replaced) against scratch repos holding a single `SCORECARD.md`;
  they exercise the frozen logic, not lane state. Fixture revision ids are
  listed above. Frozen lane bytes were not modified (sha unchanged).
- I did not execute the round-56 counters (out of scope for this arm) or the
  round-57 C2 counter; round-56 receipts were verified by reading committed
  bytes only.
- The counter's crash path (D5) means a future heading edit fails closed
  without a verdict token — a receipt for such a tree cannot be compared
  token-wise.
- `evidence=bad` is a single token for two different failures (no rows vs bad
  pointers), which limits how much a control reader can learn from the
  entering receipt.
- No production edits, commits, tool installs, or host remediation. Scratch
  (`/fast/scratch/hyaku/mori-r57/Mo57Executor46`, TMPDIR there) was removed
  after the evidence above was captured.

## Verdict

- C1 before-state reproduced exactly: `C1=unmet rows=0`, rc 1, identical to
  the frozen control; freeze commit leaves it unchanged.
- The frozen C1 counter does **not** test the predicate's "resolvable …
  evidence pointer" or the two-name coverage; it binds to one undocumented
  table by heading, and crashes (rather than reading unmet) when that heading
  is absent.
- Round-56 routed receipt defects 1, 2, 3, and the control-revision truncation
  are confirmed at the cited paths/lines; defect 1's short-form style is
  precisely the style the round-57 C1 counter rejects.
- No blockers; no changes made.
