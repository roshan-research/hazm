# -*- coding: utf-8 -*-
import codecs

from hazm.Normalizer import Normalizer
from .utils import default_stop_words


class StopWord:
	def __init__(self, file_path=default_stop_words, normal=False):
		self.stop_words = self.init(file_path, normal)
		self.normalizer = Normalizer()

	def init(self, file_path, normal):
		if not normal:
			return set(
					line.strip("\r\n") for line in codecs.open(file_path, "r", ).readlines())
		else:
			return set(
					self.normalizer.normalize(line.strip("\r\n")) for line in codecs.open(file_path, "r", ).readlines())

	def __getitem__(self, item):
		return item in self.stop_words

	def __str__(self):
		return str(self.stop_words)

	def clean(self, iterable_of_strings, return_generator=False):
		if return_generator:
			return filter(lambda item: not self[item], iterable_of_strings)
		else:
			return list(filter(lambda item: not self[item], iterable_of_strings))


