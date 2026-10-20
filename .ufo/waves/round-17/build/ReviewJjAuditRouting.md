# ReviewJjAuditRouting — fix-now / why-not mapping of hyaku jj-w1 findings (mori round 17 wave 1)

Seat: MoriR17.ReviewJjAuditRouting-5 · 2026-10-20 · reviewer (advise only, never judge)

Sources mapped: `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditMori.md`
(risks 1–3, recommendations 1–6) and `JjTrialMori.md` (H1–H5), against
`.ufo/waves/round-17/contract.md` §C1/§C2 and `.ufo/waves/round-17/wave1-context.txt`.

Evidence basis (re-verified read-only this seat, lane at entering tip):
`git rev-parse HEAD` = `refs/heads/master` = `24526ea9617cd020fee16c28fe4d4a2789dc28cb`
→ all audit line cites are current. Confirmed in place:
`tools/mori-census.sh:2100` `cat-file -e "HEAD:$rpath"` and `:2102` `log -1 --format=%ct`
(HEAD-based report closure, row 6); `:2197` `rev-parse --verify -q HEAD` + `:2207`
`log --since` (row 9); `:2231` exact-author verdict `expected="$lane-shokunin
<$lane@shokunin.local>"`; census probes already hardened
(`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE GIT_OPTIONAL_LOCKS=0`, 2197/2207);
`mori-round15-regressions.py:782-784` inherits `os.environ` + only
`GIT_OPTIONAL_LOCKS=0`, guard list at `:1418` = `tools, .git, corpus` (no `.jj`);
`mori-round16-regressions.py:697-703` `_git` = `env = dict(os.environ)`, no
`--no-optional-locks`, no `core.fsmonitor=false`, no GIT_* scrub, guard list at `:747`
same omission; `mori-silence-cases.sh:436-443` `git_q()` definition-only, zero callers.

Axes: (1) item coverage — all 14 assigned items mapped, none skipped; (2) evidence — every
bucket cites path:line verified at 24526ea; (3) actionability — every item lands in exactly
one bucket with a named owner or a closed reason; (4) scope fidelity — nothing proposed
outside contract §C2, frozen gates r13–r16, or lane write scope.

Bucket rules: **fix-now** = delivered this wave, owner = the C2 executor (contract §C2
census + `tools/mori-round17-jj-regressions.py` gate); **why-not** = correct observation,
not actionable this wave, one-line reason.

## Risks (JjAuditMori)

**R1 — HEAD is not the branch under jj (D probes).**
- Census half → **fix-now**. Verbatim C2: resolve branch (symbolic-ref → `refs/remotes/origin/HEAD` → unique `refs/heads/master|main`), anchor rows 6/9 (`2100/2102/2197/2207`) on `refs/heads/<branch>`; verified HEAD-based today.
- Gates half (r13:1245, r14:432, r15:806, r16:712 `rev-parse HEAD` pins) → **why-not** — frozen historical gates r13–r16; their probes are normal-run-only (audit `[INFERENCE]`, selftest returns earlier), and wave-1 grading flows through the C2-anchored census, not through the frozen gates.

**R2 — lane authorship only correct via helper `metaedit --update-author` (census 2231).**
- Census finding half → **fix-now**. `LANE_AUTHOR_MISMATCH` (severity drift) is verbatim C2: post-launch branch commit with lane committer but differing author, instead of folding into `other_authored_commits`.
- "Keep helper as only commit path" half → **why-not** — status quo already holds: helper runs metaedit before commit (`jj-lane.sh` cmd_commit ~219; JjTrial step 4 measured author+committer = lane on push and on rebase), so there is no code to change, only discipline.

**R3 — zero jj-colocated coverage in every gate/selftest + two unhardened git readers.**
- Coverage half → **fix-now**. C2 gate `tools/mori-round17-jj-regressions.py` builds real colocated jj sandboxes and runs the census (entering `git show 24526ea:tools/mori-census.sh` vs delivered) — exactly the missing real-repo coverage, without touching frozen selftests.
- Unhardened readers (r15:782-784, r16:697-703, both re-verified) → **why-not** — frozen historical gates r13–r16; the census already demonstrates the hardened argv shape to copy when the gates are ever unfrozen; residual race accepted for wave 1.

## Recommendations (JjAuditMori 1–6)

**Rec 1 — branch resolver in census, `refs/heads/$branch` probes** → **fix-now**. Verbatim contract §C2 resolution order; census standalone (no shared library), as the audit itself requires.

**Rec 2 — `merge-base --is-ancestor HEAD refs/heads/<branch>` → drift row** → **fix-now**. Verbatim C2 `HEAD_BRANCH_MISMATCH`, severity drift, detail names lane/short head/short branch tip.

**Rec 3 — keep `ls-files -mo`, never add `--cached`/`ls-files -s` reads** → **fix-now** (zero-diff keep). Measured safe under colocation (F5/F6/F7; trial step 5 row B green); C2 changes grading refs only, row-B input untouched — recording the decision prevents a later "improvement" that jj invalidates.

**Rec 4 — add `.jj` to protected-output lists (r15:1418, r16:747; r13/r14 have none)** → **why-not** — frozen historical gates r13–r16 and contract restricts C2 to the census; severity low (F12) and invisible-mutation window accepted this wave.

**Rec 5 — harden `r16._git` / `r15._git` (locks, fsmonitor, GIT_* scrub)** → **why-not** — same frozen-gates reason; census-side hardening already in place (re-verified 2197/2207), so the hardened pattern is documented for a future unfreeze, not this wave.

**Rec 6 — jj-colocated case in silence-cases.sh + r13/r14 selftests** → **why-not for those files** (frozen historical gates); the fix-now equivalent is delivered by the C2 gate, which asserts real colocated behavior including branch anchoring — satisfying the audit's intent without editing frozen fixtures.
*(Out of assigned scope: Rec 7, delete dead `git_q()` — re-verified dead this seat (`silence:436-443`, zero callers); flag for a later cleanup round, no owner in wave 1.)*

## Hazards (JjTrialMori H1–H5)

**H1 — citeable hash moves on rebase (`committed` ≠ `pushed`).**
- Grading half → **fix-now**: C2 anchoring on `refs/heads/<branch>` stops probes from following the movable HEAD that makes orphaned drafts gradeable; pushed-vs-branch remainder keeps contracted row semantics ("otherwise unchanged").
- Citation half ("cite only `pushed`", merge-base guard on cited hashes) → **why-not** — process rule, already enforced by the helper printing `pushed` only after push success (trial step 4); no lane tool cites commit hashes, so there is no wave-1 code artifact to own it.

**H2 — repo jj config lives outside the repo (`~/.config/jj/repos/<config-id>/`)** → **why-not** — the fix lives in the fleet helper `jj-lane.sh` / host discipline, both outside lane write scope ("never edit fleet scripts"); documented mitigation (re-run `jj-lane.sh init` on any copied/rsynced lane) is sufficient for wave 1. This is the one live operational hazard with no in-repo fix.

**H3 — intent-to-add index pollution under `auto-track=all()`** → **why-not** — lane config is measured `snapshot.auto-track = "none()"` (trial step 2 config dump), so the hazard only materializes via H2 config loss; census row-B read measured unaffected (F5/F7, ` A` rows still visible).

**H4 — detached HEAD after first mutation; `@{u}` breaks** → **fix-now (already covered)** — C2 branch resolver never consults `@{u}` and `HEAD_BRANCH_MISMATCH` surfaces exactly the residual drift; no lane tool uses `@{u}` (trial step 5 measured), so nothing further to fix.

**H5 — index reset on every jj mutation loses staged entries** → **why-not** — measured non-issue: no lane tool stages (audit F5 + inventory: lane reads only `status --porcelain` / `ls-files -m|-o`); any fix targets the fleet helper, out of write scope.

## Residual risk and verification gaps

- Frozen-gate residuals carried forward, accepted: r15/r16 unhardened git env (R3/Rec 5), missing `.jj` output guard (Rec 4), no colocated arm in r13/r14/silence selftests (Rec 6). All are single-round unfreeze items with the census pattern to copy; none block C2.
- H2 config-loss is undetectable from inside the repo; only host discipline (re-init on copy) mitigates it. [INFERENCE] A future census info-row could fingerprint `auto-track` via a probe file, but that is new scope not in contract §C2 — not proposed for wave 1.
- Not verified (out of my item scope): C1 seat-terminal behavior; the delivered (post-edit) census — the C2 executor's gate run is the verification vehicle.
- Tooling: no installs performed (none needed). No VCS mutation; only read-only `git rev-parse`, file reads/greps; sole write is this report file.
