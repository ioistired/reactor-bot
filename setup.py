import setuptools


setuptools.setup(
	name='reactor_bot',
	version='4.5.12',
	url='https://github.com/bmintz/reactor-bot',

	author='Benjamin Mintz',
	author_email='bmintz@protonmail.com',

	description='The best dang Discord poll bot around™',
	long_description=open('README.rst').read(),

	packages=setuptools.find_packages(),

	install_requires=[
		'ben_cogs',
		'discord.py>=1.0.0a1430',
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

	entry_points={
		'console_scripts': 'reactor-bot = reactor_bot.__main__:main'},

	classifiers=[
		'Development Status :: 4 - Beta',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.6',
		'License :: OSI Approved :: MIT License'])
