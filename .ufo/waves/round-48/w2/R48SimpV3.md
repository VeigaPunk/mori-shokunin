# R48SimpV3 — round 48 w2: dead weight in the landed v3 pin reconciler

**Attacked:** `tools/mori-pin-check.py` at the landed tip `e4dfff32d4f97c7ef250e9a7538fa75d4f284492`
(917 lines, sha256 `85a89a3b6ba4eb5ed0b3f784763cfe78652e6493b055b3dcf8924feaffff82e1` = working-tree bytes;
`git rev-parse HEAD` = the same revision, `git status --porcelain` shows no tracked modification).
Question: does the landed v3 carry dead weight — unused helpers, duplicated regex authorities, duplicated
nearest-path logic — that can be deleted without moving any measured behaviour?

**Verdict: HOLDS — the instrument's behaviour survives every deletion; the dead weight is real but is class
`maintainability` (duplicate authority, dead parameter, dead value space), not a C1 calibration defect.**
Nine deletion candidates were found (D1-D8 code, D9 documentation); D1-D8 were applied to scratch copies and
all three required proofs reproduce byte-identically: tool selftest `pass=60 fail=0`, `C1=met` unchanged on the
full frozen matrix, and byte-identical `PIN_CHECK` output on one junk (J1) and one honest (H3) variant.
The tool was **not** edited; the landed bytes are untouched. Proposal for round 49 in §7.

## 1. Deletion candidates (landed line numbers)

| id | weight | landed site | class | applied in scratch |
|---|---|---|---|---|
| D1 | dead parameter `raw` — never read in the body | `trunc_digest_pins(st, raw, root)` :313, caller :513 | dead parameter | yes |
| D2 | dead parameter `scratch` in `run_cmd` (TMPDIR comes from `root/.scratch`, :401-404), and the value threaded through `check`'s own `scratch` parameter (:452, :565) plus the two selftest `mkdtemp` calls that only fed it (:885, :893) | :400, :452, :565, :885, :893 | dead parameter chain | yes |
| D3 | `span_kind` returns a 5-valued kind (`tally`/`digest`/`trunc`/`command`/`ignore`) and its **only** caller consumes `"unparsed"` (:505-511); the four early-return branches stay load-bearing, the value space does not | :278-296, :506 | dead value space / stale name | yes |
| D4 | the tally-prefix literal `[A-Z][A-Z0-9_]*SELFTEST` is written **six** times: `HIDDEN_TOKEN_RE` :114, `TALLY_PIN_RE` :116, `PINLIKE_T0_RE` :117, `TALLY_TEXT_RE` :121, and re-compiled inline in `pin_commands` :348 (an exact duplicate of `TALLY_PIN_RE`) and `pin_keys` :428 | :114-121, :348, :428 | duplicate authority | yes |
| D5 | the nearest-preceding-path + sha256 hit computation is written twice — `trunc_digest_pins` :319-320 (prefix match) and `check` :589-590 (exact match) | :319, :589 | duplicated logic | yes |
| D6 | `check` parses the same registry twice, once for the duplicate-name pass (:482) and once for the main loop (:493); `parse_registry` is pure | :482, :493 | duplicated work | yes |
| D7 | `r"^ {0,3}\|"` compiled inline twice inside `hidden_rows` | :253, :262 | duplicate authority | yes |
| D8 | dead default `eidx=2` on `command_from_span` :325, `pin_commands` :339, `derive_command` :364 — every call site (5, AST-checked) passes the argument; the default is a residual v2 hard-coded entry column | :325, :339, :364 | dead default | yes |
| D9 | stale docstring: "What it reads" says a digest pin "must equal the sha256 of at least one file path named **anywhere in the row**" (:45-47), which R10 replaced with the nearest preceding path **of its own cell** (:587-590); the documented output shape (:82) omits the `hidden=N` counter the tool prints (:599-600) | :45-47, :82 | stale name / stale authority | no (documentation only, §6) |

Scratch copies: `.scratch/r48w2-R48SimpV3/base.py` (landed bytes), `cand.py` (D1-D7,
sha256 `6a5dbc8afa362d7c8442487deaefc42326ff0fe56fa41fad9a6638975b95f0f9`), `cand2.py` (D1-D8,
sha256 `6916381b200b67c07fe8732ffeaeee85d4a91d3aada2717ba37525f2e335f842`). `diff -u base.py cand2.py`:
44 removed / 50 added, net +6 lines — the additions are one shared literal, one shared regex constant and one
shared helper; the removals are 5 dead labels, 3 dead parameters, 3 dead defaults, 2 duplicate regexes,
1 duplicate parse, 2 dead `mkdtemp` calls and 1 duplicated digest computation. Line count is not the axis;
duplication is.

## 2. Proof receipts (observed, absolute paths)

All runs with `TMPDIR=/home/vgpnk/Projects/shokunin/mori-shokunin/.scratch/r48w2-R48SimpV3`.

**Tool selftest** — landed bytes vs both candidates, identical arm names *and* statuses:

```
$ TMPDIR=$S python3 -I -B tools/mori-pin-check.py --selftest      → rc=0  PIN_CHECK_SELFTEST pass=60 fail=0
$ TMPDIR=$S python3 -I -B $S/cand.py --selftest                   → rc=0  PIN_CHECK_SELFTEST pass=60 fail=0
$ TMPDIR=$S python3 -I -B $S/cand2.py --selftest                  → rc=0  PIN_CHECK_SELFTEST pass=60 fail=0
$ diff <(grep -o '^[A-Z]* [a-z0-9_]*' selftest-base.txt) <(grep -o '^[A-Z]* [a-z0-9_]*' selftest-cand.txt)
  → empty ("arm names+status identical")
```

**C1 counter, full frozen matrix** — the claim command, tool bytes at the landed tip vs the candidate:

```
$ TMPDIR=$S python3 -B .ufo/waves/round-48/count-c1.py --tool $PWD/tools/mori-pin-check.py \
      --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 --scratch $S/c1-base          → rc=0 (999 s)
$ TMPDIR=$S python3 -B .ufo/waves/round-48/count-c1.py --tool $S/cand.py \
      --rev e4dfff32d4f97c7ef250e9a7538fa75d4f284492 --scratch $S/c1-cand          → rc=0 (904 s)

both: J1-J8 expect=unmet got=unmet rc=1 · H1-H4 expect=met got=met rc=0 · real expect=met got=met rc=0
both: C1=met junk_met=0 honest_unmet=0 real=met errors=0 variants=12 rev=e4dfff32d4f97c7ef250e9a7538fa75d4f284492
$ diff c1-base.txt c1-cand.txt                                                     → empty
```

**One junk and one honest variant, `cand2` (D1-D8), byte-identical stdout** — the exact count-c1 invocation
flags (`--rev R --repo <lane> --min-tally-pins 26 --baseline-rev 2d85e33d14198d388fd3cda9cc15ec07e57e7a53
--skill <variant>`), variant files written by the counter itself into `$S/c1-base/variant-<name>.md`:

```
J1 base rc=1 / J1 cand2 rc=1 ; diff J1-base.out J1-cand2.out → identical
   PIN_CHECK=unmet tally_pins=31 digest_pins=8 mismatches=2 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32… baseline=yes
H3 base rc=0 / H3 cand2 rc=0 ; diff H3-base.out H3-cand2.out → identical
   PIN_CHECK=met tally_pins=31 digest_pins=8 mismatches=0 unparsed=0 no_command=0 dropped=0 rebound=0 duplicate=0 hidden=0 min_tally_pins=26 rev=e4dfff32… baseline=yes
```

**Property-level equivalence** (`$S/equiv.py`, no command executed, `EQUIV pass=101 fail=0`, rc 0) — over the
real `SKILL.md` at the landed tip *and* all twelve counter variants (13 texts): every touched regex compiles
to the identical `.pattern` and `.flags`; `parse_registry`, `hidden_rows`, `pin_keys` and
`pin_bindings` (rev `<REV>` / `deadbeef` / `None`) return equal values; and for every backticked span of every
parsed row, `span_kind`'s unparsed verdict equals `span_unparsed`'s reason.

**Static checks on both candidates:** `python3 -m py_compile` ok; `pyflakes` rc 0; `vulture --min-confidence 60`
rc 0; AST parameter audit (`.scratch/r48w2-R48SimpV3/astcheck.py`) reports the two `UNUSED-PARAM` findings on
the landed bytes and none on either candidate.

`lsp` device is **not mounted** in this seat (`xd://lsp` → "No such tool"; mounted: ast_edit, debug, tripo_*,
unity_cli_status). Call-site absence is therefore proved by AST name-use analysis plus `grep` as the literal
fallback, not presented as semantic proof.

## 3. Preserved contract

- The `PIN_CHECK=…` line and its counter order are unchanged — every candidate's stdout is byte-identical to
  the landed tool's on the real registry and on the junk/honest variants above.
- Exit codes 0 met · 1 unmet · 2 setup unchanged (`cli_met_rc0`, `cli_bad_rev_rc2` arms pass).
- No rule R1-R10 changes: the four "recognised span" branches in `span_unparsed` keep their original order and
  short-circuit, the two digest loops keep their per-row output positions (trunc before R9c/line-count/tally,
  full digest after, :584-593), and `trunc_digest_pins` still prints `hit` while the full-digest line still
  prints the nearest path `p` — that difference is why `_digest_hit` returns both.
- `TALLY_TOKEN` is the byte-identical literal `[A-Z][A-Z0-9_]*SELFTEST`, so `HIDDEN_TOKEN_RE` stays
  case-sensitive (R2 spec: an ASCII uppercase token) and `PINLIKE_T0_RE` stays its `re.I` twin; making one
  stand in for the other would have widened or narrowed a rule, which is not a deletion.

## 4. Considered and rejected

- **`pin_keys` via `pin_commands`** (deletes the second `SPAN_RE` scan, :428-433): rejected — it couples a
  no-command function to the command binder and depends on `rev=None` semantics of `command_from_span`. Four
  lines saved, one new coupling; the shared literal (D4) already removes the duplication that mattered.
- **Merging the two digest loops into one generator** (would delete `trunc_digest_pins` and the :584-593 loop):
  rejected — it reorders per-row output lines. Deletion that moves observable output is not free weight.
- **`PY_FLAGS` (`-I`, `-B`)**: live, not dead — `SKILL.md:665` binds `python3 -I tools/mori-routed-check.py
  --selftest`, so the flag loop in `argv_ok` is exercised by real data. (It still has no selftest arm; that is
  an R8 coverage gap for the builder, not a deletion.)
- **`inside_tree`** (:269) has one caller but is a named containment guard, not dead weight.
- **Historical provenance** — the `v2 (round 47, after …)` comment (:106-109) and the docstring's v2/v3
  paragraphs are explicitly marked historical and were left alone.

## 5. Observations outside this seat (reported, not scored)

- `evidence/after-c1-at-e4dfff32.txt` — the contract's "target after" C1 receipt — is **0 bytes** and
  untracked (`git status`: `?? .ufo/waves/round-48/evidence/after-c1-at-e4dfff32.txt`; `wc -c` → 0). My own run
  of the claim command above supplies the same receipt content. Class: landing/receipt gap, not a C1 predicate
  failure.
- `count-c1.py`'s identity no-op `text = text.replace("(743 lines)", "(743 lines)")` is already on record from
  w1 `SimpCounters.md` candidate 1; not re-reported here to avoid a second authority.

## 6. D9 detail (documentation, not behaviour)

Landed :45-47 describes the digest pin as row-wide ("named anywhere in the row"), which R10 (round-48
`CritJunkClasses` D1) replaced with the cell-nearest rule implemented at :589-590; landed :82 documents
`… duplicate=N min_tally_pins=N rev=… baseline=…` while the tool prints `… duplicate=N hidden=N
min_tally_pins=N …` (:611). The v3 paragraph at the top of the docstring is current; the "What it reads" /
"Output" sections are v2-era. Repair is text-only and changes no predicate, so it was not scored here.

## 7. Proposal for round 49

Apply D1-D8 in the landed order (D4 before D3 is not required; D2 touches three call sites, D8 three
signatures), then D9. Acceptance for the round: `python3 -I -B tools/mori-pin-check.py --selftest` →
`PIN_CHECK_SELFTEST pass=60 fail=0`; `count-c1.py --tool tools/mori-pin-check.py --rev <new tip>` → `C1=met`;
and the four `diff`s of §2 stay empty. If any of the three moves, drop the candidate — none of the eight is
needed for the claim, so none may be paid for with a rule change.

## 8. Tradeoff

Net +6 lines for −6 duplicated authorities and −9 dead slots. The one real cost is `_digest_hit`'s two-value
return, which exists only to keep the two digest output lines byte-identical; a round that is willing to
reorder those lines can collapse it further. No tool was installed or upgraded (existing `pyflakes`/`vulture`
in `~/.local/bin` were used read-only); no pacman transaction was attempted; no tracked file, frozen file, or
fleet/sibling-lane state was touched.
