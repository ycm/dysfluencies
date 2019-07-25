import json

with open('recwords.json') as f:
	recwords = json.load(f)

for r, triples in recwords.items():
	for idx, t in enumerate(triples[:-1]):
		assert int(t[1]) + int(t[2]) == int(triples[idx + 1][1])
