from mutagen.mp4 import MP4, MP4Cover, error

TEMPLATE_METADATA = {
    '\xa9nam': ['Mice On Venus'],  # track title
    '\xa9ART': ['C418'],  # album artist
    'aART': ['C418'],  # artist
    '\xa9alb': ['Minecraft - Volume Alpha'],  # album
    'trkn': [(11, 24)],  # track number / total
    '\xa9day': ['2011'],  # year
    'covr': None
}


def save_metadata(audio_filename, title, artist, album_artist, album, track, track_total, date, cover_filename):
    f = MP4(audio_filename)

    try:
        f.add_tags()
    except error:
        pass

    f['\xa9nam'] = [title]
    f['\xa9ART'] = [artist]
    f['aART'] = [album_artist]
    f['\xa9alb'] = [album]
    f['trkn'] = [(track, track_total)]
    f['\xa9day'] = [str(date)]

    with open(cover_filename, "rb") as cover_file:
        f["covr"] = [
                MP4Cover(cover_file.read(), imageformat=MP4Cover.FORMAT_JPEG)
            ]

    f.save()
