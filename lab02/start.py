#!/usr/bin/python

import os
import sys

def read_files(path):
    for filename in os.listdir(path):
        buf = open(os.path.join(path, filename), 'r').read()

def main():
    path = sys.argv[1]
    read_files(path)

if __name__ == '__main__':
    main()
