# Mo49ScribeReadme — corpus/README.md additions for round 49

Seat: wave w1, lane mori-shokunin (leaf; no subagents). Assignment: draft, inside this report, the
`corpus/README.md` additions — a `## Round-49 coverage additions` block in the house shape of
`## Round-48 coverage additions`, one coverage-map row for `corpus/knowledge/journal-reach-r49.md` with its
FR1/FR11 ground, the sweep as the proof the ground was not held, the boundary, and the Frontier note as a
dated SUPERSEDING sentence.

Nothing in `corpus/` was edited: the drafts below are fenced and the L1 integrates them.

## Read and measured

- Frozen contract: `.ufo/waves/round-49/contract.md` (C2 claim, `P-C2`, named limits; entered at
  `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86`, freeze `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`).
- House shape: `corpus/README.md:657-675` (the whole `## Round-48 coverage additions` block, read raw: lead
  prose, `| Ground | Entry | Bounded advance |` table, `Count:` + `Sweep:` line, dated Frontier note). Also read
  the earlier Frontier-note forms at `corpus/README.md:499-563` (round 25 "byte-unchanged" statement, round 31,
  round 34) and the `## Frontier` table rows FR1 and FR11 at `corpus/README.md:337-354`.
- Frozen counter: `.ufo/waves/round-49/count-c2.py` — output line built at `:188-191`
  (`C2=%s claims=%d located=%d quote_missing=%d bad_rows=%d sources=%d source_rows=%s pins=%s provenance=%s rev=%s`
  plus ` failed=…`), so the `Count:` line below quotes that shape and not a guessed one.
- Receipts: `evidence/selftest-c2.txt` → `C2_SELFTEST pass=26 fail=0`; `evidence/control-c2-donothing.txt` →
  `C2=unmet … failed=entry_absent,pins`; `evidence/sweep-journal-rows.txt`; `evidence/freeze-sha256.txt`.
- Entry ground (prose facts below): the four committed copies `corpus/evidence/sources-r49/*` (journald.conf(5),
  journalctl(1), systemd-journald.service(8), host receipt), normalised through the counter's own
  `normalise()` (imported with `PYTHONDONTWRITEBYTECODE=1`, so no `__pycache__` was written into the frozen
  directory).

Date of this report: 2026-10-25 (local), after the lane tip it cites.

## Evidence for each statement in the draft

| Draft statement | Evidence observed here |
|---|---|
| FR11 ground is exact-retained/same-boot and does not prove the journal lost nothing | `corpus/knowledge/journal-cursor-window-r16.md:11` ("supports FR11 only as an exact-retained, same-boot, read-only window … does not … prove that the journal lost nothing between the anchor and the end of the window") |
| the vacuumed-file "no retained record" class predates this entry | `corpus/knowledge/journal-alarm-routing-r14.md:166` (`` | Processes outside manager observation, inaccessible journal, vacuumed files | none | No retained record | ``) and `:176` ("**No retained record** — … or vacuumed. Nothing can be counted, and absence is not evidence of zero events.") |
| the three retention knobs were 0 in both surfaces at `b3e3453d` | re-measured read-only: `git show b3e3453d:corpus/SOURCES.md \| grep -cE 'SystemMaxUse\|MaxRetentionSec\|RuntimeMaxUse'` → `0` (rc 1); `git grep -hE 'SystemMaxUse\|MaxRetentionSec\|RuntimeMaxUse' b3e3453d -- corpus/knowledge \| wc -l` → `0` (rc 0). Per-pattern counts and the command line are in `evidence/sweep-journal-rows.txt` (committed at the freeze: `git ls-tree -r 0df17b7b \| grep round-49/evidence` lists it) |
| no `SOURCES.md` row named the `journald.conf` page | `git show b3e3453d:corpus/SOURCES.md \| grep -c 'journald\.conf'` → `0` (rc 1); sweep file records `journald\.conf SOURCES.md=0 knowledge=1` |
| the lane held the `--disk-usage` total and the vacuum wording already | `knowledge/journal-disk-usage-total-r51.md` (S470); `git show b3e3453d:corpus/SOURCES.md \| grep -c 'vacuum'` is part of the sweep (`vacuum SOURCES.md=3 knowledge=12`), i.e. the word was held, the retention rule was not |
| S351 is rejected and its flip names the two halves | `corpus/SOURCES.md:248` — `REJECTED: … flip: the public --vacuum-size= sentence plus a committed read-only disk-usage receipt, and no MESSAGE grep` |
| persistent `/var/log/journal` vs volatile `/run/log/journal`, `Storage=` fallback | normalised journald.conf(5) copy, `Options`/`Storage=` (the sibling quote inventory `w1/Mo49ExecQuotesConf.md` Q1/Q2/Q5/Q6 locates these spans; I re-found the same text through `normalise()`) |
| eight `System*`/`Runtime*` size options; `MaxRetentionSec=` default 0 turns time deletion off; `MaxFileSec=` rotates | same copy, anchors `#SystemMaxUse=` / `#MaxRetentionSec=` / `#MaxFileSec=`; page text found through `normalise()` at idx 11482, 12597 (size-based deletion/rotation, archived-only, post-vacuum overage) |
| `--vacuum-size=` / `--vacuum-time=` delete **archived** files only | normalised journalctl(1) copy idx 25818: "`--vacuum-size=` removes the oldest archived journal files until the disk space they use falls below the specified size"; "`--vacuum-time=` removes archived journal files older than the specified timespan" |
| host ceilings 256M / 64M and the drop-in | `corpus/evidence/sources-r49/host-journal-reach.txt:69-76` (`[Journal] SystemMaxUse=256M RuntimeMaxUse=64M` in `/etc/systemd/journald.conf.d/size.conf`, 46 bytes, mtime 2026-10-16); the receipt's own disk-usage totals (`56M`, `19M`, `37M`) are at `:4-14` and the two retained boots at `:89-92` |
| the four copies are the frozen ones | `sha256sum` on all four equals `count-c2.COPIES` pins and `evidence/freeze-sha256.txt`: journald.conf.5 `b4a9b53e…`, journalctl.1 `75440570…`, systemd-journald.service.8 `a7b44356…`, host-journal-reach.txt `be3952cb…` |

I did not read the two entry drafts (`Mo49ScribeEntryA`, `Mo49ScribeEntryB`); the block below describes the
entry only at the level the frozen contract fixes and cites only what the four copies say.

## Draft — append to the end of `corpus/README.md` (after line 675)

```markdown
## Round-49 coverage additions

FR1 and FR11 ground the map held only as boundaries: `knowledge/journal-cursor-window-r16.md` accepts a window only
as exact-retained and same-boot and states it does not prove the journal lost nothing, and
`knowledge/journal-alarm-routing-r14.md:166,176` puts vacuumed files in the "no retained record" class — but no lane
document said what sets how far back the retained set reaches. Round 49 adds the **journal retention rule and this
host's effective reach**: `Storage=` and the `/var/log/journal` (persistent) versus `/run/log/journal` (volatile,
in-memory) split, the eight `System*`/`Runtime*` size options with `MaxRetentionSec=` defaulting to 0 (time-based
deletion off) and `MaxFileSec=` rotation, `--vacuum-size=`/`--vacuum-time=` deleting archived files only with a
post-vacuum total that can still exceed the ceiling, and this host's own drop-in ceilings from a read-only receipt. The lane's
earlier refusal of this theme, `S351` (`journalctl(1)`, rejected round 43), flips here: the new `S486` row's
`teaches` opens `supersedes S351 —` and S351 stays a rejected row.

| Ground | Entry | Bounded advance |
|---|---|---|
| FR1 event-time attribution (evidence reach) · FR11 cursor window (retention boundary) | `knowledge/journal-reach-r49.md` | how far back the journal evidence mori reads can reach is documented from four sources (journald.conf(5) S485, journalctl(1) S486, systemd-journald.service(8) S487, this host's 2026-10-25 read-only receipt S488): which journal (`/var/log/journal` versus `/run/log/journal`), the day of the reading, the size ceilings and the `MaxRetentionSec=` default of 0, archived-file-only deletion and its post-vacuum overage, and the host's `SystemMaxUse=256M`/`RuntimeMaxUse=64M` drop-in; read-only — no vacuum, rotate or journald change was run; reach context only, no vacuum or rotate advice, and journald configuration belongs to tsukuroi |

Count: N claim rows — `python3 .ufo/waves/round-49/count-c2.py <rev>` → `C2=met claims=N located=N
quote_missing=0 bad_rows=0 sources=S source_rows=ok pins=ok provenance=ok` (`C2_SELFTEST pass=26 fail=0`).
Sweep: the ground was not held — `SystemMaxUse`, `MaxRetentionSec` and `RuntimeMaxUse` each occur 0 times in
`corpus/SOURCES.md` and 0 times in `corpus/knowledge/` at `b3e3453d`, and no `SOURCES.md` row names the
`journald.conf` page (`.ufo/waves/round-49/evidence/sweep-journal-rows.txt`); what the lane held was the
`--disk-usage` total (`knowledge/journal-disk-usage-total-r51.md`, S470) and the vacuumed-file alarm class.

FR1 / FR11 Frontier note, dated, appended (the FR1 and FR11 rows above are not rewritten): **round 49
(2026-10-25) supersedes the absence of a retention rule for the journal evidence mori reads — the rule that sets
the reach is documented in `knowledge/journal-reach-r49.md` (S485–S488), so a count or a missing record is read as
bounded by what is still retained; still frontier: no cursor was run across a rotation or a vacuum, no per-boot
share is claimed beyond the `--disk-usage` total, and fleet attribution is untouched. Reach context only: the
entry gives no vacuum or rotate advice, and journald configuration belongs to tsukuroi.**
```

## Optional — top `## Coverage map` row (L1 decides)

Round 45 added a top-map row for its entry and its C3 counter required one
(`.ufo/waves/round-45/count-c3.py:16,204`); rounds 47 and 48 added none (the map's last row is
`knowledge/census-cgroup-levels-r45.md` at `corpus/README.md:50`). If the integrator wants the map complete,
insert after line 50, before the blank line and `## Known gaps`:

```markdown
| `knowledge/journal-reach-r49.md` | how far back the journal evidence mori reads can reach: the retention rule (size ceilings, `MaxRetentionSec=` default 0, archived-only deletion and its post-vacuum overage), the persistent `/var/log/journal` versus volatile `/run/log/journal` split, and this host's effective ceilings on 2026-10-25 — reach context, not a count correction; no vacuum or rotate advice, journald configuration belongs to tsukuroi | S485, S486, S487, S488; `corpus/evidence/sources-r49/host-journal-reach.txt` |
```

## Integration slots (must be substituted, not guessed)

1. `claims=N` / `located=N` — the landed run's values; `count-c2.py` prints them itself. The floor is 8
   (contract `P-C2`), the entry drafts are told to carry 10 or more.
2. `sources=S` — the number of **distinct** sources the quote table actually draws on (`count-c2.py:188`
   counts distinct sources used, not cited rows); it can be 3 or 4. Do not paste `4` without the run.
3. `<rev>` — the landed tip.
4. If the entry lands with a different S-id mapping than S485 journald.conf(5) / S486 journalctl(1) /
   S487 systemd-journald.service(8) / S488 host receipt (the w1 spec and the sibling row reports use this
   mapping), the row's source list and the Frontier note's `(S485–S488)` must follow the registry, not this
   report.
5. The host numbers `SystemMaxUse=256M` / `RuntimeMaxUse=64M` are the receipt's own readings; if the entry
   does not adopt them, drop them from the row rather than leave the row citing a number the entry does not carry.

## What I did not do

- Did not edit `corpus/README.md`, `SKILL.md`, `SOURCES.md`, `corpus/knowledge/`, `corpus/lessons/`, `tools/`,
  `LOG.md`, `SCORECARD.md`, `QUALITY.md`, or any frozen round-49 file (contract, both counters, `controls/`,
  `evidence/`, committed source copies). The only lane write is this report.
- Did not run `count-c2.py` against the repo: the entry is not landed and the pins arm would read `bad` by
  construction (the copies are not at the entering revision — `evidence/control-c2-donothing.txt`), so a run would
  add no information. `C2=met` is **UNVERIFIED** here by design; the claim's gate is the L1's landed run.
- Did not read the entry drafts of `Mo49ScribeEntryA`/`Mo49ScribeEntryB`, so no sentence here rests on their
  wording; the row and the note are phrased from the frozen contract and the four copies.
- Did not run any host journal read beyond reading the committed receipt; no `journalctl`, no `--vacuum*`, no
  `systemctl`, no config change. No pacman, no tool install or upgrade (nothing was needed).
- No git index, jj, or fleet-repo mutation; read-only `git show`/`git grep`/`git rev-parse`/`git ls-tree` only.
  `/home/vgpnk/Projects/shokuknow` not read this seat.

## Files changed

- `.ufo/waves/round-49/w1/Mo49ScribeReadme.md` (this report).
- Scratch created and left empty: `.scratch/r49-Mo49ScribeReadme/` (used as `TMPDIR` for the two
  `normalise()` reads; no files written).

## Findings

- **MED** `corpus/evidence/sources-r49/host-journal-reach.txt:95-97` — the S488 receipt reads the runtime/system
  ceilings through `journalctl -b 0 -u systemd-journald --no-pager -q -g 'Journal .* is .*max'`, and `-g` is
  defined in the committed journalctl(1) copy (normalised idx 14508) as "Filter output to entries where the
  MESSAGE= field matches the specified regular expression." `corpus/SOURCES.md:248` (S351) states the flip as
  "the public --vacuum-size= sentence plus a committed read-only disk-usage receipt, **and no MESSAGE grep**".
  The `8M, max 64M` / `45M, max 256M` readings the receipt offers are MESSAGE-derived. This is a conflict between
  the frozen flip text and the committed receipt; reported, not resolved by me (canonical judge).
- **LOW** `corpus/evidence/sources-r49/host-journal-reach.txt:96-97` — journald's lines print the host name
  (`HOSTNAME`, present in the receipt) even though the journal path is redacted to `MACHINE_ID`; a report quoting them verbatim carries a
  host name (not credential material, but avoidable). My draft quotes neither line.
- **LOW** `corpus/README.md` / `evidence/sweep-journal-rows.txt` — the sweep records `journald\.conf
  SOURCES.md=0 knowledge=1`; the single `knowledge/` occurrence is
  `corpus/knowledge/structured-journal-scopes-r13.md:19` (a pointer: `--user` "only works if persistent logging is
  enabled, via the Storage= setting in journald.conf(5)"). The "ground not held" claim is therefore safe for the
  three retention knobs and for the `SOURCES.md` registry, but a sentence saying the page is unmentioned anywhere
  in `corpus/knowledge/` would be false; the draft avoids it.
- **LOW** `.ufo/waves/round-49/count-c2.py:188-190` — `sources=` counts distinct sources quoted, not rows cited,
  so a four-row-sourced entry can print `sources=3`. The `Count:` line must take `S` from the landed run; pasting
  `sources=4` from the row list would misquote the counter.
- **LOW** `corpus/README.md:50` — the top `## Coverage map` table ends at the round-45 entry while rounds 47-48
  added no top-map row; adding an r49 row is a precedent choice (round 45's counter did require one). Offered as
  an optional block above rather than folded into the required additions.
- **LOW** `corpus/README.md:499-563` (existing notes, not this round's) — earlier Frontier notes cite
  `corpus/README.md:332-345` for the FR table, which has since moved (`## Frontier` is at `:337` today). The r49
  note cites FR ids, not line numbers, so it does not add to that drift.
- **LOW** `.ufo/waves/round-49/count-c2.py` + `.ufo/waves/round-49/` — importing the counter as a library writes
  `__pycache__` into the frozen directory unless `PYTHONDONTWRITEBYTECODE=1` is set; my reads used it and the
  directory was not touched (round-end cleanup should still sweep `.ufo/waves/round-49/__pycache__/`).
