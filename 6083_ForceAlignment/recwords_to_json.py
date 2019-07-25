import json

RECWORDS = 'recwords.csv'

rec_to_data = {}
with open(RECWORDS) as f:
    next(f)
    for line in f:
        ln = line.split(',')
        recid = ln[0]
        word_sframe_nframes = tuple([ln[3].strip()] + ln[1:3])
        try:
            rec_to_data[recid].append(word_sframe_nframes)
        except KeyError:
            rec_to_data[recid] = [word_sframe_nframes]

with open('recwords.json', 'x') as f:
    json.dump(rec_to_data, f, indent=2)
    
