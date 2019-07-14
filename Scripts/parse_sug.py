import json
with open('MoreFiles/sugs.csv') as f:
	lines = [ln.strip() for ln in f]

with open('MoreFiles/sugs.json', 'w') as f:
	json.dump(lines, f, indent=4)