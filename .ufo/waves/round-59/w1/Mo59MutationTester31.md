# Mo59MutationTester31 — C1 counter mutation probe (round 59, w1)

Seat: mutation-tester, lane `mori-shokunin`, freeze `60b3a76ad0524c8978cc51922940be1c8c388915`,
entering `2b9f03975bfb6e508f35074ac8181ec8bf54e805`. Read-only on lane and fleet;
all mutation work on scratch copies under
`/fast/scratch/hyaku/mori-r59/Mo59MutationTester31/`. Detection only; no remediation, no
contract/counter edits, no scoring claim.

## Axes (godspeed)

1. **Kill coverage** — which of the three assigned counter mutations escape detection.
2. **Cost** — full probe matrix (17 counter runs + 5 selftests, each run exercising the
   pinned tool's selftest + all 13 hostile fixtures + 2 real-arm tool passes) in 8.6 s wall.
3. **Evidence completeness** — before/after hashes, exact outputs, byte restoration.
4. **Harm-none** — every mutant still accepts the genuine state (no false-positive regression).

## Method

Detector = `.ufo/waves/round-59/count-c1.py` (pristine sha256
`2be6fda8c54633fd96f9d447e8e78ff4ba4a6d6136670f79a9d622003f0c9dfd`; blob
`251d4de216c70e506e504ae7b43a7a5979f53027` = freeze-rev object). Mutants are scratch copies,
never the lane file. States:

- **G (genuine)**: sandbox lane repo (scratch `lane.amrU`) at `16c112f5c244336c5dc1cc7342ff9261d5dfeb73`
  containing the PIN-sha tool (`38b733d8…472b8`, extracted from the freeze commit), all 13
  committed fixtures from the freeze rev, a well-formed register scorecard and committed
  evidence; fleet repo `fleetG.lhio` with HEAD = pinned commit `2807c6ab8a9b04dcf256682bcd722c695fdd6e14`.
- **C (ghost pointer)**: same lane at `2061c88de5e14bd691ce69b6f91061f4e8e5c56b` — evidence cell
  cites `evidence/ghost.txt` which is absent from the commit; genuine fleet.
- **B (forged fleet)**: lane @ G-rev; fleet repo `fleetB.35E1` whose HEAD commit carries an
  attacker MANIFEST.json — `rounds[832]` kept tool-compatible (`lane=mori`, `lane_round=56`,
  both capability entries = the published register names), while `rounds[831]`/`rounds[833]`
  are forged (`lane=FORGED-NEIGHBOR`) plus a `forged: true` marker; the pinned object is
  **absent** from this repo.

## Mutants (smallest behavior-bearing edits, applied to scratch copies)

| id | edit (diff vs pristine) | sha256 |
|---|---|---|
| m1 | pointer arm removed: drop `failed.append("pointer:%s" % rel2)`; `ptr_ok = all_exist` → `ptr_ok = True` | `75dd893225091280a972b21c08ff8d55318ee7d0a950441c029dbd22567100c8` |
| m2 | binding relaxed to first-match: `sorted(bmap)==sorted(BOUND) and all(...)` → `any(bmap.get(k,"").startswith(v) ...)` | `612a009aac6edf4089684a077177c3af2ec3402b6695b6678af6804c3a41c0b6` |
| m3 | MANIFEST_REV pin dropped: `git_show(fleet, MANIFEST_REV, …)` → `git_show(fleet, "HEAD", …)` | `743693d6765b0bdbef7957680288ee1fd934130fa894516ca76c1d9a488bc67b` |
| m123 | all three | `fb722c273f7cdf1a02b01a1ecce356214ae0ac105bc3f7669e1bf25a84c71e83` |

## Results

Baselines (detector alive, both directions):

- Pristine @ entering `2b9f0397…` (real lane): `C1=unmet selftest=bad fixtures=bad real=bad
  pointers=bad … failed=tool_absent,selftest,fixtures_absent,manifest,real,pointers`, exit 1 —
  reproduces the frozen do-nothing control (`failed=tool_absent` present).
- Pristine @ freeze `60b3a76…` (real lane, real fleet): `C1=met selftest=ok fixtures=ok
  real=ok pointers=ok rev=60b3a76a…`, exit 0 — genuine state accepted.
- Pristine on G: `C1=met … exit=0`; on C: `C1=unmet … failed=pointer:evidence/ghost.txt,real,pointers`
  exit 1; on B: `C1=unmet … failed=manifest,real,pointers` exit 1 (refuses to bind when the
  pinned fleet object is absent — provenance enforced). No baseline failures ⇒ no inconclusive rows.

Matrix (verdict = does the mutant wrongly accept a state pristine rejects?):

| state | pristine | m1 | m2 | m3 | m123 |
|---|---|---|---|---||
| G genuine | met | met | met | met | met |
| C ghost pointer | **unmet** `pointer:…,real,pointers` | unmet `real` | unmet (≈pristine) | unmet (≈pristine) | unmet `real` |
| B forged fleet, pin absent | **unmet** `manifest,real,pointers` | unmet (≈pristine) | unmet (≈pristine) | **met, exit 0** | **met, exit 0** |

- **m3 (pin drop): SURVIVED** on state B — `C1=met selftest=ok fixtures=ok real=ok pointers=ok
  rev=16c112f5c…`, exit 0. The mutated counter binds capability provenance to attacker-supplied
  fleet HEAD bytes (`forged: true`, forged neighbor rounds) because the only content any arm
  checks is `rounds[832]`'s lane/lane_round/name-prefix fields, which an attacker can copy from
  the public register. m123 survives identically (m3 alone suffices; observed `C1=met` for m123 too).
- **m1 (pointer arm): KILLED** on state C — still unmet (`failed=real`): the real arm's second
  tool pass re-detects the missing pointer via the tool's `pointers:missing`
  (`tools/mori-register-check.py` checks `(Path(root)/rel).is_file()`), because the counter only
  materializes cat-file-resolved pointers into the tool root. The counter's pointer arm does no
  unique detection work on data-level states.
- **m2 (first-match binding): KILLED / shadowed** — identical to pristine on all three states,
  and analytically closed: the tool emits `bound[want] = entry` only after its name rule
  (`entry == name or entry.startswith(name)` + non-alnum boundary) passes, so any REGISTER_MET
  output already satisfies the strict clause `sorted(bmap)==sorted(BOUND) and all(startswith)`;
 no
  constructible data state makes first-match accept what strict binding rejects.
- Frozen selftest is blind to all mutants: `C1_SELFTEST pass=6 fail=0` exit 0 for pristine,
  m1, m2, m3, m123 (it checks constant shapes only; `MANIFEST_REV` stays defined in m3/m123 —
  only its use was retargeted).
- The 13-fixture battery is structurally blind to the escaping mutation: fixtures exercise the
  tool, and the tool never sees the pin — the pin lives only in the counter.

## Coverage finding (detection only)

The MANIFEST_REV pin is the single load-bearing defense for manifest identity/provenance in C1's
real arm; dropping it (m3, one-line mutation) escapes the entire frozen battery — hostile
fixtures, selftest, pointer arm and binding arm all still pass. The pointer arm and strict
binding arm are pure defense-in-depth (shadowed by the pinned tool's own checks plus the
materialize-and-rerun flow). Per the kill-rule framing this is a mutation-test observation about
detector redundancy, not a contract defect and not a scoring claim; frozen bytes are untouched.

## Restoration evidence

- The lane counter was never modified; mutants lived only at scratch copies.
- Post-run: `sha256sum .ufo/waves/round-59/count-c1.py` →
  `2be6fda8c54633fd96f9d447e8e78ff4ba4a6d6136670f79a9d622003f0c9dfd` (== before).
- `git status --porcelain -- .ufo/waves/round-59/count-c1.py` → empty.
- `git hash-object` of working-tree counter = `251d4de216c70e506e504ae7b43a7a5979f53027` =
  `git rev-parse 60b3a76a…:.ufo/waves/round-59/count-c1.py` (byte-identical to the frozen object).
- No fixture repo commits outside scratch; no fleet/sibling writes; no pacman; no new tools installed.

## Cleanup

All scratch receipts were copied into this report before cleanup;
`/fast/scratch/hyaku/mori-r59/Mo59MutationTester31/` (sandbox repos, mutants, logs,
`/tmp` never used) is removed as of the seat's final step.
