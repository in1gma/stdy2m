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

import urllib
from bs4 import BeautifulSoup

def bib_it(filename_input, filename_output, language, search):
	tex2text = LatexNodes2Text()
	measures = AssocMeasures()

	stop_words = stopwords.words(language)
	allow_words = words.words()
	lemmatizer = Lemmatizer()

	with open(filename_input, 'r') as file:
		raw = file.read()
		text = tex2text.latex_to_text(raw)

		finder = CollocationFinder.from_words(wordpunct_tokenize(text))
		finder.apply_word_filter(lambda word: len(word) < 3 or word.lower() in stop_words)

		collocations = finder.nbest(measures.pmi, 100)

		bib_file = open(filename_output, 'w')

		for collocation in collocations:
			if any([word for word in collocation if lemmatizer.lemmatize(word.lower()) not in allow_words]):
				string = ' '.join(collocation)
				bibtex = search(string)

				bib_file.write('@comment{{{0}}}\n{1}\n'.format(string, bibtex))

		bib_file.close()

def citeseerx_search(query):
	site = 'http://citeseerx.ist.psu.edu'

	# first request
	search_url = site + '/search?' + urllib.parse.urlencode({ 'q': query })
	response = urllib.request.urlopen(search_url)

	soup = BeautifulSoup(response.read(), 'lxml')
	ref_url = site + soup.select_one('a.doc_details')['href'] # a.doc_details[href]

	# second request for bibtex
	response = urllib.request.urlopen(ref_url)

	soup = BeautifulSoup(response.read(), 'lxml')
	return soup.select_one('#bibtex p').getText()

def main():
	filename_input = sys.argv[1]
	filename_output = sys.argv[2]
	language = 'english' # english wa defaruto language

	bib_it(filename_input, filename_output, language, citeseerx_search)

if __name__ == '__main__':
	main()