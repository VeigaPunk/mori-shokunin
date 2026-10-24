# ExecBlindBaseline — frozen-run baseline for `tools/mori-blind-check.sh` (routed defect 2)

Seat `MoriR32A2.ExecBlindBaseline`. Scope: build `frozen/blind-check/` in scratch only; no lane
writes except this report file. Routed defect: `corpus/lessons/round-31-verifier-spotcheck.md:§8` item 2
(gate registry row lacks pinned-value path, write scope, owner; no digest-pinned frozen-run baseline;
PROTOCOL §Gate standard "Two evidences", `/home/vgpnk/Projects/shokunin/PROTOCOL.md:390-397`).

## 1. What was built

Produced at `/fast/scratch/hyaku/mori-r32/ExecBlindBaseline/frozen/blind-check/` (L1 copies it to
`.ufo/waves/round-32/frozen/blind-check/` with `cp -a`; `snapshot/` contains a hidden `.ufo` dir):

| file | bytes | sha256 | source (git object) |
|---|---|---|---|
| `expected.json` | 4255 | `45226329fa119057edf72aef0237a8901f6cc6d1318761e649a330dd2b0882cf` | new (this seat) |
| `verify.sh` | 6683 | `31385477cd5cea1d8eb2201588fc3c5b10fa7b836cba418a2d5bd0635b8d297d` | new (this seat) |
| `tool/mori-blind-check.sh` | 19062 | `79b774f7736cc9074fa786ad360553987d92096a3864b07212f7a3127924beb8` | `8ab61af:tools/mori-blind-check.sh`, git blob `3c26ef69…` |
| `snapshot/allow-r30.txt` | 693 | `3f562ec11a7e29712f25b93a500cda8af4c83da025dd5ed675e10a6c69d935a6` | `458ff1c:.ufo/waves/round-31/evidence/allow-r30.txt`, blob `40169703…` |
| `snapshot/.ufo/waves/round-30/w1/CaseR30a.md` | 5732 | `7fa1c668274b625ebbbff837a1d87b08130cae7c05eabe2d74dea1a7c6ad4e31` | `5c99f2d4`, blob `61db9a9b…` |
| `snapshot/.ufo/waves/round-30/w1/CaseR30b.md` | 6045 | `22c5343552ff0c8b54ec4690c78436e9e6f939e11d733081416d9373ddc305dd` | `5c99f2d4`, blob `4a0bb80d…` |
| `snapshot/.ufo/waves/round-30/w1/CaseR30c.md` | 5637 | `71591db6636d8d19f24f85addc9e22706975f5383df42b398d88faddcb17e4ef` | `5c99f2d4`, blob `7a4d82c2…` |
| `snapshot/.ufo/waves/round-30/w1/CaseR30d.md` | 5882 | `8527a241ffb2dede92b5026e47590478781ed93c9deab26408f0c27971d51124` | `5c99f2d4`, blob `fb70eadf…` |

Named lane revision for the snapshot: **`8ab61affbd2fc59030040bf80cddc08f7c60ad82`** (round-32 C0 tip).
Every pinned blob above is byte-identical at that revision (`git rev-parse` of each path at `8ab61af`
returns the blob ids listed), so the snapshot is reproducible from the lane tip alone; the originating
revisions are `5c99f2d4213b41966d670d10006a2ff5135273e4` (round-30 writer wave, the revision named by
`.ufo/waves/round-31/evidence/c2-tool-selftest-and-r30.txt`) and
`458ff1c3b745171a461aaa4aca43efc476119d94` (round-31 tool commit, which also added the allow file).
Tool blob `3c26ef69…` is unchanged at `458ff1c`, `52435f2f` and `8ab61af`; sha256 `79b774f7…` matches the
round-31 closure's measured value (`corpus/lessons/round-31-verifier-spotcheck.md:§3 C2`).

`expected.json` pins: every snapshot input digest + bytes + git blob oid, `tool.sha256` / bytes / blob oid,
`invocation` (wave dir `.ufo/waves/round-30/w1`, regex `^CaseR30[a-d]\.md$`, allow file, revision semantics),
`expected_stdout` (5 lines) and `expected_exit` = 1.

## 2. What `verify.sh` does

Contract: `0` = pinned tool over pinned snapshot reproduced pinned stdout+exit; `1` = differ; `2` =
`snapshot_tampered` (missing or digest-mismatched pinned file — the tool is not run).

1. Requires `expected.json`; a missing or schema-invalid table is a setup error, exit 2.
2. Digest-gates **every** snapshot input (4 briefs + allow file) with `sha256sum` before anything runs.
   Any missing file or mismatch prints `snapshot_tampered` and exits 2 with the offending path/digest.
3. Runs the pinned copy `tool/mori-blind-check.sh` — not the lane's live tool — so the baseline is
   self-contained. The tool needs git (`git rev-parse --show-toplevel`, `ls-tree`, `show` at a revision),
   so `verify.sh` materialises `snapshot/` into a throwaway repo under `${TMPDIR:-/tmp}` (`mktemp -d`,
   `git init`, one commit) with `snapshot/.ufo/...` committed as `.ufo/...`, which makes the printed hit
   paths identical to the pinned `expected_stdout`. The lane is never written to and never used as the
   working tree; the temp tree is removed by an EXIT trap.
4. Compares stdout line-by-line and the exit code with `expected.json`; also compares the tool copy's
   sha256 against `tool.sha256`. Any of the three differing → `frozen_run: differ`, exit 1.

Design note (judge-visible): the tool digest mismatch is classified **exit 1 (differ), not exit 2**.
`snapshot_tampered` is reserved for the gate's *inputs* (PROTOCOL: "an edited snapshot is
`snapshot_tampered`"); a changed **tool** is the gate itself drifting, so the frozen verdict was not
reproduced → `failed`, matching the required third demonstration. A *missing* tool file is exit 2 (the
baseline cannot be evaluated at all).

## 3. Retained evidence (all three required runs + one extra)

Captured at `/fast/scratch/hyaku/mori-r32/ExecBlindBaseline/evidence/`.

**Green on the untouched snapshot** (`evidence/verify-green.txt`):

```
$ cd frozen/blind-check && bash ./verify.sh
tool_sha256=79b774f7736cc9074fa786ad360553987d92096a3864b07212f7a3127924beb8
tool_exit=1 (expected 1)
frozen_run: match
exit=0
```

**`snapshot_tampered` exit 2 after editing one snapshot byte, in a copy** (`evidence/verify-tampered.txt`;
byte 100 of `CaseR30c.md` flipped 0x52→0x58, sha256 `71591db6…` → `b71afddd…`):

```
$ cp -a frozen/blind-check copy-tamper  # then: byte 100 of snapshot/.ufo/waves/round-30/w1/CaseR30c.md  0x52 -> 0x58
snapshot_tampered
verify: digest mismatch: snapshot/.ufo/waves/round-30/w1/CaseR30c.md (expected 71591db6636d8d19f24f85addc9e22706975f5383df42b398d88faddcb17e4ef, got b71afddd060af4f6958dec8aafc7dd87aa8b7577fa1b958344fdd11831e34b88)
exit=2
```

**Exit 1 with a mutated tool copy** (`evidence/verify-muttool.txt`; rule label suffixed `MUT` in the copy):

```
$ cp -a frozen/blind-check copy-muttool  # then: append MUT to the rule label in tool/mori-blind-check.sh
verify: pinned tool bytes differ (expected 79b774f7736cc9074fa786ad360553987d92096a3864b07212f7a3127924beb8, got c378acd2047648ac17f7752bd0c5deeb0d048cb588c6e8d40fe390918f835741)
verify: stdout differs: line 3 differs: expected '.ufo/waves/round-30/w1/CaseR30a.md:1:writer-missing-files-opened-list', got '.ufo/waves/round-30/w1/CaseR30a.md:1:writer-missing-files-opened-listMUT'
verify: pinned tool bytes changed; the frozen verdict was not reproduced under the pinned tool
tool_sha256=c378acd2047648ac17f7752bd0c5deeb0d048cb588c6e8d40fe390918f835741
tool_exit=1 (expected 1)
frozen_run: differ
exit=1
```

**Extra control: missing snapshot file** (`evidence/verify-missing.txt`): `CaseR30b.md` removed from a copy →
`snapshot_tampered` / `verify: missing pinned snapshot input: snapshot/.ufo/waves/round-30/w1/CaseR30b.md`
/ exit 2.

**Pinned verdict = the committed round-30 receipt.** Pinned stdout is

```
scanned=4
blind_violations=3
.ufo/waves/round-30/w1/CaseR30a.md:1:writer-missing-files-opened-list
.ufo/waves/round-30/w1/CaseR30b.md:1:writer-missing-files-opened-list
.ufo/waves/round-30/w1/CaseR30d.md:1:writer-missing-files-opened-list
```

exit 1 — byte-for-byte the lines in `.ufo/waves/round-31/evidence/c2-tool-selftest-and-r30.txt` ("round-30
writer wave at `5c99f2d4`", `scanned=4 blind_violations=3 exit=1`). `CaseR30c` is clean because its
`## Files opened` entry (`.ufo/waves/round-30/rule-text.md`, absolute lane path) is covered by the allow
file; a/b/d have no files-opened block → `writer-missing-files-opened-list` at line 1. The committed
receipt is now digest-pinned, which is exactly what round-31 §8 item 2 said was missing.

**Self-test arm of the gate** (capability, not measurement): `TMPDIR=<seat>/tmp bash
frozen/blind-check/tool/mori-blind-check.sh --selftest` → `PASS`, exit 0 (it builds its own `mktemp` repo
in `TMPDIR` and removes it; the seat `tmp/` was empty afterwards).

## 4. Draft SKILL.md registry row (column order of `SKILL.md:162`)

Belongs under `## Round31 — blind-writer gate (tools/mori-blind-check.sh)` (currently `SKILL.md:772-782`).

```
| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| blind-writer gate (r31) | gate | `bash tools/mori-blind-check.sh <lane-rev> <wave-report-dir> <writer-name-regex> <allow-file>` inside the lane; frozen-run arm `bash .ufo/waves/round-32/frozen/blind-check/verify.sh` | 0 clean (`scanned=N`, `blind_violations=0`) · 1 failed (`blind_violations>0`, one `path:line:rule` per hit; frozen arm: `frozen_run: differ`, also when the pinned tool bytes changed) · 2 could-not-evaluate (usage, invalid lane revision, report directory absent at that revision, unreadable allow file; frozen arm: `snapshot_tampered`) | `bash tools/mori-blind-check.sh --selftest` → prints `PASS`, exit 0; spelling is `--selftest` (no `--self-test` alias); 14 synthetic briefs, expected `scanned=14`/`blind_violations=13` plus 13 exact hit lines pinned in `selftest()` | `.ufo/waves/round-32/frozen/blind-check/expected.json` — sha256 of the 4 round-30 briefs and the round-30 allow file, gate blob sha256 `79b774f7…` (`3c26ef69…`), expected stdout and exit 1 | read-only over the lane tree at the named revision; frozen arm writes only a throwaway git repo under `$TMPDIR`, removed on exit; `--selftest` uses its own `mktemp` tree; never writes the lane | mori |
```

Field coverage vs PROTOCOL §Gate standard (`PROTOCOL.md:401-403`): name ✓, `gate|probe` ✓ (`gate`),
entry command ✓ (both arms), verdict map code→class ✓ (0/1/2 → clean/failed/could-not-evaluate, with the
frozen arm's classes), self-test command and spelling ✓, pinned-value path ✓, write scope ✓, owner ✓.

## 5. For the L1

- Copy with `cp -a frozen/blind-check <lane>/.ufo/waves/round-32/frozen/blind-check/` — `snapshot/.ufo` is
  a hidden directory; `cp -r frozen/blind-check/. dst/` also works. Do not reflow `expected.json`: it is
  JSON with the pins as data.
- The frozen run does not exercise the lane's live tool. Drift check (optional, one command):
  `sha256sum <lane>/tools/mori-blind-check.sh` vs `79b774f7…`; if it differs, the frozen arm will say
  `differ` and the pin must be re-taken deliberately (that is the intended signal, not a bug).
- `git` and `python3` are the only dependencies; both are already required by the gate and the lane's
  counters. No tool was installed or updated in this seat.

## 6. Risks / limits

- The pinned verdict depends on the wave-dir string `.ufo/waves/round-30/w1` because the tool prints
  repo-relative paths; `verify.sh` takes it from `expected.json`, so a rename of the pin table is the only
  way to break it.
- `verify.sh` trusts `$TMPDIR`; if it is not writable the run fails closed at exit 2 with a message
  (never a false `match`).
- The tool copy is a duplicate of the lane blob. If the lane tool is legitimately fixed later, this frozen
  baseline keeps grading the old bytes — correct for a historical pin, but the registry row must then name
  the frozen arm's revision explicitly (it does, via `expected.json.source`).
- Classifying a tool-digest change as exit 1 (not 2) is a deliberate, documented choice (§2); if the closure
  wants every digest under `snapshot_tampered`, the third demo necessarily becomes exit 2 instead of 1, which
  contradicts the assignment's required outcome.

## 7. Bounds compliance

No lane writes except this report; all artifacts under `/fast/scratch/hyaku/mori-r32/ExecBlindBaseline/`.
Read-only git only in the lane (`git show`, `git rev-parse`, `git ls-tree`, `git merge-base`, `git log`);
no git/jj writes, no sandbox clone was needed. No `pacman`, no installs. Every command bounded by
`timeout` (≤120 s here); debug temp trees removed; `pgrep -af "mori-blind-check|verify.sh"` → none.
