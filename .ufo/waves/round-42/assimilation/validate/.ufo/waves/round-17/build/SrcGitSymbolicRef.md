# SrcGitSymbolicRef — S047 draft (wave 1, round 17)

Scribe: SrcGitSymbolicRef. Leaf member; no subagent dispatch. Lane: /home/vgpnk/Projects/shokunin/mori-shokunin (entering tip 24526ea). Nothing under corpus/ or the lane checkout was edited; this file is the only write.

## Source observed

- URL: https://git-scm.com/docs/git-symbolic-ref
- Accessed: 2026-10-20 (UTC 18:54 Z, two fetches)
- Fetch 1: reader/markdown extraction (tool `read`, trafilatura). Shows the manual's SYNOPSIS, DESCRIPTION, OPTIONS, NOTES sections and the version-history table entry "2.48.1 → 2.56.0 no changes" (no line numbers reliable in the extraction).
- Fetch 2: raw HTML via `curl -fsSL --max-time 60 <url> | tr '\n' ' ' | grep -o`, stdout only, no file written. Used to check quotes verbatim. HTML entity `&lt;name&gt;` decodes to `<name>`.
- Exit codes: curl/grep pipeline exit=0 (both quote greps matched).
- Tool installs/updates: none.

## Located quotes (verbatim, from the raw HTML)

Q1, OPTIONS > `-q`, `--quiet` (24 words):
> Do not issue an error message if the <name> is not a symbolic ref but a detached HEAD; instead exit with non-zero status silently.

Q2, NOTES, exit-status sentence (18 words in the quoted fragment; full sentence begins "git symbolic-ref will exit with status 0 if the contents of the symbolic ref were printed correctly,"):
> with status 1 if the requested name is not a symbolic ref, or 128 if another error occurs.

Q2 is the only place the manual states numeric exit codes. Q1 is the only place it states the detached-HEAD behavior under `-q`.

## Row draft (column format of corpus/SOURCES.md, Registry table)

| S047 | git-symbolic-ref manual — https://git-scm.com/docs/git-symbolic-ref | docs | A | `git symbolic-ref` reading HEAD, and the `-q` detached-HEAD exit contract | OPTIONS > -q, --quiet: "Do not issue an error message if the <name> is not a symbolic ref but a detached HEAD; instead exit with non-zero status silently."; NOTES exit-status sentence: "with status 1 if the requested name is not a symbolic ref, or 128 if another error occurs"; page history "2.48.1 → 2.56.0 no changes"; accessed 2026-10-20 | Under `-q`, a detached HEAD is a silent non-zero exit (status 1 per NOTES), distinct from the 128 used for other git errors; a probe must branch on exit status, not infer detachment from empty stdout alone. | queued | 2026-10-20 | on-release | — |

Notes on the row:
- Anchor cells use section names, not line numbers, because the extraction's line numbers are not reliable (see the SOURCES.md correction note on S014/S015).
- Status `queued`: opened and quotes located; no corpus lesson or knowledge note cites it yet. `used-by` stays `—` until a note lands (planned consumer: corpus/knowledge/jj-branch-anchor-r17.md, provisional).
- Tier A: primary upstream documentation for the git binary the census calls.

## Gate line (draft)

Gate S047: https://git-scm.com/docs/git-symbolic-ref, accessed 2026-10-20; located quote (OPTIONS > -q, 24 words, verbatim): "Do not issue an error message if the <name> is not a symbolic ref but a detached HEAD; instead exit with non-zero status silently."

## Relevance to C2 (census branch resolution), as teaching

- The contract's `detect_branch` order is `symbolic-ref -q HEAD` → `refs/remotes/origin/HEAD` → unique of `refs/heads/master`/`refs/heads/main` (contract.md, C2). The `-q` step is the one the manual documents for the detached case: it returns non-zero silently rather than printing an error.
- S044 (jj git-compatibility, the sibling row) records that colocated jj workspaces commonly have a detached Git HEAD. That is the case where the `-q` fallback path is taken. Whether the census hits that path in this lane is not observed here [INFERENCE].
- The doc gives status 1 for "not a symbolic ref" and 128 for other errors. A census that treats any non-zero result identically would merge a detached HEAD with a git failure; the gate should assert the distinction, not the doc's wording [INFERENCE from Q2].

## Limits

- Documentation only. No `git symbolic-ref` was run; the exit-status values above are the manual's statements, not observed behavior in this environment [INFERENCE that the installed git matches the page].
- The page's version-history table shows the text unchanged across 2.48.1 → 2.56.0; the manual does not name a single version for this page beyond that table.
- Not verified: whether the installed git prints the `-q` silence exactly; no probe run (not in this item's allowed commands).
- Quotes are from the fetched 2026-10-20 HTML; a later page revision may change wording and should be rechecked on-release.

## Findings for the wave

1. S047 draft is ready for L1 to fold into corpus/SOURCES.md. Gate quote is 24 words (≤25) and was matched in raw HTML.
2. No conflicts with existing S-rows (S044 describes the same detached-HEAD condition from the jj side; no duplicate URL in the registry).
3. Not edited: corpus/SOURCES.md, MANIFEST.json, .ufo/state, lane checkout, sibling reports.
