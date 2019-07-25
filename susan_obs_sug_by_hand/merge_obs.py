import json

obs_1 = json.load(open('caught_1.json'))
obs_2 = json.load(open('caught_2.json'))

for obs, cats in obs_2.items():
	assert obs not in obs_1
	obs_1[obs] = cats

with open('OBS_line_to_list_of_categories.json', 'w') as f:
	json.dump(obs_1, f, indent=2)