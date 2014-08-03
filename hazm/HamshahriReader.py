# coding: utf8

from __future__ import print_function
import os, sys, re
from xml.dom import minidom


class HamshahriReader():
	"""
	interfaces [Hamshahri Corpus](http://ece.ut.ac.ir/dbrg/hamshahri/files/HAM2/Corpus.zip) that you must download and extract it.
	"""

	def __init__(self, root='corpora/hamshahri'):
		self._root = root
		self._invalids = set(['hamshahri.dtd', 'HAM2-960622.xml', 'HAM2-960630.xml', 'HAM2-960701.xml', 'HAM2-960709.xml', 'HAM2-960710.xml', 'HAM2-960711.xml', 'HAM2-960817.xml', 'HAM2-960818.xml', 'HAM2-960819.xml', 'HAM2-960820.xml', 'HAM2-961019.xml', 'HAM2-961112.xml', 'HAM2-961113.xml', 'HAM2-961114.xml', 'HAM2-970414.xml', 'HAM2-970415.xml', 'HAM2-970612.xml', 'HAM2-970614.xml', 'HAM2-970710.xml', 'HAM2-970712.xml', 'HAM2-970713.xml', 'HAM2-970717.xml', 'HAM2-970719.xml', 'HAM2-980317.xml', 'HAM2-040820.xml', 'HAM2-040824.xml', 'HAM2-040825.xml', 'HAM2-040901.xml', 'HAM2-040917.xml', 'HAM2-040918.xml', 'HAM2-040920.xml', 'HAM2-041025.xml', 'HAM2-041026.xml', 'HAM2-041027.xml', 'HAM2-041230.xml', 'HAM2-041231.xml', 'HAM2-050101.xml', 'HAM2-050102.xml', 'HAM2-050223.xml', 'HAM2-050224.xml', 'HAM2-050406.xml', 'HAM2-050407.xml', 'HAM2-050416.xml'])
		self._paragraph_pattern = re.compile(r'(\n.{0,50})(?=\n)')

	def docs(self):
		for root, dirs, files in os.walk(self._root):
			for name in sorted(files):
				if name in self._invalids:
					continue

				try:
					elements = minidom.parse(os.path.join(root, name))
					for element in elements.getElementsByTagName('DOC'):
						doc = {}
						doc['id'] = element.getElementsByTagName('DOCID')[0].childNodes[0].data
						doc['issue'] = element.getElementsByTagName('ISSUE')[0].childNodes[0].data

						for cat in element.getElementsByTagName('CAT'):
							doc['categories_'+ cat.attributes['xml:lang'].value] = cat.childNodes[0].data.split('.')

						elm = element.getElementsByTagName('TITLE')[0]
						doc['title'] = elm.childNodes[1].data if len(elm.childNodes) > 1 else ''

						doc['text'] = ''
						for item in element.getElementsByTagName('TEXT')[0].childNodes:
							if item.nodeType == 4:  # CDATA
								doc['text'] += item.data

						# refine text
						doc['text'] = self._paragraph_pattern.sub(r'\1\n', doc['text']).replace('\no ', '\n')

						yield doc

				except Exception as e:
					print('error in reading', name, e, file=sys.stderr)

	def texts(self):
		for doc in self.docs():
			yield doc['text']
