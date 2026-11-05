# Mo93K01Crit — round 93 attempt 1, wave w1 (critic, falsify the round)

Scope: falsify the frozen round-93 contract (`contract.md`, committed 6d82b8d7). Paths are relative to the lane root. Counters were run at the entering revision 7b3fe9d5 in scratch clone `/fast/scratch/hyaku/mori-r93/Mo93K01Crit/clone` (checkout 6d82b8d7; no commit made). Leaf seat, no subagents.

## 1. P3 — digest-gate debt and rule 2

**Verdict: dropping the digest-gate claim is correct. P3's reason holds on the rules. P3's premise is wrong in one count, and "cannot be closed honestly" should read "cannot be closed under rule 2, QUALITY 193 and 195 as written".**

(a) Rule 2 forbids the in-place completion. CORPUS.md (fleet root, quoted at `corpus/SOURCES.md:211`) says: "Only `status`, `recheck` and `used-by` change in place … A correction is a new row whose `teaches` opens `supersedes S0NN —`" (`/home/vgpnk/Projects/shokunin/CORPUS.md:116-118`). `anchor` is an immutable cell (`CORPUS.md:99-100`). The recorded digest sits in the anchor cell: S502 row, anchor `… sha256 bc178ff511e0; copy corpus/evidence/sources-r53/proc.rst.v7.3` (`corpus/SOURCES.md:281`). Completing it edits that cell. The lane's own gate says the same: `tools/mori-sources-appendonly.py:9-10` ("Only the columns status, recheck and used-by may change in place"), `:63-65` (`MUTABLE = ("status", "recheck", "used-by")`). Lane practice agrees: `corpus/SOURCES.md:430` ("Immutable anchor cells were not edited").

(b) The supersession exclusion is intended, but its reason is written nowhere.
- QUALITY 195: supersession "honoured only when … the target row classifies mismatch" (`corpus/QUALITY.md:2251`).
- QUALITY 193: "A prefix agreement is `prefix-only` and fails the gate" (`corpus/QUALITY.md:2245`).
- Tool docstring: "if and only if S<id> classifies mismatch" (`tools/mori-source-digest.py:27-29`); code `:81`, `:447-457`.
- Selftest arm "prefix-only row is not superseded" (`tools/mori-source-digest.py:516-520`) pins it.
- Measured: `python3 -I tools/mori-source-digest.py --selftest` → `DIGEST_SELFTEST pass=11 fail=0`, rc 0.

The reason is that supersession asserts the predecessor is *wrong*, and a prefix row is not wrong. Measured at 7b3fe9d5, every prefix-only row's recorded value is a prefix of the actual digest (`DIGEST S502 prefix-only recorded=bc178ff511e0 actual=bc178ff511e05c1b…`). The 31 red rows are therefore a completeness failure. No lawful route repays them: rule 2 forbids the in-place edit, QUALITY 195 forbids supersession. They are red by construction. P3 should say so; "this round" understates it.

(c) The lane already breaches rule 2 on anchors, and its gate is already red on it. `python3 -I tools/mori-sources-appendonly.py 7b3fe9d5 --repo .` → `appendonly_violations=50 ids=[S041,…,S502,…] deleted=[] … round_changed=[]`, same count at 6d82b8d7 (rc 1). The S502 anchor was changed in place in `0df80303` (round 53): `git show 2a4213bf:corpus/SOURCES.md` has `lines 1043-1240 …Committed_AS 1239`; now `lines 1043-1302 …Committed_AS 1239-1251`. P3 cites no gate; it should cite this one, and state that one more in-place digest completion would be the 51st flagged id, not a new kind of event.

(d) Premise error in P3 ("S125 unpinned", singular). Measured at the lane root:
`python3 -I tools/mori-source-digest.py corpus/SOURCES.md .` → `DIGEST_CHECK rows=122 ok=87 mismatch=0 superseded=2 prefix_only=31 unpinned=2`, rc 1. Unpinned = S125 and **S612**. S612's copy exists twice, byte-identical: `.ufo/waves/round-89/evidence/sources-r89/posix-shell-v3-chap02.html` and `.ufo/waves/round-90/w1/Mo90S01Sources/sources/posix-shell-v3-chap02.html` (both 357953 B, sha256 `0889867a…`, `cmp` IDENTICAL). The no-path resolver treats two candidates as ambiguous (`tools/mori-source-digest.py`, the `sized`/`targets` block near `:420-431`). The count depends on the pinned-dir argument:
- `.ufo/waves/round-90` → `ok=88 superseded=2 prefix_only=31 unpinned=1`
- `.ufo/waves/round-89` → `ok=87 superseded=1 prefix_only=31 unpinned=3`
- `.ufo/waves/round-90/w1` → `ok=88 superseded=2 prefix_only=31 unpinned=1`

Round 92's entering run reads S612 `ok` (`.ufo/waves/round-92/w1/Mo92E01Digest.entering-run.txt`), while `SCORECARD.md:4716` reports `unpinned=1`. The "unpinned" figure is a function of an unstated argument. QUALITY 196 exists for exactly this; P3 did not apply it to its own count.

**Decision:** drop is correct. Too cautious? No. Wrong? Only in the premise count and in calling the closure "this round" rather than "under the rules".

## 2. C2 — operability or portability cosmetic?

Classification of the 12 `vgpnk` lines (`git grep -n vgpnk -- tools` at 7b3fe9d5), by hand:

| File:line | Use | Class |
|---|---|---|
| `tools/mori-blind-check.sh:247` | selftest allow-list fixture (quoted heredoc) | fixture |
| `tools/mori-misroot-sweep.py:6,20,355` | docstring / comment; the code takes `fleet_root` as an argument (`:107-109`, `:223`) | prose |
| `tools/mori-round17-context-check.py:39,116` | comments | prose |
| `tools/mori-round17-context-check.py:118` | `_FLEET_ROOT = "/home/vgpnk/Projects/shokunin"`, used by validator regexes `:261-270` | **functional** |
| `tools/mori-round17-context-check.py:508,535,557,559,565` | string literals of seat-context templates | **functional** (rendered text) |

So 6 of 12 lines are functional, all in one tool. Entering status: `C2=unmet home_literals=18 vgpnk_refs=18 tools=3 selftests=3/3 census=ok` (`count-c2.py 7b3fe9d5`, rc 1, reproduced). Every selftest already passes on this host, so nothing that runs here breaks.

**Decision:** a real operability move, narrow. It is one tool's validator and seat text. Otherwise it is portability cosmetic. The predicate is a static grep and cannot separate the two classes. Two further points:
- The repair fallback `$HOME/Projects/shokunin` (`contract.md:80-82`) re-encodes the same layout under a variable. The named limit (`contract.md:92-93`) covers concatenation, so `home_literals=0` passes it. On a host without that layout the repair shape does not require a loud failure (inference from the shape; not measured).
- The equivalence receipt (`evidence/equivalence-c2.txt`) is taken on this host, where the derived value equals the literal by construction. It cannot show operability elsewhere.

**Outside verifier needs:** (i) a clean clone run with `env -u SHOKUNIN_ROOT HOME=<dir without Projects/shokunin>`: each tool's `--selftest` and `--help` stdout byte-equal to the entering host's; (ii) `SHOKUNIN_ROOT=<other root>` run of `mori-round17-context-check.py`: rendered text and validator follow that root, not the constant; (iii) neither variable set on such a host: the tool must fail loudly, not render a wrong root; (iv) the 12-line manual classification above, committed beside the receipt.

## 3. Shape against the SCORECARD planned list (rounds 90–92)

Axis rule (`AXES.md:25-37`): one claim on a lowest non-retired axis. Calibration 5 is one of three tied lowest (calibration, freshness, depth). The rule is met. Two distinct axes is admissible. C2 on operability (7) need not be lowest.

Omissions:
- P4 (`contract.md:30-33`) drops freshness on one reading only: no recheck cadence is due. The planned freshness items are not discussed:
  - round 92 #2, re-declare the C2 digest gate (`SCORECARD.md:4701-4708`): unmet at round 92 (`SCORECARD.md:4716`), not re-declared here;
  - round 91 #3, dated census snapshot for the r86 value channel (`SCORECARD.md:4672-4673`), carried since round 86;
  - round 90 #3, F3 hermeticity (`SCORECARD.md:4592-4611`).
- The same census item is labelled **depth** at `SCORECARD.md:4553-4554` and `:4610-4611` and **freshness** at `:4672-4673`. Nobody owes it cleanly.
- Depth items: round 92 #5 landed as S619 (`corpus/SOURCES.md`, round 92). Round 92 #3, the arm-pin record, names `w1/candidates/pins.txt`; the file is at `.ufo/waves/round-91/w1/candidates/pins.txt`, not round 87.
- Coverage: S622 and S623 are not registered at 7b3fe9d5 (`grep -c '^| S62[23] '` → 0; max id S621). That is consistent with "opened this round" (`contract.md:63`), but the counter does not check it.

**Third claim, cheapest honest one: freshness, digest-resolution invariance.** Predicate: at the lane root `unpinned` equals S125 only, and identical across the three pinned-dir scopes above. Cost: one resolver change (identical-byte candidates count as one), one selftest arm, three runs; no registry row touched. Caveat: it needs a new QUALITY row, because QUALITY 193/195 and the tool docstring define ambiguity as `unpinned`; without that row it is a rule edit by code. It also moves S612 `unpinned → ok`, which is the green-ward move round 92's Mistake 2 warns about. It must be reported as a resolver change, not as debt repaid (the 31 prefix rows are untouched).

Alternatives: the arm-pin record is cheap but is "traceability metadata, not depth" by round 92's own critic note (`SCORECARD.md:4716`). The census snapshot is freshness and real but needs a dated live run and has been carried six rounds.

## 4. The one element a non-author accepts on trust

C1 is presence-only: "a fenced or empty value passes it, so the truth of each line is a non-author check" (`corpus/QUALITY.md:2249`, QUALITY 194). The admission-hash half is checkable, and I checked it: every `corpus/knowledge` and `corpus/lessons` file at 7b3fe9d5 has exactly one `git log --diff-filter=A` commit (a loop over `git ls-tree` printed nothing), so `tail -1` is unambiguous for this population. The half that is not checked is the untouched original `verified-at` text on the 12 repaired lines (dates and round labels, e.g. `2026-11-02 (round 78; …)`). The contract's "the value gains the admission commit" (`contract.md:52-55`) assumes those originals are true, and no step re-opens them.

## Checks

Run (entering 7b3fe9d5 unless noted):
- `count-c1.py 7b3fe9d5 --repo <clone> --report` → `C1_REPORT … adm_ok=7 adm_fail=12 patched12=0/12 seven_same=7/7 census_rc=0`, rc 0 (reproduces contract).
- `count-c2.py 7b3fe9d5 --repo <clone>` → `C2=unmet home_literals=18 vgpnk_refs=18 tools=3 selftests=3/3 census=ok`, rc 1 (reproduces).
- `count-c2.py 6d82b8d7 --repo <clone>` → same, rc 1 (the wave landing is not in the lane; C2 is unmet at 6d82b8d7 as expected).
- `mori-source-digest.py corpus/SOURCES.md .` → `unpinned=2`, rc 1. Pinned-dir variants as quoted in §1(d).
- `mori-source-digest.py --selftest` → `pass=11 fail=0`, rc 0.
- `mori-sources-appendonly.py 6d82b8d7 --repo .` → `appendonly_violations=50`, rc 1. `--selftest` → `pass=22 fail=0`, rc 0.
- `git log --diff-filter=A` admission uniqueness, all knowledge and lesson files: no file with count ≠ 1.
- `sha256sum` and `cmp` on the two S612 copies: identical.

Not run: the in-place completion fixture (requires a commit; seats must not commit); the C2 tools on any non-author host (no such host available to this seat); the wave's landed patches (not yet integrated).

Report: .ufo/waves/round-93/w1/Mo93K01Crit.md
