import genres.genres
import sys
import inspect
import json


def get_module_classes(module_name):
    return {name: cls for name, cls in inspect.getmembers(sys.modules[module_name], inspect.isclass)}


def find_children(father, classes):
    return [cls for cls in classes if cls.__bases__[0] == father]


def generate_dict_tree_from_classes(cls, classes):
    cls_name = cls.__name__
    tree = {cls_name: {}}
    for child in find_children(cls, classes.values()):
        tree[cls_name].update(generate_dict_tree_from_classes(child, classes))
    return tree


def get_nodes_from_classes(cls, classes, nodes):
    cls_name = cls.__name__
    nodes.append(cls_name)
    for child in find_children(cls, classes.values()):
        get_nodes_from_classes(child, classes, nodes)
    return nodes


def generate_json_class_tree():
    classes = get_module_classes("genres.genres")
    root_cls = classes['HipHop']
    dict_tree = generate_dict_tree_from_classes(root_cls, classes)
    with open('genres.json', 'w') as file:
        json.dump(dict_tree, file)


if __name__ == "__main__":
    classes = get_module_classes("genres.genres")
    root_cls = classes['HipHop']
    # dict_tree = generate_dict_tree_from_classes(root_cls, classes)
    # print(dict_tree)

