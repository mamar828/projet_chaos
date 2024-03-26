from os.path import join, dirname


def get_path(relative_path):
    return join(dirname(__file__), relative_path)
