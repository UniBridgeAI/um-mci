#!/usr/bin/env python3
import argparse, os, pathlib, subprocess, sys


def run(cmd):
    print('$', ' '.join(cmd), flush=True)
    env = os.environ.copy()
    env.setdefault('PYTHONDONTWRITEBYTECODE', '1')
    return subprocess.run(cmd, env=env).returncode


def main():
    ap = argparse.ArgumentParser(description='Run the Practical Companion validation suite against a pinned core release.')
    ap.add_argument('--core-root', required=True)
    ap.add_argument('--companion-root', default='.')
    ap.add_argument('--skip-core-validator', action='store_true')
    ap.add_argument('--release', action='store_true', help='Run release-integrity checks, including core and companion MANIFEST hash verification.')
    ap.add_argument('--check-core-manifest', action='store_true', help='Check the core MANIFEST even outside --release mode.')
    ap.add_argument('--check-companion-manifest', action='store_true', help='Check the companion MANIFEST even outside --release mode.')
    args = ap.parse_args()

    core = pathlib.Path(args.core_root).resolve()
    comp = pathlib.Path(args.companion_root).resolve()
    py = sys.executable
    errors = 0

    if not args.skip_core_validator:
        errors |= run([py, str(core/'scripts'/'validate_core_package.py'), '--core-root', str(core)])

    if args.release or args.check_core_manifest:
        errors |= run([py, str(core/'scripts'/'verify_manifest_hashes.py'), '--core-root', str(core), '--strict'])
    if args.release or args.check_companion_manifest:
        errors |= run([py, str(comp/'scripts'/'verify_companion_manifest_hashes.py'), '--companion-root', str(comp), '--strict'])

    errors |= run([py, str(comp/'scripts'/'validate_examples_against_core.py'), '--core-root', str(core), '--companion-root', str(comp)])
    errors |= run([py, str(comp/'scripts'/'validate_signature_library.py'), '--core-root', str(core), '--companion-root', str(comp)])
    errors |= run([py, str(comp/'scripts'/'validate_route_prior_notes.py'), '--core-root', str(core), '--companion-root', str(comp)])
    errors |= run([py, str(comp/'scripts'/'validate_governance_proposals.py'), '--core-root', str(core), '--companion-root', str(comp)])

    if errors:
        print('Workspace validation failed.')
        return 1
    if args.release:
        print('Workspace release validation passed.')
    else:
        print('Workspace semantic validation passed. Use --release to include MANIFEST hash checks.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
