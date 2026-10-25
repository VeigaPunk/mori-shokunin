# MutV2Digest — round 47 w2 — mutation probe: v2 digest containment

Seat: MutV2Digest (leaf, no subagents). Date: 2026-10-25.
Target invariant: `tools/mori-pin-check.py` v2 digest pins resolve only to files **inside the measured tree** — enforced by two stacked checks in `check()` (pristine lines 371–379):

- **(a)** normpath/`..` filter: `rel = os.path.normpath(p)`; skip if `os.path.isabs(rel)` or `rel == ".."` or `rel.startswith("../")`.
- **(b)** realpath-inside-root: `os.path.realpath(fp).startswith(os.path.realpath(root) + os.sep)` (with `os.path.isfile(fp)` and digest equality).

Bytes under test: `git show 68d66ca53d89be5c34a62f46af7c37449d9f9b63:tools/mori-pin-check.py`, sha256 `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6` (= tracked file at HEAD, = lane working tree; `git status --porcelain tools/mori-pin-check.py` empty). Frozen v1 (`63eecf27…`, `e3ef425a…`) not touched — this seat attacks v2 only.

Method: three scratch copies mutated (edits only on `.scratch/r47w2-MutV2Digest/` absolute paths; no tracked path ever passed to an edit tool — wave-1 M4 rule). Detector = `--selftest` (bounded, TMPDIR under scratch). Baseline first.

## Baseline (pristine)

```
$ TMPDIR=<scratch>/tmp python3 .scratch/r47w2-MutV2Digest/v2-pristine.py --selftest
… (34 lines, all PASS) …
PIN_CHECK_SELFTEST pass=34 fail=0        exit 0
```

## Mutants, expected detector, output, verdict

### (a) remove normpath/`..` filter — SURVIVED

Diff (mutant-a.py lines 371–375): `rel = os.path.normpath(p)` + the `isabs`/`..`/`../` skip replaced by `rel = p`; realpath check (b) untouched.
Expected detector: `v2_digest_path_traversal` selftest case (`../outside.py` with a real out-of-tree file whose digest matches).
Output: `PASS v2_digest_path_traversal … PIN_CHECK=unmet … mismatches=1`; `PIN_CHECK_SELFTEST pass=34 fail=0`, exit 0.
Verdict: **survived**. Coverage finding, not a contract break: while (b) is present it subsumes (a) — `root/../outside.py` normalizes outside `realpath(root)` and (b) rejects it, so no selftest case (and no PATH_RE-reachable input) distinguishes (a). (a) is defense-in-depth only; the selftest never exercises it independently. sha256 after: `893a0e7351896033b637bdbcf12908294a3e90f0d238b7f3d8a3ab652710d1ec`.

### (b) remove realpath-inside-root check — SURVIVED selftest; breaks under reproducer

Diff (mutant-b.py line 376): condition reduced to `os.path.isfile(fp) and sha256_file(fp) == digest`; (a) untouched.
Expected detector: same `v2_digest_path_traversal` case.
Output: `PASS v2_digest_path_traversal … PIN_CHECK=unmet`; `PIN_CHECK_SELFTEST pass=34 fail=0`, exit 0.
Verdict: **survived** — the selftest has no symlink case, so the realpath arm is untested. Per tasking, reproducer constructed (below); the invariant it protects demonstrably breaks. sha256 after: `c9e1fdc9859d396d6db486bf314791973271aa4d64e035f3bba12076ce4d9295`.

### (c) both removed — KILLED

Diff (mutant-c.py lines 371–374): (a)+(b) removed as above.
Expected detector: `v2_digest_path_traversal` must flip to met.
Output: `FAIL v2_digest_path_traversal  PIN_CHECK=met tally_pins=1 digest_pins=1 mismatches=0 …`; `PIN_CHECK_SELFTEST pass=33 fail=1`, exit 1.
Verdict: **killed** by `--selftest`. sha256 after: `aa2fab185c5fdd91b6710a5acabcc0c283afe1abcd3947115cbd03588f20b7e2`.

## Reproducer for (b) — symlink inside the tree (as tasked)

Fixture (all under `.scratch/r47w2-MutV2Digest/repro-b/`):

```
repro-b/outside/secret-target.py          # "TAMPERED-BYTES-B\n", OUTSIDE measured tree
repro-b/tree/tools/foo.py                 # prints FOO_SELFTEST pass=3 fail=0, rc 0
repro-b/tree/tools/link.py -> ../../outside/secret-target.py   # symlink INSIDE the tree
repro-b/tree/SKILL-b.md                   # registry: tally pin + digest pin of `tools/link.py`
repro-b/tree/SKILL-c.md                   # same row, digest pin of `../outside/secret-target.py`
```

Target digest `d6ee1e3cd02e5febdb189c22b0eb89ab32eb63205977c711e71f238375d621c8`. Invocation: `TMPDIR=<scratch>/tmp python3 <script> --root repro-b/tree --skill <SKILL-x.md> --repo <scratch>/repro-b` (`--repo` pinned inside scratch so the tool's own `.scratch` stays in bounds).

```
pristine x SKILL-b.md -> rc=1
  pin line=3 kind=tally prefix=FOO_SELFTEST state=match … rc=0
  pin line=3 kind=digest state=mismatch digest=d6ee1e3cd02e file=None
  PIN_CHECK=unmet … mismatches=1
mutant-b  x SKILL-b.md -> rc=0
  pin line=3 kind=tally prefix=FOO_SELFTEST state=match … rc=0
  pin line=3 kind=digest state=match digest=d6ee1e3cd02e file=tools/link.py
  PIN_CHECK=met … mismatches=0          ← FALSE GREEN
pristine x SKILL-c.md -> rc=1
  pin line=3 kind=digest state=mismatch digest=d6ee1e3cd02e file=None
  PIN_CHECK=unmet
mutant-c  x SKILL-c.md -> rc=0
  pin line=3 kind=digest state=match digest=d6ee1e3cd02e file=../outside/secret-target.py
  PIN_CHECK=met                          ← traversal escape (consistent with selftest kill)
```

Reading: with (b) removed, a digest pin is "satisfied" by bytes read **through a symlink that leaves the measured tree** — the pinned digest no longer attests to any in-tree file. Pristine v2 rejects both vectors (`file=None`, unmet); mutants (b) and (c) accept them (`PIN_CHECK=met`, rc 0).

## Verdict summary

| Mutant | --selftest | Reproducer | Verdict |
|---|---|---|---|
| (a) no normpath/`..` filter | pass=34 fail=0, rc 0 | n/a (shadowed by (b)) | **survived** — coverage finding: (a) is redundant behind (b), never independently exercised |
| (b) no realpath-inside-root | pass=34 fail=0, rc 0 | symlink `tools/link.py` → out-of-tree: pristine unmet / mutant **met** | **survived selftest, breaks invariant** — selftest gap: no symlink-escape case |
| (c) both removed | pass=33 fail=1, rc 1 (`v2_digest_path_traversal` FAIL) | `../outside/…` row: pristine unmet / mutant met | **killed** |

Takeaway (report only; contract unchanged): v2's digest containment is a single point of enforcement — the realpath check (b). The selftest arms the `..` vector but not the symlink vector, so a regression deleting (b) would ship green. A selftest case pinning a digest of an in-tree symlink to an out-of-tree file (expect `state=mismatch`) would close the gap; (a) remains defense-in-depth.

## Restoration evidence

- Tracked `tools/mori-pin-check.py` after all runs: sha256 `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6` = HEAD blob (`git show HEAD:tools/mori-pin-check.py | sha256sum`) = before-state; `git status --porcelain tools/mori-pin-check.py` empty (rc 0). Tracked file never opened by an edit tool; all mutations lived in scratch copies.
- Scratch pristine copy unchanged: `9832e38c…` before and after.
- No git/jj mutating commands run; no pacman; no subagents; all runs with TMPDIR under `.scratch/r47w2-MutV2Digest/tmp`; tool's own scratch pinned under `repro-b/` via `--repo`.
- UNVERIFIED: nothing material — every claim above carries its command output and exit code. Not in scope: running the tool against the real lane SKILL.md registry (C1/C2 seats cover that).
