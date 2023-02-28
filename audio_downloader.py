from pytube.contrib.playlist import Playlist
from parsers import select_audio_stream
from metadata_handler import save_metadata
from cover_downloader import download_cover
from tqdm import tqdm
import os
import argparse
import re
from mutagen.mp4 import MP4StreamInfoError


class StreamNotFoundError(Exception):
    pass


def download_playlist(playlist_url, album, file_name_prefix, fetch_thumbnail=True):
    album = re.sub('[^A-Za-z0-9 ]+', '', album)  # avoid illegal folder name
    file_name_prefix = re.sub('[^A-Za-z0-9_]+', '', file_name_prefix)  # avoid illegal file name

    output_folder = os.path.join('downloads', album)
    if not os.path.isdir(output_folder):
        os.makedirs(output_folder)

    downloaded_files = [f for f in os.listdir(output_folder) if os.path.isfile(os.path.join(output_folder, f))
                        if f[-4:] == '.m4a']

    playlist = Playlist(playlist_url)
    track_total = playlist.length

    # download cover if necessary
    cover_filename = os.path.join(output_folder, file_name_prefix + '_cover.jpg')
    if fetch_thumbnail or not os.path.isfile(cover_filename):
        download_cover(playlist.video_urls[0], cover_filename)

    # fetch metadata
    iterator = tqdm(playlist.videos)

    for track_idx, yt_video in enumerate(iterator):
        track = track_idx + 1
        artist, album_artist = yt_video.author, yt_video.author
        iterator.set_description('Video {}/{}'.format(track, track_total))
        local_filename = file_name_prefix + '_' + str(track_idx + 1) + '.m4a'
        filename = os.path.join(output_folder, local_filename)
        date = yt_video.publish_date
        title = yt_video.title

        # find a 128kbps audio track to download
        selection = select_audio_stream(yt_video.streams)
        if not selection:
            raise StreamNotFoundError
        stream = selection[0]

        try:
            # the file is already downloaded, only need to update the number of tracks in metadata
            if local_filename not in downloaded_files:
                stream.download(output_path=output_folder, filename=local_filename)

            # if the file was already there, over-write metadata
            save_metadata(filename, title, artist, album_artist, album, track, track_total, date, cover_filename)

        except (KeyError, MP4StreamInfoError) as e:
            pass

    print('Finished downloading', album)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--playlist_url', type=str, required=True)
    parser.add_argument('--album', type=str, required=True)
    parser.add_argument('--file_name_prefix', '--prefix', type=str, required=True)
    parser.add_argument('--manual_cover_art', action='store_true')
    args = parser.parse_args()
    download_playlist(args.playlist_url, args.album, args.file_name_prefix, not args.manual_cover_art)
