import matplotlib.pyplot as plt
import ast


def plot():
    with open('genetic_fitness_data.txt', 'r') as f:
        data = f.read()
        data = ast.literal_eval(data)

    max_fitness_values = data['max_fitness_values']
    avg_fitness_values = data['avg_fitness_values']

    fig, ax = plt.subplots()

    plt.plot(max_fitness_values, color='red', label='Максимальные значения приспособленности')
    plt.plot(avg_fitness_values, color='green', label='Средние значения приспособленности')
    plt.xlabel('Поколение')
    plt.ylabel('Приспособленность')
    plt.title('Зависимость приспособленности от поколения')

    ax.legend()

    plt.show()


if __name__ == "__main__":
    plot()