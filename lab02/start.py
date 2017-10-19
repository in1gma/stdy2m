#!/usr/bin/python

import os
import sys

def read_files(folder):
    for filename in os.listdir(folder):
        try:
            buf = open(os.path.join(folder, filename), 'r').read()
        except IsADirectoryError:
            continue

def main():
    folder = sys.argv[1]
    read_files(folder)

if __name__ == '__main__':
    main()
