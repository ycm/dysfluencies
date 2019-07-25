import json

RESIDUE = 'obs_residue_1.tsv'

res = open('obs_residue_2.tsv', 'w')

obs_to_categories = {}
with open(RESIDUE) as f:
	for line in f:
		got = False
		ln = [x for x in line.strip().split('\t') if x]
		
		if 'UNCAT' in ln[0]:
			continue
		
		obs = ln[1].strip()

		if 'also' in ln[2]:
			got = True
			additional = ln[2].replace('also ', '').split('/')
			_all = [ln[0].strip()] + [x.strip() for x in additional]

			# print(_all)
			obs_to_categories[obs] = _all

		elif '?' in ln[2]:
			got = True
			obs_to_categories[obs] = [ln[0].strip()]

		else:
			# got = True
			# additional = [x.strip() for x in ln[2].replace('also ', '').split('/')]
			# obs_to_categories[obs] = additional
			pass

		if not got:
			print('\t'.join(ln), file=res)

with open('caught_2.json', 'w') as f:
	json.dump(obs_to_categories, f, indent=2)