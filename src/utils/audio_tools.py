def mix_audio_trans(audio_info, trans):
    for i in audio_info:
        i['voices'] = get_text(trans, i['start_time'], i['end_time'])

def get_text(trans, start, end):
    voices = []
    for tran in trans:
        if (tran['start'] <= start < tran['end']) or (start < tran['start'] < end):
            voice = {'voice': tran['voice'],
                     'start_time': tran['start'],
                     'end_time': tran['end'],
                     'trans': filter(
                         lambda x: (x['start_time'] <= start < x['end_time'] or (start < x['start_time'] < end)),
                         tran['text'])}
            voices.append(voice)
        elif end < tran['start']:
            break
    return voices
