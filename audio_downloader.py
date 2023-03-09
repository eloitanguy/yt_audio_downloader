from pytube.contrib.playlist import Playlist
from parsers import select_audio_stream
from metadata_handler import save_metadata
from cover_downloader import download_cover
from tqdm import tqdm
import os
import argparse
import re
from mutagen.mp4 import MP4StreamInfoError
from pytube.exceptions import PytubeError
from pytube import YouTube
from urllib.error import HTTPError


class StreamNotFoundError(Exception):
    pass


def download_track(yt_video, file_name_prefix, output_folder, album, cover_filename=None, track_idx=None,
                   track_total=None, downloaded_files=None, n_tries=10, fetch_thumbnail=True):
    if track_idx is None or track_total is None or cover_filename is None:  # single track
        local_filename = file_name_prefix + '.m4a'
        cover_filename = cover_handler(output_folder, file_name_prefix, yt_video, fetch_thumbnail)
        track, track_total = 1, 1
    else:
        local_filename = file_name_prefix + '_' + str(track_idx + 1) + '.m4a'
        track = track_idx + 1
    filename = os.path.join(output_folder, local_filename)

    if downloaded_files is None:
        downloaded_files = []

    error_count = 0
    while error_count < n_tries:
        try:
            # find a 128kbps audio track to download
            selection = select_audio_stream(yt_video.streams)
            if not selection:
                raise StreamNotFoundError
            stream = selection[0]

            # the file is already downloaded, only need to update the number of tracks in metadata
            # if the file is downloaded but with a size < 1kB, re-download (broken download)
            if (local_filename not in downloaded_files) or \
                    (local_filename in downloaded_files and os.stat(filename).st_size < 1024):
                stream.download(output_path=output_folder, filename=local_filename)

            # if the file was already there, over-write metadata
            artist, album_artist = yt_video.author, yt_video.author
            date = yt_video.publish_date
            title = yt_video.title
            save_metadata(filename, title, artist, album_artist, album, track, track_total, date, cover_filename)
            break

        except (StreamNotFoundError, KeyError, MP4StreamInfoError, PytubeError, HTTPError) as e:
            error_count += 1
            print('File {} failed to download, caught {}, attempt [{}/{}]'.format(local_filename, str(e),
                                                                                  error_count, n_tries))


def cover_handler(output_folder, file_name_prefix, yt_video, fetch_thumbnail):
    cover_filename = os.path.join(output_folder, file_name_prefix + '_cover.jpg')
    if fetch_thumbnail or not os.path.isfile(cover_filename):
        download_cover(yt_video, cover_filename)
    return cover_filename


def download_playlist(playlist_url, album, file_name_prefix, fetch_thumbnail=True, n_tries=10):
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
    cover_filename = cover_handler(output_folder, file_name_prefix, playlist.videos[0], fetch_thumbnail)

    # fetch metadata
    iterator = tqdm(playlist.videos)

    for track_idx, yt_video in enumerate(iterator):
        iterator.set_description('Video {}/{}'.format(track_idx + 1, track_total))
        download_track(yt_video, file_name_prefix, output_folder, album, cover_filename, track_idx,
                       track_total, downloaded_files, n_tries, fetch_thumbnail=False)

    print('Finished downloading', album)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--playlist_url', default='', type=str)
    parser.add_argument('--video_url', default='', type=str)
    parser.add_argument('--album', type=str, required=True)
    parser.add_argument('--file_name_prefix', '--prefix', type=str, required=True)
    parser.add_argument('--manual_cover_art', action='store_true')
    args = parser.parse_args()

    if args.playlist_url != '':
        download_playlist(args.playlist_url, args.album, args.file_name_prefix, not args.manual_cover_art)
    elif args.video_url != '':
        yt_video = YouTube(args.video_url)
        output_folder = os.path.join('downloads', args.album)
        if not os.path.isdir(output_folder):
            os.mkdir(output_folder)
        download_track(yt_video, args.file_name_prefix, output_folder, args.album, cover_filename=None, track_idx=None,
                       track_total=None, downloaded_files=None, n_tries=10, fetch_thumbnail=not args.manual_cover_art)
