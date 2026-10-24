judge-role: reviewer
judge-seat: JudgeRecheck
judged-sha256: 251bf664717bbdf4c6c99ccde5cc33607b08f03550a0bd913168be2c5a348407
judged-revision: 837b2802c60a6e37a9d462f2354107307fba6ef1

- S001: agree
- S002: agree
- S007: agree
- S012: agree
- S014: agree
- S015: agree
- S031: agree
- S037: agree
- S039: agree
- S040: agree
- S041: agree
- S043: agree
- S044: agree
- S045: agree
- S046: agree
- S047: agree
- S049: agree
- S051: agree
- S052: agree
- S056: agree
- S058: agree
- S062: agree
- S064: agree
- S067: agree
- S068: agree
- S069: agree
- S071: agree
- S073: agree
- S074: agree
- S076: agree
- S117: agree
- S128: agree
- S137: agree
- S149: agree

## Reasons

- S001: Q1 trend windows over ten/sixty/three-hundred seconds + Q2 "total absolute stall time (in us)" + Q3 trigger de-registers when its fd closes are verbatim in the copy and carry both teaches halves (trend-vs-microsecond distinction; fd-bound trigger lifetime).
- S002: Q1 "all fields in this file are hierarchical" (memory.events), Q2 events.local "not hierarchical", Q3 oom_kill "killed by any kind of OOM killer" — each teaches clause sits verbatim in context.
- S007: Q1 "select a cgroup to terminate, and send SIGKILL to all processes in it", Q2 descendant-eligibility, Q3 PSI polling — the teaches sentence is carried piecewise in context.
- S012: Q1 impact sentence names the missing path traversal validation; Q2 "Affected versions >= 250 Patched versions 261 260.3 259.7 258.9" — the version-bounding teach is the advisory's own fields.
- S014: Q1 Source Options lead-in, Q2 --after-cursor definition, Q3 --output-fields definition — scope/cursor/field-selection halves all carried.
- S015: Q1 MESSAGE "primary text shown to the user" (context: "not supposed to be parsed for metadata"), Q2 MESSAGE_ID 128-bit identifier, Q3 underscore-prefixed = trusted — all three clauses verbatim.
- S031: Q1 and Q2 are adjacent halves of the literal "read end closed → write causes SIGPIPE" sentence.
- S037: Q1 UNIT=/USER_UNIT= "used by the system and user managers when logging about specific units"; Q2+Q3 reassemble the _SYSTEMD_UNIT sentence "of the process the journal entry originates from" (that phrase occurs in that sentence; occ=6 across the page) — both halves carried.
- S039: Q1 "seek to the next closest entry (in terms of time)" and Q2 "do not actually make any entry the new current entry" — the teach verbatim.
- S040: Q1 multi-cursor non-identity, Q2 test-cursor purpose after seek, Q3 next-closest seek — carried; "no dedup/completeness implied" is lane scoping the page does not contradict.
- S041: Q1 429 rate-limiting definition, Q2 the spec "does not define how the origin server identifies the user", Q3 Retry-After — carried; vendor/permanence clauses are lane scoping.
- S043: Q1/Q2/Q3 are the literal 1302/1113/1308 rows of the error table, each tagged 429 on the live page — the cannot-distinguish teach follows from the page's own table.
- S044: Q1 "jj commands will usually put the Git repo in a \"detached HEAD\" state", Q2 the page's own "not concept" typo preserved verbatim, Q3 branches-absent-or-stale — carried; commit-id-vs-branch reading is the lane's inference from carried facts.
- S045: Q1 --update-author "Update the author to the configured user... author name and email", Q2 "The author timestamp is not modified" — both teaches halves verbatim.
- S046: Q1 --is-ancestor definition, Q2 "exit with status 0 if true, or with status 1 if not", Q3 "Errors are signaled by a non-zero status that is not 1" — exact.
- S047: Q1 -q "exit with non-zero status silently" on detached HEAD, Q2 NOTES "status 1... or 128 if another error occurs" — exact.
- S049: Q1 treatment-list intro, Q2 hashed session ids, Q3 "omit or safely replace that field... do not discard the entire security event" (context); File paths and Internal network names are in the page's own class list, so the paths/internal-names clause is grounded.
- S051: Q1 "should no longer be used or collected" with current-business-purpose test, Q2 periodic-review schedule, Q3 NARA-schedule disposal — all page-borne teaches parts carried; class-gate clause is lane scoping.
- S052: Q1 "Only collect data that serves an observability purpose", Q2/Q3 hash reversibility "if the input space is small and predictable"; the drop/truncate alternative is on the page beside Q3.
- S056: transcript shows three failed fetches in batch 1 (exit 22, HTTP 403, cf-mitigated: challenge) plus three more in batch 2 and a counter re-fetch yielding 0 bodies; no challenge passed — unreachable bar met.
- S058: quotes verbatim carry the ordering half (default reverse chronological, --topo-order parent-after-child, --reverse flips); the "Diff-tree:" half is a labelled summary of the companion doc named in the row's own source cell/anchor (seat re-fetched git-diff-tree live, unchanged) — no teach clause claims this page carries it, and nothing on the page contradicts it.
- S062: Q1 UTF-16 code-unit sorting, Q2 "Whitespace between JSON tokens MUST NOT be emitted", Q3 NaN/Infinity must terminate with error — verbatim; ES-number text and duplicate-name clauses are on the page (§3.2.2.3, §3.1), -0 and json.dumps clauses cite the errata/other rows in the teaches itself.
- S064: Q1 --verify raw-20-byte-SHA-1 + object check, Q2 --end-of-options advice, Q3 $REV^{commit} peeling example — the resolve-once teach carried; blob-binding half is the lane's own application.
- S067: Q1 "document your system's actual behavior, not check for the behavior you wish your system had", Q2 "descriptions of what we have rather than statements of correctness" — the teach verbatim; re-pin reading is lane application.
- S068: Q1 lstat "does not follow symbolic links", Q2 stat "normally follows symlinks; ... or use lstat()", Q3 follow_symlinks=False acts on the last-element link — exact.
- S069: Q1 PurePath "works with strings... does not check or access the underlying file structure", Q2 "assumes that no symlinks are present... call resolve() first", Q3 walk_up default semantics — page side carried; lexical-reject rule is the lane's tool rule (superseding S073 says so).
- S071: Q1 "spec field that represents the desired state", Q2 controllers "making the current state come closer to that desired state" — vocabulary carried; observe-only stance is the lane boundary the superseding S074 declares.
- S073: same URL/sha as S069; Q1-Q3 carry the string-only/symlink-caveat teach verbatim; the "mori's own tool rule" clause is self-declared as not taught by the page.
- S074: Q1 controllers close the gap, Q2 thermostat analogy, Q3 "control loops automatically fix failures" — desired/current vocabulary carried; the observe-only clause is self-declared lane boundary.
- S076: same URL/sha as S067; Q1 actual-not-desired sentence, Q2 immediate behavior-change detection on refactor — teach carried; sameness-vs-health clause self-declared lane application.
- S117: the three quotes are this JSON page's relevant payload — v1.9.0/v1.8/v1.7 entries each pinning name→commit.sha (202d4db0…/62625072…/ebaea952…); the wording-stability teaches pin their bytes to those very tags per the anchor, so the page's share (tag identity and order v1.7<v1.8<v1.9.0) is carried and nothing on the page contradicts the rest.
- S128: Q1 -1000..+1000 range, Q2 "added to the badness score" wording, Q3 inheritance+CAP_SYS_RESOURCE inside the oom_adj paragraph — the page-borne teach carried; the oom_score [0,2000]/scaling half cites fs/proc/base.c and the sibling page named in the row's own scope/anchor.
- S137: Q1 subject "kill: option for triggering kernel oom killer" and Q2 body sentence sit in commit 750a7c0d whose author (2026-02-02T05:00:04Z) and committer (2026-02-17T20:30:10Z) dates match the anchor — the February-2026 return is carried; v1.2-removal and --kernel-oom clauses are attributed to S114/S016 in the teaches cell and contradicted nowhere on the page (0 hits for v1.2/ignored).
- S149: Q1 3% root clause, Q2 inheritance/privilege placed only in the oom_adj paragraph, Q3 -1000..+1000 range — the page-borne parts of the superseding teach carried; kernel-code parts cite fork.c/base.c/oom_kill.c rows (S127/S003) in the teaches' own parentheticals.
