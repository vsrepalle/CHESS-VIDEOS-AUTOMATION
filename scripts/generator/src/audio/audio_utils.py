import os


def ensure_output_folder(folder):

    if not os.path.exists(folder):
        os.makedirs(folder)


def audio_exists(path):

    return os.path.exists(path)