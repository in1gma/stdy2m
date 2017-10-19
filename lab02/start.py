#!/usr/bin/python

import os
import sys

from pylatexenc.latex2text import LatexNodes2Text


def read_files(folder):
    tex2text = LatexNodes2Text()
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r+') as file:
            text = tex2text.latex_to_text(file.read())

def main():
    folder = sys.argv[1]
    read_files(folder)
        

if __name__ == '__main__':
    main()