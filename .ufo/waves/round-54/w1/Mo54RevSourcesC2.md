# Mo54RevSourcesC2 — review of rows S521–S524, the used-by changes of S502/S507, and the `## Leads` additions

MACHINE_ID: 432d02b544a5459ebbff9c42ec68334d
Reviewed revision: `78295c764093ff1f6cee08d7246679900bde7265` (data commit; entering tip `39dcf4d7e410d362781a47e8365ca23b5c807598`)
Contract: `/home/vgpnk/Projects/shokunin/CORPUS.md` → SOURCES contract v1 (kaika, 2026-10-19, frozen)
Seat scope: rows S521–S524, the S502/S507 used-by changes, and the two round-54 `## Leads` bullets, all in `corpus/SOURCES.md` at the data commit, against the frozen contract.
Method: read-only. `git archive <rev>` of `corpus/SOURCES.md`, `corpus/knowledge/memory-failure-kills-r54.md` and `corpus/knowledge/kernel-v7.3-recheck-r54.md` into scratch (`/fast/scratch/hyaku/mori-r54/Mo54RevSourcesC2/`, removed after this report); anchors read in the committed copies under `corpus/evidence/`; sha256 computed independently with `sha256sum`. No git/jj mutation, no pacman use, no tool installs, no host writes, no network fetches.

## 1. What the data commit changed in `corpus/SOURCES.md`

`git diff 39dcf4d7..78295c76 -- corpus/SOURCES.md` → 1 file changed, 16 insertions(+), 4 deletions(-):

- rows S502, S507, S508, S514 rewritten in place: used-by cells gained one path each (S502/S507 → `corpus/knowledge/memory-failure-kills-r54.md`; S508/S514 → `corpus/knowledge/kernel-v7.3-recheck-r54.md`); no other cell of those four rows changed.
- ten new rows appended after S520: S515–S520 (C1's sources) and S521–S524 (C2's sources).
- two bullets appended under `## Leads (unopened)`.
- nothing else: `## Paths`, `## Search log` and the rest of the registry are untouched (relevant to Finding F1).

Separability holds as the contract's table requires: the C2 data touches only S521–S524, the S502/S507 used-by cells, the entry, and the four `sources-r54` copies; no C1 row or ledger cell is entangled in them.

## 2. Anchor verification — every named range opened in the copy

All ranges verified with `grep -n` line hits plus full ranged reads of the committed copies. Evidence per range (copy → observed):

S521 `corpus/evidence/sources-r54/memory-failure.c.v7.3` (3029 lines):

- pr_fmt 37 — line 37 is `#define pr_fmt(fmt) "Memory failure: " fmt`. Exact.
- sysctls 72-78 — the four `static int sysctl_*` definitions sit at 72 (`memory_failure_early_kill`), 74 (`memory_failure_recovery`), 76 (`enable_soft_offline`), 78 (`panic_on_unrecoverable_mf` variable). Exact.
- sysctls 134-171 — `static const struct ctl_table memory_failure_table[] = {` at 134, closing `};` at 171; the four `.procname` entries at 136, 145, 154, 163 (`"panic_on_unrecoverable_memory_failure"` at 163). Exact, and "the four sysctls" in the scope cell is the true count.
- kill_proc 286-311 — signature at 286, `return ret;` at 310, closing `}` at 311; contains the `Sending SIGBUS … due to hardware memory corruption` pr_err and the BUS_MCEERR_AR/BUS_MCEERR_AO split. Exact.
- kill_procs 462-490 — signature at 462, closing `}` at 490; contains the `forcibly killing … failure to unmap corrupted page` pr_err with `do_send_sig_info(SIGKILL, …)`. Exact.
- action_name 871-876 — `static const char *action_name[] = {` at 871, closing `};` at 876, the four outcome words Ignored/Failed/Delayed/Recovered. Exact.
- action_result 1281-1298 — signature at 1281, closing `}` at 1298; contains `trace_memory_failure_event`, the `type != MF_MSG_ALREADY_POISONED && type != MF_MSG_PFN_MAP` guard over `num_poisoned_pages_inc`/`update_per_node_mf_stats`, the `recovery action for %s: %s` pr_err, and the `panic_on_unrecoverable_mf` panic. Exact.
- per-node counters backing the scope cell: `MF_ATTR_RO(total/ignored/failed/delayed/recovered)` at 114–118, attribute group `.name = "memory_failure"` at 129–132. Present as scoped.

S522 `corpus/evidence/sources-r54/hwpoison.rst.v7.3`:

- `Failure recovery modes` heading at 54; section runs to line 73 (early kill 62–67, late kill 69–72; `User control` heading at 74). Range 54-73 exact.
- `User control` at 74 through 105 (the blank before `Testing` at 106); covers `vm.memory_failure_recovery`, `vm.memory_failure_early_kill`, `PR_MCE_KILL`. Range 74-105 exact.

S523 `corpus/evidence/sources-r54/sysfs-devices-node.v7.3`:

- memory_failure entries 192-229: `What:` lines at 192 (total), 199 (ignored), 208 (failed), 216 (delayed), 224 (recovered), recovered `Description` ending at 229; next entry (`nodeX/reclaim`) starts at 231. Exact.

S524 `corpus/evidence/sources-r54/memory-failure-trace.h.v7.3`:

- `#define TRACE_SYSTEM ras` at line 7 (with the historical-reason comment at 3–6). Exact.
- `TRACE_EVENT(memory_failure_event,` at 74; TP_printk at 93; the invocation closes `);` at 98, `#endif` at 99. The anchor "74-98 with its TP_printk" is exact.

No anchor range in S521–S524 is off by even one line.

## 3. sha256 prefixes

Independent `sha256sum` over the committed copies; the row's pinned prefix is the first 12 hex of the observed digest:

- S521 pinned `94d24a605b61` — observed `94d24a605b61f94ad1d10ab3db26aed12cb6113af15431ff873da5b98ca48003`. Match.
- S522 pinned `8011bb158129` — observed `8011bb158129776bbb38ed5808959bd14d17489527ed3987dbc3d21d27e3ecb7`. Match.
- S523 pinned `d852f950e42d` — observed `d852f950e42d92b862792477a892e77973ddb6a345bdb1748d2e7c5020198665`. Match.
- S524 pinned `a395e62b36ac` — observed `a395e62b36ace3d1295fd3e9e469fc525f67c7787f529a380633d6b800f051ea`. Match.
- S507 copy `sources-r53/vm.rst.v7.3` — observed `f81feb3dfca5…`, matching S507's unchanged pin.
- S502 copy `sources-r53/proc.rst.v7.3` — observed `bc178ff511e0…`, matching S502's unchanged pin.

Note the pins tie rows to the local committed bytes; I did not re-fetch from cgit (that is the wave's independent-refetch seat). Within-scope conclusion: the bytes on disk are what the rows describe.

## 4. Field-contract census at the data commit

Run with the frozen contract's census awk on the extracted `corpus/SOURCES.md` (369 lines):

- malformed rows: none (every registry row parses to 11 columns);
- enum violations: none (`kind`/`tier`/`status` all in the frozen vocabularies; no tier-A `community`);
- duplicate ids: none; S521–S524 are the next unused ids after S520;
- no `|` inside any cell of the new rows;
- `opened` = 2026-10-27 on all four new rows (opened in the round that writes the row — wave runs today), `recheck` = `on-release`, `status` = `mined` with a non-empty used-by, `tier` = A for code/official docs (primary for their scopes — legitimate under the tier definition), `teaches` one grounded learner benefit each.

## 5. used-by changes of S502 and S507

Both rows' used-by cells gained exactly `corpus/knowledge/memory-failure-kills-r54.md`. Cross-checked against the entry extracted at the data commit (86 lines):

- The entry's provenance block cites, in order: S521, S522, S523, S524 (line 3–5 of the entry) and S507, S502 (line 6). So the append on S502/S507 is backed by a real citation, and the reverse direction holds too: every S-row the entry names carries the entry in used-by (S521–S524 mined status is thus honest).
- S502 citation grounding: the entry's HardwareCorrupted row quotes `HardwareCorrupted / The amount of RAM/memory in KB, the kernel identifies as corrupted.` — present in `sources-r53/proc.rst.v7.3` at lines 1269–1271, inside S502's anchored meminfo section 1043-1302. The use sits inside the row's declared scope and anchor. Clean.
- S507 citation grounding: both quoted passages are present in `sources-r53/vm.rst.v7.3` — the catchable-SIGBUS sentence at 514–515 (section `memory_failure_early_kill`, heading at 495) and the panic-switch section `panic_on_unrecoverable_memory_failure` at 926 ff. — but see Finding F2: those sections are outside the row's immutable anchor/scope cells.
- The C1-side used-by changes (S508, S514 → the ledger) cross-check the same way (`source: S508, S514, S515–S520` on the ledger's line 3); listed here only to confirm the S502/S507 edits are the only C2-side ones.

## 6. `## Leads` additions

Bullet 1 (round-54): "the round-53 lead above is opened this round as S507/S521" — see Finding F3 on wording. Substantively true: the panic-on-unrecoverable surface the round-53 lead named is now cited ground (S507 copy, section at vm.rst.v7.3:926 ff.) and `mm/memory-failure.c` at v7.3 is opened as S521.

Bullet 2 (round-54 release drift from the S520 copy): every claim verified in `corpus/evidence/sources-r54/cgroup-v2.7.3.html`:

- `memory.pressure` — `<dd><p>A read-write nested-keyed file.</p>` at html line 1719; `io.pressure` same wording at 2012. Matches "documented read-write (7.2: read-only)".
- `cpu.stat` — html line 1103: `Note that the above five CFS bandwidth stats are non-hierarchical`. Matches.
- `io.stat` throttle field — html lines 2117–2118: `the use_delay and delay_nsec fields in io.stat increase. The delay_nsec value is how many nanoseconds …`. Matches "renamed delay → delay_nsec, unit microseconds → nanoseconds".
- The bullet's pointer to `corpus/knowledge/kernel-v7.3-recheck-r54.md` `## Release drift` is accurate: that section records the same three drifts and routes them here as leads.

Leads discipline is respected: both bullets stay unopened-lead territory (bullet 2 names `block/blk-iolatency.c` and `kernel/sched/` at v7.3 as *not opened*), and the round-53 lead bullet is left in place with the new bullet superseding it in prose — consistent with the lane's append-only handling of this section.

## 7. Mid-round obligations still open at the data commit

- `corpus/lessons/round-54.md` does not exist at the data commit (`git ls-tree 78295c76 -- corpus/lessons/` lists no round-54 file). Contract rule 1 requires the round lesson's `## Gate` to record, per new row, URL, access date and a ≤25-word location-grounded quote. Expected to land with the wave's drafting seats; UNVERIFIED until closure — see Finding F1.

## Findings

- F1 (MED) — `corpus/SOURCES.md` `## Search log`: the data commit adds ten source rows (S515–S524) and two leads without any round-54 bounded-search entry, although the frozen contract's Search-log rule (rule 5) wants one prose note per bounded search and every prior row-adding round (24, 37, 39, 46, 53) logged one at or before its data landing. Likewise `corpus/lessons/round-54.md` (Gate records per rule 1) is absent at `78295c76`. If both land by round closure this resolves to conformant; if closure ships without them, the registry is not conformant on rule 5 and the new rows lack their Gate quotes. Concerns: `corpus/SOURCES.md` (Search log section, after the round-53 addendum) and `corpus/lessons/round-54.md` (missing).
- F2 (LOW) — S507's used-by now cites the entry for two passages (vm.rst.v7.3:514-515 catchable SIGBUS; vm.rst.v7.3:926 ff. panic switch) that sit outside the row's immutable anchor and scope cells, which name only the overcommit/reserve sysctls (admin_reserve_kbytes 82-108, overcommit_kbytes 823-831, overcommit_memory 834-856, overcommit_ratio 859-886, user_reserve_kbytes 1106-1123). Mitigations observed: the teaches cell already records `v7.3 adds panic_on_unrecoverable_memory_failure`, and the round-53 lead explicitly pointed at the S507 copy as the kill/panic surface, so the use is continuous with recorded intent; the text is verified present, and immutable cells cannot be extended in place. Per the lane's own precedent for a new scope on a same URL (S492, S502 — "same URL … with a different scope" rows), a dedicated scoped row would have been the cleaner shape. No data correction required; noted for round-55 routing if the L1 wants the S507 scope split.
- F3 (LOW) — Leads bullet 1 wording: "the round-53 lead above is opened this round as S507/S521" — S507 was opened 2026-10-26 (round 53, per its own `opened` cell, untouched by this diff); only S521 is new this round. The accurate phrasing is that the lead resolves to the existing S507 copy plus new row S521. Cosmetic; the L1 may reword in place only if it treats this bullet as this round's own (not yet frozen) prose.

Verification gaps (not defects): (a) source bytes were checked against the committed copies' hashes and anchors only — no independent cgit re-fetch was performed in this seat; (b) the entry's 21 claim-quote pairs are the ENTAILMENT seats' surface — I verified the quotes' presence and locations only where they intersect my anchor scope (S502:1269-1271, S507:514-515, S507:926 ff.), not the entailment of all 21 rows; (c) F1's Gate quotes cannot be checked before the round lesson lands.

Report: .ufo/waves/round-54/w1/Mo54RevSourcesC2.md
