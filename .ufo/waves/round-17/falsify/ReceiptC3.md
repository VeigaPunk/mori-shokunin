# ReceiptC3 — round-17 wave-2 recount of the exact-r16 C3 sweep receipts

Seat: `MoriR17.ReceiptC3-4` (scout, leaf). Scope: **recount only** the committed C3
legacy/default sweep manifests against the byte-exact r16 artifact; no rerun of the sweep or
selftest, no VCS mutation, no edits outside this report. Lane root
`/home/vgpnk/Projects/shokunin/mori-shokunin`; HEAD at audit `5c1dfb8d0530c74eb0e1630c2b522b735b486274`.

Verdict: **the declared missed-known-artifact count reproduces exactly as 1→0, and the
committed receipts do not treat the sibling control as ownership.** One reproducibility
limitation survives (receipts record size/path but not the scanned-file digest, and the
measurement sandbox was removed mid-audit); it does not falsify the counted unit because the
artifact bytes are pinned independently by Git blob identity and the committed witness.

## 1. Receipts recounted (all committed at HEAD)

| Receipt | argv (abridged) | rc | Parsed result |
|---|---|---|---|
| `.ufo/waves/round-17/evidence/c3-before.json` | `python3 tools/mori-misroot-sweep.py --fleet-root .../MainChecks/c3-fleet --lane mori --round 16 --legacy-pathspec .ufo/waves --legacy-pathspec .ufo/reports` | 0 | `MORI_MISROOT_CLEAN`, `candidate_count=0`, `scan.untracked_entries=0`, `regular_files=0`, `bytes_read=0`, `repo_root`=sandbox |
| `.ufo/waves/round-17/evidence/c3-after.json` | same, **no** pathspec | 1 | `MORI_MISROOT_CANDIDATE`, `candidate_count=1`, candidate `{path:"MoriR16.Lesson", matched_in:["path"], size_bytes:847, read_bytes:847, truncated:false}`, `scan.untracked_entries=2`, `regular_files=2`, `bytes_read=876` |
| `.ufo/waves/round-17/evidence/count-c3.json` | `jq -s '[.[] \| (.stdout\|fromjson) \| 1 - ([.candidates[]\|select(.path=="MoriR16.Lesson")]\|length)]' c3-before.json c3-after.json` | 0 | stdout `[1, 0]`; Python recount of the same expression = `[1, 0]` |

Chronology: before `16:34:52.901`, after `16:34:52.934` (33 ms apart, same sandbox), count
`16:35:15`; `PINNED_INPUTS.json:5` observed `16:35:35`. The receipts' `stdout_sha256` values
recompute exactly for all three (`67153f7d…`, `f3cc4e9c…`, `fed77b69…`), so the stored stdout
strings were not edited after digesting.

The before `git_command` ends `… --untracked-files=all -- .ufo/waves .ufo/reports`; the after
`git_command` ends `… --untracked-files=all`. That is the r16 addendum pathspec
(`corpus/lessons/round-16-verifier-spotcheck.md:206-208`) versus the no-pathspec default.
`repo_root` equals `fleet_root` in both, so `git -C` did not adopt the enclosing lane repo.

Contradiction with the round-17 lesson table? None: `corpus/lessons/round-17.md:114` prints the
same command and `[1,0]`; `PINNED_INPUTS.json:32-36` declares C3 `before:1`, `after:0`, unit
"missed known exact root artifact assertions". Both match the recount.

## 2. Artifact identity: frozen bytes vs archived fleet original

| Copy | Size | SHA-256 | Git blob |
|---|---|---|---|
| Archived fleet original `/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/misroots/MoriR16.Lesson` | 847 | `15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e` | `cd635a3e3a12315056ee56cb1cd730de80e6adcb` (fleet repo, `ac0a7fc`, 2026-10-20 06:30:51 -0300) |
| Committed frozen `.ufo/waves/round-17/frozen/MoriR16.Lesson` | 847 | same | same `cd635a3e…` at `273aa74` **and** HEAD |
| Tool-embedded archive (`tools/mori-misroot-sweep.py:349,384`) | 847 | same | n/a — decoded bytes compare equal to the frozen file |
| Measurement sandbox copy (observed live at audit start; since removed) | 847 | same; `cmp` equal to both | n/a — regular file, mode 644, inode 43609080 vs frozen 43533258 (a copy, not a symlink/hardlink) |

Commands/results:

```
$ cmp -s <archive> <frozen>; echo $?            -> 0
$ sha256sum <archive> <frozen>                  -> 15f9f82d…5510e for both, 847 bytes each
$ git -C /home/vgpnk/Projects/shokunin ls-files -s .ufo/waves/hyaku/misroots/
  100644 cd635a3e… 0  .ufo/waves/hyaku/misroots/MoriR16.Lesson
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree 273aa74 -- .ufo/waves/round-17/frozen/MoriR16.Lesson
  100644 blob cd635a3e…  .ufo/waves/round-17/frozen/MoriR16.Lesson
```

Equal Git blob SHA-1s across two repositories prove byte identity; `cd635a3e…` is the same
object hash in the fleet archive and the lane frozen file. The fleet archive is tracked and
clean (`git status -- .ufo/waves/hyaku/misroots/` empty) and was committed at 06:30, ten hours
before the C3 measurement, so it is not a round-17 artifact.

The committed witness `.ufo/waves/round-17/frozen/c3-expected.json` pins `bytes:847`,
`sha256:15f9…`, `legacy_expected_detected:false`, `default_expected_detected:true`,
`default_expected_matched_in:["path"]`, `sibling_control:"TabiR16.Lesson"`; every field agrees
with the receipts. It entered in `5c1dfb8` (the receipts commit), not at measured commit
`273aa74`; it is not listed in `PINNED_INPUTS.json`, while the frozen artifact is
(`PINNED_INPUTS.json:15`).

The artifact is genuinely filename-only for this matcher: applying the tool's own compiled
regexes (`_lane_pattern`, `_round_pattern`, `mori-misroot-sweep.py:149,156`) to the frozen
bytes gives `lane_on_content=False`, `round_on_content=False`, while both match the path
`MoriR16.Lesson`. The artifact body is the r16 BootContinuity disclosure described at
`corpus/lessons/round-16-verifier-spotcheck.md:202-205`; it names neither lane nor round in
content. This is the "exact archived filename-only artifact", not a convenient synthetic body.

The hermetic selftest receipt (`evidence/misroot-selftest.json`) independently reports
`fixture_bytes:847`, `fixture_sha256:15f9…`, `planted_found_with_legacy_pathspec:false`,
`planted_found_without_pathspec:true`, `planted_matched_in:["path"]`,
`sandbox_unchanged:true`, rc0; its `stdout_sha256` recomputes exactly.

## 3. Missed-known-artifact 1→0 and sibling/control handling

- The counter is `1 - (number of candidates whose path is exactly "MoriR16.Lesson")`, evaluated
  per manifest. Before: empty candidate list → 1. After: one exact-path candidate → 0.
  Recomputed from the committed JSON as `[1, 0]`.
- The counter **cannot be improved by emitting a sibling**: it filters on the known path only.
  If the default run had claimed only `TabiR16.Lesson` and missed the known artifact, the
  expression would still be 1. So 1→0 is not sibling-derived.
- The after receipt shows the sibling was nevertheless exercised, not ignored:
  `untracked_entries=2`, `regular_files=2`, `bytes_read=876 = 847 + 29`, `unreadable=0`,
  `non_regular_skipped=0`, `candidate_count=1`. The second untracked file was read (29 bytes)
  and not emitted. At audit start the sandbox listing identified the two untracked entries as
  `MoriR16.Lesson` (847 B) and `TabiR16.Lesson` (29 B); the latter is lane `tabi`, not `mori`,
  so it cannot match the lane predicate by path, and the receipt proves it did not match by
  content either (it was not emitted). The committed witness names the same sibling
  (`c3-expected.json`), so the identity is durable even though its bytes are not.
- Tracked control: the sandbox also contained `seed` (5 B). A `git status --porcelain` at audit
  start listed only the two `??` entries above, so `seed` was tracked/ignored and excluded from
  the untracked scan; `regular_files=2` confirms only the two untracked files were inspected.
  The receipt does not name `seed`; this part rests on the live directory/status observation.
  An **untracked, post-measurement** `.ufo/waves/round-17/c3-capture-recipe.json`
  (mtime `16:47:24`, not in any commit) describes the same inventory: `seed\n` (5 B), sibling
  `TabiR16.Lesson` = `Tabi round16 sibling control\n` (29 B), artifact copied from the frozen
  847-B file. It matches my live sizes and the `876 = 847 + 29` arithmetic, but it was authored
  after the run and is not measurement evidence; I did not execute its setup/argv steps.
- Setup cannot masquerade as the measured improvement: a `MORI_MISROOT_SETUP` payload has no
  `candidates` key, so the jq expression would yield `1`, not `0`. In this evidence the before
  payload is rc0 `MORI_MISROOT_CLEAN` with a full `scan` block, i.e. a real pathspec miss, not a
  setup failure.

## 4. Falsification attempts and outcomes

| Attempt | Result |
|---|---|
| Substitute a synthetic content-bearing fixture for the exact artifact | Rejected: artifact content has zero lane/round tokens under the tool's own regexes; match is path-only. |
| Show the legacy pathspec would have found a root-level untracked file | Rejected empirically on the same sandbox 33 ms apart: 0 untracked under `.ufo/waves .ufo/reports`, 2 without. `repo_root` is the sandbox, so this is not a wrong-repo artifact. The real fleet-root legacy run also showed reduced visibility (`build/MisrootSweep.md:143`, 1 vs 9 untracked). |
| Game the counter with a sibling or setup payload | Rejected: exact-path filter; setup yields 1. After candidate list is precision 1/1. |
| Dispute byte correspondence to the archived original | Rejected: fleet archive and lane frozen file share blob `cd635a3e…` (847 B, SHA-256 `15f9…`); `cmp` equal; tool-embedded bytes equal; the sandbox copy I statted before removal also matched. |
| Replay the exact argv from the receipt | **Not possible now**: `…/.ufo/worktrees/round-17/MainChecks/c3-fleet` is absent (`.ufo/worktrees/round-17` mtime `16:47:43 -0300`), and the receipts record `size_bytes`/`read_bytes` but no artifact digest. Teardown is not recorded in `LOG.md` or the wave records (grep empty). This is a durability gap, not a contradiction of the recorded run. |

## 5. Residual unknowns

1. Measurement-time byte equality of the sandbox copy is inferred from a post-measurement
   stat/hash/cmp observation plus the file's `16:34` mtime; the receipt itself carries no digest.
   Confidence high, but the proof is the committed blob identity plus the observation, not the
   receipt alone. [INFERENCE for the instant of measurement]
2. Single archived original: no independent non-archive copy of the r16 fleet-root file exists
   to cross-check; provenance rests on the r16 open-queue statement and the fleet commit
   `ac0a7fc` predating round 17. [INFERENCE that the archive is faithful]
3. The sibling `TabiR16.Lesson` bytes and the tracked `seed` bytes are not retained in any
   committed receipt. The untracked post-hoc `c3-capture-recipe.json` states their exact bytes
   (29 B and 5 B, matching the live sizes and receipt arithmetic), but it postdates the run and
   is not a witness of it.
4. Git version/environment of the measurement is not recorded; C3's result does not depend on a
   feature newer than plain `git status --porcelain=v1 -z --untracked-files=all`.
5. Receipts were committed one commit after the measured commit (`5c1dfb8` is a direct child of
   `273aa74`); the tool and frozen artifact exist at `273aa74` with the pinned blobs, so
   `measured_commit` denotes tool/frozen state, not receipt storage.

## 6. Discipline

No installs/upgrades; no pacman/uv/npm/cargo; no network; no `/tmp` writes; no background jobs;
no VCS mutation; no rerun of the sweep, selftest, gates or any live probe. Only read-only
commands (`read`, `grep`, `stat`, `sha256sum`, `cmp`, `git ls-tree/ls-files/status/log`,
read-only `jq`/Python JSON recomputation, and importing the pinned tool to invoke its regexes
and `_archive_bytes`). That import created `tools/__pycache__/mori-misroot-sweep.cpython-314.pyc`
as a bytecode side effect; it was removed in the same audit, and `tools/__pycache__` is again
absent. One file retained: this report. The exact attacked
scope is the C3 recount above; this is not a blanket pass on C1, C2 or the C3 prose beyond the
counted unit.
