# Mo56SentReceipts — freeze integrity: pin lines and registry anchor cells

Seat: Mo56SentReceipts (leaf, no subagents). Lane: `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Freeze tip under test: `8be2717b0809281d07dffe83dad424a4859e0747`. Entering tip: `5b295eeebd87ebd610d8d39bfe2035742f740cfa`.
Data commits: `c419fe6d`, `6ced9da9b1f9c65065a8158735e0331938e8a599`. Lane HEAD at the time of this run: `acc62f54fb0f53b47b428594dc27365150cbd76b` (three integration commits past the freeze tip).
Scratch: `/fast/scratch/hyaku/mori-r56/Mo56SentReceipts/` (created, used, removed before yield; one `git archive` extraction of `8be2717b`, no clone, no `git add/commit/checkout/reset`, no jj command, no pacman, no install).

## Verdict on the assigned claim

Every one of the six sha256 pin lines in `.ufo/waves/round-56/evidence/freeze-sha256.txt` matches the bytes at the revision the line names, and both registry anchor cells match the committed copies. **No pin or cell mismatch exists on the assigned set.** The defects found are in how the manifest is *checkable* and *attributed*, and in what two receipts claim to have observed — not in the frozen bytes.

## 1. Pin recomputation (contract, counters, controls)

Manifest is 12 lines; lines 3-6 pin `contract.md`, `count-c1.py`, `count-c2.py`, `controls/controls.py`; lines 8-9 pin the two tools; lines 11-12 pin the two source copies.

Command (per path, at the freeze tip):

```
git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 8be2717b0809281d07dffe83dad424a4859e0747:.ufo/waves/round-56/<path> | sha256sum
```

| manifest line | path | expected (manifest) | observed at 8be2717b | result |
|---|---|---|---|---|
| 3 | `contract.md` | `088761f3f05c85ab644f8a1f91cb561a5cbfc2036acc536e08ebc48ec849bd3c` | `088761f3…49bd3c` | match |
| 4 | `count-c1.py` | `c4e58eedadda2f7069bb8f31c5b1b6ae527a54aecaa7490308a55f127047f71d` | `c4e58eed…47f71d` | match |
| 5 | `count-c2.py` | `4b350c773a3c31e54cf2cb0e3d7a5c8e92d9a1101722c9a94f53db2492812465` | `4b350c77…812465` | match |
| 6 | `controls/controls.py` | `5bf65ac0d7e70a5a4d295d52ad00186070adbef12512d1c457f73716b2a6d491` | `5bf65ac0…b2a6d491` | match |
| 8 | `tools/mori-driver-liveness.py@6ced9da9` | `6b3dba74c639190e7e96b6bed8e6ac8f285a51ce6d910fbe92e6dd39bf7be997` | `6b3dba74…f7be997` at `6ced9da9`, also at `3f494b49`, `8be2717b`, and the working tree | match |
| 9 | `tools/mori-vote-bind.py@6ced9da9` | `8be1acdbb36cd68deba005e21a4a8679534ab5a5099a787aa9335d288dfa6bca` | `8be1acdb…dfa6bca` at `6ced9da9`, also at `c419fe6d`, `3f494b49`, `8be2717b`, and the working tree | match |

Exit code of the loop: 0. The manifest file itself is committed at the freeze tip with the same bytes as the working tree (`sha256sum` of both = `aacfd231b11323e11b27d65bae508215e44f1d495de154f464584e66b9b6b6e4`).

Working tree agrees with the freeze tip for the whole pinned set: `git -C <lane> diff --stat 8be2717b -- <contract, both counters, controls/controls.py, evidence/freeze-sha256.txt, tools/, corpus/SOURCES.md, corpus/evidence/sources-r56/>` prints nothing (rc 0). The same diff of the pinned set against lane HEAD `acc62f54` is also empty, so the three post-freeze integration commits did not touch frozen bytes. `git status --porcelain` shows only `M LOG.md`, `M SCORECARD.md`, `M SHONEN.md`, `?? corpus/lessons/round-56.md`, `?? .ufo/waves/round-56/w1*` — none of them inside the pinned set.

The freeze-tip correction is consistent with its pin: `git diff 3f494b49 8be2717b` touches only `controls/controls.py` (one line: a raw-string mutant pattern `r"…\n…"` → `"…\n…"` for `fence-toggle-dropped`) and the matching line 6 of the manifest (`08620c17…` → `5bf65ac0…`). `contract.md`, `count-c1.py`, `count-c2.py` have identical blob ids at `3f494b49` and `8be2717b` (`2294c0f6…`, `9fb48886…`, `2fe0c7bb…`), so the at-freeze counter receipts (`rev=3f494b49…`) still describe the frozen counter bytes.

## 2. Registry anchor cells

Row S544 (`corpus/SOURCES.md:324`) carries `sha256 38ba3e6b309e17d3d8038e8986e274bb363ac893d1c325fe145a95882a417796` for `corpus/evidence/sources-r56/watchdog-log-grammar.txt`. Row S545 (`corpus/SOURCES.md:325`) carries `sha256 61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7` for `corpus/evidence/sources-r56/rfc8259.txt`.

```
sha256sum <lane>/corpus/evidence/sources-r56/rfc8259.txt            -> 61a5378f…4cd2d7   rc 0
sha256sum <lane>/corpus/evidence/sources-r56/watchdog-log-grammar.txt -> 38ba3e6b…417796   rc 0
git show 8be2717b:corpus/evidence/sources-r56/rfc8259.txt | sha256sum            -> 61a5378f…4cd2d7
git show 8be2717b:corpus/evidence/sources-r56/watchdog-log-grammar.txt | sha256sum -> 38ba3e6b…417796
```

Both committed copies equal both cells; the cells are 64 hex characters wide, sit on the row whose copy path they name, and appear exactly once each in `SOURCES.md` (`grep -c` = 1 / 1). Cell content is unchanged since the rows landed at `c419fe6d` (`git show c419fe6d:corpus/SOURCES.md` lines 324-325 identical). For the copy paths themselves: `git ls-tree 6ced9da9|3f494b49|8be2717b -- corpus/evidence/sources-r56` lists exactly these two files at all three revisions.

Spot-check that the cells hang on real bytes (not required by the assignment, done because an anchor with a right hash and wrong content is still a false receipt):

* `rfc8259.txt` lines 251 / 308 / 461 are `A JSON text is a serialized value.`, `value = false / null / true / object / array / number / string`, `string = quotation-mark *char quotation-mark` — exactly the three strings rows S545 and `corpus/knowledge/vote-binding-r56.md:31-33` cite.
* `watchdog-log-grammar.txt` lines 1-3 equal `scripts/hyaku/inline.sh:149`, `:176`, `:182` and lines 4-6 equal `scripts/shokunin-watchdog.sh:266`, `:405`, `:448` byte for byte (`sed -n` of both sides, `cat -A`; the fleet scripts are unmodified, `git status --porcelain scripts/hyaku/inline.sh scripts/shokunin-watchdog.sh` empty).

## 3. The manifest is not checkable by the idiom the previous rounds used

The round-49..55 spotcheck receipts all verify frozen bytes with `sha256sum -c …/evidence/freeze-sha256.txt` and report rc 0. On the round-56 manifest that command fails:

```
cd <extracted 8be2717b>/.ufo/waves/round-56 && sha256sum -c evidence/freeze-sha256.txt
contract.md: OK
count-c1.py: OK
count-c2.py: OK
controls/controls.py: OK
sha256sum: tools/mori-driver-liveness.py@6ced9da9: No such file or directory (os error 2)
tools/mori-driver-liveness.py@6ced9da9: FAILED open or read
sha256sum: tools/mori-vote-bind.py@6ced9da9: No such file or directory (os error 2)
tools/mori-vote-bind.py@6ced9da9: FAILED open or read
/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r56/rfc8259.txt: OK
/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/sources-r56/watchdog-log-grammar.txt: OK
sha256sum: WARNING: 2 listed file(s) could not be read
RC=1
```

Two independent defects in the file format:

1. Lines 8-9 put the revision (`@6ced9da9`) inside the filename field, so `-c` looks for a file literally named `…py@6ced9da9`. Two failure lines, always, for every caller.
2. Lines 11-12 are absolute host paths (`/home/vgpnk/Projects/shokunin/mori-shokunin/…`). `-c` therefore hashes the **live working tree**, not the extracted `8be2717b` bytes. In a scratch extraction the two `OK`s above were produced by reading the live lane, so this manifest would print `OK` for a committed copy that had drifted in the extraction — the check cannot see the bytes it claims to pin. (I checked committed-vs-worktree separately in §2; they do match today, so this is a detection blind spot, not a byte defect.)

Impact: a wave or round-56 verifier who runs the established command gets rc 1 with 2 `FAILED` lines and must decide whether the freeze is broken. A verifier who greps for `OK` gets 6 of 8 `OK` and may not notice that 2 lines were never checked, or that 2 `OK`s came from the wrong tree. This is a frozen-file weakness, so it is a named limit plus a routed item, not a proposed edit.

Named limit for round 56: the freeze manifest is machine-checkable only per-line (`git show <rev>:<path> | sha256sum`), not with `sha256sum -c`.
Routed item for round 57: emit pin lines as bare `sha256␠␠path` with the revision in a preceding comment or a `--rev` reading table, and use repo-relative paths, so `sha256sum -c` over a tip extraction is rc 0 and actually reads extracted bytes.

## 4. Provenance labels in the manifest do not match git

Line 2 (`# data commit 6ced9da9b1f9c65065a8158735e0331938e8a599`) is the header for lines 3-6, but none of those four files exists at `6ced9da9`:

```
git ls-tree --name-only 6ced9da9:.ufo/waves/round-56/   -> evidence/  fixtures/
git show 6ced9da9:.ufo/waves/round-56/contract.md       -> rc 128
git show 6ced9da9:.ufo/waves/round-56/count-c1.py       -> empty output (rc 0, path absent)
```

A verifier reading line 2 as the source revision for lines 3-6 gets `e3b0c442…b855` (the sha256 of empty input) for the counters and rc 128 for the contract — a false *failure*, not a false pass, but a trap in a file whose only purpose is verification. Those four files landed at `3f494b49`; only the tool pins on lines 8-9 belong to the data commits.

Also inconsistent between the two artifacts that pin the same tool bytes: line 9 says the vote binder is `@6ced9da9`, while `count-c2.py:46` says `# frozen at data commit c419fe6d`. Both are true of the bytes (`tools/mori-vote-bind.py` blob `5a7f20de…` is identical at `c419fe6d`, `6ced9da9`, `3f494b49`, `8be2717b`), but the two artifacts name different commits for the same value, and only `c419fe6d` is where the file was added (`git log --diff-filter=A`). The driver tool *did* change after being added: blob `37c2f1e1…` at `c419fe6d`, `be8dd1ed…` from `6ced9da9` on, which is why line 8's `@6ced9da9` is the correct label for it.

Named limit: manifest header line 2 and the `@<rev>` suffixes are prose, not keys, and are not consistent with git history.
Routed item for round 57: attribute each pin to the commit that introduced the pinned blob, generated by command (`git log --diff-filter=A --format=%h -- <path>`), not typed.

## 5. `controls.txt` mutant lines state an arm they never observed

`controls/controls.py` (frozen, `5bf65ac0…`) decides a mutant's fate from the exit status alone:

```
p = subprocess.run([sys.executable, p_, "--selftest"], capture_output=True, text=True, cwd=cwd)
killed = p.returncode != 0
line("mut:" + name, "KILLED" if killed else "SURVIVOR",
     "arm=" + arm + (" rc=%d" % p.returncode if not killed else ""))
```

`arm` is the static fourth field of the `MUTANTS` table; `p.stdout` is captured and discarded. The tool's selftest does name the arms it failed (`VOTE_BIND_SELFTEST pass=%d fail=%d failed=<names>`, `tools/mori-vote-bind.py:400`), so the observation exists and is thrown away. Consequence: any nonzero exit — including a mutant copy that does not even parse — is reported `KILLED arm=<expected>`.

Demonstrated in scratch against the frozen tool at `8be2717b` with controls' own `line()` formatting:

```
### syntax-error  rc=1  stdout=''
### stderr last line: 'SyntaxError: invalid syntax'
controls.py would print: mut:syntax-error             KILLED arm=t_fenced_text_ignored
```

So the 8 `KILLED arm=…` lines in `evidence/controls.txt` are asserted attributions. I re-ran the frozen `MUTANTS` table against the frozen tool with stdout kept, and on these bytes every label happens to be true (8/8 killed, observed failing arm = the labelled arm in each case; `fence-toggle-dropped` is `pass=15 fail=1 failed=t_fenced_text_ignored`, i.e. the `8be2717b` pattern correction is what makes the mutant applicable at all):

```
fence-toggle-dropped         rc=1 out=VOTE_BIND_SELFTEST pass=15 fail=1 failed=t_fenced_text_ignored
substring-scalar-binding     rc=1 out=VOTE_BIND_SELFTEST pass=8 fail=8 failed=…:EXC:no such group…,t_json_prose_substring_rejected…
hash-length-opened           rc=1 out=VOTE_BIND_SELFTEST pass=15 fail=1 failed=t_hash_len_drift_rejected
first-wins                   rc=1 out=VOTE_BIND_SELFTEST pass=14 fail=2 failed=t_last_wins_text,t_last_wins_json
text-channel-closed          rc=1 out=VOTE_BIND_SELFTEST pass=10 fail=6 failed=t_plain_binds:EXC:…,t_plain_binds,…
json-channel-closed          rc=1 out=VOTE_BIND_SELFTEST pass=10 fail=6 failed=t_json_array_binds:EXC:…,t_json_array_binds,…
roster-filter-dropped        rc=1 out=VOTE_BIND_SELFTEST pass=15 fail=1 failed=t_roster_and_name_filter
entail-verb-dropped          rc=1 out=VOTE_BIND_SELFTEST pass=15 fail=1 failed=t_entailed_verb_parsed:EXC:…
```

Secondary observation from that run: 4 of the 8 kills are exception kills (`:EXC:`), not clean assertion kills — the mutant makes the tool raise rather than answer wrongly, which the rc-only test cannot distinguish from a real behavioural kill. (Mutation-strength judgement belongs to the mutation seats; recorded here because it is the same rc-only mechanism.)

Named limit: `KILLED arm=…` in `evidence/controls.txt` is a table label, not an observed arm.
Routed item for round 57: parse `failed=<names>` from the mutant's selftest stdout, require the labelled arm to appear in it, and mark EXC-only kills as `KILLED-WEAK`.

## 6. The controls receipt mutates `HEAD`, not a pinned revision

`controls.py` reads the tool and both counters with `git show(repo, "HEAD", path)`; `enter` is used only as the revision handed to the do-nothing counter runs. The mutant block prints no revision. When this receipt was produced HEAD was the freeze tip; today HEAD is `acc62f54` (3 commits later). Re-running the receipt tomorrow silently attests whatever `HEAD` is then. Today the pinned set is byte-identical at `8be2717b` and `acc62f54` (§1), so the receipt's *content* is still valid — by luck of an empty diff, not by construction.

Related, same receipt: the two do-nothing lines are printed with `verdict[:110]`, so the measured revision is cut mid-hex —

```
do-nothing-c1                PASS C1=unmet … failed=tool_absent rev=5b295eeebd87ebd610d8d39b
do-nothing-c2                PASS C2=unmet … rev=5b295eeebd87ebd610d8d39bfe2035742
```

(the entering tip is `5b295eeebd87ebd610d8d39bfe2035742f740cfa`). Round 55's routed defect (2) asks that a row cite the revision the receipt stamps; here the stamp is truncated and the full revision cannot be recovered from the receipt. `sha256sum` of the mutant/tool source is also absent, so a reader cannot tell which tool bytes were mutated.

Named limit: `controls.txt` does not stamp the revision or tool sha it mutated, and truncates the revision it does print.
Routed item for round 57: stamp `rev=<full HEAD sha>` and the mutated tool's sha256 on every control line, and drop the 110-char cut.

## 7. Counter re-run at the freeze tip (independent reproduction)

The at-freeze receipts (`c1-at-freeze.txt`, `c2-at-freeze.txt`) are stamped `rev=3f494b49…`. I ran the frozen counters at the freeze tip itself, from a `git archive` extraction of `8be2717b`, `TMPDIR` under scratch:

```
python3 <extracted>/.ufo/waves/round-56/count-c1.py 8be2717b0809281d07dffe83dad424a4859e0747 --repo <lane>
C1=met selftest=ok fixtures=ok entry=ok row=ok norem=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
rc=0

python3 <extracted>/.ufo/waves/round-56/count-c2.py 8be2717b0809281d07dffe83dad424a4859e0747 --repo <lane>
C2=met selftest=ok tally=ok control=ok contrast=voted0 entry=ok row=ok rev=8be2717b0809281d07dffe83dad424a4859e0747
rc=0
```

Both `met` at the freeze tip, with the freeze-tip revision printed by the counter itself. The PIN constants agree with the manifest (`count-c1.py:46` = `6b3dba74…`, `count-c2.py:46` = `8be1acdb…`).

## 8. What this seat did not check

* Whether the two claims' predicates are *meaningful* (grammar fidelity of the probe against live `.ufo/watchdog.log`, tally semantics over the round-55 ledger) — that is the critic/exec seats' surface.
* The census receipts (`census-start.txt` first lines above are the start census; end census is not in the freeze set). Not assigned.
* Registry anchors of earlier rounds. Not assigned.
* `corpus/lessons/round-56.md` is untracked at the time of writing; not part of the pinned set and not read as evidence.

## Findings

1. **MED** — `.ufo/waves/round-56/evidence/freeze-sha256.txt:8-9`. The `@6ced9da9` revision suffix sits inside the filename field, so `sha256sum -c` on this manifest can never return 0: rc 1 with `tools/mori-driver-liveness.py@6ced9da9: FAILED open or read` and `tools/mori-vote-bind.py@6ced9da9: FAILED open or read`. The idiom every prior round's spotcheck used is broken for round 56; a verifier must fall back to per-line `git show <rev>:<path> | sha256sum` (which I did — all six lines match). Frozen-file weakness: named limit + routed item, no edit proposed.
2. **MED** — `.ufo/waves/round-56/evidence/freeze-sha256.txt:11-12`. Both source-copy pins use absolute host paths (`/home/vgpnk/Projects/shokunin/mori-shokunin/…`), so any `sha256sum -c` run — including inside a tip extraction — hashes the live working tree instead of the committed bytes and reports `OK` even if the extracted/committed copy had drifted. Separate committed-vs-worktree comparison shows the bytes do match today (no divergence), so this is a detection blind spot, not a byte defect.
3. **MED** — `.ufo/waves/round-56/controls/controls.py:66-95` (frozen `5bf65ac0…`) and the 8 `KILLED arm=…` lines of `.ufo/waves/round-56/evidence/controls.txt:3-10`. `KILLED` is `returncode != 0` only, and `arm=` is copied from the static `MUTANTS` table; the selftest's own `failed=<names>` field is captured and discarded. Demonstrated: a mutant that is a plain `SyntaxError` (empty stdout, rc 1) yields `KILLED arm=t_fenced_text_ignored`. Re-running the frozen table with stdout kept shows all 8 labels are true on the frozen bytes (so no false `met` claim), but the receipt cannot establish that, and 4 of 8 kills are exception kills rather than behavioural kills.
4. **LOW** — `.ufo/waves/round-56/evidence/freeze-sha256.txt:2` with lines 3-6. The header names data commit `6ced9da9` as the source of the contract, both counters and the controls module, but none of those four exists at that commit (`ls-tree` shows only `evidence/` and `fixtures/`; `git show 6ced9da9:.ufo/waves/round-56/contract.md` → rc 128). They landed at `3f494b49`. A verifier trusting the header gets a false failure (`e3b0c442…b855`, the empty-input sha256, for the counters).
5. **LOW** — `tools/mori-vote-bind.py` pin attribution: `freeze-sha256.txt:9` says `@6ced9da9`, `count-c2.py:46` says `# frozen at data commit c419fe6d`; `git log --diff-filter=A -- tools/mori-vote-bind.py` says `c419fe6d`. Bytes are identical at both commits, so no value is wrong, but two artifacts name different commits for the same pin, and only one matches the file's introduction.
6. **LOW** — `.ufo/waves/round-56/controls/controls.py:78-88` reads the tool and both counters via `git show(repo, "HEAD", path)` and never prints the revision it mutated; `.ufo/waves/round-56/evidence/controls.txt:1-2` truncates the measured revision (`rev=5b295eeebd87ebd610d8d39b…`, cut mid-hex by `verdict[:110]`). The receipt's validity therefore depends on an unrecorded HEAD state (now `acc62f54`, three commits past the freeze) and its revision stamp cannot be completed from the file.
7. **LOW** — `corpus/evidence/sources-r56/watchdog-log-grammar.txt` (pinned `38ba3e6b…`) carries 6 unlabelled `log "…"` lines: the launch/complete/dead shapes of `scripts/hyaku/inline.sh:149,176,182` and of `scripts/shokunin-watchdog.sh:266,405,448`. `corpus/knowledge/driver-liveness-r56.md:38,40` additionally cites `shokunin-watchdog.sh:241-249` (`launch-fail`) and `:398` (`wrap`) as S544 authority, and row `corpus/SOURCES.md:324`'s manifest field lists only the six extracted lines. I verified those two extra citations are true in the fleet repo, but neither shape has a frozen copy, so 2 of the 5 line kinds the probe reports rest on line-number citations into mutable fleet scripts rather than on the pinned anchor.

Verified with no mismatch found: run-56 manifest lines 3-6, 8-9 at `8be2717b` / `6ced9da9`; registry cell `38ba3e6b…` on `corpus/SOURCES.md:324` vs committed `corpus/evidence/sources-r56/watchdog-log-grammar.txt`; registry cell `61a5378f…` on `corpus/SOURCES.md:325` vs committed `corpus/evidence/sources-r56/rfc8259.txt`; both counters `met` at the freeze tip.
