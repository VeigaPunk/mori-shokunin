measured 2026-10-23T12:05:15Z
# Round 36 SKILL.md additions — draft only

Axes: freshness (C1) and operability (C2); the index-clean registry row is the routed round-35 repair. The requested additions are drafted below; `SKILL.md` was not edited.

## Decision

VERDICT: source drift is a `probe`, not a `gate`.

C1 fetches mutable URLs live. Its contract classifies failed GETs as `unavailable`, but exits 0 whenever `drifted=0`; therefore even an all-unavailable run can exit 0 and cannot establish freshness. The stored source copy is a comparison reference, but it does not make the external fetch reliably evaluable. This follows the distinction in PROTOCOL §Gate standard: a gate returns a re-runnable verdict against persisted expected values; the probe registration avoids treating unavailable observations as clean. Sources: `.ufo/waves/round-36/contract.md:35-47`; `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:388-401`.

## DRAFT SKILL.md — registry rows

Append these rows to the existing `## Gates` table without editing existing lines (table header at `SKILL.md:162`, existing first row at line 164):

```DRAFT SKILL.md
| source drift (r36 C1) | probe | `python3 tools/mori-source-drift.py --root <repo>` | 0 `drifted=0` (may include `unavailable` or `no-copy`; not proof every URL was checked) · 1 `drifted>0` · 2 could-not-evaluate (missing/unreadable `SOURCES.md`) | `python3 tools/mori-source-drift.py --selftest` | `corpus/evidence/sources-r<N>/<id>.<ext>`; highest integer N per id is compared; fetched URL content is live | none live (read-only per C1 contract); self-test scope unobserved | mori |
| SOURCES append-only (r36 C2) | gate | `python3 tools/mori-sources-appendonly.py <rev> [--repo DIR] [--round-base REV] [--path P]` | 0 no selected-scope violation (without `--round-base`: no `ids`/`deleted`; with it: no `round_changed`) · 1 violation (without it: `ids` or `deleted`; with it: `round_changed`) · 2 could-not-evaluate (error) | `python3 tools/mori-sources-appendonly.py --selftest` | Git history for `corpus/SOURCES.md` at `<rev>`; `--round-base` bounds `round_changed`; no separate expected-values file | none live (read-only Git per C2 contract); self-test scope unobserved | mori |
| index clean (r36) | gate | `bash tools/mori-index-clean.sh <repo>` | 0 clean · 1 failed (staged or intent-to-add entries) · 2 could-not-evaluate (error) | `bash tools/mori-index-clean.sh --selftest` | target repo's Git index; expected state is no staged or intent-to-add entries | no target-index writes expected; self-test scope unobserved | mori |
```

The source-drift verdict map preserves the contract's exact exit predicate; it deliberately does not call rc0 `clean`. The append-only row preserves the distinct `--round-base` exit rule. The C2 entry is drafted as the registered replacement for `.ufo/waves/round-35/check-sources-appendonly.py`, as requested; the round-36 contract identifies the round-35 checker in its QUALITY control at `.ufo/waves/round-36/contract.md:101`.

## DRAFT SKILL.md — section

Append this section after existing SKILL.md content; it does not alter prior text:

```DRAFT SKILL.md
## Round36 — source drift and append-only gates

Round36 source drift is a probe, not a clean gate: `python3 tools/mori-source-drift.py --root <repo>` fetches copied-source URLs live. `unavailable` is not `drifted`, and rc0 only says `drifted=0`; it does not prove every source was reachable (`.ufo/waves/round-36/contract.md` §C1).

For the registered append-only check, run `python3 tools/mori-sources-appendonly.py <rev> [--repo DIR] [--round-base REV] [--path P]`. It reports edited and deleted ids; `--round-base` additionally checks changes in that revision range. This registered tool replaces the round-35 wave checker `.ufo/waves/round-35/check-sources-appendonly.py` (round-36 assignment; see the prior-checker control at `.ufo/waves/round-36/contract.md:101`).

For index cleanliness, run `bash tools/mori-index-clean.sh <repo>`: rc0 means clean, rc1 means staged or intent-to-add entries, and rc2 means error. Each tool's `--selftest` is listed in the Gates registry above.
```

## Evidence, surfaces, and limits

- Registry shape and the current rows were read at `/home/vgpnk/Projects/shokunin/mori-shokunin/SKILL.md:156-164`; relevant style examples were read at `SKILL.md:772-782` and `SKILL.md:826-834`. Draft rows follow the existing eight-column header at line 162.
- C1 interface and exit predicate were read from `.ufo/waves/round-36/contract.md:33-47`; C2 interface and conditional exits from `:60-77`. Gate/probe and registry requirements were read from `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:388-416`.
- Reads of `tools/mori-source-drift.py`, `tools/mori-sources-appendonly.py`, and `tools/mori-index-clean.sh` each returned `Path ... not found`. Thus no implementation, self-test, pinned value beyond the cited contract/task, or actual write scope was verified. `self-test scope unobserved` is explicit in the rows; the index write-scope wording is a proposed expectation, not observed behavior.
- No implementation command, network fetch, self-test, build, or other check was run. No tools were installed. The only shell command was `timeout 5s date -u +%FT%TZ` → `2026-10-23T12:05:15Z`.
- Only this scoped report was written: `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/w1/DraftSkillRows.md`. No SKILL.md or product code was changed; no out-of-scope surfaces were touched.
