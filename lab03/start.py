#!/usr/bin/python

import sys
import os

from pylatexenc.latex2text import LatexNodes2Text

def bib_it(filename, language):
	tex2text = LatexNodes2Text()
	with open(filename, 'r+') as file:
		raw = file.read()
		text = tex2text.latex_to_text(raw)
		print(text)

def main():
	filename = sys.argv[1]
	try:
		language = sys.argv[3]
	except IndexError:
		language = 'english' # english wa defaruto language
	bib_it(filename, language)

if __name__ == '__main__':
	main()