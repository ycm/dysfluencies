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
Get stats for obs and sug
'''
print('Getting stats for $OBS and $SUG ...')

import pandas as pd
from collections import Counter, defaultdict

obs_ct = Counter()
sug_ct = Counter()


for ex in reading_examples:
  for ev in ex['Evaluations']:
    obs = ev['Observations']
    sug = ev['Suggestions']

    for o, cats in obs.items():
      for c in cats[1:]:
        obs_ct[c] += 1

    for s, cats in sug.items():
      for c in cats:
        sug_ct[c] += 1

all_obs_categories = sorted(list(dict(obs_ct).keys()))
all_sug_categories = sorted(list(dict(sug_ct).keys()))

print('\nFound {} $OBS categories'.format(len(all_obs_categories)))
for x in obs_ct.most_common():
  print('{}\t{}'.format(x[1], x[0]))

print('\nFound {} $SUG categories'.format(len(all_sug_categories)))
for x in sug_ct.most_common():
  print('{}\t{}'.format(x[1], x[0]))



'''
Construct intermediate TSVs
'''
# by reading example; naive +/-
temp_obs_f = open('.obs.tsv.tmp', 'w')
temp_sug_f = open('.sug.tsv.tmp', 'w')

print('\t'.join(all_obs_categories), file=temp_obs_f)
print('\t'.join(all_sug_categories), file=temp_sug_f)

for ex in reading_examples:
  current_observations = defaultdict(int)
  current_suggestions = defaultdict(int)
  for ev in ex['Evaluations']:
    curreval_obs = ev['Observations']
    curreval_sug = ev['Suggestions']
    for o, cats in curreval_obs.items():
      for c in cats[1:]:
        if cats[0] == 'NEUTRAL':
          continue

        if cats[0] == 'POSITIVE':
          current_observations[c] += 1

        else:
          assert cats[0] == 'NEGATIVE'
          current_observations[c] -= 1
    
    for s, cats in curreval_sug.items():
      for c in cats:
        current_suggestions[c] += 1
  
  curr_ex_obs_score = '\t'.join([str(current_observations[x]) for x in all_obs_categories])
  curr_ex_sug_score = '\t'.join([str(current_suggestions[x]) for x in all_sug_categories])
  
  print(curr_ex_obs_score, file=temp_obs_f)
  print(curr_ex_sug_score, file=temp_sug_f)

temp_obs_f.close()
temp_sug_f.close()

print('Finished creating naive +/- $OBS and $SUG tables.')
