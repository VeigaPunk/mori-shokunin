# RevC5Scratch — `scratch` check review (wave 2, mori round 38)

Scored tip: `f725f3076972e6e70595b5ac8279be524a111ff8`. Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only; counters run as-is; my scratch under `.ufo/waves/round-38/scratch/RevC5Scratch/`).

## Commands actually run

- `python3 .ufo/waves/round-38/conform.py f725f3076972e6e70595b5ac8279be524a111ff8 --counter .ufo/waves/round-38/count-c1.py --counter .ufo/waves/round-38/count-c4.py` → **`CONFORM=met`, exit 0** (3.4s). All six checks PASS; scratch detail below.
- AST enumeration of every `mkdtemp(` call in both counters (7 sites, matching grep).
- Live falsification: imported `count-c1.py` read-only (`__name__ != "__main__"` — defs only), overrode `SCRATCH_ROOT` in memory, called `_scratch_parent()` + `tempfile.mkdtemp` directly. All dirs created by my run were removed.

## mkdtemp inventory (grep = AST, exhaustive)

`count-c1.py` — 6 calls, every one passes `dir=`:

| file:line | `dir=` argument | resolves to |
|---|---|---|
| count-c1.py:838 | `CHALLENGE_PARENT` | `SCRATCH_ROOT` (line 71) — always round-38 root |
| count-c1.py:906 | `candidate` | `_scratch_parent()` loop var: `SCRATCH_ROOT`, else `$TMPDIR`, else `/tmp` |
| count-c1.py:983 | `_scratch_parent()` | same fallback chain |
| count-c1.py:1020 | `_scratch_parent()` | same fallback chain |
| count-c1.py:1040 | `parent` | `parent = _scratch_parent()` (line 1039) |
| count-c1.py:1092 | `parent` | same |

`count-c4.py` — 1 call:

| file:line | `dir=` argument | resolves to |
|---|---|---|
| count-c4.py:264 | `SCRATCH_ROOT` | always round-38 root (`os.makedirs(SCRATCH_ROOT)` at :263 first) |

**No `mkdtemp()` without `dir=` remains in either counter.** `SCRATCH_ROOT = os.path.join(DEFAULT_REPO, ".ufo", "waves", "round-38", "scratch")` (count-c1.py:70, count-c4.py:45). No `TemporaryDirectory`/`NamedTemporaryFile`; `os.makedirs` sites (:436, :837, :905, count-c4:263) create only the sandbox corpus dir inside a mkdtemp root or the parents themselves.

## Checker detail (from the run)

```
check scratch   PASS (count-c1.py: mkdtemp_dir=True root=True; count-c4.py: mkdtemp_dir=True root=True)
```

Backed by the grep: `mkdtemp_dir=True` ⇔ all 7 sites carry `dir=` (verified); `root=True` ⇔ both `SCRATCH_ROOT` assignments literally contain `".ufo"`, `"waves"`, `"round-38"`, `"scratch"` (verified at count-c1.py:70, count-c4.py:45). The conformance command **passes as specified**.

## Findings

### M1 (medium — falsified "every scratch dir under round-38/scratch"): `_scratch_parent()` escapes the root

`count-c1.py:898–911` tries `SCRATCH_ROOT`, then `$TMPDIR`, then `/tmp`. So 5 of 6 mkdtemp sites (probe :906, tool_dir :983, real-only :1020, blind :1040, negatives :1092) do **not** guarantee placement under `.ufo/waves/round-38/scratch`. Observed live:

- `SCRATCH_ROOT` pointed at an unwritable path in-memory, `TMPDIR` unset → `_scratch_parent()` returned `/tmp`; `mkdtemp(prefix="c1-", dir=…)` created **`/tmp/c1-3h1q0f60`** — outside the round-38 root.
- With `TMPDIR=$LANE_SCRATCH/RevC5Scratch/env-tmpdir` → parent env-redirected; scratch dir created there. Placement is environment-controlled, not lane-pinned.
- On-host corroboration: **`/tmp/mori-c1-tool-s2zsi9z8`** (mtime 2026-10-23 19:29, before this run) is a counter-created tool scratch dir already escaped to `/tmp` — the fallback has fired in the wild, today.

This contradicts the unconditional wording in the P-C5 predicate ("creates **every** scratch directory with `tempfile.mkdtemp` under the lane's `.ufo/waves/round-38/scratch`", conform.py:52–53) and count-c1's own docstring (:22: "scratch dirs are mkdtemp under the lane's .ufo/waves/round-38/scratch parent"). The `scratch` check's PASS is **not falsified** — it only asserts presence of a `dir` kwarg (conform.py:116–117) plus the `SCRATCH_ROOT` literal (:118–124) — but that PASS certifies a weaker property than the predicate claims: it never inspects the `dir=` value, so a `dir=` pointing at `/tmp` passes identically to one pointing at the lane root. The selftest's scratch mutation (:227–228) only exercises the `SCRATCH_ROOT` constant, never the `_scratch_parent` chain.

Asymmetry that sharpens it: `challenge_sandbox` (:837–838) is strict — `os.makedirs(CHALLENGE_PARENT)` then `mkdtemp(dir=CHALLENGE_PARENT)`, any failure propagates as OSError; count-c4 (:263–264) likewise has no fallback. Only the `_scratch_parent` consumers silently degrade off-lane.

### M2 (minor, out of target scope but same invariant): the checker itself violates what it enforces

`conform.py:231`: `work = tempfile.mkdtemp(prefix="mori-conform-selftest-")` — **no `dir=`**, lands in `/tmp`. Strays present: `/tmp/mori-conform-selftest-{0n3v5c_d,iz6qx2kl,rfkx4_u6}` (mtime 2026-10-23 20:05, i.e. leaked by earlier `--selftest` runs — the `shutil.rmtree(work)` at :251 doesn't fire when the process is killed mid-mutation). Not a counter, so the `scratch` check never audits it; reported as hygiene/observation, not a check defect.

### Residual risk

- If the lane scratch root ever becomes unwritable mid-run (quota, remount, `makedirs` succeeds but `mkdtemp` probe fails), count-c1 silently writes sandbox histories, tool copies and negative fixtures to `/tmp` — outside the bounds every seat in this wave was told to keep scratch inside, and pollutes a shared host dir with `c1-*`/`mori-c1-tool-*` names other seats could read or race. The strict counter (count-c4) fails loudly in the same situation; count-c1 does not.
- `$TMPDIR` is `os.makedirs`'d as a side effect (:905) — running the counter can create an env-named directory tree anywhere the user has write rights.
- None of this flips `CONFORM=met` today: the healthy path resolves `SCRATCH_ROOT` first, and my checker run confirms all six checks PASS. The gap is semantic-vs-syntactic, i.e. **the check cannot see a `dir=` that points off-lane**.

## Verdict

Checker command verified end-to-end: `CONFORM=met`, exit 0, `check scratch PASS`, and the PASS is grep-backed (every `mkdtemp(` has `dir=`; `SCRATCH_ROOT` literals correct). **FAIL on the acceptance literal**: a scratch directory provably is created outside the round-38 root by the shipped counter (`_scratch_parent()` → `/tmp` / `$TMPDIR`), making the predicate's "every scratch directory under the lane's `.ufo/waves/round-38/scratch`" false as written — the invariant holds only when `SCRATCH_ROOT` is writable, and the checker cannot tell the difference.

## Tooling

No installs or upgrades performed (stock `python3`, `git`, `stat` sufficed).

Report: .ufo/waves/round-38/w2/RevC5Scratch.md
