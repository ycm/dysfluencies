# alignment utils
# strip pauses -> combine_adjacent_pauses -> (if necessary) collapse_pauses
# validate using is_valid()

from copy import deepcopy

def combine_adjacent_pauses(alignment):
    tmp = []
    for term in alignment:
        if term[0] != '<pause>':
            tmp.append([term])
        else:
            if tmp[-1][0][0] == '<pause>':
                tmp[-1].append(term)
            else:
                tmp.append([term])
    rv = []
    for term in tmp:
        if len(term) == 1:
            rv.append(term[0])
        else:
            assert all([t[0] == '<pause>' for t in term])
            sframe = term[0][1]
            nframes = sum(t[2] for t in term)
            rv.append(['<pause>', sframe, nframes, *term[0][3:]])
    return rv

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

            # *m[0][3:] -> keep additional fields in alignment (e.g. f0)
            rv.append([m[0][0], sframe, nframes, *m[0][3:]])
    
    return rv
