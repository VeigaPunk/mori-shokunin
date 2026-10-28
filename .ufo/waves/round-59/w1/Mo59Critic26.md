# Mo59Critic26 — do-nothing adequacy attack (critic)

Scope: is there a committed state between entering (`2b9f0397`) and freeze
(`60b3a76a`) that scores `met` with less work than claimed? Method: ran the
frozen counters read-only against every candidate revision between entering and
lane HEAD (`7b86704d`), plus full path-history greps. Scratch:
`/fast/scratch/hyaku/mori-r59/Mo59Critic26/` (cleaned). No production edits, no
VCS mutation, no fleet writes.

## FINDING 1 — C1 is `met` at the freeze commit itself: zero wave work (counterexample)

```
python3 .ufo/waves/round-59/count-c1.py 60b3a76a --scratch $TMPDIR/c1-freeze
→ C1=met selftest=ok fixtures=ok real=ok pointers=ok rev=60b3a76a…   exit 0
python3 .ufo/waves/round-59/count-c1.py 8ff344ff --scratch …   → C1=met  exit 0
python3 .ufo/waves/round-59/count-c1.py be737211  / 7b86704d         → C1=met  exit 0
```

- `git cat-file -e 60b3a76a:tools/mori-register-check.py` → EXISTS, and its
  sha256 is exactly the counter's `PIN` `38b733d8…472b8`.
- The capability was landed inside the freeze bundle, not by wave work:
  `ccfd554e` ("freeze contract, C1/C2 counters, tools, fixtures, controls",
  02:49:04) created the tool at sha `02feb852`; `60b3a76a` ("freeze amendment
  … pre-data", 02:50:48) patched `check()`'s name-boundary test and re-pinned
  `count-c1.py` `PIN:` to the new sha. Earliest `C1=met` revision = `60b3a76a`
  (`ccfd554e` scores `unmet failed=tool_sha,real`).
- The contract's "Before (do-nothing control … `failed=tool_absent`)" only
  falsifies the entering revision. Every committed state from the freeze
  onward satisfies the C1 claim with nothing left for the wave: no dispatched
  seat builds the tool (dispatch grep: `tools/mori-register-check.py` appears
  only in Mo59MutationTester33's fixture-mutation item and Mo59Simplifier63's
  dead-code review — no build seat).
- Impact: false provenance — wave cannot claim C1 work landed in-round; the
  verifier will correctly measure `met`, but any seat/report claiming "the
  wave landed the C1 tool" is unsubstantiated. The claim is satisfiable
  do-nothing post-freeze; it is not a defect in the counter (the counter
  correctly discriminates `ccfd554e`), it is a framing/provenance defect in
  the claim: "the lane lands" is trivially true at freeze time.
- Smallest safe correction: none needed for counting honesty (receipt will be
  truthful if seats phrase it as "verified already-met at freeze", not
  "landed"); the L1's lesson/report should disclose that C1 capability work
  predates the wave by ~2 minutes, or the claim wording should distinguish
  freeze-bundled vs wave-landed work.

## FINDING 2 — C2's capability half is also pre-landed; residual work is a ~2560-line data commit

```
python3 .ufo/waves/round-59/count-c2.py 60b3a76a --scratch …
→ C2=unmet selftest=ok scan=ok drift=ok trees=ok entry=bad rows=bad pins=bad
  tree=bad claims=0 files=0 … failed=copy_absent:…×6,entry_absent,tree   exit 1
```

- `tools/mori-settlement-scan.py` was committed at `ccfd554e` already at the
  pinned sha `4c04bf21…5ac9a9` — the entire tool/selftest/scan/drift/trees
  arm set passes do-nothing at freeze. No committed state met C2 pre-freeze
  (entry/copies/rows never existed before `be737211`), so the "Before"
  control is honest.
- The data landed in ONE integrator commit `be737211` (03:00:09, ~8 min after
  dispatch at 02:53) + a 3-line correction `7b86704d` (demoting claim K11 —
  the r53 copy was outside the frozen `ARTIFACTS` map):
  - `count-c2.py be737211` → `unmet failed=entry` (claims=14, files=7)
  - `count-c2.py 7b86704d` → `C2=met … claims=13 files=6` exit 0
- Residual C2 work was already near-minimal: `be737211` added only 8 SOURCES
  rows (S553–S560), 7 copies (~1.6 MB of byte-exact artifacts), a 47-line
  entry, quarantine lines — no cheaper committed state exists because the
  entry grammar + per-copy rows force that shape.
- Impact: same provenance pattern as Finding 1 — the capability half of C2 is
  freeze-bundled; only the data half required in-wave work, and it was
  integrator-landed within minutes of dispatch, not produced by the 64-seat
  fleet (Scribe47's "draft the C2 entry skeleton" seat is advisory; the
  committed entry arrived from `mori-shokunin` commits).

## Impacted axes

- **C1 (calibration):** claim is met-provable trivially; wave-landed
  provenance is false → report/lesson must not credit wave work for the tool.
- **C2 (depth):** claim needs the `be737211`+`7b86704d` data commit; anything
  less scores `unmet`. No cheaper committed state.
- **Kill rule check:** `git diff 60b3a76a HEAD -- count-c1.py count-c2.py
  contract.md` is empty (sha256 2be6fda8…, 2df3ae84…, 427fca0b… respectively)
  — frozen bytes intact; no counter invalidation from this finding.

## Verdict

Adversarial finding stands: a do-nothing state exists for C1 (freeze revision
`60b3a76a` onward, i.e., less than zero marginal work — the claim is
satisfiable before any seat runs). For C2, no do-nothing state exists, but
the claimed work overstates what the wave must contribute: the tool arm is
pre-landed and the data arm is a single small integrator commit. Both claims
share a provenance pattern (capability landed inside freeze commits authored
by `mori-shokunin`, pre-dispatch) that the frozen "do-nothing" control at
`2b9f0397` does not capture.

## Evidence commands (all read-only, run from lane repo)

- `git cat-file -e <rev>:<path>` / `git show <rev>:<path> | sha256sum` for all
  claimed paths at `2b9f0397`, `ccfd554e`, `60b3a76a`, `8ff344ff`,
  `be737211`, `7b86704d`.
- `python3 .ufo/waves/round-59/count-c{1,2}.py <rev> --scratch
  /fast/scratch/hyaku/mori-r59/Mo59Critic26/…` — outputs verbatim above.
- `git log --format='%h %ci %an %s' 2b9f0397..7b86704d`; `git diff --stat`
  between revisions; `git log --all --oneline -- <paths>` for history sweep.
- `w1-dispatch.json` task scan: 64 seats, none builds `mori-register-check.py`.
