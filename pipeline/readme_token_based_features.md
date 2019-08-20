# Token-based features

August 19, 2019

Given a passage $P$ we have the following alignments:

- $G_1,\dots,G_n:$ $n$ gold alignments of $P$
- $E:$ alignment of child's reading of $P$

Crucially, each $G_i$ is not necessarily the same as every other one.

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

