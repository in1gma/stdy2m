#!/usr/bin/python

import os
import sys
import re

from pylatexenc.latex2text import LatexNodes2Text
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer # .lsa LsaSummarizer
# from sumy.summarizers.text_rank import TextRankSummarizer # check rank
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

def annotate_it(folder, language, sentences_count):
    tex2text = LatexNodes2Text()
    tokenizer = Tokenizer(language)
    stemmer = Stemmer(language)
    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(language)
    # text_rank_summarizer = TextRankSummarizer(stemmer) # check rank
    # text_rank_summarizer.stop_words = get_stop_words(language)
    for filename in os.listdir(folder):
        with open(os.path.join(folder, filename), 'r+') as file:
            raw = file.read()
            text = tex2text.latex_to_text(raw)
            parser = PlaintextParser(text, tokenizer)
            summary = summarizer(parser.document, sentences_count)
            # rated_sentences = text_rank_summarizer.rate_sentences(parser.document) # check rank
            # add summary to abstract or sciabstract after maketitle or before first section
            abstract = re.sub(r'\\begin{abstract}(.*?)\\end{abstract}', 'test', raw, re.DOTALL)
            print(abstract)

def main():
    folder = sys.argv[1]
    sentences_count = sys.argv[2]
    try:
        language = sys.argv[3]
    except IndexError:
        language = 'english' # english wa default language
    annotate_it(folder, language, sentences_count)

if __name__ == '__main__':
    main()