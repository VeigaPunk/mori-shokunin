#!/usr/bin/python3
import os, sys, time
_OUT = '/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/NoHarmRun/r16/cases/typedfields_bool_status_mixed_valid/payload-stdout.bin'
_ERR = '/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/NoHarmRun/r16/cases/typedfields_bool_status_mixed_valid/payload-stderr.bin'
_LOG = '/home/vgpnk/Projects/shokunin/mori-shokunin/.ufo/waves/round-20/falsify/NoHarmRun/r16/cases/typedfields_bool_status_mixed_valid/journalctl-argv.txt'
_PAD = 0
_SLEEP = 0
_RC = 0
def _emit():
    data = open(_OUT, 'rb').read() + b'x' * _PAD
    off = 0
    while off < len(data):
        off += os.write(1, data[off:])
    err = open(_ERR, 'rb').read()
    off = 0
    while off < len(err):
        off += os.write(2, err[off:])
with open(_LOG, 'w') as fh:
    fh.write('\x00'.join(sys.argv[1:]))
_emit()
sys.exit(_RC)
