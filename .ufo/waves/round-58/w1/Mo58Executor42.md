# Mo58Executor42 — wave-context audit + frozen-counter probe (mori round 58, w1)

Seat: `Mo58Executor42` (role `executor`, executor item).
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Fleet root: `/home/vgpnk/Projects/shokunin`.
Freeze rev `fe8801120a67c1a6b8899d7d0423839caa09e7d0`; entering rev `b783d0b892637ce8d20f188cad20e4d8913ca635`.
Lane HEAD at audit time: `4272736cfc5147586e1543413772f80daf44b04b`.

Scope honored: no production file edited, no lane/fleet/sibling write, no commit, no VCS mutation.
Only writes by this seat: this report and `Mo58Executor42.receipt.txt` in the same directory.
All fixtures were throwaway git repos under `/fast/scratch/hyaku/mori-r58/Mo58Executor42/`,
each asserted with `git -C <fixture> rev-parse --show-toplevel` before any git command.

---

## A. Wave-context audit — the five checks this seat was assigned

All five PASS. Evidence is exact and reproducible.

### A1. GODSPEED prefix — PASS

`w1-spec.json` → all 64 items' `prompt` strings begin with `/skill:godspeed`
(`has prompt godspeed: 64`). Independently confirmed against the dispatch payload
`.ufo/waves/round-58/w1-dispatch.json` → `taskCall.tasks` (64 tasks):
`all start /skill:godspeed: True`. The prefix is followed by the four-step Godspeed
posture text and the "IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS" directive.

### A2. Correct absolute report path — PASS

Every dispatch task string ends with a `Report:` trailer:
`Report: write your scoped findings to .ufo/waves/round-58/w1/<SeatName>.md`
(`all have Report: trailer: True` over 64 tasks). The wave context resolves that
relative trailer to an absolute path explicitly:

> "Every `Report:` trailer path is relative to /home/vgpnk/Projects/shokunin/mori-shokunin
> — write it at /home/vgpnk/Projects/shokunin/mori-shokunin/<that path>."

`w1-spec.json` `reportDir` = `.ufo/waves/round-58/w1`; that directory exists and is
writable by this seat (`test -w` → OK). This seat's trailer
`.ufo/waves/round-58/w1/Mo58Executor42.md` is written to
`/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-58/w1/Mo58Executor42.md`,
exactly as the trailer and context require.

### A3. Scratch cleanup — PASS

The context mandates `$HYAKU_SCRATCH/mori-r58/<seat-name>/` (default `/fast/scratch/hyaku`),
explicit creation, `TMPDIR` set there, and cleanup before yielding. This seat created
`/fast/scratch/hyaku/mori-r58/Mo58Executor42/` explicitly and ran **every** counter,
selftest and fixture driver with `TMPDIR=/fast/scratch/hyaku/mori-r58/Mo58Executor42`.
`HYAKU_SCRATCH` is unset in this session's shell (the authoritative value lives in
`scripts/hyaku/hyaku.env:28` → `HYAKU_SCRATCH=/fast/scratch/hyaku`), so the context's
stated default was used verbatim — consistent with `scripts/hyaku/disk-guard.sh:110`,
which defaults the same way. Scratch tree removed before yielding (see §E).

### A4. Pacman guard — PASS

Context: "Pacman transactions are paused host-wide: do not run pacman. No pacman, no
unverified remote scripts." `/home/vgpnk/.omp/agent/RULES.md` was read first, as the
context requires. **No package install of any kind was performed** — no pacman, no
`uv tool install`, no `cargo`/`npm -g`, no remote script piped to a shell. Every tool used
was already on the host (`python3`, `git`, `sha256sum`, `grep`, `sed` on scratch copies
only). Tool/version/channel/reason ledger: **empty — no tool installed or updated.**

### A5. No lane/fleet mutation permission — PASS

Context: "Do not edit production files, corpus registry, SCORECARD, LOG, or lane VCS …
Do not write to fleet or sibling repos." Seat task text: "do not edit production files,
commit, or mutate lane VCS … no commits, no VCS mutation, no fleet/sibling writes."
Verified: the lane's two frozen counters and `contract.md` remain byte-identical to the
freeze blobs after all probes (`git status --porcelain` on those three paths → empty;
sha256 unchanged — §B). All `git` invocations against the lane were read-only
(`git show`, `git cat-file -e`, `git rev-parse`, `git status`, `git ls-files`,
`git diff`); every mutating git call (`init/add/commit`) ran inside a scratch fixture
whose toplevel was asserted first.

---

## B. Wave-shape sanity (read-only, from the frozen dispatch payload)

- Seats: 64. Roles: reviewer 22, critic 10, mutation-tester 8, executor 8, scribe 6,
  scout 4, connector 2, sentinel 2, revenger 1, simplifier 1.
- Attack share (reviewer+critic+mutation-tester+sentinel) = 42/64 = **65.6%** (contract
  requires ≥ 25%).
- No `planner` role is instantiated — consistent with the contract's §3 note that
  `planner` is not a validator role and the L1 holds the canonical planner seat. The
  two connector items carry the bounded sibling-overlap duty in prose ("Connector duty:
  compare sibling lane surfaces and report overlap/refusal boundaries"); they do **not**
  carry a planning-walk clause (grep for "planning" in both connector task strings →
  `False`, `False`). This is consistent with the contract's "bounded sibling-overlap/
  planning walks" phrasing only if the planning walk is read as optional; flagged, not
  scored.
- `w1-dispatch.json` `taskCall.context` is byte-identical to `w1-spec.json` `context`
  (`identical: True`), so the context the seats actually received is the frozen one.
- Round-57 contrast control holds at the landed tip: `.ufo/waves/round-57/count-c1.py HEAD`
  → `C1=unmet rows=0 evidence=bad`, exit 1 (contract's stated contrast).
- Census gate green: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`
  → final line `mori ok /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`,
  **exit 0** (duplicate-URL warnings only, all `W04`, pre-existing).
- Disk guard green before and after: `/fast/scratch/hyaku` 32% → 28% used, 553.6G → 581.1G free.

---

## C. Frozen-counter integrity and baseline measurements

Counter bytes are unchanged from the freeze (kill rule satisfied for both counters at
audit time):

| file | sha256 (worktree) | sha256 (freeze blob) | equal |
|---|---|---|---|
| `.ufo/waves/round-58/count-c1.py` | `6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b` | `6ecdb627bb55522c258dc484ed5c530cfd6f7c57c6a89b4c38179df4c0f84e4b` | yes |
| `.ufo/waves/round-58/count-c2.py` | `aab888ad787964f7a153d64d85dafa58f652f977e21e22eaa492706a691010d3` | `aab888ad787964f7a153d64d85dafa58f652f977e21e22eaa492706a691010d3` | yes |

`git diff fe880112..4272736c -- count-c1.py count-c2.py contract.md` → empty.
`git status --porcelain --` on the same three paths → empty.

Selftests (run with `TMPDIR` in this seat's scratch):

```
C1_SELFTEST pass=4 fail=0     (exit 0)
C2_SELFTEST pass=6 fail=0     (exit 0)
```

Baseline counter output at all three revisions:

| rev | C1 | C2 |
|---|---|---|
| `b783d0b8…` (entering) | `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none` (exit 0) | `C2=unmet entry=absent failed=entry` (exit 1) |
| `fe880112…` (freeze) | `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none` (exit 0) | `C2=unmet entry=absent failed=entry` (exit 1) |
| `4272736c…` (HEAD) | `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none` (exit 0) | `C2=unmet entry=absent failed=entry` (exit 1) |

`git cat-file -e b783d0b8…:.ufo/waves/round-58/count-c1.py` → fails (counter absent at
entering rev), as the contract's C1 "before" control states.

---

## D. Findings — five defects found by bounded scratch fixture

### D1 (BLOCKER for C2 as landed). The C2 `KLINE` regex does not match the lane's
### entry bullet format, so a correct entry scores `claims=0`.

`count-c2.py` `KLINE = re.compile(r"^- \*\*K(\d+)\*\*.*\((tools/mori-driver-liveness\.py):(\d+)\)")`
requires the label to be exactly `**K<n>**` — bold closing right after the digits.

The lane's pending entry `corpus/knowledge/driver-events-r58.md` (untracked at HEAD,
present in the working tree) writes each bullet as:

```
- **K1 — unmatched timestamped prose is separate from a lane event.** A timestamp-first line …
```

i.e. `**K1 — …**` — the bold encloses the whole sentence, so `\*\*K(\d+)\*\*` never
matches. Measured against the real pending entry, all 8 bullets are NOMATCH and the
frozen counter reports **claims=0**:

```
C2=unmet claims=0 located=0 copy=ok tree=ok rows=ok sources=ok failed=claims   (exit 1)
```

The counter's own selftest fixture uses the `- **K{i}** …` shape
(`ENTRY_OK` in `count-c2.py`), so the selftest passes while the real artifact fails —
the selftest does not cover the entry shape the lane actually wrote.

Isolation of the cause (fixture built from the lane's real entry + real pinned copy,
only the bullet label reshaped to `**K<n>** — …`):

```
C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none   (exit 0)
```

Every quote, line number and byte-identity already checks out (located=8/8, copy=ok,
tree=ok, rows=ok, sources=ok); **only the bold-label shape is wrong.** Fix belongs in
the entry, not the counter — the counter is frozen and must not change.

### D2 (C2 false-green, "byte-faithful quotes" arm). The located-quote arm accepts a
### fabricated quote when any other backticked span on the same line matches.

The located test is `any(len(s) >= 12 and s in copy_lines[lineno-1] for s in spans)`
where `spans` is *every* backticked span on the bullet — the one introduced by
`Quote:` is not distinguished from any incidental identifier token.

Fixture: every bullet's `Quote:` field replaced by
`` `this fabricated quote is not in the source` ``, with the real source line pasted as
a second backticked span:

```
C2=met claims=8 located=8 copy=ok tree=ok rows=ok sources=ok failed=none   (exit 0)
```

So the claim "every located quote is verified as a substring of a pinned source copy"
holds only in the weak sense that *some* backticked span on the line occurs on that
source line. Two control variants bound the weakness:

- fabricated quote + incidental token that is on the cited line → `located=1`,
  `failed=quotes` (the token happened to appear on only one of the eight lines);
- fabricated quote + a token that appears on *no* cited line → `located=0`,
  `failed=quotes`.

The contract's §9 control (a) — "an entry whose quotes are NOT substrings of the pinned
copy MUST score `C2=unmet … failed=quotes`" — is therefore **violated** by the
fabricated-quote-plus-incidental-span construction above: the counter scores `met`.
This is the same class of defect as round-57 routed defect 2 (quote predicate), in
narrower form. Note this does not currently affect the lane's honest entry — it is a
counter-strength finding for the L1 and the attack seats.

### D3 (C1 false-green, pointer arm). Evidence pointers outside three prefixes are
### never resolved, so a nonexistent path passes.

`count-c1.py` resolves only paths starting with `.ufo/`, `tools/`, `corpus/`:

```python
if path.startswith((".ufo/", "tools/", "corpus/")):
    q = _git("cat-file", "-e", f"{rev}:{path}")
```

Fixture: the row-0 evidence pointer `.ufo/waves/round-56/evidence/c2-at-landed.txt`
replaced by `docs/definitely-not-here.md` (a path that does not exist in the repo):

```
C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none   (exit 0)
```

The contract states the pointer arm as "**every** evidence pointer in the two rows must
be resolved via `git cat-file -e R:<path>`". As implemented, a pointer under `docs/`,
`evidence/`, `scripts/`, or a bare top-level file is skipped without being resolved, so
`pointers=ok` is reported for a row that names a nonexistent file. The §9 do-nothing
control ("a fixture register whose two rows name a nonexistent evidence path MUST score
`C1=unmet … failed=pointers`") therefore holds only for paths under the three
whitelisted prefixes. The lane's real rows happen to use `tools/` and `.ufo/`, so the
landed state is unaffected.

### D4 (C1 weak binding). The register row's capability *name* is not bound to the
### MANIFEST text; only the key is.

`MANIFEST_HINTS = {0: "vote binding", 1: "driver-liveness"}` is checked against
`MANIFEST.json` `rounds[832].capabilities_added[j]` — the manifest side only. Nothing
ties the SCORECARD row's capability text to that manifest string.

Fixture: both round-56 rows rewritten to unrelated capabilities while keeping the keys
and resolvable pointers:

```
| `rounds[832].capabilities_added[0]` | completely unrelated capability alpha | Does nothing relevant. | `tools/mori-vote-bind.py` | 56 |
| `rounds[832].capabilities_added[1]` | totally unrelated capability beta | Nothing to do with liveness. | `tools/mori-driver-liveness.py` | 56 |

C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none   (exit 0)
```

The contract's C1 predicate item (c) says each row's **key** is bound to the manifest
key, which is what the counter checks — so this is within the letter of the frozen
predicate. It is reported because connector seat `Mo58Connector59` is explicitly tasked
with "test whether altered names or keys can still pass": the answer for **names** is
yes, they still pass; for **keys**, the row-key check does bite (the counter's own
`wrong_key_row_fails` selftest arm passes). The `used-by`/name binding for C2 rows *is*
checked (`cells[11]` must name the entry), so C2 is stricter here than C1.

---

### D5 (C1 non-hermetic arm). The MANIFEST arm is the one live read in an
### otherwise revision-pinned counter.

Every other arm of `count-c1.py` reads the tree at the measured revision
(`_git("show", f"{rev}:SCORECARD.md")`, `_git("cat-file", "-e", f"{rev}:{path}")`).
The MANIFEST arm instead opens the file from the live filesystem:

```python
m = json.load(open(os.path.join(FLEET, "MANIFEST.json")))     # count-c1.py:111
```

`FLEET` is `dirname(LANE)`, i.e. the live fleet root — not `git show <rev>:MANIFEST.json`.
So `count-c1.py b783d0b8…` reports `manifest=ok` against whatever
`/home/vgpnk/Projects/shokunin/MANIFEST.json` contains *now*, not what it contained at
`b783d0b8…`. The measurement is therefore not reproducible from the revision argument
alone, and a rev-scoped run can be contaminated by a later fleet-side manifest write.
At audit time the fleet `MANIFEST.json` is clean and does carry `rounds[832]`
(841 rounds, `rounds[832]` non-null at fleet HEAD), so the arm currently scores `ok`
legitimately — the defect is hermeticity, not a wrong verdict today.

`count-c2.py` contains no `MANIFEST` reference at all (`grep -c MANIFEST` → 0); it binds
its row to `corpus/SOURCES.md` at the measured revision, so it is fully revision-pinned.

This finding was raised independently by connector seat `Mo58Connector60`
(`.ufo/waves/round-58/w1/Mo58Connector60.md`); recorded here because the C1 claim's
calibration wording ("each row's key bound to fleet `MANIFEST.json`
`rounds[832].capabilities_added[j]`") is satisfied but not hermetically.

---

## E. Two counter/contract string mismatches (non-blocking, recorded for the L1)

1. **The contract's frozen target output for C1 names a field the counter never emits.**
   Contract line 30: ``C1=met rows=2 pointers=ok manifest=ok binding=ok selftest=ok rev=R``.
   The counter emits `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=R`.
   `grep -n "selftest=" count-c1.py` → **no match anywhere in the file**; there is no
   `selftest=` token in the C1 measure output at all (the selftest prints
   `C1_SELFTEST pass=N fail=0` as a separate invocation). A scorer that string-matches
   the contract's target line will not match the counter's real output. Same shape for
   C2: contract line 47 lists `claims=N located=N copy=ok tree=ok rows=ok sources=ok`
   while the counter emits those fields plus `failed=none` in the same slot. The C1
   difference is material (a field that can never appear); the C2 difference is
   cosmetic (one extra field).

2. **The `STUB_MARK` in `count-c1.py` is `"-- none yet --"` (ASCII hyphens) but the
   real SCORECARD stub at `SCORECARD.md:600` reads `| — none yet — | | | |` (em
   dashes).** `grep -c -- "-- none yet --" SCORECARD.md` → **0**;
   `grep -c -- "— none yet —" SCORECARD.md` → **2**. The stub-refusal test is therefore
   never exercised by the real artifact. It happens not to matter — the active register
   is still selected correctly, because the *preamble* + header checks also discriminate
   — but the guard as written is inert. This is dangerous in the other direction too:
   if the em-dash form were substituted, the **active** register would be refused,
   because the active register's own preamble (SCORECARD.md:1958) contains the em-dash
   text `— none yet —` when describing the superseded stub. Measured on a scratch copy
   of the counter with `STUB_MARK` set to the em-dash form:
   `_find_register(HEAD:SCORECARD.md)` → `None` (active register refused). Do **not**
   "fix" the marker to match the file — the ASCII form is load-bearing for a false
   negative against the real register. Recorded as an observation only; the counter is
   frozen and must not change.

Also confirmed by direct fixture: a register whose only `## Capabilities` section is the
real em-dash stub (copied verbatim from `SCORECARD.md:596-600`) scores
`C1=unmet rows=0 pointers=ok manifest=bad binding=bad failed=binding`, exit 1 — the
contract's §9 "stub-only ⇒ `binding=bad`" control holds for the real stub text.

---

## F. Risks / blockers

- **D1 is the only thing standing between the lane and `C2=met`.** The entry's content
  is otherwise fully conformant (8 claims, 8 located, copy/tree/rows/sources all ok).
  One reshape per bullet (`- **K1 — text.**` → `- **K1** — text.`) flips the counter to
  `C2=met claims=8 located=8 …`. Any seat reformatting or re-flowing those bullets
  must preserve the `**K<n>**` label shape.
- The C2 artifacts (`corpus/knowledge/driver-events-r58.md`,
  `corpus/evidence/sources-r58/`) and the `S550` row in `corpus/SOURCES.md` are
  **untracked/uncommitted** at HEAD (`git status` shows `?? corpus/knowledge/driver-events-r58.md`,
  `?? corpus/evidence/sources-r58/`, ` M corpus/SOURCES.md`; `git show HEAD:corpus/SOURCES.md | grep -c '^| S550 '`
  → 0). Until they are committed, `count-c2.py <rev>` can only ever print
  `C2=unmet entry=absent` — which is exactly what it prints at all three revisions now.
  The counter is not at fault; the artifacts are simply not landed.
- The pinned copy `corpus/evidence/sources-r58/mori-driver-liveness.py` and
  `tools/mori-driver-liveness.py` are byte-identical
  (sha256 `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997` for both)
  — the `copy=ok tree=ok` arm holds at the pending state.
- D2/D3/D4 are counter-strength findings. The counters are frozen and immutable after
  scoring, so **no counter change may be proposed for this round** — they are reported
  as round-59 input, or as L1-level scoring caveats against the C1/C2 claim wording
  (the claim sentences in `contract.md` are stronger than what the counters implement:
  "every evidence pointer … must be resolved" for C1, "every located quote is verified
  as a substring" for C2).
- D5 is a hermeticity finding on the C1 MANIFEST arm, raised independently by
  connector seat `Mo58Connector60`; the two reports agree.
- **Sibling overlap (confirmed, no double-count).** Connector seat `Mo58Connector59`
  independently reproduced D4 (their F1/F2: register-row content not bound to the key,
  MANIFEST matched by substring) and D3 (their F4: prefix-skip pointer gap), and adds
  the `rounds[999]` key-failure case which the frozen counter's own selftest already
  covers. Their `docs/` path variant of D3 is an extra case they had not tested. This
  seat's contribution is the *reproduction* with a concrete nonexistent-path fixture and
  the `docs/` case, plus D1/D2/D5 which are outside their scope.
- No remediation was performed and none is proposed for the frozen counters. Per the
  seat's remit: detection and reporting only.

## G. Cleanup

- Scratch root `/fast/scratch/hyaku/mori-r58/Mo58Executor42/` (fixtures `fixture-c2`,
  `probe/{lane,c1name,c2fix,c2tok,c2fab,c2quote,emdash}`) removed before yielding.
- The small receipt was copied into the report directory first:
  `.ufo/waves/round-58/w1/Mo58Executor42.receipt.txt` (counter sha256s, selftest
  results, per-revision counter output, r57 contrast output, census tail, disk-guard
  head).
- No file outside this seat's report directory and its scratch root was created or
  modified. The lane's frozen counters and `contract.md` remain byte-identical to the
  freeze blobs.
