# Round 28 wave 1 — CriticRoutingCoverage: does the plan cover the routed work?

Seat: `MoriR28.CriticRoutingCoverage` (critic, leaf, read-only). Measured 2026-10-22 between about 17:58Z and 18:05Z
against the lane at `079a47c61691f2b891d35458057b294ca5a99e77` (declaration) plus the untracked
`.ufo/waves/round-28/wave1-spec.json` (the wave-1 seat prompts). Nothing in the lane was edited apart from this file.

Inputs read: `.ufo/waves/round-28/contract.md` (all 75 lines), `corpus/lessons/round-27-verifier-spotcheck.md` (all),
`corpus/lessons/round-27.md:1-131`, `.ufo/waves/round-28/count-c1.sh`, `.ufo/waves/round-28/evidence/c{1,2}-before.txt`,
`.ufo/waves/round-27/w1/CriticC2Counter.md:150-204`, `corpus/QUALITY.md:345-383`, `CORPUS.md:110-118` (fleet root),
`SCORECARD.md` at `079a47c` (round-28 declaration).

## Verdict in one paragraph

The plan routes all six routed defects and all eight carried row defects somewhere: two are claims and four are
hygiene. Four gaps matter. (1) **False provenance in the W1 correction itself, and a QUALITY 83 that would misfire.**
In this jj lane a commit's author time is the moment its empty change was opened, not when its content was written.
So the round-28 correction's "existed no later than 15:45:38Z" is unproven, and a criterion keyed to author time
fails the round-28 declaration commit. (2) **The tip receipt cannot be "for the round-28 tip".** A batch cannot hold
a receipt of its own commit, so the closure will find the same defect again unless the contract names the parent.
(3) **The restores bring back old wording that live files still cite.** Restoring S096, S097 and S101 puts the old
text back while `SKILL.md`, `PROVINCE.md` and two knowledge entries still cite those ids. Nothing in the contract
requires them to cite S145–S147, and nothing requires the restores to be logged as old → new changes. (4) **C2 rests
on ten separate single seats.** No replacement rule exists, so one dead executor makes C2 a miss, which is the
round-27 M4 failure again, spread over ten rules. One r27 carried item, the older settings-value exposure, is
missing from the plan. No `operator-*.md` lesson exists.

## Coverage table

| # | Item (source) | Planned handling | Gap | Smallest fix (fits a 90-minute round) |
|---|---|---|---|---|
| RD1 | W1 future-dated (spotcheck:144-145) | hygiene: correction appended at r27 `contract.md:101-107` (`079a47c`); QUALITY 83 drafted by seat DraftQualityCriteria keyed to `%aI` | correction states "existed no later than 15:45:38Z" from author time; in jj that is the change-open time (E1). Draft 83 keyed to author time fails `079a47c` itself (E2) | append a second dated note: the bound is committer time 15:50:10Z; key QUALITY 83 to `%cI` (W1 still fails: 15:55Z > 15:50:10Z) |
| RD2 | tip receipts missing (spotcheck:146-147) | hygiene: TipReceiptsR27 (r27 tip C1 receipt, retention at `df886be1` and `6ebd518f`); contract:69-70 "as the last lane batch, for the round-28 tip" | self-reference: the last batch cannot contain a receipt of its own hash. Contract says "for the round-28 tip"; the draft 84 prompt says "measured at the parent of that batch". The two disagree, and the closure will read the contract | dated contract clarification (E3 text): receipts measured at the first parent of a final batch that adds only `evidence/tip-*.txt`; report cites both hashes and the `diff --stat` |
| RD3 | QUALITY 81 unmet: S096, S097, S101 (spotcheck:148-149) | claim C1 (`changed=0` via frozen `check-row-identity.py`) | restore re-instates first-published wording (S101 "docs and code disagree for values above 100"; S097 old "flip" text). Live citers: `SKILL.md:619`, `PROVINCE.md:257-258`, `system-pressure-r24.md:1,30,41,224`, `harness-job-capacity-r25.md` (E4). QUALITY 77 needs every corrected statement swept to the new row. The restores are in-place cell changes CORPUS Rules 2 says to log old → new. The contract requires neither. CriticC1Design (b) investigates but no contract line binds it | routed-hygiene line: each citing statement that relies on the corrected wording also cites S145/S146/S147, and the round-28 lesson logs the three restores old → new; closure hand check `git grep -nE 'S09[67]\|S101' <tip> -- SKILL.md PROVINCE.md corpus/knowledge` |
| RD4 | carried row defects S127 F1–F5, S128 F1, S129 M2, S131 tree URL and F2–F4, ReopenS140 low (spotcheck:150-151) | claim C1: S148–S152 by SupersedeS127…S140 | the counter (`count-c1.sh:36-43`) checks only id > S144, the `supersedes S0NN — ` prefix and status `mined`/`verified`. Contract:20-22 also promises a round-28 Gate record (URL, access time, quote), and nothing counts it. Nothing checks that each named finding is fixed in the new row. The counter also accepts `verified`, but the contract says `mined` | lesson Gate gets one line per new row naming the findings fixed and the new cell. Closure hand check: `git show <tip>:corpus/lessons/round-28.md \| grep -cE '^\| S1(4[5-9]\|5[0-2]) \|'` must be 8 |
| RD5 | C2 / r26 D7 (spotcheck:152-153) | claim C2; BuildCountC2, CriticC2Design, ReviewA2SpecVsTool, ten blind executors CaseA2r01–r10 | (a) each rule rests on one executor seat. Executor was the role that died at spawn in r27 (`round-27.md:55-57`). The contract has no replacement rule and says "never withdrawn" (contract:5-6), so one dead seat is a miss (E5). (b) hardening list "F1–F8 and F11" omits F10 (merge-landed file rejected), F12 (valid rev exits 2) and minor `"exit": true` == 1 (`CriticC2Counter.md:160-200`). (c) before-value is from the round-27 counter (`c2-before.txt:1`), the after-value from the round-28 counter: not the same command. (d) closure hand checks H1–H5 (`CriticC2Counter.md:204-252`) not referenced | (a) dated clause before the freeze: a case writer that returns no case is replaced once by a fresh seat with the identical blind prompt; LOG names both; "one seat per rule" counts the seat whose cases are frozen. (b) land the case file in a non-merge commit; counter rejects a bool `exit`; F12 gets distinct messages (already in the BuildCountC2 prompt). (c) commit `evidence/c2-before-r28.txt` = round-28 counter at `6ebd518f`, in the counter's batch. (d) one contract line pointing at H1–H5 |
| RD6 | r25 R1, R5 code debt (spotcheck:154) | hygiene: FixR1Runway, FixR5RoutedSelftest in sandboxes; land "only when a non-author check passes" (contract:70) | no wave-1 seat is that non-author check, and wave 2 is not specced yet. R1 adds `cases-r1.json`; the no-harm line "five round-26 selftests keep their tallies" does not say how a new fixture file is tallied | wave 2: one reviewer seat per fix, re-running each fixture file separately (old files identical tallies, new file reported on its own); otherwise carry with the reason |
| D-a | ruling: a withdrawal is not a path out of admission (spotcheck:71-79) | contract:5-6 "Nothing declared here will be withdrawn" | none | — |
| D-b | reported 7/11 vs committed `c1-after.txt` 6/10 at `0becc421` (spotcheck:50-51) | TipReceiptsR27 run (a) at `df886be1` | none if committed (QUALITY 76 shape) | — |
| D-c | Gate cites `base.c:596-597`, quote is on 597; 596 is the guard (spotcheck:115; ReopenS127.md:60,81) | none | S148 may copy the 596-597 anchor | S148's Gate quote located at `:597` |
| D-d | no committed retention scan at `df886be1` (spotcheck:87-89) | TipReceiptsR27 run (b) | see RD2 for the round-28 tip | RD2 fix |
| D-e | SHONEN `[ ]` decision tables / executable without oral context; no non-author execution (spotcheck:136-140) | none (not in contract or wave-1 spec) | not named | lesson names it carried, operator-owned promotion; no seat this round |
| Op-1 | seven fleet-root files (spotcheck:156-157) | MisrootProvenance scout (report only) | none (operator owns removal) | lesson records the provenance findings |
| Op-2 | dead-at-spawn 7/34 (spotcheck:157-158) | none explicit | becomes RD5 (a) | RD5 (a) fix |
| W2-1 | S127 F1–F5 (`round-27.md:125-127`) | C1, S148 | see RD4 | — |
| W2-2 | S128 F1 | C1, S149 | see RD4 | — |
| W2-3 | S129 M2 | C1, S150 | see RD4 | — |
| W2-4 | S131 tree URL without `?recursive=1`, F2–F4 | C1, S151 | see RD4 | — |
| W2-5 | S096, S097, S101 restores | C1 | see RD3 | — |
| W2-6 | ReopenS140 low finding | C1, S152 | see RD4 | — |
| W2-7 | pre-existing harness settings-value exposure in other older lane files, history disposition operator-owned (`round-27.md:129-131`) | **missing**: not in contract.md or any wave-1 prompt | unnamed carried item; the closure cannot tell carried from forgotten | lesson names it carried with the L0 pointer; no edits this round (operator owns history) |
| OP | `corpus/lessons/operator-*.md` | — | glob returned 0 files; nothing to reflect in QUALITY | — |

## Evidence

**E1 — jj author time is the change-open time.** `git log --format='%h a=%aI c=%cI' fc09f96c..df886be1`:

```text
126e192 a=2026-10-22T12:50:10-03:00 c=2026-10-22T12:58:23-03:00
dd4dbb2 a=2026-10-22T12:45:38-03:00 c=2026-10-22T12:50:10-03:00
5fa0a00 a=2026-10-22T12:42:09-03:00 c=2026-10-22T12:45:38-03:00
```

Each author time equals the previous commit's committer time: the empty working-copy change opened by `jj` at the
last commit (`ls -d .jj` → `.jj`). So W1's content is bounded by committer 15:50:10Z, not author 15:45:38Z. The
correction at r27 `contract.md:103-105` says "so the amendment existed no later than 15:45:38Z". That is false
provenance. [INFERENCE: the general jj timestamp rule; the three-commit chain above is observed.]

**E2 — the draft criterion would fail round 28's own declaration.** `git log -1 --format='author=%aI committer=%cI'
079a47c` → `author=2026-10-22T14:50:48-03:00 committer=2026-10-22T14:56:06-03:00`. Both receipts in that commit
open `# C1 before, measured 2026-10-22T17:55:46Z` / `# C2 before, measured 2026-10-22T17:55:46Z`
(`evidence/c1-before.txt:1`, `c2-before.txt:1`). 17:55:46Z is after the author time (17:50:48Z) and before the
committer time (17:56:06Z). The DraftQualityCriteria prompt says 83 is "never later than the author time of the
commit that ships it". The L1 was messaged once (`agent://MoriR28`, delivered).

**E3 — ready-to-paste contract clarification for RD2 (dated, append-only):**

```markdown
## Clarification C-T (appended 2026-10-22, round 28, before the final batch; nothing above is rewritten)

"Tip receipts for the round-28 tip" means: the final lane batch adds only files under
`.ufo/waves/round-28/evidence/tip-*.txt`; every receipt in it is measured at that batch's first parent P (40-hex in
each receipt header); the report cites P and the landed tip and pastes `git diff --stat P <tip>` showing only those
files. No counted input (`corpus/SOURCES.md`, `tools/`, the fixture files, the retention policy) differs between P
and the tip, so each counter reads the same at both.
```

**E4 — live citers of the restored rows** (`git grep -l '\bS0NN\b' 079a47c -- . ':!corpus/SOURCES.md' ':!.ufo'`):
S096 → `SKILL.md`, `PROVINCE.md`, `corpus/knowledge/system-pressure-r24.md` (+ LOG, SCORECARD, lessons); S097 →
`PROVINCE.md`, `system-pressure-r24.md`; S101 → `corpus/knowledge/harness-job-capacity-r25.md`. The first-published vs
current `teaches` cells differ: S101 at `90ed9b7` "…so docs and code disagree for values above 100" and at `079a47c`
"…the 100 maximum is documented only in docs/tools/eval.md:258 (S103) and enforced in sdk.ts:228…". S097 at
`df4db54` "flip: the same scope is documented by the kernel PSI documentation (S001…" and at `079a47c` "flip: the
man-pages project publishes a proc_pressure page; until then…". QUALITY 77 (`QUALITY.md:349-355`) and CORPUS.md
Rules 2 (`CORPUS.md:115-118`, log old → new) apply.

**E5 — single seat per rule.** `wave1-spec.json` items CaseA2r01…CaseA2r10 are each `executor`, one per rule. Each
rule needs ≥2 cases (contract:50-51), all from that one seat. At about 18:00Z `/fast/scratch/hyaku/mori-r28/` held a
directory for nine of the ten writers, and none for CaseA2r08. [INFERENCE: a writer may not need a scratch dir;
this is a watch item, not a death.]

**E6 — W2-7 scale (counts only, no values).** `git grep -nE 'maxJobs`?:? *`?[0-9]+' 079a47c` with lines whose number is
100 or 1 dropped: 198 lines in 44 tracked files, of which 147 are under `.ufo/waves/round-25`, 34 in
`tools/fixtures/mori-job-runway/` (invented fixture values) and 8 under `.ufo/waves/round-26`. [INFERENCE: an upper
bound on the pattern, not a count of host values; no line was classified, so no value was read into this report.]

## Strongest counterexamples, ranked

1. **RD1/E1–E2 (false provenance).** Impacted axes: calibration (a correction that asserts a bound the evidence does
   not give) and the honesty of the routed-defect fix. As written, QUALITY 83 fails closed on every jj commit whose
   receipts were written after the change was opened, which is every commit in this lane. This is a fixable defect.
2. **RD2/E3 (tip receipt self-reference).** The routed defect comes back by construction unless "tip" is defined.
   Fixable with one appended paragraph.
3. **RD3/E4 (restore without re-pointing).** Impacted axis: freshness, the axis C1 claims. After C1, a reader who
   follows S101 from the knowledge entry lands on wording the lane already knows is wrong. C1 can print `C1=met`
   while QUALITY 77 is violated. Fixable as hygiene. It is not a reason to reject C1, but the closure should check it.
4. **RD5 (a) (M4 recurrence).** Impacted axis: operability. This is a tradeoff the plan accepted rather than a
   defect, but it lacks a replacement rule. Adding one before the freeze does not narrow the claim.
5. **RD5 (c) (before/after counter mismatch).** A judge may refuse the delta because the before-value was measured
   by a different command. Fixable with one committed receipt.

## Watch item (QUALITY 80)

Untracked now (`git status --porcelain`): `.ufo/waves/round-28/wave1-dispatch.json`, `wave1-run.err`,
`wave1-run.json`, `wave1-spec.json`, `w1/`. QUALITY 82 lint over those five paths matched 0 lines
(`grep -cE 'user-[0-9]{3,}\.slice|user@[0-9]{3,}\.service|\buid[ =:]+[0-9]{3,}'`). Each JSON holds one "session"
mention, in the shared context's bound text. These files must be committed or disposed of before the final commit.

## Out of scope, noted

`corpus/lessons/2026-10-15-run-order-spoofing-shuffle-nonce-limits.md` and
`…-run-secret-timing-and-content-freshness-limits.md` have no citation in `QUALITY.md` (`grep -c` = 0 each). Both
were written by seats ("source seat: lessons-distiller"), not by the operator, so they are not operator teaching.

## Tooling and bounds

No tool installed or updated. No lane commands other than read-only git, `ls`, `grep`, and `python3` reading JSON.
No jj command. One message sent, to `agent://MoriR28` only. No host identifiers, settings values or session data are
copied here.
