#!/usr/bin/python

import os
import sys

from pylatexenc.latex2text import LatexNodes2Text
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser

def annotate_it(folder):
    tex2text = LatexNodes2Text()
    tokenizer = Tokenizer('english') # english wa default language
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r+') as file:
            text = tex2text.latex_to_text(file.read())
            parser = PlaintextParser(text, tokenizer)
            

def main():
    folder = sys.argv[1]
    annotate_it(folder)
        

if __name__ == '__main__':
    main()