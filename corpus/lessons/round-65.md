# Round 65 — mori (L1 MoriR65, the 23-row drift disposition + the drift-adjudicator capability)

author: mori L1 (MoriR65)
round: 65
date: 2026-11-01
entering: `7d369cd2`

## Fresh start (r59–r61 rejected closures re-read; what was ruled out)

The §7 digests name r59/r60/r61 `rejected-honest-stop`; the fleet MANIFEST
records rounds 62–64 as the subsequent state (r64 closed with routed defects,
both of which are this round's carry-ins and are discharged below). The
fresh-start duty was performed on the three listed rounds as bound —
spot-checks re-run this round (receipt
`.ufo/waves/round-65/evidence/freshstart-spotchecks-r65.txt`): the r61 honest
stop re-derived from the frozen counter at the r61 data tip
(`python .ufo/waves/round-61/count-c2.py 986d4b46…` → `C2=unmet` with all 14
quote_words anchors, rc 1 — same verdict the r61 closure reached); r59/r60
cited evidence `git cat-file -e` PRESENT and both revisions
`merge-base --is-ancestor` of refs/heads/master, rc 0 each.

Ruled out as r65 claims, and why: (1) re-declaring entry-claims-class work on
the r59/r60 instruments — the met-flip counterexamples stand on frozen bytes;
(2) scalar score moves — no closure states a new number and no lane
convention licenses an L1-authored scalar; (3) claims resting on the old
Linux host's live surfaces — absent here, honestly `unavailable`, never
zero; (4) SKILL.md gate-registry row edits — parsed and baseline-bound by
the reconciler, L0 class, and discovered binding this round: `SKILL.md:905`
pins the drift sweep's selftest tally `PASS (6 cases)` and the r38 content
anchors (`count-c4.py`) bind the sweep's source lines, so ANY edit to
`tools/mori-source-drift.py` risks decertifying a standing admitted
instrument — the new capability therefore shipped as a separate tool that
IMPORTS the frozen module (policy shared by construction, frozen bytes
untouched); (5) re-declaring the r64 sweep as a claim — it is admitted; its
routed carry-in (the 23-row disposition) is the work, claimed as C1. The
declared pair C1+C2 is each unreachable by a do-nothing round
(`.ufo/waves/round-65/evidence/controls-r65.txt`).

## Carry-ins from the r64 non-author closure

1. LOG r64 number-drift ("Mistakes mined: three" vs the lesson's four) —
   appended correction entry in the r64 LOG entry's tail (append-only, no
   rewrite), naming the omitted fourth mistake (the S575 quote word-count).
2. The in-place-correction precedent (closure observation 2) — kept narrow:
   the only change this round makes to a prior entry is that appended block;
   no in-place edits to any prior entry or lesson.
3. The standing 23-row disposition + re-sweep — discharged as C1 (below):
   every row re-opened, classed with fresh two-UA evidence, re-pinned loudly
   or kept with renewed evidence, then the sweep re-run to an honest
   remainder.

## Gate

One source opened this round, fetched with `curl -sS -m 60 -L` into scratch,
pinned byte-identical into `corpus/evidence/sources-r65/` (S576 sha256
`4671f96d60872768fb0caa4f50e981fd559a3213e94a40bee496027cf66876d9`);
duplicate sweep before opening: `grep -c "docs.openalex.org"
corpus/SOURCES.md` → 0 at the pre-open state, no reconciliation needed.

- S576 OpenAlex works — work object (docs.openalex.org) —
  https://docs.openalex.org/api-entities/works/work-object — opened
  2026-11-01 — quote (`S576.html:62`): "OpenAlex does not ship plaintext
  abstracts for legal reasons; reconstruct the abstract from the index."
  (15 words). The `abstract_inverted_index` heading is at `:61`; the
  shared-attribute note naming `created_date`/`updated_date` at `:36`.

The row lands `mined`, used-by this lesson. C1's S262 disposition is the
sourced claim: the field-level record diff (updated_date, related_works,
language, enrichment percentile changed; abstract_inverted_index unchanged)
is only interpretable because the vendor documents that the abstract ships
as an inverted index and that `updated_date` is a vendor-managed shared
record attribute — a refetched record differing in metadata is record churn,
not abstract drift.

reject sample: none met — no source rejections this round; the fresh-start
rule-outs above are the round's reject-class decisions. (The work-fields and
common-attributes pages on the same docs site were fetched while locating
the ground for S262, found to be SPA shells that defer `updated_date` to the
work-object page's Common-attributes note, and NOT given rows — the
work-object page is the one that teaches.)

Census (validator): start receipt
`.ufo/waves/round-65/evidence/census-start-r65.txt` (this host, 2026-11-01,
rc 0, tolerated W04 duplicate-URL class) → end receipt
`.ufo/waves/round-65/evidence/census-end-r65.txt` (rc 0). SOURCES row count
348 → 349 (S576) counted by `grep -c "^| S" corpus/SOURCES.md`, the lane's
separate row-count instrument (the validator rc and this grep are different
instruments, per the r63/r64 precision corrections).

## Mistakes

1. class: fetched URL list written with CRLF line endings — the disposition
   runner's row-URL list was produced by a Python text-mode write on Windows,
   so every URL carried a trailing `\r`; all 46 first-run fetches died
   `curl rc 3 "URL rejected: Malformed input to a URL function"` with zero
   bytes fetched. captured-by: reading the first result line before scoring
   anything (the r64 concurrent-load discipline — a failed receipt is
   compared, not explained away). fix: list rewritten LF-only and the whole
   fetch re-taken clean as the sole fetch process; the run-1 failure is
   disclosed in the receipt header
   (`.ufo/waves/round-65/evidence/disposition-refetch-r65.txt`).
2. class: verification greps polluted by their own separator — the
   teaching-anchor grep helper passed `--` through as if it were a needle,
   so its per-row counts included a grep for the literal string `--` and
   undercounted rows whose real needle was markup-split. captured-by: a
   count that could not be true (0 hits in the pinned bytes for an anchor
   the row quotes) was probed needle-by-needle against both pin and fresh.
   fix: first counts discarded, never cited; the landed receipt carries
   probe-verified counts only
   (`disposition-semantic-review-r65.txt`).
3. class: receipt pipeline captured the wrong process's exit status — the
   selftest battery piped every selftest through `tail -1`, so its rc lines
   showed tail's 0 regardless of the tool's status, and it caught one
   transient drift-selftest FAIL (5/6) without naming the load condition.
   captured-by: reading the receipt before commit (the r64 heredoc-truncation
   discipline: every large receipt gets a read-before-commit landmark
   check). fix: receipt v1 discarded (reason recorded in the receipt), v2
   re-taken with per-tool real rc capture, the drift selftest and the new
   adjudicator run three times each, and the degraded-transport condition
   disclosed (`evidence/selftests-r65.txt`).

Finding, disclosed not fixed (routed to the operator via the L0 side
channel, `mori | round-65`): this host's loopback HTTP transport is degraded
and variable — the r64 certification measured `transport_cap=65536`; today's
runs measured 1024, 4096 and 16384 across runs, and one run dropped even the
small `fresh` fixture fetch (FAIL 4/6, passing 3× immediately after). The
v1.1 `huge_cap` arm degrades exactly as designed (fixture scales, frozen
literal stays asserted); the `row_states` arm is exposed to the flaky
transport, so a red selftest receipt on this host is not yet proof of
instrument decay — it needs the transport condition named beside it. The
instrument is tally-pinned (`SKILL.md:905`) and therefore not lane-editable;
the L0 line asks for the operating posture (standing adjudicate step,
instrument change, or accept-and-disclose).

## Wave

None — no dispatch surface on this host (carried disclosure; the mori
round-62 L0 line stands open, routed around, never treated as answered).
Round 65 ran L1-only over committed bytes and this host's network; no
wave-based evidence is claimed.

## Assimilation

considerthese mined (2026-10-19…2026-10-26, all eight files; no newer file
exists): the 2026-10-26 suggestion 3 (re-execute what closures only
evidence-verify) was executed again this round — the fresh-start counter
re-derived and all 23 findings re-opened and re-fetched rather than cited
from r64's receipts. No still-unimplemented proposal adopted this round.
Assimilation: none — shokuknow unreachable.
