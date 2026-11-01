# Round 66 — mori (L1 MoriR66, the standing drift re-check: every verdict carries its moment)

author: mori L1 (MoriR66)
round: 66
date: 2026-11-01
entering: `54fcd7c9` (`54fcd7c978ac9be39ba37bec4d1a3965f480cf92`, r65 verifier spotcheck tip)

## Fresh start (r59–r61 rejected closures re-read; what was ruled out)

The §7 digests name r59/r60/r61 `rejected-honest-stop`. Spot-checks re-run
this round, not cited from r65 (receipt
`.ufo/waves/round-66/evidence/freshstart-spotchecks-r66.txt`): the frozen r61
counter re-derived at the r61 data tip (`python
.ufo/waves/round-61/count-c2.py 986d4b46…` → `C2=unmet` rc 1, all 14
quote_words anchors — the same verdict r65's re-derivation reached); r59/r60
cited evidence `git cat-file -e` PRESENT and both revisions
`merge-base --is-ancestor` of refs/heads/master, rc 0 each.

Ruled out as r66 claims, and why: (1) re-declaring the r59/r60
entry-claims-class instruments — their met-flip counterexamples stand on
frozen bytes; (2) scalar score moves — no closure states a new number and no
lane convention licenses an L1-authored scalar; (3) claims on the old Linux
host's live surfaces — absent here, honestly `unavailable`; (4) editing the
frozen sweep `tools/mori-source-drift.py` — SKILL:905 pins its selftest tally
`PASS (6 cases)` and the r38 content anchors bind its source lines; (5)
editing the r65 adjudicator's committed behavior — its 5/5 selftest and live
receipts are committed evidence at those bytes; the new capability therefore
ships as a separate tool that IMPORTS the adjudicator (which imports the
frozen sweep) — policy shared by construction, no standing byte edited; (6)
re-declaring the admitted r64/r65 sweep/disposition work as claims. The
declared pair C1+C2 is each unreachable by a do-nothing round
(`.ufo/waves/round-66/evidence/controls-r66.txt`: the re-check tool absent,
no time-churn/as-of token in either standing instrument, no re-check receipt).

## Carry-ins from the r65 non-author closure (all three discharged)

1. Counting-command nit (`grep -c " drifted"` counted 10 = 9 rows + the
   summary line) — every count this round is row-line-isolating and carries
   its command beside it (`grep -cE "^S[0-9]{3} "` for row counts, `^rc=`
   for rc lines); the lesson mines the r65 nit as M1.
2. Census receipts carried no rc line — this round's census receipts embed
   the command header, the validator output and an explicit `rc=` line
   (`.ufo/waves/round-66/evidence/census-start-r66.txt`,
   `census-end-r66.txt`).
3. The standing adjudicate item — built as C1/C2 below: a re-check that
   records fetch-time and re-derives classes against the same-time snapshot,
   wired after the sweep and demonstrated on this round's own sweep.

## Gate

One source opened this round, fetched with `curl -sS -m 60 -L` into scratch,
pinned byte-identical into `corpus/evidence/sources-r66/` (S577 sha256
`93373f284ee448fcda0afdd60eb3717fa8fb4b0133260f5dc1212d624f635b7d`);
duplicate sweep before opening: `grep -c "sphinx-doc" corpus/SOURCES.md` → 0
and `grep -c "html_last_updated_fmt" corpus/SOURCES.md` → 0 at the pre-open
state.

- S577 Sphinx build configuration — html_last_updated_fmt
  (www.sphinx-doc.org) —
  https://www.sphinx-doc.org/en/master/usage/configuration.html — opened
  2026-11-01 — quote (`S577.html:2638`, tag-stripped): "a 'Last updated on:'
  timestamp is inserted into the page footer" (first 11 words of the
  16-word quote ending "using the given strftime() format" at `:2639`); utc
  variant `:2653-2654`; the sphinx-doc.org footer itself renders no stamp
  (option unset — "If set"; pin footer copyright `:5993`).

The row lands `mined`, used-by this lesson. C1's stamp grammar rests on
S577: the footer stamp is written at page-build time from a strftime format,
so a stamp-only delta between a pin and a fresh fetch is build churn, not
content drift — the exact signature the re-check's `time-churn` class
separates (QUALITY 158).

reject sample: none met — no source rejections this round; the fresh-start
rule-outs above are the round's reject-class decisions.

Census (validator): start receipt
`.ufo/waves/round-66/evidence/census-start-r66.txt` (this host, 2026-11-01,
rc 0, tolerated W04 duplicate-URL class, command + rc line embedded) → end
receipt `.ufo/waves/round-66/evidence/census-end-r66.txt` (rc 0). SOURCES row
count 349 → 350 (S577) counted by `grep -c "^| S" corpus/SOURCES.md`, the
lane's separate row-count instrument (the validator rc and this grep are
different instruments, per the r63/r64 precision corrections).

## Mistakes

1. class: a counting command that counts its own summary — the r65 report
   cited `grep -c " drifted" …drift-live-post-r65.txt` = 9, but the grep
   returns 10 (the 9 row lines + the `drifted=9` summary line); the claimed 9
   came from the summary token, not from the command shown beside it.
   captured-by: the r65 non-author closure re-ran the cited command and got
   10 (routed nit 1). fix: row-line-isolating counts (`^S[0-9]{3}` anchored)
   with the command beside every count it names — applied to every r66
   receipt and report count, e.g. the 8 baseline rows
   (`grep -c "^S" …adjudicate-baseline-r66.txt` = 8) and the 17 standing
   rows (`grep -cE "^S[0-9]{3} " …recheck-standing-r66.txt` = 17).
2. class: a selftest comparator that contradicts the output format it
   judges — the re-check's first selftest version compared the whole row
   line (`fresh as-of=…`) against the bare token (`fresh`), failing 5/7
   while the tool's classes were 6/6 correct in every failing run; the
   summary check then indexed group 11 (unavailable) where it meant group 12
   (window). captured-by: reading the FAIL detail before changing the tool —
   `got` held the right tokens with the `as-of=` suffix attached, so the bug
   was in the judge, not the judged. fix: comparator strips the `as-of=`
   suffix and compares the 11 numeric summary groups only; both bugs and the
   fix disclosed in the receipt header
   (`…/recheck-selftest-r66.txt`, three post-fix runs PASS 7/7 rc 0).
3. class: a fabricated-by-drafting anchor — the S577 row was first drafted
   with "the pin carries its own stamp `:2726`", a line number that does not
   exist (grep over the pin finds no footer stamp; the site leaves the
   option unset); the anchor word-count was also drafted 10 where the count
   is 11. captured-by: verifying every anchor line number against the pinned
   bytes before the row was cited anywhere. fix: cell corrected pre-commit to
   what the pin shows (`:2638`/`:2639`/`:2653-2654` verified, footer
   copyright `:5993`, first-11-of-16 words) — the same verify-anchors-before-
   landing discipline the r65 semantic review used.
4. class: a silently truncated file write — the SCORECARD round-66 section
   was appended with one long here-document write whose delimiter was never
   recognized ("here-document delimited by end-of-file"): the file was left
   cut off mid-word ("… stamp grammar covers the do") with no error surfaced
   by the write itself. captured-by: the read-before-commit landmark check
   the lane owes every landing — `tail` + `grep -c` of the section's known
   landmarks before staging showed the Planned paragraph truncated and the
   file 4 lines short. fix: the missing tail re-appended and every landmark
   re-counted green (header ×1, both claim rows, capability row, Planned ×1)
   before the commit; long appends are now verified by landmark count, not
   assumed complete because the command returned.

## Wave

None — no dispatch surface on this host (carried disclosure; the mori
round-62/round-65 L0 lines stand open, routed around, never treated as
answered). Round 66 ran L1-only over committed bytes and this host's network;
no wave-based evidence is claimed.

## Assimilation

considerthese mined (2026-10-19…2026-10-26, all eight files; no newer file
exists — checked this round): the 2026-10-26 suggestion 3 (re-execute what
closures only evidence-verify) was executed again this round — the fresh-start
counter re-derived and the time-sensitivity claim re-opened with a same-day
A/B (baseline adjudicator run re-taken before the tool was built) rather than
cited from the r65 closure. No still-unimplemented proposal adopted this
round. Assimilation: none — shokuknow unreachable.
