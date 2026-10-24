# ReopenS137 — re-open of SOURCES row S137 at tip 5f00fd04

Seat: MoriR27.ReopenS137 (leaf; no subagents; no background jobs). Lane: mori-shokunin.
Tip: `5f00fd045c137b7e3835506d69946cfd9d010eb5` (branch master; committed 2026-10-22 13:07:05 -0300).
Verdicts are recommendations for MoriR27. I edited nothing in the lane.

Basis: tip bytes. The row (corpus/SOURCES.md:143), the Gate row (corpus/lessons/round-27.md:80),
the D2 row (round-27.md:107) and the entry (corpus/knowledge/userspace-oom-killers-r26.md) are
byte-identical at the tip and in the working tree (§1.3). The whole files corpus/SOURCES.md and
round-27.md differ from the tip (uncommitted edits; not reviewed here).

Labels used below: **B** = raw `750a7c0d…/main.c`; **D** = raw `v1.9.0/main.c` (S119's URL);
**E** = raw `v1.9.0/README.md` (S114's URL); **P** = raw parent `9808c759…/main.c`;
**F** = raw `8477c902…/README.md` (S016's URL); **G** = raw `master/main.c`;
**A** = the row's commits URL as written; **C** = the same URL with `&per_page=100`;
**H** = the pulls endpoint for commit 750a7c0d. `B:352` means line 352 of B.

## 0. Summary

- **Hash: consistent.** main.c@750a7c0d sha256 `d24a26c9…028df3e` is the row's value
  (SOURCES.md:143), the wave-1 value (w1/ReviewS117.md:30) and my fetch of B. The Gate row
  records no hash. No hash conflicts.
- **Anchors (22 checked, §3):** 20 hold in the bytes, 2 of them with attribution gaps.
  1 is **wrong as written**: the commits URL the row names does not return the "first page of
  100" the anchor describes. 1 is **unsupported**: "merge dates" (scope cell), because the
  commit has one parent, no pull request and a committer date.
- **Citing statements (7 hits, §6):** "merged 2026-02-17" is **unsupported** at entry:1, entry:139
  and entry:301; the row's scope says "merge dates" for the same claim (SOURCES.md:143). Entry:136
  cites "(§3.3)", a section that does not exist. round-27.md:107 "F7 cites both" is **ambiguous**.
  The Gate row (round-27.md:80) holds. The F7 dates (entry:135), the line anchors (entry:300-302) and the
  correction's account of the old line 1 hold.
- **Teaches (§4):** holds except the arrival month "returned on master in February 2026",
  which the bytes do not fix (lower bound only).
- **Duplicate check (§5):** not a duplicate of any older row's file.
- **Severity.** High: none. Medium: M1 "merged" (unsupported); M2 the named URL does not give
  the anchor's page (wrong); M3 the v1.9.0 `main.c:245-246` anchor is attributed to no row id and
  lies outside S119's declared scope. Medium, adjacent: the dangling "(§3.3)" pointer in the F7
  sentence that cites S137. Low: G4 (S114 `README.md:416` not in S114's anchor cell); the row
  title "option history" is wider than the row's own bytes; "absence" wording; "so" causal
  wording; "F7 cites both".

## 1. Receipts

### 1.1 Fetches (plain `curl -sS -L`; no browser; no challenge; access date 2026-10-22, UTC)

| Label | URL | Access | HTTP, bytes | sha256 | Use |
|---|---|---|---|---|---|
| A | https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c (the row's URL as written) | 17:10:53 | 200, 102,214 | 4ddcb62264287f8f372ccd84b0911ab7892e0dd045f5999d62dbf2e217a818f8 (receipt) | 30 entries on page 1 (default per_page) |
| B | https://raw.githubusercontent.com/rfjakob/earlyoom/750a7c0d97bb01c1bdf126fd6bf5722da17e8998/main.c | 17:10:54 | 200, 22,755 | d24a26c97744458706a870ee3eb1ddcd5e5f05dda11fe22a71d6a4952028df3e | row hash; 585 lines (`wc -l`) |
| C | https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c&per_page=100 | 17:11:31 | 200, 339,466 | e61fc1cee37ea703e2309cc10311be13e4b6d537ea8769d78275980e44921452 (receipt) | 100 entries (the anchor's page) |
| D | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c | 17:11:31 | 200, 21,053 | 08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4 | 552 lines; equals S119 (SOURCES.md:125) |
| E | https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md | 17:11:31 | 200, 19,931 | 23411dbfd8b409d433f984a5d6677830e86a383ec76935fc1e1d675e6b4374dd | 427 lines; equals S114 (SOURCES.md:120) |
| P | https://raw.githubusercontent.com/rfjakob/earlyoom/9808c7599596ef0d5a9c333f6fa346db8778f144/main.c | 17:12:19 | 200, 21,053 | 08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4 | parent of 750a7c0d; identical to D |
| F | https://raw.githubusercontent.com/rfjakob/earlyoom/8477c902fce09be26e5668acba05df216871e7ae/README.md | 17:12:02 | 200, 20,121 | b2a34e354d122fd756672a1a4014ec5382144e41451291c9d84fd6458c30826c | S016's URL (SOURCES.md:22) |
| G | https://raw.githubusercontent.com/rfjakob/earlyoom/master/main.c | 17:12:03 | 200, 22,853 | baeb78a6e45037ba17901b6897b780f3997687db61d23c7811b424fa99264370 | same hash as w1/ReviewS117.md:29 |
| H | https://api.github.com/repos/rfjakob/earlyoom/commits/750a7c0d97bb01c1bdf126fd6bf5722da17e8998/pulls | 17:13:56 | 200, 2 (`[]`) | 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945 | zero pull requests |

The GitHub API quota (unauthenticated, 60 per hour, shared with other seats) read 42 remaining
at 17:10:53 and 23 remaining at 17:13:56. I made no further API calls.

### 1.2 Other receipts

- w1/ReviewS117.md:26 records the same per_page=100 query as 403,197 bytes, sha256
  `e21b1c77…7533`. Today's C is 339,466 bytes, `e61fc1ce…1452`. The list is live. The row records
  no JSON hash, so no S137 claim depends on it (§8).
- The Gate block for the commit (w1/ReviewS117.md:185-188) gives the commit id, author date,
  committer date and subject. A matches all four (§3 rows 3-6).

### 1.3 Tip against working tree (read-only: `git rev-parse`, `git hash-object`, `git grep`, `git show`)

- corpus/SOURCES.md, whole file: tip `293f09c88835`, working tree `ab0a892a28f0`: DIFFERENT.
  The cited rows are identical. Prefix of the sha256 of each row line, tip = working tree:
  S016 `c5812bc1e42772ad`; S114 `93006460ab7b81c3`; S117 `136dbe535711216d`;
  S119 `04d85cef3b91125c`; S137 `47a2a3ee84bd7a33`.
- corpus/lessons/round-27.md, whole file: tip `f0201c6cc491`, working tree `9e10fef181a8`:
  DIFFERENT. The cited lines are identical. Prefix of the sha256 of each line set, tip = working
  tree: `^| S137 ` (:80) `942ab1056428df1f`; `^| S138` (:81) `c7ade208d22ab02b`;
  `r26 D2 S117` (:107) `17cf77a1f68dc570`.
- corpus/knowledge/userspace-oom-killers-r26.md: identical (`255937774e6a`).
- .ufo/waves/round-27/w1/ReviewS117.md: identical (`ef31b01c5690`).

### 1.4 Tooling and seat tools

- No installs or updates. Pre-existing tools used: curl 8.23.0; python3 3.14.8 (JSON parsing and
  substring checks only); git 2.56.0 (read-only verbs only); sha256sum; wc; grep; cut.
  `jq` on this host is jaq 3.1.1 and was not used. No pacman transaction.
- The operator's tooling directive was read before the first fetch. No installation was needed.
- lsp: this seat's tool list has no lsp device. No semantic reference check was run. The main.c
  checks are literal `grep -n` and python substring checks on bytes, not semantic proof.

## 2. The row at the tip (SOURCES.md:143)

Cells: kind code; tier A; status mined; opened 2026-10-22; recheck on-release; used-by
`corpus/knowledge/userspace-oom-killers-r26.md` (the only entry that uses it).
Its only URLs are A and B. Its scope and teaches cite other rows' bytes: S114 (E, lines 383 and
416), v1.9.0 `main.c:245-246` (D, named without a row id), and S016 (F).

## 3. Anchors, one by one

| # | Row says | Bytes say (where) | Verdict |
|---|---|---|---|
| 1 | commits query "first page of 100" (anchor cell) | A, the URL as written: 30 entries (the default per_page). Author dates 2021-08-09T15:40:59Z to 2026-10-15T17:31:12Z. Commit 750a7c0d is entry 5. | **WRONG** for the URL as written. Fix K2. |
| 2 | "first page of 100, 2018-07-16 to 2026-10-15" | C: 100 entries. Author dates 2018-07-16T07:04:01Z (oldest, `ff1c7df335`) to 2026-10-15T17:31:12Z. Committer dates run to 2026-10-17T18:34:22Z. | HOLDS for C. The range is author dates; the anchor does not say so (low). |
| 3 | commit 750a7c0d97bb01c1bdf126fd6bf5722da17e8998 | A, entry 5 | HOLDS |
| 4 | author date 2026-02-02T05:00:04Z | A, `commit.author.date` | HOLDS |
| 5 | committer date 2026-02-17T20:30:10Z | A, `commit.committer.date`. One parent (`9808c759…`). The committer account is the repository owner's; the author account is a different one. H shows no pull request for this SHA. | HOLDS as a **committer** date. Not a merge date (M1). |
| 6 | subject "kill: option for triggering kernel oom killer" | A, first line of the message; exact string match | HOLDS |
| 7 | main.c:201 longopts "kernel-oom" | B:201 `{ "kernel-oom", no_argument, NULL, LONG_OPT_USE_KERNEL_OOM },` | HOLDS |
| 8 | main.c:315-317 case; flag; "Using kernel OOM killer (requires Linux v5.17+)" | B:315 `case LONG_OPT_USE_KERNEL_OOM:`; B:316 `args.kernel_oom = true;`; B:317 `fprintf(stderr, "Using kernel OOM killer (requires Linux v5.17+)\n");` | HOLDS |
| 9 | main.c:352 help "use kernel OOM killer via /proc/sysrq-trigger" | B:352 `"  --kernel-oom              use kernel OOM killer via /proc/sysrq-trigger\n"` | HOLDS |
| 10 | Gate quote `:352` (round-27.md:80) | Byte-exact. The Gate string, outer quote marks included, is a substring of B:352 (python; one hit, line 352). | HOLDS |
| 11 | main.c:437-438 threshold line variant | B:437 `if (args.kernel_oom) {` inside main() (main starts at :147; the next function starts at :462). B:438 `fprintf(stderr, "triggering kernel oom when mem avail <= " PRIPCT …`. | HOLDS |
| 12 | main.c:553-554 poll-loop trigger | B:553 `if (args->kernel_oom) {`; B:554 `trigger_kernel_oom(args);` inside poll_loop (defined at :534). | HOLDS |
| 13 | main.c@750a7c0d sha256 d24a26c9…028df3e | B | HOLDS (= w1/ReviewS117.md:30) |
| 14 | 585 lines | B: `wc -l` = 585; the last byte is a newline | HOLDS |
| 15 | opened 2026-10-22 | all fetches 2026-10-22, 17:10:53Z to 17:13:56Z | HOLDS |
| 16 | scope: S114 README.md:383 | E:380 `* v1.2, 2018-10-28`; E:383 `  * Remove option to use kernel oom-killer (`-k`, now ignored for compatibility)` | HOLDS. S114's anchor cell lists 383 (SOURCES.md:120). |
| 17 | scope: S114 README.md:416 | E:416 `* v0.6: Add command-line options `-m`, `-s`, `-k`` | HOLDS in the bytes. S114's anchor cell does not list 416 (SOURCES.md:120 lists `65-67,383,289-293`). Gap G4. |
| 18 | scope: "v1.9.0 main.c:245-246" | D:179 `const char* short_opt = "m:s:M:S:kingN:P:dvr:ph";`; D:245 `case 'k':`; D:246 `fprintf(stderr, "Option -k is ignored since earlyoom v1.2\n");` | HOLDS in the bytes. These are S119's bytes (D's hash is S119's). S137 names no v1.9.0 URL. S119's declared scope (SOURCES.md:125) does not name the message. Gap M3. |
| 19 | scope: "the master re-introduction commit" | P's hash equals D's hash. P has 0 matches for `kernel-oom`; B has two (B:201 and B:352, the help line). In A, no main.c commit sits between fbe2b6ba43 (committer 2025-09-13) and 750a7c0d (committer 2026-02-17). | HOLDS: 750a7c0d is the first main.c change that re-adds the option after v1.9.0. |
| 20 | scope: "its author and merge dates" | Author date: row 4. "Merge": row 5 and M1. | **UNSUPPORTED** for "merge" (M1). |
| 21 | scope: "not the option's runtime behaviour on any host, not the v1.7-v1.9.0 log grammar (S117)" | An exclusion. The S117 row (SOURCES.md:123) covers the grammar. | HOLDS |
| 22 | scope: "the v0.6 introduction and v1.2 removal" | Composed from rows 16 and 17: E:416 adds `-k` in v0.6; E:383 names `-k` as the kernel oom-killer option removed in v1.2. | HOLDS as a composition |

Totals: 20 hold in the bytes (rows 2-19, 21-22, with rows 17 and 18 carrying attribution gaps);
1 wrong (row 1); 1 unsupported (row 20).

## 4. Teaches, sentence by sentence (SOURCES.md:143)

1. "The kernel-OOM delegation option left earlyoom in v1.2" — **HOLDS** (E:380-383).
2. "and returned on master in February 2026" — **UNSUPPORTED as an arrival month.** The bytes give
   the author date 2026-02-02 and the committer date 2026-02-17. The commit is on master today
   (A lists it on the default branch; G returns a master file). The committer date is a lower
   bound on when the commit could reach master, not a fixed arrival date. Fix K8.
3. "so a 1.9.0 binary prints 'Option -k is ignored since earlyoom v1.2'" — **HOLDS at source
   level.** D:179 includes `k` in the short-option string; D:195 passes it to getopt_long; D:245-246
   print the message. The compiled binary was not built or run; that part is [INFERENCE]. "so"
   reads as a cause; the 2026 return does not cause the 1.9.0 message (wording, low).
4. "while current master grows a --kernel-oom long option" — **HOLDS today:** G:46
   `LONG_OPT_USE_KERNEL_OOM,`; G:202 the longopt; G:316 the case; G:353 the help line.
5. "(S016 documents it from the master README)" — **HOLDS:** F:68 "You can make earlyoom trigger
   the kernel oom killer (`echo f > /proc/sysrq-trigger`)" and F:69 "by passing the `--kernel-oom`
   flag. However, be aware of the following:". The S016 row names F (SOURCES.md:22).
6. "delegation claims must name the build they hold for" — a rule, not a fact; no verdict.

Scope note (low): the row title "earlyoom kernel-oom option history" is wider than the row's own
bytes, which are one commit page and one file. The history is completed by S114 and S119 bytes.

## 5. Duplicate check

- Tip grep (`git grep -n -E '750a7c0d|d24a26c9|commits\?path' 5f00fd04 -- corpus`) returns seven corpus
  hits: the S137 row (SOURCES.md:143); entry lines 1, 139, 296 and 300; round-27.md:80; and
  round-26-verifier-spotcheck.md:149. The last is a round-26 finding that quotes the old S117 line 1
  (its commits query sits in the D2 description). It is neither a row, a Gate record nor an S137
  citation. No SOURCES row other than S137 names commit 750a7c0d, the file hash `d24a26c9`, or the
  commits query.
- Rows whose URLs name a main.c file: S117 (v1.9.0, v1.8 and v1.7 main.c; SOURCES.md:123), S119
  (v1.9.0 main.c; :125), S137 (750a7c0d main.c; :143). None holds the `d24a26c9` file. S119's file
  (`08656b0b…`) is the parent's file, not S137's file.
- **Not a duplicate.** Pre-existing overlap, not S137's: S117 and S119 both name v1.9.0 main.c.

## 6. Citing statements (`git grep -n 'S137'` at the tip; seven hits)

### S-0 SOURCES.md:143 (the row)
**Holds** for the hash, dates, line anchors and Gate. **Wrong** in M2 (the named URL) and
**unsupported** in M1 ("merge dates"). Attribution gaps M3 and G4. Fixes K1-K4 and K8.

### S-1 userspace-oom-killers-r26.md:1 (source line)
"S137 (earlyoom kernel-oom option history — …commits?path=main.c and …750a7c0d…/main.c — the v1.2
removal of the kernel-oom option (S114, README.md:383) and its re-introduction on master,
authored 2026-02-02, merged 2026-02-17; opened 2026-10-22)"
- Both URLs: identical to the row. **Holds.** The line makes no page claim, so M2 does not reach it.
- "(S114, README.md:383)": **holds** (E:383).
- "its re-introduction on master": **holds** (row 19).
- "authored 2026-02-02": **holds** (row 4).
- "merged 2026-02-17": **unsupported** (M1). Fix K1.

### S-2 userspace-oom-killers-r26.md:135-136 (F7 verdict)
"the absence of the option is verified on the tag's sources (`main.c:245-246` at v1.9.0; the v1.2
removal is S114's README.md:383 anchor; the option-history dates are S137's) and on the installed
binary's bytes (§3.3)."
- "`main.c:245-246` at v1.9.0": **holds** in the bytes (D:245-246); unattributed (M3). Fix K3.
- "the v1.2 removal is S114's README.md:383 anchor": **holds** (E:383; SOURCES.md:120).
- "the option-history dates are S137's": **holds** (rows 4-5).
- "the absence of the option is verified": **holds with a wording gap (low).** The cited lines
  show the `-k` ignore, which is evidence of removal. Absence of the long option is a negative
  check: `kernel-oom` has 0 matches in D (552 lines). Fix K7.
- "(§3.3)": **wrong pointer (medium, adjacent).** The entry has no §3. Its section headers sit at
  :8, :26, :186, :204, :232, :254, :269, :279 and :293. No committed file under
  `.ufo/waves/round-26/capture/` contains "ignored since"; the tip grep lists only wave drafts and reports,
  corpus/SOURCES.md and the entry. The installed-binary clause therefore has no
  surviving anchor. Fix K5.

### S-3 userspace-oom-killers-r26.md:139 (F7 limit)
"Upstream master has carried a kernel-OOM trigger option again authored 2026-02-02 and merged
2026-02-17 (S137, commit `750a7c0d`)"
- "carried … again": **holds** (G:202; F:69).
- "authored 2026-02-02": **holds** (row 4).
- "merged 2026-02-17": **unsupported** (M1). Fix K1.
- Commit id: **holds**.

### S-4 userspace-oom-killers-r26.md:293-304 (dated correction; S137 cited at :300-302)
"authored 2026-02-02T05:00:04Z, merged 2026-02-17; `main.c` at that commit, lines 201, 315-317, 352),
with the v1.2 removal anchored on S114 (`README.md:383`) as that row already records."
- "authored 2026-02-02T05:00:04Z": **holds** (row 4).
- "merged 2026-02-17" (line 301): **unsupported** (M1). Fix K1.
- "lines 201, 315-317, 352": **holds** (rows 7-9).
- "as that row already records": **holds** (SOURCES.md:120 lists 383).
- The account of the old line 1 (:295-297): **holds.** The pre-fix line 1 at commit `327fbcc`
  (corpus/knowledge/userspace-oom-killers-r26.md:1) reads "S117 (earlyoom tag history —
  https://github.com/rfjakob/earlyoom/releases and https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c —
  the v1.9.0 tag and commit, …"; the correction's description matches.
- "the master-side claim was true but under-cited": **holds** (G:202; F:69).

### S-5 round-27.md:80 (Gate row)
URL = the row's raw URL; accessed 2026-10-22; quote `:352` byte-exact (§3 row 10); "admit, A,
mined (ReviewS117, routed D2)". **Holds.** w1/ReviewS117.md exists; its §5 routes the defect and
its §6 asks for a new row. This line does not carry the page size, so M2 sits in the row, not here.

### S-6 round-27.md:107 (r26 D2 row)
"fixed: the r26 entry's line-1 S117 description now matches the row; the kernel-oom option history
has its own row S137; F7 cites both; dated correction appended"
- "line-1 S117 description now matches the row": **holds in substance.** The entry's title equals
  SOURCES.md:123's title, and its two API URLs are in the row's list.
- "has its own row S137": **holds.**
- "F7 cites both": **ambiguous (low).** F7 (entry:123-141) cites S114 (:135) and S137 (:135, :139)
  and cites no S117 (0 matches in :123-141). It holds if "both" means S114 and S137; it is wrong
  if "both" means S117 and S137. Fix K6.
- "dated correction appended": **holds** (entry:293-304 is the last section).

## 7. Corrections, old → new (recommendations; none applied)

Rule 2 (quoted at w1/ReviewS117.md:118-120) lets a landed row change in place only in status,
recheck and used-by. Scope and anchor edits to a row therefore need a logged correction or a new
row, and the planner chooses which. Entry and round-27 lines are not rows; they can be edited in
place.

**K1 (M1, "merged" is unsupported).**
- SOURCES.md:143 scope: "the master re-introduction commit with its author and merge dates" →
  "the master re-introduction commit with its author date and committer date" [row; planner route]
- entry:1: "authored 2026-02-02, merged 2026-02-17;" → "authored 2026-02-02, committer date 2026-02-17 (one parent; no pull request);"
- entry:139: "authored 2026-02-02 and merged 2026-02-17 (S137, commit `750a7c0d`)" → "authored 2026-02-02 and committer-dated 2026-02-17 (S137, commit `750a7c0d`)"
- entry:301: "authored 2026-02-02T05:00:04Z, merged 2026-02-17;" → "authored 2026-02-02T05:00:04Z, committer date 2026-02-17T20:30:10Z;"

**K2 (M2, the named URL does not give the anchor's page).** Choose one:
- (a) Add the page size to the URL (keeps the 2018-07-16 boundary the anchor quotes). Row, planner
  route: SOURCES.md:143 "…/commits?path=main.c ;" → "…/commits?path=main.c&per_page=100 ;".
  Entry:1 "…/commits?path=main.c and" → "…/commits?path=main.c&per_page=100 and".
- (b) Keep the URL and fix the anchor. SOURCES.md:143 "(first page of 100, 2018-07-16 to 2026-10-15)" →
  "(first page at the default per_page of 30; author dates 2021-08-09 to 2026-10-15; 750a7c0d is its fifth entry)".

**K3 (M3, attribution of v1.9.0 main.c:245-246).**
- SOURCES.md:143 scope: "(S114 README.md:416,383; v1.9.0 main.c:245-246)" →
  "(S114 README.md:416,383; S119 main.c:245-246)"
- entry:135: "(`main.c:245-246` at v1.9.0;" → "(`main.c:245-246` at v1.9.0, the S119 bytes;"
- Planner note: S119's declared scope (SOURCES.md:125) does not name the `-k` message. Record that
  in a logged note or a new row; do not widen S119 in place.

**K4 (G4, S114 README.md:416 not in S114's anchor cell).** No S137 text change is needed. The
planner may add `:416` to S114's anchor cell by logged correction (SOURCES.md:120).

**K5 (adjacent, medium; "(§3.3)").** entry:136 "and on the installed binary's bytes (§3.3)." →
"and on the installed binary's bytes (no committed capture holds the string, so this clause is
unanchored)." The same installed-binary claim at entry:131-132 needs the same treatment; it does
not cite S137.

**K6 (low; "F7 cites both").** round-27.md:107 "F7 cites both;" → "F7 cites S114 and S137;"

**K7 (low; "absence" wording).** entry:135 "the absence of the option is verified on the tag's
sources (`main.c:245-246` at v1.9.0;" → "the option's removal is verified on the tag's sources
(`main.c:245-246` at v1.9.0 ignores `-k`, and no `kernel-oom` string appears in that 552-line file;"

**K8 (low; arrival month and causal "so").** SOURCES.md:143 teaches: "returned on master in
February 2026, so a 1.9.0 binary prints" → "returned in a commit authored 2026-02-02 and committed
2026-02-17 that is on master today, and a 1.9.0 binary prints"

## 8. Residual risk and verification gaps

- The commits list is live. C's receipt differs from ReviewS117's receipt for the same query
  (§1.2). Page membership moves as commits arrive. Commit 750a7c0d is entry 5 of the default page
  today. Re-check any position claim before re-citing it.
- The default branch is taken as master [INFERENCE]. The commits API lists the repository's default
  branch; G (the raw master file) returns 200, which is consistent with master being the default.
- H's "zero pull requests" means GitHub holds no pull-request record that contains this exact SHA.
  A change merged by another route (for example, re-applied under a new SHA) would not appear.
- I did not build or run earlyoom, and I did not run omp. "Prints" in teaches sentence 3 is a
  source reading; the compiled binary's behaviour is [INFERENCE].
- The installed host binary (F7's clause) was not read. It is outside S137 and no committed capture
  holds the string (§6, S-2).
- master has moved. Four later main.c commits (`d33c11c642`, `df3934ae7d`, `b335052cd8`,
  `c33a888693`) sit above 750a7c0d in A. S137 is pinned to 750a7c0d, which is correct. G is not
  B (their hashes differ). The teaches' "current master" is a present-tense claim checked today.
- No lsp check was possible in this seat (§1.4).
- No further API calls after H. The shared quota had 23 requests left at 17:13:56.

## 9. Privacy and retention

- No session identifiers, session-store paths, pids, uids, command lines, journal text or
  /etc/default values were read or written. Upstream people are named only by role (author,
  committer).
- The operator's tooling directive was read. Its path is not written here.
