# Mo57Reviewer22 — round-56 routed defect: receipt path/wording (independent recheck)

Scope: the receipt **path/wording** cluster routed to round 57 —
`corpus/lessons/round-56-verifier-spotcheck.md` routed defects 1–3, plus the
`corpus/lessons/round-56.md` "Named limits routed to round 57" receipt-craft
items (freeze-sha256 `@rev` suffix, absolute paths, header commit naming,
controls verdict truncation). Detection and report only; no edits; frozen
contract/counters/kill rules untouched. Lane repo at entering revision
`53e2b4768af93dd2472eb26ecc9b9fdca2e9daf2` (freeze `618562c7`); all commands
below are read-only and were executed at that state.

## Verified defects

### D1 — MED · evidence-pointer paths are short-formed (routed defect 1, confirmed and wider than stated)
- Fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-56/mori.md`
  cites `evidence/…` at lines 21, 26, 54, 56, 59, 61, 71, 81 (e.g. line 21:
  `` `evidence/driver-liveness-live.txt` (1728 lines, 0 malformed, 23 lanes). ``).
- No `evidence/` directory exists at fleet root or lane root (`test -d` →
  ABSENT both). The committed location is
  `.ufo/waves/round-56/evidence/` in the **lane** repo.
- Same short form in `LOG.md:2954` (round-56 section:
  `evidence/c1-at-freeze.txt`, `evidence/controls.txt`,
  `evidence/census-start.txt`) and `corpus/lessons/round-56.md:39,46`.
- All values verify at the real paths — citation-precision defect only, as
  routed. No counterexample found against the underlying receipts.

### D2 — LOW · receipt-shape phrasing "(1728 lines, …)" (routed defect 2, confirmed)
- `mori.md:21` and `LOG.md:2952` say "1728 lines"; the receipt file
  `.ufo/waves/round-56/evidence/driver-liveness-live.txt` is **304 lines**
  (`wc -l`), and 1728 is the JSON field `"lines": 1728` at receipt line 282
  (the measured `.ufo/watchdog.log` length, not the receipt's size).
- Counterexample reading: a re-deriver comparing `wc -l` (304) against the
  prose (1728) concludes the receipt was replaced. Fix class: phrase as
  "log lines=1728" or cite the field (`receipt:282`).

### D3 — LOW · count-c2 early-return arm labels read `ok` (routed defect 3, confirmed in frozen code)
- `count-c2.py` at `8be2717b`: `evaluate()` returns `["tool_absent"]` early
  (line ~69), and the print block (lines ~158–163) labels any arm not in the
  failed list `ok` — so `evidence/controls.txt:2` reads
  `do-nothing-c2 PASS C2=unmet selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok … failed=tool_absent`
  with nothing evaluated.
- `count-c1.py` at the same commit has an explicit early-return branch
  printing every arm `bad` (lines ~188–191); `controls.txt:1` shows
  `selftest=bad fixtures=bad …`. Same semantics, opposite wording, in two
  frozen counters. Truthful in `C2=unmet failed=tool_absent`; the arm labels
  are the wording defect. Counters are frozen this round — route stands.

### D4 — MED · `@rev` suffix breaks `sha256sum -c` on the pin sheet
- `evidence/freeze-sha256.txt` lines 9–10 name
  `tools/mori-driver-liveness.py@6ced9da9` and `tools/mori-vote-bind.py@6ced9da9`.
- Executed from a `git archive` of `8be2717b`, wave dir, against the
  committed sheet:
  ```
  contract.md: OK ; count-c1.py: OK ; count-c2.py: OK ; controls/controls.py: OK
  sha256sum: tools/mori-driver-liveness.py@6ced9da9: No such file or directory
  sha256sum: tools/mori-vote-bind.py@6ced9da9: No such file or directory
  WARNING: 2 listed file(s) could not be read    (TRUE_RC=1)
  ```
- The round's fence instrument cannot be consumed by the standard checker as
  committed. The pins themselves are real (see D5) — integrity holds;
  consumability and wording fail.

### D5 — MED · pin-sheet header commit naming is wrong, and unsuffixed lines mix two commits
- Sheet header: `# data commit 6ced9da9b1f9c65065a8158735e0331938e8a599`.
- At `6ced9da9` the entire `.ufo/waves/round-56/` tree is **absent**
  (`git archive 6ced9da9` contains no wave dir; per-file `git show` empty).
- Actual pin attribution (computed via `git show <rev>:<path> | sha256sum`):

  | pinned file | pin | matches commit |
  |---|---|---|
  | contract.md `088761f3…` | `3f494b49` (identical at `8be2717b`) |
  | count-c1.py `c4e58eed…` | `3f494b49` (identical at `8be2717b`) |
  | count-c2.py `4b350c77…` | `3f494b49` (identical at `8be2717b`) |
  | controls/controls.py `5bf65ac0…` | **only `8be2717b`** (at freeze `3f494b49` it was `08620c17…`) |
  | tools/mori-driver-liveness.py `6b3dba74…` | `6ced9da9` (changed from `5befd490…` at `c419fe6d`) |
  | tools/mori-vote-bind.py `8be1acdb…` | `c419fe6d` == `6ced9da9` (unchanged) |

- So the `@6ced9da9` suffix is accurate only for the two tool lines; the four
  unsuffixed lines pin at two different commits under a header naming a
  commit that contains none of them. The sheet is internally consistent only
  at `8be2717b`, which it never names. (Corroborates Mo56ExecBinderControls'
  finding that the controls receipt is anchored to no frozen revision.)

### D6 — MED (latent) · absolute-path lines hash the worktree, not a revision
- Sheet lines 12–13 use absolute paths into the lane worktree
  (`/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r56/…`).
- Running `sha256sum -c` from the `8be2717b` **archive** verified those lines
  against the **live worktree**, not the archived bytes. They pass today only
  because worktree bytes equal the `6ced9da9` blobs (`61a5378f…`,
  `38ba3e6b…`, both confirmed). Any worktree edit or foreign checkout
  silently re-baselines the check — the defect routed in the lesson, shown
  live.

### D7 — MED · controls verdict truncation cuts the revision stamps
- `controls/controls.py` at `8be2717b`, do-nothing receipt loop:
  `line(name, "PASS"…, verdict[:110])`.
- `evidence/controls.txt:1` stamp is `rev=5b295eeebd87ebd610d8d39b` (24 of 40
  hex); line 2 is `rev=5b295eeebd87ebd610d8d39bfe2035742` (33 of 40).
- The do-nothing receipt — the Before evidence the SCORECARD cites — violates
  the round's own r55-defect-2 fix ("receipts stamp the measured revision"):
  neither line carries a complete, paste-safe revision. The counter receipts
  do (`c1-at-freeze.txt`/`c2-at-freeze.txt` carry full `rev=3f494b49…`;
  `c1-at-landed.txt`/`c2-at-landed.txt` carry full `rev=097c342b…`), so the
  asymmetry is confined to the controls receipt. controls.txt also carries no
  `exit=` markers (corroborates Mo56RevReceipts' MED).

### D8 — MED (new, same class) · the routed-defect carrier itself cites a fleet-only pointer without repo qualification
- `corpus/lessons/round-56-verifier-spotcheck.md:5,9` (committed in the lane
  at `53e2b476`): `report: .ufo/reports/round-56/mori.md (commit a1c32aa4…)`,
  with the recheck command `` git log --format='%an %H' -- .ufo/reports/round-56/mori.md ``.
- That path and commit resolve **only in the fleet repo**
  (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-56/mori.md` exists;
  `git -C /home/vgpnk/Projects/shokunin cat-file -t a1c32aa4…` → `commit`).
  From the lane repo, where the lesson lives: `git cat-file -t a1c32aa4…` →
  `fatal: … could not get object info`; no lane `.ufo/reports/round-56/`.
- A lane-side re-deriver following the lesson verbatim fails at step 1. Fix
  class: same as D1 — qualify repo and full path
  (`fleet:/home/vgpnk/Projects/shokunin/.ufo/reports/round-56/mori.md`).

### D9 — LOW (residual) · the correction receipt under-captures two of its four numbers
- `evidence/census-end.txt` (34 lines) captures the landing counting command
  and count (`# row counting command: grep -cE …` → `320`) — the QUALITY-152
  fix. But `# rows at entering tip 5b295eee:` → bare `316` and
  `# malformed-row check (expect 0):` → bare `0` carry **no command bytes**
  (the `git show 5b295eee:corpus/SOURCES.md | grep -cE …` variant is
  derivable but not captured).
- The uncorrected narrative lines still state the retyped number with no
  in-line qualification: `LOG.md:2954` "census start rc 0, 316 rows, 23 W04
  (`evidence/census-start.txt`)" and `corpus/lessons/round-56.md:46`
  "(`exit=0`, 316 rows, 23 W04)" — while `census-start.txt` (25 lines) has no
  `rows` token at all (`grep -c rows` → 0). The appended correction paragraph
  (`LOG.md` end of round-56 section; lesson lines 100–110) is the only
  repair, consistent with append-only convention — recorded here so a
  recheck reads the correction before judging the line.

## What is already fixed (contrast — do not re-route)
Round-55 routed defect 2 (measurement-revision misattribution) is fixed for
the counter receipts: `c1-at-landed.txt`/`c2-at-landed.txt` stamp
`rev=097c342b6c7d71444c0d81c9615197dc87d59c50` and the SCORECARD/spot-check
cite that stamped value. The residual stamp defects are D7 (controls line
truncation) and the sheet-level ambiguity (D4–D6).

## Independent recheck plan (non-author, read-only, ~2 minutes)
Let `R=/home/vgpnk/Projects/shokunin/mori-shokunin`,
`F=/home/vgpnk/Projects/shokunin`, `W=$R/.ufo/waves/round-56`. Expected
outputs at entering revision `53e2b476…`:

1. **Short paths (D1):**
   `grep -n 'evidence/' $F/.ufo/reports/round-56/mori.md | grep -v '\.ufo/waves'`
   → ≥7 hits (lines 21, 26, 54, 56, 59, 61, 71, 81);
   `test -d $F/evidence || test -d $R/evidence` → both ABSENT;
   `grep -n 'evidence/census-start' $R/LOG.md` → hit at 2954.
2. **Phrasing (D2):** `wc -l $W/evidence/driver-liveness-live.txt` → `304`;
   `grep -n '"lines": 1728' $W/evidence/driver-liveness-live.txt` → line 282;
   `sed -n '21p' $F/.ufo/reports/round-56/mori.md` → the "(1728 lines, …)"
   prose.
3. **Arm-label asymmetry (D3):** compare `$W/evidence/controls.txt` lines 1–2
   (`bad…bad` vs `ok…ok` on the same `failed=tool_absent`); code:
   `git -C $R show 8be2717b:.ufo/waves/round-56/count-c2.py | sed -n '154,166p'`
   vs `git -C $R show 8be2717b:.ufo/waves/round-56/count-c1.py | sed -n '186,192p'`.
4. **Pin sheet standard consumption (D4):**
   `mkdir -p <scratch>/w56b && git -C $R archive 8be2717b | tar -x -C <scratch>/w56b
   && cd <scratch>/w56b/.ufo/waves/round-56 && sha256sum -c evidence/freeze-sha256.txt`
   → 4× OK, 2× "FAILED open or read" on the `@6ced9da9` names, rc 1.
5. **Pin attribution (D5):** for each row of the table in D5, run
   `git -C $R show <rev>:<path> | sha256sum` at revs
   `c419fe6d/6ced9da9/3f494b49/8be2717b` and confirm the match columns; at
   `6ced9da9`, `git -C $R show 6ced9da9:.ufo/waves/round-56/contract.md`
   fails (file absent) — header wrong.
6. **Worktree hashing (D6):** repeat step 4 but flip one byte in a scratch
   copy of the worktree file — expect the absolute-path line to FAIL while
   the archive is untouched, proving the check follows the worktree.
7. **Truncation (D7):**
   `awk '{for(i=1;i<=NF;i++) if($i~/^rev=/) print NR": "length($i)-4}' $W/evidence/controls.txt`
   → `1: 24`, `2: 33` (full sha = 40);
   `git -C $R show 8be2717b:.ufo/waves/round-56/controls/controls.py | grep -n 'verdict\[:110\]'`
   → the truncation site; contrast `grep -o 'rev=[0-9a-f]*' $W/evidence/c1-at-landed.txt`
   → 40 hex chars.
8. **Cross-repo pointer (D8):**
   `git -C $R cat-file -t a1c32aa4344a448d6772744fa06b1632056ada0b` → fatal;
   `git -C $F cat-file -t a1c32aa4344a448d6772744fa06b1632056ada0b` → commit;
   `test -f $F/.ufo/reports/round-56/mori.md && echo exists`.
9. **Census numbers (D9):** `grep -c rows $W/evidence/census-start.txt` → 0;
   `grep -n 'row counting command' $W/evidence/census-end.txt` → line 26;
   reproduce both counts yourself:
   `git -C $R show 5b295eee…:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`
   → 316; same at HEAD → 320 (worktree now 320; `618562c7` also 320),
   matching `census-end.txt` and showing the correction's numbers are true
   even though the entering-count command is uncaptured.

## Verdict
Every routed receipt path/wording item is **CONFIRMED at named bytes**: D1,
D2, D3 (spot-check routed defects 1–3) and D4–D7 (lesson receipt-craft
items). None is repairable in-round (counters and receipts frozen; routed
correctly). Two same-class additions: D8 (the spot-check lesson's own
fleet-only pointer fails from the lane — the carrier exhibits the class it
routes) and D9 (the correction receipt leaves two numbers command-less; the
narrative lines still carry the retyped 316 with only an appended repair).
No integrity loss found: every pin, stamp, and count re-derived true; the
defects are citation precision, consumability, and wording. Recommended
routing for round-57 closure wording: full wave-relative evidence paths with
repo qualification for cross-repo pointers; full 40-hex `rev=` in all
receipt lines (raise/abandon the 110-char cap in the successor); per-line
`@rev` on every pin-sheet line plus relative paths inside a pinned archive
so `sha256sum -c` works; "log lines=N" phrasing with field citation; c2/c1
early-return label parity in the next counter generation. No counter,
predicate, kill rule, or claim change proposed or made.

Report: .ufo/waves/round-57/w1/Mo57Reviewer22.md
