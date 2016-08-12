# coding: utf8
from __future__ import unicode_literals
import codecs
from hazm.Normalizer import Normalizer
from .utils import default_stop_words


class StopWord:
	""" Class for remove stop words

		 >>> StopWord().clean(["بودی؟","مشهد","در","کی"])
		 ['بودی؟', 'مشهد', 'کی']
		 >>> StopWord(normal=True).clean(["بودی؟","مشهد","در","کی"])
		 ['بودی؟', 'مشهد']

		 """
	def __init__(self, file_path=default_stop_words, normal=False):
		self.file_path = file_path
		self.normal = normal
		self.normalizer = Normalizer().normalize
		self.stop_words = self.init(file_path, normal)

	def init(self, file_path, normal):
		if not normal:
			return set(
					line.strip("\r\n") for line in codecs.open(file_path, "r",encoding="utf-8" ).readlines())
		else:
			return set(
					self.normalizer(line.strip("\r\n")) for line in codecs.open(file_path, "r",encoding="utf-8").readlines())

	def set_normalizer(self, func):
		self.normalizer = func
		self.stop_words = self.init(self.file_path,self.normal)

	def __getitem__(self, item):
		return item in self.stop_words

	def __str__(self):
		return str(self.stop_words)

	def clean(self, iterable_of_strings, return_generator=False):
		if return_generator:
			return filter(lambda item: not self[item], iterable_of_strings)
		else:
			return list(filter(lambda item: not self[item], iterable_of_strings))

