import json

with open('../Resources/categories_to_original_obs.json') as obsf:
	obs = json.load(obsf)

with open('../Resources/categories_to_original_sug.json') as sugf:
	sug = json.load(sugf)

for cat, lns in obs.items():
	print(cat.upper())
	for ln in lns:
		print(cat.upper() + '\t' + ln)
	print()
	# print('=' * 30)