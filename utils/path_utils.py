import os


def harmonize_path(path):
    """
    harmonizes path with the right separators for the current os

    :param path: input path
    :return: harmonized path with the right separators for the current os
    """
    path = path.replace('/', os.sep)
    path = path.replace('\\', os.sep)
    return path
