#!/usr/bin/env python3
# encoding: utf-8

from . import bot

from appdirs import AppDirs
import os.path
import json
import sys


def main():
	dirs = AppDirs('reactor-bot', 'bmintz')
	bot.cogs_path = 'reactor_bot.cogs'

	with open(os.path.join(dirs.user_config_dir, 'config.json')) as config_file:
		config = json.load(config_file)
	bot.config = config

	# place the extensions in order of priority
	for extension in ('poll', 'meta', 'external.admin', 'external.stats', 'external.misc'):
		print('Loading extension', extension, file=sys.stderr)
		try:
			bot.load_extension(bot.cogs_path + '.' + extension)
		except Exception as e:
			exc = '%s: %s' % (type(e).__name__, e)
			print('Failed to load extension %s\n%s' % (extension, exc), file=sys.stderr)

	try:
		bot.run(config['tokens']['discord'])
	except:
		return 1
	else:
		return 0


sys.exit(main())
