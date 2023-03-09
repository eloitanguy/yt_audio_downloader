# Youtube audio playlist downloader

A small script that will download an audio version of a youtube playlist, 
fill in some metadata and take the thumbnail of the first video as cover for each track.

Note that by default, the script will download 128kbps m4a files.

Further note that the script will check if a file was already downloaded, 
and if so will only update the metadata (to account for an increase in the total
amount of tracks in a playlist in particular).

## Setup

    pip install -r requirements.txt

## Running the script

Find the url of a playlist you want to download, it will look like 
'https://www.youtube.com/playlist?list=...'

In order to download to `downloads/album_name/` with files `prefix_1.m4a`, `prefix_2.m4a`
and so on, run:

    python audio_downloader.py --playlist_url <url> --album 'album_name' --file_name_prefix 'prefix'

On Windows, you can run 

    python .\audio_downloader.py --playlist_url <url> --album 'album_name' --file_name_prefix 'prefix'

In order to use a manually chosen cover image, use the option ``--manual_cover_art``, with the image placed under 
``downloads/<album_name>/<file_name_prefix>_cover.jpg``. If the file is not found, a thumbnail will be downloaded 
automatically.

## Single track download

    python audio_downloader.py --video_url <url> --album 'album_name' --file_name_prefix 'prefix'
