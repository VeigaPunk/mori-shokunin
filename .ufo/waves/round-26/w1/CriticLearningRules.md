# CriticLearningRules — mori round 26, wave 1 (critic, leaf)

Scope: attack the round-26 design's conformance to the session rules before work lands. Inputs read:
`/home/vgpnk/Projects/shokunin/.scratch/goal-20261022-hyaku-12h.md:143-178` (Quality bar, Drift sentinels),
`/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-26.md:9-40` (§2), `:42-78` (§2b), `:342-350` (§6.9),
`.ufo/waves/round-26/contract.md` (landed `28b04940`), `AXES.md:10-73`, `SCORECARD.md:1-19,1417-1602`,
`corpus/lessons/round-25-verifier-spotcheck.md:172-206`, `corpus/QUALITY.md:349-355`, `.ufo/waves/round-26/wave1-spec.json`.
Lane tip when read: `jj-lane.sh state` → `branch=master local=5e5e86f11e564878e69712ae6eb1c2bd59258e24 ahead=0 behind=0`.
Tool installs: none. Network: three `curl` fetches of public earlyoom v1.9.0 files (below).

## Verdict table

| # | Rule (source) | Verdict | One-line reason |
|---|---|---|---|
| 1 | Lowest-axis rule (§2.2; AXES.md:33-34) | pass, risk | freshness 5 is tied lowest with depth 5 and calibration 5; no after-score declared |
| 2 | Learning claim (goal:145-149) | pass, risk | C1 is "a stronger entry superseding a weaker one"; its counter measures phrase absence, not knowledge; C2 lacks the capability-row after-state |
| 3 | Sourced claim (§2b.4) | risk | stated in prose but not in the counting command; "opened in round 26" is not derivable from the `opened` date |
| 4 | Drift rule (goal:172) | pass, risk | FR10 differs from r23 FR2, r24 FR12, r25 job runway; hygiene R2/R4 are calibration repairs and must stay uncounted |
| 5a | Claim sizing, C1: one command over committed bytes (§6.9; goal:151-152) | **fail** | the command reads the phrase list from the working tree relative to the current directory; from the fleet root it prints the after-value at the entering tip |
| 5b | Claim sizing, C2 | risk | selftest reads working-tree bytes; "case file unchanged since freeze" and "written by another seat" are not re-derivable by the command |
| 5c | Universal words (§6.9; goal:153-154) | pass, risk | claim statements are enumerated; "The cases cover each verdict rule, each grammar line" is an unenumerated universal |
| 6 | Causal separability (§2.3; AXES.md:30-31) | pass, risk | counters touch disjoint files; C1 host evidence is `capture.sh`, not the C2 tool |
| 7 | ≥25% attack seats (goal:160-161) | pass, risk | wave 1 has 11 of 35 attack-role seats (31.4%); only 6 to 8 of them attack a declared claim |
| 8 | Every seat item names its claim and a surface (goal:160) | risk | 9 of 35 items name neither C1 nor C2 |
| 9 | QUALITY 77 sweep (contract:44 cites it) | risk (likely fail at closure) | two more stale earlyoom statements in the same r12 entry are outside the frozen list |
| 10 | Prefer 2 claims; no exploratory/waiver (§6.9; AXES.md:66-73) | pass | 2 claims, no waiver, no exploratory claim |
| 11 | Never narrow after landing (§6.9) | pass (watch) | the fixes below harden the counter and keep the four phrases and both values; land them as a dated amendment before any after-measurement |

## Evidence and counterexamples

### 1. Lowest-axis rule — pass, risk
- `SCORECARD.md:12-14` (at master): depth 5, freshness 5, calibration 5; coverage 6, operability 7, adjacency 6
  (`:10-11,15`). Freshness is tied lowest, so C1 works the lowest axis. `AXES.md:14` defines freshness as "skill claims
  re-verified against live surfaces; stale items flagged or fixed"; C1 fits that definition.
- The stagnation waiver does not apply and is not used: the saturation line is 8 on owned axes (`SCORECARD.md:639`);
  coverage 6 and operability 7 are below it.
- Risk: contract `## C1` says "score 5" and declares no after-score, while §2.5 requires a score delta in
  SCORECARD. The freshness Axes row cites "round-10 drift pin still red" (`SCORECARD.md:13`), which C1 does not touch.
  If the L1 later writes freshness 5 → 6 from C1 alone, the closure can call it a self-assessment overreach
  (a calibration harm).
- Fix: state the target now in SCORECARD's round-26 declaration: "freshness 5 → 5 (held; C1 is a measured
  freshness move, the drift pin stays red)", matching rounds 24 and 25 (`SCORECARD.md:1516,1554` "5 → 5").

### 2. Learning claim — pass, risk
- C1 qualifies as "a stronger entry superseding a weaker one" (goal:147). C2 qualifies only as "a capability shown
  running and entered in SCORECARD's capability table" (goal:147-148; `AXES.md:62-64`: "Rows enter only through a
  round that demonstrates the capability running"; §2.6 "its row enters the SCORECARD capabilities table in the same round").
- Counterexample (C1): an r26 entry consisting of one `source:` line plus a heading, with the four phrases deleted
  from r12 and README, prints `stale_present=0` and `r26_entry=present`. The counter cannot tell knowledge from a stub.
- Counterexample (C2): the C2 after-state (contract:55-56; `SCORECARD.md:1598`) names only the selftest. A round that
  lands the tool and its PASS but no capabilities row and no live run meets the declared after-state yet fails the
  learning-claim test for C2. Rounds 24 and 25 added both (`SCORECARD.md:1530-1535,1564-1569`).
- Fix: see the pasted C1 command (it adds the S-id and supersession checks) and add to C2's after-state:

```text
C2 after (added, same round): `git show <tip>:SCORECARD.md | grep -cF 'userspace OOM killer read'` ≥ 1 in a
`### capabilities: first demonstrated round 26` table, and a committed live-run receipt
`.ufo/waves/round-26/evidence/oom-killers-live-run.txt` holding the command, verdict and exit code (counts and
states only; no MESSAGE text).
```

### 3. Sourced claim — risk
- §2b.4: "one of the round's claims rests on a `SOURCES.md` row opened this round". Contract C1 puts it in the
  statement ("whose `source:` line cites at least one `corpus/SOURCES.md` row opened in round 26"), but the C1
  counting command (contract:36-38) checks only phrases and file presence.
- "Opened in round 26" cannot be read from the `opened` column: at `248408f5` the highest id is S113 and 24 rows
  already carry `opened` 2026-10-22 (rounds 24 and 25 ran that day), from
  `git show 248408f5:corpus/SOURCES.md | grep -oE '^\| S[0-9]+' | sort -V | tail -1` → `| S113` and the `opened`
  column count → `24`. An r26 entry citing S112 would look compliant by date.
- Fix: define "opened in round 26" as "id greater than S113 (absent at `248408f5`)" and count it in the command
  (pasted below).

### 4. Drift rule — pass, risk
- Trip recorded: `round-25-verifier-spotcheck.md:204-206` ("rounds 23–25 each counted a routed repair on calibration,
  so round 26 must work a different frontier area"). Prior frontier ground: r23 C2 FR2 quota (`SCORECARD.md:1427`),
  r24 C2 FR12 pressure (`:1506`), r25 C2 harness job runway (`:1546`). Round 26 works FR10 (`PROVINCE.md:53`) on
  freshness and coverage; no r23–r25 claim touched FR10. Pass.
- Risk: wave 1 carries R2 and R4 (SCORECARD calibration corrections) as hygiene (`wave1-spec.json` item
  DraftHygieneScorecard). If the report's calibration verdict or the SCORECARD round-26 rows credit them as a
  calibration move, that is a fourth round running of the same routed defect class.
- Fix: keep calibration "5 held, hygiene only" in the round-26 SCORECARD rows and Trend verdicts; put R1–R8 under
  a "Routed hygiene (not counted)" heading.

### 5a. Claim sizing, C1 counting command — fail
The command reads `.ufo/waves/round-26/c1-phrases.txt` from the working tree, relative to the current directory,
not from committed bytes. Seat and closure tools start at the fleet root (prompt §6.2 "Seat paths are absolute").
Three counterexamples, each run with `bash -c '<contract command>'`:

| Run | Output | Meaning |
|---|---|---|
| cwd `/home/vgpnk/Projects/shokunin`, `R=248408f5` | `bash: line 1: .ufo/waves/round-26/c1-phrases.txt: No such file or directory` then `stale_present=0`, `r26_entry=absent`, exit 0 | the declared after-value printed at the entering tip |
| cwd lane root, `R=deadbeef` | `stale_present=0` | a bad revision reads as fixed (`git grep` exits 128, counted as absent) |
| cwd lane root, `R=248408f5` | `stale_present=4` | the declared before-value, reproduced |

Also, `git grep` on a missing file exits 1 (`missingfile_exit=1`), so deleting r12 reads as fixed; the contract
forbids deletion (contract:43-44) but the command cannot see it. And `git grep -F` is line-based, while QUALITY 77
(`corpus/QUALITY.md:353-354`) requires the sweep "over whitespace-folded text with emphasis removed".

Smallest safe correction (same four phrases, same before and after values; reads the frozen list from commit `28b04940`;
refuses a bad revision, a short list or a deleted file; folds whitespace and strips `*` per QUALITY 77; adds the
sourced-claim and supersession checks):

```sh
L=/home/vgpnk/Projects/shokunin/mori-shokunin; R=<rev>; git -C "$L" rev-parse -q --verify "$R^{commit}" >/dev/null || { echo bad_rev; exit 2; }
n=0; k=0; while IFS='|' read -r f p; do k=$((k+1)); b=$(git -C "$L" show "$R:$f" 2>/dev/null) || { echo "missing=$f"; exit 2; }
  printf '%s' "$b" | tr -s ' \n\t' '   ' | tr -d '*' | grep -q -F -- "$p" && n=$((n+1)); done < <(git -C "$L" show 28b04940:.ufo/waves/round-26/c1-phrases.txt)
[ "$k" -eq 4 ] || { echo "phrases_read=$k"; exit 2; }; echo "stale_present=$n"
e=$(git -C "$L" show "$R:corpus/knowledge/userspace-oom-killers-r26.md" 2>/dev/null) && echo r26_entry=present || echo r26_entry=absent
printf '%s\n' "$e" | grep -m1 '^source:' | grep -oE 'S[0-9]{3}' | awk '{sub("S","");if($1+0>113)c++} END{print "r26_new_source_ids=" c+0}'
git -C "$L" show "$R:corpus/knowledge/userspace-oom-killers-r12.md" | grep -c -F 'userspace-oom-killers-r26.md' | sed 's/^/r12_names_r26=/'
```

Declared before at `248408f5`: `stale_present=4`, `r26_entry=absent`, `r26_new_source_ids=0`, `r12_names_r26=0`.
Declared after: `0`, `present`, `≥1`, `≥1`. Executed from the fleet root (script copy
`/fast/scratch/hyaku/mori-r26/CriticLearningRules/c1-fixed.sh <rev>`): `R=248408f5` and `R=master` (`5e5e86f1`) both
print `stale_present=4`, `r26_entry=absent`, `r26_new_source_ids=0`, `r12_names_r26=0`, exit 0; `R=deadbeef` prints
`bad_rev`, exit 2. The deleted-file guard (`missing=<file>`, exit 2) was not exercised (it needs a commit).
Land it as a dated contract amendment (reason: this counterexample) before any after-measurement.

### 5b. Claim sizing, C2 — risk
- `python3 -I -B tools/mori-oom-killers.py --selftest` uses the default cases path "resolved from the script
  location" (contract:61-62), i.e. working-tree bytes. A dirty working tree changes the result.
- N is "the case count at its freeze commit" (contract:53-54), but nothing checks that `cases.json` at the tip equals
  the freeze blob; a case edit after freeze is a narrowed target that still prints `PASS N'/N'`.
- "Written by a seat other than the tool seat": every lane commit is authored `mori-shokunin` by the helper
  (`git show 28b0494` author line), so authorship is not in the bytes. Round 24's closure already ruled that order
  is shown, not independence (`SCORECARD.md:1520-1521`).
- Fix (one command over committed bytes):

```sh
L=/home/vgpnk/Projects/shokunin/mori-shokunin; R=<tip>; C=tools/fixtures/mori-oom-killers/cases.json; T=tools/mori-oom-killers.py
F=$(git -C "$L" log --format=%H --diff-filter=A "$R" -- "$C" | tail -1); B=$(git -C "$L" log --format=%H --diff-filter=A "$R" -- "$T" | tail -1)
git -C "$L" merge-base --is-ancestor "$F" "$B" && [ "$F" != "$B" ] && echo freeze_order=ok || echo freeze_order=bad
git -C "$L" diff --quiet "$F" "$R" -- "$C" && echo cases_unchanged=yes || echo cases_unchanged=no
echo "N=$(git -C "$L" show "$F:$C" | jq '.cases|length')"; D=$(mktemp -d); git -C "$L" archive "$R" | tar -x -C "$D"; python3 -I -B "$D/$T" --selftest; echo "exit=$?"
```
  Record seat independence as a process fact with pointers (the committed `w1/WriteOomKillersCases.md` and
  `w1/BuildOomKillersTool.md` reports), not as part of the counted value.

### 5c. Universal words — pass, risk
- Claim statements: C1 "none of the four phrases" (contract:22) is enumerated by the list; C2 "N/N" is enumerated.
- Risk: contract:115-118 "The cases cover each verdict rule, each grammar line, the scope boundary …" is an
  unenumerated coverage claim. Interface lines with "never" (contract:63,103,106,107) are design requirements; if
  the report presents them as verified properties, they become uncounted universals.
- Fix: give each case a `covers` array with ids from a fixed list (`V1`–`V4` verdict rules, `G1`–`G9` grammar lines,
  `B-1us`, `B-eq` scope edges, …) and report `jq '[.cases[].covers[]]|unique|length'` against the list length. Say in
  the report that the "never" lines are tested only through the named cases.

### 6. Causal separability — pass, risk
- C1's counter reads only r12, `corpus/README.md` and the r26 entry; C2's reads only the tool and the case file.
  C1's host evidence is the separate `capture.sh` (wave-1 item HostCapture: "a read-only bash script"), not the C2
  tool. Each verifies with the other absent.
- Risk: if the r26 entry or `DraftSkillFr10` text cites the C2 tool's live verdict as host-state evidence, C1's
  entry content depends on C2. Fix: cite only `capture.sh` output in the r26 entry's host-state section; the tool
  may appear under "What it changes for mori" as a pointer, not as evidence.

### 7. ≥25% attack seats — pass, risk
- `wave1-spec.json` role count: scribe 16, reviewer 6, executor 3, scout 3, critic 3, connector 2,
  mutation-tester 2 = 35; attack roles (reviewer, critic, mutation-tester, labrat) 11/35 = 31.4%.
- Risk: items that attack a declared claim: 6/35 = 17.1% (prompt names C1 or C2), 8/35 = 22.9% counting
  ReviewContractGrammar and ReviewScopeClock (they attack C2 sections). The other attack seats are no-harm,
  hygiene, privacy and conformance (ReviewRetentionBase, ReviewHygieneDebt, ReviewPrivacyDesign, this seat).
  Scouts do not count as attack under goal:161, although §6.2 lists them for wave 2.
- Fix: make wave 2 carry at least 25% of the round total as reviewer, critic, mutation-tester or labrat seats
  that each name C1 or C2; report the role-based and the claim-attacking percentages separately.

### 8. Every seat item names its claim and a surface — risk
- Items naming neither C1 nor C2: DraftHygieneScorecard, DraftHygieneKnowledge, ScoutPriorAdmissions,
  ConnSiblingOverlap, ReviewContractGrammar, ReviewPrivacyDesign, ReviewScopeClock, ReviewRetentionBase,
  ReviewHygieneDebt (python scan of `wave1-spec.json` prompts for `\bC[12]\b`).
- They serve §2b, §6.5 routed defects or the no-harm check, which §6.2 allows ("plus the frontier step and
  verification"). Fix: in wave 2 and the report, tag each such item with what it serves (`C2 grammar`,
  `no-harm R8`, `routed R2/R4`, `frontier step`), so the closure need not infer it.

### 9. QUALITY 77 sweep — risk, likely fail at closure
- Two more stale earlyoom statements sit in the same r12 entry, outside the frozen list:
  `git grep -n -F "earlyoom's service unit is not found" 248408f5 -- corpus/knowledge/userspace-oom-killers-r12.md` → line 18;
  `` git grep -n -F '`systemctl is-enabled earlyoom.service` → `not-found`' 248408f5 -- … `` → line 14.
  The host now reads `enabled` (`systemctl is-enabled earlyoom.service` → `enabled`, 2026-10-22).
- QUALITY 77 (`corpus/QUALITY.md:349-352`): "every place that states it … carries the corrected wording …
  a contradicted line left standing is a defect". C1's "Not claimed … other entries" (contract:46) does not cover
  these, because they are in the same entry.
- Fix, without changing the frozen counted list: name both as correction rows in `corpus/lessons/round-26.md` with
  their own fixed-string check (expected 2 → 0, reported as hygiene, not counted). DraftR12Corrections already
  targets lines 14 and 18, so this is a reporting fix.

## Adjacent finding (for ReviewContractGrammar, not a rules verdict)

earlyoom formats percentages with `PRIPCT "%5.2lf%%"` (`msg.h:10` at v1.9.0), so the host's kill line reads
`SIGKILL when mem avail <=  5.00% and swap free <=  5.00%` with two spaces before `5.00`
(`printf "%5.2f%%" 5` → ` 5.00%`). The grammar at contract:82-83 shows one space; the parser and the host-shaped
case need to accept the padding.

Sources opened (2026-10-22, curl, public URLs):

| URL | sha256 | Quote (line) |
|---|---|---|
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c | `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4` | `fprintf(stderr, "earlyoom " VERSION "\n");` (161) |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/kill.c | `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3` | `warn("escalating to SIGKILL after %.3f seconds\n", secs);` (318) |
| https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.h | `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c` | `#define PRIPCT "%5.2lf%%"` (10) |

The main.c and kill.c hashes equal the L1's copies in `/fast/scratch/hyaku/mori-r26/`. The contract's cited lines
match those bytes: main.c:161, :295, :414, :416, :519, :523; kill.c:318, :627, :654.

## Seat conduct
- Read-only in the lane: git log/show/grep/status, `jj-lane.sh state`; `systemctl is-active/is-enabled/show` and
  `systemctl --version`, `pacman -Q earlyoom` (query only). No unit, journal, settings or lane-index change.
- Scratch: `/fast/scratch/hyaku/mori-r26/CriticLearningRules/` (main.c, kill.c, msg.h, c1-fixed.sh). One empty probe file was
  briefly created at `/fast/scratch/hyaku/mori-r26/CriticLearningRules-c1cmd.sh` (outside my seat folder) by a
  mistyped redirect and deleted in the same command.
- Checks not run: the corrected C2 command (no tool or cases exist yet), the C1 deleted-file guard, and the
  `covers` coverage count. They are not passes.
