# Witness sandbox review

**Verdict: FAIL for scratch-confinement capability; PASS for the observed run and for distinguishing the sandbox by path, commit identity, and title.** Severity: **Medium** — `--out` can direct the clone and all subsequent sandbox writes outside the permitted scratch tree.

## Evidence

- The one requested execution used the scored tip and an explicit scratch output: `python3 .ufo/waves/round-38/fixtures/make-witness-sandbox.py f725f3076972e6e70595b5ac8279be524a111ff8 --out .ufo/waves/round-38/scratch/SentWitnessSandbox/run-20261023`. It printed sandbox commit `839e1b2346dc5d2eaae0d9eb8d1c3cf6434da725` and the sandbox path. Inspection reported its root as `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-38/scratch/SentWitnessSandbox/run-20261023`, with `HEAD` parent exactly `f725f3076972e6e70595b5ac8279be524a111ff8`; this run wrote its clone under scratch.
- Clone source and provenance: `.ufo/waves/round-38/fixtures/make-witness-sandbox.py:45-51` resolves the requested revision in `lane`, then runs `git clone --quiet --shared lane out` and checks out that revision. Observed `origin` is the lane path and `.git/objects/info/alternates` points to the lane's `.git/objects`; this is a shared clone, not an independent provenance root.
- Requested substitutions are fixed at lines 24-28: fixture payloads replace `corpus/knowledge/source-drift-hardening-r37.md`, `SCORECARD.md`, and `.ufo/waves/round-37/evidence/drift-live-r37.txt`. The sandbox commit's changed-path listing contained exactly those three paths.
- It does not pass as the lane by the requested path/identity/title signals: the sandbox root is distinct; local Git identity is `mori witness <witness@shokunin.invalid>` (set at lines 52-53), unlike the lane tip's `mori-shokunin <mori@shokunin.local>`; and the sandbox commit title is `fabricated token-satisfying binding (control)` (line 61), unlike the lane tip title. It is detached at the fabricated commit. A consumer that identifies a repository solely by `origin` could confuse the clone's source with its identity, since `origin` intentionally points at the lane.
- Scratch confinement is not enforced: lines 47-48 place the *default* temporary output under lane scratch, but when `--out` is supplied, `args.out` is used as-is. Lines 49 and 54-61 then clone and write there without resolving or checking that the destination is inside scratch. An external `--out` path is therefore a write escape, though it was not used in this run. `FIXTURES` is also fixed to `DEFAULT_LANE` at lines 22-23, even if `--lane` is overridden; this run used the default lane.

## Exploit path and impact

A caller can supply an absolute output path or a relative path containing `..` via `--out`; the builder will clone there and write the substitutions, Git config, and commit in that destination. This defeats the stated scratch-only boundary (without needing a path-traversal substitution, since the destination itself is caller-controlled).

## Smallest remediation

Canonicalize `out` and reject it unless it is beneath the canonical lane scratch directory before calling `git clone`; apply the same check to explicit and default destinations. If alternate `--lane` support is intended, derive fixture paths from that selected lane or explicitly reject the mismatch.