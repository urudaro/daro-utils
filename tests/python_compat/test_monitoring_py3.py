#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import tempfile

sys.path.insert(0, '/work/src/modules')

import monitoring


def main():
    os.environ.setdefault('LOGNAME', 'codex')

    tempdir = tempfile.mkdtemp(prefix='monitoring-py3-')
    try:
        record = monitoring.MONITOR_FILE('codex_monitor', tempdir).create()
        record.set_line('unicode_value', u'räksmörgås')
        record.set_line('string_value', 'plain-ascii')
        record.set_line('bytes_value', b'plain-bytes')
        record.set_line('number_value', 42)

        loaded = monitoring.MONITOR_FILE('codex_monitor', tempdir).read()

        assert loaded.pid == str(os.getpid())
        assert loaded.user == os.environ['LOGNAME']
        assert loaded.unicode_value == u'räksmörgås'
        assert loaded.string_value == 'plain-ascii'
        assert loaded.bytes_value == 'plain-bytes'
        assert loaded.number_value == '42'

        print('python3 monitoring test passed')
    finally:
        shutil.rmtree(tempdir)


if __name__ == '__main__':
    main()
