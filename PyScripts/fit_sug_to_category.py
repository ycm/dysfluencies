import json
from nltk.stem import PorterStemmer
import nltk
from collections import Counter

ps = PorterStemmer()
ct = Counter()

punct = '.,;:\'\"-()'

f = open('../WorkingJsons/all_sugs.json')
sugs = json.load(f)
f.close()

for i in range(len(sugs)):
	sugs[i] = ' '.join([ps.stem(w) for w in nltk.word_tokenize(sugs[i])])

f = open('../Resources/categories_to_keywords_sugs.json')
categories = json.load(f)
f.close()

stemmed_words_to_categories = {}
for k, words in categories.items():
	words = [ps.stem(w) for w in words]
	for w in words:
		stemmed_words_to_categories[w] = k
# print(stemmed_words_to_categories)

caught = 0
uncategorized = []
for i in range(len(sugs)):
	sugs[i] = sugs[i].replace('self-correct', 'selfcorrect')
	sugs[i] = sugs[i].replace('high frequency', 'highfrequency')
	sugs[i] = sugs[i].replace('self-monitor', 'selfmonitor')
	sugs[i] = sugs[i].replace('more difficult', 'harder')
	found = False
	tokens = [x for x in nltk.word_tokenize(sugs[i]) if x not in punct]
	for tkn in tokens:
		if tkn in stemmed_words_to_categories:
			ct[stemmed_words_to_categories[tkn]] += 1
			found = True
			caught += 1
			break
	if not found:
		uncategorized.append(sugs[i])

for i, cnt in ct.most_common():
	print(i, cnt)
print('\n')

print('Caught:', caught)
print('Uncategorized:', len(uncategorized))

for i in uncategorized:
	print(i)
	pass