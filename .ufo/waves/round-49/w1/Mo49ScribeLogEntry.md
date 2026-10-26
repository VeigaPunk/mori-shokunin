# Mo49ScribeLogEntry — round 49 `LOG.md` entry (draft only)

Seat: wave w1, lane mori-shokunin. Leaf seat: no subagents. Lane files were read-only except this
report; `LOG.md` was not edited, no scratch directory was created (no lane instrument was run), no
git/jj state was touched, nothing was committed.

## Behavior

Drafted the `## Round 49` entry for `LOG.md`, in a fenced block below, ready to append after the
current tail (`LOG.md:2722`, the round-48 entry). Nothing in the draft claims a landing: the landed
tip, the two after-values, the wave-1 report tally, the QUALITY criterion number, the SHONEN line and
`disposition.md` are all `[L1 fills commit]`.

The draft covers, in the house order of rounds 47–48 (entering tip → freeze → before receipts →
assimilation → considerthese → mistakes → hygiene → routed defects → wave record → boundaries):
entering tip and freeze, both claims with their before receipts and control matrix, the freeze's own
disclosure (merged witness), the journal-retention assimilation with the S351 flip, considerthese
suggestion 3, the two mistakes mined, the `.scratch` hygiene fix, and the round-48 closure's routed
defects 1–4 each with a disposition.

## Evidence (commands, outputs, exits)

Every command below ran with cwd `/home/vgpnk/Projects/shokunin/mori-shokunin`. No counter was re-run
(each takes ~10 minutes and its receipts are committed); the receipts were read and cross-checked
against bytes I could hash.

1. `git rev-parse HEAD` → `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`; `git log --oneline -5` → the
   freeze on top of `b3e3453d` (round-48 closure). **Nothing has landed this round yet.**
2. `sha256sum -c .ufo/waves/round-49/evidence/freeze-sha256.txt` → 0 non-OK lines; tail
   `.ufo/waves/round-49/assimilation/reg-ids: OK`, `…/staged-ids: OK`; rc 0. 31 pinned paths.
3. `git show b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86:tools/mori-pin-check.py | sha256sum` →
   `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1`; `sha256sum
   .ufo/waves/round-49/controls/tool-v3-entering.py` → same digest. The do-nothing control is the
   entering tool byte-for-byte.
4. `.ufo/waves/round-49/evidence/control-c1-tool-v3-entering.txt` → 26 `variant name=…` lines
   (J1–J8 `got=unmet`; H1–H4 `got=met`; N1–N9 `got=met`; N10 `got=unmet`; H5/H6/H7 `got=met`;
   real and real-opaque `got=met`) and `C1=unmet junk_met=9 honest_unmet=0 real=met errors=0
   variants=26 rev=b3e3453d…`, `exit=1`.
5. `.ufo/waves/round-49/evidence/control-c2-donothing.txt` → `C2=unmet claims=0 located=0
   quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad
   rev=b3e3453d… failed=entry_absent,pins`, `exit=1`.
6. Sniffer pair: `evidence/control-c1-stub-filename-sniffer.txt` → `C1=unmet junk_met=18 … variants=26`
   (`exit=1`); `evidence/control-c1-sniffer-under-r48-counter.txt` → `C1=met junk_met=0 … variants=12`
   (`exit=0`). Same control file, two counters, opposite verdicts.
7. `evidence/selftest-c1.txt` → `C1_SELFTEST pass=44 fail=0`; `evidence/selftest-c2.txt` →
   `C2_SELFTEST pass=26 fail=0`.
8. `evidence/census-start.txt` → 21 lines: 20 `W04` duplicate-url warnings (including S351 and S470
   both on the `journalctl(1)` URL) and one `mori ok`.
9. `git show HEAD:corpus/SOURCES.md | grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` → `257`; last row
   `| S484 |`. `corpus/SOURCES.md:248` is S351 (`rejected`, flip text) and `:249` is S470 (`mined`).
10. `.ufo/waves/round-49/w1-dispatch.json` → `counts {spawn: 49, resume: 0, total: 49}`, 49 `tasks`,
    49 unique names, all prefixed `Mo49`; roles: executor 16, scribe 14, scout 4, connector 4, critic 4,
    reviewer 3, mutation-tester 2, sentinel 1, simplifier 1.
11. Worktree at `2026-10-25T21:46:34-03:00`, `git -c core.quotepath=off status --porcelain -z` parsed:
    **0** modified/staged tracked paths; 177 untracked entries — 165 under `.scratch/`, 7 under
    `.ufo/waves/round-40/scratch/`, 5 round-49 wave files (`w1-spec.json`, `w1-dispatch.json`,
    `w1.ready`, `w1-validate.err`, `w1/`). Counts move while the wave runs.
12. `ls -d .scratch/*/ | sed 's#\.scratch/##;s#[-_].*##' | sort | uniq -c` at `2026-10-25T21:46:39` →
    68 `pin`, 34 `r48`, 33 `r48w2`, 12 `c1`, 26 `r49`, plus ten single dirs (`round22`, `CritFreezeTiming`,
    …). Round-48-class prefixes sum to **147** (the round-48 closure counted 114 at `14c5110d`).
13. `git ls-files .scratch | wc -l` → `225` files across **13** distinct paths (10 directories, 3 files);
    `du -sh .scratch` → `23G` (completed 21:46:39; an earlier read in the same minute printed `25G`,
    the tree is written while the wave runs). `.gitignore` has four lines (`.ufo/interactive-sessions/`,
    `.ufo/worktrees/`, `__pycache__/`, `*.pyc`) and **no** `.scratch/` entry.
14. `tools/mori-unlanded-check.py:15` states "`.scratch/` and anything git ignores are outside the scope
    on purpose"; the selftest arm `outside_scope_and_scratch_not_listed` is at `:132-134`.
15. `ls .ufo/waves/round-49` → no `disposition.md`; `w2/` exists and is empty; `w1/` holds two seat
    reports plus `swarm-registry.json` at read time.
16. Read-only (nothing executed there) `/home/vgpnk/Projects/shokuknow/merge/mori/`: staged entries
    `knowledge/corpus/knowledge/journal-effective-retention-r45.md`,
    `journal-reach-at-ceiling-r46.md`, `runtime-journal-reach-is-the-boot-r49.md`; `SOURCES.append.md`
    rows S516 (journald.conf(5)), S532 (journalctl(1)), S560 (systemd-journald.service(8)), and the
    own-work rows S524/S537/S544. The staged numbers are 250.3M/258.3M against 256M and six boots.
17. `corpus/evidence/sources-r49/host-journal-reach.txt` (98 lines) → `--disk-usage` 56M; `--system`
    19M; `--user` 37M; drop-in `/etc/systemd/journald.conf.d/size.conf` 46 bytes, mtime 2026-10-16,
    `SystemMaxUse=256M` / `RuntimeMaxUse=64M`; daemon start-up `System Journal … is 45M, max 256M,
    210.9M free` and `Runtime Journal … is 8M, max 64M, 56M free`; `findmnt /run` → `tmpfs`;
    `/run/log/journal` empty; `--list-boots` → two boots.
18. `count-c2.py:29-33,67-75,160-176` (read, not run): entry path `corpus/knowledge/journal-reach-r49.md`,
    `OPENED=2026-10-25`, `MIN_CLAIMS=8`, `MIN_SOURCES=3`, words 6–25, source row must be 11 cells with
    status `mined`, opened that day, a URL among the four `COPIES`, and the entry in `used-by`; the
    entry's head `source:` lines must cite every S-id that appears in the table.

## Draft entry (fenced, for `LOG.md` after line 2722)

````markdown
## Round 49 (L1 MoriR49; C1 calibration, C2 depth)

Entering `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86` (round-48 closure,
`corpus/lessons/round-48-verifier-spotcheck.md`); froze at
`0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115` (contract P-C1/P-C2, `count-c1.py`, `count-c2.py`, seven
controls, the freeze receipts, the four committed source copies under `corpus/evidence/sources-r49/`).
31 pinned paths, `sha256sum -c` → 31 OK, 0 mismatches. Round-start census
`sources-census.sh validate --root <fleet> mori` → 21 lines, 20 `W04` duplicate-url warnings and one
`ok` (`evidence/census-start.txt`); registry 257 rows, last `S484`. Scores entering: coverage 6,
operability 7, depth 5, freshness 5, calibration 5, adjacency 6 — both claims work a lowest (tied 5)
axis; no score change is claimed by the lane, the closure rules.

**Before**, measured at the entering tip with the frozen counters (`evidence/control-c1-*.txt`,
`evidence/control-c2-donothing.txt`):

- **C1 (calibration).** The entering v3 reconciler (`controls/tool-v3-entering.py`, sha256 `85a89a3b…`,
  byte-equal to `tools/mori-pin-check.py` at `b3e3453d`) prints `C1=unmet junk_met=9 honest_unmet=0
  real=met errors=0 variants=26`, rc 1 — it is green on N1–N9 (a gate row inside an HTML comment; NBSP
  in the self-test header plus a zero-width space in the pin token; a tab-indented pipe row in a fence;
  a four-space-indented pipe row outside a table; a second row for one command with a contradicting
  exit contract; a pin-less row with prose `fail=0` and a continuation line recording `fail=3`; the
  junk row as HTML table markup; the reconciler's own row re-pointed; a row naming the gate registry
  while pinning the reconciler's tally). Controls: `stub-always-met` `junk_met=18`;
  `stub-always-unmet` `honest_unmet=8 real=unmet`; `tool-r48-surface-fixes` `junk_met=1` (N9);
  `tool-r48-r11-only` `junk_met=7` (N1–N7) — the two partial candidates show each half of the target is
  separately required. `tool-r48-merged-witness` already prints the target line (`… variants=26`,
  selftest 65/65): a feasibility witness only, the two round-48 patch sets merged mechanically by the
  L1; the claim does not rest on it. The witness discloses that the target tool bytes are largely
  pre-existing round-48 seat output, so this round's new work is (a) landing that tool in `tools/` with
  its selftest arms and the K-class rules wave 1 proves, (b) the successor counter itself (opaque
  handles, a fixture-built honest pin-updating edit, three new honest controls, the real registry read
  twice), (c) the false-red audit of the new rules against earlier `SKILL.md` revisions. Counter
  selftest `C1_SELFTEST pass=44 fail=0`.
- **C2 (depth).** `python3 .ufo/waves/round-49/count-c2.py b3e3453d` → `C2=unmet claims=0 located=0
  quote_missing=0 bad_rows=0 sources=0 source_rows=bad pins=bad provenance=bad
  rev=b3e3453d… failed=entry_absent,pins`, rc 1 (the pins arm is red because the copies are not at the
  entering revision). Sweep before data (`evidence/sweep-journal-rows.txt`): `SystemMaxUse`,
  `MaxRetentionSec` and `RuntimeMaxUse` occur 0 times in `corpus/SOURCES.md` and `corpus/knowledge/` at
  `b3e3453d`, and no row names the `journald.conf` page; the lane held `--disk-usage` (S470) and the
  "vacuumed → no retained record" alarm class without the rule that sets the reach. `C2_SELFTEST
  pass=26 fail=0`.

After at the landed tip: C1 `[L1 fills commit]`, C2 `[L1 fills commit]`. Kill rule either way: a
counter re-scored under changed bytes after wave-1 scoring is not this claim's rule, and `unmet` at
the landed tip means the claim is not verified, not that a waiver applies.

**Assimilation (FR1 theme, journal retention reach).** Package
`/home/vgpnk/Projects/shokuknow/merge/mori/` read only; no campaign tool run, nothing written there.
Collision check before any append (`assimilation/{reg-ids,staged-ids,collisions}`): registry 257 ids
vs 136 staged ids → 14 collisions `S471`–`S484` (all rounds 47–48); the three staged rows adopted by
document (`S516` journald.conf(5), `S532` journalctl(1), `S560` systemd-journald.service(8)) collide
with none. Staged `journal-effective-retention-r45`, `journal-reach-at-ceiling-r46` and
`runtime-journal-reach-is-the-boot-r49` become one entry `corpus/knowledge/journal-reach-r49.md`,
renumbered by document to the four new rows `S485`–`S488` (three manual pages plus this round's
read-only host receipt); the staged own-work rows `S524`/`S537`/`S544` cite receipts outside this lane
and are not adopted — this round's host receipt replaces them. **S351 flip:** the rejected
`journalctl(1)` row stays rejected; a new row whose `teaches` opens `supersedes S351 —` carries the
flip predicate (the public `--vacuum-size=` sentence plus a committed read-only `--disk-usage`
receipt, no MESSAGE grep). That row shares S351's and S470's URL, so the round-end census is expected
to add a third `W04` for it (`[L1 fills commit]`). The quarantine slice `S244`/`S262`/`S268` keeps its
round-48 verdicts and is not appended; the 0–3-space guard proof is `[L1 fills commit]`.

Host receipt (`corpus/evidence/sources-r49/host-journal-reach.txt`, captured
2026-10-25T20:43:09-03:00): total `--disk-usage` 56M (system 19M, user 37M), the 46-byte drop-in from
2026-10-16 still setting `SystemMaxUse=256M` / `RuntimeMaxUse=64M`, the daemon's own start-up lines
reading 45M of 256M and 8M of 64M, an empty `/run/log/journal` on `tmpfs`, and **two** boots retained.
The staged entries carry 250.3M/258.3M against that ceiling and six boots (2026-10-24), and S470's
entry 269M — one day's movement, which is why the entry re-grounds every number on this receipt and
names the receipt date as its own limit.

**considerthese (item 10).** `considerthese/2026-10-25.md` suggestion 3 — flagged-versus-fixed critic
count, opened 2026-10-25, read-only, not edited — lands as a lesson measurement over round 48 and a
QUALITY criterion with its counting command. Motivating evidence: round 45's `w1/CritAxisHarm.md`
flagged the stale registry cells before `baabc992` landed and nothing in the round enforced the flag.
Measurement and criterion number `[L1 fills commit]`; suggestions 1, 2 and 4 were mined by rounds 47–48.

**Mistakes mined.**

- *The harness leaked the variant's identity.* Round 48's counter handed the tool the harness's own
  file names, so a tool that never read the registry passed (`w1/CritC1Counter.md` F1). This round's
  counter hands every variant to the tool under a sha256-derived opaque name — copy and scratch
  directory named from the variant's bytes, run order by that hash, N10/H5 built in a throwaway
  fixture repository whose path and commit message carry no variant name. Shown able to fail by the
  sniffer pair: `controls/stub-filename-sniffer.py` scores `C1=met junk_met=0 … variants=12` under the
  round-48 counter (`evidence/control-c1-sniffer-under-r48-counter.txt`) and `C1=unmet junk_met=18 …
  variants=26` here (`evidence/control-c1-stub-filename-sniffer.txt`).
- *Round work that is only ever untracked.* Round 47's late `w2` files and round 48's `.scratch`
  residue are one class; see routed defect 1.

**`.scratch` hygiene fix (round-48 routed defect 1).** `.gitignore` gains `.scratch/` and the round-48
residue is removed: `[L1 fills commit]`. Observed at the freeze, before the fix — `.gitignore` has
four lines and no `.scratch/` entry; `git status --porcelain -z` at 2026-10-25T21:46-03:00 shows
**165** untracked entries under `.scratch/`, of which **147** carry round-48 directory prefixes
(68 `pin-check-*`, 34 `r48-*`, 33 `r48w2-*`, 12 `c1-*`; the closure counted 114 at `14c5110d`, and the
count moves while a wave runs), **7** under `.ufo/waves/round-40/scratch/` — a residue class the
closure did not count and an ignore entry does not reach — and 5 round-49 wave files; no tracked file
is modified. An ignore-only fix does not clean what is already tracked: `git ls-files .scratch` → 225
files across 13 paths, and `du -sh .scratch` → 23G. `tools/mori-unlanded-check.py:15` excludes
`.scratch/` on purpose (selftest arm `outside_scope_and_scratch_not_listed`, `:132-134`), so the ignore
entry and the scope exclusion have to be decided together, or the class stays invisible to the
pre-report gate.

**Round-48 closure routed defects** (`corpus/lessons/round-48-verifier-spotcheck.md` §5), disposition:

| # | defect | disposition |
|---|---|---|
| 1 | `.scratch/` in the unlanded check or `.gitignore`, and remove the 114 untracked directories | `.gitignore` entry plus removal: `[L1 fills commit]`; see the hygiene paragraph for the observed state and its two gaps (225 already-tracked files; the `mori-unlanded-check.py` scope) |
| 2 | the report's author date at or after the lane tip it cites | this round's report is filed with an author date at or after the tip it cites: `[L1 fills commit]` |
| 3 | the lane's own routes: seven v3 survivors, K2–K8, R11 for D7, the mutation seats' selftest arms, a successor C1 counter that hides the variant identity and includes an honest pin-updating edit, unique seat names | carried into C1: N1–N7 are the seven survivors, N8 the re-pointed-own-row (D7) class, N9/N10 new, H5 the fixture-built honest pin-updating edit, the opaque handles above, and `Mo49`-prefixed unique seat names; landing `[L1 fills commit]`. K2–K8 stay named limits of P-C1 and are still routed |
| 4 | SHONEN boxes all `[~]` and not fully checkable by a non-author; promotion is operator-owned | round-49 SHONEN update `[L1 fills commit]`; the boxes stay `[~]` with pointers and no `[x]` |

**Wave record.** Two v1 waves (policy `scripts/hyaku/ufo-wave-policy.json`, band 32–64); the L1 holds
the planner seat. Wave 1 (build + first falsifiers): 49 seats (`counts.spawn=49`, 49 unique seat
names), executor 16, scribe 14, scout 4, connector 4, critic 4, reviewer 3, mutation-tester 2,
sentinel 1, simplifier 1; reports on disk `[L1 fills commit]`. Wave 2 (falsify, after landing):
`[L1 fills commit]`. Round total `[L1 fills commit]` (two waves, band 32–64 each, total held
within 64–100). No seat wrote outside its report path; the wave-1 spec, dispatch, ready
file and `w1/` are untracked round work that must land before the report is filed (round-48 M1 class)
— `tools/mori-unlanded-check.py` before the report is the gate.

**Boundaries.** Detection and report only: the host receipt is read-only (`--disk-usage`,
`cat-config`, `stat`, `findmnt`, `ls -A`, `--list-boots`, one `-b 0 -u systemd-journald` read); no
vacuum, rotate, `systemctl` or config change was run. Nothing under
`/home/vgpnk/Projects/shokuknow/` was executed or written; `/home/vgpnk/Projects/shokuknow/merge/mori`
was read as bytes only.
````

## Gates / checks I did not run

- No counter was re-run (`count-c1.py` ~10 min with `--jobs 4`; `count-c2.py`); the committed receipts
  are the evidence and are consistent with the bytes I hashed (entering tool digest, freeze manifest).
- No build, lint, test, census, gate or selftest was run. Verification of the draft entry's own claims
  is the L1's and later the closure's.
- `[INFERENCE]`: the S485→journald.conf(5) assignment comes from the sibling draft
  `w1/Mo49ScribeRowConf.md` (a seat draft, not registry bytes); S486/S487/S488 are placed by the
  contract's source order. Marked `[L1 fills commit]` in the draft rather than asserted.

## Touched surfaces

- Wrote `.ufo/waves/round-49/w1/Mo49ScribeLogEntry.md` (this file). Nothing else.
- No `TMPDIR` scratch directory was needed: no lane instrument ran.

## Out of scope (not done here)

- Appending to `LOG.md`; any commit; `SKILL.md`, `corpus/SOURCES.md`, `corpus/knowledge/`, `tools/`,
  `SCORECARD.md`, `QUALITY.md`, `SHONEN.md` edits; `.ufo/waves/round-49/disposition.md`; the wave-2 plan.

## Findings

1. **MED** — `.ufo/waves/round-49/disposition.md` does not exist, though `contract.md` declares it as
   the round-48 spot-check disposition ("written after the freeze; it changes no frozen byte"). The
   draft entry therefore cites no such file. File: `.ufo/waves/round-49/disposition.md` (absent).
2. **MED** — The routed-defect-1 fix cannot be an ignore entry alone: `.gitignore:1-4` has no
   `.scratch/`, yet `git ls-files .scratch` lists 225 tracked files across 13 paths and the directory
   is 23G. An ignore entry leaves the tracked bytes and does not shrink the tree.
3. **MED** — `tools/mori-unlanded-check.py:15` (scope statement) and the selftest arm
   `outside_scope_and_scratch_not_listed` at `:132-134` must change with defect 1; otherwise the class
   the round is fixing stays outside the pre-report gate.
4. **MED** — The committed host receipt contains a MESSAGE-field filter:
   `corpus/evidence/sources-r49/host-journal-reach.txt:92` runs
   `journalctl -b 0 -u systemd-journald --no-pager -q -g 'Journal .* is .*max'`, while S351's flip
   text (`corpus/SOURCES.md:248`) requires "no MESSAGE grep". Either the superseding row's `teaches`
   scopes that exclusion to the evidence the row rests on, or the quoted evidence must not include
   that line.
5. **LOW** — The new journalctl row adds a third registry entry on one URL (with `S351` and `S470`,
   `corpus/SOURCES.md:248-249`), so the round-end census should read 21 `W04` warnings, not 20; if it
   does not, the row is not in the registry.
6. **LOW** — `.ufo/waves/round-40/scratch/` holds 7 untracked `mori-conform-selftest-*` directories:
   a residue class outside both the closure's 114 count and the contract's fix scope.
7. **LOW** — At 2026-10-25T21:46-03:00 the round's own wave files (`.ufo/waves/round-49/w1-spec.json`,
   `w1-dispatch.json`, `w1.ready`, `w1-validate.err`, `w1/`) are untracked while wave 1 runs; they are
   the round-48 M1 class and must land before the report, with the draft entry's "reports on disk"
   figure filled from disk, not from the dispatch.
8. **LOW** — The draft's scratch-count figure (147 round-48-class prefixes at 21:46) differs from the
   closure's 114 because seats keep creating scratch directories; the draft states both numbers with
   their moment so a later closure does not read a stale figure.

## Report

`.ufo/waves/round-49/w1/Mo49ScribeLogEntry.md`
