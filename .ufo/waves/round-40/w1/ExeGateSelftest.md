# ExeGateSelftest

Axis: C2 selftest coverage and evidence fidelity.

## Direct run

Command:

```sh
python3 /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-sources-appendonly.py --selftest
```

Output:

```text
MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0
```

## Per-arm PASS records

The direct CLI reports failures and the aggregate summary, but does not print a PASS line for each successful arm. I reran the same selftest with a Python trace hook on `check_one`'s successful branch (line 845) to emit the per-arm records; the gate source was not changed.

Command:

```sh
python3 -c 'import runpy, sys
script = "/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-sources-appendonly.py"
def trace(frame, event, arg):
    if event == "line" and frame.f_code.co_name == "check_one" and frame.f_lineno == 845:
        print("PASS %s" % frame.f_locals["name"])
    return trace
sys.settrace(trace)
sys.argv = [script, "--selftest"]
runpy.run_path(script, run_name="__main__")'
```

Output:

```text
PASS clean history
PASS mutable-only edit
PASS immutable edit
PASS changed-back inside the round
PASS deleted row
PASS superseding row
PASS supersede before edit
PASS row reorder
PASS whitespace padding
PASS side-branch superseder is stale
PASS merge does not fabricate an edit
PASS landing is the last edit commit
PASS never-edited superseded row is as-of
PASS first-parent-lacks-path merge contributes no edits
PASS linear delete-then-re-add is not an edit
MORI_SOURCES_APPENDONLY_SELFTEST pass=15 fail=0
```

This confirms all 15 selftest arms reached the successful check branch and the aggregate was `pass=15 fail=0`.