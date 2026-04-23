#!/usr/bin/env python3
import argparse, collections, json, pathlib


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cases-dir', required=True)
    args = ap.parse_args()

    counts = {
        'base_paradigm_id': collections.Counter(),
        'dimension_id': collections.Counter(),
        'edge_family_id': collections.Counter(),
        'artifact_type_id': collections.Counter(),
        'vp_id': collections.Counter(),
        'tension_id': collections.Counter(),
    }

    for path in sorted(pathlib.Path(args.cases_dir).glob('*.json')):
        case = load_json(path)
        for stage in case.get('stage_hypotheses', []):
            if 'base_paradigm_id' in stage:
                counts['base_paradigm_id'][stage['base_paradigm_id']] += 1
            for item in stage.get('dimension_hypotheses', []):
                counts['dimension_id'][item['dimension_id']] += 1
            for item in stage.get('supporting_edge_family_ids', []):
                counts['edge_family_id'][item] += 1
            for item in stage.get('artifact_hypotheses', []):
                counts['artifact_type_id'][item] += 1
            for item in stage.get('validation_hypotheses', []):
                counts['vp_id'][item] += 1
            for item in stage.get('tension_hypotheses', []):
                counts['tension_id'][item] += 1

    print(json.dumps({k: dict(v) for k, v in counts.items()}, indent=2))


if __name__ == '__main__':
    main()
