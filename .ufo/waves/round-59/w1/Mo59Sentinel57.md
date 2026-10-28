# Mo59Sentinel57 — boundary audit (round 59, w1)

Scope: every counter/tool/seat action stays read-only on lane git, never writes
outside scratch/wave dirs, never reads session/secret material.
Mode: read-only on the lane; all fixture repos, clones and PoC victims live under
`/fast/scratch/hyaku/mori-r59/Mo59Sentinel57/` (cleaned after this report).
Freeze `60b3a76a…` (amended ccfd554e), entering `2b9f0397…`. Counter runs on the
sandbox clone at `8ff344ff18924c1ea63d46c3b3969f9fea05bc51` (lane HEAD during the
audit). No production edits, no lane/fleet VCS mutation, no subagents.

Tools under audit (sha256 at HEAD, both equal the frozen PINs):
`tools/mori-register-check.py` = `38b733d8…472b8`, `tools/mori-settlement-scan.py` = `4c04bf21…ac9a9`.

Verdict: **violation found** (F1–F4). The real-path run is mutation-free and
secret-read-free (R1–R5); the defect is in the *execution + write* boundary the
counters grant repo-supplied code.

## Findings

### F1 — HIGH — counters execute the repo tool blob even when its sha256 ≠ PIN, then write repo blobs without containment/symlink checks → arbitrary file overwrite outside scratch (demonstrated)

Exploit path (both counters):
1. The lane (the thing being scored) supplies `TOOL` as a blob at rev R.
2. Both counters compute `tool_ok` but gate only the *bookkeeping*, not execution:
   `count-c1.py:100-115` (`tp.write_bytes(tool_b)` at 106, selftest subprocess 112-115,
   `run_tool()` at 64-74 called from the real arm regardless of `tool_ok`);
   `count-c2.py:204-214` (`tp.write_bytes` 206, selftest subprocess 209-214), and the
   scan/drift subprocesses at `count-c2.py:233-236` and `257-259`. Observed: the PoC
   run printed `selftest=ok` while `failed=tool_sha,…` — the unpinned blob ran.
3. That blob is executed with the invoker's cwd and the full environment (F2/F3) and
   writes anything it likes under the counter's scratch (it already legitimately
   receives `--scratch`/`--root` there).
4. The counter then materializes repo blobs into scratch paths with a plain
   `root / rel` join and `write_bytes`, following symlinks:
   `count-c1.py:77-88` (`f = root / rel` 85, `f.write_bytes(b)` 87; call sites 193 and
   the fixture arm), `count-c2.py:283-295` (entry arm, `f = root / rel` 292) and
   `335-345` (hostile-tree arm, `fp = root / rel` 345). No `realpath`/`is_relative_to`
   containment assert and no `O_NOFOLLOW` anywhere.
5. Ordering makes the chain work: the tool runs (selftest arm and/or first
   `run_tool`) *before* the counter creates the write targets, so the tool can plant
   the symlink at the exact path the counter will later write.

PoC (my own throwaway repos, `git init -q` at explicit scratch paths; never the lane):
repo `poc-c2-JWIFzc` carries `tools/mori-settlement-scan.py` (sha `1990f5f6…`, ≠ PIN)
which on `--selftest` links `<scratch>/root2/corpus/knowledge/wave-settlement-artifacts-r59.md`
to a victim file outside scratch, plus the ENTRY blob `PWNED-BY-REPO-BLOB-C2`.
Run: `cd probe3 && python3 count-c2.py 67d03d1b… --repo <poc-repo> --scratch <poc-scratch>`
→ `C2=unmet selftest=ok scan=bad … failed=…` and then:

```
== victim after C2 ==
PWNED-BY-REPO-BLOB-C2
== symlink ==
lrwxrwxrwx … <scratch>/root2/corpus/knowledge/wave-settlement-artifacts-r59.md
  -> /fast/scratch/hyaku/mori-r59/Mo59Sentinel57/victim/secret.txt   (outside scratch)
```

Same result for C1: repo `poc-c1-0uPlYw` (tool sha `12d5445d…`, ≠ PIN) prints
`pointers: ["SCORECARD.md"]`; `count-c1.py c6065e94… --repo <poc-repo> --fleet <fleet-clone> --scratch <poc-scratch>`
→ `C1=unmet selftest=ok fixtures=bad real=bad pointers=ok failed=tool_sha,fixtures_absent,real`
and

```
== victim2 after C1 ==
PWNED-BY-REPO-BLOB-C1
== symlink ==
lrwxrwxrwx … <scratch>/real/_root/SCORECARD.md -> …/victim/secret2.txt
```

Impact: a revision that ships a non-PIN tool (or a compromised lane working tree at
scoring time) gets code execution as the seat and can overwrite any file the seat can
write — lane worktree, fleet files, `$HOME` dotfiles — *before* the counter reports
its (correct) `unmet` verdict. The verdict is honest; the side effect is not.
The counter is the verification instrument and cannot use its own pin as an execution
oracle: F1 holds even though both honest tools are read-only.

Smallest remediation: (a) skip every subprocess when `not tool_ok` (wrap the three
`subprocess.run` sites in C2 and both in C1 behind the pin check); (b) write with
`os.open(path, O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW, 0o644)` after an `lstat`
regular-file check, or `unlink` first; (c) assert
`Path(os.path.realpath(p)).is_relative_to(Path(os.path.realpath(root)))` in
`materialize()` and at `count-c2.py:292`/`345`. Note: editing frozen counter bytes
trips the §kill rule, so this is a report-only defect for round 59.

### F2 — MEDIUM — repo-supplied tool inherits the invoker's cwd (C2 always; C1's selftest arm)

`count-c2.py` passes no `cwd=` at 209-214, 233-236, 257-259; `count-c1.py` passes
`cwd=str(scratch)` only in `run_tool` (line 69) and none at 112-115.
The documented invocation is "read-only from the lane repo working tree"
(`contract.md`), and every seat's process cwd is the fleet root (host guard), so the
tool's relative writes land in the lane worktree / fleet root.

Evidence: the PoC tool writes `CWD_CANARY.txt` relative to cwd.

```
== cwd canary in probe3 ==   child cwd = /fast/scratch/hyaku/mori-r59/Mo59Sentinel57/probe3
== cwd canary in probe4 ==   child cwd = /fast/scratch/hyaku/mori-r59/Mo59Sentinel57/probe4
```

i.e. exactly the counter's cwd, not the scratch dir. Impact: a relative-path write by
the tool is an untracked mutation of the lane worktree — the boundary this seat exists
to check ("read-only on lane git"). No such write occurs with the two honest tools
(R1), so this is capability, not observed damage.
Smallest remediation: pass `cwd=str(scratch)` at all five sites.

### F3 — MEDIUM — full ambient environment handed to repo-supplied code (no scrub)

`count-c1.py:112-115` and `count-c2.py:209-214` pass `env={**os.environ, "TMPDIR": …}`;
the `run_tool` calls (C1) and the C2 scan/drift calls inherit the environment
implicitly. Demonstrated with a `python3` shim on PATH that dumps child env:

```
== child env dumps ==            19
== canary visible to children == 19   (R59_SENTINEL_SECRET=canary-7f3a1c)
== distinct var names leaked ==  269
```

Every child invocation saw all 269 ambient variables. If the harness carries session
material in the environment (harness tokens, agent session ids, provider keys), the
repo blob reads it. Bounded evidence: the counters themselves never read a secret
*file* (R2); the leak is env-only, and I did not print or persist any variable values
beyond the canary I set. Smallest remediation: pass a allow-list env
(`PATH`, `LANG`, `TMPDIR=scratch`, `HOME=scratch`) to every tool subprocess.

### F4 — LOW (defense in depth) — `materialize()` has no containment assertion; `..`/absolute traversal is closed only incidentally by git

`count-c1.py:85` (`root / rel`) and `count-c2.py:292,345` join tool- and tree-supplied
relative paths with no normalisation. Today an absolute or `..` pointer cannot reach
the write because the counters pre-check with `git cat-file -e R:path`
(`count-c1.py:189`, `materialize` → `git_show`), and git resolves that lookup
literally:

```
/SCORECARD.md            reject: fatal: path '/SCORECARD.md' does not exist in 'HEAD'
tools/../SCORECARD.md    reject: fatal: path 'tools/../SCORECARD.md' exists on disk, but not in 'HEAD'
../SCORECARD.md          reject: fatal: '../SCORECARD.md' is outside repository at '/home/vgpnk/…'
tools/../../SCORECARD.md reject: fatal: path 'tools/../../SCORECARD.md' exists on disk, but not in 'HEAD'
../../../../etc/hostname reject: fatal: '../../../../etc/hostname' is outside repository
```

So the classic traversal is a no-counterexample result; the residual sink is the
symlink vector (F1), which git gating does not cover. Adding the realpath containment
assert (F1c) makes the guarantee structural instead of accidental.

## No-counterexample results (bounded method)

R1 Lane/fleet read-only on the real content. Method: two `git clone --no-hardlinks`
sandboxes (lane 19808 entries, fleet 7128), full `find -printf '%P\t%s\t%T@'` snapshot
before/after one C1 and one C2 run, then a second run with `chmod -R a-w` on the
clone's `.git` and worktree.

```
== lane snapshot diff == (end)
== fleet snapshot diff == (end)
== read-only clone rerun ==
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=8ff344ff…
C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad tree=bad …
```

Zero changed/new/deleted entries in either snapshot, and identical verdicts against a
write-protected clone: no write attempt on the repo. Git surface is read-only by
construction: only `show` (2 call sites), `ls-tree` (4), `cat-file -e` (2) — no
add/commit/checkout/reset/push, no `os.chdir`.

R2 No secret/session reads by counters or tools. Method: full source read of
`count-c1.py`, `count-c2.py`, `tools/mori-register-check.py`,
`tools/mori-settlement-scan.py`; grep for `urllib|requests|socket|http|expanduser|.ssh|token|secret`.
Result: NONE (the only hit is the word "pointers" in a docstring). Inputs are argv
paths, `git show` blobs, `corpus/SOURCES.md`, `MANIFEST.json`; outputs are scratch-only.
`mori-register-check.py` writes only in `_fixture`/`selftest` (211-216, 240-249);
`mori-settlement-scan.py` writes only in the selftest `write()` helper (135-137) under
its mkdtemp (130-132); `main()` → `scan(args)` is read-only.

R3 Scratch discipline. With `--scratch` given, the counters write only under it, and
`TMPDIR` is left clean:

```
== TMPDIR residue ==            0     (fresh TMPDIR + --scratch)
== probe residue ==   probe1:(empty) probe2:(empty)
```

(Without `--scratch` both counters fall back to `tempfile.mkdtemp` in `TMPDIR`/system
tmp — `count-c1.py:259`, `count-c2.py:447`; not a violation, but the counters accept
rather than require the explicit path the contract routed for C2.)

R4 Hostile inputs are read as data, writes stay inside scratch. Fixture/tree paths
come from `git ls-tree` (no `..` possible in a tree path) and every materialisation is
`git show`-gated; `eval_entry` reads `root / cfile` only for `cfile in ARTIFACTS`
(`count-c2.py:140-149`, membership check precedes the read). C2's selftest
`shutil.rmtree` (425) is confined to its own `mkdtemp`.

R5 Seat-level actions. `w1-dispatch.json`: 64 declared `Report:` targets, all under
`.ufo/waves/round-59/w1/`; no `git add/commit/push/checkout/reset`, no `jj`, no
`rm -rf`, no `chmod`, no out-of-tree write instruction in the 64 task strings.
My own writes: this report plus scratch; no PATH directory, no fleet-tracked file, no
lane VCS command beyond `show/ls-tree/cat-file/log/rev-parse`.

## Observed state, not a defect

At HEAD `8ff344ff` C2 is still `unmet` because the six `corpus/evidence/sources-r59/`
copies and the entry are not committed yet (`failed=copy_absent:…,entry_absent,tree`).
C1 is `met` on the same clone. Recorded only so the receipt is not read as a counter
failure.

## Method limits

- Analysis of the two frozen counters and the two pinned tools only; no other seat's
  scratch or report was read, and no sibling runtime was judged.
- The PoC tool is *my* hostile blob, not a claim that the lane's pinned tools are
  hostile; both honest tools audit read-only (R2).
- Environment leak was measured by variable count and one self-set canary; no secret
  value was printed or stored.
