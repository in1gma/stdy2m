#!/usr/bin/python

import sys
import os
import re

from nltk import word_tokenize
from nltk import Text
from nltk.collocations import TrigramCollocationFinder as CollocationFinder
from nltk.collocations import TrigramAssocMeasures as AssocMeasures
from nltk.corpus import stopwords
from nltk.corpus import words
from nltk.stem.wordnet import WordNetLemmatizer as Lemmatizer

from six import iteritems

import urllib
from bs4 import BeautifulSoup

import time

def bib_it(filename_input, filename_output, language, search):
	measures = AssocMeasures()

	stop_words = stopwords.words(language)
	allow_words = words.words()
	lemmatizer = Lemmatizer()

	pattern = r'(\\begin{document}\n*\\maketitle\n*)(.*?)(\n*\\end{document})'

	with open(filename_input, 'r+') as file:
		raw = file.read()
		text = re.findall(pattern, raw, re.DOTALL)[0][1]

		tokens = word_tokenize(text)
		finder = CollocationFinder.from_words(tokens)

		collocations = []

		for ngram, freq in iteritems(finder.ngram_fd):
			if (not any(len(word) < 3 or word.lower() in stop_words for word in ngram)):
				score = finder.score_ngram(measures.pmi, *ngram)
				# print(ngram, score)
				# print(ngram, freq)

		# collocations = finder.nbest(measures.pmi, 10)

		bib_file = open(filename_output, 'w')

		for collocation in collocations:
			if any([word for word in collocation if lemmatizer.lemmatize(word.lower()) not in allow_words]):
				string = ' '.join(collocation)
				bibtex = search(string)

				bib_file.write('@comment{{{0}}}\n{1}\n'.format(string, bibtex))

		bib_file.close()

		with_cite = ''

		with_cite += '\n\\\\bibliographystyle{plain}\n\\\\bibliography{bibfile}'

		new = re.compile(pattern, re.DOTALL).sub('\\1 {0} \\3'.format(with_cite), raw)
		file.seek(0)
		file.truncate()
		file.write(new)

def citeseerx_search(query):
	# time.sleep(0.5)
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