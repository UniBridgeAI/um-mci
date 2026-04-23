#!/usr/bin/env python3
# This implementation is retained for backward compatibility; public docs prefer the validate_* wrapper.
import argparse, json, pathlib, warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)
from jsonschema import Draft202012Validator, FormatChecker


def load_json(p):
    return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))


def iter_json_files(root):
    root = pathlib.Path(root)
    return sorted(root.glob('*.json')) if root.exists() else []


def iter_dim(node):
    yield node
    for sd in node.get('subdimensions', []):
        yield from iter_dim(sd)
    for ax in node.get('associated_axes', []):
        if isinstance(ax, dict):
            yield from iter_dim(ax)


def collect_paths(options, prefix=()):
    out = set()
    for opt in options:
        path = prefix + (opt['value_id'],)
        out.add(path)
        out |= collect_paths(opt.get('children', []), path)
    return out


def option_reg(core):
    out = {}
    for seed in load_json(core/'layer2_seed'/'um_paradigm_compass_seed.v1.json')['paradigm_compass_seeds']:
        for d in seed.get('dimensions', []):
            for dim in iter_dim(d):
                out[dim['dimension_id']] = collect_paths(dim.get('options', []))
    return out


def core_ids(core):
    dims = load_json(core/'layer1_ontology'/'um_dimensions_ontology.v1.json')['dimensions']
    slots = load_json(core/'layer1_ontology'/'um_edge_slots_ontology.v1.json')['edge_slots']
    edges = load_json(core/'layer2_seed'/'um_edge_families_seed.v1.json')['edge_families']
    return {
        'paradigms': {x['paradigm_id'] for x in load_json(core/'layer1_ontology'/'um_paradigms_ontology.v1.json')['paradigms']},
        'dim_to_paradigm': {x['dimension_id']: x['paradigm_id'] for x in dims},
        'artifacts': {x['artifact_type_id'] for x in load_json(core/'layer1_ontology'/'um_artifact_types_registry.v1.json')['artifact_types']},
        'vps': {x['validation_primitive_id'] for x in load_json(core/'layer1_ontology'/'um_validation_primitives_registry.v1.json')['validation_primitives']},
        'edge_to_slot': {x['edge_family_id']: x.get('edge_slot_id') for x in edges},
        'slot_map': {x['edge_slot_id']: x for x in slots},
    }


def check_pin(pin, manifest, label, errors):
    for key, expected in [
        ('package_name', manifest.get('package_name')),
        ('package_semver', manifest.get('package_version')),
        ('layer1_registry_version', manifest.get('layer1_registry_version', 'v1')),
        ('layer2_seed_version', manifest.get('layer2_seed_version', 'v1')),
    ]:
        if (pin or {}).get(key) != expected:
            errors.append(f'{label} :: {key} pin {(pin or {}).get(key)} != core {expected}')


def validate_file(path, schema, ids, opt, manifest, errors):
    obj = load_json(path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for err in validator.iter_errors(obj):
        loc = '/'.join(str(x) for x in err.path) or '<root>'
        errors.append(f'{path} :: {loc}: {err.message}')

    check_pin(obj.get('package_version_pin', {}), manifest, str(path), errors)
    ef = obj.get('edge_family_id')
    if ef not in ids['edge_to_slot']:
        errors.append(f'{path} :: unknown edge_family_id {ef}')
        return

    stp = obj.get('stage_pattern', {})
    base = stp.get('base_paradigm_id')
    support = stp.get('supporting_paradigm_id')
    if not base:
        errors.append(f'{path} :: stage_pattern.base_paradigm_id is required for shared signature seeds')
    elif base not in ids['paradigms']:
        errors.append(f'{path} :: unknown base_paradigm_id {base}')
    if not support:
        errors.append(f'{path} :: stage_pattern.supporting_paradigm_id is required for shared signature seeds')
    elif support not in ids['paradigms']:
        errors.append(f'{path} :: unknown supporting_paradigm_id {support}')

    slot = ids['slot_map'].get(ids['edge_to_slot'].get(ef), {})
    if base and slot.get('to_paradigm_id') and base != slot.get('to_paradigm_id'):
        errors.append(f'{path} :: base_paradigm_id {base} does not match edge target {slot.get("to_paradigm_id")}')
    if support and slot.get('from_paradigm_id') and support != slot.get('from_paradigm_id'):
        errors.append(f'{path} :: supporting_paradigm_id {support} does not match edge source {slot.get("from_paradigm_id")}')

    hints = stp.get('dimension_hints', [])
    if not (hints or obj.get('required_artifact_hints') or obj.get('required_validation_hints')):
        errors.append(f'{path} :: signature seed must include at least one dimension, artifact, or validation hint')
    for hint in hints:
        dim = hint.get('dimension_id')
        if dim not in opt:
            errors.append(f'{path} :: unknown dimension_id {dim}')
            continue
        if ids['dim_to_paradigm'].get(dim) not in {base, support}:
            errors.append(f'{path} :: dimension_hint {dim} belongs to {ids["dim_to_paradigm"].get(dim)}, not base/support paradigms {base}/{support}')
        for op in hint.get('selected_option_paths', []):
            if tuple(op) not in opt[dim]:
                errors.append(f'{path} :: unknown option path {op} for {dim}')
    for art in obj.get('required_artifact_hints', []) + obj.get('optional_artifact_hints', []):
        if art not in ids['artifacts']:
            errors.append(f'{path} :: unknown artifact hint {art}')
    for vp in obj.get('required_validation_hints', []):
        if vp not in ids['vps']:
            errors.append(f'{path} :: unknown validation hint {vp}')


def main():
    ap = argparse.ArgumentParser(description='Validate companion signature seeds against the released core.')
    ap.add_argument('--core-root', required=True)
    ap.add_argument('--signatures-dir')
    ap.add_argument('--companion-root')
    args = ap.parse_args()

    core = pathlib.Path(args.core_root)
    companion = pathlib.Path(args.companion_root) if args.companion_root else (pathlib.Path(args.signatures_dir).parents[1] if args.signatures_dir else pathlib.Path('.'))

    schema = load_json(companion/'signature_library'/'schemas'/'edge_signature_seed.schema.v1.json')
    ids = core_ids(core)
    opt = option_reg(core)
    manifest = load_json(core/'MANIFEST.json')
    errors = []

    roots = [pathlib.Path(args.signatures_dir)] if args.signatures_dir else [
        companion/'signature_library'/'starter_seeds',
        companion/'signature_library'/'contributed_seeds',
    ]
    for root in roots:
        for path in iter_json_files(root):
            validate_file(path, schema, ids, opt, manifest, errors)

    if errors:
        print('Signature validation failed:')
        for err in errors:
            print(' -', err)
        return 1
    print('Signature seeds validated successfully.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
