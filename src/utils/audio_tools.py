from utils.IO import save_json, get_tmp_folder
from os import path


def mix_audio_trans(audio_info, trans):
    for i in audio_info:
        i['voices'] = get_text(trans, i['start_time'], i['end_time'])
    return save_json(audio_info, path.join(get_tmp_folder(), 'info.json'))


def get_text(trans, start, end):
    voices = []
    for tran in trans:
        if (tran['start'] <= start < tran['end']) or (start < tran['start'] < end):
            voice = {'voice': tran['voice'],
                     'start_time': max(tran['start'], start),
                     'end_time': min(tran['end'], end),
                     'trans': list(filter(
                         lambda x: (start < x['start_time'] < end),
                         tran['text']))}
            voices.append(voice)
        elif end < tran['start']:
            break
    return voices

if __name__ == '__main__':
    mix_audio_trans(mix_audio_trans())
