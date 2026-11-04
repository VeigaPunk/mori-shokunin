# Mo82S01Lesson — round 82 w1 scoped findings

## Behavior and touched surfaces

Produced only:
- `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-82.md`
- `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-82/w1/Mo82S01Lesson.md` (this report)

The lesson names all six axes, all three frozen claims/keepers/targets,
entering/freeze revisions, the complete inherited controls receipt, a
PENDING SCOUT recommendation Gate, three mistake classes and census.
No source row, knowledge entry, product code or other seat's file edited.

## Commands actually executed and outcomes

One shell invocation, cwd `/home/vgpnk/Projects/shokunin`:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin mori; printf 'census_rc=%s\n' "$?"
```

Output: 35 W04 duplicate-URL warnings, then
`mori\tok\t/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md`
and `census_rc=0`. Warnings name S035, S037, S073, S074, S075, S076,
S147, S148, S149, S150, S166, S168, S201, S218, S220, S228, S349,
S351, S470, S476, S486, S491, S492, S546, S552, S565, S566, S567,
S568, S570, S571, S583, S585, S586 and S587. No zero-warning claim.

One Python eval cell (fact computation, no writes):

```python
import pathlib,re
p=pathlib.Path('/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/SOURCES.md')
s=p.read_text()
ids=re.findall(r'^ {0,3}\|\s*(S\d{3,})\s*\|',s,re.M)
print('source_rows='+str(len(ids)))
print('max_id='+max(ids,key=lambda x:int(x[1:])))
print('S597_present='+str('S597' in ids))
```

Output:

```text
source_rows=369
max_id=S596
S597_present=False
```

These are a working-tree observation, not a committed after-revision or
final source count after admission. The before count 369/exit 0 is inherited
from `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/lessons/round-81.md`
Census after-block; it was not re-executed at the entering revision.

## Read provenance and gates

Used read/grep/glob tools (not shell re-execution) on absolute lane paths:
- `.ufo/waves/round-82/contract.md`, then `evidence/controls-r82.txt`;
- `corpus/lessons/round-81.md` and `round-81-verifier-spotcheck.md`;
- `SCORECARD.md` headings and ranges 6–60, 4034–4054, 4101–4160;
- `corpus/SOURCES.md:330-420`, `corpus/QUALITY.md` and last 100 lines;
- `SKILL.md` last 70 lines; `PROVINCE.md:540-615`;
- `corpus/README.md:337-370`;
- `.ufo/waves/round-82/w1-dispatch.json:300-302` for scout scope;
- wave/w1 directory listings and scoped source/classification/pins globs;
- `tools/mori-record-sweep.py` search for `REVISION_MISMATCH`: no matches.

All relative names in this provenance list expand under
`/home/vgpnk/Projects/shokunin/mori-shokunin/`.
Read `skill://godspeed` and `skill://agent-self-evaluation`.
A combined headings grep mistakenly used colon separators and returned
Path not found; corrected using semicolons. No state change resulted.

Scout pin directory/report absent at first inspection, so the assignment's
explicit PENDING SCOUT alternative was used. No invented URL, HTTP result,
sha256, quote or source admission. S597 is a verified available id, not an
admitted row. The rejection is a stronger-claim screening rejection, not
a claim to have opened an external rejected body.

## Findings and limits

- At inspection `/home/vgpnk/Projects/shokunin/mori-shokunin/SCORECARD.md:13`
  said the r10 pin was retired with 64 classifications (45 added, 19 changed),
  while `/home/vgpnk/Projects/shokunin/mori-shokunin/corpus/evidence/drift-classification-r82.txt`
  was absent. The Retired row at SCORECARD.md:60 also referenced it. This is
  a transient in-flight claim/evidence gap, not a final defect verdict.
- The revision arm and real pins were absent at inspection; the lesson
  explicitly does not call the implementation repaired or green. Frozen
  keepers are the delivered falsification surfaces, not proof of acceptance.
- Repeated D80-4/D81-1, D81-3 scratch replay failure and 72-round drift debt
  are attributed to the retained non-author closure/controls, not fresh
  reproduction of the historical defects.
- Blocker sent only to `agent://MoriR82`: missing scout and implementation
  evidence precluded stronger closure claims. No broadcast or dispatch.
- No C1/C2/C3 counter, selftest, mutation fixture or battery executed by
  this seat. No final revision, publication, source admission or fleet health
  verified. The L1 must use the frozen keepers on its named landed revision
  and bind subsequent source/census results to that revision.
- No scratch files/directories created; nothing to remove. No tool installs,
  upgrades, PATH writes, pacman transaction, git/jj mutation, host/service/
  credential/harness/orchestration changes, commits or pushes.

## Self-evaluation

Accuracy 4: separates inherited receipts and measured census from unrun
claims; Gate lacks source observations by explicit permitted fallback.
Completeness 3: implementation repair closure cannot be recorded while
its evidence is absent; this limitation is explicit in each affected row.
Clarity 4: required ordered sections retained; long controls are mandated
verbatim material. Actionability 4: exact keeper and census commands plus
missing prerequisites named. Conciseness 4: some repeated provenance limits
are retained to prevent a contract-only seat being read as execution.
Overall 3.8/5. Highest-impact improvement is L1 integration of actual
landed repair receipts and the scout pin, not fabrication or rerunning
another seat's work. A user should agree with the conservative evidentiary
assessment; no stronger completeness claim is made.
