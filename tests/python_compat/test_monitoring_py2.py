#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import shutil
import sys
import tempfile

sys.path.insert(0, '/work/src/modules')

import monitoring


def main():
    os.environ.setdefault('LOGNAME', 'codex')

    tempdir = tempfile.mkdtemp(prefix='monitoring-py2-')
    try:
        record = monitoring.MONITOR_FILE('codex_monitor', tempdir).create()
        record.set_line('unicode_value', u'räksmörgås')
        record.set_line('string_value', 'plain-ascii')
        record.set_line('number_value', 42)

        loaded = monitoring.MONITOR_FILE('codex_monitor', tempdir).read()

        assert loaded.pid == str(os.getpid())
        assert loaded.user == os.environ['LOGNAME']
        assert loaded.unicode_value == u'räksmörgås'.encode('utf-8')
        assert loaded.string_value == 'plain-ascii'
        assert loaded.number_value == '42'

        print('python2 monitoring test passed')
    finally:
        shutil.rmtree(tempdir)


if __name__ == '__main__':
    main()
