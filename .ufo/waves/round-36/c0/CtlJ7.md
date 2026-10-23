measured 2026-10-23T12:00:42Z
control J7 shape rule-level skip (supersede discharges)
control_sha256 4d919ac6b9e5f11470106890118767ba61c363e6aa62772cf8804ec8dd0f4302
counter_sha256 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb

Axes: contract fidelity outside the assigned defect; isolated mutation; detector sensitivity.

Mutant: one added filter removes superseded ids from `ids` after computing the genuine `superseded` list; the violation total follows the filtered ids. Deleted, superseded and round_changed remain unchanged. Source: `.ufo/waves/round-36/c0/controls/J7.py:87-106`; contract: `.ufo/waves/round-36/contract.md:60-77,101`.
Expected detector: frozen C2 counter rejects that filtered ids list, while pristine and restored bytes meet P-C2. Same bounded detector, fresh unseeded histories in all three runs.

## Required scored control: full counter output

Command: `timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J7.py`

```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J7.py
blind arm: 15/24 sandbox histories matched the hidden truth (3.2s; coverage: deletions=22 changed-back=14 superseded=9)
  repo00 FAIL: lists differ
      want: appendonly_violations=5 ids=[S134] deleted=[S036,S195,S202,S226] superseded=[S134] round_changed=[S226]
      got:  appendonly_violations=4 ids=[] deleted=[S036,S195,S202,S226] superseded=[S134] round_changed=[S226]
  repo04 FAIL: lists differ
      want: appendonly_violations=2 ids=[S087] deleted=[S199] superseded=[S087] round_changed=[S199]
      got:  appendonly_violations=1 ids=[] deleted=[S199] superseded=[S087] round_changed=[S199]
  repo06 FAIL: lists differ
      want: appendonly_violations=5 ids=[S065,S169,S228] deleted=[S024,S120] superseded=[S169] round_changed=[S024,S065,S120,S169,S228]
      got:  appendonly_violations=4 ids=[S065,S228] deleted=[S024,S120] superseded=[S169] round_changed=[S024,S065,S120,S169,S228]
  repo07 FAIL: lists differ
      want: appendonly_violations=4 ids=[S027,S200] deleted=[S266,S269] superseded=[S200] round_changed=[S027,S116,S200,S266,S269]
      got:  appendonly_violations=3 ids=[S027] deleted=[S266,S269] superseded=[S200] round_changed=[S027,S116,S200,S266,S269]
  repo08 FAIL: lists differ
      want: appendonly_violations=4 ids=[S089,S215] deleted=[S060,S299] superseded=[S089] round_changed=[S060,S215,S299]
      got:  appendonly_violations=3 ids=[S215] deleted=[S060,S299] superseded=[S089] round_changed=[S060,S215,S299]
  repo12 FAIL: lists differ
      want: appendonly_violations=3 ids=[S178,S193] deleted=[S030] superseded=[S178] round_changed=[S030,S193]
      got:  appendonly_violations=2 ids=[S193] deleted=[S030] superseded=[S178] round_changed=[S030,S193]
  repo15 FAIL: lists differ
      want: appendonly_violations=1 ids=[S087] deleted=[] superseded=[S087] round_changed=[S011,S087]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[S087] round_changed=[S011,S087]
  repo16 FAIL: lists differ
      want: appendonly_violations=3 ids=[S152] deleted=[S199,S221] superseded=[S152] round_changed=[]
      got:  appendonly_violations=2 ids=[] deleted=[S199,S221] superseded=[S152] round_changed=[]
  repo20 FAIL: lists differ
      want: appendonly_violations=3 ids=[S061] deleted=[S077,S225] superseded=[S061] round_changed=[]
      got:  appendonly_violations=2 ids=[] deleted=[S077,S225] superseded=[S061] round_changed=[]
real arm: FAIL (3.0s)
  tool:   appendonly_violations=15 ids=[S041,S044,S051,S062,S064,S179,S180,S181,S183,S184,S185,S186,S188,S189,S190] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  diff: ids: want=['S041', 'S044', 'S051', 'S062', 'S064', 'S069', 'S179', 'S180', 'S181', 'S182', 'S183', 'S184', 'S185', 'S186', 'S188', 'S189', 'S190', 'S193'] got=['S041', 'S044', 'S051', 'S062', 'S064', 'S179', 'S180', 'S181', 'S183', 'S184', 'S185', 'S186', 'S188', 'S189', 'S190']
  diff: violations: want=18 got=15
  tool exit=1
C2=unmet
seed=12641020456393857723
```
Counter exit: 1. Mutation probe: killed (baseline and restoration below both met).
VERDICT: J7 unmet exit 1

## Pristine detector run

Command: `timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /fast/scratch/hyaku/mori-r36/CtlJ7/reference.py`

```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/CtlJ7/reference.py
blind arm: 24/24 sandbox histories matched the hidden truth (3.4s; coverage: deletions=22 changed-back=14 superseded=11)
real arm: pass (2.7s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=4703386713686510934
```
Counter exit: 0.

## Restored detector run

Command: same pristine command above, after removing exactly the added filter.

```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/CtlJ7/reference.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.2s; coverage: deletions=23 changed-back=18 superseded=9)
real arm: pass (1.9s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=6480038227132898007
```
Counter exit: 0.

## Hashes, restoration and containment

Observed `timeout 120 sha256sum` outputs, in execution order:

```text
initial count-c1.py: ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145
initial count-c2.py: 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb
pristine /fast/scratch/hyaku/mori-r36/CtlJ7/reference.py: 1803b3670b66abdfbd77fcdd806e32cb36f45d8de69684b83922f67be20322ad
mutated /fast/scratch/hyaku/mori-r36/CtlJ7/reference.py: 4d919ac6b9e5f11470106890118767ba61c363e6aa62772cf8804ec8dd0f4302
scored .ufo/waves/round-36/c0/controls/J7.py: 4d919ac6b9e5f11470106890118767ba61c363e6aa62772cf8804ec8dd0f4302
pre-score count-c2.py: 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb
restored /fast/scratch/hyaku/mori-r36/CtlJ7/reference.py: 1803b3670b66abdfbd77fcdd806e32cb36f45d8de69684b83922f67be20322ad
final .ufo/waves/round-36/c0/controls/J7.py: 4d919ac6b9e5f11470106890118767ba61c363e6aa62772cf8804ec8dd0f4302
final count-c1.py: ca65c75984333f1cc442c42438453377d94cb1688f71b116d1e5f3e1c3e74045
final count-c2.py: 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb
```

Initial counter hashes matched `.ufo/waves/round-36/evidence/freeze.txt:3-4`. The scratch reference was restored byte-for-byte; the requested lane control intentionally retains its defect. No counter was edited by this seat. The final C1 hash change was reported immediately; L1 attributed it to L1's pre-data C1 redesign and confirmed this unchanged-C2 v1 receipt stands (L1 reply via `agent://MoriR36`). No further scoring followed that alert.

L1 explicitly authorized the frozen counter's own self-cleaning shared scratch/temp writes, clone method and larger packfiles (L1 containment ruling via `agent://MoriR36`); authored lane files are only this report and J7.py. `timeout 120 df -h /fast` reported 70G available before counter runs; `timeout 120 /usr/bin/du -sh /home/vgpnk/Projects/shokunin/mori-shokunin/.git` reported 118M. No lane git writes, subagents, tool installs or tool updates were performed.
