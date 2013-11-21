#coding=utf8

from .utils import u
maketrans = lambda A, B: dict((ord(a), b) for a, b in zip(A, B))


class Normalizer():
	def __init__(self):
		self.translations = maketrans(u('كي%1234567890'), u('کی٪۱۲۳۴۵۶۷۸۹۰'))

	def normalize(self, text):
		text = self.refine_characters(text)
		return text

	def refine_characters(self, text):
		"""
		>>> normalizer.refine_characters('اصلاح كاف و ياي عربي')
		'اصلاح کاف و یای عربی'
		"""
		text = text.translate(self.translations)
		return text


if __name__ == '__main__':
	import doctest
	doctest.testmod(extraglobs={'normalizer': Normalizer()})
