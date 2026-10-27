# Mo58Scribe53 — considerthese 2026-10-26 status check (draft note, not a claim)

Seat: scribe, round 58 wave w1, leaf member (no dispatch). Read-only seat: no production file,
corpus registry, SCORECARD, LOG, skill, or lane VCS was edited; no counter run, no commit.
Freeze revision `fe8801120a67c1a6b8899d7d0423839caa09e7d0`; entering revision
`b783d0b892637ce8d20f188cad20e4d8913ca635`; lane worktree HEAD during the read
`4272736cfc5147586e1543413772f80daf44b04b`. Operator input
`considerthese/2026-10-26.md` was read, not modified.

Scratch: `/fast/scratch/hyaku/mori-r58/Mo58Scribe53/` (created explicitly; `TMPDIR` set there for
the one selftest run; removed before yield). All reads were `read`/`git show`/`git grep`; no
clone, no worktree, no fixture repo.

---

## 1. Suggestion 1 status — IMPLEMENTED (verified against the operator's own wording)

Suggestion 1: "tag a mismatch as environmental when the pinned command exits with a setup error or
a missing absolute path, and as stale when it runs and prints a different tally."

Verdict: **implemented**, in the pin-check v5 / v5.1 bytes that the lane ships at the freeze
revision. `sha256(tools/mori-pin-check.py)` = `32685b9306db061d2c2df21e976823d84a4017cc3524194f4ed76327443081f0`
both in the worktree and via `git show fe8801120:tools/mori-pin-check.py` — the checked bytes are
the freeze bytes.

| Evidence | Location | Content |
|---|---|---|
| contract's pointer | `tools/mori-pin-check.py:138-150` | docstring: "every mismatch line carries `class=env` or `class=stale`… The summary line ends `env=N stale=N`, and env + stale = mismatches" (v5 block 138–144, v5.1 block 145–150) |
| provenance | `git blame -L 138,152` | 138–144 from `87e0c374` (2026-10-26 19:37, "pin-check v5 … env/stale classes"); 145–150 from `7c0b6232` (2026-10-26 19:43, "v5.1"). Both predate the round-58 freeze; `git log fe8801120 -- tools/mori-pin-check.py` lists no later touch |
| class decision | `:834-852` | `counts["mismatches"] += 1`; absent instrument file or >1 tally line → `stale`; no tally observed → `env`; different tally → `stale`; equal tally with contradicting exit → `env` when `rc is None` (timeout/OS error) else `stale`; `cls = " class=" + kind` |
| summary field | `:882-889` | `… baseline=… env=%d stale=%d` from `counts["env"], counts["stale"]` |
| counters | `:620-623` | `"env": 0, "stale": 0` initialised alongside `mismatches` |

Class-completeness check (my own read, not the tool's): there are five
`counts["mismatches"] += 1` sites — `:722` (truncated digest) → `stale`, `:739` (line-count bound
to a non-row instrument) → `stale`, `:750` (line-count differs) → `stale`, `:834` (tally) → exactly
one of `env`/`stale`, `:865` (full digest) → `stale`. So `env + stale == mismatches` holds by
construction for the counters this build emits. Named gap (docstring, unchanged): `unparsed`,
`dropped`, `rebound`, `duplicate`, `hidden`, `misattributed` are fatal counters with **no**
env/stale class, so `env=0 stale=0` does not mean "nothing failed".

Behavioural confirmation (fixtures, not a `--rev` run):
`TMPDIR=/fast/scratch/hyaku/mori-r58/Mo58Scribe53/tmp python3 tools/mori-pin-check.py --selftest`
→ `PIN_CHECK_SELFTEST pass=125 fail=0`, exit 0, 125 `PASS` lines. The eight arms that own this
split, with their printed summary tails (byte-exact):

```
PASS v5_class_env_setup_error  … mismatches=1 … env=1 stale=0
PASS v5_class_env_timeout  … mismatches=1 … env=1 stale=0
PASS v5_class_stale_tally  … mismatches=1 … env=0 stale=1
PASS v5_class_stale_digest  … mismatches=1 … env=0 stale=1
PASS v51_class_absent_instrument_stale  … env=0 stale=1
PASS v51_class_two_tallies_stale  … env=0 stale=1
PASS v51_class_wrong_then_timeout_stale  … env=0 stale=1
PASS v51_class_right_then_timeout_env  … mismatches=1 … env=1 stale=0
```

`v5_class_env_setup_error` (`:1481-1487`) is the operator's motivating case verbatim: the fixture
instrument prints `conformance setup error: No such file or directory: /nonexistent/x` and exits 2,
and is classified `env`, not `stale` — i.e. the round-50 `conform.py` hardcoded-`LANE` mismatch now
reads as environmental.

Limits of this check, stated rather than papered over:
- I did **not** run `--rev fe8801120` (that builds a ~330 MB `git clone --shared`); the runtime
  claim rests on the selftest fixtures above plus the byte identity of the checked file.
- The named limit the tool itself keeps stands: "a tally printed before a crash on a missing host
  path is still `stale`" (`:149-150`) — an instrument that prints its tally and then dies on a host
  path is misclassified as drift.
- The contract cites `:140-150`, which is accurate for the *rule text* but not where the rule is
  applied (`:834-852`, `:882-889`). A closure reader who stops at the docstring has read the
  specification, not the implementation.

Contract conformance: this status is a note, not a claim; no counter, predicate, or score is
touched by it.

## 2. Status of the other three proposals (evidence, so the round does not re-adopt blind)

| # | Proposal | Status at this read | Evidence |
|---|---|---|---|
| 2 | carry unfixed critic flags forward as an id-keyed ledger | **unimplemented as an artifact**; a criterion only | `corpus/QUALITY.md` QUALITY 153 defines the check; `python3 .ufo/waves/round-49/flagged-fixed/count-flagged.py` still prints `flagged=45 fixed=18 unfixed=9` / `na=18`; `git grep -c -F -- 'C1-F1' HEAD -- corpus/lessons` → **no lesson file matches** (`corpus/QUALITY.md` alone, 4 lines); `corpus/lessons/round-57.md:49` "suggestion 2's carry-over ledger remains planned" |
| 3 | re-execute what closures only evidence-verified | **partially acted, no standing artifact** | `corpus/lessons/round-57-verifier-spotcheck.md:40`: counters, independent verifier, verifier mutation arm and census were re-measured by the closure; three items remained evidence-verified (seat tallies, freeze order, role mix). I recomputed all three read-only at HEAD — see below |
| 4 | keep a suggestion-adoption status line | **adopted this round** | `corpus/lessons/round-58.md` § "Considerthese curation" records s1 implemented, s2/s3 unimplemented, s4 as the status line |

Suggestion 3 residual, recomputed by me from committed bytes (no tool needed, ~5 s):

```
python3 -c json.load('.ufo/waves/round-57/w1-results.json')['results']  → len=64, status-field present=0
ls .ufo/waves/round-57/w1/*.md | wc                                      → 62
git cat-file -p 6f3f8482 | head -2                                       → parent 618562c7…
python3 -c Counter(t['agent'] for t in w1-dispatch.json['taskCall']['tasks'])
  → reviewer 22, critic 10, mutation-tester 8, scribe 8, executor 6,
    scout 4, connector 2, sentinel 2, revenger 1, simplifier 1 (Σ 64)
  → attack 22+10+8+2 = 42 → 42/64 = 65.6 % ≥ 25 %
```

Every number in the r57 closure's evidence-verified sentence reproduces exactly. That is the point:
the gap is bookkeeping, not capability.

## 3. Recommendation — one still-unimplemented proposal, s3

Adopt **suggestion 3** (`considerthese/2026-10-26.md`) as this wave's single still-unimplemented
proposal, as a criterion/status note (*never* as a claim — the contract's considerthese rule).

Why s3 and not s2:
- s3's residual scope is decidable **now**, from committed bytes at the round-57 freeze
  (`618562c7`), with no dependency on round-58's unlanded diff. The three items and their
  recomputation are quoted in §2; a reviewer seat can repeat them in seconds and report
  agreement or exact divergence, which is the suggestion's own pass/fail shape.
- s2's disposition rule is explicitly "decided against that round's landing" (QUALITY 153). At
  seat time round 58 has no landing, so a mid-wave seat can only restate ids; and the existing
  check has a live false-green path (below). Adopting s2 would put a broken check in the score path
  in the same round its landing is being judged.

Draft criterion text for s3 (for the closure to word and land; not landed by me):

> A closure's "evidence-verified" list is not a verdict but a queue. Each item it names must carry
> a recomputation command that reads only committed bytes at the frozen revision; the next round's
> closure runs those commands and reports `agree` or the exact divergence. Shown able to fail: the
> round-57 closure's three items all reproduce (64 outputs, 62 reports, 0 status fields; freeze
> `618562c7` parent of `6f3f8482`; role mix 22/10/8/8/6/4/2/2/1/1 = 64, attack 42) — so "verified"
> that no one re-ran is indistinguishable from "verified" that holds only by luck. Not covered: a
> recomputation proves the tally, not the judgement drawn from it.

Routed observation on s2 (draft only, for whoever owns QUALITY 153 — I do not edit it): the check
as written greps `.ufo/waves` and `corpus/lessons` for `<id>` plus a disposition word plus a round,
and at HEAD seven of the nine ids match **inside a discussion file** —
`.ufo/waves/round-56/w1/Mo56ScribeConsiderthese.md:112` reads
`` `C1-F1 routed to round 57 (successor counter counts cels).`: the same`` — which is the criterion's
own example text, not a disposition in round 57. `corpus/lessons` matches none of the nine. A
tightened form would require the matching line to live in `corpus/lessons/round-<NN>.md` with
`NN >` the flagged round, and to carry the disposition as a table cell, so that a seat quoting the
ids cannot satisfy its own ledger.

## 4. Provenance of every claim above

Commands actually run (read-only unless noted), in this order:

1. `read` of the frozen contract, `count-c1.py`, `count-c2.py`, `tools/mori-pin-check.py`,
   `considerthese/2026-10-26.md`, `corpus/lessons/round-57.md`, `round-57-verifier-spotcheck.md`,
   `corpus/lessons/round-58.md`, `corpus/QUALITY.md:1500-1580`.
2. `mkdir -p /fast/scratch/hyaku/mori-r58/Mo58Scribe53/tmp`; `scripts/hyaku/disk-guard.sh status`
   → `/fast/scratch/hyaku 32 % use, 550.1 G free` (green; no pacman, no installs, no tool updates).
3. `sha256sum tools/mori-pin-check.py` and `git show fe8801120:tools/mori-pin-check.py | sha256sum`
   → identical `32685b93…`.
4. `git blame -L 138,152 -- tools/mori-pin-check.py`; `git log --oneline fe8801120 -- tools/mori-pin-check.py`.
5. `TMPDIR=<scratch>/tmp python3 tools/mori-pin-check.py --selftest` (twice: tail-only, then full
   capture) → `PIN_CHECK_SELFTEST pass=125 fail=0`, exit 0, 125 PASS lines.
6. `grep -n 'counts\["mismatches"\] += 1' -A3` and `grep -n 'kind = "stale"|kind = "env"|env=%d stale=%d|counts = \{'`.
7. `python3 .ufo/waves/round-49/flagged-fixed/count-flagged.py` → `flagged=45 fixed=18 unfixed=9`,
   `na=18`, exit 0.
8. `git grep -F -- <id> HEAD -- corpus/lessons .ufo/waves ':!.ufo/waves/round-49/' ':!.ufo/waves/round-17/'`
   for the nine UNFIXED ids, then `git grep -c -F -- 'C1-F1' HEAD -- corpus/lessons corpus/QUALITY.md`.
9. `git rev-list --parents -n1 618562c7…`, `git cat-file -p 6f3f8482`, and the python/json probes in §2.

Out of scope / not done: C1 or C2 counter runs at `R` (other seats own them); any edit to operator
input, corpus, SOURCES, SCORECARD, LOG, SKILL, QUALITY, counters, or lane VCS; assimilation (see
below); quarantine re-derivation (another seat's slice).

Assimilation: none — no `merge/mori/` entry is implicated by this read; the proposal is a
bookkeeping criterion, not a source-grounded capability.

Known limits of this note: the s1 verdict is a static-plus-fixture verification, not a `--rev`
run (stated in §1); the "~5 s" reproduction figure is wall-clock observation on this host, not a
pinned claim; the s2 false-green observation is at HEAD `4272736c` (round-58 in progress), not at
the freeze revision, and a later round could add real lesson-file dispositions that change the
nine-id picture — the criterion text above, not the count, is what should be landed.

Scratch `/fast/scratch/hyaku/mori-r58/Mo58Scribe53/` removed before yield; the only artifact
written is this file.
