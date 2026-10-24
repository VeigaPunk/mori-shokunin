# SourcesCensus falsify report (seat MoriR20.SourcesCensus, round 20)

**VERDICT: PARTIAL.**
The census numbers and validator results hold at every snapshot I took (BEFORE = 2061780, HEAD = 8f8c58e, LIVE-3 = 11:13:26Z UTC): `validate` rc 0 with no E-codes, all seven CORPUS.md census commands clean, and every histogram change is explained by appended rows S066–S076. No pre-existing row's status, tier, recheck, scope, anchor or teaches changed. The new rows' quotes and hashes checked out against the live sources.
It is PARTIAL because the bookkeeping around the census does not hold: the lesson's change log contradicts itself and its C2 source list is stale; the census cannot represent supersession (4 superseded rows are counted as active); the freshness check cannot fire before 2027-01-17; and the registry was being written during my run (three SOURCES.md states, 74→75→76 rows, between 11:07:16Z and 11:11:41Z), so no stable "now" existed in the window. Every number below is pinned to a named snapshot.

## 1. Snapshots (UTC, 2026-10-21)

| label | source | sha256 (prefix) | lines / bytes | rows |
|---|---|---|---|---|
| BEFORE | `git -C mori-shokunin show 2061780:corpus/SOURCES.md` | 9f0f303a89d77b5e | 106 / 48216 | 65 |
| HEAD | `git show HEAD:corpus/SOURCES.md` (8f8c58e); equal to the working copy at my first read | b22a0b11ae7db47f | 115 / 52810 | 72 |
| LIVE-1 | working copy at 11:07:50Z (mtime 11:07:16Z) | 869e926dc9bb5a9c | 117 / 54346 | 74 |
| LIVE-2 | working copy at 11:10:03–11:10:51Z (mtime 11:09:38Z) | f2ff7d92d9b9ac3a | 118 / 55136 | 75 |
| **LIVE-3** | working copy at 11:13:26Z (mtime 11:11:41Z; identical again at 11:14:04Z) | d77bfde54be2c539 | 119 / 56135 | **76** |

- Git lineage: 2061780..HEAD is 3 commits (e4d9384, 2eeae04, 8f8c58e); only 8f8c58e touches `corpus/SOURCES.md`.
- At LIVE-3 four files differ from HEAD and are uncommitted: `corpus/SOURCES.md`, `corpus/knowledge/drift-repin-r20.md`, `corpus/knowledge/wave-settlement-r20.md`, `corpus/lessons/round-20.md`. `SKILL.md:498` also names S076; I did not check its git state.
- My first read (HEAD) happened before the 11:07:16Z write; its exact time was not captured.

## 2. Commands and exact outputs

### 2.1 `validate` (required command)
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`, cwd `mori-shokunin`.
- HEAD (first read): rc 0
  ```
  mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
  mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
  mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
  ```
- LIVE-3: rc 0; the same two W04 lines plus W04 for S073, S074, S075 and S076 (URL duplicates of the superseded rows S069/S071/S070/S067), then `mori ok`.
- BEFORE: `validate --file /tmp/sc-r20/before-tree/corpus/SOURCES.md` (git archive of 2061780): rc 0; `file W04 S035`, `file W04 S037`, `file ok`.
- Validator identity: fleet `scripts/sources-census.sh` worktree sha256 `3fb7261569f46423…` equals HEAD. Its last commit is 6a1dd8c (2026-10-19 21:22:45 -0300), before the lane's round-20 commits.
- `sources-census.sh selftest`: rc 0; 96 killed, 0 SURVIVED (97 output lines).

### 2.2 CORPUS.md census commands
Seven commands, extracted verbatim from `/home/vgpnk/Projects/shokunin/CORPUS.md:134–147`, run from `mori-shokunin`. All rc 0. awk is `/usr/bin/awk` → gawk, so histogram key order is gawk's; values are shown as printed.

| # | check (CORPUS must-print) | BEFORE | HEAD | LIVE-3 |
|---|---|---|---|---|
| 1 | rows (`grep -cE`) | 65 | 72 | 76 |
| 2 | malformed, NF≠13 (must be 0) | 0 | 0 | 0 |
| 3 | tier histogram | A=55 B=3 C=7 | A=59 B=5 C=8 | A=62 B=6 C=8 |
| 4 | status histogram | mined=34 queued=23 rejected=8 | mined=39 queued=24 rejected=9 | mined=42 queued=25 rejected=9 |
| 5 | duplicate ids (must print nothing) | empty | empty | empty |
| 6 | enum / tier-inflation (must print nothing) | empty | empty | empty |
| 7 | mined used-by missing (must print nothing) | empty | empty | empty |

### 2.3 `census` and `overdue` (script modes, read-only)
- census LIVE-3: rc 0; `mori rows 76; tier.A 62; tier.B 6; tier.C 8; status.mined 42; status.queued 25; status.rejected 9; missing 0`.
- overdue LIVE-3: rc 0; 76 `cadence` lines, 0 `overdue` lines. BEFORE: 65 cadence, 0 overdue. HEAD: 72 cadence, 0 overdue.
- An independent python parse (CORPUS column semantics: id $2, kind $4, tier $5, status $9, used-by $12) agreed with the awk at all three snapshots (65 / 72 / 76).

### 2.4 Mined-citation audit (used-by path must exist and name the row id)
- BEFORE: 34 mined rows, 59 (row, path) pairs, 0 missing, 1 path that does not name its row: S001 → `corpus/lessons/2026-10-15-free-lunch-measurements-counter-baselines.md` (cites the kernel PSI URL, not "S001").
- LIVE-2 (11:10:03): 41 mined rows, 72 pairs, 0 missing; the only no-id citation is S001, unchanged since 2061780.
- LIVE-3: S076's three used-by paths (`corpus/knowledge/drift-repin-r20.md`, `corpus/lessons/round-20.md`, `SKILL.md`) exist and name S076 (checked directly). I did not re-run the full audit at LIVE-3.

## 3. Histogram: before vs now

| snapshot | rows | tier A/B/C | status mined/queued/rejected | kind docs | validate |
|---|---|---|---|---|---|
| BEFORE 2061780 | 65 | 55/3/7 | 34/23/8 | 33 | rc 0, W04×2, ok |
| HEAD 8f8c58e | 72 | 59/5/8 | 39/24/9 | 40 | rc 0, W04×2, ok |
| LIVE-3 11:13:26Z | 76 | 62/6/8 | 42/25/9 | 44 | rc 0, W04×6, ok |
| LIVE-3 active view (excl. superseded S067, S069, S070, S071) [computed] | 72 | 60/4/8 | 39/24/9 | — | — |

- BEFORE→HEAD: +7 rows (S066–S072). Tier +4A +2B +1C. Status +5 mined +1 queued +1 rejected.
- HEAD→LIVE-3: +4 rows (S073–S076). Tier +3A (S073, S074, S075) +1B (S076). Status +3 mined (S073, S074, S076) +1 queued (S075).
- BEFORE→LIVE-3: +11 rows. Tier A+7 B+3 C+1. Status mined+8 queued+2 rejected+1. Kind docs+11.
- Supersession, read from the `supersedes` text in `teaches`: S069→S073, S070→S075, S071→S074, S067→S076. The census has no superseded status, so these four are counted as active.

## 4. Append-only and change-log checks
- Rows S001–S065: byte-identical to 2061780.
- Rows S066–S076 against HEAD: no id removed. The seven committed rows keep their status, tier, recheck, scope, anchor and teaches. The only in-place edits are `used-by` appends on S066, S067, S068 and S071 (each + `corpus/lessons/round-20.md`). Ids are contiguous 1–76 with no duplicates.
- Search log entries 1–11 are contiguous. Entry 11 is at `corpus/SOURCES.md:115`. Its current counts are internally consistent (6 included + 1 excluded + 5 not rowed = 12 identified).
- Leads: the bash lead bullet (`SOURCES.md:119`) was rewritten in round 20. At HEAD it reads "(resolved round 20)"; at LIVE-3 it reads "(source admitted round 20, linkage pending)". It is a Leads bullet, not a row, so it is allowed.

## 5. Source re-open (this seat, non-author check of the new rows)

| row(s) | check | result |
|---|---|---|
| S066 | raw README at 5d98f0c1…, sha256 | `db6b2f6a1aa542dbb262dc655c6c40d3703d7c04b89b44adcd6c3e1d3e30de0b`, exact match; quote on line 75 (row cites 72–77) |
| S070, S075 | `bash-5.3.tar.gz` sha256 | `0d5cd86965f869a26cf64f4b71be7b96f90a3ba8b3d74e27e8e9d9d5550f31ba`, exact match |
| S070, S075 | `doc/bashref.texi` | pipefail sentence at lines 6063–6065 (the quote wraps 6063–6064); PIPESTATUS text at 7490–7493 |
| S075 negative claim | "early-exit SIGPIPE effect is not taught by this manual" | sweep of the whole texi for `SIGPIPE\|early exit\|exit early`: 0 hits |
| S067, S076 | Feathers essay | quote present (typographic apostrophe normalized); "August 08, 2016" |
| S068 | python `os.html` | quote present (tags stripped); "Python 3.15.0 documentation" |
| S069 | python `pathlib.html` | quote present (tags stripped) |
| S073 | same page | quote sits in the `PurePath.relative_to` Warning that names `walk_up`, as the Gate row says |
| S071, S074 | Kubernetes controller page | quote present; "Last modified September 01, 2024" |
| S072 | Wikipedia | quote present |

- Gate quote lengths, lesson Gate table: S066 15, S067 22, S068 16, S069 17, S070 22, S071 12, S072 14 words, all ≤25.
- Normalization caveat: "byte-for-text" (lesson) holds only after whitespace and typographic-quote normalization. S070's quote spans a line wrap.

## 6. Findings (open first)

- **F1 — lesson change-log contradicts itself (open).** `corpus/lessons/round-20.md:56–57` says "Status/recheck/used-by changes to existing rows: none;" and, in the same paragraph, lists in-place used-by changes for S066, S067, S068 and S071. It also lists S073 as "in-place", but S073 is an insertion (`SOURCES.md:79`). Fix the sentence (L1 decision).
- **F2 — stale C2 source list (open).** `corpus/lessons/round-20.md:16` reads "C2 … Sourced: S068, S069, S071." The knowledge file `corpus/knowledge/wave-settlement-r20.md:6–7` cites S068, S073 (supersedes S069) and S074 (supersedes S071). The lesson lists superseded rows; the knowledge file lists their superseding rows. Pick one convention.
- **F3 — census cannot express supersession (open, design).** The status enum is queued|mined|rejected. Supersession lives only in `teaches` text, and W04 flags each pair as a duplicate URL across scopes (warning only). At LIVE-3 the census reports 76 rows, 72 of them not superseded (computed).
- **F4 — "seven scribes" count (resolved in the run).** At LIVE-1/LIVE-2, `SOURCES.md` entry 11 said "seven round-20 source scribes (`build/Src*.md`)"; the glob matched 6 files. At LIVE-3 it reads "six … scribes", and the correction paragraph credits "wave-2 ReviewGate". "Identified" moved 10→12 and "not rowed" 3→5. The arithmetic is consistent in both versions.
- **F5 — validator does not check that a used-by path names its row (pre-existing).** E11 checks only existence. S001 is the case (§2.4).
- **F6 — no validator check on knowledge/lesson citations (blind spot).** My scan of the registry's used-by union plus the three named files (22 targets) found no dangling ids at 11:08:42, 11:10:03 and 11:13:26Z. At my read of `wave-settlement-r20.md:6` the knowledge file already cited S073, while my first read (HEAD) had no S073; the first live read showing S073 came later, so the write order was not observed. A transient dangling citation is [INFERENCE]; it is closed now.
- **F7 — freshness signal is vacuous for now.** At HEAD there are 25 NNd rechecks; the earliest falls due 2027-01-17 (90d rows opened 2026-10-19: S012, S018, S024, S025, S034). The 47 `on-release` rows are never judged. "0 overdue" is date arithmetic, not evidence of freshness.
- **F8 — grounding over-reach, corrected in-tree (resolved).** S070's "early-exit" teaching was not in its cited lines (confirmed by the 0-hit sweep above). S069's teaching over-reached (the pathlib Warning does not teach the `..`/absolute rejection). Both were superseded by append-only corrections (S075, S073) triggered by the wave's reopen seats. Two more supersessions: S074 raises S071 from B to A on the same page, citing the CORPUS.md tier rule (official docs are A), and S076 narrows S067. All pass validate with W04 only.
- **F9 — moving target (open for main agent).** Between 11:07:16Z and 11:11:41Z the registry went 74→75→76 rows, and the lesson and the wave-settlement knowledge file were written in the same window. SKILL.md now names S076; its write time was not checked. Any census number is valid only for its stated snapshot.

## 7. Retraction
Earlier in the run I reported S073 and S074 as dangling. That was my error: I compared a stale id set (HEAD, 72 rows) with a scan of the live file. Live-only scans show no dangling ids. Withdrawn.

## 8. Checks for the main agent after the L1 freezes the tree
1. Record `git -C mori-shokunin rev-parse HEAD` and `sha256sum corpus/SOURCES.md`.
2. `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`. Expect rc 0 and W04 only for supersession pairs.
3. The seven CORPUS.md census commands (lines 134–147) from `mori-shokunin`. Expect 0 for checks 2, 5, 6 and 7.
4. Compare rows, tier and status with the LIVE-3 table. Any further change should be append-only.
5. Decide on F1, F2 and F3. These are lane edits and belong to L1.

## 9. Bounds, tooling, commands (disclosure)
- Installs or updates: none. Used present tools only: python 3.14 kernel, `/usr/bin/awk` (gawk), `/usr/bin/curl`, git.
- Git: read-only subcommands only (`show`, `log`, `rev-parse`, `rev-list --count`, `ls-tree -r -l`, `archive`, `cat-file -t`). Disclosure: `git status --porcelain=v1 -- <paths>` ran twice without `GIT_OPTIONAL_LOCKS=0`. It can refresh the index stat cache but changes no content. One of my own log lines said "optional locks off"; that was wrong.
- Not run: `tools/mori-census.sh`. Not read: `.ufo/interactive-sessions/`, `.ufo/worktrees/`, `.jj/`, `~/.omp` session logs. No whole-lane or whole-fleet grep or glob.
- Fleet files read: `CORPUS.md:64–184`; `scripts/sources-census.sh` (header, arg parsing, validate and overdue code); `shokunin.conf`; git log/show for `scripts/sources-census.sh`.
- Lane files read: `.ufo/waves/round-20/contract.md` (grep only); `corpus/SOURCES.md`; `corpus/lessons/round-20.md`; `corpus/knowledge/drift-repin-r20.md`; `corpus/knowledge/wave-settlement-r20.md`; the registry's used-by targets (id scan); `build/` names and counts for `Src*.md`.
- Network: GET of the GitHub raw README at the pinned commit, `ftp.gnu.org` bash-5.3.tar.gz (11,355,854 bytes, held in memory only), docs.python.org (os, pathlib), michaelfeathers.silvrback.com, kubernetes.io, en.wikipedia.org.
- Scratch: `/tmp/sc-r20/` (`before-SOURCES.md`; `now-SOURCES.md` = HEAD copy; `before-tree/` = git archive of 2061780, about 60 MB). Writes to the lane: none. The only lane file I wrote is this report.
