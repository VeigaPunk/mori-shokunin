# Round 86 — mori (L1 MoriR86), attempt 1, wave w1 — lesson

round: 86
date: 2026-11-04
entering: fec2b328a4c83e0c61bc09d70e254ca47d547d34
freeze: 5e80229a450fa007d73ad0fb8bc3147e4adf5438 (contract, three counters, the do-nothing controls)
read at: `57104423a12a859cac7ac249c683b3a37d77fbe5`; HEAD moved to `98d15d8f` (contract A1) mid-seat
seat scope: this lesson and the `## Gate` it carries. No counter, no receipt, no SOURCES row, no
knowledge entry, no SCORECARD/QUALITY/SKILL/LOG line and no commit.

Axes this seat works: **calibration** (one r85 class measured on frozen bytes and pinned to the
criterion that should have caught it, with a rebuildable fixture) and **freshness** (the one source
row opened this round, re-fetched, hashed and quoted by this seat). Detection and report only.

Frozen authority: `.ufo/waves/round-86/contract.md` — `992764ea…` at `5e80229a`/`4eab48c0`/`57104423`,
`5fafb320…` at `98d15d8f` with A1's pre-data clarification appended (no target, population or count
moved; the P-C1/P-C2/P-C3 sentences this lesson quotes are byte-identical in both) — and
`evidence/controls-r86.txt` (`8cc9bb5b…`). Nothing below amends them. The three after-values belong to
`.ufo/waves/round-86/count-c*.py` and the seats that land the work; this lesson cites the frozen
predicates and its own measurements only.

## What the round did

Three claims, frozen at `5e80229a` before any after-value existed, each with a named do-nothing control
in `evidence/controls-r86.txt`:

- **C1 operability (7)** — `.ufo/waves/round-85/count-c3.py` gains six arms (selftest 20 → 26) that
  kill `H-C3-metverdict`, `C3-01-rc-range`, `C3-02-rc-dropped`, `C3-03-order`, `C3-04-agreed-skip` and
  `C3-07-subject-tokens`; target `C1=met mutants=6 killed=6 survivors=0 total=6 arms=26`. Entering
  control `C1=unmet … arms=20`; the label-only stub (six `PASS` labels, `pass=26 fail=0`, no checks)
  reads `C1=unmet … survivors=6`, so labels and tally alone are not the work.
- **C2 calibration (5, tied lowest)** — the r85 C2 counter gains a replay pass (selftest 18 → 21); a
  `# replay: required` receipt's body must equal the stdout of its `# cmd:` in a scratch export of its
  own `# rev:`. Target `C2=met receipts=5 bindings=7 bound=7 revs=5 limits=5 cmd=5 summary=5 replay=2
  matched=4 defeated=1 legacy=3 unexpected=0`. Entering `C2=unmet subject=stub
  missing=replay_match,replay_stale_mismatch,replay_none_requires_reason`. The header-only gate reads
  the defeat receipt **met** — which is why the replay rule, not the digest, is the claim.
- **C3 depth (5, tied lowest; capability acquisition)** — `.ufo/waves/round-86/count-c3.py` observes the
  census twice through two surfaces and reconciles the r82 classification's 14 bare-key
  `value-changed` rows with a value channel; target `C3=met observations=2 aa=stable tokens=64
  derived=64 name_agree=64 value_rows=14 contradicting=2`. Entering control: the counter file is absent
  at `fec2b328` (`git cat-file -e … rc 128`); disclosed: applied retroactively it already reads met.

Wave shape: one v1 wave, 12 seats (4 executor / 2 scribe / 1 scout / 2 reviewer / 1 critic / 1
mutation-tester / 1 connector), attack 4/12 = 33.3 %, per `w1-dispatch.json`. Two commits landed inside
this seat's window and are recorded, not judged: `57104423` discharges the r85 spot-check's routed
defects 1–4 (the `LOG.md` `<fill>` placeholder, the contradictory `controls-r85-entering.txt` rc lines,
the missing r85 contract A4 block, the overstated amendment disclosure) and `98d15d8f` adds the r86
contract A1 (subject `--scratch`, stub-guard naming; no target or population moved).

This seat measured first-hand: the S602 pin (re-fetch, sha256, `cmp`, quote occurrence) and the fixture
below. It ran none of the three r86 counters.

## Mistakes

| Class | Evidence pointer | Captured-by | Fix delivered and what makes it able to fail |
|---|---|---|---|
| `predicate-underreach` — the frozen r85 C2 receipt predicate bound a digest over the subject's bytes **at a revision** and searched the body only for a summary token; it never executed the receipt's `# cmd:`, so a body that its own command does not produce passed as `C2=met`. The receipt asserted an execution that no clause checked, and the assertion's shape (a command line plus a body) made the record look stronger than the predicate. | `.ufo/waves/round-85/count-c2.py` at `57104423` (sha256 `497738932080b8044142e5f49a8a4f3151ab16b876d77d25a8e0771785f8b918`, byte-identical at `fec2b328`): `grade()` (`:154`) counts `fields["cmd"]` (`:173`, `:201`) and never runs it; all seven `run(` call sites pass git or the counter's own selftest argv (`:150`, `:292`, `:294`, `:301`, `:306`, `:311`, `:320`). The limit is written down at `corpus/knowledge/receipt-provenance-r85.md:50` ("Verification by hash binds **bytes**, not **execution**") and `corpus/README.md:901` ("a correct digest over a stale body still passes (the round-86 head)"). This seat's fixture: a one-byte-stale body reads `C2=met … mismatch=0` rc 0 while the same receipt's `# cmd:`, executed in an export of its own `# rev:`, prints `stale=0` against a body saying `stale=1` (`cmp` differs at char 55). | **The r85 C2 predicate's own named limit — a limit, not a criterion.** `parse_receipt` grades the *shape* of `# limits:` only (`count-c2.py:108-111`, `weak-limits` ≥3 words containing "limit"), and no arm, gate or sweep reads a limit's content, so the two committed paragraphs that name the stale-body pass could not fail. Had the limit not been written down, this field would be `none`. | The round's C2 rule (frozen P-C2, instrument `.ufo/waves/round-86/count-c2.py`): a `# replay: required` receipt's body must equal the stdout of its `# cmd:`, executed in a scratch export of its own `# rev:` with `GIT_CONFIG_GLOBAL=/dev/null`; the frozen population specifies a `reject` receipt carrying correct headers, `# rev:` and `# counter-sha256:` and a body that differs by one byte. Falsifier, two-sided: a header-only gate reads a stale body **met** (measured below on the frozen r85 grammar with this seat's fixture: rc 0, `mismatch=0`), and the replay rule must read that `reject` receipt `defeated=1`. Landing state at this seat's write (`98d15d8f`): the subject still carries 18 arms (`49773893…`) and the two r86 receipts are absent, so this cell claims the frozen rule and the demonstration below, not a landed arm. |

The class, stated plainly: the lane wrote the limit down and then certified the claim anyway. A named
limit is a disclosure; it becomes a criterion only when something fails on it. The r85 round paid for
the limit in prose and still carried a green receipt grammar whose bodies were never reproduced — the
repair is a pass that re-runs the command, not another sentence naming the hole.

### The measurement (this seat's fixture, 2026-11-04)

Run with the lane at `57104423`; scratch `$HYAKU_SCRATCH/mori-r86/Mo86S01Lesson`, deleted after the
run. Fixture commits `ace120bd85bb…` (body equal to its command's stdout) and `df90faf3e41a…`
(one-byte-stale body), `user.name=t` / `user.email=t@t`, with
`git rev-parse --show-toplevel` asserted equal to the fixture directory before the first commit. The
fixture's `claim-sweep-r85.txt` keeps the real receipt's headers (`# rev: 25a74d4c…`,
`# counter-sha256: 4ac6b526… tools/mori-claim-sweep.py`, a ≥3-word `# limits:` line) and replaces the
command and body with a deterministic one-liner — the body says `stale=1` where the command prints
`stale=0`:

```sh
S=${HYAKU_SCRATCH:-/fast/scratch/hyaku}/mori-r86/Mo86S01Lesson
git clone --shared -q /home/vgpnk/Projects/shokunin/mori-shokunin "$S/repo"
test "$(realpath "$(git -C "$S/repo" rev-parse --show-toplevel)")" = "$(realpath "$S/repo")"
cat > "$S/repo/.ufo/waves/round-85/evidence/claim-sweep-r85.txt" <<'EOF'
# receipt: claim-sweep-r85.txt
# cmd: printf 'CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=4 pointers=274\nrc=0\n'
# rev: 25a74d4c34e8430e4fbb18d4038ef5db872fb0ee
# counter-sha256: 4ac6b52615a427d1f7d8993ab636a5830bcde744c4a51f22d9157833d940ba1d tools/mori-claim-sweep.py
# limits: named limit — this body is a worktree run while the binding pins the sweep tool bytes at the revision, not the worktree bytes
# ---
CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=1 carriers=4 pointers=274
rc=0
EOF
git -C "$S/repo" -c user.name=t -c user.email=t@t commit -qam "fixture: one-byte-stale body"
python3 -I .ufo/waves/round-85/count-c2.py HEAD --repo "$S/repo"
```

Output tail, verbatim (the two other `RECEIPT` lines are unchanged and elided):

```text
RECEIPT claim-sweep-r85.txt headers=1 rev=1 limits=1 bindings=1 bound=1 summary=1
C2=met receipts=3 bindings=5 bound=5 revs=3 limits=3 cmd=3 summary=3 mismatch=0 detector=green rev=df90faf3e41a
rc=0
```

The same receipt's own command, executed in an export of its own `# rev:`, disagrees with that body:

```text
$ ( cd "$S/export" && GIT_CONFIG_GLOBAL=/dev/null bash -c "$CMD" ) > out.txt   # cmd rc=0
$ cmp body.txt out.txt
…/body.txt …/out.txt differ: char 55, line 1                                   # cmp rc=1
body:   CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=1 carriers=4 pointers=274
stdout: CLAIM_SWEEP mismatches=0 unresolved=0 tallies=0 stale=0 carriers=4 pointers=274
```

Control: at `ace120bd85bb…`, where the body equals the command's stdout, the frozen counter reads
`C2=met … mismatch=0` **and** `cmp` exits 0 (rebuild: the same recipe with `stale=0` on the body
line). The byte is the whole difference, so the replay comparison is not vacuous and the counter's
green is not an artefact of the fixture. Fixture commit ids are fixture-local: re-running the recipe
reproduces the reading and the diff (`C2=met … mismatch=0`, `cmp` rc 1 at char 55) with a different
commit id.

## Gate

The round adds one SOURCES row, `S602`, opened and rowed by `Mo86S02Sources` from its own fetch. This
seat re-opened the source, hashed the pin and located the quotes itself; the opener's exclusion
screening (`identified 7, screened 5, included 1, excluded 6`, recorded in the row's bounded-search
paragraph) is cited as the opener's measurement and was not re-derived here.

| Candidate | Decision | Evidence / flip condition |
|---|---|---|
| **S602** — in-toto Specification v1.0.0, `https://raw.githubusercontent.com/in-toto/docs/v1.0/in-toto-spec.md` | **ADMIT** (tier A, `spec`, `mined`; row line 384, `used-by corpus/knowledge/execution-evidence-r86.md`, recheck 365d) | Accessed **2026-11-04**; this seat's own re-fetch (tag `v1.0`, raw Markdown): HTTP 200, `redirects=0`, final URL identical, **87108 bytes**, **2217 lines**, sha256 `17d3326e4cf58234619dbfe821cdc5187e55e2c89f7b63f03699c46588322097`, `cmp` byte-identical to the pin `.ufo/waves/round-86/evidence/sources-r86/in-toto-spec-v1.0.md` (same sha256, same 87108 bytes / 2217 lines). Located quote, raw lines 1063-1064 — the sentence spans the break, joined with one space, apostrophe U+2019, **9 words**: "Byproducts are not verified by in-toto’s default verification routine." Supporting quote, `:1053-1054`, **14 words**: "The COMMAND field contains the command and its arguments as executed by the functionary." Flip condition: a later tag/revision that verifies byproducts by default, or a pin whose bytes stop matching. |

Quote location, re-checked by this seat: the 9-word sentence occurs **exactly once** in the pin's text
after joining every line break with one space, and its two lines are `:1063` (`…in-toto’s`) and
`:1064` (`default verification routine. …`), so a reader following `:1063-1064` lands on the sentence.

Registry evidence, this seat's counts on both byte sets: **374** rows in the committed registry at
`98d15d8f` and **375** in the worktree after the append, by the contract grammar
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`; the append is `3 0` by
`git diff --numstat 98d15d8f -- corpus/SOURCES.md` (one row, one bounded-search paragraph, one blank
line), no existing row's `status`/`recheck`/`used-by` cell moved, and the row's URL occurs once in the
registry. Census at the worktree bytes (sha256 `24cab2a8…`, uncommitted — the L1 owns the commit):

```text
$ scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori
…
mori	ok	/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md
```

rc **0**; warnings **35**, all `W04` duplicate-URL (the entering tolerance); zero `E` codes.

Gate limits, named: this seat verified the pin's bytes and the quotes, not the source's later
availability at a revision other than the tag `v1.0` it fetched; the row's exclusion reasons and the
knowledge entry's negative-claim sweeps (`reproduc` 0, `stdout` 16, `compar` 1) are the opener's
measurements, not repeated here. **Assimilation: none** — no `merge/mori/` adoption this round, and no
existing SOURCES row was touched.
