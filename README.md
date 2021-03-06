# permuta

[![Build Status](https://travis-ci.org/PermutaTriangle/Permuta.svg?branch=master)](https://travis-ci.org/PermutaTriangle/Permuta)

Permuta is a Python library for working with perms (short for permutations),
patts (patterns), and mesh patts.

## Installing

To install Permuta on your system, simply run the following command as a superuser:

```
# ./setup.py install
```

It is also possible to install Permuta in development mode, in which case you
run the following instead:

```
# ./setup.py develop
```

To run the unit tests using pytest run:

```
pytest --cov permuta tests
```

This requires `pytest` and `pytest-cov`.

## Demo

Once you've installed Permuta, it can be imported by a Python script or an
interactive Python session, just like any other Python library:

```python
>>> from permuta.demo import *
```

For this section we focus on a subset of modified features exposed in the `demo`
submodule. Importing `*` from it supplies you with the Perm and PermClass
classes (and their respective aliases Permutation and Av).

### Creating a single perm

There are several ways of creating a perm:

```python
>>> Perm()  # Empty perm
()
>>> Perm([])  # Another empty perm
()
>>> Perm(132)  # From number
(1, 3, 2)
>>> Perm(248)  # Attempted interpretation
(1, 2, 3)
>>> Perm("1234")  # From string
(1, 2, 3, 4)
>>> Perm("dcab")  # This is equivalent to ...
(4, 3, 1, 2)
>>> Perm(["d", "c", "a", "b"])  # ... this
(4, 3, 1, 2)
>>> Perm(0, 0, 2, 1)  # Index is tie-breaker
(1, 2, 4, 3)
>>> Perm("Ragnar", "Christian", "Henning")
(3, 1, 2)
>>> Perm.monotone_increasing(4)
(1, 2, 3, 4)
>>> Perm.monotone_decreasing(3)
(3, 2, 1)
>>> random_perm = Perm.random(7)
```

You can visualize a perm using matplotlib/seaborn:

```python
>>> import matplotlib.pyplot as plt
>>> p = Perm((1, 3, 2, 4))
>>> ax = p.plot()
>>> plt.show()
```

![Plot of the perm 1324](README.d/1324.png?raw=true "Plot of the perm 1324")

The avoids, contains, and occurrence\* methods enable working with patts:

```python
>>> p.contains(321)
False
>>> p.avoids(12)
False
>>> p.occurrences_of(21)
[[3, 2]]
>>> Perm(12).occurrences_in(p)
[[1, 3], [1, 2], [1, 4], [3, 4], [2, 4]]
```

The basic symmetries are implemented:

```python
>>> [p.reverse(), p.complement(), p.inverse()]
 [(4, 2, 3, 1), (4, 2, 3, 1), (1, 3, 2, 4)]
```

To take direct sums and skew sums we use `+` and `-`:

```python
>>> q = Perm((1, 2, 3, 4, 5))
>>> p + q
(1, 3, 2, 4, 5, 6, 7, 8, 9)
>>> p - q
(6, 8, 7, 9, 1, 2, 3, 4, 5)
```

There are numerous practical methods available:

```python
>>> p.fixed_points()
[1, 4]
>>> p.ascents()
[1, 3]
>>> p.descents()
[2]
>>> p.inversions()
[[3, 2]]
>>> p.cycles()
[[1], [3, 2], [4]]
>>> p.major_index()
2
```

### Creating a perm class

You might want the set of all perms:

```python
>>> all_perms = PermClass()
>>> all_perms
<All perms>
```

Perm classes can be specified with a basis:

```python
>>> basis = [213, Perm((2, 3, 1))]
>>> basis
[213, (2, 3, 1)]
>>> perm_class = Av(basis)
>>> perm_class
<Perms avoiding: (2, 1, 3) and (2, 3, 1)>
```

Recall that Av is just an alias of PermClass.

You can ask whether a perm belongs to the perm class:

```python
>>> 4321 in perm_class
True
>>> 1324 in perm_class
False
```

You can get the n-th perm of the class or iterate:

```python
>> [perm_class[n] for n in range(10)]
[(), (1), (1, 2), (2, 1), (1, 2, 3), (1, 3, 2), (3, 2, 1), (3, 1, 2), (4, 3, 2, 1), (4, 1, 3, 2)]
>>> perm_class_iter = iter(perm_class)
>>> [next(perm_class_iter) for _ in range(10)]
[(), (1), (1, 2), (2, 1), (1, 2, 3), (1, 3, 2), (3, 2, 1), (3, 1, 2), (4, 3, 2, 1), (4, 1, 3, 2)]
```

(BEWARE: Lexicographic order is not guaranteed at the moment!)

### The subset of a perm class where the perms are a specific length

You can define a subset of perms of a specific length in the perm class:

```python
>>> perm_class_14 = perm_class.of_length(14)
>>> perm_class_14
<Perms of length 14 avoiding: (2, 1, 3) and (2, 3, 1)>
```

You can ask for the size of the subset because it is guaranteed to be finite:

```python
>>> len(perm_class_14)
8192
```

The iterating and containment functionality is the same as with `perm_class`,
but indexing has yet to be implemented:

```python
>>> 321 in perm_class_14
False
>>> (1, 14, 2, 13, 3, 4, 5, 12, 6, 11, 7, 8, 9, 10) in perm_class_14
True
>>> Perm(range(10)) - Perm(range(4)) in perm_class_14
False
>>> next(iter(perm_class_14))
(14, 1, 2, 3, 4, 5, 13, 12, 11, 10, 6, 9, 7, 8)
```

To get a feeling for the perm class, you can plot a heatmap of this subset
 using matplotlib/seaborn:

```python
>>> ax = perm_class_14.plot()
>>> plt.show()
```

![A heatmap plot for the perms of length 14 avoiding 213 and 231](README.d/av_213_231_of_length_14_heatmap.png?raw=true "A heatmap plot for the perms of length 14 avoiding 213 and 231")

## Life in Permuta beyond the demo

If your work has reached a place where your require functionality beyond
that offered by the demo, it may be time to proceed to the non-demo version
of Permuta. The first hurdle will be coming to terms with the zero based indexing.
Here's how to get started:

```python
>>> from permuta import Perm, PermSet, MeshPatt
```

## License
BSD-3: see the [LICENSE](https://github.com/PermutaTriangle/Permuta/blob/master/LICENSE) file.
