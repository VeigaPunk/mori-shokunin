# CriticC2Counter — round 31 wave 1: falsifying the C2 counter and controls

Seat: MoriR31.CriticC2Counter (critic, leaf). Lane revs read: freeze `2124cbcd`, receipts `8baccf4a` (lane HEAD), entering
tip `a12c68ae`. Scratch: `/fast/scratch/hyaku/mori-r31/CriticC2Counter/`. Every counter run used
`TMPDIR=<scratch>/tmp`, so the counter's `mkdtemp` sandbox stayed inside scratch (it was empty afterwards, `ls -A | wc -l`
→ `0`). No lane write other than this file. No tool installs or updates. No background processes; nothing left running.

## Verdict in one paragraph

The frozen counter checks what it says it checks (the scanned count, count consistency, exit 1, stray lines, and an exact
set per fixture), and the three committed controls reproduce byte for byte. But **five cheap tools that do not implement
the files-opened rule, or implement only part of it, print `C2=met`, exit 0**. Three of them are pure oracles keyed on
fixture content, fixture creation order, or the lane's own answer key. The other is an honest partial parser that gets
16/16 on the fixtures and 0/5 on held-out briefs, even when it ignores the allow file, the lane revision and the writer
regex. So `C2=met` is necessary but not sufficient for the claim title. Because the counter is frozen, this is a
tradeoff the judge has to weigh, not something to fix now. The before-value mismatch at `a12c68ae` is an error in how
the before state was described, not a change to the predicate. Naming the axis operability is defensible.

## Findings, ranked by severity

### F1 (high): cheap oracle tools meet C2

Counterexample: three tools built from the frozen fixtures, none of which parses a files-opened block. I scored each one
with the frozen counter at the freeze commit:

| tool (scratch file, sha256 prefix) | keyed on | counter output |
|---|---|---|
| `falsifier-a-content-hash.sh` (`03bec8c7`) | sha256 of each brief after replacing its own basename with `@REPORT@` | `exact=16/16`, `stray=0`, `C2=met`, exit 0 |
| `falsifier-c-creation-order.sh` (`001d78c8`) | `(st_mtime_ns, st_ino)` order of the working-tree briefs; reads no brief bytes | `C2=met` in 8 of 8 runs (`uniq -c` → `8 C2=met`) |
| `falsifier-b-answer-key.sh` (`9c3655f8`) | reads `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-31/c2-fixtures.json` only when `$0` matches `*/mori-r31-c2.*/tool.sh`; otherwise it execs the round-30 gate port | `C2=met`, exit 0. The fallback path was not run |

Command: `python3 .ufo/waves/round-31/count-c2.py 2124cbcddd676102b3d59f0765cb42e8f05090ee --tool-file <scratch>/<tool>`.

Why each one works, with evidence:
- **Content.** `gen.py` printed `built 16 distinct fixture hashes of 16`. Only F01, F11 and F12 contain the placeholder,
  so the other 13 briefs are the JSON lines verbatim. Undoing the substitution is trivial, because the tool receives the
  basename it was substituted with (`count-c2.py:86`).
- **Order.** The counter writes the briefs in fixture order (`count-c2.py:80-89`). Random names hide the fixture id
  (`:81-84`) but not the creation order, which is visible on xfs (`findmnt -T /tmp` → `xfs`; scratch is xfs too).
  Line counts alone do not identify fixtures: six of them have 3 lines (`Counter({3: 6, 4: 3, 6: 3, 7: 2, 8: 1, 5: 1})`).
- **Answer key and environment.** The tool runs with no isolation. It sees the full environment minus three GIT
  variables (`count-c2.py:21`; my `P_IGNORE_INTERFACE=1` run below reached the tool through it). It can read the lane by
  absolute path (`:20`). And it can tell it is being counted: `$0` sits under `mori-r31-c2.*/tool.sh` (`:72,93`), the
  working directory is named `repo` (`:74`), and the committer is `C2Counter` (`:99`). Falsifier B uses the `$0` check,
  so it can behave differently inside the counter than in the lane.
- **Weak control.** The committed shortcut 2 (`controls/shortcut2-canned-ids.sh:3-17`) is keyed on names the counter
  randomizes, so it was bound to fail (`evidence/c2-controls.txt:76-94`, every hit is stray). Under addendum §9, the
  pre-freeze control has to be "the cheapest control that skips the claimed work"
  (`/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md:212-216`). Falsifier A is cheaper than shortcut 1,
  and it meets.

Impacted axes: operability (the C2 axis). Calibration also suffers, because a receipt label would overstate what was
verified.

Defect or tradeoff: any counter built on frozen public fixtures, running unsandboxed author code, can be beaten by
memorization. The fix §9 prescribes ("fix it before data") changes the counter, which is no longer allowed once seats
have scored. So this is a tradeoff the judge must weigh: `C2=met` alone does not admit the claim.

Smallest safe correction (no counter change): an uncounted residual for wave-2 non-authors, published next to the
receipt.
1. Review the landed `tools/mori-blind-check.sh` blob for fixture-keyed logic. Reject if the source contains any of:
   `c2-fixtures`, `@REPORT@`, `mori-r31-c2`, `C2Counter`, `hashlib`/`sha256sum`/`md5`, `st_mtime`/`st_ino`/`stat -c`,
   `ls -t`/`ls -U`, or fixture literals such as `CaseOther`, `tools/mori-pressure.py`, `example.com`.
2. Record falsifiers A, B and C as extra control receipts, so the closure can see what the counter cannot exclude.

### F2 (high): an honest partial parser meets C2, so the fixtures leave the rule underdetermined

Counterexample: `falsifier-p-partial-rule.sh` (`b6725421`). It implements only the clauses the fixtures exercise. Its
header lists what it leaves out: `opened files` headings, `Opened files:` labels and lowercase forms; `* ` and `+ `
markers and indented entries; stripping of quotes, brackets and trailing `,;.`; checking any candidate after the first;
and the round-30 detectors, which it replaces with two one-line regexes. Results:
- Interface honoured: `exact=16/16 ... C2=met`, exit 0.
- With `P_IGNORE_INTERFACE=1`, it hard-codes three allow globs, reads the working tree instead of `<lane-rev>`, and
  hard-codes `^Case`. Still `exact=16/16`, `C2=met`, exit 0.
- On five held-out briefs written to the rule text (`rule-text.md:10-21`), it gets every one wrong:

```text
CaseH1  "## Opened files" / "- tools/x.sh"                           rule: (2, forbidden)  P: (1, missing)
CaseH2  "Files opened:" / "* LOG.md"                                 rule: (2, forbidden)  P: (1, missing)
CaseH3  "## Files opened" / "  - tools/x.sh"                         rule: (2, forbidden)  P: (1, missing)
CaseH4  "## Files opened" / "- .ufo/waves/round-31/rule-text.md tools/x.sh"   rule: (2, forbidden)  P: none
CaseH5  "## files opened" / "- \"/fast/scratch/hyaku/mori-r31/CaseH5/a.json\","  rule: none  P: (1, missing)
```

(The output was `scanned=5 blind_violations=4`, with H1, H2, H3 and H5 each at `:1:writer-missing-files-opened-list`,
exit 1. The allow file was the rule-text glob plus the `{report}/*` scratch glob.)

What the fixtures never exercise, measured over `c2-fixtures.json`:
- Entry markers present are only `- `, `1.`, `2)` and `|`. There are no `* ` or `+ ` entries and no indented lines
  (`indented []`).
- The only openers are `## Files opened` and `Files opened:`. There is no `opened files` or `Opened files:` form, no
  lowercase form, and no opener heading at a level other than H2.
- Allow lines 2, 3 and 6 (the absolute rule-text path, a bare `{report}`, the godspeed path) are never needed
  (`c2-fixtures.json:5-12`).
- F13 is meant to test punctuation stripping, but its only trailing-`.` entry (`:212`) is forbidden whether or not the
  `.` is stripped.
- Rule 6 has one positive case per detector (F15, F16).

Impacted axes: operability. The C2 title "reports every forbidden entry" (`contract.md:56`, `SCORECARD.md:1837`) also
uses a universal clause that §9 allows only when the counter enumerates the full set (`lane-addendum.md:206-207`). The
predicate does scope it to "the 16 frozen fixtures", but the title does not.

Smallest safe correction (no counter change): the closure states the C2 scope as "16 frozen fixtures", and a non-author
runs the held-out set above (plus `+ ` and H3-opener variants) against the landed tool as residual evidence beside the
C2 verdict.

### F3 (medium): the before-value at `a12c68ae` is a description error, not a predicate change

- Declared before-value: `count-c2.py a12c68ae` → `tool=absent`, `C2=unmet`, exit 1 (`SCORECARD.md:1837` at HEAD,
  `contract.md:22`).
- Committed receipt: `count-c2: fixtures absent at revision`, `C2=error`, `exit=2` (`evidence/c2-before-base.txt:1-5`).
  I re-ran it and got the same: `C2=error`, `exit=2`.
- Cause: the counter checks the fixtures (`count-c2.py:53-57`) before it looks for the tool (`:63-68`). The fixtures
  first exist at `2124cbcd`: `git cat-file -e a12c68ae:.ufo/waves/round-31/c2-fixtures.json` → `exists on disk, but
  not in 'a12c68ae'`.

My judgment is that this is an error in describing the before state, not a predicate change:
- P-C2 and the counter bytes are unchanged.
- Exit 2 is the contract's own declared code for this case ("2 bad revision or fixtures not the frozen sha256",
  `contract.md:64-65`; docstring "tampered fixtures", `count-c2.py:13`).
- The after-value ("same command at the landed tip", `SCORECARD.md:1837`) is unaffected, because the fixtures exist at
  any later tip.

What it costs:
- The declared "command that shows it unmoved" (`contract.md:22`, required by §9 at `lane-addendum.md:224-225`)
  actually shows `C2=error` at the entering tip, not an unmoved state.
- The error was knowable before any data. The declaration and the counter were committed together in `2124cbcd`
  (`git show --stat`: `SCORECARD.md | 16 ++`, `count-c2.py | 152 +++`). The receipt commit `8baccf4a` recorded the
  contradiction without reconciling it.
- The closest real before-value is `evidence/c2-controls.txt:1-6`: `2124cbcd` → `tool=absent`, `C2=unmet`, exit 1.
  That is a different revision from the declared one.
- C1 does not have this problem (`evidence/c1-before.txt`: `entry=absent`, `C1=unmet`, `exit=1`).

Smallest safe correction: an appended correction line in `SCORECARD.md` and the LOG. Do not edit the declaration row.
The line names the `c2-before-base.txt` result and the `2124cbcd` stand-in, and says P-C2 is untouched.

### F4 (medium-low): the predicate sentence is not identical in the docstring

- `contract.md:7-8` says P-C2 is "the same sentence here, in its counter's docstring and code".
- The docstring (`count-c2.py:5-9`) leaves out "no hit line outside the 16 briefs" (compare `contract.md:59-62`).
- The code does enforce it (`count-c2.py:145`, `and not stray`), and the label `C2=met` matches.
- So §9's three-way identity of plan, code and receipt label (`lane-addendum.md:219-220`) holds. Only the contract's
  extra claim about the docstring is false. No behaviour changes.

Correction: a disclosure line only.

### F5 (low): parts of the comparison are looser than the predicate sentence

Counterexample: `falsifier-e-duplicates.sh` (`ecfff01e`). It prints every hit twice, then `scanned=999` and
`blind_violations=not-a-number` after the hit lines. Result: `blind_violations=28 hit_lines=28 count_ok=yes ... stray=0
exact=16/16 C2=met`, exit 0.
- Hits are compared as sets (`count-c2.py:113,123,129`), so duplicates pass. But rule 4 says each bad entry is "one"
  hit (`rule-text.md:19-20`).
- Only the first `scanned=` and `blind_violations=` lines are read. Later ones are silently dropped, not counted as
  stray (`:110-112`).
- Output order, which the interface fixes at `contract.md:71-72`, is not checked.

What the counter does enforce, read in the code: `scanned` must be exactly the string `16` (`:137`); the violation
count must be a number equal to the number of hit lines (`:138`); the exit code must be exactly 1, so a timeout (124)
fails (`:136,139`); any line that is not shaped like a hit is stray (`:117-119`); and a hit must sit exactly in the
wave directory (`:122`), so `NotesBrief.md` and `sub/CaseNested.md` hits are stray.

Correction: residual note only.

### F6 (low): the allow-file reader that the do-nothing control adds is broader than the rule

The do-nothing port strips `./` before matching, which the rule never mentions
(`controls/do-nothing-r30-gate-port.sh:17`). No fixture depends on it, so its score of 10/16 is unaffected. Noted
because the control is more than "only the allowlist function replaced" (`contract.md:93-94`).

## Re-run of the committed controls (all three reproduce)

```text
do-nothing  sha256=4d5109e7...  exact=10/16  C2=unmet
shortcut1   sha256=89d1b947...  exact=3/16   C2=unmet
shortcut2   sha256=84d63760...  exact=4/16   C2=unmet
fixtures sha256 1442c14e963bf77df34774015dff7ee73a9738d49b3911d26b4e3b96f48e0b31 (= FIXTURES_SHA256, count-c2.py:18)
```

These match `evidence/c2-controls.txt:10,29-30,35,54-55,60,94-95`.

## Axis: operability or quality work under §9?

The operability name is defensible. This is a tradeoff, not a defect.
- **For.** §9 says to name the axis by the surface changed (`lane-addendum.md:221-225`). C2 lands a new runnable lane
  tool: `git ls-tree a12c68ae tools/` shows no blind gate. The round-30 gate is wave evidence under
  `.ufo/waves/round-30/`, not a lane tool. The new parser behaviour is real and the counter discriminates it: the held
  round-30 parser scores 10/16, and six fixtures (F01, F02, F03, F06, F09, F10) separate the two
  (`c2-controls.txt:12-21`).
- **Against (disclose in the closure).**
  - 10 of the 16 fixtures, plus all of rule 6, re-score behaviour the lane already holds. §9 calls that "quality work"
    (`lane-addendum.md:221-223`).
  - The contract confines C2 to the tool file (`contract.md:23-24`). No SKILL or PROVINCE line names
    `check-blind-wave` or `mori-blind-check` at `a12c68ae` (the `git grep` found nothing). So the operability gain is a
    tool that no lane flow invokes [INFERENCE].
  - Round 30 already claimed "Gate fixed (R5)" under operability 7 and missed (`.ufo/waves/round-30/contract.md:75`,
    `SCORECARD.md:1811,1821`). Round 31 re-claims that target under the same axis, but the "Not re-claimed" line
    (`contract.md:25`) mentions only the freeze. And `contract.md:100` calls routed repairs "not claims", while
    `contract.md:102` calls D1 "C2's substance".

## Bottom line for the judge (no counter change proposed)

1. Treat `C2=met` as "the landed tool reproduces 16 fixture outcomes". Admitting the claim title needs both F1 residual
   checks (the source review and the extra control receipts) and the F2 held-out residual.
2. F3 and F4 are corrections by appended text. Neither touches P-C2 or the after-value.
3. F5 and F6 are residual notes.

Files left in scratch for reuse: `gen.py`, `falsifier-{a,b,c,e,p}-*.sh`, and `heldout/` (a five-brief sandbox repo
plus `allow.txt`).
