measured 2026-10-23T04:56:38Z

# Control C-junk — content-free shape (tsukuroi r30–r32 precedent)

Item: CtlJunk. Shape: the control accepts any arguments, prints `{}` and exits 0 — no sample
reading, no class detection, no rate computation, no decision of any kind.

## Sandbox

- Sandbox path: `/fast/scratch/hyaku/mori-r34/CtlJunk/clone`
- Clone source: `/home/vgpnk/Projects/shokunin/mori-shokunin` (read-only; no git writes in the lane repo)
- Clone base HEAD at clone time: `24603186b555dddb88ebd607e415e27bdea747b4` (the required frozen lane commit)
- Sandbox commit with the control: `72410534bfe9a721b1017ab6a580b1ace74c36a0`
  (`control C-junk: content-free tool (prints {} exit 0)`)
- Files changed in the sandbox: `tools/mori-disk-rate.py` (new) only.

## Control source (sandbox commit `7241053`)

```python
#!/usr/bin/env python3
"""Control C-junk (content-free shape, tsukuroi r30-r32).

Accepts any arguments, prints `{}` on stdout and exits 0. Performs no work of any kind:
no sample reading, no class detection, no rate computation.
"""
import sys


def main(argv):
    # Accept and ignore every argument.
    _ = argv
    sys.stdout.write("{}")
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
```

## Counter output — run 1 (fresh seed)

Command:
`timeout 600 python3 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-34/count-c1.py HEAD --repo /fast/scratch/hyaku/mori-r34/CtlJunk/clone`

```
measured_at=2026-10-23T04:55:39Z repo=/fast/scratch/hyaku/mori-r34/CtlJunk/clone rev=72410534bfe9a721b1017ab6a580b1ace74c36a0
tool=present guard=clean seed=4300382100404031191
fixed_pass=0/12 random_pass=0/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=live-shape
first_fails=[(1, 'mismatch'), (2, 'mismatch'), (3, 'mismatch'), (4, 'mismatch'), (5, 'mismatch')]
C1=unmet
```

Exit code: `1`

## Counter output — run 2 (fresh seed)

```
measured_at=2026-10-23T04:55:48Z repo=/fast/scratch/hyaku/mori-r34/CtlJunk/clone rev=72410534bfe9a721b1017ab6a580b1ace74c36a0
tool=present guard=clean seed=8226748040398848854
fixed_pass=0/12 random_pass=0/300
states_seen=['absent', 'bad-line', 'gone', 'new', 'ok', 'reset'] classes_seen=['disk', 'partition', 'stacked', 'unknown', 'virtual'] coverage=ok
live=live-shape
first_fails=[(1, 'mismatch'), (2, 'mismatch'), (3, 'mismatch'), (4, 'mismatch'), (5, 'mismatch')]
C1=unmet
```

Exit code: `1`

## Verdict

control C-junk: C1=unmet

## Observations for the judge

- The counter discriminates the content-free shape correctly and for the right reason: the tool
  parses as JSON and exits 0 (`tool=present`, `guard=clean`), so the failure is not an exit-code
  or parse accident — it is `fixed_pass=0/12`, `random_pass=0/300` (every scenario `mismatch`)
  and `live=live-shape` (no `devices` key), i.e. the control does not produce the claimed
  operation at all.
- `coverage=ok` in the output is **not** evidence for the control: `states_seen`/`classes_seen`
  are accumulated from the *oracle's* expected devices inside `score_seeds`, not from the tool's
  output. A content-free tool therefore trivially "covers" all six states and all five classes
  while matching none of them. This is a reporting quirk of the counter's own print line, not a
  hole in the predicate (`met` requires `not ffix and not frand and lv is None`), but a reader
  skimming `coverage=ok` alone could misread it as a pass signal.
- The guard only fires on the literal substrings `.ufo` and `count-c1`; the control is trivially
  clean there, as expected for a content-free control.

## Tooling

No tools installed or updated for this seat (nothing was needed beyond the frozen counter and
stock `python3`/`git`).
