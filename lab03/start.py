#!/usr/bin/python

import sys
import os
import re

from nltk import Text
from nltk.tokenize.moses import MosesTokenizer#, MosesDetokenizer

import urllib
from bs4 import BeautifulSoup

import time

def bib_it(filename_input, filename_output, language, search):
	tokenizer = MosesTokenizer()
	# detokenizer = MosesDetokenizer()

	pattern = r'(\\begin{document}\n*\\maketitle\n*)(.*?)(\n*\\end{document})'

	with open(filename_input, 'r+') as file:
		raw = file.read()
		raw_text = re.findall(pattern, raw, re.DOTALL)[0][1]

		tokens = tokenizer.tokenize(raw_text)
		t = Text(tokens)
		t.collocations()

		bib_file = open(filename_output, 'w')
		bib_file.truncate()

		for collocation in t._collocations:
			string = ' '.join(collocation)
			bibtex = search(string)

			name = re.findall(r'@\w+{(\w+)', bibtex)[0]
			raw_text = raw_text.replace(string, '{0} \\cite{{{1}}}'.format(string, name))

			bib_file.write('\n' + ' '.join(bibtex.split()) + '\n')

		bib_file.close()

		with_cite = raw_text # detokenizer.detokenize(t.tokens, return_str=True)

		with_cite += '\n\\\\bibliographystyle{plain}\n\\\\bibliography{bibfile}'

		new = re.compile(pattern, re.DOTALL).sub('\\1 {0} \\3'.format(with_cite), raw)
		file.seek(0)
		file.truncate()
		file.write(new)

def citeseerx_search(query):
	time.sleep(0.5)
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