#!/usr/bin/env python3
import argparse
import json
import pathlib
import sys
import warnings
from typing import Dict, List, Set, Tuple
warnings.filterwarnings('ignore', category=DeprecationWarning)
from jsonschema import Draft202012Validator, RefResolver, FormatChecker


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def build_store(schema_root):
    store = {}
    for path in pathlib.Path(schema_root).rglob('*.json'):
        try:
            obj = load_json(path)
        except Exception:
            continue
        if isinstance(obj, dict) and '$id' in obj:
            store[obj['$id']] = obj
    return store


def make_validator(schema_path, store):
    schema = load_json(schema_path)
    base_uri = schema_path.resolve().parent.as_uri() + '/'
    resolver = RefResolver(base_uri=base_uri, referrer=schema, store=store)
    return Draft202012Validator(schema, resolver=resolver, format_checker=FormatChecker())


def collect_schema_errors(validator, instance, label):
    errs = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    out = []
    for e in errs:
        loc = '/'.join(str(x) for x in e.path)
        out.append(f'{label} :: {loc or "<root>"}: {e.message}')
    return out


def iter_dimension_node(node):
    yield node
    for sd in node.get('subdimensions', []):
        yield from iter_dimension_node(sd)
    for ax in node.get('associated_axes', []):
        if isinstance(ax, dict):
            yield from iter_dimension_node(ax)


def collect_option_paths(options, prefix=()):
    out = set()
    for opt in options:
        path = prefix + (opt['value_id'],)
        out.add(path)
        children = opt.get('children', [])
        if children:
            out |= collect_option_paths(children, path)
    return out


def option_path_registry(core_root):
    seeds = load_json(core_root/'layer2_seed'/'um_paradigm_compass_seed.v1.json')['paradigm_compass_seeds']
    reg = {}
    for seed in seeds:
        for d in seed.get('dimensions', []):
            for dim in iter_dimension_node(d):
                reg[dim['dimension_id']] = collect_option_paths(dim.get('options', []))
    return reg


def load_dimension_constraints(core_root):
    dims = load_json(core_root/'layer1_ontology'/'um_dimensions_ontology.v1.json')['dimensions']
    return {d['dimension_id']: d.get('selection_constraints', []) for d in dims}


def enforce_constraint(selected_dim_ids: Set[str], constraint: dict, label: str, errors: List[str]):
    ctype = constraint.get('constraint_type')
    if ctype == 'at_least_one_dimension_selected':
        pool = set(constraint.get('dimension_ids', []))
        if pool and selected_dim_ids.isdisjoint(pool):
            errors.append(f'{label} :: selection constraint failed: expected at least one of {sorted(pool)} to be selected')
    elif ctype == 'at_least_one_subdimension_selected':
        pool = set(constraint.get('subdimension_ids', []))
        if pool and selected_dim_ids.isdisjoint(pool):
            errors.append(f'{label} :: selection constraint failed: expected at least one of subdimensions {sorted(pool)} to be selected')


def extract_package_semvers(core_root):
    vals = {}
    for path in list((core_root/'layer1_ontology').glob('*.json')) + list((core_root/'layer2_seed').glob('*.json')):
        obj = load_json(path)
        vals[str(path.relative_to(core_root))] = obj.get('package', {}).get('package_semver')
    return vals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--core-root', required=True)
    args = ap.parse_args()
    core_root = pathlib.Path(args.core_root)
    schema_root = core_root / 'schemas'
    store = build_store(schema_root)
    errors: List[str] = []

    checks = [
        ('layer1_ontology/um_namespaces.v1.json', 'schemas/um_namespaces.schema.v1.json'),
        ('layer1_ontology/um_paradigms_ontology.v1.json', 'schemas/um_paradigms_ontology.schema.v1.json'),
        ('layer1_ontology/um_dimensions_ontology.v1.json', 'schemas/um_dimensions_ontology.schema.v1.json'),
        ('layer1_ontology/um_machine_controls_registry.v1.json', 'schemas/um_machine_controls_registry.schema.v1.json'),
        ('layer1_ontology/um_edge_slots_ontology.v1.json', 'schemas/um_edge_slots_ontology.schema.v1.json'),
        ('layer1_ontology/um_artifact_types_registry.v1.json', 'schemas/um_artifact_types_registry.schema.v1.json'),
        ('layer1_ontology/um_validation_primitives_registry.v1.json', 'schemas/um_validation_primitives_registry.schema.v1.json'),
        ('layer1_ontology/um_operational_tensions_ontology.v1.json', 'schemas/um_operational_tensions_ontology.schema.v1.json'),
        ('layer1_ontology/um_context_ontology.v1.json', 'schemas/um_context_ontology.schema.v1.json'),
        ('layer2_seed/um_paradigm_compass_seed.v1.json', 'schemas/um_paradigm_compass_seed.schema.v1.json'),
        ('layer2_seed/um_paradigm_defaults_seed.v1.json', 'schemas/um_paradigm_defaults_seed.schema.v1.json'),
        ('layer2_seed/um_edge_families_seed.v1.json', 'schemas/um_edge_families_seed.schema.v1.json'),
    ]

    for inst_rel, schema_rel in checks:
        validator = make_validator(core_root / schema_rel, store)
        errors.extend(collect_schema_errors(validator, load_json(core_root / inst_rel), inst_rel))

    # Package semver consistency across registries/seeds and manifest/citation
    semvers = extract_package_semvers(core_root)
    manifest = load_json(core_root/'MANIFEST.json')
    manifest_ver = manifest.get('package_version')
    if any(v != manifest_ver for v in semvers.values() if v is not None):
        errors.append(f'MANIFEST/version mismatch :: expected all registry package_semver values to equal manifest package_version {manifest_ver}; got {semvers}')
    try:
        cff_text = (core_root/'CITATION.cff').read_text(encoding='utf-8')
        import re
        m = re.search(r'^version:\s*(.+)$', cff_text, flags=re.M)
        if m and m.group(1).strip() != manifest_ver:
            errors.append(f'CITATION/version mismatch :: CITATION.cff version {m.group(1).strip()} != manifest package_version {manifest_ver}')
    except Exception as exc:
        errors.append(f'CITATION/read failure :: {exc}')

    dimensions_obj = load_json(core_root/'layer1_ontology'/'um_dimensions_ontology.v1.json')
    dimensions = {x['dimension_id'] for x in dimensions_obj['dimensions']}
    dimension_constraints = load_dimension_constraints(core_root)
    controls_obj = load_json(core_root/'layer1_ontology'/'um_machine_controls_registry.v1.json')
    controls = {x['control_id']: set(x.get('values', [])) for x in controls_obj['machine_controls']}
    artifacts = {x['artifact_type_id'] for x in load_json(core_root/'layer1_ontology'/'um_artifact_types_registry.v1.json')['artifact_types']}
    vps = {x['validation_primitive_id'] for x in load_json(core_root/'layer1_ontology'/'um_validation_primitives_registry.v1.json')['validation_primitives']}
    slots = {x['edge_slot_id'] for x in load_json(core_root/'layer1_ontology'/'um_edge_slots_ontology.v1.json')['edge_slots']}
    edge_families_obj = load_json(core_root/'layer2_seed'/'um_edge_families_seed.v1.json')['edge_families']
    edge_families = {x['edge_family_id'] for x in edge_families_obj}
    option_reg = option_path_registry(core_root)

    # paradigms ontology <-> compass seed alignment
    paradigms = {p['paradigm_id']: p for p in load_json(core_root/'layer1_ontology'/'um_paradigms_ontology.v1.json')['paradigms']}
    compass_seeds = {p['paradigm_id']: p for p in load_json(core_root/'layer2_seed'/'um_paradigm_compass_seed.v1.json')['paradigm_compass_seeds']}
    if set(paradigms) != set(compass_seeds):
        errors.append(f'Paradigm alignment :: paradigm id sets differ between ontology and compass seed: {sorted(set(paradigms)^set(compass_seeds))}')
    for pid in sorted(set(paradigms) & set(compass_seeds)):
        for field in ['label','short_code','thinking_label','definition','trigger_cue','summary_tag','semantic_tags','scope_notes']:
            if paradigms[pid].get(field) != compass_seeds[pid].get(field):
                errors.append(f'Paradigm alignment :: {pid} field {field} differs between ontology and compass seed')

    defaults = load_json(core_root/'layer2_seed'/'um_paradigm_defaults_seed.v1.json')['paradigm_defaults']
    for pd in defaults:
        pd_label = f'defaults::{pd["paradigm_id"]}'
        for d in pd.get('required_dimension_ids', []):
            if d not in dimensions:
                errors.append(f'{pd_label} :: unknown required_dimension_id {d}')
        for d in pd.get('user_must_confirm_dimension_ids', []):
            if d not in dimensions:
                errors.append(f'{pd_label} :: unknown user_must_confirm_dimension_id {d}')
        for prof in pd.get('starter_profiles', []):
            label = f'defaults::{pd["paradigm_id"]}::{prof["profile_id"]}'
            selected_dim_ids = set()
            for ds in prof.get('dimension_selections', []):
                dim_id = ds['dimension_id']
                selected_dim_ids.add(dim_id)
                if dim_id not in dimensions:
                    errors.append(f'{label} :: unknown dimension_id {dim_id}')
                    continue
                known = option_reg.get(dim_id, set())
                for path in ds.get('selected_option_paths', []):
                    if tuple(path) not in known:
                        errors.append(f'{label} :: unknown option path {path} for {dim_id}')
            # ensure required dimensions are actually resolved by this starter profile
            missing_required = set(pd.get('required_dimension_ids', [])) - selected_dim_ids
            if missing_required:
                errors.append(f'{label} :: missing selections for required dimensions {sorted(missing_required)}')
            # enforce default-level selection constraints
            for constraint in pd.get('selection_constraints', []):
                enforce_constraint(selected_dim_ids, constraint, label, errors)
            # enforce any dimension-level constraints for the current paradigm
            dim_to_paradigm = {d['dimension_id']: d['paradigm_id'] for d in dimensions_obj['dimensions']}
            for dim_id, constraints in dimension_constraints.items():
                if dim_to_paradigm.get(dim_id) != pd['paradigm_id']:
                    continue
                for constraint in constraints:
                    enforce_constraint(selected_dim_ids, constraint, label, errors)
            for mc in prof.get('machine_control_settings', []):
                cid = mc['control_id']
                if cid not in controls:
                    errors.append(f'{label} :: unknown control_id {cid}')
                else:
                    val = mc.get('selected_value_id')
                    if controls[cid] and val not in controls[cid]:
                        errors.append(f'{label} :: selected_value_id {val} not allowed for control {cid}')
            reqs = prof.get('base_artifact_requirements', {})
            for bucket in ('must', 'should', 'may'):
                for a in reqs.get(bucket, []):
                    if a not in artifacts:
                        errors.append(f'{label} :: unknown artifact id {a} in {bucket}')
            vreqs = prof.get('base_validation_requirements', {})
            for bucket in ('must', 'should', 'may'):
                for v in vreqs.get(bucket, []):
                    if v not in vps:
                        errors.append(f'{label} :: unknown validation primitive {v} in {bucket}')
            for ef in prof.get('default_support_edge_shortlist', []):
                if ef not in edge_families:
                    errors.append(f'{label} :: unknown edge family {ef}')

    for ef in edge_families_obj:
        label = f'edge_family::{ef["edge_family_id"]}'
        if ef.get('edge_slot_id') not in slots:
            errors.append(f'{label} :: unknown edge slot id {ef.get("edge_slot_id")}')
        tc = ef.get('typed_contract', {})
        for bucket in ('requires_artifact_types', 'produces_artifact_types', 'optional_artifact_types'):
            for a in tc.get(bucket, []):
                if a not in artifacts:
                    errors.append(f'{label} :: unknown artifact id {a} in {bucket}')
        for v in ef.get('default_validation_primitives', []):
            vp_id = v.get('vp_id') if isinstance(v, dict) else v
            if vp_id not in vps:
                errors.append(f'{label} :: unknown validation primitive {vp_id}')

    if errors:
        print('Core package validation failed with the following issues:')
        for err in errors:
            print(' -', err)
        sys.exit(1)
    print('Core package validated successfully.')


if __name__ == '__main__':
    main()
