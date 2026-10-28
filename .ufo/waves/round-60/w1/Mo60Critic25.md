# Mo60Critic25 — receipts determinism + rev-token analysis

Seat: critic (attack). Read-only on the lane; no commits, no VCS mutation, no
production edits. Scratch root `/fast/scratch/hyaku/mori-r60/Mo60Critic25`
(disk guard green at start: `/fast` 26% used, 600 G free), removed before yield.

Pins used (all reads at a named revision, never a working-tree read):

- frozen contract `ac496c7cde8cad965079858accae3bedfe4a73f2`
- entering revision `ddfb12fb0838b4307c445194a844f0c4b1950195`
- r59 data revision `7b86704d7c0754a09958d131b64dbfa2a6d3eaed`
- lane tip at seat run `b3c256138f00c704d5aa56eb0332d74506502ef2`
- `r59 count-c1.py` sha256 `2be6fda8…f0c9dfd`, `r59 count-c2.py` sha256
  `2df3ae84…75877be` — byte-identical at `7b86704d` and at tip (verified by
  `git show 7b86704d:.ufo/…/count-c{1,2}.py | sha256sum` vs `sha256sum` of the
  working copies), so the "counter bytes at the data rev" premise holds.

Scope: the two C1 receipts only (`evidence/r59-c1-met.txt`,
`evidence/r59-c2-met.txt`). C2/C3 instruments were not re-scored here.

---

## 1. Verdict

| Question | Answer |
|---|---|
| Do the two r59 counters reproduce byte-identically at `7b86704d`? | **Yes**, exit 0, stdout byte-identical across 4 run shapes per counter (§2). |
| Do the committed receipts byte-equal a fresh re-run? | **Yes**, sha256 identical, both. |
| Is the read surface fully revision-pinned (so `rev=` binds the data read)? | **Yes** for every lane read in both counters; one non-`rev` input (fleet MANIFEST at a constant revision) is fixed by the counter blob itself (§3). |
| Can a committed receipt byte-equal a re-run *yet lie about the revision*? | **Yes, in exactly one sense — under-attribution, not falsehood** (§4): a 40-byte edit of the `rev=` value converts a `7b86704d` receipt into a byte-exact receipt for another revision whose token vector agrees. It cannot make the receipt *false* at the revision it names. |
| Does the frozen checker accept such a relabeled receipt? | **No** — `count-c1.py` forces `R59_DATA`, so the relabel fails `bytes_differ` (verified, §5). |

No defect found that invalidates the C1 receipts arm as written.

---

## 2. Determinism evidence

Counters materialized from the pinned revision into scratch, then run as the
frozen checker runs them (`<rev> --repo <lane> --scratch <dir>`):

```
git show 7b86704d:.ufo/waves/round-59/count-c1.py > $S/pin/c1.py   # sha 2be6fda8…f0c9dfd
git show 7b86704d:.ufo/waves/round-59/count-c2.py > $S/pin/c2.py   # sha 2df3ae84…75877be
python3 $S/pin/cN.py 7b86704d7c0754a09958d131b64dbfa2a6d3eaed \
        --repo /home/vgpnk/Projects/shokunin/mori-shokunin --scratch $S/sN
```

| Run | shape varied | c1 rc | c2 rc | c1 stdout sha256 | c2 stdout sha256 |
|---|---|---|---|---|---|
| 1 | fresh scratch `s1`/`s3`, `PYTHONHASHSEED=0` | 0 | 0 | `167c9fed…bcdee4` | `4859d5ca…6caecb7` |
| 2 | fresh scratch `s2`/`s4`, `PYTHONHASHSEED=987654` | 0 | 0 | `167c9fed…bcdee4` | `4859d5ca…6caecb7` |
| 3 | `cwd=/tmp`, different `TMPDIR`, scratch `s5`/`s6` | 0 | 0 | `167c9fed…bcdee4` | `4859d5ca…6caecb7` |
| 4 | **reused** scratch dir, twice into the same path | 0 | 0 | identical | identical |

`cmp` reports no differences in every pairing; stderr was 0 bytes in all runs.
Committed receipts:

```
167c9fed…bcdee4  evidence/r59-c1-met.txt   == run output
4859d5ca…6caecb7  evidence/r59-c2-met.txt   == run output
```

Why this is structural, not luck: neither counter emits any
time/random/uuid/pid/hostname token (`grep -nE
'time\.|datetime|random|uuid|getpid|hostname|strftime'` on both: no match); every
set is consumed through `sorted` (`count-c2.py:132` `sorted({c[2] …})`,
`:362` `sorted(set(failed))`, `sid` loop over `sorted(sids)`); and no scratch or
absolute path reaches stdout — checked on the **unmet** branch too, where the
`failed=` list prints repo-relative paths only (`copy_absent:corpus/…`,
`scan_absent:.ufo/…`).

---

## 3. Read-surface audit — does `rev=` bind what is read?

`rev` is `argv[0]` in both counters (`count-c1.py:245`, `count-c2.py:436`) and is
echoed by the single result print (`count-c1.py:262-269`, printed at `:272`;
`count-c2.py:452-456`, printed at `:459`).
It is an **input echo, not a measurement**. Its binding power therefore rests
entirely on the counters reading nothing outside `rev`:

- `count-c1.py`: `git_show(repo, rev, …)` for `TOOL`, `SCORECARD.md`, every
  fixture file, the real-arm pointers, and `materialize()`; `ls-tree rev` for
  fixtures; `cat-file -e rev:path` for pointers. The one non-`rev` input is
  `mf = git_show(fleet, MANIFEST_REV, "MANIFEST.json")` (`:45`, `MANIFEST_REV`
  constant) — a constant *inside* the counter blob, so it is fixed by the
  content-addressed blob at `7b86704d`, not free.
- `count-c2.py`: every read is `git_show(repo, rev, …)` / `ls-tree rev`. The
  single `read_bytes()` (`:144` `fb_path = root / cfile`) reads
  `scratch/root2/<cfile>`, which was written from `git_show(repo, rev, cfile)`;
  it is a scratch copy of revision-pinned bytes, not a working-tree read.

No lane read escapes the pin in either counter. Therefore, given the counter blob
at `7b86704d`, a run byte-equal to a re-run at `7b86704d` cannot assert a verdict
that is false at `7b86704d`.

Verified fleet precondition for the one constant-rev read: `/home/vgpnk/Projects/
shokunin` is a git work tree, `2807c6ab…` is a commit there, and
`2807c6ab…:MANIFEST.json` exists.

---

## 4. Token-level analysis — could a receipt byte-equal yet lie about the revision?

Both receipts are one line; the `rev=` value is exactly 40 lowercase hex, one
trailing `\n`:

| receipt | bytes | `rev=` at | value span |
|---|---|---|---|
| `r59-c1-met.txt` | 96 | 51 | `[55,95)` |
| `r59-c2-met.txt` | 141 | 96 | `[100,140)` |

Three distinct senses of "lie about the revision", separated:

**(a) False measurement at the named revision — blocked.** Would require a read
outside the pin; §3 found none, and the counter blob is content-addressed at the
very revision it names.

**(b) Under-attribution — demonstrated, real.** The non-`rev` token vector is not
injective over revisions. Measured:

```
c1 vector identical (rev stripped) at: be737211 (7b86704d^), 7b86704d,
                                       ac496c7c, ddfb12fb, b3c25613
c2 vector identical (rev stripped) at: 7b86704d, ac496c7c, ddfb12fb, b3c25613
```

That span is not cosmetic: `git diff --stat 7b86704d b3c25613 --` over the
surfaces the counters read shows **69 files / 12,086 insertions** (65 r59 seat
reports added under `.ufo/waves/round-59/w1/`, `w1-results.json` +392,
`SCORECARD.md` +29, `corpus/SOURCES.md` +4). The receipts are byte-invariant
across all of it.

Exploit, executed and confirmed byte-exact:

```
sed 's/rev=7b86704d…a6d3eaed/rev=ac496c7cde8cad965079858accae3bedfe4a73f2/' \
    evidence/r59-c2-met.txt > relabel-c2-ac49.txt
python3 $S/pin/c2.py ac496c7c… --repo <lane> --scratch … > out-c2-ac49.txt
cmp relabel-c2-ac49.txt out-c2-ac49.txt   # → RELABEL_BYTE_EQUAL
```

So a 40-byte in-place edit turns the committed `7b86704d` receipt into a receipt
that byte-equals a fresh run at `ac496c7c`. The receipt bytes therefore attest
*truth at the named revision*, not *produced at the named revision*. This is the
precise content of "the `rev=` token is the only rev carrier": the token is a
label attached by the invoker; the vector carries no fingerprint of the tree.

**(c) Hand-typed forgery — indistinguishable, but not lying.** A receipt typed to
the expected output passes, because the checker's acceptance test is precisely
"this string is the counter's output at `7b86704d`". The check establishes the
string's truth; it cannot establish the file's provenance. That is the correct
reading of the C1 predicate — "exists at R and byte-equals a fresh re-run at
R59_DATA" is a reproducibility claim, and it is fully discharged.

Corollary worth recording: the counter's `rev=` token has **no grammar**. Verified
that `met` is emitted for non-identifying revs: `rev=HEAD` → `C1=met … rev=HEAD`
(c2 likewise), `rev=7b86704d` (short) → `met`. Unresolvable revs fail safe
(`rev=0000…0` and `rev=cfd554e…^` both → `unmet`, every arm bad), so `met` cannot
be obtained from a revision that does not resolve — but a `rev=HEAD` receipt is
time-dependent and would byte-equal a run at any future HEAD with the same
vector. Under the frozen instrument this is closed only because `count-c1.py`
always passes the literal `R59_DATA`; the r59 counters supply no such guard.

---

## 5. Does the frozen checker catch the relabel?

Acceptance path of `count-c1.py` `rerun_receipt` (`:121-140`) is exact and narrow:
materialize the counter from `R59_DATA` (`:48`), run it with `R59_DATA`,
`--repo <resolved lane>`, `--scratch` (`:130-135`), then only
`p.returncode != 0` → fail (`:136`) and `p.stdout != receipt_bytes` → fail
(`:138`). No `strip`, `splitlines`, or prefix match.

- relabeled-to-tip receipt vs run at `7b86704d` → `TAMPER_DETECTED` (bytes differ
  at the rev token), so a receipt that names a revision other than the run's
  argument cannot pass.
- frozen checker at tip: `C1=met dead-uncorrected=0 receipts=2/2 absent-set=5/5
  lesson=ok rev=b3c256138f00c704d5aa56eb0332d74506502ef2`, rc 0;
  `count-c1.py --selftest` → `C1_SELFTEST pass=6 fail=0`, rc 0.

Residual, currently empty gap: comparison is stdout-only. Both counters emit 0
bytes on stderr at `7b86704d`, so stderr blindness hides nothing today; it would
mask a counter that warned on stderr without changing its verdict.

---

## 6. Falsification attempts and outcomes

| Attempt | Target | Outcome |
|---|---|---|
| output depends on scratch path | path leakage | no absolute/scratch path in met or unmet output |
| output depends on `PYTHONHASHSEED` / set order | hash-ordered emission | 4 runs identical; all set iteration sorted |
| output depends on cwd / `TMPDIR` | env leakage | identical from `/tmp` with a different `TMPDIR` |
| output depends on stale scratch state | reused-dir carry-over | two passes into one dir identical |
| receipt is revision-identifying | relabel 40 bytes | **relabel succeeds** (§4b) |
| relabel passes the checker | `count-c1.py` arm | caught, `bytes_differ` |
| `met` from a bogus rev | rev grammar | `unmet` for `0000…0` and `…^`; `met` for `HEAD`/short revs |
| insensitive counter | pre-r59 revisions | vector changes (`C1=unmet … failed=tool_absent,selftest,fixtures_absent,scorecard,real,pointers`; `C2=unmet … claims=0 files=0`) — sensitivity exists, just not across the r59→r60 window |

---

## 7. Findings

**F1 — receipts are deterministic and byte-equal (PASS).** Four run shapes per
counter, exit 0, stdout sha256 stable and equal to the committed receipt bytes;
structural (no clock/pid/path tokens, sorted set iteration), not incidental.

**F2 — `rev=` is an input echo, not a measurement (confirmed, by design).** Both
counters print `argv[0]` verbatim (`count-c1.py:245` → `:269`;
`count-c2.py:436` → `:456`). Adequate for the C1 predicate, which asks for
reproducibility at a forced revision; inadequate as a provenance attestation.
Impact: bounded to reading the receipt as "generated at R" — it only supports
"true at R". Smallest safe correction: **none inside the frozen round** — adding
a surface digest token would change the frozen target output and trip the kill
rule. Recorded as a documentation limit; a future round could append a digest of
sorted `(path, blob-sha)` over the materialized reads, which would make the
vector revision-injective without changing any arm.

**F3 — the r59 counters do not validate the shape of `rev` (instrument gap, inert
here).** `met` is reachable with `rev=HEAD` and with a short rev; unresolvable
revs fail safe. The frozen receipts both carry full 40-hex equal to `R59_DATA`,
and the checker forces that literal, so nothing is at risk this round. Smallest
safe correction: none now; if the r59 counters are reused later, gate on
`re.fullmatch(r"[0-9a-f]{40}", rev)`.

**F4 — environment dependencies of the C1 receipt (portability note).** The r59
c1 counter reads the fleet repo through an absolute default
(`count-c1.py:246-247`) and `rerun_receipt` passes no `--fleet`, so reproduction
requires that fleet checkout at that path with `MANIFEST_REV` present (verified).
Inner tools are invoked as bare `python3` while the counter runs under
`sys.executable`; here both are `Python 3.14.8` at `/usr/bin/python3`. `git`
calls carry `timeout=120`; a timeout raises rather than silently diverging
(not observed; each full run finished in ~1 s). This is the r59 instrument's
absolute host path, consistent with the contract's statement that no **r60**
instrument carries one.

**F5 — stdout-only comparison (informational).** Exact byte comparison, no
normalization; stderr not compared and empty in both runs.

---

## 8. Reproduction

```bash
S=/fast/scratch/hyaku/mori-r60/Mo60Critic25
mkdir -p "$S"/{s1,s2,s3,s4,tmp,pin}; export TMPDIR=$S/tmp
cd /home/vgpnk/Projects/shokunin/mori-shokunin
R=7b86704d7c0754a09958d131b64dbfa2a6d3eaed
git show $R:.ufo/waves/round-59/count-c1.py > "$S/pin/c1.py"
git show $R:.ufo/waves/round-59/count-c2.py > "$S/pin/c2.py"
PYTHONHASHSEED=0      python3 "$S/pin/c1.py" $R --repo "$PWD" --scratch "$S/s1" > "$S/o1a"
PYTHONHASHSEED=987654 python3 "$S/pin/c1.py" $R --repo "$PWD" --scratch "$S/s2" > "$S/o1b"
cmp "$S/o1a" "$S/o1b" && cmp "$S/o1a" .ufo/waves/round-60/evidence/r59-c1-met.txt
PYTHONHASHSEED=0      python3 "$S/pin/c2.py" $R --repo "$PWD" --scratch "$S/s3" > "$S/o2a"
PYTHONHASHSEED=987654 python3 "$S/pin/c2.py" $R --repo "$PWD" --scratch "$S/s4" > "$S/o2b"
cmp "$S/o2a" "$S/o2b" && cmp "$S/o2a" .ufo/waves/round-60/evidence/r59-c2-met.txt
python3 .ufo/waves/round-60/count-c1.py b3c256138f00c704d5aa56eb0332d74506502ef2 --repo . --scratch "$S/cc1"
```

Expected: both `cmp` chains silent, `C1=met … receipts=2/2 … rev=b3c25613…`, rc 0.

Checks for Main to run after all seats land: `count-c1.py R`,
`count-c2.py R`, `count-c3.py R` plus the three selftests, at the settled R.
