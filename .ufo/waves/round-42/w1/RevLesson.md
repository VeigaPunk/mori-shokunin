# RevLesson — review of corpus/lessons/round-42.md (tip 34b9267)

Scope: every Gate row's URL/access-date/quote vs committed copies under
`corpus/evidence/sources-r42/`; refusal reason+flip; Mistakes rows
class/evidence/captured-by/fix; overclaims. Read-only; no files mutated.

## Findings by severity

### HIGH — M3 fix claim is false; the recheck never printed 1

`corpus/lessons/round-42.md:83` (M3 fix): "row S262 and the adopted entry now
carry a recheck that ran green on 2026-10-24 (`grep -c 'lack sufficient
container context'` → 1)". The committed recheck at
`corpus/knowledge/oom-victim-context-r41.md:6` is

    curl -fsSL 'https://api.openalex.org/works/https://doi.org/10.1109/TSC.2026.3698682' | grep -c 'lack sufficient container context'

I re-ran the exact URL read-only from /tmp on 2026-10-24: the response
(67270 bytes, byte-identical in size to the committed
`corpus/evidence/sources-r42/S262.oa.json`) contains the abstract ONLY as
`abstract_inverted_index` — the only `abstract*` key present. A literal
`grep -c 'lack sufficient container context'` returns **0**, never 1. The
abstract text IS verifiable (reconstructing the inverted index yields the
quoted sentence verbatim), but the recorded recheck command cannot produce
the recorded result. M3's fix repeats the stale-premise class it claims to
close: a written-down receipt that was never re-runnable as stated. The
row/entry still overclaim a green recheck.

### HIGH — S235 registry pin is a typo; "byte-identical to the pin" fails vs the row

Lesson line 41 claims "sha256 byte-identical to the pin". Computed
`sha256(corpus/evidence/sources-r42/S235.pdf)` =
`9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30dca99359e6df057ad8020`.
`corpus/SOURCES.md:241` pins
`9855a4986a312dfc946b1b97b6010a8e4f1e65a4a30cda99359e6df057ad8020`
— transposition `…4a30**dc**a…` → `…4a30**c**da…` (chars 41-44). The committed
PDF is byte-identical to the *correct* hash and to the hash quoted in
`corpus/knowledge/oom-evidence-loss-r38.md` (source line for S235), but it
does NOT match the registry pin the lesson invokes. The row's pin cell was
landed corrupted this round.

### HIGH — stale contradictory source line left in the adopted entry

`corpus/knowledge/oom-victim-context-r41.md` carries two `source:` headers:
line 1 (corrected: "publisher-deposited OpenAlex record") and line 4
(stale: "Abstract and TLDR, as recorded by the publisher's **Semantic
Scholar** record and by OpenAlex") — directly contradicting the entry's own
line 46 ("Semantic Scholar lacks the DOI") and the Gate's M3 premise. The
re-grounding edited line 1 and line 46 but left the original stale line in
place; the entry now states both that S2 carries the record and that S2
lacks the DOI.

### MEDIUM — S232 locator "html line ~25427" is bogus; the unit is wrong

Lesson line 28 cites the S232 quote at "html line ~25427". Committed
`S232.html` is 665 lines total; the quote sits at line 441 (byte offset
~31126). No unit makes "~25427" resolve. POLLPRI count 4 ✓ (4 lines), URL
✓, 節「メモリコントローラの状態通知」 present at bytes 15562/28912.

### MEDIUM — S233 section attribution slightly off for the dmesg example

Lesson lines 30-33 cite the dmesg line as being "節「OOM処理の充実」dmesg
example". In `S233.html` the `[ 1845.213445] stress-ng invoked oom-killer`
line is at line 549, under `memory.max` (h3 at 446) inside
節「メモリ使用の制限値」 (h2 at 412). 「OOM処理の充実」 (h3 at 298) is an
earlier prose section with no dmesg transcript. The worked example itself
verifies: `memory.highに制限値128MBを追加` at line 624 with 256M stressor,
and "OOM Killerが発動したログは出力されていません" in the transcript.
Claim substance stands; section pointer is wrong.

### LOW — S234 "anchor count 3" is unverifiable as stated

Lesson line 37: "(copy `S234.c`, anchor count 3)". `grep -c
container_supervisor_add_exit_monitor S234.c` = 1; `epoll_loop_add_handler`
= 2; `oom_event_fd` = 1. The number 3 is only consistent with counting the
three in-function line anchors named in SOURCES.md row 240 (lines 348/375/
381) — all verified present. If "anchor" meant occurrences in the copy, the
count is wrong; as a count of cited anchors it is defensible but unclear.

## Verified clean

- URLs/access dates: all seven rows carry accessed/refetched 2026-10-24;
  URL strings match the copies (og:url / canonical content for S232, S233,
  S241, S347; filename+SOURCES row for S234, S235; `doi` field in
  S262.oa.json).
- Quotes located verbatim in the copies: S232 (line 441), S233 (128MB/256M
  worked example, no-OOM transcript), S234 (line 381 epoll_loop_add_handler
  under ENABLE_OOM_MONITOR), S235 (p.27 约束限制, `无法成功捕捉容器` count 1
  in pdftotext), S241 (節「診断」 h3 line 738; 診断 count 3;
  `ms.translationtype: MT` line 89; KB 4010058 line 707), S262 (abstract
  reconstructs the quoted sentence exactly from the inverted index), S347
  (§ast.walk line 2862ff, "Recursively yield all descendant nodes … in no
  specified order").
- Refusal: `.ufo/waves/round-42/assimilation/refused-oom-tracing.md` carries
  the reason (ieeexplore HTTP 202 + 0-byte body; OpenAlex
  `any_repository_has_fulltext: False`) and an explicit flip condition
  (fetchable VOR PDF → re-enter gating). Reason+flip present ✓.
- Mistakes rows: all four rows have class/evidence/captured-by/fix cells
  populated ("none" is an allowed captured-by value). M1 receipts
  (`control-c2-before.txt`, `control-c3-before.txt`) exist with
  `mode=before` and expected FAILs. M4 crash receipt
  `evidence/c1-after.txt:30-41` shows the exact `TypeError: run() got an
  unexpected keyword argument 'cwd'` at count-c1.py line 244;
  `c1-noharm-manual.txt` is the committed manual re-derivation.
- Collision census numbers match receipts: reg-ids = 231 lines, staged-ids
  = 115, collisions file = 0 rows. Validate receipt ends `file ok`.
- "All five cited sources re-fetched" for r38: the entry cites exactly
  S232/S233/S234/S235/S241 = 5 ✓. QUALITY 114 exists and cites the
  considerthese "cumulative survivor ledger" proposal ✓.

## Residual risk / gaps

- "Rows touched old→new: none" (append-only claim) was not independently
  diffed — it is a prior-revision comparison outside the committed copies;
  consistent with the collision/census receipts but unproven by me.
- M2's red-before witness ("false E11 run retained in the wave tree") was
  not located beyond the named clause; the census tool lives in the fleet
  repo (`scripts/sources-census.sh`) so its cwd semantics were not
  re-executed.
- The S235 pin typo (HIGH #2) is one transposed hex pair — trivially
  fixable, but it is exactly the class of stale/false pin the Gate exists to
  catch, and the lesson asserts byte-identity against it.

## Tooling

No installs/updates. Used system pdftotext, sha256sum, grep, curl (read-only
recheck of the public OpenAlex API from /tmp).

Report: .ufo/waves/round-42/w1/RevLesson.md
