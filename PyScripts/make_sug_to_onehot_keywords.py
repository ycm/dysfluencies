import sys, os, json, pickle
from nltk.stem import PorterStemmer

stem = True
ps = PorterStemmer()

with open(sys.argv[1]) as f:
  SUG_LIST = json.load(f)

with open(sys.argv[2]) as f:
  KEYWORDS = set(json.load(f))

of = open(sys.argv[3], 'w')

line_to_onehot_kw = []
if stem:
  KEYWORDS = {ps.stem(x) for x in KEYWORDS}

print('line', end='\t', file=of)
for kw in sorted(KEYWORDS):
  print(kw, end='\t', file=of)
print(file=of)

for line in SUG_LIST:
  tokens = None
  if stem:
    tokens = set([ps.stem(x) for x in line.split()])
  else:
    tokens = set(line.split())
  
  kw_onehot = {}
  for kw in KEYWORDS:
    if kw in tokens:
      kw_onehot[kw] = 1
    else:
      kw_onehot[kw] = 0
  
  print(line, end='\t', file=of)
  for k in sorted(kw_onehot.keys()):
    print(kw_onehot[k], end='\t', file=of)
  print(file=of)
