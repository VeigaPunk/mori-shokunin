# SourceCensus — entering source registry count and append-only rules (round 16)

Seat: `MoriR16.SourceCensus` (leaf scout) · target `/home/vgpnk/Projects/shokunin/mori-shokunin`
Read-time (UTC): 2026-10-20T08:50:51Z → 08:52:42Z (local 05:50–05:52).
Entering revision: `b83edc6ee3db6822382ab673d7e6e984e420f22f` (the head recorded in
`.ufo/waves/round-16/sources-before.json`). Authority read: `/home/vgpnk/Projects/shokunin/CORPUS.md`
carries SOURCES contract v1 in full (`:64-149`) and supersedes the frozen
`.ufo/waves/kaika/SOURCES-CONTRACT-v1.md` as the reader-facing copy; `PROTOCOL.md:435` still names the
contract-v1 rules as append-only and the lane registry home.

Method: static Markdown/`git show` reads only — contract census commands (`CORPUS.md:131-149`), awk/grep,
`sha256sum`, `git show`/`git diff`. No gate, test, build, formatter, smoke, live `journalctl`, network
fetch, or further outside-lane write. **One `/tmp` staging write did occur and is disclosed in §6.**
No tool install/update. Writes: this report plus that staging file.

## 1. Entering committed census (HEAD `b83edc6`, pre-wave working tree)

| metric | value |
|---|---|
| rows | **38** (ids `S001`–`S038`, contiguous, no duplicates) |
| tier | **A=35 · B=2 · C=1** |
| status | **mined=17 · queued=20 · rejected=1** |
| tier × status | A/mined=17 · A/queued=18 · B/queued=2 · C/rejected=1 |
| kind | docs=16 · code=11 · tool=4 · spec=3 · community=2 · book=1 · own-work=1 |
| blob SHA-256 | `9e04a61b208f0751774ae4a3120fcaf4cff10c3ddeb8a6de520004ab2bda59df` (`git show HEAD:corpus/SOURCES.md`) |

Static contract checks on that blob (`CORPUS.md:131-149`):
malformed rows `NF!=13` = 0; duplicate ids = none; tier/status/kind enum violations = none;
`community` at tier A = none; mined rows with missing `used-by` paths = none; W03 (mined + `—`) = none;
E12 (row-shaped source outside `## Registry`) = none. `used-by` targets all resolve.

Wave receipt `.ufo/waves/round-16/sources-before.json`: argv
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`,
`exit_code: 0`, stdout ends `mori\tok\t…/corpus/SOURCES.md`, with exactly two warnings:
`W04 S035 duplicate url …/catalog/systemd.catalog.in across scopes` and
`W04 S037 duplicate url …/systemd.journal-fields.html across scopes`. W04 is warning-only under
`scripts/sources-census.sh:1-38`; exit 0 is consistent. Duplicate exact URLs: **S013↔S035** and
**S015↔S037** — distinct rows by scope, not duplicate ids.

## 2. Live working-tree delta observed during this seat's read (uncommitted, moving)

`corpus/SOURCES.md` changed three times while being read; any live count is a snapshot, not a final count.

| read time (UTC) | file SHA-256 | rows | tiers | statuses |
|---|---|---|---|---|
| 08:50:51 | `08c44af143fc0378122266ed647c2c5e58362603f51c2c2f44bf3f5a646b0522` | 39 | A36/B2/C1 | mined17/queued21/rejected1 |
| 08:51:48 | `44ade2132f53622d3f86164357d3ee238433ddab6f2ff75df7966567c3a3cde6` | 40 | A37/B2/C1 | mined19/queued20/rejected1 |
| 08:52:42 | `e097edf9b5563242fb902e7c460e16d3a18d3a8bd4a1201d23af948483e47a6e` | 40 | A37/B2/C1 | mined19/queued20/rejected1 |

Diff against HEAD at the last snapshot: table-row changes only on **S014, S015, S039, S040**; plus the
append-only correction block at `corpus/SOURCES.md:70` and Search-log bounded-search 7 text. No other
row cell changed; no status or recheck change (the +2 mined rows are the two new rows).

New rows (next unused ids; both `docs`/`A`/`mined`/`opened 2026-10-20`/`recheck on-release`,
`used-by corpus/knowledge/journal-cursor-window-r16.md`, `NF=13`):

| id | source URL | scope | lesson quote location |
|---|---|---|---|
| S039 | `https://www.freedesktop.org/software/systemd/man/latest/sd_journal_seek_cursor.html` | seek-to-cursor next-closest fallback | `corpus/lessons/round-16.md:68` (23-word quote, lesson-reported) |
| S040 | `https://www.freedesktop.org/software/systemd/man/latest/sd_journal_test_cursor.html` (served as `sd_journal_get_cursor`) | entry-identity test vs cursor-string comparison | `corpus/lessons/round-16.md:62` (12-word quote, lesson-reported) |

In-place `used-by` changes (only mutable cells touched; exact old→new, which the lesson reports in prose
at `corpus/lessons/round-16.md:79` but does not reproduce byte-for-byte):

- **S014** old = `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md, corpus/knowledge/journal-positive-evidence-r15.md`
  → new = same list + `, corpus/knowledge/journal-cursor-window-r16.md`.
- **S015** old = `corpus/knowledge/kill-classes-by-message-id-r12.md, corpus/knowledge/kernel-oom-line-attribution-r12.md, corpus/knowledge/structured-journal-scopes-r13.md, corpus/knowledge/journal-alarm-routing-r14.md, corpus/knowledge/journal-positive-evidence-r15.md`
  → new = same list + `, corpus/knowledge/journal-cursor-window-r16.md`.

`corpus/knowledge/journal-cursor-window-r16.md` exists (18,228 bytes, mtime 05:51 local), so the new
`used-by` path satisfies E11. Live static checks at `e097edf9…`: malformed=0, enum violations=none,
duplicate ids=none, `community`-at-A=none, W04 set unchanged (S013↔S035, S015↔S037).
The appended `SOURCES.md:70` correction is in `## Search log`, is labelled append-only, and explicitly
states immutable anchor cells were not edited — consistent with rule 2.

## 3. Registry append-only rules (authoritative text and scopes)

### 3.1 SOURCES registry (the append-only store)

Authority: `CORPUS.md:64-68` — contract v1 "(kaika, 2026-10-19, frozen), carried here in full …
A change is a new contract version, never an edit to this section." `PROTOCOL.md:435` names
`corpus/SOURCES.md` "append-only per the contract".

Shape and enums (`CORPUS.md:80-108`):
- One `## Registry` table, 11 columns (`:86`); `id` = `S` + ≥3 digits, **next unused, never reused**;
  no `|` inside any cell (`:89`).
- `kind` enum: spec · docs · paper · code · tool · dataset · talk · book · community · own-work (`:91`).
- `tier` is scoped to `scope`, never global; A primary/authoritative, B strong secondary, C lead only
  and never sole support; **`community` is never A** (`:93-97`).
- `anchor` = exact section/heading/page/line plus revision, never a bare homepage (`:99-100`).
- `teaches` = one grounded benefit; rejected rows read
  `REJECTED: <reason>; flip: <what would change the verdict>` (`:101-102`).
- `status`: `queued` (opened, worth mining) · `mined` (cited by ≥1 path in `used-by`) ·
  `rejected` (kept — a rejection is evidence of taste) (`:103-104`).
- `opened` ISO date; `recheck` ISO date or cadence (`90d`, `180d`, `on-release`) (`:105-106`);
  `used-by` repo-relative paths or `—` (`:107-108`).

Rules (`CORPUS.md:110-129`):
1. **A row is a claim** (`:112-115`) — write only after opening the source in the round that writes the
   row; the round lesson's `## Gate` records, for every new row, the URL, access date, and a ≤25-word
   quote with its location; non-author verification re-opens a sample.
2. **Append-only** (`:116-118`) — **only `status`, `recheck` and `used-by` change in place**, and each
   change is logged old→new in the round lesson. A correction is a **new row** whose `teaches` opens
   `supersedes S0NN —`. Every other cell (source, kind, tier, scope, anchor, teaches, opened) is
   immutable in practice; the contract makes no provision to rewrite them.
3. **No second method** (`:119-122`) — claim admission stays in `corpus/QUALITY.md`; research method
   stays chousa's; no duplication.
4. **Expansion is knowledge, not rows** (`:123-125`) — count admitted `knowledge/` entries citing a
   `mined` row; no row quota; a short honest registry beats a long one.
5. **Search log** (`:126-128`) — PRISMA-inspired: question/query, where, date, identified/screened/
   included/excluded, exclusion reasons, stop rationale; a negative claim carries its sweep.
6. **No credential material**, session/private URLs, or `op://` references (`:129`).

Validator (`scripts/sources-census.sh:1-38`, census commands `CORPUS.md:131-149`):
statuses are exactly `queued|mined|rejected` ("watch" is not a status), `community` never A.
Codes: E01 malformed `NF!=13`, E02 bad id, E03 duplicate id, E04 duplicate URL+scope without
supersede, E05 kind, E06 tier, E07 status, E08 opened, E09 recheck, E10 community-at-A, E11 missing
`used-by` path, E12 row-shaped source outside `## Registry`; W01–W04 are warnings and do not change
exit 0. Exits: 0 clean/warnings · 1 E/overdue · 2 usage/missing registry · 3 selftest failure.

### 3.2 Adjacent append-only stores (constrain round-16 edits elsewhere)

| store | rule | anchor |
|---|---|---|
| any append-only file | a falsified claim gets a **named correction entry in the lane's next round**, appended never rewritten; stays on the routed-defect queue until it lands | `PROTOCOL.md:366-367` |
| `LOG.md` | entries never rewritten or deleted; corrections are new entries | `PROTOCOL.md:463` |
| manifest `rounds` | append-only after closure; corrections are appended entries carrying supersede type/index | `PROTOCOL.md:314-318` |
| `PROTOCOL-APPENDIX.md` | rows are append-only dated incidents | `PROTOCOL.md:437` |
| `.ufo/l0-questions.md` | append-only; a correction appends a new line naming the superseded one | `PROTOCOL.md:524-526` |
| source contract itself | a change is a new contract version, never an edit | `CORPUS.md:64-68` |

Evidence-quality rules that gate registry edits: errata append-only (`corpus/QUALITY.md:6`, Q4);
a rejection is kept (`:7`, Q5); re-pin is a recorded act with a reason, never a way to turn red green
(`:19`, Q10); a verdict-producing gate carries its PROTOCOL §Gate registry row at the lane registry
home before results are cited (`:73`, Q31).

### 3.3 Gate registry (additive registration, not an append-only source store)

`PROTOCOL.md:398-421`: a child lane's registry home is its `SKILL.md`; row fields are name,
`gate|probe`, entry command, verdict map (code → class), self-test command/spelling, pinned-value path,
write scope, owner; closure grades no gate conformant until its row exists. Current rows at read time:
`SKILL.md:155-168` register `census`, `drift pin`, `silence oracle`, `r13 regressions`,
`r14 regressions`, `r15 regressions`. **No r16 regressions row exists at read time** — expected
mid-wave; owned by the harness/registry seats, not this one. This table is name-keyed additive
registration with retained prior rows; it is not the append-only SOURCES store.

## 4. Compliance observations at read time (advisory, no edit)

- **Observed:** new rows use the next unused ids `S039`/`S040`; both are additions, not rewrites; both
  have 11 columns (`NF=13`), valid enums, opened date, cadence, and an existing `used-by` path.
- **Observed:** the only in-place changes are `used-by` on S014/S015. `corpus/lessons/round-16.md:79`
  narrates each as "gained the same note" and names the new note; the exact old cell strings are in
  §2 above, not in the lesson. Rule 2 asks for old→new logging — prose-level match, not byte-exact.
  If L1 wants literal old→new, append it to the lesson; no SOURCES edit is needed.
- **Observed:** rule-1 evidence (URL, access date, ≤25-word quote) for the new rows lives in
  `## Source openings (this round)` (`corpus/lessons/round-16.md:49-79`) and the `## Gate` table
  (`:101`) references it; the quotes are not inside the literal `## Gate` section. Content requirement
  is met; strict section placement is an L1 judgment, not a rewrite this seat performs.
- **Observed:** `SOURCES.md:70` correction block is appended in `## Search log`, names the r15 used-by
  re-verification, and states immutable anchors were not edited — consistent with rule 2.
- **Observed:** W04 duplicate-URL warnings are unchanged (S013↔S035, S015↔S037); no resolution is
  possible by rewriting immutable cells, and no dedup action is claimed here.
- **Not observed / out of scope:** the old drift pin's red state and any re-pin. This seat did not read
  or run it; the registry diff contains no re-pin evidence. Q10 governs any re-pin (recorded act with a
  reason, never to turn red green), and the r16 context says no re-pin.

## 5. Remaining unknowns

1. **Final committed registry census is unknown to this seat.** The file moved three times in ~2 min
   (S039 queued→then S039+S040 mined, S014/S015 `used-by` appended). L1 must take the post-settle
   census from the committed bytes; §1 is the entering HEAD count and §2 is a timestamped snapshot.
2. **`sources-before.json` carries no counts.** Unlike `.ufo/waves/round-15/sources-before.json`
   (which persisted `counts` and a counting command), the r16 receipt has argv/exit/stdout/head only;
   §1 reconstructs the entering counts from the HEAD blob, not from the wave receipt.
3. **New-note citations unverified.** `corpus/knowledge/journal-cursor-window-r16.md` exists and is
   cited by both new rows; its internal citations were not verified here (the lesson seat also
   discloses it did not verify them).
4. **Quote word counts are lesson-reported** (23/12). This seat did not re-fetch the pages; no live
   network read was performed.
5. **W04 duplicate-URL rows** remain warning-only debt; no contract-conformant in-place fix exists
   because scope/anchor is immutable. A future new row must open `supersedes S0NN —` if a superseding
   scope is meant.

## 6. Disclosure (L1 IRC, 2026-10-20)

**Outside-lane write (corrected disclosure).** During the entering census this seat wrote
`/tmp/sc.tsv` — an interim static staging file, outside the lane — with this command (run from
`mori-shokunin`):

```sh
awk -F'|' '/^\| S[0-9]/{gsub(/^ +| +$/,"",$2); gsub(/^ +| +$/,"",$4); gsub(/^ +| +$/,"",$5); gsub(/^ +| +$/,"",$9); printf "%s\t%s\t%s\t%s\n",$2,$4,$5,$9}' corpus/SOURCES.md > /tmp/sc.tsv
```

Content: the 38 entering rows (`S001`–`S038`) as four tab-separated fields (id, kind, tier, status)
parsed from `corpus/SOURCES.md`; no journal data, no probe/measurement data, no download. The same
command read it back with `cut`/`sort`/`uniq`/`awk` for the first counts; every count cited in this
report was re-derived directly from the in-lane file and the HEAD blob afterward. Under
`corpus/QUALITY.md:23` (#23) a `/tmp` path is never evidence, so no result here rests on that file.
Per the L1 IRC, existence/removal was **not** checked by a new command and will not be.
This outside-lane write occurred before the L1 no-`/tmp` clarification was delivered to this seat;
it is recorded here as required, and no further outside-lane write occurred.

Exact harness evidence supplied by AttackPermission via L1 and visible in this transcript: bash tool
call **`call_00_23e6o0JRRbZbn9u7CAvC8732`**, message `46b262e9`, `2026-10-20T08:49:38.989Z`, transcript
line 35; its tool result (line 39) reported `ROWS 38` / `A35 B2 C1` /
`mined17 queued20 rejected1`, which matches the independently re-derived entering census in §1.
The staging file remains non-evidence (QUALITY #23); no rerun or existence check was performed.

**Backgrounded static command.** One static command (`grep`/`sha256sum`/awk reads of
`corpus/SOURCES.md` and `SKILL.md`) was harness-backgrounded when the L1 clarification arrived
(`bg_2758`); it completed, was acknowledged, and contained no live `journalctl` query, test, gate,
build, formatter, smoke run, `/tmp` output, network fetch, or outside-lane write. No live probe
occurred this seat. No result in this report depends on a probe or measurement.

Confidence: §1–§3 observed, statically reproduced, and line-anchored. §4 low-risk inference about
intent/placement, marked advisory. §5 explicitly unknown.
