# utility functions.

import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score as cvs
from itertools import chain, combinations

def get_cv_results(classifier, features, labels, k=5):
  scores = cvs(classifier, features, labels, cv=k)
  return tuple([scores, features.columns, labels.columns])

# from python documentation
def get_powerset(it):
  s = list(it)
  return list(chain.from_iterable(combinations(s, r) for r in range(len(s)+1)))

def filter_for_length(coll, length=4):
  return [list(x) for x in list(coll) if len(x) >= length]

def load_categories():
  obs_cats = ['ACCURACY',
    'EXPRESSION',
    'FLUENCY',
    'MONITORING_FOR_MEANING',
    'MORPHOLOGY',
    'MULTISYLLABIC_WORDS',
    'OMISSION_INSERTION',
    'PHONICS',
    'PHRASING',
    'PRONUNCIATION',
    'PUNCTUATION',
    'RATE',
    'SELF_CORRECTION',
    'SIGHT_WORD',
    'SUBSTITUTION_REVERSAL',
    'VOCABULARY',
    'WORD_ATTACK',
    'WORD_BY_WORD',
    'WORD_ENDINGS'
  ]
  sug_cats = [
    'ARTICULATION',
    'DIFFICULTY',
    'EXPRESSION',
    'FLUENCY',
    'MEANING_COMPRENHENSION',
    'MORPHOLOGY',
    'MULTISYLLABIC_WORDS',
    'OMISSIONS_INSERTIONS',
    'PHONICS',
    'PHRASING',
    'PRONUNCIATION',
    'PUNCTUATION',
    'RATE',
    'SELF_CORRECTION',
    'SELF_MONITOR',
    'SIGHT_WORD',
    'SUBSTITUTIONS_REVERSALS',
    'VOCABULARY',
    'VOICE',
    'WORD_ATTACK',
    'WORD_ENDINGS'
  ]
  return obs_cats, sug_cats

if __name__ == "__main__":
  print('utility functions.')