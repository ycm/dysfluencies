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

if __name__ == "__main__":
  print('utility functions.')