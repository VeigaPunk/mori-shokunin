# AttackSrc185 — source row S185 (Linux block/blk-mq.c at v7.2)

Seat MoriR33.AttackSrc185, round 33 wave 2. Axes: source fidelity (A1 bytes and locators), depth/FR6 (does the admitted
row carry the accounting claim the entry uses), calibration (what the admitted quotes qualify).
Objects attacked: `corpus/SOURCES.md:191` (S185 row), `corpus/lessons/round-33.md:20` (S185 Gate row),
`corpus/evidence/sources-r33/S185.src`, and the entry row that cites it (`corpus/knowledge/disk-write-rate-r33.md:20`).

**State.** Measured revision `62db24c0`. The lane is under concurrent edits by other seats: the entry sha256 changed
three times while this seat ran (`8e04b9ef…` at the revision → `8a80d3a5…` → `fa9a00dd…` → `eaeb1100…`, observed
2026-10-23T03:00-03:05Z). The S185 SOURCES line, the S185 Gate line, the committed copy and row 2's S185 clause were
content-stable across those observations except for the repair recorded in F3.

## Assigned checks 1-5: results

**1. Live re-open and sha256 — pass, no defect.** `curl -sSL --fail -m 60
https://raw.githubusercontent.com/torvalds/linux/v7.2/block/blk-mq.c` → `HTTP 200 bytes=136798` (no 429, no retry).
`sha256sum live.src` → `7483f1738ad1a00372f5fca0e553023ff4a683e4e2a73c01b3da31302bba8c11`; `sha256sum
corpus/evidence/sources-r33/S185.src` → same; the Gate sha256 (`lessons/round-33.md:20`) → same. `cmp live.src S185.src`
→ byte-identical. A second fetch gave the same 136798 bytes and sha256. `git show
62db24c0:corpus/evidence/sources-r33/S185.src | sha256sum` → same, so the on-disk copy is the measured-revision copy.

**2. Gate quotes at their locators — pass, no defect, in both the measured and current forms.** At the revision the row
quoted two lines; the current worktree row quotes three. Current form verified:
`S185.src:856` declared 8 words / actual 8, line reads `static void blk_account_io_completion(struct request *req,
unsigned int bytes)`; `S185.src:858` declared 5 / actual 5, line reads `if (req->rq_flags & RQF_IO_STAT) {`;
`S185.src:862` declared 5 / actual 5, line reads `part_stat_add(req->part, sectors[sgrp], bytes >> 9);`. All three are
contained in the whitespace-collapsed copy (`' '.join(text.split())`, the counter's `canon`), all within 3-25 words, 3 of
the allowed 4 quotes. The counter at `62db24c0` printed `S185 gate=ok quotes=2 copy=ok fetch=ok` with
`gates_ok=11/11 copies_ok=11/11 fetch_ok=11/11`; its `C1=unmet` came from `unmet_conditions=judge` (receipt absent at
this wave), not from S185.

**3. SOURCES teaches / scope / anchor — pass, with the residual notes F4/F5.** Current teaches cell “For a request
flagged RQF_IO_STAT, blk_account_io_completion adds completed bytes shifted right by 9 to the sector counter.” is stated
piece by piece: the flag by `S185.src:858`, the function and its `bytes` parameter by `:856`, the shift and the counter
by `:862`. Scope “v7.2 request-based accounting: sectors added from completed bytes in blk_account_io_completion” and
anchor “block/blk-mq.c:856,858,862; tag v7.2” name only those quoted lines, the URL path and the tag. No cell names a
fact outside them.

**4. URL pinning and uniqueness — pass, no defect.** `https://api.github.com/repos/torvalds/linux/git/ref/tags/v7.2` →
`HTTP 200`, `"ref": "refs/tags/v7.2"`, `"object": {"sha": "237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63", "type": "tag"}`
(annotated tag, not a branch), and the raw bytes at that tag are identical across two fetches. Not carried elsewhere:
`grep -n -F '<url>' corpus/SOURCES.md` → only `corpus/SOURCES.md:191` (its own row); `grep -n 'blk-mq.c'
corpus/SOURCES.md` → only 191; `git show 7d382043:corpus/SOURCES.md | grep -c 'blk-mq.c'` → `0` at the entering tip
(sanity check: the same tip file holds 34 `raw.githubusercontent.com/torvalds/linux` URLs, so the grep is not silently
empty). No other corpus file carries the URL.

**5. kind / tier — pass, no defect.** `code` and `A` fit an upstream Linux source file fetched at a release tag; the Gate
decision “admit, A, mined” agrees with SOURCES `mined`, and the sha256 is distinct from every other new id's
(`sha256sum` over S180-S190, `uniq -c` all 1).

## Findings

**F1 — none — bytes, hash, stability.** Three-way sha256 agreement (Gate value, committed copy, live fetch, revision
blob) and two byte-identical live fetches. Evidence in check 1.

**F2 — none — quote placement, containment, word counts, budget.** Evidence in check 2, for both the 2-quote measured
form and the 3-quote current form.

**F3 — major, observed live and repaired during this wave — the entry asserted the `RQF_IO_STAT` condition while no S185
quote stated it.** Sequence: at `62db24c0` row 2 read “…`blk_account_io_completion` adds completed bytes shifted right
by 9” (no condition) against two quotes (856, 862) — an R-J caveat exposure, independently reached at
`.ufo/waves/round-33/w2/AttackRow02.md:26`. Then the worktree entry gained “for a request flagged `RQF_IO_STAT`”
(`entry:20`) while the Gate row still quoted only 856 and 862 — at that moment row 2 asserted a fact no quote stated,
which is an R-J failure, not a caveat. The L1 then added `` `S185.src:858` (5 words): "if (req->rq_flags & RQF_IO_STAT)
{" `` and widened the SOURCES anchor to `856,858,862` and the teaches cell to “For a request flagged RQF_IO_STAT, …”.
I re-verified that repaired form: 3 quotes, all at their locators, all contained after collapse, declared counts equal
actual (8/5/5), six-consecutive-word anti-copy rule 0 hits against row 2's current reading cell (simulated with the
counter's own tokenisation: `canon(cell).split()` 6-grams against `canon(quote).split()`), one admit Gate row, one
SOURCES row. **Residual risk:** the repair is uncommitted; if only one half is committed, the judged rev either keeps
the caveat exposure (entry unqualified, quotes 2) or carries an unsupported clause (entry qualified, quotes 2). Both
halves must land at the same rev. Also note the guard is not merely cosmetic: `blk_account_io_start` returns before
setting the flag when `!blk_queue_io_stat(req->q)` and for ineligible passthrough requests (`S185.src:1094-1097`, flag
set at `:1099`), so without the condition the reading is strictly false for those requests.

**F4 — minor — the measured-revision quote set was narrower than the seat's approved quote, and line 859 is still
unquoted.** `.ufo/waves/round-33/w1/SrcBlkMq.md:39,44` proposed one 25-word quote for `S185.src:856-862` that includes
the guard (858) and the group selection (859); I tested it against the committed copy and it is contiguous
(`q in ' '.join(copy.split())` → `True`), so the split into 856 + 862 was a choice, inside the 3-25 limit either way. The
Gate preamble records only the SrcSectorSize replacement (`corpus/lessons/round-33.md:10-11`). The current worktree has
restored 858, which removes the material part of this gap; line 859 (`const int sgrp = op_stat_group(req_op(req));`)
remains unquoted in every form seen, so S185's quotes cannot support any write-specific or per-operation claim. No cell
makes one today; a future row that says “writes land in the write group” would need 859.

**F5 — minor — “completed bytes” rests on the quoted signature, not on a call site.** Quote 856 supplies the function
name `blk_account_io_completion` and its parameter `bytes`; the lines showing the argument is the completed byte count
are `S185.src:905` (`blk_account_io_completion(req, total_bytes);`) and `:983` (`… (req, nr_bytes);`), neither quoted.
The current cells claim only that the function adds its byte count shifted right by 9, so this is not an overreach now;
a row asserting whole-request accounting would need 881-905 or 983.

**F6 — none — bookkeeping.** `opened` 2026-10-23 agrees with Gate `accessed` 2026-10-23T02:39:58Z; `status mined`
agrees with decision “mined”; `recheck on-release` matches tag-pinned bytes; exactly one SOURCES row and exactly one
admit Gate row for S185 (`grep -n '^| S185 '` in each file returns one line, at `SOURCES.md:191` and
`lessons/round-33.md:20`).

## What must hold for the judge

Commit the entry row, the Gate quotes and the SOURCES anchor/teaches together at one rev; then `count-c1-a1.py` prints
`S185 gate=ok quotes=3 copy=ok fetch=ok`. The only S185-side judgement left is whether R-J accepts
“adds completed bytes shifted right by 9” as fully stated by 856+858+862 — I read it as stated (the condition, the
function, the parameter and the shift are each quoted) and record that reading as evidence, not as a verdict; my verdict
is not counted.

## Checks run, and tooling

Ran: two live `curl` fetches and `cmp`; `sha256sum` over the copy, the Gate value and the revision blob; `sed`/`awk`
line dumps of 853-868, 881-905, 970-990, 1085-1100; `grep -c -F` containment in the whitespace-collapsed copy; the
judged counter `python3 .ufo/waves/round-33/count-c1-a1.py 62db24c0…` (read-only: `git show` in the lane plus `curl`) at
the revision; a regex-level reproduction of the counter's Gate rules on the live worktree (it can only be run at a rev,
so the worktree was checked with its own `QUOTE_RE`, collapse and 6-gram logic); the GitHub tag API for the pin; `grep -n
-F` for the URL in `SOURCES.md` and at the entering tip; `sha256sum` distinctness over S180-S190; `git show` diffs of the
S185 SOURCES/Gate lines against the revision. Unrun: nothing among the five assigned checks. Tool installs: none; no
pacman transaction of any kind; all scratch files under `/fast/scratch/hyaku/mori-r33/AttackSrc185/`. One
`git ls-remote https://github.com/torvalds/linux refs/tags/v7.2` ran to its 90 s `timeout` with no output (the ref
advertisement is too large); the API call gave the same evidence and no process of mine remains.
