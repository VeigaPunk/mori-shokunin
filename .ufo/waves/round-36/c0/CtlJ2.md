measured 2026-10-23T11:52:26Z
control J2 shape rule-level skip (prior state)
control_sha256 f34cdbdee5b4b1fa8d2c28d5a4b2b9ac621e3d4b97b38d07ef880424de3914c6
counter_sha256 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb

Axes: byte fidelity, detector discrimination, containment, restoration.
Control: `.ufo/waves/round-36/c0/controls/J2.py`, an exact copy of `6bd57097:.ufo/waves/round-35/check-sources-appendonly.py`, without a CLI or output adapter.
Expected detector: frozen count-c2.py should report C2=unmet for the prior-state control (contract.md:85-101).

## Byte evidence
Commands: `timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 6bd57097:.ufo/waves/round-35/check-sources-appendonly.py | timeout 120 sha256sum`; `timeout 120 sha256sum` on the control and frozen files, before scoring and after scoring.
Source before and after: f34cdbdee5b4b1fa8d2c28d5a4b2b9ac621e3d4b97b38d07ef880424de3914c6.
Control before and after: f34cdbdee5b4b1fa8d2c28d5a4b2b9ac621e3d4b97b38d07ef880424de3914c6.
`timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -s 6bd57097:.ufo/waves/round-35/check-sources-appendonly.py` printed 5093.
C1 counter before and after: ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145.
C2 counter before and after: 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb.
Contract after: d903c67950a081c3e25d19a208f79c84ab6e34f99680acea31d3f8590eaa431a.
These equal the freeze entries in `.ufo/waves/round-36/evidence/freeze.txt:2-4`.

## Contained execution
Counter scratch paths are fixed at count-c2.py:42,668,687-688. Every final run used the unchanged counter in a read-only-root bwrap sandbox, mapping the seat scratch onto that fixed scratch root. A 10,000,000-byte per-file limit remained enforced. No tools were installed or updated.
`timeout 120 df -h /fast` printed `/dev/nvme1n1p2 804G 735G 69G 92% /fast` before clone writes.
To avoid copying large existing packs and checking out unrelated oversized archives, the scratch git template contained:
- `objects/info/alternates`: `/home/vgpnk/Projects/shokunin/mori-shokunin/.git/objects`
- `config`: core.sparseCheckout=true and core.sparseCheckoutCone=false
- `info/sparse-checkout`: `/corpus/SOURCES.md`
The template changes only sandbox object storage and working-tree materialization, not commits, counter bytes, control bytes or git-show history. The real oracle still walks the original ancestry (count-c2.py:527-585). Scratch template, temporary directories and the disposable clone probe were removed with bounded rm commands after use; no lane source or index was modified.

Exact scored command (no --seed):
```
timeout 900 bwrap --ro-bind / / --bind /fast/scratch/hyaku/mori-r36/CtlJ2 /fast/scratch/hyaku/mori-r36 --unshare-pid --unshare-net --proc /proc --dev /dev --die-with-parent --new-session --setenv TMPDIR /fast/scratch/hyaku/mori-r36/tmp --setenv GIT_TEMPLATE_DIR /fast/scratch/hyaku/mori-r36/template -- /usr/bin/prlimit --fsize=10000000:10000000 -- timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J2.py
```
Pristine and restored runs used the identical command without `--tool` and its value. All commands were foreground; sandbox process namespaces terminate their descendant processes on exit.

## Pristine output
```
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool_absent
C2=unmet
seed=12263662649948646864
```
Exit 1.

## J2 output (full scored counter output)
```
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J2.py
blind arm: 0/24 sandbox histories matched the hidden truth (2.5s; coverage: deletions=21 changed-back=14 superseded=10)
  repo00 FAIL: no summary line (exit 0): round_changed=[]
  repo01 FAIL: no summary line (exit 1): round_changed=[S206,S221,S296]
  repo02 FAIL: no summary line (exit 1): round_changed=[S106]
  repo03 FAIL: no summary line (exit 1): round_changed=[S284]
  repo04 FAIL: no summary line (exit 0): round_changed=[]
  repo05 FAIL: no summary line (exit 1): round_changed=[S098]
  repo06 FAIL: no summary line (exit 1): round_changed=[S228]
  repo07 FAIL: no summary line (exit 1): round_changed=[S248]
  repo08 FAIL: no summary line (exit 0): round_changed=[]
  repo09 FAIL: no summary line (exit 1): round_changed=[S028,S118]
  repo10 FAIL: no summary line (exit 0): round_changed=[]
  repo11 FAIL: no summary line (exit 1): round_changed=[S063,S160]
  repo12 FAIL: no summary line (exit 1): round_changed=[S297]
  repo13 FAIL: no summary line (exit 1): round_changed=[S112]
  repo14 FAIL: no summary line (exit 1): round_changed=[S125,S182]
  repo15 FAIL: no summary line (exit 1): round_changed=[S090,S259]
  repo16 FAIL: no summary line (exit 1): round_changed=[S124]
  repo17 FAIL: no summary line (exit 1): round_changed=[S190,S281,S298]
  repo18 FAIL: no summary line (exit 1): round_changed=[S010,S251]
  repo19 FAIL: no summary line (exit 0): round_changed=[]
  repo20 FAIL: no summary line (exit 0): round_changed=[]
  repo21 FAIL: no summary line (exit 1): round_changed=[S048,S077]
  repo22 FAIL: no summary line (exit 1): round_changed=[S170]
  repo23 FAIL: no summary line (exit 1): round_changed=[S289]
real arm: FAIL (0.4s)
  tool:   (no summary line)
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  diff: no summary line (exit 1)
  tool exit=1
C2=unmet
seed=11105846800254820548
```
Exit 1.

## Restored output
```
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool_absent
C2=unmet
seed=7279667990602129007
```
Exit 1. Restoration selected the unchanged original revision again; J2 remains only as the requested substitute artifact. Source/control hashes above establish unchanged bytes.

## Earlier unscored harness attempts
First pristine invocation omitted `--dev /dev`; counter output was:
```
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
counter setup error: git rev-parse --verify 6bd57097^{commit} failed in /home/vgpnk/Projects/shokunin/mori-shokunin: fatal: could not open '/dev/null' for reading and writing: Permission denied
```
Exit 2; no verdict. Adding the private device mount produced this earlier pristine run:
```
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool_absent
C2=unmet
seed=12995204462016331353
```
Exit 1. The initial J2 run, before configuring the scratch template, printed:
```
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J2.py
blind arm: 0/24 sandbox histories matched the hidden truth (2.5s; coverage: deletions=21 changed-back=18 superseded=9)
  repo00 FAIL: no summary line (exit 1): round_changed=[S023,S247]
  repo01 FAIL: no summary line (exit 0): round_changed=[]
  repo02 FAIL: no summary line (exit 1): round_changed=[S062,S146]
  repo03 FAIL: no summary line (exit 1): round_changed=[S155,S207]
  repo04 FAIL: no summary line (exit 0): round_changed=[]
  repo05 FAIL: no summary line (exit 1): round_changed=[S081,S095]
  repo06 FAIL: no summary line (exit 1): round_changed=[S117]
  repo07 FAIL: no summary line (exit 1): round_changed=[S274]
  repo08 FAIL: no summary line (exit 1): round_changed=[S245]
  repo09 FAIL: no summary line (exit 1): round_changed=[S284]
  repo10 FAIL: no summary line (exit 1): round_changed=[S066,S184,S289]
  repo11 FAIL: no summary line (exit 1): round_changed=[S115]
  repo12 FAIL: no summary line (exit 1): round_changed=[S106,S269]
  repo13 FAIL: no summary line (exit 1): round_changed=[S240]
  repo14 FAIL: no summary line (exit 1): round_changed=[S168]
  repo15 FAIL: no summary line (exit 1): round_changed=[S077,S157]
  repo16 FAIL: no summary line (exit 1): round_changed=[S088]
  repo17 FAIL: no summary line (exit 1): round_changed=[S201]
  repo18 FAIL: no summary line (exit 1): round_changed=[S007,S133,S225,S266]
  repo19 FAIL: no summary line (exit 1): round_changed=[S203,S206,S261]
  repo20 FAIL: no summary line (exit 1): round_changed=[S124,S290]
  repo21 FAIL: no summary line (exit 1): round_changed=[S031,S241,S267]
  repo22 FAIL: no summary line (exit 1): round_changed=[S177,S193]
  repo23 FAIL: no summary line (exit 1): round_changed=[S023,S059,S141]
counter setup error: git clone --no-local --quiet /home/vgpnk/Projects/shokunin/mori-shokunin /fast/scratch/hyaku/mori-r36/c2-533fa8be/lane-clone failed in /home/vgpnk/Projects/shokunin/mori-shokunin: fatal: fetch-pack: invalid index-pack output
```
Exit 2; no verdict. `timeout 120 git -C /home/vgpnk/Projects/shokunin/mori-shokunin count-objects -vH` showed size-pack 79.40 MiB. The file-size limit was not relaxed. A disposable clone probe with alternates then failed checkout on `.ufo/waves/round-22/evidence/measure2/synthetic-workspaces.tar.gz` and `measure3/synthetic-workspaces.tar.gz` (exit 128). Sparse checkout resolved that containment obstacle for the final runs.

## Interpretation
The exact legacy summary lacks deleted and prints round_changed separately (controls/J2.py:117-123); the frozen parser requires all fields on one line (count-c2.py:53-55). All 24 blind histories and the real arm rejected the interface. This receipt does not demonstrate semantic deletion-rule sensitivity independent of that interface rejection.
The pristine target is absent and fails, so the mutation probe is inconclusive, not a killed mutant. The separately requested negative-control score is unambiguously unmet. Frozen inputs and original source were unchanged; all scratch probes were disposable and removed.
VERDICT: mutation-probe inconclusive baseline tool_absent
VERDICT: J2 unmet exit 1
