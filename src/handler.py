import sys
from utils.IO import check_file, read_json, get_tmp_folder, save_json
from utils.audio_tools import mix_audio_trans
import json

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Pase la ruta de la informacion de audio + Ruta de la transcripcion")
        exit()
    try:
        audio_path = sys.argv[1]
        check_file(audio_path)
        info_audio = read_json(audio_path)

        trans_path = sys.argv[2]
        check_file(trans_path)
        transcription = read_json(trans_path)

        info_path = mix_audio_trans(info_audio, transcription)


    except Exception as e:
        print(e)
