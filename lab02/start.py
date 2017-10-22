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
            summary = '\n'.join([str(s) for s in summarizer(parser.document, sentences_count)]);
            # rated_sentences = text_rank_summarizer.rate_sentences(parser.document) # check rank

            pattern = re.compile(r'(\\begin{abstract}\n*)(.*?)(\n*\\end{abstract})', re.DOTALL)
            match = pattern.search(raw)
            if match is None:
                with_abstract = re.sub(r'(\\maketitle)', '\\1 \n{0}\n{1}\n{2}'.format('\\\\begin{abstract}', summary, '\\end{abstract}'), raw)
            else:
                with_abstract = pattern.sub('\\1 {0} \\3'.format(summary), raw)

            file.seek(0)
            file.write(with_abstract)

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