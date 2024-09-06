from Generator import *
from Terminal import *
from EventModel import *
from Device import *
from LoadBalancer import LoadBalancer

import numpy as np
from scipy import interpolate

def getAvgWaitingTime(p, samples):
    sum_y = 0
    for _ in range(samples):
        terminal = Terminal()

        devices = [
            Device("ОA", timeDistribution=generatorGauss(1, 0), next=terminal.process),
        ]

        # capacity=-1 -- очередь бесконечная
        storage: LoadBalancer = LoadBalancer("Буфер", devices, terminal, capacity=-1)

        generator: Generator = Generator(generatorExponent(1 / p), storage.process)

        eventModel: EventModel = EventModel(terminal)
        eventModel.addEvents(generator.process())

        eventModel.run(maxTimeModulation = 1000)
        
        sum_y += storage.totalWaitingTime / storage.processedRequest
    return sum_y / samples

import matplotlib.pyplot as plt
import matplotlib as mpl
def create_graph():
    i = 0.001
    mas = [0]
    res = [0]
    while i < 1:
        #print(i)
        mas.append(i)

        # экспоненциальный шаг
        if i < 0.7:
            res.append(getAvgWaitingTime(i, 100))
            i += 0.15 * (1.01 - i)
        else:
            res.append(getAvgWaitingTime(i, 500))
            di = 0.6 * abs(0.9 - i)
            if di < 0.025:
                di = 0.025
            i += di

    i = 1
    mas.append(i)
    res.append(getAvgWaitingTime(i, 100))

    mpl.style.use('seaborn')
    plt.scatter(mas, res, color='orange', s=10, marker='o')

    p = np.linspace(0, 1, 300)
    t_avg = interpolate.interp1d(mas, res, kind = 'cubic')#, fill_value="extrapolate")
    #plt.plot(mas, res, '-', p, t_avg(p), '--')
    plt.plot(p, t_avg(p), '-')
    #plt.plot(mas, res, '-')

    plt.grid(True)
    plt.title("Генератор: равномерный; ОА: экспоненциальный")
    plt.ylabel('Время ожидания заявки в очереди')
    plt.xlabel('Загрузка системы')
    plt.show()

if __name__ == "__main__":
    terminal = Terminal()

    l_coming = 5
    mu_handling = 3
    sigma_handling = 1

    maxTimeModulation = 100

    device = Device("ОA", timeDistribution=generatorExponent(1 / mu_handling), next=terminal.process)

    # capacity=-1 -- очередь бесконечная
    storage: LoadBalancer = LoadBalancer("Буфер", [device], terminal, capacity=-1)

    #generator: Generator = Generator(generatorExponent(1 / l_coming), storage.process)
    generator: Generator = Generator(generatorUD(1 / mu_handling, 1 / sigma_handling), storage.process)

    eventModel: EventModel = EventModel(terminal)
    eventModel.addEvents(generator.process())
    eventModel.run(maxTimeModulation = maxTimeModulation)

    print(f"Эксп. обработанных заявок: {terminal.processed:.2f} ({terminal.lastRequest.time:.1f} min)")

    #print(f"max queue length storage: {storage.maxQueue}")
    print(f"Эксп. ср. время ожидания: {storage.totalWaitingTime / (storage.processedRequest + len(storage.queue)):.2f} min")

    print(f"Эксп. интенсивность генератора: {generator.Lambda:.2f}")
    print(f"Эксп. интенсивность ОА: {device.Mu:.2f}")
    print(f"Эксп. загрузка СМО: {generator.Lambda / device.Mu:.2f}")

    # если загрузка > 1 - нестационарный режим (неустоявшийся)
    p = mu_handling / l_coming
    print(f"Теор. загрузка СМО: {p:.2f}")

    # Работает, только для экспоненциальных законов
    #print(f"Вероятность что ОА занят: {p:.2f}")

    # avg_size = p * p / (1 - p)
    #print(f"Ср. длина очереди: {avg_size:.2f}")

    # avg_t = avg_size / l_coming
    # print(f"Ср. время ожидания: {avg_t:.2f}")

    print(f"Теор. обработанных заявок: {maxTimeModulation * min(l_coming, mu_handling):.2f} ({maxTimeModulation:.2f} min)")

    create_graph()
