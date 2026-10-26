# Mo49ExecScratchHygiene — `.scratch/` hygiene plan (round 49, w1)

Seat: `Mo49ExecScratchHygiene` (executor, leaf). Lane: `mori-shokunin`.
Entering tip: `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86`. Contract read: `.ufo/waves/round-49/contract.md`.
Scratch (own): `.scratch/r49-Mo49ExecScratchHygiene/`. `TMPDIR` set to it for every lane-tool run.
Wrote only this report and that scratch dir. No `.gitignore` edit, no deletion, no git/jj mutation, no
`pacman`, no tool installed, no host read beyond read-only `ls`/`du`/`stat`-class commands.
All counts below were taken 2026-10-25T21:42–21:46-03:00 (2026-10-26T00:42–00:44Z) **while round-49 seats
were still writing `.scratch/`**; the tree grows by a few entries per minute, so the shape and the rule are
the deliverable, and §5 carries a recompute command for round end.

Report: .ufo/waves/round-49/w1/Mo49ExecScratchHygiene.md

## 0. Defect under treatment

`corpus/lessons/round-48-verifier-spotcheck.md` §1 defect (a) and §5 item 1: 114 untracked `.scratch/*`
directories were left at the round-48 closure, and `tools/mori-unlanded-check.py` "scope excludes `.scratch`,
so it cannot see them". Round 47 had the same defect (53 paths). The check is not broken; it is deliberately
blind (`mori-unlanded-check.py:13-15`: "`.scratch/` and anything git ignores are outside the scope on
purpose"), and `in_scope()` (`:43-46`) is a positive prefix whitelist (`.ufo/waves/round-N/`, `corpus/`,
`tools/`, top-level `*.md`) that no `.scratch/...` path can match.

## 1. Current state (step 1)

```
$ git -C <lane> status --porcelain | awk '/^\?\? \.scratch\//{s++} END{print "total="NR, "scratch_lines="s, "other="NR-s}'
total=171 scratch_lines=151 other=20
$ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.excludesFile GIT_CONFIG_VALUE_0=<scratch>/projected-ignore \
    git -C <lane> status --porcelain | awk '/^\?\? \.scratch\//{s++} END{print "projected_total="NR, "projected_scratch_lines="s+0}'
projected_total=20 projected_scratch_lines=0
$ du -sh .scratch
22G     .scratch
$ git -C <lane> status --porcelain=v1 -z --untracked-files=all | tr '\0' '\n' | grep -c '^?? \.scratch/'
470162
$ git -C <lane> check-ignore -v .scratch ; echo rc=$?
rc=1                                  # not ignored; .gitignore has 4 rules, none for .scratch
```

`.gitignore` is tracked (`git ls-files .gitignore`; last touched `0a05f7e6`, 2026-10-23) and holds only
`.ufo/interactive-sessions/`, `.ufo/worktrees/`, `__pycache__/`, `*.pyc`.

Top-level entries under `.scratch/` at the 21:42 snapshot: **156** = 13 tracked + 135 untracked + 8 that
`git status` never shows (empty dirs, plus `.scratch` itself). By 21:44 `find` counted 158 dirs + 3 files.

| prefix | untracked entries | size | cited in tracked files |
|---|---|---|---|
| `pin-check-*` | 45 (53 by 21:44) | 13.35G | 0 |
| `r49-*` | 17 | 4.94G | 0 |
| `r48-*` | 32 | 1.65G | 30 |
| `r48w2-*` | 29 | 0.38G | 29 |
| `c1-*` | 12 | 0.02G | 0 |
| tracked (13 entries, 225 files) | — | 29M | heavy (`round22` alone: 9,075 token hits) |

Total `du -sh` 22G; 470,162 untracked files. `pin-check-*` (git-archive exports) and `c1-*` (counter
`mkdtemp`) are pure tool temp and account for 13.4G of the 22G.

## 2. Scratch dirs cited as evidence — do not delete (step 2)

`git grep -n '\.scratch/' b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86` (20,933 hits; `.scratch/` files
themselves excluded) was reduced to distinct top-level names and intersected with the directories that exist.
"Cited" = the name occurs as `.scratch/<name>` in at least one **tracked, non-scratch** file at the entering
tip (seat reports, evidence, LOG, lessons, SKILL.md).

### 2a. Tracked scratch (13 top-level entries, 225 files, 29M) — keep
`round22` (154 files), `CritConjunctSemantics`, `CritDrainedTuple`, `CritFreezeTiming`, `critnewdag`,
`CritNewSurvivor`, `mutgate-eligible`, `MutGateFirstParent`, `MutGateReadd`, `rev-scorecard-claims`,
`c11-after-fixture-r-ExeDagR.txt`, `ExeDagN-c11-after-fixture-n.txt`, `SrcGitCommit-git-rev-parse.html`.
These are committed evidence (e.g. `corpus/knowledge/inheritance-d72ac16-r42.md:105-178` names all 71
round-40-era files; `corpus/lessons/round-24-verifier-spotcheck.md:27` measures `round22`). They are also
what keeps `<repo>/.scratch` present in a fresh clone for the tools in §3.

### 2b. Untracked but cited (59 entries) — keep
```
r48-CritC1Counter            r48-ExecCensusGuard        r48-ScoutQuarantineS262    r48w2-R48ExecD7
r48-CritC2Counter            r48-ExecPortability        r48-ScoutQuarantineS268    r48w2-R48ExecGates
r48-CritContractFreeze       r48-ExecQuoteFinderErrno   r48-ScoutQuotaHost         r48w2-R48ExecLiveRefetch
r48-CritEntryRisk            r48-ExecQuoteFinderMan     r48-ScoutStagedQuota       r48w2-R48ExecRealRegistry
r48-CritJunkClasses          r48-ExecRealRegistryAudit  r48-ScribeEntryA           r48w2-R48ExecRerunC1
r48-ExecAppendSweep          r48-ExecSkillRowsRun       r48-ScribeEntryB           r48w2-R48ExecRerunC1Clone
r48-ExecC1Replay             r48-ExecUnlandedCheck      r48-ScribeRowAliyun        r48w2-R48ExecRerunC2
r48-ExecV3ImplA              r48-ExecV3ImplB            r48-ScribeRowErrno         r48w2-R48MutC1Counter
r48-ExecV3Residuals          r48-MutC1Variants          r48-ScribeRowXfs           r48w2-R48MutC2Counter
r48-RevPromptHonesty         r48-SimpCounters           r48-l1                     r48w2-R48MutUnlanded
r48w2-R48CritEntryClaims     r48w2-R48CritFreeze        r48w2-R48CritV3Junk1       r48w2-R48MutV3Bind
r48w2-R48CritV3Junk2         r48w2-R48ExecCensusEnd     r48w2-R48MutV3Header       r48w2-R48MutV3Hidden
r48w2-R48RevC1Counter        r48w2-R48RevC2Counter      r48w2-R48RevEntryXfs       r48w2-R48RevHarnessLeak
r48w2-R48RevLesson           r48w2-R48RevQuality        r48w2-R48RevV3Code         r48w2-R48ScoutEntryContext
r48w2-R48ScribeTrends        r48w2-R48SentTools         r48w2-R48SimpV3
```
Largest cited debris: `r48w2-R48CritV3Junk2` 327.7M, `r48-ExecV3ImplB` 324.7M, `r48-ScoutQuotaHost` 323.3M,
`r48-ExecV3ImplA` 321.5M, `r48-ExecSkillRowsRun` 321.2M, `r48-ExecRealRegistryAudit` 321.4M (these hold the
pinned exports the round-48 reports hash). Deleting them would dangle hashes that committed reports cite.

### 2c. Cited but empty (5) — invisible to `git status` and to the check even without the ignore
`r48-ExecS478Recheck`, `r48-ScribeSkillRows`, `r48w2-R48ConnSiblings`, `r48w2-R48RevEntryQuotactl`,
`r48w2-R48RevSkillScore`. (`r48w2-R48RevEntryErrnoAliyun` is also empty but not cited anywhere.)
Empty directories are not the 114-directory defect class; removing or keeping them changes no git state.

## 3. Tools/gates that read `.scratch` or depend on `git status` cleanliness (step 3)

**Depend on `<repo>/.scratch` existing** (directory must stay; the ignore rule does not create or remove it):
- `tools/mori-pin-check.py:403` `tmp_parent = os.path.join(root, ".scratch")` and `:649`
  `scratch_parent = os.path.join(repo, ".scratch")` — `mkdtemp` parent; `:771-772` selftest writes
  `.scratch/old/foo.py`; `:134` rejects `/.scratch/` in bound command paths (so `tools/.scratch/x.py`
  stays a `PIN_CHECK` finding, independent of git).
- `tools/mori-retention-gate.py:459` selftest requires `TMPDIR` to resolve to `<root>/.scratch` and be a
  directory; the SKILL.md:178 pin is `mkdir -p .scratch && TMPDIR=$PWD/.scratch …` (creates it itself).
- `.ufo/waves/round-40/fixtures/run-c11-dags.py:39` — `mkdtemp(..., dir=<lane>/.scratch)`.
- `.ufo/waves/round-48/count-c1.py:292` — `mkdtemp(prefix="c1-", dir=<repo>/.scratch)`; `count-c2.py` has
  no `.scratch` reference.

**Read `.scratch` but are unaffected by an ignore rule:**
- `.ufo/waves/round-41/fixtures/c2/build-dags-r40.py:30` writes `<LANE>/.scratch/critnewdag/repos` (a
  *tracked* dir; new files there would become ignored, writes still work).
- `.ufo/waves/round-41/fixtures/run-r41-controls.py` uses `.scratch-r41` (a different name; not covered by
  `/.scratch/` and not part of this defect).
- `.ufo/waves/round-42/count-c3.py:26` counts `(".scratch/", 71, None)` via `git diff-tree` at `d72ac16`,
  not `git status`; it is not the pinned C3 (SKILL.md:186/192/196 pin the round-44/45 C3 counters).

**Use `git status` but are unaffected:**
- `tools/mori-index-clean.sh:53,71,77,101,108` — every call passes `--untracked-files=no`.
- `tools/mori-misroot-sweep.py:110` — fleet root, pathspec `.ufo/waves`/`.ufo/reports`.
- `tools/mori-round13/14/15/16-regressions.py` — `git status` inside their own fixture repos.
- `tools/mori-unlanded-check.py:58` — runs `status --porcelain=v1 -z --untracked-files=all`; the ignore
  removes `.scratch` records from that stream, and `in_scope()` already discarded them. §4 shows the output
  is byte-identical.

No tracked tool or round-40…48 gate asserts that the lane worktree is *clean* or that `.scratch` is
*visible*; none reads the count of untracked `.scratch` entries. Verdict: the ignore line is inert to the
gates, and the four `mkdtemp`/`TMPDIR` dependencies need the directory to exist — which tracked scratch
already guarantees in every clone.

## 4. Proposed `.gitignore` line and proof (step 4)

Proposed: append one line to the tracked `.gitignore`

```
/.scratch/
```

Anchored at the lane root. Rejected alternative: unanchored `.scratch/`, which would also hide nested
`tools/.scratch/` and `.ufo/waves/round-N/.scratch/` — those *are* in the unlanded check's scope and are
rejected by `mori-pin-check.py:134`, so hiding them would remove a real signal. `/.scratch/` hides only the
lane-root debris tree while tracked `.scratch` files stay tracked (gitignore never untracks).

### 4a. Sandbox (`D=$(mktemp -d)`, `git -C "$D"` everywhere, toplevel verified)

```
$ git -C "$D" init -q && git -C "$D" rev-parse --show-toplevel
/tmp/scratchhyg-vrt7cevm                       # == $D
# commit SKILL.md, tools/x.py, .scratch/kept.txt; then create .scratch/newdir/out.txt and corpus/late.md
$ git -C "$D" status --porcelain                       # before ignore
?? .scratch/newdir/
?? corpus/
$ python3 tools/mori-unlanded-check.py --repo "$D" --round 8
UNLANDED=dirty round=8 paths=1
unlanded ?? corpus/late.md                     # rc 1 — .scratch never listed
$ printf '.scratch/\n' >> "$D/.gitignore"              # then:
$ git -C "$D" status --porcelain                       # after ignore
?? .gitignore
?? corpus/
$ python3 tools/mori-unlanded-check.py --repo "$D" --round 8
UNLANDED=dirty round=8 paths=1
unlanded ?? corpus/late.md                     # rc 1 — byte-identical to before
$ git -C "$D" check-ignore -v .scratch/newdir/out.txt
.gitignore:1:.scratch/  .scratch/newdir/out.txt
$ echo changed > "$D/.scratch/kept.txt"; git -C "$D" status --porcelain
 M .scratch/kept.txt                           # tracked scratch stays visible
?? .gitignore
?? corpus/
```
Second sandbox, rule committed in the base commit: `git status --porcelain` → `?? corpus/` only; check →
`paths=1` `corpus/late.md`; `git add -A` staged only `corpus/late.md` (ignored `.scratch/newdir/out.txt`
not staged); `git ls-files .scratch` in the first sandbox still lists `.scratch/kept.txt`.

### 4b. Projection on the real lane (no write; `core.excludesFile` supplied via env)

```
$ printf '/.scratch/\n' > "$TMPDIR/projected-ignore"
$ git status --porcelain | wc -l                                        # baseline
154
$ GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=core.excludesFile GIT_CONFIG_VALUE_0="$TMPDIR/projected-ignore" \
    git status --porcelain | wc -l
9
$ python3 tools/mori-unlanded-check.py --repo . --round 49              # baseline
UNLANDED=dirty round=49 paths=7
unlanded ?? .ufo/waves/round-49/w1-dispatch.json
unlanded ?? .ufo/waves/round-49/w1-spec.json
unlanded ?? .ufo/waves/round-49/w1-validate.err
unlanded ?? .ufo/waves/round-49/w1.ready
unlanded ?? .ufo/waves/round-49/w1/Mo49ExecQuotesConf.md
unlanded ?? .ufo/waves/round-49/w1/Mo49ScribeRowConf.md
unlanded ?? .ufo/waves/round-49/w1/swarm-registry.json
rc=1
$ GIT_CONFIG_COUNT=1 … core.excludesFile="$TMPDIR/projected-ignore" \
    python3 tools/mori-unlanded-check.py --repo . --round 49
# same seven lines, rc=1; cmp of the two captures: IDENTICAL
```
The `GIT_CONFIG_*` variables are inherited by the tool's `git status` subprocess, so this measures the tool,
not a mock. At the atomic 00:44:06Z snapshot: 171 porcelain lines (151 `.scratch`) → 20 (0 `.scratch`).
The residue the check reports (round-49 dispatch files, in-flight `w1/*.md`) is unchanged, i.e. the ignore
does not blind the check to any in-scope path.

## 5. Deletion list for the L1 (round end; I delete nothing)

Rule used: a top-level `.scratch/` entry is deletable iff it is untracked **and** its name never occurs as
`.scratch/<name>` in a tracked non-scratch file at the landed tip. Snapshot at 21:42-03:00: **76 entries,
18.31G**.

Group A — round 48 and earlier, uncited, safe once no lane tool is running (13.36G):
```
c1-0hwb4hai  c1-1x495mxj  c1-4wbl9rzh  c1-5pata5a4  c1-7abgnspi  c1-92ev0hvl
c1-a4vak8t8  c1-dtqwk81s  c1-ia583qzp  c1-jop24kmf  c1-m0ua3cxh  c1-tgbnbdjm
pin-check-06xaefwz pin-check-0cy90_mk pin-check-0h0ylbp_ pin-check-1btueoqu pin-check-3feilgb1
pin-check-3pydnuk9 pin-check-51tsgf0q pin-check-64i_4y27 pin-check-6pzn3pjt pin-check-719mtsek
pin-check-76jccoid pin-check-76uatnch pin-check-7qpviv9j pin-check-8vz5ihhm pin-check-9ezbun8l
pin-check-_4_nb9xf pin-check-_inon1ry pin-check-_lurqwzj pin-check-_yfoj3l2 pin-check-e_7l957x
pin-check-emgatfhj pin-check-fc4lie4c pin-check-fvf56wxu pin-check-g03_qw2w pin-check-hv4xhuuk
pin-check-ibtrccoe pin-check-ivsuogh1 pin-check-jactb34m pin-check-jt0k9xn1 pin-check-kvsjhl53
pin-check-l33uhocv pin-check-lbm38mz_ pin-check-mrkdly48 pin-check-nuhbnojp pin-check-oixj90yr
pin-check-p6lscdby pin-check-r5g0gkny pin-check-rgp261p1 pin-check-sfjnt4zf pin-check-w12whlb9
pin-check-w4njmh9b pin-check-wc3j6eet pin-check-wl1dj21_ pin-check-xm6f9q4n pin-check-zmk9d4g4
r48-CritV3Spec  r48-ScribeRowQuotactl
```
(`pin-check-*` grew 45→53 during my measurement; every `pin-check-*` and `c1-*` is tool temp by
construction, so the globs `rm -rf .scratch/pin-check-* .scratch/c1-*` are safe at any moment no counter
run is in flight.)

Group B — round 49, in flight at my snapshot, re-check at round end (4.94G):
```
r49-L1  r49-Mo49ExecArmsBindUnlanded  r49-Mo49ExecArmsHeader  r49-Mo49ExecCensusMirror
r49-Mo49ExecControlsReplay  r49-Mo49ExecFlaggedFixed  r49-Mo49ExecImplA  r49-Mo49ExecK2K8
r49-Mo49ExecK3K6K7  r49-Mo49ExecK5X1  r49-Mo49ExecQuotesConf  r49-Mo49ExecQuotesHost
r49-Mo49ExecQuotesSvc  r49-Mo49ExecRegistryAudit  r49-Mo49ScribeEntryA  r49-Mo49ScribeEntryB
r49-Mo49ScribeRowConf
```
If a round-49 report lands and cites one of these, it moves to §2b and must stay. `r49-L1` is the L1's own
seat scratch (4.7G) — L1's call.

Recompute at round end (prints exactly the deletable set; nothing is deleted by it):

```
L=/home/vgpnk/Projects/shokunin/mori-shokunin; TIP=$(git -C "$L" rev-parse HEAD)
comm -23 \
  <(git -C "$L" status --porcelain | sed -n 's|^?? \.scratch/\([^/]*\)/.*|\1|p' | sort -u) \
  <(git -C "$L" grep -h -o -E '\.scratch/[A-Za-z0-9._-]+' "$TIP" -- . ':!.scratch' \
      | sed 's|^\.scratch/||' | sort -u)
```
Then `cd "$L/.scratch" && rm -rf -- <names>` (or the `pin-check-*`/`c1-*` globs), after confirming no
`mori-pin-check.py`/`count-c1.py` process is running.

Expected effect at closure: `git status --porcelain` loses all ~150 `.scratch` lines (171 → 20 measured, and
the 20 shrink as w1 files land); ~18.3G and ~470k files reclaimed; 13 tracked entries / 225 files and 59
cited untracked dirs untouched.

## 6. Limits / UNVERIFIED

- I did **not** edit `.gitignore`; the lane projection used an external `core.excludesFile`, so "the rule
  lands and the lane stays green" is UNVERIFIED (the sandbox shows it, the lane projection shows the
  expected line counts).
- Round-49 wave-2 reports are untracked while I measured; the citation scan covers the entering tip only.
  Group B is therefore provisional by design.
- Deletion was not run; `rm -rf` effects are not observed, only the candidate set.
- `git status` counts are a moving target (126 → 171 lines within ~25 minutes of wave-1 activity); the
  per-prefix table is a 21:42 snapshot.
- Ignoring `/.scratch/` *hides* the residue; it does not detect it. Detection at round end rests on the §5
  recompute step, not on the unlanded check.

## Findings

1. **MED — `.scratch/` is neither ignored nor in the unlanded check's scope; residue is 22G / 470k files /
   ~151 porcelain lines.** `tools/mori-unlanded-check.py:13-15,43-46` (deliberate scope) and `.gitignore`
   (4 rules, no scratch entry). This is round-48 routed defect 1, recurring from round 47.
2. **MED — the proposed ignore rule hides the residue instead of detecting it.** Without an explicit
   round-end deletion step (or a gate that counts untracked `.scratch` entries), the same defect recurs at
   the next closure: `corpus/lessons/round-48-verifier-spotcheck.md:23,100`. My §5 recompute command is the
   proposed mitigation; it is a process step, not a gate.
3. **LOW — 225 tracked `.scratch` files (13 top-level entries, 29M) must survive both the ignore and the
   deletion.** They are cited evidence (`corpus/knowledge/inheritance-d72ac16-r42.md:105-178`; `round22`
   alone has 9,075 token hits) and they keep `<repo>/.scratch` present in a fresh clone for
   `tools/mori-pin-check.py:403,649` and `tools/mori-retention-gate.py:459`.
4. **LOW — 59 untracked scratch dirs are cited as evidence by committed reports** (§2b), several holding
   the exact exports/hashes those reports record (e.g. `r48w2-R48CritV3Junk2` 327.7M,
   `r48-ExecV3ImplB` 324.7M). A blanket `rm -rf .scratch/*` would dangle those citations; the §5 rule
   excludes them.
5. **LOW — `.ufo/waves/round-40/scratch/mori-conform-selftest-*/` (untracked, in scope) and the round-49
   `w1*` dispatch files are a different leftover class**; they stay visible in `git status` after the fix
   (measured: the 20 non-scratch lines) and are not addressed here.
6. **LOW — six empty `.scratch` dirs are invisible to `git status` and to the check even without an ignore
   rule** (§2c). They are not part of the 114-directory class and no git-state fix can see them.
