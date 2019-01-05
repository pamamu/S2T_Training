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


def get_libs_config() -> dict:
    """
    TODO DOCUMENTATION
    :return:
    """
    libs_config_file = "src/configs/Libs_config.json"
    lib_config = json.loads(open(libs_config_file).read())
    return lib_config


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


def get_language_model_path():
    """
    TODO DOCUMENTATION
    :return:
    """
    lib_config = get_libs_config()
    if not os.path.isfile(lib_config['language_model_path']):
        raise FileNotFoundError()
    return lib_config['language_model_path']


def get_phonetic_model_path():
    """
    TODO DOCUMENTATION
    :return:
    """
    lib_config = get_libs_config()
    if not os.path.isfile(lib_config['phonetic_model_path']):
        raise FileNotFoundError()
    return lib_config['phonetic_model_path']


def get_acoustic_model_path():
    """
    TODO DOCUMENTATION
    :return:
    """
    lib_config = get_libs_config()
    if not os.path.isdir(lib_config['acoustic_model_path']):
        raise FileNotFoundError()
    return lib_config['acoustic_model_path']


def dic_path():
    """
    TODO DOCUMENTATION
    :return:
    """
    lib_config = get_libs_config()
    if not os.path.isfile(lib_config['dic_path']):
        raise FileNotFoundError()
    return lib_config['dic_path']


def srilm_bin_path():
    """
    TODO DOCUMENTATION
    :return:
    """
    lib_config = get_libs_config()
    if not os.path.isdir(lib_config['srilm_bin_path']):
        raise FileNotFoundError()
    return lib_config['srilm_bin_path']


def sequitu_bin_path():
    """
    TODO DOCUMENTATION
    :return:
    """
    lib_config = get_libs_config()
    if not os.path.isdir(lib_config['sequitu_bin_path']):
        raise FileNotFoundError()
    return lib_config['sequitu_bin_path']
