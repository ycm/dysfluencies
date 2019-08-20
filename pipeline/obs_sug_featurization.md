# OBS and SUG categories featurization

August 19, 2019

### Two approaches: per example and per evaluation

Per example: aggregate OBS and SUG for a single reading over all evaluations (70 examples)

Per evaluation: treat each evaluation as a separate example (222 examples)



### Featurization

Regardless of the approach used, each example involves a collection of observations and a collection of suggestions. Each observation and suggestion is tagged with the corresponding categories that the observation or suggestion applies to. A single observation may be tagged with more than 1 category; in fact, many of them are tagged with more than 1 category. Each observation is further tagged with a polarity, e.g. `POSITIVE`, `NEGATIVE`, or `NEUTRAL`.

For each example we create a mapping from OBS and SUG categories to integers defaulting at 0, which we will call $O$ and $S$.

For each observation, the polarity is noted. `NEUTRAL` observations are ignored. If an observation is `NEGATIVE`, each relevant category under $O$ is decremented by 1. If an observation is `POSITIVE`, each relevant category under $O$ is incremented by 1. For each suggestion, each relevant category under $S$ is incremented by 1.

```
Observations:
o1 : NEUTRAL, ACCURACY, EXPRESSION
o2 : POSITIVE, ACCURACY, MONITORING_FOR_MEANING
o3 : NEGATIVE, ACCURACY, VOCABULARY
o4 : NEGATIVE, VOCABULARY, SIGHT_WORD

Suggestions:
s1 : PUNCTUATION, SELF_CORRECTION
s2 : PUNCTUATION, PHONICS

Results:
--------
O:
+1 MONITORING_FOR_MEANING
-2 VOCABULARY
-1 SIGHT_WORD
(everything else 0)

S:
2 PUNCTUATION
1 SELF_CORRECTION
1 PHONICS
(everything else 0)
```

