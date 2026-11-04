# Mo86S01Lesson — round 86 (attempt 1), wave w1 — lesson seat report

Seat: scribe/lesson (`Mo86S01Lesson`). Wrote **one** path: `corpus/lessons/round-86.md` (153 lines,
sha256 `266bb5bb0c86f274bc043ef236d8b330f032018778ca52849dc62010c6dda910`). No commit, no mutating
git/jj in the lane, no counter, no receipt, no SOURCES row, no knowledge entry, no SCORECARD/QUALITY/
SKILL/LOG/README line. Detection and report only.

Revision I read: `57104423a12a859cac7ac249c683b3a37d77fbe5` (HEAD when I started). HEAD moved during
the seat: `57104423` → `98d15d8f784e55d979b84273aafb45225b8b8ccc` ("contract A1 (subject `--scratch`,
label-only stub guard) and the C2 counter guard fix", 09:27:21 −0300). The lesson's front matter states
both and the state at write.

Files read, with hashes I measured:

| path | sha256 / note |
|---|---|
| `.ufo/waves/round-86/contract.md` | `992764ea…` at `5e80229a`/`4eab48c0`/`57104423` (the P-C1/P-C2/P-C3 text I quote); `5fafb32099c3304e3fb388fe3271f92c701a29af7046da45c82c63e45bf533c6` at `98d15d8f` after A1's 13-line append |
| `.ufo/waves/round-86/evidence/controls-r86.txt` | `8cc9bb5b1a8f38e88ca85aa423b58a67fa7d5dadf0b117f8957d9aa3fc7173cb` |
| `.ufo/waves/round-85/count-c2.py` | `497738932080b8044142e5f49a8a4f3151ab16b876d77d25a8e0771785f8b918`, identical via `git show fec2b328:` and `git show HEAD:` (18 `cases.append(` arms at write) |
| `.ufo/waves/round-86/count-c1.py` | `1912e87d…`; `count-c2.py` `4bdef3a1…` (post-A1 guard fix); `count-c3.py` `6b7fc2dd…` — hashed, **not run** |
| `.ufo/waves/round-85/w1/Mo85M01Mut.md` | §5 and §7 read (the survivors §7 items 11–13 arm) |
| `corpus/lessons/round-85.md` | `f94a4dd8…` at read time (`4eab48c0`); `57104423` appended the *Errata* block (+9 lines, no rewrite) |
| `corpus/knowledge/receipt-provenance-r85.md` | `1475e28f…`; K2 at `:50`, the grammar limit at `:85-88` |
| `corpus/README.md` | `1ea45dda…`; the receipt-provenance row's `Limits` cell at `:901` |
| `corpus/evidence/drift-classification-r82.txt` | `12b4b077…` (72 lines, 64 `DRIFT_CLASS` rows) |
| `corpus/evidence/baseline-r10-20261015T2231Z.json` | `0993b235…` |
| `corpus/SOURCES.md` | `24cab2a8…` worktree (S602 appended, uncommitted); `374` rows committed at `98d15d8f` |
| `corpus/knowledge/execution-evidence-r86.md` | `6aca39ab…` (sibling `Mo86S02Sources`, uncommitted) |

## Behaviour delivered

`corpus/lessons/round-86.md`, shaped like `round-85.md`: front matter (round/date/entering/freeze/read
at/seat scope), a short `## What the round did` (the three frozen claims, their targets, the measured
entering/stub/retroactive controls, the wave shape, the two commits that landed in my window), a
`## Mistakes` section with exactly **one** mined mistake in the four-field shape, and a `## Gate`
block recording the one SOURCES row this round adds (URL, access date 2026-11-04, located ≤25-word
quote). No existing lesson was rewritten; the file is new.

## Candidate search (the three frozen candidates), and why one was mined

1. **`predicate-underreach` — the r85 receipt grammar bound a digest, not a body — VERIFIED and
   MINTED.** Committed bytes: `grade()` in `.ufo/waves/round-85/count-c2.py:154` counts
   `fields["cmd"]` (`:173`, `:201`) and never executes it; the seven `run(` call sites (`:150`,
   `:292`, `:294`, `:301`, `:306`, `:311`, `:320`) pass git argv or the counter's own `--selftest`
   argv; the body is only searched for the summary token (`:194-198`). The limit is committed twice —
   `corpus/knowledge/receipt-provenance-r85.md:50` ("Verification by hash binds **bytes**, not
   **execution**") and `corpus/README.md:901` ("a correct digest over a stale body still passes (the
   round-86 head)") — and no criterion reads a limit's content (`parse_receipt:108-111` grades the
   `# limits:` line's shape only: ≥3 words containing "limit"). First-hand demonstration below.

2. **`class-label-overreach` — the r82 classification labels on name existence — VERIFIED but NOT
   minted.** My own derivation over committed bytes (classification, r10 baseline bytes, one live
   `bash tools/mori-census.sh` capture, rc 1, 20097 bytes, 2026-11-04T12:22:09Z): 64 rows, 19
   `value-changed`, 5 name-shape (`-FINDING:SEGFAULT_JOURNAL`, `-FINDING:WATCHDOG_STALE`,
   `-FINDING:WAVE_UNSETTLED_AGE`, `-SURFACE:journal`, `HEADER`), **14 bare-key rows**; comparing the
   baseline's `name=value` atom set with the live set: `equal` 2, `differs` 6, `masked` 5, `absent` 1.
   The two `equal` rows are `-subject_commits` (`yes` in both; 5 live occurrences) and `-window`
   (`launch..NOW` in both; 5 live occurrences). So the r86 C3 counter's `value_rows=14
   contradicting=2` re-derives from my independent method. Not minted because the round's C2 mistake
   has a named criterion that *should* have caught it (a calibration contrast), while this one's
   captured-by is `none`; the C3 seat owns the capability claim that surfaced it.

3. **`record-integrity` pivot (the r85 verifier's routed defects) — NO LONGER MINEABLE.** Defects 1–4
   were discharged inside my window by `57104423`: `LOG.md` +23 lines naming the superseded
   `LOG.md:5310` `<fill>` text (append-only, not rewritten), the `controls-r85-entering.txt`
   replacement with corrected rc lines, the r85 contract *Errata* block naming A4 `91f657f6`, and the
   r85 lesson *Errata* block; defect 5 (prompt attribution) is explicitly recorded-only. Mining it
   would have been stale before the lesson was written. Evidence: `git show 57104423`.

## First-hand demonstration (the minted mistake)

Scratch `$HYAKU_SCRATCH/mori-r86/Mo86S01Lesson`, deleted after the run. Fixture `git clone --shared`
of the lane, `rev-parse --show-toplevel` asserted equal to the fixture dir before the first commit,
commits with `-c user.name=t -c user.email=t@t`. Fixture commits `ace120bd85bb…` (body equals the
command's stdout) and `df90faf3e41a…` (body one byte off: `stale=1` vs the command's `stale=0`); the
receipt keeps `# rev: 25a74d4c…` and `# counter-sha256: 4ac6b526… tools/mori-claim-sweep.py`, so both
bindings verify.

Frozen r85 counter on the stale fixture (`python3 -I .ufo/waves/round-85/count-c2.py HEAD --repo
"$S/repo"`):

```text
RECEIPT claim-sweep-r85.txt headers=1 rev=1 limits=1 bindings=1 bound=1 summary=1
C2=met receipts=3 bindings=5 bound=5 revs=3 limits=3 cmd=3 summary=3 mismatch=0 detector=green rev=df90faf3e41a
rc=0
```

The same receipt's `# cmd:` executed in a `git archive` export of its own `# rev:` with
`GIT_CONFIG_GLOBAL=/dev/null` prints `stale=0`; `cmp body.txt out.txt` → `differ: char 55, line 1`
(rc 1). Control at `ace120bd85bb…` (body = stdout): `C2=met … mismatch=0` **and** `cmp` rc 0. The
documented recipe was re-run from scratch afterwards (`6ef7a80af5b6…`): same `C2=met … mismatch=0`
rc 0, same `cmp` diff at char 55 — the recipe reproduces, only the fixture commit id differs.

## Gate (freshness)

The round adds one SOURCES row; I re-opened it myself and recorded it:

- **S602** — in-toto Specification v1.0.0, `https://raw.githubusercontent.com/in-toto/docs/v1.0/in-toto-spec.md`
  (row at `corpus/SOURCES.md:384`, 11 cells, tier A / `spec` / `mined` / verified `2026-11-04` /
  recheck `365d` / used-by `corpus/knowledge/execution-evidence-r86.md`; opened and rowed by
  `Mo86S02Sources`). My re-fetch (`curl -sSL -A …`, 2026-11-04): HTTP 200, `redirects=0`, final URL
  identical, 87108 bytes, 2217 lines, sha256
  `17d3326e4cf58234619dbfe821cdc5187e55e2c89f7b63f03699c46588322097`, `cmp` byte-identical to the pin
  `.ufo/waves/round-86/evidence/sources-r86/in-toto-spec-v1.0.md`. Located quote, raw lines
  1063-1064 (sentence spans the break, joined with one space, U+2019), **9 words**: "Byproducts are
  not verified by in-toto’s default verification routine." It occurs exactly once in the pin's text
  after joining every line break; supporting quote `:1053-1054`, 14 words.
- Registry append is `3 0` by `git diff --numstat 98d15d8f -- corpus/SOURCES.md` (row + bounded-search
  paragraph + blank line); no existing row cell moved; the URL occurs once.
- Census at the worktree bytes: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
  → `mori ok`, rc **0**; rows **374** committed → **375** worktree (contract grammar
  `^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|`); warnings **35**, all `W04`; zero `E`.

## Gates I did not run / limits

- I ran **none** of the three r86 counters; the lesson cites their frozen predicates and its own
  measurements only. C1/C2/C3 after-values are the other seats' work.
- The C2 landing state at write (`98d15d8f`): subject still `49773893…` with 18 arms and neither
  `after-c1-r86.txt` nor `replay-defeat-r86.txt` exists — the lesson states this rather than claiming
  a landed fix.
- The S602 row and its knowledge entry were **uncommitted** worktree state when I wrote (L1 owns the
  commit); the row's line number 384 is its worktree position and shifts if rows are inserted above.
- I did not re-derive the opener's exclusion screening (`identified 7, screened 5, included 1,
  excluded 6`) or the knowledge entry's negative-claim sweeps; both are attributed to
  `Mo86S02Sources` in the lesson.
- My live census capture is one observation at 2026-11-04T12:22:09Z (rc 1); the two `equal` rows are
  static strings, which is why they re-derive while the other 12 bare-key rows move or mask.

## Routed (not mine to fix)

`corpus/README.md` carries no coverage-map/index row for `corpus/knowledge/execution-evidence-r86.md`;
`Mo86S02Sources` reported it as out of its write scope (its seat names SOURCES.md, the entry, the
sources-r86 evidence dir and its report). Routing to the L1 / README index owner.

## Tooling

None installed, upgraded or removed; no pacman transaction attempted.

## Scratch

`/fast/scratch/hyaku/mori-r86/Mo86S01Lesson` (clones, live capture, export, fixture bodies) deleted
before yield; the recipe above rebuilds every reading, and fixture commit ids are disclosed as
fixture-local.
