#!/usr/bin/python
import json, sys

obs_to_sent_and_cat = 'res/obs_to_sent_and_cat.json'
reading_examples_path = 'res/reading_examples.json'

with open(obs_to_sent_and_cat) as f:
  obs_to_sent_and_cat = json.load(f)

with open(reading_examples_path) as f:
  reading_examples = json.load(f)

'''
Update reading examples JSON
'''
print('Updating reading examples JSON ...')

for ex in reading_examples:
  for idx, ev in enumerate(ex['Evaluations']):
    observations = ev['Observations'].keys()
    new_observations = {obs: obs_to_sent_and_cat[obs] for obs in observations}
    ex['Evaluations'][idx]['Observations'] = new_observations
with open(reading_examples_path, 'w') as f:
  json.dump(reading_examples, f, indent=2)

print('Done.')

'''
Create onehot encodings for observations and suggestions
'''
print('Creating onehot encodings for observations and suggestions ...')

import pandas as pd
from collections import Counter

obs_ct = Counter()
sug_ct = Counter()

all_obs_categories = set()
all_sug_categories = set()
for ex in reading_examples:
  for ev in ex['Evaluations']:
    obs = ev['Observations']
    sug = ev['Suggestions']
    for o, cats in obs.items():
      # all_obs_categories |= set(cats[1:])
      for c in cats[1:]:
        obs_ct[c] += 1
    for s, cats in sug.items():
      # all_sug_categories |= set(cats)
      for c in cats:
        sug_ct[c] += 1

print('\nFound {} $OBS categories'.format(len(set(dict(obs_ct).keys()))))
for x in obs_ct.most_common():
  print('{}\t{}'.format(x[1], x[0]))

print('\nFound {} $SUG categories'.format(len(set(dict(sug_ct).keys()))))
for x in sug_ct.most_common():
  print('{}\t{}'.format(x[1], x[0]))

# print('Found {} $OBS categories and {} $SUG categories'.format(len(all_obs_categories), len(all_sug_categories)))
