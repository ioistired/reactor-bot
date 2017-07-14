import setuptools

setuptools.setup(
	name='poll_bot',
	version='2.0.0',
	url='https://github.com/bmintz/poll-bot',

	author='Benjamin Mintz',
	author_email='bmintz@protonmail.com',

	description='A simple reaction-based Discord poll bot',
	long_description=open('README.rst').read(),

	packages=setuptools.find_packages(),

	install_requires=['discord.py'],

	extras_require={
		'dev': [
			'bumpversion',
		],
	},

	entry_points={
		'console_scripts': 'poll-bot = poll_bot.__main__:main',
	},

	classifiers=[
		'Development Status :: 4 - Beta',
		'Programming Language :: Python',
		'Programming Language :: Python :: 3.5',
		'License :: OSI Approved :: MIT License',
	],
)
