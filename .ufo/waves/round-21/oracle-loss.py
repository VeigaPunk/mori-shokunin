#!/usr/bin/env python3
"""Independent black-box measurement of the frozen round21 requirements.

Written by L1 after OracleLoss's provider death, before reading target source.
The empty before accounting is an explicit absent-representation model, not
proof of two historical implementation bugs. It never presumes a verdict
from the word before/after: every count comes from actual CLI observations.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser()
    for key in ('tool', 'root', 'required', 'before-accounting', 'after-accounting',
                'before-rule', 'after-rule', 'cases', 'out', 'revision'):
        p.add_argument('--' + key, required=True)
    a = p.parse_args()
    if len(a.revision) not in (40, 64) or any(c not in '0123456789abcdef' for c in a.revision):
        raise ValueError('full measured commit required')
    root = Path(a.root).resolve(strict=True)
    # Reject moving/uncommitted input bytes before comparison; a printed hash
    # alone is not measured-revision binding.
    for name, path in vars(a).items():
        if name in ('root', 'out', 'revision'):
            continue
        loaded = Path(path).resolve(strict=True)
        relative = loaded.relative_to(root).as_posix()
        committed = subprocess.run(
            ['git', '-C', str(root), 'cat-file', 'blob', a.revision + ':' + relative],
            capture_output=True, timeout=30)
        if committed.returncode or committed.stdout != loaded.read_bytes():
            raise ValueError('input not bound to measured commit: ' + name)
    case_document = json.loads(Path(a.cases).read_bytes())
    required_document = json.loads(Path(a.required).read_bytes())
    if case_document.get('schema') != 'mori-evidence-loss-cases-v1':
        raise ValueError('invalid case schema')
    if required_document.get('schema') != 'mori-required-observations-v1':
        raise ValueError('invalid required schema')
    cases = case_document['cases']
    required = required_document['observations']
    if {x['id'] for x in required} != {'aggregator-r10', 'aggregator-r10-resume'}:
        raise ValueError('required population differs from frozen historical pair')
    if len(required) != 2:
        raise ValueError('duplicate required population')
    rows = []
    issues = []

    def invoke(args):
        argv = [sys.executable, a.tool] + args
        r = subprocess.run(argv, capture_output=True, text=True, timeout=30)
        try:
            value = json.loads(r.stdout)
        except (ValueError, TypeError):
            value = None
        return {'argv': argv, 'exit_code': r.returncode,
                'stdout_sha256': hashlib.sha256(r.stdout.encode()).hexdigest(),
                'stderr_sha256': hashlib.sha256(r.stderr.encode()).hexdigest(),
                'stderr_bytes': len(r.stderr.encode()), 'observed': value}

    for phase, accounting, rule in (
            ('before', a.before_accounting, a.before_rule),
            ('after', a.after_accounting, a.after_rule)):
        audit = invoke(['audit', '--root', a.root, '--required', a.required,
                        '--accounting', accounting])
        classify = invoke(['classify', '--rule', rule, '--cases', a.cases])
        source_rows = json.loads(Path(accounting).read_bytes())['observations']
        actual_ids = {x['id'] for x in source_rows}
        expected_omitted = len({x['id'] for x in required} - actual_ids)
        audit_value = audit['observed'] or {}
        if audit_value.get('schema') != 'mori-evidence-loss-audit-v1':
            issues.append(phase + ':audit-schema-mismatch')
        # Both declared measurement inputs intentionally contain omissions or
        # unresolved rows. rc2 can never stand in for their expected red rc1.
        if audit['exit_code'] != 1 or audit['stderr_bytes']:
            issues.append(phase + ':audit-exit-or-stderr-mismatch')
        if audit_value.get('pin_allowed') is not False:
            issues.append(phase + ':audit-pin-not-blocked')
        if audit_value.get('omitted') != expected_omitted:
            issues.append(phase + ':omission-counter-mismatch')
        class_value = classify['observed'] or {}
        observations = class_value.get('cases', class_value.get('results', []))
        # Preserve the entire returned decision object. An unsupported output
        # shape is a real mismatch, never absence or an assumed improvement.
        by_id = {x.get('id'): x for x in observations if isinstance(x, dict)}
        independent_mismatches = []
        for case in cases:
            observed = by_id.get(case['id'], {})
            got_class = observed.get('observed_class', observed.get('class'))
            got_pin = observed.get('observed_pin_allowed', observed.get('pin_allowed'))
            if got_class != case['expected_class'] or got_pin is not case['expected_pin_allowed']:
                independent_mismatches.append(case['id'])
        expected_classify_rc = 1 if independent_mismatches else 0
        if classify['exit_code'] != expected_classify_rc or classify['stderr_bytes']:
            issues.append(phase + ':classify-exit-or-stderr-mismatch')
        if class_value.get('mismatched') != len(independent_mismatches):
            issues.append(phase + ':classify-counter-mismatch')
        rows.append({'phase': phase, 'audit': audit, 'classification': classify,
                     'independent_omitted': expected_omitted,
                     'independent_mismatched': len(independent_mismatches),
                     'independent_mismatch_ids': independent_mismatches})
    out = {'schema': 'mori-r21-oracle-v1', 'measured_revision': a.revision,
           'executing_sha256': sha(__file__), 'tool_sha256': sha(a.tool),
           'inputs': {name: sha(path) for name, path in vars(a).items()
                      if name not in ('root', 'out', 'revision')},
           'rows': rows, 'instrument_issues': issues}
    Path(a.out).write_text(json.dumps(out, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'rows': [{'phase': x['phase'],
                               'omitted': x['independent_omitted'],
                               'mismatched': x['independent_mismatched'],
                               'audit_rc': x['audit']['exit_code'],
                               'classify_rc': x['classification']['exit_code']}
                              for x in rows], 'instrument_issues': issues}))
    return 1 if issues else 0


if __name__ == '__main__':
    raise SystemExit(main())
