
from distutils.core import setup

setup(name='hazm',
	version='0.1',
	description='Python library for digesting Persian text.',
	author='Alireza Nourian',
	author_email='alireza.nournia@gmail.com',
	url='https://github.com/nournia/hazm',
	packages=['hazm'],
	package_data={'hazm': ['data/*.dat']},
	classifiers=[
		'Topic :: Text Processing',
		'Natural Language :: Persian',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.3',
		'License :: OSI Approved :: MIT License',
	],
	install_requires=['nltk']
)
