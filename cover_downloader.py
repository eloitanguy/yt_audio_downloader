from PIL import Image
import urllib.request
from io import BytesIO


def download_cover(video_url: str, filename: str):
    video_id = video_url[video_url.find('=') + 1:]
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
