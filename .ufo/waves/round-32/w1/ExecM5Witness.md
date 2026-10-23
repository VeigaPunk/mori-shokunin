# w1 — ExecM5Witness (routed defect 1: the M5 correction)

Seat: `MoriR32A2.ExecM5Witness`. Lane `/home/vgpnk/Projects/shokunin/mori-shokunin`.
Scratch: `/fast/scratch/hyaku/mori-r32/ExecM5Witness/`. Read-only on the lane; no lane writes, no git/jj writes.

**Axes named (godspeed):** correctness of the M5 wording; completeness of the masked-set enumeration; reusability of the
enumeration (a script a future counter can rerun); zero-harm (no lane file touched by me, no score changed).
**Verdict: the closure's masked set is CONFIRMED. The lesson's original wording ("ten end on a list entry") is a
different set, and both numbers are stated in the drafted correction.**

## 1. What was asked vs what the data says

The round-31 closure (`corpus/lessons/round-31-verifier-spotcheck.md:57`, §8 item 1) says the masked set is "the 9
fixtures with an expected hit on their last line (F02, F06–F08, F10, F11, F13, F15, F16), not 'ten end on a list
entry'". The round-31 lesson M5 (`corpus/lessons/round-31.md:46-48`) says "ten of the 16 frozen fixtures end on a list
entry". Both numbers are true — of *different sets*. F09, F12 and F14 end on a list entry but carry no expected hit on
that line; F15 and F16 carry their expected hit on the last line but end on prose.

## 2. Script

`/fast/scratch/hyaku/mori-r32/ExecM5Witness/masked_lastline.py` (also `masked_lastline.out`):

```python
#!/usr/bin/env python3
"""ExecM5Witness: which round-31 C2 fixtures have an expected hit on their LAST line?

The A1 counter (count-c2-a1.py:55) writes each brief as
    lines + "\n<!-- nonce ... -->\n"
so the brief's last real line is never the file's last line.  The P-C2 counter
(count-c2.py:87) writes lines + "\n", so it IS.  A tool that drops a file's last
line therefore still passes under A1 whenever the dropped line carries an
expected hit, and fails under P-C2.

This script derives the masked set two ways:
  (a) MASKED  = fixtures with an expected hit whose line number == len(lines)
                (the last line of the fixture body)   -> what the nonce hides
  (b) LIST-ENTRY = fixtures whose last line is a list entry, using the tool's own
                entry rules (mori-blind-check.sh:143-151) -> the lesson's original
                wording "ten end on a list entry"
and prints the symmetric difference, so the correction can state both numbers.

usage: masked_lastline.py [--repo <lane-repo>]
"""
import hashlib
import json
import os
import re
import sys

LANE = '/home/vgpnk/Projects/shokunin/mori-shokunin'
FIXTURES = '.ufo/waves/round-31/c2-fixtures.json'
FIXTURES_SHA256 = '1442c14e963bf77df34774015dff7ee73a9738d49b3911d26b4e3b96f48e0b31'
FIXTURES_A1 = '.ufo/waves/round-31/c2-fixtures-a1.json'
FIXTURES_A1_SHA256 = '133547ee55c40635bb288ad0f84f590920a70601c5bed62ff914cbd5848b25fc'

NUM_MARKER_RE = re.compile(r'^[0-9]+[.)]\s')


def is_list_entry(line):
    """mori-blind-check.sh:143-151 - an entry line of the files-opened block."""
    trimmed = line.strip()
    if not trimmed:
        return False
    if trimmed.startswith(('- ', '* ', '+ ', '|')):
        return True
    if trimmed[0].isdigit() and NUM_MARKER_RE.match(trimmed):
        return True
    return False


def is_separator(line):
    """mori-blind-check.sh:144 - table separator row (not an entry)."""
    t = line.strip()
    return bool(t) and set(t) <= set(' \t:|-') and '-' in t and '|' in t


def read(repo, rel):
    path = os.path.join(repo, rel)
    with open(path, 'rb') as h:
        raw = h.read()
    return raw


def analyse(fixtures, label):
    masked, list_entry = [], []
    print(f'--- {label} ---')
    for f in fixtures:
        n = len(f['lines'])
        last = f['lines'][-1]
        hits_on_last = [(a, b) for a, b in f['expect'] if a == n]
        entry = is_list_entry(last) and not is_separator(last)
        if hits_on_last:
            masked.append(f['id'])
        if entry:
            list_entry.append(f['id'])
        print(f"{f['id']}: nlines={n} last_line={last!r} last_is_list_entry={entry} "
              f"expect={f['expect']} hits_on_last_line={hits_on_last}")
    return masked, list_entry


def main(argv):
    repo = LANE
    it = iter(argv)
    for a in it:
        if a == '--repo':
            repo = next(it)
        else:
            print(__doc__)
            return 2

    raw = read(repo, FIXTURES)
    sha = hashlib.sha256(raw).hexdigest()
    print(f'{FIXTURES} sha256={sha} frozen_match={sha == FIXTURES_SHA256}')
    raw_a1 = read(repo, FIXTURES_A1)
    sha_a1 = hashlib.sha256(raw_a1).hexdigest()
    print(f'{FIXTURES_A1} sha256={sha_a1} frozen_match={sha_a1 == FIXTURES_A1_SHA256}')

    doc = json.loads(raw)
    doc_a1 = json.loads(raw_a1)

    masked, list_entry = analyse(doc['fixtures'], f"16 frozen fixtures ({FIXTURES})")
    print()
    masked_a1, list_entry_a1 = analyse(doc_a1['fixtures'], f"11 A1 fixtures ({FIXTURES_A1})")

    print()
    print(f'MASKED (expected hit on the fixture last line) frozen: n={len(masked)} {masked}')
    print(f'LIST-ENTRY (fixture last line is a list entry) frozen: n={len(list_entry)} {list_entry}')
    only_entry = [i for i in list_entry if i not in masked]
    only_masked = [i for i in masked if i not in list_entry]
    print(f'list-entry but NOT masked: n={len(only_entry)} {only_entry}')
    print(f'masked but NOT list-entry: n={len(only_masked)} {only_masked}')
    print(f'MASKED A1 (all 27): n={len(masked) + len(masked_a1)} {masked + masked_a1}')
    print(f'LIST-ENTRY A1: n={len(list_entry) + len(list_entry_a1)} {list_entry + list_entry_a1}')

    # Does dropping the last line change the expected hit set?  (the P-C2 mutant)
    changed = []
    for f in doc['fixtures']:
        n = len(f['lines'])
        want = {(a, b) for a, b in f['expect']}
        got = {(a, b) for a, b in f['expect'] if a != n}
        if want != got:
            changed.append(f['id'])
    print(f'P-C2 EOF-drop would DIFF on: n={len(changed)} {changed}')
    print(f'equals MASKED set: {changed == masked}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
```

## 3. Script output (the answer)

```
.ufo/waves/round-31/c2-fixtures.json sha256=1442c14e963bf77df34774015dff7ee73a9738d49b3911d26b4e3b96f48e0b31 frozen_match=True
.ufo/waves/round-31/c2-fixtures-a1.json sha256=133547ee55c40635bb288ad0f84f590920a70601c5bed62ff914cbd5848b25fc frozen_match=True
--- 16 frozen fixtures (.ufo/waves/round-31/c2-fixtures.json) ---
F01: nlines=8 last_line='The scratch JSON passed python3 json.load; I opened no lane source.' last_is_list_entry=False expect=[] hits_on_last_line=[]
F02: nlines=4 last_line='- corpus/SOURCES.md:12' last_is_list_entry=True expect=[[3, 'writer-forbidden-opened-path'], [4, 'writer-forbidden-opened-path']] hits_on_last_line=[(4, 'writer-forbidden-opened-path')]
F03: nlines=7 last_line='The rule text was enough.' last_is_list_entry=False expect=[] hits_on_last_line=[]
F04: nlines=3 last_line='Some prose naming nothing.' last_is_list_entry=False expect=[[1, 'writer-missing-files-opened-list']] hits_on_last_line=[]
F05: nlines=3 last_line='I read only the rule text.' last_is_list_entry=False expect=[[1, 'writer-missing-files-opened-list']] hits_on_last_line=[]
F06: nlines=6 last_line='| PROVINCE.md | scope |' last_is_list_entry=True expect=[[6, 'writer-forbidden-opened-path']] hits_on_last_line=[(6, 'writer-forbidden-opened-path')]
F07: nlines=3 last_line='2) LOG.md' last_is_list_entry=True expect=[[3, 'writer-forbidden-opened-path']] hits_on_last_line=[(3, 'writer-forbidden-opened-path')]
F08: nlines=3 last_line='- the brief template' last_is_list_entry=True expect=[[3, 'writer-forbidden-opened-path']] hits_on_last_line=[(3, 'writer-forbidden-opened-path')]
F09: nlines=4 last_line='- tools/mori-census.sh was not opened' last_is_list_entry=True expect=[] hits_on_last_line=[]
F10: nlines=6 last_line='- SKILL.md' last_is_list_entry=True expect=[[2, 'writer-forbidden-opened-path'], [6, 'writer-forbidden-opened-path']] hits_on_last_line=[(6, 'writer-forbidden-opened-path')]
F11: nlines=3 last_line='- /fast/scratch/hyaku/mori-r31/CaseOther/in.json' last_is_list_entry=True expect=[[3, 'writer-forbidden-opened-path']] hits_on_last_line=[(3, 'writer-forbidden-opened-path')]
F12: nlines=4 last_line='- file:///fast/scratch/hyaku/mori-r31/@REPORT@/x.json' last_is_list_entry=True expect=[[3, 'writer-forbidden-opened-path']] hits_on_last_line=[]
F13: nlines=3 last_line='- `tools/fixtures/mori-oom-killers/cases.json`.' last_is_list_entry=True expect=[[3, 'writer-forbidden-opened-path']] hits_on_last_line=[(3, 'writer-forbidden-opened-path')]
F14: nlines=6 last_line='- corpus/SOURCES.md' last_is_list_entry=True expect=[] hits_on_last_line=[]
F15: nlines=5 last_line='See tools/mori-oom-killers.py:42 for the parser.' last_is_list_entry=False expect=[[5, 'writer-tool-source-citation']] hits_on_last_line=[(5, 'writer-tool-source-citation')]
F16: nlines=7 last_line='exit 0' last_is_list_entry=False expect=[[7, 'writer-tool-run-output']] hits_on_last_line=[(7, 'writer-tool-run-output')]

MASKED (expected hit on the fixture last line) frozen: n=9 ['F02', 'F06', 'F07', 'F08', 'F10', 'F11', 'F13', 'F15', 'F16']
LIST-ENTRY (fixture last line is a list entry) frozen: n=10 ['F02', 'F06', 'F07', 'F08', 'F09', 'F10', 'F11', 'F12', 'F13', 'F14']
list-entry but NOT masked: n=3 ['F09', 'F12', 'F14']
masked but NOT list-entry: n=2 ['F15', 'F16']
MASKED A1 (all 27): n=16 ['F02', 'F06', 'F07', 'F08', 'F10', 'F11', 'F13', 'F15', 'F16', 'A01', 'A02', 'A03', 'A04', 'A08', 'A09', 'A11']
LIST-ENTRY A1: n=21 ['F02', 'F06', 'F07', 'F08', 'F09', 'F10', 'F11', 'F12', 'F13', 'F14', 'A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11']
P-C2 EOF-drop would DIFF on: n=9 ['F02', 'F06', 'F07', 'F08', 'F10', 'F11', 'F13', 'F15', 'F16']
equals MASKED set: True
```

(The 11 A1 rows of the output are in `masked_lastline.out`; the summary lines above are the ones that answer the
question.)

**Answer: the closure's 9 are CONFIRMED** — F02, F06, F07, F08, F10, F11, F13, F15, F16, computed from the frozen
fixtures' own bytes (sha256 matches the counter's frozen digest, so the enumeration is from the scored bytes, not a
re-read of the lesson).

**Both numbers for the correction:** 9 fixtures have an expected hit on their last line (the masked set); 10 of the 16
frozen fixtures end on a list entry (the lesson's original wording). The two sets differ by 5 ids: F09, F12, F14 are
list-entry-ending but not masked; F15, F16 are masked but not list-entry-ending.

## 4. Independent corroboration (counters run on a mutant, not on my arithmetic)

I rebuilt the EOF-drop mutant from the tip tool bytes (`git show 52435f2f:tools/mori-blind-check.sh`, sha256
`79b774f7736cc9074fa786ad360553987d92096a3864b07212f7a3127924beb8`) — the diff is exactly the two lines the round-31
critic used:

```
113c113
<         while IFS= read -r line || [[ -n $line ]]; do
---
>         while IFS= read -r line; do
203c203
<         done <<< "$content"
---
>         done < <(printf '%s' "$content")
```

My rebuilt mutant is byte-identical to the round-31 one (`sha256 03fdaa2abed72e140af751b76f4a6aeb8cd12e4d8b1b1ffaa5be37348c42698c`,
`diff` exit 0 against `/fast/scratch/hyaku/mori-r31/CriticAmendmentA1/tool-eofdrop.sh`).

`python3 .ufo/waves/round-31/count-c2.py 52435f2f --tool-file tool-eofdrop.sh` → exit 1:

```
F02 diff want=[(3, 'writer-forbidden-opened-path'), (4, 'writer-forbidden-opened-path')] got=[(3, 'writer-forbidden-opened-path')]
F06 diff want=[(6, 'writer-forbidden-opened-path')] got=[]
F07 diff want=[(3, 'writer-forbidden-opened-path')] got=[]
F08 diff want=[(3, 'writer-forbidden-opened-path')] got=[]
F10 diff want=[(2, 'writer-forbidden-opened-path'), (6, 'writer-forbidden-opened-path')] got=[(2, 'writer-forbidden-opened-path')]
F11 diff want=[(3, 'writer-forbidden-opened-path')] got=[]
F13 diff want=[(3, 'writer-forbidden-opened-path')] got=[]
F15 diff want=[(5, 'writer-tool-source-citation')] got=[]
F16 diff want=[(7, 'writer-tool-run-output')] got=[]
fixtures=16 exact=7/16
C2=unmet
```

The counter's own diff set is **exactly** my MASKED set (programmatic comparison: `EQUAL: True`). F12 is the decisive
discriminator — it ends on a list entry but is `exact` under the mutant, because its hit is on line 3 of 4.

`python3 .ufo/waves/round-31/count-c2-a1.py 52435f2f --tool-file tool-eofdrop.sh` → exit 0:

```
run2 tool_exit=1 scanned=27 scanned_ok=yes blind_violations=24 hit_lines=24 duplicate_hit_lines=0 count_ok=yes exit_ok=yes stray=0
run2 fixtures=27 exact=27/27
runs_met=2/2
C2=met
```

The same mutant against the tip tool (control, shows the tip is not the masked shape): `count-c2.py` → `exact=16/16`,
`C2=met` exit 0; `count-c2-a1.py` → `exact=27/27` in both runs, `runs_met=2/2`, `C2=met` exit 0.

## 5. Mechanism (cited, not inferred)

- `count-c2-a1.py:55` — `text = '\n'.join(f['lines']).replace(doc['placeholder'], name) + f'\n<!-- nonce {nonce} -->\n'`
  → the fixture's last body line is never the file's last line.
- `count-c2.py:87` — `text = '\n'.join(f['lines']).replace(doc['placeholder'], name) + '\n'` → it is the file's last line.
- `tools/mori-blind-check.sh:113` (`while IFS= read -r line || [[ -n $line ]]; do`) and `:203` (`done <<< "$content"`)
  are the two lines whose mutation produces the EOF-drop; `:143-151` is the entry-line rule my LIST-ENTRY test
  reimplements.
- The masked set spans **every rule the tool implements**, not only `writer-forbidden-opened-path`: F15 is
  `writer-tool-source-citation` and F16 is `writer-tool-run-output`. This is what §8 item 1 ("across every rule") means;
  a wording that named only the forbidden-path rule would understate the hole.

## 6. Drafted appended correction for `corpus/lessons/round-31.md` (M5)

Append-only; the M5 entry itself is not edited. Old wording quoted in the paragraph. Saved at
`/fast/scratch/hyaku/mori-r32/ExecM5Witness/m5-correction-draft.md`; ready to paste under a new `## Appended corrections
to round-31 records (round 32, wave 1; the M5 entry above stands as written)` heading at the end of the file:

```markdown
## Appended corrections to round-31 records (round 32, wave 1; the M5 entry above stands as written)

- **M5 correction — the masked set is the 9 fixtures whose *expected hit* is on their last line, not the "ten [that] end
  on a list entry".** Old wording, quoted from `corpus/lessons/round-31.md:46-48` (M5): "`count-c2-a1.py:55` appends
  `<!-- nonce … -->` after every brief, so no block reaches end of file; ten of the 16 frozen fixtures end on a list
  entry." Correction: the ten frozen fixtures that end on a list entry are F02, F06, F07, F08, F09, F10, F11, F12, F13 and
  F14; the set the nonce actually masks is the 9 whose **expected hit falls on the fixture's last line** — F02, F06–F08,
  F10, F11, F13, F15 and F16 — and the two sets are not the same. F09, F12 and F14 end on a list entry but carry no
  expected hit on that line (F09 and F14 expect no hits at all; F12's hit is on line 3 of 4); F15 and F16 carry their
  expected hit on the last line but end on prose, not on a list entry. The masked set spans every rule the tool
  implements, not only `writer-forbidden-opened-path`: F02, F06–F08, F10, F11 and F13 are
  `writer-forbidden-opened-path`, F15 is `writer-tool-source-citation` and F16 is `writer-tool-run-output`. Mechanism
  (unchanged): `count-c2-a1.py:55` writes each brief as `lines + "\n<!-- nonce … -->\n"`, so the fixture's last body
  line is never the file's last line, while `count-c2.py:87` writes `lines + "\n"`, so it is; a tool that drops a file's
  last line therefore keeps every expected hit under A1 and loses the last-line hits under P-C2. Evidence: the frozen
  fixtures (`.ufo/waves/round-31/c2-fixtures.json`, sha256
  `1442c14e963bf77df34774015dff7ee73a9738d49b3911d26b4e3b96f48e0b31`) recomputed by id and by the tool's own entry
  rules (`tools/mori-blind-check.sh:143-151`), and the EOF-drop mutant of the tip tool (bytes sha256
  `03fdaa2abed72e140af751b76f4a6aeb8cd12e4d8b1b1ffaa5be37348c42698c`, differing from the tip tool only at lines 113 and
  203) scored against both counters: `count-c2.py 52435f2f --tool-file <mutant>` → `exact=7/16`, `C2=unmet`, differing
  on exactly those 9 ids; `count-c2-a1.py 52435f2f --tool-file <mutant>` → `exact=27/27` in both runs, `runs_met=2/2`,
  `C2=met`. The same 7/16 vs 27/27 split was recorded in round 31 at
  `.ufo/waves/round-31/r1/CriticAmendmentA1.md`. Effect on the verdict: none — the tip tool scores `16/16` under
  `count-c2.py` and `27/27` under `count-c2-a1.py` — so this correction changes no score and closes only the wording of
  M5. The M5 fix rule stands unchanged: an amendment that perturbs the inputs must state, per perturbation, which
  failure mode it can mask, and must keep the original predicate as an explicit conjunct in the counter.
```

Note for the integrator: my seat's bounds are "write only your own report file and files under your own scratch dir",
so I did **not** append this to `corpus/lessons/round-31.md`. The L1 (or `ScribeRoutedDefects`, which owns the
`## Routed defects … disposition` prose) applies the block above; it is append-only and does not touch the M5 entry.

## 7. Files, tools, risks

Files written (all inside my bounds): this report `.ufo/waves/round-32/w1/ExecM5Witness.md`; scratch
`masked_lastline.py`, `masked_lastline.out`, `m5-correction-draft.md`, `tool-tip.sh`, `tool-eofdrop.sh`,
`eofdrop.c2.txt`, `eofdrop.c2a1.txt`, `tip.c2.txt`, `tip.c2a1.txt` (all under
`/fast/scratch/hyaku/mori-r32/ExecM5Witness/`). No lane file was edited; `git status --porcelain` in the lane shows only
the pre-existing `?? .scratch/`, `?? .ufo/waves/round-32/__pycache__/`, `?? .ufo/waves/round-32/w1/`. No git/jj write
anywhere. No process left running; every command was `timeout`-capped (counters ≤300 s, others ≤120 s) and the
counters' own `/tmp` sandboxes are removed by the counters themselves (`count-c2.py` uses `tempfile.mkdtemp` +
`shutil.rmtree`; I pointed `TMPDIR` at my scratch dir for the `count-c2.py` runs).

Tools: no install or update was needed — `python3` (stdlib only), `git`, `bwrap` 0.13.1 and `timeout` were already
present. Nothing installed, nothing upgraded, no host service touched.

Risks / blockers: none for the enumeration. Two judgement calls the L1 may want to review: (a) the correction quotes the
M5 old wording as "`count-c2-a1.py:55` appends … ten of the 16 frozen fixtures end on a list entry" and locates it at
`corpus/lessons/round-31.md:46-48`; (b) the correction states both numbers (9 masked / 10 list-entry-ending) plus the
5-id symmetric difference, so a reader can re-derive which is which. [INFERENCE] The draft's claim "spans every rule the
tool implements" is verified for the three rules the 16 frozen fixtures exercise
(`writer-forbidden-opened-path`, `writer-tool-source-citation`, `writer-tool-run-output`); a rule that only ever fires on
a non-last line would of course not be masked, so the phrase means "every rule the masked fixtures exercise", which is
what the 9 ids show.
