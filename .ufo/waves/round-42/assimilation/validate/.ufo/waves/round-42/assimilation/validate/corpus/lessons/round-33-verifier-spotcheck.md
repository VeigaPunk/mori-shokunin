author: hyaku closure (non-author integrator, @m_opus)

# mori round 33 — verifier spot-check (non-author closure)

Lane-round mori 33, attempt 1 (L1 `MoriR33`). Base `7d382043016e8854e3be2ee523a095b409c3d8a1`, landed tip
`89791013f5063644f1c79998ec60d09906845ec9`, fleet report `.ufo/reports/round-33/mori.md` (`80c1542`). Closure run
2026-10-23 (from about 03:05Z) by a fresh hyaku closure session that did not author the round. Eight read-only seats
were dispatched: ReJudgeRows01to07, ReJudgeRows08to14, A1TimingCheck, RepairCheckA, RepairCheckB, DiscernmentSpot,
ConformancePromptHarm (all reviewer) and GlossaryControlCritic (critic). GlossaryControlCritic died on spawn with its
provider's error `Cloud Code Assist API error (429): ... Individual quota reached` (2.1 s) and returned nothing; the
closure judged that question itself (§3.2). No lane counter or gate was executed: the C1 counters are evidence-verified
only. The closure did its own plain re-measure over committed bytes. No tool was installed or updated by the closure or
reported by any seat.

Driver digest (copied from `.ufo/watchdog.log`):
`2026-10-22T23:22:21-03:00 launch mori round=33 pgid=207913 driver=hyaku-inline attempt=1`;
`2026-10-23T00:17:35-03:00 complete mori round=33; hyaku-inline attempt=1`.

## 1. Step-1 conformance

- Report: `git log --format='%an %H' -- .ufo/reports/round-33/mori.md` → `mori-shokunin 80c1542073dbf7d33a806d72725d186de3f2cb26`
  (00:17:20 −03), 30 s after the lane tip (00:16:50 −03). Required sections are present and in order: Work performed :6,
  Landed changes :28, Before → after :40, Sources & frontier :50, Trend verdicts :69, SHONEN :77. The extra `Gate` and
  `Mistakes` sections are allowed. `SHONEN` has 4 lines for the 4 boxes in `SHONEN.md:5-8`, all `[~]`, and no `[x]`.
- Cited commits: `27969134 fdf4371f 62db24c0 ab8f4cfe 7a0234c2 a193627c 89791013` are all `commit` objects, and
  `git merge-base --is-ancestor <h> master` holds for each (`anc-ok` ×7).
- Push and leftovers: `jj-lane.sh state` → `branch=master local=8979101… remote=8979101… ahead=0 behind=0 head=detached
  tracked=0 untracked=2`. `git ls-remote origin refs/heads/master` → `89791013…`. `git status --porcelain` shows only
  `?? .scratch/` (pre-round) and `?? .ufo/waves/round-33/__pycache__/` (Python bytecode cache). Both are named here and
  not counted as round work.
- Prompt: ConformancePromptHarm rendered `templates/round-prompt.md` for mori r33 and diffed it against prompt lines
  1–140. The only difference is the correctly resolved `<mori-repo>` placeholder on line 1, so all round-level and
  child-lane items are carried. The prompt quotes no L2 route map, and §3 defers to host routing, which is consistent
  with `MISSION.md:57-65`. §6 is the hyaku addendum.
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → the same 12 `W04` duplicate-url
  lines the report names, then `mori ok …/corpus/SOURCES.md`, `EXIT=0`.
- Timestamps: the `27969134` author date (23:21:08) is before the launch line (23:22:21). This is a jj artifact, not
  pre-dated evidence. The working-copy change was created when `7d382043` landed at 23:21:08, jj keeps the author time
  across rewrites, and the content landed at committer time 23:28:27. Round 31 shows the same pattern (`2124cbcd`).
  MoriR33's session started at 02:22:30Z (A1TimingCheck).
- Conformance defects (status-neutral; routed in §8): receipt time labels `evidence/c1-controls.txt:1` ("dispatched
  02:38Z"; the actual C0 dispatch was 02:30:05Z) and `evidence/parity-freeze.txt:1` ("02:3xZ"; the actual run was
  02:28:27Z). Report :52-53 and lesson :79 say the six SOURCES cells changed only by gaining `lane rule:`, but S062
  ("between JSON tokens") and S064 ("once" moved) also changed words, as lesson :85-93 itself records.

Status: `ok`. The report is real and cites checkable commits.

## 2. Amendment A1 timing (closure-confirmed)

A1 (`fdf4371f`, committed 23:39:02 −03 = 02:39:02Z) landed **after every C0 control seat scored and before any data
seat existed** (A1TimingCheck, from the MoriR33 and seat transcripts and the trees):
- C0 was dispatched at 02:30:05.953Z. The last C0 report writes were at 02:35:03–02:37:53Z and the last final answers
  by 02:38:01.877Z. The Part B re-score under `count-c1-a1.py` ran at 02:38:20–02:38:35Z.
- Wave 1 was dispatched at 02:39:22.626Z, and its first seat transcript started at 02:39:22.761Z. Wave 2 started at
  02:56:49Z and the judges at 03:09:26Z. `wave1-spec/run/dispatch.json` cite the full `fdf4371f…` hash.
- `git ls-tree -r --name-only fdf4371f` contains no entry, no `lessons/round-33.md`, no `sources-r33`, no `w1`/`w2`/`judge`
  files. `git diff --stat 7d382043 fdf4371f -- corpus SKILL.md` is empty.
- `w1/swarm-registry.json` `createdAt` 02:32:40Z is from a plan-only run in which every agent id was empty. The spawn
  came after A1.
- A1 only adds conditions. `diff count-c1.py count-c1-a1.py`: `canon` row equality, distinct observations,
  6-word reading/quote overlap, and `or spans_bad` in the judge failure. Each matches the P-C1-A1 sentence at
  `contract.md:119-123`. Nothing was removed.
- P-C1 (`contract.md:26-42`) and R-J (`:44-50`) hash the same at `27969134` and `89791013`, and `git diff --numstat
  27969134 89791013 -- contract.md` is `33 0` (append only). `count-c1.py` is blob `b225074b` at every commit.

Ruling: addendum §9 says "fix it before data", and A1 did exactly that. The rule "a rule changed after any seat has
scored is not the claim's rule" refers to the claim's data. C0 seats are the controls §9 orders to be built and scored
before freezing. **The claim is judged on P-C1-A1.**

## 3. Claims

### C1 — depth: sourced decision table on reading `/proc/diskstats` as a write rate (FR6) — **not verified**

#### 3.1 Re-measure: the predicate holds honestly at the tip (re-measured, plus evidence-verified)

Plain measurements over committed bytes:
- `git show 89791013:corpus/knowledge/disk-write-rate-r33.md | grep -cE '^\| [0-9]+ \|'` → `14`.
- Cited ids ≥ S180: `S180 … S190` (11).
- `git show <rev>:corpus/SOURCES.md | grep -c '^| S[0-9]'` → `179` at `7d382043`, `190` at `89791013`.
- `grep -cE '^row [0-9]+: supported' judge/JudgeC1Rows.md` → `10`.
- `sha256sum` of the entry at `89791013` → `eaeb1100…c764`, which equals `judged-sha256:` (`JudgeC1Rows.md:4`). The entry
  is byte-identical at `ab8f4cfe`, `a193627c` and `89791013`.
- `grep -cF` of R-J's first clause → 1 in `judge/dispatch.json` and 1 in `JudgeC1Rows.md`.
- SKILL lines naming `Round33` and the entry: 7 lines; 6 of them have ≥12 words (ConformancePromptHarm, `SKILL.md:815-820`).

Evidence-verified receipts: `evidence/c1-before.txt` (`7d382043`: `entry=absent C1=unmet exit=1`) and
`evidence/c1-after.txt` (`a193627c`: `rows=14 … new_ids=11 … gates_ok=11/11 copies_ok=11/11 fetch_ok=11/11 …
supported=10 supported_new=10 spans_bad=[] unsupported=[3, 6, 7, 13] skill_rows=6 C1=met exit=0`). The frozen
`count-c1.py` is also `met`. All of these match the report's values.

Independent re-judgement under R-J (the contract's declared residual, `contract.md:73-75`, puts receipt integrity on
"the closure's own re-judgement"): **14 of 14 row verdicts agree with JudgeC1Rows.** Rows 1, 2, 4, 5, 8, 9, 10, 11, 12
and 14 are supported; rows 3, 6, 7 and 13 are unsupported.
- Row 3: the line printing `part0` is only in S182:1370,1472, which the row does not cite.
- Row 6: "approximate" needs S181:78-80, which is not cited.
- Row 7: the procfs/sysfs field-11 identity needs S181:22 or S182:1392, neither cited.
- Row 13: the observation is a fact about `tools/mori-census.sh`; S181 has no census, uptime or average text.
- Every supported span has ≥6 words and is located in a copy its row cites (rows 8–14: 14, 8, 12, 13, 7, 10 words).

The re-judges also classified each verdict cell. Rows 8 (field-count layout) and 12 (one parser for both files) are
definition or restatement verdicts. The other eight supported rows carry a write-rate decision.

#### 3.2 The post-data control CtlGlossaryA1 falls within the frozen predicate — §9 fails the claim

What the control is: `w2/CtlGlossaryA1.md`, sandbox `/fast/scratch/hyaku/mori-r33/CtlGlossaryA1/clone`, commit
`04c02aeb` (the closure read its bytes). It starts from the data revision `62db24c0` and replaces the 14 decision rows
with 11 definitions, one per S180–S190 (for example "The `sectors` member is an array of `unsigned long` values."). Every
verdict cell is `Note it.`. It adds a receipt that quotes R-J verbatim, binds `judged-sha256: abfc008e…`, and gives a
located span per row. The output, run under `count-c1-a1.py`, is `rows=11 … supported=11 supported_new=11 spans_bad=[]
… C1=met` with exit 0. The pristine and restored states print `C1=unmet` with `judge=absent`.

Closure ruling: **the control is inside what P-C1-A1 claims, so C1 does not verify.**
1. *Not the declared residual.* The contract leaves uncounted only a forged receipt "of the same shape"
   (`contract.md:73-75`; A1's CtlJunkOffTopic). This receipt is not forged. The closure read the 11 glossary rows and
   their spans (for example row 4 at `S183.src:8-11`, row 9 at `S188.src:72`, row 11 at `S190.src:1151-1152`), and each
   definition is stated by its located quote. "Note it." follows "without any further fact". An independent honest
   judge applying R-J would therefore mark all 11 supported. The control meets P-C1-A1 on its honest reading, not by
   exploiting the residual.
2. *It skips exactly the claimed work.* The declared surface is "a sourced decision table on reading `/proc/diskstats`
   … as a write rate" (`contract.md:16`; report :8-9). The axis is depth, "decision tables with real thresholds"
   (`AXES.md:11`). The sources, Gate rows and copies the control reuses are the frontier step's sourcing duty (prompt
   §2b item 4), not the depth move. With those in place, the control is one cheap edit: 11 one-line definitions and an
   honest receipt. It contains no decision. That is the §9 control "that skips the claimed work"
   (`.ufo/prompts/mori-round-33.md:352-356`). It met the target, which means "the counter or target is wrong".
3. *Data had already been taken.* Per §9, a frozen target that a cheap control meets after data has failed; it cannot
   be amended (`:357-360`). Precedents: kaidoku r29 C1 and kake r34. The lane reported this correctly and did not amend
   (report :46-48, lesson :185-187).
4. *Pre-data control set.* None of the nine pre-data controls (`contract.md:66-71`) was a no-decision control, so the
   gap was knowable before freezing. The control list tested sourcing and judging, not the claimed depth.
5. *Supporting observation, not the basis of the ruling.* Under the re-judge's classification, 8 supported rows carry
   decisions. That is below the floor of 10 that the claim's prose implies.

The strongest counter-argument: all 14 real verdicts carry a choice (CtlGlossaryA1's own row table). The entry is real,
sourced FR6 knowledge, and 10/14 rows survive an outside re-judgement. This is true and is credited under the trends
(§6). But the claim was declared measured, and its counter cannot tell this entry from a decision-free glossary. The
depth move is therefore not measured. Verdict for C1: **not verified (honest stop)**. No exploratory claim was
declared, so `unprovable-but-better` is not available for C1.

### Round-32 repair (routed by the r32 closure §8; not a claim) — **verified with two consistency defects**

RepairCheckA covered S058, S117 and S128; RepairCheckB covered S149 and S137. Both worked clause by clause from the
base-tip teaches/source cells and the committed copies (`recheck-r33/SHA256SUMS` passes `sha256sum -c`).

| row | not-current | pop / other named page / unsupported | closure vs lane §1 |
|---|---|---|---|
| S058 | agree | 3 / 3 / 3 | agree once the appended Judges correction (:208-210) is counted. The `--reverse --topo-order` "ancestors first" derivation is unsupported, and the §1 table cell omits it |
| S117 | agree | 0 / 3 / 6 | agree. The releases feed was never committed (`git ls-tree` shows 9 S117 copies). The §1 preamble :50-51 overstates the check for this row |
| S128 | agree | 5 / 1 / 4 | agree. "different contracts" is only in the last column |
| S149 | agree | 3 / 1 / 10 | agree. The lane's reading that a row id in the source cell does not name that row's pages is defensible under R-R ("the row's own source cell names"). It decides only column 4 vs 5, not currency |
| S137 | agree | 0 / 1 / 6 | the table :62 still counts `S137-main-750a.src:260` as support |

- **The repair judge's S137 disagreement: the judge is right.** `S137-main-750a.src:259-261` is a bare `case 'k'`
  printing "Option -k is ignored since earlyoom v1.2". The kernel-OOM option is a separate option,
  `LONG_OPT_USE_KERNEL_OOM` (`:201`, `:315-317`, `:352-354`). Nothing on S137's named pages ties `-k` to that option. The
  only committed link is `S117-README-v1.9.0.src:383`, a page S137 does not name.
- **Append-only: yes.** `git diff --numstat 7d382043 89791013 -- corpus/lessons/round-32.md` → `10 0`. The S058, S117
  and S128 SOURCES rows hash the same at base and tip. `recheck-r32/` is unchanged. The round-32 "finding 1" citation
  correction is accurate on every point checked.
- **Defects:** the §1 table (byte-unchanged since `62db24c0`) and the appended Judges prose (:205-211) contradict each
  other on S137's `:260` pointer and the omitted clauses, and §1 has no forward pointer. Line :209 says "those six
  clauses" but lists five; the receipt says "5 … plus 1 misfiled" (`JudgeRepairR32.md:76-77`). R-R is quoted word for
  word in the receipt (`JudgeRepairR32.md:5`). The receipt's lesson sha `470b6e3b…` equals the lesson at `ab8f4cfe`.
- QUALITY 97 (`corpus/QUALITY.md:701-711`) can fail: `grep -cF 'Reject (disagree) a row when'` returns 0 in
  `round-32/judge/JudgeRecheck.md` and 1 in `round-32/r1-dispatch.json`. One caveat: round 32's frozen rule lived in
  the dispatch, not in the contract.

## 4. Per-axis verdicts and no-harm

- `git diff 7d382043 89791013 -- SCORECARD.md` → `+27 −0`. It appends a Round 33 declaration and a measured-outcome
  table, changes no score, and rewrites no row.
- `git diff --stat 7d382043 89791013` → 139 files, 36187 insertions, 8 deletions. The 8 deleted lines are:
  - 6 in `corpus/SOURCES.md` (S041, S044, S051, S062, S064, S069). Applying lesson §3's old→new strings to the base
    rows reproduces the tip rows exactly, and the status, opened, recheck and used-by cells are unchanged.
  - 2 in `corpus/README.md` (FR5 and FR6). The old text is kept as a prefix and a Round 33 sentence is appended.
- `PROVINCE.md` and `SHONEN.md` are unchanged. `LOG.md` is `+21 −0`.

| axis | verdict | reason |
|---|---|---|
| depth | unprovable | C1's counter is met by a decision-free glossary (§3.2), so the move is not measured. The entry's content is real (10/14 rows re-judged supported). The score stays 5 under the contract's score policy |
| coverage | unchanged | no claim. FR6 was entered as knowledge, but no surface or tool changed |
| operability | unchanged | no tool change; the item-6 retirement registers debt |
| freshness | unchanged | the r32 repair marks five rows not current (routed work, not a claim) |
| calibration | unchanged | no claim |
| adjacency | unchanged | PROVINCE is unchanged; the dm double count is kept as frontier and is not sourced |

No axis is harmed.

## 5. Discernment spot-check (`corpus/lessons/round-33.md` `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S185 `block/blk-mq.c` v7.2 | admit, A, mined | live `curl -sL https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c` → sha256 `7483f173…8c11` = Gate = committed copy (136798 B) | agree | quotes at :856/:858/:862 are contiguous, 8, 5 and 5 words; this is the primary source for row 2's `RQF_IO_STAT` completion clause |
| S188 commit `b6866318….patch` | admit, A, mined | live fetch → `a844836a…8d89` = Gate = copy (8897 B) | agree | 4 quotes contiguous (10, 10, 13, 11 words); this is the only source for row 11's "zero-size barrier writes"; v7.2 `blk-flush.c:126-130` still counts flushes on `part0` only |
| SrcSectorSize quote "The size of one sector is 512 = 2**9 bytes." | reject (quote replaced) | committed `S186.src:26-27` | agree | line 27 starts with ` * bytes.`, so with whitespace collapsed the text reads "512 = 2**9 * bytes."; the quote is not contiguous. The replacement at :26 is contiguous |
| SrcDmCore `drivers/md/dm.c` v7.2 | reject (opened, not registered) | live fetch → `b01ff2d6285e…` (matches the lesson's prefix) | agree | `dm.c:506-516` accounts `io->orig_bio` on the dm device through `bdev_start/end_io_acct`. No line says the backing device counts the clone again, so the double count stays unsourced |

- SOURCES row check: rows S185 (`SOURCES.md:191`) and S187 (`:193`) at `89791013` hold no quoted text. Their anchors
  point to the contiguous Gate quotes (S187: 7, 13, 14 and 9 words, copy sha `0f2ffdc7…` = Gate).
- All 38 Gate quotes for S180–S190 are 3–25 words, contiguous at their locators, and correctly word-counted. The only
  quoted spans in the S180–S190 rows are two commit titles, of 7 and 11 words.
- No quote-length violation.

## 6. Trend verdicts

- **expansion: unprovable-but-better.** There are 11 new mined tier-A rows (179 → 190) and two of them were re-opened
  live with matching hashes. The new FR6 entry has 10/14 rows supported by outside re-judgement. But four rows stand
  unsupported in the entry (marked only through the receipt pointer at entry :15-16), and the round's measured claim
  did not verify. The lane's `improved` is not adopted.
- **quality: improved.** The r32 repair is independently confirmed: 5/5 not current, clause tallies agree, and the
  correction is append-only. QUALITY 97 is grounded in M1 and shown able to fail. The six scope cells reproduce
  exactly. Open: the §1/Judges inconsistency and the four unsupported C1 rows.
- **discernment: improved.** The outside spot-check agrees with the gate on 2 admits and 2 rejects. Round 32's
  spot-check disagreement became lesson M1 and QUALITY 97 (LEARNING.md "improved" condition). The lane's own
  reporting of CtlGlossaryA1 against its claim is also to its credit.

## 7. Ruling

`status=ok`, `admitted=false`, verdict `rejected-honest-stop`. C1's predicate holds at the tip, and the outside
re-judge agrees with all 14 row verdicts. But a cheap, honestly judged control that skips the claimed decision work met
the frozen P-C1-A1 after data, and §9 says that fails the claim. A1 itself was timed correctly. No axis is harmed. On
SHONEN: all four boxes stay `[~]` in the report. This closure does not assert that any box is non-author checkable;
promotion is operator-owned.

## 8. Routed defects (the lane owes these next round)

1. **Counter discrimination (depth).** The next depth claim freezes a predicate that a no-decision (definition-only)
   control cannot meet. It must commit that control's receipt before data and require each verdict cell to name a
   reader action, checked by something other than the header label (§3.2).
2. **Entry rows 3, 6, 7, 13** are unsupported. Cite S182:1370,1472, S181:78-80, S181:22, or narrow the cells, in a new
   append-only revision. `SKILL.md:816-818` rest on these rows.
3. **Row 8** still teaches the ABI file's "4.18+" discard boundary, which v4.18 code contradicts (w2 AttackRow08). Mark
   it in the entry.
4. **`SKILL.md:820`** says an iostat 0.0 is "never a zero write rate". Row 14 says less than that, since an idle device
   also shows 0.0 [INFERENCE, ConformancePromptHarm]. Align the SKILL line with row 14.
5. **Lesson round-33 §1 vs `## Judges`.** Append a correction that moves S137's `:260` pointer and the omitted clauses
   (S137 ×3, S149 "different contracts", S058 "ancestors first") into §1's last column with a forward pointer, and fix
   ":209 six" (five omitted plus one misfiled).
6. **Lesson :79 and report :52-53** say "no other word changed", which contradicts the S062 and S064 word edits. Append
   a correction.
7. **Receipt time labels** `c1-controls.txt:1` (02:38Z, actual 02:30:05Z) and `parity-freeze.txt:1` (02:3xZ, actual
   02:28:27Z). Future receipts should carry the measured time.
8. **CtlLocatorStale** (a false `file:L` locator survives the counter) and the §1 S117 preamble overstatement (:50-51;
   the releases feed was never committed). Fix both in the next counter or append a note.
