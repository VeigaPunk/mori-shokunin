measured 2026-10-23T12:02:23Z
control J12 shape off-topic
control_sha256 9d34bfe11b4b4c8671cd64e6659d3c235d860106866f44ffb48c1a08802e44da
counter_sha256 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb

Axes: defect fidelity, detector separation, exact-byte restoration.
Mutant: remove only `not` from the comparison-column selector, selecting status, recheck and used-by instead of immutable cells (.ufo/waves/round-36/c0/controls/J12.py:15; .ufo/waves/round-36/c0/controls/J12.py:88). Endpoint comparison, deletion, supersession, round-range accounting and CLI remain the pristine implementation (.ufo/waves/round-36/c0/controls/J12.py:76-157). Expected detector: frozen count-c2.py rejects this off-topic control; baseline and restored bytes pass. Interface: frozen contract.md:60-77.

Freeze verification before scoring: `timeout 30 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py` produced:
```text
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```
These match the original freeze (.ufo/waves/round-36/evidence/freeze.txt:3-4). The C2 hash was checked again immediately before mutant scoring and before the restored run, with the same result.

Pristine command: `timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /fast/scratch/hyaku/mori-r36/CtlJ12/probe.py` (exit 0; no --seed).
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/CtlJ12/probe.py
blind arm: 24/24 sandbox histories matched the hidden truth (3.1s; coverage: deletions=19 changed-back=15 superseded=8)
real arm: pass (2.7s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=2008569582538551713
```

Restoration: the scratch selector was changed back exactly after mutant scoring. Pristine, mutant and restored hashes from bounded `sha256sum` commands:
```text
pristine ba395f22a85bbcbc5fbac48dc7b15a83349fa8e60a8530de58dd9e3946a464b8
mutated  9d34bfe11b4b4c8671cd64e6659d3c235d860106866f44ffb48c1a08802e44da
restored ba395f22a85bbcbc5fbac48dc7b15a83349fa8e60a8530de58dd9e3946a464b8
```
The mutated scratch hash equalled the scored lane control hash. Restored command: `timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /fast/scratch/hyaku/mori-r36/CtlJ12/probe.py`; the shell printed its captured exit code after the complete counter output:
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/CtlJ12/probe.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.0s; coverage: deletions=22 changed-back=17 superseded=11)
real arm: pass (1.6s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=4685204262552601603
COUNTER_EXIT=0
```

Post-receipt counter change: a later `timeout 30 sha256sum` returned c7edaacfff029c2055bee6ddda42ff6f5c040dad7fbac81e9d169602edcbac34 for count-c2.py. Scoring stopped on that mismatch. L1 identified this as its pre-data redesign after J11 met the original counter and explicitly retained this J12 original-counter receipt (agent://MoriR36, message received after the stop). No result here is claimed for the redesigned counter. An unscored scratch-only header-handling refinement had been written before the mismatch was noticed; it was discarded, restoring the exact original pristine probe again.
Final restoration command: `timeout 30 sha256sum /fast/scratch/hyaku/mori-r36/CtlJ12/probe.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J12.py` produced:
```text
ba395f22a85bbcbc5fbac48dc7b15a83349fa8e60a8530de58dd9e3946a464b8  /fast/scratch/hyaku/mori-r36/CtlJ12/probe.py
9d34bfe11b4b4c8671cd64e6659d3c235d860106866f44ffb48c1a08802e44da  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J12.py
```
Mutation outcome: killed, not inconclusive: pristine and restored receipts passed, whereas the identical scored mutant bytes failed both arms (outputs below and above). All three runs used the same original frozen detector with independently drawn seeds and no --seed. All detector commands completed; no persistent process was started. No tools were installed or updated. L1 authorized only the counter's own self-cleaning transient writes beyond seat scratch (agent://MoriR36); authored files remained in the assigned report/control and seat scratch.

Scored mutant command: `timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J12.py`; the shell printed its captured exit code after the complete counter output:
```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J12.py
blind arm: 2/24 sandbox histories matched the hidden truth (1.8s; coverage: deletions=20 changed-back=12 superseded=12)
  repo00 FAIL: lists differ
      want: appendonly_violations=3 ids=[S015,S288] deleted=[S016] superseded=[S015] round_changed=[S288]
      got:  appendonly_violations=2 ids=[S211] deleted=[S016] superseded=[] round_changed=[S211]
  repo01 FAIL: lists differ
      want: appendonly_violations=3 ids=[] deleted=[S017,S141,S290] superseded=[] round_changed=[S141]
      got:  appendonly_violations=5 ids=[S123,S196] deleted=[S017,S141,S290] superseded=[] round_changed=[S123,S141,S196]
  repo02 FAIL: lists differ
      want: appendonly_violations=4 ids=[S218] deleted=[S105,S122,S224] superseded=[S218] round_changed=[S218,S224]
      got:  appendonly_violations=5 ids=[S179,S203] deleted=[S105,S122,S224] superseded=[] round_changed=[S179,S224]
  repo03 FAIL: lists differ
      want: appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[S009]
      got:  appendonly_violations=1 ids=[S209] deleted=[] superseded=[] round_changed=[]
  repo04 FAIL: lists differ
      want: appendonly_violations=2 ids=[S176] deleted=[S162] superseded=[S176] round_changed=[S162]
      got:  appendonly_violations=2 ids=[S260] deleted=[S162] superseded=[] round_changed=[S162]
  repo05 FAIL: lists differ
      want: appendonly_violations=2 ids=[S281] deleted=[S294] superseded=[] round_changed=[S249,S281,S294]
      got:  appendonly_violations=3 ids=[S271,S281] deleted=[S294] superseded=[] round_changed=[S271,S294]
  repo06 FAIL: lists differ
      want: appendonly_violations=3 ids=[] deleted=[S033,S164,S219] superseded=[] round_changed=[S219]
      got:  appendonly_violations=5 ids=[S149,S190] deleted=[S033,S164,S219] superseded=[] round_changed=[S149,S219]
  repo07 FAIL: lists differ
      want: appendonly_violations=1 ids=[S182] deleted=[] superseded=[S182] round_changed=[S129]
      got:  appendonly_violations=1 ids=[S198] deleted=[] superseded=[] round_changed=[S198]
  repo08 FAIL: lists differ
      want: appendonly_violations=4 ids=[S125] deleted=[S212,S247,S290] superseded=[S125] round_changed=[S212,S290]
      got:  appendonly_violations=3 ids=[] deleted=[S212,S247,S290] superseded=[] round_changed=[S212,S290]
  repo10 FAIL: lists differ
      want: appendonly_violations=2 ids=[] deleted=[S043,S171] superseded=[] round_changed=[]
      got:  appendonly_violations=3 ids=[S239] deleted=[S043,S171] superseded=[] round_changed=[]
  repo11 FAIL: lists differ
      want: appendonly_violations=3 ids=[S028] deleted=[S145,S199] superseded=[S028] round_changed=[S028,S145,S181,S199,S207]
      got:  appendonly_violations=3 ids=[S181] deleted=[S145,S199] superseded=[] round_changed=[S145,S199]
  repo12 FAIL: lists differ
      want: appendonly_violations=4 ids=[S141,S187,S271] deleted=[S061] superseded=[S271] round_changed=[S061,S141,S187,S271]
      got:  appendonly_violations=4 ids=[S059,S074,S141] deleted=[S061] superseded=[] round_changed=[S059,S061,S074,S141]
  repo13 FAIL: lists differ
      want: appendonly_violations=4 ids=[S203,S258] deleted=[S105,S292] superseded=[S203] round_changed=[S105,S193,S203,S258,S292]
      got:  appendonly_violations=3 ids=[S063] deleted=[S105,S292] superseded=[] round_changed=[S063,S105,S292]
  repo14 FAIL: lists differ
      want: appendonly_violations=3 ids=[S238,S291] deleted=[S129] superseded=[S238] round_changed=[S129,S238,S291]
      got:  appendonly_violations=2 ids=[S063] deleted=[S129] superseded=[] round_changed=[S063,S129]
  repo15 FAIL: lists differ
      want: appendonly_violations=1 ids=[S234] deleted=[] superseded=[] round_changed=[S170,S234]
      got:  appendonly_violations=3 ids=[S051,S131,S259] deleted=[] superseded=[] round_changed=[S051,S131,S259]
  repo16 FAIL: lists differ
      want: appendonly_violations=5 ids=[S017,S227] deleted=[S196,S241,S289] superseded=[S017,S227] round_changed=[S227,S289]
      got:  appendonly_violations=6 ids=[S194,S227,S270] deleted=[S196,S241,S289] superseded=[S227] round_changed=[S194,S270,S289]
  repo17 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S272] superseded=[] round_changed=[S180]
      got:  appendonly_violations=2 ids=[S261] deleted=[S272] superseded=[] round_changed=[]
  repo18 FAIL: lists differ
      want: appendonly_violations=5 ids=[S060,S168,S267] deleted=[S079,S100] superseded=[S060,S168] round_changed=[S267]
      got:  appendonly_violations=2 ids=[] deleted=[S079,S100] superseded=[] round_changed=[]
  repo19 FAIL: lists differ
      want: appendonly_violations=2 ids=[S067] deleted=[S147] superseded=[] round_changed=[S067,S181,S184]
      got:  appendonly_violations=2 ids=[S002] deleted=[S147] superseded=[] round_changed=[S002]
  repo20 FAIL: lists differ
      want: appendonly_violations=3 ids=[S011,S298] deleted=[S262] superseded=[S011,S298] round_changed=[S011]
      got:  appendonly_violations=1 ids=[] deleted=[S262] superseded=[] round_changed=[]
  repo21 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S003] superseded=[] round_changed=[S003,S193]
      got:  appendonly_violations=2 ids=[S170] deleted=[S003] superseded=[] round_changed=[S003,S170]
  repo23 FAIL: lists differ
      want: appendonly_violations=2 ids=[S076] deleted=[S023] superseded=[] round_changed=[S076,S178]
      got:  appendonly_violations=3 ids=[S076,S134] deleted=[S023] superseded=[] round_changed=[S076]
real arm: FAIL (1.7s)
  tool:   appendonly_violations=44 ids=[S002,S003,S013,S014,S015,S031,S035,S036,S037,S038,S064,S065,S066,S067,S068,S071,S077,S078,S079,S080,S081,S082,S083,S084,S085,S086,S092,S097,S114,S115,S118,S119,S120,S145,S146,S151,S191,S192,S193,S194,S195,S196,S197,S198] deleted=[] superseded=[S067,S071,S083,S084,S097,S193] round_changed=[S182,S191,S192,S193,S194,S195,S196,S197,S198]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  diff: ids: want=['S041', 'S044', 'S051', 'S062', 'S064', 'S069', 'S179', 'S180', 'S181', 'S182', 'S183', 'S184', 'S185', 'S186', 'S188', 'S189', 'S190', 'S193'] got=['S002', 'S003', 'S013', 'S014', 'S015', 'S031', 'S035', 'S036', 'S037', 'S038', 'S064', 'S065', 'S066', 'S067', 'S068', 'S071', 'S077', 'S078', 'S079', 'S080', 'S081', 'S082', 'S083', 'S084', 'S085', 'S086', 'S092', 'S097', 'S114', 'S115', 'S118', 'S119', 'S120', 'S145', 'S146', 'S151', 'S191', 'S192', 'S193', 'S194', 'S195', 'S196', 'S197', 'S198']
  diff: superseded: want=['S069', 'S182', 'S193'] got=['S067', 'S071', 'S083', 'S084', 'S097', 'S193']
  diff: round_changed: want=['S182', 'S193'] got=['S182', 'S191', 'S192', 'S193', 'S194', 'S195', 'S196', 'S197', 'S198']
  diff: violations: want=18 got=44
  tool exit=1
C2=unmet
seed=12147777329960565828
COUNTER_EXIT=1
```
VERDICT: J12 unmet exit 1
