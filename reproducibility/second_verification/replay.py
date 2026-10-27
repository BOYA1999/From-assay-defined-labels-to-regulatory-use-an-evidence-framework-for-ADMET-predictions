from collections import defaultdict
from pathlib import Path
import csv
import hashlib
import json
import math
import statistics as stats
import sys

base = Path(__file__).resolve().parent
out = Path.cwd() / 'replay_outputs'
out.mkdir(exist_ok=True)

def read(name):
    with (base / 'data' / name).open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))

def number(value):
    if value == '':
        return None, 'blank'
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None, 'non_numeric'
    return (value, 'finite') if math.isfinite(value) else (None, 'non_finite')

def ranks(values):
    locations = defaultdict(list)
    for i, value in enumerate(sorted(values), 1):
        locations[value].append(i)
    return [stats.mean(locations[value]) for value in values]

identities = read('deepdelta_identity_folds.csv')
folds = []
for fold in range(1, 11):
    train = {row['raw_smiles_sha256'] for row in identities if int(row['seed0_test_fold']) != fold}
    test = {row['raw_smiles_sha256'] for row in identities if int(row['seed0_test_fold']) == fold}
    folds.append({'seed': 0, 'fold': fold, 'train_unique_raw_smiles': len(train),
                  'test_unique_raw_smiles': len(test), 'overlap_unique_raw_smiles': len(train & test)})
deepdelta = {'records': len(identities), 'unique_raw_smiles': len({r['raw_smiles_sha256'] for r in identities}), 'folds': folds}
assert (deepdelta['records'], deepdelta['unique_raw_smiles']) == (881, 775)
assert [r['overlap_unique_raw_smiles'] for r in folds] == [19, 19, 21, 16, 18, 21, 21, 21, 21, 11]

groups = defaultdict(list)
for row in read('ppb_observed_predicted.csv'):
    groups[row['dataset'], row['model']].append(row)
ppb = []
for summary in read('ppb_reported_summaries.csv'):
    rows = groups[summary['dataset'], summary['model']]
    x = [float(row['observed_ppb_percent']) for row in rows]
    y = [float(row['predicted_ppb_percent']) for row in rows]
    sse = sum((a - b) ** 2 for a, b in zip(x, y))
    result = dict(summary, n=len(x), pearson_r_squared=stats.correlation(x, y) ** 2,
                  predictive_r_squared=1 - sse / sum((a - stats.mean(x)) ** 2 for a in x),
                  rmse_percentage_points=math.sqrt(sse / len(x)))
    assert abs(result['pearson_r_squared'] - float(summary['source_labelled_r2'])) < 1e-12
    ppb.append(result)

bile_rows = read('biliary_seven_drug_inputs.csv')
bile, mean_differences, sd_differences = [], [], []
for donor, expected, reported in [('JFC', 0.9693739833144289, 0.969), ('HUM181001B', 0.9424446736778509, 0.966)]:
    rows = [r for r in bile_rows if r['donor'] == donor]
    values = [[float(r[f'replicate_{i}']) for i in range(1, 4)] for r in rows]
    means = [stats.mean(v) for v in values]
    for row, value in zip(rows, values):
        mean_differences.append(abs(stats.mean(value) - float(row['cached_mean'])))
        sd_differences.append(abs(stats.stdev(value) - float(row['cached_sd'])))
    correlation = stats.correlation(means, [float(r['human_reference']) for r in rows])
    assert abs(correlation - expected) < 1e-12
    bile.append({'donor': donor, 'drugs': 7, 'untransformed_drug_mean_pearson_r': correlation,
                 'author_reported_r': reported, 'transformation': 'none', 'drug_means': means})

rows = read('nature_supplied_columns.csv')
frozen = json.loads((base / 'frozen_nature_checks.json').read_text(encoding='utf-8'))
nature, masks = [], []
for mapping, previous in zip(read('nature_field_mapping.csv'), frozen):
    x, y, valid = [], [], []
    for row in rows:
        a, a_status = number(row[mapping['experimental_column']])
        b, b_status = number(row[mapping['prediction_column']])
        keep = a_status == b_status == 'finite'
        masks.append(dict(endpoint=mapping['endpoint'], model=mapping['model'], source_row=row['source_row'],
                          included=int(keep), experimental_status=a_status, prediction_status=b_status))
        if keep:
            x.append(a)
            y.append(b)
            valid.append(int(row['source_row']))
    rho = stats.correlation(ranks(x), ranks(y))
    assert valid == previous['valid_rows']
    assert abs(rho - previous['source_row_recomputed_rho']) < 1e-12
    nature.append(dict(mapping, finite_pair_n=len(x), finite_pair_spearman_rho=rho,
                       shared_parent_n=len({r['B'] for r in rows if int(r['source_row']) in valid})))

with (out / 'nature_masks.csv').open('w', encoding='utf-8', newline='') as handle:
    writer = csv.DictWriter(handle, fieldnames=list(masks[0]))
    writer.writeheader()
    writer.writerows(masks)
result = {'status': 'PASS_FROZEN_CALCULATION_REPLAY', 'python': sys.version.split()[0],
          'scope': 'Replay of existing review checks; not model retraining, original-analysis reconstruction or correction of published estimates.',
          'input_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((base / 'data').glob('*.csv'))},
          'deepdelta': deepdelta, 'ppb': ppb, 'biliary': bile,
          'biliary_max_abs_cached_mean_difference': max(mean_differences),
          'biliary_max_abs_cached_sd_difference': max(sd_differences), 'nature': nature}
(out / 'results.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'status': result['status'], 'deepdelta': [deepdelta['records'], deepdelta['unique_raw_smiles']],
                  'ppb_model_dataset_checks': len(ppb), 'biliary_checks': len(bile), 'nature_checks': len(nature)}, indent=2))
