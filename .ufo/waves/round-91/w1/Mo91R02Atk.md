# Mo91R02Atk — attack the frozen P-C2 predicate (round-91 C2, freshness)

`count-c2.py` does not exist yet (frozen by name only), so the attack targets the frozen
predicate/kill-rule wording, exercised through a reference counter (`harness.py`, scratch) whose
emitter functions are lifted verbatim from `.ufo/waves/round-86/count-c3.py` at `79eaa8cf`
(`atom_map`, `volatile_fields`, `value_body`, `value_verdict`, `classifications` dedup; bare-key
`value-changed` rows only; `equal` rows excluded as the contradicting channel). It reads raw
inputs via `git show <rev>:<path>` (committed at R), or from the worktree for the hazard variant,
and prints the frozen field line. Forgers are fixture commits in `$S/fx`. No tools installed;
no pacman; read-only git on the lane only; all commits (`t`/`t@t`) live in the throwaway
`--shared` clone `$S/fx`, toplevel asserted (`FX_TOPLEVEL_OK`).

## Ground truth at 79eaa8cf (raw inputs, byte-exact vs blobs)

```
corpus/evidence/drift-classification-r82.txt   12b4b0779b118e93…  byte-exact
corpus/evidence/baseline-r10-20261015T2231Z.json 0993b23505deab2a…  byte-exact
.ufo/waves/round-82/evidence/drift-r82-live.txt  6091bc46cba5ef6e…  byte-exact
```

Degenerate-channel discovery: the only committed atom-bearing input is the r10 baseline
(`baseline atoms fields=31`); the r82 live snapshot is a token-line capture with no `key=value`
atoms (`r82snapshot atoms fields=1 {'rc': Counter({'1': 2})}`). So the value channel re-derived
from committed raw inputs is **all 14 rows `absent`** (`differs=0 masked=0 absent=14`). No
committed capture at `79eaa8cf` reproduces the round-86 live split (`.ufo/waves/round-86/evidence/c3-value-controls.txt`
is synthetic fixtures, not a census capture).

## Reproducibility (step 3)

- Pure committed-input re-derivation, two runs under different TZ/locale/TMPDIR/cwd:
  `diff emit-A.txt emit-B.txt` → `EMIT_IDENTICAL` (rc 0). No time, path or ordering dependence
  (output order = classification file order; Counters compared by equality).
- The real emitting counter `.ufo/waves/round-86/count-c3.py` at `79eaa8cf`, two same-moment
  runs: `C3_STDOUT_IDENTICAL`, both `aa=stable` — deterministic within a moment.
- Across time it is NOT reproducible: round-86 recorded (SCORECARD, at `50d80df0`)
  `C3=met … value_rows=14 contradicting=2`; the same frozen command today at `79eaa8cf` prints
  `C3=unmet observations=2 aa=stable tokens=64 derived=64 name_agree=64 value_rows=14 contradicting=0 …` rc 1.
  Nondeterminism source: the live census values (`-subject_commits`, `-window`) moved since
  2026-11-04 — time/live-system state, not paths or ordering.

## Forgers (fixture commits; counter line verbatim, rc)

| # | Class | What it forges | Verdict |
|---|---|---|---|
| F0 | (b) | honest-shaped snapshot, date self-asserted, raw inputs as-of 2026-11-04/r82/r10 | **ACCEPTED** |
| F1 | (a) | counts add up, one class disagrees with re-derivation | rejected |
| F2 | (b′) | `# data-as-of: 2026-10-15` + forged date line | **ACCEPTED** |
| F3 | (c) | raw inputs uncommitted (scratch-only), git-show counter | rejected |
| F3h | (c) hazard | same, raw bytes untracked in worktree, worktree-reading counter | **ACCEPTED** |
| F4 | (d) | snapshot omits 2 tokens the classifier emits | strict: rejected / loose: **ACCEPTED** |
| F4b | (d′) | committed raw set missing the r82 live-snapshot input | rejected |
| F5/F5b | (a′) | committed raw copies NOT byte-exact (classification edited), snapshot consistent | **ACCEPTED** |
| F6 | (d″) | snapshot carries an invented token line no raw input emits | **ACCEPTED** |

```
F0:  C2=met … date=2026-11-05 tokens=14 differs=0 masked=0 absent=14 … mismatches=0 rev=646a74d25a52  rc=0
F1:  C2=unmet … tokens=14 differs=1 masked=0 absent=13 … rederived=mismatch mismatches=1 rev=e460208e3280  rc=1
F2:  C2=met … date=2026-11-05 tokens=14 … mismatches=0 rev=e4309e48e0f7  rc=0
F3:  C2=unmet … missing-raw=corpus/evidence/drift-classification-r82.txt rev=668224de224e  rc=1
F3h: C2=met … tokens=14 … mismatches=0 rev=668224de224e  rc=0   (git status: `?? .ufo/waves/round-91/`)
F4 strict: C2=unmet … tokens=12 … unclassified=2 … mismatches=0 rev=49452debaffc  rc=1
F4 loose:  C2=met … tokens=12 differs=0 masked=0 absent=12 … mismatches=0 rev=49452debaffc  rc=0
F4b: C2=unmet … missing-raw=.ufo/waves/round-82/evidence/drift-r82-live.txt rev=598faf98d1d9  rc=1
F5:  C2=met … tokens=13 … mismatches=0 rev=6dad272a6775  rc=0   cmp raw copy vs 79eaa8cf blob → NOT_BYTE_EXACT
F5b: C2=met … tokens=13 … mismatches=0 rev=95c5cbdc6b89  rc=0   (clean rerun, 13-line snapshot)
F6:  C2=met … tokens=14 … mismatches=0 rev=6db420898717  rc=0   (both iteration modes)
```

## Clause accounting (why each acceptance survives the frozen text)

- (a) F1 — **rejected** by the re-derivation comparison: `mismatches=0`/`rederived=match` (both
  modes compare present lines). The kill-rule enumeration itself never names this case; the field
  carries it.
- (b)/(b′) F0/F2 — **accepted**: the date clause reads only the snapshot's own `# Date:` line
  ("a snapshot whose date is not 2026-11-05 keeps the claim unmet"); no clause compares the raw
  inputs' vintage (`# Date: 2026-11-04`, `As-of: 2026-11-04T07:45:13Z`, r10 baseline) to it.
  The planned honest snapshot is itself an F0 instance.
- (c) F3 — wording **rejects** ("committed raw inputs at R" + missing-raw clause) when the counter
  reads `git show <rev>:path`; the F3h acceptance shows the outcome is implementation-chosen if
  the counter opens the clone worktree. A counter MUST read at R.
- (d) F4 — mode-dependent: the strict reading ("re-derives every token's class … compares with
  the snapshot line for that token"; `unclassified` counts re-derived tokens with no snapshot
  line) rejects; a snapshot-driven counter accepts because `tokens=<n>` has **no floor/ceiling**
  (not pinned to 14 or 64) and the kill rule never names an omitted token.
- (d″) F6 — **accepted in both modes**: a snapshot line for a token the re-derivation does not
  emit is neither a mismatch (never re-derived), nor unclassified (it has a class), nor a
  duplicate; it silently inflates `tokens`.
- (a′) F5/F5b — **accepted**: "copied byte-exact" lives in the claim narrative only; no clause
  (date, missing-raw, duplicate, re-derivable, mismatches, unclassified) checks raw bytes against
  the `79eaa8cf` blobs. Two edited rows reclassifying tokens out of the channel shrink it to 13
  with `rederived=match`.
- "Full-census" is unenforceable as frozen: `tokens = differs+masked+absent` arithmetic caps the
  countable channel at the 14 bare-key value-changed rows (F0 measures 14); the other 50 census
  tokens can never appear in `tokens`.

## Is a snapshot 'dated' when the date is self-asserted? (step 4)

Under the frozen wording, "dated" means exactly `date=2026-11-05` on the snapshot's own line —
free text. No clause binds it to the raw inputs' vintage headers, to any observation event (no
census re-run is demanded), or to the entering bytes. F0/F2 prove r10/r82-vintage data reads
`C2=met … date=2026-11-05 … rc=0`. The claim's real, defensible content is reproducibility of the
classification from committed bytes — not freshness of observation.

Minimal text-only rules that close each accepted forgery (all checkable from committed bytes):

1. Raw-fidelity digest clause (kills F5/F5b; pins vintage; makes F3h's worktree bytes worthless):
   "The snapshot header records the sha256 of each raw input; the counter recomputes each from
   the committed copy at R and requires equality with the copy's blob at entering revision
   79eaa8cf."
2. Token-set closure clause (kills F6 and F4-loose): "The snapshot's token set must equal the
   re-derived token set — `tokens=<n>` with n equal to the re-derived channel size (14 at
   79eaa8cf), and a snapshot line for a token the re-derivation does not emit is a mismatch."
3. Iteration-direction sentence (kills F4-loose outright): "unclassified counts re-derived tokens
   with no snapshot line" (one sentence; makes the strict reading the only reading).

Residual limit named honestly: no text-only rule can prove a committed capture was *taken* on
2026-11-05; only a census re-run at grading time could, which would change the claim's shape.

## Amendment timing

`git cat-file -e HEAD:.ufo/waves/round-91/evidence/controls-r91.txt` →
`fatal: … does not exist in 'HEAD'` (HEAD `e02b8a39` carries only `contract.md` under
`.ufo/waves/round-91/`). Ordering step 2 (do-nothing controls commit) has **not** happened, and
Ordering §4 voids changes "after step 2". Adding clauses 1–3 now, committed and disclosed in the
contract, is a **disclosed pre-data amendment** (precedents: r86 A1 `98d15d8f`, A2 `c2bfded0`;
r87 A1 `b9e6f68d`). The same edit after the controls commit **voids C2**.

## Verdict

`ATTACK C2 forger-accepted=6 rejected=4`
- accepted: F0 (b stale-data-self-dated), F2 (b′ forged vintage disclosure), F5/F5b (a′ non-byte-exact raws),
  F4-loose (d omission), F3h (c worktree-reading hazard), F6 (d″ invented rows)
- rejected: F1 (a via `mismatches=0`), F3 (c via missing-raw), F4-strict (d via `unclassified=0`),
  F4b (d′ via missing-raw / `rederive=absent-raw`)

P-C2 as frozen verifies internal consistency of snapshot↔inputs and nothing about fidelity,
vintage, coverage or observation. C2's freshness value rests on clauses that do not exist yet.

## Limits

- `count-c2.py` is unwritten; acceptance/rejection was measured against a reference counter
  implementing the natural reading of the frozen sentence, not against the landed counter. Every
  wording-level acceptance (F0/F2/F5/F6, F4-loose) holds against the text itself; F3h/F4 are
  implementation-contingent and stated as such.
- The two live `count-c3.py` runs observed the host census (read-only); their stdout equality is
  a same-moment claim only.
- Fixture commits exist only in the deleted scratch clone; ids are reproducible by rerunning the
  recipe, not by ref (same convention as the r86 lesson's fixture).
