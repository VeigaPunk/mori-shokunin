# SrcEarlyoomReadme — earlyoom v1.9.0 README (SOURCES row draft)

Seat: `MoriR26.SrcEarlyoomReadme` (wave 1, scribe). Date: 2026-10-22.
Scope: open `https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md` and draft one
`corpus/SOURCES.md` row (id left as `S???`) plus a Gate line for the round-26 lesson.
No lane commit, no jj command, no mutation of any repo outside my report file.

## 1. Fetch receipt (Gate)

```
URL            https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md
HTTP           200
Bytes          19931
Lines          427
sha256         23411dbfd8b409d433f984a5d6677830e86a383ec76935fc1e1d675e6b4374dd
git blob sha   e7f86b1ba255425eb766fb5a205bad79176d9e03
Access date    2026-10-22 (re-fetch 2026-10-22T13:19:19Z produced the identical digest)
Tag            v1.9.0 -> annotated tag object 66d78843fd675859a09a52d3f17b1c408a827a34
                 -> commit 202d4db0d308ca6478f68de68b46cae34896ddaf (2025-09-16T19:09:23Z)
```

The L1's local copy at `/fast/scratch/hyaku/mori-r26/README.md` is byte-identical to my fetch
(`sha256 23411dbf…`, `diff` clean), so the lane already holds these exact bytes. My own copy and
all cited side files are under `/fast/scratch/hyaku/mori-r26/SrcEarlyoomReadme/`.

Verbatim quotes (each at most 25 words, with line numbers in the v1.9.0 README):

- README:28 — "By default if both are below 10%, it will kill the largest process (highest `oom_score`)."
- README:67 — "earlyoom does not use `echo f > /proc/sysrq-trigger` because:"
- README:175 — "sudo journalctl -u earlyoom | grep sending"

## 2. Ready-to-paste `corpus/SOURCES.md` row

Id left as `S???` per the item; the L1 assigns the number. Column shape matches the existing
registry (rows S098–S113 read for shape; `corpus/SOURCES.md:7` is the column header row, `:104`
is S098 and `:119` is the last row S113 — the item said "S098–S127", but the file ends at S113).

```
| S??? | earlyoom README at tag v1.9.0 — https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md | tool | A | earlyoom v1.9.0 release documentation only: the both-below-limits act rule, the SIGTERM-then-SIGKILL stage order, where actions are logged, the journalctl grep advice and the v1.9.0 changelog entry; not the post-1.9.0 upstream master README (S016), not the message grammar itself (kill.c/main.c), not host state | act rule:28,53-56,239-240; stage order:145-146,235-236,388; log destination:154,259; journal advice:170-186; changelog v1.9.0:283-287; kernel-oom absence:65-67,383,289-293 (0 hits for `kernel-oom` in the v1.9.0 README, MANPAGE and main.c; the flag was added upstream on 2026-02-02, after this tag); tag v1.9.0 = commit 202d4db0d308ca6478f68de68b46cae34896ddaf (2025-09-16); file sha256 23411dbfd8b409d433f984a5d6677830e86a383ec76935fc1e1d675e6b4374dd; HTTP 200, 19931 B, opened 2026-10-22 | The release README states that earlyoom acts only when available memory and free swap are both below their limits, escalates SIGTERM to SIGKILL at a second lower limit, logs every action to stderr, and offers `journalctl -u earlyoom \| grep sending` for reading those actions; this release has no `--kernel-oom` option, so the kernel-oom delegation that S016 documents from upstream master does not exist in the 1.9.0 binary running on this host. | mined | 2026-10-22 | on-release | corpus/knowledge/userspace-oom-killers-r26.md |
```

Tier reason (A): the release-matched upstream project documentation, fetched by direct URL from
the canonical `raw.githubusercontent.com` ref, with the byte digest and the tag's commit recorded.
It is primary for what the tool documents about itself; the registry already treats the upstream
master README of the same project as tier A (S016, `corpus/SOURCES.md:22`).

Status reason (`mined`): the file is in scope, quotable and useful, and it is the only artifact
that states the act rule and the logging destination in the release the host runs. It does not
repeat S016 (different ref, different bytes, different claims) and it is not a re-open of a
rejected row.

Flip (the condition that would reverse this): if the round's entry cites S016 for the
`--kernel-oom` delegation as a fact about this host's earlyoom, this row's scope is wrong and the
entry must be corrected instead — see finding F1.

`used-by` is written as `corpus/knowledge/userspace-oom-killers-r26.md` because the contract
requires that entry's `source:` line to cite at least one row opened in round 26
(`.ufo/waves/round-26/contract.md:24`). If the L1 wires a different consumer, that cell changes
only.

## 3. Facts the round can rest on (each with its v1.9.0 README line)

| # | Fact | Line(s) |
|---|---|---|
| A1 | Act rule is a conjunction: available memory **and** free swap must both be below their limits, otherwise earlyoom does nothing. | 28, 53-56, 239-240 ("Note: both memory and swap must be below minimum for earlyoom to act.") |
| A2 | Default threshold is 10% of user-available memory; the victim is the largest process by `oom_score`. | 28, 53-56 |
| A3 | Kill is staged: SIGTERM at the first limit, SIGKILL at a second, lower limit (default `PERCENT/2`). | 145-146 (startup thresholds), 235-236 ("earlyoom sends SIGTERM once below PERCENT, then SIGKILL once below KILL_PERCENT (default PERCENT/2)."), 388 (changelog v1.2, 2018-10-28: "Implement staged kill: first SIGTERM, then SIGKILL, with configurable limits") |
| A4 | Every action is logged to stderr; `--syslog` switches to syslog instead of the standard streams. | 154 ("Every action is logged to stderr."), 259 ("--syslog use syslog instead of std streams") |
| A5 | As a systemd service, the log is readable with `systemctl status earlyoom` (last 10 lines) and the "Checking Logs" section gives `sudo journalctl -u earlyoom \| grep sending`. | 154-159, 170-186 (advice at 175) |
| A6 | For older earlyoom versions the README advises `sudo journalctl -u earlyoom \| grep -iE "(sending\|killing)"`. | 183-186 |
| A7 | v1.9.0 changelog entry (2025-09-16): adds `-P /path/to/script` (run before killing), more debug logging for `-n`/`-N`, and "Also log oom_score_adj when killing something". | 283-287 |
| A8 | v1.9.0 contains **no** `--kernel-oom` option. The section "Why not trigger the kernel oom killer?" says earlyoom does not use `echo f > /proc/sysrq-trigger`; the `-k` kernel-oom option was removed in v1.2 and is "now ignored for compatibility". | 65-67, 383 ("Remove option to use kernel oom-killer (`-k`, now ignored for compatibility)"), 289-293 (the v1.8.2 entry, which touches only the systemd unit file) |
| A9 | The version that introduced the current kill-log wording with `cmdline` is **v1.8** (2024-04-15): `kill.c` at v1.8:539 is `sending %s to process %d uid %d "%s": oom_score %d, VmRSS %lld MiB, cmdline "%s"`, while `kill.c` at v1.7:377 has no `cmdline` and still says `badness`. The `cmdline` suffix was put on the same line by upstream commit 75340657e692 (2024-04-08) and the `badness`→`oom_score` rename by 5c452f908638 (2024-04-10); v1.9.0 then added `oom_score_adj` (cbf0bb2e5d99, 2025-09-13). | 287 (v1.9.0 changelog), 299-305 (v1.8 entry), 295-297 (v1.8.1 entry: "Fix trivial test failures caused by message rewording", commit bfde82c001c6, 2024-04-16 — this reworded the *startup threshold* line, upstream commit 8bf16e10b1ef, 2024-04-15) |
| A10 | The README's own sample kill line (README:180) still shows the pre-v1.8 shape (no `cmdline`, no `oom_score_adj`); it was brought up to the current format only on 2026-09-29 (upstream commit 48348938a8ff), after the v1.9.0 tag. The README's usage block header (230) and startup sample (143) likewise still say `earlyoom v1.8`, and 143 is even typo'd `eearlyoom v1.8`. | 143, 180, 230 |
| A11 | The v1.9.0 README documents no `escalating to SIGKILL`, `kill failed:` or `low memory!` wording at all; those strings exist only in the C sources (`kill.c:318`, `kill.c:654`, `main.c:519`/`main.c:523` at the same tag). | README has 0 hits for `escalat`, `kill failed`, `low memory!` (87 is unrelated: "low memory situations") |

## 4. Flags against the round-26 contract

**F1 — `--kernel-oom` does not exist in earlyoom 1.9.0, but the corpus asserts it does.** The
superseded entry `corpus/knowledge/userspace-oom-killers-r12.md` (Evidence bullet on S016) says
"only `--kernel-oom` delegates to the kernel OOM killer" and cites S016's README at upstream master
commit `8477c902fce09be26e5668acba05df216871e7ae` (`corpus/SOURCES.md:22`). That master README
does contain `--kernel-oom` (README at that commit, lines 68-69), but the flag was added upstream on
2026-02-02 (commit 750a7c0d97bb), which is **after** the v1.9.0 tag (2025-09-16). Verified on this
host: `pacman -Qi earlyoom` → `Version : 1.9.0-1`; `strings -a /usr/bin/earlyoom | grep -c kernel-oom`
→ `0`; `strings -a /usr/bin/earlyoom | grep -n "Option -k"` → `Option -k is ignored since earlyoom
v1.2`; `MANPAGE.md` at v1.9.0:86-87 says `-k` "removed in earlyoom v1.2, ignored for compatibility".
The v1.9.0 README has 0 hits for `kernel-oom` (only the prose at 65-67 and the changelog at 383).
Consequence: the r26 entry must not carry the `--kernel-oom` delegation forward as a fact about the
installed binary; S016's `teaches` cell is a master-branch statement and the new row (scope
`kernel-oom absence`) bounds it to the release. This is a content correction for the L1, not a
contract contradiction — the contract's C2 grammar never mentions `--kernel-oom`.

**F2 — the contract's grammar is right to anchor on the C sources, not on this README.** The
contract's message grammar (`.ufo/waves/round-26/contract.md:80-89`) quotes `sending SIGTERM to
process `, `escalating to SIGKILL after `, `kill failed: `, `low memory! at or below SIGTERM
limits`, `dryrun mode enabled`, `earlyoom <version>`, `sending SIGTERM when mem avail <= <a>% and
swap free <= <b>%,` and `SIGKILL when mem avail <= <c>% and swap free <= <d>%` with file:line
citations to `main.c`/`kill.c` at tag v1.9.0. I re-fetched `main.c` and `kill.c` at the tag and
checked every cited line number: all seven anchors match the contract exactly
(`main.c:161`, `main.c:295`, `main.c:414`, `main.c:416`, `main.c:519`, `main.c:523`; `kill.c:318`,
`kill.c:627`, `kill.c:654`). No contradiction found. But the README alone would have produced two
wrong grammar rules: it shows no `cmdline` in its sample line (README:180, finding A10) and it
shows no `escalating`/`kill failed`/`low memory!` strings at all (A11). A corpus row that cites
this README for the message grammar would be unsound; cite `kill.c`/`main.c` rows for that.

**F3 — the version token on this host carries no leading "v".** The startup line is produced by
`main.c:161` as `"earlyoom " VERSION`, where `VERSION` is `git describe --tags --dirty`
(`Makefile` at v1.9.0:3). The Arch build embeds `1.9.0`, not `v1.9.0`: the installed binary contains
the literal `earlyoom 1.9.0` (`strings -a /usr/bin/earlyoom`), and the live journal line for this
boot is `earlyoom 1.9.0`. The README's own samples say `v1.8` (143, 230). A reader that requires a
leading `v` will not match the host. The contract's `earlyoom <version>` rule is fine; the L1
should make sure the tool's regex does not assume the `v` prefix.

**F4 — the act rule is stated as a conjunction in prose, which supports the contract's threshold
grammar but is not a code citation.** README:239-240 ("Note: both memory and swap must be below
minimum for earlyoom to act.") and 28/53-56 back the "memory AND swap" reading. The MANPAGE at
v1.9.0:20 and :41-44 says the same ("If **both** memory **and** swap (if any) are below 10% …",
"SIGTERM once **both** available memory **and** free swap are …"). The README is a fair citation
for the rule's wording; the code citation for the emitted thresholds remains `main.c:414`/`416`.

**F5 — nothing in the contract's C1/C2 wording is contradicted by this README.** The contract's
host facts (earlyoom 1.9.0 active and enabled, systemd-oomd inactive and disabled) are host
readings, not README claims. My independent read agrees:
`systemctl show earlyoom.service -p LoadState,ActiveState,UnitFileState,ActiveEnterTimestamp` →
`LoadState=loaded`, `ActiveState=active`, `UnitFileState=enabled`,
`ActiveEnterTimestamp=Thu 2026-10-22 04:55:44 -03`; `systemctl show systemd-oomd.service` →
`loaded` / `inactive` / `disabled`.

**F6 — a sibling seat's draft r26 text carries the false `--kernel-oom` clause forward.** The
rewrite seat's draft (`.ufo/waves/round-26/w1/DraftR12Corrections.md:71`) keeps the sentence
"only `--kernel-oom` delegates to the kernel OOM killer" in the proposed new text. On this host
that sentence is false: earlyoom 1.9.0 has no `--kernel-oom` option at all (F1). It is true of
upstream master (S016's ref). This is a cross-seat conflict I cannot resolve from my seat — the
rewrite seat owns that file — so I report it verbatim: the clause should either be dropped or
re-scoped ("upstream master, after v1.9.0"). My own row (§2) is scoped so that it does not repeat
the claim.

**F7 — my row overlaps the tag-history seat's row; the L1 must merge them, not file both.**
`.ufo/waves/round-26/w1/SrcEarlyoomTagHistory.md:130` drafts a row whose source list includes
`https://raw.githubusercontent.com/rfjakob/earlyoom/v1.9.0/README.md` and whose scope is the
message-grammar prefixes across tags v1.7/v1.8/v1.9.0. That seat's scope is the C sources and the
tag history; mine is the README's own documentation (act rule, log destination, journalctl advice,
v1.9.0 changelog, kernel-oom absence) at the release tag, with no C-source scope. The scopes are
separable but the README URL appears in both rows. I recommend the L1 file one row: either mine
(narrow, README-only) plus the tag-history row without the README URL, or the tag-history row
widened to carry the README documentation points. I have not edited the sibling's report.
Both rows cite `corpus/knowledge/userspace-oom-killers-r26.md` as `used-by`, which is correct —
that entry needs a source line that cites round-26 rows.

## 5. Host-side corroboration (read-only, count-only, no MESSAGE text)

I ran the contract's own journal scope to check that the grammar the README documents is what the
host actually emits. Counts only; no process name, uid, command line or MESSAGE text is reproduced
here.

```
journalctl -q -b -u earlyoom.service -o json --output-fields=MESSAGE,__MONOTONIC_TIMESTAMP
  → 13 boot lines, all 13 with __MONOTONIC_TIMESTAMP >= 19964362 (ActiveEnterTimestampMonotonic)
  → 1 version line, 1 "sending SIGTERM when mem avail …" line, 1 "SIGKILL when mem avail …" line
  → 0 "sending SIG…to process", 0 "escalating to SIGKILL", 0 "kill failed", 0 "low memory!", 0 "dryrun"
The two threshold lines carry the values 10.00 / 10.00 and 5.00 / 5.00, matching the contract's
host-shaped quiet case (thresholds 10.00/10.00/5.00/5.00) and README:145-146.
```

This is corroboration for the tool seat's fixture, not a claim of my own: I did not build or run
`tools/mori-oom-killers.py`.

## 6. Side files I opened (all at tag v1.9.0, digests for the L1)

```
main.c                 sha256 08656b0bc90c85f23738661456b25c97af908bc5e2cfea78e0a69697b5f9d0e4
kill.c                 sha256 b32e0fad65e298235102f98aff37e02c94400b544d454cb57192ae697b100bf3
MANPAGE.md             sha256 cc48b02e79255ae27bad9b2c49364fcae1b6b5eb20fe8e83ecef432f360dfeda
msg.h                  sha256 e36604984a916fb00a624c27c73034bcd87d7d6facff9b290a6a561ee58de56c  (PRIPCT at :10)
meminfo.h              sha256 5b709094c507ba418a5284034614141bd48893b5a8fe1863214c46396aefb52f
Makefile               sha256 b852cb9b832729f37f2b19fe93956720a5a58017aa8f76a6036cc928d96127ae  (VERSION at :3)
kill.c at v1.7         sha256 1453cd2a6a48de4bafef6032b40c421e433270fddd1bcc94e85a83d80ec65af8  (no cmdline, :377)
kill.c at v1.8/v1.8.1/v1.8.2  sha256 459af5589d6cc092303dcc1e27783557e8a91e2820565a08fc5094bc87054133 (cmdline, :539)
README at v1.8         sha256 eb44f415cc2c1e66da912ab70ed755d36032c44fb80d8049a665287c6a961368
README at v1.8.1       sha256 2946ba59ab89708fe924870ed3feb7f71b4416267f1b1d8d7b00370408ca2ac0
README at v1.8.2       sha256 df050c085bc992bef805af058b5b88b3f870a5f4d5178112689152f0a08f4f00
README at master 8477c902  sha256 b2a34e354d122fd756672a1a4014ec5382144e41451291c9d84fd6458c30826c  (S016's ref; differs from the tag)
```

`PRIPCT` is `"%5.2lf%%"` (`msg.h:10`), which is why the SIGKILL threshold prints as ` 5.00%`
(right-aligned in five columns). The contract's `<c>%` placeholder must tolerate that leading
space — the live host line reads `mem avail <=  5.00%` with two spaces. Flagging this for the tool
seat and the case seat: a strict single-space pattern would miss the SIGKILL threshold line.

## 7. Upstream commits cited by A9 (each fetched and digested)

```
75340657e692 2024-04-08 "kill_process: put cmdline on same log line"   json sha256 50d12993ab824e7fa7fe62dcebad9e931421988a1a8476ee814bda90e0112537
5c452f908638 2024-04-10 "Rename \"badness\" -> \"oom_score\""           json sha256 042956aae0776b72ac89483fda9f6cfa0d85ff18d5d901666a447b9dffc486ac
8bf16e10b1ef 2024-04-15 "Match startup message wording to log lines"   json sha256 3cb61ecb4394d57b61571aa95556b62eebbdf190eca53a095243a11b18bfd1f1
bfde82c001c6 2024-04-16 "Fix trivial test failures caused by string changes" json sha256 da3d8dff6d7d404290970efed8d6c51219214a480e64420874c4a68d9fa46b45
cbf0bb2e5d99 2025-09-13 "Also print oom_score_adj when killing something" json sha256 a58a719c430a21edf58155908d928a871e0f1de615a2e0e9130a088be3965b04
48348938a8ff 2026-09-29 "README: update kill log line example to current format" json sha256 655a92daba82c5eb7350521fa7dceefb608eac5dc204f7af52ed90ed0defe5ce
750a7c0d97bb 2026-02-02 "kill: option for triggering kernel oom killer" json sha256 54e366d46d99fcbaa746d906940139d11261758c12670e1aed9e76bbad10873e
```

All were read through the public GitHub REST API and the public `raw.githubusercontent.com` raw
tree; no browser, no bot challenge, no access control.

## 8. Tooling and environment

No tool was installed or upgraded by this seat: the task needed only `curl`, `python3`, `sha256sum`
and `git` (read-only). Per the operator directive I would have installed through pacman/uv, but the
host-wide pacman pause in the round-26 item bounds makes pacman unavailable, and no
missing tool blocked the work, so nothing was installed. Nothing needs installing for the L1.
Versions used: curl 8.23.0, Python 3.14.8, git 2.56.0, sha256sum (GNU coreutils) 0.8.0, uv 0.13.0
(present, unused).

## 9. Out of scope for this seat

The `--kernel-oom` correction to `corpus/knowledge/userspace-oom-killers-r12.md` and to S016's
`teaches` cell, the C1 rewrite, the r26 entry text, the tool and its fixtures, and any row other
than the one in §2 are L1 or sibling-seat work; I report the facts and let the owner act.
