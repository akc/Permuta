import warnings


from permuta import Perm
from permuta.descriptors import Basis
from permuta.descriptors import Descriptor
from permuta._perm_set.finite import PermSetStatic
from permuta._perm_set.unbounded.all import PermSetAll
from permuta._perm_set.unbounded.described.avoiding import AvoidingGeneric


class Block(object):
    """Different blocks for Tilings, for convenience."""
    all = PermSetAll()
    point = PermSetStatic([Perm()])  # TODO: Make a new optimized perm set if this is a bottleneck
    increasing = AvoidingGeneric(Basis(Perm((1, 0))))
    decreasing = AvoidingGeneric(Basis(Perm((0, 1))))
    def __new__(_cls):
        warnings.warn("Block class should not be instantiated", Warning)
