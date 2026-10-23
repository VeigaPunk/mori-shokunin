#!/usr/bin/env python3
"""Round-32 seat helper (not the counter; it imports the frozen counter's own functions and changes none of them).

usage:
  seat-check.py text <copy-file>                      print the normalised text the counter matches quotes against
  seat-check.py row <id> <copy-file> '<quotes cell>'  check one draft row against R2 and the live part of R3

The quotes cell is written exactly as in the table: 1-3 double-quoted quotes separated by '; '.
"""
import hashlib, importlib.util, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location('count_c1', os.path.join(HERE, 'count-c1.py'))
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


def main(a):
    if len(a) == 2 and a[0] == 'text':
        print(c.normalise(open(a[1], 'rb').read())); return 0
    if len(a) == 4 and a[0] == 'row':
        pop = {p['id']: p for p in json.load(open(os.path.join(HERE, 'c1-population.json')))['population']}
        p = pop.get(a[1])
        if p is None:
            print(f'{a[1]}: not in population'); return 2
        data = open(a[2], 'rb').read()
        qs = c.quotes_of(a[3])
        nt = c.normalise(data)
        ref = c.tokens(p['teaches'] + ' ' + p['anchor'] + ' ' + p['scope'])
        shared = sorted(c.tokens(' '.join(qs)) & ref)
        print(f'sha256={hashlib.sha256(data).hexdigest()}')
        print(f'quotes={len(qs)} words={[len(q.split()) for q in qs]} in_copy={[q in nt for q in qs]}')
        print(f'shared_tokens={shared} topic_ok={len(shared) >= 2}')
        live = any(all(q in c.normalise(b) for q in qs) for b in c.fetch(p['url']))
        print(f'live_quotes_ok={live}')
        ok = 1 <= len(qs) <= 3 and all(3 <= len(q.split()) <= 25 for q in qs) and all(q in nt for q in qs) \
            and len(shared) >= 2 and live
        print('ROW_CHECK=' + ('pass' if ok else 'fail') + ' (judge R4 and R5 not checked here)')
        return 0 if ok else 1
    print(__doc__); return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
