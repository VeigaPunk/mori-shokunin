# ConnSiblings — sibling-lane overlap scan for round 44's three instruments

Seat: `L1Mori44-4.ConnSiblings` (round 44, wave 1, connector). Leaf member, no subagent dispatch.
Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`, HEAD `7cb59c6891d4f5d0266fe062565f094da835dc84`
(the freeze commit). Fleet and sibling repos read-only; nothing written but this file; no
`git add/commit/push/checkout/stash/reset`, no mutating `jj`, no instrument byte edited.

**Axes named (godspeed).** C1 calibration 5 · C2 operability 7 · C3 coverage 6
(`.ufo/waves/round-44/contract.md` §Context). This seat produces no claim score; it names where
each instrument stands relative to a standard another lane already holds, and whether mori is
repeating work.

**Environment fact that bounds every measurement below.** `/tmp` is full on this host:
`df -h /tmp` → `/dev/nvme0n1p1  128G  128G  364K 100% /tmp`. Any `tempfile.mkdtemp()` run
(the default `TMPDIR`) fails with `OSError: [Errno 28] No space left on device` — measured:
`count-c2.py 7cb59c68 …` (default mutants dir) crashed at
`/tmp/c2-_mfizofu/mutant-count-c2.py`. Every run below was therefore made with
`TMPDIR=/home/vgpnk/.cache/connsib`. A C2/C3 receipt taken without recording `TMPDIR` is not
reproducible on this host today. No tool was installed or upgraded by this seat.

---

## 1. The three patterns, and who owns each

| pattern the assignment names | fleet standard owner | closest sibling holder (exact pointer) | mori's artifact |
|---|---|---|---|
| report-figure reconciliation ledger | `protocol` — `PROTOCOL.md:361` §Evidence standard bullet **Claimed ≠ re-executed** ("A command offered as evidence is a re-run performed at write time with its observed output") | `kama` `tools/report-landing-audit.py` (errata ledger `registry/report-landing-errata.tsv`, one row per corrected report defect); `kumitate` `scripts/wave-census.mjs --expect` (`EXPECT_MISMATCH`/`COUNT_MISMATCH`, `SKILL.md:609`); `chousa` `tools/research-gate.sh verify-claims` (pre-registered `expect` per claim vs `observed`, `VERDICT_BEARING_CLAIMS=N/M`) | `.ufo/waves/round-44/count-c1.py` + `.ufo/waves/round-44/figures.tsv` |
| gate-registry auditor | `protocol` — `PROTOCOL.md:398` §Gate standard bullet **Registry** (row fields; registry home per lane) | `kama` `tools/gate-registry-check.py` (385 lines, `SKILL.md:1325`); `protocol` `.ufo/gates/root-ledgers.py` (root `SCORECARD.md:196`) | `tools/mori-gate-registry.py` (308 lines, sha256 `743996b1…a1f`) |
| `--selftest` registry standard | `protocol` — `PROTOCOL.md:385` §Gate standard bullet **Self-test** | `kumitate` `scripts/gate-mutants.mjs` (contract `kumitate-gate-mutants-v2`, kill predicate K43, `SKILL.md:610`); `kumitate` `scripts/counter-pins.mjs` (`kumitate-counter-pins-v1`, `SKILL.md:619`); `kotodama` `SKILL.md` §"Gates and probes" (8-column table, `--selftest` isolated-export clause) | `count-c2.py`'s `selftest_tally` + `mutant_kill` arms |

Two structural facts fix the frame:

- **The eight-cell row is not mori's invention, and the registry is a fleet-wide convention.**
  `grep -n '^## Gate' */SKILL.md` finds a `## Gate…` heading in **13 of the 19 lanes that carry a
  `SKILL.md`** — 12 registries plus one decision table (tameshi:58, "## Gate-shape decision table —
  hermetic vs live vs audit-lane"): chousa:75,
  kagi:694+746, kengaku:560, kotoba:463, kotodama:619, kumitate:587, lore:48, mado:593, mori:156,
  revenger:272, souji:167, tameshi:58, tsukuroi:1952…3050 ×19 per-round sections). `chousa:77` and
  `kengaku:562` carry the header **byte-identical** to `mori-shokunin/SKILL.md:162`
  (`| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |`), and
  mori's `## Gates` preamble already says "Registry (PROTOCOL.md §Gate standard fields)"
  (`SKILL.md:161`). The **encoding is not standardised**, though — measured headers:

  | lane | form | schema |
  |---|---|---|
  | chousa, kengaku, mori | 8-column table | identical header |
  | kotoba (`:469`), kotodama (`:648`) | 8-column table | title case / `entry command` |
  | mado (`:600`), souji (`:177`) | 8-column table | relabelled cells (`gate/probe`, `self-test command / spelling`, `pinned-value path`, `verdict map (code → class)`) |
  | kumitate (`:599`), kama (`:1326`) | 5-column table | `name \| kind \| entry command \| self-test \| pinned values live in` / kama's `Name \| Kind / entry command \| Exit map \| Self-test / pinned values \| Write scope` |
  | revenger (`:274`) | 2-column | `field \| value` |
  | lore (`:48`) | bullet list | per-gate `- **name:**` / `- **gate/probe:**` blocks, citing `../PROTOCOL.md:360-406` |
  | tsukuroi, kagi | per-round superseding sections | 19 and 2 registry sections in one file |

  mori's auditor requires the literal heading `## Gates` and the exact eight field names, so it reads
  chousa's registry and mori's own, and no other lane's — including kengaku's, whose header is
  identical but whose heading is not (measured in §2.2).
- **`kama` and `kumitate` both declare their registry home under the same protocol clause while
  using the five-column form.** `kumitate-shokunin/SKILL.md:587` — "Registry home per the fleet
  protocol's §Gate standard (round 34)" — with a five-column table at `:599`; `kama`'s two registry
  tables (`:1224`, `:1325`) are five columns too. The clause `PROTOCOL.md:398` fixes eight fields;
  the fleet's child lanes implement at least six different encodings of it, and no gate checks that
  any of them matches the clause. `PROTOCOL-APPENDIX.md:35` is protocol's own hand census of the same
  surface — "15 tracked verdict scripts across five child lanes … the exact count is
  classifier-sensitive … self-test depth splits four ways" — i.e. the fleet-level conformance
  measurement is prose, per-lane, and acknowledged classifier-sensitive.

---

## 2. Verdict per pattern: duplicating or complementing?

### 2.1 C1 figure ledger — **complementing; the form is new to the fleet**

Measured: `grep -rln '@REV@' --include=*.py --include=*.sh --include=*.mjs --include=*.tsv .`
(excluding `mori-shokunin`) → **no files**. No sibling recomputes a report's numbers from a
committed TSV whose rows are single `git` pipelines at a substituted revision. The nearest
neighbours each reconcile a *different assertion class*:

| sibling artifact | what it reconciles | why it is not C1 |
|---|---|---|
| `kama-shokunin/tools/report-landing-audit.py` | commit citations in `.ufo/reports/round-N/kama.md` (`unresolved-full-hash`, `landed-omitted`, …) with an errata TSV | assertion class = commit hashes, not counts; the TSV records *corrections*, not asserted values |
| `kumitate-shokunin/scripts/wave-census.mjs --expect` | `<round>/<wave>:<role>=<n>` vs the recomputed dispatch/report payload | per-invocation flags, not a committed ledger; no revision substitution; only wave/role counts |
| `chousa-shokunin/tools/research-gate.sh verify-claims` | per-claim `expect: supported\|contradicted\|unsupported` vs `observed` | adjudication classes, not numbers; the expect lives in a JSONL claims file, the observed is a quote-span read |
| `chousa-shokunin/corpus/evidence/round44/disposition.tsv` + `c2-count.py` (concurrent round 44) | one row per frozen path, each row's sha256 reverified | closest *form* (row-per-artifact ledger); recomputes a hash, never a count, and has no command column |

C1's distinguishing property — *the ledger row carries its own command, so the ledger is
self-verifying at any revision* — exists nowhere else in the fleet. It is a strict addition.

### 2.2 C2 gate-registry auditor — **duplicating a class kama already holds, at higher strength on two arms and lower on one**

`kama-shokunin/tools/gate-registry-check.py` is the same instrument class: reads `SKILL.md` registry
tables at a revision (`--rev`, default worktree), grades occurrence **and** meaning, prints a
`pass=/fail=` selftest tally, exit `0/1/2`. Its selftest arms (`grep -n 'arm("'` → lines 293, 298,
310, 321, 330, plus a lane-tip arm) are `valid-row`, `thin-row`, `empty-exit-map`, `missing-path`,
`prose-only`, lane-tip → `GATE_SELFTEST pass=6 fail=0`. Mori's six arms are
`registered_row_met`, `missing_cell_rejected`, `unresolved_entry_rejected`,
`unregistered_path_rejected`, `no_selftest_rejected`, `seven_cell_row_rejected` →
`GATE_REGISTRY_SELFTEST pass=6 fail=0`. **Same arm count, different arms** — the instruments
overlap but neither subsumes the other:

| property | `kama` `gate-registry-check.py` | mori `mori-gate-registry.py` |
|---|---|---|
| population | **enumerates** every tracked counter: `COUNTER_RE` (`:69`) = `\.ufo/waves/round-[^/]+/count-[^/]+\.py` or `tools/round<N>-*.py`, discovered with `git ls-files`/`git ls-tree` (`:110-121`) | **caller-supplied**: `--audit` only (`add_argument` set is `--rev --repo --registry --audit --selftest`, lines 275-279); a counter nobody names is invisible |
| schema | five-column rows (`REGISTRY_HEADER`) | eight standard cells (`FIELDS`) |
| cell-path resolution | `missing-path:PATH` grades repo-relative tokens in entry/self-test/write-scope cells at the revision | resolves only the **audited target** |
| `--selftest` presence | not graded | graded (`b"--selftest" in body`) |
| row defect classes | `thin-row`, `empty-entry`, `empty-exit-map`, `missing-path` | eight-cell emptiness, entry resolution, selftest presence |
| table scope | all registry tables it recognises | first table under `## Gates` only — measured by a sibling seat this wave (`w1/ExecGateInventory.md` §4: 6 secondary 8-cell tables invisible, 11 conforming registrations scored absent) |
| registry-heading acceptance | tables it recognises by its own `REGISTRY_HEADER` | **exact literal `## Gates`** (`parse_gate_table`, `:86`: `line.strip().lower() == "## gates"`) and a header whose first two cells are `name`,`kind` (`:101`) |
| portability across the fleet | lane-local (own tree) | **spelling-exact**: of the 12 lanes holding a gate registry, only chousa's and mori's heading+header pair parses (`kengaku` has the identical header under a different heading and fails, §2.2) |

The portability row is measured, not inferred. Run read-only against two siblings at their own tips:

```
$ python3 mori-shokunin/tools/mori-gate-registry.py \
    --repo …/chousa-shokunin --rev d29bf47d94149a1b71581eeb0f36d9ff22d41da3 \
    --registry SKILL.md --audit tools/research-gate.sh
audit tools/research-gate.sh                   PASS (row '`research-gate`': 8 cells, entry resolves, --selftest present)
rev=d29bf47d94149a1b71581eeb0f36d9ff22d41da3
REGISTRY=met
EXIT=0

$ python3 mori-shokunin/tools/mori-gate-registry.py \
    --repo …/kengaku-shokunin --rev 0883e72ef8474ca42ac1a54eb0273079f1507035 \
    --registry SKILL.md --audit tools/kengaku-gate.py
REGISTRY_SETUP no gate table with a name/kind header in SKILL.md
EXIT=2
```

kengaku's header is **byte-identical** to mori's (`kengaku-shokunin/SKILL.md:562`); the run still
fails because kengaku's heading is `## Gate/probe registry (PROTOCOL §Gate standard)` (`:560`), not
the literal `## Gates`. So the tool reads chousa's registry and cannot read kengaku's — the heading
literal, not the schema, is the gate. It follows that `tools/mori-gate-registry.py` is not a
fleet auditor and cannot be made one by pointing it at another lane; and that it already *does*
audit a sibling lane's row when the spelling matches, which is a province question, not a
capability (see §3).

**The population gap is a C2 falsifier, not a stylistic difference.** C2's predicate is "each of
*the round's* counters is a registered gate" (contract P-C2); `count-c2.py` takes `--counter`
(repeatable) and checks exactly the paths handed to it. A round can therefore print `C2=met` while
a committed counter under `.ufo/waves/round-44/` is unregistered — the failure mode kama's round-32
repair exists to close (`kama-shokunin/tools/gate-registry-check.py:14-15`: "Round 34 widens the
rule: the round-33 counters live in `tools/` and were invisible to this gate (routed defect of the
round-33 closure)"). mori's `mori-gate-registry.py` cannot see that class at all.

### 2.3 `--selftest` registry standard — **complementing, but strictly weaker than kumitate's kill predicate**

`PROTOCOL.md:385` requires a self-invocation over isolated fixtures asserting **both the exit code
and a stable expected finding-id**, with expected values committed and independent of the
recomputation. Mori's `count-c2.py` measures two things: a `pass=N fail=0` tally
(`selftest_tally`) and one committed mutant per counter caught by that counter's own selftest with
`returncode == 1 and fail >= 1` (`mutant_kill`, `count-c2.py:180-186`). It does **not** measure the
finding-id clause, and its mutant arm is single-run and exit-only.

`kumitate-shokunin/scripts/gate-mutants.mjs` holds the stronger published standard —
contract `kumitate-gate-mutants-v2`, predicate **K43**: "a mutant is KILLED iff its run is evaluable
(no timeout, no overflow, clean process group, no spawn error, a parseable case summary whose total
equals the control's), the selftest exits with a numeric non-zero status, stdout carries the exact
line `VERDICT: FAIL`, and an immediate second run of the same mutated bytes meets the same
conditions with the same sorted FAIL case names." Frozen manifest: 43 mutants over 41 frozen ids;
each mutant gets its own copy of the complete `scripts/` tree; controls re-run after the mutants.
Mori's arm would pass a mutant whose selftest exits 1 with an unparseable tally on a flaky run;
K43 would not.

Second sibling datum on the same clause: `kumitate` `scripts/counter-pins.mjs` — a byte-pin
registry (`COUNTER_PINS: CLEAN|DRIFT|FAIL-CLOSED`, `kumitate-counter-pins-v1`, 11 hermetic cases) —
holds what mori does by hand in `evidence/freeze-r44.txt`. Mori's freeze manifest pins 11 paths;
kumitate's gate makes that pin set a re-runnable, fail-closed artifact that any seat can re-execute,
and refuses an empty pin set as DRIFT rather than CLEAN.

### 2.4 C3's README frontier-map row — **complementing, at lower strength, on mori's own corpus**

`kumitate` `scripts/readme-map.mjs` (`kumitate-readme-map-v2`, `SKILL.md:624`) makes the README↔corpus
mapping a bimap: every `*.md` under `corpus/knowledge` + `corpus/lessons` must carry exactly one
README row, every row must name an existing file, and every pinned member must still exist
(`stale-covered`, `covered-not-file`). Mori's `count-c3.py` `readme_row` check is a single
substring test: `entry.encode() in readme_body`. That is a weaker form of the same idea, applied to
mori's own `corpus/README.md`; no duplication, and no sibling needs it.

---

## 3. What in the three instruments belongs to another lane

| item in mori's instruments | owner it points at | belongs there? | mori keeps it local this round? |
|---|---|---|---|
| The eight-cell row schema, the gate/probe kind, the verdict-map clause, the `--selftest` clause (`PROTOCOL.md:380,385,398`) | `protocol` (main repo) | Yes — mori *consumes* it; `SKILL.md:161` already cites it | **Yes.** A child lane's registry home is its own `SKILL.md` (`PROTOCOL.md:398`); registering its own rows is the lane's duty, not a fleet act |
| A **fleet-wide** registry conformance gate (walk every lane's registry home: child `SKILL.md`, root `SCORECARD.md` §Gate registry, aggregator section) | `protocol` + `aggregator` | Yes — the surface spans repos mori does not own, and `PROTOCOL.md:418` **Delivery** routes the standard through the integrator's `lane_prompt()`, not a lane's tool | **Yes, keep local.** `tools/mori-gate-registry.py` defaults to `--repo <mori repo> --registry SKILL.md`, and it already *succeeds* against a sibling when the spelling matches (`chousa` `REGISTRY=met`, §2.2) while failing against a sibling whose heading differs (`kengaku` `REGISTRY_SETUP`). That pair is the province line: the tool can be pointed at a lane it does not own, so its use must stay scoped to mori's own rows and it must never be reported as a fleet gate or as a verdict on a sibling's registry |
| The mutant-kill standard (K43: evaluability, exact `VERDICT: FAIL`, second-run stability) | `kumitate` (orchestration/tooling) | Yes — a frozen contract plus a 43-mutant manifest over its own `scripts/` tree | **Yes.** mori's one-mutant-per-counter arm is lane-local and must not depend on a kumitate path (a cross-lane dependency would make C2's verdict move with a repo mori cannot freeze). Cite K43 as the stronger standard; do not import |
| The counter **population** rule (enumerate tracked `count-*.py` / `tools/round<N>-*.py`) | `kama` holds an instance; the rule itself is protocol's §Gate standard **Registry** | Partly — the rule is fleet, the enumeration regex is kama's lane-local encoding | **Yes.** mori's counters are mori's paths; the enumeration belongs in mori's auditor. Routed, not imported this round |
| `scripts/sources-census.sh` (the C3 census leg) | **fleet root** (`git log --oneline -- scripts/sources-census.sh` → `ae7bf19c scripts: sources-census.sh — fleet corpus/SOURCES.md census, validator, recheck queue, shared-source map (contract v1; …)`), i.e. main-repo/operator tooling, vendored at `6a1dd8ce` | Yes — the `SOURCES-CONTRACT-v1` schema (11 columns, `queued\|mined\|rejected`) is a fleet contract; mori is a consumer | **Yes, as a read-only dependency** — but it is the one instrument surface mori does not own and cannot freeze (see §4.4) |
| The `used-by` / `coverage-map` / `verified-at` / `recheck:` entry grammar (C3) | `protocol` `CORPUS.md` + fleet census contract | Yes — mori's `count-c3.py` encodes a fleet grammar | **Yes** (mori's entry must satisfy it); mori may not amend it |

Nothing in C1 belongs to another lane: the ledger is mori's own report, mori's own artifact classes
(`registry, evidence, wave, corpus, checks`), and no sibling surface. The one fleet-level question it
raises — "should every lane reconcile its reported figures?" — is already answered in prose at
`PROTOCOL.md:361`; mori's ledger is a lane-local instance of that rule, which is the correct form
because the artifact classes differ per lane.

---

## 4. Contradictions measured (stated, not scored)

### 4.1 C2 is already `met` at the freeze commit, before any data seat runs

The freeze commit added the four r44 registry rows itself — `git diff --stat 1429c791 7cb59c68` →
`SKILL.md | 4 +` — so the registry half of C2 was satisfied by the commit that froze the
instruments. Measured at that commit, with the committed mutants path supplied:

```
$ TMPDIR=/home/vgpnk/.cache/connsib python3 .ufo/waves/round-44/count-c2.py 7cb59c68 \
    --counter .ufo/waves/round-44/count-c1.py --counter .ufo/waves/round-44/count-c2.py \
    --counter .ufo/waves/round-44/count-c3.py \
    --mutants-dir .ufo/waves/round-44/fixtures/mutants
check counters_present   PASS (3 counters)
check registry_rows      PASS (REGISTRY=met)
check tool_selftest      PASS (pass=6 fail=0)
check selftest_tally     PASS (count-c1.py pass=6; count-c2.py pass=5; count-c3.py pass=6)
check mutant_kill        PASS (count-c1.py killed (fail=1); count-c2.py killed (fail=1); count-c3.py killed (fail=1))
rev=7cb59c6891d4f5d0266fe062565f094da835dc84
C2=met
EXIT=0
```

So "C2=met at the landed tip" cannot distinguish round work from the instrument commit. The
contract's Before (`1429c791` → `C2=unmet`, `evidence/control-c2-donothing.txt`) is honest, but the
After is satisfied at freeze. Whatever the round reports for C2 must say *which* commit turned the
verdict, or C2's calibration is zero by construction. (Adjacent seats `CritSelftestHonesty` and
`CritC1Vacuity` hold the neighbouring questions; this seat does not judge them.)

### 4.2 The C2 counter's default `--mutants-dir` names a path that does not exist

`count-c2.py:355` → `ap.add_argument("--mutants-dir", default="fixtures/mutants")`; the committed
mutants are at `.ufo/waves/round-44/fixtures/mutants/` (`git ls-tree -r --name-only 7cb59c68
.ufo/waves/round-44/fixtures`). Measured at the same revision, default invocation:

```
$ TMPDIR=/home/vgpnk/.cache/connsib python3 .ufo/waves/round-44/count-c2.py 7cb59c68 --counter …
check mutant_kill        FAIL (count-c1.py mutant absent; count-c2.py mutant absent; count-c3.py mutant absent)
C2=unmet
EXIT=1
```

Two invocations of the frozen counter, same revision, opposite verdicts, and the default is the
failing one. The registry row's pinned-values cell (`SKILL.md:185`) reads
"`fixtures/mutants/<basename>` beside each counter" — "beside" is false for both the default and the
committed path. This is precisely the class `kama`'s auditor grades as `missing-path:PATH`
(a repo-relative token in a row cell that does not exist at the revision); mori's auditor does not
grade cell tokens at all, so its own row's unresolvable token is invisible to it. Not patched
(frozen instrument); routed, not repaired.

### 4.3 "Gate-standard conformance" is broader than what `count-c2.py` measures

P-C2's name and axis label say *gate-standard conformance*; the measured predicate is
**lane-local registry conformance + tally + one exit-only mutant**. `PROTOCOL.md:385` adds the
stable-finding-id assertion and committed-independent expected values; `kumitate` K43 adds
evaluability, the exact `VERDICT: FAIL` line and second-run stability. Mori's C2 satisfies the
protocol clause's *shape* (isolated fixtures, exit + tally) and one extra behaviour (a mutant dies),
not its finding-id clause. The word "conformance" in the round's report should carry that limit.

### 4.4 C3's census leg runs a fleet-owned, mutable script at worktree state

`count-c3.py:136-146` stages the committed registry bytes and then runs

```
subprocess.run(["bash", census, "validate", "--file", staged], …, cwd=repo)
```

where `--census` defaults (`count-c3.py:300`:
`args.census or os.path.join(os.path.dirname(repo), "scripts", "sources-census.sh")`) to the
**fleet-root** script, not
a mori file, and not in `evidence/freeze-r44.txt` (which pins 11 lane-relative paths:
`contract.md`, three counters, `tools/mori-gate-registry.py`, `figures-r43.tsv`, three mutants,
`SKILL.md`). Two consequences: (a) the census *input* is revision-pinned (staged from `git show`) but
the census *tool* is whatever the fleet working tree holds — the class `PROTOCOL.md:390` **Two
evidences** names ("A gate whose verdict depends on a mutable fleet artifact also ships a run over a
committed input snapshot"); (b) `validate` also resolves `used-by` paths **on disk** (census code
`E11 used-by path missing on disk`), so the leg is worktree-sensitive while C1 and C2 are
revision-bound. The do-nothing control never reaches this leg (`evidence/control-c3-donothing.txt`
stops at `check entry_present FAIL (absent)`), so the property is unmeasured today, not disproved.
A third consequence follows from the same code path: an absent census script makes `bash` exit 127,
`census_ok` records `FAIL (exit=127)` and the run prints `C3=unmet` exit 1 — a missing dependency
reads as a failed claim, not `C3_SETUP`. (`ExecOffHostReplay` is measuring the clone case this
wave; this seat does not duplicate it.)

---

## 5. One bounded move

**Record C2's receipt as a two-invocation discriminator at one revision, and label the claim
"lane-local registry conformance".**

Concretely, for the C2 receipt the executor seat already owes (`w1/ExecWitnessReceipt.md`):

1. Run the frozen counter twice at the *landed* tip with the same `--counter` set:
   (a) the default invocation, (b) `--mutants-dir .ufo/waves/round-44/fixtures/mutants`; record both
   exit codes and both `C2=` lines verbatim, plus `TMPDIR`.
2. In the round report, state (i) that C2 was already `met` at `7cb59c68` (§4.1) and therefore is not
   round work, (ii) that the default `--mutants-dir` is a mispath (§4.2) routed to round 45,
   (iii) that the claim is registry conformance, narrower than `PROTOCOL.md:385` (§4.3), with
   `kumitate` `gate-mutants.mjs` K43 named as the stronger standard for a successor.

**Why this and not an import.** It improves calibration (no claim of round work where the freeze
commit already printed `met`; no "conformance" wider than the measurement) and operability (the
receipt becomes re-executable — today the default invocation cannot pass, and the run needs
`TMPDIR` off the full `/tmp`), and it touches neither C1 nor C3. Importing `kumitate`'s
`gate-mutants`/`counter-pins`, `kama`'s `gate-registry-check.py`, or `protocol`'s root-ledgers into
mori would (a) make C2's verdict move with a repo mori cannot freeze, (b) cross the province
boundary `PROTOCOL.md:407` **Scope** draws (read-only over surfaces it does not own, never acting on
an external surface), and (c) require editing the fleet repo, which this seat is forbidden to do.
The fleet-wide standard is protocol's; the lane-local instance is mori's.

**Risks.** (1) The receipt grows from one run to two; if the C2 owner reads the pair as a
contradiction rather than a discriminator, it can be mistaken for a red gate — the report must label
which run is the claim and which is the control. (2) `TMPDIR` recording couples the receipt to host
state; the alternative (a `--scratch` flag) is an instrument edit and is out of bounds this round.
(3) Naming K43 in the report could read as adopting it; the text must say "cited, not imported".

**Verification.** Re-run both invocations at the landed tip and confirm (a) default → `C2=unmet`
`mutant_kill`, (b) explicit → `C2=met`, both at the same `rev=` line; `git show <tip>:SKILL.md |
sha256sum` unchanged from `f9b1e2bf…6d05`; `sha256sum` of all 11 freeze paths still equal
`evidence/freeze-r44.txt`; and `python3 tools/mori-gate-registry.py --rev <tip> --audit` over the
three counters still prints `REGISTRY=met`.

---

## 6. Limits

- Read-only throughout. I executed: `count-c2.py` (frozen) twice at `7cb59c68`; `mori-gate-registry.py`
  twice, pointed read-only at `chousa` and `kengaku`; `df`. I ran no **sibling** tool, no sibling
  gate, and no `--selftest` of a sibling instrument — per `PROTOCOL.md:412` a lane does not execute
  a sibling's gate. Sibling claims above are read from committed bytes (docstrings, `SKILL.md` rows,
  line numbers cited), not from re-execution. The two sibling-repo runs are disclosed because they
  cross the province line in the read direction: both are `git show`/`git ls-tree`/`git cat-file`
  reads of a repo this lane does not own, nothing was written, and their results are reported here
  as portability evidence, never as a verdict on chousa's or kengaku's gates.
- `kama`'s and `kumitate`'s arm counts and kill predicates are quoted from their own headers and
  registry rows; I did not run them.
- I did not scan `shokuknow`, the fleet `.ufo/reports/*` corpus beyond the pointers named, or any
  lane's wave directories other than mori's.
- `/tmp` was full for the whole seat (§0). Any seat that reports a tally without `TMPDIR` set is
  reporting a host failure as a verdict.
