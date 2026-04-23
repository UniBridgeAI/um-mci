# Practical Companion release checklist

Use this checklist when preparing a public companion release. Ordinary contributors usually only need `scripts/validate_workspace.py`.

1. Remove generated caches and local artifacts:

```bash
find . -name __pycache__ -prune -exec rm -rf {} +
find . -name '*.pyc' -delete
```

2. Regenerate `MANIFEST.json` from the release tree:

```bash
python scripts/generate_companion_manifest.py --root .
```
3. Run ordinary semantic validation:

```bash
python scripts/validate_workspace.py --core-root /path/to/UM_MetaControl_Interface_Core_Semantic_Package_v0.1.0 --companion-root .
```

4. Run maintainer release validation, including strict MANIFEST checks:

```bash
python scripts/validate_workspace.py --core-root /path/to/UM_MetaControl_Interface_Core_Semantic_Package_v0.1.0 --companion-root . --release
```

5. Inspect the zip contents before publishing.
6. Tag the release and archive/publish according to the repository policy.


## Version reset / freeze check

If the public release version is changed before publication, update all package/version references together before regenerating `MANIFEST.json`:

- core `MANIFEST.json` package_version and archive root
- core `CITATION.cff` version / DOI / release date
- companion `core_locator.example.json`
- companion README / quickstart / release checklist paths
- all `package_version_pin.package_semver` values in examples, templates, signatures, priors, and proposals
- companion `MANIFEST.json` package_version and archive root

Then rerun ordinary workspace validation and `--release` validation.


## External evidence refs

When route-prior or governance evidence lives outside this repository, prefer `doi:10.xxxx/...`, `https://doi.org/10.xxxx/...`, or a bare DOI beginning with `10.`. The companion validators treat these as external evidence and will not try to parse them mechanically.
