# Mo61ScribeLesson — round-61 lesson skeleton + measured findings

Seat: `Mo61ScribeLesson` (scribe, leaf). Read-only on the lane; no VCS mutation anywhere;
no sibling-repo writes; no tool installs. Scratch
`/fast/scratch/hyaku/mori-r61/Mo61ScribeLesson` (created, used, removed at yield —
all receipts are quoted in this report first).

## Deliverable

- Draft lesson skeleton: `.ufo/waves/round-61/w1/DraftLessonR61.md` — `## Gate`
  (six candidate S-rows with URL/date/quote, admitted/not-admitted with reasons),
  `## Mistakes` (the r60 godspeed-bytes-absent dispatch defect, class landing,
  evidence `.ufo/waves/round-60` dispatch, captured-by none, fix = embed + verify
  at dispatch time), and a `## Wave w1` skeleton for the integrated findings.
- The L1 owns the final `corpus/lessons/round-61.md`; this file is a draft.

## Findings (each with the exact evidence)

### F1 — the six S-row candidates, measured (feeds `## Gate`)

All six pinned v7.3 copies are byte-verified: sha256 equals the pin frozen in
`.ufo/waves/round-61/count-c2.py:30-37` (checked with `sha256sum`, and inside the
locator script below), and each candidate quote is a byte-located span of the pinned
copy at the stated line range:

```text
psi.rst                sha_ok=True loc=37-38     located=True words=18 distinct=27
psi.c                  sha_ok=True loc=1282-1283 located=True words=21 distinct=37
psi_types.h            sha_ok=True loc=50-56     located=True words=24 distinct=31
cgroup-v2.rst          sha_ok=True loc=1073-1074 located=True words=22 distinct=25
Kconfig                sha_ok=True loc=736-737   located=True words=19 distinct=27
kernel-parameters.txt  sha_ok=True loc=5540-5542 located=True words=11 distinct=33
```

All six satisfy the frozen quote predicate of `count-c2.py` (≤25 words, ≥8 distinct
bytes) even though that predicate formally applies to ledger rows, not registry rows.
Fetch receipts (all MATCH) are the fetch seat's: `.ufo/waves/round-61/w1/Mo61ExecFetch.md`.

### F2 — three census hazards for the append, all measured on a scratch mirror

I built a scratch mirror of the lane corpus (all of `corpus/`, `tools/`, SKILL.md,
PROVINCE.md, SCORECARD.md), inserted the six drafted rows at the end of the
`## Registry` table (after `| S564 …`, before `## Paths` at line 346), and ran
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-30 <mirror>`:

- Baseline (no new rows): `rc=0`, 0 E-codes, **25** W-codes, 337 rows — matches the
  contract's "census before (337 rows, exit 0)" and the `Mo61ExecCensusMid` receipt.
- With the six rows and the ledger entry present: `rc=0`, 0 E-codes, **30** W-codes,
  **343** rows. The 5 new W04s are `S565, S566, S567, S568, S570 duplicate url …
  across scopes` — S569 (`init/Kconfig?h=v7.3`) has no earlier row in the lane, so
  it produces no duplicate-URL warning.
- Hazard 1 (E04, error, lane exit 1): if a new row reuses the **scope text** of the
  round-55 v7.3 twin row, the census raises
  `mirrorC E04 S565 duplicate url git.kernel.org/…psi.rst?h=v7.3 within scope PSI interface documentation for the system-pressure entry`
  (measured by replacing S565's scope with S529's scope text verbatim).
- Hazard 2 (E11, error): if `corpus/knowledge/psi-v73-recheck-r61.md` does not exist
  on disk at census time, all six rows raise
  `E11 <id> missing used-by corpus/knowledge/psi-v73-recheck-r61.md` (measured with
  the ledger file removed). So the ledger entry must land before/with the rows.
- Hazard 3 (E12, error): rows appended after the last section raise
  `E12 <id> row outside Registry section` per row (measured).
- Counter binding: I replicated `count-c2.py`'s `rows_src` arm
  (`.ufo/waves/round-61/count-c2.py:174-183`) against the mirror: for each of the six
  files, `rows_src[<file>] = ok` — the anchor cell naming
  `copy corpus/evidence/sources-r61/<file>` plus `| mined |` plus
  `psi-v73-recheck-r61.md` in `used-by` is exactly the shape the frozen arm accepts.

Draft row shape that satisfies all of the above (measured clean): distinct scope
text, anchor cell carrying `tag v7.3; <line ranges>; sha256 <pin>; copy
corpus/evidence/sources-r61/<file>`, status `mined`, opened `2026-10-30`, recheck
`on-release`, used-by `corpus/knowledge/psi-v73-recheck-r61.md`.

### F3 — the r60 godspeed-bytes-absent dispatch defect, measured (feeds `## Mistakes`)

- Round 60 dispatch commit `76904b21`: `.ufo/waves/round-60/w1-dispatch.json` —
  64 tasks, **64 start with `/skill:godspeed`, 0 contain the directive body**
  ("Name the axes"). Same bytes at HEAD. The r60 builder at that commit
  (`git show 76904b21:.ufo/waves/round-60/build-w1-spec.py`, line 31) built every
  prompt as `"/skill:godspeed\n" + text + BOUNDS` — a grep of that file at that
  commit finds **0** occurrences of "directive": it never read the directive file.
- Contrast: `.ufo/waves/round-59/build-w1-spec.py:9` reads
  `~/.agents/skills/godspeed/directive.md` and `:139` prepends it; the r59 dispatch
  payload has the body in 64/64 tasks.
- The round-60 lesson's own cause line ("spec builder relied on renderer injection
  that did not happen", `corpus/lessons/round-60.md:102-105`) is therefore not what
  the bytes show: there was no injection path in that builder at all — the embed was
  simply missing, and the fix (`GODSPEED` read + `lead =` prepend) landed only in
  the later r60 integrate commit `bc05a145`, i.e. **after** r60's wave had already
  been dispatched. r60's seats never received the body.
- Round 61 embeds and verifies at dispatch time: `.ufo/waves/round-61/build-w1-spec.py:57-69`
  reads `~/.agents/skills/godspeed/directive.md` and prepends it; the r61 dispatch
  payload (sha256 `c21329857418461e073dd71c7195cbc434d7d30ed57d5626f19220ba143c4121`,
  99448 B) has the body in 64/64 task bodies — measured by me and independently by
  `.ufo/waves/round-61/w1/Mo61ExecGodspeed.md` (`TOTAL tasks=64 ok=64 missing=0`).
- Captured-by: none — the only r60 seat touching the shape checked just the leading
  tag (`.ufo/waves/round-60/w1/Mo60Reviewer16.md:116`: "every body starts
  `/skill:godspeed`"), which is exactly the property a bodyless payload satisfies.
- Residual gap (routed): the verification is a seat reading a file, and the r61
  dispatch payload is still **untracked**
  (`git status --porcelain` → `?? .ufo/waves/round-61/w1-dispatch.json`), whereas
  r60's payload was committed with its dispatch (`76904b21`). No committed
  machine check exists (grep for "Name the axes" over `scripts/` and lane `tools/`
  → no hits). Until the payload is committed, the dispatch-time receipt is not
  reproducible from the repo.

### F4 — C3 counter verdict depends on the repo the arm reads (routed)

Running the frozen C3 counter from the **fleet root** cwd (the host guard's stated
cwd) without `--repo` prints:

```text
C3=unmet r60hole=FAIL r61repair=ok blobrefusal=ok expectpin=ok livepins=FAIL cases=5 failed=r60 bytes lost or hole absent (red-before unfaithful);r61 counters absent or sha pin mismatch at rev rev=7370a731…
```

because `count-c3.py:281` reads the pinned r60 bytes with
`sh(a.repo, "show", f"{R60_REV}:{R60_PATH}")` and `--repo` defaults to
`os.getcwd()`; the fleet repo does not contain `.ufo/waves/round-60/count-c3.py`
(`git -C /home/vgpnk/Projects/shokunin cat-file -e ac496c7c…:…` → object absent).
With `--repo /home/vgpnk/Projects/shokunin/mori-shokunin` the same revision prints
`C3=met r60hole=ok r61repair=ok blobrefusal=ok expectpin=ok livepins=ok cases=5
failed=none rev=7370a731…` (exit 0). This explains the wave's own C3 report
(`Mo61ExecC3Run.md`: "C3 does not meet on any requested revision") as a cwd artifact
rather than a counter defect, and it means the frozen C3 met line is only
reproducible with the lane repo passed as `--repo`. Detection only; the counter is
frozen.

### F5 — C2 selftest receipt needs a floor override (routed, corroborates Mo61ExecReplay)

`TMPDIR=<scratch> python3 .ufo/waves/round-61/count-c2.py --selftest --scratch <scratch>`
→ `C2_SELFTEST pass=9 fail=1` (exit 1; the synthetic good case fails
`pointer_floor:6<40`); with `--floor 6` → `C2_SELFTEST pass=10 fail=0`. The
committed `evidence/selftest-c2.txt` matches the `--floor 6` run. Same finding as
`.ufo/waves/round-61/w1/Mo61ExecReplay.md`; frozen bytes stand.

### F6 — contract range wording (report only; no amendment proposed)

`contract.md:137` says "rows S565–S070 appended in the data phase". `S070` is an
existing row (GNU Bash manual, `corpus/SOURCES.md:76`); the six unused ids are
S565–S570 (`grep -cE '^\| S56[5-9] |^\| S570 ' corpus/SOURCES.md` → 0). My draft
uses S565–S570 and flags the range as a report finding; amendments are barred.
This corroborates `.ufo/waves/round-61/w1/Mo61ScoutS090.md` F-2 ("sic, S565–S570").

### F7 — quarantine wording conflict to reconcile (report only)

Contract `## Sources & frontier step` says the quarantine slice verdicts are
"maintained" (r59 lesson: S244 unverifiable/not fabricated). The wave's fresh
re-derivation (`.ufo/waves/round-61/w1/Mo61ExecQuarantine.md`) reports S244
"PRESENT via DOI-matched companion preprint" (arXiv 2403.18832, ACM version of
record still unfetched), S262 PRESENT, S268 PRESENT, and states no row is
fabricated. The lesson draft records both verbatim and leaves the reconciliation
to the L1.

## Gates / commands run (all read-only on the lane)

`sha256sum` over the six pinned copies; the quote-locator python (reads the copies);
`git show` / `git cat-file` / `git ls-files` / `git status --porcelain` / `git log`
(no mutation); the three census mirrors; `count-c2.py` selftest runs; `count-c3.py`
runs at the freeze with and without `--repo` (scratch only); dispatch-payload JSON
inspection. Fleet-repo git calls were read-only (`log`, `show`, `cat-file`).

## Touched surfaces

- `.ufo/waves/round-61/w1/DraftLessonR61.md` (draft skeleton, seat-spec-named)
- `.ufo/waves/round-61/w1/Mo61ScribeLesson.md` (this report)
No production file (`SKILL.md`, `corpus/`, `SCORECARD.md`, `LOG.md`, `tools/`), no
registry, no VCS state touched. Fleet repo read-only.

## Out of scope / not done

No ledger entry, no SOURCES append, no counter or contract change (amendments
barred), no S-row landed — drafts and findings only for the L1 to integrate. The
C1 registry row drafts belong to the Reg5x scribes and `Mo61ScribeRegReview`; the
ledger row drafts to the Psi scribes; both are cited, not re-derived here.

## Receipts to keep

F1 locator output, F2 mirror census outputs (`validate-mirror0b.txt`,
`validate-mirrorAfter.txt`, `validate-mirrorC.txt`, E11/E12 variant outputs),
F4's two C3 runs, F5's two selftest runs, and the dispatch JSON measurements are
all quoted verbatim in this report; the scratch itself is removed at yield.
