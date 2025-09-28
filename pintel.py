#!/usr/bin/env python3

import sys, os

VERSION = '1.0.0'

def dir_loop(dir):
    for obj in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, obj)):
            dir_loop(os.path.join(dir, obj))
        elif obj.endswith(input_format):
            original_path = os.path.join(dir, obj)
            mp3_path = os.path.splitext(original_path)[0] + '.mp3'
            if not os.path.exists(mp3_path):
                cmd_exec = 'ffmpeg -i \"%s\" -ab 192k \"%s\"'   % (original_path, mp3_path)
                print(f"Converting {original_path} to {mp3_path}")
                os.system(cmd_exec)
                os.remove(original_path)

args = sys.argv[1:]

for arg in args:
    if arg == '-h' or arg == '--help':
        print("Usage: pintel <directory> <input_format>")
        sys.exit(0)
    elif arg == '-v' or arg == '--version':
        print(VERSION)
        sys.exit(0)

if len(args) < 1:
    print("Error: Not enough arguments provided.")
    sys.exit(1)

dir = os.path.abspath(args[0])
input_format = '.' + args[1] if len(args) > 1 else '.flac'



if os.path.isdir(dir):
    dir_loop(dir)
else:
    print(f"Error: {dir} is not a directory.")
    sys.exit(1)