# ReopenS114S115 — wave-2 reopen of SOURCES rows S114 and S115

Seat: MoriR26.ReopenS114S115 (reviewer, leaf; no subagents, no background jobs).
Pin: 16935e24c93fa7e7567413d7ec091339a5df1474 (branch master; read with git only).
Scratch: /fast/scratch/hyaku/mori-r26/ReopenS114S115/ (fetched bytes, extracts, JSON replies).

## Verdicts

| Row | Verdict | Attacked |
|---|---|---|
| S114 (earlyoom README at tag v1.9.0) | holds | row sha256 and bytes, anchors, Gate quote, tier, status, used-by |
| S115 (earlyoom MANPAGE at tag v1.9.0) | holds | row sha256, bytes and lines, anchors, Gate quote, tier, status, used-by |

No defect found. Four precision notes (N1-N4) and three items not run (R1-R3) are below.

## Pinned inputs (committed bytes, read with git show)

- corpus/SOURCES.md at the pin: 181 lines, sha256 b5cb055b5c20e8a4460120bcc10d6b0b8f4cbcfc9ff63ab919b39fc011a967cd. S114 row at line 120; S115 row at line 121.
- corpus/lessons/round-26.md at the pin: 92 lines, sha256 96f1cc87007e42f0360e77a886cdacdc5838218abe1a8f6d674e0394ab0d5a65. `## Gate` at lines 59-63; S114 Gate row at line 67; S115 Gate row at line 68.
- corpus/knowledge/userspace-oom-killers-r26.md at the pin: 271 lines, sha256 73593455be93a6758f30c483e393707bd1e988b87fe9156e250598e33e50b9e5.

## Fetches (ordinary HTTP through curl; no browser, no challenge)

| Public URL | HTTP | Bytes | Lines | sha256 |
|---|---|---|---|---|
| raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md | 200 | 19931 (content-length 19931) | 427 | 23411dbfd8b409d433f984a5d6677830e86a383ec76935fc1e1d675e6b4374dd |
| raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/MANPAGE.md | 200 | 10114 (content-length 10114) | 288 | cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda |
| raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/main.c (zero-hit check only) | 200 | 21053 | — | 08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4 |

Tag pin: `git ls-remote --tags https://github.com/rfjakob/earlyoom.git 'refs/tags/v1.9.0*'` printed tag object 66d78843fd675859a09a52d3f17b1c408a827a34 and peeled `refs/tags/v1.9.0^{}` 202d4db0d308ca6478f68de68b46cae34896ddaf. The raw URLs at commit 202d4db0 return the same bytes (cmp identical for both files). The GitHub API gives commit 202d4db0 a committer date of 2025-09-16T19:09:23Z.

## S114 — holds (corpus/SOURCES.md:120)

- Fields: kind tool, tier A, status mined, opened 2026-10-22, recheck on-release, used-by corpus/knowledge/userspace-oom-killers-r26.md. Tier A and status mined pass the fleet validator enums (scripts/sources-census.sh:26-27 and :631-632, :657-659). E10 (community at tier A, :668) does not apply.
- Bytes 19931 and sha256 23411dbf…4dd match the fetch.
- Anchor line numbers, checked against the fetched README by grep line numbers and by block counts from :raw reads:
  - act rule 28 holds (line 28 "By default if both are below 10%…"); 53-56 holds (the both-memory-and-swap rule); 239-240 holds ("Note: both memory and swap must be below minimum for" / "earlyoom to act.").
  - stage order 145-146 holds (startup sample lines "sending SIGTERM when mem avail <= 10.00%…" and "SIGKILL when mem avail <= 5.00%…"); 235-236 holds ("earlyoom sends SIGTERM once below PERCENT, then" / "SIGKILL once below KILL_PERCENT…"); 388 holds ("Implement staged kill: first SIGTERM, then SIGKILL…").
  - log destination 154 holds ("Every action is logged to stderr."); 259 holds ("--syslog use syslog instead of std streams").
  - journal advice 170-186 holds (`### Checking Logs` at 170; the journalctl grep block; the quote block ends with `>` at 186).
  - changelog v1.9.0 283-287 holds (283 "* v1.9.0, 2025-09-16"; the five-line entry ends at 287).
  - kernel-oom absence 65-67 holds (section "Why not trigger the kernel oom killer?" at 65), 383 holds (changelog "Remove option to use kernel oom-killer (-k…)"), 289-293 exist (v1.8.2 changelog; see N2).
  - Zero hits: the literal `kernel-oom` has 0 hits in the README, MANPAGE and main.c at v1.9.0 (grep tool, one call over all three paths, "No matches found"). Positive controls: "oom-killer" matched the README and the MANPAGE; "sending SIGTERM when mem avail" matched main.c:414.
  - Flag added after the tag: upstream commit 750a7c0d97bb… adds `--kernel-oom` to MANPAGE.md, README.md, kill.h and main.c (GitHub API commit files). Its author date is 2026-02-02T05:00:04Z, which matches the row (see N1). That is after 2025-09-16.
- Gate quote (lesson line 67): ":28 'By default if both are below 10%, it will kill the largest process (highest `oom_score`).'" Exact match at README line 28; 15 words by wc -w, within 25.
- used-by: corpus/knowledge/userspace-oom-killers-r26.md exists at the pin (validator E11 path rule, :29) and line 1 names S114 with the README URL and sha256 23411dbf…4dd.

## S115 — holds (corpus/SOURCES.md:121)

- Fields: kind docs, tier A, status mined, opened 2026-10-22, recheck on-release, used-by corpus/knowledge/userspace-oom-killers-r26.md. Tier A and status mined pass the validator enums (same lines as S114).
- Bytes 10114, lines 288 (wc -l and grep -c both give 288), sha256 cc48b02e…dfeda match the fetch.
- Anchor line numbers, checked against the fetched MANPAGE:
  - 30-35 holds (`#### -m PERCENT[,KILL_PERCENT]` at 30; the `user mem total` paragraph at 33-35).
  - 41-45 holds (41-42 SIGTERM under both conditions; 44-45 SIGKILL and the PERCENT/2 default).
  - 55-57 holds (`#### -s` at 55; 57 "Send SIGKILL if at or below KILL_PERCENT (default PERCENT/2)…").
  - 65-84 holds (`#### -M SIZE` at 65; "If you pass both `-M` and `-m`" at 72; `#### -S SIZE` at 79; 84 "Send SIGKILL if at or below KILL_SIZE…").
  - 98-109 holds (`#### -r INTERVAL` at 98; the sample report line at 102; the twelve-line block ends at 109).
  - 205-206 holds (`#### \-\-dryrun` at 205; "dry run (do not kill any processes)" at 206).
  - 208-217 holds (`#### \-\-syslog` at 208; the ten-line block ends at 217).
  - 222-250 holds (`# EXIT STATUS` at 222; "105: Could not convert number…" at 250).
  - 270-273 holds (`# BUGS` at 270; the zero-swap `-S` caveat at 272-273).
- Gate quote (lesson line 68): ":41-42 'earlyoom sends SIGTERM once **both** available memory **and** free swap are below their respective PERCENT settings.'" MANPAGE line 41 ends "…free swap are" and line 42 is "below their respective PERCENT settings.". Joined by one space the quote is verbatim, bold markers included. 16 words by wc -w, within 25.
- used-by: line 1 of corpus/knowledge/userspace-oom-killers-r26.md names S115 with the MANPAGE URL.

## Lesson Gate (corpus/lessons/round-26.md, `## Gate`)

- Both rows are present (lines 67-68) with URL, accessed date, located quote and decision "admit, A, mined".
- "Located and at most 25 words" holds for both quotes (15 and 16 words).
- Accessed dates: S114 2026-10-22 matches the row's opened date. S115 2026-10-22T13:14:31Z is the same day as the row; the original fetch time cannot be re-observed [not verifiable].
- Named seat reports exist at the pin: .ufo/waves/round-26/w1/SrcEarlyoomReadme.md and .ufo/waves/round-26/w1/SrcEarlyoomManpage.md. The README report gives sha256 23411dbf…4dd (line 15), and its side-file list gives MANPAGE.md sha256 cc48b02e…dfeda (line 174). Both match my fetches.

## Notes (not defects)

- N1 (precision, low): the S114 anchor says the flag "was added upstream on 2026-02-02". The commit that adds it, 750a7c0d97bb…, has author date 2026-02-02T05:00:04Z and committer date 2026-02-17T21:30:10+01:00. The 2026-02-02 date holds on the author basis, but the row does not name that basis. "After this tag" holds on either date.
- N2 (precision, low): the S114 anchor cites 289-293 under "kernel-oom absence". Those lines are the v1.8.2 changelog and do not mention kernel-oom. The absence rests on the zero-hit search, so the claim stands, but the range does not show absence by itself.
- N3 (context): upstream master has moved past the tag (the README commit list runs to 2026-10-19). The rows pin the tag, and the r26 entry says so at corpus/knowledge/userspace-oom-killers-r26.md:209-212.
- N4 (context): corpus/README.md (523 lines at the pin) and the SOURCES.md header give no tier or status legend. The fleet validator enum (scripts/sources-census.sh:26-27, :631-632, :657-659) is the only written definition I found.

## Not run

- R1: the sha256 table inside .ufo/waves/round-26/w1/SrcEarlyoomManpage.md was not opened.
- R2: scripts/sources-census.sh validate was not run; only its enum lines were read with grep. The E03 and E04 duplicate checks for these two URLs were not run.
- R3: the S119 row's own sha256 was not compared with main.c (21053 bytes, sha256 08656b0b…d0e4). main.c was fetched only for the kernel-oom zero-hit check.

## Tooling and bounds

- No tool installed or upgraded. Used system curl, git (read-only: show, cat-file, and ls-remote over HTTPS), sha256sum, cmp, wc, stat and od. No pacman. Read /home/vgpnk/.omp/agent/RULES.md first.
- Wrote only this report and scratch under /fast/scratch/hyaku/mori-r26/ReopenS114S115/. No jj. No git write command. No agent messages. No subagents.
- No operator settings, session ids, journal MESSAGE text, or earlyoom prefer and avoid expressions were read or copied.
