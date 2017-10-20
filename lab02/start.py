#!/usr/bin/python

import os
import sys

from pylatexenc.latex2text import LatexNodes2Text
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer # .lsa LsaSummarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

def annotate_it(folder, language, sentences_count):
    tex2text = LatexNodes2Text()
    tokenizer = Tokenizer(language)
    stemmer = Stemmer(language)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(language)
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r+') as file:
            text = tex2text.latex_to_text(file.read())
            parser = PlaintextParser(text, tokenizer)
            summary = summarizer(parser.document, sentences_count)

def main():
    folder = sys.argv[1]
    sentences_count = sys.argv[2]
    annotate_it(folder, 'english', sentences_count) # english wa default language

if __name__ == '__main__':
    main()