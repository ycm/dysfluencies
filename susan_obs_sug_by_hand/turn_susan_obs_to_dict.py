import json

out_f = open('obs_residue_1.tsv', 'w')

line_to_categories = {}
with open('OBS_susan_annotated.tsv') as f:
	for line in f:
		ln = [x for x in line.strip().split('\t') if x]
		if not ln or len(ln) < 2:
			continue
		
		obs = ln[1].strip()

		orig_category = ln[0]
		other_category = None
		if len(ln) > 2:
			other_category = ln[-1]
		
		# print(orig_category, other_category)

		if other_category is not None and	\
		'also' not in other_category and	\
		'?' not in other_category and 		\
		'/' not in other_category:
			try:
				line_to_categories[ln[1]].append(other_category)
			except KeyError:
				line_to_categories[ln[1]] = [other_category]
			continue
		elif other_category is None and	\
		orig_category != 'UNCATEGORIZED':
			try:
				line_to_categories[ln[1]].append(orig_category)
			except KeyError:
				line_to_categories[ln[1]] = [orig_category]
		else:
			print(line.strip(), file=out_f)
			

with open('caught_1.json', 'w') as f:
	json.dump(line_to_categories, f, indent=2)

out_f.close()