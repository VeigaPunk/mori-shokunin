# Mo58Executor43 — C1 active-register identity: trace + fixture falsification

role: executor (C1 active-register identity)
lane: /home/vgpnk/Projects/shokunin/mori-shokunin
freeze revision: `fe8801120a67c1a6b8899d7d0423839caa09e7d0`
entering revision: `b783d0b892637ce8d20f188cad20e4d8913ca635`
date: 2026-10-27
scope: read-only trace of the frozen counter + isolated throwaway-git fixtures under this seat's scratch.
no production file edited; no commit; no lane/fleet VCS mutation; no fleet/sibling write.

---

## 1. What the frozen counter actually does (independent trace)

Frozen bytes are stable — no post-freeze mutation:

```
git show fe8801120a67c1a6b8899d7d0423839caa09e7d0:.ufo/waves/round-58/count-c1.py | sha256sum
  6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b
git show 4272736cfc5147586e1543413772f80daf44b04b:.ufo/waves/round-58/count-c1.py | sha256sum
  6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b
sha256sum .ufo/waves/round-58/count-c1.py
  6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b
```
(`git diff fe880112..4272736c -- .ufo/waves/round-58/` touches only `build-w1-spec.py`,
`w1-dispatch.json`, `w1-spec.json`, `w1/swarm-registry.json` — no counter byte.)

### 1.1 Register selection (`_find_register`, count-c1.py:58-69)

The counter does **not** select by line number. It enumerates every line whose
`strip()` equals exactly `"## Capabilities"`, takes each section body via
`_section` (body = lines up to the next `## ` heading), and returns the **first**
section whose body satisfies three conjuncts (count-c1.py:67):

1. `BIND_SENT in head_zone` — `"the lane's current capabilities register"` inside
   the first **12** lines of the body;
2. `STUB_MARK not in body` — `"-- none yet --"` (ASCII) absent from the whole body;
3. `"| key | capability |" in body`.

A fourth, later gate (count-c1.py:90) requires `>= 10` lines matching
`^\| \`rounds\[` in the body.

Measured on the real corpus at the freeze revision:

```
exact '## Capabilities' heading indices (0-based): [595, 1950]  -> 1-based: [596, 1951]

--- heading @1-based 596  (the superseded stub) ---
  BIND_SENT in head_zone : False
  STUB_MARK(ASCII '-- none yet --') in body: False
  em-dash '— none yet —' in body           : True
  '| key | capability |' in body            : False
  rounds[ key rows (>=10 gate)              : 0
  -> passes _find_register admission: False

--- heading @1-based 1951  (the round-35 active register) ---
  BIND_SENT in head_zone : True
  STUB_MARK(ASCII '-- none yet --') in body: False
  em-dash '— none yet —' in body           : True
  '| key | capability |' in body            : True
  rounds[ key rows (>=10 gate)              : 20
  R56 key rows present                      : 2
  -> passes _find_register admission: True

SELECTED heading (1-based): 1951
```

So on the real bytes the stub at :596 is rejected by **conjunct 1** (no bind
sentence) and **conjunct 3** (its header is `| Capability | What it can now do |`,
not `| key | capability |`) — and **not** by the stub marker. The stub's actual
cell text is the em-dash form `— none yet —` (SCORECARD.md:600); the counter's
`STUB_MARK` literal is the ASCII `-- none yet --` (count-c1.py:37). Those are
different byte sequences:

```
STUB_MARK              = '-- none yet --'  -> [0x2d,0x2d,0x20,...,0x2d,0x2d]
corpus form            = '— none yet —'    -> [0x2014,0x20,...,0x2014]
equal: False
grep -c -- "-- none yet --" SCORECARD@freeze  -> 0
grep -c  "— none yet —"   SCORECARD@freeze  -> 2   (lines 600 and 1958)
```

**The stub-refusal conjunct is inert against this corpus.** It never fires.

### 1.2 Row selection and pointer resolution (count-c1.py:86-107)

- `rows` = **lines** of the body that start with `|` and contain **either**
  R56 key (count-c1.py:86-87). It is a line count, not a key-identity set.
- `len(rows) != 2` -> `failed=rows` (count-c1.py:96).
- For each row, every backticked token is extracted; a token is **skipped**
  unless it contains `/` or ends in `.py`/`.txt`/`.md` (count-c1.py:102-103),
  and is resolved by `git cat-file -e R:<path>` **only if** it starts with one
  of three hard-coded prefixes `.ufo/`, `tools/`, `corpus/` (count-c1.py:104).

### 1.3 Manifest arm (count-c1.py:111-118)

Reads the **live** fleet worktree file `FLEET/MANIFEST.json`
(`FLEET = os.path.dirname(LANE)`, count-c1.py:36,111) — not a pinned fleet
revision — and checks only that `capabilities_added[0]` contains the substring
`"vote binding"` and `[1]` contains `"driver-liveness"` (count-c1.py:40,
113-116). The row's own capability text is never compared to the manifest
entry.

### 1.4 Baseline measurements (frozen bytes, freeze revision)

```
python3 .ufo/waves/round-58/count-c1.py fe8801120a67c1a6b8899d7d0423839caa09e7d0
  C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=fe880112...   rc=0
python3 .ufo/waves/round-58/count-c1.py --selftest
  C1_SELFTEST pass=4 fail=0                                                     rc=0
git cat-file -e b783d0b8...:.ufo/waves/round-58/count-c1.py
  fatal: path ... exists on disk, but not in 'b783d0b8...'   rc=128   (counter absent at entering rev — control holds)
python3 .ufo/waves/round-58/count-c2.py fe880112...   -> C2=unmet entry=absent failed=entry rev=... rc=1
```

---

## 2. COUNTEREXAMPLE 1 — a first stub carrying the R56 rows is bound as the "active register" (false green)

**Fixture (assigned shape):** the superseded first stub placed **before** the
real active register, with the stub *armed* so that it satisfies the counter's
admission conjuncts (bind sentence + `| key | capability |` header + >= 10
`rounds[` key rows) and additionally carries the two R56 rows. Stub marker
spelled the way the corpus spells it (em-dash `— none yet —`).

```
=== A: stub FIRST (em-dash, the CORPUS spelling) + real active register after ===
  bound: (1951, '| `rounds[832].capabilities_added[0]` | DECOY-STUB-ROW | x | `tools/mori-vote-bind.py` | 56 |')
  measure: (0, 'C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=051944e988130d0052de9cd467fd0c76c77ceb60')
```

The counter bound the **decoy stub** (row text `DECOY-STUB-ROW`), not the real
round-35 register, and scored `C1=met` rc=0. Same content, only the stub
marker's spelling changed:

```
=== B: same but stub uses ASCII '-- none yet --' (the counter's literal) ===
  bound: (1972, '| `rounds[832].capabilities_added[0]` | dual-shape seat-output vote binding | Binds final vote ')
  measure: (0, 'C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=79be5eeaf4dde58fca7f762066f44e3212b255a3')
```

With the ASCII literal the stub is refused and the **real** register at 1972 is
bound. With the corpus's own em-dash spelling the stub is bound and the real
register is never reached. The two fixtures differ **only** in the stub
marker's hyphen-vs-em-dash bytes.

**Mechanism.** `STUB_MARK` (ASCII) is the only guard that could refuse the
stub, and it never matches the corpus spelling. The remaining conjuncts
(bind sentence, key header) are properties an *armed* stub can carry.

**This is not a hypothetical latent bug — it is a live false green on the
assigned fixture.** The counter selects the wrong table and reports the
correct verdict for it. The claim text says "the section whose preamble
self-describes as ... the round-35 register; NOT the superseded stub", and
table-identity binding is asserted "(a) table-identity binding proven against
the freeze revision". On fixture A that identity is **not** proven: the counter
cannot distinguish the real register from a stub that mimics its preamble.

**Corollary (why the defect is not self-correcting).** Naively "fixing"
`STUB_MARK` to the corpus spelling `— none yet —` makes the counter fail on
the **real** corpus, because the active register's own preamble at
SCORECARD.md:1958 mentions the stub by name:

```
active-register section body line offsets containing em-dash '— none yet —': [6]
   -> 'a rejected round, are not rows. As the current self-assessment this register supersedes the `— none yet —` table in the'
em-dash token in ACTIVE register body: True
ASCII  token in ACTIVE register body: False
with STUB_MARK='— none yet —' -> _find_register on REAL file: None   (=> binding=bad, FALSE NEGATIVE)
```

So the counter is pinned between two wrong answers: the ASCII literal lets a
stub through, the em-dash literal rejects the true register. The guard needs to
be scoped to the **stub row** (e.g. a row whose first cell is exactly the stub
token) rather than "anywhere in the body", and the assertion needs a
positive identity check on the bound table (e.g. the round-35 preamble's
`Round 35 (claim C1, calibration)` prefix and the register's own
`supersedes the ... table in the first ## Capabilities section` sentence, which
only the true register carries).

---

## 3. COUNTEREXAMPLE 2 — pointer resolution covers only three hard-coded prefixes (false green)

The contract's do-nothing control (§9) requires:

> a fixture register whose two rows name a nonexistent evidence path MUST score
> `C1=unmet … failed=pointers`, exit 1

The counter resolves a pointer only if it starts with `.ufo/`, `tools/`, or
`corpus/` (count-c1.py:104). Any other repo-relative path is **never checked**.
Measured (each fixture: one `## Capabilities` section, bind sentence, key
header, 10 pad rows, the two R56 rows, evidence cell naming a path that does
not exist):

```
  pointer docs/no-such-evidence.md  -> C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none   rc=0
  pointer evidence/nope.txt         -> C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none   rc=0
  pointer artifacts/nope.log        -> C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none   rc=0
  pointer x/nope.py                 -> C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none   rc=0
  pointer ../escape.md              -> C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none   rc=0
  pointer /etc/passwd               -> C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none   rc=0
  (control, same shape, tools/ prefix)
  pointer tools/no-such-tool.py     -> C1=unmet rows=2 pointers=bad manifest=ok binding=ok failed=pointers,pointers  rc=1
```

The §9 control arm is satisfied **only** for the three hard-coded prefixes.
A register whose two rows name a nonexistent evidence path under any other
prefix scores `C1=met` rc=0 — the exact false-green class the round-57 routed
defect 2 was meant to close ("counter false-green constructions — resolve
evidence pointers"). The route is fixed only for the prefixes the lane
happens to use; the guard is prefix-conditional rather than
"every backticked repo-relative path".

Adjacent variant (same root cause, row-level): a row whose evidence cell is
**empty** (no pointer at all) also yields `pointers=ok`:

```
P_no_evidence_pointer_in_row: (0, 'C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none')
```

The contract asserts "(b) every evidence pointer in the two rows resolved via
`git cat-file -e R:<path>`" — with an empty evidence cell the set of pointers
to resolve is empty and the assertion is vacuously true, i.e. `pointers=ok`
means "no unresolvable pointer among the pointers I chose to look at", not
"the row names resolvable evidence".

---

## 4. COUNTEREXAMPLE 3 — `rows=2` counts lines, not the two R56 keys (false green)

`rows` is a list of **lines** containing either R56 key (count-c1.py:86-87);
the only gate is `len(rows) != 2`. Duplicating `capabilities_added[0]` and
**deleting `capabilities_added[1]` entirely** still gives two matching lines:

```
=== C: duplicate key[0] twice, key[1] ABSENT from register ===
  key[1] rows in file: 0 | key[0] rows: 2
  measure: (0, 'C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=bf4c78b0d3b0bb0310c84e9a687cc00a5bd04d8d')
```

The register records **one** of the two round-56 capabilities (the
driver-liveness row is gone) and the counter reports `rows=2` / `C1=met`. The
claim is that "the two round-56 admitted capabilities are recorded"; a register
holding only one of them satisfies the counter. The gate must be on the
**key set** (both `rounds[832].capabilities_added[0]` and
`... [1]` present exactly once), not on the line count.

For completeness, the counter does reject the *opposite* shapes correctly:
`key[1]` absent with `key[0]` present once -> `rows=0`, rc=1
(`U_both_r56_rows_absent` -> `failed=rows`); a `rounds[999]` row -> `failed=rows`.

---

## 5. Secondary observations (not score-moving on their own)

1. **Target-output string in the contract does not match the counter's
   output format.** The contract freezes the target as
   `C1=met rows=2 pointers=ok manifest=ok binding=ok selftest=ok rev=R`
   (contract.md:30). The counter prints
   `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=R`
   — the sixth token is `failed=none`, and there is **no** `selftest=ok` token
   anywhere in count-c1.py (`grep -c "selftest=" count-c1.py` -> 0). The
   selftest is a separate invocation with its own line
   (`C1_SELFTEST pass=4 fail=0`), never a field of the measure line. As
   written, the frozen target output is unreachable by the frozen counter.
   (C2's target string has the same shape of problem: the counter prints
   `failed=...` too, count-c2.py:110.)

2. **The manifest arm is not bound to a revision.** The counter opens the
   **live** fleet worktree `MANIFEST.json` (count-c1.py:111), so `manifest=ok`
   reflects fleet state at run time, not at any pinned fleet revision, while
   `pointers`/`rows`/`binding` are all measured at `R`. The claim's
   "(c) each row's key bound to fleet `MANIFEST.json` `rounds[832].capabilities_added[j]`"
   is checked only by the two substring hints `"vote binding"` /
   `"driver-liveness"` (count-c1.py:40). Confirmed by fixture: manifest
   `capabilities_added = ["vote binding", "driver-liveness"]` (no tool paths,
   no capability substance) -> `manifest=ok`; and
   `["vote binding driver-liveness", "driver-liveness"]` -> `manifest=ok`.

3. **The row's own capability text is never checked against the manifest.**
   Replacing the row's capability cell with
   `totally unrelated junk capability text` still gives `C1=met`
   (`F_row_capability_text_unrelated_to_manifest` -> rc=0). The "binding" is
   one-directional: manifest -> hints only.

4. **The selftest does not exercise the guard it appears to exercise.** The
   `stub_only_binding_refused` arm (count-c1.py:203) builds its stub from
   `FIXTURE_SCORECARD`, whose stub text is the ASCII `-- none yet --`
   (count-c1.py:169) — a spelling that does not occur in the corpus — and the
   arm is refused by the missing bind sentence and the row count, not by the
   stub marker. Confirmed: neutralising `STUB_MARK` entirely
   (`"<<never-matches-anything>>"`) leaves the selftest green:
   `C1_SELFTEST pass=4 fail=0` rc=0. So the selftest cannot detect a broken
   stub guard, and it never exercises the em-dash corpus spelling.

5. **The `>= 10` `rounds[` key-row gate is undocumented and untested.** It is
   a hard `binding=bad` (count-c1.py:90-92) with no counterpart in the
   contract's predicate or in any selftest arm. A register with 8 `rounds[`
   key rows plus the two R56 rows (10 total) still passes; 7 pads + 2 R56
   rows (9) fails `binding=bad`.

6. **Round-57 contrast control holds.** The round-57 counter on the freeze
   bytes prints `C1=unmet rows=0 evidence=bad rev=...` rc=1 (it selects the
   text between the FIRST `## Capabilities` and `## Saturation`), exactly the
   known wrong-table false-negative the contract records.

---

## 6. Verdict

The C1 claim as frozen is **not falsified on the real corpus** — at the freeze
revision the counter prints
`C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=...` rc=0
and the selftest is `pass=4 fail=0`, and the counter bytes are unchanged from
freeze to the landed tip.

But the claim's own two mechanisms do not hold:

- **(a) table-identity binding** — the counter binds whichever
  `## Capabilities` section satisfies three textual conjuncts, and the only
  conjunct that could reject a stub (`STUB_MARK`) is spelled differently from
  the corpus. A stub carrying the R56 rows is bound and scored `C1=met`
  (§2). Identity is *not* proven; it is inferred, and the inference is
  defeatable by the exact fixture the assignment names.
- **(b) evidence-pointer resolution** — only paths under `.ufo/`, `tools/`,
  `corpus/` are resolved (§3). A nonexistent pointer under any other prefix,
  or an empty evidence cell, yields `pointers=ok` / `C1=met`, contradicting the
  contract's own §9 do-nothing control as written.
- **the two admitted capabilities** — `rows=2` is a line count, so a register
  holding only one of the two rows scores `C1=met` (§4).

The §9 statement "If either scores met, the counter is broken and no data is
collected" is therefore met **for the fixture the frozen selftest happens to
use** but not for the general class the control describes. On the evidence
above the C1 counter is a **calibration instrument with three reproducible
false-green constructions**, each reproducible by a reviewer/mutation seat in
one command against a throwaway fixture. The C1 claim's substance (the two
round-56 capabilities are in the round-35 active register) remains true on the
committed bytes — independently re-verified here by direct inspection
(SCORECARD.md:1989-1990, keys `rounds[832].capabilities_added[0]` and
`[1]`, evidence `tools/mori-vote-bind.py` +
`.ufo/waves/round-56/evidence/c2-at-landed.txt` and
`tools/mori-driver-liveness.py` +
`.ufo/waves/round-56/evidence/c1-at-landed.txt`, all present at
`fe880112`; fleet `MANIFEST.json` `rounds[832].capabilities_added` names
"dual-shape seat-output vote binding" and "strict per-event driver-liveness
probe"). The defect is in the counter's discriminating power, not in the
register's content.

**Recommended disposition (L1 ruling, not applied here):** the C1 counter
cannot be repaired under the kill rule ("any post-freeze change to the counter
bytes, the predicate sentence, or the target output invalidates the claim"),
so these findings cannot be remediated inside round 58 by editing the frozen
bytes. They should land as (i) a lesson/routed defect for the next round
carrying the three fixtures verbatim, (ii) a note that the C1 *substance* is
independently corroborated even though the C1 *instrument* has reproducible
false greens, and (iii) a correction of the contract's frozen target-output
string, which no frozen counter can emit.

## 7. Reproduction

All fixtures are isolated throwaway git repos created under
`/fast/scratch/hyaku/mori-r58/Mo58Executor43/` (`git init` inside that dir;
every git command `git -C <that path>`). Nothing was committed outside those
throwaway repos; the lane and fleet worktrees were read-only
(`git status --porcelain` shows only other seats' pre-existing round-58
untracked artifacts; `corpus/README.md` and `corpus/SOURCES.md` modifications
predate this seat and were not touched here). `TMPDIR` was set to the seat
scratch for every counter invocation. Scratch cleaned before yield.

Driver scripts (in seat scratch, removed at cleanup):
`driver.py` (13 cases), `driver2.py` (7), `driver3.py` (5), `driver4.py` (3),
`driver5.py` (4), `driver6.py` (3), `driver7.py` (2 + identity trace),
`driver8.py` (STUB_MARK analysis), `driver9.py` (row-count gate),
`final.py` (decisive controls), `airtight.py` (final identity evidence),
`trace.py` (per-heading admission trace).

Exact counter reads:
```
python3 .ufo/waves/round-58/count-c1.py fe8801120a67c1a6b8899d7d0423839caa09e7d0
python3 .ufo/waves/round-58/count-c1.py --selftest
git show fe8801120a67c1a6b8899d7d0423839caa09e7d0:.ufo/waves/round-58/count-c1.py | sha256sum
git show fe8801120a67c1a6b8899d7d0423839caa09e7d0:SCORECARD.md | grep -n '^## Capabilities'
```
