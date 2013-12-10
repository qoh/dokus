#!/usr/bin/env python
from distutils.core import setup

setup(
	name='dokus',
	version='0.0.1',
	description='TorqueScript documentation generator',
	long_description='Dokus is a Python utility and package for generating HTML documentation or extracting data from a source tree, file or blob.',
	author='portify',
	author_email='portification@gmail.com',
	url='https://github.com/portify/dokus',
	license='MIT',
	packages=['dokus'],

	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python',
		'Programming Language :: Other',
		'Topic :: Documentation',
		'Topic :: Software Development :: Documentation'
	]
)