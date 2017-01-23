from itertools import combinations


__all__ = ["partitionings"]


def partitionings_ala_permuta(balls, bins):
    for partitioning in partitionings_helper([0]*bins, 0, balls):
        yield partitioning


def partitionings_helper(partitioning, bin_number, balls_left):
    if balls_left == 0:
        yield tuple(partitioning)
    elif bin_number == len(partitioning) - 1:
        # Last bin: put all balls left in the bin and then take them back out
        bins_already_in_bin = partitioning[bin_number]
        partitioning[bin_number] += balls_left
        yield tuple(partitioning)
        partitioning[bin_number] = bins_already_in_bin
    else:
        # Put 0 to balls_left balls into bin
        for balls in range(0, balls_left + 1):
            partitioning[bin_number] = balls
            for derived_partitioning in partitionings_helper(partitioning, bin_number + 1, balls_left - balls):
                yield derived_partitioning
        # Set bin to be empty again
        partitioning[bin_number] = 0


def partitionings_itertools(n, k):
    # Got this from a stackoverflow thread:
    # http://stackoverflow.com/a/28969798
    for c in combinations(range(n + k - 1), k - 1):
        yield tuple(b - a - 1 for a, b in zip((-1,) + c, c + (n + k - 1,)))


# The itertools partitioning seems to be faster with smaller numbers
# However, when the numbers are bigger, the permuta implementation seems faster
partitionings = partitionings_ala_permuta
