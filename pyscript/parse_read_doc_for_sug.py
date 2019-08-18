import sys

READ_DOC = sys.argv[1]
f = open(READ_DOC)
# 0 - name
# 17 - $sug
for line in f:
	ln = line.strip().split('\t')
	name = ln[0].lower()
	sugs = ln[17].lower().replace('$sug:', '').strip().split(';')

	for s in sugs:
		print('\t'.join([name, s.strip()]))