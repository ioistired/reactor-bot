#!/usr/bin/env python3
# encoding: utf-8

import setuptools

setuptools.setup(
	name='reactor_bot',
	version='4.5.15',
	url='https://github.com/bmintz/reactor-bot',

	author='Benjamin Mintz',
	author_email='bmintz@protonmail.com',

	description='The best dang Discord poll bot around™',
	long_description=open('README.rst').read(),

	packages=[
		'reactor_bot',
		'reactor_bot.cogs'],

	install_requires=[
		'asyncpg',
		'ben_cogs[sql]',
		'discord.py',
		'inflect',
		'jishaku'],

	python_requires='>=3.6',

	extras_require={
		'dev': [
			'bumpversion'],

		'test': [
			'tox',
			'pytest',
			'pytest-cov',
			'freezegun']},

	classifiers=[
		'Development Status :: 4 - Beta',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.6',
		'License :: OSI Approved :: MIT License'])
