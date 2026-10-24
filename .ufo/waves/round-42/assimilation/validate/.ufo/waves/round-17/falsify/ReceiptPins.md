# ReceiptPins — falsification of expected.json pins, sandbox metadata, frozen census and MoriR16.Lesson pins

Seat: `MoriR17.ReceiptPins-4`, mori round-17 wave 2 (fresh falsification of settled wave-1 work).
Date: 2026-10-20. Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Read-only attack: no selftests, no builds, no VCS mutation, no tool installs, no writes except
this report. Readings were taken at branch tip `5c1dfb8d0530c74eb0e1630c2b522b735b486274`
(measured inputs commit `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7`).

Method: the pin table was recomputed with an **independent** walker (own implementation:
`os.walk(followlinks=False)` + `lstat`), not by importing or invoking
`tools/mori-round17-seat-regressions.py`, then cross-checked against (a) the committed blob
bytes at the measured commit via `git cat-file --batch` / `git show`, and (b) the gate's own
recorded receipts (`fixtures.pins`, `inputs_before/after`, `expected.sha256`, `gate_sha256`).

## O1 — expected.json pin table: PASS (0 missing, 0 extra, 0 mismatched)

- `.ufo/waves/round-17/fixtures/seat/expected.json` = 54 cases (ids unique), 81 pins, every
  digest 64 lowercase hex; strict `object_pairs_hook` parse found **no duplicate JSON keys**
  in the table.
- Fixture tree contains 82 non-directory entries: **78 regular fixture files + 3 symlinks =
  81 pinned entries**, plus `expected.json`, which is excluded from its own pin map **by
  design** (doc `tools/mori-round17-seat-regressions.py:35-43`; enforcement at `:396`
  `pins must not include expected.json itself`). Directories are unpinned by design (`:403`
  `compute_pins` walks non-directory entries).
- Independent recompute: **missing (actual, unpinned) = 1 = `expected.json` only → substantive
  missing 0; extra (pinned, absent) = 0; mismatched = 0.**
- Committed anchoring (not just worktree): `git ls-tree -r 273aa74 -- .ufo/waves/round-17/fixtures/seat`
  yields 82 blobs, modes only `100644`/`120000`; sha256 of each of the 81 pinned committed blobs
  equals the declared pin; no pin lacks a committed path; only `expected.json` is
  committed-but-unpinned. `git status --porcelain -- fixtures frozen` is empty, so worktree =
  HEAD for these paths. `git diff --stat 273aa74..HEAD -- tools fixtures frozen` shows exactly
  one added file (`frozen/c3-expected.json`), so no fixture or tool bytes moved after the
  measured commit.
- Symlink pins are sha256 of the link-target text and all targets are **relative**
  (`missing-target.txt`, `trap.txt`, `real-dir`), committed as `120000`; the pins therefore
  reproduce in a fresh clone and are not machine-path dependent.
- Gate-receipt agreement: both `evidence/seat-before/run-manifest.json` and
  `evidence/seat-after/run-manifest.json` record `fixtures.pins.verified=true`,
  `declared=81`, `missing/extra/mismatched=[]`, `declared_sha256=76e2f25ee5551dda…8fda1`.
  Independently: `sha256(json.dumps(pins,sort_keys=True,separators=(",",":")))` =
  `76e2f25ee5551dda…8fda1` — **identical**, so the map verified at measurement time is byte-for-byte
  the map that exists now. `expected.sha256=b684c63b…cb01f` equals PINNED_INPUTS.
- `inputs_before == inputs_after` across all 132 walk entries in the receipt (no fixture drift
  during the run). Three manifest-vs-pin value differences are **encoding only**: the manifest
  stores `link:<target>` while pins store `sha256(<target>)`; they are the same 3 symlinks.
- Coverage sanity: 44 distinct pack names, 43 present directories; the only absent pack is
  `MissingDir`, used solely by the one `rc=2` setup case; all case `args` are literal flags
  (no case supplies `--sessions-dir` or an absolute path), so the gate always prepends its own
  per-case sandbox.

## O2 — Generated FIFO / chmod are sandbox metadata, never committed files: PASS

- Source tree scan: **0 FIFOs, 0 sockets, 0 devices**; mode histogram `51×d755, 79×f644,
  3×l777`; **no mode-000 file**. `UnreadableFile/locked.jsonl` is 0 bytes mode 644 and pinned as
  `e3b0c442…b855` (sha256 of empty content).
- `FifoSkip/pipe.jsonl` is absent from the source pack and from the pin table; its case declares
  `fifo_files: ["pipe.jsonl"]` and expects `files_scanned: 1`; receipt case `fifo_skipped` =
  `match`, observed `files_scanned=1`.
- Gate semantics: `_validate_unreadable_files` requires the source to stay readable
  (`tools/mori-round17-seat-regressions.py:512-553`); `_validate_fifo_files` rejects a source
  path that already exists (`:582-590`); `materialize_sandbox` copies the pack to
  `output/cases/<id>/sessions` and applies `os.chmod(target, 0)` (`:910`) and `os.mkfifo(target)`
  (`:928`) **only in that copy**. Pins therefore always hash source bytes.
- Committed tree modes are only `100644`/`120000`; a FIFO, device or mode-000 cannot be stored
  in git at all, and none is present. Receipt `unavailable_unreadable_file` = `match`
  (`files_scanned=2`, `locked→unavailable`, `open→completed`), proving the copy-only chmod path
  actually executed in the measurement environment.

## O3 — Frozen entering census: PASS

- `.ufo/waves/round-17/frozen/mori-census.sh`: 223560 bytes, mode 755, sha256
  `f1f8d1b62bb617bbcc4664057ab807d3fed8c275b7aabbdf7b373323c5501ff7` = PINNED_INPUTS.
- `git show 24526ea:tools/mori-census.sh | sha256sum` = `f1f8d1b6…01ff7` — byte-identical to
  the frozen copy. `24526ea` is the contract's entering tip and `git merge-base --is-ancestor
  24526ea refs/heads/master` exits 0.
- The frozen file is actually consumed: `evidence/jj-before/run-manifest.json` `census` =
  `{path: …/frozen/mori-census.sh, sha256: f1f8d1b6…}`; `jj-after` `census` =
  `{path: tools/mori-census.sh, sha256: 12e8e2d9…6d85}` = PINNED_INPUTS delivered digest.
- Content check that it is the pre-change file, not a relabelled copy: frozen has 16 `HEAD`
  references and **0** `refs/heads/`; delivered has 64 `HEAD` and 22 `refs/heads/`.
- All 9 `PINNED_INPUTS.files` digests independently recompute from `273aa74:<path>` blobs:
  **9/9 match**, 0 absent, 0 mismatched.

## O4 — MoriR16.Lesson exactness: PASS for pinned/frozen/tool bytes

- `.ufo/waves/round-17/frozen/MoriR16.Lesson`: 847 bytes, sha256
  `15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e` = PINNED_INPUTS (bytes and
  digest), matching the 847-byte claim in `corpus/lessons/round-17.md`.
- `cmp /home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/MoriR16.Lesson <frozen>` exits 0;
  both files hash to the same digest. The fleet-root original is absent
  (`test -e /home/vgpnk/Projects/shokunin/MoriR16.Lesson` rc1), consistent with relocation.
- The detector's embedded payload `_ARCHIVE_B64` (`tools/mori-misroot-sweep.py:352`) decodes
  in-memory to 847 bytes, sha256 `15f9f82d…`; decoded bytes compare **equal to both** frozen and
  archive copies, and `_archive_bytes()` self-checks the digest (`:384`).
- `frozen/c3-expected.json` states bytes 847 / sha256 `15f9f82d…`; its expected rc pair 0/1,
  `matched_in ["path"]` and missed `[1,0]` agree with `evidence/c3-before.json` (rc0,
  `MORI_MISROOT_CLEAN`, legacy pathspec) and `evidence/c3-after.json` (rc1,
  `MORI_MISROOT_CANDIDATE`, `read_bytes=size_bytes=847`, `matched_in ["path"]`), and with
  `evidence/count-c3.json` `[1,0]`. Its committed blob equals the worktree bytes
  (`git show HEAD:…` sha256 = worktree sha256, `94f9c401…`).

## Findings — provenance/coverage, not digest defects

**F1 (PINNED_INPUTS and c3-expected are retrospective documents, but their bytes are
commit-anchored).** Timeline from commits and receipts: build commit `273aa74` 16:31:56;
`jj-before` 19:32:55Z (16:32:55-03); `c3-before`/`c3-after` 16:34:52.90–.97;
`PINNED_INPUTS.observed_at` 16:35:35; `frozen/c3-expected.json` mtime 16:35:45; both pinned files
first committed in `5c1dfb8` at 16:37:09. `PINNED_INPUTS.json` is **absent from `273aa74`**
(`git cat-file -e` fatal) despite naming `measured_commit: 273aa74`. This is acceptable for the
digests because every listed digest equals bytes that already existed in `273aa74` (9/9 verified),
so no pinned byte can be result-dependent. The artifact left outside the declared pin map is
`frozen/c3-expected.json` itself: it did not exist when PINNED_INPUTS was written and is not in
`PINNED_INPUTS.files`; `grep` finds no tool/gate that reads it, so it cannot influence any
measurement. It is a post-hoc expectation record whose content matches the archive, not a
pre-registered frozen instrument.

**F2 (C3 measurement receipt records size, not witness content digest).** `c3-after` scan:
`regular_files=2`, `untracked_entries=2`, `bytes_read=876` = 847 + 29, and
`29 = len("Tabi round16 sibling control\n")` from
`.ufo/waves/round-17/c3-capture-recipe.json:19`. The two-file composition and total size therefore
corroborate the intended sandbox very strongly, but the 847-byte file's byte-identity is
*inferred* from frozen/archive provenance, not witnessed by a sha256 in the receipt. The setup
recipe is **untracked** (`git status` `??`), mtime 16:47:24, i.e. written after the run
(16:34:52) and after the measurement commit (16:37:09). Exact-byte behaviour is directly
exercised by the pinned tool's own 11-arm selftest (embedded payload + digest self-check), whose
tool digest `0a852fe6…` is pinned at `273aa74`. Sibling naming is also split: the post-hoc recipe
and `c3-expected.json:11` name `TabiR16.Lesson`, while the tool selftest uses `TabiNote.md`
(`tools/mori-misroot-sweep.py:370`); the receipt's single candidate still proves the sibling was
not flagged, but not that the named sibling file was present in that sandbox.

## Verdicts on the attacked sub-claims

| Attacked sub-claim | Verdict |
|---|---|
| expected.json pins recompute exactly (regular + symlink) | **CONFIRMED** — 81/81, 0 missing, 0 extra, 0 mismatched |
| Pins anchored to committed bytes, not just worktree | **CONFIRMED** — all 81 committed blobs at `273aa74` match |
| Generated FIFO/chmod are sandbox-only metadata | **CONFIRMED** — source has no FIFO/device/000; gate creates them only under `output/cases/<id>/sessions`; receipts show the copies ran |
| Frozen entering census equals the entering commit's file | **CONFIRMED** — byte-identical to `24526ea:tools/mori-census.sh`, consumed by jj-before |
| MoriR16.Lesson frozen/tool/archive bytes exact | **CONFIRMED** — `cmp` rc0, 847 B, same sha256 in frozen, archive, tool payload, c3-expected |
| C3 measured-sandbox byte-exactness | **PARTIAL/[INFERENCE]** — size 847 and 2-file/876-byte total corroborated; no content digest in receipt; sandbox removed; recipe untracked and postdates run |
| PINNED_INPUTS covers every frozen artifact | **GAP** — `frozen/c3-expected.json` (committed in `5c1dfb8`) and untracked `c3-capture-recipe.json` are outside `PINNED_INPUTS.files` |

No digest mismatch, missing fixture, extra pin, duplicate-key shadowing, absolute symlink pin, or
untrackable committed special file was found in the attacked scope.

## Residual unknowns

- The `MainChecks/c3-fleet` sandbox no longer exists (`ls` ENOENT), so its planted bytes cannot be
  re-hashed; exactness rests on the frozen/archive digests, the 876-byte composition arithmetic,
  and the pinned tool selftest.
- The 29-byte sibling string is quoted from the post-hoc recipe; its actual presence in the
  measured sandbox is inferred from the byte total, not independently receipted.
- No live re-run of any probe was performed (forbidden), so all statements are about committed
  receipts and current worktree bytes.

## Commands of record (all read-only, rc0 unless stated)

- Independent pin walk (in-process Python, `os.walk(followlinks=False)`, `lstat`, sha256 over
  content / `os.readlink` text): 82 entries, 81 pins, missing `['expected.json']`, extra `[]`,
  mismatched `[]`.
- `git ls-tree -r -z 273aa74 -- .ufo/waves/round-17/fixtures/seat` + `git cat-file --batch`
  (sha256 of 82 blobs): 82 blobs, modes `100644`/`120000`, 81/81 pins equal, 0 pins uncommitted.
- `git status --porcelain -- .ufo/waves/round-17/fixtures/seat .ufo/waves/round-17/frozen`:
  empty (rc0).
- `find … -printf '%y %m\n' | sort | uniq -c`: `51 d 755`, `79 f 644`, `3 l 777`;
  `find … \( -type p -o -type s -o -type b -o -type c \) | wc -l` = 0.
- `sha256sum .ufo/waves/round-17/frozen/{mori-census.sh,MoriR16.Lesson,c3-expected.json}` and
  `git show 24526ea:tools/mori-census.sh | sha256sum`: `f1f8d1b6…`, `15f9f82d…`, `94f9c401…`
  (JSON), entering blob `f1f8d1b6…`.
- `cmp <archive> .ufo/waves/round-17/frozen/MoriR16.Lesson`: rc0.
- In-memory decode of `_ARCHIVE_B64`: 847 bytes, `15f9f82d…`, `==frozen True`, `==archive True`.
- `jq` receipts: seat-before/after `fixtures.pins.verified=true, declared=81, declared_sha256=76e2f25e…`;
  `gate_sha256=21285c2b…` = pinned gate; after `tool.sha256=5819c3c0…` = pinned tool;
  jj-before census `f1f8d1b6…`, jj-after census `12e8e2d9…`; count-c1 `[54,0]`, count-c2 `[21,0]`,
  count-c3 `[1,0]`; c3-before scan `regular_files=0`, c3-after scan `regular_files=2,
  untracked_entries=2, bytes_read=876`.
- Canonical pin digest: `sha256(json.dumps(pins, sort_keys=True, separators=(",",":")))` =
  `76e2f25ee5551dda…8fda1` = receipt `declared_sha256`.
- `git log --format=… -- PINNED_INPUTS.json` → only `5c1dfb8` (16:37:09); `git diff --stat
  273aa74..HEAD -- tools fixtures frozen` → only `frozen/c3-expected.json` added.

No tool install or upgrade was performed (nothing was needed); no pacman transaction, background
job, journal query, or scratch write was made.
