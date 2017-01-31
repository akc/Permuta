from builtins import dict
from collections import OrderedDict
from permuta._perm_set.finite import PermSetPoint

from .Descriptor import Descriptor


class Tiling(dict, Descriptor):
    """Tiling class.

    Coordinates/cells are tuples of (i, j) which work in the traditional matrix way.
    """

    __specified_labels = {}

    def __init__(self, tiles=()):
        info = []
        super(Tiling, self).__init__(self._init_helper(tiles, info))
        self._hash, self._max_i, self._max_j, self._total_point_tiles = info
        #for key, value in iteritems(tiles):
        #    print(key, value)
        #if isinstance(rule, list):
        #    self.rule = {(i, j): rule[i][j]
        #                 for i in range(len(rule))
        #                 for j in range(len(rule[i]))
        #                 if rule[i][j] is not None}
        #else:
        #    self.rule = {(i, j): s
        #                 for ((i,j), s) in rule.items()
        #                 if s is not None}

    def _init_helper(self, tiles, info):
        point_perm_set = PermSetPoint()
        total_point_tiles = 0
        hash_sum = 0
        max_i = 0
        max_j = 0
        for key_val in tiles.items():  # Builds the tuple in python2
            hash_sum += hash(key_val)
            (i, j), perm_set = key_val
            if perm_set is point_perm_set:
                total_point_tiles += 1
            max_i = max(max_i, i)
            max_j = max(max_j, j)
            yield key_val
        info.append(hash(hash_sum))
        info.append(max_i)
        info.append(max_j)
        info.append(total_point_tiles)

    @classmethod
    def label(cls, block, label):
        warnings.warn("Method signature may change", PendingDeprecationWarning)
        cls.__specified_labels[block] = label

    def __hash__(self):
        return self._hash

    def __repr__(self):
        format_string = "<A tiling of {} non-empty tiles>"
        return format_string.format(len(self))

    def __str__(self):
        max_i = self._max_i
        max_j = self._max_j

        result = []

        # Create tiling lines
        for i in range(2*max_i + 3):
            for j in range(2*max_j + 3):
                # Whether or not a vertical line and a horizontal line is present
                vertical = j % 2 == 0
                horizontal = i % 2 == 0
                if vertical:
                    if horizontal:
                        result.append("+")
                    else:
                        result.append("|")
                elif horizontal:
                    result.append("-")
                else:
                    result.append(" ")
            result.append("\n")

        labels = OrderedDict()

        # Put the sets in the tiles
        row_width = 2*max_j + 4
        for (i, j), perm_set in self.items():
            # Check if label has been specified
            specified_label = self.__specified_labels.get(perm_set)
            if specified_label is None:
                # Use generic label (could reuse specified label)
                label = labels.get(perm_set)
                if label is None:
                    label = str(len(labels) + 1)
                    labels[perm_set] = label
            else:
                # If label specified, then use it
                label = specified_label
            index = (2*i + 1)*row_width + 2*j + 1
            result[index] = label

        # Legend at bottom
        for perm_set, label in labels.items():
            result.append(label)
            result.append(": ")
            result.append(str(perm_set))
            result.append("\n")

        return "".join(result)
