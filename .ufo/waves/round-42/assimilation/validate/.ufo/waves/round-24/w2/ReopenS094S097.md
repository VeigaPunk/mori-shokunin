# ReopenS094S097 — round 24, wave 2 (attempt 2)

Seat: MoriR24.ReopenS094S097 (leaf; no subagents; detection and report only).
Lane: /home/vgpnk/Projects/shokunin/mori-shokunin. Wave measured tip: a730ecf. HEAD during review: 13208d2 at start, 89849a7 at the end (see Observations). Checks run 2026-10-22; the 404 response carried `Date: Thu, 22 Oct 2026 08:59:20 GMT`. Scratch: /fast/scratch/hyaku/mori-r24-a2/w2/ReopenS094S097/.

## Result per row

| Row | Anchors | Lesson Gate quote | Scope cell | Teaches cell | Registry fields | Verdict |
|---|---|---|---|---|---|---|
| S094 (SOURCES.md:100) | Holds: 5505-5507 | Holds; source uses tabs, quote shows spaces (F7) | Holds | Holds except one clause outside the anchor (F6) | Holds | Holds; F6, F7 Low |
| S095 (SOURCES.md:101) | Holds: 41-49, 51-56, 57-70, 45-47, 64-66, 67-68, 208-214 | Holds, exact | Holds | Holds; file-shape rule rests on other rows (F8) | Holds | Holds; F8 nit |
| S096 (SOURCES.md:102) | Holds: commit, hunks, dates, tag membership | Holds, exact, 25 words | Holds; zone missing on author date (F7) | Fails on "absent irq file is a build-configuration fact" (F1) | Gate row has no digest (F7) | Overclaim, Medium (F1) |
| S097 (SOURCES.md:103) | 404 reproduced; body 196 bytes; Gate lines 3, 5, 6 hold | Holds | Holds: no man-pages 6.20 page, no /proc/pressure text | Holds (REJECTED wording) | used-by incomplete and lesson M3 false (F2); negatives unregistered (F3); digest width and fetch time (F4); flip cites S001 for S090 lines (F5) | Rejection confirmed; F2 Medium, F3-F5 Low |

## Findings, by severity

**F1 — Medium — S096 teaches cell asserts a causal rule that the commit and the register contradict.**
- Claim (SOURCES.md:102): "...so an absent irq file is a build-configuration fact and never a zero reading."
- The commit's own hunk gates the file on boot state. Patch lines 250-262: `static int __init psi_proc_init(void)`, then `if (psi_enable) {` at line 252, then `proc_create("pressure/irq", ...)` at lines 257-259 inside that block.
- v7.2 kernel/sched/psi.c agrees. `psi_enable` comes from CONFIG_PSI_DEFAULT_DISABLED and the `psi=` parameter (lines 149-158). `psi_init` disables PSI when `psi_enable` is false (lines 228-234). `psi_proc_init` creates the four files only under `if (psi_enable)` (lines 1710-1721). The whole proc block sits under `#ifdef CONFIG_PROC_FS` (lines 1537-1725).
- So an absent irq file has at least three causes: a boot-time disable (`psi=0`, or CONFIG_PSI_DEFAULT_DISABLED without `psi=1`), no CONFIG_PROC_FS, or no CONFIG_IRQ_TIME_ACCOUNTING. The teaches cell names only the last.
- The register already says otherwise. S091 teaches "a PSI switched off at boot leaves them absent rather than unreadable" (SOURCES.md:97). The Paths line says "the build and boot switches that decide which files exist" (SOURCES.md:112). The knowledge entry says a missing file "is consistent with either; the tool records no cause" (corpus/knowledge/system-pressure-r24.md:139).
- "Never a zero reading" is the lane's own rule, not text from the commit.
- Not load-bearing: the knowledge entry does not repeat the causal claim. Medium because the teaches cell is the reusable statement and states the opposite of the entry and of S091.
- Fix: replace the last clause with "the irq file exists only when CONFIG_IRQ_TIME_ACCOUNTING is built in and psi_enable is true, the same gate as cpu, memory and io; so an absent irq file has more than one cause. Absence is never a zero reading (lane rule)."

**F2 — Medium — S097 used-by is incomplete, and lesson M3 states something false.**
- SOURCES.md:103 used-by lists only corpus/lessons/round-24.md.
- corpus/knowledge/system-pressure-r24.md cites S097 twice: in its source header, "Rejected candidate: S097 (proc_pressure(5) does not exist; HTTP 404)" (line 1), and in U6, "No `proc_pressure(5)` page exists (S097, rejected: HTTP 404; ...)" (line 185). PROVINCE.md:258 cites it too.
- corpus/lessons/round-24.md:56 (M3, fix column) says "the knowledge entry cites only S090–S096." As written, that is false.
- contract.md:162-163 (A5) says S097 is "cited by nothing." Also inaccurate.
- The rejection verdict itself stands.
- Fix: used-by "corpus/lessons/round-24.md, corpus/knowledge/system-pressure-r24.md, PROVINCE.md"; M3 to read "the knowledge entry names S097 only as the rejected candidate (header line 1 and U6 line 185)".

**F3 — Low — S097 negative claims have no registered URL or digest.**
- The anchor cell asserts the man-pages 6.20 contents and the man7 proc(5) contents, but registers only the 404 URL. I re-derived both claims (see S097 below); they hold.
- Recording them for the row: man-pages 6.20 tarball https://www.kernel.org/pub/linux/docs/man-pages/man-pages-6.20.tar.xz, sha256 180f0d16a2142dd9671760ac0afeadcc25e861f695eb420293e1206a87ca083f. man7 proc(5) https://man7.org/linux/man-pages/man5/proc.5.html, fetched 2026-10-22, 31125 bytes, sha256 b197c5fa64577269f992d50f60acfd5e0cc3df756644ddd8bd19a02591272a97.

**F4 — Low — S097 record format and fetch time.**
- SOURCES.md:103 "sha256 80c3fe2ae1062abf5" has 17 hex digits. The Gate row (round-24.md:32) and the stated convention (round-24.md:21, first 16 hex) use 16. The 17-digit value is a correct prefix of the full digest 80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880.
- Fetch time: SOURCES.md:103 says 08:21:47Z; round-24.md:32 says 08:21:46Z. Not checkable retroactively. Today's fetch reproduces the 404 and the digest.

**F5 — Low — S097 flip cites the wrong row for its line numbers.**
- SOURCES.md:103: "(S001; kernel v7.2 Documentation/accounting/psi.rst lines 42-43 and 57-58)". Those lines belong to the raw v7.2 file registered as S090 (SOURCES.md:96). S001 is the HTML page with different anchors.
- The lines are correct. psi.rst line 42 is "some avg10=0.00 ...", line 43 is "full avg10=0.00 ...", and lines 57-58 read "CPU full is undefined at the system level, but has been reported since 5.13, so it is set to zero for backward compatibility."

**F6 — Low — S094 teaches cell has a clause outside its anchor.**
- SOURCES.md:100: "...is not guaranteed merely by running a Linux kernel." Lines 5505-5507 do not say this. It follows from S093 (CONFIG_PSI_DEFAULT_DISABLED, SOURCES.md:99) and S095 (the CONFIG_PSI-off branch, psi_types.h lines 208-214).
- Fix: cite those rows, or mark the clause [INFERENCE].

**F7 — Nit — quote rendering, a missing digest, and a missing zone.**
- S094 quote (round-24.md:29): source line 5505 separates the tokens with tab characters (`psi=`, two tabs, `[KNL]`). The Gate shows single spaces, though its header says quotes are copied exactly. Substance unchanged.
- S096 Gate row (round-24.md:31) has no digest, though the header (round-24.md:20-21) says every row carries one. The .patch fetched today has sha256 a255f4471b9388ba3d5bfdf64a093dec35a66cd8080473fb4bd2d4b49dce7cd6.
- S096 Gate says "commit message paragraphs 3-4". Paragraph 4 is the sign-off block; the quote is in paragraph 3 (patch lines 15-17).
- S096 scope (SOURCES.md:102) says "authored 2022-08-26" without a zone. The author date is 2022-08-26T00:41:08+08:00, which is 2022-08-25T16:41:08Z.

**F8 — Nit — S095 teaches cell derives a file-shape rule from the enum alone.**
- SOURCES.md:101: "an irq reading without a some line is expected rather than malformed." The enum (psi_types.h lines 57-70) shows no IRQ some state. The file shape itself comes from psi_show (S091) and from the commit's only_full hunk (S096, patch lines 181-203). Suggest citing those for the file-shape claim.

## Per-row evidence

### S094 — kernel-parameters.txt at tag v7.2 (SOURCES.md:100; round-24.md:29)
- Re-opened https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/kernel-parameters.txt: HTTP 200, 317993 bytes, sha256 23b1a690210b6884f040a6b1e5baf1fc18856e844d30d4784470bd210953340c. Matches the register.
- Lines 5505-5507: `psi=		[KNL] Enable or disable pressure stall information` / `			tracking.` / `			Format: <bool>`. Anchor holds.
- Scope holds (parameter, format and stated effect; no layout or counter semantics).
- Used-by holds: knowledge entry line 86 and lesson Gate row 29.
- Verdict: holds. F6, F7.

### S095 — psi_types.h at tag v7.2 (SOURCES.md:101; round-24.md:30)
- Re-opened the raw v7.2 file: HTTP 200, 5061 bytes, sha256 483269b27c82b438450632555aba2ba8a9c47b608243f78a029c4300b3618ccc. Matches.
- Lines 41-49: enum psi_res, with PSI_IRQ under `#ifdef CONFIG_IRQ_TIME_ACCOUNTING` at 45-47. Lines 51-56: comment. Line 54 "SOME: Stalled tasks & working tasks"; line 55 "FULL: Stalled tasks & no working tasks" (both exact). Lines 57-70: enum psi_states, with PSI_IRQ_FULL under the same conditional at 64-66 and PSI_NONIDLE at 67-68. Lines 208-214: the `#else /* CONFIG_PSI */` branch (NR_PSI_RESOURCES 0 at line 210; empty psi_group at line 212).
- Scope and teaches hold, except the F8 nit.
- Used-by holds: knowledge entry lines 1 and 69; lesson row 30.
- Verdict: holds.

### S096 — commit 52b1364ba0b105122d6de0e719b36db705011ac1 (SOURCES.md:102; round-24.md:31)
- Re-opened the registered URL: HTTP 200, 714097 bytes; title "sched/psi: Add PSI_IRQ to track IRQ/SOFTIRQ pressure · torvalds/linux@52b1364". The .patch: HTTP 200, 8899 bytes, sha256 a255f4471b9388ba3d5bfdf64a093dec35a66cd8080473fb4bd2d4b49dce7cd6.
- Identity and dates hold. Patch line 1 names the hash; line 3 reads "Date: Fri, 26 Aug 2022 00:41:08 +0800". The page's embedded JSON gives authoredDate 2022-08-26T00:41:08.000+08:00, committedDate 2022-09-09T11:08:32.000+02:00, and committer Peter Zijlstra.
- Merge holds. Page for bd9a3dba185c (976222 bytes): title "Merge tag 'sched-psi-2022-10-14' of git://git.kernel.org/pub/scm/linux/kernel/git/tip/tip"; authoredDate and committedDate 2022-10-14T13:03:00-07:00; its merge log lists "sched/psi: Add PSI_IRQ to track IRQ/SOFTIRQ pressure".
- Tag membership holds. The GitHub commit list for kernel/sched/psi.c at v6.1 contains the commit (data-commit-link /torvalds/linux/commit/52b1364ba0b105122d6de0e719b36db705011ac1); its v6.0 list (first page) has no such entry. The file content check is the firmer evidence: raw v6.0 psi.c (39513 bytes, sha256 126479b39bc86ac4c27cbd5c134266eb03b5d3fa9333df22eda4314a870790aa) has no PSI_IRQ or psi_account_irqtime, and raw v6.0 psi_types.h (4533 bytes) has no IRQ symbol. Raw v6.1 and v6.1-rc1 psi.c are identical (sha256 f3038de87e41da91a1050093d367084c201e68784336de24e1428d3b0db67ab6) and contain psi_account_irqtime (914-915), PSI_IRQ_FULL accounting (937), only_full (1161), psi_irq_proc_ops (1512) and `proc_create("pressure/irq", ...)` (1530).
- Quote holds. Patch lines 15-17: "Note we don't use PSI_IRQ_SOME since IRQ/SOFTIRQ always happen in the current task on the CPU, make nothing productive could run even if it were runnable, so we only use PSI_IRQ_FULL." The Gate sentence matches after joining the wrapped lines; 25 words.
- Anchors hold. psi_account_irqtime at patch lines 144-172; only_full at 181-203; psi_irq_proc_ops at 240-247; psi_proc_init at 250-262; cgroup.c irq.pressure at 87-102 and 111-120; cgroup-v2.rst irq.pressure at 40-44.
- Teaches: fails on the build-configuration clause (F1). The "charged to the task running on the CPU" clause and the "no some line by design" clause hold (patch lines 11-17).
- Registry holds.
- Verdict: identity, quote, anchors, dates and tag membership hold; teaches overclaims (F1); Gate digest missing (F7).

### S097 — man7 proc_pressure(5), rejected (SOURCES.md:103; round-24.md:32; M3 at round-24.md:56; contract A5)
- Re-opened the registered URL with and without redirect following: HTTP 404 Not Found, Content-Length 196, 0 redirects, Server Apache/2.4.58 (Ubuntu). Body 196 bytes, sha256 80c3fe2ae1062abf56456f52518bd670f9ec3917b7f85e152b347ac6b6faf880.
- Body line 3 `<title>404 Not Found</title>`, line 5 `<h1>Not Found</h1>`, line 6 `<p>The requested URL was not found on this server.</p>`. The Gate quote and the line numbers hold.
- Control: man7 proc.5 returns HTTP 200 (31125 bytes), so the 404 is specific to that path.
- man-pages 6.20, checked from the kernel.org tarball. The kernel.org listing shows man-pages-6.20.tar.xz dated 21-Oct-2026 13:08 as the newest version; there is no 6.21 or later. The tarball's sha256 (180f0d16a2142dd9671760ac0afeadcc25e861f695eb420293e1206a87ca083f) equals its line in kernel.org sha256sums.asc. The PGP signature was not checked.
  - man/man5 has no proc_pressure file and no file name containing "pressure" (`find -iname '*pressure*'` returned nothing).
  - Case-insensitive search of the whole extracted tree for `proc/pressure`: no matches.
  - Case-insensitive "pressure" in man/man5: only proc_meminfo.5 and tmpfs.5, both about memory pressure.
  - Holds: no man5/proc_pressure page and no page mentioning /proc/pressure.
- man7 section 5 index (39543 bytes): no "pressure" entry, case-insensitive. man7 proc(5): no "pressure" anywhere, case-insensitive. The row's claim "proc(5) on man7 mentions no pressure file" holds, and is stronger than stated.
- Local host, supplementary: `man -w proc_pressure` returns "No manual entry for proc_pressure".
- Flip check: v7.2 psi.rst (6792 bytes, sha256 11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692, matching S090) has the lines cited. Holds, but the citation belongs to S090 (F5).
- Scope holds: "current release 6.20, 2026-10-21".
- Registry: rejected, tier C, opened 2026-10-22 holds. used-by is incomplete (F2); digest width and fetch time (F4).
- Verdict: rejection confirmed.

## Observations outside the seat's rows (for the integrator)
- HEAD moved during this review. `git log --oneline a730ecf..HEAD` now shows 89849a7 ("round-24: pressure selftest gains matcher negative controls and a co-evolved supplementary case file (wave-2 survivors)"), then 13208d2 and 753d227. `git diff --stat a730ecf HEAD -- tools` shows tools/mori-pressure.py (55 changed lines: 50 added, 5 removed) and tools/fixtures/mori-pressure/supplementary-cases.json (181 added). The four rows, the lesson and the knowledge entry are unchanged by these commits.
- I did not analyze the tool change. The contract says cases.json was frozen before the tool landed (C2); the new supplementary file is outside that set. Whether C2's after-value must be re-measured at the final tip is the integrator's call.

## What I ran
- Lane, read-only: `git rev-parse HEAD`; `git log --oneline -5`; `git status --short`; `git diff --stat a730ecf HEAD`, with and without path filters; `git log --oneline a730ecf..HEAD`; `git log --oneline -3 -- tools/mori-pressure.py`. No tracked file was modified. Only untracked wave files from sibling seats were present.
- Fetches into scratch (status, bytes, sha256 prefix):
  - raw v7.2 kernel-parameters.txt: 200, 317993 bytes, 23b1a690210b6884 (S094)
  - raw v7.2 psi_types.h: 200, 5061 bytes, 483269b27c82b438 (S095)
  - raw v7.2 psi.rst: 200, 6792 bytes, 11c6b7129103b454 (S090, for the flip)
  - raw v7.2 psi.c: 200, 48859 bytes, 452318beaca3e6d1 (S091, for gating lines)
  - github commit page: 200, 714097 bytes; commit .patch: 200, 8899 bytes, a255f4471b9388ba
  - api.github.com commit calls: 403 (rate limit; not used)
  - github merge page bd9a3dba185c: 200, 976222 bytes
  - github commit lists for kernel/sched/psi.c at v6.1: 200, 659546 bytes; at v6.0: 200, 650900 bytes
  - raw v6.0 psi.c: 200, 39513 bytes, 126479b3; raw v6.1 and v6.1-rc1 psi.c: 200, 43235 bytes, f3038de8 (identical)
  - raw v6.0 psi_types.h: 200, 4533 bytes; raw v6.1 psi_types.h: 429 on every attempt, at least four (not used)
  - man7 proc_pressure.5.html: 404, 196 bytes, 80c3fe2ae1062abf
  - man7 proc.5.html: 200, 31125 bytes, b197c5fa; man7 dir_section_5.html: 200, 39543 bytes, 1caa9e6d
  - kernel.org man-pages listing: 200, 10625 bytes; sha256sums.asc: 200, 5988 bytes; man-pages-6.20.tar.xz: 200, 1914692 bytes, 180f0d16 (extracted under scratch)
- Reads and searches: S094 lines 5499-5515; S095 lines 36-72 and 200-216; S096 full patch and lines 244-262; S090 lines 34-66; S091 lines 140-160, 226-236 and 1706-1722, plus CONFIG_PROC_FS occurrences; SOURCES rows S085-S097 and the Paths section (lines 105-112); lesson lines 1-60; contract lines 99-168; lane-wide search for S094-S097 and proc_pressure; knowledge-entry search for irq, absent, build, boot and S094-S097; case-insensitive pressure checks on man7 and on the man-pages tree.
- Disclosure: during the man-pages step I used a few shell `grep` calls on the scratch copy, against the tool-selection rule. Their results were re-checked with the search tool, and the re-checks agree.
- Installs: none (see Tools and installs).

## Verification gaps
- api.github.com returned HTTP 403 (rate limit). Commit dates come from the commit page's embedded JSON and the .patch headers.
- raw.githubusercontent.com returned HTTP 429 for v6.1 psi_types.h. No S096 claim depends on that file; S096 claims rest on the commit and on psi.c at v6.0 and v6.1.
- The man-pages sums.asc and tarball .sign were not PGP-verified; only the digest line was compared.
- Gate access timestamps and the register's opened dates cannot be re-observed; only byte identity was checked.
- No lane code symbol is cited by these rows, so no lsp caller or definition check applied. Text positions came from reading ranges and search results.
- Not run: tools/mori-pressure.py, tools/mori-routed-check.py and any mutant. Out of scope for these four rows.

## Tools and installs
- No installs, upgrades or privileged commands. Host binaries used: curl, tar, xz, sha256sum and man, all already present. pacman was not invoked (host transactions are paused). uv, npm and cargo were not used.
- Scratch only under /fast/scratch/hyaku/mori-r24-a2/w2/ReopenS094S097/. Lane writes: this file only. No /proc, /sys or cgroup writes; no PSI triggers; no services touched.

## Suggested corrections (for the integrator; this seat did not apply them)
1. SOURCES.md:102 teaches: replace the last clause as in F1.
2. SOURCES.md:103 used-by, anchor and flip: F2, F3, F4, F5.
3. round-24.md:56 M3 wording (F2); round-24.md:31 add the .patch digest (F7).
4. SOURCES.md:100 teaches: cite S093 and S095 for the "not guaranteed" clause, or mark it [INFERENCE] (F6). round-24.md:29 quote whitespace (F7, optional).
5. SOURCES.md:102 scope: add the zone to the author date (F7).
