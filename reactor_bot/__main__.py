#!/usr/bin/env python3
# encoding: utf-8

import logging

from reactor_bot import ReactorBot

bot = ReactorBot()

def main():  # put it in a main function so that setuptools can create a launch script
	# place the extensions in order of priority
	for extension in (
		'reactor_bot.cogs.db',
		'reactor_bot.cogs.poll',
		'reactor_bot.cogs.meta',
		'jishaku',
		'ben_cogs.stats',
		'ben_cogs.debug',
		'ben_cogs.misc',
	):
		logging.info('Loading extension %s', extension)
		bot.load_extension(extension)

	bot.run(bot.config['tokens']['discord'])

main()
