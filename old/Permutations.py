# pylint: disable=missing-docstring

import collections
import itertools
import random
import sys

from math import factorial

from .Permutation import Permutation
from .math import catalan

if sys.version_info.major == 2:
    range = xrange  # pylint: disable=redefined-builtin,invalid-name,undefined-variable


class _PermutationPatternClass(object):  # pylint: disable=too-few-public-methods
    """A base class for permutation defined by patterns classes."""
    def __init__(self, length, patterns):
        self.length = length
        self.patterns = patterns

    def __str__(self):
        result = ["Permutation class of length "]
        result.append(str(self.length))
        result.append(" defined by ")
        result.append(str(self.patterns))
        return "".join(result)

    def __repr__(self):
        return self.__class__.__name__ + "({}, {})".format(self.length, self.patterns)

    def is_polynomial(self):
        raise NotImplementedError


class Permutations(object):
    def __new__(cls, length, avoiding=None):
        if avoiding is None:
            return PermutationsAvoidingNone(length)
        elif isinstance(avoiding, Permutation):
            # Decision trees for special cases
            if len(avoiding) == 2:
                if avoiding[0] == 0:
                    return PermutationsAvoiding01(length)
                else:
                    return PermutationsAvoiding10(length)
            elif len(avoiding) == 3:
                if avoiding[0] == 0:
                    if avoiding[1] == 1:
                        return PermutationsAvoiding012(length)
                    else:
                        return PermutationsAvoiding021(length)
                elif avoiding[0] == 1:
                    if avoiding[1] == 0:
                        return PermutationsAvoiding102(length)
                    else:
                        return PermutationsAvoiding120(length)
                else:
                    if avoiding[1] == 0:
                        return PermutationsAvoiding201(length)
                    else:
                        return PermutationsAvoiding210(length)
            else:
                return PermutationsAvoidingGeneric(length,(avoiding,))
        elif (isinstance(avoiding, collections.Iterable) and
                all(isinstance(x, Permutation) for x in avoiding)):
            return PermutationsAvoidingGeneric(length, avoiding)
        else:  # TODO: TypeError, not RTE
            raise RuntimeError("Cannot avoid " + repr(avoiding))


class PermutationsAvoidingGeneric(_PermutationPatternClass):
    def __init__(self, length, patterns, up_to=None):
        super(PermutationsAvoidingGeneric, self).__init__(length, tuple(patterns))
        self.length = length
        self.up_to = up_to

    def __iter__(self):
        # TODO: make this lazy, i.e. use yield inside the generation (if possible)

        current = set([Permutation()])

        # TODO: Why this strange case? Yield empty permutation if it doesn't avoid all the patterns?
        if self.up_to or self.length == 0:
            empty_permutation = Permutation()
            if not empty_permutation.avoids(*self.patterns):
                yield empty_permutation

        for length in range(1, self.length+1):
            nxt = set()
            for prev in current:
                for index in range(len(prev)+1):
                    maybe_list = list(prev[:index])
                    maybe_list.append(len(prev)+1)
                    maybe_list.extend(prev[index:])
                    maybe = Permutation(maybe_list)
                    # TODO: only check for occurrences that contain the new len(prev)+1 element
                    if not maybe.avoids(*self.patterns):
                        nxt.add(maybe)
            current = nxt
            if self.up_to or length == self.length:
                for perm in current:
                    yield perm

    def is_polynomial(self):
        overallinterset = set()
        for perm in self.patterns:
            overallinterset = overallinterset.union(types(perm))
            if len(overallinterset) == 10:  # TODO: wat?
                return True
        return False


class PermutationsAvoidingNone(itertools.permutations):
    """Class for iterating through all Permutations of a specific length."""

    __slots__ = ("length", "domain")

    def __new__(cls, length):
        domain = list(range(length))
        instance = super(PermutationsAvoidingNone, cls).__new__(cls, domain)
        # Initialize, even if it should technically be done in __init__
        instance.domain = domain
        instance.length = length
        return instance
    
    def is_polynomial(self):
        return False

    if sys.version_info.major == 2:
        def next(self):
            return Permutation(super(PermutationsAvoidingNone, self).next())  # pylint: disable=no-member
    else:
        def __next__(self):
            return Permutation(super(PermutationsAvoidingNone, self).__next__())  # pylint: disable=no-member

    def __iter__(self):
        return self

    def random_element(self):
        """Return a random permutation of the length."""
        random.shuffle(self.domain)  # TODO: Not use domain attribute?
        return Permutation(self.domain)

    def __len__(self):
        return factorial(self.length)

    def __str__(self):
        return "The set of all Permutations of length {}".format(self.length)

    def __contains__(self, other):
        """Check if other is a permutation in the set."""
        return isinstance(other, Permutation) and len(other) == self.length


class PermutationsAvoiding01(_PermutationPatternClass):
    """Class for iterating through Permutations avoiding 12 of length n"""
    def __init__(self, n):
        super(PermutationsAvoiding01, self).__init__(n,[1,2])

    def random_element(self):
        return Permutation(range(self.n,0,-1))

    def __iter__(self):
        yield Permutation(range(self.n,0,-1))

    def __len__(self):
        return 1
    
    def is_polynomial(self):
        return True


class PermutationsAvoiding10(_PermutationPatternClass):
    """Class for iterating through Permutations avoiding 21 of length n"""
    def __init__(self, n):
        super(PermutationsAvoiding10, self).__init__(n,[2,1])

    def random_element(self):
        return Permutation(range(1,self.n+1))

    def __iter__(self):
        yield Permutation(range(1,self.n+1))

    def __len__(self):
        return 1

    def is_polynomial(self):
        return True


class CatalanAvoidingClass(_PermutationPatternClass):
    def __len__(self):
        return catalan(self.n)

    def is_polynomial(self):
        return False


class PermutationsAvoiding012(CatalanAvoidingClass):
    def __init__(self,n):
        super(PermutationsAvoiding012, self).__init__(n,[1,2,3])

    def __iter__(self):

        if self.n == 0:
            yield Permutation([])
            return
        elif self.n <3:
            for p in Permutations(self.n):
                yield p
            return
        elif self.n ==3:
            for p in Permutations(self.n):
                if p!= Permutation([1,2,3]):
                    yield p
            return

        for p in PermutationsAvoiding021(self.n):
            # use simion-schmidt bijection
            m = self.n + 1
            minima = []
            minima_positions = []
            for index, value in enumerate(p):
                if value < m:
                    minima_positions.append(index)
                    minima.append(value)
                    m = value
            new_perm = []
            non_minima = [x for x in range(self.n, 0, -1) if x not in minima]
            a = 0
            b = 0
            for i in range(self.n):
                if i in minima_positions:
                    new_perm.append( minima[a] )
                    a += 1
                else:
                    new_perm.append( non_minima[b] )
                    b += 1
            yield Permutation(new_perm)


class PermutationsAvoiding021(CatalanAvoidingClass):
    """Class for iterating through Permutations avoiding 132 of length n"""
    def __init__(self, n):
        super(PermutationsAvoiding021, self).__init__(n,[1,3,2])

    def __iter__(self):

        if self.n == 0:
            yield Permutation([])
            return
        elif self.n < 3:
            for p in Permutations(self.n):
                yield p
            return
        elif self.n == 3:
            for p in Permutations(self.n):
                if p != Permutation([1,3,2]):
                    yield p
            return

        for left_length in range(0,self.n):
            right_length = self.n - 1 - left_length
            for left in PermutationsAvoiding021(left_length):
                for right in PermutationsAvoiding021(right_length):

                    yield Permutation([x + right_length for x in left]
                                         + [self.n]
                                         + list(right))
        return


class PermutationsAvoiding102(CatalanAvoidingClass):
    """Class for iterating through Permutations avoiding 213 of length n"""
    def __init__(self, n):
        super(PermutationsAvoiding102, self).__init__(n,[2,1,3])

    def __iter__(self):
        for p in PermutationsAvoiding021(self.n):
            yield p.reverse().complement()


class PermutationsAvoiding120(CatalanAvoidingClass):
    """Class for iterating through Permutations avoiding 231 of length n"""
    def __init__(self, n):
        super(PermutationsAvoiding120, self).__init__(n,[2,3,1])

    def __iter__(self):
        for p in PermutationsAvoiding021(self.n):
            yield p.reverse()


class PermutationsAvoiding201(CatalanAvoidingClass):
    """Class for iterating through Permutations avoiding 312 of length n"""
    def __init__(self, n):
        super(PermutationsAvoiding201, self).__init__(n,[3,1,2])

    def __iter__(self):
        for p in PermutationsAvoiding021(self.n):
            yield p.complement()


class PermutationsAvoiding210(CatalanAvoidingClass):
    def __init__(self,n):
        super(PermutationsAvoiding210, self).__init__(n,[3,2,1])

    def __iter__(self):
        for p in PermutationsAvoiding012(self.n):
            yield p.reverse()

# # Will return the set of polynomial types it intersects with (W_++, W+-, W^-1 ++, L_2, L_2^R etc)
# # 1: W++, 2: W+-, 3: W-+, 4: W--, 5: Winv++, 6: Winv+-, 7: Winv-+, 8: Winv--, 9: L2, 10: L2inv
def types(perm):
    interset = set([])
    for i in range(len(perm)+1):
        part1 = perm[0:i]
        part2 = perm[i:]

        if is_incr(part1):
            if is_incr(part2):
                interset.add(1)
            if is_decr(part2):
                interset.add(2)

        if is_decr(part1):
            if is_incr(part2):
                interset.add(3)
            if is_decr(part2):
                interset.add(4)

    flipperm = perm.inverse()
    for i in range(len(perm)+1):
        part1 = flipperm[0:i]
        part2 = flipperm[i:]

        if is_incr(part1):
            if is_incr(part2):
                interset.add(5)
            if is_decr(part2):
                interset.add(6)

        if is_decr(part1):
            if is_incr(part2):
                interset.add(7)
            if is_decr(part2):
                interset.add(8)
    if in_L2(perm):
        interset.add(9)
    if in_L2([perm[i] for i in range(len(perm)-1,-1,-1)]):
        interset.add(10)
    return interset

# TODO: When Permutation inherits from tuple, this function should no longer be
# necessary.
def is_decr(L):
    for i in range(len(L) - 1):
        if L[i] < L[i+1]:
            return False
    return True

# TODO: When Permutation inherits from tuple, this function should no longer be
# necessary.
def is_incr(L):
    for i in range(len(L) - 1):
        if L[i] > L[i+1]:
            return False
    return True


# TODO: When Permutation inherits from tuple, move this into Permutation.py?
def in_L2(L):
    n = len(L)
    if n == 0 or n == 1:
        return True
    if L[-1] == n:
        return in_L2(L[0:n-1])
    elif L[-1] == n-1 and L[-2] == n:
        return in_L2(L[0:n-2])
    else:
        return False
