PARTIAL

Scope: S070 row (corpus/SOURCES.md:76), Leads line (corpus/SOURCES.md:115), Gate row (corpus/lessons/round-20.md:45), resolution sentence (corpus/lessons/round-20.md:50-51). Source re-opened by me: https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz, member bash-5.3/doc/bashref.texi (11553 lines, sha256 f3d37d57a1061e24d266051de9bd47ffa43dc86584afea11576c535ad2be32d5).

Holds: identity, tarball hash and signature, both anchors, Gate quote and word count, scope, tier, Gate-to-registry agreement. Broken: two of three teaches clauses, and used-by completeness against live lane use.

## Per-field verdicts

1. Source identity and kind (docs; GNU Bash 5.3 manual in the release tarball): HOLDS. Member bash-5.3/doc/bashref.texi exists in the tarball.
2. Tarball sha256 0d5cd869...31ba (row anchor): HOLDS. `sha256sum bash-5.3.tar.gz` -> 0d5cd86965f869a26cf64f4b71be7b96f90a3ba8b3d74e27e8e9d9d5550f31ba, exit 0. Identical to SOURCES.md:76.
3. Provenance (extra check): HOLDS. `gpg --verify bash-5.3.tar.gz.sig bash-5.3.tar.gz` against the official GNU keyring (https://ftp.gnu.org/gnu/gnu-keyring.gpg, sha256 0fe55175b96a8ea1c4b670cc3fe11d56b341e4eff81b161ea49958ae550be6ca) -> "Good signature from Chet Ramey <chet@cwru.edu>", key 7C0135FB088AAF6C66C650B9BB5869F064EA74AB, exit 0. The "not certified" warning is the scratch keyring's default trust.
4. Anchor bashref.texi:6063-6064 (set -o pipefail): HOLDS. Line 6062 is `@item pipefail`; 6063-6065 carry the sentence; the item sits in "The Set Builtin" (node at 5887).
5. Anchor bashref.texi:7490-7492 (PIPESTATUS): HOLDS. Line 7489 is `@item PIPESTATUS`; 7490-7492 read "An array variable ... containing a list of exit status values from the commands in the most-recently-executed foreground pipeline".
6. Gate quote verbatim at the stated location: HOLDS. Cross-line grep matched 6063-6064: "If set, the return value of a pipeline is the value of the last" / "(rightmost) command to exit with a non-zero status". The only difference is the wrapped newline, rendered as a space.
7. Gate quote <=25 words: HOLDS. 22 words.
8. Scope "bash 5.3 only": HOLDS. doc/version.texi:7-8 `@set EDITION 5.3`, `@set VERSION 5.3`. Host `bash --version` -> 5.3.20(1)-release.
9. Tier A: HOLDS. Upstream project manual shipped in a signed release. The registry gives the same tier to other official project docs (S066, S068, S069). The tier does not overstate the source.
10. teaches clause 1, "With pipefail a pipeline returns the rightmost nonzero status": HOLDS. Manual 835-841 and 6063-6065. Host test A: `set -o pipefail; (exit 3) | (exit 4) | (exit 0)` -> status=4.
11. teaches clause 2, "so a consumer that exits early can fail a guarded pipeline": BROKEN as an S070 claim. The manual has no SIGPIPE or early-exit text: grep for SIGPIPE, early and exits-early returns no such hit (only "nearly" substrings), and the Pipelines node 769-845 was read in full. The clause is also outside the row's own stated scope. The clause is true on this host: test E `set -o pipefail; yes | head -n1` -> status=141; test F `if yes | head -n1` under pipefail -> guard=fail. The mechanism is SIGPIPE, which the row does not cite. [INFERENCE] S031 supplies it; S031 was not opened here.
12. teaches clause 3, "PIPESTATUS keeps every stage status": BROKEN as written. Manual 7490-7492 scopes PIPESTATUS to the most-recently-executed foreground pipeline. Lines 7495-7499 say Bash also sets it after simple commands. Test C: `(exit 3) | (exit 4) | (exit 0); echo mid; echo after_mid=${PIPESTATUS[*]}` -> after_mid=0. "Every stage" holds only until the next foreground command. (In test E, PIPESTATUS=0 is the intervening echo, the same overwrite.)
13. Status "queued" vs used-by "-": HOLDS (registry convention). Rows read: queued and rejected rows carry "-" (S005, S017, S042, S048 queued; S030, S055 rejected). Mined rows list paths (S031, S034). The Gate says "Admit A, queued" (round-20.md:45) and agrees.
14. "used-by paths exist and cite S070": HOLDS, vacuously. used-by is "-", so there are no paths to check.
15. used-by completeness against live use: BROKEN. corpus/knowledge/verdict-contract-r13.md applies the same rule without citing S070. Lines 42-43: "The census runs `set -euo pipefail` (`:236`), so the pipeline's status is the rightmost non-zero element: 141". Lines 49-51: pipefail promotes the producer's status to the pipeline verdict. Lines 224-227: "S031 ... does not model bash's pipeline status rule ... Those are the r9 lesson and the in-repo comments, not the man page." Grep `S070|bashref|Reference Manual|bash\(1\)|bash manual|GNU Bash` on that file -> No matches. SOURCES.md:91 says the Bash claim stays linked to existing lessons "until its authoritative manual is reachable". S070 is that manual, and no link was added, while SOURCES.md:115 and round-20.md:50-51 say the lead is "resolved".
16. Gate row vs registry row (URL, access 2026-10-21, tier A, queued, location 6063-6064): HOLDS.
17. Opened 2026-10-21: HOLDS (fetched today). Recheck "on-release": [INFERENCE] cadence not checkable here.

## Routed fixes (not applied; lane files are read-only to me)

- Narrow S070 teaches to manual-grounded text, for example: "With pipefail, a pipeline's status is that of the rightmost command exiting non-zero (0 if none); PIPESTATUS holds the statuses of the most recently executed foreground pipeline." Carry the early-exit or SIGPIPE consequence only with S031 cited in the row, or in its own row.
- Either cite the manual for the rule in verdict-contract-r13.md (bashref.texi:835-841 and 6063-6065), then set S070 to mined with that used-by path; or change "resolved" at SOURCES.md:115 and round-20.md:50-51 to "source admitted; linkage pending".
- SOURCES.md:113 heading "## Leads (unopened)" now holds a resolved item (cosmetic).
- Not opened (outside the named set): corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md, named at verdict-contract-r13.md:51-52 as the rule's origin. [INFERENCE] It is a second uncited user.
- Online manual https://www.gnu.org/software/bash/manual/bash.html: `curl -m 25` timed out (exit 28) on 2026-10-21. Consistent with SOURCES.md:115 ("web manual still timed out").

## Tooling and bounds

- Installs or updates: none. Used host /usr/bin/curl, tar, gpg, sha256sum, and bash 5.3.20(1)-release.
- Scratch: /tmp/reopen-s070 (tarball, extracted doc/bashref.texi and doc/version.texi, scratch GNUPGHOME, GNU keyring). The two gpg calls without GNUPGHOME were read-only (list or verify); nothing was imported into the default keyring.
- Lane: no production file edited; no git or jj; no subagents; census not run; no reads of .ufo/interactive-sessions/, .ufo/worktrees/ or .jj/. Greps limited to corpus/SOURCES.md, corpus/lessons/round-20.md, corpus/knowledge/verdict-contract-r13.md (named in S031's used-by), and the extracted manual files.
