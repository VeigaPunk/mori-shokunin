measured 2026-10-23 (probe run at lane tip bf0df77fee4b6ef54a90aea09335c7617f125151)

# RevKnowledgeDrift — knowledge-note quality review, round 36 wave 2

Seat: `mori-r36-w2-RevKnowledgeDrift-17` (leaf; no subagents). Item attacked:
`corpus/knowledge/source-drift-r36.md` against the fleet `CORPUS.md` rules — provenance
trio first, every count carries its command, falsifiable state table, no universal
claims, no credential material; plus any place that infers a freshness verdict from C1.
Lane untouched (read-only git queries, the lane's own read-only probe, its `--selftest`,
and two plain `curl` fetches for the anchor/drift characterization). Installs: none.
Scratch: `/fast/scratch/hyaku/mori-r36/RevKnowledgeDrift/` (pinned CORPUS.md fetch,
live_S210.html, live_S211.html). Writes: this report only. No LSP server applies to
corpus markdown prose; contract/behavior checks used `read`/`grep` plus a fetch of the
pinned source — the recorded fallback.

## Checks that held (each with its evidence)

1. **Provenance trio first — holds.** `corpus/knowledge/source-drift-r36.md:1-3` opens
   with `source: S205 — fleet CORPUS.md …` (S### row + URL + anchor),
   `verified-at: 2026-10-23`, `recheck: on-release`.
   Anchor re-derived: `curl -sS https://raw.githubusercontent.com/VeigaPunk/shokunin/6a1dd8ce1a3165a25f9f2b774b21449e0d125c94/CORPUS.md`
   → sha256 `88556402940e7a0f1dbbed3abef9e00c87a90db6f80eaed03269e371f50050b8`, 184
   lines; `diff /home/vgpnk/Projects/shokunin/CORPUS.md <fetched>` → `IDENTICAL`.
   Lines 105-106 are the `recheck` — ISO date or cadence bullet; lines 116-118 are
   rule 2 (Append-only). The note's `CORPUS.md:105-106,116-118` citations are exact
   against the pinned commit. `corpus/SOURCES.md:211` carries S205 (docs, tier A, same
   anchor, status `mined`, opened 2026-10-23).
2. **Interface and state claims match the tool.** Verified against
   `tools/mori-source-drift.py`: first `http(s)://` URL of the source cell with trailing
   `.,;)` stripped (`:68-72`), newest-N copy selection (`:75-96`), redirect-following
   with 429 Retry-After / 5xx retries (`:113-136`), `classify` fresh/excerpt/drifted
   (`:139-145`), per-row `<id> <state>` + `MORI_SOURCE_DRIFT rows=…` summary, exit 0/1
   (`:157-203`), exit 2 setup (`:169-174`), read-only (no writes under DIR),
   `--selftest` offline fixture on 127.0.0.1 (`:234-263`). Exercised:
   `python3 tools/mori-source-drift.py --selftest` →
   `MORI_SOURCE_DRIFT_SELFTEST: PASS (4 cases)`, `SELFTEST_EXIT=0`.
   `SKILL.md:872` registers it as type `probe` — the note's "probe, not a gate" holds.
3. **No freshness-admission inference.** Note `:15-16` disclaims it explicitly
   (`fresh` proves only byte identity … never that the row's `teaches` is right) and
   `:13` keeps the recheck duty. Nothing in the note derives a freshness verdict from
   C1=met. The README:565 "freshness technique" label matches the declared exploratory
   framing, not an admission. This attack found nothing.
4. **State table falsifiable.** Every meaning cell is mechanically checkable against
   `classify`/`run`; every reader action is imperative with a resolving object. One
   completeness gap only (F3).
5. **No credential material**, no `op://`, no session/private URLs in the note.
6. **Index row exists for the file**: `corpus/README.md:565` (rule "an index row is a
   claim" — written when the file exists).
7. **Round-36 copies exist as described**: `ls corpus/evidence/sources-r36/ | wc -l`
   → 16 (`S205.src`–`S220.src`); heads are raw bodies (S205.src begins `# Shokunin
   Corpus Contract`, S207.src begins `<!doctype html>`), matching note `:30`.

## Findings

### F1 — HIGH — number-drift: the "seven drifted rows" enumeration is false at the revision the note landed in (drives the verdict)

- Claim, `corpus/knowledge/source-drift-r36.md:15-19`: "That is not the same as a
  changed source: on 2026-10-23 the **seven** `drifted` rows were **five** annotated
  excerpts from round 30 (S156–S160 …) and **two** docs.python.org pages whose only
  change is the build footer (S176, S177)". No command accompanies any of these counts —
  only citations to `.ufo/waves/round-36/w1/MineCopyFidelity.md` and
  `w1/CritAxisFit.md`. CORPUS.md ("A count carries its command") requires
  `<number> — <command> <date>`; the form is violated independently of the value.
- Re-derivation at the landed tip (the note is committed in bf0df77:
  `git log -1 -- corpus/knowledge/source-drift-r36.md` → `bf0df77 2026-10-23 09:09:14 -0300`;
  `git diff --name-only 6bd57097..bf0df77 -- corpus/` lists it with SOURCES.md).
  Command: `python3 tools/mori-source-drift.py --root .` (lane root, bf0df77, 2026-10-23).
  Observed: per-row lines end with
  `S156 drifted S157 drifted S158 drifted S159 drifted S160 drifted … S176 drifted
  S177 drifted … S210 drifted S211 drifted …` and
  `MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162`,
  `EXIT=1`. **Nine drifted rows, not seven.**
- The tip receipt already contradicts the note:
  `.ufo/waves/round-36/evidence/c1-after.txt:2` — `real_rows=220 oracle_fetched=58
  oracle_fresh=49 oracle_drifted=9 oracle_excluded=0 tool_exit=1 tool_rows=220
  mismatches=0` (produced after the data commit per the round taskcall; the file has no
  commit touching it — it is the worktree receipt at the tip). My independent run
  reproduces its tallies exactly (fresh=49, drifted=9).
- The w1 evidence the note cites supports 7 only at the **entering** revision:
  `.ufo/waves/round-36/evidence/c0-rescore-v2.txt` REF1 real arm at 6bd57097 —
  `real_rows=204 oracle_fetched=42 oracle_fresh=35 oracle_drifted=7 … mismatches=0` —
  and MineCopyFidelity (measured ~12:05Z) swept exactly S156–S160, S176, S177 plus
  three tag-pinned rows. The note promotes that w1-revision snapshot to a standing
  "on 2026-10-23" fact, omitting the 16 rows the round itself appended.
- The two unlisted rows drift for causes outside the note's enumeration (both copies
  saved 2026-10-23 09:11 as raw curl bodies; each URL fetched once today):
  - **S210** (`git-scm.com/docs/git-rev-parse`; supersede row for the round-35 debt):
    `cmp corpus/evidence/sources-r36/S210.src live_S210.html` → `differ: char 899,
    line 36`. Copy: `<link rel="stylesheet" href="/application.min.c863b1ec….css"
    integrity="sha256-yGOx7KEhe2wNSj…">`; live: `href="/application.min.ee050e66….css"`
    with no integrity attribute. Site redeploy churn (asset hash + dropped SRI), not an
    annotated excerpt and not a docs.python build footer.
  - **S211** (PMC mirror `PMC5856500`, the S179 supersede row):
    `cmp … S211.src live_S211.html` → `differ: char 4004, line 77`. Rotating per-request
    server id: copy `ncbi_phid content="C1EDB38EADB4834310B38E0043536AD6.m_1"` vs live
    `content="E73CD8FDADBA8F2310D8FD00267D98E7.m_1"`. Dynamic-content churn, likewise
    outside the note's two named causes.
- Both causes are benign w.r.t. the *documented content*, which makes the defect a
  stale exhaustive enumeration rather than a missed incident — but the note's doctrine
  is exactly that a reader can enumerate the drifted set and act per row. A reader at
  the tip gets nine rows and the note explains seven.

### F2 — MEDIUM — provenance back-link broken: S205.used-by omits the citing knowledge entry and names a path that does not cite S205

- `corpus/SOURCES.md:211`: `status=mined`, `used-by=tools/mori-source-drift.py`.
- Contract (CORPUS.md, SOURCES shape): `used-by` — "repo-relative paths of the
  knowledge entries or lessons citing the row, comma-separated, or `—`"; `mined` —
  "cited by ≥1 path in `used-by`".
- `grep -n "S205" tools/mori-source-drift.py` → no match; the tool's docstring cites
  the knowledge note (`corpus/knowledge/source-drift-r36.md`), not the row. The actual
  citing entry (`source-drift-r36.md:1`) is absent from used-by, and the cell's single
  entry is a tools path, which the cell definition does not allow (compare S206/S207,
  which list `corpus/knowledge/…` paths). On its face the row's `mined` status is not
  justified by its own used-by cell. Adjacent-file defect surfaced by verifying the
  note's S205 citation; record it in the round lesson with the old→new used-by value
  (append-only permits exactly this in-place change).

### F3 — LOW — the exit-2 meaning cell is a strict subset of the tool's exit-2 causes

- Note `:10-11` and the `exit 2` table row (`:28`): "2 when `SOURCES.md` is missing or
  unreadable; no verdict" → action "Restore `DIR/corpus/SOURCES.md` and run … again".
- The tool also exits 2 on bad usage and a non-directory `--root`
  (`tools/mori-source-drift.py:365-374`; docstring `:26-27` says "bad usage").
  Observed: `python3 tools/mori-source-drift.py .` → `usage: … --root DIR | --selftest`,
  `EXIT=2`. The restore advice is wrong for those cases. Milder sibling: an unreadable
  copy file also classifies `no-copy` (`:157-163`), which the `no-copy` row (`:27`)
  does not name.

Observation (no FAIL weight): note `:30-31` says round-36 copies "classify `fresh` or
`drifted` by content alone"; `classify` also has a reachable `excerpt` branch for such
copies. Harmless today (run shows `excerpt=0`).

## Residual risk

- S210/S211-class churn is recurring: any live HTML surface with rotating tokens or
  redeploys (git-scm.com assets, PMC `ncbi_phid`, docs.python build footers) flips rows
  between runs, so any correction of the note should carry the command and date per the
  count rule instead of another frozen row list.
- I did not verify S205–S220 supersede-pair well-formedness or the round-36 lesson Gate
  rows (other seats own those); F2 is confined to the used-by/mined invariant.
- My probe run's S210/S211 states could differ at another hour (redeploy/instance
  rotation), but the count defect does not depend on them: the committed-at-tip worktree
  receipt and my run agree on `drifted=9` at the revision the note ships in.

## Verification gaps

- The frozen counter's oracle was not re-run (frozen artifact); its tallies are
  independently reproduced by the lane's own probe at the tip, so the count claim rests
  on two agreeing sources plus the per-row enumeration.
- None other: every behavioral sentence of the note was checked against tool source,
  selftest, or a live run.

## VERDICT

VERDICT: FAIL — `corpus/knowledge/source-drift-r36.md:15-19`: the exhaustive
"seven drifted rows" count (5 excerpts + 2 footer pages) contradicts the probe's output
at the note's own landing revision (`drifted=9`; S210, S211 unlisted) and its co-located
receipt `oracle_drifted=9`, and the counts carry no command; secondary:
`corpus/SOURCES.md:211` used-by/mined back-link broken; `:10-11,28` exit-2 subset.
Provenance trio, anchors, interface claims, falsifiable state table, no-universal-claims
and no-credential checks all held.
