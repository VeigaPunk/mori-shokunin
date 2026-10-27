# Mo52SentHostPaths — portability audit of the round-52 files (round prompt §7 item 4; QUALITY 127)

Seat: sentinel, mori round 52 wave w1. Read-only. Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`, fleet root
`/home/vgpnk/Projects/shokunin`. Data commit `8524904adb25e44f24d9f25aac7eae909625c18c` (DATA), entering tip
`4f266ef2fdf74d8b046f5b4f5a5c4945f65b966d`, lane tip at run time `075436b1346ca659afb8be7a46f0e67e4170aa83`.
Scratch `/fast/scratch/hyaku/mori-r52/Mo52SentHostPaths` (one `git clone --shared` of the lane, 334 MB; removed at
end of run). Disk guard checked before the heavy run: `/fast/scratch/hyaku` 26 % used, 600.4 G free; rc 0.

No file in the lane was written by me except this report. No tool installed or upgraded (nothing needed).

## 1. Mandated grep A — `/home/vgpnk`

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n '/home/vgpnk' 8524904adb25e44f24d9f25aac7eae909625c18c -- .ufo/waves/round-52/
```
83 hit lines in 11 files; per-file counts (`grep -c -F '/home/vgpnk'`):

| file | hits | what the hits are | class |
|---|---|---|---|
| `w1-spec.json` | 67 | generated dispatch record; the seat prompts quote the lane, fleet root and each seat's scratch dir | prose/data |
| `build-w1-spec.py` | 4 | `:46-47` two literal host paths inside the shared seat-rules prose constant (`/home/vgpnk/Projects/shokuknow` read-only rule, `/home/vgpnk/.omp/agent/RULES.md`); `:111,:193` the six bytes `'/home/vgpnk'` used as the *search pattern* of the audit-command text | prose only |
| `evidence/census-start.txt` | 2 | `:1` the literal command, `:25` the resolved-root column of the census output | prose (dated record) |
| `evidence/control-c1-{do-nothing,axes-only,receipts-only,living-only,rewrite-in-place,delete-stale-pins,repeat-stale-tally,witness}.txt` | 1 each (7 files with a hit; `control-c1-witness.txt` also present) | the literal counter command line, `--fleet-repo /home/vgpnk/Projects/shokunin` plus the L1 scratch path — exactly what round-51 routed defect 7 demands | prose (dated record) |
| `count-c1.py`, `count-c2.py`, `controls/c1-controls.py`, `controls/c1-data.py`, `contract.md`, `evidence/{selftest-c1,selftest-c2,sweep-overcommit,freeze-sha256,control-c2-do-nothing}.txt`, `evidence/selftests/*.txt` | 0 | — | — |

No hit is an executable default. `build-w1-spec.py` is the file QUALITY 127 already names as its "shown able to
fail" falsifier, and the two `:46-47` literals are rule prose, not paths any code resolves.

## 2. Mandated grep B — `/tmp`

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -nE 'mkdtemp\(dir="/tmp|/tmp/' 8524904adb25e44f24d9f25aac7eae909625c18c -- .ufo/waves/round-52/
```
2 hit lines, 1 per file:

| file:line | text | class |
|---|---|---|
| `build-w1-spec.py:193` | the audit command's own pattern `mkdtemp\(dir="/tmp\|/tmp/` | prose only |
| `w1-spec.json:324` | the same prompt text, serialised | prose/data |

`git grep -nE 'mkdtemp\(dir=' … -- count-c1.py count-c2.py controls/` → exit 1, no match: **no round-52 instrument
passes `dir=` to `mkdtemp`**, and none carries a `/tmp` or `/var/tmp` default.

## 3. Third class the two mandated greps cannot see (supplementary, same DATA)

```
$ git grep -nE '/fast/|/var/tmp|/usr/bin/|/opt/|/root/|/home/[a-z]' DATA -- .ufo/waves/round-52/count-c1.py .ufo/waves/round-52/count-c2.py .ufo/waves/round-52/controls/
```
Only the four `#!/usr/bin/env python3` shebangs (portable; `PATH`-resolved, not absolute-interpreter).

```
$ for f in $(git ls-tree -r --name-only DATA -- .ufo/waves/round-52/); do n=$(git show DATA:$f | grep -c -F '/fast/'); [ "$n" != 0 ] && echo "$n $f"; done
69 .ufo/waves/round-52/w1-spec.json
 1 .ufo/waves/round-52/build-w1-spec.py
 1 .ufo/waves/round-52/evidence/control-c1-witness.txt   (+ 7 sibling control receipts, 1 each)
 1 .ufo/waves/round-52/evidence/selftests/mori-unlanded-check.txt
```
`build-w1-spec.py:18`: `X = "/fast/scratch/hyaku/mori-r52"` — a module-level constant that is **interpolated into the
scratch directive of every seat prompt** (`build-w1-spec.py:52-56`, `… {X}/{your seat name}/ …`). This is the only
*executable* absolute host path in the round-52 tree, and neither mandated grep reaches it (not `/home/vgpnk`, not
`/tmp`). A spec rebuilt on any other host still tells 68 seats to write under this host's `/fast/scratch`.

The complementary blind spot is layout, not text: both counters resolve their roots **relative to `__file__`**
(`count-c1.py:484`, `count-c2.py:292,301`, `c1-controls.py:13-15`, `build-w1-spec.py:9-11`), which no path grep can
flag. Two of those defaults are wrong off-layout (§4, §5).

## 4. Instrument verdicts (relocated clone, different absolute root)

Clone: `git clone -q --shared <lane> /fast/scratch/hyaku/mori-r52/Mo52SentHostPaths/clone`
(`rev-parse --show-toplevel` = that dir; DATA present; 334 MB).

### count-c1.py — portable (needs one explicit flag)
```
$ TMPDIR=$S/tmp python3 $S/clone/.ufo/waves/round-52/count-c1.py 8524904a… --repo $S/clone --fleet-repo /home/vgpnk/Projects/shokunin --scratch $S/c1
C1=met items=42 axes=6 pins=2 boxes=4 living=7 superseded=4 locators=27 mismatches=0 errors=0 hidden=0 lane_writes=0 manifest=6209bdb8e400 rev=8524904adb25e44f24d9f25aac7eae909625c18c
exit=0   (69.96 s wall)
```
Identical counts, `manifest=` tag and verdict to `evidence/c1-at-data.txt` — only the repo path differs.
`--selftest` from the clone: `C1_SELFTEST pass=42 fail=0`, exit 0 (matches `evidence/selftest-c1.txt`).
Without `--fleet-repo` the same command gives `C1_SETUP cannot resolve manifest`, exit 2 (§5 F5).
TMPDIR is honoured: with `--scratch` omitted the archive base is `tempfile.mkdtemp(prefix="count-c1-r52-")`
(`count-c1.py:504`, no `dir=`) — a faithful micro-probe of that exact call with `TMPDIR=$S/tmp` returned
`/fast/scratch/hyaku/mori-r52/Mo52SentHostPaths/tmp/count-c1-r52-s1bzw3l5`; with an unusable `TMPDIR` stdlib falls
back to `/tmp` (`tempfile.gettempdir()` = `/tmp`), and `count-c1.py:505` refuses any base inside the repo. Writes
nothing into the lane it measures from a relocated repo (`lane_writes=0`).

### count-c2.py — portable
```
$ TMPDIR=$S/tmp python3 $S/clone/.ufo/waves/round-52/count-c2.py --selftest
C2_SELFTEST pass=45 fail=0   exit=0
$ TMPDIR=$S/tmp python3 $S/clone/.ufo/waves/round-52/count-c2.py 8524904a… --repo $S/clone
C2=unmet claims=28 located=28 quote_missing=0 bad_rows=0 sources=5 source_rows=ok pins=ok provenance=ok entailed=0 dissent=0 rev=8524904adb25e44f24d9f25aac7eae909625c18c failed=entailment
exit=1
```
Byte-identical verdict to `evidence/c2-at-data.txt`. No absolute path, no temp file, no `TMPDIR` requirement, no
non-`git` subprocess, no fleet reference (`grep -n fleet count-c2.py` → exit 1). Its `--selftest` reads the five
copies from the working tree through `lane = dirname³(here)` (`count-c2.py:326-328`), i.e. it is portable inside any
lane clone and breaks only if the script is copied out of a lane.

### controls/c1-data.py — portable
No absolute path; `<tree>` is positional; `TMPDIR` is passed to the subprocess (`:99`); receipts are titled
`$ cd <lane checkout at <rev>> && python3 <tool> --selftest` — no host path (`:105`). Requirement: `<tree>` must be a
git checkout (`git -C <tree> rev-parse HEAD`, `:95`) with `tools/` present.

### controls/c1-controls.py — NOT portable (§5 F3, F4)
```
$ python3 $S/clone/.ufo/waves/round-52/controls/c1-controls.py $S/ctl do-nothing
do-nothing exit=2 C1_SETUP cannot resolve manifest
EXIT=0
$ git -C $S/clone status --porcelain
 M .ufo/waves/round-52/evidence/control-c1-do-nothing.txt
```

## 5. Findings

### F1 (MED) — the C1 arm-(C) pin writes into the hardcoded host lane and ignores `TMPDIR`
`corpus/README.md` (appended round-52 bullet 2, from `controls/c1-data.py:20-21`) makes
`python3 .ufo/waves/round-39/conform.py <rev> --selftest` a living pin, so `count-c1.py` arm (C) executes it on every
run. That instrument hardcodes the lane (`round-39/conform.py:53 LANE = "/home/vgpnk/Projects/shokunin/mori-shokunin"`,
`:54 SCRATCH_ROOT = <LANE>/.ufo/waves/round-39/scratch`) and its selftest does
`tempfile.mkdtemp(prefix="mori-conform-selftest-", dir=SCRATCH_ROOT)` (`:492`).

Probe (my own single run from the relocated clone, `TMPDIR` set):
```
before: mori-conform-selftest-4zqojen3 mori-conform-selftest-90ok9tm5
$ cd $S && TMPDIR=$S/tmp python3 $S/clone/.ufo/waves/round-39/conform.py 4f266ef2… --selftest
CONFORM_SELFTEST pass=9 fail=0      exit=0   (51.23 s)
after:  mori-conform-selftest-1u9p53rj 8chxqzgg cswoi1cf na_ppue6 nhjcapxe   (5 dirs, mine plus concurrent seats')
$ ls $S/tmp      -> empty
```
So: files appear under `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-39/scratch/mori-conform-selftest-*`
holding `counter-*.py` fixtures while the pin runs (552 K peak observed, 3 live dirs; the dirs are removed as runs
finish — permanent accumulation UNVERIFIED, transient write VERIFIED), and nothing is written to `TMPDIR`.
`git -C <lane> status --porcelain --ignored -- .ufo/waves/round-39/scratch` reports `?? .ufo/waves/round-39/scratch/`.
Off-host the same pin raises `FileNotFoundError` on `mkdtemp(dir=<absent>)` → arm (C) mismatch → C1 not reproducible
there. Not a round-52 code defect: a host-pinned dependency the round-52 supersession text newly relies on (QUALITY
127 "Not covered: older wave instruments … not repaired" does not cover *making one a living pin*).

### F2 (MED) — `lane_writes` cannot see a pin that writes to a hardcoded lane path
`count-c1.py:528-532` diffs `git status --porcelain --ignored --untracked-files=all` of the `--repo` argument only.
When `--repo` is a clone (every control receipt, every seat replay, my run) a pin that writes into the hardcoded real
lane — F1 — is invisible, so the contract's `lane_writes=0` is evidence about the clone, not about the lane. The
contract's named limits list six blind spots (`contract.md`, C1 "Named limits") but not this one.

### F3 (HIGH) — `c1-controls.py` cannot be pointed at a fleet root; it exits 0 when every control fails at setup
`c1-controls.py:13-15` fixes `LANE = dirname³(HERE)`, `FLEET = dirname(LANE)` and passes `--fleet-repo FLEET` to the
counter (`:57-58`) with no override flag and no check that `FLEET/MANIFEST.json` exists. From any tree that is not
`<fleet>/<lane>/.ufo/waves/round-52/controls/` every control dies at setup, and `main()` returns 0 regardless
(`:75`), so an operator checking `$?` records "controls rebuilt" while the printed receipts say `exit=2`:
```
$ python3 $S/clone/.ufo/waves/round-52/controls/c1-controls.py $S/ctl do-nothing
do-nothing exit=2 C1_SETUP cannot resolve manifest
EXIT=0
```
Verified for `do-nothing` (the other seven take the same path; not re-run to keep the audit bounded).

### F4 (MED) — `c1-controls.py` rewrites the frozen receipts in its own tree
`c1-controls.py:54` writes each receipt to `W/evidence/control-c1-<name>.txt` where `W` is the script's own round-52
dir; there is no `--out` and no guard that the script is running outside the measured lane. The docstring only
promises the *clone* and *counter scratch* live outside the lane, so the natural reading is "run it from the lane".
Run from the lane at DATA it rewrites eight files listed in `evidence/freeze-sha256.txt` — the same class as
round-51 routed defect 6. Proven in the clone:
```
frozen:    c6031437dffa0db4790eed96352f2d1f23b67f6140117dd1f98b173ad63f0aae  .ufo/waves/round-52/evidence/control-c1-do-nothing.txt
rewritten: 1588b2e09c04eba54196735c3bd4873fd26de7fb79136426f50c43f7e25023a8  (same path, after the F3 run)
```
The rewritten file's body is the failed setup run, so the L1's calibration witness is replaced by an error receipt.

### F5 (LOW) — `count-c1.py` fleet root defaults to the repo's parent
`count-c1.py:484-485`: `repo = dirname³(here)`, `fleet = dirname(repo)`, no `MANIFEST.json` check before use.
Relocated clone without `--fleet-repo`:
```
$ python3 $S/clone/.ufo/waves/round-52/count-c1.py 8524904a… --repo $S/clone
C1_SETUP cannot resolve manifest       exit=2
```
Portable in the sense that matters (the override works, §4), but the requirement is stated nowhere: usage shows the
flag as optional and no receipt prints "--fleet-repo is mandatory off-layout".

### F6 (LOW) — `build-w1-spec.py:18` hardcodes this host's scratch root
`X = "/fast/scratch/hyaku/mori-r52"` is executable input to every generated prompt; invisible to both mandated
greps (it is `/fast/`, not `/home/vgpnk` or `/tmp`) and to QUALITY 127's check, which greps `'/home/vgpnk'` over
`tools/` only (`corpus/QUALITY.md:1074-1076`) and not `.ufo/waves/`. A spec rebuilt elsewhere dispatches 68 seats to a
path that does not exist there.

### F7 (LOW) — three receipts the wave spec cites are absent from DATA and from the freeze list
`git cat-file -e DATA:.ufo/waves/round-52/evidence/{c1-at-data,c2-at-data,c2-hashes-at-data}.txt` → absent for all
three; none appears in `evidence/freeze-sha256.txt`; all three exist in the working tree (mtime 21:08) and are
tracked only from `075436b1`. The round prompt and `w1-spec.json` hand seats those paths, and
`contract.md` C2 names `evidence/c2-at-data.txt` as the before-control receipt. A reader who takes the cited
receipts from DATA (`git archive DATA`, what both counters measure) finds nothing. I reproduced both readings from
the relocated clone (C1 `met`, `manifest=6209bdb8e400`; C2 `located=28 entailed=0 failed=entailment`), so the
numbers are true — the committed evidence of them is not at DATA.

### F8 (LOW) — runtime dependencies of the replay path
`git` and `tar` on `PATH` (`count-c1.py:539-541`, stdin `git archive | tar -x -C <tree>`); `python3` pins are
rewritten to `sys.executable` (`:546`, good), `bash` pins would come from `PATH`; Python ≥ 3.5
(`os.path.commonpath`, `subprocess.run`). `count-c1.py` omits `dir=` on `mkdtemp` where the lane's own round-39
`mkdtemp_ok` audit (`round-39/conform.py:248-260`) requires it — compensated by the commonpath guard, at the price of
inheriting stdlib's `/tmp` fallback.

### F9 (informational) — pin-side `/var/tmp` fallbacks are not this round's
`tools/mori-pin-check.py:952` `scratch_parent = abspath(args.scratch or TMPDIR or "/var/tmp")` — `TMPDIR`-first, so
the round-52 counter's `TMPDIR=<scratch>/tmp` (`count-c1.py:545`) is honoured; the bare invocations that create the
four 332 MB `/var/tmp/pin-check-*` trees in `disk-guard.sh status` are outside this round. Lanes tools under
`tools/` carrying `/tmp`-family strings (`mori-census.sh` 13, `mori-round17-context-check.py` 8, `mori-pin-check.py`
7, …) are outside the round-52 tree and QUALITY 127's scope.

## 6. Named limits of this audit

- Coverage is the round-52 tree at DATA plus the two counters' executed pins; `tools/` and rounds 38-49 instruments
  were read only where a round-52 pin or the C1 arm depends on them (F1, F9).
- Only `do-nothing` was run through `c1-controls.py` (F3/F4); the other seven controls share the code path.
- Whether the `round-39/conform.py` scratch dirs are always removed (versus left behind on timeout/interrupt) is
  UNVERIFIED; only the during-run write and the `TMPDIR`-ignoring are proven.
- The `--scratch`-inside-repo refusal (`count-c1.py:505`) was verified by reading; I did not execute the refusal.
- I did not re-verify the fleet `MANIFEST.json` tag `6209bdb8e400` against a second fleet checkout; one fleet root
  was used.
- Not judge: I am a dispatched seat, not an independent verifier of the round's claims. C1/C2 verdicts quoted above
  are portability reproductions, not a scoring.

## 7. Routed items (round 53)

1. Give `c1-controls.py` a `--fleet-repo` (or derive it from a required `--lane`) and make `main()` return the
   worst control's exit code — F3. Frozen-bytes rule: this is a successor, not an in-place edit.
2. Give `c1-controls.py` a `--out` (or refuse to run when `HERE` is a tree that contains `evidence/freeze-sha256.txt`
   and the target receipt is listed in it) — F4.
3. Replace the `round-39/conform.py` living pin with a portable successor, or state in the round-52 text that the
   pin is host-pinned — F1; add "pins that write to a hardcoded lane are invisible to `lane_writes`" to the C1
   named-limits list — F2.
4. Extend QUALITY 127's check to `/fast/scratch`-class scratch constants in wave generators and to layout-derived
   defaults (`dirname(repo)`, `dirname(LANE)`) — F5, F6. Criterion text is frozen this round: routed as data change
   for round 53, not applied here.
5. Commit the before-data receipts (`c1-at-data.txt`, `c2-at-data.txt`, `c2-hashes-at-data.txt`) and add them to
   `freeze-sha256.txt` — F7.

## Findings

- **HIGH — `controls/c1-controls.py:13-15,57-58,75`**: fleet root fixed to `dirname(LANE)` with no override and
  `main()` returns 0. From any tree outside `<fleet>/<lane>/…` all eight controls fail `C1_SETUP cannot resolve
  manifest` while the builder reports success (`do-nothing exit=2 … EXIT=0`).
- **MED — `.ufo/waves/round-39/conform.py:53-54,492` reached via `corpus/README.md` round-52 bullet 2**: the C1
  arm-(C) living pin hardcodes `/home/vgpnk/Projects/shokunin/mori-shokunin`, ignores `TMPDIR`, writes
  `mori-conform-selftest-*` fixtures into the real lane while it runs (5 dirs before/after a single probe, 552 K
  peak), and fails off-host.
- **MED — `count-c1.py:528-532`**: `lane_writes` samples only the `--repo` clone, so a pin writing to a hardcoded
  lane path cannot be seen; `lane_writes=0` is not evidence of no lane writes.
- **MED — `controls/c1-controls.py:54`**: receipts are written to `<script's own tree>/evidence/` with no `--out`;
  run from the lane it overwrites the eight frozen control receipts (proven: `c6031437…` → `1588b2e0…`), the defect-6
  class.
- **LOW — `count-c1.py:484-485`**: fleet root defaults to `dirname(repo)`; relocated replay needs an explicit
  `--fleet-repo` or exits 2 `C1_SETUP cannot resolve manifest`.
- **LOW — `build-w1-spec.py:18`**: `X = "/fast/scratch/hyaku/mori-r52"` — the only executable absolute host path in
  the round-52 tree, interpolated into every seat prompt and invisible to both mandated greps and QUALITY 127.
- **LOW — `evidence/{c1-at-data,c2-at-data,c2-hashes-at-data}.txt` (working tree only)**: cited by the wave spec and
  by `contract.md` C2, absent from DATA and from `freeze-sha256.txt`; tracked only from `075436b1`.
- **LOW — `count-c1.py:539,546`**: replay needs `git`, `tar` on `PATH`, Python ≥ 3.5; `mkdtemp` without `dir=`
  diverges from the lane's own round-39 `mkdtemp_ok` rule, relying on stdlib's `/tmp` fallback.
- **Informational — `count-c2.py`, `controls/c1-data.py`, `count-c1.py`**: portable — relocated-run verdicts match
  `evidence/c1-at-data.txt`, `evidence/c2-at-data.txt`, `evidence/selftest-c1.txt`, `evidence/selftest-c2.txt`
  exactly; no absolute host path, no `/tmp` default, `TMPDIR` honoured where temp files are needed.
