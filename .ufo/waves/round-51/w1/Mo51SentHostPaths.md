# Mo51SentHostPaths — portability audit (round prompt §7 item 4; QUALITY 127)

Seat: sentinel (leaf). Role: UFO-FSD sentinel — trust boundaries and failure modes from local evidence, detection and
report only. Judged revision: `87e0c374537557754bf71dd68036ded3ddc6699c` (call it T) for both greps as the item specifies;
`build-w1-spec.py` does not exist at T, so it was audited at the lane's current HEAD `b504cb1701568a0038aab9d98ec13d28eff801da`
(call it H), which is the commit that added it. No subagents, no fleet mutation, no claim re-scoring.

Scope: classify every hit of the two frozen greps (executable default that breaks off-host replay / honours TMPDIR /
prose only) and answer whether `count-c1.py`, `count-c2.py`, `controls/c1-controls.py` and `build-w1-spec.py` are
portable. The counters, predicates, controls and kill rules are frozen: every counter-side defect below is reported as
a named limit, never as a proposed fix.

## Method and raw evidence

Grep 1 (host paths), run from the lane:

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n '/home/vgpnk' 87e0c374537557754bf71dd68036ded3ddc6699c \
    -- .ufo/waves/round-51/ tools/mori-pin-check.py .ufo/waves/round-40/conform.py
87e0c374537557754bf71dd68036ded3ddc6699c:.ufo/waves/round-51/evidence/census-start.txt:1:$ scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
87e0c374537557754bf71dd68036ded3ddc6699c:.ufo/waves/round-51/evidence/census-start.txt:24:mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
87e0c374537557754bf71dd68036ded3ddc6699c:.ufo/waves/round-51/evidence/control-c1-do-nothing.txt:1:$ python3 .ufo/waves/round-51/count-c1.py aa3af1ec3118ee7766dfce1d9709ce3c0c3f6bfd --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch /fast/scratch/hyaku/mori-r51/L1/ctl/s-do-nothing
87e0c374537557754bf71dd68036ded3ddc6699c:.ufo/waves/round-51/evidence/sweep-memavailable.txt:16:## merge/mori (read-only): grep -rl -i "MemAvailable|si_mem_available" /home/vgpnk/Projects/shokuknow/merge/mori
rc=0
$ git ... grep -c '/home/vgpnk' T -- .ufo/waves/round-51/ tools/mori-pin-check.py .ufo/waves/round-40/conform.py
.ufo/waves/round-51/evidence/census-start.txt:2
.ufo/waves/round-51/evidence/control-c1-do-nothing.txt:1
.ufo/waves/round-51/evidence/sweep-memavailable.txt:1
```

=> 4 lines in 3 files, all receipts. **Zero hits in `contract.md`, `count-c1.py`, `count-c2.py`, `controls/c1-controls.py`,
`controls/witness/*`, `tools/mori-pin-check.py` and `.ufo/waves/round-40/conform.py`.**

Grep 2 (`/tmp`), run from the lane:

```
$ git -C .../mori-shokunin grep -nE 'mkdtemp\(dir="/tmp|/tmp/' 87e0c374... -- .ufo/waves/round-51/ tools/
...:949c6699c:.ufo/waves/round-51/controls/witness/conform.py:736:         'SCRATCH_ROOT = "/tmp/mori-r39-scratch"', "scratch parent moved off-lane"),
...:87e0c374...:tools/mori-census.sh:106:#     arm in isolation (/tmp/r8m/micro-disk.log) and 5x per arm through the whole
...:87e0c374...:tools/mori-census.sh:107:#     gate, interleaved (/tmp/r8m/disk-cost.log), host load ~68:
...:87e0c374...:tools/mori-census.sh:144:#     3 s apart, /tmp/r8m/mem-samples.log; cgroup walk /tmp/r8m/cgroup-max-census.sh):
...:87e0c374...:tools/mori-round15-regressions.py:109:      --fixtures .ufo/waves/round-15/fixtures --output /tmp/r15-gate
...:87e0c374...:tools/mori-silence-cases.sh:309:  WORK=$(mktemp -d /tmp/mori-silence-cases.XXXXXX)
rc=0
```

The `mkdtemp(dir="/tmp` alternative matched nothing: no counter defaults its scratch to a literal `/tmp`.
Supplementary (same tree, revision T): `/fast/` appears in 7 lines of 7 files, all receipts
(`evidence/control-c1-*.txt` ×6 at line 1, `evidence/selftests/mori-unlanded-check.txt` ×1).

Environmental facts for reading the rest: `git` = /usr/bin/git, `tar` = /usr/bin/tar, `bwrap` = /usr/bin/bwrap
(bubblewrap 0.13.1), `python3` = /usr/bin/python3. TMPDIR honouring was demonstrated mechanically under this seat's
scratch: `python3 -c 'import tempfile;print(tempfile.mkdtemp(prefix="probe-"))'` with TMPDIR set printed
`/fast/scratch/hyaku/mori-r51/Mo51SentHostPaths/tmp/probe-q1hqud5d`, while a literal `mktemp -d /tmp/probe-literal.XXXXXX`
under the same TMPDIR printed `/tmp/probe-literal.CZ1lce`.

## A. Classification of the host-path hits (grep 1)

| # | file:line | kind | class | why |
|---|---|---|---|---|
| 1 | `.ufo/waves/round-51/evidence/census-start.txt:1` | a recorded `$` command line | prose only (receipt) | the command was run with an absolute `--root`; the row text is a record, not executed by any instrument |
| 2 | `.ufo/waves/round-51/evidence/census-start.txt:24` | census output row (absolute registry path) | prose only (receipt) | census emits absolute paths in rows by design; nothing parses this file for a path |
| 3 | `.ufo/waves/round-51/evidence/control-c1-do-nothing.txt:1` | a recorded `$` command line | prose only (receipt) | receipts of the control runs are re-readable, not re-runnable off-host (their `/fast` scratch is gone by design) |
| 4 | `.ufo/waves/round-51/evidence/sweep-memavailable.txt:16` | a recorded read-only grep over `shokuknow` | prose only (receipt) | same |

Consequence: the frozen C1/C2 surface — contract, both counters, the control builder, the witness bytes, both edited
instruments — carries **no absolute host path at T**. An off-host replay of either counting command needs only the
lane tree, TMPDIR and the external binaries (§D), not this host's layout.

## B. Classification of the `/tmp` hits (grep 2)

| # | file:line | kind | class |
|---|---|---|---|
| 1 | `.ufo/waves/round-51/controls/witness/conform.py:736` | the *replacement text* of conform's own textual mutation `scratch` (anchor `SCRATCH_ROOT = os.path.join(DEFAULT_REPO, …)` → `"/tmp/mori-r39-scratch"`) | control/fixture string; executed only as a deliberately-wrong mutated copy inside conform's selftest, never a runtime default |
| 2–4 | `tools/mori-census.sh:106,107,144` | `#` comments citing old run logs (`/tmp/r8m/...`) | prose only |
| 5 | `tools/mori-round15-regressions.py:109` | a `Usage` example inside the module docstring; `--output` has no default (`add_argument("--output")`, line 2312) | prose only |
| 6 | `tools/mori-silence-cases.sh:309` | `WORK=$(mktemp -d /tmp/mori-silence-cases.XXXXXX)` on the **non-selftest** path | **executable default that ignores TMPDIR** |

Hit 6 is the only real one, and the file contradicts itself about it. Lines 300–310:

```
if [ "$SELFTEST" = 1 ]; then
  # --selftest fixtures live under the caller's TMPDIR only (never /tmp).
  case "${TMPDIR:-}" in /*) ;; *) die "--selftest requires an absolute TMPDIR" ;; esac
  [ -d "$TMPDIR" ] || die "--selftest TMPDIR is not a directory: $TMPDIR"
  WORK=$(mktemp -d "$TMPDIR/mori-silence-cases-selftest.XXXXXX") || die "mktemp under TMPDIR failed"
else
  WORK=$(mktemp -d /tmp/mori-silence-cases.XXXXXX)
fi
```

So the `--selftest` path *enforces* an absolute TMPDIR and the runtime path ignores it: with `TMPDIR=/fast/scratch/...`
exported (this round's operator directive), a normal run still builds its whole case tree on `/tmp`. Residue is not the
risk (`trap 'chmod -R u+rwX …; rm -rf -- "$MORI_CASES_WORK"' EXIT INT TERM`, line 312, removes it); the risk is that the
one lane instrument that materialises the largest fixture tree is the one that ignores the scratch directive — on a host
whose `/tmp` is a small tmpfs it is an ENOSPC/`mktemp` failure, and its work dir is not where the operator asked for it.
For contrast, the two other shell instruments use a fallback idiom that honours the variable:
`mori-census.sh:3012` `${TMPDIR:-/tmp}/mori-census-selftest.XXXXXX` and `mori-index-clean.sh:147`
`${TMPDIR:-/tmp}/mori-index-clean.XXXXXX` (portable-with-fallback, and correctly not matched by the frozen grep because
the literal is `/tmp}`).

## C. Are the four named instruments portable?

**`count-c1.py` — portable, with one failure-mode defect.** `HERE`/`DEFAULT_REPO` are derived from the file's own path
(`count-c1.py:37-38`, three `dirname`s → lane root); the default scratch is `tempfile.mkdtemp(prefix="mori-r51-c1-")`
with no `dir=`, i.e. TMPDIR (line 225); an explicit `--scratch` is refused if it lies inside the repo or inside the hidden
path (lines 226-229); arms A–D pass explicit `TMPDIR=tmpA/tmpB/tmpC/tmpD` under the per-run work dir (lines 105, 141,
174, 198). Observed proof that the repo really resolves from the file's position, not from a baked path: a copy placed
in a foreign tree (`<scratch>/fake/.ufo/waves/round-51/count-c1.py`) and run with the lane-only revision

```
$ python3 <scratch>/fake/.ufo/waves/round-51/count-c1.py 87e0c374537557754bf71dd68036ded3ddc6699c --scratch <scratch>/s1
C1_SETUP unresolvable revision 87e0c374537557754bf71dd68036ded3ddc6699c
rc=2
```

which is only possible if `DEFAULT_REPO` is that foreign tree. The defect: the revision pre-check at line 220 calls `git`
**outside** the `try:` that begins at line 232, so on a host without git the counter dies with a traceback and exit 1 —
the *unmet* code — instead of `C1_SETUP`/2:

```
$ env -i PATH=/nonexistent TMPDIR=<scratch>/tmp /usr/bin/python3 <scratch>/fake/.ufo/waves/round-51/count-c1.py 87e0c374...
FileNotFoundError: [Errno 2] No such file or directory: 'git'
rc=1
```

`count-c2.py` handles the same condition correctly (`C2_SETUP unresolvable revision`, rc=2, §D), which makes the C1
behaviour a divergence rather than a house convention.

**`count-c2.py` — portable.** Read-only (`git show` / `git ls-tree` / `git rev-parse`, docstring line 23); repo derived
from its own path (line 280) with `--repo`/`--entry` overrides; no temp files, no `mkdtemp`, no `/tmp`, no `/home`; the
selftest reads the frozen copies under the derived `lane` (lines 302-306). Observed from the same foreign tree: plain rev
→ `C2_SETUP unresolvable revision …` rc=2. Its one portability-diagnosis defect is in `--hashes`:

```
$ python3 <scratch>/fake/.ufo/waves/round-51/count-c2.py --hashes 87e0c374...
C2_SETUP entry absent at 87e0c374537557754bf71dd68036ded3ddc6699c     rc=2
```

The repo was not a repository at all; the message blames the entry. `--hashes` (line 271-278) has no revision-resolution
guard, unlike the main path (line 290-297).

**`controls/c1-controls.py` — portable.** All three inputs are positional (`c1-controls.py BASE_REV SCRATCH_DIR OUT_DIR`),
`LANE` is derived from its own path (lines 22-23), the fixture repo is a `git clone --no-local LANE` whose toplevel is
asserted before the first commit (lines 48-50), and every later git call names `-C k`. No `/home`, no `/tmp`, no baked
scratch. Two non-portability blemishes: `main(*sys.argv[1:4])` (line 94) with too few arguments prints a traceback and
exits 1 rather than a usage error/2 —

```
$ python3 .../controls/c1-controls.py
TypeError: main() missing 3 required positional arguments: 'base', 'scratch', and 'out'
rc=1
```

— and the script never removes `SCRATCH_DIR/K` or `s-*`; the caller owns cleanup (the L1 used `/fast/scratch/...`, so this
round is clean, but the script is not self-cleaning like the counters are).

**`build-w1-spec.py` — not portable (one baked path).** Not present at T; added at H. It derives the lane and fleet root
from its own location (lines 7-9) but hardcodes the scratch root:

```
20:X = "/fast/scratch/hyaku/mori-r51"
50:    items.append({"name": n, "role": role, "prompt": f"/skill:godspeed\n{n}: {text} Scratch: {X}/{n}/."})
```

No environment override and no argv input exists for it (`os.environ`, `gettempdir`, `sys.argv` absent from the file).
The value is emitted, not touched, but it *is* the instruction 68 seats obeyed (context line "Scratch (operator
2026-10-25): every clone, work tree, fixture and temp file lives under {X}/<your seat name>/"). Proof that the two path
classes are independent: a copy run from a foreign tree derived the lane correctly and still emitted this host's scratch
root —

```
$ python3 <scratch>/fake2/.ufo/waves/round-51/build-w1-spec.py        # rc=0, 68 items
Lane: … Lane repo: /fast/scratch/hyaku/mori-r51/Mo51SentHostPaths/fake2. Fleet root: /fast/scratch/hyaku/mori-r51/Mo51SentHostPaths.
- Scratch (operator directive 2026-10-25): every clone, work tree, fixture and temp file lives under /fast/scratch/hyaku/mori-r51/<your seat name>/ …
```

In the committed artifacts the literal occurs 73 times in `w1-spec.json` and 73 times in `w1-dispatch.json`
(`grep -o '/fast/scratch/hyaku/mori-r51' <file> | wc -l`). This is a repeated house pattern, not a round-51 regression:
`round-50/build-a2w1-spec.py:26` carries `X = "/fast/scratch/hyaku/mori-r50"`, while `round-48/49/build-w1-spec.py`
went further and hardcoded `L = "/home/vgpnk/Projects/shokunin/mori-shokunin"` (lines 7 there) — round 51 improved `L`/`F`
to derived and left `X` alone.

## D. External-binary dependencies of the counters

Both counters shell out to binaries with no preflight: `count-c1.py` needs `git` (lines 74, 79, 85, 156, 190, 220),
`tar` (line 191) and `bwrap` (line 140); `count-c2.py` needs `git` only. A missing binary after the pre-check is handled
the right way — an `OSError` from `sh()` propagates into `main`'s `except (RuntimeError, OSError, subprocess.SubprocessError)`
and becomes `C1_SETUP …`/exit 2, i.e. "can't run here", which is exactly the env/stale separation C1 claims. Two notes:
the missing-`git` case escapes that handler (§C), and the missing-`bwrap` case is only discovered *after* arm A has cloned
and SIGKILLed a full run, because there is no up-front `shutil.which` check. `bwrap` is present here (0.13.1), so both
counters are runnable on this host as recorded.

## E. A portability property of the v5 export the round does not name

`tools/mori-pin-check.py` v5 replaces the `git archive` export with `git clone -q --shared --no-checkout repo tree`
(lines 880-888). A `--shared` clone copies **no objects**: it records an absolute alternates path and reads every object
through the source repo. Verified on a throwaway fixture in this seat's scratch (one empty commit):

```
$ git clone -q --shared --no-checkout $D $E
--- alternates --- /fast/scratch/hyaku/mori-r51/Mo51SentHostPaths/fxA.Hxk75g/.git/objects
--- own object count --- 0
--- after the source repo moves ---
error: unable to normalize alternate object path: …/fxA.Hxk75g/.git/objects
fatal: git cat-file: could not get object info
fatal: bad object HEAD
```

Within a run this is sound — the source clone is alive and visible to the bwrap arm, and the measured tree still has a
repository of its own, which is the C1 requirement. But the measured tree is **not self-contained**: a `--keep`'d
scratch export (or anything `cp -r`'d off-host for inspection) has no objects of its own and is unreadable once the clone
it was taken from is gone. The pre-v5 `git archive` export *was* self-contained. Nothing in the contract's named limits
covers this ("arm B hides one path … does not prove portability to another host"), so it belongs in the round's limits
list even though it does not touch any verdict.

## F. Named limits of this audit (frozen or out of scope)

- Frozen-surface defects are reported, not fixed: the `count-c1.py` exit-1 traceback (§C), the `count-c2.py --hashes`
  message (§C), the `pins`/`--hashes` surfaces and every predicate are untouched.
- I did not run either full counter (that is `Mo51ExecC1Rerun`/`Mo51ExecC2Rerun`); nothing here depends on a verdict.
  `C1=met`/`C2=met` are neither confirmed nor disputed by this report.
- `build-w1-spec.py` was audited at H because it does not exist at T; the item's two greps were run exactly at T, so the
  committed `w1-spec.json`/`w1-dispatch.json` (also H) are outside their coverage and were checked separately.
- `tools/mori-silence-cases.sh:309` was classified by reading, not by running the harness (its normal mode drives real
  repos and a stub census; the construct's semantics were demonstrated separately, §A). Its write footprint was not
  measured.
- `conform.py` cosmetic: the `scratch` rule's docstring (lines 42-44) says a counter carries its scratch parent under
  `.ufo/waves/round-40/scratch`, while the code requires the literal segments `.ufo`/`waves`/`round-39`/`scratch`
  (lines 466-473) and the inspected counter is `.ufo/waves/round-40/count-c8.py:62` with `round-39` — the rule matches the
  counter and the docstring is stale. Not run here; no verdict claim.
- Portability was tested on this one host (same kernel, same user, same filesystem layout). "Portable" here means "no baked
  absolute host path and TMPDIR honoured", not "verified to run on another machine". The only cross-tree test available
  without a second host is the foreign-tree test in §C, which does prove the path derivation.

## G. Hygiene

Scratch `/fast/scratch/hyaku/mori-r51/Mo51SentHostPaths/` created (`tmp/` as TMPDIR), one fixture repo at a time, all
fixtures and probe dirs removed; nothing remained at finish. No clone of the lane was made (the foreign-tree tests used
copies of the two counters and the spec builder, and the alternates test used a two-commit throwaway repo under scratch,
whose toplevel was asserted equal to the fixture dir before committing). No `/tmp` file was created except the two
one-directory `mktemp` probes, each removed in the same command. No write outside my report and my scratch; no git/jj
mutation in the lane or the fleet root. Disk checked first:
`scripts/hyaku/disk-guard.sh status` → rc=0, `/fast` 602G free (26% used). Tool installs/upgrades: none (nothing was
needed; git 2.x/tar/bwrap 0.13.1/python3 already present).

## Findings

1. **MED — `tools/mori-silence-cases.sh:309`.** The non-selftest work dir is `mktemp -d /tmp/mori-silence-cases.XXXXXX`,
   ignoring an exported TMPDIR, while the `--selftest` branch (lines 300-307) *requires* an absolute TMPDIR. The lane's
   largest fixture tree therefore lands on `/tmp` under the round's own scratch directive; the trap at line 312 prevents
   residue but not the wrong filesystem or a small-tmpfs failure. Contrast: `mori-census.sh:3012`, `mori-index-clean.sh:147`
   use `${TMPDIR:-/tmp}`.
2. **MED — `.ufo/waves/round-51/build-w1-spec.py:20`** (`X = "/fast/scratch/hyaku/mori-r51"`), emitted 73× in
   `.ufo/waves/round-51/w1-spec.json` and 73× in `w1-dispatch.json` with no env/argv override. Lane and fleet root are
   derived (lines 7-9) but the scratch root is not, so a dispatch built from a foreign tree still directs every seat to
   this host's `/fast` (demonstrated: `Lane repo: …/fake2` in the same context as `… lives under /fast/scratch/…`).
   Repeated from `round-50/build-a2w1-spec.py:26`; landed at H `b504cb17`, not at T.
3. **MED — `.ufo/waves/round-51/count-c1.py:220`.** The `git rev-parse` pre-check is outside the `try:` at line 232, so a
   host without `git` exits 1 (traceback, the *unmet* code) instead of `C1_SETUP`/2. Observed with `PATH=/nonexistent`.
   This defeats, at the counter level, the env-versus-stale separation C1 claims; frozen, so a named limit.
4. **LOW — `.ufo/waves/round-51/count-c2.py:271-278`.** `--hashes` reports any git failure (missing repo, unresolvable
   rev) as `C2_SETUP entry absent at <rev>`; the main path (lines 290-297) reports `unresolvable revision` correctly.
   Observed from a foreign tree. Diagnosis only; exit code 2 is right.
5. **LOW — `tools/mori-pin-check.py` `export_rev` (lines 871-886).** An `OSError` (e.g. missing `git`) is folded into
   `None`, so the caller prints `PIN_CHECK_SETUP unresolvable revision` (observed, rc=2). Correct exit code, wrong cause.
6. **LOW — `tools/mori-pin-check.py:880` (`git clone --shared`).** The measured tree holds zero objects and an absolute
   alternates path to the source `.git`; a kept or relocated export is unreadable once that source repo is gone (fixture
   evidence in §E). Not among the contract's named limits.
7. **LOW — `.ufo/waves/round-51/controls/c1-controls.py:94`.** `main(*sys.argv[1:4])` with missing arguments exits 1 with a
   traceback instead of a usage error (2); and the script leaves `SCRATCH_DIR/K` and `s-*` behind (caller-owned).
8. **LOW — `.ufo/waves/round-40/conform.py:42-44`.** The `scratch` rule's docstring names
   `.ufo/waves/round-40/scratch`; the code (lines 466-473) and the inspected counter
   (`.ufo/waves/round-40/count-c8.py:62`) use `round-39`. Stale prose in the file whose portability was just fixed; also
   the rule still *requires* an in-lane scratch parent, the pattern C1 removed, but only for `DEFAULT_COUNTERS`.
9. **INFO — no finding, the positive reading.** At T the frozen round-51 surface (contract, both counters, the control
   builder, the witness bytes, `mori-pin-check.py`, `conform.py`) carries zero absolute host paths; all 4 `/home/vgpnk`
   hits and all 7 `/fast` hits are run receipts, and 5 of the 6 `/tmp` hits are comments, a docstring or a selftest
   mutation literal. `count-c1.py`, `count-c2.py` and `controls/c1-controls.py` resolve their repo from their own path and
   honour TMPDIR, so the round's C1 operability surface is off-host *path*-portable; the remaining dependencies are
   binaries (git/tar/bwrap/py3) and one baked scratch root in a build script that is not part of either claim.
