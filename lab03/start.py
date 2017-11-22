#!/usr/bin/python

import sys
import os

from pylatexenc.latex2text import LatexNodes2Text

from nltk import wordpunct_tokenize
from nltk.collocations import TrigramCollocationFinder as CollocationFinder
from nltk.collocations import TrigramAssocMeasures as AssocMeasures
from nltk.corpus import stopwords as Stopwords

def bib_it(filename, language):
	tex2text = LatexNodes2Text()
	measures = AssocMeasures()
	stopwords = Stopwords.words(language)
	with open(filename, 'r+') as file:
		raw = file.read()
		text = tex2text.latex_to_text(raw)
		tokens = [x for x in wordpunct_tokenize(text) if x.lower() not in stopwords]
		finder = CollocationFinder.from_words(tokens)#, window_size=3)
		# finder.apply_freq_filter(1)
		# print(finder.score_ngrams(measures.raw_freq))
		print(finder.nbest(measures.pmi, 100)) # likelihood_ratio ~ 1000

def main():
	filename = sys.argv[1]
	try:
		language = sys.argv[3]
	except IndexError:
		language = 'english' # english wa defaruto language
	bib_it(filename, language)

if __name__ == '__main__':
	main()