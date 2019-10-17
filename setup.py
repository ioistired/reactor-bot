#!/usr/bin/env python3
# encoding: utf-8

import setuptools

setuptools.setup(
	name='reactor_bot',
	version='4.5.15',
	url='https://github.com/iomintz/reactor-bot',

	author='Io Mintz',
	author_email='io@mintz.cc',

	description='The best dang Discord poll bot around™',
	long_description=open('README.rst').read(),

	packages=[
		'reactor_bot',
		'reactor_bot.cogs'],

	install_requires=[
		'asyncpg',
		'bot_bin[sql]>=1.0.1,<2.0.0',
		'discord.py>=1.2.3,<2.0.0',
		'inflect',
		'jishaku'],

	python_requires='>=3.6',

	extras_require={
		'dev': [
			'bumpversion'],

		'test': [
			'pytest',
			'pytest-cov',
			'freezegun']},

	classifiers=[
		'Development Status :: 4 - Beta',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'License :: OSI Approved :: MIT License'])
