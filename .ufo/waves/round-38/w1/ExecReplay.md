# C1 counter replay at scored tip

## Result

Both requested runs returned `C1=met` and printed the requested seed plus `head_at_measurement=f725f3076972e6e70595b5ac8279be524a111ff8`. The drawn-arm revisions differ across the two seeds, as expected for the run-time draw; both drawn arms and both challenge arms passed.

## Retained command evidence

Executed concurrently from `/home/vgpnk/Projects/shokunin/mori-shokunin`:

```text
python3 .ufo/waves/round-38/count-c1.py f725f3076972e6e70595b5ac8279be524a111ff8 --seed 20261023
python3 .ufo/waves/round-38/count-c1.py f725f3076972e6e70595b5ac8279be524a111ff8 --seed 3737
```

Both runs: `blind arm: 24/24 sandbox histories matched the hidden truth`; `real arm: pass`; `tool exit=1` for the real arm's reported violations; the counter verdict was `C1=met`.

### Seed 20261023

```text
drawn arm: pass (6.1s) rev=6aa0e168f1 base=4890c2d571
  truth:  appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
challenge arm (real-arm clothing): pass (0.1s)
  truth:  appendonly_violations=4 ids=[S243,S281] deleted=[S060,S167] superseded=[S281] round_changed=[S243]
  tool:   appendonly_violations=4 ids=[S243,S281] deleted=[S060,S167] superseded=[S281] round_changed=[S243]
negative memo-n1.py     rejected (drawn arm fails (rev=6b68b2e1eb: lists differ: want appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[] got appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]))
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 3/4 (repo200: per-id lines differ (malformed=0)))
negative memo-sha.py    ACCEPTED (disclosed content-keyed bound) (all four arms pass)
C1=met
seed=20261023
head_at_measurement=f725f3076972e6e70595b5ac8279be524a111ff8
```

### Seed 3737

```text
drawn arm: pass (6.1s) rev=a187534967 base=4bfa049026
  truth:  appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
  tool:   appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[]
challenge arm (real-arm clothing): pass (0.1s)
  truth:  appendonly_violations=2 ids=[S158] deleted=[S275] superseded=[S158] round_changed=[S158,S275]
  tool:   appendonly_violations=2 ids=[S158] deleted=[S275] superseded=[S158] round_changed=[S158,S275]
negative memo-n1.py     rejected (drawn arm fails (rev=e33bb56171: lists differ: want appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] round_changed=[] got appendonly_violations=18 ids=[S041,S044,S051,S062,S064,S069,S179,S180,S181,S182,S183,S184,S185,S186,S188,S189,S190,S193] deleted=[] superseded=[S069,S182,S193] round_changed=[S182,S193]))
negative const.py       rejected (blind 4/4 (repo200: lists differ))
negative summary-only.py rejected (blind 3/4 (repo200: per-id lines differ (malformed=0)))
negative memo-sha.py    ACCEPTED (disclosed content-keyed bound) (all four arms pass)
C1=met
seed=3737
head_at_measurement=f725f3076972e6e70595b5ac8279be524a111ff8
```

Seed, verdict, and measured head match each invocation. The `memo-sha.py` acceptance is explicitly disclosed by the counter as the content-keyed bound, not one of the three required fabricated-negative rejections. The pre-existing `evidence/c1-after-r38.txt` is a separate receipt (`seed=20261023`, `head_at_measurement=daa1d4d2501e1671e7b7ff1fd60a069564f178b0`) and is not substituted for this scored-tip replay.

## Risks / blockers

No replay failure or seed discrepancy observed. No tools were installed. Only this report was written; counter-created temporary material was under the allowed round-38 scratch tree.
