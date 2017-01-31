import random

from permuta import Perm

from .PermSetStatic import PermSetStatic


class PermSetPoint(PermSetStatic):
    perm = Perm((0,))
    perm_set = PermSetStatic([perm])

    __instance = None  # Singleton class

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(PermSetPoint, cls).__new__(args, kwargs)
        return cls.__instance

    @property
    def generating_function(self):
        raise NotImplementedError

    def of_length(self, length):
        if length == 1:
            return self.perm_set
        else:
            return PermSetStatic()

    def random(self):
        return self.perm

    def __contains__(self, item):
        return isinstance(item, Perm) and item == self.perm

    def __getitem__(self, key):
        if key == 0:
            return self.perm
        else:
            raise IndexError

    def __iter__(self):
        self._iter = not None
        return self

    def __next__(self):
        if self._iter is None:
            raise StopIteration
        else:
            self._iter = None
            return self.perm

    def __repr__(self):
        return "<PermSet(Perm((0,)))>>".format(len(self._tuple))

    def __str__(self):
        return "the point perm set".format(len(self._tuple))
