#!/usr/bin/env python3
# encoding: utf-8

import json
import logging
import os.path
import sys

from . import bot


def main():
	with open('data/config.json') as config_file:
		bot.config = json.load(config_file)
	bot.dev_mode = bot.config['release'] == 'development'

	# place the extensions in order of priority
	for extension in (
			'reactor_bot.cogs.poll',
			'reactor_bot.cogs.meta',
			'jishaku',
			'reactor_bot.cogs.external.admin',
			'reactor_bot.cogs.external.stats',
			'reactor_bot.cogs.external.misc'):
		print('Loading extension', extension, file=sys.stderr)
		try:
			bot.load_extension(extension)
		except Exception as e:
			exc = '%s: %s' % (type(e).__name__, e)
			print('Failed to load extension %s\n%s' % (extension, exc), file=sys.stderr)

	bot.run(bot.config['tokens']['discord'])
	return 0


sys.exit(main())
