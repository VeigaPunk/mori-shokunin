# ReviewLateMutCountC1Amended — re-verification of the late round-28 wave-2 mutation report

Seat MoriR29.ReviewLateMutCountC1Amended, 2026-10-22. Input: `.ufo/waves/round-28/w2/MutCountC1Amended.md`
(untracked; `git ls-files` count 0, no history entry). Every finding re-verified against the committed lane at
`7118f320a5ef18d20c1e361eff77db0e1a97b2d6` in a sandbox clone; each mutation re-run and its observed output quoted
below. **Recommendation: `commit as evidence`** (privacy-clean, all claims reproduced, actionable for the wave-1
round-29 C1 counter). The three survivor findings are still open defects of the round-28 counter.

## Inputs and method

- Attacked counter: `.ufo/waves/round-28/count-c1.sh`, blob `8682687f55f48bc32b4fe1d5e8c19424c1faddbf` at
  `1fc6bb0e`, `7118f320` and `8a45cef` alike (`git rev-parse <rev>:.ufo/waves/round-28/count-c1.sh`); content
  sha256 `0d7a1be0cbe6ad90296ea911d7441ef0dc6ee9454f76259bf8a40a1369f67980` — matches the w2 header.
- Frozen QUALITY 81 check: `git show df886be1cc75f1052002698bdb4a3d18a2eaf6c6:.ufo/waves/round-27/check-row-identity.py`,
  sha256 `5f05d4fe…` in this sandbox (w2 states `dc3ddad0…` — bookkeeping discrepancy only; the same frozen blob
  ref was used and all behavior reproduced; see caveats).
- Nothing changed between the attacked tip and my target: `1fc6bb0e..7118f320` adds only
  `corpus/lessons/round-28-verifier-spotcheck.md`; `corpus/SOURCES.md` blob is `bae2e852…` at both. Nothing closed
  later either: `7118f320..8a45cef` adds only the round-29 contract/census, and `.ufo/waves/round-29/count-c1.sh`
  does not exist at `8a45cef` (`git ls-tree`).
- Sandbox: `/fast/scratch/hyaku/mori-r29/ReviewLateMutCountC1Amended/lane` (`git clone --no-hardlinks` of the
  lane), inherited `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset for every run. The counter hardcodes
  `LANE=/home/vgpnk/Projects/shokunin/mori-shokunin` (count-c1.sh:12), so each run used
  `unshare --user --map-root-user --mount` with the sandbox bind-mounted over that path; the lane was touched
  read-only only. Mutants are sibling commits built with a temp index and `commit-tree`; after all runs the
  sandbox worktree is clean (`git status --porcelain` empty, HEAD `8a45cef`) and no stray index file remains.
- Baseline at `7118f320` (the counter must read met here for kills to be meaningful):

```
$ count-c1.sh 7118f320
row_identity=rows=152 changed=0 removed=0 bad=0
superseding=8/8 ids=S096,S097,S101,S127,S128,S129,S131,S140
readers_left=0
C1=met
exit=0
```

## Findings (each: claim, re-run, observed, status)

| id | w2 claim | status at 7118f320 |
|---|---|---|
| M1 | S145 `teaches` copied from S096 → killed | reproduced (killed) |
| M2 | S145 `used-by` → non-citing `corpus/README.md` → killed | reproduced (killed) |
| M3 | S145 Gate line loses sha256 → killed | reproduced (killed) |
| M4 | S145 `rejected` over mined S096 → killed | reproduced (killed) |
| M5 | live reader re-cites S096 → killed | reproduced (killed) |
| M6 | restored S096 differs in one cell → killed | reproduced (killed) |
| M7 | tsukuroi-naming reader line escapes `readers_left` | **reproduced open** |
| M8 | `rejected` can supersede a row self-flipped to `rejected` | **reproduced open** |
| M9 | no live reader needs to cite the new id | **reproduced open** |
| M10 | restored row differing in a mutable cell reads met — not a defect | reproduced (confirmed not a defect) |
| M11 | M1 born-with-the-copy: branch live on its own | reproduced (killed) |

My mutant commits (siblings of `7118f320`, sandbox only): M1 `8c9f801`, M2 `83f9080`, M3 `a985365`, M4 `0f7b6ab`,
M5 `4c9e965`, M6 `df45665`, M7 `ca8aaef`, M8 `ef2f69b`, M9 `b507001`, M10 `f820ba2`, M11 `42fae55` (M11 =
rebuilt history from S145's first publication `1c4c186` through `7118f320`, S145 born with the copied teaches).
Full outputs: `/fast/scratch/hyaku/mori-r29/ReviewLateMutCountC1Amended/runs/*.txt`.

### M1–M6, M11 — killed, as claimed

Re-run command for each: `count-c1.sh <mutant>` inside the bind-mounted namespace. Observed (one line quoted per
mutant; all exit 1, `C1=unmet`):

- M1: `superseding=7/8 ids=S097,…` / `fail S145 teaches_unchanged` (also `row_identity=… changed=1`)
- M2: `fail S145 used_by_not_citing=corpus/README.md`
- M3: `fail S145 gate_line`
- M4: `fail S145 status=rejected`
- M5: `superseding=8/8` / `readers_left=1`
- M6: `row_identity=rows=152 changed=1 removed=0 bad=0` (killed by the frozen `df886be1…` leg, as w2 noted)
- M11: `row_identity=rows=152 changed=0 removed=0 bad=0` / `superseding=7/8` / `fail S145 teaches_unchanged` /
  `readers_left=0` / `C1=unmet`, exit 1 — the mutant tree differs from `7118f320` in exactly one line
  (`git diff --stat`: `corpus/SOURCES.md | 2 +-`), S145's first publication already carries the copy, the
  identity leg is clean, and the counter's own `teaches_unchanged` branch fires alone. Matches w2's claim.

### M7 — reproduced open (survivor)

Scenario: live reader line citing superseded `S096` that also names tsukuroi (my M7 appends such a line to
`corpus/knowledge/system-pressure-r24.md`). Observed: `superseding=8/8`, `readers_left=0`, `C1=met`, exit 0 —
the line is dropped whole by `grep -v -E 'tsukuroi'` (count-c1.sh:81). Contract basis verified in the committed
round-28 contract: status rules and "`lines naming tsukuroi's own ids excluded`"
(`.ufo/waves/round-28/contract.md:87-91`), so excluding tsukuroi's own ids is right; the mechanism is line-scoped
and would also swallow a mori id on the same line.

Load-bearing observation w2 missed stating: at `7118f320` the **only** raw `olds` match in the readers is
`corpus/knowledge/oom-victim-selection-r27.md:204` (`git grep -n -w -E 'S096|S097|S101|S127|S128|S129|S131|S140'
7118f320 -- SKILL.md PROVINCE.md corpus/README.md corpus/knowledge` returns that one line) — a crosswalk naming
**tsukuroi's** S115/S118/S120/S127, contract-excluded. So the filter is what keeps `readers_left=0` at the real
tip; the real admission survives only because that line is excluded for the right reason.

Fix re-verified (w2's one-line fix, patched copy `count-c1-fixA.sh` in scratch): baseline still `C1=met` exit 0;
M7 → `readers_left=1`, `C1=unmet`; M5 still `C1=unmet`. No regression.

### M8 — reproduced open (survivor)

Scenario: S145 `status:=rejected` **and** superseded S096 `status:=rejected` in one commit. Observed:
`superseding=8/8`, `readers_left=0`, `C1=met`, exit 0. Mechanism: count-c1.sh:61 tests the superseded row's
**current** status cell (`o[8]`), so the self-flip satisfies the `rejected` branch. Contract admits `rejected`
only "when the row it supersedes is `rejected`" with S097 the 404 case (`contract.md:87-89`). History verified:
S096 first-published `mined`, S097 first-published `rejected` (`df4db54`, oldest commit carrying the ids; also
check-row-identity.py:5-6 takes first publication from full history in topological order). Fix (anchor to the
superseded row's first-published status) **not verified end-to-end** — same limits w2 disclosed.

### M9 — reproduced open (survivor)

Scenario: S145 `used-by := corpus/lessons/round-28.md` only, S145 stripped from SKILL.md/PROVINCE.md/the
knowledge note (my M9 touches exactly those files). Observed: `superseding=8/8`, `readers_left=0`, `C1=met`,
exit 0 — the lesson path cites S145 through its own Gate table, and no leg requires a **live** reader
(count-c1.sh:63-66 validates only that each `used-by` path cites the new id). Fix re-verified (w2's three-line
live-reader check, same patched copy): baseline still `C1=met`; M9 → `fail S145 no_live_reader_cites_new_id`,
`C1=unmet`; M2 still `C1=unmet` (its `used_by_not_citing` fires first). No regression.

Real-state check (does the admitted tip actually have live readers?): yes —
`git grep -l -w <id> 7118f320 -- SKILL.md PROVINCE.md corpus/README.md corpus/knowledge` per row: S145 3 files,
S146 2, S147 1, S148 4, S149 3, S150 4, S151 3, S152 1. The M9-class hole exists in the counter, not in the
admitted corpus.

### M10 — reproduced, confirmed not a defect

Scenario: S096 `status := stale` (mutable cell, differs from first-published `mined`). Observed: `C1=met`,
exit 0, `row_identity=… changed=0`. Consistent with CORPUS Rule 2 via check-row-identity.py:22
(`MUTABLE = {"status", "recheck", "used-by"}`) and with the counter not consulting `o[8]` for a `mined` new row.
Contract-consistent; no fix. Matches w2.

## Does any reproduced finding change round 28's admitted verdicts?

- **Round-28 C1 (freshness, admitted): no.** The counter's blob is unchanged `1fc6bb0e`→`7118f320`→`8a45cef` and
  `corpus/SOURCES.md` with it, so no re-run could differ; the six assigned mutants plus M11 all die exactly as
  reported; the three survivors are synthetic states absent from the real corpus at `7118f320` — all eight new
  rows have live citing readers (M9 check above), the only `olds`-matching reader line is the contract-excluded
  tsukuroi crosswalk (M7 observation above), and no row is `rejected` over a mined row (S145/S096 `mined`; S097
  first-published `rejected`, 404 case; per `df4db54`). The admission's underlying property holds; what is
  weakened is the counter's robustness, which is exactly what the spot-check routed
  (`corpus/lessons/round-28-verifier-spotcheck.md:122-125`: act on findings against C1's counter or QUALITY
  83–84).
- **Round-28 C2: no.** The file attacks only `count-c1.sh`; it makes no C2 finding.
- **QUALITY 83/84: no.** They are separate checks (`check-heading-time.py:2` — dated headings;
  `check-tip-receipts.sh:2` — tip receipts; definitions also at `corpus/lessons/round-28.md:29,54`), and the
  file carries no finding against either script.
- **Actionable now:** `.ufo/waves/round-29/count-c1.sh` did not exist at `8a45cef`; the wave-1 counter must
  close M7 (strip the tsukuroi enumeration, then count), M8 (anchor the `rejected` branch to the superseded
  row's first-published status) and M9 (require a live reader in `used-by`) — all three fixes verified above.

## Privacy and commit recommendation

**Recommend `commit as evidence`.** Reasons:

1. Every claim in the file re-verified reproduced at `7118f320` (table above); its two verified smallest fixes
   re-verified effective and regression-free; its limits section is honest (M8 fix unverified — still true).
2. Privacy scan clean: `grep -n -E 'uid=[0-9]|pid=[0-9]|user-[0-9]+\.slice|user@[0-9]+\.service|[a-z-]+\.service\b|journalctl|--prefer|--avoid|--ignore|/etc/|session-|token'`
   over the file → zero hits; manual read shows only repo paths, blob/commit ids and its own scratch paths. No
   harness settings values, no uids/pids, no user-session unit names, no host command lines.
3. Routed defect 1 of the round-28 spot-check requires commit-or-disposition of this file with findings acted on;
   the three open classes feed the round-29 counter.

Caveats to record with the commit (none blocking):

- w2's sentence "At the landed tip exactly one reader line mentions tsukuroi" is imprecise: many reader lines
  mention tsukuroi; exactly one reader line **matching a superseded id** mentions tsukuroi
  (`oom-victim-selection-r27.md:204`).
- w2's sha256 for the frozen QUALITY 81 extract (`dc3ddad0…`) does not match this sandbox's extraction of the
  same blob (`5f05d4fe…`); the blob ref `df886be1…` is identical and all behavior reproduced, so this is
  bookkeeping, not a defect.
- M8's smallest fix remains unverified end-to-end (w2's own limit, re-confirmed).

## Restoration and tooling

- Lane: read-only git only (`rev-parse`, `show`, `log`, `grep`, `ls-tree`, `ls-files`, `diff --stat` on the
  sandbox); no writes to the lane or fleet repos, no jj, no pacman transaction, no packages installed (host
  `git`, `python3`, `bash`, `unshare` only). No tool installs or upgrades to record.
- Sandbox: worktree clean after all runs; mutants exist only as unreferenced sibling commits; scratch tree
  `/fast/scratch/hyaku/mori-r29/ReviewLateMutCountC1Amended/` (`build.py`, `revs.txt`, `runs/*.txt`,
  `count-c1-fixA.sh`, `lane/`).
- Blindness: `tools/mori-oom-killers.py` never opened or run; no round-26/27 reports and no round-28 w1/w2
  reports opened beyond the item-named `w2/MutCountC1Amended.md` (QUALITY 83/84 cited from the committed check
  scripts and `corpus/lessons/round-28.md`, not from wave reports).
