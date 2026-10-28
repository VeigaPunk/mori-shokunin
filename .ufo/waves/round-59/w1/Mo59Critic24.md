# Mo59Critic24 — adversarial review: MANIFEST_REV pinning (C1)

Seat attack: what does a post-pin MANIFEST change do to the counter (stale pin vs live file)?
Scope: `.ufo/waves/round-59/count-c1.py`, `tools/mori-register-check.py`, fleet `MANIFEST.json`.
Method: read-only on both repos; all mutations confined to a `--shared` scratch clone under
`$HYAKU_SCRATCH/mori-r59/Mo59Critic24/` (removed after run). Verdicts below are exercised end-to-end,
not inferred.

## Verdict: NO counterexample to the frozen claim — but three bounded risk classes, all judge-side

The pin is a *commit* OID (`2807c6ab…e14`, `git cat-file -t` → commit, ancestor of fleet HEAD today)
and `count-c1.py:169` reads `git_show(fleet, MANIFEST_REV, "MANIFEST.json")` — i.e. an **immutable
historical blob**, never the live file. A post-pin MANIFEST edit therefore can *never* change the
manifest-arm verdict for a given SCORECARD@R: the arm is a pure function of
(`MANIFEST_REV` object availability, scorecard@R, pointer set@R). Monotone, content-addressed,
branch-agnostic. That is the correct semantics for the frozen predicate (contract L36-38: "binding
at revision-pinned fleet commit"), and it is also the entire attack surface: **the counter cannot see
live-fleet drift, only object loss.**

## Demonstrated facts

| # | Fact | Evidence |
|---|------|----------|
| 1 | Fleet MANIFEST already diverged post-pin: commit `8da77f86` appended `rounds[864]` (kama r60 closure); `show M:MANIFEST.json` sha `159b6a59…` ≠ `show HEAD:MANIFEST.json` sha `342fc6e1…` | `git -C /home/vgpnk/Projects/shokunin log --oneline 2807c6ab..HEAD -- MANIFEST.json` → 1 commit; diff shows +round 60 entry only |
| 2 | Inert divergence: `rounds[832]` still binds — append-only growth is invisible and harmless | baseline run: `C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=HEAD`, exit 0, `--fleet` = real fleet |
| 3 | **Material divergence is equally invisible**: in a `--shared` scratch clone I committed a HEAD edit replacing `rounds[832].capabilities_added` with `["RETRACTED capability (post-pin edit)", …]`; counter → `C1=met … rev=HEAD`, exit 0, byte-identical verdict to baseline | `count-c1.py HEAD --fleet <scratch>/fleet-drift` |
| 4 | The tool itself is NOT blind: run directly on the retracted manifest it exits 1 with `verdict REGISTER_UNMET`, `reasons: manifest:name=rounds[832].capabilities_added[0]`, `[1]` (BOUND requires leading name `dual-shape seat-output vote binding` / `strict per-event driver-liveness probe`) | `mori-register-check.py --scorecard SCORECARD@HEAD --manifest manifest-live.json …` → `LIVE_EXIT=1`; same inputs with pinned manifest → `REGISTER_MET`, `PINNED_EXIT=0` |
| 5 | **Object loss → permanent unmet**: counter against an empty `git init` fleet → `C1=unmet selftest=ok fixtures=ok real=bad pointers=bad rev=HEAD failed=manifest`, exit 1. No ancestry/reachability guard exists (`MANIFEST_REV` is only checked `len==40` in selftest, count-c1.py:231) | `count-c1.py HEAD --fleet <scratch>/fleet-empty` |
| 6 | `--fleet` accepts ANY repo containing commit M: my drifted clone (M present via shared objects) emits the identical `C1=met` token — receipt carries no fleet identity | same output as #2/#3 |
| 7 | `rounds[832]` binds **positionally** (tool L156-159: `rounds[ri]`, checks `lane`, `capabilities_added[j]` leading name, `lane_round`; no `round` field check) — inside the pinned blob this is frozen forever; it only matters if the pin were ever retargeted to a live file | tool source |
| 8 | Frozen integrity holds: sha256 of count-c1.py / count-c2.py / contract.md identical at freeze `60b3a76` and lane HEAD `8ff344f` | `git show <rev>:<path> | sha256sum` ×3, all SAME |

## Risk classes

**R1 — stale-pin blindness (provenance/soundness of *interpretation*, bounded).**
`C1=met rev=R` is emitted identically whether live `MANIFEST.json` equals the pinned blob or has
retracted the bound rows (#2 vs #3: identical output under a demonstrated retraction). The token's
`rev=R` names only the lane revision; the manifest half was measured at `MANIFEST_REV`, a different
repo and revision never recorded in the receipt. A reader of the receipt alone cannot tell the
claim is pinned-stale. Contract-compliant (pin is explicit at contract L36-37), but the receipt is
**ambiguous without the pin context** — the only fixable point outside frozen bytes.

**R2 — fleet object-retention dependency (availability, demonstrated).**
The claim's fate depends on object `2807c6ab` surviving in whatever repo `--fleet` resolves to.
Fleet history *is* rewritten in practice — MANIFEST notes for round 81 record "detached-HEAD
premeasure rev orphaned by M81-4 rewrite". If the pin commit is ever orphaned+gc'd, C1 is
permanently `failed=manifest` regardless of lane state (#5). Verified today: `merge-base
--is-ancestor 2807c6ab HEAD` → true. Nothing enforces this at future scoring time.

**R3 — `--fleet` mirror divergence (false provenance, demonstrated).**
`C1=met` is reproducible against *any* repo containing M — including a stale mirror or a clone whose
HEAD retracted the capabilities (#6). Two verifiers can emit divergent verdicts for the same frozen
claim purely by repo choice. Additionally the counter echoes `rev=` verbatim — a `rev=HEAD` receipt
cannot be re-verified after HEAD moves (frozen command spec says `R`; scorers must pass the sha).

## What is NOT a defect

- Positional `rounds[832]` binding (#7): inside an immutable blob there is nothing to rebind.
  `lanes`/`lane_round`/`name` checks plus `pointers` resolution under lane-R make the pin snapshot
  self-consistent; `first-working round = 56 = lane_round` verified live.
- Tool coverage of manifest mutation: fixtures f08/f09/f10/f11/f12 cover name-altered,
  substring-only, foreign-lane, wrong-index, lane_round-mismatch — and the live run (#4) shows the
  name binding actually fires on drifted bytes. The blindness is in *which manifest the counter
  hands it*, not the check.
- C2 has no MANIFEST dependency at all; this seat's attack surface is C1-only. `rev=` echo nit is
  cosmetic and out of kill-rule scope.

## Smallest safe correction (judge-side only — counter bytes are frozen)

1. Require the default `--fleet /home/vgpnk/Projects/shokunin` for scoring receipts, and verify
   `git merge-base --is-ancestor 2807c6ab8a9b04dcf256682bcd722c695fdd6e14 <fleet-tip>` at scoring
   time (receipts should record the fleet tip, not `rev=HEAD`-style refs; scorers must pass a
   literal sha for `R`).
2. Interpret `C1=met` strictly as "met against pinned manifest at 2807c6ab" — per contract — and
   annotate that any post-`2807c6ab` change to `rounds[832]` in live MANIFEST (retraction, rename,
   re-index) is out of scope of this counter by design, not a silent defect. Judge MAY add a
   one-line live-drift check: `git diff 2807c6ab <tip> -- MANIFEST.json | grep -c '832'` — cheap,
   report-only, does not touch frozen bytes.
3. If fleet history is ever rewritten such that M is unreachable, the honest outcome is
   `failed=manifest` (already observed) — treat as an infrastructure failure of the claim's
   provenance anchor, not a lane regression; do not re-score against a mirror without disclosing
   it, since mirror receipts are indistinguishable from fleet receipts (#6).

## Commands exercised (receipt)

```
# baseline — real fleet, lane HEAD
python3 .ufo/waves/round-59/count-c1.py HEAD --fleet /home/vgpnk/Projects/shokunin --scratch …/run-real
  → C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=HEAD  (exit 0)
# drifted scratch clone (HEAD MANIFEST has rounds[832] capabilities retracted; commit M present)
python3 …/count-c1.py HEAD --fleet …/fleet-drift --scratch …/run-drift
  → C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=HEAD  (exit 0)   # drift invisible
# object loss
python3 …/count-c1.py HEAD --fleet …/fleet-empty --scratch …/run-empty
  → C1=unmet … failed=manifest,real,pointers  (exit 1)
# tool on live-vs-pinned manifest bytes (scratch-materialized SCORECARD@HEAD + pointer files)
  pinned → REGISTER_MET;  live-retracted → REGISTER_UNMET reasons=manifest:name=…[0],[1]
```

No production edits, no lane VCS mutation, no fleet writes; scratch at
`/fast/scratch/hyaku/mori-r59/Mo59Critic24/` cleaned after run. Counter/contract bytes verified
byte-identical freeze→HEAD. Report: `.ufo/waves/round-59/w1/Mo59Critic24.md`.
