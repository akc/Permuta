
from itertools import product
from permuta import Perm
from permuta.descriptors import Tiling
from permuta.misc import ordered_set_partitions, flatten
from permuta._perm_set.finite import StaticPermSet
from permuta._perm_set.finite import PointPermSet

from ..PermSetDescribed import PermSetDescribed


class TilingPermSet(PermSetDescribed):
    descriptor_class = Tiling

    def __init__(self, descriptor):
        super(TilingPermSet, self).__init__(descriptor)
        self.tiling = descriptor

    def __str__(self):
        return "a tiling perm set"

    def __repr__(self):
        return "<A tiling perm set>"


class TilingPermSetGeneric(TilingPermSet):
    """A perm set containing all perms that can be generated with a tiling."""
    descriptor = None

    point_perm_set = PointPermSet()

    def __contains__(self, item):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    def __len__(self):
        raise NotImplementedError

    def of_length(self, n):
        perms = set()

        tiling = list(self.tiling.items())
        h = max( k[0] for k,v in tiling ) + 1 if tiling else 1
        w = max( k[1] for k,v in tiling ) + 1 if tiling else 1

        def permute(arr, perm):
            res = [None] * len(arr)
            for i in range(len(arr)):
                res[i] = arr[perm[i]]
            return res

        def count_assignments(at, left):

            if at == len(tiling):
                if left == 0:
                    yield []
            elif tiling[at][1] is TilingPermSetGeneric.point_perm_set:
                # this doesn't need to be handled separately,
                # it's just an optimization
                if left > 0:
                    for ass in count_assignments(at + 1, left - 1):
                        yield [1] + ass
            else:
                for cur in range(left+1):
                    for ass in count_assignments(at + 1, left - cur):
                        yield [cur] + ass

        for count_ass in count_assignments(0, n):

            cntz = [ [ 0 for j in range(w) ] for i in range(h) ]

            for i, k in enumerate(count_ass):
                cntz[tiling[i][0][0]][tiling[i][0][1]] = k

            rowcnt = [ sum( cntz[row][col] for col in range(w) ) for row in range(h) ]
            colcnt = [ sum( cntz[row][col] for row in range(h) ) for col in range(w) ]

            for colpart in product(*[ ordered_set_partitions(range(colcnt[col]), [ cntz[row][col] for row in range(h) ]) for col in range(w) ]):
                scolpart = [ [ sorted(colpart[i][j]) for j in range(h) ] for i in range(w) ]
                for rowpart in product(*[ ordered_set_partitions(range(rowcnt[row]), [ cntz[row][col] for col in range(w) ]) for row in range(h) ]):
                    srowpart = [ [ sorted(rowpart[i][j]) for j in range(w) ] for i in range(h) ]
                    for perm_ass in product(*[ s[1].of_length(cnt) for cnt, s in zip(count_ass, tiling) ]):
                        arr = [ [ [] for j in range(w) ] for i in range(h) ]

                        for i, perm in enumerate(perm_ass):
                            arr[tiling[i][0][0]][tiling[i][0][1]] = perm

                        res = [ [None]*colcnt[col] for col in range(w) ]

                        cumul = 0
                        for row in range(h-1,-1,-1):
                            for col in range(w):
                                for idx, val in zip(scolpart[col][row], permute(srowpart[row][col], arr[row][col])):
                                    res[col][idx] = cumul + val
                            cumul += rowcnt[row]
                        perms.add(Perm(flatten(res)))
        return perms


TilingPermSet.default_subclass = TilingPermSetGeneric  # Set default Avoiding class to be dispatched
