# RevC9Compat — r37 C1 counter re-run at 13bfba23 (wave 1)

Verdict: **PASS** — `C1=met`, exit 0; **malformed per-id lines = 0** across all 27 tool
invocations (24 blind + 1 real + 1 drawn + 1 challenge). No actionable defect in scope.

## Assignment and command

```
cd /home/vgpnk/Projects/shokunin/mori-shokunin
python3 .ufo/waves/round-37/count-c1.py 13bfba23b7ca063c76d3504a2ff6eb7b6a294932 --seed 41
```

Exit 0. Full transcript: `.ufo/waves/round-39/scratch/RevC9Compat/counter-primary-seed41.txt`.
The tool under test is materialized from the scored revision
(`count-c1.py:923-936`, `git show <rev>:tools/mori-sources-appendonly.py`); `6bd57097` is only
the history the real arm reads (`REAL_REV`/`REAL_BASE`, `count-c1.py:74-75`), and that revision
does **not** carry the tool (`git show 6bd57097:tools/mori-sources-appendonly.py` → "path exists
on disk, but not in '6bd57097'"; tool added at `bf0df77f`, round 36). The P-C1 wording "at
revision R" therefore resolves to the scored rev; the parenthetical "(rev 6bd57097, round base
f10a320d)" is the history, as the code implements.

## Arm lines (verbatim, primary run)

```
blind arm: 24/24 sandbox histories matched the hidden truth (2.5s; coverage: deletions=21 changed-back=14 superseded=12)
real arm: pass (0.5s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
drawn arm: pass (9.3s) rev=13bfba23b7 base=f920eaf7db
  truth:  appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
challenge arm (real-arm clothing): pass (0.1s)
  truth:  appendonly_violations=4 ids=[S148,S172] deleted=[S104,S299] superseded=[S172] round_changed=[S148]
  tool:   appendonly_violations=4 ids=[S148,S172] deleted=[S104,S299] superseded=[S172] round_changed=[S148]
negative memo-n1.py     rejected (challenge: lists differ: want appendonly_violations=3 ids=[S179] deleted=[S066,S116] superseded=[S179] round_changed=[S066,S116] got appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193])
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 3/4 (repo200: per-id lines differ (malformed=0)))
C1=met
seed=41
```

Real arm: 18 `changed` lines, one per id, byte-equal summary, oracle identical, exit 1 with
non-empty `round_changed`. Drawn arm drew a lane commit (`13bfba23b7`) with `base` = its parent;
challenge arm carried real-arm clothing (path under
`.ufo/waves/round-37/scratch/challenge-4uak9ok5/repo920`, lane identity/title) and a deletion
witness, and matched the counter's op-log truth. All three negative fixtures rejected.

## Malformed-line analysis (the assigned falsifier)

Method: a transparent tee wrapper
(`.ufo/waves/round-39/scratch/RevC9Compat/tee_tool.py`) ran the real tool as a child, forwarded
stdout/stderr/exit unchanged, and recorded each invocation (`argv`, cwd, rc, raw stdout) into
`scratch/RevC9Compat/tee/`; the counter was re-run through it at seed 41
(`scratch/RevC9Compat/counter-tee-seed41.txt`, `C1=met`). The recorded stdout was re-parsed with
the counter's own grammar (`count-c1.py:541-564`:
`^changed (S\d{3}) superseded_by=(S\d{3}|-)$`, `^deleted (S\d{3})$`).

- Invocations: 27 = blind 24 + real 1 + drawn 1 + challenge 1 (`scratch/RevC9Compat/arm-lines.txt`).
- **malformed_total = 0** (blind 0, real 0, drawn 0, challenge 0). No line beginning with
  `changed ` / `deleted ` fails the grammar in any arm.
- Non-per-id lines per invocation are exactly three classes: the P-C9 predicate banner
  (`P-C9: ...`), the single `appendonly_violations=…` summary, and the new
  `supersede_timing superseded_as_of=[…] stale_supersede=[…]` line. None begins with
  `changed `/`deleted `, so none can be miscounted.
- Cross-check (`scratch/RevC9Compat/invariants.txt`): 27/27 invocations satisfy exactly one
  summary line; `changed`-line set == summary `ids`; `deleted`-line set == summary `deleted`;
  no duplicate lines; `violations == len(ids)+len(deleted)`; exit == 1 iff `round_changed`
  non-empty (real rc=1, drawn rc=0, challenge rc=1, blind mixed as drawn).
- The `supersede_timing` line is **not** new in v2: the round-38 gate bytes at `13f3db7e` already
  print it (`13f3db7e:tools/mori-sources-appendonly.py:45,74,580`) and already print the
  PREDICATE banner before the report (`:580`). So v2 adds no new stdout line class; the
  contract's "byte-identical in shape to v1" (`.ufo/waves/round-39/contract.md:133-136`) holds
  on every arm measured.
- CID grammar compatibility: the gate rejects non-`S\d{3}` row ids (`tools/…:68,210`) and writes
  `superseded_by` as `S\d{3}` or `-` (`report()`), a strict subset of the counter's grammar — no
  id can arrive in a shape the counter calls malformed.

## Findings

**F1 (LOW, counter usability — not a claim failure).** `--tool` with a relative path fails
every arm: `run_tool` executes the child with `cwd="/"` (`count-c1.py:533`) and passes the tool
path verbatim, so `--tool .ufo/.../x.py` becomes `python3 //.ufo/...` and the failure surfaces as
`blind arm: 0/24 … no summary line (exit 2): can't open file '//…'` rather than a setup error.
Reproduced this seat. The scored invocation omits `--tool`, so C1 is unaffected; a
mutation-testing seat passing a relative control path could misread it as a tool failure (the
existing evidence uses absolute paths). Suggested one-line hardening: `os.path.abspath` the
`--tool` value in `main` (`count-c1.py:923-924`) — not applied here (read-only lane).

**F2 (INFO, scope of the measure).** C1 at seed 41 also passes with the round-38 v1 gate bytes
(`--tool <abs>/tool-v1-r38.py` → `C1=met`, same negative rejections; scratch file
`tool-v1-r38.py`), as expected because all C1 arms are linear histories where v1 and v2 agree
(contract:136-138). C1=met therefore certifies line shape/per-id truth, not v2's ancestry
semantics; v2 discrimination rests on C7/C9. Do not read the C1 receipt as evidence for P-C9.

**F3 (INFO, replay).** The drawn arm draws from `git rev-list --max-count=40 HEAD`
(`count-c1.py:762`), so its pick is HEAD-dependent. Two runs ~10 min apart drew different revs
(`13bfba23b7 base f920eaf7db` at HEAD=13bfba23; `5561819450 base 13bfba23b7` at HEAD=296b2c5 —
wave-1 commits landed mid-review); both passed. This matches the r37 receipt's own
`head_at_measurement` caveat (`.ufo/waves/round-37/evidence/c1-after-v2.txt:20`); replay of a
specific drawn-arm line requires pinning the tip.

**F4 (LOW, exit-invariant asymmetry).** `real_arm` (`count-c1.py:734`) and `real_draw_arm`
(781-800) never compare `proc.returncode` with `1 if round_changed else 0`; the printed
`tool exit=1` is informational, and `diffs` cannot include an exit mismatch. Exit drift is still
caught by `check_blind` (`692,709`) and `challenge_arm` (`822,834`), so no claim hole at seed 41;
it is a per-arm coverage asymmetry only.

## Residual risk

- Seed 41 is one run; blind coverage cleared the frozen minimum (deletions 21≥12, changed-back
  14≥12, superseded 12≥1) but other seeds were not replayed by this seat (time-box).
- The blind arm's truth is the counter's own op log; I verified line-shape, set equality,
  uniqueness, violations arithmetic and exit-vs-truth consistency, not an independent
  recomputation of that oracle (that is the blind arm's design, not a gap I can close from
  outside).
- 6bd57097 predates the gate's introduction, so the real arm judges an older SOURCES history
  with newer tool bytes — correct per the code and the P-C1 parenthetical, but the phrase "at
  revision R, tools/… prints" invites misreading; recording it here so the receipt is read as
  the code runs.
- Lane HEAD moved during the review (13bfba23 → 5561819/20260b0/296b2c5); the r37 evidence file
  for the prior replay pins its own tip. No lane files were written by this seat; scratch only.

## Verification gaps

- The runtime mounts no `lsp` device (`read xd://lsp` → "No such tool"; mounted devices:
  `ast_edit`, `debug`), so semantic `references`/`definition`/`diagnostics` were unavailable;
  caller analysis used `grep` over tracked scripts/counters plus direct execution of the tool at
  both gate versions. This is a recorded tooling limitation, not absence of callers — the
  parsers that consume gate stdout are `count-c1.py` (measured here), `count-c2.py`
  (`SUMMARY_RE` at `:54`, anchored `^`), `count-c7.py` (parses tool `--selftest` arm lines only,
  `:379`), and `conform.py` (does not parse gate stdout); none keys on line position, so the
  banner/timing lines cannot shift a summary parse.
- No mutation of the r37 counter was performed (mutation-testers own copies; the lane is
  read-only for this seat). F1/F4 were observed by running, not by mutating files.

## Tooling note

No tools installed or upgraded (network package operations not needed; pacman transactions are
paused host-wide per the seat bounds). Scratch artifacts:
`.ufo/waves/round-39/scratch/RevC9Compat/{tee_tool.py,tee/,counter-primary-seed41.txt,counter-tee-seed41.txt,arm-lines.txt,invariants.txt,tool-v1-r38.py}`.
