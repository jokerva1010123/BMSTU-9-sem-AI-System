import random
from .population import Individual


def invert_bit_mutation(individual: Individual) -> None:
    mutated_gen_index = random.randint(0, len(individual.chromosome.gene_values) - 1)
    individual.chromosome.genes[mutated_gen_index].invert_value()