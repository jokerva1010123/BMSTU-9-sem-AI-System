from one_max import solve_with_genetic_algorithm, save_data_for_plot
#from plot_fitness_data import plot


def main():
    max_fitness_values, avg_fitness_values, generation_num, working_time, best_fitness = solve_with_genetic_algorithm(
        max_generations=100,
        population_size=100,
        chromosome_len=100,
        crossover_probability=0.5,
        mutation_probability=0.5,
        show_info=True,
        debug=True
    )
    save_data_for_plot(max_fitness_values, avg_fitness_values)
    # plot()


if __name__ == "__main__":
    main()