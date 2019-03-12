import json
import time
import Pyro4

from ContainerHandler import ContainerHandler
from utils.IO import check_file, read_json, move_files
from utils.audio_tools import mix_audio_trans
from utils.lm_tools import get_sentences, get_words, generate_dic
from os import path

containers_list = ['G2P', 'SRILM', 'SPHINXBASE']


@Pyro4.expose
class TrainingHandler(ContainerHandler):

    def __init__(self, container_name, main_uri):
        super().__init__(container_name, main_uri)
        self.containers = {}

    def run(self, **kwargs):
        if 'input_json' in kwargs and 'output_folder' in kwargs:
            if all(i in self.containers.keys() for i in containers_list):
                self.running = True
                print("Container {}: Runned with {}".format(self.container_name, kwargs))
                result = self.process_training(json.loads(open(kwargs['input_json']).read()), kwargs['output_folder'])
                self.running = False
                return result
            else:
                raise ValueError("G2P, SRILM and SPHINXBASE containers are not registered")
        else:
            raise TypeError('input_json and output_folder required')

    def info(self):
        return self.running

    def slave_register(self, container, uri):
        """
        TODO DOCUMENTATION
        :param container:
        :return:
        """
        if container in containers_list and not (container in self.containers.keys()):
            self.containers[container] = uri
            print("Container {}: Registered slave <{}> with uri <{}>".format(self.container_name, container, uri))
            return True
        else:
            raise ValueError("<{}> is not a valid container name".format(container))
        pass

    def slave_unregister(self, container):
        """
        TODO DOCUMENTATION
        :param container:
        :return:
        """
        if container in self.containers:
            while self.running:
                time.sleep(1)

            del self.containers[container]
            print("Container {}: Unregistered slave <{}>".format(self.container_name, container))
            return True
        else:
            return False

    def process_training(self, audio_trans_info, output_folder):
        """
        TODO DOCUMENTATION
        :param audio_trans_info:
        :param output_folder:
        :return:
        """
        try:
            audio_path = audio_trans_info['audio_path']
            trans_path = audio_trans_info['transcription_path']

            response = []

            check_file(audio_path)
            info_audio = read_json(audio_path)

            check_file(trans_path)
            transcription = read_json(trans_path)

            info_path = mix_audio_trans(info_audio, transcription)
            response.append(info_path)

            senteces_path = get_sentences(info_path)
            print(senteces_path)

            words_path = get_words(info_path)
            print(words_path)

            # g2p_container = Pyro4.Proxy(self.containers['G2P'])
            print("G2P call")

            # srilm_container = Pyro4.Proxy(self.containers['SRILM'])
            print("SRILM call")

            # sphinxbase = Pyro4.Proxy(self.containers['SPHINXBASE'])
            print("SPHINXBASE call")

            return move_files(response, output_folder)

        except Exception as e:
            print("Container {} Error: {}".format(self.container_name, e))


if __name__ == '__main__':
    a = TrainingHandler("Training", "PYRO:MainController@localhost:4040")
    print(a.process_training(audio_trans_info=read_json("resources/input.json"), output_folder="/srv/shared_folder"))
