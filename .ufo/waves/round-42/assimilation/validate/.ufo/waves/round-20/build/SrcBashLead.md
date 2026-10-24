# SrcBashLead: GNU Bash manual, pipefail and PIPESTATUS (SOURCES.md `## Leads (unopened)`)

Verdict: the lead is partly resolved. The GNU **web** manual was unreachable from this host (every requested URL timed out, with no TCP connect). The same manual **source** was opened from the official GNU FTP tarball, which is reachable. Pipefail and PIPESTATUS are located there, with a verified signature. The web URL itself is still unopened, and the web text was not compared with the tarball text.

## Web URLs tried (all failed)

Reader tool (`read`) and `curl -sS -m 25` both used. curl reports `connect=0.000000` for every timeout, so no TCP connection was made.

| URL | Result |
|---|---|
| https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html | reader: timed out; curl: exit 28, timed out after 25 s |
| https://www.gnu.org/software/bash/manual/html_node/Pipelines.html | reader: timed out; curl: exit 28, timed out after 25 s |
| https://www.gnu.org/software/bash/manual/html_node/Bash-Variables.html | reader: timed out; curl: exit 28, timed out after 25 s |
| https://www.gnu.org/software/bash/manual/bash.html | reader: timed out; curl: exit 28 (run twice, both timed out) |
| https://www.gnu.org/software/bash/manual/bash.html/ | curl: exit 28, timed out after 25 s |
| https://www.gnu.org/software/bash/manual/ | curl: exit 28, timed out after 25 s |
| https://git.savannah.gnu.org/cgit/bash.git/plain/doc/bash.texi | HTTP 301 to https://cgit.git.savannah.gnu.org/cgit/bash.git/plain/doc/bash.texi (11 s). Following it with `-L`: exit 28, timed out after 60 s, 0 bytes |
| https://raw.githubusercontent.com/bminor/bash/master/doc/bash.texi | HTTP 404 (matches the lead's note) |

Reachable, for context: https://ftp.gnu.org/gnu/bash/ (HTTP 200), https://savannah.gnu.org/projects/bash/ (HTTP 200).

## Source opened instead

- https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz: HTTP 200, 11,355,854 bytes, sha256 `0d5cd86965f869a26cf64f4b71be7b96f90a3ba8b3d74e27e8e9d9d5550f31ba`. Contains `bash-5.3/doc/bashref.texi` (11,553 lines), which is the GNU Bash Reference Manual source. `patchlevel.h` defines `PATCHLEVEL 0`.
- Signature: https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz.sig (HTTP 200, 95 bytes, binary). Verified with `/usr/bin/gpg` against the official keyring https://ftp.gnu.org/gnu/gnu-keyring.gpg (HTTP 200, 3,698,125 bytes), in a throwaway GNUPGHOME under /tmp/bashlead. Result: `Good signature from "Chet Ramey <chet@cwru.edu>"`, key fingerprint `7C01 35FB 088A AF6C 66C6 50B9 BB58 69F0 64EA 74AB`. gpg also warned that the key is not certified by a trusted signature. That warning is expected for an uncertified keyring and was not resolved.
- Tools: no installs or updates. Used existing `curl` and `/usr/bin/gpg`. No pacman or system changes.

## Located passages (bashref.texi, bash-5.3 tarball; `@code{}` markup removed in the quotes)

1. **pipefail option, The Set Builtin**, `doc/bashref.texi:6062-6066`:
   > If set, the return value of a pipeline is the value of the last (rightmost) command to exit with a non-zero status

   22 words. Lines 6063–6064. The same item states that the option is disabled by default (line 6066).

2. **Pipelines section, exit status**, `doc/bashref.texi:837-840`:
   > If pipefail is enabled, the pipeline's return status is the value of the last (rightmost) command to exit with a non-zero status

   22 words. Lines 839–840. Line 837 says the exit status is that of the last command unless `pipefail` is enabled.

3. **PIPESTATUS, Bash Variables**, `doc/bashref.texi:7489-7492`:
   > An array variable containing a list of exit status values from the commands in the most-recently-executed foreground pipeline

   18 words. Lines 7490–7492. Lines 7492–7496 add that PIPESTATUS is also set after simple commands and subshells, so the array is overwritten by later commands.

Also present, not quoted: `doc/bashref.texi:4804` and `:5943` say a command in a pipeline other than the last is exempt from errexit only "subject to the state of the pipefail shell option". `:11029` says `set -o pipefail` makes a pipeline fail if any command fails.

## Proposed SOURCES.md row (not appended; id S066 is the next unused id, since the registry ends at S065)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S066 | GNU Bash Reference Manual (doc/bashref.texi, bash-5.3 tarball) — https://ftp.gnu.org/gnu/bash/bash-5.3.tar.gz | docs | A | pipefail pipeline exit status and PIPESTATUS array semantics | The Set Builtin, pipefail item:6062-6066; Pipelines:839-840; Bash Variables, PIPESTATUS:7489-7492; tarball sha256 0d5cd86965f869a26cf64f4b71be7b96f90a3ba8b3d74e27e8e9d9d5550f31ba; detached signature verified good (Chet Ramey, key 7C01 35FB 088A AF6C 66C6 50B9 BB58 69F0 64EA 74AB; uncertified); web manual unreachable | With pipefail the pipeline status is the rightmost non-zero status; PIPESTATUS holds per-command statuses only for the most recent foreground pipeline and is overwritten by later commands, so capture it immediately after the pipeline. | queued | 2026-10-21 | 180d | candidate: corpus/lessons/2026-10-15-errexit-pipefail-silent-crash.md; corpus/lessons/2026-10-15-selftest-grep-sigpipe-race.md |

Notes on the row:
- Tier A, because it is the GNU project's own manual source with a verified signature. Its scope is the 5.3 tarball, not the live web page.
- The "capture it immediately" phrasing in `teaches` is an inference from "most-recently-executed" and "sets PIPESTATUS after ... simple commands" (`:7492-7496`). It is not a quoted instruction.
- `used-by` lists lessons that already rely on pipefail and PIPESTATUS behavior (for example `errexit-pipefail-silent-crash` and `selftest-grep-sigpipe-race` discuss PIPESTATUS capture and rightmost-non-zero pipeline status). They are candidates, not verified citations. The lead's "Leads (unopened)" line should be removed or closed only by the L1 integration owner.
- Status: `queued`, since no knowledge note cites S066 yet. The L1 may set `mined` once a citing note exists.

## Recommended handling for the lead line

- Keep the web-URL failure record above, so the next attempt can start from this list.
- Replace the `## Leads (unopened)` entry with a pointer to S066 once the L1 admits the row.
- Recheck the web manual at a later date. Until then, the web page itself is unopened, and the row must not claim the web page matches the 5.3 tarball.

## Scope and limits

- Read-only with respect to the fleet repo, lane repos and host services. The only writes were this report, `/tmp/bashlead` scratch files, and a throwaway GPG home in `/tmp/bashlead/gh`.
- No subagents spawned (leaf seat). No builds, linters or selftests run.
- Not observed: the web manual's current text; whether it matches bash-5.3 exactly; bash behavior on the host (not tested).
- No row was appended to `corpus/SOURCES.md`, and no lesson or knowledge file was edited.
