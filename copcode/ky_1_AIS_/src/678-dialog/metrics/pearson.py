from functools import reduce
from math import sqrt

from ttypes.data import \
    ExtendedLeafData, \
    EXTENDED_LEAF_DATA_NORMALIZED_FIELDS, \
    EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS


EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS_SUM = reduce(
    lambda acc, cur:
        acc + EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS[cur],
    EXTENDED_LEAF_DATA_NORMALIZED_FIELDS,
    0.0
)


def calculate_mean(x: ExtendedLeafData) -> float:
    return reduce(
        lambda acc, cur:
            acc + EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS[cur] * x.normalized[cur],
        EXTENDED_LEAF_DATA_NORMALIZED_FIELDS,
        0.0
    ) / EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS_SUM


def calculate_pearson_correlation_coefficient(x: ExtendedLeafData, y: ExtendedLeafData) -> float:
    mean_x = calculate_mean(x)
    mean_y = calculate_mean(y)

    covariance = 0.0
    variance_x = 0.0
    variance_y = 0.0
    for field in EXTENDED_LEAF_DATA_NORMALIZED_FIELDS:
        weight = EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS[field]
        dx = x.normalized[field] - mean_x
        dy = y.normalized[field] - mean_y
        covariance += weight * dx * dy
        variance_x += weight * dx ** 2
        variance_y += weight * dy ** 2

    return covariance / sqrt(variance_x * variance_y)
