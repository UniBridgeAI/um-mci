#!/usr/bin/env python3
# Compatibility wrapper: the implementation lives in lint_governance_proposals.py.
import runpy, pathlib
runpy.run_path(str(pathlib.Path(__file__).with_name('lint_governance_proposals.py')), run_name='__main__')
