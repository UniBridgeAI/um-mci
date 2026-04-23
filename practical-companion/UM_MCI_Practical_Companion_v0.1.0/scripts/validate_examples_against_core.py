#!/usr/bin/env python3
import argparse, json, pathlib, sys, warnings, re
warnings.filterwarnings("ignore", category=DeprecationWarning)
from jsonschema import Draft202012Validator, RefResolver, FormatChecker


def load_json(p):
    return json.loads(pathlib.Path(p).read_text(encoding="utf-8"))


def is_external_ref(ref):
    if not isinstance(ref, str):
        return False
    return '://' in ref or ref.startswith('doi:') or re.match(r'^10\.\d{4,9}/', ref) is not None


def build_store(*schema_roots):
    store = {}
    for root in schema_roots:
        for path in pathlib.Path(root).rglob('*.json'):
            try:
                obj = load_json(path)
            except Exception:
                continue
            if isinstance(obj, dict) and '$id' in obj:
                store[obj['$id']] = obj
    return store


def make_validator(schema_path, store):
    schema = load_json(schema_path)
    resolver = RefResolver(base_uri=schema_path.resolve().parent.as_uri()+'/', referrer=schema, store=store)
    return Draft202012Validator(schema, resolver=resolver, format_checker=FormatChecker())


def collect_schema_errors(validator, instance, label):
    out = []
    for e in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
        loc = '/'.join(str(x) for x in e.path) or '<root>'
        out.append(f'{label} :: {loc}: {e.message}')
    return out


def iter_json_files(root):
    root = pathlib.Path(root)
    return sorted(root.glob('*.json')) if root.exists() else []


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
        out |= collect_option_paths(opt.get('children', []), path)
    return out


def option_path_registry(core_root):
    seeds = load_json(core_root/'layer2_seed'/'um_paradigm_compass_seed.v1.json')['paradigm_compass_seeds']
    reg = {}
    for seed in seeds:
        for d in seed.get('dimensions', []):
            for dim in iter_dimension_node(d):
                reg[dim['dimension_id']] = collect_option_paths(dim.get('options', []))
    return reg


def collect_core_ids(core_root):
    ctx = load_json(core_root/'layer1_ontology'/'um_context_ontology.v1.json')
    dims = load_json(core_root/'layer1_ontology'/'um_dimensions_ontology.v1.json')['dimensions']
    controls = load_json(core_root/'layer1_ontology'/'um_machine_controls_registry.v1.json')['machine_controls']
    edge_slots = load_json(core_root/'layer1_ontology'/'um_edge_slots_ontology.v1.json')['edge_slots']
    edge_families = load_json(core_root/'layer2_seed'/'um_edge_families_seed.v1.json')['edge_families']
    defaults = load_json(core_root/'layer2_seed'/'um_paradigm_defaults_seed.v1.json')['paradigm_defaults']
    return {
        'paradigm_ids': {x['paradigm_id'] for x in load_json(core_root/'layer1_ontology'/'um_paradigms_ontology.v1.json')['paradigms']},
        'dimension_ids': {x['dimension_id'] for x in dims},
        'dimension_to_paradigm': {x['dimension_id']: x['paradigm_id'] for x in dims},
        'artifact_ids': {x['artifact_type_id'] for x in load_json(core_root/'layer1_ontology'/'um_artifact_types_registry.v1.json')['artifact_types']},
        'vp_ids': {x['validation_primitive_id'] for x in load_json(core_root/'layer1_ontology'/'um_validation_primitives_registry.v1.json')['validation_primitives']},
        'edge_ids': {x['edge_family_id'] for x in edge_families},
        'edge_family_to_slot': {x['edge_family_id']: x.get('edge_slot_id') for x in edge_families},
        'slot_map': {x['edge_slot_id']: x for x in edge_slots},
        'slot_ids': {x['edge_slot_id'] for x in edge_slots},
        'control_ids': {x['control_id'] for x in controls},
        'control_values': {x['control_id']: set(x.get('values', [])) for x in controls},
        'tension_ids': {x['dimension_id'] for x in load_json(core_root/'layer1_ontology'/'um_operational_tensions_ontology.v1.json')['tension_dimensions']},
        'gov_ctx_ids': {x['dimension_id'] for x in ctx['governance_context_dimensions']},
        'aff_ctx_ids': {x['dimension_id'] for x in ctx['affordance_context_dimensions']},
        'defaults_profiles': {pd['paradigm_id']: {p['profile_id'] for p in pd.get('starter_profiles', [])} for pd in defaults},
    }


def check_version_pin(pin, expected_name, expected_semver, expected_layer1, expected_layer2, label, errors):
    if pin is None:
        errors.append(f'{label} :: missing package_version_pin')
        return
    for key, expected in [
        ('package_name', expected_name),
        ('package_semver', expected_semver),
        ('layer1_registry_version', expected_layer1),
        ('layer2_seed_version', expected_layer2),
    ]:
        if pin.get(key) != expected:
            errors.append(f'{label} :: {key} pin {pin.get(key)} != core {expected}')


def check_option_paths(dim_id, selected_paths, opt_reg, label, errors):
    if dim_id not in opt_reg:
        errors.append(f'{label} :: unknown dimension_id {dim_id}')
        return
    for path in selected_paths:
        if tuple(path) not in opt_reg[dim_id]:
            errors.append(f'{label} :: unknown option path {path} for {dim_id}')


def check_reqset(reqset, allowed, label, kind, errors):
    for bucket in ('must', 'should', 'may', 'waived'):
        for item in (reqset or {}).get(bucket, []):
            if item not in allowed:
                errors.append(f'{label} :: unknown {kind} {item} in {bucket}')


def check_tension_belief(tb, label, ids, errors):
    for b in (tb or {}).get('beliefs', []):
        tid = b.get('dimension_id')
        if tid not in ids['tension_ids']:
            errors.append(f'{label} :: unknown tension dimension_id {tid}')


def check_context_keys(ctx, allowed, label, context_name, errors):
    for key in (ctx or {}).keys():
        if key == 'extensions':
            continue
        if key not in allowed:
            errors.append(f'{label} :: unknown {context_name} key {key}')




def check_edge_role_in_stage(ei, base, label, ids, errors):
    """Check that a stage-local edge role is compatible with edge direction and the stage base paradigm."""
    ef = ei.get('edge_family_id')
    slot_id = ids['edge_family_to_slot'].get(ef)
    slot = ids['slot_map'].get(slot_id, {})
    source = slot.get('from_paradigm_id')
    target = slot.get('to_paradigm_id')
    role = ei.get('edge_role_in_stage')
    if not role:
        errors.append(f'{label} :: edge_role_in_stage is required for shared companion stage records')
        return
    if not source or not target or base not in ids.get('paradigm_ids', set()):
        return
    if target == base and source != base:
        if role not in {'incoming_support', 'internal_composition'}:
            errors.append(f'{label} :: edge_role_in_stage {role} is inconsistent with incoming edge {source} -> {target} into base {base}')
    elif source == base and target != base:
        if role not in {'outgoing_preparation', 'cross_stage_link'}:
            errors.append(f'{label} :: edge_role_in_stage {role} is inconsistent with outgoing edge {source} -> {target} from base {base}')
    elif source == base and target == base:
        if role != 'internal_composition':
            errors.append(f'{label} :: self/internal edge should use edge_role_in_stage=internal_composition')
    else:
        if role != 'cross_stage_link':
            errors.append(f'{label} :: edge {source} -> {target} is neither incoming to nor outgoing from base {base}; use edge_role_in_stage=cross_stage_link or move it to a linked stage')

def validate_stage_like(obj, label, ids, opt_reg, errors):
    base = obj.get('base_paradigm_id')
    if base not in ids['paradigm_ids']:
        errors.append(f'{label} :: unknown base_paradigm_id {base}')
    route = obj.get('route', {})
    base_profile = route.get('base_profile_id')
    if base_profile and base_profile not in {'custom', 'none', 'manual'} and base_profile not in ids['defaults_profiles'].get(base, set()):
        errors.append(f'{label} :: base_profile_id {base_profile} is not defined for {base}')

    for ds in route.get('dimension_selections', []):
        dim_id = ds['dimension_id']
        check_option_paths(dim_id, ds['selected_option_paths'], opt_reg, label, errors)
        if ids['dimension_to_paradigm'].get(dim_id) != base:
            errors.append(f'{label} :: dimension {dim_id} belongs to {ids["dimension_to_paradigm"].get(dim_id)}, not base paradigm {base}')

    for mc in route.get('machine_control_settings', []):
        cid = mc['control_id']
        if cid not in ids['control_ids']:
            errors.append(f'{label} :: unknown control_id {cid}')
        else:
            sel = mc.get('selected_value_id')
            allowed = ids['control_values'].get(cid, set())
            if allowed and sel not in allowed:
                errors.append(f'{label} :: invalid selected_value_id {sel} for control {cid}')

    for art in obj.get('artifacts', []):
        if art['artifact_type_id'] not in ids['artifact_ids']:
            errors.append(f'{label} :: unknown artifact_type_id {art["artifact_type_id"]}')
    for vp in obj.get('validations', []):
        if vp['vp_id'] not in ids['vp_ids']:
            errors.append(f'{label} :: unknown vp_id {vp["vp_id"]}')

    for ei in route.get('supporting_edge_instances', []):
        ef = ei['edge_family_id']
        if ef not in ids['edge_ids']:
            errors.append(f'{label} :: unknown edge_family_id {ef}')
        if 'edge_slot_id' in ei:
            slot = ei['edge_slot_id']
            if slot not in ids['slot_ids']:
                errors.append(f'{label} :: unknown edge_slot_id {slot}')
            elif ef in ids['edge_family_to_slot'] and ids['edge_family_to_slot'][ef] != slot:
                errors.append(f'{label} :: edge_family_id {ef} belongs to slot {ids["edge_family_to_slot"][ef]}, not {slot}')
        if ef in ids['edge_ids']:
            check_edge_role_in_stage(ei, base, label, ids, errors)

    check_reqset(obj.get('validation_plan', {}), ids['vp_ids'], label, 'validation primitive', errors)
    check_tension_belief(obj.get('tension_pre'), label+'::tension_pre', ids, errors)
    check_tension_belief(obj.get('tension_post'), label+'::tension_post', ids, errors)
    check_context_keys(obj.get('governance_context_override'), ids['gov_ctx_ids'], label, 'governance context', errors)
    check_context_keys(obj.get('affordance_context_override'), ids['aff_ctx_ids'], label, 'affordance context', errors)

    rs = obj.get('resolution_snapshot', {})
    check_reqset(rs.get('artifact_requirements', {}), ids['artifact_ids'], label+'::resolution_snapshot', 'artifact type', errors)
    check_reqset(rs.get('validation_requirements', {}), ids['vp_ids'], label+'::resolution_snapshot', 'validation primitive', errors)
    for ef in rs.get('applied_edge_families', []):
        if ef not in ids['edge_ids']:
            errors.append(f'{label} :: unknown resolution_snapshot.applied_edge_family {ef}')
    for ds in rs.get('applied_dimension_selections', []):
        dim_id = ds['dimension_id']
        check_option_paths(dim_id, ds['selected_option_paths'], opt_reg, label+'::resolution_snapshot', errors)
        if ids['dimension_to_paradigm'].get(dim_id) != base:
            errors.append(f'{label} :: resolution_snapshot dimension {dim_id} belongs to {ids["dimension_to_paradigm"].get(dim_id)}, not base paradigm {base}')
    for mc in rs.get('applied_machine_controls', []):
        cid = mc['control_id']
        if cid not in ids['control_ids']:
            errors.append(f'{label} :: unknown resolution_snapshot control_id {cid}')
        else:
            sel = mc.get('selected_value_id')
            allowed = ids['control_values'].get(cid, set())
            if allowed and sel not in allowed:
                errors.append(f'{label} :: invalid resolution_snapshot selected_value_id {sel} for control {cid}')


def local_ref_exists(comp_root, ref):
    if not isinstance(ref, str):
        return True
    if is_external_ref(ref):
        return True
    return (comp_root/ref).exists()


def validate_stage_links(meta_obj, label, errors):
    stage_ids = {st.get('stage_id') for st in meta_obj.get('stages', [])}
    order = {st.get('stage_id'): st.get('stage_order') for st in meta_obj.get('stages', [])}
    for link in meta_obj.get('stage_links', []):
        f = link.get('from_stage_id')
        t = link.get('to_stage_id')
        rel = link.get('relation')
        if f not in stage_ids:
            errors.append(f'{label} :: stage_link from_stage_id {f} does not exist')
        if t not in stage_ids:
            errors.append(f'{label} :: stage_link to_stage_id {t} does not exist')
        if f == t:
            errors.append(f'{label} :: stage_link from_stage_id and to_stage_id must differ ({f})')
        if rel in {'precedes', 'feeds'} and f in order and t in order and order[f] is not None and order[t] is not None and order[f] > order[t]:
            errors.append(f'{label} :: stage_link {rel} has from_stage order after to_stage order ({f}->{t})')


def iter_proposals(comp_root):
    roots = [
        comp_root/'governance_proposals'/'examples',
        comp_root/'governance_proposals'/'proposals',
        comp_root/'examples'/'governance_proposals',  # legacy location, if present
    ]
    out = []
    for root in roots:
        out.extend(iter_json_files(root))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--core', '--core-root', dest='core_root', required=True)
    ap.add_argument('--companion', '--companion-root', dest='companion_root', required=True)
    args = ap.parse_args()

    core_root = pathlib.Path(args.core_root)
    companion_root = pathlib.Path(args.companion_root)

    store = build_store(core_root/'schemas', companion_root/'retrospective_extraction'/'schemas', companion_root/'signature_library'/'schemas')
    stage_v = make_validator(core_root/'schemas'/'um_stage_record.schema.v1.json', store)
    meta_v = make_validator(core_root/'schemas'/'um_meta_run_record.schema.v1.json', store)
    gov_v = make_validator(core_root/'schemas'/'um_governance_proposal.schema.v1.json', store)
    retro_v = make_validator(companion_root/'retrospective_extraction'/'schemas'/'retrospective_case_record.schema.v1.json', store)
    sig_v = make_validator(companion_root/'signature_library'/'schemas'/'edge_signature_seed.schema.v1.json', store)

    ids = collect_core_ids(core_root)
    opt_reg = option_path_registry(core_root)
    manifest = load_json(core_root/'MANIFEST.json')
    expected_name = manifest.get('package_name')
    expected_semver = manifest.get('package_version')
    expected_layer1 = manifest.get('layer1_registry_version', 'v1')
    expected_layer2 = manifest.get('layer2_seed_version', 'v1')
    errors = []

    standalone_by_id = {}
    for path in iter_json_files(companion_root/'examples'/'stage_records'):
        obj = load_json(path)
        sid = obj.get('stage_id')
        if sid in standalone_by_id:
            errors.append(f'{path} :: duplicate standalone stage_id {sid}')
        else:
            standalone_by_id[sid] = obj
        errors.extend(collect_schema_errors(stage_v, obj, str(path)))
        check_version_pin(obj.get('package_version_pin'), expected_name, expected_semver, expected_layer1, expected_layer2, str(path), errors)
        validate_stage_like(obj, str(path), ids, opt_reg, errors)

    for path in iter_json_files(companion_root/'examples'/'meta_runs'):
        obj = load_json(path)
        errors.extend(collect_schema_errors(meta_v, obj, str(path)))
        check_version_pin(obj.get('package_version_pin'), expected_name, expected_semver, expected_layer1, expected_layer2, str(path), errors)
        check_tension_belief(obj.get('initial_tension_belief'), str(path)+'::initial_tension_belief', ids, errors)
        check_context_keys(obj.get('governance_context'), ids['gov_ctx_ids'], str(path), 'governance context', errors)
        check_context_keys(obj.get('affordance_context'), ids['aff_ctx_ids'], str(path), 'affordance context', errors)
        validate_stage_links(obj, str(path), errors)
        seen_stage_ids = set()
        for st in obj.get('stages', []):
            sid_tmp = st.get('stage_id')
            if sid_tmp in seen_stage_ids:
                errors.append(f'{path} :: duplicate embedded stage_id {sid_tmp}')
            seen_stage_ids.add(sid_tmp)
            slabel = f'{path}::stage::{st.get("stage_id")}'
            check_version_pin(st.get('package_version_pin'), expected_name, expected_semver, expected_layer1, expected_layer2, slabel, errors)
            validate_stage_like(st, slabel, ids, opt_reg, errors)
            sid = st.get('stage_id')
            if sid in standalone_by_id and standalone_by_id[sid] != st:
                errors.append(f'{path}::stage::{sid} :: embedded stage differs from standalone stage record')

    for path in iter_proposals(companion_root):
        obj = load_json(path)
        errors.extend(collect_schema_errors(gov_v, obj, str(path)))
        check_version_pin(obj.get('package_version_pin'), expected_name, expected_semver, expected_layer1, expected_layer2, str(path), errors)
        if not obj.get('targets'):
            errors.append(f'{path} :: targets must not be empty')
        if not obj.get('payload', {}).get('requested_action'):
            errors.append(f'{path} :: payload.requested_action is required')
        if not obj.get('evidence_pointers'):
            errors.append(f'{path} :: evidence_pointers must not be empty')
        for ref in obj.get('evidence_pointers', []):
            if not local_ref_exists(companion_root, ref):
                errors.append(f'{path} :: evidence pointer does not exist locally: {ref}')
        edge = obj.get('payload', {}).get('edge_family_id')
        if edge and edge not in ids['edge_ids']:
            errors.append(f'{path} :: unknown payload.edge_family_id {edge}')

    for path in iter_json_files(companion_root/'examples'/'retrospective_cases'):
        obj = load_json(path)
        errors.extend(collect_schema_errors(retro_v, obj, str(path)))
        check_version_pin(obj.get('package_version_pin'), expected_name, expected_semver, expected_layer1, expected_layer2, str(path), errors)
        check_context_keys(obj.get('governance_context_hypothesis'), ids['gov_ctx_ids'], str(path), 'governance context', errors)
        check_context_keys(obj.get('affordance_context_hypothesis'), ids['aff_ctx_ids'], str(path), 'affordance context', errors)
        for st in obj.get('stage_hypotheses', []):
            base = st.get('base_paradigm_id')
            if base not in ids['paradigm_ids']:
                errors.append(f'{path} :: unknown base_paradigm_id {base}')
            for dh in st.get('dimension_hypotheses', []):
                dim = dh['dimension_id']
                check_option_paths(dim, dh['selected_option_paths'], opt_reg, str(path), errors)
                if ids['dimension_to_paradigm'].get(dim) != base:
                    errors.append(f'{path} :: dimension hypothesis {dim} belongs to {ids["dimension_to_paradigm"].get(dim)}, not stage base {base}')
            for edge in st.get('supporting_edge_family_ids', []):
                if edge not in ids['edge_ids']:
                    errors.append(f'{path} :: unknown supporting edge family {edge}')
            for art in st.get('artifact_hypotheses', []):
                if art not in ids['artifact_ids']:
                    errors.append(f'{path} :: unknown artifact hypothesis {art}')
            for vp in st.get('validation_hypotheses', []):
                if vp not in ids['vp_ids']:
                    errors.append(f'{path} :: unknown validation hypothesis {vp}')
            for ten in st.get('tension_hypotheses', []):
                if ten not in ids['tension_ids']:
                    errors.append(f'{path} :: unknown tension hypothesis {ten}')

    for sig_dir in [companion_root/'signature_library'/'starter_seeds', companion_root/'signature_library'/'contributed_seeds']:
        for path in iter_json_files(sig_dir):
            obj = load_json(path)
            errors.extend(collect_schema_errors(sig_v, obj, str(path)))
            check_version_pin(obj.get('package_version_pin'), expected_name, expected_semver, expected_layer1, expected_layer2, str(path), errors)
            edge = obj.get('edge_family_id')
            if edge not in ids['edge_ids']:
                errors.append(f'{path} :: unknown edge_family_id {edge}')
            stage_pattern = obj.get('stage_pattern', {})
            base = stage_pattern.get('base_paradigm_id')
            support = stage_pattern.get('supporting_paradigm_id')
            if base and base not in ids['paradigm_ids']:
                errors.append(f'{path} :: unknown base_paradigm_id {base}')
            if support and support not in ids['paradigm_ids']:
                errors.append(f'{path} :: unknown supporting_paradigm_id {support}')
            slot = ids['slot_map'].get(ids['edge_family_to_slot'].get(edge), {})
            if base and slot.get('to_paradigm_id') and base != slot.get('to_paradigm_id'):
                errors.append(f'{path} :: base_paradigm_id {base} does not match edge target {slot.get("to_paradigm_id")}')
            if support and slot.get('from_paradigm_id') and support != slot.get('from_paradigm_id'):
                errors.append(f'{path} :: supporting_paradigm_id {support} does not match edge source {slot.get("from_paradigm_id")}')
            for hint in stage_pattern.get('dimension_hints', []):
                dim = hint.get('dimension_id')
                check_option_paths(dim, hint.get('selected_option_paths', []), opt_reg, str(path), errors)
                if ids['dimension_to_paradigm'].get(dim) not in {base, support}:
                    errors.append(f'{path} :: dimension_hint {dim} belongs to {ids["dimension_to_paradigm"].get(dim)}, not base/support paradigms {base}/{support}')
            for art in obj.get('required_artifact_hints', []) + obj.get('optional_artifact_hints', []):
                if art not in ids['artifact_ids']:
                    errors.append(f'{path} :: unknown artifact hint {art}')
            for vp in obj.get('required_validation_hints', []):
                if vp not in ids['vp_ids']:
                    errors.append(f'{path} :: unknown validation hint {vp}')

    loc_path = companion_root/'core_integration'/'core_locator.example.json'
    if loc_path.exists():
        loc = load_json(loc_path)
        if loc.get('expected_package_semver') != expected_semver:
            errors.append(f'{loc_path} :: expected_package_semver {loc.get("expected_package_semver")} != core version {expected_semver}')
        if loc.get('expected_package_name') and loc.get('expected_package_name') != expected_name:
            errors.append(f'{loc_path} :: expected_package_name {loc.get("expected_package_name")} != core name {expected_name}')

    if errors:
        print('Companion validation failed with the following issues:')
        for err in errors:
            print(' -', err)
        sys.exit(1)
    print('All companion examples and practical objects validated against the core package.')


if __name__ == '__main__':
    main()
