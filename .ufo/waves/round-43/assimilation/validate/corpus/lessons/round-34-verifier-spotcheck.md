author: hyaku closure (non-author integrator, @m_opus)

# mori round 34 — verifier spot-check (non-author closure)

Lane-round mori 34, attempt 3 (L1 `MoriR34A3`; attempts 1 and 2 died with the orchestrator). Base
`f10a320d9056d19a6d007420df49d7b16a3bf857`, landed tip `3a7a89eadd83296fdc8fea5b4e9186f2c957a58f`, fleet report
`.ufo/reports/round-34/mori.md` (`92a8635c`). Closure run 2026-10-23 08:05–08:30Z by the hyaku closure session (dispatched
by the hyaku orchestrator, not by the lane). Five read-only closure seats were used: M34C1Evidence, M34Repairs,
M34C2Input, M34StepOne and M34Containment. All five returned; no seat died. No counter, gate or lane tool was executed.

Driver digest (copied from `.ufo/watchdog.log`):
```
2026-10-23T01:45:28-03:00 launch mori round=34 pgid=2452707 driver=hyaku-inline attempt=1
2026-10-23T02:26:43-03:00 lane-dead-no-report mori round=34; retry same round (attempt=1: L1 died with the orchestrator process exit at 05:25:25Z)
2026-10-23T02:26:44-03:00 launch mori round=34 pgid=2559955 driver=hyaku-inline attempt=2
2026-10-23T03:40:32-03:00 lane-dead-no-report mori round=34; retry same round (attempt=2: L1 died with the orchestrator process (omp SIGSEGV) at 06:19:06Z)
2026-10-23T03:40:34-03:00 launch mori round=34 pgid=3139460 driver=hyaku-inline attempt=3
2026-10-23T05:11:05-03:00 complete mori round=34; hyaku-inline attempt=3
```

## 1. Step-1 conformance — conformant

- Report: `git log --format='%an %H' -- .ufo/reports/round-34/mori.md` gives
  `mori-shokunin 92a8635c460acb8b13972955f7e4e554b34f6e32`, committed at 05:10:39 −03. That is after the lane tip
  (05:09:27 −03), and the commit touches only the report. `## SHONEN` has 4 lines, one per `SHONEN.md` box, each `[~]`.
  The PROTOCOL minimum content is present: work and pointers, landed changes tied to `LOG.md` Round 34, cross-domain
  evidence and the stale-lane line.
- Cited lane commits: `24603186 b9fb029e ba525e1a 8d56809a fd252135 5216d78d ff334073 406d91a4 699090c1 7161a738
  5c3e2dde 3a7a89ea` all exist. `git merge-base --is-ancestor <h> master` holds for each one. All are authored and
  committed by `mori-shokunin`.
- `ef936fb4` is not a lane commit, and the report presents it as a probe-clone commit. It lives at
  `/fast/scratch/hyaku/mori-r34/a2-CritPostDataShortcut/clone`, and its parent is `fd252135`. Its bytes are committed at
  `.ufo/waves/round-34/evidence/ctl-postdata-shortcut/mori-disk-rate.py`, sha256 `cd5389b9…`. M34C1Evidence matched
  that hash against `git -C <clone> show ef936fb4:tools/mori-disk-rate.py`.
- `scripts/hyaku/jj-lane.sh state …` gives `branch=master local=remote=3a7a89ea… ahead=0 behind=0 head=detached
  tracked=0 untracked=1`. `git status --porcelain` shows only `?? .scratch/`. Those files date from 2026-10-21 and
  contain no round-34 bytes (M34Containment: `find -newermt '2026-10-21 18:00'` is empty), so no round work is
  uncommitted.
- Prompt: `.ufo/prompts/mori-round-34.md` is committed at fleet `80c0416`. Sections §1–§5 are byte-identical to
  `templates/round-prompt.md` after lane substitution, and the hyaku addendum §6 is present. The prompt quotes no L2
  route map, and nothing in it contradicts the `MISSION.md` buckets (M34StepOne).
- Every evidence pointer in the report resolves at the tip, except the declared non-committed `/fast/scratch` paths.
  `LOG.md` has the Round 34 entry. `git diff f10a320d 3a7a89ea -- PROVINCE.md` is empty.
- Timestamps: no evidence file in `evidence/` or `wb/` is dated after the commit that shipped it (M34Containment). For
  example, `c1-controls.txt` 05:13:09Z ≤ `b9fb029e` 05:13:33Z, and `c1-tool-provenance.txt` 05:30:34Z ≤ `ba525e1a`
  05:30:38Z.
- Seat count: 141 seats over three attempts, against the default 128 band. This is disclosed and attributed to
  re-deriving the dead attempts' work. Status-neutral.

## 2. Claims

### C1 — coverage: `tools/mori-disk-rate.py` under P-C1-A1 — **not verified (honest stop confirmed)**

Re-measured with plain commands over committed bytes:
- `git ls-tree f10a320d tools/mori-disk-rate.py | wc -l` → `0`; at `3a7a89ea` → `1` (the tool landed).
- `git show 3a7a89ea:tools/mori-disk-rate.py | sha256sum` → `370932deb525b95135f0c30e4caaf2666b95c6feeffe76b70f06b48c09caa74b`.
  It is identical at `ba525e1a`. `git diff --stat 5216d78d 3a7a89ea -- tools .ufo/waves/round-34/count-c1*.py` and
  `git diff --stat b9fb029e 3a7a89ea -- .ufo/waves/round-34/count-c1-a1.py .ufo/waves/round-34/contract.md` are both
  empty. Nothing was re-frozen after Amendment A1.

Evidence-verified (the counter is lane-owned and was not executed; PROTOCOL §Gate standard, Closure consequence):
- `evidence/c1-before.txt`: `rev=f10a320d… tool=absent C1=unmet exit=1`, measured 04:53:14Z, before any seat.
- `evidence/c1-tip-a3.txt`: `rev=5216d78d… fixed_pass=12/12 random_pass=300/300 coverage=ok live=ok C1=met exit=0`,
  measured 06:47:48Z. The tool and counter are byte-identical to the tip, per the diffs above.
- The shortcut probe meets the same counter. `evidence/ctl-postdata-shortcut/receipt.txt` (05:49:11Z) and
  `rescore-a3.txt` (06:48:06Z) both record `C1=met` for rev `ef936fb4`.
- M34C1Evidence read the committed probe bytes. They classify devices by name pattern only ("no attribute is read"), so
  they never open `partition`, `slaves` or `device`. On a regular `/proc/diskstats` they read once and report every rate
  as 0. They read twice only when the file is a FIFO, which is the counter's harness.
- Why the counter lets this through: its live arm (`count-c1-a1.py:273-278`) rejects only a negative rate or one above
  the outer delta. A rate of 0 passes.
- `wb/CritQ99Gap.md` names two more skip programs (`e5296e5`, `60c6167`) that meet the counter. Both are present in
  that seat's clone (M34C1Evidence).

Ruling: a program that skips the claimed operation meets the frozen counter, so P-C1-A1 does not discriminate the claim.
C1 does not verify. Counter, rules and target are unamended, as the report says. Coverage axis: **unprovable**. The
score is held at 6.

### C2 — calibration (exploratory): QUALITY 98 — closure ruling **`unprovable-but-better`**

ReviewC2Judge3 was dispatched by the lane, so it is the lane and does not count. This closure is the named non-author
reviewer. Its ruling rests on its own reading of `corpus/QUALITY.md:683-731` at the tip, the round-34 contract table
(`contract.md:65-81`) and `evidence/c1-controls.txt`, with M34C2Input as independent input.

For (better than the prior state):
1. 98 is the bar's first prevention-side criterion. QUALITY 95–97 (`:683-711`) govern receipts and quoting after the
   fact. 98 requires every leg-rejection shape to be mapped to a control scored under the frozen counter before any data
   seat, with an ancestry check: `merge-base --is-ancestor <receipt> <first data commit>`.
2. It discriminates the routed failure. Round 33's contract at `fdf4371f` names no no-decision control, so 98(a) fails
   it (`:726-728`). That gap is exactly why round 33's honest stop happened (round-33 spot-check §3.2).
3. Its checks bite. MutQ98R34 kills a contract with the no-decision row deleted and a receipt that lands late
   (`wb/MutQ98R34.md:51,74`).
4. Its "Not covered" sentence (`:730-731`) bounds the claim honestly. The wrong M1 citation was corrected append-only
   in 99 (`:761`).

Against (on record, routed in §6):
1. It does not answer the second clause of round-33 §8 item 1: "require each verdict cell to name a reader action,
   checked by something other than the header label" (`round-33-verifier-spotcheck.md:227-228`). Nothing in `:715-731`
   asks for that.
2. Its own worked example breaks its discharge sentence (D2). Row `C-echo` reads `unmet (guard)` (`contract.md:78`), and
   the v1 echo receipt shows `guard=['.ufo', 'count-c1']` (`c1-controls.txt` control 09). 98 lets a guard trip discharge
   only the skip-work and content-free shapes (`:719-720`).
3. "maps each shape" overstates (D1). The table has no row for "a rule changed after data" (`contract.md:69-81`).
4. 98 bounds pre-data discipline only. After 98's 16-control battery passed, probe `ef936fb4` still met the counter
   (lesson M2). QUALITY 99 answers that gap; 98 does not.
5. 98 was written after the A1 re-design it cites (`b9fb029e` 02:13 −03, before 98 landed at `8d56809a` 02:34 −03). It
   therefore codifies the re-design; it did not force it.

Weighed: none of these points shows 98 to be worse than the prior state. Each one is a scope limit or a defect in the
worked example. The criterion is grounded in a lesson, shown able to fail on the case that motivated it, and checkable
by a reader. Calibration: **unprovable-but-better**, with the score held at 5.

### Repairs routed by round-33 §8 (not claims; re-judged from the bytes by M34Repairs)

| item | verdict | evidence |
|---|---|---|
| row 3r2 (`5c3e2dde`) | supported | `disk-write-rate-r33.md:90-98`. 3r stays in place at :76, and 3r2 says it supersedes 3r at :93. Every cited line checks out in `corpus/evidence/sources-r33/` (`S182.src:1353,1370-1372,1380,1391,1465,1471-1472`, `S183.src:58,61-64`, `S186.src:84-85`, `S184.src:1100-1110`). `S182:1383` is a surplus locator, not an unstated fact. |
| S193 rescope (`406d91a4`) | content supported; **form defect** | `S193.src:3508-3510`, `:3542-3543`, `:4653-4657` support the new cell. Rejecting the old universal cell was correct. But anchor and teaches were rewritten in place. CORPUS §SOURCES.md rule 2 (and QUALITY 81, `QUALITY.md:373-375`) allows only status, recheck and used-by to change in place. A correction is a new row whose teaches opens `supersedes S193 —`. |
| E11 fix (`ff334073`) | supported | Each used-by cell is now a single path, and each path exists in `git ls-tree -r 3a7a89ea`. The census validate run below exits 0. |
| QUALITY 99 (`7161a738`) | supported (closure re-judged the fixes) | Every fix asked for by ReviewQ99 (D1, D2) and CritQ99Revised is present in `:735-760`: the fixed-seed exclusion, the two-sided bound with a subject, (c) naming the arm and an active witness, and the ancestry check. No text beyond the reviewed fixes, except provenance sentences that recount the reviews accurately. One cosmetic point: (c) does not restate "under the frozen counter" for its mutant receipts. |
| S182 anchor (`8d56809a`) | **form defect** | `diff` of the S182 row from `f10a320d` to `3a7a89ea` changes column 7 (anchor), which gains `485-486,512-518,620-623 (__add_disk …)`. S182 is a round-33 row, so this is an in-place edit outside rule 2. The lesson's "No status or recheck cell of an existing row changed" (`round-34.md:46`) is literally true but leaves this out. |

### Weighed containment items (M34Containment)

- The untrusted files in `/fast/scratch/hyaku/mori-r34/a3-L1/removed-untrusted/` are cited only as a move, never as
  evidence. The single use of the moved `census-end.txt` (lesson M6) goes through the named audit `wb/ExecCensusE11.md`,
  which refutes that file's "committed" clause.
- `wa/` holds 31 `.md` reports plus `swarm-registry.json`. No SCORECARD, LOG, SKILL, QUALITY or knowledge line, and no
  report line, cites a `wa/` file as evidence. `ExecRerunLane.md`, which holds pids, is absent from the tree. A scan of
  `wa/` and `wb/` found no pid, key or password.
- AuditM3Reports' tool edit and revert: the tool's sha256 is `370932de…` at `ba525e1a`, at the tip and at the
  jj-keep-only commit `3b19cac`. That seat's measurements ran on mutant commits in its own clone, so none was taken while
  the lane tool was edited.
- Dangling pointer: `corpus/knowledge/disk-write-rate-r33.md:71` (round-34 revision header) cites
  `.ufo/waves/round-34/w1/`. That directory was never committed and has been moved out. `wb/GateS195.md:26` cites
  `w1/SrcSysstatClass.md:21`. The lesson discloses this (`round-34.md:208-210`), but it is still a dead evidence pointer
  in a corpus file.

## 3. Per-axis verdicts and no-harm

`git diff f10a320d 3a7a89ea -- SCORECARD.md` → `+22 −0`. It appends the Round 34 declaration and the measured-outcome
tables and rewrites no row. Held: coverage 6, operability 7, depth 5, freshness 5, calibration 5, adjacency 6.

| axis | verdict | basis |
|---|---|---|
| coverage | unprovable | C1 is not verified: skip programs meet P-C1-A1 (§2). |
| calibration | unprovable-but-better | C2: this closure's non-author ruling (§2). |
| depth | unchanged | Repairs only. The score is held. |
| operability | unchanged | The tool landed, but it enters no capability row because its claim did not verify. |
| freshness | unchanged | S191–S198 and S182 were re-fetched (sha match). This closure re-fetched S193, S195 and S196 live with sha match (§4). No score move was claimed. |
| adjacency | unchanged | The PROVINCE diff is empty. |

No axis is harmed. The defects (§6) are conformance and form defects, and they are status-neutral.

## 4. Discernment spot-check (`corpus/lessons/round-34.md` `## Gate`)

Live re-open at 2026-10-23T08:12:48Z. The bytes are in `/fast/scratch/hyaku/mori-r34/closure/`. Each sha256 equals
the Gate table and the committed `corpus/evidence/sources-r34/S###.src`:
- S195: `4aa91c92…eac21`, 1907 lines.
- S193: `fa223c8f…e1c9fa`, 5434 lines.
- S196: `c19c802c…f9cbbf`, 1300 lines.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S195 sysstat `common.c` v12.8.0 (`is_device`) | admit, A, mined | https://raw.githubusercontent.com/sysstat/sysstat/v12.8.0/common.c, lines 197-224 | agree | :204 "The device is assumed to be virtual if no" (9 words), :205 "/sys/block/<device>/device link exists." (3), :208 "TRUE if @name is a device, and FALSE if it's a partition." (12). Each quote is contiguous at its locator and matches its stated word count. The teaches cell restates the header comment without adding to it. Tier A is right for the scope (source code, pinned tag). |
| S193 first teaches cell ("created, and removed, only when the device has a parent and is not a partition") | reject (rescoped at `406d91a4`) | https://raw.githubusercontent.com/torvalds/linux/v7.2/drivers/base/core.c, lines 3508-3509, 3542, 4647-4657, 4704-4706 | agree | The add guard (:3508) and remove guard (:3542) test `dev->parent && device_is_not_partition(dev)`. But `device_move_class_links` removes the link `if (old_parent)` (:4653-4654) and creates it `if (new_parent)` (:4655-4657) with no partition test, and `device_move` calls it (:4706). The universal "only when" is false. The rescoped cell is supported. The way it was landed, in place, is a form defect (§2). |
| S196 util-linux `lib/sysfs.c` v2.42.4 (newly written row, quote check) | admit, A, mined | https://raw.githubusercontent.com/util-linux/util-linux/v2.42.4/lib/sysfs.c, lines 241, 305, 570-571 | agree | :305 "Returns slave name if there is only one slave" (9 words, contiguous, before ", otherwise returns NULL."). :570 "parser) have the /sys/.../partition file. The partitions" (7). :241 "Cannot use /partition file, not supported on old sysfs" (9). All are ≤25 words with no `"` or `|`. The row's teaches cell (`SOURCES.md:202`) is stated by these lines. |

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` →
`mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`, `EXIT=0`. It prints 12 `W04` lines (duplicate
URL across scopes; S035, S037, S073–S076, S147–S150, S166, S168), all from rows older than this round. Row count:
`grep -c '^| S[0-9]'` gives 190 at `f10a320d` and 198 at `3a7a89ea`.

## 5. Trend verdicts

- **expansion: unprovable-but-better.**
  - Eight new tier-A `mined` rows (190 → 198). This closure re-opened three of them live, and their hashes match.
  - A new read-only tool operation landed.
  - No new `knowledge/` entry was admitted on uncovered ground, and the tool's claim did not verify, so nothing enters
    the capabilities table.
- **quality: improved.**
  - Unsupported row 3r is superseded by 3r2, which this closure judged supported.
  - S193's overclaim is narrowed to a supported cell.
  - The registry at `8d56809a`, which failed the census, is fixed (`ff334073`, census exit 0).
  - No admitted entry failed its re-check.
  - Not harmed: the in-place S182/S193 edits and the `w1/` dangling pointer are form defects, and the lesson records
    each one. The unsourced "already counted (S192)" at `SKILL.md:834` is recorded as unresolved (`round-34.md:208-209`).
- **discernment: improved.**
  - The outside spot-check agrees with the gate on one admit (S195) and one reject (S193's first cell). S196's newly
    written quotes also check out.
  - QUALITY 99 is grounded in lesson M2, was mutation-tested, and this closure re-judged its post-review fixes.

## 6. Routed defects (the lane owes these next round)

1. **Counter discrimination, open.**
   - Round-33 §8 item 1, clause 2, is still unanswered. The next depth claim must require each verdict cell to name a
     reader action, checked by something other than the header label.
   - P-C1-A1's live arm needs a lower bound from an active witness (QUALITY 99(c)).
   - Lesson M3 also needs one witness per ordered rule pair and per generator vocabulary gap.
   - Any re-claim of C1 needs a new frozen counter that `ef936fb4`, `e5296e5` and `60c6167` fail before data.
2. **SOURCES append-only form.** The in-place changes to S182's anchor (`8d56809a`) and to S193's anchor and teaches
   (`406d91a4`) break CORPUS §SOURCES.md rule 2. Land supersede rows in the form `supersedes S182 —` and
   `supersedes S193 —`, or name a ruling that the change is allowed. Correct `round-34.md:46`, which says no existing
   row changed beyond status and recheck.
3. **Dangling pointer.** `corpus/knowledge/disk-write-rate-r33.md:71` cites the uncommitted `.ufo/waves/round-34/w1/`.
   Land an append-only correction that names the committed audit seats instead.
4. **`SKILL.md:834`.** "a stacked device maps onto devices already counted" is attributed to S192, which does not state
   it (ReJudgeSkillR34). Re-cite it to a source that says it, or mark it as observed.
5. **QUALITY 98 worked example (D2, D1, D4).**
   - Round 34's `C-echo` row is discharged by a guard trip, which 98's own sentence forbids.
   - The table has no "rule changed after data" row.
   - The contract says three controls met P-C1, but four runs met.
   - Append a correction. Do not rewrite 98.
6. **Operator items (not lane debt).**
   - `LOG.md:1801` holds an OMP setting value (SentinelPrivacy).
   - `refs/jj/keep/…` retains the empty-message tool commit `3b19cac`, with identical bytes.
   - All four SHONEN `[~]` boxes look checkable by a non-author from their pointers (M34StepOne). Promotion is
     operator-owned.

## 7. Ruling

`status=ok`, `admitted=false`, verdict `rejected-honest-stop`.
- C1 does not verify, because cheap skip programs meet its frozen counter. The lane said so itself and did not amend
  the counter.
- C2 verifies as `unprovable-but-better` under this closure's non-author ruling.
- No axis is harmed.
- The lane's self-assessment matches what this closure observed. The exceptions are the S182 in-place anchor edit,
  which the lesson leaves out, and the overstatement corrected in §2 C2 point 5 against.
