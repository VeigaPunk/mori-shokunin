# ScribeGate — mori round 47, wave w1 report

- Seat: ScribeGate (scribe, godspeed `/skill:godspeed`)
- Lane: mori-shokunin (detection and report only)
- Date: 2026-10-25
- Assignment: draft `corpus/lessons/round-47.md` `## Gate` assimilation block — theme FR13 OOM
  tracepoints from `/home/vgpnk/Projects/shokuknow/merge/mori`; collisions (S471–S474),
  quarantine (S244/S262/S268), admit/reject candidates.
- Report path: `.ufo/waves/round-47/w1/ScribeGate.md` (relative to lane root
  `/home/vgpnk/Projects/shokunin/mori-shokunin`).

## Evidence observed (read-only, all commands exit 0)

- Frozen contract `…/round-47/contract.md` (commit 63eecf2738db96f46b0bd02b1b2dfd66787493d0):
  C2 target entry `corpus/knowledge/oom-tracepoints-r47.md`, new SOURCES row S475, and
  "the committed Linux v7.2 `include/trace/events/oom.h` copy defines eight `TRACE_EVENT`s"
  (contract.md:51–52).
- Collision scratch `.ufo/waves/round-47/assimilation/`:
  - `reg-ids` — registry id list ending S473, S474; contains S471, S472, S473, S474.
  - `staged-ids` — staged list running S471 … S606.
  - `collisions` — exactly four lines: S471, S472, S473, S474.
  - `quarantine-slice` — three rows, all with register prose
    "the cited source could not be fetched, so no quote was checked":
    S244, S262, S268.
- Merge package `/home/vgpnk/Projects/shokuknow/merge/mori/` (read-only):
  - `MERGE-REPORT.md:9` — "lane registry currently holds **243** rows; first staged id is **S471**".
  - `MERGE-REPORT.md:102` — "These staged rows point at a page the lane already has a row for."
  - `MERGE-REPORT.md:111` — maps `S501 | S262 | The kernel's default OOM victim selection has
    **no container context** …"; `:112` maps `S507 | S262 | The OOM lifecycle an observer can hook
    is **named**: mark_victim, start_task_reaping, finish_task_reaping …`.
  - `SOURCES.append.md:37` — staged S501 scope: "the paper's **abstract-level claims as recorded by
    the publisher's own metadata** — the kernel's OOM victim selection lacking container context…".
  - `SOURCES.append.md:43` — staged S507 scope: "the paper's **full text** as deposited by the
    publisher: which OOM tracepoints an eBPF observer can hook…"; anchor quote
    "It leverages eBPF to hook into OOM-related kernel tracepoints such as mark_victim,
    start_task_reaping, and finish_task_reaping".
  - Staged entry `knowledge/corpus/knowledge/oom-tracing-tracepoints-r42.md` (title line 2)
    and Claim lines 12–13: "**The OOM lifecycle an observer can hook has exactly three named
    tracepoints, and the kernel's OOM victim selection has no container context at all.**";
    lines 15–16 lean on the "such as" list above.
- Lane repo state (read-only git):
  - HEAD = freeze `63eecf27`; entering tip `2d85e33d`.
  - `git show 63eecf27:corpus/SOURCES.md` holds S471–S474 (lines 250–253) and 248 registry
    rows total — so the registry already occupied the staged package's first four ids at freeze.
  - Working tree additionally carries (L1 integration in progress) S475, S476, S477 rows in
    `corpus/SOURCES.md` (lines 254–256), untracked `corpus/knowledge/oom-tracepoints-r47.md`,
    and source copies under `corpus/evidence/sources-r47/`.
  - Lane S475 teaches (SOURCES.md:254): "The oom system defines eight trace events and only
    mark_victim carries the victim's comm, uid and memory fields"; anchor TRACE_EVENT at v7.2
    oom.h lines 12, 34, 76, 118, 134, 150, 166, 183.
  - Lane S476 teaches (SOURCES.md:255): "mark_victim is emitted in mark_oom_victim and the
    reaper reports skip, start and finish by pid only".
  - `corpus/evidence/sources-r47/include_trace_events_oom.h` defines 8 TRACE_EVENTs at exactly
    those lines (observed in the committed copy).
  - The drafted entry `corpus/knowledge/oom-tracepoints-r47.md` cross-references the Gate:
    "That headline is refused; see `corpus/lessons/round-47.md` `## Gate`." (entry line 64).
  - `corpus/lessons/round-47.md` does not yet exist (observed via glob), so the `## Gate`
    draft below is the first assimilation block for round 47.

## Gate draft — `corpus/lessons/round-47.md` `## Gate`

```markdown
## Gate

Assimilation theme FR13 (OOM tracepoints) from `/home/vgpnk/Projects/shokuknow/merge/mori`.

**Collisions.** The merge package proposes rows S471–S606 (`MERGE-REPORT.md:9`), while the
freeze registry already holds S471–S474 (`git show 63eecf27:corpus/SOURCES.md` lines 250–253).
Colliding ids: **S471, S472, S473, S474** (`.ufo/waves/round-47/assimilation/collisions`). The
four registry rows stay; no staged row is renumbered onto them. Adopted ids continue at **S475 by
document, not arithmetic** — the next adoptable id comes from the staged package's own row list
(`staged-ids`), not from counting free registry slots.

**Quarantine.** The slice (`.ufo/waves/round-47/assimilation/quarantine-slice`) carries three
rows — S244, S262, S268 — whose register prose is identical: "the cited source could not be
fetched, so no quote was checked". That register text defines the unverifiable-fetch family: a
row whose quote cannot be checked against fetched bytes is not evidence. None of the three is
appended this round — none appears among staged ids (staged run starts at S471), so the family
stays quarantined, including S262, which remains the held ROMA abstract-level row.

**Candidates.**
- Admit (re-grounded): the FR13 OOM-tracepoints theme, via the lane's own **S475/S476** rows,
  realized as `corpus/knowledge/oom-tracepoints-r47.md` (C2 counter re-derives every name, field
  set and call site from the committed copies). S475: "The oom system defines eight trace events
  and only mark_victim carries the victim's comm, uid and memory fields" (`corpus/SOURCES.md:254`;
  TRACE_EVENT at v7.2 oom.h lines 12, 34, 76, 118, 134, 150, 166, 183). S476: "mark_victim is
  emitted in mark_oom_victim and the reaper reports skip, start and finish by pid only"
  (`corpus/SOURCES.md:255`). S477 (host tracefs receipt, own-work) supports the boundaries.
- Reject staged **S501**: scope "the paper's abstract-level claims as recorded by the publisher's
  own metadata — the kernel's OOM victim selection lacking container context"
  (`SOURCES.append.md:37`) duplicates held **S262** — "the paper's abstract-level claims as
  recorded by the publisher's deposited metadata; not the full text" (`corpus/SOURCES.md:243`),
  same DOI 10.1109/TSC.2026.3698682. `MERGE-REPORT.md:102` flags the class: "These staged rows
  point at a page the lane already has a row for."; `:111` maps `S501 -> S262`. Nothing new is
  admitted from it.
- Reject the staged entry text as written (`oom-tracing-tracepoints-r42.md`): headline "The OOM
  lifecycle an observer can hook has exactly three named tracepoints" (`:12-13`) overclaims the
  committed v7.2 header, which defines eight TRACE_EVENTs (contract.md:51–52; copy
  `corpus/evidence/sources-r47/include_trace_events_oom.h`). The paper quote it leans on is a
  non-exhaustive "such as" enumeration: "OOM-related kernel tracepoints such as mark_victim,
  start_task_reaping, and finish_task_reaping" (entry `:15-16`, from staged S507). Staged S507
  therefore backs only the refused text and is not part of the admitted set.

Net: the theme is admitted only re-grounded on S475/S476 (S477 host receipt supports it); staged
S501 and the staged entry text are refused; the quarantine family is untouched.
```

## Tooling authorization record

Nothing installed or upgraded: the task needed only read-only host/git reads, which required no
new tool (no channel used). No `pacman` transaction attempted (guard — all pacman transactions
paused host-wide). No lane tools were run, so no `TMPDIR` scratch directory was needed and
nothing was executed under `/tmp`. No subagents spawned (leaf seat).

## Limits / unverified

- The working-tree SOURCES rows S475/S476/S477 and `corpus/knowledge/oom-tracepoints-r47.md`
  are observed present but uncommitted (L1 integration in progress); my Gate draft does not
  depend on their commit state, only on the freeze registry and the staged package.
- I did not run `count-c2.py` (not this seat's check); the eight-event count is observed directly
  in the committed v7.2 header copy.
