#!/usr/bin/env python3
import argparse
import datetime
import hashlib
import json
import pathlib

FORBIDDEN_DIRS = {'__pycache__', '.git'}
FORBIDDEN_SUFFIXES = {'.pyc', '.pyo'}
FORBIDDEN_NAMES = {'.DS_Store'}

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def should_include(path, root):
    rel = path.relative_to(root)
    if rel.as_posix() == 'MANIFEST.json':
        return False
    if any(part in FORBIDDEN_DIRS for part in rel.parts):
        return False
    if path.suffix in FORBIDDEN_SUFFIXES:
        return False
    if path.name in FORBIDDEN_NAMES:
        return False
    return path.is_file()

def main():
    ap = argparse.ArgumentParser(description='Regenerate MANIFEST.json for a UM-MCI Practical Companion release tree.')
    ap.add_argument('--root', required=True, help='Release root directory')
    ap.add_argument('--package-name')
    ap.add_argument('--package-version')
    ap.add_argument('--archive-root')
    args = ap.parse_args()

    root = pathlib.Path(args.root).resolve()
    manifest_path = root / 'MANIFEST.json'
    previous = {}
    if manifest_path.exists():
        previous = json.loads(manifest_path.read_text(encoding='utf-8'))

    package_name = args.package_name or previous.get('package_name') or root.name
    package_version = args.package_version or previous.get('package_version') or previous.get('package_semver') or '0.0.0'
    archive_root = args.archive_root or previous.get('archive_root') or root.name

    files = []
    for path in sorted(root.rglob('*')):
        if not should_include(path, root):
            continue
        rel = path.relative_to(root).as_posix()
        files.append({
            'path': rel,
            'size_bytes': path.stat().st_size,
            'sha256': sha256_file(path),
        })

    # Preserve any future top-level release metadata (for example doi,
    # source_commit, release_date, or license) while regenerating the
    # volatile inventory fields. This keeps MANIFEST usable as an inventory
    # file without accidentally discarding release metadata added later.
    manifest = {k: v for k, v in previous.items() if k not in {'files', 'generated_utc'}}
    manifest['package_name'] = package_name
    manifest['package_version'] = package_version
    manifest['archive_root'] = archive_root
    manifest['generated_utc'] = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    manifest.setdefault('notes', 'Generated release manifest. MANIFEST.json is excluded from the hashed file list to avoid self-referential hashing.')
    manifest['files'] = files
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'Wrote {manifest_path} with {len(files)} files.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
