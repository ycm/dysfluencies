# alignment utils

from copy import deepcopy

def strip_pauses(alignment):
    rv = deepcopy(alignment)
    while rv[0][0] == '<pause>':
        pause_len = rv[0][2]
        for idx in range(len(rv)):
            rv[idx][1] -= pause_len
        rv = rv[1:]
    while rv[-1][0] == '<pause>':
        rv = rv[:-1]
    return rv

def is_valid(alignment):
    for idx, term in enumerate(alignment[:-1]):
        if term[1] + term[2] != alignment[idx + 1][1]:
            return False
    return True

def collapse_pauses(alignment):
    # merge pauses first
    merged = []
    for idx, term in enumerate(reversed(alignment[1:])):
        if term[0] != '<pause>':
            merged.append([term])
        else:
            merged[-1].append(term)
    merged = reversed([*merged, [alignment[0]]])
    
    # collapse null durations into next non-null token
    rv = []
    for m in merged:
        if len(m) == 0:
            rv.append(m[0])
        else:
            sframe = m[-1][1]
            nframes = sum(t[2] for t in m)
            rv.append([m[0][0], sframe, nframes])
    
    return rv