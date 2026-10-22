# CriticHarmScreen — round 30 wave 1, pre-data no-harm attack on C1 and C2

Seat `MoriR30.CriticHarmScreen` (critic, leaf, read-only). Lane tip read `e936482a`; entering tip `58b61681`. Only
this report was written; no git writes, no units touched, no installs (none needed). `skill://godspeed` is not on
this host (`find / -xdev -path '*skills/godspeed*'` printed nothing). `RULES.md` was read. Tool facts are cited by
line at `58b61681`; the tool is unchanged at `e936482` (`git diff --quiet 58b61681 HEAD -- tools/`).

## Bottom line

1. **Can the C2.1 fix flip an older `KILLER_ACTED`? Yes, for one plausible fix shape, and the counter would catch it.**
   The residual cases force the tool to give a non-active earlyoom a "current invocation". It currently has none:
   `tools/mori-oom-killers.py:274-278` scopes only active units, `:436-458` nulls version, grammar, actions,
   dry-run and process-group counts for non-active units, and `:465-469` takes a non-active unit's evidence only
   from the earlier bucket. If the fix bounds that invocation at the last version line and keeps `acted` reading
   only the earlier bucket, frozen `cases-a2.json:a2-09-removed-unit-three-sends-oomd-active` (absent unit, three
   sends after its only version line, oomd 0) drops out of `KILLER_ACTED`. Every older case pins `verdict`
   (94/94), so condition 2 fails loudly. That is caught, not hidden.
2. **The real gap is silent drift in unpinned fields.** Only 3 of the 36 older `KILLER_ACTED` cases pin
   `earlier_invocation_send_lines`. Round 29's tool change `cdfcf66d` already changed that field on 4 older cases
   with every pin holding (control run below), and the round-29 closure's "all 94 older pins hold"
   (`round-29-verifier-spotcheck.md:94`) did not see it. `PASS 32/32, 32/32, 30/30` cannot show that kind of harm.
   A full-output diff can.
3. **The round-29 disputed-harm ruling is only partly guarded, and C2.3 can reverse it** (§1, H3). Depth,
   freshness and coverage traps are H4–H6 in §4.

## 1. Round-29 closure's disputed-harm ruling (`round-29-verifier-spotcheck.md:77-98`)

The shape (active, start stamp missing or 0, a real send, then a plain restart) went from `KILLER_ACTED` before
`cdfcf66d` to `KILLERS_UNKNOWN` after (`:79-80`). Ruled **not harmed**: A2-06 reports an active unit's earlier sends
"without a verdict change" (`:87-88`), active plus incomplete scope is `KILLERS_UNKNOWN` (`:89-90`), and no older case
pins `KILLER_ACTED` for it (`:94-95`). Writers get the same rules (`rule-text.md:46-47`, `:110`). The closure was not
admitted (`:149-150`; MANIFEST `rounds[483]` `admitted:false`), so a later judge seat can contradict it: two
authorities over one shape. Current guard, from the active, unbounded cases at `58b61681` (in-memory `read_inputs`):

| case | expect | earlier | sigterm |
|---|---|---|---|
| `r29-a2-07-real-then-dryrun-zero-enter` | KILLERS_UNKNOWN | 1 | 0 |
| `r29-a2-07-real-dryrun-real-missing-enter` | KILLER_ACTED (current SIGKILL) | 1 | 0 |
| `a2-05-monotonic-zero-active-quiet`, `r29-a2-10-unbounded-missing-stamp-alone` | KILLERS_UNKNOWN | 0 | 0 |
| four others | KILLER_ACTED | 0 | 0 or 1 |

Counterexample [INFERENCE from the table]: a tool change that makes an active unit's earlier sends count as evidence
only when the last invocation is not dry-run would break no pin in the 118 frozen cases. Only the first row has
earlier > 0 with `KILLERS_UNKNOWN`, and its last invocation is dry-run. So the plain-restart verdict is held by the
written rule alone until C2.3 freezes. Axis: operability, and depth (`SKILL.md:697-698`).

Smallest safe correction (a pre-freeze LOG and lesson note, which does not narrow C2): a C2.3 mismatch pinning
`KILLER_ACTED` for the disputed shape is a reported C2 miss routed to the closure, never a tool change this round.

## 2. Could C2.1's fix flip an older `KILLER_ACTED`?

What the residual needs (Judge11–13, all `tool error`): for non-active units, version `1.9.0`, grammar
`verified-1.9.0`, and `dryrun_send_lines` and `process_group_lines` of 0 (now null through `:436-458`). Judge12
(failed unit) also needs the stamped send after the start stamp out of the earlier bucket (`earlier` 0) while the
verdict stays `KILLER_ACTED`. Older-file facts at `58b61681`: 22 non-active cases. None has a send at or after a
nonzero start stamp (`post=0` in every row), and none pins version, grammar, `dryrun_send_lines` or
`process_group_lines` (the pins are only `actions`, `scope_complete` and `earlier`). There are 36 older
`KILLER_ACTED` cases (10, 11 and 15 per file); all 94 cases pin `verdict`.

I modelled four fix shapes in memory over all four files (current invocation for a non-active unit bounded at the
start stamp or at the last version line; `acted` counting that invocation's non-dry-run sends or not):

| bound | acted counts current sends | `KILLER_ACTED` lost |
|---|---|---|
| start stamp | no | `cases-a2-r29.json:r29-a2-10-failed-stamped-positive` (residual; condition 1 fails) |
| start stamp | yes | none |
| last version line | no | `cases-a2.json:a2-09-removed-unit-three-sends-oomd-active` (**older**; condition 2 fails) and the r29 case above |
| last version line | yes | none (but `a2-09-…-three-sends` earlier count moves 3 → 0, and it is unpinned) |

So a correct fix needs both parts: bound at the start stamp (which matches the judges' reasoning, round-26 `:78-79`),
and count current-invocation non-dry-run sends of a non-active unit as positive evidence. The last row shows the
unpinned-drift hazard: a correct-looking verdict, but a reported count changed on an older `KILLER_ACTED` case with
no pin to object.

Check O2 (§3) proves the drift is real: from `7118f320` to `58b61681` it prints `older_cases=94 output_changed=4
killer_acted_lost=0`, with unpinned `earlier_invocation_send_lines` changed on `c35-malformed-monotonic-timestamp`,
`a2-10-malformed-action-line-uncounted`, `a2-10-positive-evidence-elsewhere-stands` and
`a2-10-oomd-notices-positive-malformed-records`. From `58b61681` to `HEAD` it prints `output_changed=0`.

## 3. Per-axis harm screen

`<tip>` is the landed tip; run in the lane (read-only) or a sandbox clone.

### Operability (score 7)

- **O1, older verdicts and pins.** Harm: an older case fails, or a frozen file is edited. Fails if any line is not
  `PASS` or any blob differs.

```sh
for f in cases.json cases-supplementary.json cases-a2.json cases-a2-r29.json; do
  git show <tip>:tools/mori-oom-killers.py > /tmp/t.py
  git show <tip>:tools/fixtures/mori-oom-killers/$f > /tmp/c.json
  python3 -I -B /tmp/t.py --selftest --cases /tmp/c.json | tail -1
  [ "$(git rev-parse 58b61681:tools/fixtures/mori-oom-killers/$f)" = "$(git rev-parse <tip>:tools/fixtures/mori-oom-killers/$f)" ] && echo blob-same || echo BLOB-CHANGED
done   # cases-a2-r29.json blob must equal d6d5cb0a's, not just 58b61681's (same blob: round-29 :61)
```

- **O2, unpinned drift and `KILLER_ACTED` loss on the 94 older cases (the harm the pins miss).** It must print
  `killer_acted_lost=0`, and every case listed as changed needs a rule-text justification in the lesson. Positive
  control `A=7118f320 B=58b61681` prints 4 changes (above).

```sh
A=58b61681 B=<tip> python3 -I -B - <<'EOF'
import json, os, subprocess, types
A, B = os.environ["A"], os.environ["B"]
def show(r, p): return subprocess.run(["git","show",f"{r}:{p}"],capture_output=True,check=True).stdout.decode()
def load(r):
    m = types.ModuleType("t"); exec(compile(show(r,"tools/mori-oom-killers.py"),"tool","exec"), m.__dict__); return m
def flat(d, p=""):
    o = {}
    for k, v in d.items(): o.update(flat(v, p+k+".")) if isinstance(v, dict) else o.__setitem__(p+k, v)
    return o
ma, mb = load(A), load(B); tot = chg = lost = 0
for f in ["cases.json","cases-supplementary.json","cases-a2.json"]:
    for c in json.loads(show("58b61681", f"tools/fixtures/mori-oom-killers/{f}"))["cases"]:
        tot += 1; (ra, ea), (rb, eb) = ma.read_inputs(c["inputs"]), mb.read_inputs(c["inputs"])
        fa, fb = flat(ra), flat(rb); fa["exit"], fb["exit"] = ea, eb
        d = sorted(k for k in set(fa) | set(fb) if fa.get(k) != fb.get(k))
        if d:
            chg += 1; lost += fa["verdict"] == "KILLER_ACTED" != fb["verdict"]; print(f, c["id"], d)
print(f"older_cases={tot} output_changed={chg} killer_acted_lost={lost}")
EOF
```

- **O3, interface.** Harm: a schema, verdict vocabulary, exit code or CLI change breaks the SKILL registry row
  (`SKILL.md:716`). Fails if the grep prints anything, or if the path list holds anything beyond
  `tools/mori-oom-killers.py` and `tools/fixtures/mori-oom-killers/cases-a2-r30.json`.

```sh
git diff 58b61681 <tip> -- tools/mori-oom-killers.py | grep -E '^[-+].*(SCHEMA *=|VERDICT_[A-Z]+ *=|EXIT_BY_VERDICT|add_argument)'
git diff --name-only 58b61681 <tip> -- tools/
```

- **O4, retention no-harm** (contract `:107-109`). Baseline observed by me: `metric 4` at both `58b61681` and
  `e936482a` (exit 1 both; `non_author 5`, `routed 0`). Fails if the value is above 4.

```sh
python3 -I -B tools/mori-retention-gate.py scan --repo . --rev <tip> --policy .ufo/waves/round-18/frozen/c1-policy.json --allowlist corpus/evidence/retention-allowlist.json | jq .metric
```

- **O5, gate replacement.** Harm: the round-29 gate or counters are edited, not superseded. Fails on any output of
  `git diff --name-only 58b61681 <tip> -- .ufo/waves/round-29/`.

### Depth (score 5)

- **D1, the entry contradicts the landed tool.** C1 rows cite older cases and pinned fields only (contract
  `:32-36`), so the counter survives the C2 fix. The entry's prose about non-active scoping does not. Run O2
  restricted to the C1 row case ids (`grep -o` the backticked ids from the table). Any changed case is a prose
  re-check item.
- **D2, the entry or Round30 SKILL rows contradict SKILL or the fixed tool.** Counterexample: after C2.1,
  `r29-a2-10-failed-stamped-positive` reads `KILLER_ACTED`, earlier 0, state `unavailable`. That contradicts any
  sentence saying a non-active unit's evidence is only `earlier_invocation_send_lines` (`SKILL.md:698`). Inactive
  units will print `dryrun_send_lines: 0` and `process_group_lines: 0`, against the "never zero counts" wording at
  `SKILL.md:694`; that wording is right for `actions` only. Check (each hit needs a qualifier naming the
  current-invocation path or limiting "never zero" to `actions`):

```sh
git show <tip>:corpus/knowledge/earlyoom-invocation-scope-r30.md | grep -n -i -E 'not active|inactive|non-active|never zero|only .*earlier'
git show <tip>:SKILL.md | grep -n 'Round30' | grep -i -E 'inactive|not active|never zero|earlier'
```

- **D3, SKILL or knowledge edits beyond the scope.** Fails if any removed SKILL line is not the R7 `SKILL.md:661`
  line, or any knowledge path besides the new entry appears.

```sh
git diff 58b61681 <tip> -- SKILL.md | grep '^-[^-]'
git diff --name-only 58b61681 <tip> -- corpus/knowledge/
```

- **D4, the A2a statement (R6 second half).** It must say `KILLERS_UNKNOWN` for the disputed shape (`SKILL.md:697`,
  `userspace-oom-killers-r26.md` F6 `:112-123`); it fails if it says `KILLER_ACTED`.

### Coverage (score 6): PROVINCE edits (R7)

- **V1.** Harm: R7 rewrites true text or edits outside the five ScoutShonen points (`round-29/w1/ScoutShonen.md:112-123`:
  `:32`, `:236`/`:294`/`:359`/`:375`, `:68`, `:66`, `:44-57` plus the Core list). Counterexample: rounds 24, 25
  and 26 closed admitted (MANIFEST `rounds[443]`, `[455]`, `[462]`), but round 27 at `:375` closed not admitted
  (`[468]`). It must read as rejected or not admitted, never "admitted". The adjacency lines `PROVINCE.md:365-370`
  stay true after C2 (an active unit's earlier sends are still not a verdict input) and must not change. Fails on a
  hunk outside those lines, a `:375` "admitted", or a hunk touching `:365-370`.

```sh
git diff -U0 58b61681 <tip> -- PROVINCE.md | grep '^@@'
git show <tip>:PROVINCE.md | grep -n -i -E 'round[- ]27|admission pending|admitted'
```

### Freshness (score 5): SOURCES rows

- **F1, append-only and ids.** Fails if any line is removed, or the new ids are not unique and contiguous from S156.
  R3 corrections are appended, never edited in place (contract `:116-117`).

```sh
git diff 58b61681 <tip> -- corpus/SOURCES.md | grep '^-[^-]'
git show <tip>:corpus/SOURCES.md | grep -o -E '^\| S[0-9]{3} ' | sort | uniq -d
```

- **F2, census.** Baseline (`.ufo/waves/round-30/evidence/census-start.txt`): ten W04 on S035, S037, S073–S076 and
  S147–S150, `mori ok`, exit 0. Counterexample: `main.c`, `kill.c`, `msg.h`, `README.md` and `earlyoom.default` at
  `rfjakob/earlyoom/v1.9.0` are each already rowed twice. A same-scope re-open without `supersedes` is error E04
  (`scripts/sources-census.sh:25`), and a cross-scope re-open is a new W04 (`:33`). Fails on any E line, a W line on
  S156+, or an exit other than 0. Run it on a clean checkout of `<tip>`; the census reads the working tree
  [INFERENCE].

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori | diff <(grep -v '^#\|^\$\|^exit' .ufo/waves/round-30/evidence/census-start.txt) -
```

### Calibration (score 5): SCORECARD rows

- **K1.** Harm: an Axes row moves without an admitted closure (contract `:53`, `:104`). At `e936482`, 0 removed
  lines since `58b61681` (`git diff 58b61681 HEAD | grep -c '^-[^-]'` printed `0`). Fails on any output.

```sh
diff <(git show 58b61681:SCORECARD.md | sed -n '10,15p') <(git show <tip>:SCORECARD.md | sed -n '10,15p')
git diff 58b61681 <tip> -- SCORECARD.md LOG.md corpus/QUALITY.md corpus/lessons/ | grep '^-[^-]'
```

### Adjacency (score 6)

- **A1, path set.** Allowed: the C1 set (contract `:14-17`), the C2 set (`:17-18`), and routed hygiene (`:111-120`:
  LOG, `corpus/lessons/round-30.md`, SOURCES, PROVINCE, `SKILL.md:661`, QUALITY, SCORECARD append), plus
  `.ufo/waves/round-30/**`. Fails on any other path (no sibling lanes or fleet paths).

```sh
git diff --name-only 58b61681 <tip> | grep -v -E '^(\.ufo/waves/round-30/|corpus/knowledge/earlyoom-invocation-scope-r30\.md$|corpus/evidence/sources-r30/|corpus/SOURCES\.md$|corpus/lessons/round-30\.md$|corpus/QUALITY\.md$|SKILL\.md$|PROVINCE\.md$|LOG\.md$|SCORECARD\.md$|tools/mori-oom-killers\.py$|tools/fixtures/mori-oom-killers/cases-a2-r30\.json$)'
```

- **A2, entry content.** Harm: the entry drifts into diagnosing, enabling or tuning earlyoom, which belongs to
  tsukuroi and the operator (`PROVINCE.md:368-370`, `SKILL.md:678-683`), or it quotes this host's configured
  values. Fails on any hit that is advice rather than a cited upstream fact.

```sh
git show <tip>:corpus/knowledge/earlyoom-invocation-scope-r30.md | grep -n -i -E 'systemctl (enable|start|restart|edit)|/etc/default/earlyoom|--prefer|--avoid|--ignore|tune|recommend'
```

## 4. Findings

| # | Counterexample | Evidence | Axes | Kind | Smallest safe correction |
|---|---|---|---|---|---|
| H1 | last-version-line bound for non-active units without counting current sends loses older `KILLER_ACTED` `a2-09-removed-unit-three-sends-oomd-active` | §2 model; tool `:465-469` | operability | fixable (caught by verdict pin) | bound at the start stamp and count current non-dry-run sends of a non-active unit |
| H2 | the fix changes unpinned fields on older cases, invisible to `PASS N/N` | O2 control: 4 unpinned changes from `cdfcf66d` | operability, depth | fixable | add O2 to the lesson's tip receipts; justify each changed case |
| H3 | a C2.3 `tool error` ruling reverses the round-29 plain-restart ruling; only a dry-run restart is guarded | §1 table; contract `:96-101`; spot-check `:149-150` | operability, depth | tradeoff for the closure | pre-freeze LOG note: a disputed-shape `KILLER_ACTED` mismatch is a reported miss, not a tool change |
| H4 | C1 prose or Round30 SKILL rows say non-active evidence is only earlier sends, or "never zero counts" | `SKILL.md:694,698`; Judge12 expect (earlier 0, `KILLER_ACTED`) | depth | fixable | write the entry against the landed tool; qualify "never zero" to `actions` |
| H5 | an S156+ row re-opens an already-rowed earlyoom v1.9.0 URL in the same scope | `sources-census.sh:25`; SOURCES URL counts | freshness, operability | fixable | open new URLs or add `supersedes`; F2 must match the baseline |
| H6 | R7 writes "admitted" at `PROVINCE.md:375` | MANIFEST `rounds[468]` `admitted:false` | coverage, calibration | fixable | per-round wording from MANIFEST |

Unrun (no landed tip yet): O1, O3, O5, D1–D4, V1, F1–F2, K1, A1–A2. Run and observed: O2 in both directions, the
O4 baseline, the four-shape model, the active-unbounded enumeration, the census baseline and the MANIFEST reads.

`Report:` .ufo/waves/round-30/w1/CriticHarmScreen.md
