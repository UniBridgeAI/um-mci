#!/usr/bin/env python3
# This implementation is retained for backward compatibility; public docs prefer the validate_* wrapper.
import argparse, json, pathlib, warnings, re
warnings.filterwarnings('ignore', category=DeprecationWarning)
from jsonschema import Draft202012Validator, RefResolver, FormatChecker


def load_json(p):
    return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))


def is_external_ref(ref):
    if not isinstance(ref, str):
        return False
    return '://' in ref or ref.startswith('doi:') or re.match(r'^10\.\d{4,9}/', ref) is not None


def build_store(schema_root):
    store = {}
    for path in pathlib.Path(schema_root).rglob('*.json'):
        obj = load_json(path)
        if '$id' in obj:
            store[obj['$id']] = obj
    return store


def local_ref_exists(comp_root, ref):
    if not isinstance(ref, str):
        return True
    if is_external_ref(ref):
        return True
    return (comp_root/ref).exists()


def iter_proposals(comp_root):
    roots = [
        comp_root/'governance_proposals'/'examples',
        comp_root/'governance_proposals'/'proposals',
        comp_root/'examples'/'governance_proposals',
    ]
    out = []
    for root in roots:
        if root.exists():
            out.extend(sorted(root.glob('*.json')))
    return out



def extract_stage_edges(stage_obj):
    route = stage_obj.get('route', {})
    return {ei.get('edge_family_id') for ei in route.get('supporting_edge_instances', []) if ei.get('edge_family_id')}


def extract_evidence_edges(comp_root, ref):
    edges = set()
    if not isinstance(ref, str) or is_external_ref(ref):
        return edges
    p = comp_root / ref
    if not p.exists() or p.suffix != '.json':
        return edges
    try:
        obj = load_json(p)
    except Exception:
        return edges
    if 'route' in obj:
        edges |= extract_stage_edges(obj)
    for st in obj.get('stages', []):
        edges |= extract_stage_edges(st)
    for st in obj.get('stage_hypotheses', []):
        for ef in st.get('supporting_edge_family_ids', []):
            if ef:
                edges.add(ef)
    return edges

def main():
    ap = argparse.ArgumentParser(description='Validate governance proposals against the released core.')
    ap.add_argument('--core-root', required=True)
    ap.add_argument('--companion-root', required=True)
    args = ap.parse_args()
    core = pathlib.Path(args.core_root)
    comp = pathlib.Path(args.companion_root)
    schema_path = core/'schemas'/'um_governance_proposal.schema.v1.json'
    schema = load_json(schema_path)
    resolver = RefResolver(base_uri=schema_path.resolve().parent.as_uri()+'/', referrer=schema, store=build_store(core/'schemas'))
    validator = Draft202012Validator(schema, resolver=resolver, format_checker=FormatChecker())
    manifest = load_json(core/'MANIFEST.json')
    core_edge_ids = {x['edge_family_id'] for x in load_json(core/'layer2_seed'/'um_edge_families_seed.v1.json')['edge_families']}
    errors = []

    for path in iter_proposals(comp):
        inst = load_json(path)
        for err in validator.iter_errors(inst):
            loc = '/'.join(str(x) for x in err.path) or '<root>'
            errors.append(f'{path} :: {loc}: {err.message}')
        if not inst.get('targets'):
            errors.append(f'{path} :: targets must not be empty for governance proposals')
        if not inst.get('payload', {}).get('requested_action'):
            errors.append(f'{path} :: payload.requested_action is required for governance proposals')
        if not inst.get('evidence_pointers'):
            errors.append(f'{path} :: evidence_pointers must not be empty for governance proposals')
        evidence = set(inst.get('evidence_pointers', []))
        for ref in evidence:
            if not local_ref_exists(comp, ref):
                errors.append(f'{path} :: evidence pointer does not exist locally: {ref}')
        targets = set(inst.get('targets', []))
        overlap = sorted(t for t in targets if t in evidence)
        if overlap:
            errors.append(f'{path} :: targets should not also be listed as evidence_pointers: {overlap}')
        for target in targets:
            if isinstance(target, str) and not is_external_ref(target) and target.endswith('.json'):
                if not local_ref_exists(comp, target):
                    errors.append(f'{path} :: target file does not exist locally: {target}')
        pin = inst.get('package_version_pin', {})
        for key, expected in [
            ('package_name', manifest.get('package_name')),
            ('package_semver', manifest.get('package_version')),
            ('layer1_registry_version', manifest.get('layer1_registry_version', 'v1')),
            ('layer2_seed_version', manifest.get('layer2_seed_version', 'v1')),
        ]:
            if pin.get(key) != expected:
                errors.append(f'{path} :: {key} pin {pin.get(key)} != core {expected}')
        edge = inst.get('payload', {}).get('edge_family_id')
        if edge:
            if not edge.startswith('UM.EDGE_FAMILY.'):
                errors.append(f'{path} :: payload.edge_family_id must be a released UM.EDGE_FAMILY.* ID, got {edge}')
            elif edge not in core_edge_ids:
                errors.append(f'{path} :: unknown payload.edge_family_id {edge}')
        if edge:
            for target in inst.get('targets', []):
                if isinstance(target, str) and target.endswith('.json') and local_ref_exists(comp, target):
                    try:
                        target_obj = load_json(comp/target)
                    except Exception:
                        continue
                    target_edge = target_obj.get('edge_family_id')
                    if target_edge and target_edge != edge:
                        errors.append(f'{path} :: target {target} edge_family_id {target_edge} != payload.edge_family_id {edge}')

            local_evidence_edges = set()
            local_evidence_refs = []
            parseable_local_evidence_count = 0
            for ref in inst.get('evidence_pointers', []):
                if isinstance(ref, str) and not is_external_ref(ref):
                    local_evidence_refs.append(ref)
                extracted = extract_evidence_edges(comp, ref)
                if extracted:
                    parseable_local_evidence_count += 1
                local_evidence_edges |= extracted
            if local_evidence_refs and parseable_local_evidence_count == 0:
                errors.append(f'{path} :: local evidence_pointers exist but none expose machine-readable edge commitments')
            if local_evidence_edges and edge not in local_evidence_edges:
                errors.append(f'{path} :: payload.edge_family_id {edge} is not instantiated by any local evidence stage/meta-run')
    if errors:
        print('Governance proposal validation failed:')
        for e in errors:
            print(' -', e)
        return 1
    print('Governance proposals validated successfully.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
