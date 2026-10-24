# ExecLessonGate — round-37 lesson Gate line-range verification (non-author)

seat: `mori-r37-w1-ExecLessonGate` (leaf executor; no subagent dispatch)
lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin` (jj-colocated, git backend)
item attacked: the `## Gate` table of `corpus/lessons/round-37.md` — for rows S221..S225,
does the quoted text occur **contiguously at the cited `S###.src` lines** in the **committed
copies**, and is each quote **≤25 words**?

**Outcome: one real defect found (S225's cited line range under-covered its quote), independently
confirmed by `w1/ScribeLesson`, and fixed by the lane mid-session in commit `30dfe70`. Re-verified
at the current lane tip: all five rows now PASS.** Details and per-row evidence below.

## Method

Verification is against **committed blobs** (`git show <rev>:corpus/evidence/sources-r37/S###.src`),
not the working tree. Three revisions were checked:

- `HEAD` = `30dfe70fadcf5c77f8b09718f3e6042958e4d735` — the state after the lane's fix.
- `1ae1d6d69282f6c4f51355308db6a4be9a8e3d42` — the lane tip **as handed to this seat** (lesson
  blob `fd06bd1fb47a6d49bff965ae94b6530614b93011`; worktree identical at that moment).
- scored tip `e57c58b57c025364e79d130fbdf764d2674d83d6` — **neither** `corpus/lessons/round-37.md`
  nor `corpus/evidence/sources-r37/S225.src` exists at that revision (`git ls-tree e57c58b
  corpus/lessons/round-37.md` → empty; `git ls-tree e57c58b corpus/evidence/sources-r37/` → S221–S224
  only). The lesson was added at `bcf6550` and S225.src at `52d636d5`, both **after** the scored tip.
  So the committed copies this Gate cites are the lane-tip blobs; the tip is reported for
  completeness only.

Four of the five copies are HTML (OWASP / Python / Yama / Fetch pages), so the quoted text
interleaves markup (`<var>`, `<a>`, `<strong>`, `<code>`). Contiguity was therefore evaluated on
**visible text**: HTML tags removed, block-level tags (`p`, `li`, `dt`, `dd`, `div`, …) contributing
a word separator and inline tags contributing none, character references decoded, whitespace
collapsed. Two independent controls were run — a no-space tag strip and a space-substituting tag
strip, plus a raw byte grep — and **the S225 result is identical under every variant**, so the
finding does not depend on the normalisation choice.

Word count: whitespace-separated tokens of the quote exactly as written in the lesson; a
`[A-Za-z0-9]+` tokenisation was run as a control and gives the same counts for all five rows.

Scratch (not in the lane repo): `/fast/scratch/hyaku/mori-r37/ExecLessonGate/` —
`check.py`, `check2.py`, `check3.py`, `final.py`, `evidence.py`, `raw.py`, `check_lesson.py`,
`receipt-final.txt`. `check_lesson.py` parses the lesson's Gate table directly from a given git
revision (so the check is re-runnable against any tip, pre- or post-fix) and verifies each row's
quote against the committed `.src` copies.

## Result — row / range / contiguous / word-count

### At the lane tip as handed to this seat (`1ae1d6d`, lesson blob `fd06bd1f`)

| row | cited range in lesson | contiguous at cited lines | actual line span in the committed copy | occurrences of quote in file | words (ws / regex) | ≤25 | verdict |
|---|---|---|---|---|---|---|---|
| S221 | `S221.src:7230-7234` | **yes** | 7232–7234 (inside 7230–7234) | 1 | 25 / 25 | yes | PASS |
| S222 | `S222.src:5031` | **yes** | 5031–5031 (exactly the cited line) | 1 | 23 / 23 | yes | PASS |
| S223 | `S223.src:1140-1142` | **yes** | 1140–1142 (exactly the cited range) | 1 | 23 / 23 | yes | PASS |
| S224 | `S224.src:217-221` | **yes** | 217–218 (inside 217–221) | 1 | 20 / 20 | yes | PASS |
| S225 | `S225.src:8355` | **NO** | **8355–8356** — quote ends on 8356, past the cited line | 1 | 9 / 9 | yes | **FAIL** |

Four of five PASS; **S225 FAILs contiguity**. All five quotes are ≤25 words (S221 is exactly at the
25-word guard).

### At the current lane tip (`30dfe70`, after the lane's fix)

| row | cited range in lesson | contiguous at cited lines | actual span | occurrences | words (ws / regex) | ≤25 | verdict |
|---|---|---|---|---|---|---|---|
| S221 | `S221.src:7230-7234` | yes | 7232–7234 | 1 | 25 / 25 | yes | PASS |
| S222 | `S222.src:5031` | yes | 5031–5031 | 1 | 23 / 23 | yes | PASS |
| S223 | `S223.src:1140-1142` | yes | 1140–1142 | 1 | 23 / 23 | yes | PASS |
| S224 | `S224.src:217-221` | yes | 217–218 | 1 | 20 / 20 | yes | PASS |
| S225 | `S225.src:8355-8356` | **yes** | 8355–8356 | 1 | 9 / 9 | yes | PASS |

Re-run command:

```
$ python3 /fast/scratch/hyaku/mori-r37/ExecLessonGate/check_lesson.py HEAD HEAD
lesson rev HEAD | src rev HEAD
Gate rows parsed: 5
S221 cited 7230-7234: contiguous=True words=25/25 -> PASS
S222 cited 5031-5031: contiguous=True words=23/23 -> PASS
S223 cited 1140-1142: contiguous=True words=23/23 -> PASS
S224 cited 217-221: contiguous=True words=20/20 -> PASS
S225 cited 8355-8356: contiguous=True words=9/9 -> PASS
OVERALL: PASS
```

## The defect (found, confirmed, fixed)

**`corpus/lessons/round-37.md:13` — S225's Gate line range did not contain its quote.**

The lesson cited `S225.src:8355` (one line) for a quote whose last two words (`network error`) live on
`S225.src:8356`. The minimal range that actually contains the quoted text is `8355-8356`.

Committed copy `HEAD:corpus/evidence/sources-r37/S225.src` (blob `51b848dafc418e7e3f4bd9371ae2e3b7ea64beb3`,
1,854,393 bytes), raw bytes of lines 8355–8356:

```
      <p>If <var>request</var>’s <a data-link-type="dfn" href="#concept-request-redirect-count" id="ref-for-concept-request-redirect-count①">redirect count</a> is 20, then return a
 <a data-link-type="dfn" href="#concept-network-error" id="ref-for-concept-network-error④②">network error</a>.
```

Visible text per line:

- line 8355 → `If request’s redirect count is 20, then return a`
- line 8356 → `network error.`

The quote ends with `then return a network error`; `network error` is **on line 8356**, not on the
cited line 8355. Line 8355 alone yields `If request’s redirect count is 20, then return a` — the
quote is not present there.

Raw-byte control, independent of any HTML normalisation:

```
$ git show HEAD:corpus/evidence/sources-r37/S225.src | sed -n '8355p' | grep -o "network error" | wc -l
0
$ git show HEAD:corpus/evidence/sources-r37/S225.src | sed -n '8356p' | grep -o "network error" | wc -l
1
```

The quote occurs exactly once in the whole copy (at 8355–8356), so there is no other place where it
would be contiguous at the cited line.

This falsified the lesson's own Gate-note self-certification at `corpus/lessons/round-37.md:22-24`:

> "each quote above is contiguous in the committed copy named by its `S###.src` file **and at the line
> range given**; … `S225` is a `<var>`-interleaved sentence, quoted from "redirect count" to the end of
> the clause."

The note was right that the quote runs from "redirect count" to the end of the clause — but the end of
that clause is on the next line, and the range given was not widened to match.

### Provenance of the mismatch

`corpus/SOURCES.md:231` (row S225) cites the anchor cell `§4.5 HTTP-redirect fetch:8318-8360;
"redirect count is 20":8355`. The SOURCES anchor's own quoted fragment **is** wholly contained at
line 8355 alone (verified: `redirect count is 20` ∈ visible text of 8355 → True). The lesson's Gate
quote extended that fragment past the anchor's own end (`then return a network error`) while keeping
the anchor's single-line `:8355`. The SOURCES row was sound; only the lesson's Gate row over-ran its
cited line.

### Fix (lane-owned, landed during this wave — not applied by this seat)

Commit `30dfe70` ("round-37: wave-1 follow-ups — S225 quote line range, …", 2026-10-23 17:19:33
-0300) changed the range only:

```
-| … at `S225.src:8355`: "redirect count is 20, then return a network error" |
+| … at `S225.src:8355-8356`: "redirect count is 20, then return a network error" |
```

That is exactly the minimal containing range this seat measured (`8355-8356`), and the widened range
verifies contiguous. The commit touched only `SCORECARD.md` and `corpus/lessons/round-37.md`; the
`S225.src` blob is byte-identical across it
(`git rev-parse 1ae1d6d:…S225.src 30dfe70:…S225.src` → `51b848da…` both). The sibling seat
`w1/ScribeLesson` independently reported the same defect (`w1/ScribeLesson.md:14`, "Unresolved Gate
row"; VERDICT: FAIL) before this seat's own re-measurement, so the defect was caught twice by
independent measurement.

### Residual wording inaccuracy (not fixed; no citation impact)

The Gate note at `corpus/lessons/round-37.md:25-26` still says "`S225` is a `<var>`-interleaved
sentence". The `<var>` element wraps `request`, which is *before* the quoted span; the quote itself
is `<a>`-interleaved (`redirect count`, `network error`). Wording only — the line range it refers to
is now correct.

## Evidence — the four passing rows

Visible text of each cited range contains the quote as one unbroken run:

- **S221** `S221.src:7230-7234` → `15.4. Redirection 3xx The 3xx (Redirection) class of status code indicates that further action needs to be taken by the user agent in order to fulfill the request. There are several types of redirects:` — the quoted sentence occupies 7232–7234, inside the cited range. 25 words (exactly at the ≤25 guard).
- **S222** `S222.src:5031` → `Note: Disable the support for the following of the redirection in your web client in order to prevent the bypass of the input validation described in the section …` — the quoted prefix is wholly within the single cited line 5031. 23 words.
- **S223** `S223.src:1140-1142` → `The default implementation of this method does not strictly follow RFC 2616, which says that 301 and 302 responses to POST requests must not be automatically redirected without confirmation by the user. In reality, browsers` — the quote is the verbatim mid-sentence fragment the lesson's Gate note declares; it ends at `confirmation`, the source continues `by the user`. 23 words.
- **S224** `S224.src:217-221` → `1 - restricted ptrace: a process must have a predefined relationship with the inferior it wants to call PTRACE_ATTACH on. By default, …` — the quote occupies 217–218, inside the cited range. 20 words.

All five quotes are verbatim in the committed copies, each occurring exactly once, each ≤25 words.

## Files changed

Exactly one file written (my exclusive deliverable):

- `.ufo/waves/round-37/w1/ExecLessonGate.md` (this report)

No lane file was modified. No `git add/commit/push/fetch/reset/stash`, no mutating `jj` command. The
S225 defect was **not** remediated by this seat — detection and report only (mori province); the lane
landed the fix in `30dfe70`. Scratch artifacts live under
`/fast/scratch/hyaku/mori-r37/ExecLessonGate/`.

## Blockers

None. No tools were installed or upgraded in this seat, so there is nothing to record under the
tooling directive.

## Verdict

Against the lane tip **as handed to this seat** (`1ae1d6d`, lesson blob `fd06bd1f`): **FAIL** —
S225's cited range `S225.src:8355` did not contain its quote (the quote spans 8355–8356); S221–S224
PASS; all five quotes ≤25 words. The defect was independently confirmed by `w1/ScribeLesson` and
fixed by the lane in `30dfe70` (range widened to `8355-8356`).

Against the **current lane tip** (`30dfe70`): **PASS** — all five rows are contiguous at their cited
lines and ≤25 words.

VERDICT: FAIL
