import matplotlib.pyplot as plt


def plot(x: list, y: list, subplot:int):
    plt.subplot(subplot)
    plt.plot(x, y,'ro')


def show():
    plt.show()


