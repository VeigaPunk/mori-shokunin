# W2 RevC5Tool — `tool_resolve` verification (counter `.ufo/waves/round-38/count-c1.py`)

Seat: MoriR38.RevC5Tool (wave 2, falsify). Target tip: `f725f3076972e6e70595b5ac8279be524a111ff8`.
All commands re-run by this seat 2026-10-23; outputs verbatim. No installs performed.
No scratch files needed (all probes one-shot); exactly one file written (this report).
No `lsp` device exists in this seat's toolset; definitions were read directly and every
behavioral claim below is grounded in an executed command.

## Pin integrity

Exercised file is byte-identical to the pinned revision:

```
$ git show f725f3076972e6e70595b5ac8279be524a111ff8:.ufo/waves/round-38/count-c1.py | sha256sum
9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e  -
$ sha256sum .ufo/waves/round-38/count-c1.py
9ebf10a117851c7451cf3ed7aaf5d6abe176ebffde2ae379ab5dffac50a5669e  .ufo/waves/round-38/count-c1.py
```

## The four mandated calls (printed path + exit code)

| # | cwd | command (checker path abbreviated `/…/mori-shokunin/`) | printed path | exit |
|---|-----|--------------------------------------------------------|--------------|------|
| 1 | `/home/vgpnk/Projects/shokunin/mori-shokunin` | `python3 .ufo/waves/round-38/count-c1.py --print-tool .ufo/waves/round-38/fixtures/summary-only.py` | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/fixtures/summary-only.py` | 0 |
| 2 | `/` | `python3 /…/mori-shokunin/.ufo/waves/round-38/count-c1.py --print-tool .ufo/waves/round-38/fixtures/summary-only.py` | `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/fixtures/summary-only.py` | 0 |
| 3 | lane | `python3 .ufo/waves/round-38/count-c1.py --print-tool /etc/passwd` | `/etc/passwd` | 0 |
| 4 | lane | `python3 .ufo/waves/round-38/count-c1.py --print-tool ../../../../../etc/passwd` | `/etc/passwd` | 0 |
| 5 (extra) | lane | `python3 .ufo/waves/round-38/count-c1.py --print-tool ../outside.py` | `/home/vgpnk/Projects/shokunin/outside.py` | 2 |

Calls 1–2 (acceptance: lane-relative resolves to the lane absolute path from both cwds): **MET**.
Call 2 exercises the round-37 R4 fix — resolution is against `--repo`, whose default
`DEFAULT_REPO = "/home/vgpnk/Projects/shokunin/mori-shokunin"` is a hard-coded lane literal
(`count-c1.py:68`), never `os.getcwd()`.

## Why the outputs are what they are

- `resolve_tool` (`count-c1.py:914-918`): absolute paths pass through `abspath` unchanged;
  relative paths are joined to `abspath(repo)`. `os.path.abspath` normalizes `..` lexically —
  there is **no containment check** and no symlink (`realpath`) use here.
- `--print-tool` branch (`count-c1.py:953-956`): prints the resolved path, returns 0 iff
  `os.path.isfile(resolved)` else 2. It is a disclosure probe — it never executes the path.
- Checker side: `conform.py:156-163` runs the counter with `--repo` and requires exit 0,
  `isabs`, `isfile`, and `realpath(resolved)` under `realpath(repo)` — but only for its own
  in-repo fixture (`FIXTURE_REL`); the checker never probes rejection of outside paths.

## Findings by severity

**None blocking.** No acceptance FAIL condition triggered.

- **LOW (residual, containment gap — unclaimed by P-C5, not silent):** `resolve_tool` performs
  lexical normalization only, so a `..`-escaping path that lands on an *existing* file outside
  the lane returns exit 0 — call 4 printed `/etc/passwd`, exit 0, and call 5 proves a
  repo-relative path *resolves outside the lane* (`../outside.py` →
  `/home/vgpnk/Projects/shokunin/outside.py`; exit 2 only because the file is absent; had it
  existed it would have exited 0). This is not "accepted silently" under this seat's bar: the
  probe's sole behavior is to print the exact resolved target, and nothing is executed. It is
  also consistent with the documented design — `--tool FILE` is an arbitrary-file control
  (`count-c1.py:10-11`), so lane-external controls are intentional, and a non-Python outside
  file fails visibly in the child rather than passing. P-C5 (`contract.md:62`) claims only
  "resolves a repo-relative `--tool` path against the lane" — a resolution claim, not a
  confinement claim — so no round claim is violated. If confinement is ever wanted, the fix is
  a `realpath` containment check in `resolve_tool` plus a conform mutation; until a claim
  asserts it, this stays a named residual.

## Acceptance verdict

**PASS** — lane-relative resolution returns the lane absolute path with exit 0 from both the
lane cwd and `/`; the outside path and the `..`-escaping path are accepted only with their
resolved targets printed in full (never silently), and the escaping-missing path is rejected
exit 2.

## Residual risk / verification gaps

- The exit-0-on-existing-escape behavior (call 4) is real and reproducible; risk is bounded by
  full path disclosure and by `--print-tool` executing nothing. Not re-probed with a
  lane-external executable fixture, since that would exercise the documented control mechanism,
  not a claimed invariant.
- Resolution uses `abspath`, not `realpath`: a symlink inside the lane pointing outside would
  also resolve (exit 0) — same LOW residual class, not separately exercised.
- Fixture existence was observed (calls 1–2 exit 0 requires `isfile`), not separately hashed.
