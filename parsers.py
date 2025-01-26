from pytubefix.query import StreamQuery


def select_audio_stream(stream_list: StreamQuery):
    t = stream_list.filter(only_audio=True)
    selection = [s for s in t if s.abr == '128kbps' and s.mime_type == 'audio/mp4']
    return selection
