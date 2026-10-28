# Mo59Critic21 — C1 falsification (cheapest full-met path that skips real verification)

Seat: critic, C1 only. Read-only on lane; all commits were made in throwaway
repos under `/fast/scratch/hyaku/mori-r59/Mo59Critic21/` (cleaned). Counter
used: frozen `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-59/count-c1.py`
@ freeze `60b3a76a` (bytes unchanged at tip; verified by diff of working file vs
`git show 60b3a76a:...` — identical).

## Verdict

Counterexample found. Two working constructions print the exact frozen target
line `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=R`, exit 0, on
commits that are children of live lane `master` (`7b86704d`), while the tree at
R carries **1 of the 13 required hostile fixtures** (or all 13 neutered to a
stub body) and a **fabricated SCORECARD.md** whose evidence pointers are junk
files. Real verification of the hostile corpus and of the real register is
skipped entirely; only the sha-pinned tool does any checking, and it is handed
benign inputs.

## Attack axes and what each costs

| Hypothesis | Cost | Result |
|---|---|---|
| (a) fabricated bound map — stub tool prints `REGISTER_MET` + bound JSON | ~20-line python stub | **caught**: `tool_sha` + `selftest` + all 13 fixture fails (rev `852d12e7`) |
| (b) fixture dir with a *passing* scorecard | overwrite f01 scorecard+manifest | **caught**: `failed=fixture:f01-stub-only` (rev `6693939b`) |
| (c) tool renamed (arbitrary bytes at `tools/mori-register-check.py`) | same as (a) | **caught**: sha-pinned to `38b733d8…472b8`; any byte ≠ PIN is rejected |
| (d) delete 12/13 fixtures + fabricate scorecard + junk pointers | 1 index commit | **MISSED → `C1=met`** (rev `9bd41a49`) |
| (e) keep all 13 dirs, neuter every scorecard to stub + every expect.txt to `binding` | 1 index commit | **MISSED → `C1=met`** (rev `8911a4ff`) |

## Counterexamples (receipts)

All commands run with `--repo` pointing at a throwaway repo whose `master` was
fetched from the live lane; `--fleet` used the real fleet repo
`/home/vgpnk/Projects/shokunin` (MANIFEST_REV `2807c6ab` is fleet-pinned, so the
manifest arm is honest). Parent commit of both attack commits is the live lane
tip `7b86704d` ("round-59: data correction — K11 demoted…").

### V1 — corpus deletion + fabricated register

Tree at `9bd41a49d1d640acd4dbaac39f0e7565dccd9332` = `7b86704d` minus
`fixtures-c1/f02…f13` (12 dirs removed from the index), plus:

- `SCORECARD.md` replaced by a 9-line fabricated register — one `## Capabilities`
  section self-declaring "current capabilities register", exactly the two
  required keys, correct names/`56`, **no stub section at all**.
- `junk/e0a.txt`, `junk/e0b.txt`, `junk/e1.txt` added; each blob is the literal
  bytes `junk content, not evidence`. The fabricated rows cite them as
  `evidence`; the tool accepts them (existence only, tool.py:185-186
  `(Path(root)/rel).is_file()` — content never read) and the counter
  `cat-file -e`s them successfully.

Result:

```
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=9bd41a49d1d640acd4dbaac39f0e7565dccd9332
exit=0
```

A single stub-only fixture (f01, the weakest of the frozen 13 — `expect.txt` =
`binding`) is the *entire* hostile corpus the counter verified.

### V2 — corpus neutering (even weaker per-fixture)

Tree at `8911a4ff5fff32e161a8219b0126aba153bb63b7`: all 13 dirs kept, but every
`*/scorecard.md` replaced by the 8-line stub and every `*/expect.txt` replaced
by `binding`. Verified: `f03-dup-key/scorecard.md` at R2 is the stub; its
`expect.txt` is `binding` (was `keys` at freeze). Result:

```
C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=8911a4ff5fff32e161a8219b0126aba153bb63b7
exit=0
```

Since `expect.txt` is wave-controlled, any input that makes the pinned tool fail
with *any* reason prefix is declared "hostile coverage". The fixture arm only
proves "the tool rejects 13 arbitrary bad inputs whose declared reasons match",
not the frozen 13 trees.

### Baselines

- `count-c1.py 8ff344ff` (dispatch tip): `C1=met … exit=0`
- `count-c1.py 7b86704d` (current master): `C1=met … exit=0`
- C1 is already met at the freeze commit itself (`ccfd554e` contains tool +
  fixtures + counters): the wave's "landing" arm is degenerate — nothing after
  `60b3a76a` can change C1 while counter/tool/fixtures stay frozen. (Context,
  not a defect.)

## Root causes (line pointers, `count-c1.py` @ `60b3a76a`)

1. **Fixture set unbound** — `measure()` iterates
   `git ls-tree --name-only rev:FIXDIR` (line ~125) and requires only `dirs`
   nonempty (`fixtures_absent` only if zero, ~131). No count, name, or content
   check against the frozen 13. V1 deletes 12; V2 rewrites all bodies.
2. **Expect binding is tautological** — `matched = all(any(r.startswith(e) …))`
   (~152) compares tool output to an `expect.txt` the wave authors; a wave can
   shrink each expect to the prefix its weakened input actually triggers.
3. **Real-arm scorecard unbound** — `sc = git_show(repo, rev, "SCORECARD.md")`
   (~164) takes whatever blob sits at that path. The frozen claim's premise
   ("the unique `## Capabilities` section … NOT the superseded `— none yet —`
   stub, `SCORECARD.md:1951-1953`") is never re-verified; removing the stub
   entirely makes the disambiguation claim vacuous while `real=ok`.
4. **Pointer provenance is existence-only** — tool checks `is_file()`; counter
   checks `cat-file -e`. Rows may cite any committed file as "evidence"; V1's
   `pointers=ok` was earned by three files containing `junk content, not
   evidence`. False-provenance hole on the C1 axis itself.
5. **Coverage-skipping hole (minor)** — `dirs = [n for n in names if not
   n.endswith(".py")]` (~128): a hostile fixture directory named `f14-x.py`
   would be silently excluded from the corpus.

## Impact on axes

- **Calibration (C1): direct hit.** The met verdict at V1/V2 is unsound relative
  to the frozen predicate "13 hostile fixtures … each MUST score UNMET covering
  its frozen expect prefix" — 12 fixtures were never evaluated (V1) or were
  evaluated against self-authored expects (V2).
- Depth/others: untouched (no sibling files modified; counters/contract bytes
  intact — kill rules not triggered by the attack commits since no frozen file
  changed).

## Smallest safe corrections (proposals, not edits)

1. In `measure()`: freeze `FIXTURES = {name: expect_prefix, …}` (13 entries)
   and require `set(dirs) == set(FIXTURES)`; use the frozen map instead of
   reading `expect.txt` at R (the tool may still read it — counter shouldn't
   trust it). Optionally sha-pin each `scorecard.md`/`manifest.json` blob.
2. Real arm: pin a minimal invariant on `SCORECARD.md` at R — e.g., require
   `≥2` `## Capabilities` sections and a `— none yet —` stub row present
   (or pin the register section's line range), so the stub-vs-active
   disambiguation is genuinely exercised.
3. Pointers: require each reported pointer to live under an allowlist of
   evidence roots (e.g. `tools/`, `.ufo/waves/round-56/evidence/`) or, stronger,
   verify pointer target content hash recorded in a frozen map — closes the
   false-provenance lane.
4. Drop the `.py` suffix filter (or restrict the exclusion to files) so no
   fixture dir can hide.

Note these corrections change frozen counter bytes → they belong in the next
round's counter, not this one (kill rule). For this wave the defect stands: the
C1 counter can print `met` on a tree that skips 12/13 hostile verifications.

## Controls that held

- Stub/renamed tool emitting a fabricated bound map → `unmet failed=tool_sha`
  (pin arm sound; fabricated-verdict and renamed-tool cheap paths are dead).
- Passing-scorecard fixture → `unmet failed=fixture:<name>` (REGISTER_MET on a
  fixture is caught).
- Selftest arm → `selftest` failure propagates correctly.
- Do-nothing control at entering `2b9f0397` (no tool/fixtures trees) is
  consistent with `failed=tool_absent` per contract (verified: tool blob absent
  at that rev — sha256 of `git show` output is the empty-stream hash).

## Method bounds

One wave-shaped attack surface exercised: an index-only commit reachable by any
seat with write access to the lane (integrator/landing path), no force-push, no
counter/contract mutation. Not exercised: sha256-collision forgeries (infeasible
by construction), fleet-repo substitution (`--fleet` is verifier-supplied in the
canonical invocation; if a scorer ever ran with a forged `--fleet`, the
`MANIFEST_REV` pin still holds but `rev` binding of `--repo` is caller-enforced —
the counter cannot distinguish lane repo from a forged one; this is inherent to
any repo-path CLI and is mitigated only by running the counter against the real
lane path, as the default does).
