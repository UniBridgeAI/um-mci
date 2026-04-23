# Manifest and release integrity

`MANIFEST.json` is the archive inventory for the core release.

## What it contains

- `package_name` and `package_version`
- `archive_root`
- `generated_utc`
- a `files` list with:
  - relative path
  - file size in bytes
  - SHA256 checksum

## Why it matters

The manifest lets a downstream user verify that:
- the package was unpacked correctly,
- the expected files are present,
- no file was silently modified after release.

## What SHA256 means

SHA256 is a file fingerprint. Two identical files have the same SHA256 value; a changed file normally has a different value.

## Built-in integrity helper

Run `scripts/verify_manifest_hashes.py --core-root <unpacked_core_dir>` to verify file sizes and SHA256 hashes against `MANIFEST.json`. This is a release-integrity check against the published snapshot.

## Strict release-tree checking

For maintainer release checks, add `--strict`:

```bash
python scripts/verify_manifest_hashes.py --core-root . --strict
```

Strict mode also rejects unexpected release files and generated caches such as `__pycache__/`, `.pyc`, and `.DS_Store` files.


## Regenerating the manifest

After editing release files, regenerate the manifest from the unpacked core release root:

```bash
python scripts/generate_manifest.py --root .
```

Then run strict verification:

```bash
python scripts/verify_manifest_hashes.py --core-root . --strict
```


## Manifest metadata policy

`MANIFEST.json` is primarily a release-inventory and integrity file. DOI and citation metadata should be treated as authoritative in `CITATION.cff`. The manifest generator preserves existing top-level metadata fields other than the volatile inventory fields (`files` and `generated_utc`), so future fields such as `doi`, `source_commit`, `release_date`, or `license` will not be silently discarded when the manifest is regenerated.
