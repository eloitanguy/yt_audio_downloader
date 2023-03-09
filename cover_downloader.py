from PIL import Image
import urllib.request
from io import BytesIO
from urllib.error import HTTPError


def download_cover(yt_video, filename):
    try:
        video_str = str(yt_video)
        video_id = video_str[video_str.find('=') + 1:]
        img_url = 'http://img.youtube.com/vi/{}/hqdefault.jpg'.format(video_id)
        u = urllib.request.urlopen(img_url)
        raw_data = u.read()
        u.close()
    except HTTPError:
        video_id = yt_video.video_id
        img_url = 'http://img.youtube.com/vi/{}/hqdefault.jpg'.format(video_id)
        u = urllib.request.urlopen(img_url)
        raw_data = u.read()
        u.close()
    im = Image.open(BytesIO(raw_data))
    w, h = im.size
    x = min(w, h)
    left = (w - x) // 2
    top = (h - x) // 2
    right = (w + x) // 2
    bottom = (h + x) // 2
    im = im.crop((left, top, right, bottom))
    im.save(filename)
