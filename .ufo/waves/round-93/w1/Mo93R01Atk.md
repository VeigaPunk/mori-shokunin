# Report: Mo93R01Atk — C2 counter attack, mori round 93 attempt 1, wave w1

Seat: Mo93R01Atk (leaf member, no subagent dispatch). Scope: attack the frozen C2 predicate
(`.ufo/waves/round-93/contract.md` C2) and its counter (`.ufo/waves/round-93/count-c2.py`)
without editing the lane. Every fixture is a scratch clone of
`/home/vgpnk/Projects/shokunin/mori-shokunin` checked out at patch base
`6d82b8d7ef6d94a5527737f9242cdf04ad018da7` (never the entering revision as a working tree base;
all `git -C $F log --diff-filter=A` probes were read-only). Scratch root:
`/fast/scratch/hyaku/mori-r93/Mo93R01Atk`, first shell line `trap 'rm -rf -- $S' EXIT`,
`TMPDIR=$S` passed explicitly to every counter run. No lane file was edited; no mutating git/jj
command ran anywhere outside scratch clones; nothing was written to /tmp, scripts/, templates/,
MANIFEST.json, .scratch, .ufo/state, sibling lanes, or the fleet root.

All counter invocations were exactly:

```
TMPDIR=$S python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-93/count-c2.py <rev> --repo <fixture>
```

Early sanity: at entering rev `7b3fe9d5` and at patch base `6d82b8d7` over the plain clone the
counter reports `home_literals=18 vgpnk_refs=18 tools=3/3 selftests=3/3 census_rc=0` (matches
the contract receipt `evidence/measure-c2-entering.txt`).

## Attack matrix

The four forms the ticket names, each built as one added file under `tools/` in its own
scratch clone commit, plus a fifth (forged repair) in a sixth clone.

### Form 1 — relative `../../<user>` home path: MISSED (named limit covers it)

Fixture `form1-relative`, commit `e1470cf779d9`, added file
`tools/mori-form1-relative.py`:

```python
import os
live = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "vgpnk", "Projects", "shokunin"))
print(live)
```

Counter output (exact, single line):

```
C2_REPORT rev=e1470cf779d9 home_literals=18 vgpnk_refs=19 tools=3/3 selftests=3/3 census_rc=0
```

`home_literals` stays at the baseline 18 — a relative `../../<user>/Projects` form carries no
`/home/` text and is invisible to `HOME_RE`. (One `vgpnk` byte-run appears in the new file,
hence `vgpnk_refs=19`; grepping the repo still finds nothing new under `home_literals` because
the regex needs a literal `/home/`. The conjunct the predicate defeats is not the one hit.)
Verdict: **MISSED**.

### Form 2 — concatenation / `os.path.join('/home','vgpnk')` home path: MISSED (named limit covers it)

Fixture `form2-concat`, commit `c9e18d253f28`, added file `tools/mori-form2-concat.py`:

```python
import os
from os.path import join
FLEET = "/ho" + "me/vgpnk/Projects/shokunin"
LANE = "/%s/%s/Projects/shokunin/mori-shokunin" % ("home", "vgpnk")
J = join("/home", "vgpnk")
print(FLEET, LANE, J)
```

Counter output:

```
C2_REPORT rev=c9e18d253f28 home_literals=18 vgpnk_refs=21 tools=3/3 selftests=3/3 census_rc=0
```

`home_literals` 18 (unchanged): the three split/join lines leave no `/home/<user>` byte-run.
`vgpnk_refs` 21 = baseline 18 + 3 new literal-ish occurrences, but note the crucial variant:
`join("/home", some_variable)` with the user name coming from argv/env/config needs **zero**
new `vgpnk` bytes and **zero** new `/home/<user>` matches, so this form defeats both conjuncts
at once. Verdict: **MISSED**.

### Form 3 — Windows and macOS forms: MISSED (not named in limit)

Fixture `form3-os`, commit `a71bab9e5c53`, added file `tools/mori-form3-os.py`:

```python
USERS = ["C:\\Users\\vgpnk", os.path.expanduser('~'), os.path.expandvars('$HOME/Projects/shokunin')]
```

Counter output:

```
C2_REPORT rev=a71bab9e5c53 home_literals=18 vgpnk_refs=19 tools=3/3 selftests=3/3 census_rc=0
```

`home_literals` 18 (unchanged). The Windows drive-letter form carries no `/home/` bytes and the
macOs forms (`~` and `$HOME`) carry none either; `HOME_RE` has no `~`, `$HOME`, or `C:\Users`
alternative legs. `vgpnk_refs` 19 = 18 + 1 (the Windows literal). Verdict: **MISSED**, and the
ticket-prompted named-limit clause covers only relative/../../ and concat; Windows/macOS and
dotted forms are two escalation classes the contract does not name. Comment: on this Linux
host the Windows form is dead code; the `~`/`$HOME` form is live on every host where the tool
runs, and among those it is exactly the "hardcodes a host path" shape the contract's C2 prose
describes, so this is an escape of the predicate, not a niche form the counter is right to
skip. verdict remains MISSED.

### Form 4 — home path ending in a dot: MISSED (not named in limit)

Fixture `form4-dot`, commit `71cf16602b1c`, added file `tools/mori-form4-dot.py`:

```python
import subprocess
DOT = "/home/vgpnk./Projects/shokunin"
subprocess.run(["rsync", "-a", "/home/vgpnk./Projects/shokunin", "/tmp/x"])
```

Counter output:

```
C2_REPORT rev=71cf16602b1c home_literals=18 vgpnk_refs=20 tools=3/3 selftests=3/3 census_rc=0
```

`home_literals` 18 (unchanged). isolated regex check:

```
$ python3 -c "import re; print(re.search(rb'(?<![>\w])/home/[a-z_][a-z0-9_-]*(?![a-zA-Z0-9_.-])', b'/home/vgpnk./Projects'))"
None
```

The negative lookahead `(?![a-zA-Z0-9_.-])` explicitly excludes the `.` class of follow-up
characters, and `/home/vgpnk.` therefore matches nowhere. Honest runtime footnote: on this
specific host the dotted spelling does **not** alias the real home (verified:
`os.path.isdir("/home/vgpnk./Projects/shokunin")` is `False`), so this escape is
static-regex-real but has no runtime effect here. The naming mistake in the regex (assuming
that the `.` is never a hostname character) is still a genuine blind spot: the register of
what the limit allows (host path spelled with a trailing dot) is exactly the kind of shape a
tool builder could reach for on a networked home (`/home/vgpnk.` as NIS/autofs home spelling
is a real form on some hosts). Verdict: **MISSED**.

### Form 5 (extra, not ticket-named) — forged repair replacing one literal with `os.path.join('/home','vgpnk')`

Two fixture runs of the same forged repair, `form5-forged` commit `f3ac180f749a` and a
second clone `clones/forged` commit `c39b57b4b2dd` — both report the same numbers (re-ran the
counter on `clones/forged` to make sure `f3ac180f749a` was not a reporting artifact; identical
`--report` output):

```
C2_REPORT rev=c39b57b4b2dd home_literals=17 vgpnk_refs=18 tools=3/3 selftests=3/3 census_rc=0
C2=unmet home_literals=17 vgpnk_refs=18 tools=3 selftests=3/3 census=ok checks_failed=home_literals,vgpnk_refs rev=c39b57b4b2dd
rc=1
```

Diff vs patch base, one line of `tools/mori-misroot-sweep.py`:

```diff
-    git -C /home/vgpnk/Projects/shokunin status --porcelain -- .ufo/waves .ufo/reports
+    git -C os.path.join('/home', 'vgpnk') status --porcelain -- .ufo/waves .ufo/reports
```

The forged tool still runs end-to-end (selftest exit 0 against the tarball extracted from
`c39b57b4b2dd`; `finding=MORI_MISROOT_SELFTEST_OK`, `sandbox_unchanged=true`,
`schema=mori-misroot-sweep-v1`). Verdict: **forge rejected** but the rejection is on a
**partial** signal: `home_literals` drops 18→17 and the run still says `unmet` only because
`vgpnk_refs=18 ≠ 0` and `home_literals=17 ≠ 0` jointly. A single-file forged repair is
therefore *visible* in the counter output as a `home_literals=17` partial drop — the counter
gives a same-commit verifier a concrete number to check against `0`, not a boolean-only
verdict. This is favorable to detection: a forge that moves only one file per commit shows up
as a partial delta, not as silence.

## Coverage table

All numbers are exact counter `--report` lines from the runs above.

| form | fixture commit | home_literals (base 18) | vgpnk_refs (base 18) | verdict | named limit covers? |
|------|----------------|--------------------------|----------------------|---------|---------------------|
| relative `../../<user>` (`os.path.join(__file__/../*/vgpnk/…)`) | `e1470cf779d9` | 18 | 19 | MISSED | yes (contract: "…relative `../../<user>` form … is not caught") |
| concatenation / `os.path.join('/home', name)` | `c9e18d253f28` | 18 | 21 | MISSED | yes (contract: "…assembled at run time by concatenation is not caught") |
| Windows `C:\Users\vgpnk` + macOS `~`/`$HOME` | `a71bab9e5c53` | 18 | 19 | MISSED | **no** (limit does not name foreign-OS or tilde forms) |
| home path ending in a dot `/home/vgpnk./…` | `71cf16602b1c` | 18 | 20 | MISSED | **no** (limit does not name trailing-dot forms) |
| forged repair `os.path.join('/home','vgpnk')` | `c39b57b4b2dd` | 17 | 18 | forge rejected (unmet, two conjuncts fail) | — (this is the predicate refusing a real partial evasion) |

## Named limit vs escalations

Contract C2 "Named limit" verbatim:

> a host path written as a relative `../../<user>` form or assembled at run time by
> concatenation is not caught; the counter reads static bytes only.

Two of the four ticket-named forms fall under that clause (forms 1 and 2). Two escalations are
**not** named there:

1. **Windows/macOS forms** (`C:\Users\vgpnk`, `~`, `$HOME` expansions) — a live and portable
   escape: `~` is real syntax on the very platform the tool runs on, and neither conjunct can
   see it.
2. **Trailing-dot home spelling** (`/home/vgpnk.`) — the regex's lookahead
   `(?![a-zA-Z0-9_.-])` explicitly excludes the dot, so the counter will never match a path
   whose user component ends in `.`; on this host the dotted spelling does not alias the
   real home (so it is a static-only blind spot today), but the exclusion of `.` from the
   lookahead is dispositive for the predicate as frozen.

## Counter design notes (non-goals, recorded for the L1, not a repair suggestion)

- The two-conjunct design (regex **and** byte count) is what closes the rename attack the
  contract's own control (`controls-r93.sh` `c2-rename` fixture, `vgpnk` → `someone`) leaves
  in play: home_literals=18 catches the renamed literal. One conjunct alone would pass it.
- `home_literals` and `vgpnk_refs` are counted over the extracted tree at R (tar extraction
  under `TMPDIR`), so a tools-only fixture commit shows changes cleanly without touching
  upstream counters or the census.
- `tools=3` and `selftests=3/3` anchor the three named tools' presence and behavior, which is
  what keeps a forge from passing by simply weakening the counted file until the counts drop
  without repairing anything (a tool deleted in counter-counted shape drops `tools` to 2, not
  a met predicate).

## Checks run vs not run

Run (with evidence as exact outputs above):

- Counter at entering and at patch base: reproduced `home_literals=18 vgpnk_refs=18 tools=3/3 selftests=3/3 census_rc=0`.
- Counter on each of the four attack fixtures + the forged-repair clone: six full counter runs
  (five `--report` + verdict `unmet` lines as quoted), all against scratch clones at 6d82b8d7.
- Extracted-archive runtime selftest of the forged `mori-misroot-sweep.py` at
  `c39b57b4b2dd`: exit 0, `MORI_MISROOT_SELFTEST_OK`.
- Isolated regex-membership probes (precompiled byte patterns, no shell regex): 4 probes
  showing the trailing-dot form never matches, and the `/home/vgpnk/Projects` form does match.

Not run (named unrun per acceptance):

- `evidence/controls-r93.sh` end-to-end (contract's own committed control evidence; not part
  of the attack scope and not needed to judge escapability).
- Any C1-related command (out of this seat's scope entirely).
- No lane commit and no patch file under `.ufo/waves/round-93/w1/patches/` — the ticket scopes
  this seat to a report only; the patches output is intentionally not written because the
  attack adds no lane change to be patched (the fixture trees are scratch, not lane
  candidates).

Report: .ufo/waves/round-93/w1/Mo93R01Atk.md
