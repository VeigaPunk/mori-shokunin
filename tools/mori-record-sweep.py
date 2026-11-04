#!/usr/bin/env python3
"""Read-only record sweep (round 81, C2), Python 3 standard library only.

Usage: mori-record-sweep.py --root DIR [--pins FILE] [--carriers A[,B]] [--git DIR]
       mori-record-sweep.py --selftest | --help

Relative pins and carrier paths are root-relative. Default carriers are SCORECARD.md
and every binding's carrier. Explicit --carriers selects pending-arm carriers;
bindings always grade their named carriers. The summary counts all carriers read.
Pending is an exact trimmed cell-value test in Round sections, not prose intent.
Pinned rows use the first matching table row that states the key; repeated live
readings must agree. Commands are trusted read-only argv bindings, not shell text:
this tool does not sandbox them or certify their relevance or lack of side effects.
Exit 0 clean, 1 mismatches, 2 setup. Stdout only; no writes, sockets or temporary
files. Children are the pinned commands (cwd=ROOT) and read-only git commands.
Revision bindings require the first matching table row and the named revision's
blob to contain key=value; --git defaults to ROOT. Summary bindings counts both
binding lists; revisions counts mismatches (present when revisions is supplied).
Selftest is wholly in-memory and spawns no children. No repository imports.
"""

import argparse
import json
import re
import subprocess
from pathlib import Path

DEFAULT_PINS = '.ufo/waves/round-81/record-pins.json'
ROW = re.compile(r'^\s{0,3}\|')
ROUND = re.compile(r'^##\s+Round\b')


def pending_cells(text):
    """Return (line, cell index) for each exact PENDING table cell."""
    in_round = False
    found = []
    for number, line in enumerate(text.splitlines(), 1):
        if re.match(r'^#{1,2}\s', line):
            in_round = bool(ROUND.match(line))
            continue
        if in_round and ROW.match(line):
            cells = re.split(r'(?<!\\)\|', line.strip())[1:-1]
            found.extend((number, index) for index, cell in enumerate(cells)
                         if cell.strip() == 'PENDING')
    return found


def values(text, key):
    return {int(value) for value in re.findall(r'\b%s=(\d+)\b' % re.escape(key), text)}


def stated_value(text, row_contains, key):
    """Return the first row stating the key, or a useful missing-row location."""
    first = 1
    seen = False
    for number, line in enumerate(text.splitlines(), 1):
        if not ROW.match(line) or row_contains not in line:
            continue
        if not seen:
            first, seen = number, True
        match = re.search(r'\b%s=(\d+)\b' % re.escape(key), line)
        if match:
            return number, int(match[1])
    return first, None


def live_value(stdout, key):
    found = values(stdout, key)
    return next(iter(found)) if len(found) == 1 else None


def parse_pins(text):
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError('pins must be an object')
    if (data.get('schema') != 'mori-record-pins-v1'
            and not ('revisions' in data and 'schema' not in data)):
        raise ValueError('pins schema must be mori-record-pins-v1')
    bindings = data.get('bindings', [])
    if not isinstance(bindings, list):
        raise ValueError('bindings must be a list')
    for binding in bindings:
        if not isinstance(binding, dict):
            raise ValueError('binding must be an object')
        if any(not isinstance(binding.get(key), str) or not binding[key].strip()
               for key in ('carrier', 'row_contains', 'key')):
            raise ValueError('binding needs nonempty carrier, row_contains and key')
        command = binding.get('command')
        if (not isinstance(command, list) or not command
                or not all(isinstance(arg, str) and '\0' not in arg for arg in command)
                or not command[0]):
            raise ValueError('binding command must be a nonempty argv list')
    return bindings


def parse_revisions(text):
    data = json.loads(text)
    revisions = data.get('revisions', [])
    if not isinstance(revisions, list):
        raise ValueError('revisions must be a list')
    for binding in revisions:
        if not isinstance(binding, dict):
            raise ValueError('revision binding must be an object')
        if any(not isinstance(binding.get(key), str) or not binding[key].strip()
               or '\0' in binding[key]
               for key in ('carrier', 'row_contains', 'key', 'rev', 'path')):
            raise ValueError('revision binding needs nonempty carrier, row_contains, key, rev and path')
        if type(binding.get('value')) is not int or binding['value'] < 0:
            raise ValueError('revision binding value must be a nonnegative integer')
    return revisions


def contains_value(text, key, value):
    """Match the exact numeric token, not a prefix of a larger identifier/value."""
    token = '%s=%d' % (key, value)
    return re.search(r'(?<![\w.-])%s(?![\w.-])' % re.escape(token), text) is not None


def revision_sweep(texts, bindings, git_reader):
    """Grade each binding in order, reporting its first failed requirement."""
    findings = []
    for binding in bindings:
        carrier = binding['carrier']
        number, row = 1, ''
        for line, text in enumerate(texts[carrier].splitlines(), 1):
            if ROW.match(text) and binding['row_contains'] in text:
                number, row = line, text
                break
        if not row or not contains_value(row, binding['key'], binding['value']):
            detail = 'row-value'
        else:
            rc, commit = git_reader(['rev-parse', '--verify', '--end-of-options',
                                     binding['rev'] + '^{commit}'])
            if rc != 0:
                detail = 'rev-unresolvable'
            else:
                rc, blob = git_reader(['show', commit.strip() + ':' + binding['path']])
                if rc != 0:
                    detail = 'path-absent'
                elif not contains_value(blob, binding['key'], binding['value']):
                    detail = 'rev-bytes'
                else:
                    continue
        findings.append(('revision', carrier, number, detail))
    return findings


def lane_path(root, name):
    path = (root / name).resolve()
    if Path(name).is_absolute() or not path.is_relative_to(root):
        raise ValueError('carrier outside root: ' + name)
    return path


def run_command(command, root):
    try:
        result = subprocess.run(command, cwd=root, capture_output=True,
                                text=True, encoding='utf-8', errors='replace')
        return result.returncode, result.stdout
    except OSError:
        # A missing executable is pinned-command failure, not a clean record.
        return 127, ''


def sweep(texts, carriers, bindings, runner):
    """Pure grading core; runner returns (exit status, stdout)."""
    findings = []
    for carrier in carriers:
        for line, index in pending_cells(texts[carrier]):
            findings.append(('pending', carrier, line, 'cell=%d value=PENDING' % index))
    for binding in bindings:
        carrier, key = binding['carrier'], binding['key']
        line, stated = stated_value(texts[carrier], binding['row_contains'], key)
        rc, stdout = runner(binding['command'])
        live = live_value(stdout, key)
        if stated is None or live is None or rc != 0 or stated != live:
            findings.append(('pinned', carrier, line,
                             '%s stated=%s live=%s command_rc=%d' %
                             (key, stated if stated is not None else 'missing',
                              live if live is not None else 'missing-or-conflicting', rc)))
    return findings


def emit(findings, carriers, bindings, include_revisions=False):
    for arm, carrier, line, detail in findings:
        if arm == 'revision':
            print('REVISION_MISMATCH %s:%d %s' % (carrier, line, detail))
        else:
            print('RECORD_SWEEP_MISMATCH %s %s:%d %s' % (arm, carrier, line, detail))
    pending = sum(item[0] == 'pending' for item in findings)
    pinned = sum(item[0] == 'pinned' for item in findings)
    summary = 'RECORD_SWEEP pending=%d pinned=%d carriers=%d bindings=%d' % (
        pending, pinned, carriers, bindings)
    if include_revisions:
        summary += ' revisions=%d' % sum(item[0] == 'revision' for item in findings)
    print(summary)
    return int(bool(findings))


def selftest():
    passed = failed = 0

    def check(name, ok):
        nonlocal passed, failed
        passed += int(bool(ok))
        failed += int(not ok)
        print('case %s %s' % (name, 'pass' if ok else 'FAIL'))

    def bad_pins(data):
        try:
            parse_pins(data)
        except (ValueError, TypeError):
            return True
        return False

    check('pending-in-round', pending_cells('## Round 8\n| a | PENDING |') == [(2, 1)])
    check('pending-outside-round', not pending_cells('## Notes\n| a | PENDING |'))
    check('pending-prose', not pending_cells('## Round 8\nPENDING after measurements'))
    check('pending-trimmed', len(pending_cells('## Round 8\n| a |  PENDING  |')) == 1)
    check('pending-exact', not pending_cells('## Round 8\n| a | `PENDING` | pending | PENDING soon |'))
    check('round-end', not pending_cells('## Round 8\n## Notes\n| PENDING |'))
    check('round-subsection', len(pending_cells('## Round 8\n### Results\n| PENDING |')) == 1)
    check('escaped-pipe', pending_cells('## Round 8\n| a \\| b | PENDING |') == [(2, 1)])
    check('first-stating-row', stated_value('| tool |\n| tool n=4 |\n| tool n=9 |', 'tool', 'n') == (2, 4))
    check('missing-stated', stated_value('| tool absent |', 'tool', 'n') == (1, None))
    check('live-single', live_value('n=4', 'n') == 4)
    check('live-repeated-agreement', live_value('n=4\nn=4', 'n') == 4)
    check('live-conflict', live_value('n=4\nn=5', 'n') is None)
    check('live-absent', live_value('other=4', 'n') is None)
    check('malformed-json', bad_pins('{'))
    check('malformed-schema', bad_pins('{"schema":"wrong","bindings":[]}'))
    check('malformed-bindings', bad_pins('{"schema":"mori-record-pins-v1","bindings":{}}'))
    binding = dict(carrier='SCORECARD.md', row_contains='tool', key='n', command=['missing-tool'])
    check('valid-pins', parse_pins(json.dumps(dict(schema='mori-record-pins-v1', bindings=[binding]))) == [binding])
    malformed = dict(binding, command='shell text')
    check('command-not-shell', bad_pins(json.dumps(dict(schema='mori-record-pins-v1', bindings=[malformed]))))
    texts = {'SCORECARD.md': '## Round 8\n| tool n=4 | met |'}
    clean = sweep(texts, ['SCORECARD.md'], [binding], lambda command: (0, 'n=4'))
    check('clean-totals', not clean)
    dirty = sweep({'SCORECARD.md': '## Round 8\n| tool n=3 | PENDING |'},
                  ['SCORECARD.md'], [binding], lambda command: (0, 'n=4'))
    check('dirty-totals', [item[0] for item in dirty] == ['pending', 'pinned'])
    for name, result in [('tool-absent', (127, '')), ('failed-command', (1, 'n=4')),
                         ('missing-live', (0, '')), ('conflicting-live', (0, 'n=4 n=5'))]:
        found = sweep(texts, ['SCORECARD.md'], [binding], lambda command: result)
        check(name, len(found) == 1 and found[0][0] == 'pinned')
    missing = sweep({'SCORECARD.md': '| tool missing |'}, ['SCORECARD.md'], [binding],
                    lambda command: (0, 'n=4'))
    check('missing-stated-mismatch', len(missing) == 1 and missing[0][0] == 'pinned')
    revision = dict(carrier='SCORECARD.md', row_contains='tool', key='pointers',
                    value=240, rev='A', path='SCORECARD.md')

    def revision_case(rows, revisions, resolved=True, present=True, blob='pointers=240'):
        calls = []

        def git_reader(command):
            calls.append(command)
            if command[0] == 'rev-parse':
                return (0, 'commit-a\n') if resolved else (1, '')
            return (0, blob) if present else (1, '')

        found = revision_sweep({'SCORECARD.md': rows}, revisions, git_reader)
        return found, calls

    row = '| tool pointers=240 |'
    found, calls = revision_case(row, [revision])
    check('revision-conformant', not found and calls == [
        ['rev-parse', '--verify', '--end-of-options', 'A^{commit}'],
        ['show', 'commit-a:SCORECARD.md']])
    found, _ = revision_case(row, [revision], blob='pointers=237')
    check('revision-D81-1', found == [('revision', 'SCORECARD.md', 1, 'rev-bytes')])
    found, calls = revision_case(row, [revision], resolved=False)
    check('revision-unresolvable', found == [
        ('revision', 'SCORECARD.md', 1, 'rev-unresolvable')] and len(calls) == 1)
    found, _ = revision_case(row, [revision], present=False)
    check('revision-path-absent', found == [('revision', 'SCORECARD.md', 1, 'path-absent')])
    found, calls = revision_case('| other pointers=240 |', [revision])
    check('revision-missing-row', found == [
        ('revision', 'SCORECARD.md', 1, 'row-value')] and not calls)
    second = dict(revision, row_contains='second', value=237)
    found, _ = revision_case(row + '\n| second pointers=237 |', [revision, second])
    check('revision-second-stale', found == [('revision', 'SCORECARD.md', 2, 'rev-bytes')])
    found, calls = revision_case('| tool |\n' + row, [revision])
    check('revision-first-row', found == [
        ('revision', 'SCORECARD.md', 1, 'row-value')] and not calls)
    found, calls = revision_case('| tool pointers=237 |', [revision], resolved=False)
    check('revision-row-before-git', found == [
        ('revision', 'SCORECARD.md', 1, 'row-value')] and not calls)
    check('revision-token-boundaries', contains_value('`pointers=240`', 'pointers', 240)
          and not any(contains_value(text, 'pointers', 240) for text in (
              'other-pointers=240', 'pointers=2400', 'pointers=240.5', 'pointers=240e2')))
    revision_json = json.dumps({'revisions': [revision]})
    check('revision-only-pins', parse_pins(revision_json) == []
          and parse_revisions(revision_json) == [revision])
    print('RECORD_SWEEP_SELFTEST pass=%d fail=%d' % (passed, failed))
    return int(bool(failed))


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--root')
    parser.add_argument('--pins')
    parser.add_argument('--carriers')
    parser.add_argument('--git')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    try:
        if not args.root:
            raise ValueError('--root is required')
        root = Path(args.root).resolve()
        if not root.is_dir():
            raise ValueError('root must be an existing directory')
        pins = Path(args.pins) if args.pins else Path(DEFAULT_PINS)
        if not pins.is_absolute():
            pins = root / pins
        pins_text = pins.read_text(encoding='utf-8')
        bindings = parse_pins(pins_text)
        revisions = parse_revisions(pins_text)
        all_bindings = bindings + revisions
        carriers = args.carriers.split(',') if args.carriers is not None else [
            'SCORECARD.md', *(binding['carrier'] for binding in all_bindings)]
        if any(not carrier.strip() for carrier in carriers):
            raise ValueError('--carriers needs nonempty paths')
        carriers = list(dict.fromkeys(carriers))
        names = list(dict.fromkeys(carriers + [binding['carrier'] for binding in all_bindings]))
        texts = {name: lane_path(root, name).read_text(encoding='utf-8') for name in names}
        findings = sweep(texts, carriers, bindings, lambda command: run_command(command, root))
        git = Path(args.git).resolve() if args.git else root
        findings.extend(revision_sweep(texts, revisions,
                                      lambda command: run_command(['git', '-C', str(git),
                                                                   *command], root)))
        return emit(findings, len(names), len(all_bindings),
                    include_revisions='revisions' in json.loads(pins_text))
    except (OSError, ValueError) as exc:
        print('RECORD_SWEEP_SETUP ' + str(exc).replace('\n', ' '))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
