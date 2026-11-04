# Mo87R02ReviewC2 — adversarial review of C2 (calibration)

seat: `Mo87R02ReviewC2` · lane: mori · round 87 · wave w1 · date 2026-11-04
claim under attack: **C2 calibration** — two replay-capable successors (`# replay: clone`,
`# supersedes:`) retire two of the three legacy r85 receipts, target
`C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6
defeated=1 superseded=2 legacy=1 unexpected=0` at `98f48dba3267a73714b862d0fd4fc8c0e82a1d04`.
freeze: `142542e0d853b4e8ec1aa1adb86708dc5786d9c0` · entering: `6fc09d69edbb11e5070ff33258de49f062c0fb9b`
C1 landing: `03b66a437e68d493ce0aacd1d80c321cc2e6bf7c` · A1 landing: `b9e6f68d887c570909c7bacc8bac86579d850d1d`

Lane repo: `/home/vgpnk/Projects/shokunin/mori-shokunin`. Detection and report only: no lane
file was edited, no git/jj mutation was run in the lane, no subagent was dispatched. All work ran
under `/fast/scratch/hyaku/mori-r87/Mo87R02ReviewC2/` (deleted before yield) using `git clone
--shared`; fixture commits used `-c user.name=t -c user.email=t@t` after asserting each clone's
`rev-parse --show-toplevel` equalled its own directory.

## Files/hashes actually read (recorded because siblings landed work while I ran)

Worktree at lane HEAD `728bc5f4` (later moved to `a42b1d79`; claim reads are pinned to git objects,
so unaffected):

| file | sha256 |
|---|---|
| `.ufo/waves/round-87/count-c2.py` (worktree = `b9e6f68d`, post-A1) | `264a43f04af1f9f939da7b3890f608a669a0c7fc2922656ee83f35adb236b14d` |
| `.ufo/waves/round-87/count-c2.py` (at `98f48dba`, pre-A1) | `e1dfd45a161b11a1ddfeae9bfe3d83f0f4f64c7d93dc0f85fc81d18e87ba7166` |
| `.ufo/waves/round-87/contract.md` | `bf208a448e096da4da5169e1b27db1b1ca97999119a2e43e49954c894042eb07` (identical at `b9e6f68d` and worktree) |
| `.ufo/waves/round-87/evidence/controls-r87.txt` | `53d65a426632acdb5c88721a2e7847110780e8c668f8c8fbd4b1bdd5df75e616` |
| `.ufo/waves/round-87/evidence/probe-r87.txt` | `530e35e6058edfa5d690343e149e53392e3daa81ea3f13f3fe7224f26db3180d` |
| `.ufo/waves/round-87/evidence/record-sweep-r87.txt` | `213a7558e155ea4eaeec8472767fa8371b44948e40b59cf9ac8437954641f4ac` |
| `.ufo/waves/round-87/evidence/claim-sweep-r87.txt` | `429a5dca94d32e14bd3614524fd9c441d682ba3986bceda4a98a0a4354a296b8` |

No receipt drifted between `98f48dba` and the worktree: `git diff --stat 98f48dba -- <all seven
population receipts>` printed nothing.

## Verdict in one paragraph

The supersede mechanics are **real**: all nine `# counter-sha256:` bindings verify at each
receipt's own `# rev:`; both `# replay: clone` successors reproduce their bodies byte-for-byte in a
fresh `--shared` clone at `25a74d4c` (rc 0); a one-field-stale successor stops superseding (the
legacy receipt stays `legacy`); and the `after-r85.txt` legacy reason is honest — its command does
not reproduce from committed bytes. The target tail itself is exactly what the counter prints at
`98f48dba`. Two defects remain, neither of which falsifies the supersede result but both of which
weaken the claim as written: **(F1)** the claim is not self-verifying at its named revision — the
counter *committed at* `98f48dba` still has `SUBJECT_ARMS = 11` and prints `C2=unmet … subject=selftest
arms=(13, 0)`; `met` exists only with the A1 counter that landed at `b9e6f68d`, one commit *after*
the successor data, so A1's "no C2 after-value existed" is false under the data reading; **(F2)** the
replay rule binds *body text = stdout of the named command*, not *named command = bound tool* — a
successor whose `# cmd:` is `printf '<body>'` while it keeps the real digest binding passes with
`C2=met … superseded=2 legacy=1`, so a vacuous successor can retire a legacy receipt. The committed
successors are not vacuous (I reproduced both from the bound sweep tools), so C2's data is honest;
the rule is what is weaker than its wording.

---

## Attack 1 — re-run the frozen counter and verify all nine bindings myself

All commands from `/home/vgpnk/Projects/shokunin/mori-shokunin`, `HYAKU_SCRATCH=/fast/scratch/hyaku/mori-r87/Mo87R02ReviewC2`.

```console
$ python3 -I .ufo/waves/round-87/count-c2.py --selftest
...
C2_COUNTER_SELFTEST pass=17 fail=0                      # rc 0

$ python3 -I .ufo/waves/round-87/count-c2.py 98f48dba3267a73714b862d0fd4fc8c0e82a1d04
RECEIPT after-r85.txt expect=met met problems=-
RECEIPT record-sweep-r85.txt expect=met met problems=-
RECEIPT claim-sweep-r85.txt expect=met met problems=-
REPLAY after-c1-r86.txt mode=required rc=0 exported=1
RECEIPT after-c1-r86.txt expect=met met problems=-
REPLAY replay-defeat-r86.txt mode=required rc=0 exported=1
RECEIPT replay-defeat-r86.txt expect=reject failed problems=replay-mismatch
REPLAY record-sweep-r87.txt mode=clone rc=0 exported=1
RECEIPT record-sweep-r87.txt expect=met met problems=-
REPLAY claim-sweep-r87.txt mode=clone rc=0 exported=1
RECEIPT claim-sweep-r87.txt expect=met met problems=-
C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=98f48dba3267
rc 0
```

Bindings — I recomputed each declared digest as `sha256(git show <receipt #rev>:<path>)` (git-show
bytes hashed directly; identical to `git show … | sha256sum`), 9/9 match:

| receipt | bound path | receipt `# rev:` | digest | result |
|---|---|---|---|---|
| after-r85.txt | `.ufo/waves/round-85/count-c1.py` | `25a74d4c…` | `da5fb27b9cd9b9cfbbefc58fb2465fb162f796cd280f82d0aeee0e8deca485fe` | OK |
| after-r85.txt | `.ufo/waves/round-85/count-c2.py` | `25a74d4c…` | `497738932080b8044142e5f49a8a4f3151ab16b876d77d25a8e0771785f8b918` | OK |
| after-r85.txt | `.ufo/waves/round-85/count-c3.py` | `25a74d4c…` | `43ad71d8104df29f1be8e3e0cef20d485e35a5f3f70d4994d70adc67b88a2724` | OK |
| record-sweep-r85.txt | `tools/mori-record-sweep.py` | `25a74d4c…` | `b8683be24e28ce4e79730b46615174d888af4c22ac7ee4fe16b97048516e8efa` | OK |
| claim-sweep-r85.txt | `tools/mori-claim-sweep.py` | `25a74d4c…` | `4ac6b52615a427d1f7d8993ab636a5830bcde744c4a51f22d9157833d940ba1d` | OK |
| after-c1-r86.txt | `.ufo/waves/round-86/count-c1.py` | `87644619…` | `1912e87d767aabfaec4aa46992d6212ce9e1f8945792057c8ab9d89651d675f1` | OK |
| replay-defeat-r86.txt | `.ufo/waves/round-86/count-c1.py` | `87644619…` | `1912e87d767aabfaec4aa46992d6212ce9e1f8945792057c8ab9d89651d675f1` | OK |
| record-sweep-r87.txt | `tools/mori-record-sweep.py` | `25a74d4c…` | `b8683be24e28ce4e79730b46615174d888af4c22ac7ee4fe16b97048516e8efa` | OK |
| claim-sweep-r87.txt | `tools/mori-claim-sweep.py` | `25a74d4c…` | `4ac6b52615a427d1f7d8993ab636a5830bcde744c4a51f22d9157833d940ba1d` | OK |

Nine binding *lines*, six distinct digests (the two successors bind the same tool bytes at the
same rev as the r85 receipts — correct: the successor replays the identical tool revision). All
receipt `# rev:` values (`25a74d4c`, `87644619`) are ancestors of `98f48dba`; `revs=7` is honest.

## Attack 2 — reproduce each successor body myself

Fresh `git clone --shared` of the lane, `checkout -q 25a74d4c34e8430e4fbb18d4038ef5db872fb0ee`
(toplevel asserted to be the clone dir), then the receipt's own `# cmd:` run with only
`GIT_CONFIG_GLOBAL/SYSTEM=/dev/null`, `PYTHONDONTWRITEBYTECODE=1`:

```console
record-sweep-r87.txt
  cmd: python3 -I tools/mori-record-sweep.py --root . --pins .ufo/waves/round-82/record-pins.json
  clone HEAD: 25a74d4c34e8430e4fbb18d4038ef5db872fb0ee
  rc=0  stderr=''
  stdout: 'RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0\n'
  body  : 'RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0'
  cmp: IDENTICAL

claim-sweep-r87.txt
  cmd: python3 -I tools/mori-claim-sweep.py --root . --pins .ufo/waves/round-80/claim-pins.json
  rc=0  stderr=''
  stdout: 'CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=4 pointers=266\n'
  body  : 'CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=4 pointers=266'
  cmp: IDENTICAL
```

Both successors replay **rc 0, zero difference** at rev `25a74d4c`, and the clone stayed clean
(`git status --porcelain` empty). The `claim-sweep-r87` `# limits:` statement is also true: the r85
receipt's body reads `pointers=274`, the replay at the same rev reads `266`, so the older count is
not reproducible from committed bytes.

I also replayed the wave's post-landing receipt `after-r87.txt` (which appeared at HEAD `728bc5f4`)
in a clone at its `# rev:` `b9e6f68d`: rc 0, byte-identical to the recorded body, last line
`C2=met … rev=98f48dba3267`; its two bindings (`e2ff9687…` count-c1, `264a43f0…` count-c2 at
`b9e6f68d`) verify. That receipt states the canonical form correctly: **counter at `b9e6f68d`,
C1 subject `03b66a43`, C2 subject `98f48dba`**.

## Attack 3 — try to supersede with a successor whose replay fails

Fixture A: clone at `98f48dba`, change the record successor's body by **one field**
(`carriers=1` → `carriers=2`), commit, run the frozen counter at the fixture rev:

```console
REPLAY record-sweep-r87.txt mode=clone rc=0 exported=1
RECEIPT record-sweep-r87.txt expect=met failed problems=replay-mismatch
RECEIPT claim-sweep-r87.txt expect=met met problems=-
C2=unmet receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=5 defeated=1 superseded=1 legacy=2 unexpected=1 detector=green rev=c80a707904db
rc=1
```

`superseded` dropped 2 → 1 and `legacy` rose 1 → 2: `record-sweep-r85.txt` — named only by the
now-unclean successor — **stays `legacy`**, exactly as required. `claim-sweep-r85.txt` is still
retired by its clean successor.

Fixture B: both successor bodies one field stale (`revisions=0` → `9`, `pointers=266` → `267`,
body only — the first, accidental mutation of the `# limits:` line was rejected as a probe because
the rule does not read limits semantically):

```console
C2=unmet receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=4 defeated=1 superseded=0 legacy=3 unexpected=2 detector=green rev=306c80363da5
rc=1
```

`superseded=0 legacy=3` — a failed successor supersedes nothing, matching the frozen header-only
control's counts (`superseded=0 legacy=3 unexpected=2`, rc 1). **The supersede rule does bind the
replay.**

The wave's own `supersede-controls-r87.txt` (landed at HEAD, read only) reports the same shape for
a presence-based pre-fix call site; my fixture independently reproduces the fixed behaviour with the
committed counter, so the control's claim is corroborated, not merely restated.

## Attack 4 — interrogate the `after-r85.txt` legacy reason

The contract says `after-r85.txt` stays `legacy` because its body is a live-observation run
(`count-c3` observes the census three times). I ran its exact `# cmd:` once in a clone at its
`# rev:` `25a74d4c` (read-only; 2.6 s):

```console
$ bash -c "python3 -I .ufo/waves/round-85/count-c1.py 25a74d4c…; python3 -I .ufo/waves/round-85/count-c3.py 25a74d4c…"
rc=1
MUTANT count-c1.py X1_killed_rescued_as_equivalent killed rc=1
MUTANT count-c1.py X2_coupling_duplicate_passes killed rc=1
C1=met mutants=2 killed=2 survivors=0 total=2 arms=17 r84=met rev=25a74d4c34e8
C3=unmet observed=3 aa=stable subject=unmet rc=1 rev=25a74d4c34e8
C2=unmet snapshot=bound asof=1 tokens=64 agreed=64 residual=0 live=derived live_tokens=52 live_agree=45 delta=classified classified=71 union=71 absent_live=19 added_live=7 class_changed=0 deltas=26 rev=25a74d4c34e8
```

versus the recorded body:

```text
C1=met mutants=2 killed=2 survivors=0 total=2 arms=17 r84=met rev=25a74d4c34e8
rc=0
C3=met observed=3 aa=stable own_tokens=64 subject_tokens=64 subject_deltas=0 unmatched=0 unnamed=0 detector=green rev=25a74d4c34e8
rc=0
```

What differs, precisely:

1. **Exit/status:** replay `rc=1`; the body implies `rc=0`.
2. **The C3 leg is live and now unmet:** `count-c3` runs `tools/mori-census.sh` three times from
   R's own bytes and reconciles the census against its subject (`.ufo/waves/round-83/count-c2.py`);
   the subject now reads `live_tokens=52` where the recorded run read 64, so `subject=unmet` and
   the counter exits 1. This is genuine live-state drift, not a clone artifact (the clone is
   `status --porcelain` clean and all inputs are committed bytes at `25a74d4c`).
3. **The body is not the command's stdout at all:** the two standalone `rc=0` lines are printed by
   neither r85 counter — `count-c1.py` contains no `print(…rc=…)`, and `count-c3.py` prints
   `rc=%d` only on its **unmet** branch. A harness wrote them. The replay also emits an extra
   `C2=unmet …` line that the body lacks. So even if the live census happened to match, the body's
   byte form could not be reproduced by this `# cmd:`.

Verdict: **"live observation" is the true reason, not an excuse** — the command really is
live-state dependent and really does not reproduce. It is an *incomplete* reason: the recorded body
also carries harness `rc=0` lines that are not the command's stdout, which is a second,
undocumented non-replayability cause. The contract's stronger form ("no committed-byte successor
can reproduce it") is fair for the live leg, but the honest accounting should add the wrapper-line
cause. The r87 successors fix exactly this: their bodies are pure stdout.

## Attack 5 — was the population widened to hide a receipt?

```console
$ git diff --name-status 6fc09d69 98f48dba -- .ufo/waves/round-85/ .ufo/waves/round-86/
M	.ufo/waves/round-86/count-c1.py
M	.ufo/waves/round-86/count-c2.py
M	.ufo/waves/round-86/count-c3.py
```

No round-85 path changed; no `.txt` receipt changed anywhere in either tree (the three `.py` files
are C1's subject edits, not receipts). Full diff `6fc09d69..98f48dba`: those three `M` plus the new
`.ufo/waves/round-87/` contract, two counters, and four evidence files (`A`). The population tuple
is byte-identical at freeze `142542e0` and tip `b9e6f68d` (7 rows, 3 legacy / 2 required / 2 clone,
1 reject); the counter file is unchanged `142542e0..98f48dba`, and `TARGET` is byte-identical at
freeze, `98f48dba` and `b9e6f68d`. The two successors name `record-sweep-r85.txt` and
`claim-sweep-r85.txt` only; `after-r85.txt` is named by nobody. **No receipt was dropped, renamed
or widened away.**

---

## Findings by severity

### F1 — High (calibration reproducibility): the target is not printable from the counter committed at the claim's named revision

Measured, in a clean `git clone --shared` checked out at `98f48dba`:

```console
$ cd clone-at-98f48dba && python3 -I .ufo/waves/round-87/count-c2.py 98f48dba3267a73714b862d0fd4fc8c0e82a1d04
…
C2=unmet receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 subject=selftest arms=(13, 0) labels=True rev=98f48dba3267
rc=1
```

The same holds with the counter frozen at `142542e0` grading `98f48dba` — identical `unmet` line.
Cause: `98f48dba^` is C1's `03b66a43`, which moved `.ufo/waves/round-86/count-c2.py` to 13 arms;
the r87 counter at `98f48dba` still declares `SUBJECT_ARMS = 11` and an 11-label tuple. A1
(`SUBJECT_ARMS = 13`, two labels) landed at `b9e6f68d`, which is a **child** of `98f48dba`. With
the counter at `b9e6f68d`, `python3 -I .ufo/waves/round-87/count-c2.py b9e6f68d` prints
`C2=met … rev=b9e6f68d887c rc 0`, and the committed `after-r87.txt` (`# rev: b9e6f68d`, C2 subject
`98f48dba`) replays byte-identically. C1 has no such gap: `count-c1.py` at `03b66a43` grading
`03b66a43` prints `C1=met … arms=54 rc 0`.

Consequences:
- P-C2's sentence "At revision R `python3 -I .ufo/waves/round-87/count-c2.py R` prints `C2=met …`"
  is **false** at R = `98f48dba` when the counter is read from R (`met` appears only with the
  `b9e6f68d` counter). The claim needs the canonical grading revision stated explicitly; the after
  receipt already uses the defensible form (counter `b9e6f68d`, subject `98f48dba`), but the
  contract and the claim sentence do not.
- A1's timing sentence "before any C2 after-value existed" is inaccurate under the data reading:
  the successor receipts — the C2 after-value's data — were committed at `98f48dba`, one commit
  before A1. What did not exist before A1 was the measured `C2=met` line. The amendment is inside
  its promised scope otherwise: target string, population, supersede rule and kill rule are
  unchanged (verified), and the graded tail is identical pre- and post-A1 — only the subject
  sub-gate and the `met` word move.
- Fix options: (a) name `b9e6f68d` as the grading revision (counter + receipt) and `98f48dba` as
  the C2 subject, as `after-r87.txt` already does; or (b) land the successors after A1 and re-measure
  so the named revision carries both; plus correct A1's timing sentence to "before any C2
  after-value was measured".

### F2 — Medium (rule strength): the replay binds the body to the named command, not the command to the bound tool

`header_fields()` collects `# counter-sha256:` bindings unconditionally; `grade_population()` hashes
each binding path at the receipt's `# rev:`; `replay_body()` independently runs `fields["cmd"]`.
Nothing cross-checks that the executed command is the bound artifact. Fixture (clone at
`98f48dba`), replacing only the record successor's `# cmd:` with a literal printer while keeping
the genuine `tools/mori-record-sweep.py` binding:

```console
# cmd: printf 'RECORD_SWEEP pending=0 pinned=0 carriers=1 bindings=3 revisions=0\n'
# rev: 25a74d4c34e8430e4fbb18d4038ef5db872fb0ee
# counter-sha256: b8683be24e28ce4e79730b46615174d888af4c22ac7ee4fe16b97048516e8efa tools/mori-record-sweep.py
# replay: clone
# supersedes: record-sweep-r85.txt
…
C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=47217847f6aa
rc=0
```

So a vacuous successor retires a legacy receipt and the full target line passes. The committed
successors are **not** vacuous — their `# cmd:` names the exact tool their digest binds, and I
reproduced both (Attack 2) — so C2's data is honest; the *rule* would accept a counterfeit. Note
the same decoupling exists in an accepted legacy receipt: `after-r85.txt` binds
`.ufo/waves/round-85/count-c2.py` although its `# cmd:` never runs it, so bindings are declared
provenance, not proof of execution. Routed defect for round 88: require every `# counter-sha256:`
path (or at least the executed tool) to appear as a token of `# cmd:`, and add a selftest arm for the
vacuous case.

### F3 — Medium-low (hermeticity): the two `# replay: required` receipts replay against the live lane path, not the checkout

`after-c1-r86.txt` / `replay-defeat-r86.txt` carry
`--repo /home/vgpnk/Projects/shokunin/mori-shokunin`. `export_rev()` skips that absolute token
(it fails `PATHISH`), so in required mode only `.ufo/waves/round-86/count-c1.py` is exported and the
command still points at the host lane. Measured in an export-only directory:

```console
$ bash -c "<exact after-c1-r86 cmd>"        # cwd = dir containing only the exported .py
rc=0, first line: MUTANT count-c3.py H-C3-metverdict killed rc=1
$ bash -c "<same cmd, --repo /nonexistent/lane>"
rc=2, stderr: C1_SETUP unresolvable revision 87644619078308ee523cd0c976c72bf079b0ff77
```

So `replay=4 matched=6` holds on this host because the lane path exists and contains the rev; in a
relocated checkout the two r86 receipts would fail and the target would read unmet. Git objects are
content-addressed, so no byte substitution risk — this is portability/environment dependence, and
a verifier reproducing C2 off-host must restore that path or expect `replay-rc`. The two r87
successors are hermetic (clone mode, relative paths); verified.

### F4 — Low (inconsistent replay handling): a legacy-population receipt declaring `# replay: clone` is counted but never replayed

Only `required` is promoted for legacy rows (`if mode == "legacy" and fields["replay"] ==
"required"`); `clone` leaves the mode at `legacy`, so no replay runs, yet the row increments
`replay=`. Fixture: adding `# replay: clone` to `record-sweep-r85.txt`:

```console
RECEIPT record-sweep-r85.txt expect=met met problems=-     # no REPLAY line
C2=unmet receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=5 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 detector=green rev=eb6424b96ac4
rc=1
```

Only the frozen `replay=4` count catches it; the receipt itself is treated as clean without its
declared replay. Asymmetric with `required` and a latent way to display a replay that never ran.

### F5 — Low (arm label overstates its reach): `supersede_absent_target` does not test an absent target, and the `SUPERSEDE … absent=1` branch is unarmed

`cases.append(("supersede_absent_target", not supersede_verdict("old.txt", set(), [("new.txt",
"old.txt")]), "absent"))` exercises the *unclean-successor* path, not an absent target. The branch
`if target not in known: … "SUPERSEDE %s target=%s absent=1"` has no arm (the string `absent=1` does
not occur in `selfcheck`). A target-blind mutant
(`target == legacy_name` → `True`) is still killed — `FAIL supersede_wrong_target` — so the rule is
not unguarded, but this arm does not prove what its name claims. This corroborates the round-87
lesson's own routed defect (round 88).

### F6 — Informational: the frozen controls are run receipts, not re-runnable fixtures

`controls-r87.txt` cites fixture revisions `bc108f00a111` (label-only) and `bc319680dc8e`
(header-only); neither resolves in the lane (`git cat-file -e` fails — they were scratch clones).
The control text cannot be re-executed as recorded. I reconstructed equivalent fixtures instead:
the pre-A1 counter at `142542e0` grading `6fc09d69` reproduces the entering control **byte for
byte** (`C2=unmet receipts=5 absent=2 bindings=7 bound=7 revs=5 limits=5 cmd=5 summary=5 replay=2
matched=4 defeated=1 superseded=0 legacy=3 unexpected=0 detector=green rev=6fc09d69edbb`, rc 1),
and the both-stale fixture reproduces the header-only control's counts
(`superseded=0 legacy=3 unexpected=2`, rc 1).

### F7 — Informational: `# limits:` is token-checked, not content-checked

The limits gate is only `'limit' in text.lower()` and ≥3 words. A stale or false limits sentence
passes; my accidental edit of `claim-sweep-r87`'s limits line (`reads pointers=266` → `267`) left the
receipt clean. `limits=7` therefore counts present declarations, not verified ones.

---

## Residual risk and verification gaps

- **Same-host verification.** All replays ran on the host that holds the lane; F3 means the two
  required-mode replays are not host-independent. The r87 successors are host-independent.
- **Live-census side effect:** the after-r85 replay ran `tools/mori-census.sh` three times inside a
  scratch clone (2.6 s, no lane writes; clone `status --porcelain` clean afterwards). I did not run
  the census again beyond that single probe.
- **Control fixtures not re-executed:** F6; I reproduced counts with equivalent fixtures, not the
  recorded revisions.
- **Lane moved under me:** HEAD went `b9e6f68d` → `728bc5f4` → `a42b1d79` while I reviewed
  (siblings landed `after-r87.txt`, `supersede-controls-r87.txt`, lesson/SCORECARD edits; one
  uncommitted `corpus/lessons/round-87.md` modification exists). All claim-level reads are pinned to
  git objects, and I touched no lane file. I read the sibling-authored `after-r87.txt` and
  `supersede-controls-r87.txt` as evidence only; the replays and binding checks above are my own.
- **Scope:** I did not verify the sweep tools' semantics (whether `mori-record-sweep.py` /
  `mori-claim-sweep.py` compute the right thing), only that their committed bytes produce the
  recorded bodies. The claim binds no more than that. `matched=6` counts the two superseded legacy
  receipts as matched (they are clean); that is naming, not a defect.
- **Not attacked:** `resume_continuity_v1` and unrelated lane surfaces; this review is C2-only.

## Tooling

No tool was installed or upgraded (no pacman, no `uv tool`, no downloads). Only `python3`, `git`,
`sha256sum`, `bash`, and the lane's committed scripts were used.

## Scratch

`/fast/scratch/hyaku/mori-r87/Mo87R02ReviewC2/` (clones, fixtures) deleted before yield.
