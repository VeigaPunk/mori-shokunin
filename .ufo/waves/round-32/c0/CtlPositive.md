# CtlPositive — three-format positive control and one R5 mutation

## 1. Control and skipped work

**Verdict: positive control passed; C1 unmet as expected.** Three live rows passed: S002 (kernel HTML), S051 (NIST PDF), S117 (GitHub JSON). The control omits the other 31 population rows and any new-source admission. Evidence: the five complete live-counter outputs below; frozen predicate at `.ufo/waves/round-32/count-c1.py:6-37`.

Axes: freshness (live bytes), coverage (three page kinds and each R5 dependency), calibration (explicit source and reviewer limits). This is sandbox control evidence, not lane data or an independent reviewer judgment.

Mutant: change only S002's verdict from `current` to `drifted`, refreshing the judge section hash to isolate R5, but omit every used-by correction. Expected detector: S002 fails R5 with three path-specific `no_correction` findings while S051/S117 remain valid. **Killed at the row-check level**: pristine/restored S002 passes; mutant S002 fails. Global exit 1 is expected for every incomplete control and is not itself mutation-kill evidence.

## 2. Exact construction

Sandbox: `/fast/scratch/hyaku/mori-r32/CtlPositive/lane`. Below, `S=/fast/scratch/hyaku/mori-r32/CtlPositive`, `L=$S/lane`, `C=/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/count-c1.py`. Commands are shown with these path abbreviations; every subprocess used the displayed timeout and 2 GiB address-space cap.

```sh
timeout 120 prlimit --as=2147483648 -- mkdir -p "$S"
timeout 120 prlimit --as=2147483648 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks /home/vgpnk/Projects/shokunin/mori-shokunin "$L"
timeout 120 prlimit --as=2147483648 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C "$L" checkout -q 29f7d04355f17b5d45d6e00c40e2a5c3e5a2c9c4
timeout 120 prlimit --as=2147483648 -- mkdir -p "$L/corpus/evidence/recheck-r32"
timeout 120 prlimit --as=2147483648 -- curl -sSL --fail --max-time 60 --output "$L/corpus/evidence/recheck-r32/S002.src" --write-out 'S002 http=%{http_code} bytes=%{size_download} url=%{url_effective}\n' https://docs.kernel.org/admin-guide/cgroup-v2.html
timeout 120 prlimit --as=2147483648 -- curl -sSL --fail --max-time 60 --output "$L/corpus/evidence/recheck-r32/S051.src" --write-out 'S051 http=%{http_code} bytes=%{size_download} url=%{url_effective}\n' https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf
timeout 120 prlimit --as=2147483648 -- curl -sSL --fail --max-time 60 --output "$L/corpus/evidence/recheck-r32/S117.src" --write-out 'S117 http=%{http_code} bytes=%{size_download} url=%{url_effective}\n' https://api.github.com/repos/rfjakob/earlyoom/tags
timeout 120 prlimit --as=2147483648 -- pdftotext -layout "$L/corpus/evidence/recheck-r32/S051.src" "$S/S051.txt"
```

Fetch stdout, verbatim:
```text
S002 http=200 bytes=172967 url=https://docs.kernel.org/admin-guide/cgroup-v2.html
S051 http=200 bytes=818516 url=https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-122.pdf
S117 http=200 bytes=13409 url=https://api.github.com/repos/rfjakob/earlyoom/tags
```

`timeout 120 prlimit --as=2147483648 -- date -u +%Y-%m-%dT%H:%M:%SZ` after the fetches printed `2026-10-23T01:12:49Z`, the accessed value used. No fetched bytes were edited. Existing `pdftotext -v` reported `26.08.0`; no tool was installed or updated.

Files were created with `functions.write`: exact positive fixture bytes are committed at `42769eadc4cb33f325140f7d8b3b4fe911ee47be:corpus/lessons/round-32.md:1-13`, `.ufo/waves/round-32/positive-control-dispatch.json:1-10`, and `.ufo/waves/round-32/judge/JudgeRecheck.md:1-11`. The dispatch names `MoriR32A2.CtlPositive` with agent `reviewer`; the receipt explicitly says synthetic control, names the exact Recheck hash and agrees with the three ids.

Quote locations: S002.src:1409-1410 and :1420-1421; NIST section 4.2.1 printed p. 4-3 (`$S/S051.txt:1250-1251`) and ES-2 (`:260`); S117.src:3-4 and :6-8. PDF extraction and escaped JSON quotes passed R2/R3; no honest row failed normalization. S117 supports the v1.9.0 tag/commit provenance only, not its teaches cell's code-grammar or percentage claims; the lesson and synthetic receipt explicitly preserve this limit.

Section hashes were generated with `timeout 120 prlimit --as=2147483648 -- python3 "$C" --section-sha "$L/corpus/lessons/round-32.md"`: positive `9bb8997eab919f9e052ec80b53f6c01c89b9e3c1aeec5c17801e8239327e460d`; drifted `be703c5c43e8eb17c86f2d7d3f7ea02ea924cf4c715c38d56123c74cb338cf79`.

Each commit used the command form below, with only the explicit paths changed in that stage staged by the corresponding `git add -- <paths>` command. No lane/fleet git writes or pushes occurred.
```sh
timeout 120 prlimit --as=2147483648 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C "$L" add -- <stage paths>
timeout 120 prlimit --as=2147483648 -- env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C "$L" -c user.name=ctl -c user.email=ctl@sandbox commit -m '<subject below>'
```

## 3. Commits and precise mutation sequence

| State | Commit | Commit subject and exact file operation |
|---|---|---|
| Pristine positive | `42769eadc4cb33f325140f7d8b3b4fe911ee47be` | `control: three live HTML PDF JSON recheck rows`; add the three `.src` files, lesson, synthetic receipt, dispatch above |
| Missing corrections | `664e5d3f12ce785ccf3cfb7226d2b24fdce3d5ce` | `control: mark S002 drifted without used-by corrections`; `functions.edit` lesson line 11 final cell to `drifted`, receipt line 7 to drifted section hash |
| One of three | `f8fbfd86fb881f10bde7856dffdc86fc8aa73d3b` | `control: add R5 line to one of three used-by entries`; append blank line + exact marker below to `corpus/knowledge/oom-kill-counter-kernel-only-r12.md:34-35` |
| Three of three | `5b8409474f9491533e0a3cccceae51146d659e68` | `control: add R5 line to every S002 used-by entry`; append identical blank + marker to `corpus/knowledge/userspace-oom-killers-r12.md:34-35` and `corpus/knowledge/journal-alarm-routing-r14.md:392-393` |
| Restored | `ad290ce2167ca282cebf548a7de0f4e3993f410b` | `control: restore exact pristine positive bytes`; restore lesson/receipt lines and cut the three appended blank+marker pairs |

Exact appended marker: `Round32 S002 control-only: this sandbox marks the row drifted to exercise R5; no source drift is asserted.`

## 4. Frozen live counter stdout and exit codes

Every run used the unchanged lane counter, from cwd `/home/vgpnk/Projects/shokunin/mori-shokunin`, with the exact command form `timeout 600 prlimit --as=2147483648 -- python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-32/count-c1.py <full-commit-below> --repo /fast/scratch/hyaku/mori-r32/CtlPositive/lane`. No `--no-live` run was used.

Pristine positive — full stdout:
```text
revision=42769eadc4cb33f325140f7d8b3b4fe911ee47be base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=3 header_ok=True section_sha256=9bb8997eab919f9e judge_ok=True judge_seat_ok=True judge_agree=3
rows_ok=3/34 verdicts={'current': 3}
row_failures=S001:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
```
Exit code: `1`.

Missing corrections — full stdout:
```text
revision=664e5d3f12ce785ccf3cfb7226d2b24fdce3d5ce base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=3 header_ok=True section_sha256=be703c5c43e8eb17 judge_ok=True judge_seat_ok=True judge_agree=3
rows_ok=2/34 verdicts={'current': 2, 'drifted': 1}
row_failures=S001:rows=0 S002:no_correction:corpus/knowledge/oom-kill-counter-kernel-only-r12.md,no_correction:corpus/knowledge/userspace-oom-killers-r12.md,no_correction:corpus/knowledge/journal-alarm-routing-r14.md S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
```
Exit code: `1`.

One of three corrections — full stdout:
```text
revision=f8fbfd86fb881f10bde7856dffdc86fc8aa73d3b base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=3 header_ok=True section_sha256=be703c5c43e8eb17 judge_ok=True judge_seat_ok=True judge_agree=3
rows_ok=2/34 verdicts={'current': 2, 'drifted': 1}
row_failures=S001:rows=0 S002:no_correction:corpus/knowledge/userspace-oom-killers-r12.md,no_correction:corpus/knowledge/journal-alarm-routing-r14.md S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
```
Exit code: `1`.

Three of three corrections — full stdout:
```text
revision=5b8409474f9491533e0a3cccceae51146d659e68 base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=3 header_ok=True section_sha256=be703c5c43e8eb17 judge_ok=True judge_seat_ok=True judge_agree=3
rows_ok=3/34 verdicts={'current': 2, 'drifted': 1}
row_failures=S001:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
```
Exit code: `1`.

Restored positive — full stdout:
```text
revision=ad290ce2167ca282cebf548a7de0f4e3993f410b base=641a6e86ecc60634d215c0a47ab86c47661abf86 population=34 pop_sha256=4426b6501a01c07b
recheck_rows=3 header_ok=True section_sha256=9bb8997eab919f9e judge_ok=True judge_seat_ok=True judge_agree=3
rows_ok=3/34 verdicts={'current': 3}
row_failures=S001:rows=0 S007:rows=0 S012:rows=0 S014:rows=0 S015:rows=0 S031:rows=0 S037:rows=0 S039:rows=0 S040:rows=0 S041:rows=0 S043:rows=0 S044:rows=0 S045:rows=0 S046:rows=0 S047:rows=0 S049:rows=0 S052:rows=0 S056:rows=0 S058:rows=0 S062:rows=0 S064:rows=0 S067:rows=0 S068:rows=0 S069:rows=0 S071:rows=0 S073:rows=0 S074:rows=0 S076:rows=0 S128:rows=0 S137:rows=0 S149:rows=0
new_ok=0 new_failures=none
C1=unmet exit=1
```
Exit code: `1`.

## 5. Verdict and restoration evidence

R5 requires **every** used-by knowledge entry: missing all produced three failures; adding one removed precisely that path's failure; adding the other two restored `rows_ok=3/34`. The new-source check remained unmet by design. This is neither a full C1 pass nor a baseline C1 failure misreported as a killed mutant.

Actual SHA-256 outputs from `timeout 120 prlimit --as=2147483648 -- sha256sum <absolute-paths>` before mutation, during construction, and after restoration. Mutated lesson/receipt hashes were measured at the missing-correction stage; each knowledge hash was measured immediately after its marker append:

| Path relative to sandbox | Pristine SHA-256 | Mutated-byte SHA-256 | Restored SHA-256 |
|---|---|---|---|
| corpus/lessons/round-32.md | bd802aee946c97c8d5d987e7dbd9dcfa245e1a054b7bad618a46e3a52ccf5376 | cbdf50d23252ef9e3225a3d90724aa09dbc5540f27550dbff43208ce3fc0a47d | bd802aee946c97c8d5d987e7dbd9dcfa245e1a054b7bad618a46e3a52ccf5376 |
| .ufo/waves/round-32/judge/JudgeRecheck.md | beef3019f67bcd61192cf094e672822e9b578cae9b1fe6480dcbaa584546474f | 938f4626c746f3bcbead1bd2957ce11971ad70f7daf24e677d88bed3e43147ea | beef3019f67bcd61192cf094e672822e9b578cae9b1fe6480dcbaa584546474f |
| corpus/knowledge/oom-kill-counter-kernel-only-r12.md | 712db7c6f35fdd4ead745773061dfeec4445fdadaa015b8f0214b2d0439f0654 | 40406f37bd12a7c428a1d77180dfaca0bb956d58cb3fdf1f1f1e041b297a21e1 | 712db7c6f35fdd4ead745773061dfeec4445fdadaa015b8f0214b2d0439f0654 |
| corpus/knowledge/userspace-oom-killers-r12.md | aab7c0b81f6f231e1bb18892c98ea6c7d15205982e69720b29b8f3f487bc5e20 | d7d2ba39a09de5852dfd72d66cbf8e80ec7309daff8f3a3eb163baace226613d | aab7c0b81f6f231e1bb18892c98ea6c7d15205982e69720b29b8f3f487bc5e20 |
| corpus/knowledge/journal-alarm-routing-r14.md | a40c5796c332f6b930b8f2260c828b2d06b80b43ee246a782ea146912678d841 | ea935eae231dadc5f1d021d8705512e8352ee29338ffa12f38ec825d40788105 | a40c5796c332f6b930b8f2260c828b2d06b80b43ee246a782ea146912678d841 |

The initial and restored `git rev-parse <commit>^{tree}` outputs both equal `7a7f181b393b0654647de923cb2542b34e54634e`, proving exact tracked-tree restoration. The unchanged source hashes before/after were S002 `b478c1bae99899df476d6b4989cbb516f7ca93c5f009cdff64b802bbc24f3d4b`, S051 `555b9df82af12de4ca887efc21c0a9e159a14485d5d570f44b32ef15c6c62470`, S117 `423c43617a2a299315180292f43447936f6ddde01efff5baece3fc46ed8b1869`. The unchanged lane counter hash before/after was `cfa0b988a51fc59720382016c0608408c022b9aaedc19f92c24453493d1a84fe`.

## 6. Counter limits and reproducer

R5 is a marker check, not a substantive correction review: the exact control-only sentence above, explicitly asserting no source drift, satisfies it in each path. Reproducer: run the frozen live command against `664e5d3f12ce785ccf3cfb7226d2b24fdce3d5ce`, then `f8fbfd86fb881f10bde7856dffdc86fc8aa73d3b`, then `5b8409474f9491533e0a3cccceae51146d659e68`; outputs above show the exact per-path transition. This matches the declared code-level R5 (`count-c1.py:256-260`), not a contradiction of P-C1. S117 also illustrates that lexical quote relevance is weaker than proving its entire teaches cell (`:250-252`). The synthetic R4 receipt/dispatch exercises the contract's already declared trust limit (`contract.md:63-65`); it is not evidence that an actual non-author review occurred.

All five counter calls were synchronous and completed; no background jobs, services, other runtime, source-registry changes or lane commits were started by this seat.
