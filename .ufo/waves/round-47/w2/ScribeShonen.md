# ScribeShonen — mori round 47, wave w2 report

- Seat: ScribeShonen (scribe, godspeed `/skill:godspeed`)
- Lane: mori-shokunin (detection and report only)
- Date: 2026-10-25
- Assignment: draft the report's SHONEN section — one line per box of `SHONEN.md`
  (4 boxes), each `[~]` with a resolvable evidence pointer at T (path:line) or
  `[ ]`; never `[x]` (no non-author verifier). Check each pointer resolves at T =
  `68d66ca53d89be5c34a62f46af7c37449d9f9b63`.
- Report path: `.ufo/waves/round-47/w2/ScribeShonen.md` (relative to lane root
  `/home/vgpnk/Projects/shokunin/mori-shokunin`).

## 1. Pointer resolution at T (read-only git)

SHONEN.md at T is byte-identical to the working-tree copy I was given
(`git show 68d66ca…:SHONEN.md`), so the four boxes are the ones verified below.

Resolution check per pointer: `git show 68d66ca53d89be5c34a62f46af7c37449d9f9b63:<path> | sed -n '<first>,<last>p'`
— exit 0 and expected content present for every path:line pointer:

| box | pointer | resolves | observed content |
|---|---|---|---|
| 1 | `SKILL.md:162-194` | yes | gate-registry decision-table rows (`name/kind/entry/verdict map/self-test/pinned values/write scope/owner`) with per-instrument self-test cells and cited evidence |
| 1 | `corpus/QUALITY.md:983-1023` | yes | numbered quality criteria 120–122, each with lessons, rationale, check and shown-able-to-fail |
| 2 | `LOG.md:2608-2653` | yes | Round 45 entry: executed end-to-end domain work logged (attempts, motivating evidence per claim, measured counters, receipts) |
| 3 | `SKILL.md:162-194` | yes | same range as box 1 |
| 3 | `tools/mori-gate-registry.py --selftest` | operational check below | — |
| 4 | `PROVINCE.md:3-16` | yes | domain scope: owns (read-only probes), refuses (→ kumitate/tsukuroi/kama/kagi), detection-and-report-only |
| 4 | `corpus/lessons/round-45.md:168-179` | yes | lessons table rows M1–M11 with defect text, evidence, verdict |

Box 3's second pointer is a command, not a path:line. Command resolved
operationally at T:

- Tool exists at T: `git show 68d66ca…:tools/mori-gate-registry.py` — 743 lines.
- Real `--selftest` argv branch at T: parser key `ap.add_argument("--selftest", …)`
  (line 680); dispatch `if args.selftest: return selftest()` (lines 683–684);
  implementation `def selftest()` (lines 502–668), tally print at line 667.
- Command (run from lane root; TMPDIR confined to scratch):

```
TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ScribeShonen \
  python3 tools/mori-gate-registry.py --selftest
```

  Output: `selftest PASS registered_row_met … escape_flag_mention_rejected`
  (15 PASS lines); `GATE_REGISTRY_SELFTEST pass=15 fail=0`. Exit code: **0**.
  Matches the pinned value in the SKILL.md registry row (pass=15 fail=0).

No pointer failed; every box keeps `[~]`. None is `[x]` (no non-author verifier).

## 2. SHONEN section draft

```markdown
## SHONEN (drafted by ScribeShonen, round 47 w2)

Promotion to shokunin requires all of:

- [~] SKILL.md contains real decision tables, error patterns, checklists, cited sources — `SKILL.md:162-194`; `corpus/QUALITY.md:983-1023`
- [~] At least one end-to-end domain task executed and logged in LOG.md — `LOG.md:2608-2653`
- [~] Instructions executable by an agent without oral context — `SKILL.md:162-194`; `tools/mori-gate-registry.py:502-668` (selftest arm; `--selftest` → `GATE_REGISTRY_SELFTEST pass=15 fail=0`, rc 0, at T)
- [~] No cross-domain bleed (PROVINCE.md still accurate) — `PROVINCE.md:3-16`; `corpus/lessons/round-45.md:168-179`
```

Change vs SHONEN.md: box 3's second pointer is written as a path:line
(`tools/mori-gate-registry.py:502-668`, the selftest implementation) instead of
the bare command string, and the observed `--selftest` result is attached; all
other pointers are unchanged and resolve at T.

## 3. Tooling authorization record

Nothing installed or upgraded: the task needed only read-only `git show`/`git
status` and running one already-committed lane tool with the existing `python3`.
No `pacman` transaction attempted (guard — all pacman transactions paused
host-wide); no other channel used. `TMPDIR` was set to
`.scratch/r47w2-ScribeShonen` for the tool run; the tool's selftest creates and
cleans its fixture git repos under `$TMPDIR` (`finally: shutil.rmtree(tmp, …
)` at 514–515), and I verified no `grst-*` residue in scratch or `/tmp`.
No subagents spawned (leaf seat).

## 4. Limits / unverified

- Pointer resolution and sampled content are observed; I did not render an
  independent qualitative verdict on each box beyond confirming the observed
  content at the range matches the box's described kind.
- The working tree carries pre-existing changes from other seats/L1 integration
  (`LOG.md`, `SCORECARD.md` modified; wave scratch dirs and w2 spec files
  untracked) — observed via read-only `git status --porcelain`; I made no
  changes to the lane repo and did not rely on working-tree bytes for any
  pointer check (all checks used `git show` at T).
