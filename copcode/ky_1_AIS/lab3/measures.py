import numpy as np

# Евклидова мера близости
def Euclidean_measure(node1, node2):
    evk = Minkowski_measure(2, node1, node2)
    return evk


# Расстояние городских кварталов
def City_block_distance(node1, node2):
    city = Minkowski_measure(1, node1, node2)
    return city


# Косинусная мера близости
def Cosine_measure(node1, node2):
    sumMulty = 0
    for elem in range(len(node1)):
        sumMulty += node1[elem] * node2[elem]
    
    sum1 = 0
    for elem in range(len(node1)):
        sum1 += pow(node1[elem], 2)
    sum1 = pow(sum1, 1/2)
    
    sum2 = 0
    for elem in range(len(node2)):
        sum2 += pow(node2[elem], 2)
    sum2 = pow(sum2, 1/2)
    
    return (sumMulty / (sum1 * sum2))


# Расстояние Чебышева
def Chebyshev_measure(node1, node2):
    distance = []
    for elem in range(len(node1)):
        cur_dist = abs(node1[elem] - node2[elem])
        distance.append(cur_dist)
    
    return max(distance)


# Расстояние Минковского
def Minkowski_measure(p, node1, node2):
    sumMink = 0
    for elem in range(len(node1)):
        curDiff = abs(node1[elem] - node2[elem])
        sumMink += pow(curDiff, p)
    
    return pow(sumMink, 1/p)


# Ассоциативная мера
def Associative_measure(node1, node2):
    cnt_similars = 0
    cnt = 0
    for elem in range(len(node1)):
        if node1[elem] == node2[elem]:
            cnt_similars += 1
        cnt += 1

    return cnt_similars / cnt


# Мера Жаккарда
def Jaccard_measure(node1, node2):
    node1_set = set(node1)
    node2_set = set(node2)
    
    shared = node1_set.intersection(node2_set)
    total = node1_set.union(node2_set)
    
    return len(shared) / len(total)


# Древесная мера
def get_path_to_root(tree, node):
    for cur_node in tree:
        if "Name" in cur_node and cur_node["Name"] == node.name:
            path = cur_node["parent"]
    return path

def get_distance_by_path(path1, path2):
    common = sum(1 for i in path1 if i in path2)
    distance = len(path1) + len(path2) - 2 * common
    return distance

def Tree_measure(tree, node1, node2):
    path1 = get_path_to_root(tree, node1)
    path2 = get_path_to_root(tree, node2)

    if (type(path1[0]) is not list and type(path2[0]) is not list):
        distance = get_distance_by_path(path1, path2)

    elif (type(path1[0]) is list and type(path2[0]) is not list):
        distance1 = get_distance_by_path(path1[0], path2)
        distance2 = get_distance_by_path(path1[1], path2)
        distance = [distance1, distance2]

    elif (type(path1[0]) is not list and type(path2[0]) is list):
        distance1 = get_distance_by_path(path1, path2[0])
        distance2 = get_distance_by_path(path1, path2[1])
        distance = [distance1, distance2]

    elif (type(path1[0]) is list and type(path2[0]) is list):
        distance11 = get_distance_by_path(path1[0], path2[0])
        distance12 = get_distance_by_path(path1[0], path2[1])
        distance21 = get_distance_by_path(path1[1], path2[0])
        distance22 = get_distance_by_path(path1[1], path2[1])
        distance = [distance11, distance12, distance21, distance22]

    return distance


def get_correlation_matix(data, metric):
    matrix = []
    n = data.shape[0]

    for i in range(n):
        cur_vector = []

        for j in range(n):
            if (metric == Minkowski_measure):
                measure = metric(0.5, data.values.tolist()[i], data.values.tolist()[j])
            else:
                measure = metric(data.values.tolist()[i], data.values.tolist()[j])
            cur_vector.append(measure)
        matrix.append(np.array(cur_vector))

    matrix = np.array(matrix)
    return matrix


# def compare_vector(vector1, vector2):
#     vector_compare = []
    
#     n = len(vector1)
#     for i in range(n):
#         cur_elem = abs(vector1[i] - vector2[i])
#         vector_compare.append(cur_elem)

#     return vector_compare

# def compare_matrices(matrix1, matrix2):
#     matrix_compare = []
    
#     n = len(matrix1)
#     for i in range(n):
#         vector_compare = compare_vector(matrix1[i], matrix2[i])
#         matrix_compare.append(vector_compare)

#     print(matrix1[0])
#     print(matrix2[0])

#     return matrix_compare
