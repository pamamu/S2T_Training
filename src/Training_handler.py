import json
import os.path
import time

import Pyro4

from ContainerHandler import ContainerHandler
from utils.IO import check_file, read_json, clean_tmp_folder, move_files, save_json, copy_file
from utils.audio_tools import mix_audio_trans
from utils.lm_tools import get_sentences, get_words

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
        if container in containers_list:
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
            # response.append(info_path)

            senteces_path = get_sentences(info_path)
            print(senteces_path)

            words_path = get_words(info_path)
            print(words_path)

            move_files([senteces_path, words_path], output_folder)

            copy_file(audio_path, os.path.join(output_folder, 'info.json'))

            print("G2P call")
            g2p_container = Pyro4.Proxy(self.containers['G2P'])
            # g2p_container = Pyro4.Proxy('PYRO:G2P@172.19.0.4:40420')
            g2p_response = g2p_container.run(input_json=os.path.join(output_folder, 'input_g2p.json'),
                                             output_folder=output_folder)
            response.append(g2p_response[0])
            print("G2P OK")

            print("SRILM call")
            srilm_container = Pyro4.Proxy(self.containers['SRILM'])
            # srilm_container = Pyro4.Proxy('PYRO:SRILM@172.19.0.5:40450')
            srilm_response = srilm_container.run(input_json=os.path.join(output_folder, 'input_srilm.json'),
                                                 output_folder=output_folder)
            # response.append(srilm_response[0])
            print("SRILM OK")

            # print("SPHINXBASE call")
            # sphinxbase_container = Pyro4.Proxy(self.containers['SPHINXBASE'])
            # # sphinxbase_container = Pyro4.Proxy('PYRO:SPHINXBASE@172.19.0.8:40410')
            # sphinxbase_response = sphinxbase_container.run(
            #     input_json=os.path.join(output_folder, 'input_sphinxbase.json'),
            #     output_folder=output_folder)
            # reduced_model = sphinxbase_container.reduce_language_model(srilm_response[0],
            #                                                            os.path.join(output_folder,
            #                                                                         'language_model.lm.bin'))
            # response.append(reduced_model)
            # response.append(sphinxbase_response)
            print("SPHINXBASE OK")

            # clean_tmp_folder()

            response_json = save_json(response, os.path.join(output_folder, 'output_training.json'))
            return response_json

        except Exception as e:
            print("Container {} Error: {}".format(self.container_name, e))


if __name__ == '__main__':
    a = TrainingHandler("Training", "PYRO:MainController@localhost:4040")
    print(a.process_training(audio_trans_info=read_json("/srv/shared_folder/input_training.json"),
                             output_folder="/srv/shared_folder"))
