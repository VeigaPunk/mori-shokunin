measured 2026-10-23T11:53:24Z
control J5 shape rule-level skip (no deleted arm)
control_sha256 276b6b19b0c67770f1dccff50fd6ae016b335794c302f37b0bdc832b7a8f56e7
counter_sha256 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb

Axes: exact defect isolation, detector sensitivity, byte restoration.
Mutant: the only behavior-bearing substitution is `return set(previous) - set(current)` to `return set()` in `/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J5.py:68-69`.
This makes deleted=[] always and omits deletion events from round_changed. Immutable-edit events remain, including edits to ids later deleted (contract.md:69-77).
Expected detector: count-c2.py rejects the missing deleted ids and missing deletion events; blind truth is independent of the tool (count-c2.py:166-225,590-621).

Freeze check command: `timeout 15 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py`.
Observed C1: ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145.
Observed C2: 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb.
Both matched evidence/freeze.txt:3-4 before any detector run; both remained identical before unseeded scoring.
The contract hash was d903c67950a081c3e25d19a208f79c84ab6e34f99680acea31d3f8590eaa431a, matching evidence/freeze.txt:2.

## Pristine, mutated, restored detector
All replay commands used `timeout 900 env TMPDIR=/fast/scratch/hyaku/mori-r36/CtlJ5 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /fast/scratch/hyaku/mori-r36/CtlJ5/probe.py --seed 363605` from `/home/vgpnk/Projects/shokunin/mori-shokunin`.

Pristine output (successful command, C2=met; counter exit 0 under count-c2.py:720-723):
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/CtlJ5/probe.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.5s; coverage: deletions=23 changed-back=14 superseded=9)
real arm: pass (2.0s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=363605
```
Mutated replay: counter exit 1, C2=unmet; 1/24 blind histories matched; real arm passed.
Full actual replay output: /fast/scratch/hyaku/mori-r36/CtlJ5/mutated-replay.txt:1-79.
Example actual replay output (mutated-replay.txt:4-6):
```text
  repo00 FAIL: lists differ
      want: appendonly_violations=6 ids=[S004,S148,S229] deleted=[S140,S144,S172] superseded=[S229] round_changed=[S004,S140,S144,S172]
      got:  appendonly_violations=3 ids=[S004,S148,S229] deleted=[] superseded=[S229] round_changed=[S004]
```
Restored output:
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/CtlJ5/probe.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.0s; coverage: deletions=23 changed-back=14 superseded=9)
real arm: pass (1.8s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=363605
counter_exit=0
```
Mutation probe result: killed, not a baseline failure; the identical replay detector passed pristine and restored bytes and rejected mutated bytes.

## Unseeded scored receipt
Command: `timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J5.py`.
Environment: TMPDIR=/fast/scratch/hyaku/mori-r36/CtlJ5; cwd=/home/vgpnk/Projects/shokunin/mori-shokunin; no --seed.
Full counter output:
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J5.py
blind arm: 4/24 sandbox histories matched the hidden truth (2.2s; coverage: deletions=20 changed-back=15 superseded=10)
  repo00 FAIL: lists differ
      want: appendonly_violations=2 ids=[S273] deleted=[S274] superseded=[S273] round_changed=[S274]
      got:  appendonly_violations=1 ids=[S273] deleted=[] superseded=[S273] round_changed=[]
  repo02 FAIL: lists differ
      want: appendonly_violations=3 ids=[S198] deleted=[S062,S222] superseded=[S198] round_changed=[S062,S198,S222]
      got:  appendonly_violations=1 ids=[S198] deleted=[] superseded=[S198] round_changed=[S062,S198]
  repo03 FAIL: lists differ
      want: appendonly_violations=3 ids=[S185] deleted=[S224,S281] superseded=[] round_changed=[S185,S224]
      got:  appendonly_violations=1 ids=[S185] deleted=[] superseded=[] round_changed=[S185]
  repo04 FAIL: lists differ
      want: appendonly_violations=6 ids=[S025] deleted=[S030,S051,S155,S194,S238] superseded=[S025] round_changed=[S025,S030,S051,S155,S194,S238]
      got:  appendonly_violations=1 ids=[S025] deleted=[] superseded=[S025] round_changed=[S025,S030]
  repo06 FAIL: lists differ
      want: appendonly_violations=3 ids=[] deleted=[S019,S149,S268] superseded=[] round_changed=[S019,S268]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
  repo07 FAIL: lists differ
      want: appendonly_violations=3 ids=[S218] deleted=[S041,S233] superseded=[S218] round_changed=[S041,S218]
      got:  appendonly_violations=1 ids=[S218] deleted=[] superseded=[S218] round_changed=[S218]
  repo08 FAIL: lists differ
      want: appendonly_violations=4 ids=[S021,S247] deleted=[S037,S087] superseded=[S247] round_changed=[S021,S037,S087]
      got:  appendonly_violations=2 ids=[S021,S247] deleted=[] superseded=[S247] round_changed=[S021]
  repo10 FAIL: lists differ
      want: appendonly_violations=5 ids=[S170] deleted=[S059,S075,S192,S195] superseded=[] round_changed=[S092,S170]
      got:  appendonly_violations=1 ids=[S170] deleted=[] superseded=[] round_changed=[S092,S170]
  repo12 FAIL: lists differ
      want: appendonly_violations=3 ids=[S268] deleted=[S127,S166] superseded=[S268] round_changed=[]
      got:  appendonly_violations=1 ids=[S268] deleted=[] superseded=[S268] round_changed=[]
  repo13 FAIL: lists differ
      want: appendonly_violations=4 ids=[S212,S219] deleted=[S031,S180] superseded=[S212,S219] round_changed=[S105]
      got:  appendonly_violations=2 ids=[S212,S219] deleted=[] superseded=[S212,S219] round_changed=[S105]
  repo14 FAIL: lists differ
      want: appendonly_violations=4 ids=[S073,S180,S294] deleted=[S152] superseded=[] round_changed=[S073,S152,S180,S294]
      got:  appendonly_violations=3 ids=[S073,S180,S294] deleted=[] superseded=[] round_changed=[S073,S180,S294]
  repo15 FAIL: lists differ
      want: appendonly_violations=2 ids=[S198] deleted=[S099] superseded=[] round_changed=[S099,S198,S265]
      got:  appendonly_violations=1 ids=[S198] deleted=[] superseded=[] round_changed=[S198,S265]
  repo16 FAIL: lists differ
      want: appendonly_violations=3 ids=[S179] deleted=[S233,S298] superseded=[S179] round_changed=[S179,S233,S298]
      got:  appendonly_violations=1 ids=[S179] deleted=[] superseded=[S179] round_changed=[S179]
  repo17 FAIL: lists differ
      want: appendonly_violations=2 ids=[S051] deleted=[S280] superseded=[] round_changed=[S051,S275,S280]
      got:  appendonly_violations=1 ids=[S051] deleted=[] superseded=[] round_changed=[S051,S275]
  repo18 FAIL: lists differ
      want: appendonly_violations=2 ids=[S155] deleted=[S202] superseded=[] round_changed=[S155,S202]
      got:  appendonly_violations=1 ids=[S155] deleted=[] superseded=[] round_changed=[S155]
  repo19 FAIL: lists differ
      want: appendonly_violations=2 ids=[S110] deleted=[S057] superseded=[] round_changed=[S057,S110,S246]
      got:  appendonly_violations=1 ids=[S110] deleted=[] superseded=[] round_changed=[S057,S110,S246]
  repo20 FAIL: lists differ
      want: appendonly_violations=5 ids=[S188] deleted=[S058,S111,S244,S291] superseded=[S188] round_changed=[S058,S111,S188,S244,S291]
      got:  appendonly_violations=1 ids=[S188] deleted=[] superseded=[S188] round_changed=[S188]
  repo21 FAIL: lists differ
      want: appendonly_violations=4 ids=[] deleted=[S002,S130,S217,S262] superseded=[] round_changed=[S130,S156,S217]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S156]
  repo22 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S120,S170] superseded=[] round_changed=[S012,S120]
      got:  appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S012]
  repo23 FAIL: lists differ
      want: appendonly_violations=3 ids=[S071] deleted=[S037,S271] superseded=[] round_changed=[S071]
      got:  appendonly_violations=1 ids=[S071] deleted=[] superseded=[] round_changed=[S071]
real arm: pass (2.2s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=unmet
seed=5638869308831893512
counter_exit=1
```
VERDICT: J5 unmet exit 1

## Restoration and containment
Command: `timeout 15 sha256sum /fast/scratch/hyaku/mori-r36/CtlJ5/probe.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J5.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py`.
Scratch before: 80f53e2707d54e16b84e633edfa972387552d5e8379823a9bda8205b6e96e175
Scratch mutated: 276b6b19b0c67770f1dccff50fd6ae016b335794c302f37b0bdc832b7a8f56e7
Scratch restored: 80f53e2707d54e16b84e633edfa972387552d5e8379823a9bda8205b6e96e175
Lane control (retained intentionally as the requested defective control): 276b6b19b0c67770f1dccff50fd6ae016b335794c302f37b0bdc832b7a8f56e7
The before and restored scratch hashes are identical; the mutated scratch and retained control hashes are identical.
Only the assigned control and this report were written in the lane; no lane git/index writes were requested.
All four bounded counter commands completed. Python subprocess.run calls waited for their children; the counter waits for its children and removes its temporary work (count-c2.py:70-83,715-718). No background jobs were launched.
The frozen counter itself managed its prescribed sandbox histories and clone (count-c2.py:377-488,624-626,687-718); no sibling source was modified.
Tools installed or updated: none. Initial bash pty=true was unavailable; the command completed without a terminal. This tool mismatch was reported to xd://report_issue.
