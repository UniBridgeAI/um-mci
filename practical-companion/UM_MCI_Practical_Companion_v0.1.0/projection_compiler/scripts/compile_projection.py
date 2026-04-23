#!/usr/bin/env python3
import argparse
import json
import pathlib


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def iter_dimension_node(node):
    yield node
    for sd in node.get('subdimensions', []):
        yield from iter_dimension_node(sd)
    for ax in node.get('associated_axes', []):
        if isinstance(ax, dict):
            yield from iter_dimension_node(ax)


def iter_dimensions(seed):
    for d in seed.get('dimensions', []):
        yield from iter_dimension_node(d)


def find_dimension(seed, dimension_id):
    for d in iter_dimensions(seed):
        if d['dimension_id'] == dimension_id:
            return d
    return None


def build_option_index(dim):
    out = {}

    def walk(options, prefix=()):
        for opt in options:
            path = prefix + (opt['value_id'],)
            out[path] = {
                'value_id': opt['value_id'],
                'label': opt.get('label'),
                'tag': opt.get('tag'),
                'definition': opt.get('definition'),
                'children': [],
                'path': list(path),
            }
            children = opt.get('children', [])
            if children:
                for child in children:
                    out[path]['children'].append(path + (child['value_id'],))
                walk(children, path)

    walk(dim.get('options', []))
    return out


def descendants(opt_index, path_tuple, mode):
    if path_tuple not in opt_index or mode == 'none':
        return []
    frontier = list(opt_index[path_tuple].get('children', []))
    out = []
    while frontier:
        x = frontier.pop(0)
        out.append(x)
        if mode == 'all_descendants':
            frontier.extend(opt_index.get(x, {}).get('children', []))
    return out


def strip_none(x):
    if isinstance(x, dict):
        return {k: strip_none(v) for k, v in x.items() if v is not None}
    if isinstance(x, list):
        return [strip_none(v) for v in x]
    return x


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--core-root', required=True)
    ap.add_argument('--profile', required=True)
    ap.add_argument('--paradigm-id', required=True)
    ap.add_argument('--profile-id', default='starter_baseline')
    ap.add_argument('--output', required=True)
    args = ap.parse_args()

    core_root = pathlib.Path(args.core_root)
    profile = load_json(args.profile)
    compass = load_json(core_root / 'layer2_seed' / 'um_paradigm_compass_seed.v1.json')['paradigm_compass_seeds']
    defaults = load_json(core_root / 'layer2_seed' / 'um_paradigm_defaults_seed.v1.json')['paradigm_defaults']
    paradigms = load_json(core_root / 'layer1_ontology' / 'um_paradigms_ontology.v1.json')['paradigms']
    edges = load_json(core_root / 'layer2_seed' / 'um_edge_families_seed.v1.json')['edge_families']

    p_seed = next(x for x in compass if x['paradigm_id'] == args.paradigm_id)
    p_def = next(x for x in defaults if x['paradigm_id'] == args.paradigm_id)
    p_meta = next(x for x in paradigms if x['paradigm_id'] == args.paradigm_id)
    starter = next(x for x in p_def['starter_profiles'] if x['profile_id'] == args.profile_id)

    out = {
        'projection_profile_id': profile['profile_id'],
        'paradigm_id': args.paradigm_id,
        'paradigm_label': p_meta['label'],
        'paradigm_definition': p_meta.get('definition') if profile.get('include_definitions') else None,
        'starter_profile_id': starter['profile_id'],
        'dimension_views': [],
        'machine_controls': starter.get('machine_control_settings', []) if profile.get('include_machine_controls') else None,
        'artifact_requirements': starter.get('base_artifact_requirements') if profile.get('include_artifact_requirements') else None,
        'validation_requirements': starter.get('base_validation_requirements') if profile.get('include_validation_requirements') else None,
        'support_edge_shortlist': starter.get('default_support_edge_shortlist', []) if profile.get('include_support_edges') else None,
        'support_edge_hints': []
    }

    for sel in starter.get('dimension_selections', []):
        dim = find_dimension(p_seed, sel['dimension_id'])
        if dim is None:
            continue
        opt_index = build_option_index(dim)
        expanded = []
        for path_list in sel['selected_option_paths']:
            t = tuple(path_list)
            expanded.append(t)
            if profile.get('include_children_for_selected'):
                expanded.extend(descendants(opt_index, t, profile.get('selection_expansion', 'none')))
        seen = []
        for t in expanded:
            if t not in seen:
                seen.append(t)
        values = []
        for t in seen:
            rec = opt_index.get(t, {'value_id': t[-1], 'path': list(t)})
            item = {'value_id': rec.get('value_id'), 'label': rec.get('label')}
            if profile.get('include_tags'):
                item['tag'] = rec.get('tag')
            if profile.get('include_definitions'):
                item['definition'] = rec.get('definition')
            if profile.get('include_selected_path'):
                item['path'] = rec.get('path')
            values.append(item)
        dim_view = {
            'dimension_id': dim['dimension_id'],
            'label': dim.get('label'),
            'definition': dim.get('definition') if profile.get('include_definitions') else None,
            'selected_values_expanded': values
        }
        out['dimension_views'].append(dim_view)

    if profile.get('include_support_edges'):
        for edge_family_id in starter.get('default_support_edge_shortlist', []):
            ef = next((x for x in edges if x['edge_family_id'] == edge_family_id), None)
            if ef is None:
                continue
            item = {
                'edge_family_id': ef['edge_family_id'],
                'relation_role': ef['relation_role'],
                'operator_family': ef['operator_family']
            }
            if profile.get('include_definitions'):
                item['mechanism_summary'] = ef.get('mechanism_summary')
            if profile.get('include_failure_hints'):
                item['typical_failure_modes'] = ef.get('typical_failure_modes', [])
            out['support_edge_hints'].append(item)

    out = strip_none(out)
    out_path = pathlib.Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write('\n')


if __name__ == '__main__':
    main()
