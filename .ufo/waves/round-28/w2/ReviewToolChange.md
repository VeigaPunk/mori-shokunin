# ReviewToolChange — wave 2, round 28

**Verdict: holds** — attacked `tools/mori-oom-killers.py` at `6ebd518f..f2de0eed`: the diff is empty, the
emptiness is justified (zero judged tool errors because the frozen blind cases all pass), PASS 32/32 is kept
on the round-26 file, no `KILLER_ACTED` verdict moves, and the four other named round-26 selftest surfaces
tally identically at both revisions.

## Scoped diff

- `git -C <lane> diff 6ebd518f f2de0eed -- tools/mori-oom-killers.py` → **0 lines**, `diff --stat` empty, exit 0.
- `git show <rev>:tools/mori-oom-killers.py | sha256sum` → `343acaf4b94a1d18f2133b7967ef4078f0605de111a22e803ae36ace77f73d3b`
  at **both** revisions.
- Whole-tree check: `git diff --name-status 6ebd518f f2de0eed -- tools/` → exactly one entry,
  `A tools/fixtures/mori-oom-killers/cases-a2.json` (+1287 lines). No tool file changed anywhere under `tools/`.
- `cases.json` blob id `5b4dcee7b682c896c8e9f22ed1f8ac58d0176556` at both revisions (the C2 counter's F5 pin,
  `count-c2.sh:51`, satisfied).

## Requirement 1 — every change tied to a judged tool error

**Vacuously met: there are no changes to tie.** Justification, not just vacuity: the A2 judge rulings
(`contract.md:104-113`) only trigger on a frozen-case/tool mismatch, and a `tool error` ruling only *permits*
("the L1 may change the tool", `contract.md:109`) a change — the freeze selftest at
`.ufo/waves/round-28/evidence/c2-freeze-selftest.txt` recorded `MORI_OOM_KILLERS_SELFTEST: PASS 30/30` exit 0
at freeze commit `d21b8bd38b1bf72ec903a19ed543c615564e8278`, and my independent rerun at tip reproduces it
(see below). With zero mismatches there were zero rulings and zero required changes. An empty diff is the
correct outcome, not a missing fix.

## Requirement 2 — PASS 32/32 on the round-26 file

Temp extract of `f2de0eed` (`git archive` → `/fast/scratch/hyaku/mori-r28-w2/ReviewToolChange/tip`):

```
$ python3 -I -B tools/mori-oom-killers.py --selftest
MORI_OOM_KILLERS_SELFTEST: PASS 32/32     exit=0
$ python3 -I -B tools/mori-oom-killers.py --selftest --cases tools/fixtures/mori-oom-killers/cases-a2.json
MORI_OOM_KILLERS_SELFTEST: PASS 30/30     exit=0
```

Base extract also prints PASS 32/32 exit 0.

## Requirement 3 — no KILLER_ACTED turned into another verdict

- `cases.json` pins `expect.verdict` per case; 10 of 32 cases pin `KILLER_ACTED` (inspected via python3 json,
  `cases[i].expect.verdict`).
- The matcher enforces it: `tools/mori-oom-killers.py:692` (`if "verdict" in expect and result["verdict"] !=
  expect["verdict"]:` → problem recorded), plus `exit` and `expect.fields` pins in the same loop.
- PASS 32/32 on the identical blob at both revisions ⇒ every pinned verdict, including all 10 `KILLER_ACTED`,
  is produced identically. Byte-identical tool (`sha256` above) makes a flip impossible at `f2de0eed`.

## Requirement 4 — four other round-26 selftests, base vs tip tallies

| Tool | Command | `6ebd518f` | `f2de0eed` | Match |
|---|---|---|---|---|
| mori-pressure | `python3 tools/mori-pressure.py --selftest` | `PASS 12/12`, `MATCHER: rejected 48/48`, exit 0 | identical | yes |
| mori-job-runway | `python3 -I -B tools/mori-job-runway.py --selftest` | `PASS 21/21`, exit 0 | identical | yes |
| mori-retention-gate | `TMPDIR=$PWD/.scratch python3 tools/mori-retention-gate.py --selftest` | `PASS 21/21`, exit 0 | identical | yes |
| mori-routed-r24 | see finding F1 | gate mode `held:4 mismatches:0` D4 held, exit 0 | identical | yes |

All run from `git archive` extracts of the respective revisions. Retention-gate needs `TMPDIR=<repo>/.scratch`
per `SKILL.md:178`; a first run from a mis-extracted partial tree printed `FAIL 0/21` exit 2 at both revisions
(operator error in my scratch layout, not the tool — proper full-tree extracts pass 21/21 at both).

## Findings

- **F1 (low, pre-existing; not introduced by this diff).** `tools/mori-routed-r24.py` has **no `--selftest`**
  at `f2de0eed`: `--selftest` → `error: unrecognized arguments`, exit 2 (probe; also bare). The registry row
  `SKILL.md:717` already records "none built in … A committed self-test is still owed (routed defect R5)". The
  routed-hygiene R5 sandbox fix did not land at this tip (`tools/` delta is only `cases-a2.json`), consistent
  with `contract.md:70` — carried unless a non-author check passes. Tally surrogate used above: gate mode
  `--repo <clone> --rev <rev>` prints `held:4`, `mismatches:0`, D4 hygiene held, exit 0 at both revisions
  (JSON identical apart from `rev`/`rev_commit`).
- **F2 (informational).** R1 (job-runway false-number limit, `SKILL.md:718`) likewise unlanded —
  `mori-job-runway.py` unchanged. Same carried-hygiene explanation; no contract breach.

## Residual risk

- The empty diff means the two spec-vs-tool divergence shapes noted in `corpus/lessons/round-28.md:19-21`
  (A2-07 in-scope dry-run split; A2-10 stamp-less records outside the bounded branch) persist in the tool.
  That is lawful: no frozen blind case pinned a value the tool disagreed with, so no `tool error` existed.
  Any future case pinning those shapes would reopen it as a ruling, not as a retroactive defect of this tip.
- Low overall: identical bytes cannot regress a frozen-case verdict.

## Verification gaps

- routed-r24 gate mode ran against a `--no-hardlinks` clone (`clone/`, 251 revs, both target revs present) —
  predicates read committed bytes only per `SKILL.md:717`, so representative; not run against the lane path.
- `count-c1.sh`/`count-c2.sh` not run (out of my scope; other seats own the counters).
- No LSP server answers these Python tool files in a bare extract; verdict-pinning evidence above is
  tool-source line citation plus executed outputs, not LSP diagnostics — the only applicable surface here.

## Tooling

- None installed. System `python3`, `git`, `tar` only; pacman transactions paused host-wide per bounds.

Bounds: read-only on the lane; this report file is my only write there; scratch under
`/fast/scratch/hyaku/mori-r28-w2/ReviewToolChange/` (archives + `--no-hardlinks` clone). No settings values,
session ids, uids, unit names or journal text copied.
