# ReviewInherited — round-28 inherited paths

Scope: verify the six inherited paths and the census correction against the round-29 contract and L1 disposition. Lane tip reviewed: `8809a3fe1eaa87a0afa177a15263d174378e7462` (`git rev-parse HEAD`). No installs or upgrades; no tools to record.

## Findings by severity

**Low — MutHeadingCheck contains an uncorrected false secondary claim.** The committed `.ufo/waves/round-28/w2/MutHeadingCheck.md:64-66` says `git log --follow` does not help and returns nothing. The wave-1 re-review says this is not reproduced: on git 2.56.0, `--follow` returns the actual authoring commit in its fixture; it calls for an erratum in the lesson (`.ufo/waves/round-29/w1/ReviewLateMutHeadingCheck.md:67-72,98-101`). The current round-29 lesson lists the file as re-verified/committed but does not record that caveat (`corpus/lessons/round-29.md:81-87`). The principal finding remains supported; record the erratum in the lesson before closing this disposition.

## Per-path verdicts

1. **`.scratch/` — disposition appropriate; untouched.** LOG records it as pre-round and untouched (`LOG.md:1915`). Lane `git status --porcelain` reports it untracked; `stat` reports directory mtime `2026-10-21 17:05:28`, before this round's 2026-10-22 start. I did not inspect or alter its contents.
2. **`.ufo/waves/round-28/wave1-run.err` — committed as evidence; appropriate.** LOG records the 0-byte file committed at `3a147138` (`LOG.md:1915-1916`). `git show 3a147138:.ufo/waves/round-28/wave1-run.err | wc -c`, `git show HEAD:... | wc -c`, and worktree `wc -c` each returned `0`.
3. **`.ufo/waves/round-28/w1/FixR1Runway.md` — disposed out of lane; privacy disposition appropriate.** SHA-256 of `/fast/scratch/hyaku/mori-r29/L1/disposed/FixR1Runway.md` is exactly `da1e1bf4f53ba83fc72715b640d8c09833a6fb9a8805113624557bb2a293b691`; file size is 65,826 bytes. This matches LOG's recorded abbreviated digest and size (`LOG.md:1916-1917`). `git rev-list --all -- .ufo/waves/round-28/w1/FixR1Runway.md | wc -l` returned `0`. I did not copy or quote its content.
4. **`.ufo/waves/round-28/w2/MutCountC1Amended.md` — commit-as-evidence appropriate; privacy scan clean.** SHA-256 of the committed `e1c6bbe7` blob and current file both equals `dc118b9fa5974ce034616ab25bb91a2b5bdb9ed5a05e3f24aa53b3b816a09451`. Its core six-mutant/survivor account aligns with the re-review table (`w1/ReviewLateMutCountC1Amended.md:40-51`); both correctly disclose M8's fix was not verified end-to-end (`w2/MutCountC1Amended.md:117-118`; re-review `:99-101,160-163`).
5. **`.ufo/waves/round-28/w2/MutHeadingCheck.md` — commit-as-evidence appropriate with the Low caveat above; privacy scan clean.** SHA-256 for committed and current bytes matches: `700b6cd6a1410e1e31ab006daaa2a61500e50192cf83bfbe7462f22dd5fad0aa`. The re-review confirms the main rename and version findings, but flags the `--follow` assertion as an erratum (`w1/ReviewLateMutHeadingCheck.md:35-47,67-72`).
6. **`.ufo/waves/round-28/w2/MutTipReceiptCheck.md` — commit-as-evidence appropriate; privacy scan clean.** SHA-256 for committed and current bytes matches: `2379b7961386c47e7998f45e83bc289bc381b05eab080d34baae1690a3de5b5e`. The wave-1 re-review reports all 32 fixture verdicts match and separately identifies the superseded real-lane/fleet situation (`w1/ReviewLateMutTipReceiptCheck.md:29-45,99-121`); the source report scopes those old-state observations to `f2de0ee` (`w2/MutTipReceiptCheck.md:108-122`).

The byte comparisons above are SHA-256 comparisons of each committed blob at `e1c6bbe7` against its current worktree file. ReviewLate reports identify those exact files as their inputs and describe their findings; they do not supply hashes for the report files themselves, so no stronger input-hash claim is made. LOG records the three as re-verified and committed (`LOG.md:1918-1919`).

Privacy screening: searched the three Mut files for uid/pid, user-session unit, journal/session, OMP, `/etc/default`, and `--prefer`/`--avoid`/`--ignore` markers; no matches. The three ReviewLate reports independently describe their privacy scans as clean (`ReviewLateMutCountC1Amended.md:143-151`; `ReviewLateMutHeadingCheck.md:90-94`; `ReviewLateMutTipReceiptCheck.md:150-156`). This is a literal scan, not semantic proof. I did not read protected host settings. No LSP device is mounted (`read xd://lsp` returned “No such tool”; mounted devices list only `ast_edit`, `debug`); this documentation/disposition review has no code caller or definition queries.

## Census correction

The appended note in `corpus/lessons/round-28.md:160-166`, landed at `3a147138`, corrects the end count to ten W04: six carried plus S147-S150. The recorded round-29 start receipt contains those same ten W04 rows and ends `mori\tok\t…/corpus/SOURCES.md`, `exit: 0` (`.ufo/waves/round-29/evidence/census-start.txt`; read output). The correction is supported; no census defect found.

## Residual risk and verification gaps

The substantive behavior of the three mutation reports was reviewed by their wave-1 reviewers; I did not rerun their mutation harnesses. Their review reports record that evidence and its limitations. The only actionable residual found here is the unrecorded `--follow` erratum noted above.

Report: .ufo/waves/round-29/w2/ReviewInherited.md
