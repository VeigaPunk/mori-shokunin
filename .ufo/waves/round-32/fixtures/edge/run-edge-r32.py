#!/usr/bin/env python3
"""Round-32 defect-6 fixture runner: edge cases for tools/mori-blind-check.sh.

Reads fixtures/edge-r32.json, materialises each case's brief bytes and allow file into a
fresh sandbox git repo under this seat's scratch dir, runs the LANE tool the way its usage
says (cwd inside the sandbox repo, lane-rev = the sandbox commit, wave-report-dir, writer-name
regex, allow-file), and records the actual stdout/exit.

usage: run-edge-r32.py [--update]   (--update rewrites the stored `actual` column and the
                                   `agree` / `agree_alt` columns)

Never writes in the lane repo; it only reads tools/mori-blind-check.sh from it.
"""
import base64, hashlib, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(HERE, 'fixtures', 'edge-r32.json')
TOOL = '/home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-blind-check.sh'
SANDBOX = os.path.join(HERE, 'sandbox')
CLEAN_ENV = {k: v for k, v in os.environ.items() if k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}


def git(repo, *args):
    return subprocess.run(['git', '-C', repo, *args], capture_output=True, env=CLEAN_ENV)


def build_sandbox(doc):
    if os.path.exists(SANDBOX):
        shutil.rmtree(SANDBOX)
    repo = os.path.join(SANDBOX, 'repo')
    os.makedirs(os.path.join(repo, 'allow'))
    git(repo, 'init', '-q', '-b', 'main')
    for case in doc['cases']:
        wave = os.path.join(repo, case['wave_dir'])
        os.makedirs(wave, exist_ok=True)
        brief = base64.b64decode(case['brief_base64'])
        with open(os.path.join(wave, case['brief_name']), 'wb') as h:
            h.write(brief)
        with open(os.path.join(repo, 'allow', case['id'] + '.txt'), 'w') as h:
            h.write('\n'.join(case['allow_lines']) + '\n')
    git(repo, 'add', '-A')
    c = git(repo, '-c', 'user.name=EdgeR32', '-c', 'user.email=edge@example.invalid',
            'commit', '-q', '-m', 'round-32 defect-6 edge fixtures')
    if c.returncode:
        print('sandbox commit failed:', c.stderr.decode(errors='replace'))
        sys.exit(2)
    rev = git(repo, 'rev-parse', 'HEAD').stdout.decode().strip()
    return repo, rev


def run_case(case, rev, repo):
    """Run the lane tool over one case's wave dir; return (stdout_lines, exit, hits)."""
    allow = os.path.join(repo, 'allow', case['id'] + '.txt')
    proc = subprocess.run(
        ['timeout', '120', 'bash', TOOL, rev, case['wave_dir'], case['writer_regex'], allow],
        cwd=repo, capture_output=True, env=CLEAN_ENV)
    out = proc.stdout.decode(errors='replace').splitlines()
    hits = [l for l in out if l.strip() and not l.startswith('scanned=')
            and not l.startswith('blind_violations=')]
    return out, proc.returncode, hits


def verdict(hits, exit_code, want_hits, want_exit):
    return 'yes' if (sorted(hits) == sorted(want_hits) and exit_code == want_exit) else 'no'


def main(argv):
    update = '--update' in argv
    with open(JSON_PATH) as h:
        doc = json.load(h)
    repo, rev = build_sandbox(doc)
    tool_sha = hashlib.sha256(open(TOOL, 'rb').read()).hexdigest()
    print(f'sandbox={repo}')
    print(f'rev={rev}')
    print(f'tool={TOOL}')
    print(f'tool_sha256={tool_sha}')
    mismatches = 0
    for case in doc['cases']:
        out, rc, hits = run_case(case, rev, repo)
        exp = case['expected']
        alt = case.get('alt_reading')
        agree = verdict(hits, rc, exp['hits'], exp['exit'])
        agree_alt = verdict(hits, rc, alt['hits'], alt['exit']) if alt else None
        if update:
            case['actual'] = {'exit': rc, 'stdout': out, 'hits': hits}
            case['agree'] = agree
            case['agree_alt'] = agree_alt
        else:
            prev = case.get('actual') or {}
            if prev.get('exit') != rc or prev.get('hits') != hits:
                mismatches += 1
        print(f"--- {case['id']} {case['title']}")
        print(f"    expected(primary): {exp['hits']} exit={exp['exit']}  -> agree={agree}")
        if alt:
            print(f"    expected(alt)   : {alt['hits']} exit={alt['exit']}  -> agree_alt={agree_alt}")
        print(f'    actual stdout    : {out!r}')
        print(f'    actual exit      : {rc}')
    if update:
        doc['actual_run'] = {'sandbox_rev': rev, 'tool_sha256': tool_sha,
                             'sandbox': repo, 'runner': os.path.abspath(__file__)}
        with open(JSON_PATH, 'w') as h:
            json.dump(doc, h, indent=1, ensure_ascii=False)
            h.write('\n')
        print('updated', JSON_PATH)
    elif mismatches:
        print(f'MISMATCH: {mismatches} case(s) differ from the stored actual column')
        return 1
    else:
        print('stored actual column reproduced for every case')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
