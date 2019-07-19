import json

OBS_PATH = '../obs_by_evaluator.tsv'
SUG_PATH = '../sug_by_evaluator.tsv'

obs_f = open(OBS_PATH)
e2o = {}
for line in obs_f:
	ln = line.strip().split('\t')
	e = ln[0]
	o = ln[1].replace('$obs', '')
	try:
		e2o[e].append(o)
	except KeyError:
		e2o[e] = [o]
obs_f.close()

sug_f = open(SUG_PATH)
s2o = {}
for line in sug_f:
	ln = line.strip().split('\t')
	try:
		e = ln[0]
		o = ln[1].replace('$sug', '').strip()
	except:
		print(e, '**', o)
	try:
		s2o[e].append(o)
	except KeyError:
		s2o[e] = [o]
sug_f.close()

with open('../WorkingJsons/eval_to_obs.json', 'w') as f:
	json.dump(e2o, f, indent=4)

with open('../WorkingJsons/eval_to_sug.json', 'w') as f:
	json.dump(s2o, f, indent=4)