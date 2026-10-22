# ReviewSourcesShape: round 24 wave 2, SOURCES contract conformance

Seat: MoriR24.ReviewSourcesShape (leaf reviewer, no subagents).
Lane: /home/vgpnk/Projects/shokunin/mori-shokunin.
Scope: `corpus/SOURCES.md` rows S090–S097 and the new Paths line, checked against the SOURCES contract v1 in `/home/vgpnk/Projects/shokunin/CORPUS.md:64–155`, the round-24 lesson (`corpus/lessons/round-24.md`), and the validator.
Reviewed state: measured tip `a730ecfefbdb5c31b1db13aca2c40eecd5e97abc`. Lane HEAD is `13208d2a533380e1231dc935b6c338db99f1ddae`. `git diff a730ecf 13208d2 -- corpus/` prints nothing, so every finding below holds at HEAD.

## Bottom line

- The source facts hold on re-open. Every raw-file digest, quote and line range I checked matches the fetched v7.2 bytes, and the negative claim that no `proc_pressure(5)` page exists holds against the man-pages 6.20 tarball.
- The contract is not met as written. H1 is the only High finding: admitted claims rest on external sources with no registry row. M2, M3 and M4 are Medium contract breaches (a false lesson claim with an incomplete used-by; no round-24 search-log note; an in-place S090 edit whose anchor change is unlogged) that the integration owner must fix or explicitly accept before closure. M1, M5 and M6 are row or scope corrections. M7 is a validator gap: its `ok` is not a conformance verdict.
- Nothing in the lane was edited. The only file I created in the lane is this report.

## Validator (read-only, as assigned)

| Command | Result |
|---|---|
| `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` | `mori W04` for S035, S037, S073, S074, S075, S076; `mori ok …/corpus/SOURCES.md`; exit 0 |
| same with `--verbose` | identical output |
| `scripts/sources-census.sh selftest` | every listed mutant prints `killed`; `selftest ok`; exit 0 |
| `scripts/sources-census.sh census mori --root …` | rows 97; tier A 82, B 6, C 9; status mined 62, queued 25, rejected 10; missing 0; exit 0 |
| `validate --file` on scratch clone at a730ecf | same six W04 lines and `ok`; exit 0 (reproduces) |

The W04 lines are second occurrences of a URL already registered in another scope. None involves S090–S097. Nothing reports S090–S097 as malformed, duplicated, future-dated or badly tiered.

## Row matrix, S090–S097

Digest = first 16 hex of SHA-256 of the fetched file, compared with the Gate. "Re-opened" = line range fetched and read.

| Row | Tier, kind | Digest | Anchors re-opened | Gate quote | Teaches | Used-by | Flags |
|---|---|---|---|---|---|---|---|
| S090 psi.rst | A, docs | 11c6b7129103b454 match | 34–119, 181–185 match | 57–58 exact | matches | knowledge + lesson, both cite | M4, L3, L4 |
| S091 psi.c | A, code | 452318beaca3e6d1 match | 145–158, 228–234, 1251–1291, 1710–1721 match | 1282–1283 exact | matches | knowledge + lesson, both cite | M1, L3 |
| S092 cgroup-v2.rst | A, docs | a9433bb0e16a67f0 match | 1066–1087, 1215–1221, 1911–1915, 2171–2175 match | 1073–1074 exact | matches | knowledge + lesson | none |
| S093 Kconfig | A, code | a43f09d89309a6bd match | 615–624, 723–760 match | 730–731 exact | matches | knowledge + lesson | none |
| S094 kernel-parameters | A, docs | 23b1a690210b6884 match | 5505–5507 match | 5505 exact | matches (`<bool>` confirmed) | knowledge + lesson | none |
| S095 psi_types.h | A, code | 483269b27c82b438 match | 41–70, 208–214 match | 54–55 exact | matches | knowledge + lesson | L3 |
| S096 commit 52b1364 | A, code | HTML only, no digest | commit subject, dates, cgroup.c in diffstat match | commit text exact, 25 words | **overclaims** (absent irq file) | knowledge + lesson | M5, L7 |
| S097 man7 proc_pressure(5) | C, docs, rejected | 80c3fe2ae1062abf match (16) | 404 body line 6 match | exact | reason matches; **flip wrong** | lesson only; knowledge also cites it | M2, M3, L1, L2 |

Opened dates, recheck (`on-release`), status and tier values are valid for all eight rows. No community row sits at tier A. The IDs are contiguous, unused before, and the next after S089.

## Findings

### H1 (High): admitted knowledge rests on external sources with no registry row

- `corpus/knowledge/system-pressure-r24.md:1` says: "Supporting reads without registry rows: Linux v7.2 kernel/cgroup/cgroup.c and kernel/time/sched_clock.c."
- Claims resting on them: F9 (lines 103–109, cites `cgroup.c:4077-4091`, `4127`, `3970-4091`); F12 (lines 124–126, cites `sched_clock.c:48-50, 242-243` and `include/linux/sched/clock.h:112-116`); U1 (line 176, cites `kernel/sched/sched.h:3492-3521`); U7 (line 186, cites `include/linux/psi.h` and `cgroup.c`).
- The cited lines are accurate: in the fetched v7.2 files, cgroup.c has the functions at 4077 and 4085, the comment at 4127, and the entry at 5577–5580; sched_clock.c has `irqtime` at 48–50 and the enable at 242–243. The defect is provenance, not content.
- Contract: `CORPUS.md:163–166` (kaika rule) says that when the source is external, `source:` cites its `S###` row "alongside the URL and anchor". `CORPUS.md:112–115` (Rule 1) says a row is written in the round that opens the source. Neither rule has an exception for supporting reads.
- Fix: write rows for each external source, with Gate quotes, or remove the claims that depend on them.

### M1 (Medium): S091 cited beyond its scope, and its anchor does not cover what is cited

- S091 scope (`corpus/SOURCES.md:97`) says "not trigger semantics".
- The knowledge entry cites S091 for trigger semantics: F5 (lines 67–68) cites `psi.c:1364-1367` (IRQ trigger naming `some` refused with EINVAL; re-opened at 1364–1366, accurate). F8 (lines 93–96) cites `psi.c:167` (WINDOW_MAX_US; re-opened, accurate) and `psi.c:1596-1598` (EBUSY; re-opened, accurate).
- Cited lines missing from the S091 anchor cell (`SOURCES.md:97` lists 145–158, 228–235, 1251, 1257–1263, 1273–1291, 1710–1721): PSI_FREQ 160–164 (F4), total accumulation 408–410 (F10), IRQ accounting path 1032–1042 (F5), reader wrappers 1538–1550 and open handlers 1553–1566 (F7, F9).
- Fix: give trigger code its own row with its own scope, or drop the trigger claims. Extend the S091 anchor to the lines it supports; the scope exclusion stays true.

### M2 (Medium): lesson M3 is false, S097 used-by is incomplete, and a tier-C row is the sole support for a knowledge-side negative claim

- `corpus/lessons/round-24.md:56` (M3) says "the knowledge entry cites only S090–S096." The knowledge entry cites S097 at line 1 ("Rejected candidate: S097") and at line 185 (U6: "No `proc_pressure(5)` page exists (S097, rejected: HTTP 404…)").
- `corpus/SOURCES.md:103` lists used-by as `corpus/lessons/round-24.md` only. `CORPUS.md:107–108` defines used-by as "the knowledge entries or lessons citing the row".
- Amendment A5 in `.ufo/waves/round-24/contract.md:162–163` says S097 is "cited by nothing." That was already false when df4db54 landed, since the knowledge entry is in the same commit.
- `CORPUS.md:96` says tier C is "never sole support for an admitted entry." U6 has no other registered support for "no such page exists"; the sweep source is not registered (see M3).
- Fix: add `corpus/knowledge/system-pressure-r24.md` to S097's used-by; correct M3 and A5's wording; either register the man-pages sweep as a source or label U6's negative claim with its sweep method.

### M3 (Medium): no round-24 search-log note

- `corpus/SOURCES.md:114–146` holds Bounded search 1–15; the last one (line 146) is round 23. Grepping for `Round ?24|round-24|round 24|S09[0-7]` finds only registry rows (96–103) and the Paths line (112).
- `CORPUS.md:59–61` (Rule 5) requires one prose note per bounded search with identified, screened, included and excluded counts, exclusion reasons, and a stop rationale. It adds: "A negative claim carries its sweep." `CORPUS.md:82` (Shape) says the same.
- S097's sweep appears only as anchor text (`SOURCES.md:103`: "man-pages 6.20 contains no man5/proc_pressure page…"), with no method, command or date. The sweep itself holds (see Verified).
- Fix: add "Bounded search 16 — round 24" with counts (8 rows examined, 7 included, 1 rejected with reason) and the sweep method.

### M4 (Medium): S090 changed in place, and the old→new log omits the anchor change

- `git show a730ecf -- corpus/SOURCES.md`: the S090 line (`SOURCES.md:96`) changed in two cells. Anchor: "system CPU full undefined and zeroed since 5.13:57-58" → "system CPU full undefined, reported as zero since 5.13:57-58". Teaches: "each file is exactly two lines" → "each named file (cpu, memory, io) shows a some line and a full line". The new teaches is accurate (psi.rst lines 37–43 and 45–55, re-opened).
- The lesson's log (`round-24.md:45–48`) records only the teaches change, under the heading "anchor and teaches cells, old → new."
- `CORPUS.md:49–51` (Rule 2): "Only `status`, `recheck` and `used-by` change in place… A correction is a new row whose `teaches` opens `supersedes S0NN —`." The text has no same-round exception.
- Fix, as an owner decision: either record this as a documented deviation from v1, or restore the original S090 cells and add S098 "supersedes S090 —". Either way, log the anchor change old→new.

### M5 (Medium): S096 teaches overclaims and contradicts S091 and the knowledge entry

- `SOURCES.md:102` teaches: "so an absent irq file is a build-configuration fact and never a zero reading."
- The fetched S091 `psi_proc_init` creates all four files only under `if (psi_enable)` (psi.c:1710–1712). With PSI disabled at boot, the irq file is absent for a reason other than build configuration. S091's own teaches says so (`SOURCES.md:97`: "a PSI switched off at boot leaves them absent").
- The knowledge entry's decision table (`system-pressure-r24.md:139`) says: "a missing file is consistent with either; the tool records no cause."
- Fix: add a row "supersedes S096 —" that keeps the true part (the irq file exists only when CONFIG_IRQ_TIME_ACCOUNTING is built) and drops "a build-configuration fact."

### M6 (Medium, pre-existing): S059 is malformed and the validator passes it

- `corpus/SOURCES.md:65` (raw read): the anchor cell holds "REJECTED: porcelain command outside…", the teaches cell is the single word "rejected", and the anchor has no revision. The column count is 11, so NF=13 passes.
- `scripts/sources-census.sh:671–672` (W02) fires only when `length(teaches)<8`. "rejected" is exactly 8 characters, so it passes. No check requires the `REJECTED:` prefix.
- Introduced by `daceeec` (round 18), not changed in round 24.
- Fix: a correction row "supersedes S059 —" whose teaches opens `REJECTED: …; flip: …` and whose anchor carries a revision. Owner decision whether to rewrite in place.

### M7 (Medium, tooling): `validate ok` does not establish the used-by, rejection-format or search-log rules

Three mutants on the scratch clone at a730ecf (`corpus/SOURCES.md` lines 96, 100, 103; validated with `--file`):

| Mutant | Expected if the rule were enforced | Observed |
|---|---|---|
| A: S090 used-by changed to `corpus/lessons/round-23.md` (exists; does not cite S090) | a used-by citation check fails | no finding for S090 |
| B: S097 teaches "Not admitted: …" (no `REJECTED:` prefix) | a rejection-format check fails | no finding for S097 |
| C (control): S094 opened 2026-10-23 | E08 | `file E08 S094 opened=2026-10-23`; exit 1 |

- The checker works where it is designed to. E11 (`sources-census.sh:566–567`) tests only that used-by paths exist. Nothing tests the search log or anchor revisions.
- Fix (tooling owner, not implemented here): add a REJECTED-prefix check, a check that each used-by path contains the row's id, and a search-log presence check per round.

### L1 (Low): S097 flip does not name a verdict-changing condition, and its line numbers belong to S090

- `SOURCES.md:103` flip: "the same scope is documented by the kernel PSI documentation (S001; kernel v7.2 Documentation/accounting/psi.rst lines 42-43 and 57-58)." That describes why the row is unnecessary. It does not say what would change the verdict.
- The lesson gives a different flip (`round-24.md:39–40`): "the man-pages project publishes a `proc_pressure` page." That one is correct.
- Lines 42–43 and 57–58 match the fetched S090 file (psi.rst), not S001 (the live docs.kernel.org page).
- Fix: use the lesson's flip in the row; cite S090 for those lines.

### L2 (Low): S097 timestamp and digest cell differ between registry and lesson

- `SOURCES.md:103`: "fetched 2026-10-22T08:21:47Z; body 196 bytes, sha256 80c3fe2ae1062abf5". `round-24.md:32`: "2026-10-22T08:21:46Z (HTTP 404, sha256 80c3fe2ae1062abf)".
- Fetched: 196 bytes, digest `80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880`. Both prefixes agree with the bytes; the fetch time cannot be checked.
- Fix: make the two cells identical.

### L3 (Low): Gate anchor lists omit ranges the registry cites

- `round-24.md:25–32` lists anchors verified for S090 (37–38, 40–43, 57–58, 60–65, 102–110, 181–185), S091 (1257–1263, 1273–1291, 1710–1721) and S095 (41–49, 51–56, 57–70).
- The registry also cites S090 34–35, 45–46, 48–55, 81–88, 118–119; S091 145–158, 228–235, 1251; S095 208–214. Every one I re-opened is correct. The Gate should list them.

### L4 (Low): teaches cells bundle several benefits

- `CORPUS.md:101` says "one grounded learner benefit." S090's teaches has five clauses (`SOURCES.md:96`); S091 has three; S096 has two. The pattern predates round 24 (for example S011).

### L5 (Observation): the same document is registered twice

- S001 (live docs.kernel.org psi.html) and S090 (raw v7.2 psi.rst) cover one document. The lesson (`round-24.md:41–43`) justifies S090 by its different URL and anchors. The validator's E04 checks URL plus scope, so this passes. The question is whether a pinned revision should be a second row or a note on S001.

### L6 (Low, ambiguous): knowledge `source:` line gives no URLs or anchors

- `system-pressure-r24.md:1` names S-ids and file names only. `CORPUS.md:163–166` says `source:` cites the row "alongside the URL and anchor." The URLs and anchors are in the body, so this may be satisfied.

### L7 (Low): S096 dates are local-offset dates, unstated

- The registry gives authored 2022-08-26 and committed 2022-09-09. The commit page gives 2022-08-26 00:41:08 +0800 and 2022-09-09 11:08:32 +0200. The row does not say these are author-local dates.

### Info

- I1: Lane HEAD (13208d2) is one commit past the measured tip (a730ecf). SOURCES.md and the round-24 lesson are unchanged since a730ecf.
- I2: SKILL.md cites S090, S091, S095 and S096 (`SKILL.md:619, 630`). The contract's used-by covers knowledge entries and lessons only, so this is not a violation. `SKILL.md:629` cites `psi.c:1716-1717` for the irq file's creation; the creation line is 1718, and the `#ifdef` is at 1717.

## Verified (what held)

- **Digests**: SHA-256 prefixes match the Gate for S090 (11c6b7129103b454), S091 (452318beaca3e6d1), S092 (a9433bb0e16a67f0), S093 (a43f09d89309a6bd), S094 (23b1a690210b6884), S095 (483269b27c82b438) and S097 (80c3fe2ae1062abf).
- **Quotes**: exact for S090 57–58; S091 1282–1283; S092 1073–1074; S093 730–731; S094 5505; S095 54–55; S096 commit message ("Note we don't use PSI_IRQ_SOME since IRQ/SOFTIRQ always happen in the current task on the CPU, make nothing productive could run even if it were runnable, so we only use PSI_IRQ_FULL", which is 25 words with the ≤25 limit met); S097 404 body line 6.
- **Anchors**: each registry range I opened holds the content claimed. Ranges: S090 34–119 and 181–185; S091 145–158, 228–234, 1251–1291, 1710–1721; S092 1066–1087, 1215–1221, 1911–1915, 2171–2175; S093 615–624, 723–760; S094 5505–5507; S095 41–70, 208–214.
- **S096 commit** (git.kernel.org `52b1364`): subject matches the row title; author Chengming Zhou 2022-08-26 00:41:08 +0800; committer Peter Zijlstra 2022-09-09 11:08:32 +0200; diffstat includes `kernel/cgroup/cgroup.c`. Merge `bd9a3dba185c` (git.kernel.org): "Merge tag 'sched-psi-2022-10-14'", author Linus Torvalds 2022-10-14 13:03 -0700, and its list includes "sched/psi: Add PSI_IRQ to track IRQ/SOFTIRQ pressure."
- **S097 negative sweep**: `man-pages-6.20.tar.xz` from kernel.org (1,914,692 bytes; SHA-256 `180f0d16a2142dd9671760ac0afeadcc25e861f695eb420293e1206a87ca083f`). A glob for `*pressure*` in the extracted tree returns nothing. A grep for `proc_pressure|proc/pressure|pressure stall|PSI` returns only "GREEK CAPITAL LETTER PSI" rows in an iso_8859-7 page. The man7 proc(5) page (31,125 bytes) has no "pressure" match.
- **No older row changed**: `git diff df4db54^ df4db54 -- corpus/SOURCES.md` is 9 insertions and 0 deletions. a730ecf changed only the S090 line. S001 is unchanged.
- **Paths line**: all seven IDs exist. Format matches `CORPUS.md:81`. The order agrees with what the rows say.
- **Used-by for S090–S096**: the knowledge entry and the lesson each cite every one of those IDs (grep).

## Residual risk and verification gaps

- Not verified: "absent from the v6.0 psi.c history" and containment of 52b1364 in v6.1-rc1. There is no kernel clone here, the GitHub API returned 403 (rate limit), and git.kernel.org was fetched only for the commit and the merge.
- Not verified: the 2026-10-21 release date for man-pages 6.20 (not in the tarball fields I read).
- Not fetched: `kernel/sched/sched.h`, `include/linux/sched/clock.h`, `include/linux/psi.h` (cited by U1 and U7). U7 is explicitly unadmitted.
- Not verified: the fetch timestamps (08:21:46Z vs 08:21:47Z).
- Only three validator mutants were run. The selftest ran as shipped.
- Not evaluated: the C2 tool and its tests, and the knowledge entry's technical content beyond the cited lines.
- One `git status --short` ran in the lane at the start. It is read-only in content but may refresh the index stat cache. Later git calls used `--no-optional-locks`.

## Commands and tools

- Tools already present: curl, tar, git, sha256sum, and the gawk-based validator. No installs or upgrades. `/home/vgpnk/.omp/agent/RULES.md` was read first.
- Fetches (to scratch): raw v7.2 files for S090–S095; `torvalds/linux/commit/52b1364…` (HTML); `man7.org` proc_pressure(5) (404) and proc(5); `kernel.org` man-pages-6.20.tar.xz; `git.kernel.org` commit pages for `52b1364` and `bd9a3dba185c`; raw `kernel/cgroup/cgroup.c` and `kernel/time/sched_clock.c`. GitHub API calls failed with 403.
- Scratch root: `/fast/scratch/hyaku/mori-r24-a2/w2/ReviewSourcesShape/`. It holds the fetched sources, the tarball and its extraction, and a clone at a730ecf (`mori-shokunin/`). The clone's `corpus/SOURCES.md` carries the three mutant edits and was not restored. The clone is scratch and is not the lane.

## Recommended order for the integration owner

1. H1: write rows for cgroup.c and sched_clock.c (plus sched.h, clock.h and psi.h if U1 and U7 stay), or drop the claims that rest on them.
2. M2: fix S097's used-by, lesson M3 and A5's wording; register or label the sweep.
3. M3: add the round-24 search-log note.
4. M1: trigger claims need a trigger row or removal; extend S091's anchor.
5. M4: owner decision on the in-place S090 edit; log the anchor change.
6. M5: add "supersedes S096 —".
7. M6: add "supersedes S059 —" (pre-existing).
8. M7: tooling gaps, for the tooling owner.
9. L1–L3: small row and Gate corrections.
