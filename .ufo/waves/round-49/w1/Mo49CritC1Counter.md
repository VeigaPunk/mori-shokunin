# Mo49CritC1Counter — round 49 w1: attack on `count-c1.py` (C1 calibration counter)

- Seat: Mo49CritC1Counter (critic, leaf; no subagent, no judge seat, no edit to any lane or frozen file).
- Instrument: `.ufo/waves/round-49/count-c1.py`, sha256
  `3c262a15ae28adffa63f6646d5ec15498d1a4c735dbc3c38f68af16afc616b6d` — identical to
  `git show 0df17b7b:.ufo/waves/round-49/count-c1.py`, i.e. the bytes I attacked are the frozen ones.
  It imports `.ufo/waves/round-48/count-c1.py` (J1-J8, H1-H4) at module load.
- Revisions: entering `b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86`, freeze
  `0df17b7b4e667dd0aaaef0adc7d7d9973e6aa115`. Every scoring run below used `--rev b3e3453d…` and
  `--jobs 3`; the landed tip R does not exist yet, so this is a pre-landing falsifier and it changed no
  frozen byte.
- Tooling: nothing installed; `pacman` was not run; python3 stdlib only. Scratch and `TMPDIR`:
  `/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r49-Mo49CritC1Counter/` (untracked). Read-only
  git only (`show`, `rev-parse`, `log`, `-C <mktemp fixture>`); no `git add/commit/stash/checkout/reset/
  pull/push`, no jj command. Host untouched (no `journalctl`/`systemctl`).
- Machine id: `MACHINE_ID` (not recorded).

## Instrument checks (observed)

```
$ python3 .ufo/waves/round-49/count-c1.py --selftest
C1_SELFTEST pass=44 fail=0                                    [exit 0]
```

The selftest is green **with the bypass below in place** (run after the stubs were written). Two of its
arms are supposed to protect exactly this channel and do not:

- `count-c1.py:373-376` `handles_carry_no_variant_name` matches the handle *strings* against
  `variant|junk|honest|[JNH]\d|real`. A `<sha256-prefix>` handle passes vacuously.
- `count-c1.py:392-400` `filename_sniffer_not_met` scores a *fake* sniffer keyed on round-48 names
  (`variant-[JN]|/c1-[JN]|junk`). It proves the round-48 sniffer is dead; it does not test whether the
  handle is *computable*.
- `count-c1.py:377-378` `order_not_expect_sorted` asserts that the **run** order (`jobs.sort` at
  `:275`) is not ORDER-sorted. The **staging** order (`:264`) is exactly ORDER, and mtimes/inodes
  preserve it (channel C5 below). The arm gives false assurance about ordering.

## (a) Are the eighteen "junk" and seven "honest" edits really junk/honest?

I applied every edit function to `git show b3e3453d:SKILL.md` (155 067 bytes) and read the produced
row/cells. One coherent boundary holds across all 25 text edits: **junk = a pin that is false,
misattributed, or duplicated with a contradicting contract; honest = a formatting change that
carries no pin token.** No variant is
mislabeled. Specific checks, because these three were the plausible ones:

**H4 keeps the tally truthful (checked against the observed text).** `r48.v_h4` appends

```
| r48 honest second pin row | gate | `python3 .ufo/waves/round-47/count-c2.py <rev> [--repo DIR]` | 0/1/2 | `python3 .ufo/waves/round-47/count-c2.py --selftest` → `C2_SELFTEST pass=13 fail=0` | none | none | mori |
```

```
$ TMPDIR=.scratch/r49-Mo49CritC1Counter python3 .ufo/waves/round-47/count-c2.py --selftest | tail -1
C2_SELFTEST pass=13 fail=0                                    [exit 0]
```

`13 == 13`: H4 is a *true* pin on a real instrument, not a stale copy. (My first hypothesis was the
opposite — that H4 copied the `pass=14` of the round-45 row at `SKILL.md:191`; `r47_rows()` picks the
row *after* the reconciler row, which pins 13. Verified, hypothesis discarded.)

Precision that matters for wave 2: H4's new row has **the same entry command as `SKILL.md:939`**
(`python3 .ufo/waves/round-47/count-c2.py <rev> [--repo DIR]`), the same true pin, and a generic
`0/1/2` verdict map where the existing row has a detailed one. So the N5/H4 boundary is *contradiction*,
not *duplication*: N5's second row says `1 → PIN_CHECK_SETUP` against the standing `1 →
PIN_CHECK=unmet`; H4 restates without contradicting. A landed tool that reads N5 as "reject a second
row for one command" prints `unmet` on H4 → `honest_unmet=1` → `C1=unmet`. The merged witness passes
both (so its duplicate rule is contradiction-based), but this is the thinnest honest/junk edge in the
set and a K-class authority rule could step over it.

**N8 is a genuine misattribution, not a false pin.** Cell-by-cell diff of the edited row (16 cells,
only cell 11 changed):

```
cell 11
  old: `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST pass=60 fail=0`
  new: `python3 tools/mori-unlanded-check.py --selftest` → `UNLANDED_SELFTEST pass=13 fail=0`
```

The entry cell still names the reconciler, and the self-test cell now pins a *different, landed*
instrument whose tally is real:

```
$ TMPDIR=.scratch/r49-Mo49CritC1Counter python3 tools/mori-unlanded-check.py --selftest | tail -1
UNLANDED_SELFTEST pass=13 fail=0                              [exit 0]
```

So the row asserts "the reconciler's self-test is 13" while the reconciler's self-test is 60. That is
D7/R11 exactly, and only an instrument-binding rule can catch it — which is what the entering v3 cannot
do (`evidence/control-c1-tool-v3-entering.txt`: `N8 got=met`).

**N10 leaves a stale pin and H5 does not (verified from the built fixture repositories).**

```
$ grep -o "PROBE_SELFTEST pass=[0-9]* fail=0" w-e2b4320242da/SKILL.md
PROBE_SELFTEST pass=2 fail=0                                  # registry pin
$ python3 w-e2b4320242da/tools/probe.py --selftest | tail -1
PROBE_SELFTEST pass=3 fail=0                                  # observed  -> N10 stale
$ grep -o "PROBE_SELFTEST pass=[0-9]* fail=0" w-dde26571b05e/SKILL.md
PROBE_SELFTEST pass=3 fail=0
$ python3 w-dde26571b05e/tools/probe.py --selftest | tail -1
PROBE_SELFTEST pass=3 fail=0                                  # -> H5 truthful
$ git -C w-dde26571b05e log --format='%h %s | %an' | cat
6488970 c | c1
46f4d2f c | c1
```

Commit message `c`, author `c1`, and both fixtures share the identical baseline commit `46f4d2f` — no
variant name leaks through commit metadata, as the contract claims.

The other fifteen variants: J1-J8 are round-48's (already adjudicated in round 48), N1-N4 and N7 append
a row/phrase carrying `pass=999` in a rendering context the tool must not trust (comment, NBSP+ZWSP
token, tab fence, four-space block, HTML table), N5 duplicates the reconciler's authority with a
contradicting exit map (1 → `PIN_CHECK_SETUP`), N6 records `fail=0` in prose and `fail=3` on the
continuation line, N9 names the gate registry in the entry cell and pins the reconciler's true tally.
All hold a false or misattributed claim. Honest H1/H2/H3/H6/H7 add prose, an escaped trailing pipe, a
case-only header, an HTML comment/table with no pin, and indented rows with no pin. **No mislabeled
variant found.**

Residual (not a mislabel, a coupling): H4's pin is copied from the following row, so it stays honest
only while `.ufo/waves/round-47/count-c2.py --selftest` prints 13 (it does at `b3e3453d`); J7/J8 are
anchored on literals of files **outside** C1's declared surface — `(743 lines)` of
`tools/mori-gate-registry.py` (`SKILL.md:184`) and `37fd7c24ff52…` of
`.ufo/waves/round-45/count-c3.py` (`SKILL.md:192`). Any seat that touches those two rows turns
`plan()` into `C1_SETUP` (exit 2), not `C1=unmet` (see the LOW finding on the J7/J8 anchors).

## (b) Narrow tools — does any rule narrower than the junk pass?

Four cheapest one-rule candidates, each scored with the frozen counter. Command pattern:

```
$ TMPDIR=$PWD/.scratch/r49-Mo49CritC1Counter \
  python3 .ufo/waves/round-49/count-c1.py --tool <stub>.py \
  --rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 --jobs 3 --scratch <fresh dir>
```

| stub | one rule (verbatim predicate) | `C1` line | exit | what breaks it |
|---|---|---|---|---|
| `narrow-append-row.py` (sha256 `b5208e7b5f83…`) | `unmet` if any line of the copy that is not a line of `git show rev:SKILL.md` starts with `\|` or contains `pass=` | `C1=unmet junk_met=1 honest_unmet=4 real=met errors=0 variants=26` | 1 | H2 (in-place edit of a row becomes an "added" row-ish line), H3 (header line starts with `\|`), H4 (H4's *honest* new row), H7 (indented rows) — `honest_unmet=4` |
| `narrow-nonascii.py` (`fd53b596b8d0…`) | `unmet` if any character > U+007F | `C1=unmet junk_met=0 honest_unmet=8 real=unmet errors=0 variants=26` | 1 | the real registry holds 488 non-ASCII characters (`→`, `·`), so `real=unmet` and every honest edit fails |
| `narrow-html.py` (`726217cfb587…`) | `unmet` if `<!--` or `</?(table\|tr\|td\|th\|code\|div\|span\|p\|br\|b\|i)\b` appears | `C1=unmet junk_met=1 honest_unmet=7 real=unmet errors=0 variants=26` | 1 | H6 (its honest HTML table), and `real=unmet` because `SKILL.md:731` contains the prose token `swap free <= <b>%` |
| `narrow-tab.py` (`372e9cb9f97b…`) | `unmet` if `\t` appears anywhere | `C1=unmet junk_met=17 honest_unmet=1 real=met errors=0 variants=26` | 1 | H7 (its honest tab-indented fenced row); catches only N3 of 18 |

None printed `C1=met`. The honest arms do the job the contract says they do: each narrow rule is
falsified by an honest edit or by the real registry. **No narrow-pass finding here.** The one class
that does pass is not a narrow rule but an *identity oracle*, below.

## (c) Identity channels — what the counter still hands the tool

Probe stub (`probe-channels.py`, sha256 `fc43e4834c78…`) logged every channel on all 27 runs
(`.scratch/r49-Mo49CritC1Counter/channels.jsonl`). The counter's scratch held **53 entries for every
run**: 24 staged `s-*.md` copies, 2 `w-*` fixture repositories, 27 `t-*` TMPDIRs.

| # | channel | observed value | identifies the variant? | counter line |
|---|---|---|---|---|
| C1 | `--skill` basename | `s-<sha256(rev, body)[:12]>.md` | **yes, exactly** — the tag is a pure function of the variant body, and the tool has `--repo`+`--rev` or the counter source | `:216-221`, `:258` |
| C2 | `TMPDIR` basename | `t-<same tag>` | **yes**, same function | `:261`, `:229` |
| C3 | `dirname(TMPDIR)` listing | 24 staged bodies + 2 fixture repos, world-readable to the tool | **yes** — all variant bodies and the real body are readable before the run | `:255-275` |
| C4 | argv shape | `--skill` present for 24 runs; absent for 3; `--min-tally-pins 1` for the 2 fixture runs; `--baseline-rev` = fixture c0 there | partitions text / real / fixture; `--skill` **absent ⟺ the `real` run** | `:224-232`, `:269-274` |
| C5 | file mtime (and inode) order of `s-*.md` | 24/24 distinct `st_mtime_ns`, strictly increasing in **staging** order = `[J1…J8,H1…H4,N1…N9,H6,H7,real-opaque]`; inode order identical 24/24 | **yes, exactly** — nothing is hashed | `:264`, `:275` (only the *run* order is hash-sorted) |
| C6 | fixture repo path | `w-<opaque("fixture", str(move_pin), dirname(repo))>` | **yes, exactly** — recomputable from `dirname(--repo)` | `:177` |
| C7 | `--repo` for text runs | the lane path → `.ufo/waves/round-49/count-c1.py` is readable | enables C1 without any prior knowledge | `:261`, `:274` |
| C8 | commit message / author of fixtures | `c` / `c1 <c1@example.invalid>`, baseline object `46f4d2f` shared | no | `:186-192` |
| C9 | `cwd` | `<lane>` for all 27 runs | no | `:228` |
| C10 | parent cmdline (`/proc/ppid/cmdline`) | counter path + `--scratch` | no (but exposes the counter) | — |

### The two stubs and their receipts

**Hash-channel oracle** (`sniff-hash.py`, sha256 `ce19a5058135…`). It reads `--skill`, and for
text runs imports the frozen counter from `--repo` to recompute `opaque(rev, fn(SKILL.md at rev))` for
each junk variant; for fixture runs it recomputes `opaque("fixture", "False", dirname(repo))`. It never
parses a row, a pin or a tally.

```python
#!/usr/bin/env python3
"""C1 oracle B (hash channel): recompute the content-addressed handle the counter uses."""
import hashlib, importlib.util, os, sys
argv = sys.argv[1:]
def opt(name):
    return argv[argv.index(name) + 1] if name in argv else None
def opaque(*parts):
    h = hashlib.sha256()
    for p in parts:
        h.update(p if isinstance(p, bytes) else p.encode("utf-8")); h.update(b"\0")
    return h.hexdigest()[:12]
skill, repo, rev = opt("--skill"), opt("--repo") or ".", opt("--rev")
got = "met"
if skill:
    base = os.path.basename(skill)
    tag = base[2:-3] if (base.startswith("s-") and base.endswith(".md")) else ""
    counter = os.path.join(repo, ".ufo", "waves", "round-49", "count-c1.py")
    if tag and os.path.exists(counter):
        spec = importlib.util.spec_from_file_location("c1_oracle", counter)
        c1 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c1)
        text = c1.r48.git_show(repo, rev, "SKILL.md")
        for name, expect, fn in list(c1.r48.VARIANTS) + c1.NEW_VARIANTS:
            if expect == "unmet" and c1.opaque(rev, fn(text)) == tag:
                got = "unmet"; break
elif os.path.basename(repo.rstrip("/")).startswith("w-"):
    scratch = os.path.dirname(repo.rstrip("/"))
    if os.path.basename(repo.rstrip("/"))[2:] == opaque("fixture", "False", scratch):
        got = "unmet"
print("PIN_CHECK=%s" % got)
sys.exit(0 if got == "met" else 1)
```

```
$ TMPDIR=$PWD/.scratch/r49-Mo49CritC1Counter python3 .ufo/waves/round-49/count-c1.py \
    --tool $PWD/.scratch/r49-Mo49CritC1Counter/sniff-hash.py \
    --rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 --jobs 3 \
    --scratch $PWD/.scratch/r49-Mo49CritC1Counter/run-sniff-hash
variant name=J1 expect=unmet got=unmet rc=1
…  (27 lines, every one `got` == `expect`; full text at .scratch/…/out-sniff-hash.txt)
variant name=H5 expect=met got=met rc=0
variant name=real expect=met got=met rc=0
variant name=real-opaque expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86   [exit 0]
```

**Mtime-channel oracle** (`sniff-mtime.py`, sha256 `007e42a8b46c…`). It never opens a file; it
sorts `s-*.md` in `dirname(TMPDIR)` by `st_mtime_ns` and indexes the frozen `ORDER`, and for fixture
runs sorts the two `w-*` directories. It needs neither the counter nor the lane bytes.

```python
#!/usr/bin/env python3
"""C1 oracle A (mtime channel): identify the variant by the mtime rank of the staged copy."""
import os, sys
argv = sys.argv[1:]
def opt(name):
    return argv[argv.index(name) + 1] if name in argv else None
skill, repo = opt("--skill"), opt("--repo") or "."
tmp = os.environ.get("TMPDIR", "")
parent = os.path.dirname(tmp.rstrip("/")) if tmp else ""
STAGE = ["J1","J2","J3","J4","J5","J6","J7","J8","H1","H2","H3","H4",
         "N1","N2","N3","N4","N5","N6","N7","N8","N9","H6","H7","real-opaque"]
EXPECT = {n: ("met" if (n.startswith("H") or n == "real-opaque") else "unmet") for n in STAGE}
EXPECT.update({"N10": "unmet", "H5": "met"})
name = None
if skill and parent:
    sibs = [n for n in os.listdir(parent) if n.startswith("s-") and n.endswith(".md")]
    sibs.sort(key=lambda n: os.stat(os.path.join(parent, n)).st_mtime_ns)
    mine = os.path.basename(skill)
    if mine in sibs and len(sibs) == len(STAGE):
        name = STAGE[sibs.index(mine)]
elif os.path.basename(repo.rstrip("/")).startswith("w-") and parent:
    dirs = [n for n in os.listdir(parent) if n.startswith("w-")]
    dirs.sort(key=lambda n: os.stat(os.path.join(parent, n)).st_mtime_ns)
    if len(dirs) == 2:
        name = ["N10", "H5"][dirs.index(os.path.basename(repo.rstrip("/")))]
got = EXPECT.get(name, "met")      # unknown -> met (the real run carries no --skill)
print("PIN_CHECK=%s" % got)
sys.exit(0 if got == "met" else 1)
```

```
$ TMPDIR=$PWD/.scratch/r49-Mo49CritC1Counter python3 .ufo/waves/round-49/count-c1.py \
    --tool $PWD/.scratch/r49-Mo49CritC1Counter/sniff-mtime.py \
    --rev b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86 --jobs 3 \
    --scratch $PWD/.scratch/r49-Mo49CritC1Counter/run-sniff-mtime2
variant name=J1 expect=unmet got=unmet rc=1
…  (all 27 lines `got` == `expect`)
variant name=real-opaque expect=met got=met rc=0
C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26 rev=b3e3453d45ffbbecf2cce50fa1089b8eb80a4f86   [exit 0]
```

**Positive control that the stub is not passing by accident.** The first version of the mtime oracle omitted
`N10`/`H5` from its map and scored `N10 got=met` (`junk_met=1`, exit 1). After adding the two names the
same stub scored `C1=met`. The stub's verdict tracks its own identity logic, not the counter's parsing.

**Why this matters.** P-C1's literal sentence is reproducible, but the property the round claims at
`contract.md:30-32` and `count-c1.py:11-14` — "every variant reaches the tool under an opaque name … a
sha256 prefix of their bytes" — is false in the only sense that matters: a content-addressed handle is
a *deterministic function of the variant*, so it is an identity oracle, not an opaque name. Two
independent stubs (one of which opens no file) obtain `C1=met` with zero reconciliation. Whatever the
landed `tools/mori-pin-check.py` is, `C1=met` alone does not distinguish it from `sniff-hash.py`.

This is the same defect class as round 48's F1 (`w1/CritC1Counter.md`), not a new one: the fix removed
the *name* `variant-N` and replaced it with a *value* that names the variant. The contract's named limit
("a tool can pass by being narrower than the junk, so H1-H7 and the real registry are part of the
predicate") does not cover it: an oracle is not narrower, it implements no check, and H1-H7 are exactly
what it keys on.

## Counter defects outside the seat brief (observed)

1. **A second run against the same `--scratch` exits 2** (`count-c1.py:177-178` — `os.makedirs` without
   `exist_ok`):

   ```
   $ TMPDIR=… python3 .ufo/waves/round-49/count-c1.py --tool …/sniff-hash.py --rev b3e3453d… \
       --jobs 3 --scratch …/.scratch/r49-Mo49CritC1Counter/run1
   C1_SETUP fixture variant: [Errno 17] File exists: '…/run1/w-ec0f104ce129/tools'      [exit 2]
   ```

   (`run1` had already been used by the probe run above, so this is invocation 2 with that scratch; the
   third invocation reproduced the same exit 2 — `reuse-1.txt` and `reuse-2.txt`.)

   Fails closed, but a verifier who re-runs a receipt with the recorded `--scratch` gets exit 2, which
   the kill rule does not classify (it names only `C1=unmet`).

2. **N8's anchor is "exactly one row"** (`count-c1.py:128-131`). I appended one plausible wave-1 row
   ("pin reconciler floor (r49 K5) … `python3 tools/mori-pin-check.py --selftest` → `PIN_CHECK_SELFTEST
   pass=65 fail=0`") to the entering text:

   ```
   N8 with extra row raises: Anchor reconciler self-test row: 2 hits
   ```

   `plan()` turns that into `C1_SETUP` / exit 2. C1's own landing is expected to add K-class rows to
   that registry, so this is a live risk at R, not a hypothetical.

3. **The `real` arm is argv-distinguishable** (`count-c1.py:274`): it is the only run with no
   `--skill`. The contract says the tool reads "R's SKILL.md read twice"; a tool that prints `met`
   whenever `--skill` is absent passes that arm without reading anything.

4. **The predicate text does not match the executed predicate.** `contract.md:28-29` and
   `count-c1.py:9-10` say "every run with `--min-tally-pins 26 --baseline-rev 2d85e33d`"; the two
   fixture runs use `--min-tally-pins 1 --baseline-rev <fixture c0>` (`:268-269`). Necessary, but P-C1
   as written is literally false for 2 of 27 runs.

5. **`-I -B`** (`count-c1.py:225`): a landed tool that imports a sibling module (or a `tools/` package)
   crashes under isolated mode and lands in `errors`, although nothing in the contract restricts the
   landed tool to one file.

## Smallest safe corrections (routed; NOT applied — the kill rule forbids re-scoring round 49)

For the successor counter, in order of cost:

1. **Per-run random handle.** `tag = secrets.token_hex(6)` instead of `opaque(rev, body)` (`:258`,
   `:261`); same for the fixture directory (`:177`). Kills C1, C2, C6, C7.
2. **One private directory per variant.** `scratch/<nonce>/SKILL.md` with `TMPDIR=scratch/<nonce>/tmp`,
   and stage fixtures under their own parent. Kills C3 (no sibling bodies, no sibling repos).
3. **Shuffle the staging loop** (`:264`) — with (2) this closes C5 redundantly, but it is one line.
4. **Uniform argv.** Write the revision's own `SKILL.md` to an opaque copy and pass `--skill` for the
   `real` arm too (`:274`); pass the real `--min-tally-pins`/`--baseline-rev` shape wherever the fixture
   can carry it. Closes C4.
5. **One run-time-generated instance per arm class** — the only fix that survives content matching,
   because the 26 frozen bodies are public source. E.g. junk: pick a random parsed row and decrement
   its `pass=` by 1-3 (same class as J7/mismatch, must be `unmet`); honest: append a random 6-word
   prose sentence (same class as H1, must be `met`). A whitelist/oracle cannot answer an instance it
   has never seen. This is *not* a new junk class, so it does not breach "the variants are the classes
   found by rounds 47-48".
6. **Selftest arms that actually test the property**: assert the handle is not recomputable from
   `(rev, body)` (e.g. run the counter twice with different nonces and require different handles), and
   assert `dirname(TMPDIR)` contains exactly one entry. The present arms (`:373-378`) test the handle
   *string* and the *run* order only.
7. **Build the fixture under a `mkdtemp`-derived directory** instead of a fixed
   `os.makedirs(d + "/tools")`, and print the scratch path in the `C1=` line; a re-run must reproduce
   the line, not exit 2.
8. **N8**: locate the reconciler row by name (`registry pin reconciler (r47, C1)`) or require ≥1 hit
   and edit the first, so a second legitimate row cannot turn the counter into a setup error.
9. **J7/J8**: derive the line count and digest prefix from `git show rev:<path> | wc -l` and
   `sha256sum` instead of literals `(743 lines)` / `37fd7c24ff52…`.

## Limits of this review

- I did not score the landed tool (it does not exist) and did not re-score any control; the freeze
  receipts stand. My stubs are not candidates for `tools/` — they are counter falsifiers.
- C5 (mtime/inode order) was verified on this host's filesystem only (24/24 distinct, monotone); on a
  coarse-timestamp filesystem it could tie. C1/C6 are deterministic and environment-independent, and
  either alone is sufficient.
- I read `count-c1.py` and `round-48/count-c1.py` in full; I read the v3 tool's docstring and CLI only
  (I did not re-audit its rules — that was `Mo49ExecArmsBindUnlanded`/`CritFrozenCfg` territory).
- The `real` run was observed to be argv-alone distinguishable; I did not build the 5-line stub that
  exploits it because the hash-channel oracle already covers the arm.

## Affected axes

- **calibration (5, the claim's axis):** the C1 instrument cannot be credited on `C1=met` alone; a
  zero-reconciliation oracle obtains the same line. Wave 2 should report this as a limit, and the axis
  should rest on the landed tool's own `--selftest` arms plus a fresh (non-frozen) junk instance.
- **depth, freshness, adjacency, coverage, operability:** untouched — C2, the corpus and the tools are
  outside this review.
- **round-49 mistake record (false provenance risk):** if the mistake item records round 48's F1 as
  *fixed* by opaque handles, that record is wrong; the correct record is "the round-48 *name* sniffer is
  dead; the identity channel survives as two computable handles". Same for any QUALITY
  flagged-versus-fixed count that books this as closed.

## Evidence index

- `.scratch/r49-Mo49CritC1Counter/probe-channels.py` (`fc43e4834c78…`) + `channels.jsonl` (27 records,
  53 siblings per record) — channel log.
- `sniff-hash.py` (`ce19a5058135…`) + `out-sniff-hash.txt` — hash-channel oracle, `C1=met`, exit 0.
- `sniff-mtime.py` (`007e42a8b46c…`) + `out-sniff-mtime2.txt` — mtime-channel oracle, `C1=met`, exit 0.
- `narrow-append-row.py` (`b5208e7b5f83…`), `narrow-nonascii.py` (`fd53b596b8d0…`),
  `narrow-html.py` (`726217cfb587…`), `narrow-tab.py` (`372e9cb9f97b…`) + `out-*.txt` — four narrow
  candidates, all `C1=unmet`.
- `reuse-2.txt` — exit-2 receipt for a re-used `--scratch`; `reuse-1.txt` for the same failure.
- Frozen reads: `count-c1.py` sha256 `3c262a15ae28…` (== freeze); `--rev b3e3453d…` throughout.
- Commands that produced the `(a)` evidence: `python3 .ufo/waves/round-47/count-c2.py --selftest`
  (`C2_SELFTEST pass=13 fail=0`, exit 0), `python3 tools/mori-unlanded-check.py --selftest`
  (`UNLANDED_SELFTEST pass=13 fail=0`, exit 0), fixture `probe.py --selftest` in both `w-*` repos.

## Findings

- **HIGH — `.ufo/waves/round-49/count-c1.py:216-221,258,261` (content-addressed handles) with
  `contract.md:30-32` / `count-c1.py:11-14`:** the "opaque name" is `sha256(rev, variant body)[:12]`,
  a deterministic function of the variant. A 30-line stub that imports the frozen counter and recomputes
  the tags scores `C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=26` (exit 0) while
  reading no pin, row, tally or digest. The contract's sentence is false and the C1 axis evidence cannot
  separate the landed reconciler from an oracle. The selftest arms at `:373-376` and `:392-400` do not
  test computability and stay green.
- **HIGH — `.ufo/waves/round-49/count-c1.py:255-275` (one shared staging directory; staging order =
  ORDER):** every run can list its 53 sibling entries, and the 24 `s-*.md` copies are ordered by
  `st_mtime_ns` exactly as `[J1-J8,H1-H4,N1-N9,H6,H7,real-opaque]` (24/24 verified; inode 24/24). A stub that opens
  no file at all, sorts siblings by mtime and indexes that list scores `C1=met … variants=26` (exit 0).
  Independent of the HIGH above: random handles would not close it, and closing it would not close that.
- **MED — `.ufo/waves/round-49/count-c1.py:274`:** the `real` arm is the only run without `--skill`, so
  it is passable by argv alone; "R's SKILL.md read twice" adds no discrimination.
- **MED — `.ufo/waves/round-49/count-c1.py:128-131` (`v_n8` anchor `len(hits) != 1`):** one additional
  reconciler-selftest row at R (wave 1 is landing K-class rows in that registry) makes `plan()` raise
  `Anchor` → `C1_SETUP` exit 2, not the `C1=met|unmet` the kill rule addresses. Demonstrated with a
  synthetic row: `N8 with extra row raises: Anchor reconciler self-test row: 2 hits`.
- **MED — `.ufo/waves/round-49/count-c1.py:177-178` (`os.makedirs` without `exist_ok`):** a second run
  with the same `--scratch` exits 2 (`C1_SETUP fixture variant: [Errno 17] File exists: …/w-…/tools`);
  a receipt cannot be reproduced with its recorded scratch.
- **LOW — `contract.md:28-29` vs `count-c1.py:268-269`:** P-C1 says every run uses
  `--min-tally-pins 26 --baseline-rev 2d85e33d`; the two fixture runs use 1 and the fixture baseline.
- **LOW — `.ufo/waves/round-49/count-c1.py:225` (`-I -B`):** an isolated-mode crash for any landed tool
  that imports a sibling module counts as `errors` and fails C1, though no contract sentence restricts
  the tool to a single file.
- **LOW — round-48 `v_j7`/`v_j8` anchors, reached from `count-c1.py:264`:** the literals `(743 lines)`
  (`SKILL.md:184`, file `tools/mori-gate-registry.py`) and `37fd7c24ff52…` (`SKILL.md:192`, file
  `.ufo/waves/round-45/count-c3.py`) live outside C1's declared surface; editing either row turns the
  counter into a setup error.
- **LOW — round-48 `v_h4`, imported at `.ufo/waves/round-49/count-c1.py:264`:** the honest arm adds a
  second row for the **same** instrument as `SKILL.md:939` (`round-47/count-c2.py`), same true pin, a
  generic `0/1/2` map. The N5/H4 boundary is therefore contradiction-only; a landed rule that rejects
  duplicate instrument rows on N5's evidence prints `unmet` on H4 and fails C1. State the boundary
  explicitly in the variant list (this round's docstring says only "a second row … with a contradicting
  exit contract").
- **INFO — no variant mislabeled:** the three plausibility-suspect edits are sound (H4 `13 == 13`,
  H5 `3/3`, N10 `2 vs 3`, N8 cell 11 only, its pin true for the invoked unlanded check). The junk/honest
  boundary is one sentence ("a false or misattributed pin is junk; a formatting change with no pin is
  honest") and every one of the 25 text edits honours it.

Report: .ufo/waves/round-49/w1/Mo49CritC1Counter.md
