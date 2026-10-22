#!/usr/bin/env python3
"""Round-31 C2 counter (frozen before data; contract .ufo/waves/round-31/contract.md, C2).

usage: count-c2.py <lane-rev> [--tool-file <path>] [--repo <lane-repo>]

Predicate P-C2 (same sentence as the contract): C2=met iff tools/mori-blind-check.sh exists at <lane-rev>, and run on
the 16 frozen fixtures of .ufo/waves/round-31/c2-fixtures.json (committed under random brief names in a /tmp
sandbox repo) it prints scanned=16, blind_violations equal to its hit-line count, exit 1, and for every fixture
exactly the expected set of (line, rule) hits (exact=16/16).

--tool-file scores a candidate script file instead of the tool blob at <lane-rev> (used only for the committed
control receipts); the fixtures are always read from <lane-rev> and checked against the frozen sha256 below.
Exit 0 met, 1 unmet, 2 bad revision, tampered fixtures or sandbox error.
"""
import hashlib, json, os, random, shutil, string, subprocess, sys, tempfile

FIXTURES = '.ufo/waves/round-31/c2-fixtures.json'
FIXTURES_SHA256 = '1442c14e963bf77df34774015dff7ee73a9738d49b3911d26b4e3b96f48e0b31'
TOOL = 'tools/mori-blind-check.sh'
LANE = '/home/vgpnk/Projects/shokunin/mori-shokunin'
CLEAN_ENV = {k: v for k, v in os.environ.items() if k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}


def die(msg):
    print(f'count-c2: {msg}')
    print('C2=error')
    sys.exit(2)


def git(repo, *args, data=None):
    return subprocess.run(['git', '-C', repo, *args], capture_output=True, env=CLEAN_ENV, input=data)


def main(argv):
    repo, tool_file, rev = LANE, None, None
    it = iter(argv)
    for a in it:
        if a == '--tool-file':
            tool_file = next(it, None)
        elif a == '--repo':
            repo = next(it, None)
        elif rev is None:
            rev = a
        else:
            die('usage: count-c2.py <lane-rev> [--tool-file <path>] [--repo <lane-repo>]')
    if not rev or not repo:
        die('usage: count-c2.py <lane-rev> [--tool-file <path>] [--repo <lane-repo>]')
    r = git(repo, 'rev-parse', '--verify', '--quiet', '--end-of-options', rev + '^{commit}')
    if r.returncode:
        die('invalid lane revision')
    full = r.stdout.decode().strip()
    print(f'rev={full}')
    fx = git(repo, 'show', f'{full}:{FIXTURES}')
    if fx.returncode:
        die('fixtures absent at revision')
    if hashlib.sha256(fx.stdout).hexdigest() != FIXTURES_SHA256:
        die('fixtures differ from the frozen sha256')
    doc = json.loads(fx.stdout)
    if tool_file:
        tool_bytes = open(tool_file, 'rb').read()
        print(f'tool=file:{tool_file} sha256={hashlib.sha256(tool_bytes).hexdigest()}')
    else:
        t = git(repo, 'show', f'{full}:{TOOL}')
        if t.returncode:
            print('tool=absent')
            print('fixtures=16 exact=0/16')
            print('C2=unmet')
            return 1
        tool_bytes = t.stdout
        print(f'tool=present blob_sha256={hashlib.sha256(tool_bytes).hexdigest()}')

    tmp = tempfile.mkdtemp(prefix='mori-r31-c2.')
    try:
        sb = os.path.join(tmp, 'repo')
        os.makedirs(os.path.join(sb, doc['wave_dir'], 'sub'))
        if git(sb, 'init', '-q').returncode:
            die('sandbox git init failed')
        rnd = random.SystemRandom()
        used, by_name = set(), {}
        for f in doc['fixtures']:
            while True:
                name = 'Case' + ''.join(rnd.choice(string.ascii_letters + string.digits) for _ in range(6))
                if name not in used and name != 'CaseOther' and name != 'CaseNested':
                    break
            used.add(name)
            by_name[name] = f
            text = '\n'.join(f['lines']).replace(doc['placeholder'], name) + '\n'
            with open(os.path.join(sb, doc['wave_dir'], name + '.md'), 'w') as h:
                h.write(text)
        for u in doc['unscanned']:
            with open(os.path.join(sb, doc['wave_dir'], u['name']), 'w') as h:
                h.write('\n'.join(u['lines']) + '\n')
        tool_path = os.path.join(tmp, 'tool.sh')
        with open(tool_path, 'wb') as h:
            h.write(tool_bytes)
        allow_path = os.path.join(tmp, 'allow.txt')
        with open(allow_path, 'w') as h:
            h.write('\n'.join(doc['allow']) + '\n')
        if git(sb, 'add', '-A').returncode or git(sb, '-c', 'user.name=C2Counter', '-c', 'user.email=c2@example.invalid',
                                                     'commit', '-q', '-m', 'fixtures').returncode:
            die('sandbox commit failed')
        srev = git(sb, 'rev-parse', 'HEAD').stdout.decode().strip()
        try:
            run = subprocess.run(['timeout', '120', 'bash', tool_path, srev, doc['wave_dir'], doc['writer_regex'], allow_path],
                                 cwd=sb, capture_output=True, env=CLEAN_ENV)
        except OSError as e:
            die(f'tool run failed: {e}')
        out = run.stdout.decode(errors='replace').splitlines()
        print(f'tool_exit={run.returncode}')
        scanned = next((l.split('=', 1)[1] for l in out if l.startswith('scanned=')), None)
        violations = next((l.split('=', 1)[1] for l in out if l.startswith('blind_violations=')), None)
        hits = [l for l in out if not l.startswith('scanned=') and not l.startswith('blind_violations=') and l.strip()]
        got = {n: set() for n in by_name}
        stray = []
        for h in hits:
            parts = h.rsplit(':', 2)
            if len(parts) != 3 or not parts[1].isdigit():
                stray.append(h)
                continue
            base = os.path.basename(parts[0])
            name = base[:-3] if base.endswith('.md') else base
            if name in got and os.path.dirname(parts[0]) == doc['wave_dir']:
                got[name].add((int(parts[1]), parts[2]))
            else:
                stray.append(h)
        exact = 0
        for name, f in sorted(by_name.items(), key=lambda kv: kv[1]['id']):
            want = {(a, b) for a, b in f['expect']}
            if got[name] == want:
                exact += 1
                print(f"{f['id']} exact hits={len(want)}")
            else:
                print(f"{f['id']} diff want={sorted(want)} got={sorted(got[name])}")
        n = len(doc['fixtures'])
        expected_exit = 1 if any(f['expect'] for f in doc['fixtures']) else 0
        scanned_ok = scanned == str(n)
        count_ok = violations is not None and violations.isdigit() and int(violations) == len(hits)
        exit_ok = run.returncode == expected_exit
        print(f'scanned={scanned} scanned_ok={"yes" if scanned_ok else "no"} blind_violations={violations} '
              f'hit_lines={len(hits)} count_ok={"yes" if count_ok else "no"} exit_ok={"yes" if exit_ok else "no"} stray={len(stray)}')
        for s in stray:
            print(f'stray {s}')
        print(f'fixtures={n} exact={exact}/{n}')
        met = exact == n and scanned_ok and count_ok and exit_ok and not stray
        print('C2=met' if met else 'C2=unmet')
        return 0 if met else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
