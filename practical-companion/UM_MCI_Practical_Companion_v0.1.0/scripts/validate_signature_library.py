#!/usr/bin/env python3
# Compatibility wrapper: the implementation lives in lint_signature_library.py.
import runpy, pathlib
runpy.run_path(str(pathlib.Path(__file__).with_name('lint_signature_library.py')), run_name='__main__')
