import json
from nltk.stem import PorterStemmer
import nltk
from collections import Counter

ps = PorterStemmer()
ct = Counter()

f = open('../Resources/20190713ReadingCategories.json')
obs = json.load(f)
f.close()

f = open('../Resources/categories_to_keywords.json')
categories = json.load(f)
f.close()

f = open('../Resources/categories_ignore.json')
ignore = {ps.stem(w) for w in json.load(f)}
f.close()

obs = [
	ln
	for cat in obs
	for ln in obs[cat]
]

stemmed_words_to_categories = {}
for k, words in categories.items():
	words = [ps.stem(w) for w in words]
	for w in words:
		stemmed_words_to_categories[w] = k

punct = '.,;:\'\"-'

for i in range(len(obs)):
	obs[i] = obs[i].lower()
	obs[i] = obs[i].replace('word by word', 'wordbyword')
	obs[i] = obs[i].replace('word-by-word', 'wordbyword')
	obs[i] = obs[i].replace('high frequency', 'highfrequency')
	obs[i] = obs[i].replace('self correct', 'selfcorrect')
	obs[i] = obs[i].replace('self-correct', 'selfcorrect')
	tokens = nltk.word_tokenize(obs[i])
	tokens = [ps.stem(x) for x in tokens if x not in punct]
	obs[i] = ' '.join(tokens)

uncategorized = []
for o in obs:
	found = False
	for w in o.split():
		if w in stemmed_words_to_categories:
			ct[stemmed_words_to_categories[w]] += 1
			found = True
			break
	if found:
		continue
	uncategorized.append(o)

for cat, cnt in ct.most_common():
	print(cat, cnt)
print('Caught:', sum([x[1] for x in ct.most_common()]))

print('\n')
print('Uncategorized:', len(uncategorized))

not_caught = []
for line in uncategorized:
	tokens = set(line.split())
	if tokens & ignore == set():
		not_caught.append(line)

print('Not caught:', len(not_caught))

for nc in not_caught:
	# print(nc)
	pass