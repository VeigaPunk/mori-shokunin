measured 2026-10-23T12:00:11Z
control J4 shape rule-level skip (endpoint-only round_changed)
control_sha256 d7e45111051b156f962b8cac319fdf67342ac69de272919fa76e2a0e2aaed39d
counter_sha256 302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb

Axes: mutation specificity, detector discrimination, exact restoration, containment.

## Mutant and expected detector

The single mutated assignment selects endpoint immutable differences among ids held at both endpoints, plus ids absent at the tip but held at the base. It therefore loses intermediate changes that leave no endpoint difference. All other behavior is shared byte-for-byte with the pristine scratch tool. Mutation point: `.ufo/waves/round-36/c0/controls/J4.py:99-101`; contract: `.ufo/waves/round-36/contract.md:62-77`.

Expected result: the frozen counter rejects this control because round_changed must include changes anywhere in the range, including changed-back ids (`contract.md:73-74`). The bounded read-only detector uses the unchanged counter oracle (`count-c2.py:527-585`) on the real revision/base and compares all lists and the exit code.

## Frozen hashes checked before scoring

Command: `timeout 120 sha256sum /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py`

```text
ed3f0e5e779e7a034fe916b74307971a4ae847491c4f8d70e3de40c2b3ac4145  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c1.py
302f9aa05b5435bc4894edcd7e4ceb682f51830e62732273f49c60e9c29aaffb  /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py
```

Both match `.ufo/waves/round-36/evidence/freeze.txt:3-4`.

## Pristine, mutated, restored probe

The same command was run in all three phases:
`timeout 120 python3 /fast/scratch/hyaku/mori-r36/CtlJ4/detect.py /fast/scratch/hyaku/mori-r36/CtlJ4/probe.py`

Pristine output, detector exit 0:
```text
oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
tool: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
tool_exit=1 expected_exit=1
detector=pass
```

Mutated output, detector exit 1:
```text
oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
tool: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182]
tool_exit=1 expected_exit=1
detector=fail
```

Restored output, detector exit 0:
```text
oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
tool: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
tool_exit=1 expected_exit=1
detector=pass
```

Restoration evidence, from `timeout 120 sha256sum /fast/scratch/hyaku/mori-r36/CtlJ4/probe.py` at each phase:
```text
pristine 5cd71396fe88dff63bec6784202b5f885b264be7efa4c776f9455287c504fbae
mutated  d7e45111051b156f962b8cac319fdf67342ac69de272919fa76e2a0e2aaed39d
restored 5cd71396fe88dff63bec6784202b5f885b264be7efa4c776f9455287c504fbae
```

Mutation outcome: killed; baseline and restored detector passed. Scratch pristine bytes were restored exactly; the explicitly requested defective control remains at the assigned lane control path, with the same SHA-256 as the tested mutant.

## Full scored counter receipt

Command: `timeout 900 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/count-c2.py 6bd57097 --tool /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J4.py`

```text
P-C2: at revision R, tools/mori-sources-appendonly.py prints exactly the counter's hidden truth for ids, deleted, superseded and round_changed on each of 24 sandbox SOURCES.md histories drawn at run time, and on the lane's own history (rev 6bd57097, round base f10a320d) it prints exactly the counter's independent oracle, which lists at least one id.
tool: /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-36/c0/controls/J4.py
blind arm: 18/24 sandbox histories matched the hidden truth (3.4s; coverage: deletions=20 changed-back=13 superseded=11)
  repo01 FAIL: lists differ
      want: appendonly_violations=2 ids=[S284] deleted=[S200] superseded=[] round_changed=[S200,S232,S284]
      got:  appendonly_violations=2 ids=[S284] deleted=[S200] superseded=[] round_changed=[S200,S284]
  repo05 FAIL: lists differ
      want: appendonly_violations=3 ids=[S046] deleted=[S149,S153] superseded=[] round_changed=[S046,S149,S153,S226]
      got:  appendonly_violations=3 ids=[S046] deleted=[S149,S153] superseded=[] round_changed=[S149,S153,S226]
  repo07 FAIL: lists differ
      want: appendonly_violations=2 ids=[S043,S134] deleted=[] superseded=[S043] round_changed=[S043,S099,S134]
      got:  appendonly_violations=2 ids=[S043,S134] deleted=[] superseded=[S043] round_changed=[S043,S134]
  repo13 FAIL: lists differ
      want: appendonly_violations=1 ids=[S102] deleted=[] superseded=[S102] round_changed=[S102,S137,S295]
      got:  appendonly_violations=1 ids=[S102] deleted=[] superseded=[S102] round_changed=[S102]
  repo14 FAIL: lists differ
      want: appendonly_violations=1 ids=[] deleted=[S296] superseded=[] round_changed=[S054,S296]
      got:  appendonly_violations=1 ids=[] deleted=[S296] superseded=[] round_changed=[S296]
  repo23 FAIL: lists differ
      want: appendonly_violations=3 ids=[] deleted=[S086,S170,S273] superseded=[] round_changed=[S086,S291]
      got:  appendonly_violations=3 ids=[] deleted=[S086,S170,S273] superseded=[] round_changed=[S086]
real arm: FAIL (2.9s)
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182]
  oracle: appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]
  diff: round_changed: want=['S182', 'S193'] got=['S182']
  tool exit=1
C2=unmet
seed=17288421735995570710
```

Counter exit: 1. No seed override was supplied. All bounded foreground commands returned; no background jobs or subagents were started. No tools were installed or updated. The counter was run unchanged after L1 explicitly authorized its self-cleaning transient writes and clone packs (MoriR36 ruling delivered by `wait`); authored files stayed within the assigned report/control/scratch paths.

VERDICT: J4 unmet exit 1
