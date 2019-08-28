# Aligning example and gold readings with duration and $F_0$ information

Updated August 26, 2019

ycm@stanford.edu

Below is documentation for the process used for aligning a reading example with corresponding gold readings, as well as relevant features that can be extracted after the alignment.

An alignment (gold or otherwise) with duration and $F_0$ values should follow this format:

```
word	sframe	nframes	f0s
<eps>	0				10			[_ * 10]
<c1>	10			15			[_ * 16]
word1	25			9				[_ * 9]
...
```

The `f0s` column includes the $F_0$ pitch determined at each frame, organized as a list of variable length.

## Basic preprocessing

Tokens of the format `<...>` are pauses, and they are normalized to `<pause>` because for the purposes here there is no difference between `<eps>`, `<c1>`, etc.

Further, alignments are stripped of leading and trailing pauses, and adjacent `<pause>`s are merged as well. For an alignment $A$, $\hat{A}$ denotes $A$ after the preprocessing steps above.

## An optional step to deal with `<pause>`s

After the basic preprocessing steps above, an alignment retains still retains all its valuable information. To go a step further, the duration of `<pauses>` can be merged into the duration of the following word. An a processed alignment $\hat{A}$ is denoted $A*$ after this merging step.

*Aside*: The relevant auxiliary functions to perform these preprocessing steps are located in `dysfluencies/pipeline/util/condense_new.py`. Use `strip_pauses()` followed by `combine_adjacent_pauses()` to turn an alignment $A$ to $\hat A$. Then use `collapse_pauses()` to turn $\hat A$ to $A*$. If desired, a call to `is_valid()` at the very end can check the integrity of duration information in an alignment. Check `dysfluencies/pipeline/make_duration_based_features.ipynb` see these tools in action.

## Alignment using `diff`

**Pause-delimited grouping**

The Python `difflib` implementation of `diff` is used. For an example alignment $E$ and a gold alignment $G$, we preprocess to get $\hat{E}$ and $\hat{G}$. We can temporarily organize each token in $\hat E$ and $\hat G$ as two lists in order to apply `difflib.ndiff()`. Note that the further processed alignments $E*$ and $G*$ will not be used 

Visually similar lines in `difflib.ndiff()` are marked with a `?`. This feature was exploited in creating token-based featurese, but are disregarded here as including them would make things needlessly complicated. Thus, if the token `adventures` in $\hat E$ replaces the token `adventurous` in $\hat C$, we simply count one removal marked with `-` and one addition marked with `+`.

To leverage duration (and $F_0$) information when comparing $\hat E$ and $\hat G$, it seemed like a reasonable idea to separate a reading into constituent phrases. Possible ideas include dependency parsing, separating by sentence, etc.

Because duration information and pause tokens are readily available, a straightforward way of forming constituent groups is to separate by the `<pause>` token in the processed gold alignment $\hat{G}$. Then, with `difflib.ndiff()`, we can easily associate tokens in $\hat E$ with their predicted groups in $\hat G$. Below is an example of the result:

```
Gold grouping:
so maybe he would enjoy becoming an architect <pause>

Example grouping:
so he maybe enjoy becoming an <pause> architect <pause>
```

Then, the individual tokens of each gold grouping is matched with `difflib.ndiff()` to the individual tokens of its corresponding example grouping, minus `<pause>`s. In the example above, the matched tokens would be `['so', 'enjoy', 'becoming', 'an', 'architect']`. 



**Duration scores**

From this we can compute a rudimentary similarity of the time durations in the gold and example groups. For each group $e$ and $g$, the `nframes`-based similarity is computed as:
$$
\vec{m}:= \texttt{MatchedTokens}(e, g)\\
\texttt{nframes_similarity}(e,g) = \texttt{CosineSim}(\texttt{nframes}(e, \vec{m}), \texttt{nframes}(g, \vec{m}))
$$
There is a glaring shortcoming of this similarity metric. Consider the following example:

```
Gold grouping:
so maybe he would enjoy becoming an architect <pause>

Example grouping:
so maybe he architect
```

In this example, the only tokens that are considered in this metric are the matched ones, namely `['so', 'maybe', 'he', 'architect']`. If the `nframes` durations for those four tokens were identical between the example and gold groupings, the similarity would be 1.0. To help resolve this problem, the cosine similarity metric is multiplied against a `match_token_similarity`, which is simply $\dim\vec{m}/\dim g$. If a gold group has no matching tokens in the example group, this metric is given a value of 0.

This metric can be normalized by averaging similarities across all groups, and then averaging across all gold readings correesponding to this example to form the `GroupDurationSim` feature for this reading example.

This metric can alternatively be normalized using the length of each gold group. For a 5-token gold grouping in a 20-token reading, the metric should count toward 25% of the total similarity $s$ for this example reading and this gold reading. Lastly, $s$ is averaged across all gold readings to yield the `WeightedGroupDurationSim` feature for this reading example.



**F0 scores**

Similar to duration scores, we can compute the $F_0$ similarities between example and gold groups. We begin by finding a mean $F_0$, in a reading $E$ by averaging all $F_0$ values across $E*$. (This way, $F_0$ readings for pauses are ignored.) We then subtract the mean $F_0$ from all $F_0$s across $E$ to normalize for pitch differences.

For each example and gold group, we match tokens again. Then, for every aligned word, the $F_0$ slope over that word is then easily computable. We can thus construct a similarity metric $\texttt{CosineSim}(\texttt{slope}(e, \vec{m}), \texttt{slope}(g, \vec{m}))$ which is again multiplied by `match_token_similarity`.

If a gold group has no matching tokens in the example group, or whenever cosine similarity is not available (such as with a zero-vector), a score of 0 is used.

From this metric we can create `GroupF0Sim` and `WeightedGroupF0Sim` in the same way as before.

## Other features

Using `difflib.ndiff()` the number of inserted and omitted `<pause>`s is also readily available. For processed $\hat E$ and $\hat G$, we construct the features `NormalizedPausesInserted` and `NormalizedPausesOmitted` as such:
$$
\texttt{NormalizedPausesInserted} = \frac{\text{pauses inserted in }\hat E}{\text{total pauses in }\hat G}\\
\texttt{NormalizedPausesOmitted} = \frac{\text{pauses omitted from }\hat E}{\text{total pauses in }\hat G}
$$




## List of features

`GroupDurationSim`: Average duration similarity across pause-separated groups in gold readings.

`WeightedGroupDurationSim`: Above, but normalized by length of each gold group.

(It turns out that these two calculations don't differ significantly in practice. For the time being they are included in the model.)

`GroupF0Sim`: Average $F_0$ slope similarity across pause-separated groups in gold readings.

`WeightedGroupF0Sim`: Above, but normalized by length of each gold group.

`NormalizedPausesInserted`/`NormalizedPausesOmitted`: Normalized count of pauses inserted into/omitted from an example, averaged across gold readings.