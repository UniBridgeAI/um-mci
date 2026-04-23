#!/usr/bin/env python3
import argparse
import hashlib
import json
import pathlib

FORBIDDEN_DIRS = {"__pycache__", ".git"}
FORBIDDEN_SUFFIXES = {".pyc"}
FORBIDDEN_NAMES = {".DS_Store"}
IGNORED_FOR_MANIFEST_COMPARISON = {"MANIFEST.json"}


def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_actual_files(root: pathlib.Path):
    for p in root.rglob("*"):
        if p.is_file():
            yield p


def verify(root: pathlib.Path, strict: bool = False, label: str = "Manifest") -> int:
    manifest_path = root / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors = []
    manifest_files = {entry["path"] for entry in manifest.get("files", [])}

    for entry in manifest.get("files", []):
        rel = entry["path"]
        path = root / rel
        if not path.exists():
            errors.append(f"missing file: {rel}")
            continue
        if path.stat().st_size != entry.get("size_bytes"):
            errors.append(f"size mismatch for {rel}: {path.stat().st_size} != {entry.get('size_bytes')}")
        digest = sha256_file(path)
        if digest != entry.get("sha256"):
            errors.append(f"sha256 mismatch for {rel}: {digest} != {entry.get('sha256')}")

    if strict:
        actual_files = set()
        for p in iter_actual_files(root):
            rel = p.relative_to(root).as_posix()
            parts = set(p.relative_to(root).parts)
            if parts & FORBIDDEN_DIRS or p.suffix in FORBIDDEN_SUFFIXES or p.name in FORBIDDEN_NAMES:
                errors.append(f"forbidden generated/local file in release tree: {rel}")
                continue
            if rel not in IGNORED_FOR_MANIFEST_COMPARISON:
                actual_files.add(rel)

        for rel in sorted(actual_files - manifest_files):
            errors.append(f"unexpected file not listed in MANIFEST.json: {rel}")
        for rel in sorted(manifest_files - actual_files):
            if not (root / rel).exists():
                errors.append(f"manifest lists missing file: {rel}")

    if errors:
        print(f"{label} verification failed:")
        for err in errors:
            print(" -", err)
        return 1

    mode = "strict " if strict else ""
    print(f"{mode}{label} verification passed.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify file sizes and SHA256 hashes against MANIFEST.json.")
    ap.add_argument("--core-root", required=True)
    ap.add_argument("--strict", action="store_true", help="Also reject unexpected files and generated caches in the release tree.")
    args = ap.parse_args()
    return verify(pathlib.Path(args.core_root).resolve(), strict=args.strict, label="Manifest")


if __name__ == "__main__":
    raise SystemExit(main())
