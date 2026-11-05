# Round 94 — mori (L1 MoriR94, attempt 1) — lesson (draft, seat Mo94Sc01Lesson)

Draft prose for `corpus/lessons/round-94.md`. Frozen contract `.ufo/waves/round-94/contract.md` at `6b65e7c1`;
entering `84b15230`; wave spec and registry at `4ae1678d`. This draft is written before any wave seat output:
`.ufo/waves/round-94/w1/` holds only `swarm-registry.json` at drafting. Every landing number below is therefore
either a pre-freeze receipt (cited) or marked `pending landing`. Nothing here is a landing measurement.

## Gate (sources, protocol §2b)

| Row | URL | Access and recomputation | Located quote (≤25 words) | Decision |
|---|---|---|---|---|
| S624 | https://docs.python.org/3/library/stdtypes.html | 2026-11-05; sha256 `2397d83204d8901b852e5dcb72cb1b5cbf311e9db1f15116089b85ab21d22b68`, 815447 bytes (seat-supplied; contract P5). Re-fetched by this seat with `curl -L`: HTTP 200, one redirect to `https://docs.python.org/3/builtins/stdtypes.html`; sha256 and byte count match. The row should cite the post-redirect URL as well | "Return True if string starts with the prefix , otherwise return False ." (anchor `id="str.startswith"`; occurs once after inline tags are replaced by spaces; the visible text reads "prefix, otherwise return False.") | **admit** (used-by this lesson; knowledge entry citing it when landed). Teaches: `str.startswith(prefix)` is prefix equality at the string's beginning (the page adds: "test string beginning at that position", for optional `start`), so an admission check that compares the first token with `startswith` does not accept a hash that merely occurs inside a longer token |
| S622 (reuse) | https://git-scm.com/docs/git-log | Not re-opened this round. Round-93 receipt: sha256 `f206647f…`, 375834 bytes (`corpus/SOURCES.md` row S622; `corpus/lessons/round-93.md` `## Gate`). Round-94 reuse: the `%h` placeholder ("abbreviated commit hash") is the source for the 8-character `verified-at` token that C1 reads (`.ufo/waves/round-94/evidence/premises-r94.txt` P3, 19/19 `token_prefix=True`) | not re-quoted; the round-93 quotes stand | reused, not re-admitted. The located quote fixes no width for `%h`, so the 8-character width is a property of this repository's hashes, not of the source. That is the contract's named limit on C1 (a shorter `%h` would fail the 8-character tokens) |

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| `untracked-orchestrator-marker` — the round-92 and round-93 dispatch markers (`*.ready.dispatched`, `w1.ready`) sit untracked in the lane porcelain, so the dispatch record is not durable. At entering, `jj-lane.sh state` shows `untracked=3` (contract, `## Learning and frontier step`) | `.ufo/waves/round-94/evidence/gitignore-red-before.txt` (porcelain lists `?? .ufo/waves/round-92/w1.ready.dispatched`, `?? .ufo/waves/round-93/w1.ready`, `?? .ufo/waves/round-93/w1.ready.dispatched`; `check_ignore_rc=1`); `corpus/lessons/round-93-verifier-spotcheck.md` §6 D3 (same three paths) | none | a `.gitignore` rule for the marker paths. Red before: `git check-ignore` exit 1 (`gitignore-red-before.txt`; re-run by this seat on `.ufo/waves/round-93/w1.ready.dispatched`: exit 1, the path is not ignored). Green: exit 0 `pending landing`. The green receipt is not in evidence at drafting (the fix is built by seat `Mo94E03Gitig` in a scratch clone). The red receipt does not name the path it checked; the re-run above does |

## Routed defects

- **R02 (round-93 routed defect; claimed this round, not yet closed).** `count-c1.py:141` (frozen; `.ufo/waves/round-93/`
  line per `.ufo/waves/round-94/evidence/premises-r94.txt` P1) tests `ac[:7] in va`, a substring test with no token
  boundary. The round-94 claim is the v2 rule (`count-c1v2.py`): the first `verified-at:` token must be a prefix of the
  admission `%h`, read with `str.startswith` (Gate, S624). Predicate P-C1 (`contract.md`, Claims, C1). Entering
  receipts: the battery reads the frozen v1 `EMBED_FALSE_PASS v1=3/3`; v2 reads `v2=0/3`; live v2 reads `met`
  (`evidence/controls-r94.txt`, `evidence/entering-c1-r94.txt`). The fixture revision hashes differ between the two receipts
  (for example `bfdfbd3aef75` and `b88087eed54b` for the left fixture), because each run commits fresh fixtures; the verdicts
  match. The lesson says R02 is closed only if the landing run reads `C1=met` on the battery exactly as P-C1 states. `pending landing`.
- **Counter host path (round-93 routed defect; closed for round-94 counters only).** C2 covers the round-94 counters:
  `literal_r94=0` over `.ufo/waves/round-94/` is the claim (`contract.md`, C2). The round-93 counters are frozen history and
  keep their literals, named here: `.ufo/waves/round-93/count-c1.py:39` and `count-c2.py:39` (`CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"`),
  and `.ufo/waves/round-93/controls-r93.sh:81` (`/home/vgpnk/` and `/home/vgpnk` in the sed, plus two `/home/someone`
  replacement strings). The entering diagnostic reads `literal=6 files=5` (`evidence/entering-c2-r94.txt`); I counted the
  same six by hand: two `/home/vgpnk` and two `/home/someone` on line 81, one `/home/vgpnk` literal in each of `count-c1.py` and
  `count-c2.py`. The round-93 counters are not edited (`contract.md`, Premises P2). `pending landing` for the round-94 check.
- **Digest-gate debt (carried, not claimed).** 31 prefix-only digest rows and S125 unpinned,
  as recorded in round-93 (`corpus/lessons/round-93.md`, Planned item 3; round-93 contract P3). Completing a digest in place
  edits an anchor cell, which CORPUS rule 2 forbids (`contract.md`, Premises P4). Not claimed this round.
- **Round-90 nonce guard (QUALITY 191), carried.** Named in `contract.md` P4 and not claimed this round.
- **Round-93 spot-check S623 items D4 and D5 (open).** The S623 row's pin and anchor do not reproduce, and its
  "= 1" count is wrong for the second quote (`corpus/lessons/round-93-verifier-spotcheck.md` §6). No
  `supersedes S623` row exists in `corpus/SOURCES.md` at this revision (`grep` finds none), so these stay open.
  Not addressed in round-94 evidence.
- **D1 (round-93 spot-check: no planner seat), answered.** The contract's Shape line says the wave has 12 seats with no
  planner, and the L1 holds the §3 planner seat because the validator rejects `planner` (`contract.md` lines 12–13). The
  spec agrees: `.ufo/waves/round-94/w1-spec.json` has 12 `"role"` fields: connector 1, critic 2, executor 3,
  mutation-tester 2, reviewer 2, scout 1, scribe 1. I did not run the validator, so its rejection of `planner` is the
  contract's statement [INFERENCE from the contract].

## Assimilation

None. `merge/mori/` is not present in this lane (`ls merge/mori` fails at `mori-shokunin`), so no staged theme was
checked against this round's claims.

## considerthese

The newest file is `considerthese/2026-10-26.md` (the directory's last entry). Its header says "proposals only, not
acted on". Its four numbered items: 1 and 2 and 3 are proposals; 4 is a status line, and that line covers the
2026-10-25 suggestions (its text is "From 2026-10-25: suggestion 1 adopted …"). Round 93's `## Assimilation and
considerthese` read that status line as the 2026-10-26 status and wrote "no proposal is still unimplemented". That
reading does not hold for 2026-10-26 items 1–3, so it is corrected here (correction of record; round 93's file is not edited).

- **Suggestion 1 (split pin-check mismatches into "can't run here" and "stale"): implemented.** `tools/mori-pin-check.py`
  line 142 defines `stale` against "the instrument could not run here"; line 861 tags the environmental case. The file's
  last commit is `1592f53d` (round-63).
- **Suggestion 2 (follow unfixed critic flags forward): adopted as a rule.** `corpus/QUALITY.md` line 1522 (criterion 153)
  carries an unfixed flag into the next round's ledger. I did not verify a ledger file, so the operation is not confirmed.
- **Suggestion 3 (re-execute what closures only evidence-verified): the one still-unimplemented item, in practice.** The
  rule is adopted as `corpus/QUALITY.md` criterion 136 (line 1223), which requires the round after a closure to re-run that
  closure's counter at the scored revision. Round 93 was closed on committed receipts and was not re-executed (criterion
  136 names `corpus/lessons/round-49.md` as its example). The round-94 evidence has no re-run of round-93 counters at
  `8edbb86d`: the files are `controls-r94.txt`, `entering-c1-r94.txt`, `entering-c2-r94.txt`, `gitignore-red-before.txt`,
  `premises-r94.txt`, and the round-93 scan in `entering-c2-r94.txt` is a literal scan, not a counter run. [INFERENCE: the
  wave's seats (`w1-spec.json`) do not include that re-run either.]
- **Suggestion 4 (keep a suggestion-adoption status line):** the status line is present, but it covers 2026-10-25.
