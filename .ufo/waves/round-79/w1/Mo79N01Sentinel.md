# Round 79 w1 sentinel — write scope and redaction

Axes: operability, calibration, freshness. Read-only audit; no judgment, integration, dispatch, remediation or VCS mutation. Findings bind the snapshots below, not future sibling writes.

## 1. C1 imports and side effects

Read frozen contract §C1 (lines 29–44), SCORECARD Axes and r78 tail, QUALITY 159/161/162/163, and SKILL instrument registry. Enumerated imports via `ast.walk(ast.parse(tool_bytes))`, and searched with the specialized grep tool (case-sensitive):

```text
^(import |from )|open\(|subprocess|os\.(remove|unlink|rename|makedirs|mkdir)|socket|urllib|requests|shutil|tempfile|/tmp|read_text|write_text|write_bytes|exec\(|eval\(
```

Tool SHA-256: `b3b2f9e24d7aff284b1d50deef87a6862253ad20634d644d62c3d73245cdeb0a`.
Every import (including selftest-only imports):

```text
37: import os
38: import re
39: import sys
208: import io
209: from contextlib import redirect_stderr, redirect_stdout
```

Side-effect-capable calls: `open(path, "r", encoding="utf-8")` at tools/mori-control-receipt.py:110, `handle.read()` at :111; directory metadata reads `os.path.isdir` :191, `os.listdir` :195, `os.path.isfile` :196. Output calls `print` throughout and `out.write` :153 target passed streams; the live call supplies sys.stdout/sys.stderr at :203; selftest supplies StringIO. Remaining AST calls are parsing, collection/string operations and internal functions. No dynamic exec/eval, child runner, socket API, file mutation API or temporary-path allocation occurs in the source. Verb strings such as curl/systemctl are data in VERBS (:44–50), never executed.

**Item 1: no finding for file writes, subprocesses, sockets or /tmp.** The read-only `open` is required by the frozen input spec, not a forbidden write. In-memory selftest does attempt a deliberately missing absolute path (:296); it creates nothing.

**F1 — LOW, output-channel contract violation.** tools/mori-control-receipt.py:123,169,178,186–187,193,199 emit setup diagnostics to stderr although contract.md:43 says stdout only. Reproduction actually run through subprocess.run(capture_output=True):

```text
$ python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py --unknown-option
rc=2
stdout=''
stderr='mori-control-receipt.py: unknown option: --unknown-option\n'
```

Exploit/failure path: a stdout-only receipt collector sees no setup diagnostic after malformed argv; rc remains honestly 2, so this is lost evidence rather than false success. Smallest remediation: route setup/usage diagnostics to stdout and update the selftest's expected capture stream. No edit made.

## 2. Data touched — observed runtime

`command -v strace` returned `/usr/bin/strace`. Wrapper: create only own scratch directory, call the argv below with subprocess.run(capture_output=True, cwd=lane), read the trace for analysis, finally shutil.rmtree(own_scratch). `-e trace=openat,process,network` includes the assigned openat trace plus process/network evidence.

```text
$ strace -f -e trace=openat,process,network -o /fast/scratch/hyaku/mori-r79/Mo79N01Sentinel/trace.txt python3 -I /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py --dir /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence
rc=1
stderr=''
```

Full stdout (actual output, not an inferred expected result):

```text
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/census-end-r78.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/census-start-r78.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt sections=9 claims=10 bound=0 unbound=7
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt#1. the counter instrument absent from the entering tree claims=1 keys=cat_file_rc
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt#2. the tool in no ref, ever (log --all / rev-list --all --objects) claims=2 keys=log_all_lines,revlist_objects_named
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt#3. the canonical capabilities row absent at entering claims=2 keys=counter_win_mentions_in_SCORECARD,canonical_capability_headings_at_entering
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt#4. the D77-3 correction absent at entering claims=1 keys=correction_marker_in_LOG_at_entering
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt#5. S593 absent at entering claims=2 keys=S593_rows_in_SOURCES_at_entering,SOURCES_rows_at_entering
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt#7. the family table at entering (tolerant form, r77 lesson rule) claims=1 keys=family_rows_at_entering
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt#3b. precise row-form control (the 1 mention at entering is the Round-77 section C2 prose at SCORECARD.md:3892, not a capabilities-table row) claims=1 keys=row_form_counter_win_rows_at_entering
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/counter-win-live-r78.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/counter-win-selftest-r78.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/foreign-sweep-r78.txt sections=1 claims=0 bound=0 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/freshstart-spotchecks-r78.txt sections=4 claims=1 bound=0 unbound=1
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/freshstart-spotchecks-r78.txt#1. the frozen r61 counter at the r61 data tip claims=1 keys=counter_rc
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/frozen-audit-r78.txt sections=1 claims=0 bound=0 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/pin-family-r78-final.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/pin-family-r78-s593-isolated.txt sections=1 claims=1 bound=1 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/pin-family-r78.txt sections=2 claims=1 bound=1 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/post-landing-verify-r78.txt sections=5 claims=0 bound=0 unbound=0
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/s593-anchor-check-r78.txt sections=3 claims=2 bound=1 unbound=1
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/s593-anchor-check-r78.txt#B. able-to-fail arm (mislocation: wrong line + mutated count) claims=1 keys=abletofail_rc
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/selftests-battery-r78.txt sections=1 claims=12 bound=0 unbound=1
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/selftests-battery-r78.txt#(head) claims=12 keys=rc,rc,rc,rc,rc,rc,rc,rc,rc,rc,rc,rc
CONTROL_RECEIPT /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/source-s593-r78.txt sections=5 claims=8 bound=0 unbound=1
unbound /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/source-s593-r78.txt#1. duplicate sweep INTO this receipt BEFORE the fetch (the r69 lesson rule) claims=8 keys=hits_cimwin32prov,hits_wmisdk,hits_perfos_memory,hits_GlobalMemoryStatusEx,hits_PerfOS,hits_CommitLimit,S593_rows,SOURCES_rows_before
CONTROL_RECEIPT_SUMMARY files=15 sections=37 claims=40 unbound=11
```

Original trace SHA-256 `0fff4286f54c2bd6bc17b8a511ea15518a551b80fa33ea9f98553e53fdb4bbcc`. Full trace below replaces only the leading process number with `<process>` (avoids retaining unnecessary host process identifiers); addresses/argv abbreviation are strace's own. The trace contains one initial exec of Python launched by this audit wrapper, **no child created by the tool**, no network syscall, no writable open flag, no /tmp open. Interpreter startup reads its libraries, locale/config candidates, and Python packages; therefore a literal claim that the entire process opens *only* receipt files would be false. Application data reads are exactly the 15 direct sorted `.txt` files under the named evidence directory, plus its directory handle and the tool source. Programmatic comparison of trace receipt paths with sorted direct `glob('*.txt')` regular files printed `DIRECT_TXT_MATCH True COUNT 15`.

```text
<process> execve("/usr/bin/python3", ["python3", "-I", "/home/vgpnk/Projects/shokunin/mo"..., "--dir", "/home/vgpnk/Projects/shokunin/mo"...], 0x7ffc669722c8 /* 35 vars */) = 0
<process> openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/libpython3.14.so.1.0", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/libm.so.6", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/locale/locale-archive", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/gconv/gconv-modules.cache", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/proc/self/maps", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/pyvenv.cfg", O_RDONLY) = -1 ENOENT (No such file or directory)
<process> openat(AT_FDCWD, "/usr/bin/pyvenv.cfg", O_RDONLY) = -1 ENOENT (No such file or directory)
<process> openat(AT_FDCWD, "/usr/lib/libpython3.14.so.1.0._pth", O_RDONLY) = -1 ENOENT (No such file or directory)
<process> openat(AT_FDCWD, "/usr/bin/python3._pth", O_RDONLY) = -1 ENOENT (No such file or directory)
<process> openat(AT_FDCWD, "/usr/bin/python3.14._pth", O_RDONLY) = -1 ENOENT (No such file or directory)
<process> openat(AT_FDCWD, "/usr/bin/pybuilddir.txt", O_RDONLY) = -1 ENOENT (No such file or directory)
<process> openat(AT_FDCWD, "/etc/localtime", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/encodings/__pycache__/__init__.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/encodings/__init__.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/encodings", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/encodings/__pycache__/aliases.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/encodings/aliases.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/encodings/__pycache__/utf_8.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/encodings/utf_8.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/site-packages", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/site-packages/distutils-precedence.pth", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/encodings/__pycache__/utf_8_sig.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/encodings/utf_8_sig.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/lib-dynload", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/site-packages", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/site-packages/_distutils_hack/__pycache__/__init__.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/site-packages/_distutils_hack/__init__.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-control-receipt.py", O_RDONLY) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/re/__pycache__/__init__.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/re/__init__.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/__pycache__/enum.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/enum.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/__pycache__/types.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/types.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/re", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/re/__pycache__/_compiler.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/re/_compiler.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/re/__pycache__/_parser.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/re/_parser.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/re/__pycache__/_constants.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/re/_constants.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/re/__pycache__/_casefix.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/re/_casefix.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/__pycache__/functools.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/functools.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/collections/__pycache__/__init__.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/collections/__init__.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/__pycache__/keyword.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/keyword.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/__pycache__/operator.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/operator.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/__pycache__/reprlib.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/reprlib.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/__pycache__/copyreg.cpython-314.pyc", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/usr/lib/python3.14/copyreg.py", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence", O_RDONLY|O_NONBLOCK|O_CLOEXEC|O_DIRECTORY) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/census-end-r78.txt", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/census-start-r78.txt", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/controls-r78.txt", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/counter-win-live-r78.txt", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/counter-win-selftest-r78.txt", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/foreign-sweep-r78.txt", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/freshstart-spotchecks-r78.txt", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/frozen-audit-r78.txt", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/pin-family-r78-final.txt", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/pin-family-r78-s593-isolated.txt", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/pin-family-r78.txt", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/post-landing-verify-r78.txt", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/s593-anchor-check-r78.txt", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/selftests-battery-r78.txt", O_RDONLY|O_CLOEXEC) = 3
<process> openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-78/evidence/source-s593-r78.txt", O_RDONLY|O_CLOEXEC) = 3
<process> exit_group(1)                   = ?
<process> +++ exited with 1 +++
```

**Item 2: no finding for application-data scope on this live directory.** Arbitrary explicit input paths and symlinks were not exercised; the frozen contract does not impose containment on user-selected inputs. This does not certify hostile directory trees.

Scratch cleanup output: `SCRATCH_ABSENT True`. Trace was removed with the scratch directory. No fixture repos, installations or OS/unit changes.

## 3. Redaction — all available round text artifacts

Executed a Python analysis scan over every regular file under the absolute round-79 path using `Path.rglob('*')`, reading bytes once per file, UTF-8 decoding and excluding NUL/non-UTF-8 binaries. Snapshot manifest:

```text
88b256db9bf60770b808db6d19ed6508aa44319681194d1ea445bf491c032cf7  .ufo/waves/round-79/apply-c2.py (4815 bytes)
4cda8d4faf1d8680c45192f9b34e8eda608af910b8cde80b764a0680a5967fc4  .ufo/waves/round-79/build-w1-spec.py (27872 bytes)
56040b0d9cf7b957e2b745207c33e2e3b4792785659acee2d6578118327f0b5d  .ufo/waves/round-79/contract.md (6156 bytes)
4ba9498028adf2ec04c95d6f5fd7442719998c47d1996ca1c3bf3999b55bf7e8  .ufo/waves/round-79/count-c1.py (8801 bytes)
fed9a8292158b6d69e9d786d48fcbed02cb30772b5a5cb4e0386d0b034472290  .ufo/waves/round-79/count-c2.py (9453 bytes)
ab16bd3db5b3cf81f91775999f51b82b40b781acb0e53ec1cae1d48e483681f6  .ufo/waves/round-79/count-c3.py (8333 bytes)
bd5d0220b55f1432bf1012e7a8b8ab32de2e7955da499d495b4a1ce67576b6b8  .ufo/waves/round-79/evidence/census-start-r79.txt (4287 bytes)
5542861bdec4c60109375f52764d6ebe4a9a925242ebe03b696e5110abbb8851  .ufo/waves/round-79/evidence/controls-r79.txt (3752 bytes)
c9d55b14187717c31e3ab1ad9502f0f85af8615688a6304d033b5e965e0b5496  .ufo/waves/round-79/evidence/gen-after.sh (2586 bytes)
7241e1ca13d26470174a6214d5c453e54fca82fb39e996ca1c828d695139543e  .ufo/waves/round-79/evidence/gen-controls.sh (2150 bytes)
ee958db58653d3c8d63a059acfc33016413fe4a0c9d6cd44619630a22dfee198  .ufo/waves/round-79/evidence/source-rfc9111-r79.txt (22634 bytes)
4161ad1b83ecb3a36ed4f849f6f4245d749c8e5a7319cf92ab16e49e97bff409  .ufo/waves/round-79/w1/Mo79E02AxesCells-cells.md (3247 bytes)
7a06c66119e99cd1a4cba94652280cf01d26e351e5a8b4edeaf3ca16ab665901  .ufo/waves/round-79/w1/Mo79E02AxesCells.md (10608 bytes)
d6377ee9cd3d8bc98617d54434ea99124ebf9fa48db6c3ce3b59f02dd4bf1d27  .ufo/waves/round-79/w1/Mo79E03SourcePin.md (16666 bytes)
9e8ee39ac4bdd9f42d6812882a2d2b445a27413b40ba7f670fb3db3865a2c7cf  .ufo/waves/round-79/w1/Mo79M02MutantCounter.md (20586 bytes)
53ac408547664a46ca1478311f43d39ed20391cf876bde5c8d9fa219ac7fe5e9  .ufo/waves/round-79/w1/Mo79Sc01Recon.md (15594 bytes)
914718d0080093b7a2424676135eef0124af57731d745408ac2443bf669f5ff3  .ufo/waves/round-79/w1/swarm-registry.json (4218 bytes)
3745ac374750270a3d119e19a8e7f63589c61031091e130fc549cbc537ed990b  .ufo/waves/round-79/w1-dispatch.json (39025 bytes)
bc019df136524d109841f12061d37b148fda31d67d335602623e76ff3666b694  .ufo/waves/round-79/w1-spec.json (32321 bytes)
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  .ufo/waves/round-79/w1-validator.err (0 bytes)
141355486bba4dc32ea5f1790f7f8dfa459cbc3ae60df9e6002472e275c5ad7f  .ufo/waves/round-79/w1.ready (148 bytes)
0898da207e6e807fc8aaa4e9c6bf2fb471b483200d85a308db3ddd63574c191e  .ufo/waves/round-79/w1.ready.dispatched (487 bytes)
```

Output: `text_files=22 excluded_binaries=[]`. No content in excluded files was certified. Hostname tested against `socket.gethostname()` as an exact literal; user tested against `getpass.getuser()` with word boundaries after removing documented absolute root references. Neither value is reproduced. Absolute `/home/...` tokens were checked against the assignment's documented fleet/lane root and explicitly named rules path; no unrelated home path found. Documented roots are path evidence, not newly discovered host identity.

Credential/IP regex executed case-insensitively:

```text
password|token=|secret|BEGIN .*PRIVATE KEY|\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b
```

Actual hits: build-w1-spec.py:410, w1-dispatch.json:241, w1-spec.json:146 contain the requested scan pattern itself (password/token=/secret/private-key marker words). These are literal audit instructions, not credentials. Hostname hits 0; username outside documented roots 0; unrelated-home paths 0; IPv4-shaped hits 0. No credentials found by this bounded pattern scan; absence is not entropy analysis or proof no other credential format exists.

C3 source receipt `ee958db58653d3c8d63a059acfc33016413fe4a0c9d6cd44619630a22dfee198`: separate case-insensitive scan for `set-cookie|authorization:|cookie:` returned `[]`. Current retained headers are allowlisted status and content type (:93–98); public source fetching is the explicit C3 assignment, not network behavior of C1. Its author discloses transient earlier session-header retention in w1/Mo79E03SourcePin.md:99; current receipt is clean for those header patterns. Historical captured values were not accessed or reproduced, and deleting the block does not prove they never existed. No current leak finding is asserted from that disclosure alone.

RFC pin is **public-document bytes**, not private host/session material: 84477 bytes, sha256 `aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e`; inspected public IETF RFC 9111 header/title (:5–28) and §4.1 (:526–560). Author affiliations, protocol examples and public RFC content are not host-identity defects. This pin is outside the wave directory and was reviewed separately.

C2 candidate `4161ad1b83ecb3a36ed4f849f6f4245d749c8e5a7319cf92ab16e49e97bff409`: all 20 lines read; only a six-axis table and correction prose, no executable operations or host identifiers.

**Item 3: no current retained redaction finding** within the snapshotted text population. My report and later sibling artifacts are not present in this pre-write snapshot; parent must include them in its final retention check.

## 4. Boundary check

Checked C1's complete source/AST and traced runtime, all C2 cells text, C3 receipt, public RFC excerpt, and round text scans for dispatch/orchestration, OS/unit, serving-health and credential terms. C1 parses strings only; neither host remediation nor serving/model-health claims occur in the three deliverables. C3 receipt's broad source-row sweep quotes public AWS token semantics, not actual tokens; its own boundary scan for dispatch/orchestration/systemctl/model-serving/credential patterns returned `[]`. C2 changes attribution only.

Round administrative files **do contain orchestration metadata**: w1-dispatch.json schema at :2, build-w1-spec.py and w1-spec.json task descriptions, w1/swarm-registry.json:2–18 registry/member records, and ready/dispatched markers. These are pre-existing wave-administration records, not C1 running a dispatcher. I did not invoke or change them. Do not interpret this as "nothing anywhere in round-79 mentions dispatch."

**F2 — LOW, retained non-detection helper, not observed execution.** `.ufo/waves/round-79/apply-c2.py:110` contains `open(path, "w").write(text)` targeting SCORECARD.md (path formed at :66), default execution mutates unless `--check` (:102–103). File snapshot sha `88b256db9bf60770b808db6d19ed6508aa44319681194d1ea445bf491c032cf7`. Failure path: treating every round helper as a safe observation instrument and invoking this helper without --check rewrites the scorecard. Impact limited to supplied repo SCORECARD, not OS/unit/network. This is an integration script, **not** the C2 cells artifact nor the C1 instrument; no evidence it is registered or used as a detection probe, and I did not execute it. Smallest remediation: keep the mutation helper solely in integrator scratch/remove it from retained observational artifacts, or explicitly segregate it from instruments. No remediation performed. The C1/cells/pin deliverables themselves have no dispatch/OS/model-health/credential crossing finding.

## 5. Negative results, limits and own defects

1. Initial discovery found the tool absent; waited for its author rather than certifying nonexistent code. C2 and C3 authors supplied ready paths; reads and scans bind actual local bytes.
2. My first QUALITY read used physical lines 150–220, not criterion numbers 159 etc.; caught by the returned criterion headings and corrected with grep + physical lines 1644–1750.
3. My first traced invocation unnecessarily included `-B`, which could hide interpreter bytecode writes. Caught before reporting; repeated once without `-B` at the canonical `python3 -I` form. Reported runtime evidence uses only that exact-form trace. Both traces were removed with own scratch.
4. Own initial glob requested 250 and was clamped to 200; the later recursive scanner enumerated all actual regular files and did not rely on a truncated glob listing.
5. Scan snapshots are not atomic against sibling writes. The complete manifest makes the boundary explicit; no frozen counters, live-host remediation, offensive probes, credentials or resume_continuity_v1 surface were exercised (the latter is absent from this assigned surface). No selftest/closure verdict is claimed by me.
6. Self-evaluation: accuracy 4 (exact hashes/runtime; broader non-exercised inputs explicit), completeness 4 (all five assigned items, snapshot excludes later writes), clarity 4 (raw trace verbose but necessary), actionability 4 (two smallest remediations, no unauthorized edits), conciseness 3 (trace/startup reads dominate). Overall 3.8/5. Parent should run the final-wave retention check on integrated bytes; no further main-agent verification is represented as completed here.

## Post-report author notification (not independently rerun)

After this snapshot audit was submitted, Mo79E01ReceiptTool reported replacement tool SHA-256 `531d6b524635cccc57ef54712ed990899dfae36f2544143f6a1bbbd66c55f887`, stdout-only setup diagnostics, selftest 19/19 and empty stderr on its error/live battery. This is peer-reported evidence, not my executed verification. F1 above remains a proven defect of the earlier `b3b2f9e2...` bytes, not an assertion against the replacement. Parent should use the author's updated report and final-byte verification when determining closure. This report's runtime and retention claims remain explicitly pinned to the earlier snapshot.
