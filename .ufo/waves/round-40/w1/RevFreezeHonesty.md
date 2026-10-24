# RevFreezeHonesty — freeze-r40.txt honesty and coverage

Working directory for every command: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Scope: `.ufo/waves/round-40/evidence/freeze-r40.txt` (read-only seat; no production
edits). Reviewer of record for this seat only; this is a recommendation, not an
admission.

## Bottom line

1. **Disclosure: PARTIAL.** The note truthfully says the prior launch died before
   persisting the receipt and names the resuming L1 as the pinner, but it never
   states the integration persistence point and never states that the pin
   post-dates the before receipts. `corpus/lessons/round-40.md:23` (M23) describes
   the note as containing "an honest note that it was written at integration" —
   that sentence is not in the note.
2. **Coverage: INCOMPLETE in exactly one contract-frozen class.** The contract
   froze "the fixture builders **and the survivor-fixture payloads**"
   (`contract.md:5-8`); the receipt pins the two builders but none of the ten
   `fixtures/generated/survivor-*.py` payloads. All nine digests that *are*
   recorded verify against the scored tip and the entering tip.
3. **Mitigation holds for the omission**: the ten payloads are byte-reproducible
   from the two pinned inputs (`count-c8.py` + `make-survivor-fixtures.py`) and
   equal the blobs committed at `265a955`, so an auditor can still verify them —
   but not from the freeze receipt itself.

## Findings

### F1 (MEDIUM) — the note omits the integration persistence point; M23 claims it is there

`evidence/freeze-r40.txt:1-5` (verbatim):

```text
freeze-r40: sha256 over the round-40 frozen instrument paths
pinned: 2026-10-24T05:46:06Z by L1 mori-r40 attempt 1 (resumed)
note: the prior launch died before persisting this receipt; before-receipts
      run committed bytes extracted via 'git show bb1f2457:<path>' (see
      fixtures/extracted/), so before-controls are measured at entering bytes.
```

What it discloses: the prior launch did not persist the receipt; the resuming L1
("L1 mori-r40 attempt 1 (resumed)") pinned it; before-controls ran extracted
entering bytes. What the required disclosure ("persisted at integration by the
resuming L1, not before data") needs and the note does not say: the persistence
point (integration commit `8d3badd`) and the ordering against the before receipts.

Verified timeline (mtimes of production-time files; all UTC):

| event | witness | time |
|---|---|---|
| before receipts (16 files: 12 `c10-red-*`/`c10-parity`, 4 `c11-*`) | `stat` | 05:41:05Z – 05:45:53Z |
| **freeze receipt written** | `stat` + `date -u -d @%Y`; equals the `pinned:` field to the second | **05:46:06Z** |
| after receipts | `stat` | 05:47:46Z – 05:50:14Z (census-end 05:50:28Z) |
| instruments commit | `git show -s --format='%h %cI %p %s'` (E4) | 05:47:29Z |
| **freeze receipt first in history** | `git log --all -- <path>` | **05:56:11Z** (`8d3badd`, parent `265a955`) |

So the pin was written *after every before receipt* and *before every after
receipt*, and it entered history only in the integration commit. The note's
"prior launch died before persisting" is true, but a reader cannot derive "not
before data" from the receipt set because the receipts themselves carry no
timestamps; only uncommitted mtimes show the 13-second gap to the last before
receipt (05:45:53Z → 05:46:06Z).

M23 (`corpus/lessons/round-40.md:23`) states the L1 "persisted
`evidence/freeze-r40.txt` with sha256 pins plus an honest note that it was
written at integration". The note does not contain that statement, and the file
write time is 10m05s before the integration commit (it was *committed* at
integration). Either the note is missing the required sentence or M23 overstates
it; both are disclosure defects, neither is a false statement inside the note.

`contract.md:5` compounds this: "Frozen before any data seat or data receipt: …"
is stated without qualification, while the receipt of pins post-dates all 16
before receipts.

Recommendation: add one sentence (or an append-only erratum) naming `8d3badd`
(02:56:11 -0300 / 05:56:11Z), the 05:46:06Z write, the fact that all 16 before
receipts precede the pin, and that the pinned bytes equal the `265a955` blobs;
then correct M23's description of the note.

### F2 (MEDIUM) — contract-frozen survivor payloads are absent from the sha256 set

`contract.md:5-8` (verbatim):

> Frozen before any data seat or data receipt: this contract, `count-c8.py`
> (the round-40 counter bytes), `conform.py` (round-40 version, v3), the
> modified `tools/mori-sources-appendonly.py` (the tracked gate, version 3),
> the fixture builders and the survivor-fixture payloads. Pins are recorded in
> `evidence/freeze-r40.txt` (sha256 over the frozen paths).

Coverage against the contract's frozen list:

| contract-frozen path / class | pinned in freeze-r40.txt? |
|---|---|
| `.ufo/waves/round-40/contract.md` | yes |
| `.ufo/waves/round-40/count-c8.py` | yes |
| `.ufo/waves/round-40/conform.py` | yes |
| `tools/mori-sources-appendonly.py` | yes |
| builder `fixtures/make-survivor-fixtures.py` | yes |
| builder `fixtures/run-c11-dags.py` | yes |
| `fixtures/generated/survivor-*.py` (10 payloads) | **no** |
| (not contract-required) three extracted v2 copies | yes (bonus) |

The receipt pins the two builders but no payload. Ten payloads are unpinned
(sha256 from the worktree, all equal to the `265a955` blobs — commands E10–E12):

| unpinned payload | sha256 |
|---|---|
| `fixtures/generated/survivor-barecomm.py` | `ccff0e7533faa16f3d734f075ae59978174256738ab99d0ebadf19ed01853d08` |
| `fixtures/generated/survivor-cond.py` | `5b4212e134530623694da431362e11dbd7c9dd7edd32d6323b2a1886b089ca69` |
| `fixtures/generated/survivor-decoy.py` | `cfdb030cee30b50ddd374195b75b0e0f8a3034a27aab57d44f0e234ed08cfc0e` |
| `fixtures/generated/survivor-divzero.py` | `128b8324d507f395658efa3478a9c5c24b5ffbcacdce6555235a37e0d0bd9d22` |
| `fixtures/generated/survivor-inf.py` | `dfbb4cc47e5df8d30fdf2f363ede56ec77cd9a2402b1d36bd7d881283f917e0f` |
| `fixtures/generated/survivor-second-popen.py` | `059e19d493d31e695e85de58a15d77b776fde4e45eb3b2531b31fb198b2cc9e9` |
| `fixtures/generated/survivor-shadow-neg.py` | `18f2ae199960d2726cfcaa04c003db56a1be6b61f37643e8ddd8845f17429b4e` |
| `fixtures/generated/survivor-shadow-none.py` | `1822b222170b91b9d32249b4420b713c7f89ee3420131949e8ed76f2160cc084` |
| `fixtures/generated/survivor-tuple.py` | `f74ce7f79eff88ef63f59baaa91f3d332451ab694b1a841a604ffc6c2af0bea5` |
| `fixtures/generated/survivor-underscore.py` | `8995d600f55c6ee725d20951b5a0f6ed7cbe155618e02fe90994bed058b9b24d` |

Why it matters: every survivor receipt (red and after) names its payload path
and records no payload hash (e.g. `evidence/c10-red-shadow-none.txt:1`,
`evidence/c10-after-shadow-none.txt:1`). A payload swap that preserves the printed
verdict text would pass the freeze's tamper check. The header line "sha256 over
the round-40 frozen instrument paths" therefore overclaims: it covers the listed
nine paths, not the frozen set named by the contract.

Mitigation verified: regenerating from the two pinned inputs reproduces all ten
payloads byte-for-byte (command E11), and their worktree bytes equal the
`265a955` blobs (E12). Recommendation: append the ten digests above (or an
erratum) so the receipt's claim matches `contract.md:5-8`.

### F3 (LOW) — two C11 before receipts predate the final fixture-builder bytes, and the note's "committed bytes" sentence does not cover the builder dependency

`run-c11-dags.py` builds the DAG fixtures by importing the **lane** gate module
(`load_gate(lane)`, `run-c11-dags.py:24-30`) and then runs the extracted v2 script
under test. At the time `c11-red-neveredited` and `c11-red-firstparent` ran
(05:41:05Z), `tools/mori-sources-appendonly.py` was not its final byte
(`stat` mtime 05:42:28Z, i.e. 83s later; the 02:42:28 local edit is the
completion M23 describes as "gate selftest arms 12→15; dag-r redesign"). No copy
of the builder-at-05:41:05Z exists in history: the nearest jj-kept snapshot,
`e104694` (parent `bb1f2457`, 02:24:03 local / 05:24:03Z, gate blob
`91b6134ce903dd8c92e7b9db0601d92431edf51fe29ba299aab102388d5b58d8`), supports only
the round-39 `dag-a`/`dag-c`/`dag-d` cases (grep output E15) — it cannot build
`dag-n`/`dag-p` at all — and the next recorded gate blob is the final
`bde5a9a3…` at 05:47:29Z. So the dag-n/dag-p builder used at 05:41:05Z is an
unrecorded intermediate; its fixture bodies cannot be proven identical from git
alone. The note's blanket "before-receipts run committed bytes extracted via
`git show bb1f2457`" is true of the *script under test* but not of the *fixture
builder* those two receipts also executed (the lane module was uncommitted and
not yet at its final bytes at that moment).

Mitigation verified: I re-derived all three before DAG receipts with the frozen
builder plus the extracted v2 bytes; the receipt bodies are identical with the
`command:` line stripped (command E14), and all six DAG receipts record the same
`--round-base b0=07be6c7f1765`. The printed before-controls are therefore
reproducible from frozen bytes; only fixture commit identities beyond `b0` are
unrecorded.

### F4 (LOW) — the gutted-conjunct control fixtures are unpinned and the v3 copy entered history after its receipt

The contract's freeze sentence does not name the two gutted-checker controls, and
the freeze receipt does not pin them, yet `c10-red-conjunct.txt` and
`c10-after-conjunct.txt` execute them and record no hash:

- `fixtures/generated/conform-r39-conjunct-gutted.py` — sha256
  `c9f01206e2f3d5d8191ee830af8bd0720567016b46f0d0afdaf2f4f9caf375b9`, first
  branch commit `265a955` (05:47:29Z, after the 05:45:24Z receipt); jj-keep
  snapshots `2a5d94e`/`c2ecbbc` (02:47:29 local) hold identical content.
- `fixtures/generated/conform-v3-conjunct-gutted.py` — sha256
  `20e324228735d39ad6bb293aac9dfd4b3a27a009a0f2ecf222731771bd2aaabf`, first
  history entry `ede486b` (05:56:56Z, 6m42s after the 05:50:14Z receipt; jj-keep
  `614ca03` same content); absent at `8d3badd` (`git show` yields empty bytes).

Both are exact derivations of pinned bytes, which I verified: the v3 copy is
`conform.py` minus the single line `        CONJUNCT_MUTATION,` (diff `734d733`);
the r39 copy is the extracted v2 minus the 4-line `("selftest_conjunct", …)`
tuple (diff lines 451-454). So the risk is evidentiary, not a byte mystery.
Recommendation: name them as derived in the receipt (with the derivation) or pin
their digests.

## Verified clean

- **All nine recorded digests verify.** `sha256sum -c` over the receipt's own
  lines: 9/9 `OK`. Independently, `git show 265a955:<path> | sha256sum` equals the
  recorded digest for all 6 round-40 paths (E2), and `git show
  bb1f2457:<original path> | sha256sum` equals the recorded digest for all 3
  extracted copies (E3: `.ufo/waves/round-39/conform.py`, `.ufo/waves/round-39/count-c7.py`,
  `tools/mori-sources-appendonly.py` at `bb1f2457`).
- **Committed bytes match the worktree and first enter history at integration.**
  Worktree content is byte-identical to `8d3badd:…/freeze-r40.txt` (diff empty);
  the path is absent at `265a955`; the jj-kept duplicate `fab8eee` (same parent,
  same timestamp, only `corpus/SOURCES.md` differs) carries the same blob
  `4f439d99c3e39e9785a7201fc33dad2e2513b2bc`.
- **"P-C10 contract==checker PREDICATE: True" holds**; P-C11 does too. AST-extracted
  `PREDICATE` strings equal the contract blockquotes exactly once the label
  prefix (`P-C10: ` / `P-C11: `, which my regex capture had stripped) is added
  back: P-C10 1557 chars, P-C11 1029 chars, with whitespace normalised and the
  only `SequenceMatcher` delta being that 7-character prefix.
- **Payload reproducibility and tip equality** (E11, E12).
- **Before-DAG receipt reproducibility** from frozen bytes (E14).

## Residual risk and verification gaps

- Ordering evidence is mtime-based and uncommitted. During wave 1, executor seats
  rewrote three evidence files in the worktree: `c10-red-conjunct.txt`,
  `c10-after-selftest.txt` (03:01-03:02 local) and `c10-after-conjunct.txt`; their
  verdict bodies are unchanged but their mtimes are no longer production times.
  My timeline uses the snapshot taken before those rewrites; the committed
  reference remains `8d3badd`.
- The frozen contract's P-C11 parenthetical says "(19 ids)" while the measured
  lane line at `265a955` is 34 as-of ids. Disclosed in M24 and the SCORECARD
  correction; it is a claim-text defect inside the frozen bytes, not a
  freeze-execution defect, and it is outside this seat's finding scope.
- No `lsp` device is exposed in this session (tools available: read/bash/edit/
  eval/glob/grep/task/wait/web_search/write/yield), and this review is over a text
  receipt plus git objects; git hashes and diffs are the evidence of record, and
  no grep output is presented as semantic proof.
- I did not re-run the C10 after-receipts, the lane line, or the selftests (peers'
  items); this report is scoped to the freeze receipt and its coverage.

## Exact commands and key outputs

All commands run in `/home/vgpnk/Projects/shokunin/mori-shokunin`.

E1 — receipt read (19 lines, 1447 bytes), note quoted above:

```text
$ read .ufo/waves/round-40/evidence/freeze-r40.txt   # 19 lines, 1447 bytes
$ wc -l -c .ufo/waves/round-40/evidence/freeze-r40.txt
  19 1447 .ufo/waves/round-40/evidence/freeze-r40.txt
```

E2 — recorded digests against the worktree and the scored tip:

```text
$ awk '/^[0-9a-f]{64}  /{print}' .ufo/waves/round-40/evidence/freeze-r40.txt | sha256sum -c -
.ufo/waves/round-40/contract.md: OK
.ufo/waves/round-40/count-c8.py: OK
.ufo/waves/round-40/conform.py: OK
tools/mori-sources-appendonly.py: OK
.ufo/waves/round-40/fixtures/make-survivor-fixtures.py: OK
.ufo/waves/round-40/fixtures/run-c11-dags.py: OK
.ufo/waves/round-40/fixtures/extracted/conform-v2-r39.py: OK
.ufo/waves/round-40/fixtures/extracted/count-c7-r39.py: OK
.ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py: OK
$ for p in .ufo/waves/round-40/contract.md .ufo/waves/round-40/count-c8.py .ufo/waves/round-40/conform.py tools/mori-sources-appendonly.py .ufo/waves/round-40/fixtures/make-survivor-fixtures.py .ufo/waves/round-40/fixtures/run-c11-dags.py; do printf '%s  ' "$p"; git show 265a955:$p | sha256sum | cut -d' ' -f1; done
.ufo/waves/round-40/contract.md  6514914885e6a1249ed7903931b9734a55e828275121353c2727348eae504a8d
.ufo/waves/round-40/count-c8.py  4e4d50eb1e96d947f0e9d2ab25a13b2b8c33963f216f3be43060a3348702f6da
.ufo/waves/round-40/conform.py  5025b9664632d01063c11b4f5dadd4f9a063db66d73315d7ed25db8d90b83aaf
tools/mori-sources-appendonly.py  bde5a9a34c7eb3bcbee39d669b8d187caeb51807ad1bdcd85a05c1bcd06777ec
.ufo/waves/round-40/fixtures/make-survivor-fixtures.py  8ff91db744c684f7b9b5c1d84e63538602635c52214a2b802afc520e4933acea
.ufo/waves/round-40/fixtures/run-c11-dags.py  0cd7f1d23c88db501288cad7ac4381a44d855aaf79f16dd1be1cda6d71f156da
```

E3 — extracted copies equal the `bb1f2457` originals:

```text
$ for p in .ufo/waves/round-39/conform.py .ufo/waves/round-39/count-c7.py tools/mori-sources-appendonly.py; do git show bb1f2457:$p | sha256sum; done
fe0be179aba9df7150f0b6cdb50a5f9bbdb411efb1263b46ffa6b21d46ef7987  -
b92c65f224a6268a901aa6bc5ad66b499048eaca82b493356eb8e1f324ef0520  -
62cd4132dbe141538371f79723c3caff66670fab9076494cd9cf65efccfc01e7  -
```

E4 — the receipt's history:

```text
$ git log --all --oneline -- .ufo/waves/round-40/evidence/freeze-r40.txt
8d3badd round-40: evidence receipts, wave spec (66-seat v2, validated), SCORECARD/LOG/lesson
fab8eee
$ git cat-file -e 265a955:.ufo/waves/round-40/evidence/freeze-r40.txt
fatal: path '…freeze-r40.txt' exists on disk, but not in '265a955'
$ git rev-parse fab8eee:.ufo/waves/round-40/evidence/freeze-r40.txt 8d3badd:.ufo/waves/round-40/evidence/freeze-r40.txt
4f439d99c3e39e9785a7201fc33dad2e2513b2bc
4f439d99c3e39e9785a7201fc33dad2e2513b2bc
$ git show -s --format='%h %cI %p %s' 8d3badd 265a955 ede486b
8d3badd 2026-10-24T02:56:11-03:00 265a955 round-40: evidence receipts, wave spec …
265a955 2026-10-24T02:47:29-03:00 bb1f245 round-40: instruments — conform v3 (P-C10), gate v3 (P-C11), S229, r39 erratum
ede486b 2026-10-24T02:56:56-03:00 8d3badd round-40: repair S229 registry placement … + commit referenced gutted-conjunct fixture
```

E5 — mtimes (production times), exact commands and outputs (excerpt of the full
`stat` output; the ellipsis marks omitted receipt lines, not edited values):

```text
$ stat -c '%y %n' .ufo/waves/round-40/evidence/freeze-r40.txt .ufo/waves/round-40/evidence/*.txt | sort | sed -n '1,80p'
2026-10-24 02:41:05.157847329 -0300 .ufo/waves/round-40/evidence/c11-before-lane.txt
2026-10-24 02:41:05.233896194 -0300 .ufo/waves/round-40/evidence/c11-red-neveredited.txt
2026-10-24 02:41:05.314909327 -0300 .ufo/waves/round-40/evidence/c11-red-firstparent.txt
2026-10-24 02:41:19.998897063 -0300 .ufo/waves/round-40/evidence/c10-red-shadow-none.txt
… (9 more c10-red survivor/multicounter receipts, 02:41:23–02:41:45; c11-red-readd 02:42:33)
2026-10-24 02:45:24.748813534 -0300 .ufo/waves/round-40/evidence/c10-red-conjunct.txt
2026-10-24 02:45:53.496994201 -0300 .ufo/waves/round-40/evidence/c10-parity.txt
2026-10-24 02:46:06.112968810 -0300 .ufo/waves/round-40/evidence/freeze-r40.txt
2026-10-24 02:47:46.821939302 -0300 .ufo/waves/round-40/evidence/c10-after.txt
2026-10-24 02:49:20.561627438 -0300 .ufo/waves/round-40/evidence/c10-after-selftest.txt
$ stat -c '%y %n' tools/mori-sources-appendonly.py .ufo/waves/round-40/fixtures/extracted/*.py .ufo/waves/round-40/fixtures/generated/survivor-shadow-none.py
2026-10-24 02:42:28.086151564 -0300 tools/mori-sources-appendonly.py
2026-10-24 02:40:45.329767633 -0300 .ufo/waves/round-40/fixtures/extracted/conform-v2-r39.py
2026-10-24 02:40:45.330767637 -0300 .ufo/waves/round-40/fixtures/extracted/count-c7-r39.py
2026-10-24 02:40:45.327767626 -0300 .ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py
2026-10-24 02:40:52.865728718 -0300 .ufo/waves/round-40/fixtures/generated/survivor-shadow-none.py
$ date -u -d @$(stat -c %Y .ufo/waves/round-40/evidence/freeze-r40.txt) +%Y-%m-%dT%H:%M:%SZ
2026-10-24T05:46:06Z
```

UTC mtimes (converted with the same `date -u -d @…` form, in a loop):

```text
freeze-r40.txt                 05:46:06Z   (local 02:46:06.112 -0300; matches `pinned:`)
c11-red-neveredited.txt        05:41:05Z
c11-red-firstparent.txt        05:41:05Z
c11-red-readd.txt              05:42:33Z
c10-parity.txt                 05:45:53Z
c10-red-conjunct.txt           05:45:24Z   (original; peer rewrite 03:01:55 local)
c10-after.txt                  05:47:46Z
c10-after-selftest.txt         05:49:20Z   (original; peer rewrite 03:02:20 local)
tools/mori-sources-appendonly.py 05:42:28Z
.ufo/waves/round-40/conform.py 04:58:55Z
.ufo/waves/round-40/count-c8.py 04:45:54Z
.ufo/waves/round-40/contract.md 04:45:38Z
run-c11-dags.py                05:40:45Z
make-survivor-fixtures.py      04:46:21Z
```

E6 — worktree freeze content vs integration commit:

```text
$ git show 8d3badd:.ufo/waves/round-40/evidence/freeze-r40.txt | diff - .ufo/waves/round-40/evidence/freeze-r40.txt && echo IDENTICAL
IDENTICAL
```

E7 — predicate equality (AST extraction, whitespace-normalised):

```text
P-C10 contract_len 1557 code_len 1564 EQUAL False   # only delta: capture prefix "P-C10: "
  SequenceMatcher opcodes: one `insert` of "P-C10: " on the code side; no other edits
P-C11 contract_len 1029 code_len 1036 EQUAL False   # only delta: capture prefix "P-C11: "
  SequenceMatcher opcodes: one `insert` of "P-C11: " on the code side; no other edits
```

E8 — note text and M23 text:

```text
$ read .ufo/waves/round-40/evidence/freeze-r40.txt:1-5
freeze-r40: sha256 over the round-40 frozen instrument paths
pinned: 2026-10-24T05:46:06Z by L1 mori-r40 attempt 1 (resumed)
note: the prior launch died before persisting this receipt; before-receipts
      run committed bytes extracted via 'git show bb1f2457:<path>' (see
      fixtures/extracted/), so before-controls are measured at entering bytes.
$ sed -n '23p' corpus/lessons/round-40.md | fold -w 200
| M23 | inherited-unverified-freeze … | the resuming L1 re-verified every inherited
instrument byte-by-byte …, completed the unfinished work (gate selftest arms 12→15;
dag-r redesign), and persisted `evidence/freeze-r40.txt` with sha256 pins plus an honest
note that it was written at integration; before-controls all run bytes extracted via
`git show bb1f2457:<path>`, so entering-state measurement is uncontaminated. …
```

E9 — contract freeze list:

```text
$ read .ufo/waves/round-40/contract.md:1-16:raw
Frozen before any data seat or data receipt: this contract, `count-c8.py`
(the round-40 counter bytes), `conform.py` (round-40 version, v3), the
modified `tools/mori-sources-appendonly.py` (the tracked gate, version 3),
the fixture builders and the survivor-fixture payloads. Pins are recorded in
`evidence/freeze-r40.txt` (sha256 over the frozen paths). …
```

E10 — unpinned payload detection:

```text
$ for f in .ufo/waves/round-40/fixtures/generated/survivor-*.py; do grep -q "$(sha256sum "$f"|cut -d' ' -f1)" .ufo/waves/round-40/evidence/freeze-r40.txt || echo "unpinned $f"; done
unpinned .ufo/waves/round-40/fixtures/generated/survivor-barecomm.py
unpinned .ufo/waves/round-40/fixtures/generated/survivor-cond.py
unpinned .ufo/waves/round-40/fixtures/generated/survivor-decoy.py
unpinned .ufo/waves/round-40/fixtures/generated/survivor-divzero.py
unpinned .ufo/waves/round-40/fixtures/generated/survivor-inf.py
unpinned .ufo/waves/round-40/fixtures/generated/survivor-second-popen.py
unpinned .ufo/waves/round-40/fixtures/generated/survivor-shadow-neg.py
unpinned .ufo/waves/round-40/fixtures/generated/survivor-shadow-none.py
unpinned .ufo/waves/round-40/fixtures/generated/survivor-tuple.py
unpinned .ufo/waves/round-40/fixtures/generated/survivor-underscore.py
```

E11 — payload regeneration from pinned inputs (written to `/tmp`, nothing in the
lane touched; temp tree removed afterwards):

```text
$ python3 .ufo/waves/round-40/fixtures/make-survivor-fixtures.py .ufo/waves/round-40/count-c8.py /tmp/surv-check
wrote /tmp/surv-check/survivor-barecomm.py (22291 bytes)
… (10 files written)
$ for f in /tmp/surv-check/*.py; do n=$(basename "$f"); a=$(sha256sum "$f"|cut -d' ' -f1); b=$(sha256sum ".ufo/waves/round-40/fixtures/generated/$n"|cut -d' ' -f1); [ "$a" = "$b" ] && echo "reproducible $n" || echo "MISMATCH $n"; done
reproducible survivor-barecomm.py
reproducible survivor-cond.py
reproducible survivor-decoy.py
reproducible survivor-divzero.py
reproducible survivor-inf.py
reproducible survivor-second-popen.py
reproducible survivor-shadow-neg.py
reproducible survivor-shadow-none.py
reproducible survivor-tuple.py
reproducible survivor-underscore.py
```

E12 — payload bytes equal the scored-tip blobs:

```text
$ for f in .ufo/waves/round-40/fixtures/generated/survivor-*.py; do a=$(sha256sum "$f"|cut -d' ' -f1); b=$(git show 265a955:$f|sha256sum|cut -d' ' -f1); [ "$a" = "$b" ] && echo "same $f" || echo "DIFF $f"; done
same .ufo/waves/round-40/fixtures/generated/survivor-barecomm.py
… (all 10: same)
```

E13 — gutted-conjunct fixtures: derivation, commits, content equality:

```text
$ diff .ufo/waves/round-40/conform.py .ufo/waves/round-40/fixtures/generated/conform-v3-conjunct-gutted.py
734d733
<         CONJUNCT_MUTATION,
$ diff .ufo/waves/round-40/fixtures/extracted/conform-v2-r39.py .ufo/waves/round-40/fixtures/generated/conform-r39-conjunct-gutted.py
451,454d450
<         ("selftest_conjunct",
<          "out, err = proc.communicate(timeout=timeout)",
<          "out, err = proc.communicate()",
<          "communicate timeout keyword stripped"),
$ git log --all --oneline -- .ufo/waves/round-40/fixtures/generated/conform-v3-conjunct-gutted.py
ede486b round-40: … + commit referenced gutted-conjunct fixture
614ca03
$ git log --all --oneline -- .ufo/waves/round-40/fixtures/generated/conform-r39-conjunct-gutted.py
265a955 round-40: instruments — conform v3 (P-C10), gate v3 (P-C11), S229, r39 erratum
2a5d94e
c2ecbbc
$ echo 'v3 gutted:'; for c in 614ca03 ede486b 8d3badd; do printf '  %s ' $c; git show $c:.ufo/waves/round-40/fixtures/generated/conform-v3-conjunct-gutted.py 2>/dev/null | sha256sum | cut -d' ' -f1; done; echo '  worktree' $(sha256sum .ufo/waves/round-40/fixtures/generated/conform-v3-conjunct-gutted.py|cut -d' ' -f1)
v3 gutted:
  614ca03 20e324228735d39ad6bb293aac9dfd4b3a27a009a0f2ecf222731771bd2aaabf
  ede486b 20e324228735d39ad6bb293aac9dfd4b3a27a009a0f2ecf222731771bd2aaabf
  8d3badd e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  worktree 20e324228735d39ad6bb293aac9dfd4b3a27a009a0f2ecf222731771bd2aaabf
$ echo 'r39 gutted:'; for c in 2a5d94e c2ecbbc 265a955 614ca03 ede486b 8d3badd; do printf '  %s ' $c; git show $c:.ufo/waves/round-40/fixtures/generated/conform-r39-conjunct-gutted.py 2>/dev/null | sha256sum | cut -d' ' -f1; done; echo '  worktree' $(sha256sum .ufo/waves/round-40/fixtures/generated/conform-r39-conjunct-gutted.py|cut -d' ' -f1)
r39 gutted:
  2a5d94e c9f01206e2f3d5d8191ee830af8bd0720567016b46f0d0afdaf2f4f9caf375b9
  c2ecbbc c9f01206e2f3d5d8191ee830af8bd0720567016b46f0d0afdaf2f4f9caf375b9
  265a955 c9f01206e2f3d5d8191ee830af8bd0720567016b46f0d0afdaf2f4f9caf375b9
  614ca03 c9f01206e2f3d5d8191ee830af8bd0720567016b46f0d0afdaf2f4f9caf375b9
  ede486b c9f01206e2f3d5d8191ee830af8bd0720567016b46f0d0afdaf2f4f9caf375b9
  8d3badd c9f01206e2f3d5d8191ee830af8bd0720567016b46f0d0afdaf2f4f9caf375b9
  worktree c9f01206e2f3d5d8191ee830af8bd0720567016b46f0d0afdaf2f4f9caf375b9
```

E14 — before-DAG receipts reproduced with the frozen builder (probe copy under
`/tmp`; the only edit was the scratch root, `dir=…` → `/tmp/probe-dags`; the
lane was not written):

```text
$ sed 's#dir=os.path.join(lane, ".scratch")#dir="/tmp/probe-dags"#' .ufo/waves/round-40/fixtures/run-c11-dags.py > /tmp/run-c11-dags-probe.py
$ for k in n p r; do python3 /tmp/run-c11-dags-probe.py "$PWD/.ufo/waves/round-40/fixtures/extracted/gate-v2-bb1f2457.py" "$PWD" "/tmp/probe-$k.txt" "dag-$k"; done
dag-n exit=0
dag-p exit=0
dag-r exit=0
$ for pair in "n c11-red-neveredited" "p c11-red-firstparent" "r c11-red-readd"; do set -- $pair; k=$1; f=$2; tail -n +2 "/tmp/probe-$k.txt" > /tmp/a.txt; tail -n +2 ".ufo/waves/round-40/evidence/$f.txt" > /tmp/b.txt; if diff -q /tmp/a.txt /tmp/b.txt >/dev/null; then echo "IDENTICAL body: dag-$k vs $f"; else echo "DIFF body: dag-$k vs $f"; diff /tmp/a.txt /tmp/b.txt | sed -n '1,12p'; fi; done
IDENTICAL body: dag-n vs c11-red-neveredited
IDENTICAL body: dag-p vs c11-red-firstparent
IDENTICAL body: dag-r vs c11-red-readd
```

Probe artifacts (`/tmp/surv-check`, `/tmp/probe-*`, `/tmp/run-c11-dags-probe*.py`)
were removed after the checks; no file under the lane was created or modified by
these probes.

E15 — builder dependency in the runner:

```text
$ grep -n '_selftest_dag_cases\|_make_dag_repo\|_selftest_env' tools/mori-sources-appendonly.py
424:def _selftest_env():
514:def _selftest_dag_cases():
626:def _make_dag_repo(path, kind, bodies, env):
$ grep -n 'def load_gate' -A4 .ufo/waves/round-40/fixtures/run-c11-dags.py
24:def load_gate(lane):
25:    spec = importlib.util.spec_from_file_location(
26:        "gate", os.path.join(lane, "tools", "mori-sources-appendonly.py"))
$ git show e104694:tools/mori-sources-appendonly.py | sha256sum
91b6134ce903dd8c92e7b9db0601d92431edf51fe29ba299aab102388d5b58d8  -
$ grep -n '_selftest_dag_cases\|_make_dag_repo\|"dag-' /tmp/probe-lane/tools/mori-sources-appendonly.py | sed -n '1,20p'
521:def _selftest_dag_cases():
525:    repo is built by _make_dag_repo with the named shas the expectations rely
570:        ("side-branch superseder is stale", "dag-a", 1,
574:        ("merge does not fabricate an edit", "dag-c", 0,
578:        ("landing is the last edit commit", "dag-d", 1,
586:def _make_dag_repo(path, kind, bodies, env):
592:    if kind == "dag-a":
600:    elif kind == "dag-d":
608:    elif kind == "dag-c":
783:        dag_cases, dag_bodies = _selftest_dag_cases()
788:                shas = _make_dag_repo(repo, kind, dag_bodies, env)
# the 05:24Z snapshot knows only dag-a/c/d; dag-n/p/r first appear in the final blob
$ for c in e104694 1a5f7c1 20c8029 b434d01 dc2be8d; do git show -s --format='%h %cI parent=%p %s' $c; printf '   gate blob %s\n' "$(git show $c:tools/mori-sources-appendonly.py | sha256sum | cut -d' ' -f1)"; done
e104694 2026-10-24T02:24:03-03:00 parent=bb1f245 
   gate blob 91b6134ce903dd8c92e7b9db0601d92431edf51fe29ba299aab102388d5b58d8
1a5f7c1 2026-10-23T15:20:10-03:00 parent=5842dc0 
   gate blob 915527a7d2f553740ed3ab0166669031f19ce2de6b2fec8501208f97244cfc89
20c8029 2026-10-23T17:55:19-03:00 parent=1f1e996 
   gate blob 9a6164e391479bcc9e50487f9eabbc95d4f25d57793f77575d33f8520fdb09fa
b434d01 2026-10-24T02:47:29-03:00 parent=bb1f245 
   gate blob bde5a9a34c7eb3bcbee39d669b8d187caeb51807ad1bdcd85a05c1bcd06777ec
dc2be8d 2026-10-24T02:47:29-03:00 parent=bb1f245 
   gate blob bde5a9a34c7eb3bcbee39d669b8d187caeb51807ad1bdcd85a05c1bcd06777ec
```

E16 — evidence mutability during the wave (context for the mtime caveat):

```text
$ git diff --name-only 8d3badd -- .ufo/waves/round-40/evidence/
.ufo/waves/round-40/evidence/c10-after-conjunct.txt
.ufo/waves/round-40/evidence/c10-after-selftest.txt
.ufo/waves/round-40/evidence/c10-red-conjunct.txt
```

Tooling: nothing installed (no pacman, no uv/npx); all checks used `git`,
`sha256sum`, `diff`, `stat`, `date`, and `python3` (stdlib only, including a
`/tmp` probe copy of the committed runner).
