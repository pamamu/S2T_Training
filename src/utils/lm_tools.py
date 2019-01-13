import os

import subprocess

from utils.IO import get_srilm_bin_path, read_json, save_list, get_tmp_folder, check_file


def generate_model(text_file):
    max_order = 3
    command = os.path.join(get_srilm_bin_path(), 'ngram-count')
    model_file = text_file.split('.')[0] + '.lm'
    for order in reversed(range(0, max_order)):
        script = [str(command), '-text', str(text_file), '-order', str(order + 1), '-lm', str(model_file),
                  '-kndiscount']
        p = subprocess.Popen(script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        a = p.wait()
        if a == 0:
            break
    return model_file


def get_sentences(file_path):
    info_text = read_json(file_path)
    sentences = [[k['text'].lower() for k in j['trans']] for i in info_text for j in i['voices']]
    return save_list(sentences, os.path.join(get_tmp_folder(), 'sentences.txt'), 1)


def get_words(file_path):
    """
    TODO DOCUMENTATION
    :param file_path:
    :return:
    """
    info_text = read_json(file_path)
    words = [k['text'].lower() for i in info_text for j in i['voices'] for k in j['trans']]
    return save_list(words, os.path.join(get_tmp_folder(), 'words.txt'))


def check_models(models):
    print(models)


def generate_dic(words_path):
    destination_folder = os.path.join(get_tmp_folder(), 'words.dic')
    script = ['']

