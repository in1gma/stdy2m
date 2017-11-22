#!/usr/bin/python

import sys
import os

from pylatexenc.latex2text import LatexNodes2Text

from nltk import wordpunct_tokenize
from nltk.collocations import TrigramCollocationFinder as CollocationFinder
from nltk.collocations import TrigramAssocMeasures as AssocMeasures
from nltk.corpus import stopwords
from nltk.corpus import words
from nltk.stem.wordnet import WordNetLemmatizer as Lemmatizer

def bib_it(filename, language):
	tex2text = LatexNodes2Text()
	measures = AssocMeasures()
	stop_words = stopwords.words(language)
	allow_words = words.words()
	lemmatizer = Lemmatizer()
	with open(filename, 'r') as file:
		raw = file.read()
		text = tex2text.latex_to_text(raw)
		finder = CollocationFinder.from_words(wordpunct_tokenize(text))
		finder.apply_word_filter(lambda word: len(word) < 3 or word.lower() in stop_words)
		collocations = finder.nbest(measures.pmi, 100)
		for collocation in collocations:
			if any([word for word in collocation if lemmatizer.lemmatize(word.lower()) not in allow_words]):
				string = ' '.join(collocation)

def main():
	filename = sys.argv[1]
	try:
		language = sys.argv[3]
	except IndexError:
		language = 'english' # english wa defaruto language
	bib_it(filename, language)

if __name__ == '__main__':
	main()