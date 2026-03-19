#!/usr/bin/env python3
"""
Tag mka files using YouTube metadata fetched via yt-dlp,
then rename them to strip the YouTube video ID from the filename.

Expecting music files downloaded from OuterTune App
https://github.com/OuterTune/OuterTune

Usage:
    python ragetti.py <directory> [--write-tags] [--convert-mp3]
"""

import argparse
import os
import re
import subprocess
import sys

import yt_dlp


# Used a clanker to write the regex cuz I am not smart enough
FILENAME_PATTERN = re.compile(r'^(.+?) \[([A-Za-z0-9_-]{11})\]\.mka$')
ANY_MKA_PATTERN = re.compile(r'^(.+?)\.mka$')


def get_youtube_metadata(video_id: str) -> dict:
    url = f'https://www.youtube.com/watch?v={video_id}'
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)


def write_mka_tags(src_path: str, meta: dict) -> None:
    title = meta.get('title') or ''
    artists = meta.get('artists') 
    alt_artist = meta.get('channel') or meta.get('uploader') or ''
    artist = artists[0] if artists else alt_artist
    album = meta.get('album') or meta.get('playlist') or artist
    year = meta.get('release_year') or ''
    description = (meta.get('description') or '')[:500]
    youtube_id = meta.get('id') or ''

    tmp_path = src_path + '._tmp.mka'
    cmd = [
        'ffmpeg', '-y',
        '-i', src_path,
        '-c', 'copy',
        '-metadata', f'title={title}',
        '-metadata', f'artist={artist}',
        '-metadata', f'album={album}',
        '-metadata', f'date={year}',
        '-metadata', f'comment={description}',
        '-metadata', f'comment={youtube_id}',
        tmp_path,
    ]
    try:
        # TODO: Write tags without direct OS cmd
        subprocess.run(cmd, check=True, capture_output=True)
        os.replace(tmp_path, src_path)
    except subprocess.CalledProcessError as exc:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise RuntimeError(f'ffmpeg failed: {exc.stderr.decode(errors="replace")}') from exc


def convert_to_mp3(src_path: str) -> str:
    base = os.path.splitext(src_path)[0]
    mp3_path = base + '.mp3'

    cmd = [
        'ffmpeg', '-y',
        '-i', src_path,
        '-codec:a', 'libmp3lame',
        '-q:a', '0',
        mp3_path,
    ]
    try:
        # TODO: Convert to mp3 without direct OS cmd
        subprocess.run(cmd, check=True, capture_output=True)
        os.remove(src_path)
        return mp3_path
    except subprocess.CalledProcessError as exc:
        if os.path.exists(mp3_path):
            os.remove(mp3_path)
        raise RuntimeError(f'ffmpeg conversion failed: {exc.stderr.decode(errors="replace")}') from exc


def process_directory(directory: str, write_tags: bool, convert_mp3: bool) -> None:
    entries = sorted(os.listdir(directory))

    if write_tags:
        mka_files = [f for f in entries if FILENAME_PATTERN.match(f)]
    else:
        mka_files = [f for f in entries if ANY_MKA_PATTERN.match(f)]

    if not mka_files:
        print('No matching mka files found.')
        return

    for filename in mka_files:
        src_path = os.path.join(directory, filename)

        if write_tags:
            match = FILENAME_PATTERN.match(filename)
            song_name = match.group(1)
            video_id = match.group(2)

            print(f'[{video_id}] {song_name}')

            try:
                meta = get_youtube_metadata(video_id)
            except Exception as exc:
                print(f'  ERROR fetching metadata: {exc}', file=sys.stderr)
                continue

            try:
                write_mka_tags(src_path, meta)
            except Exception as exc:
                print(f'  ERROR writing tags: {exc}', file=sys.stderr)
                continue

            new_name = f'{song_name}.mka'
            new_path = os.path.join(directory, new_name)

            if os.path.exists(new_path):
                print(f'  SKIP rename — "{new_name}" already exists', file=sys.stderr)
                continue

            os.rename(src_path, new_path)
            print(f'  -> {new_name}')
            src_path = new_path
        else:
            print(filename)

        if convert_mp3:
            try:
                mp3_path = convert_to_mp3(src_path)
                print(f'  -> {os.path.basename(mp3_path)}')
            except Exception as exc:
                print(f'  ERROR converting to MP3: {exc}', file=sys.stderr)


def main() -> None:
    if '-h' in sys.argv or '--help' in sys.argv:
        print("Help")
        sys.exit()

    write_tags = False
    convert_mp3 = False

    if '--write-tags' in sys.argv:
        write_tags = True
    if '--convert-mp3' in sys.argv:
        convert_mp3 = True
        
    if not write_tags and not convert_mp3:
        print('Specify at least one action: --write-tags and/or --convert-mp3')
        sys.exit()
    if not os.path.isdir(sys.argv[-1]):
        print(f'Error: "{sys.argv[-1]}" is not a valid directory.', file=sys.stderr)
        sys.exit(1)

    process_directory(sys.argv[-1], write_tags=write_tags, convert_mp3=convert_mp3)


if __name__ == '__main__':
    main()
