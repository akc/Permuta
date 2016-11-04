from permuta.misc import left_floor_and_ceiling
import collections
import itertools
import numbers
import sys
if sys.version_info.major is 2:
    range = xrange

class Permutation(object):
    """A permutation class.

    This class is immutable by agreement.
    """

    __slots__ = (
                  "_perm"
                , "_hash_result"
                , "_pattern_details_result"
                )

    def __init__(self, l, check=False):
        """Create a new Permutation with the given list.

        This does not create a copy of the given list.
        Supply a copy of the list if you plan on mutating the original.

        Args:
            self:
                A permutation.
            l: [int]
                A list corresponding to a legal permutation.
                Can also be an iterable.
            check: bool
                If True, l will be confirmed to be a legal permutation.
        """
        if check:
            assert isinstance(l, collections.Iterable), "Non-iterable argument: {}".format(l)
            try:
                n = len(l)
            except TypeError:
                n = sum(1 for _ in l)
            used = [False]*n
            for x in l:
                assert isinstance(x, numbers.Integral), "Non-integer type: {}".format(repr(x))
                assert 1 <= x <= n, "Out of range: {}".format(x)
                assert not used[x-1], "Duplicate element: {}".format(x)
                used[x-1] = True
        self._perm = l if type(l) is list else list(l)
        self._hash_result = None
        self._pattern_details_result = None

    def contained_in(self, *perms):
        """Check if self is a pattern of perms.

        Args:
            self:
                A classical pattern.
            perms: [permuta.Permutation]
                A list of permutations.

        Returns: bool
            True iff self is a pattern of all permutations in perms.
        """
        return all(self in perm for perm in perms)

    def contains(self, *patts):
        """Check if self contains patts.

        Args:
            self:
                A permutation.
            patts: [permuta.Permutation|permuta.MeshPattern]
                A list of classical/mesh patterns.

        Returns: bool
            True iff all patterns in patt are contained in self.
        """
        return all(patt in self for patt in patts)

    def avoids(self, *patts):
        """Check if self avoids patts.

        Args:
            self:
                A permutation.
            patts: [permuta.Permutation|permuta.MeshPattern]
                A list of classical/mesh patterns.

        Returns: bool
            True iff self avoids all patterns in patts.
        """
        return all(patt not in self for patt in patts)

    def avoided_by(self, *perms):
        """Check if self is avoided by perms.

        Args:
            self:
                A classical pattern.
            perms: [permuta.Permutation]
                A list of permutations.

        Returns: bool
            True iff every permutation in perms avoids self.
        """
        return all(self not in perm for perm in perms)

    def count_occurrences_in(self, perm):
        """Count the number of occurrences of self in perm.

        Args:
            self:
                A classical pattern.
            perm: permuta.Permutation
                A permutation.

        Returns: int
            The number of times self occurs in perm.
        """
        return sum(1 for _ in self.occurrences_in(perm))

    def count_occurrences_of(self, patt):
        """Count the number of occurrences of patt in self.

        Args:
            self:
                A permutation.
            patt: permuta.Permutation|permuta.MeshPattern
                A classical/mesh pattern.

        Returns: int
            The number of times patt occurs in self.
        """
        return patt.count_occurrences_in(self)

    def occurrences_in(self, perm):
        """Find all indices of occurrences of self in perm.

        Args:
            self:
                The classical pattern whose occurrences are to be found.
            perm: permuta.Permutation
                The permutation to search for occurrences in.

        Yields: [int]
            The indices of the occurrences of self in perm.
            Each yielded element l is a list of integer indices of the
            permutation perm such that:
            self == permuta.Permutation.to_standard([perm[i] for i in l])
        """
        # Special cases
        if len(self._perm) == 0:
            # Pattern is empty, occurs in all permutations
            # This is needed for the occurrences function to work correctly
            yield []
            return
        if len(self._perm) > len(perm._perm):
            # Pattern is too long to occur in permutation
            return

        # The indices of the occurrence in perm
        occurrence_indices = [None]*len(self._perm)

        # Get left to right scan details
        pattern_details = self._pattern_details()

        # Upper and lower bound declarations
        upper_bound = None
        lower_bound = None

        # Define function that works with the above defined variables
        # i is the index of the element in perm that is to be considered
        # k is how many elements of the permutation have already been added to occurrence
        def occurrences(i, k):
            elements_remaining = len(perm) - i
            elements_needed = len(self._perm) - k

            # Get the following variables:
            #   - lfi: Left Floor Index
            #   - lci: Left Ceiling Index
            #   - lbp: Lower Bound Pre-computation
            #   - ubp: Upper Bound pre-computation
            lfi, lci, lbp, ubp = pattern_details[k]

            # Set the bounds for the new element
            if lfi is None:
                # The new element of the occurrence must be at least self[k];
                # i.e., the k-th element of the pattern
                # lbp = self[k]
                lower_bound = lbp
            else:
                # The new element of the occurrence must be at least as far
                # from its left floor as self[k] is from its left floor
                # lbp = self[k] - self[lfi]
                occurrence_left_floor = perm[occurrence_indices[lfi]]
                lower_bound = occurrence_left_floor + lbp
            if lci is None:
                # The new element of the occurrence must be at most 
                # ubp = len(self) - self[k]
                upper_bound = len(perm._perm) - ubp
            else:
                # ubp = diff
                upper_bound = perm[occurrence_indices[lci]] - ubp

            # Loop over remaining elements of perm (actually i, the index)
            while 1:
                if elements_remaining < elements_needed:
                    # Can't form an occurrence with remaining elements
                    return
                element = perm[i]
                if lower_bound <= element <= upper_bound:
                    occurrence_indices[k] = i
                    if elements_needed == 1:
                        # Yield occurrence
                        yield occurrence_indices[:]
                    else:
                        # Yield occurrences where the i-th element is chosen
                        for o in occurrences(i+1, k+1):
                            yield o
                # Increment i, that also means elements_remaining should decrement
                i += 1
                elements_remaining -= 1

        for o in occurrences(0, 0):
            yield o

    def occurrences_of(self, patt):
        """Find all indices of occurrences of patt in self.

        This method is complementary to permuta.Permutation.occurrences_in.
        It just calls patt.occurrences_in(self) internally.
        See permuta.Permutation.occurrences_in for documentation.

        Args:
            self:
                A permutation.
            perm: permuta.Permutation
                A classical pattern.

        Yields: [int]
            The indices of the occurrences of self in perm.
        """
        return patt.occurrences_in(self)

    def _pattern_details(self):
        """Subroutine of occurrences_in method."""
        # If details have been calculated before, return cached result
        if self._pattern_details_result is not None:
            return self._pattern_details_result
        result = []
        index = 0
        for fac in left_floor_and_ceiling(self._perm):
            base_element = self._perm[index]
            left_floor = 1 if fac.floor is None else self._perm[fac.floor]
            left_ceiling = len(self._perm) if fac.ceiling is None else self._perm[fac.ceiling]
            left_floor_difference = base_element - left_floor
            left_ceiling_difference = left_ceiling - base_element
            compiled = (
                         fac.floor
                       , fac.ceiling
                       , self._perm[index] if fac.floor is None else left_floor_difference
                       , len(self._perm) - self._perm[index] if fac.ceiling is None else left_ceiling_difference
                       )
            result.append(compiled)
            index += 1
        self._pattern_details_result = result
        return result

    def inverse(self):
        """Return the inverse of the permutation self."""
        n = len(self._perm)
        result = [None]*n
        for i in range(n):
            result[self._perm[i]-1] = i + 1
        return Permutation(result)

    def reverse(self):
        """Return the reverse of the permutation self."""
        return Permutation(self._perm[::-1])

    def complement(self):
        """Return the complement of the permutation self."""
        base = len(self._perm) + 1
        return Permutation(base - e for e in self._perm)

    def reverse_complement(self):
        """Return the reverse complement of self.

        Equivalent to two left or right rotations.
        """
        base = len(self._perm) + 1
        return Permutation(base - e for e in reversed(self._perm))

    def shift(self, n=1):
        """Return self shifted n steps to the right.

        If n is negative, shifted to the left.
        """
        if len(self._perm) is 0:
            return self
        n = n % len(self._perm)
        if n is 0:
            return self
        index = len(self._perm) - n
        slice_1 = itertools.islice(self._perm, index)
        slice_2 = itertools.islice(self._perm, index, len(self._perm))
        return Permutation(itertools.chain(slice_2, slice_1))

    shift_right = shift
    cyclic_shift = shift
    cyclic_shift_right = shift

    def shift_left(self, n=1):
        """Return self shifted n steps to the left.

        If n is negative, shifted to the right.
        """
        return self.shift_right(-n)

    cyclic_shift_left = shift_left

    def shift_up(self, n=1):
        """Return self shifted n steps up.

        If n is negative, shifted down.
        """
        if len(self._perm) < 2:
            return self
        n = n % len(self._perm)
        if n is 0:
            return self
        bound = len(self._perm) - n
        return Permutation(e - bound if e > bound else e + n for e in self._perm)

    def shift_down(self, n=1):
        """Return self shifted n steps down.

        If n is negative, shifted up.
        """
        return self.shift_up(-n)

    def flip_horizontal(self):
        """Return self flipped horizontally."""
        return self.complement()

    def flip_vertical(self):
        """Return self flipped vertically."""
        return self.reverse()

    def flip_diagonal(self):
        """Return self flipped along the diagonal, y = x."""
        return self.inverse()

    def flip_antidiagonal(self):
        """Return self flipped along the antidiagonal, y = len(perm) - x."""
        n = len(self._perm)
        result = [None]*n
        for i, e in ((n-e, n-i) for i, e in enumerate(self._perm)):
            result[i] = e
        return Permutation(result)

    def rotate(self, n=1):
        "Return self rotated 90 degrees to the right."""
        return self._rotate(n)

    rotate_right = rotate

    def rotate_left(self, n=1):
        "Return self rotated 90 degrees to the left."""
        return self._rotate(-n)

    def _rotate(self, n=1):
        "Return self rotated 90 times n degrees to the right."""
        n = n % 4
        if n is 0:
            return self
        elif n is 1:
            return self._rotate_right()
        elif n is 2:
            return self.reverse_complement()
        else:
            return self._rotate_left()

    def _rotate_right(self):
        "Return self rotated 90 degrees to the right."""
        len_perm = len(self._perm)
        result = [None]*len_perm
        for i, v in enumerate(self._perm):
            result[v-1] = len_perm - i
        return Permutation(result)

    def _rotate_left(self):
        "Return self rotated 90 degrees to the left."""
        len_perm = len(self._perm)
        result = [None]*len_perm
        for i, v in enumerate(self._perm):
            result[len_perm - v] = i + 1
        return Permutation(result)

    def is_increasing(self):
        """Return True if the permutation is increasing, and False otherwise."""
        for i in range(len(self._perm)):
            if self._perm[i] is not i+1:
                return False
        return True

    def is_decreasing(self):
        """Return True if the permutation is decreasing, and False otherwise."""
        len_perm = len(self._perm)
        for i in range(len_perm):
            if self._perm[i] is not len_perm - i:
                return False
        return True

    @classmethod
    def to_standard(cls, lst):
        """Return the permutation corresponding to lst."""
        n = len(lst)
        result = [None]*n
        for j, (x, i) in enumerate(sorted((lst[i], i) for i in range(n))):
            result[i] = j + 1
        return cls(result)

    def __call__(self, lst):
        """Return the result of applying self to lst."""
        assert len(lst) == len(self._perm)
        return [lst[i-1] for i in self._perm]

    def __getitem__(self, i):
        return self._perm[i]

    def __len__(self):
        return len(self._perm)

    def __iter__(self):
        return iter(self._perm)

    def __str__(self):
        return str(self._perm)

    def __repr__(self):
        return "Permutation(%s)" % repr(self._perm)

    def __eq__(self, other):
        return type(other) is Permutation and self._perm == other._perm

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return (len(self), self._perm) < (len(other), other._perm)

    def __hash__(self):
        if self._hash_result is None:
            self._hash_result = hash(tuple(self._perm))
        return self._hash_result

    def __contains__(self, patt):
        """Check if self contains patt.

        Args:
            self:
                A permutation.
            patt: permuta.Permutation|permuta.MeshPattern
                A classical/mesh pattern.

        Returns: bool
            True iff the pattern patt is contained in self.
        """
        return any(True for _ in patt.occurrences_in(self))
