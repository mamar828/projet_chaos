import os


def get_path(relative_path):
    return os.path.join(os.path.dirname(__file__), relative_path)
