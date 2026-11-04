# Mo88S02Knowledge — review of the r88 knowledge entry (round 88, w1, attempt 1)

```
seat:            Mo88S02Knowledge
role:            review / attack / record; detection and report only, no remediation
entry reviewed:  corpus/knowledge/receipt-counterfeit-r88.md, worktree version
                 sha256 30fca3a1a76b0342deae03e7f77ecdf1f2cc13d2b88f6a4fd8edac8ba7a1ca50
                 6719 bytes, 97 lines, mtime 2026-11-04T11:12:03-0300
                 version sequence seen: 7c4946c2 commit = 91949aa9 (80 lines) -> 129a1862 (88)
                 -> 30fca3a1 (97, pinned). Lines below are the 97-line version.
lane HEAD:       start 9c775ac2131da13c4c4cfdf2b14077184076f557;
                 completion fecfc10a (the L1 landed the entry as 30fca3a1, the same hash pinned
                 here, plus the wave evidence and lesson; observed, not judged here)
subject:         .ufo/waves/round-87/count-c2.py at d5e2eda494877a85edaa4e287d6ad81843d9a8a1
                 sha256 7e577f533e1dac676d3f5b3d601f2c4c622c57c325e6091e6018b5781ae73fc0, 507 lines
frozen instruments (2a5e3ad9): round-88/count-c2.py sha256 8904a3d0b5d973b58836e827a70f28cf65e1089e3eec8446cc369665664beda7, 360 lines;
                 round-88/count-c1.py sha256 3ba0f97baaae389e602fa3ac929d6b007cdd1f65062db15f34ef7f184f3a32e2
source copy:     .ufo/waves/round-88/evidence/sources-r88/tuf-spec-v1.0.37.html
                 sha256 f20fda0dda7128f3b9cc1f12f3d90301b0f6e163576ba285bfe485d1671e8def, 248698 bytes, 4997 lines
scratch:         /fast/scratch/hyaku/mori-r88/Mo88S02Knowledge (created, used, deleted at exit)
tooling:         none installed; `python3 -I`, read-only `git`, coreutils. No pacman/uv/npx.
mutations:       none in the lane. Every fixture commit is in a `--shared` clone under the seat
                 scratch, identity passed per-command (`git -C "$D" -c user.name=t
                 -c user.email=t@t commit`).
```

Provenance note: the entry moved three times while this review ran. D1 (source step), D2 (located
quote), the "both problems" sentence (D4) and the supersede-target narrowing (D14) were fixed
by the L1 in the pinned 97-line version; the status of every defect below is stated against that
version. I did not write the corpus entry. `.ufo/waves/round-88/contract.md` is also modified in
the worktree with disclosed post-data Errata E1/E2; that is the L1's file and I did not assess it.

## 0. What was run (exact)

```text
$ python3 -I .ufo/waves/round-88/count-c2.py d5e2eda4 --scratch /fast/scratch/hyaku/mori-r88/Mo88S02Knowledge/rt4
REAL rc=0 C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=d5e2eda49487
FX clean rc=0 refused C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=d5e2eda49487
FX stripped rc=1 refused problems=missing-replay
FX vacuous rc=1 refused problems=cmd-binding
FX absent-target rc=1 refused supersede-absent=1
C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23 rev=d5e2eda49487
rc=0   (20.1 s wall; a second run took 18.0 s)

$ python3 -I .ufo/waves/round-88/count-c1.py d5e2eda4 --scratch /fast/scratch/hyaku/mori-r88/Mo88S02Knowledge/c1rt
MUTANT count-c1.py M1-met-no-guard killed rc=1
MUTANT count-c1.py M2-met-drop-empty killed rc=1
MUTANT count-c1.py M3-killed-n killed rc=1
MUTANT count-c1.py M4-arms-total killed rc=1
MUTANT count-c1.py M5-split-field killed rc=1
MUTANT count-c1.py M6-anchor-guard killed rc=1
C1=met mutants=6 killed=6 survivors=0 total=6 arms=24 rev=d5e2eda49487

$ python3 -I .ufo/waves/round-87/count-c2.py --selftest --scratch /fast/scratch/hyaku/mori-r88/Mo88S02Knowledge/st
... C2_COUNTER_SELFTEST pass=23 fail=0

$ grep -c '5\.3\.7' .ufo/waves/round-88/evidence/sources-r88/tuf-spec-v1.0.37.html
0
```

The after receipt's 13-line body was diffed against the two counter runs (`diff` rc 0): byte-
faithful. The entry's `recheck:` line is reachable — with `--scratch` added (D8).

## 1. The three functions at d5e2eda4 — every entry claim checked against the bytes

The entry names `declared_replay_problem`, `binding_problems`, `absent_supersede_targets` and
claims their call sites (`entry:18-35`). Quoted from
`git show d5e2eda4:.ufo/waves/round-87/count-c2.py`:

```python
133 def declared_replay_problem(declared_mode, fields):
134     """A population row declared required/clone must carry its own `# replay:` line."""
135     if declared_mode in ("required", "clone") and fields["replay"] is None:
136         return "missing-replay"
137     return None

140 def binding_problems(cmd, bindings, replayed):
141     """Every `# counter-sha256:` path must appear in the replayed command's argv."""
142     if not replayed:
143         return []
144     tokens = set(token.strip(";'\"") for token in re.split(r"\s+", cmd or ""))
145     return ["cmd-binding"] if any(path not in tokens for _sha, path in bindings) else []

148 def absent_supersede_targets(superseders, known):
149     """(name, target) pairs whose `# supersedes:` names a receipt outside the population."""
150     return [(name, target) for name, target in superseders if target not in known]
```

Call sites inside `grade_population`:

```python
261         missing_replay = declared_replay_problem(replay_mode, fields)
262         if missing_replay:
263             problems.append(missing_replay)
264         problems.extend(binding_problems(fields["cmd"], fields["bindings"],
265                                          replay_mode in ("required", "clone")
266                                          or fields["replay"] is not None))
...
323     for name, target in absent_supersede_targets(superseders, set(present)):
324         counts["unexpected"] += 1
325         lines.append("SUPERSEDE %s target=%s absent=1" % (name, target))
326         ok = False
```

Verdict per claim:

- **Rule 1 (`entry:18-23`) is true.** `declared_replay_problem` returns `missing-replay` for a
  row declared `required`/`clone` whose parsed replay is `None`; `header_fields` sets replay to
  `None` for both an absent line and `# replay: none` (after requiring `# no-replay:`), so the
  entry's added `# replay: none` clause (`entry:19-20`) is true. The row is never replayed: the
  replay gate is `mode in ("required","clone") and fields["replay"] is not None` (`:295`).
  Corroborated by the C2 reviewer's `required-none` fixture (`w1/Mo88R02ReviewC2.md:66`).
- **Rule 2 (`entry:24-28`) is true on its stated check.** The call site (`:264-266`) is
  declared-replayable **or any parsed replay marker** — the entry says exactly that. The helper
  checks whitespace tokens of shell source, not a process argv (the docstring at `:141` says
  "argv"; the code splits `re.split(r"\s+", cmd)` and strips `;'"`). The entry's "whitespace
  token" is the accurate wording.
- **Rule 3 (`entry:29-35`) is now true and properly narrowed.** The test is `target not in
  set(present)` (`:257`, `:323`), and the entry now says "not one of the population's present
  basenames at the graded revision" and names the present-non-legacy limit. Correct.
- **The `entry:37-42` "both problems" paragraph is now true.** It is qualified exactly as the
  frozen `stripped` fixture measures (`problems=missing-replay` alone when the command names its
  bound path); reproduced in §0.
- **Selftest growth 17 -> 23 is true.** `--selftest` on the graded blob prints
  `C2_COUNTER_SELFTEST pass=23 fail=0`; the six new arms are `:395-416`
  (`missing_replay_required`, `missing_replay_clone`, `binding_not_in_cmd`, `binding_in_cmd_ok`,
  `binding_skipped_for_legacy`, `absent_target_helper`).

## 2. S604 audit — stored copy, section, quote (both fixed in the pinned version)

Stored copy hash and size match the entry's `source:` cell (sha256 `f20fda0d…`, 248698 bytes,
4997 lines).

- **Section/step: now correct.** `entry:3-4` now reads `§5.3 "Update the root role", step 5.3.5`.
  Byte evidence: the heading that contains raw lines 3502-3506 is
  `<h3 data-level="5.3" id="update-root">…Update the root role` at line 3465; it is the 5th
  `<li>` of the `<ol>` at 3466 (`<li>` at 3501; paragraph at 3502-3506), i.e. step **5.3.5**.
  The stored copy proves the 1:1 `<li>` numbering: the 9th `<li>` (3516-3517) reads `Repeat
  steps 5.3.2 to 5.3.9`, and the 10th (3518-3519, the freeze check) is referenced as `step
  5.3.10` at 3483 and 3509. `grep -c '5\.3\.7'` over the stored copy is **0**; the earlier
  `§5.3.7` in `README.md:914` and `SOURCES.md:386`, `:453` is also being corrected in the
  worktree (observed, not mine to write).
- **Quote: now present and correct.** `entry:48-50` quotes raw lines 3505-3506:

      If the version of the new root metadata file is not N+1, discard it, abort the update
      cycle, and report the rollback attack.

  It is **23 words** and occurs **exactly once** in the tag-stripped text (method: `re.sub(
  r"<[^>]+>", " ", raw)`, `html.unescape`, collapse whitespace, `text.count(q) == 1`). The
  entry pins the paragraph 3502-3506, which contains the sentence; a tighter pin is 3505-3506.
  One cosmetic point: `entry:50` has a double space after the closing quote and a 107-character
  line, but the claim is byte-true.

## 3. The entry's `recheck:` command (open, D8)

The recorded command `python3 -I .ufo/waves/round-88/count-c2.py d5e2eda4` omits `--scratch`.
`HYAKU_SCRATCH` is unset on this host and the counter's fallback is
`a.scratch or os.environ.get("HYAKU_SCRATCH") or tempfile.gettempdir()` (frozen counter `:269`),
so the recorded form writes under `/tmp` — non-citable by this round's rules. With
`--scratch <seat dir>` it printed exactly
`C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23 rev=d5e2eda49487` and exited 0
(18.0-20.1 s). The entry's quoted output (`entry:10-11`) drops the ` rev=d5e2eda49487` suffix.

## 4. Defects

Status legend: **[fixed]** = absent from the pinned 97-line version; **[open]** = present.

- **[fixed] D1 — wrong section/step.** The 80/88-line versions said `§5.3.7 "Update the root
  role"`. The pinned `entry:3-4` says `§5.3 "Update the root role", step 5.3.5`; README:914 and
  SOURCES.md:386/:453 are being corrected with it. Verified against the stored copy (§2).
- **[fixed] D2 — no located quote.** The 80/88-line versions paraphrased; the pinned
  `entry:48-50` carries the 23-word sentence (raw 3505-3506, once in the tag-stripped copy).
- **[open] D3 — `entry:3-6` lacks the stored-copy provenance.** It gives the URL and hash but not
  `.ufo/waves/round-88/evidence/sources-r88/tuf-spec-v1.0.37.html` (248698 bytes, 4997 lines).
  The r86 entry carries pin path/size/lines; SOURCES.md:386 carries them for this source.
- **[fixed] D4 — "both problems" was false as a general claim.** `entry:37-42` now says the
  frozen `stripped` fixture reports only `missing-replay` when the command still names its bound
  path; that is exactly what `after-r88.txt` measures and what I reproduced (§0).
- **[open] D5 — fixture hashes cited as evidence while the same section forbids that.**
  `entry:56-60` cites `a010047c` (comment-binding) and `entry:61-65` cites `3e84f588`
  (selfprint); `entry:77-78` says fixture hashes are not citable because a `--shared` clone
  commit embeds its commit time. Both are exactly such scratch commits (the reviewer's and the
  critic's, not mine). Cite `w1/Mo88R02ReviewC2.md:7-16` / `:67` and
  `w1/Mo88C01Critic.md:115-136`, and drop both hashes.
- **[open] D6 — `entry:75` cites an uncited sibling measurement.** `SCOPE_TABLE rows=7 applied=4
  would_refuse=0` is from `w1/Mo88Sc01Scope.md:17` (definitions at `:20-23`); name it. The number
  supports "no real row is refused", not the clause "refusing those rows would trade one silence
  for another" — that rationale is an argument, not this measurement.
- **[open] D7 — `entry:69-70` example is not admissible.** `true` produces an empty body, and
  `token in body` (`:276-278`) fails every population row's summary token; `true` cannot be
  admitted. Use the measured fabricated-body cases (D5) or drop the example.
- **[open] D8 — `entry:10-11` recheck form.** Missing `--scratch` (defaults to `/tmp`; measured
  `HYAKU_SCRATCH=unset`), and the quoted tail omits ` rev=d5e2eda49487`. With `--scratch` the
  claimed line prints (D8 is a reproducibility defect, not a false result).
- **[open] D9 — `entry:11` "re-open S604 on release" has no defined event.** Use an interval
  (`recheck: 365d`, as `receipt-supersede-r87.md:9`) or a concrete version trigger.
- **[open] D10 — missing `coverage-map:` front matter.** `README.md:914` hosts the row and the
  r86/r87 entries carry the line; `entry:1-11` does not. Add it.
- **[open] D11 — `entry:15-16` overreaches.** "admitted only when all three hold … rather than a
  count": the gate also requires rev ancestry, digest match, summary token, command/limits
  presence and replay equality (`:283-302`), and the counts move on refusal (`unexpected`
  increments at `:310`, `:315`, `:324`). The three rules are *further necessary* conditions, not
  the admission set, and the refusal is both a named problem and a count change.
- **[open] D12 — the `## Why S604 grounds it` block has no source-silence scoping.** The r86
  entry says the source says nothing about the lane; without it, `entry:46-52` reads as if the
  spec grounds the receipt rule rather than its shape.
- **[open] D13 — `entry:61-65` selfprint literal is wrong, and the error is load-bearing.** The
  entry prints `printf 'RECORD_SWEEP fabricated=1 tools/mori-record-sweep.py\n'` — no space
  before `\n`. The critic's fixture (`w1/Mo88C01Critic.md:121`) has the space:
  `printf 'RECORD_SWEEP fabricated=1 tools/mori-record-sweep.py \n'`. With the entry's literal
  `binding_problems` returns `['cmd-binding']` (the whitespace split leaves the token
  `tools/mori-record-sweep.py\n`, not the path); with the critic's literal it returns `[]`.
  Measured directly against the pinned module:

  ```text
  entry literal  -> ['cmd-binding']      path-in-tokens: False
  critic literal -> []                   path-in-tokens: True
  ```

  So the entry's own command is refused and the bullet's "it reads `met`" is false; the space
  before `\n` is the entire trick. Fix the literal (or quote the critic's) and keep the finding.
- **[fixed] D14 — supersede condition imprecise.** `entry:29-35` now says "not one of the
  population's present basenames at the graded revision" and names the present-non-legacy limit;
  the code path (`target not in set(present)`) matches.
- **[open] D15 — missing limits (highest value):**
  - *Zero-bindings vacuity:* `binding_problems(..., bindings=[])` returns `[]`; a receipt with no
    `# counter-sha256:` line passes rule 2 vacuously. This is exactly the content-drift leg
    `RECEIPT_REV_CONTENT_DRIFT` (`tameshi-shokunin/tools/receipt-revision-gate.py:28`, `:151`)
    names and mori does not carry (`corpus/lessons/round-87.md:152-157`).
  - *The declaration is the counter's own constant:* `POPULATION` (`:39-47`) decides
    "required/clone"; a row declared `legacy` whose header was stripped passes (no replay, no
    binding check). Rule 1 is a consistency check between two lane-authored declarations, not a
    history audit.
  - *Frozen population:* `POPULATION` and `TARGET` are constants; a new receipt or any count
    change reads `C2=unmet` through `tail != TARGET` (`:497-499`) regardless of the three rules.
    The gate is a round instrument, not a general receipt gate.
  - *A successor need not replay:* `supersede_counts` (`:159-167`) accepts any clean successor,
    including a header-only legacy row; `supersede_verdict` (`:153-156`) does not refuse
    `target == name`. The r87 critic's correction 5 (`w1/Mo87C01Critic.md:304-306`) is open.
  - *`# limits:` is not content-checked:* `:273-275` counts a limits cell only when it contains
    the word "limit" and at least three words. "The legacy row's `# limits:` carries the reason"
    is true of the three current rows (verified: `after-r85.txt` header; both r85 sweeps say
    "this body is a worktree run"), but it is not a gate guarantee.
- **[open] D16 — `entry:66-68` path-identity bullet is true but uncited.** Verified against the
  pinned module: `'tools/x.py'` → `[]`, `"tools/x.py"` → `[]`, `./tools/x.py` →
  `['cmd-binding']`. Its "measured" clause comes from the critic's report
  (`w1/Mo88C01Critic.md:108-113`); cite it.
- **[open] D17 — `entry:85-95` Siblings: presence and content are right, two precision nits.**
  Verified against the sibling files: tameshi `count-recheck.py:2-4` (value binding), tameshi
  `receipt-revision-gate.py` has exactly 11 codes (`:28-30`, `CODES` at `:46-49`, including
  `RECEIPT_REQUIRED_LINE_MISSING`, `RECEIPT_REV_CONTENT_DRIFT`, `RECEIPT_CONTROL_NOT_ANCESTOR`),
  mado `mado-tripwire.py:151` carries the quoted disclaimer verbatim (`"provenance is the
  snapshot author's claim, not checked"`), kotodama `check-receipt-seq.py:29-30` has
  `stamped == evaluated == measured` plus `--topo` (`:18-20`), and the two chousa entries exist.
  Nits: `entry:87` "a required-line refusal set (11 codes)" over-narrows the set (the 11 are rev
  / digest / required-line / ancestry; only `RECEIPT_REQUIRED_LINE_MISSING` is required-line),
  and the connector's table is uncited (`w1/Mo88K01Conn.md:51-64`). The tameshi content-drift
  limit should also appear in Limits (D15), not only in the citation list.
- **[open] D18 (nit) — `entry:7-8` uses a second `source:` key** for gate output. It parses (the
  S-id regex takes the first), but the r87 entry keeps one `source:` line and cites the receipt
  in the body; `evidence:` would be cleaner.

## 5. What holds (keep — do not rewrite these)

- The three rule sentences match the code at the quoted lines; the `# replay: none` clause is
  correct (`:135`, `header_fields` replay normalization); the stripped-header/zero-replay
  rationale matches `corpus/lessons/round-87.md:111-136`.
- The S604 section/step and the 23-word quote are now byte-correct (§2); the "both problems"
  paragraph and rule 3 are now correct (§1).
- The after receipt's 13-line body reproduces exactly at `d5e2eda4` (`diff` rc 0); `arms=23` is
  real.
- The Siblings section is present, right in substance, and `absorption: none` is the correct
  posture; only the two nits above.
- The new selfprint and path-identity findings are the right class and belong in the entry; the
  selfprint bullet only needs its literal fixed (D13) and the path-identity bullet a citation
  (D16).

## 6. Independent attack on rule 2 (my own measurement)

The reviewer's comment-token class reproduces on a different population row and mode. In a
`--shared` clone of the lane at `d5e2eda4`, I replaced the `# cmd:` of `after-c1-r86.txt`
(declared `required`) with a `printf` of its own body and moved the bound path into a shell
comment (all other headers unchanged, including the `# counter-sha256:` line):

```text
# cmd: printf '%s\n' 'MUTANT count-c3.py H-C3-metverdict killed rc=1' ... 'C1=met ... rev=876446190783' # .ufo/waves/round-86/count-c1.py
```

Graded by the pinned r87 counter at `d5e2eda4` (`python3 -I ./c2.py 6972441f… --repo <fixture>
--scratch <dir>`), rc 0:

```text
RECEIPT after-c1-r86.txt expect=met met problems=-
C2=met receipts=7 absent=0 bindings=9 bound=9 revs=7 limits=7 cmd=7 summary=7 replay=4 matched=6 defeated=1 superseded=2 legacy=1 unexpected=0 rev=6972441f66e5
```

So rule 2 is satisfied by a lexical mention (comment) and the body is not measured; the gate's
own docstring at `:141` promises "argv". The fixture revision `6972441f…` is a scratch commit and
is **not** citable evidence (it embeds its commit time); the citable form is the property, the
counter blob hash, and the printed target line. This is the same defect class the entry records at
`entry:56-60`; my run adds a second row/mode and confirms it is not row-specific.

## 7. Corrected replacement text

```markdown
# Receipt counterfeits — a declared mode is checked against the receipt's own header

source: S604 — The Update Framework Specification v1.0.37, §5.3 "Update the root role", step
5.3.5 "Check for a rollback attack" (raw HTML lines 3502-3506; the quoted sentence at 3505-3506),
stored copy `.ufo/waves/round-88/evidence/sources-r88/tuf-spec-v1.0.37.html` (248698 bytes, 4997
lines; sha256 `f20fda0dda7128f3b9cc1f12f3d90301b0f6e163576ba285bfe485d1671e8def`), fetched
2026-11-04 from `https://theupdateframework.github.io/specification/v1.0.37/`
source: the lane's own gate output `.ufo/waves/round-88/evidence/after-r88.txt`, committed at
`9c775ac2131da13c4c4cfdf2b14077184076f557`, measuring revision
`d5e2eda494877a85edaa4e287d6ad81843d9a8a1`
verified-at: 2026-11-04
recheck: `python3 -I .ufo/waves/round-88/count-c2.py d5e2eda4 --scratch "$TMPDIR"` prints
`C2=met real=met fx=4 clean=1 refused=2 absent=1 arms=23 rev=d5e2eda49487`; re-open S604 when a
newer TUF specification version is published
coverage-map: corpus/README.md (`## Coverage map`, the `receipt-counterfeit-r88.md` row); carries
`knowledge/receipt-supersede-r87.md` (S603; S600/S602 re-opened there)

## Rule

The gate `.ufo/waves/round-87/count-c2.py` at `d5e2eda4` adds three further necessary conditions
to the receipt grammar's existing checks (rev ancestry, digest match, summary token, command and
limits presence, replay equality). A refusal is a named problem on the row and an unmet run; the
printed counts move as well (`unexpected`).

1. **Declared mode is carried by the header.** `declared_replay_problem` (`:133-137`, called
   `:261-263`) returns `missing-replay` when the population declares a row `required` or `clone`
   and the parsed header carries no replay mode. Both an absent `# replay:` line and
   `# replay: none` — which `header_fields` normalizes to `None` after requiring a
   `# no-replay:` reason — read `missing-replay`; the row is never replayed. The reason is not
   cost: the r87 parser turned "declared replayable" and "carries no replay mode" into the same
   state, so a stripped header reached the target line with zero replays
   (`corpus/lessons/round-87.md:111-136`).
2. **A bound counter is named by the command.** `binding_problems` (`:140-145`, called `:264-266`)
   requires every `# counter-sha256:` path to appear as a whitespace token of the `# cmd:` line
   (after stripping `;'"`) on a row declared `required`/`clone` or carrying any `# replay:`
   marker; otherwise the row reads `cmd-binding`. The rule is lexical presence, not execution —
   see the first limit. A digest binds the counter's bytes; it does not bind the body to the
   command, and `printf '<body>'` reproduces any body while the digest stays genuine.
3. **A superseded target is present.** `absent_supersede_targets` (`:148-150`, called `:323-326`)
   returns every `(name, target)` whose `# supersedes:` target is not among the receipt basenames
   present at R; the caller prints `SUPERSEDE <name> target=<target> absent=1`, increments
   `unexpected` and clears `ok`. A target that is present but not a legacy row is not refused and
   retires nothing; a header-only successor can supersede — see the fourth limit.

Problems join per row. The frozen `stripped` fixture measures `problems=missing-replay` alone: its
command still names its bound path. A clone row with no replay line carries both problems only
when the bound path is also absent from the command's tokens.

## Why S604 grounds it

The rollback check reads: `If the version of the new root metadata file is not N+1, discard it,
abort the update cycle, and report the rollback attack.` (S604, raw lines 3505-3506; 23 words; the
sentence occurs exactly once in the tag-stripped copy). The new root is admitted only when it is
continuous with the record the client already trusts; a mismatch discards it and names the
failure rather than counting it.

The source says nothing about mori, receipts, digests, revisions or counters. The transferable
shape is the lane's reading — verification before admission, and a refusal that is a named
outcome rather than a suppressed error. The closest analogue is rule 1: the declaration (what the
population says the row is) must be continuous with the record (the header the row carries);
rules 2 and 3 are the lane's extensions, not the source's.

## Limits (named)

- **Naming is not execution.** `binding_problems` splits shell source on whitespace, so a bound
  path inside a shell comment satisfies it while bash never executes it. Measured by the r88 C2
  reviewer (`.ufo/waves/round-88/w1/Mo88R02ReviewC2.md` §Findings, lines 7-16, 67): a `clone`
  receipt whose `# cmd:` is `printf 'RECORD_SWEEP fabricated=1\n' # tools/mori-record-sweep.py`
  returns rc 0, `problems=-` and the exact r87 target. The independent S02 review reproduced the
  same class on a `required` row (`after-c1-r86`, path only in a comment; `C2=met`;
  `.ufo/waves/round-88/w1/Mo88S02Knowledge.md` §6). Routed as R89-C2-comment-binding. The
  helper's docstring says "argv"; the code checks whitespace tokens.
- **A self-printing command also passes when it names the path.** The rule is token presence, not
  command shape. `printf 'RECORD_SWEEP fabricated=1 tools/mori-record-sweep.py \n'` (the space
  before `\n` is load-bearing: it makes the path a token) replays, matches and names the bound
  path, so it reads `met` (critic fixture, `.ufo/waves/round-88/w1/Mo88C01Critic.md:115-136`;
  routed as R89-C2-selfprint-evasion). Without the space the token is
  `tools/mori-record-sweep.py\n` and the same row reads `cmd-binding`. The round-88 claim covers
  only the frozen fixture whose body omits the path token.
- **Token spelling is not path identity.** `'tools/x.py'` and `"tools/x.py"` are accepted (tokens
  are stripped of `;'"`); `./tools/x.py` is refused although it is the same file
  (`.ufo/waves/round-88/w1/Mo88C01Critic.md:108-113`; routed as R89-C2-path-identity). The real
  population is unaffected (`C2=met … unexpected=0`).
- **A receipt with no `# counter-sha256:` line passes binding vacuously.** The gate has no
  minimum-binding rule; tameshi's `RECEIPT_REV_CONTENT_DRIFT`
  (`tameshi-shokunin/tools/receipt-revision-gate.py:28`, `:151`) is the sibling code that names
  the content-drift leg mori does not carry. mori cites it and does not absorb it.
- **The declaration is the counter's own constant, and the gate is a frozen population.**
  `POPULATION` and `TARGET` are constants: a row declared `legacy` whose header was stripped
  passes, and a new receipt or changed count reads unmet regardless of the three rules. These
  rules are checks of consistency between two lane-authored declarations, not a general receipt
  audit.
- **A successor need not replay.** `supersede_counts` (`:159-167`) accepts any clean successor,
  including a header-only legacy row, and `supersede_verdict` (`:153-156`) does not refuse
  `target == name`. The r87 critic's correction 5 (`w1/Mo87C01Critic.md:304-306`) is open.
- **`# limits:` is not content-checked.** `:273-275` counts a limits cell only when it contains
  the word "limit" and at least three words. "The legacy row's `# limits:` carries the reason" is
  true of the three current rows; it is not a gate guarantee.
- **The S604 quote grounds the shape, not the gate.** TUF's rollback check is version continuity;
  the gate's rules are header/command bindings plus a body-versus-command replay at one
  revision. The analogy is verification-before-admission only.
- **Fixture revisions are not evidence.** A `--shared` clone's fixture commit embeds its commit
  time, so its hash moves; the r88 wrapper prints the graded revision, while a raw r87 run on a
  fixture prints the fixture revision. Cite the report and the verdict, never a fixture hash.

## Siblings (cited, not absorbed)

The r88 connector measured these relations (`.ufo/waves/round-88/w1/Mo88K01Conn.md:51-64`); the
sibling owns the stronger rule and mori only cites it:

- tameshi `tools/count-recheck.py` (`:2-4`) — value binding: a printed figure must equal the
  count its named command produces at the record's revision. mori's replay proves
  reproducibility, not that the figure is right.
- tameshi `tools/receipt-revision-gate.py` — eleven named refusal codes (`:28-30`, `:46-49`),
  including `RECEIPT_REQUIRED_LINE_MISSING` and `RECEIPT_REV_CONTENT_DRIFT`, and
  `positive`/`verdict` rev binding. mori's rule 1 is one fixed instance of that shape.
- tameshi `tools/evidence-disposition.py` — the stronger lineage rule for rule 3: a supersede
  target must be an input this document already extends, not merely a present basename.
- mado `tools/mado-tripwire.py` — unpinned inputs are refused, not downgraded;
  `provenance is the snapshot author's claim, not checked` (`:151`) is the disclaimer mori
  cites, not restates.
- kotodama `tools/check-receipt-seq.py` — stamped == evaluated == measured (`:29-30`), tree
  equality and `--topo` carrier parentage (`:18-20`); a receipt-sequence claim belongs there.
- chousa `corpus/knowledge/receipt-identity-r65.md` and `receipt-digest-provenance-r67.md` — the
  command/body-binding limit and the committed-bytes provenance rule mori implements.

`absorption: none`.
```

## 8. Verdict

**ENTRY needs-changes.**

Four defects were fixed by the L1 in the pinned version (source step, located quote, the
"both problems" generalisation, the supersede-target narrowing), and those fixes are byte-true.
The entry still fails on: the selfprint bullet's literal, whose missing space reverses its own
claimed verdict (D13, measured against the pinned module); cited fixture hashes that the entry's
own last limit says are not citable (D5); the `true` example that cannot be admitted (D7); the
recheck that writes to `/tmp` and truncates its own verdict (D8); the missing `coverage-map:`
(D10); and the missing limits that carry the depth of the claim (zero-bindings, declaration
trust, frozen population, header-only successor, limits content — D15). The replacement in §7 is
complete and byte-checked; `README.md:914` and `SOURCES.md:386/:453` are being corrected in the
worktree already.

## 9. Limits of this review

- I read the stored S604 copy, not the live URL; the `fetched 2026-11-04` cell cannot be verified
  from bytes (only the copy's hash and size are).
- I did not verify the sibling fixture hashes `a010047c…` or `3e84f588…`: they are scratch commits
  whose hashes embed commit time, so they are unreproducible by construction. I verified the
  *classes* (comment binding by my own fixture, §6; selfprint and path identity at the function
  level, §D13/D16) and the sibling reports' text.
- I ran the frozen C1 counter once (§0); I did not re-run the six mutants individually — the
  entry's C1 clause is context, not my seat's claim.
- The entry moved three times during the review; the pinned 97-line hash is the only version
  these line numbers describe (the earlier 80-line and 88-line versions shifted lines before
  `## Limits` too, so no single offset is correct — compare by the quoted code symbol, not by
  line arithmetic).
- Sibling tools were read at the fleet worktree (read-only) while their lanes move; the connector
  report's blob table (`w1/Mo88K01Conn.md:20-28`) is the pinned reference, and my accuracy check
  is at the read moment.
- `.ufo/waves/round-88/contract.md` is modified in the worktree (Errata E1/E2 appended post-data,
  disclosed); I observed it and did not assess it — the L1 owns that file.
- Scratch `/fast/scratch/hyaku/mori-r88/Mo88S02Knowledge` was deleted with an EXIT trap; no path
  outside the assigned report and that scratch was written.
