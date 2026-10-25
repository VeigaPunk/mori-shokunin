# Wave-2 seat ScribeSourcesSection — 'Sources & frontier' section draft

Seat: ScribeSourcesSection (leaf scribe, no subagents). Scope: the report's Sources & frontier
section. All commands ran read-only from `/home/vgpnk/Projects/shokunin/mori-shokunin` with
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ScribeSourcesSection`
(never /tmp). Nothing was mutated; the only file written is this report. Entering tip E =
`2d85e33d14198d388fd3cda9cc15ec07e57e7a53`; landed tip T = `68d66ca53d89be5c34a62f46af7c37449d9f9b63`;
freeze F = `63eecf2738db96f46b0bd02b1b2dfd66787493d0`.

## 1. Counting command (C2, E vs T)

Frozen instrument bytes: worktree `sha256sum .ufo/waves/round-47/count-c2.py` =
`fc77b93338b3f49b9038eaac3832537b1be2e0ff9dff2476fef750153978901e`; `git show F:.ufo/waves/round-47/count-c2.py | sha256sum` = same — worktree equals freeze, so the worktree command measures the claim's rule.

- At E: `python3 .ufo/waves/round-47/count-c2.py 2d85e33d14198d388fd3cda9cc15ec07e57e7a53`
  → `C2=unmet events=0 rows=0 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=4 source_row=bad provenance=bad rev=2d85e33d14198d388fd3cda9cc15ec07e57e7a53 failed=entry_absent,pins,source_row`, exit 1.
- At T: `python3 .ufo/waves/round-47/count-c2.py 68d66ca53d89be5c34a62f46af7c37449d9f9b63`
  → `C2=met events=8 rows=8 name_mismatch=0 field_mismatch=0 callsite_mismatch=0 pin_mismatch=0 source_row=ok provenance=ok rev=68d66ca53d89be5c34a62f46af7c37449d9f9b63`, exit 0.
- Receipt `evidence/after-c2.txt` measured at `af2250d80033ded23ec34af328068eeb85007d1c`:
  `C2=met events=8 rows=8 … source_row=ok provenance=ok rev=af2250d8…`. `git diff --stat af2250d8 T -- corpus/knowledge/oom-tracepoints-r47.md corpus/SOURCES.md corpus/evidence/sources-r47 .ufo/waves/round-47/count-c2.py` is empty; only the receipt file itself differs (added at T), so the tree at af2250d8 equals T for every measured file. Claim C2's before→after holds.

## 2. SOURCES rows before → after (E vs T)

Extracted with `git show E:corpus/SOURCES.md` / `git show T:corpus/SOURCES.md` into scratch; counted with
`awk -F'|' '/^[ ]{0,3}\| S[0-9]{3,} \|/ {print $N}'` on the registry section.

| metric | E (`2d85e33d`) | T (`68d66ca5`) | delta |
|---|---|---|---|
| rows | 247 | 251 | +4 |
| tier A | 216 | 220 | +4 |
| tier B | 14 | 14 | 0 |
| tier C | 17 | 17 | 0 |
| status mined | 196 | 201 | +5 |
| status queued | 25 | 24 | −1 |
| status rejected | 26 | 26 | 0 |

Cross-check: `scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin mori` at T prints
`mori rows 251; tier.A 220 tier.B 14 tier.C 17; status.mined 201 status.queued 24 status.rejected 26`
and `FLEET … tier.invalid 0 status.invalid 0 missing 0`, exit 0 — matches the awk counts.

Rows added (ids present at T, absent at E; `comm -13` of id lists): exactly **S475, S476, S477, S478**,
all tier A, all `mined`:

- S475 — Linux `include/trace/events/oom.h` @ v7.2 (code/A); used-by `corpus/knowledge/oom-tracepoints-r47.md`.
- S476 — Linux `mm/oom_kill.c`, `mm/page_alloc.c`, `fs/proc/base.c` @ v7.2 (code/A); used-by the entry.
- S477 — own-work host tracefs oom events receipt (own-work/A); used-by the entry.
- S478 — ROMA full text (paper/A); used-by the entry.

Rows touched old → new: exactly one — **S005**: `status` `queued` → `mined`, `used-by` `—` →
`corpus/knowledge/oom-tracepoints-r47.md` (per `git diff E T -- corpus/SOURCES.md`; no other cell of any
row changed). The re-open evidence `w1/ExecS005Status.md` and the S475 anchor agree: the committed v7.2
copy `corpus/evidence/sources-r47/include_trace_events_oom.h` sha256 `82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d`; `grep -c '^TRACE_EVENT('` → 8.

## 3. Frontier rows advanced (FR13)

`corpus/README.md` Frontier table row FR13 is unchanged at T (line 353): "eBPF kill/OOM tracing |
`SOURCES.md:11-12,23-26` | Privilege and version matter; a resident tracer is outside the census, so
retain this as knowledge/frontier only." The landing adds a new `## Round-47 coverage additions` section
(README.md:646-655, absent at E): FR13's ground was only the peer-reviewed abstract
(`knowledge/oom-victim-context-r41.md`, S262) plus one queued field-schema row (S005); at T it gains the
full v7.2 `oom` trace-event set (eight events, `TP_STRUCT__entry` field sets, emitting functions, reaper
lifecycle), entry `corpus/knowledge/oom-tracepoints-r47.md` (S475 header, S476 call sites, S477 host
tracefs listing; S005 re-opened, byte-identical). Count line in README: 8 —
`grep -c '^TRACE_EVENT(' corpus/evidence/sources-r47/include_trace_events_oom.h` (ran, exit 0). "FR13
stays frontier: no tracer is enabled, installed or proposed (the host's `events/oom/enable` reads `0` and
stays untouched)". The entry's `coverage-map: FR13` and `ground:` cite the README Frontier row.

## 4. Assimilation line (theme FR13)

From `corpus/lessons/round-47.md` `## Gate` / `## Assimilation` and
`.ufo/waves/round-47/assimilation/` (read):

- Theme: FR13, OOM tracepoints; package `/home/vgpnk/Projects/shokuknow/merge/mori/` read-only, nothing written there.
- Collisions: registry 247 ids (`assimilation/reg-ids`) vs staged 136 ids (`assimilation/staged-ids`) → exactly `S471 S472 S473 S474` (`assimilation/collisions`).
- Admitted: staged **S507** (ROMA full text, the DOI) renumbered to lane **S478** — anchored by the publisher PDF URL the L1 re-opened; the staged page-count error ("4 pages" → printed pp. 3015–3028, 14 pages) was corrected; access date, located quote (p. 3016, §I, pdftotext lines 139–141), recheck `180d`, used-by exactly the admitted entry.
- Refused: staged entry `knowledge/corpus/knowledge/oom-tracing-tracepoints-r42.md` as written ("exactly three named tracepoints" refuted by S475's eight `TRACE_EVENT`s; the paper itself says "such as"); staged **S501** (abstract-level ROMA, already held as lane S262). Quarantine slice: 3 register rows (`S244`, `S262`, `S268`) in the unchecked "could not be fetched" family (`assimilation/quarantine-slice`), verdict unverifiable, none appended.
- Renumber map: staged **S507 → S478**; staged S475–S477 collide by number only and are unrelated documents — the lane's S475–S477 are this round's own rows. No other staged row is appended.

## 5. Considerthese line

`considerthese/2026-10-25.md` suggestion 1 (lines 44–46): "Add a registry pin check to my daily review. For each `SKILL.md` gate row … compare the pinned sha256 and selftest tally against `git show HEAD:<path> | sha256sum` and a real `--selftest` run. Then list any mismatch by line number." Implemented as `tools/mori-pin-check.py` and QUALITY 123 (C1 instrument; v2 tool at T, hardened after wave-1 seats found v1 false greens).

## 6. Census runs (start + fresh end)

Both are the SOURCES-registry census `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori` (output format matches `evidence/census-start.txt`).

- Start (committed `evidence/census-start.txt`): 19 W04 duplicate-url warnings (S035, S037, S073–S076, S147–S150, S166, S168, S201, S218, S220, S228, S349, S351, S470) + `mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md` + `rc=0`.
- Fresh end run (this seat, saved in `…/.scratch/r47w2-ScribeSourcesSection/census-end-validate.txt`): 20 W04 warnings — the same 19 plus new **S476** `duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes` (S476 vs S003, distinct aspects per lesson Gate) — + the same `ok` line + `validate rc=0`. Totals mode (`census`): rows 251, tier.A 220, tier.B 14, tier.C 17, mined 201, queued 24, rejected 26; FLEET identical, `tier.invalid 0 status.invalid 0 missing 0`, exit 0. W04 is warning-only (does not affect a clean lane), so both runs exit 0; the end run's only delta is the new S476 surface (the S005 status flip and the four additions are consistent with the W-row set).

## 7. Verdict

- C2 counting command E→T: **holds** — E unmet (`failed=entry_absent,pins,source_row`), T met (`events=8 rows=8`, all mismatch counters 0, `source_row=ok provenance=ok`), receipts' rev tree equals T for every measured file.
- Sources rows before→after: **holds** — 247→251, +4 tier A (S475–S478), S005 only touched row (queued→mined, used-by added).
- Frontier FR13: **holds** — row stays frontier, gains the v7.2 event-set ground at T.
- Assimilation line: **holds** — 4 collisions S471–S474; admit S507→S478 re-grounded; refuse staged entry + S501; quarantine slice unchanged.
- Considerthese line: **holds** — suggestion 1 → `tools/mori-pin-check.py` + QUALITY 123.
- Census: **holds** — start vs fresh end both exit 0; end run adds exactly one W04 (S476).

UNVERIFIED: nothing in this seat's scope — every number above is from a command run in this seat or a direct read of committed files.
