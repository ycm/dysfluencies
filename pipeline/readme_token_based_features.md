# Token-based features

August 19, 2019

Given a passage $P$ we have the following alignments:

- $G_1,\dots,G_n:$ $n$ gold alignments of $P$
- $E:$ alignment of child's reading of $P$

Crucially, each $G_i$ is not necessarily the same as every other one.

For ease of explanation, every token in the format `<token>` (i.e. those surrounded in angle brackets) will be called a *pause*.

Where `w` denotes some word and `p` denotes some pause, each one of $C, G_1, G_2, \dots, G_n$ is formatted somewhat like:

```
p <sframe> <nframes>
p <sframe> <nframes>
w <sframe> <nframes>
w <sframe> <nframes>
p <sframe> <nframes>
w <sframe> <nframes>
w <sframe> <nframes>
w <sframe> <nframes>
...
p <sframe> <nframes>
```



First, for each alignment $C, G_1, G_2, \dots, G_n$, adjacent pauses are combined. (The relevant `sframe` and `nframes` are updated.)

Then, leading and trailing pauses are removed. (The total framecount of the alignment is thereby reduced.)

Name the modified $C, G_1, G_2, \dots, G_n$ as a collection of processed alignments $A_C, A_{G_1}, A_{G_2},\dots,A_{G_n}$.

Also, let $B_C, B_{G_1}, B_{G_2},\dots,B_{G_3}$ be the collection $A_C, A_{G_1}, A_{G_2},\dots,A_{G_n}$ where pauses in each $A_i$ are merged with the following word. From the collection of $A_i$s to the collection of $B_i$s, the total framecount of each alignment is preserved.

No collection $A_i$ or $B_i$ contained leading or trailing pauses. However, $A_i$s may contain pauses in between words while $B_i$s do not.



## Difflib

For the purposes of creating purely token-based features, `sframe` and `nframes` are ignored, and each alignment $A_i$ or $B_i$ is of the form `[w ... w, p, w ... w, p, ...]`.

Python's `difflib` module provides useful functions can be used to match sequences and output differences between two alignments $a, b$. Using `difflib`'s `ndiff` function, additions to $a$ found in $b$ are prefixed with `+`. Additions to $b$ found in $a$ are prefixed with `-`. Minor differences, such as `adventures` and `adventurous` are prefixed with `?`.

Pseudocode of token-based features for a single child's reading alignment $C$ is given below:

```bash
with n gold readings [G1,...,Gn] make collections [A_G1,...,A_Gn] and [B_G1,...,B_Gn]
with child reading alignment C make alignments A_C and B_C

features <- []
for each Collection in [(A_C, [A_G1,...,A_Gn]), (B_C, [B_G1,...,B_Gn])] do
	ExampleAlignment <- first item of Collection tuple (processed child's alignment)
	GoldAlignments <- second item of Collection tuple (list of processed gold alignments)
	
	pos_diff   <- 0
	neg_diff   <- 0
	minor_diff <- 0
	
	for each GoldAlignment in GoldAlignments do
		diff = ndiff(ExampleAlignment, GoldAlignment)
		pos_diff   += (number of additions in diff / length of GoldAlignment)
		neg_diff   += (number of removals in diff / length of GoldAlignment)
		minor_diff += (number of minor changes in diff / length of GoldAlignment)
	end
	
	pos_diff   /= n
	neg_diff   /= n
	minor_diff /= n
	
	push pos_diff, neg_diff, minor_diff to features
end
```

By repeating this process, all reading examples have **six** token based features. The theory behind this is that a perfect reading will have all six features close to `0`, whereas a highly inaccurate reading would have higher values in one or more of these features.