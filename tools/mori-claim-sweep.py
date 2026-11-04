#!/usr/bin/env python3
"""Read-only self-assessment sweep (round 80, C1).

Usage: mori-claim-sweep.py --root DIR [--pins FILE] [--carriers A[,B]]
       mori-claim-sweep.py --selftest | --help

Pins default to ROOT/.ufo/waves/round-80/claim-pins.json, with schema
mori-claim-pins-v1, tallies {"tools/name.py": integer}, stale_literals [string].
Relative pins are root-relative. Carriers are root-relative, defaulting to
SCORECARD.md,SKILL.md,SHONEN.md,LOG.md. Only selected carriers are graded.
The Axes table and capability tables (identified by their column headers) in
SCORECARD.md and checklist lines in SHONEN.md supply lane pointers. Embedded
command tokens are supported; sibling/absolute paths are not lane pointers.
Line/revision suffixes identify current paths, not historical blob checks.
Patterns containing * or ? resolve when at least one existing path matches;
this does not prove that matched files are the intended evidence.
Stale literals are checked everywhere in carriers, including fenced examples.

Exit: 0 clean, 1 mismatches, 2 setup. All output goes to stdout. No file
writes, sockets or temporary files; only pinned selftests are spawned. Python
children use -I; shell children use bash. Child environment (including TMPDIR)
is inherited, and their working directory is ROOT.
"""

import glob
import io
import json
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_CARRIERS = ('SCORECARD.md', 'SKILL.md', 'SHONEN.md', 'LOG.md')
DEFAULT_PINS = '.ufo/waves/round-80/claim-pins.json'
POINTER = re.compile(r'(?<![\w./-])(?:corpus|tools|\.ufo)/[^\s`,;|)\]}]+')


def lane_path(root, name):
    path = (root / name).resolve()
    if Path(name).is_absolute() or not path.is_relative_to(root):
        raise ValueError('path outside root: ' + name)
    return path


def visible_lines(text):
    """Yield original line numbers outside CommonMark-style fenced blocks."""
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', line)
        if fence:
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
            continue
        if marker:
            fence = marker[1]
            continue
        yield number, line


def graded_rows(carrier, text):
    axes = False
    table = False
    capability = False
    for number, line in visible_lines(text):
        if carrier == 'SHONEN.md':
            if re.match(r'^\s*- \[', line):
                yield number, line
            continue
        if carrier != 'SCORECARD.md':
            continue
        heading = re.match(r'^(#{1,6})\s+(.+?)\s*#*$', line)
        if heading:
            axes = heading[1] == '##' and heading[2].casefold() == 'axes'
            table = capability = False
        if not line.lstrip().startswith('|'):
            table = capability = False
            continue
        cells = [cell.strip().casefold() for cell in re.split(r'(?<!\\)\|', line.strip())[1:-1]]
        if not table:
            table = True
            capability = ('what it can now do' in cells and
                          any(cell in cells for cell in ('capability', 'name', 'key')))
            continue
        if all(re.fullmatch(r':?-+:?', cell) for cell in cells):
            continue
        if axes or capability:
            yield number, line


def pointers(line):
    for token in re.findall(r'`+([^`]+)`+', line):
        for match in POINTER.finditer(token):
            name = match[0]
            # Accept either ordering of the two independently optional suffixes.
            for _ in range(2):
                name = re.sub(r'(?::\d+(?:-\d+)?|@[0-9a-fA-F]+)$', '', name)
            if '..' not in Path(name).parts:
                yield name


def parse_count(text):
    """Parse only the frozen success grammars; explicit failures always win."""
    if any(int(value) != 0 for value in re.findall(r'\bfail=(\d+)\b', text)):
        raise ValueError('selftest reports nonzero fail')
    counts = []
    for line in text.splitlines():
        match = re.search(r'\bpass=(\d+)\b', line)
        if match:
            counts.append(int(match[1]))
        match = re.search(r'\bPASS \((\d+) cases\)', line)
        if match:
            counts.append(int(match[1]))
        match = re.search(r'\bPASS (\d+)/(\d+)\b', line)
        if match:
            if match[1] != match[2]:
                raise ValueError('selftest PASS numerator differs from denominator')
            counts.append(int(match[1]))
    if not counts or len(set(counts)) != 1:
        raise ValueError('unparseable or conflicting selftest counts')
    return counts[0]


def run_tool(path, root):
    if path.suffix == '.py':
        command = [sys.executable, '-I', str(path), '--selftest']
    elif path.suffix == '.sh':
        command = ['bash', str(path), '--selftest']
    else:
        raise ValueError('pinned tool must be .py or .sh: ' + str(path))
    result = subprocess.run(command, cwd=root, capture_output=True, text=True)
    if result.returncode:
        raise ValueError('selftest failed: %s rc=%d' % (path.name, result.returncode))
    return parse_count(result.stdout)


def sweep(root, pins_name, carriers, out, read_text=None, exists=None, runner=None, glob_paths=None):
    """Injected I/O permits complete in-memory fixtures without filesystem writes."""
    read_text = read_text or (lambda path: path.read_text(encoding='utf-8'))
    exists = exists or (lambda path: path.exists())
    runner = runner or run_tool
    glob_paths = glob_paths or glob.glob
    try:
        pins_path = Path(pins_name)
        if not pins_path.is_absolute():
            pins_path = lane_path(root, pins_name)
        pins = json.loads(read_text(pins_path))
        if not isinstance(pins, dict) or pins.get('schema') != 'mori-claim-pins-v1':
            raise ValueError('pins schema must be mori-claim-pins-v1')
        tallies = pins.get('tallies', {})
        literals = pins.get('stale_literals', [])
        if not isinstance(tallies, dict) or any(
                not isinstance(name, str) or type(count) is not int or count < 0
                for name, count in tallies.items()):
            raise ValueError('tallies must map tool paths to nonnegative integers')
        if not isinstance(literals, list) or any(not isinstance(s, str) or not s for s in literals):
            raise ValueError('stale_literals must be nonempty strings')
        mismatches = []
        pointer_count = 0
        for carrier in carriers:
            text = read_text(lane_path(root, carrier))
            for number, line in graded_rows(carrier, text):
                for name in pointers(line):
                    pointer_count += 1
                    path = lane_path(root, name)
                    if '*' in name or '?' in name:
                        matches = (Path(match) for match in glob_paths(str(path)))
                        resolved = any(
                            match.is_relative_to(root) and exists(match) and
                            not any(part.is_symlink() for part in (match, *match.parents))
                            for match in matches)
                    else:
                        resolved = exists(path)
                    if not resolved:
                        mismatches.append(('unresolved', carrier, number, name))
            for number, line in enumerate(text.splitlines(), 1):
                for literal in literals:
                    for _ in range(line.count(literal)):
                        mismatches.append(('stale', carrier, number, repr(literal)))
        for name, expected in tallies.items():
            if not name.startswith('tools/'):
                raise ValueError('pinned tally is not a lane tool: ' + name)
            path = lane_path(root, name)
            if not exists(path):
                raise ValueError('missing pinned tool: ' + name)
            actual = runner(path, root)
            if actual != expected:
                mismatches.append(('tally', str(pins_path), 1,
                                   '%s pinned=%d live=%d' % (name, expected, actual)))
    except (OSError, ValueError, UnicodeError, subprocess.SubprocessError) as exc:
        print('CLAIM_SWEEP_SETUP ' + str(exc).replace('\n', ' '), file=out)
        return 2
    order = {name: index for index, name in enumerate(carriers)}
    mismatches.sort(key=lambda row: (order.get(row[1], len(order)), row[2], row[0], row[3]))
    for kind, carrier, number, detail in mismatches:
        print('CLAIM_SWEEP_MISMATCH %s %s:%d %s' % (kind, carrier, number, detail), file=out)
    counts = {kind: sum(row[0] == kind for row in mismatches)
              for kind in ('unresolved', 'tally', 'stale')}
    print('CLAIM_SWEEP mismatches=%d unresolved=%d tallies=%d stale=%d carriers=%d pointers=%d'
          % (len(mismatches), counts['unresolved'], counts['tally'], counts['stale'],
             len(carriers), pointer_count), file=out)
    return int(bool(mismatches))


def selftest(out):
    import fnmatch
    root = Path('/claim-sweep-in-memory')
    header = '## Axes\n\n| Axis | Score | Evidence | Last change |\n|---|---|---|---|\n'
    pins = {'schema': 'mori-claim-pins-v1', 'tallies': {'tools/live.py': 19},
            'stale_literals': ['selftest 18 in-memory cases']}
    passed = failed = 0

    def check(name, body='', rc=0, contains=None, live=19, missing=None, pin=None, carrier='SCORECARD.md'):
        nonlocal passed, failed
        files = {root / DEFAULT_PINS: json.dumps(pins if pin is None else pin),
                 root / carrier: body}
        def read_fixture(path):
            if path == missing or path not in files:
                raise OSError('fixture unreadable: ' + str(path))
            return files[path]
        result = io.StringIO()
        present = (root / 'tools/live.py', root / 'corpus/live.md')
        actual = sweep(root, DEFAULT_PINS, [carrier], result, read_fixture,
                       lambda path: path in present,
                       lambda path, cwd: live,
                       lambda pattern: [str(path) for path in present
                                        if fnmatch.fnmatchcase(str(path), pattern)])
        ok = actual == rc and (contains is None or contains in result.getvalue())
        passed += int(ok)
        failed += int(not ok)
        print('case %s %s' % (name, 'pass' if ok else 'FAIL ' + result.getvalue().strip()), file=out)

    check('clean fixture tree', header + '| coverage | 6 | `corpus/live.md` | now |', contains='pointers=1')
    check('stale present', header + '| x | 1 | selftest 18 in-memory cases | now |', 1, 'stale=1')
    check('stale absent', header, contains='stale=0')
    check('tally equal', header, contains='tallies=0')
    check('tally mismatch', header, 1, 'pinned=19 live=20', live=20)
    check('dead pointer', header + '| x | 1 | `corpus/dead.md` | now |', 1, 'unresolved=1')
    check('live line suffix', header + '| x | 1 | `corpus/live.md:12-14` | now |', contains='pointers=1')
    check('live revision suffix', header + '| x | 1 | `corpus/live.md@abcdef1` | now |', contains='pointers=1')
    check('fenced token ignored', '```md\n' + header + '| x | 1 | `corpus/dead.md` | now |\n```', contains='pointers=0')
    check('sibling ignored', header + '| x | 1 | `../sibling/tools/dead.py` | now |', contains='pointers=0')
    check('unreadable carrier', header, 2, missing=root / 'SCORECARD.md')
    check('missing pins', header, 2, missing=root / DEFAULT_PINS)
    check('malformed pins', header, 2, pin={'schema': 'wrong'})
    check('capability table', '| Capability | What it can now do | Evidence | First-working round |\n|---|---|---|---|\n| x | read | `tools/dead.py` | 80 |', 1, 'unresolved=1')
    check('checklist command', '- [~] runnable `python tools/live.py --selftest`', contains='pointers=1', carrier='SHONEN.md')
    check('ungraded prose ignored', '`corpus/dead.md`', contains='pointers=0')
    check('multiple stale occurrences', 'selftest 18 in-memory cases; selftest 18 in-memory cases', 1, 'stale=2')
    check('wildcard existing match', header + '| x | 1 | `corpus/li?e*.md` | now |', contains='unresolved=0')
    check('wildcard no match', header + '| x | 1 | `corpus/dead*.md` | now |', 1, 'unresolved=1')
    check('stale-only total', 'selftest 18 in-memory cases', 1,
          'CLAIM_SWEEP mismatches=1 unresolved=0 tallies=0 stale=1 carriers=1 pointers=0\n')
    check('tally-only total', header, 1,
          'CLAIM_SWEEP mismatches=1 unresolved=0 tallies=1 stale=0 carriers=1 pointers=0\n', live=20)
    check('combined total', header + '| x | 1 | `corpus/dead.md` selftest 18 in-memory cases | now |', 1,
          'CLAIM_SWEEP mismatches=2 unresolved=1 tallies=0 stale=1 carriers=1 pointers=1\n')
    for text, expected in [('pass=19 fail=0', 19), ('PASS (12 cases)', 12),
                           ('PASS 7/7', 7), ('pass=3', 3), ('pass=3 fail=1', None),
                           ('PASS 2/3', None), ('nothing', None), ('pass=3\npass=4', None)]:
        try:
            actual = parse_count(text)
        except ValueError:
            actual = None
        ok = actual == expected
        passed += int(ok)
        failed += int(not ok)
        print('case grammar %r %s' % (text, 'pass' if ok else 'FAIL'), file=out)
    print('CLAIM_SWEEP_SELFTEST pass=%d fail=%d' % (passed, failed), file=out)
    return int(bool(failed))


def main(argv):
    options = {}
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg in ('--help', '-h'):
            print(__doc__)
            return 0
        if arg == '--selftest':
            return selftest(sys.stdout)
        key, sep, value = arg.partition('=')
        if key not in ('--root', '--pins', '--carriers'):
            print('CLAIM_SWEEP_SETUP unknown option: ' + arg)
            return 2
        if not sep:
            index += 1
            if index == len(argv):
                print('CLAIM_SWEEP_SETUP missing value: ' + key)
                return 2
            value = argv[index]
        if not value:
            print('CLAIM_SWEEP_SETUP empty value: ' + key)
            return 2
        options[key] = value
        index += 1
    if '--root' not in options:
        print('CLAIM_SWEEP_SETUP --root is required')
        return 2
    root = Path(options['--root']).resolve()
    if not root.is_dir():
        print('CLAIM_SWEEP_SETUP root is not a directory: ' + str(root))
        return 2
    carriers = options.get('--carriers', ','.join(DEFAULT_CARRIERS)).split(',')
    if any(not carrier for carrier in carriers):
        print('CLAIM_SWEEP_SETUP empty carrier')
        return 2
    return sweep(root, options.get('--pins', DEFAULT_PINS), carriers, sys.stdout)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
