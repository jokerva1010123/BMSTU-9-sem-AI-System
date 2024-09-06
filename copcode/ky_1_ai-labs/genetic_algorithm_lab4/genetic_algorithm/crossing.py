import random
from .population import Individual, Chromosome


def one_point_crossing(parent1: Individual, parent2: Individual) -> None:
    """
    Одноточечное скрещивание. Выбирается случайный индекс хромосомы, по которому она делится на 2 половины.
    Затем первый потомок получает гены первого родителя до индекса s и гены второго родителя начиная с индекса s, а
    второй потомок получает гены второго родитля до индекса s и гены первого родителя начиная с индекса s
    """
    s = random.randint(2, len(parent1)-3)  # TODO почему с 2, а не с 1?
    parent1_genes = parent1.chromosome.genes
    parent1.chromosome.genes[s:] = parent2.chromosome.genes[s:]
    parent2.chromosome.genes[s:] = parent1_genes[s:]
