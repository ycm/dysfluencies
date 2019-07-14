import os, sys, json, pickle
from nltk.stem import PorterStemmer
from collections import Counter
from nltk.corpus import stopwords

ps = PorterStemmer()

# WorkingJsons/all_sugs.json
with open(sys.argv[1]) as sug_json:
  sugs = json.load(sug_json)

sugs = [
	sug.replace('.', '').replace(',', '').replace('/', ' ')
	for sug in sugs
]
# WorkingJsons/20190714_keywords_for_sugs.json
with open(sys.argv[2]) as keyw_json:
	keywords = set(json.load(keyw_json))

stem = True

if stem:
  sugs = [
    [ps.stem(x) for x in sug.strip().split()]
    for sug in sugs
  ]
  keywords = {ps.stem(x) for x in keywords}
else:
	sugs = [sug.split() for sug in sugs]

unmatched = [
	' '.join(sug)
	for sug in sugs
	if set(sug) & keywords == set()
]

with open(sys.argv[3]) as sw_f:
	if stem:
		_sw = set([
			ps.stem(x) 
			for x in json.load(sw_f)
		])
	else:
		_sw = set([
			x for x in json.load(sw_f)
		])

sw = set(stopwords.words('english')) | _sw

cnt = Counter()

for sug in unmatched:
	for w in sug.split():
		if w not in sw:
			cnt[w] += 1

for w in list(cnt.most_common())[::-1]:
	print(w[0] + '\t' + str(w[1]))

print('unmatched:', len(unmatched))
