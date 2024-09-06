from functools import reduce
from math import sqrt

from ttypes.data import \
    ExtendedLeafData, \
    EXTENDED_LEAF_DATA_NORMALIZED_FIELDS, \
    EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS


def calculate_manhattan_distance(x: ExtendedLeafData, y: ExtendedLeafData) -> float:
    return sqrt(
        reduce(
            lambda acc, cur:
                acc + EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS[cur] * abs(y.normalized[cur] - x.normalized[cur]),
            EXTENDED_LEAF_DATA_NORMALIZED_FIELDS,
            0.0
        )
    )
