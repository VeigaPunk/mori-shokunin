# mori round 49 — disposition of the round-48 closure's routed defects

Written after the freeze `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`; it changes no frozen byte
(`contract.md`, `count-c1.py`, `count-c2.py`, `controls/`, `evidence/`, the source copies). It is the
file `contract.md` points at under "Entering lane tip". It was written during wave 1, before any C1 or
C2 landing: nothing here is a verdict on C1 or C2, and no value below is a landed-tip value.

Entering lane tip: `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86`.
Routed set: `corpus/lessons/round-48-verifier-spotcheck.md` §1 defects (a), (b) and §5 items 1-4.

Status words used below: **carried** (an owner and a check exist), **partly carried** (some sub-item
has no owner; named), **gap** (no owner, and the round does not hide it).

## Defect (a) / §5 item 1 — `.scratch/` residue left at closure

The closure counted 114 untracked `.scratch/*` directories and noted that
`tools/mori-unlanded-check.py` cannot see them (`in_scope()` is a positive whitelist of
`.ufo/waves/round-N/`, `corpus/`, `tools/` and top-level `*.md`; lines 13-15 say `.scratch/` is out of
scope "on purpose").

**What the round does.** Carries the closure's own two-part fix and makes the second part explicit: append
`/.scratch/` (anchored) to the tracked `.gitignore`, and delete only the untracked, uncited top-level
`.scratch` entries at round end, by a rule that keeps every directory a committed report cites. The rule,
the sandbox proof, the two guarded sets (13 tracked top-level entries / 225 files; 59 untracked but cited
directories) and the recompute command are in `w1/Mo49ExecScratchHygiene.md` §4-§5; the L1 lands the
`.gitignore` line and runs the deletion.

**Measured state at this writing** (2026-10-25T21:47:38-03:00): `git status --porcelain` = 175 lines of
which 166 are `.scratch`; 187 top-level `.scratch` entries (184 directories, 3 files); `du -sh .scratch`
= 25G; `git check-ignore -q .scratch/` exits 1 (not ignored); `.gitignore` is 4 rules. The residue grew
from the closure's 114 to 184 directories because two rounds of seats wrote into it.

**Carrier.** `w1/Mo49ExecScratchHygiene.md` (plan, proof, deletion set); `.gitignore` (one line, landing);
`w1/Mo49ScribeLogEntry.md` (LOG entry naming the fix); the L1 (deletion at round end, after wave 2).

**Check that will show it done.**

```
git status --porcelain | grep -c '^?? \.scratch/'
git check-ignore -q .scratch/; echo rc=$?
git ls-files .scratch | wc -l
```

Green is `0`, `rc=0`, `225`: no untracked scratch left, the rule is active, and no tracked scratch file was
untracked or deleted.

**Honest gap.** (i) The ignore line *hides* residue, it does not detect it: after the fix nothing in the
lane counts untracked `.scratch` entries, so the same accumulation is invisible again at the next closure
unless the §5 recompute is run as a process step — it is not a gate. (ii) The 225 tracked files under
`.scratch/` stay tracked (`gitignore` never untracks); the closure's sentence "remove the 114 untracked
scratch directories" does not touch them, and deleting them would dangle hashes that committed reports
cite (`round22` is 154 of the 225). The round treats them as evidence, not residue. (iii) The deletion has
not been run in wave 1; its result is a round-end act visible only to the closure.

## Defect (b) / §5 item 2 — the filed report's author date

**What the round does.** Records the mechanism instead of promising a fix it cannot make: the report is
filed after the last lane commit and the report prints both dates, and the disposition routes the real
repair to the fleet helper.

**Measured state.** Round-48's report `e60eb167` has `ai=2026-10-25 20:22:17 -0300`, `ci=20:27:04`, while
the lane tip it cites, `14c5110d`, is authored 20:26:17. The author field is not the filing time: in the
fleet repo each commit's author date equals the *committer date of its predecessor* (`e60eb167.ai ==
43997ee4.ci == 20:22:17`, and the identity holds for all 16 consecutive fleet commits from 19:54:40 to
20:31:37 — every author date equals its predecessor's committer date). That is
the moment the shared fleet working copy opened its next change, i.e. the end of whichever lane's commit
came before; `scripts/hyaku/fleet-commit.sh:84-86` sets author *identity* with `metaedit --update-author`
and then commits, and the author timestamp is inherited, not stamped.

**Carrier.** `contract.md` ("report author date at or after the lane tip it cites"), the L1's report step,
and this file. No wave-1 seat carries it; there is no prompt sentence about it
(`grep -n 'author date' /home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-49.md` → no match).

**Check.** The lane can check what it controls — that the report content post-dates the last lane commit:

```
stat -c '%y %n' .ufo/reports/round-49/mori.md
git -C /home/vgpnk/Projects/shokunin/mori-shokunin log -1 --format='%ci' <cited lane tip>
git -C /home/vgpnk/Projects/shokunin log -1 --format='%ai %ci' -- .ufo/reports/round-49/mori.md
```

Green is: report mtime ≥ the cited tip's committer date, and the two dates printed in the report.

**Honest gap.** The criterion *as written* is not satisfiable from inside a lane. The author date is the
shared fleet change's open time, set by the preceding commit of any lane; every lane write goes through
`fleet-commit.sh`, which does not stamp the author timestamp; no lane may run a mutating jj command to fix
it. So a concurrent fleet commit between the lane tip and the report will re-create the round-48 shape no
matter how carefully the lane files. Until the helper stamps author = commit time (fleet-side change, out
of this lane's scope), the closure should read "author date < cited tip" as this mechanism — but must still
check the ordering above, because a report written before its own last lane commit is the lane's error and
looks identical from the dates alone.

## §5 item 3 — the lane's own routes

Six sub-items. Five are carried in wave 1; one (K4) is not.

| route | what the round does | carrier | check | gap |
|---|---|---|---|---|
| seven v3 survivors (`v1_html_comment`, `v2_zwsp_header_prefix`, `v3b_tab_fence`, `v4_fourspace`, `v6_dup_authority`, `v7_split_tally`, `v8_html_table`; `w2/R48CritV3Junk1.md` "Seven survivors, seven caught") | the frozen counter carries one probe per shape (N1 comment row, N2 NBSP header + zero-width pin, N3 tab row in a fence, N4 four-space row, N5 duplicate authority row, N6 split tally, N7 HTML table row); the tool must score all seven `unmet` | `.ufo/waves/round-49/count-c1.py` (frozen; N1-N7) and `w1/Mo49ExecImplA.md` (rules F1-F5 that kill them) | `python3 .ufo/waves/round-49/count-c1.py --tool tools/mori-pin-check.py --rev <landed tip> --jobs 3` → `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26`, exit 0; the entering receipt already reads `C1=unmet junk_met=9 … variants=26` with N1-N9 `got=met` (`evidence/control-c1-tool-v3-entering.txt`) | the variants are the classes rounds 47-48 found, not the class of all junk; a tool can pass by being narrower, which is why H1-H7 and the real registry are in the predicate; wave 2 adds fresh classes and reports survivors as limits |
| K2-K8 classes (`w2/R48CritV3Junk2.md:29-36`) | K2 (env-prefix substitution) and K8 (rc-free PASS pins) get rules and arms in one seat; K3 (pin deletion), K6 (floor slack), K7 (line-count rebinding) in another; K5 (namespace join) plus defect X1 (TypeError instead of a finding) in a third | `w1/Mo49ExecK2K8.md`, `w1/Mo49ExecK3K6K7.md`, `w1/Mo49ExecK5X1.md` | per seat: the copy's `--selftest` prints `pass=N fail=0`, the real registry at `b3e3453d` stays `PIN_CHECK=met`, and each class's reproducer is shown failing on the copy | **K4 ("pins outside the self-test cell": full digest, `(N lines)`, non-`pass=` tally spelling) has no seat in wave 1 and no frozen probe** — `grep -c K4` over the 49 seat texts is 0, and the counter's variants are J1-J8/N1-N10/H1-H7. None of K2-K8 is in the frozen C1 predicate by the contract's named limit, so no frozen instrument will score them; the seats' own receipts are the only evidence, and K4 stays routed |
| rule R11 for D7 (misattribution: a row names one instrument, its self-test cell runs another) | the v4 candidate implements R11 from the round-48 fix diff, and the frozen N8 probe is the D7 shape | `w1/Mo49ExecImplA.md` (reads `r11.diff`), `.ufo/waves/round-49/count-c1.py` N8 | N8 reads `unmet` inside `C1=met junk_met=0`; the entering tool reads `N8 got=met` | a merged witness (`controls/tool-r48-merged-witness.py`) already reaches the target; the contract discloses that it is feasibility, not the claim, and that the new work is landing, arms and rules |
| selftest arms from the three mutation seats (`R48MutV3Header`, `R48MutV3Hidden`, `R48MutV3Bind`) | one seat adds an arm per surviving mutant of the header/visibility/bind rules (red on the mutant, green on the clean copy); a second seat adds the two survivors of the unlanded check (rename, 50-path cap) | `w1/Mo49ExecArmsHeader.md`, `w1/Mo49ExecArmsBindUnlanded.md` | each report pairs mutant → arm name → FAIL on mutant / PASS on clean copy, and the copy's `--selftest` prints `pass=N fail=0` | the frozen counter does not run the tool's `--selftest`, so the landed arm count is not a verified number; the arms' kill evidence is the only proof, and an arm that lands without a killed mutant would be invisible |
| successor C1 counter: opaque variant identity, an honest pin-updating edit | the counter names every variant copy and scratch dir by a sha256 prefix of its bytes, orders runs by that hash, builds the two second-file edits (N10 stale pin, H5 pin moved) inside a throwaway fixture repo, and carries both a red and a green fixture arm | `.ufo/waves/round-49/count-c1.py` (frozen, `evidence/freeze-sha256.txt` → `3c262a15…`); controls `stub-filename-sniffer.py` | `count-c1.py --selftest` → `C1_SELFTEST pass=44 fail=0` (`evidence/selftest-c1.txt`); the sniffer control scores `junk_met=18` under this counter (`evidence/control-c1-stub-filename-sniffer.txt`) while the same tool scored `met` under the round-48 counter (`evidence/control-c1-sniffer-under-r48-counter.txt`) | the handles hide the *name*, not the *shape* of an edit; a tool keyed on "the file differs from baseline" is only priced by the honest edits H6/H7 and the two real runs, and the counter does not run the tool's own selftest. Wave 2 is free to find more |
| unique seat names in wave 1 (M6) | the dispatch was built with one name per seat | `w1-dispatch.json` / `w1-spec.json` (L1) | `python3 -c "import json;d=json.load(open('.ufo/waves/round-49/w1-dispatch.json'));n=[t['name'] for t in d['taskCall']['tasks']];print(len(n),len(set(n)))"` → `49 49` (measured) | none in wave 1; wave 2's list does not exist yet (`.ufo/waves/round-49/w2/` is empty), so the property is wave-1 only |

## §5 item 4 — SHONEN boxes stay `[~]`

**Measured state.** `SHONEN.md` holds four boxes, all `[~]`, each with a pointer; `grep -c '^- \[x\]'` = 0,
`grep -c '^- \[~\]'` = 4.

**What the round does.** Keeps every box `[~]` and keeps each pointer resolvable; the report carries a
`## SHONEN` section with one line per box.

**Carrier.** `.ufo/reports/round-49/mori.md` (L1), `w1/Mo49ScribeScorecard.md` (the claim side of the same
evidence), `SHONEN.md` (pointers, not boxes).

**Check.** `grep -c '^## SHONEN' .ufo/reports/round-49/mori.md` → 1, followed by one `[~]`/`[ ]` line per
box; `grep -c '^- \[x\]' SHONEN.md` → 0.

**Why a lane cannot self-promote.** The round prompt makes `[x]` conditional on a **named non-author
verifier** (`/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-49.md:118`). The lane is the author of
both the checklist and every pointer behind it: its self-test tallies, its LOG, its "no cross-domain bleed"
claim. Ticking a box would be the same actor certifying its own work — the exact shape round 48's counter
leak was about (the object under test naming its own verdict). The non-author check that exists is the
closure (`corpus/lessons/round-48-verifier-spotcheck.md`, hyaku, committed as `b3e3453d`), and promotion
itself is operator-owned. So the boxes stay `[~]` even in the places this round improves them.

**Honest gap.** The closure could not fully check the boxes either: the self-tests and the round-wide log
are lane-asserted, and a reader must re-run the pins to test them (round 48 §5 item 4 says the same). Round
49 adds no non-author verifier for the SHONEN boxes; the boxes move only if the closure re-runs them.

## Operator teaching files

```
$ ls /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/operator-*.md
ls: cannot access '.../corpus/lessons/operator-*.md': No such file or directory   (rc 2, 2026-10-25T21:47-03:00)
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-files '*operator*'
.ufo/waves/round-16/operator-wrapup.json
```

**No `corpus/lessons/operator-*.md` exists**, so there is no operator teaching file to reflect this round
and the round claims none. The prompt's sentence "honor any `corpus/lessons/operator-*.md` teaching not yet
reflected" (`mori-round-49.md:396-399`) is satisfied vacuously; the same `ls` must be re-run at report time
in case a file appears mid-round. The only tracked path matching `*operator*` is a round-16 wave artefact,
not a teaching file. The operator-authored material this round *does* handle is
`considerthese/2026-10-25.md` (suggestion 3), carried by the considerthese item — a different channel from
`operator-*.md`.

## Summary

| routed item | status | owner | one-line check |
|---|---|---|---|
| (a) = §5.1 `.scratch` residue | partly carried | `w1/Mo49ExecScratchHygiene.md`, `.gitignore` (landing), L1 deletion | `git status --porcelain \| grep -c '^?? \.scratch/'` → 0; `git check-ignore -q .scratch/` → rc 0; `git ls-files .scratch \| wc -l` → 225 |
| (b) = §5.2 author date | gap (not lane-fixable) | L1 filing order + this file; helper change is fleet-side | report mtime ≥ cited tip committer date, both dates printed |
| §5.3 seven v3 survivors | carried | `count-c1.py` N1-N7, `w1/Mo49ExecImplA.md` | `C1=met … junk_met=0 … variants=26` |
| §5.3 K2-K8 | partly carried (K2, K3, K5, K6, K7, K8 carried; **K4 not**) | `w1/Mo49ExecK2K8.md`, `w1/Mo49ExecK3K6K7.md`, `w1/Mo49ExecK5X1.md` | per-seat selftest + real-registry run + mutant FAIL |
| §5.3 R11 for D7 | carried | `w1/Mo49ExecImplA.md`, N8 | N8 `unmet` inside a `C1=met` line |
| §5.3 mutation-seat arms | carried | `w1/Mo49ExecArmsHeader.md`, `w1/Mo49ExecArmsBindUnlanded.md` | mutant FAIL / clean PASS per arm; `pass=N fail=0` |
| §5.3 successor counter | carried | `.ufo/waves/round-49/count-c1.py` (frozen) | `C1_SELFTEST pass=44 fail=0`; sniffer `junk_met=18` |
| §5.3 unique seat names | carried (wave 1) | `w1-dispatch.json` | `49 49` |
| §5.4 SHONEN `[~]` | carried as a statement | report `## SHONEN`, `SHONEN.md` pointers | 4 `[~]`, 0 `[x]` |
| operator teaching files | nothing to do | — | `ls corpus/lessons/operator-*.md` → absent |

## Limits of this file

- Written in wave 1, before any C1/C2 landing; no landed-tip value, no claim verdict. The LOG entry's
  `[L1 fills commit]` markers are where landed hashes go.
- `.scratch` counts move while seats write: 126→171 porcelain lines within ~25 minutes of wave-1 activity
  (`w1/Mo49ExecScratchHygiene.md` §6). Each number above carries its timestamp.
- K4 is routed forward, not fixed: no wave-1 seat names it and the frozen counter has no probe for it.
- Whether the `.gitignore` line keeps the lane green is UNVERIFIED at this writing: the hygiene seat used an
  external `core.excludesFile` projection, not a landed rule.
- `evidence/control-c1-stub-filename-sniffer.txt` is byte-identical to
  `evidence/control-c1-stub-always-met.txt` (`cmp` → no difference; both `C1=unmet junk_met=18 … variants=26`).
  The sniffer's "the round-48 leak is closed" reading therefore rests on the file name plus
  `control-c1-sniffer-under-r48-counter.txt` (`C1=met … variants=12`), not on anything inside the two
  counter receipts; a reader should treat them as one measurement labelled twice until the counter prints
  the tool's identity.
