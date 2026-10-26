# Mo49ScoutCoverage — coverage and adjacency scan for `journal-reach-r49.md`

Seat: scout (read-only). Lane tip read: `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115` (freeze commit, `git log -1`). Author date of this report is on or after that tip's committer date (2026-10-25T21:36:32-03:00). No tool was installed or upgraded. No lane tool was run; no journal command was run by me (I read the committed receipt only).

Method note: the sibling hit grep ran as a background job (134 s wall). `lsp` was not used: every target is markdown/TSV/plain text, so no language server answers these files; the evidence below is text grep/read and is the literal fallback, not semantic proof.

## 1. Sibling hit list

Command (verbatim, exit 0):

```
grep -rliE 'journald\.conf|SystemMaxUse|MaxRetentionSec|vacuum' /home/vgpnk/Projects/shokunin/*-shokunin/corpus /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md
```

Hits outside mori (9 files, 3 lanes) — the other 26 hits are mori's own (`mori-shokunin/corpus/knowledge/{structured-journal-scopes-r13,journal-alarm-routing-r14,journal-positive-evidence-r15,journal-cursor-window-r16,journal-disk-usage-total-r51}.md`, `lessons/round-{12,16,16-verifier-spotcheck,17,30,30-verifier-spotcheck,43,43-verifier-spotcheck,44}.md`, `evidence/recheck-r32/S014.src`, `S015.src`, `S037.src`, `evidence/sources-r40/S229.src`, `sources-r41/S231.src`, the four `evidence/sources-r49/*` copies, `corpus/README.md`, `corpus/SOURCES.md`, `PROVINCE.md`):

```
kagi-shokunin/corpus/knowledge/handler-on-disk-state.md
kagi-shokunin/corpus/knowledge/surface-census.md
kagi-shokunin/corpus/state-shape.tsv
kaidoku-shokunin/corpus/knowledge/2026-10-13-crash-evidence.md
tsukuroi-shokunin/corpus/knowledge/boot-plane.md
tsukuroi-shokunin/corpus/knowledge/degraded-triage-r4.md
tsukuroi-shokunin/corpus/knowledge/host-health-report-r3.md
tsukuroi-shokunin/corpus/knowledge/journal-boot-plane.md
tsukuroi-shokunin/corpus/knowledge/oom-event-plane.md
```

No sibling `PROVINCE.md` matched the pattern (separate grep over kagi/kaidoku/tsukuroi `PROVINCE.md`: "No matches found"). Only `mori-shokunin/PROVINCE.md` matches (`:25` "vacuumed anchor", `:40` "rotation/vacuum", `:54` FR11 "rotation/vacuum and retention behavior").

## 2. Per-hit classification

| hit | what the matched lines say (observed) | owner class | contradicts the planned entry? |
|---|---|---|---|
| `kagi/.../handler-on-disk-state.md:164-169`, `surface-census.md:122`, `state-shape.tsv:17` | "no `purge`/`reset`/`vacuum` verb" and "grows without a vacuum verb" — kagi's own state DB/log, not journald | neither: false positive (a vacuum verb on a vault handler's SQLite store; `vacuum` word collision) | no |
| `kaidoku/.../2026-10-13-crash-evidence.md:43,47` | coredump retention "default vacuuming (MaxUse/KeepFree unset)" reaped the oldest core; "an RE pass … should run before vacuuming shrinks the window" | retention-as-evidence-reach of **coredump files** (`coredump.conf`, not `journald.conf`); kaidoku's RE evidence window, not mori's journal reach | no, but a different store: coredump `Storage=none`/`MaxUse=512M` is documented in tsukuroi `coredump-count-unit-r34.md:16,23`; the entry must not blend coredump-file reach into journal reach |
| `tsukuroi/.../boot-plane.md:20-25,263,291` | 13 boots, 181.3 M on disk (2026-10-14), `journalctl --disk-usage` and `--list-boots` read, "no `journalctl --rotate|--vacuum*`" | tsukuroi's boot/journal plane (OS diagnosis); incidental `--list-boots`/`--disk-usage` reads | no — dated 2026-10-14, a different moment than the planned 2026-10-25 receipt (56M, 2 boots) |
| `tsukuroi/.../journal-boot-plane.md:50-52,362-363,373` | "Rotation policy not proven: `/etc/systemd/journald.conf` ships with all directives commented (read 11:39); effective defaults not derived." Open unknown: "Effective journald retention (`SystemMaxUse`, rotation date of boot −12): shipped config is defaults-only; effective value not derived." | **journald configuration ownership** (tsukuroi) | not a contradiction but an overlap: the planned entry derives the effective ceilings (receipt: drop-in `/etc/systemd/journald.conf.d/size.conf` sets `SystemMaxUse=256M`, `RuntimeMaxUse=64M`, mtime 2026-10-16 11:53, i.e. two days *after* tsukuroi's 2026-10-14 read). tsukuroi's statement is a dated true reading of that moment and is now stale as a current statement; its open unknown is answered by mori's evidence, which tsukuroi has not recorded |
| `tsukuroi/.../oom-event-plane.md:189-192` | "`/etc/systemd/journald.conf` is all-commented (defaults, no drop-in dir)" used to rule out journald drop of OOM records | journald configuration ownership (tsukuroi) used as an OOM-evidence argument | same: true at its date (2026-10-14), false now (drop-in exists since 2026-10-16 per the receipt). The entry must date its reading and not restate "no drop-in" |
| `tsukuroi/.../degraded-triage-r4.md:282,526`, `host-health-report-r3.md:50,271` | `coredumpctl --help` has no delete/vacuum; core removal is a root file operation; "decide an explicit retention policy (operator)" | tsukuroi OS triage of coredump storage; operator-owned retention policy | no (coredump store, not journal) |
| mori `journal-alarm-routing-r14.md:165-166,175-176` | "Processes outside manager observation, inaccessible journal, vacuumed files — No retained record"; "No retained record — … vacuumed. Nothing can be counted, and absence is not evidence of zero events." | mori retention-as-evidence-reach (the class the entry gives a rule to) | no — the entry supplies the rule behind the sentence and must not weaken "absence is not evidence of zero events" |
| mori `journal-cursor-window-r16.md:47,66,80,91` | "Retention, vacuum, rotation and rate-limiting are not opened in this note"; "The journald retention … behaviour that determines which records exist to be returned. Not opened this round."; "No permanent-retention claim" | mori; this is the FR11 remainder | no — the planned entry opens exactly what r16 listed as not opened; it must stay an additive note and not claim the cursor probe's refusal now proves vacuum (FR11 boundary: "a byte mismatch is refusal evidence only, not proof of vacuum or deletion") |
| mori `journal-disk-usage-total-r51.md:8-10` | `--disk-usage` is a total over files the command can see; host 2026-10-24 printed 269M; "not a license to vacuum, rotate, or change journald" | mori retention-as-evidence (resource runway) | no; note the receipt's 56M (2026-10-25) vs 269M (2026-10-24) is a one-day move the entry must date, not average |
| mori `SOURCES.md` S351 (rejected, 2026-10-24) | rejected the staged reach entry "grounds itself in a shokuknow file:// note and a kernel MESSAGE grep … flip: the public --vacuum-size= sentence plus a committed read-only disk-usage receipt, and no MESSAGE grep" | mori's own refusal | the new row must be a flip of exactly this; see finding F1 |

Summary: 0 contradictions with the planned entry. 2 genuine journald-configuration statements (tsukuroi `journal-boot-plane.md`, `oom-event-plane.md`) are dated before the host drop-in's mtime, so they are stale as *current* claims and must be reported to tsukuroi, not edited by mori. kagi (SQLite) is a false positive; kaidoku (coredump store) is a different store.

## 3. One-sentence boundary the entry must carry

> This entry reads how far back the journal evidence mori can read is able to reach (the retention rule, the persistent/volatile split, vacuum order, and the ceilings the 2026-10-25 read-only receipt shows) as fleet evidence reach only; the journald configuration, its drop-ins, vacuum/rotate action and OS state belong to tsukuroi/operator, a reach figure is never a count of events or proof that an absent record never occurred, and mori ran no vacuum, rotate or config change.

(Alternative shorter form if the entry header wants one line: "Retention is read as evidence reach, never owned or tuned: `journald.conf`, drop-ins and vacuum are tsukuroi/operator state; absence past the reach is no evidence of zero.")

## 4. Coverage-map row(s) the entry should attach to

Primary attach point: the FR11 Frontier row at `corpus/README.md:351` (mirrored `PROVINCE.md:54`), which holds the exact remainder — quoted:

> `| FR11 | New-since-anchor journal record/notice subsets via cursors | `SOURCES.md:20-21`; `knowledge/journal-cursor-window-r16.md` | Cursor queries stay read-only and anchor-scoped. Round 16 advances FR11 only to an exact-retained, same-boot window: … [UNKNOWN] behavior after cursor rotation/vacuum, unreadable later journal files under `-q` (not detected; an OK window may be partial), and ordering across boots remains open. |`

and the `PROVINCE.md:54` form "Remainder: cursor rotation/vacuum and retention behavior beyond the exact-match refusal …". The entry does not close FR11 (no cursor/anchor work, no cross-boot ordering, no persisted anchor), so the append must be a dated note beside the row, following the lane's pattern (round-24 FR12, round-34 FR6, round-48 FR2: "the row above is not rewritten").

Secondary attach (map-row whose Holds text names the same gap): `corpus/README.md:43` the `knowledge/journal-cursor-window-r16.md` coverage-map row — "… rotation/vacuum and cross-boot stay unavailable; `-q`-hidden inaccessible-journal partial reads are not detected …".

Also the FR1 row at `corpus/README.md:341` (FR1 evidence reach is the contract's own framing: "journal retention reach (FR1 evidence reach)"): "Structured system-journal notice records advance round 13; kernel victim/summary token validation and fleet task correlation remain frontier. Catalog-ID records are not authenticated unique kills. …". The entry advances neither FR1's victim attribution nor its token validation, so it should cite FR1 only as "the reach beneath the FR1 class counts", not as an advance.

Where the new text lands: the lane convention since round 43 is a dated `## Round-49 coverage additions` section (examples at `README.md:624` Round-43, `:644` Round-47, `:657` Round-48) with a `| Ground | Entry | Bounded advance |` table, plus the `## Round-43 coverage additions` sentence at `:626` that already holds the neighbouring resource-runway ground ("`journalctl --disk-usage` is a total over archived and active files … 269M"). The new section should refer back to that line and state the 269M → 56M movement (dated 2026-10-24 vs 2026-10-25) as a dated reading. The entry's own header should also carry `coverage-map:` like `journal-disk-usage-total-r51.md:6` ("resource runway (journal store size). Not FR1 kernel-victim attribution.") with "FR11 remainder (retention behavior beyond the exact-match refusal); FR1 evidence reach, not attribution".

## 5. Adjacency routing (report only)

- tsukuroi row of `PROVINCE.md:66` (Adjacent table): "Owns host OS, package, systemd-unit, driver, firmware, and boot diagnosis … adjacent host diagnosis, not contested fleet ownership." That row's boundary covers the entry: journald configuration and drop-ins are tsukuroi's. The Refuses paragraph (`PROVINCE.md:12-15`) already states "OS package, systemd unit, driver/firmware and boot state (→ tsukuroi) — mori reads journal and cgroup events as fleet evidence and reports them, never owning OS state". The entry fits that sentence without a PROVINCE edit.
- Suggested tsukuroi handoff (reported by the L1, not by me): `tsukuroi-shokunin/corpus/knowledge/journal-boot-plane.md:51-52,362-363` and `oom-event-plane.md:189` record "defaults-only / no drop-in dir" as of 2026-10-14; the 2026-10-25 receipt shows a drop-in `size.conf` (`SystemMaxUse=256M`, `RuntimeMaxUse=64M`, mtime 2026-10-16). That is a candidate update for tsukuroi's open unknown "Effective journald retention (`SystemMaxUse` …) … not derived", not a mori edit.
- tsukuroi already tracks retained-boot counts that shrink across its own notes: 13 boots (2026-10-14, `journal-boot-plane.md:14`, `boot-plane.md:21`), 9 (2026-10-19, `README.md:49-50`), 6 (2026-10-22, `storage-health-r26.md:133`), and the receipt shows 2 (2026-10-25). These are dated neighbour numbers that corroborate shrinking reach; they are not mori's evidence and must not be cited as the entry's quote sources (contract bars outside-lane receipts).

## Findings

- **F1 (HIGH) — `corpus/evidence/sources-r49/host-journal-reach.txt:95-97` vs `contract.md:82` and S351's flip text.** The receipt contains `journalctl -b 0 -u systemd-journald --no-pager -q -g 'Journal .* is .*max'` — a `--grep` over MESSAGE text — and the frozen flip for S351 is "a committed read-only disk-usage receipt, and no MESSAGE grep". The matched lines are journald's own startup size lines (unit-scoped `-u systemd-journald`, one boot, two lines), not a kill/OOM count, which is not the S351 reason ("a shokuknow file:// note and a kernel MESSAGE grep"), but the literal flip wording is breached. The new `supersedes S351 —` teaches cell and the entry's limits must say so openly (a unit-scoped grep of journald's own start-up lines, never a fleet-kill count), or the entry must not draw any quote from lines 95-97. I cannot tell from here whether `count-c2.py` or a wave-2 reviewer will treat this as a flip failure: UNVERIFIED.
- **F2 (MED) — boundary sentence absent from the frozen contract.** `contract.md:69-83` names the surface but does not state the ownership boundary against tsukuroi's journald configuration; the entry needs the sentence in section 3 (or equivalent) in its body, the README round-49 section, and the SOURCES `teaches` row, otherwise it is exposed to the "mori absorbs tsukuroi's OS state" reading (`PROVINCE.md:12-15`).
- **F3 (MED) — tsukuroi staleness, `tsukuroi-shokunin/corpus/knowledge/journal-boot-plane.md:51-52,362-363,373` and `oom-event-plane.md:189-192`.** Those say journald.conf is all-commented / no drop-in dir (read 2026-10-14). The receipt (`host-journal-reach.txt:69-76`) shows `/etc/systemd/journald.conf.d/size.conf` mtime 2026-10-16 11:53:47 with `SystemMaxUse=256M`, `RuntimeMaxUse=64M`. Not a contradiction (different dates); the entry must date every host number and must not generalize "defaults-only". Route to tsukuroi; no edit by mori.
- **F4 (MED) — host numbers moved within a day.** `journal-disk-usage-total-r51.md:10` 269M (2026-10-24) vs receipt 56M total / 19M system / 37M user (2026-10-25 20:43) and 2 boots listed (`host-journal-reach.txt:89-92`). The entry must not present either as steady-state reach, and README `:626` ("269M") should receive an append-only dated pointer, not a rewrite.
- **F5 (LOW) — `host-journal-reach.txt:86-87`.** `ls -A /run/log/journal` printed nothing, exit 0, while the journald startup line names `/run/log/journal/MACHINE_ID` at 13:36:19 (`:96`). Plausibly the runtime directory is emptied after the flush to `/var/log/journal`, but I did not verify the mechanism (UNVERIFIED). The entry must not turn the empty directory into "no runtime journal" or "runtime journal disabled" without the `journald.conf(5)`/`systemd-journald.service(8)` flush wording located in the committed copies.
- **F6 (LOW) — false-positive collisions in the sibling sweep.** kagi's `vacuum` (SQLite verb) and kaidoku's coredump-file vacuum are different stores; the pattern `vacuum` alone will keep re-matching them. The entry's recheck line should use `journald.conf`/`SystemMaxUse`/`MaxRetentionSec` (0 mori hits at `b3e3453d`) rather than `vacuum`.
- **F7 (LOW) — naming drift, not a defect of this round.** `journal-disk-usage-total-r51.md` carries round number 51 although README records it under `## Round-43 coverage additions` (`:624-626`). The new entry's cross-reference should use the real file name and say "added round 43" to avoid a pointer that reads as a future round.
- **F8 (LOW) — SOURCES.md rows S485–S488 are not yet present** (grep for `S485|S486|S487|S488` found none; `git status --short corpus` printed nothing). Expected: L1 integrates in wave 1; nothing for this seat to repair.
