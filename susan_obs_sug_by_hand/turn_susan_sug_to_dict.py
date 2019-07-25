import json

SUG_susan = 'SUG_susan_annotated.tsv'

line_to_sug_categories = {}

with open(SUG_susan) as f:
	for line in f:
		ln = [x for x in line.strip().split('\t') if x]
		if len(ln) < 2:
			continue
		
		sug = ln[1]

		if len(ln) == 2:
			line_to_sug_categories[sug] = [ln[0]]
		
		if len(ln) == 3:
			assert 'also' in ln[2]
			line_to_sug_categories[sug] = [ln[0], ln[2].replace('also', '').strip()]

# with open('SUG_susan_annotated.tsv', 'w') as f:
# 	json.dump(line_to_sug_categories, f, indent=2)