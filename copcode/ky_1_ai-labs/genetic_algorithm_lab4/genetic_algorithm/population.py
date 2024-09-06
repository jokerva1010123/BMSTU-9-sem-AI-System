from __future__ import annotations
import random
from typing import List
import copy


class Population:
    def __init__(
            self,
            fitness_function,
            selection_function,
            crossing_function,
            mutation_function,
            chromosomes: List[Chromosome] = None,
            members: List[Individual] = None,
            size: int = None,
            chromosome_len: int = None,

    ):
        self._fitness_function = fitness_function
        self._selection_function = selection_function
        self._crossing_function = crossing_function
        self._mutation_function = mutation_function
        assert bool(chromosomes) + bool(members) + bool(size and chromosome_len) == 1
        if chromosomes:
            self.members: List[Individual] = \
                [Individual(fitness_function, chromosome=chromosome) for chromosome in chromosomes]
        elif members:
            self.members: List[Individual] = members
        elif size and chromosome_len:
            self.members: List[Individual] = \
                [Individual(fitness_function, chromosome_len=chromosome_len) for i in range(size)]

    def get_n_best_members(self, n):
        sorted_chromosomes = [member.chromosome for member in self.members]
        sorted_chromosomes = sorted(sorted_chromosomes, key=self._fitness_function)
        sorted_chromosomes.reverse()
        return [Individual(self._fitness_function, chromosome=copy.deepcopy(chromosome)) for chromosome in sorted_chromosomes][:n]

    def select(self):
        self.members = self._selection_function(self, n=3)

    def mutate(self, mutation_probability: float = 0.1) -> None:
        for member in self.members:
            if random.random() < mutation_probability:
                self._mutation_function(member)

    def crossover(self, crossover_probability: float = 0.9):
        for parent1, parent2 in zip(self.members[::2], self.members[1::2]):
            if random.random() < crossover_probability:
                self._crossing_function(parent1, parent2)

    def __len__(self):
        return len(self.members)

    def __str__(self):
        global LOG
        res = f'Population: members number {len(self.members)} '
        if len(self.members) < 10:
            res += '\nMembers:\n'
            for member in self.members:
                res += f'{member}\n'
            LOG += res
        else:
            LOG += res
            for member in self.members:
                LOG += f'{member.fitness} '
            LOG += '\n'

            res += '\nThere are too many members to display\n'
        return res


class Gene:
    def __init__(self, value):
        self.value = value

    def invert_value(self):
        self.value = 0 if self.value == 1 else 1

    def __str__(self):
        return str(self.value)


class Chromosome:
    def __init__(self, genes: List[Gene]):
        self.genes: List[Gene] = genes

    @property
    def gene_values(self) -> List:
        return [gene.value for gene in self.genes]

    def __str__(self):
        return str(self.gene_values)

    def __len__(self):
        return len(self.genes)


class Individual:
    def __init__(
            self,
            fitness_function,
            other: Individual = None,
            chromosome: Chromosome = None,
            chromosome_len: int = None
    ):
        assert bool(other) + bool(chromosome) + bool(chromosome_len) == 1
        if other:
            self.chromosome: Chromosome = other.chromosome
        elif chromosome_len:
            self.chromosome: Chromosome = Chromosome([Gene(random.randint(0, 1)) for i in range(chromosome_len)])
        elif chromosome:
            self.chromosome: Chromosome = chromosome
        self.fitness_calculator = fitness_function

    @property
    def fitness(self) -> int:
        return self.fitness_calculator(self.chromosome)

    def __len__(self):
        return len(self.chromosome)

    def __str__(self):
        if len(self.chromosome) <= 10:
            return f'{self.chromosome} fitness: {self.fitness}'
        else:
            return f'Индивид с хромосомой длиной {len(self.chromosome)} fitness: {self.fitness}'