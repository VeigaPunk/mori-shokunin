# ReviewHygieneD2 — routed D2 as landed at 5f00fd0, and QUALITY 77

Seat: MoriR27.ReviewHygieneD2 (leaf reviewer; no subagents, no background jobs).
Lane: mori-shokunin. Pins: landed tip `5f00fd045c137b7e3835506d69946cfd9d010eb5` (master); D2 landed in `79ecf58`; pre-fix entry at `126e192`. Every lane read was `git show <rev>:<path>`, `git log` or `git grep` (read-only). Scratch: `/fast/scratch/hyaku/mori-r27/ReviewHygieneD2/`.

Short names used below: `entry:N` = `corpus/knowledge/userspace-oom-killers-r26.md` line N at the tip; `SOURCES:N` = `corpus/SOURCES.md` line N at the tip; `r12U:N` = `corpus/knowledge/userspace-oom-killers-r12.md`; `r12C:N` = `corpus/knowledge/oom-kill-counter-kernel-only-r12.md`; `lesson:N` = `corpus/lessons/round-27.md`; `w1:N` = `.ufo/waves/round-27/w1/ReviewS117.md`; `draft:N` = `.ufo/waves/round-26/w1/DraftEntryR26.md`.

## Summary

D2 is landed in substance. Line 1 now quotes the S117 row's title, its tags and releases URLs and its scope. The kernel-oom history has its own row S137, and every S137 anchor and date I checked against upstream bytes is right. The S117 row is byte-identical to its first publication (`327fbcc`). I found no high-severity defect. Three medium defects are standing contradictions or dangling pointers under QUALITY 77 (M1–M3). Two low-to-medium items concern dates: an unsupported "merged" label, with a correction sentence that says nothing was retracted when something was (L1), and an immutable S114 date that conflicts with S137 (L2). The rest is low or info.

## Findings by severity

### M1 (medium) — dangling section pointers; the critic-named "(§3.3)" was not fixed

- Facts: the landed entry's headings sit at lines 6, 8, 26, 186, 204, 232, 254, 269, 279 and 293. It has no §3 and no §4. The pointers still standing are `entry:41-42` (§3.1), `entry:74`, `entry:107`, `entry:118`, `entry:180` (§3.2), `entry:136` (§3.3) and `entry:252` (§4.2).
- The round-26 draft held those sections: §3.1 host state (`draft:330`), §3.2 journal census (`draft:355`), §3.3 the round-26 tool (`draft:394`), §3.4 the installed binary (`draft:404`), §4.2 an L1 finding (`draft:519`). So `entry:136` points at the tool section, not at the binary evidence.
- `w1:146-147` said the "(§3.3)" pointer "is fixed separately (§7)". `w1:200-206` named the whole set and gave §3.4 as the right target. Neither was applied. `lesson:107` records D2 as "fixed", and no routed item carries these pointers.
- QUALITY 77 says "a statement a critic named explicitly gets its own named correction row" (`corpus/QUALITY.md:353-355`).
- Verdict: wrong. The binary evidence that `entry:135-136` and `entry:302-304` rely on is not reachable from the landed entry.
- Exact correction:
  - `entry:136`: "and on the installed binary's bytes (§3.3)." → "and on the installed binary's bytes (`.ufo/waves/round-26/w1/SrcEarlyoomReadme.md:85-86`: `strings -a /usr/bin/earlyoom | grep -c kernel-oom` → `0`; `strings -a /usr/bin/earlyoom | grep -n "Option -k"` → the `Option -k is ignored since earlyoom v1.2` line)." That committed text was re-run today with the same result (§5).
  - `entry:41` and `entry:42`: "(§3.1)" → "(`.ufo/waves/round-26/capture/capture.txt`, the file F1 already cites)".
  - `entry:74`, `entry:107`, `entry:118`, `entry:180`: "§3.2" → "`.ufo/waves/round-26/capture/capture-boots.txt`, the file F9 already cites". I did not check which committed file holds the "273" count at `entry:107`; the editor must find it or delete the pointer.
  - `entry:252`: "see F7 and §4.2." → "see F7 and `corpus/knowledge/userspace-oom-killers-r12.md:6` (scoped in round 26)."

### M2 (medium) — a sibling entry states the delegation exception without a build scope (QUALITY 77 sibling files; QUALITY 79)

- `r12C:21`: "`earlyoom --kernel-oom` delegates to the kernel; the counters can move if that route actually reaches a kernel OOM victim."
- `r12C:30`: "`earlyoom --kernel-oom` is the explicit delegation exception, not evidence that ordinary earlyoom signals are counted."
- These are present-tense claims about the host's earlyoom. The installed 1.9.0 has no such option: `entry:129-132`, `w1`-independent evidence `SrcEarlyoomReadme.md:85-87`, and `main-v1.9.0.c:245-246` (§5). `entry:134` and `entry:260-261` cite `r12C` for F7's kernel side, so the F7 correction is not carried where F7 points.
- QUALITY 79 (`corpus/QUALITY.md:361-364`) requires the release to be named. Without it the statement is false of the host. `SKILL.md:700` already carries the scoped form, and `r12C:14` and `r12U:13` are master-scoped, so the fix matches what the lane already does.
- Verdict: wrong (unscoped).
- Exact correction:
  - `r12C:21`: "`earlyoom --kernel-oom` delegates to the kernel; the counters can move if that route actually reaches a kernel OOM victim." → "Upstream master's `earlyoom --kernel-oom` (S016) delegates to the kernel. The installed earlyoom 1.9.0 has no such option (`userspace-oom-killers-r26.md` F7), so on this host the flag cannot move these counters. In a build that has the option, the counters can move if that route reaches a kernel OOM victim."
  - `r12C:30`: "`earlyoom --kernel-oom` is the explicit delegation exception" → "upstream master's `earlyoom --kernel-oom` (S016; absent from the installed 1.9.0) is the explicit delegation exception".

### M3 (medium) — the entry contradicts its own disclaimer about upstream master (pre-existing; D2 extended it)

- `entry:272` (Not claimed): "No claim about any earlyoom build other than 1.9.0, and no claim about upstream master."
- `entry:211` (Limits): "Upstream master has moved since — it carries a kernel-OOM trigger option again, and its README documents message shapes the tag does not have."
- `entry:139` (F7 Limit): "Upstream master has carried a kernel-OOM trigger option again authored 2026-02-02 and merged 2026-02-17 (S137, commit `750a7c0d`)".
- `entry:303-304`: "the master-side claim was true but under-cited."
- `126e192` already has the `:211` and `:272` lines, so the contradiction predates D2. D2 added dated master claims at `:139` and `:301`. QUALITY 77 says a contradicted line left standing is a defect "whether or not a corrections section exists" (`corpus/QUALITY.md:351-352`). Reader risk is low; the defect is the contradiction.
- Verdict: wrong (the disclaimer is contradicted by the same entry).
- Exact correction for `entry:272`: "- No claim about any earlyoom build other than 1.9.0. Upstream master appears only as dated facts about one commit (S137; F7 Limit) and as the master README that S016 cites; no sentence here describes master's behaviour as this host's."

### L1 (low-medium) — "merged 2026-02-17" has no merge evidence; the correction block says no statement was retracted when one was

- Evidence (API, read 2026-10-22): commit `750a7c0d` has one parent, `9808c7599596ef0d5a9c333f6fa346db8778f144`, so it is not a merge commit. The `commits/750a7c0d…/pulls` endpoint returns `[]`. The 2026-02-17 date is the committer date (Jakob Unterwurzacher); the parent is a `build(deps)` commit committed by `rfjakob` on the same day. [INFERENCE] The commit was applied on top of master that day by rebase, cherry-pick or push. A merge is not shown.
- The replaced sentence "has carried … since 2026-02-02" (`126e192:139`) dated master's carrying of the feature by the author date. The commit's author date is not evidence of when it reached master. [INFERENCE] The committer date is the earliest date the record supports; committer dates can be set by hand, and nothing here shows that this one was.
- Occurrences of "merged": `entry:1` (S137 segment), `entry:139`, `entry:301`. The S137 scope says "its author and merge dates" (`SOURCES:143`).
- `entry:302-304` says "No body statement is retracted". That is false for the replaced "since 2026-02-02" sentence. The D2 block also logs no old → new for `entry:135` or `entry:139`, although the other corrections in this file do (`entry:281-291`).
- Verdict: unsupported (the verb) and wrong (the retraction claim).
- Exact correction:
  - `entry:1`: "authored 2026-02-02, merged 2026-02-17;" → "authored 2026-02-02, committed to master 2026-02-17 (committer date);"
  - `entry:139`: "authored 2026-02-02 and merged 2026-02-17 (S137, commit `750a7c0d`)" → "authored 2026-02-02 and committed to master 2026-02-17 (committer date; a single-parent commit; S137, commit `750a7c0d`)"
  - `entry:301`: "authored 2026-02-02T05:00:04Z, merged 2026-02-17;" → "authored 2026-02-02T05:00:04Z, committed to master 2026-02-17T20:30:10Z (committer date);"
  - `entry:302-304`: replace "No body statement is retracted:" with "One sentence is retracted: 'has carried … since 2026-02-02' (`126e192:139`) dated master's carrying by the author date. The rest stands:", and add old → new rows for `entry:135` and `entry:139`.
  - `SOURCES:143` "merge dates" → "committer date". The S137 row was first published at `79ecf58`. The docstring of `.ufo/waves/round-27/check-row-identity.py` (lines 2-4) says CORPUS.md Rules 2 allow in-place change only to status, recheck and used-by. So the row wording needs a superseding row, or the entry carries the correction and the row wording becomes named debt.

### L2 (low-medium) — S114 gives a different upstream date for the same commit (immutable row)

- `SOURCES:120` (S114 evidence): "the flag was added upstream on 2026-02-02, after this tag". That date is the author date. `SOURCES:143` and `entry:139` put the commit's arrival on master at 2026-02-17.
- The entry no longer cites S114 for the date (it cites S137), so the conflict sits inside the row.
- Verdict: unsupported as an upstream-addition date.
- Route: a superseding row for the date only (the S124/S133 pattern) or named debt. No in-place edit of S114 (Rules 2).

### L3 (low) — S117 evidence hashes msg.c, but the row does not list msg.c's URL

- `SOURCES:123` lists "msg.c `a771c915…5197`". The hash is correct: `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/msg.c` gives sha256 `a771c91529053341…5197` (§5). msg.c is not among the row's URLs; S118 owns the file (`SOURCES:124`).
- ReopenS116S117 D5 (round-26 wave 2) raised it; `w1:207-209` calls it informational.
- Verdict: holds on the hash, unsupported by the row's URL list.
- Route: superseding row, or named debt. No in-place change.

### L4 (low) — the S117 scope names v1.7 and v1.8 items that the row does not anchor (ReopenS116S117 D6; not routed)

- `SOURCES:123` says the version line, the two threshold lines, the action line, the escalation line, the kill-failure line, the two low-memory warnings, the dry-run flag and the percentage format are stable "at those tags" (v1.7, v1.8, v1.9.0).
- I checked the v1.7 and v1.8 bytes, and the claim holds: v1.7 `main.c:109` (version), `:224` (dry-run), `:431` and `:435` (low memory), `kill.c:395` (kill failed); v1.8 `main.c:132`, `:263`, `:487`, `:491`, `kill.c:558`; `msg.h:10` at both.
- The row anchors none of the version, dry-run, low-memory, kill-failure or percentage lines at v1.7 or v1.8. It anchors the mem-threshold lines (`main.c:326/328` at v1.7, `:382/384` at v1.8) and the action and escalation lines (`kill.c:167/377`, `:230/539`). It lists `msg.h` only at v1.9.0.
- Also unrouted: the round-26 Gate record `corpus/lessons/round-26.md:70` cites `…/releases/tags/v1.9.0`, a URL the row does not list (ReopenS116S117 D4).
- Verdict: holds on the claim; the anchors are missing.
- Route: superseding row, or named debt.

### L5 (low) — "prints" needs the `-k` condition (F7 and S137)

- `entry:131-132`: "the installed binary on this host contains no such string and prints "Option -k is ignored since earlyoom v1.2"." `SOURCES:143` teaches: "a 1.9.0 binary prints 'Option -k is ignored since earlyoom v1.2'".
- The string sits inside `case 'k':` (`main-v1.9.0.c:245-246`), so the binary prints it only when run with `-k`.
- Exact correction in the entry: "…and prints, when run with `-k`, "Option -k is ignored since earlyoom v1.2"." The S137 teaches cell is immutable; name it as debt.

### L6 (low) — round-27 lesson wording overstates D2

- `lesson:107`: "F7 cites both" is ambiguous. F7 cites S114 (`README.md:383`) and S137 (dates); it does not cite S117 (no S117 in F7, §5).
- `lesson:107`: "now matches the row" overstates. Line 1 quotes the row's title, its tags and releases URLs and its scope, which is two of the row's ten URLs.
- `lesson:107` records D2 as fixed while M1 is still open.
- Replacement: "F7 cites S114 (README.md:383) and S137 (dates); line 1 quotes the S117 row's title, its tags and releases URLs and its scope; the (§3.3) pointer (M1) is open."

### I1 (info) — S137 date range and a receipt difference

- The first page of 100 holds (`commits?path=main.c&per_page=100`, read today). Author dates run from `2018-07-16T07:04:01Z` to `2026-10-15T17:31:12Z`, which matches `SOURCES:143` "2018-07-16 to 2026-10-15" on author dates. The committer maximum on the same page is `2026-10-17T18:34:22Z`.
- `w1` §8 gives the page's newest timestamp as `2026-10-15T17:28:19Z`. Today's author maximum is `17:31:12Z` (commit `df3934ae…`). The minute-level difference is unexplained [INFERENCE: the receipt may have used another field, or the page changed]. No verdict changes.
- `entry:1` lists S137 between S117 and S118, so the ids are out of sequence. Cosmetic.

## Statement verdicts

| # | Statement (location) | Verdict |
|---|---|---|
| 1 | `entry:1` S117 segment: title, two URLs, scope | holds. Matches `SOURCES:123` on title, first two URLs and scope. Equals `w1:137` with S127→S137 (substring test). |
| 2 | `entry:1` S137 segment: URLs, v1.2 removal, S114 anchor | holds, except "merged 2026-02-17" (L1). |
| 3 | `entry:135`: main.c:245-246 at v1.9.0; S114 README.md:383; S137 dates | holds (§5). |
| 4 | `entry:136`: "(§3.3)" for the installed-binary evidence | wrong (M1). |
| 5 | `entry:139`: "authored 2026-02-02 and merged 2026-02-17 (S137, commit `750a7c0d`)" | authored date holds; "merged" unsupported (L1). The replaced "since 2026-02-02" (`126e192:139`) was wrong (L1). |
| 6 | `entry:293-300`: description of the superseded line 1 | holds. `126e192` line 1 reads "S117 (earlyoom tag history — https://github.com/rfjakob/earlyoom/releases and https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c — …". |
| 7 | `entry:299`: "carries neither URL and no option-history scope" | holds (`SOURCES:123` has no `commits?path` and no github.com releases URL). |
| 8 | `entry:300-301`: new row S137; lines 201, 315-317, 352; dates | holds (§5). |
| 9 | `entry:302`: v1.2 removal anchored on S114 `README.md:383` | holds (`README-v1.9.0.md:383`). |
| 10 | `entry:302-304`: "No body statement is retracted"; "verified … on the installed binary" | the retraction claim is wrong (L1). The binary check holds on re-run (§5), but its pointer does not (M1). |
| 11 | `SOURCES:123` S117 row | holds on every anchor, hash and date checked (§5). The msg.c hash lacks its URL (L3); the v1.7/v1.8 scope is unanchored (L4). |
| 12 | `SOURCES:143` S137 row | holds on anchors, sha256 and dates. "merge dates" unsupported (L1); "prints" conditional (L5). |
| 13 | `w1:137-166` proposed text vs landed | holds as landed, with S127→S137 only. The landed S137 `used-by` lists only the r26 entry, which is right: no other entry cites S137 (grep). The wave-1 proposal's extra `oom-victim-selection-r27.md` was wrong. The w1 §7 "(§3.3)" fix was not applied (M1). |

## QUALITY 77 sweep

Swept: folded text (whitespace collapsed; `*`, `_` and backticks removed) of every tracked file under `corpus/` plus `SKILL.md`, `PROVINCE.md`, `README.md` and `CORPUS.md`, at `5f00fd0`.

- "earlyoom tag history": one hit, the correction block that names the superseded wording. That is a permitted named record.
- `commits?path=main.c`: hits only in S137, the entry's line 1 and correction block, and round-26 and round-27 lesson records. Permitted.
- GitHub HTML releases URL: no hit.
- "option history", "re-introduc", "carried … master", "2026-02-0x": hits only in S137, S114 (L2), the entry (F7, line 1, correction block) and the round-27 lesson.
- "delegat", "--kernel-oom", "-k": `SKILL.md:700` holds (scoped). `r12U:6` holds (scoped in round 26). `r12U:13` and `r12C:14` hold (master-scoped). `r12C:21` and `r12C:30` fail (M2).
- S117 mentions: `entry:1`, the correction block, the S117 and S137 rows, and records under `corpus/lessons/round-26*.md` and `round-27.md`. No other entry states the S117 description.
- Other round-27 corrections (D4: O2, O10, O14, O17; R7: U1, F10, psi, cgroup): the superseded wording appears only inside its own correction record. No stale line found.

Result: M2 and M3 are contradicted lines left standing. M1 is a critic-named pointer left standing. L2 is an immutable-row conflict with no permitted in-place fix.

## Receipts

External sources: ordinary `curl` 8.23.0 GETs with no browser and no challenge. Accessed 2026-10-22 between 17:12Z and 17:21Z. Hashes are sha256 of the bytes as fetched; scratch copies are in `/fast/scratch/hyaku/mori-r27/ReviewHygieneD2/`.

- `https://api.github.com/repos/rfjakob/earlyoom/commits/750a7c0d97bb01c1bdf126fd6bf5722da17e8998` (JSON). Parent `9808c7599596ef0d5a9c333f6fa346db8778f144` (one parent). Author IceLocke, `2026-02-02T05:00:04Z`. Committer "Jakob Unterwurzacher", `2026-02-17T20:30:10Z`. Message "kill: option for triggering kernel oom killer". Verification "unsigned".
- `…/commits/750a7c0d…/pulls` → `[]`.
- `…/commits/9808c7599596ef0d5a9c333f6fa346db8778f144` (parent). Author date `2026-02-17T19:49:11Z`; committer rfjakob `2026-02-17T19:53:14Z`; message "build(deps): bump actions/checkout from 2 to 6".
- `https://api.github.com/repos/rfjakob/earlyoom/git/refs/tags/v1.9.0` → tag object `66d78843fd675859a09a52d3f17b1c408a827a34`. `…/git/tags/66d78843…`: tagger `2025-09-16T19:09:33Z`, object commit `202d4db0d308ca6478f68de68b46cae34896ddaf`. Matches S117 and S114.
- `…/commits?path=main.c&per_page=100`: 100 entries; `750a7c0d` at index 4.
- Raw `…/750a7c0d97bb01c1bdf126fd6bf5722da17e8998/main.c`: 585 lines; sha256 `d24a26c97744458706a870ee3eb1ddcd5e5f05dda11fe22a71d6a4952028df3e`. Line 201: `{ "kernel-oom", no_argument, NULL, LONG_OPT_USE_KERNEL_OOM },`. Line 317: `fprintf(stderr, "Using kernel OOM killer (requires Linux v5.17+)\n");`. Line 352: `"  --kernel-oom              use kernel OOM killer via /proc/sysrq-trigger\n"`. Lines 437-438 and 553-554 match S137.
- Raw `…/v1.9.0/main.c`: 552 lines; sha256 `08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4`. Lines 245-246: `case 'k':` and `fprintf(stderr, "Option -k is ignored since earlyoom v1.2\n");`. No `kernel-oom` string.
- Raw `…/v1.9.0/README.md`: 427 lines; sha256 `23411dbfd8b409d433f984a5d6677830e86a383ec76935fc1e1d675e6b4374dd`. Line 283 `* v1.9.0, 2025-09-16`. Line 383 `* Remove option to use kernel oom-killer (`-k`, now ignored for compatibility)`. Line 416 `* v0.6: Add command-line options `-m`, `-s`, `-k`` (the S137 v0.6 claim is anchored here).
- Raw `…/v1.9.0/kill.c`: sha256 `b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3`. Line 242 `int res = kill(pid, sig);`. Lines 318, 627 and 654 match S117.
- Raw `…/v1.9.0/msg.c`: sha256 `a771c91529053341c290ede2a7df1d9fdf16e07fb9584db8a64604a45dea5197` (S117 and S118 hash; correct for msg.c). Raw `…/v1.9.0/msg.h`: 34 lines; sha256 `e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c` (S117 hash; correct). Line 10 `#define PRIPCT "%5.2lf%%"`.
- Raw `…/v1.8/main.c`: 520 lines; sha256 `9bdc8209af6f68403f1137a3e86e566a0ca137dc1ec5c46a1fdf099151b2834c`. Lines 132, 263, 382, 384, 487, 491. Raw `…/v1.8/kill.c`: 570 lines; lines 230, 539, 558. Raw `…/v1.8/msg.h`: line 10.
- Raw `…/v1.7/main.c`: 464 lines; sha256 `ceaa208361fa112857e30928a0e727711b9da6e86cebaa2f100bbd3d02113412`. Lines 109, 224, 326, 328, 431, 435. Raw `…/v1.7/kill.c`: 407 lines; lines 167, 377, 395. Raw `…/v1.7/msg.h`: 31 lines; line 10.
- Raw `torvalds/linux` v7.2 `mm/oom_kill.c`: 1257 lines; sha256 `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` (S003's hash). Lines 935-936: `count_vm_event(OOM_KILL);` and `memcg_memory_event_mm(mm, MEMCG_OOM_KILL);`.

Local, committed bytes:

- `126e192` line 1 (pre-fix): "S117 (earlyoom tag history — https://github.com/rfjakob/earlyoom/releases and https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c — the v1.9.0 tag and commit, the v1.2 removal of the kernel-oom option and its 2026-02-02 re-introduction on master;". The correction block describes this correctly.
- `SOURCES:123` (S117) row line hashes to the same value at `327fbcc`, `16935e2`, `126e192`, `79ecf58` and `5f00fd0`. S117 was not edited in the D2 landing.
- `git diff 79ecf58 5f00fd0 -- corpus/SOURCES.md`: 4 insertions, no deletions (S138–S141). `git diff 126e192 5f00fd0 -- corpus/SOURCES.md`: one deleted line, S124 (D3's restore; not reviewed here).
- `git log -S` puts the first S137 line in `79ecf58`.
- Installed binary, re-checked with counts only: `grep -c -a -F 'kernel-oom' /usr/bin/earlyoom` → `0`; `grep -c -a -F 'Option -k is ignored since earlyoom v1.2' /usr/bin/earlyoom` → `1`. The file is 43,520 B, root-owned, mtime 2025-09-17. Its sha256 begins `8d3393c8…`. This matches `w1`-cited `.ufo/waves/round-26/w1/SrcEarlyoomReadme.md:85-86`.
- `SKILL.md:700` reads: "earlyoom v1.9.0 has **no** `--kernel-oom` delegation option". It is consistent with F7.
- `lesson:80` and `SOURCES:143` agree on the S137 URLs.

## Residual risk and verification gaps

- Not opened: the S016 master README anchors (`8477c902`, lines 55-56, 68-69, 148-149); the S114, S115, S116, S118 and S119 anchors beyond those touched here; the S137 "first page" beyond the page facts above.
- kill.c lines 246-262 (the pidfd release that F7 cites) were not compared line by line. Only line 242 was checked.
- The merge question is open. The web UI was not used (no browser under the bounds). The pulls API is the only evidence, and it returned `[]`.
- I did not run `check-row-identity.py`, because QUALITY 81 is outside this scope. I compared the S117 row and the S137 first commit by hash of the row line instead.
- Wave-1 receipts I did not re-open: the single-release endpoint body and `published_at` (`w1:25-36`); the `releases` sha256; the `tags` endpoint.
- API responses are unauthenticated and moving windows; the commits page changes as commits land.
- Not reviewed: the S124 in-place restore (D3), the only deleted SOURCES line between `126e192` and the tip; the D4 and R7 corrections beyond the sweep in the QUALITY 77 section.

## Tooling record

No install, upgrade or package operation. Read `/home/vgpnk/.omp/agent/RULES.md` (operator tooling directive). Tools used, all already present: curl 8.23.0 (libcurl 8.23.0, OpenSSL 3.6.5); Python 3.14.8; git 2.56.0; jaq 3.1.1 (as `jq`); sha256sum 0.8.0 (as reported by `--version`); grep; sed. No pacman command was run. Git use was read-only (`show`, `log`, `grep`, `ls-tree`, `cat-file`). No jj command was run.

## Write scope

This file is the only file written in the lane: `.ufo/waves/round-27/w2/ReviewHygieneD2.md`. Scratch is under `/fast/scratch/hyaku/mori-r27/ReviewHygieneD2/`. No edit to the entry, rows, lessons, scripts or any other file.
