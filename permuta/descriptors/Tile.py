from .Perm import Perm
from .PermSet import PermSet


class Tile(object):
    "An enum used to represent different tiles in tilings"
    #INPUT_SET = X = "Input set"
    I = INDEFINITE = 1  # pylint: disable=invalid-name
    A = ALL_PERMS = PermSet()  # pylint: disable=invalid-name
    P = POINT_PERM_SET = PermSet([Perm()])  # pylint: disable=invalid-name
    INCREASING = PermSet.avoiding(Perm((1, 0)))
    DECREASING = PermSet.avoiding(Perm((0, 1)))
