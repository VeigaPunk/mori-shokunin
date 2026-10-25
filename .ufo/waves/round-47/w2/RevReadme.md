# RevReadme — r47 w2 seat report (README "Round-47 coverage additions" block)

Seat: review `corpus/README.md` `## Round-47 coverage additions` (lines 644–655, the file's
terminal section) against the entry (`corpus/knowledge/oom-tracepoints-r47.md`) and rows
S475–S478/S005: counts carry commands, FR13 stays frontier, no overclaim of core coverage,
coverage-map/Frontier table consistency. All reads at the landed tip T = `68d66ca5` unless
stated; E = `2d85e33d`. Read-only git only; no repo or index mutation; scratch under
`.scratch/r47w2-RevReadme/`.

## Verdict

**Holds.** No defect that breaks a claim in the block. One minor finding (F1), two
observations (F2, F3). Every factual assertion I could re-derive reproduced.

## Verified holds (command + output)

- **V1 — the count carries its command and reproduces.** Block line 652: `Count: 8 —
  \`grep -c '^TRACE_EVENT(' corpus/evidence/sources-r47/include_trace_events_oom.h\`
  2026-10-25.` Re-ran it: stdout `8`, rc 0. The targeted copy's sha256 =
  `82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d`, equal to the frozen
  pin in `.ufo/waves/round-47/count-c2.py` (`PINS`) and the pin in the entry's `source:`
  line — the counted bytes are the pinned bytes.
- **V2 — "S005 re-opened, byte-identical to v7.2" is true.** (a) Pre-state: `git show E:corpus/SOURCES.md`
  row S005 reads `… | queued | 2026-10-19 | on-release | — |`; at T it is `mined … |
  corpus/knowledge/oom-tracepoints-r47.md` — the flip the block's "held only as … one queued
  field-schema row (S005)" presupposes, recorded in `corpus/lessons/round-47.md:21-23`.
  (b) Byte-identity: fetched
  `https://raw.githubusercontent.com/torvalds/linux/c03c1a14507dfaf8b856c2608f9ac216021fc222/include/trace/events/oom.h`
  (S005's URL, master blob) → sha256 `82f04ad4…e0d`, identical to the committed v7.2 tag
  copy `corpus/evidence/sources-r47/include_trace_events_oom.h`.
- **V3 — FR13 stays frontier, structurally and textually.** `git diff E T -- corpus/README.md`
  is +13 lines, all inside the appended `## Round-47 coverage additions` section (`@@ -640,3
  +640,16 @@`); the Frontier table and its FR13 row (README:353) are byte-unchanged and still
  read "… a resident tracer is outside the census, so retain this as knowledge/frontier
  only." The block's "(the host's `events/oom/enable` reads `0` and stays untouched)" matches
  the receipt `.ufo/waves/round-47/evidence/host-tracefs.txt:143-145` (`$ sudo -n cat
  /sys/kernel/tracing/events/oom/enable` → `0`, rc 0; receipt header declares read-only,
  2026-10-25). The entry's `ground:` quote of the row is verbatim modulo its ellipsis.
- **V4 — no overclaim of core coverage.** No Core move appears anywhere in the E→T corpus
  diff (`git diff --stat E T -- corpus/`: QUALITY.md, README.md, SOURCES.md, the four
  sources-r47 copies, the entry, the lessons file — SKILL.md and the Coverage map untouched).
  Each block content-claim matches the entry: "eight events, each with its `TP_STRUCT__entry`
  field set and the function that emits it" = the catalogue's 8 rows with fields + emitting
  function; "all pid-only after the mark" = catalogue fields for `wake_reaper`/
  `start`/`finish`/`skip_task_reaping` (`pid` only; only `mark_victim` carries comm/uid/
  memory); "what it never says (cgroup path, culprit)" = the entry's "What it changes for
  mori" paragraph. First-hand re-run: `TMPDIR=<scratch> python3 .ufo/waves/round-47/count-c2.py T`
  → `C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0
  pin_mismatch=0 source_row=ok provenance=ok`, rc 0 (matches receipt `evidence/after-c2.txt`).

## Findings

- **F1 (minor — Frontier FR13 row not appended; dispatch item unanswered in the landed
  text).** The w1 dispatch asked the scribe to "say whether the FR13 row text in the Frontier
  table needs an append-only note"; the landed block records no answer and the FR13 row
  carries no round-47 append, while sibling rows that gained ground did get dated appends
  (FR1 r15 note README:351, FR5 r33 :343, FR6 r33 :344, FR10 r26/r27 :348). Consistency
  itself holds — the row's boundary text remains true and the block asserts "FR13 stays
  frontier" — but the row's evidence cell still cites only `SOURCES.md:11-12,23-26`
  (S005/S006, S017–S020: bpftrace tooling rows; all still on-target), so a reader landing on
  the Frontier row cannot discover that the map now holds a full field-level catalogue. Fix
  is one append-only boundary sentence (r47 adds the catalogue, `knowledge/oom-tracepoints-r47.md`,
  S475–S478; resident tracing stays frontier) or an explicit "no row note needed" line in the
  block. No false claim today; discoverability gap only.
- **F2 (observation — S478 absent from the block's pointer list).** The block lists "(S475
  header, S476 call sites, S477 this host's tracefs listing; S005 re-opened, byte-identical
  to v7.2)" and omits S478 (ROMA full text p. 3016), which the entry cites in `source:` and
  uses for the refused "exactly three tracepoints" headline. The w1 dispatch scoped the
  scribe to "rows S475–S477", the block never claims to enumerate all entry sources, and the
  refusal is recorded via the entry + `corpus/lessons/round-47.md` Gate. Not a correctness
  defect; noted because the round's claim surface (entry + rows) is S475–S478.
- **F3 (pre-existing, outside the assigned diff — `## Coverage map` table drift).** The
  Coverage map table (README:3-51) ends at `knowledge/census-cgroup-levels-r45.md` and has no
  rows for the r42–r47 knowledge entries (`oom-evidence-loss-r38`, `oom-victim-context-r41`,
  `journal-disk-usage-total-r51`, `pid-probe-conclusion-r44`, `oom-tracepoints-r47`). The r47
  diff neither caused nor worsened this, and P-C2 (contract) requires no README map row, so
  the r47 block is not at fault; flagging for the map's owner since the table silently
  stopped being the per-note map after r45.

## Residual risk / verification gaps

- S477 (host tracefs listing) and the S478 page-3016 quote are accepted from the committed
  receipts (`evidence/host-tracefs.txt`; `corpus/lessons/round-47.md:17` with the PDF sha256
  `1603404d…6add2`) — I did not re-read tracefs as root beyond what the receipt shows, nor
  re-extract the PDF. C2 first-hand covers every name/field/callsite against the pinned
  committed copies, which is what the block's count rests on.
- I did not audit `corpus/QUALITY.md` or `corpus/lessons/round-47.md` content beyond the
  S005 flip and Gate pointer (other seats' scope).

No actionable defect remains in this seat's scope.
