# Draft: round-20 FR3 advance (candidate text; L1 appends after acceptance)

Target 1: append to `/home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md` (after the
`## Round-18 appended scope notes (2026-10-21)` block, at end of file).

Target 2: append to `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/README.md` (after the
`## Round19 retrospective index repair (not new growth)` block, at end of file). The FR3 row at
`corpus/README.md` line 334 and the `PROVINCE.md` FR3 bullet at line 46 are left byte-unchanged;
the boundary they state still holds.

---- BEGIN PROVINCE.md APPEND ----

## Round-20 appended scope notes (2026-10-21)

- **Core, per-seat wave settlement (FR3 first-evidence advance, read-only):** `tools/mori-wave-settlement.py scan` reads every `ufo-swarm-wave-dispatch-v1` file under the lane's `.ufo/waves/` and grades each member of `taskCall.tasks[*]` by filesystem shape only. The member's `Report:` trailer path (last line of its task) is `present` (regular non-symlink file, size > 0), `empty` (size 0), `missing`, `misrooted` (absent under the lane root but a regular file at the same relative path under `--fleet-root`; counted as not present), `unsafe` (absolute, contains `..`, or resolves outside the lane root; never read) or `unparsed` (no trailer). A wave is `settled`, `partial`, `unsettled`, `no-spawn` or `unavailable`. Output is `mori-wave-settlement-v1` counts, sorted member names and the dispatch digest; report bytes are never emitted. Exit 0 only when every discovered wave is `settled` or `no-spawn`.
- **Boundary of the advance:** a `missing` or `empty` member is not a dead, failed or killed seat, and it is not proof that the report was never written. The scan cannot distinguish a report emptied or removed by hygiene from one that was never written, and it does not authenticate who wrote a dispatch file or its `taskCall` (dispatch authenticity). Result semantics and orchestration verdicts remain kumitate-owned; receipt review stays offline.
- **Frontier, FR3 (still open):** emptied-by-hygiene versus never-written, and dispatch authenticity. The round-12 hygiene-interference candidate (`corpus/lessons/round-12.md:109`) is not measured by the census.
- **Name collision, recorded:** the lane's hand-written round-19 record `.ufo/waves/round-19/wave1-settlement.json` carries the schema text `mori-wave-settlement-v1`. It is not a dispatch file, so discovery counts it as `ignored_json`; the name is not evidence that the tool ran.
- **Measurement status:** this note claims the design and its bounds. Counts (14/14 frozen oracle cases; the round-19 wave-1 reproduction and the fleet-wide totals) are recorded only from the L1-run receipts under `.ufo/waves/round-20/evidence/`; no count is stated here before that receipt is committed.

---- END PROVINCE.md APPEND ----

---- BEGIN corpus/README.md APPEND ----

## Round-20 coverage addition

| Ground | Entry | Bounded advance |
|---|---|---|
| Per-seat wave settlement (FR3 first evidence) | `tools/mori-wave-settlement.py`; oracle `.ufo/waves/round-20/frozen/c2-expected.json`; receipts `.ufo/waves/round-20/evidence/c2-{before,after}.json` | Filesystem shape per dispatched member (`present`/`empty`/`missing`/`misrooted`/`unsafe`/`unparsed`) and wave state (`settled`/`partial`/`unsettled`/`no-spawn`/`unavailable`); names and counts only; never a dead, failed or killed verdict. Emptied-by-hygiene versus never-written and dispatch authenticity stay frontier. |

## FR3 frontier boundary after round 20

The FR3 row above keeps its boundary. Round 20 moves per-seat filesystem settlement into Core
and leaves two frontier items open:

- **Emptied-by-hygiene versus never-written.** A `missing` or `empty` member does not show which
  happened: a report removed by cleanup and a report never written both read `missing`. Receipt
  review of cleanup records stays offline.
- **Dispatch authenticity.** The scan reads `ufo-swarm-wave-dispatch-v1` files as found; it does
  not verify their author or the `taskCall` payload. Payload-identity binding per attempt remains
  the observation-only round-18 dispatch ledger (`knowledge/dispatch-ledger-r18.md`).

---- END corpus/README.md APPEND ----
