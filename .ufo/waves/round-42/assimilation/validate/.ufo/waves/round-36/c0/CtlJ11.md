measured 2026-10-23T11:49:44Z
control J11 shape harness-keyed
control_sha256 ede4cfdcf9d5f2d4aae5bc35fbe7996914069fb6f2da0e6355aa55560f13a3b5
counter_sha256 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb

Axes: contract fidelity, harness selectivity, reproducibility.

## Mutant and expected detector

The only mutation is the condition at `.ufo/waves/round-36/c0/controls/J11.py:70`: replace the pristine `if False:` with a resolved-path gate. Repositories beneath `/fast/scratch` or `/tmp` use the contract implementation; all other repositories print the empty summary and return 0 (`J11.py:69-72`). The CLI includes `--path` (`J11.py:63-67`). This is the assigned shape in `.ufo/waves/round-36/contract.md:99`.

Expected detector: the frozen `count-c2.py`, bounded by `timeout 900`, should reject a harness-keyed defective control under the control decision rule (`contract.md:85-88`). Pristine, mutated and restored runs below use the same counter, revision and options, without `--seed`; only the tool file location differs for the published mutant.

## Frozen hash check before scoring

Command: `timeout 30 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py`

```text
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```

Both match `.ufo/waves/round-36/evidence/freeze.txt:3-4`.

## Pristine output

Command: `timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /fast/scratch/hyaku/mori-r36/CtlJ11/J11.py`

```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/CtlJ11/J11.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.6s; coverage: deletions=22 changed-back=15 superseded=12)
real arm: pass (2.2s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=5774851103740271775
counter_exit=0
```

## Mutated control: full scored output

Command: `timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J11.py`

```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J11.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.3s; coverage: deletions=22 changed-back=14 superseded=11)
real arm: pass (2.2s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=15059030611177113610
counter_exit=0
```

## Outside-harness witness

Command: `timeout 120 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J11.py 6bd57097 --repo /home/vgpnk/Projects/shokunin/mori-shokunin --round-base f10a320d`

```text
appendonly_violations=0 ids=[] deleted=[] superseded=[] round_changed=[]
tool_exit=0
```

The same lane history produced 18 violations in the counter's clone, as shown in the scored output. [INFERENCE] The path gate is invisible to this detector because both its sandbox repositories and its real-arm clone are below its scratch root (`count-c2.py:42,601,624-627,687`). This is a coverage finding; no contract change or integration was made.

## Restored output

The isolated scratch source was restored to `if False:` before this run; the published control retains the assigned mutant.

Command: `timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /fast/scratch/hyaku/mori-r36/CtlJ11/J11.py`

```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /fast/scratch/hyaku/mori-r36/CtlJ11/J11.py
blind arm: 24/24 sandbox histories matched the hidden truth (2.0s; coverage: deletions=22 changed-back=15 superseded=11)
real arm: pass (1.8s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  tool exit=1
C2=met
seed=9706403133870177
counter_exit=0
```

## Before/after hashes and restoration evidence

Command: `timeout 20 sha256sum /fast/scratch/hyaku/mori-r36/CtlJ11/J11.py` before mutation:

```text
b9121390bafd2c0ff3c26098f03b4135fbd028ffc2723e6d268e14a74d616c34  /fast/scratch/hyaku/mori-r36/CtlJ11/J11.py
```

Command: `timeout 20 sha256sum /fast/scratch/hyaku/mori-r36/CtlJ11/J11.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J11.py` after mutation:

```text
ede4cfdcf9d5f2d4aae5bc35fbe7996914069fb6f2da0e6355aa55560f13a3b5  /fast/scratch/hyaku/mori-r36/CtlJ11/J11.py
ede4cfdcf9d5f2d4aae5bc35fbe7996914069fb6f2da0e6355aa55560f13a3b5  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J11.py
```

Command: `timeout 20 sha256sum /fast/scratch/hyaku/mori-r36/CtlJ11/J11.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J11.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py` after restoration:

```text
b9121390bafd2c0ff3c26098f03b4135fbd028ffc2723e6d268e14a74d616c34  /fast/scratch/hyaku/mori-r36/CtlJ11/J11.py
ede4cfdcf9d5f2d4aae5bc35fbe7996914069fb6f2da0e6355aa55560f13a3b5  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J11.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```

The scratch before/restored hashes are identical. The mutant survived: pristine, mutant and restored detector exits were all 0, with both arms passing in each run. All counter stderr streams were empty. No tools were installed or updated. All bounded subprocess calls returned; no background jobs or persistent workers were started. No lane git writes were performed by this seat.

VERDICT: J11 met exit 0
