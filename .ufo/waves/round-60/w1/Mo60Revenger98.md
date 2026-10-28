# Mo60Revenger98 — r59 Sentinel57 F1 chain vs the r60 counters (round 60, w1)

Mode: read-only on the lane; every PoC is a throwaway `git init -q` repo under
`/fast/scratch/hyaku/mori-r60/Mo60Revenger98/` (cleaned before yield). Every
re-derivation is pinned: r59 counter/artifacts at data rev
`7b86704d7c0754a09958d131b64dbfa2a6d3eaed`, r60 counters at lane tip
`b3c256138f00c704d5aa56eb0332d74506502ef2` (working-tree bytes; the three r60
counters were unchanged by the C1 data commits, `git show R:path` == worktree).
No lane VCS mutation, no production edits, no fleet/sibling writes, no subagents.

Byte identity checks used before citing r59 line numbers:

```
sha256(.ufo/waves/round-59/count-c2.py @ worktree) = 2df3ae84f6d66f9ee46cd46cf2cb199ca85e7400301c5a0e9dd94b7b375877be
sha256(git show 7b86704d:…/count-c2.py)           = 2df3ae84…877be   (equal)
```

Verdict: **all three F1 steps are closed at the r60 tip**, on the same PoC
objects, with the r59 hole reproduced as a live control (no inference). Two
residuals, neither a predicate failure, are listed at the end.

---

## Step 1 — does an unpinned tool blob execute?

### r59 behaviour (hole)

`count-c2.py` computes the pin verdict and then executes on *presence*, not on
`tool_ok`:

| line | code | effect |
|---|---|---|
| 198-199 | `tool_b = git_show(repo, rev, TOOL)` / `tool_ok = … sha256(tool_b) == PIN` | pin computed |
| 205-206 | `if tool_b is not None: tp.write_bytes(tool_b)` | **unpinned bytes written** |
| 209-214 | `if tool_b is not None: subprocess.run(["python3", str(tp), "--selftest", …], env={**os.environ, …})` | **unpinned bytes executed** |
| 233-236, 257-259 | scan + drift subprocesses on the same `tp` | executed again |

`tool_ok` only feeds `if not tool_ok: failed.append("tool_sha")` (200-202) and the
final AND (360). Fail-closed at the verdict, fail-open at the effect.
Same defect class in `count-c1.py` (`97-106`, `112-115`, `run_tool()` at 152/183/194).

Reproduction (my PoC repo `poc-exec`, rev `0147d3ea…`, supplies
`tools/mori-entry-claims-check.py` + `tools/mori-settlement-scan.py` = a blob that
writes `EXEC-MARKER` under its `--scratch` parent and prints both selftest lines):

```
python3 r59-c2-at-data.py 0147d3ea… --repo <poc-exec> --scratch …/g1-old2
C2=unmet | flags: ['selftest=ok', 'tool_sha'] | markers: [g1-old2/st2/EXEC-MARKER]
marker content: "pwn --selftest --scratch …/g1-old2/st2"
```

i.e. `selftest=ok` **and** `tool_sha` in `failed=` in one run — the unpinned blob
ran. (`engine`: `count-c2.py:209-214`.)

### r60 kill

`count-c2.py` funnels every execution through one gate:

- `144-153 def run_pinned(tool_path, args, expect_pin, blob, scratch)`:
  `if blob is None or sha256(blob) != expect_pin: return None, False` — the sha
  compare **precedes** `subprocess.run(["python3", str(tool_path)] + args, …)`.
- materialisation is itself pin-gated: `168-169` `if ec_b is not None and ec_ok:
  ec_path.write_bytes(ec_b)  # materialize only when pinned`; `178-179` same for
  `scan_path`.
- all five exec sites go through `run_pinned`: `183-190` (entry-checks selftest),
  `212` (real scan), `235` (drift), `258` (renamed r54 control), `310`/`382`
  (entry arm, tree arm).
- `count-c1.py` has no repo-tool exec site at all; its one non-git subprocess is
  `rerun_receipt()` (`127-136`), whose bytes come from
  `git_show(R59_DATA, counter_rel)` — revision-pinned, not rev R, not the worktree.
- `count-c3.py` `163-183` (`g1-new`) asserts the effect, not just the token:
  `no_exec = len(markers_under(s_new)) == 0` and `gated = "tool_sha" in out and
  "tool_absent" not in out`.

Observed, same PoC repo, same rev:

```
python3 count-c2.py 0147d3ea… --repo <poc-exec> --scratch …/g1-new2
C2=unmet | flags: ['selftest=bad', 'tool_sha'] | markers: []
```

The discriminator is the side effect: r59 `selftest=ok` + marker; r60
`selftest=bad` + no marker anywhere under its scratch (recursive `rglob`).
Both counters are equally honest in the verdict — the hole was never the verdict.

Control arm (the hole is real, not a dead PoC): `count-c3.py:185-199` (`g1-old`)
runs the r59 counter against the identical PoC and requires the marker:

```
python3 count-c3.py b3c25613… --scratch …/c3
C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=b3c25613…
find …/c3 -name EXEC-MARKER  →  g1-old/st2/EXEC-MARKER   (only under g1-old)
```

---

## Step 2 — does materialisation escape the scratch root?

### r59 behaviour (hole)

No `materialize()` exists. Writes are a bare join plus `write_bytes`, so a
symlink planted at the target path is followed out of the containment root:

- `282-294`: `root = scratch / "root2"`; `292 f = root / rel`;
  `293 f.parent.mkdir(parents=True, exist_ok=True)`; `294 f.write_bytes(b)`.
- `343-345`: tree arm `fp = tr / rel; fp.parent.mkdir(...); fp.write_bytes(b)`.
- Ordering makes it reachable: the tool runs at `209-214` (and 235/258) *before*
  these writes, so the repo blob can plant the symlink at the exact path.

Classic `..` traversal is only incidentally closed (git refuses `..` tree paths);
the live sink is symlink-following.

Reproduction (`poc-symlink`, rev `03065a4c…`; tool blob (sha ≠ PIN) creates
`<scratch>/root2/corpus/knowledge/wave-settlement-artifacts-r59.md` →
`…/victim/secret.txt`, victim pre-filled `ORIGINAL-VICTIM`; repo also carries
ENTRY/SOURCES/6 copies so the write arm runs):

```
python3 r59-c2-at-data.py 03065a4c… --repo <poc-symlink> --scratch …/g2-old
C2=unmet … entry=ok rows=ok pins=ok …            (the tool ran: selftest=ok)
--- victim after ---
source: S553 — committed wave-results artifact … (the ENTRY blob, verbatim)
lrwxrwxrwx wave-settlement-artifacts-r59.md -> …/Mo60Revenger98/victim/secret.txt
```

A repo-supplied blob rewrote a file outside the counter's `--scratch` root, then
the counter read that victim back as its own entry (`entry=ok`).

### r60 kill

- `114-130 def contained(root, target)`: walks every component from `t` up to
  `root` and returns `False` on any `is_symlink()`, then
  `resolved = t.resolve(strict=False)` and
  `resolved == root_r or resolved.is_relative_to(root_r)`; otherwise `False`.
- `132-141 def materialize(root, rel, blob)`: `if not contained(root, t): return
  False` before `t.parent.mkdir` / `t.write_bytes`.
- Every repo-controlled write goes through it: `202-207` (real scan), `234-237`
  (drift), `257` (renamed control), `301` (entry arm), `375-377` (tree arm, with
  `failed.append("containment:tree:%s" % name)`); the two pinned tool writes
  (169, 179) are fixed basenames under scratch.
- `count-c3.py:202-231` (`g2`) asserts both refusals **and** absence of the
  escaped artifacts: `not (g2.parent/"escape.txt").exists()` and
  `not (g2/"nowhere"/"f.txt").exists()`.

Observed (direct module probe with the tree-wide `count-c2.py` at HEAD):

```
parent_escape:   False      inside:          True
symlink_parent:  False      abs_path(/etc/x): False
nested_dotdot('a/../../escape2.txt'): False
outside_escape_exists: False   escape2_exists: False   inside_written: b'x'
existing_file_symlink_target: False    dirlink_out_child: False
dirlink_out_newfile: False             plain_new_file: True
victim_unchanged: ORIG                 outside_new: False
contained(g,g): True
```

Composite: `C3=met … containment=ok` (receipt above). The r59 write path no
longer exists in the r60 counter: there is no `root / rel` + `write_bytes` pair.

---

## Step 3 — is `expect.txt` trusted as its own oracle?

### r59 behaviour (hole)

The hostile-tree arm reads the expectation out of the tree it is scoring, then
uses it as ground truth:

- `328 exp_b = git_show(repo, rev, base + "/expect.txt")` — bytes supplied by the
  scored revision;
- `333 expect = [e for e in exp_b.decode().strip().split(",") if e]`;
- `347 want_ok = not expect`; `348 if ok != want_ok: … verdict`; `350-352`
  `all(any(r.startswith(e) for r in reasons) for e in expect)`.

So the repository decides both the target and the acceptance rule: a tree that is
not hostile at all, labelled with an empty `expect.txt`, satisfies the arm.

Reproduction (`poc-selfcert`, rev `9edbdd38…`): all real r59 artifacts/entry/
SOURCES at `7b86704d` plus **one** tree `.ufo/waves/round-59/trees-c2/t13-selfcert`
whose content is the verifier's own synthetic *good* entry (10 claims, 3 copies,
mined S901 row — generated by the pattern in `count-c2.py --selftest`) and whose
`expect.txt` is 0 bytes:

```
python3 r59-c2-at-data.py 9edbdd38… --repo <poc-selfcert> --scratch …/g3-selfcert2
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6
exit=0
wc -c …/t13-selfcert/expect.txt → 0
```

`C2=met` with a do-nothing "hostile" tree in the set. The arm's evidence is the
artifact under audit — the r59 depth claim `trees=ok` is not self-supporting.

### r60 kill

Two independent locks in `count-c2.py`:

- names are frozen in the counter, not discovered: `83-97 FROZEN_EXPECTS` (13
  entries) and `348-351 if sorted(tdirs) != sorted(FROZEN_EXPECTS):
  failed.append("trees_set")` — an added/hidden tree is a membership failure;
- per-tree bytes are frozen: `352-366 frozen = FROZEN_EXPECTS.get(name)` →
  `if exp_b.decode().strip() != ",".join(frozen): failed.append("expect_tamper:%s" % name)`.

Verified the frozen table is the committed table (13/13 the same):

```
frozen_count: 13   mismatches: []   json( trees-c2h-expects.json ) == counter table: True
```

Observed on two PoC repos:

```
# tampered h02 expect.txt = "grammar\nTAMPERED-EXTRA"
C2=unmet … failed=…,expect_tamper:h02-malformed-claim,trees_set

# all 13 committed trees + an extra self-certifying t13-selfcert (empty expect)
C2=unmet … failed=…,tree:t13-selfcert:frozen,trees_set
```

and `count-c3.py:232-253` (`g3`) asserts the exact token
`expect_tamper:h02-malformed-claim` on the frozen h02 path
(`TAMPER_REL`, `FROZEN_H02 = "grammar"`, 58-59). Composite: `expectgate=ok`.

---

## Composite receipts at the r60 tip (read-only runs)

```
$ python3 .ufo/waves/round-60/count-c2.py b3c256138f00c704d5aa56eb0332d74506502ef2 --scratch …/c2-head
C2=met selftest=ok scan=ok drift=ok trees=ok entry=ok rows=ok pins=ok tree=ok claims=13 files=6 spans=13 rev=b3c25613…      exit=0
   (byte-equal to the contract's frozen target output)

$ python3 .ufo/waves/round-60/count-c3.py b3c256138f00c704d5aa56eb0332d74506502ef2 --scratch …/c3
C3=met toolgate=ok containment=ok expectgate=ok cases=6 rev=b3c25613…                                                       exit=0
   EXEC-MARKER present only at c3/g1-old/st2/EXEC-MARKER (the r59 control arm)
```

The bytes the counters above validated are the bytes count-c3 pins:

```
sha256(.ufo/waves/round-60/count-c1.py @ b3c25613) = 795c1f31…215ddbae = PIN_C1
sha256(.ufo/waves/round-60/count-c2.py @ b3c25613) = 8c4814f5…8e8e3ccdf976 = PIN_C2
sha256(.ufo/waves/round-60/count-c3.py @ b3c25613) = fabde06c…d5153514 (worktree == committed)
```

Do-nothing control already committed, `evidence/control-c3-do-nothing.txt`:
`C3=unmet toolgate=bad containment=bad expectgate=bad cases=1
rev=ddfb12fb… failed=count_c1_absent,count_c2_absent,g1_new_skipped,g2_skipped,g3_skipped`.

---

## Residuals (reported, not predicate failures)

1. **G2 is check-then-write, not `O_NOFOLLOW`.** `materialize()` (`132-141`) checks
   then writes; the guarantee holds only while no adversary code runs between the
   check and the write. Since every exec site is now sha-gated (`run_pinned`), no
   repo code runs inside the counter at all — the window is closed by ordering, not
   by the filesystem flag. A future exec site reintroduced outside `run_pinned`
   would silently reopen it.
2. **C1's receipt arm is revision-pinned, not sha-pinned.** `count-c1.py:123-136`
   executes `git show(R59_DATA, counter_rel)`; immutability rests on git object
   hashing of `7b86704d…`, and the executed r59 counter itself still contains the
   step-1/2 fail-open pattern — harmless only because it is pinned to a revision
   whose tool blob is the honest one (`4c04bf21…`). If `R59_DATA` ever moves, the
   hole returns with it.

Also noted (not a defect in scope): `contained()` is deliberately over-strict — it
refuses *any* symlink component, including one that resolves inside the root
(`inside_resolving_symlink: False`, nothing written), and `dirlink_out_child:
False` for a directory symlink whose target is the root's own ancestor (`base`).
Both are safe-direction refusals; only the first is stricter than necessary.

## Method limits

- Behavioural claims rest on runs against my own PoC repos; no lane content was
  mutated, and the honest lane's counter receipt (`C2=met`) was reproduced
  independently at the tip.
- r59 line numbers cite the worktree file, proven byte-identical to
  `7b86704d:…/count-{c1,c2}.py`.
- No tool installation or update was performed (nothing needed); nothing added to
  PATH, no pacman, no network.
- Concurrent-lane observation (not mine, not touched): at yield time
  `git status --porcelain` in the lane shows ` M corpus/lessons/round-60.md` in
  addition to the pre-existing untracked round-60 w1/evidence entries. That edit
  belongs to another live seat (C1 data lands during this wave). Every claim above
  reads committed objects (`git show <rev>:path`), and the three r60 counter files
  were sha-verified worktree==committed, so the modification does not affect any
  line pointer or measurement in this report.
