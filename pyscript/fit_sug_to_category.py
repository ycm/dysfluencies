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


stemmed_sug_to_original = {}
for i in range(len(sugs)):
	orig = sugs[i]
	sugs[i] = ' '.join([ps.stem(w) for w in nltk.word_tokenize(sugs[i])])
	sugs[i] = sugs[i].replace('self-correct', 'selfcorrect')
	sugs[i] = sugs[i].replace('high frequency', 'highfrequency')
	sugs[i] = sugs[i].replace('self-monitor', 'selfmonitor')
	sugs[i] = sugs[i].replace('more difficult', 'harder')
	stemmed_sug_to_original[sugs[i]] = orig

f = open('../Resources/categories_to_keywords_sugs.json')
categories = json.load(f)
f.close()

stemmed_words_to_categories = {}
for k, words in categories.items():
	words = [ps.stem(w) for w in words]
	for w in words:
		stemmed_words_to_categories[w] = k
# print(stemmed_words_to_categories)

categories_to_original_sug = {}
caught = 0
uncategorized = []
for i in range(len(sugs)):
	# orig = sugs[i]
	# stemmed_sug_to_original[sugs[i]] = orig

	found = False
	tokens = [x for x in nltk.word_tokenize(sugs[i]) if x not in punct]
	for tkn in tokens:
		if tkn in stemmed_words_to_categories:
			try:
				categories_to_original_sug[stemmed_words_to_categories[tkn]].append(stemmed_sug_to_original[sugs[i]])
			except KeyError:
				categories_to_original_sug[stemmed_words_to_categories[tkn]] = [stemmed_sug_to_original[sugs[i]]]
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
	# print(i)
	pass

categories_to_original_sug['uncategorized'] = [stemmed_sug_to_original[uc] for uc in uncategorized]

for cat, sug_lst in categories_to_original_sug.items():
	categories_to_original_sug[cat] = list(set(sug_lst))

with open('../Resources/categories_to_original_sug.json', 'w') as f:
	json.dump(categories_to_original_sug, f, indent=2)