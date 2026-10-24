# CritExploratoryBoundary — claim-structure attack (round 40, w1)

Axes attacked: **C1 operability** (conformance v3 checker) and **C2 depth** (gate
v3 P-C11). Assigned probes: exactly-two-claims, no hidden third claim, C1/C2
causal separability.

## Verdict

- **Two claims confirmed on distinct axes.** `contract.md` carries exactly
  `### C1 — operability` and `### C2 — depth`; `P-C10` occurs verbatim only in
  `conform.py` + contract; `P-C11` only in the gate + contract. No third
  P-predicate exists in the wave tree. Contract `P-C10` == `conform.py`
  `PREDICATE` and contract `P-C11` == gate `PREDICATE` **byte-for-byte after
  whitespace normalisation** (verified by `module.PREDICATE` import +
  whitespace-normalised compare), and both predicates appear verbatim in the
  receipts. The wave's other surfaces are machinery, not claims: SCORECARD has
  exactly two claim rows (C1/C2) + two capability rows; S229, the r39 erratum,
  `conform-scope-r40.md`, the SKILL.md table row, census pair, witness fixtures
  and `gen-wave-spec.py` are frontier/diff/claim-support items. **No third
  claim hides in the corpus or evidence edits.**
- **Causal separability: PROVEN dynamically both directions** (see §3).
- **The headline claims hold** on the artifact (`CONFORM=met`, selftest 11/0,
  35 as-of incl. S226, `stale=[S069]` at e37dcc6, selftest 15/0). But the
  number-bearing prose around C2 has **two layers of number-drift** and C1's
  "at revision R" is **not bound by the instrument** (F2). Findings below.

## 1. Commands run (all reproduced, this session, lane cwd unless noted)

C1 (operability) — reruns against the landed bytes:

```
$ python3 .ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b
  → all nine checks PASS; CONFORM=met; exit 0   (matches evidence/c10-after.txt;
    head_pin printed pin=ede486b…=tip — see F2)
$ python3 .ufo/waves/round-40/conform.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --selftest
  → 11 arms, each flips exactly its own check; CONFORM_SELFTEST pass=11 fail=0; exit 0
$ python3 .ufo/waves/round-40/conform.py bb1f2457bb8d3e8d5dfe98488b91e8c02e378ca3
  → CONFORM=met; exit 0   (!! pre-claim revision accepted — F2)
```

C2 (depth) — reruns:

```
$ python3 tools/mori-sources-appendonly.py 265a955cc67be4eae97d2dc5a9338a25f31eb29b --repo .
  → supersede_timing superseded_as_of=[35 ids, S041…S193,S226] stale_supersede=[]; exit 1
$ python3 tools/mori-sources-appendonly.py e37dcc6 --repo .
  → superseded_as_of=[33 ids] stale_supersede=[S069]; exit 1
$ python3 tools/mori-sources-appendonly.py --selftest
  → MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0; exit 0
```

Pin/provenance verification:

```
$ sha256sum <six frozen paths + three extracted files>
  → all nine equal evidence/freeze-r40.txt pins exactly.
$ git show bb1f2457:{.ufo/waves/round-39/conform.py,count-c7.py,tools/mori-sources-appendonly.py} | sha256sum
  → identical to fixtures/extracted/{conform-v2-r39,count-c7-r39,gate-v2-bb1f2457}.py
    (before-controls genuinely measured at entering bytes).
$ python3 (import PREDICATE from both instruments; whitespace-normalised compare to contract blockquotes)
  → P-C10 contract==conform: True; P-C11 contract==gate: True; both found verbatim in receipts.
$ python3 ast.parse diff of count-c7-r39 vs count-c8
  → AST differs only by deleted dead code; text diff = 5 deletions, 0 additions (F3).
```

## 2. Receipt audit (committed evidence re-read)

- All nine c10-red survivor receipts print `CONFORM=met` under the r39 bytes
  (divzero: `conformance setup error: division by zero`, EXIT=2 — the contract
  records this exact shape); all nine c10-after receipts print `CONFORM=unmet`
  with the named new check FAIL. Multicounter: v2 `met` → v3 `unmet` with
  per-counter `comm_violations`. Conjunct-gutted: r39 copy selftests
  `pass=8 fail=0`; v3-gutted copy `pass=0 fail=10` (every arm's expected-fail
  set gains `selftest_conjunct` — the table is genuinely live).
- c11-before-lane (v2 bytes): 18 as-of, S226 absent. c11-after-lane (v3):
  **35** as-of, S226 present, stale=[] — see F1. dag-n/p/r receipts print the
  P-C11 verdicts under v3 and the predicted wrong verdicts under v2.
- `partition` check on every committed c11 receipt: `superseded` ==
  `as_of ∪ stale` exactly at tip (35=35+0), at e37dcc6 (34=33+1), and on the
  v2 line (18=18+0) — no id floats outside the two verdict sets.

## 3. Causal separability — demonstrated, not inferred

**C1 receipts runnable without the gate v3 bytes** — dynamic:

```
$ mkdir /tmp/sep-c1/repo; git init; committed ONLY
    .ufo/waves/round-39/fixtures/witness-summary-only-live.txt   (no tools/ at all)
$ python3 …/conform.py HEAD --repo /tmp/sep-c1/repo
  → CONFORM=met, exit 0   (all nine checks PASS)
$ python3 …/conform.py HEAD --repo /tmp/sep-c1/repo \
      --counter …/fixtures/generated/survivor-decoy.py
  → CONFORM=unmet (drain_bind FAIL), exit 1
```

The repository object under test contained **no `tools/mori-sources-appendonly.py`
at any rev** — the gate path simply does not exist there. Static corroboration:
`grep -n 'mori-sources\|appendonly\|SOURCES' conform.py count-c8.py` hits only
`count-c8.py`'s `SOURCES_REL`/`show(repo, rev, SOURCES_REL)` — and that read
sits in the counter's *full-run* path, never exercised by the checker (the
checker only invokes `--print-predicate`, `--pin-only`, `--print-tool`, and
`--arms selftest`, which returns at count-c8.py:428–444 **before** the blob
reads at :449–459).

**C2 receipts runnable without the conform v3 bytes** — dynamic, two ways:

```
$ cp tools/mori-sources-appendonly.py /tmp/sep-c2/gate-standalone.py; cd /tmp/sep-c2
$ python3 gate-standalone.py --selftest   → pass=15 fail=0   (cwd has no C1 artifact at all)
$ git clone lane → /tmp/sep-c2hist; git checkout 265a955c…;
  git filter-branch --index-filter 'git rm -r --cached --ignore-unmatch
    .ufo/waves/round-40/conform.py .ufo/waves/round-40/count-c8.py' -- HEAD
  → rewritten tip 6e28c1b; `git cat-file -e HEAD:.ufo/waves/round-40/conform.py` →
    "path does not exist" — conform v3 bytes absent from the ENTIRE history
$ python3 …/tools/mori-sources-appendonly.py HEAD --repo /tmp/sep-c2hist
  → identical verdict line: 35 as-of ids incl. S226, stale_supersede=[], exit 1
```

Additionally `run-c11-dags.py` builds fixture repos whose only tracked path is
`corpus/SOURCES.md` (gate `_dag_init`/`_dag_commit`/`_dag_merge`), so the three
committed fixture receipts already ran conform-free. The gate's own docstring
confirms: "the only git commands used are `rev-parse`, `log`, `show` and
`merge-base --is-ancestor`" — all scoped to the registry path.

**Conclusion:** C1's receipts depend only on checker+counter+fixture bytes; C2's
only on gate bytes + the registry's commit DAG. Neither receipt set can have
been produced by, or contaminated by, the other claim's instrument.

## 4. Findings (attack output)

### F1 — number-drift, round 2: the correction itself is off by one (depth/C2)
`contract.md`/P-C11 say "(19 ids)"; `LOG.md`, `SCORECARD.md`, lesson `M24` and
the wave brief all "correct" this to **34**. The committed receipt
`c11-after-lane.txt` enumerates **35** ids (S041,S044,S051,S062,S064,S067,S069,
S070,S071,S083,S084,S090,S093,S096,S097,S101,S124,S127,S128,S129,S131,S140,
S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193,S226) and my live
rerun of the pinned gate at 265a955 prints the same 35. The never-edited
extension admits **17** rows (S226 + 16 earlier: S067,S070,S071,S083,S084,S090,
S093,S096,S097,S101,S124,S127,S128,S129,S131,S140), not M24's "S226 plus 15".
Arithmetic: 18 changed + 17 never-edited = 35. Smallest correction: erratum
line fixing 34→35 and 16→17 (same mechanism as M24 itself). The P-C11 semantic
sentence holds regardless; this is prose-drift in the correction layer.

### F2 — "at revision R" is not bound by the C1 checker (operability/C1)
`conform.py <rev>` never inspects repository state *at* `rev`: `head_pin`
compares `rev-parse HEAD` to the counter's own `rev-parse HEAD` output
(head=self, always true), the static audit reads the counter from **disk**, and
`rev` enters only the `timeout_state` subprocess (where any resolvable rev —
even an unrelated commit — passes, since the selftest arm returns before blob
reads). Probe: `conform.py bb1f2457` prints `CONFORM=met` byte-for-byte as at
265a955, with `pin=ede486b…` (today's HEAD) — proving neither the arg nor the
receipt's recorded rev gates anything but resolvability (an unresolvable rev
surfaces only as `timeout_state` FAIL via the counter's exit-2, a secondary
channel). The measured claim still holds — the checker does discriminate the
counter bytes — but the "at revision R" provenance clause is decorative: the
receipt's rev argument could be any commit. Smallest correction: bind
`head_pin`/`static_checks` to `git show <rev>:<counter>` bytes and compare the
pin to `rev-parse <rev>`, or erratum narrowing "at revision R" to "at HEAD at
measurement". Judge-facing iff P-C10's "at revision R" is read as binding.

### F3 — "sixteen dead lines" prose vs measured 5 (operability/C1 hygiene)
Contract C1: "round-39 `count-c7.py` bytes minus the sixteen dead lines of
SimpCounters D1–D4". Measured: `diff count-c7-r39.py count-c8.py` removes
**exactly 5 lines** (hunks `98d97`, `441,444d439`), adds 0; the AST diff is the
`ROWSTATES_RE` compile + the dead `table`/`parse_got_want` block only, and
`c10-parity.txt` shows byte-identical receipts — parity claim holds. "Sixteen"
matches the routed-input line "~16 dead lines across count-c7/conform" (a
cross-file figure), so the parenthetical mis-scopes the number to the counter
alone. Same number-drift class as F1; smallest correction: erratum 16→5 (or
restate as a D1–D4-wide figure).

### F4 — SCORECARD kill-rule mechanism mis-quotes dag-r (cosmetic, depth)
SCORECARD says a gate keeping the re-add changed event "prints `stale=[S008]`
on dag-r". Measured v2 prints `round_changed=[S008]` with `stale_supersede=[]`;
the v2→v3 dag-r delta is `superseded=[]→[S008]` + `as_of=[S008]` (the re-add
fabricates a *supersede verdict*, not a stale flag — `round_changed=[S008]`
persists under v3 because deletion inside the range is a round change by
design). Kill rule still discriminates; the quoted field name is wrong.

### F5 — provenance gap already repaired: `conform-v3-conjunct-gutted.py`
used by `c10-after-conjunct.txt` was untracked at receipt time (receipt ran
before commit `ede486b` which adds it); now committed — receipt reproducible.
Also noted: S229's registry row sat outside `## Registry` until `ede486b`;
`evidence/.parity-c{7,8}.txt` dotfiles and `scratch/selftest-v3-draft{,2}.txt`
were committed in 8d3badd (hygiene noise). `conform.py` docstring says the
counter scratch lives under `round-40/scratch` while the check requires
`round-39` (selftest's own mutation target — intentional, but docstring drift).

### F6 — divzero collateral (observation)
`c10-after-divzero.txt` prints `CONFORM=unmet` via `timeout_scope` (satisfies
the claim) but also FAILs predicate/head_pin/tool_resolve/timeout_state — the
mutated `NAME = 1/0` crashes the counter's module body at run time. Claim text
("CONFORM=unmet with the named new check FAIL") is met; the noise is inherent
to that fixture class.

## 5. Bounds and tools

Lane writes this session: this report only. Scratch I created lives under
`/tmp/sep-c1`, `/tmp/sep-c2`, `/tmp/sep-c2hist` (all outside both repos; the
two instrument selftests wrote and removed their own mandated scratch dirs —
`conform.py` hardcodes `.ufo/waves/round-40/scratch`). No git/jj mutation in
the lane; the filter-branch ran on a `/tmp` clone. Tooling: none installed —
system git 2.x filter-branch only; pacman untouched per the pause.
