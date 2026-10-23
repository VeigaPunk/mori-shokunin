# Round 33 w1 — sibling-overlap scan (ConnectorSiblings)

Seat: `MoriR33.ConnectorSiblings`, leaf, read-only. Lane repo `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Method: `timeout`-capped `grep -rn` over the sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin`
(not mori) plus the fleet-root `.ufo/` for the terms in the dispatch: `diskstats`, `iostat`, `io_ticks`,
`disk write rate`, `sectors`, `block/stat.rst`, `block/genhd.c`, `part_stat.h`, `sysstat`, plus the
judge-rule-drift class (`loosen`, `judge rule`, `frozen rule`, `rule it applied`). No URL was opened; no
tool installed or updated; no scratch file needed. Every claim below is a path:line in a committed file or
a command with its output.

Note on one grep false positive: the pattern `iostat` also matches the host name `biostat.mcgill.ca` inside
kengaku's statistics rows; those hits are not disk sources.

## 1. Overlaps (lane, path:line, what it claims)

### 1.1 Disk write-rate / diskstats reading — no sibling holds a reading table
- tsukuroi `.ufo/waves/round-26/w1/ConnSiblingOverlap.md:22` — a prior connector recorded that mori's census
  picks its write-average device from the `df` source and matches the kernel name in `/proc/diskstats`
  (`mori-shokunin/tools/mori-census.sh:1872-1886`).
- tsukuroi `.ufo/waves/round-26/w1/ConnSiblingOverlap.md:88` — the same seat recorded that the kernel name for
  the same `/tmp` partition changed between boots (one boot `nvme0n1p1`, the next `nvme1n1p1`) and prepared a
  packet for mori with state "prepared", explicitly not reported. This finding was never delivered.
- tsukuroi `.ufo/waves/round-26/w2/RevProvinceReadme.md:52` — the reviewer's inference: mori's device lookup
  would now find the second NVMe partition in `/proc/diskstats`, so its `/tmp` row would report a write average
  on an NVMe partition rather than a reason string. Not executed against mori's census.
- kama `.ufo/waves/round-16/falsify/advice/ConnectMoriFootprint.md:53` — mori's census reads `diskstats`,
  `uptime`, `meminfo`, `boot_id` (`mori-census.sh:298-300,328`). Consumption of the file, no reading rule.
- fleet-root `.ufo/waves/kaika-w1/mori-state.md:276` — the deferral this round's FR6 descends from: F6
  "Instantaneous write rate, a measured deferral (D11)"; `:289` lists
  `docs.kernel.org/admin-guide/iostats.html`: `/proc/diskstats` among the lane's unopened leads.

### 1.2 The iostats document and the sysstat package — where the facts already live
- mori `corpus/SOURCES.md:39` (row S033) already holds the URL
  `https://docs.kernel.org/admin-guide/iostats.html`, and its teaches cell already claims the two facts the
  C1 table most needs (sector-counter identity for field 7, and the need for boot/reset context before a rate).
  The row is `queued`, used-by `—`, never mined. So this URL is NOT new for round 33.
- No sibling lane holds that URL. The only `docs.kernel.org` row in tsukuroi's registry is
  `tsukuroi-shokunin/corpus/SOURCES.md:63` (S063, `admin-guide/mm/zswap.html`), a different page.
- tsukuroi `corpus/knowledge/kill-event-deep-r8.md:368` — holds the host fact that the sysstat binary is
  installed and the sa-log directory is empty; it names the package and version (`sysstat-12.8.0-1`) and cites
  its own capture file. tsukuroi `corpus/knowledge/boot-chain-r17.md:196` carries the same package inside a
  named package list (its own B:59 capture).
- Conclusion: the installed-sysstat fact is tsukuroi's; a mori C1 row on the `iostat(1)` page may state the
  reading semantics only, and must not restate the host's installed version as its own.

### 1.3 Storage-integrity frontier — adjacent, different surface
- tsukuroi `PROVINCE.md:154-175` — the round-26 frontier: btrfs per-device error counters, scrub records and
  NVMe SMART/Health lifetime fields; detection and report only; repair, running a scrub, resetting a counter
  and firmware updates stay operator-owned. Entry: `corpus/knowledge/storage-health-r26.md` (rows SH1–SH6) with
  `storage-health-r26.json`.
- tsukuroi `corpus/knowledge/degraded-triage-r4.md:193` and `corpus/knowledge/driver-firmware-plane.md:164` —
  optical-drive sector geometry, unrelated to a rate reading.
- No sibling file states a rule for reading `/proc/diskstats` or `/sys/block/<dev>/stat` as a write rate.
  Verified by two fleet-wide greps (md/py, mori excluded) whose only sibling hits are the four files above.

### 1.4 The C1 table itself
No sibling lane holds it, in any form: no decision table, no verdict rule, no reading rule for a disk write
rate in any sibling `corpus/knowledge`, `corpus/SOURCES.md` or non-scratch `.ufo` file. The nearest sibling
artifact is tsukuroi's `storage-health-r26.md`, whose measures are error counters, scrub state and SMART
lifetime fields — a different question (integrity vs rate).

Completed negative scan (this seat, 2026-10-22): `grep -rl -E 'diskstats|iostats\.html|io_ticks|block/stat\.rst|part_stat\.h'`
over all 20 sibling lane repos, `*.md|*.json|*.py|*.txt`, scratch excluded, ran 40.74 s to exit 0 and returned
exactly three files — the three cited in §1.1. The string `iostats.html` appears in no sibling lane; the
`docs.kernel.org/admin-guide/iostats.html` URL is mori's S033 alone.

## 2. Contested scope — disk observability vs tuning

- tsukuroi `PROVINCE.md:165-166` first wrote that disk-space runway and free-capacity reporting "remain mori's",
  and `:176-177` appends a correction: that overstates the split. The split is now stated by question — free
  space as fleet runway is mori's, free space as an upgrade or boot precondition is tsukuroi's.
- tsukuroi `PROVINCE.md:177` also records the coverage gap: the storage-integrity reads need privilege and
  "cover only the root's backing NVMe device; the second NVMe device (`/tmp`, `/fast`) is unread."
  mori's own live row keys the write average on `dm-0` (`corpus/knowledge/surfaces-r8.md:75-89`), i.e. a
  device-mapper name, not either NVMe device.
- Neither lane currently owns "read /proc/diskstats for a given device and report a rate". mori's
  `PROVINCE.md:49` declares FR6 with the boundary that the since-boot average stays a different measure, and
  `SKILL.md:401` states the census measures a write rate only as the average since boot. So FR6 is mori's,
  and the C1 entry is the first reading rule; no sibling contest there.
- One live collision risk: NVMe SMART "Data Units Written" is a lifetime counter a rate can be derived from,
  and tsukuroi already owns the NVMe SMART lifetime reads (`storage-health-r26.md`, rows SH1–SH6). A C1 row
  that treats NVMe SMART as a write-rate source would enter tsukuroi's surface; a row that stays inside
  `/proc/diskstats` and `/sys/block/<dev>/stat` does not.

## 3. The round-32 judge-rule-drift class — three sibling criteria already landed

Class definition (mori's own, `corpus/lessons/round-32-verifier-spotcheck.md:186`): a judge applied a looser
rule than its dispatch instruction, and the receipt did not name the rule it applied. Sibling lanes hold
landed criteria for the same class:

- kumitate `corpus/QUALITY.md:329-347` — Q25, a mutation battery has one kill predicate, frozen before any
  counted run and stated identically in plan, code and case names; its arm (5) reads, quote
  `` `kumitate-shokunin/corpus/QUALITY.md:346-347` (30 words): "Nothing about the predicate changes after any seat or L1 has run the counter; a post-data change is an appended correction, and the counter is reported under the frozen text." ``
  and its fails-when arm at `:360-361` names the case: "the predicate is edited after data and the round is
  scored under the edit".
- kake `corpus/QUALITY.md:866` arm (b) — a counter version bump preserves the declared predicate; a bump changes
  no target, threshold, cap, pin or predicate unless a scored control forced that exact change and the round's
  note names the control, its score and the reason; it rejects an unexplained change in any of those values or a
  post-measurement change not remeasured against the declared bound. Grounded in kake's round-35 routed defect 2
  (`corpus/lessons/round-35-verifier-spotcheck.md:190`, lesson row `corpus/lessons/round-36.md:100`).
- kaidoku `corpus/QUALITY.md:54` (criterion 44) — a claim presented as a test of a rule is declared and frozen
  before the L1 sees any data that answers it, by any route; the frozen test set excludes every item the lane
  already holds a response for; otherwise the result is called a re-observation, not a held-out test.
- Mirror precedent (the acceptable direction): kaidoku `corpus/lessons/round-19-verifier-spotcheck.md:103` — an
  amendment that restates the frozen rule, with an empty diff against the operative rule file, is status-neutral.
- mori's own state: `corpus/QUALITY.md:683-689` (criterion 95) already binds a judge receipt to the sha256 of the
  judged bytes; `:50` (criterion 25) covers silent narrowing of a claim's scope; the highest criterion is 96.
  No mori criterion covers a change to the rule itself after data, and none requires a receipt to name the rule
  it applied. The routed repair (round-32 item 2) asks only for the disclosure half.

## 4. The move (one, bounded)

**Axes named.** (A1) C1 depth — a new entry whose every decision-table row survives rule R-J. (A2) Repair
fidelity — the round-32 routed items under R-R, item 2 above all. (A3) Source identity — S180+ rows must be
genuinely new URLs. (A4) Judgment integrity — the frozen rule is the one applied, after data as before it.

**Proposed move.** Land one mori QUALITY row (97) with two arms, and no other change:
(a) a judge receipt names the rule it applied — the frozen rule text, or a sha256 of that rule block — in the
same receipt that already names the sha256 of the judged bytes under criterion 95; (b) nothing about the rule
or predicate changes after any seat or the L1 has run the counter, and a post-data change is an appended
correction with the round scored under the frozen text. Cite the three sibling criteria above as precedent by
path:line, and mori's own routed defect at `corpus/lessons/round-32-verifier-spotcheck.md:186`.

**Why it is non-obvious.** The routed repair as written is a paperwork fix ("a future judge receipt must name
the rule it applied"). The sibling lanes show the class needs the immutability arm too (kumitate `:347`), and
mori's own criterion 95 shows the binding mechanism (hash the judged artifact). The synthesis is to hash the
rule, not only the bytes — one new row, no counter edit, no contract change. It is checkable with mori's
existing frozen counter, whose bytes are already pinned: the C1 counter
`.ufo/waves/round-33/count-c1-a1.py` never changes, so arm (b) has a mechanical test.

**Second-order effects.**
- Contract: none. R-J and P-C1-A1 keep their word-for-word text; the counter stays untouched (the assignment
  forbids changing it), so both arms are enforced through receipts and the lesson, not through the counter.
- Runtime/substrate: no harness, MCP, unit or `/etc` file is touched; nothing is tuned.
- Sibling substrate: tsukuroi's own criteria require a sibling citation to carry a pinned blob and a quote
  (`tsukuroi-shokunin/corpus/QUALITY.md:137`, criterion 69) and treat a quote found at another line as DRIFTED
  and handed to the owner, never repaired in the sibling (`:58`). So the three citations must carry lane
  commit, blob digest and the quote, or the row itself becomes a drift-class defect.
- A1/A3: unchanged and, per §1.2, constrained — see risks.

**Risks.**
1. Post-data row. A QUALITY row landed after data exists and then used to score the same round is the very
   class being repaired (kaidoku 44's principle). The row must land in wave 1, before any judge seat runs, and
   the round lesson must name the commit that landed it. If it cannot land that early, it must not be used to
   score round 33 at all.
2. S033 collision. mori already holds the iostats URL (§1.2), so C1 rows cannot rest on it. A tag-pinned raw
   copy of the same document (`https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/iostats.rst`)
   is a new URL but the same document; whether a judge reads that as "new source" is not settled by the frozen
   text, which counts by URL. State the relation to S033 in the registry's teaches cell as declared lane
   doctrine rather than smoothing it.
3. Host-measured facts cannot support a row. mori's own r8 evidence records that a 0.2 s two-sample probe read
   0 sectors in 3 of 5 reps, and that the probe costs 4.16× the latency budget
   (`corpus/knowledge/surfaces-r8.md:75-89`). No kernel-doc quote states this, so under R-J a row whose reading
   cell asserts short-window noise on this host is unsupported; that fact must live in the entry's prose or the
   lesson, never in a reading cell.
4. Device identity. The cross-boot name change recorded at tsukuroi
   `.ufo/waves/round-26/w1/ConnSiblingOverlap.md:88` means a rate keyed by kernel name is not carried across
   boots by anything the kernel doc states. A row asserting cross-boot continuity would fail R-J; the table's
   verdict rule should instead make the reading carry its device name and its boot.

**Verification the L1 can run.**
- `git diff <freeze-commit> <tip> -- .ufo/waves/round-33/count-c1-a1.py` is empty (arm (b)'s mechanical test).
- Each round-33 judge receipt carries a rule identifier beside its judged-bytes sha256 (arm (a)); the L1 can
  grep the receipts for both fields.
- The three sibling citations resolve: `sed -n '347p' kumitate-shokunin/corpus/QUALITY.md`,
  `sed -n '866p' kake-shokunin/corpus/QUALITY.md`, `sed -n '54p' kaidoku-shokunin/corpus/QUALITY.md`.
- `grep -n 'iostats' mori-shokunin/corpus/SOURCES.md` returns S033 only, before and after the round.

## 5. Contradictions stated, not smoothed

- URL-newness vs document-newness (§4 risk 2) — the frozen text counts by URL, the judge reads by document.
  Both readings are defensible; the lane should pick one in writing and say so in the registry cell.
- FR6's purpose vs R-J's support rule (risk 3) — the round wants a usable rate reading; the host's measured
  noise, which is the reason the instantaneous rate was deferred, cannot be stated by any external source.
  The table can be fully supported and still not justify a rate implementation; those are two different results
  and the report should not merge them.
- mori's own QUALITY 25 covers silent narrowing of a claim, not post-data editing of the rule that judges it
  (`corpus/QUALITY.md:50`). Round 31's M2 (`corpus/lessons/round-31.md:27`) and round 32's routed defect 2 are
  both instances of the uncovered half; the proposed row is the first criterion that names it.

## 6. Conformance

Read-only throughout: `timeout`-capped greps and `read`; no URL fetched, no source opened, no scratch file, no
git or jj write, no process left running, no package installed (so no tool/version/channel entry is owed).
This report is the only file written, at the path the `Report:` trailer names.
