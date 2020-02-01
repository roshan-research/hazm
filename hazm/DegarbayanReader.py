# coding: utf-8

from __future__ import unicode_literals, print_function
import os
from xml.dom import minidom

class DegarbayanReader():
	"""
	interfaces [Degarbayan Corpus](https://www.peykaregan.ir/dataset/%D9%BE%DB%8C%DA%A9%D8%B1%D9%87-%D8%AF%DA%AF%D8%B1%D8%A8%DB%8C%D8%A7%D9%86)
	معانی‌جو، ر.، و میرروشندل، س.ا. (۱۳۹۶). دگربیان: توسعه پیکره متنی فارسی جملات و عبارات معادل به کمک روش جمع‌سپاری. علوم رایانش و فناوری اطلاعات، ۱۵ (۱)، ۲۲-۳۰.

	>>> degarbayan = DegarbayanReader(root='corpora/degarbayan')
	>>> next(degarbayan.pairs())
	('24 نفر نهایی تیم ملی بدون تغییری خاص معرفی شد', 'کی روش 24 بازیکن را به تیم ملی فوتبال دعوت کرد', 'Paraphrase')
	"""

	def __init__(self, root, corpus_file='CorpusPair.xml', judge_type='three_class', version=1.0):
		"""
		:param root: Path to corpus folder.
		:param corpus_file: Name of corpus pair file. Defaults to 'CorpusPair.xml'
		:param judge_type: How to return judge value. can be eighter 'two_class' or 'three_class'
				for two or three class value returns. Defaults to 'three_class'
		:param version: Corpus version. Defaults to version 1.0
		:type root: str
		:type corpuse_file: str
		:type judge_type: str
		:type version: float
		"""
		self._root = root
		self._corpus_file = corpus_file
		self._judge_type = judge_type
		if judge_type != 'three_class' and judge_type != 'two_class':
			self._judge_type = 'three_class'

	def docs(self):
	
		def judge_number_to_text(judge):
			if judge == '1' or (self._judge_type == 'two_class' and judge == '0'):
				return 'Paraphrase'
			elif judge == '0':
				return 'SemiParaphrase'
			else:
				return 'NotParaphrase'
		
		filename = os.path.join(self._root, self._corpus_file)
		if os.path.exists(filename):
			try:
				elements = minidom.parse(filename)
				for element in elements.getElementsByTagName('Pair'):
					pair = {}
					pair['id'] = element.getElementsByTagName('PairId')[0].childNodes[0].data.strip()
					pair['news_source1'] = element.getElementsByTagName('NewsSource1')[0].childNodes[0].data.strip()
					pair['news_source2'] = element.getElementsByTagName('NewsSource2')[0].childNodes[0].data.strip()
					pair['news_id1'] = element.getElementsByTagName('NewsId1')[0].childNodes[0].data.strip()
					pair['news_id2'] = element.getElementsByTagName('NewsId2')[0].childNodes[0].data.strip()
					pair['sentence1'] = element.getElementsByTagName('Sentence1')[0].childNodes[0].data.strip()
					pair['sentence2'] = element.getElementsByTagName('Sentence2')[0].childNodes[0].data.strip()
					pair['method_type'] = element.getElementsByTagName('MethodType')[0].childNodes[0].data.strip()
					pair['judge'] = judge_number_to_text(element.getElementsByTagName('judge')[0].childNodes[0].data.strip())
					yield pair
			
			except Exception as e:
				print('error in reading', filename, e, file=sys.stderr)
		else:
			print('error in reading file', filename, e, file=sys.stderr)
			raise FileNotFoundError('error in reading file', filename)

	def pairs(self):
		for pair in self.docs():
			yield pair['sentence1'], pair['sentence2'], pair['judge']
