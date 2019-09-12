LINEAR VERSUS BINARY SEARCH: A case study
Long Nguyen, lpn@mit.edu

1) PERFORMANCE THRESHOLD

On a PC running Ubuntu 18.10 with 32GB 3000MHz DDR4 RAM,
an i7-6700K at clock speed (4.0GHz), SAMSUNG 850 EVO 256GB SSD,
threshold was found to fluctuate between 6-8 even after trials,
but 7 showed up most of the time.

Some thoughts below.
  1: Threshold depends on algorithm implementation. If we fine-tuned
     the way we perform binary versus linear to account for specific
     languages like C or Python, it could vary.
  2: Language used probably matters. Have never studied compilers, but
     could definitely see basic Python overhead as something that
     might take away from accurate performance profiling compared to
     something, say, in raw assembly.
  3: Hardware for sure. Instruction sets could differ between modern
     and new computers. Apple is planning to equip future MacBooks
     with ARM processors, so this is definitely something worth
     thinking about. Could we do better depending on the ISA? Worse?
  4: Caching. My i7-6700K has L3 8MB, L2 1MB, and L3 256KB. Now, if
     we were dealing with an ancient Pentium 4 or something, trying
     to do our profiling with arrays of size 10000 might be hairy,
     since I assume there would be far more cache misses and thus
     slower operations compared to a modern processor.

2) SERIES SHAPES

I'm quite surprised at how the curves turned out. I usually think
of log versus binary as more of a close battle, but even at small
array sizes like 350 in my benchmarks, the log curve far outperforms
the linear curve. Both definitely follow linear/log trend functions
as expected.

3) NOTES

Benchmarking the linear algorithm yielded a messy scatter of points.
This was unexpected behavior, but after some thinking, it makes
sense. Benchmarking average times for linear search to converge by
choosing random keys/indices in the arrays is bound to give us
measurements all over the place, since you could have great performance
if your random key was the first element and horrific if it's the last.
