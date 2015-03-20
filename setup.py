
from distutils.core import setup

setup(name='hazm',
	version='0.5',
	description='Python library for digesting Persian text.',
	author='Alireza Nourian',
	author_email='az.nourian@gmail.com',
	url='http://www.sobhe.ir/hazm/',
	packages=['hazm'],
	package_data={'hazm': ['data/*.dat']},
	classifiers=[
		'Topic :: Text Processing',
		'Natural Language :: Persian',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.2',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'License :: OSI Approved :: MIT License',
	],
	install_requires=['nltk>=3.0.2', 'libwapiti>=0.2.1']
)
