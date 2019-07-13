import sys, os, pickle, json

with open('epr_main_fields.pkl', 'rb') as f:
	fields = pickle.load(f)

field_to_keyword = {}

for field in fields:
	f = str(field)
	field_to_keyword[f] = [x.lower() for x in field[1].replace('-', ' ').split()]
	while True:
		x = input(str(field) + ' >> ')
		if not x:
			break
		try:
			field_to_keyword[f].append(x)
		except KeyError:
			field_to_keyword[f] = [x]

with open('field_terms.json', 'w') as f:
	json.dump(field_to_keyword, f, indent=2)