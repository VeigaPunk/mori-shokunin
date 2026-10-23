# RevC4Capability — `source-drift re-fetch probe` path re-fetch probe (round-38 wave 2)

Seat: `MoriR38.RevC4Capability` (leaf, no dispatch). Tip under attack: `f725f3076972e6e70595b5ac8279be524a111ff8`
("round-38: C1 counter v4.1 + freeze v2 pins, C4 byte-capped reads, wave-1 spec/dispatch, attempt-2 evidence").

Fidelity preconditions, both verified by command:
- Working copy `.ufo/waves/round-38/count-c4.py` is byte-identical to the tip blob (`diff` of `git show f725f307…:.ufo/waves/round-38/count-c4.py` vs working file: clean).
- Working copy `SCORECARD.md` is byte-identical to the tip blob (`diff` clean; tip blob is 2177 lines).

## Target row at the tip (committed bytes)

`git show f725f307…:SCORECARD.md | sed -n 2059p` — `SCORECARD.md:2059`:

```
| round-37 C2 | source-drift re-fetch probe | Re-fetches every registry row with a committed copy and classifies the copy against today's body under a 4 MiB bounded read and a post-redirect public-destination policy; round 37 added `--selftest` 6 cases with two named, mutation-killable arms (the probe's live run first worked in round 36) | `tools/mori-source-drift.py`; `.ufo/waves/round-37/evidence/c2-after-v3.txt`; `.ufo/waves/round-37/evidence/drift-live-r37.txt` | 36 |
```

The row contains exactly 4 backticked tokens (enumerated with `re.findall(r"`([^`\n]+)`", …)` over the committed line):

1. `--selftest` (flag, not a path)
2. `tools/mori-source-drift.py`
3. `.ufo/waves/round-37/evidence/c2-after-v3.txt`
4. `.ufo/waves/round-37/evidence/drift-live-r37.txt`

## Resolved/missing table (independent `git cat-file -e` at the tip)

| # | cited token | path-like (PATH_RE)? | counter counted it | `git cat-file -e f725f307…:<path>` | object type |
|---|---|---|---|---|---|
| 1 | `--selftest` | no — regex `^[A-Za-z0-9_.-]+(/[A-Za-z0-9_.<>-]+)+$` requires ≥1 `/` (count-c4.py:66); token has none | no (correct: it is a flag, not a path) | n/a (not attempted; not a path claim) | — |
| 2 | `tools/mori-source-drift.py` | yes | yes | RESOLVED | blob |
| 3 | `.ufo/waves/round-37/evidence/c2-after-v3.txt` | yes | yes | RESOLVED | blob |
| 4 | `.ufo/waves/round-37/evidence/drift-live-r37.txt` | yes | yes | RESOLVED | blob |

Independent loop output (`for p in …; do git cat-file -e "$T:$p" && …`):

```
RESOLVED  f725f3076972e6e70595b5ac8279be524a111ff8:tools/mori-source-drift.py (blob)
RESOLVED  f725f3076972e6e70595b5ac8279be524a111ff8:.ufo/waves/round-37/evidence/c2-after-v3.txt (blob)
RESOLVED  f725f3076972e6e70595b5ac8279be524a111ff8:.ufo/waves/round-37/evidence/drift-live-r37.txt (blob)
```

## Counter's `check capability` detail (run, not read)

`python3 .ufo/waves/round-38/count-c4.py f725f3076972e6e70595b5ac8279be524a111ff8` → exit 0, `C4=met`, relevant line:

```
check capability       PASS (paths=['tools/mori-source-drift.py', '.ufo/waves/round-37/evidence/c2-after-v3.txt', '.ufo/waves/round-37/evidence/drift-live-r37.txt'] missing=[])
```

Counter detail matches my independent resolution exactly: same 3 paths, `missing=[]`, no path missed, no path invented. Mechanism, cited: `paths_in` (count-c4.py:154-162) pulls backticked tokens, strips trailing `.,;)`, skips `http*`, keeps PATH_RE matches; `resolves` (count-c4.py:131-134) runs the identical command `git cat-file -e <rev>:<path>`. The SCORECARD is read from the pinned rev's committed bytes (`show(repo, rev, SCORECARD_REL)`, count-c4.py:238), not the working tree.

## Last-row-wins / shadowing check

- Parser: `capability_row` (count-c4.py:146-151) keeps the **last** line that both `startswith("|")` and contains `CAPABILITY_KEY` ("source-drift re-fetch probe", count-c4.py:46) — last-row-wins by construction.
- At the tip, `SCORECARD.md` contains exactly **one** pipe-row with the key: line 2059 (`git show f725f307…:SCORECARD.md | grep -cn '^|.*source-drift re-fetch probe'` → 1). Other mentions at tip-blob lines 2071 and 2175 are prose, excluded by the `startswith("|")` guard (verified: they do not start with `|`).
- Therefore last row == first row == the target row. **No shadowing at `f725f307`.**

## Findings by severity

**FAIL-level: none.** All three acceptance conditions hold:
1. Every cited path resolves at the tip — 3/3 RESOLVED as blobs.
2. The counter misses nothing — its detail lists exactly the 3 path-like tokens and `missing=[]`; `--selftest` is correctly not treated as a path.
3. Last-row-wins does not let a later row shadow the target at the tip — only one row contains the key.

**[LOW, latent] count-c4.py:146-151 — last-row-wins is a dormant shadowing hazard.** If a future SCORECARD edit appends any later `|` row containing the key, the counter silently checks that row instead of the round-37 row. Two cases: (a) the later row cites dead/no paths → check fails (stricter, safe); (b) the later row cites *different but resolvable* paths (decoy) → the counter passes while the true row's receipts could be dead (weakening). Case (b) is not covered by the negative arms: `witness-dangling-row` is projected as the *entire* scorecard text (`check_capability(dangling_row)`, count-c4.py:313-315), which proves standalone-dangling rejection, not appended-decoy rejection. Not triggered at the audited tip (single row); no action taken (mori province — detection only).

## Residual risk and verification gaps

- The hazard above is structural and dormant; it activates only on a future second row containing the key.
- `git cat-file -e rev:path` also succeeds for tree objects, so a cited path that is a *directory* would count as "resolved". All three cited paths here are blobs, so this has no effect on this tip; noted as a general precision limit of both my probe and the counter's `resolves()`.
- No tools were installed or upgraded for this seat (nothing needed beyond repo-provided git/python3).
- Scratch artifacts: `.ufo/waves/round-38/scratch/RevC4Capability/{count-c4-tip.py,SCORECARD-tip.md,row-2059.txt}` (permitted scratch only; no lane file modified).

**Verdict: PASS** — no FAIL condition of this seat's acceptance criteria is triggered at `f725f3076972e6e70595b5ac8279be524a111ff8`.
