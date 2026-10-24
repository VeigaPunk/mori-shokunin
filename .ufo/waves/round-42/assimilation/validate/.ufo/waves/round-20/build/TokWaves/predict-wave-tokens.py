#!/usr/bin/env python3
"""Predict the drift tokens that the FINDING WAVE_UNSETTLED_AGE family contributes to
`mori-census.sh --drift` and check them against the round-20 entering receipt.

Inputs (all read-only):
  - baseline canonical block: corpus/evidence/baseline-r10-20261015T2231Z.json
  - live wave probe: wave-probe-replica.sh (mirrors census probe_waves, lines 876-929)
  - DRIFT_COUNTER_KEYS and the normalizer regexes: `git show HEAD:tools/mori-census.sh`
Algorithm mirrors census drift_report (pass 1 exact multiset, pass 2 same-id pairing with
drift_field_report, pass 3 unpaired new lines) and `LC_ALL=C sort -u`.
Writes nothing. Candidate analysis for TokWaves C1 only.
"""
import json
import re
import subprocess
from pathlib import Path

ROOT = Path('/home/vgpnk/Projects/shokunin/mori-shokunin')
BASE = ROOT / 'corpus/evidence/baseline-r10-20261015T2231Z.json'
RECEIPT = ROOT / '.ufo/waves/round-20/evidence/c1-drift-entering.json'
REPLICA = ROOT / '.ufo/waves/round-20/build/TokWaves/wave-probe-replica.sh'
WAVES = Path('/home/vgpnk/Projects/shokunin/.ufo/waves')
MARK = '# --- canonical output follows ---'


def census_head_text():
    return subprocess.run(['git', '-C', str(ROOT), 'show', 'HEAD:tools/mori-census.sh'],
                          capture_output=True, text=True, check=True).stdout


def counter_keys(src):
    m = re.search(r'^DRIFT_COUNTER_KEYS=\(\n(.*?)\n\)', src, re.S | re.M)
    return [w for w in m.group(1).split() if not w.startswith('#')]


def normalize(line, keys):
    # Mirrors drift_normalize for the keys that occur on WAVE_UNSETTLED_AGE lines.
    cre = '|'.join(keys)
    line = re.sub(r'\bts=[^ ;)]*', 'ts=<V>', line)
    line = re.sub(r'\bage_s=[0-9]+', 'age_s=<V>', line)
    line = re.sub(r'\bscript_sha256=[0-9a-f]+', 'script_sha256=<V>', line)
    line = re.sub(r'\b(' + cre + r')=[0-9]+', lambda m: m.group(1) + '=<V>', line)
    return line


def fields(line):
    d = {}
    for tok in line.split():
        if '=' not in tok:
            continue
        k, v = tok.split('=', 1)
        if not re.fullmatch(r'[A-Za-z0-9_]+', k):
            continue
        d[k] = d.get(k, '') + v  # drift_scan concatenates duplicated keys
    return d


def ident(line):
    rest = line[len('FINDING '):]
    return 'FINDING:' + rest.split(' severity=')[0]


def field_report(bl, nl, ident_):
    bf, nf = fields(bl), fields(nl)
    changed = []
    for k in bf:
        if k not in nf:
            changed.append('-' + k)
        elif bf[k] != nf[k]:
            changed.append(k)
    for k in nf:
        if k not in bf:
            changed.append('+' + k)
    return changed or [ident_]


def drift_report(base, new):
    base_used = [False] * len(base)
    new_used = [False] * len(new)
    rep = []
    for i, b in enumerate(base):  # pass 1: exact multiset match
        for j, n in enumerate(new):
            if not new_used[j] and n == b:
                base_used[i] = new_used[j] = True
                break
    for i, b in enumerate(base):  # pass 2: same-id pairing
        if base_used[i]:
            continue
        bid = ident(b)
        matched = -1
        for j, n in enumerate(new):
            if not new_used[j] and ident(n) == bid:
                matched = j
                break
        if matched >= 0:
            new_used[matched] = True
            rep += field_report(b, new[matched], bid)
        else:
            rep.append('-' + bid)
    for j, n in enumerate(new):  # pass 3: unpaired new lines
        if not new_used[j]:
            rep.append('+' + ident(n))
    if not rep:
        rep = ['output-order']
    return sorted(set(rep))


def replica_aged():
    out = subprocess.run(['bash', str(REPLICA), str(WAVES)], capture_output=True,
                         text=True, check=True).stdout.splitlines()
    now_epoch = int(re.search(r'now_epoch=(\d+)', out[0]).group(1))
    aged, rows = [], []
    for line in out[1:]:
        name, rest = line.split('|', 1)
        cls = re.search(r'class=([^|\s]+)', rest).group(1)
        rows.append((name, cls))
        if cls == 'AGED_UNSETTLED':
            reg = re.search(r'reg=(\d)', rest).group(1)
            disp = re.search(r'disp=(\d)', rest).group(1)
            run = re.search(r'run=(\d)', rest).group(1)
            age = re.search(r'age_s=(\d+)', rest).group(1)
            aged.append((name, reg, disp, run, age))
    return now_epoch, aged, rows


def main():
    keys = counter_keys(census_head_text())
    canon = BASE.read_text().split(MARK, 1)[1].split('\n')[1:]
    base_wave = [l for l in canon if l.startswith('FINDING WAVE_UNSETTLED_AGE ')]
    base_names = [re.search(r'obs=wave=(\S+)', l).group(1) for l in base_wave]

    now_epoch, aged, rows = replica_aged()
    new_wave = []
    for name, reg, disp, run, age in aged:
        raw = (f'FINDING WAVE_UNSETTLED_AGE severity=warn obs=wave={name} age_s={age} '
               f'threshold_s=7200 reg={reg} disp={disp} run={run} settle=0 '
               f'ts=2026-10-21T10:32:58Z script_sha256={"0" * 64}')
        new_wave.append(normalize(raw, keys))
    new_names = [n for n, *_ in aged]

    # Baseline lines are already masked at pin time; only the live side is normalized.
    predicted = drift_report(base_wave, new_wave)

    receipt_tokens = set(json.loads(RECEIPT.read_text())['tokens'])
    print('baseline WAVE lines:', len(base_wave))
    print('live AGED_UNSETTLED (now_epoch=%d): %d' % (now_epoch, len(aged)))
    for name, reg, disp, run, age in aged:
        print('  %-36s reg=%s disp=%s run=%s age_s=%s' % (name, reg, disp, run, age))
    print('removed from baseline:', sorted(set(base_names) - set(new_names)))
    print('added vs baseline    :', sorted(set(new_names) - set(base_names)))
    print('predicted WAVE-family tokens:', ' '.join(predicted))
    print('all predicted tokens in receipt:', all(t in receipt_tokens for t in predicted))
    print('-FINDING:WAVE_UNSETTLED_AGE in receipt:', '-FINDING:WAVE_UNSETTLED_AGE' in receipt_tokens)
    print('+FINDING:WAVE_UNSETTLED_AGE in receipt:', '+FINDING:WAVE_UNSETTLED_AGE' in receipt_tokens)
    print('obs in receipt:', 'obs' in receipt_tokens)
    print('SURFACE:waves in receipt:', 'SURFACE:waves' in receipt_tokens,
          '| predicted SURFACE waves state:', 'drift' if aged else 'ok')
    print('replica classes:', sorted({c for _, c in rows}), 'rows:', len(rows))


if __name__ == '__main__':
    main()
