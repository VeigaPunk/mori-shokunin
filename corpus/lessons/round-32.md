author: mori-shokunin L1 MoriR32A2 (round 32, attempt 2)

# mori round 32 — lesson

## What the round learned

- The lane's 34 `mined` source rows whose URL is not pinned to a tag or commit were opened live together as one
  population (many had been re-opened one by one in earlier rounds, M1) (frozen selector, `.ufo/waves/round-32/c1-population.json`). 33 served bytes and still carry the
  passages their `teaches` cells rest on, per the seats' verdicts and the judge receipt. One (S056, pnas.org) sits
  behind a bot challenge and is recorded `unreachable`. Seats proposed no `drifted` verdict.
- What changed on the live pages is presentation, not substance: Python docs moved 3.15.0 → 3.15.1, docs.kernel.org
  now renders as Linux 7.3.0, and two RFC URLs redirect to `rfc-editor.org/info/…`. The numeric line anchors of S002 and
  S045 no longer index today's raw HTML (wave-1 Recheck002, Recheck045). They are locators, not facts.
- A frozen token-overlap rule cannot tell a supporting quote from an on-topic one. The control wave showed it before
  data (`.ufo/waves/round-32/evidence/c1-controls.txt`), so the judge carries the semantic check.

## Recheck

| id | url | accessed | sha256 | quotes | verdict |
|---|---|---|---|---|---|
| S001 | https://docs.kernel.org/accounting/psi.html | 2026-10-23T01:31:22Z | f752c8d5447760a315048037eb8f53007f8e4862d58617264f587cccd8798258 | "The ratios (in %) are tracked as recent trends over ten, sixty, and three hundred second windows"; "The total absolute stall time (in us) is tracked and exported as well"; "The trigger will de-register when the file descriptor used to define the trigger is closed" | current |
| S002 | https://docs.kernel.org/admin-guide/cgroup-v2.html | 2026-10-23T01:31:23Z | b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b | "Note that all fields in this file are hierarchical"; "Similar to memory.events but the fields in the file are local to the cgroup i.e. not hierarchical"; "oom_kill The number of processes belonging to this cgroup killed by any kind of OOM killer" | current |
| S007 | https://www.freedesktop.org/software/systemd/man/latest/systemd-oomd.service.html | 2026-10-23T01:31:25Z | 56460ffb24d7ea3ccd771b7f834a460786b646038411c0744b981ad532af6f0a | "select a cgroup to terminate, and send SIGKILL to all processes in it"; "only descendant cgroups are eligible candidates for killing"; "systemd-oomd periodically polls PSI statistics for the system and those cgroups to decide when to take action" | current |
| S012 | https://github.com/systemd/systemd/security/advisories/GHSA-652q-wxr6-h5j6 | 2026-10-23T01:31:23Z | a51157e7c5de1389832e31abe2064c786f971ba1ade9d25e0945b2fc56898052 | "Local unprivileged users can terminate arbitrary local processes via a systemd-oomd IPC API due to a missing path traversal validation."; "Affected versions >= 250 Patched versions 261 260.3 259.7 258.9" | current |
| S014 | https://www.freedesktop.org/software/systemd/man/latest/journalctl.html | 2026-10-23T01:31:24Z | 75440570fb1f71859229ca88fed0a6764b2057c7dd90651701b3d022a5649722 | "The following options control where to read journal records from"; "Start showing entries from the location in the journal after the location specified by the passed cursor"; "A comma separated list of the fields which should be included in the output" | current |
| S015 | https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | 2026-10-23T01:31:25Z | 906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7 | "The human-readable message string for this entry. This is supposed to be the primary text shown to the user"; "A 128-bit message identifier ID for recognizing certain message types"; "Fields prefixed with an underscore are trusted fields" | current |
| S031 | https://man7.org/linux/man-pages/man7/pipe.7.html | 2026-10-23T01:31:21Z | 22809fe16836722f0359b10b59b4c0971cf3edf6ffb26528c41bd1a383f2a58e | "If all file descriptors referring to the read end of a pipe have been closed"; "a write(2) will cause a SIGPIPE signal to be generated for the calling process" | current |
| S037 | https://www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html | 2026-10-23T01:31:25Z | 906e5d34b38913ddaf729f74f468f5511f8a143bb3f86f0fdda06957af7bf5e7 | "The name of a unit. Used by the system and user managers when logging about specific units"; "the systemd unit name, the unit name in the systemd user manager (if any)"; "of the process the journal entry originates from" | current |
| S039 | https://www.freedesktop.org/software/systemd/man/latest/sd_journal_seek_cursor.html | 2026-10-23T01:31:24Z | b13d9928c1ea07a6a75dfe80d2227405c1f3ea6ac5b708219bef44fe15f6cd7b | "If no entry matching the specified cursor is found the call will seek to the next closest entry (in terms of time) instead."; "these calls do not actually make any entry the new current entry" | current |
| S040 | https://www.freedesktop.org/software/systemd/man/latest/sd_journal_test_cursor.html | 2026-10-23T01:31:25Z | 5ada44c28aa31dc7495276e2bf6a11a3370e33ae71277051736641882e5e9980 | "the same entry might be referred to by multiple different cursor strings, and hence string comparing cursors is not possible"; "whether the entry being sought to was actually found in the journal or the next closest entry was used instead"; "Seeking to a cursor position without the specific entry being available locally will seek to the next closest (in terms of time) available entry" | current |
| S041 | https://www.rfc-editor.org/rfc/rfc6585 | 2026-10-23T01:31:23Z | 3924746f977d3bd8b086fe275ccd67dc344271753e355cc9eaa9d7e698f0886b | "The 429 status code indicates that the user has sent too many requests in a given amount of time"; "Note that this specification does not define how the origin server identifies the user, nor how it counts requests"; "MAY include a Retry-After header indicating how long to wait before making a new request" | current |
| S043 | https://docs.z.ai/api-reference/api-code | 2026-10-23T01:31:27Z | 4a6ac09770cabd93d0e16a65bfc23669e85b019c23e28ddb74ea33e88d82feb4 | "1302 429 Rate limit reached for requests"; "1113 429 Insufficient balance or no resource package. Please recharge."; "1308 429 Usage limit reached" | current |
| S044 | https://docs.jj-vcs.dev/latest/git-compatibility/ | 2026-10-23T01:31:27Z | db9c9a760810386858e6b1bad4a7a334c56bd48c77692dbc1c343657ae0ca254 | "jj commands will usually put the Git repo in a \"detached HEAD\" state"; "since in jj there is not concept of a \"currently tracked branch\""; "either have no branches at all (not even a main branch) or will have branches that are out of date with jj's bookmarks" | current |
| S045 | https://docs.jj-vcs.dev/latest/cli-reference/ | 2026-10-23T01:31:22Z | 5df178565d444fbc99dc4459cdd7c80ac09b67069eb7b22405d3a45c053089ef | "Update the author to the configured user This updates the author name and email."; "The author timestamp is not modified - use --update-author-timestamp to update the author timestamp." | current |
| S046 | https://git-scm.com/docs/git-merge-base | 2026-10-23T01:31:24Z | 0dc2f88a4935851e824b3d35c8236d7d4ad4603554b2ff24cc25ec83962868f3 | "Check if the first <commit> is an ancestor of the second <commit>"; "exit with status 0 if true, or with status 1 if not"; "Errors are signaled by a non-zero status that is not 1" | current |
| S047 | https://git-scm.com/docs/git-symbolic-ref | 2026-10-23T01:31:22Z | 0d2ea49c643107a5fbb4c74f944114c48fe13152158b8255ceb4e71bea20791c | "Do not issue an error message if the <name> is not a symbolic ref but a detached HEAD; instead exit with non-zero status silently"; "with status 1 if the requested name is not a symbolic ref, or 128 if another error occurs" | current |
| S049 | https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html | 2026-10-23T01:31:23Z | 604378c015d263638d7fd3c066762e7da7ed104be7fa974223f085b5bf330bb9 | "should usually not be recorded directly in the logs, but instead should be removed, masked, sanitized, hashed, or encrypted"; "Session identification values (consider replacing with a hashed value if needed to track session specific events)"; "If a field is malformed, omit or safely replace that field and record the validation failure with bounded, safe context" | current |
| S051 | https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf | 2026-10-23T01:31:26Z | 555b9df82af12de4ca887efc21c0a9e159a14485d5d570f44b32ef15c6c62470 | "If the PII serves no current business purpose, then the PII should no longer be used or collected."; "Develop a schedule for periodic review of PII holdings"; "Disposal of PII should be conducted in accordance with the retention schedules approved by the National Archives and Records Administration" | current |
| S052 | https://opentelemetry.io/docs/security/handling-sensitive-data/ | 2026-10-23T01:31:25Z | 6104b09c73e65514ed10d7eea302bcdaed88fa12982cd77e5b3049d0df949f80 | "Only collect data that serves an observability purpose."; "Hashing the ID or name of a user may not provide the level of anonymization you need"; "hashes are reversible in practice if the input space is small and predictable" | current |
| S056 | https://www.pnas.org/doi/10.1073/pnas.1708274114 | 2026-10-23T01:31:22Z | - | - | unreachable |
| S058 | https://git-scm.com/docs/git-rev-list | 2026-10-23T01:31:23Z | 6eca09d9ef21dd4270ff2c73cac7ee26964aebc470f4dfc52705eb27749ce65f | "By default, the commits are shown in reverse chronological order."; "--topo-order Show no parents before all of its children are shown, and avoid showing commits on multiple lines of history intermixed."; "--reverse Output the commits chosen to be shown (see Commit Limiting section above) in reverse order." | current |
| S062 | https://www.rfc-editor.org/rfc/rfc8785 | 2026-10-23T01:31:23Z | 4dd9f775b3e6b5977df3e43c56c4e7530be988f9bf8fc0d5b5be202aafae76c9 | "Property name strings to be sorted are formatted as arrays of UTF-16"; "Whitespace between JSON tokens MUST NOT be emitted."; "occurrences of NaN or Infinity MUST cause a compliant JCS implementation to terminate with an appropriate error" | current |
| S064 | https://git-scm.com/docs/git-rev-parse | 2026-10-23T01:31:24Z | 64c603545b3f9799cc9525228ba70cf80444a063b32a4be37de2a5ca09b83421 | "Verify that exactly one parameter is provided, and that it can be turned into a raw 20-byte SHA-1"; "it is wise to use --end-of-options so that the name argument is not mistaken for another option"; "git rev-parse --verify --end-of-options $REV^{commit} This will error out if $REV is empty or not a valid revision" | current |
| S067 | https://michaelfeathers.silvrback.com/characterization-testing | 2026-10-23T01:31:23Z | 5d706e27809602eeeb566fd8baf0a569d7f42adc985f9d4f13a18b4dae70de16 | "The purpose of characterization testing is to document your system's actual behavior, not check for the behavior you wish your system had."; "We can see them as descriptions of what we have rather than statements of correctness." | current |
| S068 | https://docs.python.org/3/library/os.html | 2026-10-23T01:31:23Z | 2ac87dd3ac1f30a3210cb1631c5bd41f3708f100cbeeb2b5874ea4b29e17d993 | "Perform the equivalent of an lstat() system call on the given path. Similar to stat() , but does not follow symbolic links."; "This function normally follows symlinks; to stat a symlink add the argument follow_symlinks=False , or use lstat() ."; "If follow_symlinks is False , and the last element of the path to operate on is a symbolic link" | current |
| S069 | https://docs.python.org/3/library/pathlib.html | 2026-10-23T01:31:30Z | a5cfbc6b1fc4d570c434f1b737547ea87a3f964dd79b15e42ff01627b6fe85f0 | "This function is part of PurePath and works with strings. It does not check or access the underlying file structure."; "it assumes that no symlinks are present in the path; call resolve() first if necessary to resolve symlinks"; "When walk_up is false (the default), the path must start with other" | current |
| S071 | https://kubernetes.io/docs/concepts/architecture/controller/ | 2026-10-23T01:31:24Z | 96ad0ef9661c7a3fff3b360ce9643a6c1bc120bcec52b82385c94481194581cb | "These objects have a spec field that represents the desired state."; "The controller(s) for that resource are responsible for making the current state come closer to that desired state." | current |
| S073 | https://docs.python.org/3/library/pathlib.html | 2026-10-23T01:31:35Z | a5cfbc6b1fc4d570c434f1b737547ea87a3f964dd79b15e42ff01627b6fe85f0 | "This function is part of PurePath and works with strings. It does not check or access the underlying file structure."; "it assumes that no symlinks are present in the path; call resolve() first if necessary to resolve symlinks"; "This can impact the walk_up option as it assumes that no symlinks are present in the path" | current |
| S074 | https://kubernetes.io/docs/concepts/architecture/controller/ | 2026-10-23T01:31:24Z | 96ad0ef9661c7a3fff3b360ce9643a6c1bc120bcec52b82385c94481194581cb | "The controller(s) for that resource are responsible for making the current state come closer to that desired state."; "The thermostat acts to bring the current state closer to the desired state, by turning equipment on or off."; "Your cluster could be changing at any point as work happens and control loops automatically fix failures." | current |
| S076 | https://michaelfeathers.silvrback.com/characterization-testing | 2026-10-23T01:31:23Z | 5d706e27809602eeeb566fd8baf0a569d7f42adc985f9d4f13a18b4dae70de16 | "The purpose of characterization testing is to document your system's actual behavior, not check for the behavior you wish your system had."; "This is particularly useful when we want to refactor or rewrite. We can run our tests and find out immediately whether we've changed behavior." | current |
| S117 | https://api.github.com/repos/rfjakob/earlyoom/tags | 2026-10-23T01:31:22Z | 423c43617a2a299315180292f43447936f6ddde01efff5baece3fc46ed8b1869 | "\"name\": \"v1.9.0\", \"zipball_url\": \"https://api.github.com/repos/rfjakob/earlyoom/zipball/refs/tags/v1.9.0\", \"tarball_url\": \"https://api.github.com/repos/rfjakob/earlyoom/tarball/refs/tags/v1.9.0\", \"commit\": { \"sha\": \"202d4db0d308ca6478f68de68b46cae34896ddaf\""; "\"name\": \"v1.8\", \"zipball_url\": \"https://api.github.com/repos/rfjakob/earlyoom/zipball/refs/tags/v1.8\", \"tarball_url\": \"https://api.github.com/repos/rfjakob/earlyoom/tarball/refs/tags/v1.8\", \"commit\": { \"sha\": \"62625072ce8671f497a5cea5fc3db63226469093\""; "\"name\": \"v1.7\", \"zipball_url\": \"https://api.github.com/repos/rfjakob/earlyoom/zipball/refs/tags/v1.7\", \"tarball_url\": \"https://api.github.com/repos/rfjakob/earlyoom/tarball/refs/tags/v1.7\", \"commit\": { \"sha\": \"ebaea9526bcee14889b00d83a9dd3d038315cee2\"" | current |
| S128 | https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html | 2026-10-23T01:31:22Z | 769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9 | "Acceptable values range from -1000 (OOM_SCORE_ADJ_MIN) to +1000 (OOM_SCORE_ADJ_MAX)."; "The value of oom_score_adj is added to the badness score before it is used to determine which task to kill."; "a new process inherits its parent's oom_adj setting. A process must be privileged ( CAP_SYS_RESOURCE ) to update this file" | current |
| S137 | https://api.github.com/repos/rfjakob/earlyoom/commits?path=main.c | 2026-10-23T01:31:25Z | b658df9d6c52fd46c43db155022dd22c75e46fdd0abb86323ebcfc5c208bf775 | "kill: option for triggering kernel oom killer"; "This implements an option for trigger the kernel oom killer" | current |
| S149 | https://man7.org/linux/man-pages/man5/proc_pid_oom_score_adj.5.html | 2026-10-23T01:31:22Z | 769edf3b9c054934db07f16173297fc5fd63c3a4c807682355f08fa45cde80a9 | "root processes are given 3% extra memory over other tasks"; "a new process inherits its parent's oom_adj setting. A process must be privileged ( CAP_SYS_RESOURCE ) to update this file"; "Acceptable values range from -1000 (OOM_SCORE_ADJ_MIN) to +1000 (OOM_SCORE_ADJ_MAX)." | current |

## Gate (rows opened 2026-10-23 in round 32)

Five candidates opened by wave-1 seats. Three were admitted (SrcCurlMan, SrcUnicodedata, SrcHtmlUnescape), and each copy is
committed unchanged at `corpus/evidence/sources-r32/S###.src`. Two were rejected, S178 and S179, both opened by recheck
seats while they checked a row's second source. The L1 changed one seat-drafted SOURCES cell: S176's
`opened` value `2026-10-23T01:31:32Z` became `2026-10-23`, because the census rejects a timestamp there (E08).

| id | url | accessed | sha256 | quotes | decision |
|---|---|---|---|---|---|
| S175 | https://curl.se/docs/manpage.html | 2026-10-23T01:31:33Z | `9d2b36d00af7240f77480e911ce28346113419dd3eb5ebca1d8cc50284cfe5ca` | Options > -f, --fail (24 words): "Fail with error code 22 and with no response body output at all for HTTP transfers returning HTTP response codes at 400 or greater."; Options > -L, --location (11 words): "this option makes curl redo the request to the new place."; Options > -m, --max-time (13 words): "Set the maximum time in seconds that you allow each transfer to take."; Exit codes > 28 (12 words): "Operation timeout. The specified time-out period was reached according to the conditions." | admit, A, mined |
| S176 | https://docs.python.org/3/library/unicodedata.html | 2026-10-23T01:31:32Z | d3d261bcde4906ce9685d8e362a7bbb0dc4b254b1fc12f70ec46a9db65e77375 | unicodedata.normalize entry, valid form values, S176.src:516-517 (10 words): "Valid values for form are 'NFC', 'NFKC', 'NFD', and 'NFKD'."; NFKC definition, S176.src:534-536 (15 words): "The normal form KC (NFKC) first applies the compatibility decomposition, followed by the canonical composition."; NFKD definition, S176.src:533-534 (19 words): "The normal form KD (NFKD) will apply the compatibility decomposition, that is, replace all compatibility characters with their equivalents." | admit, A, mined |
| S177 | https://docs.python.org/3/library/html.html | 2026-10-23T01:31:26Z | 650c53ac7695b816427335a6fbdf3852c41c01d7458f3b502c2af4e916441bb0 | html.unescape(s) entry, first sentence (7 words): "Convert all named and numeric character references"; html.unescape(s) entry, first sentence (9 words): "in the string s to the corresponding Unicode characters"; html.unescape(s) entry, second sentence (18 words): "This function uses the rules defined by the HTML 5 standard for both valid and invalid character references" | admit, A, mined |
| S178 | https://git-scm.com/docs/git-diff-tree | 2026-10-23T01:31:59Z | `72cce59764c2ea86f06904bf1805564a3fa7047f2f424ce24620f296bc811523` | OPTIONS `-m` (13 words): "-m By default, git diff-tree --stdin does not show differences for merge commits." | reject, duplicate URL: the page is already the second URL of S058's source cell (`corpus/SOURCES.md:64`); opened by wave-1 Recheck058 to check S058's diff-tree half, copy kept at `corpus/evidence/recheck-r32/S058-difftree.src` as uncounted evidence |
| S179 | https://pmc.ncbi.nlm.nih.gov/articles/PMC5856500/ | 2026-10-23T01:31:43Z | `ccc65da58d4f56b6c91fa13a87dc9a2f34af7eab9c0cee6be83a3d3aa166201b` | article body (19 words): "In prediction, the problem of forking paths is avoided because the analytic pipeline is specified before observing the data" | reject, same work as S056 (Nosek et al. 2018, PNAS 115(11):2600-2606): a mirror row would duplicate S056's teaches cell and would not recheck S056's URL; opened by wave-1 Recheck056 (accessed time is the copy's file mtime), copy kept at `corpus/evidence/recheck-r32/S056-pmc-mirror.html` as uncounted evidence that the article text is unchanged |

Status changes this round: none to existing rows. New rows S175–S177 are `mined` and used by
`corpus/evidence/recheck-r32/README.md`. New rows S178 and S179 are `rejected`. The counter's new-source check lists both
under `new_failures` (status not `mined`), which is expected.

## Mistakes

- **M1 — a frozen contract said the population rows were never re-opened, and that was false (class: unverified
  provenance assertion).** Evidence: `.ufo/waves/round-32/contract.md:17-18` (frozen at `29f7d043`) says every
  population row "was last opened in the round that added it". Wave-1 CriticAxisFit F4 showed S014 and S015 re-opened
  in rounds 13 and 14 (`.ufo/waves/round-32/w1/CriticAxisFit.md:60-66`). The L1's sweep at the base lists earlier
  `Reopen*` seats for S041, S043–S047, S068, S117, S128 and S137, and more leads
  (`.ufo/waves/round-32/evidence/m1-reopen-sweep.txt`). Effect on the claim: none on P-C1, which counts round-32 rows
  and never reads the sentence. The axis framing is narrower than written: this round is the first recheck of the 34
  rows as one population with committed copies and a bound judge, not the first re-open of each row.
  Captured-by: none before the freeze; QUALITY 25 (state the scope measured) is nearest. Fix: QUALITY 96. Shown able to
  fail: the sweep output above contradicts the frozen sentence. The contract is not edited.
- **M2 — counter code was run on a real draft before the counter was final (class: premature use of mutable counter code on draft data).** Evidence: the round-31 timeline records SrcPidMax importing `count-c1.py` helpers on its own drafted S173 Gate row; this was a format check only, with no `main()` or predicate verdict (`corpus/lessons/round-31-verifier-spotcheck.md:41-53`). The closure routes the same defect and requires keeping counter code away from real drafts until final (`corpus/lessons/round-31-verifier-spotcheck.md:221-223`). Captured-by: the non-author verifier's timeline review (`corpus/lessons/round-31-verifier-spotcheck.md:3,41-53,221-223`). Fix: freeze the counter before any data seat, let seats run it only after the freeze commit, and make no later changes (`.ufo/waves/round-32/contract.md:78-79`); the C0 receipt records the frozen counter and control wave before data seats (`.ufo/waves/round-32/evidence/c1-controls.txt:1-3`). Shown able to fail: the round-31 timeline is the negative case—the 23:46–23:47 real-draft helper run preceded A1 at 23:52:48Z, while the closure says the counter was still open to amendment (`corpus/lessons/round-31-verifier-spotcheck.md:36,41-42,52,221-223`). A freeze-order check must reject that ordering; the current C0 receipt records control-wave runs, not an automated rejection of a pre-freeze real-draft run (`.ufo/waves/round-32/evidence/c1-controls.txt:1-3,8-23`).
- **M3 — "the same sentence" held only after whitespace was normalised (class: parity claimed at the wrong
  level).** Evidence: the P-C1 sentence wraps at different columns in `contract.md:32-34` and the `count-c1.py:7-9`
  docstring. A byte diff differs, and a whitespace-normalised diff is equal (wave-1 ReviewCounterContract finding 1,
  `.ufo/waves/round-32/w1/ReviewCounterContract.md`). The receipt label `.ufo/waves/round-32/evidence/c1-controls.txt:4-6`
  is a third wrapping. Captured-by: the round-31 closure §8 item 3 asked for the same sentence, but no check names its
  comparison level. Fix: later rounds state the predicate's parity check as
  `diff <(tr -s ' \n' ' ' < A) <(tr -s ' \n' ' ' < B)` over the extracted sentence and paste its exit code. Shown able
  to fail: a plain byte comparison of the two extracts differs.

## Attacks on the data and how they were settled

The judge (JudgeRecheck, reviewer, non-author) agreed on all 34 rows
(`.ufo/waves/round-32/judge/JudgeRecheck.md`, judged section sha `251bf664…8407` at `837b2802`). Attack seats raised the
findings below. None changes a row. Each finding is kept here as an open disagreement with the judge, not closed.

| Finding | Seat | Judge's reading | Disposition |
|---|---|---|---|
| S128 Q3 and S149 Q2 end before ", although a process can always increase its own oom_adj", which drops the exception to the privilege rule | AttackQuoteBounds F1 | no dropped negation: all quote boundaries sit on spaces or punctuation | open; the quote is under the 25-word cap only because it is cut; a later recheck should quote the whole sentence |
| S044 Q3 is from the non-colocated paragraph; S051 Q3 omits the litigation-hold clause; S062 Q1 stops before "code units" | AttackQuoteBounds F2–F4 | the other quotes in each row carry the teaches cell | open, low |
| S058 is quoted on the rev-list half only; the diff-tree half rests on an uncommitted seat fetch | ReviewMultiSource 1, CriticAxisFit F1 | `current` on the part of the teaches cell the population URL carries, plus no contradiction | open: the frozen first-URL population cannot carry a second URL (README Limits) |
| S117 quotes share no teaches-cell tokens; the tags listing carries none of the grammar claims | ReviewMultiSource 2, AttackQuoteBounds, CriticAxisFit F1 | the listing still maps the tags to the same commits, which pins the code the teaches cell rests on | open: re-certified through the tag-to-commit chain, not observed on the page |
| S128/S149 kernel and score-page clauses are not on the quoted page | ReviewMultiSource 3 | same first-URL reading | open |
| S071's mori clause is lane doctrine, not page text | AttackQuoteBounds, ReviewMultiSource 5 | honest: the row's own scope excludes it | agree with judge |
| five rows' live bytes differ from the copies (per-request tokens, asset fingerprints); every quote is still in the live text | AttackCopies | — | expected; README Limits |

The judge read one rule more loosely than the contract's wording: on the five multi-source rows, `current` means the
part the population URL carries still holds and nothing contradicts the rest. The judge stated this
(`JudgeRecheck` finding 1). The L1 did not change it. The closure may read "supports the teaches cell" strictly, and
then S058, S117, S128, S149 and S137 fail R4 and C1 is a miss. Both readings are recorded here.

## Counter review findings (frozen counter; none applied)

ReviewCounterContract lists 25 divergences between the docstring and the code (`.ufo/waves/round-32/w1/ReviewCounterContract.md`). The ones that
bear on this round's data: R5 skips non-`corpus/knowledge/` used-by paths, so a `drifted` S001 (used by a lesson only)
would need no correction (no row is `drifted`, so this is unexercised). The accessed-time regex accepts invalid dates.
Table parsing breaks on a blank line inside the table (the committed table has none). R3 accepts any one of three live
fetches. The C0 control findings (`evidence/c1-controls.txt`) are unchanged.

## Corrections to the contract's descriptive text (append-only; predicate unaffected)

- `contract.md:17-18` "every one was last opened in the round that added it": false, see M1.
- `contract.md:19-20` "their bytes cannot drift" (pinned rows): too strong. A git tag can be force-moved
  (CriticAxisFit F3). Read it as: tag and commit URLs are treated as pinned, and tag movement is not measured.
- `contract.md:10-12` anti-loop rationale: the campaign rule is the same axis and surface (or the same routed-defect
  class) three rounds running (CriticAxisFit F5). Depth was worked twice, not three times. Freshness satisfies the rule
  either way.
- The population is "first URL, conventionally unpinned" (CriticAxisFit F3): S058's second URL, S117's tag-pinned code
  files and the S060 in-toto `blob/main` files are outside it.

## Routed defects (round-31 closure §8) — disposition

| Defect | Disposition | Evidence |
|---|---|---|
| 1 M5 correction | appended to `corpus/lessons/round-31.md`: the masked set is the 9 fixtures F02, F06–F08, F10, F11, F13, F15, F16 across three rules; the ten that end on a list entry are a different set | wave-1 ExecM5Witness (`/fast/scratch` script output pasted in `.ufo/waves/round-32/w1/ExecM5Witness.md`; EOF-drop mutant `exact=7/16` vs `27/27`) |
| 2 gate registry row and frozen baseline | SKILL.md `## Round32 — blind-writer gate registry row` with all eight fields; frozen run `.ufo/waves/round-32/frozen/blind-check/` with `expected.json` pinning every input digest; `verify.sh` → `frozen_run: match` exit 0, tampered input → `snapshot_tampered` exit 2, mutated tool → exit 1 | `.ufo/waves/round-32/evidence/blind-baseline/verify-{green,tampered,muttool,missing}.txt`; L1 re-run of `verify.sh` in round 32: `frozen_run: match`, exit 0 |
| 3 `count-c2.py` docstring omits "no hit line outside the 16 briefs" | recorded in `.ufo/waves/round-32/contract.md` routed item 3; frozen round-31 file untouched | `git diff 641a6e86 HEAD -- .ufo/waves/round-31/count-c2.py` empty |
| 4 judge-vs-tip drift | R4 binds `judged-sha256` to the measured tip section; QUALITY 95 | `.ufo/waves/round-32/evidence/c1-after.txt` (`section_sha256=251bf664…`, `judge_ok=True`) |
| 5 counter code on real drafts | counter frozen at `29f7d043` (01:10:09Z) before C0 (dispatched after `f44e428e`, 01:11:44Z) and wave 1 (dispatched 01:30:57Z); M2 above | `git log 641a6e86..master` |
| 6 carried C2 ambiguities and tool edge cases | pinned as 12 evidence fixtures, no tool change: setext and indented headings, CRLF, fenced `# files opened`, `-\t`, `../` through an allow glob, words inside the heading, lead-in prose, a sub-heading in the block, plus 3 controls; 4 diverge from the primary rule-text reading (E01, E02, E03, E06) | `.ufo/waves/round-32/fixtures/edge/fixtures/edge-r32.json` (sha `79b530f6…`); copy `edge/` to a scratch dir before running `run-edge-r32.py`, which builds a sandbox git repo beside itself |
| 6 round-30 detector false positives/negatives, FR5 census probe | carried unchanged | — |

## Census and sweep

- Round start (`29f7d043`): `sources-census.sh validate … mori` → `mori ok`, exit 0, twelve W04
  (`.ufo/waves/round-32/evidence/census-start.txt`).
- Round end (after S175–S177): `mori ok`, exit 0, twelve W04 lines, the same pre-existing duplicate-URL notices
  (`.ufo/waves/round-32/evidence/census-end.txt`). One E08 during integration (S176 `opened` held a timestamp) was fixed
  before the data commit (Gate note).
- No-harm retention scan: metric 4 at `8abb90a3` and 4 at the base `641a6e86`
  (`.ufo/waves/round-32/evidence/tip-retention.txt`).
- Tip receipt: `count-c1.py 8abb90a3` → `rows_ok=34/34`, `new_ok=3`, `C1=met exit=0`
  (`.ufo/waves/round-32/evidence/tip-c1.txt`). The section sha is unchanged since the judged revision (`251bf664…`).
- Fleet-root misroot sweep (`git -C /home/vgpnk/Projects/shokunin status --porcelain`): untracked `.omp/mcp.json`,
  `AGENTS.md`, `bm.json`, `live_s228.html`, `nama.html`, `s395.txt`, `tf_bavelas.html`, `wb2.html` and a pycache file.
  None names mori round 32, and every mtime is before the attempt-2 dispatch at 01:01Z. None was moved.
- Attempt 1 (`MoriR32`) left `.scratch/` only. Nothing from it was reused.
