# Mo61ScoutPsiNovelty — PSI-ledger novelty sweep (round 61, read-only)

Question: (a) besides `corpus/knowledge/system-pressure-r24.md`, does anything in
`corpus/knowledge/` already hold v7.3 PSI ground the C2 ledger would duplicate?
(b) what must the new registry rows S565–S570 say to not duplicate S090–S095 and S520?

## Verdict

**Partial overlap — and the brief's named anchors are not the real duplicates.**
- No knowledge entry *other than the two kernel-v7.3-recheck ledgers* holds v7.3 PSI
  ground. All other psi/pressure hits (`surfaces-r7.md`, `surfaces-r8.md`,
  `census-cgroup-levels-r45.md`, `drift-pin-r10.md`, `audit-r11.md`,
  `memavailable-estimate-r51.md:84-86`, `oom-evidence-loss-r38.md:32`,
  `userspace-oom-killers-r26.md`, `harness-job-capacity-r25.md:310`,
  `overcommit-commit-limit-r52.md:58`, `selftest-flake-r9.md:107,213`) are host/tool
  or userspace (systemd-oomd/earlyoom) ground pinned to v7.2 or to non-kernel versions.
- **The real overlap: round 55 already pinned five of the six v7.3 bytes.**
  `kernel-v7.3-recheck-r55.md` re-opened the system-pressure pointers at v7.3 through
  registry rows S529–S533 (`corpus/SOURCES.md:309-313`), all `mined`/`on-release`,
  and its pointer ledger (`kernel-v7.3-recheck-r55.md:24-77`) already carries ~47
  system-pressure-r24.md rows marked `same`/`moved`/`changed`, disposition `holds` —
  at **line-position granularity, with no quotes**.
- The r55 ledger has **zero Kconfig rows** (grep `Kconfig` over that file: no match):
  the S093 anchors `init/Kconfig:730-731` (`system-pressure-r24.md:70`) and
  `init/Kconfig:743-760` (`:127`) were **never rechecked at v7.3**. The r61 Kconfig
  copy is the only genuinely new byte artifact of the six (below).
- `kernel-v7.3-recheck-r54.md:108-113` (and the Leads row `corpus/SOURCES.md:414`)
  already records, from the *rendered* page S520, that `memory.pressure`/`io.pressure`
  are documented **read-write** at 7.3 (7.2: read-only) — explicitly "recorded here,
  not as claims". `kernel-v7.3-recheck-r53.md` holds no PSI ground (resource-runway
  entries only, its coverage-map).
- Context, not an objection: r24's `recheck:` line (`system-pressure-r24.md:3`) names
  only S090 and S091; r55 already discharged that literal trigger at pointer level.
  The r61 ledger's non-duplicative content is: **byte-quote binding** for every one of
  the 47 pointers (control receipt `.ufo/waves/round-61/evidence/control-c2-do-nothing.txt`:
  `pointers=47 … failed=entry_absent rc=1`), the **two never-rechecked Kconfig
  anchors**, and the **raw-RST resolution of the r54 read-write lead** (the r54 note
  is rendered-HTML-only; r55 marked the memory/io.pressure anchors `changed`
  (`:1911-1915→1938-1942`, `:2171-2175→2202-2206`) without quoting the new bytes).

## Byte identity of the six r61 pins (measured 2026-10-30, sha256sum)

| r61 pin (`corpus/evidence/sources-r61/`) | sha256 | byte-equal prior copy | prior row(s) | v7.2→v7.3 delta |
|---|---|---|---|---|
| `psi.rst` | `11c6b7129103…37b82692` | `sources-r55/Documentation_accounting_psi.rst.v7.3` **and** `.v7.2` (identical) | S529 (SOURCES.md:309), S090 (:96) | none — byte-stable across tags |
| `psi.c` | `c4edc1e7c18c…f285ec63f` | `sources-r55/kernel_sched_psi.c.v7.3` | S530 (:310) | yes (S091 v7.2 `452318beaca3…`) |
| `psi_types.h` | `483269b27c82…300b3618ccc` | `sources-r55/include_linux_psi_types.h.v7.3` **and** `.v7.2` (identical) | S531 (:311), S095 (:101) | none — byte-stable across tags |
| `cgroup-v2.rst` | `2750c11a6324…a712611b68` | `sources-r55/Documentation_admin-guide_cgroup-v2.rst.v7.3` | S533 (:313) | yes (S092 v7.2 `a9433bb0e16a…`) |
| `Kconfig` | `d37de2a11baf…67e677e0d` | **none anywhere** (find over `corpus/evidence` for `*kconfig*`: only `sources-r61/Kconfig`) | none | yes (S093 v7.2 `a43f09d89309…`) — **new ground** |
| `kernel-parameters.txt` | `b5a13c038a27…2c94cb39a` | `sources-r55/Documentation_admin-guide_kernel-parameters.txt.v7.3` | S532 (:312) | yes (S094 v7.2 `23b1a690210b…`; psi= moved 5505-5507→5540-5542, r55 row `eee4454705c0`) |

All six r61 pins equal count-c2.py's frozen PINS (`.ufo/waves/round-61/count-c2.py:30-37`).
No `sources-r61` reference and no S565–S570 rows exist in SOURCES.md yet (grep: no match).

## What S565–S570 must say (per-row differentiation)

Counter constraints that shape the rows (verified, not inferred): the registry check
(`count-c2.py:173-182`) requires, for **each cited file**, one SOURCES.md line that
contains `corpus/evidence/sources-r61/<file>`, `| S`, `| mined |`, and
`psi-v73-recheck-r61.md`. The anchor set spans all six files (`NAMES` regex
`:39-40` matches bare filenames, so `init/Kconfig:730-731` counts; `enumerate_pointers`
`:56-63`), so in practice all six rows are needed, not just ≥4.

Registry convention to satisfy: a same-tag byte re-pin must name its prior row and
state the byte identity (precedent S519, SOURCES.md:298: *"byte-identical to v7.2
(same sha256 as S481's copy)"*), not present the bytes as new ground — silent
duplicates are rejected (S560 :340 "repeats S478's … byte hash" → REJECTED;
S564 :344 duplicate scope → REJECTED). Suggested shape, per file (ids in `FILES`
order if appended in that order; L1 assigns):

- **psi.rst row** — scope cell: same v7.3 tag, same URL as S529; note: byte-identical
  to S529's copy (same sha256 `11c6b712…`) **and** to S090's v7.2 copy (file unchanged
  between tags). Role: count-c2.py's own pinned artifact for `psi-v73-recheck-r61.md`
  (used-by cell names the ledger); no interface ground beyond S529/S090.
- **psi.c row** — note: byte-identical to S530's copy (same sha256 `c4edc1e7…`);
  the v7.2→v7.3 delta (S091 `452318be…` ≠ this) is already carried by S530/r55, whose
  rows found all quoted line positions `same`. Role: instrument re-pin for the ledger's
  byte quotes.
- **psi_types.h row** — note: byte-identical to S531's copy and to S095's v7.2 copy
  (`483269b2…` both tags). Role: instrument re-pin.
- **cgroup-v2.rst row** — the crowded one. Must differentiate from **three** prior
  rows: (1) S533 — same tag, same raw-RST URL, byte-identical (`2750c11a…`): say so;
  (2) S520 (SOURCES.md:299) — **different artifact class**: rendered
  `docs.kernel.org/7.3/admin-guide/cgroup-v2.html` (`b478c1bae998…`) vs git-tag raw
  RST; different bytes and different line numbering (r54: rendered page +31 lines vs
  7.2.0 rendering, and none of S520's seven quotes is a raw byte substring of the
  HTML); (3) S092 — the v7.2 raw (`a9433bb0…`, changed). The raw/artifact statement is
  what licenses the ledger's raw-byte quotes (e.g. the `changed` rows at
  `:1938-1942`/`:2202-2206` where the read-write wording becomes byte-citable).
- **Kconfig row** — the only **genuine new-source admit** of the six: no prior v7.3
  row or copy exists; bytes changed vs S093 (`a43f09d8…` → `d37de2a1…`). Scope cell:
  CONFIG_PSI / CONFIG_PSI_DEFAULT_DISABLED / CONFIG_IRQ_TIME_ACCOUNTING at v7.3, with
  the delta vs S093 named. The ledger's rows for `Kconfig:730-731` and `:743-760` are
  first-ever v7.3 checks of those anchors (r55 skipped them); their same/moved/changed
  verdicts must be derived from this copy.
- **kernel-parameters.txt row** — note: byte-identical to S532's copy (`b5a13c03…`);
  psi= movement 5505-5507→5540-5542 already held (r55 row `eee4454705c0`). Role:
  instrument re-pin.

Ledger framing (not a row requirement): rows re-stating r55's `same` verdicts should
be framed as quote-level binding of pointer ground r55 holds at line level — the new
facts are the byte quotes themselves, the two Kconfig anchors, and the raw-RST
read-write resolution of the r54 lead.

## Findings (report-only; amendments barred)

1. **Five of six planned S565–S570 rows are same-tag byte re-pins of S529–S533**, not
   new sources. If written as fresh admits without naming S529–S533 and the shared
   sha256s, they violate the registry's own duplicate precedent (S560/S564) — that is
   the falsifiable exposure of C2's SOURCES side. The counter itself does not catch it
   (its registry check `:173-182` matches any one line containing the copy path +
   `mined` + ledger name, even a *pre-existing* S529–S533 line augmented in place —
   which would also satisfy it; only honest new rows keep the append-only shape).
2. **The freshness axis is thinner than "never rechecked"**: psi.rst is byte-identical
   v7.2→v7.3 and psi_types.h likewise, so "re-open at v7.3" for those two is
   demonstrably a no-op at byte level (r55 already said `same`). C2's real new ground:
   Kconfig anchors, byte quotes for all 47 pointers, raw-RST read-write wording.
3. No other knowledge entry claims v7.3 PSI ground (verdict above), so no *entry*-level
   duplication exists; the overlap is registry/ledger-level only.

## Provenance

- Read-only seat: zero git/jj commands, zero writes outside this report; no scratch
  dir created (single `sha256sum` pass over `corpus/evidence/sources-r{55,61}/*`), no
  TMPDIR usage, nothing to clean. No tools installed (RULES.md authorization unused).
- Registry-cell extraction: Python parse of `corpus/SOURCES.md` rows S090–S095, S520,
  S529–S533 (sha256 cells and tail cells quoted above verbatim).
- Key line refs: SOURCES.md :96-101, :298-299, :309-313, :340, :344, :353, :409-414;
  kernel-v7.3-recheck-r55.md :24-77; kernel-v7.3-recheck-r54.md :108-113;
  system-pressure-r24.md :3, :70, :110, :127, :143; count-c2.py :26-43, :56-63,
  :173-182; evidence/control-c2-do-nothing.txt.
