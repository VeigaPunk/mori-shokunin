# LiveTameshi: C2 falsification on tameshi-shokunin

**Verdict: HOLDS.** On lane tameshi-shokunin (16 `ufo-swarm-wave-dispatch-v1` files, 965 members) the per-file and per-member settlement from `tools/mori-wave-settlement.py` agrees with the independent oracle, the wave-1 ground truth, and the committed fleet snapshot's lane totals. There are zero unexplained differences. One difference is a label change caused by a tool edit, not a lane change. The latent defects in section 4 are not triggered on this lane, so they do not change this verdict. They do affect how fleet-wide exit codes should be read.

Scope: lane `/home/vgpnk/Projects/shokunin/tameshi-shokunin`, fleet root `/home/vgpnk/Projects/shokunin`. Leaf seat, no subagents. Lane files, git index and jj state untouched; git used read-only only (`cat-file`, `log`, `rev-parse`). No tool installed or updated. Nothing under `.ufo/interactive-sessions`, `.ufo/worktrees`, `.jj` or `~/.omp` was read.

## 1. Tool version under test

The tool changed four times during this audit. Each result below is tied to the exact file hash it was produced by.

| version | mtime (-0300) | sha256 | tameshi result |
|---|---|---|---|
| committed 2eeae04 (HEAD blob) | commit 07:47:09 | `c6e6091937e4bcb02775cea81ce33990924c6e27487a6ce255d2959d94f4e795` | output `cmp`-identical to scan.json (2 runs); selftest 21/21 PASS, rc 0 |
| worktree | 08:04:26 | `e5c06dad076b8e5aebbebcd53cf7c32de41592b4899319502b8cca003d4b8a48` | not run separately; code identical to HEAD, only r7 test lines added [INFERENCE from a read of that version] |
| worktree | 08:11:12 | `203c716e1dc55fa6ac912335e15516c63a46d4d4bc7f6cd9554a2e45212061a9` | output `cmp`-identical to scan.json; selftest 22/22 PASS, rc 0 |
| worktree = frozen copy `falsify/LiveTameshi/tool-snapshot.py`, still current at report time | 08:15:31 | `c134c57b501aa6469fab6a3e240b903a0f5cfc0a5cc04240363a29972da42454` | differs from scan.json in one field (D1); selftest 23/23 PASS, rc 0 |

Reference artefacts: GT file `build/GtLaneTameshi.md` 07:37:04 -0300; fleet snapshot `evidence/c2-live-fleet.json` 07:46:53 -0300. My scan `falsify/LiveTameshi/scan.json`, sha256 `de48d06e8a9ac63148c13939d87673e0a9efb291dc284ddeb89d211db57b02ec`, exit 1, re-ran byte-identical.

## 2. Results on tameshi

Live scan, independent oracle (`falsify/LiveTameshi/oracle.json`, written from the frozen contract text, does not import the tool), and GT per-file table all agree on every column below. Empty, unparsed and unsafe are 0 in every file.

| # | dispatch (under `.ufo/waves/`) | wave | members | present | missing | misrooted | stub | state |
|---|---|---|---:|---:|---:|---:|---:|---|
| 1 | round-12/dispatch.json | tameshi-r12-w1 | 32 | 30 | 2 | 0 | 0 | partial |
| 2 | round-12/dispatch-w2.json | tameshi-r12-w2 | 32 | 32 | 0 | 0 | 0 | settled |
| 3 | round-13/dispatch.json | tameshi-r13-w1 | 32 | 32 | 0 | 0 | 0 | settled |
| 4 | round-14/dispatch.json | tameshi-r14-w1 | 32 | 32 | 0 | 0 | 0 | settled |
| 5 | round-15/dispatch1.json | tameshi-r15-w1 | 66 | 57 | 9 | 0 | 0 | partial |
| 6 | round-15/dispatch2.json | tameshi-r15-w2 | 32 | 32 | 0 | 0 | 0 | settled |
| 7 | round-16/dispatch1.json | tameshi-r16-w1 | 68 | 68 | 0 | 0 | 0 | settled |
| 8 | round-16/dispatch2.json | tameshi-r16-w2 | 67 | 67 | 0 | 0 | 0 | settled |
| 9 | round-17/dispatch1.json | tameshi-r17-w1 | 67 | 67 | 0 | 0 | 0 | settled |
| 10 | round-17/dispatch2.json | tameshi-r17-w2 | 99 | 92 | 7 | 0 | 0 | partial |
| 11 | round-18/dispatch1.json | tameshi-r18-w1 | 73 | 73 | 0 | 0 | 0 | settled |
| 12 | round-18/dispatch2.json | tameshi-r18-w2 | 93 | 93 | 0 | 0 | 0 | settled |
| 13 | round-19/run1.json | tameshi-r19-w1 | 64 | 64 | 0 | 0 | 0 | settled |
| 14 | round-19/run2.json | tameshi-r19-w2 | 64 | 64 | 0 | 0 | 0 | settled |
| 15 | round-20/run1.json | tameshi-r20-w1 | 72 | 27 | 45 | 0 | 0 | partial |
| 16 | round-20/validation-current.json | tameshi-r20-w1 (`duplicate_of` run1) | 72 | 27 | 45 | 0 | 0 | partial |
| | **total** | 16 waves (11 settled, 5 partial) | **965** | **857** | **108** | **0** | **0** | |

- **Lane totals vs fleet snapshot** (`tameshi-shokunin` entry): members 965=965, present 857=857, missing 108=108, misrooted 0=0, empty 0=0, unparsed 0=0, unsafe 0=0, unreadable_json 0=0, exit 1=1 (live rc 1). The snapshot has no per-file rows and no `stub` or `state` field, so a per-file or stub comparison against it is impossible. The per-file comparison above is against GT and the oracle.
- **Member level:** 965 GT rows (`build/MoriR20.GtLaneTameshi/member-paths.tsv`) vs oracle: 0 only-in-GT, 0 only-in-oracle, keyed on (dispatch, member, report path, status). Live scan vs oracle: 0 mismatches in dispatch sha256, state, counts, and per-member (name, agent, status) in task order.
- **Missing names** match GT F3/F4/F5 exactly: round-12 `BashWitness`, `ControlGate`; round-15 nine `Recon*`; round-17 seven (`CriticC1`, `CriticC2`, `CriticNoHarm`, `CriticSeparability`, `RegistryProvenance`, `SentinelLanded`, `SentinelTraceEscape`); round-20 45.
- **Discovery:** `find .ufo/waves` (hidden included) gives 106 regular `*.json`, 0 symlinks, 0 other entries. Tool: `ignored_json` 90, `unreadable_json` 0, 16 dispatch-v1. The top-level schema tally matches GT (28 registry, 16 dispatch, 4 wave-v1, 1 outcomes, 56 no schema, 1 array).
- **Stub and empty:** no present report contains `STATUS: started` in its first 200 bytes; 0 whitespace-only; smallest present report 1548 bytes. Tool `stub` 0 and `empty` 0 are correct.
- **Unique counts:** 893 report paths, 830 present, 63 missing, 15 unique dispatch sha256. `round-20/validation-current.json` is byte-identical to `run1.json` (sha256 `e44c144664ad2c78d84b3bf3b8584b97a33f68eb78b65267d299f6b5a7271b12`, 114468 bytes each).

## 3. Differences and explanations

Total differences: 1 (D1). Lane changes since the snapshot: none.

- **D1. `waves[15].name_hint` (`round-20/validation-current.json`).** scan.json: `undispatched-name:validation`. Frozen current copy: `filename:validation`. Structural JSON diff gives exactly this one difference. Cause: a tool edit. Committed `tools/mori-wave-settlement.py:298` emits `"undispatched-name:"`. Frozen copy `tool-snapshot.py:310` emits `"filename:"`, and its r3 selftest at `:45` now expects `filename:preview`. Status, counts, state and totals are identical. The lane did not change (below).
- **D2 (GT annotation only).** GT F3 gives `round-15/w1/SiblingOverlap.md` mtime as "05:05:06" with no date. Actual: 2026-10-20 05:05:06.82 -0300, 15292 bytes, present in both. No count effect.

Lane-change evidence (`cd tameshi-shokunin`):
- `find .ufo/waves -newermt @<GT 10:37:04Z>` → 0 files; `@<snapshot 10:46:53Z>` → 0 files.
- Newest file under `.ufo/waves`: `round-20/residual/registry.json` 07:26:50.86 -0300. Newest present report: `round-20/w1/A01ProvRound19Ruler.md` 06:44:51.26 -0300.
- All 965 trailers point under `.ufo/waves`. Present reports newer than GT or snapshot: 0. Missing report paths that exist on disk now (lexists): 0. Lane-root entries newer than GT: none.

## 4. Latent defects (probed; none triggered on tameshi)

Probes were built in `/tmp/lt-synth2` and run against committed 2eeae04 and the frozen copy. Results: `falsify/LiveTameshi/probes.json`. Line numbers are for the frozen copy unless marked HEAD.

| probe | committed 2eeae04 | frozen c134c57b | location | class |
|---|---|---|---|---|
| P1 no `.ufo` dir | rc 0, waves [] | rc 0, waves [] | `_wave_root` :79–97 → `:330–331` paths=[]; `:379` rc 0 | silent false green |
| P2 `.ufo/waves` is a symlink | rc 0, waves [] | rc 0, waves [] | `:95–96` symlink refused; `:379` | silent false green |
| P3 trailer `…/r.md/` on a regular file | present | present | `_safe_report_path` `:160–179` drops empty components | accepts a non-canonical path (POSIX gives ENOTDIR) |
| P4 stub `STATUS: started\r\n` / `…   \n` | stub for exact, present for the two variants | same | `STUB_CONTENTS` `:37` exact bytes; size gate `:238–240` | stub variants not caught |
| P6 unreadable parent holding an 11-byte report, outside waves | missing, rc 1 | missing, rc 1 | `_inspect_report_path` `:199–200` → unavailable; `_member_status` `:242–246` falls through to missing | present file reads missing (documented: knowledge note line 33) |
| P5 unreadable dir inside `.ufo/waves` | rc 2 | rc 2 | `_dispatch_files` `:100–131` raises ScanError; `:694` message | fail-closed, but message blames the lane root |
| P9 lane root is a symlink | rc 2 | rc 2 | `scan_lane` `:322–323` | fail-closed; message wrong |
| P10 dispatch file is a symlink | silently skipped, in neither count | same | `_dispatch_files` `:100–131` (`S_ISREG` only) | per spec, but invisible in counts |
| P8 `--fleet-root` is a symlink | missing (false negative) | misrooted (fixed) | HEAD `:313` `os.path.abspath`; frozen `:327` `realpath` | fixed in frozen copy |
| P11 symlinked parent of report path | missing | unsafe (fixed) | frozen `:203–204`, `:233–234` | fixed (R8) |
| P12 nonexistent `--fleet-root` | rc 0 (fleet root unused) | rc 2 | frozen `:328–329`, `:694` | behaviour change, fail-closed |

**Fleet reading.** The committed snapshot shows six lanes at exit 0 with waves 0. Five (audio, game-dev-2d, game-dev-3d, kotoba, kotodama) have no `.ufo/waves` directory. Lore has one, with 1102 `*.json` files, 0 dispatch-v1 (my tally), and `unreadable_json` 1 recorded in the snapshot. Exit 0 there means "no waves discovered", not "all settled", and the snapshot does not distinguish the two.

## 5. Document and version drift (not accuracy errors on tameshi)

- Committed docstring says stub reads "at most 64 bytes" (HEAD `:10`). Code reads at most 16 (`STUB_CONTENTS` `:37`, size gate `:238`). The frozen copy corrects the docstring.
- The frozen copy has uncommitted changes against 2eeae04: R6–R8 docstring, r7 and r8 selftest cases (23 = 14 frozen + 9 refinement), the R8 symlinked-parent `unsafe` branch, fleet-root `realpath` plus directory check, the `filename:` label, and the new error text. The worktree is not committed.
- `corpus/lessons/round-20.md:33–39` says "Eight refinement selftest cases" and lists R1–R5, missing-taskCall and r7. R8 is not disclosed. `corpus/knowledge/wave-settlement-r20.md:22` says "14 frozen + 8 refinement cases"; the frozen copy has 9. Knowledge line 34 does document the symlinked-parent rule.
- Totals double count byte-identical dispatch copies: `totals.missing` 108 is 63 unique report paths on this lane. Consumers must dedupe via `duplicate_of`.

## 6. Commands and exit codes

- Live scan: `python3 tools/mori-wave-settlement.py scan --lane-root …/tameshi-shokunin --fleet-root …/shokunin --out …/falsify/LiveTameshi/scan.json` → rc 1 (5 partial waves, the expected observation exit). Re-run: `cmp` identical.
- Committed 2eeae04 scan (scratch tree with copied frozen oracle): `cmp` identical to scan.json, 2 runs. Selftest 21/21 PASS, rc 0.
- Frozen copy (`tool-snapshot.py`): selftest 23/23 PASS, rc 0. Scan vs scan.json: structural diff = 1 (D1). Code diff vs HEAD: `falsify/LiveTameshi/tool-vs-HEAD.diff`.
- Git (read-only): `git cat-file -p HEAD:tools/mori-wave-settlement.py | sha256sum` → `c6e6…`; `git log -3 -- tools/mori-wave-settlement.py` → 2eeae04 only.

## 7. Limits

- The oracle was written from the frozen contract and never imports the tool. It reproduces the GT rows, so a shared misreading of the spec would go unseen. [INFERENCE: low risk]
- GT's basename sweep of the fleet (F6) was not re-run; fleet-wide grep is out of bounds. The misroot check here covers the same relative path under the fleet root, as specified.
- The snapshot does not record its tool version. It was written 16 seconds before commit 2eeae04 and its lane totals match HEAD's output. [INFERENCE: produced by the pre-commit tool]
- The tool changed four times during this audit. If the worktree moves again, §6 must be re-run before citing these results.

## 8. Recommendations for the L1

1. Commit or revert the worktree changes and record the tool sha256 in the snapshot.
2. Make "no waves discovered" a distinct state, not exit 0, or annotate it in the fleet snapshot.
3. Reject a trailing slash as non-file, and decide explicitly whether CRLF or trailing-space stub variants count as `stub`.
4. Report an unreadable leaf as `unavailable`, not `missing`, or document it in the lesson.
5. Disclose R8 in the lesson, correct the knowledge-note counts, and fix the HEAD docstring (64 vs 16 bytes).
6. Cite unique counts (893 / 830 / 63) next to the 965 / 857 / 108 totals.

Installs or updates: none.
