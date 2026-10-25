# mori round 47 — wave w2 — MutV2Exact (mutation-test v2 in scratch)

Seat: MutV2Exact · Lane: mori-shokunin · T = `68d66ca53d89be5c34a62f46af7c37449d9f9b63` · Target: v2 `tools/mori-pin-check.py` at T.

## Scope and method

- Target bytes extracted read-only from git: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 68d66ca…:tools/mori-pin-check.py > .scratch/r47w2-MutV2Exact/pin-v2-pristine.py` (633 lines).
- Pristine v2 sha256: `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6` — identical to the working-tree `tools/mori-pin-check.py` at measurement time (same hash from `sha256sum tools/mori-pin-check.py`), so the tested bytes are the tracked v2 bytes.
- Detector: the tool's own `--selftest` (34 arms), run with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-MutV2Exact` on every run.
- All edits were made to scratch copies only (`cp` from pristine, then edit of the scratch absolute path). No tracked lane path was ever passed to an edit tool; no git/jj mutating command was run.
- Tooling authorization: no installs or upgrades performed — python3 already present; nothing to record.
- No subagents used (leaf seat).

## Baseline (pristine bytes)

```
$ TMPDIR=<scratch> python3 .scratch/r47w2-MutV2Exact/pin-v2-pristine.py --selftest
… 34 arm lines, all PASS …
PIN_CHECK_SELFTEST pass=34 fail=0
PRISTINE_RC=0
```

Detector valid on pristine bytes (a baseline failure would have made all mutants inconclusive; not the case).

## Mutant A — revert exact match to startswith — KILLED

- File: `.scratch/r47w2-MutV2Exact/mut-a-startswith.py`
- Mutation (line 358, single point): `ok = observed is not None and observed.strip() == want` → `ok = observed is not None and observed.startswith(want)`
- v1 grounding: frozen v1 (63eecf27, sha256 `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1`) matched with prefix-anchored startswith semantics: `re.match(re.escape(want) + r"(?![0-9A-Za-z])", observed.strip())` (v1 line 262). The reversion direction matches history.
- Mutated sha256: `a18d4c15198aa8966da88eb06dccffcd581de58246602265016bf5dd9c9388df`
- Run: `TMPDIR=<scratch> python3 .scratch/r47w2-MutV2Exact/mut-a-startswith.py --selftest` → rc=1

```
FAIL token_boundary_truncated_pin  PIN_CHECK=met tally_pins=1 … mismatches=0 …
FAIL v2_weakened_pin_exact  PIN_CHECK=met tally_pins=1 … mismatches=0 …
PIN_CHECK_SELFTEST pass=32 fail=2
MUTA_RC=1
```

- Killing arms (both flip to a false green): `token_boundary_truncated_pin` (observed `pass=33 fail=0` startswith pinned `pass=3`) and `v2_weakened_pin_exact` (observed `pass=3 fail=0` startswith pinned `pass=3`).
- Verdict: **KILLED** — two independent arms catch the weakened matcher.

## Mutant B — drop the duplicate-name condition — KILLED

- File: `.scratch/r47w2-MutV2Exact/mut-b-nodup.py`
- Mutation (single point, `check()`): removed the 4-line loop `for name, n in sorted(names.items()): if n > 1: counts["duplicate"] += n - 1; out.append("pin kind=row state=duplicate …")`. `counts["duplicate"]` can then never rise, so `met` ignores duplicate row names.
- v1 grounding: frozen v1 has no `duplicate` counter at all (its counts dict and `met` conjunction lack the term) — the reversion direction matches history.
- Mutated sha256: `d187113e0e3433006f7cb4345db150373fdd6d17954b4deceeefecd7df8c0f7d`
- Run: `TMPDIR=<scratch> python3 .scratch/r47w2-MutV2Exact/mut-b-nodup.py --selftest` → rc=1

```
FAIL v2_duplicate_name  PIN_CHECK=met tally_pins=2 … unparsed=0 … duplicate=0 …
PIN_CHECK_SELFTEST pass=33 fail=1
MUTB_RC=1
```

- Killing arm: `v2_duplicate_name` (two parsed rows named `foo`; want unmet/state=duplicate, mutant reports met). `v2_hidden_row_and_duplicate` stayed unmet (its unparsed=1 counter still fires via the `(?i)` matcher), consistent with a single-point mutation.
- Verdict: **KILLED**.

## Mutant C — make unparsed detection case-sensitive again — SURVIVED (coverage finding)

- File: `.scratch/r47w2-MutV2Exact/mut-c-casesens.py`
- Mutation (line 318, single point): `if re.search(r"(?i)selftest", row["raw"]):` → `if re.search(r"selftest", row["raw"]):`
- v1 grounding: frozen v1 counted unparsed rows only on the uppercase substring `"SELFTEST" in row["raw"]` (v1 line 236); v2 widened to any case. The reversion direction matches history.
- Mutated sha256: `b35ec1e6f79ccecd70a96c3e124b05a65f7f1e18a0acd6b42214bd910f7a8d91`
- Run: `TMPDIR=<scratch> python3 .scratch/r47w2-MutV2Exact/mut-c-casesens.py --selftest` → rc=0

```
PIN_CHECK_SELFTEST pass=34 fail=0
MUTC_RC=0
```

- Verdict: **SURVIVED** — all 34 arms pass, byte-identical result profile to pristine. A surviving mutant is a coverage finding, not permission to change the contract.
- Why it survives: the only selftest arms that contain an unparsed row (`malformed_row`, `v2_hidden_row_and_duplicate`) both carry a lowercase `selftest` substring in the row raw (`--selftest` inside the command span; `foo_selftest` in the hidden row), so the case-sensitive regex still matches. No arm exercises a mixed-case-only spelling such as `Foo_Selftest`.
- False-green reproducer (probe fixture `.scratch/r47w2-MutV2Exact/probe-c/tree/`: `tools/foo.py` printing `FOO_SELFTEST pass=3 fail=0`; `SKILL.md` with one honest 8-cell row plus a 6-cell short row naming `Foo_Selftest pass=2 fail=0` — no lowercase `selftest` substring anywhere in that row's raw):

```
$ TMPDIR=<scratch> python3 pin-v2-pristine.py --root probe-c/tree --repo <scratch>
pin line=3 kind=tally prefix=FOO_SELFTEST state=match pinned='pass=3 fail=0' observed='pass=3 fail=0' rc=0 cmd='python3 tools/foo.py --selftest'
pin line=4 kind=row state=unparsed cells=6 header=8
PIN_CHECK=unmet tally_pins=1 digest_pins=0 mismatches=0 unparsed=1 …
PRISTINE_PROBE_RC=1

$ TMPDIR=<scratch> python3 mut-c-casesens.py --root probe-c/tree --repo <scratch>   # while mutated
pin line=3 kind=tally prefix=FOO_SELFTEST state=match pinned='pass=3 fail=0' observed='pass=3 fail=0' rc=0 cmd='python3 tools/foo.py --selftest'
PIN_CHECK=met tally_pins=1 digest_pins=0 mismatches=0 unparsed=0 …
MUTC_PROBE_RC=0
```

  The mixed-case disguised row is silently skipped (state=unparsed but not counted), and the remaining honest row satisfies the floor → `PIN_CHECK=met`. This is exactly the disguise class the `(?i)` widening exists for, and v2's selftest has no arm for it. (First probe run used a 7-cell honest row and was inconclusive for both binaries — discarded; the corrected 8-cell fixture above is the evidence.)

## Restoration evidence

- `mut-c-casesens.py` restored from pristine bytes and re-run: sha256 back to `9832e38c…`; restored `--selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0`, `RESTORED_RC=0` (equals pristine baseline).
- `mut-a-startswith.py` and `mut-b-nodup.py` restored from pristine bytes after their runs; final state of all four scratch copies:

```
9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6  pin-v2-pristine.py
9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6  mut-a-startswith.py
9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6  mut-b-nodup.py
9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6  mut-c-casesens.py
```

- Mutated-state hashes preserved above (A `a18d4c15…`, B `d187113e…`, C `b35ec1e6…`); mutants are reproducible from the documented one-line diffs.
- Lane integrity: `git status --porcelain -- tools/` → empty (0 lines) before and after; no tracked path edited at any point. Writes were confined to `.scratch/r47w2-MutV2Exact/` and this report.

## Seat verdict summary

| Mutant | Point attacked | Selftest result | Verdict |
|---|---|---|---|
| A | exact-match → startswith (line 358) | pass=32 fail=2, rc=1 | killed (arms: `token_boundary_truncated_pin`, `v2_weakened_pin_exact`) |
| B | drop duplicate-name condition (lines 311–314) | pass=33 fail=1, rc=1 | killed (arm: `v2_duplicate_name`) |
| C | drop `(?i)` in unparsed-row counter (line 318) | pass=34 fail=0, rc=0 | **survived** — coverage finding; false green shown on mixed-case `Foo_Selftest` short row |

Not attacked / not judged here (other seats' scope): the C1 calibration claim itself, C2 depth, and any other runtime. UNVERIFIED: nothing within this seat's assignment; all listed commands were run and their outputs and exit codes recorded above.

Report: .ufo/waves/round-47/w2/MutV2Exact.md
Report: .scratch/r47w2-MutV2Exact/
