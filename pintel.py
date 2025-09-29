#!/usr/bin/env python3

import sys, os

VERSION = '1.0.0'

def dir_loop(dir):
    for obj in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, obj)):
            dir_loop(os.path.join(dir, obj))
        elif obj.endswith(input_format):
            original_path = os.path.join(dir, obj)
            output_path = os.path.splitext(original_path)[0] + output_format
            if not os.path.exists(output_path):
                cmd_exec = 'ffmpeg -i \"%s\" -ab 192k \"%s\"'   % (original_path, output_path)
                print(f"Converting {original_path} to {output_path}")
                os.system(cmd_exec)
                if os.path.exists(output_path):
                    os.remove(original_path)

args = sys.argv[1:]

input_format = '.flac'
output_format = '.mp3'
directory = None

i = 0
while i < len(args):
    arg = args[i]
    
    if arg == '-h' or arg == '--help':
        print("Pintel converts audio files")
        print("Usage: pintel <directory> -i <input_format> -o <output_format>")
        print("Default value for input_format = mp3 output_format = flac")
        sys.exit(0)
    elif arg == '-v' or arg == '--version':
        print(VERSION)
        sys.exit(0)
    elif arg == '-i':
        if i + 1 < len(args):
            input_format = '.' + args[i + 1]
            i += 1
        else:
            print("Error: -i requires an input format")
            sys.exit(1)
    elif arg == '-o':
        if i + 1 < len(args):
            output_format = '.' + args[i + 1]
            i += 1
        else:
            print("Error: -o requires an output format")
            sys.exit(1)
    elif not arg.startswith('-'):
        if directory is None:
            directory = arg
        else:
            print("Error: Multiple directories specified")
            sys.exit(1)
    else:
        print(f"Error: Unknown option {arg}")
        sys.exit(1)
    
    i += 1

if directory is None:
    print("Error: No directory specified.")
    sys.exit(1)

dir = os.path.abspath(directory)

if os.path.isdir(dir):
    dir_loop(dir)
else:
    print(f"Error: {dir} is not a directory.")
    sys.exit(1)
