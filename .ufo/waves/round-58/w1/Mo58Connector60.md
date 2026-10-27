# Mo58Connector60 — round 58 w1 connector seat

Scope: C1 do-nothing measurement at entering `b783d0b8…`; connector overlap/refusal scan. Read-only. No commits, no VCS mutation, no fleet/sibling writes. Scratch: `/fast/scratch/hyaku/mori-r58/Mo58Connector60` (empty; cleaned before yield).

## Receipts (exact commands, output, exit)

Environment: `TMPDIR=/fast/scratch/hyaku/mori-r58/Mo58Connector60`. Lane toplevel asserted: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin/mori-shokunin`. Lane HEAD `4272736c` (freeze-validated dispatch commit atop freeze `fe880112`).

1. C1 frozen counter at entering `b783d0b8…` (run from the on-disk frozen counter; it reads `SCORECARD.md` via `git show <rev>`):
   - `python3 .ufo/waves/round-58/count-c1.py b783d0b892637ce8d20f188cad20e4d8913ca635`
   - `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=b783d0b8…` — **exit 0**
2. C1 frozen counter at freeze `fe880112…`:
   - `C1=met rows=2 pointers=ok manifest=ok binding=ok failed=none rev=fe880112…` — **exit 0**
3. C1 selftest: `python3 .ufo/waves/round-58/count-c1.py --selftest` → `C1_SELFTEST pass=4 fail=0`, **exit 0**
4. Round-57 contrast counter at entering: `python3 .ufo/waves/round-57/count-c1.py b783d0b8…` → `C1=unmet rows=0 evidence=bad rev=b783d0b8…`, **exit 1** (matches contract's stated contrast).
5. C2 frozen counter: at `fe880112…` → `C2=unmet entry=absent failed=entry`, **exit 1**; at `b783d0b8…` → `C2=unmet entry=absent failed=entry`, **exit 1**. C2 selftest → `C2_SELFTEST pass=6 fail=0`, **exit 0**.
6. Entering register facts: `git show b783d0b8…:SCORECARD.md` — `## Capabilities` at 596 (stub) and 637 and 1951 (active register; preamble line 1953 contains "the lane's current capabilities register"). Rows `rounds[832].capabilities_added[0]` at 1989 and `[1]` at 1990. Pointers `tools/mori-vote-bind.py`, `tools/mori-driver-liveness.py`, `.ufo/waves/round-56/evidence/c1-at-landed.txt`, `.ufo/waves/round-56/evidence/c2-at-landed.txt` all `git cat-file -e` → exit 0.
7. `SCORECARD.md` blob at entering and freeze are identical (`fded56fc5a4961fef3de550174e56aaf7f01ae42`). The freeze diff `b783d0b8..fe880112` touches only round-58 evidence/controls and counter files (5 files, +581), not SCORECARD.

## C1 do-nothing finding

- The frozen counter's target output `C1=met rows=2 pointers=ok manifest=ok binding=ok` is **already produced at the entering revision with zero SCORECARD or tool edits**. The only delta needed to reach the frozen target is the counter file bytes themselves (the contract's "Before" control conflates "counter file absent at R" with "claim unmet at R"). The `contract.md` "Before (control)" line is accurate only for `git cat-file -e` of the counter path; the claim predicate, as frozen, is satisfied by pre-existing state.
- Consequence: C1 as frozen has no discriminating power between "lane did round-58 work" and "lane did nothing but land the counter". Its do-nothing control (fixture-based, selftest arms) is the only thing separating work from no-work. Reported as a finding; no remediation proposed (claims/counters are frozen).
- Cheapest no-work state meeting the target: entering tree + the frozen `count-c1.py` bytes placed at `.ufo/waves/round-58/count-c1.py`. No edits to SCORECARD required.

## C1 counter weaknesses (detection only, frozen — do not patch)

- **Manifest unpinned to R.** `measure()` reads `FLEET/MANIFEST.json` from the live fleet working tree (`FLEET = dirname(LANE)`), not `git show R:MANIFEST.json`. The `rev` argument does not pin the manifest arm. Lines 110-119.
- **Silent pointer skip for non-allowlisted prefixes.** Lines 101-108: a backticked path is only existence-checked if it starts with `.ufo/`, `tools/`, or `corpus/`. Any other prefix (e.g. `scripts/x.py`) containing `/` or ending in `.py/.txt/.md` is skipped with no failure. This contradicts the contract's "every evidence pointer … resolved via `git cat-file -e`" wording for those prefixes. Current register rows use only allowlisted prefixes, so the frozen target output is unaffected today.
- Row selection is by substring `any(k in ln ...)` over the body; `len(rows)==2` guards count only.

## C2 state

- Entry, pinned copy, S550 and counter bytes absent at entering and at freeze except counter file (present at freeze, `count-c2.py`). `C2=unmet entry=absent` at both revs. The no-work state cannot meet C2; it needs the entry, pinned copy and S550 row (out of connector scope).

## Connector: sibling lane surfaces and overlap/refusal boundaries

- Fleet siblings with `.ufo/waves/round-58/` directories (read-only check): `chousa-shokunin`, `kake-shokunin`, `kotoba-shokunin`, `kotodama-shokunin`, `kumitate-shokunin`, and `mori-shokunin`. Only `mori-shokunin` has `count-c1.py`; no sibling has a `count-c1.py`/`count-c2.py` under round-58 — no counter-name collision found.
- Shared-surface boundary: the mori lane's `SCORECARD.md`, `corpus/`, `MANIFEST.json` (fleet root) and `LOG.md` are fleet-level or lane-level state. C1's manifest arm reads the fleet-root `MANIFEST.json`; any sibling/fleet write to that file changes C1 without changing the lane revision (see weakness above). Refusal boundary: this seat did not read or write any sibling's round-58 files beyond directory existence.
- Lane working tree is dirty with peer-seat report files under `.ufo/waves/round-58/w1/` and modified `corpus/README.md`, `corpus/SOURCES.md` (uncommitted, not in freeze). These are outside this seat's scope and were not touched.

## Hygiene

- Disk guard status (read-only): `/fast/scratch/hyaku` 31% used, 554.1G free; `/tmp` 4%, `/var/tmp` 35%. No ENOSPC observed; no heavy work run.
- Tool installs: none. Pacman: not run.
- Scratch `/fast/scratch/hyaku/mori-r58/Mo58Connector60` contains no files; removed before yield.

## Verification to run once by main agent

- `python3 .ufo/waves/round-58/count-c1.py <R>` at the round-end revision (expected `C1=met … rc 0`).
- `python3 .ufo/waves/round-58/count-c2.py <R>` (expected unmet until S550/entry land).
- Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori`.
