# ExecRerunC1v2 — falsification report, wave w2 (round 47)

Seat: ExecRerunC1v2 (leaf, no subagents). Target: **P-C1** at the landed tip
T = `68d66ca53d89be5c34a62f46af7c37449d9f9b63` — re-run the hardened `tools/mori-pin-check.py`
that is tracked at T, compare with `evidence/after-c1-v2.txt`, run `--selftest` and confirm
`PIN_CHECK_SELFTEST pass=34 fail=0` matches the SKILL.md registry row. All runs used
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r47w2-ExecRerunC1v2`
(never /tmp); no tools installed (none needed); no lane/fleet/git mutation (read-only `git
show`/`git diff`/`git rev-parse` only; lane dirty state pre-existing: `M LOG.md`, `M
SCORECARD.md` from before this seat).

## 1. Tool identity at T

- Frozen v1 (contract instrument, F = `63eecf27`): sha256 `e3ef425abde30974faf53a894f96650af11570d2125a5bf621395f6ab0d903e1` (matches contract; `git show 63eecf27:tools/mori-pin-check.py`).
- Tracked tool at T and working tree: sha256 `9832e38c3863ba82f7a740921e8c9d23d6cf2e702c2bb62ee2ad71fcc21bc2b6` — v2 (hardened; 223-line delta F→T), working tree clean for this file, so running `python3 tools/mori-pin-check.py` from the lane root runs T's bytes.

## 2. Rerun of the hardened tool at T (assigned command)

Command (from `/home/vgpnk/Projects/shokunin/mori-shokunin`):

```
TMPDIR=…/r47w2-ExecRerunC1v2 python3 tools/mori-pin-check.py \
  --rev 68d66ca53d89be5c34a62f46af7c37449d9f9b63 \
  --min-tally-pins 26 \
  --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
```

Result: **EXIT=0**, final line

```
PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 min_tally_pins=26 rev=68d66ca53d89be5c34a62f46af7c37449d9f9b63 baseline=yes
```

All 33 per-pin lines `state=match` (full output at scratch `rerun-T.txt`; the 28 tally pins
and 5 digest pins are the same pins as the receipt).

**Comparison with `evidence/after-c1-v2.txt`**: after normalizing only the revision token in the
transcript header, the two revision-bound commands (`conform.py` and
`mori-sources-appendonly.py` embed the measured rev), and the final `rev=` field, the rerun
output is byte-identical to the receipt (diff delta = receipt's `$ …` header line and trailing
`rc=0` wrapper only). `evidence/after-c1-v2.txt` was measured at `af2250d8`, and
`git diff --name-only af2250d8..T` lists only round-47 evidence files (no SKILL.md, no
tools/* change), so comparing the T-run against the af2250d8 receipt is valid.

## 3. --selftest vs registry row

Command: `python3 tools/mori-pin-check.py --selftest` → **EXIT=0**, final line
`PIN_CHECK_SELFTEST pass=34 fail=0` (32 PASS case lines + `cli_met_rc0` + `cli_bad_rev_rc2`
= 34 passes, 0 fails; full output at scratch `selftest.txt`).

SKILL.md at T line 938 (registry row "registry pin reconciler (r47, C1)") self-test cell:
`` `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=34 fail=0` `` —
the live run matches the row exactly. The rerun in §2 also independently observed this pin at
line 938: `pinned='pass=34 fail=0' observed='pass=34 fail=0' rc=0` — matches.

(Note: committed `evidence/selftest-pin-check.txt` is an older v1-era receipt reporting
`pass=22`; it predates v2's 34-case suite and is superseded by the current row pin, which the
live run reproduces.)

## 4. Independent cross-check: frozen-v1 scoring path at T

SKILL.md (T) records that the round-47 claim itself is scored with the frozen v1 bytes. Ran
`git show 63eecf27:tools/mori-pin-check.py` (sha256 `e3ef425a…`) with the same flags and
`--repo` at T: **EXIT=0**, `PIN_CHECK=met tally_pins=28 digest_pins=5 mismatches=0 unparsed=0
no_command=0 dropped=0 min_tally_pins=26 rev=68d66ca5… baseline=yes`. Byte-identical to
`evidence/after-c1-v1-frozen.txt` modulo the rev token and transcript wrapper.

## 5. Verdict

**HOLDS.** Nothing attacked broke:

- v2 (hardened, tracked) tool at T prints `PIN_CHECK=met` (exit 0) and reproduces the v2 receipt exactly (modulo rev token).
- `--selftest` prints `PIN_CHECK_SELFTEST pass=34 fail=0` (exit 0), matching the SKILL.md line-938 registry row.
- The frozen-v1 scoring path also prints `PIN_CHECK=met` at T, matching the v1 receipt.
- Tree equality `af2250d8`→T holds for every measured file (only evidence files differ), so the receipt comparison is sound.

Scratch: `.scratch/r47w2-ExecRerunC1v2/` (`rerun-T.txt`, `selftest.txt`,
`rerun-v1-frozen-T.txt`, `pin-check-frozen-v1.py`, normalized diff artifacts). The tool's own
exports under `<repo>/.scratch` are removed on exit (no `pin-tmp-*` leftovers). No tools
installed/updated.
