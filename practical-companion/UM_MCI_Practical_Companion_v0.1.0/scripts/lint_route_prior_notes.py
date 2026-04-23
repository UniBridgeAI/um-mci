#!/usr/bin/env python3
# This implementation is retained for backward compatibility; public docs prefer the validate_* wrapper.
import argparse, json, pathlib, re
from jsonschema import Draft202012Validator, FormatChecker


def load_json(p):
    return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))


def is_external_ref(ref):
    if not isinstance(ref, str):
        return False
    return '://' in ref or ref.startswith('doi:') or re.match(r'^10\.\d{4,9}/', ref) is not None


def iter_json_files(root):
    root = pathlib.Path(root)
    return sorted(root.glob('*.json')) if root.exists() else []


def option_path_registry(core_root):
    seeds = load_json(core_root/'layer2_seed'/'um_paradigm_compass_seed.v1.json')['paradigm_compass_seeds']
    reg = {}
    def collect(options, prefix=()):
        out = set()
        for opt in options:
            path = prefix + (opt['value_id'],)
            out.add(path)
            out |= collect(opt.get('children', []), path)
        return out
    def walk_dims(dim):
        yield dim
        for sd in dim.get('subdimensions', []):
            yield from walk_dims(sd)
        for ax in dim.get('associated_axes', []):
            if isinstance(ax, dict):
                yield from walk_dims(ax)
    for seed in seeds:
        for d in seed.get('dimensions', []):
            for dim in walk_dims(d):
                reg[dim['dimension_id']] = collect(dim.get('options', []))
    return reg


def collect_core_ids(core_root):
    edge_families = load_json(core_root/'layer2_seed'/'um_edge_families_seed.v1.json')['edge_families']
    edge_slots = load_json(core_root/'layer1_ontology'/'um_edge_slots_ontology.v1.json')['edge_slots']
    return {
        'paradigm_ids': {x['paradigm_id'] for x in load_json(core_root/'layer1_ontology'/'um_paradigms_ontology.v1.json')['paradigms']},
        'dimension_ids': {x['dimension_id'] for x in load_json(core_root/'layer1_ontology'/'um_dimensions_ontology.v1.json')['dimensions']},
        'dimension_to_paradigm': {x['dimension_id']: x['paradigm_id'] for x in load_json(core_root/'layer1_ontology'/'um_dimensions_ontology.v1.json')['dimensions']},
        'edge_ids': {x['edge_family_id'] for x in edge_families},
        'edge_to_slot': {x['edge_family_id']: x.get('edge_slot_id') for x in edge_families},
        'slot_map': {x['edge_slot_id']: x for x in edge_slots},
        'tension_ids': {x['dimension_id'] for x in load_json(core_root/'layer1_ontology'/'um_operational_tensions_ontology.v1.json')['tension_dimensions']},
    }


def local_ref_exists(comp_root, ref):
    if not isinstance(ref, str):
        return True
    if is_external_ref(ref):
        return True
    return (comp_root/ref).exists()


def check_pin(pin, manifest, label, errors):
    for key, expected in [
        ('package_name', manifest.get('package_name')),
        ('package_semver', manifest.get('package_version')),
        ('layer1_registry_version', manifest.get('layer1_registry_version', 'v1')),
        ('layer2_seed_version', manifest.get('layer2_seed_version', 'v1')),
    ]:
        if (pin or {}).get(key) != expected:
            errors.append(f'{label} :: {key} pin {(pin or {}).get(key)} != core {expected}')



def extract_stage_commitments(stage_obj):
    """Return sets of (dimension_id, option_path_tuple) and edge_family_ids from a stage-like object."""
    dims = set()
    edges = set()
    route = stage_obj.get('route', {})
    for ds in route.get('dimension_selections', []):
        dim = ds.get('dimension_id')
        for op in ds.get('selected_option_paths', []):
            dims.add((dim, tuple(op)))
    for ei in route.get('supporting_edge_instances', []):
        if ei.get('edge_family_id'):
            edges.add(ei.get('edge_family_id'))
    return dims, edges


def extract_retrospective_commitments(obj):
    """Return commitments mechanically visible in retrospective case hypotheses."""
    dims = set()
    edges = set()
    for st in obj.get('stage_hypotheses', []):
        for dh in st.get('dimension_hypotheses', []):
            dim = dh.get('dimension_id')
            for op in dh.get('selected_option_paths', []):
                if dim and isinstance(op, list):
                    dims.add((dim, tuple(op)))
        for ef in st.get('supporting_edge_family_ids', []):
            if ef:
                edges.add(ef)
    return dims, edges


def extract_evidence_commitments(comp_root, ref):
    """Extract mechanically visible commitments from local stage, meta-run, or retrospective evidence objects."""
    dims = set()
    edges = set()
    if not isinstance(ref, str) or is_external_ref(ref):
        return dims, edges
    p = comp_root / ref
    if not p.exists() or p.suffix != '.json':
        return dims, edges
    try:
        obj = load_json(p)
    except Exception:
        return dims, edges
    if 'route' in obj:
        d, e = extract_stage_commitments(obj)
        dims |= d; edges |= e
    for st in obj.get('stages', []):
        d, e = extract_stage_commitments(st)
        dims |= d; edges |= e
    if 'stage_hypotheses' in obj:
        d, e = extract_retrospective_commitments(obj)
        dims |= d; edges |= e
    return dims, edges


def external_evidence_marked(inst):
    """Return True when external-only evidence is explicitly marked as not mechanically parsed."""
    notes = str(inst.get('notes', '')).lower()
    if 'external' in notes and ('unverified' in notes or 'unchecked' in notes or 'not mechanically parsed' in notes):
        return True
    ext = inst.get('extensions', {})
    if isinstance(ext, dict):
        review = ext.get('evidence_review') or ext.get('um_mci.evidence_review') or {}
        if isinstance(review, dict) and review.get('external_evidence_unchecked') is True:
            return True
    return False

def main():
    ap = argparse.ArgumentParser(description='Validate learned route prior notes against the released core.')
    ap.add_argument('--companion-root', required=True)
    ap.add_argument('--core-root', required=False)
    args = ap.parse_args()
    root = pathlib.Path(args.companion_root)
    schema = load_json(root/'learned_priors'/'schemas'/'route_prior_note.schema.v1.json')
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    core_ids = option_reg = manifest = None
    if args.core_root:
        core = pathlib.Path(args.core_root)
        core_ids = collect_core_ids(core)
        option_reg = option_path_registry(core)
        manifest = load_json(core/'MANIFEST.json')

    paths = iter_json_files(root/'learned_priors'/'starter_notes') + iter_json_files(root/'learned_priors'/'contributed_notes')
    for path in paths:
        inst = load_json(path)
        for err in validator.iter_errors(inst):
            loc = '/'.join(str(x) for x in err.path) or '<root>'
            errors.append(f'{path} :: {loc}: {err.message}')
        if not inst.get('target_ids'):
            errors.append(f'{path} :: target_ids must not be empty for shared prior notes')
        rc = inst.get('recommended_commitment', {})
        base = rc.get('base_paradigm_id')
        if not base:
            errors.append(f'{path} :: recommended_commitment.base_paradigm_id is required for shared prior notes')
        if not rc.get('selected_option_paths') and not rc.get('supporting_edge_families'):
            errors.append(f'{path} :: shared prior note must include at least one selected_option_path or supporting_edge_family')
        if not inst.get('evidence_refs'):
            errors.append(f'{path} :: evidence_refs must not be empty for shared prior notes')
        evidence_object_count = inst.get('evidence_object_count', len(inst.get('evidence_refs', [])))
        if evidence_object_count < 1:
            errors.append(f'{path} :: evidence_object_count should be at least 1 for shared prior notes')
        if 'support_count' in inst and inst.get('support_count', 0) < 1:
            errors.append(f'{path} :: legacy support_count, when present, should be at least 1')
        if 'evidence_object_count' in inst and inst.get('evidence_object_count') != len(inst.get('evidence_refs', [])):
            errors.append(f'{path} :: evidence_object_count {inst.get("evidence_object_count")} != number of evidence_refs {len(inst.get("evidence_refs", []))}')
        if 'independent_case_count' in inst and inst.get('independent_case_count') > len(inst.get('evidence_refs', [])):
            errors.append(f'{path} :: independent_case_count cannot exceed evidence object count')
        if inst.get('evidence_kind') in {'case_based', 'retrospective', 'mixed'} and inst.get('evidence_refs'):
            if inst.get('independent_case_count', 0) < 1:
                errors.append(f'{path} :: independent_case_count should be at least 1 for case-based, retrospective, or mixed evidence')
        for ref in inst.get('evidence_refs', []):
            if not local_ref_exists(root, ref):
                errors.append(f'{path} :: evidence_ref does not exist locally: {ref}')
        if core_ids is not None:
            check_pin(inst.get('package_version_pin', {}), manifest, str(path), errors)
            if base and base not in core_ids['paradigm_ids']:
                errors.append(f'{path} :: unknown base_paradigm_id {base}')
            recommended_dimension_ids = {item.get('dimension_id') for item in rc.get('selected_option_paths', []) if item.get('dimension_id')}
            recommended_edge_family_ids = set(rc.get('supporting_edge_families', []))
            allowed_targets = set()
            if base:
                allowed_targets.add(base)
            allowed_targets |= recommended_dimension_ids
            allowed_targets |= recommended_edge_family_ids
            for tid in inst.get('target_ids', []):
                if tid.startswith('UM.PARADIGM.'):
                    if tid not in core_ids['paradigm_ids']:
                        errors.append(f'{path} :: unknown paradigm target_id {tid}')
                    elif base and tid != base:
                        errors.append(f'{path} :: paradigm target_id {tid} is not aligned with base_paradigm_id {base}')
                elif tid.startswith('UM.DIM.'):
                    if tid not in core_ids['dimension_ids']:
                        errors.append(f'{path} :: unknown dimension target_id {tid}')
                    elif tid not in allowed_targets:
                        errors.append(f'{path} :: dimension target_id {tid} is valid but not aligned with recommended_commitment')
                elif tid.startswith('UM.EDGE_FAMILY.'):
                    if tid not in core_ids['edge_ids']:
                        errors.append(f'{path} :: unknown edge_family target_id {tid}')
                    elif tid not in allowed_targets:
                        errors.append(f'{path} :: edge_family target_id {tid} is valid but not aligned with recommended_commitment')
                else:
                    errors.append(f'{path} :: target_id {tid} must be a released UM paradigm, dimension, or edge-family ID')

            scope = inst.get('scope')
            selected_count = len(rc.get('selected_option_paths', []))
            edge_count = len(rc.get('supporting_edge_families', []))
            if scope == 'paradigm' and base and base not in inst.get('target_ids', []):
                errors.append(f'{path} :: paradigm scope should include base_paradigm_id in target_ids')
            if scope == 'edge_family' and edge_count < 1:
                errors.append(f'{path} :: edge_family scope requires at least one supporting_edge_family')
            if scope == 'option_path' and selected_count < 1:
                errors.append(f'{path} :: option_path scope requires at least one selected_option_path')
            if scope == 'route_pattern' and (selected_count + edge_count) < 2:
                errors.append(f'{path} :: route_pattern scope should contain multiple commitments')
            for tid in inst.get('trigger_pattern', {}).get('active_tensions', []):
                if tid not in core_ids['tension_ids']:
                    errors.append(f'{path} :: unknown tension id {tid}')
            for item in rc.get('selected_option_paths', []):
                dim = item['dimension_id']
                if dim not in option_reg:
                    errors.append(f'{path} :: unknown dimension_id {dim}')
                    continue
                if base and core_ids['dimension_to_paradigm'].get(dim) != base:
                    errors.append(f'{path} :: selected dimension {dim} belongs to {core_ids["dimension_to_paradigm"].get(dim)}, not base_paradigm_id {base}')
                if tuple(item.get('option_path', [])) not in option_reg[dim]:
                    errors.append(f'{path} :: unknown option path {item.get("option_path")} for {dim}')
            for eid in rc.get('supporting_edge_families', []):
                if eid not in core_ids['edge_ids']:
                    errors.append(f'{path} :: unknown supporting edge family {eid}')
                elif base:
                    slot = core_ids['slot_map'].get(core_ids['edge_to_slot'].get(eid), {})
                    if slot.get('to_paradigm_id') and slot.get('to_paradigm_id') != base:
                        errors.append(f'{path} :: supporting edge family {eid} targets {slot.get("to_paradigm_id")}, not base_paradigm_id {base}')

            # Weak evidence-alignment check: at least one recommended option path or edge should
            # be mechanically visible in local evidence objects. This is not a proof of sufficiency;
            # it prevents shared prior notes from citing unrelated local evidence.
            evidence_dims = set()
            evidence_edges = set()
            local_evidence_refs = []
            parseable_local_evidence_count = 0
            for ref in inst.get('evidence_refs', []):
                if isinstance(ref, str) and not is_external_ref(ref):
                    local_evidence_refs.append(ref)
                d, e = extract_evidence_commitments(root, ref)
                if d or e:
                    parseable_local_evidence_count += 1
                evidence_dims |= d
                evidence_edges |= e
            rec_dims = {(item.get('dimension_id'), tuple(item.get('option_path', []))) for item in rc.get('selected_option_paths', [])}
            rec_edges = set(rc.get('supporting_edge_families', []))
            if local_evidence_refs and rec_dims.union(rec_edges) and parseable_local_evidence_count == 0:
                errors.append(f'{path} :: local evidence_refs exist but none expose machine-readable commitments')
            if (not local_evidence_refs) and inst.get('evidence_refs') and rec_dims.union(rec_edges) and not external_evidence_marked(inst):
                errors.append(f'{path} :: evidence_refs are external-only; mark external evidence as not mechanically parsed in notes or extensions.evidence_review.external_evidence_unchecked')
            if (evidence_dims or evidence_edges) and rec_dims.union(rec_edges):
                if evidence_dims.isdisjoint(rec_dims) and evidence_edges.isdisjoint(rec_edges):
                    errors.append(f'{path} :: local evidence does not instantiate any recommended selected_option_path or supporting_edge_family')
    if errors:
        print('Route prior validation failed:')
        for e in errors:
            print(' -', e)
        return 1
    print('Route prior notes validated successfully.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
