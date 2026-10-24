#!/usr/bin/env python3
"""Round-31 C2 counter, amendment A1 (tightened before any round-31 tool was scored; contract "Amendment A1").

usage: count-c2-a1.py <lane-rev> [--tool-file <path>] [--repo <lane-repo>]

Predicate P-C2-A1 (same sentence as the contract): C2=met iff tools/mori-blind-check.sh exists at <lane-rev> and its
bytes contain none of c2-fixtures, count-c2 and fixtures-a1; and in each of two runs, isolated with bwrap so that
/home and /fast are hidden and the environment holds only PATH, on the 16 frozen fixtures plus the 11 A1 fixtures,
written under random names in random order with random mtimes and a random nonce comment line appended to each brief,
it prints scanned=27, blind_violations equal to its hit-line count with no duplicate hit line, exit 1, no hit line
outside the 27 briefs, and exactly the expected set of (line, rule) hits for every brief (exact=27/27).

The original P-C2 (count-c2.py) is kept and reported beside this one. Exit 0 met, 1 unmet, 2 bad revision, tampered
fixtures or sandbox error.
"""
import hashlib, json, os, random, shutil, string, subprocess, sys, tempfile

FIXTURES = '.ufo/waves/round-31/c2-fixtures.json'
FIXTURES_SHA256 = '1442c14e963bf77df34774015dff7ee73a9738d49b3911d26b4e3b96f48e0b31'
FIXTURES_A1 = '.ufo/waves/round-31/c2-fixtures-a1.json'
FIXTURES_A1_SHA256 = '133547ee55c40635bb288ad0f84f590920a70601c5bed62ff914cbd5848b25fc'
TOOL = 'tools/mori-blind-check.sh'
LANE = '/home/vgpnk/Projects/shokunin/mori-shokunin'
FORBIDDEN_BYTES = (b'c2-fixtures', b'count-c2', b'fixtures-a1')
CLEAN_ENV = {k: v for k, v in os.environ.items() if k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
N_RUNS = 2


def die(msg):
    print(f'count-c2-a1: {msg}')
    print('C2=error')
    sys.exit(2)


def git(repo, *args):
    return subprocess.run(['git', '-C', repo, *args], capture_output=True, env=CLEAN_ENV)


def one_run(k, doc, fixtures, tool_bytes, rnd):
    tmp = tempfile.mkdtemp(prefix='c2a1.', dir='/tmp')
    try:
        sb = os.path.join(tmp, 'repo')
        os.makedirs(os.path.join(sb, doc['wave_dir'], 'sub'))
        if git(sb, 'init', '-q').returncode:
            die('sandbox git init failed')
        used, by_name, files = set(), {}, []
        for f in fixtures:
            while True:
                name = 'Case' + ''.join(rnd.choice(string.ascii_letters + string.digits) for _ in range(6))
                if name not in used and name not in ('CaseOther', 'CaseNested'):
                    break
            used.add(name)
            by_name[name] = f
            nonce = ''.join(rnd.choice('0123456789abcdef') for _ in range(12))
            text = '\n'.join(f['lines']).replace(doc['placeholder'], name) + f'\n<!-- nonce {nonce} -->\n'
            files.append((os.path.join(sb, doc['wave_dir'], name + '.md'), text))
        for u in doc['unscanned']:
            files.append((os.path.join(sb, doc['wave_dir'], u['name']), '\n'.join(u['lines']) + '\n'))
        rnd.shuffle(files)
        for path, text in files:
            with open(path, 'w') as h:
                h.write(text)
            t = 1_600_000_000 + rnd.randrange(100_000_000)
            os.utime(path, (t, t))
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
        cmd = ['timeout', '120', 'bwrap', '--ro-bind', '/', '/', '--tmpfs', '/home', '--tmpfs', '/fast',
               '--dev', '/dev', '--proc', '/proc', '--bind', tmp, tmp, '--chdir', sb, '--',
               '/usr/bin/env', '-i', 'PATH=/usr/bin:/bin', 'bash', tool_path, srev, doc['wave_dir'], doc['writer_regex'], allow_path]
        run = subprocess.run(cmd, capture_output=True)
        out = run.stdout.decode(errors='replace').splitlines()
        scanned = next((l.split('=', 1)[1] for l in out if l.startswith('scanned=')), None)
        violations = next((l.split('=', 1)[1] for l in out if l.startswith('blind_violations=')), None)
        heads = [l for l in out if l.startswith('scanned=') or l.startswith('blind_violations=')]
        hits = [l for l in out if l.strip() and l not in heads]
        got = {n: set() for n in by_name}
        stray = [h for h in heads[2:]] if len(heads) > 2 else []
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
        lines = []
        for name, f in sorted(by_name.items(), key=lambda kv: kv[1]['id']):
            want = {(a, b) for a, b in f['expect']}
            if got[name] == want:
                exact += 1
                lines.append(f"run{k} {f['id']} exact hits={len(want)}")
            else:
                lines.append(f"run{k} {f['id']} diff want={sorted(want)} got={sorted(got[name])}")
        n = len(fixtures)
        dup = len(hits) - len(set(hits))
        scanned_ok = scanned == str(n)
        count_ok = violations is not None and violations.isdigit() and int(violations) == len(hits)
        exit_ok = run.returncode == 1
        for l in lines:
            print(l)
        print(f'run{k} tool_exit={run.returncode} scanned={scanned} scanned_ok={"yes" if scanned_ok else "no"} '
              f'blind_violations={violations} hit_lines={len(hits)} duplicate_hit_lines={dup} count_ok={"yes" if count_ok else "no"} '
              f'exit_ok={"yes" if exit_ok else "no"} stray={len(stray)}')
        for s in stray[:10]:
            print(f'run{k} stray {s}')
        err = run.stderr.decode(errors='replace').strip().splitlines()
        if err and run.returncode not in (0, 1):
            print(f'run{k} stderr_first={err[0][:200]}')
        print(f'run{k} fixtures={n} exact={exact}/{n}')
        return exact == n and scanned_ok and count_ok and exit_ok and not stray and dup == 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


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
            die('usage: count-c2-a1.py <lane-rev> [--tool-file <path>] [--repo <lane-repo>]')
    if not rev or not repo:
        die('usage: count-c2-a1.py <lane-rev> [--tool-file <path>] [--repo <lane-repo>]')
    r = git(repo, 'rev-parse', '--verify', '--quiet', '--end-of-options', rev + '^{commit}')
    if r.returncode:
        die('invalid lane revision')
    full = r.stdout.decode().strip()
    print(f'rev={full}')
    fx = git(repo, 'show', f'{full}:{FIXTURES}')
    fa = git(repo, 'show', f'{full}:{FIXTURES_A1}')
    if fx.returncode or fa.returncode:
        die('fixtures absent at revision')
    if hashlib.sha256(fx.stdout).hexdigest() != FIXTURES_SHA256 or hashlib.sha256(fa.stdout).hexdigest() != FIXTURES_A1_SHA256:
        die('fixtures differ from the frozen sha256')
    doc = json.loads(fx.stdout)
    fixtures = doc['fixtures'] + json.loads(fa.stdout)['fixtures']
    if tool_file:
        tool_bytes = open(tool_file, 'rb').read()
        print(f'tool=file:{tool_file} sha256={hashlib.sha256(tool_bytes).hexdigest()}')
    else:
        t = git(repo, 'show', f'{full}:{TOOL}')
        if t.returncode:
            print('tool=absent')
            print(f'fixtures={len(fixtures)} exact=0/{len(fixtures)}')
            print('C2=unmet')
            return 1
        tool_bytes = t.stdout
        print(f'tool=present blob_sha256={hashlib.sha256(tool_bytes).hexdigest()}')
    leaks = [s.decode() for s in FORBIDDEN_BYTES if s in tool_bytes]
    print(f'answer_key_strings={",".join(leaks) if leaks else "none"}')
    rnd = random.SystemRandom()
    oks = [one_run(k, doc, fixtures, tool_bytes, rnd) for k in range(1, N_RUNS + 1)]
    print(f'runs_met={sum(oks)}/{N_RUNS}')
    met = all(oks) and not leaks
    print('C2=met' if met else 'C2=unmet')
    return 0 if met else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
