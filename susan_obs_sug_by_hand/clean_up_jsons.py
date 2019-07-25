import json, sys

new_d = {}
with open(sys.argv[1]) as f:
	d = json.load(f)
	for line, cats in d.items():
		if line[0] == '"' and line[-1] == '"':
			line = line[1:-1]
		new_d[line] = cats
	
with open(sys.argv[2], 'x') as f:
	json.dump(new_d, f, indent=2)