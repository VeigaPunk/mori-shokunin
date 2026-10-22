# MutRoutedHygiene — mutation probe of C1's D4 hygiene row and exit-code rule

Seat: `MoriR25.MutRoutedHygiene` (mutation-tester, leaf; no subagents, no background jobs).
Target: `tools/mori-routed-r24.py` (claim C1), private scratch copy only.
Date: 2026-10-22. Lane tip at the time: `07a31ae8e22514bbc603afa13f2de7c8b2424cca`.
Tooling: `python3 3.14.8`, `git 2.56.0` (both already present; **no install or upgrade was performed** —
nothing was missing).

## Verdicts

| # | Finding | Verdict | Severity |
|---|---|---|---|
| V0 | C1's declared after-value as measured by the pristine tool at the landed tip | **held** (not falsified) | — |
| F1 | All three mutants survive the committed before/after evidence pair; only synthetic red fixtures kill them | **coverage gap** (not a claim break) | medium |
| F2 | Reverting the D4 fix commit `e43d883` (the ignore-rule narrowing) leaves the tool green | **coverage gap** (confirms `ReviewPycacheRule` F3) | medium |
| F3 | Exit code and payload `status` duplicate the same condition and can diverge | **weakened hygiene reporting** | low |

No finding falsifies C1's declared after-value: with pristine bytes the tool prints `"mismatches": 0`,
`"held": 4` of `"items": 4`, hygiene held, exit 0 at the landed tip. The findings are about what the
committed evidence does *not* exercise.

## Method

* Private clone (never the lane): `git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin
  /fast/scratch/hyaku/mori-r25/w2-MutRoutedHygiene` (300 MB, removed at the end). The lane checkout was
  only read; `git status` in the lane is unchanged except this report file and a sibling seat's file.
* Bounded behavioural detector: run the tool (current bytes) as
  `python3 -I -B tools/mori-routed-r24.py --repo <clone> --rev <fixture sha>` and read
  **exit code + payload `status` + `mismatches` + `hygiene.held` + `hygiene.reasons`**.
  The tool reads git objects only; with no `--rerun` it executes no code from the measured revision, so
  the mutated copy of the tool never influences what it measures — only how it judges.
* Baseline first: pristine bytes discriminate (green fixtures exit 0, red fixtures exit 1). A baseline
  failure would have made every mutant result inconclusive; there was none.
* Every mutant was applied one at a time, then the file was restored and re-run; the restored run
  reproduced the pristine baseline **byte for byte** on all eight fixtures (restoration evidence below).

### Fixtures (sandbox commits in the private clone, all based on the lane tip)

| id | sha | what it is | pristine verdict |
|---|---|---|---|
| G0 | `07a31ae8e22514bbc603afa13f2de7c8b2424cca` | green: the lane tip itself | exit 0, status `held`, mismatches 0, hygiene held |
| G1 | `67d6576c93de05e1533eec0812bd76d0937a626f` | green: tip + one benign commit | exit 0, status `held`, hygiene held |
| R1 | `30ed247d1b93e9b38370f4bf87249176985402f5` | red: the D4 ignore rule dropped (revert of the fix) | exit 1, `no_pycache_ignore_rule` |
| R2 | `4e8df0727c55e89597038b063651b9aaca55929b` | red: `!tools/__pycache__/` negation line added | exit 1, `gitignore_negation_reinstates_bytecode: .gitignore` |
| R3 | `97ac35329d43b2463e45cf7af07221878c83766e` | red: tracked `tools/__pycache__/probe.pyc` | exit 1, `tracked_bytecode_under_tools` |
| R4 | `b62472504007b8c5a4757169d61150328e86262f` | red: all three hygiene defects at once | exit 1, all three reasons |
| R5 | `0e84821ebff4df5ab21b67459c0871b75ac57c75` | `git revert e43d883` (the D4 rule narrowing) | **exit 0, status `held`, hygiene held → GREEN** |
| BASE | `28b79d3d1b76824f0c825aabe6cb6c5dc49961bf` | red: the historical round-24 tip used by the evidence | exit 1, mismatches 4, hygiene red |

### Mutants (smallest behaviour-bearing points, one at a time)

| id | mutation | mutated file sha256 |
|---|---|---|
| M1 | drop the negation-line check: `tools/mori-routed-r24.py:852-853` (`gitignore_negation_reinstates_bytecode`) replaced by `pass` | `effe59023db88fbb32230d1dc3f0c346069fce348811681f3c46b50b3562bc27` |
| M2 | drop the tracked-bytecode check: `tools/mori-routed-r24.py:855-860` (`bytecode = [...]`) replaced by `bytecode = []` | `81812308e0124d7bb222655ab2f95ca8d056708177a8cfa905c147628b3f7468` |
| M3 | exit 0 when hygiene fails: `tools/mori-routed-r24.py:946` `ok = mismatches == 0 and d4_held` → `ok = mismatches == 0` | `384a7aae1bcb660706230443de6261c9ade5abd444755c5eeb039e0d84d99a91` |

### Results (exit code / payload status / hygiene held)

| bytes | G0 | G1 | R1 | R2 | R3 | R4 | R5 | BASE |
|---|---|---|---|---|---|---|---|---|
| pristine | 0 held ✔ | 0 held ✔ | 1 failed ✘ | 1 failed ✘ | 1 failed ✘ | 1 failed ✘ | 0 held ✔ | 1 failed ✘ |
| M1 | 0 held | 0 held | 1 failed | **0 held** ✘ | 1 failed | 1 failed (2 reasons) | 0 held | 1 failed |
| M2 | 0 held | 0 held | 1 failed | 1 failed | **0 held** ✘ | 1 failed (2 reasons) | 0 held | 1 failed |
| M3 | 0 held | 0 held | **0 failed** ✘ | **0 failed** ✘ | **0 failed** ✘ | **0 failed** ✘ | 0 held | 1 failed |
| restored | 0 held | 0 held | 1 failed | 1 failed | 1 failed | 1 failed | 0 held | 1 failed |

✘ = the mutant's verdict differs from pristine on that fixture (mutant killed by that input).

## F1 (medium) — every mutant survives the committed evidence pair

**Survivors.** M1, M2 and M3 all produce a verdict **identical to pristine** on both committed evidence
inputs: the green after-value (`G0`, `mismatches 0, exit 0`) and the historical red before-value
(`BASE`, `28b79d3d`, `mismatches 4, exit 1`, hygiene red `no_pycache_ignore_rule`).

Evidence (pristine vs mutant on `BASE`, `28b79d3d1b76824f0c825aabe6cb6c5dc49961bf`):

```
pristine  exit=1 status=failed mism=4 hyg=False ['no_pycache_ignore_rule']
M1        exit=1 status=failed mism=4 hyg=False ['no_pycache_ignore_rule']
M2        exit=1 status=failed mism=4 hyg=False ['no_pycache_ignore_rule']
M3        exit=1 status=failed mism=4 hyg=False ['no_pycache_ignore_rule']
```

Reason: the real repository has no `!` line in its single tracked `.gitignore` and no tracked bytecode
under `tools/`, so on BASE the only live D4 reason is `no_pycache_ignore_rule`; and on BASE
`mismatches` is 4, so dropping `d4_held` from the exit rule cannot change the exit code either.

**What kills each survivor** (input, not committed anywhere in the lane):

* M1 → fixture **R2** (`.gitignore` gains `!tools/__pycache__/`): pristine exit 1 /
  `gitignore_negation_reinstates_bytecode: .gitignore`, M1 exit 0 / hygiene held. R4 also kills M1 at
  reason level (its reason list drops the negation reason).
* M2 → fixture **R3** (tracked `tools/__pycache__/probe.pyc`): pristine exit 1 / `tracked_bytecode_under_tools`,
  M2 exit 0 / hygiene held. R4 kills M2 at reason level too.
* M3 → fixtures **R1, R2, R3, R4** (any hygiene-red state with `mismatches == 0`): pristine exit 1,
  M3 exit 0.

**Smallest fix.** Give the tool the same frozen-case self-test the C2 tool has
(`tools/mori-job-runway.py --selftest` with `tools/fixtures/mori-job-runway/cases.json`): commit the red
and green sandbox states as fixture revisions and assert the verdict per fixture. With R2/R3 present, M1
and M2 die; with any hygiene-red fixture present, M3 dies. The cheapest alternative is three extra
committed evidence files under `.ufo/waves/round-25/evidence/` (one per D4 sub-reason) — but the tool
reads git objects at a revision, so fixture revisions are the honest form. **Severity: medium** — this is
a coverage finding, not a change of contract: the D4 sub-checks and the hygiene→exit coupling are
currently asserted by no committed input at all.

## F2 (medium) — reverting the D4 fix commit does not turn the tool red

R5 is a real `git revert e43d883` ("round-25: narrow the D4 ignore rule to `tools/__pycache__/`"), i.e.
the exact revert-one-fix the assignment asks for. Pristine tool on R5:

```
exit=0 status=held mism=0 hyg=True []
```

Green. Two reasons, both inside the tool's own contract:

1. `D4_IGNORE_LINES` (`tools/mori-routed-r24.py:129-136`) accepts the blanket `__pycache__/`, which the
   revert restores, so `no_pycache_ignore_rule` never fires.
2. The tracked-bytecode scan is scoped to `TOOLS_PREFIX = "tools/"` (`:138`, `:855-860`). The 212 tracked
   `.pyc` files the narrowing was made for live under `.ufo/waves/round-20/`, not under `tools/`:

```
git ls-files | grep -c '\.pyc$'      -> 212
git ls-files | grep '\.pyc$' | cut -d/ -f1 | sort | uniq -c  ->  212 .ufo
git ls-files 'tools/**' | grep -c '\.pyc$'  -> 0
```

This is the empirical form of `ReviewPycacheRule` F3 (".ufo/waves/round-25/w1/ReviewPycacheRule.md"):
a held D4 does not show the rule is safe. Contract A1 (`contract.md:111-114`) explicitly scopes the row
to "tracked path under `tools/`" and lists the blanket forms as accepted, so the tool is **conformant** —
the gap is in the predicate, not in the implementation.

**Smallest fix.** Either narrow the accepted set to the anchored form `tools/__pycache__/` (one-line
change at `:129-136`), or add the stronger condition the reviewer suggested to the hygiene row:
`git ls-files -c -i --exclude-standard` is empty at REV. The second is the one that catches the harm
directly (it lists the 212 tracked-but-ignored files) and needs no change to the accepted-line list.

## F3 (low) — exit code and payload `status` can disagree

`tools/mori-routed-r24.py:936` computes `"status": "held" if mismatches == 0 and d4_held else "failed"`
and `:946-947` computes `ok = mismatches == 0 and d4_held` a second time. M3 changes only the second
copy, so the mutant prints **exit 0 with `"status": "failed"`** on R1–R4:

```
M3 R1 exit=0 status=failed mism=0 hyg=False ['no_pycache_ignore_rule']
```

Two copies of one condition, no test tying them. **Smallest fix:** compute `ok` once and derive
`"status"` from it (`"status": "held" if ok else "failed"`), which makes the two impossible to diverge.
Severity low: pristine bytes are consistent.

## Restoration evidence

After each mutant the file was restored from a pristine copy and re-verified:

```
cp /tmp/mori-routed-r24.pristine.py tools/mori-routed-r24.py
sha256sum tools/mori-routed-r24.py
cf5ef5815f1118ae3595171edde7f527176fde03480665eb6bbb46921c2969ef
diff -q /tmp/mori-routed-r24.pristine.py tools/mori-routed-r24.py  -> identical
```

That sha256 is also the sha256 of the **lane's** `tools/mori-routed-r24.py` at `07a31ae`
(`sha256sum` in the lane: `cf5ef5815f1118ae3595171edde7f527176fde03480665eb6bbb46921c2969ef`), so the
restored bytes are the committed bytes, not merely "a copy that behaves the same". The restored tool was
re-run over all eight fixtures and every stdout was **byte-identical** to the pristine baseline
(`diff -q` on the raw JSON payloads: G0, G1, R1, R2, R3, R4, R5 all identical).

## Scope and compliance

* Lane read-only: no `jj` command at the fleet root, no `git add/commit/checkout/...` in the lane, no
  lane commit, no lane index or sibling-lane mutation. Only this report file was written in the lane.
* All commits and all tool mutations happened in `/fast/scratch/hyaku/mori-r25/w2-MutRoutedHygiene`
  (private clone); the clone was deleted after the run.
* No subagents, no background jobs, no `agent://all` message.
* Nothing was installed: `python3` and `git` were already present at the versions named above.
* Unrun checks: none — every number in this report comes from an executed command whose output is
  quoted.

## Bottom line

C1 holds at the landed tip (pristine tool, tip `07a31ae`: exit 0, `"mismatches": 0`, `"held": 4` of
`"items": 4`, hygiene held). The attack did not break the claim. What it did show: the committed
before/after evidence cannot distinguish the tool from three mutants that each silently disable one
D4 sub-check or the hygiene→exit coupling (F1), and the "revert one fix" of the D4 narrowing commit is
not detected at all (F2). Both are coverage findings about the predicate and its fixtures, not grounds
to change the contract.
