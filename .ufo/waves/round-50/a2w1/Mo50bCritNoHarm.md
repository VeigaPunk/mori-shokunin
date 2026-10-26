# Mo50bCritNoHarm — no-harm audit of the landed round-50 data (a2w1)

Seat: critic (no-harm). Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Range audited: `7197160b927f04db294c9553fb48fadcc7a3f4e3` → `487941b9395e89678af0053cc443cdb49cdee6e3`
(freeze `950e99be…`, considerthese `649e14cf…`, salvage `9b8562a371dc916fdc0fc686619ea1e271a3e118`, data `487941b9…`).
Scratch `/fast/scratch/hyaku/mori-r50/Mo50bCritNoHarm/` (one `git archive`, one fixture repo, `TMPDIR` inside it),
removed at end. No tool installed or upgraded; no pacman transaction; no repo/index/jj mutation; no host journal,
kernel-log or cgroup read. Fleet `MANIFEST.json` read with `git cat-file`/`git show` only from
`e014499613f63f8a467821219b0296121119ca53`.

## Verdict summary

coverage **not harmed** · operability **not harmed** · depth **not harmed as a regression, F1 open in the increment**
· freshness **not harmed** · calibration **not harmed** · adjacency **not harmed**. No HIGH finding; one MED (F1,
entry wording, verified fix keeps `C2=met`) and four LOW. The salvage commit `9b8562a3` moved no axis surface.

## What the round changed (bytes)

`git -C … diff --stat 7197160b 487941b9` → `58 files changed, 15507 insertions(+), 5 deletions(-)`.

- The 5 removed lines are 4 rewrites of `SCORECARD.md` `## Axes` rows (coverage, operability, depth, calibration)
  and 1 rewrite of the `SHONEN.md` pin box. Every rewritten row is present at R; the two untouched Axes rows
  (freshness, adjacency) and the three untouched SHONEN boxes appear in the diff as context only.
- `git diff --diff-filter=D --name-only 7197160b 487941b9` → empty. No file deleted anywhere in the range.
- `git diff --name-only 7197160b 487941b9 | grep -E '^(tools/|SKILL\.md|PROVINCE\.md|corpus/QUALITY\.md|LOG\.md|README\.md|corpus/README\.md)'`
  → empty. No tool, no SKILL/PROVINCE/QUALITY, no LOG, no README touched.
- Score column of all six Axes rows unchanged (6 / 7 / 5 / 5 / 5 / 6).
- The data commit `487941b9` itself touches 6 paths: `SCORECARD.md`, `SHONEN.md`, `corpus/SOURCES.md`, and
  `assimilation/a2/{append-block.md,live-sha-L1.txt,mirror-validate.txt}`. `corpus/knowledge/oom-memcg-stat-r50.md`
  and `corpus/evidence/sources-r50/*` came in with the salvage commit and were **not** re-edited by the data commit.

Frozen bytes never moved after scoring — sha256 prefix of each frozen file at freeze / salvage / landed / worktree:

```
contract.md                 freeze=8290c6d477adb603 salv=8290c6d477adb603 land=8290c6d477adb603 wt=8290c6d477adb603
count-c1.py                 freeze=2d5c3ee53198124e salv=2d5c3ee53198124e land=2d5c3ee53198124e wt=2d5c3ee53198124e
count-c2.py                 freeze=533c8403b90e650c salv=533c8403b90e650c land=533c8403b90e650c wt=533c8403b90e650c
controls/c1-controls.py     freeze=c7b49dae9043ceda salv=c7b49dae9043ceda land=c7b49dae9043ceda wt=c7b49dae9043ceda
controls/c2-controls.py     freeze=641eecc505595504 salv=641eecc505595504 land=641eecc505595504 wt=641eecc505595504
```

## Instruments re-run at R (not taken from the L1's message)

```
python3 .ufo/waves/round-50/count-c1.py 487941b9… → C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0
  manifest=a94551c5bc8d rev=487941b9…                     rc=0
python3 .ufo/waves/round-50/count-c2.py 487941b9… → C2=met claims=22 located=22 quote_missing=0 bad_rows=0
  sources=3 source_rows=ok pins=ok provenance=ok          rc=0
```

C1 prints per-axis `expect=round_47/47/49/28/49/19_improved got=ok state=ok` for coverage, operability, depth,
freshness, calibration, adjacency — the same six N* I computed independently from the fleet MANIFEST (below), so the
Axes data agrees with an independently derived answer, not merely with the counter's own echo.

### Revision note

Every line citation below is for **R = `487941b9`** (`git show 487941b9:<path>`). At the end of this audit HEAD is
`4548a34dc8b4072abaa4335c1f54a9efcfcc314a` (the a2w1 spec commit) and the working tree carries another seat's
**uncommitted** edits to `corpus/knowledge/oom-memcg-stat-r50.md`, `SCORECARD.md`, `SHONEN.md`, `corpus/SOURCES.md`
(`git diff 487941b9 -- …` = 56 insertions, 28 deletions over those four paths). Those edits already reword row 19 to
"The summary header and the oom-kill context line print only when the rate limit allows, so a burst of kills can
leave Killed process lines without them." — i.e. F1(a) is being fixed in flight — while the intro sentence on
`:15` is unchanged there, so F1(b) is still open. I scored nothing against that uncommitted tree.

## Axis verdicts

### coverage — not harmed

- No surface, roster or row removed: no deleted file in the range; `corpus/SOURCES.md` gained exactly 3 rows.
- Append-only gate at R, round-scoped:
  `python3 tools/mori-sources-appendonly.py 487941b9… --repo <lane> --round-base 7197160b…` →
  `appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179…S193] deleted=[] …
  round_changed=[]` rc 0. The same command at the entering tip prints the **identical** 18 ids and
  `deleted=[] round_changed=[]` → the violations are pre-existing (round ≤49), not introduced here.
- New rows are well formed: `S489`, `S490`, `S491` each 11 cells under the 11-column header (`corpus/SOURCES.md:7`).
- Coverage cell: N* = 47 matches MANIFEST; the evidence pointer it adds is `round-47-verifier-spotcheck.md:68`
  = `| coverage | improved | FR13 held as a full event set plus lifecycle; … |` (present, says what the cell says).
- Residual (integration debt, not a regression): **F2** below.

### operability — not harmed

- `tools/` untouched (above), so no selftest arm changed; `SKILL.md` untouched.
- Both pinned instruments re-run at R from a `git archive` of `487941b9` in scratch:
  `PIN_CHECK_SELFTEST pass=114 fail=0` (rc 0), `UNLANDED_SELFTEST pass=17 fail=0` (rc 0) — i.e. the new pins are
  current, not stale. Receipts carry the same lines plus `exit=0`
  (`.ufo/waves/round-50/evidence/selftests/mori-pin-check.txt`, `…/mori-unlanded-check.txt`).
- The append-only gate accepting the new rows means the registry edit is legal by rule 2 (only appended, no
  in-place cell rewrite).
- Residual: **F4** (receipt header names the freeze rev, not the tip; substance unchanged because no tool changed).

### depth — not harmed as a regression; one fixable wording defect in the increment

- The entry is new: 22 claim rows, exactly 3 cells each, no duplicate claim (case/whitespace folded), shortest
  claim 16 words, all three sources used, all quotes backticked single spans.
- Claims re-opened against the frozen copies: usage line order/units (`memcontrol.c.v7.2:1805-1812`), the
  v2 `failcnt` = MEMCG_MAX (`:1799-1805`), formatter identity (`:1751`, `memory_stat_show` `:4905-4919`),
  `global_oom`/`task_memcg` labels (`:1774-1782`), group-kill line (`memcontrol.c.v7.2:1996-1998`, docs
  `oom_group_kill`), Killed-process fields (`oom_kill.c.v7.2:945-951`), `__show_mem` vs block (`:465-471`),
  Tasks-state pages (`:424-425`) — all supported.
- **F1** (MED) — one claim row and the intro's detection sentence overstate two things; details and a verified
  correction below. This is an entry-wording defect in the increment, not a removal of prior depth.

### freshness — not harmed

- The freshness row is untouched and still leads with `round 28` (N* = 28 per MANIFEST); no `recheck:` cell was
  weakened anywhere (`round_changed=[]` above).
- New sources are dated this round and the dating checks out: entry `verified-at: 2026-10-26`,
  `recheck: 90d`, and the three sha256 in that line are the committed copies:
  `sha256sum corpus/evidence/sources-r50/*` → `2d716cb7…`, `8a28e0bc…`, `452f1348…` = `freeze-sha256.txt:1-3` =
  the sha256 written in rows S489/S490/S491.
- Live fetch receipt `assimilation/a2/live-sha-L1.txt` shows the same three digests at
  `2026-10-26T09:26:36-03:00`, i.e. the "opened 2026-10-26" claim is backed by an observation, not by prose.

### calibration — not harmed (the round's high-risk axis, and it holds)

Independent derivation from the fleet record at the pinned revision (no counter involved):
`git show e0144996…:MANIFEST.json`, then, over mori entries with `verdict == admitted` and `lane_round <= 49`, the
highest `lane_round` whose `verdicts[axis]` is `improved`/`harmed`:

```
coverage (47, improved)   operability (47, improved)   depth (49, improved)
freshness (28, improved)  calibration (49, improved)   adjacency (19, improved)
```

That is exactly what the six Last-change cells say (`round 47 / 47 / 49 / 28 / 49 / 19`). Second, independent
record: the lane's own closures agree with MANIFEST for the four newly cited rounds — `round-47-verifier-spotcheck.md:67`
(operability improved, `tools/mori-pin-check.py`), `:68` (coverage improved, FR13 event set), `round-49-…:75`
(calibration 5 improved, "C1 verified; no score change claimed"), `:76` (depth 5 improved, "C2 re-measured 21/21").
Both cited files exist at R.

No evidence was dropped while rewriting the cells: backticked pointers per rewritten row, old vs new —

```
coverage     dropped []  added [round-47-verifier-spotcheck.md:68]
operability  dropped []  added [round-47-verifier-spotcheck.md:67, tools/mori-pin-check.py]
depth        dropped []  added [round-49-verifier-spotcheck.md:76]
calibration  dropped []  added [round-49-verifier-spotcheck.md:75]
```

Preserved-and-still-true citations re-read at R: `round-24-…:68` ("Score 5 → 5"), `round-24-…:88`
("Score 6 → 6"), `round-25-…:124`, `round-31-…:154`, `round-31-…:155`. The added correction paragraph's
history claim ("they named rounds 26, 31, 31 and 25") is true of the entering bytes (verified from the removed
lines). SHONEN: 4 `- [~]` boxes, 2 tally pins, no other tally token (`grep -oE '\([0-9]+/[0-9]+\)|pass=[0-9]+ fail=[0-9]+'`
→ `(114/114)`, `(17/17)` only), and both equal the live re-measurement above.

### adjacency — not harmed

- Every changed path is inside the lane repo; no sibling lane, no `shokuknow`, no fleet file written. The only
  fleet bytes read are `MANIFEST.json` at the pinned revision, read-only.
- The entry's `## Boundaries` keeps configuration (`memory.max`, `memory.oom.group`, `oom_score_adj`) in tsukuroi
  and states no host block was read; no `journalctl`, no kernel MESSAGE grep, no cgroup write appears in the new
  files (the only command in the new data is the `curl | sha256sum` recheck line).
- The known cross-document overlap is disclosed rather than absorbed: S491's row says "same URL as S003 and S476
  with a different scope", and the census receipt `assimilation/a2/mirror-validate.txt` lists
  `W04 S491 duplicate url …/mm/oom_kill.c across scopes` (a warning, as the contract says). A second, *undisclosed*
  near-duplicate exists at a different URL (F3).

## Attempt-1 salvage commit `9b8562a3`

`git diff --stat 7197160b 9b8562a3` → 52 files, all added inside `.ufo/waves/round-50/`, `corpus/knowledge/`,
`corpus/evidence/sources-r50/`, `considerthese/`, plus the late round-49 seat report
`.ufo/waves/round-49/w1/Mo49ExecCounterTiming.md`. Specifically:

- it does **not** touch `SCORECARD.md`, `SHONEN.md`, `corpus/SOURCES.md`, `SKILL.md`, `PROVINCE.md`, `tools/`,
  `LOG.md` or either README — so it cannot have moved an axis, a pin, a row or a tool selftest;
- its three source copies are byte-identical to the freeze list (`sha256sum` above = `freeze-sha256.txt:1-3`), so
  the salvage did not substitute different bytes for the frozen sources;
- the entry it brought in is byte-identical to the entry scored at R (`487941b9` does not touch that path);
- the late round-49 report is the one the contract's round-49 carrier 5 asks to be committed as inherited.

One consequence worth naming, not a harm at R (**F5**): at `9b8562a3` the entry cites S489–S491 while those registry
rows do not exist yet, so an evaluation pinned to that intermediate revision would fail `source_rows`. At R the rows
exist and `count-c2.py` prints `source_rows=ok`.

## Findings

### F1 — MED — `487941b9:corpus/knowledge/oom-memcg-stat-r50.md:15` (intro rule) and `:39` (claim row 19)

Two statements are weaker than the frozen copy supports:

1. `:39` — "The oom-kill summary and stats block are rate-limited while the victim line is not, so a burst of kills
   can print victims without a block." Its own quote
   (`if (__ratelimit(&oom_rs)) { dump_header(oc); dump_oom_victim(oc, victim); }`) shows **two** prints inside the
   guard, one of which (`dump_oom_victim`, `oom_kill.c.v7.2:444-454`) is the line that names the victim
   (`task=<comm>,pid=,uid=`). The claim is true only for the `Killed process` line (`pr_err` at
   `oom_kill.c.v7.2:945`, reached from `:1042`, outside the guard at `:1030-1033`) — which the entry's title/intro
   does bind as "the victim line" (`:11-12`), so the claim is defensible, but the row's quote alone reads as a
   refutation. Sibling seats split on this: `Mo50bRevRowsOomA.md:99` SUPPORTED, `Mo50bSimpEntry.md:215-219` MED
   (conflation), `Mo50bRevLimitsHonesty.md:411` "no defect, do not fix". Naming the line in the claim settles it
   without touching the quote or the frozen predicate.
2. `:15` — "a stats block means the kill was charged to a scope." `dump_header` is also called **unguarded** on two
   paths where no kill happens: `oom_kill.c.v7.2:1075` (`check_panic_on_oom`, before `panic()`; reachable for a
   memcg OOM when `sysctl_panic_on_oom = 2`, because the `constraint != CONSTRAINT_NONE` early return is skipped in
   mode 2) and `:1158` (`out_of_memory` after `select_bad_process` finds nothing; for a memcg OOM the function
   returns instead of panicking). On both, a `Memory cgroup stats` block can print with **no** victim line at all.
   The sound direction is "a stats block means the OOM context was a scoped memcg OOM", not "…means the kill was
   charged". `Mo50bRevEntryHeader.md:179-186` verified the block's provenance and accepted the sentence; it cites
   `:1158` only inside a parenthetical and does not draw the no-kill consequence; `Mo50bRevRowsOomA.md:117` raises
   `:1158` as LOW for row 19 only; no seat cites the `:1075` panic path.

Smallest safe correction (data only; counters untouched). The rewording below was committed in a throwaway fixture
repo under the scratch dir and scored with the frozen counter:

```
python3 .ufo/waves/round-50/count-c2.py <fixture-rev> --repo <fixture>  →
C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok   rc=0
```

so it costs the claim nothing. Row 19 (claim cell only):

```
| On the kill path the ratelimit guard covers dump_header and the `oom-kill:` context line, while the `Killed process` line is an unguarded pr_err, so a burst of kills can print victim lines without a block. | S491 | `if (__ratelimit(&oom_rs)) { dump_header(oc); dump_oom_victim(oc, victim); }` |
```

Intro, the sentence on `:15`:

```
That difference is the detection rule this entry serves: a stats block means the OOM context was a scoped memcg
OOM — the block also prints on the two non-kill paths (`check_panic_on_oom` before a panic, and `out_of_memory`
when no process is selected), so a block without a victim line is possible and is not evidence that a victim
record was lost.
```

Cheaper alternative if the L1 wants zero claim-cell churn: add only the second, intro-level sentence, which removes
the false expectation without touching the claim table at all.

### F2 — LOW — `corpus/README.md` (no Round-50 coverage-addition row)

The new entry maps `coverage-map: FR1`, but the corpus coverage index was not updated: round 47/48/49 each appended a
section (`corpus/README.md:677` is round-49's) and the FR1 row at `corpus/README.md:341` still lists only
`kernel-oom-line-attribution-r12.md` / `audit-r11.md`. Precedent is mixed (the r46 entry is also unlisted; 33 of 59
knowledge files appear in the map), so this is integration debt, not a coverage regression — the entry itself is
reachable through `corpus/SOURCES.md` `used-by`. The L1 should append the row before closure.

### F3 — LOW — `corpus/SOURCES.md:268` (S489) vs `:8` (S002)

S489 is the `/7.2/` copy of the same document as S002 (unversioned page) and its scope cell re-covers
"memory.events fields", which S002 already governs; unlike S490 ("not the master-commit path labels of S004") and
S491 ("same URL as S003 and S476 with a different scope") it does not disclaim S002. The W04 duplicate-URL detector
cannot see this because the URL paths differ (only S491 appears in the W04 list). One clause in the scope cell —
"not the unversioned page's events rows (S002)" — closes it.

### F4 — LOW — `…/evidence/selftests/mori-pin-check.txt:1`, `…/mori-unlanded-check.txt:1`

Both receipts are stamped `git archive of 950e99be…` (attempt-1 freeze), while the data commit message says the pins
land "with re-verified receipts". Substance is unaffected — no `tools/` file changed in the round and my re-run at R
prints the same `pass=114 fail=0` / `pass=17 fail=0` — but the label invites a reader to think the receipts were
produced at the tip. Either re-stamp at R or word the commit message as "receipts from the freeze rev, re-run at the
tip".

### F5 — LOW — `9b8562a3` (salvage) intermediate state

The entry lands one commit before its S489–S491 rows, so that intermediate revision carries citations to rows that do
not exist there (`C2 … failed=source_rows` if scored). Resolved at R; noted so a later reviewer does not read the
salvage commit as scored evidence.

### F6 — INFO (no action) — quote multiplicity in the HTML copy

The row quoting `Don’t rely on items remaining in a fixed position; …` is located, but that sentence occurs **twice**
in the normalised `cgroup-v2.7.2.html` (`All memory amounts are in bytes.` occurs 3×). The counter's located-quote
test does not require uniqueness in the copy (name limit), and no claim depends on the position — recorded so the
L1 does not mistake it for a uniqueness violation.

## Fixable defect vs tradeoff the judge must accept

- **Fixable now, counter-neutral:** F1 (wording, verified `C2=met`), F3 (one clause), F2 (README row), F4 (label).
- **Tradeoffs the canonical judge must reject as fixes this round** (all are named limits in the contract, not
  defects): quote-location-without-entailment, the 3-new-words floor, the MANIFEST being fleet-written and trusted
  by C1, the Last-change convention itself, the SHONEN-only hidden scan, and the three committed source copies
  (356 KiB) being judged by pinned sha256 rather than by a re-fetch. I found no place where the landed data *leans
  on* one of these limits to claim more than the evidence shows: every newly cited lesson line exists, every sha256
  matches, every pin equals a live measurement.

## Named limits of this review

- I did not re-derive the fleet MANIFEST's own closure verdicts; I checked that MANIFEST and the lane's closure
  lessons agree for the four newly cited rounds, which is as far as the fleet record can be cross-checked from here.
- The block-without-kill path (F1) is established from the frozen code, not from a host observation — no host OOM
  block was read (lane rule), so "reachable" means reachable per the code and the `panic_on_oom` gate.
- UNVERIFIED: whether any caller outside the two frozen copies prints `Memory cgroup stats for` (the same exclusion
  `Mo50bRevEntryHeader.md` names for the exported `mem_cgroup_print_oom_meminfo`).
