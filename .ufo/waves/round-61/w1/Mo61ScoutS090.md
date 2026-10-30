# Mo61ScoutS090 — v7.2-side source map for the `psi-v73-recheck-r61` ledger frontmatter

Seat: scout (leaf, read-only), 2026-10-30. Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Read: `corpus/SOURCES.md` rows S089–S096 (:95-102), S143–S146 (:149-152), S473 (:252), S520 (:299),
S528–S533 (:308-313); `corpus/knowledge/system-pressure-r24.md` in full; `.ufo/waves/round-61/contract.md`;
`.ufo/waves/round-61/count-c2.py` (PINS :30-37, NAMES regex :38-40, ROW grammar :41-43);
`.ufo/waves/round-61/w1/Mo61ExecFetch.md` (fetch receipts, read for coordination only).
No production file, registry row, or VCS state touched. Findings only — amendments barred.

## 1. The map — per pinned copy

v7.3 twin URL pattern (the lane's established form, used by S519, S521–S523, S528–S533):

    https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/<upstream-path>?h=v7.3

The v7.2 rows use `https://raw.githubusercontent.com/torvalds/linux/v7.2/<upstream-path>`.
S520 (:299) is the rendered-HTML alternative for cgroup-v2 (`https://docs.kernel.org/7.3/admin-guide/cgroup-v2.html`);
it is NOT byte-compatible with the pinned `.rst` copy — ledger quotes must come from the `.rst` bytes (S533's pattern).

| pinned copy (`corpus/evidence/sources-r61/`) | upstream path | v7.2 backing row (non-superseded) | entry frontmatter names | v7.3 twin row | pin sha256 (count-c2.py:30-37) | v7.2→v7.3 bytes |
|---|---|---|---|---|---|---|
| `psi.rst` | `Documentation/accounting/psi.rst` | **S143** (SOURCES.md:149; supersedes S090, anchor-only) | S090 (stale, see F-1) | S529 (:309) | `11c6b7129103b454…b82692` | **identical** |
| `psi.c` | `kernel/sched/psi.c` | S091 (SOURCES.md:97) | S091 | S530 (:310) | `c4edc1e7c18ca76e…85ec63f` | 1 line changed (:1026) |
| `psi_types.h` | `include/linux/psi_types.h` | S095 (SOURCES.md:101) | S095 | S531 (:311) | `483269b27c82b438…b3618ccc` | **identical** |
| `cgroup-v2.rst` | `Documentation/admin-guide/cgroup-v2.rst` | S092 (SOURCES.md:98) | S092 | S533 (:313) | `2750c11a6324e18f…2611b68` | changes start :1133; cited anchors end :1087 — hold |
| `Kconfig` | `init/Kconfig` | **S144** (SOURCES.md:150; supersedes S093, anchor-only) | S093 (stale, see F-1) | **none — no v7.3 row exists** (F-2) | `d37de2a11baf81cb…77e0d` | +6 net lines before :730 |
| `kernel-parameters.txt` | `Documentation/admin-guide/kernel-parameters.txt` | S094 (SOURCES.md:100) | S094 | S532 (:312) | `b5a13c038a27e688…4cb39a` | +35 net lines before :5505 |

Non-pinned registry rows the entry cites (frontmatter `source:` line, system-pressure-r24.md:1):
**S145** (:151; commit 52b1364ba0b1, PSI_IRQ introduction, first shipped 6.1; supersedes S096; mined r28) and
**S146** (:152; man-pages 6.20 carries no proc_pressure(5); supersedes S097; mined r28). Both are registry-backed
but deliberately unpinned; they are not among the six copies and must not be row-bound as copies.
S473 (:252) is a third cgroup-v2.rst v7.2 row (jsdelivr CDN) scoped to the r46 memory.events split —
not a supersession of S092, out of PSI scope.

## 2. Findings (report-only; frozen — no fixes applied)

- **F-1 — entry frontmatter names two superseded rows.** S143's teaches cell: "supersedes S090 —" (anchor-only:
  "reported as zero" wording, SOURCES.md:149); S144's: "supersedes S093 — anchor only: the help-text file list is
  lines 730-731" (SOURCES.md:150). The r24 entry still names S090/S093 in its `source:` line (:1) and its
  `recheck:` line says "re-open S090 and S091" (:3). The non-superseded v7.2 rows for the ledger's provenance
  trio are **S143, S091, S092, S144, S094, S095**. No later row supersedes any of S091/S092/S094/S095/S143/S144/S145/S146/S529–S533 (grep over SOURCES.md, this seat).
- **F-2 — five of six v7.3 twins already have rows; Kconfig has none.** S529–S533 (r55, 2026-10-27, copies under
  `corpus/evidence/sources-r55/`) carry sha256s **byte-identical** to five of the six count-c2.py PINS
  (psi.rst, psi.c, psi_types.h, cgroup-v2.rst, kernel-parameters.txt). But their `used-by` names
  `corpus/knowledge/kernel-v7.3-recheck-r55.md`, not this round's ledger, and C2's target requires "a SOURCES.md
  row **opened this round**, `status=mined`, `used-by` naming the ledger entry" per cited copy. So the data phase
  must append six new rows (contract: "rows S565–S070 appended" — sic, S565–S570); S529–S533 as they stand do not
  satisfy that clause. The Kconfig v7.3 twin (`d37de2a1…`) has **no registry row anywhere** — its pin first
  appears in count-c2.py:35 and the r61 fetch receipt (grep over the lane, this seat); its r61 row is the file's
  first. Sibling seat Mo61ExecFetch already fetched all six at v7.3 with MATCH receipts (Mo61ExecFetch.md:10-11,31-32).
- **F-3 — the two pins equal to v7.2 digests are genuine, not mislabeled.** `psi.rst` and `psi_types.h` pins equal
  the v7.2 S-row digests (S090/S146 record S090's full `11c6b712…b82692`; S095 prefix `483269b27c82b438`). A fresh
  `?h=v7.3` fetch on 2026-10-30 returned byte-identical files (sha256 below), so upstream genuinely did not change
  these two files between v7.2 and v7.3. The ledger can mark every psi.rst/psi_types.h pointer `same` on measured bytes.
- **F-4 — comma-list citations enumerate partially (frozen-counter behavior).** Under the counter's NAMES regex,
  `psi.c:1540,1545,1550,1686` (F3/F9 citations) yields only `psi.c:1540`; 1545/1550 never become pointers; the
  standalone `psi.c:1686` (corrections "Citations (minor)" bullet) does. Total distinct pointers = **47**,
  matching the contract's "floor 40; expected ≈47". Observation only; the counter is frozen.
- **F-5 — advisory verdict pre-computation: 44 same / 3 moved / 0 changed.** All 47 pointers are locatable in the
  pinned copies; the ledger is fully constructible. Moved rows (byte-exact whole-range matches at the new lines):
  `Kconfig:730-731 → 736-737`; `Kconfig:743-760 → 749-766`; `kernel-parameters.txt:5505-5507 → 5540-5542`.
  Independently corroborated by registry anchors written in r55: S532 "psi= parameter line 5540"; S533
  "memory.pressure file 1938" (old :1911-1915 → :1938). Overlapping pointer pairs (psi.c:1282-1288 vs 1284-1288,
  1268-1270 vs 1269-1270 vs 1268, cgroup-v2.rst:1066-1081 vs 1066-1087, psi.rst:67-88 vs 70-88) need pairwise
  distinct quotes — feasible since the ranges differ.
- **F-6 — the single v7.2→v7.3 psi.c change is IRQ-delta guard tightening.** `psi_account_irqtime`:
  `if (delta < 0)` → `if (delta <= 0)` at :1026 (early-return now also on zero delta; diff verified this seat,
  v7.2:1026 vs v7.3:1026). No enumerated anchor cites :1026; all 41 psi.c anchors are byte-identical at the same
  lines. Freshness-relevant one-liner for the ledger prose.
- **F-7 — cgroup-v2.rst changes start after the cited anchors.** First hunk `@@ -1133 +1133 @@`; +21-line
  insertion at :1163; 17 hunks total. The cited anchors :1066-1081 and :1066-1087 (cgroup.pressure, irq.pressure)
  are byte-identical in v7.3.

## 3. Pointer enumeration (counter-identical regex; 47 total)

psi.c 32, psi.rst 9, cgroup-v2.rst 2, Kconfig 2, psi_types.h 1, kernel-parameters.txt 1 = 47 (≥4 copies cited satisfied by all six).

- psi.rst: 60-65, 36-38, 40-43, 45-56, 57-59, 67-88, 102-104, 178-187, 70-88
- psi.c: 342-360, 1268-1270, 1372-1373, 1379-1380, 1712, 1017, 1540, 1686, 1710-1721, 1290-1296, 1282-1288,
  1284-1288, 160-164, 1268, 1269-1270, 600-602, 1273-1296, 1032-1042, 1364-1367, 1717-1719, 1260-1263,
  1257-1258, 228-240, 149-158, 1553-1566, 1711-1719, 167, 1596-1598, 408-410, 845-857, 551, 1538-1550
- psi_types.h: 41-49 · cgroup-v2.rst: 1066-1081, 1066-1087 · Kconfig: 730-731, 743-760 ·
  kernel-parameters.txt: 5505-5507

Every one is byte-identical at the same lines in the pinned v7.3 copies except the three F-5 moved rows.

## 4. r24 claims citing files with NO pinned copy — pointer-for-next-round rows

The entry's own H1 provenance bullet (system-pressure-r24.md:37-41) declares these files "pointers for the next
round, not admitted facts: those files have no registry row this round", covering "F12, the cgroup-code half of
F9, U1's branch location and the mechanism half of U7". Exact pointers, by file (none matches the counter's NAMES
regex, so none can enter ledger rows — they belong in provenance/limits prose only):

- `kernel/sched/sched.h:3492-3495`, `:3518-3521` — U1 irqtime_enabled static branch (:217)
- `kernel/time/sched_clock.c:48-50`, `:242-243` — F12 irqtime boot parameter (:165); frontmatter :1 flags both
  cgroup.c and sched_clock.c as "Supporting reads without registry rows"
- `include/linux/sched/clock.h:112-116` — F12 declarations (:166)
- `kernel/time/Makefile:23` — F12 CONFIG_GENERIC_SCHED_CLOCK (:166); cited but **not** in H1's enumerated list —
  additive note: it equally has no registry row
- `init/main.c:1011,1047,1445` — F7/P2 boot ordering, "no registry row" said in place (:27, :128)
- `arch/x86/kernel/tsc.c:327-328,1544-1545` — F12 x86 TSC (:166)
- `kernel/sched/clock.c:176,243` — F12 unstable-clock disable (:166)
- `kernel/cgroup/cgroup.c:4077-4091`, `:4127`, `:3970-4091` — F9 cgroup-code half (:144-149); `:5585-5589` — U7
  root file presence (:225-226)
- `include/linux/psi.h:39` — root-to-system mapping, "no registry row" said in place (:150, :225-226)

## 5. Verification receipts (this seat, 2026-10-30)

- Disk copies vs PINS: all six `corpus/evidence/sources-r61/*` sha256 == count-c2.py PINS (psi.rst `11c6b712…`,
  psi.c `c4edc1e7…`, psi_types.h `483269b2…`, cgroup-v2.rst `2750c11a…`, Kconfig `d37de2a1…`,
  kernel-parameters.txt `b5a13c03…`).
- Fresh v7.3 fetches (`curl -fsS "$B/<path>?h=v7.3"`, B=https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain,
  into scratch): all six sha256 == PINS byte-for-byte; sizes 6792/48860/5061/135851/76059/319477 B.
  (python-urllib gets HTTP 403 from git.kernel.org; curl works — tooling note for future seats.)
- Fresh v7.2 fetches, same pattern `?h=v7.2`: all six sha256 prefixes match the S-row digests
  (S090 `11c6b712…` full, S091 `452318beaca3e6d1`, S092 `a9433bb0e16a67f0`, S093 `a43f09d89309a6bd`,
  S094 `23b1a690210b6884`, S095 `483269b27c82b438`) — the registry's recorded v7.2 digests verified against upstream.
- Line counts v7.2→v7.3: Kconfig 2321→2368, cgroup-v2.rst 3524→3581, kernel-parameters.txt 8676→8710,
  psi.c 1725→1725, psi.rst 188→188, psi_types.h 216→216.
- Working tree vs entering revision 325f7e639916fcbc77fa2ec7475951a1b86bb1cb (read-only `git show` hash compare):
  system-pressure-r24.md and SOURCES.md byte-identical; count-c2.py absent at that rev (expected — ships in the
  freeze commit 7370a731…).
- Verdict computation: v7.2/v7.3 spans joined and compared byte-exact; moved rows located by exact whole-range
  match search (§2 F-5). Advisory only — the ledger seat's own verdicts govern.
- Disk guard at start: `/fast/scratch/hyaku` 53% use, 378.7G free (green). No pacman, no installs
  (system `python3` 3.14 + `curl` only). Scratch `/fast/scratch/hyaku/mori-r61/Mo61ScoutS090/` cleaned before yield.

## 6. Addendum — cross-checks against the frozen counter and the sibling scribe (2026-10-30, later same round)

Verified from the frozen `count-c2.py` bytes (read this seat, :119-190) and an independent reproduction:

- **F-8 — the counter enforces a 5-word quote floor the contract text does not state.** count-c2.py:151:
  `if not (5 <= wordcount(q) <= 25): failed.append(f"quote_words:{anchor}")`. The contract's C2 target says only
  "every quote ≤25 words, ≥8 distinct bytes". A 5-word floor is real code, unstated in the contract — a frozen
  mismatch, finding-only. ROW.match runs per `splitlines()` line, so a row is one physical line and no quote can
  span a newline; the location check is `q in "\n".join(lines[lo-1:hi])`, so each quote must sit inside ONE line
  of the stated range.
- **F-9 — 14 of the 47 enumerated pointers have no line of ≥5 whitespace tokens anywhere in their range**
  (independent repro over the pinned copies, this seat — set identical member-for-member to
  Mo61ScribePsi1-2's): `psi.c:1268-1270, 1712, 1017, 1540, 1686, 1710-1721, 1268, 1269-1270, 1717-1719,
  1257-1258, 228-240, 1711-1719, 1596-1598` and `psi_types.h:41-49`. These fail `quote_words` on any honest
  `same` row (their content demonstrably did not move or change — §2 F-5), so `C2=met` is unreachable for those
  pointers without recording a false `moved`/`changed`. Reported, not fixed (frozen).
- **F-10 — rows_src makes the six new rows mandatory with exact cell contents** (count-c2.py:182-190): the cited
  copy's SOURCES.md row must contain, on one line, `corpus/evidence/sources-r61/<f>`, `| S`, `| mined |`, and
  `psi-v73-recheck-r61.md`. S529–S533 cite `sources-r55/` paths and name the r55 entry in used-by, so they cannot
  satisfy this check — strengthens §2 F-2.
- **F-11 — psi.c's single v7.3 change (:1026, `delta < 0` → `delta <= 0`) is covered by no enumerated pointer**
  (nearest: :1017 and :1032-1042). The ledger will read "all same" for psi.c while the file did change between
  the pinned tags — a coverage nuance for the ledger prose; corroborated by Mo61ScribePsi1-2 from the committed
  r55 baselines (`corpus/evidence/sources-r55/kernel_sched_psi.c.v7.2` vs `.v7.3`, 1725 lines both, one-line
  diff; no r24 claim falsified — the skipped `rq->psi_irq_time = irq;` update and the implied PSI_IRQ_FULL 0-add
  are no-ops for F5/P3/U7).
- **Byte-identity of psi.rst v7.2 == v7.3 is proven from committed bytes, not only fresh fetches**: the r55
  copies `Documentation_accounting_psi.rst.v7.2` and `.v7.3` are both sha256 `11c6b712…`, 6792 B, empty diff
  (Mo61ScribePsi1-2, verified against my §5 fetches).
- Ledger dry-run seat Mo61ExecLedgerDry-2 had already submitted with no candidate (no anchor-failure list
  produced there); the operative drafts and receipts for the ledger slice are
  `.ufo/waves/round-61/w1/Mo61ScribePsi1.md` (41 rows: psi.rst 9 + psi.c 32, all `same`, provenance naming
  S143/S091). The remaining 6 pointers (psi_types.h 1, cgroup-v2.rst 2, Kconfig 2, kernel-parameters.txt 1 —
  two of them F-5 moved rows) plus the F-9 starved-14 problem belong to the L1's integration decision; this seat
  reports, does not integrate.
