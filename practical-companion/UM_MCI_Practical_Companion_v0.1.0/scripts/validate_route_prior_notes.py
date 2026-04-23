#!/usr/bin/env python3
# Compatibility wrapper: the implementation lives in lint_route_prior_notes.py.
import runpy, pathlib
runpy.run_path(str(pathlib.Path(__file__).with_name('lint_route_prior_notes.py')), run_name='__main__')
