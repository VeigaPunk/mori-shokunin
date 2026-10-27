# Mo57Sentinel62 — C1 counter attack (round 57, w1)

Scope: frozen C1 counter only — `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-57/count-c1.py`.
Detection/report only; no production edit, no commit, no remediation of host state. Fixtures confined to
`/fast/scratch/hyaku/mori-r57/Mo57Sentinel62/`. Predicate attacked as written in `contract.md` (not broadened).

**Verdict: C1 is false-greenable.** The counter reaches `C1=met rows=2 evidence=ok`, exit 0 on rows that describe
no capability, cite evidence that does not exist, and record the wrong first-working round. It also rejects the one
placement the SCORECARD itself declares authoritative. Severity: **high for a calibration claim** — the counter is the
only instrument for C1, so a `met` it prints is not evidence that the predicate holds.

## Surface

Frozen instrument, complete (`count-c1.py`, 14 lines):

```
 9  repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"
10  s = p.stdout.split("## Capabilities", 1)[1].split("## Saturation", 1)[0]
11  rows = [line for line in s.splitlines() if line.startswith("|") and ("driver-liveness" in line or "vote-binding" in line)]
12  ok = len(rows) == 2 and all(".ufo/waves/round-56/" in x and "| 56 |" in x for x in rows)
```

Graded region at the freeze rev `618562c` (SCORECARD.md `:596-604`): the **retired stub** table —

```
596  ## Capabilities
598  | Capability | What it can now do | Evidence pointer | First-working round |
599  |---|---|---|---|
600  | — none yet — | | | |
602  Rows enter only through a round that demonstrates the capability running (AXES.md §Capabilities); none enter through this rollout.
604  ## Saturation
```

The document declares that stub dead and names a different table as the register (`SCORECARD.md:1958-1959`, the
section whose own heading is at `:1951`):

> "As the current self-assessment this register supersedes the `— none yet —` table in the first `## Capabilities`
> section (left as filed at `d677cf3`) and the per-round capability tables, none of which listed the admitted set."

So `split(..., 1)` grades a section the lane has already declared superseded and "left as filed".

## Exploit path (headline, exact bytes)

Insert two lines immediately after `SCORECARD.md:600` (`| — none yet — | | | |`):

```
| driver-liveness | | `.ufo/waves/round-56/DOES-NOT-EXIST` | 56 |
| vote-binding | | `.ufo/waves/round-56/ALSO-MISSING` | 56 |
```

Expected output of either frozen counter form: `C1=met rows=2 evidence=ok rev=<R>`, exit 0.
Observed (fixture rev `29f872d`, byte-identical predicate): `C1=met rows=2 evidence=ok rev=29f872db79a78639d4d2811bd9715829999c478a`, rc 0.

Both cited paths are absent: `.ufo/waves/round-56/DOES-NOT-EXIST` → ABSENT (round-56 holds `evidence/`,
`w1-results.json`, `w1-spec.json`, counters only). "What it can now do" is empty in both rows; no capability is claimed;
nothing is demonstrated. The row text satisfies the predicate only as substrings.

## Attack results (all run against a scratch git fixture, frozen predicate, single `repo =` line changed)

| # | Fixture (injected at SCORECARD.md:600 unless noted) | Result |
|---|---|---|
| V0 | unmodified freeze SCORECARD | `C1=unmet rows=0 evidence=bad`, rc 1 (matches `evidence/controls.txt`) |
| **V1** | dead-pointer rows above, empty capability cells | **`C1=met rows=2 evidence=ok`, rc 0** |
| **V2** | `\| driver-liveness \| a \| ... \| 56 \|` + `\| driver-liveness \| b \| ... \| 56 \|` (zero `vote-binding`) | **`C1=met rows=2`, rc 0** |
| **V3** | rows reading `NOT demonstrated; evidence absent` / `no `.ufo/waves/round-56/` artifact exists` | **`C1=met rows=2`, rc 0** |
| V4 | honest two rows in the register the file calls current (`:1951` table, key `rounds[599].capabilities_added[j]`, paths that exist) | `C1=unmet rows=0`, rc 1 |
| V5 | first `## Capabilities` renamed `### Capabilities` | `C1=unmet rows=0`, rc 1 (region jumps to `:637`) |
| V6/V8 | `## Saturation` renamed / all `## Saturation` removed | `C1=unmet rows=1` — **no exception**; `.split(...,1)[0]` on a 1-element list silently returns the whole remainder, so the region extends to EOF |
| **V7** | `\| driver-liveness \| \| 56 \| `.ufo/waves/round-56/x` \| 1 \|` (first-working round **1**) | **`C1=met rows=2`, rc 0** |
| V9 | `## Saturation` renamed + junk rows planted in the round-12 table (`:637-645`) | `C1=met rows=2`, rc 0 |
| V10 | one row naming both capabilities | `C1=unmet rows=1`, rc 1 |
| **V12** | first `## Capabilities` heading deleted + junk rows in round-12 table | `C1=met rows=2`, rc 0 |
| **V14** | `## Saturation` renamed + two bare `\|` lines in **prose** before `## Round 12` | `C1=met rows=2`, rc 0 |
| **V15** | names only as substrings: `\| driver-liveness-stub \| ... \| 56 \|`, `\| not-yet-vote-binding \| ... \| 56 \|` | `C1=met rows=2`, rc 0 |
| **V16** | both junk rows inside a ```` ``` ```` fence within the graded region | `C1=met rows=2`, rc 0 |
| V17 | honest rows placed in the retired stub | `C1=met rows=2`, rc 0 |

Fixture revs: V1 `29f872d`, V2 `97d3696`, V3 `3a7d3a1`, V4 `8568a07`, V5 `fc7b165`, V7 `861924b`, V9 `d52bc2e`,
V12 `67bb470`, V14 `f56f1a8`, V15 `188608f`, V16 `16a932d`, V17 `546500e` (scratch repo
`/fast/scratch/hyaku/mori-r57/Mo57Sentinel62/fixture{,2}`).

## Findings

**F1 (high) — capability names are a union, not a per-name binding.** `count-c1.py:11-12` filters on
`("driver-liveness" in line or "vote-binding" in line)` and checks only `len(rows) == 2`. Two rows both naming
`driver-liveness` score `met` (V2) while the predicate requires "two rows naming `driver-liveness` and `vote-binding`".
The V2 fixture makes C1 look met with the entire `vote-binding` half absent.

**F2 (high) — "resolvable" evidence pointer is never resolved.** `:12` tests `".ufo/waves/round-56/" in x`. No
`ls-tree`/`cat-file -e` arm exists; V1 and V3 pass with absent paths and with text that says the evidence is absent.
Round 35's own counter had this arm (`count-35`… `count-c1.py:61` `git(repo, "ls-tree", "-r", "--name-only", rev)`) —
round 57 dropped it, so the check regressed.

**F3 (high) — "first-working round 56" is position-blind.** `:12` tests `"| 56 |"` anywhere in the row. V7 satisfies
it from a middle cell while the actual first-working-round cell reads `1`. The frozen predicate's
"first-working round 56" is thus satisfiable by an unrelated 56 (a count, a run tally, a score).

**F4 (high) — the graded region is the section the SCORECARD declares retired, and the region is not validated.**
`:10` takes the *first* `## Capabilities` (`:596`, the `— none yet —` stub that `:1958` says is superseded) and the
first `## Saturation` or, if that string is gone, EOF. Consequences, all observed: the document-sanctioned register
at `:1951` scores `rows=0` (V4); deleting the first heading moves grading onto the round-12 table and junk rows there
score `met` (V12); renaming the terminator silently grades to EOF (V6/V8) and rows written as plain prose count (V14).
Round 35 selected the **last** matching section (`count-c1.py:68` `cap = [i for i in starts if ...]` → `s = cap[-1]`);
round 57 inverted that to the first, which is the one the file calls historical.

**F5 (medium) — rows need not be table rows, cells, or non-empty.** `:11` accepts any line starting with `|`; no
separator/header skip, no cell count, no empty-cell rejection, no key/round-column check. Hence V15 (name inside a
longer token) and V16 (rows inside a fenced block). Round 35 rejected separator rows and validated a `KEY_RE`
column; round 57 has neither.

**F6 (low) — failure-path output shape is inconsistent.** `:8` prints `C1=unmet rows=0 evidence=bad` with no
`rev=` field for a `git show` failure, whereas the controls (`evidence/controls.txt`) and every other path carry
`rev=<R>`. A parser keying on `rev=` would mis-handle that branch. (Predicate-side, not exploitable.)

**Non-finding.** The `met` path is reachable honestly: V17 places two true rows in the graded stub and exits 0. But it
is only reachable there — i.e. passing C1 as instrumented requires editing a table the SCORECARD marks
"left as filed at `d677cf3`", which conflicts with the lane's own append-only register convention. That is a design
conflict in the frozen instrument, not an executor error; the wave should record which of the two it intends.

## Impact

Any `C1=met` printed this round proves only: the graded file contains two `|`-leading lines with the two substrings,
the path fragment and a `| 56 |` cell. It does not prove two capabilities, resolvable round-56 evidence, or
first-working round 56. A seat could reach the target with a pure junk row and no capability work at all (V1), or with
docs-structure surgery and no capability row at all (V12/V14). Because C1 is a calibration claim, a false `met`
propagates into the round-57 receipt as fabricated readiness.

## Smallest remediation (report only — not applied)

Rewrite `count-c1.py:10-12` to close F1-F5 in one pass, in counter order of cheapness:

1. Region: pick the **last** `## `-level heading starting `## Capabilities` (round-35 `cap[-1]`), end at the next
   `## ` heading (not a substring match), and fail closed (`C1=unmet`, exit 2) if no such section exists.
2. Per-name binding: exactly one row per name, matched on a whole cell (strip, then compare) — not `in`.
3. Evidence: require the evidence cell to be a backticked path that `git -C <repo> cat-file -e <R>:<path>` resolves
   and that starts `.ufo/waves/round-56/`; a directory-only pointer does not count.
4. Round: require the last cell to be `56` after strip, and require the "What it can now do" cell non-empty.

Those four changes leave V1, V2, V3, V7, V12, V14, V15, V16 unmet and keep V0/V17 unchanged. The counters are frozen
post-freeze, so this is an item for round 58, not an edit now.

## Reproduction

- Fixture driver: `/fast/scratch/hyaku/mori-r57/Mo57Sentinel62/build.py`, `build2.py`.
- Predicate copy: `count-c1-fixture.py` — `diff -u .ufo/waves/round-57/count-c1.py count-c1-fixture.py` shows exactly
  one changed line (`-repo = "/home/vgpnk/Projects/shokunin/mori-shokunin"` →
  `+repo = "/fast/scratch/.../fixture"`); every other byte identical.
- Fixture repos assert `git rev-parse --show-toplevel` == their own dir before any commit; nothing outside scratch was
  written, no fleet/lane file touched. No tool was installed or updated.
