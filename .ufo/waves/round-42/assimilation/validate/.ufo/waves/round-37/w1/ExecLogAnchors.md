# ExecLogAnchors — round-37 LOG.md entry anchor audit

Target: every hash, path and command named in the LOG.md round-37 entry (lines 2139–2184 at
audit time) resolves to the claimed surface or reruns to the claimed output.

Attacks: the LOG entry's completion claim — that a reader can take each named artifact, open it or
run it, and land on the round's measured result. Not attacked: the truth of the predicates, the
soundness of the counters' arms (separate seats), axis attribution, or the wave accounting.

Repo state moved under this seat (lane is receiving commits live):
`0a05f7e` → `1ae1d6d` → `5631efa` → `4bfa049` → `e33bb56`. Every measurement below names the
revision it was taken at. Scratch: `/fast/scratch/hyaku/mori-r37/ExecLogAnchors/` (frozen v1
counters extracted there from `e57c58b5`). Lane bytes were never edited; no install, no pacman,
no network mutation.

## 1. Hash / digest anchors

| # | Anchor (LOG.md) | Claim | Check | Result |
|---|---|---|---|---|
| H1 | :2141 `842a3207` | entering tip | `git cat-file -t 842a3207` → `commit` | PASS |
| H2 | :2143 blob `7518fef8` / `6213cf9a` | v1 `count-c1.py` / `count-c2.py` frozen blobs | `git show e57c58b5:<path> > v1/count-*.py`; `git hash-object` → `7518fef8f54a…` / `6213cf9a5ada…`; both equal the pins recorded in `evidence/freeze-r37.txt` | PASS |
| H3 | :2143 sha256 `86699627` / `71c72929` | same bytes | `sha256sum` on the extracted v1 files → `86699627c762…` / `71c72929f9ac…` | PASS |
| H4 | :2147 `bf0df77` | r36 data commit used for the before-arms | `git cat-file -t bf0df77` → `commit` ("round-36: C1/C2 data — drift probe tool, append-only gate…") | PASS |
| H5 | :2149,2155 `e57c58b5` | scored tip | `git cat-file -t e57c58b5` → `commit` | PASS |
| H6 | :2152 `1caa242` | commit that landed the two fetch policies | `git log -S "FETCH_MAX_BYTES" -- tools/mori-source-drift.py` → only `1caa242`; `git show 1caa242:tools/mori-source-drift.py` → `FETCH_MAX_BYTES` ×3, `_public_redirect_target` ×2. Contrast the pre-correction value `8ff9bba`: same greps → `0` / `0`, i.e. it touches no tool byte | PASS (corrected value verified; see F3) |
| H7 | :2151 seed `13985344346805549517` | C1 replay seed | v1 counter at `e57c58b5` with this seed reproduces `c1-after.txt` byte-for-byte (see C1) | PASS |
| H8 | :2166 `52d636d5` | S225 copy landed by naming it explicitly, 1.9 MiB | `git show --stat 52d636d5` → 1 file, 18 915 insertions; `git ls-tree 52d636d5 corpus/evidence/sources-r37/` lists all five copies; `S225.src` = 1 854 393 bytes | PASS |
| H9 | :2171 `4bfa0490` | amendments measured tip | `git cat-file -t 4bfa0490` → `commit` | PASS |
| H10 | :2175 seed `20261024` | A1 C1 re-score | `count-c1.py e57c58b5 --seed 20261024` → `C1=met`, exit 0 (drawn arm passes; drawn rev differs from the receipt because it is drawn from `git rev-list HEAD`, which moved — disclosed in the receipt's `head_at_measurement:` line) | PASS |
| H11 | P-C1 body (rev `6bd57097`, base `f10a320d`) | real arm's rev/base | both `commit` | PASS |

## 2. Path anchors

All 30 named paths exist (`for p in …; do [ -e "$p" ]`): `contract.md`, `count-c1.py`,
`count-c2.py`, the three fixtures (`memo-n1.py`, `const.py`, `summary-only.py`), `freeze-r37.txt`,
`freeze-r37-v3.txt`, `c1-before-memo.txt`, `c1-before-summary.txt`, `c1-after.txt`,
`c1-after-v2.txt`, `c2-before.txt`, `c2-after.txt`, `c2-after-v3.txt`, `drift-live-r37.txt`,
`drift-live-r37-start.txt`, `census-start.txt`, `census-end.txt`, `census-rows.txt`,
`r17-jj-selftest-r37.txt`, `s225-copy.txt`, `corpus/knowledge/source-drift-hardening-r37.md`,
`corpus/lessons/round-37.md`, `corpus/lessons/round-36-verifier-spotcheck.md`,
`corpus/knowledge/source-drift-r36.md`, `tools/mori-source-drift.py`,
`tools/mori-sources-appendonly.py`, `tools/mori-round17-jj-regressions.py`, fleet
`scripts/sources-census.sh`. No missing path.

Content anchors behind those paths (all resolve): QUALITY 106/107 (`corpus/QUALITY.md:853,862`);
SCORECARD capability rows `real-arm challenge counter` / `source-drift re-fetch probe`
(`SCORECARD.md:2058-2059`) and the `Held:` line (`:2068`); SOURCES rows S221–S225
(`corpus/SOURCES.md:227-231`, cited by the knowledge entry, and `e57c58b` adds 7 lines / 0 deletions
→ "no existing row edited"); two SKILL.md Round-37 registry rows (`SKILL.md:877-878`); the nine-row
drift prose of debt (h) at `corpus/knowledge/source-drift-r36.md:24-33` (seven + S210 + S211).

## 3. Command anchors

### C1 — `count-c1.py e57c58b5` (LOG:2149)
Frozen v1 bytes (`/fast/scratch/.../v1/count-c1.py`, sha256 `86699627…`) with the LOG's seed:
`diff` against `evidence/c1-after.txt` is empty except the receipt's `command:` header line and
`EXIT=0` trailer. Output: `blind arm: 24/24 … real arm: pass … challenge arm (real-arm clothing):
pass … negative memo-n1.py rejected (challenge: …) / const.py rejected / summary-only.py rejected /
C1=met / seed=13985344346805549517`, `EXIT=0`. PASS.

Current (v3) file at the same rev: `C1=met`, exit 0, `blind arm: 24/24`, `real arm: pass`,
`drawn arm: pass`, challenge pass, three negatives rejected. PASS.

### C2-before — `count-c2.py 842a320` (LOG:2154)
v1 bytes: `diff` against `evidence/c2-before.txt` empty except `EXIT=1`; observed `selftest FAIL
(4 unnamed arms)`, `knowledge FAIL`, `capability FAIL`, `readme FAIL`, `live FAIL`, `C2=unmet`,
exit 1. v3 bytes: same verdict, `C2=unmet`, exit 1. PASS.

### C2-after — `count-c2.py e57c58b5` (LOG:2155)
v1 bytes: `diff` against `evidence/c2-after.txt` empty except `EXIT=0`; all eight checks PASS,
`C2=met`, exit 0. PASS for the bytes the entry's own freeze pins name.

Current (v3) bytes at `e57c58b5`: `check knowledge FAIL (present=True rows=[…] cited_commit=False
touches_tool=True)`, `check live FAIL (present=True sentence=False)`, `C2=unmet`, exit 1 — because
v3 requires the cited commit `1caa242` and a `sentence:` line that the pre-correction artifacts at
that rev do not carry. Re-scored at the amendment tip: `count-c2.py 4bfa049` → all eight PASS,
`C2=met`, exit 0, byte-identical to `evidence/c2-after-v3.txt` (except `EXIT=0`). See F2.

### Before-arms — `count-c2.py bf0df77 --tool fixtures/memo-n1.py --seed 11` (LOG:2147)
Literal form fails two ways:
- `python3 .ufo/waves/round-37/count-c2.py bf0df77 --tool fixtures/memo-n1.py --seed 11` →
  `count-c2.py: error: unrecognized arguments: --tool … --seed 11`, exit 2 (the round-37 counter has
  no such flags).
- `cd .ufo/waves/round-37 && python3 ../round-36/count-c2.py bf0df77 --tool fixtures/memo-n1.py
  --seed 11` → tool `exit 2`, "no summary line", `C2=unmet`, `EXIT=1` (the r36 counter runs the tool
  with `cwd="/"`, so a relative `--tool` never resolves — `run_tool(..., cwd="/")`,
  `.ufo/waves/round-36/count-c2.py:493-495`).

Receipt-recorded form (`evidence/c1-before-memo.txt:1`) with `<lane>` expanded to the absolute lane
root: `python3 .ufo/waves/round-36/count-c2.py bf0df77 --tool <lane>/.ufo/waves/round-37/fixtures/
memo-n1.py --seed 11` → `blind arm: 24/24 (coverage deletions=24 changed-back=16 superseded=12)`,
`real arm: pass`, `C2=met`, `seed=11`, `EXIT=0`; same with `summary-only.py --seed 12` →
`C2=met`, `EXIT=0`. Both match the receipts. So the measurement reproduces; the LOG's inline form
does not (F1).

### Live sweep — LOG:2157
`timeout 280 python3 tools/mori-source-drift.py --root .` at tip → `MORI_SOURCE_DRIFT rows=225
fresh=53 excerpt=0 drifted=10 unavailable=0 no-copy=162`, `EXIT=1`, 10.3 s. Matches
`evidence/drift-live-r37.txt` at HEAD exactly. The LOG's cited numbers (`rows=220 fresh=49
drifted=9 unavailable=0 no-copy=162`) are those of `evidence/drift-live-r37-start.txt`. See F1.

### Census — `sources-census.sh validate mori` (LOG:2159)
`cd /home/vgpnk/Projects/shokunin && bash scripts/sources-census.sh validate mori` → 15
`mori W04 duplicate url …` lines then `mori ok …/mori-shokunin/corpus/SOURCES.md`, `EXIT=0`.
`census-start.txt` and `census-end.txt` are byte-identical. Row total: the receipt's own command
re-run → `842a320: 220`, `5dff52a1: 225`, `HEAD: 225`. PASS.

### r17-jj selftest — LOG:2163
`python3 tools/mori-round17-jj-regressions.py --selftest --scratch .ufo/waves/round-37/scratch-r17`
→ `SELFTEST ok: …`, `EXIT=0` (the bare `--selftest` exits 2: `setup: selftest needs --scratch DIR
or TMPDIR (no /tmp fallback)` — so the receipt's recorded command is the runnable form). Its
`pre_fix:` line's citation checks out: `.ufo/waves/round-36/w2/ExecCensusRegression.md:227`
`assertions=204 failed=9`. PASS.

### Drift selftest (P-C2 content) — `tools/mori-source-drift.py --selftest`
`selftest exit_code/row_states/summary/huge_cap/redirect_private_refused/missing_sources_exit2
PASS` → `MORI_SOURCE_DRIFT_SELFTEST: PASS (6 cases)`, `EXIT=0`. PASS.

## 4. Findings

**F1 (FAIL, two anchors do not resolve as written).**
(a) `LOG.md:2157` pairs `rows=220 fresh=49 drifted=9 unavailable=0 no-copy=162` with
`evidence/drift-live-r37.txt`; that file holds `rows=225 fresh=53 excerpt=0 drifted=10 …`
(`git show HEAD:…/drift-live-r37.txt | tail -2`). The 220-row numbers live in
`evidence/drift-live-r37-start.txt`. The entry's own A2 (`LOG.md:2178-2179`) states the correct
pairing, so the declared line is stale but corrected in the same entry.
(b) `LOG.md:2147`'s before-arm command is not rerunnable: the round-37 counter rejects
`--tool/--seed` (exit 2) and the round-36 counter resolves `--tool` against `cwd="/"`, so the
relative `fixtures/memo-n1.py` fails (exit 1, `C2=unmet`). The receipts (`c1-before-memo.txt:1`,
`c1-before-summary.txt:1`) carry the runnable form with `<lane>/…`; expanded to absolute, both
reproduce `C2=met` exit 0 exactly.

**F2 (informational, version pin).** `LOG.md:2155`'s `count-c2.py e57c58b5 → C2=met exit 0`
reproduces only with the v1 counter bytes the entry pins (`71c72929…`). The current file at that
path is v3 (sha256 `f173a642…`) and prints `C2=unmet` at `e57c58b5` (`knowledge` `cited_commit=False`,
`live` `sentence=False`); v3's `C2=met` is at `4bfa049` — reproduced, byte-identical to
`c2-after-v3.txt`. The entry's amendments paragraph names `freeze-r37-v3.txt` and the re-score tip,
but the declared line keeps the v1 connotation without a version tag.

**F3 (resolved).** The commit misattribution the entry carried (`8ff9bba`) is corrected to
`1caa242` at `LOG.md:2152` and A3; verified by content, not by string match: only `1caa242` touches
the tool, and v3's `knowledge` check now requires `git_log_touches` (`touches_tool=True`).

**F4 (cosmetic).** `LOG.md:2166` says "lesson M1–M5"; `corpus/lessons/round-37.md` now carries
M1–M10 (M6–M10 added by wave-1 commits). M1–M5 all exist, so the named range resolves; the range is
simply narrower than the file.

## 5. Risks and limits

- The lane committed five times during this audit; line numbers above are against
  `HEAD=e33bb56`. Anchors verified at earlier tips (notably the `8ff9bba` attribution) are quoted
  with the tip they were read at.
- The live sweep is network-dependent: my rerun reproduced the tip receipt's counts exactly
  (225/53/10/0/162), but the drifted count is a moving live surface (S223's footer clock), so a
  later rerun may differ for reasons unrelated to the anchors.
- I did not re-derive any predicate's truth privately; C1/C2 verdicts are read from the counters'
  own oracle (separate seats own that question).
- `count-c1.py` writes its challenge scratch under `<lane>/.ufo/waves/round-37/scratch/` (counter
  design, `contract.md` challenge-arm clause); no lane file was edited by this seat.

VERDICT: FAIL — two named anchors do not resolve as written: `LOG.md:2157` (220-row live-sweep
numbers attributed to `evidence/drift-live-r37.txt`, which holds 225/53/10; they are in
`drift-live-r37-start.txt`) and `LOG.md:2147` (before-arm command not rerunnable as written; the
receipts' `<lane>/…` form reruns to `C2=met` exit 0). Every hash, path and measurement behind the
entry resolves; the two failures are documentary-form and both have their corrected form already
present in the same entry or its receipts.
