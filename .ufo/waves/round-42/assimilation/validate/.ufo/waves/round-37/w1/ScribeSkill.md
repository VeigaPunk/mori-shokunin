# Draft Round-37 SKILL.md registry rows

## Behavior

Drafted two rows using the Round-36 eight-column schema (`name | kind | entry | verdict map | self-test | pinned values | write scope | owner`). Every cell cites a command or path confirmed in the `e57c58b57c025364e79d130fbdf764d2674d83d6` tree. This is report-only; `SKILL.md` was not edited.

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| source drift (r37) [`SKILL.md`] | probe [`tools/mori-source-drift.py`] | `python3 tools/mori-source-drift.py --root <repo>` [`tools/mori-source-drift.py`] | 0: no `drifted` rows; 1: one or more `drifted`; 2: could not evaluate; over-cap and refused redirect are `unavailable`, not `drifted` [`corpus/knowledge/source-drift-hardening-r37.md`] | `python3 tools/mori-source-drift.py --selftest`; named arms `huge_cap` and `redirect_private_refused` [`tools/mori-source-drift.py`, `.ufo/waves/round-37/count-c2.py`] | 4 MiB read limit (`FETCH_MAX_BYTES + 1` read); check the final redirect destination for a public HTTP(S) target [`tools/mori-source-drift.py`, `corpus/knowledge/source-drift-hardening-r37.md`] | No repository writes; live mode fetches URLs; self-test uses a temporary fixture [`tools/mori-source-drift.py`] | mori [`SKILL.md`] |
| SOURCES append-only discrimination (r37) [`SKILL.md`, `.ufo/waves/round-37/contract.md`] | counter [`.ufo/waves/round-37/count-c1.py`] | `python3 .ufo/waves/round-37/count-c1.py <rev>`; by default evaluates the committed `tools/mori-sources-appendonly.py` at `<rev>` [`.ufo/waves/round-37/count-c1.py`, `tools/mori-sources-appendonly.py`] | 0: `C1=met`; 1: `C1=unmet`; 2: setup error; timeout is scored unmet-by-timeout, not a list mismatch [`.ufo/waves/round-37/count-c1.py`] | No separate `--selftest`; scored arms are 24 run-time sandbox histories, the lane history, one real-arm-clothing challenge, and rejection of `memo-n1.py`, `const.py`, and `summary-only.py` [`.ufo/waves/round-37/count-c1.py`, `.ufo/waves/round-37/contract.md`] | Lane arm pins: `REAL_REV=6bd57097`, `REAL_BASE=f10a320d`, 24 blind histories; per-id `changed`/`deleted` lines as well as all four lists are compared [`.ufo/waves/round-37/count-c1.py`, `.ufo/waves/round-37/contract.md`] | Read-only git for the real arm; unique temp scratch for blind/negative arms; the challenge creates and removes a `mkdtemp` under `<repo>/.ufo/waves/round-37/scratch/` [`.ufo/waves/round-37/count-c1.py`] | mori [`SKILL.md`] |

## Gates and observed measurements

These are transcribed from the available receipts; I did not re-run the counters or probe.

- `python3 .ufo/waves/round-37/count-c1.py e57c58b57c025364e79d130fbdf764d2674d83d6` → receipt reports `C1=met`, `EXIT=0`, seed `13985344346805549517`; blind `24/24`, real arm pass, challenge arm pass, and all three negatives rejected (`.ufo/waves/round-37/evidence/c1-after.txt`). The real-arm output and oracle agree: `appendonly_violations=18`, deleted `[]`, superseded `[S069,S182,S193]`, `round_changed=[S182,S193]`.
- `python3 .ufo/waves/round-37/count-c2.py e57c58b57c025364e79d130fbdf764d2674d83d6` → receipt reports `C2=met`, `EXIT=0`; all eight checks pass, including the six-case selftest, both mutation kills, knowledge/capability/README bindings, and live receipt presence (`.ufo/waves/round-37/evidence/c2-after.txt`).
- C1 shortcut controls in the frozen contract: `count-c2.py bf0df77 --tool fixtures/memo-n1.py --seed 11` and `count-c2.py bf0df77 --tool fixtures/summary-only.py --seed 12` each report `C2=met`, exit 0 (`.ufo/waves/round-37/evidence/c1-before-memo.txt`, `c1-before-summary.txt`). These show the old counter accepting the negatives; they are not C1 pass evidence.
- C2 entering-tip control: `python3 .ufo/waves/round-37/count-c2.py 842a320` → `C2=unmet`, `EXIT=1` (`.ufo/waves/round-37/evidence/c2-before.txt`).
- `python3 tools/mori-source-drift.py --root .` → `MORI_SOURCE_DRIFT rows=220 fresh=49 excerpt=0 drifted=9 unavailable=0 no-copy=162`, exit 1 (`.ufo/waves/round-37/evidence/drift-live-r37.txt`). This is a byte-reproducibility result, not a finding that the taught source claims changed.

## Provenance and known limits

- The registry schema and all drafted row citations point to paths/commands present at the scored tip. Read-only `git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -e e57c58b57c025364e79d130fbdf764d2674d83d6:<path>` checks confirmed the counter scripts, drift tool, append-only tool, knowledge entry, `corpus/README.md`, `SCORECARD.md`, contract, and `SKILL.md` exist there.
- The `c1-after.txt` and `c2-after.txt` receipts were readable in the working tree but are **not** in the e57 tree. Each exact `cat-file -e` check returned exit 128 with `fatal: path '…' exists on disk, but not in 'e57c58b57c025364e79d130fbdf764d2674d83d6'`. Therefore the post-run outcomes above are local-receipt observations, not receipt artifacts pinned by e57. The table deliberately cites the commit-present commands and source paths instead.
- C2's disclosed limits remain: only the final redirect destination is checked; DNS-resolved private addresses are not rechecked; over-cap and refused-redirect cases are `unavailable`, not classified as drift (`corpus/knowledge/source-drift-hardening-r37.md`).
- No tool was installed. No code, counter, gate, judge, commit, or `SKILL.md` was modified; no measurement was re-executed.

## Touched surfaces, out of scope, and artifact

- Touched: `.ufo/waves/round-37/w1/ScribeSkill.md` only.
- Out of scope: editing `SKILL.md`, remediation, running tests/counters, and committing or publishing.
- Artifact: `.ufo/waves/round-37/w1/ScribeSkill.md`.

VERDICT: PASS