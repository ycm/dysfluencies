import os, sys, json, pickle
from nltk.stem import PorterStemmer
from collections import Counter
from nltk.corpus import stopwords

with open(sys.argv[1]) as sug_f:
	sugs = json.load(sug_f)

ps = PorterStemmer()

# WorkingJsons/all_sugs.json WorkingJsons/20190714_stopwords_for_sugs.json
with open(sys.argv[2]) as sw_f:
	_sw = set([
		ps.stem(x) 
		for x in json.load(sw_f)
	])

sw = set(stopwords.words('english')) | _sw

cnt = Counter()
# print(sw)
for s in sugs:
	tokenized = [
		ps.stem(w).replace('(', '').replace(')', '')
		for w in s.split()
		if w not in sw and ps.stem(w) not in sw
	]
	for t in tokenized:
		cnt[t] += 1

for w in list(cnt.most_common())[::-1]:
	print(w)
	pass
	