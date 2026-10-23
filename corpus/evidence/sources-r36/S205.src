# Shokunin Corpus Contract

Every shokunin repo carries a proprietary corpus — knowledge about its domain
*and* training lessons about itself. It is the shokunin's memory; it must never
contain generic filler.

## Layout (per child repo)

```
corpus/
  README.md        — index: what's here, coverage map, known gaps, frontier
  QUALITY.md       — the shokunin's own quality bar (LEARNING.md)
  SOURCES.md       — where it learns: opened sources, tiers, rejections (below)
  knowledge/       — domain facts, sourced notes, decision records
  lessons/         — training lessons: what worked/failed this round and why
```

Each `knowledge/` entry opens with `source:`, `verified-at:` and `recheck:`;
each `lessons/round-<N>.md` carries a `## Gate` section (candidates,
admitted, rejected with reasons, spot-check result). See `LEARNING.md`.

## Rules

- `knowledge/` entries cite a source: file path, command output, or URL.
- `lessons/` entries cite the round and the evidence (LOG.md round, commit, report).
- A corpus entry is falsifiable or marked opinion; no unverifiable claims.
- The aggregator reviews every corpus each round and files gaps as lessons.

## Rules added from the round-1/2 corpus audits

Evidence: the per-repo `corpus/lessons/round-1-aggregator-audit.md` entries and
`.ufo/reports/round-2/AGGREGATE.md`.

- **A count carries its command.** Any number in a corpus entry (rows, files,
  lines, packages) is written as `<number> — <command> <date>`. Round-1 found
  four unreproducible counts: "275 claim packages" (observed 274 program dirs /
  295 package dirs / 281 `status.json`), "20-row registry" (observed 21),
  "~40 clones" (observed 50), "scripts/ 74 entries" (observed 82).
- **A negative claim carries its sweep.** "No counterexample", "nothing
  handles X", "absent everywhere" need the search command that produced the
  absence, or the claim is unverifiable.
- **A quote names its location.** Frontmatter vs body, header comment vs code,
  script vs installed skill. Round-1 defects: an anti-trigger quoted as
  frontmatter that lives in a body table; a `128`-lane cap attributed to an
  installed skill that contains no `128`.
- **An index row is a claim.** Write the row when the file exists, not before.
  A seeded index naming seven entries while one existed is worse than a
  one-row index.
- **No credential material, ever.** Secret values, session tokens, cookies, and
  vault ref paths (`op://…`) stay out of every corpus, including this one's
  examples. Cite the file path, the mode, and the mechanism; a reader with
  authority can regenerate the metadata.
- **Corrections are new entries, never rewrites.** Lanes own
  `lessons/round-<N>.md`; the aggregator writes only
  `lessons/round-<N>-aggregator-*.md` and does not edit lane-authored corpus
  files in place (same append-only discipline `PROTOCOL.md` gives `LOG.md`).
  This rule exists because of a real collision: aggregator and kagi lane both
  wrote `kagi-shokunin/corpus/lessons/round-1.md` in the same minute
  (2026-09-28 15:56); the lane's committed version was restored and the
  aggregator's moved to `round-1-aggregator-seed.md`.
- **Each round's review emits a verdict per repo** — `conformant` or
  `not conformant`, naming the failed rule and the command that shows it.

## SOURCES.md — where a shokunin learns

Contract v1 (kaika, 2026-10-19, frozen), carried here in full from
`.ufo/waves/kaika/SOURCES-CONTRACT-v1.md`. A change is a new contract version,
never an edit to this section.

Where a shokunin learns. `corpus/knowledge/` holds admitted facts; `corpus/SOURCES.md`
holds the places they come from — what each teaches, how far to trust it for which
scope, and when to look again. It is the lane's curated reading list and the standing
record of its taste. Inputs: `kaika-w1/art-curation.md` (curation and grading practice),
`kaika-w1/critic.md` (H4–H6 gates).

### Shape

```
# SOURCES — where <id> learns
## Registry           the one table below
## Paths              ordered study sequences: `<topic> — S003 → S010 → S014: why this order`
## Search log         one prose note per bounded search (rule 5)
## Leads (unopened)   bullets; a lead is not evidence and never a row
```

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|

- `id` — `S` + 3 or more digits, the next unused; never reused. No `|` inside any cell.
- `source` — title — canonical URL or DOI (a repo path or command for `own-work`).
- `kind` — `spec` · `docs` · `paper` · `code` · `tool` · `dataset` · `talk` · `book` ·
  `community` · `own-work`.
- `tier` — scoped to `scope`, never global. **A**: primary or authoritative for that scope
  (spec, official docs, source code, original paper, maintainer statement, the lane's own
  re-runnable gate output). **B**: strong secondary (expert write-up with reproducible
  detail, survey, textbook). **C**: lead only — never sole support for an admitted entry.
  `community` is never A. Tier is curation, not truth: no NATO/GRADE labels on rows.
- `scope` — the claim or topic the tier applies to.
- `anchor` — exact section / heading / page / line plus revision (version, commit, or
  publication date). Never a bare homepage.
- `teaches` — one grounded learner benefit. Rejected rows read
  `REJECTED: <reason>; flip: <what would change the verdict>`.
- `status` — `queued` (opened, worth mining) · `mined` (cited by ≥1 path in `used-by`) ·
  `rejected` (kept — a rejection is evidence of taste).
- `opened` — ISO date the row's author opened the source. `recheck` — ISO date or cadence
  (`90d`, `180d`, `on-release`).
- `used-by` — repo-relative paths of the knowledge entries or lessons citing the row,
  comma-separated, or `—`.

### Rules

1. **A row is a claim.** Write it only after opening the source in the round that writes
   the row. The round lesson's `## Gate` records, for every new row, the URL, the access
   date, and a ≤25-word quote with its location grounding `teaches`. Non-author
   verification re-opens a sample.
2. **Append-only.** Only `status`, `recheck` and `used-by` change in place, and each change
   is logged old→new in the round lesson. A correction is a new row whose `teaches` opens
   `supersedes S0NN —`.
3. **No second method.** Claim admission stays in `corpus/QUALITY.md`; the research method
   stays chousa's (`chousa-shokunin/SKILL.md`: question → source hierarchy → citation
   chain → claim-vs-source check). `SOURCES.md` duplicates neither; `QUALITY.md` points
   here for tier definitions.
4. **Expansion is knowledge, not rows.** The expansion trend counts admitted `knowledge/`
   entries whose `source:` cites a `mined` row on uncovered coverage-map ground. There is
   no row quota; a short registry of opened, honestly tiered rows beats a long one.
5. **Search log.** PRISMA-inspired, not PRISMA-compliant: question/query, where searched,
   date, identified / screened / included / excluded counts, exclusion reasons, stop
   rationale. A negative claim carries its sweep.
6. **No credential material**, session or private URLs, or `op://` references — ever.

### Census — run from the lane root (tested 2026-10-19 on a synthetic table)

```sh
# rows (spacing-tolerant)
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
# malformed rows — 11 columns means NF=13; must print 0
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
# tier histogram
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
# status histogram
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
# duplicate ids — must print nothing
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
# enum violations and tier inflation — must print nothing
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md
# mined rows whose used-by paths do not exist — must print nothing
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
```

### Maintained parser note (outside frozen v1)

The maintained `scripts/sources-census.sh` CLI accepts 0–3 leading ASCII spaces before
Markdown table rows and headings; 4 or more spaces are indented code and are ignored.
The frozen manual census examples above assume column-zero input and remain unchanged.
Default discovery covers child repositories only: `repo=.` main-repo lanes hold no corpus.

## Rules added from the kaika campaign

Evidence: `.ufo/waves/kaika-w1/mistakes.md` (fleet mistake taxonomy, §5 lesson
proposals, §8 commands), `.ufo/waves/kaika-w1/art-curation.md`,
`.ufo/waves/kaika-w1/critic.md`, and the frozen contract above.

- **A new knowledge entry opens with its provenance trio.** `source:`,
  `verified-at:` and `recheck:` come first; when the source is external,
  `source:` cites its `S###` row in `corpus/SOURCES.md` alongside the URL and
  anchor. Provenance in prose or HTML comments is unreadable to a freshness
  sweep (`mistakes.md` §6 item 4). From the fleet root, 2026-10-19:
  683 knowledge files — `find */corpus/knowledge -type f -name '*.md' | wc -l`;
  312 carry `recheck:` —
  `grep -rlE '^[-* ]*recheck *:' --include='*.md' */corpus/knowledge | wc -l`.
- **A round lesson that mines mistakes carries `## Mistakes`.** One row per
  mistake: class · evidence pointer · captured-by (the `QUALITY.md` criterion or
  protocol rule that should have caught it, or `none`) · fix. Classes come from
  the `mistakes.md` §5 vocabulary (`vacuous`, `survivor`, `stale-premise`,
  `reference-drift`, `number-drift`, `scope`, `attribution`, `landing`,
  `provider`). Prose-only lessons did not hold: C01, C02, C07 and C10 recurred
  after capture (`mistakes.md` §5), and lanes without a `## Gate` section had
  nowhere to keep a rejection (M089).
- **A fix is shown able to fail before it counts.** A claimed repair ships one
  red-before state in which the same command exits non-clean for the named
  reason, with the fix as the only delta; the observed failure text is
  committed. Rejected exemplars: before/after trees that split identically
  (M027), a probe that mutates nothing (M029), a comparison that accepts an
  empty prior (M030) — `mistakes.md` §5 L1.
