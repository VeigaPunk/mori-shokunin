# Mo53ScribeProvince — PROVINCE.md after round 53 (commit ledger Core, v7.3 recheck freshness)

Seat: `Mo53ScribeProvince` (scribe). Lane: `mori-shokunin`. Scratch: `/fast/scratch/hyaku/mori-r53/Mo53ScribeProvince/`
(created, used only as `$TMPDIR` staging, removed at exit; no clone, no fixture, no heavy run — disk guard not needed).
No subagent. No host write. No git/jj mutation in the lane or the fleet root: every git call below is
`git log` / `git show --stat` / `git rev-parse`-class read-only.

## Decision

**A change is needed: one appended section at EOF.** `PROVINCE.md` is 400 lines and its last modification is
`af42101d` (round-30, 2026-10-22, `git log --format='%h %ci %s' -5 -- PROVINCE.md`). Rounds 31–52 appended
nothing. Two things in round 53 are not representable in the current text:

1. The commit ledger read (`tools/mori-commit-runway.py`) is a read-only probe of a quantity the file's ownership
   sentence does not name: `PROVINCE.md:10` says “resource runway (disk on the fleet root and `/tmp`, memory
   pressure)”, and the Core row at `:26` bounds runway to the `SURFACE disk` and `SURFACE cgroup` **census**
   reads. VM commit accounting is neither disk use nor pressure, and the census reads neither
   `CommitLimit` nor `Committed_AS` (`grep -c 'CommitLimit\|Committed_AS' tools/mori-census.sh` → `0`). Left
   unrecorded, a sibling reading the ownership sentence would place the overcommit ledger outside mori.
2. The v7.3 recheck is **freshness work on existing surfaces** — it adds no probe, no frontier row and no
   ownership change, so the accurate record is a note that says exactly that, next to the round-51/52 entries it
   re-reads (which `PROVINCE.md` does not otherwise index).

The minimal mechanism is the round-24/round-25 precedent: one appended `## Round-53 …` section carrying a Core
bullet, an owns-scope extension note (`PROVINCE.md:6-10` left byte-unchanged) and the boundary sentence. The
append sits after line 400, so **no line moves** and every existing line citation into the file
(`PROVINCE.md:6-10`, `:22-28`, `:26`, `:44-57`, `:386-400`, sibling citations) stays valid.

Rejected alternative — **no change**: defensible only if the Core/head lists are read as a closed ownership map
(the round-30 block at `:396-400` explicitly declares them non-exhaustive and names sixteen unnamed `tools/`
files as still open). Under that reading the runway class already covers “resource runway” in the abstract. I do
not take it, because the gap is not exhaustiveness but a *kind* of quantity: nothing in the file says mori reads
`/proc/meminfo` commit accounting, while the same file is the boundary document tsukuroi and the operator read
(`PROVINCE.md:12-16`). Recording it costs four bullets and moves no pointer.

## Grounds read (all at lane tip `95cf78ee`, data commit `2a4213bf`)

| path | lines read | what it grounded |
|---|---|---|
| `PROVINCE.md` | `:1-32`, `:295-400` (full file earlier) | Owns `:6-10`, Core head `:20-28`, runway row `:26`, Frontier head `:42-57`, round-30 block `:386-400` |
| `.ufo/waves/round-53/contract.md` | full | C1/C2 target text, verdict/exit-code interface, named limits (shared author of REF and tool; band is a bound; no cgroup commit) |
| `tools/mori-commit-runway.py` | `:1-60` (module docstring) | schema, fields, verdicts/exits, mode-0/1/2 semantics, band formula, `COMMIT_UNKNOWN`, selftest contract |
| `corpus/knowledge/commit-runway-read-r53.md` | full | band claims S511–S513, reading-rules table, Boundaries (v7.2 bytes, operator owns mode/ratio/reserve, os triage tsukuroi) |
| `corpus/knowledge/kernel-v7.3-recheck-r53.md` | `:1-45`, `:45-60`, `:81-84`, `:90-111` | S502–S510, 46/49 scope, nine-file diff table, ledger dispositions, Boundaries (host 7.2.11; not rechecked list) |
| `SKILL.md` | `:1178-1208` | `## Round53` decision table, release-recheck rule, registry row (23 cases, verdict map) |
| `.ufo/waves/round-53/evidence/c1-at-data.txt`, `c2-at-data.txt` | full | L1 receipts (read, **not** re-run by this seat) |

## Observed evidence (command → output, exit)

```
$ wc -l PROVINCE.md
400 PROVINCE.md
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin log --format='%h %ci %s' -5 -- PROVINCE.md
af42101d 2026-10-22 18:23:50 -0300 round-30: routed R7 — PROVINCE stale statements fixed by same-line substitution plus appended correction block; …
ac696ad3 2026-10-22 15:57:40 -0300 round-28: wave-2 corrections …
…                                                    (exit 0)
$ grep -n 'CommitLimit\|Committed_AS\|overcommit\|commit-runway\|recheck\|v7\.2\|v7\.3' PROVINCE.md
26:- **Resource runway** — `SURFACE disk` and `SURFACE cgroup`: …        (only other hits: :255 "v7.2 PSI" prose, :289 "fleet resource runway" prose)
$ grep -c 'CommitLimit\|Committed_AS' tools/mori-census.sh
0
$ git show --stat 2a4213bf | head -12
 7 files changed, 1470 insertions(+), 1 deletion(-)   (SKILL.md, SOURCES.md, 2 knowledge entries, tool 316 lines, cases.json 754 lines, c1-claims.txt)
```

Ledger tally, recomputed from the committed entry bytes (`awk -F'|'` over the ledger table):

```
rows=46  status[held]=44  status[absent]=2  disposition[holds]=46
absent rows: 0fbd62f51ce8, d7a1dc88dcb3 — both `overcommit-commit-limit-r52.md`, source S510 (`mm/mmap.c` v7.3)
```

L1 receipt text (read, not reproduced):

```
C1=unmet scope=46 rows=46 matched=46 status_ok=46 quote_ok=46 source_rows=ok pins=ok provenance=ok held=44 absent=2
     holds=46 changed=0 voted=0 dissent=0 rev=2a4213bf… failed=votes            exit=1
C2=met tool=present selftest=pass n=23 fixtures=80 agree=80 disagree=0 registry=ok live=ok rev=2a4213bf… exit=0
```

The C1 line is the pre-vote state (`voted=0`, `failed=votes`), i.e. the data commit before any wave seat scored;
the draft therefore records the dispositions as provisional and claims no admission.

## Draft — minimal PROVINCE.md change (append at EOF, after line 400)

```markdown
## Round-53 appended scope notes (2026-10-26)

- **Core, commit-ledger runway read (`tools/mori-commit-runway.py`; round-53 C2):** reads `CommitLimit`,
  `Committed_AS`, `MemTotal`, `SwapTotal` (optional `Hugetlb`) from `/proc/meminfo`, the five commit knobs under
  `/proc/sys/vm`, and `/sys/devices/system/cpu/present`, and prints one JSON object (`schema:
  mori-commit-runway-v1`): `verdict`, `mode`, `enforced`, `commit_limit_kb`, `committed_as_kb`, `headroom_kb`,
  `reserve_kb`, `usable_kb`, `band_kb`, `batch_pages`, `cpus_present`, `single_request_cap_kb`,
  `limit_recomputed_kb`, `limit_consistent`. Verdicts `COMMIT_OK`, `COMMIT_HEURISTIC`, `COMMIT_UNLIMITED`
  (exit 0), `COMMIT_LOW` (exit 1), `COMMIT_UNKNOWN` (exit 2). The mode decides what the numbers are: under
  `overcommit_memory` 0 the two lines are printed but never compared, so `Committed_AS` above `CommitLimit` is
  normal (`over_limit_not_enforced`) and only a single request larger than RAM + swap is refused
  (`single_request_cap_kb`); under 1 the commit test always passes and the read says nothing about memory left
  (read `MemAvailable`); under 2 the limit is enforced, `usable_kb = CommitLimit - Committed_AS -
  admin_reserve_kbytes - user_reserve_kbytes` (the user reserve at its worst case), and `COMMIT_LOW` means the
  room is inside the per-CPU counter's own error band (`band_kb = batch x present CPUs x page`, batch
  `max(min(ram pages / CPUs / 256, INT_MAX), max(2 x CPUs, 32))`), where a non-root allocation may already be
  refused while the printed numbers still show room. `COMMIT_UNKNOWN` means this tool cannot derive a number
  from the bytes it was pointed at — never zero room, never a pass. `COMMIT_LOW` is **not** a calibrated alarm
  (FR8 stays open), and `band_kb` is an upper bound from the batch rule with today's totalram and present CPUs,
  not a measured deviation. Read-only: seven files opened for reading (`/proc/meminfo`, five `/proc/sys/vm`
  knobs, `/sys/devices/system/cpu/present`); it writes no sysctl, chooses no mode, ratio or reserve, triggers no
  allocation and reads no cgroup commit (there is none). It is **not a census surface**: no `SURFACE` row, no
  census finding id, no DRIFT verdict, no baseline re-pin — `tools/mori-census.sh` names neither line. Limits
  carried with the row: the counter's reference reading and the tool share one author, so a shared misreading of
  `mm/util.c` passes both (independent recomputation is the wave's job), and the live leg compares stable fields
  only and turns on the host it runs on. Knowledge: `corpus/knowledge/commit-runway-read-r53.md` (S499,
  S511-S513, v7.2); SKILL registry `## Round53`.
- **Freshness work on existing surfaces, no scope change (round-53 C1):**
  `corpus/knowledge/kernel-v7.3-recheck-r53.md` re-reads the 46 claim rows of `memavailable-estimate-r51.md` and
  `overcommit-commit-limit-r52.md` that cite a v7.2 file (three further rows cite the 2014 commit patch, which no
  release changes) against the same paths at tag v7.3 (`refs/tags/v7.3^{}` → `c03c1a14507d`); S502-S510 are
  those nine files at v7.3, with pinned copies under `corpus/evidence/sources-r53/`. 44 of the 46 quotes still
  occur; the two `mm/mmap.c` `MAP_NORESERVE` quotes are respelled as `vma_flags_set(&vma_flags,
  VMA_NORESERVE_BIT)` for the same condition, so their status is `absent` and their disposition still `holds`. A
  `held` status proves only that the words still occur somewhere in the v7.3 file — not at the same place and
  not with the same meaning; the row's `disposition` carries the reading and remains the L1's provisional one
  until two voting seats that wrote neither the row nor its quote carry it. The two round-51/52 entries remain
  the host's reading: this ledger says what a v7.3 host would read, and the host's kernel line was 7.2.11 when
  it landed (entry Boundaries). Not rechecked: `oom-tracepoints-r47.md`, the round-50 memcg entry
  (`recheck: 90d`), prose outside the two tables, and the anchors of S492-S501. No probe, no frontier row, no
  ownership change.
- **Owns-scope extension (append-only; `PROVINCE.md:6-10` left byte-unchanged):** the first Core bullet above
  extends the owned read-only probe list named at `PROVINCE.md:6-10` — which today reads "resource runway (disk
  on the fleet root and `/tmp`, memory pressure)" — with VM commit accounting under the overcommit mode, a
  quantity that is neither disk use nor pressure. The `## Core` head (`PROVINCE.md:22-28`, whose Resource runway
  row at `:26` names only the `SURFACE disk` and `SURFACE cgroup` census reads) and the `## Frontier` head
  (`:44-57`) are not rewritten and gain no row; this section is appended at EOF, so no line moves and every
  existing line citation into this file stays valid.
- **Boundaries:** choosing `vm.overcommit_memory`, `overcommit_ratio`, `overcommit_kbytes`,
  `admin_reserve_kbytes` or `user_reserve_kbytes`, and deciding whether a commit refusal is a host fault, belong
  to the operator and tsukuroi; the lane reports the reading it made and no remediation. This note claims no
  admission: both claims are scored by the round-53 counters, and no census integration, threshold, baseline
  re-pin or frontier closure is added.
```

## Pointer and byte hygiene of the draft

- **Insertion point:** end of file, after line 400 (blank line between the round-30 block and the new heading,
  matching the spacing before `## Round-30 …` at `:386`). Nothing above is edited; `:6-16`, `:20-28`, `:26`,
  `:42-57`, `:92-400` stay byte-identical. Zero line moves → the lane's line citations into `PROVINCE.md`
  (`:6-10` in this file and in `PROVINCE.md:120-121`, `:296-297`; `:22-28` and `:44-57` at `:396-399`; sibling
  citations `../kumitate-shokunin/PROVINCE.md` lines unaffected) all still resolve.
- **Head lists:** deliberately not rewritten — the round-30 block already declares them non-exhaustive
  (`:396-400`), and rewriting `:20-28` toward “eight bullets” without also backfilling rounds 31–52 would make
  the count wrong in a new way.
- **Numbers carried:** only byte-derived ones (`46` rows, `44 held` / `2 absent`, `holds=46`, the tag
  `c03c1a14507d`, `S502-S510`, `S499`, `S511-S513`). No counter receipt line, no score, no admission word.
- **No host value is asserted:** the note names no overcommit mode, ratio, CPU count or MemTotal for this host.
  The tool reads the mode; the mode is the operator's configuration. The single host fact quoted — kernel line
  7.2.11 — is attributed to the entry's own Boundaries as an as-read value at entry time, not a standing
  configuration claim.
- **ASCII:** the draft uses `-`, `x` and `->` instead of `−`, `×`, `→` so it survives the lane's text
  conventions unchanged if pasted verbatim.

## Deliberate non-claims

- No admission, no “verified”, no vote count, no dissent: the wave has not scored at the time of writing, and
  C1's receipt at the data commit reads `voted=0 … failed=votes`.
- No census integration, no `SURFACE` row, no DRIFT id, no baseline re-pin (grounded: `tools/mori-census.sh`
  has 0 hits for both field names).
- No host configuration, no tsukuroi triage, no remediation, no threshold (FR8 stays open per the entry).
- No independently re-run counter: the `C1=` / `C2=` lines above are quoted from the L1 receipts at `2a4213bf`
  and are not this seat's measurement.
- The draft does not close, add or renumber a frontier row, and does not touch `SKILL.md`, `SHONEN.md`,
  `SCORECARD.md`, `LOG.md`, `corpus/` or `tools/`.

## Findings

1. **MED — `PROVINCE.md:386-400` (round-30 block) and the whole file: 22 rounds of unrecorded surface growth.**
   `PROVINCE.md`'s last commit is `af42101d` (round-30); rounds 31–52 appended nothing, and of the 35 files in
   `tools/` 21 are unnamed here — including resource-runway-adjacent ones (`mori-disk-rate.py`, round 34) and
   policy instruments (`mori-source-drift.py`, `mori-gate-registry.py`, `mori-sources-appendonly.py`). The
   round-30 block names sixteen unnamed tools as “still open”; the backlog has grown since. This draft appends a
   round-53 section and **does not** attempt the backfill — route it to round 54 as a documentation-freshness
   item, not as a defect of round 53.
2. **MED — `PROVINCE.md:10` and `PROVINCE.md:26`: the runway ownership sentence does not name commit
   accounting.** Owns says disk + memory pressure; Core `:26` names only the two census surfaces. A sibling or
   the operator reading the file cannot tell that mori reads `/proc/meminfo` commit fields and the five
   `/proc/sys/vm` commit knobs, and the overcommit mode is exactly the kind of host configuration tsukuroi and
   the operator will reach for. The draft's Core bullet plus owns-scope note closes this; the head sentences
   stay byte-unchanged by design.
3. **MED — contract C2 target line vs landed fixtures (wording, not result).** The contract's target line reads
   `n≥12` while the landed fixture file holds 23 cases and the counter prints `n=23 fixtures=80 agree=80`;
   `SKILL.md:1208` records `PASS 23/23`. A reader of the contract alone could believe a 12-case arm cleared the
   claim. No gate changes (counter frozen); this is a reportable wording item for the L1 and a round-54
   candidate for the contract template.
4. **LOW — `corpus/knowledge/kernel-v7.3-recheck-r53.md:81,84`: `absent` status with `holds` disposition is the
   most misreadable row shape in the ledger.** Two rows read “status `absent`” and “disposition `holds`”
   simultaneously (the two `MAP_NORESERVE` respellings). The draft states the distinction explicitly; a future
   reader skimming a status column could report two claims as changed. Wording item, no data error.
5. **LOW — `PROVINCE.md:386-400` precedent tension.** Rounds 31–52 verifier closures recorded `PROVINCE.md`
   untouched as adjacency-neutral (`corpus/lessons/round-42-verifier-spotcheck.md:87`,
   `round-47-verifier-spotcheck.md:70`, `round-48-verifier-spotcheck.md:63,72`). The round-53 append is
   consistent with r24–r27 practice, not with r31–r52 practice; the L1 should expect a reviewer to ask which
   convention holds. My reading: the closures recorded *no harm from leaving it alone*, not a rule against
   recording new ownership — but that reading is `[INFERENCE]` from the closure texts, not a stated convention.
6. **LOW (carried, not discovered) — shared author of REF and tool.** The contract's own named limit
   (`contract.md`, C2 named limits) means a shared kernel misreading passes both the reference and the tool; the
   fixture arm cannot fail on it this round. Not fixable under the frozen counter; route to round 54 as an
   independence item.
7. **LOW — `corpus/knowledge/kernel-v7.3-recheck-r53.md` Boundaries: the new v7.3 `panic_on_unrecoverable_memory_failure`
   key is recorded as a lead for the kill-event frontier, not a claim.** No PROVINCE change proposed (the Core
   kill/OOM row at `:23` is mechanism-neutral and the key is not read by any mori probe); noting it so the lead
   is not silently dropped at the round boundary.
8. **LOW — scratch discipline.** One stray `/tmp/x` (a `grep -c` tool-name list, well under 50 MB) was written by
   this seat and removed in the same session; it carried no bytes cited here and is not evidence. Scratch dir
   `/fast/scratch/hyaku/mori-r53/Mo53ScribeProvince/` was removed at exit, after the draft above was copied into
   this report. No pacman transaction, no install, no network fetch.
