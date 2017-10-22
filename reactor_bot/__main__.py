#!/usr/bin/env python3
# encoding: utf-8

from . import bot

from configparser import ConfigParser
from appdirs import AppDirs
import os.path

import sys


def main():

	dirs = AppDirs('reactor-bot', 'bmintz')
	config = ConfigParser()
	config.read(os.path.join(dirs.user_config_dir, 'reactor-bot.ini'))

	bot.config = config
	bot.load_extension('reactor_bot.stats')
	bot.run(config['discord']['api_token'])

	return 0


sys.exit(main())
