# CriticC3Final — wave-2 falsification of C3 calibration

Seat: `MoriR17.CriticC3Final-4` (critic, leaf). Scope: attack the *proposed approach and
evidence* for C3 (contract.md:21–27; Amendment A1 does not alter C3; lesson
`corpus/lessons/round-17.md:34–36,135–139`). Advisory only — no admission judgment, no
edits, no reruns of probes/selftests; counting commands read-only over committed receipts.
Lane HEAD at audit: `5c1dfb8d0530c74eb0e1630c2b522b735b486274`; measured commit `273aa74`.

## Axes attacked

Evidence provenance/durability · counter fidelity to the declared unit · negative-control
coverage · baseline emulation fidelity · matcher semantics · witness authenticity
(archived-vs-synthetic).

## Attacks executed and outcomes

| Attack | Result |
|---|---|
| **A1 — synthetic-content convenience?** The lesson gate requires the exact archived artifact, not a synthetic body that conveniently contains lane/round tokens. | **Rejected.** Frozen witness is 847 B, sha256 `15f9f82d…5510e`, byte-identical to fleet blob `cd635a3e` (`git cat-file`/`sha256sum`, and ReceiptC3's cross-repo blob comparison). Applying the tool's own regexes (`mori-misroot-sweep.py:153,161`) to the committed frozen bytes: lane token absent, round token absent — filename-only. `c3-after.json` reports `matched_in:["path"]`, consistent. The content arm is exercised only negatively on the real artifact; that is fidelity, not gaming. |
| **A2 — legacy baseline strawman?** Does the "before" run emulate the actual r16 miss? | **Rejected.** `c3-before.json` argv carries `--legacy-pathspec .ufo/waves --legacy-pathspec .ufo/reports` — the exact two-element pathspec recorded in the r16 receipt (`build/MisrootR16Facts.md:57`; `round-16-verifier-spotcheck.md:206`). `scan.untracked_entries=0` because the sandbox holds no `.ufo/**` files; that mirrors the original defect mechanism (root file outside both pathspec elements), it is not an empty-tree artifact — `c3-after.json` on the same sandbox 33 ms later enumerates 2 entries. `repo_root`==sandbox in both runs: no enclosing-repo adoption. |
| **A3 — sibling/tracked control claimed?** | **Rejected for the receipts.** `c3-after.json` `candidate_count=1`, sole candidate `MoriR16.Lesson`; second untracked entry (`TabiR16.Lesson`, 29 B, `bytes_read=876−847`) was read and not emitted. `TabiR16.Lesson` carries the round-16 token in path *and* content (`Tabi round16 sibling control`) with a foreign lane token — a real negative control, not a decoy. **But see F2/F3: the counter expression itself does not check this, and the "tracked control" is vacuous.** |
| **A4 — counter gamed?** `jq` expression `1 − count(path=="MoriR16.Lesson")`. | Counted unit reproduces exactly `[1,0]` (recomputed; stdout_sha256 fields recompute). Setup payloads have no `candidates` key → would yield 1, so a setup failure cannot fake the 0. **Survives as F2**: the expression tests presence only. |
| **A5 — planted bytes ≠ committed input?** The recipe plants "byte-exact" `frozen/MoriR16.Lesson`; do receipts prove it? | **Survives as F1 (strongest).** Receipts record only `path`, `size_bytes=847`, `read_bytes=847` — no digest. The sandbox is deleted; the only committed construction record (`c3-capture-recipe.json`) is **untracked** (`git status` `??`); `frozen/c3-expected.json` was committed at `5c1dfb8` 16:37 — *after* the 16:34 measurement — and is absent from `PINNED_INPUTS.json`. ReceiptC3's mid-audit cmp/hash of the sandbox copy is post-hoc and uncommitted. A same-name same-size impostor yields identical committed receipts. |
| **A6 — no-pathspec coverage complete?** | **Partially survives (disclosed tradeoff, not a defect).** Enumeration is `git status --untracked-files=all`: tracked misroots and git-ignored files are invisible (tool `--help` and `build/MisrootSweep.md:213–218` disclose both). Verified live: fleet `.gitignore`/info-exclude do not hide root `*.Lesson` files (`git check-ignore` rc1), so this does not affect the replayed r16 case. A misroot with neither filename nor content tokens is invisible under *any* enumeration — an undetectable class, bounded but not claimed. |
| **A7 — ownership vs candidacy?** | **Rejected.** Candidate `class` is `candidate_misroot`; `matched_in` names evidence sources; no ownership field exists. Detector is intentionally over-inclusive (lane-token lexical match, e.g. `mori` in `…/mori-shokunin`). Claiming `MoriR16.Lesson` as a candidate for lane-mori review is a lexical lead, correctly labeled. |
| **A8 — measurement sandbox vs committed input pin?** | **Survives as F1/F4.** `PINNED_INPUTS.json` pins the tool (`0a852fe…` — matches `sha256sum` of `tools/mori-misroot-sweep.py`) and the frozen artifact, but nothing pins the *sandbox construction*; `c3-capture-recipe.json` is uncommitted working-tree content. |

## Surviving findings

**F1 — measurement authority gap (strongest).** The committed `1→0` transition binds
tool digest + argv + output, but the witness property it exists to prove (planted bytes ≡
committed `frozen/MoriR16.Lesson` ≡ fleet archive) is not cryptographically bound at
measurement time: receipts carry `size_bytes`/`read_bytes`, never a digest; the recipe is
uncommitted; `c3-expected.json` postdates the measurement and is unpinned; the sandbox is
gone. The r16 lesson itself demanded the sweep's clean result *not* be trusted as clean —
the same class of argument applies here at weaker strength: receipts alone cannot
distinguish byte-exact planted witness from an 847-byte impostor. The defect is
evidence-completeness, not a shown contradiction. **Fixable**: emit per-file sha256 in
`candidates` (and a `planted_sha256`/`expected_sha256` pair), commit the recipe before
measurement, add `c3-expected.json` to `PINNED_INPUTS.json`.

**F2 — counter narrower than the claim.** The contract's acceptance is three-part:
missed `1→0` **and** "sibling and tracked controls stay unclaimed" **and** (per
`c3-expected.json`) `matched_in==["path"]`. The counted expression checks only
`path=="MoriR16.Lesson"` presence. A detector that also emitted `TabiR16.Lesson`, or
matched the witness by content, would still count `0`. The raw receipt happens to
satisfy all three parts, so the claim is supported on inspection — but the *counted
assertion* does not encode them. **Fixable**: count
`(candidate_paths != ["MoriR16.Lesson"]) or (matched_in != ["path"])` per run.

**F3 — tracked control is vacuous in the measured sandbox.** The sandbox's only tracked
file is `seed` (5 B, content `seed\n` — no lane/round tokens). A tracked file is
invisible to `git status` untracked enumeration *by construction*, so "tracked controls
stay unclaimed" is trivially true and tests nothing in the measured witness; the
meaningful control (tracked file *naming* Mori/round-16, ensuring the tool doesn't scan
tracked content) exists only in the selftest (`tracked.txt`,
`mori-misroot-sweep.py:379`). **Fixable**: recipe step `write F/tracked.txt "Mori
round-16 tracked control" && git add && commit`.

**F4 — expected-file provenance ordering.** `frozen/c3-expected.json` entered in
`5c1dfb8` (the receipts commit, 16:37) after the 16:34:52 measurement it describes, and
it is not in `PINNED_INPUTS.json` while `frozen/MoriR16.Lesson` is. Post-measurement
expected files are the self-fulfilling-witness shape the C3 admission rule exists to
reject; here its contents are also derivable from contract.md:21–27, which predates the
measurement, so this is an ordering/provenance defect rather than evidence of
manufactured expectations. **Fixable**: commit expected files before measurement; pin
them.

## Rejected attacks (recorded so they are not re-litigated)

- Content arm untested on the witness → the true artifact is filename-only; requiring
  content match would be testing the wrong fixture. Path-arm requirement is
  mutation-proven (MutMisroot KILLED, `falsify/MutMisroot.md`).
- Legacy miss is vacuous → the pathspec exclusion is exactly the r16 mechanism;
  `untracked_entries=0` vs `2` on the identical sandbox isolates pathspec as sole cause.
- Sibling-claim → receipts show `candidate_count=1`; counter cannot be improved by
  sibling emission (ReceiptC3 §3).
- Setup-failure faking the 0 → setup payloads lack `candidates`; jq yields 1.
- Duplicate-authority / double counting → single witness, single artifact; the
  selftest's embedded base64 is a *separate* hermetic instrument (advisory per M10),
  not counted evidence.

## Verdict

The declared count `1→0` is honest arithmetic over committed receipts and the
filename-only witness is authentic — the strongest falsification attempts fail. What
survives is a coherent provenance/narrowness cluster (F1–F4): **the committed measurement
does not, by itself, prove the witness property it claims**, because the sandbox recipe
is uncommitted, the expected file postdates and is unpinned, no planted digest is
recorded, the counter ignores two of three claim parts, and the tracked control is
content-free. All are fixable without changing the tool's detection semantics; none is a
tradeoff the judge must accept as inherent (the A6 untracked-only boundary *is* a
disclosed tradeoff, appropriately out of scope for a lane-scoped untracked-misroot
sweep). Impacted axes: C3 measurement fidelity/provenance; score 5 claim unaffected in
substance but its committed witness trail is weaker than the pinned-input standard the
round sets for C1/C2.

## Smallest safe correction

1. Probe emits `sha256` per candidate + `scan.planted` digest assertions; rerun once,
   commit receipts. 2. Commit `c3-capture-recipe.json` (and `c3-expected.json` before
   measurement), add both to `PINNED_INPUTS.json`. 3. Counter:
   `[run | .candidates == [{path:"MoriR16.Lesson"}] and .candidates[0].matched_in == ["path"]]`.
   4. Recipe adds a content-bearing tracked control file. Total: probe schema +one field,
   recipe +2 lines, counter +one predicate — no detection-logic change, no rerun of the
   historical r16 baseline needed.

## Discipline

No installs/upgrades; no pacman; no `/tmp` writes; no background jobs; no journalctl; no
VCS mutation (read-only `git log/ls-tree/cat-file/status/check-ignore`); no probe/selftest
reruns — all counts recomputed read-only from committed receipts. Writes: this report
only. Attacked scope: C3 claim, its tool contract, measured receipts and pinned/frozen
inputs — not a blanket pass on C1, C2, or unexamined C3 prose.
