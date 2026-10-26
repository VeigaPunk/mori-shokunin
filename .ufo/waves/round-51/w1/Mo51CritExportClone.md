# Mo51CritExportClone — attack on v5's measured tree (clone --shared vs git archive)

Seat: critic (leaf). Scope: C1 surface `tools/mori-pin-check.py` v5 at the data commit
`87e0c374537557754bf71dd68036ded3ddc6699c` — the `--rev` measured tree is a `git clone --shared`
checked out at rev (scratch), replacing the old `git archive` export under `<repo>/.scratch`.
No subagents. No tool installs. No git/jj mutations (read-only lane reads; clones FROM the lane
into scratch only). Scratch: `/fast/scratch/hyaku/mori-r51/Mo51CritExportClone/` (removed at end).
Host reads: none outside the lane repo and scratch.

## 1. What the measured tree actually is (constructed exactly as `export_rev` does)

Command (mirrors v5 `export_rev`, lines 870–886):

```
git clone -q --shared --no-checkout <lane> /fast/scratch/hyaku/mori-r51/Mo51CritExportClone/sampletree
git -C sampletree checkout -q --detach 87e0c374537557754bf71dd68036ded3ddc6699c
```

Observed internals:

| aspect | observation |
|---|---|
| HEAD | detached at `87e0c374…` (`symbolic-ref -q HEAD` → exit 1, empty) |
| `refs/heads/master` | `b504cb1701568a0038aab9d98ec13d28eff801da` — the lane's **live** master at clone time, NOT R (R is `87e0c374…`, one commit behind). `git rev-parse --verify master^{commit}` inside the tree answers `b504cb17…` |
| other refs | `refs/remotes/origin/HEAD`, `origin/master`, and every other lane branch (e.g. `hyaku/s3-mori-r24-author`, `mori-r19-attempt2-*` …) |
| hooks | only template `.sample` hooks (no active hooks) |
| config (.git/config) | minimal: core.repositoryformatversion 0, filemode, remote.origin.url, branch.master.remote/merge. No safe.directory needed (clone owned by runner; `stat` uid 1000 = vgpnk) |
| objects | `.git/objects/info/alternates` → `<lane>/.git/objects` (shared object store) |
| `.git` size | 26 files (refs, config, logs, hooks samples, info) |
| LFS | no `.gitattributes` anywhere at R (whole-tree `ls-tree -r` grep: none); no LFS files tracked; LFS filters exist only in the user's global gitconfig and never trigger without attributes |
| tracked file parity | `git ls-tree -r` list == `find` of the worktree (minus symlinks, which exist in both shapes) — byte-identical content to a `git archive` extract |

## 2. Registry comparison runs

Environment: `TMPDIR=/fast/scratch/hyaku/mori-r51/Mo51CritExportClone/tmp`, cwd = scratch.
(1) v5 at data (real registry, exactly as specified):

```
python3 <lane>/tools/mori-pin-check.py --rev 87e0c374537557754bf71dd68036ded3ddc6699c \
  --repo /home/vgpnk/Projects/shokunin/mori-shokunin \
  --scratch /fast/scratch/hyaku/mori-r51/Mo51CritExportClone/runA
```
→ exit 0, 46 lines, `PIN_CHECK=met tally_pins=35 digest_pins=8 mismatches=0 … env=0 stale=0`,
all 35 tally pins `state=match` (file `run-v5-at-data.txt`).

(2) v4 at the entering rev (`git show aa3af1ec…:tools/mori-pin-check.py`), same way, against a
fresh `--no-local` clone of the lane as `--repo` (so the old archive export and the enclosing-repo
resolution stay inside scratch, never touching the lane):

```
python3 v4-pin-check.py --rev aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd \
  --repo /fast/scratch/hyaku/mori-r51/Mo51CritExportClone/runB/v4src
```
→ exit 0, `PIN_CHECK=met …` identical per-pin lines; the only diffs vs (1) are the `rev=` string,
the `PIN_CHECK_SELFTEST` count (114→119), and the new `env=0 stale=0` summary fields.

(3) v5 at the entering rev, same commands (same-rev v4-vs-v5 comparison): exit 0, `PIN_CHECK=met`,
per-pin lines identical to (2) (diff shows only the summary fields).

(4) Counterfactual — v5 `--root` over a pure `git archive` extract of the data commit (same bytes,
no `.git`):

```
git -C <lane> archive 87e0c374… | tar -x -C runD/archroot
python3 v5-pin-check.py --root runD/archroot
```
→ exit 1, `PIN_CHECK=unmet … mismatches=2 no_command=2 env=0 stale=2`. Exactly two tally pins flip:

| pin | clone shape | archive shape |
|---|---|---|
| `tools/mori-round19-regressions.py --selftest` (SKILL.md:182) | `state=match pass=26 fail=0 rc=0` | `state=mismatch pass=25 fail=1 rc=1 class=stale` — arm `pinned-oracle-validates` fails |
| `.ufo/waves/round-49/count-c1.py --selftest` (SKILL.md:1009) | `state=match pass=44 fail=0 rc=0` | `state=mismatch pass=0 fail=1 rc=1 class=stale` (short-circuits: `master^{commit}` unresolvable) |

(`state=no_command` for the conform.py and SOURCES-appendonly rows in `--root` mode is a
`rev=None` binding artifact of `--root`, not a tree-shape difference; those rows run with a rev in
`--rev` mode.)

### Mechanisms (why the clone is load-bearing for these two pins)

- `.ufo/waves/round-49/count-c1.py` derives `LANE = dirname(dirname(dirname(HERE)))` (file line 53)
  and resolves `git -C LANE rev-parse --verify master^{commit}` (lines 353, 422). Inside the
  measured tree that means **the tree itself** must be a git repository with a resolvable `master`.
- `tools/mori-round19-regressions.py` `expected_from_pinned_commit()` (lines 836–856) runs
  `git -C <tree> show 5e393d20:.ufo/waves/round-19/frozen/expected.json`; without a repository in the
  tree this raises `HarnessError` → `pinned-oracle-validates` fails.

So the claim's motivating defect (instruments reading git objects from the tree they run in) is real
and IS exercised by the pinned registry: the clone shape is required for P-C1 arm D (`selftest
pass=119 fail=0`) to hold as measured. No counterexample to that part.

## 3. Behavioural differences clone-vs-archive that could change a pin's result

1. **Ref state is live, not pinned to R.** The measured tree's `refs/heads/master` equals the
   source lane's master **at clone time** (`b504cb17…` today, while `HEAD=87e0c374…`). Any pinned
   instrument that resolves a named branch (round-49 count-c1 does, default `--rev master`, line 313)
   sees the source's current tip, not R. Two runs of `--rev R` at different moments see different
   `master` values; if the source's master is ever deleted/renamed, `master^{commit}` inside the
   measured tree stops resolving and the pin flips to `class=env`/`class=stale` even though R is
   unchanged. Verified: `git -C sampletree rev-parse --verify master^{commit}` →
   `b504cb1701568a0038aab9d98ec13d28eff801da` ≠ R.
2. **`.git` directory (26 files) is now inside the measured tree.** No currently registered pin
   enumerates/counts tree files (the 35 tally pins are all `--selftest` invocations; the 8
   digest/lines pins read named blobs), so no observed result changes — but any future pin that
   walks the tree (find/glob/os.walk), or computes a manifest not via `git ls-files`, sees `.git`
   junk that `git archive` never shipped.
3. **Object-store dependency via alternates.** The measured tree reads objects from the lane's
   `.git/objects`. The old archive export was self-contained; the clone breaks if the lane's object
   store is moved, pruned, or made unreadable mid-measurement (class=env flips). Nothing in the
   current run exercises this.
4. **safe.directory / ownership.** Clone is created by the runner, so git's dubious-ownership guard
   never fires (verified: uid 1000, all git commands in the tree succeed). If a future runner runs
   pin-check as a different user over a scratch owned by another, `git -C <tree>` commands refuse and
   the pin flips to env. Latent only.
5. **Branch inventory is the whole source ref set.** The clone exposes `origin/*` refs for every
   lane branch plus `origin/HEAD`; an instrument reading `origin/master`/`origin/HEAD` (e.g.
   round-17 census-style probes) now resolves inside the tree where it previously resolved to the
   enclosing lane or failed. Not exercised by the current registry.
6. **Hooks / LFS / export-ignore / export-subst: no difference found.** Hooks are inactive samples
   (same in fixture repos); no `.gitattributes` exists at R, so export-ignore/export-subst and LFS
   are inert in both shapes; tracked-file content is identical (verified).

## 4. Verdict for the claim

- The clone-shape change is **real and load-bearing** for two pinned selftests (round-49 count-c1,
  round-19 regressions); without a repository in the tree, the registry fails 4 checks. The L1's
  direction is supported by evidence.
- The tree is **not a function of R alone**: it embeds a live snapshot of the source repo's refs
  (master ≠ R today), plus a hard dependency on the lane's object store. This is a named limit, not
  a current failure — no observed pin result changes between clone and archive except the two that
  require a repository, and all 35 pins match at both revs (v4@enter == v5@enter per-pin;
  v5@data met).
- `class=env` vs `class=stale` labeling worked as claimed in the archive counterfactual (both
  failing pins got `class=stale`, because they printed a tally then failed — consistent with the
  contract's named limit that "no tally line ⇒ env" is not what these exercised).

UNVERIFIED: behaviour when the source's master is deleted/renamed while the measured tree exists
(not triggered; derived from the observed ref state). Behaviour under a runner of a different user
(not tested).

## Findings

- **MED — ambient ref state in the measured tree.** `refs/heads/master` in the `--rev` tree tracks
  the source lane's live master (`b504cb17…`), not R (`87e0c374…`); round-49 count-c1 resolves
  `master` from the tree it runs in (`tools`/file lines 53, 313, 353, 422; v5 `export_rev`
  lines 870–886). Measurement is not a pure function of R.
- **LOW — `.git` dir (26 files) inside the measured tree.** No current pin enumerates the tree, so
  no observed flip; any future tree-walking pin sees it. (SKILL.md registry rows 166–1057.)
- **LOW — object-store dependency via alternates.** `--shared` clone reads the lane's objects; an
  archive was self-contained. Latent env-flip risk. (v5 `export_rev` line 880.)
- **LOW — safe.directory/ownership latent.** Works today (same-uid clone); fails if scratch owner ≠
  runner.
- **LOW — origin/* ref inventory now present**; unused by the current registry, visible to
  round-17-style probes.
- **INFO — no export-ignore/export-subst/LFS/hooks difference.** No `.gitattributes` at R; hooks
  samples only; LFS filters are global-only and never trigger.
- **INFO — the two repo-requiring pins.** Round-19 `pinned-oracle-validates` and round-49 count-c1
  selftest both fail in the archive counterfactual (class=stale) and pass in the clone — the clone
  shape is required and the fix is exercised.
