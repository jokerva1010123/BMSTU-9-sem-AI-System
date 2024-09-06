from pandas_ods_reader import read_ods
from tabulate import tabulate
import numpy as np
import json

import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

def get_data_from_ods(ods_path):
    data = read_ods(ods_path, 1, headers=True)
    data.index = data.index + 1
    return data

def get_data_from_json(json_path):
    with open(json_path) as f:
        data = json.load(f)
    return data

def write_data_to_html(data, html_path):
    f = open(html_path, 'w')
    f.write(tabulate(data, headers="keys", tablefmt='html'))


def plot_matrix(matrix, n, title):
    plt.imshow(matrix)
    plt.title(title)
    
    plt.colorbar()
    plt.xticks(np.arange(0, n, step=3))
    plt.yticks(np.arange(0, n, step=2))


def plot_matrices(matrix1, title1, matrix2, title2, \
                    matrix3, title3, matrix4, title4,\
                    matrix5, title5, matrix6, title6, \
                    matrix7, title7):
    n = matrix1.shape[0]

    plt.subplot(241)
    plot_matrix(matrix1, n, title1)

    plt.subplot(242)
    plot_matrix(matrix2, n, title2)

    plt.subplot(243)
    plot_matrix(matrix3, n, title3)

    plt.subplot(244)
    plot_matrix(matrix4, n, title4)

    plt.subplot(245)
    plot_matrix(matrix5, n, title5)

    plt.subplot(246)
    plot_matrix(matrix6, n, title6)

    plt.subplot(247)
    plot_matrix(matrix7, n, title7)
    
    plt.show()
