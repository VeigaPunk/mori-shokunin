# CriticSourcesDiscernment — round 25, wave 2 (falsify)

Seat: `MoriR25.CriticSourcesDiscernment` (critic, leaf). Target: discernment of the round-25 SOURCES rows
S098–S113 and the `source:` line of `corpus/knowledge/harness-job-capacity-r25.md`, lane HEAD
`07a31ae8e22514bbc603afa13f2de7c8b2424cca`. Read-only on the lane; scratch fetches in
`/fast/scratch/hyaku/mori-r25/w2-CriticSourcesDiscernment` (removed after use). No tools installed or upgraded.

## Verdict: weakened

The registry is mechanically clean. The census validator exits 0, every `source:` id exists and is `mined`,
and S102 (the binary row) is a valid, reproducible primary source. Four discernment defects weaken it,
but none breaks C2:

1. S101's `teaches` claims that "docs and code disagree". Its sibling row S103, from the same upstream docs
   tree at the same commit, states the maximum.
2. Several flip conditions are unsound (S105, S107, S108, S110). S110's rejection reason is partly false.
3. S104 partly duplicates teaching already carried by S099.
4. The note cites S102 for binary facts that are outside S102's anchor.

## Census validator (required run)

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`

```
mori	W04	S035 duplicate url raw.githubusercontent.com/systemd/systemd/cf8ebfc6159cf0b3b99aa9a0164ccb07c4c9c5af/catalog/systemd.catalog.in across scopes
mori	W04	S037 duplicate url www.freedesktop.org/software/systemd/man/latest/systemd.journal-fields.html across scopes
mori	W04	S073 duplicate url docs.python.org/3/library/pathlib.html across scopes
mori	W04	S074 duplicate url kubernetes.io/docs/concepts/architecture/controller across scopes
mori	W04	S075 duplicate url ftp.gnu.org/gnu/bash/bash-5.3.tar.gz across scopes
mori	W04	S076 duplicate url michaelfeathers.silvrback.com/characterization-testing across scopes
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
exit=0
```

No error codes. All six warnings are older rows (S035–S076). None of S098–S113 raises a warning: there is no
duplicate URL, no community row at tier A (E10), and no tier-C mined row with a used-by path (W01). The
validator checks syntax and enums only. It cannot see the semantic defects below.

## Byte checks (all re-fetched 2026-10-22)

| Source | Result |
|---|---|
| `docs/settings.md`, `docs/tools/eval.md`, `tools/settings.ts`, `tools/bash.ts`, `tools/eval.ts` at commit `45c35e40…` | HTTP 200. sha256 `0b2e1457…`, `fb2fc4a1…`, `51497414…`, `d985ef25…`, `01e9c5c5…` all match the rows. |
| `tools/bash.ts`, `tools/eval.ts` at tag `v18.12.6` (the S112/S113 URLs) | Byte-identical to the commit fetch (same sha256). |
| `~/.local/bin/omp`, using S102's own locator one-liner | `sha256 85d9daf3…ccfa4 size 256702432`. Clamp at byte `164406766`, schema default at byte `155231590`. Both match the S102 anchor. |
| `gh api repos/can1357/oh-my-pi/releases/tags/v18.12.6` | Asset `omp-linux-x64 256702432 sha256:85d9daf3a05fc76e8cd425ae1904eb576af8d21cc85fcf4690742626e07ccfa4`, published `2026-10-21T21:02:53Z`. The note's "byte-identical to release asset" claim holds. |
| `omp.sh/docs/settings`, `omp.sh/docs/subagents`, DeepSeek page | HTTP 200, 0 hits for `maxJobs` on each. The S107 and S108 rejection facts hold. |
| Issue #14636 (`gh api`) | Open, 0 comments. Body quoted under finding 4. |

## Findings

### 1. S101 — admitting it is correct, but its `teaches` column overclaims (medium)

**Counterexample.** S101's `teaches` (`corpus/SOURCES.md:107`, column 7) says: "a configured value above 100
reads as honoured; the code clamps it, so docs and code disagree for values above 100." The upstream docs
tree at the same commit says otherwise. `docs/tools/eval.md:258` states "the session-wide `async.maxJobs`
cap (default and maximum 100)", and that line is admitted as S103 (`SOURCES.md:109`). `docs/settings.md:623`
reads in full: "Running background-job cap, floored to at least 1; parked/queued jobs do not consume execution
slots." That is an omission, not a contradiction: no upstream doc states a value above 100 is honoured. Only
the settings page is silent. "Reads as honoured" is a reader inference with no `[INFERENCE]` tag.

**Evidence that the admission itself is sound.** A page is primary evidence of what it says and omits. The
row's scope column ("declared type, default and stated bounds; not the runtime clamp") is correct. The note
uses S101 correctly (F1: "The settings page states a default and a floor but **no maximum**… a reader of the
settings page alone would predict…"), and so does the lesson (`corpus/lessons/round-25.md:13`). Only the
registry row drifted. In wave 1, `SrcRejections.md:120-130` scoped this page to "the documented default and
floor". The landed row turned that into a docs-versus-code disagreement claim, which none of the sources
supports.

**Impacted axes.** Discernment of the source and provenance of the "documentation gap" claim. A reader of
SOURCES alone would learn a false fact about upstream docs.

**Smallest fix.** Rewrite S101's `teaches` as: "The settings reference gives default 100 and a floor of 1 and
states no maximum; the 100 maximum is documented only in docs/tools/eval.md:258 (S103), so this page alone
under-describes the clamp."

### 2. S102 (own-work binary row) — a valid primary source; held, with two hygiene gaps (low)

**Held.** The bytes, digest, offsets, version strings and the upstream release-asset digest all reproduce
(byte checks above). `own-work` at tier A is in the census enum (`scripts/sources-census.sh:655`), and S034 is
a lane precedent (`own-work | A | mined`). For "the installed build clamps at 100", the installed bytes are
more primary than any upstream file. The scope says correctly that the row is not upstream semantics and not
a live run.

**Gap a: the note cites S102 beyond its anchor.** The S102 anchor records only the clamp (`164406766`), the
schema default (`155231590`) and the version bytes. The note also attributes two more binary facts to S102:

- the refusal template at byte `160033359` (F6);
- "`var v = 15;` … consumed only through `t ?? v`" (F3).

Neither is in the row. Both are attributed to S102 with nothing in the row to recheck them by. The bytes also
show more than the note says:

- `Background job limit reached` occurs twice, at offsets `95794256` (a compiled-data region, template
  `(1…Z)`) and `160033359` (the JS template).
- `var v = 15;` occurs twice: at `160031518` in the `// packages/coding-agent/src/async/job-manager.ts`
  module, and at `168130151` in the unrelated module `web/search/providers/public.ts`.

So the one-hit reading that the note implies depends on reading per module.

Fix: add the two offsets, with their owning-module comments, to S102's anchor, or drop the S102 citation from
F3's `var v = 15` sentence and F6.

**Gap b: recheck trigger.** `recheck: on-release` does not cover a local binary swap. Fix: "on-release or on
digest change".

### 3. Duplicates among admitted rows — no exact duplicates; one partial duplicate authority (low)

- No URL is repeated across S098–S113 (the validator raised no W04 for them).
- S099 vs S104 (partial duplicate). S099's anchor already carries the whole clamp lineage ("introduced
  2026-02-22 by 476b858b3a4a … default 15 to 100 on 2026-02-26 by 944d7f8d8d …"). Its `teaches` already says
  "the clamp is not new (it ships with the 2026-02-22 async-background-jobs feature)". S104's `teaches` repeats
  the same origin fact. Two rows now teach the clamp's origin, so a recheck of one can drift from the other.
  Fix: keep S104 as the only authority on origin, and cut S099's `teaches` to the current clamp plus
  "lineage: S104".
- S101 vs S103 and S100 vs S102 are not duplicates. They are different pages, and upstream source versus
  installed bytes, with disjoint scopes.
- S112 and S113 use the mutable tag URL `…/v18.12.6/…`, while S098–S101 and S103 pin the commit. The bytes
  are identical today. Hygiene only: pin S112 and S113 to `45c35e40…` as well.

### 4. Rejected rows' flip conditions — S106, S109 and S111 are sound; S105, S107, S108 and S110 are not (low to medium)

- **S105 (termux), kind error.** The flip says: "the repo records an observed `Background job limit reached
  (N)` … then admit as an **own-work** ARM64 observation row". A third party's recorded observation is not
  own-work. In this registry own-work means the lane's own observation (S034, S102). An ARM64 build is also
  outside the note's single-binary scope. Fix: "admit as community tier C, scope ARM64 build only".
- **S107 (omp.sh), tier error, and the flip would create a duplicate.** The row itself calls omp.sh "the
  official documentation site", yet it is ranked tier C. Tier states authority; relevance is the rejection
  reason. The flip ("inlines the `async.maxJobs` row from docs/settings.md, then admit at tier A") would admit
  a mirror of S101, which is the page already known to omit the maximum. That adds a duplicate authority and
  no new evidence. Fix: tier A, kept rejected. Flip: "the site states the 100 maximum or the clamp".
- **S108 (DeepSeek), standard inconsistent with S110.** The flip admits "a third-party statement of the
  default" at tier B. S110 is rejected for exactly that kind of support ("corroborates numbers the code rows
  already anchor"). Fix: the flip should require something the code rows do not already anchor, such as an
  observed clamp, or else re-screen only.
- **S110 (issue #14636), rejection reason partly false, and the flip under-ranks.** The issue body says:
  "`AsyncJobManager` counts jobs of any kind (`DEFAULT_MAX_RUNNING_JOBS` 15, `async.maxJobs` up to 100), and
  when it's full `bash` falls through to a foreground run (`tools/bash.ts`)."
  - It names 15 correctly as the constant `DEFAULT_MAX_RUNNING_JOBS`, so "risks teaching the wrong default"
    overstates the risk.
  - The row's scope ("citing the two numbers") leaves out the issue's third claim: the bash foreground
    fallthrough that S112 admits. The rejection outcome still stands (community, corroborating, tier C).
  - The flip ("a maintainer answer … re-screened at tier C") under-ranks a first-party maintainer statement.
    The census allows community up to tier B (E10 forbids only A). A maintainer statement is also the one
    source that could close U1 (why 100).

  Fix: correct the reason to "corroborates S098, S099 and S112; adds nothing primary". Flip: "maintainer
  rationale → tier B, closes U1".
- **Sound flips.** S106 (published async block plus an observed error, giving a configured-versus-effective
  note), S109 ("re-screen at tier C at best"), and S111 (the mirror inlines the dated upstream note).

### 5. Knowledge `source:` ids — held

`harness-job-capacity-r25.md:1` cites S098, S099, S100, S101, S102, S103, S112, S113 and S104. All nine
rows exist. Each has status `mined` and used-by `corpus/knowledge/harness-job-capacity-r25.md` (column 8 and
column 11 of `SOURCES.md:104-110,118-119`). No other mined row names this note. No rejected row (S105–S111)
is cited as support.

Two minor gaps:

- Line 219 (Limits) says "re-open S098–S103", which omits S112–S113, while line 3 (`recheck:`) includes them
  (low).
- Several load-bearing facts rest on reads that have no registry row. These are F5 and F8 (`task/index.ts`,
  `spawn-run.ts`, `speculative-launch.ts`), F13 (`config/settings.ts`) and F11 (`wave-slot.sh`). The `source:`
  line declares them openly, but they have no sha256 or recheck trigger in the registry (low; registry
  coverage, not an id mismatch).

## Severity summary

| # | Target | Severity | Classification |
|---|---|---|---|
| 1 | S101 `teaches` claims "docs and code disagree" | medium | fixable defect (one cell) |
| 2a | Note cites S102 for offsets outside S102's anchor | low | fixable defect |
| 2b | S102 recheck trigger | low | hygiene |
| 3 | S099/S104 overlapping origin teaching; S112/S113 tag URLs | low | fixable defect / hygiene |
| 4 | Flips of S105, S107, S108, S110 (and S110's rejection reason) | low–medium | fixable defects |
| 5 | Note recheck line omits S112–S113 | low | hygiene |

None of these is a tradeoff the judge must reject. Each is a one-cell or one-sentence edit for the
integration owner.

## Not run / not claimed

- I did not run `tools/mori-job-runway.py` (C2 counting belongs to other seats).
- I did not reopen S098, S099, S104, S105, S106, S109 or S111 over the network. Their hashes are not
  re-verified here.
- I did not fetch `omp.sh/docs/tools` or `omp.sh/docs/slash`.
