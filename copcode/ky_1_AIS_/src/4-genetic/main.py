# genetic algorithm search for continuous function optimization
from numpy.random import randint
from numpy.random import rand


# objective function
def objective(x):
    return x[0] ** 2 + x[1] ** 2


# decode bitstring to numbers
def decode(bounds, n_bits, bitstring):
    decoded = list()
    largest = 2 ** n_bits
    for i in range(len(bounds)):
        # extract the substring
        start = i * n_bits
        end = start + n_bits
        substring = bitstring[start:end]

        # convert bitstring to a string of chars
        chars = ''.join([str(s) for s in substring])

        # convert string to integer
        integer = int(chars, 2)

        # scale integer to desired range
        value = bounds[i][0] + (integer/largest) * (bounds[i][1] - bounds[i][0])

        # store
        decoded.append(value)
    return decoded


# tournament selection
def selection(population, scores, k=3):
    # first random selection
    selection_ix = randint(len(population))
    for ix in randint(0, len(population), k-1):
        # check if better (e.g. perform a tournament)
        if scores[ix] < scores[selection_ix]:
            selection_ix = ix
    return population[selection_ix]


# crossover two parents to create two children
def crossover(p1, p2, r_cross):
    # children are copies of parents by default
    c1, c2 = p1.copy(), p2.copy()
    # check for recombination
    if rand() < r_cross:
        # select crossover point that is not on the end of the string
        pt = randint(1, len(p1)-2)
        # perform crossover
        c1 = p1[:pt] + p2[pt:]
        c2 = p2[:pt] + p1[pt:]
    return [c1, c2]


# mutation operator
def mutation(bitstring, r_mut):
    for i in range(len(bitstring)):
        # check for a mutation
        if rand() < r_mut:
            # flip the bit
            bitstring[i] = 1 - bitstring[i]


# genetic algorithm
def genetic_algorithm(objective, bounds, n_bits, n_iter, n_pop, r_cross, r_mut):
    r_mut0 = r_mut
    # initial population of random bitstring
    pop = [randint(0, 2, n_bits * len(bounds)).tolist() for _ in range(n_pop)]

    # keep track of best solution
    best, best_eval = 0, objective(decode(bounds, n_bits, pop[0]))

    # enumerate generations
    for gen in range(n_iter):
        # decode population
        decoded = [decode(bounds, n_bits, p) for p in pop]

        # evaluate all candidates in the population
        scores = [objective(d) for d in decoded]

        a = [[scores[i], i] for i in range(len(scores))]
        a.sort(key=lambda x: x[0])

        best_parents = []
        for i in range(10):
            best_parents.append(pop[a[i][1]])

        # check for new best solution
        for i in range(n_pop):
            if scores[i] < best_eval:
                best, best_eval = pop[i], scores[i]
                print(f'>{gen}, new best f({pop[i]}) = {scores[i]}')
        # select parents

        selected = [selection(pop, scores) for _ in range(n_pop)]
        # create the next generation
        children = list()

        if gen % 20:
            r_mut = 0.5
            if gen % 50:
                r_mut = 1.0
        else:
            r_mut = r_mut0

        # Вас не слышно

        for i in range(0, n_pop, 2):
            # get selected parents in pairs
            p1, p2 = selected[i], selected[i+1]
            # crossover and mutation
            for c in crossover(p1, p2, r_cross):
                # mutation
                mutation(c, r_mut)
                # store for next generation
                children.append(c)
        # replace population
        pop = best_parents + children

        if gen == n_iter - 1:
            best_eval_2 = 50
            for i in range(n_pop):
                if scores[i] < best_eval_2:
                    best, best_eval_2 = pop[i], scores[i]
                    print(f'LAST-GEN>{gen}, new best f({pop[i]}) = {scores[i]}')

    return [best, best_eval]


def main():
    # define range for input
    bounds = [[-5.0, 5.0], [-5.0, 5.0]]

    # define the total iterations
    n_iter = 500

    # bits per variable
    n_bits = 16

    # define the population size
    n_pop = 100

    # crossover rate
    r_cross = 0.9

    # mutation rate
    r_mut = 1.0 / (float(n_bits) * len(bounds))

    # perform the genetic algorithm search
    best, score = genetic_algorithm(objective, bounds, n_bits, n_iter, n_pop, r_cross, r_mut)

    print('Done!')
    decoded = decode(bounds, n_bits, best)

    print(f'f({decoded}) = {score}')


if __name__ == '__main__':
    main()
