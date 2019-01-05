import subprocess
import os
from utils.IO import get_srilm_folder


def generate_model(text_file):
    max_order = 3
    command = os.path.join(get_srilm_folder(), 'ngram-count')
    model_file = text_file.split('.')[0] + '.lm'
    for order in reversed(range(0, max_order)):
        script = [str(command), '-text', str(text_file), '-order', str(order + 1), '-lm', str(model_file),
                  '-kndiscount']
        p = subprocess.Popen(script, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        a = p.wait()
        if a == 0:
            break
    return model_file


def check_models(models):
    print(models)
