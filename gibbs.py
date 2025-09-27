#!/usr/bin/env python3

import sys, zipfile, os, re


EXTENSIONS = ('.flac', '.mp3', 'wav')
VERSION = '1.0.0'

def unzip(file, dest):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(dest)

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def rename(album, old_name):
    if os.path.exists(os.path.join(album, old_name)) and old_name.endswith(EXTENSIONS):
        dash = ' - '
        buff = old_name.split(dash)
        buff2 = buff[0].split('.')
        buff.pop(0)
        dash.join(buff)
        new_name = buff2[0] + ' - ' + buff[0]
        if not os.path.exists(new_name):
            os.rename(os.path.join(album, old_name), os.path.join(album, new_name))

def is_zip_file(path):
    return os.path.isfile(path) and path.endswith('.zip')

def prepare_album(file):
    pattern = r'\s*\(\d{4}\)$'
    album = os.path.splitext(file)[0]        
    buff = album.split(' - ')
    if len(buff) > 1:
        buff.pop(0)
        dash = ' - '
        album = dash.join(buff)
    album = re.sub(pattern, '', album)
    album.strip()
    return os.path.join(destination_arg,album)

def extract_file(file):
    if file.endswith('.zip'):
            album = prepare_album(file)
            mkdir(album)
            unzip(os.path.join(dir_arg, file), album)
            for file in os.listdir(album):
                rename(album, file)

def dir_loop(dir):
    if os.path.isdir(dir):
        for file in os.listdir(dir):
            extract_file(file)


args = sys.argv[1:]

for arg in args:
    if arg == '-h' or arg == '--help':
        print("Usage: gibbs <directory_or_zip_file> <destination_directory>")
        sys.exit(0)
    elif arg == '-v' or arg == '--version':
        print(VERSION)
        sys.exit(0)

if len(args) < 2:
    print("Error: Not enough arguments provided.")
    sys.exit(1)

destination_arg = os.path.abspath(args[1])
dir_arg = os.path.abspath(args[0])

if os.path.isdir(dir_arg):
    dir_loop(dir_arg)
elif is_zip_file(dir_arg):
    file_arg = os.path.basename(dir_arg)
    dir_arg = os.path.dirname(dir_arg)
    extract_file(file_arg)
