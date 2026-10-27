# Mo54CritC1Scope — attack on C1's scope and axis (D = the 31 v7.2-pinned table rows)

Seat: Mo54CritC1Scope (critic, C1 scope/axis). Claim under attack: round-54 C1, measured at data commit
`78295c764093ff1f6cee08d7246679900bde7265`; frozen contract `6830f3af`; counter `.ufo/waves/round-54/count-c1.py`.
All greps run with `git show 78295c76:<path>` / `git grep <rev>` against the lane repo read-only. Host kernel
observed: `7.2.11-arch1-1` (`uname -r`, 2026-10-27). No repo bytes were mutated.

## 1. Census: every v7.2 (or older) kernel byte pin with a release trigger at the data commit

`git grep -n -E 'recheck:.*(on-release|kernel release|release)' 78295c76 -- corpus/knowledge` → 18 `recheck:`
lines. Cross-joined with every `corpus/knowledge/*.md` whose source line or prose pins `torvalds/linux/v7.2`,
`@v7.2`, `?h=v7.2`, or `docs.kernel.org/7.2` (18 files) and with `corpus/SOURCES.md` (72 rows citing a v7.2
tag URL at `78295c76`). Result, grouped by what the v7.3 release trigger actually reached:

| artefact | v7.2 (or older) bytes it pins | release trigger | reached by round 54? |
|---|---|---|---|
| oom-memcg-stat-r50, commit-runway-read-r53, quota-observability-r48 | claim-table rows via S489–S491, S499, S511–S513, S481 | on-release | YES — the 31 rows of D |
| memavailable-estimate-r51, overcommit-commit-limit-r52 | claim-table rows via S492–S501 | on-release | partially — covered by the round-53 ledger, but see F5 |
| kernel-v7.3-recheck-r53 / -r54 | ledgers | on-release | n/a (armed for the next tag) |
| oom-tracepoints-r47 | S475 oom.h, S476 oom_kill.c/page_alloc.c/base.c at v7.2 — a non-`claim|source|quote` catalogue | on-release | **NO** (fired, not executed) |
| system-pressure-r24 | S090 psi.rst, S091 psi.c, S092–S095 cgroup-v2.rst/Kconfig/params/psi_types.h at v7.2 | "on a kernel release, re-open S090 and S091" | **NO** (fired, not executed) |
| watchdog-identity-r31 | S163–S165, S167, S173 at v7.2 (sched.h, exec.c, binfmt_script.c, array.c, kernel.rst) | "on a procps-ng, kernel or man-pages release" | **NO** (fired, not executed) |
| oom-victim-selection-r27 | S003 oom_kill.c, S127/S148 base.c+oom.h+fork.c at v7.2 | "on a kernel release re-open fs/proc/base.c and mm/oom_kill.c" | **NO** (fired, not executed) |
| kernel-oom-line-attribution-r12, kill-classes-by-message-id-r12, oom-kill-counter-kernel-only-r12, userspace-oom-killers-r12 | S003 v7.2 oom_kill.c (+ master-commit S004) | none — `recheck:` lines are imperative receipts hard-coding `v7.2` URLs | **NO** — and cannot self-detect drift (F5) |
| census-cgroup-levels-r45 | S473 cgroup-v2.rst `@v7.2` | `90d`, re-fetches the v7.2 URL | **NO** — version-frozen probe |
| disk-write-rate-r33 | S180–S187 (+S191–S194, S201–S202, S212–S217) v7.2 block-layer pins | "re-open when the host kernel moves past 7.2 or sysstat past 12.8.0" | **NO** — trigger not fired (host 7.2.11), and has no upstream-release arm (F4) |
| userspace-oom-killers-r26 | one kernel-side anchor (v7.2 oom_kill.c:935-936 via S003) | earlyoom/systemd releases + host commands | kernel arm absent (low — one anchor) |

Everything the round leaves unrechecked after a fired kernel-release trigger: **oom-tracepoints-r47,
system-pressure-r24, watchdog-identity-r31, oom-victim-selection-r27** — plus the r12 set and
census-cgroup-levels-r45 whose `recheck:` commands can only re-verify the old tag, and disk-write-rate-r33 whose
trigger never fires on upstream releases at all.

Routing already on record: SCORECARD `Planned (round 54)` (read at `78295c76`, line ~2843) names
"`oom-tracepoints-r47.md`, `oom-victim-selection-r27.md`, `disk-write-rate-r33.md`, `watchdog-identity-r31.md`,
the round-50 memcg entry, S511–S513" for "the v7.3 trigger for what D does not cover". Round 54 executed the
memcg entry + S511–S513 half and left the other four artefacts — and, notably, `system-pressure-r24.md` was
**not even in that list** although its `recheck:` line names a kernel release explicitly (contract line 55-56
does name r24's anchors as out-of-D, so the exclusion is disclosed at freeze but the artefact has no scheduled
recheck).

### Are the unrechecked artefacts actually stale?

- `oom-tracepoints-r47`: ran its own recheck command shape —
  `curl -fsSL 'https://git.kernel.org/.../include/trace/events/oom.h?h=v7.3'` (exit 0, into scratch) →
  `grep -c '^TRACE_EVENT('` = **8**, sha256 `82f04ad4108ba9499b638fe298967f124269c0a2feb6ddbb14b1ade59c974e0d`
  — byte-identical to the pinned v7.2 copy in S475. Conclusion stands, but the ledger never executed the
  recheck; my one-line check is a seat probe, not the artefact's record.
- `system-pressure-r24`: **stale in a way the ledger itself documents** — `kernel-v7.3-recheck-r54.md`
  `## Release drift` records that the rendered cgroup-v2 page at 7.3 documents `memory.pressure`/`io.pressure`
  as "read-write" (7.2: "read-only"). r24's S092 anchor is the same document family at v7.2; the artefact's
  access-mode statements are now one tag behind, parked as "leads", not rechecked.
- `disk-write-rate-r33`: the same drift note records `io.stat`'s throttle field renamed `delay`→`delay_nsec`
  with a unit change µs→ns at v7.3. r33's surface is /proc/diskstats field grammar (different file), and a grep
  of `tools/` and `SKILL.md` shows nothing keys `io.stat` or `delay` — so no live consumer is wrong today, but
  the artefact's v7.2 anchors drifted at a release its trigger cannot see.
- The four r12 entries' kernel anchor (S003 `oom_kill.c:447,935-936,945`): verified **incidentally fresh** —
  `corpus/evidence/sources-r54/oom_kill.c.v7.3` lines 446-448, 934-936, 945 are byte-identical to the text the
  r12 `recheck:` commands grep for. Their defect is instrument shape (version-frozen commands), not current
  wrongness.

## 2. Is `freshness` the honest axis?

Mostly yes for the rows in D, with two honest-label debts:

- **The axis is table-row freshness, not artefact freshness.** D is defined by `scope()` (`count-c1.py:212-235`):
  only `claim|source|quote` tables whose source cell resolves to a `SOURCES.md` row carrying one of four
  v7.2 URL shapes. Verified: only 7 knowledge files carry that table shape at `78295c76` (commit-runway-r53,
  journal-reach-r49, memavailable-r51, memory-failure-r54, oom-memcg-r50, overcommit-r52, quota-r48), and the
  contract/counter agree that prose, catalogues (r47's `| event | fields | emitter |…` table at :25+ does not
  match the header), and anchor prose (r24) are outside D — disclosed in contract line 55-56 and the counter
  docstring :39-40. The disclosure is correct; the *debt* is that a freshness score earned this way is silent
  on the five artefacts above that also pin v7.2 bytes. That is a named residual for the report, not a
  counter defect — the frozen scope cannot be widened this round.
- **Half of D exercised no drift.** Digest comparison of the committed copies at `78295c76`:
  `oom_kill.c`, `percpu_counter.c`, `percpu_counter.h`, `errno.h` v7.3 copies are byte-identical to their v7.2
  copies (e.g. oom_kill.c `452f1348…` both sides; errno.h `66a5ad60…` both). 10 of 31 rows sit on
  byte-identical files; for them `held` + same `line` was guaranteed before any judgement ran. The real
  freshness work is the 21 rows on the four changed copies (util.c, mm_init.c, memcontrol.c +45/+84 shifts,
  cgroup-v2.7.3.html +31).
- **Discoverability defect (fixable data, not predicate):** `grep -nE 'v7\.3|kernel-v7\.3-recheck|ledger'`
  over the three rechecked entries at `78295c76` → `oom-memcg-stat-r50.md`: zero hits; `quota-observability-r48.md`:
  zero hits; `commit-runway-read-r53.md`: mentions v7.3 only for the round-53 `mm_init.c` comparison and points
  at the *r53* ledger (:59), never the r54 ledger that holds its rows. A reader of any of the three entries sees
  only `recheck: on-release` and v7.2 quotes — nothing tells them the v7.3 recheck happened. The SOURCES.md
  `used-by` chain runs the other direction (v7.3 rows → ledger). Smallest safe correction: one prose line in
  each entry naming `kernel-v7.3-recheck-r54.md` — safe because `scope()` is frozen at the entering tip and the
  counter does not re-scan entry prose at R.

## 3. Does the line arm add anything a do-nothing control could reach?

Narrowly, yes — but price it honestly.

- The arm is `int(lv) in lines_of(raw, text, offs, q)` (`count-c1.py:331`): the ledger's line must be a line on
  which an occurrence of the quote begins in the pinned v7.3 copy. The `c1 no-line` control (contract readings
  table) shows an all-held ledger carrying v7.2 line numbers fails `line_ok=0` — for the 18 rows whose line
  moved (+45/+84 in memcontrol.c, +31 in the html, +4 in mm_init.c). For the **13 rows marked `+0`** in the
  ledger's own `## Where the quotes moved` table, a lazy relabeler copying the v7.2 line passes the arm
  identically to an honest run — on byte-identical files (10 rows) the arm is a tautology.
- What the arm genuinely buys: it binds each ledger row to the pinned v7.3 bytes at a position — a lazy ledger
  that never opened the copies cannot guess the +45/+84/+31 shifts, so the arm forces the L1's pipeline
  (`controls/c1data.py`, disclosed as the derivation source in the ledger header) to have located each quote
  mechanically. It is a *self-consistency* arm between ledger and pinned copies, not a semantic one —
  `lines_of` accepts any occurrence's line, and `status`/`disposition` still carry all the meaning (counter
  docstring :36-37). Against the strongest control the arm defeats exactly "stale-line relabel on moved rows";
  everything else it touches is ceremony an honest derivation already produces. Worth keeping (it made the
  +45/+84/+31 moves legible), but it must not be narrated as a freshness check on meaning.

## 4. Residual scope edge cases of the scope machine itself (route to round 55, not fixable now)

- `v72_key` recognises four URL spellings of "v7.2" (`count-c1.py:98-106`). A SOURCES row pinning the v7.2 tag
  **by commit hash** (`torvalds/linux/237a1c39e8df…/<path>` — S004 already uses a master-commit URL) yields
  `key=None` and the row is silently outside D even though it pins identical bytes. No claim-table row cites
  such a cell today — latent, not live.
- `v72_key` returns the first *regex* match, not the first URL: multi-URL cells like S127/S148 (`base.c` raw +
  two cgit `?h=v7.2`) map a whole row to one path key. Fine at current scope; a hazard if a multi-URL SOURCES
  row ever feeds a claim table.
- `quota-observability-r48`'s *other* v7.2 pins (S483 mips EDQUOT 1133, S484 sparc EDQUOT 69) live in `recheck:`
  prose lines, not the table — half of that entry's freshness remains at v7.2 with version-frozen commands.
- r51/r52/r45/r12 `recheck:` commands hard-code `v7.2` URLs: they re-verify that the old tag still serves old
  bytes, which always passes. Drift detection lives only in the ledger pattern (r47's `/<tag>/` form, the r53/r54
  ledgers' "fetch each path at the new tag"). Round 55 should normalise the imperative `recheck:` lines to
  `<tag>`-parameterised form or retire them in favour of ledger rows.

## Findings

- **HIGH — F1 (scope residual, named limit, route r55):** four lane artefacts pinning kernel v7.2 bytes carry a
  kernel-release recheck trigger that fired at v7.3 and was not executed: `oom-tracepoints-r47.md` (S475/S476),
  `system-pressure-r24.md` (S090–S095 — its own drift is already recorded in the r54 ledger `## Release drift`),
  `watchdog-identity-r31.md` (S163–S165/S167/S173), `oom-victim-selection-r27.md` (S003/S127/S148). Disclosed as
  out-of-D in contract :55-56, so not a verdict blocker; the SCORECARD `Planned (round 54)` list covered three
  of them and missed r24. Evidence: `git grep 'recheck:.*release'` table above; r47 probe fetch at v7.3
  (exit 0, 8 events, sha256 `82f04ad4…` identical — artefact incidentally correct but unrecorded).
- **MED — F2 (honest-axis debt):** the freshness verdict is table-row freshness only; 10/31 rows sit on
  byte-identical v7.3 files (digests above) so their `held`+`line`+`holds` required no judgement at all. The
  claim's real work is the 21 rows on util.c/mm_init.c/memcontrol.c/cgroup-v2.7.3.html. Name it in the report
  rather than letting `freshness` read as artefact freshness.
- **MED — F3 (discoverability, fixable data):** none of the three rechecked entries names
  `kernel-v7.3-recheck-r54.md` (grep above: r50 0 hits, r48 0 hits, r53 points at the r53 ledger only). A
  reader of a stale-looking v7.2 entry cannot reach its own recheck. Correction: one `rechecked-at:` prose line
  per entry (L1 data fix; counter unaffected — scope frozen at entering tip).
- **MED — F4 (trigger gap):** `disk-write-rate-r33.md:5` rechecks only "when the host kernel moves past 7.2",
  so upstream releases can never trigger it while its S180–S187/S191–S194 pins are tag-frozen. No live consumer
  is wrong today (no tool keys `io.stat`/`delay`); add an upstream-release arm to its `recheck:` or fold its
  anchors into a future ledger.
- **LOW — F5 (version-frozen recheck commands):** `memavailable-estimate-r51.md:9`,
  `overcommit-commit-limit-r52.md:9`, `quota-observability-r48.md:10-11`, the four r12 `recheck:` lines and
  `census-cgroup-levels-r45.md:5` pin `v7.2` inside the command — they pass forever and detect no drift.
- **LOW — F6 (line-arm marginality):** for the 13 `+0` rows the line arm adds nothing over quote presence; its
  discriminating power is confined to the 18 moved rows, where it defeats exactly the stale-line relabel.
  Verdict on the arm: keep, but narrate as ledger↔copy self-consistency, not semantics.
- **LOW — F7 (latent scope blind spot):** `v72_key` sees only four URL spellings of v7.2; commit-hash pins of
  the same bytes and first-regex-not-first-URL multi-URL cells are invisible to `scope()` (no live row today).
- **LOW — F8:** `quota-observability-r48.md`'s mips/sparc EDQUOT values (S483 1133, S484 69 at v7.2) and the
  r24 `memory.pressure`/`io.pressure` access-mode claims are the concrete stale bytes the scope leaves behind;
  r24's are already contradicted in-lane by the r54 ledger's drift note.
