# Mo51RevenScratchProducers — why pin-check exported under `<repo>/.scratch`, and who else writes there

- Seat: `Mo51RevenScratchProducers` (revenger, leaf). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
- Data revision read: `87e0c374537557754bf71dd68036ded3ddc6699c` (2026-10-26 19:37:01 -0300). Entering tip `aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd`, freeze `4677910eae6df3dabd38fe9a0daf1945146a1110`.
- Method: read-only git (`log --follow`, `show`, `diff`, `grep`, `ls-tree`, `status`) plus fixture repos built only in my scratch. No file in the lane was modified; no git/jj mutating command; no pacman; nothing installed (no tool was needed).
- Scratch: `/fast/scratch/hyaku/mori-r51/Mo51RevenScratchProducers/` (TMPDIR `<seat>/tmp`; three fixture repos `fx`, `fx2`, `fx3`; removed at the end). Every command below ran with `-C`/absolute paths and a verified `rev-parse --show-toplevel`.
- Counters, predicates, controls and kill rules were read, never scored or changed. This report proposes no counter change; the counter weaknesses found are named as limits.

## 1. Answer: why the export sat under `<repo>/.scratch`

The location was there in the file's **first commit**, `63eecf2738db96f46b0bd02b1b2dfd66787493d0` (round-47 freeze, 2026-10-25 10:19:06 -0300), and was never touched by v2–v4:

```
$ git show 63eecf27:tools/mori-pin-check.py | sed -n '183,190p'
def run_cmd(words, root, scratch, timeout):
    # TMPDIR lives inside the measured tree (<root>/.scratch): lane tools such as
    # mori-round19-regressions.py refuse a TMPDIR outside their own lane root.
    tmp_parent = os.path.join(root, ".scratch")
    ...
$ git show 63eecf27:tools/mori-pin-check.py | sed -n '334,340p'
    scratch_parent = os.path.join(repo, ".scratch")
    os.makedirs(scratch_parent, exist_ok=True)
    scratch = tempfile.mkdtemp(prefix="pin-check-", dir=scratch_parent)
```

Two facts about intent:

1. **The file states one reason, and it is the TMPDIR rule, not the export.** `run_cmd` puts each pinned command's `TMPDIR` under `<measured root>/.scratch` because lane tools refuse a TMPDIR outside the lane root. The `--rev` export then reused the *same* convention with `repo` as the root: the v1 docstring documents them as one rule — "under `<repo>/.scratch` (removed on exit); with `--root` it writes temp dirs under `<root>/.scratch`" (`63eecf27:tools/mori-pin-check.py:50-52`). No comment in v1–v4 says the export was placed there for git reach; the write scope was simply registered as "scratch under `<repo>/.scratch`" (`.ufo/waves/round-47/w1/ExecRegistryAudit.md:78`) and described by reviewers as "an isolated `git archive` export" (`.ufo/waves/round-47/w1/ConnCrossClaim.md:14`, `.ufo/waves/round-47/w2/RevSkillRows.md:60`).
2. **The git reach was an undocumented side effect, named only in v5.** `87e0c374:tools/mori-pin-check.py:872-876`: "The old `git archive` export sat under <repo>/.scratch, so pinned instruments that read git objects (`git -C <tree> …`) silently resolved to the enclosing repo". v5 is the first place the file says why the old location mattered.

[INFERENCE] The export location was convention-following (scratch inside the measured tree), not a deliberate git-reach design: the absence of any rationale comment in v1–v4, the docstring treating `--rev` and `--root` scratch as one rule, and the v5 comment describing the effect only after the relocation witness measured it (`evidence/control-c1-scratch-only.txt`: `reloc_mismatch=3`).

## 2. The `run_cmd` comment is accurate — and understates

The comment is byte-identical from v1 (`:184-186`) through v5 (`:540-542`). It names one tool; **three** lane tools actually refuse an outside TMPDIR, one of them `.scratch` exactly:

| tool | rule | lines |
|---|---|---|
| `tools/mori-round19-regressions.py` | TMPDIR must resolve **strictly inside** `Path(__file__).parents[1]` (the lane root), real path, not the root itself | `:878-895` |
| `tools/mori-content-review.py` | TMPDIR must be under the lane root (`commonpath == lane_root`) and not the root itself | `:355-370` |
| `tools/mori-retention-gate.py` | TMPDIR must resolve **exactly** to `<lane>/.scratch` and be a directory, else `SELFTEST retention-gate FAIL 0/21` rc 2 | `:458-470`; documented invocation `SKILL.md:178` = `mkdir -p .scratch && TMPDIR=$PWD/.scratch …` |

So the convention is real; the export merely inherited it.

## 3. Dated timeline (all times -0300)

| when | commit | event |
|---|---|---|
| 2026-10-24 03:28:48 | `d72ac167535229d737b9fa844513431d9a12f5ea` | round-41 freeze: the first `.scratch/` files enter the lane as **tracked** evidence (later enumerated by `corpus/knowledge/inheritance-d72ac16-r42.md:105-177`). |
| 2026-10-24 10:01:42 | `aa161e998eb22282e3d96ed2710bb0b39e5163de` | round-41 C3: more tracked `.scratch/` (round-22 strays). |
| 2026-10-25 10:19:06 | `63eecf2738db96f46b0bd02b1b2dfd66787493d0` | round-47 freeze creates `tools/mori-pin-check.py` **v1**: `--rev` = `git archive` exported into `<repo>/.scratch/pin-check-*`; `run_cmd` TMPDIR into `<root>/.scratch/pin-tmp-*` with the round-19 comment. |
| 2026-10-25 16:42:35 | `4dea3d091820cb3bd73b509b6ec047d017cdb023` | **v2** data: bans `.scratch/` as a *pin path* (`:193`) and adds the `v2_scratch_path_rejected` arm; export location unchanged. |
| 2026-10-25 17:03:53 | `af2250d80033ded23ec34af328068eeb85007d1c` | **v2** closure (prefix-led tallies, fences, header column); no `.scratch` change. |
| 2026-10-25 19:30:50 | `e4dfff32d4f97c7ef250e9a7538fa75d4f284492` | **v3**: scratch creation wrapped in `try` so setup failures exit 2 (R7 L5); export location unchanged. |
| 2026-10-25 22:06:57 | `24ebc7991e9081348d1aa4f558f994b1f4feccab` | round-49 data C2 adds `.scratch/` to `.gitignore` (line 5). The residue becomes invisible to plain `git status`, visible only with `--ignored`; the 225 already-tracked files stay tracked. |
| 2026-10-25 22:49:54 | `64c2d5fcd95a11f195de0387fa791cab7a54ecb1` | **v4**: `run_cmd(extra_env=…)` so a row's own `TMPDIR` wins; new arms for `TMPDIR=$PWD/.scratch` and `tools/.scratch/` argv; export location unchanged. |
| 2026-10-25 (round-47 w2) | — | the debris is already on record: "working tree … plus `.scratch/pin-check-*` debris" (`.ufo/waves/round-47/w2/ConnTrendCross.md:157`). It was not inventoried or routed until round 50. |
| 2026-10-26 09:05:32 | `487941b9395e89678af0053cc443cdb49cdee6e3` | round-50 data. At 09:36–09:50 the inventory seat measures the residue: 166→170 ignored `.scratch` lines, 25–26 G, of which **56 `pin-check-*` dirs = 17 G** (`.ufo/waves/round-50/a2w1/Mo50bExecScratchInventory.md` Findings 2–3). |
| 2026-10-26 09:31:37 (receipt 10:50:53) | `bae8656ea74a8ea3a4f2cf784e15cbeb91d9ad7d` | round-50 integration: `git clean -fdX -- .scratch` + `rm -rf .ufo/waves/round-40/scratch/mori-conform-selftest-*`; 225 tracked files stay (`evidence/a2-scratch-deletion.txt`). |
| 2026-10-26 10:52:00 | `756d5b1a5679b131203663cbbbd2c4d96f7143ee` | round-50 end receipts. |
| 2026-10-26 10:54:21 | `aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd` | round-50 verifier spot-check: §5 item 1 routes "`.scratch` producers" (`tools/mori-pin-check.py:884-887`, `.ufo/waves/round-40/conform.py:69`) to round 51; D-d names the non-hermetic re-execution. |
| 2026-10-26 11:09:49 | `4677910eae6df3dabd38fe9a0daf1945146a1110` | round-51 freeze: C1 contract, controls; `evidence/control-c1-scratch-only.txt` = `reloc_mismatch=3`, `evidence/control-c1-do-nothing.txt` = `kill_residue=12547`. |
| 2026-10-26 19:37:01 | `87e0c374537557754bf71dd68036ded3ddc6699c` | **v5** data: `--rev` tree is `git clone --shared --no-checkout` + `checkout --detach` under `--scratch`/TMPDIR; `conform.py` LANE from its own path, selftest scratch under TMPDIR; env/stale classes. |

## 4. Who else writes into the lane tree's `.scratch` (state at `87e0c374`)

Lane `.scratch` now: `du -sh .scratch` → `29M`; `git ls-files .scratch | wc -l` → `225`; `git status --porcelain --ignored -- .scratch | wc -l` → `0`; 10 tracked dirs + 3 tracked root files.

### 4.1 Live producers at the landed tip

| # | producer | what it writes | cleanup | evidence |
|---|---|---|---|---|
| 1 | `tools/mori-pin-check.py:539-546` `run_cmd` | `<measured root>/.scratch/pin-tmp-*` for **every** pinned command, in every mode | `rmtree(tmp)` in `finally`; the **parent `<root>/.scratch` is left behind** | observed §6.4 |
| 2 | same tool, `--root` mode | when `--root <lane>`/`--root .`, #1's root is the lane → lane `.scratch` | as #1 | `:542`; contract names it a limit |
| 3 | `.ufo/waves/round-49/count-c1.py:332` | default `--scratch` = `mkdtemp(prefix="c1-", dir=<repo>/.scratch)`, `repo` defaults to `LANE` (`:53`, `:324`) → lane `.scratch/c1-*` | **none** in `main()` (only the selftest's `base*` dirs are removed, `:380,402,425`) | registered at `SKILL.md:1009` |
| 4 | `.ufo/waves/round-48/count-c1.py:292` | same pattern (round-48 counter, registered `SKILL.md:971`) | none | `:292` |
| 5 | `tools/mori-retention-gate.py --selftest` | forces the caller to create and use `<lane>/.scratch` as TMPDIR | caller's | `:458-470`, `SKILL.md:178` |

### 4.2 Fixture-relative `.scratch` (not the lane)

`tools/mori-pin-check.py:1071-1072,1347-1348` build `.scratch/old/foo.py` inside throwaway roots under TMPDIR; `tools/mori-unlanded-check.py:132` writes `.scratch/seat/out.txt` inside its selftest fixture repo. `--selftest` itself is `mkdtemp(prefix="pin-selftest-")` under TMPDIR (`:1004`), never the lane.

### 4.3 Historical lane-tree writers still in the tree

- `.ufo/waves/round-22/measure-round22.py:49-50`: `TMPDIR=LANE/.scratch` and `scratch=LANE/.scratch/round22/<name>` (round-22 replay tool; not registered in `SKILL.md`).
- `.ufo/waves/round-40/conform.py` **at the entering tip**: `LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`, `SCRATCH_ROOT = <lane>/.ufo/waves/round-40/scratch`, selftest `mkdtemp(prefix="mori-conform-selftest-")` there (`aa3af1ec:conform.py:69-70,743`). At `87e0c374` it is `LANE` from `__file__` (`:72`) and `SCRATCH_ROOT = tempfile.gettempdir()` (`:73`) — fixed.
- Wave dispatch convention: r47–r49 specs sent seats to `<lane>/.scratch/<seat>` (`.ufo/waves/round-48/build-w1-spec.py:22`, `.ufo/waves/round-49/build-w1-spec.py:31`); this is where the r48/r49 seat dirs (≈8.6 G of the round-50 residue) came from. Round 50 moved to `X=/fast/scratch/hyaku/mori-r50` (`.ufo/waves/round-50/build-a2w1-spec.py:26`) and round 51 to `X=/fast/scratch/hyaku/mori-r51` (`.ufo/waves/round-51/build-w1-spec.py:20`).
- Not the lane: the fleet root `/home/vgpnk/Projects/shokunin/.scratch/` holds the orchestrator's `goal-2026*.md` files (13 entries, read-only observation); same name, different tree.

## 5. The hidden dependency v5 exposed

### 5.1 Mechanism, measured (fixture `fx2`, commits `ce98f756…` = C1 exported, `b3c869bf…` = C2 = enclosing master)

```
--- v1-v4 layout: archive at <repo>/.scratch/pin-check-x/tree, exported C1 ---
$ git -C "$T" rev-parse --verify 'master^{commit}'   -> b3c869bfc9418b0837032d056f51b6e62077a52d  rc=0   (the ENCLOSING repo's master, not C1)
$ git -C "$T" rev-parse HEAD                          -> b3c869bfc9418b0837032d056f51b6e62077a52d  rc=0   (enclosing HEAD, not C1)
$ git -C "$T" rev-parse --show-toplevel               -> .../fx2/repo                             rc=0
--- archive outside any repo (TMPDIR) ---
$ git -C "$T" rev-parse master                        -> fatal: not a git repository (or any parent …) rc=128
$ git -C "$T" rev-parse --show-toplevel               -> fatal: not a git repository (or any parent …) rc=128
--- v5 layout: git clone --shared --no-checkout + checkout --detach C1 ---
$ git -C "$CT" rev-parse HEAD                         -> ce98f7560816a9d69edbb3fb493679b7bf4b0b68 (C1)  rc=0
$ git -C "$CT" rev-parse --verify 'master^{commit}'   -> b3c869bfc9418b0837032d056f51b6e62077a52d (source tip) rc=0
$ git -C "$CT" for-each-ref                            -> refs/heads/master, refs/remotes/origin/HEAD, refs/remotes/origin/master = b3c869bf…
```

So: an archive inside the repo resolves **upward** to the lane's `.git`; outside the repo it has no repository at all; a `--shared` clone has its own `.git` **but its `master` is the source's tip at clone time, not R**.

### 5.2 The three instruments that read git from the tree they run in

| instrument | read | what it needs from the measured tree |
|---|---|---|
| `.ufo/waves/round-49/count-c1.py` | `LANE = dirname³(HERE)` (`:53`); `git -C LANE rev-parse --verify master^{commit}` and `r48.git_show(LANE, head, "SKILL.md")` in `--selftest` (`:353-355`); default `--rev master` (`:313`), `repo = opts["--repo"] or LANE` (`:324`) | a repository at/above the tree with a `master` ref and the lane's objects |
| `tools/mori-round19-regressions.py` | `repo = resolved.parents[4]` of the expected file (`:844`), then `git -C repo show ORACLE_REVISION:…` (`ORACLE_REVISION = 5e393d20…`, `:26`, `:853-857`); TMPDIR guard from `__file__` (`:878-895`) | the lane's objects (`5e393d20`) reachable from the tree |
| `.ufo/waves/round-40/conform.py` | `head_pin`: `git -C repo rev-parse HEAD` (`87e0c374:conform.py:525`), repo = `LANE` from `__file__` (`:72`) | a repository at/above the tree whose HEAD is the measured tip |

That is the `reloc_mismatch=3` of `evidence/control-c1-scratch-only.txt`: with the export moved to TMPDIR and the lane hidden, the archive has neither the lane's objects nor a repository to discover, and all three pins fail. Inside `<repo>/.scratch` they "passed" by reading the **enclosing lane repo** — silently, with no marker that the measured tree was not self-contained. v5's clone restores both properties: own `.git` (discovery) and the lane's objects through alternates (`--shared`), so `git show 5e393d20:…` still resolves.

### 5.3 The part v5 does not fix: `master` still means the source tip

v5's clone leaves `master` at the source's tip (5.1). For a `--rev R` run where R is **not** the source's current master (re-executing an old closure), the count-c1 selftest still reads `SKILL.md` at the source's master, not at R. The frozen counter's own clones avoid this deliberately:

```
$ sed -n '77,79p' .ufo/waves/round-51/count-c1.py
    # The clone's `master` is R, checked out (the lane's own state when R is its tip): pinned instruments
    # such as .ufo/waves/round-49/count-c1.py read `master` from the repository they run in.
    p = sh(["git", "-C", dest, "checkout", "-q", "-B", "master", rev], timeout=600)
```

So arm B measures a clone whose `master` **is** R, while the tool's own `--rev` clone leaves `master` at the source tip. Arm B's green therefore does not exercise the branch-reading dependency; it is a named limit of the counter (frozen — recorded, not proposed as a fix). The instrument-level tally run (master at T vs E vs absent) belongs to the seat that owns `.ufo/waves/round-51/build-w1-spec.py:202`; not duplicated here.

## 6. What v5 fixes, and the holes it leaves (observed)

### 6.1 Fixed, re-observed

- `--rev` with scratch outside the repo: the export tree is outside, the fixture repo stays clean (`status_lines=0` after completed runs).
- Selftest arm `v5_rev_export_outside_repo` (`87e0c374:tools/mori-pin-check.py:1478-1483`) asserts `PIN_CHECK=met`, `status --porcelain --ignored --untracked-files=all` empty, `not exists(<repo>/.scratch)` and the `--scratch` dir emptied.
- `conform.py` no longer carries the host path or writes its selftest scratch inside the lane.

### 6.2 "never `<repo>`" is not enforced (fixture `fx3`, v5 binary from the lane)

The docstring/help say the export is "never `<repo>`" (`:130-133`, `:900-901`), but the only rule is `--scratch` else `tempfile.gettempdir()` (`:910-915`). Two configurations put the export back inside the measured repo:

```
# C: explicit --scratch inside the repo
$ TMPDIR=<outside> python3 <lane>/tools/mori-pin-check.py --rev HEAD --repo "$R" --scratch "$R/.scratch"
pin … state=match … / PIN_CHECK=met … rc=0
probe: cwd=$R/.scratch/pin-check-hlvydrd1/tree  TMPDIR=$R/.scratch/pin-check-hlvydrd1/tree/.scratch/pin-tmp-aguh5o11

# A': the lane's documented TMPDIR convention (mkdir -p .scratch first)
$ mkdir -p "$R/.scratch"; TMPDIR="$R/.scratch" python3 <lane>/tools/mori-pin-check.py --rev HEAD --repo "$R"
pin … state=match … / PIN_CHECK=met … rc=0
probe: cwd=$R/.scratch/pin-check-zaapxtxl/tree  TMPDIR=…/tree/.scratch/pin-tmp-bjy5mjbc
$ TMPDIR="$R/.scratch" python3 -c 'import tempfile; print(tempfile.gettempdir())'
$R/.scratch
```

A SIGKILL in either configuration reproduces round-50 D-d (a full ~305 MiB tree under `<repo>/.scratch`). Note the asymmetry: `TMPDIR=<repo>/.scratch` is only honoured when that directory **already exists** (`tempfile.gettempdir()` validates candidates) — and the lane's own documented invocation is exactly `mkdir -p .scratch && TMPDIR=$PWD/.scratch …` (`SKILL.md:178`). C1 arm B is unaffected because the counter passes an outside `--scratch`/TMPDIR; the hole is an operability limit of the landed fix, not a claim failure.

### 6.3 Default scratch is `/tmp`, and the checkout is ~305 MiB

`tempfile.gettempdir()` falls back to `/tmp` when TMPDIR is unset or unusable. Measured size of the measured tree: `git ls-tree -r -l 87e0c374 | awk '{s+=$4} END{print s}'` → `319680383` bytes (304.9 MiB). So a `--rev` run without TMPDIR writes ~305 MiB under `/tmp`, contrary to the wave rule "/tmp only for files under 50 MB", and a killed run leaves it there (the docstring is honest: "a killed run leaves it in scratch, not in the repo it reads", `:131-132`; the contract also lists the `--root` residue as a limit).

### 6.4 `--root` still writes the lane tree, and leaves the parent

```
$ TMPDIR=<outside> python3 <lane>/tools/mori-pin-check.py --root "$R" --repo "$R"
pin … state=match … / PIN_CHECK=met … rc=0
probe: cwd=$R  TMPDIR=$R/.scratch/pin-tmp-f_ccgjaz
$ ls -ld "$R/.scratch"  -> drwxr-xr-x … $R/.scratch      # parent left after rmtree(tmp)
```

With `--root <lane>` that is the lane's `.scratch` (unchanged from v1; the contract names it).

## 7. Evidence index (command → observed, rc)

| command | observed |
|---|---|
| `git log --format='%H\|%ad\|%s' --date=iso --follow -- tools/mori-pin-check.py` | 6 commits: `63eecf27`, `4dea3d09`, `af2250d8`, `e4dfff32`, `64c2d5fc`, `87e0c374` (§3) |
| `git log --diff-filter=A -- tools/mori-pin-check.py` | creation = `63eecf27` |
| `for c in <6 commits>; do git show $c:tools/mori-pin-check.py \| grep -n -E 'scratch\|TMPDIR\|archive'` | export under `<repo>/.scratch` in all of v1–v4; v5 moves it (§3) |
| `git diff ${c}^ $c -- tools/mori-pin-check.py \| grep -E '^[-+].*(scratch\|TMPDIR\|archive\|clone)'` | v2 adds the `.scratch/` pin-path ban + arm; v3 wraps creation in `try`; v4 adds `extra_env`/TMPDIR arms; v5 replaces `git archive` with `clone --shared` + `--scratch` |
| `git log -S '.scratch/' -- .gitignore` | `24ebc799` (2026-10-25 22:06:57) |
| `git ls-files .scratch \| wc -l`; `du -sh .scratch`; `git status --porcelain --ignored -- .scratch \| wc -l` | `225`; `29M`; `0` |
| `git ls-tree -r -l 87e0c374 \| awk '{s+=$4} END{print s}'` | `319680383` (304.9 MiB) |
| fixture `fx2` archive-inside/outside + clone | §5.1 outputs |
| fixture `fx3` `--scratch`/TMPDIR-inside-repo, `--root` probe | §6.2, §6.4 outputs |
| `sed -n '458,470p' tools/mori-retention-gate.py`; `:355-370` content-review; `:878-895` round19 | lane TMPDIR guards (§2) |
| `grep -n 'parents\[4\]\|ORACLE_REVISION' tools/mori-round19-regressions.py` | `:844`, `:26` |
| `sed -n '77,79p' .ufo/waves/round-51/count-c1.py` | arm-B clone forces `master` = R |

## 8. Limits / UNVERIFIED

- I did not run the three instruments inside an archive-outside-repo tree to reproduce `reloc_mismatch=3` myself (the count-c1 selftest is minutes long and the receipt is frozen). The mechanism is observed at git level (§5.1) and the dependency is read statically per instrument (§5.2); the exact three failing pin names are cited from the contract/`build-w1-spec.py:155`, not re-measured here.
- The instrument-level tally dependence on `master` (§5.3) is inferred from the two observed facts (clone ref layout; `count-c1.py:353-355`); the dedicated run is another seat's item (`build-w1-spec.py:202`).
- The lane `.scratch` count is a point-in-time read at `87e0c374` while siblings run; no sibling of this wave writes the lane `.scratch` (all seats use `/fast/scratch/hyaku/mori-r51/<seat>`), so the read should be stable.
- No kernel-log MESSAGE text was read; no cgroup/sysctl/swap/systemctl/journal command ran; `/home/vgpnk/Projects/shokuknow` untouched.

## Draft for the lesson's Mistakes (fenced; L1 integrates)

```markdown
| M1 | hidden location dependence | `tools/mori-pin-check.py` v1–v4 exported the `--rev` tree with `git archive` into `<repo>/.scratch/pin-check-*` (`63eecf27:tools/mori-pin-check.py:336-338`). Git discovery walks upward, so inside that tree `git -C <tree> rev-parse master^{commit}` / `rev-parse HEAD` / `show 5e393d20:…` silently answered from the **enclosing lane repo** (fixture: archive of `ce98f756` answered `b3c869bf`, the enclosing master, rc 0; the same archive outside any repo: `fatal: not a git repository`, rc 128). Three pinned instruments depend on that reach: `.ufo/waves/round-49/count-c1.py` (`:53,:353-355`, reads `master`), `tools/mori-round19-regressions.py` (`:26,:844,:853-857`, pinned oracle `5e393d20`), `.ufo/waves/round-40/conform.py` (`:525`, `rev-parse HEAD`). Measured by the relocation witness: `evidence/control-c1-scratch-only.txt` → `reloc_mismatch=3`. | QUALITY 127 (`corpus/QUALITY.md:1070-1076`, "instruments carry no absolute host path") did not cover **repo-relative** git reach; round-47 reviewers called the export "isolated" (`ConnCrossClaim.md:14`, `RevSkillRows.md:60`) and no arm tested a git-reading pin from inside it | v5 (`87e0c374`) makes the measured tree a `git clone --shared` in `--scratch`/TMPDIR (`:872-876,:910-921`), so the tree has its own `.git` and the lane's objects. Residual (named limit): the clone's `master` is the source tip at clone time, not R — the counter's arm-B clones force `master` = R (`count-c1.py:77-79`), so arm B does not exercise it; and `--scratch <repo>/.scratch` (or a pre-created `TMPDIR=<repo>/.scratch`) is still accepted. | `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=119 fail=0` including `v5_rev_export_outside_repo` (`:1478-1483`); the relocation arm flips when the export moves (receipt above) |
```

## Findings

1. **HIGH — the v5 docstring's "never `<repo>`" is unenforced; the round-50 defect is reachable through the lane's own documented TMPDIR convention.** `tools/mori-pin-check.py:900-901,910-915` accept `--scratch <repo>/.scratch` (observed: export at `<repo>/.scratch/pin-check-hlvydrd1/tree`) and `tempfile.gettempdir()` honours a pre-existing `TMPDIR=<repo>/.scratch` (observed: export at `<repo>/.scratch/pin-check-zaapxtxl/tree`), which is exactly `SKILL.md:178`'s `mkdir -p .scratch && TMPDIR=$PWD/.scratch …`; a SIGKILL there reproduces `kill_residue=12547`-class residue. Files: `tools/mori-pin-check.py:900-901,910-915`; `SKILL.md:178`.
2. **MED — residual branch dependence: the measured tree's `master` is the source tip, not R.** `tools/mori-pin-check.py:872-876,916-921` clone `--shared` and `checkout --detach`, leaving `refs/heads/master` at the source's tip (observed); `.ufo/waves/round-49/count-c1.py:353-355` reads `master` from the tree it runs in, so for an old R the pin measures the source's master. The frozen counter's arm-B clones force `master` = R (`.ufo/waves/round-51/count-c1.py:77-79`), so the witness green does not exercise this — a named limit of arm B.
3. **MED — default scratch is `/tmp` and the checkout is 304.9 MiB.** `tools/mori-pin-check.py:912` (`tempfile.gettempdir()`), measured tree at `87e0c374` = `319680383` bytes; a run without TMPDIR writes that under `/tmp`, against the "<50 MB in /tmp" wave rule, and a killed run leaves it (docstring `:131-132`).
4. **MED — two registered counters still default their scratch into the lane `.scratch` and never remove it.** `.ufo/waves/round-49/count-c1.py:332` (`mkdtemp(dir=<repo>/.scratch)`, no cleanup in `main`; registered `SKILL.md:1009`) and `.ufo/waves/round-48/count-c1.py:292` (`SKILL.md:971`); the round-50 residue held 14 `c1-*` dirs / 30 M from this path. They are live lane-tree writers at the tip.
5. **MED — `--root` mode still writes the lane tree and leaves the parent directory.** `tools/mori-pin-check.py:539-546`: with `--root <lane>` every pin gets `TMPDIR=<lane>/.scratch/pin-tmp-*`; observed in a fixture that the parent `<root>/.scratch` survives the run. Contract names it as a limit; recorded here as the remaining `.scratch` producer of the tool.
6. **MED — `conform.py`'s entering-tip lane-tree writer was outside `.scratch` and is fixed, but the class was not generalised.** `aa3af1ec:.ufo/waves/round-40/conform.py:69-70,743` wrote `<lane>/.ufo/waves/round-40/scratch/mori-conform-selftest-*`; v5 (`87e0c374:conform.py:72-73`) derives `LANE` from `__file__` and uses TMPDIR. No sweep of the other round-38/39/41/42 `conform.py` scratch roots (listed in `Mo50bExecScratchInventory.md` §4) was part of C1.
7. **LOW — `.scratch` is simultaneously gitignored and tracked, so cleanup is split and plain status is blind.** `.gitignore:5` (added `24ebc799`, 2026-10-25 22:06:57) hides new residue from `git status --porcelain`, while 225 files (29 M) are tracked and survive `git clean -fdX`; `git status --porcelain --ignored -- .scratch` is the only count that sees both. Files: `.gitignore:5`, `.scratch/**`.
8. **LOW — the tool bans `.scratch/` as a pin path while its own scratch lived there.** `tools/mori-pin-check.py:193` rejects any registered instrument path containing `/.scratch/`, yet v1–v4 exported the measured tree into `<repo>/.scratch` and v5's `--root` mode still writes `<root>/.scratch`; a pin can therefore never name the measured tree it is measured in.
9. **LOW — the debris was on record ~1.5 days before it was measured.** `.ufo/waves/round-47/w2/ConnTrendCross.md:157` names `.scratch/pin-check-*` debris on 2026-10-25; only round 50 inventoried it (56 dirs, 17 G) and routed the producers. The round-47 write-scope cell (`.ufo/waves/round-47/w1/ExecRegistryAudit.md:78`, "scratch under `<repo>/.scratch`") documented the location without a cleanup or residue rule.

Report: `.ufo/waves/round-51/w1/Mo51RevenScratchProducers.md`
