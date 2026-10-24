# CountC3 — independent read-only receipt recount

## Scope and result

I independently recounted the retained C3 probe receipts and the wave-2 context-check receipts. I did not rerun the sweep, context checker, gate, selftests, or any build/test/lint command. C3's retained evidence supports **one missed known artifact before the no-pathspec sweep and zero afterward**. The context receipts record a 12-clause fail (`transcript_fields_only`) followed by a pass; the corrected spec hash matches the current `wave2-spec.json`.

## C3 missed-known-artifact count

`PINNED_INPUTS.json:31-36` defines the C3 counter as missed known exact root artifact assertions, before `1`, after `0`, via `evidence/count-c3.json`. The original captured probe commands and return codes (`evidence/c3-before.json:5-28`, `evidence/c3-after.json:5-24`) are:

```text
python3 tools/mori-misroot-sweep.py --fleet-root /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MainChecks/c3-fleet --lane mori --round 16 --legacy-pathspec .ufo/waves --legacy-pathspec .ufo/reports
rc=0
```

Its exact captured stdout was:

```json
{"candidate_count": 0, "candidates": [], "detection_only": true, "finding": "MORI_MISROOT_CLEAN", "fleet_root": "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MainChecks/c3-fleet", "git_command": ["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MainChecks/c3-fleet", "status", "--porcelain=v1", "-z", "--untracked-files=all", "--", ".ufo/waves", ".ufo/reports"], "lane": "mori", "legacy_pathspec": [".ufo/waves", ".ufo/reports"], "moves_or_deletes": false, "repo_root": "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MainChecks/c3-fleet", "round": 16, "scan": {"bytes_read": 0, "non_regular_skipped": 0, "read_cap": 65536, "regular_files": 0, "truncated_files": 0, "unreadable": 0, "untracked_entries": 0}, "schema": "mori-misroot-sweep-v1"}
```

```text
python3 tools/mori-misroot-sweep.py --fleet-root /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MainChecks/c3-fleet --lane mori --round 16
rc=1
```

Its exact captured stdout was:

```json
{"candidate_count": 1, "candidates": [{"class": "candidate_misroot", "matched_in": ["path"], "path": "MoriR16.Lesson", "read": "content", "read_bytes": 847, "size_bytes": 847, "truncated": false}], "detection_only": true, "finding": "MORI_MISROOT_CANDIDATE", "fleet_root": "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MainChecks/c3-fleet", "git_command": ["git", "--no-optional-locks", "-c", "core.fsmonitor=false", "-C", "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MainChecks/c3-fleet", "status", "--porcelain=v1", "-z", "--untracked-files=all"], "lane": "mori", "legacy_pathspec": null, "moves_or_deletes": false, "repo_root": "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/worktrees/round-17/MainChecks/c3-fleet", "round": 16, "scan": {"bytes_read": 876, "non_regular_skipped": 0, "read_cap": 65536, "regular_files": 2, "truncated_files": 0, "unreadable": 0, "untracked_entries": 2}, "schema": "mori-misroot-sweep-v1"}
```

Independent recount command (the same expression is retained in `evidence/count-c3.json:5-21`):

```sh
jq -s '[.[] | (.stdout|fromjson) | 1 - ([.candidates[]|select(.path=="MoriR16.Lesson")]|length)]' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/c3-before.json /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/c3-after.json
```

Observed rc `0`; exact stdout:

```json
[
  1,
  0
]
```

The after-probe's rc `1` is its recorded `MORI_MISROOT_CANDIDATE` finding, not a recount failure. The counted match is path-only, exactly `MoriR16.Lesson`; the candidate list has no sibling candidate. The frozen expectation (`frozen/c3-expected.json:2-13`) pins the 847-byte witness SHA-256 `15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e`, with `TabiR16.Lesson` as the sibling negative control.

## Pre-dispatch context fail → pass

Independent receipt projection command:

```sh
jq -s '[.[] | {finding_id,missing:(.missing // []),contexts_failing:(.contexts_failing // 0),clauses_checked,spec_sha256}]' /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/context-check-wave2-original.json /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence/context-check-wave2.json
```

Observed rc `0`; exact stdout:

```json
[
  {
    "finding_id": "CONTEXT_MISSING",
    "missing": [
      "transcript_fields_only"
    ],
    "contexts_failing": 1,
    "clauses_checked": 12,
    "spec_sha256": "a38b6b9294a7d7a095a922d1c8a7854a2f9c1ce311a2ede2554fe384a195c9e0"
  },
  {
    "finding_id": "CONTEXT_OK",
    "missing": [],
    "contexts_failing": 0,
    "clauses_checked": 12,
    "spec_sha256": "6a2dc375e6131ac4c3b2fb342979ff920048e3ee0be9d295237b68ff6760cd2e"
  }
]
```

The two receipt JSON objects themselves have no invocation `argv` or `rc` fields. Per `tools/mori-round17-context-check.py:58-64`, `CONTEXT_MISSING` maps to rc `1` and `CONTEXT_OK` maps to rc `0`; `corpus/lessons/round-17.md:162-164` independently records the original rc1 → corrected rc0 as caught before dispatch. Both are static checks only (`claims_runtime_prevention: false` in the receipts); this is not runtime prevention evidence.

[INFERENCE] I found no retained pre-correction spec bytes in the searched round-17 artifacts; that old digest cannot be independently recomputed from the available input bytes.

## SHA correspondence and provenance

Read-only Python recomputation of the three C3 captured-stdout digests returned rc `0` and:

Exact Python command:

```sh
python3 -c 'import hashlib,json,pathlib; d=pathlib.Path("/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/evidence"); names=["c3-before.json","c3-after.json","count-c3.json"]; print(json.dumps([{ "file":n,"computed":hashlib.sha256(x["stdout"].encode()).hexdigest(),"recorded":x["stdout_sha256"],"match":hashlib.sha256(x["stdout"].encode()).hexdigest()==x["stdout_sha256"]} for n in names for x in [json.loads((d/n).read_text())]],sort_keys=True,separators=(",",":")))'
```


```json
[{"computed":"67153f7d55fa2e60ecd52681e4ea1631ff3bd8385ec8d79cb6e3114acba60be3","file":"c3-before.json","match":true,"recorded":"67153f7d55fa2e60ecd52681e4ea1631ff3bd8385ec8d79cb6e3114acba60be3"},{"computed":"f3cc4e9c38e6b28818d2b3e47f3cac590169b8be6e348968e61a1225b9ccdf1b","file":"c3-after.json","match":true,"recorded":"f3cc4e9c38e6b28818d2b3e47f3cac590169b8be6e348968e61a1225b9ccdf1b"},{"computed":"fed77b69fa758c3e1d311d5e2b28467858e67448bdcccc9eed143246629d9c8a","file":"count-c3.json","match":true,"recorded":"fed77b69fa758c3e1d311d5e2b28467858e67448bdcccc9eed143246629d9c8a"}]
```

The pinned witness hash and byte count also correspond: `sha256sum` of `frozen/MoriR16.Lesson` is `15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e` (847 bytes), matching both `PINNED_INPUTS.json:15` and `frozen/c3-expected.json:4-5`. `sha256sum` of `wave2-spec.json` is `6a2dc375e6131ac4c3b2fb342979ff920048e3ee0be9d295237b68ff6760cd2e`, matching the passing context receipt.

Exact command (`rc 0`):

```sh
sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/frozen/MoriR16.Lesson /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/wave2-spec.json
```

Exact stdout:

```text
15f9f82d707d5c79b11643eed1ab4754b6959d2bede5887e07364442ada5510e  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/frozen/MoriR16.Lesson
6a2dc375e6131ac4c3b2fb342979ff920048e3ee0be9d295237b68ff6760cd2e  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-17/wave2-spec.json
```


I compared working-tree SHA-256 bytes with `git show HEAD:<path>` for the nine scoped evidence/input files (PINNED_INPUTS, count-c3, c3-before, c3-after, both wave-2 context receipts, frozen witness, frozen C3 expectation, and wave2-spec). The read-only Python command returned rc `0` and exact stdout `{"files_checked":9,"head":"5c1dfb8d0530c74eb0e1630c2b522b735b486274","mismatches":[]}`. Thus those current files match the committed blobs at current HEAD.

Exact Python command:

```sh
python3 -c 'import hashlib,json,pathlib,subprocess; r=pathlib.Path("/home/vgpnk/Projects/shokunin/mori-shokunin"); ps=[".ufo/waves/round-17/PINNED_INPUTS.json",".ufo/waves/round-17/evidence/count-c3.json",".ufo/waves/round-17/evidence/c3-before.json",".ufo/waves/round-17/evidence/c3-after.json",".ufo/waves/round-17/evidence/context-check-wave2-original.json",".ufo/waves/round-17/evidence/context-check-wave2.json",".ufo/waves/round-17/frozen/MoriR16.Lesson",".ufo/waves/round-17/frozen/c3-expected.json",".ufo/waves/round-17/wave2-spec.json"]; bad=[p for p in ps if hashlib.sha256((r/p).read_bytes()).digest()!=hashlib.sha256(subprocess.check_output(["git","-C",str(r),"show","HEAD:"+p])).digest()]; print(json.dumps({"head":subprocess.check_output(["git","-C",str(r),"rev-parse","HEAD"],text=True).strip(),"files_checked":len(ps),"mismatches":bad},sort_keys=True,separators=(",",":")))'
```


Provenance boundary: the receipts say `measured_commit` `273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7` (`evidence/c3-before.json:21-22`, `c3-after.json:17-18`, `count-c3.json:14-15`). The read-only tree query below returned only `cd635a3e3a12315056ee56cb1cd730de80e6adcb .ufo/waves/round-17/frozen/MoriR16.Lesson`; the receipt bundle and PINNED_INPUTS are not in that measured-commit tree. They do match committed blobs at current HEAD as described above. I therefore distinguish the probe's recorded measured commit from the later committed receipt bundle.

```sh
git -C /home/vgpnk/Projects/shokunin/mori-shokunin ls-tree -r --format='%(objectname) %(path)' 273aa74ab73701f41fea38ec7bd1c47b4b2bfbc7 -- .ufo/waves/round-17/PINNED_INPUTS.json .ufo/waves/round-17/evidence/count-c3.json .ufo/waves/round-17/evidence/c3-before.json .ufo/waves/round-17/evidence/c3-after.json .ufo/waves/round-17/frozen/MoriR16.Lesson .ufo/waves/round-17/frozen/c3-expected.json
```

`rc=0`; exact stdout: `cd635a3e3a12315056ee56cb1cd730de80e6adcb .ufo/waves/round-17/frozen/MoriR16.Lesson`.

## Limitations

- This recount establishes the retained witness and receipt transition only; it is not independent closure of C3 or of sibling/tracked-control behavior beyond what these captured outputs show.
- No live probe, selftest, build, test, linter, or tool installation was performed.

Report: `.ufo/waves/round-17/falsify/CountC3.md`
