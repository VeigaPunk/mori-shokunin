# mori round 32 — claim contract (frozen before data)

L1 `MoriR32A2` (attempt 2; attempt 1 landed nothing). Entering tip and base `641a6e86ecc60634d215c0a47ab86c47661abf86`
(round 31 admitted, MANIFEST rounds[495]). This file, `c1-population.json` and `count-c1.py` are committed together
before any seat runs. A declared claim is never withdrawn, narrowed, re-scaled or amended after data; a miss is
reported as a miss.

## Axis choice

Lowest non-retired axes are depth, freshness and calibration (5 each). Rounds 30 and 31 both worked depth and
operability, so the anti-loop rule excludes both this round. Freshness was last moved by round 28 (improved, score
held). One claim, freshness. No second claim: a calibration claim cheap enough to verify this round was not found
that a junk-row control could not also meet.

## C1 — freshness: the 34 mined SOURCES rows whose source URL is not pinned to a tag or commit

Surface changed: the lane's mutable-URL source rows (live docs pages, `latest` man pages, API listings). None of them
is re-checked by any lane tool or counter, and every one was last opened in the round that added it. Pinned rows (tag
or commit URLs) are excluded because their bytes cannot drift. The population is the 34 rows selected by the frozen
selector in `c1-population.json` (sha256 `4426b6501a01c07bdb3347c712c5e858447be47204fa9017c02ab6113e83e178`) over
`corpus/SOURCES.md` at the base. They cover 29 distinct URLs.

The round work for each row: open the URL live this round, commit the fetched bytes unchanged at
`corpus/evidence/recheck-r32/<id>.src`, quote 1–3 located passages that bear on the row's `teaches` cell, and give a
verdict: `current` (the live page still supports the teaches cell), `drifted` (it no longer does; every knowledge entry
in the row's `used-by` cell gets an appended `Round32` correction naming the id), or `unreachable` (three fetches fail;
the transcript is committed at `<id>.fetch.txt`). A non-author reviewer seat judges each row against the exact
`## Recheck` section bytes it names. The method cites at least one new source opened this round (S175 or higher) in
`corpus/evidence/recheck-r32/README.md`: that is the round's sourced claim.

**Predicate P-C1 (the same sentence as the counter docstring and the receipt label):** C1=met iff at <lane-rev> every
one of the 34 frozen population ids has exactly one row in the `## Recheck` table of corpus/lessons/round-32.md that
passes every row check (rows_ok=34/34), and at least one new source row S175 or higher passes the new-source check
(new_ok>=1).

Row checks R1–R5 and the new-source check are spelled out in the `count-c1.py` docstring; the code is the authority
and this file does not restate them differently. In short: header `id | url | accessed | sha256 | quotes | verdict`;
url equal to the population url; accessed at or after 2026-10-23T01:00:00Z; copy sha equal to the row sha; 1–3 quotes of
3–25 words, each inside the normalised copy and inside a live re-fetch made by the counter; the quotes share at least
2 content tokens with the row's teaches/anchor/scope cells; an `unreachable` row needs a committed transcript and
three failed counter fetches; the judge receipt `.ufo/waves/round-32/judge/JudgeRecheck.md` is from a reviewer seat
named in a committed round-32 dispatch file, names the sha256 of the judged `## Recheck` section, which must equal the
tip's, and says `agree` for the id; a `drifted` row needs an added `Round32` line naming the id in every knowledge
entry it is used by.

- Counting command: `python3 .ufo/waves/round-32/count-c1.py <rev>` (exit 0 met, 1 unmet, 2 error).
- Before (run at write time, before the freeze commit): `count-c1.py 641a6e86` → `rows_ok=0/34`, `new_ok=0`,
  `C1=unmet exit=1`.
- Declared after: the same command at the landed tip → `rows_ok=34/34`, `new_ok>=1`, `C1=met exit=0`.
- The command that would show the surface unmoved: the same counter at the base (above).

## Controls (scored under the frozen counter and committed before any data seat)

An adversarial control wave of fresh critic and mutation-tester seats builds, in sandbox clones under
`/fast/scratch/hyaku/mori-r32/`, at least: do-nothing (base), junk table (fabricated shas and quotes), all-unreachable
with fake transcripts, teaches-echo quotes (the row's own teaches text as the quote), a one-fetch reuse shortcut (one
page's bytes copied for every id), a forged judge receipt without a dispatch entry, an off-topic-real-quote shortcut
(a real sentence of the live page sharing fewer than 2 content tokens), and one honest positive row (to show the
counter can pass a row). Receipts land in `.ufo/waves/round-32/evidence/c1-controls.txt`. If any negative control
prints `C1=met`, the counter or target is wrong and is fixed before data; that fix is recorded as a pre-data amendment.
After the first data seat runs, nothing in this file or the counter changes.

Known trust limit, stated before data: R4 rests on the judge receipt being written by the named reviewer seat; a
receipt forged by the integrator together with a forged dispatch entry would pass. The integrator (L1) never writes
the receipt; it is the seat's report copied byte-exact.

## Routed defects from the round-31 closure (§8) — hygiene, not claims

1. M5 correction appended to `corpus/lessons/round-31.md` (the 9 masked fixtures F02, F06–F08, F10, F11, F13, F15,
   F16).
2. A registry row for the blind-writer gate in SKILL.md with every PROTOCOL §Gate standard field, and a frozen-run
   baseline whose `expected.json` pins input digests.
3. Frozen wording: the round-31 `count-c2.py` docstring omits P-C2's "no hit line outside the 16 briefs" clause, which
   the code enforces. Recorded here, frozen file untouched. This round's counter docstring carries the predicate
   sentence verbatim, the same as this file.
4. Judge-vs-tip drift: this round's judge receipt names the sha256 of the bytes it judged, and R4 requires that sha to
   equal the tip's.
5. Counter code on real drafts: this counter is frozen before any data seat; seats may run it only after the freeze
   commit, and nothing in it changes after that.
6. Carried C2 ambiguities and tool edge cases: pinned as committed failing fixtures (evidence only, no tool change).
