# R48RevHarnessLeak — QUALITY 126: harness-identity leak check on the landed tool

**Attacked:** `/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-pin-check.py`
(landed tip `e4dfff32d4f97c7ef250e9a7538fa75d4f284492`) — the claim that the tool
contains no branch on harness identity (`--skill` basename, TMPDIR name, variant
names `J*`/`H*`, `variant-`, `c1-`).

**Verdict: HOLDS.** The landed tool carries no harness-identity branch: static
grep finds zero name/env introspection, and one junk variant (`count-c1.py`
`v_j1`) presented under two different filenames and two different TMPDIR names
produces **byte-identical output** (md5 `ee05e10912a6bc6f76ed135b4416aaf3`) and
identical `PIN_CHECK=unmet`, rc=1.

Residual (not a defect of the tool): the **counter** `count-c1.py` still leaks
variant identity through `--skill` basename and `TMPDIR` — a zero-registry-read
keyed stub printed `C1=met` at the tip (reproduced below). That is wave-1
`CritC1Counter` F1 still open on the *harness* side; it does not contradict the
seat claim, which is about the landed tool.

Seat: leaf, no subagents. All commands run with
`TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48RevHarnessLeak`.
Scratch: `.scratch/r48w2-R48RevHarnessLeak/` (probe.py, keyed-stub.py,
variant-*.md, out-*.txt, keyed-runs/). No tools installed; no repo mutation
(read-only `git show`/`archive` exports only; the tool's own transient
`<repo>/.scratch/pin-check-*` exports were removed by the tool on exit —
verified: none remain).

---

## 1. Static check — no harness-identity branch in the landed tool

Per-pattern `grep -nE` over all 917 lines of `tools/mori-pin-check.py` at the tip:

| pattern | result |
|---|---|
| `variant` | **no matches** |
| `c1-` | **no matches** |
| `J[0-9]` | **no matches** |
| `H[0-9]` | **no matches** |
| `basename` | **no matches** |
| `getenv` / `environ\.get` | only inside the *selftest fixture string* `TMPTOOL` (line 707: a synthetic instrument testing TMPDIR-is-under-root, not a name test) |
| `environ` (all uses) | line 406 `env = dict(os.environ, TMPDIR=tmp, …)` — the tool **writes** the child's TMPDIR (fresh `mkdtemp(prefix="pin-tmp-")` under `<measured root>/.scratch`); it never reads its own `TMPDIR` for any decision |
| `r48`, `round-48`, `count-c1`, `harness`, `junk` | only doc/comment strings and selftest fixture content; no executable token |
| `splitext`, `endswith` | **no matches** (no filename-shape tests at all) |
| `startswith` | all on *content*: `|`-row detection (L145), `..` path rejection (L271/274), sha256 prefix compare (L320), `[`/`-`/`<` word cuts (L383/387), `python` interpreter check (L128) |

How `--skill` is used: `main()` (L663–668) does `open(args.skill or <root>/SKILL.md)`
for **content only**; the path is never `basename`ed, `startswith`ed, or compared.
`check()` receives `text` (the file's content), never the path — there is
structurally no site where the filename could influence the verdict.

How TMPDIR is used: the tool reads its own environment only to pass it on.
`run_cmd` (L400–416) *overrides* the child's TMPDIR with a fresh dir under the
measured tree's `.scratch`. The tool's own `TMPDIR` influences only where its
`--selftest` mode `mkdtemp`s synthetic trees — nothing in `check()`.

## 2. Empirical — identical verdicts under two harness identities

Built `v_j1` (junk: header `self-test`→`selftest`, `pass=N fail=0`→`pass=1 fail=0`
on the two round-47 gate rows; detectable only by executing the instruments —
wave-1 F5) from `count-c1.py` functions against `SKILL.md@e4dfff32`, then ran the
landed tool twice replicating the counter's `run_tool` invocation:

```bash
# run A — harness "J" identity
TMPDIR=$D/c1-J1-leakprobeA python3 -I -B tools/mori-pin-check.py \
  --rev e4dfff32… --repo $LANE --min-tally-pins 26 --baseline-rev 2d85e33d… \
  --skill $D/variant-J1.md
# run B — harness "H" identity, byte-identical file content
TMPDIR=$D/c1-H5-leakprobeB python3 -I -B tools/mori-pin-check.py \
  --rev e4dfff32… --repo $LANE --min-tally-pins 26 --baseline-rev 2d85e33d… \
  --skill $D/variant-H5.md
```

Observed:

```
A-J1 rc=1  PIN_CHECK=unmet tally_pins=31 digest_pins=8 mismatches=2 … rev=e4dfff32… baseline=yes
B-H5 rc=1  PIN_CHECK=unmet tally_pins=31 digest_pins=8 mismatches=2 … rev=e4dfff32… baseline=yes
outputs_identical=True   rc_identical=True
md5 ee05e10912a6bc6f76ed135b4416aaf3  out-A-J1.txt
md5 ee05e10912a6bc6f76ed135b4416aaf3  out-B-H5.txt   (full 43-line transcripts)
```

The `unmet` came from executed instruments, not the filename:

```
pin line=938 kind=tally prefix=PIN_CHECK_SELFTEST state=mismatch pinned='pass=1 fail=0' observed='pass=60 fail=0' rc=0 cmd='python3 tools/mori-pin-check.py --selftest'
pin line=939 kind=tally prefix=C2_SELFTEST state=mismatch pinned='pass=1 fail=0' observed='pass=13 fail=0' rc=0 cmd='python3 .ufo/waves/round-47/count-c2.py --selftest'
```

Same content → same verdict regardless of which identity the harness channels
encoded. If any branch on basename/TMPDIR/variant name existed, the `variant-J1`
presentation would have had to differ from the `variant-H5` presentation; it did
not — down to the last byte of the per-pin transcript.

## 3. Could a harness-keyed tool be written without reading the registry? — Yes; demonstrated at tip

`keyed-stub.py` (scratch, 14 lines) never opens `--skill`; it decides purely on
`os.path.basename(--skill).startswith("variant-J")` and `re.search(r"c1-J[0-9]",
os.environ["TMPDIR"])`. Run through the real counter at the landed tip:

```bash
python3 .ufo/waves/round-48/count-c1.py --tool .scratch/r48w2-R48RevHarnessLeak/keyed-stub.py \
  --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 --scratch .scratch/r48w2-R48RevHarnessLeak/keyed-runs
```

Observed (counter exit 0):

```
variant name=J1..J8 expect=unmet got=unmet rc=1   (all 8)
variant name=H1..H4 expect=met   got=met   rc=0   (all 4)
variant name=real    expect=met   got=met   rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32…
```

The counter hands the tool both leak channels verbatim
(`--skill $scratch/variant-<J|H><n>.md`; `TMPDIR=$scratch/c1-<name>-XXXXXX`,
`count-c1.py` L238, L247, L205), so a keyed tool needs **zero registry reads** to
print `C1=met`. Wave-1 F1's proposed fix (fixed basename + neutral TMPDIR +
honest-variant H5) is still unlanded in the frozen counter.

## 4. What differs in the landed tool

The landed tool's verdict path is content-and-execution only:

- `check(text, root, …)` consumes **file content** — every state (`mismatch`,
  `unparsed`, `hidden`, `rebound`, `dropped`, `duplicate`, `no_command`) derives
  from parsed rows/spans, sha256 of in-tree files, or the observed tail of an
  actually-run bound instrument (`run_cmd`), plus the `--baseline-rev` SKILL.md
  bytes fetched via `git show` (L673) and the `--min-tally-pins` floor.
- No filename, argv-source, or environment introspection anywhere; `--skill`
  is `open()`ed for bytes and forgotten.
- Consequently the tool cannot distinguish J from H even when the harness
  announces it — which is exactly what §2 shows (identical transcripts), and why
  a `variant-J`-keyed stub scores `C1=met` (§3) while the real tool does not
  cheat: same junk content is `unmet` under either name.

## 5. Residual risk and verification gaps

- **Counter leak is live**: `C1=met` is still achievable by a 14-line keyed stub
  → C1's "met" for the real candidate does not by itself prove no-identity-keying;
  that property rests on the tool's code (this seat: verified absent). Reported
  as harness finding, consistent with w1 `CritC1Counter` F1 (unfixed).
- **Coverage**: grep was exhaustive over all 917 lines (every listed pattern
  plus `getenv`/`environ`/`splitext`/`endswith`/`realpath`/`abspath`/`sys.argv`).
  The empirical identical-output check was run on **one** variant (J1, the
  execution-dependent one); the remaining 11 were not individually re-run under
  swapped identities — UNVERIFIED per-variant, but moot: with no identity branch
  anywhere in the file, no variant can receive name-dependent treatment.
- **Not re-verified here**: overall `C1=met` claim for the real tool across all
  13 variants (covered by sibling seats); per the seat's scope only the
  identity-independence property was attacked.
- The tool's own write scope held: no `pin-check-*` or `pin-tmp-*` debris left in
  `<repo>/.scratch` after either run (verified via `git status`); all artifacts
  confined to `.scratch/r48w2-R48RevHarnessLeak/`.

## Report trailer

Report: .ufo/waves/round-48/w2/R48RevHarnessLeak.md
