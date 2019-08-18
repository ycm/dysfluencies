import sys, os, json, random
from collections import *

def iter_dict(d):
    for k1, k2v in d.items():
        for k2, v in k2v.items():
            yield k1, k2, v

def collapse_adjacent_pauses(align):
    idx = 0
    current_items = []
    condensed_align = []
    for item in align:
        curr_token, sframe, nframes = item
        if '<' not in curr_token:
            if current_items:
                if len(current_items) == 1:
                    current_items = current_items[0]
                condensed_align.append(current_items)
            condensed_align.append(item)
            current_items = []
        else:
            current_items.append(item)
    if current_items:
        if len(current_items) == 1:
            current_items = current_items[0]
        condensed_align.append(current_items)
    for i in range(len(condensed_align)):
        if type(condensed_align[i][0]) == type([]):
            first_sframe = condensed_align[i][0][1]
            total_nframes = sum(x[2] for x in condensed_align[i])
            condensed_align[i] = ['<pause>', first_sframe, total_nframes]
    for i, elem in enumerate(condensed_align):
        if '<' not in elem[0]:
            continue
        condensed_align[i] = ['<pause>', elem[1], elem[2]]
    return condensed_align

def remove_leading_and_trailing_pauses(d):
    stripped_i2s2a = defaultdict(lambda: defaultdict(list))
    for item, session, alignment in iter_dict(condensed):
        assert(len(alignment)) > 4
        if alignment[0][0] == '<pause>':
            pause_length = alignment[0][-1]
            for idx in range(len(alignment))[1:]:
                alignment[idx][1] -= pause_length
            alignment = alignment[1:]
        if alignment[-1][0] == '<pause>':
            alignment = alignment[:-1]
        stripped_i2s2a[item][session] = alignment
    return stripped_i2s2a

def merge_pauses(d):
    collapsed_i2s2a = defaultdict(lambda: defaultdict(list))
    for item, session, alignment in iter_dict(d):
        new_alignment = []
        for i in range(len(alignment))[1:]:
            if alignment[i - 1][0] == '<pause>':
                alignment[i][1] = alignment[i - 1][1]
                alignment[i][-1] += alignment[i - 1][-1]
            else:
                new_alignment.append(alignment[i - 1])
        collapsed_i2s2a[item][session] = [*new_alignment, alignment[-1]]
    return collapsed_i2s2a

if __name__ == '__main__':
    print('functions to condense a reading example.')
