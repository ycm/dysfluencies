# Predicting suggestion categories from expert evaluations as well as automatic alignment data

August 27, 2019

Our end goal in the dysfluencies/Reading Profiles project is to produce a list of meaningful *suggestions* based on information relating to a reading.

## Observations and suggestions

When a user reads a passage, I will call that a reading example. In the data we're working with, each reading example also has a set of *evaluations*. Evaluations are expert assessments of a reading example. A reading example maybe have 1 or more corresponding evaluations.

Within an evaluation we have *observations* and *suggestions*. Observations are free-text notes about the reading. An observation might look something like `has trouble reading multisyllabic words`. Suggestions are free-text suggestion guidelines. A suggestion might look something like `work on building sight-word vocabulary`.

The first part of the dysfluencies project involved extracting meaningful *categories* from observations and suggestions. Observation categories include `VOCABULARY` and `EXPRESSION`. Suggestion categories include `DIFFICULTY` and `MONITORING_FOR_MEANING`. Categorizing observations and suggestions was done by Jared Bernstein, Andrew Yang, and Susan Barber. From this point on, `OBS` refers to an observation category, while `SUG` refers to a suggestion category.

## A multilabel classification task

The problem at hand is to create a model that delivers relevant suggestions to teachers who may not necessarily be reading experts. Teachers can use these suggestions to guide instruction for struggling students.

To create this model we should look at the data we have. For now, our inputs include observations, suggestions, and forced alignments for each reading example. Ideally our output is a list of suggestions.

Our preliminary proposal for this task was to create a "wireframe" model that simply uses `OBS`s to predict `SUG`s. 
$$
{X}=\begin{pmatrix}
—\mathbf v^{(1)}—\\
—\mathbf v^{(2)}—\\
\vdots\\
—\mathbf v^{(m)}—\\
\end{pmatrix}\\
\text{ }\\
{Y}=\begin{pmatrix}
|&|&&|\\
\mathbf u_1&\mathbf u_2&\dots&\mathbf u_k\\
|&|&&|
\end{pmatrix}
$$
In our feature vector $X$, a feature vector $\mathbf v^{(i)}$ is a representation of the `OBS`s associated with the $i$-th reading example. Similarly, the $i$-th row of $Y$ is a representation of the `SUG`s associated with the $i$-th reading example. Within $Y$, each column vector $\mathbf u_j$ is an arbitrary representation of the values for the $j$-th `SUG` across all reading examples.

Clearly this is a multilabel classification task. Given features in $X$, we want to predict every $\mathbf u_j$.

## Featurizing `OBS`s and `SUG`s

For each reading example we have a set of evaluations. Each evaluation contains observations and suggestions.

We tag each observation with the `OBS`s we find it belongs to. For instance, `word by word reading` could fall under `WORD_BY_WORD`. We also note the polarity of each observation. Possible polarities are `POSITIVE`, `NEUTRAL`, and `NEGATIVE`. We tag each suggestion with the `SUG`s we find it belongs to. Suggestions were **not** tagged with polarity. Each observation/suggestion can be tagged with multiple `OBS`s/`SUG`s as well.

For each reading example, we consider all `OBS`s that its observations were tagged. Each observation-`OBS` pair is given a score of 1 if the observation was `POSITIVE`, 0 if `NEUTRAL`, and -1 if `NEGATIVE`. For each `OBS`, these scores are summed.

As a concrete example, say evaluator 1 writes a `POSITIVE` observation under `FLUENCY` and a `NEGATIVE` observation under {`VOCABULARY`, `PUNCTUATION`}. Say evaluator 2 writes a `NEGATIVE` observation under {`VOCABULARY`, `SIGHT_WORD`}. This particular reading example would then have a score of -2 under `VOCABULARY`, -1 under `PUNCTUATION` and `SIGHT_WORD`, +1 under `FLUENCY`, and zero everywhere else.

For each `SUG`, we simply see if any evaluator has written a suggestion under that `SUG`. A score of 1 means one or more evaluators has written a note under that `SUG`, 0 otherwise. This implies $Y$ is a binary matrix.

Later on, we will add features related to alignment durations and $F_0$s. The label matrix $Y$, however, will remain the same.

## Training and testing

A random forest model with 25 trees and 5-fold cross validation is used to predict $Y$ from $X$. We do this by first identifying "major" features and labels. We filter out any `OBS`s below a certain number of nonzero values in $X$ and also filter out any `SUG`s below a certain number of nonzero values in $Y$. The threshold I used was 25 for both $X$ and $Y$ and is completely arbitrary.

As more features are created, I append them to $X$ and leave $Y$ the same.