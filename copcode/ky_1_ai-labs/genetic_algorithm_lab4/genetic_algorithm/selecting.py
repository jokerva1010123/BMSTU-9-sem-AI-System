import random
import copy
from typing import List
from .population import Population, Individual


def get_different_indexes(n: int, num: int):
    """
    Возвращает n различных индексов из последовательности из натурального ряда чисел (включая 0)  длиной num
    [0, 1, ..., num - 1]
    """
    assert num >= n
    numbers = list(range(num))
    indexes = []
    for i in range(n):
        index = random.randint(0, len(numbers) - 1)
        indexes.append(numbers.pop(index))
    return indexes


def tournament_selector(population: Population, n: int = 3) -> List[Individual]:
    """
    Из популяции случайно выбирается n объектов, среди них отбирается лучший.
    Он будет использован как родитель в операции скрещивания
    """
    parents: List[Individual] = []
    population_len = len(population)
    for i in range(population_len):
        indexes = get_different_indexes(n, population_len)

        parents.append(copy.deepcopy(max([population.members[i] for i in indexes], key=lambda ind: ind.fitness)))

    return parents


