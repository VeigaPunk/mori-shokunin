# Mo49ScribeDisposition — round-49 disposition draft (round 49, w1)

Seat: `Mo49ScribeDisposition` (scribe, leaf). Lane: `mori-shokunin`.
Entering lane tip `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86`; freeze `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`.
Contract read in full at `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-49/contract.md`.
Scratch: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ScribeDisposition/` (created; holds only
`seats.txt` and `implA.txt`, dumped copies of the dispatch's seat texts).
Wrote only this report and that scratch dir. No edit to `SKILL.md`, `SOURCES.md`, `corpus/`, `tools/`, `LOG.md`,
`SCORECARD.md`, `QUALITY.md`, the frozen files, or `.gitignore`; no deletion; no git/jj mutation; no `pacman`;
no tool installed; no host write; no subagent.

The deliverable is the draft text of `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-49/disposition.md`,
fenced below. The L1 lands it as-is or edits it; this report makes no claim that it already exists.

Report: .ufo/waves/round-49/w1/Mo49ScribeDisposition.md

## 1. What I read and measured (commands, output, exit code)

Routed set (verbatim source of items):

```
$ sed -n '95,110p' /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-48-verifier-spotcheck.md
## 5. Routed defects for round 49

1. Add `.scratch/` to the lane's unlanded check or `.gitignore`, and remove the 114 untracked scratch
   directories (`git status --porcelain` leftover).
2. Keep the filed report's author date at or after the lane tip it cites (author date 20:22:17 vs cited
   commit 20:26:17).
3. Carry the lane's own routes: seven v3 survivors (`R48CritV3Junk1`), the K2-K8 classes, rule R11 for D7,
   the selftest arms from the three mutation seats, a successor C1 counter that hides the variant identity
   and includes an honest pin-updating edit, unique seat names in wave 1 (M6).
4. SHONEN boxes are all `[~]` and not fully checkable by a non-author this round (the self-tests and a
   round-wide log are lane-asserted); promotion stays operator-owned.
```
(§1 defects (a),(b) at lines 23-26 of the same file: 114 untracked `.scratch/*` dirs; report author date
20:22:17 vs cited commit authored 20:26:17.)

State measured for this draft (each command run from the lane root, `date -Iseconds` = `2026-10-25T21:47:38-03:00`):

```
$ git status --porcelain | awk '/^\?\? \.scratch\//{s++} END{print "porcelain_total="NR, "scratch_lines="s+0}'
porcelain_total=175 scratch_lines=166
$ find .scratch -maxdepth 1 -mindepth 1 | wc -l ; find .scratch -maxdepth 1 -mindepth 1 -type d | wc -l
187
184
$ du -sh .scratch
25G	.scratch
$ git check-ignore -q .scratch/ && echo ignored || echo "not-ignored rc=$?"
not-ignored rc=1
$ wc -l .gitignore
4 .gitignore
$ git ls-tree -r --name-only b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 .scratch | wc -l
225
$ git ls-files .scratch | cut -d/ -f2 | sort | uniq -c | sort -rn | head -1
    154 round22
$ grep -c '^- \[x\]' SHONEN.md ; grep -c '^- \[~\]' SHONEN.md
0
4
$ ls /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/operator-*.md
ls: cannot access '/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/operator-*.md': No such file or directory   rc=2
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-files '*operator*'
.ufo/waves/round-16/operator-wrapup.json
$ python3 -c "import json;d=json.load(open('.ufo/waves/round-49/w1-dispatch.json'));n=[t['name'] for t in d['taskCall']['tasks']];print(len(n),len(set(n)))"
49 49                      # 49 tasks, 49 distinct names, no duplicate
$ S=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ScribeDisposition/seats.txt
$ grep -c -F K4 "$S" ; grep -c -F 'non-pass' "$S" ; grep -c -F 'full digest' "$S"
0
0
0
```

Author-date mechanism, measured read-only on the fleet repo:

```
$ git -C /home/vgpnk/Projects/shokunin log --format='%h ai=%ai ci=%ci %s' -3 -- .ufo/reports/round-48/mori.md
e60eb167 ai=2026-10-25 20:22:17 -0300 ci=2026-10-25 20:27:04 -0300 round-48: mori report
$ git -C /home/vgpnk/Projects/shokunin log --format='%h ai=%ai ci=%ci' --since='2026-10-25 19:50' --until='2026-10-25 20:32'
48bca5b2 ai=20:31:07 ci=20:31:37
86475fb9 ai=20:28:54 ci=20:31:07
4ea5a273 ai=20:28:52 ci=20:28:54
3fe4f939 ai=20:27:34 ci=20:28:52
9732bd29 ai=20:27:29 ci=20:27:34
c00df931 ai=20:27:17 ci=20:27:29
e28ab48a ai=20:27:14 ci=20:27:17
2fe0478c ai=20:27:04 ci=20:27:14
e60eb167 ai=20:22:17 ci=20:27:04     <- mori r48 report
43997ee4 ai=20:21:54 ci=20:22:17     <- predecessor; ci == e60eb167.ai
```

Facts used in the draft, with their source:

| fact | source |
|---|---|
| 114 untracked `.scratch` dirs at round-48 closure; unlanded check blind to them | `corpus/lessons/round-48-verifier-spotcheck.md:23`, §5 item 1 |
| unlanded check scope is a positive whitelist; `.scratch/` and ignored paths excluded "on purpose" | `tools/mori-unlanded-check.py:13-15`, `in_scope()` `:43-46` |
| hygiene seat's plan, proposed `/.scratch/`, deletion candidate set, cited-dir list | `.ufo/waves/round-49/w1/Mo49ExecScratchHygiene.md` (§1, §4, §5) |
| 225 tracked `.scratch` files (154 under `.scratch/round22/`) survive any ignore rule | `git ls-tree -r --name-only b3e3453d .scratch \| wc -l` → 225 |
| author date of a fleet commit == committer date of its predecessor | the date chain above; holds for all 16 fleet commits 19:54:40→20:31:37 |
| helper stamps author identity, then commits | `scripts/hyaku/fleet-commit.sh:84-86` |
| seven v3 survivors = v1/v2/v3b/v4/v6/v7/v8 | `.ufo/waves/round-48/w2/R48CritV3Junk1.md` results table ("Seven survivors, seven caught") |
| N1-N7 cover those seven shapes; N8 is the D7 re-point; N9/N10 extra | `.ufo/waves/round-49/count-c1.py:26-48` (docstring), contract §C1 |
| before receipt: N1-N9 print `met` under the entering v3 tool | `.ufo/waves/round-49/evidence/control-c1-tool-v3-entering.txt` → `C1=unmet junk_met=9 … variants=26`, exit=1 |
| freeze selftests | `evidence/selftest-c1.txt` `C1_SELFTEST pass=44 fail=0`; `selftest-c2.txt` `C2_SELFTEST pass=26 fail=0` |
| K2-K8 definitions | `.ufo/waves/round-48/w2/R48CritV3Junk2.md:29-36` |
| K4 has no wave-1 seat and no counter variant | `grep -c K4` on the 49 seat texts → 0; contract variant list N1-N10/H1-H7 |
| `[x]` needs a named non-author verifier | `/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-49.md:118` |
| operator teaching files are the prompt's channel: "honor any `corpus/lessons/operator-*.md`" | `mori-round-49.md:396-399` |

Time-sensitivity: my snapshot (21:47:38) and the hygiene seat's (21:42-03:00) differ because seats write
`.scratch` continuously — the seat recorded 171 porcelain lines / 151 scratch lines / 22G / 470,162 untracked
files at 21:42 and 126→171 porcelain lines within ~25 minutes (§6 of its report). The draft quotes each with
its own timestamp and does not pretend they are one measurement.

## 2. Draft — `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-49/disposition.md`

````markdown
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
````

## 3. Why each claim in the draft is checkable (self-check of the draft)

- Every "carried" row names a concrete file that exists at this writing (all `w1/*.md` rows cited were
  present when I read them: `Mo49ExecScratchHygiene.md`, and the four C1 seats are in the dispatch table).
  Rows for seats not yet filed (`Mo49ExecImplA`, `Mo49ExecK2K8`, `Mo49ExecK3K6K7`, `Mo49ExecK5X1`,
  `Mo49ExecArmsHeader`, `Mo49ExecArmsBindUnlanded`) cite the dispatch, and the draft says "carrier", not
  "result" — it never claims those seats passed.
- The before-value quoted (`C1=unmet junk_met=9 honest_unmet=0 real=met errors=0 variants=26`, exit=1) is
  the receipt's own last two lines, read byte-for-byte, not inferred.
- The seven-survivor → N1-N7 mapping is by shape, not by hash: the counter's docstring and the round-48
  report's table agree one-for-one (comment row / NBSP+ZWSP / tab in fence / four-space / duplicate
  authority / split tally / HTML table). No counter run was needed to establish it; I did not run the
  counter (it is the seats' job and takes ~10 minutes).
- The K4 gap is measured (0 name hits in the 49 seat texts; no K4 variant in the docstring) and cross-read
  against `R48CritV3Junk2.md:32`, which defines K4 separately from K3 and K7.
- The author-date mechanism is measured from sixteen consecutive fleet commits plus the round-48 report, and
  the helper lines are quoted from the script; the *cause* (jj inheriting the change's author timestamp)
  is marked as inference in the draft only where it is inference — the draft states the identity and the
  helper behaviour as observed, and the "shared working copy" framing as the observed identity's reading.

## 4. Touched surfaces

- Created: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-49/w1/Mo49ScribeDisposition.md`
  (this report).
- Created: `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49ScribeDisposition/` (`seats.txt`,
  `implA.txt`).
- No other write. `git status` for the lane was read only; the fleet repo, `shokuknow`, sibling lanes and
  the jj/git index were not touched.

## 5. Out of scope (not done here)

- `.gitignore` edit, `.scratch` deletion, `tools/` change, `SHONEN.md`/`LOG.md`/`SCORECARD.md` edit — the
  L1 integrates; this seat drafts text only.
- Running `count-c1.py`/`count-c2.py` end to end, the lane gates, or any host read beyond `ls`-class
  commands; the disposition is a document, not a gate.
- Wave 2: `.ufo/waves/round-49/w2/` is empty at this writing, so the "carried" column cannot claim a
  second-wave falsifier for any routed item yet.

## Findings

1. **MED — routed defect (b) has no owner and is not lane-satisfiable as written.**
   `corpus/lessons/round-48-verifier-spotcheck.md:101` asks for the report's author date to be at or after
   the lane tip it cites, but the author date is the shared fleet working copy's change-open time
   (`e60eb167.ai == 43997ee4.ci == 20:22:17`; the identity holds for all 16 fleet commits 19:54:40→20:31:37), and `scripts/hyaku/fleet-commit.sh:84-86` stamps identity, not the timestamp. No
   wave-1 seat carries it and the round prompt has no sentence about it. The draft substitutes a
   lane-controllable check (report mtime vs cited tip committer date) and routes the repair fleet-side.
2. **MED — routed defect (a) is not "just" `.gitignore` + delete: 225 `.scratch` files are tracked.**
   `git ls-tree -r --name-only b3e3453d .scratch | wc -l` → 225 (154 under `.scratch/round22/`), and
   `git check-ignore -q .scratch/` → rc 1 with a 4-rule `.gitignore`. An anchored `/.scratch/` line leaves
   all 225 tracked (correct: they are cited evidence), so the closure's "remove the 114 untracked
   directories" covers only part of the tree; a blanket `rm -rf .scratch/*` would dangle committed hashes.
3. **MED — the fix hides residue instead of detecting it.** `tools/mori-unlanded-check.py:13-15` excludes
   `.scratch/` and ignored paths on purpose, and nothing else counts untracked scratch entries; residue
   grew 114 → 184 directories between the round-48 closure and this snapshot (`find .scratch -maxdepth 1
   -mindepth 1 -type d | wc -l` → 184, `du -sh .scratch` → 25G, 166 porcelain lines at
   2026-10-25T21:47:38-03:00). The round's mitigation is a process step (`w1/Mo49ExecScratchHygiene.md` §5),
   not a gate.
4. **MED — K4 has no wave-1 carrier and no frozen probe.** `R48CritV3Junk2.md:32` defines K4 (pins outside
   the self-test cell: full digest, `(N lines)`, non-`pass=` tally spelling); the 49 seat texts contain no
   `K4` (0 hits) and `count-c1.py`'s variants are J1-J8/N1-N10/H1-H7, none of which is a K4 shape. Item 3's
   "the K2-K8 classes" is therefore only 6/7 carried, and the contract's named limit (K2-K8 outside the
   predicate) means no frozen instrument would report it either.
5. **LOW — "carried" for §5 item 3 is wave-1 only.** `.ufo/waves/round-49/w2/` is empty at this writing, so
   the disposition cannot name a second-wave falsifier for the survivors, the K rules, R11 or the arms; if
   wave 2 is built with different names, the disposition's carrier column needs an update before it is
   filed as final.
6. **LOW — the routed-list has a duplicated item (a)=§5.1 and (b)=§5.2.** The closure lists them twice
   (§1 defects and §5 items 1-2). The draft cross-references them explicitly instead of counting nine
   items, so an L1 reading either section gets the same eight rows.
7. **LOW — `SHONEN.md` has no `[x]` and the round cannot change that.** `grep -c '^- \[x\]' SHONEN.md` → 0,
   `grep -c '^- \[~\]'` → 4; the prompt's non-author-verifier rule
   (`/home/vgpnk/Projects/shokunin/.ufo/prompts/mori-round-49.md:118`) makes promotion operator-owned. This
   is a statement, not a defect of round 49; it is listed so the closure does not read the round's silence
   as an omission.
8. **LOW — two frozen control receipts are byte-identical, so the sniffer evidence is name-labelled only.**
   `cmp .ufo/waves/round-49/evidence/control-c1-stub-filename-sniffer.txt .ufo/waves/round-49/evidence/control-c1-stub-always-met.txt`
   → no difference (both `C1=unmet junk_met=18 honest_unmet=0 real=met errors=0 variants=26`, exit=1;
   `evidence/freeze-sha256.txt` gives both the same hash `67396610…`). The "round-48 leak is closed" reading
   rests on the file name plus `control-c1-sniffer-under-r48-counter.txt` (`C1=met … variants=12`). The draft
   states this as a limit rather than quoting the two files as separate measurements.
