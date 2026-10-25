# ScribeLog — append-only LOG correction review (round-46 wave 1)

Scope: review the round-46 append-only `LOG.md` correction for **exact command**, **count**, and **bounded wording**. Read-only review; no repo mutation, no tool installs.

## Object under review

`LOG.md:2655-2657` (file tail), "## Round-46 correction — round-45 freeze-manifest tally":

> The round-45 entry above and report say the freeze manifest verified 29/29. The non-author verifier's exact command was `grep -v '^#' .ufo/waves/round-45/evidence/freeze-r45.txt | sha256sum -c`; it reports **27 OK**, rc 0. There are 28 non-comment lines, including one blank line, and 27 checks. The digests and successful verification stand; only the stated tally was wrong.

## 1. Append-only compliance

- The correction is a **new section appended at the end** of `LOG.md` (lines 2655-2657; file total 2657 lines, nothing follows it).
- The historical round-45 entry is **untouched**: `LOG.md:2637` still reads "freeze manifest `sha256sum -c` clean (29/29)" — the false tally remains in place as a record, exactly what append-only requires (cf. `corpus/lessons/round-45-verifier-spotcheck.md:37`: "`LOG.md` is append-only, so it needs a named correction entry").
- Independent corroboration of the correction's content exists at `corpus/lessons/round-45-verifier-spotcheck.md:33-37` (the non-author verifier's measurement) and `SCORECARD.md:2557` (references the round-46 LOG correction).

## 2. Exact command

The quoted command matches the source verifier report verbatim: `corpus/lessons/round-45-verifier-spotcheck.md:34` — "I measured `grep -v '^#' .ufo/waves/round-45/evidence/freeze-r45.txt | sha256sum -c` → **27 OK**, rc 0 (28 non-comment lines, one blank)."

I executed the exact command at the lane root (read-only):

```
$ grep -v '^#' .ufo/waves/round-45/evidence/freeze-r45.txt | sha256sum -c
SKILL.md: FAILED
corpus/SOURCES.md: FAILED
corpus/README.md: OK
… (25 more OK) …
sha256sum: WARNING: 2 computed checksum(s) did NOT match
RC=1
```

This matches `sha256sum -c` semantics: the two `#` header lines and the external-census comment line are stripped; the single blank line (line 3) is silently skipped by `sha256sum -c` (no "improperly formatted" warning), leaving exactly 27 check lines. At the *current* worktree the same command gives 25 OK + 2 FAILED (`SKILL.md`, `corpus/SOURCES.md`), rc 1 — expected, because those two files changed after the round-45 freeze (SKILL.md is the object of this repair wave). The correction is about the round-45 committed state, not HEAD; see §4.

## 3. Counts

Structural counts of `.ufo/waves/round-45/evidence/freeze-r45.txt` (working copy byte-identical to the round-45 landing revision `baabc992` — manifest sha256 `72c6130c…` at both the worktree and revision `qxksmnzo`):

| measure | correction's claim | measured |
|---|---|---|
| total lines | — | 31 |
| comment lines (`#` at line start) | — | 3 (lines 1, 2, 31) |
| non-comment lines after `grep -v '^#'` | 28 | 28 |
| blank lines among them | 1 | 1 (line 3) |
| active checks | 27 | 27 |
| result at `baabc992` | 27 OK, rc 0 | 27 OK, rc 0 |

Reproduction at the round-45 landing change: for each of the 27 non-comment, non-blank manifest lines I hashed the pinned path at revision `qxksmnzo` (= `baabc992`) via `jj file show` and compared to the manifest's recorded sha256: **27/27 match, 0 mismatches** → the quoted command at that state reports exactly 27 OK, rc 0. The prior "29/29" tally is false under every reading (31 total lines − 3 comments = 28 non-comment; 27 checks; a "29" is not derivable from the file structure).

## 4. Bounded wording

"The digests and successful verification stand; only the stated tally was wrong."

- **Verified bounded.** The assertion of standing digests is scoped to the round-45 committed bytes: at `baabc992` all 27 digests hold (§3). The correction does not overclaim completeness (the external census line remains a comment, per the manifest's own header), does not claim a standing result at HEAD, and does not assert the "29/29" claim was right in any other respect.
- **State-dependence is implicit, not stated.** The claim "it reports 27 OK, rc 0" is only true at the frozen round-45 state (or any state where the pinned files still match); at the current repaired worktree the identical command returns rc 1 with 25 OK. The wording remains accurate — the correction names the verifier's measurement, not a HEAD run — but a reader executing the command at the round-46 tip would not observe rc 0. This is a documentation nuance, not a falsity: the correction's own object ("round-45 freeze-manifest tally") is historical.
- The existing round-45 entry's "(29/29)" remains in place and is explicitly superseded by the appended correction, consistent with the lane's append-only convention.

## Findings

1. The correction is genuinely append-only (tail addition, history untouched).
2. The quoted command is exact and matches the independent verifier report verbatim.
3. All stated counts are exactly correct: 28 non-comment lines, 1 blank line, 27 checks, 27 OK rc 0 at `baabc992` (reproduced 27/27).
4. The wording is bounded; "29/29" is confirmed false and the corrected tally is accurate.
5. Only caveat: "27 OK, rc 0" holds at the round-45 committed state, not at the current (repaired) tip, where SKILL.md and corpus/SOURCES.md have since changed — consistent with this wave's repair premise, and not contradicted by the correction's text.

Reproducibility: commands used — `wc -l`, `grep -vc '^#'`, `grep -c '^$'`, `sha256sum -c` (exact quoted command), `jj file show -r qxksmnzo` per pinned path. No files were modified; no git/jj mutations; no installs.
