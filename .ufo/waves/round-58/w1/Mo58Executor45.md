# Mo58Executor45 — C1 MANIFEST binding probe (round 58, wave 1)

Seat role: executor, bounded scratch fixture only. **No production file, corpus registry,
SCORECARD, LOG, MANIFEST or lane VCS was edited.** Lane `HEAD` unchanged at
`4272736cfc5147586e1543413772f80daf44b04b` before and after this seat.

Frozen artifacts used (verified byte-identical, not copies-with-edits):

| artifact | sha256 | source |
|---|---|---|
| `.ufo/waves/round-58/count-c1.py` | `6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b` | `git show fe8801120a67c1a6b8899d7d0423839caa09e7d0:.ufo/waves/round-58/count-c1.py` == worktree bytes |

Freeze revision `fe8801120a67c1a6b8899d7d0423839caa09e7d0`. Entering revision
`b783d0b892637ce8d20f188cad20e4d8913ca635`.

## 0. Baseline and stated controls reproduce

```
$ python3 .ufo/waves/round-58/count-c1.py fe8801120a67c1a6b8899d7d0423839caa09e7d0
C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=fe8801120a67c1a6b8899d7d0423839caa09e7d0   (rc 0)

$ python3 .ufo/waves/round-58/count-c1.py --selftest
C1_SELFTEST pass=4 fail=0   (rc 0)

$ git cat-file -e b783d0b892637ce8d20f188cad20e4d8913ca635:.ufo/waves/round-58/count-c1.py
fatal: path '.ufo/waves/round-58/count-c1.py' exists on disk, but not in 'b783d0b8...'   (rc 128 → counter absent at entering rev ✓)

$ python3 .ufo/waves/round-57/count-c1.py HEAD
C1=unmet rows=0 evidence=bad rev=HEAD   (rc 1 → known wrong-table false negative preserved ✓)
```

The two §9 do-nothing controls reproduce as specified:

| contract §9 control | expected | measured |
|---|---|---|
| fixture register, two rows name a nonexistent evidence path | `C1=unmet … failed=pointers`, rc 1 | `C1=unmet rows=2 pointers=bad … failed=pointers` rc 1 ✓ |
| fixture whose only `## Capabilities` table is the stub | `binding=bad`, rc 1 | `C1=unmet … binding=bad` rc 1 ✓ |

## 1. HEADLINE FINDING — the "MANIFEST binding" is not a binding; it is two independent substring hints

The claim's element **(c)** is "each row's key bound to fleet `MANIFEST.json`
`rounds[832].capabilities_added[j]`". The counter never compares a register row to a
MANIFEST entry. It checks two things that are never joined:

* **register side** (`count-c1.py:86-87`): a line counts as a row iff it starts with `|`
  and contains the literal backticked token `rounds[832].capabilities_added[0]` or
  `[1]` **anywhere in the line**;
* **MANIFEST side** (`count-c1.py:112-115`): `rounds[832].capabilities_added[0]` merely
  contains the substring `"vote binding"` and `[1]` contains `"driver-liveness"`.

Nothing ties the row found by the first test to the MANIFEST string found by the second
test. `MANIFEST_HINTS` (`count-c1.py:40`) are loose substring hints, not the actual
capability text; and the row's *capability name cell* is never compared to anything.

### Decisive receipt — both sides wrong, still `met`

Fixture register rows named **"banana slicer calibration"** / **"teapot temperature
profiler"**, and MANIFEST `rounds[832]` set to `round=999`, `lane="other-lane"`,
`capabilities_added=["not a vote binding capability at all (unrelated)",
"nor a driver-liveness thing (unrelated)", "a third entry the register never mentions"]`:

```
HEADLINE register names AND manifest entry both unrelated
  -> rc=0 C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none
HEADLINE control, identical manifest but true names
  -> rc=0 C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none
```

The two fixtures differ only in whether the register names the real capabilities, and the
counter returns a **byte-identical `met` line** for both. The counter cannot distinguish
a correct register from a wholly fictional one.

### Full altered-names / altered-keys result table

All 15 arms below ran the **unmodified frozen counter bytes** (sha `6ecdb627…`) against
scratch git fixtures. Layout per fixture: `<root>/MANIFEST.json` (the counter's `FLEET`,
derived from `__file__`) and `<root>/lane/` (the counter's `LANE`, a throwaway `git init`
repo containing the frozen counter at `.ufo/waves/round-58/count-c1.py`). Every git
command in the harness used `git -C <fixture lane>`.

| # | fixture | expected by the claim | **measured** |
|---|---|---|---|
| 01 | baseline, exact register rows | met | `met` rc 0 ✓ |
| 02 | **register capability names replaced** ("totally unrelated widget sorter" / "zzz nothing like driver liveness") | should fail (names not the MANIFEST capabilities) | **`met` rc 0** ✗ |
| 03 | **register row names swapped** vs MANIFEST | should fail | **`met` rc 0** ✗ |
| 04 | **register capability cell emptied** | should fail | **`met` rc 0** ✗ |
| 05 | **key token only in prose**, key cell says `rounds[999].capabilities_added[0]` | should fail | **`met` rc 0** ✗ |
| 06 | **both key tokens in each of two rows** (no key↔row pairing) | should fail | **`met` rc 0** ✗ |
| 07 | MANIFEST caps reduced to bare `"vote binding"` / `"driver-liveness"` | should fail | **`met` rc 0** ✗ |
| 08 | MANIFEST caps contain **negated** hints ("not a vote binding capability at all") | should fail | **`met` rc 0** ✗ |
| 09 | MANIFEST `rounds[832]` = `round 999`, `lane "other-lane"` | should fail | **`met` rc 0** ✗ |
| 10 | MANIFEST has a **third** `capabilities_added` entry the register never mentions | should fail | **`met` rc 0** ✗ |
| 11 | **nonexistent evidence path** outside the checked prefixes (`evidence/c2-at-landed.txt`) | should fail (`failed=pointers`) | **`met` rc 0** ✗ |
| 12 | **nonexistent pointer** written `./tools/no-such.py` | should fail | **`met` rc 0** ✗ |
| 13 | **first-working-round column bogus** (3 and 999) | should fail | **`met` rc 0** ✗ |
| 14 | control: bad pointer **inside** `tools/` prefix | fail | `unmet … failed=pointers` rc 1 ✓ |
| 15 | control: key token with a suffix (`…added[0]x`) | fail | `unmet rows=0 … failed=rows` rc 1 ✓ |

Note on 02/03/04: the register row names are what the register *claims the capability
is*; the counter never reads them. Note on 05/06: `count-c1.py:86-87` uses
`any(k in ln for k in R56_KEYS)` over the whole line, so the key token may sit in a prose
cell or in both cells at once.

### Why 11/12/13 slip through (pointer arm, `count-c1.py:100-108`)

```
101  for path in re.findall(r"`([^`]+)`", ln):
102      if "/" not in path and not path.endswith((".py", ".txt", ".md")):
103          continue
104      if path.startswith((".ufo/", "tools/", "corpus/")):
105          q = _git("cat-file", "-e", f"{rev}:{path}")
```

A path is only resolved when it starts with exactly `.ufo/`, `tools/` or `corpus/`.
`evidence/c2-at-landed.txt` (arm 11) and `./tools/no-such.py` (arm 12) are silently
skipped, so a row can cite evidence that does not exist and still score `pointers=ok`.
Arm 11 is the round-57 routed defect recurring in short form: the round-56 rows' own
evidence lives under `.ufo/waves/round-56/evidence/`, and the counter would not resolve a
row that cited the short `evidence/…` form. The **first-working-round column is never
read at all** (arm 13) — nothing in the counter compares it to `56` or to
MANIFEST `rounds[832].round`.

### Why 07/08/09/10 slip through (MANIFEST arm, `count-c1.py:109-119`)

`MANIFEST_HINTS` are checked with `if hint not in caps[idx]` — a plain substring test.
Any string containing `"vote binding"` / `"driver-liveness"` passes, including negated
prose (arm 08). `m["rounds"][832]` is indexed **positionally** with no check that
`rounds[832]["round"] == 56` or `["lane"] == "mori"` (arms 09, AM, AN), so the binding
silently re-targets a different closure if the fleet list shifts. Arms 10/AB show an
extra MANIFEST capability is never noticed.

### MANIFEST is read from the **live working tree**, not from any pinned revision

`count-c1.py:111` — `json.load(open(os.path.join(FLEET, "MANIFEST.json")))`. The fleet
`MANIFEST.json` lives at the fleet root (`/home/vgpnk/Projects/shokunin/MANIFEST.json`,
fleet repo), **not** in the lane repo, and is read at its current on-disk state. Fixture
H mutated `MANIFEST.json` *after* the lane commit and re-ran the counter on the *same*
lane revision:

```
H  manifest mutated post-commit (rev d7aaaf3a) -> rc=1
   C1=unmet rows=2 pointers=ok manifest=bad binding=ok failed=manifest,manifest
```

The same lane revision therefore scores `met` or `unmet` depending on the state of a
file outside the measured revision. The counter pins **no bytes** of the artifact it
claims to bind (note `count-c1.py:27` imports `hashlib` but never calls it — `grep` finds
`hashlib` only on the import line; contrast `count-c2.py`, which uses `sha256` 5 times).
This is the C2 lesson (`copy=ok`, pinned sha256) *not* applied to C1.

## 2. Second finding — the contract's frozen target output does not match the frozen counter's output

`contract.md:30` states the frozen target output is:

```
C1=met rows=2 pointers=ok manifest=ok binding=ok selftest=ok rev=R
```

The frozen counter's actual output at the freeze revision is:

```
C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=fe8801120a67c1a6b8899d7d0423839caa09e7d0
```

Token diff: the contract's `selftest=ok` is **absent** from the counter (no `selftest=`
token is printed anywhere in `count-c1.py` — `grep -n "selftest="` matches only the
`--selftest` argv branch), and the counter emits an extra `failed=none` token the
contract does not list. The literal contract string is not a substring of the real
output:

```
target literal in actual: False
tokens in target missing from actual: ['selftest=ok']
tokens in actual missing from target: ['failed=none']
```

Under the contract's own kill rule ("any post-freeze change to the counter bytes, the
predicate sentence, or **the target output** invalidates the claim"), this matters: the
frozen target output as written can never be produced by the frozen counter bytes. C2's
counter has the same shape (`count-c2.py:109-110` emits `failed=` too, while
`contract.md:47` lists no `failed` token), so the discrepancy is systemic to the contract
text rather than to C1 alone. This is a **contract-text defect, not a counter defect** —
the counter bytes are frozen and must not change; the target-output string in
`contract.md` is the thing that does not describe them.

## 3. Third finding — register-identity selection is first-match-wins and prefix-sensitive

`_find_register` (`count-c1.py:65-75`) returns the **first** `## Capabilities` heading
whose first 12 body lines contain the binding sentence, whose body lacks `-- none yet --`,
and which contains `| key | capability |`. It does not verify that the selected section is
the *last* or *authoritative* one. Consequences measured:

* **AP** — a decoy earlier `## Capabilities` section that also carries the binding phrase
  and ≥10 key rows **hides** the real register: `rc=1 … failed=rows`. A false negative
  on a correct register.
* **AJ** — a decoy earlier section naming the phrase but with no key rows →
  `binding=bad` (also a false negative).
* **AI** — a later `## Capabilities (archived)` section is ignored: `met` (correct here).
* **AF** — the two key lines inside a **fenced code block** still count as rows
  (`met`, rc 0): the row test is `ln.startswith("|")` with no markdown-structure check.
* **AK / AL** — the real stub table's em-dash marker `— none yet —` (U+2014, `SCORECARD.md:596`
  at freeze) is **not** the literal `STUB_MARK = "-- none yet --"` (ASCII hyphens,
  `count-c1.py:29`). Both the em-dash and ASCII stub forms still yield `binding=bad`
  here only because such a stub table also lacks the `| key | capability |` header and the
  binding sentence — the stub-marker check itself never fires on the real document.

## 4. What the landed register actually contains (real-data check at the freeze revision)

The register rows at `SCORECARD.md:1989-1990` (freeze `fe8801120a67c1a6b8899d7d0423839caa09e7d0`)
are **correct in substance**:

| key | register name | MANIFEST `rounds[832].capabilities_added[j]` | first-working | manifest round / lane |
|---|---|---|---|---|
| `rounds[832].capabilities_added[0]` | `dual-shape seat-output vote binding` | `dual-shape seat-output vote binding (tools/mori-vote-bind.py, 16/16 selftest, r55 tally re-bound 78/78 …)` — register name **is a prefix** of the MANIFEST string | 56 | 56 / mori |
| `rounds[832].capabilities_added[1]` | `strict per-event driver-liveness probe` | `strict per-event driver-liveness probe over .ufo/watchdog.log (tools/mori-driver-liveness.py, 13/13 selftest, live receipt 1728 log lines / 0 malformed / 23 lanes)` — register name **is a prefix** of the MANIFEST string | 56 | 56 / mori |

Both evidence pointers resolve at the freeze revision (`tools/mori-vote-bind.py`,
`.ufo/waves/round-56/evidence/c2-at-landed.txt`, `tools/mori-driver-liveness.py`,
`.ufo/waves/round-56/evidence/c1-at-landed.txt` — all under the checked prefixes). The
`rounds[832]` index is correct in the live fleet `MANIFEST.json`
(`rounds[832].round == 56`, `lane == "mori"`, `len(rounds) == 841`).

**So the landed register is right and the counter's `met` at the freeze revision is
honest about the landed data — but the counter is not what proves it.** The `met` is
equally produced by the wholly fictional register in §1. The counter establishes *table
identity*, *pointer existence under three prefixes* and *two MANIFEST substrings*; it does
not establish the **row↔MANIFEST binding** the claim asserts.

## 5. Ruled out (things that do NOT weaken C1)

* Counter bytes are provably the frozen ones (sha `6ecdb627…` == `git show fe880112…`
  == worktree). No post-freeze byte drift.
* Round-35 active-register selection works on the real document: the counter picks the
  section at `SCORECARD.md:1953` with the 19 key rows, not the `SCORECARD.md:596` stub.
  The round-57 wrong-table false negative is genuinely fixed (r57 counter still prints
  `C1=unmet rows=0 evidence=bad` on the same bytes — the contrast the contract wants).
* `n_key_rows >= 10` padding guard works: a register with only the two r56 rows and no
  other key rows scores `binding=bad` (arm Z).
* Pointer resolution works correctly for paths **inside** `.ufo/`, `tools/`, `corpus/`
  (arms 14, M) and correctly rejects a key token with a trailing suffix (arm 15) — the
  row-identity test is token-exact.
* MANIFEST index / shape failures are handled safely: missing `capabilities_added` key,
  short `rounds` array, and a missing `MANIFEST.json` all yield `manifest=bad`, rc 1
  (arms O, P, S) via the `except Exception` at `count-c1.py:117-119`.

## 6. Risk / recommendation (no code changed — counters and contract are frozen)

1. **C1 claim (c) is over-stated relative to the frozen counter.** The counter proves
   *table identity* + *pointer existence* + *two MANIFEST substrings*. It does **not**
   prove the row↔MANIFEST binding the claim names. Minimum fix in a future round: compare
   the register row's **capability-name cell** against the MANIFEST
   `capabilities_added[j]` string (the landed register's names are exact prefixes, so a
   prefix/containment test on the MANIFEST string would pass the real data and fail
   arms 02/03/04/HEADLINE), require `rounds[832]["round"] == 56` and
   `["lane"] == "mori"`, require the key token to sit in the **key cell** rather than
   anywhere in the line, and require exactly one key token per row.
2. **Pin the MANIFEST artifact**, as C2 does with `copy=ok` + sha256 — e.g. resolve
   `MANIFEST.json` through `git show` at a pinned fleet commit and record its sha256, so
   the count is a function of the measured revision only. Today the count depends on a
   live file outside the measured revision (arm H).
3. **Broaden pointer resolution** to any repo-relative path (drop the three-prefix
   allow-list) and check the **first-working-round** column against the MANIFEST round.
4. **Correct `contract.md:30`** (and `contract.md:47`) so the frozen target output
   matches the frozen counter's real token stream, or record explicitly that
   `failed=none` / no `selftest=ok` is the intended string. As written, the target output
   is unreachable by the frozen bytes.

**Detection only.** No remediation performed; no production file, contract, counter,
SCORECARD, MANIFEST, corpus registry or lane VCS was modified by this seat.

## 7. Evidence hygiene

* Scratch root: `/fast/scratch/hyaku/mori-r58/Mo58Executor45/` (`TMPDIR` set there for
  every counter run; the counter's own `--selftest` uses `tempfile.mkdtemp` under
  `TMPDIR`).
* Every fixture repo was `git init`-ed at an explicit scratch path; every git call used
  `git -C <that path>`; no commit was made outside the throwaway fixture repos; the lane
  repo's `git log`/`HEAD` are unchanged (`4272736c…`).
* `scripts/hyaku/disk-guard.sh status` was green before the heavy pass and before writing
  (124.0G free on `/tmp`, 552.5G on `/fast/scratch/hyaku`); no ENOSPC was hit.
* Scratch cleaned before yielding (fixture trees and harness scripts removed).
* Nothing was written outside
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-58/w1/` and this seat's
  scratch root. No fleet-root or sibling-repo writes.
