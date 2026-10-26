# Mo50bConnSalvage — attempt-1 salvage audit (mori round 50, wave a2w1)

Seat: connector, leaf. Assignment: audit the five salvaged w1 reports (committed at
`9b8562a371dc916fdc0fc686619ea1e271a3e118`) against the data landed at
`487941b9395e89678af0053cc443cdb49cdee6e3`; for each report say what it claimed, which of its outputs the
landed data uses, and whether those reused outputs are re-verified by the attempt-2 counters/receipts;
answer whether EntryB found anything EntryA's draft (the landed entry) lacks or gets wrong; emit a
REUSED / DISCARDED list with reasons.

Posture: read-only. No lane file was edited, staged, or committed. No mutating git/jj command ran; only
read-only `git log/show/diff/rev-parse/grep` and the frozen counters. No kernel log MESSAGE text was read;
no host state was touched; no tool was installed or upgraded (nothing was needed; no pacman transaction
attempted — host-wide pause respected). No subagents. Scratch: `/fast/scratch/hyaku/mori-r50/Mo50bConnSalvage/`
(removed at the end; every quoted byte below is re-derivable from the repo).

## Verdict (answers first)

- The landed data is overwhelmingly **EntryA's work**: the entry
  `corpus/knowledge/oom-memcg-stat-r50.md` is byte-identical to EntryA's Draft 1 plus one inserted
  `## Claims` heading; the three SOURCES rows are EntryA's Draft 2 with only the scope and anchor cells
  rewritten (9 of 11 cells byte-identical per row).
- EntryB's independent draft found **no error** in EntryA's draft on any point it checked, and my own
  spot-checks of the shared claims against the committed copies agree. EntryB does surface 4–5 substantive
  rows/sections EntryA lacks (see §5); none is in the landed entry.
- The two row-seat drafts (RowMemcontrol S490, RowOomKill S491) were **not** landed as rows, but their
  analyses materially shaped the landed rows' rewritten scope/anchor cells, and RowOomKill's two process
  warnings (W04-not-E04; entry+row landing coupling) were both honored and are re-verified at the landed tip.
- The scout's report was **guidance only**; of its concrete asks, only "the L1 must append S489–S491"
  and the S004-master-commit caution left traces in the landed data. Its must-link list, coverage-map
  block, FR1 append note, and proposed Boundaries line are **not** in the landed data.
- Every reused output is **re-verified** at the landed tip by the frozen counters (I ran both:
  `C1=met` and `C2=met` at `487941b9`), by the lane census (`rc=0`, W04 S491 present), and by the L1's
  live re-fetch receipt (`assimilation/a2/live-sha-L1.txt`, all three sha256 reproduced 2026-10-26).

## 1. Where the landed data came from (commit map, observed)

```
$ git log --oneline -8            # in /home/vgpnk/Projects/shokunin/mori-shokunin
4548a34d round-50: attempt-2 wave a2w1 spec ... + counter receipts at data commit 487941b9 (C1=met, C2=met)
487941b9 round-50: data (attempt 2, L1 MoriR50a2) — C1 Axes cells reconciled ... C2 rows S489-S491 appended ...
9b8562a3 round-50: hyaku run-8 orchestrator salvage of unlanded attempt-1 wave state and knowledge draft ...
649e14cf considerthese: 2026-10-26 daily reflection
950e99be round-50: freeze — contract, counters C1/C2, controls and receipts, assimilation scratch, source copies
7197160b hyaku run 7 interrupted ... (entering tip named by the contract)
```

- `git log --follow -- corpus/knowledge/oom-memcg-stat-r50.md` → the entry exists only from `9b8562a3`
  (the orchestrator salvage of the dead attempt-1 L1's working tree). `git diff 9b8562a3 487941b9 --
  corpus/knowledge/oom-memcg-stat-r50.md` is **empty**: the attempt-2 data commit did not touch the entry.
- `git show --stat 487941b9` → that commit changed only: `SCORECARD.md`, `SHONEN.md`, `corpus/SOURCES.md`
  (+3 rows), and `assimilation/a2/{append-block.md, live-sha-L1.txt, mirror-validate.txt}`.
- `git show --stat 9b8562a3` → the salvage committed the five w1 reports, the two C1 selftest receipts
  (`.ufo/waves/round-50/evidence/selftests/{mori-pin-check,mori-unlanded-check}.txt`), and the entry.
- Frozen files unchanged since the freeze: `git diff 950e99be HEAD -- count-c1.py count-c2.py contract.md`
  → empty (rc 0). The counters I ran are the frozen counters.
- `git diff 7197160b HEAD -- corpus/README.md PROVINCE.md corpus/knowledge/ SKILL.md` → only the new
  entry file; the scout's coverage-map / FR1-row targets were **not** edited.

## 2. Per-report audit

### 2.1 Mo50ScoutCoverageFR1 (coverage/adjacency scan; no data drafts)

**What it claimed.** The memcg OOM dump block is new ground for mori (FR1's "what the kernel prints"
half only; no closure); no sibling contests it (tsukuroi holds adjacent live readings / label counts);
S489–S491 are absent from `SOURCES.md` and the L1 must append them; the entry should carry seven links
(r12, r41, r47, r45, oom-kill-counter-r12, oom-evidence-loss-r38, optional tsukuroi two); a coverage-map
"Round-50 coverage additions" block and a dated FR1 append-only note should be added to
`corpus/README.md`; its own "Boundaries" line text; S004's `memcontrol.c:1820-1826` anchor is a
master-commit coordinate that must not be reused for v7.2; units claims need quote backing. Honest
limits: it never opened the v7.2 copies, the counter, or the contract.

**What the landed data uses.** Guidance-level reuse only:
- Its MED finding "S489–S491 must be appended; last row is S488" was acted on (rows landed at
  `corpus/SOURCES.md:268-270`, immediately after S488).
- Its MED finding on S004 master-commit drift is echoed twice: landed S490 scope says
  "; not the master-commit path labels of S004", and RowMemcontrol's same analysis (§2.4) is the
  likely direct donor. [INFERENCE] the L1 did not document cell authorship; attribution is textual.
- Not used: the seven-entry link list (grep over the landed entry for all seven names → 0 hits), the
  coverage-map block, the FR1 append-only note (README unchanged), its Boundaries line (EntryA's
  Boundaries section stands).

**Re-verified?** N/A — nothing of the scout's was landed as data; the two asks that were acted on are
verified by the landed state itself (rows present after S488; S004 scope boundary in S490).

### 2.2 Mo50ScribeEntryA (entry draft + S489–S491 row drafts + validation)

**What it claimed.** A 22-row entry (7×S489, 8×S490, 7×S491) whose quotes are exact substrings of the
counter-normalised copies; three 11-cell row drafts; fixture end-to-end `C2=met` (revs 7189a117 /
013fa55a2 on its scratch fixture); three falsifier runs (altered quote → `quote_missing`; opened-date
and removed-S491 rows → `bad_rows,source_rows,sources_floor`); per-row `located=True` table; staged
r46/r47 candidates corrected-not-adopted (tmpfs hypothesis, /tmp fixture, journalctl MESSAGE read, no
table); the report's fenced drafts are byte-identical to the tree that scored `C2=met` (Draft 1 sha256
`37dc8bc8…`, 10508 bytes per its count).

**What the landed data uses.** Almost everything:
- Landed entry = EntryA Draft 1 **verbatim plus one insertion**. Observed diff (extracted fenced draft
  vs `git show 487941b9:corpus/knowledge/oom-memcg-stat-r50.md`):

  ```
  15a16,18
  >
  > ## Claims
  >
  ```

  i.e. blank line + `## Claims` + blank line before the table (10526-byte extraction + 12 bytes =
  10538 landed bytes; extraction sha256 prefix `37dc8bc848f3ad6c` matches the report's claimed digest).
  All 22 claim rows, the front matter (source:/verified-at:/recheck: with the live curl+sha256 loop),
  Reading rules, Limits, and Boundaries are EntryA's bytes.
- Landed rows = EntryA Draft 2 as the base: **9 of 11 cells byte-identical per row** (all except scope
  and anchor). teaches cells are EntryA's verbatim (e.g. S490 teaches "The OOM report and the memory.stat
  file share memory_stat_format, and on cgroup v2 the printed failcnt is the MEMCG_MAX event counter,
  not a per-page charge count.").
- Rewritten cells (L1 synthesis, matching no draft verbatim; cell-level diff observed):
  - S489 scope adds "at kernel 7.2" and "; not the kernel print formats (S490, S491) and not any host's
    values" (cf. EntryB's "not any host's values and not the kernel print formats");
  - S489 anchor adds "; copy corpus/evidence/sources-r50/cgroup-v2.7.2.html sha256 2d716cb7…; adopts
    staged S533 renumbered by document" (copy+sha style as in the row-seat/EntryB drafts);
  - S490 scope adds "at tag v7.2" and "; not the master-commit path labels of S004" (RowMemcontrol's
    S004 analysis);
  - S490 anchor adds "; copy …/memcontrol.c.v7.2 sha256 8a28e0bc…";
  - S491 scope adds "at tag v7.2" and "; same URL as S003 and S476 with a different scope"
    (RowOomKill/EntryB/contract language);
  - S491 anchor adds "; copy …/oom_kill.c.v7.2 sha256 452f1348…".

**Re-verified?** Yes, by the frozen counter at the landed tip, which I ran:
`python3 .ufo/waves/round-50/count-c2.py 487941b9395e89678af0053cc443cdb49cdee6e3` →
`C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok`
(rc 0). `pins=ok` re-hashes the three committed copies against the frozen COPIES pins (re-verifying the
recheck: line); `located=22` re-runs the quote-location checks EntryA documented per-row; `source_rows=ok`
re-validates the three rows (mined, 2026-10-26, used-by). The L1 additionally re-fetched all three URLs
live (`assimilation/a2/live-sha-L1.txt`, 2026-10-26T09:26-03:00, all three sha256 identical to the
committed copies) — re-verifying EntryA's "live bytes still identical" claim on fresh bytes, and landed
the rows only after a mirror census run `rc=0` (`assimilation/a2/mirror-validate.txt`, 22 W04 lines
including `W04 S491 duplicate url …/oom_kill.c across scopes`).

EntryA's own fixture revs are scratch-only and long deleted; its fixture claims are not independently
re-runnable, but the same frozen counter now scores the same draft bytes at the landed lane revision,
which is the stronger statement.

### 2.3 Mo50ScribeEntryB (independent 21-row entry draft + row proposals)

**What it claimed.** An independently drafted 21-row entry (10×S489, 7×S490, 4×S491) that scored
`C2=met claims=21` end-to-end on its own scratch fixture (rev `de9e912f…`, since deleted) and through the
counter module's `evaluate()`; a block-by-block printk-order list; a key/units table; a decision table; a
"what this changes for mori" link set; proposed S489–S491 rows; findings: no S489–S491 rows and no entry
exist at the tip (both HIGH), rate-limit asymmetry (MED), typed-quote/normalisation concerns (MED),
quote-ambiguity of short spans and non-entailment rows (LOW), internal-unit mis-scaling (LOW,
[INFERENCE]). It explicitly noted overlap with EntryA's and RowOomKill's drafts and "no factual conflict
found on the points I checked".

**What the landed data uses.** Not the drafts. The L1 landed EntryA's entry and EntryA-based rows.
Closest reuse: the landed rows' rewritten scope/anchor cells match EntryB's *style* (copy path + sha256
in the anchor cell; exclusion clauses in the scope cell) more closely than EntryA's originals — e.g.
landed S491 scope "; same URL as S003 and S476 with a different scope" ≈ EntryB's S491 scope tail, and
all three landed anchors carry "copy corpus/evidence/sources-r50/<file> sha256 <digest>" as in EntryB's
and RowOomKill's drafts. [INFERENCE] textual style match; the L1 left no authorship note. EntryB's
"opens 2026-10-26 / mined / used-by the entry" row mechanics are the same mechanics EntryA used.

**Re-verified?** Partially, indirectly. EntryB's fixture claim (rev `de9e912f`) is **UNVERIFIED** — the
fixture was deleted with its scratch. EntryB's substantive cross-checks that do appear in the landed
data (v2 failcnt = MEMCG_MAX, rate-limit guard asymmetry, global-vs-memcg branch) are re-verified
because EntryA's landed rows carry the same quotes and the counter located all of them. Its unique rows
(§5) were not landed, so nothing of theirs needs verification.

### 2.4 Mo50ScribeRowMemcontrol (S490 row draft + S004 comparison + helper quotes)

**What it claimed.** An 11-cell S490 draft (scope "the memcg OOM report block only…", per-function anchor
list 1791-1830 etc.); a Gate-block line; a grounded S004-vs-S490 scope difference table (master
`c03c1a14…` vs tag v7.2: same objects sit 45–84 lines apart); six helper quote spans for the entry
seat, each located with the counter's `normalise_text`; live fetch of the v7.2 URL `http=200 size=160768
sha256 8a28e0bc… BYTE_IDENTICAL`; a census E11 methodology finding (`--file` mode resolves used-by
against the copy's parent — mirror runs are the only informative ones); findings on E11 landing coupling
and S004 anchor drift.

**What the landed data uses.** The row draft itself: **not landed** (its verbose per-function anchor and
narrow "report block only" scope were replaced by EntryA's anchor style plus one clause of its analysis).
Reused traces:
- Landed S490 scope: "; not the master-commit path labels of S004" — a direct descendant of its
  S004-comparison section (finding LOW-3 in its report).
- Its helper quotes are the same spans EntryA landed in rows 8, 11, 12 (e.g. helper 5/6 =
  `seq_buf_init(&s, buf, SEQ_BUF_SIZE); memory_stat_format(memcg, &s); seq_buf_do_printk/seq_puts`)
  — convergent derivation or donor; either way the landed quotes are counter-located at R.
- Its live-fetch method is what the L1 repeated for all three URLs in `live-sha-L1.txt`
  (re-verifying its byte-identical claim on the same day).

**Re-verified?** The parts that landed: yes — S490 row `source_rows=ok` at R; the v7.2 sha256 re-confirmed
live by the L1 receipt and by the counter's `pins=ok` (which I observed in my own run). Its E11 warnings
were honored: the rows landed in the same data commit as the (already-salvaged) entry, and the
round-end census I ran at HEAD reports `mori ok … SOURCES.md`, rc 0, with the only new warning the
expected `W04 S491`.

### 2.5 Mo50ScribeRowOomKill (S491 row draft + W04-not-E04 proof)

**What it claimed.** An 11-cell S491 draft (scope: dump_header branch + victim-line fields; anchor with
call sites ":1031 and :1075", copy sha256, live-fetch note); a proof by two census fixtures that a
different scope → `W04` (rc 0) while an identical scope → `E04` (rc 1); live fetch `http=200 size=34311
sha256 452f1348…` byte-identical; five candidate located quotes for the entry seats (with an 11-word
victim-line quote at :945 and a 6-word branch quote at :464-466); findings: E11 coupling (integrate the
entry with the rows), scope-verbatim warning (harmonising scopes converts W04 into E04), stale-(S490)
parenthetical risk, census W04 count going 21→22, `count-c2` first-URL-match note, and
"call sites :1031 and :1075" as un-reopened anchors.

**What the landed data uses.** The row draft itself: **not landed** (EntryA's anchor style chosen).
Reused traces:
- Landed S491 scope: "; same URL as S003 and S476 with a different scope" — its central W04 analysis,
  matching the contract's own framing.
- Its anchor-cell style ("copy corpus/evidence/sources-r50/oom_kill.c.v7.2 sha256 452f1348…") is the
  style all three landed anchors now carry.
- Its two process warnings were honored and are re-verified: the S491 scope landed verbatim-different
  from S003/S476 (census at HEAD: `W04 S491 duplicate url …/oom_kill.c across scopes`, lane `ok`, rc 0 —
  I ran it), and the entry existed before the rows landed (no E11; mirror-validate.txt rc 0).

**Re-verified?** Yes for the landed traces (census rc 0 at HEAD; counter `source_rows=ok` at R; live
sha256 re-confirmed in `live-sha-L1.txt`). Its "call sites :1031 and :1075" was **incomplete** — there
is a third `dump_header(oc)` call at `oom_kill.c.v7.2:1158` (the `out_of_memory` "Found nothing?!?!"
path) — but that draft was discarded and the landed S491 anchor carries no call sites, so nothing false
landed.

## 3. Did EntryB find anything EntryA's draft (the landed entry) lacks or gets wrong?

**Wrong: nothing found.** EntryB's own cross-check reported no factual conflict; my spot-checks of the
claims both drafts share agree with the committed copies:
- v2 failcnt = `memory_events[MEMCG_MAX]` — copy lines 1800-1803 match EntryA row 9's quote (and
  EntryB's identical quote);
- rate-limit asymmetry (`if (__ratelimit(&oom_rs)) { dump_header(oc); dump_oom_victim(oc, victim); }` at
  1030-1033 vs the unconditional victim `pr_err` at 945) — matches both drafts' quotes;
- global-vs-memcg branch (`if (is_memcg_oom(oc)) mem_cgroup_print_oom_meminfo … else { __show_mem …`) —
  matches;
- units (kB charge/victim lines, bytes for state keys, bare counts for event keys) — consistent in both;
- EntryB's block-by-block printk order (invoked oom-killer → charge line(s) → stats block → protected
  memory + Tasks state → oom-kill summary → Killed process) matches the call order in the copy
  (`dump_header` 456-475 then `dump_oom_victim` 444-454, per the 1031-1033 call site). EntryA's draft
  makes no order claim, so there is nothing to correct.

**Lacks (substantive items in EntryB with no counterpart in the landed entry):**
1. The summary's constraint field **names** the OOM type: `oom_constraint_text[CONSTRAINT_MEMCG]` for a
   memcg OOM. EntryB has a dedicated row (quote: the `oom_constraint_text` table, lines 239-244 region)
   and prose ("The constraint field reads CONSTRAINT_MEMCG… so the summary alone identifies which report
   shape follows"). The landed entry's row 20 says the summary "records the constraint and nodemask"
   without naming the CONSTRAINT_MEMCG value; the value appears nowhere in the landed entry.
2. `memory.oom.group` **document-level semantics** ("all tasks belonging to the cgroup or to its
   descendants … are killed together" — the indivisible-workload property). The landed entry covers
   group kills only via the S490 kernel print row + one reading rule.
3. `memory.events.local` vs `memory.events` (EntryB S489 row 8). Note the scout explicitly told the
   entry **not** to restate that distinction (it belongs to `census-cgroup-levels-r45.md`), so its
   absence from the landed entry is consistent with the wave-1 boundary, not an oversight.
4. Static-table grounding for key order (`memory_stats[]` first entries `{ "anon", … } { "file", … }
   { "kernel", … }`, line 1546ff) and the per-item output-unit conversion step
   (`memcg_page_state_output`). The landed entry instead quotes the two `seq_buf_init/…` call sites,
   which prove the shared formatter but not the key table.
5. Structural extras EntryB drafted and EntryA did not: a key/units table, a decision table, a
   "what this changes for mori" section. (EntryA's Reading rules / Limits / Boundaries stand in the
   landed entry.)

Conversely, EntryA's landed draft has rows EntryB lacks (swap charge line as a table row; the
pre-signal `count_vm_event(OOM_KILL); memcg_memory_event_mm(…)` counter row; the `Tasks state … in
pages` row; and reading rules on config-conditional keys and double-counting `kernel` vs its sub-keys).
Neither draft is a superset; EntryA's was the more complete instrument for the C2 predicate as landed.

EntryB's quote-ambiguity finding is real but does not touch the landed bytes: in the normalised HTML
copy, the short span "All memory amounts are in bytes." occurs **3×** and "…ordered to be human
readable…" **2×**, while the landed entry's longer variants occur **exactly once** each (verified with
the counter's own `normalise()`). The predicate requires table-uniqueness, not copy-uniqueness — a named
limit, not a landed-data defect.

## 4. REUSED / DISCARDED

### REUSED (output → where it landed → re-verification)

| # | Output | Landed where | Re-verified by |
|---|---|---|---|
| R1 | EntryA Draft 1 entry (22 rows, front matter, Reading rules, Limits, Boundaries) | `corpus/knowledge/oom-memcg-stat-r50.md` (via salvage `9b8562a3`; data commit added nothing but the `## Claims` heading) | `count-c2.py 487941b9` → `C2=met claims=22 located=22 … pins=ok provenance=ok` (ran, rc 0); `pins=ok` re-hashes copies; `live-sha-L1.txt` re-fetches all three URLs identical |
| R2 | EntryA Draft 2 rows S489–S491 (9/11 cells each) | `corpus/SOURCES.md:268-270` (integration vehicle `assimilation/a2/append-block.md`) | `count-c2.py 487941b9` → `source_rows=ok sources=3` (ran); census at HEAD `rc=0` incl. `W04 S491` (ran); `mirror-validate.txt` rc 0 |
| R3 | RowMemcontrol's S004-vs-S490 scope analysis | Landed S490 scope clause "; not the master-commit path labels of S004" | same as R2 |
| R4 | RowOomKill's W04-not-E04 analysis and anchor-cell style | Landed S491 scope "; same URL as S003 and S476 with a different scope"; "copy … sha256 …" in all three landed anchors | census at HEAD: `W04 S491 … across scopes`, `mori ok`, rc 0 (ran) — exactly its predicted 22nd W04 |
| R5 | RowOomKill / RowMemcontrol E11 coupling warning ("integrate entry and rows together") | honored: rows landed in `487941b9` after the entry existed (salvage `9b8562a3`); no E11 at HEAD | census rc 0; `mirror-validate.txt` rc 0 |
| R6 | EntryA/RowMemcontrol/RowOomKill live-fetch byte-identity claims | L1 re-ran all three fetches | `assimilation/a2/live-sha-L1.txt` (2026-10-26T09:26-03:00, sha256 `2d716cb7…`, `8a28e0bc…`, `452f1348…` — all identical to frozen pins) |
| R7 | Scout finding "S489–S491 rows must be appended after S488" | rows at `SOURCES.md:268-270` | row position verified by read; `source_rows=ok` |
| R8 | EntryB row-cell style (scope exclusions; copy+sha256 anchors) | the rewritten scope/anchor cells of all three landed rows | textual match only [INFERENCE]; contents re-verified via R2 |

### DISCARDED (output → reason)

| # | Output | Reason |
|---|---|---|
| D1 | EntryB's 21-row entry draft (and its key/units table, decision table, "what this changes" section) | Alternate draft; the contract needs exactly one entry. EntryA's 22-row draft was already validated end-to-end, and it covers three rows EntryB lacks (swap line, pre-signal counter increment, Tasks-state pages). No factual defect in EntryB found. Its fixture claim (rev de9e912f) is UNVERIFIED (scratch deleted). |
| D2 | EntryB's proposed S489–S491 rows (teaches cells: bytes-vs-counts, oom_kill broad-vs-local, CONSTRAINT_MEMCG split) | teaches cells differed from EntryA's; EntryA's teaches landed. Row mechanics were identical, so nothing was lost that the landed rows don't already carry. |
| D3 | RowMemcontrol's S490 row draft (scope "the memcg OOM report block only…", per-function anchor 1791-1830 etc.) | Superseded by EntryA's anchor style; its useful analysis survived as the S004 scope clause (R3). Its verbose anchor would also have been harder to re-verify at a glance. |
| D4 | RowOomKill's S491 row draft (anchor with ":1031 and :1075" call sites) | Superseded by EntryA's anchor style. Bonus: its "call sites" list was incomplete (third `dump_header` call at `oom_kill.c.v7.2:1158`), so discarding avoided landing an inaccuracy. |
| D5 | Scout's must-link list (7 entries) | Not landed: the entry carries no links section (grep = 0 hits). Presumably deferred to frontier-drafting seats this wave; the scout itself marked the tsukuroi pair "optional". |
| D6 | Scout's coverage-map "Round-50 coverage additions" block and FR1 append-only note | Not landed: `corpus/README.md`/`PROVINCE.md` unchanged `7197160b..HEAD`. Frontier/coverage integration appears deferred. |
| D7 | Scout's proposed "Boundaries: …" line | EntryA's own Boundaries section was landed instead; both carry the tsukuroi-delegation substance. |
| D8 | EntryB-unique claim rows: CONSTRAINT_MEMCG identification; memory.oom.group indivisible-workload doc row; memory_stats static-table grounding; per-item unit-conversion row | Not needed for the predicate (the landed table already draws on all three sources with 22 rows); the .local row was explicitly against the scout's boundary. Candidate depth additions for a later round's own claim — not this round's data. |
| D9 | EntryB's recheck: style (counter-based recheck) | EntryA's curl+sha256 recheck loop landed and was re-verified live (R6). |
| D10 | Staged r46/r47 candidates (tmpfs hypothesis, host-block composition numbers) | Rejected by both scribes and the contract (own-work notes, /tmp fixture, journalctl MESSAGE read, no table); nothing of them landed. |

## 5. Verification commands exercised (all read-only; cwd = lane root unless noted)

```
git log --oneline -8                                       # commit map (§1)
git log --follow -- corpus/knowledge/oom-memcg-stat-r50.md # entry first appears at 9b8562a3
git diff 9b8562a3 487941b9 -- corpus/knowledge/oom-memcg-stat-r50.md   # empty
git show --stat 487941b9 ; git show --stat 9b8562a3        # touched files (§1)
git diff 950e99be HEAD -- .ufo/waves/round-50/count-c1.py .ufo/waves/round-50/count-c2.py .ufo/waves/round-50/contract.md  # empty (frozen)
diff <EntryA Draft 1 extraction> <git show 487941b9:corpus/knowledge/oom-memcg-stat-r50.md>  # only "## Claims" hunk
python3 cell-level diff of entryA_rows.md / entryB_rows.md / landed_rows (SOURCES.md:268-270 @487941b9)  # 9/11 cells identical per row; scope+anchor synthesized
python3 .ufo/waves/round-50/count-c1.py 487941b9395e89678af0053cc443cdb49cdee6e3
  → C1=met items=8 axes=6 pins=2 boxes=4 mismatches=0 errors=0 hidden=0 manifest=a94551c5bc8d   rc=0
python3 .ufo/waves/round-50/count-c2.py 487941b9395e89678af0053cc443cdb49cdee6e3
  → C2=met claims=22 located=22 quote_missing=0 bad_rows=0 sources=3 source_rows=ok pins=ok provenance=ok   rc=0
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
  → 22 W04 lines incl. "mori W04 S491 duplicate url …/v7.2/mm/oom_kill.c across scopes"; "mori ok …/corpus/SOURCES.md"   rc=0
grep -nE 'oom-tracepoints-r47|oom-victim-context-r41|census-cgroup-levels-r45|kernel-oom-line-attribution-r12|oom-kill-counter-kernel-only-r12|oom-evidence-loss-r38|kill-oom-boundary-r33|oom-event-plane' corpus/knowledge/oom-memcg-stat-r50.md
  → no hits (scout links not landed)   rc=1
grep -n 'mem_cgroup_print_oom_meminfo\|^static void memory_stat_format\|^static void memcg_stat_format\|^int memory_stat_show\|mem_cgroup_print_oom_context' corpus/evidence/sources-r50/memcontrol.c.v7.2
  → 1693 / 1751 / 1770 / 1787(comment) / 1791(function) / 4905   rc=0
grep -n '__ratelimit\|dump_header(oc);\|Killed process %d' corpus/evidence/sources-r50/oom_kill.c.v7.2
  → 945 / 1030 / 1031 / 1075 / 1158   rc=0   (three dump_header call sites: 1031, 1075, 1158)
counter-normalise occurrence counts in corpus/evidence/sources-r50/cgroup-v2.7.2.html:
  "All memory amounts are in bytes." ×3; EntryA row-1 18-word variant ×1; "…ordered to be human readable…" ×2;
  "Don’t rely … fixed position; use the keys …!" ×2; EntryB 24-word variant ×1
cat .ufo/waves/round-50/assimilation/a2/{append-block.md,live-sha-L1.txt,mirror-validate.txt}
tail -3 .ufo/waves/round-50/evidence/selftests/mori-pin-check.txt      # PIN_CHECK_SELFTEST pass=114 fail=0
tail -3 .ufo/waves/round-50/evidence/selftests/mori-unlanded-check.txt # UNLANDED_SELFTEST pass=17 fail=0
```

Disk guard before the run: `/fast/scratch/hyaku` 24% used, 612.6 G free — no ENOSPC encountered.

## 6. Named limits (observed during this audit; reported as limits, not fix proposals)

- The C2 quote check requires table-uniqueness of a quote, **not** single occurrence inside the copy;
  short spans of the cgroup-v2 sentences occur 2–3× in the committed HTML. The landed rows happen to use
  the unique long variants (verified), so this limit does not bite the landed data. (Also flagged by
  EntryB in w1.)
- Quote location proves occurrence, not entailment (contract's own named limit; EntryB flagged two of
  its own rows for leaning on nearby code — e.g. `memory_stat_show` for the shared-formatter claim; the
  landed EntryA rows 11/12 quote both call sites directly, so the landed text does not carry that
  specific weakness).
- Cell authorship of the landed scope/anchor cells is attributed here by textual similarity
  ([INFERENCE] on R8); the L1 left no donor map. All landed cells pass the frozen checks regardless.
- EntryB's end-to-end fixture claim (`de9e912f…`, `C2=met claims=21`) is UNVERIFIED: the fixture lived
  only in its scratch directory, which the seat removed. The same counter now scores EntryA's bytes at
  the landed lane revision, so the claim's absence of proof has no bearing on the landed data.
- The C1 counter trusts the fleet MANIFEST (its own named limit); the SCORECARD/SHONEN corrections it
  verifies were attempt-2 L1 work, not salvaged w1 output — no w1 report claimed them.

## Findings

- **MED** — `corpus/knowledge/oom-memcg-stat-r50.md` (landed entry, row 20 and prose): the entry never
  names `CONSTRAINT_MEMCG` — the summary's constraint field is described as "records the constraint and
  nodemask" without the value that identifies a memcg OOM. EntryB's draft had this row; it was not
  landed. Detection value: the summary alone then identifies which report shape follows. (File:
  `corpus/knowledge/oom-memcg-stat-r50.md` row 20 / `## Reading rules`; source copy
  `corpus/evidence/sources-r50/oom_kill.c.v7.2` `oom_constraint_text` 239-244.)
- **MED** — `.ufo/waves/round-50/w1/Mo50ScoutCoverageFR1.md` §4/§5 (must-link list, coverage-map block,
  FR1 append note): none of these scout outputs is in the landed data (`corpus/README.md`, `PROVINCE.md`
  unchanged `7197160b..HEAD`; entry contains zero of the seven link targets — verified by grep). If the
  frontier-drafting seats of this wave do not pick them up, the round ships the C2 knowledge entry with
  no corpus-map linkage and no FR1 "what the kernel prints" half-advance note. Deferred, not refuted.
- **LOW** — `.ufo/waves/round-50/w1/Mo50ScribeRowOomKill.md` (draft S491 anchor): "call sites :1031 and
  :1075" is incomplete — a third `dump_header(oc)` call exists at `oom_kill.c.v7.2:1158`
  (out_of_memory "Found nothing?!?!" no-killable-processes path); 1075 is the `check_panic_on_oom` panic path. The
  draft was discarded and the landed S491 anchor carries no call sites, so no inaccuracy landed.
  (File: w1 report draft row; copy lines 1031/1075/1158.)
- **LOW** — `.ufo/waves/round-50/w1/Mo50ScribeEntryA.md` (Behaviour item 1 prose): cites
  `mem_cgroup_print_oom_meminfo` at "(:1787)" — 1787 is the doc-comment line; the function head is 1791.
  The landed S490 anchor "1787-1830" spans both, so the landed artifact is correct; the report prose is
  loose. (File: w1 report; copy lines 1787-1791.)
- **LOW** — `count-c2.py` quote check (named limit, shared with EntryB's w1 finding): copy-occurrence
  multiplicity is not constrained; short documentation spans occur 2–3× in the committed HTML copy
  (verified via the counter's own `normalise()`). Landed rows use the unique long variants.
- **INFO** — `corpus/SOURCES.md:268-270`: the three landed rows' scope/anchor cells are L1 syntheses
  matching no single draft verbatim (9/11 cells per row are EntryA's; the rewritten cells combine
  RowMemcontrol's S004 clause, RowOomKill's W04 clause, and the copy+sha256 anchor style of the row-seat
  drafts). All cells pass the frozen counter and the census at the landed tip.
- **INFO** — w1 salvage completeness: the salvage commit `9b8562a3` committed all five w1 reports, both
  C1 selftest receipts, and the entry; the attempt-2 data commit `487941b9` re-verified rather than
  re-invented (its message states receipts were re-verified; my own runs of both frozen counters at
  `487941b9` reproduce `C1=met` / `C2=met`). Nothing observed suggests an un-salvaged w1 output that the
  landed data silently depends on.
