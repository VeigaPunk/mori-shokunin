# Mo55Scribe02 — audit of new source rows S526–S543 and the round-55 lesson Gate

Seat: scribe, report-only. Lane `mori-shokunin`, round 55, wave `w1`.
Measured data revision: `b8b7064c2b54c8b6b22c288232a96c43fae1af47` (contract: "measure the latter").
Entering tip `ca52426e`; freeze `c9b908f0`; HEAD at audit time `b8a70adf` ("publish w1 ready marker").
No production edits, no git/jj mutations, no installs, no pacman. Scratch `/fast/scratch/hyaku/mori-r55/Mo55Scribe02/`, removed before yield.

## What was audited

| surface | path at `b8b7064` | size |
|---|---|---|
| registry rows | `corpus/SOURCES.md:306-323` (S526–S543) | 18 rows |
| Gate table | `corpus/lessons/round-55.md:13-44` | 32 rows over 18 ids |
| C1 entry source line | `corpus/knowledge/kernel-v7.3-recheck-r55.md:3` | S526–S534 + S516 + S502 |
| C2 entry source line | `corpus/knowledge/disk-runway-enospc-r55.md:3` | S535–S543 |
| pinned copies | `corpus/evidence/sources-r55/` | 18 new copies (+6 reused v7.2) |

Method: parse the Gate table mechanically, resolve each cited `copy:line[-line]` against the committed copy, normalise whitespace (the counters' own `re.sub(r"\s+", " ")` rule), and compare. Then re-fetch every registry URL for the 18 rows and byte-compare against the pinned copies. Then run the lane's own read-only census validator and the CORPUS.md enum/tier awk.

## Gates run (command, outcome, exit)

1. `sha256sum` over the 18 new copies (cwd `corpus/evidence/sources-r55/`) → every digest equals the `sha256` cell in `corpus/SOURCES.md:306-323` and the pin in `count-c2.py:59-77` / `count-c1.py:61-96`. exit 0.
2. `curl -sS -L` of the 18 registry URLs (cwd scratch, output to `fetch/<id>.out`) → 18/18 HTTP 200; `sha256sum` of each fetched body equals the pinned copy byte-for-byte (sizes e.g. S526 98216, S527 231585, S533 135851, S538 81330, S543 683185). exit 0.
3. `curl .../linux.git/refs/tags` and `.../man-pages.git/refs/tags` → `v7.3` and `man-pages-6.19` both present (v7.3 is the highest v7 tag listed); `https://github.com/coreutils/coreutils/tree/v9.12` → 200. exit 0.
4. Gate location check at `b8b7064` (scratch `audit_gate.py` + span resolver) → 32/32 rows located at the cited copy line; 0 rows exceed 25 words (max 22, min 1); 18/18 ids S526–S543 present; 32/32 decision cells read `admit, tier A`.
5. `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` → 23 `W04` duplicate-URL warnings, all on pre-existing ids (S035…S492), none on S526–S543; final line `mori ok …/corpus/SOURCES.md`; no E01–E12. exit 0. Identical to the committed receipt `evidence/census-end.txt` (25 lines, `exit=0`).
6. CORPUS.md enum/tier awk on `corpus/SOURCES.md` → no output (no tier/status/kind violation, no community-at-A). exit 0. Duplicate-id check → none. Row field-count check (`NF==13`) → none malformed.
7. Per-source usage derived from the entries: C1 = 78 rows (S502 1, S516 14, S526 6, S527 2, S528 2, S529 9, S530 34, S531 1, S532 1, S533 7, S534 1); C2 = 23 rows (S535 1, S536 2, S537 4, S538 5, S539 2, S540 4, S541 2, S542 2, S543 1). Every one of the 18 rows is used by at least one claim row, and both front-matter source lines match those sets.
8. `git diff b8b7064 -- corpus/lessons/round-55.md corpus/knowledge/disk-runway-enospc-r55.md` → 2 uncommitted one-line corrections (finding F9 below). `git diff b8b7064 -- corpus/evidence/sources-r55/` → empty; the copies are unchanged since the freeze.

## Behavior

- URLs: all 18 are tag-pinned primary URLs (`?h=v7.3`, `?h=man-pages-6.19`, `v9.12`); no branch, homepage, private or credential-bearing URL. Live bytes equal the pins, so the registry URL→copy binding is verified today, not merely asserted.
- Tier: every row is `A` with kind `code` (9) or `docs` (9). By source class (kernel source and kernel Documentation at tag v7.3, official man-pages 6.19 man2/man3, GNU coreutils 9.12 official manual) tier A is justified; the census E10 check is silent. The defect is not tier inflation but scope (F2/F3).
- Gate: the rule-1 record (URL, access date 2026-10-27, ≤25-word located quote) is present for all 18 ids; every quote is a true substring of its committed copy at the cited line.
- Gate quote provenance across commits: at the freeze `c9b908f0` the lesson had zero Gate rows; the table landed at `121093e2` ("land release recheck and ENOSPC runway entries") and two quotes were widened to complete source statements at `f70051dd` (S537 1002-1003 → 999-1003; S538 `will not fit` → `will * not fit`). Both pre- and post-widening forms locate; the widening is an improvement, not a regression.

## Findings

**F1 — medium — registry anchors for all 18 new rows carry no section/line locator.**
`corpus/SOURCES.md:306-323` anchor cells read only `tag v7.3; copy …; sha256 …; copy corpus/evidence/sources-r55/…`. CORPUS.md (registry rules, anchor bullet) requires "exact section / heading / page / line plus revision", and the lane's own precedent does that: `corpus/SOURCES.md:281` (S502 `meminfo section lines 1043-1302`), `:287` (S508 `sysctl_overcommit_memory/ratio/kbytes defaults 781-783, …`), `:295` (S516 `quote lines 424, 446, 465, …`). The line locators for the new rows exist only in the lesson Gate, so a reader of the registry alone cannot locate the row's evidence.
Evidence: `corpus/SOURCES.md:306-323` versus `corpus/SOURCES.md:281,287,295`.

**F2 — medium — nine rows share one boilerplate scope, so tier A is scoped to nothing checkable.**
`corpus/SOURCES.md:315-323` (S535–S543) all carry the identical scope cell `read-only filesystem block and inode runway, as applicable`. Tier is defined as "scoped to `scope`" and scope as "the claim or topic the tier applies to"; "as applicable" is not a topic, and nine sources with distinct contributions (errno constant, VFS statfs mechanics, XFS handler, btrfs statfs, btrfs sysfs, tmpfs doc, statfs(2), statvfs(3), df docs) cannot share one scope without the per-row A claim becoming unverifiable. Precedent keeps scopes row-specific (`:281`, `:287`, `:295`).
Evidence: `corpus/SOURCES.md:315-323`.

**F3 — medium — S535's anchor overstates what the pinned copy contains.**
`corpus/SOURCES.md:315` anchor claims `tag v7.3, pertinent statfs/space/inode definitions`. The copy `corpus/evidence/sources-r55/errno-base.h.v7.3` is 40 lines with 35 `#define` lines; the only pertinent definition is `#define ENOSPC 28 /* No space left on device */` at line 32. It contains no statfs, statvfs, inode or EDQUOT definition (`grep -n "statfs\|statvfs\|inode\|EDQUOT\|ENOSPC"` returns line 32 only). The row is authoritative for the ENOSPC errno value, not for a block/inode runway; the anchor wording should name the single definition.
Evidence: `corpus/SOURCES.md:315`; `corpus/evidence/sources-r55/errno-base.h.v7.3:32` (file 40 lines, 35 defines).

**F4 — low-medium — three Gate quotes are single tokens and do not ground their row's `teaches`.**
`corpus/lessons/round-55.md:15` S528 `TRACE_EVENT(mark_victim,` — teaches "OOM trace-event definitions and field schema", but the schema lives at `include_trace_events_oom.h.v7.3:79-92` (`TP_STRUCT__entry` fields) and is unquoted.
`:18` S531 `PSI_IRQ_FULL,` — teaches "PSI resource/state enums", but the quoted member sits inside `#ifdef CONFIG_IRQ_TIME_ACCOUNTING` (`include_linux_psi_types.h.v7.3:63-66`) and the state set it belongs to (`enum psi_states`, lines 57-70) is unquoted; a config-gated member is the weakest possible witness for "enums".
`:20` S533 `  memory.pressure` — teaches "cgroup v2 pressure files and cgroup.pressure switch", but the quote is the memory pressure file name at `Documentation_admin-guide_cgroup-v2.rst.v7.3:1938`; the `cgroup.pressure` switch is at line 1066 and is unquoted.
Each is located and under 25 words, so the mechanical arm passes; the grounding arm does not.
Evidence: `corpus/lessons/round-55.md:15,18,20`; copies cited above.

**F5 — low — twelve single-line locators cite a quote that spans 2–5 source lines.**
Exact spans at `b8b7064`: S536:62→62-63, S536:67→67-68, S541:42→42-43, S541:45→45-46, S542:228→228-232, S542:233→233-234, S537:919→919-920, S537:952→952-954, S537:955→955-956, S539:897→897-902, S539:677→677-679, S540:95→95-96. In every case the cited line does start the quote, so each row is located; the locator just understates the span (the lane already uses the range form where it noticed, e.g. S537:999-1003 at `round-55.md:30`).
Evidence: `corpus/lessons/round-55.md:23,24,25,26,27,28,31,32,33,39,40,43`.

**F6 — low — six titles embed the local copy filename instead of the upstream repo path.**
`corpus/SOURCES.md:315-320` read "Linux errno-base.h.v7.3 at tag v7.3", "Linux statfs.c.v7.3 at tag v7.3", "Linux xfs_super.c.v7.3 at tag v7.3", "Linux btrfs_super.c.v7.3 at tag v7.3", "Linux btrfs_sysfs.c.v7.3 at tag v7.3", "Linux tmpfs.rst.v7.3 at tag v7.3", while `:306-314` use the upstream path ("Linux fs/proc/base.c at tag v7.3"). The upstream path is not recoverable from the title for the six (e.g. `fs/xfs/xfs_super.c`, `fs/btrfs/super.c`); only the URL supplies it. The tag suffix appears twice in those titles.
Evidence: `corpus/SOURCES.md:315-320` versus `:306-314`.

**F7 — low — all 18 `teaches` cells are one template with the filename substituted.**
`:306-314` repeat "Rechecks the v7.2 … source pointers at the current pinned kernel release"; `:315-323` repeat "Grounds the round-55 ENOSPC and disk-runway interpretation in Linux <file> at tag v7.3". CORPUS.md asks for "one grounded learner benefit"; these restate provenance and the source name, so the registry does not say what a reader learns from each row. Precedent rows state a topic (`:281`, `:287`).
Evidence: `corpus/SOURCES.md:306-323`.

**F8 — low-medium — the tokens S533, S534 and S539 already denote different sources elsewhere in the lane record.**
`corpus/lessons/round-50.md:59` names "S533 (docs), S534 (own-work)" and "S539 (own-work)" as staged ids of unrelated entries; `:74` records the collision check `grep -cx` of S533/S534/S539 against `reg-ids` → 0 each; `:79` repeats the staged set. `corpus/SOURCES.md:268` (S489 anchor) states "adopts staged S533 renumbered by document". The registry now assigns S533 to cgroup-v2.rst v7.3, S534 to kernel/fork.c v7.3 and S539 to fs/btrfs/sysfs.c v7.3. The staged ids were never registry ids, so "never reused" is not broken, but the round-50 collision check is now stale and a cross-document lookup of "S533" resolves to the wrong source.
Evidence: `corpus/lessons/round-50.md:59,74,79`; `corpus/SOURCES.md:268,313,314,319`.

**F9 — info — the working tree carries an uncommitted correction to the S541 row and its C2 claim.**
At `b8b7064`, `corpus/lessons/round-55.md:25` cites `statfs.2.man-pages-6.19:42` with a quote truncated mid-line (`… /* Free blocks available to`), and `corpus/knowledge/disk-runway-enospc-r55.md:14` says "unprivileged process". The uncommitted working-tree edit changes the locator to `43-44`, narrows the quote to `fsblkcnt_t f_bavail; /* Free blocks available to unprivileged user */`, and changes the claim word to "user". Both versions locate against the copy; the edit is a correction, but the lesson and entry are being edited during the wave, so seats reading them see different text than `b8b7064`.
Evidence: `git diff b8b7064 -- corpus/lessons/round-55.md` (line 25) and `-- corpus/knowledge/disk-runway-enospc-r55.md` (line 14).

**F10 — info (named limit, not a defect) — the Gate table did not exist at the freeze.**
`git show c9b908f0:corpus/lessons/round-55.md` contains zero `| S5xx` rows; the table landed at `121093e2` and was tightened at `f70051dd`. The freeze therefore pinned copies and counters before the rule-1 quote record existed, so quote-to-copy agreement can only be audited after the freeze, never inside it.
Evidence: commit order `c9b908f0` (03:04) → `121093e2` (03:26) → `51ebd3d3` (03:32) → `f70051dd` → `b8b7064c` (03:33:50); `git show c9b908f0:corpus/lessons/round-55.md`.

## Out of scope for this seat

- No C2 entailment judgment on the 23 claims and no C1 line/status re-derivation (voter and reviewer seats own those); this seat emitted no vote line.
- No review of the host snapshot, the quarantine slice, assimilation, or the census row counts beyond registry validity.
- No edits to product code, corpus, counters, judge, or sibling lanes; no commit, push, or publish.

## Known limits

- The URL check is a 2026-10-27 observation of live bytes; it shows the tag URLs currently resolve to the pinned bytes, not that a tag can never move. The sha256 pins, not the URLs, are the durable binding.
- Whitespace normalisation follows the counters' own rule, so a quote that spans lines is judged located; it does not test that the quoted span is a complete syntactic statement.
- Severity is this scribe's curation, not a contract verdict.
- Uncommitted work by other seats can change these files after this audit; the revision measured is named above.

## Findings (severity · evidence)

- medium · F1 anchors without line locators — `corpus/SOURCES.md:306-323` vs `:281,287,295`
- medium · F2 boilerplate scope over tier A — `corpus/SOURCES.md:315-323`
- medium · F3 S535 anchor overstates the copy — `corpus/SOURCES.md:315`; `corpus/evidence/sources-r55/errno-base.h.v7.3:32`
- low-medium · F4 single-token Gate quotes fail grounding — `corpus/lessons/round-55.md:15,18,20`
- low · F5 single-line locators for multi-line quotes — `corpus/lessons/round-55.md:23-28,31-33,39,40,43`
- low · F6 titles embed copy filenames — `corpus/SOURCES.md:315-320`
- low · F7 templated `teaches` cells — `corpus/SOURCES.md:306-323`
- low-medium · F8 S533/S534/S539 token collision — `corpus/lessons/round-50.md:59,74,79`; `corpus/SOURCES.md:268`
- info · F9 uncommitted S541 correction — `corpus/lessons/round-55.md:25`; `corpus/knowledge/disk-runway-enospc-r55.md:14`
- info · F10 Gate table postdates the freeze — `git show c9b908f0:corpus/lessons/round-55.md`

Verified clean: 18/18 URL bytes = pins; 18/18 registry sha256 = copies; 32/32 Gate rows located and ≤25 words; 18/18 ids covered by ≥1 claim row; census validate exit 0 with no new warning; no duplicate id, malformed row, or tier/kind/status violation.
