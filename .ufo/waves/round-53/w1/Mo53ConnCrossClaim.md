# Mo53ConnCrossClaim — the carrier is not the claim: one gap shape across C1, C2, and the lane's remaining surfaces

Scope: cross-claim pattern only. Reads at the data commit `2a4213bf8da72f7cd78189baa5bb9be825dca1df`
(`contract.md`, `count-c1.py`, `count-c2.py`, both new entries, `corpus/QUALITY.md`, every
`corpus/knowledge/*` `recheck:` line, `tools/mori-census.sh` source, `PROVINCE.md`, `corpus/README.md`,
`sources-r53/` listing, `w1/Mo53ScoutRunwayTools.md`). One live fetch: `mm/mm_init.c?h=v7.3` from
git.kernel.org cgit into scratch `/fast/scratch/hyaku/mori-r53/Mo53ConnCrossClaim/` (removed on exit).
Machine id written MACHINE_ID. This report carries no line starting with the RECHECK or QUOTE words.

## 1. The shared principle

**The carrier is not the claim — the meaning rides a separate structure, and a correct lane keeps that
second structure explicit.**

- **C1 shape — a pinned quote is not the claim.** The counter derives `held` mechanically: the v7.2
  words still occur, whitespace-collapsed, *somewhere* in the v7.3 file (`count-c1.py` docstring limits:
  "proves the words still occur somewhere in the v7.3 file, not at the same place nor with the same
  meaning"). The meaning lives in two added structures the quote cannot carry: the `disposition`
  column (`holds`/`changed`, the L1's reading) and the ≥2 per-row RECHECK votes that ratify or reject
  that reading (`contract.md` P-C1). The two `absent` rows — `0fbd62f51ce8`, `d7a1dc88dcb3`, both
  `mm/mmap.c` `MAP_NORESERVE` — are the live proof: v7.3 respelled the flag write
  (`vma_flags_set(&vma_flags, VMA_NORESERVE_BIT)` for `vm_flags |= VM_NORESERVE`), so the quote arm
  *fails* while the disposition arm still says `holds`. A gate that trusted the located quote alone
  would call both rows `changed` — the opposite of the voted truth.
- **C2 shape — a printed number is not the enforced number.** `/proc/meminfo` prints `CommitLimit`
  under every mode; it is *enforced* only under mode 2 (`overcommit-commit-limit-r52.md:18`). The
  meaning again lives in added structures the print cannot carry: `mode`, `enforced`,
  `single_request_cap_kb`, and under mode 2 the `band_kb`/`usable_kb` pair — `COMMIT_LOW` is "inside
  the per-CPU counter's own error band", not a threshold crossing (`tools/mori-commit-runway.py:31-38`,
  `commit-runway-read-r53.md` mode table). On this host (mode 0, Committed_AS 47583772+ kB above the
  printed limit) the printed numbers show a deficit; the enforced reading is
  `COMMIT_HEURISTIC`/`over_limit_not_enforced`. A gate that trusted the printed pair alone would raise
  a false LOW on the host's normal state — exactly what the `mode-blind` control measured
  (`agree=53 disagree=27`, `evidence/control-c2-mode-blind.txt`).

Same pattern, two carriers: quote-location for text, field-value for numbers. In both, the artifact's
contents are *evidence*; the *claim* is the judgment layer on top (disposition+votes; mode+band+verdict).

## 2. QUALITY rows that already state part of it

| row | states which half | pointer |
|---|---|---|
| Q14 | a counter's semantics cite its increment site, not documentation wording — printed/doc text is not the mechanism | `QUALITY.md` round-12 rows |
| Q15 | journal class counted by structured field, never by message text — the printed `MESSAGE` is not the record's identity | QUALITY round-12 rows |
| Q34/35 | a raw class token ≠ validated-positive token; a valid empty capture is a real 0, never "no event" — the printed tally is not the validated set | `QUALITY.md:82-89` |
| Q71 | accounting-active evidence does not prove runtime enforcement — printed/active ≠ enforced | `QUALITY.md:296-306` |
| Q76 | a stale receipt's tally is never a pass "because its number looks right" — the printed tally is not the measured run | `QUALITY.md:340-348` |
| Q108 | a binding is checked for resolvability, not token presence; README row: "an anchor proves presence in the bytes, not semantics" | `QUALITY.md:872`, `corpus/README.md:599` |
| Q128 | "a located quote per claim, and the counter proves location, not entailment" | `QUALITY.md:1079-1087` |
| Q132 (+journal-reach-r49) | counter locates quotes, "does not entail"; a number matching a receipt is not thereby true today | `QUALITY.md:1150-1157` |
| Q139 | a runway reading is `MemAvailable`, never rebuilt as `MemFree + Cached`; "MemAvailable is itself a model… a threshold on it is a threshold on an estimate" — the printed field is a model, the verdict must name it | `QUALITY.md:1308-1327` |
| Q140→Q143 | the ENTAIL vote layer: location never proves the claim follows; two non-writer votes carry the entailment, `overclaim` blocks | `QUALITY.md:1329-1352`, `:1379` |
| Q142 | a self-assessment pointer lands on the words it reports — a pointer is not the pointed-at text | `QUALITY.md:1368-1377` |

So the lane already enforces the principle *inside single claims* (quote+vote, tally+receipt,
printed+structured). C1/C2 extend it one level up: the *freshness* of the claim layer itself needs the
same split — a still-locatable quote or a still-printable number is not a still-true claim.

## 3. Surfaces where the same gap is still open

| # | surface | the open gap | pointer | status |
|---|---|---|---|---|
| 1 | `oom-tracepoints-r47.md` | `recheck: on-release` fired at v7.3, unanswered — the C1 ledger's D covers only the two table entries, so this whole entry's eight-event catalogue stays un-rechecked. Same gap *inside* the entry: `TP_printk` printed labels (`total-vm=`, `:`/ `=` separators) are not the `TP_STRUCT__entry` field names — a parser keyed on printed text reads the wrong names | `oom-tracepoints-r47.md:5,33-36`; ledger boundary `:107` | trigger live, dormancy admitted (MED) |
| 2 | `oom-victim-selection-r27.md` | `recheck: on a kernel release re-open fs/proc/base.c proc_oom_score and mm/oom_kill.c oom_badness` — v7.3 fired, unanswered | `oom-victim-selection-r27.md:3` | trigger live (MED) |
| 3 | `quota-observability-r48.md` | two `recheck: on-release` rows re-fetch the *v7.2* bytes — the recipe re-proves the pin is fetchable, not that the claim holds at the new tag: the carrier check again, no meaning layer | `quota-observability-r48.md:10-11` | trigger live; recipes check the wrong object (MED) |
| 4 | `conform-scope-r40.md:7`, `source-drift-r36.md:3` | bare `recheck: on-release` names no release — for a Python-docs and a CORPUS-rule source the trigger is ambiguous (kernel tag? docs release? a CORPUS edit?) | both files' `recheck:` lines | ambiguous trigger (LOW) |
| 5 | `kernel-oom-line-attribution-r12.md:3`, `oom-kill-counter-kernel-only-r12.md:3` | v7.2-pinned recheck greps with no release trigger at all — stale only when the host's kernel line moves; today host runs 7.2.11 so dormant, not wrong | both `recheck:` lines | dormant (LOW) |
| 6 | `oom-memcg-stat-r50.md` | `recheck: 90d` on v7.2-pinned URLs — cadence guards freshness of the *fetch*, not the claim's truth on a post-7.2 host; same class C1 fixed for tables (host-pinned, correct today) | `oom-memcg-stat-r50.md:7` | dormant (LOW) |
| 7 | `journal-disk-usage-total-r51.md` / `journal-reach-r49.md` | `--disk-usage` prints a total "over the files that invocation can see", not a per-journal bound or vacuum ceiling; no lane tool reads it (grep over `tools/` → 0 hits), so the gap is a reader-hazard, not a gate | `journal-disk-usage-total-r51.md:8`; scout §1 | open, reader-facing (LOW) |
| 8 | `mori-census.sh` commit-ledger blind spot | census reads MemAvailable but has zero reads of `CommitLimit`/`Committed_AS` (scout §1-2); C2 closes it for the tool surface. The fleet's hyaku gates (`scripts/hyaku/inline-dispatcher.py`, `wave-slot.sh`, fleet-owned) also read MemAvailable only — the mode/band reading exists for the lane but no gate consumes the verdicts; FR8 stays open by design | `mori-census.sh:1791-1796`; `memavailable-estimate-r51.md:14` | lane half closed by C2; consumer half open (LOW) |
| 9 | `MEM_AVAIL_LOW` warn (`mori-census.sh:1796`) | the *correctly-handled* instance of the pattern — a warn on a kernel estimate, `threshold_label=local` names the model layer. Cited as precedent, not a gap | QUALITY 139 | handled |
| 10 | the release trigger itself | v7.3 was noticed by a hand-run `git ls-remote` (`evidence/sweeps.txt:16-19`); no lane instrument watches kernel tags or enumerates `recheck: on-release` rows — rows 1-3 above are the evidence. The C1 ledger proves the workflow (fetch → locate → disposition → votes) but nothing schedules it | `evidence/sweeps.txt`; `grep -rn 'recheck:' corpus/knowledge/` | systemic, open (MED) |
| 11 | `commit-runway-read-r53.md:49-50` — data nit | says the batch rule "is unchanged at v7.3 (`mm_compute_batch` in the v7.3 copy differs only by its line number)". No v7.3 copy of `mm_init.c` is committed (`sources-r53/` holds `mm_init.c.v7.2` only — `ls` output below); the pointer names a copy that does not exist in the lane. The *claim* verifies: I fetched `mm_init.c?h=v7.3` (sha256 `67841000…f976c`, 76467 bytes), `mm_compute_batch` moved `:191→:195` and its body diffs empty against the v7.2 copy | `commit-runway-read-r53.md:49-50` | claim true, pointer names no committed copy (LOW — data still correctable by the L1: land the v7.3 copy or reword "the v7.3 fetch") |

## 4. Frontier draft (for the L1 / frontier seat — not a committed edit)

A synthesis that improves the freshness axis without spending another axis: **give `on-release` a
scheduler and a scope rule**, so the carrier/meaning split survives the next tag for every entry, not
just the two table entries.

```text
Draft QUALITY row (round 54 candidate):
  An `on-release` recheck is a sweepable trigger with a named release, and its sweep covers every
  entry carrying the marker, not one claim's scope. When a kernel tag lands, one sweep lists every
  `recheck: on-release` row in corpus/knowledge and corpus/SOURCES.md and each row is dispositioned:
  rechecked (with the disposition layer C1 used — located quote plus a holds/changed judgment), scoped
  out with a reason (host-pinned, non-kernel source), or carried as named debt. A recipe that re-fetches
  the old tag's bytes proves the pin is reachable, never that the claim holds at the new tag.
  Ground: round-53 — v7.3 fired the marker on ≥6 entries; the C1 ledger dispositioned 46 rows of two;
  oom-tracepoints-r47, oom-victim-selection-r27 and quota-observability-r48 stayed unanswered, and the
  quota rows' recipes re-check v7.2 bytes (the carrier), not the claim at v7.3 (the meaning).
  Check sketch: `grep -l 'recheck: on-release' corpus/knowledge/*.md` ⊇ the ledger's scope; a round's
  sweep receipt names each row's disposition.
```

Companion routed item for round 54: extend the ledger shape (status + disposition + votes) to the
non-table entries (tracepoint catalogue, victim-selection call sites, quota errno rows) the next time a
release fires — the mechanics are proven; only the scope `D` was narrow by design.

## 5. Verification log

- `sed -n` / `grep` reads of the files in §scope — all at `2a4213bf` working tree; lane untouched.
- `ls corpus/evidence/sources-r53/` → 12 files: nine `*.v7.3` C1 copies + `mm_init.c.v7.2`,
  `percpu_counter.c.v7.2`, `percpu_counter.h.v7.2`. No `mm_init.c` at v7.3.
- `curl -fsSL 'https://git.kernel.org/…/plain/mm/mm_init.c?h=v7.3'` → 76467 bytes, sha256
  `678410005f881a64ae94d180c82174dc4474679b056ace69b6bc3d23978f976c` (fetched to scratch, deleted).
- `diff` of `mm_compute_batch` body, committed v7.2 copy (`:191-211`) vs fetched v7.3 (`:195-215`) →
  exit 0, identical text; surrounding diff shows the function shifted +4 lines and a top-of-hunk
  `#ifdef CONFIG_SMP / vm_committed_as_batch = 32` block moved. Entry's "differs only by its line
  number" verified TRUE for the rule; the word "copy" names an uncommitted file.
- `grep -c '^TRACE_EVENT(' corpus/evidence/sources-r47/include_trace_events_oom.h` → `8` (matches the
  r47 claim's own mechanical check).
- `grep -rn 'CommitLimit\|Committed_AS' tools/` → only `mori-commit-runway.py` (+fixtures); census has
  zero reads (scout report §1-2 agree).
- `grep -rn 'recheck:.*on-release' corpus/knowledge/` → 10 hit lines across 8 entries (listed in §3).
- Disk guard: `/fast/scratch/hyaku` 25 % used, 607 G free before the fetch; scratch removed after.
- No installs, no writes outside this report and scratch, no journal MESSAGE greps, no host mutations.

UNVERIFIED: whether any *other* lane surface consumes `COMMIT_*` verdicts (fleet hyaku scripts were
greped for `Committed_AS` → 0 hits, but their full input list was not audited); whether the v7.3
`proc.rst`/`vm.rst` diffs touch only the lines the ledger table names (a wave sibling's job).

## Findings

- **MED** — `oom-tracepoints-r47.md:5` and `oom-victim-selection-r27.md:3`: `on-release` triggers fired
  at v7.3, unanswered; the C1 ledger's scope D covers only the two table entries, so the release-recheck
  pattern is claim-scoped, not marker-scoped (§3 rows 1-2).
- **MED** — `quota-observability-r48.md:10-11`: `on-release` recipes re-fetch v7.2 bytes — they re-prove
  the carrier is reachable, not that the claim holds at v7.3; same carrier/meaning confusion the C1
  disposition layer exists to catch (§3 row 3).
- **MED** — no lane instrument watches kernel tags or enumerates `on-release` markers; v7.3 was noticed
  by a hand-run `git ls-remote` (`evidence/sweeps.txt:16`). The ledger workflow is proven but unscheduled
  (§3 row 10; draft fix in §4).
- **LOW** — `commit-runway-read-r53.md:49-50` says "the v7.3 copy" of `mm_init.c`; no such copy is
  committed under `corpus/evidence/sources-r53/`. The underlying claim verifies independently (fetched
  v7.3 file, function body byte-identical, moved :191→:195) — correctable data nit, L1's call
  (land the copy or reword).
- **LOW** — `conform-scope-r40.md:7`, `source-drift-r36.md:3`: bare `recheck: on-release` names no
  release; trigger ambiguous for non-kernel sources (§3 row 4).
- **LOW** — census and the fleet's hyaku gates read `MemAvailable` only; nothing consumes the new
  `COMMIT_*` verdicts, so the printed-vs-enforced reading exists but has no gate consumer yet — by
  design this round (FR8 open), recorded as the open half of the C2 pattern (§3 row 8).

Report: .ufo/waves/round-53/w1/Mo53ConnCrossClaim.md
