import os
import json
import shutil


def get_io_config() -> dict:
    """
    TODO DOCUMENTATION
    :return:
    """
    io_config_file = "src/configs/IO_config.json"
    io_config = json.loads(open(io_config_file).read())
    return io_config


def get_tmp_folder():
    """
    TODO DOCUMENTATION
    :return:
    """
    io_config = get_io_config()
    if not os.path.isdir(io_config['tmp_folder']):
        os.mkdir(io_config['tmp_folder'])
    return io_config['tmp_folder']


def check_file(path):
    """
    TODO DOCUMENTATION
    :param path:
    :return:
    """
    if not os.path.isfile(path):
        raise FileNotFoundError("File not found")


def read_json(path):
    """
    TODO DOCUMENTATION
    :param path:
    :return:
    """
    with open(path) as f:
        data = json.load(f)
    return data


def save_json(data, path):
    with open(path, 'w') as out:
        json.dump(data, out, indent=4, ensure_ascii=False)
    return path


def clean_tmp_folder() -> None:
    """
    TODO DOCUMENTATION
    :return:
    """
    shutil.rmtree(get_tmp_folder())
